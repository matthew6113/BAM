"""Santana Row Master Plan Update (San José): illustrative envelopes of the four proposed office buildings.

Source: City of San José, Revised Notice of Preparation of an EIR for the Santana Row Master Plan Update (files
PDC22-004 and ER22-107, February 2026; CEQAnet SCH 2013122059, document 3, attachment lrKplZ):
- Table 4.0-1, "Proposed Santana Row Project Land Uses" (PDF p. 9), "Square Footage (Maximum No. of Stories)" and
  "Net Increase/Decrease" over "the existing entitlement (PDC13-050)":
  "Lot 1A/B/C 700,000 (144 feet tall) + 579,629 sf Office"; "Lot 2B 325,000 (144 feet tall) + 245,797 sf Office";
  "Lot 10A 200,000 (139 feet tall) + 171,655 sf Office"; "Lot 17 275,000 (162 feet tall) + 275,000 sf Office";
  "Lot 22 0 +0 Potential location for new signage"; "Total 1,500,000 + 1,272,081 sf".
- Project description (PDF p. 4): "establish the new conforming heights for existing Lots 1, 2B, and 10A of 150 feet
  (plus allowable mechanical screening parapet)"; "merge existing Lots 1A, 1B, and 1C into a single parcel";
  "merge 524, 534, and 544 Dudley Avenue into a single parcel (Lot 17) with a maximum height limit of 162 feet (plus
  allowable mechanical screening parapet)"; "an increase of 1,460 spaces on Lot 1 and 831 spaces on Lot 17, and a
  loss of 97 spaces on Lot 2B".
- Figure 4, "Lot Division Diagram" (PDF p. 8): where the lots are.

How it's drawn:
- Footprints: each lot is the Santa Clara County parcels (data.sccgov.org ubcd-cewv) for the APNs the NOP names that
  lie in it on Figure 4: Lot 1A/B/C = 277-33-020, -019 and -017 (along Stevens Creek Boulevard from Winchester
  Boulevard to Santana Row); Lot 2B = 277-40-029; Lot 10A = 277-40-031; Lot 17 = 277-38-003, -004 and -005 (544, 534
  and 524 Dudley Avenue). boundary_santana_row fits Figure 4 to the parcels and checks that each lot's label falls
  inside them. Lot 22, a signage site with no floor area, isn't drawn.
- Heights: Table 4.0-1's height for each lot, to the roof. The parapets the description allows above them aren't
  drawn.
- The NOP shows no building design: each footprint is the whole lot (an envelope), not a building outline, so the
  massing is illustrative. The new floor area would also share the lots with new parking (1,460 spaces on Lot 1,
  831 on Lot 17). The existing Santana Row buildings aren't drawn (the base map has them).
- Stage: entitlement (the EIR is being prepared; no Draft EIR as of Oct 19, 2026).

    uv run --directory pipeline python -m bam_pipeline.sites.massing_santana_row
"""

from __future__ import annotations

import json

import geopandas as gpd
import pdfplumber
import shapely
from shapely.geometry import mapping, shape

from .. import config
from . import boundary_santana_row as b
from . import official_boundaries as ob

PROJECT_ID = "santana-row"
UTM = ob.UTM
SQFT = 10.7639
TABLE_PAGE = 8  # zero-based: PDF p. 9, Table 4.0-1

# lot -> (Table 4.0-1 square footage, net increase, height in feet, parking change in the description)
TABLE = {
    "Lot 1A/B/C": {"sqft": "700,000", "net": "+ 579,629 sf", "ft": 144, "limit": "150 feet (plus allowable mechanical "
                   "screening parapet) for Lot 1", "parking": "1,460 new parking spaces on Lot 1",
                   "merge": "Lots 1A, 1B and 1C would be merged into one parcel."},
    "Lot 2B": {"sqft": "325,000", "net": "+ 245,797 sf", "ft": 144, "limit": "150 feet (plus allowable mechanical "
               "screening parapet) for Lot 2B", "parking": "a loss of 97 parking spaces on Lot 2B", "merge": ""},
    "Lot 10A": {"sqft": "200,000", "net": "+ 171,655 sf", "ft": 139, "limit": "150 feet (plus allowable mechanical "
                "screening parapet) for Lot 10A", "parking": "", "merge": ""},
    "Lot 17": {"sqft": "275,000", "net": "+ 275,000 sf", "ft": 162, "limit": "a maximum height limit of 162 feet (plus "
               "allowable mechanical screening parapet)", "parking": "831 new parking spaces on Lot 17",
               "merge": "524, 534 and 544 Dudley Avenue would be merged into one parcel."},
}


def check_table(path) -> None:
    text = pdfplumber.open(str(path)).pages[TABLE_PAGE].extract_text()
    flat = " ".join(text.split())
    if "Table 4.0-1: Proposed Santana Row Project Land Uses" not in flat:
        raise SystemExit(f"PDF page {TABLE_PAGE + 1} does not hold Table 4.0-1")
    for lot, t in TABLE.items():
        for want in (f"{t['sqft']} ({t['ft']} feet tall)", t["net"]):
            if want not in flat:
                raise SystemExit(f"Table 4.0-1 does not show {want!r} for {lot}")
    if "1,500,000" not in flat or "+ 1,272,081 sf" not in flat:
        raise SystemExit("Table 4.0-1 totals have changed")


def main() -> None:
    path = b.nop_path()
    check_table(path)
    site_fc = json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())
    checks = site_fc["properties"].get("georeference", {}).get("label_distance_to_lot_m")
    if not checks:
        raise SystemExit("run bam_pipeline.sites.boundary_santana_row first (it checks the lots against Figure 4)")
    site = gpd.GeoSeries([shape(site_fc["features"][0]["geometry"])], crs=4326).to_crs(UTM).iloc[0]
    g = b.parcels()

    features = []
    for lot, t in TABLE.items():
        apns = b.LOTS[lot]["apns"]
        geom = b.lot_shape(g, apns)
        # Open away hairline slivers and self-touching corners so every output polygon is valid.
        geom = geom.buffer(-0.01, join_style="mitre").buffer(0.01, join_style="mitre").simplify(0.3, preserve_topology=True)
        if not geom.within(site.buffer(2.0)):
            raise SystemExit(f"santana-row: {lot} is not inside the site boundary")
        wgs = gpd.GeoSeries([geom], crs=UTM).to_crs(4326).iloc[0]
        geometry = ob._round(mapping(wgs))
        if not shape(geometry).is_valid:
            raise SystemExit(f"santana-row: {lot}'s envelope is not a valid polygon after rounding")
        apn_text = ", ".join(b.fmt(a) for a in apns)
        note = (f"Table 4.0-1 gives {lot} {t['sqft']} sq ft of office, {t['ft']} feet tall ({t['net']} over the "
                f"existing entitlement). The description sets {t['limit']}"
                + (f" and {t['parking']}" if t["parking"] else "") + ". " + (t["merge"] + " " if t["merge"] else "")
                + "The notice shows no building design: the whole lot is drawn as an envelope.")
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": f"{lot} office building (envelope)", "stage": "entitlement",
                "height_ft": t["ft"], "podium_ft": None, "base_ft": 0,
                "use": f"Office ({t['sqft']} sq ft)", "phase": None, "illustrative": True,
                "source": (f"illustrative: {lot} (Santa Clara County parcels {apn_text}, named in the revised notice of "
                           f"preparation and placed by its Figure 4, PDF p. 8) at the {t['ft']} ft in its Table 4.0-1 "
                           "(PDF p. 9)"),
                "note": note,
            },
            "geometry": geometry,
        })
        fp = geom.area * SQFT
        print(f"[santana-row] {lot}: {fp:,.0f} sq ft lot, {t['ft']} ft; {t['sqft']} sq ft of office would be "
              f"{int(t['sqft'].replace(',', '')) / fp:.1f} times the lot area")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the four lots where the plan would add office buildings, each drawn as a "
                        "whole-lot envelope at the height the notice of preparation gives it: Lot 1A/B/C at Stevens "
                        "Creek and Winchester boulevards (700,000 sq ft, 144 ft), Lot 2B on Stevens Creek Boulevard "
                        "(325,000 sq ft, 144 ft), Lot 10A on Olsen Drive (200,000 sq ft, 139 ft) and Lot 17 on Dudley "
                        "Avenue (275,000 sq ft, 162 ft). The buildings aren't designed yet; the existing Santana Row "
                        "buildings are left as they are."),
            "note": "Whole-lot envelopes at the stated heights, not building designs.",
            "sourceUrl": b.NOP["url"],
            "sourceLabel": "Santana Row Master Plan Update, revised notice of preparation, 2026 (PDF), Table 4.0-1",
            "lotsSourceUrl": b.AREA["landing"],
            "georeference": {
                "method": ("Lots are the Santa Clara County parcels for the APNs the notice names; Figure 4 (PDF p. 8), "
                           "fitted to the parcels in boundary_santana_row, puts each lot's label inside them."),
                "label_distance_to_lot_m": checks,
            },
            "license": ("Heights and floor areas: from a public City of San José document. Lots: Santa Clara County "
                        "open data (terms of use)."),
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    bad = [f["properties"]["label"] for f in json.loads(out.read_text())["features"] if not shape(f["geometry"]).is_valid]
    if bad:
        raise SystemExit(f"santana-row: invalid geometry written for {bad}")
    print(f"[santana-row] wrote {out.relative_to(config.ROOT)} ({len(features)} features, {out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
