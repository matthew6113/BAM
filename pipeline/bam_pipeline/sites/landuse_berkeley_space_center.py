"""Berkeley Space Center at NASA Research Park: land-use zones from the project's land use plan.

The joint EIR/EIS (UC Berkeley and NASA, Final Aug 2026, CEQAnet SCH 2024060942) studies a development
envelope, not a building design: seven Subareas with maximum floor area by use (Final EIR/EIS Table
2-6, PDF p. 233) and maximum heights (Table 2-4, p. 2-19: 80 ft in all Subareas but Subarea 7, which
is 30 ft, plus up to 25 ft of mechanical screens; a 15-ft stepback above 35 ft along Wescoat and Cody
Roads in Subareas 1, 2, 3 and 6). The plans "are conceptual until after project approval", and "the
number and configuration of buildings" may vary (Table 2-5). So the map draws the plan's land-use zones,
not buildings; the heights are in each zone's note.

Source: the "Land Use Plan" (Illustrative Land Use Plan) on Development Guidelines p. 29 (PDF p. 93) of
Appendix 2-1 to the joint Final EIR/EIS, the same plan as the Final EIR/EIS's Figure 2-6 (PDF p. 232)
at a higher resolution. It is georeferenced in boundary_berkeley_space_center.py (OpenStreetMap
building footprints), which also writes the site boundary.

What is drawn:
- Each Subarea is flood-filled inside its black outline: Subareas 2, 3 and 5 research and office
  (the pink-hatched edges are ground-floor active uses over research and office, kept with the block);
  Subarea 1 conference center, short-term lodging and active uses; Subarea 4 a parking garage;
  Subarea 6 split by its fills into student/faculty housing (solid yellow) and research and office
  with parking (teal and grey hatch).
- Subarea 7, the Central Green, is open space except its two pink active-use pavilions.
- Open space: the rest of the site after the Subareas, the pavilions and the street pavement (the
  plan's grey lanes), with strips narrower than about 6 m (sidewalks, planting strips) and pieces under
  400 m2 dropped.
- Not drawn: streets, the 6 acres of off-site utility and demolition work.

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_berkeley_space_center
"""

from __future__ import annotations

import json

import cv2
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping

from .. import config, trace
from . import boundary_berkeley_space_center as bsc
from . import traced_boundaries as tb

PROJECT_ID = bsc.PROJECT
STAGE = "entitlement"
OUT = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
DARK_MAX = 60  # black outlines, dashed building lines and labels: every channel below this
CLOSE_PX = 15  # closes the gaps the dashed lines and labels leave in a Subarea's fill
LINE_HALF_PX = 4  # the Subarea outlines are about 8 px wide; grow the fill to their centre
YELLOW = (248, 192, 20)  # student/faculty housing (and the conference hatch in Subarea 1)
PINK = (244, 140, 152)  # active uses
STREET_GREY = (200, 200, 200)
COLOR_TOL = 14
STRIP_PX = 30  # open-space strips narrower than this (about 6 m) are dropped
MIN_OPEN_M2 = 400  # and open-space pieces smaller than this
STATED_SUBAREA_ACRES = 20.84  # Master Plan p. 10 "Parcel Coverage": Subarea Area 20.84 acres (Subareas 1-6,
# "Subareas 1-6 Coverage 100%"; Subarea 7, 11% covered, is counted in its open space)
STATED_OPEN_ACRES = 10.89  # same table: Open Space 10.89 acres
REF = "Development Guidelines (Spring 2026), Land Use Plan, p. 29, App. 2-1 to the joint Final EIR/EIS"

# Seeds (raster px) inside each Subarea's outline, clear of labels and lines.
SEEDS = {"1": (1150, 1180), "2": (1700, 700), "3": (2750, 1000), "4": (2900, 2150), "5": (1560, 1700),
         "6": (800, 1450), "7": (2150, 1520)}
HEIGHT = ("Development envelope up to 80 ft, plus up to 25 ft of mechanical screens (Final EIR/EIS Table 2-4, "
          "Figure 2-9).")
STEP = {"wescoat": " Along Wescoat Road the envelope steps back 15 ft above 35 ft.",
        "cody": " Along Cody Road the envelope steps back 15 ft above 35 ft.",
        "both": " Along Wescoat and Cody Roads the envelope steps back 15 ft above 35 ft."}
ZONES = [
    # key, category, label, note
    ("2", "office", "Subarea 2: research and office",
     "Up to 680,000 sq ft of research and office uses (120,000 office, 470,000 lab and R&D, 90,000 academic) and "
     "15,000 sq ft of ground-floor active uses, the hatched edge toward the Central Green (Table 2-6). "
     + HEIGHT + STEP["wescoat"] + " Phases 1 and 2 (Final EIR/EIS pp. 2-50 to 2-53)."),
    ("3", "office", "Subarea 3: research and office",
     "Up to 600,000 sq ft of research and office uses (100,000 office, 420,000 lab and R&D, 80,000 academic) and "
     "15,000 sq ft of ground-floor active uses (Table 2-6). " + HEIGHT + STEP["cody"]
     + " Phases 1 and 2 (pp. 2-50 to 2-53)."),
    ("5", "office", "Subarea 5: research and office",
     "Up to 550,000 sq ft of research and office uses (100,000 office, 380,000 lab and R&D, 70,000 academic) and "
     "30,000 sq ft of ground-floor active uses along the Promenade (Table 2-6). " + HEIGHT + " Phases 3 and 4 (p. 2-53)."),
    ("6r", "office", "Subarea 6: research and office with parking",
     "Up to 170,000 sq ft of research and office uses (30,000 office, 120,000 lab and R&D, 20,000 academic), "
     "10,000 sq ft of active uses and a 525,000 sq ft parking garage (Table 2-6). " + HEIGHT + STEP["wescoat"]
     + " Phase 4 (p. 2-53)."),
    ("6h", "residential", "Subarea 6: student and faculty housing",
     "About 145 student and faculty housing units (130,000 sq ft) for UC students and faculty on stays of a semester "
     "to an academic year, at least 10 percent affordable at 80 percent of area median income (Final EIR/EIS "
     "pp. 2-34, 2-43). Under the No Student/Faculty Housing Variant this would be 130,000 sq ft of research and "
     "office space instead. " + HEIGHT + " Phase 4 (p. 2-53)."),
    ("1", "commercial", "Subarea 1: conference center and short-term lodging",
     "A conference center of up to 25,000 sq ft, about 100 short-term lodging units (75,000 sq ft) and 5,000 sq ft "
     "of active uses (Table 2-6). " + HEIGHT + STEP["wescoat"] + " Phase 2 (p. 2-53)."),
    ("4", "other", "Subarea 4: parking garage",
     "A parking garage of up to 555,000 sq ft (Table 2-6). " + HEIGHT + " Phase 3 (p. 2-53)."),
    ("7a", "commercial", "Subarea 7: active-use pavilions",
     ("Two pavilions in the Central Green; Subarea 7 holds up to 15,000 sq ft of active uses (Table 2-6), in an "
      "envelope up to 30 ft (Table 2-4).")),
    ("open", "open-space", "Open space",
     ("Publicly accessible open space: the Central Green, Hangar Commons, Gateway Plaza and the Promenade, with "
      "landscaping along the streets. The project must provide at least 10 acres (Final EIR/EIS Table 2-4); the "
      "Master Plan's parcel coverage table counts 10.89 acres.")),
]


def subarea_px(dark: np.ndarray, seed: tuple[int, int]) -> np.ndarray:
    if dark[seed[1], seed[0]]:
        raise SystemExit(f"seed {seed} sits on a line or label")
    img = dark.copy()
    cv2.floodFill(img, np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8), seed, 2)
    reg = (img == 2).astype(np.uint8)
    if reg.sum() > 1_200_000:
        raise SystemExit(f"the fill from {seed} leaked out of its Subarea outline")
    reg = cv2.morphologyEx(reg, cv2.MORPH_CLOSE, np.ones((CLOSE_PX, CLOSE_PX), np.uint8))
    cs, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filled = np.zeros_like(reg)
    cv2.drawContours(filled, cs, -1, 1, cv2.FILLED)
    return cv2.dilate(filled, np.ones((2 * LINE_HALF_PX + 1,) * 2, np.uint8))


def polys(mask: np.ndarray, min_px: int = 400):
    """A mask's areas as polygons (px), with their holes."""
    cs, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < min_px:
            continue  # a hole, or a speck
        holes, j = [], hier[0][i][2]
        while j != -1:
            if cv2.contourArea(cs[j]) >= min_px:
                holes.append(cs[j].reshape(-1, 2) + 0.5)
            j = hier[0][j][0]
        out.append(shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5, holes)))
    return shapely.union_all(out) if out else shapely.Polygon()


def near(rgb: np.ndarray, col) -> np.ndarray:
    return np.abs(rgb.astype(int) - np.array(col)).max(axis=2) <= COLOR_TOL


def zones_px() -> dict[str, shapely.Geometry]:
    rgb = bsc.figure()
    dark = (rgb.max(axis=2) < DARK_MAX).astype(np.uint8)
    sub = {k: subarea_px(dark, s) for k, s in SEEDS.items()}
    site = bsc.site_px()
    out = {k: polys(m) for k, m in sub.items() if k not in ("6", "7")}

    # Subarea 6: the solid yellow corner is housing, the hatch research and office with parking.
    yellow = cv2.morphologyEx((near(rgb, YELLOW) & (sub["6"] > 0)).astype(np.uint8), cv2.MORPH_OPEN,
                              np.ones((25, 25), np.uint8))  # the hatch has no yellow; drops edge specks
    s6 = polys(sub["6"])
    housing = polys(cv2.dilate(yellow, np.ones((9, 9), np.uint8)) & sub["6"])
    out["6h"] = housing
    out["6r"] = s6.difference(housing.buffer(1))

    # Subarea 7: solid pink pavilions (the hatches elsewhere are thin stripes, gone after an opening).
    pink = cv2.morphologyEx((near(rgb, PINK) & (sub["7"] > 0)).astype(np.uint8), cv2.MORPH_OPEN,
                            np.ones((25, 25), np.uint8))
    out["7a"] = polys(cv2.dilate(pink, np.ones((5, 5), np.uint8)))
    s7 = polys(sub["7"])

    # Open space: the site less the Subareas 1-6, the pavilions and the street pavement.
    street = cv2.morphologyEx(near(rgb, STREET_GREY).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    street = cv2.morphologyEx(street, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    built = shapely.union_all([g for k, g in out.items()])
    open_ = site.difference(built).difference(polys(street, 2000).buffer(2))
    open_ = open_.buffer(-STRIP_PX / 2).buffer(STRIP_PX / 2).intersection(site)
    out["open"] = shapely.union_all([open_, s7.difference(out["7a"])])
    out["_s7"] = s7
    return out


def main() -> None:
    sim, rep = bsc.georeference()
    site_utm = tb.clean(sim.geometry(bsc.site_px()))
    px = zones_px()
    feats, areas = [], {}
    for key, cat, label, note in ZONES:
        g = trace.as_multipolygon(shapely.make_valid(sim.geometry(px[key]).simplify(0.4)).intersection(site_utm))
        min_m2 = MIN_OPEN_M2 if key == "open" else 50  # open space: drops planting specks at street corners
        g = trace.as_multipolygon(shapely.MultiPolygon([p for p in g.geoms if p.area > min_m2]))
        areas[label] = g.area / tb.ACRE_M2
        feats.append({"type": "Feature", "properties": {
            "kind": "zone", "category": cat, "label": label, "stage": STAGE,
            "source": f"traced: {REF}",
            "note": note + " Approximate: the plan is conceptual until NASA approves the project.",
        }, "geometry": mapping(tb.to_wgs(g))})
    sub_acres = sum(v for k, v in areas.items() if k.startswith("Subarea") and not k.startswith("Subarea 7"))
    for k, v in areas.items():
        print(f"[{PROJECT_ID}]   {k:>52}: {v:5.2f} acres")
    print(f"[{PROJECT_ID}] Subareas 1-6 {sub_acres:.2f} acres (Master Plan {STATED_SUBAREA_ACRES}); open space "
          f"{areas['Open space']:.2f} acres (Master Plan {STATED_OPEN_ACRES} within the parcel boundary, Subarea 7 included)")
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": ("Land-use zones traced from the project's land use plan (Development Guidelines, Spring 2026, "
                        "Appendix 2-1 to the joint Final EIR/EIS; the same plan as the EIR/EIS's Figure 2-6): research "
                        "and office blocks around a Central Green, a conference center and short-term lodging, student "
                        "and faculty housing, a parking garage, active-use pavilions and open space. The plan is "
                        "conceptual, so every edge is approximate. Zones, not buildings: the EIR/EIS studies an 80-ft "
                        "development envelope, not a building design."),
            "note": "Land uses from the project's 2026 land use plan, approximate; zones, not buildings.",
            "sourceUrl": bsc.PLAN["url"],
            "sourceLabel": "Development guidelines land use plan (PDF)",
            "georeference": rep,
            "license": f"Zones: traced from a public CEQA document (CEQAnet). Georeference: {tb.OSM_LICENSE}.",
            "documents": [bsc.PLAN["url"], bsc.FEIR["url"], bsc.FEIR_DOC, bsc.CEQANET],
            "checks": {"subareas_1_to_6_acres": round(sub_acres, 2), "stated_subarea_acres": STATED_SUBAREA_ACRES,
                       "open_space_acres": round(areas["Open space"], 2), "stated_open_space_acres": STATED_OPEN_ACRES},
        },
        "features": feats,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[{PROJECT_ID}] wrote {OUT.relative_to(config.ROOT)}: {len(feats)} zones")


if __name__ == "__main__":
    main()
