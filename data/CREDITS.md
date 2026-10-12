# Credits and licenses

Every dataset, font and library the map uses, with its license and the attribution it
requires. The in-map credit line (`src/ui/Credits.tsx`) carries the attribution that
OpenStreetMap and Overture require. Keep the two in sync.

## Base map data

All base map data comes from **Overture Maps Foundation**, release `2026-09-23.1`, read
from `s3://overturemaps-us-west-2` (see `pipeline/bam_pipeline/config.py`).

| Layer | Overture theme/type | Underlying sources | License |
|---|---|---|---|
| Building footprints | buildings/building | OpenStreetMap (83.4% of footprints), Microsoft ML Buildings (14.1%), Esri Community Maps (2.5%) | ODbL 1.0 (Esri contributions: CC BY 4.0 with OpenStreetMap waivers) |
| Building heights | buildings/building `height` | OpenStreetMap, Esri Community Maps, USGS 3DEP lidar (via Overture). Microsoft ML height estimates are removed. | ODbL 1.0 |
| Water, shoreline | base/water, base/land_use (salt ponds) | OpenStreetMap | ODbL 1.0 |
| County extent, city label points | divisions/division_area, divisions/division | OpenStreetMap | ODbL 1.0 |
| Freeways, rail, ferries (optional layer) | transportation/segment | OpenStreetMap | ODbL 1.0 |

Shares of footprints by source were measured over the 2,547,306 buildings in the nine
counties (see `data/manifest.json`).

**Required attribution:** "© OpenStreetMap contributors, Overture Maps Foundation".
Overture also asks that Microsoft and Esri Community Maps contributors be credited for
the buildings theme. The credit line is shown on load and collapses after the first
interaction or five seconds. It stays one click away, which OpenStreetMap's attribution
guidelines allow.

**Share-alike (ODbL):** the PMTiles in `public/generated/tiles/` are derived from
ODbL data and are published under ODbL 1.0, with their attribution and license written
into the tile metadata. The pipeline in `pipeline/` rebuilds them from the public
Overture release, and the clipped extract should be archived (see README) because
Overture removes releases after about 60 days. The deploy workflow keeps a copy as the
GitHub release `overture-2026-09-23.1` in this repository, under the same license and attribution.

Microsoft distributes its building footprints under ODbL (US Building Footprints) and
CDLA-Permissive-2.0 (Global ML Building Footprints). This map uses them only through
Overture, which labels them ODbL.

## Project documents cited in `data/projects.json`

Official plan documents are public records, cited by URL in each project's `sources`.
For example, the Potrero Power Station Mixed-Use Development Project Draft EIR (SF
Planning, Case No. 2017-011878ENV, Oct 2018) is at
https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf.

## Traced project geometry (`data/boundaries/`, `data/massing/`)

| Project | What | Source | License / notes |
|---|---|---|---|
| 36 projects (see `pipeline/bam_pipeline/sites/official_boundaries.py`) | Site boundaries | Official GIS layers, each named in its boundary file: DataSF Zoning Map – Special Use Districts (5yf5-ms5f) and Height and Bulk Districts (h9wh-cg3m), Public Domain U.S. Government; DataSF Former Redevelopment Agency Project Areas (m288-24sn) and Parcels (acdm-wktn), ODC PDDL 1.0; City of Menlo Park parcels, CC0; City of San José zoning, CC-BY 4.0 (credit: City of San José); City of Mountain View parcels, Sunnyvale General Plan, Brisbane plan boundary, Oakland zoning, Santa Clara County and Alameda County parcels, City of Santa Clara zoning (ODC PDDL 1.0 under its Open Data Portal terms of use, 2018; credit: City of Santa Clara), City of Vallejo specific plan areas (no license stated), County of Sonoma parcels (CC BY-SA 3.0 US, credit: County of Sonoma), County of San Mateo parcels (data.smcgov.org nr6j-72z7, Public Domain; credit: County of San Mateo), Marin County parcels (Marin GIS Basemap FeatureServer layer 13; no license stated), City of East Palo Alto Specific Plan Boundary and Final_Zoning layers (no license stated), public layers under each agency's terms or disclaimer | Credited in the map's credits. Accuracy (official or approximate) is stated in each file and in the project panel. |
| UCSF Parnassus Heights, Tanforan, Northgate Town Square, Ravenswood Business District | Site boundaries | DataSF Parcels (acdm-wktn, block 2634A lots 003, 005, 011, 012); County of San Mateo parcels (six APNs, WKT geometry in State Plane CA III); Marin County parcels (six APNs); City of East Palo Alto Specific Plan Boundary less University Village's zoning parcels (Final_Zoning, R-LD and PI zones and two PR parcels) | DataSF: ODC PDDL 1.0. San Mateo County: Public Domain. **Open items for Matthew:** the Marin County parcel service (gis.marinpublic.com) and both City of East Palo Alto ArcGIS layers state no license or terms; confirm the terms with the County and the City before relying on them, as for Sunnyvale and Vallejo. |
| Oceanwide Center, 30 Van Ness | Site boundaries | DataSF Parcels (acdm-wktn): block 3708 lots 003, 006, 007, 009, 010, 011, 012, 055 and the vacated street lots 176 and 177; block 0835 lot 004 | ODC PDDL 1.0. |
| West Midway and RESHAP, Encinal Terminals | Site boundaries | Alameda County Assessor parcels (services5.arcgis.com/ROBnTHSNjoZ2Wm1P, Parcels layer 0): the 23 Tract 8696 lots between Pan Am Way, West Midway Avenue, Main Street and West Tower Avenue (books 74-1385 to 74-1388), closed over the internal streets; APNs 72-382-1, 72-382-2 and 72-382-9 | Alameda County open data (county disclaimer). |
| Alameda Marina, Alameda Point (rest of the base) | Site boundaries and land-use zones | City of Alameda zoning, ArcGIS Online "Zoning v03" (services9.arcgis.com/ucDLsG1EwPnOGY4c, Zoning_v03/FeatureServer/0), used as published: the M-X polygon between Grand and Willow streets; the AP- districts less Site A, West Midway/RESHAP and the AP-NR/G Nature Reserve | **Open item for Matthew:** the City's ArcGIS layer states no license or terms; confirm with the City of Alameda, as for Sunnyvale and Vallejo. |
| Mission Bay Ferry Landing, Redwood City ferry terminal | Site boundaries | DataSF Parcels (acdm-wktn): block 9900 lots 064 and 064H, named in the Final MND (Case 2017-008824ENV); County of San Mateo parcels (data.smcgov.org nr6j-72z7): APN 054-300-380, named in the Port of Redwood City's Draft EIR (SCH 2024041306) | DataSF: ODC PDDL 1.0. San Mateo County: Public Domain; credit: County of San Mateo. |
| Berkeley Pier and ferry terminal | Site boundary | City of Berkeley, Berkeley Water Transportation Pier Ferry Project Draft EIR (Feb 2026, CEQAnet SCH 2025040995), Figure 2-2, Project Site Location (PDF p. 54): main frame placed by its scale bar and the University Avenue roundabout, inset fitted by trimmed ICP (RMS 4.5 m) | Public record; traced (the PDF is not redistributed). Georeference: OpenStreetMap contributors (ODbL 1.0) via Overture. |
| Willow Village | Site boundary (59.17 acres) | Menlo Park Ordinance 1095 (development agreement), Exhibit A-2-1 legal description, placed on City of Menlo Park parcels (CC0) | Public record; traced. |
| Concord Naval Weapons Station | EDC property boundary | Navy–City of Concord term sheet, Exhibit A map (2026-03-30), vector fills georeferenced to OpenStreetMap roads (RMS 4.7 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). |
| Alameda Point (Site A) | Site boundary | 2022 Site A Development Plan, Parcel Diagram p. 12, georeferenced on 8 street intersections (RMS 2.5 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). |
| Suisun expansion | Annexation area (approximate) | Notice of Preparation Figure 2 (SCH 2025110452), georeferenced on SR-12 and SR-113 (RMS 32 m) | Public record; approximate. Georeference: OpenStreetMap contributors (ODbL). |
| Potrero Power Station | Site boundary and five sub-areas | Draft EIR (above), Figure 2-2, p. 2-6: vector shapes, georeferenced to OpenStreetMap street centrelines (13 intersections, RMS 3.4 m) | Public record of the City and County of San Francisco. The shapes are traced facts; the PDF itself is not redistributed (it is downloaded by checksum into the git-ignored `data/raw/docs/`). |
| Potrero Power Station | Block height limits (20 zones in 13 blocks; Block 9 outlined) | Design for Development, Feb 26, 2020 (Planning Commission Motion 20638), Figure 6.2.3, p. 245 (https://sfplanning.org/sites/default/files/documents/citywide/potreropower_D4D_final.pdf): rendered at 200 dpi, colour regions classified against the legend, georeferenced to OpenStreetMap street centrelines (7 intersections, RMS 2.0 m) | Public record of the City and County of San Francisco; traced facts, PDF not redistributed (downloaded by checksum into `data/raw/docs/`). Drawn to the limit, labelled illustrative. |
| Potrero Power Station | Footprint of the Unit 3 boiler stack | OpenStreetMap way 678950945, via Overture; height 300 ft from the Draft EIR, pp. 2-7 and 4.D-8 | ODbL 1.0, covered by the map's OpenStreetMap credit. |
| Balboa Reservoir | Block height limits (25–78 ft) | Design Standards and Guidelines, 2020, Figure 7.2-1 (https://sfplanning.org/sites/default/files/documents/citywide/balboareservoir_dsg.pdf), registered to the DataSF Special Use District outline (RMS 0.9 m) | Public record; traced. Drawn to the limit, labelled illustrative. |
| Mission Rock | Block height limits; Phase 1 buildings A, B, F, G | DataSF Height and Bulk Districts (h9wh-cg3m, used as published); Draft EIR Table 2-4 for block heights; Phase 1 footprints from OpenStreetMap via Overture, stories from DBI permits | Public Domain U.S. Government; ODbL 1.0 for footprints. Unbuilt blocks labelled illustrative. |
| Pier 70 | Parcel height limits (50–90 ft); Building 12 | Design for Development, 2022, Figure 6.4.2 (https://www.sfport.com/media/8123/download?inline=), georeferenced on street intersections (RMS 0.9 m); Building 12 footprint from OpenStreetMap via Overture | Public record of the Port of San Francisco; traced. ODbL 1.0 for the footprint. Labelled illustrative. |
| Stonestown | Parcel height limits (30–190 ft) | Design Standards and Guidelines, Apr 2024, Figure 5.9 (SF Planning document store), georeferenced on street intersections (RMS 1.0 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| India Basin | Parcel height limits (20–80 ft; towers to 160 ft) | Design Standards and Guidelines, July 2018 (Motion 20252), Figure 5-3 (https://sfplanning.s3.amazonaws.com/default/files/devagreements/indiabasin/IndiaBasin_Design_Standards_and_Guidelines.pdf), georeferenced to 133 OpenStreetMap building footprints (RMS 0.5 m), clipped to the DataSF SUD | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| Candlestick Point | Block and Candlestick Center height limits (40–180 ft); 11 tower zones (170–420 ft); Alice Griffith buildings | Addendum 7 to the CP-HPS2 FEIR (OCII, Aug 2024), Figure 5, georeferenced to DataSF parcel blocks (RMS 0.2 m); Candlestick Point Design for Development, 2024 amendment, Table 4.2; DBI permits for stories | Public record; traced. Footprints: OpenStreetMap contributors (ODbL) via Overture. Labelled illustrative. |
| Hunters Point Shipyard | Phase 2 block heights (40–120 ft); Towers A (370 ft) and B (270 ft) | Phase 2 Design for Development (OCII, Oct 2018), Fig. 4.4c, georeferenced to OpenStreetMap roads (trimmed ICP, RMS 3.6 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| Treasure Island | Block heights (45–125 ft) and flex tower zones (240–450 ft); Isle House and completed buildings | DataSF Height and Bulk Districts (h9wh-cg3m, "-TI" districts, used as published); block names and height check from the Design for Development, 2024 update, Fig. T4.q; footprints from OpenStreetMap via Overture, stories from DBI permits | Public Domain U.S. Government; ODbL 1.0 for footprints. Estimated building heights and envelopes labelled illustrative. |
| Mission Bay | The two remaining plan blocks (4 East, 12 West) | Mission Bay South Design for Development (OCII, Nov 2025), Map 4 and Height Zone Chart; Redevelopment Plan Sec. 304.5 (Ord. 022-26); DataSF parcels; block names from OCII's land use map (Oct 2023, RMS 5.5 m) | Public record and DataSF (PDDL). Labelled illustrative; the split of Block 4 East is approximate. |
| Parkmerced | Block height envelopes (45–145 ft) | DataSF Height and Bulk Districts (h9wh-cg3m, "-PM" districts, used as published), checked against the Design Standards and Guidelines (rev. 2014), Fig. 03.03.C | Public Domain U.S. Government. Labelled illustrative. |
| Parkline | 14 buildings (35–91 ft) | Master Plan Project Plans (City of Menlo Park, June 24, 2025), Sheet G3.03, georeferenced on 7 street intersections (RMS 1.4 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| Willow Village | 20 buildings (15–118 ft) | Master plan set (City of Menlo Park, Oct 2022), Sheet G3.04, fitted to the traced site boundary (RMS 0.5 m); checked against the 2023 architectural control plans | Public record; traced. Labelled illustrative. |
| Related Santa Clara | Parcel and block height limits (60/90 ft; 190 ft) | Master Community Plan Scheme C Supplement (Santa Clara Res. 25-9467, 2025), Exhibit 4C-1, georeferenced on 8 street intersections (RMS 3.0 m); CEQA Addendum 4 (Res. 25-9465) for the 190-ft cap | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| Downtown West | Block height limits (40–290 ft) | October 2020 draft Downtown West Design Standards and Guidelines (Draft EIR Appendix M, CEQAnet SCH 2019080493), Figs. 5.9 and 5.12, georeferenced to 613 OpenStreetMap building footprints (RMS 1.4 m); clipped to City of San José zoning (CC-BY 4.0, credit: City of San José) | Public record; traced. Heights from the draft, flagged for verification against the approved 2021 version. Labelled illustrative. |
| The Rise | Blocks, podiums and towers (27–228 ft) | Approved SB 35 plan set (City of Cupertino, second modification, Feb 16, 2024), sheets P-0800.xx and sections P-0831/P-0832, fitted to Santa Clara County parcels (RMS 0.3 m) | Public record; traced. Labelled illustrative. |
| Oceanwide Center | The two approved towers (850 and 605 ft to the roof) | Community Plan Exemption Checklist, Case 2006.1523E (SF Planning, 2016), Figures 2 and 3 (https://sfmea.sfplanning.org/2006.1523E_Checklist.pdf), registered to DataSF parcel corners (RMS 0.3 m); heights from Planning Commission Motion 19635 (May 5, 2016) | Public record; traced. Labelled illustrative. |
| 30 Van Ness | Podium (130 ft) and tower (520 ft) | Planning Commission packet, Record No. 2017-008051 (May 21, 2020), typical residential floor plan, PDF p. 488 (https://commissions.sfplanning.org/cpcpackets/2017-008051DNXCUAOFASHDENV.pdf): plan dimensions laid out on the DataSF parcel; envelope confirmed by Motion 21700 (2025) | Public record; dimensions transcribed. Labelled illustrative. |
| Alameda Point (Site A) | Block height limits (40–78 ft); Radium Performing Arts Center; Blocks 6–9 as built | Site A Development Plan, Second Amendment (2022), Land Use Diagram p. 11 (RMS 2.6 m); Radium revised plan (2025, approved 2026); built footprints from OpenStreetMap via Overture with heights from approved plans and Planning Board staff reports | Public record; traced. Footprints: OpenStreetMap contributors (ODbL). Envelopes labelled illustrative. |
| West Midway and RESHAP | Block height limits (40 and 50 ft); RESHAP residential buildings (±50 ft) | West Midway Development Plan (2023), sheet 10 "Land Use Diagram & Building Heights" (https://legistar1.granicus.com/alameda/attachments/5be8021b-f3c6-4a76-8312-60267b458f36.pdf), raster blocks classified by legend colour; RESHAP Development Plan (2023), p. 13 land use diagram (https://legistar1.granicus.com/alameda/attachments/d3ee17a1-dd9a-4874-99d4-ae7134ed1c5b.pdf); both fitted to the Tract 8696 Assessor lots by trimmed ICP (RMS 2.2 m and 1.0 m) | Public record; traced. Labelled illustrative. |
| Alameda Marina | The Launch (built, 60 ft); Phase II townhome lots (45 ft); The Foundry's lot (65 ft) | The Launch: OpenStreetMap relation 16011797 via Overture, height from the Planning Board staff report of Oct 14, 2019; Tract 8610 and Tract 8711 lots from Alameda County Assessor parcels; height limits from the 2018 Master Plan and 2023 Phase III staff reports (City of Alameda Legistar) | Public record; ODbL 1.0 for the footprint; Alameda County open data (county disclaimer) for the lots. Unbuilt phases labelled illustrative. |
| Brooklyn Basin | Parcel heights (86 ft; 240-ft tower zones); completed parcels | City of Oakland parcels (Assessor; for reference only); Oakland Planning Code 17.101B.130 (Ord. 13826); Design Guidelines (2014) tower-zone diagram (RMS 3.6 m); revised PDP sheet 1.4 (RMS 1.8 m); built footprints from OpenStreetMap via Overture | Public record; Oakland GIS for reference only; ODbL for footprints. Built heights estimated from stories and labelled illustrative. |
| Moffett Park | Land-use zones (MP- districts) | City of Sunnyvale zoning GIS (ZoningLegend layers 1 and 2, used as published) under Ordinance 3218-23 (2023) | Public layer under the city's terms (no license stated). |
| North Bayshore | Land-use zones | North Bayshore Master Plan (Mountain View, April 2023), Plans 4.1.1 and 4.1.2, georeferenced on street intersections (RMS 2.8 and 4.9 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Approximate. |
| Concord Naval Weapons Station | Land-use districts | Concord Reuse Project Area Plan, Book One (2012), Fig. 3-3, fitted to OpenStreetMap roads (trimmed RMS 4.1 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Approximate. |
| Suisun expansion | Proposed land-use zones | Notice of Preparation (Suisun City, Nov 2025, SCH 2025110452), Figs. 2 and 5, fitted to OpenStreetMap roads (RMS 19 and 32 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Proposed and approximate. |
| Brisbane Baylands | Draft land-use districts; Bayshore Roundhouse | 2026 staff-recommended Baylands Specific Plan, Fig. 2.3.1, fitted to the city's draft boundary (RMS 1.9 m); Roundhouse footprint from OpenStreetMap via Overture, height about 25 ft from the Council staff report (Sept 29, 2026) | Public record; traced. ODbL for the footprint. Draft, not adopted. |
| Schlage Lock | Site boundary; parcel heights (57–86 ft) | DA Exhibit B parcels (DataSF acdm-wktn); Exhibit L Conceptual Parcelization Plan (2014), fitted to the parcels (RMS 0.5 m); DataSF Height and Bulk Districts (h9wh-cg3m) | Public record; PDDL and Public Domain. Labelled illustrative. |
| Sunnydale HOPE SF | Block height zones; built buildings | Design Standards and Guidelines (rev. 2023), Fig. 7.1, fitted to the SUD and DataSF parcels (RMS 1.5 m); DBI permits; OpenStreetMap footprints via Overture | Public record; traced. ODbL for footprints. Labelled illustrative. |
| Potrero HOPE SF | Block height zones; built buildings | Design Standards and Guidelines (2016), Fig. 5.1, fitted to the SUD (RMS 2.7 m); DBI permits; OpenStreetMap footprints via Overture | Public record; traced. ODbL for footprints. Labelled illustrative. |
| Tasman East | Built towers; plan-parcel envelopes (220/85 ft) | City of Santa Clara parcels and zoning; Final and Draft EIR; HCD APR data (data.ca.gov); OpenStreetMap footprints via Overture | City of Santa Clara Open Data Portal terms (2018): ODC PDDL 1.0, credit City of Santa Clara; ODbL for footprints. Envelopes and story-based heights labelled illustrative. |
| Middlefield Park | Building envelopes (60–125 ft) | Middlefield Park Master Plan (Mountain View, Oct 2022), Fig. 8.3.5 and Table 8.3.2, fitted to existing buildings (RMS 0.5 m) | Public record; traced. Labelled illustrative. |
| Berryessa flea market site | Height areas (90–270 ft) | Berryessa BART Urban Village Plan height diagram, as reproduced in the Planning Commission report (May 2021), fitted to OpenStreetMap streets and BART (RMS 1.1 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Labelled illustrative. |
| Mare Island | Land-use zones | Mare Island Specific Plan, Figure 3.1 (rev. 2008), City of Vallejo, fitted to existing buildings (RMS 11 m) | Public record; traced. Approximate. |
| Sonoma Developmental Center | Site boundary; proposed land-use zones | County of Sonoma NOP (Aug 2025, SCH 2025081410), Figs. 3 and 4, fitted to OpenStreetMap buildings (RMS 0.8 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). Proposed. |
| Esmeralda | Draft land-use zones | Draft Esmeralda Specific Plan (City of Cloverdale, rev. Sept 2026), Fig. 2-1, fitted to County of Sonoma parcels (CC BY-SA 3.0 US) (RMS 1.9 m) | Public record; traced. Draft, not adopted. |
| The Portal | Tunnel alignment, train box, two stations; trackwork to 16th Street (`data/lines/the-portal.geojson`) | TJPA, The Portal Monthly Status Report, Sept 2026, Figure 1 (https://www.tjpa.org/media/40591?inline=), raster map georeferenced on 35 DataSF street intersections (Streets – Active and Retired, 3psu-pn9h; RMS 1.2 m); trackwork on the U.S. DOT/BTS NTAD rail network (Caltrain main line) to DataSF's 16th Street | Public record; traced, PDF not redistributed (downloaded by checksum into `data/raw/docs/`). DataSF: ODC PDDL 1.0. NTAD: public domain (work of the U.S. government). Approximate alignment. The California High-Speed Rail Authority's ArcGIS layers forbid redistribution; they were used only to check the trace locally. |
| California High-Speed Rail, SF–San José | Shared Caltrain corridor, Fourth and King to San José Diridon; three stations (`data/lines/cahsr-sf-sj.geojson`) | U.S. DOT Bureau of Transportation Statistics, NTAD North American Rail Network Lines (https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_North_American_Rail_Network_Lines/FeatureServer/0), Caltrain-owned arcs routed between the stations; split at the Record of Decision's Scott Boulevard point; station points from Caltrain's GTFS (https://www.caltrain.com/developer-resources) | NTAD: public domain ("a work of the United States government ... available for unrestricted public use"). Caltrain GTFS: Peninsula Corridor JPB developer licence (non-exclusive, revocable right to use, reproduce and redistribute; no Caltrain trademarks or system map used). Approximate alignment. The Authority's own GIS was compared locally only (redistribution not permitted). |
| BART Silicon Valley Phase II | Alignment (tunnel and above-ground track, drawn as the centreline of VTA's two tracks), four new stations and Berryessa (`data/lines/bart-silicon-valley-phase-2.geojson`) | VTA public hosted feature services on gis.vta.org: BSVII_Alignment_2022 (layer 22), BSV Phase II Stations (layer 0), BSV Phase I Stations (BSV_Phase_II_Construction layer 11) | Santa Clara Valley Transportation Authority public GIS; **no license or terms of use stated** on the services or their portal items. Open item for Matthew: confirm VTA's terms before relying on it, as for Sunnyvale and Vallejo. Credit: VTA. |
| Diridon Station | Station project footprint, station area only (about 12 acres as traced) | Diridon Station Steering Committee packet, Aug 19, 2026 (VTA iQM2), p. 92 "Future Station Project Footprint": vector outline over the slide's aerial photo, placed from two street crossings and fitted to OpenStreetMap building outlines (trimmed ICP, RMS 1.2 m) | Public record; traced. Georeference: OpenStreetMap contributors (ODbL). The slide's aerial photo (credited there to County of Santa Clara, Microsoft, Vantor) is used only to georeference and is not redistributed. Cut at the slide's edges. |
| Valley Link (Phase 1A) | Alignment (Dublin/Pleasanton to the tail tracks east of Vasco Road) and three stations (`data/lines/valley-link.geojson`) | Tri-Valley–San Joaquin Valley Regional Rail Authority: Board packet, June 10, 2026, AB 1171 Initial Project Report, Figure 4 (First Street to Vasco Road; https://www.valleylinkrail.com/_files/ugd/8f09e7_9cca9a978bb14766a336566c3710ef3a.pdf), and the 2024 Draft SEIR, Chapter 2, Figures 2-4 to 2-6 (I-580 median), 2-13 and 2-14 (stations) (CEQAnet SCH 2018092027, document 6). Street-map figures fitted to OpenStreetMap streets (trimmed ICP, RMS 1.6–2.8 m); aerial-photo figures fitted to OpenStreetMap building footprints (tile correlation, RMS 1.3–3.0 m). Station checks: BART GTFS (stop L30-1) and Caltrans California Transit Stops (stop VAS) | Public records; traced, PDFs not redistributed (downloaded by checksum into `data/raw/docs/`). Georeference: OpenStreetMap contributors (ODbL) via Overture. BART GTFS: BART developer license; Caltrans California Transit Stops: public layer, no license stated (used only as a distance check, not drawn). Approximate alignment. |
| SMART Healdsburg extension | Alignment, Windsor to Lytton Springs Road (8.86 mi as drawn), and two stations (`data/lines/smart-healdsburg.geojson`) | U.S. DOT/BTS NTAD North American Rail Network Lines, SMART-owned arcs (RROWNER 'SMRT'/'SMAR'), cut where the County of Sonoma's street centrelines (BASEPublic/Streets_Public) cross; Windsor station from the BTS National Transit Map stops (SMART feed, stop 4251896); Healdsburg station from SMART's station layer on the County of Sonoma server (SMARTPublic/SMART_Stations); checked against SMART's track layer (median 4 m apart) and the NTAD Railroad Grade Crossings layer | NTAD: public domain. Streets: CC BY-SA 3.0 US, credit "County of Sonoma". National Transit Map: CC BY 3.0 US. SMART station layer: no license stated. Approximate centreline. |
| SMART Cloverdale extension | Alignment, Lytton Springs Road to E 1st Street in Cloverdale (13.45 mi as drawn), and two stations (`data/lines/smart-cloverdale.geojson`) | As above (NTAD SMART arcs, County of Sonoma streets); Geyserville station from the County of Sonoma parcel APN 140-110-011 (CRAPublic/ParcelsPublicShapeFile); Cloverdale station from SMART's station layer (site to be determined) | NTAD: public domain. Streets and parcels: CC BY-SA 3.0 US, credit "County of Sonoma". SMART station layer: no license stated. Approximate centreline. |
| BART station-area housing | Six station-site boundaries | BART TOD Work Plan layer (BART_AB_2923_Public_Service_20230201, layer 2, BART's ArcGIS Online), parcels selected by BART status or by APNs named in City of Oakland and City of Dublin records | BART public layer (no license stated); official parcel data, credited in the boundary file. |
| BART station-area housing | West Oakland, Lake Merritt and El Cerrito Plaza buildings; North Berkeley, Ashby and Amador Station envelopes (80/61 ft) | West Oakland revised PDP (City of Oakland, 2020), floor plans fitted to the parcel corners (RMS 0.2 m); Lake Merritt tract map sheets C4.1–C4.2 (City of Oakland DRC report, 2021; RMS ≤0.2 m); El Cerrito Plaza master plan sheet A1.01 (City of El Cerrito, 2024; RMS 0.8 m); R-BMU height limit (Berkeley ODS, 2023); Amador Station's approved 61 ft (City of Dublin development map, PLPA-2021-00019); existing buildings cut out from OpenStreetMap via Overture | Public record; traced. Envelopes labelled illustrative. ODbL for the cut-out footprints. |

The Draft EIR's 2018 height districts (Figure 2-7) are no longer traced: the approved
Design for Development superseded them in 2020.

Every boundary file names its source document, page, accuracy and georeferencing
residuals; every massing feature names its source. The in-map credit line notes that
project geometry is traced from public planning documents, and each project panel links
the document.

## Fonts

From google/fonts at commit `9710da1eacb3be272583c3224dcb70f9da6eadbb`:

- **Libre Franklin**, SIL Open Font License 1.1 (Impallari Type). Used for the interface and map labels.
- **Source Serif 4**, SIL Open Font License 1.1 (Adobe). Used for summaries and notes.

The license texts ship with the fonts in `public/generated/fonts/`.

## Software

| Package | License |
|---|---|
| MapLibre GL JS | BSD-3-Clause |
| PMTiles (protomaps) | BSD-3-Clause |
| Preact | MIT |
| Tippecanoe (Felt) | BSD-2-Clause |
| fontnik (Mapbox) | BSD-2-Clause |
| GeoPandas, Shapely, pyarrow, fontTools | BSD-3-Clause / Apache-2.0 / MIT |
| Vite, Vitest, Playwright | MIT / MIT / Apache-2.0 |

## Project photos (`data/photos.json`, `public/photos/`)

One openly licensed or public-domain photo per project, approved by Matthew on 2026-10-06 and
2026-10-12, all from Wikimedia Commons. `make photos` reads each file's author and license from its
own Commons page, refuses any license outside CC0, public domain, CC BY and CC BY-SA, and copies a 1200 px
version into `public/photos/` (no hotlinking; metadata stripped). The panel shows each photo with
its credit: author, date taken, license with a link, and "via Wikimedia Commons" with a link to
the file page. CC BY and CC BY-SA photos are marked "Resized and re-encoded". The resized copies of
CC BY-SA photos are shared under the same license as the original.

| Project | Author | License | Taken | Source |
|---|---|---|---|---|
| treasure-island | 9yz | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | 2025-05-27 | [Commons](https://commons.wikimedia.org/wiki/File:Treasure_Island_-_whole_island_panorama_2025.jpg) |
| stonestown | Mx. Granger | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) | 2025-12-20 | [Commons](https://commons.wikimedia.org/wiki/File:Stonestown_Galleria_1.jpg) |
| parkmerced | Bill Abbott | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 2018-10-10 | [Commons](https://commons.wikimedia.org/wiki/File:San_Fancisco,_Lake_Merced,_Parkmerced,_I_lived_in_the_bungalos_0_to_1_year..._DSC_0680_(48646781841).jpg) |
| brisbane-baylands | Moonstone2 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2020-10-31 | [Commons](https://commons.wikimedia.org/wiki/File:Ruins_of_the_Railroad_Roundhouse_in_Brisbane_40.jpg) |
| alameda-point | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2022-12-15 | [Commons](https://commons.wikimedia.org/wiki/File:Aerial_view_of_Alameda_Seaplane_Lagoon,_December_2022.JPG) |
| mare-island | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2022-03-20 | [Commons](https://commons.wikimedia.org/wiki/File:Aerial_view_of_Mare_Island_and_Vallejo,_March_2022.JPG) |
| oakland-coliseum | Quintin Soloviev | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | 2024-03-28 | [Commons](https://commons.wikimedia.org/wiki/File:Oakland_Coliseum_aerial_view_2024.jpg) |
| candlestick-point | Pi.1415926535 | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2018-08-27 | [Commons](https://commons.wikimedia.org/wiki/File:Candlestick_Hill_aerial_view,_August_2018.JPG) |
| hunters-point-shipyard | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2024-04-06 | [Commons](https://commons.wikimedia.org/wiki/File:Aerial_view_of_Hunters_Point_Naval_Shipyard,_April_2024.JPG) |
| potrero-power-station | Pi.1415926535 | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2020-02-17 | [Commons](https://commons.wikimedia.org/wiki/File:Old_siding_and_Unit_3_at_Potrero_Generating_Station,_February_2020.JPG) |
| pier-70 | Clyde Charles Brown | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2025-02-20 | [Commons](https://commons.wikimedia.org/wiki/File:Old_shipyard_building_at_Pier_70,_San_Francisco,_California,_US.jpg) |
| mission-rock | Lexi Mattick | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | 2026-07-31 | [Commons](https://commons.wikimedia.org/wiki/File:Mission_Rock_Aerial_-_July_2026.jpg) |
| mission-bay | Firstcultural | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) | 2024-02-10 | [Commons](https://commons.wikimedia.org/wiki/File:Aerial_photo_of_Mission_Bay_and_northern_end_of_I-280.jpg) |
| india-basin | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2021-04-17 | [Commons](https://commons.wikimedia.org/wiki/File:India_Basin_Shoreline_Park,_April_2021.jpg) |
| schlage-lock | Pedro Xing | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) | 2012-11-10 | [Commons](https://commons.wikimedia.org/wiki/File:Bayshore_Station_3238_26.JPG) |
| willow-village | EspartacoPalma | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2015-04-03 | [Commons](https://commons.wikimedia.org/wiki/File:Menlo_Science_%26_Technology_Park_entrance.jpg) |
| downtown-west | 94rain | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2023-06-17 | [Commons](https://commons.wikimedia.org/wiki/File:Montgomery_Street,_Near_the_San_Jose_Diridon_Station,_Jun_17,_2023_-_52.jpg) |
| moffett-park | Grendelkhan | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2018-06-27 | [Commons](https://commons.wikimedia.org/wiki/File:Google_Moffett_Place_offices_from_the_air.jpg) |
| berryessa-flea-market | Dicklyon | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2020-06-13 | [Commons](https://commons.wikimedia.org/wiki/File:Berryessa_Flea_Market_from_new_BART_station.jpg) |
| concord-naval-weapons-station | Wing | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2015-02-01 | [Commons](https://commons.wikimedia.org/wiki/File:Concord_Naval_Weapons_Station_20150201.jpg) |
| suisun-expansion | Missvain | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | 2023-09-07 | [Commons](https://commons.wikimedia.org/wiki/File:Wind_turbines_-_September_2023_-_Sarah_Stierch.jpg) |
| sonoma-developmental-center | Missvain | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) | 2022-12-16 | [Commons](https://commons.wikimedia.org/wiki/File:Sonoma_Developmental_Center_-_Demember_2022_-_Sarah_Stierch_01.jpg) |
| the-portal | RChin | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 2015-01-26 | [Commons](https://commons.wikimedia.org/wiki/File:Transbay_Transit_Center_construction_from_above,_June_2015.jpg) |
| cahsr-sf-sj | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2024-04-23 | [Commons](https://commons.wikimedia.org/wiki/File:Caltrain_KISS_set_at_4th_and_King,_April_2024.jpg) |
| bart-silicon-valley-phase-2 | Pi.1415926535 | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2017-10-29 | [Commons](https://commons.wikimedia.org/wiki/File:Proposed_BART_yard_site_in_San_Jose,_October_2017.jpg) |
| diridon-station | Pi.1415926535 | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2019-11-29 | [Commons](https://commons.wikimedia.org/wiki/File:San_Jose_Diridon_station,_November_2019.JPG) |
| valley-link | Pi.1415926535 | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2018-05-10 | [Commons](https://commons.wikimedia.org/wiki/File:Dublin_Pleasanton_station_from_garage,_May_2018.JPG) |
| smart-healdsburg | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2022-07-21 | [Commons](https://commons.wikimedia.org/wiki/File:NWP_bridge_in_Healdsburg,_July_2022.JPG) |
| smart-cloverdale | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2022-07-21 | [Commons](https://commons.wikimedia.org/wiki/File:Cloverdale_station_from_the_northeast,_July_2022.JPG) |
| mission-bay-ferry-landing | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2020-10-04 | [Commons](https://commons.wikimedia.org/wiki/File:Remains_of_SP_freight_pier_off_16th_Street,_October_2020.JPG) |
| berkeley-pier-ferry | Amatulic | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 2014-03-08 | [Commons](https://commons.wikimedia.org/wiki/File:Berkeley_pier_old_part_3308.jpg) |
| redwood-city-ferry-terminal | U.S. Army Corps of Engineers, photographer not specified or unknown | Public domain | Undated | [Commons](https://commons.wikimedia.org/wiki/File:Redwood_City_port_aerial_view.jpg) |
| ucsf-parnassus | Alfred Twu | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) | 2021-09-21 | [Commons](https://commons.wikimedia.org/wiki/File:University_of_California_San_Francisco_-_Parnassus_campus.jpg) |
| northgate-san-rafael | Mx. Granger | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) | 2014-07-20 | [Commons](https://commons.wikimedia.org/wiki/File:The_Mall_at_Northgate.jpg) |
| bart-station-housing | Pi.1415926535 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 2025-09-27 | [Commons](https://commons.wikimedia.org/wiki/File:TOD_construction_at_Lake_Merritt_station,_September_2025.jpg) |
| alameda-point-plan | Bill Abbott | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 2018-10-10 | [Commons](https://commons.wikimedia.org/wiki/File:Aerial_view_of_Old_Alameda_Point,_October_2018.jpg) |

Approved but not yet downloaded (Wikimedia rate-limited; `make photos` fetches it):
the-rise.

## Renderings

None yet. Only images with explicit permission (press kits) or Matthew's own work
will be used; the outreach list is `docs/images/PERMISSIONS.md`. Each one will be listed in `public/renders/{id}/renders.json` with its credit
and permission note.
