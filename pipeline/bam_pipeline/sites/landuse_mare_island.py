"""Mare Island: land-use designations of the adopted Mare Island Specific Plan.

Mare Island is a plan-scale project (SPEC §7, "Massing rules"): it gets a boundary and land-use
zones only, no buildings. The zones drawn here are the ADOPTED plan's, not the new plan's: the Mare
Island Company's new specific plan (file SPA24-0001, first draft Oct 10, 2024) is only a draft under
City review, so nothing from it is drawn.

Source: the City of Vallejo's posted Mare Island Specific Plan (adopted March 1999, amended and
restated December 2005, amended July 2007, June 2008, June 2013 and August 2013; cover of the plan
text, VJO itemId 19272509). The plan text holds placeholder pages for its figures (Figure 3-1 "Land
Use" is a blank p. 48, PDF p. 70); the figures themselves are in the City's companion "Specific Plan
Graphics" file (VJO itemId 19272505, "Mare Island Specific Plan 11x17 Figures.pdf"), where PDF p. 9
is "Figure 3.1 Land Use, Mare Island Specific Plan, Revised January 2008". That is the newest land-use
map the City posts for the adopted plan; the 1999 plan's figure (itemId 19272507) is superseded and
not used. The City's Oct 2025 infrastructure assessment cites an "Amended August 2014" plan; no 2014
text or figure is posted, so the January 2008 figure is drawn and the gap noted.

No GIS layer of the plan's land-use designations exists on the City's ArcGIS server
(portal.cityofvallejo.net, CityGIS_Viewer/Planning_Development_Services, checked 2026-10-06): layers
65, 66, 67 and 69 are single outline polygons of the plan area, layer 3 is the SP-4 zoning area, and
the General Plan 2040 layers (2, 5) carry Mare Island as one "District - Mare Island" / "Mare Island"
designation that defers to the specific plan. So the figure is traced.

The figure is a scanned colour raster. Each pixel is classed by its fill colour against the
legend; line work, text and the diagrammatic building masses inside a zone go to the nearest zone.
Two legend classes are white (Industrial and Wetlands): white areas are told apart by the plan's
Reuse Area lines, using seeds in Reuse Areas 1A, 1B, 5 and 10A (industrial in the figure) and the
federal transfer parcels the figure labels Army Reserve (10B) and Forest Service, which the plan says
are not subject to it (§3.2.1, PDF p. 73). Every other white area is Wetlands. The legend's medium and
low density residential shades differ by about 15 RGB levels and the scan doesn't separate them
(the residential blocks form one colour cluster), so they are one zone. Retail/commercial is a point
symbol (two asterisks, in Reuse Areas 2A and 4), not an area, so it isn't drawn.

Category mapping (plan §3.2, PDF pp. 73-79):
  Mixed-use -> mixed-use (office/R&D, light industrial, retail, warehousing; housing allowed)
  Historic core -> mixed-use (Reuse Area 4: civic, retail, office, light industrial, museum)
  Industrial -> industrial          Educational / civic -> civic
  Residential high density, Residential medium/low density -> residential
  Open space, Golf course, Restricted open space, Restricted open space / former dredge ponds,
  Wetlands -> open-space
  Federal land (Army Reserve, Forest Service) -> other (exempt from the plan)

Georeference: the figure's diagrammatic building masses (grey) are fitted to Overture building
footprints (mostly OpenStreetMap) by trimmed ICP, starting from two street intersections (A Street
and G Street at Railroad Avenue). Zones are clipped to the site boundary (Vallejo GIS layer 67,
data/boundaries/mare-island.geojson), which leaves out the strait-side strip and wetland edges the
figure draws beyond it.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_mare_island
"""

from __future__ import annotations

import json
import math

import cv2
import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "mare-island"
STAGE = "entitlement"  # data/projects.json
ACRE_M2 = tb.ACRE_M2
OUT = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"

VJO = "https://www.cityofvallejo.net/common/pages/DisplayFile.aspx?itemId="
FIGURES = {
    "title": "Mare Island Specific Plan graphics (11x17 figures), City of Vallejo",
    "url": VJO + "19272505",
    "sha256": "4e806dd6cd3c4bb0d65b2d0832dcf6e07feb5f2049b1bf735124b266877d4bb5",
    "file": "mi-misp-figures.pdf",
}
PLAN = {
    "title": "Mare Island Specific Plan (adopted 1999, amended and restated 2005, amended through Aug 2013)",
    "url": VJO + "19272509",
    "sha256": "067812d6809296511d0fcc1637bad4a6c8446cbc532dd2bcd63c206675fd8464",
    "file": "mi-misp-2013.pdf",
}
DOCS_PAGE = "https://www.cityofvallejo.net/our_city/about_vallejo/mare_island/mare_island_planning_documents"
GIS = "https://portal.cityofvallejo.net/arcgis/rest/services/CityGIS_Viewer/Planning_Development_Services/MapServer"
FIG_PAGE = 8  # PDF p. 9, "Figure 3.1 Land Use, Mare Island Specific Plan, Revised January 2008"
FIG_LABEL = "Figure 3.1 Land Use (revised January 2008), PDF p. 9"
RENDER_SCALE = 2  # 144 dpi; the scan underneath is about 100 dpi
MAP_TOP = 300  # rows above this are the bay and the legend (render pixels)
LEGEND_BOTTOM, LEGEND_RIGHT = 490, 340  # the legend's lower swatches, over the bay

# In-map fill colours (cluster centres of the scan; the legend swatches print slightly differently).
ZONES = {
    "MU": {"rgb": [(251, 212, 18), (245, 212, 86)], "label": "Mixed-use", "category": "mixed-use",
           "note": "Office/R&D, light industrial, retail commercial and warehousing; residential uses are also "
           "allowed (plan §3.2.8, PDF p. 76). Reuse Areas 2A (Town Center, with a 50,000 sq ft retail centre at "
           "Railroad Avenue and G Street), 2B, 3A and 3B (§3.3.2, PDF p. 81)."},
    "HC": {"rgb": [(243, 152, 38)], "label": "Historic core", "category": "mixed-use",
           "note": "Reuse Area 4: civic, retail and office commercial, light industrial and visitor uses in "
           "historic buildings, with a waterfront plaza (plan §3.3.3 and §3.5.7, PDF pp. 81-82, 100-101). "
           "Category mixed-use."},
    "HD": {"rgb": [(220, 132, 118)], "label": "Residential high density", "category": "residential",
           "note": "Less than 2,500 sq ft of land per home, more than 17.4 homes per acre (plan §3.2.7, PDF p. 74)."},
    "RES": {"rgb": [(242, 221, 173), (247, 235, 190), (252, 241, 199)], "label": "Residential medium and low density", "category": "residential",
            "note": "The figure's medium (8.7-17.4 homes per acre) and low (under 8.7 homes per acre) density "
            "shades (plan §3.2.7, PDF pp. 74-75) can't be told apart in the scanned map, so they are one zone. "
            "The plan's residential program is 1,400 homes in all (PDF p. 80)."},
    "CIV": {"rgb": [(10, 184, 247)], "label": "Educational / civic", "category": "civic",
            "note": "Public and quasi-public uses: government services, utilities, schools and colleges, "
            "cultural facilities (plan §3.2.6, PDF p. 74). Mainly Reuse Area 9 (University Area, Touro University)."},
    "OS": {"rgb": [(168, 203, 110), (187, 212, 137)], "label": "Open space", "category": "open-space",
           "note": "Parks and open space, including the Community Park (Reuse Area 7) and the Regional Park "
           "(Reuse Area 12, 176 acres) (plan §3.4, PDF pp. 87-93)."},
    "GOLF": {"rgb": [(238, 243, 207)], "label": "Golf course", "category": "open-space",
             "note": "Reuse Area 11, the existing 18-hole course, 172 acres (plan §3.4.3, PDF p. 93)."},
    "RDP": {"rgb": [(41, 119, 78), (60, 129, 87)], "label": "Restricted open space / former dredge ponds",
            "category": "open-space",
            "note": "Inactive dredge ponds, restricted to managed wetlands, open space or conservation uses under "
            "the Three Party Dredge Pond Agreement (plan §3.2.2, PDF p. 73); 922 acres in Table 3-2 (PDF p. 96)."},
    "ROS": {"rgb": [(20, 161, 165)], "label": "Restricted open space", "category": "open-space",
            "note": "Reuse Area 13 (Open Space/Recreation), a landfill site; about 32 acres of it planned as a "
            "city park (plan §3.4.3, PDF p. 93; Table 3-2, PDF p. 96)."},
}
WHITE_ZONES = {
    "IND": {"label": "Industrial", "category": "industrial",
            "seeds": {"1A": (2100, 1080), "1B": (2230, 890), "5": (1065, 1075), "5 (by Dry Dock 2)": (1220, 1160),
                      "10A": (545, 1105)},
            "note": "Heavy industry, warehouse/distribution, light industrial, construction and equipment services "
            "(plan §3.2.9, PDF pp. 78-79). Reuse Areas 1A (North Island Industrial Park), 1B, 5 (Waterfront "
            "Industrial Park) and 10A; the text programs 1A as mainly light industrial, warehouse, office and "
            "retail (§3.5.1, PDF p. 97), but the figure draws it as industrial."},
    "FED": {"label": "Federal land (Army Reserve, Forest Service)", "category": "other",
            "seeds": {"10B Army Reserve": (640, 1060), "10B piers": (735, 1130), "Forest Service": (733, 860)},
            "note": "Federal transfer properties, exempt from local land use authority and not subject to the "
            "specific plan (plan §3.2.1, PDF p. 73). Category other."},
    "WET": {"label": "Wetlands", "category": "open-space", "seeds": {},
            "note": "Wetlands outside the Reuse Areas; Table 3-2 lists 2,865 acres of state-owned wetlands on "
            "Mare Island (plan §3.4.3, PDF p. 93; PDF p. 96)."},
}
WHITE = (254, 254, 254)
WATER = [(212, 243, 248), (196, 236, 244)]
MAX_DIST = 24
MIN_ZONE_PX = 400  # about 0.7 acres; smaller patches of a fill colour are line work or building masses
SMALL_WATER_PX = 20000
SMALL_WHITE_PX = 3000
SEED_MIN_PX = 800  # the Forest Service parcel is small and its label splits its white ground  # white/grey patches smaller than this (about 5 acres) are building masses or label boxes

# Starting fit: street intersections in the render (pixels) and in OpenStreetMap (UTM 10N).
INIT_POINTS = {
    ("A Street", "Railroad Avenue"): (1694.0, 1082.0),
    ("G Street", "Railroad Avenue"): (1901.0, 1082.0),
}
BBOX = (-122.33, 38.06, -122.24, 38.13)


def fetch(doc: dict):
    """trace.fetch_document, but the City's server refuses urllib's default user agent (403)."""
    import shutil
    import urllib.request

    dest = tb.DOCS / doc["file"]
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(doc["url"], headers={"User-Agent": "Mozilla/5.0 (bam-pipeline)"})
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        with urllib.request.urlopen(req) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        tmp.rename(dest)
    return trace.fetch_document(doc["url"], dest, doc["sha256"])  # checks the pinned sha256


def render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG_PAGE]
    text = page.get_textpage().get_text_range()
    rgb = np.asarray(page.render(scale=RENDER_SCALE).to_pil().convert("RGB"))
    if rgb.shape[:2] != (1584, 2448):
        raise SystemExit(f"unexpected render size {rgb.shape} (text: {text[:80]!r})")
    return rgb


def georeference(rgb: np.ndarray, site):
    v = rgb.astype(float).mean(axis=2)
    sat = rgb.max(axis=2).astype(int) - rgb.min(axis=2)
    grey = ((sat < 18) & (v > 165) & (v < 228)).astype(np.uint8)
    grey[:700] = 0  # bay, legend and the wetlands north of the developed shore: no building masses
    grey = cv2.morphologyEx(grey, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(grey, connectivity=4)
    keep = np.isin(cc, np.nonzero((st[:, cv2.CC_STAT_AREA] >= 25) & (st[:, cv2.CC_STAT_AREA] < 4000))[0])
    keep[cc == 0] = False
    k8 = keep.astype(np.uint8)
    edge = k8 - cv2.erode(k8, np.ones((3, 3), np.uint8))
    ys, xs = np.nonzero(edge)
    pts = np.c_[xs, ys].astype(float) + 0.5

    streets = tb.streets("mi-mare-island", BBOX)
    src = np.array(list(INIT_POINTS.values()))
    dst = np.array([tb.intersection(streets, a, b) for a, b in INIT_POINTS])
    init = trace.fit_similarity(src, dst)

    bld = tb.buildings("mi-mare-island", BBOX)
    bld = bld[bld.intersects(site.buffer(200))]
    target = shapely.union_all(bld.geometry.boundary.to_numpy())
    q = 0.5
    sim, d = tb.icp(pts, [target], np.zeros(len(pts), int), init, q, iterations=80)
    rep = tb.icp_report(sim, d, q, "figure building-mass edges vs Overture building outlines")
    check = np.linalg.norm(sim.apply(src) - dst, axis=1)
    rep["street_intersection_check_m"] = {f"{a} / {b}": round(float(c), 1) for (a, b), c in zip(INIT_POINTS, check)}
    rep["init"] = "A Street and G Street at Railroad Avenue (OpenStreetMap via Overture)"
    return sim, rep, d


def _components(mask: np.ndarray):
    return cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=4)


def classify(rgb: np.ndarray) -> dict:
    """Label every land pixel of the figure with a zone key."""
    keys = list(ZONES) + ["_WHITE", "_WATER"]
    pal, owner = [], []
    for i, k in enumerate(ZONES):
        for c in ZONES[k]["rgb"]:
            pal.append(c)
            owner.append(i)
    pal.append(WHITE)
    owner.append(len(ZONES))
    for c in WATER:
        pal.append(c)
        owner.append(len(ZONES) + 1)
    pal, owner = np.array(pal, float), np.array(owner)
    f = rgb.astype(float)
    best_d = np.full(rgb.shape[:2], np.inf)
    best = np.full(rgb.shape[:2], -1)
    for j, c in enumerate(pal):
        d = np.linalg.norm(f - c, axis=2)
        upd = d < best_d
        best_d[upd], best[upd] = d[upd], owner[j]
    lab = np.where(best_d <= MAX_DIST, best, -1)
    # The grey building masses count as "white" ground (the industrial areas are white with grey masses).
    v = f.mean(axis=2)
    sat = rgb.max(axis=2).astype(int) - rgb.min(axis=2)
    lab[(lab == -1) & (sat < 20) & (v > 150)] = len(ZONES)
    lab[:MAP_TOP] = -1
    lab[:LEGEND_BOTTOM, :LEGEND_RIGHT] = -1
    # Drop specks and small patches: anti-aliased edges, pale building masses that happen to match the golf
    # course or residential fill, and white street lines that match the water. They go to the nearest zone.
    for i in range(len(keys)):
        min_px = SMALL_WATER_PX if keys[i] == "_WATER" else MIN_ZONE_PX
        n, cc, st, _ = _components(lab == i)
        small = np.isin(cc, np.nonzero(st[:, cv2.CC_STAT_AREA] < min_px)[0]) & (lab == i)
        lab[small] = -1

    # White ground: split by the plan's lines into areas; large ones become Industrial, Federal or Wetlands.
    # Open the white mask first so thin white lines (residential streets, gaps along the plan's lines) don't
    # join separate areas; what the opening removes goes to the nearest zone.
    white = cv2.morphologyEx((lab == len(ZONES)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
    n, cc, st, _ = _components(white)
    zone_of_comp = {}
    for key, z in WHITE_ZONES.items():
        for name, (x, y) in z["seeds"].items():
            win = cc[y - 12:y + 13, x - 12:x + 13]
            ids = win[win > 0]
            if not len(ids):
                raise SystemExit(f"seed {name} ({key}) is not on white ground")
            cid = int(np.bincount(ids).argmax())
            if st[cid, cv2.CC_STAT_AREA] < SEED_MIN_PX:
                raise SystemExit(f"seed {name} ({key}) is on a small patch")
            if cid in zone_of_comp and zone_of_comp[cid] != key:
                raise SystemExit(f"seed {name} ({key}) shares an area with {zone_of_comp[cid]}: lines leak")
            zone_of_comp[cid] = key
    out_keys = list(ZONES) + list(WHITE_ZONES)
    final = np.full(lab.shape, -1)
    for i in range(len(ZONES)):
        final[lab == i] = i
    for cid in range(1, n):
        if st[cid, cv2.CC_STAT_AREA] < SMALL_WHITE_PX and cid not in zone_of_comp:
            continue  # building masses and label boxes inside a zone: nearest zone below
        key = zone_of_comp.get(cid, "WET")
        final[cc == cid] = out_keys.index(key)
    water = lab == len(ZONES) + 1

    # Everything else on land (lines, text, small patches) goes to the nearest zone.
    zone = final >= 0
    _, idx = cv2.distanceTransformWithLabels((~zone).astype(np.uint8), cv2.DIST_L2, 5,
                                             labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(zone)
    lookup = np.full(idx.max() + 1, -1)
    lookup[idx[ys, xs]] = final[ys, xs]
    filled = np.where(zone, final, lookup[idx])
    filled[water] = -1
    filled[:MAP_TOP] = -1
    masks = {}
    for i, k in enumerate(out_keys):
        m = (filled == i).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        masks[k] = m
    return masks


def _mask_polys(mask: np.ndarray, min_px: int = 40):
    contours, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
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
        parts = list(shapely.get_parts(p))
        while any(not isinstance(q, (Polygon, shapely.LineString, shapely.Point)) for q in parts):
            parts = [r for q in parts for r in shapely.get_parts(q)]  # flatten collections of multipolygons
        polys.extend(q for q in parts if isinstance(q, Polygon) and q.area >= min_px)
    return shapely.union_all(polys) if polys else shapely.MultiPolygon()


def _clean(g, min_acres: float = 0.5):
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
    fig_pdf = fetch(FIGURES)
    fetch(PLAN)
    site_wgs = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
                     ["features"][0]["geometry"])
    site = gpd.GeoSeries([site_wgs], crs=4326).to_crs(tb.UTM).iloc[0]

    rgb = render(fig_pdf)
    sim, rep, d = georeference(rgb, site)
    print(f"[mare-island landuse] scale {sim.scale:.2f} m/px, rotation {math.degrees(sim.rotation):.1f} deg, "
          f"trimmed RMS {sim.rms_m:.1f} m, median {np.median(d):.1f} m, checks {rep['street_intersection_check_m']}")

    masks = classify(rgb)
    specs = {**ZONES, **WHITE_ZONES}
    features, drawn = [], {}
    tol = 2.0  # m: under one render pixel (2.6 m) and about half a pixel of the ~100 dpi scan
    for key, spec in specs.items():
        g = sim.geometry(_mask_polys(masks[key])).buffer(0)
        full = g.area
        g = g.intersection(site)
        g = _clean(g.simplify(tol))
        if g is None:
            print(f"  {key}: nothing inside the site")
            continue
        acres = g.area / ACRE_M2
        drawn[key] = acres
        features.append({"type": "Feature", "properties": {
            "kind": "zone",
            "category": spec["category"],
            "label": spec["label"],
            "source": f"traced: {FIGURES['title']}, {FIG_LABEL}",
            "note": (f"{spec['note']} About {acres:,.0f} acres as drawn inside the site. Adopted plan's designation; "
                     "approximate, traced from a scanned figure."),
            "stage": STAGE,
            "accuracy": "approximate",
        }, "geometry": mapping(tb.to_wgs(g))})
        print(f"  {key:5s} {spec['category']:11s} {acres:8,.0f} ac inside site "
              f"({100 * g.area / full if full else 0:.0f}% of traced)")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Land-use designations of the adopted Mare Island Specific Plan (1999, amended and restated 2005, "
                "amended through 2013), traced from its Figure 3.1 Land Use (revised January 2008) in the City of "
                "Vallejo's posted plan graphics, and clipped to the adopted plan area from City GIS. White industrial "
                "and wetland areas are told apart by the plan's Reuse Area lines; medium and low density housing "
                "are one zone because the scan doesn't separate them; the retail/commercial asterisks (point "
                "symbols) and the diagrammatic building masses aren't drawn. Federal transfer land (Army Reserve, "
                "Forest Service) is shown but isn't subject to the plan. The Mare Island Company's new specific "
                "plan is still a draft under City review and isn't drawn. All boundaries are approximate."),
            "note": ("Land-use zones of the adopted 1999-2013 specific plan; a new plan is in City review. "
                     "Approximate zones, not buildings."),
            "sourceUrl": FIGURES["url"],
            "sourceLabel": "Specific plan land use, rev. 2008 (PDF)",
            "georeference": {
                "fit": rep,
                "note": (f"Figure building masses fitted to Overture/OpenStreetMap building outlines by trimmed "
                         f"ICP from two street intersections: about {sim.scale:.2f} m per render pixel, trimmed RMS "
                         f"{sim.rms_m:.0f} m (median {np.median(d):.0f} m over all points). Zones are clipped to "
                         "the site boundary (City of Vallejo GIS layer 67)."),
            },
            "license": ("Zone shapes: traced from the City of Vallejo's public Mare Island Specific Plan graphics. "
                        "Georeference: " + tb.OSM_LICENSE + "."),
            "documents": [FIGURES["url"], PLAN["url"], DOCS_PAGE, GIS + "/67", GIS + "/2", GIS + "/5"],
        },
        "features": features,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc, 6), indent=1) + "\n")
    print(f"[mare-island landuse] wrote {OUT.relative_to(config.ROOT)} ({OUT.stat().st_size / 1024:.0f} KB); "
          f"site {site.area / ACRE_M2:,.0f} ac, zones {sum(drawn.values()):,.0f} ac")


if __name__ == "__main__":
    main()
