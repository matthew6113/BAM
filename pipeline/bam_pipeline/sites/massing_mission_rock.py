"""Mission Rock: block height limits from the adopted zoning map, and the built Phase 1 buildings.

Sources:
- Block height limits: DataSF "Zoning Map – Height and Bulk Districts" (h9wh-cg3m, Public Domain U.S.
  Government). Inside the Mission Rock Special Use District the layer is drawn block by block:
  districts named "<height>-Mission Rock" (Planning Code Sec. 291, Zoning Map sheet HT08 as amended
  for the project). Streets, China Basin Park and Mission Rock Square are district "OS" and are left
  out. "90/120-Mission Rock" means 90 ft for commercial use and 120 ft for residential use (Draft EIR
  Figure 2-4 note and Table 2-4).
- Block letters: Draft EIR Chapter 2 (Case No. 2013.0208E, April 2017), Figure 2-4 "Proposed Site Plan
  and Height Ranges" (p. 2-21), rendered at 200 dpi and georeferenced on street-centreline
  intersections matched to OpenStreetMap (via Overture). Each zoning block takes the letter whose
  height label falls inside it. Table 2-4 (p. 2-23) heights are checked against the zoning.
- Built Phase 1 (A, B, F, G; completed 2025 per the Port's June 2026 report): footprints from
  OpenStreetMap via Overture; stories from DBI building permits (A 24, F 23, G 13, B 8). Heights are
  the footprints' mapped heights in OpenStreetMap, except Building B, which has no mapped height and
  is estimated from its permitted stories with the Draft EIR's story-height rule (Table 2-4, note b).

What this is and isn't:
- Unbuilt blocks are drawn to their zoning height limits, not as building designs, so they are
  labelled illustrative. The zoning splits blocks into a main zone and lower edge zones (the 40- and
  60-ft "base height" strips of Figure 2-4); each zone is drawn at its own limit.
- The adopted Mission Rock Design Controls (Planning Commission Resolution 20021) weren't located, so
  the zoning layer stands in for them; it matches Table 2-4 block by block.
- Pier 48's historic sheds (to be rehabilitated, not rebuilt) stay in the base map, not drawn here.
- Rooftop elements allowed above the limits (up to 20 ft, 40 ft on Block F; Draft EIR p. 2-35) aren't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_mission_rock
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Point, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "mission-rock"
UTM = "EPSG:26910"
FT = 0.3048
BBOX = (-122.3935, 37.7715, -122.3815, 37.7800)  # lon/lat window around the site

HEIGHTS = {
    "title": "DataSF Zoning Map – Height and Bulk Districts",
    "landing": "https://data.sf.gov/d/h9wh-cg3m",
    "url": "https://data.sf.gov/resource/h9wh-cg3m.geojson?" + urllib.parse.urlencode({
        "$where": "intersects(the_geom, 'POLYGON((-122.3935 37.7715, -122.3815 37.7715, -122.3815 37.78, "
                  "-122.3935 37.78, -122.3935 37.7715))')",
        "$limit": 5000,
    }),
    "license": "Public Domain U.S. Government (DataSF)",
}

DEIR = {
    "title": "Seawall Lot 337 and Pier 48 Mixed-Use Project Draft EIR, Chapter 2 (Case No. 2013.0208E, April 2017)",
    "url": "https://sfplanning.s3.amazonaws.com/sfmea/MissionRock_Ch_2_ProjectDescription.pdf",
    "sha256": "13f8f3f15de2c6e484e5584936d0b2e13365fee5dbeddedd9b4f139e3436cdea",
}
FIG_2_4 = {"page_index": 20, "printed_page": "2-21", "figure": "Figure 2-4, Proposed Site Plan and Height Ranges"}
FIG_DPI = 200
# Street centrelines in the 200-dpi render (pixels): midway between the block edges on either side.
# Third Street's centreline is the Muni line drawn down its median.
FIG_CONTROLS = {
    ("3rd Street", "Toni Stone Crossing"): (673.0, 734.0),  # Exposition Street in the figure
    ("Dr. Maya Angelou Way", "Toni Stone Crossing"): (830.0, 734.0),  # Shared Public Way
    ("Bridgeview Way", "Toni Stone Crossing"): (979.0, 734.0),
    ("3rd Street", "Long Bridge Street"): (673.0, 1092.0),
    ("3rd Street", "Mission Rock Street"): (673.0, 1272.0),
    ("Bridgeview Way", "Mission Rock Street"): (979.0, 1272.0),
}
# Centre of each block's height label in the render (pixels), and Table 2-4's height for the block.
FIG_LABELS = {
    "A": (755, 673), "G": (907, 675), "K": (1039, 675),
    "B": (760, 822), "F": (907, 794), "J": (1039, 825),
    "C": (760, 1005), "E": (905, 1034), "I": (1039, 1000),
    "D1": (745, 1205), "D2": (905, 1186), "H": (1039, 1185),
}
TABLE_2_4 = {"A": 240, "B": 120, "C": 190, "D1": 240, "D2": 100, "E": 90, "F": 240, "G": 190,
             "H": "90/120", "I": "90/120", "J": "90/120", "K": 120}
USE = {"A": "Residential", "D1": "Residential", "F": "Residential", "K": "Residential",
       "B": "Commercial", "C": "Commercial", "E": "Commercial", "G": "Commercial",
       "H": "Residential or commercial", "I": "Residential or commercial", "J": "Residential or commercial",
       "D2": "Parking"}

# Phase 1, complete (Port Item 11A, June 9, 2026). OSM way ids of the footprints in Overture, and
# the DBI permits that give the stories.
PORT_2606 = "https://www.sfport.com/sites/default/files/2026-06/item_11a_mission_rock_phase_2_update_and_port_capital.pdf"
BUILT = {
    "A": {"osm": "w1204801756", "permit": "201910073782", "stories": 24, "use": "Residential", "landmark": True},
    "F": {"osm": "w1204801749", "permit": "201910073784", "stories": 23, "use": "Residential", "landmark": True},
    "G": {"osm": "w1204801755", "permit": "201910073785", "stories": 13, "use": "Office", "landmark": False},
    "B": {"osm": "w1204801750", "permit": "201910285744", "stories": 8, "use": "Office", "landmark": False},
}
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"


def _fetch_heights() -> gpd.GeoDataFrame:
    out = config.ROOT / "data" / "raw" / "massing" / "mission_rock_height_bulk.geojson"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(HEIGHTS["url"]) as r:
            out.write_bytes(r.read())
    return gpd.read_file(out).to_crs(UTM)


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "named_buildings_mission_rock.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    # Whether the height came from OpenStreetMap itself (mapped) or was filled in by another dataset.
    g["height_from"] = g["sources"].apply(
        lambda s: next((x.get("dataset") for x in s if x.get("property") == "/properties/height"), "OpenStreetMap"))
    return g.to_crs(UTM)


def _georeference(pdf_path) -> tuple[trace.Similarity, np.ndarray]:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG_2_4["page_index"]]
    rgb = np.asarray(page.render(scale=FIG_DPI / 72).to_pil().convert("RGB"))
    if rgb.shape[:2] != (1700, 2200):
        raise SystemExit(f"unexpected Figure 2-4 render size {rgb.shape}")
    streets = tb.streets("mission_rock", BBOX)
    streets = streets[streets["subtype"] == "road"]
    src, dst, labels = [], [], []
    for (a, b), xy in FIG_CONTROLS.items():
        src.append(xy)
        dst.append(tb.intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels), rgb


def _blocks(zones: gpd.GeoDataFrame, sim: trace.Similarity) -> list[str]:
    """Each zone's block letter: zones that touch form a block; the block takes the Figure 2-4 label inside it."""
    merged = shapely.union_all([g.buffer(1.0) for g in zones.geometry])
    blocks = list(getattr(merged, "geoms", [merged]))
    pts = {k: Point(sim.apply([xy])[0]) for k, xy in FIG_LABELS.items()}
    out = []
    for g in zones.geometry:
        blk = next(b for b in blocks if b.intersects(g))
        inside = [k for k, p in pts.items() if blk.contains(p)]
        if not inside:
            raise SystemExit(f"no Figure 2-4 label falls in the zoning block at {g.centroid}")
        out.append(min(inside, key=lambda k: g.distance(pts[k])) if len(inside) > 1 else inside[0])
    used = set(out)
    if used != set(FIG_LABELS):
        raise SystemExit(f"blocks without a zoning zone: {sorted(set(FIG_LABELS) - used)}")
    return out


def _height(district: str) -> tuple[int, int | None]:
    """'240-Mission Rock' -> (240, None); '90/120-Mission Rock' -> (120, 90)."""
    h = district.split("-")[0]
    if "/" in h:
        lo, hi = (int(x) for x in h.split("/"))
        return hi, lo
    return int(h), None


def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    hb = _fetch_heights()
    zones = hb[hb["height"].str.endswith("-Mission Rock")].explode(index_parts=False).reset_index(drop=True)
    zones = zones[zones.geometry.area > 20].reset_index(drop=True)
    outside = zones[~zones.geometry.representative_point().within(site_utm)]
    if len(outside):
        raise SystemExit(f"{len(outside)} Mission Rock height zones fall outside the site")
    print(f"[mission-rock] {len(zones)} Mission Rock height zones: "
          + ", ".join(sorted(set(zones["height"].str.replace("-Mission Rock", "")), key=lambda s: int(s.split('/')[-1]))))

    pdf_path = trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "docs" / "MissionRock_Ch_2_ProjectDescription.pdf",
                                    DEIR["sha256"])
    sim, _ = _georeference(pdf_path)
    print(f"[mission-rock] Figure 2-4 georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale:.4f} m/px")
    zones["block"] = _blocks(zones, sim)

    # Table 2-4 check: each block's highest zone matches the Draft EIR.
    for blk, grp in zones.groupby("block"):
        top = max(grp["height"], key=lambda h: _height(h)[0]).replace("-Mission Rock", "")
        want = str(TABLE_2_4[blk])
        if top != want:
            raise SystemExit(f"Block {blk}: zoning {top} ft vs Draft EIR Table 2-4 {want} ft")
    print("[mission-rock] zoning heights match Draft EIR Table 2-4 for every block")

    # Built Phase 1 footprints, each checked to sit on its block.
    bldgs = _buildings()
    built = {}
    for blk, spec in BUILT.items():
        hit = bldgs[bldgs["osm"].fillna("").str.split("@").str[0] == spec["osm"]]
        if len(hit) != 1:
            raise SystemExit(f"Building {blk}: expected one footprint {spec['osm']}, found {len(hit)}")
        row = hit.iloc[0]
        block_area = shapely.union_all(zones[zones["block"] == blk].geometry.to_numpy())
        cover = row.geometry.intersection(block_area).area / block_area.area
        if cover < 0.7:
            raise SystemExit(f"Building {blk}: footprint covers only {cover:.0%} of its zoning block")
        built[blk] = row
        print(f"[mission-rock] Building {blk}: {spec['osm']} ({row['name']}), covers {cover:.0%} of the block, "
              f"mapped height {row['height']} m from {row['height_from']}")
    built_union = shapely.union_all([r.geometry for r in built.values()])

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    fig = f"{DEIR['title']}, {FIG_2_4['figure']}, p. {FIG_2_4['printed_page']}"
    features = []

    # Unbuilt blocks: each zoning zone at its limit. Built blocks are replaced by their buildings.
    order = ["K", "J", "I", "H", "C", "E", "D1", "D2"]
    for _, z in sorted(zones.iterrows(), key=lambda kv: (order.index(kv[1]["block"]) if kv[1]["block"] in order else -1,
                                                       -_height(kv[1]["height"])[0])):
        blk = z["block"]
        if blk in BUILT:
            continue
        geom = z.geometry.difference(built_union) if z.geometry.intersects(built_union) else z.geometry
        geom = shapely.make_valid(geom.simplify(0.3))
        if geom.is_empty or geom.area < 20:
            continue
        height, lower = _height(z["height"])
        district = z["height"]
        is_main = str(TABLE_2_4[blk]).split("/")[-1] == str(height)
        props = {
            "kind": "block",
            "block": blk,
            "label": f"Block {blk}",
            "stage": "entitled",
            "height_ft": height,
            "podium_ft": lower,
            "base_ft": 0,
            "use": USE[blk] if is_main else None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the height limit of zoning district \"{district}\" in {HEIGHTS['title']} "
                      f"({HEIGHTS['landing']}); block letter from {fig}",
        }
        if lower:
            props["note"] = (f"{lower} ft if commercial, {height} ft if residential (Draft EIR Fig. 2-4 and Table 2-4): "
                             f"solid to {lower} ft, with the residential allowance as a faint envelope.")
        elif not is_main:
            props["note"] = f"Lower {height}-ft edge zone of the block (the base height shown in Draft EIR Fig. 2-4)."
        features.append({"type": "Feature", "properties": props,
                         "geometry": mapping(to_wgs(trace.as_multipolygon(geom)))})

    # Built Phase 1 buildings.
    for blk in ("A", "F", "G", "B"):
        spec, row = BUILT[blk], built[blk]
        permit = f"DBI permit {spec['permit']} ({PERMIT_URL.format(spec['permit'])}): {spec['stories']} stories"
        footprint = f"footprint: OpenStreetMap {spec['osm']} via Overture {config.OVERTURE_RELEASE}"
        mapped = row["height_from"] == "OpenStreetMap" and row["height"] == row["height"]
        if mapped:
            height_ft = round(float(row["height"]) / FT)
            height_src = f"height: {row['height']:.1f} m as mapped in OpenStreetMap"
            illustrative = False
            note = None
        else:
            # Draft EIR Table 2-4 note b: commercial floors average 14 ft, the ground floor about 18 ft.
            height_ft = 18 + 14 * (spec["stories"] - 1)
            height_src = (f"height estimated from the permitted stories with {DEIR['title']}, Table 2-4 note b "
                          f"(ground floor about 18 ft, commercial floors 14 ft): 18 + 14 × {spec['stories'] - 1} ft")
            illustrative = True
            note = "No mapped height: the height is estimated from the permitted stories."
        source = f"{footprint}; stories: {permit}; {height_src}; complete per Port of SF, June 9, 2026 ({PORT_2606})"
        props = {
            "kind": "landmark" if spec["landmark"] else "building",
            "block": blk,
            "label": f"Building {blk}",
            "stage": "complete",
            "height_ft": height_ft,
            "podium_ft": None,
            "base_ft": 0,
            "use": spec["use"],
            "phase": "Phase 1",
            "illustrative": illustrative,
            "source": ("illustrative: " if illustrative else "") + source,
            "stories": spec["stories"],
        }
        if note:
            props["note"] = note
        geom = shapely.make_valid(row.geometry.simplify(0.3))
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})

    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: the unbuilt blocks are drawn to their height limits in the Mission Rock "
                "height and bulk districts of the city's zoning map, not as building designs. The four Phase 1 "
                "buildings (A, B, F and G) are drawn from their real footprints, with stories from building "
                "permits; Building B's height is estimated from its stories. Parks, streets and Pier 48's "
                "historic sheds aren't drawn."
            ),
            "note": ("Unbuilt blocks are drawn to their zoning height limits, not as building designs; "
                     "real buildings will be smaller."),
            "sourceUrl": HEIGHTS["landing"],
            "sourceLabel": "Height and bulk districts (DataSF)",
            "georeference": {
                "zoning": "GIS layer, used as published (no tracing)",
                "figure_2_4": {**sim.report(), "use": "block letters only"},
            },
            "license": ("Block shapes: DataSF zoning map (Public Domain U.S. Government). Building footprints and "
                        "mapped heights: OpenStreetMap contributors (ODbL 1.0), via Overture Maps."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(massing_fc), indent=1) + "\n")
    print(f"[mission-rock] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


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
