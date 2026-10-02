import region from '../generated/region.json';
import projects from '../../data/projects.json';

/** Absolute URL of the site root, including the base path on GitHub Pages (/BAM/). */
const SITE = `${location.origin}${import.meta.env.BASE_URL}`;

/** Where the PMTiles archives live. Defaults to the site itself; set VITE_TILE_BASE_URL for object storage. */
export const TILE_BASE_URL: string =
  (import.meta.env.VITE_TILE_BASE_URL as string | undefined) ?? `${SITE}generated/tiles`;

export const GLYPHS_URL = `${SITE}generated/glyphs/{fontstack}/{range}.pbf`;
export const LABELS_URL = `${SITE}generated/data/labels.geojson`;

export const OVERTURE_RELEASE = region.overtureRelease;

/** The nine counties' land extent, from Overture divisions (see pipeline). */
export const EXTENT = region.extent as [number, number, number, number];

/** Panning stops a little beyond the nine counties. */
export const MAX_BOUNDS = region.maxBounds as [number, number, number, number];

/**
 * The default "whole Bay" frame fits every project's approximate center, not the
 * nine counties: framing the counties leaves the projects in about 6% of the screen.
 * approxCenter is only used to frame the view; no project is drawn in M1.
 */
export const HOME_BOUNDS: [number, number, number, number] = (() => {
  const xs = projects.projects.map((p) => p.approxCenter[0]);
  const ys = projects.projects.map((p) => p.approxCenter[1]);
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
})();

export const MIN_ZOOM = 6;
export const MAX_ZOOM = 18;
/** Overview building tiles cover z6-z12; detail tiles (with heights) take over at z13. */
export const DETAIL_MIN_ZOOM = 13;
export const DETAIL_MAX_ZOOM = 15;
/** One detail archive per zoom keeps every file under 100 MB. */
export const DETAIL_ZOOMS = [13, 14, 15] as const;
/** Existing buildings extrude (faintly) only this close in, and only in 3D mode. */
export const CONTEXT_EXTRUSION_MIN_ZOOM = 14;
