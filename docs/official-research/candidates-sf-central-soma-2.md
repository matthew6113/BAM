# Official-source findings: Central SoMa key sites, part 2 (San Francisco)

Checked 2026-10-22 against documents downloaded and read in full text (local copies in
`data/raw/official/598-brannan/`, `725-harrison/` and `central-soma-2-minutes/`, git-ignored), and live queries of
DataSF (development pipeline 2026 Q2 `6jgi-cpb4`, Planning records `qvu5-m3a2` and `y673-d69b`, DBI permits
`i98e-djp9`, DBI inspections `vckc-dh2h`, parcels `acdm-wktn`). Page numbers are PDF page numbers.

Matthew asked on 2026-10-19 for the large towers proposed or being built in San Francisco, "and more". The first
Central SoMa pass (`candidates-sf-central-soma.md`) held back two of the 2018 Central SoMa Plan's key development
sites as just under 1 million sq ft and mid-rise: Key Site 5, "Park Block" (598 Brannan Street), and Key Site 2,
"4th and Harrison" (725-765 Harrison Street). Matthew asked to add both. This note confirms and extends them.

Hosts: none to add. Every source is on `sfplanning.org`, `sfplanning.s3.amazonaws.com` (SF Planning's document
store: the S3 mirror of `commissions.sfplanning.org`, cited in the form actually opened) or `data.sf.gov`. Not
reachable from this session and not cited: `citypln-m-extnl.sfgov.org` (the June 16, 2022 and Sept 24, 2026
packets for 725 Harrison, and Planning Commission minutes after July 2022), `sfbos.org` and `sfgov.legistar.com`
(Board File 180550, the 639 Bryant / 2000 Marin land exchange), `sf.gov`, `sfplanninggis.org` and the press.
No CEQAnet filing for either project was found (its listings of San Francisco Notices of Exemption for June to Sept
2019, Dec 2019 to March 2020 and June to Sept 2022 were checked; keyword search doesn't work there).

Agendas and minutes searched for both case numbers and addresses: S3 minutes for every Thursday from March 2020 to
July 2022 (95 found), sfplanning.org agendas from July 2022 to Dec 2023 (77) and Jan 2024 to Oct 22, 2026 (132, the
FiDi group's downloads). Hits are listed below; there are none for 598 Brannan after Sept 2021.

URL shorthand:
- S3 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/`; MIN(date) = S3`<date>_cal_min.pdf`
- PLAN = `https://sfplanning.org/sites/default/files/documents/citywide/Central_Corridor/2018CentralSoMaPlan.pdf`
- AG0616-22 = `https://sfplanning.org/sites/default/files/agendas/2022-06/20220616_cal.pdf`;
  AG0924-26 = `https://sfplanning.org/sites/default/files/agendas/2026-09/20260924_cpc%20%28ID%201588046%29.pdf`
- PRJ(id) = `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=<id>`; REC(id) = `https://data.sf.gov/resource/y673-d69b.json?record_id=<id>`;
  PIPE(blklot) = `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=<blklot>`; DBI(n) = `https://data.sf.gov/resource/i98e-djp9.json?permit_number=<n>`;
  INSP(n) = `https://data.sf.gov/resource/vckc-dh2h.json?reference_number=<n>`

## Summary

| project | key site | stage | size (official) | recommendation |
|---|---|---|---|---|
| `598-brannan` 598 Brannan Street | 5 | construction (affordable building only; office buildings not started) | 4.5 acres; 922,737 sf office in three buildings of 160, 185 and 150 ft; ~39,661 sf public park; 85 affordable homes on the dedicated lot | INCLUDE, boundary + traced massing |
| `725-harrison` 725-765 Harrison Street | 2 | entitled (2019, modified 2022, extended Sept 2026 to March 24, 2028) | 2.39 acres; 14 stories, 185 ft, ~981,000 gsf, 810,000 sf office | INCLUDE, boundary + traced massing |

Neither boundary overlaps a mapped one. 598 Brannan is 25 m from the Flower Mart (across 5th Street) and from
88 Bluxome (across Brannan Street). 725 Harrison is more than 60 m from every mapped boundary; One Vassar, the next
key site east across 3rd Street, is 139 m away, and The Portal's corridor 297 m.

---

## 598-brannan

Recommendation: **INCLUDE** (stage `construction`, boundary + traced massing). Three office buildings around a new
public park, approved June 6, 2019 (Phase 2 office allocation Dec 3, 2020). DBI issued the site permits for
Buildings 1 and 2 in 2021 and the old buildings were demolished that year, but nothing has been built on the office
sites since. The affordable housing building on the lot the project gave the City (160 Freelon Street, 85 homes) has
been under construction since July 15, 2025.

How to present the stage: SPEC's `construction` is "vertical construction on at least one building", and 160 Freelon
Street is the project's Building 4 site in the approval, in MOHCD's dedication letter and in Planning's 2026 records
("the 598 Brannan mixed-use development that includes an affordable housing project at 160 Freelon"). The stage note
says plainly that only the affordable building is rising. If the lead prefers to treat 160 Freelon Street as a
separate project, the stage would be `entitled` (approvals and two site permits in hand; demolition done in 2021; no
construction on the office buildings).

Documents read:
- S3`2012.0640ENX.pdf` (packet for June 6, 2019, 390 pp.: executive summary pp. 1-5, draft LPA motion pp. 6-43,
  OFA motion pp. 52-62, fee waiver agreement pp. 63-94, plans pp. 95-190 (site plan p. 115, roof plan p. 116,
  elevations pp. 156-171, data table p. 103), Community Plan Evaluation pp. 191-363, MOHCD letter pp. 376-377,
  sponsor brief pp. 378-384).
- MIN(20190606) pp. 8-10; MIN(20201112) p. 1 (continued); MIN(20201203) p. 7; MIN(20210909) pp. 7-8; MIN(20200924) p. 7.
- PLAN p. 197 (Figure 1) and p. 207 (Site 5).
- DataSF: PRJ(2012.0640) and its 11 child records; PRJ(2022-008873PRJ), REC(2022-008873APL); REC(2023-000990GPR),
  REC(2019-022611GPR), REC(2019-022107LLA), REC(2025-006139MIS), REC(2026-004471ENF), REC(2026-008242GEN);
  PIPE(3777045), PIPE(3777052); DBI permits and inspections on lots 026, 045, 050, 051, 052, 176, 177; parcels on block 3777.

| field | official value | source | verbatim quote |
|---|---|---|---|
| site | 4 lots, block 3777; ~4.5 acres; 195,467 sf | MIN(20190606) p. 8; packet pp. 10-11 | "598 BRANNAN STREET – northeast intersection of 5th and Brannan Streets, Lots 045, 050, 051 & 052 on Assessor’s Block 3777"; "The Project site spans four separate parcels (collectively encompassing approximately 4.5 acres)"; "The Project site has a total area of 195,467 square feet" |
| sponsor, owner | Brannan & Bryant Street, LLC; The Hearst Corporation | packet p. 6 | "Project Sponsor: Brannan & Bryant Street, LLC One Bush Street, Suite 450"; "Property Owner: The Hearst Corporation" |
| sponsor's parent | Tishman Speyer | packet p. 376 (MOHCD, May 20, 2019); p. 337 | "from Brannan & Bryant, LLC, an affiliate of the Tishman Speyer (Sponsor)"; CPE checklist "Project Sponsor Tishman Speyer One Bush Street" |
| program | three 150-185 ft, 10-13-story office buildings; 922,737 gsf office; 60,471 gsf retail/PDR; 5,546 gsf child care; 200 parking | packet pp. 1-2 | "construct three 150-to-185-foot-tall, 10-to-13-story, mixed-use office buildings in two phases"; "Buildings 1, 2 and 3 would contain a total of approximately 922,737 gsf of office space, approximately 60,471 gsf of ground-floor retail/PDR space and 5,546 gsf of institutional child care space"; "collectively containing 200 off-street parking spaces" |
| Building 1 | 160 ft (180 with screen); 289,087 sf office; 11 floors | packet p. 1; p. 116 | "reaching a height of 160 feet (180 ft. to top of rooftop mechanical screening), located at the northeast corner of Brannan and 5th streets, with 289,087 square feet of office use and 22,831 square feet of combined retail and PDR"; roof plan "BUILDING 1 11 FLOORS 159'6" T.O. ROOF" |
| Building 2 | 185 ft (205); 422,049 sf office; 13 floors | packet p. 1; p. 116; p. 161 | "reaching a height of 185 feet (205 ft. to top of rooftop mechanical screening), located at the southeast corner of 5th and Welsh streets, with 422,049 square feet of office use"; "185’-0” (25’-0” HEIGHT BONUS FOR AFFORDABLE HOUSING/PARK)" |
| Building 3 | 150 ft (170); 211,601 sf office; child care; 10 floors | packet p. 2; p. 116 | "reaching a height of 150 feet (170 ft. to top of rooftop mechanical screening), located mid-block on Bryant Street, with 211,601 square feet of office use, 11,054 square feet of combined retail and PDR and 5,546 square feet of child care facility"; "BUILDING 3 10 FLOORS 149'9" T.O. ROOF" |
| step-back levels | B1 level 3 at 31 ft; B2 level 6 at 73 ft; B3 level 6 at 76 ft | packet pp. 156, 161, 168 | "B1 LEVEL 3 31’-0”"; "B2 LEVEL 6 73’-0”"; "B3 LEVEL 6 76’-0”" |
| park, POPOS | ~39,661 sf public park, City-owned, built and maintained by sponsor; 19,336 sf POPOS | packet pp. 2-4; MIN(20190606) p. 8 | "separated by a central, approximately 39,661-square-foot public park"; "The Project Sponsor has agreed to construct and maintain this public park"; "approximately 19,336 square feet of privately-owned public open space (POPOS)" |
| affordable housing | 12,800 sf parcel to MOHCD; up to 72 homes expected | packet pp. 2, 37; PRJ(2012.0640) | "dedicate an approximately 12,800 square foot parcel to the Mayor’s Office of Housing and Community Development for construction of a future 100% affordable housing building (Building 4)"; "containing up to 72 affordable dwelling units" |
| land swap | 639 Bryant (City/SFPUC, 59,812 sf) for 2000 Marin Street | packet p. 10; REC(2019-022611GPR) | "This agreement has already been tentatively approved by the Board of Supervisors via Conditional Land Disposition and Acquisition Agreement-Potential Exchange of 639 Bryant Street for 2000 Marin Street (Board of Supervisors File No. 180550)"; GPR "Closed - Approved", 2020-03-10 |
| CEQA | Central SoMa Plan EIR (15183), May 29, 2019 | packet p. 4 | "on May 29, 2019, the Planning Department ... determined that the proposed application was exempt from further environmental review under Section 15183" |
| approvals | June 6, 2019: Motions 20459 (LPA), 20460 (OFA, 711,136 sf), Resolution 20461 (park fee waiver) | MIN(20190606) pp. 9-10 | "ACTION: Approved with Conditions as amended by Staff and adding an 18-month update report ... MOTION: 20459"; "to authorize 711,136 square feet of office space ... MOTION: 20460"; "ACTION: Directed the Planning Director to enter into Agreement ... RESOLUTION: 20461" |
| Phase 2 allocation | Dec 3, 2020: Motion 20816, 211,601 sf | MIN(20201203) p. 7 | "Request for an Office Development Authorization ... for Phase 2 or approximately 211,601 gross square feet of office use"; "ACTION: Approved with Conditions ... MOTION: 20816" |
| validity | 3 years for a site permit to issue | packet p. 43 | "The authorization and right vested by virtue of this action is valid for three (3) years from the effective date of the Motion. The Department of Building Inspection shall have issued a Building Permit or Site Permit to construct the Project" |
| site permits | B1, B2 issued 2021-03-17; B3 filed 2019-12-13 | DBI(201909060913), DBI(201909060914), DBI(201912139477) | "to erect a type 1-a, 11-story with one basement office and retail building. (building 1)", "issued" 2021-03-17; "to erect 13 stories, 1 basement, type i-a, office, retail bldg (building ii)", "issued" 2021-03-17; "to erect a new 10 story, 1 basement office, retail bldg.(bldg 3)", "filed" |
| demolition | 590-598 Brannan and 645 Bryant, final inspection 2021-06-25 | DBI(202002114084), DBI(202005187585); INSP | "to demolish a 2-story warehouse with office and retail.", "complete" 2021-06-25; "demolition of a type 3 1 story industrial", "complete"; inspection "FINAL INSPECT/APPRVD", "PASSED" |
| shoring | cancelled | DBI(202107194611) | "temporary excavation. shoring system for the brannan st project", "cancelled" 2024-07-02 |
| project record | On hold | PRJ(2012.0640) | "record_status": "On Hold" |
| site now | parking | REC(2025-006139MIS), REC(2026-008242GEN) | "POL referral - Commercial Parking Lot; Recommend approval" (590 Brannan, closed approved 2025-07-30); "Temporary Use Authorization: Temporary private parking lot on portion of site comprising the 598 Brannan mixed-use development that includes an affordable housing project at 160 Freelon." (submitted 2026-09-16) |
| 160 Freelon link | the dedicated parcel | REC(2023-000990GPR) | "Owner desires to satisfy a portion of the Affordability Requirement for the Principal Project through a land dedication"; "MOHCD has identified a Project Sponsor who intends construct a nine (9) story multi-family residential building with 85 affordable housing units"; "15 studios, 24 one-bedrooms, 22 two-bedrooms, 23 three-bedrooms, and 1 managers unit" |
| 160 Freelon project | 85 homes, 12,800 sf parcel; AB 2162 | PRJ(2022-008873PRJ); PIPE(3777052) | "This 100% affordable housing project will provide approximately 85 new residential units ... on a 12,800-square-foot (0.3 acre) parcel"; "25% of units will be set aside for permanent supportive housing making the project eligible for AB 2162"; applicant "160 Freelon Housing Partners, L.P."; pipeline "approved_date_planning": "2023-02-21", "pipeline_affordable_units": "84", "current_status": "Construction" |
| 160 Freelon permit | issued 2024-05-13; first construction document 2025-07-15; partial rough frame passed 2026-09-24 | DBI(202209283327); INSP(202209283327) | "priority processing, 100% affordable housing - construct 9-story, 85 dwelling units, type 1-b building.", "issued", "first_construction_document_date": "2025-07-15"; inspection "ROUGH FRAME, PARTIAL", "PASSED", 2026-09-24 |
| parcels | lot 052 retired 2025, now lots 176 (160 Freelon St, 13,291 sf) and 177 (639 Bryant St) | DataSF acdm-wktn | 3777052 "date_map_drop" 2025-09-18; 3777176 "160 FREELON ST"; 3777177 "639 BRYANT ST" |
| plan | Key Site 5, "Park Block"; park a very high priority | PLAN p. 207 | "Given the limited opportunities to identify a site for a park of this size, the creation of this park is a very high priority of the Plan." |
| office cap | allocation drawn from the Central SoMa reserve | MIN(20210909) pp. 7-8 | "the full allocation for Brannan Street needed to come out of the Central SoMa reserve" |

Stage reasoning: see above. The 2019 approval's validity required a site permit within three years; DBI issued two
in March 2021, so the approval wasn't left to lapse, but no construction on the office buildings is recorded and
Planning's project record reads "On Hold". No 2022-2026 Planning Commission item on 598 Brannan was found.

Boundary: DataSF parcels, lots 045, 050, 051 and the two successors of lot 052 (176 and 177); 4.5 acres as drawn
against the approval's 195,467 sq ft (4.49 acres). Accuracy official. (The executive summary also lists lot 026, a
small residential lot at 146-150 Freelon Street; the motions and minutes don't, so it isn't drawn.)

Massing: `pipeline/bam_pipeline/sites/massing_598_brannan.py`. The site plan (p. 115) and roof plan (p. 116) are
vector drawings at 1" = 80'. Each is registered to DataSF lot corners read from the outlines of the neighbouring
buildings drawn on the lot lines: seven corners for the site plan (RMS 0.19 m, fitted scale 1.1147 ft/pt against
1.1111) and six for the roof plan (RMS 0.16 m, 1.1186 ft/pt). Features: Building 1 roof outline at 160 ft (31,947 sq
ft) and the rest of its ground floor to 31 ft; Building 2 at 185 ft (33,271 sq ft) and base to 73 ft; Building 3 at
150 ft (17,309 sq ft) and base to 76 ft; all `entitled`, illustrative, nothing outside the lots. The typical upper
floor areas in the plan set (30,039, 30,901-33,350 and 19,756 gsf) match. 160 Freelon Street is drawn as its lot
(13,291 sq ft) with no height, kind "block", stage `construction`: the building's height in feet isn't in any
record read (the 2019 sketch was 7 floors, 75 ft, with 72 homes; the building now rising has nine stories and 85
homes). Source PDF pinned (sha256 9d8e7536…3490). All geometries valid.

Press-only facts: none recorded.

Open items: whether and when the office buildings go ahead; the park's delivery; the land exchange (Board File
180550); 160 Freelon Street's height and opening; the in-kind agreement record 2012.0640IKA (opened July 23, 2024,
"Complete"); lot 026.

---

## 725-harrison

Recommendation: **INCLUDE** (stage `entitled`, boundary + traced massing). A 14-story, 185-ft office building of
about 981,000 gsf (810,000 sq ft office), approved Dec 12, 2019 and modified June 16, 2022; its approvals expired on
June 16, 2025 and an 18-month extension to March 24, 2028 was on the Sept 24, 2026 agenda; Planning closed the
extension record as approved on Sept 29, 2026.

Lot reconciliation: the 2019 approval names lots 106, 108, 109, 112, 116 and 117 (102,067 sq ft); the 2022 approval
adds lot 113 (759 Harrison Street) and names "Lots 148, 149, and 113"; the 2026 agenda names "Lots 117, 148, 149, and
152". The parcel layer shows the six 2019 lots retired (recorded Dec 31, 2020) into lots 148 (the office site,
87,135 sq ft) and 149 (the 15,000 sq ft affordable housing lot), and lots 113 and 148 merged into lot 152 (recorded
Dec 19, 2022; 89,259 sq ft). So the current site is lots 152 and 149 (104,302 sq ft against the 104,188 in Planning's
record); the pipeline still keys the project to the retired lot 117.

Documents read:
- S3`2005.0759ENXOFAVAR.pdf` (packet for Dec 12, 2019, 385 pp., partly scanned: memo p. 1, executive summary pp.
  3-6, MOHCD letter pp. 19-20, Community Plan Evaluation pp. 21-24, draft LPA motion pp. 239-308 (clean copy),
  plans pp. 340-385 (lot lines p. 340, phasing p. 343, section p. 356, floor plans pp. 359-367)).
- MIN(20191212) pp. 9-10 (from the first group's downloads); MIN(20220616) pp. 14-15; AG0616-22 p. 8 (packet link
  only; the packet is on a blocked host); AG0924-26 pp. 4-5.
- PLAN p. 200 (Site 2).
- DataSF: PRJ(2005.0759) and its 21 child records; REC(2023-002967ENX), REC(2022-006757LLA), REC(2025-005002MIS);
  PIPE(3762117); DBI permits on block 3762 lots 106-117, 148, 149, 152; parcels on block 3762.

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, key site | "4th and Harrison" Key Development Site | packet p. 242 | "Commonly referred to as the “4th and Harrison” Key Development Site" |
| 2019 site | 6 lots, 102,067 sf (2.34 acres) | packet p. 243 | "Cumulatively, the six lots have a lot area of approximately 102,067 square feet (2.34 acres), with approximately 606‐ft of frontage along Harrison Street, 160‐ft of frontage along 4th Street, and 671‐ft of frontage along Perry Street" |
| sponsor, owner | Boston Properties, LP; Barret Block Partners, LP | packet p. 239 | "Project Sponsor: Aaron Fenton Boston Properties, LP Four Embarcadero Center"; "Property Owner: Barret Block Partners, LP Burlingame, CA" (drawings: "BARRETT BLOCK PARTNERS, LLP") |
| 2019 project | 14 stories, 185 ft, ~935,000 sf; 770,000 sf office | packet p. 242 | "new construction of a 14‐story, 185‐ft tall, mixed‐use building approximately 935,000 gross square feet in total (excluding the affordable housing)"; "approximately 770,000 square feet of office space, 3,900 square feet of retail with four micro‐retail spaces, 29,100 square feet devoted to two PDR spaces, 3,000 square feet of child care use" |
| massing | two parts; screens to 205 and 196.5 ft | packet p. 242 | "one structure that has two separate massing components: the larger, oblong‐shaped structure with the massing towards Harrison and Fourth Streets (western portion), and a smaller spheroid‐shaped structure with the massing running diagonally from Harrison to Perry Streets fronting the mid‐block paseo (eastern portion). The structure will be approximately 185 feet tall, with a 20‐foot‐tall mechanical screen at the western portion, for a total height of 205 feet, and an 11‐foot‐6‐inch‐tall mechanical screen at the eastern portion, for a total height of 196 feet 6 inches." |
| podium | six-story, 80-ft podium | packet p. 21 (CPE) | "a six-story,80-foot-tall podium with two eight-story oval-shaped mid-rise buildings above" |
| floor levels | L7 80'-1", L11 132'-1", L14 171'-1", roof 185' | packet p. 356 | "LEVEL 7 80' - 1""; "LEVEL 11 132' - 1""; "171' - 1""; "LIMIT 185' - 0"" |
| phases | Phase I west (505,000 sf office), Phase II east | packet pp. 4, 312 | "Phase I: 505,000 gsf of office"; "the Commission authorizes office use for ONLY Phase I in the western portion of the Commercial Building" |
| affordable housing | 15,000 sf lot to MOHCD; anticipated 85 ft, up to 144 homes | packet pp. 240, 242; p. 19 | "the dedication of a 15,000 square foot portion of the lot to the Mayor’s Office of Housing and Community Development (“MOHCD”) for the construction of an 8‐story, 85‐foot tall building with up to 144 dwelling units"; "The final layout of the Affordable Housing Building will ultimately be decided by MOHCD."; MOHCD Dec 2, 2019: "conditionally accepts the dedication of a portion of725 Harrison (Site) for affordable housing development from Boston Properties, Inc." |
| CEQA | CPE Dec 4, 2019; 2022 CPE dated 05/17/2022 | packet p. 1; PRJ(2005.0759) | "On December 4, 2019, the Department determined that the Project did not require further environmental review under Section 15183"; "environmental_document_type": "Community Plan Evaluation", "environmental_document_date": "05/17/2022" |
| 2019 approvals | Dec 12, 2019: 20597 (LPA), 20598 (OFA, 505,000 sf); variance intent | MIN(20191212) pp. 9-10 | "ACTION: Approved with Conditions as amended and read into the record by Dir. ... RESOLUTION: 20597"; "to authorize up to 505,000 square feet ... RESOLUTION: 20598"; "ACTION: Asst. ZA Closed the PH and indicated an intent to Grant" |
| 2022 modification | June 16, 2022: Motions 21128, 21129, 21130; 981,000 gsf, 810,000 office | MIN(20220616) pp. 14-15 | "to modify the approved Large Project Authorization under Motion No. 20597 to incorporate Lot 113 at 759 Harrison Street ... for a new construction of a 14-story, 185-foot tall mixed-use building of approximately 981,000 gsf in total with 810,000 sf of office space, 3,900 sf of retail space, 29,300 sf of PDR spaces, 3,000 sf of child care use, 16,700 sf of interior and exterior POPOS, 116 off-street below-grade parking spaces"; "MOTION: 21128"; "to authorize up to 305,000 gross square feet ... for a total of 810,000 square feet of Office use ... MOTION: 21129"; "to demolish three Unauthorized Dwelling Units at 759 Harrison Street ... MOTION: 21130" |
| 2022 site | 7 lots, 104,188 sf; "majority of the Project remains the same" | REC(2005.0759ENV-02) | "The subject property consists of seven (was six) lots totaling 104,188 square feet (formerly 102,067 square feet)"; "The majority of the Project remains the same as approved by the Planning Commission on December 12, 2019." |
| expiry and extension | expired June 16, 2025; 18 months to March 24, 2028 | REC(2005.0759ENX-03); AG0924-26 p. 4 | "all three of which have the 3 year validity condition that expired on June 16, 2025"; "The project sponsor is processing the site permit for the project in 2026 and requires these extensions in order for the permit to be finally issued."; "for an extension of eighteen (18) months to March 24, 2028"; "No physical modifications to the Project approved by the Planning Commission on June 16, 2022, under Motion No. 21128 are proposed."; ENX-03 "Closed - Approved", 2026-09-29 |
| other 2026 records | CUA-03 "Approved"; OFA-03 "Accepted"; VAR-04 "Action Pending" | REC(2005.0759CUA-03) etc. | as quoted |
| dedication swap (withdrawn) | to 560 Brannan Street | REC(2023-002967ENX) | "to switch the location of the land dedication from Lot 149 at the Project site to the parcel at 560 Brannan Street (B/L: 3777/ 044)"; "Closed - Withdrawn", 2026-04-22 |
| permits | 4 site permits filed 2019-11-15; 5 demolition/grading filed 2020-01-31; none issued | DBI(201911157378) etc. | "to erect a type 1-a, 15 story with one basement, office, retail, pdr & childcare bldg. (phase 1 west building)", "filed"; "(phase 2 east building)", "filed" |
| site now | commercial parking lot (lot 149) | REC(2025-005002MIS) | "POL referral - Commercial Parking Lot; Recommend approval" (725 Harrison St, lot 149, 2025) |
| plan | ~1 million sf potential | PLAN p. 200 | "there is potential for approximately one million square feet of total development at this site across all uses" |

Stage reasoning: approvals in hand (extended to March 24, 2028); no permit issued; no construction → `entitled`.

Boundary: DataSF parcels, lots 152 and 149; 2.4 acres as drawn. Accuracy official (the 2026 agenda names 149 and 152).

Massing: `pipeline/bam_pipeline/sites/massing_725_harrison.py`. The 2019 floor plans (sheets A20-A26, pp. 361-367) are
scanned line work with a light-blue office fill; the fill is traced from a 144-dpi render (all sheets share one
layout; the upper plan on each sheet sits 720 pt above the lower one). Registration: the 4th Street property line
(x 455.5 px), the Perry Street property line (y 2834) and the Harrison Street frontage (y 1755.5), at the corners of
lot 152 and at the middle of the notch the plans leave around lot 113, matched by a similarity: RMS 0.12 m, scale
0.1480 ft/px against the drawing's 0.1481. The eastern core, which the fill leaves out where it sits on the edge of the
upper floors, is added back (1,841 sq ft). Tiers: level 3 plate (71,136 sq ft) to 80 ft; level 7 (55,109) to 132 ft;
level 11 (52,324) to 171 ft; level 14 (42,531) to 185 ft; each split at the notch into the western (Phase I) and
eastern (Phase II) parts, 8 features, strips under 2 ft wide dropped. All `entitled`, illustrative, nothing outside the
lots, all geometries valid. The 2022 plans weren't reachable; they take in lot 113, which the drawn 2019 floors leave
as a notch (the existing four-story building there stays in the base map). Source PDF pinned (sha256 0d7057a7…b980).

Press-only facts: none recorded.

Open items: the 2022 plans and the Sept 2026 motion number; OFA-03 and VAR-04; the affordable housing lot; the
15-story count in DBI's applications; the current owner.

---

## Leads not added

- **160 Freelon Street** (block 3777 lot 176, record 2022-008873PRJ): 85 affordable homes, nine stories, under
  construction (DBI 202209283327). Included in `598-brannan` as its dedicated affordable housing site, not separately.
- **560 Brannan Street** (block 3777 lot 044): proposed in 2023 as 725 Harrison's affordable housing site instead of
  lot 149; withdrawn April 22, 2026 (REC(2023-002967ENX)). Nothing to add.
- **500 Brannan Street** (block 3777 lot 175, record 2023-009156PRJ): a five-story office and retail building of
  37,185 sq ft, "PL Filed" (PIPE(3777175)). Exclude (small).
- **2000 Marin Street** (block 4346 lot 003): the 343,882 sq ft site the 598 Brannan sponsor would give the SFPUC in
  exchange for 639 Bryant Street (REC(2019-022611GPR)); a land exchange, not a development. Exclude.
