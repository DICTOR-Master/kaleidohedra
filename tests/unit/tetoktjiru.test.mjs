// DICTO Tetoktjiru, bodies and legs (DICTO 2026-10-21): its kits and shapes.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13, TETOKTJIRU_VOLUMES as V } from '../../src/krp-core/src/polyhedra/index.js';
test('two kits in the construction sets: one Oktjiru + 8 Tetjiru, and a block of 8 + 13', () => {
  const a = KITS13.tetoktjiru, b = KITS13['tetoktjiru.block'];
  assert.equal(a.group, 'sets'); assert.equal(b.group, 'sets');
  assert.equal(a.entries.length, 9); assert.equal(b.entries.length, 21);
  for (const k of [a, b]) for (const e of k.entries) assert.ok(POLYHEDRA[e.shape], e.shape);
  assert.equal(a.entries.filter((e) => e.shape === 'TETOKTJIRU_OKTJIRU').length, 1);
  assert.equal(b.entries.filter((e) => e.shape === 'TETOKTJIRU_OKTJIRU').length, 13);
});
test('three shapes whose volumes fill space: one Oktjiru + two Tetjiru = 2 (the space per octahedron centre, less the mesh smoothing)', () => {
  assert.deepEqual(Object.keys(V).sort(), ['TETOKTJIRU_OKTJIRU', 'TETOKTJIRU_TETJIRU_DOWN', 'TETOKTJIRU_TETJIRU_UP']);
  assert.ok(Math.abs(V.TETOKTJIRU_OKTJIRU + V.TETOKTJIRU_TETJIRU_UP + V.TETOKTJIRU_TETJIRU_DOWN - 2) < 0.05);
  assert.ok(Math.abs(V.TETOKTJIRU_TETJIRU_UP - V.TETOKTJIRU_TETJIRU_DOWN) < 1e-3);
});
test('two tones: Tetjiru one tone each, every Oktjiru leg split between both', () => {
  const tones = (id) => new Set(POLYHEDRA[id].faceColours);
  assert.deepEqual([...tones('TETOKTJIRU_TETJIRU_UP')], [0xb8452f]); assert.deepEqual([...tones('TETOKTJIRU_TETJIRU_DOWN')], [0xeea58c]);
  assert.equal(tones('TETOKTJIRU_OKTJIRU').size, 2);
  assert.equal(POLYHEDRA.TETOKTJIRU_OKTJIRU.faceColours.length, POLYHEDRA.TETOKTJIRU_OKTJIRU.faces.length);
});
