"""California High-Speed Rail, San Francisco to San Jose: the shared Caltrain corridor and three stations.

What is drawn:
- The line: the existing Caltrain corridor from the San Francisco (Fourth and King) station to
  San José Diridon, which high-speed trains would share ("blended"; Final EIR/EIS Alternative A).
  segment 'shared'. It is split where the two approvals meet:
  - Fourth and King to Scott Boulevard in Santa Clara: approved by the Authority's Board on
    Aug 17, 2022 (Resolution HSRA 22-20) and selected in this section's Record of Decision
    (Oct 14, 2022): "This ROD approves the portion of Alternative A between the 4th and King
    Street Station in San Francisco and Scott Boulevard in Santa Clara".
  - Scott Boulevard to San José Diridon: "approved by the Authority Board of Directors as part of
    the San Jose to Merced Project Section approvals" (same ROD, p. 1).
  The split point is the ROD's own coordinate for the section's south limit, "Scott Boulevard
  (37.363521°, -121.959536°)" (ROD Appendix, Biological Opinion section 2.3 "Action Area", PDF
  p. 250; the ROD says "All GPS locations provided are approximate"), snapped to the line.
  The Final EIR/EIS section continues past Diridon to West Alma Avenue (48.9 miles of existing
  track); the record draws it to Diridon, the section's last station.
- Stations (status 'rebuilt': existing Caltrain stations the project modifies for high-speed rail;
  the ROD approves "modified Caltrain stations for HSR at the 4th and King Street and Millbrae
  Stations", and Diridon's was approved with the San Jose to Merced section): Caltrain's parent
  station points from Caltrain's GTFS feed.

Sources and method:
- Line geometry: U.S. DOT/BTS NTAD North American Rail Network Lines (public domain), arcs owned
  by the Peninsula Corridor Joint Powers Board (RROWNER 'JPBX'), main line, sidings and 'other'
  arcs (yards excluded), shortest path between the FRA nodes nearest the two stations
  (see ntad_rail.py).
- Stations: Caltrain GTFS (https://www.caltrain.com/developer-resources; the feed file is hosted
  by Trillium for Caltrain), parent stations 'san_francisco', 'place_MLBR', 'sj_diridon'. The
  Peninsula Corridor JPB licence grants "non-exclusive, limited and revocable rights to use,
  reproduce, and redistribute" the data; no Caltrain logo or system map is used.

What it isn't:
- Not the Authority's own alignment: the Authority's ArcGIS layers (HSR_Statewide_Alignment,
  Alignment_Hybrid_Feb_8_2024, NORCAL_LAYERS) say they "are not to be redistributed without the
  express approval from California High Speed Rail Authority", so they are not used. They were
  compared locally, as a check only (see `check` in the output report).
- One centreline for a two-to-four-track corridor, not the track HSR would use. The 17.4 miles
  of track modifications, the East Brisbane light maintenance facility, crossings and fencing
  are not drawn (no official geometry that may be published was found).

    uv run --directory pipeline python -m bam_pipeline.sites.lines_cahsr_sf_sj
"""

from __future__ import annotations

import csv
import io
import shutil
import urllib.request
import zipfile

import geopandas as gpd
from shapely.geometry import LineString, Point
from shapely.ops import substring

from .. import config
from . import ntad_rail
from .lines import UTM, write_line_project

PROJECT_ID = "cahsr-sf-sj"
ROD = {
    "title": "San Francisco to San Jose Project Section, Record of Decision (Oct 14, 2022)",
    "url": "https://hsr.ca.gov/wp-content/uploads/2022/10/FJ-Final-ROD-Combined-A11Y.pdf",
}
SCOTT_BLVD = (-121.959536, 37.363521)  # ROD, Biological Opinion sec. 2.3, PDF p. 250 ("approximate")
CALTRAIN_GTFS = {
    "title": "Caltrain GTFS",
    "landing": "https://www.caltrain.com/developer-resources",
    "url": "https://data.trilliumtransit.com/gtfs/caltrain-ca-us/caltrain-ca-us.zip",
    "license": "Peninsula Corridor Joint Powers Board developer licence: non-exclusive, limited and revocable "
               "rights to use, reproduce and redistribute the data (https://www.caltrain.com/developer-resources).",
}
GTFS_CACHE = config.ROOT / "data" / "raw" / "lines" / "gtfs" / "caltrain.zip"
STATIONS = [
    # (GTFS parent stop_id, name on the map, what the record and ROD say about it)
    ("san_francisco", "Fourth and King",
     ("Interim San Francisco terminus until The Portal reaches the Salesforce Transit Center; existing Caltrain "
      "station modified for high-speed rail (ROD p. 1).")),
    ("place_MLBR", "Millbrae",
     "Existing Caltrain and BART station modified for high-speed rail, for SFO (ROD p. 1)."),
    ("sj_diridon", "San José Diridon",
     "Existing station; its high-speed rail work was approved with the San Jose to Merced section (ROD p. 1)."),
]
# The Authority's layer, downloaded for comparison only (not redistributed, not an input).
CHSRA_CHECK = config.ROOT / "data" / "raw" / "official" / "cahsr-sf-sj" / "hybrid-align-2025-03-04.geojson"


def _gtfs_stations() -> dict[str, tuple[float, float]]:
    if not GTFS_CACHE.exists():
        GTFS_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(CALTRAIN_GTFS["url"]) as r, open(GTFS_CACHE, "wb") as f:
            shutil.copyfileobj(r, f)
    with zipfile.ZipFile(GTFS_CACHE) as z:
        rows = list(csv.DictReader(io.TextIOWrapper(z.open("stops.txt"), encoding="utf-8-sig")))
        info = next(csv.DictReader(io.TextIOWrapper(z.open("feed_info.txt"), encoding="utf-8-sig")), {})
    print(f"Caltrain GTFS feed_version {info.get('feed_version')!r}, {info.get('feed_start_date')}–{info.get('feed_end_date')}")
    return {r["stop_id"]: (float(r["stop_lon"]), float(r["stop_lat"])) for r in rows}


def _check_against_chsra(line_wgs: LineString) -> str:
    """Hausdorff-style distances from our line to the Authority's (local comparison only)."""
    if not CHSRA_CHECK.exists():
        return "Authority layer not available locally; no comparison made."
    ref = gpd.read_file(CHSRA_CHECK).to_crs(UTM)
    ref = ref[ref["SECTION"] == "San Francisco to San Jose"].geometry.union_all()
    ours = gpd.GeoSeries([line_wgs], crs=4326).to_crs(UTM).iloc[0]
    pts = [ours.interpolate(d) for d in range(0, int(ours.length), 100)]
    d = sorted(ref.distance(p) for p in pts)
    return (f"Compared locally (not published) with the Authority's Alignment_Hybrid layer, section 'San Francisco "
            f"to San Jose': median "
            f"{d[len(d) // 2]:.0f} m, 95th percentile {d[int(len(d) * 0.95)]:.0f} m, max {d[-1]:.0f} m apart, "
            f"sampled every 100 m.")


def main() -> None:
    stops = _gtfs_stations()
    pts = {sid: Point(stops[sid]) for sid, _, _ in STATIONS}
    arcs = ntad_rail.fetch_jpbx()
    line, arc_ids = ntad_rail.route(arcs, pts["san_francisco"], pts["sj_diridon"])

    utm = gpd.GeoSeries([line, Point(SCOTT_BLVD)], crs=4326).to_crs(UTM)
    l_utm, scott = utm.iloc[0], utm.iloc[1]
    at = l_utm.project(scott)
    print(f"Scott Blvd (ROD point) is {l_utm.distance(scott):.0f} m from the line, {at / 1609.344:.2f} mi from Fourth and King")
    north, south = substring(l_utm, 0, at), substring(l_utm, at, l_utm.length)
    north, south = gpd.GeoSeries([north, south], crs=UTM).to_crs(4326)

    gis = (f"GIS: {ntad_rail.NTAD['title']}, Caltrain-owned (JPBX) main line, routed between the FRA nodes "
           f"nearest Fourth and King and San José Diridon ({len(arc_ids)} arcs)")
    features = [
        {"geometry": north, "properties": {
            "kind": "line", "segment": "shared", "name": "Fourth and King to Scott Boulevard (shared Caltrain corridor)",
            "approval": "San Francisco to San Jose section: Board, Aug 17, 2022 (Res. HSRA 22-20); Record of Decision, Oct 14, 2022",
            "source": f"{gis}; split at the ROD's Scott Boulevard point (Biological Opinion sec. 2.3, PDF p. 250)."}},
        {"geometry": south, "properties": {
            "kind": "line", "segment": "shared", "name": "Scott Boulevard to San José Diridon (shared Caltrain corridor)",
            "approval": "Approved with the San Jose to Merced section (Board, Apr 28, 2022), per this section's ROD p. 1",
            "source": f"{gis}; split at the ROD's Scott Boulevard point (Biological Opinion sec. 2.3, PDF p. 250)."}},
    ]
    for sid, name, note in STATIONS:
        features.append({"geometry": pts[sid], "properties": {
            "kind": "station", "status": "rebuilt", "name": name, "note": note,
            "source": f"GIS: Caltrain GTFS, parent station '{sid}' ({CALTRAIN_GTFS['landing']})."}})

    whole = gpd.GeoSeries([line], crs=4326).to_crs(UTM).iloc[0]
    mi = whole.length / 1609.344
    check = _check_against_chsra(line)
    print(f"{mi:.1f} mi Fourth and King to Diridon; {check}")
    meta = {
        "source": gis,
        "sourceLabel": "U.S. DOT/BTS National Transportation Atlas (rail network); Caltrain GTFS stations",
        "sourceUrl": ntad_rail.NTAD["url"],
        "accuracy": "approximate",
        "accuracyNote": (
            f"Approximate alignment (shared Caltrain corridor): the federal rail network's centreline for Caltrain's "
            f"existing tracks, {mi:.1f} miles from Fourth and King to San José Diridon. High-speed trains would share "
            "these tracks (Final EIR/EIS Alternative A, about 49 miles to West Alma Avenue); the line is not the "
            "Authority's engineered alignment and shows one centreline for a two-to-four-track corridor. "
            "It is split at Scott Boulevard, the ROD's south limit for this section (ROD point, 'approximate'). "
            "Stations are Caltrain's GTFS station points."),
        "license": f"Line: {ntad_rail.NTAD['license']} Stations: {CALTRAIN_GTFS['license']}",
        "otherSources": [ROD["url"], CALTRAIN_GTFS["landing"]],
        "fraArcIds": arc_ids,
        "check": check,
    }
    write_line_project(PROJECT_ID, features, meta, corridor_m=60)


if __name__ == "__main__":
    main()
