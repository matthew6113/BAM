import type { Project } from './data';

/** What the index shows, and which projects the map draws. */
export interface ProjectFilter {
  query: string;
  /** Stage keys switched off in the legend. */
  hiddenStages: string[];
  /** One subregion, or '' for all. */
  subregion: string;
}

export const NO_FILTER: ProjectFilter = { query: '', hiddenStages: [], subregion: '' };

function fold(s: string): string {
  return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
}

export function matchesFilter(p: Project, f: ProjectFilter): boolean {
  if (f.hiddenStages.includes(p.stage)) return false;
  if (f.subregion && p.subregion !== f.subregion) return false;
  const q = fold(f.query.trim());
  if (!q) return true;
  const hay = [p.name, p.city, p.county, ...(p.aliases ?? [])].map(fold).join(' ');
  return q.split(/\s+/).every((word) => hay.includes(word));
}

export function isFiltered(f: ProjectFilter): boolean {
  return f.query.trim() !== '' || f.hiddenStages.length > 0 || f.subregion !== '';
}
