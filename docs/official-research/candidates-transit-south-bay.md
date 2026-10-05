# Candidate projects: BART station-area housing, Berryessa (San José), Tasman East (Santa Clara)

Checked 2026-10-05 against official records read in full text. Local copies are in `data/raw/official/bart-tod/`, `data/raw/official/berryessa-flea-market/` and `data/raw/official/tasman-east/` (git-ignored). Page numbers are PDF page numbers.

Shorthand:
- SJA = `https://legistar.granicus.com/sanjose/attachments/` (San José Legistar attachments)
- SCA = `https://santaclara.legistar1.com/santaclara/attachments/` (Santa Clara Legistar attachments)
- APR = California HCD, Housing Element Annual Progress Report data, Table A2 (`https://data.ca.gov/dataset/housing-element-annual-progress-report-apr-data-by-jurisdiction-and-year`, resource `fe505d9b-8c36-42ba-ba30-08bc4f34e022`). The city reports these rows to the state; the dataset says "License not specified" (state public record).

| candidate | recommendation | why |
|---|---|---|
| BART station-area housing | EXCLUDE | No single BART TOD site reaches the bar. The largest are West Oakland (762 homes, ~353,000 sq ft commercial, ~5 acres), El Cerrito Plaza (743), North Berkeley (739, ~8.2 acres) and Lake Merritt (557 homes, ~500,000 sq ft office). |
| Berryessa Flea Market South (Berryessa BART Urban Village) | INCLUDE | 61.5-acre PD zoning for up to 3,450 homes and 3.4 million sq ft of commercial, adopted 2021 and still in force; the owner withdrew its permit applications in 2023. |
| Tasman East Specific Plan | INCLUDE | 45-acre plan area for 4,500 homes, adopted 2018; state housing reports show certificates of occupancy for about 1,748 homes in seven buildings through 2025; an amendment adding 1,500 homes is in preparation. |

---

## bart-station-tod (BART station-area housing)

Documents read (bart.gov, BART's own site):
- Upcoming TOD projects: https://www.bart.gov/about/business/tod/upcoming
- Completed TOD projects: https://www.bart.gov/about/business/tod/completed
- West Oakland: https://www.bart.gov/about/business/tod/westoakland
- Lake Merritt: https://www.bart.gov/about/business/tod/lakemerritt
- North Berkeley: https://www.bart.gov/about/business/tod/north-berkeley
- Ashby: https://www.bart.gov/about/business/tod/ashby
- El Cerrito Plaza: https://www.bart.gov/about/business/tod/el-cerrito-plaza
- Millbrae: https://www.bart.gov/about/business/tod/millbrae
- City–BART Joint Vision and Priorities for Ashby and North Berkeley (2021): https://www.bart.gov/sites/default/files/docs/JVP_110421_versionfinal.pdf

| site | official value | source | verbatim quote |
|---|---|---|---|
| West Oakland (Mandela Station) | 762 homes; ~53,000 sq ft retail; ~300,000 sq ft office; ~5 acres; first phase (240 affordable homes) started Sept 2026 | westoakland page | "762 new residential units"; "300,000 sq. Ft. of office space"; "encompasses about five acres"; "Construction of the first phase (240-unit affordable housing development on the southwest portion of the site) commenced September 2026" |
| Lake Merritt | 557 homes; ~500,000 sq ft office; senior building under construction | lakemerritt page | "557 homes"; "500,000 square feet office space"; "Construction for the first phase ... began in October 2024" (the upcoming page says "started construction June 2025" and lists 97 + 439 + 100 = 636 homes: BART's own pages disagree) |
| North Berkeley | 739 homes on about 8.2 acres; city entitlements Dec 2024; first phase expected 2027 | north-berkeley page; upcoming page | "about 8.2 acres of BART-owned land"; "received its entitlement approvals from the City of Berkeley in December 2024"; "739 new homes, including 52% affordable homes"; "2027: First phase of construction anticipated to break ground" |
| Ashby (West Lot) | up to 600 homes on ~4 acres; developer selected July 2025; entitlements to be filed Q4 2026 | ashby page | "Up to 600 new apartments, half of which would be permanently affordable"; "a +/- 4-acre site (West Lot)" |
| Ashby and North Berkeley targets | 500–1,200 homes per station | JVP p.1 | "We anticipate a range of 500-1200 units at each station" |
| El Cerrito Plaza | 743 homes; first building broke ground Nov 2025 | el-cerrito-plaza page | "743 new homes"; "Construction of the first building in the El Cerrito Plaza TOD broke ground in November 2025" |
| Millbrae | 400 homes, ~150,000 sq ft office, 164-room hotel on 9.5 acres | millbrae page | "four buildings on 9.5 acres"; "approximately 150,000 square feet of office use"; "80 affordable units"; "320 market rate units" |
| Balboa Park | Upper Yard complete (131 homes, 2023) | completed page | "Completed in 2023, Kapuso at the Upper Yard ... into 131 deeply affordable homes" |
| Whole program to date | 4,232 homes and 874,000 sq ft at 15 stations | completed page | "delivered TODs at fifteen BART stations, totaling 4,232 new homes and 874,000 square feet of commercial space" |

Not found on BART's TOD pages: Fruitvale, Concord, El Cerrito del Norte. Their projects are delivered or smaller phases on city/county land, so they wouldn't change the result.

Recommendation: EXCLUDE. No single site reaches about 1,000 homes or 1 million sq ft. West Oakland (762 homes and ~353,000 sq ft of commercial on ~5 acres) and Lake Merritt (557–636 homes plus ~500,000 sq ft of office) come closest. The Berkeley vision document's top figure (1,200 per station) is a planning range, and the selected projects are 739 and up to 600. What would tip it: a decision to map a program-level "BART TOD" layer instead of individual projects (not a megaproject), or a single site re-planned above 1,000 homes.

Press-only: unit and office counts in YIMBY, NBC, Berkeleyside and EBALDC articles match BART's pages; no press-only facts are relied on.

---

## berryessa-flea-market (Berryessa BART Urban Village, Flea Market South)

Documents read (San José Legistar; sanjoseca.gov returns 403 to this environment):
- Council file 21-1627 (PDC17-051, Flea Market Southside rezoning), June 22–29, 2021: https://sanjose.legistar.com/LegislationDetail.aspx?ID=9321&GUID=FC76376F-92F9-46EF-B435-F9B192D06862
  - Planning Commission transmittal memo, May 28, 2021: SJA `0d77d0a5-c602-4d3a-b72a-9fef37220b5e.pdf`
  - Attachment 1 (supplemental memo and PC staff report PDC17-051): SJA `753c51c2-72aa-4fb0-b132-5221ece38a0d.pdf`
  - Attachment 3 (BBUV Plan, Chapter 3 Land Use): SJA `6a470a5f-c429-4338-a04a-8e4af2e07c00.pdf`; Attachment 2 (Chapter 4 Open Space): SJA `4c991260-606d-4c9f-a72c-c0f2c89e78a4.pdf`
  - Attachment 4 (replacement), PD development standards: SJA `d5de8bfb-f93d-481d-af19-a18a9b2fc422.pdf`
  - Attachment 5, PD zoning plan set "Market Park South Village" (37 MB): SJA `3a9bad7c-c607-4f36-9bb0-6215cb929306.pdf`
  - (d) Resolution, traffic policy credit (gives the 2007 history): SJA `07587a05-fe33-4070-ad08-13a28242582c.pdf`
- Council file 21-1626 (BBUV Plan, GP20-008 and C21-001): https://sanjose.legistar.com/LegislationDetail.aspx?ID=9320&GUID=52462B47-4D5A-4FEE-9F38-A2588DDC1C50
- Final adoption, Aug 3, 2021 (file 21-1668, item 2.2(e)): https://sanjose.legistar.com/LegislationDetail.aspx?ID=9356&GUID=DD9ABCD2-ABAE-458F-9C21-4CB6528F7B4D
  - Ordinance as reposted Aug 3, 2021: SJA `9ce708c6-a7c4-434d-9525-2a76c1d61e5c.pdf`
  - City Attorney's second revised summary of Council actions, Aug 2, 2021: SJA `df06cb67-b26c-40e8-9242-0e1939c01680.pdf`
- Berryessa Flea Market status report (file 25-497, Council May 13, 2025; CED Committee memo Mar 10, 2025): https://sanjose.legistar.com/LegislationDetail.aspx?ID=14563&GUID=4CF7F8A5-2E6C-4CFE-9A7B-EACDD409BEF2, memo SJA `78a6d04f-bc8f-4766-88eb-08854d2b0a74.pdf`
- Neighbouring site, for context only: 1655 Berryessa Road (file 25-804, Aug 12, 2025): https://sanjose.legistar.com/LegislationDetail.aspx?ID=14854&GUID=3E385B6B-F876-45A8-8FEA-EC8661478EA4

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | 61.5 gross acres | PC memo p.1; Ord. 30646 p.1 | "on an approximately 61.5-gross acre site located at 1590 Berryessa Road" |
| homes | up to 3,450 (density supports 1,700–3,450) | PC memo p.1; Att. 1 p.11 | "to allow up to 3,450 residential units"; "which supports between 1,700 and 3,450 dwelling units" |
| commercial | up to 3.4 million sq ft, minimum 1.5 million | PC memo p.1; Att. 4 p.3 | "up to 3.4 million square feet of commercial uses"; "A minimum of 1,500,000 square feet and up to 3,400,000 square feet" |
| land use split | commercial 16.3 ac; residential 13.1 ac; riparian/open space 17.1 ac; public open space/POPOS 5.0 ac; streets ~10 ac | Att. 1 p.11 | "riparian corridor/open space land uses on approximately 17.1 acres (27.8 %), public open space/privately owned, publicly accessible open space 5.0 acres (8.1%)" |
| urban market | 5-acre Urban Market is a condition of the rezoning | Ord. 30646 p.2; status memo p.2 | "The Planned Development zoning designated approximately five acres for an urban market" |
| vendor fund | owner $5 million, City $2.5 million | status memo p.2 | "required the property owner to contribute $5 million to a Flea Market Vendor Transition Fund. Additionally, the City pledged $2.5 million" |
| owner | Berryessa FM Development LLC | PC memo p.1 | "(BERRYESSA FM DEVELOPMENT LLC., OWNER)" |
| Planning Commission | recommended approval 5-1-1 (May 12, 2021) | PC memo p.1 | "The Planning Commission voted 5-1-1 (Commissioner Garcia opposed; Commissioner Caballero absent)" |
| Council approval | EIR certified and rezoning approved June 29, 2021 (heard June 22, 23, 29); 11-0 | Ord. 30646 p.1; City Attorney summary p.2 | "which FEIR was certified and adopted by the City Council on June 29, 2021"; "Approved 11-0." |
| ordinance | Ord. 30646, scheduled for final adoption Aug 3, 2021 | file 21-1668 item (e); City Attorney summary p.1; status memo p.2 | "The Flea Market rezoning ordinance is scheduled for final adoption as Item 2.2(e) on the August 3, 2021 City Council meeting agenda"; "(Ordinance No. 30646)" |
| BBUV Plan | adopted with the rezoning (GP20-008, C21-001; Ord. 30645 rezoned 28.86 ac of the East District) | file 21-1626; file 21-1668 item (d) | "Adoption of the Berryessa BART Urban Village Plan as the guiding policy document" |
| BBUV capacity | 22,100 jobs and 6,516 homes in the whole urban village | Att. 3 (Ch. 3) p.1 | "calls for 22,100 jobs and 6,516 housing units within the boundaries of the Urban Village" |
| earlier entitlement | 2007 Flea Market zoning (PDC03-108): up to 2,818 homes and 365,622 sq ft on ~120 acres north and south of Berryessa Rd | Res. (d) p.1 | "adopted a General Plan Amendment and Planned Development Rezoning to allow up to 2,818 residential units, 365,622 square feet of retail commercial" |
| status | owner withdrew the PD Permit and Tentative Map on Oct 24, 2023; an SB 330 preliminary application lapsed; no proposal as of Mar 2025 | status memo p.8 | "Flea Market ownership withdrew their Planned Development Permit and Tentative Map applications for site redevelopment on October 24, 2023"; "At this time there is no indication of an imminent development proposal for the site." |
| market today | about 430 vendors, ~700 stalls; market occupies ~18 net acres | Ord. 30646 p.2; Att. 1 p.6 | "rents approximately 700 vending spaces in the market to approximately 430 vendors" |
| zoning GIS | CP(PD), file 17051, approval date 2021-06-29, "DEVELOPEDASPD: No", note "SB79" | San José Zoning Districts layer (below) | attributes of OBJECTID 12061 |

Official stage: entitled. The PD zoning is in force (the city's 2025 memo and zoning GIS both treat it so), but the owner withdrew the follow-on permit and map applications in 2023 and nothing has been filed since (as of the March 2025 report). Not "paused" in the sense of halted work, since no work started; the stageNote says so plainly.

Boundary lead:
- San José Zoning Districts, `https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/401`, feature `OBJECTID = 12061` (`REZONINGFILE = '17051'`, `ZONING = 'CP(PD)'`); SHAPE_Area 2,738,651 sq ft (~62.9 ac) against the ordinance's 61.5 gross acres. License: Creative Commons Attribution (data.sanjoseca.gov "Zoning Districts" entry, license_id `cc-by`). Saved as `data/raw/official/berryessa-flea-market/zoning_17051.geojson`.
- Fallback: Ord. 30646 Exhibit A legal description (metes and bounds), APNs 254-17-052, -053, -007, -084, -095.

Massing lead: the PD development standards (Att. 4) defer heights to the BBUV Plan's building height diagram (Figure 5-4, Urban Design chapter; Figure 3-3 in Ch. 3). The plan set "Market Park South Village" (Att. 5) has the conceptual site plan, land-use blocks (residential 150–260 du/ac; commercial FAR 3.5–5.2) and the 5-acre market. The BBUV plan document itself sits on sanjoseca.gov, which this environment couldn't reach.

Press-only (not relied on): KTVU/CBS/San José Spotlight coverage of the June 2021 vote; San José Spotlight's "270 acres" for the urban village. Nothing press-only is needed for the record.

Hosts: all sources are on `sanjose.legistar.com`, `legistar.granicus.com/sanjose/` and `geo.sanjoseca.gov` (`.gov`), already accepted.

---

## tasman-east (Tasman East Specific Plan)

Documents read (Santa Clara Legistar; santaclaraca.gov returns 403 here):
- Council adoption, Nov 13, 2018 (file 18-1195): https://santaclara.legistar.com/LegislationDetail.aspx?ID=2564&GUID=D9199C07-2D4D-40E5-ADCB-5DBD76072087
  - Planning Commission report (Oct 24, 2018 hearing): SCA `0ee77387-fbe2-47c6-909b-80ff8f322ace.pdf`
  - Final EIR (Oct 2018, SCH 2016122027): SCA `f322e818-7feb-4e99-b91d-3ae13089ec4e.pdf`
  - Resolutions 18-8622, 18-8623, 18-8624 (scanned images, not text-readable): SCA `1a477c93-cfc5-41da-a2c5-05457fc175f1.pdf`, `bbcdf014-ab68-42d2-9dab-49d4b65572c7.pdf`, `c1e32364-41d5-427c-bfe0-9f29663ee8e3.pdf`
- Ordinance 1992 (Transit Neighborhood zoning) adopted Nov 27, 2018 (file 18-1563): https://santaclara.legistar.com/LegislationDetail.aspx?ID=2932&GUID=37402538-50C9-424D-B75B-9DAD56754795
- Implementation update, Aug 25, 2020 (file 20-745), with projects list: https://santaclara.legistar.com/LegislationDetail.aspx?ID=16641&GUID=4DEC47C5-0FD8-4DB8-8089-0D4A084678E7; list SCA `7d1fedcc-a476-418a-8f9e-3c70b00bd1fc.pdf`
- Plan Amendment (Calle del Sol paseo), EIR addendum and ALUC override, Nov 17, 2020 (file 20-744): https://santaclara.legistar.com/LegislationDetail.aspx?ID=16640&GUID=93BB39E7-8069-40D8-8A57-C03A6A8EA4B4
- Ordinance 2025 (TN zoning amendments) adopted Jan 12, 2021 (file 21-1406): https://santaclara.legistar.com/LegislationDetail.aspx?ID=17293&GUID=14DF03A8-064A-4EFA-9A6E-CEAEFA6BB3B4
- Parkland strategy and +1,500-unit amendment, Aug 2022 (file 22-1058): https://santaclara.legistar.com/LegislationDetail.aspx?ID=21103&GUID=8DB4A0CB-9F3D-4D0B-A43B-53AAAFF3C7EC
- BPAC update on the amendment, July 2023 (file 23-893): https://santaclara.legistar.com/LegislationDetail.aspx?ID=22513&GUID=A5A718A0-2FCB-4EF3-A706-29319066A10C
- Perkins + Will Amendment No. 7, approved Apr 21, 2026 (file 26-241): https://santaclara.legistar.com/LegislationDetail.aspx?ID=26106&GUID=25545734-0DA3-4CF9-94E7-6CB6C661AAE0
- APR Table A2 rows for Calle del Mundo, Calle de Luna, Calle del Sol, Tasman Dr and 5185 Lafayette St (saved as `data/raw/official/tasman-east/apr_a2_tasman_east.json`).

| field | official value | source | verbatim quote |
|---|---|---|---|
| acres | about 45 | PC report p.1; file 22-1058 report | "the redevelopment of an approximately 45 acre industrial area bounded by Tasman Drive to the south, the Guadalupe River to the East, the Santa Clara golf course to the north, and Lafayette Street to the west" |
| homes | 4,500 (plan capacity) | PC report p.1; file 22-1058 | "up to 4,500 residential units and 106,000 square feet of retail space" |
| retail | up to 106,000 sq ft | same | as above |
| open space | 10 acres: 5 ac public parkland plus 5 ac privately owned open space | file 22-1058 | "the amount of open space for the TESP was set at 10 acres, consisting of 5 acres of public parkland plus 5 acres of privately owned open space" |
| heights | low-rise to 65 ft, mid-rise 65–85 ft, high-rise 85–220 ft; towers capped at 220 ft or FAA Part 77, whichever is lower | PC report p.10; FEIR p.61 | "high rise (from 85 up to 220 feet in height)"; "Proposed towers within the plan area would not exceed 220 feet or the FAA Part 77 height limit, whichever is lower." |
| density | Transit Neighborhood, 85–350 du/ac (min 100 du/ac on sites over 1 acre per 2023 update) | PC report p.4; file 23-893 | "Transit Neighborhood (85 to 350 dwelling units per acre)" |
| adoption | Nov 13, 2018: Council adopts Res. 18-8622, 18-8623, 18-8624 and introduces Ord. 1992 | file 18-1195 history | "to adopt Resolutions #18-8622, #18-8623, #18-8624, and introduce Ordinance No. 1992" |
| zoning ordinance | Ord. 1992 adopted Nov 27, 2018 | file 18-1563 history | "to adopt Ordinance No. 1992" |
| first amendment | Nov 17, 2020: EIR addendum adopted, ALUC determination overridden, plan amended (Calle del Sol paseo) | file 20-744 history; file 26-241 report | "adopt Resolution No.____ to adopt the Addendum to the 2018 Final Environmental Impact Report Tasman East Specific Plan" |
| zoning amendment | Ord. 2025 adopted Jan 12, 2021 | file 21-1406 history | "to adopt Ordinance No. 2025, amending the Transit Neighborhood Zoning District" |
| applications | 11 applications, 4,484/4,485 of 4,500 units, ~65% of land | file 20-745; file 22-1058 | "In total, 4,484 residential units are either approved or pending"; "representing 4,485 of the 4,500 units available, but utilize only about 65% of the TESP land area" |
| construction 2020 | first projects under construction, incl. St. Anton's 196 affordable homes | file 20-745 | "the projects currently under construction also include a 100% affordable housing project with 196 rental units, developed by St. Anton Tasman East, LP" |
| certificates of occupancy | 2231 Calle del Mundo 196 (2022-12-21); 2333 Calle del Mundo 347 (2025-01-16); 2350 Calle de Luna 176 (2025-03-10); 5150 Calle del Sol 508 (2025-04-07); 2230 Calle del Mundo 186 (2025-08-21); 2310 Calle del Mundo 151 (2025-08-31); 2223 Calle de Luna 184 (2025-11-17). Total 1,748 | APR Table A2 | CO_ISSUE_DT1 and NO_OTHER_FORMS_OF_READINESS columns |
| permits not yet occupied | 2240 Calle de Luna, 311 homes, permit 2022-04-18; 2111 Tasman Dr entitled for 900 homes (2023-07-07); 5185 Lafayette St entitled for 198 (2023-11-02); 2200 Calle de Luna re-entitled for 583 (2023-02-26) | APR Table A2 | — |
| amendment | +1,500 homes (also ~20,000 sq ft retail, 20,000 sq ft co-working, 10,000 sq ft daycare); SEIR in preparation; consultant term extended to Dec 31, 2026 | file 23-893; file 26-241 | "the City obtained an SB2 Planning grant from the state to amend the Specific Plan to add 1,500 units of residential capacity"; "the updated CEQA work is anticipated to take longer than the previously approved contract termination date of June 2026" |

Notes and conflicts:
- The PC report's resolution text cites "SCH #2015022059", but the Final EIR cover and comment letters say SCH 2016122027. Use 2016122027 (the EIR's own cover).
- APR rows are as reported by the city each year. A building can have several CO rows; the totals above use the one CO row per address in 2022–2025. The 2240 Calle de Luna permit (311 homes) has no CO row yet.
- The developer list (SummerHill, Holland, Ensemble, Related, St. Anton, Greystar) is on the city's 2020 projects list; the plan is city-led with many owners.

Official stage: partial (certificates of occupancy for about 1,748 homes in seven buildings by Nov 2025, more permitted and entitled).

Boundary lead:
- City of Santa Clara zoning, `https://map.santaclaraca.gov/maps/rest/services/OPENDATA/RegionalZoningOpenData/MapServer/0`, filter `ZONGDSGN = 'TN' AND SPPLAN = 'TE'`: 37 parcels, ~42.4 acres (computed), dissolve to one outline. A further 10 TN parcels with no SPPLAN value (~8.6 ac) lie in the same block; check them against the plan's land-use figure before including (likely streets, the data center or parcels coded without the plan tag). Terms: `https://public-gis-missioncity.opendata.arcgis.com/pages/terms-of-use` (not read; confirm the license before shipping). Saved as `data/raw/official/tasman-east/tn_zoning.geojson`.
- Fallback: trace the Land Use Framework figure (SCA `86981332-ce20-4742-a8fd-7b687e94d41e.pdf`) or the 2022 districts diagram (SCA `5de59c12-cc80-49c9-b295-45ae5cc9615d.pdf`).

Massing lead: TESP design standards (low/mid/high-rise tiers, 220 ft cap, tower floorplate and separation rules in the FEIR p.61 text revisions; tiers on PC report p.10); per-building heights from each project's architectural review (2020 projects list gives units by address). Delivered buildings can come from Overture footprints once complete.

Press-only (not relied on): none needed.

Hosts: `santaclara.legistar.com`, `santaclara.legistar1.com` and `webapi.legistar.com/v1/santaclara/` are accepted; `map.santaclaraca.gov` and `data.ca.gov` are `.gov`.
