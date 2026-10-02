import { useEffect, useState } from 'preact/hooks';
import type { Map as MapLibreMap } from 'maplibre-gl';
import type { ViewMode } from '../map/style';
import { homeCamera, MAX_PITCH_3D, PITCH_3D } from '../map/MapView';

interface Props {
  map: MapLibreMap | null;
  mode: ViewMode;
  onModeChange: (mode: ViewMode) => void;
}

const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

export function Controls({ map, mode, onModeChange }: Props) {
  const [bearing, setBearing] = useState(0);

  useEffect(() => {
    if (!map) return;
    const update = () => setBearing(map.getBearing());
    map.on('rotate', update);
    return () => {
      map.off('rotate', update);
    };
  }, [map]);

  const disabled = !map;
  const duration = () => (reducedMotion() ? 0 : 600);

  const toggleMode = () => {
    if (!map) return;
    const next: ViewMode = mode === '3d' ? '2d' : '3d';
    onModeChange(next);
    if (next === '3d') {
      // Raise the pitch limit first, or the easing is clamped to flat.
      map.setMaxPitch(MAX_PITCH_3D);
      map.easeTo({ pitch: PITCH_3D, duration: duration() });
    } else {
      map.easeTo({ pitch: 0, bearing: 0, duration: duration() });
    }
  };

  return (
    <nav class="controls" aria-label="Map controls">
      <div class="control-group">
        <button type="button" aria-label="Zoom in" title="Zoom in" disabled={disabled}
          onClick={() => map?.zoomIn({ duration: duration() })}>
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M3 8h10" /></svg>
        </button>
        <button type="button" aria-label="Zoom out" title="Zoom out" disabled={disabled}
          onClick={() => map?.zoomOut({ duration: duration() })}>
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10" /></svg>
        </button>
      </div>
      <div class="control-group">
        <button type="button" aria-label="Reset north" title="Reset north" disabled={disabled}
          onClick={() => map?.easeTo({ bearing: 0, pitch: mode === '3d' ? map.getPitch() : 0, duration: duration() })}>
          <svg viewBox="0 0 16 16" aria-hidden="true" style={{ transform: `rotate(${-bearing}deg)` }}>
            <path class="needle-n" d="M8 2.5 10.2 8H5.8z" />
            <path d="M8 13.5 10.2 8H5.8z" />
          </svg>
        </button>
        <button type="button" class="text" aria-pressed={mode === '3d'} disabled={disabled}
          title={mode === '3d' ? 'Switch to a flat 2D map' : 'Tilt the map and show building heights'}
          onClick={toggleMode}>
          {mode === '3d' ? '2D' : '3D'}
        </button>
      </div>
      <div class="control-group">
        <button type="button" class="text wide" disabled={disabled} title="Back to the whole Bay"
          onClick={() => map && map.easeTo({ ...homeCamera(map), pitch: 0, bearing: 0, duration: reducedMotion() ? 0 : 1200 })}>
          Whole Bay
        </button>
      </div>
    </nav>
  );
}
