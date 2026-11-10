// The 4D Permutohedron (DICTO 2026-11-10; working name, DICTO names it): the geometry of DICTO's page "The 4D Permutohedron"
// (k-research studies/2026-11-10-permutohedron), ported line for line from it, from the same data (perm4-data.js). Pure maths, no three.js.
//   Build: a Schlegel view from just outside one truncated octahedron (the first cell, the outer shell): the eye at 1.18 × that cell's
//     3-space distance along its centre direction, every corner projected from the eye onto that 3-space, scaled to radius 1.
//   Sweep: the 3D cut x·d = h at the middle of each of the 119 gaps between the 120 corner heights along the page's direction d; each
//     cell's cross-section is the crossing points of its edges, ordered round the polygon. The page's events (scripts/perm4_data.py):
//     events[k] compares gap k with gap k + 1 (born, died, pairs lost and gained).
import D from './perm4-data.js';

export const X = D.X, EDGES = D.edges, CELLS = D.cells, EVENTS = D.sweep.events, PAIRS = D.pairs, SWEEP_D = D.sweep.d;
export const KINDS = ['all', 'to', 'hp'];
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const cen4 = (vs) => [0, 1, 2, 3].map((k) => vs.reduce((s, v) => s + X[v][k], 0) / vs.length);
/** An orthonormal basis of the 3-space across the unit vector n (Gram–Schmidt from the coordinate axes, as the page). */
function across(n) {
  const basis = [];
  for (const e of [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) {
    let v = e.map((x, i) => x - dot(e, n) * n[i]);
    for (const b of basis) { const p = dot(v, b); v = v.map((x, i) => x - p * b[i]); }
    const L = Math.hypot(...v);
    if (L > 1e-6 && basis.length < 3) basis.push(v.map((x) => x / L));
  }
  return basis;
}

// ---- Build: the Schlegel view ----
export const OUTER = CELLS.findIndex((c) => c.kind === 'TO');
export const EYE_FACTOR = 1.18;
const n0 = cen4(CELLS[OUTER].V), hf = Math.hypot(...n0), nh = n0.map((x) => x / hf), eye = nh.map((x) => x * hf * EYE_FACTOR), basis = across(nh);
const S3 = X.map((x) => { const dx = x.map((v, i) => v - eye[i]), t = (hf - dot(eye, nh)) / dot(dx, nh), p = eye.map((v, i) => v + t * dx[i]); return basis.map((b) => dot(p, b)); });
const sc = 1 / Math.max(...S3.map((p) => Math.hypot(...p)));
/** The 120 corners in the Schlegel view, radius 1. */
export const BUILD_POINTS = S3.map((p) => p.map((x) => x * sc));
const inKind = (c, kind) => kind === 'all' || (kind === 'to' ? c.kind === 'TO' : c.kind === 'HP');
/** The cells drawn in Build for a kind ('all' | 'to' | 'hp') and a pull (0..1): each inner cell shifted by its centroid × pull × 0.9.
 *  [{ cell, kind, outer, faces: [3D loops] }]. */
export function buildCells(kind, pull) {
  const P = BUILD_POINTS, out = [];
  CELLS.forEach((c, ci) => {
    if (!inKind(c, kind)) return;
    const cc = [0, 1, 2].map((k) => c.V.reduce((s, v) => s + P[v][k], 0) / c.V.length);
    const shift = ci === OUTER ? [0, 0, 0] : cc.map((x) => x * pull * 0.9);
    out.push({ cell: ci, kind: c.kind, outer: ci === OUTER, faces: c.F.map((f) => f.map((v) => P[v].map((x, k) => x + shift[k]))) });
  });
  return out;
}

// ---- Sweep ----
const hb = across(SWEEP_D);
export const HEIGHTS = X.map((x) => dot(x, SWEEP_D));
const sorted = [...HEIGHTS].sort((a, b) => a - b);
/** The middles of the 119 gaps between the corner heights, bottom to top. */
export const GAPS = sorted.slice(0, -1).map((h, k) => (h + sorted[k + 1]) / 2);
const CELL_EDGES = CELLS.map((c) => { const s = new Set(c.V); return EDGES.filter(([a, b]) => s.has(a) && s.has(b)); });
const R0 = 1 / Math.max(...X.map((x) => Math.hypot(...x)));
export const SWEEP_SCALE = R0 * 1.15;
/** A cell's cross-section at height h: its edges' crossing points in the cut's own frame, ordered round the polygon (null if none). */
function section(ci, h) {
  const pts = [];
  for (const [a, b] of CELL_EDGES[ci]) {
    const ha = HEIGHTS[a], hb_ = HEIGHTS[b];
    if ((ha - h) * (hb_ - h) < 0) { const t = (h - ha) / (hb_ - ha); pts.push(hb.map((B) => dot(X[a].map((x, i) => x + t * (X[b][i] - x)), B))); }
  }
  if (pts.length < 3) return null;
  const cc = [0, 1, 2].map((k) => pts.reduce((s, p) => s + p[k], 0) / pts.length);
  const cr = (u, w) => [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
  const v1 = pts[0].map((x, i) => x - cc[i]);
  let nrm = cr(v1, pts[1].map((x, i) => x - cc[i]));
  for (let k = 2; Math.hypot(...nrm) < 1e-9 && k < pts.length; k++) nrm = cr(v1, pts[k].map((x, i) => x - cc[i]));
  const L = Math.hypot(...nrm), nn = nrm.map((x) => x / L), e1 = v1.map((x) => x / Math.hypot(...v1)), e2 = cr(nn, e1);
  const ang = (p) => { const v = p.map((x, i) => x - cc[i]); return Math.atan2(dot(v, e2), dot(v, e1)); };
  return pts.sort((p, q) => ang(p) - ang(q));
}
const isSwap = (e) => !!(e && e.lost.length && e.gained.length);
/** The number of swaps up to and including gap k's change (the page's count). */
export const swapsUpTo = (k) => { let n = 0; for (let j = 0; j < k; j++) if (isSwap(EVENTS[j])) n++; return n; };
export const SWAP_TOTAL = EVENTS.filter(isSwap).length;   // 66
/** The cut at gap k (0..118) for a kind: { k, h, cells: [{ cell, kind, role: 'go' | 'meet' | null, points }], alive, to, hp,
 *  event (the change at the corner just below: the last change), what: 'swap' | 'born' | 'died' | 'first', swap (its number) }. */
export function sweepAt(k, kind) {
  const h = GAPS[k], ev = EVENTS[k - 1] ?? { lost: [], gained: [], born: [], died: [] };
  const go = new Set(ev.lost.flat()), meet = new Set(ev.gained.flat()), cells = [];
  CELLS.forEach((c, ci) => {
    if (!inKind(c, kind)) return;
    const s = section(ci, h);
    if (s) cells.push({ cell: ci, kind: c.kind, role: go.has(ci) ? 'go' : meet.has(ci) ? 'meet' : null, points: s.map((p) => p.map((x) => x * SWEEP_SCALE)) });
  });
  const to = cells.filter((c) => c.kind === 'TO').length;
  const what = isSwap(ev) ? 'swap' : ev.born.length ? 'born' : ev.died.length ? 'died' : 'first';
  return { k, h, cells, alive: cells.length, to, hp: cells.length - to, event: ev, what, swap: swapsUpTo(k) };
}
/** The next gap after k whose change is a swap (k itself when there is none). */
export function nextSwap(k) {
  for (let j = k + 1; j < GAPS.length; j++) if (isSwap(EVENTS[j - 1])) return j;
  return k;
}
