// Gated download for the founder-led sales blueprint (/blueprint/).
// POST {email, first_name?, website?} -> {ok:true}
// 1. Every valid email is saved first in Netlify Blobs (store "leads", key = the email), so no
//    lead is lost even if beehiiv is down or not configured.
// 2. The email is then added to The Founder Read on beehiiv (welcome email on, tagged with
//    utm_source "blueprint"). Needs BEEHIIV_API_KEY and BEEHIIV_PUBLICATION_ID in Netlify (the
//    same two variables the pipeline uses). Unsubscribed people are never reactivated.
// "website" is a honeypot field: real people never see it, bots fill it in.
import { getStore } from "@netlify/blobs";

const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[a-z]{2,}$/i;

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "POST only" });
  let body;
  try {
    body = await req.json();
  } catch {
    return json(400, { error: "Bad request" });
  }
  // Bot filled the hidden field: pretend it worked, store nothing.
  if (body.website) return json(200, { ok: true });

  const email = String(body.email || "").trim().toLowerCase().slice(0, 254);
  const firstName = String(body.first_name || "").trim().slice(0, 80);
  if (!EMAIL_RE.test(email)) return json(400, { error: "Please enter a valid email address." });

  const at = new Date().toISOString();
  const referrer = String(body.ref || "").slice(0, 300);
  const store = getStore({ name: "leads", consistency: "strong" });
  let rec = null;
  try {
    rec = await store.get(email, { type: "json" });
  } catch {}
  rec = rec || { email, first: at, source: "blueprint" };
  rec.firstName = firstName || rec.firstName || "";
  rec.last = at;
  rec.downloads = (rec.downloads || 0) + 1;
  if (referrer) rec.referrer = referrer;

  const key = process.env.BEEHIIV_API_KEY;
  const pub = process.env.BEEHIIV_PUBLICATION_ID;
  if (key && pub && rec.beehiiv !== "added") {
    try {
      const payload = {
        email,
        reactivate_existing: false,
        send_welcome_email: true,
        utm_source: "blueprint",
        utm_medium: "website",
        utm_campaign: "founder-led-sales-blueprint",
        referring_site: "revenueandbeyond.com/blueprint/",
      };
      if (firstName) payload.custom_fields = [{ name: "First Name", value: firstName }];
      let res = await fetch(`https://api.beehiiv.com/v2/publications/${pub}/subscriptions`, {
        method: "POST",
        headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      // If the custom field doesn't exist on the publication, retry without it.
      if (!res.ok && payload.custom_fields) {
        delete payload.custom_fields;
        res = await fetch(`https://api.beehiiv.com/v2/publications/${pub}/subscriptions`, {
          method: "POST",
          headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
          body: JSON.stringify(payload),
        });
      }
      rec.beehiiv = res.ok ? "added" : `error ${res.status}`;
    } catch (e) {
      rec.beehiiv = "error network";
    }
  } else if (!key || !pub) {
    rec.beehiiv = rec.beehiiv || "not configured";
  }

  try {
    await store.setJSON(email, rec);
  } catch {}
  // The visitor always gets the guide once the email is valid.
  return json(200, { ok: true, url: "/assets/downloads/founder-led-sales-blueprint.pdf" });
};

export const config = { path: "/api/blueprint" };
