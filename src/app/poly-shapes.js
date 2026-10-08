// Polyhedraverse's shapes for the DICTO list (no rendering): a shape's edges as point pairs for the
// turning wireframes, and its name. From krp-core's registry (src/polyhedra).
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';

export function polyShapeEdges(id) {
  const s = POLYHEDRA[id];
  if (!s) return [];
  return s.edges.map(([a, b]) => [s.vertices[a], s.vertices[b]]);
}
export const polyShapeName = (id) => POLYHEDRA[id]?.name ?? id;
