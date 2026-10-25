// /api/brief : Simon's daily brief (private).
// GET  -> { brief, state }                    header x-pipeline-key required
// POST {type:"publish", brief}                 the morning scheduled task stores today's brief
// POST {type:"state", id, status, until, title, seen}
//                                              the page marks an item done, snoozed or open again
// Storage: Netlify Blobs, store "brief", keys "latest" and "state".
// Auth: same passcode as the pipeline board (env PIPELINE_PASSCODE).
import { getStore } from "@netlify/blobs";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

const ok = (req) => {
  const key = process.env.PIPELINE_PASSCODE;
  return Boolean(key) && req.headers.get("x-pipeline-key") === key;
};

const ID = /^[A-Za-z0-9:_.\-]{1,200}$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;

export default async (req) => {
  if (!ok(req)) return json({ error: "unauthorised" }, 401);
  const store = getStore("brief");

  if (req.method === "GET") {
    const [brief, state] = await Promise.all([
      store.get("latest", { type: "json" }),
      store.get("state", { type: "json" }),
    ]);
    return json({ brief: brief || null, state: state || { items: {} } });
  }

  if (req.method !== "POST") return json({ error: "method not allowed" }, 405);

  let body;
  try { body = await req.json(); } catch { return json({ error: "bad json" }, 400); }

  if (body.type === "publish") {
    const b = body.brief;
    if (!b || typeof b !== "object" || !DAY.test(b.date || "")) return json({ error: "brief.date missing" }, 400);
    const size = JSON.stringify(b).length;
    if (size > 900000) return json({ error: "brief too large" }, 413);
    b.publishedAt = new Date().toISOString();
    await store.setJSON("latest", b);
    return json({ ok: true, date: b.date, size });
  }

  if (body.type === "state") {
    const { id, status } = body;
    if (!ID.test(id || "")) return json({ error: "bad id" }, 400);
    if (!["done", "snoozed", "open"].includes(status)) return json({ error: "bad status" }, 400);
    if (status === "snoozed" && !DAY.test(body.until || "")) return json({ error: "until required" }, 400);
    const state = (await store.get("state", { type: "json" })) || { items: {} };
    if (status === "open") {
      delete state.items[id];
    } else {
      state.items[id] = {
        status,
        until: status === "snoozed" ? body.until : null,
        at: new Date().toISOString(),
        title: String(body.title || "").slice(0, 200),
        seen: String(body.seen || "").slice(0, 40), // item's last-activity stamp when actioned
      };
    }
    // Keep the file small: drop done items older than 60 days and expired snoozes older than 30.
    const now = Date.now();
    for (const [k, v] of Object.entries(state.items)) {
      const age = (now - Date.parse(v.at)) / 864e5;
      if ((v.status === "done" && age > 60) || (v.status === "snoozed" && age > 30 && v.until < new Date().toISOString().slice(0, 10))) delete state.items[k];
    }
    state.updatedAt = new Date().toISOString();
    await store.setJSON("state", state);
    return json({ ok: true, item: state.items[id] || null });
  }

  return json({ error: "unknown type" }, 400);
};

export const config = { path: "/api/brief" };
