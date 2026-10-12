import { useRef, useState } from 'preact/hooks';
import { MAPPED_PROJECTS, PROJECTS, STAGES, stageLabel } from '../projects/data';
import { CATEGORIES, isFiltered, matchesFilter, NO_FILTER, type ProjectFilter } from '../projects/filter';

interface Props {
  openId: string | null;
  onOpen: (id: string, opener: HTMLElement) => void;
  filter: ProjectFilter;
  onFilter: (f: ProjectFilter) => void;
}

const SUBREGIONS = [...new Set(MAPPED_PROJECTS.map((p) => p.subregion))].sort();
const STAGE_ORDER = [...STAGES].sort((a, b) => a.order - b.order);
const TABS = [
  { key: '' as const, label: 'All', n: undefined },
  ...CATEGORIES.map((c) => ({ ...c, n: MAPPED_PROJECTS.filter((p) => p.category === c.key).length })),
];

/**
 * The projects index: tabs for buildings and transportation, search, a stage legend that
 * doubles as a filter, and a subregion filter. The same filter decides which projects the
 * map draws.
 */
export function ProjectIndex({ openId, onOpen, filter, onFilter }: Props) {
  const [expanded, setExpanded] = useState(false);
  const tabList = useRef<HTMLDivElement>(null);
  const tabIndex = TABS.findIndex((t) => t.key === filter.category);
  // Arrow keys, Home and End move between the tabs (the tab list is one tab stop).
  const onTabKey = (e: KeyboardEvent) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
    const next = step !== undefined ? (tabIndex + step + TABS.length) % TABS.length
      : e.key === 'Home' ? 0 : e.key === 'End' ? TABS.length - 1 : -1;
    if (next < 0) return;
    e.preventDefault();
    onFilter({ ...filter, category: TABS[next].key });
    tabList.current?.querySelectorAll<HTMLElement>('[role="tab"]')[next]?.focus();
  };
  const shown = MAPPED_PROJECTS.filter((p) => matchesFilter(p, filter));
  const stages = STAGE_ORDER.filter((s) => MAPPED_PROJECTS.some((p) => p.stage === s.key));
  const toggleStage = (key: string) =>
    onFilter({
      ...filter,
      hiddenStages: filter.hiddenStages.includes(key)
        ? filter.hiddenStages.filter((k) => k !== key)
        : [...filter.hiddenStages, key],
    });

  return (
    <nav class="project-index" aria-label="Projects">
      <button type="button" class="index-toggle" aria-expanded={expanded} aria-controls="project-index-body"
        onClick={() => setExpanded((e) => !e)}>
        Projects
        <span class="count">{isFiltered(filter) ? `${shown.length} of ${MAPPED_PROJECTS.length}` : MAPPED_PROJECTS.length}</span>
        <svg viewBox="0 0 12 12" aria-hidden="true"><path d={expanded ? 'M3 7.5 6 4.5l3 3' : 'M3 4.5 6 7.5l3-3'} /></svg>
      </button>
      <div id="project-index-body" hidden={!expanded}>
        <div class="category-tabs" role="tablist" aria-label="Project type" ref={tabList} onKeyDown={onTabKey}>
          {TABS.map((t) => {
            const on = t.key === filter.category;
            return (
              <button type="button" role="tab" aria-selected={on}
                aria-controls="project-index-list" tabIndex={on ? 0 : -1}
                onClick={() => onFilter({ ...filter, category: t.key })}>
                {t.label}
                {t.n !== undefined && <span class="n">{t.n}</span>}
              </button>
            );
          })}
        </div>
        <label class="search">
          <span class="visually-hidden">Search projects</span>
          <input type="search" placeholder="Search by name or city" value={filter.query}
            onInput={(e) => onFilter({ ...filter, query: (e.currentTarget as HTMLInputElement).value })} />
        </label>
        <fieldset class="legend">
          <legend>Stage</legend>
          {stages.map((s) => {
            const on = !filter.hiddenStages.includes(s.key);
            const n = MAPPED_PROJECTS.filter((p) => p.stage === s.key).length;
            return (
              <button type="button" class="stage-toggle" aria-pressed={on} onClick={() => toggleStage(s.key)}
                title={s.meaning}>
                <i style={{ background: `var(--stage-${s.key})` }} />
                {s.label}
                <span class="n">{n}</span>
              </button>
            );
          })}
        </fieldset>
        <label class="subregion">
          <span>Area</span>
          <select value={filter.subregion}
            onChange={(e) => onFilter({ ...filter, subregion: (e.currentTarget as HTMLSelectElement).value })}>
            <option value="">Whole Bay</option>
            {SUBREGIONS.map((r) => <option value={r}>{r}</option>)}
          </select>
        </label>
        <ul id="project-index-list" aria-live="polite">
          {shown.map((p) => (
            <li>
              <button type="button" aria-current={p.id === openId ? 'true' : undefined}
                onClick={(e) => onOpen(p.id, e.currentTarget as HTMLElement)}>
                <span class="name">{p.name}</span>
                <span class="where">{p.city}</span>
                <span class="stage">
                  <i style={{ background: `var(--stage-${p.stage})` }} />
                  {stageLabel(p.stage)}
                </span>
              </button>
            </li>
          ))}
        </ul>
        {shown.length === 0 && <p class="small">No projects match.</p>}
        {isFiltered(filter) && (
          <button type="button" class="clear" onClick={() => onFilter(NO_FILTER)}>Show all projects</button>
        )}
        {MAPPED_PROJECTS.length < PROJECTS.length && (
          <p class="small">More projects are being mapped.</p>
        )}
      </div>
    </nav>
  );
}
