// Polyhedraverse's shapes for the DICTO list (no rendering): a shape's edges as point pairs for the
// turning wireframes, and its name. From krp-core's registry (src/polyhedra).
import { getAnySpec } from '../krp-core/src/polyhedra/lookup.js';

export function polyShapeEdges(id) {
  const s = getAnySpec(id); // the star polyhedra too (D4)
  if (!s) return [];
  return s.edges.map(([a, b]) => [s.vertices[a], s.vertices[b]]);
}
export const polyShapeName = (id) => getAnySpec(id)?.name ?? id;
