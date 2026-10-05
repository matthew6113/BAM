"""Project boundaries from official GIS layers (Milestone 3).

Each project's site comes from a layer its city or county publishes: a special use district,
a redevelopment project area, a height district, a specific plan boundary, a planned
development zoning file, or the assessor's parcels named in an approval. The source and a
plain note on how well it matches the project are written into each boundary file.

Projects without a usable layer are traced from official figures instead (see the other
modules in this package); they aren't listed here.

    uv run --directory pipeline python -m bam_pipeline.sites.official_boundaries [project-id ...]
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request

import geopandas as gpd
import shapely
from shapely.geometry import mapping, shape

from .. import config

UTM = "EPSG:26910"
RAW = config.ROOT / "data" / "raw" / "boundaries"
OUT = config.ROOT / "data" / "boundaries"
ACRE_M2 = 4046.8564224

DATASF = "https://data.sf.gov"
SF_SUD = "5yf5-ms5f"  # Zoning Map - Special Use Districts (Public Domain U.S. Government)
SF_REDEV = "m288-24sn"  # Former San Francisco Redevelopment Agency Project Areas (ODC-PDDL)
SF_HEIGHT = "h9wh-cg3m"  # Zoning Map - Height and Bulk Districts (Public Domain U.S. Government)
SF_PARCELS = "acdm-wktn"  # Parcels - Active and Retired (ODC-PDDL)
SCC_PARCELS = ("https://data.sccgov.org", "ubcd-cewv")  # Santa Clara County parcels

MENLO_PARCELS = "https://services7.arcgis.com/uRrQ0O3z2aaiIWYU/arcgis/rest/services/City_of_Menlo_Park_Parcels/FeatureServer/7"
MV_PARCELS = "https://maps.mountainview.gov/arcgis/rest/services/Public/Parcel/MapServer/0"
BRISBANE_BSP = ("https://services9.arcgis.com/UGpGSV1ugL0pHSgX/arcgis/rest/services/"
                "Baylands_Specific_Plan_Boundary_DRAFT_Map_WFL1/FeatureServer/1")
SJ_ZONING = "https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/401"
SUNNYVALE_SP = "https://gis.sunnyvale.ca.gov/arcgis/rest/services/GeneralPlan/MapServer/8"
ALCO_PARCELS = "https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Parcels/FeatureServer/0"
OAK_ZONING = "https://services.arcgis.com/9tC74aDHuml0x5Yz/arcgis/rest/services/Zoning_Group_Layers_/FeatureServer/0"

NORTH_BAYSHORE_APNS = [  # Mountain View Legistar matter 7641 (North Bayshore Master Plan, PL-2021-248)
    "116-02-037", "116-02-081", "116-02-083", "116-02-084", "116-02-088", "116-10-070", "116-10-077",
    "116-10-078", "116-10-079", "116-10-080", "116-10-084", "116-10-085", "116-10-086", "116-10-088",
    "116-10-089", "116-10-095", "116-10-097", "116-10-101", "116-10-104", "116-10-102", "116-10-105",
    "116-10-107", "116-10-108", "116-11-012", "116-11-022", "116-11-024", "116-11-025", "116-11-028",
    "116-11-030", "116-11-038", "116-11-039", "116-13-027", "116-13-034", "116-13-038", "116-14-058",
    "116-14-066", "116-14-072", "116-20-043",
]


def _sql_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def socrata(base: str, dataset: str, where: str) -> dict:
    q = urllib.parse.urlencode({"$where": where, "$limit": 5000})
    return {"url": f"{base}/resource/{dataset}.geojson?{q}", "landing": f"{base}/d/{dataset}"}


def arcgis(layer: str, where: str) -> dict:
    q = urllib.parse.urlencode({"where": where, "outFields": "*", "outSR": 4326, "f": "geojson"})
    return {"url": f"{layer}/query?{q}", "landing": layer}


# id -> source query, the layer's name, what the shape covers, accuracy and license.
SPECS: dict[str, dict] = {
    "pier-70": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Pier 70'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Pier 70”",
        "accuracy": "official",
        "note": "The 35-acre Pier 70 Special Use District, which contains the 28-Acre Site and the Illinois Street parcels.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "mission-rock": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Mission Rock'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Mission Rock”",
        "accuracy": "official",
        "note": "The Mission Rock Special Use District (Seawall Lot 337 and Pier 48).",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "india-basin": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'India Basin SUD'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “India Basin SUD”",
        "accuracy": "official",
        "note": "The India Basin Special Use District: the private development site. The Rec and Park shoreline parks are outside it.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "balboa-reservoir": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Balboa Reservoir'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Balboa Reservoir”",
        "accuracy": "official",
        "note": "The Balboa Reservoir Special Use District (the 16.5-acre Project Site); the SFPUC pipeline strip along the south edge is outside it.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "stonestown": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Stonestown Special Use District'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Stonestown Special Use District”",
        "accuracy": "official",
        "note": "The Stonestown Special Use District. The existing mall is outside it.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "parkmerced": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Parkmerced'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Parkmerced”",
        "accuracy": "official",
        "note": "The Parkmerced Special Use District, including its streets.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "mission-bay": {
        "label": "DataSF redevelopment project areas",
        **socrata(DATASF, SF_REDEV, "project_ar in ('Mission Bay - North', 'Mission Bay - South')"),
        "layer": "DataSF Former Redevelopment Agency Project Areas, “Mission Bay - North” and “Mission Bay - South”",
        "accuracy": "official",
        "note": "The Mission Bay North and South redevelopment project areas, including some water and street edges.",
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "candlestick-point": {
        "label": "DataSF redevelopment project areas",
        **socrata(DATASF, SF_REDEV, "project_ar = 'Bayview Hunters Point Area B Zone 1'"),
        "layer": "DataSF Former Redevelopment Agency Project Areas, “Bayview Hunters Point Area B Zone 1”",
        "accuracy": "official",
        "note": "Zone 1 of Bayview Hunters Point Area B, the Candlestick Point redevelopment area (about 272 acres).",
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "hunters-point-shipyard": {
        "label": "DataSF height districts",
        **socrata(DATASF, SF_HEIGHT, "height = 'HP'"),
        "layer": "DataSF Zoning Map – Height and Bulk Districts, “HP”",
        "accuracy": "official",
        "note": "The Shipyard Phase 2 height district (about 421 acres). Phase 1 on the hilltop is outside it.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "treasure-island": {
        "label": "DataSF height districts",
        **socrata(DATASF, SF_HEIGHT, "height like '%-TI%' or height like '%YBI%'"),
        "layer": "DataSF Zoning Map – Height and Bulk Districts, the “-TI” and “YBI” districts",
        "accuracy": "official",
        "note": "Treasure Island and Yerba Buena Island height districts. The Job Corps campus and federal land are outside them.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "parkline": {
        "label": "Menlo Park parcels",
        **arcgis(MENLO_PARCELS, f"APN in ({_sql_list(['062390050', '062390660', '062390670', '062390730', '062390760', '062390780'])})"),
        "layer": "City of Menlo Park parcels, the six APNs in Council resolution 25-143-CC",
        "accuracy": "official",
        "note": "The six parcels approved for the Parkline master plan (about 64 acres).",
        "license": "CC0 (City of Menlo Park)",
    },
    "north-bayshore": {
        "label": "Mountain View parcels",
        **arcgis(MV_PARCELS, f"APN in ({_sql_list(a.replace('-', '') for a in NORTH_BAYSHORE_APNS)})"),
        "layer": "City of Mountain View parcels, the APNs in Legistar matter 7641",
        "accuracy": "approximate",
        "note": "Parcels named in the master plan approval. The plan covers only parts of the Gateway parcels and Shoreline Amphitheatre Lot C, so this is approximate.",
        "license": "City of Mountain View open data (use at your own risk)",
    },
    "brisbane-baylands": {
        "label": "Brisbane’s draft plan boundary",
        **arcgis(BRISBANE_BSP, "1=1"),
        "layer": "City of Brisbane, Baylands Specific Plan Boundary (marked draft, 2022)",
        "accuracy": "approximate",
        "note": "The city's draft specific plan boundary layer, about 700 acres against the plan's 680.1. Approximate until a final layer or the 2026 plan figures are traced.",
        "license": "City of Brisbane public layer (no license stated)",
    },
    "related-santa-clara": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, "apn in ('10403043', '10403042', '10403041', '10403036', '10401102', '09701039', '09701073')"),
        "layer": "Santa Clara County parcels, the seven APNs in Santa Clara resolutions 25-9465 and 25-9467",
        "accuracy": "official",
        "note": "The seven parcels of the Related Santa Clara (City Place) site, about 239 acres.",
        "license": "Santa Clara County open data (terms of use)",
    },
    "downtown-west": {
        "label": "San José zoning",
        # Two of the 16 DC(PD) polygons (under blocks D5-D7) store the file number as "19039".
        **arcgis(SJ_ZONING, "REZONINGFILE like 'PDC19-039%' or REZONINGFILE = '19039'"),
        "layer": "City of San José Zoning Districts, rezoning file PDC19-039 (16 DC(PD) polygons)",
        "accuracy": "approximate",
        "note": "The planned development zoning approved May 25, 2021: about 58 net acres, without the streets and creek in the 80-acre gross figure.",
        "license": "CC-BY 4.0, City of San José",
    },
    "moffett-park": {
        "label": "Sunnyvale specific plan boundary",
        **arcgis(SUNNYVALE_SP, "SP_Code = 'MP'"),
        "layer": "City of Sunnyvale General Plan, Specific Plan Boundary “MP”",
        "accuracy": "official",
        "note": "The Moffett Park Specific Plan area (about 1,270 acres).",
        "license": "City of Sunnyvale GIS (no license stated)",
    },
    "the-rise": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, "apn in ('31620121', '31620122')"),
        "layer": "Santa Clara County parcels 316-20-121 and 316-20-122",
        "accuracy": "official",
        "note": "The two parcels of the former Vallco site named in the Phase 1 final map report (about 50 acres).",
        "license": "Santa Clara County open data (terms of use)",
    },
    "oakland-coliseum": {
        "label": "Alameda County parcels",
        **arcgis(ALCO_PARCELS, "APN in ('41-3901-8', '41-3901-9')"),
        "layer": "Alameda County Assessor parcels 41-3901-8 (Stadium) and 41-3901-9 (Arena)",
        "accuracy": "official",
        "note": "The Stadium and Arena parcels, about 112 acres.",
        "license": "Alameda County open data (county disclaimer)",
    },
    "brooklyn-basin": {
        "label": "Oakland zoning",
        **arcgis(OAK_ZONING, "BASEZONE = 'D-OTN'"),
        "layer": "City of Oakland zoning, D-OTN (Ordinance 12759)",
        "accuracy": "approximate",
        "note": "The development parcels zoned D-OTN (about 31 acres). The parks and open space, about half the 64-acre site, sit in a larger open-space zone and aren't drawn yet.",
        "license": "City of Oakland Planning & Building (for reference only)",
    },
}


def fetch(project: str, spec: dict) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{project}.geojson"
    if not cache.exists():
        req = urllib.request.Request(spec["url"], headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            cache.write_bytes(r.read())
    fc = json.loads(cache.read_text())
    if not fc.get("features"):
        raise SystemExit(f"{project}: the query returned no features ({spec['url']})")
    return fc


def build(project: str) -> None:
    spec = SPECS[project]
    fc = fetch(project, spec)
    geoms = [shapely.make_valid(shape(f["geometry"])) for f in fc["features"] if f.get("geometry")]
    utm = gpd.GeoSeries(geoms, crs=4326).to_crs(UTM)
    # Join neighbouring shapes; slivers between adjoining parcels close at 0.5 m.
    site = shapely.union_all(utm.buffer(0.5).to_numpy()).buffer(-0.5)
    # 1 m is well inside map precision and keeps the bundled files small.
    site = site.simplify(1.0, preserve_topology=True)
    acres = site.area / ACRE_M2
    wgs = gpd.GeoSeries([site], crs=UTM).to_crs(4326).iloc[0]
    out = {
        "type": "FeatureCollection",
        "properties": {
            "project": project,
            "source": spec["layer"],
            "sourceLabel": spec["label"],
            "sourceUrl": spec["landing"],
            "query": spec["url"],
            "accuracy": spec["accuracy"],
            "accuracyNote": f"{spec['note']} {acres:,.1f} acres as drawn.",
            "license": spec["license"],
            "features_used": len(geoms),
        },
        "features": [{"type": "Feature", "properties": {"kind": "site", "name": "Project site"}, "geometry": mapping(wgs)}],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{project}.geojson").write_text(json.dumps(_round(out), indent=1) + "\n")
    print(f"[boundaries] {project}: {len(geoms)} features, {acres:,.1f} acres ({spec['accuracy']})")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


def main(ids: list[str]) -> None:
    for project in ids or list(SPECS):
        build(project)


if __name__ == "__main__":
    main(sys.argv[1:])
