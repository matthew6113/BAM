"""Balboa Reservoir: block height limits traced from the adopted design standards.

Source:
- The Balboa Reservoir Neighborhood Design Standards and Guidelines (DSG), adopted by the
  Planning Commission on May 28, 2020 (Resolution 20734), REV-1 September 15, 2020:
  - Figure 7.2-1, Building Height Diagram (p. 182; PDF page 194). Vector fills: 25, 35, 48,
    68 and 78 ft. S.7.2.1: heights "shall not exceed the maximums indicated on Figure 7.2-1".
  - Figure 3.1-1, Land Use Plan (p. 34; PDF page 46), for the open spaces: Reservoir Park
    (Block J) and the SFPUC Retained Fee Open Space (the pipeline strip, "Not governed by
    DSG/SUD").
- The 2020 public draft in the GPA initiation packet (2018-007883GPA.pdf, Feb 24, 2020) is
  superseded: its height diagram differs (e.g. Block G had a 78-ft zone, the townhouse
  step-downs were 20 ft deep). It is not used.
- Under construction (DBI permits on block 3180, lot 190, 11 Frida Kahlo Way):
  202207289451 (Building E, 7 stories, 128 homes and a community facility; first
  construction document 2025-11-25) and 202503313370 (Building A, 6 stories, 159 homes;
  first construction document 2026-06-11). The MOHCD loan evaluation of May 2, 2025 places
  Building A at "the southeast corner of the Balboa Reservoir site" (Block A). No footprints
  for either exist in the base data (Overture 2026-09-23.1 has no buildings on the site), so
  Blocks A and E stay height-limit envelopes, marked stage "construction".

What this is and isn't:
- Each zone is drawn to its height limit, not as a building design: real buildings will be
  smaller and set back (e.g. Building A steps down to 5 stories on its south side), so the
  massing is labelled illustrative.
- The figure's "Flexible height at townhouses" note of the public draft is gone in the
  adopted figure; the townhouse blocks (TH1, TH2, H) are 25 ft within 30 ft of the western
  property line (S.7.2.3), 35 ft in the middle and 48 ft on their eastern 50 ft. The 20-ft
  48-ft strips on Blocks B, D, F and G are the West Street step-down (S.7.2.2).

Georeferencing:
- Each figure's dash-dot Special Use District outline (top, west and east edges and the
  north edge of the SFPUC strip) gives four corners, matched to the corners of the official
  SUD polygon (DataSF 5yf5-ms5f, data/boundaries/balboa-reservoir.geojson) with a
  least-squares similarity fit. Residuals and the outline's largest deviation are recorded.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_balboa_reservoir
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
import shapely.ops
from shapely.geometry import LineString, Point, Polygon, mapping

from .. import config, trace

PROJECT_ID = "balboa-reservoir"
UTM = "EPSG:26910"

DSG = {
    "title": "Balboa Reservoir Neighborhood Design Standards and Guidelines (adopted May 28, 2020, "
             "Planning Commission Resolution 20734; REV-1 Sept 15, 2020)",
    "url": "https://sfplanning.org/sites/default/files/documents/citywide/balboareservoir_dsg.pdf",
    "sha256": "ad41f23d01f7ae9e6d8ee9570218cb97d6cb161e858ca4e61b6a743d1e3f19ba",
}
FIG_7_2_1 = {"page_index": 193, "printed_page": "182", "figure": "Figure 7.2-1, Building Height Diagram"}
FIG_3_1_1 = {"page_index": 45, "printed_page": "34", "figure": "Figure 3.1-1, Land Use Plan"}
MAP_FRAME = (400, 40, 660, 500)  # the figure's map (PDF points: x0, top, x1, bottom); legend and text outside

# Legend swatches of Figure 7.2-1 (RGB as stored in the PDF) -> height limit in feet.
HEIGHT_FILLS = {25: (0.627, 0.761, 0.729), 35: (0.961, 0.922, 0.867), 48: (0.608, 0.663, 0.733),
                68: (0.953, 0.78, 0.4), 78: (0.89, 0.388, 0.298)}
# The narrow step-down strips (25 and 48 ft) are drawn over the block fills; they win overlaps.
ON_TOP = (25, 48)
# Figure 3.1-1 open-space fill and the two spaces drawn here (a point inside each, PDF points).
OPEN_FILL = (0.627, 0.761, 0.729)
OPEN_SPACES = {
    "J": {"label": "Reservoir Park", "inside": (570.0, 240.0),
          "note": "Publicly accessible open space (the approximately 2-acre Reservoir Park); no buildings."},
    "SFPUC": {"label": "SFPUC open space", "inside": (520.0, 460.0),
              "note": "SFPUC Retained Fee Open Space over the pipelines, outside the Special Use District "
                      "(\"Not governed by DSG/SUD\"); no buildings."},
}

# The dash-dot SUD outline in each figure (PDF points), as straight edges.
OUTLINES = {
    193: {"top": ((425.7, 57.8), (648.6, 58.9)), "west": ((415.8, 435.7), (417.6, 61.6)),
          "east": ((652.4, 67.0), (652.4, 490.2)), "south": ((423.7, 416.2), (648.7, 477.8))},
    45: {"top": ((426.3, 51.5), (649.2, 52.5)), "west": ((416.4, 429.3), (418.2, 55.2)),
         "east": ((653.0, 60.7), (653.0, 483.8)), "south": ((424.3, 409.8), (649.4, 471.4))},
}
CORNERS = {"NW": ("top", "west"), "NE": ("top", "east"), "SE": ("south", "east"), "SW": ("south", "west")}

# Block labels in Figure 7.2-1, and the dashed TH1/H line (both blocks share one fill).
BLOCK_LABELS = ["TH2", "G", "F", "E", "TH1", "D", "C", "B", "H", "A"]
TH1_H_LINE = ((417.4, 366.2), (457.7, 377.2))

# DBI permits for the two blocks under construction.
UNDER_CONSTRUCTION = {
    "E": "Under construction: Building E, 7 stories, 128 affordable homes and a community facility "
         "(DBI permit 202207289451, first construction document Nov 25, 2025). Drawn to the block's height limit.",
    "A": "Under construction: Building A, 6 stories (5 on its south side), 159 affordable homes "
         "(DBI permit 202503313370, first construction document June 11, 2026). Drawn to the block's height limit.",
}
USE = {"TH1": "townhouses", "TH2": "townhouses", "H": "townhouses"}


def _line_cross(a, b) -> tuple[float, float]:
    (x1, y1), (x2, y2) = a
    (x3, y3), (x4, y4) = b
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
    return px, py


def _sud_corners(site_utm: Polygon) -> dict[str, tuple[float, float]]:
    """The four corners of the SUD polygon: the vertices nearest each corner of its bounding box."""
    pts = np.asarray(site_utm.exterior.coords)[:-1]
    x0, y0, x1, y1 = site_utm.bounds
    targets = {"NW": (x0, y1), "NE": (x1, y1), "SE": (x1, y0), "SW": (x0, y0)}
    return {k: tuple(pts[np.argmin(np.linalg.norm(pts - t, axis=1))]) for k, t in targets.items()}


def georeference(page_index: int, site_utm: Polygon) -> trace.Similarity:
    edges = OUTLINES[page_index]
    sud = _sud_corners(site_utm)
    src, dst, labels = [], [], []
    for name, (a, b) in CORNERS.items():
        src.append(_line_cross(edges[a], edges[b]))
        dst.append(sud[name])
        labels.append(f"SUD {name} corner")
    sim = trace.fit_similarity(src, dst, labels)
    # How far the figure's outline strays from the official outline along its whole length.
    fig_outline = Polygon([src[0], src[1], src[2], src[3]])
    sim.outline_dev_m = float(sim.geometry(fig_outline).hausdorff_distance(site_utm))  # type: ignore[attr-defined]
    return sim


def _fills(page, colour, tol=0.012) -> list[Polygon]:
    out = []
    x0, t0, x1, b0 = MAP_FRAME
    for obj in page.curves + page.rects:
        col = obj.get("non_stroking_color")
        if not obj.get("fill") or not isinstance(col, (tuple, list)) or len(col) != 3:
            continue
        if max(abs(a - b) for a, b in zip(col, colour)) > tol:
            continue
        if not (obj["x0"] >= x0 and obj["x1"] <= x1 and obj["top"] >= t0 and obj["bottom"] <= b0):
            continue
        pts = obj.get("pts") or [(obj["x0"], obj["top"]), (obj["x1"], obj["top"]),
                                 (obj["x1"], obj["bottom"]), (obj["x0"], obj["bottom"])]
        poly = shapely.make_valid(Polygon(pts))
        if not poly.is_empty and poly.area > 1:
            out.append(poly)
    return out


def trace_height_zones(page) -> list[dict]:
    """Height zones per block from Figure 7.2-1, in PDF points."""
    by_height = {h: shapely.union_all(_fills(page, c)) for h, c in HEIGHT_FILLS.items()}
    for h, g in by_height.items():
        if g.is_empty:
            raise SystemExit(f"no {h}-ft fills found in Figure 7.2-1")
    top = shapely.union_all([by_height[h] for h in ON_TOP])
    for h in by_height:
        if h not in ON_TOP:
            by_height[h] = by_height[h].difference(top)
    # Blocks: connected pieces of all fills, named by the label inside; TH1 and H share a fill.
    allfill = shapely.union_all(list(by_height.values())).buffer(0.3, join_style="mitre").buffer(-0.3, join_style="mitre")
    words = {w["text"]: Point((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2)
             for w in page.extract_words() if w["text"] in BLOCK_LABELS and w["x0"] > MAP_FRAME[0]}
    missing = set(BLOCK_LABELS) - set(words)
    if missing:
        raise SystemExit(f"block labels not found in Figure 7.2-1: {sorted(missing)}")
    (ax, ay), (bx, by) = TH1_H_LINE
    k = 200 / np.hypot(bx - ax, by - ay)
    cut = LineString([(ax - (bx - ax) * k, ay - (by - ay) * k), (bx + (bx - ax) * k, by + (by - ay) * k)])
    pieces = []
    for part in trace.as_multipolygon(allfill).geoms:
        if part.contains(words["TH1"]):
            pieces.extend(shapely.get_parts(shapely.ops.split(part, cut)))
        else:
            pieces.append(part)
    blocks = {}
    for piece in pieces:
        names = [n for n, p in words.items() if piece.contains(p)]
        if len(names) != 1:
            if piece.area > 20:
                raise SystemExit(f"block piece of {piece.area:.0f} pt² holds labels {names}")
            continue
        blocks[names[0]] = piece
    zones = []
    for block, footprint in blocks.items():
        for h, g in by_height.items():
            z = shapely.make_valid(footprint.intersection(g))
            z = shapely.union_all([p for p in shapely.get_parts(z) if isinstance(p, Polygon) and p.area >= 2])
            if not z.is_empty:
                zones.append({"block": block, "height_ft": h, "pt": z})
    return zones


def trace_open_spaces(page) -> dict[str, Polygon]:
    fills = _fills(page, OPEN_FILL)
    out = {}
    for key, spec in OPEN_SPACES.items():
        hit = [p for p in fills if p.contains(Point(spec["inside"]))]
        if len(hit) != 1:
            raise SystemExit(f"Figure 3.1-1: expected one open-space fill at {key}, found {len(hit)}")
        out[key] = hit[0]
    return out


def _streets() -> gpd.GeoDataFrame:
    from .traced_boundaries import streets
    return streets("balboa_reservoir", (-122.4600, 37.7215, -122.4500, 37.7300))


def main(plot: str | None = None) -> None:
    pdf_path = trace.fetch_document(DSG["url"], config.ROOT / "data" / "raw" / "docs" / "balboareservoir_dsg.pdf",
                                    DSG["sha256"])
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = trace.largest_polygon(site.geometry.iloc[0])

    with pdfplumber.open(pdf_path) as pdf:
        p_h = pdf.pages[FIG_7_2_1["page_index"]]
        p_l = pdf.pages[FIG_3_1_1["page_index"]]
        fig721 = georeference(FIG_7_2_1["page_index"], site_utm)
        fig311 = georeference(FIG_3_1_1["page_index"], site_utm)
        zones = trace_height_zones(p_h)
        opens = trace_open_spaces(p_l)
    for name, sim in (("Figure 7.2-1", fig721), ("Figure 3.1-1", fig311)):
        print(f"[balboa] {name} georeference: RMS {sim.rms_m:.2f} m over 4 SUD corners, "
              f"scale {sim.scale:.4f} m/pt, outline deviation {sim.outline_dev_m:.2f} m")

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    order = {b: i for i, b in enumerate(["A", "B", "C", "D", "E", "F", "G", "H", "TH1", "TH2"])}
    doc = f"{DSG['title']}, {FIG_7_2_1['figure']}, p. {FIG_7_2_1['printed_page']}"
    features = []
    for z in sorted(zones, key=lambda z: (order[z["block"]], z["height_ft"])):
        geom = trace.as_multipolygon(shapely.make_valid(fig721.geometry(z["pt"]).simplify(0.3)))
        if geom.area < 20:
            continue
        b = z["block"]
        h = z["height_ft"]
        extra = ""
        if h == 25:
            extra = "; 25-ft step-down within 30 ft of the western property line (S.7.2.3)"
        elif h == 48 and b in ("B", "D", "F", "G"):
            extra = "; 48-ft West Street step-down, 20 ft deep (S.7.2.2)"
        props = {
            "kind": "block",
            "block": b,
            "label": f"Block {b}",
            "stage": "construction" if b in UNDER_CONSTRUCTION else "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": USE.get(b, "multifamily residential"),
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the {h}-ft height limit traced from {doc}{extra}",
        }
        if b in UNDER_CONSTRUCTION:
            props["note"] = UNDER_CONSTRUCTION[b]
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})

    land = f"{DSG['title']}, {FIG_3_1_1['figure']}, p. {FIG_3_1_1['printed_page']}"
    for key, poly in opens.items():
        spec = OPEN_SPACES[key]
        geom = trace.as_multipolygon(shapely.make_valid(fig311.geometry(poly).simplify(0.3)))
        props = {
            "kind": "block",
            "block": key,
            "label": spec["label"],
            "stage": "entitled",
            "height_ft": None,
            "podium_ft": None,
            "base_ft": 0,
            "use": "open space",
            "phase": None,
            "illustrative": False,
            "source": f"traced: {land} (outline only, approximate)",
            "note": spec["note"],
        }
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each block is drawn to its height limits (25 to 78 ft) in the Design "
                "Standards and Guidelines adopted in 2020 (Fig. 7.2-1), not as a building design. Blocks A and E "
                "are under construction (DBI permits) but no real footprints exist yet, so they are drawn as "
                "envelopes too. Reservoir Park and the SFPUC open space are outlined, without height."
            ),
            "note": "Blocks are drawn to their height limits in the 2020 design standards, not as building designs; "
                    "real buildings will be smaller.",
            "sourceUrl": DSG["url"],
            "sourceLabel": "Design standards, 2020 (PDF)",
            "georeference": {
                "method": "Corners of each figure's dash-dot Special Use District outline matched to the official SUD "
                          "polygon (DataSF 5yf5-ms5f) with a least-squares similarity fit",
                "figure_7_2_1": {**fig721.report(), "outline_max_deviation_m": round(fig721.outline_dev_m, 2)},
                "figure_3_1_1": {**fig311.report(), "outline_max_deviation_m": round(fig311.outline_dev_m, 2)},
            },
            "license": "Block shapes: traced from a public SF Planning document; registered to the DataSF "
                       "Special Use Districts layer (public domain).",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(fc), indent=1) + "\n")
    print(f"[balboa] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB): "
          + ", ".join(f"{f['properties']['block']}:{f['properties']['height_ft']}" for f in features))

    if plot:
        _plot(fc, site_utm, plot)


def _plot(fc, site_utm, out) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colours = {25: "#9fc2ba", 35: "#f5ebdd", 48: "#9ba9bb", 68: "#f3c766", 78: "#e3634c", None: "#cfe8cf"}
    st = _streets()
    g = gpd.GeoDataFrame.from_features(fc["features"], crs=4326).to_crs(UTM)
    fig, ax = plt.subplots(figsize=(9, 11))
    x0, y0, x1, y1 = site_utm.buffer(120).bounds
    st.cx[x0:x1, y0:y1].plot(ax=ax, color="#888", linewidth=0.8)
    for _, r in g.iterrows():
        h = None if r["height_ft"] != r["height_ft"] else r["height_ft"]
        gpd.GeoSeries([r.geometry]).plot(ax=ax, color=colours[h], edgecolor="k", linewidth=0.4, alpha=0.9)
        c = r.geometry.representative_point()
        ax.annotate(f"{r['block']}\n{'' if h is None else int(h)}", (c.x, c.y), fontsize=6, ha="center")
    gpd.GeoSeries([site_utm.exterior]).plot(ax=ax, color="blue", linewidth=1)
    for _, s in st.cx[x0:x1, y0:y1].iterrows():
        if s["name"] and s.geometry.length > 60:
            m = s.geometry.interpolate(0.5, normalized=True)
            ax.annotate(s["name"], (m.x, m.y), fontsize=5, color="#555")
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    fig.savefig(out, dpi=130)


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else None)
