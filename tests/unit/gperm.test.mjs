// Generalized Permutohedra (src/app/gperm-geometry.js): the six named members' face counts against the known values, the membership
// (submodularity) test with positive and negative cases, the fills-space test on known space fillers and non-fillers, the line's walls
// computed exactly and checked against the face counts, and the study's wall data (gperm-walls.js) when it is there.
// DICTO · dictospheres.com
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as G from '../../src/app/gperm-geometry.js';
import { STUDY_WALLS } from '../../src/app/gperm-walls.js';

const euler = ([v, e, f]) => v - e + f;

test('every preset has its known face counts, Euler 2, and is in the family', () => {
  for (const k of G.PRESET_KEYS) {
    const s = G.shapeOf(G.PRESETS[k]);
    assert.deepEqual(s.poly.f, G.KNOWN_F[k], `${k}: [corners, edges, faces]`);
    assert.equal(euler(s.poly.f), 2, `${k}: Euler`);
    assert.ok(s.inFamily, `${k}: submodular`);
  }
});

test('the known values themselves (independent formulas)', () => {
  // permutohedron of order n: n! corners, n!(n−1)/2 edges, 2^n − 2 faces
  assert.deepEqual(G.KNOWN_F.permutohedron, [24, 24 * 3 / 2, 2 ** 4 - 2]);
  // Loday associahedron K5 (3D): Catalan(4) = 14 corners, 21 edges, n(n−3)/2 = 9 faces for the hexagon's diagonals
  assert.deepEqual(G.KNOWN_F.associahedron, [14, 21, 6 * 3 / 2]);
  // cyclohedron W3: C(6, 3) = 20 corners, 3·20/2 = 30 edges (simple), n(n−1) = 12 faces
  assert.deepEqual(G.KNOWN_F.cyclohedron, [20, 30, 12]);
});

test('the presets are the classical shapes', () => {
  const lens = (k) => { const { poly } = G.shapeOf(G.PRESETS[k]); return poly.edges.map(([a, b]) => Math.hypot(...poly.P3[a].map((x, i) => x - poly.P3[b][i]))); };
  const same = (xs) => xs.every((x) => Math.abs(x - xs[0]) < 1e-9);
  // simplex and hypersimplex regular (all edges equal), the permutohedron all edges equal (truncated octahedron)
  for (const k of ['simplex', 'hypersimplex', 'permutohedron']) assert.ok(same(lens(k)), `${k}: equal edges`);
  // hypersimplex Δ(2,4): z_S = max(0, |S| − 2)
  const z = G.zFromY(G.PRESETS.hypersimplex);
  for (const S of G.SUBSETS) assert.equal(z[S], Math.max(0, G.popcount(S) - 2));
  // the permutohedron's faces: 6 squares and 8 hexagons; the associahedron's: 3 squares and 6 pentagons
  const sides = (k) => G.shapeOf(G.PRESETS[k]).poly.faces.map((f) => f.loop.length).sort().join('');
  assert.equal(sides('permutohedron'), '44444466666666');
  assert.equal(sides('associahedron'), '444555555');
  // the associahedron keeps exactly the interval faces
  assert.deepEqual(G.shapeOf(G.PRESETS.associahedron).poly.faces.map((f) => G.setLabel(f.S)).sort(),
    ['{1,2,3}', '{1,2}', '{1}', '{2,3,4}', '{2,3}', '{2}', '{3,4}', '{3}', '{4}'].sort());
});

test('submodularity check: positive and negative cases', () => {
  // any nonnegative y is in the family
  for (let r = 0; r < 50; r++) {
    const y = Object.fromEntries(Array.from({ length: 15 }, (_, i) => [i + 1, Math.round(Math.random() * 5)]));
    assert.ok(G.inFamily(G.zFromY(y)));
  }
  // a single negative pair term leaves it (the edge of that pair would have negative length)
  assert.ok(!G.inFamily(G.zFromY({ ...G.PRESETS.permutohedron, [0b0011]: -1 })));
  // the hypersimplex has a negative y yet is in the family
  assert.ok(G.PRESETS.hypersimplex[G.FULL] < 0 && G.inFamily(G.zFromY(G.PRESETS.hypersimplex)));
  // raising one face height past the others breaks it: z_{1} too high
  const z = G.zFromY(G.PRESETS.permutohedron); z[0b0001] += 5;
  assert.ok(!G.inFamily(z));
  // the 24 wall forms are >= 0 exactly on the family (local submodularity), on random cases both sides
  for (let r = 0; r < 200; r++) {
    const y = Object.fromEntries(Array.from({ length: 15 }, (_, i) => [i + 1, Math.round(Math.random() * 6) - 1]));
    const zz = G.zFromY(y);
    assert.equal(G.WALL_FORMS.every((f) => G.wallValue(zz, f) >= 0), G.inFamily(zz));
  }
  assert.equal(G.WALL_FORMS.length, 24);
  // the support function of a sum of simplices: h(S) = sum of y_I over I meeting S
  const y = { 0b0011: 2, 0b1100: 1, 0b0111: 3 }, h = G.supportOf(G.zFromY(y));
  for (let S = 1; S <= G.FULL; S++) assert.equal(h[S], Object.entries(y).reduce((s, [I, v]) => s + ((Number(I) & S) ? v : 0), 0));
});

test('fills space (Venkov–McMullen): the known cases', () => {
  const fills = (y) => G.shapeOf(y).fill.fills;
  assert.ok(fills(G.PRESETS.permutohedron), 'truncated octahedron fills space');
  assert.ok(fills(G.PRESETS.cube), 'parallelepiped fills space');
  // the hexagonal prism: a triangle's three segments and one more
  assert.ok(fills({ 0b0011: 1, 0b0110: 1, 0b0101: 1, 0b1001: 1 }), 'hexagonal prism fills space');
  for (const k of ['simplex', 'hypersimplex', 'cyclohedron', 'associahedron']) assert.ok(!fills(G.PRESETS[k]), `${k} does not`);
  assert.deepEqual(G.shapeOf(G.PRESETS.permutohedron).fill.belts, [6]);
  assert.deepEqual(G.shapeOf(G.PRESETS.cube).fill.belts, [4]);
  // the line: only the permutohedron end is centrally symmetric
  assert.ok(!fills(G.lineY(0.001)) && !fills(G.lineY(0.5)));
});

test('the line from the permutohedron to the associahedron: exact walls, checked against the face counts', () => {
  const walls = G.lineWalls();
  // the permutohedron lies inside the cone, so the only wall is where the line leaves it: the associahedron end, t = 1
  assert.deepEqual(walls.map((w) => w.exact), ['1/1']);
  // the forms vanishing there are those whose pair is not an interval-closed step: their (A, ab) as sets
  for (let i = 0; i <= 1000; i++) { const t = i / 1000, z = G.zFromY(G.lineY(t)); assert.ok(G.inFamily(z), `t = ${t} in the family`); }
  // face counts constant inside, dropping at the wall
  for (const t of [0, 1e-6, 0.25, 0.5, 0.75, 0.999, 1 - 1e-6]) assert.deepEqual(G.shapeOf(G.lineY(t)).poly.f, [24, 36, 14], `t = ${t}`);
  assert.deepEqual(G.shapeOf(G.lineY(1)).poly.f, [14, 21, 9]);
  // the five faces that vanish at the wall
  const at1 = new Set(G.shapeOf(G.lineY(1)).poly.faces.map((f) => f.S));
  assert.deepEqual(G.SUBSETS.filter((S) => !at1.has(S)).map(G.setLabel), ['{1,3}', '{1,4}', '{2,4}', '{1,2,4}', '{1,3,4}']);
});

test('the study\'s wall data, when it is there, agrees with the live computation', () => {
  if (!STUDY_WALLS) return;
  const live = G.lineWalls().map((w) => w.t);
  assert.equal(STUDY_WALLS.length, live.length);
  STUDY_WALLS.forEach((w, i) => assert.ok(Math.abs(w.t - live[i]) < 1e-12, `wall ${i}`));
});
