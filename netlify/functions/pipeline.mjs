// Private deal pipeline API for /pipeline-…/ (Simon only).
// GET  -> returns the board (your saved edits merged with the latest weekly sweep).
// PUT  -> saves the board.
// Every request must carry the passcode in the x-pipeline-key header.
// The passcode lives in the Netlify environment variable PIPELINE_PASSCODE.
// Data is stored in Netlify Blobs (store "pipeline", key "board"), never in the public site.
// Newsletter: every deal email is added to The Founder Read on beehiiv (welcome email on),
// unless the deal is set to "Don't add". Needs BEEHIIV_API_KEY and BEEHIIV_PUBLICATION_ID
// in Netlify; without them nothing is sent. Each address is only ever submitted once, and
// beehiiv is told not to reactivate anyone who has unsubscribed.
import { getStore } from "@netlify/blobs";
import { createHash, timingSafeEqual } from "node:crypto";
import feed from "../../data/pipeline-feed.json";

const STORE = "pipeline";
const KEY = "board";
// Fields the weekly sweep is allowed to set on a deal you have not touched.
const SWEEP_FIELDS = ["company", "contact", "email", "line", "stage", "mrr", "source", "nextAction", "nextDate", "notes", "evidence", "outcome", "risk"];
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
    // An email address the sweep found fills an empty field even on deals you have edited.
    if (fd.email && !cur.email) cur.email = fd.email;
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

const EMAIL_RE = /^[^\s@<>(),;:"]+@[^\s@<>(),;:"]+\.[a-z]{2,}$/i;
const RETRY_MS = 24 * 3600 * 1000;
const PER_REQUEST = 15;

function emailsOf(deal) {
  return String(deal.email || "")
    .split(/[;,\s]+/)
    .map((e) => e.trim().toLowerCase())
    .filter((e) => EMAIL_RE.test(e));
}

async function syncNewsletter(state) {
  const key = process.env.BEEHIIV_API_KEY;
  const pub = process.env.BEEHIIV_PUBLICATION_ID;
  state.newsletter = state.newsletter || {};
  state.newsletterConfigured = Boolean(key && pub);
  if (!key || !pub) return false;
  const now = Date.now();
  const todo = [];
  for (const d of state.deals) {
    if (d.noNewsletter) continue;
    for (const email of emailsOf(d)) {
      const rec = state.newsletter[email];
      if (rec && (rec.status === "added" || now - Date.parse(rec.at) < RETRY_MS)) continue;
      if (!todo.includes(email)) todo.push(email);
    }
  }
  if (!todo.length) return false;
  const results = await Promise.allSettled(
    todo.slice(0, PER_REQUEST).map(async (email) => {
      const res = await fetch(`https://api.beehiiv.com/v2/publications/${pub}/subscriptions`, {
        method: "POST",
        headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
        body: JSON.stringify({
          email,
          reactivate_existing: false,
          send_welcome_email: true,
          utm_source: "rnb-pipeline",
          utm_medium: "pipeline",
          referring_site: "revenueandbeyond.com",
        }),
      });
      let msg = "";
      if (!res.ok) {
        try { msg = JSON.stringify(await res.json()).slice(0, 200); } catch { msg = res.statusText; }
      }
      return { email, ok: res.ok, code: res.status, msg };
    })
  );
  const at = new Date().toISOString();
  for (const r of results) {
    if (r.status !== "fulfilled") continue;
    const { email, ok, code, msg } = r.value;
    state.newsletter[email] = ok ? { status: "added", at } : { status: "error", at, code, msg };
  }
  return true;
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
    const sent = await syncNewsletter(state);
    if (sent || state.feedVersion !== prevVersion) {
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
      newsletter: current.newsletter || {},
      updatedAt: new Date().toISOString(),
    });
    await syncNewsletter(next);
    await store.setJSON(KEY, next);
    return json(200, next);
  }

  return json(405, { error: "Method not allowed." });
};

export const config = { path: "/api/pipeline" };
