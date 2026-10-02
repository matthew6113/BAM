# Official-source research: where it stands

Matthew's rule (2026-10-02): only official sources (see CLAUDE.md). This note hands the
research to the next session. Start with a network check:

```sh
for h in sfplanning.org data.sfgov.org codelibrary.amlegal.com ceqanet.lci.ca.gov; do
  printf "%-26s " $h; curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://$h/; done
```

If these still fail, the environment's network access hasn't been broadened. Matthew
changes it in the cloud environment settings. As of 2026-10-02 (second session) they still
failed, as did every other agency host tried (OCII, TIDA, Port, sfbos, Legistar, CEQAnet,
media.api.sf.gov and the South Bay, Peninsula and East Bay cities). WebFetch is blocked too;
WebSearch works, but only for finding exact filenames. Its summaries aren't sources: one
gave Potrero's Design for Development motion as 26038 when the minutes say 20638.

## Reachable even without broader access

SF Planning keeps its files in an S3 bucket that has been reachable all along. The
subdomain becomes a folder:

- `sfmea.sfplanning.org/<file>` → `https://sfplanning.s3.amazonaws.com/sfmea/<file>`
- `commissions.sfplanning.org/cpcpackets/<file>` → `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/<file>`
- Old site files are under `default/files/...`.

The bucket can't be listed, so you need exact filenames. A missing key returns 403.
Also reachable: `archives/sfhousingelement.org/files/AppendixB1.pdf` (2022 Housing Element
sites inventory, adopted Jan 2023), which profiles each large project.

Planning Commission minutes are the best official record in the bucket: case numbers,
program, acreage, heights, actions, motion numbers and dates. 361 hearings are reachable,
2013 to July 2022. They're named `cpcpackets/YYYYMMDD_cal.min.pdf` (2013–2017) and
`cpcpackets/YYYYMMDD_cal_min.pdf` (2018–2022). Later minutes aren't in the bucket. To rebuild
the local corpus (about 100 MB, `data/raw/official/cpcmin/`):

```sh
mkdir -p data/raw/official/cpcmin && cd data/raw/official/cpcmin
python3 -c "import datetime as d;x=d.date(2013,1,1)
while x<d.date(2023,1,1): print(x.strftime('%Y%m%d')); x+=d.timedelta(1)" |
  xargs -P 32 -I{} sh -c 'for s in _cal.min.pdf _cal_min.pdf; do
    curl -sf -o {}.pdf https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/{}$s &&
    pdftotext -layout {}.pdf {}.txt && break; done'
grep -il "india basin" *.txt
```

Hearing packets are often under the case number, e.g. `cpcpackets/2014-002541ENV.pdf`,
`cpcpackets/2007.0946.pdf`.

## Findings so far

- `docs/official-research/` holds per-project tables (data value, official value, status,
  source and page, verbatim quote) for the 11 other San Francisco projects, checked
  2026-10-02. They aren't applied to `data/projects.json` yet; see "Next" below.
- Potrero: the minutes add an official post-approval record, now in the timeline:
  Station A (Block 15) approved Oct 22, 2020 (Motion 20801, 11 stories, up to 403,750 sq ft
  office); about 896,323 sq ft office authorized site-wide Oct 21, 2021 (Motion 21019); the
  life-science block rule removed Jul 28, 2022 (Res. 21156). Also seen, not yet used: an
  informational hearing on Jul 15, 2021 on a ~237-ft, 27-story, 325-home tower on Block 7
  (2017-011878PHA-04), and an EIR addendum for the re-phasing (Sept 9, 2020). The EIR
  certification (Jan 30, 2020) is No. 20635.

## Potrero Power Station: leads

| Need | Official source | Notes |
|---|---|---|
| Approved block heights | Design for Development, approved by Planning Commission Motion 20638 (Jan 30, 2020) | Linked from sfplanning.org/potrero-power-station. Also on file with the Board of Supervisors, File No. 200040. Minutes: new buildings 65 to 240 ft, height district 65/240-PPS on map HT08. |
| Official boundary | Special Use District and zoning layers (data.sfgov.org); parcels 4175/002, 4175/017, 4175/018 (part), 4232/001, 4232/006, plus non-assessed Port and City land | Would replace the traced boundary ("approximate") with official geometry. |
| Affordable share (press: 30%) | Development Agreement (Board ordinance, 2020) | sfplanning.org hosts a DA terms PDF. |
| Construction status | DBI permits; UC Regents approval of the Block 2 building (Sept 2024 meeting, `regents.universityofcalifornia.edu/regmeet/sept24/f5attach6.pdf`); MOHCD (Mayor's Office of Housing) for the Sophie Maxwell Building | Needed before the stage returns to "partly built". |
| 2025–26 amendments | Addendum 2 to the EIR (CEQAnet SCH 2017112005, received 7/29/2026); Planning Commission recommendation; Board of Supervisors action | Search summaries say heights rise (65 to 180 ft, 300 ft on Block 6). Read the official text and check whether the Board adopted them. |

The press-only facts waiting for confirmation are in the project's `reported` record in
`data/projects.json`, and the open items are in its `verify` list.

## The other 24 projects

### San Francisco (11): checked against the bucket

Summary of `docs/official-research/`:
- Well covered (approvals, program, heights, parcels): India Basin, Balboa Reservoir,
  Pier 70, Mission Rock, Mission Bay, Candlestick Point, Hunters Point Shipyard, Treasure
  Island, Parkmerced (2010 documents only).
- Conflicts to resolve with the newest official figure: Pier 70 homes (data 2,000; Housing
  Element 2023 "up to 2,150") and open space (9 vs 6.5 acres); Mission Rock homes (1,200 vs
  "up to 1,300") and retail (200,000 vs ~241,000 gsf); Candlestick office (data 2M; latest
  readable official figure 750,000 sq ft in 2019, before the reported 2024 transfer);
  Treasure Island acres (405 vs ~400); India Basin acres note; Balboa open space (4.2 vs ~4).
- Nothing official reachable: Stonestown (case 2021-012028; all its documents are on blocked
  hosts) and Piers 30–32's current deal (only site size confirmed).
- Every 2024–2026 event (Candlestick groundbreaking and phase split, Treasure Island phase
  one, India Basin default, Parkmerced receivership, Pier 70 density proposal) is
  press-only so far. Official sources for them sit on blocked hosts (OCII, TIDA, Port,
  sfbos, CEQAnet); each findings file lists the exact documents to fetch.

### Next
1. When a project is mapped (Milestone 3), apply its findings file: official values in,
   conflicts settled by the newest official document, press-only facts and their sources
   into `reported`, official URLs into `sources`. The test enforces it from then on.
2. With broader network access: the Potrero D4D, DA and Addendum 2; Stonestown; and the
   2024–2026 records above.
3. The 13 projects outside San Francisco have no reachable official host at all.

### For each project

None are on the map yet; Milestone 3 adds them. For each one:
- Find the official boundary. Prefer GIS (a plan area, Special Use District or parcels) over tracing a figure.
- Confirm each fact in `projects.json` against an agency source.
- Move press-only facts into `reported`.
- `src/projects/official.ts` lists the accepted hosts, and its test enforces the rule once a project is mapped.
