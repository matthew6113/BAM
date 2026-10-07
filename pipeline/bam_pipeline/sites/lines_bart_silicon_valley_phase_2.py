"""BART Silicon Valley Phase II: alignment and stations from VTA's own GIS.

VTA's ArcGIS Enterprise server publishes the project's track alignment and its station
and portal sites as public hosted feature services (gis.vta.org, which also serves VTA's
GTFS and other open data):

- Hosted/BSVII_Alignment_2022, layer 22 "BSVII_Alignment_org": seven track lines in State
  Plane California III feet, each tagged 'Above Ground' or 'Tunnel'. Both tracks are drawn
  separately (two in the tunnel, two at grade on each side) plus one tail track west of
  Santa Clara.
- Hosted/BSV_Phase_II_Stations, layer 0: the four new stations, the two tunnel portals and
  Newhall Yard as points (the layer behind vtabart.org's construction map).
- Hosted/BSV_Phase_II_Construction, layer 11 "BSV Phase I Stations": Berryessa/North San
  José, where the extension starts.

The older BART/BART MapServer (layers 31 Project boundary, 34 Stations, 35 Alignment,
44 Newhall Yard ROW) still lists its layers but their data sources are broken ("Layer not
found", extent NaN), so it is not used.

The map draws one line per running section, so each pair of tracks is reduced to its
centreline (the midpoint between them, every 5 m). Segment types follow VTA's layer:
'Tunnel' is the single-bore tunnel between the portals; 'Above Ground' (Santa Clara and
Newhall Yard in the west, the East Portal approach from the Phase I tail tracks in the
east) is drawn as new surface track. Newhall Yard itself, the portals and the project
boundary are not drawn: the line writer has no polygon kind, and the yard is a point here.

    uv run --directory pipeline python -m bam_pipeline.sites.lines_bart_silicon_valley_phase_2
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import LineString, Point, shape

from .. import config
from .lines import UTM, write_line_project

PROJECT = "bart-silicon-valley-phase-2"
RAW = config.ROOT / "data" / "raw" / "lines"
HOSTED = "https://gis.vta.org/gis/rest/services/Hosted"
ALIGNMENT = f"{HOSTED}/BSVII_Alignment_2022/FeatureServer/22"
STATIONS = f"{HOSTED}/BSV_Phase_II_Stations/FeatureServer/0"
PHASE1_STATIONS = f"{HOSTED}/BSV_Phase_II_Construction/FeatureServer/11"
MILE_M = 1609.344
FT_M = 0.3048

# Track pairs in the alignment layer (fid), west to east. fid 2 is a single tail track.
WEST_TAIL = 2
PAIRS = {"west": (1, 3), "tunnel": (6, 7), "east": (4, 5)}

# Station points: VTA's names (bsvii_names / name) -> how the map labels and draws them.
NEW_STATIONS = {
    "Santa Clara BART Station": ("Santa Clara", "At grade, next to the Santa Clara Caltrain station"),
    "Diridon BART Station": ("Diridon", "Underground"),
    "Downtown San José BART Station": ("Downtown San José", "Underground"),
    "28th Street/Little Portugal BART Station": ("28th Street/Little Portugal", "Underground"),
}

LICENSE = ("VTA public GIS service (gis.vta.org, ArcGIS Enterprise hosted feature services shared publicly); "
           "no license or terms of use stated on the service or its portal item.")


def fetch(url: str, name: str, where: str = "1=1") -> dict:
    """Query an ArcGIS layer as GeoJSON in WGS84, cached in data/raw/lines/."""
    out = RAW / f"{name}.geojson"
    if not out.exists():
        q = urllib.parse.urlencode({"where": where, "outFields": "*", "outSR": 4326, "f": "geojson"})
        with urllib.request.urlopen(f"{url}/query?{q}", timeout=120) as r:
            data = json.loads(r.read())
        if "features" not in data or not data["features"]:
            raise SystemExit(f"{url}: no features ({str(data)[:200]})")
        RAW.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data))
    return json.loads(out.read_text())


def to_utm(geoms) -> list:
    return list(gpd.GeoSeries(geoms, crs=4326).to_crs(UTM))


def to_wgs(geoms) -> list:
    return list(gpd.GeoSeries(geoms, crs=UTM).to_crs(4326))


def centreline(a: LineString, b: LineString, step: float = 5.0) -> tuple[LineString, float, float]:
    """Midline of two roughly parallel tracks (UTM). Returns it with the median and max spacing."""
    d = np.append(np.arange(0, a.length, step), a.length)
    pa = shapely.line_interpolate_point(a, d)
    pb = shapely.line_interpolate_point(b, shapely.line_locate_point(b, pa))
    ca, cb = shapely.get_coordinates(pa), shapely.get_coordinates(pb)
    gap = np.linalg.norm(ca - cb, axis=1)
    return LineString((ca + cb) / 2).simplify(0.5), float(np.median(gap)), float(gap.max())


def oriented(line: LineString, start: Point) -> LineString:
    """The line running away from `start` (whichever end is nearer)."""
    c = list(line.coords)
    return line if Point(c[0]).distance(start) <= Point(c[-1]).distance(start) else LineString(c[::-1])


def build() -> None:
    align = fetch(ALIGNMENT, "vta-bsvii-alignment-2022")
    stations = fetch(STATIONS, "vta-bsvii-stations")
    phase1 = fetch(PHASE1_STATIONS, "vta-bsv-phase1-stations")

    tracks = {f["properties"]["fid"]: f for f in align["features"]}
    utm = dict(zip(tracks, to_utm([shape(f["geometry"]) for f in tracks.values()])))
    kinds = {fid: f["properties"]["layer"] for fid, f in tracks.items()}
    for part, (a, b) in PAIRS.items():
        want = "Tunnel" if part == "tunnel" else "Above Ground"
        assert kinds[a] == kinds[b] == want, (part, kinds[a], kinds[b])
    tunnel_ft = [tracks[f]["properties"]["shape__len"] for f in PAIRS["tunnel"]]

    pieces, notes = {}, {}
    for part, (a, b) in PAIRS.items():
        pieces[part], med, mx = centreline(utm[a], utm[b])
        notes[part] = (med, mx)
    # Chain west to east: tail track, Santa Clara and Newhall, tunnel, East Portal approach.
    tail = utm[WEST_TAIL]
    if Point(tail.coords[0]).distance(Point(utm[PAIRS["west"][0]].coords[0])) < 1:
        tail = LineString(list(tail.coords)[::-1])  # make it end where the pair begins
    west = oriented(pieces["west"], Point(tail.coords[-1]))
    west = LineString(list(tail.coords) + list(west.coords)[1:])
    tunnel = oriented(pieces["tunnel"], Point(west.coords[-1]))
    east = oriented(pieces["east"], Point(tunnel.coords[-1]))
    for x, y, label in ((west, tunnel, "west/tunnel"), (tunnel, east, "tunnel/east")):
        gap = Point(x.coords[-1]).distance(Point(y.coords[0]))
        assert gap < 15, f"{label} pieces are {gap:.1f} m apart"

    # Station points, as published.
    st = []
    for f in stations["features"]:
        p = f["properties"]
        if p.get("bsvii_names") in NEW_STATIONS:
            name, note = NEW_STATIONS[p["bsvii_names"]]
            st.append((name, "new", note, shape(f["geometry"]),
                       f"GIS: VTA BSV Phase II Stations layer ({p['bsvii_names']})"))
    assert len(st) == 4, [s[0] for s in st]
    berryessa = [f for f in phase1["features"] if f["properties"].get("name") == "Berryessa"]
    assert len(berryessa) == 1
    st.append(("Berryessa/North San José", "existing", "Existing BART station (Phase I, opened 2020); the extension starts here",
               shape(berryessa[0]["geometry"]), "GIS: VTA BSV Phase I Stations layer (Berryessa)"))

    line_all = shapely.MultiLineString([west, tunnel, east])
    dists = {}
    for name, *_rest in st:
        pt = to_utm([_rest[2]])[0]
        dists[name] = line_all.distance(pt)

    src_align = "GIS: VTA BSVII_Alignment_2022 (Hosted feature service, layer 22), centreline of the two tracks"
    features = [
        {"geometry": to_wgs([west])[0], "properties": {
            "kind": "line", "segment": "new", "name": "Santa Clara and Newhall Yard (above ground)",
            "note": "At-grade and surface track from the tail track west of Santa Clara station to the West Portal",
            "source": src_align}},
        {"geometry": to_wgs([tunnel])[0], "properties": {
            "kind": "line", "segment": "tunnel", "name": "Single-bore tunnel",
            "note": "About five miles between the West Portal and the East Portal",
            "source": src_align}},
        {"geometry": to_wgs([east])[0], "properties": {
            "kind": "line", "segment": "new", "name": "East Portal approach (above ground)",
            "note": "Surface track from the Phase I tail tracks south of Berryessa to the East Portal",
            "source": src_align}},
    ]
    for name, status, note, geom, source in st:
        features.append({"geometry": geom, "properties": {
            "kind": "station", "status": status, "name": name, "note": note, "source": source}})

    km = {k: v.length / 1000 for k, v in (("west", west), ("tunnel", tunnel), ("east", east))}
    total_mi = sum(km.values()) * 1000 / MILE_M
    tunnel_mi = km["tunnel"] * 1000 / MILE_M
    # Official length is measured from Berryessa/North San José to the Santa Clara station.
    by_name = {s[0]: s[3] for s in st}
    b_utm, sc_utm = to_utm([by_name["Berryessa/North San José"], by_name["Santa Clara"]])
    chain = LineString(list(west.coords) + list(tunnel.coords)[1:] + list(east.coords)[1:])
    sc_at = chain.project(sc_utm)
    berry_gap = Point(chain.coords[-1]).distance(b_utm)
    station_span_mi = (chain.length - sc_at + berry_gap) / MILE_M
    for name, off in dists.items():
        print(f"  station {name}: {off:.0f} m from the centreline")
    print(f"  track spacing (median/max m): " + ", ".join(f"{k} {m:.1f}/{x:.1f}" for k, (m, x) in notes.items()))
    print(f"  drawn: {total_mi:.2f} mi in all, tunnel {tunnel_mi:.2f} mi (VTA tracks {tunnel_ft[0]/5280:.2f} and "
          f"{tunnel_ft[1]/5280:.2f} mi); Berryessa to Santa Clara station {station_span_mi:.2f} mi")

    write_line_project(PROJECT, features, {
        "source": "GIS: VTA, BSVII_Alignment_2022 (track alignment) and BSV Phase II Stations, "
                  "public hosted feature services on gis.vta.org",
        "sourceLabel": "VTA GIS alignment",
        "sourceUrl": ALIGNMENT,
        "accuracy": "official",
        "accuracyNote": (
            f"Alignment from VTA's published GIS layer of the project's tracks (dated 2022 in its name), drawn as the "
            f"centreline between the two tracks. {total_mi:.1f} miles as drawn including the tail track west of Santa "
            f"Clara ({station_span_mi:.1f} miles from Berryessa/North San José to the Santa Clara station; VTA and FTA "
            f"describe about 6 miles); the tunnel section is {tunnel_mi:.1f} miles (FTA: about five). Station points "
            f"are VTA's published station sites, not platform outlines. The design may shift as VTA re-baselines the "
            f"project; Newhall Yard and the portals are not drawn."),
        "license": LICENSE,
        "lengthMiles": round(total_mi, 2),
        "tunnelMiles": round(tunnel_mi, 2),
        "berryessaToSantaClaraMiles": round(station_span_mi, 2),
        "layers": {"alignment": ALIGNMENT, "stations": STATIONS, "phase1Stations": PHASE1_STATIONS},
    })


if __name__ == "__main__":
    build()
