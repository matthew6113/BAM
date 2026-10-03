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

**Context lines:** freeways, rail and ferries are off by default, as the spec says they are optional. (Superseded 2026-10-02: on by default.)

**Style panel:** on in development, or with `?style=1` in any build. The shortcut is Alt+Shift+S, not a bare "S", per WCAG 2.1.4.

**3D toggle:** 3D tilts the map and shows faint context massing (theme `contextExtrusion`) for buildings with real heights at zoom 14 and above. 2D is flat with tilt and rotate disabled.

**"Partly built" placeholder:** `#5A6B8C`. The spec has no color for this stage.

## 2026-10-02: context lines and hosting (Matthew)

**Context lines are on by default.** Matthew asked to keep the railroads and freeways. The layer now draws:
- Freeways (OSM motorways) and highways (trunk roads). On- and off-ramps appear from zoom 12.
- Railroads: transit (BART, Muni, VTA, cable cars, SFO AirTrain) and every active standard-gauge line (Caltrain, SMART, Union Pacific and BNSF track). Named lines and stretches over 1 km show from the regional view; unnamed yards and spurs only up close.
- Ferry routes.
- Left out: narrow-gauge, funicular and "unknown" track.

**Hosting:** GitHub Pages, with the repository made public.
- **Deploys:** every push to main via `.github/workflows/deploy.yml`.
- **Address:** the site is served from `/BAM/`.
- **Tile files:** street-level building tiles are split into one archive per zoom (13, 14, 15) so no file exceeds 100 MB.
- **Archive:** the Overture extract is kept as a GitHub release asset, so builds keep working after Overture removes the release.
- **Tiles on object storage:** still possible later through `VITE_TILE_BASE_URL`.

## 2026-10-02: Milestone 2, Potrero Power Station (open for Matthew's review)

**Source for the blocks: the approved Design for Development (2026-10-03).** Matthew asked for the D4D's height plan to be traced (2026-10-03). This replaces the 2018 Draft EIR blocks, which were dropped on 2026-10-02 as superseded.
- The site boundary and five sub-areas are still traced from DEIR Figure 2-2 (vector shapes, 13 street intersections, RMS 3.4 m), 29.1 acres.
- Blocks come from D4D Figure 6.2.3, Building Height Plan (p. 245). The legend's 85 and 125 ft fills are spot colours that PDF parsers can't read, so the page is rendered at 200 dpi and each block's pixels are classified against the legend; labels and dimension lines printed on the fills take the colour of the nearest fill.
- Georeferenced on seven street intersections measured from the figure's curb lines, including Phase 1 streets now in OpenStreetMap (Maryland, Humboldt): RMS 2.0 m. Registering the figure's dash-dot site line to the 2018 boundary failed (the two boundaries differ), so it isn't used.
- Each block is a solid to its height limit, labelled "Illustrative massing": the limits are an envelope, not building designs. "180'/85'" tower zones (Blocks 1, 5, 7) are an 85-ft solid with a faint envelope to 180, 220 or 240 ft. "MAX" dimensions in the figure are plan lengths and aren't used.
- Block 9 is a dashed outline: the D4D gives two configurations, with or without Unit 3.
- Every block is "entitled". The Sophie Maxwell Building (DBI permit complete Aug 28, 2026) is cut out of Block 7 and left to the base map; UCSF's Block 2 building has no official construction record yet.
- The 2026 amendments (Addendum 2: +8 ft on residential blocks and more on Blocks 1, 5, 11, 12, 15) aren't drawn until the Board adopts them.
- The stack is 300 ft (DEIR pp. 2-7, 4.D-8) on its OpenStreetMap footprint.

**Fly-in:** 4.5 s flight (`flyTo`, ease in and out), the boundary drawing itself from 35% to 90% of it; then the surroundings within 700 m extrude faintly (0.8 s fade) and the blocks rise over 1.2 s, staggered outward over 0.6 s. Escape, close or back flies back over 3 s to where the viewer was, in the mode (2D or 3D) they were in. Reduced motion: a 160 ms dip to paper, a jump, and no rise.

**Landing camera:** from the south-southwest (bearing -30), pitch 58, zoom 16.4 for a 1440 x 900 window with the panel; smaller views zoom out to keep the site in frame. Option shown: from the southeast.

**Massing opacity by stage (theme `massing.opacity`):** entitled 0.5 (the spec's "light fill"), under construction 0.92, complete 0.95 in ink. Option shown: entitled at 0.78.

**Panel:** 400 px on the right; a bottom sheet over the lower half below 720 px. The caveats (illustrative massing, approximate boundary, with the source link) sit right under the stage bar. Numbers are shown only as stored, so the affordable share stays a percentage. Renderings: none with permission yet, so the official pages are linked.

**Projects list:** a small "Projects" disclosure under the title is the keyboard route in until the Milestone 3 index.

**Deep links:** `/p/{id}`. The build writes `p/{id}/index.html` (with the project's title and summary) and `404.html`, since Pages has no rewrites.

## 2026-10-02: official sources only (Matthew)

Matthew: "I want only official." What it means here:
- **Sources:** every fact shown traces to a public agency or body: adopted plans, hearing minutes, permits, official GIS, the published code. A test enforces this for mapped projects (`src/projects/official.ts`).
- **Press-only facts** move to the project's `reported` record, which the map never shows. For Potrero that is the 2025–26 construction and opening dates, the 2026 amendment request, the "Fifth Space" name and the 30% affordable share. The panel says that reported details are held back.
- **Potrero's stage** is "entitled" until official records (permits, UCSF, the Mayor's Office of Housing) confirm construction and the completed building. Press reports put it at "partly built".
- **Potrero's blocks:** the 2018 Draft EIR blocks are superseded and are not drawn. The map shows the traced site boundary and the 300-ft stack only. The approved block heights come from the Design for Development once it can be read. The Planning Commission minutes of Jan 30, 2020 confirm the approved range for new buildings: 65 to 240 ft.
- **Unmapped projects:** they don't open from a deep link. Their records haven't been checked against official sources yet.
- **Network:** Matthew is broadening the environment's network access so the official sites (sfplanning.org, data.sfgov.org, the code, CEQAnet, UC Regents) can be read.

