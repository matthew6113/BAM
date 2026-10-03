// Checks replacement project records written to $RECORDS_DIR (used while applying official
// findings, Milestone 3). Skipped unless RECORDS_DIR is set.
import { describe, expect, it } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import schema from '../data/schema/projects.schema.json';
import { isOfficialSource } from '../src/projects/official';

const dir = process.env.RECORDS_DIR;
describe.skipIf(!dir)('replacement records', () => {
  const ajv = new Ajv2020({ allErrors: true, strict: false });
  addFormats(ajv);
  const validate = ajv.compile({ $schema: schema.$schema, $defs: schema.$defs, $ref: '#/$defs/project' });
  for (const f of dir ? readdirSync(dir).filter((n) => n.endsWith('.json')) : []) {
    it(f, () => {
      const rec = JSON.parse(readFileSync(join(dir!, f), 'utf8'));
      validate(rec);
      expect(validate.errors ?? [], JSON.stringify(validate.errors, null, 1)).toEqual([]);
      expect(rec.sources.filter((u: string) => !isOfficialSource(u)), 'unofficial sources').toEqual([]);
      expect(rec.officialLinks?.filter((u: string) => !isOfficialSource(u)) ?? [], 'unofficial links').toEqual([]);
      expect(`${rec.id}.json`).toBe(f);
    });
  }
});
