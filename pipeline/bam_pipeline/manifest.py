"""Record what the pipeline read and wrote, so rebuilds can be compared.

Writes data/manifest.json (committed): the Overture release, each raw extract's row
count, size and SHA-256, the building stats, and each output's size and SHA-256.

    uv run --directory pipeline python -m bam_pipeline.manifest
"""

from __future__ import annotations

import hashlib
import json
import subprocess

import pyarrow.parquet as pq

from . import config


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    inputs = {}
    for p in sorted(config.RAW.glob("*.parquet")):
        inputs[p.name] = {
            "rows": pq.ParquetFile(p).metadata.num_rows,
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
        }
    outputs = {}
    for p in sorted(config.TILES_OUT.glob("*.pmtiles")):
        outputs[f"tiles/{p.name}"] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
    labels = config.DATA_OUT / "labels.geojson"
    if labels.exists():
        outputs["data/labels.geojson"] = {"bytes": labels.stat().st_size, "sha256": sha256(labels)}
    stats_path = config.BUILD / "buildings_stats.json"
    tippecanoe = subprocess.run(["tippecanoe", "--version"], capture_output=True, text=True)
    manifest = {
        "overtureRelease": config.OVERTURE_RELEASE,
        "fetchBbox": list(config.FETCH_BBOX),
        "counties": config.COUNTIES,
        "tippecanoe": (tippecanoe.stdout + tippecanoe.stderr).strip(),
        "googleFontsCommit": config.GOOGLE_FONTS_COMMIT,
        "buildings": json.loads(stats_path.read_text()) if stats_path.exists() else None,
        "inputs": inputs,
        "outputs": outputs,
    }
    config.MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"[manifest] {config.MANIFEST}")


if __name__ == "__main__":
    main()
