"""Mission Point (Santa Clara): illustrative massing from the approved alternative's conceptual site plan.

Which design: Santa Clara approved the Mission Point Project on Nov 19, 2024 (notice of determination, CEQAnet
SCH 2018072068, document 5) as "up to 2,600 housing units approximately; 2,211,000 gsf of office/R&D space",
which is the Draft EIR's Reduced Office/Increased Housing Alternative: "removing all 789,000 gsf of office/R&D
space in Area C and replacing it with 800 multifamily housing units" (Draft EIR p. 5-4; Final EIR p. 1-4). The
Draft EIR's own site plan (Figure 2-3) shows the proposed project with offices in Area C, so it isn't drawn.

Source: Mission Point Project Draft EIR (ICF for the City of Santa Clara, November 2023), Figure 5-3,
"Conceptual Site Plan - Reduced Office/Increased Housing Alternative" (PDF p. 621). Over a raster base plan it
draws each conceptual building as a heavy hand-drawn outline (vector), filled with blue scribble for office and
yellow for residential, and gives each of the four areas a height range with two call-outs whose leader dots
sit on particular buildings:
- Area A (offices, "1,213,000 GSF"): "Max H.138' up to 10 Levels", "Min H.63' up to 5 Levels";
- Area B (offices, "1,100,000 GSF"): "Max H.153' up to 10 Levels", "Min H.108' up to 8 Levels";
- Area C (homes, "800,000 GSF"): "Max H.108' up to 10 Levels", "Min H.72' up to 7 Levels";
- Area D (homes, "1,800,000 GSF"): "Max H.202' up to 20 Levels", "Min H.72' up to 7 Levels".
The figure's notes: "All elevation heights shown are approximate", measured to the highest occupied floor, and
all heights are subject to FAA limits. The Draft EIR's Table 2-3 gives each area's anticipated maximum for the
proposed project (A 123 ft, B 153 ft, C 132 ft, D 202 ft) and Table 5-1 says the alternative's heights are the
same as the project's; Figure 5-3 is the alternative's own drawing and is followed here, with Table 2-3 noted.

How it's drawn:
- Footprints: the faces enclosed by the figure's vector outlines (page coordinates), classified as office or
  residential by the colour of the scribble inside them; faces with no office or residential scribble
  (courtyards, plazas) are left empty. Each face is grown by half the outline's stroke so the footprint runs to
  the line's centre. Lines that split a building (podium and tower parts) split it here too.
- Heights: the building under each "Max" leader dot is drawn at the maximum and every other building in the
  area at the area's minimum. The figure doesn't say how tall the buildings between those are, so this is the
  lower bound of an approximate range: illustrative.
- Georeference: the dash-dot project boundary in the figure's base raster (blue-grey pixels) fitted by trimmed
  ICP to the County parcels that make up the site (data/boundaries/mission-point), starting from the four
  corners. The base raster and the vector outlines share the page's coordinates.
- Stage: entitled (no permit or construction record found). Phase: the area; the Draft EIR's construction
  schedule (Table 2-7, for the proposed project) starts Area C in 2025, D in 2027, B in 2028 and A in 2029 and
  says the order "would occur in response to market demands".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_mission_point
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import shapely
from shapely.geometry import LineString, Point, box, mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "mission-point"
UTM = ob.UTM
DEIR = {
    "title": "Mission Point Project Draft EIR (City of Santa Clara, November 2023)",
    "url": "https://ceqanet.lci.ca.gov/2018072068/4/Attachment/Nn5ZMq",
    "sha256": "33f91f05b6104f288883c59db492bb4d0843d6a2a10cb57f727620937cbda2f2",
    "file": "deir-2023-11.pdf",
}
NOD_URL = "https://ceqanet.lci.ca.gov/2018072068/5"
PAGE = 620  # PDF p. 621, Figure 5-3
IMAGE_SIZE = (3252, 2103)

OUTLINE_GREY = (0.102, 0.102, 0.102)
OUTLINE_WIDTHS = (4.76, 6.09)
OFFICE = ((0.141, 0.584, 0.926), (0.176, 0.608, 0.941))  # blue scribble
RESIDENTIAL = ((0.98, 0.78, 0.063),)  # yellow scribble
SCRIBBLE_HALF = 1.5  # pt: the scribbles are about 15-18 pt wide; this thin core keeps them inside their outlines
MIN_COVER = 0.12  # share of a face the scribble core must cover to count it as a building
MIN_FACE_PT2 = 60

# Initial corners: figure base-raster pixel -> which corner of the parcel boundary
CORNERS_PX = {"NW": (1224, 414), "NE": (2160, 456), "SE": (2314, 1524), "SW": (1056, 1804)}
ICP_KEEP = 0.8

# Area split on the page (pt): Democracy Way's new alignment (y) and the central green (x).
SPLIT_Y = 280.0
SPLIT_X_NORTH, SPLIT_X_SOUTH = 428.0, 400.0
AREAS = {
    "A": {"use": "Office/R&D", "gsf": "1,213,000", "min": 63, "max": 138, "min_lv": 5, "max_lv": 10, "max_dot": (399, 145),
          "table": 123},
    "B": {"use": "Office/R&D", "gsf": "1,100,000", "min": 108, "max": 153, "min_lv": 8, "max_lv": 10, "max_dot": (518, 165),
          "table": 153},
    "C": {"use": "Homes", "gsf": "800,000", "min": 72, "max": 108, "min_lv": 7, "max_lv": 10, "max_dot": (548, 355),
          "table": 132},
    "D": {"use": "Homes", "gsf": "1,800,000", "min": 72, "max": 202, "min_lv": 7, "max_lv": 20, "max_dot": (266, 398),
          "table": 202},
}


def _close(c, ref, tol=0.02) -> bool:
    if not isinstance(c, (tuple, list)) or len(c) != len(ref):
        return False
    return all(abs(a - b) <= tol for a, b in zip(c, ref))


def figure(path) -> tuple[list, dict, np.ndarray, tuple]:
    pdf = pdfplumber.open(path)
    pg = pdf.pages[PAGE]
    text = " ".join(w["text"] for w in pg.extract_words())
    for want in ("Figure 5-3", "Reduced Office/Increased Housing Alternative", "RESIDENTIAL: 2,600 DU"):
        if want not in text:
            raise SystemExit(f"PDF page {PAGE + 1} does not hold {want!r}")
    outlines, scribble = [], {"office": [], "residential": []}
    for o in pg.objects.get("curve", []):
        pts = [(float(x), float(y)) for x, y in o["pts"]]
        if len(pts) < 2:
            continue
        sc, lw = o.get("stroking_color"), round(o.get("linewidth") or 0, 2)
        if _close(sc, OUTLINE_GREY, 0.003) and lw in OUTLINE_WIDTHS:
            outlines.append((LineString(pts), lw))
        elif any(_close(sc, c) for c in OFFICE) and lw > 10:
            scribble["office"].append(LineString(pts))
        elif any(_close(sc, c) for c in RESIDENTIAL) and lw > 10:
            scribble["residential"].append(LineString(pts))
    im = pg.images[0]
    placement = (float(im["x0"]), float(im["top"]), float(im["x1"]), float(im["bottom"]))
    doc = pdfium.PdfDocument(str(path))
    rgb = None
    for obj in doc[PAGE].get_objects():
        if obj.type == pdfium_c.FPDF_PAGEOBJ_IMAGE:
            pil = obj.get_bitmap(render=False).to_pil().convert("RGB")
            if pil.size == IMAGE_SIZE:
                rgb = np.asarray(pil).astype(int)
    if rgb is None:
        raise SystemExit(f"PDF page {PAGE + 1} has no {IMAGE_SIZE} base image")
    return outlines, scribble, rgb, placement


def px_to_pt(px, placement) -> np.ndarray:
    x0, top, x1, bottom = placement
    a = np.asarray(px, float).reshape(-1, 2)
    return np.column_stack([x0 + a[:, 0] * (x1 - x0) / IMAGE_SIZE[0], top + a[:, 1] * (bottom - top) / IMAGE_SIZE[1]])


def georeference(rgb, placement, site) -> trace.Similarity:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    ys, xs = np.nonzero((b - r >= 12) & (r < 150) & (g < 150))  # the dash-dot project boundary
    pts = px_to_pt(np.column_stack([xs, ys]), placement)
    xy = np.asarray(site.exterior.coords)[:-1]
    corners = {"NW": xy[np.argmax(xy[:, 1] - xy[:, 0])], "NE": xy[np.argmax(xy[:, 1] + xy[:, 0])],
               "SE": xy[np.argmax(xy[:, 0] - xy[:, 1])], "SW": xy[np.argmin(xy[:, 1] + xy[:, 0])]}
    init = trace.fit_similarity(px_to_pt(list(CORNERS_PX.values()), placement), [corners[k] for k in CORNERS_PX],
                                list(CORNERS_PX))
    sim = trace.icp_similarity(pts, LineString(site.exterior.coords), init, keep=ICP_KEEP)
    sim.corner_init = init  # type: ignore[attr-defined]
    return sim


def faces(outlines) -> list:
    """Regions enclosed by the outline strokes (page pt), and the stroke half-width to grow them by."""
    strokes = shapely.union_all([ls.buffer(lw / 2, cap_style="round") for ls, lw in outlines])
    frame = box(*strokes.bounds).buffer(20)
    out = []
    for f in shapely.get_parts(frame.difference(strokes)):
        if f.area < MIN_FACE_PT2 or f.touches(frame.exterior) or f.intersects(frame.exterior):
            continue
        out.append(f)
    return out


def area_of(c: Point) -> str:
    if c.y < SPLIT_Y:
        return "A" if c.x < SPLIT_X_NORTH else "B"
    return "D" if c.x < SPLIT_X_SOUTH else "C"


def main() -> None:
    path = trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "official" / PROJECT_ID / DEIR["file"],
                                DEIR["sha256"])
    outlines, scribble, rgb, placement = figure(path)
    fc_site = json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
    site = gpd.GeoSeries([shapely.geometry.shape(fc_site["features"][0]["geometry"])], crs=4326).to_crs(UTM).iloc[0]
    if site.geom_type != "Polygon":
        site = max(site.geoms, key=lambda p: p.area)
    sim = georeference(rgb, placement, site)
    print(f"[mission-point] georeference: {sim.scale:.3f} m/pt, rotation {np.degrees(sim.rotation):.2f} deg, "
          f"ICP RMS {sim.rms_m:.1f} m ({sim.labels[0]}); corner start RMS {sim.corner_init.rms_m:.1f} m")

    cores = {k: shapely.union_all([ls.buffer(SCRIBBLE_HALF) for ls in v]) for k, v in scribble.items()}
    half = max(lw for _, lw in outlines) / 2
    buildings = []
    for f in faces(outlines):
        cover = {k: f.intersection(c).area / f.area for k, c in cores.items()}
        kind = max(cover, key=cover.get)
        if cover[kind] < MIN_COVER:
            continue
        geom = f.buffer(half, join_style="mitre")
        buildings.append({"face": f, "geom": geom, "kind": kind, "area": area_of(f.representative_point())})
    # The building under each area's "Max" leader dot (nearest face in that area).
    for a, spec in AREAS.items():
        dot = Point(spec["max_dot"])
        cands = [b for b in buildings if b["area"] == a]
        if not cands:
            raise SystemExit(f"mission-point: no buildings found in Area {a}")
        min(cands, key=lambda b: b["face"].distance(dot))["max"] = True
        uses = {b["kind"] for b in cands}
        want = "office" if spec["use"].startswith("Office") else "residential"
        if uses != {want}:
            print(f"[mission-point] note: Area {a} faces classified {sorted(uses)}; expected {want}")

    features = []
    counts = {}
    for b in sorted(buildings, key=lambda b: (b["area"], -b["geom"].centroid.y, b["geom"].centroid.x)):
        a, spec = b["area"], AREAS[b["area"]]
        counts[a] = counts.get(a, 0) + 1
        top = bool(b.get("max"))
        h = spec["max"] if top else spec["min"]
        utm = sim.geometry(b["geom"])
        utm = utm.intersection(site.buffer(5))
        if utm.is_empty:
            continue
        wgs = gpd.GeoSeries([utm.simplify(0.5)], crs=UTM).to_crs(4326).iloc[0]
        use = ("Office/R&D (Area A and B: about 2.2 million gsf of office/R&D in all)" if b["kind"] == "office"
               else "Homes (2,600 in Areas C and D)")
        note = (f"Figure 5-3 gives Area {a} {spec['min']} to {spec['max']} ft ({spec['min_lv']} to {spec['max_lv']} "
                f"levels), \"approximate\", subject to FAA limits; {'its Max leader points at this building' if top else 'drawn at the minimum: the figure gives no height for the buildings between'}. "
                f"Draft EIR Table 2-3 gives the area's anticipated maximum as {spec['table']} ft (proposed project).")
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": f"Area {a} building {counts[a]}", "stage": "entitled", "height_ft": h,
                "podium_ft": None, "base_ft": 0, "use": use, "phase": f"Area {a}", "illustrative": True,
                "source": (f"illustrative: outline traced from Draft EIR Figure 5-3 (Reduced Office/Increased Housing "
                           f"Alternative, PDF p. {PAGE + 1}); {h} ft is the figure's {'maximum' if top else 'minimum'} "
                           f"height for Area {a}"),
                "note": note,
            },
            "geometry": mapping(wgs),
        })
    for a in AREAS:
        bs = [b for b in buildings if b["area"] == a]
        fp = sum(sim.geometry(b["geom"]).area for b in bs) * 10.7639
        print(f"[mission-point] Area {a}: {len(bs)} footprints, {fp:,.0f} sq ft of footprint "
              f"({AREAS[a]['gsf']} gsf in the figure)")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing from the conceptual site plan of the approved alternative (Draft EIR "
                        "Figure 5-3): offices in Areas A and B north of the realigned Democracy Way, homes in Areas C "
                        "and D to the south. The figure gives each area an approximate height range; the building its "
                        "maximum points at is drawn at that height (138, 153, 108 and 202 ft) and the others at the "
                        "area's minimum (63, 108, 72 and 72 ft). Buildings will be designed later."),
            "note": "Conceptual footprints and approximate heights, not building designs.",
            "sourceUrl": DEIR["url"],
            "sourceLabel": "Mission Point Project Draft EIR, 2023 (PDF), Figure 5-3",
            "approvalSourceUrl": NOD_URL,
            "georeference": {
                "method": ("Figure 5-3's dash-dot project boundary (base raster) fitted by trimmed ICP to the County "
                           "parcels of the site, from the four corners; the vector outlines share the page's coordinates."),
                **sim.report(),
                "corner_start": sim.corner_init.report(),
            },
            "license": ("Footprints and heights: from a public City of Santa Clara document. Site: Santa Clara County "
                        "open data (terms of use)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[mission-point] wrote {out.relative_to(config.ROOT)} ({len(features)} features, {out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
