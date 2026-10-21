# Official-source findings: SF Railyards (Caltrain Fourth and King railyard)

Checked 2026-10-21. Matthew asked on 2026-10-21: "I want to include the potential redevelopment of
Caltrain's railyards near Mission Bay as well." Mapped as `sf-railyards`.

How it was read: CEQAnet's record and its three attachments (the notice of preparation read in full as
text, its figures as images), the Planning Department's SF Railyards program page, Rail Alignment and
Benefits (RAB) page, environmental review documents listing, 2022 fact sheet and Oct 2022 community
meeting slides, and DataSF's Planning Department records and parcels were read directly. Not reachable
from this session on Oct 21: `www.caltrain.com` and `caltrain.com` (proxy refused; Caltrain Board packets
unread), `www.sfcta.org`, `citypln-m-extnl.sfgov.org` (the Planning Department's document server, which
holds the Jan 9, 2025 Planning Commission staff report and the NOP copies linked from sfplanning.org) and
`default.sfplanning.org` for the Dec 2024 "Railyards Summary Memo". Press and developer pages
(sfyimby.com, sfstandard.com, railyards-sf.com) were also unreachable, so nothing from them was read or
recorded. Local copies are in `data/raw/docs/sf-railyards-nop-2026-09.pdf` (cached by the massing module).

URL shorthand:
- `CEQA` = `https://ceqanet.lci.ca.gov/2026091295` (CEQAnet record, SCH 2026091295)
- `NOP` = `https://ceqanet.lci.ca.gov/2026091295/Attachment/tPsmWg` ("SF Railyards NOP Public_Sept2026_ADA",
  32 pp., sha256 `049ffb000b0bd9a8b34d363cb676683746c3feef9187c4056e113c24444c598c`)
- `NOA` = `https://ceqanet.lci.ca.gov/2026091295/Attachment/urQr08` (notice of availability, 5 pp.)
- `PRJ` = `https://data.sfgov.org/resource/qvu5-m3a2.json?record_id=2026-002123PRJ` (DataSF, Planning
  Department Records – Projects)
- `DVA` / `ENV` = `https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-002123DVA` / `...ENV`
  (DataSF, Planning Department Records – Non-Projects)
- `PROG` = `https://sfplanning.org/project/sf-railyards-planning-program` (sfplanning.org/railyards redirects here)
- `ERD` = `https://sfplanning.org/environmental-review-documents?title=railyards`
- `FACT` = `https://sfplanning.org/sites/default/files/documents/citywide/railyardsprojects/railyardsprojects_factsheet.pdf`
- `MTG` = `https://sfplanning.org/sites/default/files/documents/citywide/railyardsprojects/railyardsproject-community-mtg-presentation-100522.pdf`
- `RAB` = `https://sfplanning.org/rab`

No new official hosts were needed (CEQAnet, sfplanning.org and DataSF's `.gov` hosts are accepted).

## Is it a real, officially documented redevelopment? Yes, in environmental review

It is a filed private development application with an EIR under way, not only a study:

| what | value | source, page | quote |
|---|---|---|---|
| application | record 2026-002123PRJ, opened 2026-03-11, "Under Review", applicant J. Abrams Law, P.C., planner Mat Snyder, environmental document "Environmental Impact Report" | `PRJ` | "The proposal is to redevelop the existing Caltrain station and railyards at 4th and King Streets to create a multi-phased, mixed-use, transit-oriented development with up to 7.8 million square feet of vertical development above grade. The project would reconfigure and modernize the existing rail infrastructure on the site and would be subject to a development agreement with the city." |
| project name, address | "RAILYARDS PROJECT - 700 4TH STREET", block 8700 lot 001 | `PRJ` | `project_name`, `project_address` "700 04TH ST 94107" |
| development agreement | 2026-002123DVA, opened 2026-04-15, "Submitted", applicant Prologis 4th & King LLC | `DVA` | `applicant_org` "Prologis 4th & King LLC" |
| environmental record | 2026-002123ENV, opened 2026-03-16, planner Ryan Shum | `ENV` | — |
| NOP | issued Sept 30, 2026; comments to Oct 30, 2026 | `NOP` p. 1 | "Date: September 30, 2026 / Comment Deadline: October 30, 2026 / Case No.: 2026-002123ENV / Project Title: Railyards Mixed-Use Development Project" |
| scoping meeting | Oct 14, 2026, 5:30 p.m., 49 South Van Ness Ave, Room C | `NOP` p. 1; `ERD` | "An in-person public scoping meeting will be held at 5:30 p.m. on October 14, 2026, at 49 South Van Ness Avenue, Room C (first floor)" |
| SCH number, state review | 2026091295; state review 9/30–10/29/2026; public review 10/1–10/30/2026 | `CEQA` | "Document Type NOP - Notice of Preparation of a Draft EIR Received 9/30/2026" |
| local actions | general plan amendment, rezone | `CEQA` | "Local Actions General Plan Amendment, Rezone" |

Stage: **in entitlement** (the map's "Formal review underway: EIR, specific plan, hearings, land deal"),
the same treatment as `santa-clara-station-area` at its NOP. It is more than "proposed" (an application,
a development agreement application and an NOP of an EIR exist) and has no approvals.

Earlier official steps (context, not stages):
- `RAB`: the Planning Department's Rail Alignment and Benefits Study, component 2: "Railyard
  Reconfiguration/Relocation This component considers reknitting the fabric of the City by modifying or
  relocating some or all of the activities at the 4th/King Railyard." Final report: "Rail Alignment and
  Benefits Study: Final Executive Summary Report September 2018 (Planning Department)".
- `MTG` (Oct 5, 2022, Caltrain, Prologis and SF Planning), slides "Background": "Caltrain has a perpetual
  easement primarily on the surface of the site + a minor height above the site", "Redevelopment has been
  discussed for 20 Years", and "Caltrain and Prologis are engaged in a Preliminary Business Case (PBC)
  process to analyze multiple concepts for operational, engineering, and financial feasibility at the site."
- `FACT` (2022): "The SF Railyards Project envisions the Caltrain railyards at 4th and King as a regional
  transit center with a new rail station, added Caltrain service, and neighborhood with housing, office and
  public spaces." Partners: Prologis "Railyards site owner, development lead"; Caltrain "Train corridor
  operator and owner"; SF Planning "City's lead for planning, design and outreach"; OEWD "City's lead
  development partner".
- `PROG`: "The SF Railyards is a 20-acre site ... between 4th, King, 7th, and Townsend Streets, and functions
  as Caltrain's northern terminus as well as an active service and maintenance yard. Prologis owns the
  underlying land, and Caltrain holds a perpetual easement to operate rail on the site." Lists "Planning
  Commission Hearing January 9, 2025 – Informational Presentation" (staff report on
  citypln-m-extnl.sfgov.org, unread).
- DataSF also lists an earlier City record, 2023-000384PRJ "Railyards Development" (2023-000384CWP "Railyards
  Area Design and Development", opened 2023-01-12; 2023-000384DVA "Railyards Site DA", opened 2024-04-01).
  How it relates to the 2026 application isn't stated (left in `verify`).

## Site and boundary

| what | value | source, page | quote |
|---|---|---|---|
| parcels | 8701/003, 8701/004, 8700/001, 8703/005 | `NOP` p. 1 | "Blocks/Lot Nos.: 8701/003, 8701/004, 8700/001, and 8703/005" |
| area | 18.63 acres | `NOP` p. 1; `CEQA` "Total Acres 18.63" | "Site Area: 18.63 acres" |
| bounds | Townsend, Fourth, King, Seventh | `NOP` p. 2 | "generally bounded by Townsend Street to the north, Fourth Street to the east, King Street to the south, and Seventh Street to the west (see Figure 1)" |
| existing zoning | Eastern Parcels (8701/003, /004) MB-O, 110 ft; Western Parcels (8700/001, 8703/005) Mission Bay North Redevelopment Plan, Public Facility District, Height Zone HZ-1b | `NOP` p. 6 | "Block/ Lots 8700/001 and 8703/005, referred to as the Western Parcels, are within the Mission Bay North Redevelopment Plan and Mission Bay North Public Facility District and Height Zone HZ-1b ... Block/Lots 8701/003 and 8701/004, referred to as the Eastern Parcels, are within the MB-O (Mission Bay Office) Use District and 110 Height and Bulk District." |
| offsite yard | not sited | `NOP` p. 2 | "The location of the offsite train storage and maintenance facility has not yet been determined except that it likely will be in proximity to the existing Caltrain corridor between the existing Railyards site at Fourth and King streets and the San Francisco International Airport." |

Boundary drawn: the four lots in DataSF Parcels – Active and Retired (`acdm-wktn`, ODC-PDDL), all active,
unioned: **18.6 acres**, matching the notice's 18.63 acres and its Figure 1 (p. 3). Accuracy: official.
`pipeline/bam_pipeline/sites/boundary_sf_railyards.py` → `data/boundaries/sf-railyards.geojson`. The
offsite yard isn't drawn. Checked over OpenStreetMap streets (scratchpad plot): the outline runs along
Townsend from Fourth to Seventh, down Fourth to King and along the King Street/I-280 ramps to the tip on
Seventh, as Figure 1 shows.

## Program (official, NOP)

| what | value | source, page | quote |
|---|---|---|---|
| scenarios, totals | 7,820,390 sq ft (Max Commercial) to 7,839,210 sq ft (Max Residential), excluding below-grade parking, loading and support | `NOP` p. 2 | "would range from 7,820,390 square feet (Maximum Commercial Scenario) to 7,839,210 square feet (Maximum Residential Scenario)" |
| Max Commercial | 1,765 homes (1,765,910 sq ft), 5,638,120 sq ft commercial, 172,660 sq ft retail | `NOP` p. 2; Table 1 p. 8 | "The Maximum Commercial Scenario proposes the development of up to 1,765 residential units totaling up to 1,765,910 square feet, along with up to approximately 5,638,120 square feet of commercial space and up to approximately 172,660 square feet of retail space." |
| Max Residential | 5,834 homes (5,834,800 sq ft), 1,589,980 sq ft commercial, 159,970 sq ft retail | `NOP` p. 2; Table 2 pp. 9–10 | "the Maximum Residential Scenario, proposes the development of up to 5,834 residential units totaling up to approximately 5,834,800 square feet; with up to approximately 1,589,980 square feet of commercial space; and up to approximately 159,970 square feet of retail space" |
| "commercial" | office, hotel, lab, life science | `NOP` p. 8, note 7 | "“Commercial Uses” includes general office, hotel, laboratory, life science, and other uses." |
| station hall | 19,560 sq ft on Block 1 | `NOP` p. 2 | "the new 19,560-square-foot Caltrain Station Hall would be located in Block 1" |
| rail | new tunnel, two tracks, one platform, station about 60 ft below grade | `NOP` p. 2 | "would construct a new Caltrain tunnel (Caltrain Tunnel) with two below-grade railroad tracks and one service platform, terminating at a new, reconfigured Caltrain Station below the project site. The Caltrain Station would be approximately 60 feet below grade." |
| open space | 3.73 acres (3.5 Fifth Street Variant; 4.3 At-Grade Rail Variant) | `NOP` p. 4 | "approximately 3.73 acres of publicly accessible open space (or 4.3 acres under the At-Grade Rail Variant and 3.5 acres under the Fifth Street Variant)" |
| heights | 350 to 855 ft; Eastern Parcels 400–855, Western 350–450 | `NOP` pp. 4, 7 | "The proposed rezoning would modify the existing height limits to between 350 and 855 feet across the project site." / "The existing onsite height limit of 110 feet on the Eastern Parcels would be modified to allow heights ranging from 400 feet to 855 feet, and the existing onsite height designation HZ-1b ... on the Western Parcels would be modified to allow heights ranging from 350 feet to 450 feet." |
| construction | 2029 to 2042; Phase A and Development Phase 1 by end of 2035 | `NOP` pp. 4, 26 | "The EIR will analyze a construction period assumption of approximately 13 years, from 2029 to 2042." / "is expected to be complete by the end of 2035 ... All rail infrastructure and development are anticipated to be complete by 2042." |
| approvals | Board: general plan, planning code and zoning map amendments, development agreement, Mission Bay North Redevelopment Plan amendments; Caltrain: real estate agreement, rail modifications | `NOP` pp. 27–28 | "Approval of a development agreement." / "Approval of amendments to the Mission Bay North Redevelopment Plan." / "Approval of any real estate agreement with Prologis 4th & King LLC." |

Recorded in the record as the scenario maximums (homes 5,834; commercial 5,638,120 sq ft; retail 172,660
sq ft; open space 3.73 acres), with the notes saying they are alternatives that don't add up, as
`tanforan` does. No affordable housing figure is given in the NOP (searched: "affordab" appears nowhere).
The CEQAnet summary's "Commercial (153k-563k square Feet)" is a typing slip for the NOP's 1.59–5.64 million
sq ft and isn't used.

## Massing (proposed, illustrative)

`NOP` Figure 3, Height District Plan (PDF p. 13; "SOURCE: Prologis 4th and King LLC, 2026"; a 500-ppi
raster), legend Max 855', 625', 550', 500', 450', 400', 350' and "Max 575' - Second Tower"; note "MAX
855' FOR BLOCK 1 / MAX 575' FOR SECOND TOWER". Blocks: 1 (1A and 1B) 855 ft, 2A 500, 2B 625, 3A 500, 3B
400, 3C 550, 4 350, 5 450. The figure agrees with the text's ranges (p. 7). Phases (pp. 23–26): Block 1
Phase 1.1, Block 5 Phase 1.2, Block 2 Phase 2.1, Block 3 Phase 2.2, Block 4 Phase 2.3.

Drawn in `pipeline/bam_pipeline/sites/massing_sf_railyards.py` → `data/massing/sf-railyards.geojson`:
legend colours classified inside the dashed project boundary, registered by a similarity fit of the
boundary's four corners to the DataSF parcel union (RMS 0.1 m; scale 0.504 m/px at 200 dpi, rotation
45.2°), checked against OpenStreetMap's Townsend crossings of Fourth (1.7 m) and Fifth (2.4 m) streets,
then clipped to the parcels. Every block is an illustrative envelope at its proposed limit, stage "in
entitlement". The heights are proposed (not adopted) and are limits, not buildings; Block 1 would hold one
855-ft tower and a second of 575 ft, not an 855-ft block. Figure 3 labels Sixth Street "8th STREET" and
marks only the second tower's position (on 1A).

## Overlap with mapped projects

- `the-portal`: TJPA's separate project. `NOP` p. 4: "would construct a new tunnel (Portal Tunnel), two
  railroad tracks, and one service platform for the Fourth/Townsend Station underneath the portion of
  Townsend Street that runs next to the project site", note 3: "Portions of the Portal Project
  infrastructure would be constructed within and underneath the project site (not just under Townsend
  Street). However, no proposed project buildings would be constructed directly above the Portal Project
  infrastructure." Phasing (p. 23): "Completion of the proposed project would require two preconditions: the
  completion of the Portal Project ... and the construction of an offsite train storage and maintenance
  facility". The Portal's corridor outline overlaps the site by about 9.3 acres; fine for a line project.
- `cahsr-sf-sj`: shares the Caltrain corridor whose terminus this is; its corridor outline covers most of
  the yard (about 17.6 acres). No change.
- `mission-bay`: the Western Parcels are in the Mission Bay North Redevelopment Plan area (`NOP` p. 6), so
  the outlines overlap by about 7.9 acres; the project would amend that plan. Mission Bay's record isn't
  changed.
- `mission-rock` (about 390 m east, across Third Street and the channel) and `mission-bay-ferry-landing`
  (16th Street) don't touch the site.

## Left out, and why

- Press and developer figures (reported in search snippets: an "850-foot" tower, "up to 2,500 homes",
  "8 million square feet", "15- to 20-year" buildout, an April 2026 "complete application notice"): the
  pages couldn't be opened, so nothing goes in `reported`; the NOP's official figures supersede them anyway.
- Caltrain Board items (memoranda and a cooperation agreement with Prologis appear in search results) and
  the Jan 9, 2025 Planning Commission staff report: hosts unreachable; in `verify`.
- The Pennsylvania Avenue Extension (SFCTA) and the I-280 boulevard study: separate studies, not part of
  this application.
