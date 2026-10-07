"""The Portal (Downtown Rail Extension): tunnel alignment and two stations, traced from TJPA's 2026 map.

Source figure: TJPA, The Portal Monthly Status Report, September 2026 (Board item 11, Oct 8, 2026),
p. 4 (PDF p. 7), "Figure 1. The Portal Alignment and Major Components", drawing
MP-05b-AL-20260512. It postdates the 2026 scope changes (second CEQA addendum, March 12, 2026;
FTA concurrence Aug 26, 2026: high-speed rail platforms at Fourth and Townsend removed, train box
extension and intercity bus facility removed, tunnel stub box shortened by about 750 ft), so it
shows the current design. The 2018 Final SEIS/EIR figures show the superseded, longer design and
are not used.

Method:
- The figure is a raster map (1429 x 1104 px) in the PDF, extracted losslessly. It is drawn to
  scale (scale bar, north arrow) with the SoMa street grid square to the page.
- Georeference: 35 street intersections, each the crossing of the white street bands' centres
  (measured on rows and columns 12–30 px either side of the crossing, so the crossing itself and
  labels don't bias it), matched to the same intersections of DataSF street centrelines (Streets
  – Active and Retired, 3psu-pn9h; ODC PDDL) with trace.fit_similarity. Three intersections were
  dropped because a Muni line or a bridge is drawn over them (Fourth and King, Fourth and Berry,
  Fifth and Berry).
- Alignment: the figure's orange line (light orange tunnel, dark orange stations), opened to drop
  the thin trackwork ticks and closed to bridge the vent-structure symbols drawn over it, thinned
  to a one-pixel centreline (Zhang–Suen), taken end to end, simplified by 1.5 px.
- Stations: the centroid of each dark orange shape: the Fourth and Townsend Street Station box,
  and the Salesforce Transit Center train box (the existing two-level box, fitted out by the project).
- Trackwork to 16th Street: the figure draws it as ticks on the existing railyard tracks, and the
  SFCTA memo (Jan 2026) describes "track and systems modifications to the at-grade 4th and King Yard
  and trackwork to 16th Street". It is drawn on the U.S. DOT/BTS NTAD Caltrain main line (public
  domain), from the point nearest the tunnel's west end to where DataSF's 16th Street centreline
  crosses it (segment 'shared': existing track the project modifies).

What it isn't:
- A schematic drawn at 1 inch ≈ 1,000 ft: the orange band is about 37 m wide on the ground, so the
  centreline is good to several metres, not to the track. Not the engineered alignment.
- The tunnel's west end includes the U-wall and stub box approach (below grade, open at the top),
  drawn as tunnel. Yard trackwork inside Fourth and King is not drawn.
- The California High-Speed Rail Authority's 'DTX' polyline is not used (its terms forbid
  redistribution); it was compared locally as a check (see `check` in the output).

    uv run --directory pipeline python -m bam_pipeline.sites.lines_the_portal
"""

from __future__ import annotations

import urllib.parse
import urllib.request
from collections import deque

import cv2
import geopandas as gpd
import numpy as np
import shapely
from pypdf import PdfReader
from shapely.geometry import LineString, Point
from shapely.ops import substring

from .. import config, trace
from . import ntad_rail
from .lines import UTM, write_line_project

PROJECT_ID = "the-portal"
MSR = {
    "title": "TJPA, The Portal Monthly Status Report, September 2026",
    "url": "https://www.tjpa.org/media/40591?inline=",
    "sha256": "86597a5e5734f10df58e1069fce1466aacf65fa8d237c47d1c4ad91b4ddfc421",
    "page_index": 6,  # printed page 4
    "figure": "Figure 1, The Portal Alignment and Major Components (drawing MP-05b-AL-20260512)",
    "image_size": (1429, 1104),
}
SFCTA_MEMO = "https://www.sfcta.org/sites/default/files/2026-01/SFCTA_CAC_Item9_TJPAPortalProjectFiscalYear2026MEMO_2026-01-28.pdf"
STREETS = {
    "title": "DataSF Streets – Active and Retired (3psu-pn9h)",
    "landing": "https://data.sf.gov/d/3psu-pn9h",
    "api": "https://data.sf.gov/resource/3psu-pn9h.geojson",
    "license": "Open Data Commons Public Domain Dedication and License (PDDL) 1.0; City and County of San Francisco",
}
STREETS_CACHE = config.ROOT / "data" / "raw" / "lines" / "datasf_streets_soma.geojson"
BBOX = (37.762, -122.410, 37.798, -122.385)  # south, west, north, east

# Street-centre crossings in the figure (pixels, x right, y down), measured as described above.
CONTROLS = {
    ("07TH ST", "TOWNSEND ST"): (119.5, 671.5),
    ("07TH ST", "KING ST"): (119.5, 723.5),
    ("06TH ST", "BRANNAN ST"): (252.0, 580.0),
    ("05TH ST", "BRANNAN ST"): (385.75, 581.0),
    ("03RD ST", "BRANNAN ST"): (652.5, 582.0),
    ("03RD ST", "BRYANT ST"): (653.0, 490.0),
    ("03RD ST", "HARRISON ST"): (653.5, 396.5),
    ("03RD ST", "FOLSOM ST"): (653.75, 303.5),
    ("03RD ST", "BERRY ST"): (651.0, 773.5),
    ("02ND ST", "MISSION ST"): (787.0, 119.0),
    ("01ST ST", "FOLSOM ST"): (919.5, 305.0),
    ("01ST ST", "HOWARD ST"): (919.5, 211.5),
    ("01ST ST", "MISSION ST"): (920.0, 119.5),
    ("FREMONT ST", "HARRISON ST"): (972.0, 397.5),
    ("FREMONT ST", "FOLSOM ST"): (971.75, 305.0),
    ("FREMONT ST", "HOWARD ST"): (972.0, 212.0),
    ("FREMONT ST", "MISSION ST"): (972.5, 119.5),
    ("BEALE ST", "BRYANT ST"): (1024.0, 490.0),
    ("BEALE ST", "HARRISON ST"): (1023.5, 398.0),
    ("BEALE ST", "FOLSOM ST"): (1024.0, 305.0),
    ("BEALE ST", "HOWARD ST"): (1024.5, 212.0),
    ("MAIN ST", "HARRISON ST"): (1076.5, 398.0),
    ("MAIN ST", "FOLSOM ST"): (1076.5, 305.5),
    ("MAIN ST", "HOWARD ST"): (1077.5, 212.5),
    ("MAIN ST", "MISSION ST"): (1077.5, 120.5),
    ("SPEAR ST", "HARRISON ST"): (1128.25, 398.5),
    ("SPEAR ST", "FOLSOM ST"): (1128.5, 306.0),
    ("SPEAR ST", "HOWARD ST"): (1129.5, 212.5),
    ("SPEAR ST", "MISSION ST"): (1129.75, 120.5),
    ("NEW MONTGOMERY ST", "HOWARD ST"): (743.5, 210.5),
    ("HAWTHORNE ST", "FOLSOM ST"): (720.0, 303.75),
    ("HAWTHORNE ST", "HOWARD ST"): (720.5, 210.5),
    ("STEUART ST", "HOWARD ST"): (1183.0, 213.0),
    ("STEUART ST", "MISSION ST"): (1182.25, 120.5),
    ("ESSEX ST", "FOLSOM ST"): (849.5, 304.5),
}
LIGHT_ORANGE = (247, 142, 30)  # tunnel
DARK_ORANGE = (223, 94, 38)  # stations (Fourth and Townsend box, Salesforce Transit Center train box)
INSET = (0, 0, 612, 558)  # the regional locator map in the figure's top left
LEGEND = (1015, 700, 1429, 1104)
# The Authority's layer, downloaded for comparison only (not redistributed, not an input).
CHSRA_CHECK = config.ROOT / "data" / "raw" / "official" / "cahsr-sf-sj" / "hybrid-align-2025-03-04.geojson"


def _figure() -> np.ndarray:
    pdf = trace.fetch_document(MSR["url"], config.ROOT / "data" / "raw" / "docs" / "tjpa-portal-msr-2026-09.pdf", MSR["sha256"])
    for im in PdfReader(pdf).pages[MSR["page_index"]].images:
        rgb = np.asarray(im.image.convert("RGB"))
        if rgb.shape[1::-1] == MSR["image_size"]:
            return rgb
    raise SystemExit("The Portal: Figure 1 image not found in the status report")


def _streets() -> gpd.GeoDataFrame:
    if not STREETS_CACHE.exists():
        s, w, n, e = BBOX
        q = urllib.parse.urlencode({"$where": f"active='true' AND within_box(line, {n}, {w}, {s}, {e})", "$limit": 50000})
        with urllib.request.urlopen(f"{STREETS['api']}?{q}") as r:
            STREETS_CACHE.parent.mkdir(parents=True, exist_ok=True)
            STREETS_CACHE.write_bytes(r.read())
    return gpd.read_file(STREETS_CACHE).to_crs(UTM)


def _crossing(streets: gpd.GeoDataFrame, a: str, b: str) -> np.ndarray:
    g = streets[streets["streetname"] == a].geometry.union_all().intersection(
        streets[streets["streetname"] == b].geometry.union_all())
    pts = shapely.get_coordinates(g)
    if not len(pts):
        raise SystemExit(f"DataSF streets: {a} and {b} don't cross")
    return pts.mean(axis=0)


def _thin(mask: np.ndarray) -> np.ndarray:
    """Zhang–Suen thinning of a boolean mask to one-pixel lines."""
    img = np.pad(mask.astype(np.uint8), 1)
    while True:
        changed = False
        for step in (0, 1):
            p = img

            def at(dy, dx, p=p):  # neighbour at row + dy, column + dx
                return np.roll(np.roll(p, -dy, 0), -dx, 1)

            # P2..P9 clockwise from north
            p2, p3, p4, p5, p6, p7, p8, p9 = at(-1, 0), at(-1, 1), at(0, 1), at(1, 1), at(1, 0), at(1, -1), at(0, -1), at(-1, -1)
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            b = sum(seq[:8])
            a = sum(((seq[i] == 0) & (seq[i + 1] == 1)).astype(np.uint8) for i in range(8))
            c1 = p2 * p4 * p6 if step == 0 else p2 * p4 * p8
            c2 = p4 * p6 * p8 if step == 0 else p2 * p6 * p8
            kill = (p == 1) & (b >= 2) & (b <= 6) & (a == 1) & (c1 == 0) & (c2 == 0)
            if kill.any():
                img = img & ~kill
                changed = True
        if not changed:
            return img[1:-1, 1:-1].astype(bool)


def _longest_path(skel: np.ndarray) -> list[tuple[int, int]]:
    """The longest end-to-end path through a one-pixel skeleton (two BFS passes), as (x, y) pixels."""
    pix = set(zip(*np.nonzero(skel)))
    nb = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]

    def bfs(start):
        prev, q, last = {start: None}, deque([start]), start
        while q:
            u = q.popleft()
            last = u
            for dy, dx in nb:
                v = (u[0] + dy, u[1] + dx)
                if v in pix and v not in prev:
                    prev[v] = u
                    q.append(v)
        return last, prev

    far, _ = bfs(next(iter(pix)))
    end, prev = bfs(far)
    path, u = [], end
    while u is not None:
        path.append((u[1], u[0]))
        u = prev[u]
    return path


def _mask(rgb: np.ndarray, color, tol=40) -> np.ndarray:
    m = np.abs(rgb.astype(int) - np.array(color)).max(axis=2) <= tol
    for x0, y0, x1, y1 in (INSET, LEGEND):
        m[y0:y1, x0:x1] = False
    return m


def _check_against_chsra(tunnel_wgs: LineString) -> str:
    if not CHSRA_CHECK.exists():
        return "Authority layer not available locally; no comparison made."
    ref = gpd.read_file(CHSRA_CHECK)
    ref = ref[ref["SECTION"].str.startswith("DTX")].to_crs(UTM).geometry.union_all()
    ours = gpd.GeoSeries([tunnel_wgs], crs=4326).to_crs(UTM).iloc[0]

    def spread(a, b):
        d = sorted(b.distance(a.interpolate(t)) for t in np.arange(0, a.length, 20))
        return f"median {d[len(d) // 2]:.0f} m, 95th percentile {d[int(len(d) * 0.95)]:.0f} m, max {d[-1]:.0f} m"

    return (f"Compared locally (not published) with the Authority's 'DTX (Downtown Extension)' line "
            f"({ref.length / 1609.344:.2f} mi, which predates the 2026 changes), sampled every 20 m. Its points lie "
            f"{spread(ref, ours)} from ours; ours lie {spread(ours, ref)} from it (the far points are our approach "
            f"south along Seventh Street, which its line doesn't include).")


def main() -> None:
    rgb = _figure()
    streets = _streets()
    labels = [f"{a} & {b}" for a, b in CONTROLS]
    sim = trace.fit_similarity(list(CONTROLS.values()), [_crossing(streets, a, b) for a, b in CONTROLS], labels)
    rep = sim.report()
    print(f"fit: {len(CONTROLS)} controls, RMS {rep['rms_m']} m, max {max(c['residual_m'] for c in rep['controls'])} m, "
          f"{rep['scale_m_per_unit']} m/px, rotation {rep['rotation_deg']} deg")

    def world(g):
        return gpd.GeoSeries([sim.geometry(g)], crs=UTM).to_crs(4326).iloc[0]

    # Alignment centreline
    light, dark = _mask(rgb, LIGHT_ORANGE), _mask(rgb, DARK_ORANGE, tol=25)
    band = ((light | dark).astype(np.uint8)) * 255
    band = cv2.morphologyEx(band, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    band = cv2.morphologyEx(band, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    _, lab, stats, _ = cv2.connectedComponentsWithStats(band)
    band = lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    path = _longest_path(_thin(band))
    px = LineString(path).simplify(1.5)
    if px.coords[0][1] < px.coords[-1][1]:  # run west/south end -> Transit Center
        px = LineString(px.coords[::-1])

    # Stations: dark orange shapes
    shapes = trace.raster_color_polygons(rgb, DARK_ORANGE, tol=25, min_area_px=800, close_px=9)
    shapes = [s for s in shapes if not s.intersects(shapely.box(*INSET)) and not s.intersects(shapely.box(*LEGEND))]
    if len(shapes) != 2:
        raise SystemExit(f"The Portal: expected 2 station shapes, found {len(shapes)}")
    box_px = min(shapes, key=lambda s: s.centroid.y)  # the train box is the northern one
    fts_px = max(shapes, key=lambda s: s.centroid.y)

    # Split the alignment where it enters the train box
    inside = px.intersection(box_px.buffer(1))
    cut = min(px.project(Point(c)) for c in shapely.get_coordinates(inside))
    tunnel_px, box_line_px = substring(px, 0, cut), substring(px, cut, px.length)
    tunnel, box_line = world(tunnel_px), world(box_line_px)

    # Trackwork to 16th Street on the NTAD Caltrain main line
    arcs = ntad_rail.fetch_jpbx()
    main, _ = ntad_rail.route(arcs, Point(-122.394911, 37.776404), Point(-122.386647, 37.59988))
    main_utm = gpd.GeoSeries([main], crs=4326).to_crs(UTM).iloc[0]
    west_end = gpd.GeoSeries([Point(tunnel.coords[0])], crs=4326).to_crs(UTM).iloc[0]
    s16 = main_utm.intersection(streets[streets["streetname"] == "16TH ST"].geometry.union_all())
    a, b = main_utm.project(west_end), min(main_utm.project(Point(c)) for c in shapely.get_coordinates(s16))
    gap = main_utm.distance(west_end)
    track = gpd.GeoSeries([substring(main_utm, a, b)], crs=UTM).to_crs(4326).iloc[0]

    lens = gpd.GeoSeries([tunnel, box_line, track], crs=4326).to_crs(UTM).length / 1609.344
    print(f"tunnel {lens[0]:.2f} mi + train box {lens[1]:.2f} mi = {lens[0] + lens[1]:.2f} mi; "
          f"trackwork to 16th St {lens[2]:.2f} mi; total {lens.sum():.2f} mi; tunnel end is {gap:.0f} m from the NTAD main line")
    check = _check_against_chsra(LineString(list(tunnel.coords) + list(box_line.coords)[1:]))
    print(check)

    fig = f"traced: {MSR['title']}, p. 4, {MSR['figure']}"
    features = [
        {"geometry": tunnel, "properties": {
            "kind": "line", "segment": "tunnel", "name": "Tunnel, from the Caltrain tracks at Seventh Street to the Salesforce Transit Center",
            "source": f"{fig}; orange alignment, centreline (RMS {rep['rms_m']} m georeference)."}},
        {"geometry": box_line, "properties": {
            "kind": "line", "segment": "tunnel", "name": "Salesforce Transit Center train box (existing, fitted out)",
            "source": f"{fig}; dark orange train box, centreline."}},
        {"geometry": track, "properties": {
            "kind": "line", "segment": "shared", "name": "Trackwork to 16th Street (existing Caltrain tracks)",
            "source": (f"GIS: {ntad_rail.NTAD['title']}, Caltrain main line from the point nearest the tunnel's west end "
                       f"({gap:.0f} m away) to DataSF's 16th Street centreline; extent from the figure and the SFCTA memo "
                       f"(Jan 2026): 'trackwork to 16th Street'.")}},
        {"geometry": world(fts_px.centroid), "properties": {
            "kind": "station", "status": "new", "name": "Fourth and Townsend Street Station",
            "note": "New underground station under Townsend Street between Fourth and Fifth Streets (Caltrain).",
            "source": f"{fig}; centroid of the dark orange station box."}},
        {"geometry": world(box_px.centroid), "properties": {
            "kind": "station", "status": "rebuilt", "name": "Salesforce Transit Center",
            "note": "The existing two-level train box under the Transit Center, built in Phase 1 and fitted out by The Portal.",
            "source": f"{fig}; centroid of the dark orange train box."}},
    ]
    meta = {
        "source": f"{fig}, georeferenced on {len(CONTROLS)} DataSF street intersections",
        "sourceLabel": "TJPA, The Portal Monthly Status Report (Sept 2026), Figure 1",
        "sourceUrl": MSR["url"],
        "accuracy": "traced",
        "accuracyNote": (
            f"Approximate alignment traced from TJPA's map of the current (2026) design: {lens[0] + lens[1]:.2f} miles from the "
            f"tunnel's west end to the east end of the train box, which includes the below-grade approach at the west end "
            f"(U-wall and tunnel stub box), so it is longer than TJPA's '1.3-mile tunnel'; plus {lens[2]:.2f} miles of "
            f"trackwork on existing tracks to 16th Street ({lens.sum():.2f} miles in all; TJPA: 'total project length is 2.2 miles'). "
            f"Georeferenced on {len(CONTROLS)} street intersections (DataSF centrelines), RMS {rep['rms_m']} m; the map draws the line about "
            "37 m wide, so the centreline is good to several metres. Stations are the centres of the station shapes in the map."),
        "license": (f"Traced facts from a public TJPA report (the PDF is not redistributed). Georeference: {STREETS['license']}. "
                    f"Trackwork: {ntad_rail.NTAD['license']}"),
        "otherSources": [STREETS["landing"], ntad_rail.NTAD["url"], SFCTA_MEMO],
        "georeference": rep,
        "check": check,
    }
    write_line_project(PROJECT_ID, features, meta, corridor_m=40)


if __name__ == "__main__":
    main()
