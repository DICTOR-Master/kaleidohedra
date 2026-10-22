// Polyhedraverse's shapes for the DICTO list (no rendering): a shape's edges as point pairs for the
// turning wireframes, and its name. From krp-core's registry (src/polyhedra).
import { getAnySpec } from '../krp-core/src/polyhedra/lookup.js';
import { polytope4D, polytopeTitle, polytopeWireframe } from '../krp-core/src/polyhedra/polytopes4d.js';
import { t } from './i18n.js';
import { getSettings } from './settings.js';

export function polyShapeEdges(id) {
  if (polytope4D(id)) { const w = polytopeWireframe(id); return w.edges.map(([a, b]) => [w.vertices[a], w.vertices[b]]); } // 4D polytopes (D5)
  const s = getAnySpec(id); // the star polyhedra too (D4)
  if (!s) return [];
  // a curved shape (the Reuleaux bodies): its seams, the curved creases between its patches
  if (s.curved) { const S = s.curved.seams, out = []; for (let i = 0; i < S.length; i += 6) out.push([[S[i], S[i + 1], S[i + 2]], [S[i + 3], S[i + 4], S[i + 5]]]); return out; }
  return s.edges.map(([a, b]) => [s.vertices[a], s.vertices[b]]);
}
// The Reuleaux Platonic Solids (DICTO 2026-10-21, #45) by the names Kaleidohedra's Reuleaux world gives them, in the chosen language.
export const polyShapeName = (id, L = getSettings().language) => (polytope4D(id) ? polytopeTitle(polytope4D(id))
  : getAnySpec(id)?.reuleaux ? t(`rl.name.${getAnySpec(id).reuleaux.key}`, L) : getAnySpec(id)?.name ?? id);
