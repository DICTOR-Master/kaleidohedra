// RCP v4 (DICTO's adjusted RCP, DICTO 2026-10-31): the RCP perspective with the eye beyond the far side. In krp-core's builds (eyeSide 'far') and in
// the Queens world's exact model (dicto-rcp.js): the seed keeps its true size, the far side comes out larger than the seed, and the
// existing RCP (eye on the seed's side, the default) is exactly what it was.
import test from 'node:test';
import assert from 'node:assert/strict';
import { buildRcpComplex } from '../../src/krp-core/src/polyhedra/rcpBuild.js';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { farEyePoints, rmsSize } from '../../src/app/dicto-rcp.js';
import * as WQG from '../../src/app/white-queen-geometry.js';
import * as RQG from '../../src/app/red-queen-geometry.js';

const BUILDS = [['D4', '600-cell (vertex-first)'], ['D4', '600-cell'], ['DODECAHEDRON', '120-cell'], ['CUBE', 'tesseract'], ['D8', '24-cell'], ['D4', '16-cell']];
const close = (a, b, eps, msg) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} vs ${b}`);

test('RCP v4 in krp-core: the seed is at its true (registry) size', () => {
  for (const [seed, target] of BUILDS) {
    const cx = buildRcpComplex(seed, target, { eyeSide: 'far' });
    assert.equal(cx.eyeSide, 'far');
    close(rmsSize(cx.cells[0].vertices3D), rmsSize(POLYHEDRA[seed].vertices), 1e-9, `${seed} ${target}`);
  }
});

test('RCP v4 in krp-core: the far side is larger than the seed, and larger than in the RCP view', () => {
  for (const [seed, target] of BUILDS) {
    const far = buildRcpComplex(seed, target, { eyeSide: 'far' }), near = buildRcpComplex(seed, target);
    const s0 = rmsSize(far.cells[0].vertices3D), top = Math.max(...far.cells.map((c) => c.shell));
    const outer = far.cells.filter((c) => c.shell === top).map((c) => rmsSize(c.vertices3D) / s0);
    assert.ok(Math.min(...outer) > 1.3, `${seed} ${target}: outer shell ${Math.min(...outer)} of the seed`);
    const nearOuter = near.cells.filter((c) => c.shell === top).map((c) => rmsSize(c.vertices3D) / s0);
    assert.ok(Math.max(...nearOuter) < 0.75, `${seed} ${target}: RCP view's outer shell ${Math.max(...nearOuter)} of the seed`);
  }
  // cell-first: the cell opposite the seed is exactly (d + r0) / (d − r0) = 6 / 4 of it, d = 5 × the seed's own w
  const cx = buildRcpComplex('DODECAHEDRON', '120-cell', { eyeSide: 'far' });
  close(Math.max(...cx.cells.map((c) => rmsSize(c.vertices3D))) / rmsSize(cx.cells[0].vertices3D), 1.5, 1e-9, '120-cell far cell');
});

test('RCP v4 in krp-core: same cells, shells, adjacency and Open copies; only the closed positions differ', () => {
  for (const [seed, target] of BUILDS) {
    const far = buildRcpComplex(seed, target, { eyeSide: 'far' }), near = buildRcpComplex(seed, target);
    assert.deepEqual(far.cells.map((c) => [c.id, c.shell]), near.cells.map((c) => [c.id, c.shell]));
    assert.deepEqual(far.adjacency, near.adjacency);
    assert.deepEqual(far.cells.map((c) => c.openVertices3D ?? null), near.cells.map((c) => c.openVertices3D ?? null));
    assert.deepEqual(far.openGaps ?? null, near.openGaps ?? null);
  }
  assert.throws(() => buildRcpComplex('D4', '600-cell', { eyeSide: 'side' }), /eyeSide/);
});

test('the existing RCP view is unchanged (eye on the seed side by default; fingerprints from master before RCP v4)', () => {
  const PINNED = [['D4', '600-cell (vertex-first)', 600, 1394.057550787, 4357.929873241, 5498.791270655], ['D4', '600-cell', 600, 0, 3088.503070815, -30.570327878],
    ['DODECAHEDRON', '120-cell', 120, 0, 16171.612027502, 37.817840997], ['CUBE', 'tesseract', 8, 0, 34.666666667, -5], ['D4', '5-cell', 5, 0, 6, 0.027821446],
    ['D8', '24-cell', 24, 0, 72.08, 3.111269837], ['D4', '16-cell', 16, 0, 17.333333333, 7.706010384]];
  for (const [seed, target, n, sum, sq, mix] of PINNED) {
    const cx = buildRcpComplex(seed, target);
    assert.equal(cx.eyeSide, 'seed');
    assert.deepEqual(buildRcpComplex(seed, target, { eyeSide: 'seed' }), cx);
    assert.equal(cx.cells.length, n);
    const flat = cx.cells.flatMap((c) => c.vertices3D.flat());
    close(flat.reduce((p, x) => p + x, 0), sum, 1e-6, `${target} sum`);
    close(flat.reduce((p, x) => p + x * x, 0), sq, 1e-6, `${target} squares`);
    close(flat.reduce((p, x, i) => p + x * ((i % 7) + 1), 0), mix, 1e-6, `${target} weighted`);
  }
});

test('RCP v4 in the Queens world: the seed at its true size, each queen opening out larger towards the far side', () => {
  const UP = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];
  for (const [V, r, shells, corners] of [[WQG.VERTICES, 2, WQG.CLEO_SHELLS, (ci) => WQG.CELLS[ci]], [RQG.VERTICES, RQG.RADIUS, RQG.CELL_LAYERS, (ci) => RQG.CELLS[ci].corners]]) {
    const seeds = shells[0].cells.map(corners), P = farEyePoints(V, r, seeds, UP);
    for (const c of seeds) close(rmsSize(c.map((i) => P[i])), rmsSize(c.map((i) => V[i])), 1e-9, 'seed cell true size');
    const size = (c) => rmsSize(c.map((i) => P[i])) / rmsSize(c.map((i) => V[i]));
    const last = shells[shells.length - 1].cells.map(corners).map(size);
    assert.ok(Math.min(...last) > 1.3, `far shell ${Math.min(...last)} of true size`);
    // no shell drawn much smaller than the seed (the inner shells' cells lean in 4D, so their shadows are a few per cent flatter)
    for (const [k, s] of shells.entries()) { const m = Math.max(...s.cells.map(corners).map(size)); assert.ok(m > 0.95, `shell ${k}: ${m}`); }
  }
});
