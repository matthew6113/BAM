"""Pier 70: parcel height limits traced from the adopted Design for Development, plus Building 12.

Sources:
- Parcel footprints and height limits: Pier 70 SUD Design for Development (D4D), April 26, 2022
  edition (the Port's "220531_P70_D4D_web.pdf"; it carries the Planning Commission's 2020
  amendment, Motion 20648, nine residential stories, and 2022 amendment, Motion 21086, retail and
  office definitions, neither of which changed a height limit), Figure 6.4.2 "Building Height
  Maximum", printed p. 155 (PDF page 171). Standard S6.4.1 makes the figure binding: "Building
  height per parcel shall not exceed ... the heights shown in Figure 6.4.2."
- Building 12 height (60 ft): D4D Table 6.15.2 "Height Reference Locations", printed p. 184
  ("C2 ... Building 12 / 60' height").
- Building 12 status: Port Commission staff report, Aug 11, 2026, item 11A, p. 3 ("In January 2022,
  Developer completed the rehabilitation of historic Building 12"); the same report has Phase 1
  parcels (pp. 3-5).

What this is and isn't:
- Each parcel is drawn to its height limit, not as a building design, so the massing is
  labelled illustrative. Figure 6.4.2 has four limits: 90 ft (A, B, C1, C2, D, the west leg of E1,
  F/G, H1/H2), 70 ft (E2, E3), 65 ft (PKN, PKS, HDY3, HDY1/2, the north leg of E1) and 50 ft (E4).
  Zoning (90-X/65-X/40-X) is coarser; the D4D is the parcel-level control.
- The Aug 2026 term sheet that would raise some parcels to 90 ft is not approved and isn't drawn.
- Buildings 2 and 21 are retained historic buildings that haven't been rehabilitated (the Aug 2026
  report calls Building 12 the only vertical project done), so they stay in the base map only.
- Building 12 is the one built project building: OpenStreetMap footprint, D4D height.

Georeferencing: the figure is vector. Its fills are read from the PDF; the figure is also
rendered at 200 dpi, where street centrelines are the midpoints between curb lines measured on
straight stretches beside six intersections of streets now in OpenStreetMap (Illinois, and the
Phase 1 streets Louisiana and Maryland, accepted by the City and Port in 2024). The similarity
fit and its residuals are recorded in the output.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_pier_70
"""

from __future__ import annotations

import json
import os

import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
import shapely.affinity
from shapely.geometry import Point, Polygon, mapping, shape

from .. import config, trace
from .traced_boundaries import intersection, streets

PROJECT_ID = "pier-70"
UTM = "EPSG:26910"
DOCS = config.ROOT / "data" / "raw" / "docs"

D4D = {
    "title": "Pier 70 SUD Design for Development (Port of San Francisco, April 26, 2022 edition)",
    "url": "https://www.sfport.com/media/8123/download?inline=",
    "file": "220531_P70_D4D_web.pdf",
    "sha256": "5bcb3a9b89beff6e9dca98fffbb094984dbac63d6865d9227fbc701c6c127333",
}
FIG = {"page_index": 170, "printed_page": "155", "figure": "Figure 6.4.2, Building Height Maximum"}
B12_HEIGHT = {"height_ft": 60, "where": "Table 6.15.2, Height Reference Locations, p. 184 (\"Building 12 / 60' height\")"}
PORT_2026 = {
    "title": "Port Commission staff report, Aug 11, 2026, item 11A (Pier 70 project update)",
    "url": "https://www.sfport.com/sites/default/files/2026-08/item_11a_p70_project_update_-_term_sheet_overview_-_information.pdf",
}
DPI = 200
PT_TO_PX = DPI / 72

# Street centrelines in the 200-dpi render (pixels): midpoints between the curb lines (or, on
# Maryland's curbless shared stretch, between the matching edges) measured beside each intersection.
CONTROLS = {
    ("Illinois Street", "20th Street"): (353.0, 352.0),
    ("Illinois Street", "22nd Street"): (354.0, 1185.0),
    ("Louisiana Street", "22nd Street"): (1023.0, 1169.0),
    ("Maryland Street", "22nd Street"): (1327.0, 1169.0),
    ("Maryland Street", "21st Street"): (1327.5, 655.5),
    ("Maryland Street", "20th Street"): (1327.5, 378.5),
}
# Legend swatches in the 200-dpi render (pixel centre) -> height limit in feet.
LEGEND = {90: (1453, 1458), 70: (1453, 1494), 65: (1453, 1529), 50: (1453, 1565)}
# Parcel fills of the four height colours (CMYK as stored in the PDF). Which height each one is
# comes from matching its rendered colour to the legend swatches, not from this list.
PARCEL_CMYK = [(0.475, 0.087, 0.09, 0.0), (0.481, 0.244, 0.046, 0.25), (0.359, 0.449, 0.16, 0.0), (0.667, 0.858, 0.278, 0.12)]
HISTORIC_GREY = (0.451, 0.361, 0.348, 0.013)  # "Historic Buildings" fill (CMYK as stored)
LEGEND_TOP_PT = 515  # legend swatches sit below this (PDF points from the top)

# Phase 1 parcels named in the Aug 2026 Port report (pp. 3-5): Parcel C2A (affordable), Parcel E2,
# Parcels A, C2B and D; Parcel K South is in Phase 2.
PHASE = {"A": "Phase 1", "D": "Phase 1", "E2": "Phase 1", "C2": "Phase 1", "PKS": "Phase 2"}
USE_NOTE = {
    "E1": "The D4D limits the north leg of E1 to 65 ft and the rest to 90 ft (S6.4.2).",
    "E4": "Arts building parcel; no more than five stories (S6.4.2).",
    "C2": "Includes affordable housing Parcel C2A (Phase 1).",
}

BUILDING_12 = {"osm": "w257341252", "label": "Building 12"}


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    rgb = np.asarray(page.render(scale=PT_TO_PX).to_pil().convert("RGB"))
    if rgb.shape[:2] != (1700, 2200):
        raise SystemExit(f"unexpected Figure 6.4.2 render size {rgb.shape}")
    return rgb


def georeference(st) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), xy in CONTROLS.items():
        src.append(xy)
        dst.append(intersection(st, a, b))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def _fills(pdf_path):
    """Every filled vector shape on the figure page, in render pixels, with its colour and labels."""
    with pdfplumber.open(pdf_path, pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()
        out = []
        for o in page.curves + page.rects:
            if not o.get("fill") or o["top"] > LEGEND_TOP_PT:
                continue
            pts = o.get("pts") or [(o["x0"], o["top"]), (o["x1"], o["top"]), (o["x1"], o["bottom"]), (o["x0"], o["bottom"])]
            if len(pts) < 3:
                continue
            poly = shapely.make_valid(Polygon([(float(x), float(y)) for x, y in pts]))
            if poly.is_empty or poly.area < 100:  # pt^2; drops hatching, dashes and swatch slivers
                continue
            inside = [w["text"] for w in words
                      if poly.contains(Point((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2))]
            out.append({"cmyk": tuple(o.get("non_stroking_color") or ()), "labels": inside,
                        "px": shapely.affinity.scale(poly, PT_TO_PX, PT_TO_PX, origin=(0, 0))})
    return out


def height_parcels(fills, rgb) -> list[dict]:
    """Parcels coloured with a height-legend colour, each matched to the nearest swatch in the render."""
    palette = {h: np.median(rgb[y - 6:y + 7, x - 15:x + 16].reshape(-1, 3), axis=0) for h, (x, y) in LEGEND.items()}
    parcels = []
    for f in fills:
        if not any(len(f["cmyk"]) == 4 and max(abs(a - b) for a, b in zip(f["cmyk"], c)) < 0.005 for c in PARCEL_CMYK):
            continue
        inner = f["px"].buffer(-6).intersection(shapely.box(0, 0, rgb.shape[1] - 1, rgb.shape[0] - 1))
        if inner.is_empty:
            continue
        # Sample the fill away from its edges and labels: the commonest colour inside it.
        x0, y0, x1, y1 = (int(v) for v in inner.bounds)
        ys, xs = np.mgrid[y0:y1:3, x0:x1:3]
        keep = shapely.contains_xy(inner, xs.ravel(), ys.ravel())
        px = rgb[ys.ravel()[keep], xs.ravel()[keep]].astype(float)
        if not len(px):
            continue
        vals, counts = np.unique(px, axis=0, return_counts=True)
        colour = vals[counts.argmax()]
        h, d = min(((h, float(np.linalg.norm(colour - c))) for h, c in palette.items()), key=lambda t: t[1])
        if d > 12:
            continue
        parcels.append({"height_ft": h, "labels": f["labels"], "px": f["px"], "colour_dist": round(d, 1)})
    return parcels


def _name(p) -> str:
    labs = [t for t in p["labels"] if t not in ("’",)]
    if labs == ["H1", "H2"]:
        return "H1/H2"
    if labs:
        return labs[0]
    if p["height_ft"] == 65:
        return "E1"  # the north leg of E1 has no label of its own in the figure
    raise SystemExit(f"unlabelled parcel {p}")


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "named_buildings_pier70.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = -122.3905, 37.7570, -122.3810, 37.7640
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    return g


def to_wgs(g):
    return gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]


def main() -> None:
    pdf_path = trace.fetch_document(D4D["url"], DOCS / D4D["file"], D4D["sha256"])
    st = streets("pier70", (-122.392, 37.755, -122.378, 37.766))
    st = st[st["subtype"] == "road"]
    sim = georeference(st)
    print(f"[pier-70] Figure 6.4.2 georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f} deg")
    for label, r in zip(sim.labels, sim.residuals_m):
        print(f"    {label}: {r:.2f} m")

    rgb = _render(pdf_path)
    fills = _fills(pdf_path)
    parcels = height_parcels(fills, rgb)
    # Some shapes are drawn twice (fill and outline passes): merge by parcel and height.
    merged: dict[tuple[str, int], list] = {}
    for p in parcels:
        merged.setdefault((_name(p), p["height_ft"]), []).append(p)
    parcels = []
    for (block, h), ps in merged.items():
        px = shapely.union_all([p["px"] for p in ps]).buffer(0.5, join_style="mitre").buffer(-0.5, join_style="mitre")
        parcels.append({"block": block, "height_ft": h, "colour_dist": max(p["colour_dist"] for p in ps),
                        "utm": shapely.make_valid(sim.geometry(px).simplify(0.3))})
    print("[pier-70] parcels: " + ", ".join(f"{p['block']}:{p['height_ft']} (d{p['colour_dist']})"
                                           for p in sorted(parcels, key=lambda p: p["block"])))

    # Historic Building 12 in the figure, to check the OpenStreetMap footprint against it.
    b12_fig = [f for f in fills if f["labels"] == ["12"]
               and max(abs(a - b) for a, b in zip(f["cmyk"], HISTORIC_GREY)) < 0.01]
    if len(b12_fig) != 1:
        raise SystemExit(f"expected one Building 12 shape in the figure, found {len(b12_fig)}")
    b12_fig_utm = sim.geometry(b12_fig[0]["px"])

    bld = _buildings()
    b12 = bld[bld["osm"].fillna("").str.startswith(BUILDING_12["osm"] + "@")]
    if len(b12) != 1:
        raise SystemExit(f"expected one Building 12 footprint, found {len(b12)}")
    b12_utm = gpd.GeoSeries(b12.geometry, crs=4326).to_crs(UTM).iloc[0]
    iou = b12_utm.intersection(b12_fig_utm).area / b12_utm.union(b12_fig_utm).area
    shift = b12_utm.centroid.distance(b12_fig_utm.centroid)
    print(f"[pier-70] Building 12: OSM footprint vs figure IoU {iou:.2f}, centroid offset {shift:.1f} m, "
          f"OSM height {b12['height'].iloc[0]} m")
    if iou < 0.8:
        raise SystemExit("Building 12 footprint and figure disagree; check the georeference")

    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    src = f"{D4D['title']}, {FIG['figure']}, p. {FIG['printed_page']}"
    features = []
    order = ["A", "B", "C1", "C2", "D", "E1", "E2", "E3", "E4", "F/G", "H1/H2", "PKN", "PKS", "HDY3", "HDY1/2"]
    for p in sorted(parcels, key=lambda p: (order.index(p["block"]) if p["block"] in order else 99, -p["height_ft"])):
        geom = p["utm"]
        if geom.intersects(b12_utm):
            geom = geom.difference(b12_utm)
        if geom.is_empty or geom.area < 20:
            continue
        props = {
            "kind": "block",
            "block": p["block"],
            "label": f"Parcel {p['block']}",
            "stage": "entitled",
            "height_ft": p["height_ft"],
            "podium_ft": None,
            "base_ft": 0,
            "use": None,
            "phase": PHASE.get(p["block"]),
            "illustrative": True,
            "source": f"illustrative: drawn to the {p['height_ft']}-ft height limit traced from {src}"
                      + (f"; phase: {PORT_2026['title']}, pp. 3-5" if p["block"] in PHASE else ""),
        }
        if p["block"] in USE_NOTE:
            props["note"] = USE_NOTE[p["block"]]
        features.append({"type": "Feature", "properties": props,
                         "geometry": mapping(to_wgs(trace.as_multipolygon(geom)))})

    features.append({
        "type": "Feature",
        "properties": {
            "kind": "landmark", "label": BUILDING_12["label"], "name": "Pier 70's Building 12",
            "stage": "complete", "height_ft": B12_HEIGHT["height_ft"], "podium_ft": None, "base_ft": 0,
            "use": "Market hall, maker studios and offices", "phase": "Phase 1", "illustrative": False,
            "source": f"height: {D4D['title']}, {B12_HEIGHT['where']}; rehabilitation completed Jan 2022: "
                      f"{PORT_2026['title']}, p. 3; footprint: OpenStreetMap {BUILDING_12['osm']} via Overture "
                      f"{config.OVERTURE_RELEASE} (matches the figure's Building 12, IoU {iou:.2f})",
            "note": "Historic mold loft, rehabilitated and reopened in 2022. OpenStreetMap names this footprint "
                    f"\"Pier 70\" and maps it at {b12['height'].iloc[0]:.0f} m; the height drawn is the D4D's 60 ft.",
            "osm": BUILDING_12["osm"],
        },
        "geometry": mapping(b12.geometry.iloc[0]),
    })

    near_site = to_wgs(site_utm.buffer(30))
    outside = [f["properties"]["label"] for f in features
               if not shape(f["geometry"]).representative_point().within(near_site)]
    if outside:
        print(f"[pier-70] warning: off the site: {outside}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each development parcel is drawn to its height limit in the Design for "
                "Development (Fig. 6.4.2: 90, 70, 65 or 50 ft), not as a building design. Building 12, "
                "rehabilitated in 2022, is drawn as built. Historic Buildings 2 and 21 await rehabilitation and "
                "stay in the base map. The 2026 proposal to raise some parcels to 90 ft isn't approved and "
                "isn't drawn."
            ),
            "note": ("Parcels are drawn to their height limits in the Design for Development, not as building "
                     "designs; real buildings will be smaller."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2022 (PDF)",
            "georeference": {"figure_6_4_2": sim.report(), "building_12_check": {"iou": round(iou, 3), "centroid_offset_m": round(shift, 2)}},
            "license": "Parcel shapes: traced from a public Port of San Francisco document. "
                       "Building 12 footprint: OpenStreetMap contributors (ODbL 1.0), via Overture Maps.",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(fc), indent=1) + "\n")
    print(f"[pier-70] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


if __name__ == "__main__":
    main()
