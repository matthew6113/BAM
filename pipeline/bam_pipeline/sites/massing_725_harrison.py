"""725-765 Harrison Street: the approved 14-story office building, traced from the 2019 plan set's floor plans.

Sources:
- Planning Commission packet for Record No. 2005.0759ENX/OFA/VAR-02 (725 Harrison Street, hearing Dec 12, 2019),
  Exhibit G, the architects' plans dated for the Dec 12, 2019 hearing: floor plans at 3/64" = 1'-0" on 34 x 22 in
  sheets A20 to A26 (PDF pp. 361-367, two plans a sheet), with the office floors filled in light blue. The plans are
  scanned line work (raster images); the blue floor fill is traced from a 144-dpi render. The building section (PDF
  p. 356) gives the floor levels: level 7 at 80'-1", level 11 at 132'-1", level 14 at 171'-1" and the roof at
  185'-0" ("height limit"), with mechanical screens to 205'-0" (west) and 196'-6" (east).
- The same packet's draft Large Project Authorization (PDF pp. 242-243): "new construction of a 14-story, 185-ft tall,
  mixed-use building approximately 935,000 gross square feet in total"; "one structure that has two separate massing
  components: the larger, oblong-shaped structure with the massing towards Harrison and Fourth Streets (western
  portion), and a smaller spheroid-shaped structure with the massing running diagonally from Harrison to Perry Streets
  fronting the mid-block paseo (eastern portion)"; Phase I is the western portion.
- Planning Commission minutes of Dec 12, 2019 (approved, 20597 and 20598) and of June 16, 2022 (Motion 21128, which
  modified the approval to take in lot 113 at 759 Harrison Street, for a "14-story, 185-foot tall mixed-use building
  of approximately 981,000 gsf in total"). The 2022 plans are on a host this pipeline can't reach, so the 2019 plans
  are drawn; they leave out lot 113, which the 2022 design takes in.

How it's drawn:
- The plans share one sheet layout. Each is registered to the DataSF parcels by a least-squares similarity on three
  points on its property lines: the corners at 4th and Harrison streets and at 4th and Perry streets (lot 152), and
  the middle of the Harrison Street frontage of lot 113 (759 Harrison Street), the centre of the notch the plans
  leave around it. The RMS is reported.
- Four tiers, each drawn at the height of the floor where the next one begins: level 3 (the full floors 2 to 6) to
  80 ft, level 7 (floors 7 to 10) to 132 ft, level 11 (floors 11 to 13) to 171 ft and level 14 to the 185-ft roof.
  Each tier is split at the notch into the western (Phase I) and eastern (Phase II) parts. Ground-floor open spaces,
  terraces and the rooftop mechanical screens are not modelled. Illustrative.
- The lot to be given to the City for affordable housing (lot 149) has no design, so nothing is drawn on it.

Stage: approved in 2019 and modified in 2022; the approvals were extended to March 24, 2028 (record 2005.0759ENX-03,
closed approved Sept 29, 2026). No site permit has been issued, so all volumes are "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_725_harrison
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, box, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "725-harrison"
UTM = ob.UTM
SQFT = 10.7639
SCALE = 2  # render at 144 dpi: 6.75 px to the foot at 3/64" = 1'-0"

PACKET = {
    "title": "Planning Commission packet, Record No. 2005.0759ENX/OFA/VAR-02 (725 Harrison Street), hearing Dec 12, 2019",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2005.0759ENXOFAVAR.pdf",
    "sha256": "0d7057a75291e4197726b577a2db201d69df3f3d44e37977900084254354b980",
    "file": "2005.0759ENXOFAVAR.pdf",
}
MINUTES_URL = "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20220616_cal_min.pdf"
LOT_113 = ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot = '3762113'")  # retired in 2022, merged into lot 152

BLUE = (185, 220, 255)  # office floor fill
# Each sheet holds two plans, the upper one 1440 px (720 pt) above the lower one at this render scale.
SHEET_SHIFT = 1440
# Floor plates: (sheet page, upper or lower plan, level).
PLANS = {
    "L3": (361, "lower", "level 3 (floors 2 to 6 are the same)"),
    "L7": (363, "lower", "level 7"),
    "L11": (365, "lower", "level 11"),
    "L14": (367, "upper", "level 14"),
}
# Property-line points in the lower plan (px at SCALE, y down): read from the render, where the 4th Street property
# line is the dashed line at x = 455.5, the Perry Street property line the dashed line at y = 2834 and the Harrison
# Street frontage the line at y = 1755.5; the notch the plans leave around lot 113 runs from x = 2628 to 2845.
CONTROLS = [
    ("4th and Harrison streets (lot 152)", (455.5, 1755.5), "3762152", (552886.7, 4181663.4)),
    ("4th and Perry streets (lot 152)", (455.5, 2834.0), "3762152", (552921.5, 4181628.9)),
    ("Harrison Street frontage of lot 113, midpoint", (2736.5, 1755.5), "3762113", None),
]
SPLIT_X = 2736.5  # Phase I (west) | Phase II (east), through the middle of the notch
# A point inside the eastern core (stairs, elevators), which the blue fill leaves out and which sits on the edge of
# the eastern floors from level 7 up: the core is the hollow between the level-14 eastern floor and its convex hull
# that holds this point, and it is added to every plate.
EAST_CORE_POINT = (3075, 2255)


def _valid(g):
    """A valid polygon without slivers: a tiny mitred inward and outward buffer."""
    g = shapely.make_valid(g).buffer(0)
    return g.buffer(-0.01, join_style="mitre").buffer(0.01, join_style="mitre")


def _clean(g, open_px: float, min_area: float):
    """Drop strips narrower than 2 x open_px and parts smaller than min_area (px and px²)."""
    if open_px:
        g = g.buffer(-open_px, join_style="mitre").buffer(open_px, join_style="mitre")
    parts = [p for p in getattr(_valid(g), "geoms", [_valid(g)]) if isinstance(p, Polygon) and p.area >= min_area]
    return _valid(shapely.union_all(parts)) if parts else Polygon()


def render(pdf_path, page: int) -> np.ndarray:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    return np.asarray(doc[page - 1].render(scale=SCALE).to_pil().convert("RGB"))


def floor_plate(rgb: np.ndarray, half: str):
    """The blue floor plate of one plan, outer outline only (cores and text closed over), in lower-plan px."""
    import cv2

    mask = (np.abs(rgb.astype(int) - np.array(BLUE)).max(axis=2) <= 12).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    parts = []
    for c in contours:
        shell = cv2.approxPolyDP(c, 2.0, True).reshape(-1, 2)
        if len(shell) < 3:
            continue
        p = shapely.make_valid(Polygon(shell))
        if p.area < 20000:
            continue
        cy = p.centroid.y
        if (half == "upper" and cy < 1500) or (half == "lower" and 1500 <= cy < 3000):
            parts.append(p)
    if not parts:
        raise SystemExit(f"no floor plate found in the {half} plan")
    plate = shapely.union_all(parts)
    if half == "upper":
        plate = shapely.affinity.translate(plate, 0, SHEET_SHIFT)
    return _valid(plate)


def fit(fc: dict, lot113: dict) -> trace.Similarity:
    lots = {}
    for f in fc["features"] + lot113["features"]:
        g = gpd.GeoSeries([shapely.make_valid(shape(f["geometry"]))], crs=4326).to_crs(UTM).iloc[0]
        lots[f["properties"]["blklot"]] = g
    src, dst, labels = [], [], []
    for label, fig, lot, near in CONTROLS:
        g = lots[lot]
        if near is None:  # the midpoint of lot 113's Harrison Street frontage: its two most north-westerly vertices
            v = shapely.get_coordinates(g.exterior if g.geom_type == "Polygon" else g.geoms[0].exterior)[:-1]
            score = v[:, 1] - v[:, 0]  # north-west is +y, -x
            front = v[np.argsort(-score)[:2]]
            point = front.mean(axis=0)
        else:
            v = shapely.get_coordinates(g.boundary)
            d = np.linalg.norm(v - np.array(near), axis=1)
            if d.min() > 3:
                raise SystemExit(f"no vertex of lot {lot} within 3 m of the control '{label}'")
            point = v[d.argmin()]
        src.append(fig)
        dst.append(point)
        labels.append(label)
    return trace.fit_similarity(np.array(src, float), np.array(dst, float), labels)


def main() -> None:
    pdf = trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    plates = {}
    for key, (page, half, _) in PLANS.items():
        plates[key] = floor_plate(render(pdf, page), half)
    east14 = plates["L14"].intersection(box(SPLIT_X, -1e5, 1e5, 1e5))
    hollows = shapely.convex_hull(east14).difference(east14)
    core = next((p for p in getattr(hollows, "geoms", [hollows]) if p.contains(shapely.Point(EAST_CORE_POINT))), None)
    if core is None:
        raise SystemExit("the eastern core wasn't found next to the level-14 floor")
    core = _clean(core, 6.0, 0)
    print(f"[725-harrison] eastern core: {core.area / (SCALE * 3.375) ** 2:,.0f} sq ft")
    for key, (page, half, _) in PLANS.items():
        plates[key] = _valid(plates[key].union(core))
        print(f"[725-harrison] {key} (p. {page}, {half} plan): {plates[key].area / (SCALE * 3.375) ** 2:,.0f} sq ft "
              "with the eastern core")

    fc_lots = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    lot113 = ob.fetch(f"{PROJECT_ID}-lot113", LOT_113)
    sim = fit(fc_lots, lot113)
    ft_per_px = sim.scale / 0.3048
    print(f"[725-harrison] plans -> parcels: RMS {sim.rms_m:.2f} m over {len(CONTROLS)} points, scale {ft_per_px:.4f} "
          f"ft/px (drawing scale 3/64\" = 1'-0\" at {SCALE * 72} dpi is {1 / (SCALE * 3.375):.4f})")
    for lower, upper in [("L3", "L7"), ("L7", "L11"), ("L11", "L14")]:
        out = plates[upper].difference(plates[lower]).area / (SCALE * 3.375) ** 2
        print(f"[725-harrison] {upper} outside {lower}: {out:,.0f} sq ft")

    tiers = [  # (plate, the plate above it, roof of this tier in ft, floors)
        ("L3", "L7", 80, "floors 1 to 6"),
        ("L7", "L11", 132, "floors 7 to 10"),
        ("L11", "L14", 171, "floors 11 to 13"),
        ("L14", None, 185, "floor 14"),
    ]
    west = box(-1e5, -1e5, SPLIT_X, 1e5)
    east = box(SPLIT_X, -1e5, 1e5, 1e5)
    site = ob._utm_shapes(fc_lots).union_all()
    src = f"{PACKET['title']}, PDF pp. 361-367 (floor plans, sheets A20-A26)"
    motion = (f"{PACKET['title']}, draft Large Project Authorization (PDF pp. 242-243) and building section (PDF p. 356), "
              "approved Dec 12, 2019 and modified June 16, 2022 (Motion 21128)")
    px_sqft = (SCALE * 3.375) ** 2  # px² in a square foot
    features = []
    for key, above, h, floors in tiers:
        # The part of this plate outside the one above; strips under about 2 ft wide, where the two outlines run
        # together, are dropped rather than drawn as slivers.
        ring = plates[key] if above is None else plates[key].difference(plates[above].buffer(6.0))
        ring = _clean(ring, 6.0, 100 * px_sqft)
        for side, half, phase, use in [
            ("west", west, "Phase I", "Office, with PDR space, shops and an indoor public open space"),
            ("east", east, "Phase II", "Office, with PDR space and a child care center"),
        ]:
            part = _clean(ring.intersection(half), 0.0, 100 * px_sqft)
            if part.is_empty:
                continue
            geom = _valid(sim.geometry(part))
            off = geom.difference(site.buffer(1.0)).area
            name = "Western building" if side == "west" else "Eastern building"
            label = f"{name}, {floors}"
            print(f"[725-harrison] {label}: {geom.area * SQFT:,.0f} sq ft, {h} ft, {off * SQFT:,.0f} sq ft outside the lots")
            wgs = gpd.GeoSeries([_valid(geom.simplify(0.3))], crs=UTM).to_crs(4326).iloc[0]
            features.append({
                "type": "Feature",
                "properties": {
                    "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                    "base_ft": 0, "use": use, "phase": phase, "illustrative": True,
                    "source": (f"illustrative: the {PLANS[key][2]} floor plate traced from the {src}; heights from the "
                               f"{motion}"),
                    "note": (f"The {side}ern part of the 14-story, 185-ft office building ({phase}), {floors}, drawn as "
                             f"the {PLANS[key][2]} plate up to {h} ft." if above else
                             f"The top floor of the {side}ern part of the building ({phase}), up to the 185-ft roof; "
                             f"the mechanical screen above it rises to {'205' if side == 'west' else '196.5'} ft."),
                },
                "geometry": mapping(wgs),
            })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the approved 14-story, 185-ft office building traced from the floor "
                        "plates of the December 2019 plan set, in four tiers that step back from Harrison Street, its "
                        "western (Phase I) and eastern (Phase II) parts split at 759 Harrison Street. The 2022 "
                        "modification takes in that lot, which these 2019 plans leave out; its plans weren't "
                        "available. Terraces, open spaces and mechanical screens are not drawn, and nothing is drawn "
                        "on the affordable housing lot."),
            "note": "The approved building as simple volumes at its floor and roof heights, not the final design.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2019 (PDF)",
            "approvalSourceUrl": MINUTES_URL,
            "georeference": {
                "floor_plans": sim.report(),
                "feet_per_px": round(ft_per_px, 4),
                "render_dpi": SCALE * 72,
                "method": ("The 4th Street, Harrison Street and Perry Street property lines of the plans and the notch "
                           "around lot 113 matched to DataSF parcel vertices (lot 152, and lot 113 before its 2022 "
                           "merger) by a least-squares similarity."),
            },
            "license": ("Footprints: traced from a public SF Planning document. Georeference: DataSF parcels "
                        "(ODC-PDDL)."),
        },
        "features": features,
    }
    for f in fc["features"]:
        if not shape(f["geometry"]).is_valid:
            raise SystemExit(f"invalid geometry: {f['properties']['label']}")
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[725-harrison] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
