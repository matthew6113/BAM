# Bay Area megaprojects

An interactive 3D map of the Bay Area's largest development projects. The existing city
is drawn as quiet ink footprints, in the style of the NYT's "A Map of Every Building in
America". Only the projects get color and height. Click a project and the camera flies
in, the site boundary draws, and the proposed buildings rise.

Status: **Milestone 1** (base map, no projects yet). See `docs/SPEC.md` for the full spec
and milestones, `docs/DECISIONS.md` for choices made so far, and `CHANGELOG.md` for data
changes.

## Quick start

Requirements: Node 22+, [uv](https://docs.astral.sh/uv/), and Tippecanoe 2.79.0
(`brew install tippecanoe` on macOS; on Linux build the `2.79.0` tag from
https://github.com/felt/tippecanoe).

```sh
npm install
make data        # fetch Overture, process, tile, fonts, glyphs (about 5 minutes, ~1 GB download)
npm run dev      # http://127.0.0.1:5173
```

| Command | What it does |
|---|---|
| `make data` | Whole data pipeline. Raw downloads are cached in `data/raw/` (git-ignored). |
| `make fetch` / `process` / `buildings` / `tiles` / `fonts` / `glyphs` / `manifest` | One pipeline step at a time |
| `npm run dev` | Dev server, with the style panel available |
| `npm run build` | Type-check and production build into `dist/` |
| `npm test` | Schema check of `data/projects.json`, theme and contrast tests |
| `npm run e2e` | Playwright keyboard and control tests |
| `npm run screenshots` | Playwright screenshots of key views into `docs/screenshots/m1/` |

## The data pipeline

`pipeline/` is a small Python package, run with `uv` (`pipeline/uv.lock` pins every
dependency).

1. **fetch:** reads Overture GeoParquet for release `2026-09-23.1` straight from S3 (anonymous), only the needed columns, bbox-filtered. Output goes to `data/raw/overture/2026-09-23.1/`.
2. **process:** builds the nine-county region and the mask outside it, water with a minimum zoom per feature, a shoreline dissolved from the water edge, context lines, and the curated labels (`pipeline/bam_pipeline/labels.py`). It also writes `src/generated/region.json` (extent and pan limits).
3. **buildings:** keeps the 2,547,306 footprints whose bbox center is in a county polygon. Heights are kept only when mapped or measured; Microsoft ML estimates are dropped.
4. **tiles:** Tippecanoe builds three PMTiles archives in `public/generated/tiles/`:
   - `base`: about 6 MB
   - `buildings-overview-all`: zoom 6 to 12, about 80 MB
   - `buildings-z13`, `-z14`, `-z15`: street-level footprints with heights, one archive per zoom (47, 56 and 66 MB) so every file stays under GitHub's 100 MB limit
5. **fonts / glyphs:** Libre Franklin and Source Serif 4 (OFL) as WOFF2 for the interface and SDF glyph PBFs for map labels.
6. **manifest:** writes `data/manifest.json` with the row counts, sizes and SHA-256 of every input and output. Compare it after a rebuild.

**Reproducing the data:** Overture keeps each release for only about 60 days. Archive
`data/raw/overture/2026-09-23.1/` (about 620 MB) somewhere durable, such as object
storage or a GitHub release, and check it against `data/manifest.json`. To move to a new
release, change `OVERTURE_RELEASE` in `pipeline/bam_pipeline/config.py`, rebuild, and
note the change in `CHANGELOG.md`.

## Deploying

The site is published to GitHub Pages at https://matthew6113.github.io/BAM/ by
`.github/workflows/deploy.yml`.

- **Push to main:** builds the map data, runs the tests, builds the site with base path `/BAM/` and deploys it.
- **Pull requests:** build and test only.
- **Caching:** the tiles are cached between runs and rebuilt only when the pipeline changes.
- **Archive:** on main, the Overture extract is also saved as a release asset (`overture-2026-09-23.1`). Builds keep working after Overture removes the release.

One-time setup:
1. The repository must be public, or on a paid plan.
2. In Settings, then Pages, set Source to **GitHub Actions**.

To host the tiles elsewhere, for example object storage, build with
`VITE_TILE_BASE_URL=https://…/tiles`. The host needs HTTP Range support and CORS.

## Theme and style panel

Every color lives in `src/theme/theme.json`, and the placeholders come from the spec.
To change the palette, replace that one file.

The style panel edits the theme live. Open it with **Alt+Shift+S** or the Style button in
development, or add `?style=1` to any URL. You can change any color role, try presets
(`src/theme/presets.json`), switch fonts, adjust 3D lighting and height exaggeration, and
toggle layers. A contrast check runs as you edit. **Export JSON** downloads a
`theme.json` ready to commit.

URL options, handy for sharing a view or for screenshots:

- `#map=zoom/lat/lng/bearing/pitch` sets the camera.
- `?view=3d` starts in 3D.
- `?overview=light` uses the lighter low-zoom building tiles.
- `?salt=0` draws salt ponds as land.
- `?context=0` hides freeways, highways, railroads and ferries (shown by default).
- `?mask=0` turns off the tint outside the nine counties.

## Layout

```
data/            projects.json (source of truth), schema, CREDITS.md, manifest.json
docs/            SPEC.md, DECISIONS.md, PLANNING-AUDIT.md, screenshots/
pipeline/        Python data pipeline (uv)
scripts/         glyph builder, screenshot helper
src/             app: map/ (style, view, config), theme/, ui/
tests/           Vitest unit tests, Playwright screenshot spec
```

## Licenses

Base map data © OpenStreetMap contributors and Overture Maps Foundation (ODbL 1.0). See
`data/CREDITS.md` for every dataset, font and library.
