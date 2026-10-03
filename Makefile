# Bay Area megaprojects map. `make data` rebuilds every generated file from scratch
# inputs; `make help` lists the targets.

PY = uv run --directory pipeline python -m

.PHONY: help data tools fetch process buildings tiles fonts glyphs manifest sites dev build test e2e screenshots clean-build

help:
	@echo "make data         Full data pipeline: fetch, process, tile, fonts, glyphs, manifest"
	@echo "make tools        Check that uv, node and tippecanoe are installed"
	@echo "make fetch        Download the Overture extracts into data/raw/ (cached)"
	@echo "make tiles        Rebuild PMTiles from data/build/"
	@echo "make sites        Re-trace project boundaries and massing from their source documents"
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
	$(PY) bam_pipeline.sites.massing_piers_30_32
	$(PY) bam_pipeline.sites.massing_mission_bay
	$(PY) bam_pipeline.sites.massing_treasure_island
	$(PY) bam_pipeline.sites.massing_candlestick_point
	$(PY) bam_pipeline.sites.massing_hunters_point_shipyard
	$(PY) bam_pipeline.sites.traced_boundaries

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
