// The Queens' walls (DICTO 2026-11-16, part 1, "the Queens pulled apart"): pure maths, no three.js.
// DICTO · dictospheres.com
// Both Queens from the exact models of the Queens world (white-queen-geometry.js, red-queen-geometry.js), seen along the same named
// directions (the White Queen's viewAt, as the stage slider since 2026-11-16), so nothing jumps between the worlds.
//   Cells: each cell as a pyramid from the centre (600 tetrahedral pyramids, 120 dodecahedral pyramids). Apart moves each pyramid out
//     along its own cell's 4D direction, then the picture is projected: the 4D twin of the Vacuus lens's Exploded view.
//   Sheets: the Vacuus of the heart kind, the 60 central sheets on the 60 mirrors of H4 (the plane through the centre perpendicular to a
//     White Queen corner, one per pair of opposite corners). The White Queen's 1200 triangles lie 20 to a mirror and the Red Queen's
//     720 pentagons 12 to a mirror (studies 2026-11-16-600cell-walls, walls.py and walls120.py): one wall system for both Queens.
//     Each sheet is the fan of the cones from the centre over its faces; Apart moves each sheet along its own normal (DICTO's cardboard
//     Vacuus: the sheets slide out of their slots, and at 0 they slot together into the Queen).
import * as WQG from './white-queen-geometry.js';
import * as RQG from './red-queen-geometry.js';

const EPS = 1e-9;
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const unit = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
const mean = (pts) => [0, 1, 2, 3].map((k) => pts.reduce((s, p) => s + p[k], 0) / pts.length);

export const QW_QUEENS = ['white', 'red'];
export const QW_MODES = ['cells', 'sheets'];
export const QW_DIRECTIONS = WQG.DIRECTIONS;
/** The queens' corners (4D) and radii: the White Queen at radius 2, the Red Queen built from her cells' centres. */
export const QW_VERTICES = { white: WQG.VERTICES, red: RQG.VERTICES };
export const QW_RADIUS = { white: 2, red: RQG.RADIUS };

/** The 60 mirrors: unit normals, one per pair of opposite White Queen corners (the first nonzero coordinate positive). */
export const MIRRORS = WQG.VERTICES.filter((v) => { const k = v.findIndex((x) => Math.abs(x) > EPS); return v[k] > 0; }).map(unit);

/** Cells: { corners (indices), faces (corner loops), dir (unit 4D direction of the cell's centre) } per queen. */
export const QW_CELLS = {
  white: WQG.CELLS.map((c) => ({ corners: c, faces: [[c[0], c[1], c[2]], [c[0], c[1], c[3]], [c[0], c[2], c[3]], [c[1], c[2], c[3]]], dir: unit(mean(c.map((i) => WQG.VERTICES[i]))) })),
  red: RQG.CELLS.map((c, ci) => ({ corners: c.corners, faces: RQG.cellFaces(ci), dir: unit(mean(c.corners.map((i) => RQG.VERTICES[i]))) })),
};

/** The faces of each queen that lie in a mirror: the White Queen's triangles, the Red Queen's pentagons (corner loops). */
const FACES = { white: WQG.TRIANGLES, red: RQG.PENTAGONS };
/** Sheets: for each queen, 60 × { normal, faces (loops in that mirror) }; the same 60 normals for both queens, in the same order. */
export const QW_SHEETS = Object.fromEntries(QW_QUEENS.map((q) => {
  const V = QW_VERTICES[q];
  return [q, MIRRORS.map((n) => ({ normal: n, faces: FACES[q].filter((f) => f.every((i) => Math.abs(dot(V[i], n)) < EPS)) }))];
}));

/** The view: the White Queen's named direction (frame of three 4D axes) and its turning, as the Queens world. */
export const qwView = (dir) => WQG.viewAt(dir, dir, 0);

/**
 * The pieces of a queen in a mode, projected along a frame and pulled apart by `apart` (0..1, in units of the queen's radius):
 * [{ faces: [[3D points]], struts: [[3D, 3D]] (centre to each corner), offset: 3D }]. Pure: the picture is P(x) + apart · R · P(d).
 */
export function qwPieces(queen, mode, frame, apart) {
  const V = QW_VERTICES[queen], R = QW_RADIUS[queen], pr = (x) => frame.map((f) => dot(x, f));
  const P = V.map(pr);
  const list = mode === 'cells' ? QW_CELLS[queen].map((c) => ({ dir: c.dir, faces: c.faces, corners: c.corners })) : QW_SHEETS[queen].map((s) => ({ dir: s.normal, faces: s.faces, corners: [...new Set(s.faces.flat())] }));
  return list.map((p) => {
    const o = pr(p.dir).map((x) => x * apart * R), at = (i) => P[i].map((x, k) => x + o[k]);
    return { offset: o, faces: p.faces.map((f) => f.map(at)), struts: p.corners.map((i) => [o, at(i)]) };
  });
}
