// The Red Queen 120-cell (DICTO 2026-10-28, paper #65; src/app/red-queen-geometry.js), built from the White Queen: 600 corners on one
// sphere, 1200 equal edges with 4 at each corner, 720 regular pentagons each in 2 dodecahedra, 120 regular dodecahedra; the atlas's
// four directions pass through their elements; every shadow and every one of the 124 slices matches atlas120.json (corners, faces, face
// sizes); the nine cell layers 1, 12, 20, 12, 30, 12, 20, 12, 1 with the core's corners the centres of the Cleo core's 20 cells.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import RQ from '../../src/app/red-queen-data.js';
import { VERTICES, EDGES, PENTAGONS, CELLS, RADIUS, DIRECTIONS, UNIT_DIRECTIONS, SLICE_STOPS, sliceAt, shadowAt, CELL_LAYERS, halves } from '../../src/app/red-queen-geometry.js';
import { CLEO_SHELLS } from '../../src/app/white-queen-geometry.js';

const close = (a, b, m, e = 1e-9) => assert.ok(Math.abs(a - b) < e, `${m}: ${a} vs ${b}`);
const dist = (p, q) => Math.hypot(...p.map((x, i) => x - q[i]));
const sizes = (faces) => faces.reduce((m, f) => ({ ...m, [f.length]: (m[f.length] ?? 0) + 1 }), {});

test('the model: 600 corners on one sphere, 1200 equal edges, 4 at each corner', () => {
  assert.equal(VERTICES.length, 600); assert.equal(EDGES.length, 1200);
  VERTICES.forEach((v, i) => close(Math.hypot(...v), RADIUS, `corner ${i}`));
  close(RADIUS ** 2, 7 / 4 + (3 / 4) * Math.sqrt(5), 'radius² 7/4 + 3/4√5');
  EDGES.forEach(([a, b]) => close(dist(VERTICES[a], VERTICES[b]) ** 2, 1 / 4, `edge ${a}-${b}`));
  const deg = new Array(600).fill(0); EDGES.flat().forEach((k) => deg[k]++);
  assert.ok(deg.every((d) => d === 4));
});

test('720 regular pentagons, each in exactly 2 of 120 regular dodecahedra', () => {
  assert.equal(PENTAGONS.length, 720); assert.equal(CELLS.length, 120);
  for (const p of PENTAGONS) {
    assert.equal(p.length, 5);
    p.forEach((x, i) => close(dist(VERTICES[x], VERTICES[p[(i + 1) % 5]]), 0.5, 'pentagon side'));
    p.forEach((x, i) => close(dist(VERTICES[x], VERTICES[p[(i + 2) % 5]]), 0.5 * (1 + Math.sqrt(5)) / 2, 'pentagon diagonal'));
  }
  const used = new Array(720).fill(0);
  for (const c of CELLS) {
    assert.equal(c.corners.length, 20); assert.equal(c.faces.length, 12);
    c.faces.forEach((f) => { used[f]++; assert.ok(PENTAGONS[f].every((x) => c.corners.includes(x))); });
  }
  assert.ok(used.every((n) => n === 2));
});

test('the four main directions pass through the atlas elements (the highest corners)', () => {
  DIRECTIONS.forEach((k, n) => {
    const u = UNIT_DIRECTIONS[n], h = VERTICES.map((v) => v.reduce((s, x, i) => s + x * u[i], 0)), top = Math.max(...h);
    const el = RQ.directions[k].element;
    el.forEach((i) => close(h[i], top, `${k} element ${i}`));
    assert.equal(h.filter((x) => Math.abs(x - top) < 1e-9).length, el.length, `${k}: only the element at the top`);
  });
});

test('every shadow matches the atlas', () => {
  for (const k of DIRECTIONS) {
    const s = shadowAt(k, k, 0), a = RQ.shadows[k];
    assert.equal(s.vertices.length, a.V, `${k} corners`); assert.equal(s.faces.length, a.F, `${k} faces`);
    assert.deepEqual(sizes(s.faces), Object.fromEntries(Object.entries(a.face_sizes).map(([x, y]) => [x, y])), `${k} face sizes`);
  }
});

test('all 124 slices match the atlas', () => {
  assert.deepEqual(DIRECTIONS.map((k) => SLICE_STOPS[DIRECTIONS.indexOf(k)].length), DIRECTIONS.map((k) => RQ.slice_patterns[k]));
  for (const a of RQ.slices) {
    const n = DIRECTIONS.indexOf(a.direction), k = SLICE_STOPS[n].findIndex((s) => s.height === a.height);
    assert.ok(k >= 0, `${a.direction} at ${a.height}: a stop`);
    const s = sliceAt(a.direction, k);
    if (a.F) {
      assert.equal(s.dim, 3); assert.equal(s.vertices.length, a.V, `${a.direction} ${a.height} corners`); assert.equal(s.faces.length, a.F, `${a.direction} ${a.height} faces`);
      assert.deepEqual(sizes(s.faces), a.face_sizes, `${a.direction} ${a.height} face sizes`);
    } else { assert.equal(s.dim, a.dim, `${a.direction} tip`); assert.equal(s.points.length, a.V); }
  }
});

test('nine cell layers round one, the core on the Cleo core', () => {
  assert.deepEqual(CELL_LAYERS.map((l) => l.cells.length), [1, 12, 20, 12, 30, 12, 20, 12, 1]);
  assert.deepEqual([...CELLS[CELL_LAYERS[0].cells[0]].corners].sort((a, b) => a - b), [...CLEO_SHELLS[0].cells].sort((a, b) => a - b));
});

test('halves: in each main view the front and back dodecahedra balance', () => {
  for (const u of UNIT_DIRECTIONS) { const h = halves(u); assert.equal(h.front.length, h.back.length); assert.equal(h.front.length * 2 + h.side.length, 120); }
});
