// Kaleidoverse by DICTO: the lattice-shear maths, with no three.js
// dependency (plain arrays), so the verify script can run it in Node.
//
// Six lattice parameters -- lengths a, b, c relative to FCC's, and the
// angles alpha, beta, gamma between FCC's three primitive cell vectors
// (60 degrees for plain FCC) -- define a basis; the shear is the linear
// map taking FCC's basis to it, with its rotation removed, so the scene
// shears and stretches but never spins.
import { dictoMatrix } from './dicto-fcc.js';

export const FCC_BASIS = [[1, 1, 0], [1, 0, 1], [0, 1, 1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const len = (a) => Math.sqrt(dot(a, a));
const angle = (a, b) => (Math.acos(Math.max(-1, Math.min(1, dot(a, b) / (len(a) * len(b))))) * 180) / Math.PI;
const rad = (d) => (d * Math.PI) / 180;

// 3x3 matrices as arrays of rows.
const mul = (A, B) => A.map((r) => [0, 1, 2].map((j) => r[0] * B[0][j] + r[1] * B[1][j] + r[2] * B[2][j]));
const transpose = (A) => [0, 1, 2].map((i) => [0, 1, 2].map((j) => A[j][i]));
const det = (A) => A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
function inverse(A) {
  const d = det(A);
  const c = (r1, c1, r2, c2) => A[r1][c1] * A[r2][c2] - A[r1][c2] * A[r2][c1];
  return [
    [c(1, 1, 2, 2), -c(0, 1, 2, 2), c(0, 1, 1, 2)],
    [-c(1, 0, 2, 2), c(0, 0, 2, 2), -c(0, 0, 1, 2)],
    [c(1, 0, 2, 1), -c(0, 0, 2, 1), c(0, 0, 1, 1)],
  ].map((r) => r.map((x) => x / d));
}
const columns = (vs) => [0, 1, 2].map((i) => vs.map((v) => v[i])); // matrix whose columns are vs

export const KEYS = ['a', 'b', 'c', 'alpha', 'beta', 'gamma'];
export const FCC_PARAMS = { a: 1, b: 1, c: 1, alpha: 60, beta: 60, gamma: 60 };

/** Six parameters of a basis: lengths relative to FCC's (sqrt 2), angles between vectors 2-3, 1-3 and 1-2. */
export function paramsOf([u, v, w]) {
  return { a: len(u) / Math.SQRT2, b: len(v) / Math.SQRT2, c: len(w) / Math.SQRT2, alpha: angle(v, w), beta: angle(u, w), gamma: angle(u, v) };
}

/** Whether six parameters describe a real cell (positive volume). */
export function paramsValid(p) {
  const [al, be, ga] = [rad(p.alpha), rad(p.beta), rad(p.gamma)];
  const vol2 = 1 - Math.cos(al) ** 2 - Math.cos(be) ** 2 - Math.cos(ga) ** 2 + 2 * Math.cos(al) * Math.cos(be) * Math.cos(ga);
  return p.a > 0.05 && p.b > 0.05 && p.c > 0.05 && vol2 > 1e-4;
}

/** A basis with these parameters (a along x, b in the xy-plane: the crystallographers' convention). */
export function basisOf(p) {
  const [al, be, ga] = [rad(p.alpha), rad(p.beta), rad(p.gamma)];
  const A = p.a * Math.SQRT2, B = p.b * Math.SQRT2, C = p.c * Math.SQRT2;
  const cx = C * Math.cos(be);
  const cy = (C * (Math.cos(al) - Math.cos(be) * Math.cos(ga))) / Math.sin(ga);
  return [[A, 0, 0], [B * Math.cos(ga), B * Math.sin(ga), 0], [cx, cy, Math.sqrt(Math.max(0, C * C - cx * cx - cy * cy))]];
}

/**
 * The shear for six parameters, as rows: the map taking FCC's basis to
 * basisOf(p), with its rotation removed by polar decomposition (A = R S,
 * returning S), so the result is the same whatever way basisOf faces.
 */
export function shearMatrix(p) {
  const A = mul(columns(basisOf(p)), inverse(columns(FCC_BASIS)));
  let R = A;
  for (let i = 0; i < 40; i++) {
    const inv = transpose(inverse(R));
    R = R.map((r, i2) => r.map((x, j) => (x + inv[i2][j]) / 2));
  }
  return mul(transpose(R), A);
}

/** DICTO FCC's parameters: DICTO's shear applied to FCC's basis. */
export const DICTO_PARAMS = (() => {
  const M = dictoMatrix(1); // columns
  const apply = (v) => [0, 1, 2].map((i) => M[0][i] * v[0] + M[1][i] * v[1] + M[2][i] * v[2]);
  return paramsOf(FCC_BASIS.map(apply));
})();

// "Towards": each target is a straight path from plain FCC parameters (0)
// through a halfway stop (1) to the target (2) and on. DICTO FCC is
// DICTO's lattice; Bain is the classic BCC -> FCC stretch: BCC stretched
// by sqrt2 along z is FCC, so the BCC disphenoids whose long edges lie
// across z become regular tetrahedra (the other four become quarters of
// regular octahedra).
export const BAIN_PARAMS = paramsOf(FCC_BASIS.map(([x, y, z]) => [x, y, z * Math.SQRT2]));
export const TOWARDS = {
  dicto: { name: 'DICTO FCC', params: DICTO_PARAMS, stops: ['FCC', 'halfway', 'DICTO FCC'] },
  bain: { name: 'Bain (BCC → FCC)', params: BAIN_PARAMS, stops: ['start', 'halfway', 'Bain'] },
};

/** The path's stops for a target (rejig freely: one table). */
export const pathStops = (towards = 'dicto') => TOWARDS[towards].stops.map((name, at) => ({ at, name }));
export const PATH_STOPS = pathStops('dicto');

/** Parameters on the path: a straight line from FCC (0) to the target (2) and on. */
export function paramsOnPath(s, towards = 'dicto') {
  const t = s / 2, target = TOWARDS[towards].params;
  return Object.fromEntries(KEYS.map((k) => [k, FCC_PARAMS[k] + t * (target[k] - FCC_PARAMS[k])]));
}

/** A path's usable range: as far each way as the cells stay real. */
export function pathRange(towards = 'dicto') {
  let hi = 0, lo = 0;
  while (hi < 20 && paramsValid(paramsOnPath(hi + 0.01, towards))) hi += 0.01;
  while (lo > -20 && paramsValid(paramsOnPath(lo - 0.01, towards))) lo -= 0.01;
  return [Math.ceil(lo * 10) / 10, Math.floor(hi * 10) / 10];
}
export const PATH_RANGE = pathRange('dicto');

// ---- BCC disphenoids ---------------------------------------------------
// The six orientations of the BCC Delaunay disphenoid (interstitial-
// lattice.js's cells, at half scale): two opposite edges along cube axes
// a and b, separated along the third axis.
export const BCC_DISPHENOIDS = (() => {
  const out = [];
  for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) if (a !== b) {
    const c = 3 - a - b;
    const e = (i, x) => { const v = [0, 0, 0]; v[i] = x; return v; };
    const q = (sb) => [0, 1, 2].map((i) => e(a, 0.5)[i] + e(b, sb)[i] + e(c, 0.5)[i]);
    out.push([[0, 0, 0], e(a, 1), q(0.5), q(-0.5)]);
  }
  return out;
})();

/**
 * How regular the sheared disphenoids are: for each orientation, shortest
 * edge / longest edge (1 = regular tetrahedron; plain BCC is 0.866).
 * Returns the best ratio and how many of the six are regular.
 */
export function disphenoidQuality(p) {
  const S = shearMatrix(p);
  const ratios = BCC_DISPHENOIDS.map((T) => {
    const w = T.map((v) => S.map((r) => dot(r, v)));
    const L = [];
    for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) L.push(len(w[i].map((x, k) => x - w[j][k])));
    return Math.min(...L) / Math.max(...L);
  });
  return { best: Math.max(...ratios), regular: ratios.filter((r) => r > 1 - 1e-6).length, ratios };
}

export { det as det3, mul as mul3 };

// ---- The cell (the Cell slider) ------------------------------------------
// The rhombic-dodecahedron-type cells that tile a sheared FCC lattice are
// exactly: the sheared RD's four edge directions, each shifted by one common
// vector w (any w keeps all 12 neighbour translations). Exactly one w makes
// all four edges equal: the circumcentre of the four negated directions.
// That equal-edge cell is the regular RD for plain FCC, and DICTO's skewed
// RD at the DICTO lattice (verify-kaleido.mjs checks both).

/** The regular RD's four edge directions (rdRawVerts(1)): the cube's body diagonals / 2, summing to zero. */
export const RD_DIRECTIONS = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]].map((v) => v.map((x) => x / 2));

const applyRows = (S, v) => S.map((r) => r[0] * v[0] + r[1] * v[1] + r[2] * v[2]);

/** The point equidistant from four points (circumcentre of the tetrahedron). */
function circumcentre(P) {
  const A = [1, 2, 3].map((i) => P[i].map((x, q) => 2 * (x - P[0][q])));
  const b = [1, 2, 3].map((i) => dot(P[i], P[i]) - dot(P[0], P[0]));
  const D = det(A);
  return [0, 1, 2].map((k) => det(A.map((r, i) => r.map((x, j) => (j === k ? b[i] : x)))) / D);
}

/**
 * The cell's four edge directions in world space, for lattice parameters p
 * and Cell slider t (0 = the RD sheared, 1 = the lattice's equal-edge cell).
 */
export function cellDirections(p, t) {
  const S = shearMatrix(p);
  const sheared = RD_DIRECTIONS.map((h) => applyRows(S, h));
  const w = circumcentre(sheared.map((g) => g.map((x) => -x)));
  return sheared.map((g) => g.map((x, q) => x + t * w[q]));
}

/** The same directions in the lattice's own (pre-shear) frame, for geometry drawn inside the sheared group. */
export function cellDirectionsPreShear(p, t) {
  const Sinv = inverse(shearMatrix(p));
  return cellDirections(p, t).map((g) => applyRows(Sinv, g));
}

/** The cell's 14 corners from its four edge directions, centred on the origin. */
export function cellCorners(dirs) {
  const pts = [];
  for (let m = 0; m < 16; m++) pts.push(dirs.reduce((acc, g, k) => acc.map((x, q) => x + ((m >> k) & 1 ? 0.5 : -0.5) * g[q]), [0, 0, 0]));
  // The 2 of 16 sums that lie inside are dropped by the renderer's convex hull; keep all 16 here.
  return pts;
}

const SPECIAL_ANGLES = [36, 45, 60, 70.5288, 72, 90];

/**
 * How recognisable a cell is: its line angles, the nearest special angle to
 * each, whether three directions lie in a plane (hexagon faces), and a score
 * from 0 to 1 (1 = every angle exactly special).
 */
export function cellQuality(dirs) {
  const angles = [];
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) {
    const c = Math.abs(dot(dirs[i], dirs[j])) / (len(dirs[i]) * len(dirs[j]));
    angles.push((Math.acos(Math.min(1, c)) * 180) / Math.PI);
  }
  const off = angles.map((a) => Math.min(...SPECIAL_ANGLES.map((s) => Math.abs(a - s))));
  const triples = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]].map(([i, j, k]) => Math.abs(det([dirs[i], dirs[j], dirs[k]])) / (len(dirs[i]) * len(dirs[j]) * len(dirs[k])));
  const score = off.reduce((s, d) => s + Math.exp(-(d * d) / 2), 0) / off.length;
  return { angles, off, flatness: Math.min(...triples), score };
}

/**
 * Events along the path, for Cell slider t: slider values where a line angle
 * crosses a special value, or three directions become coplanar (hexagons),
 * each refined by bisection. Sorted by position.
 */
export function pathEvents(t, range = PATH_RANGE, step = 0.01, towards = 'dicto') {
  const events = [];
  const anglesAt = (s) => cellQuality(cellDirections(paramsOnPath(s, towards), t)).angles;
  const flatAt = (s) => { const d = cellDirections(paramsOnPath(s, towards), t); return [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]].map(([i, j, k]) => det([d[i], d[j], d[k]])); };
  const bisect = (f, a, b) => { let fa = f(a); for (let i = 0; i < 50; i++) { const m = (a + b) / 2, fm = f(m); if (Math.sign(fm) === Math.sign(fa)) { a = m; fa = fm; } else b = m; } return (a + b) / 2; };
  for (let s = range[0]; s < range[1] - 1e-9; s += step) {
    const s2 = Math.min(range[1], s + step);
    const [a0, a1] = [anglesAt(s), anglesAt(s2)];
    for (let k = 0; k < 6; k++) for (const sp of SPECIAL_ANGLES) {
      if ((a0[k] - sp) * (a1[k] - sp) < 0) {
        const at = bisect((x) => anglesAt(x)[k] - sp, s, s2);
        events.push({ at, kind: sp === 90 ? 'square face' : `${sp === 70.5288 ? '70.5' : sp}° rhombus`, angle: sp });
      }
    }
    const [f0, f1] = [flatAt(s), flatAt(s2)];
    for (let k = 0; k < 4; k++) if (f0[k] * f1[k] < 0) events.push({ at: bisect((x) => flatAt(x)[k], s, s2), kind: 'hexagons (three directions in a plane)' });
  }
  return events.sort((x, y) => x.at - y.at);
}

/**
 * "Find next" targets along the path, for Cell slider t: the points where
 * the cell's quality peaks (several angles special at once, score at least
 * minScore, located by golden-section search) and the hexagon events
 * (three directions in a plane). Sorted by position.
 */
export function pathTargets(t, minScore = 0.6, range = PATH_RANGE, step = 0.02, towards = 'dicto') {
  const q = (s) => cellQuality(cellDirections(paramsOnPath(s, towards), t)).score;
  const out = [];
  const xs = [];
  for (let s = range[0]; s <= range[1] + 1e-9; s += step) xs.push(Math.min(s, range[1]));
  const ys = xs.map(q);
  for (let i = 1; i < xs.length - 1; i++) {
    if (!(ys[i] >= ys[i - 1] && ys[i] >= ys[i + 1])) continue;
    let a = xs[i - 1], b = xs[i + 1];
    const g = (Math.sqrt(5) - 1) / 2;
    for (let k = 0; k < 60; k++) {
      const c = b - g * (b - a), d = a + g * (b - a);
      if (q(c) > q(d)) b = d; else a = c;
    }
    const at = (a + b) / 2, score = q(at);
    if (score >= minScore && !out.some((o) => Math.abs(o.at - at) < 1e-4)) out.push({ at, kind: 'regular cell', score });
  }
  // Drop shoulders: a peak within 0.15 of a better one is part of that one.
  for (let i = out.length - 1; i >= 0; i--) if (out.some((o) => o !== out[i] && Math.abs(o.at - out[i].at) < 0.15 && o.score > out[i].score)) out.splice(i, 1);
  for (const e of pathEvents(t, range, 0.01, towards)) if (e.kind.startsWith('hexagons') && !out.some((o) => Math.abs(o.at - e.at) < 1e-4)) out.push({ at: e.at, kind: 'hexagons', score: q(e.at) });
  // Where a disphenoid becomes a regular tetrahedron (e.g. the Bain stop).
  const dq = (s) => disphenoidQuality(paramsOnPath(s, towards)).best;
  for (let i = 1; i < xs.length - 1; i++) {
    const [y0, y1, y2] = [dq(xs[i - 1]), dq(xs[i]), dq(xs[i + 1])];
    if (!(y1 >= y0 && y1 >= y2)) continue;
    let a = xs[i - 1], b = xs[i + 1];
    const g = (Math.sqrt(5) - 1) / 2;
    for (let k = 0; k < 60; k++) { const c = b - g * (b - a), d = a + g * (b - a); if (dq(c) > dq(d)) b = d; else a = c; }
    const at = (a + b) / 2;
    if (!(dq(at) > 1 - 1e-6)) continue;
    const same = out.find((o) => Math.abs(o.at - at) < 1e-4);
    if (same) same.kind = 'regular tetrahedra'; else out.push({ at, kind: 'regular tetrahedra', score: q(at) });
  }
  return out.sort((x, y) => x.at - y.at);
}
