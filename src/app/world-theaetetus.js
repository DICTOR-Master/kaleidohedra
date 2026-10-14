// Theaetetus: a 3D+ world (DICTO 2026-10-15), named by DICTO after Theaetetus of Athens, by tradition the first to construct the
// icosahedron. The Cleo core grown to the DICTO Hecatodihedron in DICTO's 102 clean pieces: an icosahedron of edge 1 as its 20 Cleo-Icos,
// the dodecahedron round it as 20 columns (one per core face, cut from the centre through the core's edges), then the Spheres of Dharma
// layers scaled by 2/phi (12 twisted pentagonal frusta, 30 t1, 20 caps). The other versions stay in studies/2026-10-15-icosa-star-hollow.
// Geometry: theaetetus-data.js (scripts/build-theaetetus-data.py). Tools of the Multi-shell chains.
import DATA from './theaetetus-data.js';
import { createLayeredWorld } from './world-chains.js';

export function createTheaetetusWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'theaetetus', data: DATA, kinds: ['theaetetus'], prefix: 'theaetetus',
    glassRoles: { theaetetus: new Set(['ncap', 'nt1', 'nfru5']) }, defaultParts: { theaetetus: 'c102' } });
}

/** Points whose convex hull previews the world in the DICTO menu. */
export function theaetetusPreviewPoints() {
  return DATA.theaetetus.views.c102.flatMap((p) => p[1]);
}
