"""The Orchards (former Chevron Park, San Ramon): the site traced from the approved Vesting Tentative Map.

The City approved the Orchards Master Plan and Vesting Tentative Map 9693 (Planning Commission Resolution
02-26, Feb 3, 2026; City Council Resolution 2026-040, Apr 7, 2026, denying the appeal) on "the 92-acre
site at 6001 Bollinger Canyon Road (formerly Chevron Office Park, APN: 213-120-008)". Contra Costa
County's parcel service and the City's GIS server can't be reached from this pipeline, so the parcel is
traced from the approved plan set instead: "D. Applicant's Project Plans, dated September 5, 2025"
(City of San Ramon Laserfiche record 20812236, the set the Council's conditions refer to).

1. The plan set's civil sheets are CAD drawings at 1" = 100'. Sheet C3.0, Existing Conditions (PDF
   p. 179), draws the project boundary (2.7-pt line) around "PARCEL A, DN 2000-0220096, 91.55 AC±"; at
   the sheet's scale the outline encloses that area to within a few hundredths of an acre, which checks
   the scale. Sheet C2.0, Overall Lotting Plan (PDF p. 172), draws the same boundary with the new
   parcels and lots (massing_the_orchards.py) and is related to C3.0 by a plain shift.
2. C3.0 also draws the existing campus buildings and the buildings around the site. Their outlines are
   placed on OpenStreetMap building footprints (via Overture): rotation and shift by cross-correlation
   of the filled outlines over a grid of rotations, then a rigid trimmed ICP of the outline edges with
   the scale held at 1" = 100' (RMS reported).

The outline first drawn for the map was traced from the City's 2040 General Plan Draft EIR Figure 2-4
(PDF p. 67, about 9 m per pixel); it is still traced here (traced_outline) to start the fit and to
report the difference.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_the_orchards
"""

from __future__ import annotations

import io
from functools import lru_cache

import cv2
import pdfplumber
import numpy as np
import pypdf
import shapely
import shapely.affinity
from PIL import Image
from shapely.geometry import LineString, Polygon

from .. import trace
from . import traced_boundaries as tb

PROJECT = "the-orchards"
DEIR_URL = "https://ceqanet.lci.ca.gov/2022060549/2/Attachment/ueWNFZ"
DEIR_SHA = "ad3c1dca1ee6ab79f48f656d79340a2004e3790d317a9c49f3a55d33df97c392"
DEIR = tb.DOCS / "san-ramon-2040-general-plan-draft-eir-2023-08.pdf"
PAGE = 66  # zero-based: PDF p. 67, Figure 2-4
NOE_URL = "https://ceqanet.lci.ca.gov/2026020219/Attachment/G7E_Xs"
BBOX = (-121.99, 37.745, -121.955, 37.77)
PLANS = {
    "url": "https://docs.sanramon.ca.gov/WebLink/ElectronicFile.aspx?docid=20812236&dbid=0&repo=sanramon",
    "view": "https://docs.sanramon.ca.gov/WebLink/DocView.aspx?id=20812236&dbid=0&repo=sanramon",
    "file": "orchards-project-plans-2025-09-05.pdf",
    "sha256": "afee4df22d3c8d1b9aef8b6c3c56a84c581f08d107c20a0771be2c6ef7140d8b",
}
C20, C30 = 171, 178  # zero-based: PDF pp. 172 (Overall Lotting Plan) and 179 (Existing Conditions)
M_PER_PT = 100 * 0.3048 / 72  # 1" = 100'
PARCEL_A_ACRES = 91.55  # C3.0: "PARCEL A, DN 2000-0220096, 91.55 AC±"
COUNCIL_URL = "https://docs.sanramon.ca.gov/WebLink/DocView.aspx?id=21620060&dbid=0&repo=sanramon"
GREYS = ("(0.651, 0.651, 0.651)", "(0.412, 0.412, 0.412)")  # existing buildings and site features on C3.0

OFFICE_BGR = (204, 217, 255)  # the figure's "Office" fill
ORANGE_BGR = (0, 152, 230)  # I-680
GREEN_BGR = (130, 225, 130)  # Iron Horse Trail (also parks; only a narrow corridor is used)
GREY_BGR = (178, 178, 178)  # streets
WINDOW = (800, 800, 940, 900)  # x0, y0, x1, y1 around Chevron Park

# Road crossings read off the figure (pixel x, y), with the OpenStreetMap streets they match.
CONTROLS = [
    ((796.0, 836.0), "Bollinger Canyon Road", None),  # I-680 band centre (motorway lines)
    ((874.0, 813.0), "Bollinger Canyon Road", "Camino Ramon"),
    ((897.0, 806.0), "Bollinger Canyon Road", "San Ramon Valley Iron Horse Trail"),
]


# ---------------------------------------------------------------- the approved plan set (sheets C2.0 and C3.0)

def plans_pdf():
    return trace.fetch_document(PLANS["url"], tb.DOCS / PLANS["file"], PLANS["sha256"])


@lru_cache(maxsize=2)
def sheet(page: int) -> tuple[list[dict], list[dict]]:
    """Vector objects (points in PDF points, y down; stroke colour; line width) and words of a plan sheet."""
    p = pdfplumber.open(str(plans_pdf())).pages[page]
    objs = [{"pts": [tuple(map(float, q)) for q in o["pts"]], "sc": str(o.get("stroking_color")),
             "lw": round(o.get("linewidth") or 0, 2)}
            for o in p.curves + p.lines if len(o.get("pts") or []) >= 2]
    words = p.extract_words()
    return objs, words


def boundary_pt(page: int) -> Polygon:
    """The project boundary (the 2.7-pt line) as a polygon in PDF points; the sheet frame's long rule at the
    bottom is dropped. The line's pieces are joined by a 1-pt buffer and the enclosed hole taken."""
    objs, _ = sheet(page)
    ls = [LineString(o["pts"]) for o in objs if o["sc"] == "0" and o["lw"] == 2.7]
    ls = [g for g in ls if g.bounds[1] < 1950]
    ink = shapely.union_all([g.buffer(1.0) for g in ls])
    holes = [Polygon(h) for part in shapely.get_parts(ink) for h in part.interiors]
    return max(holes, key=lambda h: h.area).buffer(1.0, join_style="mitre")


def c20_shift() -> tuple[float, float]:
    """C2.0 -> C3.0 offset (PDF points): the two sheets draw the same boundary."""
    a, b = boundary_pt(C20), boundary_pt(C30)
    dx, dy = b.centroid.x - a.centroid.x, b.centroid.y - a.centroid.y
    if shapely.affinity.translate(a, dx, dy).hausdorff_distance(b) > 1.0:
        raise SystemExit("C2.0 and C3.0 boundaries differ by more than a shift")
    return dx, dy


def _existing_outlines() -> list[Polygon]:
    """Closed outlines of buildings on C3.0 (grey, 1,500-80,000 pt2), without thin shapes (parking islands)."""
    objs, _ = sheet(C30)
    out = []
    for o in objs:
        p = o["pts"]
        if o["sc"] not in GREYS or len(p) < 4 or np.hypot(p[0][0] - p[-1][0], p[0][1] - p[-1][1]) > 0.5:
            continue
        g = Polygon(p)
        if not g.is_valid or not 1500 < g.area < 80000:
            continue
        r = np.asarray(g.minimum_rotated_rectangle.exterior.coords)
        e = sorted([np.hypot(*(r[1] - r[0])), np.hypot(*(r[2] - r[1]))])
        if e[1] / max(e[0], 1e-6) > 5 or g.area / Polygon(r).area < 0.5:
            continue
        out.append(Polygon(g.exterior))
    return out


def _fill(geoms, x0, y0, w, res=1.0) -> np.ndarray:
    m = np.zeros((w, w), np.float32)
    for g in geoms:
        for part in getattr(g, "geoms", [g]):
            xy = np.asarray(part.exterior.coords)
            px = np.c_[(xy[:, 0] - x0) / res, (y0 + w * res - xy[:, 1]) / res]
            cv2.fillPoly(m, [np.round(px).astype(np.int32)], 1.0)
    return m


@lru_cache(maxsize=1)
def georeference() -> tuple[trace.Similarity, dict]:
    """C3.0 (PDF points, y down) -> UTM 10N at 1" = 100'."""
    bnd = boundary_pt(C30)
    traced, _ = traced_outline()
    polys = _existing_outlines()
    bld = tb.buildings("orchards", BBOX)
    c = np.array(bnd.centroid.coords[0])
    tc = np.array(traced.centroid.coords[0])
    w = 1400
    x0, y0 = tc[0] - w / 2, tc[1] - w / 2
    bld = bld[bld.intersects(shapely.box(x0, y0, x0 + w, y0 + w))]
    fb = np.fft.fft2(_fill(bld.geometry, x0, y0, w))
    best = None
    lim = 120  # shifts searched, m
    for rot in np.arange(24.0, 32.01, 0.1):  # the sheets are drawn about 28 degrees off north
        sim = trace.Similarity(M_PER_PT, np.radians(rot), 0.0, 0.0)
        o = sim.apply([c])[0]
        sim.tx, sim.ty = tc - o
        md = _fill([sim.geometry(p) for p in polys], x0, y0, w)
        f = np.fft.ifft2(fb * np.conj(np.fft.fft2(md))).real
        f = np.roll(np.roll(f, lim, 0), lim, 1)[:2 * lim, :2 * lim]
        iy, ix = np.unravel_index(np.argmax(f), f.shape)
        share = f[iy, ix] / md.sum()
        if best is None or share > best[0]:
            best = (share, rot, sim, ix - lim, iy - lim)
    share, rot, sim, dx, dy = best
    sim.tx, sim.ty = sim.tx + dx, sim.ty - dy
    pts = []
    for g in polys:
        n = max(8, int(g.exterior.length / 2))
        pts += [g.exterior.interpolate(s, normalized=True).coords[0] for s in np.linspace(0, 1, n, endpoint=False)]
    pts = np.array(pts)
    edges = shapely.union_all(bld.boundary.to_numpy())
    keep = 0.5
    sim, d = tb.icp(pts, [edges], np.zeros(len(pts), int), sim, keep=keep, scale=M_PER_PT)
    rep = tb.icp_report(sim, d, keep, f"{len(polys)} building outlines on sheet C3.0 against OpenStreetMap building "
                        "footprints (rotation and shift; scale held at 1\" = 100')")
    rep["start"] = (f"cross-correlation of the filled outlines: rotation {rot:.1f} deg, {share:.0%} of the drawn "
                    "outline area on mapped buildings")
    return sim, rep


def c20_to_utm(g):
    """A C2.0 geometry (PDF points) in UTM."""
    sim, _ = georeference()
    dx, dy = c20_shift()
    return sim.geometry(shapely.affinity.translate(g, dx, dy))


def _image() -> np.ndarray:
    trace.fetch_document(DEIR_URL, DEIR, DEIR_SHA)
    page = pypdf.PdfReader(str(DEIR)).pages[PAGE]
    img = Image.open(io.BytesIO(page.images[0].data)).convert("RGB")
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def _is(im: np.ndarray, bgr) -> np.ndarray:
    return np.all(im == np.array(bgr, np.uint8), axis=2)


def _band_centres(mask: np.ndarray, rows: bool) -> np.ndarray:
    """Middle of the band in each row (rows=True) or column, as pixel (x, y) points."""
    pts = []
    if rows:
        for y in range(mask.shape[0]):
            xs = np.flatnonzero(mask[y])
            if len(xs) >= 2:
                pts.append((xs.mean() + 0.5, y + 0.5))
    else:
        for x in range(mask.shape[1]):
            ys = np.flatnonzero(mask[:, x])
            if len(ys) >= 2:
                pts.append((x + 0.5, ys.mean() + 0.5))
    return np.array(pts, float)


def _corridor(shape, p0, p1, half: float) -> np.ndarray:
    m = np.zeros(shape, np.uint8)
    cv2.line(m, tuple(int(v) for v in p0), tuple(int(v) for v in p1), 255, int(2 * half))
    return m > 0


def figure_georeference(im: np.ndarray, streets) -> tuple[trace.Similarity, dict]:
    motorway = shapely.union_all(streets[streets["class"] == "motorway"].geometry.to_numpy())
    boll = shapely.union_all(streets[streets["name"] == "Bollinger Canyon Road"].geometry.to_numpy())
    trail = shapely.union_all(streets[streets["name"] == "San Ramon Valley Iron Horse Trail"].geometry.to_numpy())
    src, dst, labels = [], [], []
    for px, a, b in CONTROLS:
        if b is None:
            x = motorway.intersection(boll)
            c = shapely.MultiPoint([g for g in getattr(x, "geoms", [x])]).centroid
            dst.append((c.x, c.y))
            labels.append("Bollinger Canyon Rd / I-680")
        else:
            dst.append(tb.intersection(streets, a, b))
            labels.append(f"{a} / {b}".replace(" Road", " Rd").replace("San Ramon Valley ", ""))
        src.append(px)
    init = trace.fit_similarity(np.array(src), np.array(dst), labels)

    # Bands near the site: I-680 (orange), the trail (green, in a narrow corridor), Bollinger (grey, in a corridor).
    H, W = im.shape[:2]
    win = np.zeros((H, W), bool)
    win[760:900, 770:960] = True
    orange = _is(im, ORANGE_BGR) & win
    green = _is(im, GREEN_BGR) & _corridor((H, W), (905, 770), (950, 890), 4) & win
    grey = _is(im, GREY_BGR) & _corridor((H, W), (790, 840), (910, 800), 5)
    p_or = _band_centres(orange, rows=True)
    p_gr = _band_centres(green, rows=True)
    p_bo = _band_centres(grey, rows=False)
    pts = np.vstack([p_or, p_gr, p_bo])
    groups = np.concatenate([np.zeros(len(p_or), int), np.ones(len(p_gr), int), np.full(len(p_bo), 2)])
    # I-680's band is drawn over both carriageways; match it to the middle of the two.
    sim, d = tb.icp(pts, [motorway, trail, boll], groups, init, keep=0.8)
    rep = tb.icp_report(sim, d, 0.8, "I-680, Iron Horse Trail and Bollinger Canyon Rd bands against OpenStreetMap")
    rep["initial_controls"] = init.report()
    return sim, rep


@lru_cache(maxsize=1)
def traced_outline():
    """The 2040 General Plan Draft EIR Figure 2-4 outline (UTM) and its fit report."""
    im = _image()
    streets = tb.streets("orchards", BBOX)
    sim, rep = figure_georeference(im, streets)

    office = _is(im, OFFICE_BGR).astype(np.uint8)
    x0, y0, x1, y1 = WINDOW
    win = np.zeros_like(office)
    win[y0:y1, x0:x1] = office[y0:y1, x0:x1]
    n, lab, st, _ = cv2.connectedComponentsWithStats(win, connectivity=4)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    lot = (lab == k).astype(np.uint8)
    contours, _ = cv2.findContours(lot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(contours, key=cv2.contourArea)[:, 0, :].astype(float) + 0.5  # pixel centres
    # Pixel-centre outline -> outer pixel edge (+0.5 px) -> middle of the 1-px parcel line (+0.5 px).
    lot_px = Polygon(c).buffer(1.0, join_style="mitre")
    site = shapely.transform(lot_px, lambda xy: sim.apply(xy))
    site = site.simplify(3.0, preserve_topology=True)
    return site, rep


def main() -> None:
    sim, rep = georeference()
    bnd = boundary_pt(C30)
    drawn_acres = bnd.area * M_PER_PT**2 / tb.ACRE_M2
    site = sim.geometry(bnd).simplify(0.5, preserve_topology=True)
    acres = site.area / tb.ACRE_M2
    traced, trep = traced_outline()
    cmp = {
        "acres": round(acres, 1),
        "traced_acres": round(traced.area / tb.ACRE_M2, 1),
        "max_deviation_m": round(site.hausdorff_distance(traced), 1),
        "only_in_new_acres": round(site.difference(traced).area / tb.ACRE_M2, 1),
        "only_in_traced_acres": round(traced.difference(site).area / tb.ACRE_M2, 1),
        "traced_from": "2040 General Plan Draft EIR Figure 2-4 (PDF p. 67), about 9 m per pixel",
        "traced_fit_rms_m": trep["rms_m"],
    }
    tb.write(PROJECT, site, {
        "source": ("traced: City of San Ramon, Orchards Vesting Tentative Map 9693 (Applicant's Project Plans dated "
                   "Sept 5, 2025, approved by Planning Commission Resolution 02-26 and City Council Resolution 2026-040), "
                   "sheet C3.0 Existing Conditions (PDF p. 179): the project boundary around Parcel A "
                   "(DN 2000-0220096, 91.55 acres), APN 213-120-008"),
        "sourceLabel": "Vesting tentative map, sheet C3.0 (2025)",
        "sourceUrl": PLANS["view"],
        "documents": [PLANS["view"], COUNCIL_URL, NOE_URL, DEIR_URL],
        "documentSha256": PLANS["sha256"],
        "accuracy": "traced",
        "accuracyShort": f"RMS {rep['rms_m']:.1f} m",
        "accuracyNote": (
            "The parcel as the approved vesting tentative map draws it: the project boundary around Parcel A "
            "(91.55 acres; the City's approvals say about 92), APN 213-120-008. The CAD sheet's shape is exact at "
            f"1\" = 100' (it encloses {drawn_acres:.2f} acres at that scale); it is placed on OpenStreetMap building "
            f"footprints using the existing buildings the sheet draws (trimmed RMS {rep['rms_m']:.1f} m, median "
            f"{rep['median_m']:.1f} m), so its position is good to a few metres. Contra Costa County's parcel map "
            f"couldn't be reached to check it. {acres:.1f} acres as drawn. The outline traced earlier from the 2040 "
            f"General Plan EIR's land-use map came to {cmp['traced_acres']:.1f} acres and lies up to "
            f"{cmp['max_deviation_m']:.0f} m from this one. The Council resolution's heading gives the parcel as "
            "APN 213-701-002, its text as 213-120-008."),
        "officialAcres": PARCEL_A_ACRES,
        "officialAcresSource": PLANS["view"],
        "license": ("Traced facts from a public City of San Ramon record (the PDF is not redistributed). "
                    f"Georeference: {tb.OSM_LICENSE}."),
        "georeference": rep,
        "tracedComparison": cmp,
    })
    print(f"[{PROJECT}] {acres:.1f} acres (drawn {drawn_acres:.2f} at 1\"=100'), fit RMS {rep['rms_m']} m, "
          f"median {rep['median_m']} m; traced {cmp['traced_acres']} acres, max deviation {cmp['max_deviation_m']} m")


if __name__ == "__main__":
    main()
