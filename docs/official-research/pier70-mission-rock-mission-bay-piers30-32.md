# Official-source findings: Pier 70, Mission Rock, Mission Bay, Piers 30–32

Checked 2026-10-02 against documents downloaded from SF Planning's document store and read in full text (local copies go in `data/raw/official/`, git-ignored). Page numbers are PDF page numbers.

Abbreviations for the sources:
- **CPC-170824**: https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20170824_cal.min.pdf. Header says "DRAFT – Meeting Minutes". 2017 minutes in the bucket use the `_cal.min.pdf` suffix, not `_cal_min.pdf`.
- **CPC-171005**: https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20171005_cal.min.pdf
- **CPC-YYYYMMDD** (other dates): https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/YYYYMMDD_cal_min.pdf
- **P70-DEIR**: https://sfplanning.s3.amazonaws.com/sfmea/Pier70DEIRFull.pdf. Pier 70 Mixed-Use District Project Draft EIR, Dec 21, 2016, Case 2014-001272ENV. The file is 179 MB.
- **MR-DEIR2**: https://sfplanning.s3.amazonaws.com/sfmea/MissionRock_Ch_2_ProjectDescription.pdf. SWL 337 & Pier 48 Draft EIR Ch. 2, April 2017, Case 2013.0208E.
- **HE-B1**: https://sfplanning.s3.amazonaws.com/archives/sfhousingelement.org/files/AppendixB1.pdf. Housing Element 2022 Sites Inventory Appendix B1, "ADOPTED - January 2023". It profiles each development agreement (DA) project. It is the newest official program figures I found for Pier 70, Mission Rock and Mission Bay.
- **NOP-2012**: https://sfplanning.s3.amazonaws.com/sfmea/2012.0718E_NOP.pdf. NOP for the Warriors arena at Piers 30–32/SWL 330, Dec 5, 2012. That project is superseded, so use this only for site facts.

Unreachable: sfport.com, sfgov.org, sfbos.org, sfgov.legistar.com, sfocii.org and onesanfrancisco.org (curl returned 000). Nothing from those hosts is confirmed here.

---

## pier-70

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 28 | 28-acre site (inside a 35-acre rezoned project site) | CONFIRMED | P70-DEIR p. S.3; CPC-170824 item 14, p. 7 | "The “28-Acre Site” is an approximately 28-acre area" |
| acresNote (wider area ~69 ac) | ~69 acres | 69 acres (DEIR); "70-acre" (HE-B1) | CONFIRMED | P70-DEIR p. S.1; HE-B1 p. 20 | "The Pier 70 area (Pier 70) encompasses 69 acres" |
| program.homes | 2,000 ("2,000+") | Prop F: 1,000–2,000. EIR/CPC: 1,645–3,025 max. HE-B1 (2023): up to 2,150 | CONFLICT (newest official is "up to 2,150") | HE-B1 p. 20; CPC-170824 item 15a, p. 9; P70-DEIR p. 2.8 | "will generate up to 2,150 dwelling units" |
| affordablePct | null | 30% | NEW (official) | HE-B1 p. 20; P70-DEIR p. 2.8 (Prop F) | "30% of which will be affordable" / "Provision of 30 percent of all new housing units at below-market rates" |
| commercialSqftTotal | 2,000,000 | Prop F: 1M–2M sq ft commercial/office. EIR/CPC: max 1,102,250–2,262,350 gsf office, plus 494,100–518,700 gsf RALI | PARTLY CONFIRMED (matches Prop F upper bound; approved max range goes higher) | P70-DEIR p. 2.9; CPC-170824 item 15a | "Creation of between approximately 1,000,000 and 2,000,000 square feet of new commercial and office space" |
| openSpaceAcres | 9 | 9 acres (Prop F/EIR/CPC 2017); 6.5 acres "waterfront parks and open space" (HE-B1 2023) | CONFLICT between official docs (probably counted differently; unresolved) | CPC-170824 item 15a; P70-DEIR p. S.4; HE-B1 p. 20 | "nine acres of publicly-owned open space" vs "6.5 acres of waterfront parks and open space" |
| heights | "verify vs D4D" | New buildings 50–90 ft; zoning 90-X/65-X. 2020 D4D amendment allows 9 stories (max height unchanged) | CONFIRMED (range) | CPC-170824 item 14, p. 8; CPC-20200206 item 10, p. 4 (Motion 20648) | "New buildings would range in height from 50 to 90 feet, consistent with Proposition F" |
| Retained historic buildings | Building 12 and others | Buildings 2, 12 and 21 rehabilitated; Irish Hill remnant retained; 7 demolished | CONFIRMED (adds detail) | P70-DEIR p. S.3–S.4 | "three contributing resources (Buildings 2, 12, and 21) would be rehabilitated" |
| developer | Brookfield Properties | Brookfield, named "the Developer" in 2023. Original DA party was "FC Pier 70, LLC" (Forest City) | CONFIRMED ("Brookfield") | HE-B1 p. 20; CPC-170824 item 15f | "distributed to the City in April 2022 by the Developer, Brookfield" |
| timeline 2014-11 Prop F | Prop F, Nov 2014, taller buildings | Prop F, Nov 4, 2014, 40 → 90 ft on the 28-Acre Site | CONFIRMED | P70-DEIR p. 2.7–2.8 | "On November 4, 2014, the San Francisco electorate approved Proposition F" |
| timeline 2017–2018 approved | "Project approved; first phase of construction begins" | CPC certified FEIR and approved on Aug 24, 2017 (Motions 19976, 19977, 19980; Res. 19978, 19979, 19981). BoS approved DDA Dec 15, 2017. Phase 1 submittal presented to CPC Jan 25, 2018. Construction start not in any official doc I reached | APPROVAL CONFIRMED; "construction begins" UNCONFIRMED | CPC-170824 pp. 8–12; CPC-20180125 item 11, p. 6 | "On December 15, 2017, the Board of Supervisors approved the Disposition and Development Agreement (DDA)" |
| stageNote: no vertical construction | (no new construction expected in 2026) | As of 2023, Phase 1 was in a permitted "down market delay" | SUPPORTS (as of 2023) | HE-B1 p. 20 | "Phase 1 of the Pier 70 project is currently in down market delay as permitted by the agreements" |
| stageNote: Phase 1 streets and Building 12 done; General Catalyst ~70k sf (2026-01) | — | none reachable | UNCONFIRMED → `reported` | — | — |
| July 2026 density proposal (~600 homes, ~420-unit building, Phase 1 ≈700, 2027 start) | — | none reachable | UNCONFIRMED → `reported` | — | — |
| verify: "Prop F year and details" | — | Resolved: Nov 4, 2014; 9 ac parks; 1,000–2,000 homes; 30% BMR; 1–2M sf commercial | CONFIRMED | P70-DEIR p. 2.8 | see above |

Two later D4D amendments: Motion 20648 (CPC-20200206, residential up to nine stories, height maximums unchanged) and Motion 21086 (CPC-20220303 p. 9, Retail/Office definitions; "would not alter overall building height maximums, parcel designations, or the overall development capacity"). Neither changes the program numbers above.

**Boundary leads**
- 28-Acre Site: "Assessor’s Block 4052/Lot 001 and Lot 002 and Block 4111/Lot 003 and Lot 004" (P70-DEIR p. S.3).
- The rezoning items list 4052/001 (partial), 4111/004 (partial), 4110/001 and 008A, and 4120/002. The 4110 and 4120 parcels are the Illinois Parcels and are not part of the 28 acres (CPC-170824 item 15c).
- Bounds: "between 20th, Michigan, and 22nd streets and San Francisco Bay".
- P70-DEIR figures: 2.1 Project Location (p. 2.6), 2.5 SUD Land Use Program (2.22), 2.6 Rehab/Retention/Demolition (2.24), 2.7/2.8 Land Use Plans (2.30/2.32), 2.13 Proposed Height Limits Plan (2.40), 2.15 Proposed Open Space Plan (2.46).
- The draft EIR figures may differ from the adopted D4D (2017, amended 2020 and 2022). The D4D itself was not found in the bucket.

**Suggested edits to projects.json**
- `program.homes`: 2150. Note: "Up to 2,150 homes (Housing Element 2023 profile); EIR analyzed 1,645–3,025."
- `program.affordablePct`: 30.
- Open space: either keep 9 and add a note about the 2023 Housing Element's 6.5-acre figure, or set null until the DDA or D4D is checked.
- `commercialSqftTotal`: keep 2,000,000 with the note "Prop F: 1–2M sq ft; approved max up to ~2.26M gsf office". Or set officeLabSqft to null.
- Timeline: replace "2017–2018" with:
  - "2017-08: Planning Commission certifies EIR and approves (Motions 19976/19977/19980)"
  - "2017-12: Board of Supervisors approves the DDA"
  - "2018-01: Phase 1 submittal presented"
  Drop "construction begins" or move it to `reported`.
- Add official sources: CPC-170824, P70-DEIR, HE-B1, CPC-20180125.
- Move these to `reported`: stageNote items (Building 12 done, General Catalyst), the July 2026 proposal, and `nextMilestone`.

**Still open**
- Delivered buildings list and Building 12 status.
- DDA/DA Phase 1 contents.
- The 9 vs 6.5 acre open-space discrepancy.
- Official record of the 2026 density amendment (not reachable).

---

## mission-rock

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 28 | 28 acres | CONFIRMED | MR-DEIR2 p. 2-1; HE-B1 p. 20 | "The 28-acre project site consists of Assessor’s Block 8719/Lot 002, Block 8719/Lot 006, and Block 9900/Lot 048" |
| program.homes | 1,200 | 1,000–1,600 (EIR/CPC 2017); "up to 1,300" (HE-B1 2023) | CONFLICT | HE-B1 p. 20; CPC-171005 item 14, p. 12 | "The project will generate up to 1,300 housing units" |
| affordablePct | 40 | 40% | CONFIRMED | MR-DEIR2 p. 2-27; HE-B1 p. 20 | "restrict 40 percent of the onsite units to inclusionary affordable housing targets" |
| officeLabSqft | 1,400,000 | 972,000–1.4 million gsf commercial | CONFIRMED (as the maximum) | CPC-171005 items 14 & 15a–d; MR-DEIR2 Table 2-3 p. 2-22 | "972,000 to 1.4 million gsf of commercial uses" |
| retailSqft | 200,000 | 241,000–244,800 gsf active/retail and production | CONFLICT | CPC-171005 item 14; MR-DEIR2 Table 2-3 | "241,000 to 244,800 gsf of active/retail and production uses" |
| openSpaceAcres | null | ~8.0 acres total (5.4 net new) | NEW (official) | CPC-171005 item 14; HE-B1 p. 20 | "for a total of approximately 8.0 acres of open space" |
| notes: Pier 48 rehab | yes | ~261,000 gsf of Pier 48 rehabilitated | CONFIRMED | CPC-171005 item 14 | "rehabilitation of approximately 261,000 gsf of Pier 48" |
| notes: new parking structure | yes | Block D2 garage, 837,200 gsf / 2,300 spaces, plus a 700-space garage under Mission Rock Square | CONFIRMED (as planned) | MR-DEIR2 Table 2-3 p. 2-22 | "Parking Structure (Block D2) 837,200 gsf" |
| notes: "5-acre China Basin Park delivered" | 5 acres | 4.4 acres planned, including the existing 2.2 acres | CONFLICT (size); delivery UNCONFIRMED | MR-DEIR2 Table 2-6 p. 2-38 | "China Basin Park 4.4" |
| massing: 11 blocks, 3 at 240 ft, 2 at 190 ft | from forum posts | 11 blocks A–K. A, D (D1), F: 240 ft (~23 stories). C, G: 190 ft. B: 120. E: 90. H, I, J: 90 (commercial) or 120 (residential). K: 120. D2 garage ~100 ft. Rooftop elements up to +20 ft (+40 ft on F) | CONFIRMED (heights from the Draft EIR; adopted Design Controls not checked) | MR-DEIR2 Table 2-4 p. 2-23, text p. 2-34 | "the residential buildings on Blocks A, D1, and F could reach a maximum building height of 240 feet (approximately 23 stories)" |
| timeline 2015 voter approval | 2015 | Prop D, Nov 3, 2015 | CONFIRMED | MR-DEIR2 p. 2-70; CPC-171005 item 14 | "passage of Proposition D, the Mission Rock Affordable Housing, Parks, Jobs, and Historic Preservation Initiative, on November 3, 2015" |
| (missing) approvals | — | CPC certified FEIR Oct 5, 2017 (Motion 20017; findings Motion 20018; Res. 20019–20021). BoS DA (File 171313) and SUD (File 170940) "PASSED Second Read" by Mar 1, 2018 report. CPC-20190725 says "In 2018, the Board of Supervisors approved the [DA] and [DDA]" | NEW (official) | CPC-171005 pp. 12–16; CPC-20180301 p. 4; CPC-20190725 item 10, p. 7 | "171313 Development Agreement - Seawall Lot 337 Associates, LLC ... PASSED Second Read" |
| Phase 1 scope (four buildings) | four buildings A, B, F, G | Phase 1 submittal: four pads, ~630 units, 550,000 gsf office, ~65,000 gsf retail. Block letters not in the minutes | CONFIRMED (count); letters UNCONFIRMED | CPC-20190725 item 10, p. 7 | "preparation of four development pads that will support ... approximately to 630 residential units, 550,000 gsf of office, and approximately 65,000 gsf of retail space" |
| timeline 2020 construction under way | 2020 | Only a 2021 statement that Parcel G "had actually received its building permit" | UNCONFIRMED for 2020 | CPC-20210909 p. 7 | "Parcel G in the Mission Rock development ... had actually received its building permit" |
| timeline 2023 Phase 1 complete | 2023 | 2023 projection only: 537 units under construction, 283 expected 2023 and 254 expected 2024 | UNCONFIRMED (official projection points to 2023–24) | HE-B1 p. 20 | "537 units under construction at Mission Rock, with 283 expected to be complete in 2023 and 254 expected to be complete in 2024" |
| stageNote: Visa ~300k sf HQ; two 23-story towers | — | Blocks A and F allowed up to 240 ft (~23 stories). Visa and actual built floors not found | UNCONFIRMED → `reported` | — | — |
| remaining phases | "no announced start" | 2023: Phase 2 (358 units, projected 2026) and Phase 4 (320 units, projected 2029) "in early planning stages" | NEW (2023, likely stale) | HE-B1 p. 20 | "Phase II and IV are in early planning stages" |
| developer | Mission Rock Partners (Giants + Tishman Speyer) | Sponsor "Seawall Lot 337 Associates, LLC". Tishman Speyer not named in any doc I reached | PARTLY UNCONFIRMED | MR-DEIR2 p. 2-1 | "The project sponsor (Seawall Lot 337 Associates, LLC)" |

**Boundary leads**
- APNs: 8719/002, 8719/006, 9900/048. CPC items list only 8719/006 and 9900/048.
- Components: 14.2-ac Seawall Lot 337, 0.3-ac Parcel P20 strip, 6.0-ac Pier 48, existing 2.2-ac China Basin Park, and 5.4 ac of streets (MR-DEIR2 p. 2-1).
- Bounds: "east of Third Street, between China Basin Channel and Mission Rock Street".
- MR-DEIR2 figures: Project Site Location (p. 2-7); Figure 2-4 "Proposed Site Plan and Height Ranges" (p. 2-21), which is the block layout and heights; Figures 2-7 and 2-8, height assumptions (pp. 2-33, 2-34).
- Adopted Mission Rock Design Controls (CPC Res. 20021) not located in the bucket.

**Suggested edits to projects.json**
- `program.homes`: 1300 ("up to"). Note: "EIR analyzed 1,000–1,600."
- `retailSqft`: 241000–244800. Use 244800 with the note "active/retail and production, max".
- `openSpaceAcres`: 8.
- Notes: change "5-acre China Basin Park" to "China Basin Park expanded to ~4.4 acres (planned)". Move "delivered" to `reported`.
- `massingNotes`: replace the forum citation with the MR-DEIR2 Table 2-4 per-block heights, labeled "Draft EIR heights; verify against adopted Design Controls".
- Timeline:
  - Make "2015" into "2015-11: Prop D".
  - Add "2017-10: Planning Commission certifies EIR, approves zoning, DA, Design Controls".
  - Add "2018: Board of Supervisors approves DA/DDA".
  - Add "2019-07: Phase 1 submittal (4 pads, ~630 homes, 550k sf office)".
  - Move "2020 construction" and "2023 complete" to `reported` unless a Port source is reached.
- `officialLinks` and `sources`: add CPC-171005, MR-DEIR2, HE-B1, CPC-20190725. Drop bisnow, sfyimby, skyscraperpage and socketsite to `reported`.
- Developer: keep the "Seawall Lot 337 Associates, LLC" name official. Put "Giants + Tishman Speyer" in `reported`.

**Still open**
- Phase 1 completion date and building letters.
- Visa headquarters size.
- Adopted Design Controls heights.
- Port Phase 1 docs (sfport.com unreachable).

---

## mission-bay

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres (unsourced 303) | 303 | 303 acres | CONFIRMED | P70-DEIR p. 4.A.18 and p. 4.B.9; HE-B1 p. 4 | "The 303-acre Mission Bay Redevelopment Plan area" |
| homes (unsourced 6,500) | 6,500 | 6,535 units incl. 1,916 affordable (HE-B1 2023). The 1998 plan envisioned ~6,000 | CONFIRMED approximately; use 6,535 | HE-B1 p. 4; P70-DEIR p. 4.B.9 | "includes 6,535 new residential units – both rental and ownership – including 1,916 affordable units on the 303-acre site" |
| plan adoption year (unsourced 1998) | 1998 | 1998 | CONFIRMED | P70-DEIR p. 4.A.18; HE-B1 Table 1 ("Year Entitled 1998") | "The plan was adopted in 1998." |
| openSpaceAcres | null | 41 acres of parks | NEW (official) | HE-B1 p. 4 | "The project also includes 41 acres of parks" |
| office/R&D (original plan) | null | 4.4M gsf office/research/commercial; ~500,000 gsf retail (1998 plan as described in the 2016 DEIR; later plan amendments may supersede) | NEW (older) | P70-DEIR p. 4.A.18 | "4.4 million gsf of office/research/commercial space, 500,000 gsf of retail space" |
| includes UCSF campus, Chase Center | yes | UCSF research campus is in the plan. Warriors event center "on an approximately 11-acre site within the Mission Bay Redevelopment Plan Area", approved Dec 2015 | CONFIRMED (plan/approval; not the Chase Center name) | P70-DEIR p. 4.A.18, 4.B.9 | "The Golden State Warriors Event Center ... was approved in December 2015" |
| stageNote: "OCII ... ten more parks ... eight years" | — | onesanfrancisco.org unreachable; not in the `official.ts` host list | UNCONFIRMED | — | — |
| stageNote: largely built out | yes | "Most of the planned units are built out with mostly low income affordable units remaining" (2023) | CONFIRMED | HE-B1 p. 4 | as quoted |
| remaining housing | — | Remaining 2 affordable parcels: proposed density increase "by up to 815 units (for a total of 980)"; 21 market-rate units on the Warriors site | NEW (2023) | HE-B1 p. 4 | as quoted |
| developer / master developer history | — | not found (no Catellus mention in reachable docs) | UNCONFIRMED | — | — |

Note: HE-B1 also says "over 25,000 square feet of commercial". That looks like an error in the source, so don't use it.

**Boundary leads**
- Mission Bay South: "generally bounded by Mariposa Street on the south, Interstate 280 on the west, Mission Creek on the north, and San Francisco Bay on the east" (CPC-20201119, item 13a).
- Mission Bay North boundary not found. The official boundary is likely on SF Planning or OCII GIS; redevelopment area layers are worth probing.

**Suggested edits to projects.json**
- Move these out of `unsourced`:
  - `acres`: 303
  - `program.homes`: 6535
  - `affordableHomes`: 1916
  - `openSpaceAcres`: 41
  - Timeline "1998: Mission Bay North and South redevelopment plans adopted"
- Sources: add HE-B1 and P70-DEIR (pp. 4.A.18).
- Keep `developer` in `unsourced`.
- Flag the stageNote "ten parks / eight years" as unverified, or add onesanfrancisco.org (City Capital Planning) to the official host list after Matthew decides.

**Still open**
- Master developer history.
- Whether the 980-unit density increase was enacted.
- Current OCII parks schedule.

---

## piers-30-32

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 15.3 | Piers 30–32 ~13 ac (lot size 12.7) plus SWL 330 2.3 ac. That is 15.3 from the rounded figures or 15.0 from the lot sizes | CONFIRMED approximately (2012 doc, superseded project, but site facts) | NOP-2012 p. 1 | "Lot Size: Piers 30‐32: 12.7 acres / Seawall Lot 330: 2.3 acres" |
| acresNote | ~13 ac pier + 2.3 ac SWL 330 | as above | CONFIRMED | NOP-2012 p. 1 | "approximately 13‐acre Piers 30‐32" |
| notes: 376k sf office, 30.7k retail, 45% deck removal, 700+ units | — | not reachable | UNCONFIRMED → `reported` | — | — |
| developer Strada (Strada-TCC) | — | not reachable | UNCONFIRMED | — | — |
| timeline 2021 ENA; 2024 BoS fiscal feasibility; 2026-03 Port split report | — | sfport.com and Legistar unreachable. A WebSearch summary named BoS File 240342 / Res. 247-24; I could not read it, so it is NOT confirmed | UNCONFIRMED | — | — |
| stage/stageNote (2026 split, piers paused) | — | not reachable | UNCONFIRMED | — | — |
| verify: SWL 330 unit count and approval status | — | nothing official reachable. CPC minutes 2015–2022 mention SWL 330 only as the 2019 SAFE Navigation Center | UNCONFIRMED | CPC-20190627 p. 8 | "SAFE Navigation Center at Seawall Lot 330, which would include 200 beds" |

**Boundary leads**
- APNs: Piers 30–32 are "9900/030; 9900/032". Seawall Lot 330 is "3770/002; 3771/002" (NOP-2012 p. 1).
- SWL 330 is "within a triangular‐shaped block bounded by Bryant Street ..." (NOP-2012 project description). It sits across The Embarcadero; the Watermark building is on the west end of that block.

**Suggested edits to projects.json**
- Keep `acres` 15.3 and the acresNote. Cite NOP-2012 as the official source for site size, labeled "site area from 2012 NOP".
- Move all program notes, developer, timeline and stageNote facts to `reported` until the Port's 2026-03 staff report (Item 11B) or the BoS resolution can actually be fetched.
- The sfport.com PDF already in `sources` is an official host but unread by me. It may be fine if another agent reads it.

**Still open**
- Everything about the current Strada deal.
- Planning has no case or EIR file for it (the WebSearch summary pointed to Waterfront Plan EIR addenda, not found in the bucket).

---

## General notes

- More 2017 CPC minutes exist under `YYYYMMDD_cal.min.pdf`. 20170824, 0831, 0907, 0928, 1005 and 1012 returned 200; 0810, 0817 and 0921 returned 403. The 2014–2015 dates also use this pattern (e.g. 20141113_cal.min.pdf, 20150212_cal.min.pdf per WebSearch). The `cpcmin` set could be extended with it.
- Page numbers for CPC minutes are the printed "Page N of M" of the page the item sits on (the header precedes that page's content). DEIR pages are printed page labels.

---

# Update with full network access (2026-10-02)

Read from the Port, OCII, DataSF and Legistar once network access was broadened. Where this
section and the one above differ, this section is newer.

Main changes: Pier 70's Aug 2026 density proposal now has an official source (proposed, not
approved). Mission Rock Phase 1 finished in 2025, not 2023. The Piers 30–32 / Seawall Lot 330
split was approved in July 2025, not March 2026. Seawall Lot 330 has a 568-unit SB 423
application (May 2026). Pier 70's open-space conflict is resolved: 9 acres covers the 35-acre
SUD, 6.5 acres the 28-Acre Site.

## pier-70

Sources:
- P70-2608: Port Commission Item 11A, Aug 11, 2026. https://www.sfport.com/sites/default/files/2026-08/item_11a_p70_project_update_-_term_sheet_overview_-_information.pdf
- P70-MIN2608: minutes of that meeting. https://www.sfport.com/media/11558/download?inline
- P70-WEB: https://www.sfport.com/projects-programs/pier-70-28-acre-site
- P70-2008: Port Item 9B, Aug 7, 2020. https://www.sfport.com/sites/default/files/2021-08/Item%209B%20Pier%2070%20Project%20Update_final.pdf
- P70-JUL26: https://www.sfport.com/meetings/port-commission-july-14-2026

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| homes | 2,000 | 28-Acre Site 1,100–2,150 (SUD-wide 1,500–3,000) | CONFLICT (use up to 2,150) | P70-WEB; P70-2608 p2 | "1,100 - 2,150 residential units, 320+ (30%) affordable" |
| affordablePct | null | 30% approved; proposed "no less than 20%", 327 stand-alone affordable units | NEW | P70-WEB; P70-2608 p5 | "Adjust the Project-wide affordable housing rate from 30% to no less than 20%" |
| openSpaceAcres | 9 | 6.5 on the 28-Acre Site; 9 across the 35-acre SUD | RESOLVED (6.5) | P70-WEB; P70-2608 p2 | "6.5 acres of waterfront and upland parks" |
| July 2026 proposal | press | Proposed in Port staff report; Port and BoS action "by the end of this year or early next year" | NEW (proposed) | P70-2608 pp1–2, 6 | "Increase the height of certain residential parcels from 65 to 90 feet … could result in an additional 600 homes on site." |
| heights | — | Approved 65 and 90 ft; proposal raises some residential parcels 65→90 ft (Prop F maximum) | CONFIRMED + NEW | P70-2608 p6 | "which is the maximum allowed by ballot measure (Proposition F, 2014)" |
| Building 12 | done | Rehab completed Jan 2022; ~90% leased; General Catalyst not named | CONFIRMED (tenant UNCONFIRMED) | P70-2608 p3 | "In January 2022, Developer completed the rehabilitation of historic Building 12" |
| Phase 1 streets | done | Accepted 2024; Phase 1 parks and vertical buildings not started | CONFIRMED | P70-2608 pp1, 3 | "These improvements were accepted by the City and Port in 2024." |
| Phase 1 scope | ~700 homes (press) | 588 homes anticipated, 3 acres of parks, up to 460k sf commercial | CONFLICT | P70-2608 p3 | "an anticipated 588 residential units" |
| ~420-unit first building; 2027 start | press | Not in official docs; 2027 only as Brookfield's statement in minutes | UNCONFIRMED | P70-MIN2608 p7 | "positioning the project to advance beginning in 2027" |
| down-market delay | — | Hit the 60-month maximum June 2026; extended to Dec 26, 2026 | NEW | P70-2608 p4 | "extend the down market delay for an additional six months to December 26, 2026" |
| construction start | "2017–2018" | Demolition Aug 2018; construction Mar 2019; DDA dated May 2, 2018 | CONFIRMED (dates corrected) | P70-2608 p3; P70-2008 p3 | "began Phase 1 site preparation and demolition in August 2018, followed by construction in March 2019" |
| developer | Brookfield | "FC Pier 70, an affiliate of Brookfield Properties" | CONFIRMED | P70-WEB | — |

Boundary: DataSF Special Use Districts (`5yf5-ms5f`, "Public Domain U.S. Government"), feature
"Pier 70" (~35.6 ac = the 35-acre SUD). The 28-Acre Site is approximately the SUD minus the
block 4110 and 4120 parcels (DataSF Parcels `acdm-wktn`, ODC-PDDL); label it approximate.
Plan figure: https://www.sfport.com/files/2021-11/pier_70_sud_land_use_plan.pdf

Still open: adopted D4D parcel heights (https://www.sfport.com/media/8123/download?inline=, 95 MB);
which parcels go 65→90 ft.

## mission-rock

Sources:
- MR-2606: Port Item 11A and Res. 26-34, June 9, 2026. https://www.sfport.com/sites/default/files/2026-06/item_11a_mission_rock_phase_2_update_and_port_capital.pdf
- MR-MIN2606: https://www.sfport.com/media/11337/download?inline
- MR-2310: Port Item 8B, Oct 10, 2023. https://www.sfport.com/files/2023-10/101023_8b_mission_rock_budget_port_capital_parcel_lease_amendment_final.pdf
- DBI permits (DataSF `i98e-djp9`), blocks 8719A/B/C.

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| Phase 1 complete | 2023 | 2025 | CONFLICT | MR-2606 pp1, 3 | "Phase 1, completed in 2025, delivered 537 apartments (including 132 Below Market Rate units), 550,000 square feet of office space, substantial retail, the 5-acre China Basin Park" |
| Phase 1 buildings | — | A ("The Canyon") and F residential (537 units); B and G office/life science; TCOs G Jan-23, A May-23, B Jun-23 | CONFIRMED | MR-2310 p5 | "two primarily residential apartment buildings (Parcel A, "The Canyon", and Parcel F) totaling 537 units" |
| Visa HQ | ~300k sf | Parcel G is Visa's global HQ; size not stated | CONFIRMED (size UNCONFIRMED) | MR-2310 p5 | "Parcel G will serve as Visa's global headquarters." |
| tower heights | two 23-story | Permit applications: F 23 stories (258 units); A 24 stories (283 units); G 13; B 8 | CONFLICT | DBI 201910073784, 201910073782, 201910073785, 201910285744 | "to erect a 24 story, type 1a , 283 residential building" |
| homes | 1,200 | "up to 1,200" (2023); "at least 1,000" (2026) | CONFIRMED | MR-2310 p4 | "will include up to 1,200 units of new, rental housing" |
| affordablePct | 40 | 40% | CONFIRMED | MR-2310 p4 | "Forty percent (40%) of the residential units in Mission Rock will be below market rate." |
| officeLabSqft | 1.4M | 1.4M | CONFIRMED | MR-2606 p3 | "1.4 million square feet of new commercial and office space" |
| openSpaceAcres | null | 8 | NEW | MR-2310 p4 | "eight acres of parks and open spaces" |
| retailSqft | 200,000 | Phase 1 52,000 gsf; total not restated (DEIR 241,000–244,800) | UNCONFIRMED total | MR-2606 p3 | "52,000 gross square feet of retail space" |
| remaining phases | no start | $10M Port Phase 2 pre-development (Res. 26-34); construction "as early as 2027"; amendments to Port Fall 2026, BoS Fall 2026/Winter 2027 | CONFLICT (update) | MR-2606 pp2, 6 | "position Phase 2 to begin construction as early as 2027" |
| approvals | — | Port Res. 18-03 (Jan 2018); BoS Res. 42-18 (DDA), Ord. 33-18 (DA), Feb 2018 | NEW | MR-2606 p8 | "approved the DDA by Resolution No. 42-18 and … the Development Agreement … by Ordinance No. 33-18" |

Boundary: DataSF SUD layer `5yf5-ms5f`, feature "Mission Rock" (~27.7 ac vs official 28).

## mission-bay

Sources: OCII https://sfocii.org/mission-bay, https://sfocii.org/projects/mission-bay-north/overview,
https://sfocii.org/projects/mission-bay-south/overview, parks map (Oct 2021)
https://sfocii.org/files/inline-images/Mission%20Bay%20South%20Open%20Space.png

| field | official value | status | quote |
|---|---|---|---|
| acres | 303 (North 65, South 238) | CONFIRMED | "covers 303 acres of land between the San Francisco Bay and Interstate-280" |
| homes | 6,535 (2,964 + 3,571) | CONFIRMED | "Total Housing 2,964 units" / "Total Housing 3,571 units" |
| affordableHomes | 1,916 (698 + 1,218) | NEW | "Affordable Housing 698 units" / "Affordable Housing 1,218 units" |
| openSpaceAcres | 40.5 (6.5 + 34) | NEW | "Parks and Open Space 6.5 acres" / "34 acres" |
| commercial | South 6.1M sf plus 429 hotel rooms; North 200k sf | NEW | "Commercial and Institutional 6.1 million square feet and 429 hotel rooms" |
| plan adoption | Nov 1998 | CONFIRMED | "established the Mission Bay North and South Redevelopment Project Areas in November 1998." |
| developer | Catellus (original), now FOCIL-MB LLC | NEW | "original master developer, Catellus Development Corporation (now held by FOCIL-MB LLC)" |
| "ten more parks over eight years" | from the City Capital Plan **2022** edition (onesanfrancisco.org/node/693); stale | STALE | "The construction of 10 additional parks in Mission Bay is anticipated over the next eight years" |

Boundary: DataSF Former Redevelopment Agency Project Areas (`m288-24sn`, ODC-PDDL), features
"Mission Bay - North" and "Mission Bay - South" (~316 ac together, including water/street
edges; cite 303).

## piers-30-32

Sources:
- P30-2603: Port Item 11B, Mar 6, 2026. https://www.sfport.com/sites/default/files/2026-03/item_11b_piers_30-32_feasibility_improvement_ideas_-_info.docx.pdf
- P30-2507: Port Item 12A and Res. 25-40, July 2025. https://www.sfport.com/media/10606/download?inline=
- P30-MIN2507: https://www.sfport.com/media/10698/download?inline
- BOS-240342: Res. 247-24. https://sfgov.legistar.com/View.ashx?M=F&ID=12946504&GUID=9CA150DB-7928-4DCF-974E-F61EA9B3F21F (file: https://sfgov.legistar.com/LegislationDetail.aspx?ID=6611808&GUID=73D61F5F-476D-4D2A-8606-C577FA08763B)
- TS-2024: term sheet, Jan 17, 2024. https://sfgov.legistar.com/View.ashx?M=F&ID=12825404&GUID=D1962148-C9BC-461D-BEAB-ACE96775317D
- PLN: DataSF Planning records `qvu5-m3a2`, record 2025-011323PRJ.
- P30-WEB: https://www.sfport.com/projects-programs/piers-30-32-and-seawall-lot-330

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 15.3 | 15.3 | CONFIRMED | BOS-240342 p1 | "an approximately 15.3-acre site generally located along the Embarcadero between Bryant and Beale Streets" |
| 2021 ENA | 2021 | Port approved Feb 9, 2021 (Res. 21-08); executed March 2021 | CONFIRMED | P30-2603 p3 | "In March 2021, Port and Strada-TCC entered into an Exclusive Negotiating Agreement" |
| 2024 BoS | fiscal feasibility | Res. 247-24, adopted Apr 30, 2024; Port endorsed term sheet Jan 23, 2024 (Res. 24-10) | CONFIRMED | BOS-240342 | "Resolution finding … is fiscally feasible under Administrative Code, Chapter 29" |
| split | 2026-03 | July 2025 (Res. 25-40); agreements executed Oct 24, 2025; March 2026 was the 6-month update | CONFLICT | P30-2603 p1 | "In July 2025 by Resolution No. 25-40, the Port Commission authorized terminating the Exclusive Negotiating Agreement" |
| stage | paused | Piers negotiations paused 18 months to study feasibility | CONFIRMED | P30-2603 pp1, 4 | "agreed to pause active negotiations on Piers 30-32 for a period of 18 months" |
| office | ~376,000 | ~375,000 GSF (+55k mezzanine) | CONFLICT (minor) | TS-2024 p12 | "Approximately 375,000 GSF office space in Pier Shed" |
| retail | ~30,700 | ~70,000 sf | CONFLICT | TS-2024 p12 | "Approximately 70,000 SF retail space, including a market hall" |
| 45% deck removal | 45% | ~45% (6 acres), earlier proposal | CONFIRMED (dated) | P30-WEB | "removal of approximately 45% of the existing Pier (6-acres)" |
| SWL 330 units | 700+ | Term sheet 713 (186 BMR); SB 423 application May 13, 2026: 568 units (86 affordable), 23 stories/230 ft + 10 stories/105 ft, under review | CONFLICT → NEW | P30-2507 p4; PLN | "Per SB 423, the proposed project is a 568-unit, multifamily residential project located on Seawall Lot 330" |
| developer | Strada | Strada Investment Group affiliates | CONFIRMED | P30-2603 p1 | "affiliates of Strada Investment Group" |

Boundary: DataSF Parcels (`acdm-wktn`, ODC-PDDL): piers 9900/030 + 9900/032 (~13.1 ac); SWL 330
3771/002 + 3770/002 (~2.33 ac). Plan figure: TS-2024 Exhibit A.
