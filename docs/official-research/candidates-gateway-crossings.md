# Official-source findings: Gateway Crossings (Santa Clara)

Checked 2026-10-19. Matthew asked on 2026-10-19 to add **Gateway Crossings** as its own project, although it lies
inside the mapped `santa-clara-station-area` plan area. An earlier session had held it as borderline for that
reason (`candidates-south-bay-2026-10.md`, "Candidates named in the brief, and other leads").

How it was read. CEQAnet's project page and document pages for SCH 2017022066 (downloaded and read as text; the
handwritten notice of determination rendered with `pdftoppm` and read by eye); a CEQAnet CSV export of every
document with the City of Santa Clara as location (388 rows) or lead agency (177 rows), Jan 1, 2017 to Oct 19, 2026, searched
for "Gateway Crossing", "1205 Coleman", "Hunter Storm", "Rickabaugh", "Chastain", "230-46-069", "230-60-" and
"Coleman Ave"; the documents that turned up, read with `pdftotext -layout`; the Santa Clara Station Area Specific
Plan's CEQAnet record (SCH 2026060462) and notice of preparation; VTA's Santa Clara BART station page and fact
sheet; and Santa Clara County's open data (parcels `ubcd-cewv`, updated Aug 26, 2026; the lidar building
footprints `e8m9-vdfi`, flown in early 2020, too early to show the project). Local copies are in
`data/raw/official/gateway-crossings/` (git-ignored). Page numbers are PDF pages unless "doc p." is given.

Blocked this session: `santaclaraca.gov` (403, also through WebFetch), `santaclara.legistar.com`,
`webapi.legistar.com`, `hcd.ca.gov`, `geotracker.waterboards.ca.gov`, `smarts.waterboards.ca.gov`, `oeaaa.faa.gov`,
`public-gis-missioncity.opendata.arcgis.com`, `gis.vta.org`, `vtabart.org`, and the press sites `sfyimby.com` and
`berkadia.com`. So no council resolution, staff report, development agreement, approved plan set, permit or
press article was read.

URL shorthand (all `https://ceqanet.lci.ca.gov/` unless a full URL is given):
- `GC/1` = `2017022066` (NOP record, received Feb 22, 2017; no attachment: "The document was originally posted
  before CEQAnet had the capability to host attachments for the public.")
- `GC/2` = `2017022066/2` (Draft EIR record, received Apr 10, 2018; no attachment, same disclaimer)
- `GC/3` = `2017022066/3` (NOD record); `NOD` = `2017022066/3/Attachment/d5qjId` (4 pp., scanned; p. 1 the
  handwritten notice, p. 2 the County Clerk-Recorder receipt, p. 3 the CDFW fee receipt, p. 4 the County's CEQA
  document declaration; sha256 `7d905737…b148`)
- `HOTEL` = `2021030592/Attachment/4isyVj` (City of Santa Clara, Dual-Branded Hotel at Coleman and Brokaw, Initial
  Study and Mitigated Negative Declaration, March 2021, 187 pp.; sha256 `a543e1e4…207b`)
- `SCS` = `2026060462` (Santa Clara Station Area Specific Plan NOP record, "Other Location Info" lists 185 APNs);
  `SCS-NOP` = `2026060462/Attachment/mtsQbf`
- `VTA` = `https://www.vta.org/sites/default/files/2024-02/bsv_santa-clara-fact-sheet.pdf` (Santa Clara BART
  station fact sheet, PDF dated Feb 6, 2024, 2 pp.; sha256 `b5039c2f…d5b7`); the same text is on
  `https://www.vta.org/projects/bart-sv/phase-ii/santa-clara-station`
- `SCC` = `https://data.sccgov.org/d/ubcd-cewv` (Santa Clara County parcels)

## Hosts needed in `src/projects/official.ts`

None. Every source is on `ceqanet.lci.ca.gov`, `www.vta.org` or `data.sccgov.org`, all already accepted.

## Summary

| project | city | stage (date) | size (official) | recommendation |
|---|---|---|---|---|
| Gateway Crossings | Santa Clara | entitled (approved July 9, 2019) | 21.4 acres; 1,565 homes, 197,000 sq ft commercial incl. a 225-room hotel and 45,000 sq ft retail, two parks of ~2.6 acres | **INCLUDE** as `gateway-crossings` (Matthew's call), boundary only |

---

## gateway-crossings: INCLUDE

Recommendation: **INCLUDE**, stage `entitled`, boundary only. Over the 1,000-home bar, with its own approval
(EIR, vesting tentative map, development agreement). It sits wholly inside `santa-clara-station-area`, a plan in
environmental review that takes in its lots; Matthew decided to show it as its own project.

Documents read: GC/1, GC/2 and GC/3 pages and the CEQAnet project page (all text); NOD (all four pages); HOTEL
(pp. 1-3 and the pages that name Gateway Crossings: 21, 41, 70-72, 142 and 147); SCS page
(APN list) and SCS-NOP (pp. 1-2); VTA (p. 1) and VTA's station page; SCC (queries below).

| field | official value | source | verbatim quote |
|---|---|---|---|
| approval | City of Santa Clara (lead agency), July 9, 2019; EIR, mitigation, monitoring plan, SOC, findings | NOD p. 1; GC/3 | handwritten: "This is to advise that the City of Santa Clara ... has approved the above described project on July 9, 2019"; boxes ticked: "The project [will] have a significant effect", "An Environmental Impact Report was prepared", "Mitigation measures [were] made a condition", "A mitigation reporting or monitoring plan [was] adopted", "A statement of Overriding Considerations [was] adopted", "Findings [were] made"; GC/3: "Approved On 7/9/2019" |
| program | 1,565 homes; 197,000 sq ft commercial incl. a 225-room hotel and 45,000 sq ft retail; ~21.4 acres; two public parks ~2.6 acres; VTM and DA | NOD p. 1 (handwritten; GC/3 has a typed copy) | "GENERAL PLAN AND ZONING AMENDMENTS TO DEVELOP 1,565 RESIDENTIAL UNITS AND 197,000 SQUARE FEET OF COMMERCIAL USES (INCLUDING A 225-ROOM HOTEL AND 45,000 SQUARE FEET OF ANCILLARY RETAIL) ON AN APPROXIMATELY 21.4 ACRE SITE. THE PROJECT INCLUDES DEVELOPMENT OF TWO PUBLIC PARKS TOTALING APPROXIMATELY 2.6 ACRES STRUCTURED AND SURFACE PARKING, PRIVATE STREETS, NEW PUBLIC STREET, ON- AND OFF-SITE IMPROVEMENTS, LANDSCAPING, AND ON-SITE INFRASTRUCTURE. THE PROJECT INCLUDES A VESTING TENTATIVE SUBDIVISION MAP AND DEVELOPMENT AGREEMENT." (GC/3 types "197,000 square feed") |
| applicant | Josh Rupert and Ed Storm / Hunter Storm Properties, 10121 Miller Avenue, Suite 200, Cupertino | NOD pp. 1, 4 (and p. 3) | "Project Applicant: Josh Rupert and Ed Storm / Hunter Storm Properties"; p. 4: "APPLICANT NAME: Josh Rupert & Ed Storm / Hunter Storm Properties"; "10121 Miller Avenue, Suite 200 Cupertino, CA 95014"; p. 3: "JOSH RUPERT & ED STORM / HUNTER STORM" |
| location | 1205 Coleman Ave., Santa Clara | NOD p. 1; GC/3 | "Project Location (include county): 1205 Coleman Ave., Santa Clara, Santa Clara County" |
| filing | signed July 10, 2019 (Debby Fernandez, Associate Planner); County Clerk file ENV22285, July 10; OPR stamp July 15, 2019 | NOD pp. 1, 2, 4 | "Date: July 10, 2019"; "Title: Associate Planner"; "File Number: ENV22285"; "File Date: 07/10/2019"; stamp "JUL 15 2019" |
| original APNs, cross streets | 230-46-069 and 070; Coleman Ave. and Brokaw Road | GC/1, GC/2 | "Parcel # 230-46-069 & 070"; "Cross Streets Coleman Ave. and Brokaw Road" |
| NOP | Feb 22 to Mar 23, 2017; GPA to 51-100 du/ac with min. commercial FAR 0.20, rezoning, new zoning district; 1,600 homes, 215,000 sq ft commercial | GC/1 | "General Plan Amendment to change the land use designation on the project site to allow residential development at 51 to 100 dwelling units per acre in conjunction with a minimum commercial floor area ratio of 0.20; an amendment to the General Plan Land Use map for the Santa Clara Station Focus Area to reflect the General Plan change; are zoning of the project site; and a zoning code text amendment to add a new zoning designation"; "Residential (Units 1,600), Commercial (Sq. Ft. 215,000)"; "State Review Period Start 2/22/2017", "End 3/23/2017" |
| existing use (2017) | vacant / light industrial | GC/1 | "Present Land Use Vacnat/Light Industrial (ML)/ Regional Comercial, Very High Density Residential, and High Density Residential" (sic) |
| Draft EIR | Apr 10 to May 24, 2018; local actions listed | GC/2 | "EIR - Draft EIR"; "State Review Period Start 4/10/2018", "End 5/24/2018"; "Local Actions Specific Plan, Rezone, Vesting Tent. Map" |
| 2021 description | ~24-acre vacant site; phased; 152,000 sq ft hotel with 225 rooms; 45,000 sq ft retail; 2.6 acres of parkland | HOTEL p. 21 (doc p. 16) | "Just to the south of the project site on the other side of Coleman Avenue is an approximately 24-acre currently vacant site that is planned for development with the Gateway Crossings project. The approved mixed-use project is the phased development of 1,565 multi-family residential units, 45,000 square feet of ground floor supporting retail, 152,000-square-foot hotel with 225 rooms, 2.6 acres of dedicated parkland, surface and structured parking, private streets, and landscaped open landscape," |
| 2021 status | approved July 2019; construction expected to overlap the hotel's (about one year) | HOTEL p. 41 (doc p. 36) | "The Gateway Crossings Project, south of the project site and opposite of Coleman Avenue, was approved in July 2019. The future Gateway Crossings Project would include a residential component; however, it is unlikely construction would be completed prior to the completion of the proposed project and construction of both projects would likely overlap." |
| site history | 1205 Coleman: FMC Corporate Technology Center / BAE Systems; 328 Brokaw: former factory (military tracked vehicles until 1996), part of the Gateway site | HOTEL pp. 70-72 (doc pp. 65-67) | "1205 Coleman Avenue: This is the location of the planned Gateway Crossings project"; "Historical site operations included manufacturing of military tracked vehicles and other machinery until 1996. Site remediation activities have occurred in support of future site redevelopment (it is part of the site of the planned Gateway Crossings project)." |
| next to the BART station | NE of the Santa Clara Caltrain / future BART station; "future" in Feb 2024 | VTA p. 1 | "Santa Clara Station, adjacent to the Santa Clara Caltrain Station and the future Gateway Crossings development, will be the end of the line station for VTA's BART Phase II Extension."; "To the northeast will be Gateway Crossings, a new development with a mix of housing, retail, and open space." |
| in the station area plan | the City's 2026 plan record lists 230-60-001 to -009 among its 185 APNs | SCS; SCS-NOP p. 1 | APN list: "230-60-001, 230-60-002, ... 230-60-009"; "DATE: June 12, 2026" |
| current lots | 230-60-001 to -008 and -010 (18.83 acres) + four unnumbered street lots (2.52 acres) = 21.35 acres; addresses 1200 Rickabaugh Wy (-001), 330 Chastain Pl (-002), 360 Brokaw Rd (-006) | SCC | rows: "23060001 1200 RICKABAUGH WY", "23060002 330 CHASTAIN PL", "23060006 360 BROKAW RD"; -010's jurisdiction field reads "SAN JOSE"; 230-46-069 and -070 aren't in the layer |

Not found on any official host reachable: the number or share of affordable homes, building heights and stories,
the site plan and phasing, the approval's resolutions and ordinances, the development agreement and any amendment,
building permits.

Stage reasoning: **entitled**. One approval (July 9, 2019) with an EIR, a vesting tentative map and a development
agreement. The County's layer now shows the site as nine numbered lots plus street lots on a new assessor's page,
with situs addresses on the new streets, which suggests a final map has recorded; that is not evidence of
construction. The two latest official documents read describe the site as "currently vacant" (March 2021) and the
development as "future" (VTA, February 2024). No permit or inspection record could be reached. (Not official, so
not used: OpenStreetMap, which the base map draws, has two large building outlines on lots 230-60-001 and -002,
edited in Sept 2025 and May 2026; and a search-engine summary of a blocked City project page put it in an "Under
Construction" list. Both suggest construction may be under way; check when the City's site can be read.)

Boundary: `official_boundaries.py`, constants `GATEWAY_CROSSINGS_APNS` (230-60-001 to -008 and -010) and
`GATEWAY_CROSSINGS_COMMON_BOX`, and `SPECS["gateway-crossings"]`: the nine lots plus the four null-APN street lots
inside the box (the box returns exactly those four). The approval's APNs (230-46-069, -070) are retired; the
successor lots are the whole of assessor's page 230-60 at Coleman Avenue and Brokaw Road (230-60-010 replaces the
-009 that the City's 2026 record still lists, as `boundary_santa_clara_station_area.py` also found). Lot areas:
-001 3.67, -002 4.00, -003 2.76, -004 3.97, -005 1.48, -006 2.03, -007 0.56, -008 0.12, -010 0.24; street lots
1.30, 0.72, 0.30, 0.20 acres. Result **21.3 acres** as drawn (21.35 before simplifying) against the NOD's
approximately 21.4. Accuracy **approximate**, as for `seely-avenue`: the approval names the retired APNs, and
the drawn lots are their successors. One polygon, valid.

Overlaps (checked against every file in `data/boundaries/`, `data/massing/`, `data/landuse/` and `data/lines/`):
- `santa-clara-station-area`: the whole site (21.3 acres, 100%) lies inside it. Expected and accepted.
- `bart-silicon-valley-phase-2`: its alignment corridor polygon touches the site's southern corner, a sliver of
  62 m² (0.02 acres, at most about 3 m wide, near -121.93376, 37.35369). An edge contact, not a shared area; the
  BSVII line itself is 52 m away.
- `cahsr-sf-sj` corridor: 56 m away, no overlap. Nothing else within 600 m; no massing or land-use feature within
  300 m.

Massing: **none**. The Draft EIR (April 2018), which would hold the site plan and heights, has no attachment on
CEQAnet and the City's site is blocked; no other official document found gives building outlines or heights.

Press-only facts: none used and no `reported` block. Search results (not opened: `sfyimby.com` and
`berkadia.com` are blocked here) say Holland Partner Group took a 99-year ground lease on a 13.3-acre Phase I in
April 2021 and that permits were filed for a seven-story, 407-home building at 350 Chastain Place, the first of
five buildings. Check and add to `reported` when the pages can be read.

Open items:
- construction status (the City's project listing, building permits, any certificate of occupancy);
- affordable homes, heights, site plan and phasing (Draft EIR, Final EIR, approval resolutions);
- any amendment since 2019 (a search summary mentions a development agreement amendment of July 7, 2020; not
  verified);
- park acreage: the NOD and the 2021 study say 2.6 acres; a search summary of the City's listing says a 2.1-acre
  park (not verified);
- the site area: 21.4 acres (NOD) vs about 24 acres (HOTEL); the drawn lots support 21.4.

---

## Leads not added

- **Santa Clara's own project pages** (not opened; 403): `https://www.santaclaraca.gov/Home/Components/BusinessDirectory/BusinessDirectory/237/2495?alpha=G`
  ("Gateway Crossings (Hunter/Storm)"), `.../BusinessDirectory/607/2954` ("Coleman Ave (1205). Gateway Crossing
  New ..." park listing) and Legistar file 22-732
  (`https://santaclara.legistar.com/LegislationDetail.aspx?GUID=0D368AB1-F9FB-404C-9AD8-7FA7B23BD037&ID=5700811`).
  **Read first when the City's site is reachable**: likely the official answer on construction status.
- **Dual-Branded Hotel at Coleman and Brokaw** (Santa Clara; SCH 2021030592). Six-story, up to 400 rooms, 86 ft
  (variance), 1.66 acres at 1240 Coleman Ave / 312 Brokaw Rd, across Coleman from Gateway Crossings; MND March 25,
  2021, no NOD on CEQAnet (`https://ceqanet.lci.ca.gov/2021030592`). **Exclude** (single building; no approval
  found).
- **1400 Coleman Avenue Residential** (Santa Clara; SCH 2025070609). 142 for-sale townhomes (29 below market rate)
  in 12 buildings (13 in the MND) up to 50 ft on 3.8 acres; NODs Sept 26 and Nov 21, 2025 (`https://ceqanet.lci.ca.gov/2025070609/3`).
  **Exclude** (below the bar).
