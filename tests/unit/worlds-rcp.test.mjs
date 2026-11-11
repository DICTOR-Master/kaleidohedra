// RCP view, RCP v4 and Sectors in the Bitruncated 600-cell and the 4D Permutohedron (DICTO 2026-11-11, "we didn't put RCP/RCP 4 and
// sectors buttons on new apps"), as in the Queens world (queen-sectors.js, dicto-rcp.js). Bitruncated 600-cell: 32 sectors over the core
// truncated icosahedron's 12 pentagons and 20 hexagons; 4D Permutohedron: 14 over the seed 3D permutohedron's 8 hexagons and 6 squares,
// the seed opposite Build's outer cell. In every picture (the world's own, RCP view, RCP v4) every cell's wedges fill exactly its volume
// and lie in their own cone; the core / seed falls apart into its pyramids, one per sector; RCP view keeps the model's sizes and RCP v4
// draws the core / seed at its true size; and the Queens world's RCP points are what they were.
import test from 'node:test';
import assert from 'node:assert/strict';
import * as BT from '../../src/app/bitrunc-geometry.js';
import * as PM from '../../src/app/perm4-geometry.js';
import { btPicture, btCellWedges, btSectorCones, BT_PICTURES, BT_SECTORS } from '../../src/app/world-bitrunc.js';
import { volume, conesOverFaces, sectorCones } from '../../src/app/queen-sectors.js';
import { rmsSize, seedEyePoints } from '../../src/app/dicto-rcp.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../../src/krp-core/src/geometry-extensions/roof-fold.js';
import * as WQG from '../../src/app/white-queen-geometry.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const close = (a, b, eps, msg) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} vs ${b}`);

test('the Queens world: sectorCones is conesOverFaces, and seedEyePoints is its RCP formula', () => {
  const UP = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];
  const old = WQG.VERTICES.map((x) => UP.map((f) => (f.reduce((s, c, i) => s + c * x[i], 0) * 10) / (10 - x[0])));
  seedEyePoints(WQG.VERTICES, 2, UP, 5).forEach((p, i) => p.forEach((x, k) => close(x, old[i][k], 1e-12, 'RCP point')));
  assert.equal(sectorCones('white').length, 20);
  const sq = conesOverFaces([[[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1]]]);
  assert.deepEqual(sq[0].axis, [0, 0, 1]); assert.equal(sq[0].normals.length, 4);
});

test('Bitruncated 600-cell: 32 sectors, 12 five-sided cones and 20 six-sided', () => {
  const C = btSectorCones();
  assert.equal(C.length, 32); assert.equal(BT_SECTORS, 32);
  assert.deepEqual(C.map((c) => c.normals.length).reduce((m, n) => ({ ...m, [n]: (m[n] ?? 0) + 1 }), {}), { 5: 12, 6: 20 });
  for (const c of C) for (const n of c.normals) assert.ok(dot(n, c.axis) > 0.05);
});

for (const key of BT_PICTURES) {
  test(`Bitruncated 600-cell, ${key}: every cell's wedges fill its volume, each in its own cone; the core in 12 + 20 pyramids`, () => {
    const M = BT.model(), { SQ } = btPicture(key), C = btSectorCones(), scale = Math.max(...SQ.map((p) => Math.hypot(...p)));
    const pieces = {};
    for (let ci = 0; ci < M.CELLS.length; ci++) {
      const W = btCellWedges(ci, key);
      pieces[W.length] = (pieces[W.length] ?? 0) + 1;
      const v = volume(M.CELL_FACES[ci].map((fi) => M.FACES[fi].loop.map((k) => SQ[k]))), w = W.reduce((s, x) => s + volume(x.faces), 0);
      close(w, v, 1e-9 * Math.max(1, v), `cell ${ci}`);
      for (const x of W) for (const f of x.faces) for (const p of f) for (const n of C[x.sector].normals) assert.ok(dot(n, p) > -1e-9 * scale, `cell ${ci}: wedge outside its cone`);
    }
    // the core and the far truncated icosahedron (both on the axis) in 32 each; as the cut is the same planes, the same in all pictures
    assert.deepEqual(pieces, { 1: 120, 2: 240, 3: 240, 4: 70, 6: 48, 32: 2 });
    const core = btCellWedges(M.CORE, key);
    assert.equal(new Set(core.map((w) => w.sector)).size, 32);
    // a pentagonal pyramid has 6 faces, a hexagonal one 7; each apex at the centre
    assert.deepEqual(core.map((w) => w.faces.length).reduce((m, n) => ({ ...m, [n]: (m[n] ?? 0) + 1 }), {}), { 6: 12, 7: 20 });
    for (const w of core) assert.ok(w.faces.filter((f) => f.length === 3).every((f) => f.some((p) => Math.hypot(...p) < 1e-9 * scale)));
  });
}

test('Bitruncated 600-cell: RCP view keeps the sizes near the model\'s, RCP v4 draws the core at its true size and the far side larger', () => {
  const M = BT.model(), core = M.CELLS[M.CORE].corners, s4 = rmsSize(core.map((k) => M.CORNERS[k]));
  close(rmsSize(core.map((k) => btPicture('dictoRcp').SQ[k])) / WS, s4, 1e-9, 'RCP v4 core');
  const r = (key) => Math.max(...btPicture(key).SQ.map((p) => Math.hypot(...p))) / WS;
  assert.ok(r('rcp') > 1.9 && r('rcp') < 2.6, `RCP radius ${r('rcp')}`);
  const far = M.CELLS.findIndex((c) => c.kind === 'TI' && c.corners.every((k) => M.CORNERS[k][0] < -M.CORE_HEIGHT + 1e-9)), sz = (key) => rmsSize(M.CELLS[far].corners.map((k) => btPicture(key).SQ[k]));
  assert.ok(sz('dictoRcp') > sz('rcp') * 1.3, `far TI: RCP v4 ${sz('dictoRcp')} vs RCP ${sz('rcp')}`);
});

test('4D Permutohedron: the seed is the 3D permutohedron opposite the outer cell, at the centre of Build', () => {
  const o = PM.CELLS[PM.OUTER], s = PM.CELLS[PM.SEED];
  assert.equal(s.kind, 'TO'); assert.equal(s.S.length + o.S.length, 5); assert.ok(!s.S.some((i) => o.S.includes(i)));
  const cen = (c) => [0, 1, 2, 3].map((k) => c.V.reduce((a, v) => a + PM.X[v][k], 0) / c.V.length);
  cen(s).forEach((x, k) => close(x, -cen(o)[k], 1e-6, 'opposite'));
  const b = [0, 1, 2].map((k) => s.V.reduce((a, v) => a + PM.BUILD_POINTS[v][k], 0) / s.V.length);
  assert.ok(Math.hypot(...b) < 1e-9, 'at the centre of Build');
});

test('4D Permutohedron: 14 sectors, 8 six-sided cones and 6 four-sided', () => {
  assert.equal(PM.SECTOR_COUNT, 14);
  assert.deepEqual(PM.SECTOR_CONES.map((c) => c.normals.length).reduce((m, n) => ({ ...m, [n]: (m[n] ?? 0) + 1 }), {}), { 4: 6, 6: 8 });
});

for (const pic of PM.PICTURES) {
  test(`4D Permutohedron, ${pic}: every cell's wedges fill its volume, each in its own cone; the seed in 8 + 6 pyramids`, () => {
    const P = PM.POINTS[pic], scale = Math.max(...P.map((p) => Math.hypot(...p)));
    let total = 0;
    PM.CELLS.forEach((c, ci) => {
      const W = PM.cellWedgesIn(ci, pic);
      total += W.length;
      const v = volume(c.F.map((f) => f.map((k) => P[k]))), w = W.reduce((s, x) => s + volume(x.faces), 0);
      // the page's corners are given to 6 decimals (perm4-data.js), so its faces are flat to about 1e-6
      close(w, v, 1e-6 * Math.max(1, v), `${pic} cell ${ci}`);
      for (const x of W) for (const f of x.faces) for (const p of f) for (const n of PM.SECTOR_CONES[x.sector].normals) assert.ok(dot(n, p) > -1e-6 * scale, `${pic} cell ${ci}: wedge outside its cone`);
    });
    assert.equal(total, 128, `${pic}: 128 pieces in all`);
    const seed = PM.cellWedgesIn(PM.SEED, pic);
    assert.equal(new Set(seed.map((w) => w.sector)).size, 14);
    assert.deepEqual(seed.map((w) => w.faces.length).reduce((m, n) => ({ ...m, [n]: (m[n] ?? 0) + 1 }), {}), { 5: 6, 7: 8 });
  });
}

test('4D Permutohedron: Build radius 1; RCP view keeps the sizes near the model\'s; RCP v4 draws the seed at its true size', () => {
  const r = (pic) => Math.max(...PM.POINTS[pic].map((p) => Math.hypot(...p)));
  close(r('build'), 1, 1e-9, 'Build');
  assert.ok(r('rcp') > 0.95 && r('rcp') < 1.3, `RCP ${r('rcp')}`);
  const seed = PM.CELLS[PM.SEED].V;
  close(rmsSize(seed.map((v) => PM.POINTS.dictoRcp[v])), rmsSize(seed.map((v) => PM.X[v])) / PM.RADIUS, 1e-9, 'RCP v4 seed');
  const outer = PM.CELLS[PM.OUTER].V, sz = (pic) => rmsSize(outer.map((v) => PM.POINTS[pic][v]));
  assert.ok(sz('dictoRcp') > sz('rcp') * 1.3, `the far cell larger in RCP v4: ${sz('dictoRcp')} vs ${sz('rcp')}`);
  // only Build has the see-through outer cell; the RCP pictures draw all 30 cells as cells
  assert.equal(PM.buildCells('all', 0, 'build').filter((c) => c.outer).length, 1);
  for (const pic of ['rcp', 'dictoRcp']) assert.equal(PM.buildCells('all', 0, pic).filter((c) => c.outer).length, 0);
});

test('the new words in all 7 languages', () => {
  for (const key of ['bt.sectors.tip', 'bt.note.sectors', 'pm.sectors.tip', 'pm.note.rcp', 'pm.note.dictoRcp', 'pm.note.sectors', 'pm.cap.all.rcp']) for (const L of LANG_ORDER) assert.notEqual(t(key, L), key);
  assert.match(t('bt.sectors.tip', 'en'), /32 sectors/); assert.match(t('pm.sectors.tip', 'en'), /14 sectors/);
});
