// Control for the fix: the picker's new vacuusPlanes against the independent count of fins.js (distinct planes, both) on all dice,
// and Lucky 7 (No. 5) against #120's truncated-octahedron row (15 plates, 15 full, 7 Resonus, 3 both). With Claude (Anthropic).
const path = require('path'), K = process.argv[2];
const G = require(path.join(K, 'aequi/geom.js')), data = require(path.join(K, 'aequi/dice.json')); G.prepare(data);
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], dot = (a, b) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const unit = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
let bad = 0, n = 0, kinds = { full: 0, shared: 0, fin: 0 }, L7 = null;
(data.dice || data).forEach(e => {
  const S = G.buildSolid(G.planesFor(data, e)), P = G.vacuusPlanes(S), V = [];
  S.edges.forEach(ed => { const m = unit(cross(S.verts[ed[0]], S.verts[ed[1]])); if (!V.some(q => Math.abs(Math.abs(dot(q, m)) - 1) < 1e-9)) V.push(m); });
  const edgesCovered = P.reduce((t, p) => t + p.edges.length, 0);
  if (P.length !== V.length || edgesCovered !== S.edges.length) bad++;
  P.forEach(p => kinds[p.kind]++); n++;
  if (e.k === 4) L7 = { plates: P.length, full: P.filter(p => p.kind === 'full').length, both: P.filter(p => p.both).length, res: G.resonusPlates(S).length };
});
console.log('dice', n, 'mismatches', bad, 'kinds over all plates', JSON.stringify(kinds));
console.log('Lucky 7', JSON.stringify(L7), '(#120 truncated octahedron: 15 plates, 15 full, 7 Resonus, 3 both)');
const ok = bad === 0 && L7 && L7.plates === 15 && L7.full === 15 && L7.both === 3 && L7.res === 7;
console.log(ok ? 'FINAL ok' : 'FINAL FAIL');
