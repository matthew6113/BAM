"""Turn the raw Overture extracts into map layers.

Outputs (data/build/*.geojsonl and public/generated/data/labels.geojson):
- region_mask: land outside the nine counties, drawn as a quiet tint
- water: ocean, bay, rivers, lakes, reservoirs and ponds, each with a minzoom
- shoreline: hairlines along the dissolved water edge, islands included
- context: freeways, rail transit and ferry routes (hidden by default in the map)
- labels.geojson: the curated city and water labels
- src/generated/region.json: extent and pan limits used by the app

    uv run --directory pipeline python -m bam_pipeline.process
"""

from __future__ import annotations

import json
import math

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import LineString, MultiLineString, Point, box, mapping

from . import config, labels

EQUAL_AREA = "EPSG:3310"  # California Albers, metres


def _write_geojsonl(path, features) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for feat in features:
            f.write(json.dumps(feat, separators=(",", ":")))
            f.write("\n")
            n += 1
    return n


def _feature(geom, props: dict, minzoom: int | None = None) -> dict:
    feat = {"type": "Feature", "geometry": mapping(geom), "properties": props}
    if minzoom is not None:
        feat["tippecanoe"] = {"minzoom": int(minzoom)}
    return feat


def _area_km2(geoms: gpd.GeoSeries) -> np.ndarray:
    return geoms.to_crs(EQUAL_AREA).area.to_numpy() / 1e6


def _minzoom_for_area(km2: float) -> int:
    # Water bodies appear once they are a few pixels across.
    if km2 >= 50:
        return 4
    if km2 >= 5:
        return 7
    if km2 >= 1:
        return 9
    if km2 >= 0.2:
        return 10
    if km2 >= 0.05:
        return 11
    if km2 >= 0.01:
        return 12
    if km2 >= 0.002:
        return 13
    return 14


# ---------------------------------------------------------------- region

def build_region() -> tuple[shapely.Geometry, dict]:
    counties = gpd.read_parquet(config.RAW / "counties.parquet")
    counties["name"] = counties["names"].apply(lambda n: n["primary"])
    ours = counties[counties["name"].isin(config.COUNTIES)]
    missing = set(config.COUNTIES) - set(ours["name"])
    if missing:
        raise SystemExit(f"[process] counties missing from Overture: {sorted(missing)}")
    region = shapely.make_valid(shapely.union_all(ours.geometry.to_numpy()))
    land = ours[ours["class"] == "land"]
    xmin, ymin, xmax, ymax = shapely.union_all(land.geometry.to_numpy()).bounds
    pad_x, pad_y = 0.25, 0.2
    info = {
        "overtureRelease": config.OVERTURE_RELEASE,
        "counties": config.COUNTIES,
        "extent": [round(v, 4) for v in (xmin, ymin, xmax, ymax)],
        "maxBounds": [
            round(max(xmin - pad_x, config.FETCH_BBOX[0]), 4),
            round(max(ymin - pad_y, config.FETCH_BBOX[1]), 4),
            round(min(xmax + pad_x, config.FETCH_BBOX[2]), 4),
            round(min(ymax + pad_y, config.FETCH_BBOX[3]), 4),
        ],
    }
    mask = box(*config.FETCH_BBOX).difference(region)
    n = _write_geojsonl(config.BUILD / "region_mask.geojsonl", [_feature(mask, {}, 0)])
    print(f"[process] region: extent {info['extent']}, mask features {n}")
    return region, info


# ---------------------------------------------------------------- water

WATER_KIND = {
    ("ocean", "ocean"): "ocean",
    ("lake", "lake"): "lake",
    ("lake", "lagoon"): "lake",
    ("lake", "oxbow"): "lake",
    ("reservoir", "reservoir"): "reservoir",
    ("reservoir", "basin"): "reservoir",
    ("river", "river"): "river",
    ("stream", "stream"): "river",
    ("canal", "canal"): "canal",
    ("pond", "pond"): "pond",
    ("pond", "fishpond"): "pond",
    ("water", "water"): "water",
    ("water", "tidal_channel"): "river",
    ("water", "dock"): "water",
    ("human_made", "salt_pond"): "salt_pond",
}


def build_water() -> gpd.GeoDataFrame:
    w = gpd.read_parquet(config.RAW / "water.parquet")
    w = w[w.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].copy()
    w["kind"] = [WATER_KIND.get((s, c)) for s, c in zip(w["subtype"], w["class"])]
    w = w[w["kind"].notna()]
    ponds_path = config.RAW / "salt_ponds.parquet"
    if ponds_path.exists():
        ponds = gpd.read_parquet(ponds_path)
        ponds = ponds[ponds.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].copy()
        ponds["kind"] = "salt_pond"
        ponds["is_intermittent"] = False
        w = gpd.GeoDataFrame(
            gpd.pd.concat([w[["geometry", "kind", "is_intermittent"]], ponds[["geometry", "kind", "is_intermittent"]]],
                          ignore_index=True),
            crs=w.crs,
        )
    # Intermittent water (seasonal ponds, dry lakebeds) would read as permanent.
    w = w[~((w["is_intermittent"] == True) & (w["kind"] != "ocean"))]  # noqa: E712
    w["geometry"] = shapely.make_valid(shapely.clip_by_rect(w.geometry.to_numpy(), *config.FETCH_BBOX))
    w = w[~w.geometry.is_empty]
    w = w.explode(index_parts=False)
    w = w[w.geometry.geom_type == "Polygon"]
    w["km2"] = _area_km2(w.geometry)
    w = w[(w["km2"] >= 0.0005) | (w["kind"] == "ocean")]
    feats = []
    for geom, kind, km2 in zip(w.geometry, w["kind"], w["km2"]):
        mz = 0 if kind == "ocean" else _minzoom_for_area(km2)
        feats.append(_feature(geom, {"kind": kind}, mz))
    n = _write_geojsonl(config.BUILD / "water.geojsonl", feats)
    print(f"[process] water: {n:,} polygons ({w['kind'].value_counts().to_dict()})")
    return w


def build_shoreline(water: gpd.GeoDataFrame) -> None:
    frame = box(*config.FETCH_BBOX).exterior.buffer(1e-5)
    feats = []

    def add_ring(ring, kind: str) -> None:
        km2 = gpd.GeoSeries([shapely.Polygon(ring)], crs=4326).pipe(_area_km2)[0]
        line = LineString(ring.coords).difference(frame)
        if line.is_empty:
            return
        mz = 0 if km2 >= 500 else _minzoom_for_area(km2)
        parts = line.geoms if isinstance(line, MultiLineString) else [line]
        for part in parts:
            if part.length > 0:
                feats.append(_feature(part, {"kind": kind}, mz))

    shore_src = water[water["kind"] != "salt_pond"]
    merged = shapely.union_all(shore_src.geometry.to_numpy(), grid_size=1e-7)
    polys = merged.geoms if hasattr(merged, "geoms") else [merged]
    for poly in polys:
        if poly.geom_type != "Polygon":
            continue
        add_ring(poly.exterior, "shore")
        for hole in poly.interiors:
            add_ring(hole, "shore")
    salt = water[water["kind"] == "salt_pond"]
    for geom in salt.geometry:
        add_ring(geom.exterior, "salt_pond")
    n = _write_geojsonl(config.BUILD / "shoreline.geojsonl", feats)
    print(f"[process] shoreline: {n:,} line features")


# ---------------------------------------------------------------- context lines

# Railroads: transit (BART, Muni, VTA, cable cars, SFO AirTrain) and active standard-gauge
# railroads (Caltrain, SMART, Union Pacific and BNSF lines, Capitol Corridor/ACE track).
# Narrow-gauge, funicular and "unknown" track (often heritage or disused) are left out.
RAIL_CLASSES = {"subway", "light_rail", "tram", "monorail", "standard_gauge"}
RAIL_EXCLUDE_FLAGS = {"is_abandoned", "is_disused", "is_under_construction"}


def _flag_values(flags) -> set[str]:
    out: set[str] = set()
    if flags is None:
        return out
    for rule in flags:
        values = rule.get("values") if rule is not None else None
        if values is not None and len(values) > 0:
            out.update(str(v) for v in values)
    return out


def _rail_minzoom(cls: str, name: str, km: float) -> int:
    """Named lines and long stretches from the regional view; yards and spurs only up close."""
    if cls != "standard_gauge" or name or km >= 1.0:
        return 8
    return 13 if km < 0.3 else 11


def build_context(region) -> None:
    s = gpd.read_parquet(config.RAW / "segments.parquet")
    s["name"] = s["names"].apply(lambda n: (n or {}).get("primary") or "")
    s["km"] = s.geometry.to_crs(EQUAL_AREA).length.to_numpy() / 1000
    feats = []
    counts = {"freeway": 0, "highway": 0, "rail": 0, "ferry": 0}
    prepared = shapely.prepared.prep(region.buffer(0.02))
    rows = zip(s.geometry, s["subtype"], s["class"], s["subclass"], s["name"], s["rail_flags"], s["km"])
    for geom, subtype, cls, subclass, name, flags, km in rows:
        if subtype == "road" and cls in ("motorway", "trunk"):
            kind = "freeway" if cls == "motorway" else "highway"
            # On- and off-ramps only once interchanges are legible.
            minzoom = 12 if subclass == "link" else (7 if cls == "motorway" else 9)
        elif subtype == "rail" and cls in RAIL_CLASSES:
            if _flag_values(flags) & RAIL_EXCLUDE_FLAGS:
                continue
            kind = "rail"
            minzoom = _rail_minzoom(cls, name, km)
        elif subtype == "water":
            kind, minzoom = "ferry", 8
        else:
            continue
        if not prepared.intersects(geom):
            continue
        counts[kind] += 1
        props = {"kind": kind}
        if kind == "rail":
            props["transit"] = cls != "standard_gauge" or "caltrain" in name.lower() or "smart" in name.lower()
        feats.append(_feature(geom, props, minzoom))
    _write_geojsonl(config.BUILD / "context.geojsonl", feats)
    print(f"[process] context: {counts}")


# ---------------------------------------------------------------- labels

def build_labels(water: gpd.GeoDataFrame) -> None:
    loc = gpd.read_parquet(config.RAW / "localities.parquet")
    loc["name"] = loc["names"].apply(lambda n: n["primary"])

    def county_of(h) -> str | None:
        for chain in h if h is not None else []:
            for item in chain:
                if item.get("subtype") == "county":
                    return item.get("name")
        return None

    loc["county"] = loc["hierarchies"].apply(county_of)
    feats = []
    for name, county, tier in labels.CITIES:
        hit = loc[(loc["name"] == name) & (loc["county"] == county)]
        if len(hit) != 1:
            raise SystemExit(f"[process] label lookup for {name} ({county}) matched {len(hit)} localities")
        pt = hit.geometry.iloc[0]
        feats.append(_feature(pt, {"name": name, "kind": "city", "tier": tier, "source": "overture:" + hit["id"].iloc[0]}))

    raw = gpd.read_parquet(config.RAW / "water.parquet")
    raw["name"] = raw["names"].apply(lambda n: (n or {}).get("primary"))
    for name, tier, override in labels.WATER:
        if override is not None:
            pt = Point(override)
            source = "placed by hand"
        else:
            hit = raw[(raw["subtype"] == "physical") & (raw["name"] == name) & raw.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
            if hit.empty:
                raise SystemExit(f"[process] no named water polygon for {name}")
            geom = max(hit.geometry, key=lambda g: g.area)
            pt = shapely.ops.polylabel(geom if geom.geom_type == "Polygon" else max(geom.geoms, key=lambda g: g.area), tolerance=1e-4)
            source = "overture:" + hit["id"].iloc[0]
        feats.append(_feature(pt, {"name": name, "kind": "water", "tier": tier, "source": source}))
    config.DATA_OUT.mkdir(parents=True, exist_ok=True)
    out = config.DATA_OUT / "labels.geojson"
    out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, indent=1))
    print(f"[process] labels: {len(feats)}")


def main() -> None:
    config.BUILD.mkdir(parents=True, exist_ok=True)
    region, info = build_region()
    config.REGION_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.REGION_JSON.write_text(json.dumps(info, indent=2) + "\n")
    water = build_water()
    build_shoreline(water)
    build_labels(water)
    if (config.RAW / "segments.parquet").exists():
        build_context(region)
    # The buildings step needs the region polygon too.
    (config.BUILD / "region.wkb").write_bytes(shapely.to_wkb(region))


if __name__ == "__main__":
    main()
