// Queen sectors (DICTO 2026-10-31): the Red Queen in 12 sectors over her core dodecahedron's pentagons, the White Queen in 20 over her
// core icosahedron's triangles; every drawn cell cut by the sector planes into convex wedges (queen-sectors.js). In every picture of the
// Shells view (Shells, RCP view, RCP v4): the wedges of each shell fill exactly its cells' volume, each wedge lies in its own sector's
// cone, and the core falls apart into the 12 pentagonal pyramids / the 20 Cleo-Icos tetrahedra, whole.
import test from 'node:test';
import assert from 'node:assert/strict';
import { sectorCones, queenWedges, cellFaceLoops, volume, clipConvex, SECTOR_COUNT } from '../../src/app/queen-sectors.js';
import * as WQG from '../../src/app/white-queen-geometry.js';
import * as RQG from '../../src/app/red-queen-geometry.js';
import { farEyePoints } from '../../src/app/dicto-rcp.js';

const UP = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];
const rcp = (V, r) => V.map((x) => UP.map((f) => (f.reduce((s, c, i) => s + c * x[i], 0) * 5 * r) / (5 * r - x[0])));
const PICTURES = {
  white: { shells: WQG.CLEO_POINTS, rcp: rcp(WQG.VERTICES, 2), dictoRcp: farEyePoints(WQG.VERTICES, 2, WQG.CLEO_SHELLS[0].cells.map((ci) => WQG.CELLS[ci]), UP) },
  red: { shells: RQG.LAYER_POINTS, rcp: rcp(RQG.VERTICES, RQG.RADIUS), dictoRcp: farEyePoints(RQG.VERTICES, RQG.RADIUS, RQG.CELL_LAYERS[0].cells.map((ci) => RQG.CELLS[ci].corners), UP) },
};
const SHELLS = { white: WQG.CLEO_SHELLS, red: RQG.CELL_LAYERS };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

test('12 sectors for the Red Queen, 20 for the White Queen; each cone bounded by its face\'s planes through the centre', () => {
  assert.equal(sectorCones('red').length, 12); assert.equal(SECTOR_COUNT.red, 12);
  assert.equal(sectorCones('white').length, 20); assert.equal(SECTOR_COUNT.white, 20);
  for (const q of ['red', 'white']) for (const c of sectorCones(q)) {
    assert.equal(c.normals.length, q === 'red' ? 5 : 3);
    for (const n of c.normals) assert.ok(dot(n, c.axis) > 0.1);
  }
});

test('clipping a cube by a plane through its centre halves it', () => {
  const C = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]];
  const F = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]].map((f) => f.map((k) => C[k]));
  assert.ok(Math.abs(volume(F) - 8) < 1e-12);
  const n = [1, 1, 0].map((x) => x / Math.SQRT2);
  assert.ok(Math.abs(volume(clipConvex(F, n)) - 4) < 1e-12);
});

for (const queen of ['white', 'red']) for (const [pic, Q] of Object.entries(PICTURES[queen])) {
  test(`${queen} queen, ${pic}: per shell the wedges' volume is the cells' volume, every wedge in its own cone`, () => {
    const cones = sectorCones(queen), scale = Math.max(...Q.map((p) => Math.hypot(...p)));
    SHELLS[queen].forEach((sh, k) => {
      const W = queenWedges(queen, Q, sh.cells);
      let cells = 0, wedges = 0;
      sh.cells.forEach((ci, i) => {
        const v = volume(cellFaceLoops(queen, ci).map((f) => f.map((x) => Q[x])));
        const w = W[i].reduce((s, x) => s + volume(x.faces), 0);
        assert.ok(Math.abs(v - w) < 1e-9 * Math.max(1, v), `${queen} ${pic} shell ${k} cell ${ci}: ${w} vs ${v}`);
        cells += v; wedges += w;
        for (const x of W[i]) for (const f of x.faces) for (const p of f) for (const n of cones[x.sector].normals) assert.ok(dot(n, p) > -1e-9 * scale, `${queen} ${pic}: wedge outside its cone`);
      });
      assert.ok(Math.abs(cells - wedges) < 1e-9 * Math.max(1, cells), `${queen} ${pic} shell ${k}`);
    });
  });
}

test('as the study found: White 300 cells whole, 300 cut in two; Red 48 whole, 70 cut in 2 or 3, the 2 on the axis in 12', () => {
  const count = (queen, n) => { const h = {}; for (const w of queenWedges(queen, PICTURES[queen].shells, [...Array(n).keys()])) h[w.length] = (h[w.length] ?? 0) + 1; return h; };
  assert.deepEqual(count('white', 600), { 1: 300, 2: 300 });
  assert.deepEqual(count('red', 120), { 1: 48, 2: 30, 3: 40, 12: 2 });
});

test('the core falls apart into the 20 Cleo-Icos tetrahedra (White) / the 12 pentagonal pyramids (Red)', () => {
  for (const pic of Object.keys(PICTURES.white)) {
    const W = queenWedges('white', PICTURES.white[pic], WQG.CLEO_SHELLS[0].cells);
    assert.equal(W.length, 20);
    const sectors = new Set();
    W.forEach((w) => { assert.equal(w.length, 1, 'each core tetrahedron whole in one sector'); assert.equal(w[0].faces.length, 4); sectors.add(w[0].sector); });
    assert.equal(sectors.size, 20);
  }
  for (const pic of Object.keys(PICTURES.red)) {
    const [W] = queenWedges('red', PICTURES.red[pic], RQG.CELL_LAYERS[0].cells);
    assert.equal(W.length, 12);
    const vols = W.map((w) => volume(w.faces));
    for (const w of W) {
      // a pentagonal pyramid: one pentagon and five triangles, its apex at the centre
      const sides = w.faces.map((f) => f.length).sort();
      assert.deepEqual(sides, [3, 3, 3, 3, 3, 5]);
      assert.ok(w.faces.filter((f) => f.length === 3).every((f) => f.some((p) => Math.hypot(...p) < 1e-9)));
    }
    assert.ok(Math.max(...vols) - Math.min(...vols) < 1e-9 * vols[0], 'the 12 pyramids congruent in volume');
  }
});
