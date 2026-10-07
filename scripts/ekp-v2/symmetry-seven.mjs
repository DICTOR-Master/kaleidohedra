import { roofFoldSolids } from '../../src/geometry-extensions/roof-fold.js';
import { writeFileSync } from 'node:fs';
const S = roofFoldSolids();
const apply = (M, v) => [0,1,2].map(i => M[i][0]*v[0]+M[i][1]*v[1]+M[i][2]*v[2]);
const Oh = [];
for (const p of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]) for (let s = 0; s < 8; s++) {
  const M = [[0,0,0],[0,0,0],[0,0,0]];
  for (let i = 0; i < 3; i++) M[i][p[i]] = (s >> i) & 1 ? -1 : 1;
  Oh.push(M);
}
const I3 = [[1,0,0],[0,1,0],[0,0,1]], Rz = [[0,-1,0],[1,0,0],[0,0,1]];
const vk = v => v.map(c => { const t = (Math.round(c * 1e6) / 1e6 + 0).toFixed(6); return t === '-0.000000' ? '0.000000' : t; }).join(',');
const fk = (type, poly) => type + '|' + poly.map(vk).sort().join('|');
const SOLIDS = { cube: S.cube.faces, dodecahedron: S.dodeca.faces, icosahedron: S.ico.faces, 'great star': S.star.faces, octahedron: S.oct.faces, stella: S.stella.faces, pacioli: S.rects.faces };
// Content of a cell: all six solids, rotated by R (about the cell centre) — returns the face keys of the cell's content (no translation)
const contentKeys = (M) => { const set = new Set(); for (const [t, faces] of Object.entries(SOLIDS)) for (const f of faces) set.add(fk(t, f.map(p => apply(M, p)))); return set; };
const keysEq = (A, B) => A.size === B.size && [...A].every(k => B.has(k));
const par = c => ((c[0]+c[1]+c[2]) % 2 + 2) % 2;
const Rof = c => par(c) === 1 ? Rz : I3;
const W = 2, cells = [];
for (let i = -W; i <= W; i++) for (let j = -W; j <= W; j++) for (let k = -W; k <= W; k++) cells.push([i,j,k]);
const inWin = c => c.every(x => Math.abs(x) <= W);
const base = { I: contentKeys(I3), R: contentKeys(Rz) };
const cache = new Map(); const contentOf = (r) => cache.get(r) ?? (cache.set(r, contentKeys(r === 'R' ? Rz : I3)), cache.get(r));
const ops = [];
const transl = [[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]];
for (const O of Oh) for (const t of transl) {
  let ok = true;
  for (const c of cells) {
    const g = apply(O, c).map((x, k) => x + t[k]);
    if (!inWin(g)) continue;
    // O applied to the content of c (rotated by its parity), must equal the content of g (rotated by its parity)
    const img = new Set();
    const mapped = contentOf(par(c) === 1 ? 'R' : 'I');
    for (const k of mapped) { const [type, rest] = [k.slice(0, k.indexOf('|')), k.slice(k.indexOf('|') + 1)]; const pts = rest.split('|').map(s => s.split(',').map(Number)); img.add(fk(type, pts.map(p => apply(O, p)))); }
    const target = contentOf(par(g) === 1 ? 'R' : 'I');
    if (!keysEq(img, target)) { ok = false; break; }
  }
  if (ok) ops.push({ O, t });
}
const key = M => M.flat().join(',');
const pointOps = new Set(ops.map(o => key(o.O)));
const swaps = ops.filter(o => (o.t[0]+o.t[1]+o.t[2]) % 2 === 1);
console.log('six contents, checkerboard: operations', ops.length, '| point operations', pointOps.size, '| swap operations (odd translation)', swaps.length);
console.log('translations (mod 2):', JSON.stringify([...new Set(ops.filter(o => key(o.O) === key(I3)).map(o => o.t.join(',')))]));
const isF = v => v.every(Number.isInteger) && ((v[0] + v[1] + v[2]) % 2 === 0);
let symmorphic = false;
for (const p of [[0,0,0],[0.5,0.5,0.5]]) {
  let ok = true; for (const { O, t } of ops) { const Op = apply(O, p); if (!isF([0,1,2].map(i => t[i] - (p[i] - Op[i])))) { ok = false; break; } }
  if (ok) symmorphic = true;
}
console.log('symmorphic about a common point:', symmorphic);
