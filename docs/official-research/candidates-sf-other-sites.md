# Official-source findings: San Francisco sites outside downtown and Central SoMa

Checked 2026-10-19 for Matthew's request of the same day ("I feel like we are still missing a lot of projects in
San Francisco ... Find all of those and more"). This group covers San Francisco outside the downtown tower and
Central SoMa groups. Documents were downloaded and read in full text with `pdftotext -layout` (local copies in
`data/raw/official/freedom-west/`, `data/raw/official/sf-gateway/` and `data/raw/official/railyards/`, git-ignored),
and DataSF was queried live: development pipeline 2026 Q2 (`6jgi-cpb4`), Planning records (`qvu5-m3a2`,
`y673-d69b`), DBI permits (`i98e-djp9`), parcels (`acdm-wktn`), special use districts (`5yf5-ms5f`) and height
districts (`h9wh-cg3m`). CEQAnet was searched by county and document type (San Francisco NOPs and EIRs, 2019 to
2026). Page numbers are PDF page numbers.

**The Freedom West Draft EIR has no usable text layer.** The CEQAnet copy (Volume 1, 516 pp.) was run through
Acrobat Paper Capture and its Type 3 fonts extract as gibberish; the Planning Department's own copy is on
`citypln-m-extnl.sfgov.org`, which the proxy blocks. Its pages were rendered with `pdftoppm` and read as images, so
quotes from it below are transcribed by eye from the page images. The notice of preparation (Apr 30, 2025) has a
normal text layer.

Hosts: none to add. Every source is on `ceqanet.lci.ca.gov`, `sfplanning.org` or `data.sf.gov`. Documents on blocked
hosts (`citypln-m-extnl.sfgov.org` minutes and packets, `sfbos.org` and `sfgov.legistar.com` Board files) are listed
as leads, not cited.

URL shorthand:
- FW-DEIR = `https://ceqanet.lci.ca.gov/2025050078/2/Attachment/wdfI_L` (Freedom West 2.0 Draft EIR, Volume 1, Case
  No. 2020-006887ENV, Jan 13, 2026, 516 pp., 47 MB; sha256 `0c8b1de5…7869`)
- FW-NOP = `https://ceqanet.lci.ca.gov/2025050078/1/Attachment/SYErkB` (notice of preparation, Apr 30, 2025, 25 pp.)
- FW-PAGE = `https://sfplanning.org/project/freedom-west`
- CPC-yyyymmdd = Planning Commission agendas on `sfplanning.org/sites/default/files/agendas/`:
  CPC-20240725 = `2024-07/20240725_cpc%20%28ID%201450244%29.pdf`, CPC-20260212 = `2026-02/20260212_cpc%20%28ID%201554963%29.pdf`,
  CPC-20260903 = `2026-08/20260903_cpc%20%28ID%201585209%29_0.pdf`, CPC-20250925 = `2025-09/20250925_cpc%20%28ID%201533917%29.pdf`
- GW-DEIR = `https://ceqanet.lci.ca.gov/2022030286/2/Attachment/fYSuZM` (San Francisco Gateway Project Draft EIR, Case
  No. 2015-012491ENV, Aug 2, 2023, 406 pp.; sha256 `1a606783…6e8c`)
- GW-RTC = `https://ceqanet.lci.ca.gov/2022030286/3/Attachment/hJS7Ux` (Responses to Comments, May 2025, 381 pp.)
- GW-NOD1 = `https://ceqanet.lci.ca.gov/2022030286/4/Attachment/k7ZK1B` (notice of determination filed Oct 28, 2025);
  GW-NOD2 = `https://ceqanet.lci.ca.gov/2022030286/5/Attachment/rlRYl2` (filed Dec 17, 2025)
- RY-NOP = `https://ceqanet.lci.ca.gov/2026091295/1/Attachment/tPsmWg` (Railyards notice of preparation, Case No.
  2026-002123ENV, Sept 30, 2026, 32 pp.); RY-NOC = `https://ceqanet.lci.ca.gov/2026091295/1/Attachment/6PpGFT`
- PIPE = `https://data.sf.gov/resource/6jgi-cpb4.json` (development pipeline, 2026 Q2)

## Summary

| project | stage | size (official) | recommendation |
|---|---|---|---|
| `freedom-west` Freedom West 2.0 (710 McAllister St) | entitlement (Draft EIR Jan 2026) | 15 buildings, 85–335 ft, 2,291 homes, 150-room hotel, 3,673,200 gsf, 10.37 acres | **INCLUDE**, boundary + illustrative height envelopes |
| `sf-gateway` San Francisco Gateway (749 Toland St / 2000 McKinnon Ave) | entitled (approved Sept–Dec 2025) | 2 buildings, 97 ft, 1,646,000 gsf enclosed (2,160,000 with roofs), 17.1 acres | **INCLUDE**, boundary + illustrative lot-sized volumes |
| `railyards` Railyards Mixed-Use Development (700 4th St) | entitlement (NOP Sept 30, 2026) | ~7.8M sq ft above grade, 1,765–5,834 homes, towers 350–855 ft, 18.63 acres | **INCLUDE** (found in this pass; not in the 2026 Q2 pipeline), boundary only |
| 11 leads (3333 California, Fort Miley, 11–15 Marina, 850 La Playa, 2190 O'Farrell, 469 Stevenson, Potrero Yard, 555 Beale, Hunters View, 900 7th St, Matson Block) | — | — | not added; see "Leads not added" |

The Railyards was not on the brief's list. It came up in the CEQAnet search of San Francisco NOPs. It sits between
the Central SoMa and Mission Bay areas; if the Central SoMa group also picked it up, keep one record.

---

## freedom-west

Recommendation: **INCLUDE** (stage `entitlement`). A 10.37-acre, two-block rebuild of the 1970s Freedom West housing
co-op with 2,291 homes and buildings up to 335 ft, well over the 1,000-home bar. The pipeline's own record for the
project (2023-007911PRX, "Tracking record for non-Planning project Freedom West") points to Planning case
2020-006887.

Documents read:
- FW-DEIR: cover (p. 7), contents and lists of figures and tables (pp. 9–16), Chapter 2 pp. 127–131, 143–152, 163–164,
  168, Chapter 4 p. 431 (read as page images).
- FW-NOP (all 25 pp., text layer).
- FW-PAGE (project page, milestones table); CPC-20240725 item 9, CPC-20260212 item 9, CPC-20260903 items 9a and 9b;
  CPC agendas of Sept 10, 17 and 24, Oct 1 and 8, 2026 (no Freedom West item).
- CEQAnet `https://ceqanet.lci.ca.gov/Project/2025050078`, `/2025050078/1`, `/2025050078/2`.
- DataSF: Planning records 2020-006887 (PRJ and children ENV, DVA, GPA, MAP, PCA, SHD, TDM, PPA), 2024-003742PRJ,
  2024-008030SUB; pipeline 2023-007911PRX; parcels on blocks 0770 and 0783.

| field | official value | source | verbatim quote |
|---|---|---|---|
| site, lots | 10.37 acres, Block 0783 Lots 023–025 and Block 0770 Lot 027, bounded by Golden Gate, Gough, Fulton and Laguna | FW-DEIR p. 127 (p. 2-1); FW-NOP p. 1 | "The Freedom West 2.0 (proposed project) site encompasses 10.37 acres on Assessor's Block 0783, Lots 023, 024, and 025, and Assessor's Block 0770, Lot 027, in San Francisco's Western Addition neighborhood."; NOP: "Lot Size: 451,500 square feet (10.37 acres)" |
| exclusions | church, 967-973 Golden Gate, part of Building 17 (870-880 McAllister) | FW-DEIR p. 127 | "The project site encompasses the majority of the two blocks, with the exception of the Bethel African Methodist Episcopal (A.M.E.) Church (916 Laguna Street), a multifamily residential building (967-973 Golden Gate Avenue), and a portion of one of the existing Freedom West residential buildings (Building 17 at 870-880 McAllister Street at the northeast corner of the McAllister Street and Laguna Street intersection)" |
| existing | 22 buildings, 358 co-op homes on site (382 incl. Building 17) | FW-DEIR p. 127 | "The project site is currently developed with 22 buildings—20 two- to three-story residential buildings that contain 358 cooperative (co-op) housing units and two multipurpose buildings, all owned by the Freedom West Homes Corporation. There are 382 existing co-op housing units in the 20 residential buildings, including 870-880 McAllister ("Building 17")." |
| sponsor | MacFarlane Partners, engaged by the co-op | FW-DEIR p. 127; CPC-20260903 p. 3 | "Freedom West Homes Corporation and its shareholders—the occupants of the co-op housing units—have engaged MacFarlane Partners, the project sponsor"; agenda: "The project sponsor, MacFarlane Development Company LLC" |
| replacement homes | 267 co-op homes; 115 more in a separate building at 870-880 McAllister | FW-DEIR p. 127 | "The proposed project would replace 267 of the 382 co-op housing units. An off-site 115-unit affordable housing project at 870-880 McAllister Street, subject to a separate ministerial process (Planning Department Case No. 2024-003742PRJ), would cover the difference" |
| buildings, stories, heights | 15 buildings, 8 to 32 stories, 85 to 335 ft | FW-DEIR p. 130 (Table 2-1) | "Number of Building(s) 22 15 7"; "Building Stories 1 to 3 stories 8 to 32 stories"; "Maximum Building Height (feet) 10 to 35 feet 85 to 335 feet" |
| homes | 2,291 (267 co-op + 2,024 additional) | FW-DEIR p. 130 (Table 2-1) | "Residential Uses 364,536 gsf / 358 housing units 2,614,700 gsf / 2,291 housing units"; "Cooperative Housing Units 362,800 gsf / 267 housing units"; "Additional Residential Housing Units – 2,251,900 gsf / 2,024 housing units" |
| other uses | commercial 68,600 gsf, CIE 14,800 gsf, hotel 108,000 gsf / 150 rooms, parking 867,000 gsf / 1,640 spaces | FW-DEIR p. 130 | "Commercial / CIE Uses – 68,600 / 14,800 gsf"; "Hotel Use – 108,000 gsf / 150 hotel rooms"; "Approximately 867,000 gsf / 1,640 spaces" |
| open space | 1.28 acres of POPOS at grade (NOP: 1.89) | FW-DEIR p. 130; FW-NOP p. 12 | "Privately Owned Public Open Space (At-Grade) – 1.28 acres"; NOP Table 1: "1.89 acres" |
| total | 3,673,200 gsf | FW-DEIR p. 131 (p. 2-5) | "Overall, the proposed project would construct approximately 3,673,200 gross square feet of mixed-use development, comprised of 2,614,700 gross square feet of residential floor area with 2,291 total residential dwelling units" |
| zoning change | RTO and 40-X/50-X to a new SUD with 85–335 ft limits; six tower locations | FW-DEIR p. 143 (p. 2-17) | "The existing height limits of 40 to 50 feet would be modified to allow heights ranging from 85 to 335 feet ... Most of the proposed project would be subject to an 85-foot height limit, with the exception of six proposed tower locations distributed throughout the project site, where height limits would be further increased to accommodate proposed heights ranging from 105 to 335 feet." |
| design status | designs not final | FW-DEIR p. 146 (p. 2-20) | "Although the building designs have not been finalized, the building characteristics and land uses for each locational prefix at maximum buildout are summarized in Table 2-2" |
| heights by parcel | 85-X most; 185-X NE-D; 165-X SW-A, SW-F; 335-X SE-A; 105-X SE-C; 225-X SE-D; OS Octavia Green | FW-DEIR p. 145 (Figure 2-8); p. 148 (Figure 2-10) | map labels "185-X", "165-X", "335-X", "105-X", "225-X", "85-X", "OS"; Figure 2-10 labels "SE-A 335 ft", "SE-D 225 ft", "NE-D 185 ft", "SW-F 165 ft", "SW-A 165 ft", "SE-C HOTEL 105 ft", "NW-CO-OP 85 ft" |
| homes by building | NW-CO-OP 267, NE-A 133, NE-B 176, NE-C 135, NE-D 224, SW-A 166, SW-B 74, SW-C 72, SW-D 74, SW-E 81, SW-F 140, SE-A 311, SE-B 151, SE-C 150 hotel rooms, SE-D 287 | FW-DEIR p. 151 (Table 2-2, rotated) | "Residential Units / Hotel Rooms 267 133 176 135 224 166 74 72 74 81 140 311 151 150 287 ... 2,291/150" |
| hotel | SE-C, 105 ft, 150 rooms | FW-DEIR p. 150 (p. 2-24) | "Building SE-C would be a 105-foot-tall, 108,000-gross-square-foot, 150-room hotel, with an additional 2,000 gross square feet of ground-floor commercial uses." |
| CIE | innovation center, community event space, childcare | FW-DEIR p. 150 | "Building NW-CO-OP would contain the 6,000-gross-square-foot Innovation Center"; "the 5,400-gross-square-foot community event space"; "A 3,400-gross-square-foot childcare center would be located on the ground floor of Building NE-A" |
| schedule | late 2026 to early 2034; phases 1A–3B | FW-DEIR pp. 163–164 (Table 2-3) | "The preliminary construction schedule assumes late 2026 as the start of construction and early 2034 as the end of construction"; "Phase 1A (2026–2029) Building NW-CO-OP" ... "Phase 3B (2030–2034) Building SE-A Building SE-C" |
| variant | hotel could go on SE-A instead | FW-DEIR p. 431 (p. 4-1) | "would allow for up to 150 hotel rooms to be located on parcel SE-A or parcel SE-C, as opposed to only on parcel SE-C as assumed under the proposed project" |
| approvals needed | DA, GP/Planning Code/zoning map amendments, SUD | FW-DEIR p. 168 (p. 2-42) | "Approval of a Development Agreement"; "Approval of amendments to the San Francisco General Plan, San Francisco Planning Code, zoning map, and height and bulk map" |
| DEIR dates | published Jan 13, 2026; hearing Feb 12; comments to Feb 27, 2026 | FW-DEIR p. 7 (cover); CPC-20260212 item 9 | "Draft EIR Publication Date: January 13, 2026"; "Draft EIR Public Hearing Date: February 12, 2026"; "Draft EIR Public Comment Period: January 13, 2026–February 27, 2026"; agenda: "Public Hearing on the Draft Environmental Impact Report" |
| NOP | Apr 30, 2025; scoping May 21, 2025 | FW-NOP p. 1–2 | "Date: April 30, 2025"; "An in-person public scoping meeting ... will be held from 5:30 p.m. on May 21, 2025" |
| co-op history | built 1973–1975 with HUD subsidy, sponsored by Bethel A.M.E. | FW-NOP p. 6 | "the U.S. Department of Housing and Urban Development subsidized the construction of Freedom West"; "Construction of the co-op occurred in two separately funded phases from 1973 to 1975." |
| NOP affordability (superseded) | 133 affordable in NE-A, 1,891 market-rate | FW-NOP pp. 5, 16 | "(267 co-op housing units, 133 affordable units, and approximately 1,891 market-rate units)"; "Building NE-A would have 133 affordable housing units" |
| 2024 hearing | informational presentation, "10.8-acre site" | CPC-20240725 item 9 | "Informational Presentation on the Freedom West Development Project ... The 10.8-acre site is bounded by Golden Gate Avenue to the north, Fulton Street to the south, Laguna Street to the west and Gough Street to the east" |
| 2026 hearing | update and GPA initiation; "up to 2,393 units" | CPC-20260903 items 9a, 9b | "The proposed 10.73-acre project is a mixed-use, multi-phased master-planned development"; "including up to 2,393 units including the replacement of 267 cooperative housing units, the option for a 150-room hotel"; "Preliminary Recommendation: Initiate and schedule a public hearing on or after October 8, 2026" |
| records | PRJ opened 2020-07-24; DVA, GPA, MAP, PCA opened 2026-05-05 | `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2020-006887PRJ`, `y673-d69b` | "open_date": "2020-07-24", "applicant_org": "MacFarlane Partners"; DVA "record_status": "Pending Review", "open_date": "2026-05-05" |
| pipeline | 2,537 units, 191,400 gsf non-residential | PIPE (`case_no=2023-007911PRX`) | "proposed_units": "2537", "non_residential_total_gsf": "191400", "description_planning": "Tracking record for non-Planning project Freedom West" |

Stage reasoning: **entitlement**. The Draft EIR is out and the rezoning, General Plan amendments and development
agreement are in review; nothing is approved. Whether the Commission initiated the General Plan amendments on Sept
3, 2026 couldn't be checked (minutes on a blocked host), and no adoption hearing appears on the Sept 10 – Oct 8, 2026
agendas; Oct 22 and 29 are cancelled. Planning's page lists the Responses to Comments as "Upcoming – Materials not yet
available".

Homes shown: 2,291, from the Draft EIR, the newest document with a full program. Three other figures exist: 2,393
(Planning's project page and the Sept 3, 2026 agenda, "up to"), 2,387 (the Planning PRJ record) and 2,537 (pipeline).
None explains its count; all are in `verify`.

Boundary: DataSF parcels, the four lots named in the NOP, Draft EIR and agendas; **approximate**, 10.8 acres as
drawn against 10.37. Lot 0770/027 still includes the 870-880 McAllister corner. Planning approved a two-lot
subdivision for it in 2024 (2024-008030SUB, "Lot 1 will contain 115 Residential and 2 Commercial Mixed Used New
Condominium units"), but the parcel layer hasn't split it yet. Its area (about 0.43 acres) explains the difference.

Massing (`massing_freedom_west.py`): Figure 2-9 (1:1,800, raster) rendered at 250 dpi. Its dashed site outline and
parcel lines were read off the render and snapped to the darkest pixel column or row within 4 px. The block between
McAllister and Fulton (all of Block 0783) and the two Gough Street corners of lot 0770/027 were fitted to the DataSF
parcel corners. The fit is 0.6387 ft/px, rotated 9.46°, RMS 0.10 m over 6 points, worst residual 0.19 m. The 15
parcels are drawn whole at their Figure 2-8 height limits, which match the Figure 2-10 labels. Parcel areas are
17,300–67,800 sq ft; the 15 total 401,112 sq ft, and with Octavia Green they come to about 450,000 sq ft against the
DEIR's 451,500. These are envelopes, illustrative, all `proposed`, with Table 2-3 phases. They overstate bulk: Figure
2-10 shows courtyards and podiums, and Table 2-2's floor areas imply towers smaller than their parcels (SE-A: 436,000
gsf over up to 32 floors on a 23,500 sq ft parcel). Option for Matthew: redraw towers as podium plus tower once the
design standards and guidelines (draft 3, Oct 2025, cited in the DEIR p. 2-17) are public.

Press-only facts: none used.

Open items: the home count (above); affordability of the 2,024 new homes; the GPA initiation vote; the DSG; the DEIR's
Volume 2 appendices (141 MB) weren't opened.

---

## sf-gateway

Recommendation: **INCLUDE** (stage `entitled`). Two very large multi-story industrial (PDR) buildings, 1.65 million
gsf of enclosed floor area (2.16 million with active roofs), approved in 2025. It clears the ~1M sq ft bar. The
pipeline's 1,091,790 gsf and "four buildings" are the 2015 application's design; the EIR, the approvals and the NODs
describe the approved two-building project.

Documents read:
- GW-DEIR: contents, Chapter 2 (pp. 81–117: site, Table 2.D-1, figures 2.D-1 to 2.D-8, Table 2.D-3).
- GW-RTC: cover memo (p. 3), contents, Section 9.B.1 (massing), Chapter 10 revisions (p. 175).
- GW-NOD1 and GW-NOD2 (3 pp. each); CPC-20250925 items 14 and 15a–15e.
- CEQAnet `https://ceqanet.lci.ca.gov/Project/2022030286` and document pages 1–5.
- DataSF: Planning records 2015-012491 (PRJ, CUA, CWP, DVA, ENV, MAP, PCA, PPA); DBI permits on 5284A/008 and
  5287/002 since 2019; SUD layer ("San Francisco Gateway SUD"); height layer at the site ("97-X").

| field | official value | source | verbatim quote |
|---|---|---|---|
| site | 743,800 sq ft (17.1 acres): 5284A/008 and 5287/002 plus streets | GW-DEIR p. 83 (p. 2-3) | "the approximately 743,800-gross-square-foot (17.1 gross total acres), rectangular project site ... consists of assessor's block 5284A, lot 008, and block 5287, lot 002, which are occupied by four structures totaling approximately 448,000 square feet of PDR space, as well as portions of the surrounding streets and Selby Street" |
| I-280 | viaduct crosses the site over Selby Street | GW-DEIR p. 83 | "An elevated portion of Interstate 280 (I-280) bisects the project site, running in a north-south direction above the existing Selby Street right-of-way" |
| sponsor | Prologis, L.P. | GW-DEIR p. 81; GW-NOD1 p. 1 | "The project sponsor, Prologis, L.P., proposes to redevelop two parcels in a core industrial area of the city."; "Project Applicant: Courtney Bell, Prologis, L.P." |
| buildings, height | two three-story buildings plus active roof, 97 ft (115 ft with appurtenances) | GW-DEIR p. 90 (p. 2-10) | "construct two new three-story buildings (plus active roof), totaling approximately 2,160,000 gross square feet. Each building would have a maximum height of approximately 97 feet (115 feet with rooftop appurtenances included)." |
| per building | PDR 583,400, yard 72,900, circulation 147,750, parking 271,750, retail 4,200; 1,080,000 each | GW-DEIR p. 91 (Table 2.D-1) | "PDR (and other permitted) Uses 583,400 583,400 1,166,800"; "Retail 4,200 4,200 8,400"; "Total 1,080,000 1,080,000 2,160,000" |
| floor area (approved) | 1,646,000 gsf enclosed; 514,000 active roof | GW-RTC p. 175 (10.B); GW-NOD1 p. 2 | "totaling approximately 1,646,000 gross square feet of enclosed floor area, or 2,160,000 gross square feet including 514,000 square feet of active roofs"; NOD: "The two three-story buildings would total approximately 1,646,000 gross square feet of enclosed floor area, or 2,160,000 gross square feet including active roofs." |
| approved program | up to 1,637,600 sq ft PDR etc., 8,400 retail, 1,125 parking; lot line adjustment dedicating ~3.9 acres | CPC-20250925 p. 7 (item 15e) | "the construction of two mixed-use buildings up to 97 feet in height totaling 1,646,000 gross square feet in size with a mix of uses including up to 1,637,600 square feet of Production, Distribution, and Repair (PDR) and approximately 8,400 square feet of Retail Sales and Service Use, a total of up to 1,125 off-street parking spaces"; "the lot line adjustment of existing property lines to dedicate approximately 3.9 acres of property to the City" |
| SUD, height | new SUD; HT10 from 65-J to 97-X | CPC-20250925 p. 6 (item 15b) | "to create the San Francisco Gateway Special Use District (SUD) ... a Zoning Map Amendment to Zoning Maps SU10 to illustrate the San Francisco Gateway SUD and HT10 to change the Height and Bulk Zoning District from 65-J to 97-X" |
| approvals | FEIR certified and CUA approved Sept 25, 2025; final Oct 28, 2025 | GW-NOD1 p. 2 | "The San Francisco Planning Commission certified the final EIR on September 25, 2025; the first approval of the project also occurred on September 25, 2025 when the Planning Commission approved the conditional use authorization for the project. The project was officially approved on October 28, 2025 when no appeal of the FEIR was filed." |
| ordinances | SUD (File 250426) and DA (File 250427) in effect Dec 12, 2025 | GW-NOD2 p. 2 | "decided to carry out or approve the project on December 12, 2025 when the ordinances for the San Francisco Gateway Special Use District (Board File 250426) and also one approving the development agreement between the City and County of San Francisco and Prologis, L.P. (Board File 250427) went into effect" |
| zoning layers | SUD and 97-X mapped | `https://data.sf.gov/d/5yf5-ms5f`; `https://data.sf.gov/d/h9wh-cg3m` | SUD "name": "San Francisco Gateway SUD"; height at (-122.397, 37.7412): "height": "97-X" |
| DEIR, RTC dates | DEIR Aug 2, 2023; comments to Oct 16, 2023; RTC memo May 7, 2025 | GW-RTC pp. 1–3 | "Draft EIR Publication Date: August 2, 2023"; "Draft EIR Public Comment Period: August 3, 2023 – October 16, 2023"; "Date: May 7, 2025" |
| NOP | Mar 9, 2022 | CEQAnet `/2022030286/1` | "NOP - Notice of Preparation of a Draft EIR Received 3/9/2022" |
| application | PRJ opened 2015-09-18; decision Approved 2025-09-25 | `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2015-012491PRJ` | "open_date": "2015-09-18", "project_decision": "Approved", "project_decision_date": "2025-09-25" |
| construction | 31 months; Building A ~4 months ahead of B | GW-DEIR p. 117 (Table 2.D-3) | "Construction duration would total 31 months"; "the start of construction for building A would be approximately 4 months before the start of construction for building B" |
| current use | parcel delivery in two buildings since Aug 2020 | GW-DEIR p. 81 | "Beginning in August 2020, parcel delivery service now occupies two buildings at the project site." |
| no new-building permit | only tenant and accessibility permits on both lots since 2019 | `https://data.sf.gov/resource/i98e-djp9.json?block=5287&lot=002`, `...block=5284A&lot=008` | — (absence, checked 2026-10-19) |

Stage reasoning: **entitled**. All approvals are in hand (CUA, FEIR, SUD, height map, DA); no demolition or
building permit for the new buildings in DBI's records.

Boundary: the San Francisco Gateway SUD from DataSF's zoning layer, **official**. It measures 17.2 acres
(749,029 sq ft) against the 743,800 sq ft site, which includes Selby Street and parts of the surrounding streets. The
two DataSF lots alone are 13.3 acres.

Massing (`massing_sf_gateway.py`): each building drawn over its whole lot at 97 ft, illustrative, `entitled`. Lots are
about 607 x 489 ft and 596 x 489 ft (Building A 292,962 sq ft, B 287,423 sq ft). The Level 1 plan (Figure 2.D-3,
p. 94) dimensions the PDR floor at 576 ft across, and the site plan (Figure 2.D-1, p. 92) shows each building nearly
filling its lot, with rounded ramp corners on McKinnon Avenue. Figure 2.D-1 is a raster with no lot lines, and its
"extent of project scope of work" outline doesn't match the SUD (its proportions are about 2.05:1 against the SUD's
2.35:1), so the building outlines weren't traced. A traced footprint would need a georeference from street
centrelines. The lots are about 600 ft long against the plan's 576-ft floor, so the volumes are slightly too big.

Press-only facts: none used.

Open items: Commission motion numbers and votes (minutes blocked); DA benefits; DSG footprints; tenants; the stale
pipeline description.

---

## railyards

Superseded (2026-10-22): the same project reached the map on Oct 21 as `sf-railyards`
(`candidates-4th-king-railyards.md`), with massing, so this record wasn't added. The findings below agree with it.

Recommendation: **INCLUDE** (stage `entitlement`), boundary only. A ~7.8 million sq ft, 18.6-acre redevelopment of
the Caltrain terminal and railyard at Fourth and King with towers of 350–855 ft (the 855 ft limit is on Block 1 at
Fourth and King). It clears every bar (homes, sq ft, tower height). Filed Mar 11, 2026, so it isn't in the 2026 Q2
pipeline.

Documents read: RY-NOP (all 32 pp., text layer; Figure 3, p. 13, read as an image), RY-NOC, CEQAnet
`https://ceqanet.lci.ca.gov/2026091295/1`; DataSF Planning records 2026-002123 (PRJ, ENV, DVA); parcels for the four
lots; pipeline (no rows for these lots).

| field | official value | source | verbatim quote |
|---|---|---|---|
| lots, area | 8701/003, 8701/004, 8700/001, 8703/005; 18.63 acres | RY-NOP p. 1 | "Blocks/Lot Nos.: 8701/003, 8701/004, 8700/001, and 8703/005"; "Site Area: 18.63 acres" |
| sponsor | Prologis 4th & King LLC, with Caltrain | RY-NOP p. 2 | "The project sponsor (Prologis 4th & King LLC), in coordination with the Peninsula Corridor Joint Powers Board/Caltrain, proposes to develop the 18.63-acre project site" |
| site | Caltrain station and railyard between Townsend, Fourth, King and Seventh | RY-NOP p. 2 | "which currently includes the existing San Francisco Caltrain Station at Fourth and King streets (Caltrain Station), and railroad tracks, platforms, and maintenance equipment (the Railyard). This project site is generally bounded by Townsend Street to the north, Fourth Street to the east, King Street to the south, and Seventh Street to the west" |
| program (two scenarios) | 7,820,390–7,839,210 sq ft; 1,765 homes + 5,638,120 commercial + 172,660 retail, or 5,834 homes + 1,589,980 commercial + 159,970 retail | RY-NOP p. 2; Tables 1–2 pp. 8–10 | "would range from 7,820,390 square feet (Maximum Commercial Scenario) to 7,839,210 square feet (Maximum Residential Scenario). The Maximum Commercial Scenario proposes the development of up to 1,765 residential units ... along with up to approximately 5,638,120 square feet of commercial space and up to approximately 172,660 square feet of retail space. The other proposed project scenario, the Maximum Residential Scenario, proposes the development of up to 5,834 residential units" |
| commercial defined | office, hotel, lab, life science | RY-NOP p. 8, note 7 | "“Commercial Uses” includes general office, hotel, laboratory, life science, and other uses." |
| station | 19,560 sq ft station hall on Block 1; tunnel and station ~60 ft below grade | RY-NOP p. 2 | "the new 19,560-square-foot Caltrain Station Hall would be located in Block 1"; "construct a new Caltrain tunnel (Caltrain Tunnel) with two below-grade railroad tracks and one service platform, terminating at a new, reconfigured Caltrain Station below the project site. The Caltrain Station would be approximately 60 feet below grade." |
| heights | 350–855 ft; eastern parcels 400–855, western 350–450 | RY-NOP pp. 4, 7; Figure 3 p. 13 | "The proposed rezoning would modify the existing height limits to between 350 and 855 feet across the project site."; "The existing onsite height limit of 110 feet on the Eastern Parcels would be modified to allow heights ranging from 400 feet to 855 feet ... on the Western Parcels would be modified to allow heights ranging from 350 feet to 450 feet."; Figure 3: "MAX 855' FOR BLOCK 1 / MAX 575' FOR SECOND TOWER", block labels "Max 625' 2B", "Max 500' 2A", "Max 500' 3A", "Max 400' 3B", "Max 550' 3C", "Max 350' 4", "Max 450' 5" |
| open space | 3.73 acres (4.3 At-Grade Rail Variant, 3.5 Fifth Street Variant) | RY-NOP p. 4 | "approximately 3.73 acres of publicly accessible open space (or 4.3 acres under the At-Grade Rail Variant and 3.5 acres under the Fifth Street Variant)" |
| schedule | ~13 years, 2029–2042; tunnel phase after The Portal | RY-NOP pp. 4, 6 | "The EIR will analyze a construction period assumption of approximately 13 years, from 2029 to 2042."; "Rail Infrastructure Phase B must occur after the Portal Project has been constructed." |
| NOP dates | Sept 30, 2026; scoping Oct 14; comments to Oct 30, 2026 | RY-NOP p. 1 | "Date: September 30, 2026"; "Comment Deadline: October 30, 2026"; "An in-person public scoping meeting will be held at 5:30 p.m. on October 14, 2026" |
| zoning now | MB-O / 110 (eastern); Mission Bay North public facility, HZ-1b (western) | RY-NOP p. 6 | "Block/Lots 8700/001 and 8703/005, referred to as the Western Parcels, are within the Mission Bay North Redevelopment Plan and Mission Bay North Public Facility District and Height Zone HZ-1b ... Block/Lots 8701/003 and 8701/004, referred to as the Eastern Parcels, are within the MB-O (Mission Bay Office) Use District and 110 Height and Bulk District." |
| records | PRJ 2026-03-11; ENV 2026-03-16; DVA 2026-04-15 | `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2026-002123PRJ`; `y673-d69b` | "project_name": "RAILYARDS PROJECT - 700 4TH STREET", "description": "... up to 7.8 million square feet of vertical development above grade ... would be subject to a development agreement with the city." |

Stage reasoning: **entitlement**. The NOP has been issued, so the EIR is formally under way, and a development
agreement application is in. No approvals.

Boundary: DataSF parcels for the four lots, **official**, 18.6 acres. The site overlaps the mapped `mission-bay`
boundary (7.9 acres, the western parcels in Mission Bay North) and `the-portal` (9.3 acres, its Townsend alignment
and station area).

Massing: none. The NOP gives height limits by block, not buildings; an 855-ft envelope over a whole block would
mislead. Add towers when the Draft EIR or design standards show building footprints.

Open items: preferred scenario; affordability; offsite maintenance facility site; Caltrain–Prologis agreement.

---

## Leads not added

Pipeline query: PIPE where `proposed_units >= 300 OR non_residential_total_gsf >= 300000` (57 rows), checked against
the map's ids and the other groups' lists.

| lead | size | stage | official URL | recommendation |
|---|---|---|---|---|
| 3333 California St (Laurel Heights) | 744 homes, 49,161 gsf non-res. | entitled (pipeline "PL Approved"); DBI site permits for four buildings filed Feb–Jun 2026, not issued; demolition permit filed Aug 26, 2026 | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2023-007909PRX`; `https://data.sf.gov/resource/i98e-djp9.json?block=1032&lot=003` | Not added: under 1,000 homes and not under construction. Watch for permit issuance. |
| SFVAMC Fort Miley (VA campus) | 1,139,700 gsf medical | pipeline "PL Filed" tracking record for "SFVAMC Fort Miley Campus Alternative 1 Construction 2013-2020" | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2025-009409PRX` | Exclude: a federal campus program from 2013–2020 with no City approval; no federal document opened (`va.gov` not tried as the record gives no link). |
| 11 & 15 Marina Blvd | 790 homes, 63,220 sq ft grocery/retail | "PL Filed" Feb 18, 2026 (2025-011405PRJ), state density bonus, 40-X | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2025-011405PRJ` | Not added: under the bar. |
| 850 La Playa (Outer Richmond) | 562 homes, 65,000 sq ft grocery | "PL Filed" May 28, 2026 (2026-003935PRJ) | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2026-003935PRJ` | Not added: under the bar. |
| 2190 O'Farrell St (Kaiser replacement hospital) | hospital 694,012 sf GFA, ~266 ft, 14 floors; garage 534,274 sf, 1,003 spaces | "PL Filed" June 10, 2026 (2026-004681PRJ); no CEQA document yet | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2026-004681PRJ` | Hold: about 1.23M sf with the garage, so borderline on sq ft; revisit when the CEQA document is out. Matthew's call on hospital campuses. |
| 469 Stevenson St | 27 stories, 274 ft (284 with mechanical), 495 homes | "PL Approved" Apr 20, 2023 (2017-014833PRJ); EIR SCH 2019100093; no DBI permits on 3704/045 since 2018 | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2017-014833PRJ` | Not added: under every bar. |
| SFMTA Potrero Yard (2500 Mariposa) | 513 affordable homes over a bus facility; ~150 ft; 1,243,000 sq ft total (708,000 public facility) | Planning approval Jan 11, 2024 (pipeline); bus facility permit 202411084679 filed; demolition permit 202608196855 filed Sept 8, 2026; asbestos removal permit 202608257106 issued Oct 7, 2026 | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2019-021884PRJ`; `https://data.sf.gov/resource/i98e-djp9.json?block=3971&lot=001` | Previously excluded (`docs/upkeep/leads-2026-10-17.md`). Note: on Planning's figures it totals 1.24M sq ft, and site work permits are starting; still one building, mostly a bus garage. Matthew's call. |
| 555 Beale / Seawall Lot 330 | 568 homes; 23 stories / 230 ft and 10 stories / 105 ft; a separate parcel (T3) for 100% affordable housing not in the application | "PL Filed" (status date May 19, 2026; 2025-011323PRJ, SB 423) | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2025-011323PRJ` | Still dropped (`_meta.dropped`): unchanged since the earlier note, under the bar. |
| HOPE SF Hunters View | 741 homes in the pipeline ("construct about 668 affordable units" in 66 buildings, 2–5 stories); 404 completed | "PL Approved" (2007.0168PRX), partly built | `https://data.sf.gov/resource/6jgi-cpb4.json?case_no=2007.0168PRX` | Not added: under 1,000 homes (the two mapped HOPE SF sites are ~1,700 each). |
| Amazon 900 7th Street | ~710,000 sq ft parcel delivery building, 6.23 acres | NOP Feb 4, 2026 (SCH 2026020145); pipeline lists 650,000 gsf | `https://ceqanet.lci.ca.gov/2026020145/1` | Not added: under 1M sq ft. |
| Matson Block (77 Beale / 50 Main) | tower up to 1,225 ft, ~2.4M gsf | NOP Dec 17, 2025 (SCH 2025120794) | `https://ceqanet.lci.ca.gov/2025120794/1` | In the downtown group's list (77 Beale); not researched here. |

Also seen and not leads: 101 Font Blvd (471 homes, permit filed) and 55 Chumasero Dr (313 homes) are within the mapped
Parkmerced site; UC Law SF's 201
Golden Gate Avenue building is 153 ft (NOD Sept 23, 2024, SCH 2023060025); St. Ignatius (2001 37th Ave) is a
182,850 sq ft school addition. No other pipeline project in the Bayview, the Mission, the Sunset or the Richmond reaches
500 homes or 500,000 gsf. The 300–499-home projects outside downtown and SoMa are 3350 Mission St (379 homes, filed
2026, Bernal Heights), 1101-1123 Sutter St (303, under construction, Nob Hill) and 151 Humboldt St (348, permit filed,
on a lot inside the mapped Potrero Power Station site).
