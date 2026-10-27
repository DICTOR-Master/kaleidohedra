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
