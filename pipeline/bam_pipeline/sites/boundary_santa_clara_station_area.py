"""Santa Clara Station Area Specific Plan: the plan area from the County parcels the City listed.

The City of Santa Clara's Notice of Preparation of a Draft Program EIR (June 12, 2026, CEQAnet
SCH 2026060462) describes "approximately 244 acres" of properties "bounded by De La Cruz Boulevard, Reed
Street, and Martin Avenue to the northeast and Franklin Street and El Camino Real to the southwest", and
the City's CEQAnet filing lists the plan's 185 assessor's parcels ("Other Location Info"). The boundary
is the union of those parcels in the Santa Clara County parcel layer (data.sccgov.org ubcd-cewv), closed
over the streets between them:

1. 174 of the 185 APNs are in the County's current (FY 2026) layer. Of the 11 that aren't, 230-59-001,
   -002, 230-60-009 and 230-61-001 have been re-mapped on the same assessor's pages; their successors
   that lie inside the notice's Project Boundary and the City of Santa Clara (230-59-008, -009,
   230-60-010 and 230-61-006) are added. The others (230-05-045, -049, -050, -078, -096 and the condo
   common-area numbers 269-16-000 and 269-60-000) have no clear successor and are left out.
2. The parcels are joined over the streets between them by a 25 m closing, which also takes in the
   plan area's internal streets, as the notice's map does.

The parcel list and the notice's small-scale Figure 2 (PDF p. 4) don't agree everywhere: the listed
parcels take in residential blocks along Franklin, Benton, Alviso and Fremont streets, a Santa Clara
University parcel at 514 Franklin Street, parcels on De La Cruz Boulevard and Grant Street and two San
José parcels on Campbell Avenue that the figure's dashed line leaves out or crosses. The text's bounds
(De La Cruz, Reed and Martin to the northeast; Franklin and El Camino Real to the southwest) and the
244-acre total fit the parcels, so they are used, and the boundary stays approximate until the City
publishes a plan-area map. Figure 2 is still traced here (street pixels fitted to OpenStreetMap by
trimmed ICP, dashes read from the PDF), only to report how far the two lie apart.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_santa_clara_station_area
"""

from __future__ import annotations

import html
import re
import urllib.request

import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import shapely
from shapely.geometry import Polygon

from .. import trace
from . import line_georef as lg
from . import official_boundaries as ob
from . import traced_boundaries as tb

PROJECT = "santa-clara-station-area"
NOP_URL = "https://ceqanet.lci.ca.gov/2026060462/Attachment/mtsQbf"
NOP_SHA = "72ad0561f3af491cdabba82b3907f8e1440e5348bbf5cb2f30e7f1838384b03a"
NOP = tb.DOCS / "santa-clara-station-area-nop-2026-06.pdf"
CEQANET = "https://ceqanet.lci.ca.gov/2026060462"
PAGE = 3  # zero-based: PDF p. 4, Figure 2, Vicinity Map
K = 4.0  # render scale, px per PDF point
DASH = (0.69531, 0.67188, 0.63672, 0.73828)  # CMYK of the "Project Boundary" dashes
MAP_PT = (285.0, 150.0, 560.0, 450.0)  # window used for the street fit (PDF points: x0, top, x1, bottom)
SITE_PT = (340.0, 210.0, 470.0, 380.0)  # the dashed boundary lies inside this box (PDF points)
ANCHOR_PT = (370.0, 252.0)  # De La Cruz Boulevard meets Coleman Avenue
SCALE_M_PER_PT = 5000 * 0.3048 / 132.0  # 0-5,000 ft scale bar, about 132 pt long (refined by the fit)
STATED_ACRES = 244  # NOP p. 2 and CEQAnet "Total Acres"
BBOX = (-121.975, 37.330, -121.905, 37.375)
# Re-mapped successors of four listed APNs (see the module docstring).
SUCCESSORS = ["23059008", "23059009", "23060010", "23061006"]
CLOSE_M = 25.0
ROAD_CLASSES = {"motorway", "trunk", "primary", "secondary", "tertiary", "residential", "unclassified",
                "living_street"}


# ---------------------------------------------------------------- parcels (shared with boundary_redwood_life)

def parcel_site(name: str, spec: dict, close_m: float = 0.0):
    """Union of a parcel query (official_boundaries.fetch spec) in UTM, slivers closed at 0.5 m and, with
    close_m, joined over the streets between the parcels. Returns (site, number of parcels)."""
    utm = ob._utm_shapes(ob.fetch(name, spec))
    site = shapely.union_all(utm.buffer(0.5).to_numpy()).buffer(-0.5)
    if close_m:
        site = site.buffer(close_m, join_style="mitre").buffer(-close_m, join_style="mitre")
    return site.simplify(1.0, preserve_topology=True), len(utm)


def compare(site, traced) -> dict:
    """How far an official outline lies from the traced one it replaces (both UTM)."""
    return {
        "acres": round(site.area / tb.ACRE_M2, 1),
        "traced_acres": round(traced.area / tb.ACRE_M2, 1),
        "max_deviation_m": round(site.hausdorff_distance(traced), 1),
        "only_in_official_acres": round(site.difference(traced).area / tb.ACRE_M2, 1),
        "only_in_traced_acres": round(traced.difference(site).area / tb.ACRE_M2, 1),
    }


def listed_apns() -> list[str]:
    """The APNs on the CEQAnet record ("Other Location Info"), cached in data/raw/boundaries."""
    cache = ob.RAW / "santa-clara-station-area-ceqanet.html"
    if not cache.exists():
        ob.RAW.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(CEQANET, headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            cache.write_bytes(r.read())
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", cache.read_text(errors="ignore"))))
    i = text.index("Other Location Info")
    apns = re.findall(r"\d{3}-\d{2}-\d{3}", text[i:text.index("Notice of Completion", i)])
    if len(apns) != 185:
        raise SystemExit(f"expected 185 APNs on the CEQAnet record, found {len(apns)}")
    return [a.replace("-", "") for a in apns]


def parcels_spec(apns: list[str]) -> dict:
    return {"label": "Santa Clara County parcels",
            **ob.socrata(*ob.SCC_PARCELS, f"apn in ({ob._sql_list(apns)})")}


def _street_pixels(rgb: np.ndarray) -> np.ndarray:
    """Centreline pixels of the base map's streets (white) and arterials (pale yellow), in PDF points."""
    a = rgb.astype(int)
    white = (a.min(2) >= 252)
    yellow = (a[..., 0] >= 245) & (a[..., 1] >= 240) & (a[..., 2] >= 170) & (a[..., 2] <= 215)
    m = white | yellow
    x0, y0, x1, y1 = (int(v * K) for v in MAP_PT)
    win = np.zeros_like(m)
    win[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    skel = lg._thin(win)
    ys, xs = np.nonzero(skel)
    return np.c_[xs, ys].astype(float) / K


def dash_shape(pts) -> Polygon:
    """A dash as drawn. Corner and curved dashes have outlines that touch themselves, so the outline
    is repaired and its filled parts kept (their convex hull would fill the inside of the corner)."""
    g = shapely.make_valid(Polygon(pts))
    parts = [p for p in shapely.get_parts(g) if p.geom_type == "Polygon" and p.area > 0]
    shape = shapely.union_all(parts).buffer(0.1).buffer(-0.1) if parts else shapely.MultiPoint(pts).convex_hull
    return max(shapely.get_parts(shape), key=lambda p: p.area)


def _dashes() -> list[Polygon]:
    page = pdfplumber.open(str(NOP)).pages[PAGE]
    out = []
    for o in page.curves:
        if o.get("non_stroking_color") != DASH:
            continue
        x0, t0, x1, b0 = SITE_PT
        if not (x0 <= o["x0"] and o["x1"] <= x1 and t0 <= o["top"] and o["bottom"] <= b0):
            continue  # the legend's sample dash and other symbols in the dash colour
        out.append(dash_shape(o["pts"]))
    return out


def _enclosed(dashes, max_gap_m: float = 120.0):
    """The area a dashed line encloses. Each dash is joined to its two nearest dashes by the
    shortest line between them, which closes the gaps and follows the line round corners; the
    enclosed faces (the main area and, where the line crosses itself, the lobe south of The
    Alameda) are then grown by half a stroke so the boundary runs down the middle of the dashes."""
    polys = list(dashes)
    stroke = float(np.median([2 * p.area / p.length for p in polys]))
    joins = []
    for i, p in enumerate(polys):
        d = shapely.distance(p, polys)
        d[i] = np.inf
        for j in np.argsort(d)[:2]:
            if d[j] <= max_gap_m:
                joins.append(shapely.shortest_line(p, polys[j]).buffer(stroke / 2, cap_style="square"))
    ink = shapely.union_all(polys + joins)
    faces = [Polygon(h) for g in shapely.get_parts(ink) for h in g.interiors]
    faces = [f for f in faces if f.area > 0.05 * tb.ACRE_M2]
    if not faces:
        raise SystemExit("the dashed boundary did not close")
    site = shapely.union_all(faces).buffer(stroke / 2, join_style="mitre")
    # Smooth the steps the joins leave at each gap (a closing at the stroke width), then drop the
    # spurs a join can leave into a corner dash (an opening at half the stroke width).
    site = site.buffer(stroke, join_style="mitre").buffer(-stroke, join_style="mitre")
    return site.buffer(-stroke / 2, join_style="mitre").buffer(stroke / 2, join_style="mitre")


def traced_outline():
    """The Figure 2 outline (UTM) and its fit report: kept to compare with the parcels."""
    trace.fetch_document(NOP_URL, NOP, NOP_SHA)
    rgb = np.asarray(pdfium.PdfDocument(str(NOP))[PAGE].render(scale=K).to_pil().convert("RGB"))
    streets = tb.streets("scsa-santa_clara_station", BBOX)
    roads = streets[(streets["subtype"] == "road") & streets["class"].isin(ROAD_CLASSES)]
    target = shapely.union_all(roads.geometry.to_numpy())
    anchor = tb.intersection(streets, "De La Cruz Boulevard", "Coleman Avenue")
    init = lg.anchored(ANCHOR_PT, anchor, SCALE_M_PER_PT, 0.0)
    px = _street_pixels(rgb)
    sim, rep = lg.register_roads(px, target, init, keep=0.6, what="base-map street centrelines")

    dashes = [sim.geometry(d) for d in _dashes()]
    site = _enclosed(dashes).simplify(1.0, preserve_topology=True)
    return site, rep


def build() -> None:
    apns = listed_apns()
    spec = parcels_spec(apns + SUCCESSORS)
    found = {f["properties"]["apn"] for f in ob.fetch(PROJECT, spec)["features"]}
    missing = sorted(set(apns) - found)
    site, n = parcel_site(PROJECT, spec, CLOSE_M)
    acres = site.area / tb.ACRE_M2
    traced, rep = traced_outline()
    cmp = compare(site, traced)
    fmt = lambda a: f"{a[:3]}-{a[3:5]}-{a[5:]}"
    props = {
        "source": ("Santa Clara County parcels (data.sccgov.org ubcd-cewv): the assessor's parcels the City of Santa "
                   "Clara listed for the Santa Clara Station Area Specific Plan on its CEQAnet notice of preparation "
                   f"record (SCH 2026060462), {len(apns) - len(missing)} of {len(apns)} found in the County's FY 2026 "
                   f"layer plus {len(SUCCESSORS)} re-mapped successors, joined over the streets between them"),
        "sourceLabel": "Santa Clara County parcels",
        "sourceUrl": spec["landing"],
        "query": spec["url"],
        "documents": [CEQANET, NOP_URL, spec["landing"]],
        "documentSha256": NOP_SHA,
        "accuracy": "approximate",
        "accuracyNote": (
            "Approximate boundary: the parcels the City listed for the plan on CEQAnet, as the County maps them, "
            f"joined over the streets between them ({CLOSE_M:.0f} m closing). {acres:,.1f} acres as drawn, streets "
            f"included, against the notice's approximately {STATED_ACRES} acres. {len(missing)} listed APNs aren't "
            f"in the County's current layer; the re-mapped successors of four of them that lie inside the notice's "
            "Project Boundary are drawn. The list and the notice's small-scale Figure 2 differ at the edges: the "
            "parcels take in residential blocks along Franklin, Benton, Alviso and Fremont streets, a Santa Clara "
            "University parcel on Franklin Street, parcels on De La Cruz Boulevard and Grant Street and two San José "
            "parcels on Campbell Avenue that the figure's dashed line leaves out or crosses. The notice's written "
            "bounds and acreage fit the parcels. The outline traced from Figure 2 came to "
            f"{cmp['traced_acres']:,.1f} acres; the two lie up to {cmp['max_deviation_m']:.0f} m apart."),
        "license": "Santa Clara County open data (terms of use)",
        "features_used": n,
        "apnsListed": len(apns),
        "apnsNotInCountyLayer": [fmt(a) for a in missing],
        "successorsAdded": [fmt(a) for a in SUCCESSORS],
        "tracedComparison": {**cmp, "traced_from": "NOP Figure 2, Vicinity Map, PDF p. 4 (dashed Project Boundary), "
                             "fitted to OpenStreetMap streets", "traced_fit_rms_m": rep["rms_m"]},
    }
    tb.write(PROJECT, site, props)
    print(f"[{PROJECT}] parcels: {n} features ({len(missing)} listed APNs missing), {acres:,.1f} acres vs "
          f"{STATED_ACRES} stated; traced {cmp['traced_acres']:,.1f} acres, max deviation {cmp['max_deviation_m']} m")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
