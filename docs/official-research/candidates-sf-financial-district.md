# Official-source findings: Financial District towers (530 Sansome, Matson Block / 77 Beale, 536 Mission)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/530-sansome/`, `data/raw/official/77-beale/`, `data/raw/official/sf-fidi-agendas/`, git-ignored)
and live queries of DataSF (development pipeline `6jgi-cpb4`, 2026 Q2 snapshot; Planning records `qvu5-m3a2` and
`y673-d69b`; building permits `i98e-djp9`; parcels `acdm-wktn`; special use districts `5yf5-ms5f`; height and bulk
districts `h9wh-cg3m`) and CEQAnet. Page numbers are PDF page numbers. Figures were looked at as rendered pages
(`pdftoppm`) and their dimension strings read with pdfplumber.

Matthew asked on 2026-10-19 for large San Francisco towers, naming "the one near Jackson Square [that] is replacing a
fire station" and "one going in by Salesforce Park". The first is 530 Sansome. The Matson Block tower at 77 Beale
Street is one candidate for the second: its notice of preparation puts the site "within 300 feet of Salesforce
Park" (other groups are covering the Transbay towers right beside the park, Parcel F and 524 Howard).

Hosts: none to add. Every source is on `ceqanet.lci.ca.gov`, `sfplanning.org` or `data.sf.gov`. Not reachable from
this session and not cited: `citypln-m-extnl.sfgov.org` (2023+ Planning Commission packets, minutes, CEQA documents
linked from the environmental review documents page), `sfbos.org` and `sfgov.legistar.com` (the Board's 2025
ordinances for 530 Sansome), the S3 mirror for the 2026 packet (`commissions/cpcpackets/2025-007507DNXOFASHD.pdf`
returns 403), and the press sites (sfyimby.com, multifamilydive.com, growsf.org: proxy 403).

URL shorthand:
- NOP530 = `https://ceqanet.lci.ca.gov/2024110311/1` (notice of preparation, Nov 8, 2024; CEQAnet page and attachments)
- DEIR = `https://ceqanet.lci.ca.gov/2024110311/2/Attachment/NHEHNp` (447 Battery and 530 Sansome Street Project Draft
  EIR, March 2025, 276 pp., sha256 `d127a20a…9988`)
- RTC = `https://ceqanet.lci.ca.gov/2024110311/3/Attachment/dFOxC_` (Responses to Comments, July 2025, 162 pp.)
- NOD = `https://ceqanet.lci.ca.gov/2024110311/4/Attachment/BML5I0` (Notice of Determination, Oct 29, 2025, 4 pp.)
- AG(date) = Planning Commission agenda PDFs under `https://sfplanning.org/sites/default/files/agendas/`:
  AG240321 = `2024-03/20240321_cpc%20%28ID%201425983%29.pdf`, AG250410 = `2025-04/20250410_cpc%20%28ID%201504528%29.pdf`,
  AG250417 = `2025-04/20250417_cpc%20%28ID%201505632%29.pdf`,
  AG250515 = `2025-05/20250515_cpc%20%28ID%201511160%29.pdf`,
  AG250717 = `2025-07/20250717_cpc_jnt_RecPark%20%28ID%201522127%29.pdf` (joint hearing with the Recreation and Park
  Commission), AG260910 = `2026-09/20260910_cpc%20%28ID%201586266%29.pdf`
- NOPM = `https://ceqanet.lci.ca.gov/2025120794/Attachment/gufVD2` (Matson Block Project notice of availability and
  notice of preparation of an EIR, Dec 17, 2025, 28 pp., sha256 `2f97a97f…2809`)
- REC(id) = `https://data.sf.gov/resource/y673-d69b.json?record_id=<id>` (child Planning records);
  PRJ(id) = `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=<id>`; PIPE(blklot) =
  `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=<blklot>`; DBI(n) =
  `https://data.sf.gov/resource/i98e-djp9.json?permit_number=<n>`

| project | stage | size | recommendation |
|---|---|---|---|
| 530 Sansome Mixed-Use Tower and Fire Station 13 (`530-sansome`) | entitled | 41 stories, ~544 ft (574 ft with mechanical); 372,580–417,770 sq ft office, 100–200 hotel rooms; 4-story, 55-ft fire station; 0.57 acres | **INCLUDE** |
| Matson Block Project / 77 Beale Street (`77-beale`) | entitlement (NOP Dec 2025; ENV record "On Hold") | tower up to 1,225 ft + 75-ft crown; up to 1,919,847 gsf office on the block, 44–437 homes, up to 350 hotel rooms; 3.47 acres | **INCLUDE** |
| 536 Mission Street (`536-mission`) | entitled (Planning Commission, Sept 10, 2026) | 46 stories; office variant 700 ft (752 ft parapet), ~1.22 million sq ft; or mixed-use 649 ft with up to 385 homes; 0.76 acres | **INCLUDE** |

---

## 530-sansome

Recommendation: **INCLUDE** (Matthew's named tower; stage `entitled`). A 41-story office/hotel tower and a separate
new Fire Station 13, approved in 2025 with a development agreement and a special use district. No building permit yet.

Documents read:
- NOD (all 4 pp.), DEIR Chapter 2 (pp. 93–125: project description, Table 2-1, Figures 2-3 to 2-21) and the
  building section and plans (pp. 101–119), RTC Chapter 4 (pp. 53–60: Draft EIR revisions, new Section 2.B).
- CEQAnet project page `https://ceqanet.lci.ca.gov/Project/2024110311` and its four document pages (NOP, EIR, RC, NOD).
- AG240321 (items 3a–3c), AG250410 and AG250417 (Draft EIR hearing), AG250515 (items 9a–9b), AG250717 (items 2–4g).
- `https://sfplanning.org/environmental-review-documents?title=530%20Sansome` (document list; the documents themselves
  link to the blocked `citypln-m-extnl` host, and the CEQAnet copies were used instead).
- DataSF: PRJ(2024-007066PRJ) and its ten child records (CUA, DVA, ENV, GPA, GPR, MAP, OFA, PCA, SHD, TDM);
  PIPE(0206017); permits on block 0206 lots 002/013/014/017 since 2019; parcels on block 0206; SUD layer; height layer.

| field | official value | source | verbatim quote |
|---|---|---|---|
| name | 530 Sansome Mixed-Use Tower and Fire Station 13 (aka 447 Battery and 530 Sansome Project) | NOD p.1 | "Project Title: 447 Battery and 530 Sansome Project (also known as the 530 Sansome Mixed-Use Tower and Fire Station 13 Development Project)" |
| lots, size | Block 0206 Lots 002, 013, 014, 017; 24,830 sq ft | NOD p.1; DEIR p.94 | "Block/Lot: Block 0206/Lots 002, 013, 014, 017" "Lot Size: 24,830 square feet"; "The approximately 24,830-square-foot project site consists of four lots (Assessor's Block 0206, Lots 002, 013, 014, and 017) located on the block bound by Sansome Street to the west, Washington Street to the north, Battery Street to the east, and Merchant Street to the south" |
| frontages, excluded lot | 99 ft Sansome, 74 ft Battery, 179 ft Washington, 276 ft Merchant; 423 Washington not included | DEIR p.96 | "approximately 99 feet of frontage on Sansome Street, 74 feet of frontage on Battery Street, 179 feet of frontage on Washington Street, and 276 feet of frontage on Merchant Street. The project site covers most of Block 0206, except for lot 018-124 at 423 Washington Street" |
| existing | 1974 fire station; three commercial buildings incl. landmark 447 Battery | DEIR pp.96, 98; NOD p.2 | "The Fire Station 13 was constructed in 1974."; "The three-story building at 447 Battery Street is currently designated as a historical landmark under article 10"; NOD: "demolition of the existing 17,800-square-foot, 3-story commercial building at 425 Washington Street, and the 12,862-square-foot, 2-story commercial building at 439-445 Washington Street; the 20,154-square-foot, 3-story commercial building at 447 Battery Street; and the 18,626-square-foot fire station at 530 Sansome Street" |
| tower (approved) | ~544 ft, 574 ft with mechanical; 41 stories; 27,030 sq ft retail; office 372,580–417,770; hotel 128,010–189,130 sq ft, 100–200 rooms; 74 parking | NOD p.2 | "a 4-story replacement fire station and a separate high-rise building up to 41 stories tall"; "The high-rise building, approximately 544 feet tall {574 feet total, including rooftop mechanical equipment), would be located on the remaining three parcels and would include approximately 27,030 square feet of retail uses (cafe, restaurant, and ballroom/pre-function/meeting spaces on levels 1 through 3); between approximately 372,580 and 417,770 square feet of office space; and between approximately 128,010 and 189,130 square feet of hotel space for approximately 100 to 200 hotel rooms. There would be three below-grade levels under the high-rise building, which would provide approximately 74 vehicle parking spaces" |
| office/hotel flexibility | five middle floors either way | DEIR p.100 | "the proposed project approvals would allow for post-entitlement refinement to the final design to program five of the middle floors of the building as either office or hotel" |
| fire station | 4 stories, ~55 ft (60 ft total), ~31,200 sq ft incl. basement, 447 Battery parcel | NOD p.2 | "The replacement fire station would be located on the 447 Battery Street parcel and would include approximately 31,200 square feet (including one basement level with 18 vehicle parking spaces and four class 1 bicycle spaces) in a 4-story, approximately 55-foot-tall building {60 feet total to the roof, including amenity space on the fourth floor and rooftop mechanical equipment) on the eastern portion of the project site" |
| Merchant Street | shared street, ~10,364 sq ft POPOS | RTC p.53 | "into a shared street/living alley with approximately ~~12,695~~ 10,364 square feet of privately maintained public open space improvements" (strike/underline in the original) |
| sponsor / applicants | EQX Jackson SQ Holdco LLC; SF Real Estate Division; SF Fire Department | NOD p.1 | "Project Applicant: James Abrams, J. Abrams Law, P.C. on behalf of EQX JACKSON SQ HOLDCO LLC ... Andrico Penick, San Francisco Division of Real Estate ... Michael Mullin, San Francisco Fire Department" |
| land exchange | City lot 530 Sansome swapped for 447 Battery before construction; fire station built at no cost to the City | REC(2024-007066GPR) | "The CPEA would provide for the exchange of the City-owned 530 Sansome Street parcel for 447 Battery Street parcel, with the closing on the transaction to occur prior to the commencement of project construction. The CPEA would provide for completion of the final construction drawings, permit processing, and construction of the new Fire Station 13 at 447 Battery Street at no cost to the City." |
| rezoning, SUD | lots 013/014/017 200-S to 555-X; new SUD over all four lots; conditional rescission of the landmark | AG250717 p.6 (item 4d); REC(2024-007066PCA) | "to create the 530 Sansome Mixed-Use Tower and Fire Station 13 Special Use District (SUD) ... and to conditionally rescind the Article 10 landmark designation of 447 Battery Street"; "HT01 to increase the maximum height for Assessor's Block 0206, Lots 013, 014, 017 from 200-S to 555-X. The height and bulk district for Lot 002 (447 Battery Street) would not be revised." |
| rezoning in effect | DataSF zoning layers show the SUD and a 555-X height district | `https://data.sf.gov/resource/5yf5-ms5f.json?name=530%20Sansome%20Mixed-Use%20Tower%20and%20Fire%20Station%20SUD`; `https://data.sf.gov/resource/h9wh-cg3m.json?height=555-X` | "name": "530 Sansome Mixed-Use Tower and Fire Station SUD"; "height": "555-X", "gen_hght": "555" (the 555-X polygon covers the tower lots; lot 002 stays 200-S) |
| office allocation | up to 420,000 gsf from the large-cap pool requested; Planning record approved | AG250717 p.7 (item 4g); REC(2024-007066OFA) | "Request for Large Cap Office Allocation pursuant to Planning Code Sections 320-325 to authorize up to 420,000 gross square feet of general office use from the large cap pool and return 40,500 square feet of office use to the small cap"; record_status "Closed - Approved", closed 2025-08-04 |
| CEQA timeline | NOP Nov 8, 2024; Draft EIR Mar 12, 2025; RTC Jul 3, 2025; NOD Oct 30, 2025 | CEQAnet project page | document list: "NOD ... 10/30/2025", "RC ... 7/3/2025", "EIR ... 3/12/2025", "NOP ... 11/8/2024" |
| Draft EIR hearing | April 17, 2025 (continued from April 10); comments to April 28 | AG250417 p.4 | "Public Hearing on the Draft Environmental Impact Report" ... "Written comments will be accepted ... until 5:00 PM on April 28, 2025" "(Continued from Regular hearing April 10, 2025)" |
| informational hearing | May 15, 2025 | AG250515 pp.4–5 | "530 SANSOME/447 BATTERY STREET PROJECT – Informational Presentation"; item 9b "Initiation of General Plan Amendments ... most predominantly to amend the Height and Bulk Designation for Lots 013, 014, and 017 from 200-S to 555-S" |
| approvals | FEIR certified July 17, 2025 (Motion 21773); Board approved Oct 21, 2025; Mayor signed Oct 27, 2025 | NOD pp.1–3 | "FEIR Certification Date: July 17, 2025" "Final Approval Date: October 27, 2025"; "The San Francisco Planning Commission certified the Final Environmental Impact Report, adopted CEQA Findings, a State of Overriding Considerations, and the Mitigation, Monitoring, Reporting Program {Motion No. 21773), recommended approval of the project to the Board of Supervisors ... on July 17, 2025, in a joint session with the Recreation and Parks Commission. The Board of Supervisors approved the project's legislation on October 21, 2025. The project was officially approved when the Mayor signed the project's legislation on October 27, 2025." |
| Board files | 250764 GPA, 250697 zoning/code, 250802 Merchant St, 250804 CPEA, 250698 DA, 250803 hotel incentive | NOD p.3 | "file no. 250764 {General Plan Amendment), 250697 (Zoning Map and Planning Code Amendment), 250802 (Merchant Street Major Encroachment Permit), 250804 (Conditional Property Exchange Agreement), 250698 (Development Agreement), and 250803 (Hotel Incentive Agreement)" |
| Planning records | PRJ decision "Approved" 2025-07-17; CUA, OFA, SHD, GPR closed approved; DVA, GPA, MAP, PCA "Approved"; TDM under review | PRJ(2024-007066PRJ), REC(…) | "project_decision": "Approved", "project_decision_date": "2025-07-17"; CUA "Closed - Approved" 2025-08-04; SHD 2025-07-22; GPR 2025-09-09 |
| earlier project | 19-story hotel + fire station on lots 013/014/017, approved July 29, 2021; MND; extended 2024 | AG240321 p.3; RTC p.56 | "On July 29, 2021, the Planning Commission approved a Downtown Project Authorization, Conditional Use Authorization, Office Development Allocation, and Shadow Findings through Motion Nos. 20955 to 20958, and Resolutions No. 20954"; RTC: "a 19-story building and a four-story replacement fire station"; "In early 2024, the planning commission approved extensions of the 2021 project approvals." |
| construction | ~39 months from 2027 (preliminary) | DEIR p.122 | "Construction of the proposed project would last approximately 39 months, beginning in 2027 (see Table 2-2)." |
| permits | none for this design; the 2019 site permit application for the 19-story project withdrawn | `https://data.sf.gov/resource/i98e-djp9.json?block=0206&lot=017` | 201912200193 "to erect 19 stories, 3 basements, type i-a, 200 hotel rooms with mixed-use building & fire house", status "withdrawn"; nothing filed after (checked Oct 19, 2026) |
| pipeline | "PL Approved" 2025-07-17 | PIPE(0206017) | "current_status": "PL Approved", "current_status_date": "2025-07-17" (its office/hotel figures are the 2024 application's: "375,000 square feet of Office use, 210,000 square feet of Hotel use") |

Stage: **entitled**. All approvals are in hand (NOD); no building permit or construction record.

Boundary: DataSF Parcels (`acdm-wktn`), blklot 0206002, 0206013, 0206014, 0206017 (the lots in the NOD and EIR).
Union about 24,835 sq ft (EIR 24,830). One polygon (the fire station lot adjoins the tower lots). The DataSF special
use district polygon for "530 Sansome Mixed-Use Tower and Fire Station SUD" was compared and not used: it is about
27,500 sq ft, extends north over Washington Street and leaves out most of lot 002, so it doesn't match the four lots
the ordinance applies to. Accuracy: official.

Massing (`pipeline/bam_pipeline/sites/massing_530_sansome.py`): dimensioned SOM plans in the DEIR. Tower 165'-0"
east–west at 2'-7" from the Sansome line (Figures 2-16 to 2-19, pp. 116–119); north–south depth and offsets per
level: hotel/amenity floors 96'-6" (1'-3" each side), level 25 89'-6" (8'-3" north, 1'-3" south), level 37 67'-6"
(15'-9" each side), roof 60'-0" (23'-3" north, 15'-9" south). The N/S section (Figure 2-8, p. 106; text in a
shifted font, read from the rendered page) puts the steps at level 24 (+304'-4"), 28 (+357'-4"), 32 (+410'-4"),
36 (+463'-4") and 40 (+516'-4"), alternating north and south, each 7–7.5 ft (pixel-measured, matching the plan
offsets); lower roof +543'-4", upper roof +555'-0", top +573'-4". Drawn as six nested steps to 304, 357, 410, 463,
516 and 544 ft; the east end of the levels 2–3 plate (174'-3" by 92'-8 1/2", 3'-9" from Sansome) to the level 4
floor at 63 ft; fire station = lot 002 at 55 ft (Figure 2-10, p. 109, shows it filling the lot). Frame: the mapped
tower lots measure 178.2 ft on Washington and 100.8 ft on Sansome (EIR 179 and 99); the plan's dimensions are kept
and laid out from the Washington and Sansome lines. Illustrative; stage `entitled`.

Press-only (kept in `reported`; pages not opened, the proxy refuses them): Related California is the developer
behind EQX Jackson SQ Holdco LLC (`https://sfyimby.com/2025/10/41-story-office-tower-approved-for-530-sansome-street-san-francisco.html`).
A search listing also gives Board ordinance numbers (198-25 for the development agreement, 203-25) on sfbos.org;
not opened, not used.

Open items: the Board ordinance numbers; Planning Commission motion numbers other than 21773; the final office/hotel
split; construction start; the mismatched SUD polygon in DataSF.

Photo: not searched in this pass.

---

## 77-beale

Recommendation: **INCLUDE** (stage `entitlement`). A full-block redevelopment by Hines with a tower of up to
1,225 ft, the tallest proposed in the city, at the start of EIR review. Planning's ENV record is "On Hold".

Documents read:
- NOPM (all 28 pp.: notice of availability pp. 1–5, NOP pp. 6–28 incl. Tables 1–5 and Figures 1–6).
- CEQAnet `https://ceqanet.lci.ca.gov/2025120794` (only document: NOP, received 12/17/2025; no Draft EIR as of
  Oct 19, 2026).
- `https://sfplanning.org/environmental-review-documents?title=Matson` (document list; documents on the blocked host).
- DataSF: PRJ(2021-012562PRJ) and children (DNX, ENV, MAP, OFA, PCA, PTA, SHD, TDM); PIPE(3711013); DBI
  202209082126, 202202157996, 202212087876; parcels on block 3711. All 2024–2026 Planning Commission agendas
  (none mention the project).

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, sponsor | Matson Block Project; Hines | NOPM pp.1, 7 | "Project Title: Matson Block Project"; "Project Sponsor: Hines, c/o Tuija Catalano / Reuben, Junius & Rose, LLP"; "The project sponsor, Hines, proposes to undertake a mixed-use project" |
| site | whole block, 11 lots, 151,390 sq ft (3.47 acres) | NOPM pp.6, 8 | "Block/Lot: Assessor's Block 3711, Lots 005, 006, 007, 008, 009, 010, 011, 012, 013, 014 and 019"; "Lot Size: Approximately 151,390 square feet (3.47 acres)"; "The site is approximately 550 feet north of Salesforce Tower and within 300 feet of Salesforce Park." |
| existing | 7 buildings; 77 Beale 473'6", 1969–71; PG&E left 2024; mostly vacant | NOPM pp.8, 12 | "77 Beale Street 3711/005-014 1969–71 473 feet, 6 inches Office tower Vacant(mostly)"; "in 2021, PG&E sold the buildings and relocated all of its operations elsewhere, with the final move in July 2024" |
| new tower | up to 1,225 ft + 75-ft crown; ~200 ft over Salesforce Tower | NOPM pp.7, 14 | "an up to 1,225-foot-tall tower with a 75-foot-tall architectural crown would be constructed"; "This new tower would exceed the height of the SalesForce Tower, which is currently the City's tallest building, by approximately 200 feet." |
| tower location | not fixed: 229 x 275 ft zone in the south; three positions studied | NOPM p.14 | "The office tower would be located in the "Tower Location Zone" shown in Figure 4, which is a 229-foot by 275-foot area located in the southern portion of the site. However, the exact tower location has not yet been determined and the final tower location could be oriented toward Main Street, Mission Street, or Beale Street." |
| tower envelope | base 275'-6" x 229'-3" to 125 ft; lower 230 x 135 ft to 679 ft; upper 210 x 135 ft to 1,225 ft | NOPM p.23 (Figure 6) | labels "Tower Massing justified on Mission Street", "125' Base", "679' Lower Tower", "1225' Upper Tower"; "Maximum Dimensions": "275'-6"", "229'-3"", "358'-3""; "230'-0"", "135'-0"", "266'-9""; "210'-0"", "135'-0"", "249'-6""; note "Illustrative diagram to show maximum massing for CEQA analysis purposes only. Not representative of actual design." |
| program | office up to 1,919,847 gsf (+350,000), institutional up to 250,000 in lieu; retail 250,000; residential 90,000 gsf at 25 Beale (44–120 units); parking 277–480 | NOPM p.14 (and Table 3 p.18) | "The proposed project would create up to 1,919,847 gsf of office uses, 250,000 gsf of retail (including up to 100,000 gsf for entertainment, and up to 75,000 square feet near the top of the tower for potential observation deck ...), 90,000 gsf of residential (44–120 units at 25 Beale), 7,500 square feet for outdoor entertainment, and up to 135,000 square feet for below-grade parking (for 277–480 spaces)"; "In total the project would include 2,402,347 gsf of built area" |
| new tower size | up to 1,816,711 gsf | NOPM p.15 | "The new tower would include up to 1,580,211 gsf of office use ... In total, the new tower would be up to 1,816,711 gsf." |
| variants | 400-ft building: up to 317 units or 350 hotel rooms; either or both, possibly in the tower | NOPM pp.3, 20; Table 4 p.19 | "a second 400-foot-tall stand-alone building along the site's Main Street façade. The second tower could include up to 317 units (300,000 gsf) of residential use (residential variant) or up to 350 rooms (260,000 gsf) of tourist hotel use"; "The program of development for either or both of the variants could be constructed in addition to the project"; Table 4 "Project Maximums ... Up to 361 – 437 units ... Up to 350 rooms" |
| kept / demolished | 215 and 245 Market kept and renovated; 25 Beale converted; 77 Beale, 45 Beale, 215 Annex, 50 Main garage demolished | NOPM pp.15, 21 | "The historic 215 Market Street (Matson) and 245 Market Street (PG&E) buildings would be retained and renovated"; "Demolition is expected to take approximately 18 months and will include 77 Beale Street, 50 Main Street, 45 Beale Street, and the 215 Market Street Annex." |
| rezoning | new Matson/PG&E Block SUD; 400-S to 1225-S on the south part; DA | NOPM p.14 | "add a new Matson/PG&E Block SUD"; "change the height and bulk designations from the existing 400-S district to 1225-S for south portion of the block"; "The project also requests approval of a Development Agreement." |
| schedule | demolition from end of 2026, done by end of 2032 | NOPM p.21 | "Demolition is anticipated to begin at the end of 2026, with all phases of construction completed by the end of 2032." |
| NOP dates | Dec 17, 2025; scoping meeting Jan 7, 2026; comments to Jan 20, 2026 | NOPM pp.1, 6 | "Date: December 17, 2025"; "PUBLIC SCOPING MEETING INFORMATION Date: January 7, 2026"; "Comment Deadline: January 20, 2026" |
| ENV status | "On Hold" | REC(2021-012562ENV) | "record_status": "On Hold" (DataSF, rows updated Oct 19, 2026) |
| earlier scheme | 85-story, 808-unit tower at 50 Main (2021); DBI application 88 stories, 808 units, withdrawn 2025-09-08 | REC(2021-012562DNX); DBI(202209082126) | "new construction of a residential tower at 50 Main with 808 units in an 85-story tall building; alteration of the existing 473'6" tall, 1,000,180-gsf office building at 77 Beale"; "to construct a 88-story, 808 dwelling units, type 1-a building.", "status": "withdrawn", "status_date": "2025-09-08" |
| revised filing | zoning map amendment for a new SUD opened July 14, 2025 | REC(2021-012562MAP); PIPE(3711013) | "Zoning map amendment to create a new Special Use District"; open_date 2025-07-14; pipeline "PL Filed" 2025-07-14 |

Stage: **entitlement**. The notice of preparation starts formal EIR review (as for Redwood LIFE and the Santa Clara
station area). Caveat: DataSF lists the ENV record "On Hold" and no Draft EIR is on CEQAnet; the reason isn't
given. If Matthew wants that read as a halt, `paused` would be the alternative; I don't recommend it on one status
field.

Boundary: DataSF Parcels, blklot 3711005–3711014 and 3711019 (NOP). Union 151,448 sq ft (NOP 151,390). Accuracy:
official.

Massing (`pipeline/bam_pipeline/sites/massing_77_beale.py`): the NOP's own maximum envelopes, in the
"justified on Mission Street" position (the one Figure 6 draws in 3D): base 125 ft over the Tower Location Zone
(block width by 229'-3" from Mission), lower tower 230 x 135 ft to 679 ft, upper tower 210 x 135 ft to 1,225 ft,
centred between Beale and Main as the figure's plan shows. **Design choice for Matthew:** the tower's position isn't
set (Mission, Main or Beale), so this is one of three; alternatives are boundary only, or a faint 1,225-ft envelope
over the whole zone (the map's `podium_ft` envelope style). The 75-ft crown, the kept buildings and the 400-ft
variant aren't drawn. Illustrative; stage `entitlement`.

Press-only: none needed (Hines is named in the NOP).

Open items: the tower's position and design; whether 1,225 ft includes the crown; why the ENV record is on hold;
homes (44–120 for certain, up to 437 with the variant); whether the Jan 7 scoping meeting took place.

---

## 536-mission

Recommendation: **INCLUDE** (stage `entitled`). The Golden Gate University site; approved by the Planning
Commission on Sept 10, 2026 in two variants. Next to Oceanwide Center (across Ecker Place), no overlap.

Documents read:
- AG260910 (items 5a–5c, p. 4).
- `https://sfplanning.org/environmental-review-documents?title=536%20Mission` (lists a General Plan Evaluation and
  MMRP, 08/20/2026; documents on the blocked host).
- `https://sfplanning.org/resource/planning-commission-hearing-packet-september-10-2026` (links only to the blocked
  packet `2025-007507DNXOFASHD.pdf` and presentation).
- DataSF: PRJ(2025-007507PRJ) and children (DNX, ENV, HRR, OFA, SHD, TDM, VAR); PIPE(3708098); all Planning records
  and permits on 3708/098; parcels on block 3708. CEQAnet: nothing filed (SF documents 2025–26 scanned by type).

| field | official value | source | verbatim quote |
|---|---|---|---|
| site | Block 3708 Lot 098, north side of Mission between Anthony and Ecker | AG260910 p.4 | "536 MISSION STREET – north side between Anthony and Ecker Streets; Lot 098 in Assessor's Block 3708 (District 6)" |
| approved variants | 700 ft, ~1.22 million sq ft office/lab; or 649 ft, ~991,000 sq ft with up to 385 units | AG260910 p.4 | "construct one of the following tower variants: 1) a 700-foot-tall, approximately 1.22 million square foot building with retail, office, and laboratory uses; or 2) a 649-foot-tall, approximately 991,000 square foot building with retail, office, and residential uses (up to 385 dwelling units) within a C-3-O(SD) (Downtown-Office (Special Development)) Zoning District and 700-S-2 Height and Bulk District" |
| stories, parapet, GSF | 46 stories; 752 ft and 698 ft to parapet; 1,357,551 / 1,181,781 gsf; 370 units | REC(2025-007507DNX) | "proposes 46-stories development with two variants. The first is a 700-foot-tall (752 feet to the top of the parapet), 1,357,551 GSF office building (the "Office Variant"). The second variant is a 650-foot-tall (698 feet to top of the parapet), 1,181,781 GSF building that would include a mix of office and 370 residential dwelling units" (PRJ record: 1,354,395 / 1,171,937 GSF and 385 units) |
| existing | 7-story, 236,680 sq ft GGU building, demolished | PRJ(2025-007507PRJ) | "The project will demolish the existing seven-story, 236,680 square foot Golden Gate University building (Institutional Use)" |
| approvals requested | DNX with exceptions; office allocation up to 555,390 sq ft; shadow findings | AG260910 p.4 | "Request for Downtown Project Authorization with exceptions"; "Request for Office Development Authorization ... to establish up to 555,390 square feet of new office use"; "Request for adoption of Shadow Findings" |
| approval | Approved Sept 10, 2026; DNX, OFA, SHD closed approved Sept 24, 2026 | PRJ(2025-007507PRJ); REC(…DNX/OFA/SHD) | "project_decision": "Approved", "project_decision_date": "2026-09-10"; "record_status": "Closed - Approved", "close_date": "2026-09-24" |
| CEQA | general plan evaluation; ENV closed July 16, 2026 | AG260910 p.4; REC(2025-007507ENV) | "The Planning Department issued a general plan evaluation pursuant to the California Environmental Quality Act (CEQA)."; "Closed - CEQA Clearance Issued", close_date 2026-07-16 (the PRJ record says "Community Plan Evaluation", 12/17/2025) |
| variance | Jessie Street parking/loading entrances, under review | REC(2025-007507VAR) | "Variances pursuant to Planning Code Sections 145.1(c)(2) and 155(s)(4)(A) are sought for the Office Variant and the Mixed-Use Variant"; "The Project's Jessie Street frontage is 185 feet"; "record_status": "Under Review", opened 2026-08-26 |
| filed | Aug 14, 2025 | PRJ(2025-007507PRJ) | "open_date": "2025-08-14" |
| permits | none for the tower | `https://data.sf.gov/resource/i98e-djp9.json?block=3708&lot=098` | only telecom and sprinkler permits (2022–2025) |

Stage: **entitled** (Planning Commission approvals; variance and TDM pending; no permits). Possible appeals to the
Board of Appeals weren't checked (blocked host).

Boundary: DataSF Parcels, blklot 3708098: 33,189 sq ft (0.76 acres) as mapped. Its nearest point to Oceanwide
Center's boundary is 7.6 m (Ecker Place); no overlap. Accuracy: official (the one lot the approvals name).

Massing (`pipeline/bam_pipeline/sites/massing_536_mission.py`): no plan could be opened (packet and CEQA document on
the blocked host), so a labelled placeholder: the whole lot to 700 ft, the office variant's roof (752 ft parapet in
the note; mixed-use variant 649 ft). The gross figures suggest an average floor of roughly 26,500–29,500 sq ft
against the 33,189-sq-ft lot, so the volume overstates the bulk by perhaps a fifth. Illustrative; stage `entitled`.
Worth redrawing from the plans when the packet can be reached
(`https://citypln-m-extnl.sfgov.org/Commissions/CPC/9_10_2026/Commission%20Packet/2025-007507DNXOFASHD.pdf`).

Press-only (kept in `reported`; not opened): developers McCourt Partners and Lincoln Property Company
(`https://www.multifamilydive.com/news/536-mission-high-rise-downtown-san-francisco/831288/`); a search listing also
says Golden Gate University sold the site for $31.6 million (not recorded).

Open items: footprint; which variant; motion numbers, vote and any appeal; floor areas and unit counts differ
between the agenda and Planning's records; lot area.

---

## Leads not added

From the 2026 Q2 pipeline (`6jgi-cpb4`, Northeast and Downtown planning districts) and CEQAnet, in or near the
Financial District, Jackson Square, Chinatown and North Beach:

- **524 & 530 Howard Street** (Block 3721 lots 013/014): 72 stories, ~795 ft (844 ft with rooftop appurtenances),
  672 homes; "PL Approved" 2024-06-18. `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=3721013`. Beside
  Salesforce Park; another group is drawing it (`524-howard` in `official_boundaries.py`).
- **570 Market Street** (0291/013): 29-story, ~300-ft hotel, ~240 rooms, 126,824 gsf; approved 2025-09-11
  (record 2019-017622PRJ, "Closed - Approval Ltr Issued"; CEQAnet NOD 12/23/2025, SCH 2024101396).
  `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2019-017622PRJ`. Below the map's scale; add only if Matthew
  wants mid-size towers.
- **955 Sansome Street** (0143/001, Telegraph Hill/North Beach): 24 stories, 132 homes (26 below market rate),
  13,710 sq ft retail, replacing a garage; application under review (revised Jan 19, 2024).
  `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2023-008196PRJ`. Proposed; small; hold.
- **758 & 772 Pacific Avenue** (0161/014, Chinatown): 15-story, 175 affordable senior homes (CCDC with the City);
  approved 2025-01-24, DBI site permit 202512151804 issued 2026-06-17.
  `https://data.sf.gov/resource/i98e-djp9.json?permit_number=202512151804`. Small; candidate only for an affordable
  housing layer.
- **545 Sansome Street** (0207/035), across Sansome from 530 Sansome: addition to a nine-story historic office
  building, about 52,400 net sq ft, approved 2023-12-14. `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=0207035`.
  Too small.
- **425 Broadway** (0163/002): two 65-ft buildings, 75 homes, approved (Motion 21055, modified under
  2024-005966PRJ). `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=0163002`. Too small.
- Not leads despite large pipeline figures: 301 Mission (penthouse merger), 160 Spear, 500 Howard, 88 Spear, 120
  Stockton, 1 Ferry Building (tenant changes; the pipeline counts the existing building's area).
