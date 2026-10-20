// The ball set (DICTO 2026-10-20): its kits and shapes.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13, BALL_SET_VOLUMES as V } from '../../src/krp-core/src/polyhedra/index.js';
test('two kits in the construction sets: one ball + 8 rounded tetrahedra, and a block of 8 + 13', () => {
  const a = KITS13.ballSet, b = KITS13['ballSet.block'];
  assert.equal(a.group, 'sets'); assert.equal(b.group, 'sets');
  assert.equal(a.entries.length, 9); assert.equal(b.entries.length, 21);
  for (const k of [a, b]) for (const e of k.entries) assert.ok(POLYHEDRA[e.shape], e.shape);
  assert.equal(a.entries.filter((e) => e.shape === 'BALLSET_BALL').length, 1);
  assert.equal(b.entries.filter((e) => e.shape === 'BALLSET_BALL').length, 13);
});
test('three shapes whose volumes fill space: one ball + two rounded tetrahedra = 2 (the space per octahedron centre)', () => {
  assert.deepEqual(Object.keys(V).sort(), ['BALLSET_BALL', 'BALLSET_TET_DOWN', 'BALLSET_TET_UP']);
  assert.ok(Math.abs(V.BALLSET_BALL + V.BALLSET_TET_UP + V.BALLSET_TET_DOWN - 2) < 1e-3);
  assert.equal(V.BALLSET_TET_UP, V.BALLSET_TET_DOWN);
});
