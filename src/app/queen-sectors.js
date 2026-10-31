// Queen sectors (DICTO 2026-10-31, "yes go ahead with twelve sectors for red queen and 20 sectors for white"; study
// k-research/studies/2026-10-31-queen-sectors): each Queen cut from the centre along the axes of her core's pyramids. A sector is
// the cone, from the seed axis v (the first coordinate), over one face of the core: the Red Queen's 12 over her core dodecahedron's
// pentagons (Aristotle's 12 pentagonal pyramids), the White Queen's 20 over her core icosahedron's triangles (the 20 Cleo-Icos).
// Whole cells cannot be dealt out (half of the White Queen's and most of the Red Queen's sit on boundaries), so every drawn cell is
// CUT by the sector planes into convex wedges, exactly. Each boundary is a hyperplane through v, its normal across v; every picture
// in the Shells view (Shells, Cut open, RCP view, RCP v4) maps a point x to (frame · x) / f(x₀) with f > 0, so in the picture the
// boundary is the plane through the centre with that same normal (spanned by the axis and a core edge's direction). Pure maths.
import * as WQG from './white-queen-geometry.js';
import * as RQG from './red-queen-geometry.js';

const FRAME = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]];   // the Shells view's frame across v (CLEO_POINTS, LAYER_POINTS, RCP)
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const unit = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
const across = (x) => FRAME.map((f) => f.reduce((s, c, i) => s + c * x[i], 0));
const mean = (P) => [0, 1, 2].map((i) => P.reduce((s, p) => s + p[i], 0) / P.length);

/** The core's faces as loops of the queen's vertex indices: the White Queen's 20 triangles (each core cell less the seed vertex 0),
 *  the Red Queen's 12 pentagons (her core dodecahedron, the cell round the White Queen's vertex 0). */
function coreFaces(queen) {
  if (queen === 'red') return RQG.cellFaces(RQG.CELL_LAYERS[0].cells[0]);
  return WQG.CLEO_SHELLS[0].cells.map((ci) => WQG.CELLS[ci].filter((k) => k !== 0));
}
/** The sectors: { axis (unit, the direction from the centre to its core face's centre), normals (the cone's bounding planes
 *  through the centre, pointing inwards: the cone is every x with n · x ≥ 0 for all n) }. */
export function sectorCones(queen) {
  const V = queen === 'red' ? RQG.VERTICES : WQG.VERTICES;
  return coreFaces(queen).map((loop) => {
    const P = loop.map((k) => across(V[k])), c = mean(P);
    const normals = P.map((p, i) => { const n = unit(cross(p, P[(i + 1) % P.length])); return dot(n, c) < 0 ? n.map((x) => -x) : n; });
    return { axis: unit(c), normals };
  });
}
export const SECTOR_COUNT = { white: 20, red: 12 };

/** The convex polytope given by its faces (point loops) cut to n · x ≥ 0: its faces, the cut face added; [] if nothing is left. */
export function clipConvex(faces, n, eps = 1e-9) {
  const d = (p) => dot(n, p);
  let lo = Infinity, hi = -Infinity;
  for (const f of faces) for (const p of f) { const x = d(p); if (x < lo) lo = x; if (x > hi) hi = x; }
  if (lo >= -eps) return faces;
  if (hi <= eps) return [];
  const out = [], cap = [];
  const put = (p) => { if (!cap.some((q) => Math.abs(q[0] - p[0]) + Math.abs(q[1] - p[1]) + Math.abs(q[2] - p[2]) < 10 * eps)) cap.push(p); };
  for (const f of faces) {
    const g = [];
    f.forEach((p, i) => {
      const q = f[(i + 1) % f.length], dp = d(p), dq = d(q);
      if (dp >= -eps) { g.push(p); if (Math.abs(dp) <= eps) put(p); }
      if ((dp > eps && dq < -eps) || (dp < -eps && dq > eps)) { const t = dp / (dp - dq), x = [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]), p[2] + t * (q[2] - p[2])]; g.push(x); put(x); }
    });
    if (g.length >= 3) out.push(g);
  }
  if (cap.length >= 3) {
    // the cut face: its points in order round their centre, in the plane
    const c = mean(cap), a = unit(sub(cap[0], c)), b = cross(n, a);
    out.push(cap.map((p) => ({ p, t: Math.atan2(dot(sub(p, c), b), dot(sub(p, c), a)) })).sort((x, y) => x.t - y.t).map((x) => x.p));
  }
  return out;
}
/** The volume of a convex polytope given by its faces (each fanned from the centre of its corners). */
export function volume(faces) {
  const all = faces.flat();
  if (!all.length) return 0;
  const o = mean(all);
  let v = 0;
  for (const f of faces) for (let i = 1; i + 1 < f.length; i++) v += Math.abs(dot(sub(f[0], o), cross(sub(f[i], o), sub(f[i + 1], o)))) / 6;
  return v;
}
/** One cell (its faces as point loops in the picture) cut into its wedges: [{ sector, faces }], each wedge in one sector's cone. */
export function cellWedges(faces, cones) {
  const size = Math.max(...faces.flat().map((p) => Math.hypot(...p))), eps = 1e-9 * Math.max(1, size), out = [];
  const pts = faces.flat();
  cones.forEach((cone, s) => {
    if (cone.normals.some((n) => pts.every((p) => dot(n, p) <= eps))) return;   // wholly outside this cone
    let w = faces;
    for (const n of cone.normals) { w = clipConvex(w, n, eps); if (!w.length) return; }
    if (volume(w) > 1e-9 * size ** 3) out.push({ sector: s, faces: w });
  });
  return out;
}
/** A cell's faces as loops of corner indices: the White Queen's tetrahedra, the Red Queen's dodecahedra. */
export const cellFaceLoops = (queen, ci) => {
  if (queen === 'red') return RQG.cellFaces(ci);
  const c = WQG.CELLS[ci];
  return [[c[0], c[1], c[2]], [c[0], c[1], c[3]], [c[0], c[2], c[3]], [c[1], c[2], c[3]]];
};
/** Every cell of the queen at the picture's points Q (one 3D point per vertex), cut into wedges: an array by cell index. */
export function queenWedges(queen, Q, cells) {
  const cones = sectorCones(queen);
  return cells.map((ci) => cellWedges(cellFaceLoops(queen, ci).map((f) => f.map((k) => Q[k])), cones));
}
