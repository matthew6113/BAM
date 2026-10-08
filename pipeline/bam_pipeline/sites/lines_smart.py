"""SMART's northern extensions: Windsor to Healdsburg (funded) and Healdsburg to Cloverdale (unfunded).

Two line projects on one railroad, split where SMART's own projects split:

- smart-healdsburg: from the Windsor platform, today's end of service, north to the Lytton Springs
  Road crossing at Healdsburg Avenue, the northern limit of the Healdsburg Extension Project
  ("milepost (MP) 72.00, located at the intersection of Lytton Springs Road and Healdsburg Avenue",
  CEQA addendum, Dec 2025, PDF p. 7). Stations: Windsor (existing) and Healdsburg (new). SMART
  reopened the Healdsburg site on Sept 16, 2026 (the historic Depot/Hudson site or a Downtown site
  on Vine Street); it is drawn at SMART's Depot point and named as under review (Matthew,
  2026-10-07).
- smart-cloverdale: from Lytton Springs Road to the 1st Street crossing in Cloverdale ("13.5 miles
  of rail and pathway, from Lytton Springs Road to 1st Street in Cloverdale", SMART Strategic Plan
  FY25-30, PDF p. 33). Stations: Geyserville (new; adopted Aug 19, 2026 at 255 Highway 128) and
  Cloverdale (new; SMART lists its site as to be determined).

All of this is SMART's out-of-service Northwestern Pacific track, to be rebuilt for passenger
service; no trains run on it, so it is segment 'new' ("nine miles of new track", SMART), not
'shared'.

Sources and method:
- Line: U.S. DOT/BTS NTAD North American Rail Network Lines (public domain), the arcs SMART owns
  (RROWNER 'SMRT' or 'SMAR'), in service or out of service (NET M, S, O, X; abandoned spurs, NET
  'A', excluded), shortest path from the FRA node nearest SMART's Sonoma County Airport station to
  the node nearest SMART's Cloverdale station point, carried on past it to the end of SMART's
  arcs there; then cut (see ntad_rail.py).
- Cut points: where the County of Sonoma's street centrelines (Streets_Public) for Lytton Springs
  Road and E 1st Street cross that line, and the Windsor station's point projected onto it.
- Stations: Windsor from the BTS National Transit Map stops layer (SMART's feed, stop 4251896,
  'SMART Windsor'; CC BY 3.0 US). Healdsburg and Cloverdale from SMART's own station layer on the
  County of Sonoma GIS server (SMARTPublic/SMART_Stations; copyright 'SMART', no licence stated).
  Geyserville from the County of Sonoma parcel SMART's Board adopted, APN 140-110-011 (255 Hwy
  128; the County's own centroid fields; CC BY-SA 3.0, credit 'County of Sonoma').
- Check: the drawn line against SMART's own track layer (SMARTPublic/SMART_Rail_Tracks), reported
  in each output's `check`.

    uv run --directory pipeline python -m bam_pipeline.sites.lines_smart
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import shapely
from pyproj import Geod
from shapely.geometry import LineString, MultiLineString, Point, shape
from shapely.ops import linemerge, substring

from .. import config
from . import ntad_rail
from .lines import UTM, write_line_project

RAW = config.ROOT / "data" / "raw" / "lines" / "smart"
SOCO = "https://socogis.sonomacounty.ca.gov/map/rest/services"
SMART_STATIONS = f"{SOCO}/SMARTPublic/SMART_Stations/FeatureServer/0"
SMART_TRACKS = f"{SOCO}/SMARTPublic/SMART_Rail_Tracks/FeatureServer/0"
STREETS = f"{SOCO}/BASEPublic/Streets_Public/FeatureServer/0"
PARCELS = f"{SOCO}/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0"
NTM_STOPS = "https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_National_Transit_Map_Stops/FeatureServer/0"
OWNERS = ("SMRT", "SMAR")  # SMART in the NTAD owner codes
NETS = ("M", "S", "O", "X")  # main, siding, other, out of service; abandoned spurs ('A') are left out
WINDSOR_STOP = "4251896"  # National Transit Map, SMART feed (ntd_id 90299): 'SMART Windsor'
GEYSERVILLE_APN = "140-110-011"  # SMART Board Res. 2026-26, Aug 19, 2026: 255 Hwy 128, Geyserville

ADDENDUM = "https://ceqanet.lci.ca.gov/2002112033/46/Attachment/xgdCcY"
STRATEGIC_PLAN = "https://www.sonomamarintrain.org/sites/default/files/Document%20Library/SMART_StrategicPlan_FY25-30.pdf"
STATION_REVIEW = "https://www.sonomamarintrain.org/healdsburgstationlocation"
GEYSERVILLE = "https://www.sonomamarintrain.org/geyserville"

LICENSES = {
    "ntad": ntad_rail.NTAD["license"],
    "streets": "County of Sonoma street centrelines (Streets_Public): 'You must source attribution “County of Sonoma”' (service copyright text).",
    "ntm": "BTS National Transit Map stops: Creative Commons Attribution 3.0 United States (service copyright text).",
    "smart": "SMART station points: SMART's layer on the County of Sonoma GIS server (copyright 'SMART'; no licence stated).",
    "parcels": "County of Sonoma parcels: CC BY-SA 3.0, credit 'County of Sonoma'.",
}


def _query(url: str, params: dict, cache_name: str) -> dict:
    """An ArcGIS REST query as GeoJSON, cached in data/raw/lines/smart/."""
    cache = RAW / cache_name
    if not cache.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        q = urllib.parse.urlencode({"outFields": "*", "outSR": 4326, "f": "geojson", **params})
        with urllib.request.urlopen(f"{url}/query?{q}") as r:
            data = json.load(r)
        if "error" in data:
            raise SystemExit(f"{url}: {data['error']}")
        cache.write_text(json.dumps(data))
    return json.loads(cache.read_text())


def _smart_station(name: str) -> Point:
    fc = _query(SMART_STATIONS, {"where": f"Name = '{name}'"}, f"smart_station_{name.split()[0].lower()}.geojson")
    assert len(fc["features"]) == 1, (name, len(fc["features"]))
    return shape(fc["features"][0]["geometry"])


def _windsor() -> Point:
    fc = _query(NTM_STOPS, {"where": f"stop_id = '{WINDSOR_STOP}' AND ntd_id = '90299'"}, "ntm_windsor.geojson")
    assert len(fc["features"]) == 1 and fc["features"][0]["properties"]["stop_name"] == "SMART Windsor"
    return shape(fc["features"][0]["geometry"])


def _geyserville() -> tuple[Point, dict]:
    fc = _query(PARCELS, {"where": f"APN = '{GEYSERVILLE_APN}'"}, "parcel_geyserville.geojson")
    assert len(fc["features"]) == 1
    p = fc["features"][0]["properties"]
    return Point(p["Long"], p["Lat"]), p


def _street(where: str, cache_name: str) -> MultiLineString:
    fc = _query(STREETS, {"where": where}, cache_name)
    return shapely.union_all([shape(f["geometry"]) for f in fc["features"]])


def _crossing(line_utm: LineString, street_wgs, label: str) -> float:
    """Distance along the line (m) where a street centreline crosses it; there must be exactly one crossing."""
    st = gpd.GeoSeries([street_wgs], crs=4326).to_crs(UTM).iloc[0]
    x = line_utm.intersection(st)
    pts = [g for g in getattr(x, "geoms", [x]) if not g.is_empty]
    assert len(pts) == 1, f"{label}: {len(pts)} crossings"
    return line_utm.project(pts[0].centroid)


def _check(line_wgs: LineString) -> str:
    """How far the drawn line runs from SMART's own track layer (a check only; that layer states no licence), every 5 m."""
    fc = _query(SMART_TRACKS, {"where": "1=1"}, "smart_tracks.geojson")
    tracks = gpd.GeoSeries([shape(f["geometry"]) for f in fc["features"]], crs=4326).to_crs(UTM).union_all()
    l = gpd.GeoSeries([line_wgs], crs=4326).to_crs(UTM).iloc[0]
    # Compare only where SMART's layer runs alongside: it stops short of 1st Street in Cloverdale.
    ends = [l.project(Point(c)) for g in getattr(tracks, "geoms", [tracks]) for c in (g.coords[0], g.coords[-1])]
    lo, hi = max(0.0, min(ends)), min(l.length, max(ends))
    d = np.array([tracks.distance(l.interpolate(s)) for s in np.arange(lo, hi, 5.0)])
    gap = l.length - hi + lo
    return (f"Against SMART's own track layer ({SMART_TRACKS}), sampled every 5 m: median {np.median(d):.0f} m, "
            f"95th percentile {np.percentile(d, 95):.0f} m, maximum {d.max():.0f} m apart"
            + (f"; that layer doesn't cover the last {gap:.0f} m of the line." if gap > 25 else "."))


def main() -> None:
    arcs = ntad_rail.fetch_owner(OWNERS, "ntad_rail_lines_smart.geojson")
    airport = _smart_station("Sonoma County - Airport Station")
    cloverdale = _smart_station("Cloverdale Station")
    healdsburg = _smart_station("Healdsburg Station")
    windsor = _windsor()
    geyserville, parcel = _geyserville()

    # Route from the Airport station to SMART's last node north of Cloverdale (past the 1st Street crossing).
    usable = arcs[arcs["NET"].isin(NETS)]
    north_end = max((Point(c) for g in usable.geometry for c in (g.coords[0], g.coords[-1])), key=lambda p: p.y)
    line, arc_ids = ntad_rail.route(arcs, airport, north_end, nets=NETS)
    l_utm = gpd.GeoSeries([line], crs=4326).to_crs(UTM).iloc[0]
    if isinstance(l_utm, MultiLineString):
        l_utm = linemerge(l_utm)

    at = {
        "windsor": l_utm.project(gpd.GeoSeries([windsor], crs=4326).to_crs(UTM).iloc[0]),
        "lytton": _crossing(l_utm, _street("Name = 'Lytton Springs' AND Type = 'Rd'", "street_lytton_springs.geojson"),
                            "Lytton Springs Rd"),
        "first": _crossing(l_utm, _street("PreDir = 'E' AND Name = '1st' AND Type = 'St' AND LeftCity = 'Cloverdale'",
                                          "street_e_1st_cloverdale.geojson"), "E 1st St, Cloverdale"),
    }
    assert at["windsor"] < at["lytton"] < at["first"], at
    pieces = {
        "smart-healdsburg": substring(l_utm, at["windsor"], at["lytton"]),
        "smart-cloverdale": substring(l_utm, at["lytton"], at["first"]),
    }
    arcs_utm = arcs[arcs["FRAARCID"].astype(int).isin([int(a) for a in arc_ids])].to_crs(UTM)

    def arcs_on(seg) -> list[int]:
        """The routed arcs that run along this piece for more than 10 m."""
        zone = seg.buffer(1.0)
        return sorted(int(a.FRAARCID) for a in arcs_utm.itertuples() if a.geometry.intersection(zone).length > 10)
    gis = (f"GIS: {ntad_rail.NTAD['title']}, SMART-owned track (RROWNER 'SMRT'/'SMAR', out of service north of "
           "Windsor), routed between FRA nodes")

    def dist(pt: Point, seg) -> float:
        return seg.distance(gpd.GeoSeries([pt], crs=4326).to_crs(UTM).iloc[0])

    for pid, seg in pieces.items():
        seg_wgs = gpd.GeoSeries([seg], crs=UTM).to_crs(4326).iloc[0]
        mi = Geod(ellps="WGS84").geometry_length(seg_wgs) / 1609.344  # on the ground, not the UTM grid
        if pid == "smart-healdsburg":
            name = "Windsor to Lytton Springs Road (Healdsburg extension)"
            cut = ("from the Windsor station (National Transit Map stop 4251896) projected onto the line, to where the "
                   "County of Sonoma's Lytton Springs Road centreline crosses it (the addendum's milepost 72.00)")
            stations = [
                (windsor, "Windsor", "existing", "Today's end of the line (service since May 2025).",
                 f"GIS: BTS National Transit Map stops, SMART feed, stop {WINDSOR_STOP} 'SMART Windsor' ({NTM_STOPS})."),
                (healdsburg, "Healdsburg (site under review)", "new",
                 "Drawn at the historic Depot/Hudson Street site in the approved project. On Sept 16, 2026 SMART "
                 "reopened the choice between it and a Downtown site on Vine Street, about 0.45 mile away; a "
                 "decision is aimed at the December 2026 Board meeting.",
                 f"GIS: SMART's station layer on the County of Sonoma server, 'Healdsburg Station' ({SMART_STATIONS})."),
            ]
            approval = "CEQA addendum adopted by SMART's Board Dec 17, 2025 (SCH 2002112033); funded (CTC baseline agreement)"
            src_extra = [ADDENDUM, STATION_REVIEW]
            label = "SMART Healdsburg extension"
        else:
            name = "Lytton Springs Road to Cloverdale (Cloverdale extension)"
            cut = ("from where the County of Sonoma's Lytton Springs Road centreline crosses the line to where its "
                   "E 1st Street centreline in Cloverdale crosses it (the Strategic Plan's limits)")
            stations = [
                (geyserville, "Geyserville", "new",
                 "Adopted by SMART's Board on Aug 19, 2026 (Resolution 2026-26) for 255 Highway 128.",
                 f"GIS: County of Sonoma parcel APN {GEYSERVILLE_APN} ({parcel['SitusFmt1']}, '{parcel['UseCDesc']}'), "
                 f"the County's centroid fields ({PARCELS})."),
                (cloverdale, "Cloverdale (site to be determined)", "new",
                 "SMART lists the Cloverdale station's location as to be determined; drawn at SMART's own GIS point.",
                 f"GIS: SMART's station layer on the County of Sonoma server, 'Cloverdale Station' ({SMART_STATIONS})."),
            ]
            approval = "Covered by SMART's 2006 EIR and 2008 SEIR (SCH 2002112033); Geyserville station adopted Aug 19, 2026; unfunded"
            src_extra = [STRATEGIC_PLAN, GEYSERVILLE]
            label = "SMART Cloverdale extension"

        for pt, sname, *_ in stations:
            print(f"{pid}: {sname} is {dist(pt, seg):.1f} m from the line")
        features = [{"geometry": seg_wgs, "properties": {
            "kind": "line", "segment": "new", "name": name, "approval": approval,
            "source": f"{gis}; cut {cut}."}}]
        for pt, sname, status, note, src in stations:
            features.append({"geometry": pt, "properties": {
                "kind": "station", "status": status, "name": sname, "note": note, "source": src}})

        check = _check(seg_wgs)
        print(f"{pid}: {mi:.2f} mi; {check}")
        station_lic = [LICENSES["ntm"], LICENSES["smart"]] if pid == "smart-healdsburg" else [LICENSES["parcels"], LICENSES["smart"]]
        meta = {
            "source": gis,
            "sourceLabel": "U.S. DOT/BTS National Transportation Atlas (rail network); County of Sonoma and SMART GIS",
            "sourceUrl": ntad_rail.NTAD["url"],
            "accuracy": "approximate",
            "accuracyNote": (
                f"Approximate alignment: the federal rail network's centreline for SMART's existing, out-of-service "
                f"track, {mi:.1f} miles as drawn, cut {cut}. One centreline, not SMART's engineered alignment. "
                f"{label} stations: " + "; ".join(s[1] for s in stations) + "."),
            "license": f"Line: {LICENSES['ntad']} Cut points: {LICENSES['streets']} Stations: " + " ".join(station_lic),
            "otherSources": src_extra + [STREETS, SMART_STATIONS, SMART_TRACKS],
            "fraArcIds": arcs_on(seg),
            "check": check,
        }
        write_line_project(pid, features, meta, corridor_m=60)


if __name__ == "__main__":
    main()
