"""Middlefield Park (Google, Mountain View): development envelopes at the master plan's maximum heights.

Source:
- Middlefield Park Master Plan, October 2022 (Attachment 8 to the City Council report of Nov 15,
  2022). Council Resolution 18734 approved the master plan that night; its conditions of approval
  (Exhibit A, item 1.a) name the "Middlefield Park Master Plan ... dated October 2022" as the
  approved plans.
- Chapter 8, Buildings:
  - Table 8.3.2 "Building heights summary" (PDF p. 130) gives each building location's "Total
    proposed height maximums (with height bonuses; not to exceed CLUP limit)": R1 and R2 123 ft,
    O1 125 ft, O2-O4 and R3-R6 95 ft, O5/P1 and P2 60 ft.
  - Figure 8.3.1 "Maximum building height" (PDF p. 129) colours each location by its maximum
    height on a plan of the site.
  - Figure 8.3.5 "Setback standards applied to the Master Plan" (PDF p. 132) draws the same plan
    at three times the resolution, with each location's building line (the envelope inside the
    required setbacks) as a thin black outline. The footprints are traced from it.
- Phases: Development Agreement Exhibit D, Table D1 (ordinance attached to the Dec 13, 2022
  second-reading report).

What this is and isn't:
- Each location is drawn as its whole buildable envelope (Fig. 8.3.5), extruded to its maximum
  height (Table 8.3.2). The Council report says "each location represents a buildable area, not a
  single building design", and the master plan calls its building form illustrative, so every
  feature is labelled illustrative. Real buildings will be smaller and step down (seven to 11
  stories residential, four to nine office, per the Council report), with 55-75 ft average street
  walls; those are noted, not drawn.
- O1 is 125 ft in Table 8.3.2 but 115 ft in Figure 8.3.1 of the same document. The table, which
  states the maximums and matches the April 2022 Draft SEIR (Table 3.2-1, 125 ft), is drawn; the
  figure's value is in the feature's note. For O5/P1 and P2 the master plan (60 ft) is newer than
  the Draft SEIR (65 ft), so 60 ft is drawn and 65 ft noted.
- R4A and R6 are the 2.4 acres Google dedicates to the City for affordable housing; they're drawn
  at the master plan's 95-ft maximum like the other locations, with a note.
- Parks (Maude Park, Ellis Park, Gateway Park, Bridge Open Space), streets and paseos are not drawn.
  Nothing new has been built (no permit record found): the 23 existing office and R&D buildings
  stay in the base map until they are demolished.

Georeferencing: the figure is an embedded raster (1764 x 1720 px) over a base map of curb lines
and existing buildings. A similarity fit on four street-centreline intersections (midway between
the curb lines) matched to OpenStreetMap starts a trimmed ICP that fits the outlines of the base
map's off-site buildings to OpenStreetMap building footprints (both via Overture); the base map
carries no scale bar, and the buildings pin it far better than the intersections of these wide,
divided roads. The intersections' residuals after the fit are recorded as a check, as is the
distance from the figure's dash-dot master plan boundary to the City of Mountain View parcels that
make up the site (data/boundaries/middlefield-park); the traced envelopes are tested against the
parcels.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_middlefield_park
"""

from __future__ import annotations

import json
import re

import cv2
import geopandas as gpd
import numpy as np
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "middlefield-park"
UTM = tb.UTM

MASTER_PLAN = {
    "title": "Middlefield Park Master Plan (October 2022), approved by Resolution 18734 on Nov 15, 2022",
    "url": "https://mountainview.legistar.com/gateway.aspx?M=F&ID=e1878a1f-8e37-45c4-84e4-04e0da99f46d.pdf",
    "sha256": "3ca2d0df1a8e7eed59f240b07659ba0a40325cc452d070b2dd9e6ed411e29560",
    "file": "mfp-master-plan-2022-10.pdf",
}
RESOLUTION = {
    "title": "Resolution 18734 approving the master plan, Exhibit A condition 1.a (plans dated October 2022)",
    "url": "https://mountainview.legistar.com/gateway.aspx?M=F&ID=a324c82e-f151-47f1-8a60-15ecb6cd21ee.pdf",
}
DA_PHASING = {
    "title": "Development Agreement, Exhibit D, Table D1 phasing plan (ordinance attached to the Dec 13, 2022 report)",
    "url": "https://mountainview.legistar.com/gateway.aspx?M=F&ID=f7269f0d-5ad4-4b0b-b069-0910174adc7c.pdf",
}
TABLE_PAGE = 129  # PDF p. 130, Table 8.3.2
HEIGHT_FIG_PAGE = 128  # PDF p. 129, Figure 8.3.1
SETBACK_FIG_PAGE = 131  # PDF p. 132, Figure 8.3.5
SETBACK_SIZE = (1764, 1720)  # the embedded raster's width, height
HEIGHT_SIZE = (588, 576)

# Street centrelines in the Figure 8.3.5 raster (pixels), each midway between the curb lines.
CONTROLS = {
    ("Ellis Street", "East Middlefield Road"): (89, 1500),
    ("Logue Avenue", "Maude Avenue"): (752, 850),
    ("Clyde Avenue", "Maude Avenue"): (1425, 1178),
    ("Tasman - Mountain View", "East Middlefield Road"): (452, 1631),  # VTA light rail crossing
}
STREETS_BBOX = (-122.060, 37.388, -122.038, 37.405)

# Figure 8.3.1 legend swatches, sampled from the page rendered at 100 dpi: (x, y) -> height ft.
LEGEND_PX = {(1226, 897): 60, (1226, 918): 95, (1226, 938): 115, (1226, 958): 123}

# Each location: a seed pixel inside its Fig. 8.3.5 outline (clear of the label), its Table 8.3.2
# row, label, use, phase (DA Table D1) and the Table 8.3.2 maximum height.
LOCATIONS = [
    # id, seed, table row, label, use, phase, height
    ("R1", (200, 1300), "R1", "Residential R1", "residential with ground-floor active uses", "Phase 1", 123),
    ("R2", (250, 1050), "R2", "Residential R2", "residential with ground-floor active uses", "Phase 1", 123),
    ("R4A", (1050, 860), "R4a/R4b", "Affordable housing site R4A", "affordable housing (land dedicated to the City)", "Phase 1", 95),
    ("R6", (1320, 1300), "R6", "Affordable housing site R6", "affordable housing (land dedicated to the City)", "Phase 1", 95),
    ("O1", (250, 700), "O1", "Office O1", "office", "Phase 2", 125),
    ("O2", (620, 470), "O2", "Office O2", "office", "Phase 2", 95),
    ("R3", (880, 700), "R3", "Residential R3", "residential with ground-floor active uses", "Phase 3", 95),
    ("R4B", (1060, 762), "R4a/R4b", "Residential R4B", "residential with ground-floor active uses", "Phase 3", 95),
    ("R5", (1350, 880), "R5", "Residential R5", "residential with ground-floor active uses", "Phase 3", 95),
    ("O3", (900, 300), "O3", "Office O3", "office", "Phase 4", 95),
    ("O4", (1200, 300), "O4", "Office O4", "office", "Phase 4", 95),
    ("O5", (1430, 420), "O5/P1", "Office O5", "office", "Phase 4", 60),
    ("P1", (1580, 420), "O5/P1", "Parking garage P1", "parking", "Phase 4", 60),
    ("P2", (1560, 700), "P2", "Parking garage P2", "parking with ground-floor active uses", "Phase 4", 60),
]
# Units and floor area by location (master plan Tables 5.3.1 and 5.3.4), for the notes.
PROGRAM = {
    "R1": "about 400 homes", "R2": "about 450 homes", "R3": "about 270 homes", "R4A": "about 210 homes",
    "R4B": "about 90 homes", "R5": "about 310 homes", "R6": "about 170 homes",
    "O1": "441,939 sq ft of office", "O2": "190,000 sq ft of office", "O3": "310,000 sq ft of office",
    "O4": "292,212 sq ft of office", "O5": "82,849 sq ft of office",
}
DARK_MAX = 90  # the building lines and labels: every channel below this
CLOSE_PX = 11  # closes notches where label strokes touch a building line
LINE_HALF_PX = 2  # the building lines are about 4-5 px wide; grow to their centre
BOUNDARY_GREY = (118, 118, 118)  # the dash-dot master plan boundary
BUILDING_GREY = (236, 236, 238)  # existing buildings in the base map
MIN_BUILDING_PX = 1500
ICP_KEEP = 0.7


# ---------------------------------------------------------------- documents

def fetch() -> pdfium.PdfDocument:
    path = trace.fetch_document(MASTER_PLAN["url"], tb.DOCS / MASTER_PLAN["file"], MASTER_PLAN["sha256"])
    return pdfium.PdfDocument(str(path))


def page_text(doc, i: int) -> str:
    return " ".join(doc[i].get_textpage().get_text_range().split())


def check_pages(doc) -> None:
    for i, want in ((HEIGHT_FIG_PAGE, "Figure 8.3.1 Maximum building height"),
                    (SETBACK_FIG_PAGE, "Figure 8.3.5 Setback standards applied to the Master Plan"),
                    (TABLE_PAGE, "Table 8.3.2 Building heights summary")):
        if want not in page_text(doc, i):
            raise SystemExit(f"PDF page {i + 1} does not hold {want!r}")


def table_heights(doc) -> dict[str, int]:
    """Total proposed height maximums from Table 8.3.2: the last height in each row."""
    flat = page_text(doc, TABLE_PAGE)
    starts = [(m.start(), m.group(1)) for m in re.finditer(r"(R\d|R4a/R4b|O\d|O5/P1|P2)\d? 182 ft", flat)]
    end = flat.index("1 High-rise core")
    out = {}
    for i, (pos, row) in enumerate(starts):
        seg = flat[pos: starts[i + 1][0] if i + 1 < len(starts) else end]
        out[row] = int(re.findall(r"(\d+) ft", seg)[-1])
    missing = {spec[2] for spec in LOCATIONS} - set(out)
    if missing:
        raise SystemExit(f"Table 8.3.2 has no row for {sorted(missing)}")
    return out


def embedded_image(doc, i: int, size: tuple[int, int]) -> np.ndarray:
    for obj in doc[i].get_objects():
        if obj.type == pdfium_c.FPDF_PAGEOBJ_IMAGE:
            im = obj.get_bitmap(render=False).to_pil().convert("RGB")
            if im.size == size:
                return np.asarray(im)
    raise SystemExit(f"PDF page {i + 1} has no {size[0]} x {size[1]} image")


def legend_colours(doc) -> dict[int, np.ndarray]:
    rgb = np.asarray(doc[HEIGHT_FIG_PAGE].render(scale=100 / 72).to_pil().convert("RGB")).astype(int)
    return {h: rgb[y, x] for (x, y), h in LEGEND_PX.items()}


# ---------------------------------------------------------------- georeference and trace

def intersections(streets: gpd.GeoDataFrame) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), px in CONTROLS.items():
        src.append(px)
        dst.append(tb.intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def building_points(rgb: np.ndarray) -> np.ndarray:
    """Outline pixels of the light grey existing buildings in the figure's base map (off the site)."""
    mask = (np.abs(rgb.astype(int) - BUILDING_GREY).max(axis=2) <= 3).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
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


def georeference(rgb: np.ndarray, streets: gpd.GeoDataFrame, buildings: gpd.GeoDataFrame):
    """Fit the figure's base-map buildings to OpenStreetMap footprints, starting from the intersections."""
    init = intersections(streets)
    pts = building_points(rgb)
    moved = init.apply(pts)
    near = buildings[buildings.intersects(shapely.box(*(moved.min(0) - 50), *(moved.max(0) + 50)))]
    target = shapely.union_all(near.geometry.boundary.to_numpy())
    sim, d = tb.icp(pts, [target], np.zeros(len(pts), int), init, keep=ICP_KEEP)
    rep = tb.icp_report(sim, d, ICP_KEEP, "base-map building outlines")
    rep["method"] = ("trimmed ICP of the figure's base-map building outlines onto OpenStreetMap building "
                     "footprints (via Overture), started from a fit on four street intersections")
    check = [{"label": label, "residual_m": round(float(np.linalg.norm(sim.apply([px])[0] - dst)), 2)}
             for label, px, dst in zip(init.labels, CONTROLS.values(),
                                       (tb.intersection(streets, a, b) for a, b in CONTROLS))]
    return sim, rep, check, init


def trace_location(dark: np.ndarray, seed: tuple[int, int]) -> np.ndarray:
    """The envelope inside one building line: flood fill from the seed, labels filled, line centred."""
    if dark[seed[1], seed[0]]:
        raise SystemExit(f"seed {seed} sits on a line or label")
    img = dark.copy()
    cv2.floodFill(img, np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8), seed, 2)
    reg = (img == 2).astype(np.uint8)
    if reg.sum() > 100_000:
        raise SystemExit(f"the fill from {seed} leaked out of its building line")
    reg = cv2.morphologyEx(reg, cv2.MORPH_CLOSE, np.ones((CLOSE_PX, CLOSE_PX), np.uint8))
    cs, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filled = np.zeros_like(reg)
    cv2.drawContours(filled, cs, -1, 1, cv2.FILLED)
    return cv2.dilate(filled, np.ones((2 * LINE_HALF_PX + 1,) * 2, np.uint8))


def mask_polygon(mask: np.ndarray) -> Polygon:
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    return shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5))


def figure_height(mask: np.ndarray, fig: np.ndarray, legend: dict[int, np.ndarray]) -> int:
    """The Figure 8.3.1 height class under a location (that figure is the same plan at 1/3 scale)."""
    h = SETBACK_SIZE[1] * HEIGHT_SIZE[0] // SETBACK_SIZE[0]
    small = np.zeros(fig.shape[:2], np.uint8)
    small[:h] = cv2.resize(mask, (HEIGHT_SIZE[0], h), interpolation=cv2.INTER_NEAREST)
    small = cv2.erode(small, np.ones((7, 7), np.uint8))
    px = fig[small > 0].astype(int)
    col = np.median(px, axis=0)
    return min(legend, key=lambda h: np.abs(legend[h] - col).sum())


def boundary_check(rgb: np.ndarray, sim: trace.Similarity, site_utm) -> dict:
    grey = (np.abs(rgb.astype(int) - BOUNDARY_GREY).max(axis=2) <= 22)
    ys, xs = np.nonzero(grey)
    pts = sim.apply(np.c_[xs, ys] + 0.5)
    d = shapely.distance(shapely.points(pts), site_utm.boundary)
    near = d[d < 30]  # the grey also draws a few labels and cul-de-sac curbs away from the boundary
    return {"what": "Fig. 8.3.5 dash-dot master plan boundary pixels within 30 m of the City parcels' outline",
            "pixels": int(len(near)), "median_m": round(float(np.median(near)), 2),
            "p90_m": round(float(np.quantile(near, 0.9)), 2)}


# ---------------------------------------------------------------- main

def main() -> None:
    doc = fetch()
    check_pages(doc)
    table = table_heights(doc)
    print(f"[{PROJECT_ID}] Table 8.3.2 maximums: {table}")
    setback = embedded_image(doc, SETBACK_FIG_PAGE, SETBACK_SIZE)
    heights_fig = embedded_image(doc, HEIGHT_FIG_PAGE, HEIGHT_SIZE)
    legend = legend_colours(doc)

    streets = tb.streets("mfp-middlefield-park", STREETS_BBOX)
    buildings = tb.buildings("mfp-middlefield-park", STREETS_BBOX)
    sim, georef, xcheck, init = georeference(setback, streets, buildings)
    print(f"[{PROJECT_ID}] intersections alone: RMS {init.rms_m:.2f} m")
    print(f"[{PROJECT_ID}] Fig. 8.3.5 georeference: trimmed RMS {georef['rms_m']} m (median {georef['median_m']} m, "
          f"p90 {georef['p90_m']} m) over {georef['points']} outline points, {sim.scale:.4f} m/px, "
          f"rotation {np.degrees(sim.rotation):.2f} deg")
    print(f"[{PROJECT_ID}] intersection check: " + ", ".join(f"{c['label']} {c['residual_m']} m" for c in xcheck))
    if georef["rms_m"] > 1.5 or max(c["residual_m"] for c in xcheck) > 10:
        raise SystemExit("the georeference is off; check the controls")

    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]
    bcheck = boundary_check(setback, sim, site_utm)
    print(f"[{PROJECT_ID}] figure boundary vs parcels: median {bcheck['median_m']} m, p90 {bcheck['p90_m']} m")

    dark = (setback.max(axis=2) < DARK_MAX).astype(np.uint8)
    fig_ref = "Middlefield Park Master Plan (Oct 2022)"
    features, total, outside, fig_heights = [], 0.0, 0.0, {}
    for loc, seed, row, label, use, phase, h in LOCATIONS:
        if table[row] != h:
            raise SystemExit(f"Table 8.3.2 gives {row} {table[row]} ft, not {h}")
        mask = trace_location(dark, seed)
        fh = figure_height(mask, heights_fig, legend)
        fig_heights[loc] = fh
        g = trace.as_multipolygon(shapely.make_valid(sim.geometry(mask_polygon(mask)).simplify(0.4)))
        total += g.area
        off = g.difference(site_utm).area
        outside += off
        print(f"[{PROJECT_ID}]   {label:>28}: {h:3d} ft (Fig. 8.3.1: {fh}), {g.area:7.0f} m2, {off:5.0f} m2 off the parcels")
        notes = []
        if loc == "O1":
            if fh != 115:
                raise SystemExit(f"Figure 8.3.1 now reads {fh} ft for O1; recheck the note")
            notes.append("Figure 8.3.1 of the same master plan shows 115 ft; its Table 8.3.2 and the April 2022 "
                         "Draft SEIR (Table 3.2-1) give 125 ft, which is drawn.")
        elif fh != h:
            raise SystemExit(f"Figure 8.3.1 shows {loc} at {fh} ft, Table 8.3.2 at {h} ft")
        if loc in ("O5", "P1", "P2"):
            notes.append("The April 2022 Draft SEIR (Table 3.2-1) gave 65 ft; the approved master plan's 60 ft is drawn.")
        if loc in ("R4A", "R6"):
            notes.append("One of two sites (2.4 acres) Google dedicates to the City for affordable housing; "
                         "the City will choose its developer and design.")
        if loc in ("R1", "R2"):
            notes.append("Within the high-rise core near the VTA Middlefield station; the CLUP airfield limit sets 123 ft.")
        prog = PROGRAM.get(loc)
        notes.insert(0, f"Whole buildable area at its maximum height{f' ({prog})' if prog else ''}; actual "
                        f"buildings will be smaller and step down.")
        props = {
            "kind": "block",
            "block": loc,
            "label": label,
            "stage": "entitled",
            "height_ft": float(h),
            "podium_ft": None,
            "base_ft": 0,
            "use": use,
            "phase": phase,
            "illustrative": True,
            "source": (f"illustrative: buildable area traced from {fig_ref}, Figure 8.3.5 (PDF p. 132); maximum "
                       f"height {h} ft from Table 8.3.2 (PDF p. 130); phase from Development Agreement Exhibit D"),
            "note": " ".join(notes),
        }
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(g))})

    check = {"envelopes_m2": round(total), "off_site_m2": round(outside), "off_site_share": round(outside / total, 4)}
    print(f"[{PROJECT_ID}] {check['off_site_share']:.1%} of the traced envelope area falls off the site parcels")
    if check["off_site_share"] > 0.03:
        raise SystemExit("too much of the traced massing falls off the site; check the georeference")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: the 14 building locations of the approved Middlefield Park Master Plan "
                "(October 2022) are drawn as their whole buildable areas inside the required setbacks (Figure 8.3.5), "
                "each raised to its maximum height in the plan's Table 8.3.2: 123 ft for the residential towers R1 and "
                "R2 by the light rail station, 125 ft for office O1, 95 ft for the other offices and residential "
                "sites (including the two affordable housing sites dedicated to the City, R4A and R6) and 60 ft for "
                "office O5 and the two garages. These are height limits, not building designs: real buildings will "
                "be smaller, seven to 11 stories residential and four to nine office. Parks and streets aren't drawn, "
                "nothing new has been built, and the existing office buildings stay in the base map."
            ),
            "note": ("Each block is a buildable area at its maximum approved height; building designs come with "
                     "later permits."),
            "sourceUrl": MASTER_PLAN["url"],
            "sourceLabel": "Master plan, 2022 (PDF)",
            "georeference": {
                "figure_8_3_5": {**georef, "image_px": list(SETBACK_SIZE)},
                "check_intersections": {"what": "street-centreline intersections in the figure against OpenStreetMap, "
                                                "after the fit", "controls": xcheck},
                "check_boundary": bcheck,
                "check_against_parcels": check,
            },
            "documents": {
                "master_plan": {"title": MASTER_PLAN["title"], "url": MASTER_PLAN["url"], "sha256": MASTER_PLAN["sha256"],
                                "pages": "Figure 8.3.1 (PDF p. 129), Table 8.3.2 (p. 130), Figure 8.3.5 (p. 132)"},
                "resolution": RESOLUTION,
                "phasing": DA_PHASING,
            },
            "license": "Envelopes: traced from a public City of Mountain View document. "
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
