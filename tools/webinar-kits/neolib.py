# -*- coding: utf-8 -*-
# Shared neo (website style) PDF helpers for R&B giveaways. Brand Book v1.2.
import base64, html, os, re
D=os.path.dirname(os.path.abspath(__file__))
def b64(p): return base64.b64encode(open(os.path.join(D,p),'rb').read()).decode()
def wordmark(main,amp,size): return f'<span style="font-family:Inter;font-weight:900;letter-spacing:-.045em;font-size:{size}px;color:{main};white-space:nowrap">Revenue<span style="color:{amp}">&amp;</span>Beyond.</span>'
WM_T=wordmark('#0B363B','#0B363B',22); WM_W=wordmark('#FFFFFF','#49E8B0',34)
def fonts():
    o=''
    for w in (400,500,700,800,900):
        o+="@font-face{font-family:'Inter';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2')}\n"%(w,b64(f'node_modules/@fontsource/inter/files/inter-latin-{w}-normal.woff2'))
    o+="@font-face{font-family:'Caveat Brush';src:url(data:font/woff2;base64,%s) format('woff2')}\n"%b64('node_modules/@fontsource/caveat-brush/files/caveat-brush-latin-400-normal.woff2')
    return o
CSS=r"""
:root{--teal:#0B363B;--green:#49E8B0;--purple:#C3A1F8;--sky:#6AD1FA;--black:#1C1C1C;--off:#F5F4F0;--div:#E8E6E0;--muted:rgba(28,28,28,.66);--ln:2px solid var(--teal)}
@page{size:794px 1123px;margin:0}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{background:#E9E7E1;color:var(--black);font-family:'Inter',Arial,sans-serif;font-size:12.4px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body.pdf{background:none}
h1,h2,h3{margin:0;color:var(--black);font-weight:900;letter-spacing:-.03em;line-height:1.08}
p{margin:0 0 8px}ul,ol{margin:0;padding:0;list-style:none}b,strong{font-weight:700}
.pg{position:relative;width:794px;height:1123px;overflow:hidden;background-color:var(--off);
 background-image:radial-gradient(rgba(11,54,59,.13) 1.5px,transparent 1.6px);background-size:22px 22px;background-position:11px 11px;
 margin:0 auto 24px;padding:46px 56px 80px;break-after:page}
body.pdf .pg{margin:0}
.pf{position:absolute;left:0;right:0;bottom:0;height:46px;padding:0 56px;display:flex;align-items:center;justify-content:space-between;font-size:8.4px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.pf::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,var(--green),var(--purple),var(--sky))}
.pf .pn{font-family:'Caveat Brush',cursive;font-size:17px;letter-spacing:.02em;color:var(--teal);text-transform:none}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.tape{display:inline-block;background:#fff;border:2px solid var(--teal);border-radius:8px;box-shadow:2px 2px 0 var(--teal);padding:4px 10px;font-size:9px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);transform:rotate(-1deg)}
h2.t{font-size:34px;letter-spacing:-.035em;margin:0 0 12px}
.hl{position:relative;display:inline-block;padding:0 6px;color:var(--teal);z-index:0}
.hl::before{content:"";position:absolute;inset:2px -1px -1px;background:var(--green);border-radius:6px;transform:rotate(-1.2deg);z-index:-1}
h3.s{font-size:16px;color:var(--teal);letter-spacing:-.02em;margin:22px 0 10px}
.lead{font-size:14px;line-height:1.55;max-width:620px}
.muted{color:var(--muted)}.small{font-size:10.6px;line-height:1.45}
.card{background:#fff;border:var(--ln);border-radius:16px;padding:16px 18px;box-shadow:5px 5px 0 var(--teal)}
.card.g{box-shadow:5px 5px 0 var(--green)}.card.p{box-shadow:5px 5px 0 var(--purple)}.card.s{box-shadow:5px 5px 0 var(--sky)}
.tg{background:#D6F7EA}.tp{background:#EEE3FD}.ts{background:#DDF3FC}
.lab{display:block;font-size:9.2px;font-weight:800;text-transform:uppercase;letter-spacing:.14em;color:var(--teal);margin-bottom:8px}
.grid{display:grid;gap:18px}.c2{grid-template-columns:1fr 1fr}.c3{grid-template-columns:repeat(3,1fr)}.grid>*{min-width:0}
.mt{margin-top:18px}.mt2{margin-top:26px}
.ul li{position:relative;padding-left:20px;margin-bottom:7px;line-height:1.48}
.ul li::before{content:"";position:absolute;left:0;top:5px;width:9px;height:9px;border-radius:50%;background:var(--green);border:1.5px solid var(--teal)}
.steps li{position:relative;padding-left:42px;margin-bottom:12px;min-height:28px;line-height:1.48}
.steps li .n{position:absolute;left:0;top:-4px;font-family:'Caveat Brush',cursive;font-size:30px;line-height:1;color:var(--teal);text-shadow:2px 2px 0 var(--green)}
.big{font-family:'Caveat Brush',cursive;font-size:38px;line-height:1;color:var(--teal);text-shadow:2px 2px 0 var(--green)}
.idea{display:grid;grid-template-columns:44px 1fr;gap:12px;padding:9px 0;border-top:1.5px solid var(--div)}
.idea:first-child{border-top:0}
.idea b{color:var(--teal);font-size:13px}
table.tb{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:var(--ln);border-radius:14px;overflow:hidden;box-shadow:5px 5px 0 var(--teal)}
.tb th{background:var(--teal);color:#fff;text-align:left;font-size:8.6px;text-transform:uppercase;letter-spacing:.14em;padding:10px 12px;font-weight:800}
.tb td{padding:10px 12px;border-top:1.5px solid var(--div);vertical-align:top;font-size:11.8px;line-height:1.42}
.tb tr:nth-child(2) td{border-top:0}
.tb td:first-child{font-weight:700;color:var(--teal)}
.prompt{background:#fff;border:var(--ln);border-radius:16px;padding:18px 24px;box-shadow:5px 5px 0 var(--teal);font-size:11.6px;line-height:1.5}
.prompt .ph{font-size:9.6px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:16px 0 7px;padding-top:12px;border-top:1.5px solid var(--div)}
.prompt .ph:first-child{margin-top:0;padding-top:0;border-top:0}
.prompt p{margin:0 0 5px}
.prompt ul li{position:relative;padding-left:14px;margin-bottom:4px}
.prompt ul li::before{content:"\2013";position:absolute;left:0;color:var(--teal)}
.prompt ol li{display:grid;grid-template-columns:18px 1fr;margin-bottom:5px}
.prompt ol li i{font-style:normal;font-weight:800;color:var(--teal)}
.prompt blockquote{margin:1px 0 4px 14px;padding-left:10px;border-left:3px solid var(--green);font-style:italic}
.fill{background:#EEE3FD;border:1.5px solid #9E74E8;border-radius:5px;padding:0 4px;font-weight:700;color:#4B1FA0;white-space:nowrap}
.cont{font-size:9.6px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.cta{background:var(--teal);color:#fff;border-radius:16px;padding:20px 24px;box-shadow:5px 5px 0 var(--green);display:flex;justify-content:space-between;align-items:center;gap:20px}
.cta h3{color:#fff;font-size:19px}
.btn{display:inline-block;background:var(--green);color:var(--teal);border:2px solid var(--teal);box-shadow:4px 4px 0 #062226;border-radius:16px;padding:10px 16px;font-weight:800;font-size:12.5px;white-space:nowrap}
.pg.cv{background-color:var(--teal);background-image:radial-gradient(rgba(255,255,255,.14) 1.5px,transparent 1.6px);color:#fff;padding:60px}
.cv .tape{color:var(--teal)}
.cvt{font-size:84px;line-height:.92;letter-spacing:-.05em;color:#fff;font-weight:900;margin:22px 0 22px}
.cvt .dot{color:var(--green)}
.cv .sub{font-size:18px;line-height:1.5;color:rgba(255,255,255,.88);max-width:540px}
.cvcard{background:var(--off);color:var(--black);border:2px solid var(--teal);border-radius:16px;padding:16px 18px;box-shadow:5px 5px 0 var(--green)}
.cvcard:nth-child(2){box-shadow:5px 5px 0 var(--purple)}.cvcard:nth-child(3){box-shadow:5px 5px 0 var(--sky)}
.cvcard b{display:block;font-size:17px;font-weight:900;color:var(--teal);letter-spacing:-.02em;margin-bottom:4px}
.sig{font-family:'Caveat Brush',cursive;font-size:30px;color:var(--green)}
/* discovery guide extras */
.step{display:grid;grid-template-columns:58px 1fr;gap:14px;background:#fff;border:var(--ln);border-radius:16px;padding:12px 18px;margin-bottom:10px}
.step .num{font-family:'Caveat Brush',cursive;font-size:44px;line-height:.9;color:var(--teal);text-shadow:3px 3px 0 var(--green)}
.step:nth-child(3n+2) .num{text-shadow:3px 3px 0 var(--purple)}.step:nth-child(3n) .num{text-shadow:3px 3px 0 var(--sky)}
.step h4{margin:0 0 3px;font-size:15px;font-weight:900;color:var(--teal);letter-spacing:-.02em}
.step .say{margin-top:8px;padding:9px 12px;font-size:12px;border-left:3px solid var(--green);background:#F3FBF7;border-radius:0 8px 8px 0;font-style:italic;font-size:11.4px}
.step .goal{font-size:9px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-left:6px}
.ladder{position:relative;padding-left:30px}
.ladder::before{content:"";position:absolute;left:11px;top:8px;bottom:8px;width:3px;background:linear-gradient(var(--green),var(--purple),var(--sky));border-radius:3px}
.rung{position:relative;background:#fff;border:var(--ln);border-radius:14px;padding:11px 15px;margin-bottom:11px;box-shadow:4px 4px 0 var(--teal)}
.rung::before{content:"";position:absolute;left:-26px;top:14px;width:14px;height:14px;border-radius:50%;background:var(--green);border:2px solid var(--teal)}
.rung .when{display:inline-block;font-family:'Caveat Brush',cursive;font-size:22px;color:var(--teal);margin-right:8px;line-height:1}
.rung b.h{font-size:13.5px;color:var(--teal)}
.rung .msg{margin-top:6px;padding:7px 10px;border-left:3px solid var(--purple);background:#F8F4FE;border-radius:0 8px 8px 0;font-size:11.2px;font-style:italic}
.code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.8px;background:#fff;border:1.5px solid var(--div);border-radius:6px;padding:1px 5px;color:var(--teal);font-weight:700}
"""
def esc(t): return html.escape(t,quote=False)
def top(label): return f'<div class="top"><span class="tape">{label}</span><div>{WM_T}</div></div>'
def build(P,title,out):
    n=len(P);o=[]
    for i,(cls,b) in enumerate(P):
        f='' if cls=='cv' else f'<div class="pf"><span>Revenue &amp; Beyond</span><span>{title}</span><span class="pn">{i+1} / {n}</span></div>'
        o.append(f'<section class="pg {cls}">{b}{f}</section>')
    doc=f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{title}</title><style>{fonts()}{CSS}</style></head><body class="pdf">{"".join(o)}</body></html>'
    open(out,'w').write(doc)
def cover(tape,title_html,sub,cards):
    c=''.join(f'<div class="cvcard"><b>{a}</b><span class="small">{b}</span></div>' for a,b in cards)
    return f'''<div>{WM_W}</div>
<div style="margin-top:120px"><span class="tape">{tape}</span>
<div class="cvt">{title_html}</div>
<p class="sub">{sub}</p></div>
<div style="position:absolute;left:60px;right:60px;bottom:60px">
<div class="grid c3" style="gap:20px">{c}</div>
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:44px;padding-top:18px;border-top:1px solid rgba(255,255,255,.2)">
<div><span class="sig">Simon Watson</span><br><span style="font-size:11.5px;color:rgba(255,255,255,.72)">Founder, Revenue &amp; Beyond. Exited founder, three exits.</span></div>
<div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.62)">revenueandbeyond.com</div></div></div>'''
