// The White Queen 600-cell (DICTO 2026-10-27, paper #63; src/app/white-queen-geometry.js): the exact source model (120 vertices, 720
// edges, 1200 triangles, 600 cells), the four main directions' shadows against #62/#63 (vertex-first 42 vertices · 80 triangles; edge-
// first 52 · 60 + 20 four-sided; face-first 56 · 84 + 12; cell-first 44 · 72 + 6), and shadows never lengthening an edge, along the path.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import SRC from '../../src/app/white-queen-data.js';
import { VERTICES, EDGES, TRIANGLES, CELLS, EDGE_LENGTH, UNIT_DIRECTIONS, DIRECTIONS, viewAt, shadowAt } from '../../src/app/white-queen-geometry.js';
import { WQ_STOPS } from '../../src/app/world-white-queen.js';

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
test('the four shadows: hull vertices and faces as #62/#63', () => {
  WQ_STOPS.forEach(({ key, u }) => {
    const s = shadowAt(u / 1000);
    assert.deepEqual([s.vertices.length, s.triangles, s.quads, s.others], [...EXPECT[key], 0], key);
    assert.equal(s.vertices.length - (s.faces.reduce((a, f) => a + f.length, 0) / 2) + s.faces.length, 2, `${key}: Euler`);
  });
});

test('the frame stays orthonormal and orthogonal to u, and shadows never lengthen an edge (along the whole path)', () => {
  for (let k = 0; k <= 300; k++) {
    const t = k / 100, { u, frame } = viewAt(t), s = shadowAt(t);
    close(Math.hypot(...u), 1, `|u| at ${t}`);
    frame.forEach((f, i) => { close(f.reduce((a, x, n) => a + x * u[n], 0), 0, `f${i}·u at ${t}`); frame.forEach((g, j) => close(f.reduce((a, x, n) => a + x * g[n], 0), i === j ? 1 : 0, `f${i}·f${j} at ${t}`)); });
    for (const [i, j] of EDGES) assert.ok(dist(s.P[i], s.P[j]) <= EDGE_LENGTH + 1e-12, `edge ${i}-${j} at ${t}`);
  }
});

test('the path is continuous through each stop', () => {
  for (const st of [1, 2]) {
    const a = viewAt(st - 1e-7), b = viewAt(st), c = viewAt(st + 1e-7);
    for (const [p, q] of [[a, b], [b, c]]) { assert.ok(dist(p.u, q.u) < 1e-6); p.frame.forEach((f, i) => assert.ok(dist(f, q.frame[i]) < 1e-6, `frame at ${st}`)); }
  }
});
