# Suggestion form: setup

The "Suggest a project" form (About page, and the link at the foot of the Projects list) sends
each suggestion to a small Google Apps Script that Matthew owns. The script adds a row to a Google
Sheet and emails him. The site is static, so this is the one piece that runs somewhere else. It's
free and needs no other service.

Until it's set up, the form still works: it opens a prefilled GitHub issue instead (people need a
GitHub account, and issues are public).

## Set up (about 5 minutes, once)

1. Create a Google Sheet, e.g. "Map suggestions".
2. In the Sheet: **Extensions → Apps Script**. Replace the editor's contents with
   [`apps-script.gs`](apps-script.gs) and save.
3. **Deploy → New deployment → Select type: Web app.**
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy, and allow the permissions it asks for (edit this spreadsheet, send email as you).
4. Copy the **Web app URL** (`https://script.google.com/macros/s/…/exec`).
5. In GitHub: **matthew6113/BAM → Settings → Secrets and variables → Actions → Variables → New
   repository variable**. Name `SUGGEST_URL`, value the web app URL.
6. Re-run the deploy (push to `main`, or **Actions → Deploy → Run workflow**). The form now sends
   to the Sheet and asks for an optional email for a reply.

The URL is public by design (it's in the page's code); all it can do is add a row. The script drops
obvious bots (a hidden honeypot field, forms sent within 3 seconds) and anything past 50 a day.

## Changing the script later

Edit it in Apps Script, then **Deploy → Manage deployments → Edit (pencil) → Version: New version
→ Deploy**. That keeps the same URL. A brand-new deployment gets a new URL, which would need step 5
again.

## Using the suggestions

The Sheet has a Status column (starts at `new`). Suggestions are leads, not facts: a project goes
on the map only after the usual official-source research. The six-weekly update also reviews open
GitHub issues titled "Suggest: …" (docs/UPKEEP.md, step 4); to have it look at Sheet suggestions,
paste them into the update PR or a GitHub issue.
