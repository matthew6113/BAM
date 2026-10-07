"""Upkeep checklist: what to re-check in each project's record, generated from the data.

Runs every six weeks or so as the first step of the update routine (docs/UPKEEP.md). It doesn't
change any project fact; it writes docs/upkeep/<date>.md listing, for every project:

- how long since its record was last verified,
- milestone dates in nextMilestone, stageNote and verify that have now passed (check the outcome),
- its open "still being checked" items,
- official links and sources that are broken (404, 410, 5xx, no answer) or that refuse
  automated requests (403, 429: open them in a browser),

plus approved photos that haven't been downloaded yet. The person or agent doing the update
works through it and records what changed in CHANGELOG.md.

    uv run --directory pipeline python -m bam_pipeline.upkeep [--no-links] [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import config

PROJECTS = config.ROOT / "data" / "projects.json"
PHOTOS = config.ROOT / "data" / "photos.json"
OUT = config.ROOT / "docs" / "upkeep"
UA = "BAM-megaprojects-map/1.0 upkeep (https://github.com/matthew6113/BAM)"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
DATE_RE = re.compile(
    r"\b(\d{4})-(\d{2})-(\d{2})\b"
    r"|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? (\d{1,2}),? (\d{4})\b"
    r"|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]* (\d{4})\b"
    r"|\b(Q[1-4]) (\d{4})\b")


def dates_in(text: str) -> list[tuple[dt.date, str]]:
    """Dates mentioned in a sentence, with the text that named them. Month-only and quarter
    dates count from the end of that month or quarter, so they only pass once it's over."""
    found = []
    for m in DATE_RE.finditer(text or ""):
        g = m.groups()
        try:
            if g[0]:
                d = dt.date(int(g[0]), int(g[1]), int(g[2]))
            elif g[3]:
                d = dt.date(int(g[5]), MONTHS[g[3][:3].lower()], int(g[4]))
            elif g[6]:
                y, mo = int(g[7]), MONTHS[g[6][:3].lower()]
                d = (dt.date(y + mo // 12, mo % 12 + 1, 1) - dt.timedelta(days=1))
            else:
                y, q = int(g[9]), int(g[8][1])
                d = dt.date(y + (q == 4), (q * 3) % 12 + 1, 1) - dt.timedelta(days=1)
        except ValueError:
            continue
        found.append((d, m.group(0)))
    return found


def check(url: str) -> tuple[str, str]:
    """('ok' | 'blocked' | 'broken' | 'unreachable', detail) for one link. A quick HEAD that
    succeeds is enough; anything else is confirmed with a full GET (some city sites, e.g.
    CivicPlus DocumentCenter, answer 404 to HEAD but serve the page), retried once."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            return "ok", str(r.status)
    except Exception:
        pass
    last = "no answer"
    for _ in range(2):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                r.read(1)
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429):
                return "blocked", str(e.code)
            if e.code < 500:
                return "broken", str(e.code)
            last = str(e.code)
        except Exception as e:  # DNS, TLS, timeout, connection reset
            last = type(e).__name__
    return "unreachable", last


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-links", action="store_true", help="skip checking links")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.date)

    data = json.loads(PROJECTS.read_text())
    projects = data["projects"]
    photos = json.loads(PHOTOS.read_text())["photos"]

    links: dict[str, tuple[str, str]] = {}
    if not args.no_links:
        urls = sorted({u for p in projects for u in p.get("officialLinks", []) + p.get("sources", [])})
        with ThreadPoolExecutor(8) as pool:
            for u, r in zip(urls, pool.map(check, urls)):
                links[u] = r

    rows, due, broken, blocked, unreachable = [], [], [], [], []
    for p in sorted(projects, key=lambda p: p["lastVerified"]):
        age = (today - dt.date.fromisoformat(p["lastVerified"])).days
        passed = []
        for field in ("nextMilestone", "stageNote"):
            for d, text in dates_in(p.get(field) or ""):
                if dt.date.fromisoformat(p["lastVerified"]) <= d < today:
                    passed.append(f"{text} ({field})")
        for v in p.get("verify", []):
            for d, text in dates_in(v):
                if dt.date.fromisoformat(p["lastVerified"]) <= d < today:
                    passed.append(f"{text} (verify)")
        if passed:
            due.append((p["id"], sorted(set(passed))))
        cited = list(dict.fromkeys(p.get("officialLinks", []) + p.get("sources", [])))
        bad = [u for u in cited if links.get(u, ("ok",))[0] == "broken"]
        blk = [u for u in cited if links.get(u, ("ok",))[0] == "blocked"]
        down = [u for u in cited if links.get(u, ("ok",))[0] == "unreachable"]
        broken += [(p["id"], u, links[u][1]) for u in bad]
        unreachable += [(p["id"], u, links[u][1]) for u in down]
        blocked += [(p["id"], u, links[u][1]) for u in blk]
        nm = (p.get("nextMilestone") or "none recorded").replace("|", "/")
        rows.append(f"| {p['id']} | {p['stage']} | {p['lastVerified']} ({age} days) | {nm} | "
                    f"{len(p.get('verify', []))} | {len(bad)} broken, {len(blk)} blocked |")

    pending = [p["id"] for p in photos if "src" not in p]
    lines = [
        f"# Upkeep checklist, {today.isoformat()}",
        "",
        "Generated by `make upkeep` from `data/projects.json`; the procedure is in `docs/UPKEEP.md`.",
        "Nothing here is a fact to publish: it's what to re-check against official sources.",
        "",
        f"{len(projects)} projects. {len(due)} have milestone dates that have passed since they were "
        f"last verified. "
        + ("Links weren't checked (--no-links)." if args.no_links else
           f"{len(links)} distinct links checked: {sum(r[0] == 'broken' for r in links.values())} broken, "
           f"{sum(r[0] == 'blocked' for r in links.values())} refuse automated requests, "
           f"{sum(r[0] == 'unreachable' for r in links.values())} didn't answer."),
        "",
        "## Check first: dates that have passed",
        "",
    ]
    lines += [f"- [ ] **{pid}**: {', '.join(items)}" for pid, items in due] or ["None."]
    lines += ["", "## Every project (oldest check first)", "",
              "| Project | Stage | Last verified | Next milestone | Open checks | Links |",
              "|---|---|---|---|---|---|", *rows, ""]
    if not args.no_links:
        lines += ["## Broken links (replace with a working official page or drop)", ""]
        lines += [f"- [ ] {pid}: {u} ({code})" for pid, u, code in broken] or ["None."]
        lines += ["", "## Links that refuse automated requests (open in a browser)", ""]
        lines += [f"- [ ] {pid}: {u} ({code})" for pid, u, code in blocked] or ["None."]
        lines += ["", "## Links that didn't answer (server error or network; try again or in a browser)", ""]
        lines += [f"- [ ] {pid}: {u} ({code})" for pid, u, code in unreachable] or ["None."]
        lines.append("")
    lines += ["## Photos approved but not downloaded (`make photos`)", ""]
    lines += [f"- [ ] {pid}" for pid in pending] or ["None."]
    lines += ["", "## New project leads", "",
              "Filled in by whoever runs the update (see docs/UPKEEP.md, step 4). Matthew decides which to add.", ""]

    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{today.isoformat()}.md"
    out.write_text("\n".join(lines) + "\n")
    print(out.relative_to(config.ROOT))


if __name__ == "__main__":
    main()
