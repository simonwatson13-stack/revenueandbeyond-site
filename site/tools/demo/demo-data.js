/* Shared made-up data for the two demos (/tools/demo/crm/ and /tools/demo/chief-of-staff/).
   Every company, person and email address here is invented. Dates are relative to today so the
   demo always looks current. */
(function () {
  var D = {};
  D.me = { name: "Alex Morgan", company: "Harbour Digital", email: "alex@harbourdigital.example" };

  D.stages = [
    ["lead", "Lead", "#fff"],
    ["discovery", "Discovery", "rgba(106,209,250,.35)"],
    ["proposal", "Proposal", "rgba(195,161,248,.4)"],
    ["negotiation", "Negotiation", "rgba(242,181,68,.35)"],
    ["won", "Won", "rgba(73,232,176,.55)"],
    ["lost", "Closed lost", "#E8E6E0"]
  ];

  // last = days since last touch, next = days until next action (negative = overdue)
  D.deals = [
    { id: "kelso", company: "Kelso Labs", contact: "Priya Shah", role: "Co-founder & CEO", email: "priya@kelsolabs.example", stage: "discovery", mrr: 3500, last: 2, next: 0, source: "LinkedIn inbound", nextAction: "Discovery call today 11:00", notes: "Seed-funded AI QA tool for fintech engineering teams. Priya still closes every deal. Wants a first sales hire by Q2.", prep: true },
    { id: "brightpath", company: "Brightpath Logistics", contact: "Tom Ellery", role: "Founder", email: "tom@brightpath.example", stage: "discovery", mrr: 2500, last: 1, next: 1, source: "Referral (Fernhill Studio)", nextAction: "Discovery call tomorrow 15:30", notes: "Route-planning SaaS for regional couriers. 14 staff. Revenue flat for three quarters.", prep: true },
    { id: "ortelius", company: "Ortelius Data", contact: "Hannah Brooks", role: "CEO", email: "hannah@orteliusdata.example", stage: "proposal", mrr: 4000, last: 9, next: -2, source: "Newsletter reply", nextAction: "Chase proposal sent 9 days ago", notes: "Proposal v2 sent. Hannah's co-founder reviewing. No reply since.", risk: true },
    { id: "marlow", company: "Marlow Robotics", contact: "James Okafor", role: "Founder & MD", email: "james@marlowrobotics.example", stage: "negotiation", mrr: 5000, last: 3, next: 2, source: "Event (Revenue Room)", nextAction: "Send revised terms with a smaller first phase", notes: "Asked to push to Q1. Real objection: cash until their January invoice run lands." },
    { id: "copperleaf", company: "Copperleaf HR", contact: "Sofia Marin", role: "Founder", email: "sofia@copperleaf.example", stage: "proposal", mrr: 3500, last: 4, next: 3, source: "LinkedIn outbound", nextAction: "Proposal walk-through call Thursday", notes: "Wants the first 90 days focused on outbound and a sales hire." },
    { id: "tidewater", company: "Tidewater Systems", contact: "Ben Carter", role: "CEO", email: "ben@tidewater.example", stage: "lead", mrr: null, last: 6, next: 1, source: "Website: Book a call", nextAction: "Reply to booking form and qualify", notes: "Booked through the website. 22 staff, B2B payroll software." },
    { id: "larkspur", company: "Larkspur Health", contact: "Dr Amira Haddad", role: "Founder", email: "amira@larkspur.example", stage: "lead", mrr: null, last: 15, next: -5, source: "Webinar sign-up", nextAction: "Send the founder-led sales blueprint", notes: "Attended the webinar, asked a question about pricing.", risk: true },
    { id: "quill", company: "Quill & Co", contact: "Ellie Ward", role: "Managing Partner", email: "ellie@quillandco.example", stage: "negotiation", mrr: 3000, last: 1, next: 4, source: "Referral (client)", nextAction: "Contract out for signature", notes: "Verbal yes on Monday. Legal reviewing terms." },
    { id: "fernhill", company: "Fernhill Studio", contact: "Marcus Lee", role: "Founder", email: "marcus@fernhill.example", stage: "won", mrr: 3500, last: 5, next: 7, source: "Referral", nextAction: "Week 6 working session", notes: "Client since September. Sprint milestone on track." },
    { id: "northwind", company: "Northwind Analytics", contact: "Grace Lin", role: "CEO", email: "grace@northwind.example", stage: "won", mrr: 4500, last: 2, next: 2, source: "LinkedIn outbound", nextAction: "Quarterly review prep", notes: "Client since July. Second sales hire starting next month." },
    { id: "pebble", company: "Pebble Payments", contact: "Owen Price", role: "Founder", email: "owen@pebble.example", stage: "lost", mrr: 2500, last: 30, next: null, source: "Event", nextAction: "Check in again in March", notes: "Chose to hire a head of sales instead. Left on good terms." }
  ];

  // What the weekly sweep "finds" in email, calendar, call notes and LinkedIn
  D.sweep = [
    { id: "ortelius", field: "stage", to: "negotiation", why: "Email from Hannah Brooks, 2 days ago: \"Board approved the budget. Can we talk terms on Friday?\"", src: "Gmail" },
    { id: "tidewater", field: "stage", to: "discovery", why: "Calendar: \"Discovery call: Tidewater Systems\" booked for Monday 10:00", src: "Calendar" },
    { id: "larkspur", field: "note", to: "Opened the blueprint email twice, no reply. Try a direct question about their pricing page.", why: "Newsletter platform: opened twice, clicked once, no reply in 15 days", src: "Beehiiv" }
  ];

  D.meetings = [
    { t: "09:00", end: "09:30", title: "Team stand-up", kind: "team", who: "Harbour Digital team" },
    { t: "11:00", end: "11:45", title: "Discovery call: Kelso Labs", kind: "client", who: "Priya Shah, Co-founder & CEO", deal: "kelso", prep: true },
    { t: "13:30", end: "14:00", title: "Working session: Fernhill Studio", kind: "client", who: "Marcus Lee", deal: "fernhill" },
    { t: "16:00", end: "16:30", title: "Terms call: Marlow Robotics", kind: "client", who: "James Okafor", deal: "marlow" }
  ];

  D.replies = [
    { from: "Hannah Brooks", co: "Ortelius Data", email: "hannah@orteliusdata.example", subj: "Re: Proposal v2", snippet: "Board approved the budget. Can we talk terms on Friday?", age: "2 days", pri: "high", deal: "ortelius",
      draft: "Hi Hannah,\n\nGreat news, thank you. Friday works. Does 10:00 or 14:00 suit you better? I'll bring a one-page summary of the terms so we can agree them on the call.\n\nBest,\nAlex" },
    { from: "Ben Carter", co: "Tidewater Systems", email: "ben@tidewater.example", subj: "Website booking: sales help", snippet: "We're 22 people and I'm still doing every demo. Is this something you help with?", age: "1 day", pri: "high", deal: "tidewater",
      draft: "Hi Ben,\n\nThanks for getting in touch. Yes, that's exactly what I help with. Before Monday's call, what would need to be true in six months for you to stop doing every demo yourself?\n\nBest,\nAlex" },
    { from: "Ellie Ward", co: "Quill & Co", email: "ellie@quillandco.example", subj: "Contract question", snippet: "Our lawyer asked about the notice period in clause 7.", age: "Today", pri: "med", deal: "quill",
      draft: "Hi Ellie,\n\nGood question from your lawyer. The notice period is 30 days after the first 90 days, so you're never locked in beyond the first sprint. Happy to jump on a quick call if useful.\n\nBest,\nAlex" }
  ];

  D.leads = [
    { name: "Nadia Petrov", co: "Lumen Freight", signal: "Viewed the pricing page 3 times this week and downloaded the blueprint", action: "Send a short personal note, not a pitch" },
    { name: "Chris Adebayo", co: "Stackwise", signal: "Commented on your LinkedIn post about first sales hires", action: "Reply to the comment, then connect" }
  ];

  D.prep = {
    kelso: {
      when: "Today, 11:00 to 11:45 (Google Meet)",
      company: "Kelso Labs",
      site: "kelsolabs.example",
      oneLiner: "AI test automation for engineering teams at fintechs and challenger banks.",
      facts: [["Founded", "2022, London"], ["Team", "18 people (4 open roles)"], ["Funding", "£3.2m seed, led by a London fintech fund, March this year"], ["Revenue", "Estimated £900k ARR, 11 customers"], ["Sales today", "Founder-led. Priya runs every first call and demo"]],
      person: { name: "Priya Shah", role: "Co-founder & CEO", bio: "Ex-engineering lead at a payments scale-up. Technical founder. Posts weekly on LinkedIn about testing culture.", recent: "Posted last week: \"Our sales cycle is longer than our build cycle. Something has to change.\"" },
      signals: ["Hiring an Account Executive (posted 12 days ago, first sales role)", "Two enterprise logos added to the website this quarter", "Reviews mention onboarding speed as the main reason they chose Kelso", "Competitor raised a Series A last month and is hiring four SDRs"],
      competitors: [["TestPilot AI", "Bigger, enterprise-focused, 9-month sales cycles"], ["Quantra", "Cheaper, self-serve, weaker on compliance"]],
      fit: { score: 8, of: 10, why: "Founder-led sales, first hire about to happen, funded and under pressure to show growth. Classic fit for the first 90 days." },
      watch: ["She may want to hire first and fix the process later. Test whether the AE will inherit anything written down.", "Technical founder: keep it concrete, show the numbers, skip the theory."],
      questions: [
        "Walk me through the last deal you won, from first touch to signature. Where did it nearly stall?",
        "What happens to a new lead today if you're on holiday for two weeks?",
        "You're hiring an AE. What will they sell, to whom, and what will they inherit on day one?",
        "What's your average sales cycle, and what would it be worth to cut it by a third?",
        "Who else is involved in a decision like this one? Your co-founder? The board?",
        "If we fast-forward six months and this has worked, what's different?",
        "What have you already tried to take sales off your plate, and what happened?"
      ],
      message: "Hi Priya,\n\nLooking forward to 11:00. I saw you're hiring your first AE, so I'd like to spend part of the call on what they'll inherit on day one.\n\nIf it helps, bring the last deal you won and we'll walk it through together.\n\nSee you shortly,\nAlex"
    },
    brightpath: {
      when: "Tomorrow, 15:30 to 16:15 (Zoom)",
      company: "Brightpath Logistics",
      site: "brightpath.example",
      oneLiner: "Route-planning software for regional courier and same-day delivery firms.",
      facts: [["Founded", "2019, Leeds"], ["Team", "14 people"], ["Funding", "Bootstrapped, profitable"], ["Revenue", "Estimated £1.4m ARR, flat for three quarters"], ["Sales today", "Founder plus one account manager, mostly referrals"]],
      person: { name: "Tom Ellery", role: "Founder", bio: "Ran a courier business for 10 years before building the software. Strong network in the industry.", recent: "Spoke on a logistics podcast about \"growing without VC\"." },
      signals: ["Referral from Fernhill Studio, a current client", "Pricing page unchanged since 2023", "Two of their larger customers were acquired this year", "No outbound activity visible on LinkedIn"],
      competitors: [["Routely", "VC-backed, aggressive pricing"], ["In-house spreadsheets", "The real competitor for most small couriers"]],
      fit: { score: 7, of: 10, why: "Profitable and stuck. Referral trust is high. Risk: no urgency, and he may see it as a cost rather than a growth plan." },
      watch: ["Flat revenue may be a pricing problem, not a sales one. Ask about the last price rise.", "Bootstrapped founder: lead with payback, not ambition."],
      questions: [
        "Revenue has been flat for three quarters. What's your read on why?",
        "When did you last put your prices up, and what happened?",
        "Where do new customers come from today, and how many came from somewhere other than referrals last year?",
        "Two of your bigger customers were acquired. What has that done to renewals?",
        "If you had a second salesperson tomorrow, what would they do in week one?",
        "What would make the next 12 months a great year?",
        "What would stop you from doing this, even if it made sense?"
      ],
      message: "Hi Tom,\n\nMarcus speaks very highly of you, so I'm glad we're talking tomorrow at 15:30.\n\nOne thing that would help: a rough idea of where your last ten customers came from. No need to be precise.\n\nSpeak tomorrow,\nAlex"
    }
  };

  // Claude Project prompt built from a prep doc
  D.projectPrompt = function (id) {
    var p = D.prep[id], d = D.deal(id);
    if (!p || !d) return "";
    return [
      "PROJECT NAME",
      p.company + ": discovery and proposal",
      "",
      "PROJECT INSTRUCTIONS (paste into the Project's custom instructions)",
      "You are my deal partner for " + p.company + " (" + p.site + "). I am " + D.me.name + ", founder of " + D.me.company + ".",
      "",
      "About the prospect:",
      "- " + p.oneLiner,
      p.facts.map(function (f) { return "- " + f[0] + ": " + f[1]; }).join("\n"),
      "- Main contact: " + p.person.name + ", " + p.person.role + ". " + p.person.bio,
      "",
      "What we know so far:",
      p.signals.map(function (s) { return "- " + s; }).join("\n"),
      "- Fit read: " + p.fit.score + "/" + p.fit.of + ". " + p.fit.why,
      "",
      "Watch-outs:",
      p.watch.map(function (s) { return "- " + s; }).join("\n"),
      "",
      "How to help me:",
      "1. After each call I will paste the transcript or my notes. Summarise what we learned, update the deal picture and list the open questions.",
      "2. Draft follow-up emails in my voice: short, plain English, one clear next step with a date.",
      "3. When I ask for a proposal, use my proposal template from the project files, with three options and firm prices.",
      "4. Flag objections early and suggest the question that brings out the real one.",
      "5. Never invent facts about " + p.company + ". If something is unknown, say so and suggest how to find out.",
      "",
      "FILES TO ADD TO THE PROJECT",
      "- This prep doc (download or copy from the brief)",
      "- My proposal template and pricing guide",
      "- Call transcripts as they happen (from Fathom or Granola)",
      "- Any documents " + p.person.name.split(" ")[0] + " sends over"
    ].join("\n");
  };

  D.deal = function (id) { for (var i = 0; i < D.deals.length; i++) if (D.deals[i].id === id) return D.deals[i]; return null; };
  D.money = function (n) { return n == null ? "" : "£" + n.toLocaleString("en-GB"); };
  D.dateFrom = function (days) { var x = new Date(); x.setDate(x.getDate() + days); return x; };
  D.fmt = function (dt, opts) { return dt.toLocaleDateString("en-GB", opts || { weekday: "short", day: "numeric", month: "short" }); };
  D.gmailCompose = function (to, subj, body) {
    return "https://mail.google.com/mail/?view=cm&fs=1&to=" + encodeURIComponent(to) + "&su=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
  };
  D.gmailSearch = function (q) { return "https://mail.google.com/mail/u/0/#search/" + encodeURIComponent(q); };

  // Per-viewer state (moves, done items). Optional: the demo works without it.
  D.load = function (k, def) { try { var v = localStorage.getItem("rbdemo:" + k); return v ? JSON.parse(v) : def; } catch (e) { return def; } };
  D.save = function (k, v) { try { localStorage.setItem("rbdemo:" + k, JSON.stringify(v)); } catch (e) {} };
  D.reset = function () { try { Object.keys(localStorage).forEach(function (k) { if (k.indexOf("rbdemo:") === 0) localStorage.removeItem(k); }); } catch (e) {} };

  // Apply saved deal edits (stage moves, notes) on top of the defaults
  var saved = D.load("deals", null);
  if (saved) D.deals.forEach(function (d) { if (saved[d.id]) for (var k in saved[d.id]) d[k] = saved[d.id][k]; });
  var added = D.load("added", []);
  added.forEach(function (d) { if (!D.deal(d.id)) D.deals.push(d); });
  D.persist = function (d, patch) {
    var s = D.load("deals", {}); s[d.id] = Object.assign(s[d.id] || {}, patch); D.save("deals", s);
    for (var k in patch) d[k] = patch[k];
  };
  window.RBDemo = D;
})();
