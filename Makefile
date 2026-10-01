# Bay Area megaprojects map. `make data` rebuilds every generated file from scratch
# inputs; `make help` lists the targets.

PY = uv run --directory pipeline python -m

.PHONY: help data tools fetch process buildings tiles fonts glyphs manifest dev build test screenshots clean-build

help:
	@echo "make data         Full data pipeline: fetch, process, tile, fonts, glyphs, manifest"
	@echo "make tools        Check that uv, node and tippecanoe are installed"
	@echo "make fetch        Download the Overture extracts into data/raw/ (cached)"
	@echo "make tiles        Rebuild PMTiles from data/build/"
	@echo "make dev          Start the dev server (http://127.0.0.1:5173)"
	@echo "make test         Data schema and theme tests"
	@echo "make screenshots  Playwright screenshots of key views into docs/screenshots/"

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

dev:
	npx vite --host 127.0.0.1

build:
	npm run build

test:
	npm test

screenshots:
	npx playwright test tests/screenshots.spec.ts

clean-build:
	rm -rf data/build public/generated
