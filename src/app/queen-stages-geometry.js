// The five stages between the White Queen and the Red Queen (DICTO 2026-10-30; k-research studies/2026-10-30-queen-stages): the
// Wythoff truncations of the 600-cell, built from the White Queen's own corners, edges, triangles and cells with the cut positions
// solved there (stages.py, cuts.py: every edge one length to 1e-14):
//   truncated 600-cell   a corner at 1/3 along each edge from each end            1440 corners, 120 icosahedra + 600 truncated tetrahedra
//   rectified 600-cell   the middle of each edge                                    720 corners, 120 icosahedra + 600 octahedra
//   bitruncated          on each triangle, 3/5 of the way from each edge's middle   3600 corners, 120 truncated icosahedra + 600 truncated
//                        to the triangle's centre                                    tetrahedra (the midpoint, halfway from White to Red)
//   rectified 120-cell   the centre of each triangle                               1200 corners, 120 icosidodecahedra + 600 tetrahedra
//   truncated 120-cell   at (5 − √5)/10 along each Red Queen edge (the centres of   2400 corners, 120 truncated dodecahedra + 600 tetrahedra
//                        two cells sharing a triangle) from each end
// Each is scaled to the White Queen's radius 2 and drawn as a shadow in the White Queen's own views (viewAt, hull).
import { VERTICES, EDGES, CELLS, viewAt, hull } from './white-queen-geometry.js';

export const STAGE_KEYS = ['white', 't01', 't1', 't12', 't2', 't23', 'red'];
export const STAGE_FACTS = {
  t01: { V: 1440, E: 4320, cells: [[120, 'icosahedron'], [600, 'truncatedTetrahedron']] },
  t1: { V: 720, E: 3600, cells: [[120, 'icosahedron'], [600, 'octahedron']] },
  t12: { V: 3600, E: 7200, cells: [[120, 'truncatedIcosahedron'], [600, 'truncatedTetrahedron']] },
  t2: { V: 1200, E: 3600, cells: [[120, 'icosidodecahedron'], [600, 'tetrahedron']] },
  t23: { V: 2400, E: 4800, cells: [[120, 'truncatedDodecahedron'], [600, 'tetrahedron']] },
};
const RADIUS = 2;
const mix = (p, q, s) => p.map((x, i) => (1 - s) * x + s * q[i]);
const mean = (ids) => [0, 1, 2, 3].map((k) => ids.reduce((s, i) => s + VERTICES[i][k], 0) / ids.length);

// the White Queen's triangles and her 1200 cell pairs sharing a triangle (the Red Queen's edges)
const TRIANGLES = [], PAIRS = [];
{
  const byFace = new Map();
  CELLS.forEach((c, ci) => {
    for (const f of [[c[0], c[1], c[2]], [c[0], c[1], c[3]], [c[0], c[2], c[3]], [c[1], c[2], c[3]]]) {
      const key = [...f].sort((a, b) => a - b).join(',');
      if (!byFace.has(key)) { byFace.set(key, []); TRIANGLES.push(f); }
      byFace.get(key).push(ci);
    }
  });
  for (const v of byFace.values()) PAIRS.push(v);
}
const CENTRES = CELLS.map(mean);
const BUILD = {
  t01: () => EDGES.flatMap(([a, b]) => [mix(VERTICES[a], VERTICES[b], 1 / 3), mix(VERTICES[b], VERTICES[a], 1 / 3)]),
  t1: () => EDGES.map(([a, b]) => mix(VERTICES[a], VERTICES[b], 0.5)),
  t12: () => TRIANGLES.flatMap((t) => { const c = mean(t); return [[t[0], t[1]], [t[0], t[2]], [t[1], t[2]]].map((e) => mix(mean(e), c, 3 / 5)); }),
  t2: () => TRIANGLES.map(mean),
  t23: () => { const s = (5 - Math.sqrt(5)) / 10; return PAIRS.flatMap(([a, b]) => [mix(CENTRES[a], CENTRES[b], s), mix(CENTRES[b], CENTRES[a], s)]); },
};

/** The edges of a uniform point set: the pairs at the shortest distance (a 4D grid of buckets one edge wide). */
function shortestPairs(P) {
  let m = Infinity;
  for (let j = 1; j < P.length; j++) { const d = Math.hypot(...P[0].map((x, k) => x - P[j][k])); if (d > 1e-9 && d < m) m = d; }
  const key = (p) => p.map((x) => Math.floor(x / m)).join(','), grid = new Map();
  P.forEach((p, i) => { const k = key(p); if (!grid.has(k)) grid.set(k, []); grid.get(k).push(i); });
  const out = [], steps = [-1, 0, 1];
  P.forEach((p, i) => {
    const b = p.map((x) => Math.floor(x / m));
    for (const a0 of steps) for (const a1 of steps) for (const a2 of steps) for (const a3 of steps) {
      for (const j of grid.get([b[0] + a0, b[1] + a1, b[2] + a2, b[3] + a3].join(',')) ?? []) {
        if (j > i && Math.abs(Math.hypot(...p.map((x, k) => x - P[j][k])) - m) < 1e-7 * m) out.push([i, j]);
      }
    }
  });
  return out;
}

const built = new Map();
/** A stage's corners (4D, radius 2) and edges. */
export function stage(key) {
  if (!built.has(key)) {
    const P = BUILD[key](), r = Math.hypot(...P[0]), V = P.map((p) => p.map((x) => (x * RADIUS) / r));
    built.set(key, { vertices: V, edges: shortestPairs(V) });
  }
  return built.get(key);
}

const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const cache = new Map();
/** A stage's shadow at fraction s of the turning from `from` to `to`: projected corners P, its edges, and the hull of the shadow. */
export function stageShadowAt(key, from, to, s) {
  const ck = `${key}${from}${to}${Math.round(s * 1e6)}`;
  if (cache.has(ck)) return cache.get(ck);
  const st = stage(key), view = viewAt(from, to, s), P = st.vertices.map((v) => view.frame.map((f) => dot(v, f)));
  const out = { u: view.u, P, edges: st.edges, ...hull(P) };
  if (cache.size > 24) cache.clear();
  cache.set(ck, out);
  return out;
}
