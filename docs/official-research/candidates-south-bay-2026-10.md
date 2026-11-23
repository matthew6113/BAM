# Official-source findings: South Bay (Santa Clara County) projects not yet on the map

Checked 2026-10-19. Matthew asked on 2026-10-19 for more South Bay projects ("I feel like we are still missing a
lot of projects in San Francisco, as well as south bay"). This group screened Santa Clara County for the largest
active projects not on the map, researched the strongest and drew four: **Mission Point** and **Freedom Circle**
(Santa Clara), **Seely Avenue Mixed-Use** and the **Pleasant Hills Golf Course redevelopment** (San José). The
Berkeley Space Center at NASA Ames was left to another agent.

How it was read. The screen used CEQAnet's CSV export for Santa Clara County, Jan 1, 2019 to Oct 19, 2026, for
document types EIR, NOP, FIN, NOD, SIR, ADM and SBE (and NOE from 2024): about 3,000 rows, filtered for 900+
homes, 800,000+ sq ft or 60+ acres and for every name in the brief. Candidates were then read on CEQAnet (project
pages, document pages and attachments, downloaded and read with `pdftotext -layout`; figures rendered with
`pdftoppm` or read as vectors with pdfplumber). Parcels came from Santa Clara County's open data
(`data.sccgov.org`, dataset `ubcd-cewv`, updated Aug 2026). Every other city or county site the brief lists as
blocked refused this session too: `sanjoseca.gov` (403), `sanjose.legistar.com`, `santaclara.legistar.com`,
`webapi.legistar.com`, `legistar.granicus.com`, `geo.sanjoseca.gov`, `map.santaclaraca.gov`, `milpitas.gov`,
`cityofpaloalto.org`, `sjsu.edu`, `plandev.santaclaracounty.gov`, `sccgov.org`, `data.ca.gov`, `dtsc.ca.gov` and
the cities of Sunnyvale and Mountain View. So no council resolution, staff report, permit record or approved plan
set was read; approvals rest on the notices of determination on CEQAnet. Local copies are in
`data/raw/official/{mission-point,seely-avenue,freedom-circle,pleasant-hills,550-e-brokaw,santana-row,sjsu-campus-master-plan,patrick-henry-drive}/`
(git-ignored). Page numbers are PDF pages unless "doc p." is given.

URL shorthand (all `https://ceqanet.lci.ca.gov/`):
- `MP/n` = `2018072068/n` (Mission Point documents): 1 and 2 the 2018 NOPs, 3 the 2022 NOP, 4 the Draft EIR
  (attachment `Nn5ZMq`, Nov 2023, 722 pp.; sha256 `33f91f05…f2`), 5 the NOD of Nov 19, 2024 (attachment `nzGYrG`;
  sha256 `dae5f582…23`), 6 the Final EIR (attachment `WU7KF1`, Apr 2024, 315 pp.; sha256 `55a4fdb6…fc`), 7 the NOD
  of Dec 3, 2024 (attachment `l2As6p`; sha256 `63a119b2…7d`)
- `SA/n` = `2022020565/n` (Seely Avenue): 1 the NOP (attachment `6aoaJZ`), 2 and 4 the Draft EIR as circulated in
  Jan and Mar 2024 (attachment `4/Attachment/O2WLAL`, 353 pp.; sha256 `5913b863…86`), 5 the NOD (attachment
  `Yi9Zn9`; sha256 `b2fb6f17…ed`) with the Final EIR Volume I (attachment `4SIxme`)
- `FC/n` = `2020060425/n` (Freedom Circle): 2 the NOP, 3 the Draft EIR (attachment `d6319_`, text volume, 733 pp.;
  sha256 `6a3d77dd…d3`), 4 the NOD of June 7, 2022 (attachment `SZMFf1`; sha256 `f936134f…d3`), 5 and 6 the NODs of
  Mar 25 and May 14, 2025 (attachments `CJkIqW`, `LrIjgg`), 7 DTSC's NOD of Aug 20, 2025
- `PH` = `2025100897` (Pleasant Hills NOP page); NOP attachment `2025100897/Attachment/Vo2HGJ` (12 pp.; sha256
  `371a4e49…4f`), notice of completion `2025100897/Attachment/lpp9sF`
- `SCC` = `https://data.sccgov.org/d/ubcd-cewv` (Santa Clara County parcels)

## Hosts needed in `src/projects/official.ts`

None. Every source is on `ceqanet.lci.ca.gov` or `data.sccgov.org` (`sccgov.org`, already listed).

## Summary

| # | project | city | stage (date) | size (official) | recommendation |
|---|---|---|---|---|---|
| 1 | Mission Point | Santa Clara | entitled (approved Nov 19 and Dec 3, 2024) | 48.6 acres; up to 2,600 homes, 2,211,000 gsf office/R&D, ~100,000 gsf retail | **INCLUDE** as `mission-point`, boundary + illustrative massing |
| 2 | Seely Avenue Mixed-Use | San José | entitled (approved Aug 13, 2024) | 22 acres; 1,472 homes, 18,965 sq ft retail, 2.5-acre park | **INCLUDE** as `seely-avenue`, boundary + illustrative massing |
| 3 | Freedom Circle (Irvine Company and Greystar sites) | Santa Clara | entitled (2022 and 2025 approvals) | 39 acres in a 108-acre focus area; 1,792 homes approved + 1,100 proposed | **INCLUDE** as `freedom-circle`, boundary only |
| 4 | Pleasant Hills Golf Course redevelopment | San José (annexation) | in entitlement (NOP Oct 14, 2025) | 113.5 acres; about 2,000 homes, 50,000 sq ft commercial | **INCLUDE** as `pleasant-hills`, boundary only |
| – | Santana Row Master Plan Update | San José | in entitlement (revised NOP Feb 2026) | +1,272,081 sq ft office in four buildings | lead: include next (see Leads) |
| – | CityView Plaza | San José | approved 2020; 2025 amendment not on CEQAnet | 3.79M sq ft (2020) | still held (see Leads) |

None of the four overlaps or lies within 600 m of a mapped project's boundary (checked against every file in
`data/boundaries/`).

---

## 1. mission-point (Santa Clara): INCLUDE

Recommendation: **INCLUDE**, stage `entitled`. A 48.6-acre redevelopment south of Tasman Drive between Patrick
Henry and Old Ironsides drives, approved in 2024 for up to 2,600 homes and 2.2 million gsf of office/R&D: well over
the bar, master-planned, multi-building, and not in the Oct 17 scan. It lies just north of the Patrick Henry Drive
Specific Plan area (across the Hetch Hetchy right-of-way) and south-west of `related-santa-clara`.

Documents read: MP/1, MP/2, MP/3 (pages); MP/4 Draft EIR (summary, Chapter 2 project description pp. 76-113,
Chapter 5 alternatives pp. 613-640, Figure 5-3 p. 621); MP/5 and MP/7 NODs (full); MP/6 Final EIR (Chapter 1,
pp. 1-12); the CEQAnet project page `Project/2018072068`.

| field | official value | source | verbatim quote |
|---|---|---|---|
| approved program | up to ~2,600 homes, 2,211,000 gsf office/R&D, ~100,000 gsf retail, ~10,000 gsf childcare, 3,000 gsf community; 4,915,000 gsf total | MP/5 NOD p. 1 (and MP/7) | "The Project would include up to 4,915,000 gross square feet (gsf) of new development, including up to 2,600 housing units approximately; 2,211,000 gsf of office/R&D space; approximately 100,000 gsf of neighborhood retail uses; and approximately 10,000 gsf of childcare facilities, along with 3,000 gsf of community space." |
| approval 1 | Nov 19, 2024, City of Santa Clara (lead agency); EIR, mitigation, SOC, findings | MP/5 NOD | "has approved the above described project on 11/19/24"; "An Environmental Impact Report was prepared"; "A statement of Overriding Considerations [was]" |
| approval 2 | Dec 3, 2024 | MP/7 NOD | "described project on 12/03/24"; attachment file name "Kylli_20210820-NOD_DA_Revised" |
| applicant | Kylli, Inc. | MP/7 NOD | "Project Applicant: Kylli, Inc." |
| site | nine APNs + Democracy Way ROW, ~48.6 acres; bounded by Tasman, Old Ironsides, Hetch Hetchy ROW, Patrick Henry | MP/7 NOD | "The Project site is located on nine parcels (assessor's parcel numbers [APNs] 104-04-150, 104 04 142, 104 04-143, 104-04-151, 104-04-112, 104-04-113, 104-04-065, 104-04-111, 104 04 064) and a roadway right-of-way (ROW) (Democracy Way) totaling approximately 48.6 acres. The Project site is generally located along the Great America Parkway corridor in Santa Clara and is bounded by Tasman Drive to the north, Old Ironsides Drive to the east, the ROW associated with the Hetch Hetchy aqueduct to the south, and Patrick Henry Drive to the west." |
| existing | four vacant light industrial buildings (142,050 gsf) and a parking lot used for Levi's Stadium events | MP/7 NOD; MP/4 p. 81 (doc p. 2-3) | "currently occupied by four vacant light industrial buildings on the northern portion of the site and a paved surface parking lot"; "primarily temporary parking for events at Levi's Stadium, which uses 3,300 parking spaces" (FEIR p. 8) |
| parcel areas | 2.99 + 1.99 + 1.57 + 2.81 + 6.33 + 7.15 + 7.16 + 8.74 + 7.27 + ROW 2.60 = 48.6 acres | MP/4 p. 81, Table 2-1 | Table rows "104-04-150 2.99 ... N/A a 2.60 Total 48.6" |
| which design was approved | the Reduced Office/Increased Housing Alternative | MP/6 p. 8 (doc p. 1-4); MP/4 p. 625 Table 5-4 | "removing all 789,000 gsf of office/R&D space in Area C and replacing it with 800 multi-family housing units ... Thus, the Reduced Office/Increased Housing Alternative would result in up to 4,913,000 gsf of new development, consisting of up to 2,600 housing units, approximately 2,211,000 gsf of office/R&D space" |
| alternative totals | up to 2,600 units; up to 2,300,000 gsf commercial (office/R&D, retail); up to 16.2 acres publicly accessible open space; up to 9,400 parking | MP/4 p. 625, Table 5-4 | "Residential Up to 1,800 units Up to 2,600 units"; "Commercial (Office/R&D, Neighborhood Retail) Up to 3,100,000 gsf Up to 2,300,000 gsf"; "Publicly Accessible Open Space Up to 16.2 acres Up to 16.2 acres" |
| open space (approval text) | up to 24 acres publicly accessible, up to 13 acres private | MP/5 NOD | "the Project would include up to 24 acres of publicly accessible open space and up to 13 acres of private open space/sustainability zones throughout the Project site, subject to final design" |
| affordable | City inclusionary policy; Draft EIR: at least 15% (proposed project) | MP/5 NOD; MP/4 p. 86 | "The Project would also provide affordable housing in compliance with the City's Inclusionary Housing Policy requirements"; "At least 15 percent of the homes would be affordable." |
| areas | A 13.3, B 8.9, C 12.7, D 13.7 acres; heights (proposed project) A 123, B 153, C 132, D 202 ft | MP/4 p. 87, Table 2-3 | "A 13.3 123 feet ... B 8.9 153 feet ... C 12.7 132 feet ... D 13.7 202 feet" |
| heights (approved alternative) | A 63-138 ft (5-10 levels), B 108-153 (8-10), C 72-108 (7-10), D 72-202 (7-20); "approximate" | MP/4 p. 621, Figure 5-3 | "Max H.138' up to 10 Levels", "Min H.63' up to 5 Levels", "Max H.153' up to 10 Levels", "Min H.108' up to 8 Levels", "Max H.108' up to 10 Levels", "Min H.72' up to 7 Levels" (twice), "Max H.202' up to 20 Levels"; "*All elevation heights shown are approximate." |
| alternative heights per Table 5-1 | "Same as Project" | MP/4 p. 617 | "Maximum Building Heights ... Same as Project" |
| substation | ~18,000 gsf, Silicon Valley Power | MP/4 p. 86 | "An electrical distribution substation, to be owned and operated by Silicon Valley Power (SVP), would be located in Area C"; Figure 5-3: "Substation might be relocated into area B" |
| jobs | ~9,408 net new employees (alternative) | MP/4 p. 625; MP/7 page ("Jobs 9408") | "approximately 9,408 net new employees" |
| history | 2018 NOPs: 10.61M gsf, 6,000 homes, buildings 240-450 ft and a tower up to 600 ft; 2022 NOP: 1,800 homes, 3M gsf office | MP/1, MP/2, MP/3 pages | "up to 10.61 M gsf of uses within buildings from 240 ft to 450 ft tall, and a tower of up to 600 ft"; "up to 1.8 million gross square feet (gsf) of residential uses (1,800 units), 3 million gsf of office buildings" |
| Draft EIR review | Nov 17, 2023 to Jan 2, 2024 | MP/6 p. 9 | "circulated for a 46-day public review period between November 17, 2023, and January 2, 2024" |
| construction schedule (proposed project) | C 2025-28, D 2027-33, B 2028-32, A 2029-34 | MP/4 p. 113, Table 2-7 | "The actual sequence of construction would occur in response to market demands" |

Stage reasoning: **entitled**. Two NODs record approvals (Nov 19 and Dec 3, 2024). No permit, demolition or
construction record could be checked (Santa Clara's permit and agenda sites are blocked), and the County's
parcel layer still shows the nine original parcels (no subdivision recorded).

Boundary: `official_boundaries.py`, constant `MISSION_POINT_APNS` and `SPECS["mission-point"]`: the nine County
parcels named in the NOD, joined over Democracy Way (`close_m` 20). Result **48.4 acres** (approval 48.6; the
parcels alone are 46.1, against Table 2-1's 46.0). Accuracy official.

Massing: `massing_mission_point.py` → `data/massing/mission-point.geojson`, 25 illustrative features. Figure 5-3 is
the approved alternative's conceptual site plan: a raster base (3,252 × 2,103 px) with hand-drawn vector building
outlines (stroke 4.76 and 6.09 pt), blue (office) and yellow (residential) scribble fills, and per-area height
call-outs. Footprints = faces enclosed by the outlines that carry office or residential scribble (courtyards are
left open), grown by half the stroke. Georeference: the base raster's blue-grey dash-dot project boundary (6,312
pixels) fitted by trimmed ICP to the parcel boundary from four corners (start RMS 2.1 m), 1.533 m/pt, rotation
0.56°, **RMS 0.3 m** over 80% of the boundary pixels. Heights: the building each "Max" leader dot points at gets
the maximum (Area A 138 ft, B 153, C 108, D 202), every other building the area's minimum (A 63, B 108, C 72,
D 72): 10 office footprints in A, 4 in B, 4 residential in C, 7 in D. This is a low reading of approximate
ranges; the notes say so. Table 2-3's maxima (A 123, C 132) disagree with Figure 5-3 and are noted. Stage
`entitled`; phase = the area.

Press-only facts: none used; no `reported` block.

Open items: the Dec 3, 2024 action (the NOD's file name suggests a development agreement); the General Plan
amendment and PD rezoning resolutions; open-space acreage (24 vs 16.2 acres); affordable count; any permits.

---

## 2. seely-avenue (San José): INCLUDE

Recommendation: **INCLUDE**, stage `entitled`. 1,472 homes on 22 acres in North San José, approved Aug 13, 2024:
over the 1,000-home bar, multi-building (three apartment buildings, an affordable building, 26 townhome blocks,
a public park). The County's parcel layer already shows the project's subdivision lots.

Documents read: SA/1 NOP (pp. 1-6); SA/4 Draft EIR (summary pp. 36-40, Chapter 2 pp. 47-76, Figure 2-4 p. 52);
SA/5 NOD (full) and Final EIR Volume I (pp. 1-12).

| field | official value | source | verbatim quote |
|---|---|---|---|
| approval | City Council, Aug 13, 2024; PD rezoning to IP(PD) and PD permit; FEIR; SOC (historical resources) | SA/5 NOD pp. 2-3 | "This is to advise that the City Council of San José approved the above-described project on August 13, 2024"; "adopted a Statement of Overriding Considerations" (for "unavoidable significant environmental effects identified in the FEIR related to historical resources") |
| program | 1,472 homes (townhomes + 6-7-story apartments), 18,965 sq ft retail, 2.5-acre park, 0.11-acre well site | SA/5 NOD p. 2 | "for the development of 1,472 residential units consisting of a mix of three-story townhomes and six- to seven-story apartment buildings, 18,965 square feet of general neighborhood retail space, and a 2.5-acre public park. The project also includes the dedication of an approximately 0.11 acre site to the San Jose Municipal Water System" |
| files, applicant | PDC21-035 / PD22-022 / ER21-284; The Hanover Company | SA/5 NOD pp. 1-2 | "File Numbers: PDC21-035/ PD22-022/ER21-284"; "Project Applicant: The Hanover Company (Attn: Scott Youdall)" |
| site | APNs 097-15-033, -034, part of 097-66-004; ~22 acres; Seely Ave, Montague Expwy, Coyote Creek, Epic Way | SA/5 NOD p. 2; SA/4 p. 47 | "The project site is bound by Seely Avenue to the west, Montague Expressway to the south, Coyote Creek to the east, and Epic Way and existing commercial properties to the north."; "Assessor's Parcel Numbers: 097-15-033, 097-15-034, and 097-66-004"; DEIR: "a portion of 097-66-004 for a total area of 22 acres" |
| components | townhomes 154 (329,844 sf lot); A 397 + 6,427 sf retail (152,096); B 372 + 5,578 (126,318); C 371 + 6,960 (127,323); affordable 178 (53,825); park 109,549; well 4,576 | SA/4 p. 55, Table 2-1 | "Townhomes 154 - 329,844 / Building A Market-Rate Apartments / Ground Floor Retail 397 6,427 152,096 / ... Affordable Apartment Building 178 - 53,825 / Public Park - - 109,549 ... Total 1,472 18,965 996,682" |
| heights | A 69 ft, B 79, C 79, affordable 82, townhomes 30 (ground to roof) | SA/4 p. 56, Table 2-2 | "Building A 69 feet / Building B 79 feet / Building C 79 feet / Affordable Apartment Building 82 feet / Townhomes 30 feet"; "Height measured from ground to roof" |
| stories | A 6, B 7, C 7; affordable 6; townhomes 3; parking above grade | SA/4 p. 56 | "Buildings A, B and C – are proposed as six stories, seven stories, and seven stories, respectively"; "no underground parking is proposed"; "The six-story, 178-unit affordable apartment building" |
| phasing | 1 infrastructure + well; 2 townhomes; 3 A; 4 affordable; 5 B; 6 C (2024-2028 schedule) | SA/4 p. 75, Table 2-4 | "This schedule represents the most aggressive feasible construction schedule as of the writing of this EIR"; Table 2-4 gives Building A 399 units |
| history | NOP: 1,470 homes, ~52,000 sq ft retail | SA/1 p. 2 | "The project includes development of 1,470 residential units, approximately 52,000 square-feet of retail space, and a public park on an approximately 22-acre site." |
| NOP date | circulated Feb 23, 2022; comments to Apr 5, 2022 | SA/4 p. 40 (doc p. 3) | "The NOP was initially circulated to local, state, and federal agencies on February 23, 2022." |
| Draft EIR | Jan 16, 2024 and again Mar 19 to May 3, 2024 | Final EIR Vol. I p. 4 | "The EIR was released for public review on January 16, 2024, for a 45-day circulation period, which was then extended to 60 days, and again on March 19, 2024 for an additional 45-day circulation period due to a procedural error" |
| historic farm | 7 contributing structures of a potential historic district (Japanese farming); Sakauye house | SA/4 p. 38 | "7 were determined to contribute to the potential historic district associated with the events of Japanese farming and farming in Santa Clara Valley: ca. 1920 cottage, two separate ca. 1930 pump houses, ca. 1920 "Sakauye house"" |

Stage reasoning: **entitled**. Council approval Aug 13, 2024 (NOD). The County's parcel layer now holds the
project's lots (the approval's APNs are retired), which suggests a final map has recorded, but no permit or
inspection record could be checked, so not `infrastructure` or `construction`.

Boundary: `SEELY_AVENUE_APNS` (097-15-042, -045, -046, -047, -048, -049 and 097-23-141 to -166) plus the
unnumbered street and common lots inside `SEELY_AVENUE_COMMON_BOX`; 42 parcels, **22.2 acres**. Accuracy
approximate, because the approval names the predecessor APNs; the successor lots match Table 2-1 (A −1.4%,
B +0.6%, C 0.0%, affordable +1.3%, park 2.505 vs 2.515 acres, well 0.111 vs 0.105 acres).

Massing: `massing_seely_avenue.py` → 30 illustrative features: Building A (097-15-042) 69 ft, B (-045) 79 ft,
C (-049) 79 ft, affordable (-046) 82 ft, 26 townhome lots 30 ft. Lots matched by area and by position on
Figure 2-4 (C beside the existing office building at 2670 Seely, A at Montague, B and the affordable building on
the levee side). Whole lots are drawn, so garages and courtyards are inside the envelopes; labelled illustrative.
Park, well, streets not drawn. Phases from Table 2-4.

Press-only facts: none used.

Open items: construction status; Building A 397 vs 399; approved plan set (heights may have changed in the PD
permit).

---

## 3. freedom-circle (Santa Clara): INCLUDE

Recommendation: **INCLUDE**, stage `entitled`. Two housing projects in the City's Freedom Circle Focus Area
(about 108 acres between Great America Parkway, Great America, San Tomas Aquino Creek and US 101): the Irvine
Company's 1,792 homes at 2518 Mission College Boulevard (approved 2025) and Greystar's 1,100 homes on a 13.3-acre
site re-designated for housing in 2022, with a state-approved cleanup plan (2025). The Irvine Company project
alone clears the bar. Drawn as the two approved sites, not the whole focus area, whose remaining capacity waits on
a future planning study.

Documents read: FC/2 (page), FC/3 Draft EIR text (pp. 1-30, 99-110), FC/4 NOD (full, incl. the project
description page), FC/5 and FC/6 NODs (full), FC/7 DTSC NOD (page), CEQAnet project page.

| field | official value | source | verbatim quote |
|---|---|---|---|
| focus area | ~108 gross acres | FC/4 p. 5; FC/3 p. 23 | "The proposed Freedom Circle Focus Area encompasses approximately 108 gross acres ... bounded by San Tomas Aquino Creek to the east, Great America Parkway to the west, Great America Theme Park to the north, and Highway 101 to the south." (CEQAnet's record lists 121 acres) |
| focus area capacity | 2,500 homes beyond Greystar's and 2M sq ft more office, subject to a future planning study | FC/4 p. 5 | "The Focus Area Plan would allow, subject to a future planning study, 2,500 dwelling units beyond those anticipated in the Greystar General Plan Amendment, and 2 million square feet of additional office space beyond that allowed under the current high-Intensity office designation." |
| Greystar | 13.3 acres; High Intensity Office → Very High Density Residential (51-100 du/ac); 1,100 homes in three 7-story buildings ≤100 ft; 2-acre park | FC/4 p. 5 | "Greystar is proposing a total of 1,100 dwelling units in three 7-story buildings, all of which are proposed to be a maximum of 100 feet In height. The proposal also includes a two-acre public park with a connection to the San Tomas Aquino Creek trail." |
| Greystar (Draft EIR) | 1,075 homes, ~2,000 sq ft amenity space; vacant site | FC/3 pp. 10, 104 | "three seven-story residential buildings with 1,075 residences, plus approximately 2,000 square feet of neighborhood amenity space"; "previously used for construction staging and parking but is now vacant" |
| Greystar APNs | 104-40-021 and 104-40-036 | FC/3 p. 273 (cultural resources citation); CEQAnet FC/4 record | "Residential Project, City of Santa Clara, Santa Clara County (APN 104-40-021 and 104-40-036)"; FC/4 page: "Parcel # 104-40-036, -021" |
| 2022 approval | June 7, 2022 (EIR certified; Focus Area Plan and Greystar GPA) | FC/4 p. 4; FC/7 page | "has approved the above described project on June 7, 2022"; DTSC: "The Freedom Circle Focus Area Plan / Greystar Project General Plan Amendment Environmental Impact Report (EIR) was certified by the City of Santa Clara on June 7, 2022." |
| Irvine Company approval | Mar 25, 2025: EIR addendum, GPA, rezone, VTM for 1,792 homes at 2518 Mission College Blvd (APN 104-40-019, 25.7 ac) | FC/5 NOD; FC/5 page | "Implementing the Freedom Circle Focus Area Plan by adopting an Addendum to the Freedom Circle Future Focus Area Plan Environmental Impact Report and Mitigation Monitoring and Reporting Program, General Plan Amendment, Rezone, and Vesting Tentative Subdivision Map for the Property Located at 2518 Mission College Boulevard to Allow the Development of 1,792 Residential Units"; "Project Applicant: Irvine Company"; "03/25/25"; page: "Total Acres 25.7 Parcel # 104-40-019" |
| architectural review | May 14, 2025 | FC/6 NOD | "Architectural Review to Allow the Development of 1,792 Residential Units ... in the Freedom Circle Future Focus Area"; "05/14/25" |
| site cleanup | DTSC approved a remedial action plan Aug 20, 2025: ~100,000 cu yd of soil (arsenic, lead, dieldrin), 13.3-acre site at 3925 and 3935 Freedom Circle; applicant CRE-GS Freedom Circle Phase I Owner, LLC | FC/7 page | "The cleanup of the site will consist of excavation and offsite disposal of approximately 100,000 cubic yards of contaminated soil."; "Approved On 8/20/2025"; "CRE-GS Freedom Circle Phase I Owner, LLC" |
| NOP, Draft EIR | June 19, 2020; Nov 8, 2021 | CEQAnet project page | "NOP City of Santa Clara 6/19/2020"; "EIR City of Santa Clara 11/8/2021" |

Stage reasoning: **entitled**. The Irvine Company project has GPA, rezoning, map and architectural approvals; the
Greystar site has its General Plan amendment and an approved cleanup plan. Greystar's later zoning and design
approvals weren't found, and no construction record could be checked.

Boundary: `FREEDOM_CIRCLE_APNS` (104-40-019, -021, -036), two pieces either side of Freedom Circle, **39.0 acres**
(25.74 + 8.28 + 5.04). Accuracy official.

Massing: none. The Irvine Company's plans and the 2025 addendum are on `santaclaraca.gov` (blocked); Greystar's
building approvals weren't found and the 2021 Draft EIR gives heights but no dimensioned site plan to place them.

Press-only facts: none used.

Open items: Greystar's zoning/architecture approvals and final count (1,100 vs 1,075); the Irvine Company design
(heights, affordability, open space); whether the 1,792 homes count against the 2,500.

---

## 4. pleasant-hills (San José): INCLUDE

Recommendation: **INCLUDE**, stage `entitlement`. The former Pleasant Hills and Cypress Greens golf courses, 113.5
acres in unincorporated east San José, proposed for about 2,000 homes with annexation into the City; an NOP was
issued Oct 2025. Over the bar and newly active.

Documents read: PH page and project page (`Project/2025100897`: "1 documents in project"); NOP (all 12 pp.); notice
of completion (pp. 1-2).

| field | official value | source | verbatim quote |
|---|---|---|---|
| NOP | Oct 14, 2025 (City); received by CEQAnet Oct 20, 2025; scoping meeting Oct 29; comments to Nov 14, 2025 | NOP pp. 1-2 | "Date: October 14, 2025"; "When: October 29, 2025 from 6:00 p.m. to 8:00 p.m. Where: August Boeger Middle School Cafeteria"; "until 5:00 p.m. on November 14, 2025" |
| files, applicant | GP22-010, Evergreen 204, PDC25-015, PD25-007, T25-004, ER23-050; Lakeside Communities, LLC | NOP p. 2 | "FILE NOS: GP22-010, EVERGREEN 204, PDC25-015, PD25-007, T25-004, ER23-050 PROJECT APPLICANT: LAKESIDE COMMUNITIES, LLC" |
| site | 113.5 gross acres, APNs 649-23-001 and 649-24-013, 2050-2079 S White Rd; golf courses closed 2004 | NOP p. 3 | "The approximately 113.5-acre project site encompasses two parcels (Assessor's Parcel Numbers 649-23-001 and 649-24-013,), located at 2050-2079 South White Road in east San José."; "formerly operated as the Pleasant Hills Golf Course (PHGC) and the Cypress Greens Golf Course until 2004, when the golf courses closed" |
| entitlements | annexation, GPA, PD prezoning, vesting tentative map, PD permit | NOP p. 2 | "The project includes an annexation into the City of San José the 113.5-gross-acre project site ... Additional entitlements requested include a General Plan Amendment (GPA) and Prezoning to a Planned Development (PD) Zoning District, a Vesting Tentative Map approval to subdivide lots, and a Planned Development Permit" |
| program | ~2,000 homes: ~362 single-family, ~1,017 townhouses, ~300 market-rate multifamily, ~321 affordable multifamily | NOP p. 4 | "around 2,000 residential units which would include a mix of market-rate single-family houses (approximately 362 units), market-rate townhouses (approximately 1,017 units), market rate multi-family dwelling units (approximately 300 units), and affordable multi-family dwelling units (approximately 321 units)" |
| heights | single-family 2 stories/30 ft; townhomes 4 stories/55 ft; two 7-story mixed-use buildings up to 120 ft | NOP p. 4 | "The single-family houses would be a maximum of two stories with a height of up to 30 feet. The townhomes would be a maximum of four stories with a height of up to 55 feet. The affordable multi-family dwelling units would be located in two seven-story, mixed-use buildings with a height of up to 120 feet." |
| commercial | up to 50,000 sq ft ground floor | NOP p. 4 | "The proposed mixed-use buildings would include up to 50,000 square feet of ground floor commercial uses." |
| open space | up to 13.8 acres (Park 1 ≤5, Park 2 ≤3.4, ~5.4 along S White Rd) | NOP p. 5 | "public and/or private open space totaling up to 13.8 acres" |
| alternative | City-requested 2,850-home alternative | NOP p. 7 | "The EIR will also include an alternative requested by the City to include an increased housing unit count of 2,850 units." |
| excluded parcel | 0.6-acre 2079 Flint Avenue, annexed but not part of the project | NOP p. 3 | "The 0.6-acre parcel at 2079 Flint Avenue (APN 649-21-014) is not part of the project but will be analyzed in the EIR as part of the annexation." (the NOC and the County give 649-24-014) |
| current designation | County: Private Recreation and Open Space | NOC p. 1 | "County of Santa Clara Land Use Designation: Private Recreation and Open Space" |

Stage reasoning: **entitlement** (NOP issued; no Draft EIR on CEQAnet as of Oct 19, 2026; no approvals).

Boundary: `PLEASANT_HILLS_APNS` (649-23-001, 649-24-013), **113.1 acres**, official. The Flint Avenue lot is left
out.

Massing: none. A proposal at NOP stage; NOP Figure 4 shows neighborhoods, not buildings.

Press-only facts: none used.

Open items: Draft EIR date; annexation progress; the Flint Avenue APN typo.

---

## Candidates named in the brief, and other leads: not added

Each: size (official figure), stage, official URL, recommendation.

- **CityView Plaza** (San José; SCH 2018022032). 3.79M sq ft in three 19-story towers, approved 2020 (see
  `candidates-orchards-cityview.md`). CEQAnet still shows only the 2018 NOP, 2019 NOP and 2020 SEIR; the 2025
  addendum (H25-008) and its approval are not posted there (searched NOD, NOE, ADM, SIR, all 2019-2026).
  https://ceqanet.lci.ca.gov/Project/2018022032. **Still held**: the amended scope can't be read.
- **Santana Row Master Plan Update** (San José; SCH 2013122059, revised NOP Feb 13, 2026; earlier NOP SCH
  2022110177, Nov 2022). Federal Realty; +1,272,081 sq ft of office over the existing entitlement in four buildings:
  Lot 1A/B/C 700,000 sq ft (144 ft), Lot 2B 325,000 (144 ft), Lot 10A 200,000 (139 ft), Lot 17 275,000 (162 ft), on
  the 42.53-acre Santana Row PD site (NOP Table 4.0-1, p. 9; Figure 4 lot diagram, vector, p. 8). Built today: 834 homes,
  214 hotel rooms, 606,535 sq ft office (Table 3.0-1). https://ceqanet.lci.ca.gov/2013122059/3 (NOP attachment
  `lrKplZ`). **Recommend include next** (meets the bar, in formal review): boundary from the nine NOP APNs, and the
  four lots as envelopes from Figure 4 at Table 4.0-1's heights. Not drawn here for time.
- **Patrick Henry Drive Specific Plan** (Santa Clara; SCH 2019120515). 73.59 acres; 12,000 net new homes (or 10,300
  + 785,000 sq ft office); adopted Mar 22, 2022 (NOD). Only one housing project found inside it: 4590 Patrick
  Henry Drive, 284 homes in an eight-story building, approved Nov 13 and 19, 2024 (SCH 2024041111); the other
  recent approvals on Patrick Henry Drive are offices (5200 Patrick Henry, Arista, 362,660 sq ft, July 2024). https://ceqanet.lci.ca.gov/2019120515/4.
  **Borderline, hold**: plan-scale like `tasman-east` but no building confirmed started; revisit with permit data.
  Note it adjoins `mission-point` across the Hetch Hetchy right-of-way.
- **Gateway Crossings** (Santa Clara; SCH 2017022066). 1,565 homes, 197,000 sq ft commercial incl. a 225-room hotel,
  21.4 acres at 1205 Coleman Ave; approved July 9, 2019 (NOD). https://ceqanet.lci.ca.gov/2017022066/3. Its
  successor parcels (230-60-001 to -007, new street names Rickabaugh and Chastain) lie inside the
  `santa-clara-station-area` boundary. **Borderline**: over the bar, but it overlaps a mapped plan; Matthew's call
  whether to draw it as a project inside that plan. Construction status unknown.
- **550 E Brokaw** (San José; SCH 2021060414). Seven 8-story office buildings, 1,924,110 sq ft, approved Feb 28, 2023;
  **superseded**: a Director's Hearing on May 14, 2025 approved an addendum for "an approximately 333,360-square-foot,
  three-story warehouse and manufacturing building" on the same 19.7 acres (NOD, `2021060414/4`).
  **Exclude** (now below the bar).
- **Almaden Office Project** (San José; SP20-005, under SCH 2003042127). Two towers, 16 stories, ~2.05 million sq ft
  incl. 1,416,717 sq ft office, 3.57 acres at Almaden Blvd and Woz Way; approved Sept 14, 2021
  (https://ceqanet.lci.ca.gov/2003042127/31). **Borderline/exclude**: a single-block, two-tower building, closer to
  `oceanwide-center` than a master plan; status unknown.
- **Valley Title Commercial Project** (San José; SCH 2021070496). 20 stories, 301 ft, ~1.34M sq ft office, 2.8 acres
  at 300 S First St; Draft EIR Apr 2022, no NOD on CEQAnet (https://ceqanet.lci.ca.gov/2021070496/2). **Exclude**
  (single block; approval not found).
- **Woz Way Project** (San José; under SCH 2003042127). Two 20-story office towers, ~1.245M sq ft; Draft SEIR Mar 2021
  (https://ceqanet.lci.ca.gov/2003042127/23); no NOD found. **Exclude** (single block; approval not found).
- **Seely Avenue Mixed-Use**: added (above).
- **Coleman and Hedding Commercial Development** (San José; SCH 2023080477). City-initiated GPA and PD rezoning,
  up to 258,720 sq ft combined industrial/commercial, 11.37 acres; approved May 6, 2025
  (https://ceqanet.lci.ca.gov/2023080477/4). **Exclude** (below the bar).
- **Five Wounds Urban Village Plan** (San José; SCH 2024030360). 427.4 acres; ~8,022 homes of capacity (about 6,000
  new), 750,000 sq ft commercial; Draft EIR Aug 25, 2026 (https://ceqanet.lci.ca.gov/2024030360/2). **Exclude**: a
  many-owner area plan ("no specific project"), like East Whisman.
- **Gateway-Main Street Specific Plan** (Milpitas; SCH 2024070432). 605 acres, four focus areas; Draft EIR
  Apr 17, 2025, NOD Nov 4, 2025 (https://ceqanet.lci.ca.gov/2024070432/2). **Exclude** (area plan, many owners).
- **San José State University Campus Master Plan** (SCH 2023030435). ~3.7M gsf net new by 2045 (1.4M academic, 400,000
  support, ~900,000 for 2,100 student beds, up to 1,000 homes at the Alquist Building site), Main Campus 88.5 acres
  + South Campus 62 acres; approved by the CSU Trustees May 21, 2025 (https://ceqanet.lci.ca.gov/2023030435/3).
  **Borderline include later**: comparably large and adopted, but a long-range campus plan on two existing campuses
  with no building sites to draw except the Alquist housing; boundary would need the campus parcels or the EIR's
  figure.
- **El Camino Real Specific Plan** (Santa Clara; SCH 2025010508). 238.3 acres, 4,392 homes; NOD May 20, 2026
  (https://ceqanet.lci.ca.gov/2025010508/3). **Exclude** (corridor plan, many owners).
- **Stanford 2026 General Use Permit** (County of Santa Clara). No NOP or other CEQA document on CEQAnet as of Oct 19,
  2026 (only the 2023 Housing Element / Stanford Community Plan EIR, SCH 2022080196); `plandev.santaclaracounty.gov`
  blocked. **Hold** until a County NOP.
- **Platform 16, Park Habitat (Westbank), Santana West, Coleman Highline**: no CEQAnet document under these names
  (2019-2026 exports); likely cleared under program EIRs or before 2019, with records only on `sanjoseca.gov`.
  **Not verifiable here**; revisit with access to San José's site.
- **Communications Hill** (San José; SCH 2001062119): only a CDFW streambed NOD (June 26, 2024) for KB Home's
  "200-plus residential units" (https://ceqanet.lci.ca.gov/2001062119/6); the specific plan dates from 2009 and is
  partly built. **Exclude** (old plan; no new project-level document).
- **Downtown Sunnyvale / CityLine** (SCH 2018052020). Downtown Specific Plan amendments: 843 homes, 860,624 sq ft
  office, 260,063 sq ft commercial, 16 acres; Draft EIR Nov 2019, 12 NODs 2020-2023
  (https://ceqanet.lci.ca.gov/2018052020/15). **Borderline**: partly built; build status not verifiable without
  `sunnyvale.ca.gov`.
- **Lawrence Station Area Plan** (Sunnyvale; SCH 2013082030, 2019012022). Plan with individual projects (e.g. 172
  affordable homes, NOD Mar 23, 2026; Intuitive Surgical campus). **Exclude** (many-owner plan).
- **Freedom Circle**: added (above).
- **Milpitas Metro Specific Plan** (SCH 2006032091). +7,000 homes, 3M sq ft office, 700 hotel rooms; NOD Feb 7, 2023
  (https://ceqanet.lci.ca.gov/2006032091/8). **Exclude** (area plan around Milpitas BART, many owners).
- **Mountain View Terra Bella**: 1155-1185 Terra Bella office (~20,000 sq ft) and Terra Bella Public Storage & Alta
  Housing (4.8 acres) only. **Exclude** (small).
- **North Ventura Coordinated Area Plan** (Palo Alto; SCH 2023020691). +530 homes, 60 acres; NOD Aug 5, 2024.
  **Exclude** (below the bar).
- **Kaiser Permanente San José Medical Center** (SCH 2023050424): 685,000 sq ft hospital + 250,000 sq ft outpatient,
  40 acres; NOD Oct 10, 2024. **Good Samaritan Hospital** (SCH 2023060108): ~750,000 sq ft of hospital wings +
  200,000 sq ft MOB, 20 acres; NOD Nov 22, 2024. **Sutter Santa Clara Hospital** (SCH 2026040360): 850,000 sq ft,
  8 stories, 302 beds; NOP Apr 8, 2026. **Exclude all three** (single hospitals, under 1M sq ft).
- **Campbell Tech Park** (SCH 2024121066): 290 homes; Draft EIR Apr 15, 2026. **Exclude** (below the bar).
- **El Paseo & 1777 Saratoga Avenue** (San José; SCH 2020090521): 994 homes, 165,949 sq ft commercial, 10.7 acres;
  approved June 21, 2022 (https://ceqanet.lci.ca.gov/2020090521/4). **Borderline/exclude** (just under 1,000 homes).
- **Berryessa Road Residential and Office** (San José; SCH 2019049077): up to 910 homes and 658,000 sq ft office,
  13 acres; NOP Apr 2019 only. **Exclude** (no later document; next to `berryessa-flea-market`).
- **Central Arques Specific Plan** (Sunnyvale; SCH 2024071114): 80 acres, up to 3.49M gsf nonresidential studied,
  heights 75 → 100 ft; NOP July 29, 2024. **Exclude for now** (industrial/R&D zoning update, many owners; no Draft EIR).
- **Peery Park Specific Plan Amendment** (Sunnyvale; SCH 2015062013): +1.2M sq ft office/R&D, +1,632 homes, 450 acres;
  NOP Sept 30, 2026. **Exclude** (many-owner plan).
- **Petal Fields** (unincorporated County; SCH 2026040424): 838 homes on 134.5 acres; NOP Apr 9, 2026. **Exclude**
  (below the bar).
- **Santa Clara Downtown Precise Plan** (SCH 2022010282): 1,071 homes, 531,720 sq ft office, 197,900 sq ft
  commercial, 25 acres; NOD Dec 12, 2023. **Borderline** (precise plan for the old downtown; many parcels).
- **Mountain View R3 Zoning District Update** (SCH 2025070500, citywide, 16,000 homes) and **Moffett Boulevard
  Precise Plan** (SCH 2025080374, 950 homes): **Exclude** (zoning update; below the bar).

Already reflected: `tasman-east` records the Aug 28, 2026 Draft Supplemental EIR for its +1,500-home amendment
(SCH 2016122027, https://ceqanet.lci.ca.gov/2016122027/7); nothing to add.
