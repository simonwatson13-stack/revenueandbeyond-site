/**
 * 3am Thoughts – Lead Feed
 * Runs inside simon@3amthoughts.co.uk (script.google.com). Read-only on Gmail.
 *
 * Once a day it searches this inbox and writes one row per conversation to a
 * Google Sheet called "3am Thoughts – Lead Feed", shared (view only) with
 * simon@revenueandbeyond.com. The R&B pipeline sweep reads that sheet every Monday.
 * Nothing is forwarded, sent, labelled or deleted. Only the summary row leaves the inbox.
 *
 * SETUP (once):
 *   1. Paste this whole file into a new project at script.google.com (signed in as the 3am account).
 *   2. Choose the function "setup" in the toolbar and click Run. Approve the permissions.
 *   3. That's it. It creates the sheet, shares it, back-fills 18 months and schedules a daily refresh at about 6am.
 */

const CONFIG = {
  sheetName: '3am Thoughts – Lead Feed',
  shareWith: 'simon@revenueandbeyond.com',
  ownDomains: ['3amthoughts.co.uk', '3amthoughts.com', 'revenueandbeyond.com'],
  backfillDays: 540,     // first run: about 18 months
  dailyDays: 14,         // daily runs: re-check the last two weeks (catches new replies on older threads)
  maxThreads: 400,       // per run, to stay inside Apps Script time limits
  snippetChars: 300,
  // Skip bulk mail and automated senders. Booking invites from Jordan are kept.
  baseQuery: '-category:promotions -category:social -category:forums ' +
             '-from:(noreply OR no-reply OR notifications OR mailer-daemon OR newsletter OR news) ' +
             '-subject:("3-Minute Read")'
};

const HEADERS = [
  'Thread ID', 'Last message', 'First message', 'Subject', 'External contacts', 'Company domains',
  'Internal only', 'Messages', 'Last sender', 'Last message snippet',
  'Booking: company website', 'Booking: what they do', 'Booking: turnover', 'Booking: challenges',
  'Booking: service wanted', 'Gmail link', 'Updated'
];

function setup() {
  const ss = getSheet_();
  try {
    ss.addViewer(CONFIG.shareWith);
  } catch (e) {
    Logger.log('Could not share automatically (' + e + '). Share the sheet with ' + CONFIG.shareWith + ' by hand.');
  }
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'refresh')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('refresh').timeBased().everyDays(1).atHour(6).inTimezone('Europe/London').create();
  run_(CONFIG.backfillDays);
  Logger.log('Done. Sheet: ' + ss.getUrl());
}

function refresh() {
  run_(CONFIG.dailyDays);
}

function run_(days) {
  const ss = getSheet_();
  const sh = ss.getSheets()[0];
  const existing = readExisting_(sh);
  const threads = searchAll_(CONFIG.baseQuery + ' newer_than:' + days + 'd', CONFIG.maxThreads);
  const now = new Date();
  threads.forEach(th => {
    const row = summarise_(th, now);
    if (!row) return;
    const at = existing.index[row[0]];
    if (at) {
      sh.getRange(at, 1, 1, HEADERS.length).setValues([row]);
    } else {
      sh.appendRow(row);
      existing.index[row[0]] = sh.getLastRow();
    }
  });
  if (sh.getLastRow() > 2) {
    sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).sort({ column: 2, ascending: false });
  }
}

function searchAll_(query, max) {
  const out = [];
  for (let start = 0; out.length < max; start += 100) {
    const batch = GmailApp.search(query, start, Math.min(100, max - out.length));
    out.push.apply(out, batch);
    if (batch.length < 100) break;
  }
  return out;
}

function summarise_(thread, now) {
  const msgs = thread.getMessages();
  if (!msgs.length) return null;
  const first = msgs[0], last = msgs[msgs.length - 1];

  const people = {};
  msgs.forEach(m => {
    [m.getFrom(), m.getTo(), m.getCc()].join(',').split(',').forEach(raw => {
      const email = (raw.match(/<([^>]+)>/) || [null, raw])[1].trim().toLowerCase();
      if (!email || email.indexOf('@') < 0) return;
      const domain = email.split('@')[1];
      if (CONFIG.ownDomains.indexOf(domain) >= 0) return;
      const name = raw.replace(/<[^>]+>/, '').replace(/"/g, '').trim();
      people[email] = name && name.indexOf('@') < 0 ? name + ' <' + email + '>' : email;
    });
  });
  const emails = Object.keys(people);
  const domains = Array.from(new Set(emails.map(e => e.split('@')[1])))
    .filter(d => ['gmail.com', 'googlemail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'icloud.com'].indexOf(d) < 0);

  // Jordan's "Business Diagnosis Call" booking invites carry the lead's answers.
  const bookingText = msgs.map(m => m.getPlainBody()).find(b => /Business Diagnosis Call/i.test(b) && /annual turnover/i.test(b)) || '';
  const field = label => {
    const m = bookingText.match(new RegExp(label + '[^\\n]*:\\s*\\n?\\s*([^\\n]+)', 'i'));
    return m ? m[1].replace(/<[^>]+>/g, '').trim().slice(0, 200) : '';
  };

  const snippet = (last.getPlainBody() || '')
    .split(/\n(On .+wrote:|From: |-----Original Message-----)/)[0]
    .replace(/\s+/g, ' ').trim().slice(0, CONFIG.snippetChars);

  return [
    thread.getId(),
    last.getDate(),
    first.getDate(),
    thread.getFirstMessageSubject(),
    Object.values(people).join('; '),
    domains.join('; '),
    emails.length ? 'No' : 'Yes',
    msgs.length,
    last.getFrom(),
    snippet,
    field('Company website'),
    field('core solution/service your company offers'),
    field('annual turnover'),
    field('top 3 challenges'),
    field('Which service are you interested in'),
    'https://mail.google.com/mail/u/0/#all/' + thread.getId(),
    now
  ];
}

function getSheet_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty('SHEET_ID');
  if (id) {
    try { return SpreadsheetApp.openById(id); } catch (e) { /* recreate below */ }
  }
  const ss = SpreadsheetApp.create(CONFIG.sheetName);
  const sh = ss.getSheets()[0];
  sh.setName('Threads');
  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
  sh.setFrozenRows(1);
  props.setProperty('SHEET_ID', ss.getId());
  return ss;
}

function readExisting_(sh) {
  const index = {};
  const n = sh.getLastRow();
  if (n > 1) {
    sh.getRange(2, 1, n - 1, 1).getValues().forEach((r, i) => { if (r[0]) index[r[0]] = i + 2; });
  }
  return { index: index };
}
