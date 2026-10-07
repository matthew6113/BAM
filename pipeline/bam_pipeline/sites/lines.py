"""Shared writer for line projects (rail lines, shoreline defenses): alignment and stations.

A line project is drawn as its alignment, not a site. Each tracing module builds its features
in WGS84 and calls write_line_project(), which writes:

- data/lines/<id>.geojson: the alignment (kind 'line', LineString or MultiLineString) and the
  stations (kind 'station', Point). Every feature carries a `source` saying where its geometry
  came from ("GIS: ..." or "traced: ...").
- data/boundaries/<id>.geojson: a corridor around the alignment (kind 'site'), so the map can
  hit-test, frame and filter the project like any other. It is not a property line.

Line `segment` values (how the map draws each piece):
- 'new': new surface or elevated track or structure
- 'tunnel': new underground running
- 'shared': existing track the project upgrades and shares (drawn lighter)

Station `status` values: 'new', 'rebuilt' (existing station rebuilt or expanded), 'existing'.
"""

from __future__ import annotations

import json

import geopandas as gpd
from shapely.geometry import mapping

from .. import config

UTM = "EPSG:26910"
LINES = config.ROOT / "data" / "lines"
BOUNDARIES = config.ROOT / "data" / "boundaries"
SEGMENTS = {"new", "tunnel", "shared"}
STATION_STATUS = {"new", "rebuilt", "existing"}
REQUIRED_META = {"source", "sourceLabel", "sourceUrl", "accuracy", "accuracyNote", "license"}


def _round(obj, nd=6):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    return obj


def write_line_project(project: str, features: list[dict], meta: dict, corridor_m: float = 60) -> None:
    """features: [{'geometry': shapely geometry in WGS84, 'properties': {...}}].

    meta needs source, sourceLabel, sourceUrl (must be in the project's `sources`), accuracy
    ('official' | 'traced' | 'approximate'), accuracyNote and license, as boundary files do.
    """
    missing = REQUIRED_META - meta.keys()
    if missing:
        raise ValueError(f"{project}: meta is missing {sorted(missing)}")
    if meta["accuracy"] not in ("official", "traced", "approximate"):
        raise ValueError(f"{project}: bad accuracy {meta['accuracy']!r}")
    for f in features:
        p, g = f["properties"], f["geometry"]
        if p.get("kind") == "line":
            assert g.geom_type in ("LineString", "MultiLineString"), (project, p)
            assert p.get("segment") in SEGMENTS, (project, p)
        elif p.get("kind") == "station":
            assert g.geom_type == "Point", (project, p)
            assert p.get("status") in STATION_STATUS, (project, p)
        else:
            raise ValueError(f"{project}: unknown kind in {p}")
        assert str(p.get("name", "")).strip() and str(p.get("source", "")).strip(), (project, p)

    gdf = gpd.GeoDataFrame([f["properties"] for f in features], geometry=[f["geometry"] for f in features], crs=4326)
    utm = gdf.to_crs(UTM)
    lengths = utm[utm["kind"] == "line"].geometry.length
    km = float(lengths.sum()) / 1000

    LINES.mkdir(parents=True, exist_ok=True)
    out = {
        "type": "FeatureCollection",
        "properties": {"project": project, **meta, "lengthKm": round(km, 2)},
        "features": [
            {"type": "Feature", "properties": f["properties"], "geometry": _round(mapping(f["geometry"]))}
            for f in features
        ],
    }
    (LINES / f"{project}.geojson").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")

    corridor = utm.geometry.buffer(corridor_m).union_all().simplify(5)
    site = gpd.GeoSeries([corridor], crs=UTM).to_crs(4326).iloc[0]
    boundary = {
        "type": "FeatureCollection",
        "properties": {
            "project": project, **meta, "corridor": True, "corridorMetres": corridor_m,
            "accuracyNote": f"{meta['accuracyNote']} The site shown is a {corridor_m:g} m corridor around the alignment, for selecting it on the map; it is not a property line.",
        },
        "features": [{"type": "Feature", "properties": {"kind": "site", "name": "Alignment corridor"}, "geometry": _round(mapping(site))}],
    }
    (BOUNDARIES / f"{project}.geojson").write_text(json.dumps(boundary, indent=1, ensure_ascii=False) + "\n")
    print(f"{project}: {len(features)} features, {km:.2f} km of line")
