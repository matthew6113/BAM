import { useEffect, useRef } from 'preact/hooks';
import * as maplibregl from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import { Protocol } from 'pmtiles';
import 'maplibre-gl/dist/maplibre-gl.css';
import type { Theme } from '../theme/theme';
import { buildStyle, type ViewMode } from './style';
import { HOME_BOUNDS, MAX_BOUNDS, MAX_ZOOM, MIN_ZOOM } from './config';

maplibregl.setWorkerUrl(workerUrl);
const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

export const PITCH_3D = 55;
export const MAX_PITCH_3D = 65;

const isTouch = typeof matchMedia === 'function' && matchMedia('(pointer: coarse)').matches;

/** Camera that frames every project site, padded for the viewport size. */
export function homeCamera(map: maplibregl.Map): maplibregl.JumpToOptions {
  const small = map.getContainer().clientWidth < 640;
  const pad = small ? 28 : 72;
  return (
    map.cameraForBounds(HOME_BOUNDS, {
      padding: { top: pad + (small ? 48 : 24), bottom: pad, left: pad, right: pad },
    }) ?? { center: [-122.2, 37.75], zoom: 8.5 }
  );
}

interface Props {
  theme: Theme;
  mode: ViewMode;
  onReady: (map: maplibregl.Map) => void;
  onFirstInteraction?: () => void;
}

export function MapView({ theme, mode, onReady, onFirstInteraction }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const applied = useRef({ theme, mode });

  useEffect(() => {
    if (!container.current) return;
    // Read before the map exists: MapLibre writes its own hash as soon as it moves.
    const startsFromHash = /(^#|&)map=/.test(location.hash);
    const map = new maplibregl.Map({
      container: container.current,
      style: buildStyle(theme, { mode }),
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
    map.keyboard.enable();
    if (mode === '2d') map.touchZoomRotate.disableRotation();
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
    if (!map) return;
    if (applied.current.theme === theme && applied.current.mode === mode) return;
    applied.current = { theme, mode };
    map.setStyle(buildStyle(theme, { mode }), { diff: true });
  }, [theme, mode]);

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

  return <div ref={container} class="map" role="region" aria-label="Map of the Bay Area" />;
}
