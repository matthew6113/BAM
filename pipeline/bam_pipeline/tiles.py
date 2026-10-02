"""Tile the processed layers into PMTiles with Tippecanoe (2.79.0).

Archives in public/generated/tiles/:
- base.pmtiles: region mask, water, shoreline, context lines (z4-z14)
- buildings-overview-{variant}.pmtiles: every footprint as shape only (z6-z12)
- buildings-z13/z14/z15.pmtiles: full footprints with mapped heights, attribute h, one
  archive per zoom (z15 is overzoomed beyond 15)

The overview has two variants for the M1 look review:
- "all": no tile size limit. Every building is kept; sub-pixel footprints are
  accumulated into pixel-sized squares (Tippecanoe's tiny-polygon reduction), the
  same technique behind the NYT building map. Heavier tiles.
- "light": the standard 500 KB tile budget, dropping buildings in the densest
  areas. Lighter, but dense cores thin out.

    uv run --directory pipeline python -m bam_pipeline.tiles [base] [overview-all] [overview-light] [buildings-z13] ...
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time

from . import config

TIPPECANOE_VERSION = "2.79.0"
ATTRIBUTION = (
    '<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, '
    '<a href="https://overturemaps.org">Overture Maps Foundation</a>'
)
LICENSE_NOTE = (
    f"Derived from Overture Maps release {config.OVERTURE_RELEASE} "
    "(OpenStreetMap, Microsoft ML Buildings, Esri Community Maps, USGS lidar heights). "
    "Database license: ODbL-1.0."
)


def check_tippecanoe() -> None:
    exe = shutil.which("tippecanoe")
    if not exe:
        sys.exit("tippecanoe not found. Install 2.79.0 (macOS: brew install tippecanoe; see README).")
    out = subprocess.run([exe, "--version"], capture_output=True, text=True)
    version = (out.stdout + out.stderr).strip().split()[-1].lstrip("v")
    if version != TIPPECANOE_VERSION:
        print(f"[tiles] warning: tippecanoe {version} found, pipeline is pinned to {TIPPECANOE_VERSION}; "
              "tiles may differ byte for byte")


def run(name: str, args: list[str]) -> None:
    out = config.TILES_OUT / f"{name}.pmtiles"
    config.TILES_OUT.mkdir(parents=True, exist_ok=True)
    cmd = [
        "tippecanoe", "-o", str(out), "--force", "--quiet",
        "--name", f"Bay Area megaprojects: {name}",
        "--attribution", ATTRIBUTION,
        "--description", LICENSE_NOTE,
        *args,
    ]
    t0 = time.time()
    subprocess.run(cmd, check=True)
    print(f"[tiles] {name}: {out.stat().st_size / 1e6:.1f} MB in {time.time() - t0:.0f}s")


B = config.BUILD
BUILDS = {
    "base": [
        "-Z4", "-z14",
        "--no-tiny-polygon-reduction", "--no-feature-limit", "--no-tile-size-limit",
        "--detect-shared-borders", "--simplification=2",
        "-L", f"region_mask:{B / 'region_mask.geojsonl'}",
        "-L", f"water:{B / 'water.geojsonl'}",
        "-L", f"shoreline:{B / 'shoreline.geojsonl'}",
        "-L", f"context:{B / 'context.geojsonl'}",
    ],
    "buildings-overview-all": [
        "-Z6", "-z12", "-X", "-l", "buildings",
        "--no-feature-limit", "--no-tile-size-limit",
        str(B / "buildings.fgb"),
    ],
    "buildings-overview-light": [
        "-Z6", "-z12", "-X", "-l", "buildings",
        "--drop-densest-as-needed",
        str(B / "buildings.fgb"),
    ],
    # Detail tiles are split by zoom so every file stays under 100 MB (GitHub's per-file limit).
    **{
        f"buildings-z{z}": [
            f"-Z{z}", f"-z{z}", "-l", "buildings", "-y", "h",
            "--no-feature-limit", "--no-tile-size-limit",
            str(B / "buildings.fgb"),
        ]
        for z in (13, 14, 15)
    },
}

ALIASES = {"overview-all": "buildings-overview-all", "overview-light": "buildings-overview-light"}


def main(argv: list[str]) -> None:
    check_tippecanoe()
    names = [ALIASES.get(a, a) for a in argv] or list(BUILDS)
    for name in names:
        run(name, BUILDS[name])


if __name__ == "__main__":
    main(sys.argv[1:])
