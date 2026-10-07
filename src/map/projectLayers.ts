import type {
  ExpressionSpecification,
  LayerSpecification,
  SourceSpecification,
} from 'maplibre-gl';
import type { Feature, FeatureCollection, MultiPolygon, Point, Polygon } from 'geojson';
import { stageColor, STAGE_KEYS, type StageKey, type Theme } from '../theme/theme';
import {
  boundaryLine,
  centroidOf,
  landUseOf,
  MAPPED_PROJECTS,
  massingOf,
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

const EMPTY: FeatureCollection = { type: 'FeatureCollection', features: [] };

/** One point per mapped project (site centroid), for the regional markers. */
function projectPoints(): FeatureCollection<Point> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.map((p) => {
      const site = siteOf(p.id)!;
      return pointFeature(centroidOf(site.geometry), { id: p.id, name: p.name, stage: p.stage });
    }),
  };
}

function projectSites(): FeatureCollection<Polygon | MultiPolygon> {
  return {
    type: 'FeatureCollection',
    features: MAPPED_PROJECTS.map((p) => {
      const site = siteOf(p.id)!;
      return { type: 'Feature', properties: { id: p.id, name: p.name, stage: p.stage }, geometry: site.geometry };
    }),
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
  const drawn = selection?.phase === 'landed' && site ? boundaryLine(site.geometry) : undefined;
  return {
    'project-points': { type: 'geojson', data: projectPoints() },
    'project-sites': { type: 'geojson', data: projectSites() },
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
  if (!site) return ['has', 'h'];
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
      filter: others,
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
      filter: others,
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
      layout: { 'line-join': 'round', 'line-cap': 'round' },
      paint: { 'line-color': c.selection, 'line-width': ['interpolate', ['linear'], ['zoom'], 12, 1.5, 17, 2.5] },
    },
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
      // A soft land-colored halo that clears the building ink around each dot.
      id: 'project-marker-halos',
      type: 'circle',
      source: 'project-points',
      maxzoom: 13,
      filter: others,
      paint: {
        'circle-color': c.land,
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 10, 10, 15, 12.5, 17],
        'circle-blur': 0.35,
        'circle-opacity': ['interpolate', ['linear'], ['zoom'], 12, 1, 13, 0],
      },
    },
    {
      id: 'project-markers',
      type: 'circle',
      source: 'project-points',
      maxzoom: 13,
      filter: others,
      paint: {
        'circle-color': stageCol,
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 5, 10, 7.5, 12.5, 8.5],
        'circle-stroke-color': c.land,
        'circle-stroke-width': 2,
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

export type { Feature };
