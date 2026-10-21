// Aristotle's Pyramid (DICTO 2026-10-21; paper #44): each Platonic solid's face pyramids fill exactly the solid (volumes add up, every
// pyramid's tip at the centre); the three fills are whole cells: 8 unit cubes of cube pyramids; 8 octet cells of 8 octahedron + 8
// tetrahedron pyramids each (equal numbers), each cell the 60° rhombohedron of volume 2 (edge √2), here edge 1; and the kit
// 'antonius.block': 8 golden rhombohedra, each 2 Cleo-Icos + 1 Antonius, Antonius 4 times the Cleo-Icos, pieces adding up to the cells.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { SOLID_KEYS, FILL_KEYS, facePyramids, fillPieces, goldenCells, pieceVolume } from '../../src/app/aristotle-geometry.js';

const close = (a, b, msg, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} vs ${b}`);
const sum = (P) => P.reduce((a, p) => a + pieceVolume(p), 0);
const s5 = Math.sqrt(5), PHI = (1 + s5) / 2;
const VOLUME = { cube: 1, tetrahedron: Math.SQRT2 / 12, octahedron: Math.SQRT2 / 3, dodecahedron: (15 + 7 * s5) / 4, icosahedron: 5 * PHI * PHI / 6 };
const FACES = { cube: 6, tetrahedron: 4, octahedron: 8, dodecahedron: 12, icosahedron: 20 };

test('each solid is its face pyramids, tips at the centre', () => {
  for (const k of SOLID_KEYS) {
    const P = facePyramids(k);
    assert.equal(P.length, FACES[k], k);
    close(sum(P), VOLUME[k], `${k} volume`, 1e-6);
    for (const p of P) assert.ok(p.faces.slice(1).every((f) => Math.hypot(...f[0]) < 1e-9), `${k} tip at the centre`);
  }
});

test('the three fills are whole cells', () => {
  assert.deepEqual(FILL_KEYS, ['cube', 'octet', 'golden']);
  const cube = fillPieces('cube');
  assert.equal(cube.length, 48); close(sum(cube), 8, 'cube fill');
  const octet = fillPieces('octet'), O = octet.filter((p) => p.kind === 'octahedron'), T = octet.filter((p) => p.kind === 'tetrahedron');
  assert.equal(O.length, 64); assert.equal(T.length, 64, 'equal numbers');
  close(sum(octet), 8 * 2 / (2 * Math.SQRT2), 'octet: 8 cells of volume 2 at edge √2');
  close(sum(O), 8 * VOLUME.octahedron, 'octahedra'); close(sum(T), 16 * VOLUME.tetrahedron, 'tetrahedra');
  const golden = fillPieces('golden'), C = golden.filter((p) => p.kind === 'icosahedron'), A = golden.filter((p) => p.kind === 'antonius');
  assert.equal(C.length, 16); assert.equal(A.length, 8, 'two Cleo-Icos to one Antonius');
  for (const a of A) close(pieceVolume(a), 4 * pieceVolume(C[0]), 'Antonius = 4 Cleo-Icos', 1e-6);
  const cells = goldenCells();
  assert.equal(cells.length, 8);
  const cellVol = (c) => { const [a, b, d] = [1, 2, 3].map((i) => c[i].map((x, j) => x - c[0][j]));
    return Math.abs(a[0] * (b[1] * d[2] - b[2] * d[1]) - a[1] * (b[0] * d[2] - b[2] * d[0]) + a[2] * (b[0] * d[1] - b[1] * d[0])); };
  close(sum(golden), cells.reduce((s, c) => s + cellVol(c), 0), 'the pieces fill the 8 rhombohedra', 1e-6);
  for (const c of cells) close(cellVol(c), 6 * pieceVolume(C[0]), 'rhombohedron = 6 Cleo-Icos', 1e-6);
});
