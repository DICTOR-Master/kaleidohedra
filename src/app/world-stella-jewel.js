// The Stella–Jewel Lattice (direct request, 2026-10-08): DICTO Jewels (DJ, DICTO's name for the
// windows solid, DISCOVERIES #10) on the even cells and stella octangulas on the odd cells, filling
// space (study 10b). Views: both, or the DICTO Jewels alone (they meet face to face on all 12
// rhombi, leaving stella-shaped holes). The five-fold overlay adds the five window positions on each
// face, the cube's choice bright. The world itself is world-pair-lattice.js. Ported from
// Kaleidohedra (direct request, 2026-10-08), beside the Sunstar Lattice.
import {
  ekpWindowsSolid, roofFoldSolids, ROOF_FOLD_COLOURS as C, insideDragonJewel, insideStella, fiveWindowPositions, dogstarSolid, PHI,
} from '../krp-core/src/geometry-extensions/roof-fold.js';
import { OCTET_CLUSTERS, octetNetworkCells, kagomeNeighbourClusters } from './octet-cells.js';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { createPairLatticeWorld } from './world-pair-lattice.js';
import { storageKey } from './site.js';

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
    // Arrangements (arrangement: true) open from their own DICTO entries, each its colour scheme;
    // the rest are views of the lattice, offered in its panel.
    modes: [{ id: 'both', even: true, odd: true }, { id: 'jewels', even: true, odd: false }, { id: 'tetra', even: true, odd: false, cluster: 'tetra', arrangement: true, pieceColour: 0xd9a520, edgeColour: 0xfff0a0 }, { id: 'octa', even: true, odd: true, cluster: 'octa', arrangement: true, pieceColour: 0x8c5a2b }, { id: 'octet', even: true, odd: false, network: true, arrangement: true, pieceColour: 0xa9c4e8 }, { id: 'kagome', even: true, odd: false, cluster: 'kagome', network: 'kagome', arrangement: true, pieceColour: 0xd9a520 }, { id: 'chain', even: true, odd: false, chain: true }],
    // DICTO's clusters of DICTO Jewels (DICTO, 2026-10-09; krp-core DJ_TETRAHEDRAL_CLUSTER and
    // DJ_OCTAHEDRAL_CLUSTER), each placed whole (octet-cells.js).
    networkCells: octetNetworkCells,
    kagomeNeighbours: kagomeNeighbourClusters,
    // Each cluster drawn whole, as its krp-core shape (DICTO 2026-10-09: cohesive blocks).
    clusterBlocks: { tetra: POLYHEDRA.DJ_TETRAHEDRAL_CLUSTER, kagome: POLYHEDRA.DJ_TETRAHEDRAL_CLUSTER, octa: POLYHEDRA.DJ_OCTAHEDRAL_CLUSTER },
    clusters: OCTET_CLUSTERS,
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
