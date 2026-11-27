// Dump the Star Cores world's chain (the app's own code) for one shape: for each turn the solid S (corners, faces) and the star's spike
// tips (DICTO 27 Nov: "turn 4 star ... turn 5 star same turn 3 star, turn 1 star looks too spikey"). With Claude (Anthropic).
// Usage (from a k-mix tree): node dump_star_turns.mjs <k-mix dir> <shape id, default D109> <t: 2 | phi> > out.json
import path from 'node:path';
const [, , KMIX, SHAPE = 'D109', T = '2'] = process.argv;
const imp = (p) => import(path.resolve(KMIX, p));
const { STAR_CORES_LIST, POLYHEDRA } = await imp('src/krp-core/src/polyhedra/index.js');
const G = await imp('src/app/star-cores-geometry.js');
const spec = G.findStarCoresShape(STAR_CORES_LIST, SHAPE);
if (!spec) { console.error('shape not found', SHAPE); process.exit(2); }
const chain = G.starCoresChain(POLYHEDRA[spec.id], T);
const out = { shape: SHAPE, name: spec.name || spec.label || spec.key || '', t: chain.t, turns: chain.turns.map((x, k) => ({
  turn: k + 1, solid: { vertices: x.solid.vertices, faces: x.solid.faces }, tips: x.step.tips || null,
  halo: x.step.halo ? { vertices: x.step.halo.vertices, faces: x.step.halo.faces } : null,
  star: x.step.star ? { vertices: x.step.star.vertices, faces: x.step.star.faces } : null })) };
console.log(JSON.stringify(out));
