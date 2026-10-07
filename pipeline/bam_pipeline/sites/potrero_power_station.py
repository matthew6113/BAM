"""Potrero Power Station: site boundary and block height limits, traced from official documents.

Sources:
- Boundary and sub-areas: Draft EIR, Volume 1 (SF Planning Case No. 2017-011878ENV, Oct 2018),
  Figure 2-2 (p. 2-6), vector shapes in the PDF.
- Block height limits: Design for Development (D4D), Feb 26, 2020, approved by Planning
  Commission Motion 20638, Figure 6.2.3 Building Height Plan (p. 245).
- Stack height (300 ft): Draft EIR pp. 2-7 and 4.D-8.

What this is and isn't:
- The D4D is the approved plan in force. Amendments proposed in 2026 (Addendum 2: +8 ft on
  residential blocks, more on Blocks 1, 5, 11, 12 and 15) aren't drawn until the Board adopts them.
- Each block is drawn to its height limit, not as a building design: real buildings will be
  smaller, and towers rise to the upper limit only on part of a block ("180'/85'" in the figure
  means a tower zone up to 180 ft over an 85-ft base). So the massing is labelled illustrative.
- Block 9 depends on whether Unit 3 is kept (two configurations in the figure), so it is outlined only.
- The "MAX" dimensions in the figure are plan-length limits (bulk), not heights.

Georeferencing:
- Figure 2-2: street-name labels in the PDF give street centrelines in figure coordinates,
  matched to OpenStreetMap intersections (via Overture) with a least-squares similarity fit.
- Figure 6.2.3: rendered at 200 dpi. Street centrelines are the midpoints of the curb lines
  measured beside seven intersections, including streets built in Phase 1 (Maryland, Humboldt)
  that are now in OpenStreetMap. Residuals are recorded in the output.

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

D4D = {
    "title": "Potrero Power Station Design for Development (Feb 26, 2020; Planning Commission Motion 20638)",
    "url": "https://sfplanning.org/sites/default/files/documents/citywide/potreropower_D4D_final.pdf",
    "sha256": "908b5e928dca888c0d0340417d85463361eae41819db81ce65cef72c42e267da",
}
FIG_6_2_3 = {"page_index": 246, "printed_page": "245", "figure": "Figure 6.2.3, Building Height Plan"}
D4D_DPI = 200
# Street centrelines in the 200-dpi render (pixels): midpoints of the curb lines measured on
# straight stretches next to each intersection.
D4D_CONTROLS = {
    ("Illinois Street", "22nd Street"): (416.75, 385.5),
    ("Illinois Street", "23rd Street"): (416.75, 1040.0),
    ("3rd Street", "22nd Street"): (209.5, 385.5),
    ("3rd Street", "23rd Street"): (225.5, 1039.25),
    ("Maryland Street", "22nd Street"): (1187.5, 373.0),
    ("Maryland Street", "Humboldt Street"): (1187.0, 685.0),
    ("Maryland Street", "23rd Street"): (1187.5, 1041.0),
}
# Legend swatch centres (pixels) -> height limit in feet.
D4D_LEGEND = {35: (186, 1198), 65: (186, 1240), 85: (186, 1282), 90: (186, 1322), 100: (186, 1364), 125: (186, 1404),
              130: (444, 1198), 145: (444, 1240), 160: (444, 1282), 180: (444, 1322), 220: (444, 1364), 240: (444, 1404)}
# Each block's extent in the render (pixels), for naming the traced zones.
D4D_BLOCKS = {
    "13": (436, 406, 730, 660), "14": (774, 406, 870, 510), "1": (780, 524, 950, 660), "2": (976, 524, 1166, 660),
    "3": (1206, 524, 1390, 660), "4": (1410, 524, 1534, 660), "5": (660, 708, 840, 880), "15": (860, 708, 950, 1010),
    "7": (976, 708, 1166, 850), "8": (1206, 708, 1390, 850), "9": (1424, 708, 1540, 940), "11": (976, 924, 1166, 1010),
    "12": (1206, 924, 1390, 1010),
}
# Tower zones: upper height limit over a base height ("180'/85'" in the figure).
D4D_BASE_FT = {("1", 180): 85, ("5", 220): 85, ("7", 240): 85}

# Buildings already in the base map (OpenStreetMap via Overture), matched to the EIR.
STACK = {
    "osm": "w678950945",
    "note": "OpenStreetMap footprint mapped at 91.44 m (300 ft), matching the Draft EIR's 300-ft Boiler Stack "
            "(pp. 2-7, 4.D-8) and its position south of the Unit 3 Power Block (Fig. 2-7).",
}
SOPHIE_MAXWELL = {"name": "Sophie Maxwell Building"}

# Per-block stage. Blocks are entitled unless an official record says otherwise; the one
# finished building (Sophie Maxwell) is cut out of its block. UCSF's Block 2 building is under
# construction per the Planning Commission's finding in Resolution 21945 (July 30, 2026); UC
# buildings have no city building permit, so there is no permit date.
STAGES: dict[str, str] = {"2": "construction"}
STAGE_NOTES: dict[str, str] = {
    "2": "Under construction: UCSF's building (Planning Commission Resolution 21945, July 30, 2026, finding 4: "
         "'construction has commenced')."
}


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


def _d4d_render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG_6_2_3["page_index"]]
    rgb = np.asarray(page.render(scale=D4D_DPI / 72).to_pil().convert("RGB"))
    if rgb.shape[:2] != (1700, 2200):
        raise SystemExit(f"unexpected Figure 6.2.3 render size {rgb.shape}")
    return rgb


def georeference_fig_6_2_3(streets) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), xy in D4D_CONTROLS.items():
        src.append(xy)
        dst.append(_intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def _block_of(pt: Point) -> str | None:
    return next((b for b, (x0, y0, x1, y1) in D4D_BLOCKS.items() if x0 <= pt.x <= x1 and y0 <= pt.y <= y1), None)


def trace_height_zones(rgb: np.ndarray, sim: trace.Similarity) -> list[dict]:
    """Trace each block's height zones from Figure 6.2.3.

    Within a block's extent, pixels take the nearest legend colour. Labels and dimension lines
    printed on the fills leave gaps, so each block's outline is the closed, hole-filled union of
    its coloured pixels, and every gap pixel inside it takes the colour of the nearest fill.
    """
    import cv2

    heights = list(D4D_LEGEND)
    palette = np.array([np.median(rgb[y - 5:y + 6, x - 12:x + 13].reshape(-1, 3), axis=0) for x, y in D4D_LEGEND.values()])
    zones = []
    for block, (x0, y0, x1, y1) in D4D_BLOCKS.items():
        if block == "9":
            continue
        sub = rgb[y0:y1, x0:x1].astype(float)
        dist = np.linalg.norm(sub[:, :, None, :] - palette[None, None], axis=3)
        # A tight match: anti-aliased edges of text and lines fall between colours and are filled below.
        label = np.where(dist.min(axis=2) <= 15, dist.argmin(axis=2), -1)
        coloured = (label >= 0).astype(np.uint8)
        coloured = cv2.morphologyEx(coloured, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        label[coloured == 0] = -1
        # The block: close the gaps text leaves, then fill holes.
        mask = cv2.morphologyEx(coloured * 255, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(mask)
        cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, 255, cv2.FILLED)
        # Gap pixels take the nearest coloured pixel's height.
        _, nearest = cv2.distanceTransformWithLabels((label < 0).astype(np.uint8), cv2.DIST_L2, 5,
                                                     labelType=cv2.DIST_LABEL_PIXEL)
        seeds = np.flatnonzero(label.ravel() >= 0)  # zero pixels are numbered in scan order from 1
        filled = label.ravel()[seeds][nearest.ravel() - 1].reshape(label.shape)
        for i in np.unique(filled[mask > 0]):
            part = ((filled == i) & (mask > 0)).astype(np.uint8) * 255
            part = cv2.morphologyEx(part, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
            polys = [shapely.make_valid(Polygon(cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2) + [x0, y0]))
                     for c in cv2.findContours(part, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                     if cv2.contourArea(c) >= 400]
            if polys:
                # Dimension lines split a zone into touching pieces; join them again.
                merged = shapely.union_all(polys).buffer(3, join_style="mitre").buffer(-3, join_style="mitre")
                zones.append({"block": block, "height_ft": heights[i], "px": merged})
    # Block 9 is drawn white, as an outline: the white area inside its extent.
    x0, y0, x1, y1 = D4D_BLOCKS["9"]
    white = (rgb[y0:y1, x0:x1].min(axis=2) > 235).astype(np.uint8) * 255
    contours, _ = cv2.findContours(white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    zones.append({"block": "9", "height_ft": None, "px": Polygon(cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2) + [x0, y0])})
    for z in zones:
        z["utm"] = trace.as_multipolygon(shapely.make_valid(sim.geometry(z["px"]).simplify(0.3)))
    return [z for z in zones if z["utm"].area >= 30]


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

    # --- height zones from the D4D's Figure 6.2.3 ---
    d4d_path = trace.fetch_document(D4D["url"], config.ROOT / "data" / "raw" / "docs" / "potreropower_D4D_final.pdf", D4D["sha256"])
    fig623 = georeference_fig_6_2_3(streets)
    print(f"[potrero] Figure 6.2.3 georeference: RMS {fig623.rms_m:.2f} m over {len(fig623.labels)} intersections, "
          f"scale {fig623.scale:.4f} m/px")
    zones = trace_height_zones(_d4d_render(d4d_path), fig623)
    print(f"[potrero] traced {len(zones)} height zones: "
          + ", ".join(f"{z['block']}:{z['height_ft']}" for z in sorted(zones, key=lambda z: (int(z['block']), z['height_ft'] or 0))))

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
            "sourceLabel": "Draft EIR, Oct 2018 (PDF)",
            "accuracyShort": f"about ±{fig22.rms_m:.0f} m",
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

    d4d = f"{D4D['title']}, {FIG_6_2_3['figure']}, p. {FIG_6_2_3['printed_page']}"
    features = []
    for z in sorted(zones, key=lambda z: (int(z["block"]), z["height_ft"] or 0)):
        geom = z["utm"].difference(sophie_utm) if z["utm"].intersects(sophie_utm) else z["utm"]
        if geom.is_empty or geom.area < 20:
            continue
        base = D4D_BASE_FT.get((z["block"], z["height_ft"]))
        props = {
            "kind": "block",
            "block": z["block"],
            "label": f"Block {z['block']}",
            "stage": STAGES.get(z["block"], "entitled"),
            "height_ft": z["height_ft"],
            "podium_ft": base,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the height limit traced from {d4d}"
                      + (f"; tower zone up to {z['height_ft']} ft over an {base}-ft base" if base else ""),
        }
        if z["block"] in STAGE_NOTES:
            props["note"] = STAGE_NOTES[z["block"]]
        if z["block"] == "9":
            props["note"] = "Outlined only: the D4D gives two configurations, with or without the Unit 3 Power Block."
        if z["utm"].intersects(sophie_utm):
            props["note"] = "The built Sophie Maxwell Building (1212 Maryland St.) is cut out of this block."
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
            "illustrative": True,
            "summary": (
                "Illustrative massing: each block is drawn to its height limit in the Design for Development "
                "approved in 2020 (Fig. 6.2.3), not as a building design. Towers may reach the faint upper "
                "envelope on only part of a block. Proposed 2026 amendments that would raise some limits aren't "
                "drawn until the Board adopts them."
            ),
            "note": ("Blocks are drawn to their height limits in the 2020 Design for Development, not as building "
                     "designs; real buildings will be smaller."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2020 (PDF)",
            "georeference": {"figure_6_2_3": fig623.report()},
            "license": "Block shapes: traced from a public SF Planning document. "
                       "Stack footprint: OpenStreetMap contributors (ODbL 1.0).",
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
