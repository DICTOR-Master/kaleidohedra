// K1, K2 (DICTO 2026-10-27: "try the keyed Lotus Jewel Axes version"). Corner pieces (big, golden split) at n in {0,2}^3, a Dodecaxes
// (small, every hexagon keyed into the big piece) at the middle. K1: corners are Lotus Jewel Axes (every hexagon dented). K2: the
// hexagon facing the middle dented (the Dodecaxes' key fills it), the 7 outer hexagons keyed outward (the mirrored Tricap, INTO_SMALL),
// as the Hexa's outward roofs. Triangle meshes (pieces need not be convex), sites scaled by phi/2.
import { writeFileSync } from 'node:fs';
import { PHI, SIGNS, INTO_BIG, INTO_SMALL, pieceSurface } from '/home/dicto/k-mix/src/krp-core/src/polyhedra/golden-split.js';
const at = (n) => n.map((c) => (c * PHI) / 2);
const corners = [[0, 0, 0], [2, 0, 0], [0, 2, 0], [0, 0, 2], [2, 2, 0], [2, 0, 2], [0, 2, 2], [2, 2, 2]];
const inward = (n) => SIGNS.findIndex((s) => s.every((x, i) => x === Math.sign(1 - n[i])));
const variants = {
  K1: () => corners.map((n) => ['lotusJewelAxes', pieceSurface(true, Array(8).fill(INTO_BIG)), n]),
  K2: () => corners.map((n) => ['keyedOut', pieceSurface(true, SIGNS.map((_, i) => (i === inward(n) ? INTO_BIG : INTO_SMALL))), n]),
};
for (const [name, f] of Object.entries(variants)) {
  const P = [...f(), ['dodecaxes', pieceSurface(false, Array(8).fill(INTO_BIG)), [1, 1, 1]]];
  let s = '', base = 1; const json = [];
  P.forEach(([r, tris, n], k) => {
    const t = at(n), V = [], idx = new Map(), F = tris.map((tri) => tri.map((p) => { const q = p.map((x, i) => x + t[i]), key = q.map((x) => x.toFixed(9)).join(','); if (!idx.has(key)) { idx.set(key, V.length); V.push(q); } return idx.get(key); }));
    s += `o ${r}_${k}\n` + V.map((v) => `v ${v.join(' ')}`).join('\n') + '\n' + F.map((fc) => 'f ' + fc.map((i) => i + base).join(' ')).join('\n') + '\n';
    base += V.length; json.push({ role: r, vertices: V, tris: F });
  });
  writeFileSync(`${process.argv[2]}/${name}.obj`, s); writeFileSync(`${process.argv[2]}/${name}.json`, JSON.stringify(json));
  console.log(name, P.length, 'pieces');
}
