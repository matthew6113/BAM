"""Piers 30–32 and Seawall Lot 330: the zoning height envelope on the seawall lot, and the pier outline.

Nothing here is entitled. The project split in July 2025 (Port Resolution 25-40): the piers are paused
for 18 months, and Seawall Lot 330 has an SB 423 application for 568 homes under Planning review since
May 13, 2026 (Planning record 2025-011323PRJ).

Sources:
- Height limits: DataSF "Zoning Map – Height and Bulk Districts" (h9wh-cg3m, Public Domain U.S.
  Government), clipped to the site's assessor parcels (DataSF Parcels acdm-wktn, ODC-PDDL), the same
  parcels as data/boundaries/piers-30-32.geojson.
  - Seawall Lot 330 (3770/002, 3771/002) is all in district 65/105-R. In the R bulk district the first
    number is the podium height limit and the second the tower height limit; only towers meeting the
    bulk and spacing controls of Sec. 270(e) may rise above the podium limit (Planning Code Sec. 263.19).
    So it is drawn as a 65-ft podium under a 105-ft tower envelope over the whole lot.
  - Piers 30–32 (9900/030, 9900/032) are in district 40-X. Port Commission Item 11B (March 6, 2026)
    confirms "the 40-foot height limit at Piers 30-32". The pier is drawn as an outline only, at no
    height: the deck is to be demolished and a smaller single pier rebuilt (2024 term sheet, Exhibit B;
    "a smaller Pier area", Item 11B), the negotiations are paused, and no official plan says where on it
    a building would go. A 40-ft box over the whole 13-acre deck would show a building that no plan
    proposes. The limit is stated in the feature's note.

Not drawn:
- The SB 423 proposal itself (a 23-story, 230-ft tower on the north of the lot and a 10-story, 105-ft
  mass on the south; Planning record 2025-011323PRJ). Its application plans weren't found in an official
  source, and the record's words don't locate the masses precisely enough to draw them. Its tower would
  exceed the zoning limit drawn here (SB 423 with the state density bonus). The 2024 term sheet's
  Exhibit E site plan is for the superseded 713-home scheme, so it isn't traced.
- Existing structures that aren't part of the project: Red's Java House on the pier's Embarcadero edge
  and six low (about 3–6 m) structures mapped on the seawall lot. They stay in the base map as flat
  footprints. The build lists them and stops if anything taller than 10 m (or unmeasured, other than
  Red's Java House) appears on the site.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_piers_30_32
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

PROJECT_ID = "piers-30-32"
UTM = "EPSG:26910"
BBOX = (-122.3895, 37.7840, -122.3830, 37.7885)  # lon/lat window around the site
RAW = config.ROOT / "data" / "raw" / "massing"
DOCS = config.ROOT / "data" / "raw" / "docs"

_WINDOW = "POLYGON(({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))".format(*BBOX)
HEIGHTS = {
    "title": "DataSF Zoning Map – Height and Bulk Districts",
    "landing": "https://data.sf.gov/d/h9wh-cg3m",
    "url": "https://data.sf.gov/resource/h9wh-cg3m.geojson?" + urllib.parse.urlencode({
        "$where": f"intersects(the_geom, '{_WINDOW}')", "$limit": 5000}),
}
PARCELS = {
    "title": "DataSF Parcels",
    "landing": "https://data.sf.gov/d/acdm-wktn",
    "url": "https://data.sf.gov/resource/acdm-wktn.geojson?" + urllib.parse.urlencode({
        "$where": "blklot in ('9900030', '9900032', '3771002', '3770002') and active = true", "$limit": 5000}),
}
SWL = ("3770002", "3771002")
PIER = ("9900030", "9900032")

ITEM_11B = {
    "title": "Port Commission Item 11B, Piers 30-32 feasibility improvement ideas (March 6, 2026)",
    "url": "https://www.sfport.com/sites/default/files/2026-03/item_11b_piers_30-32_feasibility_improvement_ideas_-_info.docx.pdf",
    "sha256": "ad2e2e3838f041ceb2917393c5c4ac176de34332981d5c5d25240850c0aa2d1b",
    "quote": "40-foot height limit at Piers 30-32",
}
PLANNING_RECORD = "https://data.sfgov.org/resource/qvu5-m3a2.json?record_id=2025-011323PRJ"
CODE_263_19 = "Planning Code Sec. 263.19"


def _get(url: str, out) -> object:
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url) as r:
            out.write_bytes(r.read())
    return out


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "p3032-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "names", "height"], filter=f), cache)
    t = pq.read_table(cache)
    return gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                            geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)),
                            crs=4326).to_crs(UTM)


def _check_item_11b() -> None:
    import pypdfium2 as pdfium

    pdf = trace.fetch_document(ITEM_11B["url"], DOCS / "p3032-port-item-11b-2026-03.pdf", ITEM_11B["sha256"])
    doc = pdfium.PdfDocument(str(pdf))
    text = " ".join(" ".join(doc[i].get_textpage().get_text_range().split()) for i in range(len(doc)))
    if ITEM_11B["quote"] not in text:
        raise SystemExit(f"Item 11B no longer says {ITEM_11B['quote']!r}")


def _check_planning_record() -> str:
    rec = json.loads(_get(PLANNING_RECORD, RAW / "p3032-planning-2025-011323PRJ.json").read_text())[0]
    desc = rec["description"]
    for want in ("568-unit", "23 stories and 230 feet", "10 stories and 105 feet"):
        if want not in desc:
            raise SystemExit(f"Planning record 2025-011323PRJ no longer says {want!r}")
    return rec["record_status"]


def main() -> None:
    hb = gpd.read_file(_get(HEIGHTS["url"], RAW / "p3032-height_bulk.geojson")).to_crs(UTM)
    parcels = gpd.read_file(_get(PARCELS["url"], RAW / "p3032-parcels.geojson")).to_crs(UTM)
    if sorted(parcels["blklot"]) != sorted(SWL + PIER):
        raise SystemExit(f"unexpected parcels {sorted(parcels['blklot'])}")
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    # Zoning clipped to each parcel; report every district that touches it.
    zones = gpd.overlay(parcels[["blklot", "geometry"]], hb[["height", "geometry"]], how="intersection")
    zones["area"] = zones.area
    for blklot, grp in zones.groupby("blklot"):
        print(f"[{PROJECT_ID}] {blklot}: " + ", ".join(f"{h} {a:,.1f} m²" for h, a in zip(grp["height"], grp["area"])))
    zones = zones[zones["area"] > 20]  # drop slivers where district lines run along the parcel edge
    swl_d = set(zones[zones["blklot"].isin(SWL)]["height"])
    pier_d = set(zones[zones["blklot"].isin(PIER)]["height"])
    if swl_d != {"65/105-R"} or pier_d != {"40-X"}:
        raise SystemExit(f"zoning changed: Seawall Lot 330 {swl_d}, piers {pier_d}")

    _check_item_11b()
    status = _check_planning_record()
    print(f"[{PROJECT_ID}] Item 11B confirms the 40-ft pier limit; Planning record 2025-011323PRJ: {status}")

    # Existing structures on the site: none belongs to the project; they stay in the base map.
    b = _buildings()
    on = b[b.geometry.intersection(site_utm).area > 0.2 * b.geometry.area]
    for _, r in on.iterrows():
        name = (r["names"] or {}).get("primary")
        print(f"[{PROJECT_ID}] existing structure {r['id'][:8]} {name or ''} {r.geometry.area:.0f} m², "
              f"height {r['height']} m (base map, not drawn)")
        if name != "Red's Java House" and not (r["height"] == r["height"] and r["height"] <= 10):
            raise SystemExit(f"unexpected structure {r['id']} on the site; look before drawing")

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    clean = lambda g: trace.as_multipolygon(shapely.make_valid(g.buffer(0.05).buffer(-0.05).simplify(0.3)))  # noqa: E731
    zoning = f"{HEIGHTS['title']} ({HEIGHTS['landing']})"
    parcels_src = f"{PARCELS['title']} ({PARCELS['landing']})"
    features = []

    swl = shapely.union_all(zones[zones["blklot"].isin(SWL)].geometry.to_numpy())
    features.append({"type": "Feature", "geometry": mapping(to_wgs(clean(swl))), "properties": {
        "kind": "block",
        "block": "SWL 330",
        "label": "Seawall Lot 330",
        "stage": "proposed",
        "height_ft": 105,
        "podium_ft": 65,
        "base_ft": 0,
        "use": None,
        "phase": None,
        "illustrative": True,
        "source": (f"illustrative: drawn to zoning district \"65/105-R\" in {zoning}, clipped to parcels "
                   f"3770/002 and 3771/002 in {parcels_src}; 65 ft podium and 105 ft tower limits per "
                   f"{CODE_263_19}"),
        "note": ("Zoning envelope, not the proposal: a 65-ft podium limit with towers allowed to 105 ft. "
                 "The SB 423 application under review proposes 23 stories (230 ft) and 10 stories (105 ft), "
                 f"which isn't drawn because no official plan locates them ({PLANNING_RECORD})."),
    }})

    pier = shapely.union_all(zones[zones["blklot"].isin(PIER)].geometry.to_numpy())
    features.append({"type": "Feature", "geometry": mapping(to_wgs(clean(pier))), "properties": {
        "kind": "block",
        "block": "Piers 30–32",
        "label": "Piers 30–32",
        "stage": "paused",
        "height_ft": None,
        "podium_ft": None,
        "base_ft": 0,
        "use": None,
        "phase": None,
        "illustrative": False,
        "source": (f"outline: parcels 9900/030 and 9900/032 in {parcels_src}; zoning district \"40-X\" in "
                   f"{zoning}; 40-ft limit confirmed by {ITEM_11B['title']} ({ITEM_11B['url']}), p. 4"),
        "note": ("Outline only. The 40-ft height limit applies, but the pier is to be rebuilt smaller and "
                 "no official plan places a building on it, so no volume is drawn."),
    }})

    for f in features:
        c = shapely.geometry.shape(f["geometry"]).centroid
        if not gpd.GeoSeries([c], crs=4326).to_crs(UTM).iloc[0].within(site_utm.buffer(1)):
            raise SystemExit(f"{f['properties']['label']} falls outside the site")
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: Seawall Lot 330 is drawn to its zoning height limits (a 65-ft podium "
                "with towers allowed to 105 ft), not as the building proposed there. Piers 30–32 are outlined "
                "only: the 40-ft limit applies, but the pier is to be rebuilt smaller and no official plan "
                "places a building on it. The SB 423 proposal for the lot (23 and 10 stories) isn't drawn."
            ),
            "note": "The seawall lot shows the zoning limits, not the proposed towers; the pier is outlined only.",
            "sourceUrl": HEIGHTS["landing"],
            "sourceLabel": "Height and bulk districts (DataSF)",
            "georeference": {"zoning": "GIS layers, used as published (no tracing)"},
            "license": ("Zoning: DataSF (Public Domain U.S. Government). Parcels: DataSF (ODC Public Domain "
                        "Dedication and License)."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"[{PROJECT_ID}] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size // 1024} KB)")


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
