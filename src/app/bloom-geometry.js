// The Icosaxes Bloom's geometry (DICTO 2026-10-27): paper #59, "The Icosaxes Hexa: Bloom, Bud and Seed" (DICTO DOI
// 10.5281/zenodo.23677485). Twenty Icosaxes (or Lotus Jewel Axes), one on each corner of a dodecahedron, each turned by the rotation of
// the icosahedron that carries (1,1,1) to its corner, centres at distance d. Stops, as fractions of the first touch φ²√3/2: the Bloom
// (1, twelve open windows), the Bud (1/φ, sealed round a hollow), the Seed (1/3, one solid; Lotus Jewel Axes 1/φ³). The Icosaxes
// Hexa (8 Icosaxes round an Unborn Axes), the Lotus Hexa (keyed outward round a Dodecaxes) and a patch of the keyed Icosaxes Kagome
// network. Pieces from krp-core's golden split (icosahedron edge 1). No three.js here, so the unit tests can run it.
import { PHI, ICO, SIGNS, FLAT, INTO_BIG, INTO_SMALL, pieceSurface, toPolygons } from '../krp-core/src/polyhedra/golden-split.js';

export const TOUCH = (PHI * PHI * Math.sqrt(3)) / 2;
export const STOP_FRACTIONS = { bloom: 1, bud: 1 / PHI, seed: 1 / 3, lotusSeed: 1 / PHI ** 3 };

const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const mul = (A, B) => A.map((r) => [0, 1, 2].map((j) => r[0] * B[0][j] + r[1] * B[1][j] + r[2] * B[2][j]));
const apply = (M, v) => M.map((r) => dot(r, v));
const r6 = (x) => Math.round(x * 1e6) + 0;                       // + 0: no −0, so rounding noise near zero gives one key
const key = (M) => M.flat().map(r6).join();
/** The 60 rotations of the icosahedron (corners (0, ±1/2, ±φ/2) and cyclic), from a three-fold and a five-fold turn. */
export function rotations() {
  const C3 = [[0, 0, 1], [1, 0, 0], [0, 1, 0]];
  const k = [0, 1, PHI].map((x) => x / Math.hypot(1, PHI)), c = Math.cos((2 * Math.PI) / 5), s = Math.sin((2 * Math.PI) / 5);
  const C5 = [0, 1, 2].map((i) => [0, 1, 2].map((j) => (i === j ? c : 0) + (1 - c) * k[i] * k[j] + s * [[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]][i][j]));
  const out = new Map([[key([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]]);
  for (let grew = true; grew;) {
    grew = false;
    for (const M of [...out.values()]) for (const g of [C3, C5]) { const N = mul(g, M); if (!out.has(key(N))) { out.set(key(N), N); grew = true; } }
  }
  return [...out.values()];
}
const U = [1, 1, 1].map((x) => x / Math.sqrt(3));
/** One rotation per corner of the dodecahedron: the twenty that carry (1,1,1) to each corner (the three-fold turn keeps the piece). */
export function cornerTurns() {
  const seen = new Map();
  for (const M of rotations()) { const c = apply(M, U), k2 = c.map(r6).join(); if (!seen.has(k2)) seen.set(k2, M); }
  return [...seen.values()];
}
const mesh = (big, states) => toPolygons(pieceSurface(big, states));
export const ICOSAXES = mesh(true, Array(8).fill(FLAT));
export const LOTUS_JEWEL_AXES = mesh(true, Array(8).fill(INTO_BIG));
export const UNBORN_AXES = mesh(false, Array(8).fill(FLAT));
export const DODECAXES = mesh(false, Array(8).fill(INTO_BIG));
/** Volume of a closed polygon mesh with outward faces. */
export function volume({ vertices: V, faces: F }) {
  let v = 0;
  for (const f of F) for (let i = 1; i + 1 < f.length; i++) { const [a, b, c] = [V[f[0]], V[f[i]], V[f[i + 1]]]; v += dot(a, [b[1] * c[2] - b[2] * c[1], b[2] * c[0] - b[0] * c[2], b[0] * c[1] - b[1] * c[0]]); }
  return v / 6;
}
/** The twenty pieces at fraction f of the first touch: [{ vertices, faces, centre }]. */
export function twenty(lotus, f) {
  const P = lotus ? LOTUS_JEWEL_AXES : ICOSAXES, d = f * TOUCH;
  return cornerTurns().map((M) => { const t = apply(M, U).map((x) => x * d); return { vertices: P.vertices.map((v) => apply(M, v).map((x, i) => x + t[i])), faces: P.faces, centre: t }; });
}
const at = (n) => n.map((x) => (x * PHI) / 2);
const moved = (m, t) => ({ vertices: m.vertices.map((v) => v.map((x, i) => x + t[i])), faces: m.faces, centre: t });
const CORNERS = SIGNS.map((s) => [...s]);
/** The Icosaxes Hexa: eight Icosaxes on a cube round an Unborn Axes; keyed (the Lotus Hexa): each corner piece dented towards the
 *  centre, keyed outward on its other seven hexagons, round a Dodecaxes. [{ role: 'big' | 'small', vertices, faces, centre }] */
export function hexa(keyed) {
  const out = [{ role: 'small', ...moved(keyed ? DODECAXES : UNBORN_AXES, [0, 0, 0]) }];
  for (const c of CORNERS) {
    const states = keyed ? SIGNS.map((s) => (s.every((x, i) => x === -c[i]) ? INTO_BIG : INTO_SMALL)) : Array(8).fill(FLAT);
    out.push({ role: 'big', ...moved(mesh(true, states), at(c)) });
  }
  return out;
}
/** A patch of the keyed Icosaxes Kagome network: cube clusters on a body-centred lattice of Unborn Axes sites (the middle one and its
 *  eight neighbours), a Dodecaxes at each cluster centre; each Icosaxes dented towards its cluster centres, keyed outward elsewhere. */
export function kagome() {
  const anchors = [[0, 0, 0], ...SIGNS.map((s) => s.map((x) => 2 * x))], centre = new Set(anchors.map((a) => a.join()));
  const ico = new Map();
  for (const a of anchors) for (const s of SIGNS) { const n = a.map((x, i) => x + s[i]); ico.set(n.join(), n); }
  const cache = new Map(), out = anchors.map((a) => ({ role: 'small', ...moved(DODECAXES, at(a)) }));
  for (const n of ico.values()) {
    const states = SIGNS.map((s) => (centre.has(n.map((x, i) => x + s[i]).join()) ? INTO_BIG : INTO_SMALL)), k2 = states.join();
    if (!cache.has(k2)) cache.set(k2, mesh(true, states));
    out.push({ role: 'big', ...moved(cache.get(k2), at(n)) });
  }
  return out;
}
