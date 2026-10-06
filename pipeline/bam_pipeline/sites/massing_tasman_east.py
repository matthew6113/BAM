"""Tasman East: built buildings from OpenStreetMap footprints, the rest to the plan's height limits.

What is drawn:
1. Buildings with occupancy or reported complete (stage "complete"), on real footprints from
   OpenStreetMap via Overture (buildings and building parts), matched to their projects by the
   City of Santa Clara's land parcels (APNs in the state housing reports). Heights:
   - Related, 2300 Calle de Luna (2350 Calle de Luna and 5150 Calle del Sol): the CEQA addendum
     for the project (January 2021, PDF p. 3) gives 20 stories "approximately 214 feet" (home for
     the ambulatory aged), 22 stories "approximately 217 feet" and 8 stories "approximately 70
     feet" (apartments), plus a seven-story garage with amenity space on its eighth level.
   - Greystar, 2223 Calle de Luna and 2230 Calle del Mundo: "Approximately 85'" (about 90 ft to
     the parapet), project data table for the 2023 extension of the approval.
   - Stories only (height estimated at the plan area's own average, illustrative): St. Anton,
     2231 Calle del Mundo, six stories (Notice of Exemption, CEQAnet 2020030015/2); 2302/2310
     Calle del Mundo, an eight-story building (Draft SEIR, Aug 2026, Table 2.2-1); 5123 Calle
     del Sol Parcel 19 (address 2240 Calle de Luna), an eight-story mid-rise (Notice of
     Determination, July 2019, CEQAnet 2016122027/5).
   - SummerHill, 2333 Calle del Mundo: no official height or story count was found, so the
     footprint has no height (the base map still draws it).
   The average story height: the four buildings above with both stories and feet
   (214/20, 217/22, 70/8, 85/8 twice) give 671 ft over 66 stories, 10.2 ft a story.
2. Every other parcel in the plan (City of Santa Clara land parcels tagged with the plan), drawn
   to the plan's height limits: towers up to 220 ft "or the FAA Part 77 height limit, whichever is
   lower" (Final EIR text revisions, PDF p. 61), over podiums of up to 85 ft (Draft EIR section
   2.3.4, PDF p. 61: podium-style buildings "shall not exceed 85 feet above existing grade"). The
   Draft SEIR for the +1,500-unit amendment (Aug 2026) keeps "a maximum of 220 feet". These are
   height envelopes, not designs, so they are illustrative. Streets are outside the parcels.
   Parks already dedicated sit on the built projects' parcels, which carry only their buildings.
   The plan's other parks (2.5 acres in the River District, at least 1 acre in the Center
   District) have no fixed location in any official document (the Open Space Framework calls
   them conceptual), so they are not cut out.

Newer documents win (rule of 2026-10-05): 5123 Calle del Sol Parcel 19 is "Constructed" in the
Draft SEIR (Aug 2026) although the state housing reports list no certificate of occupancy through
2025; the Holland (2200 Calle de Luna) and Related (2101 Tasman Drive) approvals of 2023 are
"abandoned" per the Draft SEIR; 5185 Lafayette Street was approved at 21 stories (2023) and is
described at 18 stories in the Draft SEIR. Each is noted on its feature.

No figure is traced, so there is no georeference fit: parcels are the City's GIS and
footprints are OpenStreetMap.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_tasman_east
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "tasman-east"
UTM = tb.UTM
RAW = config.ROOT / "data" / "raw" / "official" / "tasman-east"
BBOX = (-121.9700, 37.4060, -121.9600, 37.4120)

SC_BASE = "https://map.santaclaraca.gov/maps/rest/services/OPENDATA/RegionalBaseOpenData/MapServer"
SC_PARCELS = f"{SC_BASE}/7"  # Land Parcels: APN, status (A active, R retired), specific plan tag
SC_ADDRESSES = f"{SC_BASE}/2"  # Site Addresses
APR_SQL = (
    'SELECT "YEAR","APN","STREET_ADDRESS","ENT_APPROVE_DT1","NO_ENTITLEMENTS","BP_ISSUE_DT1",'
    '"NO_BUILDING_PERMITS","CO_ISSUE_DT1","NO_OTHER_FORMS_OF_READINESS" '
    'FROM "fe505d9b-8c36-42ba-ba30-08bc4f34e022" WHERE "JURIS_NAME" ILIKE \'SANTA CLARA\' '
    'AND "APN" LIKE \'097-%\' AND ("STREET_ADDRESS" ILIKE \'%CALLE D%\' OR "STREET_ADDRESS" ILIKE \'%TASMAN%\' '
    'OR "STREET_ADDRESS" ILIKE \'%LAFAYETTE%\') ORDER BY "APN","YEAR"'
)
APR_URL = "https://data.ca.gov/api/3/action/datastore_search_sql?" + urllib.parse.urlencode({"sql": APR_SQL})
APR_LANDING = "https://data.ca.gov/dataset/housing-element-annual-progress-report-apr-data-by-jurisdiction-and-year"

SCA = "https://santaclara.legistar1.com/santaclara/attachments/"
DOCS = {
    "feir": {"url": SCA + "f322e818-7feb-4e99-b91d-3ae13089ec4e.pdf",
             "sha256": "ac0d3b92a343bdc5380d214b56d5a667eb354beaf6c116cd019bb5a34aebc5c2",
             "file": "te-tesp-feir-2018.pdf",
             "check": {60: ["would not exceed 220 feet or the FAA Part 77 height limit, whichever is lower"]}},
    "deir": {"url": SCA + "620caa40-c419-4890-8f31-52e5126c0526.pdf",
             "sha256": "76854d2ae35b6bf727f638b824d74fcb1a11d3d55534829c609cfa921890e198",
             "file": "te-tesp-deir-2018.pdf",
             "check": {60: ["Podium-style buildings shall not exceed 85 feet above existing grade"],
                       176: ["exceeding approximately 175 feet in height above ground would require submittal"]}},
    "dseir": {"url": "https://ceqanet.lci.ca.gov/2016122027/7/Attachment/wRdzt5",
              "sha256": "f6298cb9c26b2a910ad9553f66636c9edcea8e4a6543c1c9a01a83f98cd8443f",
              "file": "te-tesp-amendment-dseir-2026.pdf",
              "check": {34: ["have been abandoned"],
                        35: ["5,000 square feet of retail space in an eight-story building", "Constructed",
                             "within an 18-story building"],
                        38: ["at maximum, 220 feet"]}},
    "related": {"url": SCA + "e6c34bac-7ee7-4ada-a313-704e06eb3ee0.pdf",
                "sha256": "7dc5bb19b2d43d04ae9467500d4e71cb289ffc90e44b49f6007b70c3b7a406a7",
                "file": "te-related-addendum-2021.pdf",
                "check": {2: ["20 stories tall (approximately 214 feet to roof line)",
                              "22 stories tall (approximately 217 feet to the roof line)",
                              "eight stories tall (approximately 70 feet to the roof line)",
                              "seven-story, above-grade parking garage"]}},
    "greystar": {"url": SCA + "6329e9a6-e29a-4f31-a2cf-ab8a09b2f902.pdf",
                 "sha256": "79d28291b5d829db92b15ed5dca40704e0b21e0cd75c93e6971fa79adc140398",
                 "file": "te-greystar-project-data-2023.pdf",
                 "check": {0: ["Approximately 85’", "Approximately 90’ to parapet"]}},
    "nod2019": {"url": "https://files.ceqanet.lci.ca.gov/233986-5/attachment/"
                       "H3Y3BKuZJbQSm4f_X5AwnWav9Z7CM0c0Tq-R3fYMFM29kY1nrKQACj6kRtUox8JBpVpwlv5LgusuArb70",
                "sha256": "3ddc3f9a58b7f70a1e37c342803446960f92370dde2e570f7f37dc38a3ee1aad",
                "file": "te-nod-5123-calle-del-sol-2019.pdf",
                "check": {1: ["Parcel 19 is proposed to be eight-story, mid-rise building with 311",
                              "Parcel 29 is proposed to be a 20-story building with 192"]}},
}
# Pages without a PDF to pin: checked for their phrase on each run.
PAGES = {
    "st_anton_noe": {"url": "https://ceqanet.lci.ca.gov/2020030015/2",
                     "file": "te-ceqanet-2020030015-2.html", "check": ["196-unit, six-story"]},
}
LEGISTAR = {  # matter id -> (file number, phrase checked in the report text)
    16988: ("20-1095", "construct an eight story mid-rise building, comprised of 299 dwelling units"),
    22462: ("23-842", "21-story, 198-unit multifamily residential development"),
    22437: ("23-817", "Mid-Rise Scheme including two eight-story residential buildings"),
    22948: ("23-1329", "two, 12-story buildings and one 11-story building"),
}

TOWER_FT, PODIUM_FT = 220, 85
FT_PER_STORY = round((214 + 217 + 70 + 85 + 85) / (20 + 22 + 8 + 8 + 8), 1)  # 10.2

FEIR_REF = "Tasman East Specific Plan Final EIR (Oct 2018), text revisions to section 2.3.4.1, PDF p. 61"
DEIR_REF = "Draft EIR (July 2018), section 2.3.4, PDF p. 61"
DSEIR_REF = "Tasman East Specific Plan Amendment +1,500 units, Draft SEIR (Aug 2026, CEQAnet 2016122027/7)"
RELATED_REF = "Related Tasman East addendum to the Final EIR (Jan 2021), PDF p. 3 (" + DOCS["related"]["url"] + ")"
GREYSTAR_REF = ("project data table, PLN22-00634 extension of PLN2020-14513, Development Review Hearing "
                "Jan 11, 2023 (" + DOCS["greystar"]["url"] + ")")
NOD_REF = "Notice of Determination for 5123 Calle del Sol, July 2019 (CEQAnet 2016122027/5), PDF p. 2"
EST = (f"height estimated at {FT_PER_STORY} ft a story, the average of the plan area's buildings with both "
       f"stories and feet in official records (Related addendum, Jan 2021; Greystar data table, 2023)")

# Built projects: their APNs in the state housing reports (APR Table A2) or approvals. Parcels
# since re-mapped are found through the retired APNs they replaced.
BUILT = {
    "st-anton": {"apns": ["097-05-059"], "apr": ["2231 CALLE DEL MUNDO"]},
    "summerhill": {"apns": ["097-05-062", "097-05-063", "097-05-064"], "apr": ["2333 CALLE DEL MUNDO"]},
    "related": {"apns": ["097-46-016", "097-46-017", "097-46-018", "097-46-028"],
                "apr": ["2350 CALLE DE LUNA", "5150 CALLE DEL SOL"]},
    "greystar": {"apns": ["097-46-020", "097-46-027"], "apr": ["2223 CALLE DE LUNA", "2230 CALLE DEL MUNDO"]},
    "ensemble-2302": {"apns": ["097-46-024"], "apr": ["2310 CALLE DEL MUNDO"]},
    "ensemble-p19": {"apns": ["097-46-019"], "apr": []},  # building permit 2022 (2240 Calle de Luna), no CO
}

# Footprints (OpenStreetMap way ids, read through Overture).
FOOTPRINTS = [
    {"project": "st-anton", "osm": ["w1313997468"], "label": "St. Anton, 2231 Calle del Mundo",
     "stories": 6, "stories_src": "196-unit, six-story affordable project (City of Santa Clara Notice of Exemption, "
     "CEQAnet 2020030015/2)", "use": "Residential (196 affordable homes)",
     "note": "196 affordable homes. Certificate of occupancy Dec 21, 2022 (state housing report)."},
    {"project": "summerhill", "osm": ["w1351049824"], "label": "2333 Calle del Mundo",
     "height_ft": None, "use": "Residential (347 homes)",
     "source_height": "no official height or story count found; outline only",
     "note": "347 homes (SummerHill). Certificate of occupancy Jan 16, 2025 (state housing report). "
             "Height needs verification."},
    {"project": "related", "osm": ["w1351049825", "w1351049827"], "label": "2350 Calle de Luna",
     "height_ft": 214, "use": "Home for the ambulatory aged",
     "source_height": "20 stories, approximately 214 ft to the roof line (" + RELATED_REF + ")",
     "note": ("Related's home for the ambulatory aged: 176 homes with occupancy Mar 10, 2025 (state housing report). "
              "OpenStreetMap doesn't separate the four-story base from the 16-story tower above it, so the whole "
              "footprint is drawn to 214 ft.")},
    {"project": "related", "part": "w1523954747", "label": "5150 Calle del Sol, tower", "height_ft": 217,
     "use": "Residential",
     "source_height": "22 stories, approximately 217 ft to the roof line (" + RELATED_REF + ")",
     "note": "Related's 22-story apartment tower (OpenStreetMap maps 21 levels). 5150 Calle del Sol has 508 homes "
             "with occupancy Apr 7, 2025 (state housing report)."},
    {"project": "related", "part": "w1523954744", "label": "5150 Calle del Sol, mid-rise", "height_ft": 70,
     "use": "Residential",
     "source_height": "8 stories, approximately 70 ft to the roof line (" + RELATED_REF + ")",
     "note": "Related's eight-story apartment building, part of 5150 Calle del Sol."},
    {"project": "related", "garage_parts": True, "parent": "w1351049829", "label": "5150 Calle del Sol, garage", "use": "Parking and amenities",
     "note": ("The seven-story garage with shared amenity space on its eighth level (Related addendum, Jan 2021). "
              "Levels per part from OpenStreetMap.")},
    {"project": "greystar", "osm": ["w1359187881"], "label": "2223 Calle de Luna", "height_ft": 85,
     "use": "Residential (184 homes)",
     "source_height": "8 stories, approximately 85 ft, about 90 ft to the parapet (" + GREYSTAR_REF + ")",
     "note": "184 homes (Greystar). Certificate of occupancy Nov 17, 2025 (state housing report)."},
    {"project": "greystar", "osm": ["w1359187880"], "label": "2230 Calle del Mundo", "height_ft": 85,
     "use": "Residential (186 homes)",
     "source_height": "8 stories, approximately 85 ft, about 90 ft to the parapet (" + GREYSTAR_REF + ")",
     "note": "186 homes (Greystar). Certificate of occupancy Aug 21, 2025 (state housing report)."},
    {"project": "ensemble-2302", "osm": ["w1359187882"], "label": "2310 Calle del Mundo", "stories": 8,
     "stories_src": "an eight-story building with 151 homes (" + DSEIR_REF + ", Table 2.2-1, PDF p. 36)",
     "use": "Residential (151 affordable homes)",
     "note": "151 homes (Ensemble, approved as 2302 Calle del Mundo). Certificate of occupancy Aug 31, 2025 "
             "(state housing report)."},
    {"project": "ensemble-p19", "osm": ["w1351049828"], "label": "5123 Calle del Sol, Parcel 19", "stories": 8,
     "stories_src": "eight-story mid-rise with 311 homes (" + NOD_REF + ")",
     "use": "Residential (311 homes)",
     "note": ("Building permit Apr 18, 2022 for 311 homes, filed as 2240 Calle de Luna; no certificate of occupancy in the "
              "state housing reports through 2025. The Draft SEIR (Aug 2026) lists 5123 Calle del Sol as constructed, "
              "and the newer document is followed.")},
]
GARAGE_DEFAULT_LEVELS = 8  # the Addendum's seven garage levels plus the amenity level

# Unbuilt parcels with approvals (APN -> note); everything else is the plan alone.
APPROVALS = {
    "097-05-060": "2263 Calle del Mundo: approved Nov 2020 for an eight-story building with 301 homes (file 20-1095), "
                  "extended 2022; not built.",
    "097-05-061": "Part of the 2263 Calle del Mundo site (1.94 acres), approved Nov 2020 for an eight-story building "
                  "with 301 homes; not built.",
    "097-05-058": ("2200 Calle de Luna: re-approved Feb 2023 for 583 homes in two 12-story and one 11-story buildings "
                   "(state housing report; file 23-1329); the Draft SEIR (Aug 2026) says the project was abandoned."),
    "097-05-056": ("2111 Tasman Drive: approved July 2023 for 900 homes in eight-story buildings (file 23-817); the Draft "
                   "SEIR (Aug 2026) says the project was abandoned."),
    "097-46-011": ("5185 Lafayette Street: approved 2023 for a 21-story building with 198 homes (file 23-842); the Draft "
                   "SEIR (Aug 2026) describes it as 18 stories. Not built."),
    "097-46-002": "2354 Calle del Mundo: approved 2021 for an 89-home mid-rise building; not built.",
    "097-46-029": ("5123 Calle del Sol Parcel 29: approved July 2019 for a 20-story building with 192 homes (Notice of "
                   "Determination); not built."),
    "097-46-015": "Holds an existing data center (5101 Lafayette Street); the plan allows housing here.",
}

LABELS = {
    "097-05-056": "2111 Tasman Drive", "097-05-058": "2200 Calle de Luna",
    "097-05-060": "2263 Calle del Mundo", "097-05-061": "2263 Calle del Mundo, east part",
    "097-46-011": "5185 Lafayette Street", "097-46-002": "2354 Calle del Mundo",
    "097-46-029": "5123 Calle del Sol, Parcel 29", "097-46-015": "5101 Lafayette Street",
}


# ---------------------------------------------------------------- fetching

def _get(url: str, dest):
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            tmp.write_bytes(r.read())
        tmp.rename(dest)
    return dest


def _arcgis(layer: str, name: str) -> gpd.GeoDataFrame:
    q = urllib.parse.urlencode({
        "where": "1=1", "geometry": ",".join(map(str, BBOX)), "geometryType": "esriGeometryEnvelope",
        "inSR": 4326, "spatialRel": "esriSpatialRelIntersects", "outFields": "*", "outSR": 4326, "f": "geojson"})
    path = _get(f"{layer}/query?{q}", RAW / f"te-{name}.geojson")
    return gpd.read_file(path).to_crs(UTM)


def _overture(kind: str) -> gpd.GeoDataFrame:
    cache = config.RAW / f"te-{kind}_tasman_east.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        d = ds.dataset(f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type={kind}/",
                       filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["osm"] = g["sources"].apply(
        lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), "") or "")
    g["way"] = g["osm"].str.split("@").str[0]
    return g.to_crs(UTM)


def _text(pdf_path, page: int) -> str:
    import pypdfium2 as pdfium

    t = pdfium.PdfDocument(str(pdf_path))[page].get_textpage().get_text_range()
    t = t.replace("\ufffe", "-").replace("\u00ad", "-").replace("\u2010", "-")
    return re.sub(r"\s+", " ", t).replace("'", "’")


def _check_documents() -> None:
    for key, d in DOCS.items():
        path = trace.fetch_document(d["url"], tb.DOCS / d["file"], d["sha256"])
        for page, phrases in d["check"].items():
            text = _text(path, page)
            for p in phrases:
                if re.sub(r"\s+", " ", p) not in text:
                    raise SystemExit(f"{d['file']} PDF p. {page + 1}: expected {p!r}")
    for key, d in PAGES.items():
        html = _get(d["url"], tb.DOCS / d["file"]).read_text(errors="replace")
        for p in d["check"]:
            if p not in html:
                raise SystemExit(f"{d['url']}: expected {p!r}")
    for mid, (file_no, phrase) in LEGISTAR.items():
        dest = tb.DOCS / f"te-legistar-{mid}.txt"
        if not dest.exists():
            api = f"https://webapi.legistar.com/v1/santaclara/matters/{mid}"
            with urllib.request.urlopen(f"{api}/versions", timeout=60) as r:
                key = json.load(r)[-1]["Key"]
            with urllib.request.urlopen(f"{api}/texts/{key}", timeout=60) as r:
                dest.write_text(json.load(r).get("MatterTextPlain") or "")
        if phrase not in re.sub(r"\s+", " ", dest.read_text()):
            raise SystemExit(f"Legistar file {file_no}: expected {phrase!r}")


def _apr() -> list[dict]:
    path = _get(APR_URL, RAW / "te-apr-a2.json")
    return json.loads(path.read_text())["result"]["records"]


# ---------------------------------------------------------------- build

def _label(parcel, addr: gpd.GeoDataFrame, used: set[str]) -> str:
    """The approval's address, else the City site address nearest the middle of the parcel."""
    if parcel["APN"] in LABELS:
        label = LABELS[parcel["APN"]]
    else:
        near = addr[addr.geometry.within(parcel.geometry.buffer(3))].copy()
        near["d"] = near.geometry.distance(parcel.geometry.representative_point())
        names = [n for n in near.sort_values("d")["FULLADDR"].dropna() if n not in used]
        label = names[0] if names else f"Parcel {parcel['APN']}"
    label = label.replace("Calle De ", "Calle de ").replace("Calle Del ", "Calle del ")
    used.add(label)
    return label


def _site_parcels(parcels: gpd.GeoDataFrame, apns: list[str]) -> gpd.GeoDataFrame:
    """Active parcels for a project's APNs, following retired APNs to the parcels that replaced them."""
    active = parcels[parcels["LNDPARSTATUS"] == "A"]
    src = parcels[parcels["APN"].isin(apns)]
    if src.empty:
        raise SystemExit(f"APNs {apns} not in the City's parcels")
    area = shapely.union_all(src.geometry.to_numpy())
    share = active.geometry.intersection(area).area / active.geometry.area
    out = active[share > 0.5]
    if abs(out.geometry.area.sum() - area.area) > 0.02 * area.area:
        raise SystemExit(f"APNs {apns}: replacement parcels don't cover the same land")
    return out


def main() -> None:
    _check_documents()
    apr = _apr()
    co = {}
    for r in apr:
        if r["CO_ISSUE_DT1"] and int(r["NO_OTHER_FORMS_OF_READINESS"] or 0) > 0:
            co.setdefault(r["STREET_ADDRESS"].split(",")[0].upper(), []).append(r)
    for proj, spec in BUILT.items():
        for a in spec["apr"]:
            if a not in co:
                raise SystemExit(f"{a}: no certificate of occupancy row in the state housing reports")

    parcels = _arcgis(SC_PARCELS, "sc-land-parcels")
    addresses = _arcgis(SC_ADDRESSES, "sc-site-addresses")
    plan = parcels[(parcels["SPPLAN"] == "TE") & (parcels["LNDPARSTATUS"] == "A")]
    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
                 ["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]
    print(f"[{PROJECT_ID}] {len(plan)} active plan parcels, {plan.geometry.area.sum() / tb.ACRE_M2:.1f} ac "
          f"(site {site_utm.area / tb.ACRE_M2:.1f} ac)")

    built_sites = {p: _site_parcels(parcels, s["apns"]) for p, s in BUILT.items()}
    built_apns = set().union(*[set(g["APN"]) for g in built_sites.values()])
    for p, g in built_sites.items():
        print(f"[{PROJECT_ID}]   built {p:>14}: {', '.join(sorted(g['APN']))} "
              f"({g.geometry.area.sum() / tb.ACRE_M2:.2f} ac)")

    buildings = _overture("building")
    parts = _overture("building_part")
    features = []
    built_geoms = []

    def building(geom, props):
        geom = trace.as_multipolygon(shapely.make_valid(geom.simplify(0.3)))
        built_geoms.append(geom)
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})

    for fp in FOOTPRINTS:
        proj_site = shapely.union_all(built_sites[fp["project"]].geometry.to_numpy())
        base = {"kind": "building", "stage": "complete", "podium_ft": None, "base_ft": 0, "phase": None}
        if fp.get("garage_parts"):
            used = {f["part"] for f in FOOTPRINTS if "part" in f}
            parent = shapely.union_all(buildings[buildings["way"] == fp["parent"]].geometry.to_numpy())
            g = parts[parts.geometry.within(parent.buffer(1)) & ~parts["way"].isin(used)]
            if g.empty:
                raise SystemExit("Related garage parts not found")
            for lv, grp in g.groupby(g["num_floors"].fillna(GARAGE_DEFAULT_LEVELS).astype(int)):
                ways = ", ".join(sorted(grp["way"]))
                building(shapely.union_all(grp.geometry.to_numpy()), {
                    **base, "label": fp["label"], "height_ft": round(lv * FT_PER_STORY), "use": fp["use"],
                    "illustrative": True,
                    "source": (f"illustrative: footprint OpenStreetMap building parts {ways} (via Overture "
                               f"{config.OVERTURE_RELEASE}); {lv} levels ("
                               + ("OpenStreetMap building:levels" if grp["num_floors"].notna().all()
                                  else "the addendum's seven-story garage with amenity space on the eighth level")
                               + f"), {EST}"),
                    "note": fp["note"]})
            continue
        if "part" in fp:
            g = parts[parts["way"] == fp["part"]]
            what = f"OpenStreetMap building part {fp['part']}"
        else:
            g = buildings[buildings["way"].isin(fp["osm"])]
            what = "OpenStreetMap building " + " and ".join(fp["osm"])
        if len(g) != len(fp.get("osm", [1])):
            raise SystemExit(f"{fp['label']}: expected footprint(s) {fp.get('osm') or fp.get('part')}, found {len(g)}")
        geom = shapely.union_all(g.geometry.to_numpy())
        if geom.intersection(proj_site).area < 0.9 * geom.area:
            raise SystemExit(f"{fp['label']}: footprint is not on the project's parcels")
        if "stories" in fp:
            h, illus = round(fp["stories"] * FT_PER_STORY), True
            src = (f"illustrative: footprint {what} (via Overture {config.OVERTURE_RELEASE}); {fp['stories_src']}; "
                   f"{EST}")
        else:
            h, illus = fp["height_ft"], False
            src = f"{what} (via Overture {config.OVERTURE_RELEASE}); height: {fp['source_height']}"
        building(geom, {**base, "label": fp["label"], "height_ft": h, "use": fp["use"], "illustrative": illus,
                        "source": src, "note": fp["note"]})

    # ---- the rest of the plan to its height limits
    built_union = shapely.union_all(built_geoms)
    open_parcels = plan[~plan["APN"].isin(built_apns)]
    addr = addresses.copy()
    used_labels: set[str] = set()
    for _, r in open_parcels.sort_values("APN").iterrows():
        g = r.geometry.difference(built_union).intersection(site_utm.buffer(1))
        g = trace.as_multipolygon(shapely.make_valid(g.simplify(0.4)))
        if g.area < 50:
            continue
        label = _label(r, addr, used_labels)
        approval = APPROVALS.get(r["APN"])
        note = (approval + " " if approval else "") + (
            f"Drawn to the plan's limits: towers up to {TOWER_FT} ft (or the FAA limit, if lower) over podiums up "
            f"to {PODIUM_FT} ft. Buildings over about 175 ft need an FAA no-hazard determination.")
        features.append({"type": "Feature", "properties": {
            "kind": "block", "block": r["APN"], "label": label, "stage": "entitled",
            "height_ft": TOWER_FT, "podium_ft": PODIUM_FT, "base_ft": 0,
            "use": "Transit Neighborhood: housing with ground-floor retail or other active uses", "phase": None,
            "illustrative": True,
            "source": (f"illustrative: City of Santa Clara land parcel {r['APN']} (Tasman East plan area); "
                       f"height envelope from the plan's standards: towers \"would not exceed 220 feet or the FAA "
                       f"Part 77 height limit, whichever is lower\" ({FEIR_REF}), podiums \"shall not exceed 85 feet "
                       f"above existing grade\" ({DEIR_REF}); unchanged in the {DSEIR_REF}, PDF p. 39"),
            "note": note}, "geometry": mapping(tb.to_wgs(g))})
        print(f"[{PROJECT_ID}]   open {r['APN']}: {g.area / tb.ACRE_M2:5.2f} ac  {label}"
              + ("  *" if approval else ""))

    n_build = sum(f["properties"]["kind"] == "building" for f in features)
    open_ac = sum(gpd.GeoSeries([shape(f["geometry"])], crs=4326).to_crs(UTM).area.iloc[0]
                  for f in features if f["properties"]["kind"] == "block") / tb.ACRE_M2
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Buildings finished since 2022 are drawn on their OpenStreetMap footprints, at official heights where "
                "the City's records give them (the Related towers at about 214 and 217 ft, the Greystar buildings at "
                f"about 85 ft) and otherwise estimated from official story counts at {FT_PER_STORY} ft a story "
                "(illustrative); SummerHill's 2333 Calle del Mundo has no official height and is outlined only. "
                f"Every other parcel in the plan ({open_ac:.0f} acres) is an illustrative height envelope: the plan "
                f"allows towers up to {TOWER_FT} ft (or the FAA limit, if lower) over podiums up to {PODIUM_FT} ft. "
                "These are limits, not designs. Streets are outside the parcels; the plan's undecided park sites "
                "are not cut out."),
            "note": ("Built buildings are drawn on their real footprints; every other parcel shows the plan's "
                     "height limits, not a design."),
            "sourceUrl": DOCS["feir"]["url"],
            "sourceLabel": "Final EIR, 2018 (PDF)",
            "georeference": {"method": "none: City of Santa Clara GIS parcels and OpenStreetMap footprints, no "
                                       "traced figure"},
            "license": ("Parcels: City of Santa Clara open data (map.santaclaraca.gov). Footprints: "
                        + tb.OSM_LICENSE + "."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[{PROJECT_ID}] wrote {path.relative_to(config.ROOT)} ({n_build} buildings, "
          f"{len(features) - n_build} parcel envelopes, {path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
