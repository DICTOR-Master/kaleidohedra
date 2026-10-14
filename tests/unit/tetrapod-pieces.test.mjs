// DICTO's tetrapod pieces (2026-10-14): each is one closed solid with the volume of its cells (five TOs, four RDs, edge 1).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';

const volume = (s) => s.faces.reduce((t, f) => { for (let k = 1; k + 1 < f.length; k++) { const [a, b, c] = [s.vertices[f[0]], s.vertices[f[k]], s.vertices[f[k + 1]]]; t += a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]); } return t; }, 0) / 6;

test('five truncated octahedra: 62 faces, volume 5 × 8√2', () => {
  const s = POLYHEDRA.TETRAPOD_FIVE_TO; assert.ok(s); assert.equal(s.faces.length, 62);
  assert.ok(Math.abs(volume(s) - 5 * 8 * Math.SQRT2) < 1e-6);
});
test('four rhombic dodecahedra: 36 faces, volume 4 × 16√3/9', () => {
  const s = POLYHEDRA.TETRAPOD_FOUR_RD; assert.ok(s); assert.equal(s.faces.length, 36);
  assert.ok(Math.abs(volume(s) - 4 * 16 * Math.sqrt(3) / 9) < 1e-6);
});
