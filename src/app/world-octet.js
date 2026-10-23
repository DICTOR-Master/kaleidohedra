// DICTO Icosahedral Octet (DICTO 2026-10-13; DISCOVERIES F21): Euclid's roofs moved to the icosahedron, as networks that grow with a
// Size slider, on the shared layered-world engine (Pull apart, Crystal, X-ray). Cells from src/app/octet-data.js (built and checked by
// scripts/build-octet-data.py; site rules checked by studies/2026-10-10-icosa-networks-3/octet-sites-check.py). Names by DICTO:
// Admiral Cap, Weirdstone, Tadpole, Frog Chorus, Lotus Jewel, Unborn. The AXE gap (DICTO 2026-10-23, study 2026-10-23-axe-gap): on the
// simple cubic lattice the gap between the icosahedra (or Lotus Jewels) and the void pieces is exactly 6 AXE per cell, so the Lotus
// Jewel network, its twin (whole icosahedra and Unborns) and the four-kind network (Lotus Jewel, Tricap, Unborn, AXE) fill space;
// the AXE can be hidden. Mixed blocks (DICTO 2026-10-23): each Tricap given to its icosahedron or to its dodecahedron by a pattern of
// blocks; every such choice fills space. Golden split (DICTO 2026-10-23, study 2026-10-23-shadow-forms): every AXE coned from the point
// 1/phi along its axis, its 4 pyramids joining the icosahedra and Unborns, so the network is two truncated octahedra (Icosaxes and
// Unborn Axes, names by DICTO; with keys Lotus Jewel Axes and Dodecaxes; Polyhedraverse's DICTO's pieces, krp-core golden-split.js); each hexagon between them flat or keyed by a Tricap either way, by a
// pattern or a tap. Words: i18n octet.*.
import OCTET from './octet-data.js';
import { SIGNS, FLAT, INTO_BIG, INTO_SMALL, pieceParts, pieceSurface, toPolygons } from '../krp-core/src/polyhedra/golden-split.js';
import { createLayeredWorld } from './world-chains.js';

const { a: A, phi: PHI, cells: C } = OCTET;
const KINDS = ['caps', 'allIco', 'frog', 'pyrochlore', 'lotusJewel', 'icoUnborn', 'axeNet', 'mixed', 'goldenSplit'];
const range = (k) => Array.from({ length: 2 * k + 1 }, (_, i) => i - k);
const near = (p, r) => Math.hypot(...p) <= r + 1e-9;
// One cell at a place, or turned inside out through its middle (the octet's other tetrahedra).
const put = (cell, t, invert = false, role = null) => cell.map(([r, V, F]) => [role ?? r,
  V.map((v) => v.map((x, i) => (invert ? -x : x) + t[i])), invert ? F.map((f) => [...f].reverse()) : F]);
// Octahedra at (a/2)n, n with even sum; corners of the truss at odd sum; tetrahedra at (a/4)s, s odd, turned when sum(s) = 1 mod 4.
function octSites(r) {
  const out = [], k = Math.ceil(r / (A / 2));
  for (const x of range(k)) for (const y of range(k)) for (const z of range(k)) {
    const p = [x, y, z].map((c) => (c * A) / 2);
    if (near(p, r)) out.push({ p, even: (x + y + z) % 2 === 0 });
  }
  return out;
}
function tetSites(r) {
  const out = [], k = Math.ceil(r / (A / 4)) | 1;
  const odd = range(k).filter((c) => Math.abs(c) % 2 === 1);
  for (const x of odd) for (const y of odd) for (const z of odd) {
    const p = [x, y, z].map((c) => (c * A) / 4);
    if (near(p, r)) out.push({ p, s: [x, y, z], invert: (((x + y + z) % 4) + 4) % 4 === 1 });
  }
  return out;
}
// Pyrochlore inside the octet: one tetrahedron of each turn at every corner, mirror images through it (1 in 8 of the tetrahedra).
export const pyro = (s) => [[1, 1, 1], [3, 3, 3]].some((b) => { const d = s.map((c, i) => c - b[i]); return d.every((c) => ((c % 4) + 4) % 4 === 0) && d.reduce((t, c) => t + c / 4, 0) % 2 === 0; });
const R = (size) => size * (A / 2) * 1.01;
// The simple cubic networks (Lotus Jewel and its twins): sites n (phi/2), icosahedra at even n, voids at odd n, within the size's
// ball. Lotus Jewel network: Lotus Jewels + void dodecahedra; icoUnborn: icosahedra + Unborns; axeNet: Lotus Jewels, each with its
// 8 Tricaps, + Unborns, each with the Tricaps whose icosahedron is not shown. In all three, the 2 AXE on each face between two shown
// voids (the gap: exactly 6 AXE per cell).
const centreOf = (V) => V.reduce((t, v) => t.map((c, i) => c + v[i] / V.length), [0, 0, 0]);
const sign = (v) => v.map((c) => Math.sign(c));
const AXE_FACE = [C.axeX, C.axeY, C.axeZ];
export function scSites(size) {
  const r = size * PHI * 1.01, k = 2 * size + 1, ico = new Map(), voids = new Map();
  for (const x of range(k)) for (const y of range(k)) for (const z of range(k)) {
    const n = [x, y, z], par = n.map((c) => Math.abs(c) % 2);
    if (par.some((c) => c !== par[0]) || !near(n.map((c) => (c * PHI) / 2), r)) continue;
    (par[0] ? voids : ico).set(n.join(','), n);
  }
  return { ico, voids };
}
/** The pieces of a simple cubic network on given sites (Maps of n): [role, vertices, faces, n of the site it belongs to]. Shared with
 *  the build world (world-octet-build.js), which passes the cells built. */
export function scPieces(kind, ico, voids) {
  const at = (n) => n.map((c) => (c * PHI) / 2), out = [];
  const add = (pieces, n) => out.push(...pieces.map((p) => [...p, n]));
  for (const n of ico.values()) {
    if (kind === 'icoUnborn') add(put(C.oct.slice(0, 1), at(n)), n);
    else add([...put(C.lotusJewel, at(n)), ...(kind === 'axeNet' ? put(C.tricap, at(n)) : [])], n);
  }
  for (const n of voids.values()) {
    if (kind === 'lotusJewel') { add(put(C.voidDodeca, at(n)), n); continue; }
    add(put(C.unborn, at(n)), n);
    if (kind === 'axeNet') {
      for (const t of C.tricap) {
        const owner = n.map((c, i) => c - sign(centreOf(t[1]))[i]);
        if (!ico.has(owner.join(','))) add(put([t], at(owner)), n);
      }
    }
  }
  for (const n of voids.values()) [0, 1, 2].forEach((a) => {
    const m = n.map((c, i) => c + (i === a ? 2 : 0));
    if (voids.has(m.join(','))) add(put(AXE_FACE[a], at(n.map((c, i) => c + (i === a ? 1 : 0)))), n);
  });
  return out;
}
const scNetwork = (kind) => (size) => { const { ico, voids } = scSites(size); return scPieces(kind, ico, voids); };

// ---- Mixed blocks (DICTO 2026-10-23; study 2026-10-23-axe-gap, point tests for every pattern, block size and swap) ----
// Every Tricap is exactly icosahedron ∩ dodecahedron and no two overlap, so giving each to its icosahedron or to its dodecahedron, any
// way at all, fills space (with the 6 AXE per cell). The pattern marks blocks of cells (block b: cells floor((c + floor(b/2))/b), so a
// block sits on the middle): a marked cell's dodecahedron keeps its 8 Tricaps (whole), the others give theirs to the icosahedra. Swap
// marks lattice points instead (the same blocks of points): a marked icosahedron keeps its 8 Tricaps, the rest go to the dodecahedra.
// Patterns: layers (z), rods (x + y), checker (x + y + z), pyrochlore (fcc(8) + (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1): the midpoints
// of the diamond fcc(8) + {0, (2,2,2)}, 16 blocks in 8^3, moved so the middle block is one).
const mod = (a, m) => ((a % m) + m) % m;
const PYRO_OFFSETS = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]];
export const MIXED_PATTERNS = {
  layers: (B) => mod(B[2], 2) === 0,
  rods: (B) => mod(B[0] + B[1], 2) === 0,
  checker: (B) => mod(B[0] + B[1] + B[2], 2) === 0,
  pyrochlore: (B) => PYRO_OFFSETS.some((o) => { const m = B.map((c, i) => mod(c + 1 - o[i], 8)); return m.every((c) => c % 4 === 0) && (m.reduce((t, c) => t + c, 0) / 4) % 2 === 0; }),
};
const blockOf = (c, b) => c.map((x) => Math.floor((x + Math.floor(b / 2)) / b));
const TRI_DIR = C.tricap.map((t) => sign(centreOf(t[1])));  // Tricap i of an icosahedron lies towards the void at n + TRI_DIR[i]
// An icosahedron keeping the Tricaps in mask (bit i: Tricap i): the Lotus Jewel with those windows closed by the icosahedron's corner
// faces; a dodecahedron keeping the Tricaps in mask (bit i: the Tricap i of the icosahedron at -TRI_DIR[i], i.e. on its corner
// -TRI_DIR[i]/(2 phi)): the Unborn with those Tricaps' apexes over its equilateral faces. One closed mesh each, faces outward.
const near0 = (p, q) => Math.hypot(...p.map((c, i) => c - q[i])) < 1e-6;
const cut = new Map();
function icoKeeping(mask) {
  const k = `i${mask}`;
  if (cut.has(k)) return cut.get(k);
  const [, JV, JF] = C.lotusJewel[0], V = JV.map((v) => [...v]);
  let F = JF.map((f) => [...f]);
  C.tricap.forEach(([, T], i) => {
    if (!(mask >> i & 1)) return;
    const apex = T.reduce((a, v) => (Math.hypot(...v) < Math.hypot(...a) ? v : a));
    const ai = V.findIndex((v) => near0(v, apex));
    const base = T.filter((v) => v !== apex).map((b) => V.findIndex((v) => near0(v, b)));
    F = F.filter((f) => !f.includes(ai));
    const [a, b, c] = base.map((j) => V[j]), n = [0, 1, 2].map((m) => (b[(m + 1) % 3] - a[(m + 1) % 3]) * (c[(m + 2) % 3] - a[(m + 2) % 3]) - (b[(m + 2) % 3] - a[(m + 2) % 3]) * (c[(m + 1) % 3] - a[(m + 1) % 3]));
    F.push(n.reduce((t, x, m) => t + x * a[m], 0) > 0 ? base : [...base].reverse());
  });
  cut.set(k, [V, F]);
  return [V, F];
}
function dodecaKeeping(mask) {
  const k = `d${mask}`;
  if (cut.has(k)) return cut.get(k);
  const [, UV, UF] = C.unborn[0], V = UV.map((v) => [...v]);
  let F = UF.map((f) => [...f]);
  C.tricap.forEach(([, T], i) => {
    if (!(mask >> i & 1)) return;
    const P = T.map((v) => v.map((c, m) => c - (TRI_DIR[i][m] * PHI) / 2));  // the Tricap moved into the dodecahedron's frame
    const tip = P.find((v) => !UV.some((u) => near0(u, v)));
    const base = P.filter((v) => v !== tip).map((b) => V.findIndex((v) => near0(v, b)));
    const fi = F.findIndex((f) => f.length === 3 && base.every((j) => f.includes(j)));
    const face = F[fi]; F.splice(fi, 1);
    V.push(tip); const t = V.length - 1;
    face.forEach((a, j) => F.push([a, face[(j + 1) % 3], t]));
  });
  cut.set(k, [V, F]);
  return [V, F];
}
const ALL = 255;
/** Mixed blocks on the sites of a size: { pattern, block, swap }. Void sites within the ball of size + 1, and the icosahedra whose 8 voids are
 *  all shown (so the network's skin is dodecahedra and Unborns). Roles: mxIco (whole icosahedron), mxJewel (Lotus Jewel), mxDodeca (whole
 *  dodecahedron), mxUnborn, mxTrans (an icosahedron or a dodecahedron keeping 1 to 7 Tricaps), axe. */
export function mixedPieces(size, { pattern = 'layers', block = 1, swap = false } = {}) {
  const marked = MIXED_PATTERNS[pattern];
  const { voids } = scSites(size + 1), ico = new Map(); // one cell wider than the other networks: the blocks need room
  for (const n of voids.values()) for (const d of TRI_DIR) {
    const m = n.map((c, i) => c - d[i]), key = m.join(',');
    if (!ico.has(key) && TRI_DIR.every((e) => voids.has(m.map((c, i) => c + e[i]).join(',')))) ico.set(key, m);
  }
  // does Tricap i of the icosahedron at m (towards the void m + TRI_DIR[i]) go to the dodecahedron?
  const toDodeca = (m, i) => (swap ? !marked(blockOf(m.map((c) => c / 2), block)) : marked(blockOf(m.map((c, j) => (c + TRI_DIR[i][j] - 1) / 2), block)));
  const at = (n) => n.map((c) => (c * PHI) / 2), out = [];
  const piece = (role, [V, F], n) => out.push([role, V.map((v) => v.map((c, i) => c + at(n)[i])), F, n]);
  for (const m of ico.values()) {
    let mask = 0;
    TRI_DIR.forEach((_, i) => { if (!toDodeca(m, i)) mask |= 1 << i; });
    if (mask === ALL) piece('mxIco', [C.oct[0][1], C.oct[0][2]], m);
    else if (mask === 0) piece('mxJewel', [C.lotusJewel[0][1], C.lotusJewel[0][2]], m);
    else piece('mxTrans', icoKeeping(mask), m);
  }
  for (const n of voids.values()) {
    let mask = 0;
    TRI_DIR.forEach((d, i) => { if (toDodeca(n.map((c, j) => c - d[j]), i)) mask |= 1 << i; });
    if (mask === ALL) piece('mxDodeca', [C.voidDodeca[0][1], C.voidDodeca[0][2]], n);
    else if (mask === 0) piece('mxUnborn', [C.unborn[0][1], C.unborn[0][2]], n);
    else piece('mxTrans', dodecaKeeping(mask), n);
  }
  for (const n of voids.values()) [0, 1, 2].forEach((a) => {
    const m = n.map((c, i) => c + (i === a ? 2 : 0));
    if (voids.has(m.join(','))) out.push(...put(AXE_FACE[a], at(n.map((c, i) => c + (i === a ? 1 : 0)))).map((p) => [...p, n]));
  });
  return out;
}
// ---- Golden split (DICTO 2026-10-23; study 2026-10-23-shadow-forms, exact in Q(√5)) ----
// Big truncated octahedra (icosahedron + 12 AXE pyramids) on the lattice points, small ones (Unborn + 12) on the cube centres. Each
// hexagon between a big piece and a small one is FLAT, keyed INTO_BIG (its Tricap goes to the small piece: the Lotus Jewel network's
// key) or INTO_SMALL (the Tricap mirrored in the hexagon goes to the big piece; it lies inside the Unborn); every choice fills space
// (point tests: krp-core tests/unit/golden-split.test.mjs, tests/unit/golden-split-world.test.mjs). Patterns: smooth, all keyed,
// checker and pyrochlore (Mixed blocks' blocks of cells: a marked cell's small piece takes the keys), random (one key in two); Swap
// turns the keys the other way; a tap on a hexagon steps it flat → into the big → into the small → flat. Whole pieces (big green,
// small orange) unless X-ray is on: then the cores (icosahedron, Lotus Jewel, Unborn, dodecahedron; pink if partly keyed), the AXE
// pyramids cyan and the mirrored keys purple, so the cut shows what each piece is made of.
// A hexagon is named by its small piece (odd n) and the direction s to the big one: 'x,y,z|sx,sy,sz'.
export const GS_PATTERNS = ['smooth', 'allKeyed', 'checker', 'pyrochlore', 'random'];
const gsHash = (k) => { let h = 2166136261; for (let i = 0; i < k.length; i++) h = Math.imul(h ^ k.charCodeAt(i), 16777619); return h >>> 0; };
/** The key state of a hexagon under { pattern, block, swap, flips }. */
export function gsState(n, s, { pattern = 'smooth', block = 1, swap = false, flips = {} } = {}) {
  const tag = `${n.join(',')}|${s.join(',')}`;
  if (Number.isInteger(flips[tag])) return flips[tag];
  const keyed = pattern === 'allKeyed' || (pattern === 'random' && gsHash(tag) % 2 === 1)
    || ((pattern === 'checker' || pattern === 'pyrochlore') && MIXED_PATTERNS[pattern](blockOf(n.map((c) => (c - 1) / 2), block)));
  return keyed ? (swap ? INTO_SMALL : INTO_BIG) : FLAT;
}
const gsGeom = new Map();
const neg = (s) => s.map((c) => -c);
// one piece kind (big or small) with given key states: whole (polygons, each face tagged with its hexagon index or -1) or parts
function gsPiece(big, states, xray) {
  const k = `${big}${states.join('')}${xray}`;
  if (gsGeom.has(k)) return gsGeom.get(k);
  const hexOf = (P) => {   // squares face along an axis; every other face belongs to the hexagon it lies on, dents and keys included
    const c = P.reduce((t, p) => t.map((x, i) => x + p[i] / P.length), [0, 0, 0]);
    const a = P[0], n = [0, 1, 2].map((m) => (P[1][(m + 1) % 3] - a[(m + 1) % 3]) * (P[2][(m + 2) % 3] - a[(m + 2) % 3]) - (P[1][(m + 2) % 3] - a[(m + 2) % 3]) * (P[2][(m + 1) % 3] - a[(m + 1) % 3]));
    if (n.filter((x) => Math.abs(x) > 1e-9 * Math.hypot(...n)).length === 1) return -1;
    return SIGNS.reduce((b, s, i) => (s.reduce((t, x, m) => t + x * c[m], 0) > SIGNS[b].reduce((t, x, m) => t + x * c[m], 0) ? i : b), 0);
  };
  const mesh = (tris) => { const { vertices, faces } = toPolygons(tris); return [vertices, faces, faces.map((f) => hexOf(f.map((i) => vertices[i])))]; };
  let out;
  if (!xray) {
    out = [[big ? 'gsBig' : 'gsSmall', ...mesh(pieceSurface(big, states))]];
  } else {
    const p = pieceParts(big, states), has = (st) => states.some((x) => x === st), every = (st) => states.every((x) => x === st);
    const core = big ? (!has(INTO_BIG) ? 'mxIco' : every(INTO_BIG) ? 'mxJewel' : 'mxTrans')
      : (every(FLAT) ? 'mxUnborn' : every(INTO_BIG) ? 'mxDodeca' : 'mxTrans');
    out = [[core, ...mesh(p.core)], ...p.pyramids.map((T) => ['axe', ...mesh(T)]), ...p.keys.map((T) => ['tricap', ...mesh(T)])];
  }
  gsGeom.set(k, out);
  return out;
}
/** Golden split on the sites of a size: [role, vertices, faces, n, { anchor, tags }] (tags: each face's hexagon name, or null). */
export function goldenPieces(size, o = {}) {
  const { ico, voids } = scSites(size), out = [];
  const at = (n) => n.map((c) => (c * PHI) / 2);
  const place = (big, n) => {
    const hex = SIGNS.map((s) => (big ? [n.map((c, i) => c + s[i]), neg(s)] : [n, s]));
    const states = hex.map(([m, s]) => gsState(m, s, o)), names = hex.map(([m, s]) => `${m.join(',')}|${s.join(',')}`), c = at(n);
    for (const [role, V, F, H] of gsPiece(big, states, !!o.xray)) {
      out.push([role, V.map((v) => v.map((x, i) => x + c[i])), F, n, { anchor: c, tags: H.map((h) => (h < 0 ? null : names[h])) }]);
    }
  };
  for (const n of ico.values()) place(true, n);
  for (const n of voids.values()) place(false, n);
  return out;
}
/** The next key state of a hexagon when tapped: flat → into the big → into the small → flat. */
export const gsNext = (tag, o) => { const [n, s] = tag.split('|').map((q) => q.split(',').map(Number)); return (gsState(n, s, o) + 1) % 3; };
const network = (tetCell) => (size) => [
  ...octSites(R(size)).filter((o) => o.even).flatMap((o) => put(C.oct, o.p)),
  ...tetSites(R(size)).flatMap((t) => put(C[tetCell], t.p, t.invert)),
];
export const OCTET_VIEWS = {
  caps: { maxSize: 4, views: { network: network('tet'), cell: [...put(C.oct, [0, 0, 0]), ...put(C.tet, [A / 4, A / 4, A / 4])] } },
  allIco: { maxSize: 3, views: { network: network('tetIco'), octahedron: put(C.oct, [0, 0, 0]), tetrahedron: put(C.tetIco, [0, 0, 0]) } },
  frog: { maxSize: 2, views: {
    network: (size) => [
      ...octSites(R(size)).filter((o) => o.even).flatMap((o) => put(C.oct.slice(0, 1), o.p)),
      ...tetSites(R(size)).flatMap((t) => put(C.tetIco.slice(0, 1), t.p, t.invert)),
      ...octSites(R(size)).filter((o) => !o.even).flatMap((o) => put(C.frog, o.p)),
    ],
    star: put(C.frog, [0, 0, 0]),
  } },
  pyrochlore: { maxSize: 4, views: {
    network: (size) => {
      const r = R(size) * 2;
      return [
        ...octSites(r).filter((o) => o.even).flatMap((o) => put(C.oct, o.p, false, 'octGlass')),
        ...tetSites(r).flatMap((t) => (pyro(t.s) ? put(C.tet, t.p, t.invert, t.invert ? 'pyroDown' : 'pyroUp') : put(C.tet, t.p, t.invert, 'tetGlass'))),
      ];
    },
    alone: (size) => tetSites(R(size) * 2).filter((t) => pyro(t.s)).flatMap((t) => put(C.tet, t.p, t.invert, t.invert ? 'pyroDown' : 'pyroUp')),
  } },
  lotusJewel: { maxSize: 3, views: { network: scNetwork('lotusJewel'), jewel: put(C.lotusJewel, [0, 0, 0]) } },
  icoUnborn: { maxSize: 3, views: { network: scNetwork('icoUnborn'), unborn: put(C.unborn, [0, 0, 0]) } },
  axeNet: { maxSize: 3, views: {
    network: scNetwork('axeNet'),
    ico: [...put(C.lotusJewel, [0, 0, 0]), ...put(C.tricap, [0, 0, 0])],
    dodeca: [...put(C.unborn, [0, 0, 0]), ...C.tricap.flatMap((t) => put([t], sign(centreOf(t[1])).map((c) => -c * PHI / 2)))],
  } },
  mixed: { maxSize: 3, options: { patterns: Object.keys(MIXED_PATTERNS), block: 3, startBlock: 2 }, views: {
    network: (size, o) => mixedPieces(size, o),
    transitions: (size, o) => mixedPieces(size, o).filter(([r]) => r === 'mxTrans' || r === 'axe'),
  } },
  goldenSplit: { maxSize: 3, options: { patterns: GS_PATTERNS, block: 3, startBlock: 1, buttons: true, blockPatterns: ['checker', 'pyrochlore'], flips: true, xray: true },
    tap: gsNext, views: { network: (size, o) => goldenPieces(size, o) } },
};
const DATA = OCTET_VIEWS;
const GLASS = { mixed: new Set(['mxDodeca', 'mxUnborn']), caps: new Set(['ico']), allIco: new Set(['ico', 'icoSmall']), frog: new Set(['ico', 'icoSmall']), pyrochlore: new Set(['octGlass', 'tetGlass']), lotusJewel: new Set(['voidDodeca']),
  icoUnborn: new Set(['unborn']), axeNet: new Set(['unborn']), goldenSplit: new Set(['gsSmall', 'mxUnborn', 'mxDodeca']) };

export function createOctetWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'octet', data: DATA, kinds: KINDS, glassRoles: GLASS, prefix: 'octet',
    defaultParts: { caps: 'network', allIco: 'network', frog: 'network', pyrochlore: 'network', lotusJewel: 'network', icoUnborn: 'network', axeNet: 'network', mixed: 'network', goldenSplit: 'network' },
    hideable: { lotusJewel: 'axe', icoUnborn: 'axe', axeNet: 'axe', mixed: 'axe' }, openAction,
    // the four pieces live in Polyhedraverse's DICTO's pieces (one place per shape); the world links to them
    links: { goldenSplit: [['Icosaxes', 'tool:polyShape:DICTO_ICOSAXES'], ['Unborn Axes', 'tool:polyShape:DICTO_UNBORN_AXES'],
      ['Lotus Jewel Axes', 'tool:polyShape:DICTO_LOTUS_JEWEL_AXES'], ['Dodecaxes', 'tool:polyShape:DICTO_DODECAXES']] } });
}

/** Points whose convex hull previews a network in the DICTO menu (one cell). */
export function octetPreviewPoints(kind) {
  const first = { caps: C.oct, allIco: C.tetIco, frog: C.oct.slice(0, 1), pyrochlore: C.tet, lotusJewel: C.lotusJewel, icoUnborn: C.unborn, axeNet: [...C.lotusJewel, ...C.tricap], mixed: C.voidDodeca, goldenSplit: [['gs', gsPiece(true, Array(8).fill(FLAT), false)[0][1]]] }[kind] ?? [];
  return first.flatMap((p) => p[1]);
}
