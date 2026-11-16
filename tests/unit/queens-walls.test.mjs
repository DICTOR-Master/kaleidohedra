// The Queens' walls (DICTO 2026-11-16; src/app/queens-walls-geometry.js): 600 and 120 cells, 60 sheets on the 60 mirrors, 20 triangles
// to a White sheet and 12 pentagons to a Red one (as studies 2026-11-16-600cell-walls: walls.py, walls120.py), every sheet face in its
// mirror, and at Apart 0 the pieces are exactly the Queen (every cell once, every triangle / pentagon once, nothing moved).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { MIRRORS, QW_CELLS, QW_SHEETS, QW_VERTICES, qwPieces, qwView } from '../../src/app/queens-walls-geometry.js';
import * as WQG from '../../src/app/white-queen-geometry.js';
import * as RQG from '../../src/app/red-queen-geometry.js';

const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const key = (f) => [...f].sort((a, b) => a - b).join(',');

test('600 and 120 cells, each a pyramid on its own direction', () => {
  assert.equal(QW_CELLS.white.length, 600); assert.equal(QW_CELLS.red.length, 120);
  for (const q of ['white', 'red']) for (const c of QW_CELLS[q]) { assert.ok(Math.abs(Math.hypot(...c.dir) - 1) < 1e-12); assert.ok(c.corners.every((i) => dot(QW_VERTICES[q][i], c.dir) > 0)); }
  assert.ok(QW_CELLS.white.every((c) => c.faces.length === 4)); assert.ok(QW_CELLS.red.every((c) => c.faces.length === 12));
});
test('60 mirrors: unit, pairwise distinct (no two opposite), each perpendicular to a White Queen corner', () => {
  assert.equal(MIRRORS.length, 60);
  for (let i = 0; i < 60; i++) for (let j = i + 1; j < 60; j++) assert.ok(Math.abs(Math.abs(dot(MIRRORS[i], MIRRORS[j])) - 1) > 1e-6);
});
test('60 sheets: 20 triangles each (White), 12 pentagons each (Red), on the same 60 planes', () => {
  assert.equal(QW_SHEETS.white.length, 60); assert.equal(QW_SHEETS.red.length, 60);
  assert.ok(QW_SHEETS.white.every((s) => s.faces.length === 20 && s.faces.every((f) => f.length === 3)));
  assert.ok(QW_SHEETS.red.every((s) => s.faces.length === 12 && s.faces.every((f) => f.length === 5)));
  QW_SHEETS.white.forEach((s, i) => assert.deepEqual(s.normal, QW_SHEETS.red[i].normal));
});
test('every sheet face lies in its mirror plane', () => {
  for (const q of ['white', 'red']) for (const s of QW_SHEETS[q]) for (const f of s.faces) for (const i of f) assert.ok(Math.abs(dot(QW_VERTICES[q][i], s.normal)) < 1e-9);
});
test('at Apart 0 the pieces are the Queen: every face once, every cell once, nothing moved', () => {
  const tri = QW_SHEETS.white.flatMap((s) => s.faces.map(key)), pen = QW_SHEETS.red.flatMap((s) => s.faces.map(key));
  assert.equal(tri.length, 1200); assert.equal(new Set(tri).size, 1200); assert.deepEqual(new Set(tri), new Set(WQG.TRIANGLES.map(key)));
  assert.equal(pen.length, 720); assert.equal(new Set(pen).size, 720); assert.deepEqual(new Set(pen), new Set(RQG.PENTAGONS.map(key)));
  assert.deepEqual(QW_CELLS.white.map((c) => key(c.corners)), WQG.CELLS.map(key));
  assert.deepEqual(QW_CELLS.red.map((c) => key(c.corners)), RQG.CELLS.map((c) => key(c.corners)));
  const { frame } = qwView('vertex-first');
  for (const q of ['white', 'red']) for (const m of ['cells', 'sheets']) {
    const P = QW_VERTICES[q].map((x) => frame.map((f) => dot(x, f)));
    for (const p of qwPieces(q, m, frame, 0)) { assert.ok(p.offset.every((x) => x === 0)); for (const [, b] of p.struts) assert.ok(P.some((v) => v.every((x, k) => Math.abs(x - b[k]) < 1e-12))); }
  }
});
test('Apart moves each sheet along its own normal and each cell along its own direction', () => {
  const { frame } = qwView('edge-first'), pr = (x) => frame.map((f) => dot(x, f));
  const s = qwPieces('red', 'sheets', frame, 0.5), c = qwPieces('white', 'cells', frame, 1);
  s.forEach((p, i) => pr(QW_SHEETS.red[i].normal).forEach((x, k) => assert.ok(Math.abs(p.offset[k] - x * 0.5 * RQG.RADIUS) < 1e-12)));
  c.forEach((p, i) => pr(QW_CELLS.white[i].dir).forEach((x, k) => assert.ok(Math.abs(p.offset[k] - x * 2) < 1e-12)));
});
