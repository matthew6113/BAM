/**
 * Line-project style mockups (dev only, Oct 2026). Not real project data: the HSR line is the
 * Caltrain corridor from the public-domain NTAD rail network, and The Portal and BART Silicon
 * Valley Phase II are schematic lines between real station points, drawn to compare styles.
 * Open with ?lines=a|b|c (and &draw=0..1 for a mid-fly-in frame). Remove once a style is chosen.
 */
import type { LayerSpecification, SourceSpecification } from 'maplibre-gl';
import { stageColorExpression } from './projectLayers';
import { stageColor, type StageKey, type Theme } from '../theme/theme';

export type LineMock = 'a' | 'b' | 'c';

export function lineMockOption(): { option: LineMock; draw: number } | null {
  if (!import.meta.env.DEV || typeof location === 'undefined') return null;
  const q = new URLSearchParams(location.search);
  const option = q.get('lines');
  if (option !== 'a' && option !== 'b' && option !== 'c') return null;
  const draw = Math.min(1, Math.max(0, Number(q.get('draw') ?? 1)));
  return { option, draw };
}

const DATA = '/docs/mockups/lines/lines-mock.geojson';

export function lineMockSources(): Record<string, SourceSpecification> {
  return { 'line-mock': { type: 'geojson', data: DATA, lineMetrics: true } };
}

const isLine = ['==', ['get', 'kind'], 'line'];
const isStation = ['==', ['get', 'kind'], 'station'];
const seg = (s: string) => ['all', isLine, ['==', ['get', 'segment'], s]];

export function lineMockLayers(theme: Theme, option: LineMock, draw: number): LayerSpecification[] {
  const col = stageColorExpression(theme);
  const land = theme.colors.land;
  const z = (lo: number, hi: number) => ['interpolate', ['exponential', 1.6], ['zoom'], 8, lo, 15, hi];
  // Drawn up to `draw` of each line's length (the fly-in draws the line, like a site boundary).
  const progress = (color: string) => [
    'step', ['line-progress'], color, Math.max(draw, 0.0001), 'rgba(0,0,0,0)',
  ];
  const stationLabel: LayerSpecification = {
    id: 'line-mock-station-label', type: 'symbol', source: 'line-mock', minzoom: 11,
    filter: isStation as never,
    layout: {
      'text-field': ['get', 'name'], 'text-font': ['Libre Franklin Medium'], 'text-size': 12,
      'text-offset': [0, 1.1], 'text-anchor': 'top',
    },
    paint: { 'text-color': theme.colors.labels, 'text-halo-color': land, 'text-halo-width': 1.5 },
  };

  if (option === 'a') {
    // A. Thread: a quiet stage-coloured line, dashed where it runs in tunnel, hairline where it
    // shares existing track; stations as small rings.
    return [
      { id: 'line-mock-shared', type: 'line', source: 'line-mock', filter: seg('shared') as never,
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': col, 'line-width': z(1, 2.5), 'line-opacity': 0.7 } },
      { id: 'line-mock-new', type: 'line', source: 'line-mock', filter: seg('new') as never,
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': col, 'line-width': z(1.6, 4) } },
      { id: 'line-mock-tunnel', type: 'line', source: 'line-mock', filter: seg('tunnel') as never,
        layout: { 'line-join': 'round' },
        paint: { 'line-color': col, 'line-width': z(1.6, 4), 'line-dasharray': [1.5, 1.2] } },
      { id: 'line-mock-station', type: 'circle', source: 'line-mock', filter: isStation as never,
        paint: { 'circle-radius': z(2.5, 6), 'circle-color': land, 'circle-stroke-color': col, 'circle-stroke-width': z(1.2, 2.5) } },
      stationLabel,
    ] as LayerSpecification[];
  }

  if (option === 'b') {
    // B. Corridor: the line as a wide translucent band, like a site's fill, with a thin spine;
    // tunnel bands lighter. Stations rise as low extruded volumes (mock footprints).
    return [
      { id: 'line-mock-band', type: 'line', source: 'line-mock', filter: isLine as never,
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-color': col,
          'line-width': ['interpolate', ['exponential', 2], ['zoom'], 8, 3, 12, 10, 16, 120],
          'line-opacity': ['case', ['==', ['get', 'segment'], 'tunnel'], 0.16, 0.26],
        } },
      { id: 'line-mock-spine', type: 'line', source: 'line-mock', filter: isLine as never,
        layout: { 'line-join': 'round' },
        paint: { 'line-color': col, 'line-width': z(0.8, 1.6) } },
      { id: 'line-mock-station-3d', type: 'fill-extrusion', source: 'line-mock',
        filter: ['==', ['get', 'kind'], 'station-footprint'] as never,
        paint: { 'fill-extrusion-color': col, 'fill-extrusion-height': 14, 'fill-extrusion-opacity': 0.8 } },
      { id: 'line-mock-station', type: 'circle', source: 'line-mock', filter: isStation as never, maxzoom: 13,
        paint: { 'circle-radius': z(2.5, 5), 'circle-color': col, 'circle-stroke-color': land, 'circle-stroke-width': 1 } },
      stationLabel,
    ] as LayerSpecification[];
  }

  // C. Cased line: a bold stage-coloured line on a land-coloured casing, so it reads over the
  // building print at every zoom; tunnel runs are drawn as a hollow tube. Stations are solid dots.
  return [
    { id: 'line-mock-casing', type: 'line', source: 'line-mock', filter: isLine as never,
      layout: { 'line-cap': 'round', 'line-join': 'round' },
      paint: { 'line-gradient': progress(land) as never, 'line-width': z(4, 11) } },
    // line-gradient can't read feature data, so one core layer per stage.
    ...(['entitled', 'infrastructure'] as StageKey[]).map((stage) => ({
      id: `line-mock-core-${stage}`, type: 'line', source: 'line-mock',
      filter: ['all', isLine, ['!=', ['get', 'segment'], 'tunnel'], ['==', ['get', 'stage'], stage]] as never,
      layout: { 'line-cap': 'round', 'line-join': 'round' },
      paint: { 'line-gradient': progress(stageColor(theme, stage)) as never, 'line-width': z(2, 6) } })),
    { id: 'line-mock-tube', type: 'line', source: 'line-mock',
      filter: ['all', isLine, ['==', ['get', 'segment'], 'tunnel']] as never,
      layout: { 'line-cap': 'round', 'line-join': 'round' },
      paint: { 'line-color': col, 'line-width': z(3, 9), 'line-opacity': draw >= 1 ? 1 : 0 } },
    { id: 'line-mock-tube-hollow', type: 'line', source: 'line-mock',
      filter: ['all', isLine, ['==', ['get', 'segment'], 'tunnel']] as never,
      layout: { 'line-cap': 'round', 'line-join': 'round' },
      paint: { 'line-color': land, 'line-width': z(1.2, 4.5), 'line-opacity': draw >= 1 ? 1 : 0 } },
    { id: 'line-mock-station', type: 'circle', source: 'line-mock', filter: isStation as never,
      paint: { 'circle-radius': z(3, 8), 'circle-color': col, 'circle-stroke-color': land, 'circle-stroke-width': z(1, 2.5),
        'circle-opacity': draw >= 1 ? 1 : 0, 'circle-stroke-opacity': draw >= 1 ? 1 : 0 } },
    stationLabel,
  ] as LayerSpecification[];
}
