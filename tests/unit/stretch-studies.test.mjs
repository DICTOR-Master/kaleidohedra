// DICTO stretched solids (DICTO 2026-10-22; paper #49): face counts at spacing 1 as in the paper's study, every edge
// one edge long there, and the counts the same at other spacings (the hull's shape of faces does not depend on the spacing).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { stretchedSolid, faceKind, capCentres } from '../../src/app/stretch-geometry.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const count = (F) => { const c = {}; for (const f of F) c[f.length] = (c[f.length] ?? 0) + 1; return c; };
const CASES = [
  ['cube', 2, 14, { 4: 2, 5: 8, 6: 4 }],
  ['face', 2, 22, { 4: 10, 5: 12 }],
  ['body', 2, 24, { 4: 12, 5: 12 }],
  ['five', 2, 18, { 4: 6, 5: 10, 7: 2 }],
  ['cube', 3, 29, { 3: 2, 4: 15, 5: 12 }],
  ['cube', 4, 34, { 3: 4, 4: 18, 5: 12 }],
];
test('face counts at spacing 1, edges of one edge', () => {
  for (const [dir, caps, n, kinds] of CASES) {
    const F = stretchedSolid(1, dir, caps);
    assert.equal(F.length, n, `${dir} ${caps}`); assert.deepEqual(count(F), kinds, `${dir} ${caps}`);
    // every edge one edge long; along the cube and five-fold axes an edge parallel to the stretch runs on for a second edge
    const lengths = dir === 'cube' || dir === 'five' ? [1, 2] : [1];
    for (const f of F) f.forEach((p, i) => { const e = Math.hypot(...p.map((c, k) => c - f[(i + 1) % f.length][k])) / (2 / PHI); assert.ok(lengths.some((m) => Math.abs(e - m) < 1e-9), `${dir} ${caps}: edge ${e}`); });
  }
});
test('the same faces at other spacings; caps centred; kinds named', () => {
  for (const [dir, caps, n] of CASES) for (const sp of [0.5, 1.7, 2.7]) assert.equal(stretchedSolid(sp, dir, caps).length, n, `${dir} ${caps} at ${sp}`);
  for (const caps of [2, 3, 4]) { const C = capCentres(1, 'body', caps); for (let a = 0; a < 3; a++) assert.ok(Math.abs(C.reduce((t, p) => t + p[a], 0)) < 1e-12); }
  const d = capCentres(1, 'face', 4); assert.ok(Math.abs(Math.hypot(...d[0].map((c, k) => c - d[1][k])) - 2 / PHI) < 1e-12, 'spacing 1 = one edge');
  assert.deepEqual(['pentagon', 'rhombus', 'triangle', 'long'], [faceKind([1, 2, 3, 4, 5]), faceKind([1, 2, 3, 4]), faceKind([1, 2, 3]), faceKind([1, 2, 3, 4, 5, 6, 7])]);
});
