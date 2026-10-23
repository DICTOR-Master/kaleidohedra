// DICTONIC (DICTO 2026-10-23; src/app/world-dictonic.js): the pieces the world draws fill space with 0 gaps and 0 overlaps (point
// test) at every stop of both sliders and between them: Golden (T(x) on the lattice points, T(1/x) on the cube centres; x = 0, 1, τ,
// ∞ and 0.1, 0.5, 3, 20), Keyed (Lotus Jewel Axes + Dodecaxes) and Delian (the octet family; every stop and t = 0.05, 0.2, 0.42, 0.6,
// 0.9). Golden at x = 1 is Kelvin's (all edges equal), at x = τ the pieces are Icosaxes and Unborn Axes; the stops sit where the
// slider snaps.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { goldenFamily, delianFamily, goldenT, GOLDEN_STOPS, DELIAN_STOPS, DICTONIC_VIEWS } from '../../src/app/world-dictonic.js';
import { goldenPieces } from '../../src/app/world-octet.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (u, w) => u[0] * w[0] + u[1] * w[1] + u[2] * w[2];
const cross = (u, w) => [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
function winding(V, F, p) {
  let w = 0;
  for (const f of F) for (let m = 1; m + 1 < f.length; m++) {
    const [a, b, c] = [f[0], f[m], f[m + 1]].map((i) => sub(V[i], p)), la = Math.hypot(...a), lb = Math.hypot(...b), lc = Math.hypot(...c);
    w += 2 * Math.atan2(dot(a, cross(b, c)), la * lb * lc + dot(a, b) * lc + dot(a, c) * lb + dot(b, c) * la);
  }
  return Math.round(w / (4 * Math.PI));
}
function pointTest(list, half, samples = 2000) {
  let seed = 3, gaps = 0, doubled = 0;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let k = 0; k < samples; k++) {
    const p = [rnd(), rnd(), rnd()].map((q) => (q * 2 - 1) * half);
    const cover = list.reduce((s, [, V, F, , x]) => (Math.hypot(...sub(p, x.anchor)) < 2 ? s + winding(V, F, p) : s), 0);
    if (cover === 0) gaps++; else if (cover > 1) doubled++;
  }
  return { gaps, doubled };
}

for (const x of [...GOLDEN_STOPS.map((s) => s.v), 0.1, 0.5, 3, 20]) {
  test(`Golden fills at x = ${x} (0 gaps, 0 overlaps)`, () => assert.deepEqual(pointTest(goldenFamily(2, x), PHI), { gaps: 0, doubled: 0 }));
}
test('Keyed fills (Lotus Jewel Axes + Dodecaxes)', () => assert.deepEqual(pointTest(goldenPieces(2, { pattern: 'allKeyed' }), PHI), { gaps: 0, doubled: 0 }));
for (const t of [...DELIAN_STOPS.map((s) => s.v), 0.05, 0.2, 0.42, 0.6, 0.9]) {
  test(`Delian fills at t = ${t.toFixed(6)} (0 gaps, 0 overlaps)`, () => assert.deepEqual(pointTest(delianFamily(3, t), 1), { gaps: 0, doubled: 0 }));
}

test('the stops: Kelvin equal pieces, τ = Icosaxes + Unborn Axes, and the slider snaps exactly onto each stop', () => {
  const vol = ({ vertices: V, faces: F }) => F.reduce((s, f) => { for (let m = 1; m + 1 < f.length; m++) s += dot(V[f[0]], cross(V[f[m]], V[f[m + 1]])); return s; }, 0) / 6;
  const K = goldenT(1), E = K.faces.flatMap((f) => f.map((a, i) => Math.hypot(...sub(K.vertices[a], K.vertices[f[(i + 1) % f.length]]))));
  assert.ok(K.faces.length === 14 && Math.max(...E) - Math.min(...E) < 1e-12, 'x = 1: Kelvin\'s regular truncated octahedron');
  assert.ok(Math.abs(vol(goldenT(PHI)) - (1 + 2 * Math.sqrt(5) / 3)) < 1e-12 && Math.abs(vol(goldenT(1 / PHI)) - (1 + Math.sqrt(5) / 3)) < 1e-12);
  for (const [k, stops] of [['golden', GOLDEN_STOPS], ['delian', DELIAN_STOPS]]) for (const s of stops) assert.equal(DICTONIC_VIEWS[k].param.value(s.u), s.v);
  assert.match(DICTONIC_VIEWS.golden.param.caption(PHI, 'en'), /Icosaxes .*Unborn Axes/);
  assert.match(DICTONIC_VIEWS.delian.param.caption(DELIAN_STOPS.find((s) => s.key === 'bond').v, 'en'), /Samson 0\.2357 · Delilah 0\.2357/);
});
