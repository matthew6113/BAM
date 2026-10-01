import region from '../generated/region.json';
import projects from '../../data/projects.json';

/** Where the PMTiles archives live. Defaults to the dev server; set VITE_TILE_BASE_URL for object storage. */
export const TILE_BASE_URL: string =
  (import.meta.env.VITE_TILE_BASE_URL as string | undefined) ?? `${location.origin}/generated/tiles`;

export const GLYPHS_URL = `${location.origin}/generated/glyphs/{fontstack}/{range}.pbf`;
export const LABELS_URL = `${location.origin}/generated/data/labels.geojson`;

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
/** Existing buildings extrude (faintly) only this close in, and only in 3D mode. */
export const CONTEXT_EXTRUSION_MIN_ZOOM = 14;
