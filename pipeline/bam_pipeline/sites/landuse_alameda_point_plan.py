"""Alameda Point (rest of the base): boundary and land-use zones from the City of Alameda's zoning GIS.

The rest of the former Naval Air Station Alameda is plan-scale (SPEC §7): the 2014 Alameda Point zoning
(AMC 30-4.24) and EIR, the Main Street Neighborhood Specific Plan (2017) and the Town Center and Waterfront
Precise Plan (2014) set what can be built, but outside Site A and West Midway/RESHAP no developer has been
chosen. So the map draws a boundary and the zoning districts only, no buildings.

- Zones: City of Alameda ArcGIS Online "Zoning v03" (Zoning_v03/FeatureServer/0), the Alameda Point districts
  as published: AP-MS (Main Street Neighborhood), AP-AR (Adaptive Reuse), AP-WTC (Waterfront Town Center),
  AP-E1 to AP-E4 (Enterprise District) and AP-OS (Open Space). AP-NR/G, the Nature Reserve (the federal
  wildlife refuge land), isn't a development area and is left out.
- Cut out: the two Alameda Point projects mapped on their own, Site A (data/boundaries/alameda-point.geojson,
  traced from its 2022 Development Plan) and West Midway and RESHAP (data/boundaries/west-midway-reshap.geojson,
  County parcels). Slivers left along the traced Site A edge are dropped.
- Boundary: the union of the zones drawn, written to data/boundaries/alameda-point-plan.geojson.

District descriptions are quoted from City staff reports (Legistar), not paraphrased from memory:
the June 8, 2026 Planning Board study session on Main Street Neighborhood North (matter 15882), the
Nov 2025 Enterprise District report (matter 15362), the May 2025 Pacific Fusion report (matter 14861) and
the Dec 6, 2025 Alameda Point housing update (Exhibit 1 to matter 15882).

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_alameda_point_plan
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

import geopandas as gpd
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "alameda-point-plan"
STAGE = "entitled"  # data/projects.json
UTM = tb.UTM
ACRE_M2 = tb.ACRE_M2
RAW = config.ROOT / "data" / "raw" / "landuse"
OUT = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
LAYER = "https://services9.arcgis.com/ucDLsG1EwPnOGY4c/arcgis/rest/services/Zoning_v03/FeatureServer/0"
WHERE = "zone LIKE 'AP-%'"
ZONING = {
    "url": f"{LAYER}/query?" + urllib.parse.urlencode({"where": WHERE, "outFields": "objectid,zone,description",
                                                       "orderByFields": "objectid", "outSR": 4326, "f": "geojson"}),
    "file": "ap-zoning-v03.geojson",
}
CUTS = ["alameda-point", "west-midway-reshap"]
MSNN = "https://webapi.legistar.com/v1/alameda/matters/15882/texts/17089"
ED_2025 = "https://webapi.legistar.com/v1/alameda/matters/15362/texts/16546"
PF_2025 = "https://webapi.legistar.com/v1/alameda/matters/14861/texts/16009"
HOUSING_2025 = "https://legistar1.granicus.com/alameda/attachments/f39cda77-9fb6-4fe0-a9e7-2408361ab198.pdf"
QUOTES = {
    MSNN: ["The Main Street Neighborhood Specific Plan and Alameda Point-Main Street (\"AP-MS\") zoning regulations "
           "contemplate a mix of historic preservation, adaptive reuse, infill development, residential uses",
           "Existing AP-AR zoning generally allows adaptive reuse, commercial, institutional, assembly, waterfront, "
           "and community-serving uses, but does not currently allow new residential development"],
    ED_2025: ["The zoning is highly flexible, allowing for nearly any job generating use but prohibiting residential "
              "use, aside from a 100-foot \"buffer\" area."],
    PF_2025: ["designated for high-quality research and development (R&D), industrial, manufacturing, and office uses "
              "in the 2014 Alameda Point Zoning and EIR"],
}

# zone code(s) -> label, category, note
DISTRICTS = {
    "AP-MS": ("Main Street Neighborhood (AP-MS)", "residential",
              "The Main Street Neighborhood Specific Plan (2017) and AP-MS zoning \"contemplate a mix of historic "
              "preservation, adaptive reuse, infill development, residential uses, and limited neighborhood-serving "
              "commercial and community-serving uses\", mostly two to four stories (Planning Board study session, "
              "June 8, 2026). The City is weighing a developer search for Main Street Neighborhood North, where a "
              "feasibility study found room for about 600 to 1,000 homes. West Midway and RESHAP, in this district, "
              "are mapped as their own project. Category: residential."),
    "AP-AR": ("Adaptive reuse (AP-AR)", "commercial",
              "\"Existing AP-AR zoning generally allows adaptive reuse, commercial, institutional, assembly, "
              "waterfront, and community-serving uses, but does not currently allow new residential development\", "
              "except reuse of Building 17 (Planning Board study session, June 8, 2026). The Navy-era hangars and "
              "the historic district; the City leases and sells buildings here. Category: commercial."),
    "AP-WTC": ("Waterfront Town Center (AP-WTC)", "mixed-use",
               "Governed by the Town Center and Waterfront Precise Plan (2014). Site A, in this district, is mapped "
               "as its own project; the rest wraps the Seaplane Lagoon. Category: mixed-use."),
    "AP-E": ("Enterprise District (AP-E1 to AP-E4)", "industrial",
             "About 100 acres \"designated for high-quality research and development (R&D), industrial, "
             "manufacturing, and office uses\" (City Council report, May 2025); the zoning allows \"nearly any job "
             "generating use but prohibiting residential use\" (Nov 2025). Pacific Fusion's option on 13 acres for a "
             "fusion research facility ended in 2025 when it chose New Mexico. Category: industrial."),
    "AP-OS": ("Open space (AP-OS)", "open-space",
              "Alameda Point's open space district, including the shoreline park land on the base's northwest "
              "edge and south of the Enterprise District. Category: open-space."),
}
ORDER = ["AP-MS", "AP-WTC", "AP-AR", "AP-E", "AP-OS"]


def _fetch() -> gpd.GeoDataFrame:
    path = RAW / ZONING["file"]
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(ZONING["url"], headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            path.write_bytes(r.read())
    print(f"[alameda-point-plan] zoning query sha256 {hashlib.sha256(path.read_bytes()).hexdigest()[:16]}")
    g = gpd.read_file(path)
    if g.empty:
        raise SystemExit("Alameda zoning: the query returned no features")
    return g.to_crs(UTM)


def _quotes() -> None:
    for url, qs in QUOTES.items():
        cache = RAW / f"ap-legistar-{url.rsplit('/', 3)[-3]}.json"
        if not cache.exists():
            with urllib.request.urlopen(url) as r:
                cache.write_bytes(r.read())
        text = " ".join(json.loads(cache.read_text())["MatterTextPlain"].split())
        for q in qs:
            if q not in text:
                raise SystemExit(f"{url} no longer says {q!r}")


def _clean(g):
    # An 8-m opening drops the breakwaters and the slivers left along the cut edges (piers stay).
    g = shapely.make_valid(g).buffer(-8, join_style="mitre").buffer(8, join_style="mitre").simplify(0.8)
    parts = [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area >= 0.5 * ACRE_M2]
    return trace.as_multipolygon(shapely.union_all(parts)) if parts else None


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    _quotes()
    z = _fetch()
    z["code"] = z["zone"].where(~z["zone"].str.match(r"AP-E\d"), "AP-E")
    unknown = sorted(set(z["code"]) - set(DISTRICTS) - {"AP-NR/G"})
    if unknown:
        raise SystemExit(f"unmapped Alameda Point districts: {unknown}")
    cut = shapely.union_all([gpd.read_file(config.ROOT / "data" / "boundaries" / f"{c}.geojson").to_crs(UTM)
                             .geometry.iloc[0] for c in CUTS]).buffer(1)

    zones = {}
    for code in ORDER:
        g = shapely.union_all(z[z["code"] == code].geometry.to_numpy())
        cleaned = _clean(g.difference(cut))
        if cleaned is not None:
            zones[code] = cleaned
    site = shapely.union_all(list(zones.values())).buffer(0.5).buffer(-0.5)
    site = shapely.make_valid(site.simplify(1.0))

    acres = site.area / ACRE_M2
    tb.write(PROJECT_ID, site, {
        "source": ("City of Alameda zoning (Zoning v03): the Alameda Point districts AP-MS, AP-AR, AP-WTC, AP-E1 to "
                   "AP-E4 and AP-OS, less Site A and West Midway/RESHAP (mapped on their own) and the AP-NR/G Nature "
                   "Reserve"),
        "sourceLabel": "City of Alameda zoning (GIS)",
        "sourceUrl": LAYER,
        "query": ZONING["url"],
        "accuracy": "approximate",
        "accuracyNote": (f"The City's Alameda Point zoning districts as published, with Site A's traced boundary and "
                         f"the West Midway/RESHAP parcels cut out, so the edge along Site A is approximate. "
                         f"{acres:,.1f} acres as drawn."),
        "license": "City of Alameda ArcGIS Online (no license stated)",
    })

    feats, report = [], []
    for code, g in zones.items():
        label, category, note = DISTRICTS[code]
        ac = g.area / ACRE_M2
        report.append(f"  {label:<40} {category:<11} {ac:7.1f} ac")
        feats.append({"type": "Feature", "properties": {
            "kind": "zone", "category": category, "label": label, "district": code,
            "source": f"GIS: City of Alameda Zoning v03, query {WHERE}, zone {code if code != 'AP-E' else 'AP-E1 to AP-E4'}",
            "note": f"{note} {ac:,.1f} acres as drawn.", "stage": STAGE, "acres": round(ac, 1),
        }, "geometry": mapping(tb.to_wgs(g))})
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": ("The Alameda Point zoning districts outside Site A and West Midway/RESHAP, as published in the "
                        "City of Alameda's zoning GIS: the Main Street Neighborhood, Waterfront Town Center, Adaptive "
                        "Reuse and Enterprise districts and open space. The Nature Reserve is left out. Zones, not "
                        "buildings; the plans' height and density limits aren't shown."),
            "note": "Alameda Point zoning districts (2014) from the City's GIS; zones, not buildings.",
            "sourceUrl": LAYER,
            "sourceLabel": "City of Alameda zoning (GIS)",
            "georeference": "GIS as published (City of Alameda Zoning v03, requested in WGS84).",
            "license": "City of Alameda ArcGIS Online (no license stated)",
            "documents": [LAYER, ZONING["url"], MSNN, ED_2025, PF_2025, HOUSING_2025],
        },
        "features": feats,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), indent=1, ensure_ascii=False) + "\n")
    print("\n".join(report))
    print(f"[alameda-point-plan] wrote {OUT.relative_to(config.ROOT)} ({len(feats)} zones, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
