# Official-source findings: The Orchards (San Ramon) and CityView Plaza (San José)

Checked 2026-10-17. Matthew asked on 2026-10-17 to add six projects from the Oct 17 lead scan
(`docs/upkeep/leads-2026-10-17.md`); this file covers two of them. **The Orchards** is added
(`the-orchards`, boundary only). **CityView Plaza is stopped**: its current approved scope
can't be read from here (see part 2).

How it was read. This session's network was narrower than the brief expected. Reachable: CEQAnet
(project pages, attachments and the CSV export), `www.sanramon.ca.gov` (its HTML pages only) and the
Overture S3 bucket. Refused by the egress proxy: `sanramon.ca.gov` (bare), `docs.sanramon.ca.gov`
(the City's Laserfiche), `cdnsm5-hosted.civiclive.com` (where every `www.sanramon.ca.gov/UserFiles/...`
link redirects, so none of the City's PDFs or images could be read), `sanramonca.iqm2.com`,
`sanramonca.portal.civicclerk.com`, `gis.sanramon.ca.gov`, Contra Costa County GIS (`gis.cccounty.us`,
`ccmap.cccounty.us`), `sanjose.legistar.com`, `webapi.legistar.com`, `legistar.granicus.com`,
`geo.sanjoseca.gov`, `data.sccgov.org` and `sjpermits.org`. `www.sanjoseca.gov` answers "Access Denied"
(403) to scripts and to headless Chromium with a browser user agent. WebFetch failed on the same hosts.
Local copies are in `data/raw/orchards/` and `data/raw/cityview/` (git-ignored). Page numbers are PDF
pages unless a document page is given.

URL shorthand:
- `NOE` = `https://ceqanet.lci.ca.gov/2026020219/Attachment/G7E_Xs` (Orchards notice of exemption, signed
  Feb 5, 2026, posted Feb 6, 2026; 4 pp.; sha256 `c0342c7c…5b4a`), CEQAnet record
  `https://ceqanet.lci.ca.gov/2026020219`
- `SR-PAGE` = `https://www.sanramon.ca.gov/cms/one.aspx?pageId=19165945` (City project page, "The Orchards
  (formerly Chevron Park)")
- `SR-NEWS/<slug>` = `https://www.sanramon.ca.gov/news/what_s_new/<slug>` (City news items)
- `GP-DEIR` = `https://ceqanet.lci.ca.gov/2022060549/2/Attachment/ueWNFZ` (San Ramon 2040 General Plan Draft
  EIR, Aug 2023, 613 pp.; sha256 `ad3c1dca…c392`)
- `CV-DSEIR` = `https://ceqanet.lci.ca.gov/2018022032/4/Attachment/znvbLi` (CityView Plaza Office Project Draft
  Supplemental EIR, Mar 2020, 164 pp.; sha256 `0245e717…72a9`)
- `WOZ-DSEIR` = `https://ceqanet.lci.ca.gov/2003042127/23/Attachment/-wwI_E` (City of San José, Woz Way Project
  Draft SEIR, Mar 2021; sha256 `50204305…d22e`)

## Hosts needed in `src/projects/official.ts`

None. Every source in the Orchards record is on `ceqanet.lci.ca.gov` or `www.sanramon.ca.gov` (a `.gov`
host). The City's file store `cdnsm5-hosted.civiclive.com` would be needed to cite its PDFs directly (it is
the CivicLive CDN that `www.sanramon.ca.gov/UserFiles/...` redirects to), but no record cites it; the record
cites the `www.sanramon.ca.gov` pages that link them.

---

## 1. The Orchards (former Chevron Park), San Ramon: INCLUDE

### Lead check

| lead said | official | verdict |
|---|---|---|
| up to 2,510 homes | "up to 2,510 residential units" (NOE p. 1; SR-PAGE) | confirmed |
| about 92 acres | "the existing 92-acre site" (NOE p. 1); "approximately 92 acres" (SR-PAGE) | confirmed; the press figure of 144 acres is wrong |
| over about 20 years | "a master plan to construct up to 2,510 residential units over the course of 20 years" (SR-NEWS/orchards_third_public_hearing) | confirmed |
| PC approved Feb 3, 2026 (Res. 02-26) | "approved Resolution No. 02-26, approving the Orchards Development Project" (SR-NEWS/orchards_third_public_hearing) | confirmed |
| appeal Feb 12; Council denied Apr 7, 2026 | "On February 12, 2026, the City received an appeal ... The City Council voted unanimously to deny the appeal and uphold the Planning Commission's original project approval." (SR-NEWS/the_orchards_appeal_denied) | confirmed |
| NOE posted Feb 6, 2026 | CEQAnet 2026020219: "Received 2/6/2026 Posted 2/6/2026" | confirmed |

Meets the bar (2,510 homes). Not on the map under another name; nearest mapped projects are far away.
Stage: **entitled** (approved, appeal denied; no permits or construction found).

### Official values

| field | value | source, page | quote |
|---|---|---|---|
| applications | MJ 2024-0004, DP 2024-0006, DP 2024-0008, AR 2024-0013, TRP 2024-0009, ENVR 2025-0003 | NOE p. 1 | "Orchards Development Project (MJ 2024-0004, DP 2024-0006, DP 2024-0008, AR 2024-0013, TRP 2024-0009, and ENVR 2025-0003)" |
| location / parcel | 6001 Bollinger Canyon Road, APN 213-120-008 | NOE p. 1 | "6001 Bollinger Canyon Road, San Ramon, CA 94583 Contra Costa County (APN: 213-120-008)" |
| applicant / owner | BR6001, LLC (c/o Sunset Development Company) | NOE p. 1 | "PROJECT APPLICANT: BR6001, LLC (c/o Sunset Development Company)"; "PROPERTY OWNER: BR6001, LLC (c/o Sunset Development Co.)" |
| program | demolish 1.3M sq ft office; 3 districts, 191 lots, up to 2,510 units; Neighborhood District 230 SF + 138 townhomes + 58 optional ADUs | NOE p. 1 | "demolition of 1.3m sq. ft. office buildings (formerly Chevron Office Park), subdivision of the existing 92-acre site into three Districts and 191 lots for up to 2,510 residential units, and approval of two development plans for the development of the Orchards Development Master Plan, and the Neighborhood District consisting of 230 single-family homes, 138 multi-family townhomes, and 58 optional accessory dwelling units (ADUs)" |
| density | 46.3 du per net acre (NOE p. 1); 47.2 du/ac sitewide (NOE p. 2, findings) | NOE pp. 1-2 | "overall density of 46.3 dwelling units per net acre"; "sitewide density of 47.2 dwelling units per acre" |
| districts | Mixed-Use, Multi-Family, Single Family/Townhomes; Neighborhood District 368 units + 58 ADUs | SR-NEWS/the_orchards_appeal_denied | "subdivide the property to create three Districts on approximately 92 acres for Mixed-Use, Multi-Family, and Single Family/Townhomes uses; ... a development plan for the Neighborhood District consisting of 368 units and 58 optional accessory dwelling units" |
| zoning | Downtown Mixed Use – South (DMU-S), 20–60 du/ac | NOE pp. 1-2 | "consistent with the City of San Ramon 2040 General Plan and Zoning designation of Downtown Mixed Use – South (DMU-S)"; "The DMU-S designation permits a density range of 20–60 dwelling units per acre." |
| CEQA | statutory exemption, Guidelines 15183, tiered on the 2040 GP EIR (SCH 2022060549) | NOE p. 1 | "Statutory Exemptions: Projects Consistent with the General Plan - 15183" |
| GP 2040 approval | Dec 12, 2023 (NOD "Approved On 12/12/2023"); NOE says the EIR was certified Dec 13, 2023 | `https://ceqanet.lci.ca.gov/2022060549/3`; NOE p. 1 | used the NOD date and the City page ("On December 12, 2023, the San Ramon City Council approved the General Plan 2040 Update ... re-zone ... to Downtown Mixed Use-South") |
| purchase | Sunset bought the campus, announced Sept 28, 2022 | SR-PAGE (Overview tab) | "On September 28, 2022, Sunset Development announced the purchase of Chevron's 92-acre, 1.3-million-square-foot "Chevron Park" campus in Bishop Ranch" |
| applications filed / complete | Nov 21, 2024 / Mar 26, 2025 | SR-NEWS/orchards_preliminary_application | "submitted formal applications ... on November 21, 2024. The applications were deemed complete on March 26, 2025." |
| SB 330 preliminary application | June 24, 2025; GP/zoning amendments rescinded; FAR reduction 1.25 → 0.5 dropped | same | "Sunset Development filed a Preliminary Housing Development application and rescinded their applications to amend the General Plan and Zoning Ordinance ... will no longer pursue the initial proposal to reduce the General Plan and Zoning standard for minimum Floor Area Ratio from 1.25 to 0.5." |
| hearings | PC Dec 16, 2025; Jan 20, 2026; Feb 3, 2026 | SR-NEWS/orchards_third_public_hearing | "took place at the Planning Commission Meeting on Tuesday, December 16, 2025"; "...January 20, 2026"; "...February 3" |
| ARB | design meetings May and June 2025 | SR-NEWS/orchards_preliminary_application | "several public meetings were conducted by the Architectural Review Board in May and June 2025" |

Not found officially (left null): affordable homes, commercial floor area in the Mixed-Use District, open
space acreage, block heights. These are in the staff reports, conditions of approval, project plans
(`docs.sanramon.ca.gov/WebLink/DocView.aspx?id=20812236`) and design guidelines (`.../Orchards/C%20Design%20Guidelines%20Reduced.pdf`),
all on hosts refused here.

Draft zoning (context only, not used): the 2023 GP Draft EIR Appendix A2 (`https://ceqanet.lci.ca.gov/2022060549/2/Attachment/BMxFru`,
p. 9) lists an 85 ft DMU-S height limit, but it is the August 2023 draft and the adopted code wasn't
reachable, so it isn't drawn or cited.

### Boundary

`pipeline/bam_pipeline/sites/boundary_the_orchards.py` → `data/boundaries/the-orchards.geojson`, **approximate**.

- The approval names one parcel (APN 213-120-008). The County's parcel map and the City's GIS were refused, so
  the parcel is traced from GP-DEIR Figure 2-4, Proposed San Ramon Land Use Designations (PDF p. 67), one
  embedded raster (1,987 × 1,500 px) drawn from the City's GIS with parcel lines. Chevron Park is the pale
  "Office" area south of Bollinger Canyon Road between I-680 and the Iron Horse Trail; a parcel line separates
  the large western lot (the campus, with its courtyard buildings) from the smaller lots along the trail (the
  Bishop Ranch 1 buildings, reached by OSM's "Bishop Ranch 1" roads). The western lot is the site.
- Georeference: three road crossings read off the figure (Bollinger Canyon Rd at I-680, at Camino Ramon and at
  the Iron Horse Trail; initial RMS 16 m), refined by trimmed ICP of the I-680, trail and Bollinger bands
  against OpenStreetMap (via Overture): 9.35 m/px, rotation 1.65°, trimmed RMS 3.9 m over the closest 80%.
- Result: 88.6 acres against the official 92 (−4%). Good to about 10–20 m (one or two pixels).
- Cross-check: the GP Draft EIR Appendix A2 "City Core" sheet (p. 16) outlines the same block on an aerial
  photo; it agrees by eye. Its APN list includes 213-120-008.

**Update (Oct 17, later): approved plans reached, boundary re-traced.** `docs.sanramon.ca.gov` (Laserfiche
WebLink) became reachable; the project folder is `\Planning\Projects\The Orchards` (folder 20812232), with
the Planning Commission packet of Dec 16, 2025 (folder 20812245) and the City Council packet of Apr 7, 2026
(folder 21619738). Downloaded (sha256 pinned in the modules): D. Applicant's Project Plans, Sept 5, 2025
(record 20812236, 218 pp.); Orchards Design Guidelines, Nov 14, 2025 (21620063, 224 pp.); City Council
Resolution 2026-040 with Exhibits A-C (21620060); Planning Commission Resolution 02-26 (21620061); Affordable
Housing Plan, Dec 4, 2025 (21620068). Contra Costa County's parcel services, `gis.sanramon.ca.gov` and the
civiclive file store still refuse the connection, so the County parcel couldn't be used.

| field | value | source | quote |
|---|---|---|---|
| site | Parcel A, 91.55 acres | Plans sheet C3.0 (PDF p. 179) | "PARCEL A DN 2000-0220096 91.55 AC±" |
| site | 92 acres, APN 213-120-008 | CC Res. 2026-040 p. 3 | "the Master Plan area encompasses the 92-acre site at 6001 Bollinger Canyon Road (formerly Chevron Office Park, APN: 213-120-008)" |
| APN conflict | 213-701-002 | CC Res. 2026-040 p. 1 (heading) | "LOCATED AT 6001 BOLLINGER CANYON ROAD (APN: 213-701-002)" |
| homes | 2,452 + 58 optional ADUs | CC Res. 2026-040, conditions p. 1 | "three Districts totaling up to 2,452 dwelling units and 58 optional accessory dwelling units (ADUs)" |
| districts | 619 / 1,465 / 368 | CC Res. 2026-040 p. 4 | "up to 619 dwelling units within the Mixed Use District with 125,000 sq. ft. of ground floor retail, entertainment and commercial uses, 2) 1,465 dwelling units within the Multi-Family District ... 368 single-family townhomes and detached homes plus 58 optional Accessory Dwelling Units" |
| affordable | 397 (16.2%) | CC Res. 2026-040 p. 4 | "commits to 16.2% (397 units) of the 2,452 units as deed restricted units for very low, low, and moderate income households" |
| affordable mix | 163 / 212 / 22 | CC Res. 2026-040 finding (c); AHP p. 3 table | "163 Very Low-Income, 212 Very-Low Income, and 22 Moderate Income units" (the resolution's second "Very-Low" is the AHP's Low, 80% AMI) |
| affordable site | 100 homes (99 + manager) | AHP p. 2; CC conditions (Neighborhood) | "an approximately 1.9-acre site ... for the development of a 100-home affordable community by Eden Housing, with 99 affordable homes and one manager's unit" |
| height | 85 ft max | CC Res. 2026-040 findings | "subject to a maximum height of 85 feet, per Division D2-14 of the San Ramon Zoning Ordinance" |
| MU heights | 5-7 floors, 85 ft | DG p. 162, Fig. 7.1.2 | "may be developed to between five (5) to seven (7) floors and a maximum height of 85 feet" |
| MF heights | B, C 85 ft; E, F, G, H 65 ft | DG p. 168, Fig. 7.2.2 | "(B and C parcels) may be developed up to seven (7) floors and a maximum height of 85 feet" / "The E, F, G and H parcels ... four (4) or five (5) floors and a maximum height of 65 feet" |
| ND heights | 40 / 35 ft | DG p. 175, Fig. 7.3.2 | "Attached Row Townhomes: 40-feet; Single-Family Row Homes: 35-feet; Single-Family Homes: 35-feet; Single-Family Court Homes: 35-feet" |
| ND heights (older) | 30 ft single-family, 40 ft townhomes | Plans sheet SP4, DMU-S standards table | "Height limit [1] Maximum ... 30 30 30 40 16" |
| parcels | MU A1-A4, D1 (8.9 ac); MF B1, B2, C1, C2, E1, F1, G1, G2, H1 (16.3 ac); lots 1-103 (27.8 ac) | Plans sheet C2.0 area table (PDF p. 172) | tabled areas in sq ft |
| phasing | MU and MF districts "future application" | Plans sheet L-200 (PDF p. 166) | "FUTURE APPLICATION MULTI-FAMILY DISTRICT (MFD) FUTURE APPLICATION MIXED-USE ..." |

Boundary now `traced` (was `approximate`): sheet C3.0's project boundary (2.7-pt CAD line) at 1" = 100' encloses
91.58 acres against the tabled 91.55, which confirms the scale. It is placed by the existing buildings the sheet
draws (71 closed outlines) on OpenStreetMap building footprints: cross-correlation of filled outlines over
rotations 24-32° (best 27.7°), then rigid trimmed ICP with the scale held (rotation 27.8°, trimmed RMS 0.8 m over
the closest 50% of outline points, median 2.9 m). 91.6 acres as drawn. Against the GP-DEIR trace (88.6 acres): up
to 34.5 m apart. Massing: `massing_the_orchards.py`, the C2.0 development parcels and lots (each checked against its
tabled area within 1%; lots 1-103 against the 1,210,450 sq ft total) raised to the design guidelines' limits; the
attached row townhome lots (78-103) identified from DG Figure 7.3.2 and plan sheet SP2. Open-space and street
parcels are left empty; the 1-story retail pavilion in the Mixed-Use District (DG Fig. 7.1.2) has no stated
height in feet and isn't drawn.

### Geometry on the site

None. No massing: the project plans and design guidelines were unreachable, and no official document read
here gives block footprints or heights. All existing campus buildings are to be demolished (NOE p. 1), so no
existing buildings are kept. Plot: `oct17-plots/the-orchards.png` in the scratchpad.

### Press only (not in the record)

The press reports "nearly 3,000" homes and 144 acres; both contradict the City and are not kept. No press fact
was needed, so the record has no `reported` block.

---

## 2. CityView Plaza, downtown San José: STOPPED

### Why

The City's project page (only seen as search-result snippets; `www.sanjoseca.gov` refuses this environment)
lists an **Addendum, file H25-008** (with ER25-055 and AD24-707), covering "changes to the approved project
that includes a new eight-story structure with 35,000 square feet of retail space and 1260 parking stalls; and
conversion of existing office space to 330 residential units", with a Site Development Permit hearing before
the Director of Planning set for Aug 27, 2025. The press (SF YIMBY, Feb 2026) reports building permits for an
eight-story retail and garage structure at 185 Park Avenue, and a shift from office to housing.

So the 2020 three-tower design is at least partly superseded: the 2020 plan demolished every existing building,
while the addendum converts existing office space to homes. Whether the three 19-story towers (3.8M sq ft)
remain entitled can't be read without the addendum and the Director's decision, both posted only on
`sanjoseca.gov`. Without them:
- the project can't be shown to still meet the bar (1M+ sq ft), and
- drawing the 2020 towers would draw a superseded document as if current.

Per the brief, the project is stopped and not added. No record, boundary or massing was written.

### What to fetch to finish it (from a browser that can reach sanjoseca.gov)

1. The CityView Plaza project page (lead URL) and its Addendum H25-008 with Appendices A–D.
2. The Director's hearing result for Aug 27, 2025 (Planning Director hearing agendas/actions), and the June 16,
   2020 City Council action and resolution (Legistar, `sanjose.legistar.com`).
3. Building permits for 185 Park Avenue (and any others) from San José's permit portal, which would set the
   stage (construction) under the permit-date rule.
4. Parcels: Santa Clara County assessor (data.sccgov.org `ubcd-cewv`), APNs 259-41-054, -057, -066, -067,
   -068, -070 (CV-DSEIR p. 20); exclude 190 Park Avenue (shown as existing on Figure 2.2-1).

### Official facts gathered (for whoever finishes it)

| field | value | source, page | quote |
|---|---|---|---|
| 2018 project | 24-story residential tower, 253 units, 267 ft, 170 Park Ave site (APN 259-41-067) | CEQAnet `https://ceqanet.lci.ca.gov/2018022032` (NOP 2/15/2018) | "construct a 24-story residential tower with upt o 253 residential units ... maximum height of 267 feet to the roofline" |
| 2019 NOP | 3.66M sq ft office/commercial on 6.9 gross acres, replacing ~960,567 sq ft | `https://ceqanet.lci.ca.gov/2018022032/3` (NOP 8/9/2019) | "construction of an office development totaling approximately 3.66 million square feet of office and commercial space above a subterranean parking garage on an approximately 6.9-gross acre site"; "Site excludes the buildings at 121 and 190 Park Center Plaza." |
| 2020 SEIR | 3.79M sq ft (3,574,533 office, 65,500 retail/active), 8.1 gross acres, demolish ~1,041,567 sq ft | `https://ceqanet.lci.ca.gov/2018022032/4` (SIR 3/11/2020) | "construct an office development totaling approximately 3. 79 million square feet, comprised of 65,500 square feet of ground floor retail and active tenant ground floor space and 3,574,533 square feet of office space, on an approximately 8.1 gross-acre site" |
| site | 8.1 acres, APNs 259-41-054, -057, -066, -067, -068, -070 | CV-DSEIR p. 20 (doc p. 3) | "The applicant proposes to redevelop approximately 8.1 acres (APNs 259-41-054, -057, -066, -067, -068, -070)" |
| buildings | three 19-story towers (A, B, C), up to 293 ft to top of parapet, FAR 10.7, total 3,790,236 sq ft, pedestrian bridge floors 5–19 | CV-DSEIR p. 20 (doc p. 3) | "three new 19-story office buildings (Towers A, B, and C) ... totaling 3,790,236 square feet. The buildings would be up to 293 feet tall to the top of the parapet with a floor area ratio (FAR) of 10.7." |
| airport height | 293 ft is the airport limit for the site | CV-DSEIR p. 29 (doc p. 12) | "not exceeding the maximum height limitation of 293 feet for the safe operation of Mineta San José International Airport" |
| phasing | Phase 1 Tower A + podium on W San Fernando (150 S Almaden kept); Phase 2 Tower B; Phase 3 demolish 150 S Almaden, Tower C | CV-DSEIR p. 29 (doc p. 12), Table 2.2-2; Figure 2.2-4 p. 30 | "Tower A and podium along West San Fernando Street"; "After complete vacancy, the office tower at 150 South Almaden Boulevard would be demolished" |
| site plan | Figure 2.2-1, vector, Towers A–C footprints, property line | CV-DSEIR p. 24 | — |
| alternative | Reduced Development Alternative 3: east tower 19 → 12 stories (−174,958 sq ft) to avoid shading Plaza de César Chávez | CV-DSEIR p. 150 | "would reduce the height of the east tower from 19 stories to 12 stories" |
| approved | listed as approved, not constructed (Mar 2021) | WOZ-DSEIR doc p. 151 (PDF p. 157), Table 19 | "City View Plaza Project ... totaling approximately 3.8 million square feet of office and commercial space ... Approved but not constructed" |
| approval date | June 16, 2020, City Council | City page (search snippet only, **not verified**) | "approved by the City Council on June 16, 2020" |

No CEQA notice of determination for the 2020 approval is posted on CEQAnet (the CEQAnet CSV export for San José
lists only the 2018 NOP, the 2019 NOP and the 2020 SEIR under SCH 2018022032).

Overlap with `downtown-west`: none. Downtown West's boundary runs east only to about −121.8969 (west of SR 87);
CityView sits between Almaden Boulevard and Market Street (about −121.891 to −121.887), roughly 500 m east.
