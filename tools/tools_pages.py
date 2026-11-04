# -*- coding: utf-8 -*-
"""Builds the tools shop from data/products.json, using the newsletter page as the shell.

  site/tools/index.html          the catalogue: free tools, kits (Stripe), done-with-you installs
  site/tools/thanks/index.html   where Stripe Payment Links send buyers (noindex); checks the
                                 order with /api/tools/order and offers the download

To change a product, edit data/products.json, run python3 tools/tools_pages.py, push.
A kit switches from "Join the waitlist" to "Buy now" as soon as its stripeLink is filled in.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DOMAIN = "https://revenueandbeyond.com"
# Soft launch: page is live but unlinked and noindex. Set to False at launch, then add the
# sitemap entry and the nav/footer links.
HIDDEN = True
DATA = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))
P = DATA["products"]
shell = open(os.path.join(SITE, "newsletter", "index.html"), encoding="utf-8").read()
h = lambda s: html.escape(s or "", quote=True)

GROUPS = [
    ("free", "Free", "Free tools", "Take them, use them, pass them on.", "c-green"),
    ("kit", "Kits", "Kits you set up yourself", "A Claude skill, the files it needs and a one-page set-up guide. Buy, download, running in about ten minutes.", "c-purple"),
    ("install", "Done with you", "Done with you", "The bigger systems. I build them into your business with you, on your tools, with your rules.", "c-sky"),
    ("event", "Workshop", "Workshop", "See it all running before you build anything.", "c-green"),
]

CSS = """
<style>
.pg-tools .hero{background:linear-gradient(180deg,var(--tint-green) 0%,rgba(245,244,240,0) 100%)}
.pg-tools .hero h1{max-width:16em;margin-left:auto;margin-right:auto}
.tl-chips{justify-content:center;margin:26px 0 0}
.tl-group{padding:46px 0 10px}
.tl-group[hidden]{display:none}
.tl-head{max-width:1180px;margin:0 auto 22px;padding:0 24px}
.tl-head h2{font-size:clamp(1.5rem,2.6vw,2rem);margin:0 0 6px}
.tl-head p{margin:0;color:var(--muted);max-width:40em}
.pg-tools .ocards-wrap{max-width:1180px}
.pg-tools .ocards{grid-template-columns:repeat(3,1fr)}
.ocard .tl-soon{position:absolute;top:18px;right:16px;font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;background:var(--tint-purple);color:var(--teal);border-radius:999px;padding:4px 10px}
.ocard.is-soon .og{padding-right:100px}
.ocard .btn-solid{background:var(--green);color:var(--teal);border-color:var(--teal)}
.tl-how{padding:70px 0 20px}
.tl-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1132px;margin:26px auto 0;padding:0 24px;list-style:none}
.tl-steps li{background:#fff;border:2px solid var(--teal);border-radius:16px;padding:20px;box-shadow:4px 4px 0 var(--green)}
.tl-steps li:nth-child(2){box-shadow:4px 4px 0 var(--purple)}
.tl-steps li:nth-child(3){box-shadow:4px 4px 0 var(--sky)}
.tl-steps .n{font-family:var(--hand);font-size:1.9rem;line-height:1;color:var(--teal)}
.tl-steps b{display:block;color:var(--teal);margin:6px 0 4px}
.tl-steps span{font-size:.93rem;color:var(--muted)}
.tl-faq{padding:60px 0 100px}
.tl-faq .faqs{max-width:760px;margin:22px auto 0}
.tl-dlg{border:2px solid var(--teal);border-radius:18px;box-shadow:7px 7px 0 var(--green);padding:28px 26px 24px;max-width:440px;width:calc(100% - 32px);background:#fff;color:var(--black)}
.tl-dlg::backdrop{background:rgba(11,54,59,.45)}
.tl-dlg h2{font-size:1.3rem;margin:0 0 6px;padding-right:28px}
.tl-dlg p{margin:0 0 14px}
.tl-dlg label{display:block;font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--teal);margin:10px 0 5px}
.tl-dlg input{width:100%;font:inherit;font-size:1rem;padding:13px 14px;border:2px solid var(--teal);border-radius:12px;background:#fff}
.tl-dlg input:focus{outline:3px solid var(--green);outline-offset:1px}
.tl-dlg .btn{width:100%;margin-top:16px}
.tl-x{position:absolute;top:12px;right:14px;background:none;border:0;font-size:26px;line-height:1;color:var(--teal);cursor:pointer;padding:4px}
.tl-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
.tl-fine{font-size:.82rem;color:var(--muted);margin:12px 0 0!important}
.tl-fine a{color:inherit}
.tl-err{color:#B3261E;font-weight:600;font-size:.9rem;margin:10px 0 0!important}
.tl-card{background:#fff;border:2px solid var(--teal);border-radius:18px;box-shadow:7px 7px 0 var(--green);padding:30px 28px;max-width:620px;margin:0 auto}
.tl-card h2{font-size:1.5rem;margin:0 0 8px}
.tl-card ol{margin:14px 0 0;padding-left:20px}
.tl-card li{margin:0 0 8px}
@media (max-width:1000px){.pg-tools .ocards{grid-template-columns:repeat(2,1fr)}.tl-steps{grid-template-columns:1fr}}
@media (max-width:560px){.pg-tools .ocards{grid-template-columns:1fr}.tl-card{padding:24px 18px}}
</style>
"""

def button(p):
    k, live = p["kind"], p["status"] == "live"
    if k == "free" and p.get("href"):
        return f'<a class="btn btn-ghost btn-sm" href="{h(p["href"])}" data-tl-go="{h(p["id"])}">Get it free</a>'
    if k == "free" and live and p.get("file"):
        return f'<button class="btn btn-ghost btn-sm" type="button" data-tl-form="{h(p["id"])}" data-mode="download">Get it free</button>'
    if k == "kit" and p.get("stripeLink"):
        return f'<a class="btn btn-sm btn-solid" href="{h(p["stripeLink"])}" data-tl-buy="{h(p["id"])}" rel="noopener">Buy now &rarr;</a>'
    if k == "install":
        return f'<a class="btn btn-ghost btn-sm" href="/book/?ref=tools-{h(p.get("bookRef", p["id"]))}" data-tl-go="{h(p["id"])}">Book a scoping call</a>'
    return f'<button class="btn btn-ghost btn-sm" type="button" data-tl-form="{h(p["id"])}" data-mode="waitlist">Join the waitlist</button>'

def card(p, colour):
    soon = p["status"] != "live" and not (p["kind"] == "kit" and p.get("stripeLink"))
    tag = '<span class="tl-soon">Coming soon</span>' if soon and p["kind"] != "event" else ""
    pts = "".join(f"<li>{h(x)}</li>" for x in p.get("points", []))
    note = f'<small>{h(p["priceNote"])}</small>' if p.get("priceNote") else ""
    return f"""<article class="ocard {colour}{' is-soon' if tag else ''}" id="{h(p['id'])}">{tag}
  <p class="og">{h(p['format'])}</p>
  <h2>{h(p['name'])}</h2>
  <p class="op">{h(p['price'])}{note}</p>
  <p class="os">{h(p['summary'])}</p>
  <p class="ob"><b>Best for:</b> {h(p['for'])}</p>
  <ul class="oh">{pts}</ul>
  {button(p)}
</article>"""

groups_html = ""
for key, chip, title, intro, colour in GROUPS:
    items = [p for p in P if p["kind"] == key]
    if not items:
        continue
    cards = "\n".join(card(p, colour) for p in items)
    groups_html += f"""
<section class="tl-group" data-group="{key}">
  <div class="tl-head"><h2>{h(title)}</h2><p>{h(intro)}</p></div>
  <div class="ocards-wrap"><div class="ocards">
{cards}
  </div></div>
</section>"""

chips = '<button class="chip on" type="button" data-f="all">All</button>' + "".join(
    f'<button class="chip" type="button" data-f="{k}">{h(c)}</button>' for k, c, *_ in GROUPS if any(p["kind"] == k for p in P))

FAQ = [
    ("What is a Claude skill?", "A folder of instructions and files that teaches Claude how to do one job your way, every time. You add it to Claude once and it is there whenever you ask for that job."),
    ("What do I need to use a kit?", "A paid Claude plan (Pro or above) and ten minutes. Each kit comes with a one-page set-up guide. Some kits work better with your call recorder or email connected to Claude, and the guide says which."),
    ("Can I share a kit with my team?", "Use it across your own business as much as you like. Please don't resell it or share it outside your company."),
    ("What if it doesn't work for me?", "Email me at simon@revenueandbeyond.com. I'll help you get it running, and if I can't, I'll refund you."),
    ("What does done with you mean?", "I build the system into your business on your own tools, test it with you and hand it over working. It starts with a free scoping call so we both know the fixed fee before anything starts."),
]
faq_html = "".join(f'<div class="q"><h3>{h(q)}</h3><p>{h(a)}</p></div>' for q, a in FAQ)

MAIN = f"""
<section class="hero" style="padding-bottom:30px">
  <div class="col">
    <p class="eyebrow" style="justify-content:center">Tools</p>
    <h1>The tools I built to run <span class="hl">my own business</span>.</h1>
    <p class="lead" style="margin-top:22px">I run Revenue &amp; Beyond on a set of AI tools I built with Claude: a brief on my phone every morning, a deal board that updates itself, proposals straight from a call and a newsletter that goes out on four channels. Some are free. Some are kits you set up yourself. The bigger ones I build with you.</p>
    <div class="chips tl-chips" role="group" aria-label="Filter tools">{chips}</div>
  </div>
</section>
{groups_html}
<section class="tl-how">
  <div class="col-wide" style="text-align:center"><h2>How the <span class="hl">kits</span> work</h2></div>
  <ol class="tl-steps">
    <li><span class="n">01</span><b>Buy</b><span>Secure checkout with Stripe. You get a VAT receipt by email.</span></li>
    <li><span class="n">02</span><b>Download</b><span>Straight after payment, from your order page. Bookmark it to download again.</span></li>
    <li><span class="n">03</span><b>Set up</b><span>Add the skill to Claude and follow the one-page guide. About ten minutes.</span></li>
  </ol>
</section>
<section class="tl-faq">
  <div class="col-wide" style="text-align:center"><h2>Questions</h2></div>
  <div class="faqs">{faq_html}</div>
  <p class="small center" style="margin-top:34px">Want to talk about your own set-up? <a class="link" href="/book/?ref=tools">Book a free call</a>.</p>
</section>
<dialog class="tl-dlg" id="tlDlg" aria-labelledby="tlDlgH">
  <button class="tl-x" type="button" id="tlX" aria-label="Close">&times;</button>
  <div id="tlAsk">
    <h2 id="tlDlgH">Join the waitlist</h2>
    <p id="tlDlgP">I'll email you the day it's ready.</p>
    <form id="tlForm" novalidate>
      <label for="tlName">First name</label><input id="tlName" type="text" autocomplete="given-name" maxlength="80">
      <label for="tlEmail">Work email</label><input id="tlEmail" type="email" autocomplete="email" required maxlength="254" placeholder="you@company.com">
      <div class="tl-hp" aria-hidden="true"><label for="tlWeb">Website</label><input id="tlWeb" type="text" tabindex="-1" autocomplete="off"></div>
      <button class="btn" type="submit" id="tlBtn">Keep me posted &rarr;</button>
    </form>
    <p class="tl-err" id="tlErr" role="alert" hidden></p>
    <p class="tl-fine">You'll also get The Founder Read, my free email for founders, every Sunday evening. Unsubscribe any time. <a href="/privacy-policy.html">Privacy policy</a>.</p>
  </div>
  <div id="tlDone" hidden tabindex="-1">
    <h2>You're <span class="hl">on the list</span>.</h2>
    <p id="tlDoneP">I'll email you the day it's ready.</p>
    <a class="btn" id="tlDl" href="#" hidden download>Download &darr;</a>
  </div>
</dialog>
"""

PRODUCT_NAMES = {p["id"]: p["name"] for p in P}
JS = """
<script>
window.rbTrack=function(n,p){try{(window.gtag||function(){(window.dataLayer=window.dataLayer||[]).push(arguments);})('event',n,p||{});}catch(e){}};
(function(){
  var NAMES=%s, chips=document.querySelectorAll('.tl-chips .chip'), groups=document.querySelectorAll('.tl-group');
  chips.forEach(function(c){c.addEventListener('click',function(){
    var f=c.getAttribute('data-f'); chips.forEach(function(x){x.classList.toggle('on',x===c);});
    groups.forEach(function(g){g.hidden=!(f==='all'||g.getAttribute('data-group')===f);});
  });});
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('[data-tl-buy],[data-tl-go]'); if(!b) return;
    if(b.hasAttribute('data-tl-buy')) rbTrack('begin_checkout',{item_id:b.getAttribute('data-tl-buy'),transport_type:'beacon'});
    else rbTrack('select_item',{item_id:b.getAttribute('data-tl-go'),transport_type:'beacon'});
  });
  var dlg=document.getElementById('tlDlg'), form=document.getElementById('tlForm'), ask=document.getElementById('tlAsk'), done=document.getElementById('tlDone'),
      err=document.getElementById('tlErr'), btn=document.getElementById('tlBtn'), dl=document.getElementById('tlDl'), cur=null, mode='waitlist',
      RE=/^[^\\s@<>()[\\]\\\\,;:"]+@[^\\s@<>()[\\]\\\\,;:"]+\\.[a-z]{2,}$/i;
  function label(){return mode==='download'?'Send it to me \\u2192':'Keep me posted \\u2192';}
  document.querySelectorAll('[data-tl-form]').forEach(function(b){b.addEventListener('click',function(){
    cur=b.getAttribute('data-tl-form'); mode=b.getAttribute('data-mode')||'waitlist';
    document.getElementById('tlDlgH').textContent=(mode==='download'?'Get ':'Waitlist: ')+(NAMES[cur]||'');
    document.getElementById('tlDlgP').textContent=mode==='download'?'Tell me where to send it and it is yours straight away.':"I'll email you the day it's ready.";
    ask.hidden=false; done.hidden=true; err.hidden=true; btn.disabled=false; btn.textContent=label(); dl.hidden=true;
    if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');
    document.getElementById('tlEmail').focus();
  });});
  document.getElementById('tlX').addEventListener('click',function(){dlg.close?dlg.close():dlg.removeAttribute('open');});
  dlg.addEventListener('click',function(e){if(e.target===dlg) dlg.close();});
  form.addEventListener('submit',function(e){
    e.preventDefault(); err.hidden=true;
    var email=document.getElementById('tlEmail').value.trim();
    if(!RE.test(email)){err.textContent='Please enter a valid email address.';err.hidden=false;return;}
    btn.disabled=true; btn.textContent='Sending...';
    fetch('/api/tools/lead',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({product:cur,email:email,first_name:document.getElementById('tlName').value.trim(),website:document.getElementById('tlWeb').value})})
      .then(function(r){return r.json().then(function(j){return {ok:r.ok,status:r.status,j:j};});})
      .then(function(res){
        if(!res.ok){btn.disabled=false;btn.textContent=label();err.textContent=(res.j&&res.j.error)||'Something went wrong. Please try again.';err.hidden=false;return;}
        rbTrack('generate_lead',{form_name:'tools',item_id:cur,route:res.j.type});
        ask.hidden=true; done.hidden=false; done.focus();
        if(res.j.url){document.getElementById('tlDoneP').textContent='Here it is. The Founder Read lands on Sunday evening.';dl.href=res.j.url;dl.hidden=false;}
      })
      .catch(function(){btn.disabled=false;btn.textContent=label();err.textContent='Something went wrong. Please try again.';err.hidden=false;});
  });
})();
</script>
""" % json.dumps(PRODUCT_NAMES)

THANKS_MAIN = """
<section class="hero" style="padding-bottom:30px">
  <div class="col">
    <p class="eyebrow" style="justify-content:center">Your order</p>
    <h1>Thank <span class="hl">you</span>.</h1>
  </div>
</section>
<section style="padding:10px 0 110px">
  <div class="col-wide">
    <div class="tl-card" id="tkCard" aria-live="polite">
      <div id="tkWait"><h2>Checking your order...</h2><p>This takes a second.</p></div>
      <div id="tkOk" hidden>
        <h2 id="tkName">Your kit</h2>
        <p>Payment received. Your receipt is on its way from Stripe<span id="tkEmail"></span>.</p>
        <a class="btn" id="tkDl" href="#">Download your kit &darr;</a>
        <ol>
          <li>Unzip the download and open the set-up guide first.</li>
          <li>Add the skill to Claude, following the steps in the guide.</li>
          <li>Ask Claude for the job the guide describes. That's it.</li>
        </ol>
        <p class="tl-fine">Bookmark this page to download again later (up to 10 times). Stuck? Email <a href="mailto:simon@revenueandbeyond.com">simon@revenueandbeyond.com</a>.</p>
      </div>
      <div id="tkErr" hidden>
        <h2>Something's not right</h2>
        <p id="tkErrP">I couldn't confirm this order.</p>
        <p class="tl-fine">If you've paid, email <a href="mailto:simon@revenueandbeyond.com">simon@revenueandbeyond.com</a> with your receipt and I'll send the kit straight over.</p>
      </div>
    </div>
    <p class="small center" style="margin-top:28px"><a class="link" href="/tools/">Back to all tools</a></p>
  </div>
</section>
"""

THANKS_JS = """
<script>
window.rbTrack=function(n,p){try{(window.gtag||function(){(window.dataLayer=window.dataLayer||[]).push(arguments);})('event',n,p||{});}catch(e){}};
(function(){
  var id=new URLSearchParams(location.search).get('session_id'), $=function(x){return document.getElementById(x);};
  function fail(m){$('tkWait').hidden=true;$('tkErr').hidden=false;if(m)$('tkErrP').textContent=m;}
  if(!id){fail('There is no order reference on this link.');return;}
  fetch('/api/tools/order?session_id='+encodeURIComponent(id)).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});})
    .then(function(res){
      if(!res.ok){fail(res.j&&res.j.error);return;}
      $('tkWait').hidden=true;$('tkOk').hidden=false;$('tkName').textContent=res.j.product.name;
      if(res.j.email)$('tkEmail').textContent=' to '+res.j.email;
      $('tkDl').href=res.j.download;
      $('tkDl').addEventListener('click',function(){rbTrack('kit_download',{item_id:res.j.product.id,transport_type:'beacon'});});
      try{if(!sessionStorage.getItem('rb_p_'+id)){sessionStorage.setItem('rb_p_'+id,'1');rbTrack('purchase',{transaction_id:id,items:[{item_id:res.j.product.id,item_name:res.j.product.name}]});}}catch(e){}
    }).catch(function(){fail('Your order could not be checked just now. Refresh the page in a minute.');});
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
    if indexable:
        s = s.replace('href="https://revenueandbeyond.com/newsletter/"', f'href="{url}"')
    else:
        s = re.sub(r'<link rel="canonical" href="[^"]*">\n', "", s)
        s = s.replace('content="index, follow, max-image-preview:large"', 'content="noindex, nofollow"')
    s = s.replace('{"@type":"ListItem","position":2,"name":"Newsletter","item":"https://revenueandbeyond.com/newsletter/"}',
                  '{"@type":"ListItem","position":2,"name":"Tools","item":"%s"}' % (DOMAIN + "/tools/"))
    s = s.replace('class="pg-newsletter"', 'class="pg-tools"')
    s = s.replace('<a href="/newsletter/" class="active" aria-current="page">Newsletter</a>', '<a href="/newsletter/">Newsletter</a>')
    s = s.replace("../assets/", "/assets/")
    s = s.replace("</head>", CSS + ("" if indexable else "<script>try{localStorage.setItem('rb_nl_pop',String(Date.now()))}catch(e){}</script>") + "</head>")
    s = re.sub(r'<main id="main">.*?</main>', lambda m: f'<main id="main">{main}</main>', s, flags=re.S)
    s = s.replace("</body>", js + "</body>")
    out = os.path.join(SITE, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(s)
    print("wrote", out)

build("/tools/", "Tools and kits for founder-led businesses | Revenue & Beyond",
      "The AI tools I built with Claude to run my own business: free tools, kits you set up yourself, and done-with-you systems for founder-led B2B businesses.",
      MAIN, JS, not HIDDEN)
build("/tools/thanks/", "Your order | Revenue & Beyond", "Download your kit.", THANKS_MAIN, THANKS_JS, False)
