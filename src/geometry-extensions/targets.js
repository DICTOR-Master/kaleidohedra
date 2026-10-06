// The target cells (TARGETS.md, data/geometry-targets.json): every equal-edge
// space-filling zonohedron whose edge directions meet only at special angles.
// Each target is stored as the Gram matrix of its unit edge directions; this
// rebuilds the directions, the zonohedron (edge 1), its faces by kind, its
// volume and its lattice of translations. Three-free; checked by
// scripts/verify-targets.mjs.

export const TARGET_TYPES = ['parallelepiped', 'hexagonal prism', 'rhombic dodecahedron', 'elongated dodecahedron', 'truncated octahedron'];

const EPS = 1e-7;
// cos of 0, 36, 45, 60, arccos(1/3), 72 and 90 degrees.
const SPECIAL_COS = [1, (1 + Math.sqrt(5)) / 4, Math.SQRT1_2, 0.5, 1 / 3, (Math.sqrt(5) - 1) / 4, 0];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const scale = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.hypot(...a);
const unit = (a) => scale(a, 1 / norm(a));
export const det3 = (a, b, c) => dot(a, cross(b, c));
const lineAngle = (a, b) => (Math.acos(Math.min(1, Math.abs(dot(a, b)))) * 180) / Math.PI;
const label = (x) => String(Math.round(x * 100) / 100);

// Unit vectors with the given Gram matrix (rank 3): the first three
// independent ones by Cholesky, every other one by its dot products with those.
export function directionsFromGram(recorded) {
  // The file rounds to 9 places; snap each entry back to its exact special cosine.
  const G = recorded.map((row) => row.map((g) => {
    const c = SPECIAL_COS.find((x) => Math.abs(Math.abs(g) - x) < 1e-6);
    return c === undefined ? g : Math.sign(g) * c;
  }));
  const n = G.length;
  const basis = [];
  const B = [];
  for (let i = 0; i < n && basis.length < 3; i++) {
    // Gram-Schmidt in coordinates: v_i's components along the basis built so far.
    const v = [0, 0, 0];
    for (let k = 0; k < basis.length; k++) {
      let s = G[i][basis[k]];
      for (let m = 0; m < k; m++) s -= v[m] * B[k][m];
      v[k] = s / B[k][k];
    }
    const rest = G[i][i] - v.reduce((s, x) => s + x * x, 0);
    if (rest < 1e-9) continue;
    v[basis.length] = Math.sqrt(rest);
    basis.push(i);
    B.push(v);
  }
  return G.map((row, i) => {
    const k = basis.indexOf(i);
    if (k >= 0) return B[k];
    // Solve B x = (row's dots with the basis): B is lower triangular.
    const x = [0, 0, 0];
    for (let r = 0; r < 3; r++) {
      let s = row[basis[r]];
      for (let m = 0; m < r; m++) s -= B[r][m] * x[m];
      x[r] = s / B[r][r];
    }
    return x;
  });
}

// The face kind of a zone (the directions lying in one face plane), named as discover.py names it.
function kindOf(zone) {
  const angs = [];
  for (let i = 0; i < zone.length; i++) for (let j = i + 1; j < zone.length; j++) angs.push(Math.round(lineAngle(zone[i], zone[j]) * 100) / 100);
  angs.sort((a, b) => a - b);
  if (zone.length === 2) return angs[0] === 90 ? 'square' : `rhombus ${label(angs[0])}`;
  return angs.every((a) => a === 60) ? 'regular hexagon' : `hexagon ${angs.map((a) => label(180 - a)).join('/')}`;
}

// The zonohedron of unit directions D, centred at the origin: every face is the
// zonogon of the directions in its plane, counter-clockwise seen from outside.
export function zonohedron(D) {
  const planes = [];
  for (let i = 0; i < D.length; i++) for (let j = i + 1; j < D.length; j++) {
    const c = cross(D[i], D[j]);
    if (norm(c) < EPS) continue;
    const n = unit(c);
    if (!planes.some((p) => norm(cross(p, n)) < EPS)) planes.push(n);
  }
  const faces = [];
  for (const n of planes) {
    const zone = D.filter((d) => Math.abs(dot(d, n)) < EPS);
    for (const s of [1, -1]) {
      const m = scale(n, s);
      const centre = D.filter((d) => Math.abs(dot(d, n)) >= EPS).reduce((c, d) => add(c, scale(d, Math.sign(dot(d, m)) / 2)), [0, 0, 0]);
      const u = zone[0], w = cross(m, u);
      const angle = (e) => Math.atan2(dot(e, w), dot(e, u));
      // Each zone direction turned to angle [0, pi), in counter-clockwise order.
      const edges = zone.map((e) => (angle(e) < -EPS || Math.abs(angle(e) - Math.PI) < EPS ? scale(e, -1) : e)).sort((a, b) => angle(a) - angle(b));
      let p = edges.reduce((q, e) => sub(q, scale(e, 0.5)), centre);
      const polygon = [];
      for (const e of [...edges, ...edges.map((e) => scale(e, -1))]) { polygon.push(p); p = add(p, e); }
      faces.push({ polygon, normal: m, centre, kind: kindOf(zone) });
    }
  }
  return faces;
}

const polygonArea = (P, n) => {
  let a = [0, 0, 0];
  for (let i = 0; i < P.length; i++) a = add(a, cross(P[i], P[(i + 1) % P.length]));
  return dot(a, n) / 2;
};
export const volumeOf = (faces) => faces.reduce((v, f) => v + (polygonArea(f.polygon, f.normal) * dot(f.centre, f.normal)) / 3, 0);

export function faceCounts(faces) {
  const out = {};
  for (const f of faces) out[f.kind] = (out[f.kind] ?? 0) + 1;
  return out;
}

// The lattice: each face's neighbour sits at twice the face centre. Three of
// those translations whose determinant is the cell volume form a basis.
export function latticeBasis(faces) {
  const T = faces.map((f) => scale(f.centre, 2));
  const vol = volumeOf(faces);
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) for (let k = j + 1; k < T.length; k++) {
    const d = det3(T[i], T[j], T[k]);
    if (Math.abs(Math.abs(d) - vol) < 1e-6) return d > 0 ? [T[i], T[j], T[k]] : [T[i], T[k], T[j]];
  }
  return null;
}

// One target's cell, built: directions, faces (polygons), volume, lattice basis.
export function buildTarget(target) {
  const directions = directionsFromGram(target.gram);
  const faces = zonohedron(directions);
  return { directions, faces, volume: volumeOf(faces), basis: latticeBasis(faces) };
}

// Name and number within its type, as in TARGETS.md: "Parallelepiped #12 · 36/60/90".
export function numberTargets(targets) {
  const seen = {};
  return targets.map((t) => {
    seen[t.type] = (seen[t.type] ?? 0) + 1;
    return { ...t, number: seen[t.type] };
  });
}
export const targetAngles = (t) => [...new Set(t.line_angles.map(label))].join('/');

let dataPromise = null;
export function loadTargets() {
  dataPromise ??= fetch('./data/geometry-targets.json').then((r) => r.json()).then((d) => numberTargets(d.targets)).catch(() => []);
  return dataPromise;
}

// The world's emblem (wizard thumbnail): the regular-hexagon elongated
// dodecahedron (DISCOVERIES.md #5), the zonohedron of the four Bain
// directions and one at right angles to their common axis (checked in verify-targets).
export const EMBLEM_DIRECTIONS = [[1, 1, Math.SQRT2], [1, -1, Math.SQRT2], [-1, 1, Math.SQRT2], [-1, -1, Math.SQRT2]].map((v) => scale(v, 0.5)).concat([[1, 0, 0]]);
