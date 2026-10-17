"""The Orchards: illustrative height envelopes on the approved parcels and lots.

Footprints: Vesting Tentative Map 9693, sheet C2.0 Overall Lotting Plan (Applicant's Project Plans dated
Sept 5, 2025, PDF p. 172), the CAD lot lines at 1" = 100', placed with the georeference of
boundary_the_orchards.py (sheet C3.0 fitted to OpenStreetMap building footprints). The sheet's area table
names the development parcels of each district. The sheet's lot lines are joined into faces (line ends
that stop short of the line they meet are extended to it), and each parcel is checked against its tabled
area: most agree within 1%, four (A4, B1, C2, G1) differ by 2-13% and say so in their note; lots 1-103
together agree with the table's total within 1%.

Heights: Orchards Design Guidelines dated Nov 14, 2025 (the version the City Council's conditions of
approval name, Resolution 2026-040, condition 1):
- Mixed-Use District (parcels A1 to A4 and D1): "between five (5) to seven (7) floors and a maximum height
  of 85 feet" (p. 162, Figure 7.1.2).
- Multi-Family District: the B and C parcels "up to seven (7) floors and a maximum height of 85 feet"; the
  E, F, G and H parcels "four (4) or five (5) floors and a maximum height of 65 feet" (p. 168, Figure 7.2.2).
- Neighborhood District: "Attached Row Townhomes: 40-feet"; single-family row, detached and court homes
  35 feet, measured to the midpoint of the roof (p. 175, Figure 7.3.2). The attached row townhomes stand on
  lots 78 to 103 (the clusters west of the park and beside Parcel E in Figure 7.3.2 and on plan sheet SP2);
  lots 1 to 77 hold the single-family homes.

Each parcel or lot is drawn whole and raised to its limit: an illustrative envelope, not a building. The
plan set's DMU-S standards table (sheet SP4) gives 30 ft for the single-family types; the newer design
guidelines' 35 ft is used and the other value noted. Phases: the Neighborhood District's development
plan is approved; the Mixed-Use and Multi-Family districts are marked "future application" on the plan
set (sheet L-200), within the 20-year master plan. Parcel H1 is the multi-family affordable site (sheet
SP4). The existing campus buildings are all to be demolished, so none are drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_the_orchards
"""

from __future__ import annotations

import json
import re

import shapely
from shapely.geometry import LineString, Point, mapping

from .. import config, trace
from . import boundary_the_orchards as bo
from . import traced_boundaries as tb

PROJECT = "the-orchards"
OUT = config.ROOT / "data" / "massing" / f"{PROJECT}.geojson"
GUIDELINES = {
    "url": "https://docs.sanramon.ca.gov/WebLink/ElectronicFile.aspx?docid=21620063&dbid=0&repo=sanramon",
    "view": "https://docs.sanramon.ca.gov/WebLink/DocView.aspx?id=21620063&dbid=0&repo=sanramon",
    "file": "orchards-design-guidelines-2025-11-14.pdf",
    "sha256": "d51db81d5b2b250a687c285146d484503c8a34b94bc9eae38963d19bd8d73875",
}
SQFT = 0.09290304

# Sheet C2.0 area table (sq ft) for the development parcels.
PARCELS = {
    "A1": 115330, "A2": 109813, "A3": 41265, "A4": 26256, "D1": 95433,
    "B1": 127549, "B2": 92810, "C1": 99115, "C2": 55263, "E1": 93035, "F1": 67041, "G1": 48343, "G2": 53400,
    "H1": 74608,
}
LOTS_TOTAL_SQFT = 1210450  # lots 1-103, "TOTAL (SF±)"
MU = "Mixed-use: homes over ground-floor retail, entertainment and commercial uses"
MF = "Multi-family homes (apartments, condominiums, senior or affordable housing)"


def spec(name: str) -> dict:
    """Height limit, use, phase and source for a parcel ("A1") or lot ("LOT 12")."""
    future = "Future application (master plan, about 20-year buildout)"
    if name.startswith("LOT"):
        n = int(name.split()[1])
        town = n >= 78
        return {
            "height_ft": 40 if town else 35,
            "use": "Attached row townhomes" if town else "Single-family homes (court, detached and row homes)",
            "phase": "Neighborhood District (development plan approved)",
            "source": (f"illustrative: lot {n} from Vesting Tentative Map 9693 sheet C2.0 (plans PDF p. 172), drawn to "
                       f"the {40 if town else 35}-ft limit for {'attached row townhomes' if town else 'single-family homes'} "
                       "in the Orchards Design Guidelines (Nov 14, 2025), p. 175, Figure 7.3.2"),
            "note": None if town else "The plan set's DMU-S standards table (sheet SP4) gives 30 ft; the newer design guidelines give 35 ft.",
        }
    letter = name[0]
    if letter in "AD":
        h, use, page, fig = 85, MU, 162, "7.1.2"
    else:
        h, use, page, fig = (85 if letter in "BC" else 65), MF, 168, "7.2.2"
    note = None
    if name == "H1":
        use = "Affordable homes (the multi-family affordable site)"
        note = ("The Affordable Housing Plan (Dec 4, 2025) dedicates a site for a 100-home affordable community "
                "(99 affordable homes and a manager's unit); plan sheet SP4 marks Parcel H1 as the multi-family affordable site.")
    return {
        "height_ft": h,
        "use": use,
        "phase": future,
        "source": (f"illustrative: Parcel {name} from Vesting Tentative Map 9693 sheet C2.0 (plans PDF p. 172), drawn to "
                   f"the {h}-ft limit in the Orchards Design Guidelines (Nov 14, 2025), p. {page}, Figure {fig}"),
        "note": note,
    }


def labels() -> dict[str, tuple[float, float]]:
    """Label points of the parcels and lots on C2.0, from horizontal words ("LOT" "12", "PARCEL" "A1") and the
    vertical ones, which come out with their characters reversed ("68" over "TOL" is lot 86)."""
    _, words = bo.sheet(bo.C20)
    out = {}
    for i, w in enumerate(words):
        t = w["text"]
        if t in ("LOT", "PARCEL"):
            nxt = [v for v in words if v is not w and abs(v["top"] - w["top"]) < 16 and 0 <= v["x0"] - w["x1"] < 30]
            if t == "LOT":
                nxt = [v for v in nxt if v["text"].isdigit()]
            else:
                nxt = [v for v in nxt if re.fullmatch(r"[A-Z]\d{1,2}", v["text"])]
            if nxt:
                v = min(nxt, key=lambda v: v["x0"] - w["x1"])
                key = f"LOT {v['text']}" if t == "LOT" else v["text"]
                out.setdefault(key, ((w["x0"] + v["x1"]) / 2, (w["top"] + v["bottom"]) / 2))
        elif t in ("TOL", "LECRAP"):  # vertical label: the number sits just above, reversed
            above = [v for v in words if abs(v["x0"] - w["x0"]) < 6 and 0 < w["top"] - v["top"] < 30]
            if above:
                v = max(above, key=lambda v: v["top"])
                txt = v["text"][::-1]
                key = f"LOT {txt}" if t == "TOL" and txt.isdigit() else (txt if re.fullmatch(r"[A-Z]\d{1,2}", txt) else None)
                if key:
                    out.setdefault(key, ((w["x0"] + w["x1"]) / 2, (v["top"] + w["bottom"]) / 2))
    return out


def _extend_dangling(ls: list[LineString], reach: float = 40.0, tol: float = 0.5) -> list[LineString]:
    """CAD "extend": a line end that stops short of the line it should meet (it touches nothing within tol)
    is carried on along its last segment, up to reach, to the first line it hits."""
    tree = shapely.STRtree(ls)
    out = list(ls)
    for i, g in enumerate(ls):
        xy = list(g.coords)
        for end, prev in ((xy[-1], xy[-2]), (xy[0], xy[1])):
            p = Point(end)
            near = [j for j in tree.query(p.buffer(tol)) if j != i and ls[j].distance(p) <= tol]
            if near:
                continue
            dx, dy = end[0] - prev[0], end[1] - prev[1]
            n = (dx * dx + dy * dy) ** 0.5
            if n == 0:
                continue
            ray = LineString([end, (end[0] + dx / n * reach, end[1] + dy / n * reach)])
            hits = []
            for j in tree.query(ray):
                if j == i:
                    continue
                x = ray.intersection(ls[j])
                for q in shapely.get_parts(x):
                    if q.geom_type == "Point" and q.distance(p) > 1e-6:
                        hits.append(q)
            if hits:
                q = min(hits, key=p.distance)
                out.append(LineString([end, (q.x, q.y)]))
    return out


def faces() -> list[shapely.Polygon]:
    """The faces of C2.0's property lines (1.26 pt) and project boundary (2.7 pt), in PDF points. Line ends
    that stop short are extended to the line they meet; the lines are then thickened by 0.4 pt, the enclosed
    holes taken and grown back."""
    objs, _ = bo.sheet(bo.C20)
    ls = [LineString(o["pts"]) for o in objs if o["sc"] == "0" and o["lw"] in (1.26, 2.7)]
    ls = _extend_dangling([g for g in ls if g.bounds[1] < 1950 and g.length > 0])
    ink = shapely.union_all([g.buffer(0.4) for g in ls])
    holes = [shapely.Polygon(h) for part in shapely.get_parts(ink) for h in part.interiors]
    return [h.buffer(0.4, join_style="mitre") for h in holes if h.area > 50]


def main() -> None:
    sim, rep = bo.georeference()
    sq = (bo.M_PER_PT / 0.3048) ** 2  # sq ft per pt2
    lab = labels()
    fs = faces()
    want = list(PARCELS) + [f"LOT {n}" for n in range(1, 104)]
    feats, lot_sqft = [], 0.0
    for name in want:
        if name not in lab:
            raise SystemExit(f"{name}: no label found on sheet C2.0")
        pt = Point(lab[name])
        hit = [f for f in fs if f.contains(pt)]
        if len(hit) != 1:
            raise SystemExit(f"{name}: {len(hit)} faces under its label")
        face = hit[0]
        sqft = face.area * sq
        off = None
        if name in PARCELS:
            off = sqft / PARCELS[name] - 1
            if abs(off) > 0.15:
                raise SystemExit(f"Parcel {name}: {sqft:,.0f} sq ft drawn against {PARCELS[name]:,} tabled")
        else:
            lot_sqft += sqft
        g = bo.c20_to_utm(face).simplify(0.3, preserve_topology=True)
        s = spec(name)
        props = {
            "kind": "block",
            "block": name.title() if name.startswith("LOT") else f"Parcel {name}",
            "label": name.title() if name.startswith("LOT") else f"Parcel {name}",
            "stage": "entitled",
            "height_ft": s["height_ft"],
            "podium_ft": None,
            "base_ft": 0,
            "use": s["use"],
            "phase": s["phase"],
            "illustrative": True,
            "source": s["source"],
        }
        notes = [s["note"]] if s["note"] else []
        if off is not None and abs(off) > 0.02:  # the sheet's lot lines and its area table don't quite agree
            notes.append(f"Drawn about {sqft:,.0f} sq ft against {PARCELS[name]:,} sq ft in sheet C2.0's area table, "
                         "so its edges are approximate.")
        if notes:
            props["note"] = " ".join(notes)
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(g))})
    if abs(lot_sqft / LOTS_TOTAL_SQFT - 1) > 0.01:
        raise SystemExit(f"lots 1-103: {lot_sqft:,.0f} sq ft drawn against {LOTS_TOTAL_SQFT:,} tabled")
    trace.fetch_document(GUIDELINES["url"], tb.DOCS / GUIDELINES["file"], GUIDELINES["sha256"])

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT,
            "illustrative": True,
            "summary": (
                "Illustrative height envelopes: the approved development parcels and lots of Vesting Tentative Map "
                "9693, each drawn whole and raised to the height limit the Orchards Design Guidelines (Nov 2025) set "
                "for it: 85 ft in the Mixed-Use District and on the Multi-Family District's B and C parcels, 65 ft on "
                "its E, F, G and H parcels, 40 ft on the attached row townhome lots and 35 ft on the single-family "
                "lots of the Neighborhood District. They are limits, not building designs; streets, parks and open "
                "space parcels are left empty. The existing office campus, to be demolished, isn't drawn."),
            "note": "Approved parcels raised to the design guidelines' height limits; real buildings will be smaller.",
            "sourceUrl": GUIDELINES["view"],
            "sourceLabel": "Orchards Design Guidelines, Nov 2025",
            "documents": [GUIDELINES["view"], bo.PLANS["view"], bo.COUNCIL_URL],
            "georeference": rep,
            "license": ("Footprints and heights: traced facts from public City of San Ramon records (the PDFs are not "
                        f"redistributed). Georeference: {tb.OSM_LICENSE}."),
        },
        "features": feats,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(config.ROOT)}: {len(feats)} envelopes; lots {lot_sqft:,.0f} sq ft "
          f"(tabled {LOTS_TOTAL_SQFT:,})")


if __name__ == "__main__":
    main()
