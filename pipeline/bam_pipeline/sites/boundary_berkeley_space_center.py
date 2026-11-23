"""Berkeley Space Center (Berkeley Air & Space Center) at NASA Research Park: the project site, traced.

The site is federal land at NASA Ames Research Center, a portion of Santa Clara County APN 116-18-012,
which is the whole 1,284-acre NASA parcel in the County's layer (data.sccgov.org ubcd-cewv), so no
parcel layer draws it. It is traced from the project's own plan:

- Source: the "Land Use Plan" (Illustrative Land Use Plan) on Development Guidelines p. 29 (PDF p. 93)
  of Appendix 2-1, "Proposed Master Plan, Development Guidelines, and Standards" (Spring 2026), as
  attached to the joint Final EIR/EIS on CEQAnet (SCH 2024060942, document 3). It is the same plan
  as the Final EIR/EIS's Figure 2-6 (PDF p. 232) at a higher resolution (one 3,834 x 2,740 px raster,
  300 dpi), with a 0-400 ft scale bar drawn as vectors on the page.
- The "Project Site" line (grey dash-dot, along the outer edge of the realigned Wescoat, Cody and
  Girard roads, which the site includes) is traced: the dashes are bridged and the enclosed area is
  pulled back to the line's centre. The Final EIR/EIS gives the Project Site as "approximately 39
  acres" (p. 2-4). The black dashed "Parcel Boundary" (the leased premises, 34.92 acres per p. 2-28)
  runs inside it, on the same line along the west end and Girard Road, and is not drawn; where the two
  coincide its dashes help close the site line.

Georeference: the plan's base map is a street map with grey existing buildings outside the site.
Starting from the Wescoat Road / McCord Avenue (Dailey Road) crossing (hand-located) and the scale
bar, a coarse search over rotation and scale correlates the figure's building mask with OpenStreetMap
building footprints (via Overture), and a trimmed ICP of the figure's building outlines onto the
OpenStreetMap footprints refines it. The fitted scale is checked against the scale bar.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_berkeley_space_center
"""

from __future__ import annotations

import json
from functools import lru_cache

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import shapely
from shapely.geometry import shape

from .. import config, trace
from . import line_georef as lg
from . import traced_boundaries as tb

PROJECT = "berkeley-space-center"
CEQANET = "https://ceqanet.lci.ca.gov/Project/2024060942"
FEIR_DOC = "https://ceqanet.lci.ca.gov/2024060942/3"
FEIR = {  # the joint Final EIR/EIS itself (Aug 2026), for the stated acreages
    "url": "https://ceqanet.lci.ca.gov/2024060942/3/Attachment/G8IBj9",
    "sha256": "1607901216bb37c5868d35edc116dc36e1490e1fa4370584b38e6d85e885c351",
}
PLAN = {
    "title": ("Berkeley Space Center Development Guidelines (Spring 2026), Land Use Plan, p. 29: Appendix 2-1 to the "
              "joint Final EIR/EIS (Aug 2026)"),
    "url": "https://ceqanet.lci.ca.gov/2024060942/3/Attachment/YBGZ4B",
    "file": "berkeley-space-center-app2-1-master-plan-guidelines-2026.pdf",
    "sha256": "6b206eb03d9019d46b677137fff18e7b8269b1d412719922598be8d5455c8a6b",
}
PAGE = 92  # zero-based: PDF p. 93, Development Guidelines p. 29 "Land Use Plan"
SIZE = (3834, 2740)  # the map raster, px
FT = 0.3048
BBOX = (-122.062, 37.405, -122.045, 37.418)
NAME = "berkeley_space_center"  # Overture cache name

# Wescoat Road / McCord Avenue, where McCord continues south as Dailey Road (one OpenStreetMap node),
# located by hand in the raster: a start for the search only.
ANCHOR_PX = (1185.0, 822.0)
ANCHOR_STREETS = ("Wescoat Road", "McCord Avenue")
BUILDING_GREY = (200, 200, 200)  # existing buildings in the base map
BUILDING_TOL = 6
MIN_BUILDING_PX = 1500
ICP_KEEP = 0.6
SITE_GREY = (118, 118, 118)  # the "Project Site" dash-dot line
SITE_TOL = 16
SITE_MAX_SAT = 16  # JPEG noise gives the grey line up to about 14 of saturation
SITE_MARGIN_PX = 100  # building-mask pixels this close to the site line are left out of the fit
LINE_HALF_PX = 6  # the site line is about 12 px wide
BRIDGE_PX = 31  # bridges the gaps between dashes
INSIDE_PX = (2000, 1600)  # a raster point inside the site
STATED_SITE_ACRES = 39  # "an approximately 39-acre project site" (Final EIR/EIS p. 2-4)
STATED_PARCEL_ACRES = 34.92  # "the total parcel boundary [34.92 acres]" (Final EIR/EIS p. 2-28)
NEIGHBOURS = ["moffett-park", "north-bayshore"]


@lru_cache(maxsize=1)
def document() -> pdfium.PdfDocument:
    path = trace.fetch_document(PLAN["url"], tb.DOCS / PLAN["file"], PLAN["sha256"])
    return pdfium.PdfDocument(str(path))


@lru_cache(maxsize=1)
def figure() -> np.ndarray:
    page = document()[PAGE]
    text = " ".join(page.get_textpage().get_text_range().split())
    if "LAND USE PLAN" not in text or "Project Site" not in text:
        raise SystemExit(f"PDF p. {PAGE + 1} is not the Development Guidelines Land Use Plan")
    for obj in page.get_objects():
        if obj.type == pdfium_c.FPDF_PAGEOBJ_IMAGE:
            im = obj.get_bitmap(render=False).to_pil().convert("RGB")
            if im.size == SIZE:
                return np.asarray(im)
    raise SystemExit(f"no {SIZE[0]} x {SIZE[1]} raster on PDF p. {PAGE + 1}")


def scale_bar_m_per_px() -> float:
    """The page's 0-400 ft scale bar (vector rectangles) in metres per raster pixel."""
    path = tb.DOCS / PLAN["file"]
    page = pdfplumber.open(str(path)).pages[PAGE]
    words = {w["text"]: w for w in page.extract_words() if w["top"] > 700 and w["x0"] < 260}
    if "400’" not in words or "0’" not in words:
        raise SystemExit("scale bar labels not found")
    bars = [r for r in page.rects if r["top"] > 700 and r["x1"] < 200 and r["bottom"] - r["top"] < 8]
    x0, x1 = min(r["x0"] for r in bars), max(r["x1"] for r in bars)
    image = next(o for o in page.images if (o["srcsize"][0], o["srcsize"][1]) == SIZE)
    px_per_pt = SIZE[0] / (image["x1"] - image["x0"])
    return 400 * FT / ((x1 - x0) * px_per_pt)


def building_mask(rgb: np.ndarray) -> np.ndarray:
    m = (np.abs(rgb.astype(int) - BUILDING_GREY).max(axis=2) <= BUILDING_TOL).astype(np.uint8)
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def outline_points(mask: np.ndarray) -> np.ndarray:
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    h, w = mask.shape
    pts = []
    for c in cs:
        if cv2.contourArea(c) < MIN_BUILDING_PX:
            continue
        c = c.reshape(-1, 2)
        inside = (c[:, 0] > 2) & (c[:, 1] > 2) & (c[:, 0] < w - 3) & (c[:, 1] < h - 3)  # not the frame edge
        pts.append(c[inside][::4])
    return np.vstack(pts).astype(float) + 0.5


@lru_cache(maxsize=1)
def georeference() -> tuple[trace.Similarity, dict]:
    """Figure px (y down) -> UTM 10N: coarse building-mask search, then trimmed ICP on building outlines."""
    rgb = figure()
    buildings = tb.buildings(NAME, BBOX)
    streets = tb.streets(NAME, BBOX)
    anchor = tb.intersection(streets, *ANCHOR_STREETS)
    bar = scale_bar_m_per_px()
    mask = building_mask(rgb)
    # Only the existing buildings around the site: inside it the plan draws new roads in the same grey.
    off = np.zeros_like(mask)
    cv2.fillPoly(off, [np.round(np.asarray(site_px().buffer(SITE_MARGIN_PX).exterior.coords)).astype(np.int32)], 1)
    mask[off > 0] = 0
    h, w = mask.shape
    f, pad = 4, 60
    small = cv2.resize(mask.astype(np.float32), (w // f, h // f), interpolation=cv2.INTER_AREA)
    polys = [np.asarray(p.exterior.coords) for g in buildings.geometry for p in getattr(g, "geoms", [g])]
    best = None
    for s in np.linspace(bar * 0.98, bar * 1.02, 5):
        for r in np.arange(-4.0, 4.001, 0.25):
            sim = lg.anchored(ANCHOR_PX, anchor, s, r)
            m = np.zeros((h // f + 2 * pad, w // f + 2 * pad), np.float32)
            for c in polys:
                q = lg.to_figure(sim, c) / f + pad
                if q[:, 0].max() < 0 or q[:, 1].max() < 0 or q[:, 0].min() > m.shape[1] or q[:, 1].min() > m.shape[0]:
                    continue
                cv2.fillPoly(m, [np.round(q).astype(np.int32)], 1.0)
            res = cv2.matchTemplate(m, small, cv2.TM_CCORR_NORMED)
            _, v, _, loc = cv2.minMaxLoc(res)
            if best is None or v > best[0]:
                best = (v, s, r, loc)
    v, s, r, loc = best
    sim = lg.anchored(ANCHOR_PX, anchor, s, r)
    shift = sim.apply([((loc[0] - pad) * f, (loc[1] - pad) * f)])[0] - sim.apply([(0, 0)])[0]
    sim.tx, sim.ty = sim.tx + shift[0], sim.ty + shift[1]

    pts = outline_points(mask)
    moved = sim.apply(pts)
    near = buildings[buildings.intersects(shapely.box(*(moved.min(0) - 80), *(moved.max(0) + 80)))]
    target = shapely.union_all(near.geometry.boundary.to_numpy())
    fit, d = tb.icp(pts, [target], np.zeros(len(pts), int), sim, keep=ICP_KEEP, iterations=120)
    rep = tb.icp_report(fit, d, ICP_KEEP, "base-map building outlines")
    rep["method"] = ("coarse search (rotation -4 to 4 deg, scale within 2% of the scale bar) correlating the plan's grey "
                     "building mask with OpenStreetMap building footprints (via Overture), started from the Wescoat Road / "
                     "McCord Avenue crossing; then trimmed ICP of the plan's building outlines onto the footprints")
    rep["coarse_correlation"] = round(float(v), 3)
    rep["scale_bar_m_per_px"] = round(bar, 5)
    rep["scale_vs_bar_pct"] = round(100 * (fit.scale / bar - 1), 2)
    rep["anchor_residual_m"] = round(float(np.linalg.norm(fit.apply([ANCHOR_PX])[0] - np.asarray(anchor))), 2)
    return fit, rep


def _enclosed_px(walls: np.ndarray) -> shapely.Polygon:
    """The area a dashed line encloses, back at the line's centre (px)."""
    poly = tb._enclosed(walls.astype(np.uint8), BRIDGE_PX, INSIDE_PX)
    poly = poly.buffer(-(BRIDGE_PX // 2 + LINE_HALF_PX), join_style="mitre")
    return poly.buffer(-30).buffer(30).simplify(1.5)  # drops labels touching the outside of the line


def site_px() -> shapely.Polygon:
    rgb = figure().astype(int)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    walls = ((np.abs(rgb - SITE_GREY).max(axis=2) <= SITE_TOL) & (sat < SITE_MAX_SAT)).astype(np.uint8)
    # The base map's thin grey street and curb lines share the colour; an opening keeps only the line's
    # 12-px dashes and dots.
    walls = cv2.morphologyEx(walls, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    # Where the black dashed Parcel Boundary runs on the same line (the west end and Girard Road), its dashes
    # alternate with the site line's; together they close it. Black inside the site doesn't matter.
    black = (rgb.max(axis=2) < 40).astype(np.uint8)
    return trace.largest_polygon(_enclosed_px(walls | black))


def site() -> tuple[shapely.Polygon, trace.Similarity, dict]:
    sim, rep = georeference()
    g = tb.clean(sim.geometry(site_px()))
    return g.simplify(0.5, preserve_topology=True), sim, rep


def neighbour_overlaps(site_utm) -> dict:
    out = {}
    for pid in NEIGHBOURS:
        fc = json.loads((config.ROOT / "data" / "boundaries" / f"{pid}.geojson").read_text())
        g = gpd.GeoSeries([shape(f["geometry"]) for f in fc["features"]], crs=4326).to_crs(tb.UTM).union_all()
        out[pid] = {"overlap_m2": round(float(g.intersection(site_utm).area), 1),
                    "distance_m": round(float(g.distance(site_utm)), 1)}
    return out


def main() -> None:
    g, sim, rep = site()
    acres = g.area / tb.ACRE_M2
    over = neighbour_overlaps(g)
    print(f"[{PROJECT}] georeference: {sim.scale:.5f} m/px ({rep['scale_vs_bar_pct']:+.2f}% vs the scale bar), rotation "
          f"{np.degrees(sim.rotation):.2f} deg, coarse r={rep['coarse_correlation']}, ICP trimmed RMS {rep['rms_m']} m, "
          f"median {rep['median_m']} m over {rep['points']} points; anchor off by {rep['anchor_residual_m']} m")
    print(f"[{PROJECT}] project site {acres:.1f} acres (stated about {STATED_SITE_ACRES}); neighbours {over}")
    if abs(rep["scale_vs_bar_pct"]) > 2 or rep["median_m"] > 4:
        raise SystemExit("the georeference is off; check the anchor and the building mask")
    if any(v["overlap_m2"] > 0 for v in over.values()):
        raise SystemExit(f"the site overlaps a mapped project: {over}")
    tb.write(PROJECT, g, {
        "source": (f"traced: {PLAN['title']}, the Project Site line (grey dash-dot); the same plan as the Final EIR/EIS's "
                   "Figure 2-6 (PDF p. 232)"),
        "sourceUrl": PLAN["url"],
        "sourceLabel": "Development guidelines land use plan (PDF)",
        "documents": [PLAN["url"], FEIR["url"], FEIR_DOC, CEQANET],
        "accuracy": "traced",
        "accuracyShort": f"median {rep['median_m']:.0f} m",
        "accuracyNote": (
            f"The Project Site as the project's land use plan draws it (the area to be redeveloped, including the "
            f"realigned Wescoat, Cody and Girard roads along its edges), traced and fitted to OpenStreetMap building "
            f"footprints (median {rep['median_m']:.1f} m, trimmed RMS {rep['rms_m']:.1f} m over the closest "
            f"{int(ICP_KEEP * 100)}% of {rep['points']:,} building-outline points; the fitted scale is within "
            f"{abs(rep['scale_vs_bar_pct']):.1f}% of the plan's scale bar). {acres:.1f} acres as drawn, against the Final "
            f"EIR/EIS's approximately {STATED_SITE_ACRES}; the plan's Parcel Boundary (the leased premises, "
            f"{STATED_PARCEL_ACRES} acres in the EIR) lies inside it and is not drawn. The site is federal land within "
            "NASA Ames Research Center; the county parcel (APN 116-18-012) is the whole NASA property, so no parcel layer "
            "draws it. The 6 acres of off-site utility and demolition work are not drawn."),
        "license": f"Boundary: traced from a public CEQA document (CEQAnet). Georeference: {tb.OSM_LICENSE}.",
        "georeference": rep,
        "statedAcres": STATED_SITE_ACRES,
        "neighbours": over,
    })


if __name__ == "__main__":
    main()
