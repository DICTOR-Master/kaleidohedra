// The HexOct family (paper #86, "The HexOct Family", DICTO DOI 10.5281/zenodo.23896077): the five single-solid tile pairs, each
// built from the study's checked shifts (studies/2026-11-02-hexoct-connected, pairs.json), against the paper's numbers. Each tile has
// one layer cell's volume (1/√2), its pieces are joined along faces (one solid; #75's c-tile is not), its merged faces number as the
// paper's table, and at λ = 3/8 both tiles are convex: the c-tile a brick of two cubes of edge 1/√2, the h-tile the twisted cube
// (6 squares of side 1/√2, 6 isosceles triangles 1/√2, 1/√2, √(2/3), 11 corners at heights −1, −½, 0, ½, 1 layers, 1 + 3 + 3 + 3 + 1).
// Filling: in whole stackings, every layer's tile, carried by the world's motion, is the layer's own pieces computed directly
// (#57's Rule of Halves, or for B a layer's two tetrahedral pieces and the whole octahedral piece above), each up to an in-layer
// lattice step, one to one: the paper's Lemma, so the tiles fill each stacking exactly as the pieces do. Hull ratios as the table.
import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { ConvexHull } from 'three/addons/math/ConvexHull.js';
import { HEXOCT_SETS, HEXOCT_FAMILY, hexoctTile, hexoctSurface, tileMotion, setLambda, hexoctCrystal, hexoctCrystalTiles, placedSurface, layerTile } from '../../src/app/hexoct-geometry.js';
import { joinedAlongFaces } from '../../src/app/tile-surface.js';
import { stackingPieces, layerTypes, LAYER_H } from '../../src/app/stackings-geometry.js';
import { emptyBuild, placeTile, tilePieces, nextPlanTile, buildFrom } from '../../src/app/world-hexoct-kit.js';
import { hexoctLayers, parseSetChain } from '../../src/app/world-hexoct.js';

const S3 = Math.sqrt(3), CELL = Math.SQRT1_2, FAMILY = ['A', 'B', 'C', 'D', 'E'];
const apply = (M, v) => [M[0] * v[0] + M[1] * v[1], M[2] * v[0] + M[3] * v[1], v[2]];
const isLattice = (d) => { const v = d[1] / (S3 / 2), u = d[0] - v / 2; return [u, v].every((x) => Math.abs(x - Math.round(x)) < 1e-7) && Math.abs(d[2]) < 1e-7; };
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const centre = (V) => V.reduce((a, v) => a.map((x, c) => x + v[c] / V.length), [0, 0, 0]);
// convex hull volume (three's ConvexHull)
function hullVolume(P) {
  const h = new ConvexHull().setFromPoints(P.map((v) => new THREE.Vector3(...v)));
  let vol = 0;
  for (const f of h.faces) {
    const pts = []; let e = f.edge;
    do { pts.push(e.head().point); e = e.next; } while (e !== f.edge);
    for (let i = 1; i + 1 < pts.length; i++) vol += pts[0].dot(pts[i].clone().cross(pts[i + 1])) / 6;
  }
  return Math.abs(vol);
}

test('the family: five members with the paper\'s names and weights, after #75', () => {
  assert.deepEqual(HEXOCT_SETS, ['75', ...FAMILY]);
  assert.deepEqual(FAMILY.map((k) => HEXOCT_FAMILY[k].name), ['A · HexOct 3/8', 'B · HexOct −1/8 (whole octahedra)', 'C · HexOct −1/8', 'D · HexOct −11/24', 'E · HexOct 1/10']);
  assert.deepEqual(FAMILY.map(setLambda), [3 / 8, -1 / 8, -1 / 8, -11 / 24, 1 / 10]);
  assert.equal(setLambda('75'), 1 / 10);
});

for (const set of FAMILY) for (const type of ['c', 'h']) test(`${HEXOCT_FAMILY[set].name}: the ${type}-tile is one solid of one cell, ${HEXOCT_FAMILY[set].faces[type]} faces`, () => {
  const T = hexoctTile(type, set), S = hexoctSurface(type, set), F = HEXOCT_FAMILY[set];
  assert.ok(Math.abs(T.reduce((s, p) => s + p.volume, 0) - CELL) < 1e-9, 'pieces: one layer cell');
  assert.ok(Math.abs(S.volume - CELL) < 1e-9, 'its surface closes round one layer cell');
  assert.ok(joinedAlongFaces(T.length, S.contacts), 'joined along faces');
  assert.equal(S.faces, F.faces[type], 'merged faces as the paper\'s table');
  const corners = T.flatMap((p) => p.vertices), hull = hullVolume(corners);
  assert.ok(Math.abs(CELL / hull - F.hull[type]) < 1e-3, `hull ratio ${(CELL / hull).toFixed(4)} as the table's ${F.hull[type]}`);
});

test('#75\'s c-tile is two towers touching at a point; E is the same pieces made whole', () => {
  const T = hexoctTile('c', '75'), S = hexoctSurface('c', '75');
  assert.equal(joinedAlongFaces(T.length, S.contacts), false);
  assert.ok(joinedAlongFaces(4, hexoctSurface('c', 'E').contacts));
  // E's c-tile: the same four pieces, two of them moved by one lattice step
  const E = hexoctTile('c', 'E');
  assert.deepEqual(E.map((p) => p.role), ['octTop', 'tet', 'tet', 'octBottom']);
  for (const p of E) assert.ok(T.some((q) => q.role === p.role && isLattice(sub(p.site, q.site)) && p.vertices.every((v, i) => isLattice(sub(v, q.vertices[i])))));
});

test('A · HexOct 3/8: the c-tile a brick of two cubes, the h-tile the twisted cube, both convex', () => {
  const s = 1 / Math.SQRT2;
  for (const type of ['c', 'h']) {
    const S = hexoctSurface(type, 'A'), V = hexoctTile(type, 'A').flatMap((p) => p.vertices);
    for (const c of S.cells) assert.ok(V.every((v) => dot(c.n, sub(v, c.poly[0])) < 1e-9), `${type}: every face a supporting plane (convex)`);
  }
  const lens = (type) => hexoctSurface(type, 'A').edges.map(([u, v]) => Math.hypot(...sub(u, v)));
  const brick = hexoctSurface('c', 'A');
  assert.equal(brick.corners.length, 8);
  // edges of the cells: the short sides 1/√2 and the long ones in two halves of 1/√2 (the cubes' sides); the brick's long edge 2/√2
  assert.ok(lens('c').every((l) => Math.abs(l - s) < 1e-9));
  const far = Math.max(...brick.corners.flatMap((a) => brick.corners.map((b) => Math.hypot(...sub(a, b)))));
  assert.ok(Math.abs(far - Math.sqrt(s * s * 6)) < 1e-9, 'diagonal of a 1 × 1 × 2 brick of side 1/√2');
  const tw = hexoctSurface('h', 'A');
  assert.equal(tw.corners.length, 11);
  const heights = tw.corners.map((p) => Math.round((p[2] / LAYER_H) * 2) / 2 + 0).sort((a, b) => a - b);
  assert.deepEqual(heights, [-1, -0.5, -0.5, -0.5, 0, 0, 0, 0.5, 0.5, 0.5, 1]);
  // its faces: 6 squares of side 1/√2 and 6 triangles 1/√2, 1/√2, √(2/3)
  const byFace = new Map();
  for (const c of tw.cells) byFace.set(c.face, [...(byFace.get(c.face) ?? []), ...c.poly]);
  const shapes = [...byFace.values()].map((P) => {
    const pts = P.filter((p, i) => P.findIndex((q) => Math.hypot(...sub(p, q)) < 1e-9) === i && tw.corners.some((q) => Math.hypot(...sub(p, q)) < 1e-9));
    const d = pts.flatMap((a, i) => pts.slice(i + 1).map((b) => Math.hypot(...sub(a, b)))).sort((a, b) => a - b);
    return pts.length === 4 ? (Math.abs(d[0] - s) < 1e-9 && Math.abs(d[3] - s) < 1e-9 ? 'square' : 'quad?') : pts.length === 3 ? (Math.abs(d[0] - s) < 1e-9 && Math.abs(d[1] - s) < 1e-9 && Math.abs(d[2] - Math.sqrt(2 / 3)) < 1e-9 ? 'triangle' : 'tri?') : `${pts.length}?`;
  });
  assert.deepEqual(shapes.sort(), [...Array(6).fill('square'), ...Array(6).fill('triangle')]);
});

const columns = new Map(), columnOf = (word, lam) => { const k = `${word}:${lam}`; if (!columns.has(k)) columns.set(k, stackingPieces(word, lam)); return columns.get(k); };
const BALL = { A: [0, 0], B: [0.5, S3 / 6], C: [1, S3 / 3] };
// a layer's own pieces computed directly from the whole stacking: the Rule of Halves (four pieces), or for B the two tetrahedral
// pieces and the whole octahedral piece of the gap above (as its two halves)
function ownPieces(word, L, set) {
  const lam = setLambda(set), all = columnOf(word, lam), n = word.length;
  if (HEXOCT_FAMILY[set].split !== 'whole') return layerTile(word, L, lam, all);
  const P = n * LAYER_H, ball = [...BALL[word[L]], L * LAYER_H];
  return all.filter((p) => (p.role === 'tet' && p.layer === L) || (p.role !== 'tet' && p.gap === L && (p.role === 'octBottom' ? p.layer === L : p.layer === (L + 1) % n)))
    .map((p) => { const dz = Math.round((p.site[2] - ball[2]) / P) * P; return { vertices: p.vertices.map((v) => [v[0] - ball[0], v[1] - ball[1], v[2] - dz - ball[2]]) }; });
}
for (const set of FAMILY) test(`${HEXOCT_FAMILY[set].name}: in 3C, 2H, 4H, 6H, 9R and two longer words every layer is its tile carried by the world's motion`, () => {
  for (const word of ['ABC', 'AB', 'ABAC', 'ABCACB', 'ABACACBCB', 'ABCBCACB', 'ABCBABCACB']) {
    const n = word.length, types = layerTypes(word);
    for (let L = 0; L < n; L++) {
      const M = tileMotion(types[L], word[(L - 1 + n) % n], word[L], word[(L + 1) % n]);
      const own = ownPieces(word, L, set), used = new Set();
      const T = hexoctTile(types[L], set);
      assert.equal(T.length, own.length, `${word} ${L}: as many pieces`);
      // the same piece up to a lattice step: some step d carries every corner onto a corner
      const same = (V, X) => V.length === X.length && V.some((v) => { const d = sub(X[0], v); return isLattice(d) && V.every((w) => X.some((u) => Math.hypot(...sub(sub(u, w), d)) < 1e-7)); });
      for (const p of T) {
        const V = p.vertices.map((v) => apply(M, v));
        const q = own.findIndex((x, qi) => !used.has(qi) && same(V, x.vertices));
        assert.ok(q >= 0, `${set} ${word} layer ${L} ${p.role}: one of the layer's own pieces, up to a lattice step`);
        used.add(q);
      }
    }
  }
});

test('crystals and the kit take any set; the kit\'s helper builds the world\'s crystal for every member', () => {
  for (const set of FAMILY) {
    const types = hexoctLayers('6H'), P = hexoctCrystal(types, 3, 3, set), tiles = hexoctCrystalTiles(types);
    assert.equal(P.length, [...types].reduce((s, t) => s + 9 * hexoctTile(t, set).length, 0));
    const surf = placedSurface(tiles[0].type, set, tiles[0].place);
    assert.ok(surf.tris.length > 0 && surf.edges.length > 0);
    const b = emptyBuild();
    for (let i = 0; i < 12; i++) assert.ok(placeTile(b, nextPlanTile(b, types).tile));
    for (const x of b.tiles.values()) assert.equal(tilePieces(b, x, set).length, hexoctTile(x.type, set).length);
  }
  // an old snapshot (no set) still loads
  assert.equal(buildFrom({ tiles: [[0, 0, 0, 'c']], letters: [[-1, 'C'], [0, 'A'], [1, 'B']] }).tiles.size, 1);
});

test('links: hexoct:<fill>[:<pair>], the pair last (#75\'s links have none)', () => {
  assert.deepEqual(parseSetChain('3C'), ['3C', null]);
  assert.deepEqual(parseSetChain('3C:A'), ['3C', 'A']);
  assert.deepEqual(parseSetChain('fib:e'), ['fib', 'E']);
  assert.deepEqual(parseSetChain('chh:c'), ['chh', 'C'], 'a c/h sequence, then pair C');
  assert.deepEqual(parseSetChain('c'), ['c', null], 'one part is always the fill');
  assert.deepEqual(parseSetChain('free:75'), ['free', '75']);
  assert.deepEqual(parseSetChain('4H:Z'), ['4H:Z', null]);
});
