# Changelog

Data changes to `data/projects.json` and other project facts, newest first. Each entry
says what changed, why and against which source. Code changes live in git history.

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
