# Official-source findings: India Basin, Balboa Reservoir, Stonestown, Parkmerced

Checked 2026-10-02 against documents downloaded from SF Planning's document store and read in full text (local copies go in `data/raw/official/`, git-ignored). Page numbers are PDF page numbers.

URL shorthand:
- MIN = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/YYYYMMDD_cal_min.pdf` (Planning Commission minutes)
- CPC = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/`
- MEA = `https://sfplanning.s3.amazonaws.com/sfmea/`

---

## india-basin

Documents: MIN 20180726 (items 2, 15a–15g), MIN 20180823 (development agreement), MIN 20181018 and 20181025 (Board reports); CPC `2014-002541ENV.pdf` (final EIR certification motion and Responses to Comments, 2018-07-11); CPC `2014-002541DVA.pdf` (development agreement memo and text, hearing 2018-08-23); CPC `2014-002541GPA.pdf` (executive summary, hearing 2018-06-21).

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 29 | BUILD portion 29.26 ac; with the Rec and Park parks 38.24 ac; development agreement site "approximately 28 acres" | CONFIRMED (29.26) | ENV.pdf p.1 | "BUILD PORTION ... ABOUT 29.26 UNDEVELOPED ACRES"; "TOTALING ABOUT 38.24 ACRES" |
| acresNote: "~29 ac including public parks" | — | 29.26 ac is the BUILD portion only; with the parks 38.24 ac | CONFLICT | ENV.pdf p.1; MIN 20180726 item 15b | "redevelop approximately 39 acres located along the India Basin shoreline" |
| acresNote: "700 Innes parcel about 15 acres" | ~15 | 22.42 ac (17.12 developer-controlled plus 5.30 rights-of-way) | CONFLICT | DVA.pdf p.167 | "approximately 22.42 acres that includes 17.12 acres of property controlled by the Developer" |
| homes | 1,575 | 1,575 | CONFIRMED | MIN 20180726 item 15e (Res. 20250) | "approximately 1,575 residential units" |
| affordablePct | null | 25% | NEW | MIN 20180726 item 2 / MIN 20180823 (Res. 20261); DVA.pdf p.36 | "25% affordable housing and 11 acres of parks and open space" |
| commercialSqftTotal | 209,100 | 209,106 gsf (minutes round to 209,000) | CONFIRMED | ENV.pdf p.27 (RTC Table 2-1) | "Commercial Space—retail, office, R&D ... 209,106 gsf" |
| openSpaceAcres | 24.5 | 24.5 ac whole project (about 15.5 BUILD plus about 8.98 Rec and Park); the DA digest says "11 acres" for BUILD's commitment | CONFIRMED | ENV.pdf p.27 | "Publicly Accessible Recreation/Open Space ... (24.5 acres)" |
| heights | ~14 stories / 160 ft | 20–160 ft, up to 14 stories; height district 20/160-IB adopted 2018-07-26 (the GPA executive summary says 30/160-IB) | CONFIRMED | ENV.pdf p.28; MIN 20180726 item 15f (Res. 20251) | "ranging from one to 14 stories (20–160 feet tall)"; "from 40-X to 20/160-IB" |
| developer | BUILD | India Basin Investment, LLC "(aka BUILD)" | CONFIRMED | DVA.pdf p.1 | "India Basin Investment, LLC (aka BUILD)" |
| park construction (900 Innes 2022–24; Shoreline Park 2025–27) | — | none reachable (the BCDC deck is the applicant's presentation) | UNCONFIRMED | — | — |
| distressed stage; Sept 2026 default | — | none | UNCONFIRMED (press only) | — | — |

Approvals in the minutes:
- 2018-07-26, Planning Commission: final EIR certified (Motion 20247); CEQA findings (Motion 20248); shadow findings (Motion 20249); General Plan amendments (Res. 20250); Planning Code and zoning map amendments (Res. 20251); design standards and guidelines (Motion 20252).
- 2018-08-23: development agreement recommended (Res. 20261).
- October 2018: Board files 180816, 180680 and 180681 passed first and second reading (reported in MIN 20181018 p.5 and MIN 20181025 p.9; exact Board dates not given).

Boundary leads:
- Development and SUD lots (MIN 20180726 items 15d, 15g): 4606/100, 026; 4607/024, 025; 4620/001, 002; 4621/016, 018, 021, 100, 101; 4630/002, 005, 006, 007, 100; 4631/001, 002; 4644/001, 004a, 005, 006, 006a, 007–010, 010A–C, 011; 4645/001, 002b, 003a, 004, 006, 007, 007a, 010, 010A, 011–015; 4596/025, 026; 4597/025, 026.
- The whole EIR site (item 15b) adds 4629A/003–006, 010–013; 4646/001–003, 003A, 019, 020; 4622/007, 008, 012, 013, 016–019; 4605/010–019.
- Best for tracing: the metes-and-bounds legal descriptions in the development agreement, Exhibits A (developer property), B (India Basin Open Space) and D (rights-of-way), around DVA.pdf pp.100–107.
- EIR Figures 2-4b, 2-5b, 2-6a, 2-7a show massing and heights.

Still open: Board final-passage dates and ordinance numbers; later DA amendments; official source for park construction and the 2026 default.

---

## balboa-reservoir

Documents: MIN 20190613, 20190912, 20200409, 20200528 (items 17–18f), 20200730, 20200827; CPC `2018-007883GPA.pdf` (executive summary for initiating the General Plan amendments, with draft DA key terms and design standards; 87 MB).

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 17 | 17.6 ac (key terms and design standards say "approximately 17-acre") | CONFIRMED (17.6 preferred) | MIN 20200528 item 17; GPA.pdf p.31 | "a 17.6-acre project site within the Balboa Park Station Plan Area" |
| homes | 1,100 | about 1,100 (EIR also studied a 1,550-unit option) | CONFIRMED | MIN 20200528 item 18a (Motion 20731) | "approximately 1,100 dwelling units" |
| affordablePct | 50 | 50% | CONFIRMED (draft key terms, pre-approval) | GPA.pdf pp.4, 31 | "Fifty percent (50%) of the residential units produced by the Project will be affordable housing units" |
| affordableHomes | 550 | not stated as a number | UNCONFIRMED (derived) | — | — |
| openSpaceAcres | 4.2 | about 4 ac | CONFLICT (minor) | MIN 20200528 item 18a; GPA.pdf p.3 | "approximately 4 acres of open space" |
| 2-acre central park | — | about 2-acre Reservoir Park | CONFIRMED | GPA.pdf p.3 | "the approximately 2-acre "Reservoir Park."" |
| educator housing | City College and SFUSD | about 150 units with a City College preference; SFUSD not mentioned | PARTLY CONFIRMED | GPA.pdf p.33 | "approximately 150 units with a preference for City College employees" |
| retail / community | — | about 7,500 gsf retail; about 10,000 gsf community space and childcare | NEW | MIN 20200528 item 18a | "approximately 7,500 gross square feet of retail" |
| heights | — | 25–78 ft; 48-X for blocks TH1, TH2 and H, 78-X elsewhere | NEW | MIN 20200528 items 18a, 18e | "New buildings would range in height from 25 to 78 feet" |
| developer | BRIDGE and AvalonBay | DA party Reservoir Community Partners, LLC (draft key terms name BHC Balboa Builders, LLC) | UNCONFIRMED (the company names) | MIN 20200528 item 18f; GPA.pdf p.31 | "Reservoir Community Partners, LLC" |
| site owner | — | SFPUC | CONFIRMED | MIN 20190613 | "3180/190, owned by the San Francisco Public Utilities Commission" |
| Board approval 2020-08 | 2020-08 | Board denied the CEQA appeal and approved all four items (reported 2020-08-27) | CONFIRMED (month) | MIN 20200827 pp.6–7 | "The Board then voted to approve the General Plan, Planning Code, Zoning Map and Development Agreement" |
| DA executed 2021 | 2021 | none | UNCONFIRMED | — | — |
| Building A (159 homes) April 2026; first ~290 affordable homes | — | not reachable (sf.gov, sfbos blocked) | UNCONFIRMED | — | — |

Approvals in the minutes:
- 2020-04-09: General Plan amendments initiated (Res. 20679).
- 2020-05-28, Planning Commission: subsequent EIR certified (Motion 20730); CEQA findings (Motion 20731); General Plan amendments (Res. 20732); Planning Code and map amendments (Res. 20733); design standards and guidelines (Res. 20734); development agreement (Motion 20735, as printed).
- August 2020, Board: MIN 20200827 says second reading passed "on October 18th", which can't be right in an August report; exact date open.

Boundary leads: Block 3180, Lot 190 (partial); the SUD excludes "the 80-foot wide strip along the southern boundary containing SFPUC pipelines" (MIN 20200528 item 18e). Design standards figures 1.3-1, 1.3-2, 1.4-1 in GPA.pdf.

Still open: exact Board dates and ordinance numbers; whether the final DA kept 50%; whether construction started in 2026. The record's existing `sfbos.org/.../r0339-23.pdf` and sf.gov loan-committee sources may confirm these but weren't reachable.

---

## stonestown

No official document for the 2021–2024 redevelopment was reachable:
- The 2015–2022 minutes cover only mall permits (400 Winston Drive, Motions 20240 and 20332 in 2018; Motion 21114 in 2022).
- Every bucket key tried for case 2021-012028 (ENV, DVA, PRJ, GPA, PCA, MAP; DEIR, RTC, NOP on sfmea) returned 403.
- CEQAnet, media.api.sf.gov, sfbos.archive.sf.gov and sfplanning.org are blocked.

Every fact in the record is UNCONFIRMED (30 acres, 3,491 homes, 20% affordable, office/retail/community figures, 6 acres open space, 4–18 stories, ~200 senior homes, 2024 Board approval, $438M tax district). Search summaries mention a 43-acre site and a May 9, 2024 EIR certification; neither has been read in a document.

Leads (not yet read):
- Mall parcel: Block 7295, Lot 004 (400 Winston Drive), MIN 20180719 item 11.
- CEQAnet SCH 2022040571; notice of determination `media.api.sf.gov/documents/2024-0000037_NOD_-_Stonestown_Development_Project.pdf`.
- Board ordinance `sfbos.archive.sf.gov/sites/default/files/o0208-24.pdf`.
- EIFD No. 2 financing plan `media.api.sf.gov/documents/Stonestown_IFP_1-8-26.pdf`.

---

## parkmerced

Documents: CPC `2008.0021EMTZW.pdf` (memo for the 2010-12-16 hearing plus the 2010-10-21 executive summary); MEA `2008.0021E_Parkmerced_DEIR_VI-01.pdf` (draft EIR, 2010-05-12). No Parkmerced items in the 2013–2022 minutes. All figures are from 2010 pre-approval documents and may be superseded by the 2011 development agreement or later amendments.

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 152 | 152 ac including streets (about 116 without) | CONFIRMED | DEIR_VI-01 p.16; EMTZW.pdf p.47 | "approximately 116‐acre site (152‐acres including streets)" |
| homes | 5,679 net new, 8,900 total | same | CONFIRMED | DEIR_VI-01 p.16; EMTZW.pdf p.48 | "an additional 5,679 net new units ... a total of 8,900 units" |
| affordableHomes | null | 852 on-site | NEW (2010) | EMTZW.pdf p.48 | "5,679 new homes (852 of which are on‐site affordable units)" |
| retailSqft | 230,000 | 230,000 | CONFIRMED (2010) | EMTZW.pdf p.48 | "230,000 sf of neighborhood retail space" |
| officeLabSqft | 80,000 | 80,000 | CONFIRMED (2010) | EMTZW.pdf p.48 | "80,000 sf of office space" |
| community center | 64,000 sf | 64,000 sf | CONFIRMED (2010) | EMTZW.pdf p.48 | "64,000 sf dedicated to a community center" |
| openSpaceAcres | null | 68 ac | NEW | EMTZW.pdf p.48 | "68 acres of open space and new parks" |
| 11 towers stay | — | about 1,683 units in 11 towers kept; 1,538 replaced | CONFIRMED | DEIR_VI-01 p.16 | "About 1,683 of the existing apartments located in 11 tower buildings would be retained" |
| heights | — | new buildings 35–145 ft | NEW | EMTZW.pdf p.48 | "range in height from 35 feet to 145 feet" |
| 2011-05-24 Board approval; 2015 Phase 1; 2019 refinancing; 2025 receivership; 2026 Yellowstone | — | none | UNCONFIRMED | — | — |

Boundary leads: bounds and Assessor's Blocks on DEIR_VI-01 p.16 (Vidal Dr, Font Blvd, Pinto Ave and Serrano Dr to the north; 19th Ave and Junipero Serra Blvd to the east; Brotherhood Way to the south; Lake Merced Blvd to the west; Blocks 7303, 7303A, 7308–7311, 7314, 7316, 7319–7326, 7330–7345, 7333 A-B, 7333E, 7353–7373). Full block/lot list on EMTZW.pdf p.1. DEIR Figure III.1 (page III.5).

Still open: the development agreement (`default.sfplanning.org/publications_reports/parkmerced/R18273_PM_DA.pdf`, blocked); the EIR certification motion and date; 2015 Phase 1 records.

---

# Update with full network access (2026-10-02)

Read from the Board of Supervisors, MOHCD, Rec and Park, DBI permits (DataSF `i98e-djp9`; data.sfgov.org now redirects to data.sf.gov) and the Assessor-Recorder stamps on recorded agreements. Where this section and the one above differ, this section is newer.

Shorthand: BOS = `https://sfbos.org/sites/default/files/`, BOSA = `https://sfbos.archive.sf.gov/sites/default/files/`, MEDIA = `https://media.api.sf.gov/documents/`.

Caution: SF Planning's India Basin page carries an HTML comment (invisible to visitors) with stale text, including "became effective on October 3, 2019". Strip comments before quoting sfplanning.org pages.

## india-basin

| field | official value | status | source | quote |
|---|---|---|---|---|
| Board approvals | Ord. 251-18 (SUD/zoning, file 180680), 252-18 (DA, 180681), 261-18 (General Plan, 180816); first reading 2018-10-16, final passage 2018-10-23 | NEW | BOS o0251-18.pdf p30; o0252-18.pdf p13; o0261-18.pdf p7 | "Date Passed: October 23, 2018" |
| DA recorded | 2019-10-16, DOC-2019-K843986-00 | NEW | https://sfplanning.s3.amazonaws.com/default/files/devagreements/indiabasin/IndiaBasin_Development_Agreement_Recorded.pdf p1 | "Wednesday, OCT 16, 2019 10:27:01" |
| 700 Innes | developer owns 14.7 ac, options on 2.4 more | CONFIRMED | o0252-18.pdf p2 | "owns the approximately 14. 7 acre site along Innes Street ... holds options to purchase an additional 2.4 acres" |
| program | up to 1,575 units; 209,106 sf commercial; 15.5 ac publicly accessible open space in the DA | CONFIRMED | o0252-18.pdf p2 | "up to 1,575 dwelling units, approximately 676,052 square feet (15.5 acres) of publicly accessible open space" |
| affordablePct | 25% | NEW | o0252-18.pdf p1 | "including 25% affordable housing and 11 acres of parks and open space" |
| 900 Innes | park project broke ground 2021; 900 Innes opened Oct 2024 | CONFLICT (data: 2022–2024) | sfrecpark.org/m/newsflash/home/detail/2951; …/detail/2258 | "The India Basin Waterfront Park project broke ground in 2021. The park's southern portion at 900 Innes Ave. opened in fall 2024" |
| Shoreline Park | groundbreaking 2025-08-19; completion expected 2028 | CONFLICT (data: 2025–2027) | sfrecpark.org detail/2951; sf.gov release (below); sfrecpark.org/CivicAlerts.aspx?AID=2535 | "began in fall 2025 and is anticipated to be completed in 2028" |
| combined park | 10-acre India Basin Waterfront Park | NEW | sf.gov release | "turning it into 10 acres of vibrant public space" |
| private site | DBI grading permits for 700 Innes (filed 2022) still in plan check; none issued | NEW | DBI 202205033459, 202204212681 | "clearing, grubbing, rough grading & soil import on the site of 700 innes." |
| 2026 default; "distressed" | no official record | UNCONFIRMED | — | — |

sf.gov release: https://www.sf.gov/news-mayor-lurie-breaks-ground-on-final-phase-of-india-basin-waterfront-park-project-upgrading-open-space-in-bayview-hunters-points

Official stage: entitled (no issued permits on the private site). Boundary: DataSF Special Use Districts (`5yf5-ms5f`, "Public Domain U.S. Government"), feature "India Basin SUD" (~30.2 ac, development site only; parks need separate geometry). Fallback: recorded DA Exhibits A, B, D.

## balboa-reservoir

| field | official value | status | source | quote |
|---|---|---|---|---|
| Board approval | Ord. 141-20 (SUD, file 200422), 142-20 (DA, 200423), 143-20 (General Plan, 200635); first reading 2020-08-11, final passage 2020-08-18 | CONFIRMED + dates | BOS o0142-20.pdf p13 | "August 18, 2020 Board of Supervisors - FINALLY PASSED" |
| DA recorded | 2021-03-10 | CONFIRMED | MEDIA Approved_Balboa_Reservoir_Building_A_Loan_Evaluation_-_LC_5-2-25.pdf p6 | "The DA was recorded on Marth 10, 2021." (sic) |
| affordable | 50%, ~550 units | CONFIRMED | o0142-20.pdf p3; BOS r0339-23.pdf p1 | "50%, or 550 homes, as affordable housing units" |
| acres | DA 17.6; SUD Project Site 16.5; land sold ~16 | CONFIRMED (approx.) | o0142-20.pdf p1; o0141-20.pdf p7 | "approximately 17.6-acre site" |
| openSpaceAcres | ~4 | CONFLICT (data 4.2) | o0142-20.pdf p3 | "approximately 4 acres of publicly accessible open spaces" |
| landowner | SFPUC sold the site to BHC Balboa Builders on 2022-12-20 ($11.4M) | CONFLICT | r0339-23.pdf p1 | "On December 20, 2022 ... the SFPUC sold the approximately 16-acre Balboa Reservoir ... to BHC Balboa Builders, LLC" |
| developer | DA party Reservoir Community Partners, LLC; MOHCD: BRIDGE and Avalon Bay selected 2017 | CONFIRMED | sf.gov loan committee 2025-11-07 | "BRIDGE Housing Corporation ... and Avalon Bay were selected as the Master Plan developers" |
| first affordable buildings | E (128) + A (159) = 287 | CONFIRMED | BOSA r0414-25.pdf | "construction of approximately 287 new" |
| Building E | site permit 2025-01-08; first construction document 2025-11-25 | NEW | DBI 202207289451 | "bldg e ... erect a 7-story ... with 128 residential units & community facility." |
| Building A | site permit 2025-09-03; first construction document 2026-06-11; tower crane permit 2026-08-21; MOHCD plan: start April 2026, complete January 2028 | CONFIRMED (start ~June–Aug 2026) | DBI 202503313370, 202605201591; https://www.sf.gov/meeting--november-07--2025--citywide-affordable-housing-loan-committee-meeting | "The Sponsor plans to start construction in April 2026 and complete construction by January 2028." |
| market-rate | Block C/D (243 units) and 170 Meyer (174) permits filed 2026-08-26 | NEW | DBI 202607094805, 202607084737 | "market-rate multi-family residential with 243 units" |

Stage (inferred from permits): under construction. Boundary: DataSF `5yf5-ms5f`, feature "Balboa Reservoir" (~16.6 ac = SUD Project Site; excludes the SFPUC pipeline strip). Parcels: block 3180, lots 190, 201, 202, 204, 205 (DataSF `acdm-wktn`, PDDL).

## stonestown

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| EIR | — | certified 2024-05-09 (Motion 21559); CEQA findings Motion 21560; no appeal | NEW | MEDIA 2024-0000037_NOD_-_Stonestown_Development_Project.pdf p2 | "The Final Environmental Impact Report (FEIR) was certified on May 9, 2024 ... no appeals were filed." |
| Board approval | 2024 | Ord. 204-24 (zoning/SUD, file 240409), 205-24 (DA, 240410), 208-24 (General Plan, 240575); first reading 2024-07-16, final passage 2024-07-23; NOD approval date 2024-08-01 | CONFIRMED + dates | BOSA o0204-24.pdf p64; o0205-24.pdf p14; NOD p1 | "July 23, 2024 Board of Supervisors - FINALLY PASSED" |
| DA | — | dated 2025-05-06; recorded 2025-07-07 (Doc. 2025049884) | NEW | MEDIA Stonestown_IFP_1-8-26.pdf p12 | "Development Agreement dated as of May 6, 2025, and recorded in the Official Records on July 7, 2025" |
| acres | 30 | ~30 ac project site; ~27 ac redeveloped inside the 43-ac mall site | CONFIRMED | NOD pp1–2; o0205-24.pdf p9 | "Lot Size: Approximately 30 acres" |
| acresNote ~40 | ~40 | 43 (incl. 2 ac right-of-way) | CONFLICT | NOD p2 | "in the 43- acre (including 2 acres of public right-of-way) Stonestown Galleria shopping mall site" |
| homes | 3,491 | up to 3,491 with the Variant Sub-Area (3,341 without) | CONFIRMED | o0205-24.pdf p4 | "up to approximately 3,341 residential units (or approximately 3,491 residential units with the addition of the Variant Sub-Area)" |
| affordablePct | 20 | 20% required; financing plan projects 350 inclusionary, 0 stand-alone | CONFIRMED (gap noted) | Board hearing notice (sfgov.legistar.com View.ashx ID=13062979) p2 | "with a requirement that 20% of the total units be affordable" |
| retail / office | 160,000 / 96,000 | same | CONFIRMED | o0205-24.pdf p5 | "up to approximately 160,000 square feet of net new Retail" |
| community | ~63,000 | 53,000 (63,000 with variant) | CONFIRMED | o0205-24.pdf p5 | — |
| openSpaceAcres | 6 | ~6 net new | CONFIRMED | o0205-24.pdf p5 | "approximately 6 net new acres of privately owned, publicly accessible open space" |
| heights | 4–18 stories | 30–190 ft; draft EIR 3–18 stories | CONFLICT | NOD p2; MEDIA Stonestown_-_EIR.pdf p131 | "heights ranging from 30 to 190 feet" |
| senior homes | ~200 | 201 | CONFIRMED | Stonestown_-_EIR.pdf p659 | "(including 201 senior housing units)" |
| mall stays | — | 710,000 sf stays; outside the SUD | CONFIRMED | NOD p2 | "710,000 square feet of the existing mall will remain" |
| developer | Brookfield | DA parties Stonestown NW Parcel LLC and affiliates; applicant Brookfield Properties | CONFIRMED | NOD p1 | "Project Applicant: Christie Donnelly, Brookfield Properties" |
| tax district | "moving through City Hall" | EIFD No. 2 formed and financing plan adopted 2026-02-12 (Res. 2026-03); $438.06M (2025 dollars) | CONFLICT (done) | MEDIA Reso_2026-03.pdf pp9, 13; IFP pp6, 14 | "approximately $438 million (estimated in 2025 dollars)" |
| phasing | ~20 yrs | 9 areas, 2028–2051 (developer projection) | CONFIRMED (approx.) | IFP p11 | "Total ... 3,491 ... 2028-2051" |
| permits | — | none for new buildings on blocks 7295/7296 since 2022 | NEW | DBI | — |

Boundary: DataSF `5yf5-ms5f`, feature "Stonestown Special Use District" (~38.5 ac, larger than 30; unchecked). Alternatives: EIFD boundary (IFP Exhibits A and B, "coterminous with the boundaries of the Subject Property"); Board map sfgov.legistar.com View.ashx?M=F&ID=13028771&GUID=5365CA6A-04A7-4732-8598-F2737A74BDD6.

## parkmerced

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| Board approval | 2011-05-24 | first reading 2011-05-24; final passage 2011-06-07 (6–5): Ord. 89-11 (DA), 90-11 (SUD), 91-11 (zoning map), 92-11 (General Plan); effective 2011-07-09 | CONFLICT (use 2011-06-07) | https://sfbos.org/ftp/uploadedfiles/bdsupvrs/ordinances11/o0089-11.pdf; recorded DA p11 | "On June 7, 2011, the Board adopted Ordinance No. 89-11 ... The Enacting Ordinance took effect on July 9, 2011." |
| EIR | — | certified 2011-02-10 | NEW | DA p10 | "certified by the Planning Commission on February 10, 2011" |
| acres | 152 | ~152 | CONFIRMED | DA p9 | "the approximately 152-acre site" |
| homes | 5,679 net / 8,900 | same | CONFIRMED (adopted DA) | DA p9 | "1,683 existing-to-be-retained units + 1,538 newly constructed Replacement Units + 5,679 newly constructed units = 8,900 units" |
| commercial | 230k retail / 80k office | 310,000 sf commercial (split only in 2010 documents) | CONFIRMED total | DA p32 | "310,000 square feet of commercial use, 64,000 square feet of recreational/fitness center/community center use" |
| affordable | (2010: 852) | 15% inclusionary, on-site, off-site or fee; Phase 1 ~220 on-site BMR anticipated | NEW (don't show 852) | sfplanning.org/project/parkmerced | "approximately 220 BMR units" |
| heights | — | 35–145 ft | CONFIRMED | DesignReview_StaffReport.pdf p2 | "range in height from 35 feet to 145 feet" |
| Phase 1 | 2015 | approved 2015-06-03, ~1,668 units in 4 subphases | CONFIRMED | sfplanning.org/project/parkmerced | "On June 3, 2015, the City approved Phase 1 ... approximately 1,668 residential dwelling units" |
| final maps | — | Board Motion M23-149, 2023-12-12, Final Maps 10699/10700 (Subphases 1C, 1D) | NEW | https://sfgov.legistar.com/LegislationDetail.aspx?ID=6446248&GUID=D6849B97-2F87-42EE-8615-2E4085DA91B4 | "Enactment #: M23-149" |
| permits | never broke ground | 199 Vidal (64 units) issued 2018-10-29, no construction recorded; three 2022 filings (471, 268, 151 units) still filed | CONFIRMED (nothing completed) | DBI 201511132572, 202212138195, 202212208799, 202212198663 | "to erect a 14-story, 471-dwelling units" |
| 2019 refinancing; 2025 receivership; 2026 Yellowstone | — | no official record | UNCONFIRMED | — | — |
| developer | — | Parkmerced Investors Properties LLC (DA); Parkmerced Owner, LLC (2015) | NEW | DA p7 | "PARKMERCED INVESTORS PROPERTIES, LLC" |

Official stage: entitled. Boundary: DataSF `5yf5-ms5f`, feature "Parkmerced" (~161 ac, likely includes streets). Also DA Exhibits A and B: https://default.sfplanning.org/publications_reports/parkmerced/Parkmerced_Development_Agreement_As_Recorded.pdf

Hosts: add `sfrecpark.org` (Rec and Park) to the official list. Credits: DataSF "Zoning Map - Special Use Districts" (`5yf5-ms5f`, Public Domain U.S. Government) and "Parcels – Active and Retired" (`acdm-wktn`, ODC PDDL 1.0).
