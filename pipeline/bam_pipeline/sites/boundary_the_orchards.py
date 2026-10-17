"""The Orchards (former Chevron Park, San Ramon): the site traced from the City's General Plan EIR map.

The approval names one parcel: the Notice of Exemption (CEQAnet SCH 2026020219, Feb 6, 2026) gives
"6001 Bollinger Canyon Road ... (APN: 213-120-008)" and "the existing 92-acre site". Neither Contra
Costa County's parcel service nor the City's GIS and document servers can be reached from this
pipeline, so the parcel is traced from the City's own map instead.

The San Ramon 2040 General Plan Draft EIR (Aug 2023, CEQAnet SCH 2022060549) Figure 2-4, Proposed
San Ramon Land Use Designations (PDF p. 67), is one embedded raster (1,987 x 1,500 px) drawn from the
City's GIS with parcel lines. Chevron Park is the pale "Office" area south of Bollinger Canyon Road
between I-680 and the Iron Horse Trail; a parcel line splits it into the large western lot (the
campus) and the smaller Bishop Ranch 1 lots along the trail. The western lot is the site.

1. The figure is placed by three road crossings read off the figure (Bollinger Canyon Road at I-680,
   at Camino Ramon and at the Iron Horse Trail), matched to OpenStreetMap centrelines, then refined
   by trimmed ICP of the I-680 band, the trail band and the Bollinger Canyon Road band against
   their OpenStreetMap lines.
2. The lot is the pale fill's largest piece in that window, grown by half a pixel so its edge sits
   on the middle of the 1-px parcel line.

At about 9 m per pixel the outline is good to a pixel or two (10-20 m), so it is marked approximate
and its acreage is reported against the official 92 acres.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_the_orchards
"""

from __future__ import annotations

import io

import cv2
import numpy as np
import pypdf
import shapely
from PIL import Image
from shapely.geometry import Polygon

from .. import trace
from . import traced_boundaries as tb

PROJECT = "the-orchards"
DEIR_URL = "https://ceqanet.lci.ca.gov/2022060549/2/Attachment/ueWNFZ"
DEIR_SHA = "ad3c1dca1ee6ab79f48f656d79340a2004e3790d317a9c49f3a55d33df97c392"
DEIR = tb.DOCS / "san-ramon-2040-general-plan-draft-eir-2023-08.pdf"
PAGE = 66  # zero-based: PDF p. 67, Figure 2-4
NOE_URL = "https://ceqanet.lci.ca.gov/2026020219/Attachment/G7E_Xs"
BBOX = (-121.99, 37.745, -121.955, 37.77)

OFFICE_BGR = (204, 217, 255)  # the figure's "Office" fill
ORANGE_BGR = (0, 152, 230)  # I-680
GREEN_BGR = (130, 225, 130)  # Iron Horse Trail (also parks; only a narrow corridor is used)
GREY_BGR = (178, 178, 178)  # streets
WINDOW = (800, 800, 940, 900)  # x0, y0, x1, y1 around Chevron Park

# Road crossings read off the figure (pixel x, y), with the OpenStreetMap streets they match.
CONTROLS = [
    ((796.0, 836.0), "Bollinger Canyon Road", None),  # I-680 band centre (motorway lines)
    ((874.0, 813.0), "Bollinger Canyon Road", "Camino Ramon"),
    ((897.0, 806.0), "Bollinger Canyon Road", "San Ramon Valley Iron Horse Trail"),
]


def _image() -> np.ndarray:
    trace.fetch_document(DEIR_URL, DEIR, DEIR_SHA)
    page = pypdf.PdfReader(str(DEIR)).pages[PAGE]
    img = Image.open(io.BytesIO(page.images[0].data)).convert("RGB")
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def _is(im: np.ndarray, bgr) -> np.ndarray:
    return np.all(im == np.array(bgr, np.uint8), axis=2)


def _band_centres(mask: np.ndarray, rows: bool) -> np.ndarray:
    """Middle of the band in each row (rows=True) or column, as pixel (x, y) points."""
    pts = []
    if rows:
        for y in range(mask.shape[0]):
            xs = np.flatnonzero(mask[y])
            if len(xs) >= 2:
                pts.append((xs.mean() + 0.5, y + 0.5))
    else:
        for x in range(mask.shape[1]):
            ys = np.flatnonzero(mask[:, x])
            if len(ys) >= 2:
                pts.append((x + 0.5, ys.mean() + 0.5))
    return np.array(pts, float)


def _corridor(shape, p0, p1, half: float) -> np.ndarray:
    m = np.zeros(shape, np.uint8)
    cv2.line(m, tuple(int(v) for v in p0), tuple(int(v) for v in p1), 255, int(2 * half))
    return m > 0


def georeference(im: np.ndarray, streets) -> tuple[trace.Similarity, dict]:
    motorway = shapely.union_all(streets[streets["class"] == "motorway"].geometry.to_numpy())
    boll = shapely.union_all(streets[streets["name"] == "Bollinger Canyon Road"].geometry.to_numpy())
    trail = shapely.union_all(streets[streets["name"] == "San Ramon Valley Iron Horse Trail"].geometry.to_numpy())
    src, dst, labels = [], [], []
    for px, a, b in CONTROLS:
        if b is None:
            x = motorway.intersection(boll)
            c = shapely.MultiPoint([g for g in getattr(x, "geoms", [x])]).centroid
            dst.append((c.x, c.y))
            labels.append("Bollinger Canyon Rd / I-680")
        else:
            dst.append(tb.intersection(streets, a, b))
            labels.append(f"{a} / {b}".replace(" Road", " Rd").replace("San Ramon Valley ", ""))
        src.append(px)
    init = trace.fit_similarity(np.array(src), np.array(dst), labels)

    # Bands near the site: I-680 (orange), the trail (green, in a narrow corridor), Bollinger (grey, in a corridor).
    H, W = im.shape[:2]
    win = np.zeros((H, W), bool)
    win[760:900, 770:960] = True
    orange = _is(im, ORANGE_BGR) & win
    green = _is(im, GREEN_BGR) & _corridor((H, W), (905, 770), (950, 890), 4) & win
    grey = _is(im, GREY_BGR) & _corridor((H, W), (790, 840), (910, 800), 5)
    p_or = _band_centres(orange, rows=True)
    p_gr = _band_centres(green, rows=True)
    p_bo = _band_centres(grey, rows=False)
    pts = np.vstack([p_or, p_gr, p_bo])
    groups = np.concatenate([np.zeros(len(p_or), int), np.ones(len(p_gr), int), np.full(len(p_bo), 2)])
    # I-680's band is drawn over both carriageways; match it to the middle of the two.
    sim, d = tb.icp(pts, [motorway, trail, boll], groups, init, keep=0.8)
    rep = tb.icp_report(sim, d, 0.8, "I-680, Iron Horse Trail and Bollinger Canyon Rd bands against OpenStreetMap")
    rep["initial_controls"] = init.report()
    return sim, rep


def main() -> None:
    im = _image()
    streets = tb.streets("orchards", BBOX)
    sim, rep = georeference(im, streets)

    office = _is(im, OFFICE_BGR).astype(np.uint8)
    x0, y0, x1, y1 = WINDOW
    win = np.zeros_like(office)
    win[y0:y1, x0:x1] = office[y0:y1, x0:x1]
    n, lab, st, _ = cv2.connectedComponentsWithStats(win, connectivity=4)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    lot = (lab == k).astype(np.uint8)
    contours, _ = cv2.findContours(lot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(contours, key=cv2.contourArea)[:, 0, :].astype(float) + 0.5  # pixel centres
    # Pixel-centre outline -> outer pixel edge (+0.5 px) -> middle of the 1-px parcel line (+0.5 px).
    lot_px = Polygon(c).buffer(1.0, join_style="mitre")
    site = shapely.transform(lot_px, lambda xy: sim.apply(xy))
    site = site.simplify(3.0, preserve_topology=True)
    acres = site.area / tb.ACRE_M2

    tb.write(PROJECT, site, {
        "source": ("traced: City of San Ramon, San Ramon 2040 General Plan Draft EIR (Aug 2023, SCH 2022060549), "
                   "Figure 2-4, Proposed San Ramon Land Use Designations (PDF p. 67): the Chevron Park parcel"),
        "sourceLabel": "General Plan Draft EIR, Figure 2-4 (2023)",
        "sourceUrl": DEIR_URL,
        "accuracy": "approximate",
        "accuracyNote": (
            "The approval names one parcel, APN 213-120-008 at 6001 Bollinger Canyon Road, the \"existing 92-acre site\" "
            "(Notice of Exemption, Feb 2026). The County's parcel map can't be reached here, so the parcel is traced from "
            "the City's General Plan EIR land-use map, which draws parcel lines at about 9 m per pixel: the large lot of "
            "the former Chevron Park between I-680, Bollinger Canyon Road and the Bishop Ranch 1 lots along the Iron "
            "Horse Trail. The map is placed on I-680, the trail and Bollinger Canyon Road (trimmed RMS "
            f"{rep['rms_m']:.0f} m), so the edge is good to about 10-20 m. {acres:.1f} acres as drawn, against the "
            "official 92 acres."
        ),
        "officialAcres": 92,
        "officialAcresSource": NOE_URL,
        "license": ("Traced facts from a public City of San Ramon document (the PDF is not redistributed). "
                    f"Georeference: {tb.OSM_LICENSE}."),
        "georeference": rep,
    })


if __name__ == "__main__":
    main()
