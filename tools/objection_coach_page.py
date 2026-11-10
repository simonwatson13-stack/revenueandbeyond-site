# -*- coding: utf-8 -*-
"""Builds the Objection Coach free download page from the newsletter page shell.

  site/objection-coach/index.html   open download, no sign-up, indexed and in the sitemap

The PDF lives at site/assets/downloads/rnb-objection-coach.pdf. To publish a new version,
replace that file (same name) and push. The page and every shared link keep working.
Run from the repo root: python3 tools/objection_coach_page.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PATH = "/objection-coach/"
PDF = "/assets/downloads/rnb-objection-coach.pdf"
FILE = "rnb-objection-coach.pdf"
DOMAIN = "https://revenueandbeyond.com"
URL = DOMAIN + PATH
shell = open(os.path.join(SITE, "newsletter", "index.html"), encoding="utf-8").read()

INSIDE = [
    ("01", "Set it up in five minutes", "Step by step, in Claude or ChatGPT"),
    ("02", "Three answers every time", "Diagnose, reframe, or a clean takeaway"),
    ("03", "The method", "Seven ideas behind every answer"),
    ("04", "The eight objections you'll hear most", "What they usually mean, and the question to ask first"),
    ("05", "The full prompt", "Ready to paste, with your offer, rules and proof"),
    ("06", "Role-play and prep commands", "Practise the call before you have it"),
]

# Formal edition of the site style: same tokens, cards and offset shadows, no handwriting, tilt or highlighter.
CSS = """
<style>
.bd-hero{padding:56px 0 40px}
.bd-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.bd-grid h1{font-size:clamp(2.3rem,5.4vw,3.9rem);line-height:1.02;margin:14px 0 18px}
.bd-grid h1 .dot{color:var(--green)}
.bd-grid .lead{font-size:1.12rem;max-width:30em}
.bd-cover{justify-self:center;max-width:360px;width:100%}
.bd-cover img{display:block;width:100%;height:auto;border:2px solid var(--teal);border-radius:14px;box-shadow:8px 8px 0 var(--teal)}
.bd-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 0;max-width:34em}
.bd-stats div{border-top:3px solid var(--teal);padding-top:10px;font-size:.88rem;line-height:1.35}
.bd-stats b{display:block;font-size:1.7rem;font-weight:900;letter-spacing:-.03em;color:var(--teal);line-height:1.05;margin-bottom:4px}
.bd-card{background:#fff;border:2px solid var(--teal);border-radius:16px;box-shadow:5px 5px 0 var(--teal);padding:26px 26px 22px;margin-top:30px;max-width:34em}
.bd-card h2{font-size:1.35rem;margin:0 0 6px}
.bd-card p{margin:0 0 14px}
.bd-fine{font-size:.82rem;color:var(--muted,rgba(28,28,28,.68));margin:12px 0 0!important}
.bd-fine a{color:inherit;text-decoration:underline}
.bd-share{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.bd-share .btn{font-size:13px;padding:11px 16px;background:#fff}
.bd-inside{padding:30px 0 70px}
.bd-inside h2{text-align:center;margin-bottom:8px}
.bd-inside .sub{text-align:center;max-width:34em;margin:0 auto 30px}
.bd-list{list-style:none;margin:0 auto;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:900px}
.bd-list li{display:flex;gap:16px;align-items:flex-start;background:#fff;border:2px solid var(--teal);border-radius:14px;padding:16px 18px;box-shadow:4px 4px 0 var(--teal)}
.bd-list .n{font-weight:900;font-size:1.05rem;line-height:1.35;color:var(--teal);min-width:1.8em}
.bd-list b{display:block;color:var(--teal)}
.bd-list span{font-size:.92rem;color:var(--muted,rgba(28,28,28,.68))}
.bd-by{display:flex;gap:18px;align-items:center;max-width:720px;margin:44px auto 0;background:#fff;border:2px solid var(--teal);border-radius:16px;padding:20px 22px}
.bd-by img{width:76px;height:76px;border-radius:14px;border:2px solid var(--teal);object-fit:cover}
.bd-by p{margin:0;font-size:.95rem}
.bd-note{max-width:720px;margin:18px auto 0;font-size:.82rem;color:var(--muted,rgba(28,28,28,.68));text-align:center}
.bd-end{text-align:center;margin-top:30px}
@media (max-width:820px){
  .bd-hero{padding:34px 0 20px}
  .bd-grid{grid-template-columns:1fr;gap:34px}
  .bd-cover{max-width:260px;order:-1}
  .bd-list{grid-template-columns:1fr}
  .bd-card{padding:22px 18px 20px}
  .bd-by{flex-direction:column;text-align:center}
}
</style>
"""

ITEMS = "".join(f'<li><span class="n">{n}</span><div><b>{t}</b><span>{d}</span></div></li>' for n, t, d in INSIDE)
ENC = "https%3A%2F%2Frevenueandbeyond.com%2Fobjection-coach%2F"

MAIN = f"""
<section class="bd-hero">
  <div class="col-wide bd-grid">
    <div>
      <p class="eyebrow">Free tool &middot; For B2B founders</p>
      <h1>Objection Coach<span class="dot">.</span></h1>
      <p class="lead">Paste what the prospect said. Get what it really means, the questions that bring out the real objection, and three replies you can send or say today.</p>
      <div class="bd-stats"><div><b>5 min</b>to set up in Claude or ChatGPT</div><div><b>8</b>objections you'll hear most, decoded</div><div><b>3</b>replies every time, as an email and for a call</div></div>
      <div class="bd-card">
        <h2>Free to download</h2>
        <p>No sign-up needed. Six pages: the set-up, the method, and the full prompt to paste into your own AI assistant.</p>
        <a class="btn" href="{PDF}" target="_blank" rel="noopener" download data-bd-dl="open" style="width:100%">Download the Objection Coach (PDF) &darr;</a>
        <p class="bd-fine" style="margin-top:18px!important"><b>Know a founder who keeps hearing "let's push to Q1"?</b> Pass it on.</p>
        <div class="bd-share">
          <button class="btn" type="button" id="bdCopy">Copy link</button>
          <a class="btn" data-bd-share="linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url={ENC}" target="_blank" rel="noopener">Share on LinkedIn</a>
          <a class="btn" data-bd-share="whatsapp" href="https://wa.me/?text=Free%20Objection%20Coach%20for%20founders%3A%20{ENC}" target="_blank" rel="noopener">WhatsApp</a>
          <a class="btn" data-bd-share="email" href="mailto:?subject=Objection%20Coach%2C%20a%20free%20tool%20for%20founders&amp;body=Thought%20you%27d%20find%20this%20useful%3A%20{ENC}">Email it</a>
        </div>
        <p class="bd-fine" id="bdCopied" role="status" hidden>Link copied.</p>
        <p class="bd-fine">Not getting The Founder Read yet? <a href="/newsletter/">It's free, every Sunday evening</a>.</p>
      </div>
    </div>
    <div class="bd-cover"><img src="/assets/img/objection-coach-cover.jpg" alt="Cover of the Objection Coach by Simon Watson" width="640" height="904"></div>
  </div>
</section>
<section class="bd-inside">
  <div class="col-wide">
    <h2>What's inside</h2>
    <p class="sub">Most deals are not lost to a "no". They are lost to a stall nobody questioned. This shows you what is really going on before you reply.</p>
    <ul class="bd-list">{ITEMS}</ul>
    <div class="bd-by">
      <img src="/assets/img/simon-watson-headshot.jpg" alt="Simon Watson" width="76" height="76" loading="lazy">
      <p><b>Built by Simon Watson.</b> Exited founder. Three exits: an IPO, a trade sale and a VC-backed sale. 20+ years selling and scaling B2B businesses across EMEA.</p>
    </div>
    <p class="bd-end small">Want a second pair of eyes on a deal that's stalling? <a class="link" href="/book/">Book a free Diagnosis Call</a>. More free tools on the <a class="link" href="/tools/">tools page</a>.</p>
  </div>
</section>
"""

JS = f"""
<script>
/* Google Analytics events. Consent is handled by /assets/js/analytics.js. */
window.rbTrack=function(name,params){{try{{(window.gtag||function(){{(window.dataLayer=window.dataLayer||[]).push(arguments);}})('event',name,params||{{}});}}catch(e){{}}}};
document.addEventListener('click',function(e){{
  var a=e.target.closest&&e.target.closest('[data-bd-dl],[data-bd-share]'); if(!a) return;
  if(a.hasAttribute('data-bd-dl')) rbTrack('tool_download',{{route:a.getAttribute('data-bd-dl'),file_name:'{FILE}',transport_type:'beacon'}});
  else rbTrack('share',{{method:a.getAttribute('data-bd-share'),content_type:'tool',item_id:'objection-coach',transport_type:'beacon'}});
}});
(function(){{
  var b=document.getElementById('bdCopy'), m=document.getElementById('bdCopied'), url='{URL}';
  if(!b) return;
  b.addEventListener('click',function(){{
    function ok(){{rbTrack('share',{{method:'copy_link',content_type:'tool',item_id:'objection-coach'}});m.hidden=false;b.textContent='Copied';setTimeout(function(){{b.textContent='Copy link';}},2200);}}
    if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(url).then(ok,function(){{prompt('Copy this link',url);}});}}
    else{{prompt('Copy this link',url);}}
  }});
}})();
</script>
"""

def E(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")

TITLE = "Objection Coach, a free tool for B2B founders | Revenue & Beyond"
DESC = ("Free Objection Coach for B2B founders. Paste what the prospect said and get what it really means, "
        "the questions that bring out the real objection, and three replies you can use today. Free PDF, no sign-up.")

s = shell
s = re.sub(r"<title>.*?</title>", f"<title>{E(TITLE)}</title>", s, flags=re.S)
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(DESC)}">', s)
s = re.sub(r'<meta (property|name)="(og|twitter):title" content="[^"]*">', lambda m: f'<meta {m.group(1)}="{m.group(2)}:title" content="{E(TITLE)}">', s)
s = re.sub(r'<meta (property|name)="(og|twitter):description" content="[^"]*">', lambda m: f'<meta {m.group(1)}="{m.group(2)}:description" content="{E(DESC)}">', s)
s = s.replace('content="https://revenueandbeyond.com/newsletter/"', f'content="{URL}"')
s = s.replace('href="https://revenueandbeyond.com/newsletter/"', f'href="{URL}"')
s = s.replace("/assets/img/og-image.png", "/assets/img/objection-coach-og.png")
s = s.replace('content="Revenue &amp; Beyond. Build, scale and sell your B2B business."', 'content="Objection Coach, a free tool by Simon Watson."')
s = s.replace('{"@type":"ListItem","position":2,"name":"Newsletter","item":"https://revenueandbeyond.com/newsletter/"}',
              '{"@type":"ListItem","position":2,"name":"Objection Coach","item":"%s"}' % URL)
s = s.replace('class="pg-newsletter"', 'class="pg-objection-coach"')
s = s.replace('<a href="/newsletter/" class="active" aria-current="page">Newsletter</a>', '<a href="/newsletter/">Newsletter</a>')
s = s.replace("../assets/", "/assets/")
s = s.replace("</head>", CSS + "</head>")
s = re.sub(r'<main id="main">.*?</main>', lambda m: f'<main id="main">{MAIN}</main>', s, flags=re.S)
s = s.replace("</body>", JS + "</body>")
out = os.path.join(SITE, PATH.strip("/"), "index.html")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(s)
print("wrote", out)
