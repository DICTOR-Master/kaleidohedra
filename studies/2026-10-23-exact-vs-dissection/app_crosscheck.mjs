// app_crosscheck.mjs: the app's own code (krp-core, pinned e5e5dbc) set to this study's slider values gives the same cells
// (float; the exact proofs are in check.py). DICTO · dictospheres.com, 2026-10-23.
// Run: node app_crosscheck.mjs <path to a krp-core checkout at e5e5dbc>
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const core = process.argv[2];
const K = await import(join(core, 'src/geometry-extensions/kaleido-lattice.js'));
const D = await import(join(core, 'src/geometry-extensions/dicto-fcc.js'));
const T = await import(join(core, 'src/geometry-extensions/targets.js'));
const here = dirname(fileURLToPath(import.meta.url));
const J = (f) => JSON.parse(readFileSync(join(here, 'data', f)));
let fails = 0;
const check = (label, ok) => { console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}`); if (!ok) fails++; };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

// Two direction sets span congruent zonotopes (up to a uniform scale k) when some signed permutation matches their Gram matrices.
function sameZonotope(A, B, k = 1, tol = 1e-9) {
  if (A.length !== B.length) return false;
  const n = A.length;
  const perms = [];
  const rec = (p, rest) => (rest.length ? rest.forEach((x, i) => rec([...p, x], rest.filter((_, j) => j !== i))) : perms.push(p));
  rec([], [...Array(n).keys()]);
  for (const p of perms) for (let s = 0; s < 1 << n; s++) {
    const sg = (i) => ((s >> i) & 1 ? -1 : 1);
    let ok = true;
    for (let i = 0; i < n && ok; i++) for (let j = i; j < n && ok; j++)
      ok = Math.abs(dot(A[i], A[j]) * k * k - sg(i) * sg(j) * dot(B[p[i]], B[p[j]])) < tol;
    if (ok) return true;
  }
  return false;
}
const deg = (p) => ({ a: p.a, b: p.b, c: p.c, alpha: p.alpha.degrees, beta: p.beta.degrees, gamma: p.gamma.degrees });

// Bain RD and the regular-hexagon ED
const bain = J('bain-rd.json'), f5 = J('regular-hexagon-ed.json');
const Bp = K.paramsOnPath(2, 'bain');
check('Towards Bain, stop 2: the app\'s slider values equal the study\'s', ['a', 'b', 'c', 'alpha', 'beta', 'gamma'].every((k) => Math.abs(Bp[k] - deg(bain.move.app_slider_values)[k]) < 1e-9));
check('Bain stop 2, Cell = 1: the app\'s cell is the study\'s Bain RD', sameZonotope(K.cellDirections(Bp, 1), bain.edge_directions_float));
check('the app\'s regular-hexagon ED (targets.js EMBLEM_DIRECTIONS) is the study\'s F5', sameZonotope(T.EMBLEM_DIRECTIONS, f5.edge_directions_float));

// Bilinski: the study's slider values, and the scale-free form a = b = c = 1, alpha = beta = 60, gamma = 36
const bil = J('bilinski-dodecahedron.json');
const pB = deg(bil.move['app_slider_values (scaled to the app edge sqrt3/2)']);
const cB = K.cellDirections(pB, 1);
const kB = Math.sqrt(dot(bil.edge_directions_float[0], bil.edge_directions_float[0]) / 0.75); // app length -> study length
check(`sliders a=b=c=${pB.a.toFixed(4)}, alpha=beta=${pB.alpha.toFixed(4)}, gamma=${pB.gamma.toFixed(4)}, Cell = 1: the app's cell is Bilinski's dodecahedron (edge sqrt3/2)`, sameZonotope(cB, bil.edge_directions_float, kB, 1e-9));
check('  and the app says it fills space there (no red band)', K.cellFillsSpace(pB, 1));
const p36 = { a: 1, b: 1, c: 1, alpha: 60, beta: 60, gamma: 36 };
const c36 = K.cellDirections(p36, 1);
const k36 = Math.sqrt(dot(bil.edge_directions_float[0], bil.edge_directions_float[0]) / dot(c36[0], c36[0]));
check('plain FCC sliders with only gamma moved from 60 to 36, Cell = 1: Bilinski\'s dodecahedron (scaled)', sameZonotope(c36, bil.edge_directions_float, k36, 1e-9) && K.cellFillsSpace(p36, 1));
check('  at Cell = 0 the same sliders give a cell that is NOT Bilinski\'s (an affine image of Kepler\'s)', !sameZonotope(K.cellDirections(p36, 0), bil.edge_directions_float, Math.sqrt(dot(bil.edge_directions_float[0], bil.edge_directions_float[0]) / dot(K.cellDirections(p36, 0)[0], K.cellDirections(p36, 0)[0])), 1e-6));
check('  the app\'s angle slider reaches 36 (range 20-150, step 0.1): gamma = 36.0 exactly on the slider grid', Math.abs(pB.gamma - 36) < 1e-9);

// DICTO FCC and F7
const ed = J('elongated-dodecahedron-type.json');
const F1 = ed.members.dicto_skewed_RD_F1;
const kD = 2 / Math.sqrt(3); // app edge sqrt3/2 -> study edge 1
check('Towards DICTO FCC, stop 2, Cell = 1: the app\'s cell is the study\'s exact DICTO skewed RD (edge sqrt3/2)', sameZonotope(K.cellDirections(K.paramsOnPath(2), 1), F1.edge_directions_float, kD));
const fl = ed.members.dicto_free_lines;
check('krp-core DICTO_SKEWED_ED_16 is the study\'s ED on free line ' + ed.F7_partitions.ED16[0], sameZonotope(D.DICTO_SKEWED_ED_16, fl[ed.F7_partitions.ED16[0]].solid.edge_directions_float));
check('krp-core DICTO_SKEWED_ED_18 is the study\'s ED on free line ' + ed.F7_partitions.ED18[0], sameZonotope(D.DICTO_SKEWED_ED_18, fl[ed.F7_partitions.ED18[0]].solid.edge_directions_float));
check('plain FCC, Cell = 1: the regular RD (all line angles 70.53)', K.cellQuality(K.cellDirections(K.FCC_PARAMS, 1)).angles.every((x) => Math.abs(x - 70.5288) < 1e-3));
console.log(fails ? `\n${fails} FAILED` : '\nAll app cross-checks pass.');
process.exit(fails ? 1 : 0);
