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

// ---- Slices (W3, DICTO 2026-10-27): the cut of the 600-cell by the 3-space x·d = h, d the source's own d (not a unit vector, so
// heights compare within one direction only, as #63). Heights are exact in Q(√5), [a, b] = a + b√5 with a, b rationals [p, q].
const gcd = (x, y) => { x = Math.abs(x); y = Math.abs(y); while (y) [x, y] = [y, x % y]; return x || 1; };
const R = (p, q = 1) => { if (q < 0) { p = -p; q = -q; } const g = gcd(p, q); return [p / g, q / g]; };
const rAdd = (x, y) => R(x[0] * y[1] + y[0] * x[1], x[1] * y[1]);
const rMul = (x, y) => R(x[0] * y[0], x[1] * y[1]);
const rParse = (s) => { const [p, q = '1'] = String(s).split('/'); return R(Number(p), Number(q)); };
const qAdd = (x, y) => [rAdd(x[0], y[0]), rAdd(x[1], y[1])];
const qMul = (x, y) => [rAdd(rMul(x[0], y[0]), rMul(R(5), rMul(x[1], y[1]))), rAdd(rMul(x[0], y[1]), rMul(x[1], y[0]))];
const qFloat = (x) => x[0][0] / x[0][1] + (x[1][0] / x[1][1]) * Math.sqrt(5);
const qKey = (x) => `${x[0][0]}/${x[0][1]},${x[1][0]}/${x[1][1]}`;
const rStr = ([p, q]) => (q === 1 ? `${p}` : `${p}/${q}`);
/** An exact height written as #63 writes it: '0', '1/4', '√5', '-1/2 + 1/2√5', '1 + 1/2√5'. */
export function q5String([a, b]) {
  if (b[0] === 0) return rStr(a);
  const bs = `${Math.abs(b[0]) === 1 && b[1] === 1 ? '' : rStr([Math.abs(b[0]), b[1]])}√5`;
  if (a[0] === 0) return `${b[0] < 0 ? '-' : ''}${bs}`;
  return `${rStr(a)} ${b[0] > 0 ? '+' : '-'} ${bs}`;
}
const EXACT = SRC.vertices_exact.map((v) => v.map(([a, b]) => [rParse(a), rParse(b)]));
const D_EXACT = DIRECTIONS.map((k) => SRC.directions[k].d_exact.map(([a, b]) => [rParse(a), rParse(b)]));
const HEIGHTS = D_EXACT.map((d) => EXACT.map((v) => v.reduce((s, x, i) => qAdd(s, qMul(x, d[i])), [R(0), R(0)])));
const D_FLOAT = D_EXACT.map((d) => d.map(qFloat));

/** The slice stops of one direction, from the centre (height 0) to the tip: every vertex height and the exact midpoint of every
 *  gap between two neighbouring ones (#63, Lemma: one pattern per gap). [{ h (exact), height (string), value (float), atVertex, tip }] */
export const SLICE_STOPS = DIRECTIONS.map((_, n) => {
  const seen = new Map();
  for (const h of HEIGHTS[n]) seen.set(qKey(h), h);
  const hs = [...seen.values()].sort((x, y) => qFloat(x) - qFloat(y));
  const cuts = [...hs.map((h) => ({ h, atVertex: true })), ...hs.slice(1).map((h, i) => ({ h: qMul(qAdd(hs[i], h), [R(1, 2), R(0)]), atVertex: false }))];
  const top = qFloat(hs[hs.length - 1]);
  return cuts.filter((c) => qFloat(c.h) > -1e-12).sort((x, y) => qFloat(x.h) - qFloat(y.h))
    .map((c) => ({ ...c, height: q5String(c.h), value: qFloat(c.h), tip: Math.abs(qFloat(c.h) - top) < 1e-12 }));
});

/** The slice of direction n at its stop k, in the direction's own 3D frame: { stop, points, dim, and (dim 3) the hull as hull() }.
 *  The points: the vertices at that height and the crossing points of the edges that pass through it. */
const sliceCache = new Map();
export function sliceAt(dir, k) {
  const n = indexOf(dir), key = `${n}.${k}`;
  if (sliceCache.has(key)) return sliceCache.get(key);
  const stop = SLICE_STOPS[n][k], hk = qKey(stop.h), hv = stop.value, H = HEIGHTS[n], d = D_FLOAT[n], frame = FRAMES[n];
  const pts4 = VERTICES.filter((_, i) => qKey(H[i]) === hk);
  for (const [a, b] of EDGES) {
    const ha = qFloat(H[a]), hb = qFloat(H[b]);
    if ((ha - hv) * (hb - hv) < 0 && qKey(H[a]) !== hk && qKey(H[b]) !== hk) {
      const t = (hv - ha) / (hb - ha);
      pts4.push(VERTICES[a].map((x, i) => x + t * (VERTICES[b][i] - x)));
    }
  }
  const points = pts4.map((p) => frame.map((f) => dot(p, f)));
  // the dimension of the points (a tip: a point, an edge or a triangle)
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

// ---- Cleo shells (W4b, DICTO 2026-10-27): the 600 cells round the vertex v = (2, 0, 0, 0) in 15 shells by the height of their
// centre along v (units where v is at +2), from the 20 cells at v (the Cleo core) to the 20 at the opposite vertex; seen in perspective
// from an eye just beyond the opposite vertex, at height −21/10 (study 2026-10-27-white-queen-600, cleo_shells.py).
export const CLEO_EYE = -21 / 10;
/** The 120 vertices in that perspective, in vertex-first's own frame: the apex v at the centre. */
export const CLEO_POINTS = VERTICES.map((x) => FRAMES[0].map((f) => dot(x, f) / (x[0] - CLEO_EYE)));
/** The shells, from the core outwards: { cells (indices into CELLS), height (float, of the cell centres along v) }. */
export const CLEO_SHELLS = (() => {
  const by = new Map();
  CELLS.forEach((c, i) => { const h = c.reduce((s, k) => s + VERTICES[k][0], 0) / 4, key = Math.round(h * 1e9); if (!by.has(key)) by.set(key, { height: h, cells: [] }); by.get(key).cells.push(i); });
  return [...by.values()].sort((a, b) => b.height - a.height);
})();

// ---- Halves (W5, DICTO 2026-10-27; front_cells_exact.py): in a shadow along u, a cell is in front if its centre·u > 0, behind if < 0,
// side-on (flattened in the shadow) if = 0. In the four main views the front cells tile the shadow exactly once, and so do the back ones.
const CENTRES = CELLS.map((c) => [0, 1, 2, 3].map((a) => c.reduce((s, k) => s + VERTICES[k][a], 0) / 4));
/** { front, back, side } cell indices for the view direction u (side-on within 1e-9). */
export function halves(u) {
  const out = { front: [], back: [], side: [] };
  CENTRES.forEach((c, i) => { const x = dot(c, u); out[x > 1e-9 ? 'front' : x < -1e-9 ? 'back' : 'side'].push(i); });
  return out;
}

// ---- Four-sided faces by kind (W7, DICTO 2026-10-27; as #63 and study check63_exact.py, in the same order): square, rectangle,
// isosceles trapezium, kite, else general (parallelograms, other trapezia, rhombi and the rest). Lengths compared to 1e-9.
const near = (a, b) => Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b));
const sq3 = (a) => dot3(a, a);
const parallel3 = (a, b) => Math.hypot(...cross(a, b)) <= 1e-9 * Math.max(1, Math.hypot(...a) * Math.hypot(...b));
export const QUAD_KINDS = ['square', 'rectangle', 'trapezium', 'kite', 'general'];
/** The kind of the four-sided face with corners a, b, c, d in order round it. */
export function quadKind([a, b, c, d]) {
  const s = [sq3(sub(b, a)), sq3(sub(c, b)), sq3(sub(d, c)), sq3(sub(a, d))];
  const eqd = near(sq3(sub(c, a)), sq3(sub(d, b)));
  const par1 = parallel3(sub(b, a), sub(c, d)), par2 = parallel3(sub(c, b), sub(d, a));
  const all = near(s[0], s[1]) && near(s[1], s[2]) && near(s[2], s[3]), opp = near(s[0], s[2]) && near(s[1], s[3]);
  if (all && eqd) return 'square';
  if (opp && eqd) return 'rectangle';
  if ((par1 || par2) && eqd && !(par1 && par2)) return 'trapezium';
  if (par1 || par2 || all) return 'general';   // parallelograms, other trapezia, rhombi
  if ((near(s[0], s[1]) && near(s[2], s[3])) || (near(s[1], s[2]) && near(s[3], s[0]))) return 'kite';
  return 'general';
}
/** The four-sided faces of a slice (sliceAt) counted by kind. */
export function quadKinds(s) {
  const out = Object.fromEntries(QUAD_KINDS.map((k) => [k, 0]));
  if (s.dim === 3) for (const f of s.faces) if (f.length === 4) out[quadKind(f.map((k) => s.points[k]))]++;
  return out;
}

// ---- Line up (W7): each direction's main symmetry axis inside its slicing 3-space, in the direction's own frame (unit 3D vectors).
//   vertex-first: a 5-fold axis, towards a neighbour of the vertex (the vertex figure is an icosahedron);
//   edge-first:   the edge itself, the 5-fold axis of the ring of five cells round it;
//   face-first:   the 3-fold axis, normal to the triangle within the 3-space;
//   cell-first:   a 3-fold axis through the cell, from its centre towards one of its corners.
export const SLICE_AXES = DIRECTIONS.map((k, n) => {
  const el = SRC.directions[k].element, d = UNIT_DIRECTIONS[n], V0 = VERTICES[el[0]];
  const inSpace = (a) => { const c = dot(a, d); return a.map((x, i) => x - c * d[i]); };
  let a;
  if (k === 'vertex-first') a = inSpace(VERTICES[EDGES.find(([i, j]) => i === el[0] || j === el[0]).find((x) => x !== el[0])]);
  else if (k === 'edge-first') a = inSpace(VERTICES[el[1]].map((x, i) => x - V0[i]));
  else if (k === 'cell-first') a = inSpace(V0);
  else {
    // the unit vector orthogonal to d and to the triangle's two edges (Gram–Schmidt from the coordinate axes)
    const basis = [d, unit(inSpace(VERTICES[el[1]].map((x, i) => x - V0[i])))];
    const e2 = VERTICES[el[2]].map((x, i) => x - V0[i]);
    basis.push(unit(basis.reduce((v, b) => { const c = dot(v, b); return v.map((x, i) => x - c * b[i]); }, e2)));
    a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]].map((e) => basis.reduce((v, b) => { const c = dot(v, b); return v.map((x, i) => x - c * b[i]); }, e)).sort((x, y) => Math.hypot(...y) - Math.hypot(...x))[0];
  }
  const v = FRAMES[n].map((f) => dot(a, f)), l = Math.hypot(...v);
  return v.map((x) => x / l);
});
