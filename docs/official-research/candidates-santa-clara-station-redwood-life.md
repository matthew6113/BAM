# Official-source findings: Santa Clara Station Area Specific Plan and Redwood Life Precise Plan

Checked 2026-10-17. Two leads from the Oct 17 scan (`docs/upkeep/leads-2026-10-17.md`), added at Matthew's
request. Both are at the notice-of-preparation stage of a CEQA review, so each gets a boundary and no land use
or massing (no adopted plan, and no official land-use map yet).

How it was read: CEQAnet project and document pages and their attachments (`ceqanet.lci.ca.gov`, redirecting
to `files.ceqanet.lci.ca.gov`) were read directly; the notices of preparation were read in full as text and
their figures rendered. The City sites (`santaclaraca.gov`, `redwoodcity.org`) answer scripts with a 403 even
with a browser user agent, and headless Chromium can't reach them through this session's proxy; the agenda
systems (`santaclara.legistar.com`, `webapi.legistar.com`), the County parcel services (`data.sccgov.org`,
`data.smcgov.org`), the City of Santa Clara's map server and `planredwoodlife.org` are refused by the proxy.
So both boundaries are traced from the notices' figures rather than built from the parcels the notices list.
Local copies: `data/raw/docs/santa-clara-station-area-nop-2026-06.pdf` and
`data/raw/docs/redwood-life-nop-2025-08.pdf` (git-ignored; sha256 pinned in the boundary modules). Page
numbers are PDF pages.

URL shorthand:
- `SC-CEQA` = `https://ceqanet.lci.ca.gov/2026060462` (CEQAnet document page, NOP received 6/10/2026)
- `SC-NOP` = `https://ceqanet.lci.ca.gov/2026060462/Attachment/mtsQbf` (Notice of Preparation, June 12, 2026, 7 pp.)
- `SC-NOC` = `https://ceqanet.lci.ca.gov/2026060462/Attachment/M1Z8RU` (Notice of Completion form, 2 pp.)
- `RL-CEQA` = `https://ceqanet.lci.ca.gov/2025081015` (CEQAnet document page, NOP received 8/21/2025)
- `RL-PROJ` = `https://ceqanet.lci.ca.gov/Project/2025081015` (CEQAnet project page: "1 documents in project")
- `RL-NOP` = `https://ceqanet.lci.ca.gov/2025081015/Attachment/yselzM` (Notice of Preparation, Aug 22, 2025, 8 pp.)

No new official hosts are needed: every source is on `ceqanet.lci.ca.gov` (and one `vta.org` GIS layer). The
City project pages are `.gov` (Santa Clara) or not cited (Redwood City's `redwoodcity.org`; see below).

---

## Summary

| # | project | city | stage (date) | size (official) | recommendation |
|---|---|---|---|---|---|
| 1 | Santa Clara Station Area Specific Plan | Santa Clara | in entitlement: NOP June 12, 2026; comments to July 13, 2026 | ~244 acres; up to 8,300 homes, 2.1M sq ft office, 1.7M sq ft light industrial | **INCLUDE** as `santa-clara-station-area` (plan-scale, boundary only) |
| 2 | Redwood Life Precise Plan | Redwood City | in entitlement: NOP Aug 22, 2025; no Draft EIR on CEQAnet as of Oct 17, 2026 | ~84 acres; 2.731M sq ft life science (net +1.764M), 104-room hotel | **INCLUDE** as `redwood-life` (boundary only) |

---

## 1. santa-clara-station-area

| field | value | source | page | quote |
|---|---|---|---|---|
| lead agency, plan | City of Santa Clara; a specific plan (SCSASP) with a Draft Program EIR | SC-NOP | 1 | "The City of Santa Clara (lead agency) will prepare a Draft Environmental Impact Report (EIR) for the proposed Santa Clara Station Area Specific Plan (SCSASP)." |
| NOP date, comment period | June 12, 2026; comments to July 13, 2026 (5 p.m.) | SC-NOP | 1 | "the NOP public review period will begin on June 12, 2026, and end on July 13, 2026" |
| scoping meeting | June 29, 2026, 6:00-7:30 p.m., Zoom | SC-NOP | 2 | "June 29, 2026 6:00 p.m. to 7:30 p.m. Zoom Webinar" |
| project web page | santaclaraca.gov specific plans page | SC-NOP | 2 | "Project related documents, including this NOP, can be found on the project webpage: https://www.santaclaraca.gov/our-city/departments-a-f/community-development/planning-division/specific-plans/santa-clara-station-focus-area-plan" (the PDF breaks the URL at "planning-division") |
| area, location | ~244 acres around the Santa Clara Transit Station | SC-NOP | 2 | "The SCSASP project area is comprised of approximately 244 acres of properties bounded by De La Cruz Boulevard, Reed Street, and Martin Avenue to the northeast, and Franklin Street and El Camino Real to the southwest. Located at the center of the SCSASP area is the Santa Clara Transit Station, which is served by Caltrain, Altamont Commuter Express, and Santa Clara Valley Transportation Authority bus service." |
| background | General Plan focus area | SC-NOP | 2 | "The City of Santa Clara 2010-2035 General Plan, adopted November 2010, envisions transforming the SCSASP area as a gateway into the City. The Santa Clara Station Focus Area is planned for mixed use, transit-oriented development, including a central roadway, or "main street"" |
| program | 8,300 homes; 2.1M sq ft office; 1.7M sq ft light industrial; 105,060 sq ft institutional; 134,920 sq ft retail; 19.5 acres open space | SC-NOP | 2 | "The proposed SCSASP would include up to 8,300 residential units, 2.1 million square feet of commercial office, 1.7 million square feet of light industrial, 105,060 square feet of institutional land uses, 134,920 square feet of retail, and 19.5 acres of open space." |
| program-level EIR | no specific development projects | SC-NOP | 5 | "The EIR is intended to be a program-level document ... No specific development projects are being considered at this time." |
| jobs | 10,800 | SC-CEQA | — | "Total Acres 244 Jobs 10800" |
| present land use | ten existing General Plan designations | SC-CEQA | — | "Present Land Use Low Density Residential, Medium Density Residential, High Density Residential, Very High Density Mixed Use, Neighborhood Mixed Use, Public/Quasi Public, Community Mixed Use, Regional Mixed Use, Regional Commercial, Light Industrial." |
| parcels | about 190 APNs (books 224, 230, 269) | SC-CEQA | — | "Other Location Info 224-01-017, 230-05-005, ..." (full list on the page) |
| centre | 37°21'9.8"N 121°56'11.1"W | SC-CEQA | — | "Location Coordinates 37°21'9.8"N 121°56'11.1"W" |
| NOC | Specific Plan; residential 8,300 units; commercial 134,920 sq ft; industrial 1.7 million; educational 105,060 sq ft | SC-NOC | 1 | "Local Action Type: ... Specific Plan"; "Residential: Units 8,300"; "Educational: 105,060 sq. ft." |
| documents in project | the NOP only (plus Caltrans and NAHC comment letters) | SC-CEQA | — | attachments: NOP Notice, NOP Form, NOP, NOC, "2026060462_DOT Comment", "2026060462_NAHC Comment" |

Lead figures checked: all correct (244 acres, 8,300 homes, 2.1M office, 1.7M light industrial, 134,920 retail,
19.5 acres open space, NOP June 12, 2026, SCH 2026060462). The NOP itself is the City's; CEQAnet logged it
received June 10.

**Boundary.** Traced from SC-NOP Figure 2, Vicinity Map (p. 4): a vector map on an Esri street base map with
the "Project Boundary" as black dashes (0-5,000 ft scale bar). The street pixels (white streets and yellow
arterials) were thinned and fitted to OpenStreetMap street centrelines (Overture) by trimmed ICP from the De
La Cruz Boulevard / Coleman Avenue junction: 11.64 m per PDF point, rotation 1.0°, trimmed RMS 13.5 m over
the closest 60% of 32,555 street pixels (median 19.9 m). The dashes were read from the PDF, joined across their
gaps and the line's centre taken. The line crosses itself where a small lobe south of The Alameda (east of
Santa Clara University) joins the main area; both are kept. **208 acres as drawn** against the NOP's 244 acres
of properties: the vicinity map is small-scale (the dashed line is ~18 m wide on the ground) and generalised,
so the boundary is `approximate`. A parcel-exact boundary would be the union of the CEQAnet APNs in the Santa
Clara County parcel layer (`data.sccgov.org` `ubcd-cewv`, used for `related-santa-clara`), once that host can
be reached from the pipeline.

**Boundary update (Oct 17, later).** `data.sccgov.org` became reachable. The CEQAnet record's "Other Location
Info" lists 185 APNs; 174 are in the County's FY 2026 parcel layer (`ubcd-cewv`, updated Aug 26, 2026). The 11
that aren't: 230-05-045, -049, -050, -078, -096 (no clear successor), 230-59-001, -002, 230-60-009, 230-61-001
(re-mapped on the same assessor's pages; the successors inside the NOP's Project Boundary and the City of Santa
Clara, 230-59-008, -009, 230-60-010 and 230-61-006, are added; 230-61-002, 230-59-004, -005 and others lie mostly
in San José or outside the line and are left out) and 269-16-000, 269-60-000 (condo common-area numbers). The
boundary is now the union of those 178 parcels joined over the streets by a 25 m closing: **249.4 acres**
(the listed parcels alone close to 244.1 acres; the parcels without streets are 219.6). Kept `approximate`:
the list fits the NOP's written bounds ("De La Cruz Boulevard, Reed Street, and Martin Avenue to the northeast
and Franklin Street and El Camino Real to the southwest") and its 244 acres, but differs from Figure 2 at the
edges: it takes in residential blocks along Franklin, Benton, Alviso, Fremont and Harrison streets west of the
dashed line, a Santa Clara University parcel (230-08-079, 514 Franklin Street, 11.7 acres), parcels at
1775-1885 De La Cruz Boulevard and 1709 Grant Street, and two San José parcels on Campbell Avenue (230-13-011,
230-14-026) that the line crosses; Figure 2 in turn takes in the street and airport-edge strips beyond Martin
Avenue. Against the traced outline: 72.6 acres only in the parcels, 31.4 acres only in the trace, up to about
300 m apart (Hausdorff). An overlay of OpenStreetMap streets on the NOP figure also shows its base map is
generalised by tens of metres, so the figure can't settle the edges.

**Land use.** None. The plan is at the NOP stage and the NOP maps no land-use concept; the land-use
alternatives and task force materials are on the City page, which couldn't be read.

**Overlap with existing records.**
- `related-santa-clara`: no overlap. That site is next to Levi's Stadium, about 6 km north; the plan area is
  around the Santa Clara Caltrain station south of the airport.
- `bart-silicon-valley-phase-2`: its at-grade tracks (the "Santa Clara and Newhall Yard (above ground)"
  segment) and its Santa Clara station point (-121.9334, 37.3533, from VTA's station layer) lie inside the
  plan area; the station is about 270 m from the CEQAnet centre point. The line's 60 m corridor boundary covers
  about 15% of the plan area. The Newhall Yard maintenance facility is to the southeast, outside the plan area.
- `cahsr-sf-sj`: its corridor along the Caltrain tracks crosses the plan area (about 14% of it).
- Neither is a site-project overlap: a line project's corridor runs through a city's plan area, as Diridon
  station sits beside `downtown-west`. Recommendation: include the plan as its own record (it adds 8,300 homes
  and 3.8M sq ft of jobs space that the BART record doesn't count), and say in its notes that the BART station and
  tracks run through it.
- `downtown-west`: about 2.7 km away; no overlap.

**Left out.** The 2010 General Plan's focus-area numbers (a search snippet quotes "approximately two million
net new square feet of commercial uses and 1,650 housing units" from a santaclaraca.gov PDF that couldn't be
opened). Any affordability requirement (none published). The City project page's documents.

## 2. redwood-life

| field | value | source | page | quote |
|---|---|---|---|---|
| lead agency, applicant | City of Redwood City; Longfellow Real Estate Partners | RL-NOP | 1 | "From: City of Redwood City, Lead Agency Applicant: Longfellow Real Estate Partners (Longfellow)" |
| NOP date, scoping, comments | Aug 22, 2025; scoping meeting Sept 2, 2025, 6 p.m., Council Chambers; comments by Sept 22, 2025 | RL-NOP | 1 | "send written comments ... by September 22, 2025"; "public Scoping Meeting on September 2, 2025, at 6:00 p.m. in person at the Council Chambers" |
| plans online | planredwoodlife.org | RL-NOP | 1 | "The current project plans may be viewed on-line at: https://www.planredwoodlife.org/." |
| site | 800, 1400, 1600, 3400 Bridge Parkway; ~84 acres; four APNs | RL-NOP | 2 | "located at 800, 1400, 1600, and 3400 Bridge Parkway in Redwood City, generally located between Belmont Slough and Marine Parkway. The project site totals approximately 84 acres and consists of four parcels (Assessor's Parcel Numbers [APNs]: 095-012-220, -450, -460, and -150)." |
| existing | 20 two-story buildings, 967,680 sq ft | RL-NOP | 2 | "the Redwood LIFE office park, which consists of 20, two-story buildings, totaling 967,680 square feet of research and development office and life science uses" |
| history | acquired 2019; preliminary application Apr 2021; formal application June 2022; City-led precise plan July 2023 | RL-NOP | 3 | "Longfellow ... acquired the project site in 2019. In April 2021, they submitted a preliminary application, and in June 2022, they submitted a formal planning application"; "In July 2023, the City Council initiated a process to prepare a City-led Precise Plan ..." |
| Alternative 2 | the project under study is the resubmitted application matching the City's alternative | RL-NOP | 3 | "Longfellow withdrew their original planning application and resubmitted a new project application consistent with the City's project alternative ("Alternative 2"), hereinafter referred to as the project." |
| entitlements | repeal Westport Specific Plan; adopt precise plan; rezone | RL-NOP | 3 | "The project includes repeal of the existing Westport Specific Plan and the adoption of the new Precise Plan to replace it. ... the property would be rezoned to precise plan zoning." |
| program | 11 life science buildings, ~2.731M sq ft (net +1.764M); ~20,000 sq ft amenity center; ~104-room hotel; four garages | RL-NOP | 3 | "construct 11 life science buildings totaling approximately 2.731 million square feet (a net increase of 1.764 million square feet compared to existing conditions), an approximately 20,000 square-foot community amenity center within one of the life science buildings, an approximately 104-room hotel, and four parking garages" |
| heights | 5-6 stories, ~100 ft roof (~120 ft screens); hotel 5 stories, ~85 ft (~95 ft); garages 5-8 levels, ~77 ft | RL-NOP | 3 | "range from five- to six-stories tall with a maximum roof height of approximately 100 feet (and approximately 120 feet to the top of the mechanical equipment screening)"; "The parking garages would be five- to eight-levels tall, with a maximum height of approximately 77 feet." |
| open space | ~42.4 acres, 38.7 acres POPA | RL-NOP | 3 | "a total of approximately 42.4-acres of open space throughout the project site, including 38.7-acres of privately-owned, publicly-accessible (POPA) open space" |
| sea level rise | levee improvements on Belmont Slough | RL-NOP | 3 | "construct sea-level rise improvements along the existing levee on Belmont Slough" |
| community benefits | affordable housing contributions, SLR, TDM, open space, amenity center, sustainability, childcare, union labor, Bay Trail gap | RL-NOP | 4 | "contributions towards the community benefits such as affordable housing, sea-level rise resiliency, transportation demand management program, open space, community amenity center, sustainability, childcare, union labor, and bay trail gap improvements" |
| site plan | Figure 4, Conceptual Site Plan | RL-NOP | 8 | "Source: Hellmuth, Obata & Kassabaum, Inc., August 5, 2025." |
| status | only the NOP is on CEQAnet | RL-PROJ | — | "1 documents in project ... NOP City of Redwood City 8/21/2025 Redwood Life Precise Plan" |

Lead figures checked: 84 acres, the four Bridge Parkway addresses, 11 buildings and 2.731M sq ft, NOP Aug 2025
(SCH 2025081015) are right. The lead's "the EIR is reported to study a reduced Alternative 2" is slightly off:
per the NOP, Alternative 2 is the project itself (Longfellow resubmitted to match it), not an alternative to
it. No Draft EIR: CEQAnet lists only the NOP (checked Oct 17, 2026), so the "early summer 2026" expectation
didn't happen. The press reports a delay (Redwood City Pulse, Sept 17, 2026; not opened here).

Size test: 2.731M sq ft gross on a defined 84-acre site (1.764M net new) clears the 1M sq ft bar either way.
The lead suggested waiting for the Draft EIR; Matthew's add list includes it, and the NOP is an official,
specific project description, so it's added at `entitlement` with the Draft EIR as the next milestone.

**Boundary.** Traced from RL-NOP Figure 3, Aerial Photograph and Surrounding Area (p. 7): black vector dashes
over an aerial photo (Google Earth, photo date April 2022; 0-1,400 ft scale bar). The photo was fitted to
OpenStreetMap building footprints (Overture) with `line_georef.register_buildings`: 3.27 m per PDF point,
rotation 0.48°, RMS 2.77 m over 53 tile control points. The dashes were read from the PDF and closed as for
Santa Clara. **81.9 acres as drawn** against the NOP's 84 (the line follows the Belmont Slough levee and
Marine Parkway). `approximate`. A parcel-exact line would be the County of San Mateo parcels for the four APNs
(`data.smcgov.org` `nr6j-72z7`, used for `redwood-city-ferry-terminal`), once that host can be reached.

**Boundary update (Oct 17, later).** `data.smcgov.org` became reachable. The four APNs are all in the County
layer (095-012-150 at 3400, -220 at 800, -450 at 1400 and -460 at 1600 Bridge Parkway); their union is
**84.2 acres** against the NOP's 84, and is now the boundary (`official`). The traced outline (81.9 acres)
lies within 34.7 m of it (Hausdorff, at the southern tip by Bridge Parkway); 2.7 acres are only in the
parcels (mostly along the Marine Parkway edge), 0.4 acres only in the trace.

**Massing / land use.** None for now. Figure 4 (p. 8) is a conceptual site plan of the 11 buildings, garages
and hotel with floor areas and story counts, by the applicant's architect, but the precise plan's development
standards aren't published and the site plan may change in the Draft Precise Plan. Draw massing from the Draft
Precise Plan (or its EIR project description) when it is out.

**Left out.** The press accounts of when the Council and Planning Commission chose Alternative 2 (a March
joint study session, year not stated in what could be read) and of the 2026 schedule slip: in `reported`.
`planredwoodlife.org` (named by the NOP for current plans; who runs it is unknown and the host is refused
here). Redwood City's own pages on `redwoodcity.org` (403 to scripts; `.org`, not in `official.ts`).
