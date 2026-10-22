"""524 and 530 Howard Street: the approved 72-story tower as one simple volume.

Sources (no plan drawings could be read):
- SF Planning's record of the project's Transportation Demand Management plan, 2023-010883TDM (DataSF Planning
  records, y673-d69b): "construct a new 72-story, approximately 795-foot (844 feet, including mechanical penthouse
  levels and screening features), residential building (approximately 882,251 gross square feet of building area;
  818,275 square feet of residential Gross Floor Area), with 672 dwelling units".
- The project record 2023-010883PRJ (qvu5-m3a2) is "Closed - Approval Ltr Issued", decision "Approved", and the
  Planning Department's development pipeline (6jgi-cpb4, 2026 Q2) lists the project as "PL Approved" on
  June 18, 2024, with the same 795 ft / 844 ft and 672 homes.
- The site is block 3721 lots 013 and 014 (DBI site permit application 202311170986), the boundary file.

How it's drawn:
- The approval letter and its plans are on a Planning host this research couldn't reach, so the tower's floor plate,
  setbacks and any podium are unknown. The volume is the site inset evenly until its area equals the building's
  average gross floor area per story (about 882,251 sq ft over 72 stories, some 12,250 sq ft), extruded to the
  795-ft roof. Its position and outline are assumptions; the rooftop features to 844 ft, the levels 2-4 garage,
  the level 5 deck and the bridge over Natoma Street to Salesforce Park are not drawn. Illustrative.

Stage: approved; DBI hasn't issued the site permit (application filed Nov 17, 2023), so it's drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_524_howard
"""

from __future__ import annotations

import json

import geopandas as gpd
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "524-howard"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639

RECORD = {
    "title": "SF Planning record 2023-010883TDM (524 and 530 Howard Street), DataSF Planning records",
    "url": "https://data.sf.gov/resource/y673-d69b.json?record_id=2023-010883TDM",
    "file": "2023-010883TDM.json",
}
STORIES = 72
ROOF_FT = 795
TOP_FT = 844
GROSS_SQFT = 882_251
# Phrases the record must still contain, or the module stops (the record is live data, so it isn't pinned by hash).
EXPECT = ["72-story", "795-foot", "844 feet", "882,251 gross square feet", "672 dwelling units"]


def check_record() -> str:
    path = trace.fetch_document(RECORD["url"], config.ROOT / "data" / "raw" / "docs" / RECORD["file"])
    rows = json.loads(path.read_text())
    text = " ".join((r.get("description") or "") for r in rows)
    missing = [p for p in EXPECT if p not in text]
    if missing:
        raise SystemExit(f"524 Howard: the Planning record no longer says {missing}; re-read it and update the module")
    return text


def main() -> None:
    check_record()
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    site = shapely.union_all(ob._utm_shapes(fc).buffer(0.01).to_numpy()).buffer(-0.01)
    target = GROSS_SQFT / STORIES / SQFT  # m2
    lo, hi = 0.0, 20.0
    for _ in range(60):  # even inset whose area is the average gross floor area per story
        mid = (lo + hi) / 2
        if site.buffer(-mid, join_style="mitre").area > target:
            lo = mid
        else:
            hi = mid
    tower = site.buffer(-lo, join_style="mitre")
    print(f"[524-howard] site {site.area * SQFT:,.0f} sq ft; tower {tower.area * SQFT:,.0f} sq ft "
          f"(inset {lo / FT:.1f} ft), roof {ROOF_FT} ft")
    wgs = gpd.GeoSeries([tower.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
    feature = {
        "type": "Feature",
        "properties": {
            "kind": "building", "label": "Tower", "stage": "entitled", "height_ft": ROOF_FT, "podium_ft": None,
            "base_ft": 0, "use": "Homes (672, 68 of them affordable)", "phase": None, "illustrative": True,
            "source": (f"illustrative: the site (DataSF parcels 3721/013 and 014) inset evenly to the average gross "
                       f"floor area per story in the {RECORD['title']} (about {GROSS_SQFT:,} sq ft over {STORIES} "
                       f"stories); roof height from the same record"),
            "note": (f"About {ROOF_FT} ft to the roof, {TOP_FT} ft with mechanical penthouse levels and screening. "
                     "The real floor plate, setbacks and garage podium aren't known from the documents read."),
        },
        "geometry": mapping(wgs),
    }
    out_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (f"Illustrative massing: one simple volume for the approved {STORIES}-story tower, the site inset "
                        f"evenly to the building's average floor area (about 12,250 sq ft) and extruded to the {ROOF_FT}-ft "
                        f"roof. The approved plans weren't available, so the tower's real outline, its garage podium, "
                        f"the rooftop features to {TOP_FT} ft and the bridge to Salesforce Park are not drawn."),
            "note": "A placeholder volume of the approved size, not the design.",
            "sourceUrl": RECORD["url"],
            "sourceLabel": "SF Planning record 2023-010883TDM (DataSF)",
            "georeference": {
                "method": "No drawing: the DataSF parcels of the site, inset evenly (mitred) by the distance printed above.",
                "inset_ft": round(lo / FT, 1),
            },
            "license": "Figures: SF Planning records on DataSF. Lots: DataSF parcels (ODC-PDDL).",
        },
        "features": [feature],
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(out_fc), indent=1) + "\n")
    print(f"[524-howard] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
