// The White Queen 600-cell (DICTO 2026-10-27, paper #63): the shadows of the 600-cell, computed live from the exact source model
// (white-queen-data.js, nothing else). The 4D view direction u turns along one of six great circles, one for each pair of the four
// main directions (vertex-, edge-, face-, cell-first; the d of the source file): from one unit direction towards the other in the plane
// they span (DICTO 2026-10-27). The 120 vertices are projected along u into the 3D space orthogonal to u, in an orthonormal frame turned
// with u (so the shadow never jumps along a turning). The shadow's outline is the convex hull of the projected vertices, its coplanar
// triangles merged into the real faces. Pure maths, no three.js.
import SRC from './white-queen-data.js';

export const DIRECTIONS = ['vertex-first', 'edge-first', 'face-first', 'cell-first'];
/** a + b√5 from the source's exact [a, b] (each a rational written as 'p' or 'p/q'). */
const rational = (s) => { const [p, q = '1'] = String(s).split('/'); return Number(p) / Number(q); };
export const q5 = ([a, b]) => rational(a) + rational(b) * Math.sqrt(5);

export const VERTICES = SRC.vertices_exact.map((v) => v.map(q5));   // the 120, from the exact coordinates
export const EDGES = SRC.edges, TRIANGLES = SRC.triangles, CELLS = SRC.cells;
export const EDGE_LENGTH = Math.sqrt(5) - 1;                            // the source's edge, √5 − 1 (circumradius 2)

const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const unit = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
/** The four main directions as unit vectors (the source's d: the vertex, edge midpoint, triangle centre and cell centre). */
export const UNIT_DIRECTIONS = DIRECTIONS.map((k) => unit(SRC.directions[k].d_exact.map(q5)));

/** Turn x by angle in the plane of the unit pair (a, w) (a towards w), leaving the plane's orthogonal complement fixed. */
function turn(x, { a, w }, angle) {
  const xa = dot(x, a), xw = dot(x, w), co = Math.cos(angle), si = Math.sin(angle);
  return x.map((c, k) => c + (xa * (co - 1) - xw * si) * a[k] + (xa * si + xw * (co - 1)) * w[k]);
}
/** The great-circle turning from main direction i to main direction j: the plane (a, w) and the angle between them. */
function turning(i, j) {
  const a = UNIT_DIRECTIONS[i], b = UNIT_DIRECTIONS[j], c = dot(a, b);
  return { a, w: unit(b.map((x, k) => x - c * a[k])), angle: Math.acos(Math.max(-1, Math.min(1, c))) };
}
// Each main direction's own frame: vertex-first (u = (1, 0, 0, 0)) shows the other three axes, (0, 1, 0, 0) up; the others carry it
// along the turnings vertex → edge → face → cell, so neighbouring views share their orientation.
const FRAME0 = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];
export const FRAMES = [FRAME0];
for (let i = 0; i < 3; i++) { const st = turning(i, i + 1); FRAMES.push(FRAMES[i].map((f) => turn(f, st, st.angle))); }
const indexOf = (k) => (typeof k === 'number' ? k : DIRECTIONS.indexOf(k));
/** The six turnings, one per pair of main directions (each may be run either way). */
export const PAIRS = DIRECTIONS.flatMap((a, i) => DIRECTIONS.slice(i + 1).map((b) => [a, b]));

/** The view at fraction s (0..1) of the turning from main direction `from` to `to` (keys or indices): { u, frame }. At s = 0 it is the
 *  start's own view; the frame turns with u, so at s = 1 it is the end direction in the frame the turning brings. */
export function viewAt(from, to, s) {
  const i = indexOf(from), j = indexOf(to), x = Math.max(0, Math.min(1, s));
  if (x === 0 || i === j) return { u: UNIT_DIRECTIONS[i], frame: FRAMES[i] };
  const st = turning(i, j), ang = st.angle * x;
  return { u: x === 1 ? UNIT_DIRECTIONS[j] : turn(UNIT_DIRECTIONS[i], st, ang), frame: FRAMES[i].map((f) => turn(f, st, ang)) };
}

/** The 120 vertices projected along u into the frame: 3D points (some coincide). */
export const project = ({ frame }) => VERTICES.map((v) => frame.map((f) => dot(v, f)));

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const EPS = 1e-9;

/** The convex hull of 3D points (incremental): triangles [i, j, k] (indices into P) facing outwards. */
function hullTriangles(P) {
  const n = P.length;
  let a = 0; for (let i = 1; i < n; i++) if (P[i][0] < P[a][0]) a = i;
  let b = a, best = -1; for (let i = 0; i < n; i++) { const d = Math.hypot(...sub(P[i], P[a])); if (d > best) { best = d; b = i; } }
  let c = a; best = -1; for (let i = 0; i < n; i++) { const d = Math.hypot(...cross(sub(P[b], P[a]), sub(P[i], P[a]))); if (d > best) { best = d; c = i; } }
  const n0 = cross(sub(P[b], P[a]), sub(P[c], P[a]));
  let e = a; best = -1; for (let i = 0; i < n; i++) { const d = Math.abs(dot3(n0, sub(P[i], P[a]))); if (d > best) { best = d; e = i; } }
  let faces = [];
  const add = (i, j, k) => { const nn = cross(sub(P[j], P[i]), sub(P[k], P[i])), l = Math.hypot(...nn); const nu = nn.map((x) => x / l); faces.push({ v: [i, j, k], n: nu, d: dot3(nu, P[i]) }); };
  if (dot3(n0, sub(P[e], P[a])) > 0) { add(a, c, b); add(a, b, e); add(b, c, e); add(c, a, e); }
  else { add(a, b, c); add(a, e, b); add(b, e, c); add(c, e, a); }
  const used = new Set([a, b, c, e]);
  for (let p = 0; p < n; p++) {
    if (used.has(p)) continue;
    const vis = faces.filter((f) => dot3(f.n, P[p]) - f.d > EPS);
    if (!vis.length) continue;
    const dir = new Set(); vis.forEach((f) => f.v.forEach((x, i) => dir.add(`${x},${f.v[(i + 1) % 3]}`)));
    const horizon = [];
    vis.forEach((f) => f.v.forEach((x, i) => { const y = f.v[(i + 1) % 3]; if (!dir.has(`${y},${x}`)) horizon.push([x, y]); }));
    const gone = new Set(vis); faces = faces.filter((f) => !gone.has(f));
    for (const [x, y] of horizon) add(x, y, p);
  }
  return faces;
}

/** The shadow's hull with its real faces: { points (distinct projected points), vertices (indices of the hull's corners),
 *  faces (each a loop of corner indices, outward), triangles / quads / others (face counts by sides) }. */
export function hull(P3) {
  const points = [], index = P3.map((p) => {
    let k = points.findIndex((q) => Math.abs(q[0] - p[0]) + Math.abs(q[1] - p[1]) + Math.abs(q[2] - p[2]) < 1e-9);
    if (k < 0) { k = points.length; points.push(p); }
    return k;
  });
  const tris = hullTriangles(points);
  // merge neighbouring triangles in one plane into one face
  const edgeOf = new Map(); tris.forEach((f, ti) => f.v.forEach((x, i) => edgeOf.set(`${x},${f.v[(i + 1) % 3]}`, ti)));
  const group = new Array(tris.length).fill(-1); let g = 0;
  for (let s = 0; s < tris.length; s++) {
    if (group[s] >= 0) continue;
    const stack = [s]; group[s] = g;
    while (stack.length) {
      const f = tris[stack.pop()];
      f.v.forEach((x, i) => {
        const o = edgeOf.get(`${f.v[(i + 1) % 3]},${x}`);
        if (o !== undefined && group[o] < 0 && dot3(tris[o].n, tris[s].n) > 1 - 1e-9 && Math.abs(tris[o].d - tris[s].d) < 1e-7) { group[o] = g; stack.push(o); }
      });
    }
    g++;
  }
  const faces = [];
  for (let k = 0; k < g; k++) {
    const T = tris.filter((_, i) => group[i] === k), dir = new Set();
    T.forEach((f) => f.v.forEach((x, i) => dir.add(`${x},${f.v[(i + 1) % 3]}`)));
    const next = new Map();
    T.forEach((f) => f.v.forEach((x, i) => { const y = f.v[(i + 1) % 3]; if (!dir.has(`${y},${x}`)) next.set(x, y); }));
    const start = next.keys().next().value, loop = [start];
    for (let x = next.get(start); x !== start && loop.length <= next.size; x = next.get(x)) loop.push(x);
    // drop corners where the boundary runs straight on (a point in the middle of an edge)
    const n = T[0].n;
    const corners = loop.filter((x, i) => {
      const p = points[loop[(i + loop.length - 1) % loop.length]], q = points[loop[(i + 1) % loop.length]];
      return Math.abs(dot3(n, cross(sub(points[x], p), sub(q, points[x])))) > 1e-9;
    });
    faces.push(corners);
  }
  const vertices = [...new Set(faces.flat())];
  return { points, index, vertices, faces, triangles: faces.filter((f) => f.length === 3).length, quads: faces.filter((f) => f.length === 4).length, others: faces.filter((f) => f.length > 4).length };
}

/** Everything the world draws at fraction s of the turning from `from` to `to`: the projected vertices and the hull. */
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
