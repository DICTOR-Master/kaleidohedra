// A: the icosahedral Hexa block (DICTO 2026-10-27): 8 icosahedra (A1) or 8 Lotus Jewels (A2) at n in {0,2}^3, the void dodecahedron
// at (1,1,1) (Unborn + 8 Tricaps, each Tricap also in its icosahedron: they pass through each other, as the Jewels in the Hexa), and
// the 2 AXE on each of the block's 6 faces. Writes one OBJ per variant, a group per piece, sites scaled by phi/2.
import { writeFileSync } from 'node:fs';
const { default: O } = await import('/home/dicto/k-mix/src/app/octet-data.js');
const C = O.cells, PHI = O.phi, at = (n) => n.map((c) => (c * PHI) / 2);
const put = (cell, t) => cell.map(([r, V, F]) => [r, V.map((v) => v.map((x, i) => x + t[i])), F]);
const ctr = (V) => V.reduce((t, v) => t.map((x, i) => x + v[i] / V.length), [0, 0, 0]);
const icoSites = [[0, 0, 0], [2, 0, 0], [0, 2, 0], [0, 0, 2], [2, 2, 0], [2, 0, 2], [0, 2, 2], [2, 2, 2]];
const mid = [1, 1, 1], AXE = [C.axeX, C.axeY, C.axeZ];
function block(kind) {
  const P = [];
  for (const n of icoSites) P.push(...put(kind === 'A1' ? C.oct.slice(0, 1) : C.lotusJewel, at(n)));
  P.push(...put(C.voidDodeca, at(mid)));
  for (let a = 0; a < 3; a++) for (const s of [0, 2]) {          // the face sites: mid with coordinate a set to 0 or 2
    const n = mid.map((c, i) => (i === a ? s : c)), pair = put(AXE[a], at(n));
    P.push(...pair);   // both AXE of the pair: they straddle the face, between the four icosahedra round it
  }
  return P;
}
for (const kind of ['A1', 'A2']) {
  const P = block(kind); let s = '', base = 1;
  P.forEach(([r, V, F], k) => { s += `o ${r}_${k}\n` + V.map((v) => `v ${v.join(' ')}`).join('\n') + '\n' + F.map((f) => 'f ' + f.map((i) => i + base).join(' ')).join('\n') + '\n'; base += V.length; });
  writeFileSync(`${process.argv[2]}/${kind}.obj`, s);
  console.log(kind, P.length, 'pieces:', Object.entries(P.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {})).map((e) => e.join(' ')).join(', '));
}
