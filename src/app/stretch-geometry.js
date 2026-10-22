// DICTO stretched solids (the stretched dodecahedron, extended; DICTO 2026-10-22; paper #49, The Stretching Theorem): the convex hull of copies of the
// regular dodecahedron (Studies' frame: Euclid's cube at ±1, so edge 2/φ; its cube axes are the dodecahedron's two-fold axes
// through the roof ridges). Two caps: the copy moved along a direction (cube axis, DICTO's F11; face diagonal; body diagonal;
// five-fold axis). Three or four caps: copies at the corners of an equilateral triangle or a regular tetrahedron. The spacing
// is in edges: at 1 every edge of the hull is one edge long. Checked against the paper's study (2026-10-22-swept-dodecahedra).
// No three.js here, so the unit tests can run it.
import { roofFoldCell, convexHullFaces, PHI } from '../krp-core/src/geometry-extensions/roof-fold.js';

const unit = (v) => { const l = Math.hypot(...v); return v.map((c) => c / l); };
export const STRETCH_DIRECTIONS = ['cube', 'face', 'body', 'five'];
export const STRETCH_CAPS = [2, 3, 4];
// The five-fold axis: a face normal of this very dodecahedron (the face whose normal leans most to +z), from its own geometry.
const faceNormal = () => {
  const D = roofFoldCell().dodeca;
  const normals = convexHullFaces(D).map((f) => { const c = [0, 1, 2].map((a) => f.reduce((t, p) => t + p[a], 0) / f.length); return unit(c); });
  return normals.reduce((best, n) => (n[2] > best[2] ? n : best));
};
const DIRECTION = { cube: [1, 0, 0], face: [1, 1, 0], body: [1, 1, 1], five: faceNormal() };
const s = Math.SQRT1_2;
const CORNERS = { 3: [[0, 0, 0], [s, s, 0], [s, 0, s]], 4: [[0, 0, 0], [s, s, 0], [s, 0, s], [0, s, s]] };
const EDGE = 2 / PHI;   // one edge, in the frame's units

/** The caps' centres (frame units), centred on the origin. */
export function capCentres(spacing, direction = 'cube', caps = 2) {
  const P = (caps === 2 ? [[0, 0, 0], unit(DIRECTION[direction] ?? DIRECTION.cube)] : CORNERS[caps] ?? CORNERS[3]).map((p) => p.map((c) => c * spacing * EDGE));
  const mid = [0, 1, 2].map((a) => P.reduce((t, p) => t + p[a], 0) / P.length);
  return P.map((p) => p.map((c, a) => c - mid[a]));
}
/** The hull's faces (polygons, frame units). */
export function stretchedSolid(spacing, direction = 'cube', caps = 2) {
  const D = roofFoldCell().dodeca;
  return convexHullFaces(capCentres(spacing, direction, caps).flatMap((c) => D.map((p) => p.map((x, a) => x + c[a]))));
}
/** A face's kind, for its colour: pentagon, rhombus (any quadrilateral), long (a hexagon), triangle. */
export const faceKind = (f) => (f.length === 5 ? 'pentagon' : f.length === 4 ? 'rhombus' : f.length === 3 ? 'triangle' : 'long');

/** The five-fold axis used (for the tests). */
export const FIVE_FOLD = DIRECTION.five;
