// The Red Queen 120-cell (DICTO 2026-10-28, paper #65): built exactly from the White Queen 600-cell (white-queen-geometry.js), as #65
// builds it: its 600 corners are the centres of her 600 cells, its 1200 edges join two cells that share a triangle, its 720 pentagons
// stand round her 720 edges (the five cells on each edge), and its 120 dodecahedra round her 120 vertices (the twenty cells at each).
// The four main directions are the atlas's own (red-queen-data.js, from atlas120.json); the shadows, slices, nine cell layers and
// halves are computed live from this model as the White Queen's are from hers. Pure maths, no three.js.
import RQ from './red-queen-data.js';
import { VERTICES as WV, EDGES as WE, CELLS as WC, VERTICES_EXACT, Q5, hull, turn, q5String } from './white-queen-geometry.js';

const { R, qAdd, qMul, qFloat, qKey } = Q5;
export const DIRECTIONS = ['vertex-first', 'edge-first', 'face-first', 'cell-first'];
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const unit = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

// ---- the model ----
/** The 600 corners exactly, [a, b] per coordinate: the centre of each of the White Queen's cells (the mean of its four vertices). */
export const VERTICES_EXACT_RQ = WC.map((c) => [0, 1, 2, 3].map((a) => qMul(c.reduce((s, k) => qAdd(s, VERTICES_EXACT[k][a]), [R(0), R(0)]), [R(1, 4), R(0)])));
export const VERTICES = VERTICES_EXACT_RQ.map((v) => v.map(qFloat));
/** The 1200 edges: two cells sharing a triangle. */
const cellsOfTri = new Map();
WC.forEach((c, ci) => { for (const t of [[c[0], c[1], c[2]], [c[0], c[1], c[3]], [c[0], c[2], c[3]], [c[1], c[2], c[3]]]) { const k = [...t].sort((a, b) => a - b).join(','); if (!cellsOfTri.has(k)) cellsOfTri.set(k, []); cellsOfTri.get(k).push(ci); } });
export const EDGES = [...cellsOfTri.values()].filter((x) => x.length === 2);
const adjacent = new Set(EDGES.map(([a, b]) => `${Math.min(a, b)},${Math.max(a, b)}`));
const isEdge = (a, b) => adjacent.has(`${Math.min(a, b)},${Math.max(a, b)}`);
/** The 720 pentagons, one round each of the White Queen's edges: its five cells in order round it (each next one sharing a triangle). */
export const PENTAGONS = WE.map(([i, j]) => {
  const ring = WC.map((c, ci) => (c.includes(i) && c.includes(j) ? ci : -1)).filter((ci) => ci >= 0), loop = [ring[0]];
  while (loop.length < ring.length) loop.push(ring.find((x) => !loop.includes(x) && isEdge(x, loop[loop.length - 1])));
  return loop;
});
/** The 120 dodecahedra, one round each of the White Queen's vertices: { corners (its 20 cells), faces (its 12 pentagons) }. */
export const CELLS = WV.map((_, v) => ({ corners: WC.map((c, ci) => (c.includes(v) ? ci : -1)).filter((ci) => ci >= 0), faces: WE.map(([i, j], e) => (i === v || j === v ? e : -1)).filter((e) => e >= 0) }));
/** A dodecahedron's faces as loops of corner indices, for drawing. */
export const cellFaces = (ci) => CELLS[ci].faces.map((p) => PENTAGONS[p]);
export const RADIUS = Math.hypot(...VERTICES[0]);   // √(7/4 + 3/4√5), the corners' radius when the White Queen's is 2

// ---- the four main directions (the atlas's d, exactly) and their frames ----
/** '7/8 + 3/8√5', '1/4', '0', '-1/2 + 1/2√5', '√5' → [a, b] with a, b rationals. */
function parseQ5(s) {
  let a = R(0), b = R(0);
  const terms = s.replace(/\s+/g, '').replace(/-/g, '+-').split('+').filter(Boolean);
  for (const t0 of terms) {
    const root = t0.endsWith('√5'), t = root ? t0.slice(0, -2) : t0, neg = t.startsWith('-'), body = neg ? t.slice(1) : t;
    const [p, q = '1'] = (body === '' ? '1' : body).split('/'), r = R((neg ? -1 : 1) * Number(p), Number(q));
    if (root) b = qAdd([R(0), b], [R(0), r])[1]; else a = qAdd([a, R(0)], [r, R(0)])[0];
  }
  return [a, b];
}
const D_EXACT = DIRECTIONS.map((k) => RQ.directions[k].d_exact.map(parseQ5));
export const UNIT_DIRECTIONS = D_EXACT.map((d) => unit(d.map(qFloat)));
function turning(i, j) {
  const a = UNIT_DIRECTIONS[i], b = UNIT_DIRECTIONS[j], c = dot(a, b);
  return { a, w: unit(b.map((x, k) => x - c * a[k])), angle: Math.acos(Math.max(-1, Math.min(1, c))) };
}
// vertex-first's frame: the coordinate axes made orthogonal to its direction (Gram–Schmidt, the three longest kept); the others carry
// it along the turnings vertex → edge → face → cell, as the White Queen's do
const gram = (d) => {
  const out = [];
  for (const e of [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]]) {
    let v = e.slice();
    for (const b of [d, ...out]) { const c = dot(v, b); v = v.map((x, i) => x - c * b[i]); }
    if (Math.hypot(...v) > 1e-6 && out.length < 3) out.push(unit(v));
  }
  return out;
};
export const FRAMES = [gram(UNIT_DIRECTIONS[0])];
for (let i = 0; i < 3; i++) { const st = turning(i, i + 1); FRAMES.push(FRAMES[i].map((f) => turn(f, st, st.angle))); }
const indexOf = (k) => (typeof k === 'number' ? k : DIRECTIONS.indexOf(k));
export function viewAt(from, to, s) {
  const i = indexOf(from), j = indexOf(to), x = Math.max(0, Math.min(1, s));
  if (x === 0 || i === j) return { u: UNIT_DIRECTIONS[i], frame: FRAMES[i] };
  const st = turning(i, j), ang = st.angle * x;
  return { u: x === 1 ? UNIT_DIRECTIONS[j] : turn(UNIT_DIRECTIONS[i], st, ang), frame: FRAMES[i].map((f) => turn(f, st, ang)) };
}
export const project = ({ frame }) => VERTICES.map((v) => frame.map((f) => dot(v, f)));

// ---- shadows ----
const cache = new Map();
export function shadowAt(from, to, s) {
  const key = `${indexOf(from)}${indexOf(to)}${Math.round(s * 1e6)}`;
  if (cache.has(key)) return cache.get(key);
  const view = viewAt(from, to, s), P = project(view), H = hull(P);
  const out = { u: view.u, P, ...H };
  if (cache.size > 64) cache.clear();
  cache.set(key, out);
  return out;
}

// ---- slices: the cut by the 3-space x·d = h, d the atlas's own d (heights compare within one direction, as #65) ----
const HEIGHTS = D_EXACT.map((d) => VERTICES_EXACT_RQ.map((v) => v.reduce((s, x, i) => qAdd(s, qMul(x, d[i])), [R(0), R(0)])));
export const SLICE_STOPS = DIRECTIONS.map((_, n) => {
  const seen = new Map();
  for (const h of HEIGHTS[n]) seen.set(qKey(h), h);
  const hs = [...seen.values()].sort((x, y) => qFloat(x) - qFloat(y));
  const cuts = [...hs.map((h) => ({ h, atVertex: true })), ...hs.slice(1).map((h, i) => ({ h: qMul(qAdd(hs[i], h), [R(1, 2), R(0)]), atVertex: false }))];
  const top = qFloat(hs[hs.length - 1]);
  return cuts.filter((c) => qFloat(c.h) > -1e-12).sort((x, y) => qFloat(x.h) - qFloat(y.h))
    .map((c) => ({ ...c, height: q5String(c.h), value: qFloat(c.h), tip: Math.abs(qFloat(c.h) - top) < 1e-12 }));
});
const sliceCache = new Map();
export function sliceAt(dir, k) {
  const n = indexOf(dir), key = `${n}.${k}`;
  if (sliceCache.has(key)) return sliceCache.get(key);
  const stop = SLICE_STOPS[n][k], hk = qKey(stop.h), hv = stop.value, H = HEIGHTS[n], frame = FRAMES[n];
  const pts4 = VERTICES.filter((_, i) => qKey(H[i]) === hk);
  for (const [a, b] of EDGES) {
    const ha = qFloat(H[a]), hb = qFloat(H[b]);
    if ((ha - hv) * (hb - hv) < 0 && qKey(H[a]) !== hk && qKey(H[b]) !== hk) {
      const t = (hv - ha) / (hb - ha);
      pts4.push(VERTICES[a].map((x, i) => x + t * (VERTICES[b][i] - x)));
    }
  }
  const points = pts4.map((p) => frame.map((f) => dot(p, f)));
  let dim = 0;
  if (points.length > 1) {
    const o = points[0], far = points.reduce((b, p) => (Math.hypot(...sub(p, o)) > Math.hypot(...sub(b, o)) ? p : b), o), e = sub(far, o);
    if (Math.hypot(...e) > 1e-9) dim = 1;
    const off = points.map((p) => Math.hypot(...cross(e, sub(p, o))) / Math.hypot(...e));
    const k3 = off.indexOf(Math.max(...off));
    if (dim && off[k3] > 1e-9) {
      dim = 2;
      const nn = cross(e, sub(points[k3], o));
      if (points.some((p) => Math.abs(dot3(nn, sub(p, o))) / Math.hypot(...nn) > 1e-9)) dim = 3;
    }
  }
  const out = { stop, points, dim, ...(dim === 3 ? hull(points) : {}) };
  sliceCache.set(key, out);
  return out;
}

// ---- the nine cell layers (#65): the 120 dodecahedra round the one at the White Queen's vertex (2, 0, 0, 0), by the height of their
// centres along it (1, 12, 20, 12, 30, 12, 20, 12, 1), seen in perspective from just beyond the opposite dodecahedron, as her Cleo shells
// are; the core is the dodecahedron whose corners are the centres of her Cleo core's 20 cells.
const FRAME_UP = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];
export const LAYER_EYE = -1.05 * RADIUS;
export const LAYER_POINTS = VERTICES.map((x) => FRAME_UP.map((f) => dot(x, f) / (x[0] - LAYER_EYE)));
export const CELL_LAYERS = (() => {
  const by = new Map();
  WV.forEach((v, i) => { const key = Math.round(v[0] * 1e9); if (!by.has(key)) by.set(key, { height: v[0], cells: [] }); by.get(key).cells.push(i); });
  return [...by.values()].sort((a, b) => b.height - a.height);
})();

// ---- halves: a dodecahedron is in front if its centre (her vertex) · u > 0 ----
export function halves(u) {
  const out = { front: [], back: [], side: [] };
  WV.forEach((c, i) => { const x = dot(c, u); out[x > 1e-9 ? 'front' : x < -1e-9 ? 'back' : 'side'].push(i); });
  return out;
}

// ---- Line up: each direction's main symmetry axis inside its slicing 3-space, in the direction's own frame:
//   vertex-first: a 3-fold axis, towards a neighbour (the vertex figure is a tetrahedron);
//   edge-first:   the edge itself, the 3-fold axis of the three pentagons round it;
//   face-first:   the 5-fold axis, normal to the pentagon within the 3-space;
//   cell-first:   a 5-fold axis through the dodecahedron, from its centre towards one of its pentagons' centres.
export const SLICE_AXES = DIRECTIONS.map((k, n) => {
  const el = RQ.directions[k].element, d = UNIT_DIRECTIONS[n];
  const inSpace = (a) => { const c = dot(a, d); return a.map((x, i) => x - c * d[i]); };
  const V = (i) => VERTICES[i];
  let a;
  if (k === 'vertex-first') a = inSpace(V(EDGES.find(([i, j]) => i === el[0] || j === el[0]).find((x) => x !== el[0])));
  else if (k === 'edge-first') a = inSpace(V(el[1]).map((x, i) => x - V(el[0])[i]));
  else if (k === 'cell-first') {
    const cell = CELLS.find((c) => el.every((x) => c.corners.includes(x))) ?? CELLS[0], loop = PENTAGONS[cell.faces[0]];
    a = inSpace([0, 1, 2, 3].map((i) => loop.reduce((s, x) => s + V(x)[i], 0) / 5));
  } else {
    // the unit vector orthogonal to d and to the pentagon's plane (Gram–Schmidt from the coordinate axes)
    const basis = [d, unit(inSpace(V(el[1]).map((x, i) => x - V(el[0])[i])))];
    const e2 = V(el[2]).map((x, i) => x - V(el[0])[i]);
    basis.push(unit(basis.reduce((v, b) => { const c = dot(v, b); return v.map((x, i) => x - c * b[i]); }, e2)));
    a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]].map((e) => basis.reduce((v, b) => { const c = dot(v, b); return v.map((x, i) => x - c * b[i]); }, e)).sort((x, y) => Math.hypot(...y) - Math.hypot(...x))[0];
  }
  const v = FRAMES[n].map((f) => dot(a, f)), l = Math.hypot(...v);
  return v.map((x) => x / l);
});
