# Candidate projects: Northgate Town Square (San Rafael), Ravenswood Business District / 4 Corners (East Palo Alto)

Checked 2026-10-07 against documents downloaded and read in full text. Local copies are in `data/raw/official/northgate-san-rafael/` and `data/raw/official/ravenswood-business-district/` (git-ignored). Page numbers are PDF page numbers unless marked "printed". Draft records are in the scratchpad (`records/new/<id>.json`); both pass `tests/record-check.test.ts`.

Access notes:
- San Rafael: `www.cityofsanrafael.org` (WordPress/ProudCity) responds. Its files live in a Google Cloud bucket, `storage.googleapis.com/proudcity/sanrafaelca/`. The WordPress REST API (`/wp-json/wp/v2/{posts,pages,meetings,documents}?search=`) is the quickest way to find dated items. There is no Legistar or Granicus; agendas and packets are on the meeting pages.
- East Palo Alto: `www.cityofepa.org` (Drupal) responds, but its site search returns 403. The lead URL `.../page/16201/rbdspu_execsum.pdf` and the project page `/planning/page/rbd-specific-plan-update` named in the 2024 notices both return 404 now; the adopted plan is under `/planning/page/ravenswood4-corners-specific-plan-adopted-12172024`. Agendas since Sept 19, 2023 are on Granicus (`cityofepa.granicus.com/ViewPublisher.php?view_id=1`). Its AgendaViewer links redirect through Google's document viewer to `granicus_production_attachments.s3.amazonaws.com/cityofepa/...`, and full packets are on `d3n9y02raazwpg.cloudfront.net/cityofepa/...`. Older meetings are on `eastpaloalto.iqm2.com` (its calendar is empty, but `Detail_Meeting.aspx?ID=` and `FileOpen.aspx` still work).
- Marin County GIS: `gis.marinpublic.com/arcgis/rest/services/BaseMap/Basemap/FeatureServer/13` (parcels). `gis.marincounty.gov` is behind Cloudflare.

Hosts added to `src/projects/official.ts`:
- `OFFICIAL_HOSTS`: `cityofsanrafael.org`, `gis.marinpublic.com`, `cityofepa.org`, `cityofepa.granicus.com`, `eastpaloalto.iqm2.com`.
- `OFFICIAL_PREFIXES`: `storage.googleapis.com/proudcity/sanrafaelca/`, `d3n9y02raazwpg.cloudfront.net/cityofepa/`, `granicus_production_attachments.s3.amazonaws.com/cityofepa/`, `services8.arcgis.com/qac9exitge3rh5x7/` (East Palo Alto's ArcGIS Online organisation; its zoning web map is owned by a `@cityofepa.org` account and linked from the City's "Interactive maps" page).

Summary of recommendations:

| candidate | recommendation | id |
|---|---|---|
| Northgate Town Square (Northgate Mall redevelopment) | INCLUDE (entitled; demolition not yet officially confirmed) | `northgate-san-rafael` |
| Ravenswood Business District / 4 Corners Specific Plan | INCLUDE as a plan-scale record, like `moffett-park` (Matthew's call; see reasoning) | `ravenswood-business-district` |
| East Palo Alto Waterfront (Emerson Collective) | EXCLUDE for now (conceptual; only a 299-home Phase 1 under review); note it in the RBD record | — |
| 2020 Bay Road (1.34M sq ft office) | EXCLUDE (on hold at the applicant's request) | — |
| 1675 Bay Road, "University and Bay at 4 Corners" | EXCLUDE (274 homes on about 6 acres) | — |

---

## northgate-san-rafael

URL shorthand:
- SR = `https://storage.googleapis.com/proudcity/sanrafaelca/`
- PAGE = `https://www.cityofsanrafael.org/northgatetownsquaredev/` (current project page); ARCH = `https://www.cityofsanrafael.org/northgate-town-square-rev/` (archived entitlement page)
- CCSR = SR`2024/11/6.a-Northgate-Town-Square-Project.pdf` (City Council agenda report, Dec 2, 2024, 28 pp.)
- PCSR = SR`2024/10/A-PC-Staff-Report-10-29-2024.pdf` (Planning Commission staff report, Oct 29, 2024, 36 pp.)
- R15359 = SR`2025/07/CC-Resolution-15359-Northgate-Town-Square-Project-Signed.pdf` (6 pp.)
- R15360 = SR`2025/07/Reso-15360-with-Attachments-signed.pdf` (202 pp., with conditions and affordable housing agreements)
- ORD = SR`2024/12/4.b-Northgate-Town-Square-Project-Ordinance-Adoption.pdf` (Ordinance 2043 and exhibits, 121 pp.)
- MIN1202 = SR`2024/11/CC-SA-Minutes-2024-12-02.pdf`; MIN1216 = SR`2025/02/CC-SA-Minutes-2024-12-16.pdf`
- DEVPLAN = SR`2024/10/H-ATTACHMENT-2-Exhibit-C-Northgate-Town-Square-Development-Plan-2025-2040.pdf` (2 pp.)
- APR = SR`2026/03/0ce061e5-3.b-general-plan-and-housing-element-annual-progress-reports.pdf` (City Council, Mar 16, 2026, 41 pp.)
- CEQA = `https://ceqanet.lci.ca.gov/2021120187` (documents /1 to /7)

Documents also read: PC minutes Oct 29, 2024 (SR`2024/10/PC-Approved-Minutes_10-29-24-signed.pdf`); PD standards (SR`2024/10/G-ATTACHMENT-2-Exhibit-B-Northgate-PD-Standards.pdf`); legal description (SR`2024/10/I-ATTACHMENT-2-Exhibit-D-legal-description.pdf`); Dec 1, 2025 Council item on Northgate Specific Plan funding (SR`2025/11/e3d5ba62-4.d-funding-agreements-to-prepare-the-northgate-and-souteast-san-rafael-specific-plans.pdf`); the City's news posts of Feb 26, 2025 and Mar 18, 2026; the Northgate Specific Plan RFP page (Feb 13, 2026); the April 28, 2026 Planning Commission page (555 Northgate Dr.).

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, address, applicant | Northgate Town Square, 5800 Northgate Drive; Merlone Geier Partners, LLC | CCSR p.1 | "NORTHGATE TOWN SQUARE PROJECT-( 5800 NORTHGATE DRIVE)– PUBLIC HEARING ... ENTITLEMENT REQUESTS FROM MERLONE GEIER PARTNERS, LLC" |
| ownership | bought from Macerich in 2017 | R15360 p.1 | "in 2017 Merlone Geier Partners purchased the Project Site from The Macerich Company" |
| acres, APNs | about 44.76 acres; 6 APNs | R15360 p.1; CCSR p.3 | "the approximately 44.76 acre property commonly known as the Northgate Mall, inclusive of APN #s 175-060-012, -040, -059, -061, -066, and -067" |
| existing mall | about 766,507 sq ft; opened 1964 | R15360 p.1 | "began operation in 1964, underwent major renovations in 1987 ... and currently consists of approximately 766,507 square feet of commercial space" |
| program (approved) | Phase 1: 864 homes (87 BMR), 501,941 sq ft commercial; Phase 2: 1,422 homes (143 BMR), 219,380 sq ft commercial; 56,975 sq ft Town Square | R15360 p.1; ORD p.1 | "Phase 1 (2025) includes operation of 501,941 square feet of commercial space, 864 residential units (87 deed restricted below market rate units affordable to low-income households), and privately owned publicly accessible open space and recreational uses including but not limited to the 56,975 square foot Town Square, 9,604 bicycle hub ... Phase 2 (2040) includes operation of 219,380 square feet of commercial space, 1,422 residential units (including 143 deed restricted below market rate units" |
| development plan totals | same | DEVPLAN pp.1–2 | "Total Residential Units 864 / Total Commercial Sq Ft. 501,941 sf"; "Total Residential Units 1,422 / Total Commercial Sq Ft. 219,380 sf" |
| buildings | R1 38 and R2 100 townhomes; R3 280, R4 446, R5 309, R6 249 apartments | PCSR pp.21–22 (Table 4) | "Phase 1 (2025) Total 864 87"; "Phase 2 (2040) Total 558 56"; "Buildout Total 1,422 143" |
| affordability | 10% low-income (50–80% AMI), on site, deed-restricted in perpetuity | CCSR p.7; PCSR p.21 | "require the applicant to provide ten percent (10%) of the total number of units in the Project as affordable to low-income households, earning no more than 80% AMI" |
| heights | 78-ft limit by density bonus concession; R4/R6 72 ft (77.5 parapet), R3/R5 62 ft (67.5), townhomes 35 ft | PCSR p.7, p.23 (Table 5) | "the tallest buildings proposed are Residential 4 and Residential 6, each of which measure 72 feet to the roof and 77.5 feet to the parapet" |
| density | 32 homes per acre | PCSR p.22 | "The Project proposes an overall residential density of 32 units per acre." |
| no DA | development agreement withdrawn June 2024 | CCSR p.4 | "The Project initially included an application for a Development Agreement, however, that application was withdrawn by the applicant as part of the June 2024 Revised Project submittal." |
| PC recommendation | Oct 29, 2024, Res. 24-06, 24-07, 24-08 | CCSR p.2 | "At that meeting the Planning Commission approved Resolution Nos. 24-06, 24-07, and 24-08" |
| EIR certified | Dec 2, 2024, Res. 15359, 5–0 | MIN1202 p.7; R15359 p.6 | "Resolution 15359 - Resolution certifying the Final Environmental Impact Report (FEIR)"; "AYES: COUNCILMEMBERS: Bushey, Hill, Kertz, Llorens Gulati & Mayor Kate / NOES: ... None" |
| entitlements | Dec 2, 2024, Res. 15360 (VTSM, master use permit, design review, sign program, affordable housing agreement), 5–0 | MIN1202 p.7 | "Resolution 15360 - Resolution approving the Vesting Tentative Subdivision Map, Master Use Permit inclusive of a project wide affordable housing agreement, Environmental and Design Review Permit, and Master Sign Program" |
| rezoning | Ordinance 2043 adopted Dec 16, 2024, 5–0 | MIN1216 p.4 | "Councilmember Kertz moved and Councilmember Bushey seconded to waive the second reading and adopt by title only Ordinance 2043." "AYES: Councilmembers: Bushey, Hill, Kertz, Llorens Gulati & Mayor Kate" |
| NODs | Dec 6 and Dec 23, 2024; approved 12/2/2024 | CEQA /6, /7 | "Approving Agency City of San Rafael ... Approved On 12/2/2024" |
| stage (City) | approved; demolition "begins in the Fall of 2025" | PAGE (modified 2025-11-14) | "On December 2, 2024, the San Rafael City Council approved the Northgate Town Square project." "Demolition begins in the Fall of 2025, with subsequent phases of construction to follow." |
| next steps (City) | financing, design, construction prep | City news, Feb 26, 2025 | "the project is set to move forward with the next stages of development, including securing financing, finalizing architectural designs, and preparing for construction." |
| permits so far | none counted in 2025 | APR p.6 | "Housing projects that have been entitled are not reflected in the RHNA progress if they did not also receive a building permit." The 2025 permit tables (pp.20–41) contain no 5800 Northgate / 175-060 entries. |
| city context | Northgate drove the entitlement surge | APR p.6 | "This recent surge in development activity is largely the result of the redevelopment of Northgate Mall" |
| Northgate Specific Plan | City preparing a specific plan for the 100+ acre PDA around the mall (MTC grant); RFP Feb 2026, proposals due Apr 2, 2026 | Dec 1, 2025 item, Annex I; RFP page | "This Priority Development Area (PDA) covers over 100 acres within the Northgate area of North San Rafael. The anchor property within PDA is Northgate Mall" "Northgate Mall has recently been re-entitled as a mixed-use project, with a mix of retail and restaurants as well as 1422 dwelling units." |

Superseded figures (do not use): NOP (Dec 2021) 1,443 homes, 225,100 sq ft, Phase 1 1,013 homes; Draft EIR (Jan 2024) 1,422 homes, 217,520 sq ft, Phase 1 922 / Phase 2 500 homes, 10.5% affordable; the developer's March 2024 SB 330 alternative (719 + 1,086 homes, 168 affordable; posted on the City site as a "Statement from Merlone Geier"). The City's project pages still say "225,100 square feet" (ARCH), which is the 2021 figure; the approvals say 219,380.

Press figures vs official: "up to 1,422 homes, phase 1 up to 864" matches. The affordable share is 10% (143 homes), not the 10.5% in the Draft EIR.

Stage: **entitled**. No official record of demolition or building permits was found as of 2026-10-07. The only report of work is a student newspaper (Apr 27, 2026: deconstruction of the former Sears building by Ghilotti Bros.); it's kept in `reported`. San Rafael's permit portal was not searched.

Separate nearby project: 555 Northgate Drive (APN 175-060-32), a 7-story, 193-home all-affordable building approved by the Planning Commission on Apr 28, 2026. Not part of Northgate Town Square.

Boundary lead:
- Marin County parcels, `https://gis.marinpublic.com/arcgis/rest/services/BaseMap/Basemap/FeatureServer/13`, `where=Prop_ID IN ('175-060-12','175-060-40','175-060-59','175-060-61','175-060-66','175-060-67')`. All six return (Jurisdiction "San Rafael"), totalling 43.87 acres (Shape__Area in sq ft, EPSG 2872) against 44.76 in the approvals. Bounding box -122.5468 to -122.5420, 38.0009 to 38.0065; center about -122.5444, 38.0037 (CEQAnet: 38°0'13.3"N 122°32'40.1"W). No copyright or license text on the service; confirm terms. Local copy: `parcels.geojson`.
- Check against the legal description (Ordinance 2043 Exhibit D) and plan sheet SD-12, which the ordinance names as the Project Site.

Massing lead: Development Plan Phase 1 and Phase 2 site plans (DEVPLAN; Figures 1–2 in CCSR p.5) with the PCSR Table 5 heights (Town Square Pavilion 45'3"; Residential 1–2 35'; Residential 3 and 5 62' (67'6" parapet); Residential 4 and 6 72' (77'6"); Pad 1–5 20'4" to 30'6"; Major 1 46'5"; Shops 1 34'6"; Major 2 39'7"; Shops 2/2A 41'6"; garage 27' (40' tower); cinema 46'8", existing). Full approved drawing set: `https://publicrecords.cityofsanrafael.org/WebLink/DocView.aspx?id=40866&dbid=0&repo=CityofSanRafael` (not opened). Draw as "Illustrative massing".

Recommendation: **INCLUDE**. 1,422 homes on 44.8 acres clears the 1,000-home bar; fully entitled with a City resolution trail and parcels.

---

## ravenswood-business-district

URL shorthand:
- EPA = `https://www.cityofepa.org/`
- SP = EPA`sites/default/files/fileattachments/planning/page/9021/ravenswood_business_district_4_corners_specific_plan_final.pdf` ("Final Adopted Plan", 470 pp., created Feb 3, 2025; pages still footed "Public Review Draft")
- SPPAGE = EPA`planning/page/ravenswood4-corners-specific-plan-adopted-12172024`
- CEQA = `https://ceqanet.lci.ca.gov/2022040352` (/1 NOP, /2 Draft SEIR, /3 Final, /4 and /5 NODs)
- AG1203 = `https://granicus_production_attachments.s3.amazonaws.com/cityofepa/2120b3225e83b69e9a3e4c0e33e6acbc0.pdf` (Council agenda, Dec 3, 2024)
- PK1217 = `https://d3n9y02raazwpg.cloudfront.net/cityofepa/da8aa36c-d815-11ee-98bb-0050569183fa-3408cd31-ecd7-4429-9d91-65986d552499-1734654695.pdf` (Council packet, Dec 17, 2024, 153 pp.)
- PK0303 = `https://d3n9y02raazwpg.cloudfront.net/cityofepa/967a0d3d-d23a-11f0-bb28-005056a89546-3408cd31-ecd7-4429-9d91-65986d552499-1772343676.pdf` (Council packet, Mar 3, 2026, 451 pp.)

Also read: every City Council and Planning Commission agenda on Granicus from Jan 2025 to Oct 6, 2026 (grepped for Ravenswood, RBD, Waterfront, Bay Road, development agreements, allocations); the City's project pages; the July 6, 2021 Council staff report on the EPA Waterfront preliminary application (iQM2 `FileOpen.aspx?Type=30&ID=3614&MeetingID=1419`).

| field | official value | source | verbatim quote |
|---|---|---|---|
| plan area | about 207 acres; excludes University Village | SP p.13 (printed 4), p.14 | "The Plan Area encompasses approximately 207 acres and is located in the northeastern portion of East Palo Alto." "The Plan Area does not include University Village, a single-family neighborhood immediately east of University Avenue." |
| bounds | UPRR/city limits north; Illinois St rail easement west; Weeks or Runnymede St south; Ravenswood Preserve and Baylands east | SP p.13 | "generally bounded by the City limits/Union Pacific Railroad (UPRR) tracks to the north, the western edge of the Union Pacific Railroad easement along the back of Illinois Street to the west, Weeks Street or Runnymede Street to the south, and the Ravenswood Open Space Preserve and Palo Alto Baylands Nature Preserve to the east" |
| acres (CEQA) | NOP 350; NODs 207 | CEQA /1; /4, /5 | "Total Acres 350"; "Total Acres 207" |
| capacity (plan) | 3,350,000 sq ft office/R&D; 300,000 industrial; 112,400 retail; 154,700 community/civic; 53,500 tenant amenity; 1,600 homes (1,472 MF, 128 SF/TH) | SP p.79 (printed 70, Table 4-1) | "Office/R&D 3,350,000 s.f.*"; "Industrial 300,000 s.f. **"; "Retail 112,400 s.f. **"; "Community/Civic 154,700 s.f. **"; "Tenant Amenity 53,500 s.f. **"; "All Units 1,600 units"; "Multi-family 1,472 units"; "Single-family/ Townhouse 128 units" |
| capacity (CEQA) | 3.3M office/R&D, 129,700 civic | CEQA /5 | "The Specific Plan Update will allow up to 3.3 million square feet (sf) of office/R&D, 300,000 sf of industrial, 112,400 sf of retail, 129,700 sf of civic/community, and 53,500 sf of tenant amenity space, as well as 1,600 residential units in the Plan area." |
| office allocation | 2.7M standard; 250,000 minor reserve; 400,000 exemplary reserve | SP p.366 (printed 357) | "There shall be 2,700,000 square feet of office/R&D made available for allocation"; "250,000 square feet ... reserved for projects with less than 150,000 total square feet"; "400,000 square feet ... reserved for projects proposing to exceed the maximum FAR"; "Council may consider increasing the total office/R&D development capacity in the Plan Area beyond the maximum 3,350,000 square feet." |
| affordability | citywide inclusionary: 20% on site (or alternative) | SP p.22 | "Residential developments must provide 20 percent of all new housing units on-site at a level affordable to low- and moderate-income households or provide an alternative mitigation." |
| heights | tallest 7–8 stories at east end of Bay Road, Four Corners and employment core | SP p.91 (printed 82) | "standards focus the tallest buildings (seven to eight stories) at the far end of Bay Road, in Four Corners with appropriate transitions, and in the employment core. Four and five-story buildings are allowed along the middle of Bay Road" |
| supersedes 2013 plan | yes | SP p.21 | "This Specific Plan represents a comprehensive update to the prior Plan, which was adopted in 2013, and as such, wholly supersedes the previous Plan." |
| Dec 3, 2024 | FSEIR certified, GPA approved, ordinances introduced; 4 ayes, 1 abstention | CEQA /4; PK1217 pp.32–33 | "On Dec. 3, 2024, the City Council approved the General Plan Amendment (GP24-001) ... and introduced an ordinance to adopt the Specific Plan and zoning amendment." "AYES: Mayor Lopez, Councilmembers Abrica, Gauthier, and Romero" "ABSTAIN: Vice-Mayor Barragan" |
| Dec 17, 2024 | plan and zoning ordinances adopted (consent 3.3) | CEQA /5; SPPAGE | "On Dec. 17, 2024, the City Council approved through a second reading to adopt the Specific Plan Update and related zoning amendment." "The City Council adopted the Ravenswood Business District/4 Corners (RBD) Specific Plan (Update) on December 17, 2024, superseding the 2013 RBD Plan." |
| ordinance numbers | not found (packet has "DRAFT ORDINANCE No. ___"; minutes not posted) | PK1217 p.36 | — |

Projects in the plan area (City project pages, read 2026-10-07):

| project | status (City) | size (official) | source |
|---|---|---|---|
| East Palo Alto Waterfront (Sycamore Real Estate Investment LLC / Emerson Collective), 151 Tara St. area | "Under Review"; "The project is in a conceptual stage." | 2021 preliminary: 52 acres, 15 parcels, contemplated 750,000 sq ft office, 550,000 R&D, 50,000 retail, 40,000 community, 260,000 residential = 1,650,000 sq ft (Council staff report, July 6, 2021, p.9 Table 2) | EPA`planning/project/east-palo-alto-epa-waterfront` |
| EPA Waterfront Phase 1 | "Under Review"; design review received 11.27.24 | "299 residential units, 294,465 square feet"; "Community/ Commercial Space: 11,009 square feet"; "Total Gross Area: 314,563 square feet" | EPA`planning/project/epa-waterfront-phase-1` |
| 2020 Bay Road | "Under Review"; "currently on hold per applicant's request" | "17.2-acre site ... five 8-story office buildings ... approximately 1,343,292 square feet" (filed 2019, under the 2013 plan) | EPA`planning/project/2020-bay-road-design-review` |
| 1990 Bay Road "The Landing" (Harvest Properties) | "Under Review"; preliminary review 2021 | office, lab/R&D, retail, civic; no size on the page | EPA`planning/project/1990-bay-road-landing-dr21-003` |
| 1675 Bay Road / 2400 University, "University and Bay at 4 Corners" (Sand Hill Property Co.) | "Approved" on both project pages; PC declined to approve Feb 9, 2026; Council appeal hearing Mar 3, 2026 | townhomes 106 (11 affordable) on 4.61 ac; mixed-use 168 (25 affordable), 6 stories / 75 ft, on 1.45 ac; vested under the 2013 plan by SB 330 | PK0303 pp.75–77 |
| 2535 Pulgas Ave Civic Commons (City) | application received 7.18.25 | 102,614 sq ft City Hall, library, chambers | EPA`planning/project/2535-pulgas-avenue-civic-commons` |

No office/R&D allocation request, master plan or development agreement under the 2024 plan appears on any City Council or Planning Commission agenda from January 2025 to October 6, 2026 (the 2025–26 development agreement items are for Woodland Park, outside the plan area).

Plan vs project: `moffett-park` (a 1,270-acre plan with no single developer) is on the map as a plan-scale record, while East Whisman was excluded because Middlefield Park was its project. In the RBD no single project is both large and approved: the Waterfront is conceptual apart from a 299-home first phase, 2020 Bay Road is on hold, and Four Corners is 274 homes. The plan itself (3.35M sq ft office/R&D, 1,600 homes) clears the 1M sq ft bar.

Recommendation: **INCLUDE as a plan-scale record** (`ravenswood-business-district`, stage `entitled`, boundary only), following the Moffett Park precedent. Matthew may prefer to wait and map the EPA Waterfront once it has a full application; if so, EXCLUDE the plan and keep the Waterfront on a watch list.

Boundary lead:
- City of East Palo Alto ArcGIS, "Specific Plan Boundary": `https://services8.arcgis.com/Qac9ExiTge3RH5x7/arcgis/rest/services/2025_EPA_Zoning_Map_WFL1/FeatureServer/0` (layer of web map 0c155f23684d4731972d324ed6817270, "2025 EPA Zoning Map", linked from EPA`planning/page/interactive-maps`). One polygon, about 325.7 acres (computed), bbox -122.1418 to -122.1264, 37.4687 to 37.4840. It is the outer line and has no hole for University Village; compared with SP Figure 1-3 "Plan Boundary" (PDF p.18), which shows University Village "Outside of Specific Plan Area". Cut University Village out (trace Figure 1-3, or use the City's zoning parcels in `Final_Zoning/FeatureServer/0`) before drawing; label "Approximate boundary". No license stated on either layer. Local copy: `sp_boundary.geojson`.
- Center used: CEQAnet's SEIR point, 37°28'26.1"N 122°7'45.1"W (the Final and NOD points, 37°16'57"N 122°4'32"W, are wrong; they fall in the South Bay, not East Palo Alto).

Massing lead: plan-scale, so zones only. SP Figure 6-1 Land Use Zones Map and Figure 6-3 Maximum Height Map (Chapter 6; heights in feet), Figure 4-5 Maximum Heights.

Press or non-official: not used. The leads named Sobrato and University Circle; Sobrato does not appear by name on the City's project list (University Circle, 1900–2050 University Ave, has only a "Phase II" design review page, and was not checked further).
