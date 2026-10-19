"""98 Franklin Street: the approved podium and tower as two simple volumes.

Sources:
- The Planning Commission packet for Record No. 2016-014802PRJ (hearing May 28, 2020; Exhibit B, the plan set by
  Skidmore, Owings & Merrill dated May 11, 2020). PDF p. 126, "Lower Tower Floor Plan" (scale 1/32" = 1'-0", a vector
  drawing), dimensions the tower at 130'-0" along Oak Street and 110'-0" along Franklin Street, and the lot at
  141'-9" on Oak Street and 125'-0" on Franklin Street, all measured from the Oak and Franklin corner. The elevations
  and sections (PDF pp. 110-113) give "TOP OF ROOF: 365'-0"", "TOP OF PARAPET: 396'-8"" and "TOP OF PODIUM ROOF:
  68'-0"".
- The same packet's draft Downtown Project Authorization (PDF pp. 41, 60-61), approved as Motion 20728 on May 28,
  2020 (minutes of that date, PDF p. 9): "a new 36-story mixed-use building reaching a roof height up to 365 feet
  tall (396'8" inclusive of rooftop screening/mechanical equipment)"; "a 5-story podium reaching a maximum height of
  68'"; "The Project's tower includes an average floor area of approximately 11,577 sf, while the maximum plan
  length is 130' and the maximum diagonal dimension is 170'3.5"".

How it's drawn:
- The plan's three property-line corners (the ends of its dimension lines: Oak and Franklin, the east end of the
  141'-9" Oak Street frontage, the south end of the 125'-0" Franklin Street frontage) are matched to the same corners
  of the DataSF parcels (block 0836 lots 008, 009 and 013, the boundary file) by a least-squares similarity; the RMS
  is reported.
- Tower: the outline of the lower tower floor, the closed ring of the plan's heaviest lines (the faceted curtain wall
  and the east and west balconies), carried to the map and extruded from the ground to the 365-ft roof. The upper
  third of the tower is about 5 percent smaller, and the parapet to 396 ft 8 in isn't drawn.
- Podium: the rest of the lots at 68 ft. The approval describes a "full lot coverage podium"; its roof terraces
  (the Market Street end steps down to a 54-ft 9-in terrace) aren't drawn. Illustrative.

Which design: the 2020 approval. In 2023 the Planning Commission heard a modification to a 38-story, 400-ft
building with 385 homes (agenda of March 30, 2023), and Planning's records of its zoning map change and Downtown
Project Authorization closed as approved in July and August 2023; but the development agreement that agenda says
"would enable" it (Board of Supervisors file 221163) is still "Under Review" in Planning's records, the City's
development pipeline (2026 Q2) still lists the 2020 approval with 345 homes, and the 2023 plans couldn't be opened.
To draw the 400-ft version instead, set TOWER_ROOF_FT = 400 and update the notes (the 2023 footprint is unknown).

Stage: approved in 2020; the site is still a parking lot and DBI's site permit application 202102184905 (filed
Feb 18, 2021) hasn't been issued, so both volumes are drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_98_franklin
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import LineString, Polygon, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "98-franklin"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639
PT_PER_FT = 72 / 32  # the plan's scale, 1/32" = 1'-0"

PACKET = {
    "title": "Planning Commission packet, Record No. 2016-014802PRJ (98 Franklin Street), hearing May 28, 2020",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2016-014802PRJ.pdf",
    "sha256": "b4f63cd58f027148d3358a8ae3cf0deba8eb2282b3909601ab23a435fcf660dd",
    "file": "2016-014802PRJ.pdf",
    "page": 126,
}
MINUTES_2020 = "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200528_cal_min.pdf"

# Property-line corners on PDF p. 126 (points, y down), at the ends of the dimension lines' extension lines, each
# with a point near the same corner of the parcels (UTM 10N); the code snaps to the nearest parcel vertex.
CORNERS = [
    ("Oak Street and Franklin Street (lot 013)", (256.17, 149.85), (551005.4, 4181026.0)),
    ("Oak Street, east end of the site (lot 008)", (575.07, 149.85), (551048.0, 4181033.1)),
    ("Franklin Street, south end of the site's frontage (lot 013)", (256.17, 431.07), (551011.6, 4180988.4)),
]
# Plan dimensions, in feet, to check the reading of the sheet: the lot's two frontages and the tower's two sides,
# each measured from the Oak and Franklin corner (x and y extents on the sheet).
LOT_DIMS_FT = {"Oak Street": 141 + 9 / 12, "Franklin Street": 125.0}
TOWER_DIMS_FT = {"along Oak Street": 130.0, "along Franklin Street": 110.0}
TOWER_EAST_PT, TOWER_SOUTH_PT = 548.67, 397.35  # the 130'-0" and 110'-0" dimension lines' far extension lines

WALL_LW = 0.8  # the heaviest line weight on the sheet (0.84 pt): curtain wall, balconies and core walls
TOWER_BOX = (250, 143, 556, 404)  # x0, top, x1, bottom on the sheet: the floor plate, not the street or dimensions
TOWER_AREA_SQFT = (10_500, 13_500)  # expected outline area, as a check against a changed PDF

TOWER_ROOF_FT = 365
PARAPET_FT = 396 + 8 / 12
PODIUM_FT = 68


def check_dims() -> None:
    (_, nw, _), (_, ne, _), (_, sw, _) = CORNERS
    got = {"Oak Street": ne[0] - nw[0], "Franklin Street": sw[1] - nw[1]}
    for k, pt in got.items():
        ft = pt / PT_PER_FT
        if abs(ft - LOT_DIMS_FT[k]) > 0.5:
            raise SystemExit(f"98 Franklin: {k} reads {ft:.1f} ft on the sheet, plan says {LOT_DIMS_FT[k]:.1f} ft")
    tower = {"along Oak Street": TOWER_EAST_PT - nw[0], "along Franklin Street": TOWER_SOUTH_PT - nw[1]}
    for k, pt in tower.items():
        ft = pt / PT_PER_FT
        if abs(ft - TOWER_DIMS_FT[k]) > 0.5:
            raise SystemExit(f"98 Franklin: the tower {k} reads {ft:.1f} ft, plan says {TOWER_DIMS_FT[k]:.1f} ft")


def tower_outline_pt(page) -> Polygon:
    """The floor plate: the area inside the closed ring of heavy wall lines."""
    x0, top, x1, bottom = TOWER_BOX
    lines = []
    for o in page.lines + page.curves + page.rects:
        if (o.get("linewidth") or 0) < WALL_LW:
            continue
        if o["x0"] < x0 or o["x1"] > x1 or o["top"] < top or o["bottom"] > bottom:
            continue
        pts = o.get("pts") or [(o["x0"], o["top"]), (o["x1"], o["top"]), (o["x1"], o["bottom"]),
                               (o["x0"], o["bottom"]), (o["x0"], o["top"])]
        if len(pts) >= 2:
            lines.append(LineString(pts))
    ink = shapely.union_all([g.buffer(0.6) for g in lines])
    plate = Polygon(trace.largest_polygon(ink).exterior).buffer(-0.6, join_style="mitre")
    plate = trace.largest_polygon(shapely.make_valid(plate))
    area = plate.area / PT_PER_FT**2
    if not TOWER_AREA_SQFT[0] <= area <= TOWER_AREA_SQFT[1]:
        raise SystemExit(f"98 Franklin: the tower outline is {area:,.0f} sq ft on the sheet, outside the range")
    return plate


def lots_utm() -> Polygon:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    utm = ob._utm_shapes(fc)
    g = shapely.union_all(utm.buffer(0.5).to_numpy()).buffer(-0.5)
    return trace.largest_polygon(g)


def fit(lot: Polygon) -> trace.Similarity:
    vertices = shapely.get_coordinates(lot.boundary)
    src, dst, labels = [], [], []
    for label, fig, near in CORNERS:
        d = np.linalg.norm(vertices - near, axis=1)
        if d.min() > 3:
            raise SystemExit(f"98 Franklin: no parcel vertex within 3 m of '{label}'")
        src.append(fig)
        dst.append(vertices[d.argmin()])
        labels.append(label)
    return trace.fit_similarity(np.array(src, float), np.array(dst, float), labels)


def clean(g, min_m2: float = 1.0):
    """Drop slivers and spikes, then simplify; keeps every part over min_m2 (the podium's wedges between the
    tower's inset faces and the street lines are separate parts). The result must be valid."""
    g = shapely.make_valid(g).buffer(-0.01, join_style="mitre").buffer(0.01, join_style="mitre")
    parts = [p.simplify(0.2) for p in trace.as_multipolygon(shapely.make_valid(g)).geoms if p.area >= min_m2]
    g = parts[0] if len(parts) == 1 else shapely.MultiPolygon(parts)
    if not g.is_valid:
        raise SystemExit("98 Franklin: a massing polygon is invalid after cleaning")
    return g


def main() -> None:
    pdf = trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    check_dims()
    with pdfplumber.open(pdf) as doc:
        plate_pt = tower_outline_pt(doc.pages[PACKET["page"] - 1])

    lot = lots_utm()
    sim = fit(lot)
    print(f"[98-franklin] plan p. {PACKET['page']} -> parcels: RMS {sim.rms_m:.2f} m over {len(CORNERS)} corners, "
          f"scale {sim.scale / FT:.4f} ft/pt (plan 1/32\" = 1' gives {1 / PT_PER_FT:.4f})")

    tower = shapely.make_valid(sim.geometry(plate_pt)).buffer(0)
    off = tower.difference(lot.buffer(0.5)).area
    tower = clean(tower.intersection(lot))
    # A 2-cm gap keeps the podium's parts from touching at the tower's corners once coordinates are rounded.
    podium = clean(lot.difference(tower.buffer(0.02, join_style="mitre")))
    print(f"[98-franklin] lots {lot.area * SQFT:,.0f} sq ft; tower {tower.area * SQFT:,.0f} sq ft "
          f"({off * SQFT:,.0f} sq ft trimmed outside the lots); podium {podium.area * SQFT:,.0f} sq ft")

    plan = f"{PACKET['title']}, Exhibit B (plan set, May 2020), PDF p. {PACKET['page']} (lower tower floor plan)"
    parts = [
        ("Podium", podium, PODIUM_FT, "High school (French American International School), shops, lobbies",
         ("illustrative: the lots (DataSF parcels, block 0836 lots 008, 009 and 013) less the tower, at the podium "
          f"height in the {PACKET['title']}, draft Downtown Project Authorization, PDF p. 60, and its plans, PDF "
          "pp. 110-113"),
         ("A five-story podium, 68 ft to the roof (2020 approval), over the whole site: about 84,815 sq ft for the "
          "International High School of the French American International School and about 3,229 sq ft of retail. "
          "Its roof terraces, including the lower one at the Market Street end, aren't drawn.")),
        ("Tower", tower, TOWER_ROOF_FT, "Homes (345 in the building)",
         (f"illustrative: the lower tower floor outline from the {plan}, registered to the parcel corners; roof "
          "height from the same packet (PDF pp. 41 and 110) and the Planning Commission minutes of May 28, 2020"),
         ("Roof at 365 ft, 36 stories; 396 ft 8 in to the top of the rooftop screen (2020 approval, Motion 20728). "
          "The faceted outline is the lower tower floor; the upper third of the tower is about 5 percent smaller. "
          "A 2023 modification to a 400-ft, 38-story building is described in the project's record but isn't "
          "drawn.")),
    ]
    features = []
    for label, geom, h, use, source, note in parts:
        wgs = gpd.GeoSeries([geom], crs=UTM).to_crs(4326).iloc[0]
        feature = {
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        }
        if not shape(ob._round(feature)["geometry"]).is_valid:
            raise SystemExit(f"98 Franklin: the {label.lower()} polygon is invalid after rounding")
        features.append(feature)

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the 365-ft tower and 68-ft podium approved in 2020, as two simple "
                        "volumes. The tower's faceted outline is the lower tower floor from the approved plans, "
                        "registered to the parcel corners; the 396-ft rooftop screen and the podium's terraces "
                        "aren't drawn. A 2023 modification to a 400-ft tower isn't drawn."),
            "note": "The 2020 approved heights on simple volumes, not the final design.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2020: plans and draft motions (PDF)",
            "heightSourceUrl": MINUTES_2020,
            "georeference": {
                "plan": sim.report(),
                "method": ("The plan's three property-line corners matched to the DataSF parcel corners "
                           "(least-squares similarity)."),
            },
            "license": ("Tower outline: traced from a public SF Planning document. Lots: DataSF parcels "
                        "(ODC-PDDL)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[98-franklin] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
