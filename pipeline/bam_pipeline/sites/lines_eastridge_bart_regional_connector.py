"""Eastridge to BART Regional Connector (VTA): light rail alignment and stations traced from VTA's plans.

VTA publishes no GIS layer of the extension that this build can reach (gis.vta.org refused the
connection on 2026-10-17), so the alignment is traced from the plan-and-profile sheets VTA attached
to the Draft Second Supplemental EIR: "Attachment C, Detailed Plans for the Proposed Changes"
(Eastridge to BART Regional Connector: Capitol Expressway Light Rail Project, Draft SEIR-2, 2018;
sheets EX001 to EX015, BKF Engineers for VTA, dated July 19, 2018, contract C801), posted on
vta.org with the 2019 Final SEIR-2, which VTA certified on June 6, 2019 (CEQAnet SCH 2001092014).
The later addenda (Feb 2020: turn lane, traction power, PG&E service, tree in-lieu fees, parking
canopies; Feb 2021: tree removals) do not move the tracks.

The 15 sheets (one 3,224 x 5,000 px scan each, 300 dpi, plan at 1" = 40') run from STA 964+80 on
Capitol Avenue at Wilbur Avenue, where the extension conforms to the existing tracks south of the
Alum Rock station, to the bumping posts at STA 1095+ beyond Eastridge station. On each sheet:

1. The two track centrelines ("CL NB TRACK", "CL SB TRACK (CONTROL LINE)") are found by their station
   ticks: short black strokes across the line every 50 ft (187 px at the sheet's scale, which the
   scale bar confirms). Tick candidates are chained left to right at whole multiples of the tick
   spacing with a smooth slope, and the two longest chains are the tracks (crossover tracks at
   Eastridge, which cross at a slope, fall out).
2. Georeference: the sheet's grey base map near the tracks (kerbs, medians, lane lines, cross
   streets) is fitted to OpenStreetMap street centrelines (via Overture) by trimmed ICP with the
   scale held at the drawing scale, so only rotation and shift are fitted. Fits are started from
   several offsets across the corridor (placed by the sheet's stations along a rough corridor line:
   OpenStreetMap's Capitol Avenue and Capitol Expressway, smoothed, counting from Wilbur Avenue),
   because parallel carriageways make the fit ambiguous sideways.
3. Tie (adjust): the sheets are adjusted together by least squares: each match-line join must close
   (the SB control line's stationing gives the distance across it) with a smooth tangent, and on
   EX001-EX011, where VTA puts the line in the median of Capitol Avenue and Capitol Expressway, the
   tracks' middle is held to the middle of the street. EX012-EX015, where the tracks leave the
   median for the Eastridge Transit Center, follow from the joins and their own street fits.
4. The alignment is the centreline between the two tracks; where only one track is found (the
   first and last few hundred feet), the other is taken at the local track spacing. Consecutive
   sheets are joined straight across the short gap at each match line.

Stations (points on the centreline): Story Road, the platform between work points WP1 and WP2 on
sheet EX004; Eastridge, the platform between WP3 and WP4 on sheet EX014. The existing Alum Rock
station is north of the sheets and not drawn.

The check against OpenStreetMap's own mapping of the line under construction ("Alum Rock-Eastridge
Corridor") is reported, not used.

    uv run --directory pipeline python -m bam_pipeline.sites.lines_eastridge_bart_regional_connector
"""

from __future__ import annotations

import cv2
import numpy as np
import shapely
import shapely.ops
from shapely.geometry import LineString, Point

from .. import config, trace
from . import line_georef as lg
from . import traced_boundaries as tb
from .lines import write_line_project
from .lines_bart_silicon_valley_phase_2 import centreline, oriented

PROJECT = "eastridge-bart-regional-connector"
ATT_C = {
    "url": "https://www.vta.org/sites/default/files/documents/Att_C_Detailed_Plans_for_the_Proposed_Changes.pdf",
    "file": "ebrc-draft-seir-2-attachment-c-detailed-plans-2018.pdf",
    "sha256": "e082435cf6178dbc3f25a1bf34d9f142664981d90e00fac43faa2142b7432312",
}
SHEET_SIZE = (3224, 5000)  # as scanned (portrait); rotated a quarter turn to read
N_SHEETS = 15
BBOX = (-121.845, 37.300, -121.800, 37.380)
FT = 0.3048
MILE_M = 1609.344
TICK_PX = 187.0  # station ticks every 50 ft
PX_PER_FT = TICK_PX / 50  # 3.74 px/ft: the 0-40 ft scale bar measures 149.5 px
M_PER_PX = FT / PX_PER_FT
TICK_BAND = (400, 1450, 600, 4400)  # y0, y1, x0, x1 (rotated sheet px) where the tracks run
ICP_BAND = (100, 1500, 400, 4450)
DS = 4  # the ICP runs on the sheet shrunk 4x
LEFT_MATCH_X, RIGHT_MATCH_X = 862.0, 4250.0  # match lines: first ticks sit on the left one
# First guess only: Wilbur Avenue crosses the tracks at about STA 965+14 (sheet EX001, px x 1310), and
# the corridor ends near (605390, 4131850) UTM 10N, the Eastridge end of East Capitol Expressway's median.
WILBUR_STA = 965.14
EASTRIDGE_END = np.array([605390.0, 4131850.0])
LATERAL_STARTS_M = (-45, -30, -15, 0, 15, 30, 45)
CANDIDATE_RMS_RATIO = 1.15
BAND_M = 45.0
# Station platforms: (sheet index, x of the platform's two work points, name, note).
STATIONS = [
    (3, (1770.0, 2750.0), "Story Road", "New elevated station in the Capitol Expressway median, reached by a pedestrian overcrossing"),
    (13, (2975.0, 4000.0), "Eastridge", "New at-grade station at the Eastridge Transit Center"),
]

LICENSE = ("Traced facts from public VTA documents (the PDFs are not redistributed). Georeference: "
           f"{tb.OSM_LICENSE}.")


def sheet(pdf, k: int) -> np.ndarray:
    """Sheet EX00k+1, grey, rotated to read (x along the track, y down)."""
    rgb = lg.pdf_image(pdf, k + 1, SHEET_SIZE)
    return np.rot90(rgb, 1).copy()


def tick_candidates(gray: np.ndarray) -> np.ndarray:
    """Short vertical black strokes with a thin horizontal line through their middle: (x, y)."""
    y0, y1, x0, x1 = TICK_BAND
    b = (gray < 110).astype(np.uint8)
    b[:y0], b[y1:], b[:, :x0], b[:, x1:] = 0, 0, 0, 0
    vert = cv2.morphologyEx(b, cv2.MORPH_OPEN, np.ones((13, 1), np.uint8))
    hor = cv2.morphologyEx(b, cv2.MORPH_OPEN, np.ones((1, 25), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(vert, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, _ = st[i]
        if not (14 <= h <= 40 and w <= 6):
            continue
        left = np.nonzero(hor[y:y + h, max(0, x - 20):x])[0]
        right = np.nonzero(hor[y:y + h, x + w:x + w + 20])[0]
        if len(left) < 5 or len(right) < 5:
            continue
        ly = y + float(np.median(np.r_[left, right]))
        if abs(ly - (y + h / 2)) <= h * 0.3:
            out.append((x + w / 2, ly))
    return np.array(sorted(out))


def _best_chain(t: np.ndarray, used: np.ndarray) -> list[int]:
    n = len(t)
    length, prev, slope = np.ones(n), -np.ones(n, int), np.zeros(n)
    for i in range(n):
        if used[i]:
            continue
        best = None
        for j in range(i):
            if used[j]:
                continue
            dx, dy = t[i, 0] - t[j, 0], t[i, 1] - t[j, 1]
            m = round(dx / TICK_PX)
            if not (1 <= m <= 5 and abs(dx - TICK_PX * m) < 40) or abs(dy / dx) > 0.2:
                continue
            if prev[j] >= 0 and abs(dy - slope[j] * dx) > 12:
                continue
            key = (length[j] + 1, -abs(dy / dx - (slope[j] if prev[j] >= 0 else dy / dx)))
            if best is None or key > best[0]:
                best = (key, j, dy / dx)
        if best:
            length[i], prev[i], slope[i] = best[0][0], best[1], best[2]
    i = int(np.argmax(np.where(used, -1, length)))
    chain = []
    while i >= 0:
        chain.append(i)
        i = prev[i]
    return chain[::-1]


def track_chains(gray: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The two tracks as tick chains (px), the upper (NB) first."""
    t = tick_candidates(gray)
    used = np.zeros(len(t), bool)
    chains = []
    for _ in range(2):
        c = _best_chain(t, used)
        used[c] = True
        chains.append(t[c])
    nb, sb = sorted(chains, key=lambda c: c[:, 1].mean())
    return nb, sb


def grey_pixels(gray: np.ndarray, track: np.ndarray) -> np.ndarray:
    """The base map's grey linework (not the black project linework) within BAND_M of the track,
    shrunk DS times, as px. Keeping to the corridor leaves mostly the expressway's own kerbs and
    medians and the cross streets, whose pattern pins the sheet sideways better than the parallel
    frontage roads and parking aisles further out."""
    y0, y1, x0, x1 = ICP_BAND
    g = cv2.resize(gray[y0:y1, x0:x1].astype(np.float32), ((x1 - x0) // DS, (y1 - y0) // DS), interpolation=cv2.INTER_AREA)
    m = ((g > 120) & (g < 235)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    ys, xs = np.nonzero(m)
    pts = np.c_[xs * DS + x0, ys * DS + y0].astype(float)
    near = shapely.distance(shapely.points(pts), LineString(track)) < BAND_M / M_PER_PX
    pts = pts[near]
    sel = np.random.default_rng(0).choice(len(pts), min(len(pts), 20000), replace=False)
    return pts[sel]


def _angle_px(a, b) -> float:
    return float(np.arctan2(-(b[1] - a[1]), b[0] - a[0]))  # figure y is down


def _anchored(px, utm, rotation) -> trace.Similarity:
    sim = trace.Similarity(M_PER_PX, rotation, 0.0, 0.0)
    o = sim.apply([px])[0]
    sim.tx, sim.ty = utm[0] - o[0], utm[1] - o[1]
    return sim


def reference_route(streets) -> LineString:
    """A first guess of the corridor, only to start each sheet's fit: OpenStreetMap's South Capitol Avenue
    from Wilbur Avenue and East Capitol Expressway on to Eastridge, ordered along the corridor and
    smoothed over 150 m, so the two carriageways average to the median."""
    wilbur = np.array(tb.intersection(streets, "South Capitol Avenue", "Wilbur Avenue"))
    junction = np.array(tb.intersection(streets, "South Capitol Avenue", "East Capitol Expressway"))
    axis = (EASTRIDGE_END - wilbur) / np.linalg.norm(EASTRIDGE_END - wilbur)
    s_j = (junction - wilbur) @ axis
    parts = []
    for name, lo, hi in (("South Capitol Avenue", -20.0, s_j), ("East Capitol Expressway", s_j, np.inf)):
        sel = (streets["name"] == name) & (streets["class"] != "residential")
        xy = np.concatenate([np.asarray(shapely.segmentize(g, 5).coords) for g in streets[sel].geometry])
        s_ = (xy - wilbur) @ axis
        side = (xy - wilbur) @ np.array([-axis[1], axis[0]])
        parts.append(xy[(s_ >= lo) & (s_ <= hi) & (np.abs(side) < 150)])
    xy = np.concatenate(parts)
    s = (xy - wilbur) @ axis
    sel = s < np.linalg.norm(EASTRIDGE_END - wilbur) + 100
    xy, s = xy[sel], s[sel]
    pts = []
    for c in np.arange(0, s.max(), 10.0):
        w = np.abs(s - c) < 75
        if w.sum() >= 3:
            pts.append(xy[w].mean(0))
    route = LineString(pts)
    start = route.project(Point(wilbur))
    return shapely.ops.substring(route, start, route.length)


def station_at(k: int, x: float) -> float:
    """Station (in hundreds of feet) at sheet px x, from the sheet's match lines."""
    if k == N_SHEETS - 1:
        return 1090.0 + (x - LEFT_MATCH_X) / (PX_PER_FT * 100)
    right = 973.0 + 9 * k
    return right - (RIGHT_MATCH_X - x) / (PX_PER_FT * 100)


def to_utm(sim, px) -> np.ndarray:
    return sim.apply(np.asarray(px, float))


def tick_stations(k: int, sb: np.ndarray) -> np.ndarray:
    """Station (hundreds of feet) of each SB control-line tick: 50 ft apart along the drawn line,
    counted from the end nearest a match line."""
    arc = np.r_[0, np.cumsum(np.hypot(*np.diff(sb, axis=0).T))]
    steps = np.round(arc / TICK_PX) * 0.5
    if k == N_SHEETS - 1:
        first = round(station_at(k, sb[0, 0]) * 2) / 2
        return first + steps
    last = round(station_at(k, sb[-1, 0]) * 2) / 2
    return last - (steps[-1] - steps)


def _corrected(sim: trace.Similarity, pivot_px, c) -> trace.Similarity:
    """sim, then turned by c[2] (rad) about the pivot and shifted c[0] along / c[1] across its heading."""
    a, b, phi = c
    piv = sim.apply([pivot_px])[0]
    new = trace.Similarity(sim.scale, sim.rotation + phi, 0.0, 0.0)
    o = new.apply([pivot_px])[0]
    h = sim.rotation  # figure x (along the track) points this way on the ground
    shift = a * np.array([np.cos(h), np.sin(h)]) + b * np.array([-np.sin(h), np.cos(h)])
    new.tx, new.ty = piv[0] - o[0] + shift[0], piv[1] - o[1] + shift[1]
    return new


SIGMA = {"along_m": 10.0, "across_m": 30.0, "turn_deg": 5.0, "join_m": 0.5, "join_turn_deg": 0.5, "median_m": 4.0}
# Sheets where VTA puts the tracks in the middle of the street: Capitol Avenue's existing light rail
# median (EX001-EX002) and "primarily in the median of Capitol Expressway" (EX003-EX011). From EX012
# the tracks leave the median for the Eastridge Transit Center, so they are held by the joins alone.
MEDIAN_SHEETS = range(0, 11)


def track_middle(nb: np.ndarray, sb: np.ndarray) -> np.ndarray:
    """Points midway between the tracks, at the SB ticks where the NB track is also drawn (px)."""
    x = sb[:, 0]
    ok = (x >= nb[0, 0]) & (x <= nb[-1, 0])
    return np.c_[x[ok], (sb[ok, 1] + np.interp(x[ok], nb[:, 0], nb[:, 1])) / 2]


def side_of(route: LineString, pts: np.ndarray) -> np.ndarray:
    """Signed distance (m) of ground points from the corridor's middle line (left positive)."""
    out = []
    for x, y in pts:
        at = route.project(Point(x, y))
        a, b, f = route.interpolate(max(0.0, at - 5)), route.interpolate(at + 5), route.interpolate(at)
        t = np.array([b.x - a.x, b.y - a.y])
        t /= np.linalg.norm(t)
        out.append(t[0] * (y - f.y) - t[1] * (x - f.x))
    return np.array(out)


def adjust(sims: list, nbs: list, sbs: list, stations: list, route: LineString) -> tuple[list, dict]:
    """Tie the sheets together and to the street.

    The street fit alone is ambiguous sideways: the plans draw many parallel kerb, lane and median
    lines and OpenStreetMap has a few centrelines, so fits a carriageway apart score almost alike.
    Two further facts settle it. The SB control line is stationed, so the ground distance from one
    sheet's last tick to the next sheet's first is known (50 ft per tick step), and the line must
    run on smoothly across each match line. And where VTA puts the tracks in the street's median
    (MEDIAN_SHEETS), their middle is held to the middle of the street (OpenStreetMap's carriageways
    averaged). A least-squares adjustment (Gauss-Newton) finds per-sheet corrections (shift along
    and across, turn) to the street fits that meet all three, at the sigmas in SIGMA."""
    n = len(sims)
    pivots = [sb[len(sb) // 2] for sb in sbs]
    mids = [track_middle(nb, sb)[::3] for nb, sb in zip(nbs, sbs)]

    def residuals(x):
        c = x.reshape(n, 3)
        adj = [_corrected(sims[k], pivots[k], c[k]) for k in range(n)]
        r = []
        for k in range(1, n):
            e = adj[k - 1].apply(sbs[k - 1][-2:])
            s_ = adj[k].apply(sbs[k][:2])
            d0, d1 = e[1] - e[0], s_[1] - s_[0]
            d0, d1 = d0 / np.linalg.norm(d0), d1 / np.linalg.norm(d1)
            u = (d0 + d1) / np.linalg.norm(d0 + d1)
            gap = (stations[k][0] - stations[k - 1][-1]) * 100 * FT
            r += list((s_[0] - e[1] - u * gap) / SIGMA["join_m"])
            r.append(np.arcsin(np.clip(d0[0] * d1[1] - d0[1] * d1[0], -1, 1)) / np.radians(SIGMA["join_turn_deg"]))
        for k in MEDIAN_SHEETS:
            r += list(side_of(route, adj[k].apply(mids[k])) / SIGMA["median_m"])
        r += list(c[:, 0] / SIGMA["along_m"]) + list(c[:, 1] / SIGMA["across_m"])
        r += list(c[:, 2] / np.radians(SIGMA["turn_deg"]))
        return np.array(r)

    x = np.zeros(3 * n)
    for _ in range(15):
        r0 = residuals(x)
        J = np.empty((len(r0), len(x)))
        for j in range(len(x)):
            dx = np.zeros_like(x)
            dx[j] = 1e-4
            J[:, j] = (residuals(x + dx) - r0) / 1e-4
        step = np.linalg.lstsq(J, -r0, rcond=None)[0]
        x += step
        if np.abs(step).max() < 1e-5:
            break
    c = x.reshape(n, 3)
    out = [_corrected(sims[k], pivots[k], c[k]) for k in range(n)]
    off = {f"EX{k + 1:03d}": round(float(np.median(side_of(route, out[k].apply(mids[k])))), 1) for k in range(n)}
    rep = {"method": ("least-squares tie of the sheets: match-line joins closed using the SB control line's stationing, "
                      "smooth tangents across joins, and on EX001-EX011 the tracks' middle held to the middle of "
                      "Capitol Avenue / Capitol Expressway (OpenStreetMap carriageways averaged); per-sheet "
                      "corrections to the street fits, sigmas " + ", ".join(f"{k} {v}" for k, v in SIGMA.items())),
           "corrections": {f"EX{k + 1:03d}": {"along_m": round(float(c[k, 0]), 1), "across_m": round(float(c[k, 1]), 1),
                                               "turn_deg": round(float(np.degrees(c[k, 2])), 2)} for k in range(n)},
           "offset_from_street_middle_m": off}
    return out, rep


def choose_candidates(candidates: list, nbs: list, sbs: list, route: LineString) -> list[int]:
    """Of each sheet's street fits, the one whose track middle sits nearest the street's middle where
    the tracks run in the median; elsewhere the fit with the lowest residual."""
    pick = []
    for k, cands in enumerate(candidates):
        if k in MEDIAN_SHEETS:
            mid = track_middle(nbs[k], sbs[k])[::3]
            pick.append(int(np.argmin([np.abs(side_of(route, sim.apply(mid))).mean() for sim, _ in cands])))
        else:
            pick.append(0)
    return pick


FITS_CACHE = config.RAW / "lines" / "eastridge-sheet-fits.pkl"


def fit_sheets(pdf, streets, roads):
    """Tracks and street fits for every sheet (cached in data/raw/lines/, keyed by the document hash)."""
    import pickle
    if FITS_CACHE.exists():
        cached = pickle.loads(FITS_CACHE.read_bytes())
        if cached.get("sha256") == ATT_C["sha256"] and cached.get("starts") == (LATERAL_STARTS_M, CANDIDATE_RMS_RATIO, BAND_M):
            return cached["sheets"], cached["candidates"]
    route = reference_route(streets)
    sheets, reports, candidates = [], {}, []
    for k in range(N_SHEETS):
        gray = cv2.cvtColor(sheet(pdf, k), cv2.COLOR_RGB2GRAY).astype(int)
        nb, sb = track_chains(gray)
        spacing = float(np.median(np.diff(np.r_[nb[:, 0], sb[:, 0]][np.argsort(np.r_[nb[:, 0], sb[:, 0]])])))
        mid = sb[len(sb) // 2]
        ch = (station_at(k, mid[0]) - WILBUR_STA) * 100 * FT
        p, q = route.interpolate(ch - 15), route.interpolate(ch + 15)
        heading = np.arctan2(q.y - p.y, q.x - p.x)
        a, b = sb[max(0, len(sb) // 2 - 2)], sb[min(len(sb) - 1, len(sb) // 2 + 2)]
        init = _anchored(mid, route.interpolate(ch).coords[0], float(heading - _angle_px(a, b)))
        px = grey_pixels(gray, sb)
        fp = shapely.Polygon(init.apply([(ICP_BAND[2], ICP_BAND[0]), (ICP_BAND[3], ICP_BAND[0]),
                                         (ICP_BAND[3], ICP_BAND[1]), (ICP_BAND[2], ICP_BAND[1])])).buffer(250)
        target = shapely.union_all(roads[roads.intersects(fp)].geometry.to_numpy())
        # Parallel carriageways make the fit ambiguous sideways: start it from several offsets across the
        # corridor (the tracks leave the median at both ends) and keep every fit within 8% of the best.
        sub = px[np.random.default_rng(1).choice(len(px), min(len(px), 3000), replace=False)]
        normal = np.array([-np.sin(heading), np.cos(heading)])
        trials = []
        for dn in LATERAL_STARTS_M:
            i0 = _anchored(mid, np.asarray(route.interpolate(ch).coords[0]) + dn * normal, init.rotation)
            s0, d0 = tb.icp(sub, [target], np.zeros(len(sub), int), i0, keep=0.4, iterations=40, scale=M_PER_PX)
            inl = d0 <= np.quantile(d0, 0.4)
            trials.append((float(np.sqrt((d0[inl] ** 2).mean())), dn, s0))
        trials.sort(key=lambda t: t[0])
        cands = []
        for rms0, dn, s0 in trials:
            if rms0 > trials[0][0] * CANDIDATE_RMS_RATIO:
                break
            if any(np.hypot(*(c[0].apply([mid])[0] - s0.apply([mid])[0])) < 3 for c in cands):
                continue
            cands.append((s0, {"lateral_start_m": dn, "trial_rms_m": round(rms0, 2)}))
        sim, rep = cands[0]
        rep["px"] = px
        rep["target"] = target
        rep["ticks"] = {"NB": int(len(nb)), "SB": int(len(sb))}
        reports[f"EX{k + 1:03d}"] = rep
        sheets.append((sim, nb, sb, spacing))
        candidates.append(cands)
        print(f"  EX{k + 1:03d}: {len(nb)}+{len(sb)} ticks, {len(cands)} candidate street fits")

    FITS_CACHE.parent.mkdir(parents=True, exist_ok=True)
    FITS_CACHE.write_bytes(pickle.dumps({"sha256": ATT_C["sha256"], "starts": (LATERAL_STARTS_M, CANDIDATE_RMS_RATIO, BAND_M),
                                         "sheets": sheets, "candidates": candidates}))
    return sheets, candidates


def build() -> None:
    pdf = trace.fetch_document(ATT_C["url"], tb.DOCS / ATT_C["file"], ATT_C["sha256"])
    streets = tb.streets("ebrc", BBOX)
    roads = streets[streets["subtype"] == "road"]

    sheets, candidates = fit_sheets(pdf, streets, roads)
    reports = {}
    stations = [tick_stations(k, sh[2]) for k, sh in enumerate(sheets)]
    route = reference_route(streets)
    pick = choose_candidates(candidates, [sh[1] for sh in sheets], [sh[2] for sh in sheets], route)
    for k, j in enumerate(pick):
        s0, info = candidates[k][j]
        px, target = candidates[k][0][1]["px"], candidates[k][0][1]["target"]
        sim, d = tb.icp(px, [target], np.zeros(len(px), int), s0, keep=0.4, iterations=80, scale=M_PER_PX)
        rep = tb.icp_report(sim, d, 0.4, "grey base-map linework against OpenStreetMap street centrelines")
        rep.update({"candidates": len(candidates[k]), "chosen": j, "lateral_start_m": info["lateral_start_m"],
                    "ticks": {"NB": int(len(sheets[k][1])), "SB": int(len(sheets[k][2]))}})
        print(f"  EX{k + 1:03d}: chose fit {j} of {len(candidates[k])} (trimmed RMS {rep['rms_m']} m, "
              f"started {rep['lateral_start_m']} m across)")
        reports[f"EX{k + 1:03d}"] = rep
        sheets[k] = (sim,) + tuple(sheets[k][1:])
    adjusted, tie = adjust([sh[0] for sh in sheets], [sh[1] for sh in sheets], [sh[2] for sh in sheets], stations, route)
    sheets = [(adjusted[k],) + tuple(sh[1:]) for k, sh in enumerate(sheets)]
    for k, cr in tie["corrections"].items():
        print(f"  {k}: tie correction {cr}")

    # Centreline per sheet (UTM), then joined across the match lines.
    pieces, joins = [], []
    for k, (sim, nb, sb, _) in enumerate(sheets):
        a, b = LineString(to_utm(sim, nb)), LineString(to_utm(sim, sb))
        mid, med_gap, _ = centreline(b, a, step=2.0)  # along the SB control line
        mid = oriented(mid, Point(b.coords[0]))
        # Extend over SB-only stretches (start of EX001, Eastridge tail tracks) at half the track spacing.
        half = med_gap / 2
        sb_line = b
        s0 = sb_line.project(Point(mid.coords[0]))
        s1 = sb_line.project(Point(mid.coords[-1]))
        nb_mid = Point(np.asarray(a.coords)[len(a.coords) // 2])
        at = sb_line.project(nb_mid)
        p0, p1 = sb_line.interpolate(max(0.0, at - 5)), sb_line.interpolate(min(sb_line.length, at + 5))
        foot = sb_line.interpolate(at)
        side = 1.0 if (p1.x - p0.x) * (nb_mid.y - foot.y) - (p1.y - p0.y) * (nb_mid.x - foot.x) > 0 else -1.0
        off = sb_line.offset_curve(side * half)
        coords = list(mid.coords)
        if s0 > 5:
            head = shapely.ops.substring(off, 0, off.project(Point(coords[0])))
            coords = list(head.coords)[:-1] + coords
        if sb_line.length - s1 > 5:
            tail = shapely.ops.substring(off, off.project(Point(coords[-1])), off.length)
            coords = coords + list(tail.coords)[1:]
        line = LineString(coords).simplify(0.3)
        if pieces:
            p_end = np.asarray(pieces[-1].coords[-1])
            q0, q1 = np.asarray(line.coords[0]), np.asarray(line.coords[1])
            prev_dir = p_end - np.asarray(pieces[-1].coords[-2])
            prev_dir /= np.linalg.norm(prev_dir)
            v = q0 - p_end
            joins.append({"after": f"EX{k:03d}", "gap_m": round(float(np.linalg.norm(v)), 1),
                          "sideways_m": round(float(abs(prev_dir[0] * v[1] - prev_dir[1] * v[0])), 1)})
        pieces.append(line)
    chain = []
    for p in pieces:
        chain += list(p.coords)
    alignment = LineString(chain).simplify(0.3)

    # Stations: the middle of each platform's work points, on the centreline.
    st_feats = []
    for k, (xa, xb), name, note in STATIONS:
        sim, nb, sb, _ = sheets[k]
        sb_line = LineString(sb)
        ya, yb = (np.interp(x, sb[:, 0], sb[:, 1]) for x in (xa, xb))
        nya, nyb = (np.interp(x, nb[:, 0], nb[:, 1]) for x in (xa, xb))
        mid_px = ((xa + xb) / 2, (ya + yb + nya + nyb) / 4)
        g = Point(to_utm(sim, [mid_px])[0])
        g = alignment.interpolate(alignment.project(g))
        length_ft = abs(xb - xa) / PX_PER_FT
        st_feats.append({"geometry": lg.utm_to_wgs(g), "properties": {
            "kind": "station", "status": "new", "name": name, "note": note,
            "source": (f"traced: VTA Draft SEIR-2 Attachment C, sheet EX{k + 1:03d}: middle of the platform between its "
                       f"work points (about {length_ft:.0f} ft apart)")}})
        del sb_line

    # Check only: OpenStreetMap's mapping of the line under construction.
    osm = streets[streets["name"].fillna("").str.contains("Eastridge Corridor")]
    check = {}
    if len(osm):
        o = shapely.union_all(osm.geometry.to_numpy())
        ends = shapely.MultiPoint([q for g in getattr(o, "geoms", [o]) for q in (g.coords[0], g.coords[-1])])
        pts = [alignment.interpolate(s) for s in np.arange(0, alignment.length, 25)]
        # Only where OpenStreetMap maps the tracks (not past its ends, e.g. the tail tracks).
        pts = [p for p in pts if shapely.ops.nearest_points(o, p)[0].distance(ends) > 1.0]
        dd = np.array([o.distance(p) for p in pts])
        check = {"osm_corridor_median_m": round(float(np.median(dd)), 1),
                 "osm_corridor_p90_m": round(float(np.quantile(dd, 0.9)), 1),
                 "osm_corridor_note": ("distance from the traced centreline to the nearer of OpenStreetMap's two "
                                       "'Alum Rock-Eastridge Corridor' tracks; the tracks are about 2-3 m either side "
                                       "of the centreline")}

    miles = alignment.length / MILE_M
    rms = [r["rms_m"] for r in reports.values()]
    print(f"  {miles:.2f} miles as drawn; joins {joins}; check {check}")
    src = ("traced: VTA, Eastridge to BART Regional Connector Draft SEIR-2 (2018), Attachment C, Detailed Plans for "
           "the Proposed Changes, sheets EX001-EX015: centreline between the NB and SB track centrelines")
    features = [{"geometry": lg.utm_to_wgs(alignment), "properties": {
        "kind": "line", "segment": "new", "name": "Light rail extension, Alum Rock to Eastridge",
        "note": ("From the existing tracks on Capitol Avenue at Wilbur Avenue, onto an elevated guideway mostly in "
                 "the Capitol Expressway median, down to the at-grade Eastridge station"),
        "source": src}}] + st_feats

    write_line_project(PROJECT, features, {
        "source": ("traced: VTA, Eastridge to BART Regional Connector: Capitol Expressway Light Rail Project, Draft "
                   "Second Supplemental EIR (2018), Attachment C, Detailed Plans for the Proposed Changes "
                   "(sheets EX001-EX015, July 2018); georeferenced to OpenStreetMap streets"),
        "sourceLabel": "VTA Draft SEIR-2 plans (2018), Attachment C",
        "sourceUrl": ATT_C["url"],
        "accuracy": "traced",
        "accuracyNote": (
            f"Track centrelines traced from VTA's 15 plan-and-profile sheets (1\" = 40'), found by their 50-ft station "
            f"ticks, and drawn as the centreline between the two tracks: {miles:.1f} miles as drawn from the conform "
            f"point with the existing tracks at Wilbur Avenue to the bumping posts beyond Eastridge (VTA: 2.4 miles). "
            f"Each sheet is fitted to OpenStreetMap streets at the drawing scale (trimmed RMS {min(rms):.1f}-"
            f"{max(rms):.1f} m), and the sheets are tied together at their match lines and to the middle of the street "
            f"along Capitol Avenue (where the plans draw the tracks in its median) and Capitol Expressway (where VTA "
            f"describes the line 'primarily in the median'). As a check, "
            f"the result lies a median {check.get('osm_corridor_median_m', float('nan')):.0f} m (90% within "
            f"{check.get('osm_corridor_p90_m', float('nan')):.0f} m) from OpenStreetMap's own mapping of the tracks "
            f"under construction, so the line is good to about 5 m, less certain at the Eastridge end. The plans "
            f"date from the 2018 environmental review; "
            f"the 2020 and 2021 addenda did not move the tracks, but the final design may differ in detail. Station "
            f"points are platform middles, not platform outlines. The existing Alum Rock station, north of the plans, "
            f"is not drawn."),
        "license": LICENSE,
        "lengthMiles": round(miles, 2),
        "georeference": {"sheets": reports, "tie": tie, "joins": joins, "scale_m_per_px": round(M_PER_PX, 5),
                         "start": "Wilbur Avenue x South Capitol Avenue (OpenStreetMap) at the conform point, sheet EX001"},
        "check": check,
        "otherSources": ["https://www.vta.org/projects/eastridge-bart-regional-connector",
                         "https://ceqanet.lci.ca.gov/Project/2001092014"],
    })


if __name__ == "__main__":
    build()
