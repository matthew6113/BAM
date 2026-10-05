"""Suisun expansion: proposed land-use zones, traced from the city's Notice of Preparation.

Nothing here is adopted. The only official land-use map is in the City of Suisun City's Notice
of Preparation for the project's environmental impact report (CEQAnet SCH 2025110452, Nov 12,
2025), which describes the applicant's proposal for review:

- Figure 5 "Specific Plan Land Use Zones" (PDF p. 18) maps the seven zones the proposed
  Specific Plan would establish (NOP pp. 5-6; acreages in Table 1, p. 7). Neighborhood Mixed
  Use is one colour on the map; the text splits it by Travis AFB compatibility zone (C 2,463
  acres, D 4,133 acres) but the figure doesn't draw that line, so it is drawn as one zone.
- Figure 2 (PDF p. 15) shows the proposed Area Plan's two sub-areas (NOP p. 5): the Travis
  Protection Zone (5,726 acres, keeping the county's agricultural restrictions) and the
  existing Lambie Industrial Park (1,410 acres, county MG-3 industrial zoning carried over).
  The site boundary in data/boundaries was traced from the same figure.

No draft specific plan or draft EIR has been published, so there is no finer or newer
official land-use map. Both figures are small-scale rasters, so every zone is approximate.

Zone -> category:
  Commercial Mixed Use (CMU) -> mixed-use       Industry and Technology (IT) -> industrial
  Maker and Manufacturing (MM) -> mixed-use     Neighborhood Mixed Use (NMU) -> residential
    (MM allows housing, workshops and light      (the NOP: "predominantly, but not
     industry together)                           exclusively, a residential zone")
  Open Space Civic (OSC) -> open-space          Open Space Infrastructure (OSI) -> other
    (Central Park)                                (water, waste, solar and energy systems,
  Open Space (OS) -> open-space                    with trails and buffers)
  Travis Protection Zone -> other (agricultural restrictions kept)
  Lambie Industrial Park -> industrial

Specific Plan streets and the state routes drawn over the zones are given to the nearest
zone, so the ~153 acres of Caltrans right-of-way and Delta Camp (Table 1) are not split out.

Georeferencing:
- Figure 5: pixels of existing roads drawn in the base map (SR-12, SR-113 and eight county
  roads) are fitted to the same roads in OpenStreetMap (via Overture) by trimmed ICP.
- Figure 2: the same SR-12 / SR-113 fit used for the site boundary (traced_boundaries.py).

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_suisun_expansion
"""

from __future__ import annotations

import json
import math

import cv2
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "suisun-expansion"
STAGE = "entitlement"
ACRE_M2 = tb.ACRE_M2

NOP = {
    "title": "Suisun Expansion Project Notice of Preparation (City of Suisun City, SCH 2025110452, Nov 2025)",
    "url": tb.SUISUN_NOP["url"],
    "sha256": tb.SUISUN_NOP["sha256"],
    "file": "ssn-nop-2025110452.pdf",
}
CEQANET = "https://ceqanet.lci.ca.gov/2025110452"

FIG5_PAGE = 17  # PDF p. 18
FIG5_SIZE = (2500, 1419)
FIG5_MAP = (310, 45, 2185, 980)  # map frame (image pixels): x0, y0, x1, y1; legend below

# In-map fill colours (sampled from the map; the legend swatches are printed darker).
ZONES = {
    "CMU": {"rgb": (243, 162, 198), "label": "Proposed commercial mixed use (CMU)", "category": "mixed-use",
            "acres": 868, "note": "Downtown and two district centres: offices, higher-density housing, hotels, "
            "hospitals, larger retail, civic and cultural uses (NOP p. 5). Table 1 (p. 7): up to 33,501 homes and "
            "29.7M sq ft non-residential at full buildout."},
    "IT": {"rgb": (203, 221, 242), "label": "Proposed industry and technology (IT)", "category": "industrial",
           "acres": 2272, "note": "Manufacturing, research, industrial and infrastructure uses such as data centres "
           "and plants; no housing (NOP p. 5). Table 1 (p. 7): up to 51.9M sq ft non-residential."},
    "MM": {"rgb": (217, 183, 215), "label": "Proposed maker and manufacturing (MM)", "category": "mixed-use",
           "acres": 698, "note": "Small businesses, light industry, entertainment and housing mixed (NOP p. 6). "
           "Table 1 (p. 7): up to 18,259 homes and 14.0M sq ft non-residential."},
    "NMU": {"rgb": (247, 220, 177), "label": "Proposed neighborhood mixed use (NMU)", "category": "residential",
            "acres": 6596, "note": "Predominantly residential, with smaller workplaces, schools, shops and parks "
            "(NOP p. 6). The text splits it by Travis AFB compatibility zone (C: 2,463 acres, row homes; D: 4,133 "
            "acres, row homes and multi-family) but Figure 5 doesn't draw that line. Table 1 (p. 7): up to "
            "122,153 homes in all."},
    "OSC": {"rgb": (203, 224, 149), "label": "Proposed open space civic (OSC)", "category": "open-space",
            "acres": 865, "note": "Central Park around the Big Ditch: recreation and civic gathering places "
            "(NOP p. 6)."},
    "OSI": {"rgb": (187, 211, 197), "label": "Proposed open space infrastructure (OSI)", "category": "other",
            "acres": 2967, "note": "At the edge of the plan: water, waste, solar and energy-storage systems, "
            "with trails, conservation areas and buffers (NOP p. 6). Category other: mainly infrastructure."},
    "OS": {"rgb": (212, 235, 214), "label": "Proposed open space (OS)", "category": "open-space",
           "acres": 1319, "note": "Recreation, natural and agricultural land, including existing conservation "
           "easements (NOP p. 6)."},
}
# Pixels of hatching drawn over OS (conservation easement) and of road lines are reassigned
# to the nearest zone below.
MAX_DIST = 26

# Existing roads in Figure 5's base map (image pixels, polylines), each paired with the
# OpenStreetMap road it is fitted to. Pixels of dark grey road ink within 8 px of a guide
# are used.
FIG5_GUIDES = {
    "SR-113": [(1235, 56), (1235, 728)],
    "Birds Landing Road": [(1237, 752), (1231, 965)],
    "Olsen Road": [(985, 752), (988, 860)],
    "Currie Road": [(1425, 752), (1425, 960)],
    "Azevedo Road": [(1675, 752), (1675, 922)],
    "Shiloh Road": [(670, 450), (672, 960)],
    "Little Honker Bay Road": [(681, 735), (950, 735)],
    "Creed Road": [(325, 229), (1100, 231)],
    "SR-12 west": [(325, 347), (600, 350)],
    "SR-12 south": [(990, 737), (1670, 737)],
    "SR-12 east": [(1690, 737), (1787, 750), (2120, 966)],
}
# Starting transform: the 2.5-mile scale bar (about 12.8 m per image pixel), and SR-12 meeting
# SR-113 (Birds Landing Road) at about (1236, 737).
FIG5_INIT = {"scale": 12.8, "fig": (1236.0, 737.0), "utm": (604500.0, 4226850.0)}

AREA_PLAN = {
    "TPZ": {"rgb": [(165, 177, 141), (158, 167, 134), (120, 130, 100)],
            "label": "Proposed area plan: Travis Protection Zone", "category": "other", "acres": 5726,
            "note": "Buffer for Travis Air Force Base operations that would keep the development restrictions of "
            "the county's Exclusive Agricultural zone (NOP p. 5). Category other: agricultural land, no new "
            "community."},
    "LIP": {"rgb": [(159, 192, 237)], "label": "Proposed area plan: Lambie Industrial Park", "category": "industrial",
            "acres": 1410, "note": "Existing industrial park; the Area Plan would keep it for industrial uses as "
            "under the county's MG-3 zoning (NOP p. 5)."},
}


# Metres by which the Figure 2 fills are grown (about 2 and 7 figure pixels): the fills stop at
# the dash-dot annexation line and at the sub-area lines, which belong to the areas.
AREA_PLAN_GROW_M = {"LIP": 40.0, "TPZ": 150.0}


def _image(pdf_path, page_index: int, size) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[page_index]
    for obj in page.get_objects():
        if obj.type == 3:
            rgb = np.asarray(obj.get_bitmap(render=False).to_pil().convert("RGB"))
            if rgb.shape[1::-1] == tuple(size):
                return rgb
    raise SystemExit(f"figure image on PDF page {page_index + 1} not found")


def _osm_roads():
    g = tb.streets("suisun", (-122.10, 38.05, -121.60, 38.40))
    sr12 = g[(g["class"] == "trunk")]
    out = {
        "SR-113": g[(g["class"] == "primary") & g.intersects(shapely.box(601000, 4226500, 606000, 4260000))],
        "SR-12 west": sr12[sr12.intersects(shapely.box(585000, 4228000, 597000, 4236000))],
        "SR-12 south": sr12[sr12.intersects(shapely.box(597000, 4224000, 614000, 4228500))],
        "SR-12 east": sr12[sr12.intersects(shapely.box(609000, 4218000, 620000, 4228500))],
    }
    for name in FIG5_GUIDES:
        if name not in out:
            out[name] = g[g["name"] == name]
    for name, sel in out.items():
        if sel.empty:
            raise SystemExit(f"{name} not found in OpenStreetMap")
    return {k: shapely.union_all(v.geometry.to_numpy()) for k, v in out.items()}


def georeference_fig5(rgb: np.ndarray):
    roads = _osm_roads()
    v = rgb.astype(float).mean(axis=2)
    sat = rgb.max(axis=2).astype(int) - rgb.min(axis=2)
    ink = (v < 175) & (sat < 20)
    pts, groups, targets = [], [], []
    for i, (name, guide) in enumerate(FIG5_GUIDES.items()):
        m = np.zeros(ink.shape, np.uint8)
        cv2.polylines(m, [np.array(guide, np.int32)], False, 1, 17)
        ys, xs = np.nonzero(m.astype(bool) & ink)
        pts.append(np.c_[xs, ys].astype(float) + 0.5)
        groups.append(np.full(len(xs), i))
        targets.append(roads[name])
    pts, groups = np.vstack(pts), np.concatenate(groups)
    init = trace.Similarity(FIG5_INIT["scale"], 0.0, 0, 0)
    o = init.apply([FIG5_INIT["fig"]])[0]
    init.tx, init.ty = FIG5_INIT["utm"][0] - o[0], FIG5_INIT["utm"][1] - o[1]
    keep = 0.8
    sim, d = tb.icp(pts, targets, groups, init, keep, iterations=80)
    rep = tb.icp_report(sim, d, keep, "road-line pixels vs OpenStreetMap")
    rep["roads"] = list(FIG5_GUIDES)
    return sim, rep, d


def georeference_fig2(rgb: np.ndarray):
    """The site-boundary fit from traced_boundaries.build_suisun, repeated (same guides, same OSM roads)."""
    g = tb.streets("suisun", (-122.10, 38.05, -121.60, 38.40))
    osm = {
        "SR-12": g[(g["class"] == "trunk") & g.intersects(shapely.box(588000, 4224000, 612000, 4234000))],
        "SR-113": g[(g["class"] == "primary") & g.intersects(shapely.box(601000, 4226500, 606000, 4260000))],
    }
    v = rgb.astype(float).mean(axis=2)
    sat = rgb.max(axis=2).astype(float) - rgb.min(axis=2)
    casing = (v < 120) & (sat < 14) & (v > 45)
    pts, groups, targets = [], [], []
    for i, (name, guide) in enumerate(tb.SUISUN_GUIDES.items()):
        m = np.zeros(casing.shape, np.uint8)
        cv2.polylines(m, [np.array(guide, np.int32)], False, 1, 17)
        ys, xs = np.nonzero(m.astype(bool) & casing)
        pts.append(np.c_[xs, ys].astype(float))
        groups.append(np.full(len(xs), i))
        targets.append(shapely.union_all(osm[name].geometry.to_numpy()))
    pts, groups = np.vstack(pts), np.concatenate(groups)
    init = trace.Similarity(tb.SUISUN_INIT["scale"], math.radians(tb.SUISUN_INIT["rotation_deg"]), 0, 0)
    o = init.apply([tb.SUISUN_INIT["fig"]])[0]
    init.tx, init.ty = tb.SUISUN_INIT["utm"][0] - o[0], tb.SUISUN_INIT["utm"][1] - o[1]
    keep = 0.8
    sim, d = tb.icp(pts, targets, groups, init, keep, iterations=60)
    return sim, tb.icp_report(sim, d, keep, "SR-12 and SR-113 casings vs OpenStreetMap")


def _mask_polys(mask: np.ndarray, min_px: int = 40):
    contours, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    if hier is None:
        return shapely.MultiPolygon()
    for i, c in enumerate(contours):
        if hier[0][i][3] != -1 or len(c) < 3:
            continue
        holes, ch = [], hier[0][i][2]
        while ch != -1:
            if len(contours[ch]) >= 3 and cv2.contourArea(contours[ch]) >= min_px:
                holes.append(contours[ch].reshape(-1, 2) + 0.5)
            ch = hier[0][ch][0]
        p = shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5, holes))
        polys.extend(q for q in getattr(p, "geoms", [p]) if isinstance(q, Polygon) and q.area >= min_px)
    return shapely.union_all(polys) if polys else shapely.MultiPolygon()


def trace_fig5(rgb: np.ndarray) -> dict:
    """Label each pixel inside the Specific Plan with its zone (nearest-zone fill under line work)."""
    keys = list(ZONES)
    cols = np.array([ZONES[k]["rgb"] for k in keys], float)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None], axis=3)
    lab = np.where(dist.min(axis=2) <= MAX_DIST, dist.argmin(axis=2), -1)
    x0, y0, x1, y1 = FIG5_MAP
    frame = np.zeros(lab.shape, bool)
    frame[y0:y1, x0:x1] = True
    lab[~frame] = -1
    # Drop specks (anti-aliased line edges that happen to match a fill colour).
    for i in range(len(keys)):
        m = (lab == i).astype(np.uint8)
        n, cc, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
        small = np.isin(cc, np.nonzero(stats[:, cv2.CC_STAT_AREA] < 60)[0]) & (m > 0)
        lab[small] = -1
    zone = lab >= 0
    # The Specific Plan area: all zone fills, with the line work between them closed.
    plan = cv2.morphologyEx(zone.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    cnts, _ = cv2.findContours(plan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    plan = np.zeros_like(plan)
    cv2.drawContours(plan, [c for c in cnts if cv2.contourArea(c) > 5000], -1, 1, -1)
    # Nearest zone for every line pixel inside the plan.
    _, idx = cv2.distanceTransformWithLabels((~zone).astype(np.uint8), cv2.DIST_L2, 5,
                                             labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(zone)
    lookup = np.full(idx.max() + 1, -1)
    lookup[idx[ys, xs]] = lab[ys, xs]
    filled = np.where(plan > 0, lookup[idx], -1)
    out = {}
    for i, k in enumerate(keys):
        m = (filled == i).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        out[k] = _mask_polys(m)
    return out


def trace_fig2(rgb: np.ndarray) -> dict:
    out = {}
    for k, z in AREA_PLAN.items():
        pal = np.array(z["rgb"], float)
        d = np.linalg.norm(rgb[:, :, None, :].astype(float) - pal[None, None], axis=3).min(axis=2)
        m = (d < 22).astype(np.uint8)
        m[:, tb.SUISUN_LEGEND_X:] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        out[k] = _mask_polys(m, min_px=200)
    return out


def _clean(g, min_acres: float = 2.0):
    parts = []
    for p in getattr(g, "geoms", [g]):
        if not isinstance(p, Polygon) or p.area < min_acres * ACRE_M2:
            continue
        holes = [h for h in p.interiors if Polygon(h).area >= min_acres * ACRE_M2]
        parts.append(Polygon(p.exterior, holes))
    if not parts:
        return None
    return parts[0] if len(parts) == 1 else shapely.MultiPolygon(parts)


def main() -> None:
    pdf = trace.fetch_document(NOP["url"], tb.DOCS / NOP["file"], NOP["sha256"])
    site_wgs = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
                     ["features"][0]["geometry"])
    import geopandas as gpd

    site = gpd.GeoSeries([site_wgs], crs=4326).to_crs(tb.UTM).iloc[0]

    rgb5 = _image(pdf, FIG5_PAGE, FIG5_SIZE)
    sim5, rep5, d5 = georeference_fig5(rgb5)
    print(f"[suisun landuse] Figure 5: scale {sim5.scale:.2f} m/px, rotation {np.degrees(sim5.rotation):.2f} deg, "
          f"trimmed RMS {sim5.rms_m:.0f} m, median {np.median(d5):.0f} m")
    rgb2 = _image(pdf, tb.SUISUN_PAGE, tb.SUISUN_IMAGE_SIZE)
    sim2, rep2 = georeference_fig2(rgb2)
    print(f"[suisun landuse] Figure 2: scale {sim2.scale:.2f} m/px, trimmed RMS {sim2.rms_m:.0f} m")

    sp = {k: sim5.geometry(g).buffer(0) for k, g in trace_fig5(rgb5).items()}
    sp = {k: g.intersection(site) for k, g in sp.items()}
    sp_union = shapely.union_all(list(sp.values())).buffer(0)
    # Area Plan sub-areas: the Figure 2 fills, grown to take in the boundary line and the thin gaps
    # left by line work (AREA_PLAN_GROW_M), kept inside the site and outside the Specific Plan zones.
    traced2 = {k: sim2.geometry(g).buffer(0) for k, g in trace_fig2(rgb2).items()}
    rest = site.difference(sp_union)
    ap = {"LIP": traced2["LIP"].buffer(AREA_PLAN_GROW_M["LIP"]).intersection(rest)}
    ap["TPZ"] = traced2["TPZ"].buffer(AREA_PLAN_GROW_M["TPZ"]).intersection(rest).difference(ap["LIP"])

    features, drawn = [], {}
    tol = 6.0  # m: under half a pixel of either figure (13 and 20 m per pixel)
    for key, spec, geom, fig in ([(k, ZONES[k], sp[k], "Figure 5, Specific Plan Land Use Zones, p. 18") for k in ZONES]
                                 + [(k, AREA_PLAN[k], ap[k], "Figure 2, Annexation Area, Area Plan, Specific Plan, "
                                     "and 20 Year Plan Boundaries, p. 15") for k in AREA_PLAN]):
        geom = _clean(geom.simplify(tol))
        if geom is None:
            raise SystemExit(f"{key}: nothing traced")
        acres = geom.area / ACRE_M2
        drawn[key] = acres
        features.append({"type": "Feature", "properties": {
            "kind": "zone",
            "category": spec["category"],
            "label": spec["label"],
            "source": f"traced: {NOP['title']}, {fig}",
            "note": (f"{spec['note']} About {acres:,.0f} acres as drawn; the NOP states about {spec['acres']:,} "
                     f"acres. Approximate: traced from a small-scale figure. Proposed, not adopted."),
            "stage": STAGE,
            "accuracy": "approximate",
        }, "geometry": mapping(tb.to_wgs(geom))})
        print(f"  {key:4s} {spec['category']:12s} {acres:8,.0f} ac (NOP {spec['acres']:,})")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Proposed land use, nothing adopted: the seven zones of the proposed Specific Plan traced from Figure 5 "
                "of the City of Suisun City's Notice of Preparation (SCH 2025110452, Nov 2025), and the proposed Area "
                "Plan's Travis Protection Zone and Lambie Industrial Park from its Figure 2. Streets and state routes "
                "are folded into the nearest zone (the ~153 acres of Caltrans right-of-way and Delta Camp are not "
                "split out), Neighborhood Mixed Use isn't split by Travis compatibility zone because the figure "
                "doesn't draw that line, and no buildings are drawn. All boundaries are approximate."),
            "note": "Proposed land use from the city's 2025 Notice of Preparation; nothing is adopted. Approximate zones, not buildings.",
            "sourceUrl": NOP["url"],
            "sourceLabel": "Notice of preparation, 2025 (PDF)",
            "georeference": {
                "figure_5": rep5,
                "figure_2": rep2,
                "note": ("Figure 5 fitted to existing roads in its base map (SR-12, SR-113 and seven county roads) by "
                         f"trimmed ICP: about {sim5.scale:.1f} m per pixel, RMS {sim5.rms_m:.0f} m. Figure 2 uses the "
                         f"site boundary's SR-12 / SR-113 fit (about {sim2.scale:.0f} m per pixel, RMS "
                         f"{sim2.rms_m:.0f} m). Zones are clipped to the site boundary; Area Plan zones exclude the "
                         "Specific Plan zones."),
            },
            "license": ("Zone shapes: traced from a public City of Suisun City CEQA notice. Georeference: "
                        + tb.OSM_LICENSE + "."),
            "documents": [CEQANET, NOP["url"]],
        },
        "features": features,
    }
    out = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tb._round(fc, 6), indent=1) + "\n")
    print(f"[suisun landuse] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.0f} KB); "
          f"site {site.area / ACRE_M2:,.0f} ac, zones {sum(drawn.values()):,.0f} ac")


if __name__ == "__main__":
    main()
