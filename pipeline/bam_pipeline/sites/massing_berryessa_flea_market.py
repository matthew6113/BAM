"""Berryessa Flea Market South: height zones from the Berryessa BART Urban Village Plan.

Source:
- The Flea Market Southside Planned Development zoning (PDC17-051, Ordinance 30646, approved
  June 29, 2021) sets no heights of its own. Its development standards say "Building heights
  shall be consistent with the height limits described in the Urban Design chapter of the
  Berryessa BART Urban Village Plan, as may be amended" (Exhibit B; Attachment 4 of Council
  file 21-1627).
- The plan's own document sits on sanjoseca.gov, which this pipeline can't reach. The same
  diagram is reproduced as "Figure 1: BBUV Plan Height Limit Diagram" in the Planning
  Commission supplemental staff report for GP20-008 and C21-001 (May 5, 2021), p. 12 of 20
  (PDF page 19), which is Attachment 1 of the Council's BBUV Plan adoption item (file 21-1626,
  June 22-29, 2021). Legend: up to 40, 70, 90, 160 and 270 ft; dashed circles mark "Towers"
  as key visual locations.
- The Council adopted the plan on June 29, 2021 with the Planning Commission's changes, which
  were redlines to the Land Use and Open Space chapters to allow the 5-acre Urban Market on
  the BART Plaza and Central Open Space (Council memo, May 28, 2021). Nothing in that item
  changed the height diagram. The Council staff report for 1655 Berryessa Road (file 25-804,
  July 21, 2025) still quotes the plan's 90 and 160 ft limits north of Berryessa Road, which
  match this figure.

What this is and isn't:
- Each coloured development area in the figure is drawn to its height limit, not as a
  building design: illustrative. Towers occupy only part of the 270-ft areas.
- The plan's development areas are conceptual (the rezoning fixes acreages, not block lines),
  so the shapes follow the plan's diagram, not a site plan.
- Riparian corridor and public open space (green in the figure), including the BART Plaza and
  Central Open Space that hold the 5-acre Urban Market, have no height and are left out. So
  are the streets. Areas outside the PDC17-051 zoning (north of Berryessa Road, east of the
  BART tracks) are clipped off.
- Nothing has been built or permitted: the owner withdrew its permit and map applications
  in 2023. The flea market's own sheds are not drawn.

Georeferencing: the figure is an embedded 974 x 881 JPEG. The centrelines of its white
streets and of the grey BART trackway are fitted to OpenStreetMap roads and the BART line
(via Overture) by trimmed ICP, started from Mabury Road at the BART line and the figure's
scale bar. The fitted scale is checked against the scale bar.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_berryessa_flea_market
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

PROJECT_ID = "berryessa-flea-market"
UTM = tb.UTM
FT = 0.3048

REPORT = {
    "title": ("Planning Commission supplemental staff report, File Nos. GP20-008 and C21-001 "
              "(Berryessa BART Urban Village Plan), May 5, 2021"),
    "url": "https://legistar.granicus.com/sanjose/attachments/afe4bc58-e013-42b2-870b-ccdbfd873751.pdf",
    # Council file 21-1626 (BBUV Plan adoption), which lists the report as Attachment 1.
    "file_url": "https://sanjose.legistar.com/LegislationDetail.aspx?ID=9320&GUID=52462B47-4D5A-4FEE-9F38-A2588DDC1C50",
    "sha256": "e4a894921ae55938f462bbdcf4106814dac97f53b1fea82bf55d347089862e59",
    "file": "bfm-bbuv-pc-supplemental-2021-05-05.pdf",
}
FIG = {"page_index": 18, "printed_page": "12 of 20", "figure": "Figure 1: BBUV Plan Height Limit Diagram"}
IMAGE_SIZE = (881, 974)  # rows, columns of the embedded raster

# Legend swatches (RGB sampled from the figure's legend; the map fills match within ~10).
LEGEND = {40: (241, 131, 106), 70: (107, 206, 243), 90: (31, 114, 189), 160: (106, 47, 143), 270: (147, 40, 140)}
MAX_DIST = 45
CLOSE_PX = 5

# ICP start: Mabury Road crossing the BART trackway (pixel), and the scale bar
# (0 at x = 722 px, 1,200 ft at x = 945 px, measured on the raster).
START_PX = (633, 818)
SCALE_BAR_PX = (722, 945)
SCALE_BAR_FT = 1200
ICP_KEEP = 0.5
# Legend, scale bar and north arrow: no streets there.
MASK_OUT = [(0, 740, 200, 881), (690, 820, 974, 881)]
WALKWAYS = ["footway", "path", "cycleway", "steps", "pedestrian", "track", "bridleway"]

MIN_AREA_M2 = 150  # drop specks from anti-aliased edges


def _image(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    imgs = [o for o in page.get_objects() if o.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE]
    if len(imgs) != 1:
        raise SystemExit(f"expected one image on the Figure 1 page, found {len(imgs)}")
    rgb = np.asarray(imgs[0].get_bitmap(render=False).to_pil().convert("RGB"))
    if rgb.shape[:2] != IMAGE_SIZE:
        raise SystemExit(f"unexpected Figure 1 raster size {rgb.shape}")
    return rgb


def _ridges(mask: np.ndarray, min_half_width: float) -> np.ndarray:
    """Centre-line pixels of a mask: local maxima of the distance transform."""
    dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 3)
    ridge = (dt >= min_half_width) & (dt >= cv2.dilate(dt, np.ones((3, 3), np.uint8)))
    y, x = np.nonzero(ridge)
    return np.c_[x, y].astype(float) + 0.5


def georeference(rgb: np.ndarray, streets: gpd.GeoDataFrame) -> tuple[trace.Similarity, dict]:
    a = rgb.astype(int)
    white = a.min(axis=2) >= 249
    grey = ((np.abs(a[:, :, 0] - a[:, :, 1]) < 6) & (np.abs(a[:, :, 1] - a[:, :, 2]) < 6)
            & (a[:, :, 0] > 85) & (a[:, :, 0] < 130))
    for x0, y0, x1, y1 in MASK_OUT:
        white[y0:y1, x0:x1] = False
        grey[y0:y1, x0:x1] = False
    road_px, track_px = _ridges(white, 2.0), _ridges(grey, 2.5)
    points = np.vstack([road_px, track_px])
    groups = np.r_[np.zeros(len(road_px), int), np.ones(len(track_px), int)]

    roads = streets[(streets["subtype"] == "road") & ~streets["class"].isin(WALKWAYS)]
    bart = streets[(streets["subtype"] == "rail") & streets["name"].fillna("").str.startswith("BART")]
    road_lines = shapely.union_all(roads.geometry.to_numpy())
    bart_line = shapely.union_all(bart.geometry.to_numpy())
    mabury = shapely.union_all(roads[roads["name"] == "Mabury Road"].geometry.to_numpy())
    cross = shapely.get_coordinates(mabury.intersection(bart_line))
    if not len(cross):
        raise SystemExit("Mabury Road and the BART line do not cross in OpenStreetMap")
    anchor = cross.mean(axis=0)
    bar_m_per_px = SCALE_BAR_FT * FT / (SCALE_BAR_PX[1] - SCALE_BAR_PX[0])
    u = np.array(START_PX, float)
    init = trace.fit_similarity(np.array([u, u + [100, 0], u + [0, -100]]),
                                np.array([anchor, anchor + [100 * bar_m_per_px, 0], anchor + [0, 100 * bar_m_per_px]]))
    sim, d = tb.icp(points, [road_lines, bart_line], groups, init, ICP_KEEP)
    rep = tb.icp_report(sim, d, ICP_KEEP, "street and BART trackway centrelines")
    rep["track_median_m"] = round(float(np.median(d[groups == 1])), 2)
    rep["scale_bar_m_per_px"] = round(bar_m_per_px, 4)
    rep["scale_vs_bar"] = f"{(sim.scale / bar_m_per_px - 1) * 100:+.1f}%"
    return sim, rep


def trace_zones(rgb: np.ndarray) -> list[tuple[int, Polygon]]:
    """Height areas: pixels nearest each legend colour; a closing fills the dashed tower circles."""
    cols = np.array(list(LEGEND.values()), float)
    heights = list(LEGEND)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None], axis=3)
    label = np.where(dist.min(axis=2) <= MAX_DIST, dist.argmin(axis=2), -1)
    for x0, y0, x1, y1 in MASK_OUT[:1]:
        label[y0:y1, x0:x1] = -1
    zones = []
    for i, h in enumerate(heights):
        m = (label == i).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        # The dashed tower circles and text are a few pixels thick; streets are 8 px or more.
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((CLOSE_PX, CLOSE_PX), np.uint8))
        m = cv2.medianBlur(m * 255, 5)  # smooth JPEG-ragged edges
        contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in contours:
            if cv2.contourArea(c) < 40:
                continue
            p = shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5)).buffer(0.5, join_style="mitre")
            zones.append((h, p))
    return zones


def main() -> None:
    pdf_path = trace.fetch_document(REPORT["url"], tb.DOCS / REPORT["file"], REPORT["sha256"])
    rgb = _image(pdf_path)
    streets = tb.streets("bfm-berryessa", (-121.892, 37.356, -121.860, 37.382))
    sim, georef = georeference(rgb, streets)
    print(f"[berryessa] Figure 1 georeference: trimmed RMS {sim.rms_m:.2f} m, scale {sim.scale:.4f} m/px "
          f"({georef['scale_vs_bar']} vs the scale bar), rotation {np.degrees(sim.rotation):.2f} deg")

    site = shape(json.loads((config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(UTM).iloc[0]

    zones = []
    for h, px in trace_zones(rgb):
        g = shapely.make_valid(sim.geometry(px)).intersection(site_utm)
        g = shapely.make_valid(g.simplify(0.4))
        parts = [p for p in getattr(g, "geoms", [g]) if isinstance(p, Polygon) and p.area >= MIN_AREA_M2]
        for p in parts:
            zones.append({"height_ft": h, "utm": p})
    # Number the areas north to south.
    zones.sort(key=lambda z: (-round(z["utm"].centroid.y, -1), z["utm"].centroid.x))
    fig = f"{REPORT['title']}, {FIG['figure']}, p. {FIG['printed_page']} ({REPORT['url']})"
    features = []
    total = {}
    for n, z in enumerate(zones, 1):
        h = z["height_ft"]
        total[h] = total.get(h, 0) + z["utm"].area / tb.ACRE_M2
        print(f"[berryessa]   area {n:>2}: up to {h:>3} ft, {z['utm'].area / tb.ACRE_M2:5.2f} ac")
        props = {
            "kind": "block",
            "block": str(n),
            "label": f"Development area {n}, up to {h} ft",
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the {h}-ft height limit traced from {fig}",
            "note": "Height limit of the Berryessa BART Urban Village Plan, which the PD zoning (PDC17-051) adopts; "
                    "drawn as an envelope, not a building design.",
        }
        if h == 270:
            props["note"] += " The plan marks tower locations in these areas; towers would cover only part of them."
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(z["utm"]))})
    print("[berryessa] acres by height: " + ", ".join(f"{h} ft {a:.1f}" for h, a in sorted(total.items())))

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each development area is drawn to its height limit in the Berryessa BART "
                "Urban Village Plan's height diagram (90, 160 and 270 ft), which the 2021 Planned Development zoning "
                "adopts, not as a building design. The plan's areas are conceptual, and towers would rise on only "
                "part of the 270-ft areas. The creek corridors, parks and plazas, including the 5-acre urban market, "
                "and the streets are not drawn; nothing has been built or permitted."
            ),
            "note": ("Development areas are drawn to the urban village plan's height limits, not as building designs; "
                     "no development application is on file."),
            "sourceUrl": REPORT["file_url"],
            "sourceLabel": "Urban village plan height diagram, 2021",
            "georeference": {"figure_1": georef},
            "license": "Height areas: traced from a public City of San José document. "
                       "Georeference: " + tb.OSM_LICENSE + ".",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[berryessa] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
