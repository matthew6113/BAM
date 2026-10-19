# Official-source findings: Central SoMa key sites (San Francisco)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/flower-mart/`, `88-bluxome/`, `655-fourth-street/`, `one-vassar/`, `5m/` and
`central-soma-minutes/`, git-ignored), and live queries of DataSF (development pipeline 2026 Q2 `6jgi-cpb4`,
Planning records `qvu5-m3a2` and `y673-d69b`, DBI permits `i98e-djp9`, DBI inspections `vckc-dh2h`, DBI
complaints `gm2e-bten`, parcels `acdm-wktn`, special use districts `5yf5-ms5f`) and CEQAnet. Page numbers are
PDF page numbers.

Matthew asked on 2026-10-19 for the large towers proposed or being built in San Francisco, "and more". This
group covers the 2018 Central SoMa Plan's "key development sites" (Plan, Part II.D, Figure 1, PDF p. 197: eight
sites, "large, underutilized development opportunities with lot areas ranging from 25,000 square feet to well over
100,000 square feet", p. 196) and anything else large in Central and East SoMa in Planning's pipeline.

Hosts: none to add. Every source is on `sfplanning.org`, `sfplanning.s3.amazonaws.com` (SF Planning's document
store: the S3 mirror of `commissions.sfplanning.org`, cited in the form actually opened), `data.sf.gov` or
`ceqanet.lci.ca.gov`. Not reachable from this session and not cited: `citypln-m-extnl.sfgov.org` (2023+
Planning Commission packets, minutes and CEQA documents), `sfbos.org` and `sfgov.legistar.com` (Board ordinances),
`sf.gov`, `sfplanninggis.org` (Property Information Map), and the press.

URL shorthand:
- PLAN = `https://sfplanning.org/sites/default/files/documents/citywide/Central_Corridor/2018CentralSoMaPlan.pdf`
- S3 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/`; MIN(date) = S3`<date>_cal_min.pdf`
- AG(date) = Planning Commission agenda: AG1214-23 = `https://sfplanning.org/sites/default/files/agendas/2023-12/20231214_cpc%20%28ID%201410056%29.pdf`;
  AG0924-26 = `https://sfplanning.org/sites/default/files/agendas/2026-09/20260924_cpc%20%28ID%201588046%29.pdf`;
  AG1001-26 = `https://sfplanning.org/sites/default/files/agendas/2026-09/20261001_cpc%20%28ID%201589032%29.pdf`;
  AG1008-26 = `https://sfplanning.org/sites/default/files/agendas/2026-10/20261008_cpc%20%28ID%201590027%29.pdf`
- PRJ(id) = `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=<id>`; REC(id) = `https://data.sf.gov/resource/y673-d69b.json?record_id=<id>`;
  PIPE(blklot) = `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=<blklot>`; DBI(n) = `https://data.sf.gov/resource/i98e-djp9.json?permit_number=<n>`

## Summary

| project | key site | stage | size (official) | recommendation |
|---|---|---|---|---|
| `flower-mart` Flower Mart, 610-698 Brannan | 4 | entitled (2019); amendment under review | 6.5 acres; approved 2,032,165 sq ft office, 8-18 stories, to ~236 ft; proposed up to 3,532 homes, height limits 350-600 ft | INCLUDE, boundary only |
| `88-bluxome` 88 Bluxome Street | 7 | entitled (Dec 12, 2025) | 2.61 acres; 1,500 homes in towers of 599 and 528 ft, ~1,777,000 sq ft | INCLUDE, boundary only |
| `655-fourth-street` 655 Fourth Street ("the Creamery") | 8 | entitled (Dec 14, 2023; final Jan 17, 2024) | 1.64 acres; 1,105 homes in towers of 380 and 400 ft | INCLUDE, boundary only |
| `one-vassar` One Vassar, 400 2nd / 645 and 657 Harrison | 3 | entitled (Feb 20, 2020) | 2.36 acres; ~1.5 million sq ft: 350-ft office and residential towers (489 homes), 200-ft hotel (468 rooms) | INCLUDE, boundary + traced massing |
| 598 Brannan Street | 5 | entitled (2019) | ~994,000 sq ft, four mid-rise buildings | lead (hold) |
| 725-765 Harrison Street | 2 | entitled (2019, 2022; extended 2026) | ~981,000 sq ft, 14 stories, 185 ft | lead (hold) |
| 395 3rd Street | — | approved 2023; new SB 423 filing 2026 | 501-524 homes, 45 stories | lead (below bar) |
| 5M (Fifth and Mission) | — | partly built | 688 homes (302 built), 676,000 sq ft remaining | lead (hold; separate pass) |

All four included projects are approved but unbuilt. Three are drawn as boundaries only because no current design
could be read from an official host (Flower Mart's design is in flux; 88 Bluxome's and 655 Fourth's current plans
sit on hosts this session can't reach). Boundaries don't overlap Mission Bay or Mission Rock: 655 Fourth Street
touches Mission Bay's boundary along Townsend Street (7.7 m² overlap, a sliver) and, with One Vassar, overlaps The
Portal's corridor polygon, which is expected (the Downtown Rail Extension runs under Townsend and 2nd streets). The
Railyards (700 4th Street), across Townsend from 655 Fourth, is drawn by another group; the two are 35 m apart.

---

## flower-mart

Recommendation: **INCLUDE** (stage `entitled`, boundary only). A 6.5-acre key site with a 2019 approval for about
2 million sq ft of office and a Development Agreement; the developer is now seeking to amend the agreement and
rezone the site for up to 3,532 homes with height limits of 350 to 600 ft.

How to present it: the stage follows the approvals in hand (2019 entitlements, Development Agreement in effect
from 2020); the program fields show the approved office program and the notes, summary and next milestone carry the
2025-26 proposal. No buildings are drawn: the 2019 design is being replaced and the 2026 proposal is a set of
scenarios (office/lab, residential, mixed-use, institutional), not a design.

Documents read:
- S3`2017-000663ENXOFAPCADVA_amended_combined.pdf` (packet for July 18, 2019, 932 pp.: executive summary pp. 1-7,
  draft LPA motion pp. 8-60; plans skimmed).
- MIN(20190613) p. 5 (informational hearing), MIN(20190718) pp. 8-10 (approvals), MIN(20191212), MIN(20191219) and
  MIN(20200109) p. 4 (Board actions reported to the Commission).
- AG1001-26 pp. 3-4 (informational hearing on the Development Agreement amendment).
- PLAN pp. 196-197 (key sites, Figure 1) and p. 204 (Site 4).
- DataSF: PRJ(2017-000663PRJ), PRJ(2025-008569PRJ), child records on block 3778 (y673-d69b), PIPE(3778047), DBI
  permits on lots 001B to 048.

| field | official value | source | verbatim quote |
|---|---|---|---|
| site | 6 lots, block 3778; ~6.5 acres | packet p. 5; AG1001-26 p. 3 | "for the development of the approximately 6.5-acre Flower Mart site, located on the southern half of the block north of Brannan Street between 5th Street and 6th Street (Assessor’s Parcel Block No. 3778, Lot Nos. 001B, 002B, 004, 005, 047, and 048)[Board File No. 190682]" |
| sponsor | KR Flower Mart, LLC | packet p. 2 | "Project Sponsor: KR Flower Mart, LLC" |
| 2019 program | 3 buildings, 8-18 stories; 2,032,165 sf office, 113,036 sf PDR, 83,459 sf retail, 35,450 sf POPOS | packet p. 2 | "construct three new 8-to 18-story, mixed-use office buildings, containing a total of 2,032,165 sf of office, 113,036 sf of Production, Distribution and Repair (PDR), 83,459 sf of retail, 35,450 sf of privately owned public open space (POPOS), 769 off-street parking spaces" |
| variant | 2,061,380 sf office, 90,976 retail, 22,690 child care, 950 community | packet p. 2 | "A project variant would contain a total of 2,061,380 sf of office, 90,976 sf of retail, 22,690 sf of child care facility, 950 sf community facility" |
| 2019 heights | Blocks 115-236 ft; Market Hall 148 ft; Gateway 200 ft | packet p. 13 | "approximately 115 to 236 feet in height, 625 feet in length and 240 feet in depth"; "approximately 148 feet in height, 525 feet in length and 102 feet in depth"; "approximately 200 feet in height, 175 feet in length and 130 feet in depth" |
| CEQA | covered by Central SoMa Plan EIR (15183), July 3, 2019 | packet p. 6 | "on July 3, 2019, the Planning Department ... determined that the proposed application was exempt from further environmental review under Section 15183" |
| approvals | July 18, 2019: Res. 20483, Motions 20484 (LPA), 20485 (OFA), Res. 20486 (DA) | MIN(20190718) pp. 9-10 | "ACTION: Approved ... RESOLUTION: 20483"; "ACTION: Approved with Conditions ... MOTION: 20484"; "MOTION: 20485"; "ACTION: Adopted a Recommendation for Approval ... RESOLUTION: 20486" |
| first-phase office | 1,355,363 sf (variant 1,384,578) | MIN(20190718) p. 10 | "to authorize up to 1,355,363 sf of office use for Phase 1A of the Project, or 1,384,578 sf of office use for Phase 1A of the Project Variant" |
| DA terms | interim market at 2000 Marin; permanent market or payment; land for affordable housing; $5 million to Sunnydale Hub | MIN(20190718) p. 10 | "construction of a new wholesale flower mart on the Project Site, or alternatively in the event a payment option is exercised, a one-time Developer payment for the construction of a new flower mart at an alternative permanent site; rent subsidy payments to existing flower vendors; relocation of existing flower vendors to a temporary site at 2000 Marin Street; land dedication for affordable housing; enhanced workforce development program; donation of $5,000,000 to the Sunnydale Hub Project" |
| Board | DA and code changes passed second read (Jan 2020) | MIN(20200109) p. 4 | "190682 Development Agreement - KR Flower Mart, LLC - Flower Mart - Fifth and Brannan Streets. Sponsor: Haney. Staff: Samonsky. PASSED Second Read" |
| site permits | 5 applications filed Aug 6, 2019, none issued | DBI(201908068051) to DBI(201908068055) | "to erect a type 1-a, 17-story office, retail and instituional occupancy with 1 basement. (bldg 2)", status "filed" |
| revised project (2025) | base: 5 bldgs to 270 ft, 2,660,700 sf office/lab; variants residential (7 bldgs to 500 ft, ~3,500 units), mixed-use (to 480 ft, ~1,242 units), institutional | PRJ(2025-008569PRJ) | "construction of five new buildings up to 270 feet in height (up to 18 stories) containing 2,660,700 square feet of office/laboratory space"; "Under the Residential Variant, there would be seven buildings with a maximum height of 500 feet ... approximately 3,500 dwelling units" |
| environmental review | 2025-008569ENV opened Sept 24, 2025, "Under Review" | REC(2025-008569ENV) | record_status "Under Review", open_date 2025-09-24 |
| DA amendment filed | DVA-02, MAP-02, PCA-02 opened May 6, 2026 | REC(2017-000663DVA-02) | record_status "Under Review", open_date 2026-05-06 |
| 2026 proposal | up to 3,532 units; new Flower Mart SUD; 160/270 ft limits to 350-600 ft | AG1001-26 pp. 3-4 | "Depending on the development scenario, the project could include up to 3,532 dwelling units; office, retail/commercial, and cultural, institutional, and educational (CIE) uses"; "create a new Flower Mart Special Use District and a Design Standards and Guidelines document. The proposed rezoning would modify the existing height limits of 160 and 270 feet to heights 350 to 600 feet." |
| site now | buildings vacant | PIPE(3778047) | "previously occupied by the Wholesale Flower Market and are now vacant" (case 2026-000246PRX, "PL Filed") |

Stage reasoning: approvals in hand (LPA, office allocation, Development Agreement) and no permit issued → `entitled`.
The amendment is a new formal review, so it's the next milestone, not the stage.

Boundary: DataSF parcels, the six lots; 6.83 acres as drawn against 6.5. Accuracy official.
Massing: none (see above). Press-only facts: none recorded. The developer is commonly called Kilroy; the official
records name only KR Flower Mart, LLC.

Open items: the Board ordinance numbers (sfbos.org blocked); whether the wholesale market has moved (a search result
points to an sf.gov page saying a new market at 901 16th Street opened in 2025; sf.gov couldn't be opened); the type
of environmental document for 2025-008569ENV; the 3,532 vs ~3,500 homes.

---

## 88-bluxome

Recommendation: **INCLUDE** (stage `entitled`, boundary only). SF Planning approved two residential towers of 599
and 528 ft with 1,500 homes on Dec 12, 2025, replacing (in Planning's pipeline) a 2019 office approval.

Which project is current: the pipeline (2026 Q2) lists only the 2025 residential project for the lot ("PL Approved",
2025-12-12), so it's the one shown. But the 2019 office approval hasn't lapsed on record: DBI issued its three
site permits in 2020 and, on Oct 9, 2026, issued amendments to them. Both facts are in the record's stage note and
`verify`.

Documents read:
- DataSF: PRJ(2025-004642PRJ), REC(2025-004642PPS), REC(2025-004642TDM), PIPE(3786037); PRJ(2015-012490PRJ),
  REC(2015-012490ENX-02), REC(2023-009587GPR), REC(2021-009391ZAD); DBI permits, inspections and complaints on 3786/037.
- S3`2015-012490ENXOFAVARc1.pdf` (packet for July 2019, 145 pp.: pp. 1-12), MIN(20190711), MIN(20190725) pp. 9-10.
- PLAN p. 197 (Figure 1, Site 7).

| field | official value | source | verbatim quote |
|---|---|---|---|
| 2025 project | ~2.6-acre lot split in 3; two high-rises; 1,777,000 sf; 1,500 units; 599 ft (785 units) and 528 ft (715 units) | PRJ(2025-004642PRJ) | "an approximately 2.6-acre development lot, which is identified as a “key development site” in the Central SoMa Plan Area. The Project will subdivide the site into three separate parcels. The western and central parcels will be 43,670 square feet (“sf”) and 47,580 sf respectively ... The easternmost parcel, sized 22,690 sf, will be dedicated to the City for future affordable housing development."; "The western building will be 599’ tall and contain approximately 914,000 sf, including a 2,035 square-foot ground floor commercial space, and 785 dwelling units; the eastern building will be 528’ tall and contain approximately 863,000 sf of residential use and 715 dwelling units." |
| parking, park | 465 spaces, 450 bike; Bluxome Linear Park | PRJ(2025-004642PRJ) | "totaling 465 off-street parking spaces and 450 Class 1 bicycle parking spaces"; "the planned Bluxome Linear Park, a new public park within the Bluxome Street right-of-way spanning the north side of Bluxome Street from Fourth to Fifth Streets, which will be constructed as part of the Project" |
| approval | Approved Dec 12, 2025 | PRJ(2025-004642PRJ); PIPE(3786037) | "record_status": "Closed - Approval Ltr Issued", "project_decision": "Approved", "project_decision_date": "2025-12-12"; pipeline "current_status": "PL Approved" (but "has_approved_entitlement": false) |
| affordable | 150 of 1,500 (low income); State Density Bonus | PRJ(2025-004642PRJ); PIPE(3786037) | "number_affordable_units_prop": "150", "state_density_bonus_individual": "CHECKED"; pipeline "bmr_units_low": "150", "state_density": true |
| unit mix | 459 studios, 655 1-BR, 343 2-BR, 33 3-BR (rental) | REC(2025-004642PPS) | "totaling 1,500 rental homes in a mix of 459 studios; 655 1-bedrooms; 343 2-bedrooms; and 33 3-bedrooms" |
| lot | 114,048 sf (2.61 acres) | 2019 packet p. 9 | "on a rectangular-shaped lot measuring 114,048 square feet (2.61 acres) on the majority of the subject block, with frontages on Bluxome, Fifth, and Brannan Streets" |
| 2019 owner | Alexandria Real Estate Equities, Inc. | 2019 packet p. 6 | "Property Owner: Alexandria Real Estate Equities, Inc." |
| 2019 approval | Motions 20493 (LPA), 20494 (OFA), July 25, 2019 | MIN(20190725) pp. 9-10 | "1,197,280 GSF of space, including 775,000 GSF of office, 134,460 GSF of tennis club, 106,220 GSF of 100% affordable housing"; "MOTION: 20493"; "MOTION: 20494" |
| 2023 change | tennis club removed | REC(2015-012490ENX-02) | "Modification of the Large Project Authorization approved per Planning Commission Motion No. 20493 to remove the 134,460 sq. ft. tennis facility from the sub-basement floors of the Project." (Closed - Approved, 2023-08-21) |
| office permits | site permits issued 2020-06-16; demolition issued 2020-07-14; amendments issued 2026-10-09 | DBI(201903215884), DBI(201909131588), DBI(202107265067) | "west bldg. erect 15-story, type 1a, 2 basement, office and retail building", issued 2020-06-16; "to demolish 3 stories tennis club", issued 2020-07-14; "west bldg: alter site permit pa# 201903215884. to remove two basement levels of the podium structure", issued 2026-10-09 |

Stage reasoning: an approval in hand (Dec 2025) and no construction (no first construction document on any permit;
no inspections recorded on the lot) → `entitled`. DBI's demolition permit was issued in 2020 but no completion or
inspection is recorded, so demolition isn't claimed.

Boundary: DataSF parcels, lot 037; 2.65 acres as drawn. Accuracy official.
Massing: none. The record gives heights and floor areas but no footprints or positions; the approval letter and
plans are not on a reachable host.

Press-only (in `reported`, found by search; the articles were blocked here and not read): the sponsor is Strada
Investment Group; the towers are 58 and 51 stories; Alexandria is selling the site
(`https://sfyimby.com/2025/12/plans-approved-for-58-story-88-bluxome-street-promptly-hits-market-in-san-francisco.html`).

Open items: the approval letter and its legal basis; CEQA for the 2025 project; developer; which project goes ahead;
demolition status.

---

## 655-fourth-street

Recommendation: **INCLUDE** (stage `entitled`, boundary only). Two residential towers (380 and 400 ft) with 1,105
homes, approved Dec 14, 2023 as a modification of a 2019 approval; final Jan 17, 2024. Sponsor Tishman Speyer.

Documents read:
- CEQAnet `https://ceqanet.lci.ca.gov/2024010421` and its attachments: the Notice of Exemption (case 2022-011490ENV,
  4 pp., `.../Attachment/xIq6y-`) and the State form (`.../Attachment/vz8e2W`).
- AG1214-23 p. 6 (items 11a-c).
- MIN(20190620) pp. 5-6, MIN(20190905) p. 5; S3`2014-000203ENXCUA%20revised.pdf` (2019 packet, 401 pp.: p. 1).
- DataSF: PRJ(2022-011490PRJ), PRJ(2014-000203PRJ), child records on block 3787, PIPE(3787028), DBI permits.

| field | official value | source | verbatim quote |
|---|---|---|---|
| site | 7 lots, block 3787; 71,290 sf (1.64 acres) | NOE p. 1 | "Block/Lot: 3787/Lots 26, 28, 50 and 161-164 Lot Size: 71,290 square feet (1.64 acres)" |
| sponsor | Tishman Speyer | NOE p. 1 | "Project Sponsor: Veronica Klein, Tishman Speyer" |
| project | podium + two towers, 380 and 400 ft; ~1,032,594 sf residential; 1,105 units | NOE p. 2 | "construct a podium building with two towers rising to approximately 380 and 400 feet in height, respectively, and containing a total of approximately 1,032,594 square feet of residential area. The proposed project would consist of approximately 1,105 dwelling units with a mix of approximately 129 studios, 539 one-bedroom units, 400 two-bedroom units, and 37 three-bedroom units." |
| retail, plaza, parking | 9,857 sf retail; 9,153 sf POPOS; ~284 stalls; 354 bike | NOE p. 2 | "9,857 square feet of ground-floor retail use"; "a plaza with 9,153 square feet of exterior privately owned, publicly accessible open space (POPOS)"; "approximately 284 vehicle parking stalls" |
| screens | 405 and 435 ft with screening | AG1214-23 p. 6 | "two residential towers up to 380 and 400 feet tall, respectively (405’ and 435’ tall inclusive of rooftop screening/mechanical equipment)"; "Other features include six off-street loading spaces, 271 parking spaces" |
| approval | decided Dec 14, 2023 (LPA); final Jan 17, 2024 | NOE pp. 1, 3 | "Final Approval Date: January 17, 2024"; "The City and County of San Francisco decided to carry out or approve the project on December 14, 2023. The approval action for the proposed project is large project authorization by the San Francisco Planning Commission. The project was officially approved on January 17, 2024, when no appeal of the General Plan Evaluation was filed during the 30-day appeal period." |
| CEQA | Community Plan Exemption (15183), General Plan Evaluation dated Nov 30, 2023 | NOE p. 3; PRJ(2022-011490PRJ) | "Community Plan Exemption (Sec. 21083.3; 15183)"; "environmental_document_date": "11/30/2023" |
| units in data | 1,096 | PRJ(2022-011490PRJ); PIPE(3787028) | "number_of_units_prop": "1096" (the same record's description says 1,105); pipeline "proposed_units": "1096", "affordability_type": "Fee" |
| 2019 approval | Motions 20470 and 20471, June 20, 2019: four towers 400/360 ft, 960 units, 38-room hotel | MIN(20190620) pp. 5-6; 2019 packet p. 1 | "MOTION: 20470"; "MOTION: 20471"; "construction of two new buildings that appear as four separate towers (Towers 1A, 2A, 1B and 2B) measuring 400 and 360 feet in height" |
| 2019 sponsor | 655 4th Owner, LLC | 2019 packet p. 1 | "Project Sponsor: 655 4th Owner, LLC" |
| appeal | withdrawn (Sept 2019) | MIN(20190905) p. 5 | "The appeal for 655 4th Street was withdrawn." |
| permits | 3 site permit applications (2019), none issued | DBI(201909262783), DBI(201909262785) | "tower 1. to erect 40 stories, 3 basements, type i-a, 494 residential units"; "tower 2. erect a 40 stories, 501 dwelling residential units"; status "filed" |

Stage reasoning: final approval Jan 17, 2024; no permit issued → `entitled`.

Boundary: DataSF parcels, the seven lots; 1.65 acres as drawn. Accuracy official.
Massing: none. The 2023 packet (`citypln-m-extnl.sfgov.org/Commissions/CPC/12_14_2023/Commission%20Packet/2022-011490ENXCUAPCA.pdf`)
and the GPE figures are on a blocked host; the 2019 plans are a superseded four-tower design.

Press-only: none recorded (story counts of 38 and 40 appear in press coverage found by search, not read).

Open items: Dec 14, 2023 motion numbers (minutes on a blocked host); 1,105 vs 1,096 homes; affordable housing
(fee); the Downtown Rail Extension fee waiver ordinance (Board File 231164, heard as item 11a).

---

## one-vassar

Recommendation: **INCLUDE** (stage `entitled`, boundary + traced massing). Three buildings, about 1.5 million sq ft,
approved Feb 20, 2020; site permits for two buildings approved by DBI in 2023 but not issued.

Documents read:
- S3`2012.1384PRJ.pdf` (packet for Feb 20, 2020, 592 pp.: pp. 1-35, 55-72, 153-160, plans skimmed).
- MIN(20200130) p. 15 (informational hearing), MIN(20200220) pp. 8-10 (approvals).
- CEQAnet `https://ceqanet.lci.ca.gov/Project/2020050176` and `/2020050176/2` (Notice of Exemption, May 7, 2020).
- DataSF: PRJ(2012.1384), its child records, PIPE(3763001), DBI permits on the site's lots; parcels on block 3763.

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, size | One Vassar; ~1.5 million sf | packet p. 14 | "Commonly referred to as the “2nd and Harrison” or ʺOne Vassarʺ (identified as Key Site No. 3 in the Central SoMa Area Plan), the One Vassar project (the ʺProjectʺ) will create an approximately 1.5 million‐square foot mixed‐use development" |
| program | 489 units; 468 hotel rooms; 493,115 gsf office; 42,013 PDR; 14,000 child care; 37,551 retail | packet p. 14 | "approximately 42,013 gross square feet of production, distribution and repair (PDR) use, approximately 489 residential units, a hotel with 468 guestrooms, approximately 493,115 gross square feet (gsf) of office (consisting of approximately 430,000 new gsf at 400 2nd Street, and approximately 63,115 gsf of existing legal office use at 645 Harrison Street)" |
| Building 1 | 27 stories, 350 ft (385 with mech.) | packet p. 15 | "a 350‐foot tall (or 385‐feet tall with the rooftop mechanical equipment), 27‐story office building" |
| Building 2 | 15-story addition, 200 ft; existing podium 55 ft | packet pp. 15, 71 | "retain the historic building and construct a 15‐story vertical addition for a total height of 200‐ft (or 220‐ft with rooftop mechanical equipment) containing approximately 468 guestrooms"; "will measure approximately 200 feet tall, with a 15‐foot‐tall mechanical screen, for a total height of 215 feet. The building’s podium along all facades will have a height of 55 feet, which is the height of the existing structure." |
| Building 3 | 35 stories, 350 ft; 85-ft podium | packet pp. 15, 71 | "a 350‐foot tall (or 385 feet with the rooftop mechanical equipment), 35‐story residential building consisting of up to 489 dwelling units"; "The building’s podium along all facades will have a height of 85 feet." |
| podiums, floor plates | 85-ft podiums; plates 14,935 / 16,000 / 12,000 sf | packet pp. 70, 160 | "The building’s podium along all facades will have a height of 85 feet built to the property line with the exception of the northeast corner"; bulk diagram: "12,000 SF ... 14,935 SF FLOOR PLATE ... 16,000 SF ... FLOOR PLATE" |
| site | 12 lots, 102,694 sf (2.36 acres) | packet p. 24 | "Cumulatively, the 12 lots have a lot area of approximately 102,694 square feet (2.36 acres), with approximately 606‐ft of frontage along Harrison Street, 200‐ft of frontage along 2nd Street" |
| Perry Street extension | on Caltrans property | packet p. 32 | "the proposed private driveway (the Perry Street extension to 2nd Street on Caltrans property)" |
| affordable | fee at 33% | packet p. 17 | "The Project Sponsor must pay an Affordable Housing Fee at a rate equivalent to thirty‐three percent (33%) because it is a rental project that is providing one hundred and ten percent (110%) of the otherwise required amount" |
| CEQA | 15183 determination Feb 5, 2020; NOE May 7, 2020 | packet p. 17; CEQAnet 2020050176/2 | "on February 5, 2020, the Planning Department ... determined that the proposed application was exempt from further environmental review under Section 15183"; NOE "Received 5/7/2020" |
| approvals | Feb 20, 2020: Motions 20665 (LPA), 20666 (OFA), 20667 (CUA) | MIN(20200220) pp. 9-10 | "ACTION: Approved with Conditions with corrections submitted by Staff ... MOTION: 20665"; "MOTION: 20666"; "MOTION: 20667" |
| owner | One Vassar, 433 California St. | packet p. 14; CEQAnet | "Property Owner: One Vassar 433 California Street, 7th Floor"; NOE contact "Sharon Lai, One Vassar ... Project Applicant" |
| permits | office and residential site permits "approved" 2023, hotel "filed"; demolitions filed 2023; none issued | DBI(201912068928), DBI(201912068933), DBI(201912068937), DBI(202312223011) | "to erect 27 stories, 3 basements, type i-a, office, pdr, retail building", status "approved" 2023-06-23; "to erect 35 stories, 4 basements, type i-a, 489 residential with childcare & retail building", "approved" 2023-11-13; "retain the historic 4 story building & construct new 237,750 sf vertical addition", "filed" |

Stage reasoning: approvals in hand, no permit issued, no construction → `entitled`. (The pipeline's "BP Approved"
means DBI approved a permit, not issued it.)

Boundary: DataSF parcels, lots 001, 078, 079, 080, 080A, 081, 099, 100, 101, 105 and 113, plus 125. The approval's
lot 112 was retired in 2019 (parcel layer: map drop 2019-05-29) and split into lot 125 (416 2nd Street, 7,432 sq ft,
between lot 113 and the AC Transit yard) and lot 126 (the bus yard, 124,212 sq ft). Lot 125 is drawn because the
traced Building 1 podium extends into it and the approval's 2nd Street frontage needs it; lot 126 is not. 2.18
acres as drawn against 2.36. Accuracy approximate.

Massing: `pipeline/bam_pipeline/sites/massing_one_vassar.py`. Packet p. 159 ("Typical tower plans", 1" = 50') is a
vector drawing; registered to six lot corners (lots 105, 001, 099, 081) by a similarity, RMS 0.22 m, fitted scale
0.6977 ft/pt against the drawing's 0.6944. Traced areas: office tower 14,738 sq ft (bulk diagram 14,935), hotel
floor 16,180 (16,000), residential tower 11,804 (12,000); podiums 8,746 and 8,766 sq ft beside the towers; nothing
falls outside the lots. Features: 400 2nd tower 350 ft and podium 85 ft; 645 Harrison hotel addition from 55 to
200 ft (existing building left to the base map); 657 Harrison tower 350 ft and podium 85 ft. All `entitled`,
illustrative. Source PDF pinned (sha256 5d42b2f6…d280).

Press-only (in `reported`, found by search; the article was blocked here and not read): a January 2024 three-year
extension, lower affordable housing fees and changes to the residential tower; Cresleigh Management and Stanford
Hotels behind the project (`https://therealdeal.com/san-francisco/2024/01/17/cresleigh-management-moves-ahead-with-triple-towers-in-sf/`).
No Planning record or 2024-2026 Planning Commission agenda mentioning One Vassar was found.

Open items: any 2024 extension or modification; current owner; lot 112 and the Perry Street extension; the hotel
permit.

---

## Leads not added

- **598 Brannan Street** (Key Site 5, "Park Block"; case 2012.0640; block 3777 lots 045, 050, 051, 052): three office
  buildings and a 100% affordable residential building (up to 72 homes), 922,737 sq ft of office and about
  994,000 sq ft of non-residential space in all (PIPE(3777045)), with a special exception for 25 ft above the height
  limit; approved June 6, 2019 (Motions 20459 and 20460, MIN(20190606) pp. 9-10); site permits filed Dec 2019, none
  issued. `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20190606_cal_min.pdf`. Recommendation: hold;
  just under the 1M sq ft bar and not a tower. Could be added boundary-only.
- **725-765 Harrison Street** (Key Site 2; case 2005.0759; block 3762 lots 117, 148, 149, 152): a 14-story, 185-ft
  office building of about 981,000 sq ft (810,000 office), approved Dec 12, 2019 (Motion 20597), modified June 16,
  2022 (Motion 21128); an 18-month extension to March 24, 2028 was heard Sept 24, 2026 (AG0924-26 p. 4) and the
  record is "Closed - Approved" Sept 29, 2026 (REC(2005.0759ENX-03)). Recommendation: hold; just under the bar,
  mid-rise.
- **395 3rd Street** (block 3750 lot 086): approved June 29, 2023 (PIPE(3750086): 524 units); a new SB 423 notice
  of intent (Sept 11, 2026) is for a 45-story building with 501 homes (AG1008-26 p. 5). Height in feet not found.
  Recommendation: exclude for now (below 1,000 homes); recheck when the SB 423 application is filed.
- **5M** (Fifth and Mission Special Use District; cases 2011.0409, 2018-011363PRX; about 4 acres): pipeline lists
  688 homes (302 completed in a 21-story building) and 676,000 sq ft of non-residential space, "PL Approved". The
  2015 approvals are on hosts not reachable here (S3 minutes for Sept-Oct 2015 return 403); outside Central SoMa.
  `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=3725090`. Recommendation: hold for a separate pass (stage
  would be `partial`).
- **505 Brannan Street** (block 3786 lot 038, case 2015-009704): an 11-story addition on a 6-story office building,
  about 296,000 sq ft in all; heard and approved Dec 14, 2023 (AG1214-23 pp. 7-8; PIPE(3786038) "PL Approved"). Exclude (below bar).
- **490 Brannan Street** (Key Site 6, "Wells Fargo"; block 3776 lot 025, case 2020-005610): 286,097 sq ft
  non-residential, building permit filed 2022 (PIPE(3776025)). Exclude.
- **180 Hawthorne / 650 Harrison Street** (case 2017-004921): 320 homes, approved Oct 8, 2025 (PIPE(3750009)). Exclude.
- **555 Beale Street (Seawall Lot 330)** (case 2025-011323): 568 homes, application filed May 19, 2026
  (PIPE(3771002)). Exclude (below bar, unapproved); likely a waterfront group's.
- **Key Site 1, "5th and Howard"** (block 3732): no large project in the 2026 pipeline. Nothing to add.
- **Railyards (700 4th Street)**: NOP Sept 30, 2026 (SCH 2026091295); already drawn by another group (`railyards`).
- Outside this group, seen in the pipeline: 620 Folsom Street (826 homes, filed 2022, 320-I) and Transbay Block 4
  (681 homes, filed 2022) in the Transit Center District.
