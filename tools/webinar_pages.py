# -*- coding: utf-8 -*-
# Webinar giveaway landing pages for revenueandbeyond.com (Nov 2026). Self-contained: own CSS, Netlify Forms gate.
import os, html, json
D=os.path.dirname(os.path.abspath(__file__))
E=lambda t: html.escape(t, quote=True)
DL='/assets/downloads/webinar-7q4k/'

CSS = r"""
:root{--teal:#0B363B;--green:#49E8B0;--purple:#C3A1F8;--sky:#6AD1FA;--black:#1C1C1C;--off:#F5F4F0;--div:#E2DFD7;--muted:rgba(28,28,28,.68);--ln:2px solid var(--teal)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--off);color:var(--black);font-family:Inter,Arial,sans-serif;font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;
 background-image:radial-gradient(rgba(11,54,59,.10) 1.5px,transparent 1.6px);background-size:26px 26px}
a{color:var(--teal)}img{max-width:100%;height:auto;display:block}
h1,h2,h3{font-weight:900;letter-spacing:-.035em;line-height:1.05;margin:0;color:var(--black)}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
header.top{position:sticky;top:0;z-index:20;background:rgba(245,244,240,.92);backdrop-filter:blur(8px);border-bottom:1.5px solid var(--div)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;height:72px}
.logo{font-weight:900;letter-spacing:-.045em;font-size:24px;color:var(--teal);text-decoration:none}
.logo .amp{color:var(--teal)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--green);color:var(--teal);border:2px solid var(--teal);box-shadow:4px 4px 0 var(--teal);border-radius:16px;padding:12px 20px;font-weight:800;font-size:16px;text-decoration:none;cursor:pointer;font-family:inherit;transition:transform .12s,box-shadow .12s}
.btn:hover{transform:translate(-1px,-1px);box-shadow:5px 5px 0 var(--teal)}
.btn:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--teal)}
.btn.ghost{background:#fff}.btn.sm{padding:9px 16px;font-size:14.5px;border-radius:14px;box-shadow:3px 3px 0 var(--teal)}
.btn.block{width:100%}
.tape{display:inline-block;background:#fff;border:2px solid var(--teal);border-radius:8px;box-shadow:2px 2px 0 var(--teal);padding:5px 11px;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);transform:rotate(-1.5deg)}
.kick{font-family:'Caveat Brush',cursive;font-size:30px;color:var(--teal);line-height:1}
.hl{position:relative;display:inline-block;padding:0 8px;color:var(--teal);z-index:0}
.hl::before{content:"";position:absolute;inset:4px -2px -2px;background:var(--green);border-radius:8px;transform:rotate(-1.2deg);z-index:-1}
.card{background:#fff;border:var(--ln);border-radius:20px;padding:26px;box-shadow:6px 6px 0 var(--teal)}
.card.g{box-shadow:6px 6px 0 var(--green)}.card.p{box-shadow:6px 6px 0 var(--purple)}.card.s{box-shadow:6px 6px 0 var(--sky)}
.hero{padding:64px 0 40px}
.hero .grid{display:grid;grid-template-columns:1.12fr .88fr;gap:56px;align-items:start}
.hero h1{font-size:clamp(40px,5.6vw,66px);margin:16px 0 18px}
.hero .sub{font-size:20px;line-height:1.55;max-width:560px;margin:0 0 22px}
.price{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin:6px 0 22px}
.price s{font-weight:800;font-size:22px;color:var(--muted)}
.price b{font-weight:900;font-size:40px;letter-spacing:-.03em;color:var(--teal)}
.price span{font-size:14px;color:var(--muted);font-weight:600}
.ticks{list-style:none;padding:0;margin:0 0 10px}
.ticks li{position:relative;padding-left:34px;margin:0 0 12px}
.ticks li::before{content:"";position:absolute;left:0;top:3px;width:22px;height:22px;border-radius:50%;background:var(--purple) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12.5l4 4 8-9' fill='none' stroke='%230B363B' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/14px no-repeat}
.formcard{position:relative;scroll-margin-top:96px}
.formcard h2{font-size:28px;margin:6px 0 6px}
.formcard p.note{font-size:14.5px;color:var(--muted);margin:0 0 18px}
label{display:block;font-weight:700;font-size:14.5px;margin:0 0 6px;color:var(--teal)}
input[type=text],input[type=email],input[type=url]{width:100%;font:inherit;font-size:16px;padding:13px 14px;border:2px solid var(--teal);border-radius:12px;background:var(--off);margin:0 0 14px;color:var(--black)}
input:focus{outline:none;box-shadow:0 0 0 4px rgba(73,232,176,.45);background:#fff}
.opt{font-weight:500;color:var(--muted)}
.check{display:flex;gap:10px;align-items:flex-start;font-weight:500;font-size:14px;color:var(--black);margin:2px 0 18px;cursor:pointer}
.check input{width:19px;height:19px;margin:2px 0 0;accent-color:var(--teal);flex:none}
.fine{font-size:12.5px;color:var(--muted);margin:12px 0 0;text-align:center}
.hp{position:absolute;left:-9999px}
.err{display:none;color:#A1261B;font-size:14px;font-weight:600;margin:-4px 0 12px}
.done{display:none}
.done.show{display:block}
.done h2{font-size:30px}
.dl{display:flex;align-items:center;gap:14px;background:var(--off);border:2px solid var(--teal);border-radius:14px;padding:14px 16px;margin:12px 0;text-decoration:none;color:var(--black);box-shadow:3px 3px 0 var(--green);transition:transform .12s}
.dl:hover{transform:translate(-1px,-1px)}
.dl .ic{flex:none;width:42px;height:42px;border-radius:10px;background:var(--teal);color:var(--green);display:grid;place-items:center;font-weight:900;font-size:12px;letter-spacing:.04em}
.dl b{display:block;color:var(--teal);font-size:16px}.dl small{color:var(--muted);font-size:13.5px}
.dl .ar{margin-left:auto;font-weight:900;color:var(--teal);font-size:20px}
section.band{padding:72px 0}
.sh{max-width:720px;margin:0 0 34px}
.sh h2{font-size:clamp(32px,4vw,46px);margin:12px 0 12px}
.sh p{font-size:18.5px;margin:0;color:var(--muted)}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.g3 h3{font-size:22px;margin:8px 0 8px;color:var(--teal)}
.g3 p{margin:0;font-size:16px}
.num{font-family:'Caveat Brush',cursive;font-size:52px;line-height:.9;color:var(--teal);text-shadow:3px 3px 0 var(--green)}
.card.p .num{text-shadow:3px 3px 0 var(--purple)}.card.s .num{text-shadow:3px 3px 0 var(--sky)}
.tealband{background:var(--teal);color:#fff;background-image:radial-gradient(rgba(255,255,255,.10) 1.5px,transparent 1.6px);background-size:26px 26px}
.tealband h2,.tealband h3{color:#fff}.tealband .sh p{color:rgba(255,255,255,.78)}
.tealband .tape{color:var(--teal)}
.sample{background:#fff;color:var(--black);border:2px solid var(--teal);border-radius:20px;padding:24px 26px;box-shadow:8px 8px 0 var(--green);font-size:15.5px}
.sample .lab{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:14px 0 4px;display:block}
.sample .lab:first-child{margin-top:0}
.sample p{margin:0}
.sample blockquote{margin:6px 0 0;padding:10px 14px;border-left:4px solid var(--green);background:#F2FBF7;border-radius:0 10px 10px 0;font-style:italic}
.pill{display:inline-block;background:#FDE6E2;color:#8A2416;border:1.5px solid #8A2416;border-radius:999px;padding:1px 10px;font-weight:800;font-size:13px}
.preview{filter:drop-shadow(0 18px 30px rgba(11,54,59,.18))}
.about{display:grid;grid-template-columns:220px 1fr;gap:36px;align-items:center}
.about img{width:220px;height:220px;object-fit:cover;border-radius:24px;border:3px solid var(--teal);box-shadow:8px 8px 0 var(--purple)}
.about h2{font-size:36px;margin:10px 0 12px}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin-top:18px}
.stat{background:#fff;border:2px solid var(--teal);border-radius:14px;padding:10px 14px;box-shadow:3px 3px 0 var(--green);font-size:14px;font-weight:600}
.stat b{display:block;font-size:20px;color:var(--teal);font-weight:900;letter-spacing:-.02em}
.faq{max-width:820px}
details{background:#fff;border:2px solid var(--teal);border-radius:16px;padding:0 22px;margin:0 0 14px;box-shadow:4px 4px 0 var(--teal)}
details:nth-child(3n+2){box-shadow:4px 4px 0 var(--purple)}details:nth-child(3n){box-shadow:4px 4px 0 var(--sky)}
summary{cursor:pointer;list-style:none;font-weight:800;font-size:17.5px;padding:18px 34px 18px 0;position:relative;color:var(--teal)}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:0;top:12px;font-size:28px;font-weight:700}
details[open] summary::after{content:"\2013"}
details p{margin:0 0 18px}
.final{text-align:center}
.final h2{font-size:clamp(32px,4.2vw,50px);margin:14px auto 14px;max-width:780px}
.final p{max-width:620px;margin:0 auto 26px;font-size:18.5px;color:rgba(255,255,255,.8)}
.final .btn{box-shadow:4px 4px 0 #062226}
footer{padding:34px 0;font-size:14px;color:var(--muted);border-top:1.5px solid var(--div)}
footer .wrap{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
footer a{color:var(--muted)}
.rainbow{height:5px;background:linear-gradient(90deg,var(--green),var(--purple),var(--sky))}
nav.mini{display:flex;align-items:center;gap:22px}
nav.mini a.l{font-weight:600;font-size:15px;text-decoration:none;color:var(--black)}
nav.mini a.l:hover{color:var(--teal);text-decoration:underline;text-underline-offset:4px}
.book{display:grid;grid-template-columns:1.3fr .7fr;gap:36px;align-items:center}
.book h2{font-size:clamp(30px,3.8vw,44px);margin:12px 0 12px}
.book p{margin:0 0 10px;font-size:17.5px}
.book ul{margin:8px 0 0}
.book .side{text-align:center}
.book .side img{width:150px;height:150px;object-fit:cover;border-radius:22px;border:3px solid var(--teal);box-shadow:6px 6px 0 var(--green);margin:0 auto 18px}
.book .side small{display:block;margin-top:12px;color:var(--muted);font-size:13.5px}
.more{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
a.mc{display:block;min-width:0;overflow-wrap:anywhere;background:#fff;border:2px solid var(--teal);border-radius:16px;padding:20px;text-decoration:none;color:var(--black);box-shadow:4px 4px 0 var(--teal);transition:transform .12s}
a.mc:nth-child(2){box-shadow:4px 4px 0 var(--green)}a.mc:nth-child(3){box-shadow:4px 4px 0 var(--purple)}a.mc:nth-child(4){box-shadow:4px 4px 0 var(--sky)}
a.mc:hover{transform:translate(-2px,-2px)}
a.mc b{display:block;font-size:19px;font-weight:900;letter-spacing:-.02em;color:var(--teal);margin-bottom:6px}
a.mc span{font-size:15px;color:var(--muted)}
a.mc i{display:block;font-style:normal;font-weight:800;color:var(--teal);margin-top:12px;font-size:14.5px}
footer.full{padding:44px 0 30px}
footer.full .wrap{display:block}
footer.full .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px;margin-bottom:26px}
footer.full h4{margin:0 0 10px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}
footer.full ul{list-style:none;margin:0;padding:0}footer.full li{margin:0 0 7px}
footer.full a{color:var(--black);text-decoration:none}footer.full a:hover{text-decoration:underline}
footer.full .base{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;border-top:1.5px solid var(--div);padding-top:18px}
@media (max-width:900px){
 nav.mini a.l{display:none}
 .book,.more,footer.full .cols{grid-template-columns:1fr}

 .hero{padding:36px 0 20px}.hero .grid,.g2,.about{grid-template-columns:1fr;gap:34px}
 .g3{grid-template-columns:1fr}.about img{width:160px;height:160px}
 header.top .btn{padding:8px 12px;font-size:13.5px}section.band{padding:54px 0}
}
"""

JS = r"""
(function(){
  var f=document.getElementById('kitform'); if(!f) return;
  var done=document.getElementById('done'), err=document.getElementById('err'), product=f.getAttribute('data-product');
  var KEY='rb_webinar_'+product;
  function track(n,p){try{(window.gtag||function(){(window.dataLayer=window.dataLayer||[]).push(arguments);})('event',n,p||{});}catch(e){}}
  function reveal(){f.style.display='none';done.classList.add('show');try{localStorage.setItem(KEY,'1')}catch(e){}}
  try{if(localStorage.getItem(KEY)==='1'){f.style.display='none';done.classList.add('show');}}catch(e){}
  document.querySelectorAll('a[data-track=book]').forEach(function(a){a.addEventListener('click',function(){track('book_call_click',{item_id:product});});});
  done.querySelectorAll('a.dl').forEach(function(a){a.addEventListener('click',function(){track('webinar_download',{item_id:product,file:a.getAttribute('href').split('/').pop()});});});
  f.addEventListener('submit',function(e){
    e.preventDefault(); err.style.display='none';
    var em=f.querySelector('[name=email]').value.trim(), nm=f.querySelector('[name=first-name]').value.trim();
    if(!nm||!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){err.textContent='Please add your first name and a valid email.';err.style.display='block';return;}
    var b=f.querySelector('button'); b.disabled=true; b.textContent='Sending...';
    var body={product:product,source:'webinar',email:em,first_name:nm,company:f.querySelector('[name=company]').value.trim(),
      newsletter:f.querySelector('[name=newsletter]').checked,website:f.querySelector('[name=website]').value};
    fetch('/api/tools/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(function(r){track(r.ok?'generate_lead':'webinar_signup_error',{form_name:'webinar-'+product});reveal();})
      .catch(function(){track('webinar_signup_error',{form_name:'webinar-'+product});reveal();});
  });
})();
"""

def page(k):
    t=k['title']; slug=k['slug']; form=k['form']
    ticks=''.join(f'<li>{E(x)}</li>' for x in k['ticks'])
    inside=''.join(f'<div class="card {c}"><div class="num">{i+1}</div><h3>{E(a)}</h3><p>{b}</p></div>' for i,(c,a,b) in enumerate(zip(['g','p','s'],[x[0] for x in k['inside']],[x[1] for x in k['inside']])))
    how=''.join(f'<div class="card {c}"><div class="num">{i+1}</div><h3>{E(a)}</h3><p>{b}</p></div>' for i,(c,(a,b)) in enumerate(zip(['g','p','s'],k['how'])))
    dls=''.join(f'<a class="dl" href="{DL}{fn}" download><span class="ic">{ext}</span><span><b>{E(lab)}</b><small>{E(desc)}</small></span><span class="ar">&darr;</span></a>' for fn,ext,lab,desc in k['files'])
    faq=''.join(f'<details><summary>{E(q)}</summary><p>{a}</p></details>' for q,a in k['faq'])
    desc=k['meta']
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<title>{E(t)}: free for webinar attendees | Revenue &amp; Beyond</title>
<meta name="description" content="{E(desc)}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="https://revenueandbeyond.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Revenue &amp; Beyond">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{E(t)} | Revenue &amp; Beyond">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="https://revenueandbeyond.com/{slug}/">
<meta property="og:image" content="https://revenueandbeyond.com{DL}{k['preview']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F4F0">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat+Brush&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script src="/assets/js/analytics.js" defer></script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="/" aria-label="Revenue &amp; Beyond, home">Revenue<span class="amp">&amp;</span>Beyond.</a>
<nav class="mini" aria-label="Main site">
<a class="l" href="/">Home</a><a class="l" href="/about/">About</a><a class="l" href="/insights/">Insights</a><a class="l" href="/newsletter/">Newsletter</a>
<a class="btn sm" href="#get">Get the kit free</a>
</nav>
</div></header>

<main>
<section class="hero"><div class="wrap grid">
<div>
<span class="tape">Free for webinar attendees</span>
<div class="kick" style="margin-top:22px">{E(k['kicker'])}</div>
<h1>{k['h1']}</h1>
<p class="sub">{k['sub']}</p>
<div class="price"><s>&pound;99 +VAT</s><b>Free</b><span>for everyone on the webinar</span></div>
<ul class="ticks">{ticks}</ul>
<p style="font-size:15px;color:var(--muted);margin:14px 0 0"><b style="color:var(--teal)">Best for:</b> {k['bestfor']}</p>
</div>

<div class="card p formcard" id="get">
<form id="kitform" name="{form}" data-product="{form}" method="POST" action="#" novalidate>
<p class="hp" aria-hidden="true"><label>Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label></p>
<span class="tape" style="transform:rotate(1.5deg)">Instant download</span>
<h2>Get the {E(t)}</h2>
<p class="note">Tell me where to send updates and the download links appear straight away.</p>
<label for="fn">First name</label><input type="text" id="fn" name="first-name" autocomplete="given-name" required>
<label for="em">Work email</label><input type="email" id="em" name="email" autocomplete="email" required>
<label for="co">Company website <span class="opt">(optional)</span></label><input type="text" id="co" name="company" autocomplete="url" placeholder="yourcompany.com">
<label class="check"><input type="checkbox" name="newsletter" value="yes"> Also send me The Founder Read, my free weekly newsletter for B2B founders. Unsubscribe any time.</label>
<p class="err" id="err"></p>
<button class="btn block" type="submit">Get my free kit</button>
<p class="fine">No spam. I'll only use your details to know who downloaded the kit and, if you tick the box, to send the newsletter. See the <a href="/privacy-policy.html">privacy policy</a>.</p>
</form>
<div class="done" id="done">
<span class="tape" style="transform:rotate(1.5deg);background:var(--green)">You're in</span>
<h2 style="margin:12px 0 6px">Here's your kit</h2>
<p class="note" style="font-size:15px;color:var(--muted);margin:0 0 6px">Download both files. Bookmark this page if you want to come back to them.</p>
{dls}
<p style="font-size:15px;margin:14px 0 0">{k['done_tip']}</p>
</div>
</div>
</div></section>

<section class="band"><div class="wrap g2">
<div><img class="preview" src="{DL}{k['preview']}" alt="Pages from the {E(t)} guide" width="1100" height="818" loading="lazy"></div>
<div class="sh" style="margin:0"><span class="tape">What's inside</span><h2>{k['inside_h2']}</h2><p>{k['inside_p']}</p></div>
</div>
<div class="wrap" style="margin-top:44px"><div class="g3">{inside}</div></div></section>

<section class="band tealband"><div class="wrap g2">
<div class="sh" style="margin:0"><span class="tape">See it work</span><h2>{k['ex_h2']}</h2><p>{k['ex_p']}</p></div>
<div class="sample">{k['sample']}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sh"><span class="tape">How it works</span><h2>Set up once. Use it on <span class="hl">every deal</span>.</h2></div>
<div class="g3">{how}</div>
</div></section>

<section class="band" style="padding-top:20px"><div class="wrap"><div class="card about">
<img src="{DL}simon-watson.jpg" alt="Simon Watson" width="220" height="220">
<div><span class="tape">Who built it</span>
<h2>I'm Simon Watson.</h2>
<p style="margin:0 0 6px">I'm an exited founder. I've been part of three exits (an IPO, a trade sale and a VC-backed sale) and spent 20+ years selling and scaling B2B businesses across EMEA. Today I co-sell with founders who still run their own sales, so they close more without doing it all themselves.</p>
<p style="margin:0">I built this for my own deals first. It's the same tool I use every week.</p>
<div class="stats"><div class="stat"><b>3 exits</b>IPO, trade sale, VC-backed sale</div><div class="stat"><b>20+ years</b>selling B2B across EMEA</div><div class="stat"><b>8-figure exit</b>a founder-led agency, in 26 months</div></div>
</div></div></div></section>

<section class="band" style="padding-top:20px"><div class="wrap">
<div class="sh"><span class="tape">Questions</span><h2>Good to know</h2></div>
<div class="faq">{faq}</div>
</div></section>

<section class="band" id="book"><div class="wrap"><div class="card g book">
<div><span class="tape">Free 30-minute call</span>
<h2>{k['book_h2']}</h2>
<p>{k['book_p']}</p>
<ul class="ticks"><li>Bring a live deal, a stalled prospect or your sales numbers</li><li>Leave with two or three things to do this month</li><li>No pitch unless you ask for one</li></ul>
</div>
<div class="side"><img src="{DL}simon-watson.jpg" alt="Simon Watson" width="150" height="150" loading="lazy">
<a class="btn" href="/book/" data-track="book">Book a call with me</a>
<small>Pick a time that suits you. Takes a minute.</small></div>
</div></div></section>

<section class="band" style="padding-top:10px"><div class="wrap">
<div class="sh"><span class="tape">More from me</span><h2>Keep <span class="hl">exploring</span></h2><p>Head over to the main site for more on founder-led sales, pricing and building a business that sells.</p></div>
<div class="more">
<a class="mc" href="/insights/"><b>Insights</b><span>Stories and lessons from three exits and the founders I work with.</span><i>Read the articles &rarr;</i></a>
<a class="mc" href="/newsletter/"><b>The Founder Read</b><span>My free weekly newsletter. Three minutes, every Sunday evening.</span><i>Subscribe free &rarr;</i></a>
<a class="mc" href="/blueprint/"><b>Founder-led sales blueprint</b><span>Seven parts and a scorecard to get sales out of your head.</span><i>Get the free guide &rarr;</i></a>
<a class="mc" href="/"><b>revenueandbeyond.com</b><span>How I help B2B founders sell more without doing it all themselves.</span><i>Visit the website &rarr;</i></a>
</div>
</div></section>
</main>
<div class="rainbow"></div>
<footer class="full"><div class="wrap">
<div class="cols">
<div><a class="logo" href="/">Revenue<span class="amp">&amp;</span>Beyond.</a><p style="margin:10px 0 0;font-size:14.5px;color:var(--muted)">Build, scale and sell your B2B business. That's what I help founders do.</p></div>
<div><h4>Explore</h4><ul><li><a href="/">Home</a></li><li><a href="/about/">About</a></li><li><a href="/testimonials/">Testimonials</a></li><li><a href="/work-with-me/">Work with me</a></li></ul></div>
<div><h4>Free content</h4><ul><li><a href="/insights/">Insights</a></li><li><a href="/newsletter/">Newsletter</a></li><li><a href="/blueprint/">Sales blueprint</a></li></ul></div>
<div><h4>Get in touch</h4><ul><li><a href="/book/">Book a call</a></li><li><a href="https://www.linkedin.com/in/simonwatson13" rel="noopener">LinkedIn</a></li><li><a href="mailto:simon@revenueandbeyond.com">simon@revenueandbeyond.com</a></li></ul></div>
</div>
<div class="base"><span>&copy; 2026 Revenue &amp; Beyond. London.</span><span><a href="/privacy-policy.html">Privacy Policy</a> &nbsp;&middot;&nbsp; <a href="/terms-of-service.html">Terms of Service</a></span></div>
</div></footer>
<script>{JS}</script>
</body>
</html>'''

OC=dict(slug='webinar/objection-coach',form='objection-coach',title='Objection Coach',kicker='PDF + AI prompt',
 h1='Know what the prospect <span class="hl">really</span> means.',
 sub='Paste what the prospect said. Get what it really means, the questions that bring out the real objection, and three replies you can use today.',
 ticks=['Set up in five minutes in Claude or ChatGPT','The eight objections you\'ll hear most, decoded','Three replies every time, for email or a call'],
 bestfor='Founders whose deals stall at "let\'s push to Q1" or "send me something".',
 meta='Objection Coach: paste what the prospect said and get what it really means, the questions to ask and three replies you can use today. Free for webinar attendees.',
 preview='oc-preview.png',
 files=[('RnB-Objection-Coach.pdf','PDF','Objection Coach guide (PDF)','6 pages: set-up, the method, the eight objections, the prompt'),
        ('Objection-Coach-Prompt.txt','TXT','The prompt, ready to paste','Copy into a Claude or ChatGPT Project')],
 done_tip='<b>Start here:</b> open the PDF at page 2, then paste the prompt file into a new Claude Project. Five minutes, then try it on the last objection you heard.',
 inside_h2='Your objection-handling coach, <span class="hl">on call</span>',
 inside_p='A six-page guide and a ready-to-paste prompt. Fill in your offer, rules and proof once, and every reply sounds like you.',
 inside=[('The method','Seven ideas behind every answer. Every objection is a trust gap, not a fact, so you diagnose before you reply.'),
         ('The eight objections, decoded','"Push to Q1", "no budget", "send me a proposal", silence after a proposal, and four more. What each one usually means and the first question to ask.'),
         ('The prompt','A full coaching prompt with a worked example. Role-play a tough call, prep for a meeting, or tighten a draft in one line.')],
 ex_h2='One stall. Three ways to <span class="hl" style="color:var(--teal)">move it</span>.',
 ex_p='Every answer gives you a read on the deal, the questions to ask and three replies: diagnose, reframe or a clean takeaway.',
 sample='''<span class="lab">You paste</span><p>"For timing purposes I think we need to push this to Q1. Let's reconnect in January."</p>
<span class="lab">Deal risk</span><p><span class="pill">High</span> Thirteen months, two proposals, silence since the founders met.</p>
<span class="lab">What they really mean</span><p>"Not now" is covering a question nobody has answered: what did the founders actually say?</p>
<span class="lab">Option 1: Diagnose</span><blockquote>When the founders met, was Q1 their call because of delivery, or was there something in the proposal that didn't sit right? If it's the proposal, I'd rather know now than in January.</blockquote>''',
 how=[('Create a Project','In Claude or ChatGPT, create a project called "Objection Coach" and paste in the prompt.'),
      ('Add your business','Fill in what you sell, your rules (like "never discount") and your proof. Five minutes.'),
      ('Paste the objection','Drop in the email or your call notes. Get the read, the questions and three replies.')],
 faq=[('Is it really free?','Yes, for everyone on the webinar. It normally sells for &pound;99 +VAT. Share it with your team too.'),
      ('Do I need a paid AI account?','No. It works on free Claude and ChatGPT accounts. A paid plan gives you Projects and more messages, which makes daily use easier.'),
      ('Will the replies sound like me?','Yes, once you fill in your rules and add two or three emails you\'re proud of to the project files. It learns your tone from them.'),
      ('What happens to my details?','I keep them so I know who downloaded this kit and, only if you tick the box, my weekly newsletter. Nothing else, and you can unsubscribe at any time.')],
 book_h2='Got a deal stuck at <span class="hl">"not now"?</span>',
 book_p='Book a free Diagnosis Call. We will look at one stalled deal together, work out what is really going on, and agree the reply that moves it forward.',
 final_h2='Stop losing deals to <span class="hl">"let\'s push to Q1"</span>')

DC=dict(slug='webinar/discovery-call-prep',form='discovery-prep',title='Discovery Call Prep kit',kicker='Claude skill + discovery guide',
 h1='Walk into every call <span class="hl">prepared</span>.',
 sub='Researches the prospect before the call: company, founder, competitors, reviews and filings. Then a brief with a fit read, the questions to ask and a pre-call message.',
 ticks=['Prospect and competitor research in minutes','7-step discovery call guide and follow-up ladder','Set up once with your ICP and offer'],
 bestfor='Founders running their own discovery calls.',
 meta='Discovery Call Prep kit: a Claude skill that researches your prospect before the call, plus a 7-step discovery guide and follow-up ladder. Free for webinar attendees.',
 preview='dc-preview.png',
 files=[('discovery-call-prep-skill.zip','ZIP','The Claude skill (ZIP)','Upload in Claude under Customize, then Skills'),
        ('RnB-Discovery-Call-Guide.pdf','PDF','Discovery Call Guide (PDF)','Set-up steps, the 7-step call, checklist and follow-up ladder')],
 done_tip='<b>Start here:</b> open the guide at page 2. It walks you through adding your ideal customer and offer, uploading the skill and running your first prep.',
 inside_h2='Your research assistant and your <span class="hl">call plan</span>',
 inside_p='A Claude skill that does the homework, and a five-page guide for running the call and the follow-up.',
 inside=[('The skill','Researches the website, founder, three sized competitors, reviews, Companies House filings and news. Flags claims that don\'t add up.'),
         ('The 7-step discovery call','Open, pain, attempts, a relatable story, a light visual, pause and price, then book the next step. With lines to use at each step.'),
         ('The follow-up ladder','Five follow-ups from same-day recap to a clean takeaway. Each one has a reason to exist. None says "just checking in".')],
 ex_h2='A five-minute read <span class="hl" style="color:var(--teal)">before you dial</span>.',
 ex_p='Type one line with the company and contact. The brief comes back in seven short sections, bottom line first.',
 sample='''<span class="lab">You type</span><p>"Prep me for my discovery call with Acme Analytics, acme.io. I'm meeting Priya, the founder, on Thursday at 2pm."</p>
<span class="lab">Fit read</span><p><b style="color:var(--teal)">Possible fit.</b> Right size and sector, but she is also running a second venture, so bandwidth may be the real constraint.</p>
<span class="lab">Competitors</span><p>Three rivals, sized and priced. The gap is proof: 11 reviews against 300+.</p>
<span class="lab">Ask her</span><blockquote>Your site says 200+ clients. How many of those came from you personally?</blockquote>
<p style="font-size:12.5px;color:var(--muted);margin-top:10px">Illustrative example.</p>''',
 how=[('Add your business','Tell it what you sell, who your ideal customer is and the red flags. Once.'),
      ('Upload the skill','Upload the ZIP in Claude under Customize, then Skills. Ten minutes, step by step in the guide.'),
      ('Type one line','"Prep me for my call with [company]." Read the brief, send the pre-call message, run the call.')],
 faq=[('Is it really free?','Yes, for everyone on the webinar. It normally sells for &pound;99 +VAT.'),
      ('Which Claude plan do I need?','Skills run on Claude\'s free and paid plans with code execution switched on, but research is much better on a paid plan (Pro or above) with web search on. No skills on your plan? The guide shows how to run it from a Claude Project instead.'),
      ('Does it work with ChatGPT?','Yes. Paste the skill file into a ChatGPT Project or Custom GPT\'s instructions and switch on web search. The guide explains how.'),
      ('Is it only for UK companies?','No. It uses Companies House for UK businesses and the public equivalent elsewhere where one exists. Everything else works anywhere.'),
      ('What happens to my details?','I keep them so I know who downloaded this kit and, only if you tick the box, my weekly newsletter. Nothing else, and you can unsubscribe at any time.')],
 book_h2='Want a second pair of eyes on <span class="hl">your pipeline?</span>',
 book_p='Book a free Diagnosis Call. Bring your next discovery call or a deal that has gone quiet, and we will plan how to win it together.',
 final_h2='Be the best-prepared person <span class="hl">on the call</span>.')

OUT=os.environ.get('SITE_OUT',os.path.join(os.path.dirname(D),'site'))
for k in (OC,DC):
    d=os.path.join(OUT,k['slug']); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(page(k))
print('ok')
