// The Stella–Jewel Lattice (direct request, 2026-10-08): DICTO Jewels (DJ, DICTO's name for the
// windows solid, DISCOVERIES #10) on the even cells and stella octangulas on the odd cells, filling
// space (study 10b). Views: both, or the DICTO Jewels alone (they meet face to face on all 12
// rhombi, leaving stella-shaped holes). The five-fold overlay adds the five window positions on each
// face, the cube's choice bright. The world itself is world-pair-lattice.js. Ported from
// Kaleidohedra (direct request, 2026-10-08), beside the Sunstar Lattice.
import {
  ekpWindowsSolid, roofFoldSolids, ROOF_FOLD_COLOURS as C, insideDragonJewel, insideStella, fiveWindowPositions, dogstarSolid, PHI,
} from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DJ_TETRA_OFFSETS, DJ_OCTA_TILING } from '../krp-core/src/polyhedra/stellaJewel.js';
import { createPairLatticeWorld } from './world-pair-lattice.js';
import { storageKey } from './site.js';

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
function dragonChain(DJ) {
  const k = 1 / PHI ** 3, S = roofFoldSolids();
  const at = (faces, s) => faces.map((f) => f.map((p) => p.map((c) => c * s)));
  return [
    { faces: S.cube.faces.map((f) => [f, C.cube]), opacity: 0.2 },
    { faces: S.stella.faces.map((f) => [f, C.stella]), opacity: 0.3 },
    { faces: dogstarSolid().map((f) => [f, C.dogstar]), opacity: 0.45 },
    { faces: at(S.dodeca.faces, k).map((f) => [f, C.dodeca]), opacity: 0.6 },
    { faces: [...at(DJ.rhombi, k).map((f) => [f, C.dodeca]), ...at(DJ.walls, k).map((f) => [f, 0xb8892a])], opacity: 1 },
  ];
}

export function createStellaJewelWorld(opts) {
  const DJ = ekpWindowsSolid();
  const five = fiveWindowPositions();
  return createPairLatticeWorld(opts, {
    storageKey: storageKey('stella-jewel'),
    panelId: 'worldstellajewel-panel',
    minimiser: 'stella-jewel',
    strings: 'dj',
    modes: [{ id: 'both', even: true, odd: true }, { id: 'jewels', even: true, odd: false }, { id: 'tetra', even: true, odd: false, cluster: 'tetra' }, { id: 'octa', even: true, odd: false, cluster: 'octa' }, { id: 'octet', even: true, odd: false, network: true }, { id: 'chain', even: true, odd: false, chain: true }],
    // DICTO's clusters of DICTO Jewels (DICTO, 2026-10-09; krp-core DJ_TETRAHEDRAL_CLUSTER and
    // DJ_OCTAHEDRAL_CLUSTER), each placed whole. Both fill space with stella octangulas, so the
    // clusters a site can belong to come from those packings and every Jewel is in exactly one:
    // tetrahedral, the four cells at an all-even anchor; octahedral, the six round an odd centre
    // on DJ_OCTA_TILING's lattice.
    // The octet network (DICTO, 2026-10-09): the clusters as the octet truss's cells, sharing Jewels.
    // A tetrahedral cell wherever the four Jewels round a cell corner are all there, an octahedral one
    // wherever the six round an odd cell are (its stella then hidden inside); edges join Jewels that
    // meet face to face.
    networkCells: (evens) => {
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
    },
    clusters: {
      tetra: (s) => {
        const anchor = s.map((c) => c - (((c % 2) + 2) % 2));
        return DJ_TETRA_OFFSETS.map((d) => anchor.map((c, i) => c + d[i]));
      },
      octa: (s) => {
        const o = AXES6.map((d) => s.map((c, i) => c + d[i])).find(onOctaLattice);
        return AXES6.map((d) => o.map((c, i) => c + d[i]));
      },
    },
    evenFaces: [...DJ.rhombi.map((f) => [f, C.dodeca]), ...DJ.walls.map((f) => [f, 0xb8892a])],
    oddFaces: roofFoldSolids().stella.faces.map((f) => [f, C.stella]),
    insideEven: insideDragonJewel,
    insideOdd: insideStella,
    // Across a face to the stella; DICTO Jewel to DICTO Jewel across the rhombi.
    touches: (s, d) => Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]) === 1 || (((s[0] + s[1] + s[2]) % 2) + 2) % 2 === 0,
    overlay: { faint: five.filter((x) => !x.chosen).map((x) => x.rhombus), bright: five.filter((x) => x.chosen).map((x) => x.rhombus) },
    brightColor: C.dodeca,
    holePrompt: true,
    // The Dragon chain (study 12a, direct request 2026-10-08): inside each DICTO Jewel, every step
    // touching, its cube, stella octangula, Dogstar, the Dogstar's 1/phi^3 core dodecahedron and the
    // next DICTO Jewel 1/phi^3 the size.
    chainLayers: dragonChain(DJ),
  });
}
