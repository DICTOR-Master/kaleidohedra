// Dump the app's own pieces and web (k-dshells branch dictonic-shells, src/app/world-dictonic.js) at the study's sample
// parameters, as floats, for the frame/scale assert and the float cross-check (check_app.py). Run from anywhere:
//   node --import ./reg.mjs app_dump.mjs > ../data/raw/app-dump.json   (reg.mjs only resolves 'three' for the import)
import { goldenT, delianFamily, webOf } from '/home/dicto/k-dshells/src/app/world-dictonic.js';
import { scSites } from '/home/dicto/k-dshells/src/app/world-octet.js';
import { tetPiece, octPiece, OCTET_FAMILY_STOPS as ST } from '/home/dicto/k-dshells/src/krp-core/src/polyhedra/delian-bond.js';
const PHI = (1 + Math.sqrt(5)) / 2;
// goldenCells of world-dictonic.js (not exported): whole T(x) on the lattice points, T(1/x) on the cube centres
function goldenCells(size, x) {
  const { ico, voids } = scSites(size), out = [], at = (n) => n.map((c) => (c * PHI) / 2);
  const put = (role, { vertices, faces }, n) => { const c = at(n); out.push([role, vertices.map((v) => v.map((q, i) => q + c[i])), faces, n, { anchor: c }]); };
  for (const n of ico.values()) put('gsBig', goldenT(x), n);
  for (const n of voids.values()) put('gsSmall', goldenT(x === 0 ? Infinity : x === Infinity ? 0 : 1 / x), n);
  return out;
}
const GX = { '0': 0, '1/3': 1 / 3, '1/2': 0.5, '1': 1, '2': 2, '3': 3, 'tau': PHI, '1/tau': 1 / PHI, 'sqrt2': Math.SQRT2, 'inf': Infinity };
const DT = { '0': 0, '1/6': 1 / 6, '1/4': 0.25, '1/3': 1 / 3, '1/2': 0.5, '2/3': 2 / 3, '1': 1, ...Object.fromEntries(Object.entries(ST).map(([k, v]) => ['stop:' + k, v])) };
const out = { golden: {}, delian: {} };
for (const [k, x] of Object.entries(GX)) {
  const pieces = goldenCells(2, x);
  out.golden[k] = { x: x === Infinity ? 'inf' : x, big: goldenT(x).vertices, small: goldenT(x === 0 ? Infinity : x === Infinity ? 0 : 1 / x).vertices,
    pieces: pieces.map(([role, , , n, e]) => [role, n, e.anchor]), web: webOf(pieces) };
}
for (const [k, t] of Object.entries(DT)) {
  const pieces = delianFamily(2, t);
  out.delian[k] = { t, tet0: tetPiece([0, 0, 0], t), tet1: tetPiece([1, 0, 0], t), oct: octPiece([1, 0, 0], t),
    pieces: pieces.map(([role, V, , c, e]) => [role, c, e.anchor, V.length]), web: webOf(pieces) };
}
console.log(JSON.stringify(out));
