"""Transbay Parcel F: the approved tower, traced from the floor plans in the 2020 Planning Commission packet.

Source:
- Planning Commission packet for Record No. 2016-013312PRJ, 542-550 Howard Street (Transbay Parcel F), hearing
  Jan 9, 2020: Exhibit B, the architect's 309 application drawings (Pelli Clarke Pelli, Dec 20, 2019). The floor
  plans are vector drawings, each with the site's property line as a dash-dot line:
  PDF p. 387 "Plan - Level 2", p. 390 "Plan - Level 7", p. 391 "Plan - Level 17 to 30 - Typical office floor"
  and p. 393 "Plan - Level 34 to 61 - Typical residential floor".
- Level heights from the same packet's tower section (PDF p. 395): level 5 at +64'-0", level 8 at +108'-0", level 33
  at +429'-10", the roof (level 62) at +749'-10" and the top at +800'-0". The draft Downtown Project Authorization
  (PDF p. 12, finding 2): "a new 61-story mixed-use building reaching a height of 749'-10" tall (799'-9" inclusive
  of rooftop screening/mechanical equipment)". The Commission adopted it as Motion 20616 on Jan 9, 2020 (minutes),
  and on Jan 28, 2021 amended only its affordable housing conditions (Motion 20843), so the design is unchanged.

How it's drawn:
- For each plan, the property line's six right-angled corners (the two Howard Street corners, the Natoma Street
  corners and the two corners of the strip along Natoma Street behind 540 Howard Street) are matched to the same
  corners of the DataSF parcels (block 3721 lots 016, 135, 136 and 138, the boundary file) by a least-squares
  similarity; the RMS is reported. The building's outer outline on that plan is carried to the map with it.
- Four volumes: levels 1-4 (the level 2 outline, which the drawing leaves open along the east property line and is
  closed up it, to level 5 at 64 ft); levels 5-7 (the level 7 outline, to 108 ft), which cantilever over the rail
  "train box" below the site's northwest corner; levels 8-32, hotel and office (the typical office outline; the
  hotel floors share it), to level 33 at 429 ft 10 in; and levels 33-61, residential amenity and homes (the typical
  residential outline), to the roof at 749 ft 10 in. The crown and rooftop screen
  (to 799 ft 9 in), the ground floor's own outline, the terraces cut out of levels 5 and 6, the smaller level 31-32
  plates and the pedestrian bridge to Salesforce Park are not drawn. Illustrative.

Stage: approved (Jan 9, 2020; amended Jan 28, 2021); DBI hasn't issued the site permit (application 201903215849,
filed March 21, 2019), so every volume is drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_transbay_parcel_f
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import Polygon, mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "transbay-parcel-f"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639

PACKET = {
    "title": "Planning Commission packet, Record No. 2016-013312PRJ (542-550 Howard Street, Transbay Parcel F), hearing Jan 9, 2020",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2016-013312DNXCUAOFAVARSHDPCAMAPGPA_DRAFT.pdf",
    "sha256": "4edfeb92a6a2394ecd8a447af19d8b5e176fc5e88cb5a2a423a23fc6dec8ce59",
    "file": "2016-013312DNXCUAOFAVARSHDPCAMAPGPA_DRAFT.pdf",
}
MINUTES_URL = "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200109_cal_min.pdf"

PROPERTY_DASH = 9.026  # first dash length of the property line's dash-dot pattern
# Property-line vertices (in the drawing's order) that are true corners of the parcels, each with a point near the
# same corner of the DataSF parcels (UTM 10N); the code snaps to the nearest parcel vertex.
CORNERS = [
    (3, "Howard Street, west end of the frontage (lot 135 at the bus ramp property)", (553048.3, 4182409.7)),
    (4, "Howard Street, east end of the frontage (lot 016 at 540 Howard Street)", (553076.0, 4182437.6)),
    (5, "rear corner of 540 Howard Street (lot 136)", (553051.2, 4182462.3)),
    (6, "east corner of the Natoma Street strip (lot 136 at 530 Howard Street)", (553070.5, 4182481.8)),
    (7, "Natoma Street, east end of the frontage (lot 136)", (553059.8, 4182492.5)),
    (8, "Natoma Street, west end of the frontage (lot 138 at the bus ramp property)", (552997.9, 4182430.4)),
]

# Each volume: the plan page (1-based), which half of the sheet the plan sits on, the outline stroke's point count
# and first point (PDF points), points that close an outline drawn open, the closed area in square points (a check
# against a changed PDF), the base and roof heights in feet, and its text.
LEVELS = [
    {
        "label": "Levels 1-4", "page": 387, "half": "bottom", "npts": 13, "first": (463.2, 791.4),
        # The level 2 outline is drawn open along the east property line; it closes up that line.
        "close": [(482.8, 791.4)], "area_pt2": 65547,
        "plan": "Plan - Level 2", "base_ft": 0, "height_ft": 64,
        "use": "Lobbies and shops on the ground floor, hotel amenities, bike parking and building services",
        "note": "Levels 1 to 4, drawn at the level 2 outline up to level 5 (+64 ft). The ground floor is smaller.",
    },
    {
        "label": "Levels 5-7", "page": 390, "half": "top", "npts": 16, "first": (437.2, 493.5),
        "close": [], "area_pt2": 62788,
        "plan": "Plan - Level 7", "base_ft": 64, "height_ft": 108,
        "use": "Shops and office lobby at the Salesforce Park bridge (level 5), hotel amenities",
        "note": ("Levels 5 to 7, drawn at the level 7 outline up to level 8 (+108 ft); levels 5 and 6 leave open "
                 "terraces at the bridge to Salesforce Park. They cantilever over the rail train box under the site's "
                 "northwest corner."),
    },
    {
        "label": "Hotel and office floors", "page": 391, "half": "top", "npts": 20, "first": (254.6, 258.6),
        "close": [], "area_pt2": 64368,
        "plan": "Plan - Level 17 to 30 - Typical office floor", "base_ft": 108, "height_ft": 429.83,
        "use": "Hotel (189 rooms, levels 8-16), office (about 276,000 sq ft, levels 17-31), mechanical (level 32)",
        "note": ("Levels 8 to 32, drawn at the typical office outline (the hotel floors share it) up to level 33 "
                 "(+429 ft 10 in)."),
    },
    {
        "label": "Residential floors", "page": 393, "half": "top", "npts": 12, "first": (443.9, 480.7),
        "close": [], "area_pt2": 52877,
        "plan": "Plan - Level 34 to 61 - Typical residential floor", "base_ft": 429.83, "height_ft": 749.83,
        "use": "Homes (165), with residential amenities on level 33",
        "note": ("Levels 33 to 61, drawn at the typical residential outline up to the roof at 749 ft 10 in; the "
                 "rooftop screen and mechanical equipment reach 799 ft 9 in (Motion 20616)."),
    },
]


def _half(o, half: str) -> bool:
    mid = (o["top"] + o["bottom"]) / 2
    return mid < 560 if half == "top" else mid >= 560


def property_line(page, half: str) -> np.ndarray:
    """The 12-point dash-dot property line of the plan on one half of the sheet (PDF points, y down)."""
    found = []
    for o in page.curves:
        dash = o.get("dash")
        if dash and dash[0] and abs(dash[0][0] - PROPERTY_DASH) < 0.01 and len(o["pts"]) == 12 and _half(o, half):
            found.append(np.array(o["pts"], float))
    if not found:
        raise SystemExit(f"p. {page.page_number}: no property line on the {half} half")
    return found[0]


def outline(page, spec: dict) -> Polygon:
    """The building's outer outline: the solid black stroke with the expected point count and first point."""
    for o in page.curves:
        if not (o.get("stroke") and _half(o, spec["half"]) and len(o["pts"]) == spec["npts"]):
            continue
        if (o.get("dash") and o["dash"][0]) or tuple(o.get("stroking_color") or ()) != (0.0, 0.0, 0.0):
            continue
        if np.hypot(*(np.array(o["pts"][0]) - spec["first"])) > 0.5:
            continue
        poly = shapely.make_valid(Polygon(list(o["pts"]) + spec["close"])).buffer(0)
        if abs(poly.area - spec["area_pt2"]) > 50:
            raise SystemExit(f"p. {spec['page']}: outline area {poly.area:.0f} pt2, expected {spec['area_pt2']}")
        return poly
    raise SystemExit(f"p. {spec['page']}: building outline ({spec['npts']} points from {spec['first']}) not found")


def site_vertices() -> np.ndarray:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    return shapely.get_coordinates(shapely.union_all(ob._utm_shapes(fc).buffer(0.01).to_numpy()).boundary)


def fit(pl: np.ndarray, vertices: np.ndarray) -> trace.Similarity:
    src, dst, labels = [], [], []
    for i, label, near in CORNERS:
        d = np.linalg.norm(vertices - near, axis=1)
        if d.min() > 3:
            raise SystemExit(f"no parcel vertex within 3 m of the corner '{label}'")
        src.append(pl[i])
        dst.append(vertices[d.argmin()])
        labels.append(label)
    return trace.fit_similarity(np.array(src), np.array(dst), labels)


def main() -> None:
    pdf = trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    vertices = site_vertices()
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM).union_all()
    features, georef = [], {}
    with pdfplumber.open(pdf) as doc:
        for spec in LEVELS:
            page = doc.pages[spec["page"] - 1]
            pl = property_line(page, spec["half"])
            sim = fit(pl, vertices)
            poly = shapely.make_valid(Polygon(sim.apply(np.array(outline(page, spec).exterior.coords)))).buffer(0)
            outside = poly.difference(site.buffer(0.5)).area
            print(f"[parcel-f] {spec['label']}: p. {spec['page']} fit RMS {sim.rms_m:.2f} m "
                  f"(scale {sim.scale / FT:.4f} ft/pt); {poly.area * SQFT:,.0f} sq ft, "
                  f"{outside * SQFT:,.0f} sq ft outside the parcels; {spec['base_ft']}-{spec['height_ft']} ft")
            georef[f"p{spec['page']}"] = {"plan": spec["plan"], **sim.report()}
            wgs = gpd.GeoSeries([poly.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
            features.append({
                "type": "Feature",
                "properties": {
                    "kind": "building", "label": spec["label"], "stage": "entitled",
                    "height_ft": spec["height_ft"], "podium_ft": None, "base_ft": spec["base_ft"],
                    "use": spec["use"], "phase": None, "illustrative": True,
                    "source": (f"illustrative: outline traced from the {PACKET['title']}, Exhibit B, PDF p. "
                               f"{spec['page']} ({spec['plan']}), registered on the property line's corners; "
                               f"heights from the tower section, PDF p. 395"),
                    "note": spec["note"],
                },
                "geometry": mapping(wgs),
            })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the approved 61-story tower in four volumes, their outlines traced from "
                        "the floor plans in the 2020 Planning Commission packet (levels 2, 7, 17-30 and 34-61) and "
                        "registered on the site's property-line corners: a base to 64 ft, levels 5-7 cantilevered over "
                        "the rail train box to 108 ft, the hotel and office floors to 429 ft 10 in and the residential "
                        "floors to the roof at 749 ft 10 in. The crown to 799 ft 9 in and the bridge to Salesforce "
                        "Park are not drawn."),
            "note": "The approved tower as simple volumes, not the final design.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2020 (PDF)",
            "approvalSourceUrl": MINUTES_URL,
            "georeference": {
                "method": ("Each plan's property-line corners matched to the DataSF parcel corners of block 3721 lots "
                           "016, 135, 136 and 138 (least-squares similarity)."),
                **georef,
            },
            "license": "Outlines: traced from a public SF Planning document. Lots: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[parcel-f] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
