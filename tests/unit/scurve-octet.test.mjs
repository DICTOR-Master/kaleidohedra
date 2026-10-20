// The S-curved double octet (DICTO 2026-10-20): its kits and shapes.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13, SCURVE_OCTET_VOLUMES as V } from '../../src/krp-core/src/polyhedra/index.js';
test('two kits in the construction sets: one octahedron + 8 tetrahedra, and a block of 8 + 13', () => {
  const a = KITS13.sCurveOctet, b = KITS13['sCurveOctet.block'];
  assert.equal(a.group, 'sets'); assert.equal(b.group, 'sets');
  assert.equal(a.entries.length, 9); assert.equal(b.entries.length, 21);
  for (const k of [a, b]) for (const e of k.entries) assert.ok(POLYHEDRA[e.shape], e.shape);
  assert.equal(a.entries.filter((e) => e.shape.startsWith('SCURVE_OCT')).length, 1);
  assert.equal(b.entries.filter((e) => e.shape.startsWith('SCURVE_OCT')).length, 13);
});
test('six shapes: four tetrahedra near 1/3 and the octahedron in two turns near 4/3 (the bend moves volume a little)', () => {
  const ids = Object.keys(V); assert.equal(ids.length, 6);
  for (const id of ids) assert.ok(id.startsWith('SCURVE_OCT') ? Math.abs(V[id] - 4 / 3) < 0.01 : Math.abs(V[id] - 1 / 3) < 0.01, `${id} ${V[id]}`);
});
