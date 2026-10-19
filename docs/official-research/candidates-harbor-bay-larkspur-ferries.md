# Official-source findings: Harbor Bay and Larkspur ferry terminals

Checked 2026-10-19. Matthew asked on 2026-10-19 to "add the proposed ferries for farther down the line": the
two terminals he pre-approved on 2026-10-12 (docs/UPKEEP.md, "Pre-approved: add when ready"), now at their
current stage rather than waiting for their CEQA documents. This file follows
`candidates-ferry-terminals.md` (§4 Harbor Bay, §6 Larkspur, §9 vision ideas), which has the earlier reading.

How it was read: CEQAnet (project pages, document records, attachments and searches by lead agency and city)
was read directly today. Today the proxy refused connections to `www.sfbayferry.com`, WETA's CloudFront
document store, `goldengate.org`, `www.alamedaca.gov` and `alameda.legistar.com` (CONNECT 403; WebFetch can't
resolve them either), so WETA's Board packets and budget and the District's study page are quoted from the
local copies made on 2026-10-12 (`data/raw/official/ferry/`, git-ignored), and anything newer on those sites
couldn't be checked. Web searches (2026-10-19) found nothing newer for either project. Page numbers are PDF
pages unless a document page is given.

URL shorthand (as in `candidates-ferry-terminals.md`):
- `WETA-SEP26` = `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260921171636/b9252026aFULLLink.pdf`
- `WETA-MAY26` = the WETA Board packet for May 14, 2026 (local copy `b51426aFULLLink.pdf`; its CloudFront URL
  wasn't recorded on Oct 12 and couldn't be looked up today)
- `WETA-FY27` = `https://d262kwcyxl71on.cloudfront.net/wp-content/uploads/20260612202624/FY2027-Final-Budget.pdf`
- `PBA` = `https://planbayarea.org/sites/default/files/documents/2026-04/Final_Plan_Bay_Area_2050_Plus_Transportation_Project_List_Report.pdf`
- `LFEP-NOP` = `https://ceqanet.lci.ca.gov/2024091190/2/Attachment/9FEu4G` (sha256
  `8839ae049d667eb3d5c8a10038e3241dec4933d761838412e2cbaa32eafbb41a`, 9 pp.)

## Summary

| # | project | stage (official) | site figure | recommendation |
|---|---|---|---|---|
| 1 | Larkspur Ferry Service and Parking Expansion (Golden Gate Bridge, Highway and Transportation District) | `entitlement`: NOP Sept 30, 2024; EIR in preparation; Draft EIR "Date TBD" | yes: NOP Figure 2, Project Location | **ADD** as `larkspur-ferry-expansion`, boundary traced from Figure 2 (approximate) |
| 2 | Harbor Bay Ferry Terminal Modernization (WETA) | `proposed`: planning and preliminary engineering; "CEQA approach, project description and memo" in progress; no CEQA filing | **none** | **WAIT**: draft record ready, no boundary; add when WETA files its CEQA document or shows a site plan |
| 3 | 2050 Service Vision Tier 2 sites (Hercules, Martinez, Pittsburg, Antioch, Foster City, SF Southern Waterfront, Alameda Landing, Oakland Airport, SFO) | vision only | none | none added |

---

## 1. larkspur-ferry-expansion

Recommendation: **ADD**, stage `entitlement` (formal environmental review under way: the District issued the
NOP of a Draft EIR in 2024; the map stages NOP-only projects such as `redwood-life` and `santa-clara-station-area`
the same way). The Draft EIR, which Matthew's Oct 12 condition waited for, is still not out.

Documents read:
- CEQAnet project SCH 2024091190: `https://ceqanet.lci.ca.gov/Project/2024091190` (read 2026-10-19: one document,
  the NOP); NOP record `https://ceqanet.lci.ca.gov/2024091190/2`.
- The NOP with Figures 1 and 2 (`LFEP-NOP`); the notice of completion
  `https://ceqanet.lci.ca.gov/2024091190/2/Attachment/d8sisn`; state comment letters (CDFW
  `.../Attachment/09jVVd`, Caltrans `.../Attachment/33_rZ0`, State Lands `.../Attachment/FgThZk`, NAHC
  `.../Attachment/jg5XeF`).
- District study page `https://goldengate.org/district/district-projects/larkspur-ferry-service-parking-expansion-study`
  (local copy of 2026-10-12, `gg-lark.html`; unreachable today).
- `PBA` p. 38, 25-T11-149.

| field | official value | source | quote |
|---|---|---|---|
| lead agency | Golden Gate Bridge, Highway and Transportation District; also the applicant | CEQAnet NOP record | "Contact Types Lead/Public Agency / Project Applicant" |
| description (current) | service from 42 to up to 76 daily trips through 2050; landside access: parking, TDM, walking and cycling, transit and shuttles, SMART link | CEQAnet project page | "would increase ferry service incrementally based on demand from 42 daily trips to as many as 76 daily trips through 2050" |
| description (NOP) | more high-speed boats; possible new route to 16th Street (Mission Bay); parking on the main lot and/or the Country Mart north lot | `LFEP-NOP` p. 2 | "expanding Larkspur Ferry Terminal parking on the main terminal parking lot and/or the north parking lot located in the Country Mart shopping center across Sir Francis Drake Boulevard" |
| new route | potential, to the foot of 16th Street near Mission Bay and UCSF | `LFEP-NOP` p. 2 | "potentially creating a new ferry route to the foot of 16th Street" |
| constraints | trips capped at 42; site space-constrained with limited parking | `LFEP-NOP` p. 2 | "The number of ferry revenue trips per day is capped at 42." |
| NOP | received Sept 30, 2024; dated Oct 1, 2024; review Oct 1-30, 2024 | CEQAnet NOP record; `LFEP-NOP` p. 1 | "Received 9/30/2024"; "Public Review Period Start 10/1/2024 … End 10/30/2024" |
| scoping | Oct 15, 2024, 5-7 p.m., Drakes Landing Community Room, Greenbrae | `LFEP-NOP` p. 3 | "The scoping meeting will be held on October 15, 2024 from 5:00 to 7:00 p.m." |
| cross streets | Sir Francis Drake Blvd and Larkspur Landing Circle | CEQAnet NOP record | — |
| ridership (2019) | > 8,000 average weekday; 42 average daily crossings, seven ferries | District study page | "Average weekday ridership was over 8,000 passengers on a fleet of seven ferries that supported 42 average daily crossings." |
| parking | riders turned away several days a week, often before 10 a.m. | District study page | "ferry passengers arriving by car were turned away several days per-week, often before 10 am, due to a lack of parking" |
| outreach | 25 stakeholder interviews; open house May 2024; passenger survey Sept 2024; scoping open house Oct 2024 | District study page | "Community Open House – May 2024" |
| Draft EIR | not released; date TBD | District study page (Oct 12); CEQAnet (Oct 19: NOP only) | "Release of Draft Environmental Impact Report – Date TBD" |
| regional plan | GGT program incl. new Larkspur-San Francisco (Mission Bay) ferry, 30-min peak; Larkspur-Ferry Building frequency to 20-min peak; 2036-2050; $991M program (with express buses) | `PBA` p. 38, 25-T11-149 | "new ferry service between Larkspur and San Francisco (Mission Bay) (30 minute peak headways)" |
| size / cost | none official: no parking count, acreage or cost in the NOP | — | — |

Boundary: no GIS layer. Traced from `LFEP-NOP` Figure 2, Project Location (PDF p. 5): an aerial photo (tiled
JPEG strips, 0-600 ft scale bar) with four outlines, "Larkspur Ferry Terminal", "Main Parking Lot", "Overflow
Parking" and "Larkspur SMART Station". The outlines are picked by colour and filled; the photo is fitted to
OpenStreetMap building footprints (`line_georef.register_buildings`, at 2 px per point: 150 tiles, RMS 1.5 m,
max 4 m; scale within 0.1% of the scale bar; turned 1.5°, about the difference between State Plane zone III
and UTM grid north here, so the figure was drawn in State Plane). As drawn: terminal 1.8 acres, main lot 11.4,
overflow lot 1.1, SMART station 0.1 (in two pieces where the "NWP RR" label breaks its outline); 14.5 acres in
all. The parking aisles in OpenStreetMap fall inside the traced main lot. Accuracy `approximate`: it's a location
map for an NOP, not a site plan, and the Country Mart north lot the text names isn't outlined. The yellow
"Corte Madera Channel" line isn't drawn. Module: `pipeline/bam_pipeline/sites/boundary_larkspur_ferry_expansion.py`.
No massing: the parking design (surface lot or structure) isn't defined until the Draft EIR.

Not used (couldn't be read today): a Nov 20, 2025 District Board committee item authorizing a third amendment
to the environmental clearance and preliminary design contract with Jacobs Engineering Group
(`https://www.goldengate.org/assets/1/25/2025-1120-bocomm-no5-appracts3rdamendlfexpansproject.pdf`), and the
study overview handout (`https://goldengate.org/assets/1/6/02_overview_20241004_low-res.pdf`), which a search
snippet says expected the Draft EIR in late 2025 or early 2026 and project approval in late 2026 or early 2027.
Both are District documents and should be read for the next update.

Press-only: none used.

## 2. Harbor Bay Ferry Terminal Modernization — WAIT

Recommendation: **WAIT** (draft record prepared, no boundary). Stage would be `proposed`: WETA has budgeted and
is designing the project but has filed nothing under CEQA and holds no approvals.

What's new since Oct 12: nothing official found. CEQAnet has no Harbor Bay modernization filing (searches on
2026-10-19 by lead agency "Water Emergency Transportation Authority" and "San Francisco Bay Area Water Emergency
Transit Authority", and by city "Alameda" since May 2026). WETA's latest CEQAnet filings are a Vallejo streambed
NOD (Sept 21, 2026) and a Seaplane Lagoon electrification exemption (July 27, 2026). The one Harbor Bay CEQAnet
record, SCH 2024071234 (`https://ceqanet.lci.ca.gov/Project/2024071234`), is the California Energy Commission's
2024 exemption for its grant to an electric float and battery at the existing terminal, not the new terminal.
WETA's site, document store and the City of Alameda's site were unreachable today, so an October 2026 Board
packet couldn't be checked.

| field | official value | source | quote |
|---|---|---|---|
| scope | new electrified terminal north of the existing one, built while service continues; new fixed pier, security gate, gangway, piles, utilities, charging; grid connection to AMP near Harbor Bay Pkwy and Bay Edge Rd; existing terminal demolished after | `WETA-FY27` p. 19 | "A new, electrified ferry terminal north of the existing terminal will be constructed while maintaining ferry service during construction of the new facility." |
| work to date | FY2025/26 planning and preliminary engineering to pick the preferred option; FY2026/27 design and environmental and permitting approvals | `WETA-FY27` p. 19 | "In FY2026/27, the design will be advanced for the new terminal and electric distribution service along with the necessary environmental and permitting approvals." |
| funding | partly funded by State and local grants | `WETA-FY27` p. 19 | "This project is currently only partially funded by State and local grant sources." |
| budget | $38,137,042 total; $1,190,286 prior years; $1,141,545 FY2026/27; $35,805,211 future years | `WETA-FY27` capital budget table (Facility Electrification, Harbor Bay) | — |
| budget (June 30, 2026) | $36,731,737 total project budget; $382,132 spent in FY2025/26 | `WETA-SEP26` p. 39 | — |
| status | Basis of Design and Level 5 cost estimate done; geotechnical report done; "CEQA approach, project description and memo" and draft Section 106 report in progress | `WETA-SEP26` p. 19 | "Completed Basis of Design and Level 5 cost estimate for marine engineering" |
| milestone | Sept 2026: "Harbor Bay and Oakland, Initiate Resource Agency Permitting" (planned; not confirmed done) | `WETA-SEP26` milestones table | — |
| fleet plan | Harbor Bay electric capacity assumed in FY2034, marked unfunded | `WETA-SEP26` fleet plan | "the Terminal EV Vessel Capacity assumes electrification of the Harbor Bay terminal in FY 2034" |
| regional plan | frequency upgrades and ZEV conversion of existing WETA routes incl. Harbor Bay, 2025-2035 | `PBA`, 25-T11-166 | — |

Boundary: **no official site figure**. WETA's documents say only "north of the existing terminal"; the Sept 2026
terminals slide has no map, and no plan, figure or GIS has been published. Drawing a boundary around the
existing terminal would misplace a project whose point is to move it, and drawing one north of it would invent
a site. A project without a boundary isn't shown on the map (`tests/project.spec.ts`, "a project not yet on the
map"), so the draft record could go into the data now, but nothing would appear until a site exists.
Recommendation: wait for WETA's CEQA document (an exemption, IS/MND or EIR) or a Board item with a site plan;
the record then needs a boundary and the stage re-checked.

## 3. WETA 2050 Service Vision and REEF: newly sited terminals?

None. The Service Vision 2050 map (reproduced in a staff report in `WETA-MAY26`, PDF p. 118, "Figure 1. San
Francisco Bay Ferry Service Expansion Plan Map", "Source: San Francisco Bay Ferry") shows Tier 1 (proposed):
Mission Bay, Treasure Island, Berkeley, Redwood City (all already on the map or in `treasure-island`), and
Tier 2: Hercules, Martinez, Pittsburg, Antioch, Foster City, SF Southern Waterfront, Alameda Landing, Oakland
Airport and SFO, as dots on a diagram. The REEF fact sheet (Sept 2025) phases terminals as "Phase 4 – Long
Runs: Vallejo, Carquinez Strait, Redwood City". WETA's May 14, 2026 minutes record only Board interest in
Carquinez Strait communities (`candidates-ferry-terminals.md` §9). The one new capital line is "Mare Island
Facility Planning & Engineering", $290,000 of private funding for "preliminary project work on the Mare Island
electrification project" (`WETA-SEP26`, budget amendment, Sept 25, 2026): electrification of the existing Mare
Island stop. CEQAnet has no WETA filing for any new site. No official site exists for any of them.
