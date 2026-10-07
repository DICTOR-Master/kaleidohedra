// Merged outer surface of a 3x3x3 block, with odd cubes turned (v2) and unturned (for comparison):
// each face's stored normal agrees with its winding and points outward; the surface is closed
// (the enclosed volume is the same from two reference points); the volume matches a Monte Carlo
// estimate of the union.
import { roofFoldSolids, turnPoint, mergedDodecaSurface } from '../../src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
const dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
const sub = (a, b) => [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
const add = (a, b) => [a[0]+b[0], a[1]+b[1], a[2]+b[2]];
const scl = (a, s) => [a[0]*s, a[1]*s, a[2]*s];
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
const len = a => Math.hypot(...a);
const unit = a => scl(a, 1 / len(a));
const odd = s => ((s[0]+s[1]+s[2]) % 2 + 2) % 2 === 1;
const sites = [];
for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) for (let k = -1; k <= 1; k++) sites.push([i, j, k]);
// Outward dodecahedron planes at a site, turned when the site is turned.
const planesOf = (s, turned) => S.dodeca.faces.map(f => {
  const g = turned ? f.map(turnPoint) : f;
  let n = unit(cross(sub(g[1], g[0]), sub(g[2], g[0])));
  const c = scl(g.reduce(add), 1 / g.length);
  if (dot(n, c) < 0) n = scl(n, -1);
  return { n, d: dot(n, add(g[0], scl(s, 2))) };
});
const cache = new Map();
const P = (s, t) => { const k = s.join() + (t ? 'T' : 'P'); if (!cache.has(k)) cache.set(k, planesOf(s, t)); return cache.get(k); };
const inUnion = (x, turnedFn) => sites.some(s => P(s, turnedFn(s)).every(({ n, d }) => dot(n, x) <= d + 1e-9));
const signedVolume = (pieces, o) => {
  let v = 0;
  for (const { polygon } of pieces) {
    const a0 = sub(polygon[0], o);
    for (let i = 1; i + 1 < polygon.length; i++) v += dot(a0, cross(sub(polygon[i], o), sub(polygon[i + 1], o))) / 6;
  }
  return v;
};
const R = 6, N = 600000;
for (const [label, turnedFn] of [['unturned', () => false], ['v2 (odd cubes turned)', odd]]) {
  const pieces = mergedDodecaSurface(sites, turnedFn);
  let mismatch = 0, notOutward = 0;
  for (const { site, polygon, normal } of pieces) {
    const w = unit(cross(sub(polygon[1], polygon[0]), sub(polygon[2], polygon[0])));
    if (dot(w, normal) <= 0) mismatch++;
    const c = scl(polygon.reduce(add), 1 / polygon.length), e = 1e-3;
    if (inUnion(add(c, scl(normal, e)), turnedFn) || !inUnion(sub(c, scl(normal, e)), turnedFn)) notOutward++;
  }
  const v1 = signedVolume(pieces, [0, 0, 0]), v2 = signedVolume(pieces, [0.37, -0.21, 0.13]);
  let hits = 0;
  for (let t = 0; t < N; t++) if (inUnion([-R + 2*R*Math.random(), -R + 2*R*Math.random(), -R + 2*R*Math.random()], turnedFn)) hits++;
  const mc = (2*R)**3 * hits / N, se = (2*R)**3 * Math.sqrt(hits) / N;
  console.log(`${label}: faces ${pieces.length}; winding/normal mismatches ${mismatch}; not outward ${notOutward}; `
    + `closure difference ${Math.abs(v1 - v2).toExponential(1)}; surface volume ${v1.toFixed(3)}; union (Monte Carlo) ${mc.toFixed(2)} +/- ${se.toFixed(2)}`);
}
