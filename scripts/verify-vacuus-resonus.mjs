// Polyhedraverse's Vacuus and Resonus view computes its planes in the app from each polyhedron's own corners
// (src/app/vacuus-resonus.js). This checks every count against the exact catalogue (data/vacuus-resonus-catalogue.json, from the
// study 2026-11-24-vacuus-resonus-catalogue) for every polyhedron it covers, about both centres for the Johnson polyhedra.
import { readFileSync } from 'node:fs';
import { getAnySpec } from '../src/krp-core/src/polyhedra/lookup.js';
import { analyse, cornerCentroid, volumeCentroid } from '../src/app/vacuus-resonus.js';

const CATALOGUE = JSON.parse(readFileSync(new URL('../data/vacuus-resonus-catalogue.json', import.meta.url), 'utf8'));
let failures = 0, checks = 0;
function eq(got, want, msg) {
  checks++;
  if (JSON.stringify(got) !== JSON.stringify(want)) { failures++; console.error(`FAIL: ${msg}: app ${JSON.stringify(got)}, catalogue ${JSON.stringify(want)}`); }
}
function check(id, spec, which, centre, card) {
  const r = analyse(spec, centre), k = r.counts, tag = `${id} (${which})`;
  eq([spec.vertices.length, spec.edges.length, spec.faces.length], [card.V, card.E, card.F], `${tag} V/E/F`);
  eq(r.mirrors, card.mirrors, `${tag} mirrors`);
  eq([k.plates, k.full, k.shared, k.single], [card.vacuus.plates, card.vacuus.full, card.vacuus.shared, card.vacuus.single], `${tag} Vacuus plates full/shared/single`);
  eq(k.kind, card.vacuus.kind, `${tag} kind`);
  eq(k.vacuusOnMirrors, card.vacuus.onMirrors, `${tag} Vacuus plates on mirrors`);
  eq([k.vacuusSphere.V, k.vacuusSphere.E, k.vacuusSphere.regions], card.vacuus.sphere, `${tag} Vacuus V/E/regions`);
  eq(k.vacuusSphere.simplicial, card.vacuus.simplicial, `${tag} Vacuus simplicial`);
  eq([k.resonusPlanes, k.twoFaces, k.oneFace], [card.resonus.planes, card.resonus.twoFaces, card.resonus.oneFace], `${tag} Resonus planes two/one face`);
  eq(k.resonusOnMirrors, card.resonus.onMirrors, `${tag} Resonus planes on mirrors`);
  eq([k.resonusSphere.V, k.resonusSphere.E, k.resonusSphere.regions], card.resonus.sphere, `${tag} Resonus V/E/regions`);
  eq(k.resonusSphere.simplicial, card.resonus.simplicial, `${tag} Resonus simplicial`);
  eq(k.both, card.both, `${tag} R∩V`);
  // Every plate and plane is drawn as a slice polygon of the polyhedron.
  eq(r.plates.every((p) => p.slice.length >= 3) && r.resonus.every((p) => p.slice.length >= 3), true, `${tag} every plane has a slice polygon`);
}
let n = 0;
for (const [id, entry] of Object.entries(CATALOGUE)) {
  const spec = getAnySpec(id);
  if (!spec) { failures++; console.error(`FAIL: ${id} not in the registry`); continue; }
  n++;
  check(id, spec, 'corner centroid', cornerCentroid(spec), entry.corner);
  if ('volume' in entry) check(id, spec, 'volume centroid', volumeCentroid(spec), entry.volume);
}
console.log(`${n} polyhedra, ${checks} checks, ${failures} failures`);
if (n !== 137) { console.error(`FAIL: expected 137 catalogue polyhedra in the registry, found ${n}`); failures++; }
process.exit(failures ? 1 : 0);
