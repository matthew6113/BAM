import type { StyleSpecification, LayerSpecification, ExpressionSpecification } from 'maplibre-gl';
import type { Theme } from '../theme/theme';
import {
  CONTEXT_EXTRUSION_MIN_ZOOM,
  DETAIL_MIN_ZOOM,
  GLYPHS_URL,
  LABELS_URL,
  TILE_BASE_URL,
} from './config';

export type ViewMode = '2d' | '3d';

export interface StyleOptions {
  mode: ViewMode;
}

const OSM_CREDIT =
  '<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, ' +
  '<a href="https://overturemaps.org">Overture Maps Foundation</a>';

/** Fontstack names match the glyph folders built by scripts/build-glyphs.mjs. */
export function fontStacks(family: string) {
  return {
    regular: [`${family} Regular`],
    medium: [family === 'Libre Franklin' ? 'Libre Franklin Medium' : `${family} SemiBold`],
    italic: [`${family} Italic`],
  };
}

const visible = (on: boolean) => (on ? 'visible' : 'none') as 'visible' | 'none';

/** Builds the whole MapLibre style from the theme. Every color comes from the theme. */
export function buildStyle(theme: Theme, opts: StyleOptions): StyleSpecification {
  const c = theme.colors;
  const L = theme.layers;
  const fonts = fontStacks(theme.type.mapLabels);
  const w = theme.map.shorelineWidth;
  const showSaltPonds = L.saltPonds;

  const waterFilter: ExpressionSpecification = showSaltPonds
    ? ['==', ['geometry-type'], 'Polygon']
    : ['!=', ['get', 'kind'], 'salt_pond'];

  const shorelineWidth: ExpressionSpecification = [
    'interpolate', ['exponential', 1.4], ['zoom'],
    6, 0.45 * w,
    10, 0.7 * w,
    14, 1.1 * w,
    18, 1.8 * w,
  ];

  const cityLabel = (tier: 1 | 2 | 3, minzoom: number): LayerSpecification => ({
    id: `label-city-${tier}`,
    type: 'symbol',
    source: 'labels',
    minzoom,
    maxzoom: 14.5,
    filter: ['all', ['==', ['get', 'kind'], 'city'], ['==', ['get', 'tier'], tier]],
    layout: {
      visibility: visible(L.labels),
      'text-field': ['get', 'name'],
      'text-font': tier === 1 ? fonts.medium : fonts.regular,
      'text-size': tier === 1
        ? ['interpolate', ['linear'], ['zoom'], 6, 11.5, 9, 14, 12, 15.5]
        : tier === 2
          ? ['interpolate', ['linear'], ['zoom'], 8, 11, 10, 12.5, 13, 13.5]
          : ['interpolate', ['linear'], ['zoom'], 10, 11, 13, 12.5],
      'text-letter-spacing': 0.01,
      'text-max-width': 8,
      'symbol-sort-key': tier,
      'text-padding': 6,
    },
    paint: {
      'text-color': c.labels,
      'text-halo-color': c.land,
      'text-halo-width': 2,
      'text-halo-blur': 0.5,
    },
  });

  const waterLabel = (tier: 1 | 2 | 3, minzoom: number): LayerSpecification => ({
    id: `label-water-${tier}`,
    type: 'symbol',
    source: 'labels',
    minzoom,
    filter: ['all', ['==', ['get', 'kind'], 'water'], ['==', ['get', 'tier'], tier]],
    layout: {
      visibility: visible(L.labels),
      'text-field': ['get', 'name'],
      'text-font': fonts.italic,
      'text-size': tier === 1
        ? ['interpolate', ['linear'], ['zoom'], 6, 11, 9, 13, 12, 15]
        : ['interpolate', ['linear'], ['zoom'], 8, 10.5, 11, 12.5],
      'text-letter-spacing': 0.06,
      'text-max-width': 7,
      'symbol-sort-key': tier,
    },
    paint: {
      'text-color': c.labels,
      'text-halo-color': c.water,
      'text-halo-width': 1.2,
      'text-halo-blur': 0.4,
    },
  });

  const layers: LayerSpecification[] = [
    { id: 'land', type: 'background', paint: { 'background-color': c.land } },
    {
      id: 'outside-region',
      type: 'fill',
      source: 'base',
      'source-layer': 'region_mask',
      layout: { visibility: visible(L.outsideRegion) },
      paint: { 'fill-color': c.outsideRegion, 'fill-antialias': false },
    },
    {
      id: 'water',
      type: 'fill',
      source: 'base',
      'source-layer': 'water',
      filter: waterFilter,
      layout: { visibility: visible(L.water) },
      paint: { 'fill-color': c.water, 'fill-antialias': false },
    },
    {
      id: 'shoreline',
      type: 'line',
      source: 'base',
      'source-layer': 'shoreline',
      filter: showSaltPonds ? ['has', 'kind'] : ['==', ['get', 'kind'], 'shore'],
      layout: { visibility: visible(L.shoreline && L.water), 'line-join': 'round', 'line-cap': 'round' },
      paint: { 'line-color': c.shoreline, 'line-width': shorelineWidth },
    },
    {
      id: 'context-freeway',
      type: 'line',
      source: 'base',
      'source-layer': 'context',
      filter: ['==', ['get', 'kind'], 'freeway'],
      layout: { visibility: visible(L.context), 'line-join': 'round', 'line-cap': 'round' },
      paint: {
        'line-color': c.context,
        'line-width': ['interpolate', ['exponential', 1.5], ['zoom'], 8, 0.5, 12, 1.2, 16, 3],
      },
    },
    {
      id: 'context-rail',
      type: 'line',
      source: 'base',
      'source-layer': 'context',
      filter: ['==', ['get', 'kind'], 'rail'],
      layout: { visibility: visible(L.context), 'line-join': 'round' },
      paint: {
        'line-color': c.context,
        'line-width': ['interpolate', ['linear'], ['zoom'], 9, 0.6, 14, 1.4],
        'line-dasharray': [4, 2],
      },
    },
    {
      id: 'context-ferry',
      type: 'line',
      source: 'base',
      'source-layer': 'context',
      filter: ['==', ['get', 'kind'], 'ferry'],
      layout: { visibility: visible(L.context), 'line-cap': 'round' },
      paint: {
        'line-color': c.shoreline,
        'line-width': ['interpolate', ['linear'], ['zoom'], 9, 0.6, 14, 1.2],
        'line-dasharray': [0.5, 2.5],
      },
    },
    {
      id: 'buildings-overview',
      type: 'fill',
      source: 'buildings-overview',
      'source-layer': 'buildings',
      maxzoom: DETAIL_MIN_ZOOM,
      layout: { visibility: visible(L.buildings) },
      paint: {
        'fill-color': c.buildings,
        // Lighter at regional zoom so density reads as tone; full ink from street level.
        'fill-opacity': [
          'interpolate', ['linear'], ['zoom'],
          8, theme.opacity.buildingsRegional,
          DETAIL_MIN_ZOOM, theme.opacity.buildings,
        ],
      },
    },
    {
      id: 'buildings',
      type: 'fill',
      source: 'buildings-detail',
      'source-layer': 'buildings',
      minzoom: DETAIL_MIN_ZOOM,
      layout: { visibility: visible(L.buildings) },
      paint: { 'fill-color': c.buildings, 'fill-opacity': theme.opacity.buildings },
    },
    {
      // Faint context massing for buildings with a mapped or measured height (3D mode only).
      id: 'buildings-context-3d',
      type: 'fill-extrusion',
      source: 'buildings-detail',
      'source-layer': 'buildings',
      minzoom: CONTEXT_EXTRUSION_MIN_ZOOM,
      filter: ['has', 'h'],
      layout: { visibility: visible(L.buildings && opts.mode === '3d') },
      paint: {
        'fill-extrusion-color': c.contextExtrusion,
        'fill-extrusion-height': ['*', ['get', 'h'], theme.map.heightExaggeration],
        'fill-extrusion-base': 0,
        'fill-extrusion-opacity': [
          'interpolate', ['linear'], ['zoom'],
          CONTEXT_EXTRUSION_MIN_ZOOM, 0,
          CONTEXT_EXTRUSION_MIN_ZOOM + 1, theme.opacity.contextExtrusion,
        ],
        'fill-extrusion-vertical-gradient': true,
      },
    },
    waterLabel(1, 6),
    waterLabel(2, 7.8),
    waterLabel(3, 10),
    cityLabel(1, 6),
    cityLabel(2, 8.4),
    cityLabel(3, 10),
  ];

  const overview = L.overview === 'light' ? 'buildings-overview-light' : 'buildings-overview-all';

  return {
    version: 8,
    name: `Bay Area megaprojects (${theme.name})`,
    glyphs: GLYPHS_URL,
    light: {
      anchor: 'map',
      color: theme.map.light.color,
      intensity: theme.map.light.intensity,
      position: [1.15, theme.map.light.azimuth, theme.map.light.polar],
    },
    sources: {
      base: { type: 'vector', url: `pmtiles://${TILE_BASE_URL}/base.pmtiles`, attribution: OSM_CREDIT },
      'buildings-overview': {
        type: 'vector',
        url: `pmtiles://${TILE_BASE_URL}/${overview}.pmtiles`,
        attribution: OSM_CREDIT,
      },
      'buildings-detail': {
        type: 'vector',
        url: `pmtiles://${TILE_BASE_URL}/buildings-detail.pmtiles`,
        attribution: OSM_CREDIT,
      },
      labels: { type: 'geojson', data: LABELS_URL },
    },
    layers,
  };
}
