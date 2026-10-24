// DICTO Shadow Form (DICTO 2026-10-24; DICTO's idea and name): the engine, with no DOM and no three.js, shared by the public demo
// (the Studies entry, world-shadow-form.js) and a later private development page. Forms (solids) sit with their centres on the
// points of a grid in space; the negative space, the DICTO Shadow Form, is everything inside the convex hull of all the forms that no
// form fills: hull(every form's corners) − union(the forms that are not containers). A container is a see-through form whose inside
// counts as space (nests: Euclid's roofs = dodecahedron container − its cube). Stages 2–3 (dissecting the negative into pockets,
// nearest-form cells, plane and grid-cell cuts) build on shadowForm()'s Manifold result and volumeInBox().
//   Grids (integer index q, position spacing · q): cubic, every q; face-centred (octet), q with an even coordinate sum; body-centred,
//     q with all three coordinates the same parity. The spacing is the integer step (half the conventional cube for fcc and bcc).
//   Turning is shared (DICTO 2026-10-24: "rotate one shape but all others move synchronised"): one orientation `turn` turns every form
//     about its own grid point, so the arrangement keeps its relative orientations. turnOf() is the single place a later counter-turn
//     (alternate forms turning the other way) would go. snapTurn(): each Euler angle to the nearer multiple of 15° or 36° (DICTO
//     2026-10-24: 15° gives 90/60/45/30, 36° the pentagonal 36/72).
//   An arrangement is plain JSON: { version: 1, grid, spacing, turn: [x, y, z, w], forms: [{ form, at: [i, j, k], offset?: [x, y, z],
//     scale?, q?: [x, y, z, w], container? }] }; a form's point v goes to spacing · at + turn · (offset + q · (scale · v)).
//   The Boolean is manifold-3d (pinned MANIFOLD_VERSION; the page loads it lazily from the CDN, the unit tests from node_modules).
//   Forms: geometry reused, never re-derived: krp-core's Polyhedraverse registry (Platonic solids, the stella octangula, J11 and
//     DICTO's pieces), the OG from the Golden Bodhi Pyrochlore data, the DICTO OCD Stella from its world's data. EXAMPLES rebuild DICTO's
//     own void finds from their worlds' data (roof-fold.js EKP cell, the Bodhi-pyro cube frame, Platonic-mix D slab, icosa clusters).
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { roofFoldSolids, PHI } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { ICOSA_PARTS, ICOSA_SOLIDS } from '../krp-core/src/geometry-extensions/icosa.js';
import BODHI from './bodhi-pyro-data.js';
import BULL from './bull-horns-data.js';
import { slabPieces, pieceCentre, pieceVolume } from './platonic-mix-geometry.js';

export const MANIFOLD_VERSION = '3.5.4';
export const MANIFOLD_URL = `https://cdn.jsdelivr.net/npm/manifold-3d@${MANIFOLD_VERSION}/manifold.js`;
let manifoldLoading = null;
/** The manifold-3d WASM module, loaded once ({ Manifold, Mesh, ... }); importer lets Node pass its own import of the package. */
export function loadManifold(importer = () => import(/* @vite-ignore */ MANIFOLD_URL)) {
  return (manifoldLoading ??= importer().then(async (m) => { const wasm = await m.default(); wasm.setup(); return wasm; }));
}

// ---- vectors and quaternions ([x, y, z, w]) ----
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.hypot(a[0], a[1], a[2]);
const unit = (a) => mul(a, 1 / norm(a));
const mean = (P) => mul(P.reduce(add, [0, 0, 0]), 1 / P.length);
export const IDENTITY = [0, 0, 0, 1];
export const qmul = (a, b) => [
  a[3] * b[0] + a[0] * b[3] + a[1] * b[2] - a[2] * b[1], a[3] * b[1] - a[0] * b[2] + a[1] * b[3] + a[2] * b[0],
  a[3] * b[2] + a[0] * b[1] - a[1] * b[0] + a[2] * b[3], a[3] * b[3] - a[0] * b[0] - a[1] * b[1] - a[2] * b[2]];
export const qnorm = (q) => { const l = Math.hypot(...q) || 1; return q.map((c) => c / l); };
export const qAxisAngle = (axis, angle) => { const u = unit(axis), s = Math.sin(angle / 2); return [u[0] * s, u[1] * s, u[2] * s, Math.cos(angle / 2)]; };
export function qrot(q, v) {
  const [x, y, z, w] = q, t = mul(cross([x, y, z], v), 2);
  return add(add(v, mul(t, w)), cross([x, y, z], t));
}
/** Quaternion of a proper rotation matrix (rows). */
export function qFromMatrix(m) {
  const tr = m[0][0] + m[1][1] + m[2][2];
  let q;
  if (tr > 0) { const s = 0.5 / Math.sqrt(tr + 1); q = [(m[2][1] - m[1][2]) * s, (m[0][2] - m[2][0]) * s, (m[1][0] - m[0][1]) * s, 0.25 / s]; }
  else if (m[0][0] > m[1][1] && m[0][0] > m[2][2]) { const s = 2 * Math.sqrt(1 + m[0][0] - m[1][1] - m[2][2]); q = [0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s]; }
  else if (m[1][1] > m[2][2]) { const s = 2 * Math.sqrt(1 + m[1][1] - m[0][0] - m[2][2]); q = [(m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s]; }
  else { const s = 2 * Math.sqrt(1 + m[2][2] - m[0][0] - m[1][1]); q = [(m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s, (m[1][0] - m[0][1]) / s]; }
  return qnorm(q);
}
const matrixOf = (q) => [[1, 0, 0], [0, 1, 0], [0, 0, 1]].map((e) => qrot(q, e)).reduce((m, c, j) => { c.forEach((x, i) => { m[i][j] = x; }); return m; }, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]);

// ---- turning: shared, snapped on release ----
/** The orientation form i turns by: the shared turn (the one place a later counter-turn option would change). */
export const turnOf = (arr) => arr.turn ?? IDENTITY;
export const SNAP_STEPS = [15, 36];
const snapAngle = (a) => {
  const d = (a * 180) / Math.PI;
  const best = SNAP_STEPS.map((s) => Math.round(d / s) * s).sort((x, y) => Math.abs(x - d) - Math.abs(y - d))[0];
  return (best * Math.PI) / 180;
};
/** Each Euler angle (XYZ) of q to the nearer multiple of 15° or 36°. */
export function snapTurn(q) {
  const m = matrixOf(qnorm(q));
  const y = Math.asin(Math.max(-1, Math.min(1, m[0][2])));
  let x, z;
  if (Math.abs(m[0][2]) < 0.9999999) { x = Math.atan2(-m[1][2], m[2][2]); z = Math.atan2(-m[0][1], m[0][0]); } else { x = Math.atan2(m[2][1], m[1][1]); z = 0; }
  const [sx, sy, sz] = [x, y, z].map(snapAngle);
  return qnorm(qmul(qmul(qAxisAngle([1, 0, 0], sx), qAxisAngle([0, 1, 0], sy)), qAxisAngle([0, 0, 1], sz)));
}

// ---- grids ----
export const GRIDS = ['cubic', 'fcc', 'bcc'];
const mod2 = (n) => ((n % 2) + 2) % 2;
export const onGrid = (grid, q) => (grid === 'fcc' ? mod2(q[0] + q[1] + q[2]) === 0 : grid === 'bcc' ? new Set(q.map(mod2)).size === 1 : true);
/** The grid's points with every coordinate in [-n, n] (integer indices). */
export function gridIndices(grid, n = 2) {
  const out = [];
  for (let i = -n; i <= n; i++) for (let j = -n; j <= n; j++) for (let k = -n; k <= n; k++) if (onGrid(grid, [i, j, k])) out.push([i, j, k]);
  return out;
}
/** The grid point nearest p (scene units). */
export function snapToGrid(grid, spacing, p) {
  const r = p.map((c) => c / spacing), base = r.map(Math.floor);
  let best = null, bd = Infinity;
  for (let a = -1; a <= 2; a++) for (let b = -1; b <= 2; b++) for (let c = -1; c <= 2; c++) {
    const q = [base[0] + a, base[1] + b, base[2] + c];
    if (!onGrid(grid, q)) continue;
    const d = norm(sub(q, r));
    if (d < bd - 1e-12) { bd = d; best = q; }
  }
  return best;
}
/** Nearest-neighbour distance of a grid at a spacing. */
export const neighbourDistance = (grid, spacing) => spacing * (grid === 'fcc' ? Math.SQRT2 : grid === 'bcc' ? Math.sqrt(3) : 1);

// ---- forms ----
function specForm(id) {
  const s = POLYHEDRA[id];
  return { vertices: s.vertices.map((v) => (Array.isArray(v) ? [...v] : [v.x, v.y, v.z])), faces: s.faces.map((f) => [...(Array.isArray(f) ? f : f.vertices)]) };
}
const dataForm = (d) => ({ vertices: d.v.map((v) => [...v]), faces: d.f.map((f) => [...f]) });
let OCD_STELLA = null; // loaded with the world (ocd-stella-data.js is its world's lazy data); loadFormData()
/** Load the forms whose data loads lazily elsewhere (the DICTO OCD Stella). */
export async function loadFormData(importer = () => import('./ocd-stella-data.js')) {
  if (!OCD_STELLA) OCD_STELLA = (await importer()).default.solids.stella;
}
// Picker order: the Platonic solids, Kepler's stella octangula, then DICTO's pieces. Names are i18n sf.form.<key>.
const FORM_SOURCES = {
  tetrahedron: () => specForm('D4'), cube: () => specForm('CUBE'), octahedron: () => specForm('D8'), dodecahedron: () => specForm('DODECAHEDRON'),
  icosahedron: () => specForm('D20'), stella: () => specForm('STELLA_OCTANGULA'),
  axe: () => specForm('KIT13_ICOSA13_AXE'), cleo: () => specForm('KIT13_ICOSA13_CLEO'), unborn: () => specForm('DICTO_UNBORN'),
  icosaxes: () => specForm('DICTO_ICOSAXES'), unbornAxes: () => specForm('DICTO_UNBORN_AXES'), lotusJewelAxes: () => specForm('DICTO_LOTUS_JEWEL_AXES'),
  dodecaxes: () => specForm('DICTO_DODECAXES'), samson: () => specForm('DICTO_SAMSON'), delilah: () => specForm('DICTO_DELILAH'),
  jewel: () => specForm('DRAGON_JEWEL'), dogstar: () => specForm('DOGSTAR'), og: () => dataForm(BODHI.ocd),
  ocdStella: () => (OCD_STELLA ? dataForm(OCD_STELLA) : null), j11: () => specForm('J11_GYROELONGATED_PENTAGONAL_PYRAMID'),
};
export const FORM_KEYS = Object.keys(FORM_SOURCES);
const formCache = new Map();
const signedVolume = (V, F) => F.reduce((s, f) => { for (let m = 1; m + 1 < f.length; m++) s += dot(V[f[0]], cross(V[f[m]], V[f[m + 1]])); return s; }, 0) / 6;
/** A form's geometry: { vertices, faces (outward polygons), convex, volume }; null while its data isn't loaded. */
export function formGeometry(key) {
  if (formCache.has(key)) return formCache.get(key);
  const g = FORM_SOURCES[key]?.();
  if (!g) return null;
  if (signedVolume(g.vertices, g.faces) < 0) g.faces = g.faces.map((f) => [...f].reverse());
  g.volume = signedVolume(g.vertices, g.faces);
  const V = g.vertices;
  g.convex = g.faces.every((f) => { const n = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]])), l = norm(n); return V.every((v) => dot(n, sub(v, V[f[0]])) <= 1e-6 * l); });
  formCache.set(key, g);
  return g;
}

// ---- arrangements ----
const clean = (x) => Math.round(x * 1e12) / 1e12 + 0; // no -0: arrangements round-trip through JSON
/** A plain-JSON copy, checked (unknown forms dropped). */
export function normaliseArrangement(a) {
  const out = { version: 1, grid: GRIDS.includes(a?.grid) ? a.grid : 'cubic', spacing: Number.isFinite(a?.spacing) && a.spacing > 0 ? a.spacing : 1,
    turn: Array.isArray(a?.turn) && a.turn.length === 4 && a.turn.every(Number.isFinite) ? qnorm(a.turn) : [...IDENTITY], forms: [] };
  for (const f of Array.isArray(a?.forms) ? a.forms : []) {
    if (!FORM_KEYS.includes(f?.form) || !Array.isArray(f.at) || f.at.length !== 3 || !f.at.every(Number.isInteger)) continue;
    const g = { form: f.form, at: [...f.at] };
    if (Array.isArray(f.offset) && f.offset.length === 3 && f.offset.every(Number.isFinite)) g.offset = f.offset.map(clean);
    if (Number.isFinite(f.scale) && f.scale > 0) g.scale = f.scale;
    if (Array.isArray(f.q) && f.q.length === 4 && f.q.every(Number.isFinite)) g.q = qnorm(f.q);
    if (f.container) g.container = true;
    out.forms.push(g);
  }
  return out;
}
/** Where form i's point v lands (scene units). */
export function placer(arr, f) {
  const turn = turnOf(arr), c = mul(f.at, arr.spacing), off = f.offset ?? [0, 0, 0], q = f.q ?? IDENTITY, s = f.scale ?? 1;
  return (v) => add(c, qrot(turn, add(off, qrot(q, mul(v, s)))));
}
/** Each form placed: { form, container, vertices (scene), faces, convex }. Forms whose data isn't loaded are skipped. */
export function placedForms(arr) {
  const out = [];
  arr.forms.forEach((f, index) => {
    const g = formGeometry(f.form);
    if (!g) return;
    const at = placer(arr, f);
    out.push({ index, form: f.form, container: !!f.container, vertices: g.vertices.map(at), faces: g.faces, convex: g.convex });
  });
  return out;
}

// ---- the negative: hull − union of the forms that aren't containers ----
function solidOf(wasm, p) {
  const { Manifold, Mesh } = wasm;
  if (p.convex) return Manifold.hull(p.vertices);
  const tris = [];
  for (const f of p.faces) for (let m = 1; m + 1 < f.length; m++) tris.push(f[0], f[m], f[m + 1]);
  const mesh = new Mesh({ numProp: 3, vertProperties: Float32Array.from(p.vertices.flat()), triVerts: Uint32Array.from(tris) });
  mesh.merge();
  return new Manifold(mesh);
}
/** The DICTO Shadow Form of an arrangement: { negative (a Manifold; the caller deletes it), hullVolume, formsVolume, negativeVolume,
 *  hullPoints }. formsVolume is the union of the non-container forms (overlaps counted once). */
export function shadowForm(arr, wasm) {
  const placed = placedForms(arr);
  const pts = placed.flatMap((p) => p.vertices);
  if (pts.length < 4) return { negative: null, hullVolume: 0, formsVolume: 0, negativeVolume: 0 };
  const { Manifold } = wasm;
  const hull = Manifold.hull(pts);
  const solids = placed.filter((p) => !p.container).map((p) => solidOf(wasm, p));
  const union = solids.length ? Manifold.union(solids) : null;
  const negative = union ? hull.subtract(union) : hull.translate([0, 0, 0]);
  const res = { negative, hullVolume: hull.volume(), formsVolume: union ? union.volume() : 0, negativeVolume: negative.volume() };
  hull.delete(); union?.delete(); solids.forEach((s) => s.delete());
  return res;
}
/** The negative's volume inside the box [min, max] (a check on a whole cell well inside the cluster). */
export function volumeInBox(wasm, negative, min, max) {
  const box = wasm.Manifold.cube(sub(max, min)).translate(min), part = negative.intersect(box), v = part.volume();
  box.delete(); part.delete();
  return v;
}
/** The negative as triangles: { positions: Float32Array (3 per corner), triangles: count }. */
export function meshOf(negative) {
  const m = negative.getMesh(), P = m.vertProperties, n = m.numProp, T = m.triVerts, out = new Float32Array(T.length * 3);
  for (let i = 0; i < T.length; i++) for (let a = 0; a < 3; a++) out[3 * i + a] = P[T[i] * n + a];
  return { positions: out, triangles: T.length / 3 };
}

// ---- placing a form like given corners (EKP cell data) ----
const outerShell = (P) => { const c = mean(P), r = Math.max(...P.map((p) => norm(sub(p, c)))); return { c, r, pts: P.filter((p) => norm(sub(p, c)) > r - 1e-6) }; };
/** The similarity (offset, scale, q) taking a form onto target corners T, or null. Rotations only. With as many corners as the form,
 *  every corner must land on one (centres: the corner means); otherwise its outermost corners on T's (a stella's 8 cube corners). */
export function fitForm(key, T) {
  const g = formGeometry(key), full = g.vertices.length === T.length;
  const frameOf = (P) => { const s = full ? { c: mean(P), pts: P } : outerShell(P); return { ...s, r: Math.max(...s.pts.map((p) => norm(sub(p, s.c)))) }; };
  const A = frameOf(g.vertices), B = frameOf(T), s = B.r / A.r;
  const a = A.pts.map((p) => mul(sub(p, A.c), s)), b = B.pts.map((p) => sub(p, B.c));
  if (a.length !== b.length) return null;
  const i0 = a.findIndex((p) => norm(p) > B.r - 1e-6), i1 = a.findIndex((p) => norm(cross(p, a[i0])) > 1e-6);
  const frame = (u, v) => { const e1 = unit(u), e3 = unit(cross(u, v)), e2 = cross(e3, e1); return [e1, e2, e3]; };
  const Fa = frame(a[i0], a[i1]);
  for (const u of b) for (const w of b) {
    if (Math.abs(norm(u) - norm(a[i0])) > 1e-6 || Math.abs(norm(w) - norm(a[i1])) > 1e-6 || Math.abs(dot(u, w) - dot(a[i0], a[i1])) > 1e-6 || norm(cross(u, w)) < 1e-9) continue;
    const Fb = frame(u, w);
    const R = [0, 1, 2].map((r) => [0, 1, 2].map((c) => Fb[0][r] * Fa[0][c] + Fb[1][r] * Fa[1][c] + Fb[2][r] * Fa[2][c]));
    const Rv = (v) => R.map((row) => dot(row, v));
    if (!a.every((v) => b.some((x) => norm(sub(Rv(v), x)) < 1e-5))) continue;
    const q = qFromMatrix(R);
    return { offset: sub(B.c, qrot(q, mul(A.c, s))), scale: s, q };
  }
  return null;
}

// ---- EXAMPLES: DICTO's own void finds, rebuilt from their worlds' data ----
const EKP = () => roofFoldSolids();
const cornersOf = (faces) => { const out = []; for (const p of faces.flat()) if (!out.some((q) => norm(sub(p, q)) < 1e-9)) out.push(p); return out; };
const scaled = (P, k) => P.map((p) => mul(p, k));
const nested = (parts, k) => parts.map(([form, T, container]) => ({ form, at: [0, 0, 0], ...fitForm(form, scaled(T, k)), ...(container ? { container: true } : {}) }));
const cell = (c, h) => [c.map((x) => x - h), c.map((x) => x + h)];
const DODECA_V = (e) => ((15 + 7 * Math.sqrt(5)) / 4) * e ** 3, ICO_V = (e) => ((5 * (3 + Math.sqrt(5))) / 12) * e ** 3;
// The Bodhi-pyro cube frame M = s·R (det −1): turning the whole world by −Rᵀ (the OG is centrally symmetric) puts the body-centred
// grid on the axes, OGs at s·(i, j, k), all coordinates of one parity, each turned by −Rᵀ.
const BODHI_FRAME = (() => {
  const M = BODHI.cubes[0].M, s = norm(M[0]);
  const R = M.map((r) => r.map((x) => x / s)), det = dot(R[0], cross(R[1], R[2])), sg = det < 0 ? -1 : 1;
  const Rt = [0, 1, 2].map((i) => [0, 1, 2].map((j) => sg * R[j][i]));
  return { s, turn: qFromMatrix(Rt) };
})();
/** key → { paper, build(): arrangement, check?: { min, max, expected, what } (the negative inside a cell well inside the cluster) }. */
export const EXAMPLES = {
  // #42 The DICTO Sunstar: dodecahedra (edge 1) on alternate cubes of edge φ; the hole in the middle cube is one Dogstar, φ/2.
  dogstar: { paper: '#42', build: () => ({ grid: 'fcc', spacing: PHI, forms: gridIndices('fcc', 2).filter((q) => q.every((c) => c >= 0)).map((at) => ({ form: 'dodecahedron', at })) }),
    check: { ...Object.fromEntries(['min', 'max'].map((k, i) => [k, cell([PHI, PHI, PHI], PHI / 2)[i]])), expected: PHI / 2, what: 'one Dogstar' } },
  // #31 / Golden Bodhi Pyrochlore: OGs on the body-centred grid of the Bodhi-pyro frame; the Bull-horns OG adaptor is 22.57% of space.
  bullHorns: { paper: '#31', build: () => ({ grid: 'bcc', spacing: BODHI_FRAME.s, turn: BODHI_FRAME.turn, forms: gridIndices('bcc', 2).filter((q) => norm(q) <= 2 + 1e-9).map((at) => ({ form: 'og', at })) }),
    check: { min: [-BODHI_FRAME.s, -BODHI_FRAME.s, -BODHI_FRAME.s], max: [BODHI_FRAME.s, BODHI_FRAME.s, BODHI_FRAME.s], expected: BULL.adaptorShare * 8 * BODHI_FRAME.s ** 3, what: 'the Bull-horns OG adaptor in one cube of two OGs' } },
  // #48 Golden split: icosahedra (edge 1) on the cubic grid of spacing φ; per cell an Unborn and 6 AXE, (9 + 7√5)/12.
  goldenSplit: { paper: '#48', build: () => ({ grid: 'cubic', spacing: PHI, forms: gridIndices('cubic', 1).map((at) => ({ form: 'icosahedron', at })) }),
    check: { min: [-PHI / 2, -PHI / 2, -PHI / 2], max: [PHI / 2, PHI / 2, PHI / 2], expected: (9 + 7 * Math.sqrt(5)) / 12, what: 'an Unborn + 6 AXE per cell' } },
  // #47 Every Mix: the dodecahedra of the D slab (platonic-mix-geometry.js), the middle layer; the long hexagon's middle cube is its
  // Dogstar S plus the two roofs its boundary pieces Y add (both from that world's own pieces).
  longHexagon: { paper: '#47', build: () => {
    const D = slabPieces('D', ['D']).pieces.filter((p) => p.kind === 'D'), h = PHI / 2;
    return { grid: 'fcc', spacing: PHI, forms: D.map((p) => ({ form: 'dodecahedron', at: sub(pieceCentre(p), [0, 0, h]).map((c) => Math.round(c / PHI)) })) };
  }, check: { min: [-PHI / 2, -PHI / 2, PHI / 2], max: [PHI / 2, PHI / 2, 1.5 * PHI], what: 'the middle cube of the long hexagon: S + 2 roofs (#47 pieces)',
    get expected() { const P = slabPieces('D', ['D']).pieces, v = (k) => pieceVolume(P.find((p) => p.kind === k)); return v('S') + 2 * (v('Y') - PHI ** 3); } } },
  // #19 DESHI: thirteen icosahedra, twelve round one (R. W. Gray's arrangement; DICTO's name), from the icosa cluster data.
  deshi: { paper: '#19', build: () => ({ grid: 'cubic', spacing: 1, forms: ICOSA_PARTS.DESHI.pieces.map((p) => ({ form: 'icosahedron', at: [0, 0, 0], ...fitForm('icosahedron', p.vertices) })) }) },
  // #19 Lotus seed build: DICTO's own build of the Lotus seed, a dodecahedron with a J11 on each pentagon; the rest of the Lotus seed
  // (its hull) is 30 AXE + 20 FUJI.
  lotusBuild: { paper: '#19', build: () => ({ grid: 'cubic', spacing: 1, forms: ICOSA_PARTS.LOTUS_SEED.build.filter((p) => p.role === 'dodeca' || p.role === 'j11')
    .map((p) => ({ form: p.role === 'dodeca' ? 'dodecahedron' : 'j11', at: [0, 0, 0], ...fitForm(p.role === 'dodeca' ? 'dodecahedron' : 'j11', p.vertices) })) }),
  check: { whole: true, expected: 30 * ICOSA_SOLIDS.AXE.volume + 20 * ICOSA_SOLIDS.FUJI.volume, what: '30 AXE + 20 FUJI' } },
  // Kepler's stella octangula alone: its hull is the cube; cube edge 1, the negative is the other half, 1/2.
  stella: { paper: 'Kepler', build: () => ({ grid: 'cubic', spacing: 1, forms: nested([['stella', cornersOf(EKP().stella.faces), false]], 1 / 2) }), check: { whole: true, expected: 1 / 2, what: 'cube − stella' } },
  // #10b The Stella–Jewel Lattice: stellas on the odd cells of the cube checkerboard (cube edge 2, as the EKP cell); the negative is the
  // DICTO Jewels: in two cells (one odd, one even) a Jewel's 12 beside the stella's 4.
  stellaJewel: { paper: '#10b', build: () => {
    const fit = fitForm('stella', cornersOf(EKP().stella.faces));
    return { grid: 'cubic', spacing: 2, forms: gridIndices('cubic', 1).filter((q) => mod2(q[0] + q[1] + q[2]) === 1).map((at) => ({ form: 'stella', at, ...fit })) };
  }, check: { min: [-1, -1, -1], max: [3, 1, 1], expected: 12, what: 'one DICTO Jewel (12) per even–odd pair of cells' } },
  // Nests from the Euclid–Kepler–Pacioli cell (roof-fold.js), the outer form a container (its inside counts as space).
  euclidRoofs: { paper: 'Euclid', build: () => ({ grid: 'cubic', spacing: 1, forms: nested([['dodecahedron', cornersOf(EKP().dodeca.faces), true], ['cube', cornersOf(EKP().cube.faces), false]], PHI / 2) }),
    check: { whole: true, expected: (7 + 3 * Math.sqrt(5)) / 4, what: "Euclid's 6 roofs (dodecahedron edge 1)" } },
  cubeOcta: { paper: '', build: () => ({ grid: 'cubic', spacing: 1, forms: nested([['cube', cornersOf(EKP().cube.faces), true], ['octahedron', cornersOf(EKP().oct.faces), false]], 1 / 2) }),
    check: { whole: true, expected: 5 / 6, what: 'cube − octahedron (cube edge 1)' } },
  cubeTetra: { paper: '', build: () => ({ grid: 'cubic', spacing: 1, forms: nested([['cube', cornersOf(EKP().cube.faces), true], ['tetrahedron', cornersOf(EKP().cube.faces).filter((p) => p[0] * p[1] * p[2] > 0), false]], 1 / 2) }),
    check: { whole: true, expected: 2 / 3, what: 'cube − tetrahedron (cube edge 1)' } },
  octaCube: { paper: '', build: () => ({ grid: 'cubic', spacing: 1, forms: nested([['octahedron', cornersOf(EKP().oct.faces), true], ['cube', EKP().oct.faces.map(mean), false]], Math.SQRT1_2) }),
    check: { whole: true, expected: (7 * Math.SQRT2) / 27, what: 'octahedron − cube on its face centres (octahedron edge 1)' } },
  // #8 the EKP cell: dodecahedron ⊃ cube ⊃ stella ⊃ octahedron (containers) ⊃ Pacioli's icosahedron.
  ekpNest: { paper: '#8', build: () => {
    const S = EKP();
    return { grid: 'cubic', spacing: 1, forms: nested([['dodecahedron', cornersOf(S.dodeca.faces), true], ['cube', cornersOf(S.cube.faces), true], ['stella', cornersOf(S.stella.faces), true],
      ['octahedron', cornersOf(S.oct.faces), true], ['icosahedron', cornersOf(S.ico.faces), false]], 1) };
  }, check: { whole: true, expected: DODECA_V(2 / PHI) - ICO_V(2 / PHI ** 2), what: 'dodecahedron − Pacioli icosahedron (cube edge 2)' } },
};
export const EXAMPLE_KEYS = Object.keys(EXAMPLES);
/** An example's arrangement (plain JSON). */
export const exampleArrangement = (key) => normaliseArrangement({ turn: IDENTITY, ...EXAMPLES[key].build() });
/** The starting arrangement: a cube and an octahedron side by side. */
export const START = () => normaliseArrangement({ grid: 'cubic', spacing: 1, forms: [{ form: 'cube', at: [0, 0, 0] }, { form: 'octahedron', at: [1, 0, 0] }] });
