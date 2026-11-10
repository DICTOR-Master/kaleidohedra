// The Bitruncated 600-cell world (DICTO 2026-11-10; src/app/bitrunc-geometry.js, world-bitrunc.js): the stage t12's 3600 corners and
// 7200 edges sorted into 720 cells (120 truncated icosahedra, 600 truncated tetrahedra), each corner in 2 + 2 of them, the faces where
// they meet (2400 hexagons, 1200 triangles, 720 pentagons); the sweep's counts: along the generic direction (no two corner heights
// equal) 716 cells appear, 716 disappear and there are 2166 scutoid swaps, nothing else; along cell-first 1782 pairs let go and 1782
// meet, balanced at every height where no cell appears or disappears. The slices tile a closed surface; the shells and the captions.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as BT from '../../src/app/bitrunc-geometry.js';
import { stage } from '../../src/app/queen-stages-geometry.js';
import { btSweepCaption, btShadowCaption, btShellsCaption, btShells, middleSwap, bitruncPreviewEdges } from '../../src/app/world-bitrunc.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const M = BT.model();
const count = (a) => a.reduce((m, x) => ({ ...m, [x]: (m[x] ?? 0) + 1 }), {});
const dist = (p, q) => Math.hypot(...p.map((x, i) => x - q[i]));

test('the stage itself: 3600 corners and 7200 edges, the same objects as queen-stages-geometry.js builds', () => {
  assert.equal(M.CORNERS.length, 3600); assert.equal(M.EDGES.length, 7200);
  assert.equal(M.CORNERS, stage('t12').vertices); assert.equal(M.EDGES, stage('t12').edges);
});
test('720 cells: 120 truncated icosahedra (60 corners, 90 edges), 600 truncated tetrahedra (12 corners, 18 edges)', () => {
  assert.equal(M.CELLS.length, 720);
  assert.deepEqual(count(M.CELLS.map((c) => `${c.kind}:${c.corners.length}:${c.edges.length}`)), { 'TI:60:90': 120, 'tt:12:18': 600 });
  assert.equal(BT.TI_COUNT, 120);
  M.CELLS.forEach((c, i) => assert.equal(c.kind, i < 120 ? 'TI' : 'tt'));
});
test('every corner lies in exactly four cells, two of each kind', () => {
  assert.deepEqual(count(M.CELLS_AT.map((a) => `${a.length}:${a.filter((c) => c < 120).length}`)), { '4:2': 3600 });
});
test('every cell lies in one 3-space (its corners on one sphere round its centre, coplanar in 4D)', () => {
  for (const c of M.CELLS) {
    const P = c.corners.map((k) => M.CORNERS[k]), m = [0, 1, 2, 3].map((i) => P.reduce((s, p) => s + p[i], 0) / P.length), r = P.map((p) => dist(p, m));
    assert.ok(Math.max(...r) - Math.min(...r) < 1e-9);
    const n = m.map((x) => x / Math.hypot(...m));   // the cell's normal is its centre's direction
    const h = P.map((p) => p.reduce((s, x, i) => s + x * n[i], 0));
    assert.ok(Math.max(...h) - Math.min(...h) < 1e-9);
  }
});
test('the faces: 2400 hexagons (TI–tt), 1200 triangles (tt–tt), 720 pentagons (TI–TI); each a closed loop of edges', () => {
  assert.deepEqual(count(M.FACES.map((f) => `${f.kind}:${f.corners.length}:${f.cells.map((c) => (c < 120 ? 'TI' : 'tt')).join('-')}`)),
    { 'hexagon:6:TI-tt': 2400, 'triangle:3:tt-tt': 1200, 'pentagon:5:TI-TI': 720 });
  const E = new Set(M.EDGES.map(([a, b]) => `${Math.min(a, b)},${Math.max(a, b)}`));
  for (const f of M.FACES) f.loop.forEach((a, i) => { const b = f.loop[(i + 1) % f.loop.length]; assert.ok(E.has(`${Math.min(a, b)},${Math.max(a, b)}`)); });
  // a TI has 12 pentagons and 20 hexagons, a tt 4 triangles and 4 hexagons
  assert.deepEqual(count(M.CELL_FACES.map((fs) => fs.map((fi) => M.FACES[fi].corners.length).sort().join(''))), { [`${'5'.repeat(12)}${'6'.repeat(20)}`]: 120, 33336666: 600 });
  // and every edge of the stage lies in exactly three faces (three cells round each edge of a 4D solid whose corners lie in four)
  const per = new Map(); for (const f of M.FACES) f.loop.forEach((a, i) => { const b = f.loop[(i + 1) % f.loop.length], k = `${Math.min(a, b)},${Math.max(a, b)}`; per.set(k, (per.get(k) ?? 0) + 1); });
  assert.equal(per.size, 7200); assert.ok([...per.values()].every((n) => n === 3));
});

test('the generic direction: no two of the 3600 corner heights equal', () => {
  const s = BT.sweep('generic'), h = [...s.heights].sort((a, b) => a - b);
  let m = Infinity; for (let i = 1; i < h.length; i++) m = Math.min(m, h[i] - h[i - 1]);
  assert.ok(m > 1e-6, `nearest two heights ${m}`); assert.equal(s.levels.length, 3600);
  assert.ok(Math.abs(Math.hypot(...BT.GENERIC) - 1) < 1e-12);
});
test('the generic sweep: 716 cells appear, 716 disappear, 2166 scutoid swaps, nothing else', () => {
  const s = BT.sweep('generic');
  assert.deepEqual(s.totals, { levels: 3600, born: 716, died: 716, letGo: 2166, meet: 2166, swaps: 2166 });
  const kinds = count(s.events.slice(1, -1).map((e) => `${e.born.length}${e.died.length}${e.letGo.length}${e.meet.length}`));
  assert.deepEqual(kinds, { 1000: 716, '0100': 716, '0011': 2166 });
  // each swap: four distinct cells, the two letting go no longer touch, the two meeting did not touch before, all four round that corner
  s.events.forEach((e, L) => {
    if (!e.letGo.length) return;
    const four = new Set([...e.letGo[0], ...e.meet[0]]); assert.equal(four.size, 4);
    const corner = s.heights.findIndex((h) => h === s.levels[L]);
    assert.deepEqual([...four].sort((a, b) => a - b), [...M.CELLS_AT[corner]].sort((a, b) => a - b));
  });
  // the four cells at the lowest corner are there from the start, so 720 − 4 appear in the sweep
  assert.equal(s.events[0].born.length, 4); assert.equal(s.events[3599].died.length, 4);
});
test('cell-first: 1782 pairs let go and 1782 meet; balanced at every height where no cell appears or disappears', () => {
  const s = BT.sweep('cell-first');
  assert.equal(s.totals.letGo, 1782); assert.equal(s.totals.meet, 1782);
  const quiet = s.events.slice(1, -1).filter((e) => !e.born.length && !e.died.length);
  assert.ok(quiet.length > 0);
  for (const e of quiet) assert.equal(e.letGo.length, e.meet.length);
});
test('the four main directions: every pair that meets lets go again, every cell that appears disappears', () => {
  for (const d of BT.DIRECTIONS) { const s = BT.sweep(d).totals; assert.equal(s.letGo, s.meet, d); assert.equal(s.born, s.died, d); }
});

test('a slice: the cross-sections of the cells alive there tile a closed surface (every polygon side shared by exactly two)', () => {
  for (const [d, k] of [['generic', middleSwap('generic')], ['generic', 1001], ['cell-first', 60], ['vertex-first', 41]]) {
    const s = BT.sliceAt(d, k), key = (p) => p.map((x) => Math.round(x * 1e6)).join(','), sides = new Map();
    assert.equal(s.ti + s.tt, s.cells.length);
    for (const c of s.cells) {
      assert.ok(c.points.length >= 3);
      c.points.forEach((p, i) => { const q = c.points[(i + 1) % c.points.length], a = key(p), b = key(q), kk = a < b ? `${a}|${b}` : `${b}|${a}`; sides.set(kk, (sides.get(kk) ?? 0) + 1); });
    }
    assert.ok([...sides.values()].every((n) => n === 2), `${d} ${k}`);
  }
});
test('the world opens on a swap near the middle of the generic sweep, its four cells lit', () => {
  const k = middleSwap('generic'), s = BT.sliceAt('generic', k);
  assert.ok(s.event && s.event.letGo.length === 1 && s.event.meet.length === 1);
  const alive = new Set(s.cells.map((c) => c.cell));
  [...s.event.letGo[0], ...s.event.meet[0]].forEach((c) => assert.ok(alive.has(c)));
});

test('shells by graph distance from one truncated icosahedron: 1, 32, 142, 242, 232, 71', () => {
  assert.deepEqual(M.SHELLS.map((x) => x.length), [1, 32, 142, 242, 232, 71]);
  assert.equal(btShells(), 6); assert.equal(M.SHELLS.flat().length, 720);
  assert.equal(M.CELLS[M.SHELLS[0][0]].kind, 'TI');
  // the first shell: the core's 12 TI neighbours (pentagons) and 20 tt (hexagons)
  assert.deepEqual(count(M.SHELLS[1].map((c) => M.CELLS[c].kind)), { TI: 12, tt: 20 });
});
test('the Shells perspective draws the core undistorted at its true size', () => {
  const C = M.CELLS[M.CORE].corners;
  for (let i = 0; i < 20; i++) for (let j = i + 1; j < 20; j++) {
    assert.ok(Math.abs(dist(M.SHELL_POINTS[C[i]], M.SHELL_POINTS[C[j]]) - dist(M.CORNERS[C[i]], M.CORNERS[C[j]])) < 1e-9);
  }
  // the eye sits beyond the far truncated icosahedron's 3-space and no other cell's (a true Schlegel picture)
  const beyond = M.CELLS.filter((c) => {
    const P = c.corners.map((k) => M.CORNERS[k]), m = [0, 1, 2, 3].map((i) => P.reduce((s, p) => s + p[i], 0) / P.length), r = Math.hypot(...m);
    return (M.SHELL_EYE * m[0]) / r > r + 1e-12;
  });
  assert.equal(beyond.length, 1);
});
test('the cover: the core (90 edges) and the 32 cells round it', () => {
  const e = bitruncPreviewEdges(); assert.equal(e.widths.filter((w) => w === 2).length, 90); assert.ok(e.length > 90 && e.colours.length === e.length);
});

test('captions in all 7 languages: every word translated, the live counts in them', () => {
  const k = middleSwap('generic'), s = BT.sliceAt('generic', k);
  const shadow = BT.stageShadowAt('t12', 'vertex-first', 'cell-first', 0);
  for (const L of LANG_ORDER) {
    const caps = [btSweepCaption('generic', k, L), btSweepCaption('cell-first', 60, L), btSweepCaption('generic', 0, L), btSweepCaption('generic', 1, L),
      btShadowCaption({ from: 'vertex-first', to: 'cell-first', u: 0 }, shadow, L), ...[1, 2, 6].map((n) => btShellsCaption(n, L))];
    for (const c of caps) { assert.ok(!/\b(bt|wq|rq)\.[a-z]/.test(c) && !/[{}]/.test(c), `${L}: ${c}`); }
    assert.ok(caps[0].includes(String(s.event.swapFrom + 1)) && caps[0].includes('2166') && caps[0].includes(String(s.cells.length)), `${L}: ${caps[0]}`);
  }
  assert.ok(btSweepCaption('generic', k, 'en').includes(`Swap ${s.event.swapFrom + 1} of 2166: two cells let go, two meet`));
  for (const key of ['bt.note.sweep', 'bt.note.shadow', 'bt.note.shells', 'wq.link.bitrunc', 'wiz.3d.bitrunc']) for (const L of LANG_ORDER) assert.notEqual(t(key, L), key);
});
