# Official-source findings: new Bay Area ferry terminals

Checked 2026-10-12. Matthew asked on 2026-10-12: "please check for upcoming ferry terminals, and add as
applicable". This file surveys new ferry terminals and major terminal rebuilds that are planned, funded, in
environmental review, approved or under construction, notes the ones recently finished, and says which go on
the map.

Inclusion test used here (Matthew's brief): an official project with a defined site and at least environmental
review under way or funding committed. Long-range vision ideas and finished terminals are left out (and
listed). Electrification of an existing terminal is not a new terminal.

How it was read: WETA's site (`www.sfbayferry.com`) answers scripts with a 403 unless a browser user agent is
sent; with one it serves its pages, its WordPress API and its document store on CloudFront. Board packets,
budgets and fact sheets were read in full as text. CEQAnet project and document pages, the Draft EIRs (read in
full), Port of San Francisco Port Commission memos, the Public Works Commission award, Board of Supervisors
resolutions, City of Berkeley pages and staff reports, the Golden Gate Bridge District's study page and Plan Bay
Area 2050+ were read directly. Local copies are in `data/raw/official/ferry/` (git-ignored). Page numbers are
PDF pages unless a document page is given ("p. ES-7").

URL shorthand:
- `WETA-SEP26` = `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260921171636/b9252026aFULLLink.pdf`
  (WETA Board packet, Sept 25, 2026: capital program quarterly report, July 2026 minutes, budget tables)
- `WETA-JUN26` = `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260605181542/b61126aFULLLink.pdf`
  (WETA Board packet, June 11, 2026, with the May 14, 2026 minutes)
- `WETA-FY27` = `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260612202624/FY2027-Final-Budget.pdf`
  (WETA FY2026/27 adopted budget, capital project descriptions pp. 15-18, capital budget table)
- `PBA` = `https://planbayarea.org/sites/default/files/documents/2026-04/Final_Plan_Bay_Area_2050_Plus_Transportation_Project_List_Report.pdf`

## Hosts added to `src/projects/official.ts`

- `sfbayferry.com` — the San Francisco Bay Area Water Emergency Transportation Authority (WETA), a regional
  public agency, which runs San Francisco Bay Ferry. WETA's own Board packets name it: "The full agenda packet
  is available for download at sanfranciscobayferry.com/next-board-meeting/" (WETA-SEP26, p. 1), and
  `sanfranciscobayferry.com` now answers with a 301 to `www.sfbayferry.com`. The Port of Redwood City's and the
  City of Berkeley's Draft EIRs cite `sanfranciscobayferry.com` pages as WETA's.
- `sanfranciscobayferry.com` — WETA's former domain (same proof).
- `d262kwcyxl71on.cloudfront.net/wp-content/uploads/` (prefix only) — WETA's document store: every Board
  packet, minutes, budget and fact sheet linked from `www.sfbayferry.com/board-meetings/`,
  `/media-and-reports/` and the project pages is served from this CloudFront distribution's WordPress uploads
  folder (an AWS S3 origin). A CloudFront distribution name belongs to one account; only its `wp-content/uploads/`
  path is accepted. A test checks that another distribution is not.
- `sfpublicworks.org` — San Francisco Public Works, a City department (sf.gov's Public Works pages link to it).
  Its Commission awarded the Mission Bay Ferry Landing contract.

---

## Summary

| # | terminal | city | stage (date) | cost / funding (official) | recommendation |
|---|---|---|---|---|---|
| 1 | Mission Bay Ferry Landing (16th Street) | San Francisco | site work: MND 2018, permits 2019-2025, Phase 1 dredging done 2020; $33.0M construction contract awarded July 23, 2026, start expected Aug 2026 | Phase 2B contract $33,018,200; SFCTA $4.5M grant "leverages more than $75.8 million" | **INCLUDE**, mapped as `mission-bay-ferry-landing` |
| 2 | Berkeley Pier and ferry terminal (Berkeley Water Transportation Pier Ferry) | Berkeley | in entitlement: Draft EIR Feb 27, 2026; Final EIR to Council fall 2026 | $105.8M at 60% design (City, Sept 2026); ~$11M secured for design/EIR; no construction funding | **INCLUDE**, mapped as `berkeley-pier-ferry` |
| 3 | Port of Redwood City Ferry Terminal | Redwood City | in entitlement: Draft EIR Sept 17, 2026, comments to Nov 2, 2026 | none in the EIR; PBA $78M for Oakland-Redwood City service incl. terminal | **INCLUDE**, mapped as `redwood-city-ferry-terminal` |
| 4 | Harbor Bay Ferry Terminal Modernization (new terminal north of the existing one) | Alameda | planning/design; CEQA approach being set | $38.1M budget, mostly unfunded | BORDERLINE (would tip with a CEQA document and funding) |
| 5 | Vallejo Ferry Terminal Reconfiguration | Vallejo | IS/MND adopted July 2024; design-build RFP fall 2026 | $22.0M budget | EXCLUDE (rebuild within the existing terminal's footprint) |
| 6 | Larkspur Ferry Service and Parking Expansion (Golden Gate Ferry) | Larkspur | NOP Sept 30, 2024; Draft EIR date TBD | — | BORDERLINE (service and parking at an existing terminal; no Draft EIR yet) |
| 7 | Treasure Island terminal electrification | San Francisco | fully funded, statutory exemption 2025, construction award due Nov 2026 | $6.8M | EXCLUDE (existing terminal; part of `treasure-island`) |
| 8 | Oakland, Seaplane Lagoon, Downtown SF (Gate G), Richmond, Main Street electrification | various | design/construction | see below | EXCLUDE (electrification of existing terminals) |
| 9 | Carquinez Strait (Hercules, Martinez, Benicia, Pittsburg, Antioch), South Bay, Foster City, Mare Island short-hops | — | vision / studies only | — | EXCLUDE (no official project with a site) |
| 10 | Seaplane Lagoon (2021), Richmond, Downtown SF expansion, Main Street refurbishment, Central and North Bay maintenance facilities, Treasure Island landing | — | complete | — | EXCLUDE (complete) |

Three terminals mapped (the cap was six); the rest are listed for Matthew below.

**Separate projects, not one program.** The map's one program-level record, `bart-station-housing`, groups
sites that share one agency and one program and are each too small alone. These three terminals have different
lead agencies (the Port of San Francisco, the City of Berkeley, the Port of Redwood City), different stages
(site work against two Draft EIRs) and different funding, and each has its own CEQA record and site. As
separate projects each flies in to its own shoreline site and states its own stage honestly; a "new ferry
terminals" program would need a camera from Berkeley to Redwood City and a single stage that fits none of them.
This also follows how the SMART extensions are separate records.

**Drawing.** No new drawing type. Each terminal is an ordinary site project: a boundary from official GIS
(parcels named in the CEQA documents) or traced from the EIR's site figure, with no massing (piers, gangways and
floats are low structures on the water; the Redwood City hotel is a rezoning allowance with no design). The line
projects' station points weren't used: a project with stations but no alignment would fail the line tests and
the landed view hides the boundary for line projects.

---

## 1. mission-bay-ferry-landing

Recommendation: **INCLUDE**, stage `infrastructure` (site work). A single-float, two-berth regional ferry
landing at Terry A. Francois Boulevard about 100 ft south of 16th Street, with a covered pier, plaza and Agua
Vista Park improvements, built by the Port of San Francisco; WETA builds the electric charging float.

Documents read:
- SF Planning, Final Mitigated Negative Declaration, Case 2017-008824ENV (June 18, 2018):
  `https://sfmea.sfplanning.org/Mission%20Bay%20Ferry_Final%20MND_061818.pdf`; CEQAnet SCH 2018052002:
  `https://ceqanet.lci.ca.gov/Project/2018052002`.
- Port Commission memos: Phase 2a advertise (Feb 21, 2025) `https://www.sfport.com/media/10211/download`;
  Phase 2a award (May 9, 2025) `https://www.sfport.com/media/10448/download`; COWI amendment (May 9, 2025)
  `https://www.sfport.com/media/10449/download`.
- Public Works Commission, July 23, 2026: staff report and award
  `https://sfpublicworks.org/sites/default/files/Commissions/July%2023%2C%202026/Item%206_PWC%20Mission%20Bay%20Ferry%20SR%20Reso%20award%202026-7-23%20v722.pdf`;
  resolution
  `https://sfpublicworks.org/sites/default/files/Commissions/July%2023%2C%202026/Resolution%207-23-2026/PWC%20Resolution%202026-0068%20Mission%20Bay%20Ferry%20Award%202026-7-23.pdf`.
- Board of Supervisors Resolutions 404-26 `https://media.api.sf.gov/documents/r0404-26.pdf` and 399-26
  `https://media.api.sf.gov/documents/r0399-26.pdf` (both adopted July 14, 2026).
- WETA project page `https://www.sfbayferry.com/project/mission-bay-ferry-landing/`; WETA-SEP26; WETA-FY27.

| field | official value | source | quote |
|---|---|---|---|
| site | Block/Lot 9900/064 and 9900/064H; lot size 153,257 sq ft | MND cover | "Block/Lot: 9900/064 and 9900/064H … Lot Size: 153,257 square feet" |
| location | Terry A. Francois Blvd, ~100 ft south of 16th St | PW staff report p. 1 | "located on Terry Francois Boulevard, approximately 100 feet south of 16th Street" |
| design | single float, two berths; pier 108x22 ft, ramp 26x22 ft, gangway 85x10 ft, float 135x42 ft | MND p. 5, Table 1 | "construction of a single-float, two-berth Ferry Landing" |
| capacity | up to 6,000 passengers/day | Port memo May 9, 2025, p. 2 | "berth two ferry boats simultaneously and handle up to 6,000 passengers per day" |
| CEQA | Final MND June 18, 2018; NOD July 6, 2018; addendum June 4, 2019; memo to file April 30, 2026 | PW staff report p. 3 | "Memorandum to File (2017-008824ENV), issued April 30, 2026" |
| permits | BCDC 2017.008.00 (Dec 17, 2019) and amendment (Aug 1, 2025); USACE SPN-2017-00264S (May 4, 2020); CDFW ITP; NMFS IHA (May 14, 2026) | PW resolution p. 1 | "BCDC Permit 2017.008.01 (Amendment One), issued August 1, 2025" |
| Phase 1 | dredging and site preparation, Dutra, completed 2020 | Port memo May 9, 2025, p. 3 | "The first site preparation project was completed in 2020 with Construction Contract No. 2830." |
| Phase 2a | marine demolition, sand-cap dredging, mattress; advertised Mar 19, 2025; award to Vortex ($13,114,750) recommended | Port memo May 9, 2025, pp. 1, 3 | "award … to Vortex Marine Construction in the amount of $13,114,750" |
| Port authorization | June 9, 2026, PW to advertise/award/oversee Phase 2B, NTE $41M | PW resolution p. 1 | "with a not-to-exceed budget of $41,000,000" |
| award | July 23, 2026: McGuire and Hester - Power Engineering Construction Company JV, $33,018,200 + $3,301,820 contingency, 690 days | PW resolution p. 2 | "in the amount of $33,018,200 with a contingency of $3,301,820" |
| schedule | start Aug 2026; substantial completion Mar 2028; final May 2028 | PW staff report p. 2 | "Anticipated Start of Construction: August 2026 / Substantial Completion: March 2028 / Final Completion: May 2028" |
| contract funding | Port $640,000; 2012 GO bond $2M; SFPUC $4M; UCSF $2.5M; SF sales tax $4.5M; RM3 $13.86M; EPA $5,518,200 | PW staff report p. 2 | table "Contract Total: $33,018,200" |
| total funding | SFCTA $4.5M grant leverages > $75.8M from other sources | Res. 404-26 p. 2 | "leverages more than $75.8 million from other local, state, and federal sources" |
| WETA role | float fabricated and installed by WETA; float RFP Jan 2027; service with second electric vessel Nov 2028 | PW reso p. 2; WETA-SEP26 milestones and July minutes | "Mission Bay electric ferry service with a second vessel anticipated in November 2028" |
| WETA budget | Mission Bay (Facility Electrification) $39,073,047 | WETA-FY27 capital budget table | — |

Boundary: DataSF Parcels (acdm-wktn), blklot 9900064 and 9900064H (ODC PDDL). In the parcel map lot 064 also
covers the water around the old Pier 64 north of the landing (6.8 acres drawn against the MND's 153,257 sq ft);
Pier 64's debris removal is the Phase 2a mitigation work. Massing lead: MND Figures 3-6 (pier, gangway, float,
canopy plan, on an aerial); no heights beyond the pier deck at about 13 ft above MLLW (MND p. 5). Not drawn.

Press-only: none used.

## 2. berkeley-pier-ferry

Recommendation: **INCLUDE**, stage `entitlement`. The City of Berkeley's project to replace the Berkeley
Municipal Pier (closed July 2015) with a dual-use public pier and WETA ferry terminal, a breakwater, charging
floats, a plaza and landside work on University Avenue and Seawall Drive.

Documents read:
- CEQAnet SCH 2025040995: `https://ceqanet.lci.ca.gov/Project/2025040995`; Draft EIR record
  `https://ceqanet.lci.ca.gov/2025040995/2`; Draft EIR (Feb 2026, 661 pp.)
  `https://ceqanet.lci.ca.gov/2025040995/2/Attachment/-QKY5z`; notice of availability
  `https://ceqanet.lci.ca.gov/2025040995/2/Attachment/LX2HZH`.
- City project page `https://berkeleyca.gov/node/9711`; Council consent item Sept 15, 2026
  `https://berkeleyca.gov/sites/default/files/2026-09-15%20Item%2012%20Grant%20Application%20Safe%20Routes.pdf`.
- WETA: project page `https://www.sfbayferry.com/project/berkeley-ferry-project/`; fact sheet (June 25, 2026)
  `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260625163056/Berkeley-Pier-Terminal-Project-Fact-Sheet_Final.pdf`;
  WETA-SEP26; WETA-FY27. PBA p. 40.

| field | official value | source | quote |
|---|---|---|---|
| components | pier ≤1,080 x 22 ft; breakwater ~400 x 15 ft | Draft EIR p. 57 (2-4) | "The proposed pier would be a maximum of 1,080 feet in length and would have a width of 22 feet." |
| floats | two 135 x 42 ft universal charging floats; one in the first phase | Draft EIR p. 61 | "In the first phase of the project, the City would implement one gangway and one float" |
| acres | 195.6 total acres; APNs 060-2445-001-00, 060-2527-001-01, 060-2527-002-00 | CEQAnet Draft EIR record | "Total Acres 195.6" |
| Draft EIR | received Feb 26, 2026; review Feb 27 to Apr 28, 2026 | CEQAnet; City page | "Public review of the Draft Environmental Impact Report concluded on April 28, 2026." |
| first notice | 45 days to April 13, 2026 (then extended) | NOA p. 3 | "April 13, 2026 (a 45-day public review period)" |
| streamlining | certified by the Governor under SB 149 | City page | "has been certified as a transportation project by the Governor under Senate Bill No. 149" |
| Final EIR | to Council fall 2026; 60% design, 90% due fall 2026 | Sept 15, 2026 item p. 3 | "The Final EIR is anticipated to be considered by Council in Fall, 2026." |
| cost | $105.8M (60% design); construction funding not identified | Sept 15, 2026 item p. 2 | "The current construction cost estimate for the entire Project is $105.8M" |
| cost (WETA) | $104M: $79M pier and terminal, $25M plaza and landside; $11M secured | WETA fact sheet | "estimated to cost a total of $104 million" |
| design/EIR funding | SCC $2.96M (Res. 70,629); ACTC $5.139M (Res. 70,950); WETA up to $3M RM3 (Res. 71,325) | Sept 15, 2026 item pp. 1-2 | — |
| grant | application for up to $25M RM3 SR2TBT for landside work (due Oct 5, 2026) | Sept 15, 2026 item p. 1 | "for up to $25,000,000 for construction of portions of the landside elements" |
| ridership | > 1,000 average weekday passengers | WETA fact sheet | "projected to serve over 1,000 average weekday passengers" |
| regional plan | Berkeley-SF service incl. new terminal, $124M capital, 2025-2035 | PBA p. 40, 25-T11-164 | "including a new terminal in Berkeley" |
| WETA status | Draft EIR Feb 2026; Final EIR certification anticipated fall 2026 | WETA-SEP26 capital report | "Final EIR certification anticipated in Fall 2026" |

Boundary: no GIS layer; the three CEQA parcels don't outline the site (one is a 2,000 m² sliver, one a large
water parcel). Traced from the Draft EIR's Figure 2-2, Project Site Location (PDF p. 54; embedded raster 3,059 x
2,202 px): north-up, scale bar 650 ft = 349 px, placed on the University Avenue/Marina Boulevard roundabout
(OpenStreetMap streets agree to about 5 m); the inset (the full 2.5-mile dredged channel) fitted to the main
frame by rigid trimmed ICP (RMS 4.5 m). 186 acres drawn against 195.6. Module:
`pipeline/bam_pipeline/sites/boundary_berkeley_pier_ferry.py`. Massing lead: Figure 2-5 (3D layout) and Figure
2-3; low structures, not drawn.

Press-only: none used.

## 3. redwood-city-ferry-terminal

Recommendation: **INCLUDE**, stage `entitlement`. The Port of Redwood City's terminal for San Francisco Bay
Ferry service to San Francisco and Oakland, on a 9.2-acre Port parcel at Redwood Creek and Westpoint Slough,
with a rezoning for future visitor-serving uses.

Documents read:
- CEQAnet SCH 2024041306: `https://ceqanet.lci.ca.gov/Project/2024041306`; Draft EIR record
  `https://ceqanet.lci.ca.gov/2024041306/2`; Draft EIR, compiled (Sept 2026, 840 pp.)
  `https://ceqanet.lci.ca.gov/2024041306/2/Attachment/L59I-_`; notice of availability (Sept 17, 2026)
  `https://ceqanet.lci.ca.gov/2024041306/2/Attachment/e0miq4`.
- WETA: project page `https://www.sfbayferry.com/project/redwood-city-ferry-study/`; "Our Ferry Future"
  `https://www.sfbayferry.com/our-ferry-future/`; WETA-SEP26; WETA-FY27 PDF p. 14 (doc. p. 11). PBA p. 40.

| field | official value | source | quote |
|---|---|---|---|
| site | 9.2-acre parcel APN 054-300-380 | NOA p. 1; CEQAnet | "The project site encompasses a 9.2-acre parcel near the confluence of Redwood Creek and Westpoint Slough" |
| terminal | float with two berths, gangway, pile-supported access pier, parking lot, transit stops | NOA p. 1 | "berths for two ferry vessels at a pile-supported floating dock" |
| service | 320-passenger vessels; SF ~61 min, Oakland JLS ~71 min; 3-4 weekday peak trips each way | Draft EIR p. ES-7/ES-8 (PDF p. 20) | "one-way travel time of about 71 minutes … about 61 minutes" |
| rezoning | GI to General Commercial: hotel ≤3 stories, ≤180,000 sq ft; restaurants ≤20,000 sq ft; office ≤10,000 sq ft | NOA p. 2 | "a three-story hotel (maximum 180,000 square feet)" |
| hotel rooms | 100-200 rooms | CEQAnet Draft EIR record | "Other (100-200-room hotel,20,000 sf restaurant, parking,10k sf office)" |
| construction | ~4 years from 2027: 9 months fill, ~15 months terminal and access, 24 months visitor uses | Draft EIR p. ES-8 (PDF p. 20), Table 2-1 | "Project construction would span about four years and is estimated to start in 2027." |
| NOP | Apr 30, 2024 (review May 1-31, 2024); scoping May 15, 2024 | CEQAnet; NOA p. 2 | — |
| Draft EIR | NOA Sept 17, 2026; comments to Nov 2, 2026; meeting Oct 7, 2026 | NOA p. 2 | "ends at 5:00 p.m. on November 2, 2026" |
| review (CEQAnet) | Sept 23 to Nov 9, 2026 | CEQAnet record | (conflicts with the NOA; in `verify`) |
| WETA role | responsible agency; SMCTA funds environmental review | WETA-FY27 PDF p. 14 | "As the Lead Agency, the Port of Redwood City is preparing CEQA/NEPA-compliant environmental reviews supported through funding from the San Mateo County Transportation Authority." |
| regional plan | Oakland-Redwood City service incl. new terminal, $78M capital, 2036-2050 | PBA p. 40, 25-T11-165 | "including a new terminal in Redwood City" |

Boundary: County of San Mateo parcels (data.smcgov.org nr6j-72z7, Public Domain), APN 054300380 (9.4 acres drawn
against 9.2). The float extends into Redwood Creek and the Seaport Boulevard work is outside it. Massing lead:
Draft EIR Figure 2-7 (ferry terminal plan) and Figure 2-6 (conceptual full build-out); the hotel has no design.

Press-only: none used.

## 4. Harbor Bay Ferry Terminal Modernization (Alameda) — BORDERLINE

WETA-FY27 PDF p. 19: "A new, electrified ferry terminal north of the existing terminal will be constructed while
maintaining ferry service during construction of the new facility … The existing terminal will be demolished
once the new terminal is operational." Budget $38,137,042, of which $35,805,211 is future-year (capital table);
"This project is currently only partially funded by State and local grant sources." WETA-SEP26: basis of design
and Level 5 estimate done; "CEQA approach, project description and memo" next. Would tip to INCLUDE with a CEQA
filing and a site plan.

## 5. Vallejo Ferry Terminal Reconfiguration — EXCLUDE

CEQAnet SCH 2024051079 (`https://ceqanet.lci.ca.gov/Project/2024051079`): "reconfigure the existing Vallejo Ferry
Terminal … within the footprint of the existing ferry terminal and basin area"; IS/MND May 23, 2024, NOD July
16, 2024, CDFW streambed agreement NOD Sept 21, 2026. WETA-FY27: total budget $22,023,766; "replacement of
gangway, bridge/fixed pier and passenger float" to avoid dredging; design-build RFP fall 2026, award Dec 2026
(WETA-SEP26). A rebuild of an existing terminal, not a new or expanded one.

## 6. Larkspur Ferry Service and Parking Expansion (Golden Gate Ferry) — BORDERLINE

CEQAnet SCH 2024091190 (`https://ceqanet.lci.ca.gov/Project/2024091190`): NOP received Sept 30, 2024: "increasing
capacity by adding more high-speed boats, potentially creating a new ferry route to the foot of 16th Street …
and expanding Larkspur Ferry Terminal parking". District study page
(`https://goldengate.org/district/district-projects/larkspur-ferry-service-parking-expansion-study`): "Release of
Draft Environmental Impact Report – Date TBD". PBA p. 38, 25-T11-149, lists Larkspur-Mission Bay service, 2036-2050.
Service and parking at an existing terminal; no Draft EIR. (`goldengate.org` is the District's own site but isn't
in the host list; not needed since nothing was mapped.)

## 7. Treasure Island terminal electrification — EXCLUDE

WETA-SEP26 (July 2026 minutes): three-party MOU among WETA, TIMMA and TIDA approved (Resolution 2026-31); "The
total project cost is $6.8 million, which is fully funded"; "environmental clearance … via a statutory exemption
approved by SF Planning in 2025". Construction contract award due Nov 2026, groundbreaking Dec 2026; a modified
float by June 2027 and service by early FY2027/28 (WETA-FY27 PDF p. 17). It electrifies the existing Treasure Island
landing, which is part of `treasure-island`; worth a line in that record's next update.

## 8. Electrification of other existing terminals — EXCLUDE

From WETA-FY27 PDF pp. 17-19 and the capital table: Downtown SF Gate G universal charging float ($90.1M line; Gates E
and F unfunded); Seaplane Lagoon ($37.4M; completion end of 2027); Oakland Ferry Terminal Modernization ($40.9M;
"without significant identified funding"); Richmond ($4.2M; studies); Main Street ($11.9M); Central Bay
maintenance facility. None adds a terminal.

## 9. Vision-level ideas — EXCLUDE

- WETA's 2050 Service Vision (`https://www.sfbayferry.com/service-vision-and-business-plan/`): "expanding to 14
  routes … connections from Mission Bay and Treasure Island to the Ferry Building, Berkeley to San Francisco, and
  Oakland to Redwood City — and exploring innovative service models like short-hop routes … Vallejo/Mare
  Island". The REEF program page lists "Phase 4 – Long Runs: Vallejo, Carquinez Strait, Redwood City".
- Carquinez Strait: WETA's May 14, 2026 minutes (WETA-JUN26, PDF p. 38) record Board interest only: "referenced past
  interest from communities along the Carquinez Strait, including Benicia, Martinez, Hercules, Pittsburg, and
  Antioch." PBA's Hercules Hub (25-T11-170) is a Capitol Corridor rail station, not a ferry terminal. No official
  terminal project found for Martinez, Antioch, Pittsburg, Benicia or Hercules.
- South Bay, Foster City, Alviso: no official project found.
- Mare Island: an existing San Francisco Bay Ferry stop (select Vallejo trips), not new.

## 10. Recently completed — EXCLUDE

WETA's projects page (`https://www.sfbayferry.com/projects/`) lists as completed: Downtown San Francisco Ferry
Terminal Expansion, Main Street Alameda Ferry Terminal Refurbishment, Richmond Ferry Terminal, Central Bay and
North Bay Operations and Maintenance Facilities. Seaplane Lagoon opened for service July 1, 2021 (in
`alameda-point`). Treasure Island ferry service began March 1, 2022 (in `treasure-island`).
