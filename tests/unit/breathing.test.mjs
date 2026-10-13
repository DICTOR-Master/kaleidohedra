// Golden Breathing Pyrochlore (DICTO 2026-10-14): the four cells fill space for any breathing ratio, every hexagon is a
// flat-ended triangle with sides 1 and r, and every corner is shared tip to tip by one big and one small tetrahedron.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cellAt, kindAt, neighbours, BREATHING_STOPS } from '../../src/app/world-breathing.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const sub = (a, b) => a.map((x, i) => x - b[i]);
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const volume = ({ V, F }) => {
  const c = V.reduce((s, p) => s.map((x, i) => x + p[i] / V.length), [0, 0, 0]);
  let v = 0;
  for (const f of F) for (let m = 1; m + 1 < f.length; m++) v += Math.abs(dot(sub(V[f[0]], c), cross(sub(V[f[m]], c), sub(V[f[m + 1]], c)))) / 6;
  return v;
};
for (const r of [0.3, 0.5, 1 / PHI, 1]) {
  test(`r = ${r.toFixed(3)}: big + small tetrahedra + two truncated tetrahedra fill the cell`, () => {
    const u = (Math.SQRT2 * (1 + r)) / 4;
    const sum = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]].reduce((s, q) => s + volume(cellAt(q, r)), 0);
    assert.ok(Math.abs(sum - (4 * u) ** 3 / 4) < 1e-9, `${sum}`);
  });
  test(`r = ${r.toFixed(3)}: hexagons are flat-ended triangles, sides 1 and r`, () => {
    for (const q of [[2, 2, 2], [3, 3, 3]]) {
      const { V, F } = cellAt(q, r);
      for (const f of F.filter((x) => x.length === 6)) {
        const L = f.map((k, i) => Math.hypot(...sub(V[k], V[f[(i + 1) % 6]]))).sort((a, b) => a - b);
        assert.ok(Math.abs(L[0] - r) < 1e-9 && Math.abs(L[5] - 1) < 1e-9, L.join());
      }
    }
  });
}
test('every corner of a big tetrahedron is a corner of exactly one small one', () => {
  const r = 1 / PHI, A = cellAt([0, 0, 0], r);
  const small = neighbours([0, 0, 0]).filter((q) => kindAt(q) === 'B').map((q) => cellAt(q, r));
  assert.equal(small.length, 4);
  for (const p of A.V) assert.equal(small.filter((c) => c.V.some((v) => Math.hypot(...sub(v, p)) < 1e-9)).length, 1);
});
test('the slider opens on golden', () => { assert.equal(BREATHING_STOPS[0].key, 'golden'); assert.ok(Math.abs(BREATHING_STOPS[0].r - 1 / PHI) < 1e-12); });
