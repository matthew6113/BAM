"""Valley Link Phase 1A: alignment and three stations, traced from the Authority's figures.

What Phase 1A is (Authority Board packet, June 10, 2026, item 4.c.2, AB 1171 Initial Project
Report, PDF pp. 29-31): "approximately 11 miles of new passenger rail along I-580 to connect the
existing BART rail system at Dublin/Pleasanton to the existing ACE rail system at Vasco Road in
Livermore and includes a third station at Isabel Avenue". "Similar to the previously approved
Phase 1 project, Phase 1A would be constructed within the I-580 median from the
Dublin/Pleasanton BART Station to just east of the First Street overcrossing in Livermore.
However, unlike the Phase 1 project, just east of the First Street overcrossing, Phase 1A would
branch south from the median of I-580 via a flyover crossing eastbound I-580 as shown in
Figure 4. The alignment then continues on a viaduct, passing over Las Positas Boulevard, the
Union Pacific Railroad (UPRR) spur, and the proposed Livermore OMF, before returning to grade
south of the proposed Livermore OMF parallel to the existing UPRR tracks. From there, the Phase
1A alignment would extend approximately one mile before terminating with a tail track east of
the Vasco Road Station."

Sources and method, west to east:
- Dublin/Pleasanton Station approach: Draft SEIR (April 2024, CEQAnet SCH 2018092027, document
  6), Chapter 2, Figure 2-13 (an aerial photo with the proposed alignment and the elevated
  platform south of eastbound I-580). Georeferenced to OpenStreetMap building footprints.
- I-580 median, Dublin/Pleasanton to First Street: Draft SEIR Figures 2-4, 2-5 and 2-6
  (Proposed Project 1-3 of 9), which draw the "Median Widening" for the rail line as a yellow
  line. Each figure is fitted to OpenStreetMap streets (trimmed ICP from two I-580 crossings).
  The 2026 report says Phase 1A keeps the Phase 1 median alignment to First Street (quoted above).
- Between the station and the median the figures don't draw the alignment (the SEIR says it runs
  "via an elevated viaduct over the eastbound I-580 freeway lanes to the median of I-580"); the
  two traced ends are joined with a straight line, marked as constructed.
- First Street to Vasco Road: the June 2026 report's Figure 4 (an aerial photo with the Phase 1A
  alignment, the Vasco Road Station platform and the OMF). Georeferenced to building footprints.
- Stations: the centre of each platform in the figures (Dublin/Pleasanton, Figure 2-13; Isabel,
  Figure 2-14; Vasco Road, Figure 4). Checked against BART's GTFS stop for Dublin/Pleasanton and
  Caltrans' California Transit Stops point for the Vasco Road ACE station.

Phase 1B (Southfront Road to Mountain House, unfunded) and the superseded 2021 route are not drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.lines_valley_link
"""

from __future__ import annotations

import csv
import io
import json
import urllib.parse
import urllib.request
import zipfile

import cv2
import numpy as np
import shapely
from shapely.geometry import LineString, Point
from shapely.ops import substring

from .. import config, trace
from . import line_georef as lg
from . import traced_boundaries as tb
from .lines import write_line_project

PROJECT_ID = "valley-link"
DOCS = config.ROOT / "data" / "raw" / "docs"
RAW = config.ROOT / "data" / "raw" / "lines"

IPR = {
    "title": "Tri-Valley-San Joaquin Valley Regional Rail Authority, Board packet, June 10, 2026 "
             "(item 4.c.2, AB 1171 Initial Project Report)",
    "url": "https://www.valleylinkrail.com/_files/ugd/8f09e7_9cca9a978bb14766a336566c3710ef3a.pdf",
    "sha256": "a4bc4aa74047ac9939ee5da1cb71f0e9fbcf8d838d81b9925af2c208b197bee2",
    "file": "valley-link-board-packet-2026-06-10.pdf",
}
SEIR = {
    "title": "Valley Link Rail Project Draft Subsequent EIR, Chapter 2, Project Description (April 2024, SCH 2018092027)",
    "url": "https://ceqanet.lci.ca.gov/2018092027/6/Attachment/ZPbOAG",
    "page": "https://ceqanet.lci.ca.gov/2018092027/6",
    "sha256": "9f9b4897798f1b31c8586693557aaa33df8668d46ca7369a37a36e46b00b93e5",
    "file": "valley-link-dseir-2024-ch2.pdf",
}
BART_GTFS = "https://www.bart.gov/dev/schedules/google_transit.zip"
CA_TRANSIT_STOPS = "https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/CA_Transit_Stops/FeatureServer/0"

# Figure 4 (IPR PDF p. 31): an aerial photo, 1390 x 470 px. Rough start: the First Street
# overcrossing (the red "replace existing First Street overcrossing" box) and about 2.6 m/px.
FIG4 = {"page_index": 30, "size": (1390, 470), "pdf_page": 31,
        "name": "Figure 4, Valley Link Phase 1A Connection From I-580 to Vasco Road Station",
        "start": ((217, 122), "First Street x I-580"), "scale": 2.6,
        "exclude": [(1240, 0, 1390, 100)]}  # the DRAFT stamp and north arrow
# SEIR figures (1-based PDF pages 9-11, 18, 19). Figures 2-4 to 2-6 are street maps (2088 x 1373 px)
# with two hand-located I-580 crossings each to start the fit; 2-13 and 2-14 are aerial photos.
MEDIAN_FIGS = {
    "2-4": {"page_index": 8, "controls": [((861, 665), "Hacienda Drive"), ((1374, 670), "Santa Rita Road")]},
    "2-5": {"page_index": 9, "controls": [((295, 745), "Fallon Road"), ((1290, 770), "Airway Boulevard")]},
    "2-6": {"page_index": 10, "controls": [((920, 785), "North Livermore Avenue"), ((2000, 728), "First Street")]},
}
FIG_2_13 = {"page_index": 17, "size": (1539, 1015), "name": "Figure 2-13, Dublin/Pleasanton Station",
            "start": ((665, 430), "the existing BART platform (BART GTFS stop L30-1)"), "scale": 0.387,
            "band": (540, 700), "exclude": [(0, 900, 330, 1015), (980, 905, 1539, 1015)]}
FIG_2_14 = {"page_index": 18, "size": (1539, 1015), "name": "Figure 2-14, Isabel Station",
            "start": ((500, 233), "Isabel Avenue x I-580"), "scale": 0.651,
            "band": (180, 300), "exclude": [(0, 900, 330, 1015), (960, 905, 1539, 1015)]}
# The median figures share one map layout and scale (2,000-ft bar, same frame), so scale is held
# at Figure 2-4's free fit and only rotation and shift are refined on 2-5 and 2-6, whose open
# hillsides have few streets.
STREET_CLASSES = ["motorway", "trunk", "primary", "secondary", "tertiary", "residential", "unclassified"]
BBOX = (-121.925, 37.675, -121.69, 37.725)


def _docs():
    ipr = trace.fetch_document(IPR["url"], DOCS / IPR["file"], IPR["sha256"])
    seir = trace.fetch_document(SEIR["url"], DOCS / SEIR["file"], SEIR["sha256"])
    return ipr, seir


def _i580_crossings() -> dict[str, tuple[float, float]]:
    """Where named streets cross I-580: midpoint of the crossings of the two carriageways
    (OpenStreetMap motorway segments, via Overture)."""
    g = tb.streets("valley_link", BBOX)
    mw = g[g["class"] == "motorway"].geometry.union_all()
    out = {}
    names = {"Hacienda Drive": ["Hacienda Drive"], "Santa Rita Road": ["Santa Rita Road"],
             "Fallon Road": ["Fallon Road", "El Charro Road"], "Airway Boulevard": ["Airway Boulevard"],
             "North Livermore Avenue": ["North Livermore Avenue"], "First Street": ["First Street"],
             "Isabel Avenue": ["Isabel Avenue"]}
    for key, ns in names.items():
        road = g[g["name"].isin(ns)].geometry.union_all()
        pts = shapely.get_coordinates(road.intersection(mw))
        if not len(pts):
            raise SystemExit(f"{key} doesn't cross I-580 in OpenStreetMap")
        out[key] = tuple(pts.mean(axis=0))
    return out


def _street_mask(rgb: np.ndarray) -> np.ndarray:
    a = rgb.astype(int)
    g = a.mean(2).astype(np.float32)
    sat = a.max(2) - a.min(2)
    m = (sat < 14) & (g > 150) & (g < 215) & (np.abs(g - cv2.GaussianBlur(g, (0, 0), 3)) > 3)
    h, w = m.shape
    m[int(h * 0.86):, :] = False  # legend
    m[:int(h * 0.27), :int(w * 0.29)] = False  # locator inset
    return m


def trace_median(seir, roads) -> tuple[LineString, dict]:
    """The 'Median Widening' line of SEIR Figures 2-4 to 2-6, in UTM, west to east."""
    xing = _i580_crossings()
    pieces, reports, scale = [], {}, None
    for name, f in MEDIAN_FIGS.items():
        rgb = lg.pdf_image(seir, f["page_index"], (2088, 1373))
        h, w = rgb.shape[:2]
        m = _street_mask(rgb)
        (p0, n0), (p1, n1) = f["controls"]
        if scale is None:
            init = trace.fit_similarity([p0, p1], [xing[n0], xing[n1]])
            sim, _ = lg.coarse_roads(m, roads, init, scale_range=0.0, rot_range=2.0, rot_step=0.25, pad=60)
        else:
            init = lg.anchored(p0, xing[n0], scale, rot)
            sim, _ = lg.coarse_roads(m, roads, init, scale_range=0.0, rot_range=0.0, pad=60)
        ys, xs = np.nonzero(m)
        sel = np.random.default_rng(0).choice(len(xs), min(20000, len(xs)), replace=False)
        pts = np.c_[xs[sel], ys[sel]].astype(float)
        target = roads[roads.intersects(lg.footprint(sim, w, h))].geometry.union_all()
        if scale is None:
            fit, d = tb.icp(pts, [target], np.zeros(len(pts), int), sim, 0.5, iterations=60)
            scale, rot = fit.scale, float(np.degrees(fit.rotation))
        else:
            fit, d = tb.icp(pts, [target], np.zeros(len(pts), int), sim, 0.5, iterations=60, scale=scale)
        rep = tb.icp_report(fit, d, 0.5, "street casings vs OpenStreetMap streets")
        rep["start"] = f"{n0} and {n1} crossings of I-580 (hand-located in the figure)"
        reports[f"Figure {name}"] = rep
        a = rgb.astype(int)
        yellow = (a[..., 0] > 200) & (a[..., 1] > 200) & (a[..., 2] < 90)
        yellow[int(h * 0.86):, :] = False
        pieces.append(fit.geometry(lg.column_centreline(yellow, smooth=9)))
        print(f"[valley-link] Figure {name}: {rep['scale_m_per_unit']} m/px, rot {rep['rotation_deg']} deg, "
              f"trimmed RMS {rep['rms_m']} m, median {rep['median_m']} m")
    # Merge: 25 m bins along the easting, median northing (the figures overlap at their edges).
    pts = np.vstack([np.asarray(p.coords) for p in pieces])
    bins = np.floor(pts[:, 0] / 25)
    xy = [(pts[bins == b, 0].mean(), np.median(pts[bins == b, 1])) for b in np.unique(bins)]
    line = LineString(xy).simplify(2)
    # Agreement where neighbouring figures overlap
    gaps = []
    for a_, b_ in zip(pieces, pieces[1:]):
        x = np.arange(max(a_.bounds[0], b_.bounds[0]), min(a_.bounds[2], b_.bounds[2]), 10)
        ya = np.interp(x, *np.asarray(a_.coords).T)
        yb = np.interp(x, *np.asarray(b_.coords).T)
        gaps.append(round(float(np.median(np.abs(ya - yb))), 1))
    reports["overlap_agreement_m"] = gaps
    return line, reports


def _station_figure(seir, f, buildings, anchor_utm):
    rgb = lg.pdf_image(seir, f["page_index"], f["size"])
    init = lg.anchored(f["start"][0], anchor_utm, f["scale"], 1.5)
    sim, rep = lg.register_buildings(rgb, buildings, init, exclude=f["exclude"], pad=150, tile=200, search=25)
    rep["start"] = f"{f['start'][1]}, {f['scale']} m/px (scale bar)"
    a = rgb.astype(int)
    band = np.zeros(a.shape[:2], bool)
    band[f["band"][0]:f["band"][1], :] = True
    blue = (a[..., 2] > a[..., 0] + 70) & (a[..., 2] > 120) & band
    platform = blue & (a[..., 1] < 110)  # dark blue platform fill vs the lighter alignment lines
    plat = lg.largest_blob(cv2.morphologyEx(platform.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)))
    return rgb, sim, rep, blue, plat


def trace_dublin(seir, buildings, bart_utm):
    rgb, sim, rep, blue, plat = _station_figure(seir, FIG_2_13, buildings, bart_utm)
    line = sim.geometry(lg.column_centreline(blue, min_pixels=2, midrange=True, smooth=41).simplify(1.0))
    station = sim.geometry(Point(lg.blob_centroid(plat)))
    print(f"[valley-link] Figure 2-13: RMS {rep['rms_m']} m over {rep['tiles_used']} tiles")
    return line, station, rep


def trace_isabel(seir, buildings, anchor):
    rgb, sim, rep, blue, plat = _station_figure(seir, FIG_2_14, buildings, anchor)
    station = sim.geometry(Point(lg.blob_centroid(plat)))
    print(f"[valley-link] Figure 2-14: RMS {rep['rms_m']} m over {rep['tiles_used']} tiles")
    return station, rep


def trace_fig4(ipr, buildings, first_st):
    rgb = lg.pdf_image(ipr, FIG4["page_index"], FIG4["size"])
    init = lg.anchored(FIG4["start"][0], first_st, FIG4["scale"], 1.5)
    sim, rep = lg.register_buildings(rgb, buildings, init, exclude=FIG4["exclude"], pad=60, tile=120, search=10)
    rep["start"] = f"{FIG4['start'][1]}, {FIG4['scale']} m/px"
    a = rgb.astype(int)
    blue = (a[..., 2] > a[..., 0] + 70) & (a[..., 2] > 120)
    green = (a[..., 1] > 120) & (a[..., 1] > a[..., 0] + 60) & (a[..., 1] > a[..., 2] + 50)  # Vasco Road platform
    red = (a[..., 0] > 150) & (a[..., 1] < 80) & (a[..., 2] < 80)  # First Street overcrossing box drawn over the line
    # The alignment is a darker blue than the station parking block, whose outline is still caught:
    # find the block (an opening of all blue), and clear its outline above the line along its south edge.
    block = cv2.morphologyEx(blue.astype(np.uint8), cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
    bx, by, bw, bh = cv2.boundingRect(block)
    dark = blue & (a[..., 2] < 155)
    dark[by - 4:by + bh - 8, bx - 4:bx + bw + 4] = False  # the green platform carries the line past the block
    line_mask = dark | green | red
    for x0, y0, x1, y1 in FIG4["exclude"] + [(455, 0, 505, 25)]:  # stamp, north arrow, I-580 shield
        line_mask[y0:y1, x0:x1] = False
    m = cv2.morphologyEx(line_mask.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    px, gaps = lg.chain_paths(lg.component_paths(lg._thin(m.astype(bool)), min_px=10), max_gap=40)
    px = px.simplify(1.0)
    rep["line_gaps_bridged_px"] = [round(g, 1) for g in gaps]
    plat = lg.largest_blob(green)
    station = sim.geometry(Point(lg.blob_centroid(plat)))
    print(f"[valley-link] Figure 4: RMS {rep['rms_m']} m over {rep['tiles_used']} tiles; {px.length * sim.scale:.0f} m of line")
    return sim.geometry(px), station, rep


def _bart_stop() -> Point:
    cache = config.ROOT / "data" / "raw" / "official" / "valley-link" / "bart_gtfs.zip"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(BART_GTFS) as r:
            cache.write_bytes(r.read())
    with zipfile.ZipFile(cache) as z:
        rows = csv.DictReader(io.TextIOWrapper(z.open("stops.txt"), "utf-8-sig"))
        s = next(r for r in rows if r["stop_id"] == "L30-1")
    return Point(float(s["stop_lon"]), float(s["stop_lat"]))


def _ace_stop() -> Point:
    cache = RAW / "caltrans_transit_stops_vas.geojson"
    if not cache.exists():
        q = urllib.parse.urlencode({"where": "stop_id='VAS'", "outFields": "stop_id,stop_name,agency", "outSR": 4326, "f": "geojson"})
        with urllib.request.urlopen(f"{CA_TRANSIT_STOPS}/query?{q}") as r:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(r.read())
    return Point(json.loads(cache.read_text())["features"][0]["geometry"]["coordinates"])


def main() -> None:
    ipr, seir = _docs()
    g = tb.streets("valley_link", BBOX)
    roads = g[g["class"].isin(STREET_CLASSES)]
    buildings = tb.buildings("valley_link", BBOX)
    xing = _i580_crossings()
    bart, ace = _bart_stop(), _ace_stop()
    bart_u, ace_u = lg.wgs_to_utm(bart), lg.wgs_to_utm(ace)

    median, med_reps = trace_median(seir, roads)
    dublin_line, dublin_st, rep_213 = trace_dublin(seir, buildings, (bart_u.x, bart_u.y))
    isabel_st, rep_214 = trace_isabel(seir, buildings, xing["Isabel Avenue"])
    conn, vasco_st, rep_4 = trace_fig4(ipr, buildings, xing["First Street"])

    # Median: from where the yellow line starts to where Figure 4's line starts (just west of First St).
    a = median.project(Point(conn.coords[0]))
    median_cut = substring(median, 0, a)
    junction_gap = Point(conn.coords[0]).distance(median.interpolate(a))
    # Station approach: Figure 2-13's line runs off the figure's east edge still south of the
    # eastbound lanes; join its east end to the start of the median line.
    link = LineString([dublin_line.coords[-1], median_cut.coords[0]])
    print(f"[valley-link] link from the station approach to the median: {link.length:.0f} m; "
          f"Figure 4 starts {junction_gap:.1f} m from the traced median line")

    pieces = {
        "dublin": dublin_line, "link": link, "median": median_cut,
        "connection": LineString([median_cut.coords[-1], *conn.coords[1:]]),
    }
    lens = {k: v.length for k, v in pieces.items()}
    total_mi = sum(lens.values()) / 1609.344
    print(f"[valley-link] total {total_mi:.2f} mi ({', '.join(f'{k} {v / 1609.344:.2f}' for k, v in lens.items())})")

    d_bart = dublin_st.distance(bart_u)
    d_ace = vasco_st.distance(ace_u)
    print(f"[valley-link] Dublin/Pleasanton platform {d_bart:.0f} m from the BART stop; Vasco Road platform {d_ace:.0f} m from the ACE stop")

    w = lg.utm_to_wgs
    seir_fig = f"traced: {SEIR['title']}"
    ipr_fig = f"traced: {IPR['title']}, PDF p. {FIG4['pdf_page']}, {FIG4['name']}"
    features = [
        {"geometry": w(pieces["dublin"]), "properties": {
            "kind": "line", "segment": "new", "name": "Dublin/Pleasanton Station and approach, elevated south of eastbound I-580",
            "source": f"{seir_fig}, PDF p. 18, {FIG_2_13['name']}: 'Proposed Rail Alignment', centre of the two tracks "
                      f"(RMS {rep_213['rms_m']} m georeference)."}},
        {"geometry": w(pieces["link"]), "properties": {
            "kind": "line", "segment": "new", "name": "Viaduct over eastbound I-580 into the median",
            "source": ("constructed: a straight join between the end of the alignment in Figure 2-13 and the start of the "
                       "median widening in Figure 2-4, which the SEIR describes as 'an elevated viaduct over the eastbound "
                       "I-580 freeway lanes to the median of I-580' (p. 2-6). Not drawn in the figures.")}},
        {"geometry": w(pieces["median"]), "properties": {
            "kind": "line", "segment": "new", "name": "In the I-580 median, Dublin/Pleasanton to First Street",
            "source": (f"{seir_fig}, PDF pp. 9-11, Figures 2-4 to 2-6 (Proposed Project 1-3 of 9): the 'Median Widening' line "
                       "(trimmed RMS " + ", ".join(f"{r['rms_m']}" for k, r in med_reps.items() if k.startswith("Figure")) +
                       " m). The 2026 report: 'Phase 1A would be constructed within the I-580 median from the "
                       "Dublin/Pleasanton BART Station to just east of the First Street overcrossing'.")}},
        {"geometry": w(pieces["connection"]), "properties": {
            "kind": "line", "segment": "new",
            "name": "First Street to Vasco Road: flyover, Southfront and Mid-town aerial viaducts, then at grade beside the UPRR tracks",
            "source": f"{ipr_fig}: the blue Valley Link alignment to the tail tracks east of Vasco Road (RMS {rep_4['rms_m']} m georeference).",
            "note": ("Runs parallel to the existing Union Pacific tracks, not on them: 'returning to grade south of the proposed "
                     "Livermore OMF parallel to the existing UPRR tracks' (2026 report, PDF p. 30).")}},
        {"geometry": w(dublin_st), "properties": {
            "kind": "station", "status": "new", "name": "Dublin/Pleasanton",
            "note": (f"A new double-track aerial Valley Link platform south of eastbound I-580, beside the existing BART station "
                     f"(its centre is {d_bart:.0f} m from BART's platform stop). Transfers are through the BART station concourse."),
            "source": f"{seir_fig}, PDF p. 18, {FIG_2_13['name']}: centre of the 'Elevated Valley Link Platform'."}},
        {"geometry": w(isabel_st), "properties": {
            "kind": "station", "status": "new", "name": "Isabel",
            "note": "A new at-grade platform in the I-580 median east of Isabel Avenue, with parking south of the freeway.",
            "source": f"{seir_fig}, PDF p. 19, {FIG_2_14['name']}: centre of the 'At-Grade Valley Link Platform' (RMS {rep_214['rms_m']} m georeference)."}},
        {"geometry": w(vasco_st), "properties": {
            "kind": "station", "status": "new", "name": "Vasco Road",
            "note": (f"New Valley Link platforms beside the existing Vasco Road ACE platform, for cross-platform transfers "
                     f"(the figure's platform centre is {d_ace:.0f} m from Caltrans' ACE stop point)."),
            "source": f"{ipr_fig}: centre of the green 'Valley Link Vasco Road Station Platform'."}},
    ]
    rms = [rep_213["rms_m"], rep_214["rms_m"], rep_4["rms_m"]] + [r["rms_m"] for k, r in med_reps.items() if k.startswith("Figure")]
    meta = {
        "source": (f"{IPR['title']}, Figure 4 (First Street to Vasco Road); {SEIR['title']}, Figures 2-4 to 2-6 (I-580 median), "
                   "2-13 and 2-14 (stations); georeferenced to OpenStreetMap streets and building footprints"),
        "sourceLabel": "Valley Link Board packet (June 10, 2026), Figure 4, and Draft SEIR (2024) figures",
        "sourceUrl": IPR["url"],
        "accuracy": "traced",
        "accuracyNote": (
            f"Approximate alignment traced from the Authority's figures: {total_mi:.1f} miles as drawn (the Authority: 'approximately "
            f"11 miles'). Figure 4 of the June 2026 report gives the current Phase 1A route from First Street to Vasco Road; "
            f"the I-580 median and the stations come from the 2024 Draft SEIR, whose median alignment the 2026 report keeps. "
            f"The figures are fitted to OpenStreetMap with RMS {min(rms):.1f}-{max(rms):.1f} m, and the lines are drawn tens of "
            f"metres wide, so the centreline is good to about 10-20 m, not to the track. The {lens['link']:.0f}-m join from the "
            "Dublin/Pleasanton platform into the median is not drawn in the figures and is a straight line. Phase 1B "
            "(Southfront Road to Mountain House, unfunded) is not drawn."),
        "license": (f"Traced facts from public documents of the Tri-Valley-San Joaquin Valley Regional Rail Authority (PDFs not "
                    f"redistributed). Georeference: {tb.OSM_LICENSE}. Station checks: BART GTFS (bart.gov developer terms); "
                    "Caltrans California Transit Stops (public, no license stated)."),
        "otherSources": [SEIR["page"], SEIR["url"], BART_GTFS, CA_TRANSIT_STOPS],
        "georeference": {"Figure 4": rep_4, "Figure 2-13": rep_213, "Figure 2-14": rep_214, **med_reps},
        "check": (f"Dublin/Pleasanton platform centre {d_bart:.0f} m from BART GTFS stop L30-1; Vasco Road platform centre "
                  f"{d_ace:.0f} m from Caltrans' ACE stop VAS; Figure 4's line starts {junction_gap:.1f} m from the traced median line."),
    }
    write_line_project(PROJECT_ID, features, meta, corridor_m=60)


if __name__ == "__main__":
    main()
