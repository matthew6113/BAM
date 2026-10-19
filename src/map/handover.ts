import type { Map as MapLibreMap } from 'maplibre-gl';
import { areaOf, centroidOf, isLineProject, MAPPED_PROJECTS, siteOf } from '../projects/data';

/**
 * Each project is a dot until its site is big enough on screen to draw as its own shape, then the
 * shape takes over (Matthew, 2026-10-13: option D). Big sites draw as shapes from the regional view;
 * small ones stay dots until street level.
 */

/** A site takes over from its dot once it is about this wide on screen (the side of a square of its area). */
export const HANDOVER_PX = 18;
/** Dots end here (the marker layer's maxzoom): every site is drawn by then. */
export const LAST_DOT_ZOOM = 13;
/** The swap is a short fade in time (instant with reduced motion), so a still map never shows a site half drawn. */
const FADE_MS = 200;

/** How wide a site reads, in metres: the side of a square of its area. */
export function siteWidth(id: string): number {
  const site = siteOf(id);
  if (!site) return 0;
  return Math.sqrt(areaOf(site.geometry));
}

/** The zoom at which a project's site is HANDOVER_PX across (512-px tiles), at the latest LAST_DOT_ZOOM. */
export function handoverZoom(id: string): number {
  const site = siteOf(id);
  const width = siteWidth(id);
  if (!site || !width) return LAST_DOT_ZOOM;
  const lat = centroidOf(site.geometry)[1];
  const metresPerPxAtZ0 = (2 * Math.PI * 6378137 * Math.cos(lat * (Math.PI / 180))) / 512;
  return Math.min(LAST_DOT_ZOOM, Math.log2((HANDOVER_PX * metresPerPxAtZ0) / width));
}

/** Whether a project is drawn as its site's shape at this zoom (1) or as a dot (0). */
export function handover(at: number, zoom: number): 0 | 1 {
  return zoom >= at ? 1 : 0;
}

// Line projects have no site shape or dot: the line is drawn at every zoom.
const AT = MAPPED_PROJECTS.filter((p) => !isLineProject(p.id)).map((p) => ({ id: p.id, at: handoverZoom(p.id) }));

/**
 * Keep every project's handover in step with the camera, as feature state (`shown`, 0 the dot, 1 the
 * shape) on its site and dots. Per-feature zoom values in a style expression are only sampled at
 * whole zoom levels, which leaves sites half drawn between them; the camera's own zoom keeps each
 * swap clean.
 */
export function trackHandover(map: MapLibreMap): () => void {
  const goal = new Map<string, number>();
  const drawn = new Map<string, number>();
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  let before = 0;
  const draw = (id: string, shown: number) => {
    drawn.set(id, shown);
    map.setFeatureState({ source: 'project-sites', id }, { shown });
    map.setFeatureState({ source: 'project-points', id }, { shown });
  };
  const fade = (now: number) => {
    const step = (before ? now - before : 16) / FADE_MS;
    before = now;
    frame = 0;
    for (const [id, to] of goal) {
      const from = drawn.get(id) ?? to;
      if (from !== to) draw(id, to > from ? Math.min(to, from + step) : Math.max(to, from - step));
    }
    if ([...goal].some(([id, to]) => drawn.get(id) !== to)) frame = requestAnimationFrame(fade);
    else before = 0;
  };
  const update = (instant: boolean) => {
    if (!map.getSource('project-sites') || !map.getSource('project-points')) return;
    const zoom = map.getZoom();
    for (const { id, at } of AT) {
      const to = handover(at, zoom);
      if (!instant && goal.get(id) === to) continue;
      goal.set(id, to);
      if (instant || reduce.matches || !drawn.has(id)) draw(id, to);
    }
    if (!frame && [...goal].some(([id, to]) => drawn.get(id) !== to)) frame = requestAnimationFrame(fade);
  };
  const zoomed = () => update(false);
  // A restyle can replace the sources, and their state with them.
  const restyled = () => update(true);
  map.on('zoom', zoomed);
  map.on('styledata', restyled);
  update(true);
  return () => {
    cancelAnimationFrame(frame);
    map.off('zoom', zoomed);
    map.off('styledata', restyled);
  };
}
