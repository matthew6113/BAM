import type { Project } from './data';

/** What the index shows, and which projects of the open tab the map draws. */
export interface ProjectFilter {
  query: string;
  /** Stage keys switched off in the legend. */
  hiddenStages: string[];
  /** One subregion, or '' for all. */
  subregion: string;
}

/**
 * The two tabs, buildings and transit (`category` in data/projects.json). One is always open, and
 * the list and the map show only its projects (Matthew, 2026-10-21). `slug` names the tab in the
 * address: ?tab=transit.
 */
export type Category = 'buildings' | 'transportation';
export const CATEGORIES: { key: Category; label: string; slug: string }[] = [
  { key: 'buildings', label: 'Buildings', slug: 'buildings' },
  { key: 'transportation', label: 'Transit', slug: 'transit' },
];
/** The tab the page opens on. The address leaves it out. */
export const DEFAULT_CATEGORY: Category = 'buildings';

/** The tab an address names (?tab=transit), if it names one. */
export function categoryFromSlug(slug: string | null): Category | undefined {
  return CATEGORIES.find((c) => c.slug === slug)?.key;
}

/** How the address names a tab: its slug, or null for the default tab. */
export function slugOf(category: Category): string | null {
  return category === DEFAULT_CATEGORY ? null : CATEGORIES.find((c) => c.key === category)!.slug;
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

/** Whether search, stage or area narrow the list (the tab is not a filter: one is always open). */
export function isFiltered(f: ProjectFilter): boolean {
  return f.query.trim() !== '' || f.hiddenStages.length > 0 || f.subregion !== '';
}
