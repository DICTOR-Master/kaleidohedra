// Verifies Kaleidohedra's lattice shear (geometry-extensions/kaleido-lattice.js):
// plain FCC is the identity; the path's stop 2 turns the FCC rhombic
// dodecahedron into exactly DICTO's skewed RD (congruent: same distances
// between every pair of corners); every point on the path is a real cell.
import { rdRawVerts } from '../src/core/lattice.js';
import { dictoCellVerts } from '../src/geometry-extensions/dicto-fcc.js';
import { FCC_PARAMS, DICTO_PARAMS, PATH_RANGE, PATH_STOPS, paramsOnPath, paramsValid, shearMatrix, det3, cellDirections, cellCorners, cellQuality, pathTargets, RD_DIRECTIONS, BAIN_PARAMS, disphenoidQuality, pathRange, pathStops } from '../src/geometry-extensions/kaleido-lattice.js';
import { NEIGHBOR_OFFSETS } from '../src/core/lattice.js';
import { dictoMatrix, DICTO_DIRECTIONS, DICTO_SKEWED_ED_16, DICTO_SKEWED_ED_18 } from '../src/geometry-extensions/dicto-fcc.js';

let failures = 0;
const check = (label, ok) => { console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}`); if (!ok) failures++; };
const apply = (S, v) => S.map((r) => r[0] * v[0] + r[1] * v[1] + r[2] * v[2]);
const dists = (vs) => { const d = []; for (let i = 0; i < vs.length; i++) for (let j = i + 1; j < vs.length; j++) d.push(Math.hypot(vs[i][0] - vs[j][0], vs[i][1] - vs[j][1], vs[i][2] - vs[j][2])); return d.sort((a, b) => a - b); };
const dotp = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const lineAngle = (a, b) => (Math.acos(Math.min(1, Math.abs(dotp(a, b)) / Math.hypot(...a) / Math.hypot(...b))) * 180) / Math.PI;
const coplanar = (a, b, c) => Math.abs(det3([a, b, c])) < 1e-9;
// Faces as sorted labels, each counted twice (opposite faces).
const faces = (g) => {
  const out = [];
  for (let i = 0; i < g.length; i++) for (let j = i + 1; j < g.length; j++) {
    const third = g.findIndex((v, k) => k !== i && k !== j && coplanar(g[i], g[j], v));
    if (third >= 0) {
      if (third < j) continue; // each hexagon once, from its lowest pair
      const angs = [lineAngle(g[i], g[j]), lineAngle(g[i], g[third]), lineAngle(g[j], g[third])].map((a) => Math.round(a * 1000) / 1000).sort((a, b) => a - b);
      const lens = [g[i], g[j], g[third]].map((v) => Math.hypot(...v));
      const regular = angs.every((a) => a === 60) && lens.every((l) => Math.abs(l - lens[0]) < 1e-9);
      out.push(regular ? 'regular hexagon' : `hexagon ${angs.join('/')}`, regular ? 'regular hexagon' : `hexagon ${angs.join('/')}`);
    } else {
      const a = Math.round(lineAngle(g[i], g[j]) * 1000) / 1000;
      const sq = Math.abs(Math.hypot(...g[i]) - Math.hypot(...g[j])) < 1e-9;
      const label = a === 90 && sq ? 'square' : sq ? `rhombus ${a}` : `parallelogram ${a}`;
      out.push(label, label);
    }
  }
  const count = {};
  for (const f of out) count[f] = (count[f] || 0) + 1;
  return JSON.stringify(Object.fromEntries(Object.entries(count).sort()));
};
const zonoVolume = (S) => { let v = 0; for (let i = 0; i < S.length; i++) for (let j = i + 1; j < S.length; j++) for (let k = j + 1; k < S.length; k++) v += Math.abs(det3([S[i], S[j], S[k]])); return v; };

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

// Towards Bain: BCC stretched sqrt2 along z is FCC; its disphenoids go regular.
{
  const B = shearMatrix(paramsOnPath(2, 'bain'));
  check('Bain stop 2 is exactly the stretch diag(1, 1, sqrt2)', pathStops('bain')[2].name === 'Bain' && B.every((r, i) => r.every((x, j) => Math.abs(x - (i === j ? (i === 2 ? Math.SQRT2 : 1) : 0)) < 1e-9)) && KEYS_OK());
  function KEYS_OK() { return Object.keys(BAIN_PARAMS).every((k) => Math.abs(paramsOnPath(2, 'bain')[k] - BAIN_PARAMS[k]) < 1e-9); }
  const d0 = disphenoidQuality(paramsOnPath(0, 'bain')), d2 = disphenoidQuality(paramsOnPath(2, 'bain'));
  check(`plain BCC disphenoids: short/long edge ${d0.best.toFixed(4)} = sqrt3/2, none regular`, Math.abs(d0.best - Math.sqrt(3) / 2) < 1e-9 && d0.regular === 0);
  check('at Bain, 2 of the 6 disphenoid orientations are regular tetrahedra and the other 4 are quarter-octahedra (edges 1 x5, sqrt2 x1)', d2.regular === 2 && d2.ratios.filter((r) => Math.abs(r - Math.SQRT1_2) < 1e-9).length === 4);
  const T = pathTargets(1, 0.6, pathRange('bain'), 0.02, 'bain');
  check(`Find on the Bain path reaches the regular tetrahedra at 2 (${T.length} targets)`, T.some((e) => e.kind === 'regular tetrahedra' && Math.abs(e.at - 2) < 1e-3));
  check('the DICTO path has no regular-tetrahedra targets (disphenoids only get less regular there)', !pathTargets(1).some((e) => e.kind === 'regular tetrahedra'));
}

// The Bain shear's cells (DISCOVERIES.md #4, #5). A zonohedron's faces come
// from pairs of edge directions (a parallelogram) or coplanar triples (a
// hexagon); each face polygon is classified from its directions.
{
  const B = shearMatrix(paramsOnPath(2, 'bain'));
  const rd = RD_DIRECTIONS.map((v) => apply(B, v));
  check('Bain RD: equal edges, 4 squares and 8 rhombi of 60 degrees', rd.every((v) => Math.abs(Math.hypot(...v) - 1) < 1e-9) && faces(rd) === JSON.stringify({ 'rhombus 60': 8, square: 4 }));
  // Elongated dodecahedron: the RD's four directions plus one more, length 1.
  const edX = [...rd, apply(B, [1, 0, 0])];
  check(`Bain ED along x: equal edges, 4 regular hexagons, 4 squares, 4 rhombi of 60 degrees (${faces(edX)})`, edX.every((v) => Math.abs(Math.hypot(...v) - 1) < 1e-9) && faces(edX) === JSON.stringify({ 'regular hexagon': 4, 'rhombus 60': 4, square: 4 }));
  const edZ = [...rd, [0, 0, 1]];
  check(`Bain ED along z: 8 rhombi of 60 degrees, 4 equal-edged hexagons with 135/135/90 corners (${faces(edZ)})`, faces(edZ) === JSON.stringify({ 'hexagon 45/45/90': 4, 'rhombus 60': 8 }));
  // The Polyhedraverse ED (elongation = the RD's edge, sqrt3/2, before the
  // shear) is NOT the regular-hexagon one: its x edge stays sqrt3/2.
  check('the standard ED sheared has hexagon edges 1, 1, 0.866 (not regular)', Math.abs(Math.hypot(...apply(B, [Math.sqrt(3) / 2, 0, 0])) - Math.sqrt(3) / 2) < 1e-9);
}

// DICTO's skewed ED (TARGETS.md #16, #18): extends DICTO's skewed RD
// (DISCOVERIES.md #1) by a fifth edge direction, the same way DISCOVERIES.md
// #5 extends the Bain RD. Found by matching DICTO_DIRECTIONS' Gram matrix
// against every already-catalogued equal-edge ED cell's 4-direction sub-sets;
// exactly two contain it exactly, #16 and #18.
{
  const PHI = (1 + Math.sqrt(5)) / 2;
  check('DICTO skewed ED #16: equal edges, 4 rhombus 60, 4 rhombus 72, 2 hexagon 36/36/72, 2 regular hexagon, volume phi^2 + 2', DICTO_SKEWED_ED_16.every((v) => Math.abs(Math.hypot(...v) - 1) < 1e-9) && faces(DICTO_SKEWED_ED_16) === JSON.stringify({ 'hexagon 36/36/72': 2, 'regular hexagon': 2, 'rhombus 60': 4, 'rhombus 72': 4 }) && Math.abs(zonoVolume(DICTO_SKEWED_ED_16) - (PHI * PHI + 2)) < 1e-9);
  check('DICTO skewed ED #18: equal edges, 6 rhombus 60, 2 rhombus 72, 4 hexagon 36/72/72, volume phi^3 + 1/2', DICTO_SKEWED_ED_18.every((v) => Math.abs(Math.hypot(...v) - 1) < 1e-9) && faces(DICTO_SKEWED_ED_18) === JSON.stringify({ 'hexagon 36/72/72': 4, 'rhombus 60': 6, 'rhombus 72': 2 }) && Math.abs(zonoVolume(DICTO_SKEWED_ED_18) - (PHI * PHI * PHI + 0.5)) < 1e-9);
  // Both contain DICTO's skewed RD's four directions exactly (its first 4 entries, unchanged).
  check('both skewed EDs keep DICTO_DIRECTIONS exactly as their first four directions', DICTO_DIRECTIONS.every((v, i) => DICTO_SKEWED_ED_16[i].every((x, k) => x === v[k]) && DICTO_SKEWED_ED_18[i].every((x, k) => x === v[k])));
}

console.log(failures === 0 ? '\nAll checks passed (0 failures).' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
