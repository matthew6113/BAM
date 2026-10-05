"""Moffett Park: land-use (zoning) districts of the adopted Moffett Park Specific Plan.

Moffett Park is a plan-scale project (SPEC §7, "Massing rules"): it gets a boundary and land-use
zones only, no buildings. The zones come straight from the City of Sunnyvale's own GIS, used as
published, not traced:

- Base districts: Sunnyvale GIS "ZoningLegend" map service, layer 2 "Zoning District", every
  polygon whose `Zoning` starts with "MP-" (the ten Moffett Park Specific Plan districts the plan's
  zoning ordinance created). The layer was last edited in March 2025, so it carries the zoning as
  adopted by Ordinance 3218-23 (July 25, 2023) and any later map changes.
- Ecological combining district: the same service, layer 1 "Combining District", `CombiningD = 'ECD'`.
  The ECD overlays parts of MP-O1 and MP-E3 in the plan area's northwest corner. Because it bars new
  commercial, industrial, office and residential uses (SMC 19.29.060(b), Ordinance 3218-23 p. 13),
  it is drawn as its own open-space zone carved out of the base districts under it, and its note
  names those districts.

The district names and purposes are from Ordinance 3218-23, Exhibit A (SMC Chapter 19.29), Section
19.29.050 (Attachment 1 pp. 11–12); the ordinance's Exhibit B, Figure 26 "Zoning District Map"
(Attachment 1 p. 26), is the adopted map the GIS layer was checked against. The adopted plan's FAR,
density and height standards (MPSP Table 2, Section 4.4; Figure 30, Section 5.3) aren't given here:
the plan PDF sits on sunnyvale.ca.gov, which refuses scripted downloads, so those numbers are left out
rather than taken from the draft or the staff change matrix.

The zoning layer leaves street rights-of-way unzoned, so streets are not part of any zone here
either. Zones are clipped to the specific plan boundary (data/boundaries/moffett-park.geojson, from
Sunnyvale GIS GeneralPlan layer 8); every MP- polygon already lies inside it. The Lockheed Martin core
campus, which that layer also draws as its own area, is inside the plan area and is zoned MP-E2 (and part
of MP-E3); the Council exempted Lockheed Martin only from the innovation and creation space rules.
The MP-MU minimum density (36 units/acre) is from the Council's adopting motion (July 11, 2023 minutes).

    uv run --directory pipeline python -m bam_pipeline.sites.landuse_moffett_park
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

PROJECT_ID = "moffett-park"
UTM = "EPSG:26910"
ACRE_M2 = 4046.8564224
RAW = config.ROOT / "data" / "raw" / "landuse"
DOCS = config.ROOT / "data" / "raw" / "docs"
OUT = config.ROOT / "data" / "landuse" / f"{PROJECT_ID}.geojson"
STAGE = "entitled"  # data/projects.json

SERVICE = "https://gis.sunnyvale.ca.gov/arcgis/rest/services/ZoningLegend/MapServer"


def _query(layer: int, where: str, fields: str) -> str:
    q = urllib.parse.urlencode({"where": where, "outFields": fields, "orderByFields": "OBJECTID",
                                "outSR": 4326, "f": "geojson"})
    return f"{SERVICE}/{layer}/query?{q}"


ZONING = {
    "layer": f"{SERVICE}/2",
    "name": "Sunnyvale GIS ZoningLegend layer 2 “Zoning District”",
    "where": "Zoning LIKE 'MP-%'",
    "url": _query(2, "Zoning LIKE 'MP-%'", "OBJECTID,Zoning"),
    "file": "mp-zoning-districts.geojson",
    # The query output is byte-stable; a changed hash means the city edited the layer.
    "sha256": "c75d12a78378badf1170ca7b621235ddea167492a62e89709e33503b7610b6da",
}
ECD = {
    "layer": f"{SERVICE}/1",
    "name": "Sunnyvale GIS ZoningLegend layer 1 “Combining District”",
    "where": "CombiningD = 'ECD'",
    "url": _query(1, "CombiningD = 'ECD'", "OBJECTID,CombiningD"),
    "file": "mp-combining-ecd.geojson",
    "sha256": "b905854e695ef1423239d58fb67fdaaf3fcb4090ddb368019742ba52f73f3c82",
}
ORDINANCE = {
    "title": "Ordinance 3218-23 (Moffett Park Specific Plan zoning, adopted July 25, 2023)",
    "url": "https://legistar.granicus.com/Sunnyvale/attachments/898afbde-8963-4d24-bc5c-90e388ebed42.PDF",
    "file": "mp-ordinance-3218-23.pdf",
    "sha256": "86f8d13ff4e628c380c933850d13fb1c64b42d003fca57e210c1244a7b721329",
}
MATTER = "https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=13874&GUID=69D247EA-029D-4192-99E3-DA5579E0A8EF"
MINUTES = {
    "title": "City Council minutes, July 11, 2023 (plan adopted as amended)",
    "url": "https://legistar.granicus.com/Sunnyvale/meetings/2023/7/3762_M_City_Council_23-07-11_Meeting_Minutes.pdf",
    "file": "mp-council-minutes-2023-07-11.pdf",
    "sha256": "771c2e27ef813cd650ed349d30d01ba8165665cb7ca03ff05786d4fce6762ada",
}
# The Lockheed Martin core campus, outlined on Figure 26 and drawn in Sunnyvale GIS (GeneralPlan layer 8,
# SP_Code 'LCC'), lies inside the plan area: it is all of MP-E2 and the southern part of MP-E3.
LCC_LAYER = ("https://gis.sunnyvale.ca.gov/arcgis/rest/services/GeneralPlan/MapServer/8/query?"
             + urllib.parse.urlencode({"where": "SP_Code = 'LCC'", "outFields": "*", "outSR": 4326, "f": "geojson"}))

ORD_DISTRICTS = "Ordinance 3218-23, Exhibit A, SMC 19.29.050, p. 11–12"
# District -> (label, category, note). Purposes paraphrase SMC 19.29.050 as adopted.
DISTRICTS: dict[str, tuple[str, str, str]] = {
    "MP-AC": ("MP-AC activity center", "mixed-use",
              "A mix of office, residential and commercial uses, with neighborhood-serving shops, services and "
              f"entertainment in ground-floor storefronts ({ORD_DISTRICTS}). Category: mixed-use."),
    "MP-R": ("MP-R residential", "residential",
             f"Very high-density housing ({ORD_DISTRICTS}). Category: residential."),
    "MP-MU": ("MP-MU mixed use", "mixed-use",
              f"Standalone residential, standalone office, or mixed-use development ({ORD_DISTRICTS}). Housing "
              "here must be built to at least 36 units/acre (City Council motion of July 11, 2023, item 12, "
              "minutes p. 12). Category: mixed-use."),
    "MP-O1": ("MP-O1 office 1", "office",
              "Densification of existing office campuses in the Posolmi and Onizuka neighborhoods; no housing "
              f"({ORD_DISTRICTS}). Category: office."),
    "MP-O2": ("MP-O2 office 2", "office",
              "Higher-intensity corporate and professional office near the activity center, residential and "
              f"mixed-use districts and transit; no housing ({ORD_DISTRICTS}). Category: office."),
    "MP-E1": ("MP-E1 mixed employment 1", "office",
              "Corporate and professional office, light industrial and other non-residential uses in an urban "
              f"pattern with integrated open space; no housing ({ORD_DISTRICTS}). Category: office, the district's "
              "first-named use."),
    "MP-E2": ("MP-E2 mixed employment 2", "industrial",
              f"A mix of office, R&D and industrial uses; no housing ({ORD_DISTRICTS}). This district is the "
              "Lockheed Martin core campus (outlined on Ordinance 3218-23 Figure 26, p. 26; Sunnyvale GIS "
              "GeneralPlan layer 8, 'Lockheed Core Campus'). Category: industrial, the closest fit for an "
              "office/R&D/industrial employment district."),
    "MP-E3": ("MP-E3 mixed employment 3", "industrial",
              "A mix of office, R&D and light industrial; no housing; the ordinance says MP-E3 shall be combined "
              f"with the ecological combining district ({ORD_DISTRICTS}). Category: industrial, as for MP-E2."),
    "MP-H": ("MP-H hospitality", "commercial",
             f"Hotel and hospitality uses; no housing ({ORD_DISTRICTS}). Category: commercial."),
    "MP-PF": ("MP-PF public facilities", "civic",
              "Governmental, public utility and educational buildings and facilities; no housing "
              f"({ORD_DISTRICTS}). Category: civic."),
}
ORDER = ["MP-R", "MP-MU", "MP-AC", "MP-O1", "MP-O2", "MP-E1", "MP-E2", "MP-E3", "MP-H", "MP-PF"]


def _fetch_gis(spec: dict) -> gpd.GeoDataFrame:
    """Download a GIS query once into data/raw/landuse and check its pinned hash.

    trace.fetch_document can't be used here: the Sunnyvale server refuses urllib's default user agent.
    """
    path = RAW / spec["file"]
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(spec["url"], headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            path.write_bytes(r.read())
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != spec["sha256"]:
        raise SystemExit(f"{path.name}: sha256 {got} does not match the pinned {spec['sha256']} "
                         "(the city edited the layer: re-check it, then re-pin)")
    gdf = gpd.read_file(path)
    if gdf.empty:
        raise SystemExit(f"{spec['name']}: the query returned no features")
    return gdf.to_crs(UTM)


def _clean(g):
    """Valid polygons only, 0.5 m simplification, slivers under 0.05 acre dropped."""
    g = shapely.make_valid(g).simplify(0.5, preserve_topology=True)
    parts = [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area >= 0.05 * ACRE_M2]
    return trace.as_multipolygon(shapely.union_all(parts)) if parts else None


def main() -> None:
    # The ordinance is the adopted text the labels and notes come from; pin it.
    trace.fetch_document(ORDINANCE["url"], DOCS / ORDINANCE["file"], ORDINANCE["sha256"])
    trace.fetch_document(MINUTES["url"], DOCS / MINUTES["file"], MINUTES["sha256"])

    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    boundary = shapely.union_all(site.geometry.to_numpy())

    zoning = _fetch_gis(ZONING)
    unknown = sorted(set(zoning["Zoning"]) - set(DISTRICTS))
    if unknown:
        raise SystemExit(f"unmapped Moffett Park districts in the zoning layer: {unknown}")
    ecd = _fetch_gis(ECD)
    ecd_geom = shapely.union_all(ecd.geometry.to_numpy()).intersection(boundary)

    # How much of the layer lies inside the plan boundary (it should be all of it).
    whole = zoning.geometry.area.sum()
    inside = zoning.geometry.intersection(boundary).area.sum()

    features, report = [], []
    under_ecd = []
    for code in ORDER:
        rows = zoning[zoning["Zoning"] == code]
        if rows.empty:
            continue
        g = shapely.union_all(rows.geometry.to_numpy()).intersection(boundary)
        overlap = g.intersection(ecd_geom).area
        if overlap > 0.05 * ACRE_M2:
            under_ecd.append((code, overlap / ACRE_M2))
        whole_ac = g.area / ACRE_M2
        g = _clean(g.difference(ecd_geom))
        if g is None:
            continue
        label, category, note = DISTRICTS[code]
        if overlap > 0.05 * ACRE_M2:
            note += (f" In the city's GIS the ecological combining district covers {overlap / ACRE_M2:,.1f} of the "
                     f"district's {whole_ac:,.1f} acres; that part is drawn as the open-space zone, the rest here.")
        features.append((code, label, category, note, g))

    ecd_note_under = ", ".join(f"{c} ({a:,.1f} acres)" for c, a in under_ecd)
    ecd_clean = _clean(ecd_geom)
    if ecd_clean is not None:
        features.append((
            "ECD", "Ecological combining district", "open-space",
            "Preserves, expands and enhances green space and biological resources in the plan area's northwest "
            "corner, with public access and passive recreation; new commercial, industrial, office and residential "
            "uses aren't allowed (Ordinance 3218-23, Exhibit A, SMC 19.29.050(k) and 19.29.060(b), p. 12–13). "
            f"Overlays {ecd_note_under}. Category: open-space.",
            ecd_clean,
        ))

    out_features = []
    for code, label, category, note, g in features:
        acres = g.area / ACRE_M2
        frac_in = g.intersection(boundary).area / g.area
        report.append(f"  {label:<32} {category:<11} {acres:8.1f} ac  inside {frac_in:.3f}")
        src = (f"GIS: {ECD['name']}, query {ECD['where']}" if code == "ECD"
               else f"GIS: {ZONING['name']}, query Zoning = '{code}'")
        wgs = gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]
        out_features.append({
            "type": "Feature",
            "properties": {
                "kind": "zone",
                "category": category,
                "label": label,
                "district": code,
                "source": src,
                "note": f"{note} {acres:,.1f} acres in the plan area as drawn.",
                "stage": STAGE,
                "acres": round(acres, 1),
            },
            "geometry": mapping(wgs),
        })

    total = sum(f["properties"]["acres"] for f in out_features)
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "summary": (
                f"The Moffett Park Specific Plan's ten zoning districts and its ecological combining district "
                f"({len(out_features)} zones, {total:,.0f} of the plan area's ~1,270 acres), taken as published "
                "from the City of Sunnyvale's zoning GIS layers and clipped to the plan boundary. The ecological "
                "combining district is drawn as its own open-space zone over the office and employment districts "
                "it overlays. Streets aren't zoned in the source, so they're left out. The plan's FAR, density "
                "and height limits (adopted plan Table 2 and Figure 30) aren't shown."
            ),
            "note": "Zoning districts of the adopted 2023 Moffett Park Specific Plan, from Sunnyvale GIS; zones, not buildings.",
            "sourceUrl": ZONING["layer"],
            "sourceLabel": "Sunnyvale zoning districts (GIS)",
            "georeference": ("GIS as published (Sunnyvale ZoningLegend layers 1 and 2, requested in WGS84); "
                             f"{inside / whole:.1%} of the layer's MP- district area lies inside the plan boundary. "
                             "Checked by eye against Ordinance 3218-23 Exhibit B, Figure 26 (p. 26)."),
            "license": "City of Sunnyvale GIS (no license stated)",
            "documents": [ZONING["layer"], ZONING["url"], ECD["layer"], ECD["url"], ORDINANCE["url"], MATTER,
                          MINUTES["url"], LCC_LAYER],
        },
        "features": out_features,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(_round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"[moffett-park] {len(zoning)} MP- polygons ({inside / whole:.1%} of their area inside the boundary), "
          f"{len(ecd)} ECD polygon(s)")
    print("\n".join(report))
    print(f"[moffett-park] wrote {OUT.relative_to(config.ROOT)} ({len(out_features)} zones, {total:,.1f} acres, "
          f"{OUT.stat().st_size // 1024} KB)")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


if __name__ == "__main__":
    main()
