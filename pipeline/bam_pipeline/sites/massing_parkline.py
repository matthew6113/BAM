"""Parkline (the former SRI International campus, Menlo Park): new buildings at their approved heights.

Source:
- Parkline Master Plan Project Plans, project variant, dated June 24, 2025 (the City's
  "project-variant-master-plan-set_0703.pdf", linked as Attachment K, "Full master plan project
  plans", of City Council staff report 25-143-CC, Sept 30, 2025). The Council approved the master
  plan on Sept 30, 2025 and adopted its ordinances on Oct 7, 2025.
- Sheet G3.03 "Conceptual Building Height Plan" (PDF page 73) draws each new building's footprint
  and lists its approximate height at the top of the parapet, from 35 ft (Town Homes 1) to 91 ft
  (Offices 2-4). The Conditional Development Permit (CDP, Exhibit 3 to the zoning ordinance;
  staff report p. J-1.587) makes the sheet binding: "2.3.4 Building heights shall generally
  conform to the maximum heights provided on Sheet G3.03 of the Project Plans and not exceed the
  maximum heights permitted by the Design Standards"; "2.3.4.1 Buildings R1 and R2 shall conform
  to the varied building heights as depicted ... on Sheet G3.03"; "2.3.4.2 Parking Garage 3 ...
  shall not exceed three (3) stories and 50 feet in height."
- The Design Standards' maximums (CDP Exhibit D, staff report pp. J-1.627 and J-1.651):
  multifamily 75 ft, attached townhomes 40 ft, detached townhomes 35 ft, office/R&D 95 ft,
  parking structures 70 ft, amenity building 55 ft, each before the allowed parapet, roof-deck
  railing and stair-tower exceedances. They're recorded on each feature.

What this is and isn't:
- Each new building is drawn as its G3.03 footprint, extruded to the sheet's approximate parapet
  height. The sheet itself says the heights "are intended to provide an illustrative example", and
  architectural control permits will set the final designs, so the massing is labelled
  illustrative.
- Residential 1 and 2 step between 3 and 6 stories (G3.03 labels each wing in stories only); they
  are drawn whole at the sheet's building height (72 and 62 ft), as is Residential 3's one-story
  wing (75 ft). Upper terraces are part of the
  footprint; the small utility and trash enclosures, the common utility yard and the office
  buildings' cantilevered terraces are left out.
- The 1.6-acre affordable housing parcel (up to 154 homes) has no building on G3.03, so nothing is
  drawn there. Neither is the 2.6-acre public park.
- Buildings P, S and T, which SRI keeps, are existing buildings in the base map and aren't redrawn.
  Nothing new has been built: the project is entitled.
- The Phase 2 application (2026), which would replace this plan, is under review and isn't drawn.

Georeferencing: G3.03 is a raster sheet (1" = 100'). Rendered at 150 dpi, street centrelines
(midway between the curb lines in its base map) at seven intersections around the site are matched
to OpenStreetMap (via Overture) with a least-squares similarity fit; residuals are recorded. As a
check, the fitted scale is compared with the sheet's printed scale, and the traced footprints are
compared with the City of Menlo Park parcels that make up the site.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_parkline
"""

from __future__ import annotations

import json
import shutil
import urllib.error
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "parkline"
UTM = tb.UTM

PLANS = {
    "title": "Parkline Master Plan Project Plans, project variant (June 24, 2025)",
    "url": "https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/"
           "under-review/parkline/map20250703/project-variant-master-plan-set_0703.pdf",
    "sha256": "787ff582d1345e4c38354c200efbc23f827c698a3125995e58aaa744a55de513",
    "file": "pl-master-plan-set-20250624.pdf",
}
STAFF_REPORT = {
    "title": "City Council staff report 25-143-CC (Sept 30, 2025), CDP section 2.3.4 (p. J-1.587) and "
             "Design Standards (CDP Exhibit D, pp. J-1.627, J-1.651)",
    "url": "https://www.menlopark.gov/files/sharedassets/public/v/2/agendas-and-minutes/city-council/2025-meetings/"
           "20250930/j1-20250930-cc-parkline.pdf",
}
SHEET = {"page_index": 72, "sheet": "G3.03", "title": "Conceptual Building Height Plan"}
DPI = 150
SHEET_SCALE_M_PER_PT = 100 * 0.3048 / 72  # 1" = 100'-0"
IMAGE_SIZE = (3601, 5400)  # rows, columns of the 150-dpi render

# Street centrelines in the render (pixels), each midway between the curb lines drawn either side.
CONTROLS = {
    ("Ravenswood Avenue", "Laurel Street"): (1373, 287),
    ("Ravenswood Avenue", "Pine Street"): (1865, 282),
    ("Ravenswood Avenue", "Marcussen Drive"): (3140, 267),
    ("Ravenswood Avenue", "Middlefield Road"): (4370, 253),
    ("Middlefield Road", "Ringwood Avenue"): (4367, 1028),
    ("Middlefield Road", "Seminary Drive"): (4374, 2499),
    ("Laurel Street", "Burgess Drive"): (1187, 2883),
}
STREETS_BBOX = (-122.190, 37.447, -122.166, 37.465)

# Fill colours in the render (RGB), from the sheet's legend: residential (with its tan upper-terrace
# hatch), office/R&D, parking garage.
CLASSES = {
    "residential": [(252, 204, 68), (244, 230, 190)],
    "office": [(177, 204, 231)],
    "garage": [(189, 189, 189)],
}
COLOUR_TOL = 14

# Each building: its fill class, the render box (pixels) its pieces' centres fall in, and the
# G3.03 table entry "Approx. height at T.O. parapet (ft), as shown" with its stories.
# Design-standard maximums (CDP Exhibit D) by building type.
DS_MAX = {"multifamily": 75, "townhomes": "40 ft if attached or 35 ft if detached", "office/R&D": 95,
          "parking structure": 70, "amenity building": 55}
DS_NOUN = {"multifamily": "multifamily buildings", "townhomes": "townhomes", "office/R&D": "office/R&D buildings",
           "parking structure": "parking structures", "amenity building": "the amenity building"}
BUILDINGS = [
    # label, class, box (x0, y0, x1, y1), height ft, stories, use, design-standard type
    ("Residential 1", "residential", (1404, 392, 2309, 810), 72.0, "4-6", "residential", "multifamily"),
    ("Residential 2", "residential", (1296, 864, 1877, 1620), 62.0, "3-5", "residential", "multifamily"),
    ("Residential 3", "residential", (3834, 365, 4253, 648), 75.0, "6", "residential", "multifamily"),
    ("Town Homes 1", "residential", (1242, 1715, 1890, 1985), 35.0, "2", "residential", "townhomes"),
    ("Town Homes 2", "residential", (3848, 707, 4280, 977), 45.0, "3", "residential", "townhomes"),
    ("Office 1", "office", (2754, 648, 3348, 878), 75.0, "4", "office/R&D", "office/R&D"),
    ("Office 2", "office", (3132, 986, 3470, 1593), 91.0, "5", "office/R&D", "office/R&D"),
    ("Office 3", "office", (3146, 1661, 3416, 2241), 91.0, "5", "office/R&D", "office/R&D"),
    ("Office 4", "office", (2444, 1985, 3038, 2255), 91.0, "5", "office/R&D", "office/R&D"),
    ("Office 5", "office", (2552, 999, 2876, 1580), 75.0, "4", "office/R&D", "office/R&D"),
    ("Office amenity building", "office", (1985, 1742, 2376, 1922), 41.0, "2", "office amenity", "amenity building"),
    ("Parking garage 1", "garage", (3632, 1075, 3848, 1634), 65.5, "5", "parking", "parking structure"),
    ("Parking garage 2", "garage", (3537, 1912, 3848, 2381), 65.5, "5", "parking", "parking structure"),
    ("Parking garage 3", "garage", (2012, 1922, 2327, 2376), 44.5, "3", "parking", "parking structure"),
]
DARK_MAX = 100  # outlines and lettering: every channel below this
OUTLINE_PX = 6  # building outlines are about 5 px wide
MIN_PART_PX = 1000  # smaller pieces are equipment pads and enclosures (a townhome is about 2,000)
MIN_HOLE_PX = 5000  # courtyards are kept as holes; smaller openings (roof equipment drawn white) are not
CLOSE_PX = 3
OPEN_PX = 9  # strips lettering strokes (about 4 px) that run out of a building


# ---------------------------------------------------------------- documents

def fetch_plans():
    """The plan set is 138 MB and the city's server drops long transfers; resume until complete."""
    dest = tb.DOCS / PLANS["file"]
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(".pdf.part")
        for _ in range(60):
            have = tmp.stat().st_size if tmp.exists() else 0
            req = urllib.request.Request(PLANS["url"], headers={"Range": f"bytes={have}-"} if have else {})
            try:
                with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "ab" if have else "wb") as f:
                    if have and r.status != 206:
                        raise SystemExit("the city's server ignored the range request; delete the partial file")
                    total = int(r.headers["Content-Range"].split("/")[-1]) if have else int(r.headers["Content-Length"])
                    shutil.copyfileobj(r, f)
            except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
                print(f"[parkline] download interrupted ({e}); resuming")
                continue
            if tmp.stat().st_size >= total:
                break
        tmp.rename(dest)
    return trace.fetch_document(PLANS["url"], dest, PLANS["sha256"])


def render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[SHEET["page_index"]]
    text = page.get_textpage().get_text_range()
    if "CONCEPTUAL BUILDING HEIGHT PLAN" not in text or "G3.03" not in text or "2025.06.24" not in text:
        raise SystemExit("PDF page 73 is not Sheet G3.03 of the June 24, 2025 plans")
    rgb = np.asarray(page.render(scale=DPI / 72).to_pil().convert("RGB"))
    if rgb.shape[:2] != IMAGE_SIZE:
        raise SystemExit(f"unexpected render size {rgb.shape}")
    return rgb, text


def check_table(text: str) -> None:
    """Every height drawn must be in the sheet's building height table, with its stories."""
    import re

    flat = " ".join(text.split())
    for label, _, _, h, stories, _, _ in BUILDINGS:
        want = f"{int(h)}'-{int(round((h - int(h)) * 12))}\""
        pat = re.escape(label.upper()) + r"\*? " + re.escape(want) + r" \(" + re.escape(stories) + r" STOR(Y|IES)\)"
        if not re.search(pat, flat):
            raise SystemExit(f"G3.03's table does not give {label} as {want} ({stories} stories)")


# ---------------------------------------------------------------- georeference and trace

def georeference(streets: gpd.GeoDataFrame) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), px in CONTROLS.items():
        src.append(px)
        dst.append(tb.intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    sim = trace.fit_similarity(src, dst, labels)
    per_pt = sim.scale * DPI / 72
    if abs(per_pt / SHEET_SCALE_M_PER_PT - 1) > 0.01:
        raise SystemExit(f"fitted scale {per_pt:.4f} m/pt is off the sheet's 1\" = 100' ({SHEET_SCALE_M_PER_PT:.4f})")
    return sim


def class_mask(rgb: np.ndarray, colours) -> np.ndarray:
    d = np.min([np.abs(rgb.astype(int) - np.array(c)).max(axis=2) for c in colours], axis=0)
    return (d <= COLOUR_TOL).astype(np.uint8)


def trace_building(rgb: np.ndarray, masks: dict, spec):
    """One building's footprint in render pixels.

    The building is its class fill plus the dark linework drawn on and around it (outlines, wing
    lines, lettering), taken as the connected pieces holding fill whose centres fall in the
    building's box. Holes are filled unless they are mostly lawn or paving (courtyards); an opening
    then strips lettering that runs out over the lawn.
    """
    label, cls, (x0, y0, x1, y1) = spec[:3]
    pad = 40
    win = (slice(y0 - pad, y1 + pad), slice(x0 - pad, x1 + pad))
    fill = masks[cls][win]
    rsub = rgb[win].astype(int)
    dark = (rsub.max(axis=2) < DARK_MAX).astype(np.uint8)
    # Anti-aliasing leaves a hairline between a fill and its outline; label on a 1-px dilation.
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cv2.dilate(fill | dark, np.ones((3, 3), np.uint8)), connectivity=8)
    lab[(fill | dark) == 0] = 0
    keep = np.zeros_like(fill)
    for i in range(1, n):
        part = (lab == i) & (fill > 0)
        if part.sum() < 150:
            continue
        ys, xs = np.nonzero(part)
        if pad <= xs.mean() < pad + x1 - x0 and pad <= ys.mean() < pad + y1 - y0:
            keep[lab == i] = 1
    if not keep.any():
        raise SystemExit(f"no {cls} fill found for {label}")
    if cls == "residential":  # close small gaps in the townhome front linework
        keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((CLOSE_PX, CLOSE_PX), np.uint8))
    lawn = (np.abs(rsub - [200, 222, 174]).max(axis=2) <= 16) | (rsub.min(axis=2) >= 240)
    contours, hier = cv2.findContours(keep, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    filled = keep.copy()
    for i, c in enumerate(contours):
        if hier[0][i][3] == -1:
            continue
        hole = np.zeros_like(keep)
        cv2.drawContours(hole, [c], -1, 1, cv2.FILLED)
        hole &= 1 - keep
        if hole.sum() and lawn[hole > 0].mean() < 0.5:
            filled |= hole
    # Offices and garages: keep only what lies within an outline's width of the fill, which drops the
    # hatched utility and trash enclosures and terraces their linework ties on. (Townhome fronts are
    # drawn as linework, so residential buildings keep it.) Then strip lettering strokes.
    if cls != "residential":
        core = cv2.morphologyEx(fill & keep, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        cs, _ = cv2.findContours(core, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(core, cs, -1, 1, cv2.FILLED)
        filled &= cv2.dilate(core, np.ones((2 * OUTLINE_PX + 1,) * 2, np.uint8))
    filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, np.ones((OPEN_PX, OPEN_PX), np.uint8))
    # Pieces that are all linework (a stretch of the dashed site boundary) aren't buildings.
    n, lab = cv2.connectedComponents(filled, connectivity=4)
    for i in range(1, n):
        if fill[lab == i].mean() < 0.25:
            filled[lab == i] = 0
    contours, hier = cv2.findContours(filled, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    off = np.array([x0 - pad, y0 - pad]) + 0.5
    for i, c in enumerate(contours):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < MIN_PART_PX:
            continue
        holes = []
        ch = hier[0][i][2]
        while ch != -1:
            if cv2.contourArea(contours[ch]) >= MIN_HOLE_PX:
                holes.append(contours[ch].reshape(-1, 2) + off)
            ch = hier[0][ch][0]
        polys.append(shapely.make_valid(Polygon(c.reshape(-1, 2) + off, holes)))
    return shapely.union_all(polys)


# ---------------------------------------------------------------- main

def main() -> None:
    pdf_path = fetch_plans()
    rgb, text = render(pdf_path)
    check_table(text)
    streets = tb.streets("pl_parkline", STREETS_BBOX)
    sim = georeference(streets)
    print(f"[parkline] Sheet G3.03 georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale * DPI / 72:.4f} m/pt (sheet: {SHEET_SCALE_M_PER_PT:.4f}), "
          f"rotation {np.degrees(sim.rotation):.2f} deg")

    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]
    masks = {k: class_mask(rgb, v) for k, v in CLASSES.items()}

    fig = f"{PLANS['title']}, Sheet {SHEET['sheet']} \"{SHEET['title']}\" (PDF p. {SHEET['page_index'] + 1})"
    features, total, outside = [], 0.0, 0.0
    for spec in BUILDINGS:
        label, cls, _, h, stories, use, ds_type = spec
        px = trace_building(rgb, masks, spec)
        g = shapely.make_valid(sim.geometry(px)).simplify(0.35)
        g = trace.as_multipolygon(shapely.make_valid(g))
        total += g.area
        outside += g.difference(site_utm).area
        print(f"[parkline]   {label:>24}: {h:5.1f} ft, {g.area:8.0f} m2, {len(g.geoms)} part(s), "
              f"{g.difference(site_utm).area:5.0f} m2 off the parcels")
        ds_max = DS_MAX[ds_type]
        props = {
            "kind": "building",
            "label": label,
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": use,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: footprint and approximate parapet height ({h:g} ft, {stories} "
                      f"{'story' if stories == '1' else 'stories'}) traced from {fig}; CDP 2.3.4",
            "note": (f"G3.03 calls its heights an illustrative example. The design standards cap "
                     f"{DS_NOUN[ds_type]} at {ds_max if isinstance(ds_max, str) else f'{ds_max} ft'}, before allowed parapets and rooftop structures.")
                    + (f" Steps between {stories.replace('-', ' and ')} stories by wing; drawn whole at the building's height."
                       if "-" in stories else "")
                    + (" CDP 2.3.4.2 caps this garage at 3 stories and 50 ft." if label == "Parking garage 3" else ""),
        }
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(g))})
    check = {"footprints_m2": round(total), "off_site_m2": round(outside), "off_site_share": round(outside / total, 4)}
    print(f"[parkline] {check['off_site_share']:.1%} of the traced footprint area falls off the site parcels")
    if check["off_site_share"] > 0.02:
        raise SystemExit("too much of the traced massing falls off the site; check the georeference")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: the 14 new buildings of the approved 2025 master plan (three apartment "
                "buildings, two townhome groups, five office/R&D buildings, an amenity building and three parking "
                "garages) are drawn as their footprints on the plan's Conceptual Building Height Plan (Sheet G3.03, "
                "June 24, 2025), at its approximate parapet heights of 35 to 91 ft. The sheet calls these heights an "
                "illustrative example within the design standards' limits. Buildings P, S and T, which SRI keeps, "
                "stay in the base map; the affordable housing parcel and the public park have no building drawn. "
                "Nothing new has been built, and the 2026 Phase 2 proposal isn't drawn."
            ),
            "note": ("Buildings are drawn from the approved 2025 plan's conceptual height plan; final designs "
                     "come with each building's architectural control permit."),
            "sourceUrl": PLANS["url"],
            "sourceLabel": "Master plan project plans, 2025 (PDF)",
            "georeference": {"sheet_g3_03": {**sim.report(),
                                             "method": "street-centreline intersections matched to OpenStreetMap, "
                                                       "least-squares similarity",
                                             "sheet_scale_m_per_unit": round(SHEET_SCALE_M_PER_PT * 72 / DPI, 5)},
                             "check_against_parcels": check},
            "documents": {
                "project_plans": {"title": PLANS["title"], "url": PLANS["url"], "sha256": PLANS["sha256"],
                                  "pages": "Sheet G3.03, PDF p. 73"},
                "cdp_and_design_standards": STAFF_REPORT,
            },
            "license": "Building footprints: traced from a public City of Menlo Park document. "
                       "Georeference: " + tb.OSM_LICENSE + ".",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[parkline] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
