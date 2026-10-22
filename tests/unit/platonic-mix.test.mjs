// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47): the world's geometry, checked as the paper's study checked it.
// Each piece kind has its volume (the connectors from their closed faces); for all 31 mixes the block holds every solid of the mix
// and no other, the slabs stack D, C, T/O, I with the study's heights, and random points inside the block (away from its sides) lie
// in exactly one piece (ray-cast parity, so the non-convex connectors count too). Dodecahedra never overlap (they are pieces).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PHI, WORLDS, SOLID_KINDS, TEMPLATES, buildMix, helpersOf, pieceVolume } from '../../src/app/platonic-mix-geometry.js';

const close = (a, b, msg, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} vs ${b}`);
const L = PHI * PHI / Math.SQRT2, dod = (15 + 7 * Math.sqrt(5)) / 4, roof = (dod - PHI ** 3) / 6, ico = 5 * PHI * PHI / 6;
const oct = (e) => Math.SQRT2 / 3 * e ** 3, tet = (e) => Math.SQRT2 / 12 * e ** 3;
const VOL = { D: dod, I: ico, C: 1, T: tet(1), O: oct(1), P: oct(1) / 2, Q: tet(1) / 4, 'Q′': tet(L) / 4, A: (oct(L) - ico) / 6, S: PHI ** 3 - 6 * roof, X: PHI ** 3 - roof, Y: PHI ** 3 + roof };
const MIXES = [];
for (let m = 1; m < 32; m++) MIXES.push(WORLDS.filter((_, i) => m & (1 << i)).join(''));

test('templates and every piece have their volumes', () => {
  for (const [k, F] of Object.entries(TEMPLATES)) close(pieceVolume({ faces: F }), VOL[k], k, 1e-9);
  const { pieces } = buildMix('DICTO');
  for (const p of pieces) close(pieceVolume(p), VOL[p.kind], p.kind, 1e-9);
  const O = buildMix('O').pieces;
  for (const p of O) close(pieceVolume(p), VOL[p.kind], p.kind, 1e-9);
});

test('all 31 mixes: the solids of the mix and no other, slab heights as in the study', () => {
  const H = { D: 3 * PHI, C: 1, TO: Math.SQRT2, I: L * Math.sqrt(2 / 3) };
  for (const m of MIXES) {
    const { pieces, slabs, top } = buildMix(m);
    const kinds = new Set(pieces.map((p) => p.kind));
    assert.deepEqual(SOLID_KINDS.filter((k) => kinds.has(k)), SOLID_KINDS.filter((k) => m.includes(k)), m);
    assert.deepEqual(slabs.map((s) => s.world), ['D', 'C', 'TO', 'I'].filter((w) => [...w].some((c) => m.includes(c))), `${m} order`);
    close(top, slabs.reduce((a, s) => a + H[s.world], 0), `${m} height`, 1e-9);
    if (m === 'C') assert.deepEqual(helpersOf(pieces), []);
  }
  assert.deepEqual(helpersOf(buildMix('DICTO').pieces), ['P', 'Q′', 'A', 'S', 'X', 'Y'], 'DICTO: Q only when O without T');
  assert.deepEqual(helpersOf(buildMix('O').pieces), ['P', 'Q']);
});

// ray-cast parity: is x inside the closed piece?
const DIR = [0.5377, 0.2913, 0.7912];
function crosses(o, a, b, c) {
  const e1 = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], e2 = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const p = [DIR[1] * e2[2] - DIR[2] * e2[1], DIR[2] * e2[0] - DIR[0] * e2[2], DIR[0] * e2[1] - DIR[1] * e2[0]];
  const det = e1[0] * p[0] + e1[1] * p[1] + e1[2] * p[2]; if (Math.abs(det) < 1e-12) return false;
  const tv = [o[0] - a[0], o[1] - a[1], o[2] - a[2]], u = (tv[0] * p[0] + tv[1] * p[1] + tv[2] * p[2]) / det; if (u < 0 || u > 1) return false;
  const q = [tv[1] * e1[2] - tv[2] * e1[1], tv[2] * e1[0] - tv[0] * e1[2], tv[0] * e1[1] - tv[1] * e1[0]];
  const v = (DIR[0] * q[0] + DIR[1] * q[1] + DIR[2] * q[2]) / det; if (v < 0 || u + v > 1) return false;
  return (e2[0] * q[0] + e2[1] * q[1] + e2[2] * q[2]) / det > 0;
}
function inside(x, piece) {
  let n = 0;
  for (const F of piece.faces) for (let i = 1; i + 1 < F.length; i++) if (crosses(x, F[0], F[i], F[i + 1])) n++;
  return n % 2 === 1;
}
test('all 31 mixes: points inside the block lie in exactly one piece', () => {
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (const m of MIXES) {
    const { pieces, top } = buildMix(m);
    const boxes = pieces.map((p) => { const V = p.faces.flat(); return [0, 1, 2].map((a) => [Math.min(...V.map((v) => v[a])), Math.max(...V.map((v) => v[a]))]); });
    let bad = 0;
    for (let n = 0; n < 400; n++) {
      const x = [rnd() * 2 - 1, rnd() * 2 - 1, 0.001 + rnd() * (top - 0.002)];
      let c = 0;
      pieces.forEach((p, i) => { if (boxes[i].every(([lo, hi], a) => x[a] >= lo && x[a] <= hi) && inside(x, p)) c++; });
      if (c !== 1) bad++;
    }
    assert.equal(bad, 0, `${m}: points not covered exactly once`);
  }
});

test('the world\'s slabs: each on its own from z = 0, pieces named uniquely, the same pieces as the stacked block', async () => {
  const { slabsOf, slabPieces, pieceKey } = await import('../../src/app/platonic-mix-geometry.js');
  assert.deepEqual(slabsOf(''), []);
  assert.deepEqual(slabsOf('OID'), ['D', 'TO', 'I']);
  for (const m of MIXES) {
    const whole = buildMix(m);
    let n = 0;
    for (const [i, w] of slabsOf(m).entries()) {
      const s = slabPieces(w, m, i), keys = s.pieces.map(pieceKey);
      assert.equal(new Set(keys).size, keys.length, `${m} ${w}: unique names`);
      close(s.top, whole.slabs[i].top - whole.slabs[i].z0, `${m} ${w} height`);
      const zs = s.pieces.flatMap((p) => p.faces.flat().map((v) => v[2]));
      assert.ok(Math.min(...zs) > -1e-9 && Math.max(...zs) < s.top + 1e-9, `${m} ${w}: inside its slab`);
      n += s.pieces.length;
    }
    assert.equal(n, whole.pieces.length, `${m}: same pieces`);
  }
});
