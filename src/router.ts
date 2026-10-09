/**
 * Deep links: /p/{project-id} under the site's base path (/BAM/ on github.io, / on map.matthewhuguet.com).
 * Query and hash are kept, so view options and the camera survive navigation.
 */
const BASE = import.meta.env.BASE_URL;

export function projectIdFromPath(path: string = location.pathname): string | null {
  const rest = path.startsWith(BASE) ? path.slice(BASE.length) : path.replace(/^\//, '');
  const m = /^p\/([a-z0-9]+(?:-[a-z0-9]+)*)\/?$/.exec(rest);
  return m ? m[1] : null;
}

export function pathForProject(id: string | null): string {
  return id ? `${BASE}p/${id}` : BASE;
}

export function navigate(id: string | null, replace = false) {
  const url = pathForProject(id) + location.search + location.hash;
  if (url === location.pathname + location.search + location.hash) return;
  if (replace) history.replaceState({ project: id }, '', url);
  else history.pushState({ project: id }, '', url);
}
