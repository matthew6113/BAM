# Bay Area Megaprojects Map

An interactive 3D web map of the Bay Area's largest development projects, built as a
public portfolio piece for Matthew Huguet ("Matty"). Pan the whole region, click a
project, and the camera makes a slow fly-in: the site boundary draws, proposed buildings
rise in place, and a panel explains what it is, where it stands, and the sources.

## Read before writing code

- `docs/SPEC.md`: full design, interaction, data and technical spec, plus milestones.
- `data/projects.json`: 25 researched projects with stage, program, timeline, summary and
  sources (verified Oct 1, 2026). Treat it as the source of truth for project facts.

## The look in one line

The present as print, the future in color: every existing building is drawn as a quiet,
flat footprint (NYT's "A Map of Every Building in America"), and only the projects get
color and height (Melbourne's Development Activity Model). The more certain a building
is, the more solid it's drawn.

## Ground rules

Accuracy
- Never invent a fact, number, date, boundary or height. If it isn't in
  `data/projects.json` or a source you can cite, mark it as needing verification.
- Every project fact shown in the UI must trace to a source URL in the data.
- Label approximations in the data and in the UI ("Illustrative massing",
  "Approximate boundary").
- Keep `lastVerified` dates honest. Update them only when you actually re-check.

Data and licensing
- Use open data only, and record each dataset's license and required attribution in
  `data/CREDITS.md`. Show credits in the map.
- Renderings: only images with permission (press kits) or that Matthew made. Otherwise
  link to the official page. Never hotlink or scrape renders.
- Keep raw downloads in `data/raw/` (git-ignored). Ask before any single download over
  about 2 GB.
- The data pipeline must be reproducible with one command.

Design
- All colors live in one theme file. Matthew is supplying his own palette, so ship
  placeholder colors and make swapping them a one-file change.
- Sentence case everywhere. Labels sparse. One orchestrated motion moment: the fly-in.
- Respect `prefers-reduced-motion`. Keyboard accessible. Works on mobile Safari.

Workflow
- Follow the milestones in `docs/SPEC.md`. Stop for Matthew's review after Milestone 1
  (base map look) and Milestone 2 (Potrero Power Station vertical slice).
- Before each checkpoint, take Playwright screenshots of key views and summarize what
  changed and what's still open.
- Commit in small, described steps.
- When you're unsure about a design choice that affects the look, show options rather
  than picking silently.

## Commands

- `npm install` then `make data`: full data pipeline (Overture fetch, process, Tippecanoe
  tiles, fonts, glyphs, manifest). Needs uv and Tippecanoe 2.79.0. Raw downloads are cached
  in `data/raw/`; individual steps are `make fetch|process|buildings|tiles|fonts|glyphs|manifest`.
- `npm run dev`: dev server on http://127.0.0.1:5173 (style panel: Alt+Shift+S or `?style=1`).
- `npm test`: schema check of `data/projects.json` plus theme and contrast tests.
- `npx tsc --noEmit`: type-check. `npm run build`: production build.
- `npm run screenshots`: Playwright screenshots of key views into `docs/screenshots/m1/`
  (headless Chromium with SwiftShader WebGL; set `SHOTS_DIR` to write elsewhere).
- Deploy: not set up yet (Milestone 5). Tiles are too large for a static host and will go to
  object storage; set `VITE_TILE_BASE_URL` to point the app at them.
