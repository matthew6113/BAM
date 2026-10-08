"""U.S. DOT/BTS NTAD North American Rail Network Lines: fetch a railroad's arcs (Caltrain, SMART) and route along them.

The National Transportation Atlas Database rail network is "a work of the United States
government ... not protected by any U.S. copyrights" (public domain). Each arc carries its
owner (RROWNER1..3), its network class (NET: M main, S siding, Y yard, I industry, O other,
X out of service, A abandoned) and
the FRA node ids at either end (FRFRANODE, TOFRANODE), so a route between two places is a
shortest path over the arcs.

The ArcGIS service returns at most `maxRecordCount` features per request and says so only with
`exceededTransferLimit`, so the fetch pages with resultOffset until a short page.
"""

from __future__ import annotations

import heapq
import json
import urllib.parse
import urllib.request

import geopandas as gpd
from shapely.geometry import LineString, Point

from .. import config

UTM = "EPSG:26910"
NTAD = {
    "title": "U.S. DOT Bureau of Transportation Statistics, NTAD North American Rail Network Lines",
    "url": "https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_North_American_Rail_Network_Lines/FeatureServer/0",
    "license": "Public domain: 'a work of the United States government as defined in 17 U.S.C. § 101 ... available "
               "for unrestricted public use' (service copyright text).",
}
CACHE = config.ROOT / "data" / "raw" / "lines" / "ntad_rail_lines_jpbx.geojson"
OWNER = "JPBX"  # Peninsula Corridor Joint Powers Board (Caltrain) in the NTAD owner codes
PAGE = 200


def fetch_owner(owners: tuple[str, ...], cache_name: str) -> gpd.GeoDataFrame:
    """Every NTAD arc owned (RROWNER1..3) by any of `owners`, cached as data/raw/lines/<cache_name>."""
    cache = CACHE.parent / cache_name
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        codes = ", ".join(f"'{o}'" for o in owners)
        where = " OR ".join(f"RROWNER{i} IN ({codes})" for i in (1, 2, 3))
        feats, offset = [], 0
        while True:
            q = urllib.parse.urlencode({
                "where": where, "outFields": "*", "outSR": 4326, "f": "geojson",
                "orderByFields": "OBJECTID", "resultOffset": offset, "resultRecordCount": PAGE,
            })
            with urllib.request.urlopen(f"{NTAD['url']}/query?{q}") as r:
                page = json.load(r)["features"]
            feats += page
            if len(page) < PAGE:
                break
            offset += PAGE
        with urllib.request.urlopen(f"{NTAD['url']}/query?" + urllib.parse.urlencode(
                {"where": where, "returnCountOnly": "true", "f": "json"})) as r:
            count = json.load(r)["count"]
        if count != len(feats):
            raise SystemExit(f"NTAD: fetched {len(feats)} arcs but the service reports {count}")
        cache.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    return gpd.read_file(cache)


def fetch_jpbx() -> gpd.GeoDataFrame:
    """Every NTAD arc the Peninsula Corridor Joint Powers Board owns, cached in data/raw/lines/."""
    return fetch_owner((OWNER,), CACHE.name)


def route(arcs: gpd.GeoDataFrame, start: Point, end: Point, nets=("M", "S", "O")) -> tuple[LineString, list[int]]:
    """Shortest path (Dijkstra, by length) over the arcs, from the FRA node nearest `start` to the
    node nearest `end` (both WGS84 points). Returns the path in WGS84 and its FRAARCIDs."""
    utm = arcs[arcs["NET"].isin(nets)].to_crs(UTM)
    adj: dict[int, list] = {}
    pos: dict[int, tuple] = {}
    for _, a in utm.iterrows():
        c = list(a.geometry.coords)
        u, v, n = int(a["FRFRANODE"]), int(a["TOFRANODE"]), a.geometry.length
        pos[u], pos[v] = c[0], c[-1]
        adj.setdefault(u, []).append((v, n, c, int(a["FRAARCID"])))
        adj.setdefault(v, []).append((u, n, c[::-1], int(a["FRAARCID"])))
    s_utm, e_utm = (gpd.GeoSeries([p], crs=4326).to_crs(UTM).iloc[0] for p in (start, end))

    def nearest(p):
        return min(pos, key=lambda k: (pos[k][0] - p.x) ** 2 + (pos[k][1] - p.y) ** 2)

    s, e = nearest(s_utm), nearest(e_utm)
    dist, prev, pq = {s: 0.0}, {}, [(0.0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == e:
            break
        if d > dist[u]:
            continue
        for v, n, c, arc in adj[u]:
            if d + n < dist.get(v, float("inf")):
                dist[v], prev[v] = d + n, (u, c, arc)
                heapq.heappush(pq, (d + n, v))
    if e not in dist:
        raise SystemExit("NTAD: no path between the two points")
    parts, ids, n = [], [], e
    while n != s:
        u, c, arc = prev[n]
        parts.insert(0, c)
        ids.insert(0, arc)
        n = u
    coords = [xy for i, c in enumerate(parts) for xy in (c if i == 0 else c[1:])]
    line = gpd.GeoSeries([LineString(coords)], crs=UTM).to_crs(4326).iloc[0]
    return line, ids
