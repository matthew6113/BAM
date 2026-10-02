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

**Source for the blocks: the 2018 Draft EIR, labelled illustrative.** The approved plan's Design for Development and Planning Code Figure 249.87-4 could not be reached from the build environment (sfplanning.org and data.sfgov.org are blocked here; only known PDF links on sfplanning.s3.amazonaws.com work). So:
- The site boundary and five sub-areas are traced from DEIR Figure 2-2 (vector shapes, 13 street intersections, RMS 3.4 m). The site is 29.1 acres traced against the DEIR's "approximately 29.0 acres".
- The blocks are the height districts in DEIR Figure 2-7 (the 2018 proposal), labelled "Illustrative massing" in the data and the panel. Search summaries say the approved plan runs 65 to 240 ft; that is not used until read in a primary source.
- Each block is a solid to its podium height with the upper height limit as a faint envelope, because the figure doesn't place towers.
- Block 9 (Unit 3) is a dashed outline with no height: the DEIR gives two configurations.
- Block 2 is "under construction" (from the stage note); the rest are "entitled". The Sophie Maxwell Building is complete but drawn flat: its height in feet isn't sourced yet.
- The stack is 300 ft (DEIR pp. 2-7, 4.D-8) on its OpenStreetMap footprint.

**Fly-in:** 4.5 s flight (`flyTo`, ease in and out), the boundary drawing itself from 35% to 90% of it; then the surroundings within 700 m extrude faintly (0.8 s fade) and the blocks rise over 1.2 s, staggered outward over 0.6 s. Escape, close or back flies back over 3 s to where the viewer was, in the mode (2D or 3D) they were in. Reduced motion: a 160 ms dip to paper, a jump, and no rise.

**Landing camera:** from the south-southwest (bearing -30), pitch 58, zoom 16.4 for a 1440 x 900 window with the panel; smaller views zoom out to keep the site in frame. Option shown: from the southeast.

**Massing opacity by stage (theme `massing.opacity`):** entitled 0.5 (the spec's "light fill"), under construction 0.92, complete 0.95 in ink. Option shown: entitled at 0.78.

**Panel:** 400 px on the right; a bottom sheet over the lower half below 720 px. The caveats (illustrative massing, approximate boundary, with the source link) sit right under the stage bar. Numbers are shown only as stored, so the affordable share stays a percentage. Renderings: none with permission yet, so the official pages are linked.

**Projects list:** a small "Projects" disclosure under the title is the keyboard route in until the Milestone 3 index.

**Deep links:** `/p/{id}`. The build writes `p/{id}/index.html` (with the project's title and summary) and `404.html`, since Pages has no rewrites.

