"""598 Brannan Street: the three approved office buildings, traced from the 2019 plan set's site and roof plans.

Sources:
- Planning Commission packet for Record No. 2012.0640B/ENX (598 Brannan Street, hearing June 6, 2019), Exhibit B
  ("598 Brannan Street planning update", May 23, 2019): PDF page 115, the "Site plan" (1" = 80'), with the ground-floor
  outlines of Buildings 1, 2 and 3 and the Building 4 affordable housing site; and PDF page 116, the "Roof plan"
  (1" = 80'), with each building's roof outline and labels "Building 1 / 11 floors / 159'6" T.O. roof", "Building 2 /
  13 floors / 185' T.O. roof" and "Building 3 / 10 floors / 149'9" T.O. roof". Both are vector drawings.
- The same packet's draft Large Project Authorization (PDF p. 9): "Building 1 would be a mixed-use office building
  reaching a height of 160 feet (180 ft. to top of rooftop mechanical screening), located at the northeast corner of
  Brannan and 5th streets"; "Building 2 would be a mixed-use office building reaching a height of 185 feet (205 ft. to
  top of rooftop mechanical screening), located at the southeast corner of 5th and Welsh streets"; "Building 3 would
  be a mixed-use office building reaching a height of 150 feet (170 ft. to top of rooftop mechanical screening),
  located mid-block on Bryant Street". The elevations (PDF pp. 156, 161, 168) give the floor levels where the
  buildings step back: Building 1 level 3 at 31 ft, Building 2 level 6 at 73 ft, Building 3 level 6 at 76 ft.
- Planning Commission minutes of June 6, 2019: approved as Motions 20459 (Large Project Authorization) and 20460
  (office allocation, Phase 1); minutes of Dec 3, 2020: Motion 20816 (office allocation, Phase 2, Building 3).
- DataSF Planning record 2023-000990GPR and DBI permit 202209283327: the parcel the project dedicated for affordable
  housing (now lot 176, 160 Freelon Street) holds a nine-story building with 85 affordable homes, under construction.

How it's drawn:
- Each page is registered to the DataSF parcels by a least-squares similarity on lot corners the drawing shows: the
  corners of lot 045 at 5th and Brannan streets, at 5th and Welsh streets and on Brannan Street, and the corners of
  lots 050 and the former lot 052 (now 176 and 177) on Bryant Street and at Freelon Street, read from the outlines of
  the neighbouring buildings drawn on the lot lines. The RMS is reported.
- Each office building is two volumes: its roof outline from the roof plan, at the roof height in the approval, and
  the rest of its ground-floor outline from the site plan, up to the level where the building steps back. Upper
  floors that overhang the ground floor are drawn down to the ground; terraces cut into the upper floors and the
  rooftop mechanical screens (to 180, 205 and 170 ft) are not modelled. Illustrative.
- Building 4: the affordable housing site, the parcel itself (lot 176), outlined on the ground: the building now
  rising there (nine stories, 85 homes) isn't the one sketched in 2019, and its height in feet isn't in the records
  read.

Stage: the office buildings were approved in 2019 and 2020; DBI issued the site permits for Buildings 1 and 2 on March
17, 2021, but none of the three has been started, so they are drawn as "entitled". The affordable housing building is
"construction" (first construction document July 15, 2025).

    uv run --directory pipeline python -m bam_pipeline.sites.massing_598_brannan
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "598-brannan"
UTM = ob.UTM
SQFT = 10.7639

PACKET = {
    "title": "Planning Commission packet, Record No. 2012.0640B/ENX (598 Brannan Street), hearing June 6, 2019",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2012.0640ENX.pdf",
    "sha256": "9d8e75366f1360b20d663b25cd5fe942ea22e63b1c7e95fa5641b5f12eae3490",
    "file": "2012.0640ENX.pdf",
    "site_page": 115,
    "roof_page": 116,
}
MINUTES_URL = "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20190606_cal_min.pdf"
PARCELS_URL = "https://data.sf.gov/d/acdm-wktn"

BLACK = (0.0, 0.0, 0.0, 1.0)  # site plan: ground-floor outlines (heavy stroke)
OUTLINE = (0.746, 0.676, 0.668, 0.898)  # roof plan: roof outlines (dark grey stroke)

# Expected bounding boxes (x0, top, x1, bottom), PDF points, of the outlines read from each page.
SITE_BBOX = {
    "b1": (223.5, 498.1, 432.3, 641.0),
    "b2_a": (223.5, 322.7, 503.4, 458.2),  # Building 2 is drawn as two open paths
    "b2_b": (223.5, 322.6, 401.7, 467.0),
    "b3": (493.6, 147.1, 714.9, 265.3),
}
ROOF_BBOX = {
    "b1": (239.4, 503.6, 445.7, 627.4),
    "b2": (254.6, 349.4, 512.5, 452.5),
    "b3": (493.7, 161.4, 707.0, 226.5),
}

# Lot corners shown on each page (PDF points, y down) and, for each, the lot and a point near that corner of it in
# UTM 10N; the code snaps the point to the nearest vertex of that lot.
SITE_CONTROLS = [
    ("5th and Brannan streets (lot 045)", (223.48, 641.01), "3777045", (552948.1, 4181212.8)),
    ("5th Street at Welsh Street (lot 045)", (223.52, 322.59), "3777045", (552871.0, 4181289.2)),
    ("Brannan Street, east corner of lot 045", (470.99, 642.09), "3777045", (553007.1, 4181272.3)),
    ("Bryant Street, west corner of lot 050", (470.99, 147.09), "3777050", (552887.6, 4181390.8)),
    ("lot 050, 160 ft from Bryant Street", (470.99, 290.64), "3777050", (552922.5, 4181356.2)),
    ("Bryant Street, east corner of former lot 052 (lot 177)", (718.51, 147.14), "3777177", (552947.1, 4181450.4)),
    ("east corner of former lot 052 at Freelon Street (lot 176)", (718.51, 466.48), "3777176", (553024.0, 4181374.2)),
]
ROOF_CONTROLS = [
    ("5th and Brannan streets (lot 045)", (225.99, 640.85), "3777045", (552948.1, 4181212.8)),
    ("Brannan Street, east corner of lot 045", (472.53, 640.8), "3777045", (553007.1, 4181272.3)),
    ("Bryant Street, west corner of lot 050", (472.53, 147.71), "3777050", (552887.6, 4181390.8)),
    ("lot 050, 160 ft from Bryant Street", (472.53, 290.71), "3777050", (552922.5, 4181356.2)),
    ("Bryant Street, east corner of former lot 052 (lot 177)", (719.1, 147.76), "3777177", (552947.1, 4181450.4)),
    ("east corner of former lot 052 at Freelon Street (lot 176)", (719.1, 465.86), "3777176", (553024.0, 4181374.2)),
]


def _close(a, b, tol=0.002) -> bool:
    return isinstance(a, (list, tuple)) and len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def _bbox_ok(o, want, tol=1.0) -> bool:
    return all(abs(v - w) <= tol for v, w in zip((o["x0"], o["top"], o["x1"], o["bottom"]), want))


def _pick(page, want, test):
    hits = [o for o in page.rects + page.curves if test(o) and _bbox_ok(o, want)]
    if not hits:
        raise SystemExit(f"page {page.page_number}: no outline at {want}")
    return [tuple(p) for p in hits[0]["pts"]]


def _valid(g):
    """A valid polygon without slivers: a tiny mitred inward and outward buffer."""
    g = shapely.make_valid(g).buffer(0)
    return g.buffer(-0.01, join_style="mitre").buffer(0.01, join_style="mitre")


def read_site(page) -> dict[str, Polygon]:
    heavy = lambda o: o.get("stroke") and _close(o.get("stroking_color"), (0.0, 0.0, 0.0, 0.984), 0.01)
    out = {
        "b1": Polygon(_pick(page, SITE_BBOX["b1"], heavy)),
        "b3": Polygon(_pick(page, SITE_BBOX["b3"], heavy)),
    }
    a = _pick(page, SITE_BBOX["b2_a"], heavy)  # (455.9, 458.2) ... (223.5, 322.7)
    b = _pick(page, SITE_BBOX["b2_b"], heavy)  # (400.8, 458.6) ... (223.5, 322.6)
    out["b2"] = Polygon(list(reversed(a)) + b)
    return {k: _valid(v) for k, v in out.items()}


def read_roof(page) -> dict[str, Polygon]:
    grey = lambda o: (o.get("stroke") and _close(o.get("stroking_color"), OUTLINE, 0.01)
                      and abs((o.get("linewidth") or 0) - 0.583) < 0.05)
    return {k: _valid(Polygon(_pick(page, ROOF_BBOX[k], grey))) for k in ROOF_BBOX}


def fit(fc: dict, controls) -> trace.Similarity:
    lots = {}
    for f in fc["features"]:
        g = gpd.GeoSeries([shapely.make_valid(shape(f["geometry"]))], crs=4326).to_crs(UTM).iloc[0]
        lots[f["properties"]["blklot"]] = shapely.get_coordinates(g.boundary)
    src, dst, labels = [], [], []
    for label, fig, lot, near in controls:
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
        site = read_site(doc.pages[PACKET["site_page"] - 1])
        roof = read_roof(doc.pages[PACKET["roof_page"] - 1])

    fc_lots = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    fits = {"site": fit(fc_lots, SITE_CONTROLS), "roof": fit(fc_lots, ROOF_CONTROLS)}
    for name, sim in fits.items():
        print(f"[598-brannan] {name} plan -> parcels: RMS {sim.rms_m:.2f} m, scale {sim.scale / 0.3048:.4f} ft/pt "
              f"(drawing scale 1\" = 80' is {80 / 72:.4f})")

    ground = {k: _valid(fits["site"].geometry(g)) for k, g in site.items()}
    top = {k: _valid(fits["roof"].geometry(g)) for k, g in roof.items()}
    lots = ob._utm_shapes(fc_lots)
    site_all = lots.union_all()
    lot176 = next(shapely.make_valid(g) for g, f in zip(lots, fc_lots["features"])
                  if f["properties"]["blklot"] == "3777176")

    src_site = f"{PACKET['title']}, PDF p. {PACKET['site_page']} (site plan)"
    src_roof = f"{PACKET['title']}, PDF p. {PACKET['roof_page']} (roof plan)"
    motion = f"{PACKET['title']}, draft Large Project Authorization (PDF p. 9), approved as Motion 20459"
    parts = []
    for key, name, roof_ft, step_ft, step_level, phase, use_top, use_base, desc in [
        ("b1", "Building 1", 160, 31, "level 3", "Phase 1", "Office (289,087 sq ft)",
         "Office, with shops and PDR space on the ground floor",
         "Building 1, at 5th and Brannan streets: an 11-story office building, 160 ft to the roof (180 ft with the "
         "rooftop mechanical screen), with 289,087 sq ft of office and 22,831 sq ft of retail and PDR space."),
        ("b2", "Building 2", 185, 73, "level 6", "Phase 1", "Office (422,049 sq ft)",
         "Office, with shops and PDR space on the ground floor",
         "Building 2, at 5th and Welsh streets: a 13-story office building, 185 ft to the roof (205 ft with the "
         "rooftop mechanical screen), using the 25-ft height bonus for the affordable housing site and the park, "
         "with 422,049 sq ft of office and 27,036 sq ft of retail and PDR space."),
        ("b3", "Building 3", 150, 76, "level 6", "Phase 2", "Office (211,601 sq ft)",
         "Office, with PDR space and a child care center on the ground floor",
         "Building 3, mid-block on Bryant Street: a 10-story office building, 150 ft to the roof (170 ft with the "
         "rooftop mechanical screen), with 211,601 sq ft of office, 11,054 sq ft of retail and PDR space and a "
         "5,546 sq ft child care center."),
    ]:
        tower = top[key]
        base = _valid(ground[key].difference(tower.buffer(0.05)))
        parts.append((f"{name}", tower, roof_ft, use_top, phase,
                      f"illustrative: the roof outline traced from the {src_roof}; roof height from the {motion}",
                      desc + " Its upper floors are drawn as the roof outline, down to the ground; their terraces "
                             "and the mechanical screen are not."))
        parts.append((f"{name} base", base, step_ft, use_base, phase,
                      f"illustrative: the ground-floor outline traced from the {src_site}, less the upper floors, "
                      f"up to {step_level} ({step_ft} ft) in the elevations of the same packet",
                      f"The lower floors of {name} where they reach beyond its upper floors, up to {step_level} "
                      f"(about {step_ft} ft)."))

    features = []
    for label, geom, h, use, phase, source, note in parts:
        off = geom.difference(site_all.buffer(1.0)).area
        print(f"[598-brannan] {label}: {geom.area * SQFT:,.0f} sq ft, {h} ft, {off * SQFT:,.0f} sq ft outside the lots")
        wgs = gpd.GeoSeries([_valid(geom.simplify(0.2))], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": phase, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })

    print(f"[598-brannan] 160 Freelon Street (lot 176): {lot176.area * SQFT:,.0f} sq ft")
    features.append({
        "type": "Feature",
        "properties": {
            "kind": "block", "label": "160 Freelon Street (affordable housing)", "stage": "construction",
            "height_ft": None, "podium_ft": None, "base_ft": 0, "use": "Homes (85, all affordable)", "phase": None,
            "illustrative": False,
            "source": "DataSF Parcels – Active and Retired, block 3777 lot 176 (the dedicated affordable housing site)",
            "note": ("The lot the project dedicated to the City for affordable housing, where a nine-story building "
                     "with 85 affordable homes has been under construction since July 2025 (DBI permit "
                     "202209283327). Its height in feet isn't in the records read, so the lot is outlined, not "
                     "raised."),
        },
        "geometry": mapping(gpd.GeoSeries([_valid(lot176.simplify(0.2))], crs=UTM).to_crs(4326).iloc[0]),
    })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the three approved office buildings traced from the 2019 plan set's site "
                        "and roof plans and drawn to the roof heights in the approval: Building 1 at 160 ft on 5th "
                        "and Brannan streets, Building 2 at 185 ft on 5th and Welsh streets and Building 3 at 150 ft "
                        "on Bryant Street, each with its lower floors to where it steps back. The affordable housing "
                        "site at 160 Freelon Street, under construction, is outlined. Terraces, mechanical screens "
                        "and the public park are not drawn."),
            "note": "The approved buildings as simple volumes at their roof heights, not the final designs.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2019 (PDF)",
            "approvalSourceUrl": MINUTES_URL,
            "georeference": {
                "page_115": fits["site"].report(),
                "page_116": fits["roof"].report(),
                "method": ("Lot corners drawn on each plan (lots 045, 050 and the former 052, now 176 and 177) matched "
                           "to DataSF parcel vertices by a least-squares similarity."),
            },
            "license": ("Footprints: traced from a public SF Planning document. Georeference and the affordable "
                        "housing lot: DataSF parcels (ODC-PDDL)."),
        },
        "features": features,
    }
    for f in fc["features"]:
        if not shape(f["geometry"]).is_valid:
            raise SystemExit(f"invalid geometry: {f['properties']['label']}")
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[598-brannan] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
