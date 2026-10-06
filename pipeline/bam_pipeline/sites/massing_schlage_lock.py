"""Schlage Lock (Visitacion Valley Zone 1): development parcels drawn to their height limits, plus
the rehabilitated historic office building.

Sources:
- Parcel shapes: the Development Agreement's final exhibits (SF Planning file dated 08-22-14,
  Ord. 149-14), Exhibit L, Visitacion Valley Schlage Lock Infrastructure Plan (May 28, 2014),
  Figure 1.1 "Conceptual Parcelization Plan" (PDF p. 86). The figure is CAD vector line work:
  the property line (1.68-pt strokes, dashed) and the proposed parcel lines (1.44-pt black
  strokes) are read straight from the PDF, dash gaps and short line ends are joined, and the
  lines are polygonised into parcels.
- Height limits: DataSF "Zoning Map – Height and Bulk Districts" (h9wh-cg3m, Public Domain U.S.
  Government): the 57-X, 68-X, 76-X and 86-X districts mapped on the site with the Schlage Lock
  rezoning (Ord. 150-14, 2014). The zoning layer is drawn block by block (streets included), so it
  is clipped to the parcels.
- Height check: Visitacion Valley/Schlage Lock Design for Development (D4D, the June 16, 2014
  version adopted with the Board's approvals), Figure 2-3 "Height Map" (printed p. 39, PDF p. 43):
  "Maximum building heights for the Schlage Lock site are established in the Height Zone Diagram,
  shown in Fig. 2-3" (p. 40). Its blocks carry the same numbers as the parcels, and the zoning
  heights inside each parcel must be ones the figure gives that block (D4D_HEIGHTS); the run stops
  otherwise. Both documents are 2014 and agree, so neither is superseded.
- Built: the Old Office Building (2201 Bayshore Blvd), footprint from OpenStreetMap via Overture;
  DBI permit 201507010504 (rehabilitation, 4 stories, complete 2022-09-16).

Georeferencing: the figure's property line is fitted to the Project Site's assessor parcels
(data/boundaries/schlage-lock.geojson, from DA Exhibit B and DataSF acdm-wktn) by trimmed ICP, a
similarity started from the figure's scale bar and north arrow. Every traced parcel's area is then
checked against the acreage printed on the figure (all within 0.02 acres). The Planning
Department's revised Phase 1 approval (Sept 17, 2018), Exhibit A (Tentative Map, Proposed
Parcelization Plan, C3), prints the same parcel numbers and acreages, so the 2014 layout still
stands.

What this is and isn't:
- Each parcel is drawn whole to its height limit, not as a building design, so the massing is
  labelled illustrative. The D4D's setbacks (upper-floor setbacks of 15%, 10% on Parcels 10-12),
  massing breaks and the 10-ft corner allowance at Leland Ave and Bayshore Blvd aren't drawn.
- Not drawn: Parcel 13 (the Old Office Building's lot, which keeps the building; the building
  itself is drawn), Parcel 14 south of Sunnydale Ave (no height in the D4D's figure and not one of
  Exhibit F's development parcels), Visitacion Park (Parcel A), Leland Park/Greenway (Parcel D),
  the streets and alleys (Parcels B, C, E, F) and the railroad parcels (G, UPRR, JPB).
- Stage: every parcel is "entitled". The two apartment permits on Parcels 1-3 (201912189909 and
  201912189911) are still only filed, and the 2016 grading permit was never completed.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_schlage_lock
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import LineString, Point, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "schlage-lock"
UTM = tb.UTM
RAW = config.ROOT / "data" / "raw" / "massing"
BBOX = (-122.4065, 37.7055, -122.3995, 37.7135)  # lon/lat window over the site
ACRE_M2 = tb.ACRE_M2

DA = {
    "title": "Visitacion Valley/Schlage Lock Development Agreement, final exhibits (SF Planning file dated 08-22-14; "
             "Ord. 149-14), Exhibit L Infrastructure Plan (May 28, 2014)",
    "url": tb.SCHLAGE_DA["url"],
    "sha256": tb.SCHLAGE_DA["sha256"],
    "file": tb.SCHLAGE_DA["file"],
}
FIG = {"page_index": 85, "printed_page": "PDF p. 86", "figure": "Figure 1.1, Conceptual Parcelization Plan"}
FIG_WINDOW = (150, 130, 620, 730)  # the map's frame in PDF points (x0, top, x1, bottom); legend is outside
PROPERTY_LINE_PT = 1.68  # stroke widths (PDF points) of the black property line and proposed parcel lines
PARCEL_LINE_PT = 1.44
JOIN_GAP_PT = 25  # join a line end to the nearest other line within this distance (dash gaps, short ends)
SCALE_BAR_M_PER_PT = 60.96 / (299 * 72 / 300)  # the 200-ft scale bar measures 299 px at 300 dpi
NORTH_ARROW_DEG = -20  # the north arrow leans about 20 degrees left of up

# A point inside each development parcel (PDF points) and the acreage printed in the figure.
PARCELS = {
    "1": ((261, 395), 0.96), "2": ((339, 395), 1.12), "3": ((278, 289), 0.59), "4": ((342, 293), 0.64),
    "5": ((303, 216), 0.52), "6": ((354, 228), 0.54), "7": ((243, 502), 0.94), "8": ((238, 600), 1.69),
    "9": ((340, 599), 1.68), "10": ((424, 423), 0.58), "11": ((432, 494), 0.91), "12": ((451, 611), 1.47),
}
ACRE_TOL = 0.02
# Phase 1 as approved by Planning on Sept 17, 2018 ("approves the development of Parcels 1, 2, and 3").
PHASE_1 = {"1", "2", "3"}

D4D = {
    "title": "Visitacion Valley/Schlage Lock Design for Development (June 16, 2014, as adopted)",
    "url": "https://default.sfplanning.org/Citywide/Visitacion_Valley/Visitacion_Valley_Schlage-Design_for_Development_20140616_BoS.pdf",
    "file": "sl-d4d-2014.pdf",
    "sha256": "5c4d8c4522deaa844b2a45bfe57757594577004927fb77affb7efbb7f5ba9216",
}
D4D_FIG = {"page_index": 42, "printed_page": "39", "figure": "Figure 2-3, Height Map"}
D4D_LEGEND = ["5 Stories | 57FT", "6 Stories | 68FT", "7 Stories | 76FT", "8 Stories | 86FT"]
# Heights Figure 2-3 colours on each block (read from the figure against its legend). Blocks 9 and 11
# are split: a 68-ft band along Block 9's north side, and Block 10's 68-ft zone reaching into
# Block 11's north-east corner; the rest 86 ft.
D4D_HEIGHTS = {"1": {76}, "2": {68}, "3": {68}, "4": {68}, "5": {57}, "6": {57}, "7": {68}, "8": {86},
               "9": {68, 86}, "10": {68}, "11": {68, 86}, "12": {86}}

HEIGHTS = {
    "title": "DataSF Zoning Map – Height and Bulk Districts",
    "landing": "https://data.sf.gov/d/h9wh-cg3m",
    "url": "https://data.sf.gov/resource/h9wh-cg3m.geojson?" + urllib.parse.urlencode({
        "$where": "intersects(the_geom, 'POLYGON((-122.408 37.706,-122.398 37.706,-122.398 37.716,"
                  "-122.408 37.716,-122.408 37.706))')",
        "$limit": 2000,
    }),
    "cache": RAW / "sl-height-bulk.geojson",
}
MIN_ZONE_M2 = 400  # smaller zoning pieces in a parcel are fit slivers along its edges; they join a neighbour

OFFICE = {
    "osm": "w868885320",
    "label": "Old Office Building",
    "permit": "201507010504",
}
PERMIT_URL = "https://data.sfgov.org/resource/i98e-djp9.json?permit_number={}"
HOUSING_PERMITS = ["201912189909", "201912189911"]


# ---------------------------------------------------------------- inputs

def _fetch_json(url: str, cache) -> object:
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=120) as r:
            cache.write_bytes(r.read())
    return json.loads(cache.read_text())


def _heights() -> gpd.GeoDataFrame:
    fc = _fetch_json(HEIGHTS["url"], HEIGHTS["cache"])
    return gpd.GeoDataFrame.from_features(fc["features"], crs=4326).to_crs(UTM)


def _permit(number: str) -> dict:
    rows = _fetch_json(PERMIT_URL.format(number), RAW / f"sl-dbi-{number}.json")
    if len(rows) != 1:
        raise SystemExit(f"schlage-lock: expected one DBI record for {number}, found {len(rows)}")
    return rows[0]


def _buildings() -> gpd.GeoDataFrame:
    """Overture building footprints over the site, with names and heights (cached)."""
    cache = RAW / "sl-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["osm"] = g["sources"].apply(lambda s: next((x["record_id"].split("@")[0] for x in s
                                                  if x.get("dataset") == "OpenStreetMap" and x.get("record_id")), None))
    g["height_src"] = g["sources"].apply(lambda s: next((x.get("dataset") for x in s
                                                         if x.get("property") == "/properties/height"), None))
    return g


def _site() -> shapely.Polygon:
    fc = json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
    site = next(f for f in fc["features"] if f["properties"]["kind"] == "site")
    return gpd.GeoSeries([shapely.geometry.shape(site["geometry"])], crs=4326).to_crs(UTM).iloc[0]


# ---------------------------------------------------------------- figure 1.1

def _strokes(page, width: float) -> list[LineString]:
    x0, y0, x1, y1 = FIG_WINDOW
    out = []
    for o in page.lines + page.curves:
        if abs(o["linewidth"] - width) > 0.01 or str(o["stroking_color"]) != "0":
            continue
        pts = [(float(x), float(y)) for x, y in o["pts"]]
        if len(pts) >= 2 and all(x0 < x < x1 and y0 < y < y1 for x, y in pts):
            out.append(LineString(pts))
    return out


def _faces(lines: list[LineString]) -> list[shapely.Polygon]:
    """Polygonise the parcel line work: each dangling line end is joined to the nearest other line
    within JOIN_GAP_PT (the gaps of dashed lines and short ends at corners)."""
    joins = []
    for i, line in enumerate(lines):
        others = shapely.union_all([m for j, m in enumerate(lines) if j != i])
        for xy in (line.coords[0], line.coords[-1]):
            p = Point(xy)
            d = p.distance(others)
            if 1e-6 < d <= JOIN_GAP_PT:
                joins.append(shapely.shortest_line(p, others))
    noded = shapely.union_all(lines + joins)
    return [f for f in shapely.get_parts(shapely.polygonize(shapely.get_parts(noded))) if f.area > 150]


def georeference(property_lines: list[LineString], site) -> tuple[trace.Similarity, dict]:
    pts = np.vstack([np.array([ln.interpolate(d).coords[0] for d in np.arange(0, ln.length, 1.0)])
                     for ln in property_lines if ln.length > 0])
    init = trace.Similarity(SCALE_BAR_M_PER_PT, np.radians(NORTH_ARROW_DEG), 0, 0)
    shift = np.array(site.centroid.coords[0]) - init.apply(pts).mean(0)
    init.tx, init.ty = float(shift[0]), float(shift[1])
    keep = 0.8
    sim, d = tb.icp(pts, [site.exterior], np.zeros(len(pts), int), init, keep, iterations=200)
    rep = tb.icp_report(sim, d, keep, "Figure 1.1 property line vs the Project Site's assessor parcels")
    return sim, rep


# ---------------------------------------------------------------- heights

def _zones(parcel, heights: gpd.GeoDataFrame, name: str) -> list[tuple[int, object]]:
    """Split a parcel by the zoning height districts; slivers join the neighbour they share most edge with."""
    pieces = []
    for _, z in heights.iterrows():
        g = parcel.intersection(z.geometry)
        if g.area > 0.5:
            h = int(z["height"].split("-")[0]) if z["height"][0].isdigit() else None
            pieces.append([h, g])
    is_big = [p[1].area >= MIN_ZONE_M2 and p[0] is not None for p in pieces]
    big = [p for p, k in zip(pieces, is_big) if k]
    if not big:
        raise SystemExit(f"schlage-lock: Parcel {name} has no height district")
    for (h, g), k in zip([tuple(p) for p in pieces], is_big):
        if k:
            continue
        host = max(big, key=lambda b: g.buffer(0.5).intersection(b[1].buffer(0.5)).area)
        host[1] = shapely.union_all([host[1], g])
    # Merge pieces of the same height, then check them against the D4D's Figure 2-3.
    out: dict[int, object] = {}
    for h, g in big:
        out[h] = shapely.union_all([out[h], g]) if h in out else g
    if not set(out) <= D4D_HEIGHTS[name]:
        raise SystemExit(f"schlage-lock: Parcel {name} zoning heights {sorted(out)} are not the D4D's {sorted(D4D_HEIGHTS[name])}")
    return sorted(out.items())


# ---------------------------------------------------------------- main

def main() -> None:
    da_path = trace.fetch_document(DA["url"], tb.DOCS / DA["file"], DA["sha256"])
    d4d_path = trace.fetch_document(D4D["url"], tb.DOCS / D4D["file"], D4D["sha256"])
    with pdfplumber.open(d4d_path) as pdf:
        text = pdf.pages[D4D_FIG["page_index"]].extract_text() or ""
        if not all(s in text for s in ["FIGURE 2-3", "Height Map", *D4D_LEGEND]):
            raise SystemExit("schlage-lock: D4D Figure 2-3 legend not found on the expected page")

    site = _site()
    with pdfplumber.open(da_path) as pdf:
        page = pdf.pages[FIG["page_index"]]
        prop = _strokes(page, PROPERTY_LINE_PT)
        parcel_lines = _strokes(page, PARCEL_LINE_PT)
    sim, georef = georeference(prop, site)
    print(f"[schlage-lock] Figure 1.1 fit to the assessor site: scale {sim.scale:.4f} m/pt "
          f"(scale bar {SCALE_BAR_M_PER_PT:.4f}), rotation {np.degrees(sim.rotation):.2f} deg, "
          f"trimmed RMS {sim.rms_m:.2f} m, median {georef['median_m']} m, p90 {georef['p90_m']} m")

    faces = _faces(prop + parcel_lines)
    parcels, acres = {}, {}
    for name, (xy, stated) in PARCELS.items():
        hits = [f for f in faces if f.contains(Point(xy))]
        if len(hits) != 1:
            raise SystemExit(f"schlage-lock: Parcel {name} label point falls in {len(hits)} faces")
        g = shapely.make_valid(sim.geometry(hits[0]))
        a = g.area / ACRE_M2
        if abs(a - stated) > ACRE_TOL:
            raise SystemExit(f"schlage-lock: Parcel {name} traces to {a:.3f} acres, the figure says {stated}")
        parcels[name], acres[name] = g, round(a, 3)
    print("[schlage-lock] parcels (traced vs printed acres): "
          + ", ".join(f"{k} {acres[k]:.2f}/{PARCELS[k][1]:.2f}" for k in PARCELS))
    georef["acreage_check"] = {k: {"traced": acres[k], "printed": PARCELS[k][1]} for k in PARCELS}

    heights = _heights()
    for n in HOUSING_PERMITS:
        if _permit(n).get("status") != "filed":
            raise SystemExit(f"schlage-lock: housing permit {n} has moved past 'filed'; review the parcels' stage")

    fig = f"{DA['title']}, {FIG['figure']} ({FIG['printed_page']})"
    d4d = f"{D4D['title']}, {D4D_FIG['figure']}, p. {D4D_FIG['printed_page']}"
    features = []
    for name, parcel in parcels.items():
        parcel = parcel.intersection(site)
        zones = _zones(parcel, heights, name)
        split = len(zones) > 1
        for h, g in zones:
            g = trace.as_multipolygon(shapely.make_valid(g.simplify(0.3)))
            props = {
                "kind": "block",
                "block": name,
                "label": f"Parcel {name}",
                "stage": "entitled",
                "height_ft": h,
                "podium_ft": None,
                "base_ft": 0,
                "use": None,
                "phase": "Phase 1" if name in PHASE_1 else None,
                "illustrative": True,
                "source": f"illustrative: drawn to the {h}-ft height limit of the {h}-X district in the {HEIGHTS['title']} "
                          f"(h9wh-cg3m; Ord. 150-14), clipped to Parcel {name} as traced from {fig}; "
                          f"height matches {d4d}",
            }
            notes = []
            if split:
                notes.append(f"Part of Parcel {name}: the zoning map and the D4D's height map split it between "
                             + " and ".join(f"{z} ft" for z, _ in zones) + ".")
            if name == "1":
                notes.append("The development agreement requires a full-service grocery store of at least 15,000 sq ft "
                             "on Parcel 1.")
            if name in PHASE_1:
                notes.append("Planning approved Parcels 1, 2 and 3 as Phase 1 on Sept 17, 2018; building permits for "
                             "two apartment buildings (5 and 7 stories) were filed in Dec 2019 and not issued.")
            if notes:
                props["note"] = " ".join(notes)
            features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(g))})
    print("[schlage-lock] zones: " + ", ".join(f"{f['properties']['block']}:{f['properties']['height_ft']}" for f in features))

    # --- the Old Office Building ---
    b = _buildings()
    office = b[b["osm"] == OFFICE["osm"]]
    if len(office) != 1:
        raise SystemExit(f"schlage-lock: expected one footprint for OpenStreetMap {OFFICE['osm']}, found {len(office)}")
    office = office.iloc[0]
    office_utm = gpd.GeoSeries([office.geometry], crs=4326).to_crs(UTM).iloc[0]
    if not office_utm.representative_point().within(site):
        raise SystemExit("schlage-lock: the office footprint is not on the site")
    permit = _permit(OFFICE["permit"])
    if permit.get("status") != "complete" or permit.get("number_of_proposed_stories") != "4":
        raise SystemExit(f"schlage-lock: DBI permit {OFFICE['permit']} is {permit.get('status')}, "
                         f"{permit.get('number_of_proposed_stories')} stories")
    features.append({
        "type": "Feature",
        "properties": {
            "kind": "landmark", "label": OFFICE["label"], "stage": "complete",
            # No official height: the base map's figure is a machine-learning estimate, so none is drawn.
            "height_ft": None, "podium_ft": None, "base_ft": 0,
            "use": "Office", "phase": None, "illustrative": False,
            "source": f"footprint: OpenStreetMap {OFFICE['osm']} via Overture {config.OVERTURE_RELEASE}; "
                      f"height: none official (the base map's {office['height_src']} estimate is not used); "
                      f"stories: DBI permit {OFFICE['permit']} ({PERMIT_URL.format(OFFICE['permit'])}): 4 stories, "
                      f"rehabilitation complete {permit['completed_date'][:10]}",
            "stories": 4,
            "note": "The historic Schlage Lock office building (about 1926) at 2201 Bayshore Blvd, kept and "
                    "rehabilitated for offices. DBI counts 4 stories; no official height in feet was found, so it is "
                    "outlined, not raised. The zoning map gives its lot a 45-ft limit.",
            "osm": OFFICE["osm"],
        },
        "geometry": mapping(office.geometry),
    })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each of the twelve development parcels is drawn whole to its height limit "
                "(57 to 86 ft) under the 2014 rezoning and Design for Development, not as a building design. Parcel "
                "shapes are traced from the development agreement's parcelization plan. The restored Old Office "
                "Building is drawn from the base map. Parks, streets, the rail lots and Parcel 14 aren't drawn."
            ),
            "note": ("Parcels are drawn to their 2014 height limits, not as building designs; nothing new has been "
                     "built yet."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2014 (PDF)",
            "georeference": {"figure_1_1": georef},
            "license": "Parcel shapes: traced from a public City and County of San Francisco development agreement "
                       "exhibit. Height limits: DataSF Zoning Map – Height and Bulk Districts (Public Domain). "
                       "Office footprint: OpenStreetMap contributors (ODbL 1.0), via Overture Maps.",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[schlage-lock] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
