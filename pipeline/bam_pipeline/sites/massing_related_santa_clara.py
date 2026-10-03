"""Related Santa Clara: parcel and block height envelopes from the 2025 Master Community Plan.

Source:
- Related Santa Clara Master Community Plan (MCP) Scheme C Supplement, adopted by City of Santa
  Clara Resolution 25-9467 (rezoning, July 8, 2025); the supplement is the resolution's exhibit.
  It is the newest adopted document with height rules by parcel. Scheme C chapters replace or
  supplement the matching chapters of the original 2016 MCP.
  - Exhibit 4C-1 (Scheme C) "Parcel & Block Key Plan", printed p. 54 (PDF p. 66): parcels 1-5
    (black lines) and the development blocks of Parcels 4 and 5 (red dashed lines). The footnote
    says the retention pond in Parcel 1 "is a City utility facility and not part of the
    development area".
  - Parcels 1 and 2 (light industrial), printed pp. 55 and 57 (PDF pp. 67 and 69): "Buildings
    should be moderate height (roughly one to two high ceiling levels, or 60'). Up to 50% of
    buildings may reach a height of up to 90'". Drawn as 90 ft over a 60-ft base.
  - Parcels 4 and 5 (City Center), printed pp. 59 and 61 (PDF pp. 71 and 73): towers "of up to
    approximately 10-12 stories, with a maximum building height consistent with ALUC regulations
    and Federal Aviation hazard limits"; podiums about 2-5 stories. No height in feet.
- The project-wide cap in feet: Revised Land Use CEQA Addendum 4 (Resolution 25-9465, PDF p. 16,
  footnote 2): "The maximum allowable height of the Approved Project at 17 stories, or 190 feet, is
  measured against the finished grade of the on-site streets." The 2016 MCP (Resolution 16-8339,
  PDF p. 294) likewise says buildings "will not exceed 17 stories on any parcel", and the Scheme C
  program tables allow up to 17 floors on Parcels 4 and 5. So the blocks of Parcels 4 and 5 are
  drawn to 190 ft. The Scheme C text removes the old 219-ft-above-sea-level limit on Parcel 4; the
  Planning Commission report of June 11, 2025 (p. 6) notes the site is now outside the Airport
  Influence Area.

What this is and isn't:
- Each parcel or block is drawn to its maximum height, not as a building design. Real buildings
  will be lower over most of each zone (Parcels 4 and 5 expect 10-12-story towers on 2-5-story
  podiums), so the massing is labelled illustrative. Heights are above existing ground (the 190 ft
  is measured from the future on-site street grade, which isn't mapped).
- Parcels 1 and 2 are drawn as one zone (same height rules): the exhibit's dividing line doesn't fit
  the site areas in Table 3C-2 (PDF p. 37: 49.6 acres "including 12.8 acres city use area" and 60.9
  acres), which match the county parcels instead. Exhibit 4C-1 draws one red outline around blocks
  WN and WJ, WS and WM, WK and WL, and WF and WG, so each pair is one zone.
- Parcel 3 (the city park) and the retention pond are not massing. The rest of Parcel 1's "city use
  area" isn't located in any figure, so it stays in the zone. The "WA" area of Parcel 5 has no
  block outline in Exhibit 4C-1 and isn't drawn. Open spaces inside blocks are only shown in the
  plan's illustrative ground-floor plans, so the blocks are drawn whole.
- Nothing has been built: the site is vacant (Planning Commission report, June 11, 2025, p. 1).

Georeferencing: Exhibit 4C-1 is an embedded 1920 x 1924 raster with a grey street base map. At
eight intersections the street centrelines are measured in the figure (midway between the curb
lines, from cross-sections along each street) and matched to OpenStreetMap (via Overture) with a
least-squares similarity fit; residuals are recorded. Block outlines are found by casting rays
from a point inside each block to the red dashes; parcels by the black parcel lines.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_related_santa_clara
"""

from __future__ import annotations

import json
import re

import cv2
import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Point, Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "related-santa-clara"
UTM = tb.UTM

MCP = {
    "title": "Master Community Plan Scheme C Supplement (Santa Clara Resolution 25-9467, July 8, 2025)",
    "url": "https://santaclara.legistar1.com/santaclara/attachments/9db31837-65bc-485b-a1ef-ce58bade9f50.pdf",
    "sha256": "1bb080abf779c99a347a2d8b94d3985a7a1e971fdd3f7dbaa7d2d7042c79543f",
    "file": "rsc-res-25-9467-mcp-scheme-c.pdf",
}
FIG = {"page_index": 65, "printed_page": "54", "figure": "Exhibit 4C-1 (Scheme C), Parcel & Block Key Plan"}
IMAGE_SIZE = (1924, 1920)  # rows, columns of the embedded map raster
ADDENDUM = (
    "CEQA Addendum 4 (Resolution 25-9465, July 8, 2025), PDF p. 16, note 2 "
    "(https://santaclara.legistar1.com/santaclara/attachments/595ea4c8-fb0f-4da1-bb99-eace63cf42ed.pdf)"
)

# Height text the module checks in the supplement (0-based page index: phrase).
HEIGHT_TEXT = {
    66: ["or 60’). Up to 50%", "height of up to 90’"],
    68: ["or 60’). Up to 50%", "height of up to 90’"],
    70: ["approximately 10-12 stories", "Part 77 criteria"],
    72: ["approximately 10-12 stories", "Part 77 criteria"],
}

# Intersections: rough figure pixel and rough UTM position. The figure point is then measured
# from the drawn curb lines and the OSM point is where the named streets cross nearest the guess.
CONTROLS = {
    ("Lafayette Street", "Tasman Drive"): ((1052, 1720), (591468, 4140468)),
    ("Lick Mill Boulevard", "Tasman Drive"): ((1591, 1741), (591892, 4140685)),
    ("Calle del Sol", "Tasman Drive"): ((1328, 1734), (591686, 4140576)),
    ("Calle de Luna", "Lafayette Street"): ((1053, 1525), (591385, 4140618)),
    ("Calle del Mundo", "Lafayette Street"): ((1055, 1368), (591318, 4140740)),
    ("Great America Way", "Lafayette Street"): ((1132, 280), (590906, 4141610)),
    ("Great America Parkway", "Great America Way"): ((518, 377), (590476, 4141270)),
    ("Great America Parkway", "Old Mountain View-Alviso Road"): ((308, 741), (590472, 4140899)),
}
ROAD_RGB = (215, 217, 220)  # street fill in the base map
MEDIAN_GAP_PX = {"Tasman Drive": 14}  # Tasman's light-rail median splits the street fill

DARK_MAX = 90  # parcel lines are black
RED_RGB = (216, 56, 58)  # block lines are red dashes
SITE_RGB = (222, 100, 59)  # the orange site line, kept apart from the red
POND_RGB = (210, 228, 234)
PARCEL_LINE_HALF_PX = 5  # parcel lines are about 11 px wide
BLOCK_LINE_HALF_PX = 3

# One point inside each zone (raster pixels).
# Parcels 1 and 2 share their height rules and are drawn as one zone: the exhibit's line between
# them doesn't fit Table 3C-2's site areas (49.6 and 60.9 acres, which match the county parcels).
PARCELS = {"1": (1300, 560), "2": (1300, 1100)}
# Exhibit 4C-1 draws one red outline around WN and WJ, WS and WM, WK and WL, and WF and WG (a
# street or paseo runs through each), so each pair is one zone.
BLOCKS = {
    "WN and WJ": ("4", (444, 1030)), "WP&WR": ("4", (690, 1030)), "WS and WM": ("4", (896, 1030)),
    "WK and WL": ("4", (600, 1180)), "WE": ("4", (472, 1380)),
    "WF and WG": ("4", (600, 1380)), "WH": ("4", (896, 1380)),
    "WB": ("5", (600, 1580)), "WC/WD": ("5", (800, 1580)),
}

INDUSTRIAL_FT, INDUSTRIAL_BASE_FT = 90, 60
CITY_CENTER_FT = 190
PHASE = {"5": "Phase 1", "4": "Phase 2"}  # Development Area Plans 1 (Parcel 5) and 2 (Parcel 4), 2020


def _image(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    for o in page.get_objects():
        if o.type != pdfium.raw.FPDF_PAGEOBJ_IMAGE:
            continue
        rgb = np.asarray(o.get_bitmap(render=False).to_pil().convert("RGB"))
        if rgb.shape[:2] == IMAGE_SIZE:
            return rgb
    raise SystemExit("Exhibit 4C-1 map raster not found")


def _check_text(pdf_path) -> None:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    for i, phrases in HEIGHT_TEXT.items():
        text = re.sub(r"\s+", " ", doc[i].get_textpage().get_text_range()).replace("'", "’")
        for p in phrases:
            if p not in text:
                raise SystemExit(f"MCP Scheme C p. {i + 1}: expected {p!r}")


# ---------------------------------------------------------------- georeference

def _crossing(streets, a, b, guess) -> np.ndarray:
    la = shapely.union_all(streets[streets["name"] == a].geometry.to_numpy())
    lb = shapely.union_all(streets[streets["name"] == b].geometry.to_numpy())
    pts = shapely.get_coordinates(la.intersection(lb))
    near = pts[np.linalg.norm(pts - guess, axis=1) < 40] if len(pts) else pts
    if not len(near):
        raise SystemExit(f"{a} and {b} do not cross near {guess} in OpenStreetMap")
    return near.mean(axis=0)  # divided roads cross more than once; use the middle


def _centres(road, streets, name, junction, to_fig, r0=22, r1=70) -> np.ndarray:
    """Street centre points in the figure: cross-sections of the grey fill along the OSM line."""
    gap = MEDIAN_GAP_PX.get(name, 6)
    line = shapely.union_all(streets[streets["name"] == name].geometry.to_numpy())
    ring = Point(junction).buffer(r1).difference(Point(junction).buffer(r0))
    part = line.intersection(ring)
    t = np.arange(-45, 45.01, 0.5)
    out = []
    for ln in getattr(part, "geoms", [part]):
        if ln.is_empty or ln.length < 5:
            continue
        for s in np.arange(0, ln.length, 4):
            a = to_fig(shapely.get_coordinates(ln.interpolate(s)))[0]
            d = (to_fig(shapely.get_coordinates(ln.interpolate(min(s + 2, ln.length))))[0]
                 - to_fig(shapely.get_coordinates(ln.interpolate(max(s - 2, 0))))[0])
            u = d / np.linalg.norm(d)
            n = np.array([-u[1], u[0]])
            q = np.round(a + t[:, None] * n).astype(int)
            if (q < 0).any() or (q[:, 0] >= road.shape[1]).any() or (q[:, 1] >= road.shape[0]).any():
                continue
            idx = np.flatnonzero(road[q[:, 1], q[:, 0]])
            if not len(idx):
                continue
            lo = hi = idx[np.argmin(np.abs(t[idx]))]
            while len(nxt := idx[(idx < lo) & (idx >= lo - 2 * gap)]):
                lo = nxt.min()
            while len(nxt := idx[(idx > hi) & (idx <= hi + 2 * gap)]):
                hi = nxt.max()
            if t[hi] - t[lo] <= 80:
                out.append(a + (t[lo] + t[hi]) / 2 * n)
    if len(out) < 8:
        raise SystemExit(f"{name}: too few cross-sections near {junction}")
    return np.array(out)


def _fit_line(pts: np.ndarray):
    keep = np.ones(len(pts), bool)
    for _ in range(10):
        m = pts[keep].mean(0)
        d = np.linalg.svd(pts[keep] - m)[2][0]
        r = np.abs((pts - m) @ np.array([-d[1], d[0]]))
        new = r <= max(2.0, 3 * np.median(r[keep]))
        if (new == keep).all():
            break
        keep = new
    return m, d


def georeference(rgb: np.ndarray, streets: gpd.GeoDataFrame) -> trace.Similarity:
    road = np.abs(rgb.astype(int) - ROAD_RGB).max(axis=2) <= 6
    rough = trace.fit_similarity([px for px, _ in CONTROLS.values()], [g for _, g in CONTROLS.values()])
    inv = np.linalg.inv(rough.matrix())

    def to_fig(xy):
        a = (inv @ (np.asarray(xy, float).reshape(-1, 2) - [rough.tx, rough.ty]).T).T
        a[:, 1] *= -1
        return a

    src, dst, labels = [], [], []
    for (a, b), (_, guess) in CONTROLS.items():
        j = _crossing(streets, a, b, np.asarray(guess, float))
        (ma, da), (mb, db) = (_fit_line(_centres(road, streets, n, j, to_fig)) for n in (a, b))
        s = np.linalg.solve(np.c_[da, -db], mb - ma)
        src.append(ma + s[0] * da)
        dst.append(j)
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


# ---------------------------------------------------------------- tracing

def _polys(mask: np.ndarray, min_px: float = 400):
    contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    polys = [shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5)) for c in contours if cv2.contourArea(c) >= min_px]
    return shapely.union_all(polys) if polys else Polygon()


def _region(regions: np.ndarray, seed, grow_px: int, max_px: int, what: str) -> np.ndarray:
    x, y = seed
    region = (regions == regions[y, x]).astype(np.uint8)
    if regions[y, x] == 0 or region.sum() > max_px:
        raise SystemExit(f"{what} is not closed in the figure ({region.sum()} px)")
    contours, _ = cv2.findContours(region * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros_like(region)
    cv2.drawContours(mask, contours, -1, 1, cv2.FILLED)  # fill the holes text and drawings leave
    k = 2 * grow_px + 1
    return cv2.dilate(mask, np.ones((k, k), np.uint8)) > 0  # grow to the middle of the line


def _cast(wall: np.ndarray, seed, what: str, n: int = 720, rmax: float = 500) -> Polygon:
    ang = np.arange(n) * 2 * np.pi / n
    steps = np.arange(1, rmax, 0.5)
    r = np.full(n, np.nan)
    for i, a in enumerate(ang):
        x = np.round(seed[0] + steps * np.cos(a)).astype(int)
        y = np.round(seed[1] + steps * np.sin(a)).astype(int)
        ok = (x >= 0) & (x < wall.shape[1]) & (y >= 0) & (y < wall.shape[0])
        hit = np.flatnonzero(wall[y[ok], x[ok]])
        if len(hit):
            r[i] = steps[hit[0]]
    w = 15
    pad = np.r_[r[-w:], r, r[:w]]
    med = np.array([np.nanmedian(pad[i:i + 2 * w + 1]) for i in range(n)])
    bad = np.isnan(r) | (r > 1.25 * med)
    if bad.sum() > n * 0.05:
        raise SystemExit(f"Block {what}: outline open in {bad.sum()} of {n} directions")
    r[bad] = med[bad]
    poly = shapely.make_valid(Polygon(np.c_[seed[0] + r * np.cos(ang), seed[1] + r * np.sin(ang)]))
    # An opening removes the thin spikes left by rays that slipped through a gap to a nearby line.
    return trace.largest_polygon(poly.buffer(-6, join_style="mitre").buffer(6, join_style="mitre")).simplify(0.7)


def trace_zones(rgb: np.ndarray) -> list[dict]:
    zones = []
    dark = (rgb.max(axis=2) < DARK_MAX).astype(np.uint8)
    _, regions = cv2.connectedComponents(1 - dark, connectivity=4)
    pond = np.abs(rgb.astype(int) - POND_RGB).max(axis=2) <= 6
    mask = np.zeros(dark.shape, bool)
    for name, seed in PARCELS.items():
        mask |= _region(regions, seed, PARCEL_LINE_HALF_PX, 900_000, f"Parcel {name}")
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)) > 0  # the shared line
    wet = cv2.morphologyEx((pond & mask).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(wet)
    big = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 5000]
    if len(big) != 1:
        raise SystemExit(f"expected one retention pond in Parcel 1, found {len(big)}")
    zones.append({"parcel": "1 and 2", "block": None, "px": _polys(mask), "pond_px": _polys(lab == big[0])})
    # Blocks: cast rays from a point inside each block to the red dashes (joined by a closing) or a
    # thick black parcel line; rays that slip through a gap take the median of their neighbours.
    dr = np.linalg.norm(rgb.astype(float) - RED_RGB, axis=2)
    red = ((dr < 70) & (dr < np.linalg.norm(rgb.astype(float) - SITE_RGB, axis=2))).astype(np.uint8)
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8))
    thick = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))  # parcel lines, not text
    wall = (red | thick) > 0
    for block, (parcel, seed) in BLOCKS.items():
        outline = _cast(wall, seed, block)
        px = outline.buffer(BLOCK_LINE_HALF_PX, join_style="mitre")  # to the middle of the dashes
        zones.append({"parcel": parcel, "block": block, "px": px, "pond_px": Polygon()})
    return zones


def main() -> None:
    pdf_path = trace.fetch_document(MCP["url"], tb.DOCS / MCP["file"], MCP["sha256"])
    _check_text(pdf_path)
    rgb = _image(pdf_path)
    streets = tb.streets("rsc-related-santa-clara", (-121.990, 37.395, -121.955, 37.420))
    streets = streets[streets["subtype"] == "road"]
    sim = georeference(rgb, streets)
    print(f"[{PROJECT_ID}] Exhibit 4C-1 georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f} deg")

    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]
    zones = trace_zones(rgb)
    for z in zones:
        g = sim.geometry(z["px"])
        if not z["pond_px"].is_empty:
            pond = sim.geometry(z["pond_px"])
            z["pond_ac"] = pond.area / tb.ACRE_M2
            g = g.difference(pond)
        z["utm"] = trace.as_multipolygon(shapely.make_valid(g.simplify(0.4)))
        inside = z["utm"].intersection(site_utm).area / z["utm"].area
        what = f"Parcel {z['parcel']}" + (f" block {z['block']}" if z["block"] else "")
        print(f"[{PROJECT_ID}]   {what:>22}: {z['utm'].area / tb.ACRE_M2:5.1f} ac, {inside:.0%} inside the site"
              + (f" (retention pond {z['pond_ac']:.1f} ac cut out)" if "pond_ac" in z else ""))

    fig = f"{MCP['title']}, {FIG['figure']}, p. {FIG['printed_page']}"
    features = []
    for z in zones:
        parcel, block = z["parcel"], z["block"]
        if block is None:
            props = {
                "kind": "block", "block": "Parcels 1 and 2", "label": "Parcels 1 and 2",
                "stage": "entitled", "height_ft": INDUSTRIAL_FT, "podium_ft": INDUSTRIAL_BASE_FT, "base_ft": 0,
                "use": "Light industrial (Scheme C)", "phase": None, "illustrative": True,
                "source": (f"illustrative: parcels outlined from {fig}, without the retention pond (the exhibit's "
                           f"note: not part of the development area); drawn to {INDUSTRIAL_FT} ft over a "
                           f"{INDUSTRIAL_BASE_FT}-ft base from the Parcel 1 and 2 building heights, pp. 55 and 57 "
                           f"(\"roughly one to two high ceiling levels, or 60'. Up to 50% of buildings may reach "
                           f"a height of up to 90'\")"),
                "note": ("Light industrial campuses. Up to half of the buildings may rise above 60 ft, to 90 ft. "
                         "The city's retention pond is left out."),
            }
        else:
            page = {"4": "59", "5": "61"}[parcel]
            props = {
                "kind": "block", "block": block, "label": ("Blocks " if " and " in block else "Block ") + block,
                "stage": "entitled", "height_ft": CITY_CENTER_FT, "podium_ft": None, "base_ft": 0,
                "use": "Mixed use: residential, office, hotel and retail", "phase": PHASE[parcel],
                "illustrative": True,
                "source": (f"illustrative: block outlined from {fig}; drawn to the project's {CITY_CENTER_FT}-ft "
                           f"maximum (17 stories, measured from the finished grade of the on-site streets; "
                           f"{ADDENDUM}). The Parcel {parcel} guidelines (p. {page}) expect towers of about "
                           f"10-12 stories on 2-5-story podiums"),
                "note": f"Parcel {parcel}. Towers are expected to be about 10-12 stories; 190 ft is the cap.",
            }
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(z["utm"]))})

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each zone is drawn to its maximum height under the 2025 Master Community "
                "Plan Scheme C Supplement, not as a building design. The light-industrial Parcels 1 and 2 rise to "
                "90 ft over a 60-ft base (up to half the buildings may exceed 60 ft); the City Center blocks of "
                "Parcels 4 and 5 rise to the project's 190-ft (17-story) cap, though the plan expects 10-12-story "
                "towers on low podiums. The city park (Parcel 3) and the retention pond are not massing; nothing "
                "has been built."
            ),
            "note": ("Parcels and blocks are drawn to their height limits in the 2025 master plan, not as building "
                     "designs; real buildings will be lower over most of each block."),
            "sourceUrl": MCP["url"],
            "sourceLabel": "Master Community Plan Scheme C, 2025 (PDF)",
            "georeference": {"exhibit_4c_1": sim.report()},
            "license": "Parcel and block shapes: traced from a public City of Santa Clara document. "
                       "Georeference: " + tb.OSM_LICENSE + ".",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[{PROJECT_ID}] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
