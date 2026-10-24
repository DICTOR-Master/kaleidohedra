// DICTONIC (DICTO 2026-10-23): the three DICTONIC BONDS of the six DICTONIC SOLIDS (names by DICTO), one world, a bond button each
// and one big slider whose meaning depends on the bond (it snaps to the special points; no step buttons):
//   Golden: the factor x of paper #48 Theorem 4: T(x) = hull of all permutations of (±(1 + x), ±x, 0), its squares at L/2, on the
//     lattice points (spacing L = phi) and T(1/x) on the cube centres fill space; x → 0 octahedra + cuboctahedra, x = 1 Kelvin, x = τ
//     Icosaxes + Unborn Axes (the golden bond; X-ray shows their icosahedron / Unborn cores and AXE pyramids, from the octet world's
//     Golden split), x → ∞ cuboctahedra + octahedra.
//   Keyed: Lotus Jewel Axes + Dodecaxes, all keyed (no slider); "Set keys one by one" opens the Golden split.
//   Delian: the octet family (krp-core delian-bond.js, study 2026-10-23-shadow-forms/octet): every tetrahedron–octahedron double cone
//     cut at fraction t, from rhombic dodecahedra (t = 0) through the octet (1/3) to cubes (1); the Delian bond Samson + Delilah at
//     t = 1 − (2/3)·2^(−1/3).
// The caption names the stop and gives the two pieces' volumes (golden: icosahedron edge 1; Delian: octet edge 1, as in
// Polyhedraverse); the bond's two solids open in Polyhedraverse (one place per shape). Built on the layered-world engine
// (world-chains.js: kind buttons, param slider). Words: i18n dictonic.*.
import { createLayeredWorld } from './world-chains.js';
import { goldenPieces, scSites } from './world-octet.js';
import { convexPolygons } from '../krp-core/src/polyhedra/golden-split.js';
import { tetPiece, octPiece, octetFamilyVolumes, OCTET_FAMILY_STOPS } from '../krp-core/src/polyhedra/delian-bond.js';
import { t } from './i18n.js';
import { mountTheorem } from './dictonic-theorem.js';

const PHI = (1 + Math.sqrt(5)) / 2;
export const DICTONIC_BONDS = ['golden', 'keyed', 'delian'];
const fmt = (v, d = 3) => v.toFixed(d);
const volume = ({ vertices: V, faces: F }) => F.reduce((s, f) => {
  for (let m = 1; m + 1 < f.length; m++) { const [a, b, c] = [V[f[0]], V[f[m]], V[f[m + 1]]]; s += a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]); }
  return s;
}, 0) / 6;

// ---- Golden: the slider is log x from 0.02 to 50 (x = 1 in the middle), its ends x = 0 and x = ∞ ----
const goldenX = (u) => (u <= 0 ? 0 : u >= 1000 ? Infinity : 0.02 * 2500 ** (u / 1000));
const goldenU = (x) => Math.round((1000 * Math.log(x / 0.02)) / Math.log(2500));
export const GOLDEN_STOPS = [{ u: 0, v: 0, key: 'zero' }, { u: 500, v: 1, key: 'kelvin' }, { u: goldenU(PHI), v: PHI, key: 'tau' }, { u: 1000, v: Infinity, key: 'inf' }];
/** T(x), its squares at L/2 (L = phi), as a convex solid about its centre: { vertices, faces }. */
const tCache = new Map();
export function goldenT(x) {
  if (tCache.has(x)) return tCache.get(x);
  const L = PHI, P = [];
  const base = x === Infinity ? [1, 1, 0] : [1 + x, x, 0].map((c) => c / (1 + x));
  for (const p of [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]) for (const sx of [1, -1]) for (const sy of [1, -1]) for (const sz of [1, -1]) {
    const q = p.map((i) => base[i]);
    P.push([sx * q[0], sy * q[1], sz * q[2]].map((c) => (c * L) / 2));
  }
  const out = convexPolygons(P);
  tCache.set(x, out);
  return out;
}
/** The golden bond's network at x: [role, vertices, faces, n, { anchor }] on the sites of the size (big at even n, small at odd n). */
export function goldenFamily(size, x, xray = false) {
  if (x === PHI) return goldenPieces(size, { pattern: 'smooth', xray });
  const { ico, voids } = scSites(size), out = [], at = (n) => n.map((c) => (c * PHI) / 2);
  const put = (role, { vertices, faces }, n) => { const c = at(n); out.push([role, vertices.map((v) => v.map((q, i) => q + c[i])), faces, n, { anchor: c }]); };
  for (const n of ico.values()) put('gsBig', goldenT(x), n);
  for (const n of voids.values()) put('gsSmall', goldenT(x === 0 ? Infinity : x === Infinity ? 0 : 1 / x), n);
  return out;
}

// ---- Delian: the octet family, t linear on the slider; pieces at octet edge 1 ----
export const DELIAN_STOPS = [['rd', 'rd'], ['equilateralRd', 'equilateral'], ['octet', 'octet'], ['half', 'half'], ['delian', 'bond'], ['equilateralCube', 'equilateral'], ['cube', 'cube']]
  .map(([k, key]) => ({ u: Math.round(OCTET_FAMILY_STOPS[k] * 1000), v: OCTET_FAMILY_STOPS[k], key }));
const R2 = Math.SQRT1_2;
/** The octet family's network at t: Samson-like pieces in the unit cubes, Delilah-like ones on the odd points, within the size's ball. */
export function delianFamily(size, tt) {
  const r = 1.25 * size, k = Math.ceil(r) + 1, out = [];
  // Every piece is a translate of one of three: the cube piece in an even or an odd cube, and the octahedron piece (DICTO 2026-10-25,
  // more layers: one hull each instead of one per piece).
  const parity = (x, y, z) => ((x + y + z) % 2 + 2) % 2;
  const tetHull = [0, 1].map((p) => convexPolygons(tetPiece([p, 0, 0], tt))), octHull = convexPolygons(octPiece([1, 0, 0], tt));
  const put = (role, { vertices, faces }, shift, c) => { const a = c.map((q) => q * R2); out.push([role, vertices.map((v) => v.map((q, i) => (q + shift[i]) * R2)), faces, c, { anchor: a }]); };
  for (let x = -k; x <= k; x++) for (let y = -k; y <= k; y++) for (let z = -k; z <= k; z++) {
    const p = parity(x, y, z);
    if (tt > 0 && Math.hypot(x + 0.5, y + 0.5, z + 0.5) <= r) put('dlTet', tetHull[p], [x - p, y, z], [x + 0.5, y + 0.5, z + 0.5]);
    if (tt < 1 && p === 1 && Math.hypot(x, y, z) <= r) put('dlOct', octHull, [x - 1, y, z], [x, y, z]);
  }
  return out;
}

// ---- The web of bonds (DICTO 2026-10-25: "the network of bonds should create a web of lattices that change with the rhythm of the
// loop"): the centres stay put; a bond is a face two pieces share, weighted by its area. Both families are face to face (each is a
// weighted Voronoi diagram), so two pieces share a face exactly when they have a face with the same centre. ----
const polyArea = (P) => { let x = 0, y = 0, z = 0; for (let i = 1; i + 1 < P.length; i++) { const [a, b, c] = [P[0], P[i], P[i + 1]];
  const u = b.map((q, j) => q - a[j]), v = c.map((q, j) => q - a[j]); x += u[1] * v[2] - u[2] * v[1]; y += u[2] * v[0] - u[0] * v[2]; z += u[0] * v[1] - u[1] * v[0]; }
  return Math.hypot(x, y, z) / 2; };
/** Bonds of a face-to-face network of convex pieces [role, vertices, faces, n, { anchor }]: [[anchorA, anchorB, area]]. */
export function webOf(pieces) {
  const seen = new Map(), out = [];
  for (const [, V, F, , extra] of pieces) for (const f of F) {
    const P = f.map((k) => V[k]), c = P.reduce((s, p) => s.map((q, i) => q + p[i] / P.length), [0, 0, 0]);
    const key = c.map((q) => Math.round(q * 1e5)).join(','), other = seen.get(key);
    if (other) { out.push([other, extra.anchor, polyArea(P)]); seen.delete(key); } else seen.set(key, extra.anchor);
  }
  return out;
}
/** The golden family as whole pieces (at x = τ too: Icosaxes + Unborn Axes as single solids, not their X-ray parts). */
function goldenCells(size, x) {
  const { ico, voids } = scSites(size), out = [], at = (n) => n.map((c) => (c * PHI) / 2);
  const put = (role, { vertices, faces }, n) => { const c = at(n); out.push([role, vertices.map((v) => v.map((q, i) => q + c[i])), faces, n, { anchor: c }]); };
  for (const n of ico.values()) put('gsBig', goldenT(x), n);
  for (const n of voids.values()) put('gsSmall', goldenT(x === 0 ? Infinity : x === Infinity ? 0 : 1 / x), n);
  return out;
}
// Layers (DICTO 2026-10-25): up to 6 on an iPad or a computer, 4 on a phone.
const layersMax = () => (typeof window !== 'undefined' && Math.min(window.screen?.width ?? 1024, window.screen?.height ?? 1024) < 600 ? 4 : 6);

const stopOf = (stops, u) => stops.find((s) => s.u === u) ?? null;
const valueOf = (stops, map) => (u) => stopOf(stops, u)?.v ?? map(u);
function goldenCaption(x, L) {
  const st = GOLDEN_STOPS.find((s) => s.v === x);
  const head = st ? t(`dictonic.stop.golden.${st.key}`, L) : `x = ${fmt(x, 3)}`;
  const vb = volume(goldenT(x)), vs = volume(goldenT(x === 0 ? Infinity : x === Infinity ? 0 : 1 / x));
  const [nb, ns] = x === PHI ? ['Icosaxes', 'Unborn Axes'] : [t('dictonic.piece.big', L), t('dictonic.piece.small', L)];
  return `${head} · ${nb} ${fmt(vb)} · ${ns} ${fmt(vs)}`;
}
function delianCaption(tt, L) {
  const st = DELIAN_STOPS.find((s) => s.v === tt);
  const head = st ? t(`dictonic.stop.delian.${st.key}`, L) : `t = ${fmt(tt, 3)}`;
  const [vt, vo] = octetFamilyVolumes(tt).map((v) => v / (2 * Math.SQRT2));   // cube of side 2 → octet edge 1
  const [nt, no] = st?.key === 'bond' ? ['Samson', 'Delilah'] : [t('dictonic.piece.tet', L), t('dictonic.piece.oct', L)];
  return `${head} · ${nt} ${fmt(vt, 4)} · ${no} ${fmt(vo, 4)}`;
}
export const DICTONIC_VIEWS = {
  golden: { maxSize: layersMax, web: (size, o) => webOf(goldenCells(size, o.param)), webRadius: 0.07, xray: true, param: { start: goldenU(PHI), stops: GOLDEN_STOPS, value: valueOf(GOLDEN_STOPS, goldenX), caption: goldenCaption, pauseAt: [500] },
    views: { network: (size, o) => goldenFamily(size, o.param, o.xray) } },
  keyed: { maxSize: layersMax, xray: true, views: { network: (size, o) => goldenPieces(size, { pattern: 'allKeyed', xray: o.xray }) } },
  delian: { maxSize: layersMax, web: (size, o) => webOf(delianFamily(size, o.param)), webRadius: 0.09, param: { start: DELIAN_STOPS.find((s) => s.key === 'bond').u, stops: DELIAN_STOPS, value: valueOf(DELIAN_STOPS, (u) => u / 1000), caption: delianCaption, pauseAt: [DELIAN_STOPS.find((s) => s.key === 'octet').u] },
    views: { network: (size, o) => delianFamily(size, o.param) } },
};
const LINKS = {
  golden: [['Icosaxes', 'tool:polyShape:DICTO_ICOSAXES'], ['Unborn Axes', 'tool:polyShape:DICTO_UNBORN_AXES']],
  keyed: [['Lotus Jewel Axes', 'tool:polyShape:DICTO_LOTUS_JEWEL_AXES'], ['Dodecaxes', 'tool:polyShape:DICTO_DODECAXES'], ['', 'tool:octetWorld:goldenSplit', 'dictonic.keyed.oneByOne']],
  delian: [['Samson', 'tool:polyShape:DICTO_SAMSON'], ['Delilah', 'tool:polyShape:DICTO_DELILAH']],
};

export function createDictonicWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'dictonic', data: DICTONIC_VIEWS, kinds: DICTONIC_BONDS, prefix: 'dictonic',
    glassRoles: { golden: new Set(['gsSmall', 'mxUnborn']), keyed: new Set(['gsSmall', 'mxDodeca']), delian: new Set(['dlOct']) },
    defaultParts: { golden: 'network', keyed: 'network', delian: 'network' }, kindButtons: true, rowWords: { size: 'dictonic.layers', shells: 'dictonic.topLayer' }, foldNote: true,
    theorem: (panel) => mountTheorem(panel, { stopsOf: (k) => DICTONIC_VIEWS[k].param.stops, valueAt: (k, u) => DICTONIC_VIEWS[k].param.value(Math.round(u)), openAction }), links: LINKS, openAction });
}

/** Points whose convex hull previews DICTONIC in the DICTO menu: Icosaxes. */
export const dictonicPreviewPoints = () => goldenT(PHI).vertices;
