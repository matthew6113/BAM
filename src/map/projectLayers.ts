import type {
  ExpressionSpecification,
  LayerSpecification,
  SourceSpecification,
} from 'maplibre-gl';
import type { Feature, FeatureCollection, Geometry, MultiPolygon, Point, Polygon } from 'geojson';
import { stageColor, STAGE_KEYS, type StageKey, type Theme } from '../theme/theme';
import {
  alignmentMidpoint,
  boundaryLine,
  centroidOf,
  isLineProject,
  lineOf,
  landUseOf,
  MAPPED_PROJECTS,
  massingOf,
  getProject,
  pointFeature,
  siteOf,
  type Massing,
} from '../projects/data';

export const FT = 0.3048;
/** Surrounding buildings extrude faintly within this distance of the selected site. */
export const CONTEXT_RADIUS_M = 700;

/** Where the selected project is in the fly-in. */
export type FlightPhase = 'flying' | 'landed';

export interface Selection {
  id: string;
  phase: FlightPhase;
}

const getStage = (id: string) => getProject(id)?.stage;

const EMPTY: FeatureCollection = { type: 'FeatureCollection', features: [] };

/** One point per mapped project (site centroid), for the regional markers. */
function projectPoints(): FeatureCollection<Point> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.map((p) => {
      const site = siteOf(p.id)!;
      // A line's marker sits on the line, not at the middle of its corridor.
      const at = alignmentMidpoint(p.id) ?? centroidOf(site.geometry);
      return pointFeature(at, { id: p.id, name: p.name, stage: p.stage });
    }),
  };
}

function projectSites(): FeatureCollection<Polygon | MultiPolygon> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.map((p) => {
      const site = siteOf(p.id)!;
      return {
        type: 'Feature',
        properties: { id: p.id, name: p.name, stage: p.stage, line: isLineProject(p.id) },
        geometry: site.geometry,
      };
    }),
  };
}

/** Every mapped line project's alignment and stations, tagged with the project's id, name and stage. */
function projectLines(): FeatureCollection<Geometry> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.flatMap((p) =>
      (lineOf(p.id)?.features ?? []).map((f) => ({
        ...f,
        properties: { ...f.properties, label: f.properties.name, id: p.id, name: p.name, stage: p.stage },
      })),
    ),
  };
}

/** Labels for landmarks in the selected project's massing (sparse by design). */
function massingLabels(m: Massing | undefined): FeatureCollection<Point> {
  if (!m) return EMPTY as FeatureCollection<Point>;
  return {
    type: 'FeatureCollection',
    features: m.features
      .filter((f) => f.properties.kind === 'landmark')
      .map((f) => pointFeature(centroidOf(f.geometry), {
        label: f.properties.label,
        // Left out when unknown, so the label shows the name alone.
        ...(f.properties.height_ft != null ? { height_ft: f.properties.height_ft } : {}),
      })),
  };
}

export function stageColorExpression(theme: Theme): ExpressionSpecification {
  const pairs = STAGE_KEYS.flatMap((s) => [s, stageColor(theme, s)]);
  return ['match', ['get', 'stage'], ...pairs, theme.colors.buildings] as unknown as ExpressionSpecification;
}

export function landUseColorExpression(theme: Theme): ExpressionSpecification {
  const pairs = Object.entries(theme.landUse.colors).flat();
  return ['match', ['get', 'category'], ...pairs, theme.landUse.colors.other] as unknown as ExpressionSpecification;
}

export function projectSources(selection: Selection | null): Record<string, SourceSpecification> {
  const massing = selection ? massingOf(selection.id) : undefined;
  const landUse = selection ? landUseOf(selection.id) : undefined;
  const site = selection ? siteOf(selection.id) : undefined;
  // A landed line project is drawn by its own layers, so the drawing line clears.
  const drawn = selection?.phase === 'landed' && site && !isLineProject(selection.id) ? boundaryLine(site.geometry) : undefined;
  return {
    'project-points': { type: 'geojson', data: projectPoints() },
    'project-sites': { type: 'geojson', data: projectSites() },
    'project-lines': { type: 'geojson', data: projectLines() },
    // Filled by the fly-in as the camera approaches; complete once landed.
    'project-boundary-draw': { type: 'geojson', data: drawn ? { type: 'FeatureCollection', features: [drawn] } : EMPTY },
    // Plan-scale projects: the adopted plan's land-use zones, flat on the ground.
    'project-landuse': { type: 'geojson', data: (landUse ?? EMPTY) as FeatureCollection },
    'project-massing': { type: 'geojson', data: (massing ?? EMPTY) as FeatureCollection, promoteId: 'fid' },
    'project-massing-labels': { type: 'geojson', data: massingLabels(massing) },
  };
}

/** Filter for context buildings: near the selected site, but not on it. */
export function contextFilter(selection: Selection | null): ExpressionSpecification {
  const site = selection ? siteOf(selection.id) : undefined;
  // A line's corridor runs for miles: its surroundings get the same faint context as the region.
  if (!site || isLineProject(selection!.id)) return ['has', 'h'];
  // ['distance', GeoJSON] measures metres from each building to the site polygon.
  return [
    'all',
    ['has', 'h'],
    ['>', ['distance', site.geometry], 1],
    ['<', ['distance', site.geometry], CONTEXT_RADIUS_M],
  ] as unknown as ExpressionSpecification;
}

/** Project layers drawn under the place labels. */
export function projectLayers(
  theme: Theme,
  selection: Selection | null,
  fonts: { medium: string[]; regular: string[] },
  hidden: string[] = [],
): LayerSpecification[] {
  const c = theme.colors;
  const stageCol = stageColorExpression(theme);
  const selectedId = selection?.id ?? '';
  // Every other project, unless the index filter hides it.
  const others: ExpressionSpecification = hidden.length
    ? ['all', ['!=', ['get', 'id'], selectedId], ['!', ['in', ['get', 'id'], ['literal', hidden]]]]
    : ['!=', ['get', 'id'], selectedId];
  const landed = selection?.phase === 'landed';
  // Line projects draw their alignment instead of a site.
  const othersSites: ExpressionSpecification = ['all', others, ['!', ['get', 'line']]];
  const lineSelected = !!selection && isLineProject(selection.id);
  const exaggeration = theme.map.heightExaggeration;
  // Before landing, buildings that have not risen yet stand at zero height.
  const rise: ExpressionSpecification = ['coalesce', ['feature-state', 'rise'], landed ? 1 : 0];
  const solidHeight: ExpressionSpecification = [
    '*', ['coalesce', ['get', 'podium_ft'], ['get', 'height_ft']], FT * exaggeration,
    ['case', ['==', ['get', 'stage'], 'complete'], 1, rise],
  ];
  const presentStages = selection
    ? [...new Set((massingOf(selection.id)?.features ?? []).map((f) => f.properties.stage))]
    : [];

  const layers: LayerSpecification[] = [
    {
      id: 'project-site-fill',
      type: 'fill',
      source: 'project-sites',
      minzoom: 11.5,
      filter: othersSites,
      paint: {
        'fill-color': stageCol,
        'fill-opacity': ['interpolate', ['linear'], ['zoom'], 11.5, 0, 12.5, theme.opacity.siteFill],
      },
    },
    {
      id: 'project-site-outline',
      type: 'line',
      source: 'project-sites',
      minzoom: 11.5,
      filter: othersSites,
      layout: { 'line-join': 'round' },
      paint: {
        'line-color': stageCol,
        'line-width': ['interpolate', ['linear'], ['zoom'], 12, 1, 16, 2],
        'line-opacity': ['interpolate', ['linear'], ['zoom'], 11.5, 0, 12.5, 1],
      },
    },
    {
      // Land-use zones fade in once the camera has landed: zones, not buildings.
      id: 'project-landuse-fill',
      type: 'fill',
      source: 'project-landuse',
      paint: {
        'fill-color': landUseColorExpression(theme),
        'fill-opacity': landed ? theme.landUse.opacity : 0,
        'fill-opacity-transition': { duration: 600, delay: 0 },
      },
    },
    {
      id: 'project-landuse-outline',
      type: 'line',
      source: 'project-landuse',
      paint: {
        'line-color': c.land,
        'line-width': ['interpolate', ['linear'], ['zoom'], 12, 0.5, 16, 1.5],
        'line-opacity': landed ? 1 : 0,
      },
    },
    {
      id: 'project-boundary-draw',
      type: 'line',
      source: 'project-boundary-draw',
      layout: { 'line-join': 'round', 'line-cap': 'round', visibility: lineSelected ? 'none' : 'visible' },
      paint: { 'line-color': c.selection, 'line-width': ['interpolate', ['linear'], ['zoom'], 12, 1.5, 17, 2.5] },
    },
    ...lineLayers(theme, selection, fonts, hidden),
    // Massing: one extrusion layer per stage, so each stage gets its own solidity.
    ...presentStages
      .filter((s) => s !== undefined)
      .map((stage): LayerSpecification => ({
        id: `project-massing-${stage}`,
        type: 'fill-extrusion',
        source: 'project-massing',
        filter: ['all', ['==', ['get', 'stage'], stage], ['>', ['coalesce', ['get', 'height_ft'], 0], 0]],
        paint: {
          'fill-extrusion-color': stageColor(theme, stage as StageKey),
          'fill-extrusion-height': solidHeight,
          'fill-extrusion-base': 0,
          'fill-extrusion-opacity': theme.massing.opacity[stage as StageKey] ?? 0.8,
          'fill-extrusion-vertical-gradient': true,
        },
      })),
    {
      // The upper height limit above a podium: allowed, not designed. Drawn as a faint envelope.
      id: 'project-massing-envelope',
      type: 'fill-extrusion',
      source: 'project-massing',
      filter: ['>', ['coalesce', ['get', 'podium_ft'], 0], 0],
      paint: {
        'fill-extrusion-color': stageCol,
        'fill-extrusion-base': ['*', ['get', 'podium_ft'], FT * exaggeration, rise],
        'fill-extrusion-height': ['*', ['get', 'height_ft'], FT * exaggeration, rise],
        'fill-extrusion-opacity': theme.opacity.massingEnvelope,
        'fill-extrusion-vertical-gradient': false,
      },
    },
    {
      // Blocks without a height in the source are outlined on the ground only.
      id: 'project-massing-outline',
      type: 'line',
      source: 'project-massing',
      filter: ['all', ['==', ['get', 'kind'], 'block'], ['==', ['coalesce', ['get', 'height_ft'], -1], -1]],
      paint: { 'line-color': stageCol, 'line-width': 1.5, 'line-dasharray': [3, 2] },
    },
    {
      id: 'project-markers',
      type: 'circle',
      source: 'project-points',
      maxzoom: 13,
      filter: others,
      paint: {
        'circle-color': stageCol,
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 4, 10, 6, 12.5, 7],
        'circle-stroke-color': c.land,
        'circle-stroke-width': 1.5,
        'circle-opacity': ['interpolate', ['linear'], ['zoom'], 12, 1, 13, 0],
        'circle-stroke-opacity': ['interpolate', ['linear'], ['zoom'], 12, 1, 13, 0],
      },
    },
    {
      id: 'project-names',
      type: 'symbol',
      source: 'project-points',
      minzoom: 12,
      maxzoom: 15.5,
      filter: others,
      layout: {
        'text-field': ['get', 'name'],
        'text-font': fonts.medium,
        'text-size': 12,
        'text-max-width': 9,
      },
      paint: { 'text-color': c.labels, 'text-halo-color': c.land, 'text-halo-width': 2, 'text-halo-blur': 0.5 },
    },
    {
      id: 'project-massing-labels',
      type: 'symbol',
      source: 'project-massing-labels',
      layout: {
        'text-field': ['case', ['has', 'height_ft'],
          ['concat', ['get', 'label'], ', ', ['to-string', ['get', 'height_ft']], ' ft'], ['get', 'label']],
        'text-font': fonts.regular,
        'text-size': 11.5,
        // Beside the base, not on it: a tall landmark covers anything placed above its foot.
        'text-offset': [0.9, 0],
        'text-anchor': 'left',
        visibility: landed ? 'visible' : 'none',
      },
      paint: { 'text-color': c.labels, 'text-halo-color': c.land, 'text-halo-width': 1.8 },
    },
  ];
  return layers;
}

const lineWidth = (z6: number, z10: number, z15: number): ExpressionSpecification =>
  ['interpolate', ['exponential', 1.6], ['zoom'], 6, z6, 10, z10, 15, z15];

/**
 * Line projects, drawn as a cased line (Matthew, 2026-10-07: option C): a bold stage-coloured
 * line on a land-coloured casing, so it reads over the building print at every zoom. Tunnel
 * runs are a hollow tube; track the project shares with existing service is drawn lighter.
 * While the camera flies in, the selected line draws itself (as a site's boundary does).
 */
function lineLayers(
  theme: Theme,
  selection: Selection | null,
  fonts: { medium: string[]; regular: string[] },
  hidden: string[],
): LayerSpecification[] {
  const c = theme.colors;
  const stageCol = stageColorExpression(theme);
  const selectedId = selection?.id ?? '';
  const landed = selection?.phase === 'landed';
  const notHidden: ExpressionSpecification = hidden.length ? ['!', ['in', ['get', 'id'], ['literal', hidden]]] : true as never;
  // The selected line is drawn by the fly-in until it lands.
  const shown: ExpressionSpecification = landed ? notHidden : ['all', notHidden, ['!=', ['get', 'id'], selectedId]];
  const isLine: ExpressionSpecification = ['==', ['get', 'kind'], 'line'];
  const tunnel: ExpressionSpecification = ['==', ['get', 'segment'], 'tunnel'];
  const drawStage = selection ? (getStage(selection.id) as StageKey | undefined) : undefined;
  const drawColor = drawStage ? stageColor(theme, drawStage) : c.selection;
  const lineSelected = !!selection && isLineProject(selection.id);
  const round = { 'line-join': 'round', 'line-cap': 'round' } as const;
  return [
    {
      id: 'project-line-casing', type: 'line', source: 'project-lines',
      filter: ['all', shown, isLine], layout: round,
      paint: { 'line-color': c.land, 'line-width': lineWidth(2.6, 4.5, 11) },
    },
    {
      id: 'project-line-core', type: 'line', source: 'project-lines',
      filter: ['all', shown, isLine, ['!', tunnel]], layout: round,
      paint: {
        'line-color': stageCol,
        'line-width': lineWidth(1.3, 2.2, 6),
        'line-opacity': ['case', ['==', ['get', 'segment'], 'shared'], 0.55, 1],
      },
    },
    {
      id: 'project-line-tube', type: 'line', source: 'project-lines',
      filter: ['all', shown, isLine, tunnel], layout: round,
      paint: { 'line-color': stageCol, 'line-width': lineWidth(1.8, 3, 9) },
    },
    {
      id: 'project-line-tube-hollow', type: 'line', source: 'project-lines',
      filter: ['all', shown, isLine, tunnel], layout: round,
      paint: { 'line-color': c.land, 'line-width': lineWidth(0.6, 1.2, 4.5) },
    },
    {
      // Drawn by the fly-in: the selected line, growing along its length.
      id: 'project-line-draw-casing', type: 'line', source: 'project-boundary-draw', layout: { ...round, visibility: lineSelected ? 'visible' : 'none' },
      paint: { 'line-color': c.land, 'line-width': lineWidth(2.6, 4.5, 11) },
    },
    {
      id: 'project-line-draw', type: 'line', source: 'project-boundary-draw', layout: { ...round, visibility: lineSelected ? 'visible' : 'none' },
      paint: { 'line-color': drawColor, 'line-width': lineWidth(1.3, 2.2, 6) },
    },
    {
      id: 'project-line-stations', type: 'circle', source: 'project-lines', minzoom: 9,
      filter: ['all', shown, ['==', ['get', 'kind'], 'station']],
      paint: {
        'circle-color': ['case', ['==', ['get', 'status'], 'existing'], c.land, stageCol],
        'circle-radius': lineWidth(1.5, 3, 8),
        'circle-stroke-color': ['case', ['==', ['get', 'status'], 'existing'], stageCol, c.land],
        'circle-stroke-width': lineWidth(0.8, 1.2, 2.5),
      },
    },
    {
      // Stations are named only on the open project: labels stay sparse.
      id: 'project-line-station-labels', type: 'symbol', source: 'project-lines', minzoom: 10.5,
      filter: ['all', ['==', ['get', 'kind'], 'station'], ['==', ['get', 'id'], landed ? selectedId : '']],
      layout: {
        'text-field': ['get', 'label'], 'text-font': fonts.medium, 'text-size': 12,
        'text-offset': [0, 0.9], 'text-anchor': 'top', 'text-max-width': 9,
      },
      paint: { 'text-color': c.labels, 'text-halo-color': c.land, 'text-halo-width': 2, 'text-halo-blur': 0.5 },
    },
    {
      // Wide and invisible: makes a thin line easy to hover and click.
      id: 'project-line-hit', type: 'line', source: 'project-lines',
      filter: ['all', ['!=', ['get', 'id'], selectedId], notHidden, isLine], layout: round,
      paint: { 'line-color': c.land, 'line-opacity': 0, 'line-width': 16 },
    },
  ] as LayerSpecification[];
}

export type { Feature };
