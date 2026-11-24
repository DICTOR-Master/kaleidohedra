import { RVCMG_V2_CONNECTOR_ADDITIONS } from './app/lib/polyhedra/miscellaneous/rvcmg-connectors-v2/index';
import { ARCHIVED_RVCMG_CONNECTOR_ADDITIONS } from './app/lib/polyhedra/miscellaneous/index';
import { CATALAN_ADDITIONS } from './app/lib/polyhedra/catalan';
const out: any = {};
for (const [k, s] of Object.entries({ ...RVCMG_V2_CONNECTOR_ADDITIONS, ...ARCHIVED_RVCMG_CONNECTOR_ADDITIONS })) {
  out[k] = { name: (s as any).name, vertices: (s as any).vertices, faces: (s as any).faces };
}
const cat: any = {};
for (const id of ['RHOMBIC_DODECAHEDRON','RHOMBIC_TRIACONTAHEDRON','DELTOIDAL_ICOSITETRAHEDRON','DELTOIDAL_HEXECONTAHEDRON']) {
  const s: any = (CATALAN_ADDITIONS as any)[id]; cat[id] = { vertices: s.vertices, face0: s.faces[0] };
}
console.log(JSON.stringify({ pieces: out, catalan: cat }));
