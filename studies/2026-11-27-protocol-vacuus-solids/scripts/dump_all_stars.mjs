// Dump every Star Cores shape's chain (the app's own code), both rules (t = 2 and t = phi) (27 Nov 2026, DICTO "yes please": which stars
// come closest to Vacuus-Solids). With Claude (Anthropic). Usage: node dump_all_stars.mjs <k-mix dir> > all.json
import path from 'node:path';
const KMIX = process.argv[2]; const imp = (p) => import(path.resolve(KMIX, p));
const { STAR_CORES_LIST, POLYHEDRA } = await imp('src/krp-core/src/polyhedra/index.js');
const G = await imp('src/app/star-cores-geometry.js');
const out = [];
for (const s of STAR_CORES_LIST) for (const T of ['2', 'phi']) {
  const spec = POLYHEDRA[s.id]; if (!spec) continue;
  let chain = null; try { chain = G.starCoresChain(spec, T); } catch (e) { continue; }
  if (!chain) continue;
  out.push({ D: s.D, name: s.name || s.label || s.key || '', t: T, turns: chain.turns.map((x, k) => ({ turn: k + 1,
    solid: { vertices: x.solid.vertices, faces: x.solid.faces }, tips: x.step.tips || null })) });
}
console.log(JSON.stringify(out));
