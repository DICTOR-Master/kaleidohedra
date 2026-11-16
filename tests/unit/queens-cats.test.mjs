// The Queens' walls, part 2 (DICTO 2026-11-16; src/app/queens-cats-geometry.js): the counts of Silent Running (#109) and Walls of
// Silence (#110), recomputed from the app's own models. Theorem A (the plates of A and B on the 600-cell's 60 mirrors and 300 cross
// walls), Theorem B (10 inscribed 600-cells, every corner in exactly 2; 1200 A, 1200 B and 600 C3 copies; the walls they use; the B
// copies split the triangles), Theorem B′ (P* = Q, the dual cats' f-vectors, plates on the 60 mirrors, kinds, Q as their overlap, 60
// pentagons covered whole by each), and the three kinds.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as G from '../../src/app/queens-cats-geometry.js';
import { MIRRORS, QW_VERTICES, QW_RADIUS, QW_SHEETS } from '../../src/app/queens-walls-geometry.js';
import * as WQG from '../../src/app/white-queen-geometry.js';
import * as RQG from '../../src/app/red-queen-geometry.js';

const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const norm = (a) => Math.hypot(...a);
const unit = (a) => a.map((x) => x / norm(a));
const W = QW_VERTICES.white, Q = QW_VERTICES.red;
const par = (n, m) => Math.abs(dot(unit(n), unit(m))) > 1 - 1e-9;
const sorted = (a) => [...a].sort((x, y) => x - y).join(',');
const count = (xs) => xs.reduce((m, x) => m.set(x, (m.get(x) ?? 0) + 1), new Map());

test('the walls of the White Queen: 60 mirrors and 300 cross walls', () => {
  const w = G.whiteWalls();
  assert.equal(w.mirrors.length, 60); assert.equal(w.cross.length, 300);
  assert.equal(w.mirrors, MIRRORS);
  for (const c of w.cross) assert.ok(!w.mirrors.some((m) => par(m, c)));
});

test('one S5 of the White Queen: 60 in all; its orbits A, −A, C3 (20 each), B, −B (30 each) are all 120 corners', () => {
  assert.equal(G.s5sOf(W).length, 60);
  const o = G.orbitsOf(W, G.whiteS5());
  assert.deepEqual(G.ORBITS.map((k) => o[k].length), [20, 20, 20, 30, 30]);
  assert.equal(new Set(G.ORBITS.flatMap((k) => o[k])).size, 120);
  // −A is A through the centre, and −B is B
  const key = (x) => x.map((c) => Math.round(c * 1e6)).join(',');
  for (const [a, b] of [['A', '-A'], ['B', '-B']]) assert.equal(sorted(o[a].map((i) => key(W[i].map((c) => -c))).map((k) => W.findIndex((v) => key(v) === k))), sorted(o[b]));
  // C3 is the 20 roots of the S5's A4: closed under the centre
  assert.equal(sorted(o.C3), sorted(G.whiteS5().roots));
});

test('Theorem A: A has 30 plates, all mirrors; B 80, 40 mirrors and 40 cross walls; together all 60 mirrors, 10 shared', () => {
  const cats = G.whiteCats();
  const sides = (s) => [...count(s.faces.map((f) => f.length))].sort();
  for (const k of ['A', '-A']) {
    const s = cats[k];
    assert.deepEqual(sides(s), [[3, 20], [6, 10]]);   // 20 triangles, 10 hexagons
    assert.equal(s.plates.length, 30);
    assert.ok(s.plates.every((p) => p.faces.length === 1 && p.wall.kind === 'mirror'));
    assert.equal(new Set(s.plates.map((p) => p.wall.index)).size, 30);
    assert.equal(s.kind, 'nonheart');
  }
  for (const k of ['B', '-B']) {
    const s = cats[k];
    assert.deepEqual(sides(s), [[3, 50], [4, 30]]);   // 50 triangles, 30 rectangles
    assert.equal(s.plates.length, 80);
    assert.ok(s.plates.every((p) => p.faces.length === 1));
    assert.equal(s.plates.filter((p) => p.wall.kind === 'mirror').length, 40);
    assert.equal(s.plates.filter((p) => p.wall.kind === 'cross').length, 40);
    assert.equal(s.kind, 'nonheart');
  }
  const mA = new Set(cats.A.plates.map((p) => p.wall.index)), mB = new Set(cats.B.plates.filter((p) => p.wall.kind === 'mirror').map((p) => p.wall.index));
  assert.equal([...mA].filter((i) => mB.has(i)).length, 10);
  assert.equal(new Set([...mA, ...mB]).size, 60);
  // C3: 70 faces on 5 cross walls, 14 on each; heart
  assert.equal(cats.C3.faces.length, 70); assert.equal(cats.C3.plates.length, 5);
  assert.ok(cats.C3.plates.every((p) => p.faces.length === 14 && p.wall.kind === 'cross'));
  assert.equal(cats.C3.kind, 'heart');
  // every face of A and B lies in its plate
  for (const k of ['A', 'B']) for (const p of cats[k].plates) for (const fi of p.faces) for (const i of cats[k].faces[fi]) assert.ok(Math.abs(dot(cats[k].corners[i], p.normal)) < 1e-9);
});

test('Theorem B (a): 10 inscribed 600-cells, every corner in exactly 2, two states of 5', () => {
  const ins = G.inscribed();
  assert.equal(ins.cells.length, 10);
  assert.ok(ins.cells.every((c) => c.length === 120));
  const per = new Array(600).fill(0); ins.cells.forEach((c) => c.forEach((i) => per[i]++));
  assert.deepEqual([...new Set(per)], [2]);
  const [one, two] = ins.states;
  assert.equal(one.length, 5); assert.equal(two.length, 5);
  for (const s of ins.states) for (const a of s) for (const b of s) if (a !== b) assert.equal(ins.meet(a, b), 0);
  for (const a of one) for (const b of two) assert.equal(ins.meet(a, b), 24);   // a shared 24-cell
  // each a 600-cell: radius of the Red Queen, 12 neighbours at 36° for every corner, 720 edges
  for (let ci = 0; ci < 10; ci++) assert.equal(G.inscribedEdges(ci).length, 720);
});

test('Theorem B (b): 1200 A, 1200 B and 600 C3 copies, 120, 120 and 60 in each 600-cell; 40, 60 and 20 through each corner', () => {
  const sets = { A: new Set(), B: new Set(), C3: new Set() }, through = { A: new Array(600).fill(0), B: new Array(600).fill(0), C3: new Array(600).fill(0) };
  for (let ci = 0; ci < 10; ci++) {
    const list = G.copiesIn(ci);
    assert.equal(list.length, 60);   // its 60 S5s
    const inCell = { A: new Set(), B: new Set(), C3: new Set() };
    for (const o of list) for (const k of G.ORBITS) {
      const key = sorted(o[k]);
      inCell[G.TYPE[k]].add(key);
      if (!sets[G.TYPE[k]].has(key)) { sets[G.TYPE[k]].add(key); for (const i of o[k]) through[G.TYPE[k]][i]++; }
    }
    assert.deepEqual([inCell.A.size, inCell.B.size, inCell.C3.size], [120, 120, 60]);
  }
  assert.deepEqual([sets.A.size, sets.B.size, sets.C3.size], [1200, 1200, 600]);
  assert.deepEqual([...new Set(through.A)], [40]); assert.deepEqual([...new Set(through.B)], [60]); assert.deepEqual([...new Set(through.C3)], [20]);
});

test('Theorem B (c), (d): the walls the copies use in one 600-cell, and the B copies split its 1200 triangles exactly', () => {
  // the Red Queen's walls: M her 60 mirrors (normals along the White Queen's corners), X the 300 along her own corners, N the rest
  const cls = (n) => (MIRRORS.some((m) => par(m, n)) ? 'M' : Q.some((x) => par(x, n)) ? 'X' : 'N');
  const ci = G.inscribed().states[0][0], cell = G.inscribed().cells[ci], list = G.copiesIn(ci);
  const used = { A: [], B: [] }, triB = new Map(), triA = new Map();
  const edge = new Set(G.inscribedEdges(ci).map(([a, b]) => `${a},${b}`)), isEdge = (a, b) => edge.has(a < b ? `${a},${b}` : `${b},${a}`);
  for (const o of list) for (const k of ['A', '-A', 'B', '-B']) {
    const s = G.solid(o[k].map((i) => Q[i]));
    assert.equal(s.plates.length, G.TYPE[k] === 'A' ? 30 : 80);
    assert.equal(s.kind, 'nonheart');
    for (const p of s.plates) used[G.TYPE[k]].push(p.normal);
    for (const f of s.faces) if (f.length === 3) {
      const t = f.map((i) => o[k][i]);
      if (isEdge(t[0], t[1]) && isEdge(t[1], t[2]) && isEdge(t[0], t[2])) { const m = G.TYPE[k] === 'A' ? triA : triB, key = sorted(t); m.set(key, (m.get(key) ?? 0) + 1); }
    }
  }
  const distinct = (ns) => { const out = []; for (const n of ns) if (!out.some((m) => par(m, n))) out.push(n); return out; };
  const A = distinct(used.A), B = distinct(used.B);
  assert.ok(used.A.every((n) => cls(n) === 'X'), 'every A copy is hidden in the Red Queen: its plates on the 300');
  assert.equal(A.length, 60);   // the 600-cell's own 60 mirrors, all among the 300
  const byB = count(B.map(cls));
  assert.deepEqual([byB.get('M'), byB.get('X'), byB.get('N')], [60, 60, 240]);   // all 360 walls of the 600-cell
  assert.equal(triB.size, 1200); assert.deepEqual([...new Set(triB.values())], [1]);
  assert.equal(triA.size, 1200); assert.deepEqual([...new Set(triA.values())], [2]);
  assert.ok(cell.length === 120);
});

test('dual polarity: P* = Q and Q* = P (r² = |Red Queen corner|²)', () => {
  const r2 = QW_RADIUS.red ** 2, key = (x) => x.map((c) => Math.round(c * 1e6)).join(','), Qk = new Set(Q.map(key)), Wk = new Set(W.map(key));
  const polarOf = (V, corners) => { const c = [0, 1, 2, 3].map((k) => corners.reduce((s, i) => s + V[i][k], 0) / corners.length), n = unit(c), h = dot(n, V[corners[0]]); assert.ok(corners.every((i) => Math.abs(dot(n, V[i]) - h) < 1e-9)); assert.ok(V.every((x) => dot(n, x) <= h + 1e-9)); return n.map((x) => (r2 * x) / h); };
  const Pstar = WQG.CELLS.map((c) => polarOf(W, c));
  assert.equal(Pstar.length, 600); assert.ok(Pstar.every((y) => Qk.has(key(y)))); assert.equal(new Set(Pstar.map(key)).size, 600);
  const Qstar = RQG.CELLS.map((c) => polarOf(Q, c.corners));
  assert.equal(Qstar.length, 120); assert.ok(Qstar.every((y) => Wk.has(key(y)))); assert.equal(new Set(Qstar.map(key)).size, 120);
});

test("Theorem B′: the dual cats' f-vectors, plates on the Red Queen's 60 mirrors, kinds, their overlap the Red Queen, 60 pentagons each", () => {
  const D = G.dualCats(), f = (s) => [s.corners.length, s.edges.length, s.faces.length, s.facets.length];
  for (const k of ['A', '-A']) { assert.deepEqual(f(D[k]), [10, 30, 40, 20]); assert.equal(D[k].kind, 'inherited'); }
  for (const k of ['B', '-B']) { assert.deepEqual(f(D[k]), [20, 80, 90, 30]); assert.equal(D[k].kind, 'inherited'); }
  assert.deepEqual(f(D.C3), [30, 70, 60, 20]); assert.equal(D.C3.kind, 'heart');
  const fpp = { A: 4, '-A': 4, B: 9, '-B': 9, C3: 6 };
  for (const k of G.ORBITS) {
    assert.equal(D[k].plates.length, 10);
    assert.ok(D[k].plates.every((p) => p.wall.kind === 'mirror' && p.faces.length === fpp[k]));
    // each covers 60 of the Red Queen's pentagons whole, 6 of the 12 on each of its mirrors, and none in part
    assert.ok(D[k].plates.every((p) => p.covers.whole.length === 6 && p.covers.partly.length === 0));
    for (const p of D[k].plates) for (const j of p.covers.whole) assert.ok(QW_SHEETS.red[p.wall.index].faces[j].length === 5);
  }
  // A*: 5 corners on the Red Queen, 5 at φ² times her radius
  const onQ = D.A.corners.filter((y) => Q.some((x) => norm(x.map((c, i) => c - y[i])) < 1e-9)).length;
  assert.equal(onQ, 5);
  assert.equal(D.A.corners.filter((y) => Math.abs(norm(y) - G.PHI ** 2 * QW_RADIUS.red) < 1e-9).length, 5);
  // the Red Queen = A* ∩ −A* ∩ C3* ∩ B* ∩ −B*: their 120 cells lie on her 120 cell walls, each once
  const walls = G.ORBITS.flatMap((k) => D[k].facets);
  assert.equal(walls.length, 120);
  const dQ = norm([0, 1, 2, 3].map((k) => RQG.CELLS[0].corners.reduce((s, i) => s + Q[i][k], 0) / 20));
  const hit = walls.map((w) => { assert.ok(Math.abs(w.h - dQ) < 1e-9); return W.findIndex((x) => dot(unit(x), w.n) > 1 - 1e-9); });
  assert.ok(hit.every((i) => i >= 0)); assert.equal(new Set(hit).size, 120);
  // and every corner of the Red Queen is inside all five
  for (const k of G.ORBITS) for (const x of Q) for (const w of D[k].facets) assert.ok(dot(w.n, x) <= w.h + 1e-9);
});

test('the three kinds on small cases: a centrally symmetric set is heart; kindOf reads non-heart and inherited heart from the plates', () => {
  const cross = [[1, 0, 0, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, 0, 0, -1]];
  assert.equal(G.solid(cross).kind, 'heart');   // the 16-cell
  const s5 = [[4, -1, -1, -1, -1], [-1, 4, -1, -1, -1], [-1, -1, 4, -1, -1], [-1, -1, -1, 4, -1], [-1, -1, -1, -1, 4]];
  // the regular 5-cell in 4D (sum-zero space, an orthonormal basis of it)
  const B = [[1, -1, 0, 0, 0], [1, 1, -2, 0, 0], [1, 1, 1, -3, 0], [1, 1, 1, 1, -4]].map(unit);
  const cell5 = s5.map((x) => B.map((b) => dot(x, b)));
  const s = G.solid(cell5);
  assert.equal(s.faces.length, 10); assert.equal(s.plates.length, 10); assert.equal(s.kind, 'nonheart');
});
