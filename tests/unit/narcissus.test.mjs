// Narcissus (DICTO's name, 2026-11-04) and the Narcissus-and-cubes Fibonacci block in Polyhedraverse. Figures from the research study
// 2026-11-04-dehn-screen (pv_shapes.py; HexOct tiles at λ = 3/8): Narcissus 10 corners, 1 hexagon, 3 quadrilaterals, 6 triangles, its own mirror image;
// the block: 8 layers (types chcchchc) × 7 tiles, 42 Narcissus and 70 cubes, no overlaps.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, NARCISSUS_IDS } from '../../src/krp-core/src/polyhedra/index.js';

const N = POLYHEDRA.DICTO_NARCISSUS, B = POLYHEDRA.DICTO_NARCISSUS_TOGETHER;
const v3 = (p) => (Array.isArray(p) ? p : [p.x, p.y, p.z]);
test('both entries are registered, Narcissus first', () => {
  assert.deepEqual(NARCISSUS_IDS, ['DICTO_NARCISSUS', 'DICTO_NARCISSUS_TOGETHER', 'RD_TRD_HALF_CELL']);
  assert.ok(N && B);
  assert.equal(N.name, 'Narcissus');
});
test('Narcissus: 10 corners, faces 6 triangles + 3 quadrilaterals + 1 hexagon', () => {
  assert.equal(N.vertices.length, 10);
  const counts = {};
  for (const f of N.faces) { const n = (f.vertices ?? f).length; counts[n] = (counts[n] ?? 0) + 1; }
  assert.deepEqual(counts, { 3: 6, 4: 3, 6: 1 });
});
test('Narcissus is its own mirror image (a mirror plane through its 3-fold axis)', () => {
  const P = N.vertices.map(v3); const c = P.reduce((a, p) => a.map((x, i) => x + p[i] / P.length), [0, 0, 0]);
  const Q = P.map((p) => p.map((x, i) => x - c[i]));
  // the hexagon's normal is the 3-fold axis; try mirror planes containing it through each corner
  const hex = N.faces.find((f) => (f.vertices ?? f).length === 6); const h = (hex.vertices ?? hex).map((i) => Q[typeof i === 'number' ? i : i.index ?? i]);
  const sub = (a, b) => a.map((x, i) => x - b[i]), cr = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0), nrm = (a) => a.map((x) => x / Math.hypot(...a));
  const axis = nrm(cr(sub(h[1], h[0]), sub(h[2], h[0])));
  let found = false;
  for (const p of Q) {
    const r = sub(p, axis.map((x) => x * dot(p, axis))); if (Math.hypot(...r) < 1e-9) continue;
    const n = nrm(cr(axis, r));
    const M = Q.map((q) => sub(q, n.map((x) => 2 * x * dot(q, n))));
    if (M.every((m) => Q.some((q) => Math.hypot(...sub(m, q)) < 1e-9))) { found = true; break; }
  }
  assert.ok(found);
});
test('the block: 112 pieces, 42 Narcissus (gold) and 70 cubes', () => {
  assert.equal(B.parts.length, 112);
  const gold = B.parts.filter(([a]) => B.faceColours[a] === 0xd4a020).length;
  assert.equal(gold, 42);
});
test('the RD/TRD half-cell: 13 corners, one hexagon, two-colour seam (3 gold, 3 purple)', () => {
  const P = POLYHEDRA.RD_TRD_HALF_CELL; assert.equal(P.vertices.length, 13);
  const sizes = P.faces.map((f) => (f.vertices ?? f).length); assert.equal(sizes.filter((n) => n === 6).length, 1); assert.equal(sizes.length, 10);
  assert.equal(P.faceColours.filter((c) => c === 0xd4a020).length, 3); assert.equal(P.faceColours.filter((c) => c === 0x7a5fb0).length, 3);
});
