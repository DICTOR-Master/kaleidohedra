// B keyed (DICTO 2026-10-27: "try the keyed version"): the cube8 network patch with Dodecaxes at the 9 cluster centres. NK1: every
// Icosaxes a Lotus Jewel Axes (all 8 hexagons dented). NK2: dented only towards its two cluster centres (opposite hexagons), the
// mirrored Tricap keyed outward on the 6 hexagons facing empty sites. Pieces as triangle meshes (JSON for the overlap check) and OBJ.
import { writeFileSync } from 'node:fs';
import { PHI, SIGNS, INTO_BIG, INTO_SMALL, pieceSurface } from '/home/dicto/k-mix/src/krp-core/src/polyhedra/golden-split.js';
const at = (n) => n.map((c) => (c * PHI) / 2);
const anchors = [[1, 1, 1], ...[-1, 1].flatMap((x) => [-1, 1].flatMap((y) => [-1, 1].map((z) => [1 + 2 * x, 1 + 2 * y, 1 + 2 * z])))];
const centre = new Set(anchors.map((a) => a.join()));
const ico = new Map();
for (const a of anchors) for (const s of SIGNS) { const n = a.map((c, i) => c + s[i]); ico.set(n.join(), n); }
const mesh = (tris, t) => { const V = [], idx = new Map(); const F = tris.map((tri) => tri.map((p) => { const q = p.map((x, i) => x + t[i]), k = q.map((x) => x.toFixed(9)).join(); if (!idx.has(k)) { idx.set(k, V.length); V.push(q); } return idx.get(k); })); return { V, F }; };
for (const name of ['NK1', 'NK2']) {
  const P = [];
  for (const n of ico.values()) {
    const states = SIGNS.map((s) => (name === 'NK1' || centre.has(n.map((c, i) => c + s[i]).join()) ? INTO_BIG : INTO_SMALL));
    const own = SIGNS.filter((s) => centre.has(n.map((c, i) => c + s[i]).join())).length;
    P.push({ role: name === 'NK1' ? 'lotusJewelAxes' : 'keyedOut', own, ...mesh(pieceSurface(true, states), at(n)) });
  }
  for (const a of anchors) P.push({ role: 'dodecaxes', ...mesh(pieceSurface(false, Array(8).fill(INTO_BIG)), at(a)) });
  let s = '', base = 1;
  P.forEach((p, k) => { s += `o ${p.role}_${k}\n` + p.V.map((v) => `v ${v.join(' ')}`).join('\n') + '\n' + p.F.map((f) => 'f ' + f.map((i) => i + base).join(' ')).join('\n') + '\n'; base += p.V.length; });
  writeFileSync(`${process.argv[2]}/${name}.obj`, s);
  writeFileSync(`${process.argv[2]}/${name}.json`, JSON.stringify(P.map((p) => ({ role: p.role, vertices: p.V, tris: p.F }))));
  const owns = [...new Set(P.filter((p) => p.own !== undefined).map((p) => p.own))];
  console.log(name, P.length, 'pieces; cluster centres facing each Icosaxes:', owns.join(' or '));
}
