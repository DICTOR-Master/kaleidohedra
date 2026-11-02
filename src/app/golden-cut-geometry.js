// ✂ Golden Cut (DICTO, paper #88 "Golden Cuts: the DICTO-Kepler Golden Truncations and the DICTO-GTT-Solids"): a Platonic solid of
// edge 1 cut the same depth x (0 < x < 1/2, measured along each edge from its corner) at every corner. Each corner becomes a regular
// polygon of side k·x (k = 1 for the tetrahedron, octahedron and icosahedron, √2 for the cube, φ for the dodecahedron: the corner
// figure's side over the edge) and each original face a truncated polygon with sides k·x and 1 − 2x. Three marked stops:
//   archimedean  the sides equal, k·x = 1 − 2x: x = 1/(k + 2) (the Archimedean truncated solid);
//   greater      the Greater Golden Cut, corner sides long: k·x = φ(1 − 2x), x = φ/(k + 2φ);
//   lesser       the Lesser Golden Cut, original sides long: 1 − 2x = φ·k·x, x = 1/(φk + 2).
// For the octahedron DICTO names the two golden stops Icosaxes (greater) and Unborn Axes (lesser): they are krp-core's DICTO_ICOSAXES
// and DICTO_UNBORN_AXES (golden-split.js) up to size, checked in tests/unit/golden-cut.test.mjs.
// The solids come from krp-core's registry through Aristotle's Pyramid's five (D·I·C·T·O, DICTO's order) and DICTO Vacuus's
// outward-wound, centred form; no three.js here, so the unit tests run it.
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { SOLID_KEYS, SOLID_IDS } from './aristotle-geometry.js';
import { vacuusSolidOf } from './vacuus-geometry.js';

export const PHI = (1 + Math.sqrt(5)) / 2;
/** The five, in DICTO's order (dodecahedron, icosahedron, cube, tetrahedron, octahedron), and their registry ids. */
export const GCUT_SOLIDS = SOLID_KEYS;
export const GCUT_IDS = SOLID_IDS;
/** The corner polygon's side per unit of cut: the chord of the corner figure. */
export const GCUT_K = { dodecahedron: PHI, icosahedron: 1, cube: Math.SQRT2, tetrahedron: 1, octahedron: 1 };
/** The stops, in slider order (x growing). */
export const GCUT_STOPS = ['lesser', 'archimedean', 'greater'];
/** The slider's reach: the open interval 0 < x < 1/2, kept clear of the two ends where a polygon closes up. */
export const X_MIN = 0.01, X_MAX = 0.49;

/** The cut x of a stop on solid `key`. */
export function stopX(key, stop) {
  const k = GCUT_K[key];
  if (stop === 'greater') return PHI / (k + 2 * PHI);
  if (stop === 'lesser') return 1 / (PHI * k + 2);
  if (stop === 'archimedean') return 1 / (k + 2);
  return NaN;
}

/** The stop that cut x is at (to `tol`), else null. */
export function stopAt(key, x, tol = 1e-9) {
  return GCUT_STOPS.find((s) => Math.abs(stopX(key, s) - x) <= tol) ?? null;
}

/** The two side lengths at cut x and their ratio long/short (≥ 1). */
export function sidesAt(key, x) {
  const corner = GCUT_K[key] * x, original = 1 - 2 * x;
  return { corner, original, ratio: Math.max(corner, original) / Math.min(corner, original) };
}

/** A solid key from an address word: a key (octahedron), its name in capitals (OCTAHEDRON) or its registry id (D8); else null. */
export function gcutKeyOf(word) {
  if (!word) return null;
  const w = String(word).toLowerCase();
  return GCUT_SOLIDS.find((k) => k === w || GCUT_IDS[k].toLowerCase() === w) ?? null;
}
/** The key of registry id `id` when it is one of the five, else null. */
export const gcutKeyOfId = (id) => GCUT_SOLIDS.find((k) => GCUT_IDS[k] === id) ?? null;

const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];

/** Solid `key` cut at x: { vertices, corners: [loop], faces: [loop], edge } about the solid's centre. Loops are point lists, wound
 *  outward; `corners` are the regular corner polygons (one per original corner), `faces` the truncated original faces (one per face).
 *  The registry's solid is scaled to edge 1 first (it is already; the scale guards it). */
export function goldenCut(key, x) {
  const s = vacuusSolidOf(POLYHEDRA[GCUT_IDS[key]]);
  const [a0, b0] = s.edges[0], P0 = s.vertices, len = Math.hypot(P0[a0][0] - P0[b0][0], P0[a0][1] - P0[b0][1], P0[a0][2] - P0[b0][2]);
  const P = P0.map((p) => p.map((c) => c / len));
  // the cut point on edge v→w, at x from v
  const at = new Map();
  const cut = (v, w) => { const k = `${v},${w}`; if (!at.has(k)) at.set(k, lerp(P[v], P[w], x)); return at.get(k); };
  // each face keeps its loop with every corner cut off: near v_i towards v_{i+1}, then near v_{i+1} towards v_i
  const faces = s.faces.map((f) => f.flatMap((v, i) => { const w = f[(i + 1) % f.length]; return [cut(v, w), cut(w, v)]; }));
  // round corner v, a face (… u, v, w …) runs cut(v, u) → cut(v, w); the corner polygon crosses that segment the other way, so from
  // cut(v, w) it goes on to cut(v, u): follow next[w] = u round v.
  const next = P.map(() => new Map());
  for (const f of s.faces) f.forEach((v, i) => next[v].set(f[(i + 1) % f.length], f[(i - 1 + f.length) % f.length]));
  const corners = next.map((m, v) => {
    const start = m.keys().next().value, loop = [];
    let w = start;
    do { loop.push(cut(v, w)); w = m.get(w); } while (w !== start && loop.length <= m.size);
    return loop;
  });
  return { vertices: [...at.values()], corners, faces, edge: 1 };
}

/** Volume of a closed surface given as outward point loops (fan from each loop's first point). */
export function volumeOf(loops) {
  let v = 0;
  for (const L of loops) for (let i = 1; i + 1 < L.length; i++) {
    const [a, b, c] = [L[0], L[i], L[i + 1]];
    v += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6;
  }
  return v;
}
