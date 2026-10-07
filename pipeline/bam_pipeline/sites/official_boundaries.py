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
# County of San Mateo parcels (Public Domain). The GeoJSON endpoint returns no geometry: the
# polygon is the WKT text field "shape", in State Plane California III feet.
SMC_PARCELS = ("https://data.smcgov.org", "nr6j-72z7")

MENLO_PARCELS = "https://services7.arcgis.com/uRrQ0O3z2aaiIWYU/arcgis/rest/services/City_of_Menlo_Park_Parcels/FeatureServer/7"
MV_PARCELS = "https://maps.mountainview.gov/arcgis/rest/services/Public/Parcel/MapServer/0"
BRISBANE_BSP = ("https://services9.arcgis.com/UGpGSV1ugL0pHSgX/arcgis/rest/services/"
                "Baylands_Specific_Plan_Boundary_DRAFT_Map_WFL1/FeatureServer/1")
SJ_ZONING = "https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/401"
SUNNYVALE_SP = "https://gis.sunnyvale.ca.gov/arcgis/rest/services/GeneralPlan/MapServer/8"
ALCO_PARCELS = "https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Parcels/FeatureServer/0"
OAK_ZONING = "https://services.arcgis.com/9tC74aDHuml0x5Yz/arcgis/rest/services/Zoning_Group_Layers_/FeatureServer/0"
SC_ZONING = "https://map.santaclaraca.gov/maps/rest/services/OPENDATA/RegionalZoningOpenData/MapServer/0"
SONOMA_PARCELS = "https://socogis.sonomacounty.ca.gov/map/rest/services/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0"
MARIN_PARCELS = "https://gis.marinpublic.com/arcgis/rest/services/BaseMap/Basemap/FeatureServer/13"
EPA_SP_BOUNDARY = ("https://services8.arcgis.com/Qac9ExiTge3RH5x7/arcgis/rest/services/"
                   "2025_EPA_Zoning_Map_WFL1/FeatureServer/0")
EPA_ZONING = "https://services8.arcgis.com/Qac9ExiTge3RH5x7/arcgis/rest/services/Final_Zoning/FeatureServer/0"
# Layer 67 is the adopted plan's own area; layer 3 (zoning "SP-4") runs out over the bay.
VALLEJO_SP = ("https://portal.cityofvallejo.net/arcgis/rest/services/CityGIS_Viewer/"
              "Planning_Development_Services/MapServer/67")

MIDDLEFIELD_PARK_APNS = [  # Mountain View Resolution 18734 (Middlefield Park Master Plan), Legistar matter 6895
    "160-58-001", "160-58-016", "160-58-017", "160-57-004", "160-57-006", "160-57-007", "160-57-008",
    "160-57-009", "160-57-010", "160-57-011", "160-57-012", "160-57-013", "160-59-005", "160-59-006",
]

NORTH_BAYSHORE_APNS = [  # Mountain View Legistar matter 7641 (North Bayshore Master Plan, PL-2021-248)
    "116-02-037", "116-02-081", "116-02-083", "116-02-084", "116-02-088", "116-10-070", "116-10-077",
    "116-10-078", "116-10-079", "116-10-080", "116-10-084", "116-10-085", "116-10-086", "116-10-088",
    "116-10-089", "116-10-095", "116-10-097", "116-10-101", "116-10-104", "116-10-102", "116-10-105",
    "116-10-107", "116-10-108", "116-11-012", "116-11-022", "116-11-024", "116-11-025", "116-11-028",
    "116-11-030", "116-11-038", "116-11-039", "116-13-027", "116-13-034", "116-13-038", "116-14-058",
    "116-14-066", "116-14-072", "116-20-043",
]

ESMERALDA_APNS = [  # Cloverdale Planning Commission staff report, Oct 1, 2026, p. 1 (Esmeralda Specific Plan)
    "117-050-010", "117-050-011", "117-050-012", "117-050-017", "117-050-024", "117-050-026", "117-050-027",
    "117-050-028", "117-050-029", "116-310-013", "116-310-014",
]


UCSF_PARNASSUS_BLKLOTS = [  # DataSF parcels, block 2634A (New Hospital EIR: "Block 2634A/Lot 011 & 005")
    "2634A003", "2634A005", "2634A011", "2634A012",
]

TANFORAN_APNS = [  # Draft EIR p. 53; the vacant lot is 014-311-060 in the NOP and the County layer (014-316-060 in the DEIR)
    "014316080", "014316300", "014316310", "014316360", "014316330", "014311060",
]

NORTHGATE_APNS = [  # San Rafael Resolution 15360 and Ordinance 2043 (Dec 2024)
    "175-060-12", "175-060-40", "175-060-59", "175-060-61", "175-060-66", "175-060-67",
]


def _sql_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def socrata(base: str, dataset: str, where: str) -> dict:
    q = urllib.parse.urlencode({"$where": where, "$limit": 5000})
    return {"url": f"{base}/resource/{dataset}.geojson?{q}", "landing": f"{base}/d/{dataset}"}


def arcgis(layer: str, where: str) -> dict:
    q = urllib.parse.urlencode({"where": where, "outFields": "*", "outSR": 4326, "f": "geojson"})
    return {"url": f"{layer}/query?{q}", "landing": layer}


# University Village, which the Ravenswood/4 Corners plan leaves out (Figure 1-3), in the City's
# zoning parcels: its single-family (R-LD) lots, the school site (PI), the park strip and Jack
# Farrell Park (PR, by APN; the plan's other PR parcels are in the plan area).
RAVENSWOOD_UV = {
    "label": "East Palo Alto zoning parcels",
    **arcgis(EPA_ZONING, "New_Zone in ('R-LD', 'PI') or APN in ('093580010', '063088210')"),
    "url": arcgis(EPA_ZONING, "New_Zone in ('R-LD', 'PI') or APN in ('093580010', '063088210')")["url"]
           + "&" + urllib.parse.urlencode({"geometry": "-122.1418,37.4687,-122.1264,37.4840",
                                           "geometryType": "esriGeometryEnvelope", "inSR": 4326,
                                           "spatialRel": "esriSpatialRelIntersects"}),
    "close_m": 20,  # fills University Village's own streets between its lots
    "open_m": 6,  # drops the street-edge slivers the cut leaves along University Avenue
}


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
    # north-bayshore: traced from the master plan's project area line in landuse_north_bayshore.py.
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
    "berryessa-flea-market": {
        "label": "San José zoning",
        # The layer stores the file number without its prefix; the "PDC17-051" form is matched too in case it changes.
        **arcgis(SJ_ZONING, "REZONINGFILE = '17051' or REZONINGFILE like 'PDC17-051%'"),
        "layer": "City of San José Zoning Districts, rezoning file PDC17-051 (CP(PD), approved June 29, 2021)",
        "accuracy": "official",
        "note": "The planned development zoning of Ordinance 30646, which describes an approximately 61.5-gross-acre site.",
        "license": "CC-BY 4.0, City of San José",
    },
    "tasman-east": {
        "label": "Santa Clara zoning",
        **arcgis(SC_ZONING, "ZONGDSGN = 'TN' and SPPLAN = 'TE'"),
        "layer": "City of Santa Clara zoning, the 37 TN parcels tagged with the Tasman East plan (SPPLAN “TE”)",
        "accuracy": "approximate",
        "note": ("The parcels of the Tasman East Specific Plan area, which the City describes as about 45 acres between "
                 "Tasman Drive, the Guadalupe River, the golf course and Lafayette Street. The plan's own streets are "
                 "outside the parcels, so the shape is net of them. The layer's 10 other TN parcels are retired records "
                 "that lie wholly inside these and add no area."),
        "license": "City of Santa Clara Open Data Portal terms of use (2018)",
    },
    "sunnydale-hope-sf": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Sunnydale Hope SF'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Sunnydale Hope SF”",
        "accuracy": "official",
        "note": "The Sunnydale HOPE SF Special Use District (Planning Code 249.75), the approximately 50-acre site of Ordinance 18-17.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "potrero-hope-sf": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'Potrero Hope SF'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “Potrero Hope SF”",
        "accuracy": "official",
        "note": "The Potrero HOPE SF Special Use District (Planning Code 249.74); Ordinance 15-17 describes an approximately 38-acre site.",
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "middlefield-park": {
        "label": "Mountain View parcels",
        **arcgis(MV_PARCELS, f"APN in ({_sql_list(a.replace('-', '') for a in MIDDLEFIELD_PARK_APNS)})"),
        "layer": "City of Mountain View parcels, the 14 APNs in Resolution 18734 (Middlefield Park Master Plan)",
        "accuracy": "approximate",
        "note": ("The 14 parcels the master plan approves, against the Council report's “approximately 40 acres”. "
                 "Streets between them are left out, and the approved street vacations will change the edges."),
        "license": "City of Mountain View open data (use at your own risk)",
    },
    "mare-island": {
        "label": "Vallejo specific plan areas",
        **arcgis(VALLEJO_SP, "Name = 'Mare Island' and Year = 2005"),
        "layer": "City of Vallejo GIS, Existing Specific Plan Area “Mare Island” (2005)",
        "accuracy": "approximate",
        "note": ("The adopted 2005 Mare Island Specific Plan area, about 3,100 acres; the whole island is 5,250 acres "
                 "in the 2005 EIR. The new specific plan's boundary isn't published, and may differ."),
        "license": "City of Vallejo GIS (no license stated)",
    },
    "esmeralda": {
        "label": "County of Sonoma parcels",
        **arcgis(SONOMA_PARCELS, f"APN IN ({_sql_list(ESMERALDA_APNS)})"),
        "layer": "County of Sonoma Parcels Public Shapefile, the 11 APNs in the Cloverdale Planning Commission staff report of Oct 1, 2026",
        "accuracy": "approximate",
        "note": ("The 11 parcels the Planning Commission staff report lists for the Esmeralda Specific Plan, in two "
                 "pieces either side of the 80-foot SMART rail corridor, which isn't one of the parcels (the plan "
                 "leaves it out of its land-use districts). The County's parcel shapes run a little over the Plan "
                 "Area's 261.44 acres (Addendum Exhibit 3): about 3.8 acres of parcel 116-310-014, a narrow strip "
                 "running northwest from the site's north corner outside Cloverdale's city limits (Permit Sonoma City "
                 "Limits layer), is the roughly 4-acre unincorporated \u201cPanhandle\u201d the plan now excludes, and "
                 "it is still drawn here."),
        "license": "CC BY-SA 3.0, County of Sonoma",
    },
    "ucsf-parnassus": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(UCSF_PARNASSUS_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 2634A lots 003, 005, 011 and 012",
        "accuracy": "approximate",
        "note": ("The four assessor parcels of block 2634A that hold the Parnassus Heights campus and the Mount Sutro "
                 "Open Space Reserve, against the approximately 107 acres the Regents and the CPHP EIR give for the site. "
                 "The official campus boundary (2014 LRDP Figure 6-11, as amended) couldn't be read, and campus blocks "
                 "north of Parnassus Avenue may be missing."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "tanforan": {
        "label": "San Mateo County parcels",
        "url": f"{SMC_PARCELS[0]}/resource/{SMC_PARCELS[1]}.json?"
               + urllib.parse.urlencode({"$where": f"apn in ({_sql_list(TANFORAN_APNS)})", "$limit": 5000}),
        "landing": f"{SMC_PARCELS[0]}/d/{SMC_PARCELS[1]}",
        "wkt": {"field": "shape", "crs": "EPSG:2227"},
        "layer": "County of San Mateo parcels, the six APNs in the Tanforan Redevelopment Project EIR",
        "accuracy": "official",
        "note": ("The six parcels the Draft EIR (p. 53) lists for the 44-acre project site: the Shops at Tanforan and the "
                 "vacant lot north of Sneath Lane, whose APN the Draft EIR gives as 014-316-060 and the NOP and the "
                 "County layer as 014-311-060."),
        "license": "Public Domain (County of San Mateo)",
    },
    "northgate-san-rafael": {
        "label": "Marin County parcels",
        **arcgis(MARIN_PARCELS, f"Prop_ID IN ({_sql_list(NORTHGATE_APNS)})"),
        "layer": "Marin County parcels (Marin GIS Basemap, layer 13), the six APNs in San Rafael Resolution 15360 and Ordinance 2043",
        "accuracy": "approximate",
        "note": ("The six Northgate Mall parcels the City's approvals name as the Project Site, against the approvals' "
                 "approximately 44.76 acres. Not yet checked against the Ordinance 2043 legal description (Exhibit D). "
                 "The County's parcel service states no license; its terms are an open item."),
        "license": "Marin County GIS (no license stated; terms to confirm)",
    },
    "ravenswood-business-district": {
        "label": "East Palo Alto’s specific plan boundary",
        **arcgis(EPA_SP_BOUNDARY, "1=1"),
        "minus": RAVENSWOOD_UV,
        "layer": ("City of East Palo Alto, 2025 EPA Zoning Map “Specific Plan Boundary”, less University Village "
                  "as drawn by the City's zoning parcels (Final_Zoning)"),
        "accuracy": "approximate",
        "note": ("The City's specific plan boundary layer is the plan's outer line (about 327 acres) and takes in "
                 "University Village, which the adopted plan leaves out (Figure 1-3). University Village is cut out "
                 "here as the City's zoning parcels zoned R-LD (its single-family lots) and PI (the school site) and "
                 "its two PR park parcels inside the line, closed over their own streets, against the plan's "
                 "approximately 207 acres. The narrow strip along the rail line north of Tulane Avenue, which the "
                 "plan includes, is too thin to keep."),
        "license": "City of East Palo Alto ArcGIS (no license stated; terms to confirm)",
    },
}


def fetch(name: str, spec: dict) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{name}.{'json' if 'wkt' in spec else 'geojson'}"
    if not cache.exists():
        req = urllib.request.Request(spec["url"], headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            cache.write_bytes(r.read())
    data = json.loads(cache.read_text())
    if "wkt" in spec:  # Socrata rows with the polygon as WKT text in a projected CRS
        field, crs = spec["wkt"]["field"], spec["wkt"]["crs"]
        rows = [r for r in data if r.get(field)]
        geoms = gpd.GeoSeries([shapely.force_2d(shapely.from_wkt(r[field])) for r in rows], crs=crs).to_crs(4326)
        data = {"type": "FeatureCollection",
                "features": [{"type": "Feature", "geometry": mapping(g), "properties": {}} for g in geoms]}
    if not data.get("features"):
        raise SystemExit(f"{name}: the query returned no features ({spec['url']})")
    return data


def _utm_shapes(fc: dict) -> gpd.GeoSeries:
    geoms = [shapely.make_valid(shape(f["geometry"])) for f in fc["features"] if f.get("geometry")]
    return gpd.GeoSeries(geoms, crs=4326).to_crs(UTM)


def build(project: str) -> None:
    spec = SPECS[project]
    utm = _utm_shapes(fetch(project, spec))
    geoms = list(utm)
    # Join neighbouring shapes; slivers between adjoining parcels close at 0.5 m.
    site = shapely.union_all(utm.buffer(0.5).to_numpy()).buffer(-0.5)
    if "minus" in spec:  # an area the layer takes in but the plan leaves out
        cut = spec["minus"]
        parts = _utm_shapes(fetch(f"{project}-minus", cut))
        parts = parts[parts.representative_point().within(site)]
        hole = shapely.union_all(parts.buffer(cut["close_m"]).to_numpy()).buffer(-cut["close_m"])
        site = site.difference(hole).buffer(-cut["open_m"]).buffer(cut["open_m"])
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
            **({"minusSource": spec["minus"]["label"], "minusSourceUrl": spec["minus"]["landing"],
                "minusQuery": spec["minus"]["url"]} if "minus" in spec else {}),
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
