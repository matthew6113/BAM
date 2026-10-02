const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const int = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
const dec = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

export const formatInt = (n: number) => int.format(n);
export const formatNumber = (n: number) => dec.format(n);

/** 1,600,000 -> "1.6 million"; values are never rounded beyond what the data states. */
export function formatSqft(n: number): string {
  if (n >= 1_000_000 && Number.isInteger(n / 10_000)) return `${dec.format(n / 1_000_000)} million sq ft`;
  return `${int.format(n)} sq ft`;
}

/** ISO-ish dates from the data ("2025-10", "2026-09-10") in a readable form; other text unchanged. */
export function formatDate(s: string): string {
  let m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
  if (m) return `${MONTHS[+m[2] - 1]} ${+m[3]}, ${m[1]}`;
  m = /^(\d{4})-(\d{2})$/.exec(s);
  if (m) return `${MONTHS[+m[2] - 1]} ${m[1]}`;
  return s;
}

/** A source URL shown as host and path, since the data holds URLs, not titles. */
export function sourceText(url: string): string {
  try {
    const u = new URL(url);
    const path = decodeURIComponent(u.pathname).replace(/\/$/, '');
    const short = path.length > 64 ? `${path.slice(0, 61)}…` : path;
    return `${u.hostname.replace(/^www\./, '')}${short}`;
  } catch {
    return url;
  }
}
