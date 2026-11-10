// The 4D Permutohedron (DICTO 2026-11-10; src/app/perm4-data.js, perm4-geometry.js, world-perm4.js): the page's model checked from
// scratch: its 120 corners are the 120 orderings of (1, …, 5) (itertools order) placed isometrically; 240 edges (orderings differing by a
// swap of two neighbouring values); 30 cells, 10 truncated octahedra (24 corners) and 20 hexagonal prisms (12), each the orderings whose
// values on a subset S are the smallest; every corner in 4 cells. The sweep recomputed along the page's direction (0.26, 0.53, −0.72,
// 0.36 normalised): 26 births, 66 swaps, 26 deaths, as the page's own events; the Build and Sweep views and captions in 7 languages.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as PM from '../../src/app/perm4-geometry.js';
import { pmCaption, perm4PreviewEdges } from '../../src/app/world-perm4.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const perms = (() => { const out = [], go = (p, rest) => { if (!rest.length) out.push(p); rest.forEach((x, i) => go([...p, x], [...rest.slice(0, i), ...rest.slice(i + 1)])); }; go([], [1, 2, 3, 4, 5]); return out; })();
const dist = (a, b) => Math.hypot(...a.map((x, i) => x - b[i]));
const count = (a) => a.reduce((m, x) => ({ ...m, [x]: (m[x] ?? 0) + 1 }), {});

test('120 corners: the orderings of 1..5, every distance as between the orderings', () => {
  assert.equal(PM.X.length, 120);
  for (let i = 0; i < 120; i++) for (let j = i + 1; j < 120; j += 7) assert.ok(Math.abs(dist(PM.X[i], PM.X[j]) - dist(perms[i], perms[j])) < 1e-5);
});
test('240 edges: the orderings differing by swapping two neighbouring values', () => {
  const E = new Set(PM.EDGES.map(([a, b]) => `${Math.min(a, b)},${Math.max(a, b)}`));
  const want = [];
  for (let i = 0; i < 120; i++) for (let j = i + 1; j < 120; j++) { const d = perms[i].map((x, k) => Math.abs(x - perms[j][k])).sort(); if (d.join() === '0,0,0,1,1') want.push(`${i},${j}`); }
  assert.equal(PM.EDGES.length, 240); assert.equal(want.length, 240); assert.ok(want.every((k) => E.has(k)));
});
test('30 cells: 10 truncated octahedra and 20 hexagonal prisms, each the orderings with the smallest values on S; every corner in 4', () => {
  assert.deepEqual(count(PM.CELLS.map((c) => `${c.kind}:${c.V.length}:${c.F.length}`)), { 'TO:24:14': 10, 'HP:12:8': 20 });
  for (const c of PM.CELLS) {
    const k = c.S.length, want = perms.map((p, i) => (new Set(c.S.map((s) => p[s])).size === k && c.S.every((s) => p[s] <= k) ? i : -1)).filter((i) => i >= 0);
    assert.deepEqual([...c.V].sort((a, b) => a - b), want); assert.equal(c.kind, k === 1 || k === 4 ? 'TO' : 'HP');
  }
  const per = new Array(120).fill(0); PM.CELLS.forEach((c) => c.V.forEach((v) => per[v]++)); assert.ok(per.every((n) => n === 4));
});
test('the sweep, recomputed: 26 births, 66 swaps, 26 deaths along the page direction, and the same as the page\'s events', () => {
  const d0 = [0.26, 0.53, -0.72, 0.36], l = Math.hypot(...d0);
  d0.forEach((x, i) => assert.ok(Math.abs(x / l - PM.SWEEP_D[i]) < 1e-12));
  const H = PM.HEIGHTS, span = (vs) => [Math.min(...vs.map((v) => H[v])), Math.max(...vs.map((v) => H[v]))];
  const state = (z) => ({ alive: new Set(PM.CELLS.map((c, i) => { const [a, b] = span(c.V); return a < z && z < b ? i : -1; }).filter((i) => i >= 0)),
    pairs: new Set(PM.PAIRS.filter(([, , f]) => { const [a, b] = span(f); return a < z && z < b; }).map(([a, b]) => `${a},${b}`)) });
  let prev = state(PM.GAPS[0]), born = 0, died = 0, swaps = 0;
  for (let k = 1; k < PM.GAPS.length; k++) {
    const cur = state(PM.GAPS[k]), ev = PM.EVENTS[k - 1];
    const lost = [...prev.pairs].filter((p) => !cur.pairs.has(p) && p.split(',').every((c) => cur.alive.has(+c)));
    const gained = [...cur.pairs].filter((p) => !prev.pairs.has(p) && p.split(',').every((c) => prev.alive.has(+c)));
    const b = [...cur.alive].filter((c) => !prev.alive.has(c)), dd = [...prev.alive].filter((c) => !cur.alive.has(c));
    born += b.length; died += dd.length; if (lost.length && gained.length) swaps++;
    assert.deepEqual([lost.length, gained.length, b.length, dd.length], [ev.lost.length, ev.gained.length, ev.born.length, ev.died.length], `event ${k - 1}`);
    prev = cur;
  }
  assert.deepEqual({ born, died, swaps }, { born: 26, died: 26, swaps: 66 });
  assert.equal(PM.SWAP_TOTAL, 66); assert.equal(PM.GAPS.length, 119);
  const h = [...H].sort((a, b) => a - b); for (let i = 1; i < 120; i++) assert.ok(h[i] - h[i - 1] > 1e-6);
});
test('Build: the outer shell is one truncated octahedron, the 29 others inside it; pull moves the inner cells out', () => {
  const all = PM.buildCells('all', 0);
  assert.equal(all.length, 30); assert.equal(all.filter((c) => c.outer).length, 1); assert.equal(all.find((c) => c.outer).kind, 'TO');
  assert.ok(Math.abs(Math.max(...PM.BUILD_POINTS.map((p) => Math.hypot(...p))) - 1) < 1e-12);
  assert.equal(PM.buildCells('to', 0).length, 10); assert.equal(PM.buildCells('hp', 0).length, 20);
  const r = (cs) => Math.max(...cs.filter((c) => !c.outer).flatMap((c) => c.faces.flat()).map((p) => Math.hypot(...p)));
  assert.ok(r(PM.buildCells('all', 0.45)) > r(all));
});
test('Sweep: the cut at a swap, its cells and its counts; Next swap', () => {
  const k = PM.nextSwap(59), s = PM.sweepAt(k, 'all');
  assert.equal(s.what, 'swap'); assert.equal(s.cells.filter((c) => c.role === 'go').length, 2); assert.equal(s.cells.filter((c) => c.role === 'meet').length, 2);
  assert.equal(s.alive, s.to + s.hp); assert.equal(s.swap, PM.swapsUpTo(k));
  let n = 0, j = 0; for (;;) { const x = PM.nextSwap(j); if (x === j) break; j = x; n++; } assert.equal(n, 66);
});
test('captions and words in all 7 languages', () => {
  for (const L of LANG_ORDER) {
    for (const v of [{ mode: 'build', kind: 'all' }, { mode: 'build', kind: 'to' }, { mode: 'sweep', kind: 'all', gap: PM.nextSwap(59) }, { mode: 'sweep', kind: 'hp', gap: 0 }]) {
      const c = pmCaption(v, L); assert.ok(!/\bpm\.[a-z]/.test(c) && !/[{}]/.test(c), `${L}: ${c}`);
    }
    for (const key of ['pm.note.build', 'pm.note.sweep', 'wiz.3d.perm4', 'pm.next', 'pm.play']) assert.notEqual(t(key, L), key);
  }
  const k = PM.nextSwap(59), s = PM.sweepAt(k, 'all');
  assert.equal(pmCaption({ mode: 'sweep', kind: 'all', gap: k }, 'en'), `corner ${k} of 119 · swap ${s.swap} of 66: two cells let go, two meet · ${s.alive} cells in the cut (${s.to} truncated octahedra, ${s.hp} prisms)`);
});
test('the cover: all 240 edges', () => { const e = perm4PreviewEdges(); assert.equal(e.length, 240); assert.equal(e.colours.length, 240); });
