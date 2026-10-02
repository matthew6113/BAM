import { useCallback, useEffect, useRef, useState } from 'preact/hooks';
import type { Map as MapLibreMap } from 'maplibre-gl';
import { MapView } from './map/MapView';
import type { ViewMode } from './map/style';
import { applyCssVariables, defaultTheme, normalizeTheme, type Theme } from './theme/theme';
import { Controls } from './ui/Controls';
import { Credits } from './ui/Credits';
import { StylePanel } from './ui/StylePanel';

const params = new URLSearchParams(location.search);
/** The style panel is a design tool: on in development, or in any build with ?style=1. */
const STYLE_PANEL_ENABLED = import.meta.env.DEV || params.get('style') === '1';
const STORAGE_KEY = 'bam.theme.v1';

function loadTheme(): Theme {
  let theme = structuredClone(defaultTheme);
  if (STYLE_PANEL_ENABLED && !params.has('test')) {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) theme = normalizeTheme(JSON.parse(saved));
    } catch {
      // Storage can be blocked; fall back to the theme file.
    }
  }
  return applyLayerParams(theme);
}

/** Layer options from the URL, so a view can be shared or screenshotted: ?overview=light&salt=0&context=1 */
function applyLayerParams(theme: Theme): Theme {
  const flag = (name: string) => (params.has(name) ? params.get(name) !== '0' : undefined);
  const L = theme.layers;
  if (params.get('overview') === 'light' || params.get('overview') === 'all') {
    L.overview = params.get('overview') as 'all' | 'light';
  }
  L.saltPonds = flag('salt') ?? L.saltPonds;
  L.context = flag('context') ?? L.context;
  L.outsideRegion = flag('mask') ?? L.outsideRegion;
  L.labels = flag('labels') ?? L.labels;
  return theme;
}

export function App() {
  const [theme, setTheme] = useState<Theme>(loadTheme);
  const [mode, setMode] = useState<ViewMode>(params.get('view') === '3d' ? '3d' : '2d');
  const [map, setMap] = useState<MapLibreMap | null>(null);
  const [panelOpen, setPanelOpen] = useState(STYLE_PANEL_ENABLED && params.get('style') === '1');
  const [interacted, setInteracted] = useState(false);
  const styleToggle = useRef<HTMLButtonElement>(null);

  const closePanel = useCallback(() => {
    setPanelOpen(false);
    // Return focus to the control that opened the panel.
    requestAnimationFrame(() => styleToggle.current?.focus());
  }, []);

  useEffect(() => {
    applyCssVariables(theme);
    if (!STYLE_PANEL_ENABLED) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(theme));
    } catch {
      // Not critical: the panel still works without persistence.
    }
  }, [theme]);

  useEffect(() => {
    if (!STYLE_PANEL_ENABLED) return;
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName))) return;
      // Alt+Shift+S, not a bare "S": single-key shortcuts fire while typing (WCAG 2.1.4).
      if (e.altKey && e.shiftKey && e.code === 'KeyS') {
        e.preventDefault();
        setPanelOpen((open) => !open);
      } else if (e.key === 'Escape') {
        closePanel();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [closePanel]);

  const onReady = useCallback((m: MapLibreMap) => {
    setMap(m);
    document.body.dataset.mapReady = 'true';
  }, []);

  return (
    <div class={`app ${panelOpen ? 'with-panel' : ''}`}>
      <a class="skip-link" href="#controls-start">Skip to map controls</a>
      <header class="title">
        <h1>Bay Area megaprojects</h1>
      </header>
      <MapView theme={theme} mode={mode} onReady={onReady} onFirstInteraction={() => setInteracted(true)} />
      <span id="controls-start" tabIndex={-1} />
      <Controls map={map} mode={mode} onModeChange={setMode} />
      <Credits collapse={interacted} />
      {STYLE_PANEL_ENABLED && (
        <button ref={styleToggle} type="button" class="style-toggle" hidden={panelOpen}
          onClick={() => setPanelOpen(true)} title="Open the style panel (Alt+Shift+S)">
          Style
        </button>
      )}
      {panelOpen && <StylePanel theme={theme} onChange={setTheme} onClose={closePanel} />}
    </div>
  );
}
