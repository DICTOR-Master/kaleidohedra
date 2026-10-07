// Roof node rule (DISCOVERIES #8): every roof vertex of a cube is an icosahedron vertex of a neighbouring cube.
// Counts, for a representative even and odd cube, the roof vertices that coincide with an icosahedron vertex of one
// of the 26 neighbouring cubes: variation A (unturned) and variation B (odd cubes turned by the app's turnPoint).
import { roofFoldSolids, turnPoint, siteParity } from '../../src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
const uniq = P => { const m = new Map(); for (const p of P) m.set(p.map(c => c.toFixed(6)).join(), p); return [...m.values()]; };
const DV = uniq(S.dodeca.faces.flat()), IV = uniq(S.ico.faces.flat());
const ROOF = DV.filter(p => Math.max(...p.map(Math.abs)) > 1 + 1e-6); // dodecahedron vertices outside the cube
const key = p => p.map(x => (Math.round(x * 1e6) / 1e6 + 0).toFixed(6)).join(',');
const turned = (c, variant) => variant === 'B' && siteParity(...c) === 1;
const toGlobal = (p, c, variant) => (turned(c, variant) ? turnPoint(p) : p).map((x, i) => x + 2 * c[i]);
const nbrs = [];
for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) for (let k = -1; k <= 1; k++) if (i || j || k) nbrs.push([i, j, k]);
function iceOfNeighbours(c, variant) {
  const set = new Set();
  for (const n of nbrs) { const g = [c[0] + n[0], c[1] + n[1], c[2] + n[2]]; for (const v of IV) set.add(key(toGlobal(v, g, variant))); }
  return set;
}
const matched = (c, variant) => { const ice = iceOfNeighbours(c, variant); return ROOF.filter(r => ice.has(key(toGlobal(r, c, variant)))).length; };
console.log(`roof vertices per cube ${ROOF.length}; icosahedron vertices per cube ${IV.length}`);
for (const variant of ['A', 'B']) for (const c of [[0, 0, 0], [1, 0, 0]]) {
  console.log(`${variant} cube ${c.join(',')} (${siteParity(...c) ? 'odd' : 'even'}): roof vertices on a neighbour's icosahedron vertex: ${matched(c, variant)} of ${ROOF.length}`);
}
console.log('every even cube is a translate of 0,0,0 and every odd cube of 1,0,0, so these cover all cubes');
// Edge directions of the dodecahedron (its edges lie on the icosahedron's 2-fold axes): unturned cells vs turned cells.
const d2 = (p, q) => Math.hypot(...p.map((x, i) => x - q[i]));
const minD = Math.min(...DV.flatMap((p, i) => DV.slice(i + 1).map(q => d2(p, q))));
const dirs = (f) => {
  const set = new Set();
  DV.forEach((p, i) => DV.slice(i + 1).forEach(q => {
    if (Math.abs(d2(p, q) - minD) > 1e-6) return;
    const v = f(q).map((x, k) => x - f(p)[k]), n = Math.hypot(...v);
    let u = v.map(x => x / n);
    if (u.find(x => Math.abs(x) > 1e-9) < 0) u = u.map(x => -x);
    set.add(u.map(x => (Math.round(x * 1e6) / 1e6 + 0).toFixed(6)).join(','));
  }));
  return set;
};
const D0 = dirs(p => p), D1 = dirs(p => turnPoint(p));
const shared = [...D0].filter(k => D1.has(k)).length;
console.log(`edge directions: unturned cell ${D0.size}; turned cell ${D1.size}; shared ${shared}; variation A ${D0.size}; variation B ${new Set([...D0, ...D1]).size}`);
