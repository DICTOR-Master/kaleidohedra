// DICTO-TIC's Hypsicles and Golden rectangles paths (DICTO 2026-10-14). Hypsicles ("Book XIV" of Euclid): the icosahedron and the
// dodecahedron in one sphere have the same inradius, so their central pyramids have the same height; inradius ÷ circumradius = 0.79465.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PATHS, GEOMETRY } from '../../src/app/world-cycles.js';

test('Hypsicles: same sphere, same height', () => {
  const { IN_ICO, IN_DOD, R_ICO, DOD_SAME } = GEOMETRY;
  for (const P of DOD_SAME) for (const p of P) assert.ok(Math.abs(Math.hypot(...p) - R_ICO) < 1e-9);
  assert.ok(Math.abs(IN_ICO - IN_DOD) < 1e-9);
  assert.ok(Math.abs(IN_ICO / R_ICO - 0.794654) < 1e-6);
});
test('the two new paths', () => {
  assert.deepEqual(PATHS[6].stations, ['icosahedron', 'cleoIcosOpen', 'dodecaPyramids', 'dodecaSameSphere']);
  assert.deepEqual(PATHS[7].stations, ['gr1', 'gr2', 'gr3', 'icosahedron']);
  assert.equal(PATHS[6].keeps.length, 3); assert.equal(PATHS[7].keeps.length, 3);
});
