// ✂ Golden Cut (golden-cut-geometry.js, paper #88): the ten golden cut values, exact, and the cut solids they make.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { PHI, GCUT_SOLIDS, GCUT_K, GCUT_STOPS, stopX, stopAt, sidesAt, gcutKeyOf, gcutKeyOfId, goldenCut, volumeOf } from '../../src/app/golden-cut-geometry.js';

const close = (a, b, msg, eps = 1e-12) => assert.ok(Math.abs(a - b) <= eps, `${msg}: ${a} vs ${b}`);
const S5 = Math.sqrt(5), S2 = Math.SQRT2, S10 = Math.sqrt(10);
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
const sides = (loop) => loop.map((p, i) => dist(p, loop[(i + 1) % loop.length]));

test('the five in D·I·C·T·O order; the slider order of the stops', () => {
  assert.deepEqual(GCUT_SOLIDS, ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']);
  assert.deepEqual(GCUT_STOPS, ['lesser', 'archimedean', 'greater']);
  for (const k of GCUT_SOLIDS) assert.ok(stopX(k, 'lesser') < stopX(k, 'archimedean') && stopX(k, 'archimedean') < stopX(k, 'greater'), k);
});

// The ten golden cuts (paper #88, golden-cuts-exact.md), as closed forms, and each cut solid's volume (edge 1).
const TEN = [
  ['dodecahedron', 'greater', 1 / 3, 1205 / 324 + 557 * S5 / 324],
  ['dodecahedron', 'lesser', (7 - S5) / 22, 20095 / 5324 + 27581 * S5 / 15972],
  ['icosahedron', 'greater', (3 - S5) / 2, -45 / 4 + 71 * S5 / 12],
  ['icosahedron', 'lesser', 1 / 2 - S5 / 10, 19 / 20 + 31 * S5 / 60],
  ['cube', 'greater', (-3 * S2 - 2 + S10 + 2 * S5) / 4, (-19 * S5 - 13 * S10 + 30 * S2) / 3 + 44 / 3],
  ['cube', 'lesser', (-2 * S5 - 2 + S10 + 3 * S2) / 4, (-30 * S2 - 13 * S10 + 19 * S5) / 3 + 44 / 3],
  ['tetrahedron', 'greater', (3 - S5) / 2, (-35 * S2 + 16 * S10) / 12],
  ['tetrahedron', 'lesser', 1 / 2 - S5 / 10, (5 * S2 + 8 * S10) / 300],
  ['octahedron', 'greater', (3 - S5) / 2, (-26 * S2 + 12 * S10) / 3],
  ['octahedron', 'lesser', 1 / 2 - S5 / 10, (10 * S2 + 6 * S10) / 75],
];
test('the ten golden cut values, exact; the long/short ratio φ; the cut solid (sides, regular corners, volume)', () => {
  // the brief's decimals for the cube
  close(stopX('cube', 'greater'), 0.347943, 'cube greater ≈ 0.347943', 5e-7);
  close(stopX('cube', 'lesser'), 0.233196, 'cube lesser ≈ 0.233196', 5e-7);
  close(1 / (PHI * PHI), (3 - S5) / 2, 'triangles greater = 1/φ²');
  close(1 / (PHI * S5), 1 / 2 - S5 / 10, 'triangles lesser = 1/(φ√5)');
  for (const [key, stop, x, vol] of TEN) {
    const name = `${key} ${stop}`;
    close(stopX(key, stop), x, `${name} x`);
    assert.equal(stopAt(key, x), stop, `${name}: the stop is found at its x`);
    const sd = sidesAt(key, x);
    close(sd.ratio, PHI, `${name}: long/short = φ`);
    assert.ok(stop === 'greater' ? sd.corner > sd.original : sd.original > sd.corner, `${name}: the right sides long`);
    const cs = goldenCut(key, x), F = POLYHEDRA[{ dodecahedron: 'DODECAHEDRON', icosahedron: 'D20', cube: 'CUBE', tetrahedron: 'D4', octahedron: 'D8' }[key]];
    assert.equal(cs.corners.length, F.vertices.length, `${name}: one corner polygon per corner`);
    assert.equal(cs.faces.length, F.faces.length, `${name}: one face per face`);
    for (const c of cs.corners) sides(c).forEach((l) => close(l, GCUT_K[key] * x, `${name}: corner side k·x`, 1e-9));
    for (const f of cs.faces) sides(f).forEach((l, i) => close(l, i % 2 ? GCUT_K[key] * x : 1 - 2 * x, `${name}: face sides alternate`, 1e-9));
    close(volumeOf([...cs.corners, ...cs.faces]), vol, `${name}: volume (paper #88)`, 1e-9);
  }
});

test('the Archimedean stop makes the Archimedean truncated solid: all sides equal, krp-core\'s volume', () => {
  const ARCH = { dodecahedron: 'TRUNCATED_DODECAHEDRON', icosahedron: 'TRUNCATED_ICOSAHEDRON', cube: 'TRUNCATED_CUBE', tetrahedron: 'TRUNCATED_TETRAHEDRON', octahedron: 'TRUNCATED_OCTAHEDRON' };
  for (const key of GCUT_SOLIDS) {
    const x = stopX(key, 'archimedean'), cs = goldenCut(key, x), side = 1 - 2 * x;
    close(sidesAt(key, x).ratio, 1, `${key}: ratio 1`);
    for (const l of [...cs.corners, ...cs.faces].flatMap(sides)) close(l, side, `${key}: every side`, 1e-9);
    const A = POLYHEDRA[ARCH[key]], e = dist(A.vertices[A.edges[0][0]], A.vertices[A.edges[0][1]]);
    const va = Math.abs(volumeOf(A.faces.map((f) => f.map((i) => A.vertices[i])))) * (side / e) ** 3;
    close(volumeOf([...cs.corners, ...cs.faces]), va, `${key}: volume of krp-core's ${ARCH[key]} at that edge`, 1e-9);
  }
});

test("the octahedron's golden stops are DICTO's Icosaxes and Unborn Axes (krp-core), up to size", () => {
  // compare sorted distances from the centre, scaled so the largest is 1
  const radii = (pts) => { const r = pts.map((p) => Math.hypot(...p)).sort((a, b) => a - b); return r.map((v) => v / r[r.length - 1]); };
  for (const [stop, id] of [['greater', 'DICTO_ICOSAXES'], ['lesser', 'DICTO_UNBORN_AXES']]) {
    const cs = goldenCut('octahedron', stopX('octahedron', stop)), S = POLYHEDRA[id];
    const m = [0, 1, 2].map((k) => S.vertices.reduce((s, v) => s + v[k], 0) / S.vertices.length);
    const mine = radii(cs.vertices), theirs = radii(S.vertices.map((v) => v.map((c, k) => c - m[k])));
    assert.equal(mine.length, theirs.length, `${id}: 24 corners`);
    // same shape: corner set similar (both centrally symmetric about the centre with the octahedral axes); check edge ratio too
    const e = (P) => { const d = []; for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) d.push(dist(P[i], P[j])); d.sort((a, b) => a - b); return d[0] / d[d.length - 1]; };
    close(e(cs.vertices), e(S.vertices), `${id}: shortest/longest corner distance`, 1e-9);
    mine.forEach((r, i) => close(r, theirs[i], `${id}: radii`, 1e-9));
    assert.equal(S.faces.length, 14, `${id}: 8 hexagons + 6 squares`);
  }
});

test('address words: names, capitals and registry ids', () => {
  assert.equal(gcutKeyOf('OCTAHEDRON'), 'octahedron');
  assert.equal(gcutKeyOf('D8'), 'octahedron');
  assert.equal(gcutKeyOf('icosahedron'), 'icosahedron');
  assert.equal(gcutKeyOf('DODECAHEDRON'), 'dodecahedron');
  assert.equal(gcutKeyOf('CUBOCTAHEDRON'), null);
  assert.equal(gcutKeyOfId('D4'), 'tetrahedron');
  assert.equal(gcutKeyOfId('TRUNCATED_CUBE'), null);
});
