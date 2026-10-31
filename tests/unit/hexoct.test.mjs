// HexOct (DICTO 2026-10-31; paper #75, "HexOct: Two Tiles for Every Stacking"): the two layer tiles at the paper's λ = 1/10 and the
// crystals of the world. Each tile is one ball's share (volume 1/√2 at ball spacing 1) of four pieces: two tetrahedral pieces and two
// octahedral halves; the c-tile is two towers meeting only at the ball, the h-tile one solid on the vertical line over the ball. In whole
// stackings (the fills and others), every layer's own tile, computed directly, is its type's tile carried by the motion the world uses
// (the paper's theorem), each piece up to a lattice translation in the layer. The fills' c/h sequences, the Fibonacci word, the field.
// The world lives in Kaleidohedra beside the Stackings World (moved from Polyhedraverse 2026-11-01). The HexOct kit (Polyhedraverse,
// 2026-11-01): tiles placed one at a time keep their layers' letters; the fill helper's next tile, followed to the end, builds exactly
// the world's crystal; free placement onto a placed tile; one kind per layer; no layer emptied between others; saving and loading.
import test from 'node:test';
import assert from 'node:assert/strict';
import { HEXOCT_LAMBDA, HEXOCT_FILLS, hexoctTile, layerTile, tileMotion, hexoctCrystal, fillTypes, fibonacciTypes, parseTypes, lettersOf, LATTICE_SYMMETRIES } from '../../src/app/hexoct-geometry.js';
import { hexoctLayers } from '../../src/app/world-hexoct.js';
import { layerTypes, LAYER_H } from '../../src/app/stackings-geometry.js';
import { HEXKIT_FILLS, emptyBuild, canPlace, placeTile, removeTile, tilePieces, previewPieces, kitPlan, nextPlanTile, freeTarget, buildFrom, layerType } from '../../src/app/world-hexoct-kit.js';
import { worldTitle } from '../../src/app/dimension-wizard.js';

const S3 = Math.sqrt(3);
const apply = (M, v) => [M[0] * v[0] + M[1] * v[1], M[2] * v[0] + M[3] * v[1], v[2]];
const isLattice = (d) => { const v = d[1] / (S3 / 2), u = d[0] - v / 2; return [u, v].every((x) => Math.abs(x - Math.round(x)) < 1e-7) && Math.abs(d[2]) < 1e-7; };
const roleCount = (T) => T.reduce((a, p) => ({ ...a, [p.role]: (a[p.role] ?? 0) + 1 }), {});

test('the paper\'s weight; 12 lattice symmetries', () => {
  assert.equal(HEXOCT_LAMBDA, 0.1);
  assert.equal(LATTICE_SYMMETRIES.length, 12);
});

for (const type of ['c', 'h']) test(`the ${type}-tile: four pieces, one ball's share`, () => {
  const T = hexoctTile(type);
  assert.deepEqual(roleCount(T), { tet: 2, octTop: 1, octBottom: 1 });
  assert.ok(Math.abs(T.reduce((s, p) => s + p.volume, 0) - Math.SQRT1_2) < 1e-9);
  // the two tetrahedral pieces have the same volume, and so do the two halves (each tile holds one tetrahedral shape and one half shape)
  const tets = T.filter((p) => p.role === 'tet'), halves = T.filter((p) => p.role !== 'tet');
  assert.ok(Math.abs(tets[0].volume - tets[1].volume) < 1e-9 && Math.abs(halves[0].volume - halves[1].volume) < 1e-9);
  // λ = 1/10 > −7/24: the tetrahedral pieces reach a full layer up and down (the tiles interlock), to the next layers' balls
  const zs = tets.flatMap((p) => p.vertices.map((v) => v[2]));
  assert.ok(Math.abs(Math.max(...zs) - LAYER_H) < 1e-9 && Math.abs(Math.min(...zs) + LAYER_H) < 1e-9);
});

test('the c-tile is two towers meeting only at the ball; the h-tile one solid over the ball', () => {
  const xy = (p) => p.site.slice(0, 2).map((x) => x.toFixed(6)).join(',');
  const C = hexoctTile('c'), H = hexoctTile('h');
  // c: each tower a tetrahedral piece with an octahedral half over it, the towers on opposite sides of the ball
  const towers = new Map(); for (const p of C) towers.set(xy(p), [...(towers.get(xy(p)) ?? []), p.role].sort());
  assert.deepEqual([...towers.values()].sort(), [['octBottom', 'tet'], ['octTop', 'tet']]);
  const [a, b] = [...towers.keys()].map((k) => k.split(',').map(Number));
  assert.ok(Math.hypot(a[0] + b[0], a[1] + b[1]) < 1e-9, 'point-symmetric about the ball');
  // the towers share only the ball's point: the corners they have in common are the ball alone
  const corners = (role) => C.filter((p) => xy(p) === [...towers.keys()][role]).flatMap((p) => p.vertices);
  const shared = corners(0).filter((u) => corners(1).some((v) => Math.hypot(u[0] - v[0], u[1] - v[1], u[2] - v[2]) < 1e-9));
  assert.ok(shared.length > 0 && shared.every((v) => Math.hypot(...v) < 1e-9), 'touching at the ball only');
  // h: both tetrahedral pieces on one vertical line, a corner each at the ball (the double pyramid), the halves on one line beside it
  const ht = H.filter((p) => p.role === 'tet'), ho = H.filter((p) => p.role !== 'tet');
  assert.equal(xy(ht[0]), xy(ht[1])); assert.equal(xy(ho[0]), xy(ho[1]));
  for (const p of ht) assert.ok(p.vertices.some((v) => Math.hypot(...v) < 1e-9));
});

// whole stackings: the fills' words and others with c and h layers mixed (#57's 9R, an 8-layer and a 10-layer word)
for (const word of ['ABC', 'AB', 'ABAC', 'ABCACB', 'ABACACBCB', 'ABCBCACB', 'ABCBABCACB']) {
  test(`${word}: every layer's own tile is its type's tile, carried by the world's motion`, () => {
    const n = word.length, types = layerTypes(word);
    for (let L = 0; L < n; L++) {
      const own = layerTile(word, L), M = tileMotion(types[L], word[(L - 1 + n) % n], word[L], word[(L + 1) % n]);
      assert.ok(M, `${word} layer ${L}: a motion`);
      for (const p of hexoctTile(types[L])) {
        const V = p.vertices.map((v) => apply(M, v)), s = apply(M, p.site);
        const q = own.find((x) => x.role === p.role && x.vertices.length === V.length && isLattice(x.site.map((c, i) => c - s[i])));
        assert.ok(q, `${word} layer ${L} ${p.role}: a piece there`);
        const d = q.site.map((c, i) => c - s[i]);
        assert.ok(V.every((v) => q.vertices.some((u) => Math.hypot(u[0] - v[0] - d[0], u[1] - v[1] - d[1], u[2] - v[2] - d[2]) < 1e-7)), `${word} layer ${L} ${p.role}: the same piece`);
      }
    }
  });
}

test('the fills: their c/h sequences, Fibonacci c → ch, h → c from c', () => {
  assert.deepEqual(HEXOCT_FILLS, ['3C', '2H', '4H', '6H', 'fib']);
  assert.equal(fillTypes('3C'), 'cccccccc');
  assert.equal(fillTypes('2H'), 'hhhhhhhh');
  assert.equal(fillTypes('4H'), 'chchchch');
  assert.equal(fillTypes('6H'), 'hcchcchc');
  assert.equal(fibonacciTypes(13), 'chcchchcchcch');
  assert.equal(fillTypes('fib'), 'chcchchc');
  // the letters agree with the types they were built from (layer k is h when layers k − 1 and k + 1 match)
  for (const f of HEXOCT_FILLS) {
    const T = fillTypes(f), Ls = lettersOf(T);
    for (let k = 0; k < T.length; k++) { assert.notEqual(Ls[k + 1], Ls[k + 2]); assert.equal(Ls[k] === Ls[k + 2] ? 'h' : 'c', T[k], `${f} layer ${k}`); }
  }
});

test('the viewer\'s own sequence: c and h only, up to 16; short ones repeated to six layers', () => {
  assert.equal(parseTypes(' C h, H '), 'chh');
  for (const bad of ['', 'chx', 'abc', 'c'.repeat(17), null]) assert.equal(parseTypes(bad), null);
  assert.equal(hexoctLayers('own', 'chh'), 'chhchh');
  assert.equal(hexoctLayers('own', 'cchhchc'), 'cchhchc');
  assert.equal(hexoctLayers('4H', 'x'), 'chchchch');
});

test('a crystal: four pieces per tile, 3 × 3 tiles per layer, the right tile on every layer, filling one ball\'s share each', () => {
  const T = fillTypes('fib'), P = hexoctCrystal(T);
  assert.equal(P.length, T.length * 9 * 4);
  for (let k = 0; k < T.length; k++) assert.ok(P.filter((p) => p.layer === k).every((p) => p.type === T[k]));
  // no two pieces of one kind in the same place (each piece of the stacking drawn once)
  const keys = P.map((p) => `${p.role}:${p.vertices.reduce((a, v) => a.map((x, i) => x + v[i] / p.vertices.length), [0, 0, 0]).map((x) => x.toFixed(5)).join(',')}`);
  assert.equal(new Set(keys).size, P.length);
});

test('HexOct is a Kaleidohedra world beside the Stackings World', () => {
  assert.equal(worldTitle('3D', 'tool:hexoctWorld'), 'HexOct');
  assert.equal(worldTitle('3D', 'tool:stackingsWorld'), 'The Stackings World');
});

// the kit: the helper's ghost, tile by tile, against the world's crystal (the same pieces, the crystal only moved to its middle)
const corners = (P) => P.flatMap((p) => p.vertices);
for (const fill of ['3C', '2H', '4H', '6H', 'fib']) test(`the kit's ${fill} helper: each next tile, placed, builds the world's crystal`, () => {
  const types = hexoctLayers(fill), crystal = hexoctCrystal(types), b = emptyBuild();
  let shift = null, placed = 0;
  for (;;) {
    const nx = nextPlanTile(b, types);
    assert.equal(nx.conflict, undefined, `${fill}: no conflict after ${placed}`);
    if (nx.done) break;
    const { k, i, j, type } = nx.tile;
    assert.equal(type, types[k], `${fill}: the ghost's kind is its layer's`);
    const ghost = previewPieces(b, nx.tile);
    assert.ok(placeTile(b, nx.tile));
    const real = tilePieces(b, nx.tile);
    assert.deepEqual(corners(ghost), corners(real), `${fill}: the ghost is the tile that lands`);
    const want = crystal.slice(((k * 3 + i) * 3 + j) * 4, ((k * 3 + i) * 3 + j) * 4 + 4);
    assert.deepEqual(want.map((p) => p.role), real.map((p) => p.role));
    shift ??= want[0].vertices[0].map((x, c) => x - real[0].vertices[0][c]);
    const A = corners(want), B = corners(real);
    assert.ok(A.every((v, n) => v.every((x, c) => Math.abs(x - B[n][c] - shift[c]) < 1e-9)), `${fill} layer ${k} tile ${i},${j}: the crystal's own`);
    placed++;
  }
  assert.equal(placed, types.length * 9);
  assert.equal(kitPlan(types).length, placed);
});

test('the kit: one kind per layer, a new layer next to the others, letters as lettersOf', () => {
  assert.deepEqual(HEXKIT_FILLS, ['free', '3C', '2H', '4H', '6H', 'fib', 'own']);
  const b = emptyBuild();
  assert.equal(canPlace(b, { k: 1, i: 0, j: 0, type: 'c' }), false, 'the first tile goes on layer 0');
  assert.ok(placeTile(b, { k: 0, i: 0, j: 0, type: 'h' }));
  assert.equal(b.letters.get(-1), 'B', 'an h layer: the same letter on both sides');
  assert.equal(placeTile(b, { k: 0, i: 1, j: 0, type: 'c' }), false, 'a c-tile in an h layer');
  assert.equal(placeTile(b, { k: 2, i: 0, j: 0, type: 'c' }), false, 'not two layers up');
  assert.ok(placeTile(b, { k: 1, i: 0, j: 0, type: 'c' }));
  assert.equal(b.letters.get(2), 'C', 'a c layer: the third letter beyond');
  assert.ok(placeTile(b, { k: -1, i: 0, j: 0, type: 'c' }));
  assert.equal(b.letters.get(-2), 'C');
  // layers −1, 0, 1 are c h c bottom up: the letters of layers −2 … 2 are lettersOf('chc') moved down one layer
  assert.deepEqual([-2, -1, 0, 1, 2].map((k) => b.letters.get(k)), ['C', 'B', 'A', 'B', 'C']);
  assert.deepEqual(lettersOf('chc').map((x) => ({ A: 'B', B: 'A', C: 'C' })[x]), ['C', 'B', 'A', 'B', 'C'], 'the same up to naming');
  // no layer emptied between others; the end layers can go
  assert.equal(removeTile(b, '0,0,0'), false);
  assert.ok(removeTile(b, '1,0,0'));
  assert.equal(layerType(b, 1), null);
  assert.ok(placeTile(b, { k: 1, i: 0, j: 0, type: 'h' }), 'the emptied top layer takes either kind again');
  assert.equal(b.letters.get(2), 'A', 'h: the letter below it');
});

test('the kit: a tap on a tile puts the picked tile on that side', () => {
  const b = emptyBuild();
  placeTile(b, { k: 0, i: 0, j: 0, type: 'c' });
  assert.deepEqual(freeTarget(b, { k: 0, i: 0, j: 0 }, [1, 0, 0], 'c'), { k: 0, i: 1, j: 0, type: 'c' }, 'beside it, in its layer');
  const up = freeTarget(b, { k: 0, i: 0, j: 0 }, [0, 0, 1], 'h');
  assert.equal(up.k, 1, 'an h-tile on top (the layer beside is c)');
  assert.ok(placeTile(b, up));
  const down = freeTarget(b, { k: 0, i: 0, j: 0 }, [0.2, 0.1, -1], 'h');
  assert.equal(down.k, -1);
  // each of the three places above is one ball spacing from the ball
  const P = tilePieces(b, up);
  assert.equal(P.length, 4);
  assert.equal(freeTarget(b, { k: 0, i: 0, j: 0 }, [1, 0, 0], 'h').k !== 0, true, 'an h-tile never lands in a c layer');
});

test('the kit saves and loads, the letters too', () => {
  const b = emptyBuild();
  const types = hexoctLayers('6H');
  for (let n = 0; n < 30; n++) placeTile(b, nextPlanTile(b, types).tile);
  const snap = { tiles: [...b.tiles.values()].map((x) => [x.k, x.i, x.j, x.type]), letters: [...b.letters.entries()] };
  const c = buildFrom(JSON.parse(JSON.stringify(snap)));
  assert.equal(c.tiles.size, 30);
  assert.deepEqual([...c.letters.entries()].sort(), [...b.letters.entries()].sort());
  assert.deepEqual(nextPlanTile(c, types), nextPlanTile(b, types));
  // a bad snapshot: an empty build
  assert.equal(buildFrom({ tiles: [[3, 0, 0, 'c']], letters: [] }).tiles.size, 0);
  assert.equal(buildFrom(null).tiles.size, 0);
  // a build that left the plan is told, not followed
  const d = emptyBuild(); placeTile(d, { k: 0, i: 0, j: 0, type: 'h' });
  assert.deepEqual(nextPlanTile(d, hexoctLayers('3C')), { conflict: 0 });
});
