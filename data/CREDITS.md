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
| 20 projects (see `pipeline/bam_pipeline/sites/official_boundaries.py`) | Site boundaries | Official GIS layers, each named in its boundary file: DataSF Zoning Map – Special Use Districts (5yf5-ms5f) and Height and Bulk Districts (h9wh-cg3m), Public Domain U.S. Government; DataSF Former Redevelopment Agency Project Areas (m288-24sn) and Parcels (acdm-wktn), ODC PDDL 1.0; City of Menlo Park parcels, CC0; City of San José zoning, CC-BY 4.0 (credit: City of San José); City of Mountain View parcels, Sunnyvale General Plan, Brisbane plan boundary, Oakland zoning, Santa Clara County and Alameda County parcels, public layers under each agency's terms or disclaimer | Credited in the map's credits. Accuracy (official or approximate) is stated in each file and in the project panel. |
| Potrero Power Station | Site boundary and five sub-areas | Draft EIR (above), Figure 2-2, p. 2-6: vector shapes, georeferenced to OpenStreetMap street centrelines (13 intersections, RMS 3.4 m) | Public record of the City and County of San Francisco. The shapes are traced facts; the PDF itself is not redistributed (it is downloaded by checksum into the git-ignored `data/raw/docs/`). |
| Potrero Power Station | Block height limits (20 zones in 13 blocks; Block 9 outlined) | Design for Development, Feb 26, 2020 (Planning Commission Motion 20638), Figure 6.2.3, p. 245 (https://sfplanning.org/sites/default/files/documents/citywide/potreropower_D4D_final.pdf): rendered at 200 dpi, colour regions classified against the legend, georeferenced to OpenStreetMap street centrelines (7 intersections, RMS 2.0 m) | Public record of the City and County of San Francisco; traced facts, PDF not redistributed (downloaded by checksum into `data/raw/docs/`). Drawn to the limit, labelled illustrative. |
| Potrero Power Station | Footprint of the Unit 3 boiler stack | OpenStreetMap way 678950945, via Overture; height 300 ft from the Draft EIR, pp. 2-7 and 4.D-8 | ODbL 1.0, covered by the map's OpenStreetMap credit. |

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

## Renderings

None yet. Only images with explicit permission (press kits) or Matthew's own work
will be used. Each one will be listed in `public/renders/{id}/renders.json` with its credit
and permission note.
