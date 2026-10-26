// H1, H2 (DICTO 2026-10-27: "icosaxes and unborn axes"): Icosaxes (green) at n in {0,2}^3, sites scaled by phi/2 as the golden split;
// at the middle (1,1,1) an Unborn Axes (orange, H1: they meet face to face) or another Icosaxes (H2: passing through, as the Hexa).
import { writeFileSync } from 'node:fs';
import { PHI, FLAT, pieceSurface, toPolygons } from '/home/dicto/k-mix/src/krp-core/src/polyhedra/golden-split.js';
const solid = (big) => toPolygons(pieceSurface(big, Array(8).fill(FLAT)));
const I = solid(true), U = solid(false), at = (n) => n.map((c) => (c * PHI) / 2);
const corners = [[0, 0, 0], [2, 0, 0], [0, 2, 0], [0, 0, 2], [2, 2, 0], [2, 0, 2], [0, 2, 2], [2, 2, 2]];
for (const [name, mid] of [['H1', U], ['H2', I]]) {
  const P = [...corners.map((n) => ['icosaxes', I, at(n)]), [mid === U ? 'unbornAxes' : 'icosaxes', mid, at([1, 1, 1])]];
  let s = '', base = 1; const json = [];
  P.forEach(([r, M, t], k) => {
    const V = M.vertices.map((v) => v.map((x, i) => x + t[i]));
    s += `o ${r}_${k}\n` + V.map((v) => `v ${v.join(' ')}`).join('\n') + '\n' + M.faces.map((f) => 'f ' + f.map((i) => i + base).join(' ')).join('\n') + '\n';
    base += V.length; json.push({ role: r, vertices: V });
  });
  writeFileSync(`${process.argv[2]}/${name}.obj`, s); writeFileSync(`${process.argv[2]}/${name}.json`, JSON.stringify(json));
  console.log(name, P.length, 'pieces; faces per Icosaxes', I.faces.length, 'Unborn Axes', U.faces.length);
}
