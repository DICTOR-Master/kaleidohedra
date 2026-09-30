// Verifies Kaleidoverse's lattice shear (geometry-extensions/kaleido-lattice.js):
// plain FCC is the identity; the path's stop 2 turns the FCC rhombic
// dodecahedron into exactly DICTO's skewed RD (congruent: same distances
// between every pair of corners); every point on the path is a real cell.
import { rdRawVerts } from '../src/core/lattice.js';
import { dictoCellVerts } from '../src/geometry-extensions/dicto-fcc.js';
import { FCC_PARAMS, DICTO_PARAMS, PATH_RANGE, PATH_STOPS, paramsOnPath, paramsValid, shearMatrix, det3 } from '../src/geometry-extensions/kaleido-lattice.js';

let failures = 0;
const check = (label, ok) => { console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}`); if (!ok) failures++; };
const apply = (S, v) => S.map((r) => r[0] * v[0] + r[1] * v[1] + r[2] * v[2]);
const dists = (vs) => { const d = []; for (let i = 0; i < vs.length; i++) for (let j = i + 1; j < vs.length; j++) d.push(Math.hypot(vs[i][0] - vs[j][0], vs[i][1] - vs[j][1], vs[i][2] - vs[j][2])); return d.sort((a, b) => a - b); };

const I = shearMatrix(FCC_PARAMS);
check('plain FCC (slider 0) is the identity', I.every((r, i) => r.every((x, j) => Math.abs(x - (i === j ? 1 : 0)) < 1e-9)));
check('stop 2 is DICTO FCC', PATH_STOPS.find((s) => s.at === 2)?.name === 'DICTO FCC' && Object.keys(DICTO_PARAMS).every((k) => Math.abs(paramsOnPath(2)[k] - DICTO_PARAMS[k]) < 1e-9));
const S = shearMatrix(paramsOnPath(2));
const sheared = rdRawVerts(1).map((v) => apply(S, v));
const a = dists(sheared), b = dists(dictoCellVerts(1));
check("at stop 2 the FCC rhombic dodecahedron becomes DICTO's skewed RD exactly (all 91 corner distances match)", a.length === b.length && a.every((x, i) => Math.abs(x - b[i]) < 1e-9));
check(`volume at stop 2 is 0.8502 of FCC's (${det3(S).toFixed(4)})`, Math.abs(det3(S) - 0.850231) < 1e-4);
check(`every point on the path from ${PATH_RANGE[0]} to ${PATH_RANGE[1]} is a real cell`, Array.from({ length: 200 }, (_, i) => PATH_RANGE[0] + (i / 199) * (PATH_RANGE[1] - PATH_RANGE[0])).every((s) => paramsValid(paramsOnPath(s)) && det3(shearMatrix(paramsOnPath(s))) > 0));
check('just past the end of the path the cells collapse', !paramsValid(paramsOnPath(PATH_RANGE[1] + 0.2)));
check('the shear never spins the scene (symmetric matrix)', [paramsOnPath(2), paramsOnPath(-3), { a: 1.3, b: 0.8, c: 1.1, alpha: 80, beta: 50, gamma: 70 }].every((p) => { const M = shearMatrix(p); return M.every((r, i) => r.every((x, j) => Math.abs(x - M[j][i]) < 1e-9)); }));

console.log(failures === 0 ? '\nAll checks passed (0 failures).' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
