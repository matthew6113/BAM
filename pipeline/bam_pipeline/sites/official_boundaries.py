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

# Oceanwide Center: the eight lots in Planning Motion 19635 and the CPE checklist (3708/003, 006, 007, 009,
# 010, 011, 012, 055), plus 176 and 177, the parts of Jessie Street and Elim Alley vacated to the project by
# Ordinance 137-16 (added to the parcel layer on July 26, 2016; together about the CPE's 4,859 sq ft).
OCEANWIDE_BLKLOTS = [
    "3708003", "3708006", "3708007", "3708009", "3708010", "3708011", "3708012", "3708055", "3708176", "3708177",
]

# 30 Van Ness: the single lot named in Ordinance 01-25 (Planning Code Section 249.99) and Motion 21700.
VAN_NESS_30_BLKLOTS = ["0835004"]

# West Midway and RESHAP (Alameda Point): the lots of Tract 8696 "West Midway Large Lot" (final map approved
# Apr 2025, Legistar matter 14761) inside the block bounded by Pan Am Way, West Midway Avenue, Main Street and
# West Tower Avenue, as the Alameda County Assessor numbers them after the map recorded (books 74-1385 to 74-1388).
WEST_MIDWAY_APNS = (
    [f"74-1385-{n}" for n in range(1, 12)] + ["74-1386-1", "74-1386-2"]
    + [f"74-1387-{n}" for n in range(1, 6)] + [f"74-1388-{n}" for n in range(1, 6)]
)

# Encinal Terminals: Ordinance 3312 (Feb 1, 2022) names APNs 072-0382-001, 072-0382-002, 072-0383-003 and
# 072-0382-009 (the City's 6.4-acre tidelands parcel). The Assessor now splits 072-0383-003 into 72-383-3-1, a
# strip under the Clement Avenue extension, so it's left out; the other three are the site.
ENCINAL_APNS = ["72-382-1", "72-382-2", "72-382-9"]

ALAMEDA_ZONING = ("https://services9.arcgis.com/ucDLsG1EwPnOGY4c/arcgis/rest/services/Zoning_v03/FeatureServer/0")

TANFORAN_APNS = [  # Draft EIR p. 53; the vacant lot is 014-311-060 in the NOP and the County layer (014-316-060 in the DEIR)
    "014316080", "014316300", "014316310", "014316360", "014316330", "014311060",
]

# Mission Bay Ferry Landing: the Port lots on the cover page of the Final MND (Case 2017-008824ENV, June 18, 2018).
MISSION_BAY_FERRY_BLKLOTS = ["9900064", "9900064H"]

# Port of Redwood City Ferry Terminal: the parcel in the Draft EIR's CEQAnet record (SCH 2024041306, Sept 24, 2026).
REDWOOD_CITY_FERRY_APNS = ["054300380"]

NORTHGATE_APNS = [  # San Rafael Resolution 15360 and Ordinance 2043 (Dec 2024)
    "175-060-12", "175-060-40", "175-060-59", "175-060-61", "175-060-66", "175-060-67",
]

# 530 Sansome Mixed-Use Tower and Fire Station 13: Block 0206, Lots 002 (447 Battery, the new fire station), 013,
# 014 and 017 (the tower), the four lots of the EIR (case 2024-007066ENV) and its Notice of Determination (Oct 2025).
SANSOME_530_BLKLOTS = ["0206002", "0206013", "0206014", "0206017"]

# Matson Block (77 Beale / 50 Main): the whole of Block 3711, Lots 005-014 and 019, as listed in the Notice of
# Preparation of an EIR of Dec 17, 2025 (case 2021-012562ENV, SCH 2025120794).
MATSON_BLOCK_BLKLOTS = [f"3711{n:03d}" for n in range(5, 15)] + ["3711019"]

# 536 Mission Street: Block 3708, Lot 098, the single lot of Planning record 2025-007507 (Planning Commission
# agenda of Sept 10, 2026).
MISSION_536_BLKLOTS = ["3708098"]

# 10 South Van Ness: "Lots 003A and 004 in Assessor's Block 3506", as the Planning Commission's minutes of June 11,
# 2020 (case 2015-004568) and its agenda of Nov 7, 2024 (case 2024-008986PPS) name the site.
SOUTH_VAN_NESS_10_BLKLOTS = ["3506003A", "3506004"]

# One Oak (1500-1540 Market Street): "Lots 001, 002, 003, 004, and 005 in Assessor's Block 0836", as the Planning
# Commission agenda of March 19, 2026 (case 2024-005509) and Motion 19943 (June 15, 2017) name the site.
ONE_OAK_BLKLOTS = ["0836001", "0836002", "0836003", "0836004", "0836005"]

# Mission Point (Santa Clara): the nine APNs in the City's notice of determination of Dec 3, 2024 (CEQAnet SCH
# 2018072068, document 7) and Draft EIR Table 2-1; the Democracy Way right-of-way between them is closed over.
MISSION_POINT_APNS = [
    "10404150", "10404142", "10404143", "10404151", "10404112", "10404113", "10404065", "10404111", "10404064",
]

# Seely Avenue Mixed-Use (San José): the approval (NOD of Aug 13, 2024, SCH 2022020565) names APNs 097-15-033,
# 097-15-034 and part of 097-66-004, which the County has since retired. Their successors are the project's own
# lots, matching Draft EIR Table 2-1: 097-15-042 (Building A), -045 (B), -046 (affordable), -047 (well), -048
# (park), -049 (C), the 26 townhome lots 097-23-141 to -166, and the unnumbered private-street and common lots.
SEELY_AVENUE_APNS = (
    ["09715042", "09715045", "09715046", "09715047", "09715048", "09715049"]
    + [f"09723{n}" for n in range(141, 167)]
)
SEELY_AVENUE_COMMON_BOX = "37.4012, -121.9195, 37.3955, -121.9145"  # unnumbered lots inside the subdivision

# Freedom Circle (Santa Clara): 104-40-019, 2518 Mission College Blvd (Irvine Company; NODs of Mar 25 and May 14,
# 2025, SCH 2020060425) and the Greystar site, 104-40-021 and 104-40-036 (NOD of June 7, 2022; Draft EIR).
FREEDOM_CIRCLE_APNS = ["10440019", "10440021", "10440036"]

# Pleasant Hills Golf Course redevelopment (San José): the two APNs of the project site in the NOP of Oct 14, 2025
# (SCH 2025100897). The 0.6-acre parcel at 2079 Flint Avenue is annexed but "not part of the project".
PLEASANT_HILLS_APNS = ["64923001", "64924013"]

# Freedom West 2.0: Block 0783, Lots 023, 024 and 025, and Block 0770, Lot 027, the four lots named in the Notice of
# Preparation (Apr 30, 2025) and Draft EIR (Jan 13, 2026) for case 2020-006887ENV (SCH 2025050078). Lot 0770/027 also
# holds the separate 870-880 McAllister senior housing site (case 2024-003742PRJ), which the project leaves out.
FREEDOM_WEST_BLKLOTS = ["0783023", "0783024", "0783025", "0770027"]


# Transbay Parcel F (542-550 Howard Street): Assessor's Block 3721, Lots 016, 135, 136 and 138, as listed in the
# Planning Commission's approvals of Jan 9, 2020 (Motions 20615-20618, case 2016-013312) and their Jan 28, 2021
# amendments (Motions 20843-20845).
TRANSBAY_PARCEL_F_BLKLOTS = ["3721016", "3721135", "3721136", "3721138"]

# 524 and 530 Howard Street: Block 3721, Lots 013 (524 Howard, parking lot) and 014 (530 Howard, office building),
# the two lots of DBI site permit application 202311170986 and Planning record 2023-010883PRJ.
HOWARD_524_BLKLOTS = ["3721013", "3721014"]

# Flower Mart (610-698 Brannan Street): Block 3778, Lots 001B, 002B, 004, 005, 047 and 048, the six lots of the
# Planning Commission's July 18, 2019 approvals (Motion 20484, case 2017-000663) and of the 2026 Development Agreement
# amendment (Planning Commission agenda of Oct 1, 2026, record 2025-008569PRJ).
FLOWER_MART_BLKLOTS = ["3778001B", "3778002B", "3778004", "3778005", "3778047", "3778048"]

# 88 Bluxome Street: Block 3786, Lot 037, the single lot of Motion 20493 (July 25, 2019) and of Planning record
# 2025-004642PRJ (approved Dec 12, 2025).
BLUXOME_88_BLKLOTS = ["3786037"]

# 655 4th Street: Block 3787, Lots 026, 028, 050 and 161-164, the seven lots of Motions 20470 and 20471 (June 20,
# 2019) and of the Dec 14, 2023 Planning Commission agenda (record 2022-011490).
FOURTH_655_BLKLOTS = ["3787026", "3787028", "3787050", "3787161", "3787162", "3787163", "3787164"]

# One Vassar (400 2nd, 645 and 657 Harrison Streets): Block 3763, Lots 001, 078, 079, 080, 080A, 081, 099, 100, 101,
# 105, 112 and 113 in Motions 20665-20667 (Feb 20, 2020, case 2012.1384). Lot 112 was retired in 2019; its piece at
# 416 2nd Street, between lot 113 and the AC Transit yard (lot 126), is now lot 125, which is drawn in its place.
ONE_VASSAR_BLKLOTS = [
    "3763001", "3763078", "3763079", "3763080", "3763080A", "3763081", "3763099", "3763100", "3763101", "3763105",
    "3763113", "3763125",
]

# Gateway Crossings (1205 Coleman Avenue, Santa Clara): the approval (NOD of July 9, 2019, SCH 2017022066) covers about
# 21.4 acres; CEQAnet's records of the 2017 NOP and 2018 Draft EIR give APNs 230-46-069 and -070, which the County has
# since retired. Their successors are the lots on assessor's page 230-60 (230-60-001 to -008, and -010, re-mapped from
# the -009 that the City's 2026 station-area plan record still lists) and the unnumbered street lots inside
# GATEWAY_CROSSINGS_COMMON_BOX: about 21.35 acres together.
GATEWAY_CROSSINGS_APNS = [f"23060{n:03d}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 10)]
GATEWAY_CROSSINGS_COMMON_BOX = "37.3568, -121.9367, 37.3535, -121.9318"  # unnumbered street lots inside the subdivision

# 98 Franklin Street: "Lots 008, 009, & 013 in Assessor's Block 0836", as the Planning Commission's minutes of May 28,
# 2020 (Motions 20726-20728, case 2016-014802) and its agenda of March 30, 2023 name the site.
FRANKLIN_98_BLKLOTS = ["0836008", "0836009", "0836013"]


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
    "west-midway-reshap": {
        "label": "Alameda County parcels",
        **arcgis(ALCO_PARCELS, f"APN in ({_sql_list(WEST_MIDWAY_APNS)})"),
        "layer": ("Alameda County Assessor parcels: the 23 lots of Tract 8696 (West Midway Large Lot) between "
                  "Pan Am Way, West Midway Avenue, Main Street and West Tower Avenue"),
        "accuracy": "official",
        "close_m": 30,  # takes in the new internal streets between the lots (Waves and Valor avenues, Orion Street)
        "note": ("The 26-acre West Midway site and the 8.5-acre RESHAP campus beside it, as the County's parcels of "
                 "the 2025 final map draw them, closed over the new streets between the lots. The lots alone are "
                 "about 29.4 acres."),
        "license": "Alameda County open data (county disclaimer)",
    },
    "encinal-terminals": {
        "label": "Alameda County parcels",
        **arcgis(ALCO_PARCELS, f"APN in ({_sql_list(ENCINAL_APNS)})"),
        "layer": "Alameda County Assessor parcels 72-382-1, 72-382-2 and 72-382-9 (1521 and 1527 Buena Vista Avenue)",
        "accuracy": "approximate",
        "note": ("The three parcels Ordinance 3312 (2022) names for the Encinal Terminals Master Plan, including the "
                 "City's 6.4-acre tidelands parcel (72-382-9). They reach out over the wharf and the water's edge, so "
                 "they cover more than the master plan's 23-acre site; the fourth APN in the ordinance is now a "
                 "strip under the Clement Avenue extension and is left out."),
        "license": "Alameda County open data (county disclaimer)",
    },
    "alameda-marina": {
        "label": "City of Alameda zoning",
        **arcgis(ALAMEDA_ZONING, "zone = 'M-X'"),
        "url": arcgis(ALAMEDA_ZONING, "zone = 'M-X'")["url"] + "&" + urllib.parse.urlencode(
            {"geometry": "-122.2471,37.7753", "geometryType": "esriGeometryPoint", "inSR": 4326,
             "spatialRel": "esriSpatialRelIntersects"}),
        "layer": ("City of Alameda zoning (Zoning v03), the M-X Mixed Use Planned Development District polygon "
                  "between Grand Street and Willow Street north of Clement Avenue"),
        "accuracy": "approximate",
        "note": ("The Alameda Marina Master Plan's uplands as the City's zoning map draws them (the master plan's "
                 "27 acres of private uplands and submerged land). The 17 acres of City tidelands in the plan, "
                 "mostly the 530-slip marina, aren't zoned M-X and aren't drawn."),
        "license": "City of Alameda ArcGIS Online (no license stated)",
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
        "license": "City of Santa Clara Open Data Portal terms of use (2018): ODC PDDL 1.0, credit City of Santa Clara",
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
                 "in the 2005 EIR. The City's April 27, 2026 report says the draft new plan keeps the same overall "
                 "boundary (about 3,131 acres); no map of it is published as GIS."),
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
        "license": "CC BY-SA 3.0 US, County of Sonoma",
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
    "oceanwide-center": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(OCEANWIDE_BLKLOTS)})"),
        "layer": ("DataSF Parcels – Active and Retired, block 3708 lots 003, 006, 007, 009, 010, 011, 012 and 055 "
                  "and the vacated street lots 176 and 177"),
        "accuracy": "official",
        "note": ("The eight lots Planning Motion 19635 (May 5, 2016) approves, with the portions of Jessie Street and "
                 "Elim Alley vacated to the project by Ordinance 137-16, against the CPE checklist's 59,445 sq ft "
                 "(1.36 acres). The corner building at 82–84 First Street and 510 Mission Street (lot 008) isn't part "
                 "of the project, so 88 First Street (lot 009) is drawn as a separate piece."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "30-van-ness": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(VAN_NESS_30_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 0835 lot 004",
        "accuracy": "official",
        "note": ("Assessor's Block 0835, Lot 004, the whole of the 30 Van Ness Avenue Special Use District "
                 "(Ordinance 01-25); Motion 21700 gives the lot as 38,123 sq ft."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "mission-bay-ferry-landing": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(MISSION_BAY_FERRY_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 9900 lots 064 and 064H",
        "accuracy": "approximate",
        "note": ("The two Port of San Francisco lots the Final Mitigated Negative Declaration names for the Mission Bay "
                 "Ferry Landing and Water Taxi Landing (Case 2017-008824ENV, cover page: Block/Lot 9900/064 and 9900/064H, "
                 "153,257 sq ft): the shoreline strip along Terry A. Francois Boulevard from 16th Street south past Agua "
                 "Vista Park. In the City's parcel map lot 064 also takes in the water around the old Pier 64 north of "
                 "the landing, where the Port's Phase 2a contract removes marine debris, so the lots drawn are about "
                 "twice the MND's lot size. The pier, gangway and float stand in the Bay and aren't drawn separately; "
                 "the lots also take in the 2018 water taxi landing site, which the 2026 construction contract doesn't "
                 "mention."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "redwood-city-ferry-terminal": {
        "label": "San Mateo County parcels",
        "url": f"{SMC_PARCELS[0]}/resource/{SMC_PARCELS[1]}.json?"
               + urllib.parse.urlencode({"$where": f"apn in ({_sql_list(REDWOOD_CITY_FERRY_APNS)})", "$limit": 5000}),
        "landing": f"{SMC_PARCELS[0]}/d/{SMC_PARCELS[1]}",
        "wkt": {"field": "shape", "crs": "EPSG:2227"},
        "layer": "County of San Mateo parcels, APN 054-300-380, the parcel named in the Port of Redwood City's Draft EIR",
        "accuracy": "official",
        "note": ("The 9.2-acre parcel the Draft EIR's notice of completion lists for the Port of Redwood City Ferry Terminal "
                 "Project (CEQAnet SCH 2024041306, Sept 2026): the ferry terminal, parking lot and the area rezoned for "
                 "future visitor-serving uses. The float and access pier extend into Redwood Creek off the parcel, and the "
                 "Seaport Boulevard, railroad and Bay Trail work in the wider project area isn't drawn."),
        "license": "Public Domain (County of San Mateo)",
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
    "530-sansome": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(SANSOME_530_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 0206 lots 002, 013, 014 and 017",
        "accuracy": "official",
        "note": ("The four lots the EIR and its Notice of Determination name (24,830 sq ft): Fire Station 13 at 530 "
                 "Sansome Street and 425 and 439-445 Washington Street (lots 017, 014 and 013) for the tower, and 447 "
                 "Battery Street (lot 002) for the new fire station. The office condominiums at 423 Washington Street, "
                 "on the corner of Washington and Battery, aren't part of the site. The 530 Sansome special use "
                 "district polygon in DataSF's zoning layer doesn't match these lots, so the parcels are used."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "77-beale": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(MATSON_BLOCK_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3711 lots 005 to 014 and 019",
        "accuracy": "official",
        "note": ("The whole block bounded by Market, Main, Mission and Beale streets, the eleven lots the Notice of "
                 "Preparation names, against its 151,390 sq ft (3.47 acres)."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "536-mission": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(MISSION_536_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3708 lot 098",
        "accuracy": "official",
        "note": ("The Golden Gate University lot between Mission and Jessie streets at Ecker Place, the single lot "
                 "of the Planning Commission's Sept 10, 2026 approvals. Oceanwide Center's site is across Ecker "
                 "Place, about 25 ft away; the two don't touch."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "10-south-van-ness": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(SOUTH_VAN_NESS_10_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3506 lots 003A and 004",
        "accuracy": "official",
        "note": ("Lots 003A and 004 in Assessor's Block 3506, the triangular site at Market Street, South Van Ness "
                 "Avenue and 12th Street that the Planning Commission's 2020 minutes and 2024 agenda name, against the "
                 "1.17 acres in the project's CEQA filings. The project would merge the two lots."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "one-oak": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(ONE_OAK_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 0836 lots 001 to 005",
        "accuracy": "official",
        "note": ("Lots 001 to 005 in Assessor's Block 0836, on Market Street between Van Ness Avenue and Oak Street, "
                 "as the Planning Commission's 2017 approval and March 19, 2026 agenda name them, against the 18,219 sq "
                 "ft lot area in Motion 19943. The public plaza the project would build in the Oak Street roadway (Oak "
                 "Plaza) is off the lots and isn't drawn."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "mission-point": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, f"apn in ({_sql_list(MISSION_POINT_APNS)})"),
        "layer": "Santa Clara County parcels, the nine APNs in Santa Clara's notice of determination for Mission Point (Dec 3, 2024)",
        "accuracy": "official",
        "close_m": 20,  # takes in the Democracy Way right-of-way between the parcels
        "note": ("The nine parcels the City's approval names for the Mission Point Project, joined over the Democracy Way "
                 "right-of-way that the project takes in, against the approval's approximately 48.6 acres (Draft EIR "
                 "Table 2-1: 46.0 acres of parcels plus 2.6 acres of right-of-way)."),
        "license": "Santa Clara County open data (terms of use)",
    },
    "seely-avenue": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, f"apn in ({_sql_list(SEELY_AVENUE_APNS)}) or "
                                f"(apn is null and within_box(the_geom, {SEELY_AVENUE_COMMON_BOX}))"),
        "layer": ("Santa Clara County parcels: the Seely Avenue project's lots (097-15-042 to -049, 097-23-141 to -166) "
                  "and the unnumbered street and common lots between them"),
        "accuracy": "approximate",
        "note": ("The approval names APNs 097-15-033, 097-15-034 and part of 097-66-004, which are no longer in the "
                 "County's layer. Drawn instead from the parcels that replaced them, which are the project's own lots: "
                 "Buildings A, B and C, the affordable building, the park and the well site match the Draft EIR's lot "
                 "areas (Table 2-1) within 2%, against the approval's approximately 22 acres. The Seely Avenue frontage "
                 "dedication isn't a parcel and isn't drawn."),
        "license": "Santa Clara County open data (terms of use)",
    },
    "freedom-circle": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, f"apn in ({_sql_list(FREEDOM_CIRCLE_APNS)})"),
        "layer": ("Santa Clara County parcels 104-40-019 (2518 Mission College Boulevard) and 104-40-021 and 104-40-036 "
                  "(the Greystar site), named in Santa Clara's approvals"),
        "accuracy": "official",
        "note": ("The two sites with approvals in the Freedom Circle Focus Area: the Irvine Company's 25.7-acre site at "
                 "2518 Mission College Boulevard and Greystar's 13.3-acre site on Freedom Circle, separated by Freedom "
                 "Circle itself. The rest of the 108-acre focus area, which awaits a future planning study, isn't drawn."),
        "license": "Santa Clara County open data (terms of use)",
    },
    "pleasant-hills": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, f"apn in ({_sql_list(PLEASANT_HILLS_APNS)})"),
        "layer": "Santa Clara County parcels 649-23-001 and 649-24-013, the project site in San José's notice of preparation (Oct 2025)",
        "accuracy": "official",
        "note": ("The former Pleasant Hills and Cypress Greens golf courses, the two parcels the notice of preparation "
                 "names, against its approximately 113.5 gross acres. The 0.6-acre house lot at 2079 Flint Avenue, which "
                 "would be annexed with them but isn't part of the project, isn't drawn."),
        "license": "Santa Clara County open data (terms of use)",
    },
    "freedom-west": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(FREEDOM_WEST_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 0783 lots 023, 024 and 025 and block 0770 lot 027",
        "accuracy": "approximate",
        "note": ("The four lots the Notice of Preparation and Draft EIR name for Freedom West 2.0 (case 2020-006887ENV), "
                 "against the Draft EIR's 451,500 sq ft (10.37 acres): the whole block between McAllister and Fulton "
                 "streets and most of the block to the north. Lot 0770/027 also takes in the corner of McAllister and "
                 "Laguna streets at 870-880 McAllister Street, a separate 115-home senior housing project (case "
                 "2024-003742PRJ) that the Draft EIR leaves out of the site; the lot split approved in 2024 (case "
                 "2024-008030SUB) isn't in the parcel layer yet, so that corner, about 0.4 acres, is drawn as part of "
                 "the site. Bethel A.M.E. Church and 967-973 Golden Gate Avenue are on their own lots and aren't drawn."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "sf-gateway": {
        "label": "DataSF special use districts",
        **socrata(DATASF, SF_SUD, "name = 'San Francisco Gateway SUD'"),
        "layer": "DataSF Zoning Map – Special Use Districts, “San Francisco Gateway SUD”",
        "accuracy": "official",
        "note": ("The San Francisco Gateway Special Use District (Board File 250426, in effect Dec 12, 2025): Lot 008 in "
                 "Block 5284A and Lot 002 in Block 5287 with the portions of the surrounding streets and Selby Street "
                 "in the project, against the approvals' 743,800 sq ft (about 17.1 acres). Interstate 280 crosses the "
                 "site overhead between the two buildings."),
        "license": "Public Domain U.S. Government (DataSF)",
    },
    "transbay-parcel-f": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(TRANSBAY_PARCEL_F_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3721 lots 016, 135, 136 and 138",
        "accuracy": "official",
        "note": ("The four lots of Transbay Parcel F named in the Planning Commission's approvals (Jan 9, 2020), "
                 "against the 32,229 sq ft (0.74 acres) in Motion 20616. The west edge follows the curved line of "
                 "the Transit Center's bus ramp property (lots 134 and 137), which isn't part of the site; the strip "
                 "of lot 136 along Natoma Street reaches east behind 540 Howard Street (lot 015) to 530 Howard Street."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "524-howard": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(HOWARD_524_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3721 lots 013 and 014",
        "accuracy": "official",
        "note": ("The parking lot at 524 Howard Street (lot 013) and the office building at 530 Howard Street (lot "
                 "014), the two lots of DBI site permit application 202311170986, running through from Howard Street "
                 "to Natoma Street. Transbay Parcel F's strip along Natoma Street adjoins lot 014 on the west; the "
                 "two sites share that line and don't overlap."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "flower-mart": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(FLOWER_MART_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3778 lots 001B, 002B, 004, 005, 047 and 048",
        "accuracy": "official",
        "note": ("The six lots of the Flower Mart site on the north side of Brannan Street between 5th and 6th streets, "
                 "as the 2019 approvals and the Oct 1, 2026 Planning Commission agenda name them, against the "
                 "approximately 6.5 acres in the Development Agreement. The rest of the block, north of the site's "
                 "service drive, isn't part of it."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "88-bluxome": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(BLUXOME_88_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3786 lot 037",
        "accuracy": "official",
        "note": ("Lot 037 in Assessor's Block 3786, the former San Francisco Tennis Club site on Brannan, 5th and "
                 "Bluxome streets, against the 114,048 sq ft (2.61 acres) in Motion 20493. The 2025 project would "
                 "split it into three parcels (43,670, 47,580 and 22,690 sq ft, west to east), the eastern one for "
                 "City affordable housing; that split isn't in the parcel layer, so the whole lot is drawn."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "655-fourth-street": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(FOURTH_655_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 3787 lots 026, 028, 050 and 161 to 164",
        "accuracy": "official",
        "note": ("The seven lots at the northeast corner of 4th and Townsend streets that the 2019 approvals and the "
                 "Dec 14, 2023 Planning Commission agenda name, against the 71,290 sq ft development lot in the "
                 "Planning Department's record of the modified project."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "one-vassar": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(ONE_VASSAR_BLKLOTS)})"),
        "layer": ("DataSF Parcels – Active and Retired, block 3763 lots 001, 078, 079, 080, 080A, 081, 099, 100, 101, "
                  "105, 113 and 125"),
        "accuracy": "approximate",
        "note": ("The lots on Harrison Street between 2nd Street and the AC Transit yard that the Planning Commission's "
                 "Feb 20, 2020 approvals name, against their 102,694 sq ft (2.36 acres). One of the approval's twelve "
                 "lots, 112, has since been retired; its piece at 416 2nd Street, now lot 125, is drawn in its place, "
                 "and the rest of it, the AC Transit bus yard (lot 126), isn't. Vassar Place, a public street, "
                 "separates 400 2nd Street from the rest of the site."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
    },
    "gateway-crossings": {
        "label": "Santa Clara County parcels",
        **socrata(*SCC_PARCELS, f"apn in ({_sql_list(GATEWAY_CROSSINGS_APNS)}) or "
                                f"(apn is null and within_box(the_geom, {GATEWAY_CROSSINGS_COMMON_BOX}))"),
        "layer": ("Santa Clara County parcels: the lots that replaced the Gateway Crossings site (230-60-001 to -008 and "
                  "-010) and the unnumbered street lots between them"),
        "accuracy": "approximate",
        "note": ("The approval's site at 1205 Coleman Avenue, which CEQAnet records as APNs 230-46-069 and -070. The "
                 "County has since retired those two parcels and mapped the site as new lots on assessor's page 230-60 "
                 "(addressed on Rickabaugh Way, Chastain Place and Brokaw Road) with unnumbered street lots between "
                 "them; those lots and streets are drawn, and together they match the approval's approximately 21.4 "
                 "acres. The site lies inside the Santa Clara Station Area Specific Plan area."),
        "license": "Santa Clara County open data (terms of use)",
    },
    "98-franklin": {
        "label": "DataSF parcels",
        **socrata(DATASF, SF_PARCELS, f"blklot in ({_sql_list(FRANKLIN_98_BLKLOTS)})"),
        "layer": "DataSF Parcels – Active and Retired, block 0836 lots 008, 009 and 013",
        "accuracy": "official",
        "note": ("Lots 008, 009 and 013 in Assessor's Block 0836, the L-shaped parking lot at Franklin and Oak streets "
                 "with a strip through to Market Street that the Planning Commission's May 28, 2020 approvals name, "
                 "against the approximately 23,750 sq ft in the approval and the Hub Plan EIR. One Oak's site (lots "
                 "001 to 005) is to the east, beyond 1546-1564 Market Street (lot 007); the two don't touch."),
        "license": "ODC Public Domain Dedication and License (DataSF)",
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
    if "close_m" in spec:  # lots of one subdivision, joined over the streets between them
        site = site.buffer(spec["close_m"], join_style="mitre").buffer(-spec["close_m"], join_style="mitre")
    if "minus" in spec:  # an area the layer takes in but the plan leaves out
        cut = spec["minus"]
        parts = _utm_shapes(fetch(f"{project}-minus", cut))
        parts = parts[parts.representative_point().within(site)]
        hole = shapely.union_all(parts.buffer(cut["close_m"]).to_numpy()).buffer(-cut["close_m"])
        site = site.difference(hole).buffer(-cut["open_m"]).buffer(cut["open_m"])
    # 1 m is well inside map precision and keeps the bundled files small.
    site = site.simplify(1.0, preserve_topology=True)
    if site.geom_type == "MultiPolygon":  # drop slivers between parcels, which round away to degenerate rings
        parts = [p for p in site.geoms if p.area > 1.0]
        site = parts[0] if len(parts) == 1 else shapely.MultiPolygon(parts)
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
