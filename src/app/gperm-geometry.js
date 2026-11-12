// Generalized Permutohedra (Postnikov 2009): the deformation cone of the 3D permutohedron, n = 4. Pure maths, no three.js.
// DICTO · dictospheres.com
//
// A shape of the family has one face height z_S for each nonempty proper subset S of {1, 2, 3, 4} (14 faces), and is
//   P(z) = { x in R^4 : x1 + x2 + x3 + x4 = z_[4],  sum over i in S of x_i >= z_S for every S },
// drawn in its own 3D hyperplane. Subsets are bitmasks: bit i (value 1 << i) is the number i + 1; [4] is FULL = 15.
// Postnikov's y-coordinates: P = sum over I of y_I * Δ_I (Δ_I the simplex on the unit vectors e_i, i in I), and then
// z_S = sum of y_I over I ⊆ S (Postnikov 2009, Prop. 6.3); a negative y_I gives a signed Minkowski sum.
// Membership: z_S + z_T <= z_{S∪T} + z_{S∩T} for all S, T (z_∅ = 0). Written for the support function
// h(S) = max over P of x_S = z_[4] − z_{[4]∖S} this is the submodular inequality h(S) + h(T) >= h(S∪T) + h(S∩T), the form of
// Ardila, Castillo, Eur and Postnikov (2020); `inFamily` tests exactly that.
// The wall forms: for a pair {a, b} and a set A avoiding it, λ_{A,ab}(z) = z_{A∪ab} + z_A − z_{A∪a} − z_{A∪b} is the length
// (in units of |e_a − e_b|) of every edge of P in direction e_a − e_b between the chambers that put A first and then a, b. All 24 are
// >= 0 exactly on the family; an edge vanishes, and with it faces, where one of them reaches 0. Along a straight line they are linear,
// so the line's walls are exact.

export const FULL = 15;
export const N = 4;
/** The 14 nonempty proper subsets, by size then value (the faces). */
export const SUBSETS = Array.from({ length: 14 }, (_, i) => i + 1).sort((a, b) => popcount(a) - popcount(b) || a - b);
export function popcount(m) { let c = 0; for (; m; m &= m - 1) c++; return c; }
/** A subset as its numbers, {1,3}. */
export const setLabel = (m) => `{${[0, 1, 2, 3].filter((i) => m & (1 << i)).map((i) => i + 1).join(',')}}`;
const bits = (...ns) => ns.reduce((m, n) => m | (1 << (n - 1)), 0);

/** z from Postnikov's y (an object mask → y_I; masks 1..15). z[0] = 0, z[FULL] = the sum of all y. */
export function zFromY(y) {
  const z = new Array(16).fill(0);
  for (let S = 1; S <= FULL; S++) for (const [I, v] of Object.entries(y)) if (v && (Number(I) & ~S) === 0) z[S] += v;
  return z;
}
/** The support function h(S) = max over P of x_S = z_[4] − z_{[4]∖S}; h(∅) = 0. */
export function supportOf(z) { return z.map((_, S) => (S === 0 ? 0 : z[FULL] - z[FULL & ~S])); }
/** Submodularity of h on all pairs S, T (with tolerance eps). */
export function isSubmodular(h, eps = 1e-9) {
  for (let S = 0; S <= FULL; S++) for (let T = 0; T <= FULL; T++) if (h[S] + h[T] < h[S | T] + h[S & T] - eps) return false;
  return true;
}
/** Is z the face heights of a generalized permutohedron? */
export const inFamily = (z, eps) => isSubmodular(supportOf(z), eps);

/** The 24 wall forms {A, a, b} (a < b numbers' bits, A avoiding both) and their value at z. */
export const WALL_FORMS = [];
for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) for (let A = 0; A <= FULL; A++) if (!(A & (1 << a)) && !(A & (1 << b))) WALL_FORMS.push({ A, a: 1 << a, b: 1 << b });
export const wallValue = (z, { A, a, b }) => z[A | a | b] + z[A] - z[A | a] - z[A | b];

// ---- the six named members (DICTO's stops), by Postnikov's y ----
const ys = (list, v = 1) => Object.fromEntries(list.map((m) => [m, v]));
const PAIRS = SUBSETS.filter((m) => popcount(m) === 2);
export const PRESETS = {
  simplex: ys([FULL]),                                                    // Δ_[4]
  cube: ys([bits(1, 2), bits(1, 3), bits(1, 4)]),                         // Δ_12 + Δ_13 + Δ_14
  hypersimplex: { ...ys(SUBSETS.filter((m) => popcount(m) === 3)), [FULL]: -2 },   // Δ(2,4): z_S = max(0, |S| − 2)
  cyclohedron: ys([bits(1, 2), bits(2, 3), bits(3, 4), bits(4, 1), bits(1, 2, 3), bits(2, 3, 4), bits(3, 4, 1), bits(4, 1, 2), FULL]),   // cyclic intervals
  associahedron: ys([bits(1, 2), bits(2, 3), bits(3, 4), bits(1, 2, 3), bits(2, 3, 4), FULL]),                                          // Loday: the intervals [i, j]
  permutohedron: ys(PAIRS),                                               // the six Δ_ij
};
export const PRESET_KEYS = ['simplex', 'cube', 'hypersimplex', 'cyclohedron', 'associahedron', 'permutohedron'];
/** The known face counts [corners, edges, faces] of each member. */
export const KNOWN_F = { simplex: [4, 6, 4], cube: [8, 12, 6], hypersimplex: [6, 12, 8], cyclohedron: [20, 30, 12], associahedron: [14, 21, 9], permutohedron: [24, 36, 14] };

/** The main line: y(t) = (1 − t) · permutohedron + t · associahedron, t in [0, 1]. */
export function lineY(t) {
  const y = {};
  for (const [k, v] of Object.entries(PRESETS.permutohedron)) y[k] = (y[k] ?? 0) + (1 - t) * v;
  for (const [k, v] of Object.entries(PRESETS.associahedron)) y[k] = (y[k] ?? 0) + t * v;
  return y;
}
/** The walls of the line, exactly: the t in (0, 1] where a wall form reaches 0 (each linear in t; integers at the two ends), with the
 *  forms that vanish there. With the permutohedron inside the cone, a wall can only be met where the line leaves the open cone. */
export function lineWalls() {
  const z0 = zFromY(PRESETS.permutohedron), z1 = zFromY(PRESETS.associahedron), at = new Map();
  for (const f of WALL_FORMS) {
    const l0 = wallValue(z0, f), l1 = wallValue(z1, f);
    if (l0 === l1) continue;
    // l(t) = l0 + t (l1 − l0) = 0 at t = l0 / (l0 − l1), a ratio of integers
    const num = l0, den = l0 - l1;
    if (den <= 0 || num <= 0 || num > den) continue;
    const key = `${num / gcd(num, den)}/${den / gcd(num, den)}`;
    if (!at.has(key)) at.set(key, { t: num / den, exact: key, forms: [] });
    at.get(key).forms.push(f);
  }
  return [...at.values()].sort((p, q) => p.t - q.t);
}
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; }

// ---- the staged route (DICTO's choice, 2026-11-12): one face at a time from the permutohedron to the associahedron ----
// The 5 faces whose subsets are not intervals ({1,3}, {1,4}, {2,4}, {1,2,4}, {1,3,4}) slide out, one stage each, from the permutohedron's
// height to the associahedron's while the others hold, all at the same speed (a stage as long as its height change, the deficit D_S:
// 1, 1, 1, 2, 2). Of the 120 orders, 16 stay in the family throughout; {1,2,4} and {1,3,4} can never go first. This one takes the pairs
// first. Membership is convex and every stage straight, so the stage ends being in the family proves the whole route is (unit test).
export const STAGE_ORDER = [bits(1, 3), bits(1, 4), bits(2, 4), bits(1, 2, 4), bits(1, 3, 4)];
const Z_PI = zFromY(PRESETS.permutohedron), Z_LO = zFromY(PRESETS.associahedron);
export const STAGE_DEFICITS = STAGE_ORDER.map((S) => Z_PI[S] - Z_LO[S]);
export const STAGE_TOTAL = STAGE_DEFICITS.reduce((a, b) => a + b, 0);   // 7
/** The walls: after stage k (s = the heights moved so far) the face STAGE_ORDER[k] has vanished. */
export const STAGE_WALLS = STAGE_ORDER.map((S, k) => ({ s: STAGE_DEFICITS.slice(0, k + 1).reduce((a, b) => a + b, 0), face: S }));
/** The heights at s in [0, STAGE_TOTAL]: earlier stages done, the current face part way, later ones still at the permutohedron's. */
export function stagedZ(s) {
  const z = [...Z_PI];
  let left = Math.max(0, Math.min(STAGE_TOTAL, s));
  STAGE_ORDER.forEach((S, k) => { const d = Math.min(left, STAGE_DEFICITS[k]); z[S] -= d; left -= d; });
  return z;
}
/** The stage s lies in (0-based; the last stage at the very end). */
export function stageAt(s) { const k = STAGE_WALLS.findIndex((w) => s < w.s); return k < 0 ? STAGE_ORDER.length - 1 : k; }

// ---- the polytope of z: corners, faces, edges ----
const PERMS = [];
(function perms(p, rest) { if (!rest.length) { PERMS.push(p); return; } rest.forEach((r, i) => perms([...p, r], rest.filter((_, j) => j !== i))); })([], [0, 1, 2, 3]);
/** An orthonormal frame of the hyperplane sum x = 0, so that the permutohedron is the truncated octahedron with its squares on the axes. */
export const FRAME = [[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]].map((r) => r.map((x) => x / 2));
const dot = (u, v) => u.reduce((s, x, i) => s + x * v[i], 0);

/** The polytope of heights z (in the family): its corners (4D, distinct), faces (each { S, loop: corner indices in order }), edges. */
export function polytope(z, eps = 1e-9) {
  // every corner is the greedy point of an ordering w: x_{w1} = z_{w1}, x_{wk} = z_{w1..wk} − z_{w1..w(k−1)} (a supermodular z)
  const X = [], scale = Math.max(1, ...z.map(Math.abs)), tol = scale * eps;
  for (const w of PERMS) {
    const x = [0, 0, 0, 0];
    let prev = 0;
    for (let k = 0; k < N; k++) { const S = w.slice(0, k + 1).reduce((m, i) => m | (1 << i), 0); x[w[k]] = z[S] - (k ? z[prev] : 0); prev = S; }
    if (!X.some((q) => q.every((v, j) => Math.abs(v - x[j]) <= tol))) X.push(x);
  }
  const tight = (S) => X.map((x, i) => [i, x.reduce((s, v, j) => s + (S & (1 << j) ? v : 0), 0)]).filter(([, s]) => Math.abs(s - z[S]) <= tol).map(([i]) => i);
  const P3 = X.map((x) => FRAME.map((f) => dot(f, x)));
  const faces = [];
  for (const S of SUBSETS) {
    const ids = tight(S);
    if (ids.length < 3) continue;
    // a face only when its corners span a plane: the largest triangle has area
    const c = [0, 1, 2].map((k) => ids.reduce((s, i) => s + P3[i][k], 0) / ids.length);
    const nrm = FRAME.map((f) => -dot(f, [0, 1, 2, 3].map((j) => (S & (1 << j) ? 1 : 0))));   // outward: x_S is smallest on the face
    const nl = Math.hypot(...nrm), n = nrm.map((v) => v / nl);
    const u0 = P3[ids[0]].map((v, k) => v - c[k]);
    let u = u0, ul = Math.hypot(...u);
    if (ul < scale * 1e-7) { u = P3[ids[1]].map((v, k) => v - c[k]); ul = Math.hypot(...u); }
    u = u.map((v) => v / ul);
    const v = [n[1] * u[2] - n[2] * u[1], n[2] * u[0] - n[0] * u[2], n[0] * u[1] - n[1] * u[0]];
    const ang = (i) => { const d = P3[i].map((p, k) => p - c[k]); return Math.atan2(dot(d, v), dot(d, u)); };
    const loop = [...ids].sort((p, q) => ang(p) - ang(q));
    let area = 0;
    for (let i = 0; i < loop.length; i++) { const p = P3[loop[i]], q = P3[loop[(i + 1) % loop.length]]; const cr = [p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]]; area += dot(cr, n) / 2; }
    if (Math.abs(area) > scale * scale * 1e-9) faces.push({ S, loop, normal: n });
  }
  const ek = new Set(), edges = [];
  for (const f of faces) for (let i = 0; i < f.loop.length; i++) {
    const a = f.loop[i], b = f.loop[(i + 1) % f.loop.length], k = a < b ? `${a}-${b}` : `${b}-${a}`;
    if (!ek.has(k)) { ek.add(k); edges.push([Math.min(a, b), Math.max(a, b)]); }
  }
  return { X, P3, faces, edges, f: [X.length, edges.length, faces.length] };
}

/** Venkov–McMullen: a convex polytope tiles space by translates iff it is centrally symmetric, its faces are centrally symmetric, and
 *  every belt (the faces holding a translate of one edge, in 3D) has 4 or 6 faces. Returns { fills, symmetric, facesSymmetric, belts }. */
export function fillsSpace(poly, eps = 1e-7) {
  const { P3, faces, edges } = poly;
  const R = Math.max(...P3.map((p) => Math.hypot(...p))) || 1, tol = R * eps;
  const near = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1], p[2] - q[2]) <= tol;
  const has = (pts, q) => pts.some((p) => near(p, q));
  const c = [0, 1, 2].map((k) => P3.reduce((s, p) => s + p[k], 0) / P3.length);
  const symmetric = P3.every((p) => has(P3, p.map((v, k) => 2 * c[k] - v)));
  const facesSymmetric = faces.every((f) => { const pts = f.loop.map((i) => P3[i]), fc = [0, 1, 2].map((k) => pts.reduce((s, p) => s + p[k], 0) / pts.length); return pts.every((p) => has(pts, p.map((v, k) => 2 * fc[k] - v))); });
  // belts: for each edge, the faces with an edge that is a translate of it (either way round)
  const vec = ([a, b]) => P3[b].map((v, k) => v - P3[a][k]);
  const faceEdges = faces.map((f) => f.loop.map((a, i) => vec([a, f.loop[(i + 1) % f.loop.length]])));
  const same = (u, w) => near(u, w) || near(u, w.map((x) => -x));
  const belts = edges.map((e) => { const u = vec(e); return faceEdges.filter((fe) => fe.some((w) => same(u, w))).length; });
  const beltsOk = belts.every((n) => n === 4 || n === 6);
  return { fills: symmetric && facesSymmetric && beltsOk, symmetric, facesSymmetric, beltsOk, belts: [...new Set(belts)].sort((a, b) => a - b) };
}

/** Everything the world shows for y (or heights z): { z, inFamily, poly, fill }. */
export function shapeOf(y) { return shapeOfZ(zFromY(y)); }
export function shapeOfZ(z) {
  const ok = inFamily(z), poly = polytope(z);
  return { z, inFamily: ok, poly, fill: fillsSpace(poly) };
}
