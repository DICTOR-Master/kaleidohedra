// DICTO Dodeca: a 3D+ world (DICTO 2026-10-13), the dodecahedral twin of DICTO Icosa. The DICTO Dodeca-13 (#13), the DICTO-Star
// (#14) and DICTO's DICTO-ICOSA star (the DICTO-Star with a pyramid on each free face, and its hollow with the core icosahedron),
// with the tools of the Multi-shell chains. The single pieces stay in Polyhedraverse's catalogue (DICTO's pieces); this world
// shows them assembled. Geometry: krp-core's Dodeca-13 parts and dodeca-data.js (scripts/build-dodeca-data.py).
import { DODECA13_PARTS } from '../krp-core/src/polyhedra/dodeca13.js';
import STAR_DATA from './dodeca-data.js';
import { createLayeredWorld } from './world-chains.js';

const parts13 = DODECA13_PARTS.DICTO_DODECA13;
const conv = (list) => list.map((p) => [p.role, p.vertices, p.faces]);
const DATA = {
  dodeca13: { views: { open: conv(parts13.pieces.filter((p) => p.role === 'dodeca' || p.role === 'centre')), pieces: conv(parts13.pieces),
    units: conv(parts13.units), stars: conv(parts13.stars) } },
  star: STAR_DATA.star,
  icosaStar: STAR_DATA.icosaStar,
};

export function createDodecaWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'dodeca', data: DATA, kinds: ['dodeca13', 'star', 'icosaStar'], prefix: 'dodeca',
    glassRoles: { dodeca13: new Set(['dodeca', 'centre']), star: new Set(['centre', 'dodeca']), icosaStar: new Set(['dodeca', 'j63']) },
    defaultParts: { dodeca13: 'pieces', star: 'star', icosaStar: 'pyramids' } });
}

/** Points whose convex hull previews a shape in the DICTO menu. */
export function dodecaPreviewPoints(kind) {
  const views = DATA[kind]?.views;
  return views ? Object.values(views)[0].flatMap((p) => p[1]) : [];
}
