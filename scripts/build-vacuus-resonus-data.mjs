// Builds data/vacuus-resonus-catalogue.json (Polyhedraverse's Vacuus and Resonus view) from the exact Vacuus/Resonus
// catalogue (catalogue-all.json of the 2026-11-24 catalogue study), keyed
// by krp-core's shape ids. Usage:
//   node scripts/build-vacuus-resonus-data.mjs path/to/catalogue-all.json
// Only polyhedra this app's registry holds are kept (the catalogue's
// bipyramids and trapezohedra n = 3-12 and the prisms/antiprisms past
// n = 10 are not in the registry; the 4-gonal prism is the cube and the
// 3-gonal antiprism the octahedron).
import { readFileSync, writeFileSync } from 'node:fs';

const src = process.argv[2];
if (!src) throw new Error('usage: node scripts/build-vacuus-resonus-data.mjs catalogue-all.json');
const rows = JSON.parse(readFileSync(src, 'utf8'));

const PLATONIC = { tetrahedron: 'D4', cube: 'CUBE', octahedron: 'D8', dodecahedron: 'DODECAHEDRON', icosahedron: 'D20' };
// Johnson polyhedra the registry files under the deltahedra.
const JOHNSON_ALIAS = { 12: 'D6', 13: 'D10', 17: 'D16', 51: 'D14', 84: 'D12' };

function card(c) {
  const sph = (a) => [a.sphere_V, a.sphere_E, a.regions];
  return {
    V: c.V, E: c.E, F: c.F,
    mirrors: c.mirrors,
    vacuus: {
      plates: c.vacuus_plates, full: c.vacuus_full, shared: c.vacuus_shared, single: c.vacuus_single,
      kind: c.vacuus_kind, onMirrors: c.vacuus_on_mirrors,
      sphere: sph(c.vacuus_arr), simplicial: c.vacuus_arr.simplicial,
    },
    resonus: {
      planes: c.resonus_planes, twoFaces: c.resonus_two_faces, oneFace: c.resonus_one_face,
      onMirrors: c.resonus_on_mirrors,
      sphere: sph(c.resonus_arr), simplicial: c.resonus_arr.simplicial,
    },
    both: c.both,
  };
}

const out = {};
for (const r of rows) {
  let id = null;
  if (r.family === 'Platonic') id = PLATONIC[r.name];
  else if (r.family === 'Archimedean' || r.family === 'Catalan') id = r.name.toUpperCase().replaceAll(' ', '_');
  else if (r.family === 'prism' || r.family === 'antiprism') {
    const n = parseInt(r.name, 10);
    const lo = r.family === 'prism' ? 5 : 4;
    if ((n >= lo || (r.family === 'prism' && n === 3)) && n <= 10) id = `${r.family.toUpperCase()}_${n}`;
  } else if (r.family === 'Johnson') id = JOHNSON_ALIAS[r.J] ?? r.name;
  if (!id) continue;
  if (out[id]) throw new Error(`duplicate ${id}`);
  out[id] = r.family === 'Johnson'
    ? { family: 'Johnson', name: r.name, sameCentre: r.same_centre, corner: card(r.corner), volume: card(r.volume) }
    : { family: r.family, name: r.name, corner: card(r) };
}
writeFileSync(new URL('../data/vacuus-resonus-catalogue.json', import.meta.url), JSON.stringify(out) + '\n');
console.log(Object.keys(out).length, 'polyhedra written');
