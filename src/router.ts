/**
 * Deep links: /p/{project-id} and /about under the site's base path (/BAM/ on github.io, / on
 * map.matthewhuguet.com). Query and hash are kept, so view options and the camera survive navigation.
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

function go(path: string, state: Record<string, unknown>, replace: boolean) {
  const url = path + location.search + location.hash;
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
