import { describe, expect, it } from 'vitest';
import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import schema from '../data/schema/projects.schema.json';
import data from '../data/projects.json';

describe('data/projects.json', () => {
  it('matches the schema', () => {
    const ajv = new Ajv2020({ allErrors: true, strict: false });
    addFormats(ajv);
    const validate = ajv.compile(schema);
    const ok = validate(data);
    expect(validate.errors ?? [], JSON.stringify(validate.errors, null, 2)).toEqual([]);
    expect(ok).toBe(true);
  });

  it('has unique project ids', () => {
    const ids = data.projects.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('only uses stages that are defined', () => {
    const keys = new Set(data.stages.map((s) => s.key));
    for (const p of data.projects) expect(keys.has(p.stage), p.id).toBe(true);
  });

  it('never dates a verification in the future', () => {
    const latest = data._meta.lastVerified;
    for (const p of data.projects) expect(p.lastVerified <= latest, p.id).toBe(true);
  });
});
