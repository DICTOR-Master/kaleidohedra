// The outer surface of a solid made of convex pieces that meet face to face (the HexOct family's tiles, paper #86): the pieces' faces
// with the parts where two pieces touch taken away, and coplanar faces merged, as the paper draws them ("merged faces are drawn solid
// with their edges"). A float port of the study's exact union_faces (k-research studies/2026-10-31-hexoct-ring-build/scripts/
// exactfaces.py): per plane, every piece face is cut by the lines of all the faces in that plane into cells; a cell counts +1 for each
// piece face on it pointing one way and −1 the other way, so a cell where two pieces touch counts 0 (a joint, not drawn) and the rest
// are surface. Cells of one plane and one side that share an edge are one merged face; a cell side that no other cell of its face
// covers is an edge of the solid.
const EPS = 1e-7;
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
const area2 = (P) => P.reduce((s, p, i) => { const q = P[(i + 1) % P.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
const fix = (x, d) => (Math.abs(x) < 0.5 * 10 ** -d ? 0 : x).toFixed(d);   // a rounded key, no "-0"
const mean = (P) => P.reduce((a, p) => a.map((x, c) => x + p[c] / P.length), P[0].map(() => 0));

// the part of convex polygon P (2D, ccw) on side `keep` (+1: a·x ≥ c, −1: a·x ≤ c) of the line a·x = c
function clip(P, [a, c], keep) {
  const out = [], side = (p) => keep * (a[0] * p[0] + a[1] * p[1] - c);
  for (let i = 0; i < P.length; i++) {
    const p = P[i], q = P[(i + 1) % P.length], sp = side(p), sq = side(q);
    if (sp >= -EPS) out.push(p);
    if ((sp > EPS && sq < -EPS) || (sp < -EPS && sq > EPS)) { const t = sp / (sp - sq); out.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]); }
  }
  const clean = out.filter((p, i) => Math.hypot(p[0] - out[(i + 1) % out.length][0], p[1] - out[(i + 1) % out.length][1]) > EPS);
  return clean.length >= 3 && Math.abs(area2(clean)) > 1e-10 ? clean : null;
}
const inside = (P, x) => P.every((p, i) => { const q = P[(i + 1) % P.length]; return (q[0] - p[0]) * (x[1] - p[1]) - (q[1] - p[1]) * (x[0] - p[0]) > 1e-9; });

/** pieces: [{ vertices, faces }] (each convex, faces as corner-index loops). Returns { faces: merged face count, cells: [{ plane, n
 *  (outward), face (merged face id), poly (3D) }], edges: [[u, v]] (the solid's edges), contacts: [[i, j, area]] (pieces touching
 *  along a face), volume, corners: points where the edges turn }. */
export function tileSurface(pieces) {
  const planes = new Map();
  pieces.forEach((pc, pi) => {
    const c = mean(pc.vertices);
    for (const f of pc.faces) {
      const P = f.map((i) => pc.vertices[i]);
      let n = [0, 0, 0];
      for (let i = 1; i + 1 < P.length; i++) n = n.map((x, k) => x + cross(sub(P[i], P[0]), sub(P[i + 1], P[0]))[k]);
      n = norm(n);
      if (dot(n, sub(P[0], c)) < 0) n = n.map((x) => -x);   // outward
      // the unoriented plane: its normal's first clear component positive
      const k = Math.abs(n[0]) > EPS ? 0 : Math.abs(n[1]) > EPS ? 1 : 2, s = n[k] > 0 ? 1 : -1, m = n.map((x) => x * s), d = dot(m, P[0]);
      const key = [...m, d].map((x) => fix(x, 6)).join(',');
      if (!planes.has(key)) {
        const u = norm(Math.abs(m[0]) < 0.9 ? cross(m, [1, 0, 0]) : cross(m, [0, 1, 0])), w = cross(m, u);
        planes.set(key, { m, d, u, w, items: [] });
      }
      planes.get(key).items.push({ s, pi, P });
    }
  });
  const cells = [], contacts = new Map();
  let faceId = 0, volume = 0;
  for (const [key, pl] of planes) {
    const to2 = (p) => [dot(p, pl.u), dot(p, pl.w)], to3 = (q) => pl.m.map((x, k) => x * pl.d + q[0] * pl.u[k] + q[1] * pl.w[k]);
    const polys = pl.items.map((it) => { const Q = it.P.map(to2); return { ...it, Q: area2(Q) < 0 ? Q.reverse() : Q }; });
    const lines = new Map();
    for (const { Q } of polys) Q.forEach((p, i) => {
      const q = Q[(i + 1) % Q.length], a = norm([q[1] - p[1], p[0] - q[0], 0]).slice(0, 2), c = a[0] * p[0] + a[1] * p[1];
      const sg = Math.abs(a[0]) > EPS ? Math.sign(a[0]) : Math.sign(a[1]);
      lines.set([a[0] * sg, a[1] * sg, c * sg].map((x) => fix(x, 6)).join(','), [[a[0] * sg, a[1] * sg], c * sg]);
    });
    // the same cell cut from two faces: the same centre (matched within a tolerance, not by a rounded key, which can fall either side
    // of a rounding step)
    const cellList = [];
    for (const it of polys) {
      let cur = [it.Q];
      for (const L of lines.values()) cur = cur.flatMap((C) => [clip(C, L, 1), clip(C, L, -1)].filter(Boolean));
      for (const C of cur) {
        const c = mean(C), a = Math.abs(area2(C));
        let e = cellList.find((x) => Math.hypot(x.c[0] - c[0], x.c[1] - c[1]) < 1e-6 && Math.abs(x.a - a) < 1e-8);
        if (!e) cellList.push((e = { C, c, a, w: 0, by: [] }));
        e.w += it.s; e.by.push(it.pi);
      }
    }
    const surf = [];
    for (const e of cellList) {
      if (Math.abs(e.w) > 1) throw new Error(`tileSurface: pieces overlap on plane ${key}`);
      if (e.w === 0) {
        const [i, j] = [...new Set(e.by)].sort((x, y) => x - y);
        if (j !== undefined) { const k = `${i},${j}`; contacts.set(k, (contacts.get(k) ?? 0) + Math.abs(area2(e.C))); }
      } else surf.push(e);
    }
    // merged faces: cells of one side that share an edge (a point just across a cell's side lies in the other cell)
    const across = (C, i) => {
      const p = C[i], q = C[(i + 1) % C.length], mid = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], l = Math.hypot(q[0] - p[0], q[1] - p[1]);
      return [mid[0] + ((q[1] - p[1]) / l) * 1e-5, mid[1] - ((q[0] - p[0]) / l) * 1e-5];   // outward of a ccw cell: to the right
    };
    const par = surf.map((_, i) => i), find = (i) => (par[i] === i ? i : (par[i] = find(par[i])));
    const open = surf.map((e) => e.C.map(() => true));
    surf.forEach((e, a) => e.C.forEach((_, i) => {
      const x = across(e.C, i), b = surf.findIndex((f, bi) => bi !== a && f.w === e.w && inside(f.C, x));
      if (b >= 0) { par[find(a)] = find(b); open[a][i] = false; }
    }));
    const ids = new Map();
    surf.forEach((e, a) => {
      const r = find(a);
      if (!ids.has(r)) ids.set(r, faceId++);
      const n = pl.m.map((x) => x * e.w), P = e.C.map(to3);
      // the cell's corners in turn about its outward normal
      if (dot(cross(sub(P[1], P[0]), sub(P[2], P[0])), n) < 0) P.reverse();
      cells.push({ plane: key, n, face: ids.get(r), poly: P, edges: e.C.flatMap((_, i) => (open[a][i] ? [[to3(e.C[i]), to3(e.C[(i + 1) % e.C.length])]] : [])) });
      volume += (e.w * pl.d * Math.abs(area2(e.C))) / 3;
    });
  }
  const edges = cells.flatMap((c) => c.edges);
  // corners: end points of the edges where they do not run straight on
  const ends = new Map();
  for (const [p, q] of edges) for (const [a, b] of [[p, q], [q, p]]) {
    const k = a.map((x) => fix(x, 5)).join(',');
    if (!ends.has(k)) ends.set(k, { p: a, dirs: [] });
    ends.get(k).dirs.push(norm(sub(b, a)));
  }
  const corners = [...ends.values()].filter((e) => e.dirs.some((d) => e.dirs.some((g) => Math.hypot(...cross(d, g)) > 1e-6))).map((e) => e.p);
  return { faces: faceId, cells, edges, contacts: [...contacts].map(([k, a]) => [...k.split(',').map(Number), a]), volume, corners };
}

/** Whether a set of pieces is one solid joined along faces: the contact graph of tileSurface connects every piece. */
export function joinedAlongFaces(n, contacts) {
  const seen = new Set([0]), stack = [0];
  while (stack.length) { const i = stack.pop(); for (const [a, b, ar] of contacts) if (ar > 1e-9) for (const [x, y] of [[a, b], [b, a]]) if (x === i && !seen.has(y)) { seen.add(y); stack.push(y); } }
  return seen.size === n;
}
