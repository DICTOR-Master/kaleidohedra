// The Bitruncated 600-cell world (DICTO 2026-11-10; working name, DICTO names it): the midpoint between the White Queen and the Red
// Queen, the stage t12 of queen-stages-geometry.js (its 3600 corners and 7200 edges, nothing built twice), with its 720 cells:
//   120 truncated icosahedra (TI), one per White Queen vertex v: the 60 corners whose White Queen edge contains v;
//   600 truncated tetrahedra (tt), one per White Queen cell C: the 12 corners whose triangle lies in C.
// Every corner lies in exactly four cells (2 TI + 2 tt). The cells meet in 2400 hexagons (TI–tt), 1200 triangles (tt–tt) and 720
// pentagons (TI–TI). A cell's edges are the stage's edges with both ends in the cell.
// The sweep: sliced along a direction d by the 3-spaces x·d = h, the slice is a convex solid whose surface is tiled by the cells'
// cross-sections. The tiling changes only at corner heights; between two neighbouring ones it is one pattern (the cells alive and the
// pairs of cells that touch, i.e. whose shared face crosses the 3-space). Comparing neighbouring gaps: cells appear, cells disappear,
// pairs let go and pairs meet. Along a generic direction every corner height brings exactly one of: a cell appearing, a cell
// disappearing, or a scutoid swap (one pair lets go and another meets, four cells in all). Pure maths, no three.js.
// Everything is built on first use (model()), not when the app starts: the edges of 3600 corners take a moment to find.
import { stage, stageCorners, stageShadowAt, STAGE_TRIANGLES, STAGE_TRIANGLE_CELLS } from './queen-stages-geometry.js';
import { VERTICES as WQ_VERTICES, EDGES as WQ_EDGES, CELLS as WQ_CELLS, UNIT_DIRECTIONS, FRAMES as WQ_FRAMES } from './white-queen-geometry.js';

export { stageShadowAt };
export const STAGE = 't12';
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const unit = (a) => { const l = Math.hypot(...a); return a.map((x) => x / l); };
const EPS = 1e-9;

// ---- the model: corners, edges, cells, faces, shells ----
// corner 3t + j lies on edge j of triangle t: [t0, t1], [t0, t2], [t1, t2]
const EDGE_PICK = [[0, 1], [0, 2], [1, 2]];
const cornerEdge = (k) => { const t = STAGE_TRIANGLES[Math.floor(k / 3)], [a, b] = EDGE_PICK[k % 3]; return [t[a], t[b]]; };
function buildModel() {
  const ST = stage(STAGE), CORNERS = ST.vertices, EDGES = ST.edges;   // 3600 corners (radius 2), 7200 edges
  const TI = WQ_VERTICES.map(() => []), TT = WQ_CELLS.map(() => []);
  for (let k = 0; k < CORNERS.length; k++) {
    for (const v of cornerEdge(k)) TI[v].push(k);
    for (const c of STAGE_TRIANGLE_CELLS[Math.floor(k / 3)]) TT[c].push(k);
  }
  /** The 720 cells: 0..119 the truncated icosahedra (by White Queen vertex), 120..719 the truncated tetrahedra (by White Queen cell).
   *  { kind: 'TI' | 'tt', of (the vertex or cell index), corners, edges (indices into EDGES) }. */
  const CELLS = [...TI.map((corners, of) => ({ kind: 'TI', of, corners })), ...TT.map((corners, of) => ({ kind: 'tt', of, corners }))];
  const TI_COUNT = TI.length;
  {
    const cellsAt = CORNERS.map(() => []);
    CELLS.forEach((c, ci) => c.corners.forEach((k) => cellsAt[k].push(ci)));
    CELLS.forEach((c) => { c.edges = []; });
    EDGES.forEach(([a, b], ei) => { for (const ci of cellsAt[a]) if (cellsAt[b].includes(ci)) CELLS[ci].edges.push(ei); });
  }
  /** The cells round each corner (four each). */
  const CELLS_AT = (() => { const at = CORNERS.map(() => []); CELLS.forEach((c, ci) => c.corners.forEach((k) => at[k].push(ci))); return at; })();

  /** The 4320 faces where two cells meet: { cells: [a, b], corners, kind: 'hexagon' | 'triangle' | 'pentagon' }. */
  const FACES = (() => {
    const out = [];
    // hexagons: TI(v) ∩ tt(C) for v a corner of C
    WQ_CELLS.forEach((c, ci) => c.forEach((v) => {
      const inTI = new Set(TI[v]);
      out.push({ cells: [v, TI_COUNT + ci], corners: TT[ci].filter((k) => inTI.has(k)), kind: 'hexagon' });
    }));
    // triangles: the three corners of a White Queen triangle, between its two cells' tt
    STAGE_TRIANGLES.forEach((_, t) => out.push({ cells: STAGE_TRIANGLE_CELLS[t].map((c) => TI_COUNT + c), corners: [3 * t, 3 * t + 1, 3 * t + 2], kind: 'triangle' }));
    // pentagons: the five corners on a White Queen edge (one per triangle round it), between its two ends' TI
    const onEdge = new Map();
    for (let k = 0; k < CORNERS.length; k++) { const [a, b] = cornerEdge(k), key = a < b ? `${a},${b}` : `${b},${a}`; if (!onEdge.has(key)) onEdge.set(key, []); onEdge.get(key).push(k); }
    for (const [a, b] of WQ_EDGES) out.push({ cells: [a, b], corners: onEdge.get(a < b ? `${a},${b}` : `${b},${a}`), kind: 'pentagon' });
    return out;
  })();
  // each face's corners in order round it (walking its edges)
  {
    const nb = CORNERS.map(() => []);
    for (const [a, b] of EDGES) { nb[a].push(b); nb[b].push(a); }
    for (const f of FACES) {
      const inF = new Set(f.corners), loop = [f.corners[0]];
      while (loop.length < f.corners.length) {
        const last = loop[loop.length - 1], prev = loop[loop.length - 2];
        loop.push(nb[last].find((x) => inF.has(x) && x !== prev && !loop.includes(x)));
      }
      f.loop = loop;
    }
  }
  /** Each cell's faces (indices into FACES): a TI's 12 pentagons and 20 hexagons, a tt's 4 triangles and 4 hexagons. */
  const CELL_FACES = (() => { const out = CELLS.map(() => []); FACES.forEach((f, fi) => f.cells.forEach((c) => out[c].push(fi))); return out; })();
  /** Each cell's neighbours (cells sharing a face with it). */
  const NEIGHBOURS = (() => { const n = CELLS.map(() => []); for (const f of FACES) { n[f.cells[0]].push(f.cells[1]); n[f.cells[1]].push(f.cells[0]); } return n; })();

  // ---- shells ----
  // The 720 cells in shells by graph distance (cells sharing a face) from one TI, the core: the TI of the White Queen vertex
  // (2, 0, 0, 0). In perspective from an eye just beyond the opposite TI (as the White Queen's Cleo shells, from just beyond her
  // opposite vertex): the core lies in the 3-space x₀ = h_core, so it is drawn undistorted, and at its true size.
  const CORE = WQ_VERTICES.findIndex((v) => v[0] > 2 - 1e-9);
  const CORE_HEIGHT = CORNERS[CELLS[CORE].corners[0]][0];
  const SHELL_EYE = -CORE_HEIGHT - EYE_GAP;
  const SHELL_POINTS = CORNERS.map((x) => WQ_FRAMES[0].map((f) => (dot(x, f) * (CORE_HEIGHT - SHELL_EYE)) / (x[0] - SHELL_EYE)));
  /** The shells from the core outwards: arrays of cell indices. */
  const SHELLS = (() => {
    const dist = CELLS.map(() => -1), out = [[CORE]];
    dist[CORE] = 0;
    for (let k = 0; out[k].length; k++) {
      const next = [];
      for (const c of out[k]) for (const m of NEIGHBOURS[c]) if (dist[m] < 0) { dist[m] = k + 1; next.push(m); }
      out.push(next.sort((a, b) => a - b));
    }
    out.pop();
    return out;
  })();
  return { CORNERS, EDGES, CELLS, TI_COUNT, CELLS_AT, FACES, CELL_FACES, NEIGHBOURS, CORE, CORE_HEIGHT, SHELL_EYE, SHELL_POINTS, SHELLS };
}
let built = null;
/** The model, built once: { CORNERS, EDGES, CELLS, TI_COUNT, CELLS_AT, FACES, CELL_FACES, NEIGHBOURS, CORE, CORE_HEIGHT, SHELL_EYE,
 *  SHELL_POINTS, SHELLS } (each as described above). */
export const model = () => built ?? (built = buildModel());
export const TI_COUNT = WQ_VERTICES.length;   // cells 0..119 are the truncated icosahedra
export const EYE_GAP = 1 / 10;

// ---- the directions ----
// the White Queen's four main directions (vertex-, edge-, face-, cell-first) and one generic direction, fixed, with no two of the
// 3600 corner heights equal (the nearest two 3.6e-6 apart; checked in tests/unit/bitrunc.test.mjs). Its parts are irrational on
// purpose: the corners' differences have parts in Q(√5), so a direction of short decimals such as (0.29, 0.53, −0.71, 0.37) is
// easily orthogonal to one of them (it is to (−3, 1, −1, −1)) and gives equal heights.
export const DIRECTIONS = ['vertex-first', 'edge-first', 'face-first', 'cell-first', 'generic'];
export const GENERIC = unit([Math.SQRT2 / 5, Math.sqrt(3) / 3, -Math.PI / 4, Math.E / 7]);   // ≈ (0.260, 0.531, −0.723, 0.357)
export const UNITS = [...UNIT_DIRECTIONS, GENERIC];
/** An orthonormal frame of the 3-space across d (the White Queen's own frames for the main directions). */
function frameAcross(d) {
  const basis = [d];
  for (const e of [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) {
    if (basis.length === 4) break;
    const v = basis.reduce((x, b) => { const c = dot(x, b); return x.map((y, i) => y - c * b[i]); }, e);
    if (Math.hypot(...v) > 1e-6) basis.push(unit(v));
  }
  return basis.slice(1);
}
export const FRAMES = [...WQ_FRAMES, frameAcross(GENERIC)];
const indexOf = (k) => (typeof k === 'number' ? k : DIRECTIONS.indexOf(k));

// ---- the sweep ----
const sweeps = new Map();
/** The sweep along a direction: { levels (the distinct corner heights, bottom to top), heights (per corner), stops, events, totals }.
 *  stops: every level and the exact middle of every gap, bottom to top: { value, level (index) | gap (index) }.
 *  events[L] (L = 1 .. levels − 2, comparing gap L − 1 with gap L): { born, died, letGo, meet } (cells; pairs of cells),
 *  and swapFrom (the number of pairs that let go below this level). */
export function sweep(dir) {
  const n = indexOf(dir);
  if (sweeps.has(n)) return sweeps.get(n);
  const { CORNERS, CELLS, FACES } = model(), d = UNITS[n], heights = CORNERS.map((p) => dot(p, d));
  const order = heights.map((_, i) => i).sort((a, b) => heights[a] - heights[b]);
  const levels = [], levelOf = new Array(CORNERS.length);
  for (const k of order) { if (!levels.length || heights[k] - levels[levels.length - 1] > EPS) levels.push(heights[k]); levelOf[k] = levels.length - 1; }
  const span = (corners) => { let lo = Infinity, hi = -Infinity; for (const k of corners) { lo = Math.min(lo, levelOf[k]); hi = Math.max(hi, levelOf[k]); } return [lo, hi]; };
  const cellSpan = CELLS.map((c) => span(c.corners)), faceSpan = FACES.map((f) => span(f.corners));
  // alive in gap g (between levels g and g + 1): lo ≤ g < hi
  const aliveIn = (ci, g) => cellSpan[ci][0] <= g && g < cellSpan[ci][1];
  const events = levels.map(() => ({ born: [], died: [], letGo: [], meet: [], swapFrom: 0 }));
  cellSpan.forEach(([lo, hi], ci) => { if (lo < hi) { events[lo].born.push(ci); events[hi].died.push(ci); } });
  faceSpan.forEach(([lo, hi], fi) => {
    const [a, b] = FACES[fi].cells;
    if (lo === hi) return;   // a face lying in one 3-space x·d = h never crosses one between two heights
    if (aliveIn(a, hi) && aliveIn(b, hi)) events[hi].letGo.push([a, b]);   // the face stops crossing; both cells live on
    if (lo > 0 && aliveIn(a, lo - 1) && aliveIn(b, lo - 1)) events[lo].meet.push([a, b]);   // it starts crossing; both cells were there
  });
  let swaps = 0;
  for (const e of events) { e.swapFrom = swaps; swaps += e.letGo.length; }
  const inner = events.slice(1, -1);
  const totals = {
    levels: levels.length,
    born: inner.reduce((s, e) => s + e.born.length, 0),
    died: inner.reduce((s, e) => s + e.died.length, 0),
    letGo: swaps, meet: inner.reduce((s, e) => s + e.meet.length, 0),
    // a scutoid swap: one pair lets go and another meets, four cells in all, nothing else at that height
    swaps: inner.filter((e) => e.letGo.length === 1 && e.meet.length === 1 && !e.born.length && !e.died.length && new Set([...e.letGo[0], ...e.meet[0]]).size === 4).length,
  };
  const stops = [];
  levels.forEach((h, L) => { stops.push({ value: h, level: L }); if (L + 1 < levels.length) stops.push({ value: (h + levels[L + 1]) / 2, gap: L }); });
  const out = { dir: DIRECTIONS[n], d, heights, levels, cellSpan, faceSpan, events, totals, stops };
  sweeps.set(n, out);
  return out;
}

/** The slice of direction `dir` at its stop k: the cross-sections of the cells alive there, in the direction's own 3D frame.
 *  { stop, value, cells: [{ cell, kind, points (3D loop, ordered round its outward normal) }], ti, tt, touching (pairs of cells whose
 *  shared face crosses), event (at a level: that level's event) }. */
const sliceCache = new Map();
export function sliceAt(dir, k) {
  const n = indexOf(dir), key = `${n}.${k}`;
  if (sliceCache.has(key)) return sliceCache.get(key);
  const { CORNERS, EDGES, CELLS, FACES } = model(), sw = sweep(n), stop = sw.stops[k], h = stop.value, H = sw.heights, frame = FRAMES[n];
  const cells = [];
  CELLS.forEach((c, ci) => {
    let lo = Infinity, hi = -Infinity;
    for (const v of c.corners) { lo = Math.min(lo, H[v]); hi = Math.max(hi, H[v]); }
    if (!(h - lo > EPS && hi - h > EPS)) return;
    const pts = [];
    const add = (p4) => { const p = frame.map((f) => dot(p4, f)); if (!pts.some((q) => Math.abs(q[0] - p[0]) + Math.abs(q[1] - p[1]) + Math.abs(q[2] - p[2]) < 1e-9)) pts.push(p); };
    for (const ei of c.edges) {
      const [a, b] = EDGES[ei], ha = H[a] - h, hb = H[b] - h;
      if (Math.abs(ha) <= EPS) add(CORNERS[a]);
      if (Math.abs(hb) <= EPS) add(CORNERS[b]);
      if ((ha > EPS && hb < -EPS) || (ha < -EPS && hb > EPS)) { const t = ha / (ha - hb); add(CORNERS[a].map((x, i) => x + t * (CORNERS[b][i] - x))); }
    }
    cells.push({ cell: ci, kind: c.kind, points: pts });
  });
  // order each polygon round its normal, the normal pointing out of the slice (away from the middle of all its points)
  const all = cells.flatMap((c) => c.points), mid = [0, 1, 2].map((i) => all.reduce((s, p) => s + p[i], 0) / Math.max(1, all.length));
  for (const c of cells) {
    const P = c.points, m = [0, 1, 2].map((i) => P.reduce((s, p) => s + p[i], 0) / P.length);
    let nrm = [0, 0, 0];
    for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) {
      const a = P[i].map((x, q) => x - m[q]), b = P[j].map((x, q) => x - m[q]);
      const cr = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
      if (Math.hypot(...cr) > Math.hypot(...nrm)) nrm = cr;
    }
    if (dot(nrm, m.map((x, i) => x - mid[i])) < 0) nrm = nrm.map((x) => -x);
    nrm = unit(nrm);
    const e1 = unit(P[0].map((x, i) => x - m[i])), e2 = [nrm[1] * e1[2] - nrm[2] * e1[1], nrm[2] * e1[0] - nrm[0] * e1[2], nrm[0] * e1[1] - nrm[1] * e1[0]];
    const ang = (p) => { const v = p.map((x, i) => x - m[i]); return Math.atan2(dot(v, e2), dot(v, e1)); };
    c.points = P.slice().sort((a, b) => ang(a) - ang(b));
    c.normal = nrm;
  }
  const alive = new Set(cells.map((c) => c.cell));
  const touching = FACES.filter((f) => {
    if (!alive.has(f.cells[0]) || !alive.has(f.cells[1])) return false;
    let lo = Infinity, hi = -Infinity;
    for (const v of f.corners) { lo = Math.min(lo, H[v]); hi = Math.max(hi, H[v]); }
    return h - lo > EPS && hi - h > EPS;
  }).map((f) => f.cells);
  const ti = cells.filter((c) => c.kind === 'TI').length;
  const out = { stop, value: h, cells, ti, tt: cells.length - ti, touching, event: stop.level !== undefined ? sw.events[stop.level] : null };
  if (sliceCache.size > 200) sliceCache.clear();
  sliceCache.set(key, out);
  return out;
}


/** The world's cover in the DICTO menu, quick (no edge search over all 3600 corners): the core truncated icosahedron and the 32 cells
 *  round it in the Shells view's perspective, each cell's edges its corners at the edge's length. { core: [[a, b], …], ring: [[a, b], …] }. */
export function coverEdges() {
  const C = stageCorners(STAGE), core = WQ_VERTICES.findIndex((v) => v[0] > 2 - 1e-9);
  const ti = (v) => C.map((_, k) => k).filter((k) => cornerEdge(k).includes(v));
  const tt = (c) => C.map((_, k) => k).filter((k) => STAGE_TRIANGLE_CELLS[Math.floor(k / 3)].includes(c));
  const coreCorners = ti(core), h = C[coreCorners[0]][0], eye = -h - EYE_GAP;
  const P = (x) => WQ_FRAMES[0].map((f) => (dot(x, f) * (h - eye)) / (x[0] - eye));
  const dist = (a, b) => Math.hypot(...C[a].map((x, i) => x - C[b][i]));
  let len = Infinity;
  for (let i = 1; i < coreCorners.length; i++) len = Math.min(len, dist(coreCorners[0], coreCorners[i]));
  const edgesOf = (ks) => { const out = []; ks.forEach((a, i) => ks.slice(i + 1).forEach((b) => { if (Math.abs(dist(a, b) - len) < 1e-7) out.push([a, b]); })); return out; };
  const near = new Set(WQ_EDGES.filter((e) => e.includes(core)).map(([a, b]) => (a === core ? b : a)));
  const ring = [...[...near].map(ti), ...WQ_CELLS.map((c, ci) => (c.includes(core) ? tt(ci) : null)).filter(Boolean)];
  const seen = new Set(), pick = (ks) => edgesOf(ks).filter(([a, b]) => { const key = `${a},${b}`; if (seen.has(key)) return false; seen.add(key); return true; }).map(([a, b]) => [P(C[a]), P(C[b])]);
  const coreEdges = pick(coreCorners);
  return { core: coreEdges, ring: ring.flatMap(pick) };
}
