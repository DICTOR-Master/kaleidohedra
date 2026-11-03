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
import { tileSurface } from './tile-surface.js';

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
  return aboutBall(word, L, pieces.filter((p) => p.layer === L));
}
// pieces of a column moved to the period's copy next to layer L, about layer L's ball
function aboutBall(word, L, list) {
  const P = word.length * LAYER_H, ball = [...POS[word[L]], L * LAYER_H];
  return list.map((p) => {
    const dz = Math.round((p.site[2] - ball[2]) / P) * P;   // the period's copy next to the layer
    const at = (v) => [v[0] - ball[0], v[1] - ball[1], v[2] - dz - ball[2]];
    return { role: p.role, site: at(p.site), vertices: p.vertices.map(at), faces: p.faces, volume: p.volume };
  });
}
const tiles = new Map();
/** The c-tile (cubic stacking ABC, layer B) or the h-tile (hexagonal stacking AB, layer A), cached: paper #75's (set '75', the
 *  default) or a member of paper #86's HexOct family (set 'A' … 'E', familyTile). */
export function hexoctTile(type, set = '75') {
  const key = `${set}:${type}`;
  if (!tiles.has(key)) tiles.set(key, set === '75' ? (type === 'c' ? layerTile('ABC', 1) : layerTile('AB', 0)) : familyTile(type, set));
  return tiles.get(key);
}

// ---- the HexOct family (paper #86, "The HexOct Family", DICTO DOI 10.5281/zenodo.23896077, concept 10.5281/zenodo.23896076) ----
// #75's c-tile is two towers touching at a point; moving one tower by one in-layer lattice step joins them along a face, and since
// every piece is only swapped for its own translate the layer is filled exactly as before (#86's Lemma), so every stacking is still a
// string of the two tiles. The five members (names as the paper's table, placeholders until DICTO names them), each with the study's
// checked shifts (k-research studies/2026-11-02-hexoct-connected, scripts/pairs.json; verify.py: 42 stackings, 0 overlaps): per
// piece, in the order of the study's tiles.py (top half of the octahedral piece below, tetrahedral piece below, tetrahedral piece
// above, bottom half of the octahedral piece above; vanished pieces left out), the lattice step (a, b) = a·a1 + b·a2. Member B splits
// the layers otherwise (§6): a layer's two tetrahedral pieces and the WHOLE octahedral piece of the gap above. The paper's face counts
// (coplanar faces merged), hull ratios and the number of piece pairs its exact check tested go with each, for the tests and captions.
export const HEXOCT_SETS = ['75', 'A', 'B', 'C', 'D', 'E'];
export const HEXOCT_FAMILY = {
  A: { name: 'A · HexOct 3/8', lam: 3 / 8, lamText: '3/8', split: 'halves', tc: [[0, 0], [-1, -1]], th: [[0, 0], [0, 0]], faces: { c: 6, h: 12 }, hull: { c: 1, h: 1 }, pairs: 7472 },
  B: { name: 'B · HexOct −1/8 (whole octahedra)', lam: -1 / 8, lamText: '−1/8', split: 'whole', tc: [[0, 0], [-1, -1], [0, 0]], th: [[0, 0], [0, 0], [-1, 0]], faces: { c: 8, h: 10 }, hull: { c: 6 / 7, h: 6 / 7 }, pairs: 6480 },
  C: { name: 'C · HexOct −1/8', lam: -1 / 8, lamText: '−1/8', split: 'halves', tc: [[0, 0], [0, 1], [0, 0], [0, 1]], th: [[0, 0], [0, 0], [0, 0], [0, 0]], faces: { c: 10, h: 14 }, hull: { c: 0.800, h: 0.735 }, pairs: 11232 },
  D: { name: 'D · HexOct −11/24', lam: -11 / 24, lamText: '−11/24', split: 'halves', tc: [[0, 0], [0, 1]], th: [[0, 0], [0, 0]], faces: { c: 18, h: 8 }, hull: { c: 0.783, h: 1 }, pairs: 4080 },
  E: { name: 'E · HexOct 1/10', lam: 1 / 10, lamText: '1/10', split: 'halves', tc: [[0, 0], [0, 1], [0, 0], [0, 1]], th: [[0, 0], [0, 0], [0, 0], [0, 0]], faces: { c: 24, h: 30 }, hull: { c: 0.745, h: 0.778 }, pairs: 13520 },
};
/** The weight λ of a tile set. */
export const setLambda = (set) => (set === '75' ? HEXOCT_LAMBDA : HEXOCT_FAMILY[set].lam);
/** The pieces of a family member's c- or h-tile in the study's order (each { role, site, vertices, faces, volume, part }, `part` the
 *  study's piece number; member B's whole octahedral piece as its two halves, both part 2), each moved by its lattice step. */
export function familyTile(type, set) {
  const F = HEXOCT_FAMILY[set], [word, L] = type === 'c' ? ['ABC', 1] : ['AB', 0], n = word.length, steps = type === 'c' ? F.tc : F.th;
  const all = stackingPieces(word, F.lam), own = layerTile(word, L, F.lam, all);
  const tets = own.filter((p) => p.role === 'tet'), lo = tets.find((p) => p.site[2] < 0), hi = tets.find((p) => p.site[2] > 0);
  let parts;
  if (F.split === 'whole') {
    // the whole octahedral piece of the gap above the layer: its bottom half (this layer's) and its top half (the next layer's)
    const oct = aboutBall(word, L, all.filter((p) => p.role !== 'tet' && p.gap === L % n && (p.role === 'octBottom' ? p.layer === L : p.layer === (L + 1) % n)));
    parts = [[lo], [hi], oct];
  } else parts = [own.find((p) => p.role === 'octTop'), lo, hi, own.find((p) => p.role === 'octBottom')].filter(Boolean).map((p) => [p]);
  if (parts.length !== steps.length || parts.some((g) => !g.length || g.some((p) => !p))) throw new Error(`HexOct ${set} ${type}: ${parts.length} pieces, the study has ${steps.length}`);
  return parts.flatMap((g, part) => {
    const [a, b] = steps[part], d = [a * A1[0] + b * A2[0], a * A1[1] + b * A2[1], 0], mv = (v) => v.map((x, c) => x + d[c]);
    return g.map((p) => ({ ...p, site: mv(p.site), vertices: p.vertices.map(mv), part }));
  });
}
const surfaces = new Map();
/** The merged surface of a set's tile (tile-surface.js): faces, cells, edges, contacts, volume, corners; cached. */
export function hexoctSurface(type, set) {
  const key = `${set}:${type}`;
  if (!surfaces.has(key)) surfaces.set(key, tileSurface(hexoctTile(type, set)));
  return surfaces.get(key);
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

/** Where each tile of a crystal goes: the layers of `types` (bottom up), each a patch of cols × rows tiles, about the crystal's middle,
 *  z up: [{ type, layer, place }], `place` taking a point of the type's reference tile to its place in the crystal. */
export function hexoctCrystalTiles(types, cols = 3, rows = 3) {
  const n = types.length, Ls = lettersOf(types), out = [];
  const mid = [((cols - 1) * A1[0] + (rows - 1) * A2[0]) / 2 + POS.B[0], ((rows - 1) * A2[1]) / 2 + POS.B[1], ((n - 1) * LAYER_H) / 2];   // B: the balls' mean offset
  for (let k = 0; k < n; k++) {
    const type = types[k], M = tileMotion(type, Ls[k], Ls[k + 1], Ls[k + 2]), b = POS[Ls[k + 1]];
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
      const o = [b[0] + i * A1[0] + j * A2[0] - mid[0], b[1] + i * A1[1] + j * A2[1] - mid[1], k * LAYER_H - mid[2]];
      out.push({ type, layer: k, place: (v) => apply(M, v).map((x, c) => x + o[c]) });
    }
  }
  return out;
}
/** A crystal of HexOct tiles of a set ('75' by default): the layers of `types` (bottom up), each a patch of cols × rows tiles. Pieces
 *  about the crystal's middle, z up: [{ type, role, layer, vertices, faces }]. */
export function hexoctCrystal(types, cols = 3, rows = 3, set = '75') {
  return hexoctCrystalTiles(types, cols, rows).flatMap(({ type, layer, place }) =>
    hexoctTile(type, set).map((p) => ({ type, role: p.role, layer, vertices: p.vertices.map(place), faces: p.faces })));
}
/** A set's tile surface carried by `place`: its faces as triangles [[a, b, c], …] and its edges [[u, v], …] (the merged faces only,
 *  no seams between the pieces; the HexOct family is drawn so, as paper #86's plates). */
export function placedSurface(type, set, place) {
  const S = hexoctSurface(type, set), tris = [];
  for (const c of S.cells) { const P = c.poly.map(place); for (let i = 1; i + 1 < P.length; i++) tris.push([P[0], P[i], P[i + 1]]); }
  return { tris, edges: S.edges.map(([u, v]) => [place(u), place(v)]) };
}

/** Edges [[p, q], …] of the two tiles side by side (the DICTO menu's preview): the c-tile left, the h-tile right. */
export function hexoctPreviewEdges() {
  const out = [];
  for (const [type, dx] of [['c', -0.8], ['h', 0.6]]) for (const p of hexoctTile(type)) for (const f of p.faces) {
    f.forEach((a, i) => { const u = p.vertices[a], v = p.vertices[f[(i + 1) % f.length]]; out.push([[u[0] + dx, u[2], -u[1]], [v[0] + dx, v[2], -v[1]]]); });
  }
  return out;
}

// ---- one tile at a time (the HexOct kit in Polyhedraverse, DICTO 2026-11-01) ----
export { third as thirdLetter };
/** The ball of tile (i, j) of layer k on position `letter` (z up, the same frame as hexoctCrystal before it is centred). */
export const hexoctBall = (letter, i, j, k) => [POS[letter][0] + i * A1[0] + j * A2[0], POS[letter][1] + i * A1[1] + j * A2[1], k * LAYER_H];
/** One tile of `type` (of a set, '75' by default) at ball (i, j) of layer k whose layers below, at and above sit on the letters given:
 *  its pieces [{ type, role, vertices, faces }], placed exactly as hexoctCrystal places them (by tileMotion). */
export function hexoctTileAt(type, below, at, above, i, j, k, set = '75') {
  const place = hexoctPlace(type, below, at, above, i, j, k);
  return hexoctTile(type, set).map((p) => ({ type, role: p.role, vertices: p.vertices.map(place), faces: p.faces }));
}
/** The map taking a point of the `type` reference tile to tile (i, j) of layer k (as hexoctTileAt). */
export function hexoctPlace(type, below, at, above, i, j, k) {
  const M = tileMotion(type, below, at, above), o = hexoctBall(at, i, j, k);
  return (v) => apply(M, v).map((x, c) => x + o[c]);
}
