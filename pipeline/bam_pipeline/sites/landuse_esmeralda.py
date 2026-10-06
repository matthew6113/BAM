"""Esmeralda (Cloverdale): land-use districts from the draft Esmeralda Specific Plan.

Esmeralda is a plan-scale project still in hearings, so the map draws its boundary and
land-use zones only, no buildings (SPEC §7).

Zones
- Source: the City of Cloverdale's draft Esmeralda Specific Plan, Version 7 (Sept 25, 2026,
  posted as "Revised 9/29/26"), Chapter 2, Figure 2-1 "Land Use Districts" (PDF p. 22,
  printed p. 16). It's the newest official land-use map for the site. The Planning
  Commission heard it on Oct 1, 2026 and the City Council takes it up on Oct 7 and 14, 2026,
  so it is not adopted. It would replace the 2009 Alexander Valley Resort Specific Plan,
  which was approved but never built and isn't drawn. No City GIS layer of the SP-2
  districts was found.
- Heights per district are Table 2-2 (PDF p. 26, printed p. 20), all subject to the Airport
  Safety Zones and FAA Part 77 overlays (Figures 2-3 and 2-5), which can lower them.
- The figure mixes vector and raster. The village districts (VMU, VH, VR) and the orange
  publicly accessible circulation (PAC) parcels are vector fills, used exactly. The open space
  districts (OSR, OSC) are a semi-transparent raster over an aerial photo: each pixel is
  labelled with the nearest printed green; hatched overlays, labels and lines inside them
  take the nearest fill's class. The PAC parcels are the plan's streets and paths, not a
  land-use district, so they're left out, as is the SMART rail corridor (outside the parcels).
- VR parcels are split into the two height groups of Table 2-2 (VR-1/VR-2 at 35 ft, VR-3 to
  VR-5 at 25 ft). The parcel names are drawn as outlined text, not searchable, so each VR
  piece is matched to a hand-placed anchor at its printed label (ANCHORS, in PDF points).
- Georeference: the outer edge of the figure's coloured districts (the Plan Area) is fitted
  (similarity, trimmed ICP) to the site boundary in data/boundaries/esmeralda.geojson (County
  of Sonoma parcels named in the staff report). The ICP starts from a coarse search over
  rotations, with no hand-picked control points. The parcels include a ~3.8-acre strip outside
  the city (the "Panhandle") that the figure leaves out; the trimmed fit ignores it.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_esmeralda
"""

from __future__ import annotations

import json
import re

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import MultiLineString, Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "esmeralda"
STAGE = "entitlement"
UTM = tb.UTM
ACRE_M2 = tb.ACRE_M2
DOCS = config.ROOT / "data" / "raw" / "docs"
OUT = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
BOUNDARY = config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson"

PROJECT_PAGE = "https://www.cloverdale.net/esmeralda"
SP = {
    "title": "Draft Esmeralda Specific Plan, Version 7 (City of Cloverdale, Sept 25, 2026; posted as revised 9/29/26)",
    "url": "https://www.cloverdale.net/DocumentCenter/View/7035/Draft-Specific-Plan---Revised-92926",
    "file": "esmeralda-draft-specific-plan-v7.pdf",
    "sha256": "86fd632abb87d0d3d63bb7c0dfa92c14707a72f5174c934b2b8b931953743eae",
}
FIG = {"page_index": 21, "figure": "Figure 2-1, Land Use Districts", "pdf_page": 22, "printed_page": "16"}
TABLE = {"page_index": 25, "table": "Table 2-2", "pdf_page": 26, "printed_page": "20"}
PC_REPORT = "https://www.cloverdale.net/DocumentCenter/View/6998/Agenda-Report"
SONOMA_PARCELS = "https://socogis.sonomacounty.ca.gov/map/rest/services/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0"

DPI = 300
K = DPI / 72  # render pixels per PDF point
RENDER_SHAPE = (3301, 2550, 3)
MAP_FRAME_PT = (36.5, 302.5, 576.0, 721.0)  # x0, top, x1, bottom of the map in PDF points
LEGEND_PT = (36.0, 505.0, 206.0, 722.0)  # legend panel over the map's lower left

# Vector fills (RGB, 0-1) as written in the PDF.
VECTOR = {
    "vh": (0.757, 0.655, 0.784),
    "vr": (0.98, 1.0, 0.6),
    "vmu": (0.529, 0.761, 0.949),
    "pac": (0.847, 0.588, 0.255),
}
# Raster greens as rendered (they're semi-transparent over the aerial photo).
GREENS = {
    "osc": (105, 185, 97),
    "osr": (196, 225, 185),
    "osr_amph": (199, 219, 157),  # OSR-3 under the Amphitheater Overlay's tint
    "osc_rpz": (70, 186, 174),  # the Airport Runway Protection Overlay's teal hatch over OSC-8
    "osc_rpz_edge": (88, 186, 136),  # its anti-aliased edges
}
GREEN_CLASS = {"osc": "osc", "osr": "osr", "osr_amph": "osr", "osc_rpz": "osc", "osc_rpz_edge": "osc"}
GREEN_MAX_DIST = 28
GREENNESS_MIN = 18  # G minus the mean of R and B: the light OSR green is close to the photo's pale greys
GAP_MAX_PX = 6000  # unlabelled specks (text, lines) up to ~0.5 ha take the nearest fill
GAP_MAX_LIGHT = 190  # larger gaps too, if they're hatched (mean darkest channel below this)

# Hand-placed anchors at the printed VR parcel labels (PDF points, y down).
ANCHORS = {
    "VR-1A": (373.0, 617.4), "VR-1B": (353.5, 645.4), "VR-1C": (374.8, 651.8),
    "VR-2A": (423.9, 605.7), "VR-2B": (436.8, 639.0),
    "VR-3A": (455.8, 570.0), "VR-3B": (471.3, 587.5), "VR-4": (481.2, 541.7),
    "VR-5A": (255.5, 425.9), "VR-5B": (257.0, 443.4),
}
MIN_GREEN_M2 = 1200  # drops the pale Entry Circle island (~970 m2); the smallest OSC piece is ~1,700 m2
ICP_KEEP = 0.8
ROTATIONS = range(0, 360, 10)

TABLE_NOTE = "Table 2-2, p. 20"
DISTRICTS = {
    "vmu": {
        "label": "Village mixed use (VMU)", "category": "mixed-use",
        "note": "Retail, restaurants, hotel, offices, maker space, childcare and all housing types around the Entry "
                "Circle; up to 35 ft, net FAR 2.5, 10-30 homes per acre (senior housing 60) (Table 2-1, p. 18; "
                f"{TABLE_NOTE}).",
    },
    "vh": {
        "label": "Village hospitality (VH)", "category": "commercial",
        "note": "The resort hotel with its spa, event and conference space, dining and shared parking, plus homes and "
                "the Piazza; up to 50 ft for the hotel and other non-residential uses, 35 ft for homes; net FAR 0.3, "
                f"5 homes per acre (Table 2-1, p. 18; {TABLE_NOTE}). Mapped to commercial: hotel-led. Part of it is "
                "in the Restricted Use Overlay (no homes, schools or day care without further cleanup) and the "
                "airport's safety zones.",
    },
    "vr12": {
        "label": "Village residential (VR-1, VR-2)", "category": "residential",
        "note": "Detached and attached homes, senior housing and small neighborhood uses; up to 35 ft, net FAR 1.0, "
                f"4-20 homes per acre (Table 2-1, p. 18; {TABLE_NOTE}).",
    },
    "vr35": {
        "label": "Village residential (VR-3 to VR-5)", "category": "residential",
        "note": "Detached and attached homes, senior housing and small neighborhood uses; up to 25 ft, net FAR 0.75, "
                f"4-15 homes per acre (Table 2-1, p. 18; {TABLE_NOTE}). VR-5A and VR-5B, east of the rail line, are "
                "an optional housing area.",
    },
    "osr": {
        "label": "Open space recreation (OSR)", "category": "open-space",
        "note": "Sports fields, playgrounds, picnic areas, gardens, farming and trails, including the 4.75-acre public "
                "sports park (OSR-1); an amphitheater only with a use permit; structures up to 15 ft (Table 2-1, "
                f"p. 18; {TABLE_NOTE}).",
    },
    "osc": {
        "label": "Open space conservation (OSC)", "category": "open-space",
        "note": "Habitat protection and restoration along the Russian River and in the groves, with trails and small "
                "utility structures; up to 15 ft, tree houses in the Hilltop Overlay up to 20 ft (Table 2-1, p. 18; "
                f"{TABLE_NOTE}). The plan puts the district at 123 acres (Table 2-2 note; Figure 2-2 on p. 21 "
                "says 93.4).",
    },
}
HEIGHT_CAVEAT = "Heights are subject to the Airport Safety Zones and FAA Part 77 overlays, which can lower them."
DRAFT = "Draft specific plan land use, not yet adopted."


# ---------------------------------------------------------------- documents

def _check(pdf_path) -> None:
    with pdfplumber.open(pdf_path) as pdf:
        fig = " ".join((pdf.pages[FIG["page_index"]].extract_text() or "").split())
        table = " ".join((pdf.pages[TABLE["page_index"]].extract_text() or "").split())
    if "Figure 2-1: Land Use Districts" not in fig:
        raise SystemExit("Specific Plan has changed: Figure 2-1 is not on PDF p. 22")
    for s in ("Table 2-2: Development Standards", "VR-3, & VR- 4-15 0.75 25", "VR-1 & VR-2 4-20 1.0 35",
              "Other Uses: 50", "Open Space Recreation n/a .05 15"):
        if s not in table:
            raise SystemExit(f"Specific Plan has changed: {s!r} not on PDF p. 26")


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    rgb = np.asarray(page.render(scale=K).to_pil().convert("RGB"))
    if rgb.shape != RENDER_SHAPE:
        raise SystemExit(f"unexpected Figure 2-1 render size {rgb.shape}")
    return rgb


def _frame_mask(shape) -> np.ndarray:
    m = np.zeros(shape[:2], bool)
    x0, y0, x1, y1 = (round(v * K) for v in MAP_FRAME_PT)
    m[y0:y1, x0:x1] = True
    lx0, ly0, lx1, ly1 = (round(v * K) for v in LEGEND_PT)
    m[ly0:ly1, lx0:lx1] = False
    return m


def _vector_fills(pdf_path, frame: Polygon) -> dict[str, shapely.Geometry]:
    """Union of each vector fill colour inside the map frame, in render pixels."""
    out = {}
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[FIG["page_index"]]
        for key, rgb in VECTOR.items():
            polys = trace.pdf_filled_polygons(page, rgb, tol=0.005)
            # Fills are drawn as many thin strips with hairline gaps; a 0.3 pt close joins them.
            g = shapely.union_all([shapely.make_valid(p).buffer(0.3, join_style="mitre") for p in polys])
            g = g.buffer(-0.3, join_style="mitre").intersection(frame)
            out[key] = shapely.affinity.scale(g, K, K, origin=(0, 0))
    return out


def _fill_mask(shape, g) -> np.ndarray:
    m = np.zeros(shape[:2], np.uint8)
    for p in getattr(g, "geoms", [g]):
        if not isinstance(p, Polygon) or p.is_empty:
            continue
        cv2.fillPoly(m, [np.round(np.asarray(p.exterior.coords)[:, :2]).astype(np.int32)], 1)
        for h in p.interiors:
            cv2.fillPoly(m, [np.round(np.asarray(h.coords)[:, :2]).astype(np.int32)], 0)
    return m.astype(bool)


# ---------------------------------------------------------------- georeference

def _green_dist(rgb: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """Distance to each printed green; pixels that aren't green enough get infinity."""
    keys = list(GREENS)
    cols = np.array([GREENS[k] for k in keys], float)
    d = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None], axis=3)
    f = rgb.astype(float)
    d[f[..., 1] - (f[..., 0] + f[..., 2]) / 2 < GREENNESS_MIN] = np.inf
    return d, keys


def _plan_area_px(rgb: np.ndarray, village: np.ndarray, frame: np.ndarray) -> np.ndarray:
    """The figure's coloured Plan Area: district fills, holes and text filled in."""
    dist, _ = _green_dist(rgb)
    m = ((dist.min(axis=2) <= GREEN_MAX_DIST) | village) & frame
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, comp, stats, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 20000:
            keep[comp == i] = 1
    contours, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filled = np.zeros_like(keep)
    cv2.drawContours(filled, contours, -1, 1, thickness=cv2.FILLED)
    return filled.astype(bool)


def georeference(area: np.ndarray, site) -> tuple[trace.Similarity, dict]:
    contours, _ = cv2.findContours(area.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    pts = np.vstack([c.reshape(-1, 2) for c in contours]).astype(float)[::2]
    outline = MultiLineString([p.exterior for p in getattr(site, "geoms", [site])])
    groups = np.zeros(len(pts), int)

    # Coarse seed: centroids matched, scale from the areas, rotation searched.
    ys, xs = np.nonzero(area)
    c_px = np.array([xs.mean(), ys.mean()])
    scale = float(np.sqrt(site.area / area.sum()))
    c_m = np.array([site.centroid.x, site.centroid.y])
    best = None
    for deg in ROTATIONS:
        rot = np.radians(deg)
        R = scale * np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
        t = c_m - R @ (c_px * [1, -1])
        init = trace.Similarity(scale, rot, float(t[0]), float(t[1]))
        sim, d = tb.icp(pts, [outline], groups, init, keep=ICP_KEEP, iterations=40)
        score = float(np.quantile(d, ICP_KEEP))
        if best is None or score < best[0]:
            best = (score, sim, d)
    _, sim, d = best
    rep = tb.icp_report(sim, d, ICP_KEEP, "Figure 2-1 Plan Area edge to the site boundary")
    rep["seed"] = f"centroids and areas matched, rotation searched every {ROTATIONS.step} deg (no hand-picked points)"
    rep["target"] = ("data/boundaries/esmeralda.geojson (County of Sonoma parcels named in the Planning Commission "
                     "staff report, Oct 1, 2026)")
    return sim, rep


def _site_mask(shape, sim: trace.Similarity, site, pad_m: float = 3) -> np.ndarray:
    minv = np.linalg.inv(sim.matrix())
    mask = np.zeros(shape[:2], np.uint8)
    for p in getattr(site.buffer(pad_m), "geoms", [site.buffer(pad_m)]):
        xy = (minv @ (np.asarray(p.exterior.coords)[:, :2] - [sim.tx, sim.ty]).T).T
        xy[:, 1] *= -1
        cv2.fillPoly(mask, [np.round(xy).astype(np.int32)], 1)
    return mask.astype(bool)


# ---------------------------------------------------------------- classification

def _nearest_fill(lab: np.ndarray, sel: np.ndarray) -> None:
    src = np.where(lab >= 0, 0, 1).astype(np.uint8)
    _, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.full(near.max() + 1, -1, np.int32)
    zero = src == 0
    lut[near[zero]] = lab[zero]
    lab[sel] = lut[near[sel]]


def classify_greens(rgb: np.ndarray, region: np.ndarray) -> np.ndarray:
    """Open-space pixels: 0 = OSC, 1 = OSR, -1 none."""
    dist, keys = _green_dist(rgb)
    order = ["osc", "osr"]
    cls = np.array([order.index(GREEN_CLASS[k]) for k in keys])
    lab = cls[dist.argmin(axis=2)].astype(np.int32)
    lab[(dist.min(axis=2) > GREEN_MAX_DIST) | ~region] = -1
    # Hatch lines, labels and their halos are cleared with a margin, then take the nearest fill.
    dark = cv2.dilate(((lab < 0) & region).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & region
    lab[dark] = -1
    gaps = ((lab < 0) & region).astype(np.uint8)
    n, comp, stats, _ = cv2.connectedComponentsWithStats(gaps, connectivity=8)
    # Small gaps are filled whatever their colour; larger ones only where they're hatching, not the
    # white SMART corridor strip.
    lightness = np.bincount(comp.ravel(), weights=rgb.min(axis=2).ravel().astype(float), minlength=n)
    fill = np.zeros(n, bool)
    area = stats[1:, cv2.CC_STAT_AREA]
    fill[1:] = (area <= GAP_MAX_PX) | (lightness[1:] / area < GAP_MAX_LIGHT)
    _nearest_fill(lab, fill[comp] & (gaps > 0))
    return lab


def _polys(mask: np.ndarray, min_px: float = 200) -> list[Polygon]:
    m = mask.astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    contours, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    if hier is None:
        return out
    for j, c in enumerate(contours):
        if hier[0][j][3] != -1 or cv2.contourArea(c) < min_px or len(c) < 3:
            continue
        holes = []
        child = hier[0][j][2]
        while child != -1:
            if cv2.contourArea(contours[child]) >= min_px and len(contours[child]) >= 3:
                holes.append(contours[child].reshape(-1, 2))
            child = hier[0][child][0]
        out.append(shapely.make_valid(Polygon(c.reshape(-1, 2), holes)))
    return out


def split_vr(vr_px) -> dict[str, list]:
    """Split the VR fill into its two height groups by the parcel label anchors.

    Each piece takes the group of the nearest anchor; the River Lane and Village Drive fills
    cut some parcels into more than one piece.
    """
    groups: dict[str, list] = {"vr12": [], "vr35": []}
    parts = [p for p in getattr(vr_px, "geoms", [vr_px]) if isinstance(p, Polygon) and p.area > 4 * K * K]
    used = set()
    for p in parts:
        dist = {n: p.distance(Point(x * K, y * K)) for n, (x, y) in ANCHORS.items()}
        names = [n for n, d in dist.items() if d == 0] or [min(dist, key=dist.get)]
        if dist[names[0]] > 40 * K:
            raise SystemExit(f"VR piece at {p.representative_point()} is {dist[names[0]] / K:.0f} pt from any label")
        kinds = {"vr12" if n[3] in "12" else "vr35" for n in names}
        if len(kinds) != 1:
            raise SystemExit(f"VR piece at {p.representative_point()} holds labels of both height groups: {names}")
        groups[kinds.pop()].append(p)
        used.update(names)
    if used != set(ANCHORS):
        raise SystemExit(f"VR labels without a piece: {sorted(set(ANCHORS) - used)}")
    return groups


# ---------------------------------------------------------------- main

def _dumps(obj) -> str:
    text = json.dumps(obj, indent=1)
    return re.sub(r"\[\s*(-?[\d.]+),\s*(-?[\d.]+)\s*\]", r"[\1, \2]", text) + "\n"


def main() -> None:
    urllib_opener()
    sp_path = trace.fetch_document(SP["url"], DOCS / SP["file"], SP["sha256"])
    _check(sp_path)

    site = gpd.read_file(BOUNDARY).to_crs(UTM).union_all()
    rgb = _render(sp_path)
    frame = _frame_mask(rgb.shape)
    x0, y0, x1, y1 = MAP_FRAME_PT
    lx0, ly0, lx1, ly1 = LEGEND_PT
    frame_pt = shapely.box(x0, y0, x1, y1).difference(shapely.box(lx0, ly0, lx1, ly1))
    vec = _vector_fills(sp_path, frame_pt)
    village = _fill_mask(rgb.shape, shapely.union_all(list(vec.values())))

    area = _plan_area_px(rgb, village, frame)
    sim, georef = georeference(area, site)
    print(f"[{PROJECT_ID}] Figure 2-1 fit: RMS {georef['rms_m']} m (median {georef['median_m']} m, "
          f"p90 {georef['p90_m']} m), scale {georef['scale_m_per_unit']} m/px, rotation {georef['rotation_deg']} deg")

    # Only inside the figure's own Plan Area: the parcels' Panhandle strip is photo there, not a district.
    region = frame & area & _site_mask(rgb.shape, sim, site) & ~village
    green = classify_greens(rgb, region)
    zones_px = {"vh": [vec["vh"]], "vmu": [vec["vmu"]], **split_vr(vec["vr"]),
                "osc": _polys(green == 0), "osr": _polys(green == 1)}

    source = f"traced: {SP['title']}, {FIG['figure']}, p. {FIG['printed_page']} (PDF p. {FIG['pdf_page']})"
    features, acres, trimmed = [], {}, {}
    for key, spec in DISTRICTS.items():
        polys = zones_px.get(key) or []
        if not polys:
            raise SystemExit(f"no {spec['label']} traced from Figure 2-1")
        g = shapely.make_valid(sim.geometry(shapely.union_all(polys)))
        inside = g.intersection(site)
        trimmed[key] = 1 - inside.area / g.area
        if trimmed[key] > 0.05:
            raise SystemExit(f"{spec['label']}: {trimmed[key]:.1%} of the traced zone falls outside the site")
        geom = inside.buffer(0.5, join_style="mitre").buffer(-0.5, join_style="mitre").simplify(0.75)
        geom = trace.as_multipolygon(shapely.make_valid(geom))
        # Raster crumbs (e.g. the pale centre of the Entry Circle) are dropped from the greens.
        min_m2 = MIN_GREEN_M2 if key in ("osr", "osc") else 150
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= min_m2]))
        acres[key] = geom.area / ACRE_M2
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "zone",
                "category": spec["category"],
                "label": spec["label"],
                "source": source,
                "note": f"{DRAFT} {spec['note']} {HEIGHT_CAVEAT} About {acres[key]:.1f} acres as drawn.",
                "stage": STAGE,
            },
            "geometry": mapping(tb.to_wgs(geom)),
        })

    for key, spec in DISTRICTS.items():
        print(f"  {spec['label']:<36} {spec['category']:<11} {acres[key]:7.1f} ac  (trimmed {trimmed[key]:.1%})")
    print(f"  total {sum(acres.values()):.1f} of {site.area / ACRE_M2:.1f} site acres; the rest is PAC streets "
          "and paths, the Panhandle strip and edge slivers")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Land-use districts traced from Figure 2-1 of the City of Cloverdale's draft Esmeralda Specific Plan "
                "(Version 7, revised Sept 29, 2026), which the Planning Commission heard on Oct 1, 2026 and the City "
                "Council has not yet adopted. Six zones are drawn: village mixed use and village hospitality around "
                "the entry, village residential split into its two height groups, and open space recreation and "
                "conservation, mostly east of the SMART rail line and along the Russian River. The plan's publicly "
                "accessible circulation parcels (streets and paths) and the SMART corridor aren't zones and are left "
                "out, and the overlays (restricted use, airport, piazza, hilltop, amphitheater) aren't drawn; no "
                "buildings are drawn."
            ),
            "note": "Land-use districts from the draft 2026 specific plan, not yet adopted; zones, not buildings.",
            "sourceUrl": SP["url"],
            "sourceLabel": "Draft specific plan land use, 2026 (PDF)",
            "georeference": {"figure_2_1": georef},
            "license": ("Zone shapes: traced from a public City of Cloverdale planning document. Fitted to County of "
                        "Sonoma parcels (CC BY-SA 3.0, County of Sonoma)."),
            "documents": [PROJECT_PAGE, SP["url"], PC_REPORT, SONOMA_PARCELS],
            "superseded": ("The 2009 Alexander Valley Resort Specific Plan (amended 2016 and 2018), approved for the same "
                           "site but never built, would be replaced; it isn't drawn."),
        },
        "features": features,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(_dumps(tb._round(fc, 6)))
    print(f"[{PROJECT_ID}] wrote {OUT.relative_to(config.ROOT)} ({len(features)} zones, {OUT.stat().st_size // 1024} KB)")


def urllib_opener() -> None:
    import urllib.request

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (bay-area-megaprojects pipeline)")]
    urllib.request.install_opener(opener)


if __name__ == "__main__":
    main()
