// Each app's logo solid, as wireframe edges for the welcome screen (KRP: one welcome, each app its
// own symbol; DICTO 2026-10-08, generic over the apps). Rhombiverse: the rhombic dodecahedron.
// Kaleidohedra: the regular-hexagon elongated dodecahedron (DISCOVERIES.md #5), lying with its long
// axis horizontal and a hexagon towards you, as in its logo.
import { convexHullFaces } from '../krp-core/src/geometry-extensions/roof-fold.js';

const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const unit = (a) => { const l = Math.hypot(...a); return a.map((c) => c / l); };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];

/** The zonohedron of some directions: its faces (polygons), scaled so the farthest corner is at 2. */
function zonohedronFaces(dirs) {
  const pts = [];
  for (let m = 0; m < 1 << dirs.length; m++) pts.push(dirs.reduce((acc, d, i) => acc.map((c, k) => c + ((m >> i) & 1 ? 0.5 : -0.5) * d[k]), [0, 0, 0]));
  const s = 2 / Math.max(...pts.map((p) => Math.hypot(...p)));
  return convexHullFaces(pts.map((p) => p.map((c) => c * s)));
}
function edgesOf(faces) {
  const seen = new Map();
  for (const f of faces) f.forEach((a, i) => {
    const b = f[(i + 1) % f.length];
    const key = [a, b].map((v) => v.map((c) => c.toFixed(5)).join()).sort().join('|');
    if (!seen.has(key)) seen.set(key, [a, b]);
  });
  return [...seen.values()];
}
/** Express edges in a view frame looking at `toward`, with `rightHint` as near screen-horizontal as it goes. */
function inView(edges, toward, rightHint) {
  const f = unit(toward);
  const right = unit(rightHint.map((c, i) => c - dot(rightHint, f) * f[i]));
  const up = cross(f, right).map((c) => -c);
  return edges.map((e) => e.map((v) => [dot(v, right), dot(v, up), dot(v, f)]));
}

// The RD: the zonohedron of the cube's four body diagonals.
const RD = edgesOf(zonohedronFaces([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]));
// The regular-hexagon ED: the four Bain directions (1, +-1, +-sqrt2)/2 and (1, 0, 0), long along x.
const R2 = Math.SQRT2;
const ED_FACES = zonohedronFaces([[1, 1, R2], [1, -1, -R2], [-1, 1, -R2], [-1, -1, R2]].map((v) => v.map((c) => c / 2)).concat([[1, 0, 0]]));
const HEX = ED_FACES.find((f) => f.length === 6);
const ED = inView(edgesOf(ED_FACES), HEX.reduce((a, p) => a.map((c, i) => c + p[i]), [0, 0, 0]), [1, 0, 0]);

/** edges: [[a, b], ...] (corners within radius 2); tilt (radians); spinFirst: spin about the
 *  screen's vertical, then tilt (Kaleidohedra), or tilt then spin (Rhombiverse). */
export const LOGOS = {
  rhombiverse: { edges: RD, tilt: 0.5, spinFirst: false, label: 'a rotating wireframe rhombic dodecahedron' },
  kaleidohedra: { edges: ED, tilt: 0.08, spinFirst: true, label: 'a wireframe regular-hexagon elongated dodecahedron, turning slowly' },
};
