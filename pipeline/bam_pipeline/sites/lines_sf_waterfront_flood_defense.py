"""San Francisco waterfront flood defenses: the Recommended Plan's shoreline line, by reach.

No GIS of the Recommended Plan's defense line is published (USACE's Final Report is not
scriptable and the Port's open data has only the jurisdiction polygon). The plan itself "indicates
approximately where to build flood defenses" (Recommended Plan Highlights, Aug 2026, p. 18).

Source figure: Port of San Francisco, "USACE Flood Study Update and Next Steps", Port Commission
presentation, Aug 11, 2026 (https://www.sfport.com/media/11441/download), slide 13, "Draft
Phasing and Implementation Strategy": a plan-view map (1536 x 741 px raster, drawn rotated with
the Bay at the top) of the Port shoreline from Aquatic Park to Heron's Head Park, coloured by
"Flood Impact Segments" (the sea level rise at which each stretch is first overtopped in a 100-year
tide), with the four reaches separated by dashed lines and the subreaches outlined.

Method:
- Georeference: the base map's street casings (light, unsaturated, thin) are matched to DataSF
  street centrelines (Streets - Active and Retired, 3psu-pn9h; ODC PDDL): a coarse search over
  scale and rotation (template matching for the shift), then trimmed ICP (traced_boundaries.icp,
  built on trace.fit_similarity). The RMS over the closest 50% of street pixels is reported.
- Line: the coloured flood-impact segments (red, orange, yellow, green), thinned to a one-pixel
  centreline (Zhang-Suen) and split into branches.
- Reaches: the three dashed reach boundaries, located by hand at their two ends in the figure
  (pixels below), cut the line into Reach 1 Fisherman's Wharf, Reach 2 Embarcadero, Reach 3 South
  Beach / Mission Bay and Reach 4 Islais Creek / Bayview (names and limits from the Highlights, p. 38).

What it isn't: the engineered alignment. Where a defense sits relative to the shoreline (bayward,
at the shoreline, or inland) is decided in design; the map draws the shoreline stretches it
protects. Labelled approximate.

    uv run --directory pipeline python -m bam_pipeline.sites.lines_sf_waterfront_flood_defense
"""

from __future__ import annotations

import urllib.parse
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import shapely
import shapely.ops
from shapely.geometry import LineString, MultiLineString, Point

from .. import config, trace
from . import line_georef as lg
from .lines import UTM, write_line_project

PROJECT_ID = "sf-waterfront-flood-defense"
DECK = {
    "title": "Port of San Francisco, USACE Flood Study Update and Next Steps (Port Commission, Aug 11, 2026)",
    "url": "https://www.sfport.com/media/11441/download",
    "sha256": "798e29aaa764d81c13106c055000535beb36a1f216f2f0ca3e736ef46d6ecd8e",
    "file": "sfport-flood-study-update-2026-08-11.pdf",
    "page_index": 12,  # slide 13
    "size": (1536, 741),
    "figure": "slide 13, Draft Phasing and Implementation Strategy",
}
HIGHLIGHTS = "https://www.sfport.com/sites/default/files/2026-08/260817_Highlights%20Document_Rec%20Plan.pdf"
STREETS = {
    "title": "DataSF Streets - Active and Retired (3psu-pn9h)",
    "landing": "https://data.sf.gov/d/3psu-pn9h",
    "api": "https://data.sf.gov/resource/3psu-pn9h.geojson",
    "license": "Open Data Commons Public Domain Dedication and License (PDDL) 1.0; City and County of San Francisco",
}
SHORELINE = {
    "title": "DataSF SF Shoreline and Islands (txuc-3kzm)",
    "landing": "https://data.sf.gov/d/txuc-3kzm",
    "api": "https://data.sf.gov/resource/txuc-3kzm.geojson",
    "license": "ODC PDDL 1.0",
}
RAW = config.ROOT / "data" / "raw" / "lines"
STREETS_CACHE = RAW / "datasf_streets_waterfront.geojson"
SHORELINE_CACHE = RAW / "datasf_shoreline.geojson"
BBOX = (37.725, -122.432, 37.812, -122.36)  # south, west, north, east
# Rough start for the fit: the figure's centre near Mission Creek at Fourth Street, about 6 m/px
# (the 1,000-ft scale bar), drawn with the Bay up (rotated about 70 degrees).
START = {"fig": (768, 370), "lonlat": (-122.396, 37.774), "scale": 6.0, "rotation_deg": -71}
EXCLUDE = [(1000, 0, 1536, 60)]  # scale bar, north arrow and "San Francisco Bay"
# Dashed reach boundaries, both ends located by hand in the figure (pixels).
REACH_BOUNDARIES = [((240, 95), (308, 228)), ((590, 35), (642, 178)), ((1200, 165), (1100, 385))]
REACHES = [
    "Reach 1, Fisherman's Wharf (Aquatic Park to Telegraph Hill)",
    "Reach 2, Embarcadero (Telegraph Hill to the Bay Bridge)",
    "Reach 3, South Beach / Mission Bay (Bay Bridge to Potrero Point)",
    "Reach 4, Islais Creek / Bayview (Potrero Point to Heron's Head Park)",
]


def _fetch(api: str, cache, where: str) -> gpd.GeoDataFrame:
    if not cache.exists():
        q = urllib.parse.urlencode({"$where": where, "$limit": 50000})
        with urllib.request.urlopen(f"{api}?{q}") as r:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(r.read())
    return gpd.read_file(cache).to_crs(UTM)


def main() -> None:
    pdf = trace.fetch_document(DECK["url"], config.ROOT / "data" / "raw" / "docs" / DECK["file"], DECK["sha256"])
    rgb = lg.pdf_image(pdf, DECK["page_index"], DECK["size"])
    s, w, n, e = BBOX
    streets = _fetch(STREETS["api"], STREETS_CACHE, f"active='true' AND within_box(line, {n}, {w}, {s}, {e})")
    shore = _fetch(SHORELINE["api"], SHORELINE_CACHE, "1=1")

    # Street casings: light, unsaturated, thin
    a = rgb.astype(int)
    g = a.mean(2).astype(np.float32)
    casing = ((g - cv2.GaussianBlur(g, (0, 0), 3)) > 3) & ((a.max(2) - a.min(2)) < 10)
    for x0, y0, x1, y1 in EXCLUDE:
        casing[y0:y1, x0:x1] = False
    c = lg.wgs_to_utm(Point(START["lonlat"]))
    init = lg.anchored(START["fig"], (c.x, c.y), START["scale"], START["rotation_deg"])
    coarse, corr = lg.coarse_roads(casing, streets, init, scale_range=0.25, rot_range=12, rot_step=1.0, pad=180)
    ys, xs = np.nonzero(casing)
    sel = np.random.default_rng(0).choice(len(xs), min(25000, len(xs)), replace=False)
    pts = np.c_[xs[sel], ys[sel]].astype(float)
    target = streets[streets.intersects(lg.footprint(coarse, *DECK["size"]))].geometry.union_all()
    sim, rep = lg.register_roads(pts, target, coarse, keep=0.5, what="street casings vs DataSF street centrelines")
    rep["coarse_correlation"] = round(corr, 3)
    print(f"[waterfront] fit {rep['scale_m_per_unit']} m/px, rotation {rep['rotation_deg']} deg, trimmed RMS {rep['rms_m']} m, "
          f"median {rep['median_m']} m")

    # Flood-impact segments: saturated reds, oranges, yellows and greens (the subreach fills are blue)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    m = (hsv[..., 1] > 85) & ((hsv[..., 0] < 85) | (hsv[..., 0] > 160)) & (hsv[..., 2] > 60)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    branches = lg.component_paths(lg._thin(m.astype(bool)), min_px=12)
    px = MultiLineString(branches).simplify(1.0)
    print(f"[waterfront] {len(branches)} traced piece(s)")

    # Cut into reaches at the dashed boundaries (extended a little past their drawn ends).
    pieces = list(getattr(px, "geoms", [px]))
    cutters = []
    for p, q in REACH_BOUNDARIES:
        d = np.subtract(q, p) / np.hypot(*np.subtract(q, p))
        cutters.append(LineString([np.subtract(p, d * 40), np.add(q, d * 40)]))
    reach_of = []
    for piece in pieces:
        parts = shapely.ops.split(piece, shapely.MultiLineString(cutters)) if any(piece.intersects(c) for c in cutters) else [piece]
        for part in getattr(parts, "geoms", parts):
            mid = part.interpolate(0.5, normalized=True)
            # which side of each boundary: count boundaries the point is "past" (east/south along the shore)
            k = sum(1 for (p, q) in REACH_BOUNDARIES
                    if (q[0] - p[0]) * (mid.y - p[1]) - (q[1] - p[1]) * (mid.x - p[0]) < 0)
            reach_of.append((k, part))
    by_reach: dict[int, list[LineString]] = {}
    for k, part in reach_of:
        by_reach.setdefault(k, []).append(part)

    features, lens = [], {}
    for k in sorted(by_reach):
        geom_px = shapely.line_merge(MultiLineString(by_reach[k]))
        geom = sim.geometry(geom_px)
        lens[REACHES[k]] = geom.length
        features.append({"geometry": lg.utm_to_wgs(geom), "properties": {
            "kind": "line", "segment": "new", "name": REACHES[k],
            "source": (f"traced: {DECK['title']}, {DECK['figure']}: the 'Flood Impact Segments' line between the dashed reach "
                       f"boundaries (trimmed RMS {rep['rms_m']} m georeference)."),
        }})
    total = sum(lens.values())
    print("[waterfront] " + "; ".join(f"{k.split(',')[0]} {v / 1609.344:.2f} mi" for k, v in lens.items()) + f"; total {total / 1609.344:.2f} mi")

    # Check against the DataSF shoreline
    shore_line = shore.geometry.union_all().boundary
    samples = [ln.interpolate(t) for _, p in reach_of for ln in [sim.geometry(p)] for t in np.arange(0, ln.length, 25)]
    dist = np.array([shore_line.distance(p) for p in samples])
    check = (f"Sampled every 25 m, the traced line lies a median {np.median(dist):.0f} m (90th percentile {np.quantile(dist, 0.9):.0f} m) "
             f"from the DataSF shoreline ({SHORELINE['landing']}).")
    print("[waterfront] " + check)

    meta = {
        "source": f"{DECK['title']}, {DECK['figure']}, georeferenced to DataSF street centrelines",
        "sourceLabel": "Port Commission presentation (Aug 11, 2026), phasing map",
        "sourceUrl": DECK["url"],
        "accuracy": "approximate",
        "accuracyNote": (
            f"Approximate alignment: the shoreline stretches the Port's phasing map marks as flood-impact segments, which the "
            f"Recommended Plan defends ('indicates approximately where to build flood defenses', Recommended Plan Highlights, p. 18). "
            f"{total / 1609.344:.1f} miles as drawn, because the line follows the water's edge into Mission Creek and Islais Creek "
            f"(both banks) and around the Pier 80-96 terminals; the Port describes its jurisdiction as '7.5 miles' of shoreline. "
            f"The map is small-scale (about {rep['scale_m_per_unit']:.0f} m per pixel) and fitted to DataSF "
            f"streets with a trimmed RMS of {rep['rms_m']} m, so the line is good to roughly 20-40 m. Where each defense "
            "sits (bayward, at the shoreline or inland) is decided in design. Reaches split at the map's dashed boundaries."),
        "license": (f"Traced facts from a public Port of San Francisco presentation (the PDF is not redistributed). "
                    f"Georeference: {STREETS['title']}, {STREETS['license']}. Check: {SHORELINE['title']}, {SHORELINE['license']}."),
        "otherSources": [HIGHLIGHTS, STREETS["landing"], SHORELINE["landing"]],
        "georeference": rep,
        "check": check,
    }
    write_line_project(PROJECT_ID, features, meta, corridor_m=60)


if __name__ == "__main__":
    main()
