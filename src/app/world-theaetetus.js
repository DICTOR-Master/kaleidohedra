// Theaetetus: a 3D+ world (DICTO 2026-10-15), named by DICTO after Theaetetus of Athens, by tradition the first to construct the
// icosahedron. The Cleo core grown to the DICTO Hecatodihedron: an icosahedron of edge 1 held exactly in the icosidodecahedron of edge 1
// by Cleo-Icos (an icosahedron's face pyramids), flat pentagonal pyramids and the tetrahedra X and Y, then the Spheres of Dharma layers
// scaled by 2/phi out to the Hecatodihedron, each Cleo-Ico fused with the dodecahedron's corner pyramid into one bipyramid (DICTO's
// choice). Geometry: theaetetus-data.js (scripts/build-theaetetus-data.py; studies/2026-10-15-icosa-star-hollow). Tools of the
// Multi-shell chains.
import DATA from './theaetetus-data.js';
import { createLayeredWorld } from './world-chains.js';

export function createTheaetetusWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'theaetetus', data: DATA, kinds: ['theaetetus'], prefix: 'theaetetus',
    glassRoles: { theaetetus: new Set(['ncap', 'nt1', 'nfru5']) }, defaultParts: { theaetetus: 'heca' } });
}

/** Points whose convex hull previews the world in the DICTO menu. */
export function theaetetusPreviewPoints() {
  return DATA.theaetetus.views.heca.flatMap((p) => p[1]);
}
