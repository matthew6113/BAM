import type { GeoJSONSource, Map as MapLibreMap, PaddingOptions } from 'maplibre-gl';
import type { Feature, LineString, MultiPolygon, Polygon } from 'geojson';
import { bboxOf, centroidOf, linePrefix, metres, type Massing, type Project } from './data';

export interface Camera {
  center: [number, number];
  zoom: number;
  pitch: number;
  bearing: number;
}

/** The flight takes about 4.5 s; the boundary draws itself over its second half. */
export const FLIGHT_MS = 4500;
export const RETURN_MS = 3000;
export const RISE_MS = 1200;
export const RISE_STAGGER_MS = 600;

/** Where the fly-in lands when a project has no tuned camera yet. */
export const DEFAULT_PITCH = 58;

/**
 * Tuned cameras in data/projects.json are framed for this much open map: a 1440 x 900
 * window less the 400 px panel. Smaller views zoom out to keep the same site in frame.
 */
export const REFERENCE_VIEW = { width: 1040, height: 900 };

/** Below this width the panel is a bottom sheet over the lower half of the map. */
export const SHEET_BREAKPOINT = 720;
export const PANEL_WIDTH = 400;
export const SHEET_FRACTION = 0.5;

export const prefersReducedMotion = () =>
  typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;

const easeInOutCubic = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
const easeOutCubic = (t: number) => 1 - (1 - t) ** 3;
const clamp01 = (t: number) => Math.min(1, Math.max(0, t));

export function currentCamera(map: MapLibreMap): Camera {
  const c = map.getCenter();
  return { center: [c.lng, c.lat], zoom: map.getZoom(), pitch: map.getPitch(), bearing: map.getBearing() };
}

/** The part of the map the project panel covers, so the camera centres on what's left. */
export function panelPadding(map: MapLibreMap): PaddingOptions {
  const el = map.getContainer();
  if (el.clientWidth < SHEET_BREAKPOINT) {
    return { top: 48, right: 0, bottom: Math.round(el.clientHeight * SHEET_FRACTION), left: 0 };
  }
  return { top: 0, right: Math.min(PANEL_WIDTH, Math.round(el.clientWidth * 0.45)), bottom: 0, left: 0 };
}

/**
 * The landing camera for a project: its tuned camera, zoomed out to fit smaller views,
 * or (until one is tuned) the site's bounds seen from the south at the default pitch.
 */
export function landingCamera(map: MapLibreMap, project: Project, site: Polygon | MultiPolygon, padding: PaddingOptions): Camera {
  const el = map.getContainer();
  const w = Math.max(1, el.clientWidth - (padding.left ?? 0) - (padding.right ?? 0));
  const h = Math.max(1, el.clientHeight - (padding.top ?? 0) - (padding.bottom ?? 0));
  if (project.camera) {
    const fit = Math.log2(Math.min(w / REFERENCE_VIEW.width, h / REFERENCE_VIEW.height));
    return { ...project.camera, zoom: project.camera.zoom + Math.min(0, fit) };
  }
  const [x0, y0, x1, y1] = bboxOf(site);
  const fitted = map.cameraForBounds([x0, y0, x1, y1], { padding: { top: 60, bottom: 60, left: 60, right: 60 } });
  return {
    center: centroidOf(site),
    zoom: (fitted?.zoom ?? 15) - 0.3,
    pitch: DEFAULT_PITCH,
    bearing: 0,
  };
}

function setBoundary(map: MapLibreMap, line: Feature<LineString> | null) {
  const src = map.getSource('project-boundary-draw') as GeoJSONSource | undefined;
  src?.setData({ type: 'FeatureCollection', features: line ? [line] : [] });
}

/** Reduced motion: dip to paper, jump, wait for the map to settle, come back up. */
async function dip(map: MapLibreMap, jump: () => void): Promise<void> {
  const veil = document.createElement('div');
  veil.className = 'dip';
  document.body.appendChild(veil);
  await new Promise((r) => requestAnimationFrame(() => r(null)));
  veil.classList.add('on');
  await new Promise((r) => setTimeout(r, 160));
  jump();
  await Promise.race([new Promise((r) => map.once('idle', () => r(null))), new Promise((r) => setTimeout(r, 1500))]);
  veil.classList.remove('on');
  await new Promise((r) => setTimeout(r, 260));
  veil.remove();
}

/**
 * Fly to a project. Resolves when the camera arrives, or when the viewer interrupts the
 * flight (the boundary is then completed at once). `current` turns false if another
 * flight has started since, and this one must leave the map alone.
 */
export async function flyIn(
  map: MapLibreMap, camera: Camera, padding: PaddingOptions, boundary: Feature<LineString>, current: () => boolean,
): Promise<void> {
  // Stop any flight in progress first: stopping fires its moveend, which must not end this one.
  map.stop();
  if (prefersReducedMotion()) {
    await dip(map, () => map.jumpTo({ ...camera, padding }));
    if (current()) setBoundary(map, boundary);
    return;
  }
  setBoundary(map, null);
  const start = performance.now();
  const onMove = () => {
    if (!current()) return;
    const t = (performance.now() - start) / FLIGHT_MS;
    const drawn = clamp01((t - 0.35) / 0.55);
    if (drawn > 0) setBoundary(map, linePrefix(boundary, easeInOutCubic(drawn)));
  };
  map.on('move', onMove);
  await new Promise<void>((resolve) => {
    map.once('moveend', () => resolve());
    // `essential` keeps MapLibre from skipping the flight; reduced motion is handled above.
    map.flyTo({ ...camera, padding, duration: FLIGHT_MS, curve: 1.42, easing: easeInOutCubic, essential: true });
  });
  map.off('move', onMove);
  if (current()) setBoundary(map, boundary);
}

/** Fly back out to where the viewer was, dropping the panel's padding on the way. */
export async function flyOut(map: MapLibreMap, camera: Camera): Promise<void> {
  map.stop();
  const padding = { top: 0, right: 0, bottom: 0, left: 0 };
  if (prefersReducedMotion()) {
    await dip(map, () => map.jumpTo({ ...camera, padding }));
    return;
  }
  await new Promise<void>((resolve) => {
    map.once('moveend', () => resolve());
    map.flyTo({ ...camera, padding, duration: RETURN_MS, curve: 1.42, easing: easeInOutCubic, essential: true });
  });
}

/** Hide every building that has not been built yet (rise = 0) before the reveal. */
export function lowerMassing(map: MapLibreMap, massing: Massing) {
  for (const f of massing.features) {
    if (f.properties.stage !== 'complete') map.setFeatureState({ source: 'project-massing', id: f.properties.fid! }, { rise: 0 });
  }
}

/**
 * Raise the project's buildings over about 1.2 s, staggered outward from the centre of
 * the site. Returns a function that finishes the animation at once.
 */
export function riseMassing(map: MapLibreMap, massing: Massing, center: [number, number], onDone?: () => void): () => void {
  const items = massing.features
    .filter((f) => f.properties.stage !== 'complete' && f.properties.fid !== undefined)
    .map((f) => ({ id: f.properties.fid!, d: metres(centroidOf(f.geometry), center) }));
  const maxD = Math.max(1, ...items.map((i) => i.d));
  const set = (id: number, v: number) => map.setFeatureState({ source: 'project-massing', id }, { rise: v });
  if (prefersReducedMotion()) {
    items.forEach((i) => set(i.id, 1));
    onDone?.();
    return () => {};
  }
  const start = performance.now();
  let raf = 0;
  let done = false;
  const finish = () => {
    if (done) return;
    done = true;
    cancelAnimationFrame(raf);
    items.forEach((i) => set(i.id, 1));
    onDone?.();
  };
  const frame = () => {
    const now = performance.now() - start;
    let all = true;
    for (const i of items) {
      const t = clamp01((now - (i.d / maxD) * RISE_STAGGER_MS) / RISE_MS);
      if (t < 1) all = false;
      set(i.id, easeOutCubic(t));
    }
    if (all) finish();
    else raf = requestAnimationFrame(frame);
  };
  raf = requestAnimationFrame(frame);
  return finish;
}
