"""Alameda Marina: the three residential phases of the Alameda Marina Master Plan.

Sources (City of Alameda records, Legistar):
- Height limits: Planning Board staff report on the Master Plan (May 2018, Legistar matter 7315): "the
  Master Plan establishes a building height limit of 65 feet for the two major residential buildings on
  each side of the commercial core area and a 45-foot height limit for the balance of the site."
- Phase I, "Wrap A" (The Launch, 360 homes, complete): footprint from OpenStreetMap via Overture
  (relation r16011797, "The Launch Apartments"); height from the Planning Board staff report on its design
  review (Oct 14, 2019, matter 9050): "The new four- to five-story building varies between approximately
  50' to 60' in height", drawn at 60 ft.
- Phase II (182 townhomes in 31 buildings, under construction per the City Council staff report of June 1,
  2026, matter 15877): the lots of Tract 8610 as the Alameda County Assessor maps them (books 71-292 and
  71-293), closed over the private streets between them, drawn to the master plan's 45-ft limit.
- Phase III, "Wrap B" (The Foundry, 259 homes, approved 2023, not started): Lot 4 of Tract 8500, which
  Tract 8711 "The Foundry" (2024) subdivides for condominiums; the Assessor's parcel 71-291-12, between
  Lot 3 (71-291-8) and the Tract 8610 townhomes, as on the Tract 8711 map. Height from
  the Planning Board staff report of July 10, 2023 (matter 13013): a 5-story building that "varies in height
  between 50 and 65 feet" (64 ft 11 in at most); drawn at 65 ft over the lot.

What this is and isn't: Phases II and III are drawn as whole lots at their height limits, not as building
designs, so they're labelled illustrative. Building 19 and the other maritime commercial buildings, the
marina, parks and streets aren't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_alameda_marina
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

import geopandas as gpd
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import official_boundaries as ob
from . import traced_boundaries as tb

PROJECT_ID = "alameda-marina"
UTM = tb.UTM
ACRE_M2 = tb.ACRE_M2
OUT = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
RAW = config.ROOT / "data" / "raw" / "massing"
BBOX = (-122.2560, 37.7720, -122.2420, 37.7800)

LAUNCH_OSM = "r16011797"
FOUNDRY_APN = "71-291-12"  # Tract 8711 Lot 1, between Lot 3 of Tract 8500 (71-291-8) and Tract 8610
TOWNHOME_PREFIXES = ("71-292-", "71-293-")


def _legistar(matter: int, text_id: int, title: str) -> dict:
    return {"matter": matter, "title": title,
            "api": f"https://webapi.legistar.com/v1/alameda/matters/{matter}/texts/{text_id}"}


SR_MASTER_PLAN = _legistar(7315, 7770, "Planning Board staff report, Alameda Marina Master Plan (May 2018)")
SR_WRAP_A = _legistar(9050, 9650, "Planning Board staff report, Phase I (Wrap A) design review (Oct 14, 2019)")
SR_WRAP_B = _legistar(13013, 13902, "Planning Board staff report, Phase III (Wrap B) design review (July 10, 2023)")
CC_2026 = _legistar(15877, 17084, "City Council staff report, Phase III affordable housing amendment (June 1, 2026)")
QUOTES = {
    7315: ["a building height limit of 65 feet for the two major residential buildings on each side of the "
           "commercial core area and a 45-foot height limit for the balance of the site"],
    9050: ["The new four- to five-story building varies between approximately 50' to 60' in height"],
    13013: ["Wrap B is a 5-story multifamily building that varies in height between 50 and 65 feet"],
    15877: ["the Phase I residential rental building is complete and occupied, and the Phase II ownership "
            "buildings are under construction"],
}
PARCELS = {
    "file": "alameda-marina-parcels.geojson",
    "url": f"{ob.ALCO_PARCELS}/query?" + urllib.parse.urlencode({
        "where": f"APN = '{FOUNDRY_APN}' OR APN LIKE '71-292-%' OR APN LIKE '71-293-%'",
        "outFields": "APN", "outSR": 4326, "f": "geojson"}),
}


def _text(rec: dict) -> str:
    cache = RAW / f"am-legistar-{rec['matter']}.json"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(rec["api"]) as r:
            cache.write_bytes(r.read())
    text = " ".join(json.loads(cache.read_text())["MatterTextPlain"].split())
    for q in QUOTES.get(rec["matter"], []):
        if q not in text:
            raise SystemExit(f"Legistar matter {rec['matter']} no longer says {q!r}")
    return text


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "buildings_alameda_marina.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        x0, y0, x1, y1 = BBOX
        f = ((pc.field("bbox", "xmin") < x1) & (pc.field("bbox", "xmax") > x0)
             & (pc.field("bbox", "ymin") < y1) & (pc.field("bbox", "ymax") > y0))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["osm"] = g["sources"].apply(
        lambda s: (next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None) or "").split("@")[0])
    return g.to_crs(UTM)


def _parcels() -> gpd.GeoDataFrame:
    path = RAW / PARCELS["file"]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(PARCELS["url"], headers={"User-Agent": "Mozilla/5.0 (bay-area-megaprojects pipeline)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            path.write_bytes(r.read())
    g = gpd.read_file(path)
    if g.empty:
        raise SystemExit("Alameda Marina parcels: the query returned no features")
    return g.to_crs(UTM)


def main() -> None:
    for rec in (SR_MASTER_PLAN, SR_WRAP_A, SR_WRAP_B, CC_2026):
        _text(rec)
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]
    parcels = _parcels()
    parcels = parcels[parcels.geometry.representative_point().within(site_utm.buffer(2))]
    foundry = parcels[parcels["APN"] == FOUNDRY_APN].geometry
    if len(foundry) != 1:
        raise SystemExit(f"parcel {FOUNDRY_APN} (Lot 4, The Foundry) not found once")
    foundry = foundry.iloc[0]
    th = parcels[parcels["APN"].str.startswith(TOWNHOME_PREFIXES)]
    if len(th) < 100:
        raise SystemExit(f"only {len(th)} Tract 8610 townhome parcels found")
    townhomes = shapely.union_all(th.geometry.to_numpy()).buffer(6, join_style="mitre").buffer(-6, join_style="mitre")
    townhomes = townhomes.intersection(site_utm)

    bldgs = _buildings()
    launch = bldgs[bldgs["osm"] == LAUNCH_OSM]
    if len(launch) != 1:
        raise SystemExit("The Launch's OpenStreetMap footprint not found")
    launch_geom = launch.geometry.iloc[0]
    mapped_th = bldgs[bldgs.geometry.centroid.within(townhomes)]
    print(f"[alameda-marina] Launch footprint {launch_geom.area:.0f} m²; Foundry lot {foundry.area / ACRE_M2:.2f} ac; "
          f"townhome lots {townhomes.area / ACRE_M2:.2f} ac ({len(th)} parcels, {len(mapped_th)} buildings mapped in OSM)")

    to_wgs = tb.to_wgs
    feats = [
        ({"kind": "building", "block": "Wrap A", "label": "The Launch", "stage": "complete", "height_ft": 60,
          "podium_ft": None, "base_ft": 0, "use": "Residential (360 rental homes, 49 affordable)", "phase": "Phase I",
          "illustrative": False, "homes": 360,
          "source": (f"footprint: OpenStreetMap {LAUNCH_OSM} (\"The Launch Apartments\") via Overture "
                     f"{config.OVERTURE_RELEASE}; height: \"varies between approximately 50' to 60' in height\", "
                     f"{SR_WRAP_A['title']} ({SR_WRAP_A['api']}); complete per {CC_2026['title']} ({CC_2026['api']})"),
          "note": "A four- to five-story building, 50–60 ft, around a parking garage; drawn at 60 ft."},
         launch_geom),
        ({"kind": "block", "block": "Tract 8610", "label": "Phase II townhomes", "stage": "construction",
          "height_ft": 45, "podium_ft": None, "base_ft": 0, "use": "Residential (182 townhomes, 25 affordable)",
          "phase": "Phase II", "illustrative": True, "homes": 182,
          "source": (f"illustrative: the Tract 8610 lots (Alameda County Assessor parcels 71-292 and 71-293, "
                     f"{ob.ALCO_PARCELS}) drawn to the master plan's 45-ft limit for the balance of the site, "
                     f"{SR_MASTER_PLAN['title']} ({SR_MASTER_PLAN['api']}); under construction per {CC_2026['title']}"),
          "note": (f"182 townhomes in 31 buildings, drawn as their lots at the 45-ft limit. {len(mapped_th)} of the "
                   "buildings are already mapped in OpenStreetMap.")},
         townhomes),
        ({"kind": "block", "block": "Lot 4", "label": "The Foundry (Wrap B)", "stage": "entitled", "height_ft": 65,
          "podium_ft": None, "base_ft": 0, "use": "Residential (259 rental homes and a work/live unit)",
          "phase": "Phase III", "illustrative": True, "homes": 259,
          "source": (f"illustrative: Lot 4 of Tract 8500 (Tract 8711 \"The Foundry\"; Alameda County Assessor parcel "
                     f"{FOUNDRY_APN}) drawn to the building's 65-ft maximum, \"varies in height between 50 and 65 "
                     f"feet\", {SR_WRAP_B['title']} ({SR_WRAP_B['api']})"),
          "note": ("Approved in 2023 with 259 homes; in July 2026 the City cut its affordable homes from 43 to 21 "
                   "(Ordinance 3406) and the applicant said construction could start that summer.")},
         foundry),
    ]
    features = []
    for props, g in feats:
        g = trace.as_multipolygon(shapely.make_valid(g.intersection(site_utm.buffer(2)).simplify(0.4)))
        c = g.centroid
        if not site_utm.buffer(20).contains(c):
            raise SystemExit(f"{props['label']} is off the site")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(g))})
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("The finished Phase I building (The Launch) uses its real footprint and the height in its "
                        "approved design. Phase II's townhome lots and Phase III's lot (The Foundry) are illustrative: "
                        "whole lots drawn to the master plan's 45-ft and 65-ft limits, not building designs. Building "
                        "19 and the other maritime commercial buildings, the marina, parks and streets aren't drawn."),
            "note": "Unbuilt phases are drawn as lots at their height limits, not as building designs.",
            "sourceUrl": SR_MASTER_PLAN["api"],
            "sourceLabel": "Alameda Marina master plan staff report, 2018",
            "documents": [SR_MASTER_PLAN["api"], SR_WRAP_A["api"], SR_WRAP_B["api"], CC_2026["api"], PARCELS["url"]],
            "georeference": "Footprint and parcels as published (OpenStreetMap via Overture; Alameda County Assessor parcels).",
            "license": "Building footprint: " + tb.OSM_LICENSE + ". Parcels: Alameda County open data (county disclaimer).",
        },
        "features": features,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[alameda-marina] wrote {OUT.relative_to(config.ROOT)} ({len(features)} features, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
