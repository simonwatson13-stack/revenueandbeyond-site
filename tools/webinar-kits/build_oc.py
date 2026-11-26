# -*- coding: utf-8 -*-
# Objection Coach, webinar edition (Nov 2026). Content from rnb-objection-coach-prompt.md (public version).
import re, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from neolib import *
TITLE='Objection Coach'
def inline(t):
    t=esc(t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'\[([^\]]+)\]',r'<span class="fill">\1</span>',t)
    return t
md=open(os.path.join(D,'oc/rnb-objection-coach-prompt.md')).read()
body=md[md.index('\nSTART OF PROMPT\n')+17:md.index('\nEND OF PROMPT')]
secs=[];cur=None
for l in body.split('\n'):
    if l.startswith('# '): cur=[l[2:],[]];secs.append(cur)
    elif cur: cur[1].append(l)
def sec_html(title,lines):
    out=[f'<div class="ph">{inline(title)}</div>'];mode=None
    def close():
        nonlocal mode
        if mode: out.append(f'</{mode}>'); mode=None
    for l in lines:
        l=l.rstrip()
        if not l or l=='---' or re.match(r'^\|\s*-',l):
            if not l: close()
            continue
        if l.startswith('|'):
            c=[x.strip() for x in l.split('|')[1:-1]]
            if c[0]=='They say': continue
            if mode!='ul': close(); out.append('<ul>'); mode='ul'
            out.append(f'<li><b>{inline(c[0])}</b>: usually means {inline(c[1] if c[1].startswith("I ") else c[1][0].lower()+c[1][1:])}. First question: {inline(c[2])}</li>'); continue
        if l.startswith('>'):
            close(); t=l[1:].strip()
            if t: out.append(f'<blockquote>{inline(t)}</blockquote>')
            continue
        if l.startswith('- '):
            if mode!='ul': close(); out.append('<ul>'); mode='ul'
            out.append(f'<li>{inline(l[2:])}</li>'); continue
        m=re.match(r'^(\d+)\. (.*)',l)
        if m:
            if mode!='ol': close(); out.append('<ol>'); mode='ol'
            out.append(f'<li><i>{m.group(1)}.</i><span>{inline(m.group(2))}</span></li>'); continue
        close(); out.append(f'<p>{inline(l)}</p>')
    close(); return ''.join(out)
S={t:l for t,l in secs}
PROMPT_PAGES=[
  ''.join(sec_html(k,S[k]) for k in ['Role','My business [FILL IN]','My rules [FILL IN]','My proof [FILL IN]','The method']),
  ''.join(sec_html(k,S[k]) for k in ['Common objections: what they usually mean','What to give me','Other things I may ask for']),
  sec_html('Worked example',S['Worked example']),
]
P=[]
def page(b,cls=''): P.append((cls,b))
page(cover('Webinar edition','Objection<br>Coach<span class="dot">.</span>',
 'Paste what the prospect said. Get what it really means, the questions that bring out the real objection, and three replies you can send or say today.',
 [('Diagnose','What they really mean, and how healthy the deal is.'),('Surface','The questions that bring the real objection out.'),('Respond','Three replies, as an email and as words for a call.')]),'cv')

page(top('Start here')+'''
<h2 class="t">Turn every "not now" into a <span class="hl">next step</span></h2>
<p class="lead">Very few deals end with a firm "no". Most just pause. "Let's push to Q1." "Send me something." "I need to think about it." Each one is an invitation to ask a better question. I built this so you can see what is really going on, and reply with confidence.</p>
<h3 class="s">Set it up in five minutes</h3>
<ul class="steps">
<li><span class="n">1</span>In Claude, create a new <b>Project</b> called "Objection Coach". ChatGPT works too: use a Custom GPT or Project.</li>
<li><span class="n">2</span>Open the project instructions and paste the prompt. The quickest way is the <b>Objection-Coach-Prompt.txt</b> file that came with this PDF. Or copy everything inside the white boxes on pages 4 to 6.</li>
<li><span class="n">3</span>Replace the <span class="fill">highlighted</span> text with your own offer, rules and proof. The more specific you are, the sharper the replies.</li>
<li><span class="n">4</span>Optional: add your proposal template, pricing, case studies and two or three emails you are proud of to the project files, so it learns how you write.</li>
<li><span class="n">5</span>Start a new chat in the project. Paste what the prospect said, plus a line or two of deal history.</li>
</ul>
<div class="grid c2 mt2">
<div class="card g"><span class="lab">Day to day</span><ul class="ul">
<li>Paste the email, message or call notes. Add how long you have been talking, what they have seen and what you last sent.</li>
<li>Follow up in the same chat: "Make option 2 shorter." "They replied with this."</li></ul></div>
<div class="card p"><span class="lab">Three commands worth knowing</span><ul class="ul">
<li><b>Role-play:</b> it plays the prospect, then scores you when you say "end scene".</li>
<li><b>Prep me for [name]:</b> the likely objections and the one question you must ask.</li>
<li><b>Tighten:</b> shorter, sharper drafts.</li></ul></div></div>
<h3 class="s" style="margin-top:28px">Every answer gives you three options</h3>
<div class="grid c3" style="gap:16px;margin-bottom:0">
<div class="card g tg" style="padding:13px 15px"><b style="color:var(--teal);font-size:14px">1. Diagnose</b><p class="small" style="margin:4px 0 0">Recommended first. Asks the question that brings out the real objection.</p></div>
<div class="card p tp" style="padding:13px 15px"><b style="color:var(--teal);font-size:14px">2. Reframe</b><p class="small" style="margin:4px 0 0">Changes how they see the timing, cost or risk, often with a smaller first step.</p></div>
<div class="card s ts" style="padding:13px 15px"><b style="color:var(--teal);font-size:14px">3. Clean takeaway</b><p class="small" style="margin:4px 0 0">Closes it off politely and stops the chasing. Often the move that restarts a deal.</p></div></div>
<h3 class="s" style="margin-top:28px">The January objection: three moves that keep the deal moving</h3>
<div class="grid c3" style="gap:16px">
<div class="card g" style="padding:13px 15px"><span class="big" style="font-size:30px">1</span><b style="display:block;color:var(--teal);font-size:14px;margin-top:2px">Ask what changes.</b><p class="small" style="margin:4px 0 0">"If it were January already, what would be different?"</p></div>
<div class="card p" style="padding:13px 15px"><span class="big" style="font-size:30px">2</span><b style="display:block;color:var(--teal);font-size:14px;margin-top:2px">Shrink the first step.</b><p class="small" style="margin:4px 0 0">A smaller start now feels safe to say yes to.</p></div>
<div class="card s" style="padding:13px 15px"><span class="big" style="font-size:30px">3</span><b style="display:block;color:var(--teal);font-size:14px;margin-top:2px">Book the date today.</b><p class="small" style="margin:4px 0 0">A diary slot beats "speak in January".</p></div></div>
''')
ideas=[('Every objection is a trust gap, not a fact.','A stall almost always hides a real objection: value, money, time, authority, risk, or "this won\'t work for us".'),
('Diagnose before you prescribe.','Ask the question that brings out the real objection before answering the stated one.'),
('"No budget" means "I don\'t see the value yet".','Separate value from money. Get them to say the value in their own words.'),
('"I need to think about it" means not enough trust yet.','Find the hesitation while you are still talking. Never take it literally.'),
('"Next quarter" is rarely about the calendar.','Take the risk off the table: a smaller first step, a clear recommendation and a booked date. Reassurance beats pressure.'),
('Commitment happens in the conversation.','End every exchange with a booked next step and a date, never "let me know".'),
('Be honest about deal health.','Long cycles, repeated proposals and silence after a decision meeting mean "no decision".')]
rows=[('"Let\'s push this to next quarter"','Not a priority yet, or a hidden objection','"If it were next quarter already, what would be different?"'),
('"We don\'t have the budget"','I don\'t see the value yet','"Money aside, is this what you need?"'),
('"I need to think about it"','Not enough trust to say yes','"Totally get it. What\'s the hesitation?"'),
('"Send me a proposal"','Often a polite exit','"Happy to. What does it need to show for you to say yes?"'),
('"I need to run it past my co-founder"','Real sign-off, or a shield','"If it were only your decision, would you do it?"'),
('"We tried someone before"','Fear of paying for nothing','"What happened? What would have had to be different?"'),
('"We\'re looking at another option"','Wants to know why you','"What would make that the better choice for you?"'),
('Silence after a proposal','Something went cold','"Has something changed, or is this one to close off for now?"')]
page(top('The method')+'<h2 class="t">Seven ideas behind every <span class="hl">answer</span></h2>'
 +'<div class="card" style="padding:6px 18px">'+''.join(f'<div class="idea"><span class="big" style="font-size:28px">{i+1}</span><div><b>{esc(a)}</b> <span class="muted">{esc(b)}</span></div></div>' for i,(a,b) in enumerate(ideas))+'</div>'
 +'<h3 class="s" style="margin-top:26px">The eight objections you will hear most</h3>'
 +'<table class="tb"><tr><th style="width:34%">They say</th><th style="width:27%">It usually means</th><th>Ask first</th></tr>'
 +''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a,b,c in rows)+'</table>')
page(top('The prompt')+'''<div class="cont">Copy everything inside the white boxes, pages 4 to 6 (or use the .txt file)</div>
<div class="prompt" style="font-size:11px;line-height:1.42;padding:14px 22px">'''+PROMPT_PAGES[0]+'</div>')
for i,ph in enumerate(PROMPT_PAGES[1:]):
    last=(i==len(PROMPT_PAGES)-2); extra=''
    if last:
        extra='''<div class="cta" style="margin-top:12px;padding:14px 20px"><div><h3>Want a hand with a live deal?</h3><p style="margin:6px 0 0;font-size:12.2px;color:rgba(255,255,255,.82)">Book a free Diagnosis Call and I'll run it through the coach with you.</p><p style="margin:8px 0 0;font-size:9.6px;color:rgba(255,255,255,.6)">A free tool from Revenue &amp; Beyond. Share it with your team, and with any founder it could help.</p></div><span class="btn">revenueandbeyond.com/book</span></div>'''
    page(top('The prompt')+f'<div class="cont">Prompt continued, {i+2} of 3</div><div class="prompt"'+(' style="font-size:11px;line-height:1.45;padding:14px 22px"' if last else '')+f'>{ph}</div>'+extra)
os.makedirs(os.path.join(D,'out'),exist_ok=True)
build(P,TITLE,os.path.join(D,'out/oc.html')); print('pages',len(P))
# plain-text prompt for copy and paste
s=md.index('\nSTART OF PROMPT\n')+1; e=md.index('\nEND OF PROMPT')+1+len('END OF PROMPT')
setup=md[md.index('## Set it up'):md.index('\n---\n\nSTART')]
txt=('OBJECTION COACH  |  A free tool from Revenue & Beyond\n\n'+setup.replace('**','').replace('## ','').replace('paste everything below the line marked START OF PROMPT','paste everything between the two lines further down this file')+'\n\n'+'='*60+'\nCOPY EVERYTHING BETWEEN THE TWO LINES BELOW INTO YOUR PROJECT INSTRUCTIONS\n'+'='*60+'\n\n'
     +md[s+len('START OF PROMPT'):e-len('END OF PROMPT')].strip().lstrip('-').strip()+'\n\n'+'='*60+'\nEND OF PROMPT\n'+'='*60+'\n\nWant help with a live deal? Book a free Diagnosis Call at revenueandbeyond.com/book\n')
open(os.path.join(D,'out/Objection-Coach-Prompt.txt'),'w').write(txt)
