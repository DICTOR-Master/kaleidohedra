// DICTO's Vacuus and Resonus of a convex polyhedron (DICTO 2026-11-24/25), computed from its own corners, edges and faces about a
// chosen centre O. Ported from the archived Polyhedraverse (branch vacuus-resonus-view, app/lib/vacuusResonus.ts).
//   Vacuus: one plate through O and each edge; edges on one plane share a plate. A plate is a full sheet if it carries, with each edge
//           e, the opposite edge -e; a shared sheet if it carries two or more edges but is not full; a single fin if it carries one.
//           Kind: heart (all full), non-heart (all single), inherited heart (else).
//   Resonus: one plane through O parallel to each face; parallel faces share one plane.
//   Mirror: a plane through O whose reflection maps the corner set onto itself.
//   On the sphere: the planes cut the unit sphere into V points, E arcs and R regions; simplicial when every region is a triangle.
// Floating point with a tolerance, for display. The exact counts are the catalogue's (data/vacuus-resonus-catalogue.json);
// scripts/verify-vacuus-resonus.mjs checks that this module agrees with them on every polyhedron. Pure maths, no three.js.
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const mul = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.sqrt(dot(a, a));
const unit = (a) => mul(a, 1 / norm(a));
const EPS = 1e-6;
const DET_EPS = 1e-10;
/** Directions up to sign, clustered with a hash grid (looks up d and -d). */
class LineSet {
  cells = new Map();
  dirs = [];
  key(d, dx = 0, dy = 0, dz = 0) {
    const q = 1 / (EPS * 20);
    return `${Math.round(d[0] * q) + dx},${Math.round(d[1] * q) + dy},${Math.round(d[2] * q) + dz}`;
  }
  find(d) {
    for (const s of [d, mul(d, -1)]) {
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
        for (const i of this.cells.get(this.key(s, dx, dy, dz)) ?? []) {
          if (norm(cross(this.dirs[i], d)) < EPS * 10) return i;
        }
      }
    }
    return -1;
  }
  /** Index of d's line, adding it if new. */
  add(d) {
    const f = this.find(d);
    if (f >= 0) return f;
    this.dirs.push(d);
    const k = this.key(d);
    const cell = this.cells.get(k);
    if (cell) cell.push(this.dirs.length - 1);
    else this.cells.set(k, [this.dirs.length - 1]);
    return this.dirs.length - 1;
  }
}
function sphereArrangement(normals) {
  // Each crossing line is found as the full set of planes through it: plane k holds the line of planes i and j exactly when
  // det(n_i, n_j, n_k) = 0. The determinant keeps the coordinates' own accuracy, where comparing line directions would magnify it for
  // planes at a small angle. Every region has at least 3 sides once the planes do not all share one line, and the sides add up to 2E,
  // so all are triangles exactly when 2E = 3R.
  const P = normals.length;
  const covered = /* @__PURE__ */ new Set();
  let lines = 0;
  let E = 0;
  for (let i = 0; i < P; i++) {
    for (let j = i + 1; j < P; j++) {
      if (covered.has(i * P + j)) continue;
      const d = cross(normals[i], normals[j]);
      const through = [i, j];
      for (let k = 0; k < P; k++) if (k !== i && k !== j && Math.abs(dot(d, normals[k])) < DET_EPS) through.push(k);
      for (const a of through) for (const b of through) if (a < b) covered.add(a * P + b);
      lines++;
      E += 2 * through.length;
    }
  }
  const V = 2 * lines;
  const regions = P === 1 ? 2 : 2 - V + E;
  const simplicial = lines > 1 && 2 * E === 3 * regions;
  return { V, E, regions, simplicial };
}
function cornerCentroid(spec) {
  const s = spec.vertices.reduce((acc, v) => add(acc, v), [0, 0, 0]);
  return mul(s, 1 / spec.vertices.length);
}
/** Centroid of the solid region (cones from the corner centroid over fan triangles). */
function volumeCentroid(spec) {
  const p = cornerCentroid(spec);
  let vol = 0;
  let acc = [0, 0, 0];
  for (const f of spec.faces) {
    const a = spec.vertices[f[0]];
    for (let k = 1; k + 1 < f.length; k++) {
      const b = spec.vertices[f[k]];
      const c = spec.vertices[f[k + 1]];
      const v = Math.abs(dot(sub(a, p), cross(sub(b, p), sub(c, p)))) / 6;
      vol += v;
      acc = add(acc, mul(add(add(p, a), add(b, c)), v / 4));
    }
  }
  return mul(acc, 1 / vol);
}
function faceNormal(c, f) {
  let n = [0, 0, 0];
  for (let i = 0; i < f.length; i++) n = add(n, cross(c[f[i]], c[f[(i + 1) % f.length]]));
  return unit(n);
}
/** The convex polygon where the plane through O with normal n cuts the hull. */
function slicePolygon(c, edges, n, scale) {
  const pts = [];
  const tol = EPS * scale;
  const push = (p) => {
    if (!pts.some((q) => norm(sub(p, q)) < tol * 10)) pts.push(p);
  };
  for (const [i, j] of edges) {
    const da = dot(c[i], n);
    const db = dot(c[j], n);
    if (Math.abs(da) < tol) push(c[i]);
    if (Math.abs(db) < tol) push(c[j]);
    if (da > tol && db < -tol || da < -tol && db > tol) {
      const t = da / (da - db);
      push(add(c[i], mul(sub(c[j], c[i]), t)));
    }
  }
  if (pts.length < 3) return pts;
  const u = unit(Math.abs(n[0]) < 0.9 ? cross(n, [1, 0, 0]) : cross(n, [0, 1, 0]));
  const w = cross(n, u);
  return pts.map((p) => ({ p, a: Math.atan2(dot(p, w), dot(p, u)) })).sort((x, y) => x.a - y.a).map((x) => x.p);
}
function analyse(spec, centre) {
  const c = spec.vertices.map((v) => sub(v, centre));
  const scale = Math.max(...c.map(norm));
  const tol = EPS * scale;
  const hasCorner = (p) => c.some((q) => norm(sub(p, q)) < tol * 10);
  const isMirror = (n) => c.every((v) => hasCorner(sub(v, mul(n, 2 * dot(v, n)))));
  const edgeKey = (i, j) => i < j ? `${i},${j}` : `${j},${i}`;
  const edgeSet = new Set(spec.edges.map(([i, j]) => edgeKey(i, j)));
  const cornerIndex = (p) => c.findIndex((q) => norm(sub(p, q)) < tol * 10);
  const plateLines = new LineSet();
  const plateEdges = [];
  spec.edges.forEach(([i, j], e) => {
    const k = plateLines.add(unit(cross(c[i], c[j])));
    (plateEdges[k] ?? (plateEdges[k] = [])).push(e);
  });
  const resLines = new LineSet();
  const resFaces = [];
  spec.faces.forEach((f, fi) => {
    const k = resLines.add(faceNormal(c, f));
    (resFaces[k] ?? (resFaces[k] = [])).push(fi);
  });
  const plates = plateLines.dirs.map((n, k) => {
    const edges = plateEdges[k];
    let sheet = edges.length === 1 ? "single" : "shared";
    if (edges.length > 1) {
      const full2 = edges.every((e) => {
        const [i, j] = spec.edges[e];
        const oi = cornerIndex(mul(c[i], -1));
        const oj = cornerIndex(mul(c[j], -1));
        return oi >= 0 && oj >= 0 && edgeSet.has(edgeKey(oi, oj));
      });
      if (full2) sheet = "full";
    }
    return { normal: n, edges, sheet, mirror: isMirror(n), both: resLines.find(n) >= 0, slice: slicePolygon(c, spec.edges, n, scale) };
  });
  const resonus = resLines.dirs.map((n, k) => ({
    normal: n,
    faces: resFaces[k],
    mirror: isMirror(n),
    both: plateLines.find(n) >= 0,
    slice: slicePolygon(c, spec.edges, n, scale)
  }));
  const mirrorLines = new LineSet();
  let mirrors = 0;
  for (let i = 0; i < c.length; i++) {
    for (let j = i + 1; j < c.length; j++) {
      const d = sub(c[i], c[j]);
      if (Math.abs(norm(c[i]) - norm(c[j])) > tol * 10) continue;
      const n = unit(d);
      if (mirrorLines.find(n) >= 0) continue;
      mirrorLines.add(n);
      if (isMirror(n)) mirrors++;
    }
  }
  const full = plates.filter((p) => p.sheet === "full").length;
  const single = plates.filter((p) => p.sheet === "single").length;
  const shared = plates.length - full - single;
  const kind = full === plates.length ? "heart" : single === plates.length ? "non-heart" : "inherited heart";
  const twoFaces = resonus.filter((r) => r.faces.length === 2).length;
  return {
    centre,
    corners: c,
    mirrors,
    plates,
    resonus,
    counts: {
      plates: plates.length,
      full,
      shared,
      single,
      kind,
      vacuusOnMirrors: plates.filter((p) => p.mirror).length,
      vacuusSphere: sphereArrangement(plates.map((p) => p.normal)),
      resonusPlanes: resonus.length,
      twoFaces,
      oneFace: resonus.length - twoFaces,
      resonusOnMirrors: resonus.filter((r) => r.mirror).length,
      resonusSphere: sphereArrangement(resonus.map((r) => r.normal)),
      both: plates.filter((p) => p.both).length
    }
  };
}
export {
  analyse,
  cornerCentroid,
  sphereArrangement,
  volumeCentroid
};
