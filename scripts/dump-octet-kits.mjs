// The DICTO Icosahedral Octet's kits for Polyhedraverse (DICTO 2026-10-13): the octahedron and tetrahedron cells and two blocks, from
// the world's own views, each piece listed from the centre out. Usage: node scripts/dump-octet-kits.mjs > octet-kits-raw.json
import { OCTET_VIEWS as V } from '../src/app/world-octet.js';
const mid = (P) => [0, 1, 2].map((k) => P.reduce((t, p) => t + p[k], 0) / P.length);
const outward = (list) => [...list].sort((x, y) => Math.hypot(...mid(x[1])) - Math.hypot(...mid(y[1])));
process.stdout.write(JSON.stringify({ octet: {
  octahedron: outward(V.allIco.views.octahedron),
  tetrahedron: outward(V.allIco.views.tetrahedron),
  octetBlock: outward(V.caps.views.network(2)),
  allIcoBlock: outward(V.allIco.views.network(1)),
} }));
