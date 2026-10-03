# Changelog

Data changes to `data/projects.json` and other project facts, newest first. Each entry
says what changed, why and against which source. Code changes live in git history.

## 2026-10-03 (Milestone 4, batch 2: massing for five more San Francisco projects)

`massingNotes` updated and each massing source (design documents, DBI permits for built
buildings) added to `sources` for **candlestick-point**, **hunters-point-shipyard**,
**treasure-island**, **mission-bay** and **piers-30-32**. Hunters Point's notes now give its
two towers (370 and 270 ft), which the 2018 Design for Development allows beyond the 40–120 ft
block limits. Mission Bay's only unbuilt plan blocks are 4 East and 12 West (MOHCD pipeline,
DBI permits); its official page in `sources` (sfocii.org/mission-bay) now returns 404 and is
due for replacement at its next re-check.

## 2026-10-03 (Milestone 4, batch 1: massing for five San Francisco projects)

`massingNotes` updated and each massing source added to `sources` for **balboa-reservoir**,
**mission-rock**, **pier-70**, **stonestown** and **india-basin**. All massing is traced from
adopted design standards or the zoning map and drawn to the height limit, labelled illustrative.
India Basin's Oct 2024 design-standards amendment (draft) changes no heights; the 2018
Figure 5-3 limits stand.

## 2026-10-03 (Milestone 3: official records for every project)

Every project record other than Potrero was rewritten from the official findings in
`docs/official-research/` (checked 2026-10-02): official values in, conflicts settled by the
newest official document, press-only facts and their sources moved to each record's
`reported` object, `unsourced` removed (Mission Bay's figures are now official). Stage changes:
- **india-basin**: distressed → entitled (no official record of the default; private site has no issued permits).
- **parkmerced**: distressed → entitled (no official record of the receivership).
- **balboa-reservoir**: entitled → construction (DBI first construction documents for Buildings E and A).
Notable corrections: Candlestick groundbreaking Sept 9, 2026 (not 10) and office 2.8M sq ft;
Mission Rock Phase 1 finished 2025; Piers 30–32 split July 2025, Seawall Lot 330 application 568
homes; Treasure Island density increase not approved; Willow Village 1,730 homes; Alameda Point
1,300-home cap; Brooklyn Basin 3,700 homes; Concord 12,272 homes; Coliseum sold as one closing.
Each record's `sources` also cites the GIS layer its boundary comes from.

## 2026-10-03 (official records and the Design for Development)

For **potrero-power-station**, from official records read once network access opened:
- `program.affordablePct`: null → **30**, from the recorded development agreement (Recital H).
- `stage`: entitled → **partial**: DBI permit 202212229038 for the Sophie Maxwell Building
  (8 stories, 105 affordable homes) was marked complete Aug 28, 2026 (permit dates count for
  stages, Matthew 2026-10-03).
- `developer`: **California Barrel Company LLC (Fifth Space)**, as named in Addendum 2.
- `timeline`: Board approval corrected to Apr 21, 2020 (Ordinance 62-20, effective May 24,
  not May 25); added Station A, office allocation and phasing actions (2020–2022), the
  Sophie Maxwell permits, UC Regents' Block 2 approval, Addendum 2 and the 2026 amendment
  hearings.
- Massing: block height limits traced from the D4D's Figure 6.2.3 (see docs/DECISIONS.md).
- `verify`: now the Sophie Maxwell opening date, UCSF construction start and the Board's
  final action on the 2026 amendments.

## 2026-10-02 (official sources only)

Matthew asked for official sources only. For **potrero-power-station**:
- Press-only facts moved into a new `reported` record that the map never shows: the
  "partly built" stage and its stage note, the developer name "Fifth Space (formerly Associate Capital)",
  the 30% affordable share, the 2025 and 2026 timeline entries, and the press sources.
- `stage`: partial → **entitled**, the latest status official sources confirm so far.
  It returns to "partly built" once city or UC records confirm the construction and the completed building.
- `stageNote`: rewritten from the minutes (EIR certified and Design for Development
  approved Jan 30, 2020) and the existing sfplanning.org source (agreement effective May 25, 2020).
- `developer`: **California Barrel Company, LLC (Associate Capital)**, the Development
  Agreement party and project sponsor named in the minutes of Jan 30, 2020 and Sept 5, 2019.
- `timeline`: added the Jan 30, 2020 Planning Commission approvals.
- `program.affordablePct`: 30 → null (moved to `reported` until the Development Agreement is read).
- `verify`: added the affordable share, construction status, approved block heights and the
  status of the 2025–26 amendments.
- Massing: the 2018 Draft EIR blocks and the Sophie Maxwell Building are no longer drawn;
  only the 300-ft stack remains.

## 2026-10-02 (official sources)

Matthew asked for official sources only. Checked against the San Francisco Planning
Commission's minutes of January 30, 2020, the hearing that certified the EIR and
approved the Design for Development (Motion 20638), the Special Use District, the
zoning map change and the Development Agreement:
https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200130_cal_min.pdf

- **potrero-power-station, program.officeLabSqft:** 1,600,000 → **1,459,978** (gross sq ft
  of "commercial office/laboratory use", minutes items 13 and 14a, p. 9). The 1.6 million
  figure came from press coverage and has no official source.
- **potrero-power-station, program.retailSqft:** null → **99,464** (gross sq ft of
  "commercial-retail use", same items).
- **potrero-power-station, sources:** added the minutes.
- Confirmed by the same minutes, unchanged: 2,601 homes, 250 hotel rooms, 6.9 acres of
  open space, approximately 29 acres. The minutes also give the approved height range
  for new buildings (65 to 240 ft) and the new height district (65/240-PPS on map HT08).

`lastVerified` was not changed: the rest of the record has not been re-checked yet.

## 2026-10-02

- **potrero-power-station, camera:** added (`center` [-122.3838, 37.7566], zoom 16.4,
  pitch 58, bearing -30). A display setting, not a fact; tuned from screenshots.
- **potrero-power-station, traced geometry:** new `data/boundaries/potrero-power-station.geojson`
  (site and five sub-areas, Draft EIR Fig. 2-2, p. 2-6) and
  `data/massing/potrero-power-station.geojson` (illustrative height districts, Fig. 2-7,
  p. 2-20; stack 300 ft, pp. 2-7 and 4.D-8). Source:
  https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf
- **schema:** projects may carry an optional `camera`.

`lastVerified` was not changed: no project facts were re-checked.

## 2026-10-01

Approved by Matthew after the planning audit (`docs/PLANNING-AUDIT.md`).

- **potrero-power-station, summary and massingNotes:** "brick stack" changed to
  "concrete boiler stack". Source: Potrero Power Station Mixed-Use Development Project
  Draft EIR, Oct 2018, p. 2-7 ("the adjacent 300-foot tall concrete boiler exhaust
  stack") and p. 4.D-8 ("The reinforced concrete Boiler Stack ... at 300 feet in
  height"). The brick structure on the site is Station A's Turbine Hall (p. 4.D-7).
  https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf
- **potrero-power-station, acresNote:** the 29 vs 21 acre question is answered by the
  same Draft EIR, p. S-2: an approximately 29.0-acre site including a 21-acre Power
  Station sub-area. `acres` stays 29. The Draft EIR was added to `sources`. The
  "Final site acreage" verify item stays, because the 2026 amendments could change it.
- **mission-bay:** `acres` (303), `program.homes` (6,500), `developer` and the 1998
  timeline entry are moved into a new `unsourced` object, so the map never shows
  them. The research notes said these were approximate figures from general knowledge.
  They come back once each one has a citable source.

`lastVerified` was not changed. Only the facts listed above were re-checked.
