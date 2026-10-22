// Private deal pipeline API for /pipeline-…/ (Simon only).
// GET  -> returns the board (your saved edits merged with the latest weekly sweep).
// PUT  -> saves the board.
// Every request must carry the passcode in the x-pipeline-key header.
// The passcode lives in the Netlify environment variable PIPELINE_PASSCODE.
// Data is stored in Netlify Blobs (store "pipeline", key "board"), never in the public site.
import { getStore } from "@netlify/blobs";
import { createHash, timingSafeEqual } from "node:crypto";
import feed from "../../data/pipeline-feed.json";

const STORE = "pipeline";
const KEY = "board";
// Fields the weekly sweep is allowed to set on a deal you have not touched.
const SWEEP_FIELDS = ["company", "contact", "line", "stage", "mrr", "source", "nextAction", "nextDate", "notes", "evidence", "outcome", "risk"];
// Fields worth suggesting when you have edited a deal and the sweep disagrees.
const SUGGEST_FIELDS = ["stage", "mrr", "nextAction", "nextDate", "notes"];

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store", "x-robots-tag": "noindex" },
  });

const digest = (s) => createHash("sha256").update(String(s)).digest();

function authorised(req) {
  const expected = process.env.PIPELINE_PASSCODE;
  if (!expected || expected.length < 8) return "unconfigured";
  const given = req.headers.get("x-pipeline-key") || "";
  return timingSafeEqual(digest(given), digest(expected)) ? "ok" : "denied";
}

function snapshot(fd) {
  const o = {};
  for (const f of SUGGEST_FIELDS) if (f in fd) o[f] = fd[f];
  return o;
}

function mergeFeed(state) {
  if (!feed || !Array.isArray(feed.deals)) return state;
  if (state.feedVersion === feed.version) return state;
  const deleted = new Set(state.deleted || []);
  const byId = new Map(state.deals.map((d) => [d.id, d]));
  for (const fd of feed.deals) {
    if (!fd.id || deleted.has(fd.id)) continue;
    const cur = byId.get(fd.id);
    if (!cur) {
      const fresh = { ...fd, edited: false, addedBy: "sweep", addedAt: feed.version, swept: snapshot(fd) };
      state.deals.push(fresh);
      byId.set(fd.id, fresh);
      continue;
    }
    // Last touch is a fact, so always take the newer date.
    if (fd.lastTouch && (!cur.lastTouch || fd.lastTouch > cur.lastTouch)) cur.lastTouch = fd.lastTouch;
    if (!cur.edited) {
      for (const f of SWEEP_FIELDS) if (f in fd) cur[f] = fd[f];
      delete cur.suggestion;
    } else {
      // Only suggest what the sweep has changed its mind about since last week,
      // so a deal you deliberately moved is not nagged every Monday.
      const prev = cur.swept || {};
      const s = {};
      for (const f of SUGGEST_FIELDS) {
        if (!(f in fd)) continue;
        const changedBySweep = JSON.stringify(fd[f]) !== JSON.stringify(prev[f]);
        const differsFromYou = JSON.stringify(fd[f]) !== JSON.stringify(cur[f]);
        if (changedBySweep && differsFromYou) s[f] = fd[f];
      }
      if (Object.keys(s).length) cur.suggestion = { ...(cur.suggestion || {}), ...s, from: feed.version };
    }
    cur.swept = snapshot(fd);
  }
  state.feedVersion = feed.version;
  return state;
}

async function load(store) {
  const saved = await store.get(KEY, { type: "json" });
  return saved && Array.isArray(saved.deals)
    ? saved
    : { deals: [], deleted: [], feedVersion: null, updatedAt: null };
}

export default async (req) => {
  const auth = authorised(req);
  if (auth === "unconfigured") return json(503, { error: "Passcode not set. Add PIPELINE_PASSCODE (8+ characters) in Netlify, then redeploy." });
  if (auth !== "ok") {
    await new Promise((r) => setTimeout(r, 800));
    return json(401, { error: "Wrong passcode." });
  }

  const store = getStore({ name: STORE, consistency: "strong" });

  if (req.method === "GET") {
    const before = await load(store);
    const prevVersion = before.feedVersion;
    const state = mergeFeed(before);
    if (state.feedVersion !== prevVersion) {
      state.updatedAt = new Date().toISOString();
      await store.setJSON(KEY, state);
    }
    return json(200, state);
  }

  if (req.method === "PUT") {
    let body;
    try {
      body = await req.json();
    } catch {
      return json(400, { error: "Bad JSON." });
    }
    if (!body || !Array.isArray(body.deals)) return json(400, { error: "Missing deals." });
    if (JSON.stringify(body).length > 900_000) return json(413, { error: "Board too large." });
    const current = await load(store);
    if (current.updatedAt && body.baseUpdatedAt !== current.updatedAt) {
      return json(409, { error: "The board changed since you opened it. Reloaded the latest version.", state: mergeFeed(current) });
    }
    const next = mergeFeed({
      deals: body.deals,
      deleted: Array.isArray(body.deleted) ? body.deleted : current.deleted || [],
      feedVersion: current.feedVersion,
      updatedAt: new Date().toISOString(),
    });
    await store.setJSON(KEY, next);
    return json(200, next);
  }

  return json(405, { error: "Method not allowed." });
};

export const config = { path: "/api/pipeline" };
