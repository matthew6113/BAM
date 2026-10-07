# Keeping the map current

The map is updated about every six weeks: on the 1st of January, April, July and October, and on
the 15th of February, May, August and November. A scheduled Claude Code routine runs this
procedure in a fresh cloud session, opens a pull request with the changes, and lists possible
new projects for Matthew to decide on. Nothing reaches the live map until Matthew merges the PR.
The same steps work by hand.

The rules in `CLAUDE.md` apply throughout: official sources only, never invent a fact, keep
`lastVerified` honest, and put facts only the press reports in a project's `reported` record.

## 1. Start

- Work on a new branch, `upkeep/<YYYY-MM-DD>`, from the latest `main`.
- `npm install`, then `make upkeep`. This writes `docs/upkeep/<date>.md`: every project with
  its last check date, milestone dates that have passed, open "still being checked" items, and
  links that are broken or refuse automated requests. It changes no facts.

## 2. Re-check every existing project

Work through the checklist, starting with "Check first", then every project, oldest check first.
For each project:

1. Open its official pages (`officialLinks`, then the agency pages and records in `sources`) and
   look for anything since `lastVerified`: hearings and votes, approvals or appeals, amended
   agreements, permits issued or completed, groundbreakings, completions, sales, lawsuits,
   pauses, new applications or environmental documents. Good official places to look:
   - the city or county's project page and planning department news;
   - Legistar or Granicus agendas and minutes (Planning Commission, Council, Board of Supervisors,
     Port, OCII, redevelopment successor agencies);
   - CEQAnet (ceqanet.lci.ca.gov) for new notices on the project;
   - building permit portals (e.g. SF DBI, San José permits), where the record cites them.
2. Update the record only with what an official source states, citing the URL in `sources`:
   `stage`, `stageNote`, `timeline` (append; don't rewrite history), `nextMilestone`, `program`
   numbers, `developer`, and `verify` (drop items that are now settled, add new doubts).
   When documents disagree, the newer adopted one wins; note the other in `verify`.
3. Set `lastVerified` to today only if the project was actually re-checked. If a source couldn't
   be opened (blocked, down), say so in the PR instead of bumping the date.
4. Broken links: replace with the agency's current page for the same document, or remove the
   link if the fact it supported is cited elsewhere. Never swap in a press or developer page.
5. If the change affects what's drawn (a new site plan, heights, phases, a boundary change),
   don't redraw it in the routine. List it under "Geometry to redraw" in the PR.
6. Add a dated entry to `CHANGELOG.md` per project changed: what changed, why, and the source.
7. Update `_meta.lastVerified` to the newest record date.

## 3. Photos

Run `make photos` if the checklist lists approved photos that haven't been downloaded yet.
Don't add or replace photos without Matthew's approval.

## 4. Look for new projects (Matthew decides)

Search official sources for large Bay Area projects that aren't on the map or in `_meta.dropped`.
The bar: a master-planned, multi-building project of roughly 1,000+ homes or 1M+ sq ft of
commercial space, or a comparably large site (Matthew has also included smaller ones by choice,
such as Esmeralda and BART station-area housing). Places to look:

- CEQAnet: new notices of preparation and EIRs in the nine counties (Alameda, Contra Costa,
  Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, Sonoma);
- planning commission and council agendas of the largest cities (San Francisco, San José,
  Oakland, Fremont, Santa Clara, Sunnyvale, Mountain View, Concord, Richmond, Hayward,
  Santa Rosa, Vallejo);
- state lists: HCD's SB 35 / streamlined approvals, Prohousing designations;
- agency land programs (BART, Caltrain, VTA, Port of SF, Port of Oakland, state surplus land).

Don't add any of them. Write each lead under "New project leads" in the checklist: name, city,
size (homes and sq ft as the official source states them), stage, the official source URL, and
a one-line recommendation (include, exclude or borderline, and why). Also flag projects on the
map that look finished or dead, which Matthew may want to drop or keep as "complete".

## 5. Check and open the PR

- `npx tsc --noEmit` and `npm test` must pass.
- Commit in small, described steps, push the branch and open a PR to `main` titled
  "Update <YYYY-MM-DD>". In the body:
  - **What changed**: one line per project changed, with sources;
  - **Couldn't check**: blocked or down sources, and projects left at their old date;
  - **Geometry to redraw**: if any;
  - **New projects for Matthew**: the leads, each as a checkbox, with a request to reply with
    the ones to add (they'll go through the usual research and mapping steps);
  - **Still open**: anything else needing his decision.
- Don't merge. Matthew reviews and merges; merging to `main` deploys the site.
