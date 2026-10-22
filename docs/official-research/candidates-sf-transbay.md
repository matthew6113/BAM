# Official-source findings: Transbay and Rincon towers (San Francisco)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/transbay-parcel-f/`, `524-howard/` (with the Planning Commission agendas in `524-howard/agendas/`),
`transbay-block-4/` and `620-folsom/`, all git-ignored), and live queries of DataSF: development pipeline
`6jgi-cpb4` (2026 Q2), Planning records `qvu5-m3a2` and `y673-d69b`, DBI building permits `i98e-djp9`, DBI
inspections `vckc-dh2h`, DBI complaints `gm2e-bten`, parcels `acdm-wktn` and height districts `h9wh-cg3m`. Page
numbers are PDF page numbers.

Matthew asked on 2026-10-19 for the tower "going in by Salesforce Park". Two approved towers sit right beside the park
on the north side of Howard Street between First and Second streets: Transbay Parcel F (542-550 Howard) and, next to
it, 524 and 530 Howard Street. Both are researched here, with two other large Transbay/Rincon candidates from the
Planning Department's pipeline: Transbay Block 4 (200 Main Street) and 620 Folsom Street.

Hosts: none to add. Every source is on `sfplanning.org`, SF Planning's S3 document store
(`sfplanning.s3.amazonaws.com`, the store behind `commissions.sfplanning.org`, cited in the form actually opened) or
`data.sf.gov`. Not reachable from this session and not cited: `sfbos.org` and Legistar (Board files), `tjpa.org`,
`sfocii.org`, `citypln-m-extnl.sfgov.org` (2023+ Planning Commission packets and minutes) and the press.

URL shorthand:
- PKT = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2016-013312DNXCUAOFAVARSHDPCAMAPGPA_DRAFT.pdf`
  (Planning Commission packet for 542-550 Howard Street (Transbay Parcel F), hearing Jan 9, 2020: executive
  summary, draft motions and resolutions, draft ordinances, Exhibit B plans, Exhibit D community plan evaluation;
  454 pp., 151 MB, sha256 `4edfeb92...ce59`)
- MIN0109 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200109_cal_min.pdf` (minutes, Jan 9, 2020)
- MIN0128 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20210128_cal_min.pdf` (minutes, Jan 28, 2021)
- MIN0623 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20220623_cal_min.pdf`,
  MIN0728 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20220728_cal_min.pdf` (minutes, 2022)
- AG(date) = `https://sfplanning.org/sites/default/files/agendas/...` (Planning Commission agendas; full URLs in the
  draft records: 2020-01/20200109_cal.pdf, 2021-01/20210128_cal.pdf, 2022-07/20220728_cal.pdf,
  2024-10/20241024_cpc%20%28ID%201476978%29.pdf, 2025-04/20250410_cpc%20%28ID%201504528%29.pdf)
- PIPE(blklot) = `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=...`; PRJ(id) =
  `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=...`; REC(id) =
  `https://data.sf.gov/resource/y673-d69b.json?record_id=...`; DBI(n) =
  `https://data.sf.gov/resource/i98e-djp9.json?permit_number=n`

| project | stage | size (official) | recommendation |
|---|---|---|---|
| Transbay Parcel F (`transbay-parcel-f`) | entitled (approved 2020, amended 2021; no site permit) | 61 stories, 749 ft 10 in roof (799 ft 9 in top); ~957,000 gsf; 165 homes, 189-room hotel, 275,674 sf office; 0.74 acres | **INCLUDE** |
| 524 and 530 Howard Street (`524-howard`) | entitled (approved 2024; no site permit) | 72 stories, ~795 ft roof (~844 ft top); 672 homes (68 affordable); ~0.40 acres | **INCLUDE** |
| Transbay Block 4, 200 Main Street | proposal withdrawn (zoning changes recommended 2022, withdrawn 2025) | 47-story, 513-ft tower + 16-story building; 681 homes (306 affordable) | **EXCLUDE** (lead) |
| 620 Folsom Street | application on hold since 2023-24; DBI permit withdrawn | 62 stories, 640 ft; 826 homes | **HOLD** (lead) |

---

## transbay-parcel-f

Recommendation: **INCLUDE** (stage `entitled`). The tower Matthew most likely means: it would stand on the vacant lot
between Howard Street and Salesforce Park, with a bridge into the park. Approved in 2020 and amended in 2021; DBI
permitted test trenches and test shafts but hasn't issued the site permit.

Documents read:
- PKT: executive summary (pp. 1-7), draft Downtown Project Authorization (pp. 9-60, incl. findings and conditions),
  draft PCA/MAP ordinance (pp. 120-130), plan sheets (pp. 369-454: plans pp. 384-394, section p. 395, site
  parcelization p. 435, bulk diagram p. 437), community plan evaluation (pp. 172-200, skimmed).
- MIN0109 (items 13a-13f, pp. 7-11), AG 2020-01-09; MIN0128 (items 7a-7e, pp. 5-8), AG 2021-01-21 and 2021-01-28.
- DataSF: PIPE(3721016); PRJ(2016-013312PRJ); REC children 2016-013312CUA, -CUA-02, -DNX, -DNX-02, -DVA, -ENV, -GPA,
  -MAP, -MCM-02, -OFA, -OFA-02, -PCA, -PPA, -SHD, -TDM, -VAR; DBI permits on lots 016/135/136/138; inspections and
  complaints; parcels of block 3721; height districts.

| field | official value | source | verbatim quote |
|---|---|---|---|
| lots, owner, sponsor | Block 3721 lots 016, 135, 136, 138; sponsor F4 Transbay Partners, LLC; owner Parcel F Owner, LLC | PKT p.1 | "Block/Lot: 3721/016, 135, 136, 138"; "Project Sponsor: F4 Transbay Partners, LLC"; "Property Owner: Parcel F Owner, LLC" |
| applicant | Cameron Falconer of Hines | PKT p.10 | "On October 13, 2016, Cameron Falconer of Hines, acting on behalf of F4 Transbay Partners, LLC (hereinafter "Project Sponsor"), submitted an application ... for a Preliminary Project Assessment" |
| site | 32,229 sq ft (0.74 acres), undeveloped, train box in NW corner | PKT p.12 (finding 3) | "The Project Site ("Site") consists of four contiguous lots (Lots 016, 135, 136, and 137) within Assessor's Block 3721, totaling 32,229 square feet (0.74 acres) in area. ... is undeveloped at-grade and served as a construction staging area for the adjacent Salesforce Transit Center"; "A below-grade "Train Box" is located within the northwest corner of the Site, occupying approximately 12,000 square feet" (note: "137" here; every other part of the approvals says 138) |
| land sale | acquired from the TJPA | PKT p.123 (draft PCA/MAP ordinance) | "the Project sponsor acquired the site from the Transbay Joint Powers Authority with the land sales proceeds used to support completion of the Transbay Transit Center" |
| project | 61 stories, 749'-10" (799'-9"); ~957,000 gsf; 165 du; 189 rooms; 275,674 sf office; ~9,000 sf retail; ~20,000 sf open space; 183 parking | PKT p.12 (finding 2), p.2 | "a new 61-story mixed-use building reaching a height of 749'-10" tall (799'-9" inclusive of rooftop screening/mechanical equipment). The Project would include 165 dwelling units, 189 hotel rooms, 275,674 square feet of office use floor area, approximately 9,000 square feet of retail space, approximately 20,000 square feet of open space, 178 Class 1 and 34 Class 2 bicycle parking spaces, and four below-grade levels that would accommodate up to 183 vehicle parking spaces"; p.2: "a total of approximately 957,000 gross square feet of floor area" |
| bridge | to Salesforce Park | PKT p.12 | "The Project also would construct a pedestrian bridge providing public access to Salesforce Park located on the roof of the Transbay Transit Center." |
| unit mix | 21 one-bed, 92 two-bed, 52 three-bed | PKT p.60 | "The Project contains, 21 one-bedroom, 92 two-bedroom, and 52 three-bedroom units" |
| levels | hotel 8-16, office 17-31, mech 32, amenity 33, homes 34-61; roof +749'-10", top +800'-0" | PKT pp.390-393 (plan titles), p.395 (section) | "PLAN - LEVEL 8 TO16 - TYPICAL HOTEL FLOOR"; "PLAN - LEVEL 17 TO 30 - TYPICAL OFFICE FLOOR"; "PLAN - LEVEL 34 TO 61 - TYPICAL RESIDENTIAL FLOOR"; section: "62 + 749'-10" ... ROOF TOP", "TOP + 800'-0"", "8 ... + 108'-0"", "5 ... + 64'-0"", "33 ... + 429'-10"" |
| floor plates | upper tower avg 15,330 sf; lower 18,590 sf | PKT p.26, p.437 | p.26: "a much narrow upper tower average floor plate area of 15,330 sf"; p.437: "15,330 sf ... 82%" and "18,590 sf" |
| cantilever | tower shifted off the train box | PKT pp.12-13 | "the proposed mixed-use building is purposely set back from the northwest corner of the Site ... by cantilevering the building podium over the area of the Train Box, thereby shifting the majority of the tower's mass onto Lots 016 and 135" |
| CEQA | community plan evaluation under the Transit Center District Plan EIR, Aug 27, 2019 | PKT p.11 | "On August 27, 2019, the Department determined that the proposed application did not require further environmental review under Section 15183 of the CEQA Guidelines" |
| shadow | Rec and Park Commission Res. 1909-016, Sept 19, 2019 | PKT p.11 | "On September 19, 2019, the Recreation and Park Commission ... recommended, through Resolution No. 1909-016, that the Planning Commission find that the shadows cast by the Project would not be adverse" |
| 2020 approvals | Jan 9, 2020: 20613 (GPA), 20614 (PCA/MAP), 20615 (shadow, 5-1), 20616 (DNX), 20617 (OFA), 20618 (CUA) | MIN0109 pp.7-11 | 13d: "ACTION: Approved with Conditions AYES: Diamond, Fung, Johnson, Koppel, Melgar, Moore ABSENT: Richards RESOLUTION: 20616"; 13c: "NAYS: Moore ... RESOLUTION: 20615" (the minutes label all six "RESOLUTION"; Planning's DVA record calls 20615-20618 motions) |
| height swap | 750-S-2 ↔ 450-S within the site; part of lots 135/138 from P to C-3-O(SD) | MIN0109 p.8 (13b); DataSF `h9wh-cg3m` | "revise Zoning Map HT-01 to reclassify the height and bulk district designations for a portion of the project site from 750-S-2 to 450-S and from 450-S to 750-S-2"; the height layer now shows 1,309 sq ft of lot 016 in 750-S-2 and 4,412 sq ft of lot 138 in 450-S, matching PKT p.435 ("LOT 16 (750'): 1,310 SF") |
| 2021 amendments | Jan 28, 2021: DA recommended (Motion 20841), PCA/MAP (Res. 20842), DNX-02/CUA-02/OFA-02 (Motions 20843-20845) | MIN0128 pp.5-8 | "Request to amend Conditions of Approval of Motion No. 20616 ... to reflect a change in the compliance with the inclusionary affordable housing requirements through payment of an in-lieu affordable housing fee to the Office of Community Investment and Infrastructure for use within the Transbay Redevelopment Project Area"; "MOTION: 20843" |
| DA, map records | closed as approved | REC(2016-013312DVA), REC(2016-013312MAP) | "record_status": "Closed - Approved", "close_date": "2021-11-08" (both) |
| validity | 3 years from when the code/map amendments take effect, unless a site permit issues | PKT p.51 (condition 1) | "The authorization and right vested by virtue of this action is valid for three (3) years from the date that the Planning Code text amendment(s) and/or Zoning Map amendment(s) become effective. The Department of Building Inspection shall have issued a Building Permit or Site Permit to construct the project ... within this three-year period." |
| site permit | filed 2019-03-21, not issued | DBI(201903215849) | "to erect a type 1-a, 62 story, mixed use condo with 165 dwelling units, hotel, office and retail with 5 story basement.", "status": "filed", "last_permit_activity_date": "2023-08-04" |
| site work permits | archaeology trenches issued 2020-02-24; two test drilled shafts issued 2020-09-14 (revision 2021-11-16); shoring/excavation filed 2021-12-08, not issued | DBI(202002053600), DBI(202006259099), DBI(202109158507), DBI(202112083939) | "archeological exploration of designated archelogically sensitive areas by excavating trenches"; "installation of two drilled shafts, testig of one drilled shaft, and associated site preperation." "status": "issued"; "cmu wall, shoring wall and excavation." "status": "filed" |
| inspections | none listed for these permits | `vckc-dh2h` (block 3721 lots 016/135/136/138) | only a 2024 complaint investigation ("Fence not secured") |
| pipeline 2026 | still "PL Approved" | PIPE(3721016) | "current_status": "PL Approved", "approved_date_planning": "2020-01-09" |
| newer filings | none on the four lots after 2021 | PRJ/REC by block 3721 | — (absence, checked 2026-10-19) |

Stage: **entitled**. Approvals are in hand and the 2026 pipeline lists the project as approved; no vertical work. The
2020 and 2021 test trenches and test shafts are investigations, not site work. Whether the approvals are still valid
(three-year term, unless the development agreement extends it) is in `verify`.

Boundary: DataSF parcels, blklot 3721016, 3721135, 3721136, 3721138 (the lots in every approval). About 31,990 sq ft
(0.73 acres) as drawn against 32,229 sq ft. The west edge follows the curved bus-ramp property (lots 134 and 137,
TJPA), which isn't part of the site. Accuracy: official. It touches the 524-530 Howard site along lot 014's west
line (no overlap). About 15,400 sq ft of it falls inside `the-portal`'s 40-m alignment corridor; that overlap is
real on the ground (the train box is under the site) and the corridor "is not a property line".

Massing: traced from the vector floor plans in PKT Exhibit B. Each plan carries the site's property line (dash-dot);
its six right-angled corners were matched to the parcels' corners (similarity, RMS 0.06 m, 0.5323 ft/pt). Four
volumes: levels 1-4 (level 2 outline, p.387, drawn open along the east property line and closed up it; 0-64 ft,
18,575 sq ft), levels 5-7 (level 7 outline, p.390; 64-108 ft, 17,790 sq ft), levels 8-32 (typical office outline,
p.391, shared by the hotel floors; 108-429.8 ft, 18,238 sq ft) and levels 33-61 (typical residential outline, p.393;
429.8-749.8 ft, 14,982 sq ft). The traced plates match the packet's bulk figures (lower 18,590, upper 15,330 sq ft).
Not drawn: the crown to 799 ft 9 in, the ground floor's own outline, the terraces of levels 5-6, levels 31-32, the
bridge. Illustrative; all `entitled`.

Press-only: none used. (A web search turned up Bisnow pieces on the 2019-2020 approvals; not opened.)

Open items: the Board ordinances (Files 191259/201385, 201386) and the development agreement's term; whether the
approvals are still in force; whether the test shafts were drilled; 61 vs 62 stories; the "137" typo in finding 3.

---

## 524-howard

Recommendation: **INCLUDE** (stage `entitled`). Also beside Salesforce Park (directly across Natoma Street), and the
taller of the two. The approval letter and plans are on `citypln-m-extnl.sfgov.org`, which couldn't be reached, so
the record rests on Planning's DataSF records and Planning Commission agendas; the massing is a placeholder.

Documents read:
- DataSF: PIPE(3721013); PRJ(2023-010883PRJ); REC(2023-010883TDM), REC(2023-010883GPR); REC(2024-008633PCA);
  PRJ(2025-000685PRJ), REC(2025-000685CUA); earlier parking-lot records 2019-020048, 2022-008234; DBI(202311170986)
  and the other permits on lots 013/014; parcels; height districts.
- AG 2024-10-24 (item 14, p.5), AG 2025-04-10 (item 6, p.5), AG 2020-09-03 and AG 2023-02-16 (earlier parking-lot
  extensions).

| field | official value | source | verbatim quote |
|---|---|---|---|
| project | 72 stories, ~795 ft (~844 ft with appurtenances), 818,922 gsf residential, 672 du, 68 at 50% AMI | PIPE(3721013) | "construct a new 72-story, approximately 795-foot tall (approximately 844 feet inclusive of permitted rooftop appurtenances) residential building containing 818,922 gross square feet of residential use. The Project includes 672 dwelling units, with 68 dwelling units dedicated to households earning 50% AMI. The dwelling unit mix is comprised of 424 one-bedroom units, 180 two-bedroom units, and 68 three-bedroom units." |
| existing | parking lot (524) and 4-story 29,955 sf commercial building (530) | PIPE(3721013) | "would demolish an existing surface parking lot located at 524 Howard Street and a four-story, 29,955 square-foot commercial building located at 530 Howard Street" |
| parking, deck, bridge | 3 above-grade garage levels, 149 cars, 422 Class 1 bikes; public 5th-floor deck with path to Salesforce Park | PIPE(3721013) | "three levels of above-grade, off-street garage parking, including 149 vehicular parking spaces"; "a publicly-accessible fifth-floor deck with a walking path connecting to Salesforce Park accessed via elevators on the Natoma Street frontage" |
| approval | "PL Approved" June 18, 2024; record closed "Approval Ltr Issued" Sept 17, 2024 | PIPE(3721013); PRJ(2023-010883PRJ) | "current_status": "PL Approved", "approved_date_planning": "2024-06-18", "state_density": true; "record_status": "Closed - Approval Ltr Issued", "project_decision": "Approved", "close_date": "2024-09-17" |
| density bonus | concessions and waivers incl. height and bulk | REC(2023-010883TDM) | "Consistent with the state density bonus law, the proposed project requests the following three incentives and concessions: (1) consolidate Section 415b inclusionary housing requirement such that project's base project will contain 15% on-site units at 50% AMI; (2) allow relocation of existing curb cut on Howard Street (Sec 155); and (3) allow above-grade parking (Sec 155). ... waivers from ... maximum allowable lot coverage (Sec 134); residential open space requirement (Sec 135); dwelling unit unit exposure requirements (Sec 140); active use requirements on Howard and Natoma streets (Sec 145.1); maximum allowable width of parking and loading entrance on Natoma Street (Sec 145.1); building height (Sec 260); setback and bulk reduction controls (Sec 270)." |
| building area | ~882,251 gsf building; 818,275 sf residential GFA | REC(2023-010883TDM) | "approximately 882,251 gross square feet of building area; 818,275 square feet of residential Gross Floor Area" (the project record gives "residential_prop": "882899") |
| height district | 450-S | PIPE(3721013); `h9wh-cg3m` | "height_district": "450-S" |
| bridge referral | General Plan referral, closed approved Mar 4, 2024 | REC(2023-010883GPR) | "A pedestrian bridge proposed over the Natoma Street right-of-way, connecting a proposed 72-story residential tower at 524 and 530 Howard Street with the Salesforce Transit Center Park." "Closed - Approved" |
| site permit | filed Nov 17, 2023, lots 013 and 014; not issued | DBI(202311170986) | "erect a 71-story above grade containing 672 w/ associated amenity space. levels 2-4 house parking & building support services. the building will have 1 basement level below grade ... there is a bridge connection from level 5 to saleforce park.", "number_of_proposed_stories": "72", "status": "filed" |
| fee waiver | ordinance BF 240879 heard Oct 24, 2024; Planning record closed approved Mar 27, 2025 | AG 2024-10-24 p.5; REC(2024-008633PCA) | "Ordinance, introduced by Supervisor Dorsey, amending the Planning Code to waive the Transit Center District Open Space Impact Fee for 524 Howard Street, LLC's development project at 524 and 530 Howard Street in recognition of the project's proposed construction of a pedestrian bridge connecting to the Transbay Transit Center's rooftop park" |
| parking lot | 2-year extension of the temporary public parking lot, Apr 10, 2025 | AG 2025-04-10 p.5; PRJ(2025-000685PRJ) | "Request for Conditional Use Authorization ... to permit a two-year extension of an existing, temporary Public Parking Lot"; "project_decision": "Approved", "project_decision_date": "2025-04-10" |
| 530 Howard in use | parcel delivery use permit completed Sept 24, 2025 | DBI(202407096030) | "change of use from office to parcel delivery service for cannabis products." "status": "complete", "completed_date": "2025-09-24" |

Stage: **entitled** (Planning approval; no site permit; existing building and parking lot still in use).

Boundary: DataSF parcels, blklot 3721013 and 3721014 (the DBI application's lots; lot 015, 540 Howard, isn't part).
About 17,460 sq ft (0.40 acres). Accuracy: official. No overlap with Parcel F (they share lot 014's west line); about
3,300 sq ft at the Natoma Street end falls inside `the-portal`'s 40-m corridor (the corridor's width, not a real
conflict: the train box runs under the Transit Center north of Natoma).

Massing: no drawing could be opened. One placeholder volume: the site inset evenly (10.2 ft) to the building's
average gross floor area per story (882,251 / 72 = about 12,250 sq ft), extruded to 795 ft. Its outline and position
are assumptions, stated in the file. The module re-reads the TDM record and stops if its figures change.
Illustrative, `entitled`. (A sibling record, 536 Mission, draws its placeholder as the whole lot instead; either way
the lead may prefer one convention.)

Press-only (kept in `reported`; found by web search, pages not reachable from this session): developer Bayhill
Ventures (SF YIMBY, Oct 2024); ministerial approval under AB 2011 with the state density bonus law, dated Sept 25
by KTVU (year from context, 2024).

Open items: the approval letter (date, pathway, conditions) and plans; the fee-waiver ordinance's number;
floor-area and story-count differences across records; the developer behind 524 Howard Street, LLC.

Photo: none looked for.

---

## Transbay Block 4 (200 Main Street) — not added

Recommendation: **EXCLUDE for now**. The 47-story design was recommended by the Planning Commission in 2022, but the
zoning changes it needed were withdrawn in 2025 and its building permits were never issued; Planning's 2026
pipeline entry still reads "PL Filed". It is one project with two buildings: DBI's two 2019 applications are the
16-story mid-rise (192 homes) and the 47-story tower (491 homes) = 683.

| field | official value | source | verbatim quote |
|---|---|---|---|
| project (2022) | 47-story tower 513 ft + 6-story townhouses + 16-story mid-rise; 681 du, 306 affordable | AG 2022-07-28 pp.6-7; MIN0728 pp.9-11 | "a 47-story tower (513-feet exclusive of mechanical penthouse) with 6-story townhouse adjunct, a 16-story mid-rise building and a single-story shared podium with shared underground facilities. The Project would include approximately 681 residential units, of which 306 (45%) would be affordable" |
| site | block bounded by Howard, Main, Beale and the Tehama alignment; lot 010 | same | "the block bounded by Howard Street on the north, Main Street on the east, Beale Street on the west, and the alignment of Tehama Street on the south, Lot 010 in Assessor's Block 3739" |
| actions | GPA initiated June 23, 2022 (Res. 21133); July 28, 2022: map change recommended (Res. 21152), GPA (21153), Redevelopment Plan amendment conformity (21154) | MIN0623 p.9; MIN0728 pp.10-11 | "RESOLUTION: 21152", "RESOLUTION: 21153", "RESOLUTION: 21154" |
| withdrawn | map amendment withdrawn Jan 2, 2025; GPA withdrawn Sept 23, 2025 | REC(2018-015785MAP), REC(2018-015785GPA) | "record_status": "Closed - Withdrawn", "close_date": "2025-01-02"; "Closed - Withdrawn", "2025-09-23" |
| height map | still 50/85/450-TB | `h9wh-cg3m` at the site | "height": "50/85/450-TB" |
| permits | both filed Dec 20, 2019, never issued | DBI(201912200111), DBI(201912200133) | "erect a 16 stories 192 residential type 1a construction with two basement apartment building"; "erect a 47 stories 491 residential units type 1a construction no basement apartment building", "status": "filed" |
| CEQA | clearance issued Jan 31, 2023 | REC(2018-015785ENV) | "Closed - CEQA Clearance Issued", "close_date": "2023-01-31" |

Reported (not opened): the developer (F4 Transbay Partners / Hines) let its option lapse in June 2024 (SF Examiner,
`https://www.sfexaminer.com/news/business/two-sf-tower-projects-face-troubles-amid-weak-downtown-economy/article_c74c1c8a-29df-11ef-822a-efd6c6092675.html`);
a 2025 TJPA presentation (`https://www.tjpa.org/media/39745/download`, official host, blocked) reportedly describes a
new affordable-housing RFP for "Block 4 West". Revisit when OCII selects a new developer.

## 620 Folsom Street — not added

Recommendation: **HOLD**. A 62-story, 640-ft, 826-home density-bonus tower (Planning case 2022-009434) whose Planning
applications have been "On Hold" since 2022 filings and whose DBI site permit application was withdrawn in March 2024.
No hearing for it appears in the 377 Planning Commission agendas downloaded from Planning's hearing archive (2019 to
July 2026; five downloads failed).

| field | official value | source | verbatim quote |
|---|---|---|---|
| project | 62 stories, 640 ft, 826 du (118 studio, 118 1-bed, 472 2-bed, 118 3-bed); 50% density bonus | PRJ(2022-009434PRJ) | "Demolition of an existing 3-story office building and construction of a new 62-story, 640 feet height, residential building. ... 826 dwelling units ... 15% of the Base Project units would be affordable to very low income households, allowing for a 50% density bonus." |
| site | 17,550 sq ft, 320-I | REC(2022-009434DNX) | "The project site at 620 Folsom Street (Block 3735/010) has a lot area of 17,550 square feet ... the 320-I Height & Bulk District" |
| status | PRJ, DNX, ENV and SHD all "On Hold" | PRJ, REC | "record_status": "On Hold" |
| DBI | 65-story, 711-unit application withdrawn Mar 11, 2024 | DBI(202212168497) | "to erect a 65-story, 711-dwelling units, type 1-a, mixed-used building.", "status": "withdrawn", "status_date": "2024-03-11" |
| earlier | 2021 PPA: 58 stories, 575 ft roof, 623 units | REC(2021-008617PPA) | "a 58 story tower will be constructed, 575' to the roof and 600' to the elevator enclosure" |

---

## Leads not added

- **Transbay Block 4, 200 Main Street** — 47-story 513-ft tower and 16-story building, 681 homes (306 affordable);
  zoning changes recommended July 28, 2022, withdrawn 2025; permits never issued.
  `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20220728_cal_min.pdf`. Exclude until OCII picks a new
  project for the block.
- **620 Folsom Street** — 62 stories, 640 ft, 826 homes; Planning applications on hold, DBI application withdrawn
  2024. `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2022-009434PRJ`. Hold; re-check if the hold lifts.
- **Transbay Block 2, 200 Folsom Street** (seen in passing) — two 100% affordable buildings (85 ft and 165 ft, 335
  homes; DBI permits for 151 senior and 184 homes, first construction documents 2024, the senior building's permit
  completed July 2026). `https://data.sf.gov/resource/i98e-djp9.json?permit_number=202208019628`. Below the
  500-ft bar; not recommended for this group.
- **The earlier 524 Howard Street project** (Planning case 2013.0882, 334 homes; PKT p.13: "an approximately 495-foot
  tall, 48-story mixed use residential and hotel development") — superseded by the 2023 application; not drawn.

Notes for the lead:
- `official_boundaries.build()` writes a zero-area degenerate ring as a second part of both new boundary files (as it
  already does for `related-santa-clara`, `tasman-east` and `freedom-circle`); harmless to the tests, but a filter on
  part area in `build()` would tidy every file.
- The Parcel F packet (151 MB) is pinned by `massing_transbay_parcel_f.py` into `data/raw/docs/`.
