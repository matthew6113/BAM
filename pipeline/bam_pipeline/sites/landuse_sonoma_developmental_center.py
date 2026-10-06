"""Sonoma Developmental Center: proposed land-use zones, traced from the county's Notice of Preparation.

Nothing here is approved. The County of Sonoma adopted an SDC Specific Plan in December 2022
(EIR SCH 2022020222), but after the Superior Court's October 2024 ruling the Board of
Supervisors decertified the EIR and rescinded the plan (Dec 3, 2024). That plan is superseded
and is not drawn. The newest official land-use map is in the county's Notice of Preparation for
the new EIR (CEQAnet SCH 2025081410, Aug 29, 2025), which covers a revised SDC Campus Specific
Plan and Eldridge Renewal's 990-home Builder's Remedy application:

- Figure 4 "Specific Plan Update Land Use Diagram" (PDF p. 22): six land-use classes inside the
  core campus (Low/Medium Density Residential, Medium/Flex Density Residential, Flex Zone,
  Employment, Park, Open Space), with the wildfire buffer around it. This is what is traced.
- Figure 5 "Eldridge Renewal Project Site Plan" (PDF p. 23) uses the same classes and names
  the uses in the Employment areas; with the NOP text (pp. 8-9) it is used only to label the
  north-west Employment block as the hotel and conference center and the western one as the
  Main Building and Innovation + Small Business Center.

Zone -> category:
  Low/Medium Density Residential -> residential   Medium/Flex Density Residential -> residential
  Flex Zone -> mixed-use (apartments and mixed-use buildings around the Central Green, NOP pp. 7-8)
  Employment (hotel and conference center, north-west) -> commercial
  Employment (Main Building, Innovation + Small Business Center, west) -> office
  Park -> open-space   Open Space -> open-space
  Wildfire buffer (the project area outside the core campus) -> open-space (managed open space, NOP p. 6)

Streets are drawn white in the figure, between the zones, so they are left out of every zone.

Georeferencing: Figure 4 is drawn on the same base map and in the same pixel frame as Figure 3
(PDF p. 21), from which the site boundary was traced (traced_boundaries.build_sdc). The frame
match is checked by phase correlation on the base map outside the campus, and Figure 3's fit is
repeated here: street crossings for a start, then trimmed ICP of the figure's building outlines
to Overture (OpenStreetMap) building footprints.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_sonoma_developmental_center
"""

from __future__ import annotations

import json

import cv2
import numpy as np
import shapely
import shapely.affinity
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "sonoma-developmental-center"
STAGE = "entitlement"
ACRE_M2 = tb.ACRE_M2

NOP = tb.SDC_NOP  # same file the site boundary was traced from (cached as data/raw/docs/sdc-nop-2025081410.pdf)
CEQANET = "https://ceqanet.lci.ca.gov/2025081410"
SUPERSEDED_EIR = "https://ceqanet.lci.ca.gov/2022020222"
FIG4_PAGE = 21  # PDF p. 22
FIG4_TITLE = "Figure 4, Specific Plan Update Land Use Diagram, p. 22"

HEIGHTS = ("The NOP gives typical heights of two to three stories for apartments, mixed-use buildings and townhomes, "
           "one to three for detached homes and three for co-housing (pp. 7-8); it doesn't tie heights to districts.")

# In-map fill colours (sampled from the figure; fills are flat except where hillshade shows through).
ZONES = {
    "LMDR": {"rgb": (247, 244, 137), "label": "Proposed low/medium density residential", "category": "residential",
             "note": "Figure 4's lower-density housing district. The NOP doesn't assign housing types to districts; "
                     "it describes 368 detached homes (courtyard, hillside, large and small) in compact neighbourhoods "
                     "throughout the core campus (p. 8). " + HEIGHTS},
    "MFDR": {"rgb": (249, 214, 148), "label": "Proposed medium/flex density residential", "category": "residential",
             "note": "Figure 4's higher-density housing district. The NOP doesn't assign housing types to districts; "
                     "it places townhomes along Arnold Drive, at the east end of the Central Green and north and south "
                     "of the Main Building (p. 7). " + HEIGHTS},
    "FLEX": {"rgb": (205, 172, 215), "label": "Proposed flex zone", "category": "mixed-use",
             "note": "Apartments and mixed-use buildings with ground-floor commercial uses around the Central Green and "
                     "major streets, grouped around the Central Green (NOP pp. 7-8). Category mixed-use: housing with "
                     "ground-floor commercial uses. " + HEIGHTS},
    "EMP": {"rgb": (247, 149, 146), "label": "Proposed employment", "category": "office", "note": ""},
    "PARK": {"rgb": (99, 181, 53), "label": "Proposed park", "category": "open-space",
             "note": "Parks, including the Central Green. The NOP gives about 67 acres of parks, recreation areas and "
                     "open space in all, with walking trails, sports fields, playgrounds, dog parks, a community "
                     "center and gym, and riparian corridors (p. 7)."},
    "OS": {"rgb": (189, 217, 169), "label": "Proposed open space", "category": "open-space",
           "note": "Open space along Sonoma Creek and Mill Creek, where the plan would set riparian setbacks (NOP p. 6). "
                   "The NOP gives about 67 acres of parks, recreation and open space in all (p. 7)."},
}
EMPLOYMENT = {
    "hotel": {"label": "Proposed employment: hotel and conference center", "category": "commercial",
              "note": "A 150-key boutique hotel with conference facilities, amenities and a parking structure in the "
                      "north-west of the core campus, about 120,000 sq ft in all (NOP pp. 7, 9; named on Figure 5, "
                      "p. 23). Category commercial: visitor-serving."},
    "west": {"label": "Proposed employment: Main Building and innovation center", "category": "office",
             "note": "The historic Main Building, reused for office, retail and entertainment, and the Small Business + "
                     "Innovation Center behind it (two reused shops and three new buildings for office, R&D, creative "
                     "services and micro-manufacturing) (NOP pp. 8-9; named on Figure 5, p. 23). Category office. "
                     "About 130,000 sq ft of commercial uses project-wide (p. 7)."},
}
HOTEL_MAX_ROW = 1800  # employment pieces above this image row (Laurel Street to A Street) are the hotel block
MAX_DIST = 18  # colour distance after a brightness scale (hillshade)
WHITE_MIN, WHITE_SAT = 236, 14  # streets
EDGE_PX = 30  # half-width of the band along the core line where white is the dash gaps
STREET_MIN_PX = 40000  # about 2,000 m2: keeps the loop road south of Mill Creek, drops label haloes
FRAME_CHECK = [(0, 800, 3800, 5100), (4300, 5500, 1500, 4000)]  # base-map windows outside the campus (y0, y1, x0, x1)


def _fig4_image(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG4_PAGE]
    text = page.get_textpage().get_text_range()
    if "Figure 4" not in text or "Land Use Diagram" not in text:
        raise SystemExit("sonoma-developmental-center: Figure 4 land use diagram is not on p. 22")
    for obj in page.get_objects():
        if obj.type == 3:
            bmp = obj.get_bitmap(render=False)
            if (bmp.width, bmp.height) == tb.SDC_IMAGE_SIZE:
                return np.asarray(bmp.to_pil().convert("RGB"))[:tb.SDC_MAP_BOTTOM].astype(int)
    raise SystemExit("Figure 4 image not found")


def frame_check(fig3: np.ndarray, fig4: np.ndarray) -> dict:
    """Figures 3 and 4 share a pixel frame: phase correlation of the base map outside the campus."""
    g3, g4 = fig3.mean(axis=2).astype(np.float32), fig4.mean(axis=2).astype(np.float32)
    out = []
    for y0, y1, x0, x1 in FRAME_CHECK:
        (dx, dy), resp = cv2.phaseCorrelate(g3[y0:y1, x0:x1], g4[y0:y1, x0:x1])
        if abs(dx) > 2 or abs(dy) > 2 or resp < 0.3:
            raise SystemExit(f"Figure 4 is not in Figure 3's frame (shift {dx:.1f}, {dy:.1f} px, response {resp:.2f})")
        out.append({"window_px": [x0, y0, x1, y1], "shift_px": [round(float(dx), 2), round(float(dy), 2)],
                    "response": round(float(resp), 2)})
    return {"method": "phase correlation of Figure 3 and Figure 4 base maps", "windows": out}


def georeference(fig3: np.ndarray):
    """traced_boundaries.build_sdc's fit, repeated: crossings to start, then building outlines by trimmed ICP."""
    mx, mn = fig3.max(axis=2), fig3.min(axis=2)
    g = tb.streets("sdc", tb.SDC_BBOX)
    src, dst, labels = [], [], []
    for (a, b), xy in tb.SDC_CONTROLS.items():
        src.append(xy)
        dst.append(tb.intersection(g, a, b))
        labels.append(f"{a} / {b}")
    init = trace.fit_similarity(src, dst, labels)
    grey = ((np.abs(fig3 - tb.SDC_BUILDING_GREY).max(axis=2) <= tb.SDC_BUILDING_TOL) & (mx - mn < 10)).astype(np.uint8)
    grey = cv2.morphologyEx(grey, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    edge = np.vstack([c.reshape(-1, 2)[::4] for c in contours if cv2.contourArea(c) >= 400]).astype(float) + 0.5
    b = tb.buildings("sdc", tb.SDC_BBOX)
    near = shapely.box(*init.geometry(shapely.MultiPoint(edge)).bounds).buffer(100)
    target = shapely.union_all(b[b.intersects(near)].boundary.to_numpy())
    keep = 0.7
    sim, d = tb.icp(edge, [target], np.zeros(len(edge), int), init, keep, iterations=100)
    rep = tb.icp_report(sim, d, keep, "Figure 3 building outlines vs Overture (OpenStreetMap) buildings")
    check = np.linalg.norm(sim.apply(src) - np.asarray(dst), axis=1)
    rep["street_crossings_m"] = {lab: round(float(r), 1) for lab, r in zip(labels, check)}
    return sim, rep, d, check


def _mask_polys(mask: np.ndarray, min_px: int = 400):
    contours, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hier is None:
        return shapely.MultiPolygon()
    polys = []
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


def core_campus_px(fig4: np.ndarray) -> Polygon:
    """Figure 4's black dashed core-campus line, back to its centre (as build_sdc does on Figure 3), with the
    notches left between the dashes closed."""
    mx, mn = fig4.max(axis=2), fig4.min(axis=2)
    black = ((mx < tb.SDC_BLACK_MAX) & (mx - mn < tb.SDC_BLACK_SAT)).astype(np.uint8)
    core = tb._enclosed(black, 31, tb.SDC_INSIDE_PX).buffer(-(31 // 2 + tb.SDC_CORE_HALF_PX)).buffer(-40).buffer(40)
    return trace.largest_polygon(core.buffer(30).buffer(-30).simplify(3))


def trace_fig4(rgb: np.ndarray, core_px: Polygon) -> dict:
    """Label each pixel of the core campus with its zone; streets (white) stay unlabelled."""
    keys = list(ZONES)
    pal = np.array([ZONES[k]["rgb"] for k in keys], np.float32)
    x0, y0, x1, y1 = (int(v) for v in core_px.buffer(20).bounds)
    x0, y0 = max(x0, 0), max(y0, 0)
    im = rgb[y0:y1, x0:x1].astype(np.float32)
    lab = np.full(im.shape[:2], -1, np.int16)
    for r in range(0, im.shape[0], 200):
        c = im[r:r + 200]
        s = np.clip((c[:, :, None, :] * pal).sum(3) / (pal ** 2).sum(1), 0.7, 1.08)  # hillshade brightness
        d = np.linalg.norm(c[:, :, None, :] - s[..., None] * pal, axis=3)
        lab[r:r + 200] = np.where(d.min(2) <= MAX_DIST, d.argmin(2), -1)
    # Drop specks (anti-aliased edges and text that happen to match a fill).
    for i in range(len(keys)):
        m = (lab == i).astype(np.uint8)
        _, cc, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
        lab[np.isin(cc, np.nonzero(stats[:, cv2.CC_STAT_AREA] < 300)[0]) & (m > 0)] = -1
    # Streets: white, closed to take in the street-name lettering drawn on them.
    mx, mn = im.max(axis=2), im.min(axis=2)
    street = ((mn >= WHITE_MIN) & (mx - mn <= WHITE_SAT)).astype(np.uint8)
    # The white gaps of the dashed core-campus line aren't streets.
    ring = np.round(np.asarray(core_px.exterior.coords) - (x0, y0)).astype(np.int32)
    cv2.polylines(street, [ring], True, 0, 2 * EDGE_PX)
    street = cv2.morphologyEx(street, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    street = cv2.morphologyEx(street, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    # Isolated white bits (the haloes around creek names in the open space) aren't streets.
    _, cc, stats, _ = cv2.connectedComponentsWithStats(street, connectivity=8)
    street[np.isin(cc, np.nonzero(stats[:, cv2.CC_STAT_AREA] < STREET_MIN_PX)[0])] = 0
    core = np.zeros(lab.shape, np.uint8)
    cv2.fillPoly(core, [ring], 1)
    # Line work inside a zone (creeks, lettering, the dashed core line) takes the nearest zone.
    zone = lab >= 0
    _, idx = cv2.distanceTransformWithLabels((~zone).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(zone)
    lookup = np.full(idx.max() + 1, -1)
    lookup[idx[ys, xs]] = lab[ys, xs]
    filled = np.where((core > 0) & ((street == 0) | zone), lookup[idx], -1)
    out = {}
    for i, k in enumerate(keys):
        m = cv2.morphologyEx((filled == i).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        out[k] = shapely.affinity.translate(_mask_polys(m), x0, y0)
    return out


def _clean(g, min_acres: float = 0.05):
    parts = []
    for p in getattr(g, "geoms", [g]):
        if not isinstance(p, Polygon) or p.area < min_acres * ACRE_M2:
            continue
        parts.append(Polygon(p.exterior, [h for h in p.interiors if Polygon(h).area >= min_acres * ACRE_M2]))
    if not parts:
        return None
    return parts[0] if len(parts) == 1 else shapely.MultiPolygon(parts)


def main() -> None:
    import geopandas as gpd

    pdf = trace.fetch_document(NOP["url"], tb.DOCS / NOP["file"], NOP["sha256"])
    fig3 = tb._sdc_image(pdf)
    fig4 = _fig4_image(pdf)
    frame = frame_check(fig3, fig4)
    sim, rep, d, check = georeference(fig3)
    print(f"[sdc landuse] fit scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f} deg, trimmed RMS "
          f"{sim.rms_m:.2f} m (median {np.median(d):.2f} m); street crossings median {np.median(check):.1f} m, "
          f"max {check.max():.1f} m; Figure 4 frame shift {[w['shift_px'] for w in frame['windows']]} px")

    site_wgs = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
                     ["features"][0]["geometry"])
    site = gpd.GeoSeries([site_wgs], crs=4326).to_crs(tb.UTM).iloc[0]

    core_px = core_campus_px(fig4)
    core = sim.geometry(core_px).buffer(0).intersection(site)

    traced = trace_fig4(fig4, core_px)
    zones = {k: sim.geometry(g).buffer(0).intersection(core) for k, g in traced.items()}
    emp = zones.pop("EMP")
    hotel_cut = sim.geometry(shapely.box(0, 0, tb.SDC_IMAGE_SIZE[0], HOTEL_MAX_ROW))
    emp_parts = {"hotel": emp.intersection(hotel_cut), "west": emp.difference(hotel_cut)}
    buffer_zone = site.difference(core.buffer(0.5))

    tol = 0.75  # m (about 3 figure pixels)
    specs = [(k, ZONES[k], zones[k]) for k in ("LMDR", "MFDR", "FLEX")]
    specs += [(f"EMP-{k}", {**ZONES["EMP"], **v}, emp_parts[k]) for k, v in EMPLOYMENT.items()]
    specs += [(k, ZONES[k], zones[k]) for k in ("PARK", "OS")]
    specs.append(("BUFFER", {"label": "Proposed wildfire buffer", "category": "open-space",
                             "note": "Managed open space ringing the core campus on the west, north and east: defensible "
                                     "space with fuel-management rules and protection for the Sonoma Valley Wildlife "
                                     "Corridor (NOP pp. 3, 6; 49 acres). Drawn as the project area outside Figure 4's "
                                     "core campus line."}, buffer_zone))
    features, drawn = [], {}
    for key, spec, geom in specs:
        geom = _clean(geom.simplify(tol))
        if geom is None:
            raise SystemExit(f"{key}: nothing traced")
        acres = geom.area / ACRE_M2
        drawn[key] = acres
        inside = geom.intersection(site).area / geom.area
        if inside < 0.95:
            raise SystemExit(f"{key}: only {inside:.0%} inside the site")
        features.append({"type": "Feature", "properties": {
            "kind": "zone",
            "category": spec["category"],
            "label": spec["label"],
            "source": f"traced: {NOP['title']}, {FIG4_TITLE}",
            "note": (f"{spec['note']} About {acres:,.1f} acres as drawn, streets excluded. Approximate: traced from "
                     f"the county's figure. Proposed, not approved."),
            "stage": STAGE,
            "accuracy": "approximate",
        }, "geometry": mapping(tb.to_wgs(geom))})
        print(f"  {key:10s} {spec['category']:12s} {acres:7.1f} ac")

    core_acres = core.area / ACRE_M2
    park_os = drawn["PARK"] + drawn["OS"]
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Proposed land use, nothing approved: the six land-use classes of the revised SDC Campus Specific Plan "
                "traced from Figure 4 (Specific Plan Update Land Use Diagram, p. 22) of the County of Sonoma's Notice of "
                "Preparation (SCH 2025081410, Aug 2025), with the two Employment areas named from Figure 5 (the "
                "Eldridge Renewal site plan) and the NOP text, and the wildfire buffer as the project area outside the "
                f"core campus. Streets, drawn white in the figure, are left out of the zones (about {core_acres - sum(v for k, v in drawn.items() if k != 'BUFFER'):.0f} "
                f"of the core campus's {core_acres:.0f} acres as drawn). The 2022 specific plan, rescinded in December "
                "2024, is not drawn. No buildings are drawn; all zone edges are approximate."),
            "note": "Proposed land use from the county's 2025 Notice of Preparation; nothing is approved. Approximate zones, not buildings.",
            "sourceUrl": NOP["url"],
            "sourceLabel": "Notice of preparation, 2025 (PDF)",
            "georeference": {
                "fit": rep,
                "frame_check": frame,
                "note": (f"Figure 4 shares Figure 3's pixel frame (phase-correlation shift under 2 px). Figure 3 fitted "
                         f"to Overture (OpenStreetMap) building footprints by trimmed ICP: {sim.scale:.3f} m per pixel, "
                         f"RMS {sim.rms_m:.1f} m over the closest 70% of {len(d):,} building-edge points; six street "
                         f"crossings within {check.max():.0f} m. Zones clipped to the site boundary in "
                         "data/boundaries, traced from the same figures."),
            },
            "acresCheck": {
                "parks_and_open_space_drawn": round(park_os, 1),
                "parks_and_open_space_nop": 67,
                "buffer_drawn": round(drawn["BUFFER"], 1),
                "buffer_nop": tb.SDC_BUFFER_ACRES,
                "core_drawn": round(core_acres, 1),
                "core_nop": tb.SDC_CORE_ACRES,
            },
            "superseded": ("SDC Specific Plan adopted Dec 2022 (EIR SCH 2022020222), rescinded with its EIR decertified "
                           "on Dec 3, 2024; not drawn."),
            "license": ("Zone shapes: traced from a public County of Sonoma CEQA notice. Georeference: "
                        + tb.OSM_LICENSE + "."),
            "documents": [CEQANET, NOP["url"]],
        },
        "features": features,
    }
    out = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tb._round(fc, 6), indent=1) + "\n")
    print(f"[sdc landuse] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.0f} KB); site "
          f"{site.area / ACRE_M2:.0f} ac, core {core_acres:.0f} ac, parks + open space {park_os:.0f} ac (NOP 67)")


if __name__ == "__main__":
    main()
