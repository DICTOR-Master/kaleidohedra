import { roofFoldSolids } from '../../src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
const apply = (M, v) => [0, 1, 2].map(i => M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2]);
const mul = (A, B) => A.map((r, i) => [0, 1, 2].map(j => r[0] * B[0][j] + r[1] * B[1][j] + r[2] * B[2][j]));
const inv = M => M.map((r, i) => [0, 1, 2].map(j => M[j][i]));
const key = M => M.flat().map(x => Math.round(x)).join(',');
const Oh = [];
for (const p of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]) for (let s = 0; s < 8; s++) {
  const M = [[0,0,0],[0,0,0],[0,0,0]];
  for (let i = 0; i < 3; i++) M[i][p[i]] = (s >> i) & 1 ? -1 : 1;
  Oh.push(M);
}
const Rz = [[0,-1,0],[1,0,0],[0,0,1]];
const vk = v => v.map(c => { const t = (Math.round(c * 1e6) / 1e6 + 0).toFixed(6); return t === '-0.000000' ? '0.000000' : t; }).join(',');
const faceKey = poly => poly.map(vk).sort().join('|');
const faceSet = faces => new Set(faces.map(faceKey));
const image = (faces, M) => faces.map(f => f.map(p => apply(M, p)));
const same = (A, B) => A.size === B.size && [...A].every(k => B.has(k));
const solids = {
  'dodecahedron': S.dodeca.faces,
  'icosahedron': S.ico.faces,
  'great star': S.star.faces,
  'octahedron': S.oct.faces,
  'stella octangula': S.stella.faces,
  'Pacioli rectangles': S.rects.faces,
};
const groupOf = faces => { const base = faceSet(faces); return Oh.filter(M => same(faceSet(image(faces, M)), base)); };
const G = {};
for (const [name, faces] of Object.entries(solids)) G[name] = groupOf(faces);
const inSet = (M, list) => list.some(N => key(N) === key(M));
const conj = (M) => mul(Rz, mul(M, inv(Rz)));
console.log('solid'.padEnd(20), '|G| in Oh', '  R90 keeps it?', '  |G ∩ R90 G R90^-1|', '  axes realigned?');
for (const [name, faces] of Object.entries(solids)) {
  const g = G[name];
  const rotG = g.map(conj);
  const shared = g.filter(M => inSet(M, rotG));
  const keeps = inSet(Rz, g);
  const realigned = !keeps && shared.length === g.length ? 'no (same group)' : (keeps ? 'no' : 'yes');
  console.log(name.padEnd(20), String(g.length).padStart(8), String(keeps).padStart(16), String(shared.length).padStart(20), '  ', realigned);
}
// Shared symmetry of all six contents together, unrotated and rotated
const all = Object.values(G).reduce((acc, g) => acc.filter(M => inSet(M, g)));
const allRot = all.map(conj);
console.log('shared by all six (unrotated):', all.length, '| after 90 deg:', allRot.length, '| same set:', all.length === allRot.length && all.every(M => inSet(M, allRot)));
