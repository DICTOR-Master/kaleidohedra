// The Star Cores world (DICTO's Star Cores papers #79–#81 and the Star Cores book): a convex solid's star core treatment as one chain.
// Star: every face's pyramid from the centre O turned outwards as a spike, its tip t × the foot of the face perpendicular (the centre
// rule, t = 2 the mirrored spikes, t = φ the golden ones: star-step-geometry.js's 'doubling' and 'golden' rules). Halo: the convex hull
// of the tips. Core of the turn (research study 2026-10-30-star-cores, star_core.py core_of): the faces grouped into families (number
// of sides, distance from O), the hull of each family's tips, and the core the common part of the family hulls that are solid (a
// family whose tips lie in a plane, or that has fewer than four, is left out). The core, scaled back to the solid's circumradius, is
// the next solid of the chain: for the group B solids of the book the cores settle into period two.
// Pure maths, no three.js.
import { solidOf, starStep, PHI } from './star-step-geometry.js';

export const STAR_CORES_T = { 2: 'doubling', phi: 'golden' };
export const STAR_CORES_PHASES = ['solid', 'star', 'halo', 'core'];
export const TURNS = 5;                 // the chain shown: five turns (Hamlet's and Ophelia's cores settle into period two from turn 2)

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const norm = (a) => Math.hypot(a[0], a[1], a[2]);

const lerp = (a, b, u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
const dedupe = (P, tol) => P.filter((p, i) => P.findIndex((q) => norm(sub(p, q)) < tol) === i);
/** Points of one plane (normal n) in turn round their centre, anticlockwise seen from the side n points to. */
function loopRound(P, n) {
  const c = P.reduce((s, p) => [s[0] + p[0] / P.length, s[1] + p[1] / P.length, s[2] + p[2] / P.length], [0, 0, 0]);
  const u = sub(P[0], c), w = cross(n, u);
  return P.map((p) => [Math.atan2(dot(sub(p, c), w), dot(sub(p, c), u)), p]).sort((a, b) => a[0] - b[0]).map(([, p]) => p);
}
/** The facet planes of the hull of points P, by brute force over triples (a family has at most 120 tips): every plane through three
 *  of them with all of P on one side, oriented with P on its inner side n·x ≤ d, each plane once. Exact in what it keeps, unlike an
 *  incremental hull, which can turn faces of a many-cospherical-point set inside out. */
function facetsOf(P, R) {
  const tol = 1e-9 * R, out = [];
  const known = (n, d) => out.some((q) => Math.abs(q.d - d) < 1e-7 * R && norm(sub(q.n, n)) < 1e-7);
  for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) for (let k = j + 1; k < P.length; k++) {
    let n = cross(sub(P[j], P[i]), sub(P[k], P[i]));
    const l = norm(n);
    if (!(l > 1e-9 * R * R)) continue;
    n = scale(n, 1 / l);
    let d = dot(n, P[i]), above = false, below = false;
    for (const p of P) { const h = dot(n, p) - d; if (h > tol) above = true; else if (h < -tol) below = true; if (above && below) break; }
    if (above && below) continue;
    if (above) { n = scale(n, -1); d = -d; }
    if (!known(n, d)) out.push({ n, d });
  }
  return out;
}
/** Whether points span 3D (not all in one plane), relative to size R. */
function solidSpan(P, R) {
  if (P.length < 4) return false;
  // a well-conditioned plane: the point farthest from the first, then the one making the largest triangle with both
  const a = P[0];
  let b = a, n = null, best = 0;
  for (const p of P) if (norm(sub(p, a)) > norm(sub(b, a))) b = p;
  for (const p of P) { const c = cross(sub(b, a), sub(p, a)); if (norm(c) > best) { best = norm(c); n = c; } }
  if (!(best > 1e-9 * R * R)) return false;
  n = scale(n, 1 / best);
  return P.some((p) => Math.abs(dot(n, sub(p, a))) > 1e-7 * R);   // the dataset's 15 digits leave tips of a flat family ~1e-10 apart
}

/** The faces' families: (number of sides, distance from O), as lists of face indices. */
export function familiesOf(solid) {
  const tol = 1e-7 * solid.R, fam = [];
  solid.planes.forEach(({ c }, i) => {
    const sides = solid.faces[i].length;
    const f = fam.find((x) => x.sides === sides && Math.abs(x.c - c) < tol);
    if (f) f.faces.push(i); else fam.push({ sides, c, faces: [i] });
  });
  return fam;
}

/** The core of the turn at t (2 or φ): { vertices, faces, families (all), used (the solid ones) }, or null when no family hull is
 *  solid or the common part is not a bounded solid round O. */
export function coreOf(solid, t) {
  const fam = familiesOf(solid);
  const tips = solid.planes.map(({ n, c }) => scale(n, t * c));
  const planes = [];
  let used = 0;
  for (const f of fam) {
    const T = f.faces.map((i) => tips[i]);
    if (!solidSpan(T, solid.R)) continue;
    used += 1;
    planes.push(...facetsOf(T, solid.R));
  }
  if (!planes.length) return null;
  if (planes.some(({ d }) => !(d > 1e-9 * solid.R))) return null;   // O must be inside every family hull
  // The common part {x : n·x ≤ d}: a cube far round O clipped by each plane in turn (each face polygon cut, the cut closed by a new
  // face on the plane). A face of the cube left at the end means the part is not bounded by the planes.
  const tol = 1e-9 * solid.R, B = 100 * solid.R;
  const C = [[-B, -B, -B], [B, -B, -B], [B, B, -B], [-B, B, -B], [-B, -B, B], [B, -B, B], [B, B, B], [-B, B, B]];
  let poly = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 4, 7, 3]].map((f) => ({ pts: f.map((k) => C[k]), plane: null }));
  const P = [];
  for (const pl of planes) if (!P.some((q) => norm(sub(q.n, pl.n)) < 1e-7 && Math.abs(q.d - pl.d) < 1e-7 * solid.R)) P.push(pl);
  for (const pl of P) {
    const { n, d } = pl, cut = [], next = [];
    for (const f of poly) {
      const out = [];
      f.pts.forEach((a, i) => {
        const b = f.pts[(i + 1) % f.pts.length], ha = dot(n, a) - d, hb = dot(n, b) - d;
        if (ha <= tol) out.push(a);
        if ((ha < -tol && hb > tol) || (ha > tol && hb < -tol)) { const x = lerp(a, b, ha / (ha - hb)); out.push(x); cut.push(x); }
        else if (Math.abs(hb) <= tol && ha > tol) cut.push(b);
        if (Math.abs(ha) <= tol) cut.push(a);
      });
      if (out.length >= 3) next.push({ pts: out, plane: f.plane });
    }
    if (cut.length >= 3) next.push({ pts: loopRound(dedupe(cut, tol * 10), n), plane: pl });
    poly = next;
    if (!poly.length) return null;
  }
  if (poly.some((f) => !f.plane)) return null;
  // indexed corners, merged; faces with fewer than three distinct corners dropped
  const V = [], at = (p) => { let k = V.findIndex((q) => norm(sub(p, q)) < 1e-7 * solid.R); if (k < 0) { k = V.length; V.push(p); } return k; };
  const faces = [];
  for (const f of poly) {
    const loop = [];
    for (const p of f.pts) { const k = at(p); if (loop.at(-1) !== k && loop[0] !== k) loop.push(k); }
    if (loop.length >= 3) faces.push(loop);
  }
  return { vertices: V, faces, families: fam.length, used };
}

/** The whole chain for a shape spec ({ vertices, faces }) at t ('2' or 'phi'): turns [{ solid, step (star, halo), core }], each
 *  next solid the core scaled back to the first solid's circumradius; it stops at a turn with no core. null if not a convex solid
 *  with its centre inside every face. */
export function starCoresChain(spec, tKey = '2', turns = TURNS) {
  const t = tKey === 'phi' ? PHI : 2, rule = STAR_CORES_T[tKey] ?? 'doubling';
  let solid = solidOf(spec);
  if (!solid) return null;
  const R = solid.R, out = [];
  for (let k = 0; k < turns && solid; k++) {
    const step = starStep(solid, rule);
    const core = coreOf(solid, t);
    out.push({ solid, step, core });
    if (!core) break;
    const r = Math.max(...core.vertices.map(norm));
    solid = solidOf({ vertices: core.vertices.map((v) => scale(v, R / r)), faces: core.faces });
  }
  return { R, t, tKey, turns: out };
}

/** The slider's positions: turn k, phase p (0 solid, 1 star, 2 halo, 3 core), as k·4 + p; the last one the last turn's core, or its
 *  halo when it has none. */
export const positionsOf = (chain) => (chain ? (chain.turns.length - 1) * 4 + (chain.turns.at(-1).core ? 3 : 2) : 0);
export const phaseAt = (pos) => ({ turn: Math.floor(pos / 4), phase: STAR_CORES_PHASES[pos % 4] });

/** Whether two solids are similar to 1e-6 in the sense of the study's shape(): the same corner count, faces by number of sides,
 *  corner radii and edge lengths, both scaled to circumradius 1. */
export function sameShape(a, b) {
  if (!a || !b || a.vertices.length !== b.vertices.length || a.faces.length !== b.faces.length) return false;
  const sig = (s) => {
    const m = Math.max(...s.vertices.map(norm)), V = s.vertices.map((v) => scale(v, 1 / m));
    const sides = s.faces.map((f) => f.length).sort((x, y) => x - y);
    const radii = V.map(norm).sort((x, y) => x - y);
    const seen = new Set(), edges = [];
    for (const f of s.faces) f.forEach((p, i) => { const q = f[(i + 1) % f.length], k = p < q ? `${p},${q}` : `${q},${p}`; if (!seen.has(k)) { seen.add(k); edges.push(norm(sub(V[p], V[q]))); } });
    return { sides, radii, edges: edges.sort((x, y) => x - y) };
  };
  const A = sig(a), B = sig(b), close = (x, y) => x.length === y.length && x.every((v, i) => Math.abs(v - y[i]) < 1e-6);
  return A.sides.every((v, i) => v === B.sides[i]) && close(A.radii, B.radii) && close(A.edges, B.edges);
}

/** A shape of the list by D-number (D109) or key (ophelia, ti_star_core), any case. */
export const findStarCoresShape = (shapes, id) => shapes.find((s) => s.D.toLowerCase() === String(id).toLowerCase() || s.key === String(id).toLowerCase().replaceAll('_', '-'));

/** The star's own corners and faces (the solid with its spikes): the solid's corners and one tip per face; the spikes' triangles,
 *  two neighbouring spikes' triangles over a shared edge counted once where they lie in one plane. */
export function starCounts(solid, tips) {
  const tol = 1e-9 * solid.R, owner = new Map();
  solid.faces.forEach((f, fi) => f.forEach((a, i) => owner.set(`${a},${f[(i + 1) % f.length]}`, fi)));
  let faces = solid.faces.reduce((n, f) => n + f.length, 0);
  for (const [a, b] of solid.edges) {
    const i = owner.get(`${a},${b}`), j = owner.get(`${b},${a}`), A = solid.vertices[a], B = solid.vertices[b];
    const n = cross(sub(B, A), sub(tips[i], A)), l = norm(n);
    if (l > 0 && Math.abs(dot(n, sub(tips[j], A))) / l < tol) faces -= 1;
  }
  return { v: solid.vertices.length + tips.length, f: faces };
}
