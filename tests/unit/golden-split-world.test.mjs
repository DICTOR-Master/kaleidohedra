// The octet world's Golden split (DICTO 2026-10-23; src/app/world-octet.js goldenPieces, geometry krp-core golden-split.js): the pieces
// the world draws fill space with 0 gaps and 0 overlaps (point test, winding numbers) for every pattern, with and without Swap, at block
// sizes 1 and 2, and after single hexagons are tapped; under X-ray the parts (cores, AXE pyramids, mirrored keys) fill the same space;
// whole pieces have real flat faces (big smooth: 8 hexagons + 6 squares); a tap steps a hexagon flat → into the big → into the small.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { goldenPieces, gsState, gsNext, GS_PATTERNS } from '../../src/app/world-octet.js';

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
function pointTest(list, samples = 2500) {
  let seed = 11, gaps = 0, doubled = 0;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const near = list.map(([, V, F, , x]) => ({ V, F, c: x.anchor }));
  for (let k = 0; k < samples; k++) {
    const p = [rnd(), rnd(), rnd()].map((q) => (q * 2 - 1) * PHI);   // two cells across round the middle, well inside size 2
    const cover = near.reduce((t, q) => (Math.hypot(...sub(p, q.c)) < 1.3 ? t + winding(q.V, q.F, p) : t), 0);
    if (cover === 0) gaps++; else if (cover > 1) doubled++;
  }
  return { gaps, doubled };
}

test('whole pieces have flat faces: the smooth big piece 8 hexagons + 6 squares, the keyed small one 6 squares + 48 triangles', () => {
  const sm = goldenPieces(1, { pattern: 'smooth' }), ak = goldenPieces(1, { pattern: 'allKeyed' });
  const big = sm.find((p) => p[0] === 'gsBig'), small = ak.find((p) => p[0] === 'gsSmall');
  assert.deepEqual([big[2].filter((f) => f.length === 6).length, big[2].filter((f) => f.length === 4).length, big[2].length], [8, 6, 14]);
  assert.deepEqual([small[2].filter((f) => f.length === 4).length, small[2].filter((f) => f.length === 3).length], [6, 48]);
  assert.equal(big[4].tags.filter(Boolean).length, 8, 'each hexagon tagged for taps, squares not');
});

for (const pattern of GS_PATTERNS) for (const swap of [false, true]) for (const block of pattern === 'checker' || pattern === 'pyrochlore' ? [1, 2] : [1]) {
  test(`fills: ${pattern}${swap ? ', swap' : ''}, block ${block} (0 gaps, 0 overlaps)`, () => {
    assert.deepEqual(pointTest(goldenPieces(2, { pattern, block, swap, flips: {} })), { gaps: 0, doubled: 0 });
  });
}

test('fills after taps, and under X-ray its parts fill the same space', () => {
  const o = { pattern: 'checker', block: 1, swap: false, flips: {} };
  const tags = [...new Set(goldenPieces(2, o).flatMap((p) => p[4].tags.filter(Boolean)))].filter((_, i) => i % 3 === 0);
  tags.forEach((t, i) => { o.flips[t] = i % 3; });
  assert.deepEqual(pointTest(goldenPieces(2, o)), { gaps: 0, doubled: 0 });
  const parts = goldenPieces(2, { ...o, xray: true });
  assert.ok(parts.some((p) => p[0] === 'axe') && parts.some((p) => p[0] === 'tricap'), 'AXE pyramids and mirrored keys among the parts');
  assert.deepEqual(pointTest(parts, 1500), { gaps: 0, doubled: 0 });
});

test('a tap steps a hexagon flat → into the big → into the small → flat; Swap turns the pattern keys', () => {
  const n = [1, 1, 1], s = [1, -1, 1], tag = '1,1,1|1,-1,1', o = { pattern: 'smooth', flips: {} };
  const seen = [];
  for (let k = 0; k < 4; k++) { seen.push(gsState(n, s, o)); o.flips[tag] = gsNext(tag, o); }
  assert.deepEqual(seen, [0, 1, 2, 0]);
  assert.equal(gsState(n, s, { pattern: 'allKeyed' }), 1);
  assert.equal(gsState(n, s, { pattern: 'allKeyed', swap: true }), 2);
});
