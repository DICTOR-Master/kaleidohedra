// The Global Web of Bonds (DICTO 2026-10-25, "yes excellent idea, build it"): the companion world of paper #53, "The Global Web of
// Bonds: How Bonds Hand Over Across Crystal Networks" (DICTO DOI 10.5281/zenodo.23631140), from DICTO's idea that the DICTONIC branches show up elsewhere
// in geometric networks in slightly different guises. Phase 1: three networks, a button each and one big slider, the weight
// difference λ = w_A − w_B over the range where both kinds have pieces; each piece is the power (weighted Voronoi) cell of its site.
// All three hand over with a single switch, as the Delian bond does: the switch point is where only unlike bonds remain.
//
// Exact values and units are those of the study (k-research studies/2026-10-25-relay-census: README "Units", data/raw/tables.md):
//   square + centres: corners 2ℤ², centres 2ℤ² + (1, 1) (square edge 2); A = corner, B = centre; λ ∈ [−2, 2]; one flip, λ = 0 (the
//     square tiling, the switch point); the truncated square tiling 4.8.8 with all edges equal at λ = ±(2√2 − 2); ends: square tilings.
//   honeycomb + centres: the triangular lattice of edge 1 split 2 : 1; A = honeycomb, B = centre; λ ∈ [−1, 1]; one flip, λ = −1/2 (the
//     trihexagonal tiling 3.6.3.6, the switch point); the truncated hexagonal tiling 3.12.12 at λ = 1 − √3; regular hexagons at 0;
//     ends: hexagons round the centres (λ = −1), triangles round the honeycomb points (λ = 1).
//   rock salt NaCl: Na at the points of ℤ³ with even coordinate sum, Cl at the odd ones (Na–Cl distance 1); A = Na, B = Cl;
//     λ ∈ [−1, 1]; one flip, λ = 0 (cubes, the switch point); all edges equal at λ = ±(4 − 2√3), the larger piece with 6 squares and
//     12 hexagons beside cubes; ends: rhombic dodecahedra.
// The cells are computed here, exact in floats: for each site of the motif (one per translation class), the half-planes / half-spaces
// of its near neighbours are intersected (line pairs in 2D, plane triples in 3D, the feasible points kept), one cell per class at each
// λ, the faces read off the planes, then translated over the network (as DICTONIC's delianFamily does). The planar networks are drawn as thin slabs lying flat, so
// the engine's web, layers and X-ray work unchanged; there a bond's size is the length of the shared edge. Words: i18n globalWeb.*.
import { createLayeredWorld } from './world-chains.js';
import { webOf } from './world-dictonic.js';
import { t } from './i18n.js';
import { mountTheoremSheet, switchPicture } from './theorem-sheet.js';

const S2 = Math.SQRT2, S3 = Math.sqrt(3);
export const GLOBAL_WEB_NETWORKS = ['square', 'honeycomb', 'nacl'];
export const SLAB = 0.1; // the planar networks' slab thickness (study units)
const EPS = 1e-9;
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];

// ---- the networks: sites as [classIndex, point], the motif's kinds, the range of λ ----
const HEX = (i, j) => [i + j / 2, (j * S3) / 2];
const mod = (a, n) => ((a % n) + n) % n;
export const NETS = {
  square: { dim: 2, lo: -2, hi: 2, kinds: ['corner', 'centre'], motif: [['corner', [0, 0]], ['centre', [1, 1]]], spacing: S2, reach2: 8,
    sites(r) { const out = [], k = Math.ceil(r) + 1; for (let x = -k; x <= k; x++) for (let y = -k; y <= k; y++) if (mod(x + y, 2) === 0 && x * x + y * y <= r * r) out.push([mod(x, 2), [x, y]]); return out; } },
  honeycomb: { dim: 2, lo: -1, hi: 1, kinds: ['honeycomb', 'centre'], motif: [['centre', HEX(0, 0)], ['honeycomb', HEX(1, 0)], ['honeycomb', HEX(0, 1)]], spacing: 1, reach2: 4,
    sites(r) { const out = [], k = Math.ceil(2 * r) + 2; for (let i = -k; i <= k; i++) for (let j = -k; j <= k; j++) { const p = HEX(i, j); if (Math.hypot(...p) <= r) out.push([mod(i - j, 3), p]); } return out; } },
  nacl: { dim: 3, lo: -1, hi: 1, kinds: ['Na', 'Cl'], motif: [['Na', [0, 0, 0]], ['Cl', [1, 0, 0]]], spacing: 1, reach2: 4,
    sites(r) { const out = [], k = Math.ceil(r) + 1; for (let x = -k; x <= k; x++) for (let y = -k; y <= k; y++) for (let z = -k; z <= k; z++) if (x * x + y * y + z * z <= r * r) out.push([mod(x + y + z, 2), [x, y, z]]); return out; } },
};
const isA = (net, kind) => kind === net.kinds[0];
const weight = (net, kind, lam) => (isA(net, kind) ? lam : 0);

/** The power cell of motif site m at λ: { points (2D: the polygon in order; 3D: { vertices, faces }), facets: [{ kind, size }] } with
 *  coordinates about the site, or null where the cell has shrunk to a point. */
export function powerCell(name, m, lam, reach2 = NETS[name].reach2) {
  const net = NETS[name], [kind, s] = net.motif[m], ws = weight(net, kind, lam), d = net.dim;
  const cls = net.motif.map(([k]) => k);
  const nb = net.sites(Math.sqrt(reach2) + Math.hypot(...s) + 1).map(([c, q]) => [cls[c], sub(q, s)]).filter(([, q]) => { const l = dot(q, q); return l > EPS && l <= reach2 + EPS; });
  // |p − q|² − w_q ≥ |p|² − w_s  ⇔  2 q·p ≤ |q|² − w_q + w_s  (p about the site)
  const H = nb.map(([k, q]) => ({ kind: k, n: q.map((x) => 2 * x), b: dot(q, q) - weight(net, k, lam) + ws }));
  const ok = (p) => H.every((h) => dot(h.n, p) <= h.b + EPS * 10);
  const pts = [];
  const add = (p) => { if (ok(p) && !pts.some((q) => Math.hypot(...sub(p, q)) < 1e-9)) pts.push(p); };
  if (d === 2) {
    for (let i = 0; i < H.length; i++) for (let j = i + 1; j < H.length; j++) {
      const [a, b] = H[i].n, [c, e] = H[j].n, det = a * e - b * c;
      if (Math.abs(det) < 1e-12) continue;
      add([(H[i].b * e - b * H[j].b) / det, (a * H[j].b - H[i].b * c) / det]);
    }
  } else {
    for (let i = 0; i < H.length; i++) for (let j = i + 1; j < H.length; j++) for (let k = j + 1; k < H.length; k++) {
      const [A, B, C] = [H[i].n, H[j].n, H[k].n], det = dot(A, [B[1] * C[2] - B[2] * C[1], B[2] * C[0] - B[0] * C[2], B[0] * C[1] - B[1] * C[0]]);
      if (Math.abs(det) < 1e-12) continue;
      const r = [H[i].b, H[j].b, H[k].b], col = (M, c) => M.map((row, x) => row.map((v, y) => (y === c ? r[x] : v)));
      const M = [A, B, C], det3 = (Q) => Q[0][0] * (Q[1][1] * Q[2][2] - Q[1][2] * Q[2][1]) - Q[0][1] * (Q[1][0] * Q[2][2] - Q[1][2] * Q[2][0]) + Q[0][2] * (Q[1][0] * Q[2][1] - Q[1][1] * Q[2][0]);
      add([0, 1, 2].map((c) => det3(col(M, c)) / det));
    }
  }
  const mid = pts.reduce((a, p) => a.map((x, i) => x + p[i] / pts.length), new Array(d).fill(0)), spread = Math.max(0, ...pts.map((p) => Math.hypot(...sub(p, mid))));
  if (pts.length < d + 1 || spread < 1e-7) return null;
  const onPlane = (P) => H.find((h) => P.every((p) => Math.abs(dot(h.n, p) - h.b) < 1e-7));
  if (d === 2) {
    const c = pts.reduce((a, p) => [a[0] + p[0] / pts.length, a[1] + p[1] / pts.length], [0, 0]);
    pts.sort((p, q) => Math.atan2(p[1] - c[1], p[0] - c[0]) - Math.atan2(q[1] - c[1], q[0] - c[0]));
    const facets = pts.map((p, i) => { const q = pts[(i + 1) % pts.length]; return { kind: onPlane([p, q])?.kind, size: Math.hypot(...sub(p, q)) }; });
    return { points: pts, facets, measure: Math.abs(pts.reduce((a, p, i) => { const q = pts[(i + 1) % pts.length]; return a + p[0] * q[1] - p[1] * q[0]; }, 0)) / 2 };
  }
  // the faces: on each neighbour's plane, the corners lying in it (three or more), wound about the outward normal (the same hull
  // convexPolygons finds, without its search over all corner triples; tests/unit/global-web.test.mjs compares the two)
  const faces = [], facets = [], seen = new Set();
  for (const h of H) {
    const on = pts.map((_, i) => i).filter((i) => Math.abs(dot(h.n, pts[i]) - h.b) < 1e-7), key = on.join(',');
    if (on.length < 3 || seen.has(key)) continue;
    const fc = on.reduce((a, i) => a.map((x, j) => x + pts[i][j] / on.length), [0, 0, 0]), u = sub(pts[on[0]], fc), w = cross(h.n, u);
    const f = on.sort((i, j) => Math.atan2(dot(sub(pts[i], fc), w), dot(sub(pts[i], fc), u)) - Math.atan2(dot(sub(pts[j], fc), w), dot(sub(pts[j], fc), u)));
    if (faceArea(f.map((i) => pts[i])) < 1e-12) continue;
    seen.add(key); faces.push(f); facets.push({ kind: h.kind, size: faceArea(f.map((i) => pts[i])) });
  }
  const poly = { vertices: pts, faces };
  return { points: poly, facets, measure: volume(poly) };
}
function faceArea(P) {
  let x = 0, y = 0, z = 0;
  for (let i = 1; i + 1 < P.length; i++) { const u = sub(P[i], P[0]), v = sub(P[i + 1], P[0]); x += u[1] * v[2] - u[2] * v[1]; y += u[2] * v[0] - u[0] * v[2]; z += u[0] * v[1] - u[1] * v[0]; }
  return Math.hypot(x, y, z) / 2;
}
function volume({ vertices: V, faces: F }) {
  const c = V.reduce((a, p) => a.map((x, i) => x + p[i] / V.length), [0, 0, 0]);
  return F.reduce((s, f) => {
    for (let m = 1; m + 1 < f.length; m++) { const [a, b, e] = [V[f[0]], V[f[m]], V[f[m + 1]]].map((p) => sub(p, c)); s += Math.abs(a[0] * (b[1] * e[2] - b[2] * e[1]) - a[1] * (b[0] * e[2] - b[2] * e[0]) + a[2] * (b[0] * e[1] - b[1] * e[0])); }
    return s;
  }, 0) / 6;
}

// one cell per motif site and λ (cached), as a solid about the site: 3D as computed, 2D as a slab lying flat (the plane is x–z, y up)
const cellCache = new Map();
function cellSolid(name, m, lam) {
  const key = `${name}.${m}.${lam}`;
  if (cellCache.has(key)) return cellCache.get(key);
  if (cellCache.size > 400) cellCache.clear();
  const c = powerCell(name, m, lam);
  let out = null;
  if (c && NETS[name].dim === 3) out = c.points;
  else if (c) {
    const P = c.points, n = P.length, h = SLAB / 2;
    const vertices = [...P.map(([x, y]) => [x, -h, y]), ...P.map(([x, y]) => [x, h, y])];
    const faces = [[...P.keys()].reverse(), P.map((_, i) => n + i), ...P.map((_, i) => [i, (i + 1) % n, n + ((i + 1) % n), n + i])];
    out = { vertices, faces };
  }
  cellCache.set(key, out);
  return out;
}
const at3 = (name, p) => (NETS[name].dim === 2 ? [p[0], 0, p[1]] : p);
/** The network at λ: [role, vertices, faces, site, { anchor, kind }] within the size's ball (A pieces role gwA, B pieces gwB). */
export function globalWebFamily(name, size, lam) {
  const net = NETS[name], r = 1.25 * net.spacing * size, out = [];
  const cells = net.motif.map((_, m) => cellSolid(name, m, lam));
  for (const [m, p] of net.sites(r)) {
    const cell = cells[m]; if (!cell) continue;
    const kind = net.motif[m][0], a = at3(name, p);   // the cell is about its site: it moves to the site
    out.push([isA(net, kind) ? 'gwA' : 'gwB', cell.vertices.map((v) => v.map((x, i) => x + a[i])), cell.faces, p, { anchor: a, kind }]);
  }
  return out;
}
// bond colours, as in paper #53's figures: the unlike bond gold, A–A blue, B–B green
export const BOND_COLOURS = { ab: '#ffc857', aa: '#7fd3ff', bb: '#5fd38a' };
const bondType = (net, k1, k2) => (k1 !== k2 ? 'ab' : isA(net, k1) ? 'aa' : 'bb');
/** The web of bonds: [[anchorA, anchorB, size, colour, type]], size = shared edge length (2D) or shared face area (3D). */
export function globalWeb(name, size, lam) {
  const net = NETS[name], pieces = globalWebFamily(name, size, lam), kindOf = new Map(pieces.map((p) => [p[4].anchor, p[4].kind]));   // webOf hands back the anchors themselves
  return webOf(pieces).map(([a, b, area]) => { const ty = bondType(net, kindOf.get(a), kindOf.get(b)); return [a, b, net.dim === 2 ? area / SLAB : area, parseInt(BOND_COLOURS[ty].slice(1), 16), ty]; });
}

// ---- exact closed forms (study README, notes 1, 2a, 3; cell measures from them): one bond of each type, and the two cell measures ----
export const BOND_SIZES = {
  square: (l) => ({ ab: Math.max(0, (2 - Math.abs(l)) / S2), aa: l > 0 ? l : 0, bb: l < 0 ? -l : 0 }),
  honeycomb: (l) => ({ ab: l > -0.5 ? (1 - l) / S3 : S3 * (l + 1), aa: l > -0.5 ? (2 * l + 1) / S3 : 0, bb: l < -0.5 ? -(2 * l + 1) : 0 }),
  nacl: (l) => ({ ab: (1 - Math.abs(l)) ** 2, aa: l > 0 ? (l * (2 - l)) / S2 : 0, bb: l < 0 ? (-l * (2 + l)) / S2 : 0 }),
};
/** [A cell, B cell] area (2D) or volume (3D), exact. Square: the smaller cell is a square of the unlike edge; honeycomb: a regular
 *  hexagon (centre, λ > −1/2) or an equilateral triangle (honeycomb, λ < −1/2); rock salt: a cube of edge 1 − |λ|. */
export const CELL_MEASURES = {
  square: (l) => { const small = (2 - Math.abs(l)) ** 2 / 2; return l >= 0 ? [4 - small, small] : [small, 4 - small]; },
  honeycomb: (l) => { if (l >= -0.5) { const c = (S3 / 2) * (1 - l) ** 2; return [((3 * S3) / 2 - c) / 2, c]; } const hc = ((3 * S3) / 4) * (l + 1) ** 2; return [hc, (3 * S3) / 2 - 2 * hc]; },
  nacl: (l) => { const small = (1 - Math.abs(l)) ** 3; return l >= 0 ? [2 - small, small] : [small, 2 - small]; },
};
// the study's tables (data/raw/tables.md): at every stop and on every open interval, each kind's cell (corners in 2D, face vector in
// 3D, 'point') and its bonds by neighbour kind. [λ or [from, to], A: [cell, bonds], B: [cell, bonds]]
export const STUDY_TABLES = {
  square: [[-2, ['point', {}], ['4-gon', { centre: 4 }]], [[-2, 0], ['4-gon', { centre: 4 }], ['8-gon', { centre: 4, corner: 4 }]], [0, ['4-gon', { centre: 4 }], ['4-gon', { corner: 4 }]],
    [[0, 2], ['8-gon', { centre: 4, corner: 4 }], ['4-gon', { corner: 4 }]], [2, ['4-gon', { corner: 4 }], ['point', {}]]],
  honeycomb: [[-1, ['point', {}], ['6-gon', { centre: 6 }]], [[-1, -0.5], ['3-gon', { centre: 3 }], ['12-gon', { centre: 6, honeycomb: 6 }]], [-0.5, ['3-gon', { centre: 3 }], ['6-gon', { honeycomb: 6 }]],
    [[-0.5, 1], ['6-gon', { centre: 3, honeycomb: 3 }], ['6-gon', { honeycomb: 6 }]], [1, ['3-gon', { honeycomb: 3 }], ['point', {}]]],
  nacl: [[-1, ['point', {}], ['12×4', { Cl: 12 }]], [[-1, 0], ['6×4', { Cl: 6 }], ['6×4+12×6', { Cl: 12, Na: 6 }]], [0, ['6×4', { Cl: 6 }], ['6×4', { Na: 6 }]],
    [[0, 1], ['6×4+12×6', { Cl: 6, Na: 12 }], ['6×4', { Na: 6 }]], [1, ['12×4', { Na: 12 }], ['point', {}]]],
};
export const tableRow = (name, l) => STUDY_TABLES[name].find(([w]) => (Array.isArray(w) ? l > w[0] && l < w[1] : Math.abs(l - w) < 1e-12));

// ---- the slider: u = 0..1000 runs λ linearly over the range; the stops (exact) ----
const STOP_LIST = {
  square: [[-2, 'endB'], [-(2 * S2 - 2), 'uniformB'], [0, 'switch'], [2 * S2 - 2, 'uniformA'], [2, 'endA']],
  honeycomb: [[-1, 'endB'], [1 - S3, 'uniform'], [-0.5, 'switch'], [0, 'hex'], [1, 'endA']],
  nacl: [[-1, 'endB'], [-(4 - 2 * S3), 'equalB'], [0, 'switch'], [4 - 2 * S3, 'equalA'], [1, 'endA']],
};
export const SWITCH = { square: 0, honeycomb: -0.5, nacl: 0 };
const uOf = (name, l) => Math.round((1000 * (l - NETS[name].lo)) / (NETS[name].hi - NETS[name].lo));
export const GLOBAL_WEB_STOPS = Object.fromEntries(GLOBAL_WEB_NETWORKS.map((n) => [n, STOP_LIST[n].map(([v, key]) => ({ u: uOf(n, v), v, key }))]));
const lamOf = (name) => (u) => GLOBAL_WEB_STOPS[name].find((s) => s.u === u)?.v ?? NETS[name].lo + ((NETS[name].hi - NETS[name].lo) * u) / 1000;

const fmt = (v, d = 3) => v.toFixed(d).replace('-', '−');
const pieceWord = (name, kind, L) => t(`globalWeb.piece.${{ corner: 'corner', centre: 'centre', honeycomb: 'honeycomb', Na: 'na', Cl: 'cl' }[kind]}`, L);
function caption(name, l, L) {
  const st = GLOBAL_WEB_STOPS[name].find((s) => s.v === l), net = NETS[name], [ma, mb] = CELL_MEASURES[name](l);
  const head = st ? t(`globalWeb.stop.${name}.${st.key}`, L) : `λ = ${fmt(l)}`, w = net.dim === 2 ? 'globalWeb.caption.area' : 'globalWeb.caption.volume';
  return `${head} · ${t(w, L, { piece: pieceWord(name, net.kinds[0], L), v: fmt(ma) })} · ${t(w, L, { piece: pieceWord(name, net.kinds[1], L), v: fmt(mb) })}`;
}
// Layers (as DICTONIC): up to 6 on an iPad or a computer, 4 on a phone
const layersMax = () => (typeof window !== 'undefined' && Math.min(window.screen?.width ?? 1024, window.screen?.height ?? 1024) < 600 ? 4 : 6);
const VIEW_DIR = { square: [0, 1, 0.5], honeycomb: [0, 1, 0.5], nacl: [1, 0.75, 1.35] };
export const GLOBAL_WEB_VIEWS = Object.fromEntries(GLOBAL_WEB_NETWORKS.map((name) => [name, {
  maxSize: layersMax, viewDir: VIEW_DIR[name], webRadius: name === 'nacl' ? 0.07 : 0.045, webNote: NETS[name].dim === 2 ? 'globalWeb.web.note2d' : 'globalWeb.web.note3d',
  web: (size, o) => globalWeb(name, size, o.param),
  param: { start: uOf(name, SWITCH[name]), stops: GLOBAL_WEB_STOPS[name], value: lamOf(name), caption: (l, L) => caption(name, l, L), pauseAt: [uOf(name, SWITCH[name])] },
  views: { network: (size, o) => globalWebFamily(name, size, o.param) },
}]));

// ---- the theorem (statement, live chart, bonds per piece, the switch in the dual) ----
const BOND_NAMES = { square: { ab: 'globalWeb.thm.bond.centreCorner', aa: 'globalWeb.thm.bond.cornerCorner', bb: 'globalWeb.thm.bond.centreCentre' },
  honeycomb: { ab: 'globalWeb.thm.bond.centreHoneycomb', aa: 'globalWeb.thm.bond.honeycombHoneycomb', bb: 'globalWeb.thm.bond.centreCentre' } };
const NACL_BONDS = { ab: 'Na–Cl', aa: 'Na–Na', bb: 'Cl–Cl' };
const MARK_WORDS = { square: { uniformB: '4.8.8', uniformA: '4.8.8' }, honeycomb: { uniform: '3.12.12' } };
function countLine(name, l, L) {
  const net = NETS[name], row = tableRow(name, l);
  const part = (kind, [cell, bonds]) => {
    const own = bonds[kind] ?? 0, other = Object.entries(bonds).filter(([k]) => k !== kind).reduce((s, [, n]) => s + n, 0);
    const n = cell === 'point' ? t('globalWeb.thm.count.point', L) : own && other ? t('globalWeb.thm.count.split', L, { n: own + other, u: other, l: own }) : t('globalWeb.thm.count.n', L, { n: own + other });
    return `${pieceWord(name, kind, L)}: ${n}`;
  };
  return row ? `${part(net.kinds[0], row[1])} · ${part(net.kinds[1], row[2])}` : '';
}
const tk = (key) => (L) => t(key, L);
// the dual quadrilateral at the switch: B–B diagonal (horizontal, bonded before the switch), A–A (vertical, after); honeycomb:
// a rhombus, centre–centre √3 against honeycomb–honeycomb 1; square and rock salt: a square, both diagonals equal
const HALF = { square: [34, 34], honeycomb: [40, 40 / S3], nacl: [34, 34] };
const NETWORKS = Object.fromEntries(GLOBAL_WEB_NETWORKS.map((name) => [name, {
  areas: BOND_SIZES[name], curves: [['bb', BOND_COLOURS.bb], ['ab', BOND_COLOURS.ab], ['aa', BOND_COLOURS.aa]], marks: GLOBAL_WEB_STOPS[name].filter((s) => s.key !== 'endA' && s.key !== 'endB').map((s) => s.key),
  statement: tk(`globalWeb.thm.${name}`), detail: tk('globalWeb.thm.detail'), chart: tk(NETS[name].dim === 2 ? 'globalWeb.thm.chart2d' : 'globalWeb.thm.chart3d'),
  bond: (key, L) => (name === 'nacl' ? NACL_BONDS[key] : t(BOND_NAMES[name][key], L)),
  mark: (k, L) => (k === 'switch' ? t('globalWeb.thm.mark.switch', L) : k === 'hex' ? t('globalWeb.thm.mark.hex', L) : MARK_WORDS[name]?.[k] ?? t('dictonic.stop.delian.equilateral', L)),
  count: (l, L) => countLine(name, l, L),
  flip: { svg: (l) => switchPicture({ a: HALF[name][0], b: HALF[name][1], cols: [BOND_COLOURS.bb, BOND_COLOURS.aa], before: l < SWITCH[name], after: l > SWITCH[name] }),
    now: (l, paused) => !!paused || Math.abs(l - SWITCH[name]) < 1e-9, label: tk(`globalWeb.thm.flip.${name}`) },
}]));
const WORDS = { more: tk('dictonic.thm.more'), less: tk('dictonic.thm.less'), almanac: tk('dictonic.thm.almanac'), title: tk('dictonic.thm.almanac.title'), entry: tk('dictonic.thm.almanac.entry') };

export function createGlobalWebWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'globalweb', data: GLOBAL_WEB_VIEWS, kinds: GLOBAL_WEB_NETWORKS, prefix: 'globalWeb', glassRoles: {},
    defaultParts: Object.fromEntries(GLOBAL_WEB_NETWORKS.map((n) => [n, 'network'])), kindButtons: true, rowWords: { size: 'dictonic.layers', shells: 'dictonic.topLayer' }, foldNote: true,
    theorem: (panel) => mountTheoremSheet(panel, { networks: NETWORKS, words: WORDS, entryAction: 'openAlmanac:dicto:globalWeb', stopsOf: (k) => GLOBAL_WEB_STOPS[k], valueAt: (k, u) => GLOBAL_WEB_VIEWS[k].param.value(Math.round(u)), openAction }),
    openAction });
}

/** Points whose convex hull previews the world in the DICTO menu: the rock salt Na piece with all edges equal (6 squares, 12 hexagons). */
export const globalWebPreviewPoints = () => powerCell('nacl', 0, 4 - 2 * S3).points.vertices;
