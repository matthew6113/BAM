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
  'cloverdale.net', // City of Cloverdale (agendas, staff reports)
  'cloverdale.granicus.com', // City of Cloverdale's agenda file server
  // Transit and regional agencies' own sites, several on non-government domains
  // (Matthew, 2026-10-07: approved, with the agenda and document stores below)
  'vta.org', // Santa Clara Valley Transportation Authority (www., gis., gtfs. subdomains)
  'vtabart.org', // VTA's BART Silicon Valley Phase II project site (reports, FTA oversight reports)
  'diridonsj.org', // Diridon Station partner agencies' project site, run by the City of San José
  'santaclaravta.iqm2.com', // VTA's agenda system (Board, BSVII Oversight, Diridon Steering Committee)
  'cityofsanrafael.org', // City of San Rafael (www., publicrecords. Laserfiche)
  'gis.marinpublic.com', // Marin County GIS (assessor parcels)
  'cityofepa.org', // City of East Palo Alto
  'cityofepa.granicus.com', // City of East Palo Alto's agenda system
  'eastpaloalto.iqm2.com', // City of East Palo Alto's agenda system before Sept 2023
  'smcgov.org', // County of San Mateo (data.smcgov.org open data, assessor parcels)
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
  // Tri-Valley–San Joaquin Valley Regional Rail Authority (Valley Link): agency site and its project/environmental site
  'valleylinkrail.com',
  'getvalleylinked.com',
  'tjpa.org', // Transbay Joint Powers Authority (The Portal / Downtown Rail Extension, Salesforce Transit Center)
  'sfcta.org', // San Francisco County Transportation Authority (Prop L sales tax, board memos)
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
  'd3n9y02raazwpg.cloudfront.net/cityofepa/', // East Palo Alto agenda packets (Granicus)
  'granicus_production_attachments.s3.amazonaws.com/cityofepa/', // East Palo Alto agendas and minutes (Granicus)
  'storage.googleapis.com/proudcity/sanrafaelca/', // City of San Rafael's document store (staff reports, resolutions)
  'services8.arcgis.com/qac9exitge3rh5x7/', // City of East Palo Alto
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
