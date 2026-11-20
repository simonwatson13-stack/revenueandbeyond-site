// Password gate for the Founder Portal (/founder-portal/ and everything under it,
// including the demos and the Founder Line page). The thanks page stays open because
// Stripe sends buyers there with a session id.
//
// Set the password in Netlify: Project configuration > Environment variables >
// PORTAL_PASSWORD (8+ characters), then redeploy. Changing it signs everyone out.
// Until it is set, the portal shows a "not available" page to everyone (fails closed).
//
// A correct password sets a signed cookie for 30 days, so clients only enter it once
// per browser. Nothing else on the site is affected.

import type { Config, Context } from "https://edge.netlify.com";

const COOKIE = "rb_portal";
const MAX_AGE = 60 * 60 * 24 * 30;

async function sign(secret: string, msg: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function same(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

function cookieValue(req: Request, name: string): string {
  const raw = req.headers.get("cookie") || "";
  for (const part of raw.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === name) return v.join("=");
  }
  return "";
}

function page(status: number, opts: { error?: string; unconfigured?: boolean; next?: string }): Response {
  const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c] as string));
  const body = opts.unconfigured
    ? `<p class="lead">The Founder Portal isn't open yet. If you're a client, I'll send you access shortly.</p>`
    : `<p class="lead">This area is for clients of Revenue &amp; Beyond. Enter the password I sent you.</p>
       <form method="post" class="fg-form" autocomplete="on">
         <input type="hidden" name="next" value="${esc(opts.next || "/founder-portal/")}">
         <label for="pw">Password</label>
         <input id="pw" name="password" type="password" required autofocus autocomplete="current-password">
         ${opts.error ? `<p class="fg-err" role="alert">${esc(opts.error)}</p>` : ""}
         <button class="btn" type="submit">Enter the portal &rarr;</button>
       </form>`;
  const html = `<!doctype html><html lang="en-GB"><head><meta charset="UTF-8">
<title>Founder Portal | Revenue &amp; Beyond</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat+Brush&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<style>
body{min-height:100vh;display:flex;flex-direction:column}
.fg{flex:1;display:flex;align-items:center;justify-content:center;padding:40px 20px}
.fg-card{background:#fff;border:2px solid var(--teal);border-radius:22px;box-shadow:7px 7px 0 var(--green);padding:34px 30px 30px;max-width:460px;width:100%;text-align:center}
.fg-logo{font-weight:900;letter-spacing:-.03em;color:var(--teal);text-decoration:none;font-size:17px}
.fg h1{font-size:clamp(2.2rem,6vw,3rem);margin:18px 0 8px;line-height:1}
.fg h1 .hl{background:var(--green);border-radius:10px;padding:0 .15em}
.fg .lead{font-size:1rem;margin:0 0 20px}
.fg-form{text-align:left;display:grid;gap:10px}
.fg-form label{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--teal)}
.fg-form input[type=password]{font:inherit;font-size:16px;border:2px solid var(--teal);border-radius:12px;padding:11px 14px;width:100%}
.fg-form .btn{width:100%;justify-content:center;margin-top:6px}
.fg-err{color:#C2410C;font-weight:700;font-size:14px;margin:0}
.fg-foot{font-size:13px;color:var(--muted);margin:18px 0 0}
.fg-foot a{color:var(--teal);font-weight:700}
</style></head><body>
<main class="fg"><div class="fg-card">
<a class="fg-logo" href="/">Revenue&amp;Beyond.</a>
<h1>Founder <span class="hl">Portal</span>.</h1>
${body}
<p class="fg-foot">Not a client yet? <a href="/book/">Book a free Diagnosis Call</a>.</p>
</div></main></body></html>`;
  return new Response(html, {
    status,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" },
  });
}

export default async (req: Request, _context: Context) => {
  const secret = Netlify.env.get("PORTAL_PASSWORD") || "";
  const url = new URL(req.url);
  if (secret.length < 8) return page(503, { unconfigured: true });

  const token = await sign(secret, "founder-portal");

  if (req.method === "POST") {
    const form = await req.formData().catch(() => null);
    const pw = String(form?.get("password") || "");
    let next = String(form?.get("next") || "/founder-portal/");
    if (!next.startsWith("/founder-portal")) next = "/founder-portal/";
    const ok = same(await sign(secret, "pw:" + pw), await sign(secret, "pw:" + secret));
    if (!ok) return page(401, { error: "That password isn't right. Try again, or ask me for it.", next });
    return new Response(null, {
      status: 303,
      headers: {
        location: next,
        "set-cookie": `${COOKIE}=${token}; Path=/founder-portal; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
        "cache-control": "no-store",
      },
    });
  }

  if (same(cookieValue(req, COOKIE), token)) {
    const res = await _context.next();
    const out = new Response(res.body, res);
    out.headers.set("cache-control", "private, no-store");
    return out;
  }
  return page(401, { next: url.pathname + url.search + url.hash });
};

export const config: Config = {
  path: ["/founder-portal", "/founder-portal/*"],
  excludedPath: ["/founder-portal/thanks", "/founder-portal/thanks/*"],
};
