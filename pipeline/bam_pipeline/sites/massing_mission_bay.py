"""Mission Bay: the plan blocks still to be built, drawn to their height limits.

Mission Bay is largely built, so this draws only what official sources show is left on the
redevelopment plan's development blocks. Everything already built stays in the base map.

What's left, and the sources that say so:
- Block 4 East (Mission Bay South, parcel 8711/029B): 100% affordable housing. Entitlement
  approved Nov 18, 2025 and building permits issued (DBI 202512161871, 16 stories, 165 homes,
  issued June 26, 2026; DBI 202512172072, 23 stories, 233 homes, issued Sept 9, 2026). MOHCD's
  affordable housing pipeline lists both phases as pre-construction, with construction starting
  in 2027 and 2028, so the block is "entitled", not yet "construction".
- Block 12 West (parcel 8710/006): affordable housing site with no project yet. MOHCD lists it
  as "Multiphase Project before Predevelopment" (construction estimated 2028). The adopted 2023
  Housing Element (Appendix B1, p. 4) says two affordable parcels remain in Mission Bay; these
  are the two in MOHCD's pipeline.

Heights (Mission Bay South Design for Development, as amended Nov 17, 2025):
- Map 4 "Height" (p. 22) puts Block 12 in height zone HZ-2 and Block 4 in HZ-3. The Height Zone
  Chart (p. 24) gives both zones a 65-ft base height, a 90-ft midrise height and a 160-ft tower
  height, with midrise and tower heights allowed only on a share of each zone's developable area
  (not block by block). Each block is drawn with the tower limit as height_ft and the base height
  as podium_ft, so the map shows the base solid and the tower allowance as an envelope.
- The northern half of Block 4 East has a 250-ft limit for affordable housing (chart footnote,
  and Redevelopment Plan Sec. 304.5 as amended by Ordinance 022-26, Feb 13, 2026). The plan
  doesn't map the half-line; it's drawn here by splitting the parcel into equal-area halves
  parallel to Mission Rock Street (approximate).

Footprints: DataSF "Parcels – Active and Retired" (acdm-wktn), one assessor parcel per block.
Block names: OCII "Mission Bay Land Use Map", October 2023, georeferenced on street
intersections matched to OpenStreetMap (via Overture); each parcel must contain its block label.

Left out on purpose (see the summary): completed buildings, including the recent ones (Block 1's
hotel, 2024; Blocks 9 and 9A affordable housing, 2023 and 2025; 1450 Owens on Blocks 41-43, 2025),
whose footprints are already in the base data (checked here); the Blocks 29-30 hotel/residential
project (entitled, no start date per the Housing Element, and no official footprint); UCSF land;
parks and streets; Mission Bay North (complete per OCII).

    uv run --directory pipeline python -m bam_pipeline.sites.massing_mission_bay
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.affinity import rotate
from shapely.geometry import Point, box, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "mission-bay"
UTM = "EPSG:26910"
BBOX = (-122.400, 37.760, -122.380, 37.7795)  # lon/lat window around Mission Bay South
RAW = config.ROOT / "data" / "raw" / "massing"
DOCS = config.ROOT / "data" / "raw" / "docs"

D4D = {
    "title": "Mission Bay South Design for Development (OCII, as amended Nov 17, 2025)",
    "url": "https://sfocii.org/files/2026-08/Design%20for%20Development%20for%20the%20Mission%20Bay%20South%20Project%20Area%20November%2017%2C%202025.pdf",
    "file": "mb-mbs-d4d-2025.pdf",
    "sha256": "32ae30bca7e63311297e9544496638475691d810e6ce12cb04aa42a4cb3c081d",
    "map4": "Map 4 \"Height\", p. 22",
    "chart": "Height Zone Chart, p. 24",
}
PLAN = {
    "title": "Mission Bay South Redevelopment Plan (as amended by Ordinance 022-26, Feb 13, 2026)",
    "url": "https://sfocii.org/files/inline-files/6th%20Redevelopment%20Plan%20Amendment%20for%20the%20MBS%20Redevelopment%20Project.pdf",
    "file": "mb-mbs-plan-6th-amendment.pdf",
    "sha256": "3853989bcb5dcf7f92f00d272721564467bbd9da0eb9d016d110c16bdc67697a",
    "section": "Sec. 304.5, p. 20",
}
LAND_USE = {
    "title": "OCII Mission Bay Land Use Map, October 2023",
    "url": "https://sfocii.org/sites/default/files/inline-files/MB%20Land%20Use%20Map%20Oct%202023_0.pdf",
    "file": "mb-land-use-map-2023.pdf",
    "sha256": "3c232447f08b865f929ff28c4075b5669307ee4a92a734b00382572b7692a662",
}
HE_B1 = "https://sfplanning.s3.amazonaws.com/archives/sfhousingelement.org/files/AppendixB1.pdf"
PARCELS = {"title": "DataSF Parcels – Active and Retired", "landing": "https://data.sf.gov/d/acdm-wktn"}
MOHCD = {"title": "MOHCD Affordable Housing Pipeline (DataSF)", "landing": "https://data.sf.gov/d/aaxw-2cb8",
         "api": "https://data.sf.gov/resource/aaxw-2cb8.json"}
DBI = {"landing": "https://data.sf.gov/d/i98e-djp9", "api": "https://data.sf.gov/resource/i98e-djp9.json"}

# Street centrelines in the 200-dpi render of the land use map (pixels), read from the block edges
# on either side of each street.
LU_DPI = 200
LU_CONTROLS = {
    ("3rd Street", "Channel Street"): (1140.0, 614.0),
    ("3rd Street", "Mission Rock Street"): (1140.0, 806.0),
    ("3rd Street", "China Basin Street"): (1140.0, 916.0),
    ("4th Street", "China Basin Street"): (979.0, 916.0),
    ("3rd Street", "16th Street"): (1140.0, 1519.0),
    ("4th Street", "16th Street"): (978.5, 1519.0),
    ("Owens Street", "16th Street"): (815.0, 1519.0),
    ("Illinois Street", "16th Street"): (1232.0, 1519.0),
    ("3rd Street", "Mariposa Street"): (1139.0, 1828.0),
    ("Owens Street", "Mariposa Street"): (815.0, 1828.0),
}

# Height zones (D4D Map 4 and Height Zone Chart): base, midrise and tower heights in feet.
ZONES = {"HZ-2": (65, 90, 160), "HZ-3": (65, 90, 160)}

BLOCKS = {
    "4E": {
        "name": "Block 4 East",
        "blklot": "8711029B",
        "zone": "HZ-3",
        "use": "Affordable housing",
        "mohcd": ["Mission Bay South Block 4 East (Phase I)", "Mission Bay South Block 4 East (Phase II)"],
        "permits": {"202512161871": (16, 165), "202512172072": (23, 233)},
    },
    "12W": {
        "name": "Block 12 West",
        "blklot": "8710006",
        "zone": "HZ-2",
        "use": "Affordable housing",
        "mohcd": ["Mission Bay South Block 12 West"],
        "permits": {},
    },
}

# Recently completed buildings whose footprints must already be in the base data: assessor parcel
# and the DBI new-construction permit marked complete (2023-2025).
RECENT = {
    "Block 1 hotel (100 Channel St)": ("8715208", "201509227707"),
    "Block 9 (410 China Basin St)": ("8719003", "201901281440"),
    "Block 9A (400 China Basin St)": ("8719008", "202103166613"),
    "Blocks 41-43 parcel 7 (1450 Owens St)": ("8709017", "202012281760"),
}


def _cached_json(name: str, url: str):
    out = RAW / name
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url) as r:
            out.write_bytes(r.read())
    return json.loads(out.read_text())


def _soql(base: str, **params) -> str:
    return base + "?" + urllib.parse.urlencode(params)


def _parcels() -> gpd.GeoDataFrame:
    lots = [b["blklot"] for b in BLOCKS.values()] + [v[0] for v in RECENT.values()]
    url = _soql("https://data.sf.gov/resource/acdm-wktn.geojson",
                **{"$where": "active='True' AND blklot in(" + ",".join(f"'{x}'" for x in lots) + ")", "$limit": 5000})
    out = RAW / "mb-parcels-blocks.geojson"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url) as r:
            out.write_bytes(r.read())
    g = gpd.read_file(out).to_crs(UTM)
    g = g.dissolve(by="blklot", as_index=False, aggfunc="first")
    missing = set(lots) - set(g["blklot"])
    if missing:
        raise SystemExit(f"parcels not found in {PARCELS['landing']}: {sorted(missing)}")
    return g.set_index("blklot")


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "mb-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    return gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                            geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)),
                            crs=4326).to_crs(UTM)


def _georeference(streets: gpd.GeoDataFrame) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), xy in LU_CONTROLS.items():
        src.append(xy)
        dst.append(tb.intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def _label_points(sim: trace.Similarity, labels: list[str]) -> dict[str, Point]:
    import pdfplumber

    path = trace.fetch_document(LAND_USE["url"], DOCS / LAND_USE["file"], LAND_USE["sha256"])
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        out = {}
        for lab in labels:
            x, y = trace.pdf_label_center(page, lab)
            out[lab] = Point(sim.apply([(x * LU_DPI / 72, y * LU_DPI / 72)])[0])
    return out


def _check_status() -> dict[str, list[dict]]:
    """Fetch (once) the MOHCD pipeline and DBI permit records the stages rest on, and check them."""
    names = [n for b in BLOCKS.values() for n in b["mohcd"]]
    mohcd = _cached_json("mb-mohcd-pipeline.json", _soql(
        MOHCD["api"], **{"$where": "project_name in(" + ",".join(f"'{n}'" for n in names) + ")"}))
    by_name = {r["project_name"]: r for r in mohcd}
    out = {}
    for key, b in BLOCKS.items():
        recs = []
        for n in b["mohcd"]:
            r = by_name.get(n)
            if r is None:
                raise SystemExit(f"{b['name']}: {n!r} not in {MOHCD['landing']}")
            if r.get("issuance_of_first_construction_document"):
                raise SystemExit(f"{b['name']}: {n} has a first construction document; revisit the stage")
            if r.get("block") != b["blklot"][:4] or r.get("lot", "").lstrip("0") != b["blklot"][4:].lstrip("0"):
                raise SystemExit(f"{b['name']}: MOHCD parcel {r.get('block')}/{r.get('lot')} != {b['blklot']}")
            recs.append(r)
            print(f"[mission-bay] {n}: {r['project_status']}, {r['construction_status']}, "
                  f"start est. {r.get('estimated_actual_construction_start_date', '')[:7]}")
        out[key] = recs
    permits = list(BLOCKS["4E"]["permits"])
    dbi = _cached_json("mb-dbi-permits.json", _soql(
        DBI["api"], **{"$where": "permit_number in(" + ",".join(f"'{p}'" for p in permits) + ")",
                       "$select": "permit_number,status,issued_date,block,lot,number_of_proposed_stories,proposed_units"}))
    for p, (stories, units) in BLOCKS["4E"]["permits"].items():
        r = next((x for x in dbi if x["permit_number"] == p), None)
        if r is None or r["block"] + r["lot"] != BLOCKS["4E"]["blklot"]:
            raise SystemExit(f"DBI permit {p} not found on parcel {BLOCKS['4E']['blklot']}")
        if int(float(r["number_of_proposed_stories"])) != stories or int(float(r["proposed_units"])) != units:
            raise SystemExit(f"DBI permit {p}: {r['number_of_proposed_stories']} stories, {r['proposed_units']} units")
        print(f"[mission-bay] DBI {p}: {r['status']} {r.get('issued_date', '')[:10]}, {stories} stories, {units} homes")
    return out


def _split_north(parcel, streets: gpd.GeoDataFrame):
    """Split a parcel into equal-area halves along Mission Rock Street; return (north, south)."""
    mr = shapely.union_all(streets[streets["name"] == "Mission Rock Street"].geometry.to_numpy())
    near = shapely.shortest_line(parcel.centroid, mr)
    (x0, y0), (x1, y1) = near.coords
    ang = np.degrees(np.arctan2(y1 - y0, x1 - x0))  # direction from the parcel towards Mission Rock St
    # Rotate so that direction points along +y, then cut horizontally at the area median.
    g = rotate(parcel, 90 - ang, origin=parcel.centroid)
    minx, miny, maxx, maxy = g.bounds
    lo, hi = miny, maxy
    for _ in range(60):
        mid = (lo + hi) / 2
        if g.intersection(box(minx - 1, miny - 1, maxx + 1, mid)).area < g.area / 2:
            lo = mid
        else:
            hi = mid
    cut = (lo + hi) / 2
    north = rotate(g.intersection(box(minx - 1, cut, maxx + 1, maxy + 1)), -(90 - ang), origin=parcel.centroid)
    south = rotate(g.intersection(box(minx - 1, miny - 1, maxx + 1, cut)), -(90 - ang), origin=parcel.centroid)
    if north.distance(mr) >= south.distance(mr):
        raise SystemExit("Block 4 East split: the north half is not the one on Mission Rock Street")
    return north, south


def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    for doc in (D4D, PLAN):
        trace.fetch_document(doc["url"], DOCS / doc["file"], doc["sha256"])

    streets = tb.streets("mb-mission_bay", BBOX)
    streets = streets[streets["subtype"] == "road"]
    sim = _georeference(streets)
    print(f"[mission-bay] land use map georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale:.4f} m/px")

    parcels = _parcels()
    labels = _label_points(sim, list(BLOCKS))
    for key, b in BLOCKS.items():
        geom = parcels.loc[b["blklot"]].geometry
        if not geom.contains(labels[key]):
            raise SystemExit(f"{b['name']}: land use map label {key} falls {geom.distance(labels[key]):.0f} m "
                             f"outside parcel {b['blklot']}")
        if not geom.representative_point().within(site_utm):
            raise SystemExit(f"{b['name']}: parcel {b['blklot']} is outside the site")

    # Undeveloped check, and recent completions present in the base footprints.
    bldgs = _buildings()
    built = shapely.union_all(bldgs.geometry.to_numpy())
    for key, b in BLOCKS.items():
        geom = parcels.loc[b["blklot"]].geometry
        cover = geom.intersection(built).area / geom.area
        if cover > 0.05:
            raise SystemExit(f"{b['name']}: base footprints already cover {cover:.0%} of the parcel")
        print(f"[mission-bay] {b['name']} (parcel {b['blklot']}): {geom.area:.0f} m², base footprints cover {cover:.0%}")
    recent_ok = []
    for name, (lot, permit) in RECENT.items():
        geom = parcels.loc[lot].geometry
        cover = geom.intersection(built).area / geom.area
        if cover < 0.4:
            raise SystemExit(f"{name}: base footprints cover only {cover:.0%} of parcel {lot}; draw it here")
        recent_ok.append(name)
        print(f"[mission-bay] recent: {name}, DBI {permit}: base footprints cover {cover:.0%} of parcel {lot}")

    status = _check_status()

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    heights = f"{D4D['title']}, {D4D['map4']} and {D4D['chart']} ({D4D['url']})"
    footprint = f"footprint: assessor parcel {{}} in {PARCELS['title']} ({PARCELS['landing']})"
    named = f"block named on the {LAND_USE['title']}"
    features = []

    # Block 4 East: north half to 250 ft, south half to 160 ft.
    b = BLOCKS["4E"]
    base, mid, tower = ZONES[b["zone"]]
    north, south = _split_north(parcels.loc[b["blklot"]].geometry, streets)
    permits = " and ".join(f"{p} ({s} stories, {u} homes)" for p, (s, u) in b["permits"].items())
    starts = " and ".join(r["estimated_actual_construction_start_date"][:4] for r in status["4E"])
    common_4e = (f"Entitlement approved Nov 18, 2025; DBI building permits {permits} issued in 2026. MOHCD lists "
                 f"both phases as pre-construction, starting {starts}.")
    for half, geom, height in (("north", north, 250), ("south", south, tower)):
        if half == "north":
            limit = (f"250 ft for affordable housing on the northern half of Block 4 East ({PLAN['title']}, "
                     f"{PLAN['section']}; {D4D['chart']} footnote)")
            note = (f"Northern half of Block 4 East (approximate split): 250-ft limit for affordable housing, "
                    f"{base}-ft base height. {common_4e}")
        else:
            limit = f"{tower} ft tower height in {b['zone']}"
            note = (f"Southern half of Block 4 East (approximate split): {base}-ft base height, {mid}-ft midrise and "
                    f"{tower}-ft towers allowed on a share of {b['zone']}. {common_4e}")
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "block", "block": "4E", "label": f"Block 4 East ({half})", "stage": "entitled",
                "height_ft": height, "podium_ft": base, "base_ft": 0, "use": b["use"], "phase": None,
                "illustrative": True,
                "source": (f"illustrative: drawn to the height limit, not a building design: {limit}; base height "
                           f"{base} ft in {b['zone']}, {heights}; {footprint.format(b['blklot'])}, split into "
                           f"equal-area halves parallel to Mission Rock Street (approximate); {named}; status: "
                           f"{MOHCD['title']} ({MOHCD['landing']}) and DBI permits ({DBI['landing']})"),
                "note": note,
            },
            "geometry": mapping(to_wgs(trace.as_multipolygon(shapely.make_valid(geom.simplify(0.3))))),
        })

    # Block 12 West.
    b = BLOCKS["12W"]
    base, mid, tower = ZONES[b["zone"]]
    r = status["12W"][0]
    features.append({
        "type": "Feature",
        "properties": {
            "kind": "block", "block": "12W", "label": "Block 12 West", "stage": "entitled",
            "height_ft": tower, "podium_ft": base, "base_ft": 0, "use": b["use"], "phase": None,
            "illustrative": True,
            "source": (f"illustrative: drawn to the height limit, not a building design: {tower} ft tower height, "
                       f"{base} ft base height in {b['zone']}, {heights}; {footprint.format(b['blklot'])}; {named}; "
                       f"status: {MOHCD['title']} ({MOHCD['landing']})"),
            "note": (f"Affordable housing site with no project yet: MOHCD lists it as \"{r['construction_status'][4:]}\", "
                     f"starting about {r['estimated_actual_construction_start_date'][:4]}. {base}-ft base height, "
                     f"{mid}-ft midrise and {tower}-ft towers allowed on a share of {b['zone']}."),
        },
        "geometry": mapping(to_wgs(trace.as_multipolygon(shapely.make_valid(parcels.loc[b["blklot"]].geometry.simplify(0.3))))),
    })

    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Mission Bay is largely built, so only the two plan blocks official sources show as still to come "
                "are drawn: Block 4 East (affordable housing, entitled with building permits issued in 2026) and "
                "Block 12 West (an affordable housing site with no project yet). Both are illustrative: each "
                "parcel is drawn to its height limit in the Mission Bay South Design for Development (65-ft base, "
                "160-ft towers, and 250 ft on the northern half of Block 4 East), not as a building design. "
                "Completed buildings, including the most recent (Block 1's hotel, Blocks 9 and 9A, and 1450 Owens "
                "Street), are already in the base map. Not drawn: the entitled Warriors hotel and residential "
                "building on Blocks 29-30, which has no start date or official footprint; UCSF's campus; parks "
                "and streets."
            ),
            "note": ("Only the blocks left to build are drawn, to their height limits rather than as designs; "
                     "the rest of Mission Bay is already built."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2025 (PDF)",
            "georeference": {
                "parcels": "GIS layer, used as published (no tracing)",
                "land_use_map": {**sim.report(), "use": "block names only"},
                "block_4e_split": "equal-area halves parallel to Mission Rock Street (approximate; the plan maps no line)",
            },
            "statusSources": {
                "mohcd": MOHCD["landing"],
                "dbi": DBI["landing"],
                "housingElement": f"{HE_B1} (p. 4: two affordable parcels remain; Blocks 29-30 units have no start date)",
            },
            "recentCompletionsInBase": recent_ok,
            "license": ("Block shapes: DataSF parcels (Public Domain U.S. Government). Heights: OCII Mission Bay "
                        "South Design for Development and Redevelopment Plan (public records)."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(fc), indent=1) + "\n")
    print(f"[mission-bay] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


if __name__ == "__main__":
    main()
