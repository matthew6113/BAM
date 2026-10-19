"""Matson Block (77 Beale Street): the new tower's maximum envelope, one of three positions the EIR will study.

Source:
- Notice of Preparation of an EIR, Matson Block Project (SF Planning, case 2021-012562ENV, Dec 17, 2025; CEQAnet
  SCH 2025120794), attachment "2021-012562ENV-NOA-NOP-OCR":
  - PDF p. 14: "The office tower would be located in the “Tower Location Zone” shown in Figure 4, which is a
    229-foot by 275-foot area located in the southern portion of the site. However, the exact tower location has
    not yet been determined and the final tower location could be oriented toward Main Street, Mission Street, or
    Beale Street."
  - Figure 4 "Proposed Site Plan" (PDF p. 17): the Tower Location Zone runs the full width of the block between Main
    and Beale streets along Mission Street.
  - Figure 6 "Proposed Massing Scenarios" (PDF p. 23): plans of the tower "justified on" Mission, Main or Beale
    Street, and the maximum dimensions of the massing "justified on Mission Street": base 275'-6" by 229'-3" up to
    125 ft; lower tower 230'-0" by 135'-0" up to 679 ft; upper tower 210'-0" by 135'-0" up to 1,225 ft. Note on the
    figure: "Illustrative diagram to show maximum massing for CEQA analysis purposes only. Not representative of
    actual design."
  - PDF pp. 2 and 9: the tower is "up to 1,225-foot-tall ... with a 75-foot-tall architectural crown".

How it's drawn:
- The block (DataSF parcels, the boundary file) gives the frame: the Mission / Beale corner, with one axis along
  Mission Street toward Main Street and one along Beale Street toward Market Street.
- The "justified on Mission Street" scenario, the one Figure 6 draws in three dimensions: the base fills the Tower
  Location Zone (the block's width by 229'-3" from the Mission Street line) to 125 ft; the lower tower (230 ft
  along Mission Street, 135 ft deep from it) to 679 ft; the upper tower (210 by 135 ft) to 1,225 ft. The towers are
  centred between Beale and Main streets, as the figure's plan shows them. These are the maximum envelopes the EIR
  will study, not a design; the final position (against Mission, Main or Beale Street) and shape are to be set by
  design guidelines. The crown, the 25 Beale Street conversion and the optional 400-ft variant building are not
  drawn. Illustrative.

Stage: in environmental review (notice of preparation, Dec 2025; no Draft EIR yet). Drawn at the project's stage,
"entitlement".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_77_beale
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "77-beale"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639

NOP = {
    "title": "Notice of Preparation of an EIR, Matson Block Project (case 2021-012562ENV, Dec 17, 2025)",
    "url": "https://ceqanet.lci.ca.gov/2025120794/Attachment/gufVD2",
    "sha256": "2f97a97f54b78e0cf2eabcdd1810e3bea161007f2c663a5262724e633b162809",
    "file": "2021-012562ENV-NOA-NOP-OCR.pdf",
}

ZONE_DEPTH_FT = 229 + 3 / 12  # Figure 6: base 275'-6" x 229'-3"; p. 14: "229-foot by 275-foot area"
LOWER = {"along": 230.0, "deep": 135.0, "top": 679.0}
UPPER = {"along": 210.0, "deep": 135.0, "top": 1225.0}
BASE_TOP_FT = 125.0


def block_utm() -> Polygon:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    g = shapely.union_all(ob._utm_shapes(fc).buffer(0.5).to_numpy()).buffer(-0.5)
    return g if g.geom_type == "Polygon" else max(g.geoms, key=lambda p: p.area)


def frame(block: Polygon) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """The Mission / Beale corner, a unit vector along Mission toward Main and one along Beale toward Market."""
    xy = np.array(block.simplify(0.5).exterior.coords)[:-1]
    i = int(np.argmin(xy[:, 1]))  # southernmost corner: Mission and Beale
    corner = xy[i]
    edges = [xy[(i + 1) % len(xy)] - corner, xy[i - 1] - corner]
    along = max(edges, key=lambda v: v[0])  # Mission Street, north-east toward Main
    inward = min(edges, key=lambda v: v[0])  # Beale Street, north-west toward Market
    check = {
        "mission_frontage_ft": round(float(np.linalg.norm(along)) / FT, 1),
        "beale_frontage_ft": round(float(np.linalg.norm(inward)) / FT, 1),
        "corner_angle_deg": round(float(np.degrees(np.arccos(along @ inward / np.linalg.norm(along) / np.linalg.norm(inward)))), 2),
    }
    return corner, along / np.linalg.norm(along), inward / np.linalg.norm(inward), check


def main() -> None:
    # The figures this module transcribes, pinned (about 1.5 MB).
    trace.fetch_document(NOP["url"], config.ROOT / "data" / "raw" / "docs" / NOP["file"], NOP["sha256"])
    block = block_utm()
    corner, along, inward, check = frame(block)
    width_ft = check["mission_frontage_ft"]
    print(f"[77-beale] block {block.area * SQFT:,.0f} sq ft (NOP 151,390); Mission {width_ft} ft, Beale "
          f"{check['beale_frontage_ft']} ft; corner {check['corner_angle_deg']} deg")

    def at(a: float, d: float) -> np.ndarray:
        return corner + along * a * FT + inward * d * FT

    def rect(a0: float, a1: float, d0: float, d1: float) -> Polygon:
        return Polygon([at(a0, d0), at(a1, d0), at(a1, d1), at(a0, d1)])

    zone = rect(0, width_ft, 0, ZONE_DEPTH_FT).intersection(block)
    mid = width_ft / 2
    lower = rect(mid - LOWER["along"] / 2, mid + LOWER["along"] / 2, 0, LOWER["deep"])
    upper = rect(mid - UPPER["along"] / 2, mid + UPPER["along"] / 2, 0, UPPER["deep"])
    if not (upper.within(lower.buffer(0.01)) and lower.within(zone.buffer(0.05))):
        raise SystemExit("77 Beale: the tower envelopes don't nest inside the Tower Location Zone")

    fig6 = f"{NOP['title']}, Figure 6 (PDF p. 23)"
    parts = [
        ("Tower base (maximum envelope)", zone.difference(lower), BASE_TOP_FT,
         "Office, retail and lobbies (program not yet set)",
         f"illustrative: the Tower Location Zone (the block's width by 229 ft 3 in from Mission Street) in the {NOP['title']}, "
         f"Figure 4 (PDF p. 17), at the 125-ft maximum base height in {fig6}",
         "The largest base the EIR will study (275 ft 6 in by 229 ft 3 in, up to 125 ft), not a design."),
        ("Lower tower (maximum envelope)", lower.difference(upper), LOWER["top"],
         "Office, possibly with institutional, hotel or residential floors",
         f"illustrative: 230 by 135 ft, against Mission Street and centred between Beale and Main streets, up to "
         f"679 ft, from {fig6} (“justified on Mission Street”)",
         "The widest the tower's lower floors could be (230 by 135 ft), to 679 ft."),
        ("Upper tower (maximum envelope)", upper, UPPER["top"],
         "Office, possibly with institutional, hotel or residential floors and an observation deck near the top",
         f"illustrative: 210 by 135 ft, against Mission Street and centred between Beale and Main streets, up to "
         f"1,225 ft, from {fig6} (“justified on Mission Street”)",
         "Up to 1,225 ft, with an architectural crown of up to 75 ft (Notice of Preparation). The EIR will study "
         "the tower against Mission, Main or Beale Street; its final position and shape aren't set."),
    ]
    features = []
    for label, geom, h, use, source, note in parts:
        wgs = gpd.GeoSeries([geom.simplify(0.05)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitlement", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })
        print(f"[77-beale] {label}: {geom.area * SQFT:,.0f} sq ft, {h:.0f} ft")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the maximum envelope the EIR will study for the new tower, in one of its "
                        "three positions (against Mission Street, the one the Notice of Preparation draws in 3D): a "
                        "base up to 125 ft over the Tower Location Zone, a lower tower of 230 by 135 ft to 679 ft and "
                        "an upper tower of 210 by 135 ft to 1,225 ft. The tower could instead stand against Main or "
                        "Beale Street; its design isn't set. The historic Matson and PG&E buildings and 25 Beale "
                        "Street are kept and not drawn."),
            "note": "Maximum envelopes for environmental review, not a design.",
            "sourceUrl": NOP["url"],
            "sourceLabel": "Notice of Preparation, 2025 (PDF)",
            "georeference": {
                "method": ("Figure dimensions laid out from the Mission Street / Beale Street corner of the DataSF "
                           "parcels, along Mission and Beale streets; towers centred between Beale and Main."),
                "frontages_as_mapped": check,
            },
            "license": "Dimensions: from a public SF Planning document. Block: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[77-beale] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
