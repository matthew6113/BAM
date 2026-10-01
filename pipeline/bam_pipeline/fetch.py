"""Download the Overture extracts for the Bay Area into data/raw/.

Reads Overture's GeoParquet straight from S3 with pyarrow. Only the needed columns
are read, and the bbox filter lets pyarrow skip row groups outside the region. Each
extract is cached: delete the file to fetch it again.

    uv run --project pipeline python -m bam_pipeline.fetch
"""

from __future__ import annotations

import os
import sys
import time

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq

from . import config

# name -> (theme, type, columns, extra filter)
EXTRACTS: dict[str, tuple[str, str, list[str], pc.Expression | None]] = {
    "counties": (
        "divisions",
        "division_area",
        ["id", "geometry", "bbox", "subtype", "class", "names", "region", "country", "is_territorial"],
        (pc.field("subtype") == "county") & (pc.field("region") == "US-CA"),
    ),
    "localities": (
        "divisions",
        "division",
        ["id", "geometry", "bbox", "subtype", "names", "population", "hierarchies", "local_type"],
        pc.field("subtype") == "locality",
    ),
    "water": (
        "base",
        "water",
        ["id", "geometry", "bbox", "subtype", "class", "names", "is_salt", "is_intermittent"],
        None,
    ),
    "salt_ponds": (
        # Most South Bay salt ponds are tagged as land use in OpenStreetMap, not as water.
        "base",
        "land_use",
        ["id", "geometry", "bbox", "subtype", "class", "names"],
        pc.field("class") == "salt_pond",
    ),
    "segments": (
        "transportation",
        "segment",
        ["id", "geometry", "bbox", "subtype", "class", "names", "rail_flags"],
        (pc.field("subtype") == "rail")
        | (pc.field("subtype") == "water")
        | ((pc.field("subtype") == "road") & pc.field("class").isin(["motorway", "trunk"])),
    ),
    "buildings": (
        "buildings",
        "building",
        ["id", "geometry", "bbox", "height", "sources"],
        None,
    ),
}


def _filesystem() -> pafs.S3FileSystem:
    # Overture is a public bucket. Some environments inject placeholder AWS
    # credentials, which S3 rejects, so drop them and read anonymously.
    for key in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
        os.environ.pop(key, None)
    return pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)


def _bbox_filter(bbox: tuple[float, float, float, float]) -> pc.Expression:
    xmin, ymin, xmax, ymax = bbox
    return (
        (pc.field("bbox", "xmin") < xmax)
        & (pc.field("bbox", "xmax") > xmin)
        & (pc.field("bbox", "ymin") < ymax)
        & (pc.field("bbox", "ymax") > ymin)
    )


def fetch_one(name: str, force: bool = False) -> None:
    theme, type_, columns, extra = EXTRACTS[name]
    out = config.RAW / f"{name}.parquet"
    if out.exists() and not force:
        print(f"[fetch] {name}: cached ({out.stat().st_size / 1e6:.1f} MB)")
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme={theme}/type={type_}/"
    t0 = time.time()
    dataset = ds.dataset(path, filesystem=_filesystem(), format="parquet")
    filt = _bbox_filter(config.FETCH_BBOX)
    if extra is not None:
        filt = filt & extra
    scanner = dataset.scanner(columns=columns, filter=filt, batch_readahead=8, fragment_readahead=4)
    tmp = out.with_suffix(".parquet.tmp")
    rows = 0
    writer: pq.ParquetWriter | None = None
    try:
        for batch in scanner.to_batches():
            if batch.num_rows == 0:
                continue
            if writer is None:
                writer = pq.ParquetWriter(tmp, batch.schema, compression="zstd")
            writer.write_table(pa.Table.from_batches([batch]))
            rows += batch.num_rows
    finally:
        if writer is not None:
            writer.close()
    if rows == 0:
        sys.exit(f"[fetch] {name}: no rows returned; check the release and bbox")
    tmp.rename(out)
    print(f"[fetch] {name}: {rows:,} rows, {out.stat().st_size / 1e6:.1f} MB in {time.time() - t0:.0f}s")


def main(argv: list[str]) -> None:
    names = [a for a in argv if not a.startswith("-")] or list(EXTRACTS)
    force = "--force" in argv
    for name in names:
        fetch_one(name, force=force)


if __name__ == "__main__":
    main(sys.argv[1:])
