"""BART station-area housing: one program-level project, with a boundary and massing per station site.

Added at Matthew's request (2026-10-07). The program is BART's transit-oriented development on its own
land at the stations where it is not yet complete. Six sites are drawn, each from official sources:

Boundaries (one part per site, all from BART's own GIS unless noted):
- BART's "BART_AB_2923_Public_Service_20230201" feature service (BART's ArcGIS Online organisation,
  linked from bart.gov/about/business/tod/ab2923 as the "map of AB 2923 Parcels and TOD Work Plan"),
  layer 2 "TOD Work Plan": BART-owned parcels with their station, APN, acreage and TOD status.
  - West Oakland: the parcels BART marks "In Progress" at the station (004-0071-003-00, 004-0077-003-00
    and the vacated Center Street), which make up the block the City of Oakland describes (about 5.58
    acres between 7th, 5th, Chester and Mandela Parkway).
  - Lake Merritt: APNs 001-0169-001-00 (Block 1) and 001-0171-002-00 (Block 2), named in the City of
    Oakland Design Review Committee staff report of April 14, 2021 (PLN20038), p. 8.
  - North Berkeley: the four parcels BART marks "In Progress" at the station (about 8.1 acres; BART
    says "about 8.2 acres"). The greenway and auxiliary-lot parcels are left out.
  - Ashby: the West Lot, APN 053-1597-039-04 (BART: "a +/- 4-acre site (West Lot)"). The East Lot goes
    to the City of Berkeley under the 2024 exchange agreement and is not part of BART's project.
  - El Cerrito Plaza: the four parcels BART marks "In Progress" at the station, which include the station
    and track right-of-way (the City's master plan site is "roughly 6 acres" without them).
  - West Dublin/Pleasanton (Amador Station): APNs 941-2842-002-00 and 941-2842-004-00, named in the City
    of Dublin's Notice of Determination of July 28, 2026 (CEQAnet, SCH 2010022005, document 8).

Massing:
- West Oakland: traced from the Revised Preliminary Development Plan approved by the Oakland Planning
  Commission on November 4, 2020 (plan set dated July 24, 2020; PDF on oaklandca.gov). Footprints from
  the floor plans on PDF pp. 120 (typical floors) and 124 (floors 20-31, with the roofs of T3 and T4),
  rendered at 100 dpi and georeferenced by the site rectangle's four corners (fitted to the red site line)
  matched to the corners of BART's parcels. Heights from the elevations and sections (A-20.01, A-30.01,
  A-30.02): T1 tower roof 320'-0", T1 west wing up to the 19th-floor level (189'-8"), T1 podium up to
  the 4th-floor level (39'-4"), T3 roof 70'-0" over a ground floor to the 2nd-floor level (20'-0"), T4
  roof 100'-0".
- Lake Merritt: lot lines traced from the Vesting Tentative Tract Map sheets C4.1 (Block 1) and C4.2
  (Block 2) in the DRC staff report (PDF pp. 81-82), georeferenced by each block's four corners matched to
  BART's parcels. Heights and bases from the staff report's zoning table (p. 8): Buildings A and C 275 ft
  with 48-ft and 45-ft bases, Buildings B and D 83 ft. Tower footprints use the dimensions on sheets A2.13
  (Building A, 26'-7" back from the west lot line) and A2.33 (Building C floors 4-12, 22'-8" from the west
  lot line and 11'-0" from Oak Street).
- El Cerrito Plaza: building footprints traced from the colour fill of sheet A1.01 "Overall site plan -
  upper floors" in the master plan set approved July 3, 2024 (PL23-0024, Attachment D, PDF p. 43),
  georeferenced by the four corners of the main lot's property line matched to BART's parcels. Heights from
  the A3 section sheets of the same set.
- North Berkeley, Ashby and Amador Station: illustrative envelopes over the BART parcels at the official
  height limit (R-BMU 80 ft for the Berkeley sites, per the adopted North Berkeley Objective Design
  Standards citing BMC 23.202.150(F); 90 ft at Amador Station per BART's AB 2923 rezoned layer for the
  City of Dublin), with existing buildings on the parcels cut out.

    uv run --directory pipeline python -m bam_pipeline.sites.bart_station_housing
"""

from __future__ import annotations

import json
import math
import time
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, box, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT = "bart-station-housing"
UTM = "EPSG:26910"
ACRE_M2 = 4046.8564224
FT = 0.3048
RAW = config.ROOT / "data" / "raw" / "bart-station-housing"

BART_TOD = ("https://services.arcgis.com/sqS7RNuF1BQinj5N/arcgis/rest/services/"
            "BART_AB_2923_Public_Service_20230201/FeatureServer")
BART_WORKPLAN = f"{BART_TOD}/2"  # TOD Work Plan
BART_REZONED = f"{BART_TOD}/9"  # AB 2923 Rezoned (the height standard that applies on each parcel)
BART_LICENSE = "BART public ArcGIS Online service (no license stated)"
OSM = "OpenStreetMap contributors (ODbL 1.0), via Overture Maps"

DOCS = {
    "wo_pdp": {
        "url": ("https://www.oaklandca.gov/files/assets/city/v/1/planning-amp-building/documents/dp/"
                "mandela-station-bart/wo-bart-pdp-revised-approval-dated-september-16-2020.pdf"),
        "file": "wo_pdp_2020.pdf",
        "sha256": "970b7bd6c77e51a1ca83b8864c772fb8f6e3a47205129170fd454a97d8186365",
        "label": ("West Oakland BART TOD Revised Preliminary Development Plan, approved by the Oakland Planning "
                  "Commission Nov 4, 2020 (PLN18490-R02; plan set dated July 24, 2020)"),
    },
    "lm_drc": {
        "url": ("https://www.oaklandca.gov/files/assets/city/v/1/planning-amp-building/documents/dp/"
                "lake-merritt-bart/041421_drcstaffreport_lmbart_signed.pdf"),
        "file": "lm_drc_staffreport_2021.pdf",
        "sha256": "1f82d4af28c8a7bb12a06373f198aceb3bcfce869df957eae27a87dc11a64673",
        "label": ("Lake Merritt BART TOD, City of Oakland Design Review Committee staff report, Apr 14, 2021 "
                  "(PLN20038), with the Preliminary Development Plan set"),
    },
    "ecp_plans": {
        "url": "https://www.elcerrito.gov/DocumentCenter/View/20671/Attachment-D_Project-Plans",
        "file": "ecp_plans_2024.pdf",
        "sha256": "ac08b19aa66c1cbe09a7d9632cd75b3ed607bfada5cd70d023b956d5b359d547",
        "label": ("El Cerrito Plaza BART TOD master plan, Attachment D (project plans, May 20, 2024) to the City "
                  "of El Cerrito's ministerial approval PL23-0024 of July 3, 2024"),
    },
}

# Official pages cited for facts on each site (all also in the project's `sources`).
WO_PAGE = "https://www.oaklandca.gov/Planning-Building/Major-Development-Projects/West-Oakland-BART-Development-Mandela-Station"
LM_PAGE = "https://www.oaklandca.gov/Planning-Building/Major-Development-Projects/Lake-Merrit-BART-Transit-Oriented-Development"
BART_NEWS_WO = "https://www.bart.gov/news/articles/2026/news20260901-0"
BART_LM = "https://www.bart.gov/about/business/tod/lakemerritt"
BART_UPCOMING = "https://www.bart.gov/about/business/tod/upcoming"
BART_NB = "https://www.bart.gov/about/business/tod/north-berkeley"
BART_ASHBY = "https://www.bart.gov/about/business/tod/ashby"
BART_ECP = "https://www.bart.gov/about/business/tod/el-cerrito-plaza"
NB_ODS = "https://berkeleyca.gov/sites/default/files/documents/2023-12-12%20NB%20BART%20ODS_ADOPTED.pdf"
BK_APR = "https://berkeleyca.gov/sites/default/files/documents/Berkeley_City_2024_%20GP%20APR.pdf"
ECP_APPROVAL = "https://www.elcerrito.gov/DocumentCenter/View/20672/PL23-0024_Ministerial-Approval-Letter"
ECP_AS = ("https://www.elcerrito.gov/DocumentCenter/View/22554/"
          "PL22-0150-Parcel-A-South-Ministerial-Approval-Letter-Including-Conditions")
EC_TOD = "https://elcerrito.gov/1381/Transit-Oriented-Development-TOD"
DUBLIN_NOD = "https://ceqanet.lci.ca.gov/2010022005/8"

# --------------------------------------------------------------------------- sites

SITES = [
    {
        "key": "west-oakland", "name": "West Oakland (Mandela Station)", "station": "West Oakland",
        "where": "STATION_AR = 'West Oakland' AND TOD_WKPLAN = 'In Progress'",
        "named_by": "the parcels BART's TOD Work Plan layer marks “In Progress” at West Oakland, which form the "
                    "block the City of Oakland describes (about 5.58 acres between 7th, 5th and Chester Streets "
                    "and Mandela Parkway)",
        "accuracy": "official",
    },
    {
        "key": "lake-merritt", "name": "Lake Merritt", "station": "Lake Merritt",
        "where": "APN_D IN ('001-0169-001-00', '001-0171-002-00')",
        "named_by": "APNs 001-0169-001-00 (Block 1) and 001-0171-002-00 (Block 2), named in the Oakland DRC staff "
                    "report of Apr 14, 2021 (PLN20038), p. 8",
        "accuracy": "official",
    },
    {
        "key": "north-berkeley", "name": "North Berkeley", "station": "North Berkeley",
        "where": "STATION_AR = 'North Berkeley' AND TOD_WKPLAN = 'In Progress'",
        "named_by": "the four parcels BART's TOD Work Plan layer marks “In Progress” at North Berkeley (BART: "
                    "“about 8.2 acres of BART-owned land surrounding the station”); they include the station",
        "accuracy": "approximate",
    },
    {
        "key": "ashby", "name": "Ashby (West Lot)", "station": "Ashby",
        "where": "APN_D = '053-1597-039-04'",
        "named_by": "APN 053-1597-039-04, the Ashby West Lot parcel in BART's TOD Work Plan layer (BART: “a +/- "
                    "4-acre site (West Lot)”); it includes the station entrance",
        "accuracy": "approximate",
    },
    {
        "key": "el-cerrito-plaza", "name": "El Cerrito Plaza", "station": "El Cerrito Plaza",
        "where": "STATION_AR = 'El Cerrito Plaza' AND TOD_WKPLAN = 'In Progress'",
        "named_by": "the four parcels BART's TOD Work Plan layer marks “In Progress” at El Cerrito Plaza; they "
                    "include the station and track right-of-way, which the master plan does not build on",
        "accuracy": "approximate",
    },
    {
        "key": "west-dublin", "name": "West Dublin/Pleasanton (Amador Station)", "station": "West Dublin/Pleasanton",
        "where": "APN_D IN ('941-2842-002-00', '941-2842-004-00')",
        "named_by": "APNs 941-2842-002-00 and 941-2842-004-00, named in the City of Dublin's Notice of Determination "
                    "for Amador Station (CEQAnet SCH 2010022005, received July 28, 2026)",
        "accuracy": "official",
    },
]


def _get(url: str, dest, tries: int = 4) -> bytes:
    """Download once into data/raw (cached), retrying the occasional reset connection."""
    if dest.exists():
        return dest.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                data = r.read()
            dest.write_bytes(data)
            return data
        except OSError:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))
    raise AssertionError


def document(key: str):
    d = DOCS[key]
    dest = RAW / "docs" / d["file"]
    _get(d["url"], dest)
    return trace.fetch_document(d["url"], dest, d["sha256"])


def arcgis_query(layer: str, where: str) -> str:
    q = urllib.parse.urlencode({"where": where, "outFields": "*", "outSR": 4326, "f": "geojson"})
    return f"{layer}/query?{q}"


def bart_parcels() -> gpd.GeoDataFrame:
    stations = sorted({s["station"] for s in SITES})
    where = "STATION_AR IN (" + ", ".join(f"'{s}'" for s in stations) + ")"
    raw = _get(arcgis_query(BART_WORKPLAN, where), RAW / "gis" / "bart_tod_workplan.geojson")
    fc = json.loads(raw)
    if not fc.get("features"):
        raise SystemExit("BART TOD Work Plan query returned no features")
    g = gpd.GeoDataFrame.from_features(fc["features"], crs=4326).to_crs(UTM)
    g["APN_D"] = g["APN_D"].fillna("").str.strip()
    return g


def bart_rezoned() -> gpd.GeoDataFrame:
    raw = _get(arcgis_query(BART_REZONED, "1=1"), RAW / "gis" / "bart_ab2923_rezoned.geojson")
    return gpd.GeoDataFrame.from_features(json.loads(raw)["features"], crs=4326).to_crs(UTM)


def _select(g: gpd.GeoDataFrame, where: str) -> gpd.GeoDataFrame:
    """The handful of SQL-ish filters used in SITES, evaluated locally on the cached layer."""
    if where.startswith("APN_D IN") or where.startswith("APN_D ="):
        apns = [a.strip(" '") for a in where.split("(", 1)[-1].rstrip(")").split(",")] if "IN" in where \
            else [where.split("=", 1)[1].strip(" '")]
        return g[g["APN_D"].isin(apns)]
    station = where.split("STATION_AR = '", 1)[1].split("'", 1)[0]
    status = where.split("TOD_WKPLAN = '", 1)[1].split("'", 1)[0]
    return g[(g["STATION_AR"] == station) & (g["TOD_WKPLAN"] == status)]


def site_shapes(g: gpd.GeoDataFrame) -> dict[str, dict]:
    out = {}
    for s in SITES:
        sel = _select(g, s["where"])
        if sel.empty:
            raise SystemExit(f"{s['key']}: no BART parcels for {s['where']}")
        shape = shapely.union_all(sel.buffer(0.5).to_numpy()).buffer(-0.5).simplify(0.5, preserve_topology=True)
        out[s["key"]] = {**s, "utm": shape, "apns": [a or "(vacated street, no APN)" for a in sel["APN_D"]],
                         "acres": shape.area / ACRE_M2}
    return out


# --------------------------------------------------------------------------- boundary

def write_boundary(sites: dict[str, dict]) -> None:
    whole = shapely.union_all([s["utm"] for s in sites.values()])
    total = whole.area / ACRE_M2
    parts = []
    for s in sites.values():
        parts.append({
            "type": "Feature",
            "properties": {
                "kind": "sub-area", "name": s["name"], "acres": round(s["acres"], 2),
                "apns": s["apns"], "accuracy": s["accuracy"],
                "source": f"BART TOD Work Plan layer: {s['named_by']}",
            },
            "geometry": mapping(tb.to_wgs(s["utm"])),
        })
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT,
            "source": "BART TOD Work Plan layer (BART AB 2923 public service, layer 2): BART-owned parcels at each site",
            "sourceLabel": "BART TOD parcels",
            "sourceUrl": BART_WORKPLAN,
            "query": arcgis_query(BART_WORKPLAN, "STATION_AR IN (...)"),
            "accuracy": "approximate",
            "accuracyNote": (
                "Six BART station sites, each drawn from BART's own parcel layer: West Oakland, Lake Merritt, North "
                "Berkeley, Ashby (West Lot), El Cerrito Plaza and West Dublin/Pleasanton (Amador Station). The "
                "parcels at North Berkeley, Ashby and El Cerrito Plaza include station entrances and track "
                "right-of-way that won't be built on. Walnut Creek, Fremont, Bay Fair and Richmond aren't drawn: "
                f"no official source places a defined project on a parcel yet. {total:,.1f} acres as drawn."
            ),
            "license": BART_LICENSE,
            "features_used": int(sum(len(s["apns"]) for s in sites.values())),
        },
        "features": [{"type": "Feature", "properties": {"kind": "site", "name": "Project site"},
                      "geometry": mapping(tb.to_wgs(whole))}] + parts,
    }
    path = tb.OUT / f"{PROJECT}.geojson"
    path.write_text(json.dumps(tb._round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"[bart] wrote {path.relative_to(config.ROOT)}: {len(parts)} sites, {total:,.1f} acres")
    for s in sites.values():
        print(f"    {s['name']}: {s['acres']:.2f} acres, APNs {', '.join(s['apns'])}")


# --------------------------------------------------------------------------- rendering helpers

def render(pdf_path, page_no: int, dpi: int) -> np.ndarray:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(pdf_path))
    return np.asarray(pdf[page_no - 1].render(scale=dpi / 72).to_pil().convert("RGB"))


def corners_utm(shape) -> dict[str, tuple[float, float]]:
    """The four corners of a roughly rectangular parcel group: west-, north-, east- and south-most hull vertices."""
    hull = np.asarray(shape.convex_hull.simplify(1.0).exterior.coords)[:-1]
    return {
        "west": tuple(hull[hull[:, 0].argmin()]), "east": tuple(hull[hull[:, 0].argmax()]),
        "north": tuple(hull[hull[:, 1].argmax()]), "south": tuple(hull[hull[:, 1].argmin()]),
    }


def fit(fig_pts: dict, utm_pts: dict, labels: dict) -> trace.Similarity:
    keys = list(fig_pts)
    sim = trace.fit_similarity([fig_pts[k] for k in keys], [utm_pts[k] for k in keys], [labels[k] for k in keys])
    return sim


def red_rectangle(rgb: np.ndarray, x0: int, x1: int, y0: int, y1: int, band: int = 8) -> dict:
    """Corners of a red dash-dot site rectangle: a line fitted to the red pixels along each edge."""
    a = rgb.astype(int)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    ys, xs = np.nonzero(red)
    inside_x = (xs > x0 - band) & (xs < x1 + band)
    inside_y = (ys > y0 - band) & (ys < y1 + band)
    top = np.polyfit(xs[inside_x & (abs(ys - y0) < band)], ys[inside_x & (abs(ys - y0) < band)], 1)
    bot = np.polyfit(xs[inside_x & (abs(ys - y1) < band)], ys[inside_x & (abs(ys - y1) < band)], 1)
    left = np.polyfit(ys[inside_y & (abs(xs - x0) < band)], xs[inside_y & (abs(xs - x0) < band)], 1)
    right = np.polyfit(ys[inside_y & (abs(xs - x1) < band)], xs[inside_y & (abs(xs - x1) < band)], 1)

    def meet(h, v):
        y = (h[0] * v[1] + h[1]) / (1 - h[0] * v[0])
        return (float(v[0] * y + v[1]), float(y))

    return {"tl": meet(top, left), "tr": meet(top, right), "br": meet(bot, right), "bl": meet(bot, left)}


def feature(geom_utm, **props) -> dict:
    g = shapely.make_valid(geom_utm)
    if g.geom_type == "GeometryCollection":
        g = shapely.union_all([p for p in g.geoms if p.geom_type in ("Polygon", "MultiPolygon")])
    g = g.simplify(0.3, preserve_topology=True)
    base = {"kind": "building", "block": None, "label": "", "stage": "entitled", "height_ft": None,
            "podium_ft": None, "base_ft": 0, "use": None, "phase": None, "illustrative": False, "source": ""}
    base.update(props)
    if base["block"] is None:
        del base["block"]
    return {"type": "Feature", "properties": base, "geometry": mapping(tb.to_wgs(g))}


# --------------------------------------------------------------------------- West Oakland

# Revised PDP (plan set dated July 24, 2020), PDF p. 124 "floors 20-31" plan, 100 dpi render. The site
# rectangle is found from the red site line; the shapes below were read off the same render.
WO_PAGE_UPPER = 124
WO_RECT_APPROX = (304, 1234, 258, 790)  # x0, x1, y0, y1 of the red site rectangle
WO_T1_AREA = [(761, 259), (1233.7, 255.5), (1233.9, 454), (980, 404), (980, 376), (761, 337)]  # T1 development area
WO_T1_WING = [(815, 259), (992, 258), (992, 360), (862, 356), (862, 345), (815, 345)]  # to the 19th-floor level
WO_T1_TOWER = [(992, 257), (1232, 256), (1232, 452), (1135, 432), (1135, 360), (992, 360)]  # floors 20-31
WO_T3_GROUND = [(304, 455), (462, 480), (575, 527), (677, 548), (677, 789), (304, 789)]
WO_T3_UPPER = [(303, 452), (437.5, 486), (600, 536), (681, 547.5), (681, 786), (378, 786), (378, 550),
               (419, 550), (419, 511), (303, 502)]  # typical floors, PDF p. 120 (same frame as p. 124)
WO_T3_COURT = [(472, 542), (575, 586), (575, 692), (472, 692)]
WO_T4 = [(791, 607), (892, 607), (892, 614), (917, 614), (921, 564), (1232, 622), (1232, 779), (1102, 779),
         (1102, 775), (1010, 775), (1010, 785), (791, 785)]


def west_oakland(site: dict) -> tuple[list[dict], dict]:
    pdf = document("wo_pdp")
    rgb = render(pdf, WO_PAGE_UPPER, 100)
    x0, x1, y0, y1 = WO_RECT_APPROX
    fig = red_rectangle(rgb, x0, x1, y0, y1)
    c = corners_utm(site["utm"])
    # The plan has 7th Street along the top and Chester Street on the left.
    utm = {"tl": c["north"], "tr": c["east"], "br": c["south"], "bl": c["west"]}
    labels = {"tl": "7th St / Chester St parcel corner", "tr": "7th St / Mandela Pkwy parcel corner",
              "br": "5th St / Mandela Pkwy parcel corner", "bl": "5th St / Chester St parcel corner"}
    sim = fit(fig, utm, labels)
    P = lambda pts: sim.geometry(Polygon(pts))  # noqa: E731
    doc = DOCS["wo_pdp"]["label"]
    t1_area, wing, tower = P(WO_T1_AREA), P(WO_T1_WING), P(WO_T1_TOWER)
    podium = t1_area.difference(wing.union(tower).buffer(0.05))
    t3_ground = P(WO_T3_GROUND)
    t3_upper = P(WO_T3_UPPER).difference(P(WO_T3_COURT)).intersection(t3_ground.buffer(1.0))
    t3_base = t3_ground.difference(t3_upper.buffer(0.05))
    t4 = P(WO_T4)
    common = {"block": "West Oakland"}
    feats = [
        feature(tower, **common, label="T1 tower", height_ft=320, use="Residential",
                source=f"traced: {doc}, PDF p. 124 (floors 20-31 plan); height: sheet A-20.01, roof 320'-0\"",
                note="31 stories; 522 market-rate homes in T1 (City of Oakland project page)."),
        feature(wing, **common, label="T1 west wing", height_ft=189.7, use="Residential",
                source=f"traced: {doc}, PDF p. 124 (outline of the floors below the 19th-floor roof terrace); "
                       "height: sheet A-20.01, 19th-floor level 189'-8\""),
        feature(podium, **common, label="T1 podium", height_ft=39.3, use="Retail, parking",
                source=f"traced: {doc}, PDF p. 124 (T1 development area line); height: sheet A-20.01, "
                       "4th-floor level 39'-4\" (the podium roof terraces are at the 4th floor)"),
        feature(t3_upper, **common, label="T3 (affordable homes)", height_ft=70, stage="construction",
                use="Affordable residential", phase="Phase 1",
                source=f"traced: {doc}, PDF p. 120 (typical floor plan); height: sheet A-30.02, roof 70'-0\"; "
                       f"under construction: BART, Sept 1, 2026 ({BART_NEWS_WO})",
                note="7 stories, 240 affordable homes; BART says construction began September 2026. The "
                     "courtyard is approximate."),
        feature(t3_base, **common, label="T3 ground floor", height_ft=20, stage="construction",
                use="Retail, parking", phase="Phase 1",
                source=f"traced: {doc}, PDF p. 124 (T3 outline); height: sheet A-30.02, 2nd-floor level 20'-0\" "
                       "(decks and courtyard at the 2nd floor)"),
        feature(t4, **common, label="T4 (office)", height_ft=100, use="Office, retail",
                source=f"traced: {doc}, PDF p. 124 (T4 roof outline); height: sheet A-30.01, roof 100'-0\" (the "
                       f"City describes a “100-ft tall” office building, {WO_PAGE})"),
    ]
    geo = {**sim.report(), "method": "least-squares similarity on the four corners of the plan's site rectangle "
                                     "(lines fitted to the red site line) matched to the corners of BART's parcels",
           "page": "Revised PDP, PDF p. 124 (100 dpi); p. 120 shares its frame"}
    return feats, geo


# --------------------------------------------------------------------------- Lake Merritt

# Vesting Tentative Tract Map sheets in the DRC staff report, 100 dpi renders (1" = 20', so 5 px a foot).
LM_B1_PAGE, LM_B2_PAGE = 81, 82
LM_B1 = {"nw": (608.8, 666.9), "ne": (2109.3, 667.0), "se": (2109.3, 1665.7), "sw": (608.6, 1665.7)}
LM_B2 = {"nw": (612.7, 729.0), "ne": (2116.0, 729.0), "se": (2116.0, 1724.0), "sw": (612.7, 1724.0)}
LM_LOT_A = [(969.4, 666.9), (2109.3, 667.0), (2109.3, 1036.0), (1807.0, 1146.0), (969.4, 1029.4)]
LM_LOT_B = [(865.7, 1665.7), (865.7, 1443.5), (879.5, 1345.0), (2109.3, 1518.9), (2109.3, 1665.7)]
LM_A_TOWER_X = 969.4 + 26.58 * 5.0  # 26'-7" from the lot's west line (sheet A2.13)
LM_D_EAST_X = 612.7 + 124.05 / 300.10 * (2116.0 - 612.7)  # Lot 2 (Building D): 24,810 sq ft over the 200-ft depth
LM_C_TOWER = (22.67, 11.0)  # Building C floors 4-12: ft back from the west lot line and from Oak Street (A2.33)


def lake_merritt(site: dict, parcels: gpd.GeoDataFrame) -> tuple[list[dict], dict]:
    document("lm_drc")
    doc = DOCS["lm_drc"]["label"]
    b1 = parcels[parcels["APN_D"] == "001-0169-001-00"].geometry.iloc[0]
    b2 = parcels[parcels["APN_D"] == "001-0171-002-00"].geometry.iloc[0]
    feats, geo = [], {}
    for name, block, fig_pts, page in (("Block 1", b1, LM_B1, LM_B1_PAGE), ("Block 2", b2, LM_B2, LM_B2_PAGE)):
        c = corners_utm(block)
        # Sheets have the long street (9th / 8th Street) along the top; the blocks run WNW-ESE.
        utm = {"nw": c["north"], "ne": c["east"], "se": c["south"], "sw": c["west"]}
        if name == "Block 1":
            labels = {"nw": "9th St / Oak St", "ne": "9th St / Fallon St", "se": "8th St / Fallon St", "sw": "8th St / Oak St"}
        else:
            labels = {"nw": "8th St / Madison St", "ne": "8th St / Oak St", "se": "7th St / Oak St", "sw": "7th St / Madison St"}
        sim = fit(fig_pts, utm, {k: f"{name}: {v} block corner" for k, v in labels.items()})
        geo[name] = {**sim.report(), "page": f"DRC staff report PDF p. {page} (sheet C4.{1 if name == 'Block 1' else 2})"}
        P = lambda pts, s=sim: s.geometry(Polygon(pts))  # noqa: E731
        if name == "Block 1":
            lot_a, lot_b = P(LM_LOT_A), P(LM_LOT_B)
            tower = lot_a.intersection(P([(LM_A_TOWER_X, 600), (2200, 600), (2200, 1200), (LM_A_TOWER_X, 1200)]))
            base = lot_a.difference(tower.buffer(0.05))
            src = f"traced: {doc}, sheet C4.1 (Vesting Tentative Tract Map, Block 1), PDF p. 81"
            feats += [
                feature(tower, block="Lake Merritt Block 1", label="Building A tower", height_ft=275, use="Residential",
                        source=f"{src}; tower set back 26'-7\" from the lot's west line per sheet A2.13 (PDF p. 94); "
                               "height: staff report p. 8, “Building A: 275 ft”",
                        note="28 stories; 360 homes in the 2021 plan. BART's upcoming-projects page now lists a "
                             "439-home market-rate building here."),
                feature(base, block="Lake Merritt Block 1", label="Building A base", height_ft=48, use="Residential, retail",
                        source=f"{src}; height: staff report p. 8, building base “Building A: 48 ft”"),
                feature(lot_b, block="Lake Merritt Block 1", label="Building B (Chinatown senior homes)", height_ft=83,
                        stage="construction", use="Affordable senior residential", phase="Phase 1",
                        source=f"{src} (Lot 2); height: staff report p. 8, “Building B: 83 ft”; under construction per "
                               f"BART ({BART_LM})",
                        note="7 stories, 97 affordable senior homes. BART's pages give the construction start as "
                             "October 2024 (project page) and June 2025 (upcoming-projects page). The lot is drawn; "
                             "the building is slightly smaller."),
            ]
        else:
            lot_d = P([(LM_B2["nw"][0], 729.0), (LM_D_EAST_X, 729.0), (LM_D_EAST_X, 1724.0), (LM_B2["sw"][0], 1724.0)])
            lot_c = P([(LM_D_EAST_X, 729.0), (2116.0, 729.0), (2116.0, 1724.0), (LM_D_EAST_X, 1724.0)])
            px_ft = (2116.0 - 612.7) / 300.10
            tx0, tx1 = LM_D_EAST_X + LM_C_TOWER[0] * px_ft, 2116.0 - LM_C_TOWER[1] * px_ft
            tower = P([(tx0, 729.0), (tx1, 729.0), (tx1, 1724.0), (tx0, 1724.0)])
            base = lot_c.difference(tower.buffer(0.05))
            src = f"traced: {doc}, sheet C4.2 (Vesting Tentative Tract Map, Block 2), PDF p. 82"
            feats += [
                feature(tower, block="Lake Merritt Block 2", label="Building C tower (office)", height_ft=275,
                        use="Office",
                        source=f"{src}; tower set back 22'-8\" from the west lot line and 11'-0\" from Oak Street per "
                               "sheet A2.33 (floors 4-12, PDF p. 109); height: staff report p. 8, “Building C: 275 ft”",
                        note="19 stories, up to 500,000 sq ft of office (City of Oakland). Upper floors may step in "
                             "further; drawn at the floors 4-12 outline."),
                feature(base, block="Lake Merritt Block 2", label="Building C base", height_ft=45, use="Office, retail",
                        source=f"{src}; height: staff report p. 8, building base “Building C: 45 ft”"),
                feature(lot_d, block="Lake Merritt Block 2", label="Building D (family homes)", height_ft=83,
                        use="Affordable residential",
                        source=f"{src} (Lot 2, 24,810 sq ft, split from Lot 1 along the 200-ft lot line); height: "
                               "staff report p. 8, “Building D: 83 ft”",
                        note="7 stories, 100 affordable family homes."),
            ]
    return feats, geo


# --------------------------------------------------------------------------- El Cerrito Plaza

# Sheet A1.01 "Overall site plan - upper floors" (PDF p. 43), 100 dpi render (1" = 40', 0.4 ft a pixel).
ECP_PAGE = 43
ECP_FILL = (245, 232, 188)  # the residential fill of the upper floors
# Corners of the main lot's property line (the heavy dashed line), read off the render.
ECP_CORNERS = {"tl": (646.0, 350.0), "tr": (1938.0, 351.0), "br": (1957.0, 1733.0), "bl": (666.5, 1721.5)}
ECP_LABELS = {"tl": "Liberty St / Fairmount Ave lot corner", "tr": "Liberty St / Central Ave lot corner",
              "br": "Central Ave / Richmond St lot corner", "bl": "Fairmount Ave / Richmond St lot corner"}
# Each building's extent on the sheet (px), for naming the traced fills.
ECP_BUILDINGS = [
    {"label": "Parcel C-West", "box": (646, 346, 1218, 746), "height_ft": 78, "stage": "entitled",
     "use": "Affordable residential, possible library",
     "height_src": "sheet A3.50C-W section (PDF p. 65): ground (library) level 0'-0\", roof 78'-0\"",
     "note": "6 stories, 79 homes (approval letter, Table 1)."},
    {"label": "Parcel C-East", "box": (646, 746, 1218, 1230), "height_ft": 76.5, "stage": "entitled",
     "use": "Affordable residential",
     "height_src": "sheet A3.50C-E section (PDF p. 70): building height 76'-6\"",
     "note": "6 stories, 84 homes (approval letter, Table 1)."},
    {"label": "Parcel B", "box": (1218, 346, 1960, 1090), "height_ft": 85, "stage": "entitled",
     "use": "Residential, BART garage",
     "height_src": "sheet A3.50B section (PDF p. 60): 85' to average grade (78' on the station side)",
     "note": "7 stories, 259 homes and the 145-space BART garage (approval letter, Table 1)."},
    {"label": "Parcel D", "box": (1218, 1440, 1960, 1740), "height_ft": 57, "stage": "entitled",
     "use": "Affordable residential",
     "height_src": "sheet A3.50D section (PDF p. 75): building height 57'-0\"",
     "note": "5 stories, 118 homes (approval letter, Table 1). The approval letter gives 67-85 ft for the five "
             "master-plan buildings; the section sheet's 57 ft is used."},
    {"label": "Parcel A-South", "box": (2100, 1240, 2470, 1740), "height_ft": None, "stage": "construction",
     "use": "Affordable residential", "phase": "Phase 1",
     "height_src": "approval PL22-0150 (Apr 3, 2023): a 6-story building; no height in feet was found",
     "note": "70 homes, 69 of them affordable; construction began November 2025 (City of El Cerrito). Drawn as an "
             "outline: no official height in feet was found."},
    {"label": "Parcel A-North", "box": (2470, 1140, 3040, 1740), "height_ft": 75, "stage": "entitled",
     "use": "Residential",
     "height_src": "sheet A3.50A-N section (PDF p. 51): 75' to average grade",
     "note": "6 stories, 133 homes (approval letter, Table 1)."},
]


def el_cerrito_plaza(site: dict, parcels: gpd.GeoDataFrame) -> tuple[list[dict], dict]:
    pdf = document("ecp_plans")
    doc = DOCS["ecp_plans"]["label"]
    main = parcels[(parcels["STATION_AR"] == "El Cerrito Plaza") & (parcels["APN_D"] != "504-050-012-5")]
    c = corners_utm(shapely.union_all(main.buffer(0.5).to_numpy()).buffer(-0.5))
    # The sheet is turned: Liberty Street (the lot's southwest side) runs along the top.
    utm = {"tl": c["south"], "tr": c["west"], "br": c["north"], "bl": c["east"]}
    sim = fit(ECP_CORNERS, utm, ECP_LABELS)
    rgb = render(pdf, ECP_PAGE, 100)
    fills = trace.raster_color_polygons(rgb, ECP_FILL, tol=12, min_area_px=200, close_px=9, simplify_px=1.0)
    feats = []
    for b in ECP_BUILDINGS:
        x0, y0, x1, y1 = b["box"]
        parts = [p.intersection(box(x0, y0, x1, y1)) for p in fills if box(x0, y0, x1, y1).intersects(p)]
        parts = [p for p in parts if p.area > 200]
        if not parts:
            raise SystemExit(f"El Cerrito Plaza: no fill found for {b['label']}")
        # Close the corridors and walls between the unit fills (32 px = 12.8 ft), keeping square corners;
        # courtyards are wider and stay open.
        fig = shapely.union_all(parts).buffer(32, join_style="mitre").buffer(-32, join_style="mitre")
        geom = sim.geometry(fig).intersection(site["utm"].buffer(1.0))
        feats.append(feature(
            geom, block="El Cerrito Plaza", label=b["label"], height_ft=b["height_ft"], stage=b["stage"],
            use=b["use"], phase=b.get("phase"),
            source=f"traced: {doc}, sheet A1.01 overall site plan - upper floors (PDF p. 43); height: {b['height_src']}",
            note=b["note"]))
    geo = {**sim.report(), "method": "least-squares similarity on the four corners of the main lot's property line "
                                     "matched to the corners of BART's parcels",
           "page": "sheet A1.01, PDF p. 43 (100 dpi)"}
    return feats, geo


# --------------------------------------------------------------------------- illustrative envelopes

def envelope(site: dict, name: str, height_ft: float, stage: str, source: str, note: str,
             cut_existing: bool = True) -> dict:
    """The BART parcels at the height limit, with any existing building on them cut out."""
    existing = []
    if cut_existing:
        x0, y0, x1, y1 = gpd.GeoSeries([site["utm"]], crs=UTM).to_crs(4326).total_bounds
        blds = tb.buildings(f"bart-{site['key']}", (x0 - 0.0005, y0 - 0.0005, x1 + 0.0005, y1 + 0.0005))
        existing = [b for b in blds.geometry if b.intersects(site["utm"]) and b.intersection(site["utm"]).area > 50]
    geom = site["utm"].difference(shapely.union_all(existing).buffer(1.0)) if existing else site["utm"]
    if existing and stage != "proposed":
        note += f" {len(existing)} existing building(s) on the parcels (OpenStreetMap) are cut out."
    return feature(geom, kind="block", block=name, label=name, height_ft=height_ft, stage=stage,
                   use="Residential (mixed use)", illustrative=True, source=f"illustrative: {source}", note=note)


# --------------------------------------------------------------------------- main

def main() -> None:
    parcels = bart_parcels()
    sites = site_shapes(parcels)
    write_boundary(sites)

    feats, geo = [], {}
    f, geo["west_oakland"] = west_oakland(sites["west-oakland"])
    feats += f
    f, geo["lake_merritt"] = lake_merritt(sites["lake-merritt"], parcels)
    feats += f
    f, geo["el_cerrito_plaza"] = el_cerrito_plaza(sites["el-cerrito-plaza"], parcels)
    feats += f

    rbmu = (f"the R-BMU zoning district's 80-ft / 7-story maximum (BMC 23.202.150(F)), as stated in the City of "
            f"Berkeley's adopted North Berkeley BART Objective Design Standards, Dec 2023, Sec. 2.1.1 ({NB_ODS})")
    feats.append(envelope(
        sites["north-berkeley"], "North Berkeley", 80, "entitled",
        f"BART parcels drawn to {rbmu}",
        "Entitled Dec 11, 2024 for 739 homes in buildings of 3 to 8 stories (City of Berkeley 2024 General Plan "
        "progress report); the design isn't drawn. Paths, plazas and the station area will stay open."))
    feats.append(envelope(
        sites["ashby"], "Ashby West Lot", 80, "proposed",
        f"the West Lot parcel drawn to {rbmu}",
        "Developer selected July 2025; BART describes five buildings of 6 to 8 stories with up to 600 homes. No "
        "design has been filed with the City."))
    rz = bart_rezoned()
    dub = rz[rz["apn"].astype(str).str.contains("941-2842-00[24]", regex=True)]
    dub_h = sorted(set(dub["Building_Height"].astype(str)))
    feats.append(envelope(
        sites["west-dublin"], "Amador Station", 90, "entitled",
        f"BART parcels drawn to the 90-ft limit in BART's AB 2923 rezoned layer for these parcels (City of Dublin; "
        f"“{'; '.join(dub_h)}”, {BART_REZONED})",
        "300 affordable homes (City of Dublin, July 2026); construction awaits funding (BART). The design isn't drawn. "
        "OpenStreetMap has two footprints here tagged building=construction (checked 2023); no official source says "
        "work has started, so they aren't treated as buildings.",
        cut_existing=False))

    srcs = sorted({d["url"] for d in DOCS.values()})
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT,
            "illustrative": True,
            "summary": (
                "West Oakland, Lake Merritt and El Cerrito Plaza are traced from their approved plans, with heights "
                "from the plans' sections and the City's zoning tables. North Berkeley, the Ashby West Lot and "
                "Amador Station have no published design, so they are illustrative envelopes: BART's parcels "
                "drawn to the height limit (80 ft in Berkeley's R-BMU district, 90 ft at Amador Station). Real "
                "buildings there will cover less of the land. Parcel A-South at El Cerrito Plaza is outlined "
                "only: its approval gives stories, not feet."),
            "note": "Approved designs at three stations; height-limit envelopes, not designs, at the other three.",
            "sourceUrl": DOCS["wo_pdp"]["url"],
            "sourceLabel": "West Oakland plan, 2020 (PDF)",
            "georeference": geo,
            "license": f"Plans: City of Oakland and City of El Cerrito public records; parcels: {BART_LICENSE}; "
                       f"existing buildings: {OSM}",
            "documents": srcs + [BART_WORKPLAN, BART_REZONED, NB_ODS, BK_APR, ECP_APPROVAL, ECP_AS, EC_TOD,
                                 DUBLIN_NOD, WO_PAGE, LM_PAGE, BART_LM, BART_NEWS_WO],
        },
        "features": feats,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT}.geojson"
    out.write_text(json.dumps(tb._round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"[bart] wrote {out.relative_to(config.ROOT)}: {len(feats)} features, {out.stat().st_size / 1024:.0f} KB")
    for k, v in geo.items():
        if "rms_m" in v:
            print(f"    {k}: RMS {v['rms_m']} m")
        else:
            for kk, vv in v.items():
                print(f"    {k} {kk}: RMS {vv['rms_m']} m")


if __name__ == "__main__":
    main()
