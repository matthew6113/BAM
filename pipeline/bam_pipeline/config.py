"""Pipeline settings. Change the Overture release here and nowhere else."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Overture Maps release. Overture keeps releases for about 60 days, so the clipped
# extract in data/raw/ should be archived (see README, "Reproducing the data").
OVERTURE_RELEASE = "2026-09-23.1"
OVERTURE_BUCKET = "overturemaps-us-west-2"
OVERTURE_REGION = "us-west-2"

# Fetch window: the nine counties' land extent (measured from Overture divisions,
# about -123.536, 36.893, -121.208, 38.864) plus a margin so the edge of the
# pannable area is never blank.
FETCH_BBOX = (-123.75, 36.75, -121.00, 39.00)

# The nine Bay Area counties as Overture names them (division_area, subtype county).
COUNTIES = [
    "Alameda County",
    "Contra Costa County",
    "Marin County",
    "Napa County",
    "San Francisco",
    "San Mateo County",
    "Santa Clara County",
    "Solano County",
    "Sonoma County",
]

# Paths
RAW = ROOT / "data" / "raw" / "overture" / OVERTURE_RELEASE
BUILD = ROOT / "data" / "build"
TILES_OUT = ROOT / "public" / "generated" / "tiles"
DATA_OUT = ROOT / "public" / "generated" / "data"
FONTS_OUT = ROOT / "public" / "generated" / "fonts"
GLYPHS_OUT = ROOT / "public" / "generated" / "glyphs"
REGION_JSON = ROOT / "src" / "generated" / "region.json"
MANIFEST = ROOT / "data" / "manifest.json"

# Building heights: keep only heights that were mapped (OpenStreetMap, Esri
# Community Maps) or measured (USGS lidar). Microsoft ML height estimates are
# dropped, so buildings without a real height stay flat.
DROP_HEIGHT_SOURCES = {"Microsoft ML Buildings"}

# Fonts: google/fonts at a pinned commit (SIL Open Font License 1.1).
GOOGLE_FONTS_COMMIT = "9710da1eacb3be272583c3224dcb70f9da6eadbb"
