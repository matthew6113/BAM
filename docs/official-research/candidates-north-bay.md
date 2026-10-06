# Official-source findings: north-bay candidates (Mare Island, Sonoma Developmental Center)

Checked 2026-10-05 against documents downloaded and read in full text (local copies in `data/raw/official/mare-island/` and `data/raw/official/sdc/`, git-ignored). Page numbers are PDF page numbers.

Both are candidates for new records; neither is on the map yet. Draft records:
`scratchpad/records/candidates/mare-island.json` and `sonoma-developmental-center.json`.

URL shorthand:
- VJO = `https://www.cityofvallejo.net/common/pages/GetFile.ashx?key=` (City of Vallejo's document server)
- NOP25 = `https://ceqanet.lci.ca.gov/2025081410/Attachment/7biXwK` (SDC notice of preparation, Aug 29, 2025; the same file Permit Sonoma posts as `SIGNED-SDC-Eldridge-NOP-20250826.pdf`)

Hosts not yet in `src/projects/official.ts`:
- `cityofvallejo.net` (with `portal.cityofvallejo.net`, the City's ArcGIS server). The City's own domain: the City's comment letter lists staff at `@cityofvallejo.net` (City Manager andrew.murray@, Assistant City Manager gillian.haen@, Planning Director kristin.pollot@; VJO`9yhFAU3W` p.1), and its Planning Division letterhead is 555 Santa Clara Street. The City also runs `vallejo.gov` (passes as .gov but sits behind a Cloudflare challenge that blocked every fetch).
- `permitsonoma.org` (with `parcelsearch.permitsonoma.org`). Sonoma County's Permit & Resource Management Department: the county's own pages link to it (`sonomacounty.gov` District 1 SDC page: "visit Permitsonoma.org"), and its letters carry the County of Sonoma letterhead at 2550 Ventura Avenue. It holds the SDC project page, scoping boards (phasing) and the completeness letter that names the developer team.
- Optional: `stories.opengov.com/cityofvallejo/` (City Manager reports Vallejo publishes on OpenGov). Only needed for the 2019 Nimitz acquisition.

---

## mare-island

Recommendation: **INCLUDE** (stage `entitlement`). A whole former naval shipyard with a new specific plan under formal City review, at up to 14,000 homes. The record fails the record check only because `cityofvallejo.net` isn't on the official-host list yet. Add the host and it passes; the schema already validates.

Documents read:
- VJO`5As%2FAST1`: Vallejo Land Use Entitlement (VALUE) List, Long Range Planning Projects, May 2026 (7 pp.).
- VJO`9yhFAU3W`: City letter to Mare Island Company, "Draft Mare Island Specific Plan (File #SPA24-0001)", Feb 7, 2026 (87 pp.).
- VJO`A8pCAb40`: Mare Island Infrastructure Assessment, final report, October 2025, for the City and Vallejo Flood & Wastewater District (West Yost; 268 pp., 266 MB).
- VJO`piRGAR%2Fa`: Hanson Bridgett letter for the Vallejo Flood and Wastewater District to the City, June 30, 2026 (20 pp.).
- CEQAnet SCH 2003092057, documents 1 (NOP, 2003-09-18) and 2 (supplemental EIR, 2005-08-11): `https://ceqanet.lci.ca.gov/2003092057/2`.
- City GIS: `https://portal.cityofvallejo.net/arcgis/rest/services/CityGIS_Viewer/Planning_Development_Services/MapServer` (layers 3, 65–69).

| field | official value | source | verbatim quote |
|---|---|---|---|
| plan history | adopted 1999; amended and restated 2005; amended Aug 2014 | VALUE p.2; CEQAnet 2003092057/2; MIIA p.50 | "comprehensive update to the Mare Island Specific Plan (MISP), originally adopted by the Vallejo City Council in 1999"; "Amend and restate the 1999 Mare Island Specific Plan with the 2005 Mare Island Specific Plan ... including an additional 2.7 million square feet of development potential"; "Mare Island Specific Plan, Amended August 2014" |
| acres | 5,250 (whole island, the 2003–05 EIR) | CEQAnet 2003092057/1 and /2 | "Total Acres 5,250" |
| homes | up to 14,000 (draft, not approved) | VALUE p.2 | "The land use plan in the draft is estimated to generate up to 14,000 dwelling units and between 14,900 and 17,000 jobs." |
| neighborhoods | nine | VALUE p.2 | "envisions the redevelopment of Mare Island into nine livable, connected, and diverse neighborhoods" |
| earlier build-out scenario | 9,271 homes; 8,130,380 sq ft commercial; 18,000 jobs; build-out by 2063 (from MIC's Feb 2023 preliminary plan; superseded by the Oct 2024 draft) | MIIA p.45 (Table 2-3), p.33 | "Residential Uses 9,271"; "Commercial Uses - 8,130,380"; "(b) Includes 18,000 jobs"; "Build-out is expected to occur within 40 years, year 2063." |
| scope of the build-out | MIC land only; Navy and State lands excluded | MIIA p.45 | "This plan identified build-out land uses for all areas of the island, excluding Navy and State lands." |
| developer | Mare Island Company / Nimitz Group | letter p.1 | "Dear Andrea Jones and Mare Island Company / Nimitz Group Team" |
| draft submitted | Oct 10, 2024, file SPA24-0001 | letter p.1 | "Thank you for submitting the First Draft of the Mare Island Specific Plan (MISP) dated October 10, 2024." |
| stage / status | City comments sent Feb 7, 2026; second draft, NEPA, CEQA NOP and Draft EIR next | VALUE p.2 | "The City transmitted a consolidated comment letter on the initial draft Mare Island Specific Plan to Mare Island Company on February 7, 2026." "Next steps include continued coordination with Mare Island Company, completion of NEPA documentation, release of the CEQA Notice of Preparation, continued drafting of the Infrastructure Plan and Financing Plan, submittal of a second draft Specific Plan package, and preparation of the Draft EIR for public review." |
| council update | Apr 27, 2026 | VALUE p.2 | "The City Council received an informational update on the Mare Island planning process on April 27, 2026, including updates on the Specific Plan, environmental review, infrastructure planning, development agreements, Beautification Plan, Connolly Corridor Project, and Coral Sea Village Subdivision." |
| development agreement | to be negotiated with the plan | letter p.1 | "matters outlined in Section D (Items for Development Agreement) will be addressed through negotiation of the Development Agreement accompanying adoption of the Specific Plan" |
| heights (draft standards) | 85-ft maximum in the CRMX and CR zones (eight-story mixed use questioned) | letter p.17 (item A36) | "clarify how an eight-story mixed-use building can be built within the 85-foot height maximum if the minimum ground floor non-residential height is 18 feet" |
| Touro neighborhood | 162,000 sq ft academic/office and 895 dorms remaining | letter p.17 (item A39) | "the remaining 162,000 square feet of academic and office space and 895 dorms" |
| Connolly Street corridor | ~29,000 sq ft office, 373 homes, 200-room hotel; not yet submitted (Oct 2025) | MIIA p.38 | "approximately 29,000 square feet of office space, 373 multi-family residential units, a 200-room hotel"; "has not been formally submitted or approved" |
| North Mare Island DDA | CEQA addendum, Feb 2022 | MIIA p.38, fn.1 | "North Mare Island Disposition and Development Agreement (DDA) and Implementation Project; CEQA Addendum to the Mare Island Specific Plan EIS/EIR (1999) and the Mare Island Amended and Restated Specific Plan Project Final Subsequent EIR (2005), Stantec, February 2022" |
| dispute | VFWD says the City misstated its comments (A79–A91, C39–C52) | VFWD letter p.1 | "to address errors and inaccuracies in the City of Vallejo ("City") characterization of VFWD's comments" |

Approvals: none yet for the new plan. Earlier: the 1999 plan and EIS/EIR, the 2005 amended and restated plan and subsequent EIR, the 2014 amendment, the 2018 ENA and later DDA for North Mare Island (council records not yet read).

Boundary lead:
- City of Vallejo GIS, `Planning_Development_Services/MapServer/3` (Specific Plans), filter `SpPlan = 'SP-4'` (Name "Mare Island Specific Plan", one ring; bbox lon −122.3175 to −122.2484, lat 38.0643 to 38.1189). Layer 67 ("Existing Specific Plan Area", Mare Island, Year 2005) and layer 69 ("MareIslandSpecificPlan_poly") are alternatives. No copyright or license text on the service, so ask the City before redistributing. This is the adopted plan's area. The new plan's boundary is in the Oct 2024 draft, which the City hasn't posted with the letter.
- Draw it "Approximate boundary"; much of the polygon is wetland and dredge ponds.

Massing lead: the draft MISP development standards (pp.72–83 of the draft, cited in the letter) give zone height limits (85 ft in CRMX/CR). They're applicant proposals still under review, so don't draw them until adoption. MIIA Figure 2-2 maps build-out land use (the 2023 scenario).

Press or non-official only (kept in `reported`):
- City Manager report on OpenGov (City-authored but on a host not yet listed), Nov 2019: "The Nimitz Group has completed its acquisition of 500 acres of land from Lennar Mare Island, LLC (LMI), expanding their holdings to over 800 acres"; ENA for 157 acres of North Mare Island in May 2018; 170-acre golf course bought June 2019. `https://stories.opengov.com/cityofvallejo/published/arHGvVTeZ`
- Vallejo Sun: Connolly corridor project halted while the City negotiates with the developer on infrastructure. `https://www.vallejosun.com/central-corridor-project-on-mare-island-halted-while-vallejo-negotiates-with-developer-on-infrastructure/`
- Mare Island Company's site (`mareislandco.com`): developer's own description of the draft plan. Not used.

Still open: the April 27, 2026 staff report (vallejo.gov blocked); council actions on the ENA, DDA and development agreements; the new plan's boundary and commercial program; what was built under the old plan.

---

## sonoma-developmental-center

Recommendation: **INCLUDE**, at the threshold. 990 homes plus 250,000 sq ft of commercial and hotel space on a 160-acre core campus (209 acres with the wildfire buffer), all in formal county review. It sits just under the 1,000-home bar; what tips it in is a whole-campus master plan with a specific plan, EIR and an active Builder's Remedy application. If the bar is applied strictly, call it BORDERLINE. The draft record passes the record check.

Documents read:
- CEQAnet SCH 2025081410 (NOP, received 2025-08-29) and its attachments: NOP25 (31 pp.) and the PLP24-0005 public notice (`.../Attachment/Ttc3pF`).
- CEQAnet SCH 2022020222 documents 1 (NOP 2022), 2 (Draft EIR), 4 (Final EIR), 5 (NOD 2022-12-19).
- County news release, Dec 4, 2024: `https://sonomacounty.gov/board-of-supervisors-decertifies-eir-and-repeals-the-approval-of-the-sonoma-developmental-center-specific-plan-in-response-to-court-ruling`.
- DGS: Sonoma Developmental Center Annual Report, Dec 12, 2023 (`https://www.dgs.ca.gov/-/media/Divisions/DGS/LegReports/Accessible-Reports/2023/2023-SDC-Annual-Report-ADA-Final.pdf`); 2024 Surplus and Excess Real Property Annual Report (`https://www.dgs.ca.gov/-/media/Divisions/RESD/Publications/AMB/Surplus-Property-for-Sale-PDFs/2024-Surplus-and-Excess-Property-Report-Final-v26.pdf`); RFP AMB 2022-05-17.
- Permit Sonoma (host to add): project page `https://permitsonoma.org/sdcproject`; long-range plan page `https://permitsonoma.org/regulationsandlongrangeplans/longrangeplans/sonomadevelopmentalcenter`; completeness letter `https://parcelsearch.permitsonoma.org/api/documents/8710024` (Mar 6, 2025); scoping boards 1A, 3A, 3B, 6 and the Sept 25, 2025 scoping presentation (under `https://permitsonoma.org/Microsites/Permit%20Sonoma/Documents/Divisions/Planning/Project%20Review/SDC/`).

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres (project area) | 160-acre core campus plus 49-acre wildfire buffer | NOP25 p.3; CEQAnet 2025081410 | "The Project Area consists of a 160-acre core campus and surrounding 49-acre wildfire buffer."; "Total Acres 160" |
| acres (historic site) | about 945 (core ~180, rest ~765) | NOP25 p.3 | "With a total area of approximately 945 acres, the SDC site consisted of a developed core campus covering approximately 180 acres and approximately 765 acres" |
| land transfers | ~650 ac to State Parks (Jan 2024); ~58 ac to CAL FIRE (Feb 2024; DGS says March 2024, 58.15 ac) | NOP25 p.3; DGS 2024 p.9 | "In January 2024, the State transferred approximately 650 acres of open space on the SDC site to the California Department of Parks and Recreation"; "In March 2024, approximately 58.15 acres of open space bordering Highway 12 transferred to CAL FIRE" |
| homes | 990 (785 market rate, 200 affordable, 5 independent living) | NOP25 p.7 | "the Project would involve 785 new market rate units, 5 independent living homes, and 200 affordable units" |
| affordable | 200, "slightly more than 20 percent" | NOP25 p.7 | "200 units or slightly more than 20 percent would be deed restricted for lower income households" |
| commercial | ~130,000 sq ft | NOP25 p.7 | "Approximately 130,000 square feet of commercial uses, including office, retail, research and development, micro-manufacturing" |
| hotel | 150 rooms, ~120,000 sq ft with parking structure | NOP25 p.7 | "A 150-room hotel and ancillary uses and amenities with a parking structure (approximately 120,000 square feet in total)" |
| commercial + hotel | 250,000 sq ft (background wording) | NOP25 p.2 | "250,000 square feet of commercial space including office, retail, research and development, and micro-manufacturing uses and a 150-guest room hotel" |
| open space | ~67 ac (CEQAnet summary and county page say ~70) | NOP25 p.7 | "Approximately 67 acres of outdoor public parks, active recreational areas, and open space areas" |
| heights | apartments, townhomes 2–3 stories; detached 1–3; co-housing 3 | NOP25 pp.7–8 | "Typical building height would be two to three stories" |
| developer | Eldridge Renewal, LLC (letter addressed to Keith Rogal, Rogal and Associates, and Rob Toste, The Grupe Company) | CEQAnet notice p.1; completeness letter p.1 | "Project Applicant: County of Sonoma and Eldridge Renewal LLC"; "Keith Rogal, Rogal and Associates, Eldridge Renewal, LLC" ... "Rob Toste The Grupe Company" |
| application | SB 330 preliminary Aug 2023 (PRE23-0008); full Feb 16, 2024; resubmitted Feb 4, 2025; complete Mar 6, 2025 (PLP24-0005) | completeness letter p.1; CEQAnet 2025081410 | "originally received on February 16, 2024, and resubmitted on February 4, 2025 is complete for processing"; "The application was deemed complete on March 6, 2025" |
| Builder's Remedy | yes | CEQAnet 2025081410 | "vesting their rights under the Gov. Code § 65589.5(d)(5) provision known as the "Builder's Remedy."" |
| 2022 plan | adopted Dec 16, 2022: 620 base homes plus density bonus, 230,000 sq ft commercial/office, 120-room hotel | NOP25 p.2; DGS 2023 p.6 | "620 base dwelling units ... 230,000 square feet of commercial/office space, and a 120-room boutique hotel"; "on December 16, 2022, the county adopted the SDC Specific Plan, certified the FEIR ... amended the general plan, and rezoned the property" |
| lawsuit | filed Jan 18, 2023 (SCALE); final judgment and writ Oct 22, 2024 | DGS 2023 p.6; CEQAnet 2025081410 | "On January 18, 2023, local stakeholders filed a challenge to the FEIR."; "final judgment and writ of mandamus on October 22, 2024" |
| repeal | Dec 3, 2024 | county release (Dec 4, 2024, "on Tuesday"); Permit Sonoma long-range page | "The board on Tuesday decertified the environmental impact report and rescinded the adoption of the Specific Plan."; "On December 3, 2024 the Board of Supervisors voided certification" |
| state sale | buyer selected for exclusive negotiations April 2023 (not named by DGS) | DGS 2024 p.9 | "The state selected a buyer for exclusive negotiations in April 2023." |
| new EIR | NOP Aug 29, 2025; scoping Sept 25, 2025 | NOP25 p.1 | "Comment Period: August 29, 2025 through September 29, 2025"; "Scoping Meeting: September 25, 2025" |
| Draft EIR timing | not in 2026 | Permit Sonoma project page | "the Draft EIR will not be ready for release in 2026" |
| phasing (proposed) | three phases, Mar 2027 to Aug 2036 | scoping board 6 (Development Phasing Plan) | "three staggered phases over a period of approximately 9.5 years between March 2027 and August 2036" |

Approvals: none current. The 2022 specific plan, EIR, General Plan amendment and rezoning were set aside on Dec 3, 2024. The Builder's Remedy application is limited to five hearings (Permit Sonoma FAQ). Superseded documents (the 2022 plan and its EIR) shouldn't be drawn as current.

Boundary lead:
- Trace NOP25 Figure 3, "Project Area" (PDF p.21): the 160-acre core campus and the 49-acre wildfire buffer, drawn "Approximate boundary". Figure 2 (p.20) shows the pre-2024 boundary and the transfers.
- County of Sonoma parcels (`https://socogis.sonomacounty.ca.gov/map/rest/services/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0`, `APN in ('054-090-001','054-150-005','054-150-010')`), CC BY-SA 3.0, attribution "County of Sonoma". The three parcels still total about 990 acres (pre-transfer), so use them only as context or to clip the traced figure. DGS's 2024 report also lists 054-150-013 and part of 054-080-001.
- CEQAnet coordinates: 38°20'50"N 122°31'7"W.

Massing lead: NOP25 Figure 4 (site plan, p.22) and scoping board 3B (proposed site plan and development program). Heights from the NOP text are 2–3 stories, so the drawing is "Illustrative massing". The future objective design standards are in the revised specific plan, which isn't published yet.

Press only (kept in `reported`):
- Press Democrat, Apr 4, 2023: the state picked The Grupe Company and Rogal & Partners. `https://www.pressdemocrat.com/2023/04/04/state-picks-developers-for-the-sonoma-developmental-center-2/`
- Press Democrat: a lawsuit seeks to vacate the state's selection of Eldridge Renewal. `https://www.pressdemocrat.com/article/news/sonoma-developmental-center-lawsuit-eldridge-renewal/`
- Press Democrat: the county was "blindsided" when the developer sought hundreds more units. `https://www.pressdemocrat.com/article/news/a-new-wrinkle-in-bid-to-redevelop-sonoma-development-center-site-came-out/` (not read)

Still open: whether the state and Eldridge Renewal have signed a purchase and sale agreement (DGS's 2025 report isn't posted); the Draft EIR date; the outcome of the suit over the state's selection.
