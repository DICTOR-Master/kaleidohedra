import { HEMI_RD_INTERFACE, hemiRdInterfaceFrame } from './app/lib/rvcmg/hemiRdInterface';
import { CATALAN_ADDITIONS } from './app/lib/polyhedra/catalan';
import { buildRdHemiSolid } from './app/lib/rvcmg/rdHemi';
const RD: any = (CATALAN_ADDITIONS as any).RHOMBIC_DODECAHEDRON;
const h = buildRdHemiSolid('X','X');
console.log(JSON.stringify({ hex: HEMI_RD_INTERFACE, frame: hemiRdInterfaceFrame(), rdv: RD.vertices, hemi: { v: h.spec.vertices, f: h.spec.faces } }));
