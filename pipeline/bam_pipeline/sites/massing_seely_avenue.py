"""Seely Avenue Mixed-Use (San José): illustrative height envelopes on the project's lots.

Sources:
- 0 Seely Avenue Mixed-Use Project Draft EIR (City of San José, January 2024; posted to CEQAnet
  Mar 19, 2024, SCH 2022020565, document 4), Section 2.3:
  - Table 2-1 "Project Components" (doc p. 16, PDF p. 55): homes, retail and lot area for each part:
    townhomes 154 homes on 329,844 sq ft; Building A 397 homes and 6,427 sq ft of retail on 152,096 sq ft;
    Building B 372 and 5,578 on 126,318; Building C 371 and 6,960 on 127,323; the affordable apartment
    building 178 homes on 53,825; the public park 109,549; the well site (Lot 3) 4,576.
  - Table 2-2 "Building Heights" (doc p. 17, PDF p. 56), "measured from ground to roof": Building A 69 ft, Buildings B
    and C 79 ft, the affordable apartment building 82 ft, the townhomes 30 ft. The text: Buildings A, B and C
    are "six stories, seven stories, and seven stories", the affordable building "six-story", the townhomes
    "three stories".
  - Table 2-4 "Project Phasing" (doc p. 36, PDF p. 75): 1 infrastructure and well, 2 townhomes, 3 Building A,
    4 the affordable building, 5 Building B, 6 Building C.
  - Figure 2-4 "Conceptual Site Plan" (KTGY Architecture, June 2023; PDF p. 52) places each building on its
    lot (Lots 1 to 6 and the townhome lots).
- The City Council approved the project on Aug 13, 2024 (notice of determination, CEQAnet document 5); the
  Final EIR (Volume I, Aug 2024) keeps the Draft EIR's description and tables.

How it's drawn: the County's parcel layer now holds the project's subdivision lots, the same parcels the
boundary is built from (official_boundaries.SPECS["seely-avenue"]). Each building's lot is matched to Table 2-1
by area and to Figure 2-4 by position (Building C beside the existing office building on Seely Avenue, the
park in the middle, Building A at Montague Expressway, Building B and the affordable building along the Coyote
Creek levee), and the whole lot is raised to the building's Table 2-2 height. The lots also hold each
building's parking garage and courtyards, so these are envelopes, not building footprints: illustrative. The
26 townhome lots (097-23-141 to -166, the plan's Lots 7 to 32) are each raised to 30 ft. The park, the well
site, the streets and the common lots aren't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_seely_avenue
"""

from __future__ import annotations

import json

import geopandas as gpd
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "seely-avenue"
UTM = ob.UTM
SQFT = 10.7639
DEIR = {
    "title": "0 Seely Avenue Mixed-Use Project Draft EIR (City of San José, January 2024)",
    "url": "https://ceqanet.lci.ca.gov/2022020565/4/Attachment/O2WLAL",
    "sha256": "5913b86367455afcd05921fc9b5277ce4275c57127452db9ebfdc5a865de1e86",
    "file": "deir-2024-03.pdf",
}
NOD_URL = "https://ceqanet.lci.ca.gov/2022020565/5"

# APN -> (label, Table 2-1 lot area in sq ft, Table 2-2 height in ft, stories, use, phase)
BUILDINGS = {
    "09715042": ("Building A", 152_096, 69, 6, "Homes (397 market-rate apartments) over 6,427 sq ft of ground-floor retail",
                 "Phase 3 (Draft EIR schedule: Oct 2024 to Oct 2026)"),
    "09715045": ("Building B", 126_318, 79, 7, "Homes (372 market-rate apartments) over 5,578 sq ft of ground-floor retail",
                 "Phase 5 (Draft EIR schedule: Oct 2025 to Oct 2027)"),
    "09715049": ("Building C", 127_323, 79, 7, "Homes (371 market-rate apartments) over 6,960 sq ft of ground-floor retail",
                 "Phase 6 (Draft EIR schedule: Oct 2026 to Oct 2028)"),
    "09715046": ("Affordable apartment building", 53_825, 82, 6, "Affordable homes (178 apartments)",
                 "Phase 4 (Draft EIR schedule: Apr 2025 to Oct 2026)"),
}
TOWNHOME_APNS = [f"09723{n}" for n in range(141, 167)]
TOWNHOMES_FT = 30
TOWNHOMES_PHASE = "Phase 2 (Draft EIR schedule: Sept 2024 to Jan 2026)"


def lots() -> gpd.GeoDataFrame:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    rows = [{"apn": f["properties"].get("apn"), "geometry": shapely.make_valid(shapely.geometry.shape(f["geometry"]))}
            for f in fc["features"] if f.get("geometry")]
    return gpd.GeoDataFrame(rows, crs=4326).to_crs(UTM)


def main() -> None:
    # The Draft EIR this module transcribes, pinned (about 60 MB).
    trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "official" / PROJECT_ID / DEIR["file"], DEIR["sha256"])
    g = lots()
    by_apn = {r.apn: r.geometry for r in g.itertuples() if r.apn}
    features = []
    checks = {}

    def add(label, geom, h, use, phase, source, note):
        wgs = gpd.GeoSeries([geom.simplify(0.3)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": phase, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })

    for apn, (label, table_sqft, h, stories, use, phase) in BUILDINGS.items():
        geom = by_apn.get(apn)
        if geom is None:
            raise SystemExit(f"seely-avenue: lot {apn} for {label} is missing from the parcel layer")
        drawn = geom.area * SQFT
        diff = drawn / table_sqft - 1
        checks[label] = {"apn": apn, "drawn_sqft": round(drawn), "table_sqft": table_sqft, "diff_pct": round(diff * 100, 1)}
        if abs(diff) > 0.03:
            raise SystemExit(f"seely-avenue: {label} lot {apn} is {drawn:,.0f} sq ft against Table 2-1's {table_sqft:,}")
        add(label, geom, h, use, phase,
            (f"illustrative: County parcel {apn[:3]}-{apn[3:5]}-{apn[5:]} ({label}'s lot, Draft EIR Table 2-1 and "
             f"Figure 2-4) raised to the {h}-ft height in Draft EIR Table 2-2"),
            (f"{stories} stories, {h} ft from ground to roof (Draft EIR Table 2-2). The whole lot is drawn, so the "
             "envelope also covers the building's parking garage and courtyards."))

    town = [by_apn[a] for a in TOWNHOME_APNS if a in by_apn]
    if len(town) != len(TOWNHOME_APNS):
        raise SystemExit(f"seely-avenue: found {len(town)} of {len(TOWNHOME_APNS)} townhome lots")
    for i, (apn, geom) in enumerate(zip(TOWNHOME_APNS, town), start=1):
        add(f"Townhomes {i}", geom, TOWNHOMES_FT, "For-sale townhomes (154 in all)", TOWNHOMES_PHASE,
            (f"illustrative: County parcel {apn[:3]}-{apn[3:5]}-{apn[5:]}, one of the 26 townhome lots (Figure 2-4 "
             "Lots 7 to 32), raised to the 30-ft townhome height in Draft EIR Table 2-2"),
            "Three-story townhomes, 30 ft from ground to roof (Draft EIR Table 2-2).")
    checks["townhome lots"] = {"count": len(town), "drawn_sqft": round(sum(t.area for t in town) * SQFT)}
    for k, v in checks.items():
        print(f"[seely-avenue] {k}: {v}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: each building's lot, as the County now maps the project's subdivision, "
                        "raised to the building's height in the Draft EIR (Building A 69 ft, Buildings B and C 79 ft, "
                        "the affordable building 82 ft, the 26 townhome lots 30 ft). The lots also hold the garages "
                        "and courtyards, so the volumes are envelopes, not the buildings' footprints."),
            "note": "Envelopes on the approved lots, not the final building designs.",
            "sourceUrl": DEIR["url"],
            "sourceLabel": "Seely Avenue Mixed-Use Project Draft EIR, 2024 (PDF)",
            "approvalSourceUrl": NOD_URL,
            "georeference": {
                "method": ("No georeferencing: the lots are Santa Clara County parcels, each matched to Draft EIR Table 2-1 "
                           "by area and to Figure 2-4 by position."),
                "lot_area_checks": checks,
            },
            "license": ("Heights and program: from a public City of San José document. Lots: Santa Clara County open data "
                        "(terms of use)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[seely-avenue] wrote {out.relative_to(config.ROOT)} ({len(features)} features, {out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
