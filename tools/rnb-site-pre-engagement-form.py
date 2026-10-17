#!/usr/bin/env python3
"""Revenue & Beyond: adds the online Pre-Engagement Pack to a built site folder.

Usage: python3 rnb-site-pre-engagement-form.py <site_folder>
Reads <site_folder>/book/index.html as the page shell (head, header, footer),
writes <site_folder>/<SLUG>/index.html and .../thanks/index.html.
       python3 rnb-site-pre-engagement-form.py <site_folder> --preview out.html  (standalone preview)
Submissions go to Netlify Forms (form name "pre-engagement"). The page is noindex
and is not added to the sitemap or nav: it is sent to clients by link.
"""
import html, re, sys, os

SITE = sys.argv[1]
FORM = "pre-engagement"
# Private URL: unlisted and hard to guess. Change SLUG to rotate the link (old link then 404s).
SLUG = "pack-2woipwnn5y"
PREVIEW = "--preview" in sys.argv  # standalone file for a clickable preview: inline CSS, submit simulated
E = html.escape

# ---------------------------------------------------------------- content
# Each section: (title, intro, optional, items)
# item types:
#   ("pair", [(key, label, hint, input_type, required, autocomplete), ...])
#   ("q", key, label, hint, rows)
#   ("ideal", rows[(key,label,hint)])
#   ("team", n)
#   ("matrix", key_prefix, question, hint, first_col, status_label, status_opts, extra_select, notes_label, rows)
S = []
S.append(("The basics", "Let's start simple. A few facts to orient everything that follows.", False, [
    ("pair", [("01 Company name", "Company name", "e.g. Acme Ltd", "text", True, "organization"),
              ("01 Your name and title", "Your name and title", "e.g. Jane Smith, Founder and CEO", "text", True, "name")]),
    ("pair", [("01 Website", "Website", "e.g. acme.co.uk", "text", False, "url"),
              ("email", "Best email to reach you", "So I can reply to you", "email", True, "email")]),
    ("q", "01 What you do", "How long have you been in business, and what do you do in one sentence?", "The version you'd say at a dinner party, not a pitch.", 2),
]))
S.append(("Your revenue today", "Where revenue actually comes from, and how it is generated, is the starting point for everything.", False, [
    ("pair", [("02 Annual revenue", "Approximate annual revenue", "e.g. £2.4m", "text", False, "off"),
              ("02 Revenue target 12 months", "Revenue you are targeting in 12 months", "e.g. £5m", "text", False, "off")]),
    ("pair", [("02 Annual profit EBITDA", "Approximate annual profit (EBITDA)", "e.g. £300k, or a margin such as 12%", "text", False, "off"),
              ("02 Profit target 12 months", "Profit you are targeting in 12 months", "A rough figure is fine", "text", False, "off")]),
    ("q", "02 Revenue sources", "Where does the majority of your revenue come from today?", "Existing clients, referrals, outbound, inbound, events, partnerships. Be specific about the split if you can.", 4),
    ("q", "02 Founder dependency", "How dependent is your revenue on you personally?", "Roughly what % would be at risk if you stepped back for three months? And why?", 4),
    ("q", "02 Sales process", "What is your current sales process? How does a new client typically come in?", "Walk me through it: first contact → conversation → proposal → close. Even if it is informal, describe what actually happens.", 5),
    ("q", "02 Sales team", "Do you have a sales team or anyone helping you sell? If so, how is that working?", "Headcount, roles, and your honest view of what is working and what is not.", 4),
    ("q", "02 Commercials", "What does a typical engagement look like commercially?", "Approximate contract value, how you charge (project, retainer or day rate) and how long it usually takes from first conversation to signed. A range is fine. This is not an audit.", 4),
]))
S.append(("The problem you need to solve", "Often the most important section. The more specific you are, the more useful the work will be.", False, [
    ("q", "03 Core challenge", "What's the core revenue challenge you're facing right now?", "Not the polished version. What are you actually worried about?", 5),
    ("q", "03 Already tried", "What have you already tried? What happened?", "Sales hires, agencies, processes, tools. What did you invest in, and what was the result?", 4),
    ("q", "03 Why not solved", "Why hasn't this been solved yet?", "Time, expertise, bandwidth, the wrong people, the wrong approach? Usually it's a combination.", 4),
    ("q", "03 What it would mean", "What would it mean for you personally if this was solved in the next 12 months?", "Think beyond the revenue number. What changes for you as the founder?", 4),
]))
S.append(("Your ideal client", "Who you are really for, and who you are not for. If you work with different types of client, focus on the one you want more of.", False, [
    ("ideal", [("04 ICP industry", "Industry or sector", "e.g. technology, marketing services, recruitment"),
               ("04 ICP company size", "Company size (employees)", "e.g. 20 to 150"),
               ("04 ICP revenue range", "Revenue range", "e.g. £3m to £20m"),
               ("04 ICP geography", "Geography", "e.g. UK, EMEA, global"),
               ("04 ICP decision maker", "Decision maker", "e.g. CEO, founder, CRO, MD"),
               ("04 ICP budget", "Typical budget for your services", "e.g. £2k to £10k a month")]),
    ("q", "04 Best-fit clients", "Name two or three existing clients who represent this ideal. What made them a great fit?", "Think about the results you got, how enjoyable they were to work with and whether they put in the work.", 4),
    ("q", "04 Client goals", "What are your ideal clients trying to achieve? What does success look like for them?", "Business goals and personal motivations. What are they actually trying to accomplish?", 4),
    ("q", "04 Client pain", "What pain are they in when they come to you? What do they want to escape?", "The more specific the better. Use the language they would use themselves, not a category.", 4),
    ("q", "04 Buying trigger", "What triggers the decision to hire someone like you? What had to happen first?", "e.g. a hire fell through, an exit date was set, the pipeline went quiet, a sales team failed to deliver.", 4),
]))
S.append(("Your positioning and differentiation", "This creates contrast. It forces clarity on what makes you different, and why that matters.", False, [
    ("q", "05 Why you over alternatives", "Why should someone choose you over the obvious alternatives: a big agency, an in-house hire, a generalist consultant?", "What can you do that they simply can't?", 4),
    ("q", "05 Why you answer", "When a prospect asks \"why you?\", what do you actually say?", "Write the answer you give in real conversations, not the polished positioning statement.", 4),
    ("q", "05 Lost deals", "Who do you lose deals to, and why?", "The agency, the in-house hire, the \"we'll do it ourselves\" decision. What did they choose, what reason did they give, and what do you suspect the real one was?", 4),
    ("q", "05 One thing to land", "What's the one thing you want people to understand about you immediately?", "If someone spent ten seconds on your website or LinkedIn, what would you want to land?", 3),
]))
S.append(("Your story and credibility", "What you have lived through, and how much proof you already have.", False, [
    ("q", "06 Origin", "Where did this business come from? What was the spark, or the moment that made it inevitable?", "The origin: a client conversation, a frustration, a gap you kept seeing.", 4),
    ("q", "06 Pivotal moment", "What's the pivotal moment in your career that shaped how you think about this work?", "The project, client, win or failure that changed your approach.", 4),
    ("q", "06 Credibility", "Which past roles or results give you the most credibility in the market?", "Specific companies, outcomes and numbers. The things you'd put in a case study.", 4),
    ("q", "06 Network", "Who in your existing network could open doors right now if you reached out?", "Former clients, colleagues, investors, partners. People who already know what you are capable of.", 4),
    ("q", "06 Referrals", "How do referrals actually arrive? Walk me through it.", "Is it one or two people who send most of them? A loose network? Former colleagues or clients? And when a referral comes in, what reason do they give for passing your name on?", 4),
]))
S.append(("Where you're headed", "The ambition, and making sure the work is aimed at the right target.", False, [
    ("q", "07 12 to 24 months", "What does the business look like in 12 to 24 months if everything goes right?", "Revenue, profit, team, clients, your own role. Be specific and ambitious.", 4),
    ("q", "07 Urgency", "Is there a specific event or milestone driving urgency?", "An exit, an investment round, a key hire, a market window. Even if it is informal, name the deadline that makes now important.", 3),
    ("q", "07 Flying start", "What would a flying start look like in the first 30 to 60 days of working together?", "Conversations had, proposals out, clients won, processes in place. Make it concrete.", 4),
    ("q", "07 Headline", "If everything went right, what headline would you love to read about your company in two years?", "Dream out loud. This one is meant to be ambitious.", 2),
]))
S.append(("You, the founder", "Optional, but valuable. A revenue engine built around an exhausted founder does not last. This section helps me design something you'll actually want to run. Answer as much or as little as you like.", True, [
    ("q", "08 Energy and drains", "What parts of your week give you energy, and what drains you?", "Be specific: the meetings, tasks, clients or conversations that lift you, and the ones you dread.", 4),
    ("q", "08 Sustainable pace", "On a scale of 1 to 10, how sustainable is your current pace?", "1 is running on fumes, 10 is could happily do this for years. What's behind the number?", 2),
    ("q", "08 Hours", "Roughly how many hours a week are you working, and how many would you like to be working?", "A rough guess is fine. Include evenings and weekends if they are part of the reality.", 2),
    ("q", "08 Stop doing", "If you could stop doing one thing in the business tomorrow, what would it be?", "The task, role or responsibility you'd hand over first if you could.", 3),
    ("q", "08 Good week", "What does a genuinely good week look like for you?", "Not the most productive week. The one you'd happily repeat.", 3),
    ("q", "08 Enough", "What does 'enough' look like, for the business and for you personally?", "Revenue, lifestyle, time, freedom, an exit. Some founders have a clear number, others have never thought about it. Both are useful to know.", 3),
    ("q", "08 Role in two years", "What role do you want to be playing in the business in two years?", "Chief seller, CEO, chair, product lead, investor, or gone entirely. There's no wrong answer, but it shapes everything I build with you.", 3),
    ("q", "08 Support", "Who do you lean on when things get hard?", "A co-founder, board, chair, peer group, coach or mentor, or nobody yet.", 2),
    ("q", "08 Design around", "Is there anything about how you work that I should design around?", "Family commitments, working patterns, time zones, how you prefer to communicate, the days you protect.", 3),
]))
S.append(("Marketing and sales resource", "Who you have behind you matters as much as what you are trying to do. This shows me the resource reality before I suggest what is possible.", False, [
    ("q", "09 Marketing tried", "What marketing activities have you tried? What worked, what didn't, and why do you think that is?", "e.g. LinkedIn content, paid ads, SEO, events, cold outreach, email campaigns, PR, partnerships. Be specific about what you invested in and what happened.", 5),
    ("q", "09 Willing to do", "Looking ahead, what are you actually willing to do?", "Some founders will write LinkedIn posts, pick up the phone to cold prospects and speak at events. Others won't, and that's fine, but it changes the approach. Be honest about where your energy and appetite sit.", 4),
    ("q", "09 Budget", "What is your current marketing and sales budget, annual or monthly?", "Include tools, freelancers, agencies, paid media and events. A range is fine.", 2),
    ("team", 4),
    ("q", "09 Design capability", "Do you have a designer, brand system or tool that can produce sales documents and decks? How does that work in practice?", "e.g. an in-house designer, a freelancer on retainer, Canva or Figma templates, a branded PowerPoint deck, nothing formal.", 3),
    ("q", "09 Tools", "What tools and technology do you use for sales and marketing?", "CRM, outreach, email, analytics, automation. e.g. HubSpot, Salesforce, Pipedrive, Apollo, LinkedIn Sales Navigator, Mailchimp, or nothing formal. Include how actively each one is used.", 4),
]))
S.append(("AI and automation", "Where AI is already working in your business, where it isn't, and how far you want to go. There's no right level of adoption. This tells me what there is to build on.", False, [
    ("matrix", "10 AI", "Where are you using AI in sales and marketing today?", "Pick a status for each area, and say which tool you use and what it does.",
     "Status", ["None", "Testing", "Embedded"], None, "Tool used and what it's doing",
     ["Prospect and account research", "Lead lists and data enrichment", "Outreach and email drafting",
      "Content (LinkedIn, blog, newsletter)", "Proposals, decks and sales documents", "Call recording, notes and follow-ups",
      "CRM updates and admin", "Forecasting and reporting", "Client service and account management"]),
    ("q", "10 Personal AI use", "How do you personally use AI?", "Daily, occasionally or never. What for: thinking, writing, research, admin? Which tools?", 3),
    ("q", "10 Team AI use", "Who in the business uses AI day to day, and is it officially supported?", "A company-wide tool and approach, a few enthusiasts, or people using it quietly on their own accounts?", 3),
    ("q", "10 AI wins and misses", "Where has AI genuinely saved time or made money, and where has it disappointed?", "Specific examples beat general impressions. 'It writes the first draft of every proposal' is useful. 'We use ChatGPT' less so.", 4),
    ("q", "10 AI constraints", "Are there any constraints on how you can use AI?", "Client confidentiality, regulated data, contractual terms, a sceptical co-founder or board, an existing IT or security policy.", 3),
    ("q", "10 CRM data quality", "How clean and complete is your CRM and customer data?", "AI is only as good as the data it works from. Rate it 1 to 5, and tell me what's missing, out of date or lives in someone's head.", 3),
    ("q", "10 AI ambition", "How far would you like to go?", "From 'help my team work faster' to 'automate whole processes or replace roles'. Be honest about your appetite and any concerns.", 3),
    ("q", "10 Market AI pressure", "Are your clients or competitors talking about AI, and is it changing what they expect from you?", "Pricing pressure, faster turnaround, new AI-native competitors, or clients asking how you use it.", 3),
]))
S.append(("Marketing and sales collateral", "What you have, what you're using and what you know is missing. This tells me where the starting point is and what needs to be built.", False, [
    ("matrix", "11 Asset", "What marketing and sales collateral do you currently have? Rate it honestly.", "Quality: 1 is poor, 5 is excellent.",
     "Have it?", ["Yes", "Partly", "No"], ("Quality", ["1", "2", "3", "4", "5"]), "Notes: what's wrong with it",
     ["Website", "LinkedIn profile or company page", "Pitch deck or credentials deck", "Proposal template",
      "Case studies or client results", "One-pagers or service overview", "Email outreach sequences",
      "Sales scripts or call frameworks", "Video or demo content", "Thought leadership (blog, newsletter, social)"]),
    ("q", "11 What's missing", "What do you think is missing? What would make the biggest difference to your ability to win new business?", "Think about the assets or processes that, if they existed and were good, would give you confidence going into sales conversations.", 5),
]))
S.append(("Anything else", "The thing that didn't fit anywhere above, but you want me to know before the call.", False, [
    ("q", "12 Previous support", "Have you invested in sales or marketing support before? What happened?", "Agencies, consultants, BDR hires, tools. What did you try, what did it cost and what was the result? If it didn't work, what do you think went wrong?", 4),
    ("q", "12 Hesitations", "Is there anything making you hesitant, or anything I should know before I start?", "A bad experience, a sceptical co-founder, a constraint I haven't asked about. Better to surface it now than discover it in month two.", 4),
]))

# ---------------------------------------------------------------- render
fid = 0
def nid():
    global fid; fid += 1; return f"f{fid}"

def textarea(key, label, hint, rows):
    i = nid()
    return (f'<div class="pe-q"><label for="{i}">{E(label)}</label>'
            f'<p class="pe-hint" id="{i}h">{E(hint)}</p>'
            f'<textarea id="{i}" name="{E(key)}" rows="{rows}" aria-describedby="{i}h"></textarea></div>')

def field(key, label, hint, typ, req, ac):
    i = nid()
    star = ' <span class="pe-req" aria-hidden="true">*</span>' if req else ''
    return (f'<div class="pe-q"><label for="{i}">{E(label)}{star}</label>'
            f'<p class="pe-hint" id="{i}h">{E(hint)}</p>'
            f'<input id="{i}" type="{typ}" name="{E(key)}" autocomplete="{ac}" aria-describedby="{i}h"{" required" if req else ""}></div>')

def select(name, opts, label):
    return (f'<select name="{E(name)}" aria-label="{E(label)}"><option value="">{E(label.split(": ")[-1])}</option>'
            + "".join(f'<option>{E(o)}</option>' for o in opts) + '</select>')

def render_item(it):
    t = it[0]
    if t == "q":
        return textarea(*it[1:])
    if t == "pair":
        return '<div class="pe-pair">' + "".join(field(*f) for f in it[1]) + '</div>'
    if t == "ideal":
        rows = "".join(
            f'<div class="pe-row"><label for="{(i:=nid())}"><b>{E(l)}</b><span>{E(h)}</span></label>'
            f'<input id="{i}" type="text" name="{E(k)}"></div>' for k, l, h in it[1])
        return f'<div class="pe-q"><p class="pe-label">Describe your ideal client. Who are they?</p><div class="pe-table">{rows}</div></div>'
    if t == "team":
        rows = ""
        for n in range(1, it[1] + 1):
            rows += (f'<div class="pe-person"><span class="pe-num">{n}</span>'
                     f'<input type="text" name="09 Team {n} role or name" placeholder="Role or name" aria-label="Person {n}: role or name">'
                     + select(f"09 Team {n} capacity", ["Full-time", "Part-time", "Freelance", "VA", "Offshore"], f"Person {n}: capacity") +
                     f'<input type="text" name="09 Team {n} what they do" placeholder="What they do and how it\'s working" aria-label="Person {n}: what they do and how it is working"></div>')
        return ('<div class="pe-q"><p class="pe-label">Who do you currently have supporting marketing and sales?</p>'
                '<p class="pe-hint">Describe each person\'s role and how they work with you. Leave rows blank if you don\'t need them.</p>'
                f'<div class="pe-people">{rows}</div></div>')
    if t == "matrix":
        _, pre, q, hint, sl, sopts, extra, notes, rows = it
        out = ""
        for r in rows:
            sel = select(f"{pre} {r} {sl.rstrip('?').lower()}", sopts, f"{r}: {sl}")
            if extra:
                sel += select(f"{pre} {r} {extra[0].lower()}", extra[1], f"{r}: {extra[0]}")
            out += (f'<div class="pe-mx"><b>{E(r)}</b><div class="pe-mx-c">{sel}'
                    f'<input type="text" name="{E(pre + " " + r + " notes")}" placeholder="{E(notes)}" aria-label="{E(r)}: {E(notes)}"></div></div>')
        return (f'<div class="pe-q"><p class="pe-label">{E(q)}</p><p class="pe-hint">{E(hint)}</p>'
                f'<div class="pe-matrix">{out}</div></div>')
    raise ValueError(t)

accents = ["var(--green)", "var(--purple)", "var(--sky)"]
steps = []
for n, (title, intro, opt, items) in enumerate(S, 1):
    num = f"{n:02d}"
    tag = '<span class="pe-opt">Optional</span>' if opt else ''
    body = "".join(render_item(it) for it in items)
    steps.append(
        f'<fieldset class="pe-step" data-step="{n}" id="s{num}" style="--acc:{accents[(n-1)%3]}">'
        f'<legend class="pe-legend"><span class="pe-n">{num}</span><span class="pe-t">{E(title)}</span>{tag}</legend>'
        f'<p class="pe-intro">{E(intro)}</p>{body}</fieldset>')

chips = "".join(f'<button type="button" class="pe-chip" data-go="{n}" aria-label="Section {n}: {E(t)}">{n:02d}</button>'
                for n, (t, *_rest) in enumerate(S, 1))
TOTAL = len(S)

FORM_HTML = f'''
<section class="hero pe-hero">
  <div class="col-wide">
    <p class="eyebrow" style="justify-content:center">Pre-engagement pack</p>
    <h1>A conversation <span class="hl">on paper</span>.</h1>
    <p class="lead">Before I start work with you, this helps me understand your business, your story and the problem you want solved. There are no right or wrong answers. Honest ones are more useful than polished ones.</p>
    <p class="bk-tags"><span class="tg">45 to 60 minutes</span><span class="tg hand">Saves as you go</span><span class="tg">Section 08 is optional</span></p>
  </div>
</section>

<section class="pe-wrap" aria-label="Pre-engagement pack">
  <div class="col-wide">
    <div class="pe-card">
      <div class="pe-top" aria-live="polite">
        <div class="pe-prog-row"><strong id="peWhere">Section 1 of {TOTAL}</strong><span id="peSaved" class="pe-saved">Your answers save in this browser as you type. Use Save my progress to send Simon what you have so far</span></div>
        <div class="pe-bar" aria-hidden="true"><span id="peBar"></span></div>
        <nav class="pe-chips" aria-label="Jump to a section">{chips}</nav>
      </div>
      <noscript><p class="pe-ns">All sections are shown below. Fill in what you can and press Send at the bottom.</p></noscript>
      <form name="{FORM}" id="peForm" method="POST" action="/{SLUG}/thanks/" data-netlify="true" netlify-honeypot="bot-field" accept-charset="UTF-8">
        <input type="hidden" name="form-name" value="{FORM}">
        <input type="hidden" name="subject" id="peSubject" value="Pre-engagement pack">
        <input type="hidden" name="Status" id="peStatus" value="Complete">
        <p class="pe-hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <div class="pe-body">{"".join(steps)}</div>
        <div class="pe-foot">
          <button type="button" class="btn btn-ghost btn-sm" id="peBack">Back</button>
          <p class="pe-err" id="peErr" role="alert" hidden></p>
          <p class="pe-ok" id="peOk" role="status" hidden></p>
          <div class="pe-actions">
            <button type="button" class="btn btn-ghost btn-sm" id="pePause">Save my progress</button>
            <button type="button" class="btn btn-sm" id="peNext">Next section</button>
            <button type="submit" class="btn btn-sm" id="peSend">Send it to Simon</button>
          </div>
        </div>
      </form>
      <div class="pe-done" id="peDone" hidden tabindex="-1">
        <p class="eyebrow">All done</p>
        <h2>Thank you for the <span class="mk">honesty</span>.</h2>
        <p>Your answers are with me. I will read every one before the call, so the time together goes on your business, not on background.</p>
        <p class="small">A copy is not emailed to you, so if you want one, use the button below before you close this page.</p>
        <p><button type="button" class="btn btn-ghost btn-sm" id="peCopy">Download a copy of my answers</button></p>
      </div>
    </div>
    <p class="small pe-privacy">Your answers come straight to me and are not shared. See the <a class="link" href="/privacy-policy.html">privacy policy</a>. Questions? Email <a class="link" href="mailto:simon@revenueandbeyond.com">simon@revenueandbeyond.com</a>.</p>
  </div>
</section>
'''

CSS = '''<script>document.documentElement.classList.add('js')</script>
<style>
.pe-hero{padding-bottom:40px}
.pe-hero .lead{margin-bottom:26px}
.pe-wrap{padding:8px 0 96px}
.pe-card{background:#fff;border:2px solid var(--teal);border-radius:24px;box-shadow:8px 8px 0 var(--purple)}
.pe-top{position:sticky;top:75px;z-index:5;background:var(--offwhite);border-bottom:2px solid var(--teal);border-radius:22px 22px 0 0;padding:16px 24px 14px}
.pe-prog-row{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline;font-size:14px}
.pe-prog-row strong{color:var(--teal);font-weight:800}
.pe-saved{font-size:12.5px;color:var(--muted)}
.pe-bar{height:8px;border:2px solid var(--teal);border-radius:99px;background:#fff;margin:10px 0 12px;overflow:hidden}
.pe-bar span{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--green),var(--purple),var(--sky));transition:width .25s}
.pe-chips{display:flex;gap:6px;flex-wrap:wrap}
.pe-chip{font:inherit;font-size:12px;font-weight:800;color:var(--teal);background:#fff;border:2px solid var(--teal);border-radius:8px;padding:3px 8px;cursor:pointer;min-width:38px}
.pe-chip.done{background:rgba(73,232,176,.35)}
.pe-chip[aria-current="step"]{background:var(--teal);color:#fff}
.pe-body{padding:28px 32px 8px}
.pe-step{border:0;margin:0;padding:0;min-width:0}
.js .pe-step{display:none}.js .pe-step.on{display:block}
.pe-legend{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:0;margin:0 0 12px;font-weight:900;color:var(--teal);letter-spacing:var(--track);font-size:clamp(1.5rem,3vw,2rem);line-height:1.1}
.pe-n{display:inline-flex;align-items:center;justify-content:center;min-width:52px;height:46px;padding:0 8px;background:var(--acc);border:2px solid var(--teal);border-radius:12px;box-shadow:3px 3px 0 var(--teal);font-size:1.15rem;transform:rotate(-2deg)}
.pe-opt{font-size:11px;letter-spacing:.14em;text-transform:uppercase;background:var(--purple);border:2px solid var(--teal);border-radius:8px;padding:3px 10px}
.pe-intro{color:var(--muted);margin:0 0 8px;max-width:40em}
.pe-q{margin:26px 0 0}
.pe-q label,.pe-label{display:block;font-weight:800;color:var(--black);font-size:16px;line-height:1.4;margin:0 0 4px}
.pe-req{color:var(--teal)}
.pe-hint{font-size:14px;color:var(--muted);margin:0 0 10px;line-height:1.5}
.pe-card input[type=text],.pe-card input[type=email],.pe-card textarea,.pe-card select{width:100%;font:inherit;font-size:16px;color:var(--black);background:#fff;border:2px solid var(--teal);border-radius:14px;padding:12px 14px;box-shadow:4px 4px 0 var(--teal);transition:box-shadow .12s,transform .12s}
.pe-card textarea{resize:vertical;min-height:84px;line-height:1.55;overflow:hidden}
.pe-card input:focus,.pe-card textarea:focus,.pe-card select:focus{outline:none;box-shadow:4px 4px 0 var(--green);border-color:var(--teal)}
.pe-card .bad{box-shadow:4px 4px 0 #d64545}
.pe-pair{display:grid;grid-template-columns:1fr 1fr;gap:0 24px}
.pe-table{border:2px solid var(--teal);border-radius:14px;overflow:hidden;box-shadow:4px 4px 0 var(--teal)}
.pe-row{display:grid;grid-template-columns:240px 1fr;border-top:1.5px solid var(--teal)}
.pe-row:first-child{border-top:0}
.pe-row label{margin:0;padding:10px 14px;background:var(--offwhite);border-right:1.5px solid var(--teal);font-weight:400}
.pe-row label b{display:block;font-size:14.5px}.pe-row label span{display:block;font-size:12.5px;color:var(--muted);line-height:1.4}
.pe-card .pe-row input{border:0;border-radius:0;box-shadow:none}
.pe-card .pe-row input:focus{box-shadow:inset 0 0 0 3px var(--green)}
.pe-people{display:grid;gap:12px}
.pe-person{display:grid;grid-template-columns:28px 1fr 150px 1.6fr;gap:10px;align-items:center}
.pe-num{font-family:'Caveat Brush',cursive;font-size:26px;color:var(--teal);text-align:center}
.pe-matrix{display:grid;gap:10px}
.pe-mx{display:grid;grid-template-columns:230px 1fr;gap:12px;align-items:center;padding:10px 0;border-top:1px solid var(--divider)}
.pe-mx:first-child{border-top:0}
.pe-mx b{font-size:14.5px;line-height:1.35}
.pe-mx-c{display:flex;gap:10px}
.pe-mx-c select{width:auto;min-width:118px;flex:0 0 auto}
.pe-mx-c input{flex:1}
.pe-card select{padding:11px 34px 11px 12px;appearance:none;-webkit-appearance:none;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%230B363B' stroke-width='2.2'/%3E%3C/svg%3E") no-repeat right 12px center}
.pe-foot{display:flex;align-items:center;gap:14px;justify-content:space-between;padding:22px 32px 28px;margin-top:28px;border-top:2px solid var(--teal);background:var(--offwhite);border-radius:0 0 22px 22px}
.pe-err,.pe-ok{margin:0;flex:1;text-align:center;font-size:14px;font-weight:700;color:#b02a2a;line-height:1.45}
.pe-ok{color:var(--teal)}
.pe-actions{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end}
html:not(.js) #pePause{display:none}
.js #peSend{display:none}.js.pe-last #peSend{display:inline-flex}.js.pe-last #peNext{display:none}
.js.pe-first #peBack{visibility:hidden}
html:not(.js) #peNext,html:not(.js) #peBack,html:not(.js) .pe-chips,html:not(.js) .pe-bar{display:none}
html:not(.js) .pe-step+.pe-step{margin-top:56px;padding-top:40px;border-top:2px solid var(--divider)}
.pe-hp{position:absolute;left:-9999px}
.pe-done{padding:56px 32px;text-align:center}
.pe-done h2{margin:6px 0 16px}.pe-done p{max-width:34em;margin-left:auto;margin-right:auto}
.pe-privacy{text-align:center;margin-top:22px}
.pe-ns{padding:16px 32px 0;margin:0;font-weight:700}

@media (max-width:700px){
  .pe-body{padding:22px 18px 4px}.pe-top{padding:12px 16px}.pe-foot{padding:18px;flex-wrap:wrap}
  .pe-pair{grid-template-columns:1fr}
  .pe-row{grid-template-columns:1fr}.pe-row label{border-right:0;border-bottom:1.5px solid var(--teal)}
  .pe-person{grid-template-columns:24px 1fr;}.pe-person select,.pe-person input:last-child{grid-column:2}
  .pe-mx{grid-template-columns:1fr;gap:8px}.pe-mx-c{flex-wrap:wrap}.pe-mx-c input{flex-basis:100%}
  .pe-err,.pe-ok{order:-1;flex-basis:100%}.pe-actions{flex:1;justify-content:flex-end}
  .pe-card{box-shadow:5px 5px 0 var(--purple)}
}
</style>
'''

JS = '''
<script>
(function(){
  var root=document.documentElement; root.classList.add('js');
  var form=document.getElementById('peForm'); if(!form) return;
  var steps=[].slice.call(form.querySelectorAll('.pe-step')), N=steps.length, cur=0;
  var chips=[].slice.call(document.querySelectorAll('.pe-chip'));
  var bar=document.getElementById('peBar'), where=document.getElementById('peWhere'), saved=document.getElementById('peSaved');
  var err=document.getElementById('peErr'), KEY='rb_pe_pack_v1', top=document.querySelector('.pe-wrap');
  function fields(){return [].slice.call(form.querySelectorAll('input[name],textarea[name],select[name]')).filter(function(f){return f.type!=='hidden'&&f.name!=='bot-field';});}
  function grow(t){t.style.height='auto';t.style.height=(t.scrollHeight+4)+'px';}
  // restore
  var data={}; try{data=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){data={};}
  fields().forEach(function(f){ if(data[f.name]!=null) f.value=data[f.name]; });
  var t; function save(){clearTimeout(t);t=setTimeout(function(){
    var d={}; fields().forEach(function(f){ if(f.value) d[f.name]=f.value; });
    d.__step=cur; try{localStorage.setItem(KEY,JSON.stringify(d)); saved.textContent='Saved in this browser '+new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});}catch(e){saved.textContent='Autosave is off in this browser, so finish in one go';}
    marks();},400);}
  form.addEventListener('input',function(e){ if(e.target.tagName==='TEXTAREA') grow(e.target); e.target.classList.remove('bad'); save(); });
  form.addEventListener('change',save);
  function marks(){ chips.forEach(function(c,i){ var any=[].slice.call(steps[i].querySelectorAll('input[name],textarea[name],select[name]')).some(function(f){return f.value;}); c.classList.toggle('done',any); }); }
  function valid(i){
    var bad=[].slice.call(steps[i].querySelectorAll('[required]')).filter(function(f){return !f.value.trim()||(f.type==='email'&&!/^\\S+@\\S+\\.\\S+$/.test(f.value));});
    bad.forEach(function(f){f.classList.add('bad');});
    if(bad.length){err.textContent='Please add your name, company and email so I know who this is from.';err.hidden=false;bad[0].focus();return false;}
    err.hidden=true;return true;
  }
  function show(i,focus){
    if(i>0&&cur===0&&!valid(0)) return;
    cur=Math.max(0,Math.min(N-1,i));
    steps.forEach(function(s,k){s.classList.toggle('on',k===cur);});
    chips.forEach(function(c,k){ if(k===cur) c.setAttribute('aria-current','step'); else c.removeAttribute('aria-current'); });
    root.classList.toggle('pe-first',cur===0); root.classList.toggle('pe-last',cur===N-1);
    where.textContent='Section '+(cur+1)+' of '+N; bar.style.width=Math.round((cur+1)/N*100)+'%';
    steps[cur].querySelectorAll('textarea').forEach(grow);
    if(focus){ var y=top.getBoundingClientRect().top+window.scrollY-80; window.scrollTo({top:y,behavior:'smooth'}); var l=steps[cur].querySelector('legend'); if(l){l.setAttribute('tabindex','-1');l.focus({preventScroll:true});} }
    save();
  }
  document.getElementById('peNext').addEventListener('click',function(){ok.hidden=true;show(cur+1,true);});
  document.getElementById('peBack').addEventListener('click',function(){show(cur-1,true);});
  chips.forEach(function(c,k){c.addEventListener('click',function(){show(k,true);});});
  var start=parseInt(data.__step,10); show(isNaN(start)?0:start,false); marks();
  function encode(){ var p=[]; new FormData(form).forEach(function(v,k){p.push(encodeURIComponent(k)+'='+encodeURIComponent(v));}); return p.join('&'); }
  function asText(){ var out='Revenue & Beyond pre-engagement pack\\n\\n'; fields().forEach(function(f){ if(f.value) out+=f.name+'\\n'+f.value+'\\n\\n'; }); return out; }
  var lastText='';
  var ok=document.getElementById('peOk');
  function setSubject(kind){ var co=(form.querySelector('[name="01 Company name"]')||{}).value||'';
    document.getElementById('peStatus').value=kind==='pause'?'In progress (saved at section '+(cur+1)+' of '+N+')':'Complete';
    document.getElementById('peSubject').value=(kind==='pause'?'Pre-engagement pack IN PROGRESS: ':'Pre-engagement pack: ')+co; }
  document.getElementById('pePause').addEventListener('click',function(){
    ok.hidden=true;
    if(!valid(0)){show(0,true);return;}
    var b=this; b.disabled=true; b.textContent='Saving...'; setSubject('pause');
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:encode()})
      .then(function(r){ if(!r.ok) throw new Error(r.status);
        b.disabled=false; b.textContent='Save my progress'; err.hidden=true;
        ok.textContent='Saved. Simon has your answers so far. Come back to this page any time to carry on.'; ok.hidden=false; save(); })
      .catch(function(){ b.disabled=false; b.textContent='Save my progress';
        err.textContent='That did not save to Simon. Your answers are still saved in this browser. Try again in a moment.'; err.hidden=false; });
  });
  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(!valid(0)){show(0,true);return;}
    setSubject('final'); ok.hidden=true;
    var b=document.getElementById('peSend'); b.disabled=true; b.textContent='Sending...';
    lastText=asText();
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:encode()})
      .then(function(r){ if(!r.ok) throw new Error(r.status);
        try{localStorage.removeItem(KEY);}catch(x){}
        form.hidden=true; document.querySelector('.pe-top').hidden=true;
        var d=document.getElementById('peDone'); d.hidden=false; d.focus(); window.scrollTo({top:top.getBoundingClientRect().top+window.scrollY-80,behavior:'smooth'}); })
      .catch(function(){ b.disabled=false; b.textContent='Send it to Simon';
        err.textContent='That did not send. Your answers are still saved here. Try again, or email simon@revenueandbeyond.com.'; err.hidden=false; });
  });
  document.getElementById('peCopy').addEventListener('click',function(){
    try{var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lastText],{type:'text/plain'}));a.download='my-pre-engagement-answers.txt';document.body.appendChild(a);a.click();a.remove();}catch(x){}
  });
})();
</script>
'''

THANKS_MAIN = '''
<section class="hero">
  <div class="col-wide">
    <p class="eyebrow" style="justify-content:center">All done</p>
    <h1>Thank you for the <span class="hl">honesty</span>.</h1>
    <p class="lead">Your answers are with me. I will read every one before the call, so the time together goes on your business, not on background.</p>
    <div class="cta"><a class="btn btn-ghost" href="/">Back to the site</a></div>
  </div>
</section>
'''

# ---------------------------------------------------------------- shell
shell = open(os.path.join(SITE, "book", "index.html"), encoding="utf-8").read()

def build(title, desc, canon, body_class, main, extra_head="", extra_js=""):
    s = shell
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', s)
    s = re.sub(r'<link rel="canonical" href="[^"]*">\n?', '<meta name="referrer" content="no-referrer">\n', s)
    s = s.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, nofollow, noarchive">')
    # strip social/structured data and the Beehiiv tracker: private client page
    s = re.sub(r'<meta property="og:[^>]*>\n?', "", s)
    s = re.sub(r'<meta name="twitter:[^>]*>\n?', "", s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", s, flags=re.S)
    s = re.sub(r'<!-- Beehiiv attribution tracker.*?</script>\n?', "", s, flags=re.S)
    s = s.replace("</head>", extra_head + "</head>")
    s = s.replace('class="pg-book"', f'class="{body_class}"')
    s = s.replace('href="#calendar">Book a call', 'href="/book/">Book a call')
    s = re.sub(r'<main id="main">.*?</main>', f'<main id="main">{main}</main>', s, flags=re.S)
    # no newsletter pop-up on this page
    s = re.sub(r'<div class="nl-pop".*?\n</div>\n(?=<script>)', "", s, flags=re.S)
    s = re.sub(r'\n    \(function\(\)\{\n      var pop=document.getElementById\(\'nlPop\'\).*?\}\)\(\);\n', "\n", s, flags=re.S)
    s = s.replace("../assets/", "/assets/")
    s = s.replace("</body>", extra_js + "</body>")
    if PREVIEW:
        css = open(os.path.join(SITE, "assets", "style.css"), encoding="utf-8").read().replace("url(/assets/", "url(https://revenueandbeyond.com/assets/")
        s = re.sub(r'<link rel="stylesheet" href="/assets/style.css[^"]*">', "<style>" + css.replace("\\", "\\\\") + "</style>", s)
        s = re.sub(r'href="/(?!/)', 'target="_blank" rel="noopener" href="https://revenueandbeyond.com/', s)
        s = s.replace('src="/assets/', 'src="https://revenueandbeyond.com/assets/')
        s = s.replace("fetch('/',", "(window.__peFake=function(){return Promise.resolve({ok:true});})('/',")
        s = s.replace('<main id="main">', '<main id="main"><div style="background:#0B363B;color:#fff;text-align:center;font-size:13px;font-weight:700;padding:9px 16px">Preview only. Nothing you type here is sent anywhere.</div>', 1)
    return s

# relative asset paths in the shell are ../assets: use absolute so depth doesn't matter
if PREVIEW:
    out = sys.argv[sys.argv.index("--preview") + 1]
    open(out, "w", encoding="utf-8").write(build("Pre-engagement pack", "Preview of the Revenue & Beyond pre-engagement pack.", "", "pg-pe", FORM_HTML, CSS, JS))
    print("preview written", out); sys.exit(0)
os.makedirs(os.path.join(SITE, SLUG, "thanks"), exist_ok=True)
page = build("Pre-engagement pack | Revenue & Beyond",
             "A short set of questions to complete before working with Simon Watson.",
             "", "pg-pe", FORM_HTML, CSS, JS)
open(os.path.join(SITE, SLUG, "index.html"), "w", encoding="utf-8").write(page)
thanks = build("Thank you | Revenue & Beyond", "Your pre-engagement answers are in.",
               "", "pg-pe", THANKS_MAIN)
open(os.path.join(SITE, SLUG, "thanks", "index.html"), "w", encoding="utf-8").write(thanks)

# Hiding relies on the page's own meta tags (noindex, no-referrer). Nothing in robots.txt,
# sitemap.xml, _headers or _redirects names the private path, so the site never reveals it.
hdr = os.path.join(SITE, "_headers")
if os.path.exists(hdr):
    h = open(hdr, encoding="utf-8").read()
    h2 = re.sub(r"\n*/pre-engagement/\*\n  X-Robots-Tag: noindex, nofollow\n?", "\n", h)
    if h2 != h: open(hdr, "w", encoding="utf-8").write(h2)
print("pre-engagement page written:", sum(1 for _ in re.finditer(r'name="', page)), "named fields incl. hidden")
