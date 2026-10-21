// Aristotle's Pyramid (DICTO 2026-10-21; DICTO's question, paper #44, DICTO DOI 10.5281/zenodo.23529497): the geometry of the world,
// computed from the Platonic solids and the Cleo-Icos & Antonius kit already in krp-core. No three.js here, so the unit tests can run it.
//   - facePyramids(key): a Platonic solid cut from its centre into its face pyramids (the cone from the centre over each face).
//   - FILLS: three blocks of a few cells: cube pyramids filling cubes; the octet cut up (each 60° rhombohedron = tetrahedron +
//     octahedron + tetrahedron, cut into 8 octahedron and 8 tetrahedron pyramids); the golden fix (the kit 'antonius.block': 8 prolate
//     golden rhombohedra, each Cleo-Icos + Antonius + Cleo-Icos).
// A piece is { kind, faces: [[x, y, z][]], axis }: its faces as polygons (corners in order) and the direction it is drawn apart along.
import { POLYHEDRA, KITS13 } from '../krp-core/src/polyhedra/index.js';

export const SOLID_KEYS = ['cube', 'tetrahedron', 'octahedron', 'dodecahedron', 'icosahedron'];
const SOLID_IDS = { cube: 'CUBE', tetrahedron: 'D4', octahedron: 'D8', dodecahedron: 'DODECAHEDRON', icosahedron: 'D20' };
export const GOLDEN_KIT = 'antonius.block';

const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const norm = (a) => { const l = Math.hypot(...a) || 1; return scale(a, 1 / l); };
const mean = (P) => scale(P.reduce(add, [0, 0, 0]), 1 / P.length);
/** v turned by the unit quaternion [x, y, z, w]. */
function rotate(v, [x, y, z, w]) {
  const tx = 2 * (y * v[2] - z * v[1]), ty = 2 * (z * v[0] - x * v[2]), tz = 2 * (x * v[1] - y * v[0]);
  return [v[0] + w * tx + (y * tz - z * ty), v[1] + w * ty + (z * tx - x * tz), v[2] + w * tz + (x * ty - y * tx)];
}

/** The pyramid from apex O over the polygon F: the base and one triangle per side. */
function pyramid(kind, O, F) {
  const faces = [F, ...F.map((p, i) => [O, F[(i + 1) % F.length], p])];
  return { kind, faces, axis: norm(sub(mean(F), O)) };
}
/** All face pyramids of a convex solid given by its corners and faces (corner indices), apex at its centre. */
function conePieces(kind, V, F, centre = mean(V)) { return F.map((f) => pyramid(kind, centre, f.map((i) => V[i]))); }

/** A Platonic solid (edge 1, centre at the origin) cut into its face pyramids. */
export function facePyramids(key) {
  const S = POLYHEDRA[SOLID_IDS[key]];
  return conePieces(key, S.vertices, S.faces);
}
/** The whole solid's faces (for its outline while drawn apart). */
export function solidFaces(key) { const S = POLYHEDRA[SOLID_IDS[key]]; return S.faces.map((f) => f.map((i) => S.vertices[i])); }

// (a) cube pyramids filling cubes: 2 × 2 × 2 cubes of edge 1, each cut into its 6 pyramids; tone by the cube's parity.
const CUBE = POLYHEDRA.CUBE;
function cubeFill() {
  const out = [];
  for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) {
    const c = [i - 0.5, j - 0.5, k - 0.5];
    for (const p of conePieces('cube', CUBE.vertices.map((v) => add(v, c)), CUBE.faces, c)) out.push({ ...p, tone: (i + j + k) % 2, cell: out.length / 6 | 0 });
  }
  return out;
}

// (b) the octet cut up. The octahedron of corners ±e_i and the two tetrahedra on its faces x + y + z = ±1 make the 60° rhombohedron
// with edges (0, 1, 1), (1, 0, 1), (1, 1, 0), one cell of the face-centred cubic lattice; the cells fill space by those translations.
// Edge √2 here, scaled to edge 1.
const OCTA_V = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
const OCTA_F = [[0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4], [2, 0, 5], [1, 2, 5], [3, 1, 5], [0, 3, 5]];
const TET_UP = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]], TET_F = [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]];
export const OCTET_CELL_EDGES = [[0, 1, 1], [1, 0, 1], [1, 1, 0]];
function octetCell(c) {
  const s = 1 / Math.SQRT2, at = (v) => scale(add(v, c), s);
  return [
    ...conePieces('octahedron', OCTA_V.map(at), OCTA_F),
    ...conePieces('tetrahedron', TET_UP.map(at), TET_F),
    ...conePieces('tetrahedron', TET_UP.map((v) => at(scale(v, -1))), TET_F),
  ];
}
function octetFill() {
  const out = [], [a, b, c] = OCTET_CELL_EDGES;
  for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) {
    const o = add(add(scale(a, i - 0.5), scale(b, j - 0.5)), scale(c, k - 0.5)), cell = (i * 2 + j) * 2 + k;
    for (const p of octetCell(o)) out.push({ ...p, tone: p.kind === 'octahedron' ? 0 : 1, cell });
  }
  return out;
}

// (c) the golden fix: the Polyhedraverse kit 'antonius.block' as it is, each piece its shape turned and moved into place.
function goldenFill() {
  const kit = KITS13[GOLDEN_KIT], centre = mean(kit.cells.flat());
  return kit.entries.map((e, n) => {
    const S = POLYHEDRA[e.shape], V = S.vertices.map((v) => sub(add(rotate(v, e.quaternion), e.position), centre));
    const kind = e.shape === 'ANTONIUS' ? 'antonius' : 'icosahedron';
    return { kind, faces: S.faces.map((f) => f.map((i) => V[i])), axis: norm(mean(V)), tone: kind === 'antonius' ? 1 : 0, cell: n / 3 | 0 };
  });
}
export function goldenCells() {
  const kit = KITS13[GOLDEN_KIT], centre = mean(kit.cells.flat());
  return kit.cells.map((c) => c.map((v) => sub(v, centre)));
}

export const FILL_KEYS = ['cube', 'octet', 'golden'];
const FILL_MAKERS = { cube: cubeFill, octet: octetFill, golden: goldenFill };
const fillCache = new Map();
export const fillPieces = (key) => { if (!fillCache.has(key)) fillCache.set(key, FILL_MAKERS[key]()); return fillCache.get(key); };

/** Volume of a closed piece (faces as polygons, counter-clockwise or all clockwise from outside). */
export function pieceVolume(p) {
  let v = 0;
  for (const F of p.faces) for (let i = 1; i + 1 < F.length; i++) {
    const [a, b, c] = [F[0], F[i], F[i + 1]];
    v += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6;
  }
  return Math.abs(v);
}
