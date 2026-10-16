/**
 * Receiver for the map's "Suggest a project" form (src/ui/SuggestForm.tsx).
 *
 * Paste this into a Google Sheet's Apps Script editor (Extensions > Apps Script) and deploy it as a
 * web app; the steps are in scripts/suggest/README.md. Each suggestion becomes a row in the
 * "Suggestions" tab, and you get an email about it. Nothing is ever published back to the map.
 */

const SHEET_NAME = 'Suggestions';
const NOTIFY_BY_EMAIL = true;
const DAILY_LIMIT = 50; // ignore anything past this many a day (a flood is spam)
const LIMITS = { project: 200, place: 200, link: 500, notes: 2000, email: 200 };

function doPost(e) {
  const p = (e && e.parameter) || {};
  // A filled honeypot or a form sent within 3 seconds of loading is a bot. Answer "ok" anyway.
  if (p.website || Number(p.elapsed) < 3000) return ok_();
  const row = Object.keys(LIMITS).map((k) => clean_(p[k], LIMITS[k]));
  if (!row[0] || !row[1]) return ok_();

  const cache = CacheService.getScriptCache();
  const key = 'count-' + Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd');
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const count = Number(cache.get(key) || 0);
    if (count >= DAILY_LIMIT) return ok_();
    cache.put(key, String(count + 1), 21600);
    const book = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = book.getSheetByName(SHEET_NAME) || book.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Received', 'Project', 'Where', 'Official link', 'Notes', 'Email', 'Status']);
      sheet.setFrozenRows(1);
    }
    sheet.appendRow([new Date()].concat(row, ['new']));
  } finally {
    lock.releaseLock();
  }

  if (NOTIFY_BY_EMAIL) {
    const labels = ['Project', 'Where', 'Official link', 'Notes', 'Email'];
    MailApp.sendEmail({
      to: Session.getEffectiveUser().getEmail(),
      subject: 'Map suggestion: ' + row[0],
      body: labels.map((l, i) => l + ': ' + (row[i] || '-')).join('\n') +
        '\n\nAll suggestions: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl(),
    });
  }
  return ok_();
}

/** Trim, cap the length, and stop a cell from being read as a formula. */
function clean_(value, max) {
  let s = String(value || '').trim().slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function ok_() {
  return ContentService.createTextOutput('ok');
}
