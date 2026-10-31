// HexOct's geometry (DICTO 2026-10-31): the two layer tiles of paper #75, "HexOct: Two Tiles for Every Stacking" (DICTO DOI
// 10.5281/zenodo.23737639; DICTO named them HexOct), stacked into any close-packed stacking. The tile of layer L, for one ball, is four
// pieces of the Rule of Halves (#57): the top half of the octahedral piece of the gap below, the tetrahedral pieces of the two gaps next
// to the layer, and the bottom half of the octahedral piece of the gap above (k-research studies/2026-10-29-endless-stack-cell,
// tiles.py). The c-tile is the tile of the cubic stacking ABC (two towers meeting at the ball), the h-tile that of the hexagonal
// stacking AB (one solid round the vertical line over the ball). Both come from stackings-geometry.js at the paper's weight λ = 1/10.
// By the paper's theorem every layer's tile is its type's tile carried by one motion that keeps the layer: a symmetry of the triangular
// lattice about the ball (z kept); here the motion is the one that takes the tile's four holes onto the layer's own holes, and
// tests/unit/hexoct.test.mjs checks the carried tiles against the pieces computed directly for whole stackings.
import { stackingPieces, LAYER_H, PRESETS, layerTypes } from './stackings-geometry.js';

export const HEXOCT_LAMBDA = 1 / 10;   // the weight of the paper's figures (#75 Figures 1 and 2)
const S3 = Math.sqrt(3);
const POS = { A: [0, 0], B: [0.5, S3 / 6], C: [1, S3 / 3] };   // A = 0, B = (a1 + a2)/3, C = 2(a1 + a2)/3, as stackings-geometry.js
const A1 = [1, 0], A2 = [0.5, S3 / 2];
const third = (a, b) => 'ABC'.replace(a, '').replace(b, '');

/** The fills on the buttons: each a cyclic c/h sequence of layer types (3C, 2H, 4H, 6H from their Ramsdell words) or Fibonacci. */
export const HEXOCT_FILLS = ['3C', '2H', '4H', '6H', 'fib'];
const LAYERS = 8;   // layers shown for a fill (whole periods: 3C and 2H four … eight, 4H four periods, 6H two plus two)
/** The Fibonacci word of layer types: c → ch, h → c, from c (c, ch, chc, chcch, chcchchc, …), its first n letters. */
export function fibonacciTypes(n) {
  let w = 'c';
  while (w.length < n) w = [...w].map((x) => (x === 'c' ? 'ch' : 'c')).join('');
  return w.slice(0, n);
}
/** The c/h sequence of a fill, `n` layers long (a periodic fill repeated). */
export function fillTypes(fill, n = LAYERS) {
  if (fill === 'fib') return fibonacciTypes(n);
  const p = layerTypes(PRESETS[fill]).join('');
  return p.repeat(Math.ceil(n / p.length)).slice(0, n);
}
export const MAX_OWN = 16;
/** The viewer's own sequence: c and h only (spaces, commas and case ignored), 1 … MAX_OWN letters; else null. */
export function parseTypes(text) {
  const s = String(text ?? '').toLowerCase().replace(/[\s,·.-]/g, '');
  return /^[ch]+$/.test(s) && s.length <= MAX_OWN ? s : null;
}
/** The letters A/B/C of the layers −1 … n of a stacking whose layers 0 … n−1 have the types `types` (layer 0 on A, layer 1 on B). */
export function lettersOf(types) {
  const n = types.length, L = [types[0] === 'h' ? 'B' : 'C', 'A', 'B'];   // L[k + 1] is layer k
  for (let k = 1; k < n; k++) L.push(types[k] === 'h' ? L[k] : third(L[k], L[k + 1]));
  return L;
}

// ---- the two tiles ----
/** The tile of layer L of a periodic word: its four pieces about the layer's ball (z up, layer spacing LAYER_H). */
export function layerTile(word, L, lam = HEXOCT_LAMBDA, pieces = stackingPieces(word, lam)) {
  const P = word.length * LAYER_H, ball = [...POS[word[L]], L * LAYER_H];
  return pieces.filter((p) => p.layer === L).map((p) => {
    const dz = Math.round((p.site[2] - ball[2]) / P) * P;   // the period's copy next to the layer
    const at = (v) => [v[0] - ball[0], v[1] - ball[1], v[2] - dz - ball[2]];
    return { role: p.role, site: at(p.site), vertices: p.vertices.map(at), faces: p.faces, volume: p.volume };
  });
}
const tiles = new Map();
/** The c-tile (cubic stacking ABC, layer B) or the h-tile (hexagonal stacking AB, layer A), cached. */
export function hexoctTile(type) {
  if (!tiles.has(type)) tiles.set(type, type === 'c' ? layerTile('ABC', 1) : layerTile('AB', 0));
  return tiles.get(type);
}

// ---- the motions ----
// The 12 symmetries of the triangular lattice about a ball, as 2 × 2 matrices on (x, y): six turns, six mirrors.
export const LATTICE_SYMMETRIES = [0, 1, 2, 3, 4, 5].flatMap((k) => {
  const c = Math.cos((k * Math.PI) / 3), s = Math.sin((k * Math.PI) / 3);
  return [[c, -s, s, c], [c, s, s, -c]];
});
const apply = (M, v) => [M[0] * v[0] + M[1] * v[1], M[2] * v[0] + M[3] * v[1], v[2]];
// which of the three positions A, B, C an in-plane offset falls on (0, 1, 2), up to the lattice
function cls(x, y) {
  const v = y / A2[1], u = x - v * A2[0];
  return (((Math.round(3 * u) % 3) + 3) % 3);
}
/** The motion carrying the `type` tile onto layer k's (letters below, at, above): its four holes onto the layer's, each up to the lattice. */
export function tileMotion(type, below, at, above) {
  const want = { tet: { lo: below, hi: above }, octTop: third(below, at), octBottom: third(at, above) };
  const ball = POS[at];
  const target = (p) => {
    const letter = p.role === 'tet' ? (p.site[2] < 0 ? want.tet.lo : want.tet.hi) : want[p.role];
    return cls(POS[letter][0] - ball[0], POS[letter][1] - ball[1]);
  };
  const T = hexoctTile(type);
  return LATTICE_SYMMETRIES.find((M) => T.every((p) => { const q = apply(M, p.site); return cls(q[0], q[1]) === target(p); })) ?? null;
}

/** A crystal of HexOct tiles: the layers of `types` (bottom up), each a patch of cols × rows tiles. Pieces about the crystal's middle,
 *  z up: [{ type, role, layer, vertices, faces }]. */
export function hexoctCrystal(types, cols = 3, rows = 3) {
  const n = types.length, Ls = lettersOf(types), out = [];
  const mid = [((cols - 1) * A1[0] + (rows - 1) * A2[0]) / 2 + POS.B[0], ((rows - 1) * A2[1]) / 2 + POS.B[1], ((n - 1) * LAYER_H) / 2];   // B: the balls' mean offset
  for (let k = 0; k < n; k++) {
    const type = types[k], M = tileMotion(type, Ls[k], Ls[k + 1], Ls[k + 2]), T = hexoctTile(type), b = POS[Ls[k + 1]];
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
      const o = [b[0] + i * A1[0] + j * A2[0] - mid[0], b[1] + i * A1[1] + j * A2[1] - mid[1], k * LAYER_H - mid[2]];
      for (const p of T) out.push({ type, role: p.role, layer: k, vertices: p.vertices.map((v) => apply(M, v).map((x, c) => x + o[c])), faces: p.faces });
    }
  }
  return out;
}

/** Edges [[p, q], …] of the two tiles side by side (the DICTO menu's preview): the c-tile left, the h-tile right. */
export function hexoctPreviewEdges() {
  const out = [];
  for (const [type, dx] of [['c', -0.8], ['h', 0.6]]) for (const p of hexoctTile(type)) for (const f of p.faces) {
    f.forEach((a, i) => { const u = p.vertices[a], v = p.vertices[f[(i + 1) % f.length]]; out.push([[u[0] + dx, u[2], -u[1]], [v[0] + dx, v[2], -v[1]]]); });
  }
  return out;
}
