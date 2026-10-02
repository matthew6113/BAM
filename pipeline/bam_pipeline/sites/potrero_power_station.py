"""Potrero Power Station: site boundary and block massing traced from the Draft EIR.

Source: Potrero Power Station Mixed-Use Development Project Draft EIR, Volume 1
(SF Planning Case No. 2017-011878ENV, October 2018).

- Boundary and sub-areas: Figure 2-2 (p. 2-6), vector shapes in the PDF.
- Blocks and height limits (2018 proposal, not drawn): Figure 2-7, Proposed Height District Plan (p. 2-20), a raster.
- Stack height (300 ft): pp. 2-7 and 4.D-8.

What this is and isn't:
- The 2018 Draft EIR describes the project as first proposed. The plan approved in 2020
  (the "project variant" in the Responses to Comments, the Design for Development and
  Planning Code Figure 249.87-4) modified the land use plan and limits new buildings to
  65 to 240 ft (Planning Commission minutes, Jan 30, 2020).
  The 2018 blocks are superseded, so they are traced but not drawn (DRAW_DEIR_BLOCKS):
  the map shows official, current facts only. Draw the D4D's blocks once it can be read.
- The site is the same ~29-acre site (Planning Commission minutes, Jan 30, 2020).

Georeferencing:
- Figure 2-2: street-name labels in the PDF give street centrelines in figure
  coordinates. Their intersections are matched to the same intersections in
  OpenStreetMap (via Overture) with a least-squares similarity fit; residuals are
  recorded in the output.
- Figure 2-7 has no text layer, so its dash-dot site boundary is registered onto the
  Figure 2-2 boundary (trimmed ICP).

    uv run --directory pipeline python -m bam_pipeline.sites.potrero_power_station
"""

from __future__ import annotations

import io
import json
import os

import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import shapely
from pypdf import PdfReader
from shapely.geometry import LineString, Point, Polygon, box, mapping

from .. import config, trace

PROJECT_ID = "potrero-power-station"
UTM = "EPSG:26910"

DEIR = {
    "title": "Potrero Power Station Mixed-Use Development Project Draft EIR, Volume 1 (Case No. 2017-011878ENV, Oct 2018)",
    "url": "https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf",
    "sha256": "55daaa4f9d715ef07e67294f491b4ed22c1e6776605f529daf3b8df6c9ba2871",
}
FIG_2_2 = {"page_index": 97, "printed_page": "2-6", "figure": "Figure 2-2, Project Site Sub-Areas and Ownership"}
FIG_2_7 = {"page_index": 111, "printed_page": "2-20", "figure": "Figure 2-7, Proposed Height District Plan"}

# Figure 2-2 sub-area fills (CMYK as stored in the PDF) and the legend's names.
SUB_AREAS = {
    "Power Station sub-area": {"cmyk": (0.213, 0.021, 0.034, 0.0), "owner": "California Barrel Co. LLC"},
    "PG&E sub-area": {"cmyk": (0.053, 0.176, 0.279, 0.0), "owner": "PG&E"},
    "Port sub-area": {"cmyk": (0.302, 0.391, 0.052, 0.0), "owner": "SF Port"},
    "Southern sub-area": {"cmyk": (0.52, 0.024, 0.789, 0.0), "owner": "Harrigan Weidenmuller Co."},
    "City sub-area": {"cmyk": (0.029, 0.0, 0.49, 0.0), "owner": "City and County of San Francisco"},
}
LEGEND_TOP = 520  # Figure 2-2 legend swatches sit below this (PDF points from the top)

# Street labels in Figure 2-2 -> OSM street names. Vertical labels give x, horizontal give y.
VERTICAL = {"Third St": "3rd Street", "Illinois St": "Illinois Street", "Michigan St": "Michigan Street"}
HORIZONTAL = {"20th St": "20th Street", "22nd St": "22nd Street", "23rd St": "23rd Street",
              "24th St": "24th Street", "25th St": "25th Street", "Humboldt St": "Humboldt Street"}
CONTROL_PAIRS = [
    ("Third St", "20th St"), ("Third St", "22nd St"), ("Third St", "23rd St"), ("Third St", "24th St"), ("Third St", "25th St"),
    ("Illinois St", "20th St"), ("Illinois St", "22nd St"), ("Illinois St", "23rd St"), ("Illinois St", "24th St"),
    ("Illinois St", "25th St"), ("Illinois St", "Humboldt St"),
    ("Michigan St", "24th St"), ("Michigan St", "25th St"),
]

# Figure 2-7 legend: swatch centres in the figure image (pixels) -> height limit in feet.
LEGEND_SWATCHES = {65: (57, 877), 85: (57, 908), 90: (57, 938), 95: (57, 968),
                   125: (243, 877), 128: (243, 908), 180: (243, 938), 300: (243, 968)}
# Regions of the figure image that are not the plan (legend, Block 9 inset, scale bar, title).
FIG27_EXCLUDE = [(0, 790, 1435, 1109), (1170, 380, 1435, 705), (1150, 1000, 1435, 1109)]
FIG27_SCALE_M_PER_PX = 400 * 0.3048 / 193  # 0-400 ft scale bar is about 193 px long
# A point inside each block, read from the figure (pixels), for naming the traced zones.
BLOCK_SEEDS = {
    "13": (350, 400), "14": (505, 360), "1": (545, 445), "2": (690, 445), "3": (855, 445), "4": (980, 445),
    "5": (465, 590), "6": (575, 565), "7": (700, 580), "8": (860, 580), "9": (1000, 630),
    "10": (575, 690), "11": (695, 720), "12": (855, 720),
}
# Labels in the figure that pair an upper (tower) height with a podium height.
PODIUM_FT = {("1", 180): 85, ("5", 180): 85, ("7", 180): 85, ("6", 300): 65}
# Block 9 is drawn as an outline only; its massing depends on whether Unit 3 is kept.
BLOCK_9_PX = (950, 522, 1047, 750)

# Buildings already in the base map (OpenStreetMap via Overture), matched to the EIR.
STACK = {
    "osm": "w678950945",
    "note": "OpenStreetMap footprint mapped at 91.44 m (300 ft), matching the Draft EIR's 300-ft Boiler Stack "
            "(pp. 2-7, 4.D-8) and its position south of the Unit 3 Power Block (Fig. 2-7).",
}
SOPHIE_MAXWELL = {"name": "Sophie Maxwell Building"}

# Per-block stage, from data/projects.json (stageNote). Everything else is entitled.
STAGES = {"2": "construction"}

# Official sources only (Matthew, 2026-10-02). The Draft EIR's height districts are the 2018
# proposal, superseded by the Design for Development approved in 2020, so they are traced (to
# check against the D4D later) but not drawn. True emits them again, labelled illustrative.
DRAW_DEIR_BLOCKS = False


def _streets() -> gpd.GeoDataFrame:
    out = config.RAW / "streets_potrero.parquet"
    if not out.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=transportation/type=segment/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = -122.395, 37.748, -122.375, 37.765
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin) & (pc.field("subtype") == "road"))
        t = d.to_table(columns=["id", "geometry", "names"], filter=f)
        g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                             geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
        g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
        g[["id", "name", "geometry"]].to_parquet(out)
    return gpd.read_parquet(out).to_crs(UTM)


def _intersection(streets: gpd.GeoDataFrame, a: str, b: str) -> tuple[float, float]:
    la = shapely.line_merge(shapely.union_all(streets[streets["name"] == a].geometry.to_numpy()))
    lb = shapely.line_merge(shapely.union_all(streets[streets["name"] == b].geometry.to_numpy()))
    x = la.intersection(lb)
    if x.is_empty:
        raise SystemExit(f"{a} and {b} do not intersect in OpenStreetMap")
    p = x if x.geom_type == "Point" else x.centroid
    return p.x, p.y


def georeference_fig_2_2(page, streets) -> trace.Similarity:
    xs = {k: trace.pdf_label_center(page, k)[0] for k in VERTICAL}
    ys = {k: trace.pdf_label_center(page, k)[1] for k in HORIZONTAL}
    src, dst, labels = [], [], []
    for v, h in CONTROL_PAIRS:
        src.append((xs[v], ys[h]))
        dst.append(_intersection(streets, VERTICAL[v], HORIZONTAL[h]))
        labels.append(f"{VERTICAL[v]} / {HORIZONTAL[h]}")
    return trace.fit_similarity(src, dst, labels)


def _fig27_image(reader: PdfReader) -> np.ndarray:
    images = reader.pages[FIG_2_7["page_index"]].images
    if len(images) != 1:
        raise SystemExit(f"expected one image on the Figure 2-7 page, found {len(images)}")
    from PIL import Image

    img = Image.open(io.BytesIO(images[0].data)).convert("RGB")
    if img.size != (1435, 1109):
        raise SystemExit(f"unexpected Figure 2-7 image size {img.size}")
    return np.asarray(img)


def _in_plan(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    keep = np.ones_like(x, dtype=bool)
    for x0, y0, x1, y1 in FIG27_EXCLUDE:
        keep &= ~((x >= x0) & (x <= x1) & (y >= y0) & (y <= y1))
    return keep


def register_fig_2_7(rgb: np.ndarray, boundary_utm: Polygon, fig22: trace.Similarity) -> trace.Similarity:
    import cv2

    dark = rgb.max(axis=2) < 60
    # Drop ink printed on coloured block fills (block numbers, height labels).
    sat = (rgb.max(axis=2).astype(int) - rgb.min(axis=2).astype(int)) > 40
    near_fill = cv2.dilate(sat.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    ys, xs = np.nonzero(dark & ~near_fill)
    keep = _in_plan(xs, ys)
    pts = np.column_stack([xs[keep], ys[keep]]).astype(float)
    # Start from the scale bar and Figure 2-2's rotation (both plans are drawn on the
    # street grid), with the centres of the two boundaries aligned.
    init = trace.Similarity(FIG27_SCALE_M_PER_PX, fig22.rotation, 0.0, 0.0)
    c_fig = init.apply(pts).mean(axis=0)
    c_utm = np.asarray(boundary_utm.exterior.coords).mean(axis=0)
    init.tx, init.ty = (c_utm - c_fig)
    return trace.icp_similarity(pts, boundary_utm.exterior, init, iterations=80, keep=0.6)


def trace_blocks(rgb: np.ndarray, sim: trace.Similarity, site_utm: Polygon) -> list[dict]:
    palette = {h: tuple(np.median(rgb[sy - 4:sy + 5, sx - 6:sx + 7].reshape(-1, 3), axis=0)) for h, (sx, sy) in LEGEND_SWATCHES.items()}
    zones = []
    for height, poly in trace.raster_classify_regions(rgb, palette, max_dist=30, open_px=5, min_area_px=600):
        c = poly.representative_point()
        if not _in_plan(np.array([c.x]), np.array([c.y]))[0]:
            continue
        block = min(BLOCK_SEEDS, key=lambda b: Point(BLOCK_SEEDS[b]).distance(c))
        zones.append({"block": block, "height_ft": height, "px": poly})
    x0, y0, x1, y1 = BLOCK_9_PX
    zones.append({"block": "9", "height_ft": None, "px": box(x0, y0, x1, y1)})
    out = []
    for z in zones:
        # Clip to the traced site: regions outside it are other colours that resemble the legend.
        geom = shapely.make_valid(sim.geometry(z["px"]).simplify(0.4)).intersection(site_utm)
        geom = trace.as_multipolygon(geom)
        if geom.area >= 100:
            out.append({**z, "utm": geom})
    return out


def _base_buildings(site_utm: Polygon) -> gpd.GeoDataFrame:
    import pyarrow.parquet as pq

    xmin, ymin, xmax, ymax = gpd.GeoSeries([site_utm], crs=UTM).to_crs(4326).total_bounds
    t = pq.read_table(config.RAW / "buildings.parquet", columns=["id", "geometry", "bbox", "height", "sources"],
                      filters=[("bbox", "is_valid", True)] if False else None)
    bb = t.column("bbox")
    m = (pc.and_(pc.and_(pc.less(pc.struct_field(bb, "xmin"), xmax), pc.greater(pc.struct_field(bb, "xmax"), xmin)),
                 pc.and_(pc.less(pc.struct_field(bb, "ymin"), ymax), pc.greater(pc.struct_field(bb, "ymax"), ymin))))
    t = t.filter(m)
    g = gpd.GeoDataFrame(t.drop(["geometry", "bbox"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["record"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("property") in ("", None)), None))
    return g


def _named_building(name: str) -> gpd.GeoDataFrame:
    import pyarrow.parquet as pq

    # Names were not kept in the building extract; look the footprint up in Overture by name.
    for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
        os.environ.pop(k, None)
    cache = config.RAW / "named_buildings_potrero.parquet"
    if not cache.exists():
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = -122.392, 37.751, -122.378, 37.762
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    return g


def main() -> None:
    pdf_path = trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "docs" / "2017-011878ENV_DEIR_Volume_1.pdf",
                                    DEIR["sha256"])
    streets = _streets()

    # --- boundary from Figure 2-2 ---
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[FIG_2_2["page_index"]]
        fig22 = georeference_fig_2_2(page, streets)
        parts = {}
        for name, spec in SUB_AREAS.items():
            polys = trace.pdf_filled_polygons(page, spec["cmyk"], max_top=LEGEND_TOP)
            if not polys:
                raise SystemExit(f"no shapes found for {name}")
            parts[name] = shapely.make_valid(shapely.union_all([fig22.geometry(p) for p in polys]))
    site_utm = trace.largest_polygon(shapely.union_all(list(parts.values()), grid_size=0.05).buffer(0.05).buffer(-0.05))
    print(f"[potrero] Figure 2-2 georeference: RMS {fig22.rms_m:.2f} m over {len(fig22.labels)} intersections, "
          f"site {site_utm.area / 4046.86:.1f} acres")

    # --- blocks from Figure 2-7 ---
    rgb = _fig27_image(PdfReader(pdf_path))
    fig27 = register_fig_2_7(rgb, site_utm, fig22)
    print(f"[potrero] Figure 2-7 registration: RMS {fig27.rms_m:.2f} m ({fig27.labels[0]}), "
          f"scale {fig27.scale:.4f} m/px (scale bar {FIG27_SCALE_M_PER_PX:.4f})")
    zones = trace_blocks(rgb, fig27, site_utm)

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731

    # --- existing buildings matched to the EIR ---
    named = _named_building(SOPHIE_MAXWELL["name"])
    stack = named[named["osm"].fillna("").str.startswith(STACK["osm"])]
    sophie = named[named["name"] == SOPHIE_MAXWELL["name"]]
    if len(stack) != 1 or len(sophie) != 1:
        raise SystemExit(f"expected one stack and one Sophie Maxwell footprint, found {len(stack)} and {len(sophie)}")
    sophie_utm = gpd.GeoSeries(sophie.geometry, crs=4326).to_crs(UTM).iloc[0]

    doc = f"{DEIR['title']}"
    boundary_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "source": f"traced: {doc}, {FIG_2_2['figure']}, p. {FIG_2_2['printed_page']}",
            "sourceUrl": DEIR["url"],
            "accuracy": "traced",
            "accuracyNote": (
                f"Vector shapes from the EIR figure, georeferenced to OpenStreetMap street centrelines at "
                f"{len(fig22.labels)} intersections (RMS {fig22.rms_m:.1f} m). Approximate boundary: parcel lines were not available."),
            "georeference": fig22.report(),
        },
        "features": [
            {"type": "Feature", "properties": {"kind": "site", "name": "Project site"}, "geometry": mapping(to_wgs(site_utm))},
            *[
                {"type": "Feature", "properties": {"kind": "sub-area", "name": name, "owner": SUB_AREAS[name]["owner"]},
                 "geometry": mapping(to_wgs(geom))}
                for name, geom in parts.items()
            ],
        ],
    }

    features = []
    for z in sorted(zones, key=lambda z: (int(z["block"]), z["height_ft"] or 0)) if DRAW_DEIR_BLOCKS else []:
        geom = z["utm"].difference(sophie_utm) if z["block"] == "7" else z["utm"]
        if geom.is_empty or geom.area < 20:
            continue
        podium = PODIUM_FT.get((z["block"], z["height_ft"]))
        props = {
            "kind": "block",
            "block": z["block"],
            "label": f"Block {z['block']}",
            "stage": STAGES.get(z["block"], "entitled"),
            "height_ft": z["height_ft"],
            "podium_ft": podium,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: height district traced from {doc}, {FIG_2_7['figure']}, p. {FIG_2_7['printed_page']}. "
                      "2018 proposal; may differ from the plan approved in 2020.",
        }
        if z["block"] == "9":
            props["note"] = "Drawn as an outline: the 2018 plan gives two configurations, with or without the Unit 3 Power Block."
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(trace.as_multipolygon(geom)))})

    features.append({
        "type": "Feature",
        "properties": {
            "kind": "landmark", "label": "Stack", "name": "Unit 3 Boiler Stack", "stage": "complete",
            "height_ft": 300, "base_ft": 0, "illustrative": False,
            "source": f"height: {doc}, pp. 2-7 and 4.D-8 ('the reinforced concrete Boiler Stack ... at 300 feet in height'); "
                      f"footprint: OpenStreetMap {STACK['osm']} via Overture {config.OVERTURE_RELEASE}",
            "note": STACK["note"], "osm": STACK["osm"],
        },
        "geometry": mapping(stack.geometry.iloc[0]),
    })
    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": DRAW_DEIR_BLOCKS,
            "summary": (
                "Block massing is illustrative: height districts proposed in the 2018 Draft EIR (Fig. 2-7), which "
                "may differ from the plan approved in 2020. Blocks are drawn as podium solids with the upper height "
                "limit as a faint envelope; tower positions are not specified in the source."
                if DRAW_DEIR_BLOCKS else
                "Only official, current facts are drawn: the 300-ft boiler stack. Block massing waits for the "
                "Design for Development approved in 2020; the 2018 Draft EIR blocks are superseded and not drawn."
            ),
            **({"georeference": {"figure_2_7": fig27.report(), "registered_to": "Figure 2-2 site boundary"}}
               if DRAW_DEIR_BLOCKS else {}),
            "license": ("Block shapes: traced from a public SF Planning document. " if DRAW_DEIR_BLOCKS else "")
                       + "Stack footprint: OpenStreetMap contributors (ODbL 1.0).",
        },
        "features": features,
    }

    for folder, fc in (("boundaries", boundary_fc), ("massing", massing_fc)):
        path = config.ROOT / "data" / folder / f"{PROJECT_ID}.geojson"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_round(fc), indent=1) + "\n")
        print(f"[potrero] wrote {path.relative_to(config.ROOT)} ({len(fc['features'])} features)")


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
