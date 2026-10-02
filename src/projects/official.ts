/**
 * Official sources (Matthew, 2026-10-02: "only official"). Every fact the map shows must
 * trace to one of these: public agencies and bodies, their adopted plans, records and GIS,
 * and the official publishers of their codes. Press and developer sites don't count;
 * facts that only they report wait in a project's `reported` record.
 */
const OFFICIAL_HOSTS = [
  'sfplanning.org',
  'sfplanning.s3.amazonaws.com', // SF Planning's document store (sfmea., commissions., default. subdomains)
  'sfgov.org',
  'sf.gov',
  'sfport.com',
  'sfmta.com',
  'sfbos.org',
  'sfgov.legistar.com', // Board of Supervisors legislative files (ordinances, attachments)
  'codelibrary.amlegal.com', // publisher of the San Francisco Municipal Code
  'ceqanet.lci.ca.gov',
  'regents.universityofcalifornia.edu',
];

export function isOfficialSource(url: string): boolean {
  let host: string;
  try {
    host = new URL(url).hostname.toLowerCase();
  } catch {
    return false;
  }
  if (host.endsWith('.gov') || host.endsWith('.ca.us')) return true;
  return OFFICIAL_HOSTS.some((h) => host === h || host.endsWith(`.${h}`));
}
