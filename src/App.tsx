import { useCallback, useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { matchesFilter, NO_FILTER, type ProjectFilter } from './projects/filter';
import type { Map as MapLibreMap } from 'maplibre-gl';
import { homeCamera, MapView, MAX_PITCH_3D, syncStyle } from './map/MapView';
import type { Selection } from './map/projectLayers';
import type { ViewMode } from './map/style';
import { alignmentOf, boundaryLine, centroidOf, getProject, loadProjectGeometry, MAPPED_PROJECTS, massingOf, siteOf } from './projects/data';
import {
  currentCamera,
  flyIn,
  flyOut,
  landingCamera,
  lowerMassing,
  panelPadding,
  riseMassing,
  type Camera,
} from './projects/flight';
import { navigate, projectIdFromPath } from './router';
import { applyCssVariables, defaultTheme, normalizeTheme, type Theme } from './theme/theme';
import { Controls } from './ui/Controls';
import { Credits } from './ui/Credits';
import { ProjectIndex } from './ui/ProjectIndex';
import { ProjectPanel } from './ui/ProjectPanel';
import { StylePanel } from './ui/StylePanel';

const params = new URLSearchParams(location.search);
/** The style panel is a design tool: on in development, or in any build with ?style=1. */
const STYLE_PANEL_ENABLED = import.meta.env.DEV || params.get('style') === '1';
const STORAGE_KEY = 'bam.theme.v1';
/** The page title on the home view (a deep-linked page starts with its project's title). */
const SITE_TITLE = 'Bay Area megaprojects';

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

/** Everything a flight needs to know that outlives a render. */
interface FlightState {
  /** Bumped by every open and close; a step that finds it changed has been superseded. */
  token: number;
  finishRise: (() => void) | null;
  /** Where the viewer was before the first fly-in, to fly back to. */
  returnCamera: Camera | null;
  returnMode: ViewMode;
  opener: HTMLElement | null;
}

export function App() {
  const [theme, setTheme] = useState<Theme>(loadTheme);
  const [mode, setMode] = useState<ViewMode>(params.get('view') === '3d' ? '3d' : '2d');
  const [map, setMap] = useState<MapLibreMap | null>(null);
  const [panelOpen, setPanelOpen] = useState(STYLE_PANEL_ENABLED && params.get('style') === '1');
  const [interacted, setInteracted] = useState(false);
  const [selection, setSelection] = useState<Selection | null>(null);
  const [openId, setOpenId] = useState<string | null>(null);
  const [filter, setFilter] = useState<ProjectFilter>(NO_FILTER);
  const hidden = useMemo(() => MAPPED_PROJECTS.filter((p) => !matchesFilter(p, filter)).map((p) => p.id), [filter]);
  const styleToggle = useRef<HTMLButtonElement>(null);
  const flight = useRef<FlightState>({ token: 0, finishRise: null, returnCamera: null, returnMode: '2d', opener: null });
  const live = useRef({ theme, mode, openId });
  live.current = { theme, mode, openId };

  const closePanel = useCallback(() => {
    setPanelOpen(false);
    // Return focus to the control that opened the panel.
    requestAnimationFrame(() => styleToggle.current?.focus());
  }, []);

  /** Open a project: panel in, fly to its camera, draw the boundary, raise its buildings. */
  const openProject = useCallback(async (id: string, opts: { push?: boolean; opener?: HTMLElement | null } = {}) => {
    const project = getProject(id);
    const site = siteOf(id);
    // Only mapped projects open: their facts have been checked against official sources.
    if (!map || !project || !site) return;
    const f = flight.current;
    const token = ++f.token;
    const current = () => flight.current.token === token;
    f.finishRise?.();
    f.finishRise = null;
    if (!live.current.openId) {
      f.returnCamera = currentCamera(map);
      f.returnMode = live.current.mode;
      f.opener = opts.opener ?? (document.activeElement as HTMLElement | null);
    }
    // The project's massing and land use are fetched on demand (small, usually cached).
    await loadProjectGeometry(id);
    if (!current()) return;
    if (opts.push !== false) navigate(id);
    document.title = `${project.name} · ${SITE_TITLE}`;
    setOpenId(id);

    const massing = massingOf(id);
    setMode('3d');
    map.setMaxPitch(MAX_PITCH_3D);
    const flying: Selection = { id, phase: 'flying' };
    setSelection(flying);
    // For tests and screenshots: where the fly-in is (flying, landed, risen).
    document.body.dataset.flight = 'flying';
    // Apply now, not on the next render: the flight writes into the project's sources.
    syncStyle(map, { theme: live.current.theme, mode: '3d', selection: flying });
    if (massing) lowerMassing(map, massing);
    const padding = panelPadding(map);
    // A line project draws its alignment; any other project, its site boundary.
    const drawing = alignmentOf(id) ?? boundaryLine(site.geometry);
    await flyIn(map, landingCamera(map, project, site.geometry, padding), padding, drawing, current);
    if (!current()) return;

    const landed: Selection = { id, phase: 'landed' };
    setSelection(landed);
    document.body.dataset.flight = 'landed';
    syncStyle(map, { theme: live.current.theme, mode: '3d', selection: landed });
    const risen = () => {
      if (current()) document.body.dataset.flight = 'risen';
    };
    if (massing) f.finishRise = riseMassing(map, massing, centroidOf(site.geometry), risen);
    else risen();
  }, [map]);

  /** Close the panel and fly back to where the viewer was (or to `to`). */
  const closeProject = useCallback(async (opts: { push?: boolean; to?: Camera } = {}) => {
    if (!map || !live.current.openId) return;
    const f = flight.current;
    const token = ++f.token;
    f.finishRise?.();
    f.finishRise = null;
    if (opts.push !== false) navigate(null);
    document.title = SITE_TITLE;
    setOpenId(null);
    const back = opts.to ?? f.returnCamera;
    const backMode = opts.to ? '2d' : f.returnMode;
    const opener = f.opener;
    f.returnCamera = null;
    f.opener = null;
    // Focus now, not on the next frame: frames can be slow mid-flight, and the opener sits
    // outside the panel that is about to unmount.
    (opener?.isConnected ? opener : map.getCanvas()).focus({ preventScroll: true });
    if (back) await flyOut(map, back);
    if (flight.current.token !== token) return;
    setSelection(null);
    delete document.body.dataset.flight;
    setMode(backMode);
  }, [map]);

  const goHome = useCallback(() => {
    if (!map) return;
    const camera = homeCamera(map);
    if (live.current.openId) {
      void closeProject({ to: camera });
      return;
    }
    map.easeTo({ ...camera, duration: matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 1200 });
  }, [map, closeProject]);

  // Deep link on load, and the back and forward buttons.
  useEffect(() => {
    if (!map) return;
    const sync = (initial: boolean) => {
      const id = projectIdFromPath();
      if (id && !siteOf(id)) {
        navigate(null, true);
        return;
      }
      if (id && id !== live.current.openId) void openProject(id, { push: false });
      else if (!id && live.current.openId && !initial) void closeProject({ push: false });
    };
    sync(true);
    const onPop = () => sync(false);
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [map, openProject, closeProject]);

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
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName))) return;
      // Alt+Shift+S, not a bare "S": single-key shortcuts fire while typing (WCAG 2.1.4).
      if (STYLE_PANEL_ENABLED && e.altKey && e.shiftKey && e.code === 'KeyS') {
        e.preventDefault();
        setPanelOpen((open) => !open);
      } else if (e.key === 'Escape') {
        // The topmost panel closes first.
        if (panelOpen) closePanel();
        else if (live.current.openId) void closeProject();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [closePanel, closeProject, panelOpen]);

  const onReady = useCallback((m: MapLibreMap) => {
    setMap(m);
    document.body.dataset.mapReady = 'true';
  }, []);

  const project = openId ? getProject(openId) : undefined;
  const mappedIndex = MAPPED_PROJECTS.findIndex((p) => p.id === openId);
  const neighbour = (step: number) =>
    mappedIndex < 0 || MAPPED_PROJECTS.length < 2
      ? undefined
      : MAPPED_PROJECTS[(mappedIndex + step + MAPPED_PROJECTS.length) % MAPPED_PROJECTS.length];
  const prev = neighbour(-1);
  const next = neighbour(1);

  return (
    <div class={`app ${panelOpen ? 'with-panel' : ''} ${project ? 'with-project' : ''}`}>
      <a class="skip-link" href="#controls-start">Skip to map controls</a>
      <header class="title">
        <h1>{SITE_TITLE}</h1>
        <ProjectIndex openId={openId} onOpen={(id, opener) => void openProject(id, { opener })}
          filter={filter} onFilter={setFilter} />
      </header>
      <MapView theme={theme} mode={mode} selection={selection} hidden={hidden} onReady={onReady}
        onFirstInteraction={() => setInteracted(true)}
        onSelectProject={(id) => void openProject(id)} />
      <span id="controls-start" tabIndex={-1} />
      <Controls map={map} mode={mode} onModeChange={setMode} onHome={goHome} />
      <Credits collapse={interacted || !!project} />
      {project && (
        <ProjectPanel project={project} onClose={() => void closeProject()}
          onPrev={prev && (() => void openProject(prev.id))} prevName={prev?.name}
          onNext={next && (() => void openProject(next.id))} nextName={next?.name} />
      )}
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
