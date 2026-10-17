// Site lattices (DICTO 2026-10-17, growing Rhombiverse's Hexagonal block): lattices given as data — a repeat cell (three basis vectors)
// and the pieces inside it ("kinds", each a convex solid by its corners) — so every one builds the same way: tap a face, and the piece
// that lies just across it (whatever kind it is) goes in. Cells are stored as (x, y, z) with the kind folded into x (x·8 + o), so one
// world store holds every kind.
//   hcp       hexagonal close packing at fcc's own sphere spacing (√2 at SCALE 1, DICTO: "match fcc"): two trapezo-rhombic dodecahedra
//             per cell (the A and B layers' Voronoi cells, worked out here from their 12 neighbours), each of the RD's volume;
//   gyro      the gyrated octet: tetrahedra and octahedra on the hcp points, the slab above each layer the mirror of the one below
//             (6 pieces per cell: in each slab one up tetrahedron, one down tetrahedron, one octahedron);
//   triprism  triangular prisms, six to a Hex Prism (DICTO: "six make a hex prism"): the Hex Prism's own lattice, edge and height.
const S2 = Math.SQRT2, S3 = Math.sqrt(3);
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.hypot(...a);

// A convex solid's outward face planes { n, d } (n·x ≤ d inside), from its corners.
export function facePlanes(V) {
  const out = [], c = mul(V.reduce(add, [0, 0, 0]), 1 / V.length);
  for (let i = 0; i < V.length; i++) for (let j = i + 1; j < V.length; j++) for (let k = j + 1; k < V.length; k++) {
    let n = cross(sub(V[j], V[i]), sub(V[k], V[i])); const l = norm(n); if (l < 1e-9) continue; n = mul(n, 1 / l);
    let d = dot(n, V[i]); if (dot(n, c) > d) { n = mul(n, -1); d = -d; }
    if (V.some((v) => dot(n, v) > d + 1e-7)) continue;
    if (!out.some((p) => Math.abs(dot(p.n, n) - 1) < 1e-7 && Math.abs(p.d - d) < 1e-7)) out.push({ n, d });
  }
  return out;
}
// Corners of { x : n·x ≤ d for every plane } (a bounded convex solid), by every triple of planes.
function cornersOf(P) {
  const out = [];
  for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) for (let k = j + 1; k < P.length; k++) {
    const a = P[i].n, b = P[j].n, c = P[k].n, det = dot(a, cross(b, c)); if (Math.abs(det) < 1e-9) continue;
    const x = mul(add(add(mul(cross(b, c), P[i].d), mul(cross(c, a), P[j].d)), mul(cross(a, b), P[k].d)), 1 / det);
    if (P.every((p) => dot(p.n, x) <= p.d + 1e-7) && !out.some((y) => norm(sub(x, y)) < 1e-7)) out.push(x);
  }
  return out;
}
function voronoi(site, others) {
  const P = others.filter((q) => norm(sub(q, site)) > 1e-9).map((q) => { const n = sub(q, site), l = norm(n); return { n: mul(n, 1 / l), d: dot(mul(n, 1 / l), mul(add(q, site), 0.5)) }; });
  return cornersOf(P);
}

// ---- hcp at fcc's spacing: a = √2 in the layers, layers c/2 = √(4/3) apart
const A = S2, C = 2 * A * Math.sqrt(2 / 3);
const HB = [[A, 0, 0], [A / 2, A * S3 / 2, 0], [0, 0, C]];
const B_OFF = add(mul(add(HB[0], HB[1]), 1 / 3), [0, 0, C / 2]);
const hcpSites = []; for (let i = -2; i <= 2; i++) for (let j = -2; j <= 2; j++) for (let k = -1; k <= 1; k++) { const o = add(add(mul(HB[0], i), mul(HB[1], j)), mul(HB[2], k)); hcpSites.push(o, add(o, B_OFF)); }
const near = (p) => hcpSites.filter((q) => norm(sub(q, p)) < A * 1.01);
const HCP_KINDS = [voronoi([0, 0, 0], near([0, 0, 0])), voronoi(B_OFF, near(B_OFF))];

// ---- the gyrated octet on the same points: slab 0 (A layer → B layer) and slab 1, its mirror in the B layer
const At = (i, j) => add(mul(HB[0], i), mul(HB[1], j)), Bt = (i, j) => add(At(i, j), B_OFF);
const SLAB0 = [
  [At(0, 0), At(1, 0), At(0, 1), Bt(0, 0)],                         // up tetrahedron: an A triangle, the B point over it
  [Bt(1, 0), Bt(0, 1), Bt(1, 1), At(1, 1)],                         // down tetrahedron: a B triangle over an A point
  [At(1, 0), At(0, 1), At(1, 1), Bt(0, 0), Bt(1, 0), Bt(0, 1)],     // octahedron: an A triangle and the B triangle turned over it
];
const mirror = (v) => [v[0], v[1], C - v[2]];
const GYRO_KINDS = [...SLAB0, ...SLAB0.map((V) => V.map(mirror))];

// ---- triangular prisms in the Hex Prism's own frame (hex-prism.js: flat-top hexagon of radius R, height √3·R, axial q, r)
const R = 1, H = S3;
const TB = [[1.5 * R, S3 * R / 2, 0], [0, S3 * R, 0], [0, 0, H]];
const hv = (k) => [R * Math.cos(Math.PI / 3 * k), R * Math.sin(Math.PI / 3 * k)];
const TRI_KINDS = [0, 1, 2, 3, 4, 5].map((k) => { const a = hv(k), b = hv(k + 1); return [-1, 1].flatMap((s) => [[0, 0, s * H / 2], [a[0], a[1], s * H / 2], [b[0], b[1], s * H / 2]]); });

const make = (id, basis, kinds, colour) => {
  const planes = kinds.map(facePlanes), centres = kinds.map((V) => mul(V.reduce(add, [0, 0, 0]), 1 / V.length));
  const M = basis, det = dot(M[0], cross(M[1], M[2]));
  const toCell = (p) => [dot(p, cross(M[1], M[2])) / det, dot(p, cross(M[2], M[0])) / det, dot(p, cross(M[0], M[1])) / det];
  const origin = (x, y, z) => add(add(mul(M[0], x), mul(M[1], y)), mul(M[2], z));
  return {
    id, kinds, planes, centres, colour,
    /** a kind's corners about its own centre (its InstancedMesh geometry) */
    local: (o) => kinds[o].map((v) => sub(v, centres[o])),
    /** world position of a piece's centre (times the app's scale s) */
    centre: (x, y, z, o, s = 1) => mul(add(origin(x, y, z), centres[o]), s),
    /** the first piece offered on an empty world: the one whose centre is nearest the origin, where the camera looks */
    first: (() => { let best = null; for (let x = -1; x <= 1; x++) for (let y = -1; y <= 1; y++) for (let z = -1; z <= 1; z++) for (let o = 0; o < kinds.length; o++) {
      const c = norm(add(origin(x, y, z), centres[o])); if (!best || c < best[0] - 1e-9) best = [c, [x, y, z, o]]; } return best[1]; })(),
    /** the piece that holds point p (world, unscaled), as [x, y, z, o], or null */
    pieceAt(p) {
      const f = toCell(p).map(Math.floor);
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
        const x = f[0] + dx, y = f[1] + dy, z = f[2] + dz, q = sub(p, origin(x, y, z));
        for (let o = 0; o < kinds.length; o++) if (planes[o].every((pl) => dot(pl.n, q) <= pl.d - 1e-6)) return [x, y, z, o];
      }
      return null;
    },
  };
};
export const SITE_LATTICES = {
  hcp: make('hcp', HB, HCP_KINDS, 'glassite'),
  gyro: make('gyro', HB, GYRO_KINDS, 'glassite'),
  triprism: make('triprism', TB, TRI_KINDS, 'water'),
};
export const SITE_LATTICE_LABELS = { hcp: 'HCP · trapezo-rhombic dodecahedra', gyro: 'Gyrated octet · tetrahedra and octahedra', triprism: 'Triangular prisms' };
// the kind folded into x, so one world store keyed (x, y, z) holds every kind
export const packCell = (x, o) => x * 8 + o;
export const unpackCell = (X) => { const o = ((X % 8) + 8) % 8; return [(X - o) / 8, o]; };
/** the piece across a tapped face: hit point p (world, unscaled) and the face's outward normal n */
export function acrossFace(lat, p, n) { return lat.pieceAt(add(p, mul(n, 0.02))); }
export const _test = { HCP_KINDS, GYRO_KINDS, TRI_KINDS, facePlanes, A, C };
