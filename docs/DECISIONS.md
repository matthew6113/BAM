# Decisions

Choices that shape the map, in the order they were made. The evidence is in
`docs/PLANNING-AUDIT.md`. Newest last.

## 2026-10-01: build plan (approved by Matthew: "continue with all per recommendations")

**Stack**
- Vite + TypeScript + Preact for the UI.
- MapLibre GL JS 6 + PMTiles for the map.
- A Python (uv) and Tippecanoe 2.79 pipeline for the data.
- Playwright for screenshots.
- No deck.gl, because its interleaved mode crashes on MapLibre 6.

**Base data:** the Overture Maps release is pinned to `2026-09-23.1`.
- Buildings, water, counties, city points and context lines all come from Overture.
- The pipeline reads Overture with pyarrow. DuckDB is not used because its extensions are blocked in the build sandbox, and third-party copies are not trusted.

**Building heights:** only mapped (OpenStreetMap, Esri) or measured (USGS lidar) heights are kept. Microsoft's ML estimates are dropped, so 1,021,947 buildings stay flat, along with the ones that never had a height. 1,003,219 of 2,547,306 buildings have a height.

**Data corrections:** the three approved corrections are applied and logged in CHANGELOG.md:
- Potrero's stack is concrete, not brick.
- Potrero's acreage note now cites the Draft EIR.
- Mission Bay's unsourced figures are held out of the map.

**Parcels:** used only as tracing references, never shown, with each county's license checked before use.

**Network:** sfplanning.org and data.sfgov.org are needed before Milestone 2. They are blocked in the build environment.

## 2026-10-01: Milestone 1 defaults (open for Matthew's review)

**Default view:** frames every project's approximate center, not the full nine counties. Panning is limited to the nine counties plus a margin.

**Buildings below zoom 13:**
- "Every building" tiles (80 MB archive): no tile size limit, with Tippecanoe's tiny-polygon reduction keeping density.
- "Lighter" tiles (20 MB) drop too many buildings in the cores. They stay available as an option only.

**Building opacity:**
- The regional ramp starts at 60% at zoom 8 and reaches the spec's 85% at zoom 13.
- Flat 85% is the alternative.
- Both are in the theme (`opacity.buildingsRegional`, `opacity.buildings`).

**Land outside the nine counties:** a faint tint (`outsideRegion`) explains why the buildings stop at the county line.

**Salt ponds:** drawn as water. The toggle changes little, because most South Bay ponds are already mapped as water and the large white areas are tidal marsh.

**Context lines:** freeways, rail and ferries are off by default, as the spec says they are optional.

**Style panel:** on in development, or with `?style=1` in any build. The shortcut is Alt+Shift+S, not a bare "S", per WCAG 2.1.4.

**3D toggle:** 3D tilts the map and shows faint context massing (theme `contextExtrusion`) for buildings with real heights at zoom 14 and above. 2D is flat with tilt and rotate disabled.

**"Partly built" placeholder:** `#5A6B8C`. The spec has no color for this stage.
