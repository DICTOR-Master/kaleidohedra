// DICTO 28 Nov: "Lucky 7 ... I think it is a mistake throughout the catalog as all seem to have too many fins for the numbers".
// For each catalogued die: edges (= Vacuus triangles the picker draws and counts as "plates"), distinct Vacuus PLANES (#120's plates:
// planes through O and an edge; opposite edges share one), Resonus planes, and planes in both. With Claude (Anthropic).
const path = require('path'), K = process.argv[2];
const G = require(path.join(K, 'aequi/geom.js')), data = require(path.join(K, 'aequi/dice.json'));
G.prepare(data);
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], dot = (a, b) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const unit = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
function planes(S) {
  const V = [], R = [];
  const add = (L, n) => { if (!L.some(m => Math.abs(Math.abs(dot(m, n)) - 1) < 1e-9)) L.push(n); };
  S.edges.forEach(e => add(V, unit(cross(S.verts[e[0]], S.verts[e[1]]))));
  S.faces.forEach(f => add(R, unit(f.n)));
  const both = V.filter(n => R.some(m => Math.abs(Math.abs(dot(m, n)) - 1) < 1e-9)).length;
  return { edges: S.edges.length, vac: V.length, res: R.length, both };
}
let tot = 0, fewer = 0, lucky = [];
const dice = data.dice || data.list || data;
dice.forEach((e, i) => {
  const S = G.buildSolid(G.planesFor(data, e)); const p = planes(S); tot++;
  if (p.vac < p.edges) fewer++;
  if (e.k === 4 && lucky.length < 6) lucky.push({ i, g: e.g, faces: S.faces.length, ...p });
});
console.log('dice', tot, '; dice whose distinct Vacuus planes < edges (picker over-counts "plates"):', fewer);
console.log('Lucky 7 examples:', JSON.stringify(lucky));
console.log(tot > 0 ? 'FINAL ok' : 'FINAL FAIL');
