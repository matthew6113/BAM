import type { Feature, FeatureCollection, Geometry, LineString, MultiPolygon, Point, Polygon } from 'geojson';
import data from '../../data/projects.json';
import type { StageKey } from '../theme/theme';

export type Project = (typeof data.projects)[number] & {
  camera?: { center: [number, number]; zoom: number; pitch: number; bearing: number };
};
export type Stage = (typeof data.stages)[number];

export const STAGES: Stage[] = data.stages;
export const PROJECTS: Project[] = data.projects as Project[];
export const DATA_LAST_VERIFIED: string = data._meta.lastVerified;

export interface MassingProps {
  fid?: number;
  kind: 'block' | 'landmark' | 'building';
  block?: string;
  label: string;
  stage: StageKey;
  height_ft: number | null;
  podium_ft?: number | null;
  base_ft: number;
  illustrative: boolean;
  source: string;
  note?: string;
}

export interface BoundaryProps {
  kind: 'site' | 'sub-area';
  name: string;
}

type Collection<G extends Geometry, P> = FeatureCollection<G, P> & { properties?: Record<string, unknown> };
export type Boundary = Collection<Polygon | MultiPolygon, BoundaryProps>;
export type Massing = Collection<Polygon | MultiPolygon, MassingProps>;

// Traced project geometry lives in data/ (committed, with its sources) and is bundled.
const boundaryFiles = import.meta.glob('../../data/boundaries/*.geojson', { query: '?raw', import: 'default', eager: true });
const massingFiles = import.meta.glob('../../data/massing/*.geojson', { query: '?raw', import: 'default', eager: true });

function byId<T>(files: Record<string, unknown>): Map<string, T> {
  const out = new Map<string, T>();
  for (const [path, raw] of Object.entries(files)) {
    const id = path.split('/').pop()!.replace('.geojson', '');
    out.set(id, JSON.parse(raw as string) as T);
  }
  return out;
}

const BOUNDARIES = byId<Boundary>(boundaryFiles);
const MASSING = byId<Massing>(massingFiles);

/** Projects drawn on the map: those with a traced boundary (Potrero only, in Milestone 2). */
export const MAPPED_PROJECTS: Project[] = PROJECTS.filter((p) => BOUNDARIES.has(p.id));

export function getProject(id: string): Project | undefined {
  return PROJECTS.find((p) => p.id === id);
}

export function boundaryOf(id: string): Boundary | undefined {
  return BOUNDARIES.get(id);
}

export function siteOf(id: string): Feature<Polygon | MultiPolygon, BoundaryProps> | undefined {
  return BOUNDARIES.get(id)?.features.find((f) => f.properties.kind === 'site');
}

/** Massing with a numeric feature id per building, for feature-state animation. */
export function massingOf(id: string): Massing | undefined {
  const m = MASSING.get(id);
  if (!m) return undefined;
  return { ...m, features: m.features.map((f, i) => ({ ...f, properties: { ...f.properties, fid: i + 1 } })) };
}

export function stageLabel(key: string): string {
  return STAGES.find((s) => s.key === key)?.label ?? key;
}

// ---------------------------------------------------------------- geometry helpers

type Ring = [number, number][];

function outerRings(g: Polygon | MultiPolygon): Ring[] {
  return g.type === 'Polygon' ? [g.coordinates[0] as Ring] : g.coordinates.map((p) => p[0] as Ring);
}

export function bboxOf(g: Polygon | MultiPolygon): [number, number, number, number] {
  let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity];
  for (const ring of outerRings(g)) {
    for (const [x, y] of ring) {
      x0 = Math.min(x0, x);
      y0 = Math.min(y0, y);
      x1 = Math.max(x1, x);
      y1 = Math.max(y1, y);
    }
  }
  return [x0, y0, x1, y1];
}

/** Area-weighted centroid of the outer rings (good enough for labels and staggering). */
export function centroidOf(g: Polygon | MultiPolygon): [number, number] {
  // Work relative to a nearby origin: with raw longitudes, the shoelace terms for a
  // building-sized ring cancel badly in floating point.
  const [ox, oy] = outerRings(g)[0][0];
  let a = 0;
  let cx = 0;
  let cy = 0;
  for (const ring of outerRings(g)) {
    for (let i = 0; i < ring.length - 1; i++) {
      const x0 = ring[i][0] - ox;
      const y0 = ring[i][1] - oy;
      const x1 = ring[i + 1][0] - ox;
      const y1 = ring[i + 1][1] - oy;
      const f = x0 * y1 - x1 * y0;
      a += f;
      cx += (x0 + x1) * f;
      cy += (y0 + y1) * f;
    }
  }
  if (a === 0) {
    const [bx0, by0, bx1, by1] = bboxOf(g);
    return [(bx0 + bx1) / 2, (by0 + by1) / 2];
  }
  return [ox + cx / (3 * a), oy + cy / (3 * a)];
}

/** Ground distance in metres (equirectangular; fine at site scale). */
export function metres(a: [number, number], b: [number, number]): number {
  const k = Math.cos(((a[1] + b[1]) / 2) * (Math.PI / 180)) * 111320;
  return Math.hypot((a[0] - b[0]) * k, (a[1] - b[1]) * 110540);
}

/** The site's outer boundary as a line, for the drawing animation. */
export function boundaryLine(g: Polygon | MultiPolygon): Feature<LineString> {
  const ring = outerRings(g).sort((r1, r2) => r2.length - r1.length)[0];
  return { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: ring } };
}

/** The first `t` (0 to 1) of a line, by length. */
export function linePrefix(line: Feature<LineString>, t: number): Feature<LineString> {
  const c = line.geometry.coordinates as [number, number][];
  if (t >= 1) return line;
  const seg = c.slice(1).map((p, i) => metres(c[i], p));
  const total = seg.reduce((s, d) => s + d, 0);
  let left = Math.max(0, t) * total;
  const out: [number, number][] = [c[0]];
  for (let i = 0; i < seg.length; i++) {
    if (left >= seg[i]) {
      out.push(c[i + 1]);
      left -= seg[i];
      continue;
    }
    const f = seg[i] === 0 ? 0 : left / seg[i];
    out.push([c[i][0] + (c[i + 1][0] - c[i][0]) * f, c[i][1] + (c[i + 1][1] - c[i][1]) * f]);
    break;
  }
  if (out.length < 2) out.push(c[0]);
  return { ...line, geometry: { type: 'LineString', coordinates: out } };
}

export function pointFeature(coords: [number, number], props: Record<string, unknown>): Feature<Point> {
  return { type: 'Feature', properties: props, geometry: { type: 'Point', coordinates: coords } };
}
