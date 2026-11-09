// Golamandalas's geometry (DICTO 2026-11-08), ported from k-research studies/2026-11-08-tetra-yantra (render3d.py, cleo_sphere.py,
// sphere81.py): the DICTO Yantra (mandala-data.js, GF1) as nine tetrahedra spinning about the vertical axis inside nine nested cones,
// its nine marma circles, the three still positions (the yantra narrowed to cos 30°, all 18 meetings kept), and the yantra by gnomonic
// projection on the sphere: twenty in the inscribed circles of the Cleo-Icos' faces (the spherical icosahedron), eighty on the
// twice-split Cleo sphere. Pure functions, no three.js: app coordinates are y up, the sphere of the yantra's circle has radius 1, and
// the still view looks along −z (study frame (x, y, h) → app (x, h, −y)).
import { YANTRA_B, YANTRA_W, YANTRA_APEX } from './mandala-data.js';

export const N_TRI = 9;
export const B = YANTRA_B, W = YANTRA_W, A = YANTRA_APEX;
/** Triangle i (0-based) points up when its apex is above its base (depth smaller). */
export const isUp = (i) => A[i] < B[i];
/** The great pair (triangles 3 and 7, the Cleo-Antonius). */
export const GREAT = new Set([2, 6]);
const S = 2;                                   // diameter-1 frame → sphere radius 1
const h = (d) => (0.5 - d) * S;                // height from a depth
export const SPIN_MIN = -30, SPIN_MAX = 150;   // the spin slider, degrees
/** The three still positions (degrees): one in each of the three mirror planes. */
export const STILL_STOPS = [0, 60, 120];
/** The opening spin: between two still positions, so the yantra is seen in 3D. */
export const SPIN_START = 30;

/** The flat yantra's 27 segments [[x, depth], [x, depth], i] (diameter-1 frame). */
export function flatSegments() {
  const out = [];
  for (let i = 0; i < N_TRI; i++) {
    const L = [-W[i], B[i]], R = [W[i], B[i]], P = [0, A[i]];
    out.push([L, R, i], [L, P, i], [R, P, i]);
  }
  return out;
}
const r9 = (v) => Math.round(v * 1e9) / 1e9;
function inter([[x1, y1], [x2, y2]], [[x3, y3], [x4, y4]]) {
  const den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
  if (Math.abs(den) < 1e-14) return null;
  const px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den;
  const py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den;
  const on = ([p, q]) => Math.min(p[0], q[0]) - 1e-12 <= px && px <= Math.max(p[0], q[0]) + 1e-12 && Math.min(p[1], q[1]) - 1e-12 <= py && py <= Math.max(p[1], q[1]) + 1e-12;
  return on([[x1, y1], [x2, y2]]) && on([[x3, y3], [x4, y4]]) ? [r9(px), r9(py)] : null;
}
/** The marmas: points (not corners, inside the circle) where three or more segments meet, as [r, depth] with r ≥ 0, mirror pairs
 *  folded (render3d.py). The DICTO Yantra has 9: each spins to a marma circle, where two cones and a disc meet. */
export function marmas() {
  const segs = flatSegments(), cnt = new Map();
  for (let s = 0; s < segs.length; s++) for (let u = s + 1; u < segs.length; u++) {
    const q = inter(segs[s], segs[u]);
    if (!q) continue;
    const k = q.join(',');
    if (!cnt.has(k)) cnt.set(k, { q, segs: new Set() });
    cnt.get(k).segs.add(s).add(u);
  }
  const corners = new Set();
  for (let i = 0; i < N_TRI; i++) for (const [x, y] of [[-W[i], B[i]], [W[i], B[i]], [0, A[i]]]) corners.add(`${r9(x)},${r9(y)}`);
  const out = new Map();
  for (const [k, { q, segs: ss }] of cnt) {
    if (ss.size < 3 || corners.has(k) || q[0] ** 2 + (q[1] - 0.5) ** 2 >= 0.25) continue;
    const f = [Math.abs(q[0]), q[1]];
    out.set(f.join(','), f);
  }
  return [...out.values()].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
}

const rotY = ([x, y, z], t) => [x * Math.cos(t) + z * Math.sin(t), y, -x * Math.sin(t) + z * Math.cos(t)];
/** Tetrahedron i turned by `deg` about the vertical axis: { base: [3 corners], apex }. Base inscribed in the cone's base circle; apex-down
 *  ones turned 60° (as in the stella octangula), as render3d.py. */
export function tetra(i, deg = 0) {
  const off = isUp(i) ? Math.PI / 2 : Math.PI / 2 + Math.PI / 3, t = (deg * Math.PI) / 180;
  const base = [0, 1, 2].map((k) => { const a = off + (k * 2 * Math.PI) / 3; return rotY([W[i] * S * Math.cos(a), h(B[i]), -W[i] * S * Math.sin(a)], t); });
  return { base, apex: [0, h(A[i]), 0] };
}
/** Cone i: apex height, base height, base radius (app units). */
export const cone = (i) => ({ apex: h(A[i]), base: h(B[i]), r: W[i] * S });
/** The nine marma circles: { r, y } (app units). */
export const marmaCircles = () => marmas().map(([r, d]) => ({ r: r * S, y: h(d) }));
/** A still position (deg one of STILL_STOPS, or any multiple of 60°): seen along −z, the yantra narrowed to cos 30° in the plane z = 0:
 *  its segments [[p, q, i]] and its meetings (each marma at ±r cos 30°: 18). */
export function narrowed() {
  const c = Math.sqrt(3) / 2;
  const segs = flatSegments().map(([p, q, i]) => [[p[0] * c * S, h(p[1]), 0], [q[0] * c * S, h(q[1]), 0], i]);
  const meet = marmas().flatMap(([r, d]) => [[-r * c * S, h(d), 0], [r * c * S, h(d), 0]]);
  return { segs, meet };
}
export const stopAt = (deg, tol = 1e-9) => STILL_STOPS.findIndex((s) => Math.abs(s - deg) <= tol);

// ---- the sphere: gnomonic projection from the centre ----
const PHI = (1 + Math.sqrt(5)) / 2;
const norm = (v) => { const l = Math.hypot(...v); return v.map((x) => x / l); };
const add = (...vs) => vs.reduce((a, v) => a.map((x, k) => x + v[k]));
const sc = (v, s) => v.map((x) => x * s);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
/** The icosahedron's 12 corners on the unit sphere and its 20 faces, in the studies' order (itertools.product / combinations). */
export function icosahedron() {
  const V = [];
  for (const c of [[0, 1, PHI], [1, PHI, 0], [PHI, 0, 1]]) {
    const opts = c.map((x) => (x ? [x, -x] : [0]));
    for (const a of opts[0]) for (const b of opts[1]) for (const d of opts[2]) V.push(norm([a, b, d]));
  }
  let E = Infinity;
  for (let i = 0; i < 12; i++) for (let j = i + 1; j < 12; j++) E = Math.min(E, dist(V[i], V[j]));
  const F = [];
  for (let i = 0; i < 12; i++) for (let j = i + 1; j < 12; j++) for (let k = j + 1; k < 12; k++)
    if ([[i, j], [i, k], [j, k]].every(([p, q]) => Math.abs(dist(V[p], V[q]) - E) < 1e-9)) F.push([i, j, k]);
  return { V, F };
}
/** One DICTO Yantra on the sphere: in the cap of angular radius rho round `cen`, its top towards `point`; each of its 27 segments as
 *  a polyline of n + 1 points on the unit sphere (a great-circle arc): [[points, i]]. */
export function sphereYantra(cen, point, rho, n = 24) {
  const up = norm(add(point, sc(cen, -dot(point, cen)))), rt = cross(up, cen), k = Math.tan(rho) / 0.5;
  const P = (x, d) => norm(add(cen, sc(rt, x * k), sc(up, (0.5 - d) * k)));
  return flatSegments().map(([p, q, i]) => [Array.from({ length: n + 1 }, (_, s) => P(p[0] + ((q[0] - p[0]) * s) / n, p[1] + ((q[1] - p[1]) * s) / n)), i]);
}
/** The cap's rim (the yantra's circle on the sphere) as a closed polyline. */
export function capRim(cen, point, rho, n = 90) {
  const up = norm(add(point, sc(cen, -dot(point, cen)))), rt = cross(up, cen), k = Math.tan(rho);
  return Array.from({ length: n + 1 }, (_, s) => { const a = (2 * Math.PI * s) / n; return norm(add(cen, sc(rt, k * Math.cos(a)), sc(up, k * Math.sin(a)))); });
}
/** The Cleo sphere (cleo_sphere.py): twenty yantras, one in the inscribed circle of each face of the spherical icosahedron (the base of
 *  each Cleo-Ico), its top towards the face's first corner; rho the inscribed circle's angular radius (20.9052°; adjacent caps touch). */
export function cleoSphere() {
  const { V, F } = icosahedron();
  const c0 = norm(add(V[F[0][0]], V[F[0][1]], V[F[0][2]]));
  const rho = Math.acos(dot(c0, norm(add(V[F[0][0]], V[F[0][1]]))));
  const caps = F.map((t) => ({ cen: norm(add(V[t[0]], V[t[1]], V[t[2]])), point: V[t[0]], rho }));
  return { V, F, rho, caps };
}
/** The 81 sphere (sphere81.py): each Cleo face split into four by its side midpoints (80 triangles: 20 central, 60 corner), a yantra
 *  in each triangle's inscribed circle, corner ones pointing to their icosahedron corner; with the bindu at the centre, 81. */
export function sphere81() {
  const { V, F } = icosahedron(), tris = [];
  for (const t of F) {
    const [a, b, c] = t.map((k) => V[k]), ab = norm(add(a, b)), bc = norm(add(b, c)), ca = norm(add(c, a));
    tris.push({ v: [a, ab, ca], point: a }, { v: [b, bc, ab], point: b }, { v: [c, ca, bc], point: c }, { v: [ab, bc, ca], point: ab });
  }
  const ang = (p, q) => Math.acos(Math.max(-1, Math.min(1, dot(p, q))));
  for (const tr of tris) {
    const [a, b, c] = tr.v, la = ang(b, c), lb = ang(c, a), lc = ang(a, b);
    tr.cen = norm(add(sc(a, la), sc(b, lb), sc(c, lc)));
    tr.rho = Math.min(...[[a, b], [b, c], [c, a]].map(([p, q]) => Math.asin(Math.abs(dot(tr.cen, norm(cross(p, q)))))));
  }
  const key = (p) => p.map((x) => x.toFixed(9)).join(',');
  const corners = new Set(tris.flatMap((tr) => tr.v.map(key)));
  const edges = new Set(tris.flatMap((tr) => [[0, 1], [1, 2], [2, 0]].map(([i, j]) => [key(tr.v[i]), key(tr.v[j])].sort().join('|'))));
  return { tris, corners: corners.size, edges: edges.size };
}
/** A great-circle arc from p to q as n + 1 points (the 81 sphere's triangle sides). */
export const arc = (p, q, n = 16) => Array.from({ length: n + 1 }, (_, s) => norm(add(sc(p, 1 - s / n), sc(q, s / n))));
/** The study renders' view of the spheres (cleo_sphere.py, sphere81.py): rows of the tilt Rx(0.35) · Ry(0.3). */
export function studyTilt() {
  const cx = Math.cos(0.35), sx = Math.sin(0.35), cy = Math.cos(0.3), sy = Math.sin(0.3);
  const Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]], Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]];
  return Rx.map((r) => [0, 1, 2].map((j) => r[0] * Ry[0][j] + r[1] * Ry[1][j] + r[2] * Ry[2][j]));
}
/** The wizard card's turning preview: the nine tetrahedra at the opening spin (edges). */
export function mandalaPreviewEdges() {
  const out = [];
  for (let i = 0; i < N_TRI; i++) {
    const { base, apex } = tetra(i, SPIN_START);
    base.forEach((p, k) => out.push([p, base[(k + 1) % 3]], [p, apex]));
  }
  return out;
}
