import { useEffect, useRef, useState } from 'preact/hooks';
import presets from '../theme/presets.json';
import {
  contrastIssues,
  defaultTheme,
  normalizeTheme,
  stageColor,
  type ColorRole,
  type StageKey,
  type Theme,
} from '../theme/theme';

interface Props {
  theme: Theme;
  onChange: (theme: Theme) => void;
  onClose: () => void;
}

const COLOR_LABELS: Record<ColorRole, string> = {
  land: 'Land (paper)',
  water: 'Water',
  shoreline: 'Shoreline hairline',
  outsideRegion: 'Land outside the nine counties',
  buildings: 'Existing buildings (ink)',
  labels: 'Labels',
  context: 'Context lines',
  contextExtrusion: 'Building heights in 3D',
  selection: 'Selection highlight',
  panelBackground: 'Panel background',
  panelText: 'Panel text',
  panelRule: 'Panel rules',
};

const STAGE_LABELS: Record<StageKey, string> = {
  proposed: 'Proposed',
  entitlement: 'In entitlement',
  entitled: 'Entitled',
  infrastructure: 'Site work',
  construction: 'Under construction',
  partial: 'Partly built (placeholder, not in spec)',
  complete: 'Complete',
  paused: 'Paused',
  distressed: 'Distressed',
};

const FONTS = ['Libre Franklin', 'Source Serif 4'];

const LAYER_LABELS: Record<Exclude<keyof Theme['layers'], 'overview'>, string> = {
  buildings: 'Buildings',
  water: 'Water',
  shoreline: 'Shoreline hairline',
  saltPonds: 'Salt ponds drawn as water',
  outsideRegion: 'Tint land outside the nine counties',
  labels: 'Labels',
  context: 'Freeways, highways, railroads and ferries',
};

function ColorField({ label, value, onInput }: { label: string; value: string; onInput: (v: string) => void }) {
  const [text, setText] = useState(value);
  // Keep the text box in sync when the value changes elsewhere (picker, preset, import).
  useEffect(() => setText(value), [value]);
  return (
    <label class="field color-field">
      <span>{label}</span>
      <input type="color" value={value} onInput={(e) => onInput((e.target as HTMLInputElement).value.toUpperCase())} />
      <input
        type="text"
        value={text}
        spellcheck={false}
        aria-label={`${label} hex`}
        onInput={(e) => {
          const v = (e.target as HTMLInputElement).value.trim();
          setText(v);
          if (/^#[0-9a-f]{6}$/i.test(v)) onInput(v.toUpperCase());
        }}
      />
    </label>
  );
}

function Slider(props: { label: string; min: number; max: number; step: number; value: number; onInput: (v: number) => void }) {
  return (
    <label class="field slider-field">
      <span>{props.label}</span>
      <input type="range" min={props.min} max={props.max} step={props.step} value={props.value}
        onInput={(e) => props.onInput(Number((e.target as HTMLInputElement).value))} />
      <output>{props.value}</output>
    </label>
  );
}

export function StylePanel({ theme, onChange, onClose }: Props) {
  const fileInput = useRef<HTMLInputElement>(null);
  const closeButton = useRef<HTMLButtonElement>(null);
  const [message, setMessage] = useState('');
  useEffect(() => closeButton.current?.focus(), []);
  const set = (fn: (t: Theme) => void) => {
    const next = structuredClone(theme);
    fn(next);
    onChange(next);
  };
  const issues = contrastIssues(theme);

  const exportTheme = async () => {
    const json = JSON.stringify(theme, null, 2) + '\n';
    const blob = new Blob([json], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'theme.json';
    a.click();
    URL.revokeObjectURL(a.href);
    try {
      await navigator.clipboard.writeText(json);
      setMessage('Downloaded theme.json and copied it to the clipboard.');
    } catch {
      setMessage('Downloaded theme.json.');
    }
  };

  const importTheme = async (file: File) => {
    try {
      onChange(normalizeTheme(JSON.parse(await file.text())));
      setMessage(`Imported ${file.name}.`);
    } catch (err) {
      setMessage(`Could not read ${file.name}: ${(err as Error).message}`);
    }
  };

  return (
    <aside class="style-panel" aria-label="Style panel">
      <header>
        <h2>Style</h2>
        <button ref={closeButton} type="button" class="close" aria-label="Close style panel" onClick={onClose}>
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg>
        </button>
      </header>
      <p class="hint">Changes apply live. Export the result and commit it as <code>src/theme/theme.json</code>.</p>

      <section>
        <h3>Preset</h3>
        <select
          aria-label="Preset"
          onChange={(e) => {
            const name = (e.target as HTMLSelectElement).value;
            if (name === '__default') return onChange(structuredClone(defaultTheme));
            const p = presets.presets.find((x) => x.name === name);
            if (p) set((t) => { Object.assign(t.colors, p.colors); t.name = p.name; });
          }}
        >
          <option value="">Choose a preset…</option>
          <option value="__default">Theme file (placeholders)</option>
          {presets.presets.map((p) => <option value={p.name}>{p.name}</option>)}
        </select>
      </section>

      <section>
        <h3>Base map colors</h3>
        {(Object.keys(COLOR_LABELS) as ColorRole[]).map((role) => (
          <ColorField label={COLOR_LABELS[role]} value={theme.colors[role]}
            onInput={(v) => set((t) => { t.colors[role] = v; })} />
        ))}
        <Slider label="Building opacity, street level" min={0.3} max={1} step={0.05} value={theme.opacity.buildings}
          onInput={(v) => set((t) => { t.opacity.buildings = v; })} />
        <Slider label="Building opacity, city (zoom 12.5)" min={0.1} max={1} step={0.05} value={theme.opacity.buildingsCity}
          onInput={(v) => set((t) => { t.opacity.buildingsCity = v; })} />
        <Slider label="Building opacity, regional" min={0.1} max={1} step={0.05} value={theme.opacity.buildingsRegional}
          onInput={(v) => set((t) => { t.opacity.buildingsRegional = v; })} />
        <Slider label="Shoreline weight" min={0.5} max={3} step={0.25} value={theme.map.shorelineWidth}
          onInput={(v) => set((t) => { t.map.shorelineWidth = v; })} />
      </section>

      <section>
        <h3>Stage colors</h3>
        <p class="hint">Not drawn yet (no projects in Milestone 1). Complete follows the existing buildings unless you change it.</p>
        {(Object.keys(STAGE_LABELS) as StageKey[]).map((stage) => (
          <ColorField label={STAGE_LABELS[stage]} value={stageColor(theme, stage)}
            onInput={(v) => set((t) => { t.stages[stage] = v; })} />
        ))}
      </section>

      <section>
        <h3>Type</h3>
        {([['ui', 'Interface'], ['text', 'Summaries and notes'], ['mapLabels', 'Map labels']] as const).map(([key, label]) => (
          <label class="field">
            <span>{label}</span>
            <select value={theme.type[key]} onChange={(e) => set((t) => { t.type[key] = (e.target as HTMLSelectElement).value; })}>
              {FONTS.map((f) => <option value={f}>{f}</option>)}
            </select>
          </label>
        ))}
        <p class="sample" style={{ fontFamily: `'${theme.type.text}'` }}>
          A decommissioned power plant on the Central Waterfront, being turned into a dense neighborhood.
        </p>
      </section>

      <section>
        <h3>3D</h3>
        <Slider label="Height exaggeration" min={0.5} max={3} step={0.1} value={theme.map.heightExaggeration}
          onInput={(v) => set((t) => { t.map.heightExaggeration = v; })} />
        <Slider label="Light direction (°)" min={0} max={359} step={1} value={theme.map.light.azimuth}
          onInput={(v) => set((t) => { t.map.light.azimuth = v; })} />
        <Slider label="Light height (°)" min={0} max={90} step={1} value={theme.map.light.polar}
          onInput={(v) => set((t) => { t.map.light.polar = v; })} />
        <Slider label="Light intensity" min={0} max={1} step={0.05} value={theme.map.light.intensity}
          onInput={(v) => set((t) => { t.map.light.intensity = v; })} />
        <Slider label="Context massing opacity" min={0} max={1} step={0.05} value={theme.opacity.contextExtrusion}
          onInput={(v) => set((t) => { t.opacity.contextExtrusion = v; })} />
      </section>

      <section>
        <h3>Layers</h3>
        {(Object.keys(LAYER_LABELS) as (keyof typeof LAYER_LABELS)[]).map((key) => (
          <label class="check">
            <input type="checkbox" checked={theme.layers[key]}
              onChange={(e) => set((t) => { t.layers[key] = (e.target as HTMLInputElement).checked; })} />
            {LAYER_LABELS[key]}
          </label>
        ))}
        <fieldset>
          <legend>Building tiles below zoom 13</legend>
          {([['all', 'Every building (heavier tiles)'], ['light', 'Lighter tiles (dense cores thinned)']] as const).map(([v, label]) => (
            <label class="check">
              <input type="radio" name="overview" checked={theme.layers.overview === v}
                onChange={() => set((t) => { t.layers.overview = v; })} />
              {label}
            </label>
          ))}
        </fieldset>
      </section>

      <section>
        <h3>Contrast check</h3>
        {issues.length === 0 ? (
          <p class="hint">Every check passes.</p>
        ) : (
          <ul class="issues">
            {issues.map((i) => (
              <li>{i.subject} on {i.against}: {i.ratio.toFixed(2)}:1 (needs {i.needed}:1)</li>
            ))}
          </ul>
        )}
      </section>

      <section class="actions">
        <button type="button" onClick={exportTheme}>Export JSON</button>
        <button type="button" onClick={() => fileInput.current?.click()}>Import JSON</button>
        <button type="button" onClick={() => { onChange(structuredClone(defaultTheme)); setMessage('Reset to the theme file.'); }}>Reset</button>
        <input ref={fileInput} type="file" accept="application/json,.json" hidden
          onChange={(e) => {
            const f = (e.target as HTMLInputElement).files?.[0];
            if (f) importTheme(f);
          }} />
        <p class="hint" role="status">{message}</p>
      </section>
    </aside>
  );
}
