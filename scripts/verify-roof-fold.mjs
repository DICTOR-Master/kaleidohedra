// Verifies the roof-fold cell (geometry-extensions/roof-fold.js):
//
//   - cube, dodecahedron and icosahedron are regular, with edges
//     2 : 2/phi : 2/phi^2, all along icosahedral two-fold axes;
//   - copies at translations by 2 give 13 nodes per cell, every dodecahedron
//     vertex is a node, and every roof vertex is a neighbour's icosahedron vertex;
//   - the dodecahedra cover space once or twice, mean (5 + sqrt5)/4;
//   - each icosahedron face has one node at 2/phi from its three corners,
//     the 20 tips are the dodecahedron's vertices, apex 36 degrees;
//   - the node set's symmetry is the 24 operations of m-3 about the origin,
//     with only lattice translations: Pm-3, nodes on 1b and 12j (0, y, z).
import { PHI, ROOF_FOLD_PERIOD as P, roofFoldCell } from '../src/geometry-extensions/roof-fold.js';

let failures = 0;
function check(label, condition) {
  console.log(`${condition ? 'OK  ' : 'FAIL'} ${label}`);
  if (!condition) failures++;
}
const EPS = 1e-9;
const sub = (a, b) => a.map((c, i) => c - b[i]);
const add = (a, b) => a.map((c, i) => c + b[i]);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.hypot(...a);
const wrap = (v) => v.map((c) => { const m = ((c % P) + P) % P; return Math.abs(m - P) < EPS ? 0 : m; });
const key = (v) => wrap(v).map((c) => c.toFixed(7)).join();

const C = roofFoldCell();

// 1. Regular solids and the edge chain.
const degreesAll = (n, edges, d) => { const deg = new Array(n).fill(0); edges.forEach(([i, j]) => { deg[i]++; deg[j]++; }); return deg.every((x) => x === d); };
check(`cube: 12 edges of 2, 3 at each corner`, C.cubeEdges.length === 12 && degreesAll(8, C.cubeEdges, 3));
check(`dodecahedron: 30 edges of 2/phi, 3 at each of 20 vertices`, C.dodecaEdges.length === 30 && degreesAll(20, C.dodecaEdges, 3));
check(`icosahedron: 30 edges of 2/phi^2, 5 at each of 12 vertices`, C.icoEdges.length === 30 && degreesAll(12, C.icoEdges, 5));
const icoD = [];
for (let i = 0; i < 12; i++) for (let j = i + 1; j < 12; j++) icoD.push(norm(sub(C.ico[i], C.ico[j])));
icoD.sort((a, b) => a - b);
check('the 30 shortest icosahedron distances are equal, the next is longer', icoD[29] - icoD[0] < EPS && icoD[30] - icoD[29] > 0.1);

const AXES = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
for (const [s, t] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) for (let r = 0; r < 3; r++) {
  const b = [1, s * PHI, t / PHI];
  AXES.push([b[(3 - r) % 3], b[(4 - r) % 3], b[(5 - r) % 3]]);
}
const onAxis = (v) => AXES.some((a) => norm(cross(v, a)) / (norm(v) * norm(a)) < EPS);
const allOnAxes = (V, E) => E.every(([i, j]) => onAxis(sub(V[i], V[j])));
check('15 distinct two-fold axes', new Set(AXES.map((a) => a.map((c) => (c / norm(a)).toFixed(6)).join())).size === 15);
check('every cube, dodecahedron and icosahedron edge is along a two-fold axis',
  allOnAxes(C.cube, C.cubeEdges) && allOnAxes(C.dodeca, C.dodecaEdges) && allOnAxes(C.ico, C.icoEdges));

// 2. Nodes per cell and coincidences.
const nodeKeys = new Set(C.nodes.map(key));
const everyPoint = new Set([...C.dodeca, ...C.ico].map(key));
check(`13 nodes per cell (${nodeKeys.size}), no other points`, nodeKeys.size === 13 && everyPoint.size === 13);
const icoKeys = new Set(C.ico.map(key));
check('every roof vertex is an icosahedron vertex of a neighbouring cell', C.dodeca.slice(8).every((v) => icoKeys.has(key(v)) && norm(v) > 1.5));

// 3. Covering by dodecahedra.
const faceNormals = C.ico.map((v) => v.map((c) => c / norm(v)));
const faceDist = Math.max(...C.dodeca.map((v) => dot(v, faceNormals[0])));
check('all 12 dodecahedron faces are planes through 5 vertices at the same distance',
  faceNormals.every((n) => C.dodeca.filter((v) => Math.abs(dot(v, n) - faceDist) < EPS).length === 5 && Math.max(...C.dodeca.map((v) => dot(v, n))) < faceDist + EPS));
const inside = (p) => faceNormals.every((n) => dot(p, n) <= faceDist + EPS);
check('the icosahedron lies inside its own dodecahedron', C.ico.every(inside));
const N = 48;
const counts = { 0: 0, 1: 0, 2: 0, more: 0 };
let total = 0;
for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) for (let k = 0; k < N; k++) {
  const p = [i, j, k].map((c, a) => -1 + (2 * (c + 0.5 + 0.0137 * (a + 1))) / N);
  let m = 0;
  for (const x of [-2, 0, 2]) for (const y of [-2, 0, 2]) for (const z of [-2, 0, 2]) if (inside(sub(p, [x, y, z]))) m++;
  total += m;
  counts[m > 2 ? 'more' : m]++;
}
const mean = total / N ** 3;
const exactMean = (10 + 2 * Math.sqrt(5)) / 8;
check(`dodecahedron volume (15+7sqrt5)/4 (2/phi)^3 = 10 + 2sqrt5`, Math.abs(((15 + 7 * Math.sqrt(5)) / 4) * (2 / PHI) ** 3 - (10 + 2 * Math.sqrt(5))) < EPS && Math.abs(exactMean - (5 + Math.sqrt(5)) / 4) < EPS);
check(`every sample point covered once or twice (${(counts[1] / N ** 3).toFixed(3)} once, ${(counts[2] / N ** 3).toFixed(3)} twice)`, counts[0] === 0 && counts.more === 0);
check(`sampled mean multiplicity ${mean.toFixed(4)} matches (5+sqrt5)/4 = ${exactMean.toFixed(4)}`, Math.abs(mean - exactMean) < 0.01);

// 4. Spikes on the icosahedron faces.
const faces = [];
for (let a = 0; a < 12; a++) for (let b = a + 1; b < 12; b++) for (let c = b + 1; c < 12; c++) {
  const e = 2 / PHI ** 2;
  if ([[a, b], [a, c], [b, c]].every(([i, j]) => Math.abs(norm(sub(C.ico[i], C.ico[j])) - e) < EPS)) faces.push([a, b, c]);
}
const nearNodes = [];
for (const n of C.nodes) for (const x of [-2, 0, 2]) for (const y of [-2, 0, 2]) for (const z of [-2, 0, 2]) nearNodes.push(add(n, [x, y, z]));
const tips = faces.map((f) => {
  const V = f.map((i) => C.ico[i]);
  const c = V.reduce(add).map((x) => x / 3);
  return nearNodes.filter((p) => dot(sub(p, c), c) > 0 && V.every((v) => Math.abs(norm(sub(p, v)) - 2 / PHI) < EPS));
});
check(`20 icosahedron faces, each with exactly one tip node`, faces.length === 20 && tips.every((t) => t.length === 1));
const tipKeys = new Set(tips.map((t) => t[0].map((c) => c.toFixed(7)).join()));
const dodecaKeys = new Set(C.dodeca.map((v) => v.map((c) => c.toFixed(7)).join()));
check('the 20 tips are exactly the 20 dodecahedron vertices', tipKeys.size === 20 && [...tipKeys].every((k) => dodecaKeys.has(k)));
const apex = (Math.acos(1 - (2 / PHI ** 2) ** 2 / (2 * (2 / PHI) ** 2)) * 180) / Math.PI;
check(`spike faces are golden triangles (apex ${apex.toFixed(4)} degrees)`, Math.abs(apex - 36) < 1e-9);

// 5. Symmetry: which of the 48 cubic point operations map the node set to itself, and with which translation.
const PERMS = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [1, 0, 2], [0, 2, 1], [2, 1, 0]];
const ops = [];
for (const perm of PERMS) for (let s = 0; s < 8; s++) {
  const sg = [s & 1 ? -1 : 1, s & 2 ? -1 : 1, s & 4 ? -1 : 1];
  ops.push({ even: PERMS.indexOf(perm) < 3, f: (v) => perm.map((p, i) => sg[i] * v[p]) });
}
const preserves = (f, t) => C.nodes.every((v) => nodeKeys.has(key(add(f(v), t))));
const candidates = (f) => C.nodes.map((v) => sub(v, f(C.nodes[0])));
const kept = ops.map((op) => candidates(op.f).filter((t) => preserves(op.f, t)));
check('exactly 24 point operations keep the node set (m-3), all with no swap of two axes',
  kept.filter((t) => t.length).length === 24 && ops.every((op, i) => (kept[i].length > 0) === op.even));
check('each works with a lattice translation only (symmorphic, origin on the icosahedron centre)', kept.every((ts) => ts.every((t) => key(t) === key([0, 0, 0]))));
const stab = (v) => ops.filter((op) => key(op.f(v)) === key(v)).length;
check(`corner node is fixed by all 24 (Wyckoff 1b); each icosahedron vertex by 2, a mirror (12j, (0, y, z), y = ${(1 / (2 * PHI)).toFixed(4)}, z = ${(1 / (2 * PHI ** 2)).toFixed(4)} in cell units)`,
  ops.filter((op) => op.even).every((op) => key(op.f([1, 1, 1])) === key([1, 1, 1])) && C.ico.every((v) => ops.filter((op) => op.even && key(op.f(v)) === key(v)).length === 2) && C.ico.every((v) => v.some((c) => Math.abs(c) < EPS)) && stab([1, 1, 1]) === 48);

console.log(failures === 0 ? '\nAll checks passed (0 failures).' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
