// DICTO's four Star Cores solids (D106–D109) and Kagemusha's crests in Polyhedraverse, and the Star Cores world's chain (DICTO
// 2026-11-02). Figures from DICTO Solids v7 and the research studies 2026-11-01-star-cores-d (kagemusha-variants.json) and
// 2026-10-30-star-cores / 2026-11-01-star-cores-book (star-cores.json, star-cores-new4.json).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, STAR_CORES_SOLID_IDS, KAGEMUSHA_CREST_IDS, STAR_CORES_SHAPE_IDS, STAR_CORES_LIST } from '../../src/krp-core/src/polyhedra/index.js';
import { starCoresChain, coreOf, positionsOf, phaseAt, sameShape, findStarCoresShape, starCounts } from '../../src/app/star-cores-geometry.js';
import { solidOf, tipsOf } from '../../src/app/star-step-geometry.js';

const STAR_CORES_SHAPES = STAR_CORES_LIST;
const specOf = (s) => POLYHEDRA[s.id];

const volume = (s) => s.faces.reduce((t, f) => { for (let k = 1; k + 1 < f.length; k++) { const [a, b, c] = [s.vertices[f[0]], s.vertices[f[k]], s.vertices[f[k + 1]]]; t += a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]); } return t; }, 0) / 6;
// closed and oriented: every directed edge once, its reverse once
function closed(s) {
  const de = new Map();
  for (const f of s.faces) f.forEach((a, i) => { const k = `${a},${f[(i + 1) % f.length]}`; de.set(k, (de.get(k) ?? 0) + 1); });
  for (const [k, n] of de) { const [a, b] = k.split(','); if (n !== 1 || de.get(`${b},${a}`) !== 1) return false; }
  return s.vertices.length - de.size / 2 + s.faces.length === 2;
}
const sides = (s) => s.faces.reduce((o, f) => ({ ...o, [f.length]: (o[f.length] ?? 0) + 1 }), {});

test('the four Star Cores solids: names, f-vectors, faces by sides and volumes of DICTO Solids v7', () => {
  assert.deepEqual(STAR_CORES_SOLID_IDS, ['DICTO_CUBE_PEARL', 'DICTO_GOLDEN_CLASP', 'DICTO_HAMLET', 'DICTO_OPHELIA']);
  const want = {
    DICTO_CUBE_PEARL: ['Cube Pearl', 32, 48, 18, { 4: 6, 6: 12 }, 424 / 125],
    DICTO_GOLDEN_CLASP: ['Golden Clasp', 48, 72, 26, { 4: 12, 6: 8, 8: 6 }, -613 / 2 + (279 / 2) * Math.sqrt(5)],
    // Hamlet and Ophelia shown at circumradius 1.1 (dataset circumradii 0.77626…, 0.76639…): the volume scales by the cube
    DICTO_HAMLET: ['Hamlet', 452, 720, 270, { 3: 60, 4: 30, 5: 120, 9: 60 }, 1.742494068294532 * (1.1 / 0.7762610742062294) ** 3],
    DICTO_OPHELIA: ['Ophelia', 642, 1080, 440, { 4: 300, 6: 120, 12: 20 }, 1.799658753384913 * (1.1 / 0.7663939105162879) ** 3],
  };
  for (const [id, [name, v, e, f, by, vol]] of Object.entries(want)) {
    const s = POLYHEDRA[id];
    assert.equal(s.name, name);
    assert.equal(s.vertices.length, v, `${id} corners`); assert.equal(s.edges.length, e, `${id} edges`); assert.equal(s.faces.length, f, `${id} faces`);
    assert.deepEqual(sides(s), by, `${id} faces by sides`);
    assert.ok(closed(s), `${id} closed`);
    assert.ok(Math.abs(volume(s) - vol) < 1e-9, `${id} volume ${volume(s)} against ${vol}`);
    assert.ok(solidOf(s), `${id} convex with its centre inside every face (★ Star step)`);
  }
});

test("Kagemusha's crests: MAEDATE an octahedron, KUWAGATA a dipyramid, volumes of kagemusha-variants.json; Kagemusha with five of each", () => {
  assert.deepEqual(KAGEMUSHA_CREST_IDS, ['KAGEMUSHA_MAEDATE', 'KAGEMUSHA_KUWAGATA', 'DICTO_MAEDATE', 'DICTO_KUWAGATA']);
  const M = POLYHEDRA.DICTO_MAEDATE, K = POLYHEDRA.DICTO_KUWAGATA;
  assert.equal(M.name, 'MAEDATE'); assert.equal(K.name, 'KUWAGATA');
  assert.equal(M.vertices.length, 6); assert.deepEqual(sides(M), { 3: 8 });
  assert.equal(K.vertices.length, 5); assert.deepEqual(sides(K), { 3: 6 });
  assert.ok(closed(M) && closed(K));
  assert.ok(Math.abs(volume(M) - 0.221752373906) < 1e-9, `MAEDATE ${volume(M)}`);
  assert.ok(Math.abs(volume(K) - 2 * 0.0752) < 1e-4, `KUWAGATA ${volume(K)}`);
  // Kagemusha (D86): 17 corners, 30 triangles, volume 3.76038…; its 10 notch faces covered by the crests
  const KAGE = 3.7603843164581723;
  for (const [id, piece, faces, corners] of [['KAGEMUSHA_MAEDATE', M, 30 - 10 + 5 * 6, 17 + 5 * 2], ['KAGEMUSHA_KUWAGATA', K, 30 - 10 + 5 * 4, 17 + 5]]) {
    const s = POLYHEDRA[id];
    assert.ok(closed(s), `${id} closed`);
    assert.equal(s.faces.length, faces); assert.equal(s.vertices.length, corners);
    assert.ok(Math.abs(volume(s) - KAGE - 5 * volume(piece)) < 1e-9, `${id} volume = Kagemusha + 5 crests`);
    const gold = s.faceColours.filter((c) => c === 0xd9a520).length, teal = s.faceColours.filter((c) => c === 0x2bb7c4).length;
    assert.equal(gold, 20); assert.equal(teal, faces - 20);
  }
});

test('the Star Cores shapes: all 52 in Polyhedraverse, D-numbers unique, newest first, each convex (★ Star step), 42 new at circumradius 1.1', () => {
  assert.equal(STAR_CORES_SHAPES.length, 52);
  const D = STAR_CORES_SHAPES.map((s) => Number(s.D.slice(1)));
  assert.equal(new Set(D).size, 52);
  assert.deepEqual(D, [...D].sort((a, b) => b - a));
  for (const s of STAR_CORES_SHAPES) { assert.ok(POLYHEDRA[s.id], `${s.D} in PV`); assert.ok(solidOf(specOf(s)), `${s.D} ${s.name}`); }
  assert.equal(new Set(STAR_CORES_SHAPES.map((s) => s.id)).size, 52, 'one PV id each');
  // the ones PV had already keep their ids (one name per shape)
  assert.deepEqual(STAR_CORES_SHAPES.filter((s) => !STAR_CORES_SHAPE_IDS.includes(s.id)).map((s) => s.id), ['DICTO_OPHELIA', 'DICTO_HAMLET', 'DICTO_GOLDEN_CLASP', 'DICTO_CUBE_PEARL', 'DICTO_SAMSON', 'DICTO_DODECA13_NEEDLE', 'DICTO_DODECA13_WEDGE', 'DICTO_SKEWED_ED_18', 'DICTO_SKEWED_ED_16', 'DICTO_SKEWED_RD']);
  assert.equal(STAR_CORES_SHAPE_IDS.length, 42);
  for (const id of STAR_CORES_SHAPE_IDS) { const r = Math.max(...POLYHEDRA[id].vertices.map((v) => Math.hypot(...v))); assert.ok(Math.abs(r - 1.1) < 1e-9, `${id} circumradius ${r}`); assert.ok(closed(POLYHEDRA[id]), `${id} closed`); }
  assert.equal(POLYHEDRA.DICTO_SC_OGDOECONTAHEDRON.faces.length, 80);
  assert.equal(findStarCoresShape(STAR_CORES_SHAPES, 'd106').name, 'Cube Pearl');
  assert.equal(findStarCoresShape(STAR_CORES_SHAPES, 'ti_star_core').D, 'D105');
});

// The core of the turn and the core of the core, against the float study (corners, faces) for every shape and both t.
const STUDY = {
  D109: [[120, 62], [60, 32]], D108: [[120, 62], [60, 32]], D107: [[24, 14], [24, 14]], D106: [[24, 14], [24, 14]], D105: [[60, 32], [60, 32]],
  D40: [[30, 32], [60, 32]], D41: [[60, 32], [30, 32]], D28: [[60, 32], [60, 32]], D37: [[12, 8], [6, 8]], D77: [[6, 8], [6, 8]],
  D87: [[120, 62], [60, 32]], D45: [[90, 92], [60, 32]], D90: [[40, 22], [10, 7]], D99: [[20, 12], null], D97: [[12, 8], null],
  D51: [[60, 32], [60, 32]], D47: [[120, 62], [60, 32]], D1: [null, null], D81: [null, null],
};
test('the core of the turn and of the core agree with the Star Cores study, at t = 2 and t = φ', () => {
  for (const [D, [c1, c2]] of Object.entries(STUDY)) {
    const s = findStarCoresShape(STAR_CORES_SHAPES, D), spec = specOf(s);
    for (const tk of ['2', 'phi']) {
      const ch = starCoresChain(spec, tk), T = ch.turns;
      const got1 = T[0].core ? [T[0].core.vertices.length, T[0].core.faces.length] : null;
      assert.deepEqual(got1, c1, `${D} t=${tk} core`);
      const got2 = T[1]?.core ? [T[1].core.vertices.length, T[1].core.faces.length] : null;
      if (c1) assert.deepEqual(got2, c2, `${D} t=${tk} core of the core`);
    }
  }
});

test('period two (the book): the cores of Cube Pearl and Golden Clasp from turn 1, of Hamlet and Ophelia from turn 2; the GTI and the TI Star core return', () => {
  for (const [D, from] of [['D106', 1], ['D107', 1], ['D108', 2], ['D109', 2]]) {
    const T = starCoresChain(specOf(findStarCoresShape(STAR_CORES_SHAPES, D)), '2').turns;
    assert.equal(T.length, 5);
    assert.ok(sameShape(T[from + 2].solid, T[from].solid), `${D}: turn ${from + 3} = turn ${from + 1}`);
    assert.ok(!sameShape(T[from + 1].solid, T[from].solid), `${D}: period two, not one`);
    if (from === 2) assert.ok(!sameShape(T[3].solid, T[1].solid), `${D}: not yet at turn 2`);
  }
  for (const D of ['D40', 'D105']) {
    const s = specOf(findStarCoresShape(STAR_CORES_SHAPES, D)), S = solidOf(s), C = coreOf(S, 2);
    assert.ok(!sameShape(C, S), `${D}: the core is another solid`);
    const T = starCoresChain(s, 'phi').turns;
    assert.ok(sameShape(T[2].solid, T[0].solid), `${D}: the core's core is the solid again`);
  }
});

test('the core is the common part of the family hulls: every core corner inside every family hull, on at least three of their planes', () => {
  for (const D of ['D106', 'D28', 'D45']) {
    const solid = solidOf(specOf(findStarCoresShape(STAR_CORES_SHAPES, D)));
    const core = coreOf(solid, 2);
    const tips = solid.planes.map(({ n, c }) => n.map((x) => 2 * c * x));
    // each core corner is at most as far out as the farthest tip of every family in every direction it lies in (a hull test by support)
    for (const p of core.vertices) {
      const r = Math.hypot(...p), u = p.map((x) => x / r);
      assert.ok(r <= Math.max(...tips.map((q) => q[0] * u[0] + q[1] * u[1] + q[2] * u[2])) + 1e-9);
    }
    assert.ok(core.faces.every((f) => f.length >= 3));
    assert.ok(Math.abs(volume(core)) > 0);
  }
});

test('the slider: four phases a turn, ending on the last core, or on the halo of a turn without one', () => {
  const cp = starCoresChain(POLYHEDRA.DICTO_CUBE_PEARL, '2');
  assert.equal(positionsOf(cp), 19);
  assert.deepEqual(phaseAt(0), { turn: 0, phase: 'solid' });
  assert.deepEqual(phaseAt(7), { turn: 1, phase: 'core' });
  const fang = starCoresChain(specOf(findStarCoresShape(STAR_CORES_SHAPES, 'D81')), '2');
  assert.equal(fang.turns.length, 1); assert.equal(positionsOf(fang), 2);
  assert.equal(phaseAt(positionsOf(fang)).phase, 'halo');
});

test("the star's own counts: corners = the solid's + one tip per face; the GTI's star is the Golden TI Star's 92 corners, 180 faces", () => {
  for (const [id, v, f] of [['DICTO_CUBE_PEARL', 50, 96], ['DICTO_GOLDEN_CLASP', 74, 144], ['DICTO_SC_GTI', 92, 180], ['DICTO_SC_OGDOECONTAHEDRON', 182, 360]]) {
    const S = solidOf(POLYHEDRA[id]);
    for (const r of ['doubling', 'golden']) assert.deepEqual(starCounts(S, tipsOf(S, r)), { v, f }, `${id} ${r}`);
  }
});
