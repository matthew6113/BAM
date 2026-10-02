# Changelog

Data changes to `data/projects.json` and other project facts, newest first. Each entry
says what changed, why and against which source. Code changes live in git history.

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
