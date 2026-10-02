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
