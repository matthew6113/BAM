# Official-source research: where it stands

Matthew's rule (2026-10-02): only official sources (see CLAUDE.md). This note hands the
research to the next session. Start with a network check:

```sh
for h in sfplanning.org data.sfgov.org codelibrary.amlegal.com ceqanet.lci.ca.gov; do
  printf "%-26s " $h; curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://$h/; done
```

Network access was broadened on 2026-10-02: sfplanning.org, data.sfgov.org, CEQAnet,
sfgov.legistar.com, sfbos.org, the Port, UC Regents and the city sites respond. amlegal still
returns 403 to scripts (bot blocking). WebSearch summaries aren't sources: one gave
Potrero's Design for Development motion as 26038 when the minutes say 20638.

## SF Planning's document store (S3)

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

All 25 projects have been checked against official sources (2026-10-02). Per-project tables
(data value, official value, status, source and page, verbatim quote, best boundary source)
are in `docs/official-research/`:
- `candlestick-shipyard-treasure-island.md`, `pier70-mission-rock-mission-bay-piers30-32.md`,
  `india-basin-balboa-stonestown-parkmerced.md`: a first pass from SF Planning's bucket, then
  an "Update with full network access" section that supersedes it.
- `brisbane-willow-parkline-north-bayshore.md`, `related-downtown-west-moffett-the-rise.md`,
  `concord-coliseum-alameda-brooklyn-suisun.md`.

All 25 records have been applied to `data/projects.json` (2026-10-03, Milestone 3), and every
project is mapped, so the official-sources test covers them all. Open items per project are in
each record's `verify` list.

Decisions (Matthew, 2026-10-03):
- **Applying findings:** apply each project's findings file when it is mapped (Milestone 3),
  not all at once.
- **City-run sites on non-government domains count as official.** They're listed in
  `src/projects/official.ts`; shared vendor hosts (Legistar/Granicus, ArcGIS Online,
  CloudFront) only under the agency's own path.
- **Permit dates count for stages.** A DBI (or city) building permit's first construction
  document date marks "under construction", and its completion date marks a building
  delivered. Word them as permit facts in the UI ("permit marked complete Aug 28, 2026"),
  since they aren't opening dates.
- Some city sites block scripts with Akamai (Oakland, Alameda, Santa Clara, San Jose,
  Sunnyvale, Cupertino, Suisun); their Legistar systems work instead.

## Potrero Power Station: done (2026-10-02)

Network access was broadened on 2026-10-02 and every lead below was read:
- Design for Development, Feb 26, 2020 (Motion 20638):
  `sfplanning.org/sites/default/files/documents/citywide/potreropower_D4D_final.pdf`.
  Figure 6.2.3 Building Height Plan (p. 245) gives each block's height (65 to 240 ft).
  Traced 2026-10-03 into `data/massing/` (see docs/DECISIONS.md).
- Development agreement: Board File 200040, Ordinance 62-20, finally passed Apr 21, 2020,
  effective May 24, 2020 (not May 25). The recorded agreement (Recital H) says affordable
  housing is "intended to constitute thirty percent (30%)" of all units. First amendment:
  Ordinance 67-24 (EIFD).
- 2026 amendments: Addendum 2 (CEQAnet, July 16, 2026) proposes +8 ft on residential blocks
  and more on Blocks 1, 5, 11, 12 and 15 (its Figure 6). The search summary's "65 to 180 ft,
  300 on Block 6" was wrong. Planning Commission recommended them July 30, 2026 (Res. 21945);
  the Board's Land Use Committee recommended File 260724 on Sept 28, 2026; the full Board's
  vote and the SUD ordinance (File 260770) are pending. Until enacted, the 2020 D4D governs.
- Built: the Sophie Maxwell Building, 1212 Maryland St. (DBI permit 202212229038: 8 stories,
  105 homes, 100% affordable; issued Oct 25, 2023; completed Aug 28, 2026). Stage is now
  "partly built".
- UCSF Block 2: Regents approved Sept 19, 2024 (300,000 gsf, 8 stories, 130 ft plus an
  18-ft screen). Construction start (press: Aug 2025) still needs an official source.
- The SF Legistar API (webapi.legistar.com) stops around 2020; read file pages on
  sfgov.legistar.com instead. sfgov.legistar.com is now an official host.

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
1. Done (Milestone 3): findings applied and all projects mapped.
2. With broader network access: the Potrero D4D, DA and Addendum 2; Stonestown; and the
   2024–2026 records above.
3. The 13 projects outside San Francisco have no reachable official host at all.

### For each project

None are on the map yet; Milestone 3 adds them. For each one:
- Find the official boundary. Prefer GIS (a plan area, Special Use District or parcels) over tracing a figure.
- Confirm each fact in `projects.json` against an agency source.
- Move press-only facts into `reported`.
- `src/projects/official.ts` lists the accepted hosts, and its test enforces the rule once a project is mapped.
