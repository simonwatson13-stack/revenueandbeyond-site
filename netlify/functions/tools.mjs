// Tools and kits shop (/tools/). Three routes:
//
// POST /api/tools/lead     {product, email, first_name?, website?}  -> {ok, url?}
//   Free tools and waitlists. Saves the lead in Netlify Blobs (store "tools-leads", key = email)
//   and adds it to The Founder Read on beehiiv (same env vars as /api/blueprint). If the product
//   is a free tool with a file, returns its download url.
//
// GET  /api/tools/order?session_id=cs_...                        -> {ok, product:{id,name,format}, download}
//   Called by /tools/thanks/ after a Stripe Payment Link redirects there. Checks the Checkout
//   Session with Stripe (STRIPE_SECRET_KEY, a restricted key with read access to Checkout
//   Sessions is enough), matches its payment_link to a product in data/products.json, and
//   records the order in Netlify Blobs (store "orders", key = session id).
//
// GET  /api/tools/download?session_id=cs_...                     -> the kit file
//   Same check, then streams the file from kits/ (bundled with this function, never published
//   on the site). Limited to MAX_DOWNLOADS per order.
//
// Stripe set-up per kit: Payment Link > After payment > "Don't show confirmation page" >
// redirect to https://revenueandbeyond.com/tools/thanks/?session_id={CHECKOUT_SESSION_ID}
import { getStore } from "@netlify/blobs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import catalogue from "../../data/products.json";

const MAX_DOWNLOADS = 10;
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[a-z]{2,}$/i;
const SESSION_RE = /^cs_(test_|live_)?[A-Za-z0-9]{10,200}$/;
const PRODUCTS = catalogue.products;

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

async function checkSession(id) {
  if (!SESSION_RE.test(id || "")) return { error: [400, "Missing or invalid order reference."] };
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return { error: [503, "Checkout is not set up yet."] };
  let s;
  try {
    const r = await fetch(`https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(id)}`, {
      headers: { authorization: `Bearer ${key}` },
    });
    if (r.status === 404) return { error: [404, "I couldn't find that order."] };
    if (!r.ok) return { error: [502, "Stripe could not be reached. Please try again in a minute."] };
    s = await r.json();
  } catch {
    return { error: [502, "Stripe could not be reached. Please try again in a minute."] };
  }
  if (s.payment_status !== "paid" && s.payment_status !== "no_payment_required")
    return { error: [402, "This order has not been paid yet."] };
  const product = PRODUCTS.find(
    (p) => p.kind === "kit" && p.stripePaymentLinkId && p.stripePaymentLinkId === s.payment_link
  );
  if (!product || !product.file) return { error: [404, "This order doesn't match a kit. Email me and I'll sort it."] };
  return { session: s, product };
}

async function recordOrder(s, product, isDownload) {
  const store = getStore({ name: "orders", consistency: "strong" });
  let rec = null;
  try {
    rec = await store.get(s.id, { type: "json" });
  } catch {}
  rec = rec || {
    session: s.id,
    product: product.id,
    email: (s.customer_details && s.customer_details.email) || "",
    name: (s.customer_details && s.customer_details.name) || "",
    amount: s.amount_total,
    currency: s.currency,
    first: new Date().toISOString(),
    downloads: 0,
  };
  if (isDownload) {
    if (rec.downloads >= MAX_DOWNLOADS) return { rec, blocked: true };
    rec.downloads += 1;
    rec.last = new Date().toISOString();
  }
  try {
    await store.setJSON(s.id, rec);
  } catch {}
  return { rec, blocked: false };
}

async function lead(req) {
  if (req.method !== "POST") return json(405, { error: "POST only" });
  let body;
  try {
    body = await req.json();
  } catch {
    return json(400, { error: "Bad request" });
  }
  if (body.website) return json(200, { ok: true }); // honeypot
  const product = PRODUCTS.find((p) => p.id === String(body.product || ""));
  if (!product) return json(400, { error: "Unknown product." });
  const email = String(body.email || "").trim().toLowerCase().slice(0, 254);
  const firstName = String(body.first_name || "").trim().slice(0, 80);
  if (!EMAIL_RE.test(email)) return json(400, { error: "Please enter a valid email address." });

  const freeFile = product.kind === "free" && product.status === "live" && product.file;
  const type = freeFile ? "download" : "waitlist";
  const at = new Date().toISOString();
  const store = getStore({ name: "tools-leads", consistency: "strong" });
  let rec = null;
  try {
    rec = await store.get(email, { type: "json" });
  } catch {}
  rec = rec || { email, first: at, items: {} };
  rec.firstName = firstName || rec.firstName || "";
  rec.last = at;
  rec.items[product.id] = { type, at };

  const key = process.env.BEEHIIV_API_KEY;
  const pub = process.env.BEEHIIV_PUBLICATION_ID;
  if (key && pub && rec.beehiiv !== "added") {
    try {
      const payload = {
        email,
        reactivate_existing: false,
        send_welcome_email: true,
        utm_source: "tools",
        utm_medium: "website",
        utm_campaign: `tools-${product.id}`,
        referring_site: "revenueandbeyond.com/tools/",
      };
      const res = await fetch(`https://api.beehiiv.com/v2/publications/${pub}/subscriptions`, {
        method: "POST",
        headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      rec.beehiiv = res.ok ? "added" : `error ${res.status}`;
    } catch {
      rec.beehiiv = "error network";
    }
  } else if (!key || !pub) {
    rec.beehiiv = rec.beehiiv || "not configured";
  }
  try {
    await store.setJSON(email, rec);
  } catch {}
  return json(200, { ok: true, type, url: freeFile ? `/assets/downloads/${product.file}` : null });
}

async function order(req) {
  const id = new URL(req.url).searchParams.get("session_id");
  const c = await checkSession(id);
  if (c.error) return json(c.error[0], { error: c.error[1] });
  const { rec } = await recordOrder(c.session, c.product, false);
  return json(200, {
    ok: true,
    product: { id: c.product.id, name: c.product.name, format: c.product.format },
    email: rec.email,
    downloadsLeft: Math.max(0, MAX_DOWNLOADS - rec.downloads),
    download: `/api/tools/download?session_id=${encodeURIComponent(c.session.id)}`,
  });
}

async function download(req) {
  const id = new URL(req.url).searchParams.get("session_id");
  const c = await checkSession(id);
  if (c.error) return json(c.error[0], { error: c.error[1] });
  const { blocked } = await recordOrder(c.session, c.product, true);
  if (blocked) return json(429, { error: "Download limit reached for this order. Email me and I'll send it." });
  const name = path.basename(c.product.file);
  let buf;
  try {
    buf = await readFile(path.join(process.cwd(), "kits", name));
  } catch {
    return json(503, { error: "The file isn't ready yet. Email me and I'll send it." });
  }
  return new Response(buf, {
    status: 200,
    headers: {
      "content-type": name.endsWith(".pdf") ? "application/pdf" : "application/zip",
      "content-disposition": `attachment; filename="${name}"`,
      "cache-control": "private, no-store",
      "x-robots-tag": "noindex",
    },
  });
}

export default async (req) => {
  const p = new URL(req.url).pathname.replace(/\/+$/, "");
  if (p.endsWith("/lead")) return lead(req);
  if (p.endsWith("/order")) return order(req);
  if (p.endsWith("/download")) return download(req);
  return json(404, { error: "Not found" });
};

export const config = { path: ["/api/tools/lead", "/api/tools/order", "/api/tools/download"] };
