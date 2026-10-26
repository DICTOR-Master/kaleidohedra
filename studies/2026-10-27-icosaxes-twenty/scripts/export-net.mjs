// B patch (DICTO 2026-10-27: "render the cube8 network"): cube8 clusters (8 Icosaxes round an Unborn Axes) on the bcc anchor lattice
// (1,1,1) + <(2,2,-2), (2,-2,2), (-2,2,2)>; the middle cluster and its 8 neighbours, each Icosaxes written once (every one is shared by
// two clusters). Sites scaled by phi/2.
import { writeFileSync } from 'node:fs';
import { PHI, FLAT, pieceSurface, toPolygons } from '/home/dicto/k-mix/src/krp-core/src/polyhedra/golden-split.js';
const I = toPolygons(pieceSurface(true, Array(8).fill(FLAT))), U = toPolygons(pieceSurface(false, Array(8).fill(FLAT)));
const at = (n) => n.map((c) => (c * PHI) / 2);
const anchors = [[1, 1, 1], ...[-1, 1].flatMap((x) => [-1, 1].flatMap((y) => [-1, 1].map((z) => [1 + 2 * x, 1 + 2 * y, 1 + 2 * z])))];
const ico = new Map();
for (const a of anchors) for (const x of [-1, 1]) for (const y of [-1, 1]) for (const z of [-1, 1]) { const n = [a[0] + x, a[1] + y, a[2] + z]; ico.set(n.join(), n); }
const P = [...[...ico.values()].map((n) => ['icosaxes', I, n]), ...anchors.map((a) => ['unbornAxes', U, a])];
// N1: the pieces as they are; N2: each piece shrunk about its centre, with each cluster's cube drawn as 12 thin gold bars, so the
// corner-sharing shows.
const write = (file, shrink, frames) => {
  let s = '', base = 1;
  const put = (r, V, F, k) => { s += `o ${r}_${k}\n` + V.map((v) => `v ${v.join(' ')}`).join('\n') + '\n' + F.map((f) => 'f ' + f.map((i) => i + base).join(' ')).join('\n') + '\n'; base += V.length; };
  P.forEach(([r, M, n], k) => { const t = at(n); put(r, M.vertices.map((v) => v.map((x, i) => x * shrink + t[i])), M.faces, k); });
  if (frames) anchors.forEach((a, k) => {
    const C = [-1, 1].flatMap((x) => [-1, 1].flatMap((y) => [-1, 1].map((z) => at([a[0] + x, a[1] + y, a[2] + z]))));
    C.forEach((p, i) => C.forEach((q, j) => {
      const diff = [0, 1, 2].filter((m) => Math.abs(p[m] - q[m]) > 1e-9);
      if (j <= i || diff.length !== 1) return;
      const m = diff[0], w = 0.035;
      const lo = p.map((x, mm) => (mm === m ? Math.min(x, q[mm]) : x - w)), hi = p.map((x, mm) => (mm === m ? Math.max(x, q[mm]) : x + w));
      const V = [0, 1, 2, 3, 4, 5, 6, 7].map((b) => [0, 1, 2].map((mm) => ((b >> mm) & 1 ? hi[mm] : lo[mm])));
      put('frame', V, [[0, 2, 3, 1], [4, 5, 7, 6], [0, 1, 5, 4], [2, 6, 7, 3], [0, 4, 6, 2], [1, 3, 7, 5]], `${k}_${i}_${j}`);
    }));
  });
  writeFileSync(`${process.argv[2]}/${file}.obj`, s);
};
write('N1', 1, false); write('N2', 0.55, true);
console.log(anchors.length, 'clusters,', ico.size, 'Icosaxes (expected 9*8-8 = 64)');
