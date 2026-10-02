import { useEffect, useRef, useState } from 'preact/hooks';
import * as maplibregl from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import { Protocol } from 'pmtiles';
import 'maplibre-gl/dist/maplibre-gl.css';
import type { Theme } from '../theme/theme';
import { stageLabel } from '../projects/data';
import { buildStyle, type ViewMode } from './style';
import type { Selection } from './projectLayers';
import type { Camera } from '../projects/flight';
import { HOME_BOUNDS, MAX_BOUNDS, MAX_ZOOM, MIN_ZOOM } from './config';

maplibregl.setWorkerUrl(workerUrl);
const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

export const PITCH_3D = 55;
export const MAX_PITCH_3D = 65;

const isTouch = typeof matchMedia === 'function' && matchMedia('(pointer: coarse)').matches;

/** Camera that frames every project site, flat and north up, padded for the viewport size. */
export function homeCamera(map: maplibregl.Map): Camera {
  const small = map.getContainer().clientWidth < 640;
  const pad = small ? 28 : 72;
  const fit = map.cameraForBounds(HOME_BOUNDS, {
    padding: { top: pad + (small ? 48 : 24), bottom: pad, left: pad, right: pad },
  });
  const center = fit?.center ? maplibregl.LngLat.convert(fit.center) : { lng: -122.2, lat: 37.75 };
  return { center: [center.lng, center.lat], zoom: fit?.zoom ?? 8.5, pitch: 0, bearing: 0 };
}

interface StyleInputs {
  theme: Theme;
  mode: ViewMode;
  selection: Selection | null;
}

const applied = new WeakMap<maplibregl.Map, StyleInputs>();

/**
 * Bring the map's style up to date, as a diff. Called from render effects and directly by
 * the fly-in, which needs the project's sources in place before it touches them.
 */
export function syncStyle(map: maplibregl.Map, next: StyleInputs) {
  const prev = applied.get(map);
  if (
    prev && prev.theme === next.theme && prev.mode === next.mode &&
    prev.selection?.id === next.selection?.id && prev.selection?.phase === next.selection?.phase
  ) return;
  applied.set(map, next);
  map.setStyle(buildStyle(next.theme, next), { diff: true });
}

/** Layers that open a project when clicked. */
export const PROJECT_HIT_LAYERS = ['project-site-fill', 'project-markers'];

interface Hover {
  name: string;
  stage: string;
  x: number;
  y: number;
}

interface Props {
  theme: Theme;
  mode: ViewMode;
  selection: Selection | null;
  onReady: (map: maplibregl.Map) => void;
  onFirstInteraction?: () => void;
  onSelectProject?: (id: string) => void;
}

export function MapView({ theme, mode, selection, onReady, onFirstInteraction, onSelectProject }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [hover, setHover] = useState<Hover | null>(null);
  const select = useRef(onSelectProject);
  select.current = onSelectProject;

  useEffect(() => {
    if (!container.current) return;
    // Read before the map exists: MapLibre writes its own hash as soon as it moves.
    const startsFromHash = /(^#|&)map=/.test(location.hash);
    const map = new maplibregl.Map({
      container: container.current,
      style: buildStyle(theme, { mode, selection }),
      bounds: startsFromHash ? undefined : HOME_BOUNDS,
      maxBounds: MAX_BOUNDS,
      minZoom: MIN_ZOOM,
      maxZoom: MAX_ZOOM,
      maxPitch: mode === '3d' ? MAX_PITCH_3D : 0,
      hash: 'map',
      attributionControl: false,
      canvasContextAttributes: { antialias: true },
      pixelRatio: Math.min(window.devicePixelRatio || 1, isTouch ? 2 : 3),
      dragRotate: mode === '3d',
      pitchWithRotate: mode === '3d',
      fadeDuration: 150,
    });
    applied.set(map, { theme, mode, selection });
    map.keyboard.enable();
    if (mode === '2d') map.touchZoomRotate.disableRotation();

    // Hovering a site shows its name and stage; clicking it starts the fly-in.
    const hoverable = !isTouch;
    map.on('mousemove', PROJECT_HIT_LAYERS, (e) => {
      const f = e.features?.[0];
      if (!f || !hoverable) return;
      map.getCanvas().style.cursor = 'pointer';
      const p = f.properties as { name: string; stage: string };
      setHover({ name: p.name, stage: p.stage, x: e.point.x, y: e.point.y });
    });
    map.on('mouseleave', PROJECT_HIT_LAYERS, () => {
      map.getCanvas().style.cursor = '';
      setHover(null);
    });
    map.on('click', PROJECT_HIT_LAYERS, (e) => {
      const id = e.features?.[0]?.properties?.id as string | undefined;
      if (!id) return;
      setHover(null);
      map.getCanvas().style.cursor = '';
      select.current?.(id);
    });
    map.on('movestart', () => setHover(null));
    map.once('load', () => {
      if (!startsFromHash) map.jumpTo(homeCamera(map));
      onReady(map);
    });
    const first = () => onFirstInteraction?.();
    map.once('dragstart', first);
    map.once('zoomstart', (e) => {
      if ((e as { originalEvent?: Event }).originalEvent) first();
    });
    mapRef.current = map;
    if (import.meta.env.DEV || new URLSearchParams(location.search).has('test')) {
      (window as unknown as { __map: maplibregl.Map }).__map = map;
    }
    return () => {
      map.remove();
      mapRef.current = null;
    };
    // The map is created once; theme and mode changes are applied below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (map) syncStyle(map, { theme, mode, selection });
  }, [theme, mode, selection]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    if (mode === '3d') {
      map.setMaxPitch(MAX_PITCH_3D);
      map.dragRotate.enable();
      map.touchZoomRotate.enableRotation();
      map.touchPitch.enable();
      return;
    }
    map.dragRotate.disable();
    map.touchZoomRotate.disableRotation();
    map.touchPitch.disable();
    // Lock the pitch only once the map has eased back to flat, so the easing isn't cut short.
    const lock = () => map.setMaxPitch(0);
    if (map.getPitch() === 0 && !map.isMoving()) lock();
    else map.once('moveend', lock);
    return () => {
      map.off('moveend', lock);
    };
  }, [mode]);

  return (
    <>
      <div ref={container} class="map" role="region" aria-label="Map of the Bay Area" />
      {hover && (
        <div class="map-tooltip" role="presentation" style={{ left: `${hover.x}px`, top: `${hover.y}px` }}>
          <strong>{hover.name}</strong>
          <span>
            <i style={{ background: `var(--stage-${hover.stage})` }} />
            {stageLabel(hover.stage)}
          </span>
        </div>
      )}
    </>
  );
}
