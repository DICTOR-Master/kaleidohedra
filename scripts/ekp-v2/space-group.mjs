// Space-group type from the exact operations in ops.json (written by symmetry-compare.mjs).
// Each reflection (det -1, trace 1) has a normal along a cube axis (family <100>) or along a face
// diagonal (family <110>). Its glide is classed as a mirror (no translation in the plane), an axial
// glide (half a cube-axis translation in the plane: a, b or c) or a diagonal glide (d or n).
// Per family the Hermann-Mauguin letter is the highest class present: mirror, then axial, then diagonal.
import { readFileSync } from 'node:fs';
const ops = JSON.parse(readFileSync(new URL('./ops.json', import.meta.url), 'utf8'));
const apply = (M, v) => [0, 1, 2].map(i => M[i][0]*v[0] + M[i][1]*v[1] + M[i][2]*v[2]);
const dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
const det = M => M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);
const trace = M => M[0][0] + M[1][1] + M[2][2];
const isInt = v => v.every(c => Math.abs(c - Math.round(c)) < 1e-9);
// The normal of a reflection: the vector n with components in {-1, 0, 1} and O n = -n.
function normalOf(O) {
  for (const a of [-1, 0, 1]) for (const b of [-1, 0, 1]) for (const c of [-1, 0, 1]) {
    const n = [a, b, c];
    if ((a || b || c) && apply(O, n).every((x, i) => x === -n[i])) return n;
  }
  throw new Error('reflection without a normal');
}
// Glide class of (O, t) with normal n. The translation is split into its part parallel to the plane, which
// is what distinguishes the glide types; the lattice is primitive (P) or face-centred (F).
function glideClass(t, n, lattice) {
  const p = t.map((x, i) => x - (dot(t, n) / dot(n, n)) * n[i]);
  const inPlane = v => isInt(v) && Math.abs(dot(v, n)) < 1e-9 && (lattice === 'P' || Math.abs((v[0] + v[1] + v[2]) % 2) < 1e-9);
  if (inPlane(p)) return 'mirror';
  const j = n.indexOf(0); // a cube axis lying in the plane
  const prim = [0, 1, 2].map(i => (i === j ? (lattice === 'F' ? 2 : 1) : 0)); // shortest in-plane translation along it
  if (inPlane(p.map((x, i) => x - prim[i] / 2))) return 'axial';
  return 'diagonal';
}
const familyOf = n => n.map(Math.abs).sort().join(''); // '001' = <100>, '011' = <110>
const letterOf = c => (c.mirror ? 'm' : c.axial ? 'c' : c.diagonal ? 'd' : '');
const KNOWN = { 'Pm-3': 200, 'Fm-3': 202, 'Fm-3m': 225, 'Fm-3c': 226, 'Fd-3m': 227, 'Fd-3c': 228 };
const labels = { original: 'identical cells, unturned', network: 'stars on even cubes, icosahedra on odd cubes', v2: 'checkerboard: odd cubes turned 90 degrees' };
for (const name of ['original', 'network', 'v2']) {
  const lattice = name === 'original' ? 'P' : 'F';
  const counts = { '001': {}, '011': {} };
  let reflections = 0;
  for (const { O, t } of ops[name]) {
    if (det(O) !== -1 || trace(O) !== 1) continue;
    reflections++;
    const n = normalOf(O);
    const k = glideClass(t, n, lattice);
    counts[familyOf(n)][k] = (counts[familyOf(n)][k] || 0) + 1;
  }
  const symbol = `${lattice}${letterOf(counts['001'])}-3${letterOf(counts['011'])}`;
  console.log(`== ${labels[name]}`);
  console.log(`   reflections: ${reflections}`);
  console.log(`   <100> family: ${JSON.stringify(counts['001'])}`);
  console.log(`   <110> family: ${JSON.stringify(counts['011'])}`);
  console.log(`   symbol: ${symbol}${KNOWN[symbol] ? ` (No. ${KNOWN[symbol]})` : ''}`);
}
