// DICTO Vacuus (DICTO 2026-11-03): a lens on any solid whose centre O (the mean of its corners, as in the census) lies strictly
// inside every face plane. Five ways to see the solid from its centre:
//   pyramids  the solid split into its centre pyramids, one per face, apex O;
//   exploded  the same pyramids drawn apart, each along its face normal;
//   star      each pyramid turned out over its own face: apex the mirror image of O in the face plane (the Star step's doubling
//             rule, star-step-geometry.js tipsOf(…, 'doubling')), the inside left empty;
//   sheets    the Vacuus fins: for every edge, the triangle (O, edge), grouped by congruence (three sides, SSS);
//   struts    the rods from O to every corner, grouped by length.
// Pure maths, no three.js. Points are centred on O.
import { tipsOf } from './star-step-geometry.js';

export const VACUUS_VIEWS = ['pyramids', 'exploded', 'star', 'sheets', 'struts'];

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const norm = (a) => Math.hypot(a[0], a[1], a[2]);

/** Newell normal of a face loop (not normalised; its length is twice the face's area). */
function newell(P, f) {
  const n = [0, 0, 0];
  for (let i = 0; i < f.length; i++) {
    const a = P[f[i]], b = P[f[(i + 1) % f.length]];
    n[0] += (a[1] - b[1]) * (a[2] + b[2]); n[1] += (a[2] - b[2]) * (a[0] + b[0]); n[2] += (a[0] - b[0]) * (a[1] + b[1]);
  }
  return n;
}

/** A solid in lens form, centred on O: { vertices, faces (outward loops), edges, planes: [{ n, c, area }] (n unit, outward; c the
 *  distance of the face plane from O), R (circumradius about O) }; null when the lens does not apply: a curved shape, a face not flat,
 *  the faces not one consistently wound closed surface (so "outward" is not defined), or O not strictly inside every face plane.
 *  Convexity is not required: a star-shaped solid such as the stella octangula qualifies. */
export function vacuusSolidOf(spec) {
  if (!spec || spec.curved || !Array.isArray(spec.vertices) || !Array.isArray(spec.faces) || !spec.faces.length) return null;
  const { vertices, faces } = spec;
  const O = [0, 1, 2].map((k) => vertices.reduce((s, v) => s + v[k], 0) / vertices.length);
  const V = vertices.map((v) => sub(v, O));
  const R = Math.max(...V.map(norm));
  if (!(R > 0)) return null;
  // one closed surface, each edge crossed once each way: then its winding says which side is out
  const dir = new Map();
  for (const f of faces) {
    if (f.length < 3) return null;
    f.forEach((a, i) => { const k = `${a},${f[(i + 1) % f.length]}`; dir.set(k, (dir.get(k) ?? 0) + 1); });
  }
  for (const [k, c] of dir) { const [a, b] = k.split(','); if (c !== 1 || dir.get(`${b},${a}`) !== 1) return null; }
  let vol = 0;
  for (const f of faces) for (let i = 1; i + 1 < f.length; i++) vol += dot(V[f[0]], cross(V[f[i]], V[f[i + 1]])) / 6;
  if (Math.abs(vol) < 1e-12 * R ** 3) return null;
  const flip = vol < 0;
  const F = [], planes = [];
  for (const f0 of faces) {
    const f = flip ? [...f0].reverse() : [...f0];
    const nn = newell(V, f), area = norm(nn) / 2;
    if (area < 1e-12 * R * R) return null;
    const n = scale(nn, 1 / (2 * area)), c = dot(n, V[f[0]]);
    if (f.some((k) => Math.abs(dot(n, V[k]) - c) > 1e-5 * R)) return null;   // a flat face
    if (!(c > 1e-9 * R)) return null;                                          // O strictly inside this face plane
    F.push(f); planes.push({ n, c, area });
  }
  const seen = new Set(), E = [];
  for (const f of F) f.forEach((a, i) => { const b = f[(i + 1) % f.length], k = a < b ? `${a},${b}` : `${b},${a}`; if (!seen.has(k)) { seen.add(k); E.push([a, b]); } });
  return { vertices: V, faces: F, edges: E, planes, R };
}

/** True when the solid is a cube: six four-sided faces, all edges one length, all corners one distance from O (a rhombohedron
 *  in a sphere has square faces). Its Star then closes into the rhombic dodecahedron (#87 Proposition 2: every edge angle 90°). */
export function isCube(solid) {
  if (!solid || solid.faces.length !== 6 || solid.vertices.length !== 8 || solid.faces.some((f) => f.length !== 4)) return false;
  const P = solid.vertices, L = solid.edges.map(([a, b]) => norm(sub(P[a], P[b]))), r = P.map(norm), tol = 1e-6;
  return L.every((l) => Math.abs(l - L[0]) < tol * solid.R) && r.every((x) => Math.abs(x - solid.R) < tol * solid.R);
}

/** The centre pyramids, one per face: { base (the face's corners, outward loop), n (unit outward normal), c (height) }; apex O. */
export const pyramidsOf = (solid) => solid.faces.map((f, i) => ({ base: f.map((k) => solid.vertices[k]), n: solid.planes[i].n, c: solid.planes[i].c }));

/** The star: each pyramid's tip turned out over its face, the mirror image of O in the face plane (2c along n). */
export const starTipsOf = (solid) => tipsOf(solid, 'doubling');

// Group values by a key rounded to a tolerance relative to R; classes sorted by their key, so colours follow the measure.
function classify(items, keyOf, R) {
  const tol = 1e-6 * R, classes = [];
  for (const it of items) {
    const key = keyOf(it);
    let c = classes.find((k) => k.key.length === key.length && k.key.every((x, i) => Math.abs(x - key[i]) <= tol));
    if (!c) { c = { key, count: 0 }; classes.push(c); }
    c.count += 1;
    it.cls = c;
  }
  classes.sort((a, b) => { for (let i = 0; i < a.key.length; i++) if (Math.abs(a.key[i] - b.key[i]) > tol) return a.key[i] - b.key[i]; return 0; });
  classes.forEach((c, i) => { c.index = i; });
  for (const it of items) { it.cls = it.cls.index; }
  return classes;
}

/** The Vacuus fins: for every edge [a, b], the triangle (O, a, b). Congruent (same three sides) fins share a class: { fins: [{ a, b,
 *  cls }], classes: [{ sides: [short, middle, long], count }] }. */
export function finsOf(solid) {
  const P = solid.vertices;
  const fins = solid.edges.map(([i, j]) => ({ a: P[i], b: P[j] }));
  const classes = classify(fins, (f) => [norm(f.a), norm(f.b), norm(sub(f.a, f.b))].sort((x, y) => x - y), solid.R);
  return { fins, classes: classes.map((c) => ({ sides: c.key, count: c.count })) };
}

/** The struts: from O to every corner, grouped by length: { struts: [{ v, len, cls }], classes: [{ len, count }] }. */
export function strutsOf(solid) {
  const struts = solid.vertices.map((v) => ({ v, len: norm(v) }));
  const classes = classify(struts, (s) => [s.len], solid.R);
  return { struts, classes: classes.map((c) => ({ len: c.key[0], count: c.count })) };
}

/** Signed volume of the pyramids together (= the solid's when they tile it without overlap) and of the solid. */
export function volumes(solid) {
  const pyr = solid.planes.reduce((s, { c, area }) => s + (area * c) / 3, 0);
  let v = 0;
  for (const f of solid.faces) for (let i = 1; i + 1 < f.length; i++) v += dot(solid.vertices[f[0]], cross(solid.vertices[f[i]], solid.vertices[f[i + 1]])) / 6;
  return { pyramids: pyr, solid: v };
}
