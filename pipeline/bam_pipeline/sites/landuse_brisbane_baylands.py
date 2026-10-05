"""Brisbane Baylands: land-use zones from the 2026 Specific Plan, and the historic Roundhouse.

The Baylands is a plan-scale project that the City Council hasn't approved yet, so the map
draws its boundary and land-use zones only, no buildings (SPEC §7). The one exception is the
landmark SPEC names: the historic Bayshore Roundhouse, which exists today.

Zones
- Source: the City of Brisbane's 2026 Staff-Recommended Baylands Specific Plan (May 14, 2026),
  Chapter 2, Figure 2.3.1 "Land Use Plan" (PDF p. 10, printed p. 2-9). It's the newest
  official land-use map for the site. The Planning Commission recommended it on Aug 13, 2026;
  the City Council hasn't acted, so it is not adopted. The adopted General Plan (Measure JJ,
  2018) only splits the Baylands into two designations, "Baylands Planned Development -
  Residential Permitted" and "- Non Residential", each requiring a specific plan (city GIS
  layer GP_Land_Use_Designations_NAD83_20251110); the specific plan figure supersedes that
  level of detail and is used here.
- The figure is a raster (colour fills over an aerial photo). It is rendered at 200 dpi and
  each pixel is labelled with the nearest legend colour as printed in the map. The hatched
  Amenities Area is found from its hatch lines. Text, leader lines and the red plan-area line
  take the class of the nearest fill; white streets and the rail corridor stay out, as in the
  figure (they're the plan's "Roadway Rights-of-Way"). Brisbane Lagoon is drawn in the figure
  but isn't a land-use category, so it's left out.
- Georeference: the figure's red dash-dot "Specific Plan Area" line is fitted (similarity,
  trimmed ICP) to the site boundary in data/boundaries/brisbane-baylands.geojson (the city's
  Baylands Specific Plan Boundary layer). The plan's linework and that layer agree to about
  2 m; the aerial photo under the figure is offset from OpenStreetMap by up to ~30 m in places,
  so it isn't used for the fit. A coarse two-point seed starts the ICP.
- Zones are merged per district, clipped to the site boundary, and simplified to 1 m.

Landmark
- Footprint: OpenStreetMap way 123684307 "Bayshore Roundhouse", via Overture Maps.
- Height: about 25 ft, the "Roundhouse's existing height (~25 feet...)" in the City Council
  staff report for the Sept 29, 2026 hearing (agenda packet PDF p. 7), summarising Final EIR
  mitigation measure MM CUL-1a. The FEIR's Cultural Resources Technical Report (Appendix E)
  describes it only as a one-story brick building.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_brisbane_baylands
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import MultiLineString, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "brisbane-baylands"
STAGE = "entitlement"
UTM = tb.UTM
ACRE_M2 = tb.ACRE_M2
DOCS = config.ROOT / "data" / "raw" / "docs"
OUT_LANDUSE = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
OUT_MASSING = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
BOUNDARY = config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson"

SP_PAGE = "https://www.brisbaneca.gov/775/2026-Baylands-Specific-Plan"
SP_CH2 = {
    "title": "2026 Staff-Recommended Baylands Specific Plan (City of Brisbane, May 14, 2026), "
             "Chapter 2, Land Use Program and Definitions",
    "url": "https://www.brisbaneca.gov/DocumentCenter/View/2988",
    "file": "bb2-sp-ch02-land-use.pdf",
    "sha256": "45ecd2caef8f5a813c58dc47ed3401d2b880e2854cdde19914af9a15e2c075f1",
}
FIG = {"page_index": 9, "figure": "Figure 2.3.1, Land Use Plan", "pdf_page": 10, "printed_page": "2-9"}
CC_0929 = {
    "title": "City of Brisbane City Council special meeting, Sept 29, 2026, agenda packet "
             "(Baylands Specific Plan and EIR, meeting 2 staff report)",
    "url": "https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12608,plainText=false)",
    "file": "bb2-cc-20260929-packet.pdf",
    "sha256": "32e88193c3475e7460cb00467ddb5f3e546f37f5f57a8999484528d124851771",
}
GP_LAYER = ("https://services9.arcgis.com/UGpGSV1ugL0pHSgX/arcgis/rest/services/"
            "GP_Land_Use_Designations_NAD83_20251110/FeatureServer/7")

DPI = 200
RENDER_SHAPE = (2200, 1700, 3)
MAP_FRAME = (140, 200, 1560, 1890)  # x0, y0, x1, y1 of the map in the render (pixels)
LEGEND_BOX = (130, 1440, 560, 1895)  # legend panel inside the map frame

# Two rough street-intersection picks, used only to seed the ICP (they're off by tens of metres).
SEED = {"Bayshore Boulevard x Sunnydale Avenue": (688, 255), "Bayshore Boulevard x Tunnel Avenue": (936, 1380)}
STREETS_BBOX = (-122.418, 37.672, -122.385, 37.716)
ICP_KEEP = 0.7

# Fill colours as printed in the map (they're a little lighter than the legend swatches).
PALETTE = {
    "ldr": (239, 222, 153),
    "mdr": (254, 196, 118),
    "hdr": (186, 170, 158),
    "hdc": (233, 111, 133),
    "mdc": (196, 176, 200),
    "ldc": (237, 220, 236),
    "os": (170, 195, 120),
    "os_dark": (148, 180, 84),  # wetlands and creek corridor, also Open Space in the legend
    "ex": (165, 216, 209),
    "si": (210, 205, 211),
    "si_light": (220, 213, 220),
    "amen": (200, 170, 188),  # Amenities Area base under the hatch
    "lagoon": (176, 208, 236),  # Brisbane Lagoon: not a land-use category
}
HATCH = [(172, 132, 152), (160, 104, 135)]
MAX_DIST = 16
GAP_MAX_PX = 1500  # about 0.8 ha
GAP_MAX_LIGHT = 240  # mean of the darkest channel; white streets are ~250

# The plan's district (Figure 2.3.1 legend; definitions in Section 2.4, pp. 2-11 to 2-13).
DISTRICTS = {
    "hdr": {
        "label": "High density residential", "category": "residential",
        "note": "Minimum average 95 homes per acre; Multi-Family Mid (to 110 ft) and Multi-Family High "
                "(to 270 ft, west of the rail line) (Sec. 2.4.1, p. 2-11).",
    },
    "mdr": {
        "label": "Mid density residential", "category": "residential",
        "note": "Minimum average 75 homes per acre; townhomes and Multi-Family Low (50 ft) and Mid "
                "(110 ft) buildings (Sec. 2.4.1, p. 2-11).",
    },
    "ldr": {
        "label": "Low density residential", "category": "residential",
        "note": "Minimum average 25 homes per acre; duplexes, townhomes and small multifamily buildings "
                "up to 50 ft (four stories) (Sec. 2.4.1, p. 2-11).",
    },
    "hdc": {
        "label": "High density commercial", "category": "commercial",
        "note": "Transit-oriented commercial and hotel buildings up to 270 ft near the Bayshore Caltrain "
                "station; minimum average FAR 3.5. The plan's 500,000 sq ft of hotel goes here "
                "(Sec. 2.4.2, p. 2-12). Mapped to commercial: office, hotel and retail together.",
    },
    "mdc": {
        "label": "Mid density commercial", "category": "office",
        "note": "Office, laboratory and R&D campus buildings up to 100 ft (low-rise) or 150 ft (mid-rise); "
                "minimum average FAR 1.25 (Sec. 2.4.2, p. 2-12). Mapped to office.",
    },
    "ldc": {
        "label": "Low density commercial", "category": "office",
        "note": "Campus-style offices up to 100 ft along Sierra Point Parkway; minimum average FAR 0.5 "
                "(2.0 within half a mile of the Caltrain station) (Sec. 2.4.2, p. 2-12). Mapped to office.",
    },
    "os": {
        "label": "Open space", "category": "open-space",
        "note": "Parks, trails, wetlands and habitat, including Roundhouse Park and Ice House Hill; the "
                "plan designates 148.4 acres (Sec. 2.4.3, pp. 2-12 to 2-13).",
    },
    "amen": {
        "label": "Amenities area", "category": "other",
        "note": "Community gathering, recreation and clubhouse uses for residents, buildings up to 60 ft "
                "(Sec. 2.4.3, p. 2-12). Mapped to other: not public civic use.",
    },
    "si": {
        "label": "Sustainable infrastructure", "category": "industrial",
        "note": "Energy, water recycling, potable water storage, the city corporation yard and a possible "
                "high-speed rail maintenance facility (Sec. 2.4.3, p. 2-13). Mapped to industrial: "
                "utility and infrastructure land.",
    },
    "ex": {
        "label": "Existing use area", "category": "industrial",
        "note": "Existing uses expected to stay: Recology, Golden State Lumber, the Kinder Morgan tank "
                "farm, a machinery company, a sanitary district pump station and Bayshore Boulevard "
                "businesses (Sec. 2.4.3, p. 2-13). Mapped to industrial.",
    },
}
MERGE = {"os_dark": "os", "si_light": "si"}

# Table 2.3.1 (p. 2-10) acres by category, for the check printed at the end.
TABLE_ACRES = {"residential": 52.8, "commercial (HDC+MDC+LDC)": 121.3, "open space": 148.4, "amenities": 2.6,
               "existing use": 38.3, "sustainable infrastructure": 105.2, "rights-of-way (not drawn)": 63.7}

# The boundary layer (marked draft, 2022) leaves out two holes, about 23 acres (Kinder Morgan tank
# farm) and 5 acres (Golden State Lumber and Recology), that Figure 2.3.1 includes as Existing Use
# Areas. Zones are trimmed to the boundary as published, so most of that district isn't drawn.
HOLES_NOTE = ("The city's boundary layer (marked draft, 2022) leaves out the Kinder Morgan tank farm and the "
              "Golden State Lumber and Recology sites, which the 2026 plan includes as existing use areas, and a "
              "strip of existing use west of the rail line near Community Fields, so those aren't drawn.")

ROUNDHOUSE_OSM = "w123684307"
ROUNDHOUSE_FT = 25


# ---------------------------------------------------------------- documents

def _fetch(doc: dict):
    # The city's servers refuse Python's default user agent.
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (bay-area-megaprojects pipeline)")]
    urllib.request.install_opener(opener)
    return trace.fetch_document(doc["url"], DOCS / doc["file"], doc["sha256"])


def _check_documents(sp_path, cc_path) -> None:
    with pdfplumber.open(sp_path) as pdf:
        fig = pdf.pages[FIG["page_index"]].extract_text() or ""
        table = pdf.pages[FIG["page_index"] + 1].extract_text() or ""
    if "FIGURE 2.3.1 LAND USE PLAN" not in fig or "TOTAL SPECIFIC PLAN AREA 680.1" not in table:
        raise SystemExit("Specific Plan chapter 2 has changed: Figure 2.3.1 or Table 2.3.1 not where expected")
    with pdfplumber.open(cc_path) as pdf:
        text = " ".join((p.extract_text() or "") for p in pdf.pages)
    if "existing height (~25 feet" not in " ".join(text.split()):
        raise SystemExit("Sept 29, 2026 staff report no longer gives the Roundhouse's ~25 ft height")


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    rgb = np.asarray(page.render(scale=DPI / 72).to_pil().convert("RGB"))
    if rgb.shape != RENDER_SHAPE:
        raise SystemExit(f"unexpected Figure 2.3.1 render size {rgb.shape}")
    return rgb


# ---------------------------------------------------------------- georeference

def _frame_mask(shape) -> np.ndarray:
    m = np.zeros(shape[:2], bool)
    x0, y0, x1, y1 = MAP_FRAME
    m[y0:y1, x0:x1] = True
    lx0, ly0, lx1, ly1 = LEGEND_BOX
    m[ly0:ly1, lx0:lx1] = False
    return m


def _red_line(rgb: np.ndarray) -> np.ndarray:
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    return (r > 130) & (g < 75) & (b < 85) & (r - g > 80)


def georeference(rgb: np.ndarray, site) -> tuple[trace.Similarity, dict]:
    streets = tb.streets("bb2-brisbane_baylands", STREETS_BBOX)
    seed = trace.fit_similarity(list(SEED.values()), [tb.intersection(streets, *k.split(" x ")) for k in SEED])
    ys, xs = np.nonzero(_red_line(rgb) & _frame_mask(rgb.shape))
    pts = np.c_[xs, ys].astype(float)
    outline = MultiLineString([p.exterior for p in getattr(site, "geoms", [site])])
    sim, d = tb.icp(pts, [outline], np.zeros(len(pts), int), seed, keep=ICP_KEEP)
    rep = tb.icp_report(sim, d, ICP_KEEP, "Figure 2.3.1 Specific Plan Area line to the site boundary")
    rep["target"] = ("data/boundaries/brisbane-baylands.geojson (City of Brisbane, Baylands Specific Plan "
                     "Boundary layer)")
    rep["check"] = ("by eye, OpenStreetMap streets (via Overture) overlaid on the figure's aerial photo agree "
                    "within about 10-30 m; the photo under the plan's linework is itself offset, so it isn't "
                    "used for the fit")
    return sim, rep


# ---------------------------------------------------------------- classification

def _site_mask(shape, sim: trace.Similarity, site, pad_m: float = 3) -> np.ndarray:
    minv = np.linalg.inv(sim.matrix())
    mask = np.zeros(shape[:2], np.uint8)
    for p in getattr(site.buffer(pad_m), "geoms", [site.buffer(pad_m)]):
        xy = (minv @ (np.asarray(p.exterior.coords)[:, :2] - [sim.tx, sim.ty]).T).T
        xy[:, 1] *= -1
        cv2.fillPoly(mask, [np.round(xy).astype(np.int32)], 1)
    return mask.astype(bool)


def classify(rgb: np.ndarray, region: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """Label each pixel with a palette key index (-1 for none)."""
    keys = list(PALETTE)
    cols = np.array([PALETTE[k] for k in keys], float)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None], axis=3)
    lab = dist.argmin(axis=2).astype(np.int32)
    lab[(dist.min(axis=2) > MAX_DIST) | ~region] = -1

    # Amenities Area: the region its hatch lines cover; its fill there counts as amenities.
    hatch = np.zeros(rgb.shape[:2], bool)
    for c in HATCH:
        hatch |= np.linalg.norm(rgb.astype(float) - c, axis=2) <= 22
    hatch &= region
    hm = cv2.morphologyEx(hatch.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, comp, stats, _ = cv2.connectedComponentsWithStats(hm)
    area_ok = np.zeros(rgb.shape[:2], bool)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 800:
            area_ok |= comp == i
    amen, mdc = keys.index("amen"), keys.index("mdc")
    lab[area_ok & ((lab == mdc) | (lab == amen) | hatch)] = amen
    lab[~area_ok & (lab == amen)] = mdc

    # Text, leader lines, dots and the red plan-area line take the nearest fill's class.
    # Their anti-aliased edges blend into greys that pass for other fills, so they're cleared first.
    dark = (rgb.max(axis=2) < 150) | _red_line(rgb)
    dark = cv2.dilate(dark.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & region
    lab[dark] = -1
    src = np.where(lab >= 0, 0, 1).astype(np.uint8)
    _, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.full(near.max() + 1, -1, np.int32)
    zero = src == 0
    lut[near[zero]] = lab[zero]
    lab[dark] = lut[near[dark]]

    # Small unlabelled specks left inside fills (the light halo around labels) take the nearest
    # fill too; white streets, the rail corridor and anything off the site are large or white.
    gaps = ((lab < 0) & region).astype(np.uint8)
    n, comp, stats, _ = cv2.connectedComponentsWithStats(gaps, connectivity=8)
    lightness = rgb.min(axis=2).astype(float)
    sums = np.bincount(comp.ravel(), weights=lightness.ravel(), minlength=n)
    fill = np.zeros(n, bool)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] <= GAP_MAX_PX and sums[i] / stats[i, cv2.CC_STAT_AREA] < GAP_MAX_LIGHT:
            fill[i] = True
    sel = fill[comp] & (gaps > 0)
    src = np.where(lab >= 0, 0, 1).astype(np.uint8)
    _, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.full(near.max() + 1, -1, np.int32)
    zero = src == 0
    lut[near[zero]] = lab[zero]
    lab[sel] = lut[near[sel]]
    return lab, keys


def trace_zones(lab: np.ndarray, keys: list[str]) -> dict[str, list[Polygon]]:
    out: dict[str, list[Polygon]] = {}
    for i, key in enumerate(keys):
        district = MERGE.get(key, key)
        if district not in DISTRICTS:
            continue
        mask = (lab == i).astype(np.uint8) * 255
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        contours, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if hier is None:
            continue
        for j, c in enumerate(contours):
            if hier[0][j][3] != -1 or cv2.contourArea(c) < 60:
                continue
            holes = []
            child = hier[0][j][2]
            while child != -1:
                if cv2.contourArea(contours[child]) >= 60:
                    holes.append(contours[child].reshape(-1, 2))
                child = hier[0][child][0]
            shell = c.reshape(-1, 2)
            if len(shell) < 3:
                continue
            poly = shapely.make_valid(Polygon(shell, [h for h in holes if len(h) >= 3]))
            out.setdefault(district, []).append(poly)
    return out


# ---------------------------------------------------------------- landmark

def _roundhouse() -> gpd.GeoDataFrame:
    cache = config.RAW / "bb2-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = STREETS_BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "class", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    hit = g[g["osm"].fillna("").str.split("@").str[0] == ROUNDHOUSE_OSM]
    if len(hit) != 1 or hit["name"].iloc[0] != "Bayshore Roundhouse":
        raise SystemExit(f"expected one Overture building from OSM {ROUNDHOUSE_OSM} named Bayshore Roundhouse")
    return hit.to_crs(UTM)


# ---------------------------------------------------------------- main

def _dumps(obj) -> str:
    """Indented JSON with one coordinate pair per line."""
    text = json.dumps(obj, indent=1)
    return re.sub(r"\[\s*(-?[\d.]+),\s*(-?[\d.]+)\s*\]", r"[\1, \2]", text) + "\n"


def main() -> None:
    sp_path = _fetch(SP_CH2)
    cc_path = _fetch(CC_0929)
    _check_documents(sp_path, cc_path)

    site = gpd.read_file(BOUNDARY).to_crs(UTM).union_all()
    site_filled = shapely.union_all([Polygon(p.exterior) for p in getattr(site, "geoms", [site])])
    rgb = _render(sp_path)
    sim, georef = georeference(rgb, site)
    print(f"[{PROJECT_ID}] Figure 2.3.1 fit: RMS {georef['rms_m']} m (median {georef['median_m']} m, "
          f"p90 {georef['p90_m']} m), scale {georef['scale_m_per_unit']} m/px, rotation {georef['rotation_deg']} deg")

    region = _frame_mask(rgb.shape) & _site_mask(rgb.shape, sim, site)
    lab, keys = classify(rgb, region)
    zones_px = trace_zones(lab, keys)

    source = (f"traced: {SP_CH2['title']}, {FIG['figure']}, p. {FIG['printed_page']} (PDF p. {FIG['pdf_page']})")
    features, acres, trimmed = [], {}, {}
    for key, spec in DISTRICTS.items():
        polys = zones_px.get(key, [])
        if not polys:
            raise SystemExit(f"no {spec['label']} traced from Figure 2.3.1")
        g = shapely.make_valid(sim.geometry(shapely.union_all(polys)))
        inside = g.intersection(site)
        trimmed[key] = 1 - inside.area / g.area
        geom = inside.buffer(0.5, join_style="mitre").buffer(-0.5, join_style="mitre").simplify(1.0)
        geom = trace.as_multipolygon(shapely.make_valid(geom))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 250]))
        acres[key] = geom.area / ACRE_M2
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "zone",
                "category": spec["category"],
                "label": spec["label"],
                "source": source,
                "note": f"Draft specific plan land use, not yet adopted. {spec['note']} "
                        f"About {acres[key]:.1f} acres as drawn." + (f" {HOLES_NOTE}" if key == "ex" else ""),
                "stage": STAGE,
            },
            "geometry": mapping(tb.to_wgs(geom)),
        })
        # The boundary layer has holes where the 2026 plan keeps existing uses (see HOLES_NOTE); only
        # what falls outside its outer edge would mean a bad fit.
        off = 1 - g.intersection(site_filled).area / g.area
        if off > 0.05:
            raise SystemExit(f"{spec['label']}: {off:.1%} of the traced zone falls outside the site's outer edge")

    for key, spec in DISTRICTS.items():
        print(f"  {spec['label']:<28} {spec['category']:<11} {acres[key]:7.1f} ac  (trimmed {trimmed[key]:.1%})")
    res = sum(acres[k] for k in ("hdr", "mdr", "ldr"))
    com = sum(acres[k] for k in ("hdc", "mdc", "ldc"))
    print(f"  drawn: residential {res:.1f}, commercial {com:.1f}, open space {acres['os']:.1f}, amenities "
          f"{acres['amen']:.1f}, existing {acres['ex']:.1f}, infrastructure {acres['si']:.1f} acres; "
          f"Table 2.3.1: {TABLE_ACRES}")

    documents = [SP_PAGE, SP_CH2["url"], CC_0929["url"], GP_LAYER,
                 "https://services9.arcgis.com/UGpGSV1ugL0pHSgX/arcgis/rest/services/"
                 "Baylands_Specific_Plan_Boundary_DRAFT_Map_WFL1/FeatureServer/1"]
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                "Land-use districts traced from Figure 2.3.1 of the City of Brisbane's 2026 Staff-Recommended "
                "Baylands Specific Plan (May 2026), which the Planning Commission recommended in August 2026 and "
                "the City Council has not yet adopted. Ten districts are drawn, from high density residential "
                "near the Bayshore Caltrain station to open space, sustainable infrastructure and existing uses "
                "that stay. Streets, the Caltrain corridor and Brisbane Lagoon aren't zones and are left out; "
                "no buildings are drawn. " + HOLES_NOTE
            ),
            "note": "Land-use districts from the draft 2026 specific plan, not yet adopted; zones, not buildings.",
            "sourceUrl": SP_CH2["url"],
            "sourceLabel": "Draft specific plan land use, 2026 (PDF)",
            "georeference": {"figure_2_3_1": georef},
            "license": ("Zone shapes: traced from a public City of Brisbane planning document. Fitted to the "
                        "city's Baylands Specific Plan Boundary layer; streets for the seed from OpenStreetMap "
                        "contributors (ODbL 1.0) via Overture Maps."),
            "documents": documents,
            "superseded": ("The adopted General Plan (Measure JJ, 2018) designates the area only as Baylands "
                           "Planned Development, Residential Permitted and Non Residential (city GIS layer "
                           "GP_Land_Use_Designations_NAD83_20251110), pending a specific plan."),
        },
        "features": features,
    }
    OUT_LANDUSE.parent.mkdir(parents=True, exist_ok=True)
    OUT_LANDUSE.write_text(_dumps(tb._round(fc, 6)))
    print(f"[{PROJECT_ID}] wrote {OUT_LANDUSE.relative_to(config.ROOT)} ({len(features)} zones, "
          f"{OUT_LANDUSE.stat().st_size // 1024} KB)")

    # The historic Roundhouse, as it stands.
    rh = _roundhouse()
    geom = shapely.make_valid(rh.geometry.iloc[0].simplify(0.3))
    record = rh["osm"].iloc[0]
    massing = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": False,
            "summary": (
                "Only the historic Bayshore Roundhouse is drawn: its real footprint from OpenStreetMap, at the "
                "existing height of about 25 ft given in the city's Sept 29, 2026 staff report. The plan's "
                "proposed buildings aren't drawn while the specific plan awaits approval; see the land-use zones."
            ),
            "note": "The 1910 Southern Pacific roundhouse, listed in the National Register, which the plan keeps and restores.",
            "sourceUrl": CC_0929["url"],
            "sourceLabel": "City Council staff report, Sept 29, 2026 (PDF)",
            "georeference": "Footprint from OpenStreetMap as mapped (no tracing).",
            "license": "Footprint: OpenStreetMap contributors (ODbL 1.0), via Overture Maps.",
            "documents": [CC_0929["url"], SP_CH2["url"]],
        },
        "features": [{
            "type": "Feature",
            "properties": {
                "kind": "landmark",
                "label": "Bayshore Roundhouse",
                "stage": "complete",
                "height_ft": ROUNDHOUSE_FT,
                "podium_ft": None,
                "base_ft": 0,
                "use": None,
                "phase": None,
                "illustrative": False,
                "source": (f"footprint: OpenStreetMap way {record.lstrip('w').split('@')[0]} \"Bayshore Roundhouse\" "
                           f"via Overture Maps ({rh['id'].iloc[0]}); height: \"the Roundhouse's existing height "
                           f"(~25 feet...)\", {CC_0929['title']}, PDF p. 7"),
                "note": ("Height is approximate (about 25 ft, one story). Built in 1910, listed in the National "
                         "Register in 2010. The plan restores it as the centrepiece of 3.9-acre Roundhouse Park "
                         "and its restoration plan recommends lifting it 6 to 8 ft for sea level rise."),
            },
            "geometry": mapping(tb.to_wgs(geom)),
        }],
    }
    OUT_MASSING.parent.mkdir(parents=True, exist_ok=True)
    OUT_MASSING.write_text(json.dumps(tb._round(massing), indent=1) + "\n")
    print(f"[{PROJECT_ID}] wrote {OUT_MASSING.relative_to(config.ROOT)} (Roundhouse, {geom.area:,.0f} m2)")


if __name__ == "__main__":
    main()
