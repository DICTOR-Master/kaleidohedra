// Gathers every 13's kits from their checked sources into one JSON (DICTO 2026-10-13, docs/PLAN-13.md stage 1).
// Usage: node scripts/dump-thirteens.mjs <rd13 rounded json (0.15, exact RD centre)> <fattest json (0.35, exact RD centre)> <free-centre json (0.15)> > thirteens-raw.json
import fs from 'fs';
import { ICOSA_PARTS } from '../src/krp-core/src/geometry-extensions/icosa.js';
import { DODECA13_PARTS } from '../src/krp-core/src/polyhedra/dodeca13.js';
import SEEDS from '../src/app/seeds-data.js';
import STAR from '../src/app/dodeca-data.js';
import { POLYHEDRA } from '../src/krp-core/src/polyhedra/index.js';
const conv = (list) => list.map((p) => [p.role, p.vertices, p.faces]);
const d13 = DODECA13_PARTS.DICTO_DODECA13;
// RD 13: plain (13 RDs of the FCC lattice, neighbours sqrt2 apart) and the rounded keyed block (studies/2026-10-13-rd13-block)
const NB = []; for (const x of [-1, 0, 1]) for (const y of [-1, 0, 1]) for (const z of [-1, 0, 1]) { const a = [x, y, z].map(Math.abs).sort(); if (a[0] === 0 && a[1] === 1 && a[2] === 1) NB.push([x, y, z]); }
const rdCell = (p) => {
  const V = [], key = (v) => v.map((c) => c.toFixed(6)).join(','), at = (v) => { let i = V.findIndex((w) => key(w) === key(v)); if (i < 0) { V.push(v); i = V.length - 1; } return i; };
  const F = NB.map((n) => { const [i, j] = [0, 1, 2].filter((k) => n[k]); const k = 3 - i - j; const e = (m, s) => [0, 1, 2].map((q) => (q === m ? s : 0));
    const add = (...vs) => [0, 1, 2].map((q) => p[q] + vs.reduce((t, v) => t + v[q], 0));
    return [add(e(i, n[i])), add(e(i, n[i] / 2), e(j, n[j] / 2), e(k, 0.5)), add(e(j, n[j])), add(e(i, n[i] / 2), e(j, n[j] / 2), e(k, -0.5))].map(at); });
  return [V, F];
};
// Every face wound outward (normal away from the cell's middle).
const outward = ([V, F]) => {
  const c = [0, 1, 2].map((q) => V.reduce((t, v) => t + v[q], 0) / V.length);
  return [V, F.map((f) => {
    const [a, b, d] = f.map((i) => V[i]); const u = [0, 1, 2].map((q) => b[q] - a[q]), w = [0, 1, 2].map((q) => d[q] - a[q]);
    const n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
    const m = [0, 1, 2].map((q) => f.reduce((t, i) => t + V[i][q], 0) / f.length - c[q]);
    return n[0] * m[0] + n[1] * m[1] + n[2] * m[2] < 0 ? [...f].reverse() : f;
  })];
};
const plain = [[0, 0, 0], ...NB].map((p, i) => { const [V, F] = outward(rdCell(p)); return [i ? 'rd' : 'rdCentre', V, F]; });
const R = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const blockOf = (R) => R.cells.map((faces, ci) => {
  const V = [], key = (v) => v.map((c) => c.toFixed(6)).join(','), at = (v) => { let i = V.findIndex((w) => key(w) === key(v)); if (i < 0) { V.push(v); i = V.length - 1; } return i; };
  const [, F] = outward([V, faces.map((f) => f.map(at))]);
  return [ci === 0 ? 'rdCentre' : Math.abs(R.volumes[ci] - R.volumes[1]) < 1e-3 ? 'rdA' : 'rdB', V, F];
});
const rounded = blockOf(R);
// The fattest outer pieces (DICTO 2026-10-13: "I like the fattest RDs"), minimum thickness 0.35, as a second rounded view.
const fattest = process.argv[3] ? blockOf(JSON.parse(fs.readFileSync(process.argv[3], 'utf8'))) : null;
// The free-centre block (DICTO 2026-10-13: exact RD centre as main, free as variant).
const roundedFree = process.argv[4] ? blockOf(JSON.parse(fs.readFileSync(process.argv[4], 'utf8'))) : null;
// The regular-hexagon elongated dodecahedron's 13 (DICTO 2026-10-13, finding #5): a centre and its 12 face neighbours in its own
// honeycomb (each across a face, at twice that face's offset), 4 across the regular hexagons and 8 across the rhombi; and seven such
// blocks filling space (the block lattice from w = (1, 2, 5) mod 13 on the ED lattice, checked in studies/2026-10-13-rd13-block).
// A space-filler's 13 (DICTO 2026-10-13): a centre and twelve face neighbours in its own honeycomb (each across a face, at twice that
// face's offset), and seven such blocks filling space (block lattice from a weight w mod 13 that separates the 13, as RD 13).
// The regular-hexagon ED: all 12 faces (4 regular hexagons, 8 rhombi). The truncated octahedron (DICTO's 4 + 5 + 4): the 8 hexagons and
// the 4 squares round its middle, the top and bottom squares left as windows onto the gold centre.
const det3 = (a, b, c) => a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);
const cross = (u, v) => [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
function clusterOf(id, keepFace, roleOf) {
  const S = typeof id === 'string' ? POLYHEDRA[id] : id;
  const c = [0, 1, 2].map((q) => S.vertices.reduce((t, v) => t + v[q], 0) / S.vertices.length);
  const V0 = S.vertices.map((v) => v.map((x, q) => x - c[q]));
  const faces = S.faces.map((f, i) => ({ f, i, n: [0, 1, 2].map((q) => (2 * f.reduce((t, k) => t + V0[k][q], 0)) / f.length) })).filter(keepFace);
  const nbr = faces.map((x) => x.n);
  const piece = (t, role) => [role, V0.map((v) => v.map((x, q) => x + t[q])), S.faces];
  const cluster = [piece([0, 0, 0], roleOf(null)), ...faces.map((x) => piece(x.n, roleOf(x.f)))];
  // the lattice: all face neighbours of the cell (not only the twelve), a basis among them
  const all = S.faces.map((f) => [0, 1, 2].map((q) => (2 * f.reduce((t, k) => t + V0[k][q], 0)) / f.length));
  let basis = null;
  for (let i = 0; i < all.length && !basis; i++) for (let j = i + 1; j < all.length && !basis; j++) for (let k = j + 1; k < all.length && !basis; k++) {
    const M = [all[i], all[j], all[k]], d = det3(...M);
    if (Math.abs(d) < 1e-6) continue;
    const solve = (n) => [det3(n, M[1], M[2]) / d, det3(M[0], n, M[2]) / d, det3(M[0], M[1], n) / d];
    if (all.every((n) => solve(n).every((x) => Math.abs(x - Math.round(x)) < 1e-6))) basis = { M, solve };
  }
  const coords = [[0, 0, 0], ...nbr.map((n) => basis.solve(n).map(Math.round))];
  let W = null;
  for (let a = 0; a < 13 && !W; a++) for (let b = 0; b < 13 && !W; b++) for (let cc = 0; cc < 13 && !W; cc++) {
    if (!(a || b || cc)) continue;
    if (new Set(coords.map((x) => (((a * x[0] + b * x[1] + cc * x[2]) % 13) + 13) % 13)).size === 13) W = [a, b, cc];
  }
  if (!W) throw new Error(id + ': this 13 does not fill space by a sublattice of index 13');
  const cand = [];
  for (let x = -5; x <= 5; x++) for (let y = -5; y <= 5; y++) for (let z = -5; z <= 5; z++) {
    if (!(x || y || z) || (((W[0] * x + W[1] * y + W[2] * z) % 13) + 13) % 13) continue;
    cand.push([0, 1, 2].map((q) => x * basis.M[0][q] + y * basis.M[1][q] + z * basis.M[2][q]));
  }
  cand.sort((u, v) => Math.hypot(...u) - Math.hypot(...v));
  const T = [cand[0]];
  T.push(cand.find((v) => Math.hypot(...cross(T[0], v)) > 1e-6));
  T.push(cand.find((v) => Math.abs(det3(T[0], T[1], v)) > 1e-6));
  const blocks = [[0, 0, 0], ...T.flatMap((t) => [t, t.map((x) => -x)])].flatMap((t, b) => cluster.map(([r, V, F]) => [b ? r + 'N' : r, V.map((v) => v.map((x, q) => x + t[q])), F]));
  return { cluster, blocks };
}
const HEXED = clusterOf('REGULAR_HEX_ED', () => true, (f) => (!f ? 'hexCentre' : f.length === 6 ? 'hexByHex' : 'hexByRhombus'));
// the TO's middle: the squares whose neighbour is level with the centre (the axis through the two window squares is the one left out)
// The other 12-neighbour space-fillers (DICTO 2026-10-13): DICTO's skewed RD, the Bain RD, and the golden Bilinski dodecahedron, built
// as Polyhedraverse's Nets do (the zonohedron of four of the icosahedron's five-fold axes, edge 1).
const PHI = (1 + Math.sqrt(5)) / 2;
const FIVE = [[0, 1, PHI], [0, 1, -PHI], [1, PHI, 0], [1, -PHI, 0]].map((v) => v.map((x) => x / Math.hypot(...v)));
const BILINSKI = (() => {
  const P = [];
  for (let m = 0; m < 16; m++) P.push([0, 1, 2].map((q) => FIVE.reduce((t, v, i) => t + ((m >> i) & 1 ? 0.5 : -0.5) * v[q], 0)));
  // the 14 corners are the zonotope's extreme points; faces: the 12 rhombi spanned by pairs of the four axes
  const F = [], V = [];
  const key = (p) => p.map((x) => x.toFixed(6)).join(',');
  const at = (p) => { const k = key(p); let i = V.findIndex((w) => key(w) === k); if (i < 0) { V.push(p); i = V.length - 1; } return i; };
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) for (const sgn of [1, -1]) {
    const n = cross(FIVE[i], FIVE[j]).map((x) => x * sgn);
    const others = [0, 1, 2, 3].filter((k) => k !== i && k !== j);
    const base = [0, 1, 2].map((q) => others.reduce((t, k) => t + Math.sign(FIVE[k].reduce((u, x, r) => u + x * n[r], 0)) * 0.5 * FIVE[k][q], 0));
    const a = FIVE[i], b = FIVE[j];
    const quad = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([s1, s2]) => base.map((x, q) => x + (s1 * a[q] + s2 * b[q]) / 2));
    const idx = quad.map(at);
    const c = [0, 1, 2].map((q) => quad.reduce((t, p) => t + p[q], 0) / 4);
    const nn = cross(quad[1].map((x, q) => x - quad[0][q]), quad[2].map((x, q) => x - quad[0][q]));
    F.push(nn.reduce((t, x, q) => t + x * c[q], 0) > 0 ? idx : [...idx].reverse());
  }
  return { vertices: V, faces: F };
})();
const RDFAM = Object.fromEntries([['skewedRd13', 'DICTO_SKEWED_RD'], ['bainRd13', 'BAIN_RD'], ['bilinski13', BILINSKI]].map(([k, sp]) =>
  [k, clusterOf(sp, () => true, (f) => (!f ? `${k}Centre` : `${k}Cell`))]));
const TOS = POLYHEDRA.TRUNCATED_OCTAHEDRON;
const sqAxes = TOS.faces.filter((f) => f.length === 4).map((f) => { const n = [0, 1, 2].map((q) => f.reduce((t, k) => t + TOS.vertices[k][q], 0)); return n.map(Math.abs).indexOf(Math.max(...n.map(Math.abs))); });
const windowAxis = 2;
const TO13 = clusterOf('TRUNCATED_OCTAHEDRON', (x) => x.f.length === 6 || Math.abs(x.n[windowAxis]) < 1e-6, (f) => (!f ? 'toCentre' : f.length === 6 ? 'toByHex' : 'toBySquare'));
const out = {
  dodeca13: { pieces: conv(d13.pieces), units: conv(d13.units), stars: conv(d13.stars) },
  icosa13: { pieces: conv(ICOSA_PARTS.LOTUS_SEED.pieces), build: conv(ICOSA_PARTS.LOTUS_SEED.build), units: conv(ICOSA_PARTS.LOTUS_SEED.units) },
  unity: { open: conv(ICOSA_PARTS.UNITY.pieces), venus: conv(ICOSA_PARTS.VENUS.pieces) },
  deshi: { deshi: conv(ICOSA_PARTS.DESHI.pieces) },
  bodhi: { seed: SEEDS.bodhi.views.seed.filter((p) => p[0] !== 'outer'), kitA: SEEDS.bodhi.views.kitA, kitB: SEEDS.bodhi.views.kitB },
  dictoStar: { star: STAR.star.views.star },
  // Seven rounded blocks: one and its six nearest neighbours (plus and minus the block lattice's three short vectors), keyed.
  hexed: { cluster: HEXED.cluster, blocks: HEXED.blocks },
  to13: { cluster: TO13.cluster, blocks: TO13.blocks },
  ...Object.fromEntries(Object.entries(RDFAM).map(([k, c]) => [k, { cluster: c.cluster, blocks: c.blocks }])),
  rd13: { plain, rounded, ...(fattest ? { fattest } : {}), ...(roundedFree ? { roundedFree } : {}), blocks: [[0, 0, 0], ...R.L.flatMap((t) => [t, t.map((x) => -x)])].flatMap((t, b) => rounded.map(([role, V, F]) => [b ? `${role}N` : role, V.map((v) => v.map((x, q) => x + t[q])), F])) },
};
process.stdout.write(JSON.stringify(out));
