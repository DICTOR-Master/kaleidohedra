// DICTO's octet structure (DICTO, 2026-10-09), shared by the pair lattices whose even cells hold one
// piece and odd cells another (Stella–Jewel: DICTO Jewels and stellas; Sunstar: dodecahedra and
// Dogstars): the even pieces' clusters, and those clusters as the cells of the octet truss.
// - Clusters, each placed whole: tetrahedral (the four even cells round a cell corner) and
//   octahedral (the six round an odd cell, its odd piece then hidden inside). Both fill space with
//   the odd pieces, so a site's cluster comes from those packings and every even piece is in exactly
//   one: tetrahedral at all-even anchors, octahedral on krp-core's DJ_OCTA_TILING lattice (checked in
//   krp-core's verify-dicto-jewel-cluster.mjs and verify-sunstar-cluster.mjs).
// - The octet network: sharing pieces, each complete cluster drawn as its truss cell.
import { DJ_TETRA_OFFSETS, DJ_OCTA_TILING } from '../krp-core/src/polyhedra/stellaJewel.js';

const AXES6 = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
// Is the odd cell o a centre of the octahedral clusters' packing (origin + an integer combination
// of the basis)?
function onOctaLattice(o) {
  const [a, b, c] = DJ_OCTA_TILING.basis, v = o.map((x, i) => x - DJ_OCTA_TILING.origin[i]);
  const det = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);
  // Cramer's rule: the coordinates of v in the basis must all be whole numbers.
  const col = (r0, r1, r2) => r0[0] * (r1[1] * r2[2] - r1[2] * r2[1]) - r0[1] * (r1[0] * r2[2] - r1[2] * r2[0]) + r0[2] * (r1[0] * r2[1] - r1[1] * r2[0]);
  return [col(v, b, c), col(a, v, c), col(a, b, v)].every((n) => n % det === 0);
}

export const OCTET_CLUSTERS = {
  tetra: (s) => {
    // s = anchor + one of (0,0,0), (1,1,0), (1,0,1), (0,1,1), the anchor all-even.
    const anchor = s.map((c) => c - (((c % 2) + 2) % 2));
    return DJ_TETRA_OFFSETS.map((d) => anchor.map((c, i) => c + d[i]));
  },
  octa: (s) => {
    const o = AXES6.map((d) => s.map((c, i) => c + d[i])).find(onOctaLattice);
    return AXES6.map((d) => o.map((c, i) => c + d[i]));
  },
};

// The octet network: a tetrahedral cell wherever the four even pieces round a cell corner are all
// there, an octahedral one wherever the six round an odd cell are; edges join neighbours.
// The octet network (DICTO, 2026-10-09): the clusters as the octet truss's cells, sharing Jewels.
// A tetrahedral cell wherever the four Jewels round a cell corner are all there, an octahedral one
// wherever the six round an odd cell are (its stella then hidden inside); edges join Jewels that
// meet face to face.
export function octetNetworkCells(evens) {
  const has = new Set(evens.map((s) => s.join()));
  const triangles = [], seen = new Set();
  const add = (k, tris, colour) => { if (seen.has(k)) return; seen.add(k); for (const t of tris) triangles.push({ sites: t, colour }); };
  for (const s of evens) {
    for (const dx of [-1, 0]) for (const dy of [-1, 0]) for (const dz of [-1, 0]) {
      const corner = [s[0] + dx, s[1] + dy, s[2] + dz];
      const around = [];
      for (const a of [0, 1]) for (const b of [0, 1]) for (const c of [0, 1]) around.push([corner[0] + a, corner[1] + b, corner[2] + c]);
      const four = around.filter((c) => (((c[0] + c[1] + c[2]) % 2) + 2) % 2 === 0);
      if (four.every((c) => has.has(c.join()))) add(`t${corner.join()}`, [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]].map((ix) => ix.map((i) => four[i])), 0xffc857);
    }
    for (const d of AXES6) {
      const o = s.map((c, i) => c + d[i]);
      const six = AXES6.map((e) => o.map((c, i) => c + e[i]));
      if (!six.every((c) => has.has(c.join()))) continue;
      const [xp, xm, yp, ym, zp, zm] = six;
      const tris = [];
      for (const X of [xp, xm]) for (const Y of [yp, ym]) for (const Z of [zp, zm]) tris.push([X, Y, Z]);
      add(`o${o.join()}`, tris, 0x7cc4ff);
    }
  }
  const edges = [];
  for (const s of evens) for (const d of [[1, 1, 0], [1, -1, 0], [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]]) {
    const n = s.map((c, i) => c + d[i]);
    if (has.has(n.join())) edges.push([s, n]);
  }
  return { triangles, edges };
}
