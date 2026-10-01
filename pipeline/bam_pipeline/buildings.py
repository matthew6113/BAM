"""Select the buildings inside the nine counties and attach honest heights.

A building belongs to the region when the center of its bounding box falls inside a
county polygon (land or maritime, so Alcatraz and Treasure Island count). Heights are
kept only when they were mapped or measured. Microsoft ML height estimates are
dropped (config.DROP_HEIGHT_SOURCES), and those buildings stay flat on the map.

Output: data/build/buildings.fgb with one attribute, h (metres, 0.1 m precision).

    uv run --directory pipeline python -m bam_pipeline.buildings
"""

from __future__ import annotations

import json
import time

import geopandas as gpd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import shapely

from . import config


def _ml_height_mask(sources: pa.ListArray) -> np.ndarray:
    """True where the height came from a dropped source (e.g. Microsoft ML)."""
    flat = pc.list_flatten(sources)
    parents = pc.list_parent_indices(sources).to_numpy()
    prop = pc.struct_field(flat, "property")
    dataset = pc.struct_field(flat, "dataset")
    hit = pc.and_(
        pc.equal(prop, "/properties/height"),
        pc.is_in(dataset, value_set=pa.array(sorted(config.DROP_HEIGHT_SOURCES))),
    )
    hit = pc.fill_null(hit, False).to_numpy(zero_copy_only=False)
    mask = np.zeros(len(sources), dtype=bool)
    mask[parents[hit]] = True
    return mask


def main() -> None:
    t0 = time.time()
    region = shapely.from_wkb((config.BUILD / "region.wkb").read_bytes())
    shapely.prepare(region)
    pf = pq.ParquetFile(config.RAW / "buildings.parquet")
    parts = []
    stats = {"fetched": 0, "in_region": 0, "with_height": 0, "ml_height_dropped": 0}
    for batch in pf.iter_batches(batch_size=250_000, columns=["geometry", "bbox", "height", "sources"]):
        stats["fetched"] += batch.num_rows
        bbox = batch.column("bbox")
        cx = (pc.struct_field(bbox, "xmin").to_numpy() + pc.struct_field(bbox, "xmax").to_numpy()) / 2
        cy = (pc.struct_field(bbox, "ymin").to_numpy() + pc.struct_field(bbox, "ymax").to_numpy()) / 2
        inside = shapely.contains_xy(region, cx, cy)
        if not inside.any():
            continue
        height = batch.column("height").to_numpy(zero_copy_only=False).astype("float64")
        ml = _ml_height_mask(batch.column("sources"))
        stats["ml_height_dropped"] += int((ml & ~np.isnan(height) & inside).sum())
        height[ml] = np.nan
        height = np.round(height, 1)
        geoms = shapely.from_wkb(batch.column("geometry").to_numpy(zero_copy_only=False)[inside])
        h = height[inside]
        stats["in_region"] += int(inside.sum())
        stats["with_height"] += int((~np.isnan(h)).sum())
        parts.append(gpd.GeoDataFrame({"h": h}, geometry=geoms, crs=4326))
    gdf = gpd.GeoDataFrame(np.concatenate([p["h"].to_numpy() for p in parts]), columns=["h"],
                           geometry=np.concatenate([p.geometry.to_numpy() for p in parts]), crs=4326)
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    out = config.BUILD / "buildings.fgb"
    if out.exists():
        out.unlink()
    gdf.to_file(out, driver="FlatGeobuf", engine="pyogrio")
    stats["written"] = len(gdf)
    (config.BUILD / "buildings_stats.json").write_text(json.dumps(stats, indent=2))
    print(f"[buildings] {json.dumps(stats)} in {time.time() - t0:.0f}s, {out.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
