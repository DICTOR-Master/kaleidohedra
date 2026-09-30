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

// The path slider's stops (rejig freely: one table).
export const PATH_STOPS = [
  { at: 0, name: 'FCC' },
  { at: 1, name: 'halfway' },
  { at: 2, name: 'DICTO FCC' },
];

/** Parameters on the path: a straight line from FCC (0) to DICTO FCC (2) and on. */
export function paramsOnPath(s) {
  const t = s / 2;
  return Object.fromEntries(KEYS.map((k) => [k, FCC_PARAMS[k] + t * (DICTO_PARAMS[k] - FCC_PARAMS[k])]));
}

/** The path's usable range: as far each way as the cells stay real. */
export const PATH_RANGE = (() => {
  let hi = 0, lo = 0;
  while (hi < 20 && paramsValid(paramsOnPath(hi + 0.01))) hi += 0.01;
  while (lo > -20 && paramsValid(paramsOnPath(lo - 0.01))) lo -= 0.01;
  return [Math.ceil(lo * 10) / 10, Math.floor(hi * 10) / 10];
})();

export { det as det3, mul as mul3 };
