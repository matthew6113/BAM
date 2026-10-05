"""Brooklyn Basin (Oak to Ninth): the built parcels' buildings and the unbuilt parcels' height envelopes.

Sources (all City of Oakland, via the City Council's Legistar attachment store):
- Height limits: Oakland Planning Code Chapter 17.101B (D-OTN Oak to Ninth District Zone), Sec.
  17.101B.130, as restated by the clerical update adopted as Ordinance 13826 (2024; Exhibit A, PDF p. 4):
  "Height limits throughout the project area range from eighty-six (86) feet to two hundred forty (240)
  feet. The height of mid-rise structures on designated parcels can increase up to one hundred and
  twenty (120) feet; however, the heights of the 240-foot towers cannot be increased."
- Tower zones: Oak to 9th Brooklyn Basin Design Guidelines (November 2006, revised September 2014),
  the "Tower zone" diagram on printed p. 14 (PDF p. 18) and the text on printed p. 15 ("Buildings above
  120 feet and up to 240 feet in height are limited to particular tower zones (see diagram) ... Within
  each of these zones, one tower will be permitted"; "Apart from the tower zones, the predominant
  building height ... is 86 feet"). The guidelines are Attachment D2b to the City Council's May 2023
  approvals (Legistar file 23-0206).
- Which tower zones still stand: the Planning Commission staff report of January 11, 2023 (Attachment 7
  to file 23-0206): "Parcels H, J, and A are fully entitled without tower components", and the revised
  Preliminary Development Plan (Resolution 89709, May 2, 2023) allows "up to two towers, rather than a
  single tower, on Parcel M (but not increase the total number of towers allowed)".
- Parcel shapes: City of Oakland parcels (Oakland_Parcels_Public, from the Alameda County Assessor),
  matched to the development parcels by the Assessor's parcel numbers in the 2025 Planning Commission
  staff report for Parcel H (018-0465-017), by the completed buildings on them, and by their fills on
  sheet 1.4 (below). Parcels K
  and L share one Assessor's parcel; they are split along Harbor Lane West as drawn on the revised
  Preliminary Development Plan, sheet 1.4 "Development Program and Parcelization Plan" (April 2022
  revision, Attachment A1 to file 23-0206, PDF p. 6). Sheet 1.4 is georeferenced by a least-squares
  similarity between its parcel fills and the same parcels in the city's parcel layer.
- Built parcels: the City of Oakland's Official Statement for the CFD No. 2023-1 special tax bonds
  (Attachment A to file 25-0862, July 2025), Table 2 (p. 28) names each completed building and its
  parcel, and pp. 40-41 give the stories of Caspian (Parcel G, "seven-story") and Portico (Parcel J,
  "eight-story"). Footprints are OpenStreetMap buildings via Overture. No official story count was
  found for Parcels A, B, C and F, so their stories are OpenStreetMap's building:levels, said plainly.
  Heights are estimated from stories (labelled illustrative): about 11 ft a floor, the floor-to-floor
  height of the Preliminary Development Plan's illustrative building sections (sheet 5.3, PDF p. 34,
  levels at +19, +31, +42, +53, +64, +75, +86 ft), capped at the 86-ft mid-rise limit.

What this is and isn't:
- Unbuilt parcels (D, E, H, K, L, M) are drawn to the 86-ft limit, not as building designs, so they are
  labelled illustrative. The tower zones still entitled (K, and H, whose March 2025 Final Development
  Permit option 2 has a 23-story tower) are drawn to 240 ft over an 86-ft base.
- Parcel M may hold up to two towers (2023), but no document found places them, so M is drawn at 86 ft
  with a note. The 120-ft allowance for parts of mid-rise buildings and the 55-ft step-downs along
  Clinton Basin and the mews (Design Guidelines pp. 15-17) are not drawn.
- Parks, streets, the marinas and the 9th Avenue Terminal are not massing. Older buildings still
  standing on Parcels K, L and M stay in the base map.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_brooklyn_basin
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "brooklyn-basin"
UTM = tb.UTM
FT = 0.3048
DOCS = config.ROOT / "data" / "raw" / "docs"
CACHE = config.ROOT / "data" / "raw" / "massing"
BBOX = (-122.2660, 37.7830, -122.2480, 37.7930)  # lon/lat window around the site
L2 = "https://oakland.legistar1.com/oakland/attachments/"

PDP = {
    "title": "Brooklyn Basin - Oak to 9th Development Plan, Preliminary Development Plan (revised December 2022; "
             "Attachment A1 to Legistar file 23-0206)",
    "url": L2 + "4dd4b2ec-e0e4-4e95-94b0-2dc59f109069.pdf",
    "file": "bb-34144-A1.pdf",
    "sha256": "7349215868d9d0bb67cce9e12c21166b3f1c88eb341940e6cef540f05e4c2805",
}
SHEET_1_4 = {"page_index": 5, "sheet": "sheet 1.4 \"Development Program and Parcelization Plan\" (April 2022 revision)",
             "pdf_page": 6, "dpi": 100}
DG = {
    "title": "Oak to 9th Brooklyn Basin Design Guidelines (November 2006, revised September 2014; "
             "Attachment D2b to Legistar file 23-0206)",
    "url": L2 + "1b34cc1f-3524-4e14-a367-8525418da155.pdf",
    "file": "bb-34144-D2b.pdf",
    "sha256": "0d6ea373c565ed5b509fed0e48c5a30bb91d01240f4a224b6fc8991cc1a1bd1f",
}
DG_FIG = {"page_index": 17, "printed_page": "14", "pdf_page": 18, "figure": "\"Tower zone\" diagram", "dpi": 150}
CODE = {
    "title": "Oakland Planning Code Chapter 17.101B (D-OTN), clerical update adopted by Ordinance 13826 (2024), "
             "Exhibit A, Sec. 17.101B.130",
    "url": L2 + "9a0331be-abd6-4cf1-b700-09bf1cba330c.pdf",
    "file": "bb-13826-exhibitA.pdf",
    "sha256": "aff7921c81afdf94ea00bfe433fe72d75ac00dc3302023ea3023431ae8905c91",
}
PC_2023 = {
    "title": "Planning Commission staff report, January 11, 2023 (Attachment 7 to Legistar file 23-0206)",
    "url": L2 + "2ce230bd-4a5f-48a0-be40-01f8cec5e05f.pdf",
    "file": "bb-34144-att7.pdf",
    "sha256": "93009e7b871905bb5e20b48949a9ea2e1cba263d814ba3674416d394b791c73a",
}
RES_89709 = {
    "title": "City Council Resolution 89709 (May 2, 2023), revising the Preliminary Development Plan",
    "url": L2 + "27a8c2de-28a3-4a7a-9b3f-9bf30fb51935.pdf",
    "file": "bb-89709-cms.pdf",
    "sha256": "e3a95a92d392a670b783c63ba8ba648400f8cc943f15c800931493696519ef25",
}
OS_2025 = {
    "title": "City of Oakland CFD No. 2023-1 Official Statement (Attachment A to Legistar file 25-0862, July 2025)",
    "url": L2 + "19a992d0-69e8-4aa1-ac01-8bacb3620c18.pdf",
    "file": "bb-25-0862-attA.pdf",
    "sha256": "7f750fc746ad9f0982ac2d24585f1a859f4d7d3e75de503ec48b7b5575c55827",
}
# Planning Commission records of 2025 (oaklandca.gov blocks scripts, so these are cited, not fetched).
PC_H_2025 = ("https://www.oaklandca.gov/files/assets/city/v/1/public-meetings/planning-commission/2025/"
             "item-2-staff-report-2-19-25-bb-parcel-h-option-2-case-file-pud06010-r02-pudf05-planning-commission-3.5.2025.pdf")
# Minutes of March 5, 2025 (adopted at the March 19, 2025 meeting, whose minutes record "Approval of Minutes
# Date: March 5, 2025 ... Action: 5 Ayes, 1 Abstained").
PC_MIN_0305 = ("https://www.oaklandca.gov/files/assets/city/v/1/public-meetings/planning-commission/2025/"
               "3.5.2025-pc-meeting-minutes-appr-via-catherine-3.12.2025.pdf")
PC_MIN_0319 = ("https://www.oaklandca.gov/files/assets/city/v/1/public-meetings/planning-commission/2025/"
               "3.19.2025-pc-meeting-minutes-appr-via-catherine-3.28.2025.pdf")

PARCELS = {
    "title": "City of Oakland parcels (Oakland_Parcels_Public; Alameda County Assessor, Oakland GIS)",
    "layer": "https://services.arcgis.com/9tC74aDHuml0x5Yz/arcgis/rest/services/Oakland_Parcels_Public/FeatureServer/0",
}
# Development parcel -> Assessor's parcel numbers (APN_GROUND without spaces).
APN = {
    "A": ["018046501200"],  # Foon Lok West and East
    "B": ["018046501900"],  # Orion
    "C": ["018046501400"],  # Artizan
    "D": ["018046501500"],
    "E": ["018046501600"],
    "F": ["018046500220", "018046500218"],  # Paseo Estero, Vista Estero
    "H": ["018046501700"],  # PC staff report, March 5, 2025
    "J": ["018046501800"],  # Portico
    "KL": ["018046000411"],
    "M": ["018043000114"],  # matched by its sheet 1.4 fill (the IoU check below)
}
# Centre of each parcel's label on sheet 1.4 at 100 dpi (pixels): a point inside its grey fill.
SHEET_LABELS = {"A": (2805, 700), "B": (2650, 780), "C": (2600, 980), "D": (2425, 1150), "E": (2330, 1250),
                "F": (2515, 700), "G": (2322, 790), "H": (2225, 1000), "J": (2115, 1200), "K": (1832, 870),
                "L": (1725, 1120), "M": (1418, 930)}
# Parcels whose sheet fill and Assessor's parcel are the same lot: the georeference controls.
SHEET_CONTROLS = ["A", "B", "C", "D", "E", "F", "H", "J", "M"]

# Design Guidelines tower-zone diagram at 150 dpi: street-centreline intersections (pixels) and their
# OpenStreetMap names (the plan's streets were built and named since; "8th Avenue" in OSM is the street
# the PDP calls 8th Avenue, and "9th Avenue" includes the loop along Parcel E).
DG_CONTROLS = {
    ("8th Avenue", "Brooklyn Basin Way"): (1131.7, 500.8),
    ("8th Avenue", "Clinton Lane"): (1234.2, 370.8),
    ("9th Avenue", "Clinton Lane"): (1315.8, 437.5),
    ("9th Avenue", "Brooklyn Basin Way"): (1212.5, 564.2),
    ("8th Avenue", "9th Avenue"): (1035.8, 635.0),
    ("Embarcadero", "5th Avenue"): (834.2, 365.0),
}
TOWER_ORANGE = (240, 105, 35)
TOWER_ZONES_KEPT = {"K", "H"}  # A and J are built without towers; see the module docstring

# Completed buildings: OSM way of the footprint, parcel, and stories with their source.
BUILT = [
    {"name": "Foon Lok West", "osm": "w944972671", "parcel": "A", "use": "Affordable housing", "phase": "Phase 1"},
    {"name": "Foon Lok East", "osm": "w1184511636", "parcel": "A", "use": "Affordable housing", "phase": "Phase 1"},
    {"name": "Orion", "osm": "w782291037", "parcel": "B", "use": "Residential", "phase": "Phase 1"},
    {"name": "Artizan", "osm": "w782291050", "parcel": "C", "use": "Residential", "phase": "Phase 1"},
    {"name": "Paseo Estero", "osm": "w782294676", "parcel": "F", "use": "Affordable housing", "phase": "Phase 1"},
    {"name": "Vista Estero", "osm": "w782294675", "parcel": "F", "use": "Affordable housing", "phase": "Phase 1"},
    {"name": "Caspian", "osm": "w1096126290", "parcel": "G", "use": "Residential, retail", "phase": "Phase 1",
     "stories": 7, "stories_src": "\"The seven-story building\" (p. 41)"},
    {"name": "Portico", "osm": "w1096126291", "parcel": "J", "use": "Residential, retail", "phase": "Phase 2",
     "stories": 8, "stories_src": "\"The eight-story building\" (p. 41)"},
]
FLOOR_FT = 11  # PDP sheet 5.3 sections: +19, +31, +42, +53, +64, +75, +86 ft
MIDRISE_FT = 86
TOWER_FT = 240

UNBUILT = {
    "D": {"phase": "Phase 2", "note": "Final Development Permit approved March 2021 (PC staff report, March 5, 2025, "
                                      "Table 1); its design isn't drawn. Planned for 243 homes (2025 Official Statement)."},
    "E": {"phase": "Phase 2", "note": "Final Development Permit approved October 2022 (PC staff report, March 5, 2025, "
                                      "Table 1); its design isn't drawn. Planned for 191 senior homes, \"Saltaire\" "
                                      "(2025 Official Statement)."},
    "H": {"phase": "Phase 2", "note": "The Planning Commission approved two Final Development Permit options on March 5, "
                                      "2025: a 5-story and a 7-story building, or a 5-story building (58 ft) and a "
                                      "23-story tower (235 ft) (staff report " + PC_H_2025 + "; minutes " + PC_MIN_0305 + ", "
                                      "adopted March 19, 2025, " + PC_MIN_0319 + "). The "
                                      "January 2023 staff report had H \"entitled without tower components\"; the newer "
                                      "approval is drawn, using the Design Guidelines' tower zone on H."},
    "K": {"phase": "Phase 3", "note": "One of the Design Guidelines' tower zones (240 ft) faces Clinton Basin. "
                                      "K and L are planned for 620 homes together (2025 Official Statement)."},
    "L": {"phase": "Phase 3", "note": "K and L are planned for 620 homes together (2025 Official Statement)."},
    "M": {"phase": "Phase 4", "note": "Up to two towers of up to 240 ft are allowed on Parcel M since May 2023 "
                                      "(Resolution 89709), but no adopted document places them, so they aren't drawn."},
}


def _docs() -> dict:
    return {d["file"]: trace.fetch_document(d["url"], DOCS / d["file"], d["sha256"])
            for d in (PDP, DG, CODE, PC_2023, RES_89709, OS_2025)}


def _check_text(paths: dict) -> None:
    """The facts this module relies on, checked against the documents' text."""
    import pdfplumber

    def text(doc, pages=None):
        with pdfplumber.open(paths[doc["file"]]) as pdf:
            sel = pdf.pages if pages is None else [pdf.pages[i] for i in pages]
            return " ".join(" ".join((p.extract_text() or "").split()) for p in sel)

    checks = [
        (CODE, None, "eighty-six (86) feet to two hundred forty (240) feet"),
        (DG, [18], "Buildings above 120 feet and up to 240 feet in height are limited"),
        (DG, [18], "Mid-rise buildings up to 86 feet in height"),
        (PC_2023, None, "H, J, and A are fully entitled without tower components"),
        (RES_89709, None, "up to two towers, rather than a single tower, on Parcel M"),
        (OS_2025, None, "The seven-story building"),
        (OS_2025, None, "The eight-story building"),
    ]
    for doc, pages, phrase in checks:
        t = text(doc, pages)
        if " ".join(phrase.split()) not in t:
            raise SystemExit(f"{doc['file']}: expected to find {phrase!r}")
    print(f"[{PROJECT_ID}] {len(checks)} quoted facts found in the source documents")


def _parcels() -> gpd.GeoDataFrame:
    out = CACHE / "bb-oakland-parcels.geojson"
    if not out.exists():
        apns = sorted({a for v in APN.values() for a in v})
        where = "APN_GROUND IN (" + ",".join(f"'{a[:3]} {a[3:]}'" for a in apns) + ")"
        q = urllib.parse.urlencode({"where": where, "outFields": "APN_GROUND,PRINTPARCEL,FULL_SITUSADDRESS",
                                    "outSR": 4326, "f": "geojson"})
        with urllib.request.urlopen(f"{PARCELS['layer']}/query?{q}") as r:
            data = r.read()
        if b'"features"' not in data:
            raise SystemExit(f"parcel query failed: {data[:200]!r}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
    g = gpd.read_file(out).to_crs(UTM)
    g["apn"] = g["APN_GROUND"].str.replace(" ", "")
    missing = {a for v in APN.values() for a in v} - set(g["apn"])
    if missing:
        raise SystemExit(f"parcels missing from the city layer: {sorted(missing)}")
    return g


def _parcel(parcels: gpd.GeoDataFrame, key: str):
    return shapely.union_all(parcels[parcels["apn"].isin(APN[key])].geometry.buffer(0.05).to_numpy()).buffer(-0.05)


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "bb-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(
        lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    return g.to_crs(UTM)


def _render(pdf_path, page_index: int, dpi: int) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[page_index]
    return np.asarray(page.render(scale=dpi / 72).to_pil().convert("RGB"))


def _sheet_regions(rgb: np.ndarray) -> dict[str, Polygon]:
    """Each parcel's grey fill on sheet 1.4, as a pixel polygon."""
    v = rgb.astype(int).mean(axis=2)
    sat = rgb.max(axis=2).astype(int) - rgb.min(axis=2).astype(int)
    mask = ((v > 180) & (v < 205) & (sat < 8)).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab = cv2.connectedComponents(mask)
    out = {}
    for key, (x, y) in SHEET_LABELS.items():
        k = lab[y, x]
        if k == 0:
            raise SystemExit(f"sheet 1.4: no grey fill under the label of Parcel {key}")
        region = (lab == k).astype(np.uint8) * 255
        region = cv2.morphologyEx(region, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))  # fill the label text
        contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contours, key=cv2.contourArea)
        out[key] = shapely.make_valid(Polygon(cv2.approxPolyDP(c, 1.0, True).reshape(-1, 2)))
    shared = [a for a in out for b in out if a < b and out[a].equals(out[b])]
    if shared:
        raise SystemExit(f"sheet 1.4: parcels share one fill: {shared}")
    return out


def _dg_tower_zones(rgb: np.ndarray, sim: trace.Similarity) -> list[Polygon]:
    polys = trace.raster_color_polygons(rgb, TOWER_ORANGE, tol=45, min_area_px=300, close_px=9, simplify_px=1.0)
    # Close the gaps between the hatch stripes' traced edges and smooth the pixel steps (in metres).
    return [sim.geometry(p).buffer(1.5).buffer(-1.5).simplify(1.5) for p in polys]


def _height_from_stories(stories: int) -> int:
    return min(MIDRISE_FT, FLOOR_FT * stories)


def main() -> None:
    paths = _docs()
    _check_text(paths)
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = shapely.union_all(site[site["kind"] == "site"].geometry.to_numpy())
    parcels = _parcels()

    # Sheet 1.4 georeferenced on the parcels it shares with the city's parcel layer.
    sheet_rgb = _render(paths[PDP["file"]], SHEET_1_4["page_index"], SHEET_1_4["dpi"])
    if sheet_rgb.shape[:2] != (2400, 3600):
        raise SystemExit(f"unexpected sheet 1.4 render size {sheet_rgb.shape}")
    regions = _sheet_regions(sheet_rgb)
    src = [regions[k].centroid.coords[0] for k in SHEET_CONTROLS]
    dst = [_parcel(parcels, k).centroid.coords[0] for k in SHEET_CONTROLS]
    sheet_sim = trace.fit_similarity(src, dst, [f"Parcel {k} centroid" for k in SHEET_CONTROLS])
    print(f"[{PROJECT_ID}] sheet 1.4 georeference: RMS {sheet_sim.rms_m:.2f} m over {len(src)} parcel centroids, "
          f"scale {sheet_sim.scale:.4f} m/px")
    for k in SHEET_CONTROLS:  # each traced fill should overlap its city parcel closely
        a, b = sheet_sim.geometry(regions[k]), _parcel(parcels, k)
        iou = a.intersection(b).area / a.union(b).area
        if iou < 0.75:
            raise SystemExit(f"Parcel {k}: sheet 1.4 fill and city parcel overlap only {iou:.0%} (IoU)")

    # Parcels K and L: the city parcel split between the two sheet fills (nearest fill wins).
    kl = _parcel(parcels, "KL")
    k_fig, l_fig = sheet_sim.geometry(regions["K"]), sheet_sim.geometry(regions["L"])
    # Each 1-m cell of the city parcel goes to the nearer of the two georeferenced sheet fills.
    minx, miny, maxx, maxy = kl.bounds
    xs, ys = (a.ravel() for a in np.meshgrid(np.arange(minx, maxx, 1.0), np.arange(miny, maxy, 1.0)))
    cells = shapely.box(xs, ys, xs + 1.0, ys + 1.0)
    pts = shapely.points(xs + 0.5, ys + 0.5)
    near_k = shapely.distance(k_fig, pts) <= shapely.distance(l_fig, pts)
    # Simplifying smooths the 1-m staircase along the split; L takes the rest so the two tile the parcel.
    k_part = trace.largest_polygon(shapely.union_all(cells[near_k]).simplify(1.5).intersection(kl))
    l_part = trace.largest_polygon(kl.difference(k_part))
    shapes = {key: _parcel(parcels, key) for key in ("A", "B", "C", "D", "E", "F", "H", "J", "M")}
    shapes["K"], shapes["L"] = k_part, l_part
    for key in ("K", "L"):
        print(f"[{PROJECT_ID}] Parcel {key}: {shapes[key].area / 4046.86:.2f} ac from the shared city parcel")

    # Design Guidelines tower zones.
    dg_rgb = _render(paths[DG["file"]], DG_FIG["page_index"], DG_FIG["dpi"])
    if dg_rgb.shape[:2] != (1275, 1651):
        raise SystemExit(f"unexpected Design Guidelines render size {dg_rgb.shape}")
    streets = tb.streets("bb-brooklyn_basin", BBOX)
    streets = streets[streets["subtype"] == "road"]
    src, dst, labels = [], [], []
    for (a, b), xy in DG_CONTROLS.items():
        src.append(xy)
        dst.append(tb.intersection(streets, a, b))
        labels.append(f"{a} / {b}")
    dg_sim = trace.fit_similarity(src, dst, labels)
    print(f"[{PROJECT_ID}] Design Guidelines diagram georeference: RMS {dg_sim.rms_m:.2f} m over {len(src)} "
          f"intersections, scale {dg_sim.scale:.4f} m/px")
    zones = _dg_tower_zones(dg_rgb, dg_sim)
    towers = {}
    for key in ("A", "H", "J", "K"):
        hit = [z for z in zones if z.intersection(shapes[key]).area > 0.5 * z.area]
        if len(hit) != 1:
            raise SystemExit(f"Parcel {key}: expected one Design Guidelines tower zone, found {len(hit)}")
        share = hit[0].intersection(shapes[key]).area / shapes[key].area
        print(f"[{PROJECT_ID}] tower zone on Parcel {key}: {hit[0].area:.0f} m², {share:.0%} of the parcel"
              + ("" if key in TOWER_ZONES_KEPT else " (parcel built without a tower; not drawn)"))
        towers[key] = hit[0].intersection(shapes[key])

    # Built buildings.
    bldgs = _buildings()
    built = []
    for spec in BUILT:
        hit = bldgs[bldgs["osm"].fillna("").str.split("@").str[0] == spec["osm"]]
        if len(hit) != 1:
            raise SystemExit(f"{spec['name']}: expected one footprint {spec['osm']}, found {len(hit)}")
        row = hit.iloc[0]
        if spec["parcel"] in shapes:
            cover = row.geometry.intersection(shapes[spec["parcel"]]).area / row.geometry.area
            if cover < 0.85:
                raise SystemExit(f"{spec['name']}: only {cover:.0%} of the footprint is on Parcel {spec['parcel']}")
        elif not row.geometry.representative_point().within(site_utm):
            raise SystemExit(f"{spec['name']}: footprint is off the D-OTN site")
        built.append((spec, row))
        print(f"[{PROJECT_ID}] {spec['name']} (Parcel {spec['parcel']}): {spec['osm']}, "
              f"OSM levels {row['num_floors']}, official stories {spec.get('stories')}")
    built_union = shapely.union_all([r.geometry for _, r in built])

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    sheet_ref = f"{PDP['title']}, {SHEET_1_4['sheet']}, PDF p. {SHEET_1_4['pdf_page']}"
    dg_ref = f"{DG['title']}, {DG_FIG['figure']}, printed p. {DG_FIG['printed_page']} (PDF p. {DG_FIG['pdf_page']})"
    code_ref = f"{CODE['title']} ({CODE['url']})"
    features = []

    def add(props, geom):
        geom = shapely.make_valid(geom.simplify(0.3))
        geom = trace.as_multipolygon(geom)
        if geom.is_empty:
            return
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})

    for key in ("D", "E", "H", "K", "L", "M"):
        geom = shapes[key].intersection(site_utm.buffer(0.5))
        if geom.intersects(built_union):
            geom = geom.difference(built_union)
        shape_src = (f"parcel: City of Oakland parcels, APN {', '.join(APN['KL' if key in 'KL' else key])} "
                     f"({PARCELS['layer']})")
        if key in "KL":
            shape_src += f", split between K and L along Harbor Lane West as drawn on {sheet_ref}"
        tower = towers.get(key) if key in TOWER_ZONES_KEPT else None
        base = geom.difference(tower) if tower is not None else geom
        add({
            "kind": "block", "block": key, "label": f"Parcel {key}", "stage": "entitled",
            "height_ft": MIDRISE_FT, "podium_ft": None, "base_ft": 0, "use": "Residential",
            "phase": UNBUILT[key]["phase"], "illustrative": True,
            "source": f"illustrative: drawn to the 86-ft mid-rise limit of {code_ref} and {DG['title']}, printed "
                      f"p. 15; {shape_src}",
            "note": UNBUILT[key]["note"],
        }, base)
        if tower is not None:
            add({
                "kind": "block", "block": key, "label": f"Parcel {key} tower zone", "stage": "entitled",
                "height_ft": TOWER_FT, "podium_ft": MIDRISE_FT, "base_ft": 0, "use": "Residential",
                "phase": UNBUILT[key]["phase"], "illustrative": True,
                "source": f"illustrative: tower zone traced from {dg_ref}, drawn to the 240-ft tower limit of "
                          f"{code_ref} over the 86-ft mid-rise limit; one tower is allowed in the zone",
                "note": ("A tower of up to 240 ft is allowed somewhere in this zone, with a floor plate of at most "
                         "15,000 sq ft (Design Guidelines p. 15); the zone is drawn whole, solid to 86 ft. "
                         + (UNBUILT[key]["note"] if key == "H" else "")).strip(),
            }, tower)

    for spec, row in built:
        stories = spec.get("stories")
        if stories:
            stories_src = f"stories: {OS_2025['title']} ({OS_2025['url']}), {spec['stories_src']}"
        else:
            stories = int(row["num_floors"])
            stories_src = (f"stories: {stories}, as mapped in OpenStreetMap (building:levels); no official story "
                           f"count was found")
        height = _height_from_stories(stories)
        add({
            "kind": "building", "block": spec["parcel"], "label": spec["name"], "stage": "complete",
            "height_ft": height, "podium_ft": None, "base_ft": 0, "use": spec["use"], "phase": spec["phase"],
            "illustrative": True,
            "source": (f"illustrative: footprint: OpenStreetMap {spec['osm']} via Overture {config.OVERTURE_RELEASE}; "
                       f"{stories_src}; height estimated at {FLOOR_FT} ft a story (the floor-to-floor height of "
                       f"{PDP['title']}, sheet 5.3 sections, PDF p. 34), capped at the 86-ft limit; complete per "
                       f"{OS_2025['title']}, Table 2, p. 28"),
            "stories": stories,
            "note": f"Parcel {spec['parcel']}. The height is estimated from the stories; no official height was found.",
        }, row.geometry)

    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: the unbuilt parcels (D, E, H, K, L and M) are drawn to the 86-ft mid-rise "
                "limit of the Oak to Ninth zoning and design guidelines, with the tower zones still entitled on "
                "Parcels H and K drawn to 240 ft. These are limits, not building designs. The eight completed "
                "buildings on Parcels A, B, C, F, G and J are drawn from their real footprints, with heights "
                "estimated from their stories. Parks, streets and the marinas aren't drawn, and Parcel M's two "
                "allowed towers aren't placed."
            ),
            "note": "Unbuilt parcels are drawn to their height limits, not as building designs; real buildings will be smaller.",
            "sourceUrl": DG["url"],
            "sourceLabel": "Design guidelines, 2014 (PDF)",
            "georeference": {
                "sheet_1_4": {**sheet_sim.report(), "method": "least-squares similarity on the centroids of parcel "
                              "fills matched to the same parcels in the city's parcel layer", "use": "K / L split only"},
                "design_guidelines_tower_zones": {**dg_sim.report(), "method": "least-squares similarity on street "
                                                  "intersections matched to OpenStreetMap (via Overture)"},
                "parcels": "City GIS layer, used as published (no tracing)",
            },
            "license": ("Parcel shapes: City of Oakland GIS (from the Alameda County Assessor), published for reference "
                        "only. Plan figures: City of Oakland public records. Building footprints and story counts: "
                        "OpenStreetMap contributors (ODbL 1.0), via Overture Maps."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".geojson.tmp")
    tmp.write_text(json.dumps(_round(fc), indent=1) + "\n")
    tmp.rename(path)
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
