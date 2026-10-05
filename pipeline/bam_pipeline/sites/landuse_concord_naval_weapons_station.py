"""Concord Naval Weapons Station: land-use districts of the adopted Concord Reuse Project Area Plan.

The adopted land-use control for the former base is the City of Concord's Concord Reuse
Project Area Plan, adopted by the City Council on January 24, 2012 as part of the General
Plan (Res. No. 12-4823.2). Its land-use map is Book One, Figure 3-3 "Area Plan Diagram"
(PDF p. 49, printed p. 41), with the districts defined in Table 3-4 (pp. 44-47) and the
development program in Table 3-2 (p. 40). No later amendment of the Area Plan was found
(checked Oct 2026: the City's Area Plan and Long-Range Planning pages still cite the 2012
plan). The land-use diagram the Council reviewed with the earlier master developer on
August 22, 2018 was direction for a Specific Plan that was never adopted (City memo to
Council, Dec 15, 2020), and the Specific Plan with Brookfield starts in winter 2026-27. The
"Area Plan Diagram" image on the City's Area Plan page (DocumentCenter/View/2357) is a
low-resolution copy of the same 2012 diagram without its legend. The developer's concept
plan in the 2026 Navy term sheet (Exhibit B) is not adopted and is not drawn.

Figure 3-3 is a mix of vector fills and flattened image tiles, so the districts are traced
from a 400-dpi render by nearest-colour classification against the in-map fills. Streets and
creeks drawn over the districts are given to the nearest district: the plan's vector fills
run continuously under the street symbols, and its district acreages include streets.

Georeference: the figure's existing arterials and freeways (vector road fills in the base
map, outside the site) are reduced to centrelines and fitted to OpenStreetMap roads (via
Overture) by trimmed ICP, started from a rough fit to the three BART stations on the map.

Parts of the EDC property the diagram gives no district are left uncovered: chiefly the
strip along the SR-4 / BART corridor north of Delta Road, which the diagram draws as
freeway, and thin slivers at the edges.

The Area Plan covers about 5,046 acres (Table 3-2); the project site here is the Navy's
~2,422-acre Economic Development Conveyance (EDC) property (data/boundaries), so the zones are
clipped to it. Most of the plan's Conservation Open Space (the future regional park, conveyed
separately) lies outside the EDC property.

Zone -> category:
  North Concord TOD core -> mixed-use (office-led mixed-use employment centre; housing optional)
  North Concord TOD neighborhood -> residential ("mixed-use residential district")
  Central neighborhood -> residential        Village neighborhood -> residential
  Village center -> mixed-use (main street with housing, retail, community facilities)
  Commercial flex -> commercial (R&D, light industrial, office and/or retail; the plan's
    "Commercial" heading)
  Campus -> civic and First responder training center -> civic (the plan's "Civic and
    Institutional" heading)
  Conservation open space -> open-space
  Greenways, citywide parks and tournament facilities -> open-space

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_concord_naval_weapons_station
"""

from __future__ import annotations

import json
import math
import sys

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import MultiPolygon, Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "concord-naval-weapons-station"
STAGE = "entitlement"
ACRE_M2 = tb.ACRE_M2
UTM = tb.UTM

BOOK1 = {
    "title": "Concord Reuse Project Area Plan, Book One: Vision and Standards (City of Concord, adopted Jan 24, 2012)",
    "url": "https://www.concordreuseproject.org/DocumentCenter/View/1105",
    "sha256": "2a1e73aafb798240e9cb374daa7cadcd8ceafc30d8bfde2aa203c6dfb31d2571",
    "file": "cnws-area-plan-book1-2012-01-24.pdf",
}
DOCUMENTS = [
    BOOK1["url"],
    "https://www.concordreuseproject.org/152/The-Area-Plan",
    # Res. No. 12-4823.2 (Jan 24, 2012): General Plan amended to adopt the Area Plan.
    "https://www.concordreuseproject.org/DocumentCenter/View/1093/2012-01-24-Res-No-12-48232-Amend-Concord-2030-Urb-Area",
    # Dec 15, 2020 memo: the 2018 diagram was direction for an unadopted Specific Plan.
    "https://concordreuseproject.org/DocumentCenter/View/1786/1-December-15-2020-Memo-to-City-Council",
    "https://www.concordreuseproject.org/157/Specific-Plan",
]
FIG = "Figure 3-3, Area Plan Diagram, p. 41 (PDF p. 49)"
PAGE = 48  # PDF p. 49
MAP_PT = (36.5, 60.5, 575.5, 449.5)  # map frame in PDF points (x0, top, x1, bottom); legend below
DPI = 400

# Vector road fills of the base map (pdfplumber RGB): existing arterials (grey) and the
# freeway casings and centres (SR-4, SR-242).
ROAD_FILLS = [(0.5843, 0.5922, 0.6039), (0.4314, 0.4392, 0.4471), (0.9216, 0.9255, 0.9255)]
# Starting transform from three BART stations (figure points: station icons; lon/lat of the
# stations, approximate) - only a start, refined by the road fit.
INIT_CONTROLS = {
    "North Concord/Martinez BART": ((134.2, 175.4), (-122.0247, 38.0034)),
    "Concord BART": ((104.7, 364.6), (-122.0290, 37.9737)),
    "Pittsburg/Bay Point BART": ((517.1, 92.9), (-121.9454, 38.0189)),
}

# District fills as printed inside the map (sampled; the legend swatches print slightly
# differently). Each: label, category, Table 3-2 acres (planning-area-wide), note.
DISTRICTS = {
    "tod_core": {
        "rgb": [(51, 27, 61)], "label": "North Concord TOD core", "category": "mixed-use", "acres": 55,
        "note": "Region-serving mixed-use employment centre by North Concord BART: Class A offices, shops, "
                "services, plazas; housing optional up to 20 du/gross acre (60-150 du/net acre), FAR 2.0-4.0 "
                "(Table 3-4, p. 44). Table 3-2 (p. 40): ~700 homes and 3,000,000 sq ft commercial."},
    "tod_nbhd": {
        "rgb": [(134, 83, 161)], "label": "North Concord TOD neighborhood", "category": "residential", "acres": 90,
        "note": "Mixed-use residential district within walking distance of BART: 20-30 du/gross acre "
                "(18-100 du/net acre), FAR 1.0-3.0, with local retail, a grocery store and community facilities "
                "(Table 3-4, p. 44). Table 3-2 (p. 40): ~2,200 homes and 150,000 sq ft commercial. Category "
                "residential: the plan calls it a mixed-use residential district."},
    "central": {
        "rgb": [(198, 177, 213)], "label": "Central neighborhood", "category": "residential", "acres": 180,
        "note": "Mixed-use residential district at moderate densities: 15-20 du/gross acre (14-50 du/net "
                "acre), low- to mid-rise (Table 3-4, p. 45). Table 3-2 (p. 40): ~2,600 homes and 100,000 sq ft "
                "commercial."},
    "vcenter": {
        "rgb": [(111, 109, 173)], "label": "Village center", "category": "mixed-use", "acres": 70,
        "note": "Main-street centres anchoring the village neighborhoods: multi-unit housing, retail and "
                "community facilities, 5-20 du/gross acre (18-50 du/net acre), FAR 0.5-2.0 (Table 3-4, p. 45). "
                "Table 3-2 (p. 40): ~500 homes and 350,000 sq ft commercial."},
    "village": {
        "rgb": [(255, 219, 132)], "label": "Village neighborhood", "category": "residential", "acres": 740,
        "note": "Residential districts at moderate to low densities: 8-12 du/gross acre (6-45 du/net acre), "
                "attached and detached homes (Table 3-4, p. 46). Table 3-2 (p. 40): ~6,200 homes."},
    "flex": {
        "rgb": [(249, 175, 143)], "label": "Commercial flex", "category": "commercial", "acres": 210,
        "note": "Region-serving retail and/or workplace district: R&D/flex, light industrial, office and "
                "retail, FAR 0.2-1.0, no housing (Table 3-4, p. 46). Table 3-2 (p. 40): ~1,700,000 sq ft. "
                "Category commercial: the plan lists it under Commercial."},
    "campus": {
        "rgb": [(43, 125, 193)], "label": "Campus", "category": "civic", "acres": 120,
        "note": "Educational, research and development, health-care and/or cultural uses; up to 800,000 sq ft "
                "for any use besides a four-year campus (Table 3-4, p. 47). Category civic: the plan lists it "
                "under Civic and Institutional."},
    "frtc": {
        "rgb": [(0, 155, 205)], "label": "First responder training center", "category": "civic", "acres": 80,
        "note": "Training grounds and facilities for emergency services (Table 3-4, p. 47; Table 3-12, p. 62)."},
    "cons": {
        "rgb": [(226, 219, 158), (219, 212, 154), (212, 205, 148)], "label": "Conservation open space",
        "category": "open-space", "acres": 2715,
        "note": "Conservation lands, mostly the future regional park, conveyed separately from the EDC "
                "property; on the EDC property mainly the creek corridors (Table 3-2, p. 40; Section 3.4)."},
    "green": {
        "rgb": [(88, 129, 68)], "label": "Greenways, citywide parks and tournament facilities", "category": "open-space",
        "acres": 786,
        "note": "Greenways, citywide parks and the tournament sports facility (Table 3-2, p. 40; Section 3.4). "
                "Neighborhood parks, pocket parks and plazas sit inside the development districts and are not "
                "drawn (p. 63)."},
}
MAX_DIST = 24  # colour distance for a pixel to count as a district fill
FILL_GAP_PX = 41  # street and creek symbols up to ~7 pt wide are closed over inside the plan area
MIN_ZONE_ACRES = 0.5
# The BART station icons print in the First Responder Training Center blue; the real district
# is one large fill north of SR-4, so small blue patches are dropped (and filled from their
# neighbours).
MIN_COMPONENT_PX = {"frtc": 5000}
TRACE_EPS_PX = 0.8  # contour simplification in render pixels (~2.6 m), removing the pixel staircase


def _render(pdf_path) -> np.ndarray:
    with pdfplumber.open(pdf_path) as pdf:
        im = pdf.pages[PAGE].crop(MAP_PT).to_image(resolution=DPI).original.convert("RGB")
    return np.asarray(im)


def _px_to_pt(xy):
    a = np.asarray(xy, float).reshape(-1, 2)
    return np.c_[MAP_PT[0] + a[:, 0] * 72 / DPI, MAP_PT[1] + a[:, 1] * 72 / DPI]


def georeference(pdf_path):
    """Fit the figure's existing roads (centrelines of the vector road fills) to OpenStreetMap."""
    k = 8.0  # raster pixels per point
    w, h = int((MAP_PT[2] - MAP_PT[0]) * k), int((MAP_PT[3] - MAP_PT[1]) * k)
    mask = np.zeros((h, w), np.uint8)
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[PAGE]
        for obj in page.curves + page.rects:
            col = obj.get("non_stroking_color")
            if not obj.get("fill") or not isinstance(col, (list, tuple)) or len(col) != 3:
                continue
            if obj["top"] < MAP_PT[1] or obj["bottom"] > MAP_PT[3]:
                continue
            if min(max(abs(a - b) for a, b in zip(col, c)) for c in ROAD_FILLS) > 0.0006:
                continue
            pts = obj.get("pts") or [(obj["x0"], obj["top"]), (obj["x1"], obj["top"]),
                                     (obj["x1"], obj["bottom"]), (obj["x0"], obj["bottom"])]
            if len(pts) >= 3:
                xy = (np.asarray(pts, float) - [MAP_PT[0], MAP_PT[1]]) * k
                cv2.fillPoly(mask, [np.round(xy).astype(np.int32)], 1)
    # Ridge of the distance transform: the road centrelines.
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    ridge = (dist >= cv2.dilate(dist, np.ones((3, 3), np.uint8)) - 1e-6) & (dist > 1.5)
    ys, xs = np.nonzero(ridge)
    pts = np.c_[MAP_PT[0] + (xs + 0.5) / k, MAP_PT[1] + (ys + 0.5) / k]
    pts = np.unique(np.round(pts, 0), axis=0)  # thin to ~1 point per figure point

    g = tb.streets("cnws-concord", (-122.08, 37.93, -121.90, 38.05))
    g = g[g["subtype"] == "road"] if "subtype" in g else g
    g = g[g["class"].isin(["motorway", "trunk", "primary", "secondary", "tertiary"])]
    target = shapely.union_all(g.geometry.to_numpy())

    labels = list(INIT_CONTROLS)
    ll = gpd.GeoSeries(gpd.points_from_xy(*np.array([INIT_CONTROLS[n][1] for n in labels]).T), crs=4326).to_crs(UTM)
    init = trace.fit_similarity([INIT_CONTROLS[n][0] for n in labels], np.c_[ll.x, ll.y], labels)
    keep = 0.7
    sim, d = tb.icp(pts, [target], np.zeros(len(pts), int), init, keep, iterations=100)
    rep = tb.icp_report(sim, d, keep, "arterial and freeway centrelines vs OpenStreetMap")
    rep["init"] = {"from": "three BART stations", "rms_m": round(init.rms_m, 1)}
    print(f"[cnws] init (BART) scale {init.scale:.3f} m/pt rot {math.degrees(init.rotation):.2f} deg RMS {init.rms_m:.0f} m; "
          f"ICP scale {sim.scale:.3f} m/pt rot {math.degrees(sim.rotation):.2f} deg trimmed RMS {sim.rms_m:.1f} m, "
          f"median {np.median(d):.1f} m, p90 {np.quantile(d, 0.9):.1f} m over {len(d)} points")
    return sim, rep


def classify(rgb: np.ndarray) -> np.ndarray:
    """Label image: index into DISTRICTS for every pixel inside the plan area, -1 outside."""
    keys = list(DISTRICTS)
    cols, idx = [], []
    for i, kk in enumerate(keys):
        for c in DISTRICTS[kk]["rgb"]:
            cols.append(c)
            idx.append(i)
    cols, idx = np.array(cols, float), np.array(idx)
    flat = rgb.reshape(-1, 3).astype(float)
    best = np.full(len(flat), np.inf)
    lab = np.full(len(flat), -1)
    for c, i in zip(cols, idx):
        d = np.linalg.norm(flat - c, axis=1)
        sel = d < best
        best[sel], lab[sel] = d[sel], i
    lab[best > MAX_DIST] = -1
    lab = lab.reshape(rgb.shape[:2])
    # Remove specks (anti-aliased edges, text) before filling.
    clean = np.full_like(lab, -1)
    icons = np.zeros(lab.shape, bool)  # dropped symbols that sit on district fills
    for i in range(len(keys)):
        m = (lab == i).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, cc, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        keep = np.zeros(n, bool)
        keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= MIN_COMPONENT_PX.get(keys[i], 60)
        clean[keep[cc]] = i
        if keys[i] in MIN_COMPONENT_PX:
            icons |= (~keep[cc]) & (cc > 0) & (stats[cc, cv2.CC_STAT_AREA] >= 600)
    # Icons count only where they sit on a district fill (the North Concord station, not the others).
    n, cc = cv2.connectedComponents(icons.astype(np.uint8), connectivity=8)
    touch = cv2.dilate((clean >= 0).astype(np.uint8), np.ones((21, 21), np.uint8)).astype(bool)
    on_fill = np.zeros(n, bool)
    on_fill[np.unique(cc[icons & touch])] = True
    on_fill[0] = False
    icons = on_fill[cc]
    # Plan area: all district pixels and dropped icons, with street and creek symbols closed over.
    area = ((clean >= 0) | icons).astype(np.uint8)
    area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (FILL_GAP_PX, FILL_GAP_PX)))
    # Fill holes (labels and symbols wholly inside the plan area).
    cnts, _ = cv2.findContours(area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filled = np.zeros_like(area)
    cv2.drawContours(filled, cnts, -1, 1, thickness=cv2.FILLED)
    # Every unlabelled pixel in the area takes the nearest district.
    src = (clean < 0).astype(np.uint8)
    _, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.full(int(near.max()) + 1, -1)
    zero = src == 0
    lut[near[zero]] = clean[zero]
    out = lut[near]
    out[filled == 0] = -1
    return out


def _polys(mask: np.ndarray) -> list[Polygon]:
    cnts, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    if hier is None:
        return out
    for i, c in enumerate(cnts):
        if hier[0][i][3] != -1 or len(c) < 3:
            continue
        holes, ch = [], hier[0][i][2]
        while ch != -1:
            h = cv2.approxPolyDP(cnts[ch], TRACE_EPS_PX, True).reshape(-1, 2)
            if len(h) >= 3:
                holes.append(h + 0.5)
            ch = hier[0][ch][0]
        shell = cv2.approxPolyDP(c, TRACE_EPS_PX, True).reshape(-1, 2)
        if len(shell) < 3:
            continue
        p = shapely.make_valid(Polygon(shell + 0.5, holes))
        out.extend(q for q in getattr(p, "geoms", [p]) if isinstance(q, Polygon))
    return out


def main() -> None:
    pdf_path = trace.fetch_document(BOOK1["url"], tb.DOCS / BOOK1["file"], BOOK1["sha256"])
    sim, rep = georeference(pdf_path)
    rgb = _render(pdf_path)
    lab = classify(rgb)

    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
                 ["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]

    to_utm = lambda g: sim.geometry(shapely.transform(g, _px_to_pt))  # noqa: E731
    zones = {}
    for i, key in enumerate(DISTRICTS):
        polys = _polys(lab == i)
        if not polys:
            continue
        g = shapely.make_valid(to_utm(shapely.union_all(polys)))
        zones[key] = g
    plan_area = shapely.union_all(list(zones.values()))

    features, stats = [], []
    for key, g in zones.items():
        z = DISTRICTS[key]
        drawn_plan = g.area / ACRE_M2
        clip = g.intersection(site_utm).simplify(0.75)
        parts = [p for p in getattr(clip, "geoms", [clip]) if isinstance(p, Polygon) and p.area >= MIN_ZONE_ACRES * ACRE_M2]
        if not parts:
            stats.append((z["label"], z["category"], drawn_plan, 0.0, z["acres"]))
            continue
        clip = MultiPolygon(parts) if len(parts) > 1 else parts[0]
        acres = clip.area / ACRE_M2
        stats.append((z["label"], z["category"], drawn_plan, acres, z["acres"]))
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "zone",
                "category": z["category"],
                "label": z["label"],
                "source": f"traced: {BOOK1['title']}, {FIG}",
                "note": (f"{z['note']} About {acres:,.0f} acres on the EDC property as drawn ({drawn_plan:,.0f} acres "
                         f"across the plan area as traced; Table 3-2 gives ~{z['acres']:,} planning-area-wide). "
                         f"Approximate boundary: traced from a small-scale plan diagram."),
                "stage": STAGE,
                "accuracy": "approximate",
                "acres": round(acres, 1),
            },
            "geometry": mapping(tb.to_wgs(clip)),
        })

    covered = shapely.union_all([shape(f["geometry"]) for f in features])
    covered_utm = gpd.GeoSeries([covered], crs=4326).to_crs(UTM).iloc[0]
    site_ac = site_utm.area / ACRE_M2
    cov_ac = covered_utm.intersection(site_utm).area / ACRE_M2
    outside_plan = site_utm.difference(plan_area).area / ACRE_M2
    for lab_, cat, plan_ac, ac, tbl in stats:
        print(f"  {lab_:55s} {cat:11s} plan {plan_ac:7.0f} ac  on site {ac:7.1f} ac  (Table 3-2: {tbl:,})")
    print(f"[cnws] site {site_ac:,.0f} ac; zones cover {cov_ac:,.0f} ac; site outside the traced plan area "
          f"{outside_plan:,.1f} ac; plan area as traced {plan_area.area / ACRE_M2:,.0f} ac (Table 3-2: 5,046)")

    rep["note"] = (f"Figure 3-3 fitted to its existing arterials and freeways (vector road centrelines) against "
                   f"OpenStreetMap by trimmed ICP from a three-BART-station start: about {sim.scale:.1f} m per figure "
                   f"point, rotation {math.degrees(sim.rotation):.1f} deg, trimmed RMS {sim.rms_m:.0f} m (90% of road points "
                   f"within {rep['p90_m']:.0f} m). The diagram is drawn at about 1:51,000, so district edges are "
                   f"generalised by tens of metres. Zones clipped to the EDC property boundary.")
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                f"Land-use districts of the City of Concord's adopted Concord Reuse Project Area Plan (2012, part of "
                f"the General Plan), traced from Book One Figure 3-3 and clipped to the Navy's Economic Development "
                f"Conveyance property. The Area Plan covers about 5,046 acres, including the future regional park "
                f"outside this site. Streets and creeks drawn over the districts are folded into the nearest one; neighborhood "
                f"parks and plazas (not mapped by the plan) and the developer's unadopted 2026 concept plan aren't drawn. "
                f"About {outside_plan:,.0f} acres of the site have no district on the diagram (mainly the SR-4 / BART "
                f"corridor strip) and are left blank. Zones, not buildings; all boundaries approximate."),
            "note": "Land-use districts from the adopted 2012 Area Plan; the Specific Plan is next. Approximate zones, not buildings.",
            "sourceUrl": BOOK1["url"],
            "sourceLabel": "Area Plan land use diagram, 2012 (PDF)",
            "georeference": rep,
            "license": "Zone shapes: traced from a public City of Concord plan. Georeference: " + tb.OSM_LICENSE + ".",
            "documents": DOCUMENTS,
        },
        "features": features,
    }
    out = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[cnws] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.0f} KB, {len(features)} zones)")
    if "--debug" in sys.argv:
        np.save(config.ROOT / "data" / "raw" / "docs" / "cnws-labels.npy", lab)


if __name__ == "__main__":
    main()
