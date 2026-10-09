// Polyhedraverse's shapes for the DICTO list (no rendering): a shape's edges as point pairs for the
// turning wireframes, and its name. From krp-core's registry (src/polyhedra).
import { getAnySpec } from '../krp-core/src/polyhedra/lookup.js';
import { polytope4D, polytopeTitle, polytopeWireframe } from '../krp-core/src/polyhedra/polytopes4d.js';

export function polyShapeEdges(id) {
  if (polytope4D(id)) { const w = polytopeWireframe(id); return w.edges.map(([a, b]) => [w.vertices[a], w.vertices[b]]); } // 4D polytopes (D5)
  const s = getAnySpec(id); // the star polyhedra too (D4)
  if (!s) return [];
  return s.edges.map(([a, b]) => [s.vertices[a], s.vertices[b]]);
}
export const polyShapeName = (id) => (polytope4D(id) ? polytopeTitle(polytope4D(id)) : getAnySpec(id)?.name ?? id);
