// Builds src/app/octet-truss-data.js for the world "The OG on the Octet Truss" (DICTO 2026-10-19; paper #37, DICTO DOI 10.5281/zenodo.23457016).
// The pieces are the exact-checked meshes of the study 3D pages (branch research: studies/2026-10-18-ocd-octet, -p1-golden-key-octet,
// -p2-penrose-core-octet, -p3-golden-envelope-octet, -p4-golden-octet-adaptor), read straight from the pages' scenes so the app shows
// the paper's geometry: each kit's "round one OG" assembly as placed there, and from it one lattice cell's worth of pieces (items that
// differ by an fcc vector R(a, b, c), a + b + c even, are the same item), which the world repeats to grow the network.
// Usage (dicto-node, needs Playwright): node scripts/build-octet-truss-data.mjs <research checkout root> [out]
import { chromium } from 'playwright';
import fs from 'node:fs';
const [ROOT, OUT = 'src/app/octet-truss-data.js'] = process.argv.slice(2);
const R = 2 * (1 + Math.sqrt(5)) / 2 / 3;   // 2φ/3: the octahedron |x| + |y| + |z| ≤ R, fcc vectors R(1, 1, 0)
const S = (p) => `${ROOT}/studies/${p}`;
const P1 = S('2026-10-18-p1-golden-key-octet/renders/p1-golden-key-octet.html'), P2 = S('2026-10-18-p2-penrose-core-octet/renders/p2-penrose-core-octet.html');
const P3 = S('2026-10-18-p3-golden-envelope-octet/renders/p3-golden-envelope-octet.html'), P4 = S('2026-10-18-p4-golden-octet-adaptor/renders/p4-golden-octet-adaptor.html');
const OC = S('2026-10-18-ocd-octet/renders/step10-pieces.html');
// kit: family, page, its set view (or null: one of each piece, laid out), its round-one-OG view, or a fixed view (the chamber)
const KITS = [
  { id: 'keys', fam: 'keys', page: P1, set: 'The set (2 shapes)', round: 'Round one octahedron' },
  { id: 'penrose', fam: 'penrose', page: P2, set: 'The set (3 shapes)', round: 'Round one octahedron' },
  { id: 'cores', fam: 'penrose', page: OC, set: null, round: "Keyless kit, 3 Penrose cores (DICTO's choice)" },
  { id: 'grown', fam: 'envelopes', page: P3, set: null, round: '3 · Two-shape set' },
  { id: 'halves', fam: 'envelopes', page: P4, set: null, round: 'Two shapes: envelope + adaptor half', closed: ['half'] },   // the page shows the halves pulled apart
  { id: 'one', fam: 'envelopes', page: P4, set: null, round: 'One piece, see-through' },
  { id: 'chamber', fam: 'envelopes', page: P4, fixed: 'Chamber, cut open' },
  { id: 'envW', fam: 'glue', page: P4, set: 'Envelope + W, the set', round: 'Envelope + W (Fable)' },
  { id: 'ogW', fam: 'glue', page: P4, set: 'OCD + W, the set', round: 'OCD + W with OCD imprints' },
  { id: 'starW', fam: 'glue', page: P4, set: 'Star-centred W, the set', round: 'OCD + W centred on the Penrose star' },
];
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 900, height: 900 } });
const wrap = (f) => 'data:text/html;base64,' + Buffer.from('<!doctype html><meta charset=utf-8>' + fs.readFileSync(f, 'utf8')).toString('base64');
const geoms = {}, byHash = {};   // name -> {v, t, c, o}; vertex hash -> name (the same solid on two pages is stored once)
let last = null;
async function grab(f, label) {
  if (last !== f) { await page.goto(wrap(f)); await page.waitForTimeout(2500); last = f; }
  return page.evaluate((label) => {
    const btn = [...document.querySelectorAll('#btns button')].find((x) => x.textContent.trim() === label);
    if (!btn) throw new Error('no view ' + label); btn.click();
    const e = document.getElementById('ex'); if (e) { e.value = 0; e.dispatchEvent(new Event('input')); }
    const name = new Map(Object.entries(G).map(([k, g]) => [g, k]));
    const out = [];
    world.updateMatrixWorld(true);
    world.traverse((m) => {
      if (!m.isMesh || !m.visible) return;
      const k = name.get(m.geometry); if (!k) return;
      const pos = m.geometry.attributes.position.array;
      out.push({ k, m: [...m.matrixWorld.elements], pos: k in (window.__sent ??= {}) ? null : Array.from(pos),
        c: m.material.color.getHex(), o: m.material.transparent ? m.material.opacity : 1 });
      window.__sent[k] = 1;
    });
    return out;
  }, label);
}
const r6 = (x) => Math.round(x * 1e6) / 1e6;
function store(f, it) {
  const key = `${f}|${it.k}`;
  if (!geoms[key]) {
    if (!it.pos) throw new Error('missing geometry ' + key);
    const v = [], t = [], idx = new Map();
    for (let i = 0; i < it.pos.length; i += 9) {
      const tri = [0, 1, 2].map((j) => {
        const p = [it.pos[i + 3 * j], it.pos[i + 3 * j + 1], it.pos[i + 3 * j + 2]].map(r6), h = p.join();
        if (!idx.has(h)) { idx.set(h, v.length); v.push(p); }
        return idx.get(h);
      });
      if (new Set(tri).size === 3) t.push(tri);
    }
    const h = JSON.stringify(v);
    geoms[key] = byHash[h] ?? { name: `${it.k}`, v, t, c: it.c, o: it.o, alias: [] };
    byHash[h] = geoms[key];
  }
  return geoms[key];
}
const apply = (m, p) => [m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12], m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13], m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14]];
const pieces = [], pid = new Map();
const idOf = (g) => { if (!pid.has(g)) { pid.set(g, pieces.length); pieces.push(g); } return pid.get(g); };
// an item: [piece, 12 numbers (3×3 linear part by rows, then the translation)], plus its centre for pull-apart and the network radius
function item(f, it) {
  const g = store(f, it), m = it.m;
  // the solid's own centre of volume (the corner average depends on how the boolean mesh was triangulated)
  const V = g.v.map((p) => apply(m, p)); let vol = 0; const cs = [0, 0, 0];
  for (const [a, b2, c] of g.t) {
    const A = V[a], B = V[b2], C = V[c], d = (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0]) + A[2] * (B[0] * C[1] - B[1] * C[0])) / 6;
    vol += d; for (let k = 0; k < 3; k++) cs[k] += d * (A[k] + B[k] + C[k]) / 4;
  }
  const cen = cs.map((x) => x / vol);
  return { vol: Math.abs(vol), p: idOf(g), M: [m[0], m[4], m[8], m[1], m[5], m[9], m[2], m[6], m[10], m[12], m[13], m[14]].map(r6), cen: cen.map(r6), c: it.c, o: it.o };
}
// two items of the same volume whose centres of volume are one fcc vector apart are the same item of the tiling, whatever piece
// name and turn the page used (e.g. a flanking core placed by the inversion is the other flank's translate)
function unitCell(items) {
  const unit = [];
  for (const it of items) {
    const dup = unit.some((u) => {
      const d = u.cen.map((x, i) => (x - it.cen[i]) / R), n = d.map(Math.round);
      return Math.abs(u.vol - it.vol) < 1e-5 && d.every((x, i) => Math.abs(x - n[i]) < 1e-4) && (n[0] + n[1] + n[2]) % 2 === 0;
    });
    if (!dup) unit.push(it);
  }
  return unit;
}
function layout(items) {   // one of each piece, side by side, as turned in the assembly
  const seen = new Map();
  for (const it of items) if (!seen.has(it.p)) seen.set(it.p, it);
  const lin = (it) => [it.M[0], it.M[3], it.M[6], 0, it.M[1], it.M[4], it.M[7], 0, it.M[2], it.M[5], it.M[8], 0, 0, 0, 0, 1];
  let x = 0; const out = [];
  [...seen.values()].forEach((it, i) => {
    const P = pieces[it.p].v.map((p) => apply(lin(it), p)), c = P.reduce((a, p) => a.map((s, j) => s + p[j]), [0, 0, 0]).map((s) => s / P.length);
    const r = Math.max(...P.map((p) => Math.hypot(p[0] - c[0], p[1] - c[1], p[2] - c[2])));
    if (i) x += r;
    out.push({ ...it, M: [...it.M.slice(0, 9), x - c[0], -c[1], -c[2]].map(r6), cen: [x, 0, 0] }); x += r + 0.15;
  });
  const mid = (x - 0.15) / 2;
  return out.map((it) => ({ ...it, M: [...it.M.slice(0, 9), r6(it.M[9] - mid), it.M[10], it.M[11]], cen: [r6(it.cen[0] - mid), 0, 0] }));
}
// Point inside a placed piece (ray parity; the meshes are closed). Used to rebuild the keyless three-core kit: the study page's
// assembly (step10, "Keyless kit, 3 Penrose cores") places its caps, rests and tetrahedra by all 24 operations of Th, which these
// notched pieces do not all share, so it holds overlapping wrong copies (its cell sums to 5.5079, not 2.5103). The right copies are
// the ones inside the Penrose-core kit's own pieces (P2, whose cell sums exactly): caps inside the notched octahedron, cores and rests
// inside a middle piece; the tetrahedra are P2's.
const linOf = (it) => [it.M[0], it.M[3], it.M[6], 0, it.M[1], it.M[4], it.M[7], 0, it.M[2], it.M[5], it.M[8], 0, it.M[9], it.M[10], it.M[11], 1];
const placed = (it) => { const V = pieces[it.p].v.map((p) => apply(linOf(it), p)); return { V, T: pieces[it.p].t }; };
function inside(sol, q) {
  const d = [0.5773, 0.6181, 0.5331], n = Math.hypot(...d); const D = d.map((x) => x / n); let hits = 0;
  for (const [a, b, c] of sol.T) {
    const A = sol.V[a], B = sol.V[b], C = sol.V[c], e1 = B.map((x, i) => x - A[i]), e2 = C.map((x, i) => x - A[i]);
    const pv = [D[1] * e2[2] - D[2] * e2[1], D[2] * e2[0] - D[0] * e2[2], D[0] * e2[1] - D[1] * e2[0]], det = e1[0] * pv[0] + e1[1] * pv[1] + e1[2] * pv[2];
    if (Math.abs(det) < 1e-12) continue;
    const tv = q.map((x, i) => x - A[i]), u = (tv[0] * pv[0] + tv[1] * pv[1] + tv[2] * pv[2]) / det; if (u < 0 || u > 1) continue;
    const qv = [tv[1] * e1[2] - tv[2] * e1[1], tv[2] * e1[0] - tv[0] * e1[2], tv[0] * e1[1] - tv[1] * e1[0]], v = (D[0] * qv[0] + D[1] * qv[1] + D[2] * qv[2]) / det;
    if (v < 0 || u + v > 1) continue;
    if ((e2[0] * qv[0] + e2[1] * qv[1] + e2[2] * qv[2]) / det > 1e-9) hits++;
  }
  return hits % 2 === 1;
}
// points just inside a placed piece: the centre of every triangle, pushed 2e-3 inwards
function samples(it) {
  const { V, T } = placed(it), out = [];
  const tri = T.map(([a, b, c]) => { const e1 = V[b].map((x, i) => x - V[a][i]), e2 = V[c].map((x, i) => x - V[a][i]);
    const nv = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]; return { a, b, c, nv, A: Math.hypot(...nv) }; })
    .filter((t) => t.A > 1e-9);
  const sol = { V, T };
  for (const t of tri) {
    const m = [0, 1, 2].map((i) => (V[t.a][i] + V[t.b][i] + V[t.c][i]) / 3), u = t.nv.map((x) => x / t.A);
    for (const s of [-2e-3, 2e-3]) { const q = m.map((x, i) => x + s * u[i]); if (inside(sol, q)) { out.push(q); break; } }
  }
  return out;
}
const within = (it, refs) => { const q = samples(it); return q.length > 0 && q.every((x) => refs.some((r) => inside(r, x))); };
const kits = {};
for (const k of KITS) {
  const take = async (label) => (await grab(k.page, label)).map((it) => item(k.page, it));
  if (k.fixed) { kits[k.id] = { fam: k.fam, fixed: await take(k.fixed) }; continue; }
  let round = await take(k.round);
  if (k.closed) round = round.map((it) => (k.closed.includes(pieces[it.p].name) ? { ...it, M: [...it.M.slice(0, 9), 0, 0, 0], cen: it.cen.map((x, i) => r6(x - it.M[9 + i])) } : it));
  kits[k.id] = { fam: k.fam, set: k.set ? await take(k.set) : layout(round), round, unit: unitCell(round) };
}
await b.close();
{
  // per place, keep the one copy of each piece whose own volume lies in the right region (random points inside the copy):
  // a cap inside the notched octahedron and outside the OG, a core or rest inside the middle piece there
  const p2 = kits.penrose, nm = (it) => pieces[it.p].name;
  const no = p2.round.filter((it) => nm(it) === 'no').map(placed), mids = p2.round.filter((it) => nm(it) === 'mid').map(placed);
  const og = kits.cores.round.filter((it) => nm(it) === 'k_ocd').map(placed);
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  function score(it, ok) {
    const sol = placed(it), lo = [0, 1, 2].map((k) => Math.min(...sol.V.map((v) => v[k]))), hi = [0, 1, 2].map((k) => Math.max(...sol.V.map((v) => v[k])));
    let n = 0, good = 0;
    for (let tries = 0; n < 60 && tries < 6000; tries++) {
      const q = lo.map((a, k) => a + rnd() * (hi[k] - a)); if (!inside(sol, q)) continue;
      n++; if (ok(q)) good++;
    }
    return n ? good / n : 0;
  }
  const okCap = (q) => no.some((r) => inside(r, q)) && !og.some((r) => inside(r, q));
  const okMid = (q) => mids.some((r) => inside(r, q));
  const groups = new Map();
  for (const it of kits.cores.round) {
    const n = nm(it); if (n === 'k_ocd' || n.startsWith('k_tet')) continue;
    const key = n + '|' + it.cen.map((x) => Math.round(x / 0.3)).join();   // copies at one place sit within ~0.1 of each other
    (groups.get(key) ?? groups.set(key, []).get(key)).push(it);
  }
  const keep = [kits.cores.round.find((it) => nm(it) === 'k_ocd')];
  for (const [key, list] of groups) {
    const ok = key.startsWith('k_cap') ? okCap : okMid;
    const best = list.map((it) => [score(it, ok), it]).sort((a, b2) => b2[0] - a[0])[0];
    if (best[0] < 0.97) console.log('warning: best copy only', best[0].toFixed(3), key);
    keep.push(best[1]);
  }
  const c = kits.cores; c.round = keep.concat(p2.round.filter((it) => nm(it).startsWith('tet'))); c.unit = unitCell(c.round); c.set = layout(c.round);
}
// colours: each piece keeps the colour and glass of its first use
const pack = (list) => list.map((it) => [it.p, ...it.M, ...it.cen]);
const data = { R, pieces: pieces.map((g) => ({ name: g.name, c: g.c, o: g.o, v: g.v, t: g.t })),
  kits: Object.fromEntries(Object.entries(kits).map(([id, k]) => [id, Object.fromEntries(Object.entries(k).map(([n, v]) => [n, typeof v === 'string' ? v : pack(v)]))])) };
fs.writeFileSync(OUT, '// Generated by scripts/build-octet-truss-data.mjs (The OG on the Octet Truss, DICTO 2026-10-19; paper #37). Do not edit.\n'
  + '// Items: [piece, 3×3 linear part by rows, translation, centre].\nexport default ' + JSON.stringify(data) + ';\n');
for (const [id, k] of Object.entries(kits)) console.log(id, Object.fromEntries(Object.entries(k).filter(([, v]) => Array.isArray(v)).map(([n, v]) => [n, v.length])));
console.log('pieces', pieces.map((g, i) => `${i}:${g.name}(${g.t.length})`).join(' '), (fs.statSync(OUT).size / 1024).toFixed(0) + ' KB');
