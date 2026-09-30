// Verifies Kaleidoverse's lattice shear (geometry-extensions/kaleido-lattice.js):
// plain FCC is the identity; the path's stop 2 turns the FCC rhombic
// dodecahedron into exactly DICTO's skewed RD (congruent: same distances
// between every pair of corners); every point on the path is a real cell.
import { rdRawVerts } from '../src/core/lattice.js';
import { dictoCellVerts } from '../src/geometry-extensions/dicto-fcc.js';
import { FCC_PARAMS, DICTO_PARAMS, PATH_RANGE, PATH_STOPS, paramsOnPath, paramsValid, shearMatrix, det3, cellDirections, cellCorners, cellQuality, pathTargets, RD_DIRECTIONS } from '../src/geometry-extensions/kaleido-lattice.js';
import { NEIGHBOR_OFFSETS } from '../src/core/lattice.js';
import { dictoMatrix, DICTO_DIRECTIONS } from '../src/geometry-extensions/dicto-fcc.js';

let failures = 0;
const check = (label, ok) => { console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}`); if (!ok) failures++; };
const apply = (S, v) => S.map((r) => r[0] * v[0] + r[1] * v[1] + r[2] * v[2]);
const dists = (vs) => { const d = []; for (let i = 0; i < vs.length; i++) for (let j = i + 1; j < vs.length; j++) d.push(Math.hypot(vs[i][0] - vs[j][0], vs[i][1] - vs[j][1], vs[i][2] - vs[j][2])); return d.sort((a, b) => a - b); };

const I = shearMatrix(FCC_PARAMS);
check('plain FCC (slider 0) is the identity', I.every((r, i) => r.every((x, j) => Math.abs(x - (i === j ? 1 : 0)) < 1e-9)));
check('stop 2 is DICTO FCC', PATH_STOPS.find((s) => s.at === 2)?.name === 'DICTO FCC' && Object.keys(DICTO_PARAMS).every((k) => Math.abs(paramsOnPath(2)[k] - DICTO_PARAMS[k]) < 1e-9));
const S = shearMatrix(paramsOnPath(2));
const M = dictoMatrix(1);
const gram = (f) => NEIGHBOR_OFFSETS.map((x) => NEIGHBOR_OFFSETS.map((y) => { const p = f(x), q = f(y); return (p[0] * q[0] + p[1] * q[1] + p[2] * q[2]).toFixed(6); }).join()).join('|');
check('the lattice at stop 2 is exactly DICTO FCC\'s (same 12 neighbour vectors, up to rotation)', gram((v) => apply(S, v)) === gram((v) => [0, 1, 2].map((i) => M[0][i] * v[0] + M[1][i] * v[1] + M[2][i] * v[2])));
const sameDirs = (A, B) => { const g = (D) => D.map((a) => D.map((b) => Math.abs(a[0] * b[0] + a[1] * b[1] + a[2] * b[2]).toFixed(6)).sort().join()).sort().join('|'); return g(A) === g(B); };
check("at stop 2 with Cell = 1 the cell is exactly DICTO's skewed RD (its four edge directions match DICTO's, lengths and angles, up to rotation and sign)", sameDirs(cellDirections(paramsOnPath(2), 1), DICTO_DIRECTIONS.map((g) => g.map((x) => (x * Math.sqrt(3)) / 2))));
check('at FCC with Cell = 1 the cell is the regular rhombic dodecahedron (all angles 70.5)', cellQuality(cellDirections(FCC_PARAMS, 1)).angles.every((x) => Math.abs(x - 70.5288) < 1e-3));
check('Cell = 0 is the RD simply sheared', cellDirections(paramsOnPath(2), 0).every((g, i) => { const h = apply(S, RD_DIRECTIONS[i]); return g.every((x, q) => Math.abs(x - h[q]) < 1e-12); }));
check('Cell = 1 always has four equal edges', [paramsOnPath(-3), paramsOnPath(1), paramsOnPath(4), { a: 1.2, b: 0.9, c: 1, alpha: 70, beta: 55, gamma: 65 }].every((p) => { const L = cellDirections(p, 1).map((g) => Math.hypot(...g)); return L.every((x) => Math.abs(x - L[0]) < 1e-9); }));
{
  // The Cell slider never changes the lattice: the 12 face translations stay the same for every t.
  const trans = (g) => { const T = []; for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) { const n = [g[i][1] * g[j][2] - g[i][2] * g[j][1], g[i][2] * g[j][0] - g[i][0] * g[j][2], g[i][0] * g[j][1] - g[i][1] * g[j][0]]; for (const sg of [1, -1]) T.push(g.reduce((c, gk, k) => (k === i || k === j ? c : c.map((x, q) => x + gk[q] * Math.sign(sg * (n[0] * gk[0] + n[1] * gk[1] + n[2] * gk[2])))), [0, 0, 0]).map((x) => x.toFixed(6)).join()); } return T.sort().join('|'); };
  const base = trans(cellDirections(paramsOnPath(2), 0));
  check('the Cell slider keeps the lattice: same 12 translations at every step from 0 to 1', Array.from({ length: 21 }, (_, i) => i / 20).every((t) => trans(cellDirections(paramsOnPath(2), t)) === base));
}
check('the regularity meter scores 1 at FCC and at DICTO FCC', Math.abs(cellQuality(cellDirections(paramsOnPath(0), 1)).score - 1) < 1e-9 && Math.abs(cellQuality(cellDirections(paramsOnPath(2), 1)).score - 1) < 1e-9);
{
  const T = pathTargets(1);
  check(`Find reaches FCC (0) and DICTO FCC (2) as regular cells (${T.length} targets on the path)`, T.some((e) => Math.abs(e.at) < 1e-3 && e.kind === 'regular cell') && T.some((e) => Math.abs(e.at - 2) < 1e-3 && e.kind === 'regular cell'));
}
check(`volume at stop 2 is 0.8502 of FCC's (${det3(S).toFixed(4)})`, Math.abs(det3(S) - 0.850231) < 1e-4);
check(`every point on the path from ${PATH_RANGE[0]} to ${PATH_RANGE[1]} is a real cell`, Array.from({ length: 200 }, (_, i) => PATH_RANGE[0] + (i / 199) * (PATH_RANGE[1] - PATH_RANGE[0])).every((s) => paramsValid(paramsOnPath(s)) && det3(shearMatrix(paramsOnPath(s))) > 0));
check('just past the end of the path the cells collapse', !paramsValid(paramsOnPath(PATH_RANGE[1] + 0.2)));
check('the shear never spins the scene (symmetric matrix)', [paramsOnPath(2), paramsOnPath(-3), { a: 1.3, b: 0.8, c: 1.1, alpha: 80, beta: 50, gamma: 70 }].every((p) => { const M = shearMatrix(p); return M.every((r, i) => r.every((x, j) => Math.abs(x - M[j][i]) < 1e-9)); }));

console.log(failures === 0 ? '\nAll checks passed (0 failures).' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
