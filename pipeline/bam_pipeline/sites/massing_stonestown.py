"""Stonestown: parcel height limits, traced from the adopted Design Standards and Guidelines.

Source:
- Stonestown Design Standards and Guidelines (DSG), April 2024 (file dated 2024-04-23), the
  "master plan document" SF Planning lists under "Adopted Stonestown Development Project
  Documents" (Planning case 2021-012028; adopted with the 2024 approvals). Figure 5.9,
  "Maximum building heights", printed p. 187 (PDF page 208). Standard S5.3.1: "New
  construction shall not exceed maximum heights as established by Figure 5.9."
- The same plan, in black and white, is Figure 249.9-5 "Stonestown Building Heights Maximum"
  of the Special Use District (Planning Code Sec. 249.9, Ordinance 204-24, p. 28). The SUD
  defines "Tower" as "all New Construction above 90 feet in height" and limits it to an
  average floorplate of 12,500 sq ft above 90 ft (Sec. 249.9(g)), which is why the 150- and
  190-ft zones are drawn as tower zones over a 90-ft base.

What this is and isn't:
- Each parcel is drawn to its height limit, not as a building design; real buildings will be
  smaller, and towers occupy only part of a tower zone. So the massing is labelled illustrative.
- The figure shows the project with the Variant Sub-Area (Parcel E3E, up to 3,491 homes); the
  inset for the project without it (Parcel E3) is not drawn.
- The hatched "90-foot flex zone" next to Parcel NW2 is an alternative place for the NW2
  building (S5.2.2, S5.3.1), so it is outlined only (no height).
- The white "15-foot maximum height subject to S2.1.2" areas are project open spaces, not
  development parcels, and are left out. So are Figure 5.7's open spaces inside parcels.
- The existing mall (710,000 sq ft, staying) is outside the Special Use District. No new
  building has been built or permitted, so no built footprints are drawn.

Georeferencing: the map in Figure 5.9 is an embedded 1800 x 1839 raster. Street centrelines
(midway between the curb lines drawn in the base map) at six intersections are matched to
OpenStreetMap (via Overture) with a least-squares similarity fit; residuals are recorded.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_stonestown
"""

from __future__ import annotations

import json

import cv2
import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "stonestown"
UTM = tb.UTM

DSG = {
    "title": "Stonestown Design Standards and Guidelines (April 2024; Planning case 2021-012028)",
    # SF Planning's project page links this M-Files share; the REST URL below is its download.
    "page_url": "https://citypln-m-extnl.sfgov.org/SharedLinks.aspx?accesskey=ad1e00d6088f207fc57af21017ef4288f33d767889f220aee642919f2961c494&VaultGUID=A4A7DACD-B0DC-4322-BD29-F6F07103C6E0",
    "url": "https://citypln-m-extnl.sfgov.org/REST/sharedlinks/%7ba4a7dacd-b0dc-4322-bd29-f6f07103c6e0%7d/"
           "ad1e00d6088f207fc57af21017ef4288f33d767889f220aee642919f2961c494/content",
    "sha256": "9231c9ef3a86e5e66996a7f3bb81c8109ec6487c902bb957a4b791c4b31cb86d",
    "file": "stonestown-dsg-20240423.pdf",
}
FIG_5_9 = {"page_index": 207, "printed_page": "187", "figure": "Figure 5.9, Maximum building heights"}
SUD_ORD = "Ordinance 204-24 (Planning Code Sec. 249.9), Figure 249.9-5 and Sec. 249.9(g)"
IMAGE_SIZE = (1839, 1800)  # rows, columns of the embedded map raster

# Street centrelines in the raster (pixels), each midway between the curb lines drawn either
# side, matched to the OpenStreetMap crossing nearest the rough UTM position given.
CONTROLS = {
    ("20th Avenue", "Eucalyptus Drive"): ((1188, 77), (546178, 4176110)),
    ("21st Avenue", "Eucalyptus Drive"): ((976, 81), (546097, 4176112)),
    ("20th Avenue", "Buckingham Way"): ((1199, 366), (546176, 4176003)),
    ("20th Avenue", "Winston Drive"): ((1225, 1283), (546170, 4175651)),
    ("19th Avenue", "Eucalyptus Drive"): ((1438, 70), (546272, 4176109)),
    ("19th Avenue", "Winston Drive"): ((1482, 1283), (546268, 4175647)),
}

# Legend fills (the PDF's vector legend swatches, RGB 0-255; the raster matches within 2).
LEGEND = {30: (212, 194, 222), 40: (155, 110, 175), 50: (91, 59, 110), 90: (190, 236, 237),
          150: (245, 211, 213), 190: (238, 156, 196)}
TOWER_BASE_FT = 90  # SUD Sec. 249.9: "Tower" means all new construction above 90 ft

# One point inside each parcel's fill (raster pixels). The parcel is the region enclosed by
# the figure's black parcel lines that holds the point.
PARCELS = {
    "NW1": [(250, 550)], "NW2": [(470, 520)], "NW3": [(480, 330)], "NW2 flex zone": [(530, 470)],
    "W1": [(700, 500)], "W2": [(920, 520)], "W3/4": [(780, 820), (810, 1150)],
    "E1": [(1330, 500)], "E2": [(1135, 900)], "E3E": [(1330, 880)], "E4": [(1330, 1130)],
    "E5": [(1100, 480)], "E6": [(1130, 1230)],
    "S1": [(1100, 1600)], "S2": [(1340, 1500)], "S3": [(680, 1450)],
}
FLEX = "NW2 flex zone"
LINE_HALF_PX = 2  # parcel lines are about 4 px wide; regions grow to the line centre


def _image(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG_5_9["page_index"]]
    imgs = [o for o in page.get_objects() if o.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE]
    if len(imgs) != 1:
        raise SystemExit(f"expected one image on the Figure 5.9 page, found {len(imgs)}")
    rgb = np.asarray(imgs[0].get_bitmap(render=False).to_pil().convert("RGB"))
    if rgb.shape[:2] != IMAGE_SIZE:
        raise SystemExit(f"unexpected Figure 5.9 raster size {rgb.shape}")
    return rgb


def georeference(streets: gpd.GeoDataFrame) -> trace.Similarity:
    src, dst, labels = [], [], []
    for (a, b), (px, guess) in CONTROLS.items():
        la = shapely.union_all(streets[streets["name"] == a].geometry.to_numpy())
        lb = shapely.union_all(streets[streets["name"] == b].geometry.to_numpy())
        pts = shapely.get_coordinates(la.intersection(lb))
        near = pts[np.linalg.norm(pts - guess, axis=1) < 40] if len(pts) else pts
        if not len(near):
            raise SystemExit(f"{a} and {b} do not cross near {guess} in OpenStreetMap")
        src.append(px)
        dst.append(near.mean(axis=0))  # divided roads cross more than once; use the middle
        labels.append(f"{a} / {b}")
    return trace.fit_similarity(src, dst, labels)


def trace_parcels(rgb: np.ndarray) -> list[dict]:
    """Height zones per parcel: nearest legend colour inside each outlined parcel."""
    dark = (rgb.max(axis=2) < 70).astype(np.uint8)
    _, regions = cv2.connectedComponents(1 - dark, connectivity=4)
    palette = np.array(list(LEGEND.values()), float)
    heights = list(LEGEND)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - palette[None, None], axis=3)
    label = np.where(dist.min(axis=2) <= 18, dist.argmin(axis=2), -1)
    zones, taken = [], np.zeros(dark.shape, bool)
    grow = np.ones((2 * LINE_HALF_PX + 1, 2 * LINE_HALF_PX + 1), np.uint8)
    for name, points in PARCELS.items():
        ids = {int(regions[y, x]) for x, y in points}
        region = np.isin(regions, list(ids)).astype(np.uint8)
        if region.sum() > 120_000:
            raise SystemExit(f"parcel {name} is not closed in the figure ({region.sum()} px)")
        # Fill the holes text leaves, then grow to the middle of the parcel line.
        contours, _ = cv2.findContours(region * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mask = np.zeros_like(region)
        cv2.drawContours(mask, contours, -1, 1, cv2.FILLED)
        mask = (cv2.dilate(mask, grow) > 0) & ~taken
        taken |= mask
        if name == FLEX:
            zones.append({"block": name, "height_ft": None, "px": _polys(mask)})
            continue
        lab = np.where(mask, label, -1)
        seed = (lab >= 0).astype(np.uint8)
        seed = cv2.morphologyEx(seed, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        lab[seed == 0] = -1
        # Text, dashes and line pixels take the nearest fill's height.
        _, nearest = cv2.distanceTransformWithLabels((lab < 0).astype(np.uint8), cv2.DIST_L2, 5,
                                                     labelType=cv2.DIST_LABEL_PIXEL)
        seeds = np.flatnonzero(lab.ravel() >= 0)
        filled = lab.ravel()[seeds][nearest.ravel() - 1].reshape(lab.shape)
        for i in np.unique(filled[mask]):
            part = (filled == i) & mask
            part = cv2.morphologyEx(part.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
            geom = _polys(part)
            if not geom.is_empty and geom.area >= 400:
                zones.append({"block": name, "height_ft": heights[i], "px": geom})
    return zones


def _polys(mask: np.ndarray):
    contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    polys = [shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5)) for c in contours if cv2.contourArea(c) >= 200]
    if not polys:
        return Polygon()
    # Dashed lines split a zone into touching pieces; join them again.
    return shapely.union_all(polys).buffer(1.5, join_style="mitre").buffer(-1.5, join_style="mitre")


def main() -> None:
    pdf_path = trace.fetch_document(DSG["url"], tb.DOCS / DSG["file"], DSG["sha256"])
    rgb = _image(pdf_path)
    streets = tb.streets("stonestown", (-122.4850, 37.7240, -122.4710, 37.7340))
    streets = streets[streets["subtype"] == "road"]
    sim = georeference(streets)
    print(f"[stonestown] Figure 5.9 georeference: RMS {sim.rms_m:.2f} m over {len(sim.labels)} intersections, "
          f"scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f} deg")

    zones = trace_parcels(rgb)
    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]
    for z in zones:
        z["utm"] = trace.as_multipolygon(shapely.make_valid(sim.geometry(z["px"]).simplify(0.4)))
        inside = z["utm"].intersection(site_utm).area / z["utm"].area
        print(f"[stonestown]   {z['block']:>14}: {str(z['height_ft']):>4} ft, {z['utm'].area / tb.ACRE_M2:5.2f} ac, "
              f"{inside:.0%} inside the SUD")

    fig = f"{DSG['title']}, {FIG_5_9['figure']}, p. {FIG_5_9['printed_page']}"
    order = list(PARCELS)
    features = []
    for z in sorted(zones, key=lambda z: (order.index(z["block"]), z["height_ft"] or 0)):
        h = z["height_ft"]
        base = TOWER_BASE_FT if h and h > TOWER_BASE_FT else None
        flex = z["block"] == FLEX
        props = {
            "kind": "block",
            "block": "NW2" if flex else z["block"],
            "label": "Parcel NW2 flex zone" if flex else f"Parcel {z['block']}",
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": base,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": (f"illustrative: outlined from {fig} (90-foot flex zone)" if flex else
                       f"illustrative: drawn to the {h}-ft height limit traced from {fig}"
                       + (f"; tower zone over a {base}-ft base ({SUD_ORD}: towers are new construction above "
                          f"90 ft, with an average floorplate of at most 12,500 sq ft)" if base else "")),
        }
        if flex:
            props["note"] = ("Outlined only: an alternative location for the Parcel NW2 building, up to 90 ft "
                             "(DSG S5.2.2 and S5.3.1).")
        elif z["block"] == "E3E":
            props["note"] = "Drawn with the Variant Sub-Area (Parcel E3E), as in the figure."
        features.append({"type": "Feature", "properties": props,
                         "geometry": mapping(tb.to_wgs(z["utm"]))})

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each new-construction parcel is drawn to its height limit in the adopted "
                "Stonestown Design Standards and Guidelines (April 2024, Fig. 5.9), from 30 to 190 ft, not as a "
                "building design. Towers may rise above 90 ft on only part of each 150- and 190-ft zone. The project "
                "open spaces, the NW2 flex zone's height and the existing mall, which stays, are not drawn as massing; "
                "no new building has been built yet."
            ),
            "note": ("Parcels are drawn to their height limits in the 2024 Design Standards and Guidelines, not as "
                     "building designs; real buildings will be smaller."),
            "sourceUrl": DSG["page_url"],
            "sourceLabel": "Design standards and guidelines, 2024 (PDF)",
            "georeference": {"figure_5_9": sim.report()},
            "license": "Parcel shapes: traced from a public SF Planning document. "
                       "Georeference: " + tb.OSM_LICENSE + ".",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[stonestown] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
