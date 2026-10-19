import type {
  ExpressionSpecification,
  LayerSpecification,
  SourceSpecification,
} from 'maplibre-gl';
import type { Feature, FeatureCollection, Geometry, MultiPolygon, Point, Polygon } from 'geojson';
import { stageColor, STAGE_KEYS, type StageKey, type Theme } from '../theme/theme';
import {
  boundaryLine,
  centroidOf,
  dredgingOf,
  isLineProject,
  lineOf,
  landUseOf,
  MAPPED_PROJECTS,
  markersOf,
  massingOf,
  getProject,
  pointFeature,
  siteOf,
  type Massing,
} from '../projects/data';
import { LAST_DOT_ZOOM, siteWidth } from './handover';

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

/**
 * One point per mapped site (its centroid), for the dots and names. `size` (how wide the site
 * reads, in metres) puts small sites' dots on top and big sites' names first.
 */
function projectPoints(): FeatureCollection<Point> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.flatMap((p) => {
      const at = markersOf(p.id);
      const size = Math.round(siteWidth(p.id));
      return at.map((xy) => pointFeature(xy, { id: p.id, name: p.name, stage: p.stage, size }));
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

/** The dredging-only parts of sites (the Berkeley ferry's channel), drawn apart from the filled site. */
function projectDredging(): FeatureCollection<Polygon | MultiPolygon> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.flatMap((p) =>
      dredgingOf(p.id).map((f) => ({ type: 'Feature' as const, properties: { id: p.id, stage: p.stage }, geometry: f.geometry })),
    ),
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
    // Keyed by project id: the handover (handover.ts) is feature state on both.
    'project-points': { type: 'geojson', data: projectPoints(), promoteId: 'id' },
    'project-sites': { type: 'geojson', data: projectSites(), promoteId: 'id' },
    'project-dredging': { type: 'geojson', data: projectDredging() },
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
  // A proposed site (no approvals yet) is an outline only, dashed, per the stage spec (Matthew, 2026-10-08).
  const proposedSite: ExpressionSpecification = ['==', ['get', 'stage'], 'proposed'];
  const selectedProposed = !!selection && getStage(selection.id) === 'proposed';
  const lineSelected = !!selection && isLineProject(selection.id);
  const exaggeration = theme.map.heightExaggeration;
  // Before landing, buildings that have not risen yet stand at zero height.
  const rise: ExpressionSpecification = ['coalesce', ['feature-state', 'rise'], landed ? 1 : 0];
  const solidHeight: ExpressionSpecification = [
    '*', ['coalesce', ['get', 'podium_ft'], ['get', 'height_ft']], FT * exaggeration,
    ['case', ['==', ['get', 'stage'], 'complete'], 1, rise],
  ];
  // How far each project has gone from dot to site shape (handover.ts): 0 the dot, 1 the shape.
  const shown: ExpressionSpecification = ['coalesce', ['feature-state', 'shown'], 0];
  const dot: ExpressionSpecification = ['-', 1, shown];
  const siteFill = (opacity: number): ExpressionSpecification => ['case', proposedSite, 0, ['*', opacity, shown]];
  const presentStages = selection
    ? [...new Set((massingOf(selection.id)?.features ?? []).map((f) => f.properties.stage))]
    : [];

  const layers: LayerSpecification[] = [
    {
      // A site draws as its own shape once it is big enough on screen (handover.ts): strongly filled
      // while it is small, fading to a tint at street level so the buildings on it show.
      // Also the click target for sites (PROJECT_HIT_LAYERS), so a proposed site stays in it, unfilled.
      id: 'project-site-fill',
      type: 'fill',
      source: 'project-sites',
      filter: othersSites,
      paint: {
        'fill-color': stageCol,
        'fill-opacity': ['interpolate', ['linear'], ['zoom'],
          10, siteFill(theme.opacity.siteFillRegional), 13.5, siteFill(theme.opacity.siteFill)],
      },
    },
    {
      id: 'project-site-outline',
      type: 'line',
      source: 'project-sites',
      filter: ['all', othersSites, ['!', proposedSite]],
      layout: { 'line-join': 'round' },
      paint: {
        'line-color': stageCol,
        'line-width': ['interpolate', ['linear'], ['zoom'], 8, 0.75, 12, 1, 16, 2],
        'line-opacity': shown,
      },
    },
    {
      id: 'project-site-outline-proposed',
      type: 'line',
      source: 'project-sites',
      filter: ['all', othersSites, proposedSite],
      layout: { 'line-join': 'round' },
      paint: {
        'line-color': stageCol,
        'line-width': ['interpolate', ['linear'], ['zoom'], 8, 1, 12, 1.25, 16, 2],
        'line-opacity': shown,
        'line-dasharray': [3, 2],
      },
    },
    {
      // Dredging only, nothing built: a dotted outline and no fill, so a dredged channel doesn't read as
      // built ground. Shown for the selected project too.
      id: 'project-dredging-outline',
      type: 'line',
      source: 'project-dredging',
      minzoom: 11.5,
      filter: hidden.length ? ['!', ['in', ['get', 'id'], ['literal', hidden]]] : ['has', 'id'],
      layout: { 'line-join': 'round', 'line-cap': 'round' },
      paint: {
        'line-color': stageCol,
        'line-width': ['interpolate', ['linear'], ['zoom'], 12, 1.2, 16, 2],
        'line-opacity': ['interpolate', ['linear'], ['zoom'], 11.5, 0, 12.5, 0.85],
        'line-dasharray': [0, 2],
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
      // A proposed site's boundary draws dashed too (butt caps, so the dashes stay crisp).
      layout: {
        'line-join': 'round', 'line-cap': selectedProposed ? 'butt' : 'round', visibility: lineSelected ? 'none' : 'visible',
      },
      paint: {
        'line-color': c.selection, 'line-width': ['interpolate', ['linear'], ['zoom'], 12, 1.5, 17, 2.5],
        ...(selectedProposed ? { 'line-dasharray': [3, 2] } : {}),
      },
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
      // A dot for a site still too small to draw (handover.ts): small and solid, with a thin, hard
      // paper ring (Matthew, 2026-10-13: option D). A proposed project is a hollow ring, as its site
      // is a dashed outline. Small sites' dots sit on top.
      id: 'project-markers',
      type: 'circle',
      source: 'project-points',
      maxzoom: LAST_DOT_ZOOM,
      filter: others,
      layout: { 'circle-sort-key': ['-', 0, ['get', 'size']] },
      paint: {
        'circle-color': ['case', proposedSite, c.land, stageCol],
        'circle-radius': ['interpolate', ['linear'], ['zoom'],
          6, 2.75, 10, 4, 12.5, 5],
        'circle-stroke-color': ['case', proposedSite, stageCol, c.land],
        'circle-stroke-width': ['case', proposedSite, 1.5, 1],
        'circle-opacity': dot,
        'circle-stroke-opacity': dot,
      },
    },
    {
      // Invisible and wider than the dots: an easy target to hover, click and tap.
      id: 'project-marker-hit',
      type: 'circle',
      source: 'project-points',
      maxzoom: LAST_DOT_ZOOM,
      filter: others,
      paint: { 'circle-radius': 11, 'circle-color': c.land, 'circle-opacity': 0 },
    },
    {
      // Names beside the dots and sites, the biggest sites placed first; names that would collide
      // are left out. From the regional view on desktop; a phone's whole-bay view stays unlabelled.
      id: 'project-names',
      type: 'symbol',
      source: 'project-points',
      minzoom: 8.5,
      maxzoom: 15.5,
      filter: others,
      layout: {
        'text-field': ['get', 'name'],
        'text-font': fonts.medium,
        'text-size': ['interpolate', ['linear'], ['zoom'], 8.5, 10.5, 12, 12],
        'text-max-width': 8,
        'text-variable-anchor': ['left', 'right', 'top', 'bottom'],
        'text-radial-offset': 0.7,
        'text-justify': 'auto',
        'symbol-sort-key': ['-', 0, ['get', 'size']],
      },
      paint: { 'text-color': c.labels, 'text-halo-color': c.land, 'text-halo-width': 1.5, 'text-halo-blur': 0.5 },
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
  // The open line's station names draw last, above other projects' markers (Esmeralda's sits on Cloverdale).
  const labels = layers.findIndex((l) => l.id === 'project-line-station-labels');
  return [...layers.slice(0, labels), ...layers.slice(labels + 1), layers[labels]];
}

const lineWidth = (z6: number, z10: number, z15: number): ExpressionSpecification =>
  ['interpolate', ['exponential', 1.6], ['zoom'], 6, z6, 10, z10, 15, z15];

/**
 * Line projects, drawn as a cased line (Matthew, 2026-10-07: option C): a bold stage-coloured
 * line on a land-coloured casing, so it reads over the building print at every zoom. Tunnel
 * runs are a hollow tube; track the project shares with existing service is drawn lighter, and a
 * proposed line (no approvals or funding to build) is dashed, per the stage spec's "outline only
 * (dashed)", as a proposed site's outline is.
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
  // The selected line is drawn by the fly-in until it lands; once landed it stays drawn even if the
  // index filter hides its stage, as an open site does.
  const shown: ExpressionSpecification = landed
    ? ['any', ['==', ['get', 'id'], selectedId], notHidden]
    : ['all', notHidden, ['!=', ['get', 'id'], selectedId]];
  const isLine: ExpressionSpecification = ['==', ['get', 'kind'], 'line'];
  const tunnel: ExpressionSpecification = ['==', ['get', 'segment'], 'tunnel'];
  const proposed: ExpressionSpecification = ['==', ['get', 'stage'], 'proposed'];
  const dash = [2, 1.6];
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
      filter: ['all', shown, isLine, ['!', tunnel], ['!', proposed]], layout: round,
      paint: {
        'line-color': stageCol,
        'line-width': lineWidth(1.3, 2.2, 6),
        'line-opacity': ['case', ['==', ['get', 'segment'], 'shared'], 0.55, 1],
      },
    },
    {
      id: 'project-line-core-proposed', type: 'line', source: 'project-lines',
      filter: ['all', shown, isLine, ['!', tunnel], proposed], layout: { 'line-join': 'round' },
      paint: { 'line-color': stageCol, 'line-width': lineWidth(1.3, 2.2, 6), 'line-dasharray': dash },
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
      id: 'project-line-draw', type: 'line', source: 'project-boundary-draw',
      layout: drawStage === 'proposed' ? { 'line-join': 'round', visibility: lineSelected ? 'visible' : 'none' }
        : { ...round, visibility: lineSelected ? 'visible' : 'none' },
      paint: {
        'line-color': drawColor, 'line-width': lineWidth(1.3, 2.2, 6),
        ...(drawStage === 'proposed' ? { 'line-dasharray': dash } : {}),
      },
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
