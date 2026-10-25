// Atom onions, part C: the app's own shells (k-dshells branch dictonic-shells) at the stops, and DICTO's named pieces from
// Polyhedraverse, as floats, for check_app.py. Run: node --import ./reg.mjs app_dump.mjs > ../data/raw/app-dump.json
import { goldenT, GOLDEN_STOPS, DELIAN_STOPS } from '/home/dicto/k-dshells/src/app/world-dictonic.js';
import { tetPiece, octPiece, OCTET_FAMILY_STOPS as ST } from '/home/dicto/k-dshells/src/krp-core/src/polyhedra/delian-bond.js';
import { GOLDEN_SPLIT_ADDITIONS as G } from '/home/dicto/k-dshells/src/krp-core/src/polyhedra/golden-split.js';
import { DELIAN_BOND_ADDITIONS as D } from '/home/dicto/k-dshells/src/krp-core/src/polyhedra/delian-bond.js';
import { t } from '/home/dicto/k-dshells/src/app/i18n.js';
const PHI = (1 + Math.sqrt(5)) / 2;
const out = { golden: {}, delian: {}, pieces: {}, stops: { golden: GOLDEN_STOPS, delian: DELIAN_STOPS, octet: ST }, names: {} };
for (const [k, x] of Object.entries({ '0': 0, '1/tau': 1 / PHI, '1': 1, 'tau': PHI, 'inf': Infinity })) out.golden[k] = goldenT(x).vertices;
for (const [k, v] of Object.entries(ST)) out.delian[k] = { t: v, tet: v > 0 ? tetPiece([0, 0, 0], v) : [], oct: v < 1 ? octPiece([1, 0, 0], v) : [] };
for (const id of ['DICTO_ICOSAXES', 'DICTO_UNBORN_AXES']) out.pieces[id] = { name: G[id].name, vertices: G[id].vertices };
for (const id of ['DICTO_SAMSON', 'DICTO_DELILAH']) out.pieces[id] = { name: D[id].name, vertices: D[id].vertices };
for (const k of ['zero', 'kelvin', 'tau', 'inf']) out.names[`golden.${k}`] = t(`dictonic.stop.golden.${k}`, 'en');
for (const k of ['rd', 'equilateral', 'octet', 'half', 'bond', 'cube']) out.names[`delian.${k}`] = t(`dictonic.stop.delian.${k}`, 'en');
console.log(JSON.stringify(out));
