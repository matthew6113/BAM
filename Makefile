# Bay Area megaprojects map. `make data` rebuilds every generated file from scratch
# inputs; `make help` lists the targets.

PY = uv run --directory pipeline python -m

.PHONY: help data tools fetch process buildings tiles fonts glyphs manifest sites photos upkeep dev build test e2e screenshots clean-build

help:
	@echo "make data         Full data pipeline: fetch, process, tile, fonts, glyphs, manifest"
	@echo "make tools        Check that uv, node and tippecanoe are installed"
	@echo "make fetch        Download the Overture extracts into data/raw/ (cached)"
	@echo "make tiles        Rebuild PMTiles from data/build/"
	@echo "make sites        Re-trace project boundaries and massing from their source documents"
	@echo "make photos       Download the approved project photos from Wikimedia Commons into public/photos/"
	@echo "make upkeep       Write the update checklist to docs/upkeep/<date>.md (see docs/UPKEEP.md)"
	@echo "make dev          Start the dev server (http://127.0.0.1:5173)"
	@echo "make test         Data, geometry, theme and helper tests"
	@echo "make e2e          Playwright interaction tests (map controls, fly-in, panel, deep links)"
	@echo "make screenshots  Playwright screenshots of key views into docs/screenshots/m1 and m2"

data: tools fetch process buildings tiles fonts glyphs manifest

tools:
	@command -v uv >/dev/null || (echo "Missing uv: https://docs.astral.sh/uv/" && exit 1)
	@command -v node >/dev/null || (echo "Missing Node 22+" && exit 1)
	@command -v tippecanoe >/dev/null || (echo "Missing tippecanoe 2.79.0 (macOS: brew install tippecanoe)" && exit 1)
	@uv sync --directory pipeline --quiet
	@test -d node_modules || npm install

fetch:
	$(PY) bam_pipeline.fetch

process:
	$(PY) bam_pipeline.process

buildings:
	$(PY) bam_pipeline.buildings

tiles:
	$(PY) bam_pipeline.tiles

fonts:
	$(PY) bam_pipeline.fonts

glyphs:
	node scripts/build-glyphs.mjs

manifest:
	$(PY) bam_pipeline.manifest

# Traced project geometry is committed in data/boundaries/ and data/massing/; this redoes it.
# Downloads each source document once (checked by SHA-256) into data/raw/docs/.
sites:
	$(PY) bam_pipeline.sites.potrero_power_station
	$(PY) bam_pipeline.sites.official_boundaries
	$(PY) bam_pipeline.sites.massing_balboa_reservoir
	$(PY) bam_pipeline.sites.massing_mission_rock
	$(PY) bam_pipeline.sites.massing_pier_70
	$(PY) bam_pipeline.sites.massing_stonestown
	$(PY) bam_pipeline.sites.massing_india_basin
	$(PY) bam_pipeline.sites.massing_mission_bay
	$(PY) bam_pipeline.sites.massing_treasure_island
	$(PY) bam_pipeline.sites.massing_candlestick_point
	$(PY) bam_pipeline.sites.massing_hunters_point_shipyard
	$(PY) bam_pipeline.sites.massing_related_santa_clara
	$(PY) bam_pipeline.sites.massing_parkmerced
	$(PY) bam_pipeline.sites.massing_parkline
	$(PY) bam_pipeline.sites.massing_willow_village
	$(PY) bam_pipeline.sites.massing_downtown_west
	$(PY) bam_pipeline.sites.massing_alameda_point
	$(PY) bam_pipeline.sites.massing_the_rise
	$(PY) bam_pipeline.sites.massing_brooklyn_basin
	$(PY) bam_pipeline.sites.massing_berryessa_flea_market
	$(PY) bam_pipeline.sites.massing_middlefield_park
	$(PY) bam_pipeline.sites.massing_tasman_east
	$(PY) bam_pipeline.sites.massing_schlage_lock
	$(PY) bam_pipeline.sites.massing_sunnydale_hope_sf
	$(PY) bam_pipeline.sites.massing_potrero_hope_sf
	$(PY) bam_pipeline.sites.landuse_moffett_park
	$(PY) bam_pipeline.sites.landuse_suisun_expansion
	$(PY) bam_pipeline.sites.landuse_north_bayshore
	$(PY) bam_pipeline.sites.landuse_concord_naval_weapons_station
	$(PY) bam_pipeline.sites.landuse_brisbane_baylands
	$(PY) bam_pipeline.sites.landuse_esmeralda
	$(PY) bam_pipeline.sites.landuse_mare_island
	$(PY) bam_pipeline.sites.traced_boundaries
	$(PY) bam_pipeline.sites.landuse_sonoma_developmental_center
	$(PY) bam_pipeline.sites.lines_bart_silicon_valley_phase_2
	$(PY) bam_pipeline.sites.lines_the_portal
	$(PY) bam_pipeline.sites.lines_cahsr_sf_sj
	$(PY) bam_pipeline.sites.lines_valley_link
	$(PY) bam_pipeline.sites.bart_station_housing

photos:
	$(PY) bam_pipeline.photos

upkeep:
	$(PY) bam_pipeline.upkeep

dev:
	npx vite --host 127.0.0.1

build:
	npm run build

test:
	npm test

e2e:
	npm run e2e

screenshots:
	npm run screenshots

clean-build:
	rm -rf data/build public/generated
