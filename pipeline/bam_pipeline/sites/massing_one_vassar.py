"""One Vassar: the three approved buildings, traced from the plan set's typical tower plans.

Sources:
- Planning Commission packet for Record No. 2012.1384 (One Vassar, hearing Feb 20, 2020), PDF page 159: the
  architects' "Typical tower plans" sheet (Exhibit C, sheet 8, 1" = 50'-0"), a vector drawing of the whole site with
  the three towers' typical floors over the ground-level outlines of 400 2nd Street (Building 1), the existing
  building at 645 Harrison Street (Building 2) and 657 Harrison Street (Building 3).
- The same packet's draft Large Project Authorization (PDF pp. 19-20, 70-71) and the executive summary (p. 15):
  Building 1 "a 350-foot tall (or 385-feet tall with the rooftop mechanical equipment), 27-story office building"
  whose "podium along all facades will have a height of 85 feet"; Building 2 "a 15-story vertical addition for a total
  height of 200-ft" whose podium "will have a height of 55 feet, which is the height of the existing structure";
  Building 3 "a 350-foot tall (or 385 feet with the rooftop mechanical equipment), 35-story residential building"
  whose "podium along all facades will have a height of 85 feet". The bulk diagram (p. 160) gives the typical tower
  floor plates as 14,935 sq ft (400 2nd), 16,000 sq ft (645 Harrison) and 12,000 sq ft (657 Harrison).
- Planning Commission minutes of Feb 20, 2020: approved as Motions 20665 (Large Project Authorization), 20666
  (office allocation) and 20667 (hotel conditional use).

How it's drawn:
- Page 159 is registered to the DataSF parcels of the site (the boundary file) by a least-squares similarity on six
  lot corners the drawing shows: the four corners of the 645 Harrison Street building that the plan draws on its lot
  lines (lot 105), the Harrison Street / Vassar Place corner of 400 2nd Street (lot 001), and the Harrison Street and
  Perry Street corners of 657 Harrison Street's west lot line (lots 099 and 081). The RMS is reported.
- Building 1: the ground-level outline (with the 15-ft setback at the 2nd and Harrison corner) at the 85-ft podium
  height, less the tower; the tower is the typical office floor (blue) at 350 ft.
- Building 2: the hotel addition is the typical hotel floor outline (purple), drawn from the top of the existing
  four-story building (55 ft) to 200 ft. The existing building, which the project keeps, is left to the base map.
- Building 3: the ground-level outline at the 85-ft podium height, less the tower; the tower is the rectangle of the
  typical residential floor (yellow units and their corner columns) at 350 ft.
- Roof heights are drawn; rooftop mechanical screens (to 385, 215 and 385 ft) are not. The setbacks within the
  podiums and the hotel's recessed fifth-floor lobby are not modelled. Illustrative.

Stage: approved in 2020; DBI approved the site permits for 400 2nd Street (June 23, 2023) and 657 Harrison Street
(Nov 13, 2023) but has issued none, and no demolition permit has been issued. All volumes are drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_one_vassar
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import Polygon, box, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "one-vassar"
UTM = ob.UTM
SQFT = 10.7639

PACKET = {
    "title": "Planning Commission packet, Record No. 2012.1384 (One Vassar), hearing Feb 20, 2020",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2012.1384PRJ.pdf",
    "sha256": "5d42b2f62742f5262c215cc681ce2fa223482edc6ea72515d0e9c12d6ea8d280",
    "file": "2012.1384PRJ.pdf",
    "plan_page": 159,
}
MINUTES_URL = "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200220_cal_min.pdf"

WHITE = (0.0, 0.0, 0.0, 0.0)
BLUE = (0.323, 0.0, 0.024, 0.0)  # Building 1 typical office floor
YELLOW = (0.09, 0.075, 0.382, 0.0)  # Building 3 units
GREY = (0.75, 0.679, 0.671, 0.901)  # Building 3 ground-level outline (stroke)

# Expected bounding boxes (x0, top, x1, bottom), PDF points, of the shapes read from page 159.
BBOX = {
    "b1_ground": (825.5, 257.3, 1046.8, 485.0),
    "b1_tower": (875.6, 278.6, 1022.5, 484.9),
    "b2_existing": (445.7, 257.3, 769.1, 487.0),
    "b2_hotel": (457.3, 369.0, 756.4, 480.3),
    "b3_ground": (183.8, 257.3, 396.1, 486.1),
    "b3_tower": (218.2, 279.8, 350.8, 462.7),
}

# Lot corners shown on page 159 (PDF points, y down) and, for each, the lot and a point near that corner of it in
# UTM 10N; the code snaps the point to the nearest vertex of that lot.
CONTROLS = [
    ("645 Harrison: Harrison St / west lot line (lot 105)", (445.7, 257.3), "3763105", (553168.1, 4181946.3)),
    ("645 Harrison: Harrison St / Vassar Place (lot 105)", (769.1, 257.3), "3763105", (553216.4, 4181994.9)),
    ("645 Harrison: west lot line / rear (lot 105)", (445.7, 487.0), "3763105", (553203.0, 4181911.7)),
    ("400 2nd: Harrison St / Vassar Place (lot 001)", (825.5, 257.3), "3763001", (553225.0, 4182003.6)),
    ("657 Harrison: Harrison St / west lot line (lot 099)", (183.8, 257.3), "3763099", (553128.8, 4181906.9)),
    ("657 Harrison: Perry St / west lot line (lot 081)", (184.0, 486.1), "3763081", (553163.8, 4181872.3)),
]


def _close(a, b, tol=0.002) -> bool:
    return isinstance(a, (list, tuple)) and len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def _bbox_ok(o, want, tol=1.5) -> bool:
    return all(abs(v - w) <= tol for v, w in zip((o["x0"], o["top"], o["x1"], o["bottom"]), want))


def _poly(o) -> Polygon:
    return shapely.make_valid(Polygon(o["pts"])).buffer(0)


def read_plan(page) -> dict[str, Polygon]:
    shapes = page.rects + page.curves
    found: dict[str, Polygon] = {}

    def pick(key, test):
        hits = [o for o in shapes if test(o) and _bbox_ok(o, BBOX[key])]
        if not hits:
            raise SystemExit(f"page {PACKET['plan_page']}: no shape for {key} at {BBOX[key]}")
        found[key] = _poly(hits[0])

    pick("b1_ground", lambda o: o.get("fill") and _close(o.get("non_stroking_color"), WHITE) and len(o["pts"]) == 7)
    pick("b1_tower", lambda o: o.get("fill") and _close(o.get("non_stroking_color"), BLUE))
    pick("b2_existing", lambda o: o.get("fill") and _close(o.get("non_stroking_color"), WHITE))
    pick("b2_hotel", lambda o: o.get("fill") and _close(o.get("non_stroking_color"), WHITE) and len(o["pts"]) == 9)
    pick("b3_ground", lambda o: o.get("stroke") and _close(o.get("stroking_color"), GREY) and len(o["pts"]) == 15)
    # Building 3's tower: the rectangle around its units (yellow fills west of Hawthorne Street Plaza).
    units = [o for o in shapes if o.get("fill") and _close(o.get("non_stroking_color"), YELLOW) and o["x1"] < 400]
    x0, top = min(o["x0"] for o in units), min(o["top"] for o in units)
    x1, bottom = max(o["x1"] for o in units), max(o["bottom"] for o in units)
    if not all(abs(v - w) <= 1.5 for v, w in zip((x0, top, x1, bottom), BBOX["b3_tower"])):
        raise SystemExit(f"page {PACKET['plan_page']}: Building 3's units span {(x0, top, x1, bottom)}")
    found["b3_tower"] = box(x0, top, x1, bottom)
    return found


def fit_plan(fc: dict) -> trace.Similarity:
    lots = {}
    for f in fc["features"]:
        g = gpd.GeoSeries([shapely.make_valid(shape(f["geometry"]))], crs=4326).to_crs(UTM).iloc[0]
        lots[f["properties"]["blklot"]] = shapely.get_coordinates(g.boundary)
    src, dst, labels = [], [], []
    for label, fig, lot, near in CONTROLS:
        v = lots[lot]
        d = np.linalg.norm(v - np.array(near), axis=1)
        if d.min() > 3:
            raise SystemExit(f"no vertex of lot {lot} within 3 m of the control '{label}'")
        src.append(fig)
        dst.append(v[d.argmin()])
        labels.append(label)
    return trace.fit_similarity(np.array(src, float), np.array(dst, float), labels)


def main() -> None:
    pdf = trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    with pdfplumber.open(pdf) as doc:
        plan = read_plan(doc.pages[PACKET["plan_page"] - 1])

    fc_lots = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    sim = fit_plan(fc_lots)
    ft_per_pt = sim.scale / 0.3048
    print(f"[one-vassar] page {PACKET['plan_page']} -> parcels: RMS {sim.rms_m:.2f} m over {len(CONTROLS)} lot corners, "
          f"scale {ft_per_pt:.4f} ft/pt (drawing scale 1\" = 50' is {50 / 72:.4f})")

    utm = {k: shapely.make_valid(sim.geometry(g)).buffer(0) for k, g in plan.items()}
    b1_tower, b2_hotel, b3_tower = utm["b1_tower"], utm["b2_hotel"], utm["b3_tower"]
    b1_podium = utm["b1_ground"].difference(b1_tower.buffer(0.05))
    b3_podium = utm["b3_ground"].difference(b3_tower.buffer(0.05))
    site = ob._utm_shapes(fc_lots).union_all()
    for name, g in [("400 2nd tower", b1_tower), ("400 2nd podium", b1_podium), ("645 Harrison hotel", b2_hotel),
                    ("657 Harrison tower", b3_tower), ("657 Harrison podium", b3_podium)]:
        off = g.difference(site.buffer(1.0)).area
        print(f"[one-vassar] {name}: {g.area * SQFT:,.0f} sq ft, {off * SQFT:,.0f} sq ft outside the lots")

    src = f"{PACKET['title']}, PDF p. {PACKET['plan_page']} (typical tower plans)"
    motion = f"{PACKET['title']}, draft Large Project Authorization (PDF pp. 19-20, 70-71), approved as Motion 20665"
    parts = [
        ("400 2nd Street tower", b1_tower, 350, 0, "Office (about 430,000 gross sq ft)",
         f"illustrative: the typical office floor traced from the {src}; roof height from the {motion}",
         "Building 1: a 27-story office building, 350 ft to the roof and 385 ft with the rooftop mechanical "
         "equipment. Typical tower floor about 14,935 sq ft (packet p. 160)."),
        ("400 2nd Street podium", b1_podium, 85, 0, "Office, with shops and an indoor public open space",
         f"illustrative: the ground-level outline traced from the {src}, less the tower, at the 85-ft podium height "
         f"in the {motion}",
         "The 85-ft podium of Building 1, set back 15 ft at the corner of 2nd and Harrison streets."),
        ("645 Harrison Street hotel addition", b2_hotel, 200, 55, "Hotel (468 rooms)",
         f"illustrative: the typical hotel floor traced from the {src}; heights from the {motion}",
         "Building 2: a 15-story hotel addition on the existing four-story building at 645 Harrison Street, which "
         "the project keeps (its 55-ft roof is the addition's base); 200 ft to the roof, 215 ft with the mechanical "
         "screen. The existing building, with office, PDR and new retail space, is not drawn."),
        ("657 Harrison Street tower", b3_tower, 350, 0, "Homes (489)",
         f"illustrative: the rectangle of the typical residential floor traced from the {src}; roof height from "
         f"the {motion}",
         "Building 3: a 35-story residential building, 350 ft to the roof and 385 ft with the rooftop mechanical "
         "equipment. Typical tower floor about 12,000 sq ft (packet p. 160)."),
        ("657 Harrison Street podium", b3_podium, 85, 0, "Homes, child care and shops",
         f"illustrative: the ground-level outline traced from the {src}, less the tower, at the 85-ft podium height "
         f"in the {motion}",
         "The 85-ft podium of Building 3, with a 14,000 sq ft child care center, beside the new Hawthorne Street "
         "Plaza."),
    ]
    features = []
    for label, geom, h, base, use, source, note in parts:
        wgs = gpd.GeoSeries([geom.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": base, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the three approved buildings traced from the 2020 plan set's typical "
                        "tower plans and drawn to the roof heights in the approval: a 350-ft office tower on an 85-ft "
                        "podium at 2nd and Harrison streets, a 200-ft hotel addition on the existing four-story "
                        "building at 645 Harrison Street, and a 350-ft residential tower on an 85-ft podium at 657 "
                        "Harrison Street. Rooftop screens, podium setbacks and the existing building are not drawn."),
            "note": "The approved buildings as simple volumes at their roof heights, not the final designs.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2020 (PDF)",
            "approvalSourceUrl": MINUTES_URL,
            "georeference": {
                "page_159": sim.report(),
                "feet_per_point": round(ft_per_pt, 4),
                "method": ("Six lot corners drawn on the plan (lots 105, 001, 099 and 081) matched to DataSF parcel "
                           "vertices by a least-squares similarity."),
            },
            "license": ("Footprints: traced from a public SF Planning document. Georeference: DataSF parcels "
                        "(ODC-PDDL)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[one-vassar] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
