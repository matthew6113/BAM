# Changelog

Data changes to `data/projects.json` and other project facts, newest first. Each entry
says what changed, why and against which source. Code changes live in git history.

## 2026-10-07 (official-source pass: west San Francisco and HOPE SF)

Each project's held-back press facts (`reported`) and open questions (`verify`) were checked against
official records. Findings, with URLs, pages and quotes: `docs/official-research/update-2026-10-07-sf-west.md`.
`lastVerified` is unchanged, because only these items were re-checked, not whole records.

- **treasure-island:** developer now names its owners (Stockbridge, Wilson Meany, Kenwood Investments,
  Lennar; Board Budget and Legislative Analyst, 2024), replacing the press's "TIDG" in `reported`. Homes
  completed: more than 1,200 by May 2026 (City Administrator), up from about 1,000. The press's
  "phase one complete in July 2026" is contradicted: Planning says Major Phase 1 builds out through 2027.
  It and its timeline entry are dropped. Added: the 2016 start of Stage 1 infrastructure (TIDA schedule),
  the Bay FC facility permit (Jan 6, 2026), TIDA's unit-increase schedule (Board action targeted for
  November) and 490 Avenue of the Palms switching to rentals (TIDA, Sept 2026).
- **stonestown:** the 30 acres are "parking lots and streets" (Mayor's Office), so `reported.acresNote` is
  removed. The affordable options are now spelled out from the development agreement (up to three parcels for
  100% affordable buildings, inclusionary homes, or a fee on up to 390 homes). Added the Board's
  approval of the financing plan (Resolution 36-26, Jan 27, 2026).
- **balboa-reservoir:** the educator housing is confirmed by the adopted development agreement: about 150
  homes, with City College first priority and SFUSD second. The press note is removed, and the open-space split
  is added (park 2.0, SFPUC 1.2, paseos 0.8 acres).
- **parkmerced:** no official record of the default, receivership or takeover, so the stage stays
  entitled. Added Planning's Sept 2024 finding of no construction since 2011. Phase 1 affordable
  homes corrected to 48 + 37 on site plus about $59.4M in fees, and heights corrected to the zoning's
  45–145 ft (Ordinance 91-11; the 35-ft figure came from the 2010 staff report).
- **potrero-hope-sf:** affordable homes now 800 (about 619 replacement + 200 tax-credit; MOHCD, 2025).
  Phase 3 demolition has started: 23 permits (153 units) issued in April 2026, 19 marked complete by
  Sept 1, 2026 (DBI, re-checked today). The City's 2022 schedule (last phase in 2034) is added.
- **sunnydale-hope-sf:** EIR/EIS certified July 9, 2015 (Motion 19409), with CEQA findings Nov 17, 2016;
  the buildings are Block 6 (242 Hahn St) and Block 7 (65 Santos St). The development agreement counts
  694 market-rate and 1,074 affordable homes. All verify items are resolved.
- **schlage-lock:** the agreement took effect Feb 27, 2015 for 15 years. The 2009 ordinances were finally
  passed Apr 28, 2009. Grading began in 2016 and site preparation finished in early 2019. Zone 1 is about
  20 acres (parcels listed). The Dec 2019 filings were three buildings, not two (146, 152 and 258 homes).

## 2026-10-07 (BART station-area housing, added)

New project `bart-station-housing`, added at Matthew's request as one program-level entry: BART's
housing on its own station land where the work isn't finished. No single site reaches the usual
1,000-home bar (see `docs/official-research/candidates-transit-south-bay.md`). Re-checked BART's
upcoming and completed TOD pages today: Millbrae's Gateway is now listed as completed (2025), so it
is left out with the other 15 delivered stations (4,232 homes, 874,000 sq ft). Six sites are drawn:
West Oakland (762 homes; 240 affordable under construction since Sept 14, 2026), Lake Merritt (557
homes and up to 500,000 sq ft of office; the senior building is under construction), North Berkeley
(739 homes, entitled Dec 2024), the Ashby West Lot (up to 600 homes; developer selected), El Cerrito
Plaza (743 homes; first building under construction since Nov 2025) and Amador Station at West
Dublin/Pleasanton (300 affordable homes; awaiting funding). Homes total 3,701, an explicit sum of the
official per-site figures (Ashby at its "up to" figure). Walnut Creek's last phase, Fremont, Bay Fair
and Richmond are named in the record but not drawn: no official source places a defined project on a
parcel yet.

Boundary: one part per site from BART's own TOD Work Plan GIS layer (BART's ArcGIS organisation,
added to `src/projects/official.ts`), selected by BART's "in progress" status or by APNs named in City
of Oakland and City of Dublin records. Massing: West Oakland (2020 revised PDP), Lake Merritt (2021 tract
map and zoning table) and El Cerrito Plaza (2024 approved master plan) are traced from the approved plans
with their heights; North Berkeley, Ashby and Amador Station are illustrative height-limit envelopes (80 ft
R-BMU, 90 ft at Amador). Conflicts between official documents (Lake Merritt 557 vs 636 homes, start date,
El Cerrito heights) are in the record's `verify` list. Pipeline: `bam_pipeline.sites.bart_station_housing`
(in `make sites`). The landing camera frames all six stations from El Cerrito to Dublin (centred on the
sites' centroid, as the camera test requires); because the sites are only a few pixels across at that
scale, a site whose centroid falls more than 1 km off it now gets one regional marker per station, and
those markers stay visible (slightly larger) while the program is open. No other project's markers change.

## 2026-10-06 (project photos and official links)

Project photos, approved by Matthew: one openly licensed or public-domain photo for each of 23
projects (18 downloaded so far; Wikimedia rate-limited the other five, which `make photos` fetches), from Wikimedia Commons (`data/photos.json`, research in `docs/images/`). `make photos`
reads each file's license and author from its own Commons page, refuses anything outside CC0,
public domain, CC BY and CC BY-SA, and copies a resized version into `public/photos/`, so the site
never hotlinks. Parkline's approved photo (an abstract atrium detail) was dropped at Matthew's
request. The panel shows each photo after the summary with its caption and credit. Ten
projects have no usable open photo yet. Renderings still need written permission; the outreach
list is `docs/images/PERMISSIONS.md`.

Official links: mission-bay's `sfocii.org/mission-bay` returned 404 and is replaced by the OCII
Mission Bay North and South overview pages. Added the project pages for mission-rock (Port),
india-basin, stonestown and balboa-reservoir (SF Planning) and sonoma-developmental-center
(Permit Sonoma). Each was opened on 2026-10-06.

## 2026-10-06 (the nine new projects on the map)

All nine new projects now have site boundaries and massing or land-use zones, each source added
to `sources` and described in `massingNotes`. Notable calls: Mare Island's boundary uses Vallejo's
2005 specific plan area (the SP-4 zoning area runs over the bay); Schlage Lock's historic office
building is outlined without a height (no official figure); Middlefield Park's O1 height conflict
(125 vs 115 ft) and Berryessa's height diagram source are in `verify`.

## 2026-10-06 (Esmeralda, Cloverdale)

**esmeralda** added at Matthew's request: the Esmeralda Specific Plan in Cloverdale (up to 605
homes and a 160-room hotel on about 261 acres; below the usual 1,000-home bar), from City of
Cloverdale records (`docs/official-research/candidates-esmeralda.md`). `cloverdale.net` and
`cloverdale.granicus.com` join the official hosts. The City Council hearings are Oct 7 and 14, 2026.

## 2026-10-06 (eight new projects)

Added at Matthew's request after official-source research (`docs/official-research/candidates-*.md`,
checked 2026-10-05): **tasman-east**, **sunnydale-hope-sf**, **potrero-hope-sf**,
**middlefield-park**, **schlage-lock**, **berryessa-flea-market**, **mare-island** and
**sonoma-developmental-center** (990 homes, just under the 1,000-home bar). BART station-area
housing (no single site reaches 1,000 homes) and the East Whisman Precise Plan (a zoning plan,
covered by Middlefield Park) were not added. `cityofvallejo.net` and `permitsonoma.org` (Permit
Sonoma) join the official hosts. The records are on file; they go on the map once their boundaries
are drawn.

## 2026-10-05 (Milestone 4: land-use zones for the plan-scale projects)

**moffett-park**, **north-bayshore**, **concord-naval-weapons-station**, **suisun-expansion** and
**brisbane-baylands** get land-use zones (`data/landuse/`), not buildings, per the SPEC; each
plan document is added to `sources` and `massingNotes` says what was drawn. Suisun's zones are
proposed (NOP) and Brisbane's are from the draft 2026 specific plan, both labelled so. Brisbane
also gets the Bayshore Roundhouse landmark (about 25 ft, Council staff report). **north-bayshore**'s
boundary is now traced from the master plan's project-area line (189.3 acres as drawn, with
internal streets and the Shoreline Amphitheatre), replacing the parcel assembly that cut off
about 7 acres of plan residential (Matthew, 2026-10-05).

## 2026-10-05 (Milestone 4, batch 4: The Rise, Alameda Point, Brooklyn Basin, Oakland Coliseum)

`massingNotes` updated and each massing source added to `sources` for **the-rise**,
**alameda-point** and **brooklyn-basin**. **oakland-coliseum** gets no massing: no plan is filed
or approved, and its D-CO-2 zoning (159 ft above mean sea level, Ord. 13302 and 13894) covers the
whole site; both ordinances are now cited. **downtown-west** block E1 is drawn at the approved
Development Agreement's 260 ft (Matthew: the more recent document wins). `apps.cupertino.org`
(the City of Cupertino's document server) added to the official hosts.

## 2026-10-03 (Milestone 4, batch 3: Parkmerced, Parkline, Willow Village, Related Santa Clara, Downtown West)

`massingNotes` updated and each massing source added to `sources` for **parkmerced**,
**parkline**, **willow-village**, **related-santa-clara** and **downtown-west**. Related Santa
Clara now cites CEQA Addendum 4 (Res. 25-9465) for its 190-ft cap. **downtown-west**: the
boundary now includes the two DC(PD) zoning polygons filed as "19039" (62.8 acres as drawn,
was 58.3); its heights come from the October 2020 draft design standards because the approved
2021 version could not be retrieved, so a `verify` item was added.

## 2026-10-03 (Piers 30–32 removed)

**piers-30-32** removed from the map at Matthew's request: the record, its boundary and its
massing are deleted and the project is listed under `_meta.dropped`. 24 projects remain.

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
