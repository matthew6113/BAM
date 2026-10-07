# Candidate projects: UCSF Parnassus Heights, Tanforan

Checked 2026-10-07. I downloaded the documents and read them in full text. Local copies are in `data/raw/official/ucsf-parnassus/` and `data/raw/official/tanforan/` (git-ignored). Page numbers are PDF page numbers. Draft records are in the scratchpad (`records/new/<id>.json`); both pass `tests/record-check.test.ts`.

Access notes:
- `realestate.ucsf.edu`, `campusplanning.ucsf.edu` and `www.ucsf.edu` return 403 to curl and to WebFetch. UCSF facts come from UC Regents items and minutes (`regents.universityofcalifornia.edu`), CEQAnet, and HCAI open data instead. Regents meeting index pages don't exist; items are at `regmeet/<mon><yy>/<item>.pdf` (e.g. `jan21/f5.pdf`) and minutes at `minutes/<yyyy>/board<m>.<d>.pdf`. There are no July meetings in that pattern.
- HCAI's eServices portal (`esp.oshpd.ca.gov`) fails TLS through the proxy; its open data on `data.chhs.ca.gov` works.
- `www.sanbruno.ca.gov` works but drops connections often; retry. Its AgendaCenter search (`/AgendaCenter/Search/?term=tanforan&CIDs=all&startDate=...`) lists packets; the site search is JavaScript-only.
- San Mateo County's ArcGIS server (`gis.smcgov.org`) returns "Access Unavailable"; its Socrata portal `data.smcgov.org` works.

Hosts:
- Added `smcgov.org` to `src/projects/official.ts` (County of San Mateo; `data.smcgov.org` parcels).
- `sanbruno.ca.gov`, `data.chhs.ca.gov` (California Health and Human Services, HCAI datasets) and `esp.oshpd.ca.gov` are already official through the `.gov` rule. No UCSF host was added, because nothing on it could be read.

| candidate | recommendation | id |
|---|---|---|
| UCSF Comprehensive Parnassus Heights Plan | INCLUDE (construction) | `ucsf-parnassus` |
| Tanforan redevelopment, San Bruno | INCLUDE (entitlement) | `tanforan` |

---

## ucsf-parnassus (Comprehensive Parnassus Heights Plan)

Documents:
- REG21 = Regents item F5, Jan 20, 2021 (LRDP Amendment #7 for the CPHP): https://regents.universityofcalifornia.edu/regmeet/jan21/f5.pdf
- MIN21 = Board minutes, Jan 21, 2021: https://regents.universityofcalifornia.edu/minutes/2021/board1.21.pdf
- REG22 = Regents item F6, May 18, 2022 (New Hospital budget, scope, EIR, design): https://regents.universityofcalifornia.edu/regmeet/may22/f6.pdf
- MIN22 = Board minutes, May 19, 2022: https://regents.universityofcalifornia.edu/minutes/2022/board5.19.pdf
- REG23 = Regents item F4, Sept 20, 2023 (Parnassus Research and Academic Building): https://regents.universityofcalifornia.edu/regmeet/sept23/f4.pdf
- CPHP EIR, SCH 2020010175: https://ceqanet.lci.ca.gov/2020010175. Draft EIR (July 2020, 144 MB): `.../2020010175/3/Attachment/el9B-o`. NOD, Jan 22, 2021: https://ceqanet.lci.ca.gov/2020010175/7. Later NODs for LPPI demolition (May 2022), PRAB make-ready (Sept 2022), PRAB (Sept 2023), Central Campus Site Improvements (Sept 2024).
- New Hospital EIR, SCH 2021070547: https://ceqanet.lci.ca.gov/2021070547. Final EIR Vol. 1 (May 2022): `.../2021070547/3/Attachment/Squ362`. NOD for Addendum #1, Apr 14, 2026: https://ceqanet.lci.ca.gov/2021070547/6 (PDF `.../6/Attachment/bP5FW8`).
- HCAI Hospital Building Data (data generated Oct 1, 2026): https://data.chhs.ca.gov/dataset/hospital-building-data (CSV `ca-hcai-hospital-building-data-10012026.csv`).

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | about 107; 61-acre reserve | REG21 p.3 | "comprising approximately 107 acres of land in the mature Inner Sunset mixed-use neighborhood"; "The 61-acre Mount Sutro Open Space Reserve occupies the central and southern portion of the campus site." |
| plan horizon | about 30 years, to ~2050 | REG21 p.6 | "would guide the development of the Parnassus Heights campus site through the next 30 years, or an approximate horizon year of 2050" |
| new space | about 2.9 million gsf | CEQAnet NOD 2020010175/7 | "In total, the CPHP provides for development of approximately 2.9 million gross square feet (gsf) of new building space at Parnassus Heights." |
| space ceiling | 3.55 → 5.05 million gsf (non-residential) | REG21 p.7–8 | "would increase the space ceiling limit from the current 3.55 million gsf to a proposed 5.05 million gsf, excluding housing" |
| net space | +1.37 million gsf over 2019 | REG21 p.7 | "the proposed LRDP amendment would result in a net increase in the space program by approximately 1.37 million gsf (excluding housing) by 2050" |
| population | 17,400 (2018) → 25,300 (2050) | REG21 p.7–8 | "a net increase in the average daily population by approximately 7,900 by 2050" |
| on-campus homes | 762 new (332 net at Aldea, 430 West Side) | REG21 p.12; CPHP DEIR p.571 | "The CPHP proposes the development of an additional 762 units of on-campus housing for students, faculty, and staff, comprised of 332 net new units at the Aldea Housing complex and 430 units in the West Side district" |
| on-campus homes total | 222 → 364 (2030) → 984 (2050) | CPHP DEIR p.569 | "housing on the campus site would increase to a total of 364 housing units by 2030, and to a total of 984 units by 2050" |
| MOU homes (citywide) | 1,263, 40% affordable, half by 2030 | REG22 p.16 | "Housing: Build 1,263 new homes citywide (40 percent affordable) – half of them by 2030. To date, 71 homes have been delivered, and 230 homes are under construction" |
| CPHP approval | Jan 21, 2021, conditioned on the City MOU | MIN21 pp.27–28 | "Approval of paragraph (4) above is conditioned on the Chair of the Board of Regents countersigning the Memorandum of Understanding (MOU) between UCSF and the City and County of San Francisco"; "Upon motion of Chair Pérez, duly seconded, the recommendation, as amended, was approved" |
| initial phase | hospital, RAB, Irving St arrival, Aldea, by 2030 | REG21 p.5 | "The CPHP proposes the following four Initial Phase projects to be completed by 2030" |
| hospital scope | 15 stories, ~875,000 gsf, ~336 beds | REG22 p.2; MIN22 p.20 | "construction of a 15-story, approximately 875,000-gross-square-foot (GSF) new hospital building, providing approximately 336 patient beds" |
| beds | 499 (2022) → 682 (2030) at Parnassus | REG22 p.5 (Table 2) | "Total 499 682 183" |
| hospital budget | $4,332,271,000 | REG22 p.1–2, p.23 | "approve the full budget of $4,332,271,000 to be funded from external financing ($2,666,271,000), gift funds ($1.2 billion), and hospital reserves ($466 million)" |
| Diller gift | $500 million | REG22 p.8 | "including a $500 million philanthropic commitment from the Helen Diller Foundation" |
| hospital approval | May 19, 2022 | MIN22 p.24; NOD 2021070547/4 | "the recommendations of the Finance and Capital Strategies Committee were approved"; NOD "Approved On 5/19/2022" |
| hospital height | ~269 ft to roof, ~294 ft to rooftop screen | NHPH FEIR Vol.1 p.70 | "The height of the building above ground level would be approximately 269 feet to the roof level, and approximately 294 feet to top of rooftop perimeter screening." (EIR studied ~900,000 gsf; the approved scope is ~875,000 gsf) |
| massing | 5-story podium, 4-story inset, 6-story stepped tower | REG22 p.9 | "a five-story base Podium ... a four-story middle Inset portion ... and the stepped six-story Mountain form containing patient rooms" |
| schedule (2022) | completion 2030; renovations 2030–2034; opening FY 2031 | REG22 p.13, p.28 | "to maintain a mandated completion date for the New Hospital in 2030. Renovations of Moffitt and Long Hospitals would begin in early 2030 and be complete in 2034."; "the New Hospital, which is scheduled to open in FY 2031" |
| construction start | April 2024 | NOD Apr 14, 2026 | "Construction on the HDH project commenced in April 2024." |
| 2026 status | structural steel and above-ground concrete phases next | NOD Apr 14, 2026 | "during planning for the next two phases of construction, the Structural Steel phase and Above-Ground Structural Concrete phase" |
| HCAI status | Helen Diller Hospital, BLD-06771, under construction, 15 stories | HCAI CSV (Oct 1, 2026) | "UCSF Medical Center,San Francisco,BLD-06771,Helen Diller Hospital,OSHPD 1-Under Construction,5s,...,15,2019 California Building Code (CBC)" |
| PRAB | 9 stories, ~323,000 gsf, $843.1M; construction end of 2023 into 2028 | REG23 p.1–2, p.11; NOD 2020010175/14 (approved 9/21/2023) | "the construction of a nine-story"; "approve the full budget of $843.1 million"; "Construction of the new building and remaining site improvements for the west campus are scheduled to begin at the end of 2023 and continue into 2028." |

Superseded: the CPHP Draft EIR (2020) described the hospital at about 955,000 gsf, 16 stories and up to 294 ft (DEIR p.108). The New Hospital EIR (2021–22) is 15 stories and ~900,000 gsf, and the Regents approved ~875,000 gsf. Use the 2022 figures.

Conflicts with the brief and with press:
- The "~1,200 housing units" figure is the MOU's **1,263 homes citywide**, not homes on this site. The CPHP itself adds 762 on-campus units. The draft record uses 762 and puts 1,263 in the notes.
- "Opening 2030": officially, *completion* is mandated in 2030, and UCSF Health's projections show opening in FY 2031 (as of 2022). No newer official date was found.
- Cost: $4.33 billion is the May 2022 approved budget. I found no later official revision in Regents items through Sept 2026 (I checked items f1–f18, h, b, a and c for every meeting).

Stage: `construction` (hospital since April 2024).

Boundary lead:
- The official campus boundary is the 2014 LRDP "Figure 6-11" (named in the Regents' Resolution, REG21 Attachment 5), as amended by Amendments #7 and #10. It is on `campusplanning.ucsf.edu`, which blocks scripts. CPHP DEIR Figure 3-14 shows the hospital study area.
- DataSF parcels (acdm-wktn, ODC PDDL): block 2634A lots 011 (90.87 ac, includes Mount Sutro), 003 (12.8 ac), 005 (2.96 ac, the LPPI/hospital site; New Hospital DEIR lists "Block 2634A/Lot 011 & 005") and 012 (0.97 ac) total about 107.6 acres. That is close to 107, but campus blocks north of Parnassus Avenue (Irving Street side) may need adding. Trace against the LRDP figure and label it "Approximate boundary".
- HCAI gives the facility point 37.763106, -122.457822.

Massing lead: Helen Diller Hospital, 15 stories, 269 ft roof / 294 ft screen (NHPH FEIR p.70), on lot 005 east of Moffitt/Long; podium, inset and stepped tower (REG22 p.9). PRAB 9 stories on the UC Hall site. West Side housing 6–10 stories, 72–120 ft (CPHP DEIR p.116). Draw as "Illustrative massing".

Not found officially: Aldea or West Side housing project approvals; PRAB 2026 status; any HCAI-published completion date.

Recommendation: INCLUDE. It has about 2.9 million gsf of new space (well over the 1M sq ft bar), an approved plan and EIR, and a $4.33B hospital under construction.

---

## tanforan (Tanforan redevelopment, San Bruno)

Documents:
- CEQAnet SCH 2023120409: https://ceqanet.lci.ca.gov/2023120409 (NOP Dec 14, 2023; Draft EIR June 27, 2025, `/2`; **Final EIR received Oct 5, 2026**, `/3`).
- DEIR = Draft EIR, June 2025: `https://ceqanet.lci.ca.gov/2023120409/2/Attachment/bUptzG` (also City DocumentCenter 7602).
- FEIR = Final EIR, October 2026: `https://ceqanet.lci.ca.gov/2023120409/3/Attachment/dIF3g9`, same as `https://www.sanbruno.ca.gov/DocumentCenter/View/9642/Tanforan_Redevelopment_Project_FEIR_ADA`; MMRP at DocumentCenter 9643.
- SR26 = Joint City Council/Planning Commission study session packet, May 19, 2026 (staff report, Item 3c, pp. 25–29): https://www.sanbruno.ca.gov/AgendaCenter/ViewFile/Agenda/_05192026-2573
- Slides, May 19, 2026: https://www.sanbruno.ca.gov/AgendaCenter/ViewFile/Agenda/_05192026-2582
- City development update, Oct 2026: https://www.sanbruno.ca.gov/DocumentCenter/View/9615/October-2026-Development-Update
- County of San Mateo parcels: https://data.smcgov.org/d/nr6j-72z7 (Public Domain)

| field | official value | source | verbatim quote |
|---|---|---|---|
| applicant | ARE-San Francisco No. 96, LLC | DEIR p.52 | "ARE-San Francisco No.96, LLC (project applicant) proposes to redevelop the 44-acre Shops at Tanforan Shopping Center" |
| developer identity | Alexandria Real Estate (ARE) | SR26 p.25 | "the Tanforan redevelopment project proposed by Alexandria Real Estate (ARE)" |
| purchase | 2021–2022, $351M total | SR26 p.25 | "ARE purchased the Tanforan properties from multiple owners in 2021 and 2022 for a total of $351 M." |
| acres, parcels | 44 acres, six APNs | DEIR p.53 | "The 44-acre project site includes six parcels (APNs 014-316-080, 014-316-300, 014-316-310, 014-316-360, 014-316-330, and 014-316-060)" |
| APN discrepancy | NOP and County give 014-311-060 for the vacant lot | CEQAnet NOP | "six parcels (APNs 014-316-080, 014-316-300, 014-316-310, 014-316-360, 014-316-330, and 014-311-060)" |
| program | homes 1,014–1,514; lab/office 1,174,000–1,723,580 sq ft; retail 111,950–211,950; amenity 55,000–69,000; hotel 170 rooms | DEIR p.65; CEQAnet FEIR summary | "approximately 1,014 to 1,514 multi-family residential units ... approximately 1,174,000 to 1,723,580 square feet of life-science laboratory and office uses, and approximately 55,000 to 69,000 square feet of amenity uses ... The project could also construct a 125,000-square foot, 170-room hotel." |
| affordable | up to 200 in a stand-alone building | DEIR p.66 | "The housing component would include up to 200 affordable housing units in a stand-alone building on the northern portion of the project site." |
| net new | 2,169,041–2,330,461 sq ft | DEIR p.66 | "In total, the project would construct 2,169,041 to 2,330,461 square feet of net new development on the project site." |
| demolition, kept | ~785,489 sq ft demolished; Target and theater stay | DEIR p.65 | "demolish all existing uses on the project site except for the Century at Tanforan Theater, the Target, and their associated parking garages" |
| scenarios | A (R&D): 1,014 homes, 1,792,580 sf office/R&D incl. amenity; B (residential): 1,514 homes, 1,229,000 sf office/R&D incl. amenity, hotel | DEIR Tables 2-2, 2-3 (pp. 70–71) | "Office/R&D (Total) - - 1,792,580"; "Residential (Total) ... (1,514 DU)" |
| density, FAR | min 75 du/ac, max 1,514 homes; FAR 4.5 | DEIR p.66 | "multi-family housing densities at a minimum of 75 dwelling units per acre, and a maximum number of 1,514 dwelling units"; "combined floor area ratio (FAR) maximum ... would be 4.5" |
| heights | 1–7 stories, 20 ft to 79 ft 7 in; SFO limits 127–148 ft AMSL | DEIR p.71; FEIR p.133 (revision) | "Proposed building heights would range from 1 to 7 stories (20 to 79 feet, 7 inches)"; the FEIR changes "125 feet to 145 feet" to "127 feet to 148 feet" |
| open space | 8.2 ac (A) / 8 ac (B), ~98,500–99,000 sf public | DEIR p.72 | "for a total of 356,000 sf (8.2 acres) of open space"; "for a total of 350,000 sf (8 acres) of open space" |
| CEQA schedule (2025) | Make Ready ~1.3 yrs; full build-out ~6 yrs later, by 2033 | DEIR p.84 | "completion of Phase 4 Flex 2, which would be full build-out, could occur approximately 6 years after the end of Make Ready, by the fall of 2033" |
| approvals needed | GPA, PD zoning and plan, design guidelines, PD permits, vesting tentative map, DA, ALUC override, EIR | DEIR p.88 | "General Plan Amendment ... Development Agreement ... Override of Airport Land Use Commission Inconsistency Determination for Residential Uses" |
| prior zoning action | Ords. 1954, 1955, Sept 10, 2024 | DEIR p.57 | "(Ordinance Nos. 1954 and 1955, adopted by the San Bruno City Council on September 10, 2024)" |
| ALUC override | first 1,014 units already overridden | SR26 p.26 | "the City Council already approved a prior override to allow the first 1,014 units as part of the Housing Element" |
| DA status | stalled late 2025, resumed early 2026 | SR26 p.28 | "DA negotiations stalled in the latter half of 2025, delaying the project." "Negotiations re-commenced in early 2026" |
| DA principles | endorsed Aug 26, 2025 | SR26 p.28 | "City Council endorsed a list of Guiding Principles for the Development Agreement on August 26, 2025" |
| hearings | PC Oct 20, 2026; Council certification Nov 10, 2026 (anticipated) | FEIR pp.7–8 | "The Planning Commission anticipates holding a hearing on October 20, 2026"; "The City anticipates that certification of the Final EIR will be considered by the City Council on November 10, 2026." |
| City project list | "Under Review" (Oct 2026 update still says Draft EIR available) | Oct 2026 development update | "Tanforan ... Under Review New transit oriented mixed use village Draft Environmental Impact Report Available." |

Not yet posted: the Planning Commission's Oct 20 agenda (none on the AgendaCenter as of Oct 7), a draft development agreement, and an ALUC decision on the extra 500 homes.

Developer expectations (SR26 p.29; ARE's view, quoted by staff; kept in `reported`): "By the end of 2027 • Demolition and site preparation"; "By the end of 2028 • Residential partner begins vertical construction of the first building(s)"; "By the end of 2030 • First building(s) completed"; "Full build-out is anticipated to be at least 10-15 years out." This conflicts with the DEIR's construction scenario (build-out by 2033), which is a CEQA assumption, not a schedule.

Minor inconsistency: the May 2026 slides describe the early phases as "780,000 sq. ft. of life-science lab/office space" and "100,000 sq. ft. of new retail", while DEIR Table 2-2 has 724,000 sf office plus 35,000 sf amenity and 106,250 sf in-line retail. Use the EIR.

Stage: `entitlement` (Final EIR out; hearings pending).

Boundary lead:
- County of San Mateo parcels, `https://data.smcgov.org/resource/nr6j-72z7.json?$where=apn in('014316080','014316300','014316310','014316360','014316330','014311060')`. All six return; the `shape` field is WKT in State Plane CA III feet (EPSG 2227). Computed areas are 15.33, 11.98, 11.47, 2.22, 1.52 and 1.41 ac, about 43.92 ac in all. These match DEIR Table 2-1 (p.53) to within 0.06 ac. License: Public Domain. Credit "County of San Mateo".
- Cross-check against DEIR Figure 2-3 (Existing Parcels). CEQAnet point: 37°38'10.91"N 122°25'4.79"W.

Massing lead: DEIR Figure 2-8 (Conceptual Site Plan) and Figure 2-10 (Conceptual Building Height Plan), max 79 ft 7 in. Three residential buildings line Sneath Lane, a retail village sits in the center, lab/office and a parking structure are south of Tanforan Way, and flex zones sit at the NW and SE corners. Draw as "Illustrative massing". The City also hosts the applicant's Phase 1 package (`sanbruno.ca.gov/DocumentCenter/View/6348`, "2024 1004_Tanforan_Phase 01 Package"), not read.

Recommendation: INCLUDE. It has 1,014–1,514 homes and 1.17–1.72M sq ft of lab/office on 44 acres next to BART, with a Final EIR published Oct 2026 and hearings set for fall 2026.
