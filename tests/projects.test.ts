import { describe, expect, it } from 'vitest';
import {
  boundaryOf,
  centroidOf,
  getProject,
  LAND_USE_CATEGORIES,
  landUseOf,
  linePrefix,
  loadAllGeometry,
  MAPPED_PROJECTS,
  massingOf,
  metres,
  boundaryLine,
  siteOf,
  bboxOf,
} from '../src/projects/data';
import { isOfficialSource } from '../src/projects/official';
import { STAGE_KEYS } from '../src/theme/theme';
import { formatDate, formatSqft, sourceText } from '../src/ui/format';
import { pathForProject, projectIdFromPath } from '../src/router';

// Massing and land use load on demand in the app; the checks below need all of it.
await loadAllGeometry();

const inside = ([x, y]: [number, number], [x0, y0, x1, y1]: number[]) => x >= x0 && x <= x1 && y >= y0 && y <= y1;

describe('traced project geometry', () => {
  it('maps Potrero Power Station', () => {
    expect(MAPPED_PROJECTS.map((p) => p.id)).toContain('potrero-power-station');
  });

  for (const project of MAPPED_PROJECTS) {
    describe(project.id, () => {
      const boundary = boundaryOf(project.id)!;
      const meta = boundary.properties ?? {};

      it('has exactly one site polygon', () => {
        expect(boundary.features.filter((f) => f.properties.kind === 'site')).toHaveLength(1);
      });

      it('cites official sources only', () => {
        const unofficial = project.sources.filter((u) => !isOfficialSource(u));
        expect(unofficial, 'move press-only facts and their sources into `reported`').toEqual([]);
      });

      it('says where the boundary came from and how accurate it is', () => {
        expect(['official', 'traced', 'approximate']).toContain(meta.accuracy);
        expect(String(meta.source)).toMatch(/\S/);
        // Every fact shown must trace to a source in the project's list.
        expect(project.sources).toContain(meta.sourceUrl);
      });

      const landUse = landUseOf(project.id);
      if (landUse) {
        it('draws land-use zones from a cited source, on the site', () => {
          expect(project.sources).toContain(landUse.properties?.sourceUrl);
          expect(String(landUse.properties?.note)).toMatch(/\S/);
          const [x0, y0, x1, y1] = bboxOf(siteOf(project.id)!.geometry);
          const pad = 0.0005;
          for (const f of landUse.features) {
            const p = f.properties;
            expect(p.kind, p.label).toBe('zone');
            expect(LAND_USE_CATEGORIES, p.label).toContain(p.category);
            expect(STAGE_KEYS, p.label).toContain(p.stage);
            expect(p.source, p.label).toMatch(/^(traced|GIS)/);
            expect(inside(centroidOf(f.geometry), [x0 - pad, y0 - pad, x1 + pad, y1 + pad]), p.label).toBe(true);
          }
        });
      }

      const massing = massingOf(project.id);
      if (!massing) return;

      it('cites its massing source', () => {
        expect(project.sources).toContain(massing.properties?.sourceUrl);
      });

      it('gives every massing feature a stage, a source and an honest height', () => {
        for (const f of massing.features) {
          const p = f.properties;
          expect(STAGE_KEYS, p.label).toContain(p.stage);
          expect(p.source, p.label).toMatch(/\S/);
          expect(typeof p.illustrative, p.label).toBe('boolean');
          if (p.height_ft !== null) expect(p.height_ft, p.label).toBeGreaterThan(0);
          if (p.podium_ft != null) expect(p.podium_ft, p.label).toBeLessThan(p.height_ft ?? Infinity);
          if (p.illustrative) expect(p.source, p.label).toMatch(/^illustrative/);
        }
      });

      it('labels illustrative massing as such', () => {
        const illustrative = massing.features.some((f) => f.properties.illustrative);
        expect(Boolean(massing.properties?.illustrative)).toBe(illustrative);
        if (illustrative) expect(String(massing.properties?.summary)).toMatch(/illustrative/i);
      });

      it('keeps the massing on the site', () => {
        const [x0, y0, x1, y1] = bboxOf(siteOf(project.id)!.geometry);
        const pad = 0.0005;
        for (const f of massing.features) {
          expect(inside(centroidOf(f.geometry), [x0 - pad, y0 - pad, x1 + pad, y1 + pad]), f.properties.label).toBe(true);
        }
      });

      it('lands its camera on the site', () => {
        if (!project.camera) return;
        const site = siteOf(project.id)!.geometry;
        expect(metres(project.camera.center, centroidOf(site))).toBeLessThan(300);
      });
    });
  }

  it('keeps the Potrero stack at its sourced 300 ft', () => {
    const stack = massingOf('potrero-power-station')!.features.find((f) => f.properties.kind === 'landmark')!;
    expect(stack.properties.height_ft).toBe(300);
    expect(stack.properties.source).toMatch(/2-7.*4\.D-8/);
  });
});

describe('Potrero block height limits', () => {
  const blocks = massingOf('potrero-power-station')!.features.filter((f) => f.properties.kind === 'block');
  const zones = (b: string) =>
    blocks
      .filter((f) => (f.properties as { block?: string }).block === b)
      .map((f) => f.properties.height_ft)
      .sort((x, y) => (x ?? 0) - (y ?? 0));

  it('matches the Design for Development height plan (Fig. 6.2.3)', () => {
    expect(zones('13')).toEqual([85, 125]);
    expect(zones('14')).toEqual([90]);
    expect(zones('1')).toEqual([85, 180]);
    expect(zones('2')).toEqual([130]);
    expect(zones('3')).toEqual([130]);
    expect(zones('4')).toEqual([65, 85]);
    expect(zones('5')).toEqual([85, 220]);
    expect(zones('15')).toEqual([145, 160]);
    expect(zones('7')).toEqual([85, 240]);
    expect(zones('8')).toEqual([85, 125]);
    expect(zones('11')).toEqual([130]);
    expect(zones('12')).toEqual([100]);
    expect(zones('9')).toEqual([null]);
  });

  it('draws tower zones over an 85-ft base and cites the D4D', () => {
    for (const f of blocks) {
      expect(f.properties.source).toMatch(/Design for Development.*6\.2\.3/);
      const tower = [180, 220, 240].includes(f.properties.height_ft ?? 0);
      expect(f.properties.podium_ft ?? null).toBe(tower ? 85 : null);
    }
  });
});

describe('official sources', () => {
  it('tells agencies from the press', () => {
    expect(isOfficialSource('https://sfplanning.s3.amazonaws.com/sfmea/x.pdf')).toBe(true);
    expect(isOfficialSource('https://data.sfgov.org/d/abcd-1234')).toBe(true);
    expect(isOfficialSource('https://www.sfmta.com/reports/x.pdf')).toBe(true);
    expect(isOfficialSource('https://www.cityofalameda.ca.gov/x')).toBe(true);
    expect(isOfficialSource('https://sfgov.legistar.com/LegislationDetail.aspx?ID=1')).toBe(true);
    expect(isOfficialSource('https://concordreuseproject.org/DocumentCenter/View/2374')).toBe(true);
    expect(isOfficialSource('https://legistar.granicus.com/sanjose/attachments/x.pdf')).toBe(true);
    expect(isOfficialSource('https://legistar.granicus.com/Sunnyvale/attachments/x.pdf')).toBe(true);
    expect(isOfficialSource('https://legistar.granicus.com/somecompany/attachments/x.pdf')).toBe(false);
    expect(isOfficialSource('https://apps.cupertino.org/pdf/x.pdf')).toBe(true);
    expect(isOfficialSource('https://portal.cityofvallejo.net/arcgis/rest/services/x')).toBe(true);
    expect(isOfficialSource('https://permitsonoma.org/x')).toBe(true);
    expect(isOfficialSource('https://www.cloverdale.net/AgendaCenter/x')).toBe(true);
    expect(isOfficialSource('https://www.cupertino.org/x')).toBe(false);
    expect(isOfficialSource('https://services7.arcgis.com/uRrQ0O3z2aaiIWYU/arcgis/rest/services/x')).toBe(true);
    expect(isOfficialSource('https://services7.arcgis.com/someoneelse/arcgis/rest/services/x')).toBe(false);
    expect(isOfficialSource('https://sfyimby.com/2026/02/x.html')).toBe(false);
    expect(isOfficialSource('https://www.sfchronicle.com/x')).toBe(false);
    expect(isOfficialSource('https://sfplanning.org.example.com/x')).toBe(false);
  });
});

describe('geometry helpers', () => {
  it('finds the centroid of a building-sized ring precisely', () => {
    const stack = massingOf('potrero-power-station')!.features.find((f) => f.properties.kind === 'landmark')!;
    const c = centroidOf(stack.geometry);
    const [x0, y0, x1, y1] = bboxOf(stack.geometry);
    expect(inside(c, [x0, y0, x1, y1])).toBe(true);
    expect(metres(c, [(x0 + x1) / 2, (y0 + y1) / 2])).toBeLessThan(2);
  });

  it('cuts a line by length', () => {
    const line = boundaryLine(siteOf('potrero-power-station')!.geometry);
    const len = (l: typeof line) =>
      (l.geometry.coordinates as [number, number][][]).reduce(
        (sum, r) => sum + r.slice(1).reduce((s, p, i) => s + metres(r[i], p), 0), 0);
    const whole = len(line);
    expect(len(linePrefix(line, 0.5)) / whole).toBeCloseTo(0.5, 3);
    expect(linePrefix(line, 1)).toBe(line);
    expect(linePrefix(line, 0).geometry.coordinates[0].length).toBeGreaterThanOrEqual(2);
  });

  it('draws every piece of a multi-part site', () => {
    const site = siteOf('downtown-west')!.geometry;
    const pieces = site.type === 'MultiPolygon' ? site.coordinates.length : 1;
    expect(pieces).toBeGreaterThan(1);
    expect(boundaryLine(site).geometry.coordinates).toHaveLength(pieces);
  });
});

describe('panel formatting', () => {
  it('writes square feet as the data states them', () => {
    expect(formatSqft(1_600_000)).toBe('1.6 million sq ft');
    expect(formatSqft(1_234_567)).toBe('1,234,567 sq ft');
    expect(formatSqft(250_000)).toBe('250,000 sq ft');
  });

  it('writes dates in sentence form', () => {
    expect(formatDate('2025-10')).toBe('Oct 2025');
    expect(formatDate('2026-10-01')).toBe('Oct 1, 2026');
    expect(formatDate('Spring 2027')).toBe('Spring 2027');
  });

  it('shows sources as host and path', () => {
    expect(sourceText('https://www.sfchronicle.com/realestate/article/x.php')).toBe('sfchronicle.com/realestate/article/x.php');
  });
});

describe('deep links', () => {
  it('reads and writes /p/{id}', () => {
    expect(projectIdFromPath('/p/potrero-power-station')).toBe('potrero-power-station');
    expect(projectIdFromPath('/p/potrero-power-station/')).toBe('potrero-power-station');
    expect(projectIdFromPath('/')).toBeNull();
    expect(projectIdFromPath('/p/Not_An_Id')).toBeNull();
    expect(pathForProject('potrero-power-station')).toBe('/p/potrero-power-station');
    expect(getProject('potrero-power-station')?.name).toBe('Potrero Power Station');
  });
});
