"""Oceanwide Center: the two approved towers, traced from the CPE checklist's floor plans.

Source:
- Community Plan Exemption Checklist, 50 First Street (Oceanwide Center), Case 2006.1523E (SF Planning,
  2016), Figure 2 "Project Site Level 1 Floor Plan" (PDF page 6) and Figure 3 "First Street Tower,
  Typical Office Floor Plan (Flr. 28)" (PDF page 7). Both are vector drawings with the property line in
  red.
- Heights from Planning Commission Motion 19635 (Downtown Project Authorization, May 5, 2016): the First
  Street Tower's roof at about 850 ft, "with mechanical and architectural features extending to a height
  of 910"; the Mission Street Tower at about 605 ft, with screening to 625 ft and elevator equipment to
  636 ft. The CPE checklist gives the same figures (Table 2: 60 and 54 stories).

How it's drawn:
- Figure 2's red property line is matched, corner by corner, to the DataSF parcels of the site (the
  boundary file; the same lots and vacated street areas), by a least-squares similarity. The RMS is
  reported.
- The Mission Street Tower is the rectangle of corner columns in Figure 2: it runs from the Mission
  Street property line to its fourth column line, and from the Ecker Place line across the realigned
  Jessie Street. Motion 19635 gives its lower floors as 133 ft long with a 164 ft 11 in diagonal, which
  the traced rectangle matches to within a few feet.
- The First Street Tower is the typical office floor of Figure 3 (the slab and its two cores). Figure 3
  is registered to Figure 2 through the property-line corners both show, then carried to the map with
  Figure 2's transform.
- Both are extruded to their roof heights as single volumes: the tower setbacks, the First Street
  Tower's 68-ft "urban room", the podium-level retail and the rehabilitated 78 and 88 First Street
  buildings are not modelled. Illustrative.

Stage: excavation, shoring and the first foundation pours for the Mission Street Tower were inspected
under DBI permits from 2017; the last recorded inspection on its site permit is Sept 21, 2020. Neither
tower rose above ground, so both are drawn at the project's stage ("paused").

    uv run --directory pipeline python -m bam_pipeline.sites.massing_oceanwide_center
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "oceanwide-center"
UTM = ob.UTM
SQFT = 10.7639

CPE = {
    "title": "Community Plan Exemption Checklist, 50 First Street (Oceanwide Center), Case No. 2006.1523E",
    "url": "https://sfmea.sfplanning.org/2006.1523E_Checklist.pdf",
    "sha256": "9695904d4d1d2ef7f8bb732ae6a5c658ddaef9150c6ae9224a47f5d25f89efe3",
    "file": "2006.1523E_Checklist.pdf",
}
MOTION = ("Planning Commission Motion No. 19635 (Downtown Project Authorization), May 5, 2016, "
          "Board of Supervisors File No. 160382")
MOTION_URL = "https://sfgov.legistar.com/View.ashx?M=F&ID=4454990&GUID=A40F1C7E-8BCB-4D64-AC85-1CFCDFB96DF1"

FIG2_PAGE, FIG3_PAGE = 6, 7  # 1-based PDF pages

# Corners of the red property line in Figure 2 (PDF points, y down), each with a point near the same
# corner of the parcels in UTM 10N; the code snaps that point to the nearest parcel vertex.
FIG2_CONTROLS = [
    ("First / Mission corner (lot 009)", (191, 422), (553025.4, 4182660.6)),
    ("First / Stevenson corner (lot 003)", (633, 422), (552948.0, 4182736.2)),
    ("Mission / Ecker corner (lot 012)", (191, 111), (552971.8, 4182606.5)),
    ("Ecker Place, rear of lot 012", (315, 111), (552950.1, 4182627.7)),
    ("Stevenson Street, rear of lot 055", (633, 214), (552912.1, 4182700.0)),
    ("Rear corner of lot 055", (533, 214), (552929.5, 4182683.0)),
    ("Rear jog of lot 055", (533, 261), (552937.7, 4182690.9)),
    ("Rear of lot 006", (424, 261), (552956.9, 4182672.1)),
    ("Rear jog of lot 006", (424, 230), (552951.8, 4182666.6)),
    ("Rear of lot 007", (362, 230), (552962.4, 4182656.1)),
    ("Rear corner of lot 011", (315, 228), (552970.0, 4182647.9)),
]

# The same property-line corners in Figure 3 (left) and Figure 2 (right), PDF points.
FIG3_TO_FIG2 = [
    ((667, 79), (633, 214)),
    ((486, 79), (533, 214)),
    ((486, 164), (533, 261)),
    ((289, 164), (424, 261)),
    ((289, 108), (424, 230)),
    ((176, 108), (362, 230)),
    ((667, 458), (633, 422)),
]

# Tower outlines, PDF points (y down), read off the vector drawings.
# Mission Street Tower, Figure 2: the corner columns, Mission Street line to the fourth column line,
# Ecker Place line to the column row south of the realigned Jessie Street.
MISSION_TOWER_FIG2 = [(191.0, 113.4), (309.6, 113.4), (309.6, 271.8), (191.0, 271.8)]
# First Street Tower, Figure 3: the office slab (to the facade fins and the First and Stevenson
# property lines) and its two cores.
FIRST_TOWER_FIG3 = [(113, 108), (286, 108), (286, 187), (497, 187), (497, 98), (667, 98), (667, 458), (113, 458)]

TOWERS = [
    {
        "label": "First Street Tower",
        "height_ft": 850,
        "use": "Office, with homes on floors 43 to 60",
        "note": ("Roof at about 850 ft (60 stories); mechanical and architectural features reach 910 ft "
                 "(Motion 19635). About 1.06 million gross sq ft of office and 109 homes (CPE checklist, Table 2). "
                 "Drawn at the office floor's size; the residential floors above are smaller."),
        "source": (f"illustrative: footprint traced from the {CPE['title']}, Figure 3 (typical office floor, PDF "
                   f"p. 7), registered through Figure 2 (p. 6); roof height from {MOTION}"),
    },
    {
        "label": "Mission Street Tower",
        "height_ft": 605,
        "use": "Hotel (169 rooms) on floors 3 to 21, 156 homes above",
        "note": ("Roof at about 605 ft (54 stories); screening to 625 ft and elevator equipment to 636 ft "
                 "(Motion 19635). Lower floors 133 ft long, 164 ft 11 in on the diagonal."),
        "source": (f"illustrative: footprint traced from the {CPE['title']}, Figure 2 (level 1 floor plan, "
                   f"corner columns, PDF p. 6); roof height from {MOTION}"),
    },
]


def red_segments(page) -> list[tuple[float, float, float, float]]:
    """The red (property line) strokes on a pdfplumber page, as (x0, top, x1, bottom)."""
    out = []
    for o in page.lines + page.rects + page.curves:
        c = o.get("stroking_color")
        if isinstance(c, (list, tuple)) and len(c) == 3 and c[0] > 0.8 and c[1] < 0.3 and c[2] < 0.3:
            out.append((o["x0"], o["top"], o["x1"], o["bottom"]))
    return out


def check_on_red(points, segs, page_no: int, tol: float = 2.0) -> None:
    """Every control point must sit on a red stroke of its figure (guards against a changed PDF)."""
    lines = shapely.MultiLineString([[(a, b), (c, d)] if (a, b) != (c, d) else [(a, b), (a + 0.01, b)]
                                     for a, b, c, d in segs])
    for p in points:
        d = lines.distance(shapely.Point(p))
        if d > tol:
            raise SystemExit(f"page {page_no}: control point {p} is {d:.1f} pt from the red property line")


def site_vertices() -> np.ndarray:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    utm = ob._utm_shapes(fc)
    return shapely.get_coordinates(shapely.union_all(utm.to_numpy()).boundary)


def fit_fig2(vertices: np.ndarray) -> trace.Similarity:
    src, dst, labels = [], [], []
    for label, fig, near in FIG2_CONTROLS:
        d = np.linalg.norm(vertices - near, axis=1)
        if d.min() > 3:
            raise SystemExit(f"no parcel vertex within 3 m of the control '{label}'")
        src.append(fig)
        dst.append(vertices[d.argmin()])
        labels.append(label)
    return trace.fit_similarity(np.array(src, float), np.array(dst, float), labels)


def fit_fig3_to_fig2() -> tuple[np.ndarray, float]:
    """Similarity Figure 3 -> Figure 2 in page points (both y down), and its RMS in points."""
    a = np.array([p for p, _ in FIG3_TO_FIG2], float)
    b = np.array([q for _, q in FIG3_TO_FIG2], float)
    ma, mb = a.mean(0), b.mean(0)
    A, B = a - ma, b - mb
    U, S, Vt = np.linalg.svd(B.T @ A / len(a))
    D = np.eye(2)
    if np.linalg.det(U @ Vt) < 0:
        D[1, 1] = -1
    R = U @ D @ Vt
    s = float(np.trace(np.diag(S) @ D) / ((A**2).sum() / len(a)))
    M = np.eye(3)
    M[:2, :2] = s * R
    M[:2, 2] = mb - s * R @ ma
    res = np.linalg.norm((a @ M[:2, :2].T + M[:2, 2]) - b, axis=1)
    return M, float(np.sqrt((res**2).mean()))


def main() -> None:
    pdf = trace.fetch_document(CPE["url"], config.ROOT / "data" / "raw" / "docs" / CPE["file"], CPE["sha256"])
    with pdfplumber.open(pdf) as doc:
        check_on_red([fig for _, fig, _ in FIG2_CONTROLS], red_segments(doc.pages[FIG2_PAGE - 1]), FIG2_PAGE)
        check_on_red([p for p, _ in FIG3_TO_FIG2], red_segments(doc.pages[FIG3_PAGE - 1]), FIG3_PAGE)

    vertices = site_vertices()
    sim = fit_fig2(vertices)
    M, rms3 = fit_fig3_to_fig2()
    print(f"[oceanwide] Figure 2 -> parcels: RMS {sim.rms_m:.2f} m over {len(FIG2_CONTROLS)} corners, "
          f"scale {sim.scale / 0.3048:.4f} ft/pt; Figure 3 -> Figure 2: RMS {rms3:.2f} pt, "
          f"scale {np.sqrt(abs(np.linalg.det(M[:2, :2]))):.3f}")

    first_fig2 = np.array(FIRST_TOWER_FIG3, float) @ M[:2, :2].T + M[:2, 2]
    outlines = [Polygon(sim.apply(first_fig2)), Polygon(sim.apply(MISSION_TOWER_FIG2))]

    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM).union_all()
    features = []
    for tower, poly in zip(TOWERS, outlines):
        poly = shapely.make_valid(poly).buffer(0)
        off = poly.difference(site.buffer(1.0)).area
        print(f"[oceanwide] {tower['label']}: {poly.area * SQFT:,.0f} sq ft footprint, "
              f"{off * SQFT:,.0f} sq ft outside the parcels")
        wgs = gpd.GeoSeries([poly.simplify(0.3)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": tower["label"], "stage": "paused",
                "height_ft": tower["height_ft"], "podium_ft": None, "base_ft": 0,
                "use": tower["use"], "phase": None, "illustrative": True,
                "source": tower["source"], "note": tower["note"],
            },
            "geometry": mapping(wgs),
        })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the two approved towers as single volumes, their footprints traced "
                        "from the 2016 CPE checklist's floor plans and extruded to the roof heights in Planning "
                        "Motion 19635 (about 850 ft and 605 ft; parapet and equipment reach 910 and 636 ft). "
                        "Setbacks, the First Street Tower's open ground-floor “urban room” and the two "
                        "historic First Street buildings the project keeps are not drawn. Neither tower rose "
                        "above its foundations."),
            "note": "The approved towers as simple volumes at their roof heights, not the final designs.",
            "sourceUrl": CPE["url"],
            "sourceLabel": "CPE checklist floor plans, 2016 (PDF)",
            "heightSourceUrl": MOTION_URL,
            "georeference": {
                "figure_2": sim.report(),
                "figure_3_to_figure_2": {"rms_pt": round(rms3, 2), "controls": len(FIG3_TO_FIG2)},
                "method": "Figure 2's red property-line corners matched to DataSF parcel vertices (similarity).",
            },
            "license": ("Tower footprints: traced from a public SF Planning document. Georeference: DataSF "
                        "parcels (ODC-PDDL)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[oceanwide] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
