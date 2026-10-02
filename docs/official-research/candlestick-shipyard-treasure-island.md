# Official-source findings: Candlestick Point, Hunters Point Shipyard, Treasure Island

Checked 2026-10-02 against documents downloaded from SF Planning's document store and read in full text (local copies go in `data/raw/official/`, git-ignored). Page numbers are PDF page numbers.

**Documents I read**
- **[M-YYYYMMDD]** Planning Commission minutes: `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/YYYYMMDD_cal_min.pdf`
- **[EIR-ES]** CP-HPS2 Final EIR Vol. I, Executive Summary (2010 FEIR, reissued Aug 2017): `https://sfplanning.s3.amazonaws.com/sfmea/CP-HPS_FEIR_Vol_I_2017-08-11.pdf`
- **[ADD-2013]** EIR Addendum, Dec 11, 2013: `https://sfplanning.s3.amazonaws.com/sfmea/2007.0946E_Adm.pdf`
- **[ADD5-A]** Addendum 5 (April 2018), Appendix A comparison tables: `https://sfplanning.s3.amazonaws.com/sfmea/AppA_ComparisonTables_28pp.pdf`
- **[PKT-2018]** Planning Commission packet for the Apr 26, 2018 hearing (case 2007.0946GPA-02 etc.), 898 pp: `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2007.0946.pdf`
- **[PKT-2019]** Planning Commission packet for the Oct 24, 2019 Candlestick D4D amendments (case 2007.0946CWP-03), 289 pp: `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2007.0946CWP-03.pdf`
- **[TI-2011]** Planning Commission informational memo, Mar 3, 2011 (case 2007.0903): `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2007.0903.pdf`
- **[TI-2019]** Planning Commission memo, Aug 22, 2019 (case 2007.0903PHA): `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2007.0903PHA.pdf`
- **[TI-CR1]** TI/YBI EIR Comments & Responses Vol. 1 (Mar 10, 2011): `https://sfplanning.s3.amazonaws.com/sfmea/2007.0903E_CR1.pdf`

**Hosts I could not reach.** None of these hosts responded (connection refused / no HTTP response), so nothing below draws on them:
- sfocii.org (Addenda 5–7, CCII resolutions, including Reso 28-2024)
- sfbos.org (Ordinance 164-18)
- ceqanet.lci.ca.gov (2024 Notice of Determination)
- sf.gov and media.api.sf.gov (TIDA items)
- generalplan.sfplanning.org
- default.sfplanning.org (cpcmotions)

**Planning Commission 2024.** No 2024 minutes, calendars or packets for case 2007.0946 are reachable in the bucket. I probed about 30 key names; all returned 403.

---

## 1. candlestick-point

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 280 | ~281 | CONFIRMED (approx.); use 281 | ADD-2013 p.2; M-20180322 item 14b; M-20180426 item 14a | "281 acres at Candlestick Point (Candlestick) and 421 acres at Hunters Point Shipyard"; "consists of roughly 281 acres at Candlestick Point" |
| homes | 7,200 | 7,218 (2018 change, restated in 2019) | CONFIRMED as approx.; exact figure is 7,218. The 2024 variant is not checked | ADD5-A p.4; PKT-2018 p.3; PKT-2019 p.2 (Table 1) | "Provide for 7,218 housing units at CP"; "Approximately 7,218 units at Candlestick"; "Housing Units 6,225 units 7,218 units" |
| affordablePct | null | 32% BMR, project-wide (CP+HPS2) | NEW official fact | PKT-2019 p.1 | "32% of the residential units will be below-market rate" |
| officeLabSqft | 2,000,000 | 750,000 sf office at CP (2019 proposal). Transfer of "up to 2,050,000" sf in 2024 appears only in search snippets of the CEQAnet NOD, which I could not open | CONFLICT with the last official figure I could read (2019). 2M is UNCONFIRMED (2024 docs unreachable) | PKT-2019 p.2 Table 1 | "Office 150,000 sf 750,000 sf" |
| commercialSqftTotal | 3,000,000 | not stated. 2018 CP nonresidential GSF total was 1,185,000 | UNCONFIRMED (superseded by 2019/2024) | ADD5-A p.25 Table A-2 | "GSF Total 1,185,000 SF" (Candlestick column) |
| openSpaceAcres | 100 | 105.7 ac total "Parks & open space" at CP (2018). This includes 90.9 ac of the *existing* State Recreation Area; new parks are 9.0 ac and new SRA 5.8 ac | CONFLICT in substance: ~100 counts the existing CPSRA | ADD5-A p.25 Table A-2 | "PARKS & OPEN SPACE … 105.7 AC"; "Existing State Recreation Area … 90.9 AC" |
| tower heights (verify) | needs verification | D4D max heights 40–420 ft. Up to 12 towers (>120 ft). 2019 amendment raised Candlestick Center from 65/80 ft to 120 ft and 85 ft. The 2024 D4D height increase is not checked | CONFIRMED through 2019; 2024 UNCONFIRMED | ADD5-A p.4; PKT-2019 p.4; PKT-2019 p.136 | "maximum building heights at CP range from 40 feet to 420 feet"; "allows for up to 12 towers (buildings above 120-feet tall)"; "High-rise buildings to a maximum of 420 ft height" |
| Candlestick Center | — | ~22.29 acres (former stadium site) | NEW | PKT-2019 p.2 | "Candlestick Center encompasses roughly 22.29 acres" |
| timeline 2008 | "voters set a conceptual framework" | June 2008 Proposition G. The Conceptual Framework itself was endorsed by the Board in May 2007 | CONFIRMED with correction | PKT-2018 p.25 | "In June 2008, San Francisco voters approved Proposition G … The Bayview Jobs, Parks, and Housing Initiative"; "In May 2007, the Board of Supervisors adopted and the Mayor approved a resolution endorsing a Conceptual" (Framework) |
| original approval | (missing) | FEIR certified June 3, 2010; Board affirmed July 14, 2010 | NEW | ADD-2013 p.2 | "On June 3, 2010, the San Francisco Planning Commission and the Redevelopment Agency Commission certified the Final Environmental Impact Report" |
| 2018 amendments | (missing) | Apr 26, 2018: Planning Commission Resolutions 20162–20165 (GPA, map amendment, consistency findings, D4D). Board files 180475/180476 passed second read by Jul 12, 2018 | NEW | M-20180426 items 14a–d; M-20180712 | "RESOLUTION: 20162" … "20165"; "180475 General Plan Amendments … PASSED Second Read" |
| 2019 D4D amendment | (missing) | Oct 24, 2019, Motion 20552 (heights, Candlestick Center). CCII approved the R&D transfer Oct 15, 2019 | NEW | M-20191024 item 14; PKT-2019 p.2 | "MOTION: 20552"; "transfer of some R&D/office entitlement from Hunters Point Shipyard which was approved by CCII … on October 15, 2019" |
| timeline late 2024 | permits 7,200 homes, ~2M sf shift, decoupling | Official docs unreachable. The only official thread is a search snippet of the CEQAnet NOD (10/28/2024, "2024 Modified Project Variant"), which I did not read | UNCONFIRMED → `reported` | — | — |
| timeline by Aug 2026 (7 phases) | DDA amended | — | UNCONFIRMED → `reported` | — | — |
| 2026-09-10 groundbreaking | — | — | UNCONFIRMED → `reported` | — | — |
| developer | FivePoint | "FivePoint (previously Lennar Urban)" | CONFIRMED | PKT-2018 p.3 | "FivePoint (previously Lennar Urban) (Developer)" |

**Boundary leads**
- Assessor Block 4991 / Lot 276 (the "Jamestown Parcel") was **removed** from the Candlestick Point Sub-Area Plan, the special use district (SUD) and the D4D in 2018 (M-20180426 14a–d; PKT-2018 p.1). Exclude it from the boundary.
- What the plan area contains: the "former Candlestick Park Stadium and parking lot, the Candlestick Point State Recreational Area, the Alice Griffith Housing development site" (M-20180322).
- The boundary equals the Candlestick Point Activity Node SUD on Planning Code Sectional Map SU10, and the CP Height and Bulk District on map HT10.
- Figures to trace:
  - EIR Figure II-1 (Project Location)
  - EIR Figure II-5 (Proposed Maximum Building Heights)
  - Addendum 5 Figure 5 (CP-HPS2 Land Use Plan, p.16 of the main addendum; the main body was not reachable, only Appendix A)
  - PKT-2019 D4D height maps (around pp.104–107, 136)
- Addendum 5 also says it would "modify the boundary of CP-05" (ADD5-A p.4).

**Suggested edits to projects.json**
- `acres`: 281. `acresNote`: "Approximately 281 acres (SF Planning / OCII, 2013–2018)". Drop the 270 note.
- `program.homes`: 7218, with the note "7,218 per 2018 amendments (Addendum 5); 2024 changes not yet verified".
- `program.affordablePct`: 32. Note that it applies "project-wide across Candlestick Point and Hunters Point Shipyard Phase 2, per SF Planning Oct 2019".
- `program.officeLabSqft`: either set 750000 (2019 official) or set null and move 2,000,000 to `reported` until the 2024 OCII/NOD docs are read.
- `program.commercialSqftTotal`: move 3,000,000 to `reported`.
- `program.openSpaceAcres`: 105.7, with a note that it includes the 90.9-ac existing Candlestick Point State Recreation Area. Alternatively, move 100 to `reported`.
- `timeline`:
  - Replace 2008 with "2008-06: Voters approve Proposition G".
  - Add "2010-06-03: EIR certified; project approved".
  - Add "2018-04-26: Planning Commission approves amendments (7,218 homes at Candlestick)".
  - Add "2019-10-24: Candlestick Center D4D amended (Motion 20552)".
  - Move the late-2024, Aug-2026 and Sept-10-2026 entries to `reported`.
- `officialLinks`: add PKT-2019, ADD5-A, ADD-2013 and EIR-ES.
- `stageNote`: the groundbreaking is press-only. The stage stays as is, but the facts behind it go in `reported`.

**Still open**
- The 2024 Modified Project Variant needs OCII Addendum 7, CCII Reso 28-2024, the Sep 12, 2024 Planning Commission packet, and the Board ordinance. It would settle current homes, office/R&D (about 2.05M?) and heights (120–180 ft?). All are unreachable.
- The DDA amendment that created seven phases is unverified.

---

## 2. hunters-point-shipyard

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 420 | HPS Phase II: 421 ac (2013) and "roughly 402 acres" (2018 hearing items). Whole shipyard about 490 ac | CONFLICT / inconsistent official figures. 420 matches 2013, not 2018 | ADD-2013 p.2; M-20180322 14a; M-20180426 14a; PKT-2018 p.25 | "421 acres at Hunters Point Shipyard (HPS Phase II)"; "Phase II site encompasses roughly 402 acres and includes all of Hunters Point Shipyard except for the portions referred to as 'Hilltop' and 'Hillside'"; "landfill peninsula of approximately 490 acres" |
| Phase 2 homes | null | 3,454 (2018 Modified Project Variant, including 172 transferred from Phase 1) | NEW official (pre-2024) | ADD5-A p.25 Table A-2; PKT-2018 p.3 | "Approximately 3,454 units at the Shipyard" |
| Phase 2 R&D/office | null | 4,265,000 sf (2018). The 2019 and 2024 transfers to Candlestick reduce this; the current figure is unverified | NEW; SUPERSEDED in part | ADD5-A p.25; PKT-2018 p.3 | "Allowing up to 4,265,000 sq. ft. of research and development / office use at the Shipyard" |
| Phase 2 other (2018) | null | 100,000 sf regional retail, 226,000 sf neighborhood retail, 75,000 sf maker space, 410,000 sf institutional, hotel with 175 rooms, 255,000 sf artist studio | NEW (2018) | ADD5-A p.25 | "Hotel … 120,000 SF … 175 ROOMS"; "Institution … 410,000 SF" |
| Phase 2 open space | null | 232.0 ac parks & open space (2018) | NEW (2018) | ADD5-A p.25 | "PARKS & OPEN SPACE … 232.0 AC" (HPS2 column) |
| Phase 2 heights | — | 2010: 40–105 ft. 2018: some blocks raised from 65 to 85 ft and from 105 to 120 ft | NEW | ADD5-A p.4 | "maximum building heights at HPS range from 40 feet to 105 feet"; "increase from 65 feet to 85 feet and from 105 feet to 120 feet" |
| Phase 1 program | "a few hundred homes" (built) | Phase 1 DDA (2003): infrastructure for up to 1,600 units, about 30% affordable, about 25 ac of parks. Parcel A was conveyed by the Navy in 2005. 172 Phase 1 units were moved to Phase 2 in 2018. Homes actually delivered: no official count | Built count UNCONFIRMED; entitlement NEW | PKT-2018 p.24; p.3 | "up to 1,600 residential units, of which approximately 30% must be affordable and approximately 25 acres of public parks and open space" |
| timeline 1999 Lennar awarded | 1999 | Not found. The official record shows the Shipyard Redevelopment Plan adopted in 1997 and the Phase 1 DDA with "Lennar/BVHP Partners" in 2003 | UNCONFIRMED; suggest replacing with official dates | PKT-2018 p.24 | "In 1997 … adopted the Hunters Point Shipyard Redevelopment Plan"; "In 2003, the Agency entered into the Hunters Point Shipyard Phase 1 Disposition and Development Agreement" |
| timeline 2008 | voters approve | June 2008 Proposition G | CONFIRMED | PKT-2018 p.25 | (see Candlestick) |
| timeline 2016 FivePoint spun off | — | PKT-2018 only says "FivePoint (previously Lennar Urban)"; no date | UNCONFIRMED → `reported` | PKT-2018 p.3 | — |
| 2025 start moved to 2038; Phase 1 parks 2026–2030; ~7 acres; Navy retesting | — | — | UNCONFIRMED → `reported` | — | — |
| 2018 approvals | (missing) | Apr 26, 2018: Resolutions 20162–20165, including the full replacement of the HPS Phase 2 D4D (20165) | NEW | M-20180426 14d | "fully amending the Hunters Point Shipyard Phase 2 Design for Development document" … "RESOLUTION: 20165" |

**Boundary leads**
- Phase II is defined as "all of Hunters Point Shipyard except for the portions referred to as 'Hilltop' and 'Hillside'" (Phase 1 / Parcel A). So the boundary is the Shipyard Redevelopment Project Area minus Parcel A.
- The PKT-2018 header lists HPS Block 4591A / Lots 007, 079, 080, 081 and Block 4591D / Lots 136 and 137. These are the lots subject to the 2018 General Plan amendments, not necessarily the whole area.
- The HPS boundary equals the Hunters Point Shipyard SUD and the HP Height and Bulk District.
- The 2018 HPS Phase 2 D4D is in PKT-2018 (898 pp; its maps are not yet traced).
- The Navy parcel boundaries (Parcels B–G, UC-1/2) are not checked; the Navy site is unreachable.

**Suggested edits to projects.json**
- `acres`: keep 420 but change `acresNote` to "421 acres (2013 EIR addendum); 2018 Planning Commission items say roughly 402 acres for Phase 2 excluding Hilltop/Hillside". Alternatively, use 402 and cite the 2018 source.
- `program`: fill homes 3454, officeLabSqft 4265000 and openSpaceAcres 232. Label them "2018 approved program; reduced by later transfers to Candlestick (2019, 2024), current figures unverified". Or keep them null and put the 2018 figures in `notes` with the source.
- `program.notes`: add "Phase 1 entitled up to 1,600 homes, ~30% affordable, ~25 acres of parks (2003 DDA)".
- `timeline`:
  - Replace 1999 with "1997: Shipyard Redevelopment Plan adopted" and "2003: Phase 1 DDA with Lennar/BVHP Partners".
  - Add "2005: Navy conveys Parcel A".
  - Add "2010-06-03: Phase 2 EIR certified".
  - Add "2018-04-26: Phase 2 plan redesigned (3,454 homes, 4.27M sf R&D)".
  - Move 2016, 2025 and 2026–2030 to `reported`.
- `stageNote`: everything in it (2038, Navy retesting, 7 acres) is press-only and goes to `reported`. "Paused" stays as the drawn stage but needs an official citation.
- `officialLinks`: add PKT-2018, ADD5-A and ADD-2013.

**Still open**
- Current Phase 2 program after the 2024 transfer.
- Phase 1 homes delivered (needs OCII).
- Navy retesting status.

---

## 3. treasure-island

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 405 | about 400 ac (TI + YBI project area). Excludes the 37-ac Job Corps campus and the eastern half of YBI (Coast Guard) | CONFLICT (minor): official is "approximately 400" | TI-2011 p.1, p.2 | "The Project covers approximately 400 acres on both Treasure Island and Yerba Buena Island"; "The Project Area excludes 37 acres of Treasure Island" |
| homes | 8,000 | 8,000 (271 on YBI) | CONFIRMED (2011 program; a 2026 unit increase was proposed but not verified) | TI-2011 p.2; TI-2019 p.1 | "8,000 new residential units"; "up to 8,000 homes … save for 271 homes which will be located on Yerba Buena Island" |
| affordableHomes / Pct | null | up to 2,400 affordable units (= 30% of 8,000). At least 20% of affordable units for very-low income; about 435 TIHDI units | NEW official (2011) | TI-CR1 p.151 | "TIDA has agreed to provide up to 2,400 units that would be affordably priced at a range of below-market rates" |
| retail / office / hotel | null | 140,000 sf retail; 100,000 sf office; 311,000 sf adaptive reuse (Buildings 1–3); 500 hotel rooms | NEW (2011) | TI-2011 p.2 | "140,000 square feet of new retail uses"; "100,000 square feet of commercial office space"; "500 hotel rooms" |
| openSpaceAcres | 300 | ~300 | CONFIRMED | TI-2011 p.3 | "300 acres of open space" |
| planned tower heights (verify; "about 40 stories") | ~40 stories | Max height 450 ft in the final D4D (reduced from 650 ft). Approved example: Block C2.1, about 31 stories / 315 ft. Stories for the 450-ft tower are not stated | Height CONFIRMED in feet; "40 stories" UNCONFIRMED | TI-CR1 p.103, p.177; TI-2019 p.2 | "the tallest tower would be reduced from 650 feet to 450 feet"; "approximately 31-story, 315-foot tall building with 265 residential units" |
| approval | (missing) | Board approved June 2011 (Development Agreement, Ord. 0095-11) | NEW | TI-2019 p.1 | "approved by the San Francisco Board of Supervisors in June 2011 pursuant to a Development Agreement (San Francisco Board of Supervisors in Ordinance No. 0095-11)" |
| developer | TIDG (Lennar, Stockbridge, Wilson Meany) | TICD selected 2003. "Treasure Island Development Group" is named as sponsor/owner in 2019. Partner names are not in the official docs I read | Partially CONFIRMED; partner list → `reported` | TI-2011 p.2; TI-2019 p.1 | "in 2003, the Treasure Island Development Authority ("TIDA") selected … Treasure Island Community Development, LLC" |
| Phase 1 status (2019) | — | Subphase 1C included one 100%-affordable building | NEW | TI-2019 p.1 | "one 100% affordable housing building in Subphase 1C has received Planning Director approval" |
| Isle House 22 stories / opening; 2016 infrastructure; 2022 ferry; 2026 1,000+ residents, Bay FC, phase one complete Jul 2026; "recently approved more density" | — | Not in reachable official docs. TIDA items exist (media.api.sf.gov, incl. "02.11.26_Item_9_Unit_Increase.pdf") but the host was unreachable | UNCONFIRMED → `reported` | — | — |

**Boundary leads**
- 2011: Assessor Block 1939 / Lots 001, 002 (TI-2011 p.1).
- 2019: subdivided Blocks 8903/001 and 8904/002 for C2.1/C2.4 (TI-2019 p.1).
- The project area is TI minus the 37-ac Job Corps campus, plus the western half of YBI (the eastern half is Coast Guard).
- EIR Figure II.6a "Treasure Island Maximum Height Limit Plan" (EIR p. II.25), and D4D Figure T4.p "Maximum Height Limit Plan" (draft D4D p.157) (TI-CR1 p.103).
- Planning Code §249.52, the TI/YBI SUD, with zoning districts TI-R / TI-OS and the "-TI" height districts (e.g. 70-TI/315 Flex Zone).

**Suggested edits to projects.json**
- `acres`: 400. `acresNote`: "Approximately 400 acres; excludes the 37-acre Job Corps campus and the Coast Guard's half of Yerba Buena Island (SF Planning, 2011)".
- `program`:
  - affordableHomes: 2400, affordablePct: 30, with the note "up to 2,400 (2011 EIR)".
  - retailSqft: 140000; officeLabSqft: 100000; hotelKeys: 500. Label these as the 2011 approved program.
- `timeline`:
  - Add "2003: TIDA selects master developer".
  - Add "2011-06: Board of Supervisors approves the project (Ord. 95-11)".
  - Move 2016, 2022, 2024, 2026-06 and 2026-07 to `reported`.
- `massingNotes`: "Max allowed height 450 ft (Design for Development); C2.1 approved at ~31 stories / 315 ft". Move Isle House 22 stories and "about 40 stories" to `reported`.
- `stageNote`: entirely press-sourced, so it goes to `reported`. Note that one current source in the record (media.api.sf.gov `070826_Communications.pdf`) is an official SF host, but I could not reach it to confirm.
- `officialLinks`: add TI-2011, TI-2019 and TI-CR1.

**Still open**
- The 2024 DDA/D4D amendments and the 2026 unit-increase item (TIDA, on sf.gov and media.api.sf.gov). These would update homes, affordability and density.
- Phase-one completion status.
- Isle House height and opening.

---

## Cross-cutting notes
- The prompt suggested many Hunters Point hearings in 2018–2021. In the downloaded minutes, Shipyard items appear only in 2018 (Mar 22, Apr 19 comment, Apr 26, Jun 28, Jul 12). No 2019–2021 HPS items were found; the 2019 action was Candlestick-only.
- Every 2024–2026 claim for all three projects depends on OCII, TIDA, the Board or CEQAnet, and those hosts were unreachable from here. They should go to `reported` until someone can fetch those hosts.
