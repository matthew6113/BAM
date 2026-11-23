"""Santana Row Master Plan Update (San José): the project site as the County parcels inside the NOP's lot diagram.

Source: City of San José, Revised Notice of Preparation of an EIR for the Santana Row Master Plan Update (files
PDC22-004 and ER22-107, February 2026; CEQAnet SCH 2013122059, document 3, attachment lrKplZ):
- cover (PDF p. 1): "APNs: 277-33-017, 277-33-019, 277-33-020 277-40-029, 277-40-031, 277-38-003 277-38-004,
  277-38-005, & 277-38-012";
- p. 4: "The approximately 42.53-acre project site is located at the southeast corner of Stevens Creek Boulevard and
  Winchester Boulevard";
- Figure 4, "Lot Division Diagram" (PDF p. 8, "Source: WRNS Studio, February 18, 2022"): the lots of Santana Row
  with the project boundary as a blue dashed line. North points to the right of the page. The main outline is part
  of the figure's raster base; the Lot 22 outline, added in 2026, is a vector dashed line.

The nine APNs are only the lots that would change (Lot 1A/B/C, 2B, 10A, 17 and 22): about 5.9 acres of the 42.53.
The rest of the site isn't listed by APN, so it is taken from Figure 4:

1. Santa Clara County parcels (data.sccgov.org ubcd-cewv) in a box around Santana Row.
2. The figure's dashed line: the blue pixels of the page rendered at 4 px per point; the enclosed faces (the main
   site and Lot 22), grown by half a stroke, are the traced outline.
3. Georeference: a similarity from the five lot labels to the NOP's parcels (LOT 1 to 277-33-019, the middle of the
   three Lot 1 parcels along Stevens Creek Boulevard; LOT 2B to 277-40-029; LOT 10A to 277-40-031; LOT 17 to the
   three Dudley Avenue parcels 277-38-003 to -005, which the NOP merges into Lot 17; LOT 22 to 277-38-012, the
   County's 0.54-acre parcel), refined by trimmed ICP of the dashed-line pixels to the outline of the parcels
   selected in step 4 (two rounds).
4. Site: the nine NOP parcels plus every parcel whose representative point lies inside the traced outline and
   at least half of whose area does (the condominium parcels stack inside the blocks), joined at 0.5 m.

The outline and the parcels agree to about a metre or two except at Lot 22, which the figure draws smaller than
the County parcel; the parcel is drawn. Accuracy: approximate (the parcels are official, but the NOP names only
nine of them; the rest are chosen by the figure).

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_santana_row
"""

from __future__ import annotations

import re

import geopandas as gpd
import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import shapely
from shapely.geometry import LineString, Polygon

from .. import config, trace
from . import official_boundaries as ob
from . import traced_boundaries as tb
from .boundary_santa_clara_station_area import compare

PROJECT = "santana-row"
CEQANET = "https://ceqanet.lci.ca.gov/2013122059/3"
NOP = {
    "title": "Revised Notice of Preparation of an EIR, Santana Row Master Plan Update (City of San José, February 2026)",
    "url": "https://ceqanet.lci.ca.gov/2013122059/3/Attachment/lrKplZ",
    "sha256": "7710e9c5f61258d22ea82bdacba605f385157fd66c20b8d1777f873e14f874f9",
    "file": "nop-2026-02.pdf",
}
PAGE = 7  # zero-based: PDF p. 8, Figure 4
K = 4  # render scale, px per PDF point
FRAME_PT = (53.0, 103.0, 751.0, 485.0)  # the map frame (x0, top, x1, bottom); the north arrow is black
STROKE_PT = 2.5  # half-gap closing for the dashes (the line is about 1.75 pt wide, dashes 5 on 3 off)
STATED_ACRES = 42.53

# The NOP's nine APNs, by lot (the lot each lies in on Figure 4; Lot 17 is "524, 534, and 544 Dudley Avenue").
LOTS = {
    "Lot 1A/B/C": {"label": "LOT 1", "apns": ["27733020", "27733019", "27733017"], "control": "27733019"},
    "Lot 2B": {"label": "LOT 2B", "apns": ["27740029"], "control": "27740029"},
    "Lot 10A": {"label": "LOT 10A", "apns": ["27740031"], "control": "27740031"},
    "Lot 17": {"label": "LOT 17", "apns": ["27738003", "27738004", "27738005"], "control": None},
    "Lot 22": {"label": "LOT 22", "apns": ["27738012"], "control": "27738012"},
}
NOP_APNS = [a for lot in LOTS.values() for a in lot["apns"]]
AREA = {
    "label": "Santa Clara County parcels",
    **ob.socrata(*ob.SCC_PARCELS, "within_box(the_geom, 37.3245, -121.9535, 37.3150, -121.9425)"),
}


def fmt(apn: str) -> str:
    return f"{apn[:3]}-{apn[3:5]}-{apn[5:]}"


def nop_path():
    return trace.fetch_document(NOP["url"], config.ROOT / "data" / "raw" / "official" / PROJECT / NOP["file"],
                                NOP["sha256"])


def parcels() -> gpd.GeoDataFrame:
    """The County parcels around Santana Row, in UTM, with their APN and object id."""
    fc = ob.fetch(f"{PROJECT}-area", AREA)
    rows = [f for f in fc["features"] if f.get("geometry")]
    geoms = [shapely.make_valid(shapely.geometry.shape(f["geometry"])) for f in rows]
    g = gpd.GeoDataFrame({"apn": [f["properties"].get("apn") for f in rows],
                          "objectid": [f["properties"].get("objectid") for f in rows]},
                         geometry=geoms, crs=4326).to_crs(ob.UTM)
    missing = sorted(set(NOP_APNS) - set(g["apn"].dropna()))
    if missing:
        raise SystemExit(f"{PROJECT}: NOP parcels missing from the County layer: {', '.join(map(fmt, missing))}")
    return g


def lot_shape(g: gpd.GeoDataFrame, apns: list[str]):
    return shapely.union_all(g[g["apn"].isin(apns)].buffer(0.5).to_numpy()).buffer(-0.5)


def figure() -> tuple[np.ndarray, dict]:
    """Figure 4's dashed-line pixels and its lot labels (page points, y down)."""
    path = nop_path()
    page = pdfplumber.open(str(path)).pages[PAGE]
    words = page.extract_words(keep_blank_chars=True)
    # The labels use a subset font whose codes are the ASCII codes less 29 ("(cid:47)(cid:50)(cid:55)" = "LOT").
    decode = lambda t: re.sub(r"\(cid:(\d+)\)", lambda m: chr(int(m.group(1)) + 29), t).strip()
    text = [decode(w["text"]) for w in words]
    if "LOT DIVISION DIAGRAM" not in " ".join(text) and "DIAGRAM" not in text:
        raise SystemExit(f"PDF page {PAGE + 1} is not Figure 4, Lot Division Diagram")
    labels = {t: ((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2) for t, w in zip(text, words)
              if t.startswith("LOT ")}
    rgb = np.asarray(pdfium.PdfDocument(str(path))[PAGE].render(scale=K).to_pil().convert("RGB")).astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    ys, xs = np.nonzero((b - r > 50) & (b > 90) & (r < 120))  # the blue dashes, about (37, 64, 128)
    pts = np.unique(np.round(np.column_stack([xs, ys]) / K * 2) / 2, axis=0)  # half-point grid
    x0, t0, x1, b0 = FRAME_PT
    pts = pts[(pts[:, 0] > x0) & (pts[:, 0] < x1) & (pts[:, 1] > t0) & (pts[:, 1] < b0)]
    return pts, labels


def traced_outline_pt(pts: np.ndarray) -> Polygon:
    """The faces the dashed line encloses (the main site and Lot 22), grown to the middle of the line."""
    ink = shapely.union_all(shapely.buffer(shapely.points(pts), STROKE_PT))
    faces = sorted((Polygon(h) for part in shapely.get_parts(ink) for h in part.interiors), key=lambda f: -f.area)
    if len(faces) < 2 or faces[1].area < 500:
        raise SystemExit(f"{PROJECT}: Figure 4's dashed line did not close into the site and Lot 22")
    return shapely.union_all([f.buffer(STROKE_PT, join_style="mitre") for f in faces[:2]])


def select(g: gpd.GeoDataFrame, outline) -> gpd.GeoDataFrame:
    """The NOP parcels plus the parcels inside the outline (representative point in, at least half the area in)."""
    zone = outline.buffer(3.0)
    inside = g.representative_point().within(outline) & (g.intersection(zone).area >= 0.5 * g.area)
    return g[inside | g["apn"].isin(NOP_APNS)]


def georeference(g: gpd.GeoDataFrame) -> tuple[trace.Similarity, Polygon, dict, gpd.GeoDataFrame]:
    pts, labels = figure()
    src, dst, names = [], [], []
    for name, lot in LOTS.items():
        src.append(labels[lot["label"]])
        dst.append((lot_shape(g, [lot["control"]]) if lot["control"] else lot_shape(g, lot["apns"])).centroid.coords[0])
        names.append(name)
    sim = init = trace.fit_similarity(src, dst, names)
    outline_pt = traced_outline_pt(pts)
    for _ in range(2):
        sel = select(g, sim.geometry(outline_pt))
        site = shapely.union_all(sel.buffer(0.5).to_numpy()).buffer(-0.5)
        target = shapely.union_all([LineString(p.exterior.coords) for p in shapely.get_parts(site)])
        sim = trace.icp_similarity(pts, target, init, keep=0.8)
    sel = select(g, sim.geometry(outline_pt))
    # Each NOP lot's label must fall inside its parcels.
    checks = {}
    for name, lot in LOTS.items():
        p = shapely.Point(sim.apply([labels[lot["label"]]])[0])
        shape = lot_shape(g, lot["apns"])
        checks[name] = round(float(p.distance(shape)), 1)
        if not p.within(shape.buffer(1.0)):
            raise SystemExit(f"{PROJECT}: Figure 4's {lot['label']} label lands {checks[name]} m outside APNs "
                             f"{', '.join(map(fmt, lot['apns']))}")
    sim.label_start = init  # type: ignore[attr-defined]
    return sim, outline_pt, checks, sel


def build() -> None:
    g = parcels()
    sim, outline_pt, checks, sel = georeference(g)
    site = shapely.union_all(sel.buffer(0.5).to_numpy()).buffer(-0.5).simplify(1.0, preserve_topology=True)
    traced = sim.geometry(outline_pt).simplify(1.0, preserve_topology=True)
    cmp = compare(site, traced)
    acres = site.area / tb.ACRE_M2
    nop_acres = lot_shape(g, NOP_APNS).area / tb.ACRE_M2
    lot22 = lot_shape(g, LOTS["Lot 22"]["apns"]).area / tb.ACRE_M2
    n_null = int(sel["apn"].isna().sum())
    props = {
        "source": ("Santa Clara County parcels (data.sccgov.org ubcd-cewv) inside the project boundary of Figure 4, "
                   "Lot Division Diagram, of San José's Revised Notice of Preparation for the Santana Row Master Plan "
                   "Update (February 2026; CEQAnet SCH 2013122059), with the nine parcels the notice names "
                   f"({', '.join(map(fmt, NOP_APNS))})"),
        "sourceLabel": "Santa Clara County parcels",
        "sourceUrl": AREA["landing"],
        "query": AREA["url"],
        "documents": [CEQANET, NOP["url"], AREA["landing"]],
        "documentSha256": NOP["sha256"],
        "accuracy": "approximate",
        "accuracyNote": (
            "Approximate boundary: the notice of preparation names only the nine parcels that would change "
            f"(Lots 1A/B/C, 2B, 10A, 17 and 22; {nop_acres:,.1f} acres), so the rest of the approximately 42.53-acre "
            "site is the County parcels inside the dashed project boundary of the notice's Figure 4, including the "
            f"private streets and the condominium parcels inside the blocks. {acres:,.1f} acres as drawn, of which "
            f"Lot 22 (added in 2026, after the 42.53-acre figure was first published in 2022) is {lot22:,.2f}. The "
            f"figure's outline, fitted to the parcels (RMS {sim.rms_m:.1f} m), lies up to {cmp['max_deviation_m']:.0f} m "
            "from them, the most at Lot 22, which the figure draws smaller than the County's parcel."),
        "license": "Santa Clara County open data (terms of use)",
        "features_used": int(len(sel)),
        "parcelsWithoutApn": n_null,
        "apnsNamed": [fmt(a) for a in NOP_APNS],
        "georeference": {
            "method": ("Figure 4 (PDF p. 8): a similarity from the five lot labels to the NOP's parcels, refined by "
                       "trimmed ICP of the blue dashed-line pixels to the selected parcels' outline."),
            **sim.report(),
            "label_start": sim.label_start.report(),
            "label_distance_to_lot_m": checks,
        },
        "tracedComparison": {**cmp, "traced_from": "NOP Figure 4, Lot Division Diagram, PDF p. 8 (blue dashed "
                             "project boundary)"},
    }
    tb.write(PROJECT, site, props)
    print(f"[{PROJECT}] {len(sel)} parcels ({n_null} without APN), {acres:,.2f} acres vs {STATED_ACRES} stated; NOP "
          f"parcels {nop_acres:,.2f} acres; fit RMS {sim.rms_m:.2f} m (labels {sim.label_start.rms_m:.1f} m); traced "
          f"{cmp['traced_acres']:,.1f} acres, max deviation {cmp['max_deviation_m']} m")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
