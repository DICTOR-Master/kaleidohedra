// Generalized Permutohedra (src/app/gperm-geometry.js): the six named members' face counts against the known values, the membership
// (submodularity) test with positive and negative cases, the fills-space test on known space fillers and non-fillers, the line's walls
// computed exactly and checked against the face counts, and the study's wall data (gperm-walls.js) when it is there.
// DICTO · dictospheres.com
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as G from '../../src/app/gperm-geometry.js';
import { STUDY } from '../../src/app/gperm-walls.js';

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

test('the staged route: one face at a time, every point in the family, exact walls and face counts', () => {
  const lab = G.STAGE_ORDER.map(G.setLabel);
  assert.deepEqual(lab, ['{1,3}', '{1,4}', '{2,4}', '{1,2,4}', '{1,3,4}']);
  assert.deepEqual(G.STAGE_DEFICITS, [1, 1, 1, 2, 2]);
  assert.deepEqual(G.STAGE_WALLS.map((w) => w.s), [1, 2, 3, 5, 7]);
  // exactly in the family: the heights are integers at every stage end and the 24 wall forms (exact integers) are >= 0 there;
  // membership is convex and each stage is a straight segment, so the whole route is in the family
  const ends = [0, ...G.STAGE_WALLS.map((w) => w.s)];
  for (const s of ends) { const z = G.stagedZ(s); assert.ok(z.every(Number.isInteger)); assert.ok(G.WALL_FORMS.every((f) => G.wallValue(z, f) >= 0), `s = ${s}`); }
  // and densely, as a check of the code path
  for (let v = 0; v <= 700; v++) assert.ok(G.inFamily(G.stagedZ(v / 100)), `v = ${v}`);
  // each stage moves only its face; the others hold
  for (let k = 0; k < 5; k++) {
    const a = G.stagedZ(ends[k]), b = G.stagedZ(ends[k + 1]);
    assert.deepEqual(G.SUBSETS.filter((S) => a[S] !== b[S]), [G.STAGE_ORDER[k]]);
  }
  // face counts at the stage ends, and that the stage's face holds until its wall and vanishes there
  const F = [[24, 36, 14], [21, 32, 13], [18, 28, 12], [15, 24, 11], [15, 23, 10], [14, 21, 9]];
  ends.forEach((s, k) => assert.deepEqual(G.polytope(G.stagedZ(s)).f, F[k], `stage end ${k}`));
  for (let k = 0; k < 5; k++) {
    const S = G.STAGE_ORDER[k], before = G.polytope(G.stagedZ(ends[k + 1] - 1e-3)), at = G.polytope(G.stagedZ(ends[k + 1]));
    assert.equal(before.faces.length, 14 - k); assert.ok(before.faces.some((f) => f.S === S));
    assert.equal(at.faces.length, 13 - k); assert.ok(!at.faces.some((f) => f.S === S));
    const z = G.stagedZ(ends[k + 1]), tight = at.X.filter((x) => Math.abs(x.reduce((t, v, j) => t + (S & (1 << j) ? v : 0), 0) - z[S]) < 1e-9);
    // the three pair faces (squares) shrink to a corner, the two triple faces to an edge
    assert.equal(tight.length, G.popcount(S) === 2 ? 1 : 2, `${G.setLabel(S)} shrinks to a ${G.popcount(S) === 2 ? 'corner' : 'edge'}`);
  }
  // the end is the associahedron; only the permutohedron end fills space
  assert.deepEqual(G.stagedZ(7), G.zFromY(G.PRESETS.associahedron));
  assert.ok(G.shapeOfZ(G.stagedZ(0)).fill.fills);
  for (let v = 1; v <= 700; v += 7) assert.ok(!G.shapeOfZ(G.stagedZ(v / 100)).fill.fills);
});

test('which orders work: 16 of 120, and {1,2,4}, {1,3,4} can never go first', () => {
  const zP = G.zFromY(G.PRESETS.permutohedron), zL = G.zFromY(G.PRESETS.associahedron), NI = G.STAGE_ORDER;
  const ok = (z) => G.WALL_FORMS.every((f) => G.wallValue(z, f) >= 0);
  const perms = (a) => (a.length ? a.flatMap((x, i) => perms([...a.slice(0, i), ...a.slice(i + 1)]).map((p) => [x, ...p])) : [[]]);
  const good = perms(NI).filter((ord) => { const z = [...zP]; return ord.every((S) => { z[S] = zL[S]; return ok(z); }); });
  assert.equal(good.length, 16);
  for (const S of NI) { const z = [...zP]; z[S] = zL[S]; assert.equal(ok(z), G.popcount(S) === 2, `${G.setLabel(S)} alone first`); }
});

test('the k-research study (gperm-walls.js) agrees with this geometry', () => {
  assert.ok(STUDY.allChecksOk);
  const zP = G.zFromY(G.PRESETS.permutohedron), zL = G.zFromY(G.PRESETS.associahedron), fr = (x) => { const [a, b = '1'] = String(x).split('/'); return Number(a) / Number(b); };
  for (const S of [...G.SUBSETS, G.FULL]) {
    const L = G.setLabel(S), n = G.popcount(S);
    // the study's frame is this one moved by (1, 1, 1, 1): each height + |S|
    assert.equal(fr(STUDY.zStart[L]), zP[S] + n, `start ${L}`); assert.equal(fr(STUDY.zEnd[L]), zL[S] + n, `end ${L}`);
    if (S !== G.FULL) assert.equal(STUDY.interval[L], zP[S] === zL[S], `interval ${L}`);
  }
  // its straight line: one wall at t = 1, the same 5 faces, the same face counts as here
  assert.deepEqual(STUDY.lineA.map((w) => w.param), ['1']);
  assert.deepEqual(G.lineWalls().map((w) => w.exact), ['1/1']);
  assert.deepEqual([...STUDY.lineA[0].faces].sort(), G.STAGE_ORDER.map(G.setLabel).sort());
  assert.deepEqual(STUDY.lineA[0].fAt, G.KNOWN_F.associahedron);
  // its equal-speed line: the faces with deficit 1 go at s = 1, those with 2 at s = 2 (the same deficits the staged route uses)
  assert.deepEqual(STUDY.lineB.map((w) => [w.param, [...w.faces].sort()]), [['1', ['{1,3}', '{1,4}', '{2,4}']], ['2', ['{1,2,4}', '{1,3,4}']]]);
  G.STAGE_ORDER.forEach((S, k) => assert.equal(G.STAGE_DEFICITS[k], fr(STUDY.zStart[G.setLabel(S)]) - fr(STUDY.zEnd[G.setLabel(S)])));
});
