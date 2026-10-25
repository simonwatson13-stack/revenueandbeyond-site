# -*- coding: utf-8 -*-
"""Builds the two founder-led sales blueprint pages from the newsletter page shell.

  site/blueprint/index.html           gated: email in, guide out (posts to /api/blueprint)
  site/blueprint/download/index.html  open: for Founder Read readers, free to share (noindex)

The PDF lives at site/assets/downloads/founder-led-sales-blueprint.pdf. To publish a new
version of the guide, replace that file (same name) and push. Every link keeps working.
Run from the repo root: python3 tools/blueprint_pages.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PDF = "/assets/downloads/founder-led-sales-blueprint.pdf"
DOMAIN = "https://revenueandbeyond.com"
shell = open(os.path.join(SITE, "newsletter", "index.html"), encoding="utf-8").read()

INSIDE = [
    ("00", "Before you start", "You are the reason it is growing, and the reason it is stuck"),
    ("01", "Select", "Who you choose matters more than how many"),
    ("02", "Pipeline", "Stages that mean something"),
    ("03", "Outreach", "Outreach that actually gets a reply"),
    ("04", "The conversation", "Diagnose before you prescribe"),
    ("05", "The first sales hire", "Build the system before you hire the seller"),
    ("06", "The numbers", "Five numbers, every week"),
    ("07", "The scorecard", "How much does your sales depend on you?"),
]

CSS = """
<style>
.bp-hero{padding:56px 0 40px}
.bp-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.bp-grid h1{font-size:clamp(2.3rem,5.4vw,3.9rem);line-height:1.02;margin:14px 0 18px}
.bp-grid .lead{font-size:1.12rem;max-width:30em}
.bp-cover{position:relative;justify-self:center;max-width:380px;width:100%}
.bp-cover img{display:block;width:100%;height:auto;border:2px solid var(--teal);border-radius:14px;box-shadow:10px 10px 0 var(--green);transform:rotate(1.6deg)}
.bp-cover .tg{position:absolute;left:-18px;bottom:34px;transform:rotate(-4deg)}
.bp-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 0;max-width:34em}
.bp-stats div{border-top:3px solid var(--green);padding-top:10px;font-size:.88rem;line-height:1.35}
.bp-stats div:nth-child(2){border-color:var(--purple)}
.bp-stats div:nth-child(3){border-color:var(--sky)}
.bp-stats b{display:block;font-family:var(--hand);font-size:1.9rem;font-weight:400;color:var(--teal);line-height:1}
.bp-card{background:#fff;border:2px solid var(--teal);border-radius:18px;box-shadow:7px 7px 0 var(--green);padding:28px 28px 24px;margin-top:30px;max-width:34em}
.bp-card h2{font-size:1.35rem;margin:0 0 6px}
.bp-card p{margin:0 0 14px}
.bp-form{display:grid;grid-template-columns:1fr 1.4fr;gap:10px}
.bp-form label{display:block;font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--teal);margin-bottom:5px}
.bp-form input{width:100%;font:inherit;font-size:1rem;padding:13px 14px;border:2px solid var(--teal);border-radius:12px;background:#fff;color:var(--black,#1C1C1C)}
.bp-form input:focus{outline:3px solid var(--green);outline-offset:1px}
.bp-form .btn{grid-column:1/-1;width:100%;margin-top:6px;font-size:15px;padding:16px 20px}
.bp-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
.bp-fine{font-size:.82rem;color:var(--muted,rgba(28,28,28,.68));margin:12px 0 0!important}
.bp-fine a{color:inherit;text-decoration:underline}
.bp-err{color:#B3261E;font-weight:600;font-size:.9rem;margin:10px 0 0!important}
.bp-done h2 .hl{font-size:inherit}
.bp-done .btn{margin-top:4px}
.bp-share{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.bp-share .btn{font-size:13px;padding:11px 16px;background:#fff}
.bp-inside{padding:30px 0 70px}
.bp-inside h2{text-align:center;margin-bottom:8px}
.bp-inside .sub{text-align:center;max-width:34em;margin:0 auto 30px}
.bp-list{list-style:none;margin:0 auto;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:900px}
.bp-list li{display:flex;gap:16px;align-items:flex-start;background:#fff;border:2px solid var(--teal);border-radius:14px;padding:16px 18px;box-shadow:4px 4px 0 var(--green)}
.bp-list li:nth-child(4n+2),.bp-list li:nth-child(4n+3){box-shadow:4px 4px 0 var(--purple)}
.bp-list .n{font-family:var(--hand);font-size:1.7rem;line-height:1;color:var(--teal);min-width:1.6em}
.bp-list b{display:block;color:var(--teal)}
.bp-list span{font-size:.92rem;color:var(--muted,rgba(28,28,28,.68))}
.bp-by{display:flex;gap:18px;align-items:center;max-width:720px;margin:44px auto 0;background:var(--tint-green);border:2px solid var(--teal);border-radius:16px;padding:20px 22px}
.bp-by img{width:76px;height:76px;border-radius:14px;border:2px solid var(--teal);object-fit:cover}
.bp-by p{margin:0;font-size:.95rem}
.bp-end{text-align:center;margin-top:40px}
@media (max-width:820px){
  .bp-hero{padding:34px 0 20px}
  .bp-grid{grid-template-columns:1fr;gap:34px}
  .bp-cover{max-width:280px;order:-1}
  .bp-form{grid-template-columns:1fr}
  .bp-list{grid-template-columns:1fr}
  .bp-card{padding:22px 18px 20px}
  .bp-by{flex-direction:column;text-align:center}
}
</style>
"""

def inside_section(intro):
    items = "".join(f'<li><span class="n">{n}</span><div><b>{t}</b><span>{d}</span></div></li>' for n, t, d in INSIDE)
    return f"""
<section class="bp-inside">
  <div class="col-wide">
    <h2>What's <span class="hl">inside</span></h2>
    <p class="sub">{intro}</p>
    <ul class="bp-list">{items}</ul>
    <div class="bp-by">
      <img src="/assets/img/simon-watson-headshot.jpg" alt="Simon Watson" width="76" height="76" loading="lazy">
      <p><b>Written by Simon Watson.</b> Exited founder. Three exits: an IPO, a trade sale and a VC-backed sale. 20+ years selling and scaling B2B businesses across EMEA.</p>
    </div>
    <p class="bp-end small">Want a second pair of eyes on your own sales? <a class="link" href="/book/">Book a free Diagnosis Call</a>.</p>
  </div>
</section>"""

COVER = """<div class="bp-cover"><img src="/assets/img/blueprint-cover.jpg" alt="Cover of The founder-led sales blueprint by Simon Watson" width="640" height="905"><span class="tg hand">Free guide</span></div>"""
STATS = """<div class="bp-stats"><div><b>07</b>parts, each with actions to take this month</div><div><b>20</b>minutes to read end to end</div><div><b>01</b>scorecard to show where sales still depends on you</div></div>"""
H1 = 'The founder-led sales <span class="hl">blueprint.</span>'
LEAD = "How to get sales out of your head and into a system that grows, holds and sells without you."

GATED_MAIN = f"""
<section class="bp-hero">
  <div class="col-wide bp-grid">
    <div>
      <p class="eyebrow">Free guide &middot; For B2B founders</p>
      <h1>{H1}</h1>
      <p class="lead">{LEAD}</p>
      {STATS}
      <div class="bp-card" id="bpCard">
        <div id="bpAsk">
          <h2>Get your free copy</h2>
          <p>Tell me where to send it and the guide is yours straight away.</p>
          <form class="bp-form" id="bpForm" novalidate>
            <div><label for="bpName">First name</label><input id="bpName" name="first_name" type="text" autocomplete="given-name" maxlength="80"></div>
            <div><label for="bpEmail">Work email</label><input id="bpEmail" name="email" type="email" autocomplete="email" required maxlength="254" placeholder="you@company.com"></div>
            <div class="bp-hp" aria-hidden="true"><label for="bpWeb">Website</label><input id="bpWeb" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <button class="btn" type="submit" id="bpBtn">Send me the blueprint &rarr;</button>
          </form>
          <p class="bp-err" id="bpErr" role="alert" hidden></p>
          <p class="bp-fine">You'll also get The Founder Read, my free email for founders, every Sunday evening. Unsubscribe any time. <a href="/privacy-policy.html">Privacy policy</a>.</p>
        </div>
        <div class="bp-done" id="bpDone" hidden tabindex="-1">
          <h2>It's <span class="hl">yours</span>.</h2>
          <p>Read it once end to end, then do the scorecard in part 07 and start with your lowest score.</p>
          <a class="btn" href="{PDF}" target="_blank" rel="noopener" download data-bp-dl="gated">Download the blueprint (PDF) &darr;</a>
          <p class="bp-fine">The Founder Read lands on Sunday evening. If it isn't there, check your promotions tab.</p>
        </div>
      </div>
    </div>
    {COVER}
  </div>
</section>
{inside_section("Seven parts and a scorecard. Every part ends with the actions to take this month.")}
"""

OPEN_MAIN = f"""
<section class="bp-hero">
  <div class="col-wide bp-grid">
    <div>
      <p class="eyebrow">Free guide &middot; For B2B founders</p>
      <h1>{H1}</h1>
      <p class="lead">{LEAD}</p>
      {STATS}
      <div class="bp-card">
        <h2>Your copy is <span class="hl">ready</span></h2>
        <p>No sign-up needed. Read it once end to end, then do the scorecard in part 07.</p>
        <a class="btn" href="{PDF}" target="_blank" rel="noopener" download data-bp-dl="open" style="width:100%">Download the blueprint (PDF) &darr;</a>
        <p class="bp-fine" style="margin-top:18px!important"><b>Know a founder who'd find it useful?</b> Pass it on.</p>
        <div class="bp-share">
          <button class="btn" type="button" id="bpCopy">Copy link</button>
          <a class="btn" id="bpLi" data-bp-share="linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Frevenueandbeyond.com%2Fblueprint%2Fdownload%2F" target="_blank" rel="noopener">Share on LinkedIn</a>
          <a class="btn" data-bp-share="email" href="mailto:?subject=The%20founder-led%20sales%20blueprint&amp;body=Thought%20you'd%20find%20this%20useful%3A%20https%3A%2F%2Frevenueandbeyond.com%2Fblueprint%2Fdownload%2F">Email it</a>
        </div>
        <p class="bp-fine" id="bpCopied" role="status" hidden>Link copied.</p>
        <p class="bp-fine">Not getting The Founder Read yet? <a href="/newsletter/">It's free, every Sunday evening</a>.</p>
      </div>
    </div>
    {COVER}
  </div>
</section>
{inside_section("Seven parts and a scorecard. Every part ends with the actions to take this month.")}
"""

TRACK_JS = """
<script>
/* Google Analytics events for the blueprint pages. Consent is handled by /assets/js/analytics.js:
   events queue in the dataLayer and are sent under whatever consent the visitor chose. */
window.rbTrack=function(name,params){try{(window.gtag||function(){(window.dataLayer=window.dataLayer||[]).push(arguments);})('event',name,params||{});}catch(e){}};
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('[data-bp-dl],[data-bp-share]'); if(!a) return;
  if(a.hasAttribute('data-bp-dl')) rbTrack('blueprint_download',{route:a.getAttribute('data-bp-dl'),file_name:'founder-led-sales-blueprint.pdf',transport_type:'beacon'});
  else rbTrack('share',{method:a.getAttribute('data-bp-share'),content_type:'guide',item_id:'founder-led-sales-blueprint',transport_type:'beacon'});
});
</script>
"""

GATED_JS = TRACK_JS + """
<script>
(function(){
  var KEY='rb_blueprint', ask=document.getElementById('bpAsk'), done=document.getElementById('bpDone'),
      form=document.getElementById('bpForm'), btn=document.getElementById('bpBtn'), err=document.getElementById('bpErr'),
      RE=/^[^\\s@<>()[\\]\\\\,;:"]+@[^\\s@<>()[\\]\\\\,;:"]+\\.[a-z]{2,}$/i;
  function show(focus){ask.hidden=true;done.hidden=false;if(focus)done.focus();}
  try{if(localStorage.getItem(KEY))show(false);}catch(e){}
  form.addEventListener('submit',function(e){
    e.preventDefault(); err.hidden=true;
    var email=document.getElementById('bpEmail').value.trim();
    if(!RE.test(email)){err.textContent='Please enter a valid email address.';err.hidden=false;document.getElementById('bpEmail').focus();return;}
    btn.disabled=true; btn.textContent='Sending...';
    fetch('/api/blueprint',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({email:email,first_name:document.getElementById('bpName').value.trim(),website:document.getElementById('bpWeb').value,ref:document.referrer})})
      .then(function(r){return r.json().then(function(j){return {ok:r.ok,status:r.status,j:j};});})
      .then(function(res){
        if(res.ok){try{localStorage.setItem(KEY,String(Date.now()));}catch(x){} rbTrack('generate_lead',{form_name:'blueprint',route:'gated'}); show(true); return;}
        if(res.status===400){btn.disabled=false;btn.textContent='Send me the blueprint \\u2192';err.textContent=(res.j&&res.j.error)||'Please check your email address.';err.hidden=false;return;}
        throw new Error(res.status);
      })
      .catch(function(){ rbTrack('blueprint_signup_error',{form_name:'blueprint'}); show(true); }); // never block a real person because of a server hiccup
  });
})();
</script>
"""

OPEN_JS = TRACK_JS + """
<script>
(function(){
  var b=document.getElementById('bpCopy'), m=document.getElementById('bpCopied'), url='https://revenueandbeyond.com/blueprint/download/';
  if(!b) return;
  b.addEventListener('click',function(){
    function ok(){rbTrack('share',{method:'copy_link',content_type:'guide',item_id:'founder-led-sales-blueprint'});m.hidden=false;b.textContent='Copied';setTimeout(function(){b.textContent='Copy link';},2200);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(ok,function(){prompt('Copy this link',url);});}
    else{prompt('Copy this link',url);}
  });
})();
</script>
"""

def E(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")

def build(path, title, desc, main, js, indexable):
    s = shell
    url = DOMAIN + path
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', s)
    s = re.sub(r'<meta (property|name)="(og|twitter):title" content="[^"]*">', lambda m: f'<meta {m.group(1)}="{m.group(2)}:title" content="{E(title)}">', s)
    s = re.sub(r'<meta (property|name)="(og|twitter):description" content="[^"]*">', lambda m: f'<meta {m.group(1)}="{m.group(2)}:description" content="{E(desc)}">', s)
    s = s.replace('content="https://revenueandbeyond.com/newsletter/"', f'content="{url}"')
    s = s.replace("/assets/img/og-image.png", "/assets/img/blueprint-og.png")
    s = s.replace('content="Revenue &amp; Beyond. Build, scale and sell your B2B business."', 'content="The founder-led sales blueprint, a free guide by Simon Watson."')
    if indexable:
        s = s.replace('href="https://revenueandbeyond.com/newsletter/"', f'href="{url}"')
    else:
        s = re.sub(r'<link rel="canonical" href="[^"]*">\n', "", s)
        s = s.replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"')
    # breadcrumb in the structured data
    s = s.replace('{"@type":"ListItem","position":2,"name":"Newsletter","item":"https://revenueandbeyond.com/newsletter/"}',
                  '{"@type":"ListItem","position":2,"name":"The founder-led sales blueprint","item":"%s"}' % url)
    s = s.replace('class="pg-newsletter"', 'class="pg-blueprint"')
    s = s.replace('<a href="/newsletter/" class="active" aria-current="page">Newsletter</a>', '<a href="/newsletter/">Newsletter</a>')
    s = s.replace("../assets/", "/assets/")
    s = s.replace("</head>", CSS + "</head>")
    s = re.sub(r'<main id="main">.*?</main>', lambda m: f'<main id="main">{main}</main>', s, flags=re.S)
    s = s.replace("</body>", js + "</body>")
    out = os.path.join(SITE, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(s)
    print("wrote", out)

build("/blueprint/", "The founder-led sales blueprint: free guide for B2B founders | Revenue & Beyond",
      "A free guide for B2B founders: how to get sales out of your head and into a system that grows, holds and sells without you. Seven parts and a scorecard.",
      GATED_MAIN, GATED_JS, True)
build("/blueprint/download/", "Download: The founder-led sales blueprint | Revenue & Beyond",
      "Free to download and share: how to get sales out of your head and into a system that grows, holds and sells without you.",
      OPEN_MAIN, OPEN_JS, False)
