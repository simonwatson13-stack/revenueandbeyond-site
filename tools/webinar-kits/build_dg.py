# -*- coding: utf-8 -*-
# Discovery Call Prep kit: guide PDF (webinar edition, Nov 2026)
import os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from neolib import *
TITLE='Discovery Call Prep kit'
P=[]
def page(b,cls=''): P.append((cls,b))

page(cover('Webinar edition','Discovery<br>Call Prep<span class="dot">.</span>',
 'Walk into every discovery call knowing the company, the founder and their competitors. Then run the call in seven steps and follow up without chasing.',
 [('Research','A Claude skill that preps the prospect in minutes.'),('Run the call','A seven-step discovery flow with lines to use.'),('Follow up','A five-rung ladder that never says "just checking in".')]),'cv')

page(top('Start here')+'''
<h2 class="t">Turn up as the best-prepared <span class="hl">person</span> on the call</h2>
<p class="lead">Most founders do discovery on instinct, and prep for five minutes on the company website. This kit does the homework for you, then gives you a simple way to run the call and follow it up. I use the same approach on my own calls.</p>
<div class="grid c2 mt">
<div class="card g"><span class="lab">In this kit</span><ul class="ul">
<li><b>discovery-call-prep.zip</b>: the Claude skill. Researches the company, founder, competitors, reviews and filings, then writes your brief.</li>
<li><b>This guide</b>: the seven-step call, a before-you-dial checklist and the follow-up ladder.</li></ul></div>
<div class="card p"><span class="lab">What you need</span><ul class="ul">
<li>A Claude account (Pro or above works best for research).</li>
<li>Web search switched on in Claude.</li>
<li>Ten minutes to set it up once with your ideal customer and offer.</li></ul></div></div>
<h3 class="s" style="margin-top:26px">Set up the skill in ten minutes</h3>
<ul class="steps">
<li><span class="n">1</span><b>Add your business.</b> Unzip the file, open <span class="code">my-business.md</span> and replace the examples in [square brackets] with your offer, ideal customer, red flags, results and the problems your best customers have. Zip the <span class="code">discovery-call-prep</span> folder again. (Skip this and Claude asks you the questions on the first run.)</li>
<li><span class="n">2</span><b>Switch on file creation.</b> In Claude, open Settings, then Capabilities, and turn on code execution and file creation. Skills need it.</li>
<li><span class="n">3</span><b>Upload the skill.</b> Go to Customize, then Skills. Click "+", choose to create a skill, then "Upload a skill" and pick the zip.</li>
<li><span class="n">4</span><b>Check it is on.</b> The skill appears in your list as discovery-call-prep. Make sure its toggle is on.</li>
<li><span class="n">5</span><b>Run it.</b> In any chat, paste the line below with your prospect's details.</li>
</ul>
<div class="card s" style="margin-top:6px;padding:13px 18px"><span class="lab">Paste this, then fill it in</span>
<p style="margin:0;font-size:12.6px">Prep me for my discovery call with <span class="fill">company name</span>, <span class="fill">website</span>. I'm meeting <span class="fill">name, role</span> on <span class="fill">date and time</span>. Here's what they told me: <span class="fill">booking form or email</span></p></div>
<div class="grid c2 mt2">
<div class="card"><span class="lab">What comes back</span><ul class="ul small">
<li>A fit read: strong, possible or poor</li><li>Who the founder is, and their current load</li><li>Three competitors, sized, with the real gap</li><li>Your call plan in the seven steps</li><li>Takeaways and a pre-call message, two versions</li></ul></div>
<div class="card tp" style="box-shadow:5px 5px 0 var(--purple)"><span class="lab">No skills on your plan?</span><p class="small" style="margin:0">Create a Claude Project called "Call Prep" and paste the whole of <span class="code">SKILL.md</span> and <span class="code">my-business.md</span> into the project instructions. Same result. This also works in a ChatGPT Project or Custom GPT with web search on.</p></div></div>
''')

steps=[
('Open and set the agenda','Agree time, purpose and the possible outcomes',"We've got 30 minutes. I'd like to understand where things are, share how I've helped businesses like yours, and by the end we'll both know if a next step makes sense. If it doesn't, that's fine too. Fair?"),
('Find the pain','The problem in their words, and what it costs',"What made now the right time to have this conversation? And if nothing changes in the next six months, what does that cost you?"),
('Ask what they have tried','What failed, and why it didn\'t stick',"What have you already tried to fix this? What got in the way?"),
('Tell one relatable story','Relatable beats impressive',"A founder I worked with last year was in almost the same spot. Here's what we changed first, and what happened."),
('Show a light visual','A sketch, not a deck',"Can I draw this? Here's where you are, here's where you want to be, and the three things in between."),
('Pause, then price','Float the range early, then stop talking',"Clients in your position usually invest between X and Y, depending on Z. How does that sit with you?"),
('Book the next step','A date in the diary before you hang up',"Shall we put 30 minutes in for Thursday to go through the proposal together, with your co-founder on the call?"),
]
page(top('The call')+'<h2 class="t">The discovery call in <span class="hl">seven steps</span></h2>'
 +'<p class="lead" style="margin-bottom:16px">Listen for 70% of the call. Your job is to understand the problem better than they do, then show them a way through it. The lines are starting points. Say them your way.</p>'
 +''.join(f'<div class="step"><div class="num">{i+1}</div><div><h4>{esc(a)}<span class="goal">{esc(b)}</span></h4><div class="say">"{esc(c)}"</div></div></div>' for i,(a,b,c) in enumerate(steps)))

page(top('Before and after')+'''
<h2 class="t">Ten minutes <span class="hl">before</span> you dial</h2>
<div class="grid c2">
<div class="card g"><span class="lab">The checklist</span><ul class="ul">
<li>Read the snapshot and fit read in your brief.</li>
<li>Pick one opener: a recent post, launch or hire of theirs.</li>
<li>Choose the one client story that sounds most like them.</li>
<li>Know your price range, out loud, without hesitating.</li>
<li>Send the pre-call message with one "bring this" ask.</li>
<li>Write the follow-up email now. It becomes your script.</li></ul></div>
<div class="card p"><span class="lab">Five things that kill discovery calls</span><ul class="ul">
<li>Pitching in the first ten minutes.</li>
<li>Taking the first problem they mention at face value.</li>
<li>Leaving price until the last two minutes, or the proposal.</li>
<li>A 30-slide deck instead of one simple picture.</li>
<li>Ending with "let me know" instead of a date.</li></ul></div></div>
<h3 class="s" style="margin-top:28px">Score the call straight after</h3>
<p class="muted" style="max-width:600px">Five questions, yes or no. Five yeses means a real opportunity. Three or fewer means you have more discovery to do before you send anything.</p>
<table class="tb" style="margin-top:6px"><tr><th style="width:8%">#</th><th style="width:52%">Did I get...</th><th>Why it matters</th></tr>
<tr><td>1</td><td>The problem in their own words?</td><td>You will quote it back in the proposal.</td></tr>
<tr><td>2</td><td>What it costs them if nothing changes?</td><td>The cost of doing nothing anchors your price.</td></tr>
<tr><td>3</td><td>Who else decides, and how?</td><td>Most stalls come from a decision maker you never met.</td></tr>
<tr><td>4</td><td>A reaction to the price range?</td><td>No surprises at proposal stage.</td></tr>
<tr><td>5</td><td>A next step with a date?</td><td>No date, no deal. Just hope.</td></tr></table>
<div class="cta" style="margin-top:30px"><div><h3>Write the follow-up email first</h3><p style="margin:6px 0 0;font-size:12.2px;color:rgba(255,255,255,.82)">Before the call, draft the recap you want to send afterwards: their problem, what it costs, what you agreed, the next step. Then run the call to fill in the gaps.</p></div><span class="big" style="color:var(--green);text-shadow:2px 2px 0 #062226;font-size:44px">1st</span></div>
''')

rungs=[
('Same day','The recap','Their problem in their words, what you agreed, and the next step with its date. Send within two hours.',"Thanks for today, Sam. You said the real issue is that every deal still needs you on the call. We agreed to walk through a plan on Thursday at 2pm. I'll bring a first draft."),
('Day 2','Add value','Something useful and specific to them: an idea, an introduction or a short example. No new ask.',"Thought of you when I saw this. It's how one founder took himself out of first calls in six weeks. Worth five minutes before Thursday."),
('Day 7','Check the decision','If the step slipped or went quiet, ask a real question about where things are.',"Has anything changed since we spoke, or is fixing the founder bottleneck still a priority for this quarter?"),
('Day 14','Make it easy','Offer a smaller first step or bring new proof. Try a different channel: phone or LinkedIn.',"If a full plan feels like a lot right now, we could start with a two-week sprint on your first-call process only."),
('Day 21','Clean takeaway','Close it off politely. This often restarts the deal.',"I'll take this off the table for now so you're not being chased. If it comes back up, I'm a message away."),
]
page(top('Follow-up')+'<h2 class="t">The follow-up <span class="hl">ladder</span></h2>'
 +'<p class="lead" style="margin-bottom:16px">Every follow-up needs a reason to exist. If you can\'t say what is new or useful in it, don\'t send it. Never send "just checking in".</p>'
 +'<div class="ladder">'+''.join(f'<div class="rung"><span class="when">{esc(w)}</span><b class="h">{esc(t)}.</b> <span class="small">{esc(d)}</span><div class="msg">"{esc(m)}"</div></div>' for w,t,d,m in rungs)+'</div>'
 +'''<div class="grid c2" style="margin-top:6px;gap:16px"><div class="card s" style="padding:12px 16px"><span class="lab">After the ladder</span><p class="small" style="margin:0">Move them to a light nurture: something genuinely useful every six to eight weeks, no pitch. Plenty of deals close on the second time around.</p></div>
<div class="cta" style="padding:12px 16px;box-shadow:5px 5px 0 var(--purple)"><div><b style="font-size:14px">Want a second pair of eyes on a live deal?</b><p style="margin:4px 0 0;font-size:10.4px;color:rgba(255,255,255,.75)">Book a free Diagnosis Call at revenueandbeyond.com/book</p></div></div></div>''')

os.makedirs(os.path.join(D,'out'),exist_ok=True)
build(P,TITLE,os.path.join(D,'out/dg.html')); print('pages',len(P))
