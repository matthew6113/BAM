"""North Bayshore: land-use zones traced from Google's approved North Bayshore Master Plan.

North Bayshore is a plan-scale project (SPEC section 7): it gets a boundary and land-use zones,
no buildings.

Source:
- North Bayshore Master Plan, April 2023 (Google LLC, PL-2021-248), approved by the Mountain
  View City Council on June 13, 2023 (Resolution 18810). Attachment 7 to the council report
  for that hearing (Legistar matter 7095, event 2504), from the city's Legistar file store.
  The city's project page links the same plan (mountainview.gov showpublisheddocument/7175),
  but mountainview.gov refuses scripted downloads, so the Legistar copy is used.
- Plan 4.1.2, "Land use (core master plan area)", p. 33, for everything it covers.
- Plan 4.1.1, "Land use", p. 32, only for the three parking sites outside Plan 4.1.2's frame:
  the Shoreline Amphitheatre Lot C garage (SA-P-1, which the plan notes lies outside the
  precise plan area) and the two garage sites on Marine Way.

Newest adopted wins: the master plan (2023) is newer and more specific than the North
Bayshore Precise Plan (adopted 2014, last amended Dec 7, 2021, Res. 18627), whose character
areas (Core, General, Edge, Gateway) cover the whole district and are not drawn here.

What this is and isn't:
- The plan's own legend classes, one feature per class: office, residential, hotel, public
  use, open space, parking, district central plant and the two flex classes. The plan says
  its "roadway alignments, and land use parcels are general depictions", so every zone is
  approximate.
- "Active uses" is a hatch along block edges for ground-floor retail and community space over
  the block's main use; it is not a zone, so those edges keep the block's use.
- Streets, the green loop trail and the pale "illustrative representation of the City's
  Gateway Master Plan" blocks are left out (the last is the city's separate Gateway plan).
- The Shoreline Amphitheatre itself ("area not subject to redevelopment") is left out.

Site boundary: this module also writes data/boundaries/north-bayshore.geojson, the plan's own
"Project area" line (the dash-dot line in both figures), and clips the zones to it.

Georeferencing: both figures are embedded rasters. Street centrelines at intersections
(midway between the curb lines in the base map) are matched to OpenStreetMap (via Overture)
with a least-squares similarity fit per figure; residuals are recorded.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_north_bayshore
"""

from __future__ import annotations

import json

import cv2
import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, box, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "north-bayshore"
STAGE = "entitled"
UTM = tb.UTM

PLAN = {
    "title": "North Bayshore Master Plan, April 2023 (approved June 13, 2023, Resolution 18810)",
    "url": "https://mountainview.legistar.com/gateway.aspx?M=F&ID=c8cc29fa-61b5-4936-bb9a-6705a30d063c.pdf",
    "page_url": "https://www.mountainview.gov/our-city/departments/community-development/planning/active-projects/google-projects/north-bayshore-master-plan",
    "city_copy": "https://www.mountainview.gov/home/showpublisheddocument/7175/638254594938830000",
    "agenda": "https://webapi.legistar.com/v1/mountainview/events/2504/eventitems",
    "council_report": "https://mountainview.legistar.com/gateway.aspx?M=F&ID=c5d191b7-b2bd-4e61-a167-15b425bc8c98.pdf",
    "sha256": "70504a7a9ee3dc4b820c776a29cc5d5c9f95e0b16fcf28e3a7a4a712db1f0a2f",
    "file": "nb-master-plan-2023-04.pdf",
}
PRECISE_PLAN = "https://www.mountainview.gov/home/showpublisheddocument/4406/638214110650830000"

FIGURES = {
    "4.1.2": {"page_index": 32, "printed_page": "33", "name": "Plan 4.1.2, Land use (core master plan area)",
              "size": (2239, 3864)},
    "4.1.1": {"page_index": 31, "printed_page": "32", "name": "Plan 4.1.1, Land use", "size": (2251, 3860)},
}

# Street centrelines in each raster (pixels), midway between the curb lines drawn either side,
# matched to where the same OpenStreetMap streets cross (mean of the crossings, for divided roads).
CONTROLS = {
    "4.1.2": {
        ("North Shoreline Boulevard", "Charleston Road"): (1840, 372),
        ("North Shoreline Boulevard", "Space Park Way"): (1830, 1168),
        ("North Shoreline Boulevard", "Pear Avenue"): (1828, 1543),
        ("Huff Avenue", "Charleston Road"): (912, 298),
    },
    "4.1.1": {
        ("North Shoreline Boulevard", "Amphitheatre Parkway"): (2420, 1047),
        ("North Shoreline Boulevard", "Charleston Road"): (2420, 1330),
        ("Marine Way", "Casey Avenue"): (679, 125),
        ("Marine Way", "Coast Avenue"): (686, 284),
    },
}
STREETS_BBOX = (-122.106, 37.405, -122.062, 37.437)

# Legend classes: the plan's legend label, our category, and the fill colours (RGB) in the
# raster (solid fills match the PDF's vector legend swatches; hatch colours sampled from the
# hatched blocks). Hatched classes are found by the density of their stripe colour.
CLASSES = {
    "office": {"label": "Office", "category": "office", "rgb": (0, 173, 239)},
    "residential": {"label": "Residential", "category": "residential", "rgb": (246, 194, 46)},
    "hotel": {"label": "Hotel", "category": "commercial", "rgb": (160, 101, 173)},
    "public": {"label": "Public use", "category": "civic", "rgb": (200, 238, 247)},
    "parking": {"label": "Parking", "category": "other", "rgb": (128, 129, 133)},
    "dcp": {"label": "District central plant", "category": "other", "rgb": (62, 150, 76)},
    "open": {"label": "Open space", "category": "open-space", "rgb": (193, 217, 103)},
    "flex_res": {"label": "Flex: parking, residential", "category": "other", "stripe": (91, 91, 91)},
    "flex_comm": {"label": "Flex: community use, district systems", "category": "civic", "stripe": (231, 150, 193)},
}
NOTES = {
    "office": "Office campus blocks; the plan allows 3,117,931 sq ft of office, including 1,814,681 sq ft rebuilt "
              "(Table 4.1.1, p. 34). Office buildings 4 to 8 stories (council report, June 13, 2023, p. 4).",
    "residential": "Up to 7,000 homes across the plan (Table 4.1.1, p. 34), 5 to 15 stories (council report, p. 4). "
                   "Hatched block edges in the figure mark ground-floor active uses.",
    "hotel": "Up to 525 hotel rooms in two locations, 10 to 13 stories (Table 4.1.1, p. 34; council report, p. 4).",
    "public": "Public use, as the figure's legend labels it; the figure doesn't name the use.",
    "parking": "Parking garages, including the Shoreline Amphitheatre Lot C garage (SA-P-1), which the plan notes "
               "is outside the precise plan area and needs its own development review permit (Plan 4.1.1, p. 32).",
    "dcp": "District central plant for the plan's district utility systems (130,000 sq ft, Table 4.1.1, p. 34).",
    "open": "Parks and open space; about 26.1 acres in the plan (Table 4.1.1, p. 34). Includes both dedicated public "
            "parks and privately owned, publicly accessible open space; the figure doesn't tell them apart.",
    "flex_res": "A flex block in the plan's legend: parking or residential.",
    "flex_comm": "A flex block in the plan's legend: community use or district systems.",
}
COLOR_TOL = 10  # max channel difference from a legend colour (the raster is crisp)
ACTIVE = (224, 14, 124)  # "active uses" hatch: reassigned to the block's main use
FILL_PX = {"ink": 6, "active": 10}  # how far line and hatch pixels take the nearest zone's class


def _image(pdf_path, fig: str) -> np.ndarray:
    import pypdfium2 as pdfium

    spec = FIGURES[fig]
    page = pdfium.PdfDocument(str(pdf_path))[spec["page_index"]]
    imgs = [o for o in page.get_objects() if o.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE]
    big = [o for o in imgs if o.get_px_size()[0] > 3000]
    if len(big) != 1:
        raise SystemExit(f"expected one map raster on the Plan {fig} page, found {len(big)}")
    rgb = np.asarray(big[0].get_bitmap(render=False).to_pil().convert("RGB"))
    if rgb.shape[:2] != spec["size"]:
        raise SystemExit(f"unexpected Plan {fig} raster size {rgb.shape}")
    return rgb


def georeference(streets: gpd.GeoDataFrame, fig: str) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), px in CONTROLS[fig].items():
        la = shapely.union_all(streets[streets["name"] == a].geometry.to_numpy())
        lb = shapely.union_all(streets[streets["name"] == b].geometry.to_numpy())
        pts = shapely.get_coordinates(la.intersection(lb))
        if not len(pts) or np.ptp(pts, axis=0).max() > 40:
            raise SystemExit(f"{a} and {b}: {len(pts)} crossings in OpenStreetMap, spread {np.ptp(pts, axis=0)}")
        src.append(px)
        dst.append(pts.mean(axis=0))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def classify(rgb: np.ndarray) -> dict[str, np.ndarray]:
    """Boolean mask per legend class, in raster pixels."""
    keys = list(CLASSES)
    img = rgb.astype(np.int16)

    def near(col):
        return np.abs(img - np.array(col, np.int16)).max(axis=2) <= COLOR_TOL

    solid = {k: near(c["rgb"]) for k, c in CLASSES.items() if "rgb" in c}
    stripes = {k: near(c["stripe"]) for k, c in CLASSES.items() if "stripe" in c}
    # Hatched blocks: where a stripe colour is dense, the stripes and the fill between them
    # (residential yellow, or the green that matches the plant's fill) belong to the flex class.
    win = (31, 31)
    flex = {}
    for k, m in stripes.items():
        dens = cv2.blur(m.astype(np.float32), win)
        under = solid["residential"] if k == "flex_res" else solid["dcp"]
        flex[k] = (dens > 0.15) & (m | under)
    label = np.full(rgb.shape[:2], -1, np.int16)
    for i, k in enumerate(keys):
        if k in solid:
            label[solid[k]] = i
    for k, m in flex.items():
        label[m] = keys.index(k)

    # Lines, text and the active-use hatch take the nearest zone's class (within a few px),
    # which also grows each zone to the middle of its outline. Light base-map colours don't.
    ink = (label < 0) & (rgb.min(axis=2) < 150)
    active = np.abs(img - np.array(ACTIVE, np.int16)).max(axis=2) <= 30
    _, nearest = cv2.distanceTransformWithLabels((label < 0).astype(np.uint8), cv2.DIST_L2, 5,
                                                 labelType=cv2.DIST_LABEL_PIXEL)
    dist = cv2.distanceTransform((label < 0).astype(np.uint8), cv2.DIST_L2, 5)
    seeds = np.flatnonzero(label.ravel() >= 0)
    filled = label.ravel()[seeds][nearest.ravel() - 1].reshape(label.shape)
    take = (ink & (dist <= FILL_PX["ink"])) | (active & (dist <= FILL_PX["active"]))
    label = np.where(take, filled, label)

    out = {}
    for i, k in enumerate(keys):
        m = (label == i).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
        out[k] = m > 0
    return out


def _polys(mask: np.ndarray, min_px: float):
    contours, hier = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    if hier is None:
        return Polygon()
    for i, c in enumerate(contours):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < min_px:
            continue
        holes, child = [], hier[0][i][2]
        while child != -1:
            if cv2.contourArea(contours[child]) >= min_px:  # text holes are filled
                holes.append(contours[child].reshape(-1, 2) + 0.5)
            child = hier[0][child][0]
        polys.append(shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5, holes)))
    return shapely.union_all(polys) if polys else Polygon()


# The plan's "Project area" is a thick dash-dot line. Per figure: the opening (px) that keeps
# it and drops thinner block outlines and the NBPP boundary's dashes, the closing disk (px)
# that joins its dashes, and half its stroke width (px).
PROJECT_LINE = {"4.1.2": {"open": 5, "join": 25, "half_width": 4},
                "4.1.1": {"open": 3, "join": 17, "half_width": 2}}
PLAN_ACRES = 153  # council report, June 13, 2023, p. 3: "Project Area: Approximately 153 acres."


def project_area(rgb: np.ndarray, masks: dict[str, np.ndarray], fig: str):
    """Areas enclosed by the plan's project-area line, in raster pixels.

    The line's dashes are joined by a dilation; each enclosed region that is mostly plan
    land-use colour (not base map) is a piece of the project area, grown back out to the
    middle of the line.
    """
    spec = PROJECT_LINE[fig]
    dark = (rgb.max(axis=2) < 90).astype(np.uint8)
    thick = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((spec["open"],) * 2, np.uint8))
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (spec["join"],) * 2)
    line = cv2.dilate(thick, disk)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(1 - line, connectivity=4)
    plan = np.zeros(dark.shape, bool)
    for m in masks.values():
        plan |= m
    h, w = dark.shape
    keep = np.zeros(dark.shape, np.uint8)
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if x == 0 or y == 0 or x + bw >= w or y + bh >= h or area < 2000:
            continue
        region = lab == i
        if plan[region].mean() > 0.3:
            keep[region] = 1
    grow = spec["join"] // 2 + spec["half_width"]
    keep = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1,) * 2))
    contours, _ = cv2.findContours(keep * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return shapely.union_all([shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5)) for c in contours])


def write_boundary(site_utm, sims: dict) -> None:
    acres = site_utm.area / tb.ACRE_M2
    lo, hi = sorted(s.rms_m for s in sims.values())
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "source": ("traced: North Bayshore Master Plan (April 2023), project area line in Plan 4.1.2, Land use "
                       "(core master plan area), p. 33, and Plan 4.1.1, Land use, p. 32 (Lot C and Marine Way sites)"),
            "sourceLabel": "master plan land use (PDF)",
            "sourceUrl": PLAN["url"],
            "accuracy": "traced",
            "accuracyShort": f"RMS {lo:.1f}-{hi:.1f} m",
            "accuracyNote": (
                f"The plan's own project area line, traced from its land use figures and placed on OpenStreetMap "
                f"street crossings (RMS {sims['4.1.2'].rms_m:.1f} m for Plan 4.1.2, {sims['4.1.1'].rms_m:.1f} m for "
                f"Plan 4.1.1). {acres:.1f} acres as drawn; the council report (June 13, 2023, p. 3) gives "
                f"approximately {PLAN_ACRES} acres. The line takes in the internal streets and, at Lot C, the "
                f"Shoreline Amphitheatre, which the plan marks as not subject to redevelopment."),
            "license": "Shape traced from a public City of Mountain View record (council attachment); "
                       "placement: " + tb.OSM_LICENSE + ".",
            "georeference": {f"plan_{fig.replace('.', '_')}": s.report() for fig, s in sims.items()},
        },
        "features": [{"type": "Feature", "properties": {"kind": "site", "name": "Project site"},
                      "geometry": mapping(tb.to_wgs(site_utm))}],
    }
    path = tb.OUT / f"{PROJECT_ID}.geojson"
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[north-bayshore] wrote {path.relative_to(config.ROOT)}: {acres:.1f} acres as drawn "
          f"(plan: about {PLAN_ACRES})")


def main() -> None:
    pdf_path = trace.fetch_document(PLAN["url"], tb.DOCS / PLAN["file"], PLAN["sha256"])
    streets = tb.streets("nb-north_bayshore", STREETS_BBOX)
    streets = streets[streets["subtype"] == "road"]
    zones: dict[str, list] = {k: [] for k in CLASSES}
    areas = []
    sims, core_frame = {}, None
    for fig in ("4.1.2", "4.1.1"):
        rgb = _image(pdf_path, fig)
        sim = georeference(streets, fig)
        sims[fig] = sim
        print(f"[north-bayshore] Plan {fig} georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} "
              f"intersections, scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f} deg")
        h, w = rgb.shape[:2]
        frame = sim.geometry(box(0, 0, w, h))
        masks = classify(rgb)
        # Drop specks under ~400 sq m. On Plan 4.1.1 only whole garage sites are wanted (each
        # over 3 acres); smaller grey shapes there are amphitheatre structures in the base map.
        min_px = (400 if fig == "4.1.2" else 4000) / sim.scale**2
        pa = sim.geometry(project_area(rgb, masks, fig))
        if fig == "4.1.1":  # only the sites outside Plan 4.1.2's frame
            pa = shapely.union_all([p for p in getattr(pa, "geoms", [pa])
                                    if p.intersection(core_frame).area < 0.05 * p.area])
        print(f"[north-bayshore]   project area from Plan {fig}: {len(getattr(pa, 'geoms', [pa]))} pieces, "
              f"{pa.area / tb.ACRE_M2:.1f} ac")
        areas.append(pa)
        for k, m in masks.items():
            if fig == "4.1.1" and k != "parking":
                continue  # Plan 4.1.1 is used only for the parking sites outside Plan 4.1.2
            g = sim.geometry(_polys(m, min_px))
            if fig == "4.1.1":
                g = shapely.union_all([p for p in getattr(g, "geoms", [g])
                                       if p.intersection(core_frame).area < 0.05 * p.area])
            if not g.is_empty:
                zones[k].append(g)
        if fig == "4.1.2":
            core_frame = frame.buffer(-20)

    # Joining the dashes leaves shallow scallops along the line; a 4 m closing and a 2 m
    # opening smooth them.
    site = shapely.union_all(areas).buffer(4, join_style="mitre").buffer(-6, join_style="mitre")
    site = site.buffer(2, join_style="mitre")
    site_utm = trace.as_multipolygon(shapely.make_valid(site.simplify(0.75)))
    write_boundary(site_utm, sims)

    features = []
    for k, parts in zones.items():
        if not parts:
            continue
        g = shapely.make_valid(shapely.union_all(parts))
        inside = g.intersection(site_utm)
        share = inside.area / g.area
        g = trace.as_multipolygon(shapely.make_valid(inside.simplify(0.6)))
        g = shapely.MultiPolygon([p for p in g.geoms if p.area >= 500])  # clipping slivers
        if g.is_empty:
            continue
        c = CLASSES[k]
        fig = "Plan 4.1.1, p. 32 (garages outside Plan 4.1.2) and Plan 4.1.2, p. 33" if k == "parking" \
            else f"{FIGURES['4.1.2']['name']}, p. 33"
        print(f"[north-bayshore]   {c['label']:>38}: {g.area / tb.ACRE_M2:6.2f} ac in {len(g.geoms)} parts "
              f"({share:.0%} of the traced zone inside the project area)")
        features.append({"type": "Feature", "properties": {
            "kind": "zone",
            "category": c["category"],
            "label": c["label"],
            "stage": STAGE,
            "source": f"traced: North Bayshore Master Plan (April 2023), {fig}",
            "note": NOTES[k] + " Approximate: the plan calls its land use parcels general depictions.",
        }, "geometry": mapping(tb.to_wgs(g))})

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Land-use zones traced from the land use plans in Google's North Bayshore Master Plan (April 2023), "
                "approved by the Mountain View City Council in June 2023: office, residential, hotel, public use, open "
                "space, parking, the district central plant and two flex classes, clipped to the project "
                "area line as the plan draws it. "
                "The plan calls these general depictions, so every edge is approximate. Ground-floor active uses, "
                "streets, the green loop trail, the Shoreline Amphitheatre and the city's separate Gateway plan are "
                "left out. Zones, not buildings."
            ),
            "note": "Land uses from the approved 2023 master plan, approximate; zones, not buildings.",
            "sourceUrl": PLAN["url"],
            "sourceLabel": "Master plan land use, 2023 (PDF)",
            "georeference": {f"plan_{fig.replace('.', '_')}": s.report() for fig, s in sims.items()},
            "license": "Zones: traced from a public City of Mountain View record (council attachment). "
                       "Georeference: " + tb.OSM_LICENSE + ".",
            "documents": [PLAN["url"], PLAN["page_url"], PLAN["city_copy"], PLAN["agenda"], PLAN["council_report"],
                          PRECISE_PLAN],
        },
        "features": features,
    }
    path = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[north-bayshore] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
