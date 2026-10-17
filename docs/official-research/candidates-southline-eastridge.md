# Official-source findings: Southline and the Eastridge to BART Regional Connector

Checked 2026-10-17, from the Oct 17 lead scan (`docs/upkeep/leads-2026-10-17.md`). Matthew asked to add both.

How it was read: CEQAnet project, document and notice-of-determination pages and attachments (SCH 2020050452,
SCH 2001092014) were read directly; the Southline Draft EIR (850 pp.) and Final EIR (1,060 pp., with the Revised
Specific Plan as its Appendix 2.1) were read as text, with the figures viewed. VTA's project page, project document
list, fact sheet, newsletters, the 2019 Final SEIR-2 chapter 1, the 2020 and 2021 addenda and the 2018 Attachment C
plan sheets were read on `www.vta.org`. Page numbers are PDF pages unless a document page is given ("p. 2-23").
Local copies are in `data/raw/oct17/` and `data/raw/docs/` (git-ignored).

Not reachable from this session on 2026-10-17 (the egress proxy refused the connection): `ssf.net` / `www.ssfca.gov`
(City of South San Francisco: its posted Specific Plan, permit portal, Laserfiche WebLink and Legistar),
`data.smcgov.org` (County parcels), `vta.gov`, `gis.vta.org`, `gtfs.vta.org`, `caltrans-gis.dot.ca.gov`,
`www.arcgis.com`, `web.archive.org`. What these would have settled is listed under each project.

## Hosts

No new host is needed: every source cited is on `ceqanet.lci.ca.gov` or `vta.org`, both already in
`src/projects/official.ts`. (`vta.gov`, which the lead cites, is VTA's newer domain but could not be opened and is not
cited; `vta.org` serves the same project page.) If the City of South San Francisco's own pages are cited later, its
hosts `ssf.net` and `ssfca.gov` (the City's site; `ssf.net` redirects to `www.ssfca.gov`) would need adding.

---

## Summary

| # | project | city | stage (official) | size (official) | recommendation |
|---|---|---|---|---|---|
| 1 | Southline | South San Francisco | entitled: City Council approval July 13, 2022, second reading July 27, 2022 | up to 2,800,000 sq ft office/R&D on 28.5 acres | **INCLUDE** as `southline`, stage `entitled`; press construction reports held in `reported` |
| 2 | Eastridge to BART Regional Connector | San José | under construction since spring 2024; 67% complete May 31, 2026; service early 2028 | 2.4-mile light rail extension, 2 new stations, $652.9M | **INCLUDE** as `eastridge-bart-regional-connector`, category `transportation`, stage `construction` |

Neither overlaps a mapped project. Southline is across Huntington Avenue from San Bruno BART; the nearest edge of the
`tanforan` site is about 70 m away across Huntington Avenue and the city line (no overlap). The EBRC is separate from `bart-silicon-valley-phase-2`; it meets VTA's existing Orange
Line at Alum Rock.

---

## 1. southline

Recommendation: **INCLUDE**, stage `entitled`. A transit-oriented office/R&D campus of up to 2.8 million sq ft on a
former industrial site at 30 Tanforan Avenue in South San Francisco's Lindenville sub-area, across Huntington Avenue
from San Bruno BART, with a new east-west Southline Avenue and the 1.5-acre Southline Commons. Applicant: Lane
Partners.

Documents read:
- CEQAnet project page `https://ceqanet.lci.ca.gov/Project/2020050452`: NOP received 5/20/2020; Draft EIR 9/28/2021;
  Final EIR 5/18/2022; NODs 7/15/2022 and 7/29/2022.
- Draft EIR (Sept 2021) `https://ceqanet.lci.ca.gov/2020050452/3/Attachment/jwO0Ib` (document page
  `https://ceqanet.lci.ca.gov/2020050452/3`).
- Final EIR / Responses to Comments (May 2022) `https://ceqanet.lci.ca.gov/2020050452/4/Attachment/i50fMG`, which
  includes "New Appendix 2.1, Revised Southline Specific Plan" (PDF pp. 877-1060).
- NOD stamped July 14, 2022 `https://ceqanet.lci.ca.gov/2020050452/5/Attachment/23TQ-d`; NOD stamped July 28, 2022
  `https://ceqanet.lci.ca.gov/2020050452/6/Attachment/TVBE3X`.

| field | official value | source | quote |
|---|---|---|---|
| approvals | City Council approved July 13, 2022 | NOD 7/14/2022 p. 1 | "This is to advise that the City Council, Lead Agency, has approved the above described project on July 13, 2022" |
| second reading | July 27, 2022 | NOD 7/28/2022 p. 1 | "approved the above described project on July 13. 2022 and completed a second reading on July 271 2022" |
| actions | Specific Plan, GP amendment, zoning map and ordinance amendments, development agreement, design review, TDM plan, Precise Plan, vesting tentative map, EIR | NOD p. 1 | "Specific Plan; General Plan Amendment, Zoning Map and Ordinance Amendments, Development Agreement, Design Review, Transportation Demand Management Plan, Precise Plan, Vesting Tentative Map, and Environmental Impact Report for the Southline Project" |
| size, site | 28.5 acres, up to 2.8M sq ft | NOD p. 1 | "to redevelop a 28.5-acre industrial site in the Lindenville sub-area with up to 2.8 million square feet of transit-oriented office/ R&D and associated amenity uses" |
| addresses | 30, 40, 50, 54, 80 Tanforan Ave; 315, 319, 325, 347, 349 S. Maple Ave; 160, 180 S. Linden Ave; 240 Dollar Ave | NOD p. 1 | "Site at the intersection of Tanforan and South Maple Avenues: 30 Tanforan Avenue, …" |
| parcels | APNs 014-250-090, -080, -050, 014-241-030, -040, 014-232-030 | CEQAnet document pages 3-6 | "Parcel # 014-250-090, 014-250-080, 014-250-050, 014-241-030, 014-241-040, and 014-232-030" |
| acres (plan) | 28.5 acres | Revised Specific Plan p. 1-3 (FEIR PDF p. 899) | "28.5-acre Specific Plan area is in the Lindenville sub-area" |
| acres (DEIR) | 26.5 acres | DEIR p. 22 | "redevelop an approximately 26.5-acre" |
| why they differ | Alternative D adds about 2.1 acres (80 Tanforan) | FEIR PDF p. 102 | "under Alternative D, the Specific Plan area would increase by approximately 2.1 acres for a total area of approximately 28.6 acres" |
| revised plan | the revised Specific Plan follows Alternative D | FEIR PDF p. 145 | "The Draft Southline Specific Plan included in Appendix 2 of the draft EIR has been updated to align with Alternative D (Reduced Underground Parking Alternative)." |
| floor area cap | 2,800,000 sq ft, FAR about 2.4, parking structures excluded | Revised SP Table 2-1, p. 2-24 (FEIR PDF p. 936) | "The total allowable floor area shall be 2,800,000 square feet across the entire Specific Plan area, which equates to approximately 2.4 FAR, exclusive of parking structures" |
| conceptual buildout | Office/R&D 2,730,290; public amenity 13,500; tenant amenity 56,210; Phase 1 684,710 sq ft | Revised SP Table 2-3, p. 2-34 (FEIR PDF p. 946) | "Total 5 684,710 2,120,330 2,800,000"; note 5: "With exception for the total buildout square footage of 2,800,000 sf, the square footages provided in this Table 2-3 are not intended as caps" |
| Phase 1 (Alt D) | B1 318,380; B2 69,710 (three stories); B7 296,620 sq ft; office/R&D 615,000; new Parking Structure D at 80 Tanforan | FEIR Table 5-4 and text, PDF p. 105 | "construct a new above-grade parking structure (Parking Structure D) on the 80 Tanforan Avenue property"; "the amenities building would be reduced from four stories to three stories" |
| Phase 1 (DEIR) | B1 317,495 sq ft, 113 ft, 6 stories; B2 88,200, 60 ft, 4 stories; B7 295,220, 113 ft, 6 stories; total 612,715 office | DEIR Table 3-10, PDF p. 131 | "Building Height (feet) 113 60 113" |
| heights | about 120 ft, set by FAA / SFO ALUCP limits | Revised SP Table 2-1 (PDF p. 936); DEIR p. 117 | "generally, the maximum height limit within the Specific Plan would be 120 feet" |
| conceptual heights | 80, 105, 115, 120 ft by building | Revised SP Figure 2-8, p. 2-23 (PDF p. 935) | legend "80 feet / 105 feet / 115 feet / 120 feet" |
| phasing | Phase 1: Buildings 1, 2, 7, Parking Structure D; future: 3-6, Parking Structure C | Revised SP Figure 2-9, p. 2-35 (PDF p. 947) | legend "Phase 1 / Future Phases" |
| open space (DEIR) | up to 341,800 sq ft (7.8 acres); 1.5-acre Southline Commons | DEIR p. 22; Revised SP p. 2-3 | "up to 341,800 square feet (7.8 acres), of open space" |
| applicant | Lane Partners | DEIR p. 22 | "The project applicant, Lane Partners, proposes to redevelop" |
| construction start (EIR) | Phase 1 anticipated to start 2022 | DEIR pp. 33, 112 | "with Phase 1 construction anticipated to commence in 2022" |

Lead figures checked: "2.8M sq ft on 28.5 acres" is right (the Draft EIR's 26.5 acres predates the added parcel).
"Approved 2022": the City approved it on July 13, 2022 (second reading July 27), not in September as the press dates the
vote. "Phase 1 … about 612,715 sq ft plus an 88,200 sq ft amenities building" are the Draft EIR figures; the revised
plan's Phase 1 is 615,000 sq ft of office/R&D and a 69,710 sq ft, three-story amenities building plus Parking
Structure D.

Stage: `entitled`. The press reports Phase 1 under construction (Building 1 steel up in May 2023, a construction loan
and recapitalization in January 2023, Building 1 topped out per the architect), and OpenStreetMap already maps
footprints where Buildings 1 and 2 and Parking Structure D are planned, but no City of South San Francisco permit or
staff report could be reached to confirm it (`ssf.net` refused the connection). Press claims go in `reported`.

Boundary: traced (`pipeline/bam_pipeline/sites/boundary_southline.py`, `accuracy: "approximate"`) from the dotted
"Specific Plan Area" line in the Revised Specific Plan's Figure 2-8 (FEIR PDF p. 935): the figure's aerial photo is
fitted to OpenStreetMap building footprints (`line_georef.register_buildings`, RMS 1.3 m over 39 tiles, from two
hand-located street points); the dots are bridged and filled and pulled back to the dot centres. 28.4 acres as drawn
against the plan's 28.5. Preferred official source when reachable: County of San Mateo parcels (`data.smcgov.org`
`nr6j-72z7`) for the six APNs above (the Draft EIR speaks of seven parcels).

Massing: `pipeline/bam_pipeline/sites/massing_southline.py`, illustrative envelopes. Figure 2-8's coloured footprints
(classified against its legend, with the photo's greys as extra classes) raised to their figure heights: Buildings 4
and 5 (one touching zone) 120 ft, Building 6 120 ft, Parking Structure C 105 ft, Buildings 1, 3, 7 115 ft, Building 2
80 ft, Parking Structure D 80 ft; phase from Figure 2-9; all `entitled`. Notes carry the Draft EIR and Alternative D
figures where they differ (Buildings 1 and 7: 113 ft in the DEIR; Building 2: 60 ft and four stories in the DEIR,
three stories in Alternative D). Nothing drawn as built.

Left out: the Draft EIR's Office and Life Sciences scenario site plans (superseded by the revised plan's layout); the
off-site street improvements (Huntington, Tanforan, Linden/Dollar); the Precise Plan drawings (Building 1 and 7 floor
plans, superseded by Alternative D sizes).

Press-only (to `reported`): SF YIMBY, Jan 2023 (recapitalization, $373M construction loan) and May 2023 (Building 1
steel); DES Architects + Engineers, "Southline B1 Tops Out".

Open: the City's adopted Specific Plan text and any later amendments; Phase 1 building permits and certificates of
occupancy; the County parcel check.

## 2. eastridge-bart-regional-connector

Recommendation: **INCLUDE**, category `transportation`, stage `construction`. VTA's 2.4-mile extension of the Orange
Line light rail from the Alum Rock station along Capitol Avenue and, mostly on an elevated guideway, the Capitol
Expressway median to the Eastridge Transit Center, with an elevated Story Road station and an at-grade Eastridge
station. Formerly the Capitol Expressway Light Rail Project (Phase 2 of the Capitol Expressway Transit Improvement
Project).

Documents read:
- VTA project page `https://www.vta.org/projects/eastridge-bart-regional-connector` (weekly construction updates to
  Sept 28, 2026) and document list `https://www.vta.org/projects/documents?project=966`.
- Fact sheet (EBRC-CELR-093026, Sept 30, 2026) `https://www.vta.org/sites/default/files/2026-09/FS-EBRC-EN-093026.pdf`.
- Newsletters: Spring 2024 `https://www.vta.org/sites/default/files/2024-04/UPDATE-EastridgeBART-newsletter-2024.pdf`;
  Summer 2024 `https://www.vta.org/sites/default/files/2024-08/FinalEBRC%20Summer%20Newsletter%202024%28web%29.pdf`;
  Fall 2025 `https://www.vta.org/sites/default/files/2026-01/2025EBRC_Fall_Newsletter_SC_adafile.pdf`;
  Winter 2026 `https://www.vta.org/sites/default/files/2026-03/2026EBRC_Winter_Newsletter.pdf`;
  Summer 2026 `https://www.vta.org/sites/default/files/2026-07/2026EBRC_Summer_Newsletter_ADA_Final.pdf`.
- Final SEIR-2 (2019), Chapter 1 `https://www.vta.org/sites/default/files/documents/Ch_01_Introduction_FSEIR-2.pdf`;
  Draft SEIR-2 (2018) Attachment C, Detailed Plans for the Proposed Changes
  `https://www.vta.org/sites/default/files/documents/Att_C_Detailed_Plans_for_the_Proposed_Changes.pdf`.
- Third Addendum (Feb 2021)
  `https://www.vta.org/sites/default/files/2021-02/2021%20Third%20Addendum%20to%20the%20Final%20Second%20Supplemental%20Environmental%20Impact%20Report.pdf`;
  Second Addendum (Jan 2020) `https://www.vta.org/sites/default/files/2020-01/FSEIR2-EBRC_Addendum_No_2_202001_0.pdf`.
- CEQAnet `https://ceqanet.lci.ca.gov/Project/2001092014` (18 documents); NODs `/2001092014/13` (VTA, June 2019),
  `/14` (Feb 2020), `/15` (CPUC, Apr 2020), `/16` (Mar 2021), `/17` (Valley Water, Apr 2021), `/18` (CTC, Aug 2023),
  with `/18/Attachment/BPu1pF`.

| field | official value | source | quote |
|---|---|---|---|
| description | Alum Rock station to Eastridge Transit Center, elevated guideway mostly in the expressway median; elevated Story Road station, at-grade Eastridge station | fact sheet p. 1 | "extends light rail from the existing Alum Rock Light Rail Station to the Eastridge Transit Center, with an elevated guideway primarily in the center of Capitol Expressway" |
| length | 2.4 miles | fact sheet p. 2; CTC NOD | "The Project will construct a 2.4-mile extension"; "a distance of approximately 2.4 miles" |
| route | begins on Capitol Avenue near Wilbur Avenue, into the expressway median on an elevated structure, south to Quimby Road | Summer 2026 newsletter p. 1 | "The 2.4-mile alignment begins on Capitol Avenue near Wilbur Avenue, transitions into the Capitol Expressway median on an elevated structure, and continues south to Quimby Road" |
| other works | TPSS at Ocala and Eastridge; HOV lanes removed Story-Tully; 115-kV towers replaced | CTC NOD (2023) p. 1 | "high-occupancy vehicle lanes will be removed between Story Road and Tully Road" |
| cost | $652.9 million (design, ROW, utilities, construction) | fact sheet p. 1 | "$652.9 million for design, right of way, utilities, and construction" |
| funding | 2000 Measure A $313.6M; SB1 $25.1M; RM3 $130.0M; LCTOP $14.8M; TIRCP $46.6M; other $122.8M to be secured | fact sheet p. 1 | "Other funding sources*** $122.8M … ***To be secured" |
| schedule (fact sheet) | environmental 2019; addenda 2020, 2021; final design 2022; ROW 2022; construction early 2024 through 2027; revenue service 2028 | fact sheet p. 1 | "Revenue service . . . Expected 2028" |
| CEQA | Final SEIR-2 approved June 6, 2019 | CEQAnet NOD /13 | "Approved On 6/6/2019" |
| CPUC | eight grade-separated highway crossings, two at-grade pedestrian crossings | CEQAnet NOD /15 (received 4/17/2020) | "Authority granted to construct eight grade separated highway crossings and two at grade pedestrian light rail crossings" |
| CTC | approved as responsible agency Aug 16-17, 2023 | CTC NOD p. 1 | "the California Transportation Commission has approved the above-described project on August 16-17, 2023" |
| contract | March 7, 2024: $437,161,464 to MCM Railworks, JV | Spring 2024 newsletter p. 1 | "VTA's Board of Directors unanimously awarded the construction contract in the amount of $437,161,464 to MCM Railworks, Joint Venture" |
| construction start | May 2024 (Summer 2024); April 2024 (Winter 2026); spring 2024 (Sept 21, 2026 update) | newsletters | "Construction activities began on May 2024"; "Major construction of the EBRC officially began in April 2024" |
| groundbreaking | Saturday June 8, 2024 | Summer 2024 newsletter | "On Saturday, June 8, … gathered at the Eastridge Transit Center to celebrate the start of construction" |
| progress | 67% complete as of May 31, 2026; about 1.5 miles of guideway done | Summer 2026 newsletter p. 1 | "crews have completed approximately 1.5 miles of the guideway. As of May 31, 2026, the project is 67% complete." |
| opening | complete late 2027; passenger service early 2028 | Summer 2026 newsletter p. 1 | "The EBRC Project is anticipated to be completed in late 2027 and passenger service is anticipated to begin in early 2028" |
| history | NOI/NOP Sept 2001; Final EIR May 2005; Final SEIR Aug 2007; phasing addendum June 2010; IS/MND March 2014 (Ocala station dropped); SEIR-2 June 2019; Second Addendum Feb 2020 | Third Addendum pp. 2-3 | "A Second Supplemental EIR (SEIR-2) and Second Subsequent IS was approved in June 2019" |
| earlier phases | Phase 1A pedestrian/safety work done fall 2012; Phase 1B Eastridge Transit Center rebuilt 2015 | fact sheet p. 1 | "This was completed in Fall 2012"; "This was completed in 2015" |

Lead figures checked: 2.4 miles, Alum Rock to Eastridge, under construction, completion 2028: confirmed (construction
end late 2027, service early 2028). Cost: VTA's figure is $652.9 million (the lead's range came from press). The
lead's "more than 50% complete in Dec 2025" was not checked; VTA's newest figure is 67% at May 31, 2026.

Geometry (`pipeline/bam_pipeline/sites/lines_eastridge_bart_regional_connector.py`, written like
`lines_valley_link.py`; the line writer also writes the 60 m corridor boundary, as for `valley-link` and
`bart-silicon-valley-phase-2`):
- Source: Draft SEIR-2 Attachment C (15 scanned plan-and-profile sheets EX001-EX015, BKF Engineers for VTA, July 19,
  2018, 1" = 40'), STA 964+80 at the Wilbur Avenue conform point to the bumping posts near STA 1095. No official GIS
  could be reached (`gis.vta.org`).
- Tracks: both track centrelines found automatically by their 50-ft station ticks (187 px apart, matching the
  sheet's scale bar), drawn as the centreline between them.
- Georeference: per sheet, trimmed ICP of the grey base map within 45 m of the tracks onto OpenStreetMap street
  centrelines at the drawing scale (trimmed RMS 0.7-1.7 m), several sideways starts; then a least-squares tie of all
  sheets: match-line joins closed using the stationing (sideways misfit under 1 m after the tie), smooth tangents,
  and on EX001-EX011 the tracks' middle held to the middle of Capitol Avenue / Capitol Expressway (VTA: "primarily in
  the center of Capitol Expressway"). Street fits alone were ambiguous sideways by a carriageway (10-45 m), which is
  why the tie is needed.
- Check (not a source): the traced centreline lies a median 1.8 m (90% within 4.2 m) from OpenStreetMap's mapping of
  the tracks under construction ("Alum Rock-Eastridge Corridor"), where OpenStreetMap maps them.
- 2.47 miles as drawn (VTA: 2.4 miles; the drawn line includes the tie-in at Wilbur and the tail tracks past
  Eastridge). One segment, `new`.
- Stations: Story Road (platform middle between work points WP1-WP2, sheet EX004) and Eastridge (WP3-WP4, sheet
  EX014), both `new`. The existing Alum Rock station lies north of the sheets and is not drawn.

Left out: the 2004-2014 alternatives (including the dropped Ocala station); Phase 1 sidewalks and the 2015 transit
center rebuild (done); the Story Road pedestrian overcrossing, traction power substations and relocated transmission
towers (no line or station kind for them).

Press-only: none used.

Open: the construction start month (April or May 2024 in VTA's own newsletters); the $122.8M still to be secured;
the geometry against VTA GIS or construction drawings, especially the Eastridge end (EX012-EX015), which leaves the
median and is held by the sheet joins only.
