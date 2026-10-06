# Candidate projects: Schlage Lock, Sunnydale HOPE SF, Potrero HOPE SF, Middlefield Park, East Whisman Precise Plan

Checked 2026-10-05. I downloaded the documents and read them in full text. Local copies are in `data/raw/official/cand-smv/`, which is git-ignored. Page numbers are PDF page numbers. Draft records for the four recommended candidates are in the scratchpad (`records/candidates/<id>.json`), and all four pass `tests/record-check.test.ts`.

Access notes:
- `www.mountainview.gov` returns 403 (Akamai) to every request, so the city's project pages and the adopted precise plan PDF couldn't be read there. Mountain View documents come from Legistar instead: the `webapi.legistar.com/v1/mountainview/` API, plus attachments fetched through `mountainview.legistar.com/gateway.aspx?M=F&ID=<guid>.pdf`.
- The SF Legistar web API (`webapi.legistar.com/v1/sfgov/`) stops at late 2018. SF ordinances were read from the Board's archive at `sfbos.archive.sf.gov`; `sfbos.org` URLs redirect there.
- DBI permits come from DataSF `i98e-djp9`. `data.sfgov.org` now redirects to `data.sf.gov`, and both are `.gov`.

URL shorthand:
- MVGW = `https://mountainview.legistar.com/gateway.aspx?M=F&ID=<guid>.pdf`
- PERMIT = `https://data.sfgov.org/resource/i98e-djp9.json?permit_number=<n>`
- SFHOPE = `https://sfplanning.s3.amazonaws.com/default/files/devagreements/HOPE-SF/`

Summary of recommendations:

| candidate | recommendation | id |
|---|---|---|
| Schlage Lock / Visitacion Valley | INCLUDE (entitled, stalled) | `schlage-lock` |
| Sunnydale HOPE SF | INCLUDE (partly built) | `sunnydale-hope-sf` |
| Potrero HOPE SF | INCLUDE (partly built) | `potrero-hope-sf` |
| Middlefield Park | INCLUDE (entitled) | `middlefield-park` |
| East Whisman Precise Plan | EXCLUDE (a plan, not a project; Middlefield Park is its project) | — |

---

## schlage-lock (Visitacion Valley/Schlage Lock)

Documents:
- Planning project page: https://sfplanning.org/visitacion-valleyschlage-lock-plan
- OEWD development agreement summary, May 2, 2014: https://sfplanning.s3.amazonaws.com/default/files/Citywide/Visitacion_Valley/visvalley_SchlageLockDASummary-May2014.pdf
- Ordinance 149-14 (development agreement, Board file 140444): https://sfbos.archive.sf.gov/ftp/uploadedfiles/bdsupvrs/ordinances14/o0149-14.pdf
- Ordinance 150-14 (SUD and zoning, file 140445): https://sfbos.archive.sf.gov/ftp/uploadedfiles/bdsupvrs/ordinances14/o0150-14.pdf (image-only PDF; title from Legistar API)
- Revised Phase 1 approval, Sept 17, 2018: http://default.sfplanning.org/Citywide/Visitacion_Valley/Schlage_Revised_Phase01_Conditions_FINAL-091718.pdf
- Revised Phase 1 application, July 2018 (the applicant's document; used only for parcel and boundary leads): http://default.sfplanning.org/Citywide/Visitacion_Valley/VIS_VALLEY_REVISED_PHASE01_APPLICATION-FINAL-072718.pdf
- Planning's annual update under DA §6.4, Oct 2025: https://sfplanning.org/sites/default/files/documents/citywide/VisValley/visvalley_planning_presentation-103125.pdf
- Planning Code §249.45: https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_planning/0-0-0-21314
- DBI permits at 2201 and 2401 Bayshore Blvd (block 5087)

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | 20 (the Schlage site) | DA summary p.1 | "transformation the 20-acre Schlage Lock site" |
| EIR area | about 46 acres (whole redevelopment program) | Ord. 149-14 p.2 | "redevelopment of an approximately 46-acre project area" |
| homes | up to 1,679 | Ord. 149-14 p.2; DA summary p.1 | "up to 1,679 dwelling units of new housing, up to 46, 700 square feet of new retail" |
| retailSqft | 46,700 | same | as above |
| affordablePct | 15% inclusionary, at least 2/3 on site | DA summary p.2 | "The Project has a 15% inclusionary housing requirement"; "At least 2/3 of the Inclusionary Housing Program Requirement must be satisfied with on-site BMR units" |
| grocery | at least 15,000 sq ft on Parcel 1 | DA summary p.3 | "Parcel 1 of the Project must include a full service grocery store of at least 15,000 square feet" |
| DA term | 15 years | DA summary p.1 | "The development agreement ("DA") has a 15-year term" |
| developer | Visitacion Development, LLC (Universal Paragon Corporation) | DA summary p.1; Ord. 149-14 title | "Visitation Development, LLC (a division of Universal Paragon Corporation)" |
| Board approval | finally passed 2014-07-22, Ord. 149-14 | Ord. 149-14 p.9 | "July 22, 2014 Board of Supervisors - FINALLY PASSED" |
| EIR | certified 2008-12-18 by Planning Commission and the former Redevelopment Agency | Ord. 149-14 p.2 | "certified a final environmental impact report ("FEIR") for the Visitacion Valley Redevelopment Program ... on December 18, 2008" |
| Phase 1 | first approved 2017-07-05; revised approval 2018-09-17 (Parcels 1–3, Leland Park) | Phase 1 approval letter p.2 | "earlier Phase 1 Application submittal, dated April 28, 2017 and approved July 5, 2017"; "This letter approves the revised Development Phase I Application subject to the conditions below." |
| historic office rehab | permit 201507010504 issued 2016-05-18, complete 2022-09-16 | PERMIT 201507010504 | "rehabof historic bldg for use as office space" |
| housing permits | 201912189909 (2201 Bayshore, 5 stories, 146 units) and 201912189911 (2401 Bayshore, 7 stories, 152 units), both "filed" 2019-12-18 | PERMIT | "to erect (n) 5-story (1) basement, type ii, 146 dwelling units" |
| site work | grading permit 201608155048 issued 2016-10-11, never completed | PERMIT | "rough grading for future utilities" |

Stage: entitled. Nothing official shows vertical construction. Planning's 2025 update covers only impact fees and neighborhood capital projects.

Boundary lead: the DataSF Special Use Districts layer (5yf5-ms5f, Public Domain) has a feature named "Visitacion Valley/Schlage SUD", but it measures about 45 acres because it covers Zone 1 (the Schlage site) and also Zone 2 (Bayshore and Leland). Zone 1 has to be traced from the Design for Development (June 16, 2014, `http://default.sfplanning.org/Citywide/Visitacion_Valley/Visitacion_Valley_Schlage-Design_for_Development_20140616_BoS.pdf`) or the DA exhibits (`Visitacion_Valley_Schlage-Final_DA_Exhibits-082214.pdf`), registered to DataSF parcels (acdm-wktn, ODC PDDL). Block 5087, lots 003, 003A, 004 and 005, comes to about 8.4 acres, so it is only part of the site.

Massing lead: Design for Development height plan. The Phase 1 application lists Parcels 1–3 at 55, 64 and 72 ft, but that is the applicant's table and needs checking against the D4D.

Developer-only (Baylands Development, Inc., Oct 2025 annual update, hosted by Planning but authored by the developer): https://sfplanning.org/sites/default/files/documents/citywide/VisValley/visvalley_presentation_baylands-103125.pdf
- "Phase 1 timeline delayed pending improved market conditions"
- new name "Leland Square"
- "~252 affordable units"
- "Historic Office Rehabilitation (completed in 2022)", which DBI confirms.

Press-only: UPC plans and 1/3 rental shares (SF Examiner), and the 2014 Mayor's Office release (sfgov.org mayoredlee). Neither was used.

Recommendation: INCLUDE. It has 1,679 homes on 20 acres, a recorded DA and a Phase 1 approval. It is entitled and stalled, and the DA runs to about 2029. The record is `schlage-lock`, with the developer's delay statement kept in `reported`. It sits next to the existing `brisbane-baylands` record (same owner, across the county line).

---

## sunnydale-hope-sf

Documents:
- Planning project page: https://sfplanning.org/sunnydale-hope-sf
- Ord. 18-17 (DA, file 161164): https://sfbos.archive.sf.gov/sites/default/files/o0018-17.pdf
- Ord. 16-17 (SUD): https://sfbos.archive.sf.gov/sites/default/files/o0016-17.pdf
- DA: SFHOPE `Sunnydale/HOPE-SF_Sunnydale_Development_Agreement.pdf`
- Phase 4 approval, July 15, 2022: https://sfplanning.org/sites/default/files/documents/devagreements/Sunnydale_HopeSF_Phase4_Application_Approval.pdf
- MOHCD Block 9 loan evaluation, Jan 24, 2025: https://media.api.sf.gov/documents/Approved_Sunnydale_Block_9_Loan_Evaluation_-_LC_1-24-25.pdf
- DBI permits

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | about 50 | Ord. 18-17 p.1 | "approximately 50-acre site located in Visitacion Valley" |
| homes | up to 1,770 | Ord. 18-17 p.2 | "a maximum of 1,770 units, of which 775 are replacement units ... approximately 200 are additional affordable housing units ... up to 730 units that will be for market rate" |
| homes (page) | about 1,770; 775 + ~200 + ~694 | Planning page | "approximately 1,770 residential units (775 replacement affordable units, approximately 200 additional affordable housing units, and approximately 694 market rate units)" |
| affordable | at least 969 rent-restricted | DA Exhibit C | "Construction of at least 969 new rent-restricted apartments" |
| open space | 3.6 ac (ordinance); 3.5 ac (page); DA Exhibit C counts 9.6 ac including 5 ac private | Ord. 18-17 p.2; page; DA | "3.6 acres of new open spaces" |
| neighborhood space | about 60,000 sq ft | Ord. 18-17 p.2 | "approximately 60,000 square feet of new neighborhood serving spaces" |
| Board | finally passed 2017-01-31; ordinance effective 2017-03-03 | Ord. 18-17 p.8; DA recital N | "Ordinance was FINALLY PASSED on 1/31/2017"; "The Enacting Ordinance took effect on March 3, 2017." |
| EIR | Planning page: "certified 7/9/15"; DA recital says "certified by the Planning Commission on November 17, 2016" | page; DA recital K | CONFLICT, listed in `verify` |
| DA term | 25 years | DA §3.2 | "for twenty-five (25) years thereafter" |
| developer | Sunnydale Development Co., LLC; Mercy Housing and Related California | Ord. 18-17 title; Phase 4 approval p.1 | "Development Agreement between Mercy Housing / Related California, the City and County of San Francisco, and the San Francisco Housing Authority" |
| status July 2022 | 222 complete (Parcel Q, Blocks 6A and 6B); Phase 4 approved | Phase 4 approval p.2 | "Complete (Parcel Q, Blocks 6A and 6B) 222" |
| permit: 1491 Sunnydale (Parcel Q/Casala) | 55 units, complete 2020-02-20 | PERMIT 201612225710 | "55 units affordable multi family apartments" |
| permit: 242 Hahn | 167 units, complete 2022-06-24 (MOHCD names "290 Malosi"; Casala + 290 Malosi = 222) | PERMIT 201806202372; Block 9 eval p.10 | "Casala and 290 Malosi, totaling 222 units" |
| permit: Blocks 3A/3B, 1501 Sunnydale | 80 and 90 units, both complete 2025-04-28 | PERMIT 202106031523, 202106031549 | "sunnydale block 3a (lot 3) ... 80 residential units" |
| permit: 1500 Sunnydale | community center with childcare, complete 2024-10-15 | PERMIT 202107124132 | "community center with childcare center" |
| permit: Block 9, 1652 Sunnydale | 95 units; first construction document 2025-06-18 | PERMIT 202211146447; Block 9 eval p.2 | "Sunnydale HOPE SF Block 9 will include 95 units of affordable housing" |
| permit: 1501 Sunnydale lot 019E | 89 units; first construction document 2025-07-16 (block not named; Block 7 is the likely match) | PERMIT 202211297323 | "erect a 5-story,89 dwelling units" |

Stage: partial. Permits mark 392 homes complete, and 184 more are under construction.

Boundary lead: DataSF SUD layer 5yf5-ms5f, feature "Sunnydale Hope SF" (about 50.3 acres, Public Domain). It is official and matches the DA site. Massing lead: SUD (Planning Code §249.75) height controls and the Design Standards and Guidelines (SFHOPE `Sunnydale/HOPE-SF_Sunnydale_Design_Controls_Guidelines.pdf`); built and under-way blocks have 4–5 stories per their permits.

Press-only: none was needed.

Recommendation: INCLUDE as `sunnydale-hope-sf`. It has 1,770 homes on 50 acres, is multi-phase and is actively building. It meets the bar.

---

## potrero-hope-sf

Documents:
- Planning project page: https://sfplanning.org/potrero-hope-sf
- Ord. 15-17 (DA, file 161161): https://sfbos.archive.sf.gov/sites/default/files/o0015-17.pdf
- Ord. 13-17 (SUD): https://sfbos.archive.sf.gov/sites/default/files/o0013-17.pdf
- DA: SFHOPE `Potrero/HOPE-SF_Potrero_Development_Agreement.pdf`
- Phase 2 approval, Oct 13, 2017: SFHOPE `Potrero/HOPE-SF_Potrero_Phase2_Approval_20171013.pdf`
- City announcement, Mar 11, 2021: https://www.sf.gov/news--city-announces-groundbreaking-critical-infrastructure-potrero-hope-sf-affordable-housing
- MOHCD Phase III loan evaluation, Apr 4, 2025: https://media.api.sf.gov/documents/Approved-Potrero_HOPE_SF_Phase_III_Predevelopment_Loan_Evaluation_LC_4-04-2025.pdf
- DBI permits

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | about 38 (also "nearly 40") | Ord. 15-17 pp.1, 5 | "approximately 38-acre irregularly-shaped site bounded by 23rd Street and Missouri" |
| homes | up to 1,700 | Ord. 15-17 p.2 | "a maximum of 1,700 units, of which approximately 800 are replacement units for existing Potrero households and additional affordable housing units. There are also up to 800 units that will be for market rate" |
| homes (page) | about 1,700; 619 + ~200 + ~800 | Planning page | "approximately 1,700 residential units, (619 replacement affordable units, approximately 200 additional affordable housing units, and approximately 800 market rate units)" |
| affordable (2021 release) | 619 rebuilt plus 155 more affordable | sf.gov 2021-03-11 | "rebuild 619 units of distressed public housing and create an additional 155 affordable homes" (conflict, listed in `verify`) |
| open space | 3.5 ac | Ord. 15-17 p.2; page | "3.5 acres of new open spaces" |
| neighborhood space | about 50,000 sq ft (ordinance); 45,000 (page) | Ord. 15-17 p.2 | "approximately 50,000 square feet of new neighborhood serving spaces" |
| EIR | certified 2015-12-10, Motion 19529 | DA recital K | "certified by the Planning Commission on December 10, 2015, by Motion No. 19529" |
| Board | finally passed 2017-01-31 | Ord. 15-17 p.8 | "Ordinance was FINALLY PASSED on 1/31/2017" |
| developer | BRIDGE Potrero Community Associates, LLC (BRIDGE Housing) | Ord. 15-17 title; page | "Development Agreement - BRIDGE Potrero Community Associates, LLC" |
| Phase 2 | approved 2017-10-13 (Blocks A and B) | Phase 2 approval p.1 | "Potrero HOPE SF —Phase 2(Blocks A and B)" |
| Phase 2 infrastructure | began the week of 2021-03-11; 3.96 acres | sf.gov 2021 | "Phase 2 of the Potrero HOPE SF development is comprised of 3.96 acres of land" |
| schedule | five phases, last in 2035 | sf.gov 2021 | "Once the final of five construction and development phases is completed in 2035" |
| permit: 1101 Connecticut | 72 units, complete 2019-10-28 | PERMIT 201603172392 | "72 units, 100% affordable housing" |
| permit: 1801 25th (Block B) | 157 units; first construction document 2022-08-22; complete 2025-12-04 | PERMIT 202006108345; Phase III eval p.6 | "Out of the 157 units at Block B, 117 will house existing Potrero ..." |
| Phase 3 | predevelopment funding for demolishing 23 buildings (Loan Committee 2025-04-04) | Phase III eval p.1 | "Potrero Phase III Demolition" |

Stage: partial. Permits mark 229 homes complete.

Boundary lead: DataSF SUD layer 5yf5-ms5f, feature "Potrero Hope SF" (about 36 acres, Public Domain), official. Massing lead: SUD (Planning Code §249.74) heights and the Design Standards and Guidelines. Built blocks are 5 and 7 stories per their permits.

Press-only: the Potrero View reports a 2034 completion. Not used.

Recommendation: INCLUDE as `potrero-hope-sf`. It has 1,700 homes on 38 acres, is multi-phase and is building. The record's name and aliases keep it distinct from `potrero-power-station`.

---

## middlefield-park (Mountain View)

Documents (Legistar matters 6116, 6117, 6876, 6895, 10628):
- Council report, Nov 15, 2022: MVGW 139b5db2-d2ff-4b5c-8289-1757db0928d7
- Master plan resolution: MVGW a324c82e-f151-47f1-8a60-15ecb6cd21ee
- DA key terms: MVGW c0795dd4-ca8c-4797-b091-39cbbe8c9907
- DA ordinance as attached: MVGW 44cb14e7-2867-48c7-9275-de4cdcd7513f
- Second-reading report, Dec 13, 2022: MVGW f7269f0d-5ad4-4b0b-b069-0910174adc7c
- Minutes, Nov 15, 2022: https://legistar1.granicus.com/mountainview/meetings/2022/11/2103_M_City_Council_22-11-15_Meeting_Minutes.pdf (`legistar1.granicus.com/mountainview/` isn't in official.ts; the record cites `webapi.legistar.com/v1/mountainview/events/2103/eventitems` instead)
- Lease report, June 23, 2026: MVGW 96fd7425-1e3a-493c-ad8c-35e070c634f6

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | about 40; 14 parcels | Council report p.2 | "Project Site Size: Approximately 40 acres." |
| homes | up to 1,900 | Res. 18734 title (minutes p.6) | "Approving a Master Plan to Construct Up to 1,900 Residential Units, 1,317,000 Square Feet of Office/R&D, 50,000 Square Feet of Ground-Floor Commercial Space, 6.97 Acres of Public Parks and 2.8 Acres of Privately Owned, Publicly Accessible Open Space" |
| affordable | 2.4 acres dedicated to the City; applicant estimates 380 units (20%); staff example 338 (17%) | Council report pp.16, 6 | "up to an estimated 380 affordable units (20% of units) to be accommodated via land delivery"; "City staff's example assessment is less at 338 units (17%)" |
| office | 1,317,000 sq ft (632,354 net new) | Council report pp.4, 14 | "Google is requesting 632,354 square feet from the development reserve" |
| open space | 6.97 ac public parks plus 2.87 ac POPA (title says 2.8) | Council report p.4 | "6.97 acres are proposed to be dedicated to the City as public parks ... and 2.87 acres are proposed as a privately owned, publicly accessible (POPA) open space" |
| heights | residential 7–11 stories; office 4–9 stories | Council report pp.3–4 | "heights ranging from approximately seven to 11 stories"; "ranging in height from approximately four to nine stories" |
| existing | 23 buildings, 684,645 sq ft | Council report p.3 | "Comprised of 23 existing one- to four-story buildings with 684,645 square feet" |
| developer | Google LLC with Lendlease | Council report p.3 | "Applicant/Owner: Google LLC, in partnership with Lendlease" |
| phasing | four phases over about 8–12 years | Council report p.5 | "construct the Master Plan in four phases over approximately eight to 12 years" |
| approvals | 2022-11-15: Res. 18733 (SEIR), 18734 (master plan), 18735 (VTM), 18736 (vacation), 18737 (surplus land), 18738 (park credit); vote 6-0, 1 recused | minutes pp.6–7 | "Adopt Resolution No. 18734 of the City Council ..." |
| DA | second reading 2022-12-13; effective 2023-01-12; 12 + 8 years = 20 years | second-reading report p.1; key terms p.1 | "If adopted, the ordinance and DA will be effective on January 12, 2023."; "Total: 20 Years" |
| 2026 lease | Council report recommends a 7-year City lease of 485 and 495 Clyde Ave (APN 160-57-006, -007; about 3.72 acres; both master plan parcels) from Google for a park and pickleball courts, with an option for Google to sell | lease report pp.1, 3 | "The City and Google will execute a seven-year lease for the property with Google having an option to sell the property to the City" |

Stage: entitled. I found no permit or construction record (Mountain View permit data isn't on an accessible open portal). The Council's action on the 2026 lease isn't posted in Legistar yet. The lease report doesn't mention the master plan, so what it means for the master plan is open.

Boundary lead: Mountain View parcels, `https://maps.mountainview.gov/arcgis/rest/services/Public/Parcel/MapServer/0`, filtered to `APN IN ('16057004','16057006','16057007','16057008','16057009','16057010','16057011','16057012','16057013','16058001','16058016','16058017','16059005','16059006')`. All 14 match and sum to about 39.8 acres (centroid -122.049, 37.397). This is the same layer and terms as `north-bayshore`. Alternatively, trace Council report Figure 3. Massing lead: master plan (MVGW e1878a1f-…) land-use plan and story ranges; East Whisman Precise Plan Table 7 converts stories to feet (residential: stories × 10 + 20 ft; office: stories × 15 + 20 ft).

Press-only (kept in `reported`): Google is offering the site for sale (Mountain View Voice 2025-06-02; The Real Deal 2025-05-30; San José Spotlight).

Recommendation: INCLUDE as `middlefield-park`. It has 1,900 homes and 1.3M sq ft of office on 40 acres, is entitled, and its DA runs up to 20 years from Jan 2023. A sale or the lease could change its course, so it needs a re-check before launch.

---

## East Whisman Precise Plan (Mountain View)

Documents: Council report, Nov 5, 2019 (MVGW 33f99e61-4af9-4a25-b395-5284a81b4cac); EPC-recommended plan text (MVGW e8594aa2-089b-452b-9920-c1c579db39c4, 212 pp., redlined); EIR resolution (MVGW a1708125-9bab-4f51-ae97-88709253af57); minutes, Nov 5 and Dec 10, 2019.

| field | official value | source | verbatim quote |
|---|---|---|---|
| targets | 5,000 homes (1,000 affordable), 2M sq ft office, 100,000 sq ft commercial, 30 acres parks | Council report p.2 | "Character Area targets include 5,000 new residential units, 1,000 of which will be affordable, 2 million square feet of office, 100,000 square feet of new neighborhood commercial, and 30 acres of parks and open space." |
| area | plan text redline "368412-acre" (368 struck, 412 inserted); the Caltrans letter in the EIR record says 403 acres | plan p.9; EIR resolution | "The 403-acre Plan area" (CONFLICT) |
| adoption | 2019-11-05: Res. 18395 (EIR), 18396 (GPA), 18397 (plan), 18398, 18399; 2019-12-10: Ord. 21.19 (rezoning to P-41), 22.19 | minutes 2019-11-05, 2019-12-10 | "Adopt Resolution No.18397 Adopting the East Whisman Precise Plan" |

Recommendation: EXCLUDE. It is a zoning plan for about 400 acres of many owners, not a project, and its development is built through individual applications. Middlefield Park, the plan's Google master plan (about 38% of the new housing expected in the Mixed-Use Character Area, per its Council report p.16), represents it on the map. Other approved projects in the plan (LinkedIn's 700 E. Middlefield, 400 Logue, 490 E. Middlefield, 685 E. Middlefield, Sobrato's 600 Ellis) are individually below the bar. This follows how `north-bayshore` represents Google's master plan rather than the North Bayshore Precise Plan.

---

## Hosts

All sources in the four records pass `isOfficialSource` as is. The `.gov` hosts are `sfbos.archive.sf.gov`, `media.api.sf.gov`, `www.sf.gov` and `data.sfgov.org`; the others are already listed. Optional additions:
- `legistar1.granicus.com/mountainview/`, Mountain View's Legistar file store. It is the `MeetingFile`/`MatterAttachmentHyperlink` base returned by `webapi.legistar.com/v1/mountainview/`, and it would let records cite council minutes PDFs directly. This is the same pattern as the existing `legistar1.granicus.com/alameda/` entry.
