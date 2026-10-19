"""One Oak (1500-1540 Market Street): the approved podium and tower as two simple volumes.

Sources:
- Heights and program from the latest approval, the Planning Commission's hearing of March 19, 2026 (case
  2024-005509; agenda items 7a-7e, PDF pp. 4-5): "a new, approximately 508,000-square-foot residential building
  with a tower over podium design containing 541 dwelling units. The podium portion of the building is 14
  stories high, with a roof height of approximately 139 feet, while the tower extends to 41 stories, reaching a
  roof height of 400 feet (or approximately 416 feet inclusive of mechanical equipment, and 436 feet tall
  inclusive of elevator overrun and rooftop screening)". SF Planning's project record (DataSF qvu5-m3a2,
  2024-005509PRJ) gives the decision as approved on 2026-03-19.
- The tower's position and outline from the only dimensioned plans that could be opened: the plans approved in
  2017 (Snøhetta, May 15, 2017), Exhibit B of the Planning Commission packet for Record No. 2009.0159PRJ (hearing
  Jan 16, 2020), PDF p. 52, "Amenity plan level 14", a vector drawing with the property lines dimensioned
  (177'-0" on Oak Street, 39'-2" on Van Ness Avenue, 218'-1 1/2" on Market Street, 166'-8" on the west side).
  The 2026 plans are in a packet on a host this pipeline can't reach. SF Planning's interdepartmental review
  record (2024-005509PRV) says the 2026 changes "increase the footprint (and massing) of both the podium and
  the tower", so the real tower is larger than the 2017 outline drawn here.

How it's drawn:
- The four property-line corners at the ends of the plan's dimension lines are matched to the corners of the
  DataSF parcels (block 0836 lots 001-005, the boundary file) by a least-squares similarity; the RMS is reported.
- Tower: the level-14 floor of the 2017 plans (the union of its filled rooms, cores and corridors, about 9,200 sq
  ft; Motion 19943 gives the 2017 tower's average floor as 9,637 sq ft), carried to the map and extruded from the
  ground to the 400-ft roof. The crown, mechanical screen and elevator overrun (to 436 ft) aren't drawn.
- Podium: the rest of the lots at 139 ft. The podium's real outline, its terraces and the Oak Plaza in the
  street aren't drawn. Illustrative.

Stage: approved (March 19, 2026); no construction permit has been issued (DBI site permit application
201612094535, for the 2017 design, is still "filed"), so both volumes are drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_one_oak
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

PROJECT_ID = "one-oak"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639
PT_PER_FT = 72 / 20  # the plan's scale, 1" = 20'-0"

PACKET = {
    "title": "Planning Commission packet, Record No. 2009.0159PRJ (1540 Market Street, aka One Oak), hearing Jan 16, 2020",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2009.0159DNXCUA-02.pdf",
    "sha256": "90c172781a4b90481f3423ce03cb123c97f7afda02e40a7b845707452177411a",
    "file": "2009.0159DNXCUA-02.pdf",
    "page": 52,
}
AGENDA_2026 = "https://sfplanning.org/sites/default/files/agendas/2026-03/20260319_cpc%20%28ID%201559820%29.pdf"

# Property-line corners on PDF p. 52 (points, y down), at the ends of the dimension lines' extension lines,
# each with a point near the same corner of the parcels (UTM 10N); the code snaps to the nearest parcel vertex.
CORNERS = [
    ("Oak Street, west end of the site (lot 005)", (283.50, 91.73), (551067.8, 4181036.4)),
    ("Oak Street and Van Ness Avenue (lot 001)", (921.66, 91.73), (551120.9, 4181045.2)),
    ("Van Ness Avenue and Market Street (lot 001)", (921.66, 233.03), (551122.9, 4181033.0)),
    ("Market Street, west end of the site (lot 005)", (283.50, 692.60), (551076.2, 4180985.9)),
]
# Plan dimensions between those corners, in feet, to check the reading of the sheet.
PLAN_DIMS_FT = {"Oak Street": 177.0, "Van Ness Avenue": 39 + 2 / 12, "west side": 166 + 8 / 12}

# Fill colours (RGB) of the level-14 floor plate: amenity rooms, corridors, stairs, cores, columns, glazing.
TOWER_FILLS = [
    (0.738, 0.93, 0.859), (1.0, 1.0, 0.836), (0.48, 0.563, 0.684), (0.5, 0.5, 0.5),
    (0.84, 0.84, 0.84), (0.131, 0.122, 0.123), (0.844, 0.891, 0.91),
]
TOWER_BOX = (380, 90, 870, 495)  # x0, top, x1, bottom on the sheet: the floor plate, not the legend
TOWER_AREA_PT2 = (110_000, 125_000)  # expected outline area, as a check against a changed PDF

TOWER_ROOF_FT = 400
PODIUM_FT = 139


def tower_outline_pt(page) -> Polygon:
    polys = []
    for o in page.curves + page.rects:
        c = o.get("non_stroking_color")
        if not o.get("fill") or c is None or len(c) != 3:
            continue
        if not any(max(abs(a - b) for a, b in zip(c, k)) < 0.01 for k in TOWER_FILLS):
            continue
        x0, top, x1, bottom = TOWER_BOX
        if o["x0"] < x0 or o["x1"] > x1 or o["top"] < top or o["bottom"] > bottom:
            continue
        pts = o.get("pts") or [(o["x0"], o["top"]), (o["x1"], o["top"]), (o["x1"], o["bottom"]), (o["x0"], o["bottom"])]
        if len(pts) >= 3:
            g = shapely.make_valid(Polygon(pts))
            if g.area > 0:
                polys.append(g)
    u = shapely.union_all([g.buffer(1.5) for g in polys]).buffer(-1.5)
    plate = Polygon(trace.largest_polygon(u).exterior)
    if not TOWER_AREA_PT2[0] <= plate.area <= TOWER_AREA_PT2[1]:
        raise SystemExit(f"One Oak: level-14 outline is {plate.area:,.0f} sq pt, outside the expected range")
    return plate


def check_dims() -> None:
    (_, nw, _), (_, ne, _), (_, se, _), (_, sw, _) = CORNERS
    got = {"Oak Street": ne[0] - nw[0], "Van Ness Avenue": se[1] - ne[1], "west side": sw[1] - nw[1]}
    for k, pt in got.items():
        ft = pt / PT_PER_FT
        if abs(ft - PLAN_DIMS_FT[k]) > 1.0:
            raise SystemExit(f"One Oak: {k} reads {ft:.1f} ft on the sheet, plan says {PLAN_DIMS_FT[k]:.1f} ft")


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
            raise SystemExit(f"One Oak: no parcel vertex within 3 m of '{label}'")
        src.append(fig)
        dst.append(vertices[d.argmin()])
        labels.append(label)
    return trace.fit_similarity(np.array(src, float), np.array(dst, float), labels)


def main() -> None:
    pdf = trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    check_dims()
    with pdfplumber.open(pdf) as doc:
        plate_pt = tower_outline_pt(doc.pages[PACKET["page"] - 1])

    lot = lots_utm()
    sim = fit(lot)
    print(f"[one-oak] plan p. {PACKET['page']} -> parcels: RMS {sim.rms_m:.2f} m over {len(CORNERS)} corners, "
          f"scale {sim.scale / FT:.4f} ft/pt (plan 1\" = 20' gives {1 / PT_PER_FT:.4f})")

    tower = shapely.make_valid(sim.geometry(plate_pt)).buffer(0)
    off = tower.difference(lot.buffer(0.5)).area
    tower = tower.intersection(lot)
    podium = lot.difference(tower)
    print(f"[one-oak] lots {lot.area * SQFT:,.0f} sq ft; tower {tower.area * SQFT:,.0f} sq ft "
          f"({off * SQFT:,.0f} sq ft trimmed outside the lots); podium {podium.area * SQFT:,.0f} sq ft")

    plan = f"{PACKET['title']}, Exhibit B (plans approved in 2017), PDF p. {PACKET['page']} (amenity plan level 14)"
    parts = [
        ("Podium", podium, PODIUM_FT, "Homes, lobby, leasing office and community room, parking entry",
         ("illustrative: the lots (DataSF parcels, block 0836 lots 001-005) less the tower, at the podium height on "
          "the Planning Commission agenda of March 19, 2026 (case 2024-005509, PDF p. 4)"),
         ("A 14-story podium about 139 ft tall (2026 approval). Its real outline, terraces and setbacks aren't "
          "drawn.")),
        ("Tower", tower, TOWER_ROOF_FT, "Homes (541 in the building)",
         (f"illustrative: the level-14 floor outline of the 2017 plans, from the {plan}, registered to the parcel "
          "corners; roof height from the Planning Commission agenda of March 19, 2026 (PDF p. 4)"),
         ("Roof at 400 ft, 41 stories; about 416 ft with mechanical equipment and 436 ft with the elevator overrun "
          "and rooftop screening (2026 approval). The outline is the 2017 design's; the 2026 approval enlarged the "
          "tower's footprint, so the real tower is wider than drawn.")),
    ]
    features = []
    for label, geom, h, use, source, note in parts:
        wgs = gpd.GeoSeries([geom.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the 400-ft tower and 139-ft podium approved in 2026, as two simple "
                        "volumes. The tower is placed and shaped from the plans approved in 2017 (the 2026 plans "
                        "couldn't be opened); the 2026 approval enlarged the tower's footprint, so the real tower is "
                        "wider than drawn. The crown and screening to 436 ft aren't drawn."),
            "note": "The approved heights on simple volumes; the tower outline is from the earlier, smaller design.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2020: plans approved in 2017 (PDF)",
            "heightSourceUrl": AGENDA_2026,
            "georeference": {
                "plan": sim.report(),
                "method": ("The plan's four property-line corners matched to the DataSF parcel corners "
                           "(least-squares similarity)."),
            },
            "license": ("Tower outline: traced from a public SF Planning document. Lots: DataSF parcels "
                        "(ODC-PDDL)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[one-oak] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
