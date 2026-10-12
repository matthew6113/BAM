"""West Midway and RESHAP (Alameda Point): block height limits from the approved development plans.

Sources (City of Alameda records, Legistar):
- West Midway: Development Plan approved by the Planning Board on May 22, 2023 (Resolution PB-23-09),
  attached as Exhibit 2 to the Dec 8, 2025 Phase A design review (Legistar matter 15369), sheet 10
  "Land Use Diagram & Building Heights" (PDF p. 10, dated May 4, 2023). The diagram is one raster image:
  each land-use block is a flat colour matching a vector legend swatch, and each block prints its
  height limit ("HEIGHT: 40' Max."; 50 ft for the three 4-story condominium parcels). Blocks are traced
  by classifying pixels to the nearest legend colour.
- RESHAP: Development Plan approved May 8, 2023 (Exhibit 1 to the Dec 4, 2023 amendment, Legistar
  matter 13437), p. 13 "Landuse Diagram" (1" = 100'): "ALL BUILDING HEIGHTS LIMITED TO +/- 50' HEIGHT".
  The December 2023 amendment raised the homes from 309 to 332 without changing "the building
  footprints, planned height of the buildings". The residential buildings (orange "Residential flats"
  and "Resident services" fills) are drawn; the 1- and 2-story shelter and community buildings, whose
  heights the plan doesn't give in feet, the farm, parking and open space aren't.

Georeference: both figures are fitted (similarity, trimmed ICP) to the Alameda County Assessor's lots
of Tract 8696, the 2025 final map that subdivided the site (the same parcels as the site boundary,
pipeline/bam_pipeline/sites/official_boundaries.py "west-midway-reshap"). West Midway's block fills are
matched to the street edges of the lots; RESHAP's campus outline (all of its fills and paving) to the
lots that West Midway's blocks don't cover. No hand-picked control points. The RESHAP fit's scale is
checked against the plan's printed 1" = 100' scale.

What this is and isn't: every block is drawn to its height limit over the whole block, not as building
designs, so all of it is labelled illustrative. Streets, paseos, parks and the commercial corner's
temporary container village aren't drawn as buildings (the corner is drawn as its block, 40 ft).

    uv run --directory pipeline python -m bam_pipeline.sites.massing_west_midway_reshap
"""

from __future__ import annotations

import json

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import shapely
from shapely.geometry import Polygon, mapping

from .. import config, trace
from . import official_boundaries as ob
from . import traced_boundaries as tb

PROJECT_ID = "west-midway-reshap"
UTM = tb.UTM
ACRE_M2 = tb.ACRE_M2
DOCS = tb.DOCS
OUT = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
STAGE = "entitled"

WM_PLAN = {
    "title": "West Midway Development Plan (Brookfield Properties and Catellus, May 4, 2023), approved May 22, 2023",
    "url": "https://legistar1.granicus.com/alameda/attachments/5be8021b-f3c6-4a76-8312-60267b458f36.pdf",
    "file": "wm-development-plan-2023.pdf",
    "sha256": "9cbd1d3c5b05455fc5ade24e78867a3acd84c20d1dc59e82e9bf9c5ae7d4c536",
    "page_index": 9,
    "sheet": "sheet 10, Land Use Diagram & Building Heights",
}
WM_RASTER_PX = (4150, 3038)
RESHAP_PLAN = {
    "title": "RESHAP Development Plan (May 8, 2023), approved by the Planning Board on May 8, 2023",
    "url": "https://legistar1.granicus.com/alameda/attachments/d3ee17a1-dd9a-4874-99d4-ae7134ed1c5b.pdf",
    "file": "reshap-development-plan-2023.pdf",
    "sha256": "8f6f12d7ddf2063465b90b378577bfb67e4a341e170174687211e511a558f592",
    "page_index": 12,
    "sheet": "p. 13, Landuse Diagram",
}
RESHAP_DPI = 300
RESHAP_CROP_PX = (2100, 380, 4200, 2400)  # x0, y0, x1, y1 of the site in the 300-dpi render (legend excluded)
RESHAP_SCALE_M_PX = 100 * 0.3048 / RESHAP_DPI  # 1" = 100'

# West Midway blocks: legend colour as rendered in the raster (RGB), height printed in the block, use, homes.
# Phase A (Dec 8, 2025 design review, 284 homes) is the duets, the 3-story townhomes A and the 4-story condos.
WM_BLOCKS = {
    "duets": {"rgb": (226, 189, 178), "height": 40, "label": "3-story duets", "homes": 60, "phase": "Phase A",
              "note": "60 homes in 30 three-story duet buildings; eaves 30 ft, roof-deck stair towers up to 45 ft."},
    "tha": {"rgb": (253, 245, 162), "height": 40, "label": "3-story townhomes A", "homes": 110, "phase": "Phase A",
            "note": "110 homes in three-story townhouse buildings."},
    "condo4": {"rgb": (254, 172, 98), "height": 50, "label": "4-story condominiums", "homes": 114, "phase": "Phase A",
               "note": "114 homes on three parcels, the only part of West Midway allowed 50 ft."},
    "condo3": {"rgb": (125, 217, 152), "height": 40, "label": "3-story condominiums", "homes": 104, "phase": "Phase B",
               "note": "104 homes."},
    "thb": {"rgb": (255, 238, 96), "height": 40, "label": "3-story townhomes B", "homes": 90, "phase": "Phase B",
            "note": "90 homes along West Tower Avenue."},
    "retail": {"rgb": (188, 105, 89), "height": 40, "label": "Commercial corner", "homes": None, "phase": "Phase B",
               "note": "7,500–10,000 sq ft of commercial space at Pan Am Way and West Tower Avenue, first as a "
                       "temporary container village (by 2027), then a permanent building (by 2030)."},
}
WM_MIN_BLOCK_PX = 60_000  # drops stray specks of a colour inside other blocks (labels, anti-aliasing)

# RESHAP fills (300-dpi render), the residential buildings and the rest of the campus (for the outline only).
RESHAP_BUILDINGS = {"flats": (249, 183, 0), "services": (249, 123, 0)}
RESHAP_OTHER = {"shelter": (255, 226, 198), "community": (203, 101, 122), "os_n": (0, 127, 64),
                "os_r": (221, 237, 184), "farm": (0, 0, 255), "parking": (122, 122, 122), "paving": (207, 207, 207)}
RESHAP_MIN_PX = 3000

ICP_KEEP = 0.6  # the 2025 lots moved some street edges (Skylark Street now curves), so trim harder


def _wm_raster(pdf_path) -> np.ndarray:
    page = pdfium.PdfDocument(str(pdf_path))[WM_PLAN["page_index"]]
    imgs = [o for o in page.get_objects() if o.type == pdfium_c.FPDF_PAGEOBJ_IMAGE and o.get_px_size()[0] > 4000]
    if len(imgs) != 1 or tuple(imgs[0].get_px_size()) != WM_RASTER_PX:
        raise SystemExit("West Midway sheet 10: the land use raster is not where expected")
    with pdfplumber.open(str(pdf_path), pages=[WM_PLAN["page_index"] + 1]) as pdf:
        text = pdf.pages[0].extract_text()
    for s in ("LAND USE DIAGRAM & BUILDING HEIGHTS", "HEIGHT: 40' Max.", "May 4, 2023"):
        if s not in text:
            raise SystemExit(f"West Midway sheet 10 no longer shows {s!r}")
    return np.asarray(imgs[0].get_bitmap(render=False).to_pil().convert("RGB")).astype(int)


def _classify(rgb: np.ndarray, palette: dict, max_dist: float, close_px: int, open_px: int) -> dict:
    """Pixel masks for each palette colour (nearest colour within max_dist), closed over text and lines."""
    keys = list(palette)
    cols = np.array([palette[k] for k in keys], float)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None], axis=3)
    near, ok = dist.argmin(axis=2), dist.min(axis=2) <= max_dist
    out = {}
    for i, k in enumerate(keys):
        m = ((near == i) & ok).astype(np.uint8) * 255
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((close_px, close_px), np.uint8))
        out[k] = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((open_px, open_px), np.uint8))
    return out


def _polys(mask: np.ndarray, min_px: float) -> list[Polygon]:
    cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < min_px:
            continue
        holes, ch = [], hier[0][i][2]
        while ch != -1:
            if cv2.contourArea(cs[ch]) >= min_px / 4:
                holes.append(cs[ch].reshape(-1, 2) + 0.5)
            ch = hier[0][ch][0]
        out.append(shapely.make_valid(Polygon(cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2) + 0.5, holes)))
    return out


def _outline_points(g, step: float) -> np.ndarray:
    pts = []
    parts = shapely.get_parts(g)
    for ring in shapely.get_rings(parts[shapely.get_type_id(parts) == 3]):
        ln = shapely.LineString(ring.coords)
        n = max(int(ln.length / step), 4)
        pts.append(shapely.get_coordinates(shapely.line_interpolate_point(ln, np.linspace(0, ln.length, n, endpoint=False))))
    return np.vstack(pts)


def _bbox_init(fig_geom, utm_geom) -> trace.Similarity:
    fx0, fy0, fx1, fy1 = fig_geom.bounds
    ux0, uy0, ux1, uy1 = utm_geom.bounds
    src = [(fx0, fy1), (fx1, fy1), (fx1, fy0), (fx0, fy0)]  # figure y down: bottom-left first
    dst = [(ux0, uy0), (ux1, uy0), (ux1, uy1), (ux0, uy1)]
    return trace.fit_similarity(src, dst)


def _fit(fig_geom, target_geom, step: float, what: str, scale: float | None = None):
    pts = _outline_points(fig_geom, step)
    init = _bbox_init(fig_geom, target_geom)
    if scale is not None:
        init = trace.Similarity(scale, init.rotation, init.tx, init.ty)
    target = shapely.union_all([shapely.boundary(target_geom)])
    sim, d = tb.icp(pts, [target], np.zeros(len(pts), int), init, ICP_KEEP, iterations=100, scale=scale)
    return sim, tb.icp_report(sim, d, ICP_KEEP, what)


def main() -> None:
    lots = ob._utm_shapes(ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID]))
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    # ---- West Midway blocks
    wm_pdf = trace.fetch_document(WM_PLAN["url"], DOCS / WM_PLAN["file"], WM_PLAN["sha256"])
    rgb = _wm_raster(wm_pdf)
    masks = _classify(rgb, {k: v["rgb"] for k, v in WM_BLOCKS.items()}, max_dist=22, close_px=31, open_px=9)
    blocks_px = {k: shapely.union_all(_polys(m, WM_MIN_BLOCK_PX)) for k, m in masks.items()}
    # A block that encloses another (townhomes A around the condo parcels) loses the enclosed area.
    order = list(WM_BLOCKS)
    for k in order:
        others = shapely.union_all([blocks_px[o] for o in order if o != k])
        blocks_px[k] = shapely.make_valid(blocks_px[k].difference(others))
    wm_union_px = shapely.union_all(list(blocks_px.values()))
    lots_union = shapely.union_all(lots.to_numpy())
    wm_sim, wm_rep = _fit(wm_union_px, lots_union, 6.0, "West Midway block outlines to the Tract 8696 lots")
    if wm_sim.rms_m > 2.5 or wm_rep["median_m"] > 4:
        raise SystemExit(f"West Midway fit is poor: RMS {wm_sim.rms_m:.1f} m, median {wm_rep['median_m']} m")
    # Blocks are kept to the 2025 lots: the final map moved a few street edges from the 2023 plan.
    lots_cut = lots_union.buffer(1.0)
    blocks = {k: shapely.make_valid(wm_sim.geometry(g)).intersection(lots_cut) for k, g in blocks_px.items()}
    print(f"[west-midway] sheet 10 fit: RMS {wm_sim.rms_m:.2f} m, scale {wm_sim.scale:.4f} m/px, "
          f"rotation {np.degrees(wm_sim.rotation):.2f}°")

    # ---- RESHAP: the lots West Midway's blocks don't cover
    wm_all = shapely.union_all(list(blocks.values())).buffer(3)
    reshap_lots = [g for g in lots if g.intersection(wm_all).area < 0.3 * g.area]
    reshap_site = shapely.union_all(reshap_lots).buffer(8, join_style="mitre").buffer(-8, join_style="mitre")
    print(f"[west-midway] RESHAP lots: {len(reshap_lots)}, {reshap_site.area / ACRE_M2:.2f} acres")

    rs_pdf = trace.fetch_document(RESHAP_PLAN["url"], DOCS / RESHAP_PLAN["file"], RESHAP_PLAN["sha256"])
    with pdfplumber.open(str(rs_pdf), pages=[RESHAP_PLAN["page_index"] + 1]) as pdf:
        t13 = pdf.pages[0].extract_text()
    for s in ("ALL BUILDING HEIGHTS LIMITED TO", "+/- 50' HEIGHT", "LANDUSE DIAGRAM", "1\" = 100'-0\""):
        if s not in t13:
            raise SystemExit(f"RESHAP p. 13 no longer shows {s!r}")
    page = pdfium.PdfDocument(str(rs_pdf))[RESHAP_PLAN["page_index"]]
    rs = np.asarray(page.render(scale=RESHAP_DPI / 72).to_pil().convert("RGB")).astype(int)
    x0, y0, x1, y1 = RESHAP_CROP_PX
    crop = np.full_like(rs, 255)
    crop[y0:y1, x0:x1] = rs[y0:y1, x0:x1]
    rmasks = _classify(crop, {**RESHAP_BUILDINGS, **RESHAP_OTHER}, max_dist=25, close_px=15, open_px=7)
    campus_mask = np.zeros(crop.shape[:2], np.uint8)
    for m in rmasks.values():
        campus_mask |= m
    campus_mask = cv2.morphologyEx(campus_mask, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    campus_px = max(_polys(campus_mask, 200_000), key=lambda p: p.area)
    campus_px = Polygon(campus_px.exterior)
    rs_sim, rs_rep = _fit(campus_px, reshap_site, 15.0, "RESHAP campus outline to the RESHAP lots")
    scale_err = rs_sim.scale / RESHAP_SCALE_M_PX - 1
    rs_rep["printed_scale_check"] = (f"fitted {rs_sim.scale:.4f} m/px against the printed 1\" = 100' "
                                     f"({RESHAP_SCALE_M_PX:.4f} m/px at {RESHAP_DPI} dpi): {scale_err:+.1%}")
    print(f"[west-midway] RESHAP p. 13 fit: RMS {rs_sim.rms_m:.2f} m; {rs_rep['printed_scale_check']}")
    if rs_sim.rms_m > 3.0 or abs(scale_err) > 0.05:
        raise SystemExit("RESHAP fit is poor")
    rs_buildings = shapely.union_all([g for k in RESHAP_BUILDINGS for g in _polys(rmasks[k], RESHAP_MIN_PX)])
    rs_buildings = rs_sim.geometry(rs_buildings)

    # ---- features
    to_wgs = tb.to_wgs
    wm_fig = f"{WM_PLAN['title']}, {WM_PLAN['sheet']}"
    features = []
    for k, spec in WM_BLOCKS.items():
        g = trace.as_multipolygon(shapely.make_valid(blocks[k].intersection(site_utm.buffer(2)).simplify(0.4)))
        acres = g.area / ACRE_M2
        props = {
            "kind": "block", "block": k, "label": spec["label"], "stage": STAGE,
            "height_ft": spec["height"], "podium_ft": None, "base_ft": 0,
            "use": "Residential" if spec["homes"] else "Commercial",
            "phase": spec["phase"], "illustrative": True,
            "source": (f"illustrative: drawn to the {spec['height']}-ft limit printed in the block on {wm_fig} "
                       f"({WM_PLAN['url']}); block traced from the same sheet"),
            "note": spec["note"] + (" Phase A's buildings passed design review on Dec 8, 2025." if spec["phase"] == "Phase A"
                                    else ""),
        }
        if spec["homes"]:
            props["homes"] = spec["homes"]
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(g))})
        print(f"[west-midway] {spec['label']}: {acres:.2f} ac at {spec['height']} ft")
    g = trace.as_multipolygon(shapely.make_valid(rs_buildings.intersection(site_utm.buffer(2)).simplify(0.4)))
    features.append({"type": "Feature", "properties": {
        "kind": "block", "block": "reshap", "label": "RESHAP supportive housing", "stage": STAGE,
        "height_ft": 50, "podium_ft": None, "base_ft": 0, "use": "Residential (supportive and affordable housing)",
        "phase": "Phases 1–4", "illustrative": True, "homes": 332,
        "source": (f"illustrative: the \"Residential flats\" and \"Resident services\" buildings traced from "
                   f"{RESHAP_PLAN['title']}, {RESHAP_PLAN['sheet']} ({RESHAP_PLAN['url']}), drawn to its "
                   "\"ALL BUILDING HEIGHTS LIMITED TO +/- 50' HEIGHT\""),
        "note": ("332 homes in four buildings of up to four stories (the plan's 309, raised to 332 in December 2023 "
                 "without changing the footprints or heights). Phase 1 is Stardust Gardens (80 homes) and Harbor "
                 "Village; the 1- and 2-story shelter and community buildings aren't drawn."),
    }, "geometry": mapping(to_wgs(g))})
    print(f"[west-midway] RESHAP buildings: {g.area / ACRE_M2:.2f} ac at 50 ft")

    for f in features:
        c = shapely.geometry.shape(f["geometry"]).centroid
        cu = gpd.GeoSeries([c], crs=4326).to_crs(UTM).iloc[0]
        if not site_utm.buffer(20).contains(cu):
            raise SystemExit(f"{f['properties']['label']} is off the site")
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: West Midway's six land-use blocks are drawn to the height limits in its "
                        "2023 Development Plan (40 ft; 50 ft for the 4-story condominiums), over whole blocks, not "
                        "as building designs, and RESHAP's residential buildings are drawn from its 2023 land use "
                        "diagram at the plan's 50-ft limit. Streets, paseos, parks, parking and RESHAP's small "
                        "shelter and community buildings aren't drawn."),
            "note": "Blocks are drawn to their height limits, not as building designs.",
            "sourceUrl": WM_PLAN["url"],
            "sourceLabel": "West Midway development plan, 2023 (PDF)",
            "documents": [WM_PLAN["url"], RESHAP_PLAN["url"], ob.SPECS[PROJECT_ID]["landing"]],
            "georeference": {"west_midway_sheet_10": wm_rep, "reshap_p13": rs_rep},
            "license": ("Shapes traced from public City of Alameda records, fitted to Alameda County Assessor parcels "
                        "(county disclaimer)."),
        },
        "features": features,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[west-midway] wrote {OUT.relative_to(config.ROOT)} ({len(features)} features, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
