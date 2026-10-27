// The White Queen 600-cell (DICTO 2026-10-27, paper #63; src/app/white-queen-geometry.js): the exact source model (120 vertices, 720
// edges, 1200 triangles, 600 cells), the four main directions' shadows against #62/#63 (vertex-first 42 vertices · 80 triangles; edge-
// first 52 · 60 + 20 four-sided; face-first 56 · 84 + 12; cell-first 44 · 72 + 6), each of the six turnings (either way) starting and
// ending at those counts, and shadows never lengthening an edge along every turning.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import SRC from '../../src/app/white-queen-data.js';
import { VERTICES, EDGES, TRIANGLES, CELLS, EDGE_LENGTH, UNIT_DIRECTIONS, DIRECTIONS, PAIRS, viewAt, shadowAt } from '../../src/app/white-queen-geometry.js';

const close = (a, b, m) => assert.ok(Math.abs(a - b) < 1e-9, `${m}: ${a} vs ${b}`);
const dist = (p, q) => Math.hypot(...p.map((x, i) => x - q[i]));

test('the source model: 120 / 720 / 1200 / 600, its own checks passed, exact = float', () => {
  assert.equal(VERTICES.length, 120); assert.equal(EDGES.length, 720); assert.equal(TRIANGLES.length, 1200); assert.equal(CELLS.length, 600);
  assert.equal(SRC.checks.length, 13); assert.ok(SRC.checks.every((c) => c.pass));
  VERTICES.forEach((v, i) => { close(Math.hypot(...v), 2, `vertex ${i} radius`); v.forEach((x, k) => close(x, SRC.vertices[i][k], `vertex ${i} exact vs float`)); });
  EDGES.forEach(([i, j]) => close(dist(VERTICES[i], VERTICES[j]), EDGE_LENGTH, `edge ${i}-${j}`));
});

test('the four main directions are the source elements\' centres', () => {
  DIRECTIONS.forEach((k, n) => {
    const el = SRC.directions[k].element, c = [0, 1, 2, 3].map((a) => el.reduce((s, i) => s + VERTICES[i][a], 0) / el.length), l = Math.hypot(...c);
    c.forEach((x, a) => close(x / l, UNIT_DIRECTIONS[n][a], `${k} axis ${a}`));
  });
});

const EXPECT = { 'vertex-first': [42, 80, 0], 'edge-first': [52, 60, 20], 'face-first': [56, 84, 12], 'cell-first': [44, 72, 6] };
const counts = (s) => [s.vertices.length, s.triangles, s.quads, s.others];
test('the four shadows: hull vertices and faces as #62/#63', () => {
  DIRECTIONS.forEach((key) => {
    const s = shadowAt(key, key, 0);
    assert.deepEqual(counts(s), [...EXPECT[key], 0], key);
    assert.equal(s.vertices.length - (s.faces.reduce((a, f) => a + f.length, 0) / 2) + s.faces.length, 2, `${key}: Euler`);
  });
});

test('six turnings, one per pair of main directions, each starting and ending at the right counts (both ways)', () => {
  assert.equal(PAIRS.length, 6);
  assert.deepEqual(new Set(PAIRS.map((p) => p.join())).size, 6);
  for (const [a, b] of PAIRS) {
    for (const [from, to] of [[a, b], [b, a]]) {
      assert.deepEqual(counts(shadowAt(from, to, 0)), [...EXPECT[from], 0], `${from} → ${to} at its start`);
      assert.deepEqual(counts(shadowAt(from, to, 1)), [...EXPECT[to], 0], `${from} → ${to} at its end`);
      const mid = viewAt(from, to, 0.5).u, A = UNIT_DIRECTIONS[DIRECTIONS.indexOf(from)], B = UNIT_DIRECTIONS[DIRECTIONS.indexOf(to)];
      const sum = A.map((x, i) => x + B[i]), l = Math.hypot(...sum);
      mid.forEach((x, i) => close(x, sum[i] / l, `${from} → ${to}: halfway on the great circle`));
    }
  }
});

test('the frame stays orthonormal and orthogonal to u, and shadows never lengthen an edge (along every turning)', () => {
  for (const [from, to] of PAIRS) {
    for (let k = 0; k <= 60; k++) {
      const x = k / 60, { u, frame } = viewAt(from, to, x), s = shadowAt(from, to, x);
      close(Math.hypot(...u), 1, `|u| ${from} → ${to} at ${x}`);
      frame.forEach((f, i) => { close(f.reduce((a, y, n) => a + y * u[n], 0), 0, `f${i}·u at ${x}`); frame.forEach((g, j) => close(f.reduce((a, y, n) => a + y * g[n], 0), i === j ? 1 : 0, `f${i}·f${j} at ${x}`)); });
      for (const [i, j] of EDGES) assert.ok(dist(s.P[i], s.P[j]) <= EDGE_LENGTH + 1e-12, `${from} → ${to}: edge ${i}-${j} at ${x}`);
    }
  }
});

test('a turning starts in its start direction\'s own frame (no jump on picking it)', () => {
  for (const [from, to] of PAIRS) {
    const a = viewAt(from, to, 0), b = viewAt(from, to, 1e-7);
    a.frame.forEach((f, i) => assert.ok(dist(f, b.frame[i]) < 1e-6));
    assert.deepEqual(a.frame, viewAt(from, from, 0).frame);
  }
});

// The Slice view against #63's atlas (white-queen-atlas.json: the 62 entries of study 2026-10-27-white-queen-600/data/atlas600.json,
// fields as there): the same stops in the same order, the same exact height strings, and every live slice with exactly the atlas's
// vertices and face sizes (the tips: the same dimension and points). This is the check that the app shows the paper's slices.
import { readFileSync } from 'node:fs';
import { SLICE_STOPS, sliceAt, q5String } from '../../src/app/white-queen-geometry.js';
const ATLAS = JSON.parse(readFileSync(new URL('./white-queen-atlas.json', import.meta.url)));
test('all 62 slices of the atlas, live from the source: stops, heights, vertices and face sizes', () => {
  assert.equal(ATLAS.length, 62);
  assert.deepEqual(SLICE_STOPS.map((s) => s.length), [9, 17, 21, 15]);
  DIRECTIONS.forEach((dir, n) => {
    const E = ATLAS.filter((e) => e.direction === dir);
    assert.equal(E.length, SLICE_STOPS[n].length, dir);
    E.forEach((e, k) => {
      const s = sliceAt(dir, k), tag = `${dir} ${e.height}`;
      assert.equal(s.stop.height, e.height, `${tag}: exact height`); close(s.stop.value, e.h, `${tag}: height`);
      assert.equal(s.stop.atVertex, e.at_vertex_layer, `${tag}: at a vertex height`);
      assert.equal(s.stop.tip, k === E.length - 1, `${tag}: tip`);
      if (e.dim !== undefined) { assert.equal(s.dim, e.dim, `${tag}: tip dimension`); assert.equal(s.points.length, e.V, `${tag}: tip points`); return; }
      assert.equal(s.dim, 3, tag);
      assert.equal(s.vertices.length, e.V, `${tag}: vertices`);
      assert.equal(s.faces.length, e.F, `${tag}: faces`);
      const fs = {}; for (const f of s.faces) fs[f.length] = (fs[f.length] ?? 0) + 1;
      assert.deepEqual(Object.fromEntries(Object.entries(fs).map(([a, b]) => [a, b])), e.face_sizes, `${tag}: face sizes`);
    });
  });
});
test('Humpty Dumpty (cell-first, 1 + 1/2√5): 48 vertices, 92 triangles; Shadow-17 (edge-first, 1 + √5): 17 vertices, 30 triangles', () => {
  for (const [dir, h, V, T] of [['cell-first', '1 + 1/2√5', 48, 92], ['edge-first', '1 + √5', 17, 30]]) {
    const k = SLICE_STOPS[DIRECTIONS.indexOf(dir)].findIndex((s) => s.height === h), s = sliceAt(dir, k);
    assert.ok(k >= 0 && s.stop.atVertex); assert.equal(s.vertices.length, V); assert.equal(s.faces.length, T); assert.ok(s.faces.every((f) => f.length === 3));
  }
  assert.equal(q5String([[-1, 2], [1, 2]]), '-1/2 + 1/2√5'); assert.equal(q5String([[0, 1], [1, 1]]), '√5'); assert.equal(q5String([[1, 4], [0, 1]]), '1/4');
});

// Cleo shells (W4b; study cleo_shells.py): the 600 cells round one vertex in 15 shells by the height of their centres, in perspective
// from height −21/10; each shell one kind of piece (sorted squared edge lengths in the view, floats to 1e-9), the core the 20 cells at
// the vertex with the apex at the centre and its 12 base corners equidistant from it.
import { CLEO_SHELLS, CLEO_POINTS, CLEO_EYE, halves } from '../../src/app/white-queen-geometry.js';
test('Cleo shells: 15 shells of 20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20, each one kind; the Cleo core', () => {
  assert.equal(CLEO_EYE, -2.1);
  assert.deepEqual(CLEO_SHELLS.map((s) => s.cells.length), [20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20]);
  assert.equal(new Set(CLEO_SHELLS.flatMap((s) => s.cells)).size, 600);
  const d2 = (p, q) => p.reduce((s, x, i) => s + (x - q[i]) ** 2, 0);
  CLEO_SHELLS.forEach((sh, k) => {
    const kinds = sh.cells.map((ci) => { const c = CELLS[ci], L = []; for (let a = 0; a < 4; a++) for (let b = a + 1; b < 4; b++) L.push(d2(CLEO_POINTS[c[a]], CLEO_POINTS[c[b]])); return L.sort((x, y) => x - y); });
    kinds.forEach((L) => L.forEach((x, i) => assert.ok(Math.abs(x - kinds[0][i]) <= 1e-9 * Math.max(1, x), `shell ${k}: one kind`)));
  });
  const core = CLEO_SHELLS[0].cells, apex = 0;   // vertex 0 is v = (2, 0, 0, 0)
  assert.ok(core.every((ci) => CELLS[ci].includes(apex)), 'the core: the 20 cells at v');
  CLEO_POINTS[apex].forEach((x) => close(x, 0, 'apex at the centre'));
  const base = [...new Set(core.flatMap((ci) => CELLS[ci]))].filter((k) => k !== apex);
  assert.equal(base.length, 12);
  base.forEach((k) => close(Math.hypot(...CLEO_POINTS[k]), Math.hypot(...CLEO_POINTS[base[0]]), '12 base corners equidistant'));
});

// Halves (W5; study front_cells_exact.py): front / back / side-on cells in the four main views.
test('Halves: front, back and side-on cells in the four main views', () => {
  const EXP = { 'vertex-first': [270, 270, 60], 'edge-first': [290, 290, 20], 'face-first': [288, 288, 24], 'cell-first': [273, 273, 54] };
  for (const dir of DIRECTIONS) { const h = halves(viewAt(dir, dir, 0).u); assert.deepEqual([h.front.length, h.back.length, h.side.length], EXP[dir], dir); }
});
test('Halves: in each main view the front cells fill the shadow once, and so do the back cells (volumes)', () => {
  const det = (a, b, c) => a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);
  const sub = (p, q) => p.map((x, i) => x - q[i]);
  for (const dir of DIRECTIONS) {
    const s = shadowAt(dir, dir, 0), h = halves(s.u), c0 = s.points[0];
    let hullVol = 0;
    for (const f of s.faces) for (let i = 1; i + 1 < f.length; i++) hullVol += det(sub(s.points[f[0]], c0), sub(s.points[f[i]], c0), sub(s.points[f[i + 1]], c0)) / 6;
    const vol = (list) => list.reduce((t, ci) => { const [a, b, c, d] = CELLS[ci].map((k) => s.P[k]); return t + Math.abs(det(sub(b, a), sub(c, a), sub(d, a))) / 6; }, 0);
    close(Math.abs(hullVol), vol(h.front), `${dir}: front`); close(Math.abs(hullVol), vol(h.back), `${dir}: back`);
    close(vol(h.side), 0, `${dir}: side-on cells are flat`);
  }
});
