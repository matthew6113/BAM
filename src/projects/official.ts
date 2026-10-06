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
  // City- and county-run sites on non-government domains (Matthew, 2026-10-03: accept them)
  'sfrecpark.org', // SF Recreation and Park Department
  'sfocii.org', // SF Office of Community Investment and Infrastructure (redevelopment successor)
  'sftreasureisland.org', // Treasure Island Development Authority
  'onesanfrancisco.org', // SF Capital Planning Program
  'cityofconcord.org',
  'concordreuseproject.org', // City of Concord's reuse project site
  'suisunexpansion.com', // City of Suisun City's annexation site
  'acgov.org', // Alameda County
  'sccgov.org', // Santa Clara County (data.sccgov.org)
  'cityofvallejo.net', // City of Vallejo's document and ArcGIS servers (portal.cityofvallejo.net)
  'permitsonoma.org', // Permit Sonoma, Sonoma County's planning department
  // Agenda systems: one subdomain per agency
  'brisbaneca.api.civicclerk.com',
  'mountainview.legistar.com',
  'sanjose.legistar.com',
  'santaclara.legistar.com',
  'santaclara.legistar1.com',
  'sunnyvaleca.legistar.com',
  'cupertino.legistar.com',
  'oakland.legistar.com',
  'oakland.legistar1.com',
  'alameda.legistar.com',
  // City of Cupertino's document server (its Legistar item for The Rise links its approved plans here)
  'apps.cupertino.org',
];

/** Shared vendor hosts, accepted only under an agency's own path. */
const OFFICIAL_PREFIXES = [
  'legistar.granicus.com/sanjose/',
  'legistar.granicus.com/sunnyvale/',
  'legistar.granicus.com/cupertino/',
  'legistar1.granicus.com/alameda/',
  'webapi.legistar.com/v1/sfgov/',
  'webapi.legistar.com/v1/santaclara/',
  'webapi.legistar.com/v1/mountainview/',
  'webapi.legistar.com/v1/oakland/',
  'webapi.legistar.com/v1/alameda/',
  'd3n9y02raazwpg.cloudfront.net/suisuncityca/', // Suisun City agenda packets
  // ArcGIS Online organisations
  'services9.arcgis.com/ugpgsv1ugl0phsgx/', // City of Brisbane
  'services7.arcgis.com/urrq0o3z2aaiiwyu/', // City of Menlo Park
  'services5.arcgis.com/robnthsnjoz2wm1p/', // Alameda County
  'services9.arcgis.com/ucdlsg1ewpnogy4c/', // City of Alameda
  'services.arcgis.com/9tc74adhuml0x5yz/', // City of Oakland
];

export function isOfficialSource(url: string): boolean {
  let host: string;
  let path: string;
  try {
    const u = new URL(url);
    host = u.hostname.toLowerCase();
    path = `${host}${u.pathname.toLowerCase()}`;
  } catch {
    return false;
  }
  if (host.endsWith('.gov') || host.endsWith('.ca.us')) return true;
  if (OFFICIAL_HOSTS.some((h) => host === h || host.endsWith(`.${h}`))) return true;
  return OFFICIAL_PREFIXES.some((p) => path.startsWith(p));
}
