/**
 * Deep links: /p/{project-id} and /about under the site's base path (/BAM/ on github.io, / on
 * map.matthewhuguet.com). Query and hash are kept, so view options and the camera survive navigation.
 * The open tab rides in the query (?tab=transit) except on a project's own page, which implies it.
 */
const BASE = import.meta.env.BASE_URL;

const rest = (path: string) => (path.startsWith(BASE) ? path.slice(BASE.length) : path.replace(/^\//, ''));

export function projectIdFromPath(path: string = location.pathname): string | null {
  const m = /^p\/([a-z0-9]+(?:-[a-z0-9]+)*)\/?$/.exec(rest(path));
  return m ? m[1] : null;
}

/**
 * Project ids that no longer exist, and the index search that lists what replaced them, so old
 * links still land somewhere useful: the map opens with the index showing those projects.
 */
export const RETIRED_IDS: Record<string, string> = {
  // Split into one project per station (Matthew, 2026-10-19).
  'bart-station-housing': 'BART TOD',
};

/** The index search for a link to a retired project id, or null. */
export function retiredQuery(path: string = location.pathname): string | null {
  const id = projectIdFromPath(path);
  return id && Object.prototype.hasOwnProperty.call(RETIRED_IDS, id) ? RETIRED_IDS[id] : null;
}

export function isAboutPath(path: string = location.pathname): boolean {
  return /^about\/?$/.test(rest(path));
}

export function pathForProject(id: string | null): string {
  return id ? `${BASE}p/${id}` : BASE;
}

export const ABOUT_PATH = `${BASE}about`;

/** The open tab's slug, or null for the default tab. */
let tab: string | null = null;

/** The tab named in the address (?tab=transit), or null. */
export function tabFromQuery(search: string = location.search): string | null {
  return new URLSearchParams(search).get('tab');
}

/** The current query with the tab set, or left out on a project's page and for the default tab. */
function queryFor(path: string): string {
  const want = tab && !projectIdFromPath(path) ? tab : null;
  const q = new URLSearchParams(location.search);
  if (q.get('tab') === want) return location.search;
  if (want) q.set('tab', want);
  else q.delete('tab');
  const s = q.toString();
  return s ? `?${s}` : '';
}

function go(path: string, state: unknown, replace: boolean) {
  const url = path + queryFor(path) + location.hash;
  if (url === location.pathname + location.search + location.hash) return;
  if (replace) history.replaceState(state, '', url);
  else history.pushState(state, '', url);
}

export function navigate(id: string | null, replace = false) {
  go(pathForProject(id), { project: id }, replace);
}

/** Open (or, with false, leave) the about page. */
export function navigateAbout(open: boolean, replace = false) {
  go(open ? ABOUT_PATH : BASE, { about: open }, replace);
}

/** Put the open tab in the address (null for the default tab), in place: no new history entry. */
export function setTab(slug: string | null) {
  tab = slug;
  go(location.pathname, history.state, true);
}
