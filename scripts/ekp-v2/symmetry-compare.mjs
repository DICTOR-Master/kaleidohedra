// Symmetry of three structures on the cubic cell lattice, with the contents held fixed:
//   original: the seven pieces in every cube, unturned (the EKP cell as built in the app);
//   network:  stars on even cubes, icosahedra on odd cubes, unturned (DISCOVERIES #8b);
//   v2:       the seven pieces in every cube, odd cubes turned 90 degrees about z.
// An operation is (O, t): a cube symmetry O (signed permutation) with a cube translation t (cell units).
import { roofFoldSolids } from '../../src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
const apply = (M, v) => [0, 1, 2].map(i => M[i][0]*v[0] + M[i][1]*v[1] + M[i][2]*v[2]);
const mul = (A, B) => A.map(r => [0, 1, 2].map(j => r[0]*B[0][j] + r[1]*B[1][j] + r[2]*B[2][j]));
const det = M => M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);
const Oh = [];
for (const p of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]) for (let s = 0; s < 8; s++) {
  const M = [[0,0,0],[0,0,0],[0,0,0]];
  for (let i = 0; i < 3; i++) M[i][p[i]] = (s >> i) & 1 ? -1 : 1;
  Oh.push(M);
}
const key = M => M.flat().join(',');
const I3 = [[1,0,0],[0,1,0],[0,0,1]], Rz = [[0,-1,0],[1,0,0],[0,0,1]];
const vk = v => v.map(c => { const t = (Math.round(c * 1e6) / 1e6 + 0).toFixed(6); return t === '-0.000000' ? '0.000000' : t; }).join(',');
const fk = (type, poly) => type + '|' + poly.map(vk).sort().join('|');
const ALL = { cube: S.cube.faces, dodecahedron: S.dodeca.faces, icosahedron: S.ico.faces, 'great star': S.star.faces, octahedron: S.oct.faces, stella: S.stella.faces, pacioli: S.rects.faces };
const NET_EVEN = { 'great star': S.star.faces }, NET_ODD = { icosahedron: S.ico.faces };
const keysOf = (solids, M) => { const set = new Set(); for (const [t, faces] of Object.entries(solids)) for (const f of faces) set.add(fk(t, f.map(p => apply(M, p)))); return set; };
const eq = (A, B) => A.size === B.size && [...A].every(k => B.has(k));
const par = c => ((c[0]+c[1]+c[2]) % 2 + 2) % 2;
const W = 2, cells = [];
for (let i = -W; i <= W; i++) for (let j = -W; j <= W; j++) for (let k = -W; k <= W; k++) cells.push([i, j, k]);
const inWin = c => c.every(x => Math.abs(x) <= W);
const T8 = [[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]];
// Content of a cube, given its parity and rotation: the set of face keys at the origin.
function structure(name) {
  const cache = new Map();
  const content = (c) => {
    const rot = name === 'v2' && par(c) === 1 ? 'R' : 'I';
    const solids = name === 'network' ? (par(c) === 0 ? NET_EVEN : NET_ODD) : ALL;
    const k = (name === 'network' ? par(c) : '') + rot;
    if (!cache.has(k)) cache.set(k, keysOf(solids, rot === 'R' ? Rz : I3));
    return cache.get(k);
  };
  const ops = [];
  for (const O of Oh) for (const t of T8) {
    let ok = true, checked = 0;
    for (const c of cells) {
      const g = apply(O, c).map((x, k) => x + t[k]);
      if (!inWin(g)) continue;
      checked++;
      const img = keysOf({}, O); // placeholder, replaced below
      // image of content(c) under O, compared with content(g)
      const mapped = new Set();
      for (const k2 of content(c)) { const i = k2.indexOf('|'); const type = k2.slice(0, i); const pts = k2.slice(i + 1).split('|').map(s => s.split(',').map(Number)); mapped.add(fk(type, pts.map(p => apply(O, p)))); }
      if (!eq(mapped, content(g))) { ok = false; break; }
    }
    if (ok && checked) ops.push({ O, t });
  }
  return ops;
}
// Lattice of pure translations: even-sum cube vectors (face-centred) or all cube vectors (primitive)
const inLattice = (v, lattice) => v.every(Number.isInteger) && (lattice === 'F' ? ((v[0]+v[1]+v[2]) % 2 === 0) : true);
function symmorphicAbout(ops, p, lattice) {
  return ops.every(({ O, t }) => { const Op = apply(O, p); const v = [0,1,2].map(i => t[i] - (p[i] - Op[i])); return inLattice(v, lattice); });
}
// Glide vectors of the reflections: translation parallel to the mirror plane, in cell units.
function reflectionGlides(ops) {
  const out = [];
  for (const { O, t } of ops) {
    if (det(O) > 0) continue;
    const cand = []; for (const a of [-1,0,1]) for (const b of [-1,0,1]) for (const c of [-1,0,1]) if (a||b||c) cand.push([a,b,c]);
    const n = cand.find(v => { const Ov = apply(O, v); return Ov.every((x, i) => Math.abs(x + v[i]) < 1e-9); });
    if (!n) continue;
    const nn = n.map(x => x / Math.hypot(...n));
    const tn = t[0]*nn[0] + t[1]*nn[1] + t[2]*nn[2];
    const tpar = t.map((x, i) => +(x - tn * nn[i]).toFixed(3));
    out.push({ normal: n.join(','), glide: tpar.join(','), offset: +tn.toFixed(3) });
  }
  return out;
}
const structures = [['original (identical, unturned)', 'original'], ['network (stars even, icosahedra odd)', 'network'], ['v2 (identical, odd turned)', 'v2']];
for (const [label, name] of structures) {
  const ops = structure(name);
  const points = new Set(ops.map(o => key(o.O)));
  const lattice = name === 'original' ? 'P' : 'F';
  const transl = [...new Set(ops.filter(o => key(o.O) === key(I3)).map(o => o.t.join(',')))];
  console.log(`== ${label}`);
  console.log(`   operations (O, t) with t in the 8 cube classes: ${ops.length}; point operations: ${points.size}; pure translations (mod 2): [${transl.join(' | ')}]`);
  console.log(`   lattice of translations: ${lattice === 'P' ? 'primitive (all integer cube vectors)' : 'face-centred (even-sum cube vectors)'}`);
  const cs = [[0,0,0],[0.5,0.5,0.5]];
  console.log(`   fixed point common to all operations: ${cs.some(p => symmorphicAbout(ops, p, lattice)) ? 'yes (symmorphic)' : 'no (non-symmorphic)'}`);
  const swaps = ops.filter(o => (o.t[0]+o.t[1]+o.t[2]) % 2 === 1);
  console.log(`   operations exchanging even and odd cubes: ${swaps.length}`);
  const g = reflectionGlides(ops);
  const kinds = {};
  for (const r of g) kinds[r.glide] = (kinds[r.glide] || 0) + 1;
  console.log(`   reflections: ${g.length}; glide vectors parallel to the mirror (cell units; 1 cell = half a conventional cube): ${JSON.stringify(kinds)}`);
}
