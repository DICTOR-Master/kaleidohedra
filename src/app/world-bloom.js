// The Icosaxes Bloom (DICTO 2026-10-27): the companion world of paper #59, "The Icosaxes Hexa: Bloom, Bud and Seed" (DICTO DOI
// 10.5281/zenodo.23677485). Twenty Icosaxes (or Lotus Jewel Axes), one on each corner of a dodecahedron, slid in towards the centre
// to the exact stops only (DICTO 2026-10-27, 'stops sounds best': overlapping pieces between stops look messy): first touch, the Bloom
// (twelve open windows); 1/φ, the Bud (sealed round a hollow); 1/3, the Seed (one solid; Lotus Jewel Axes 1/φ³). Each stop shows the
// joined solid (bloom-joined-data.js); Pieces shows the twenty separate pieces at that stop. ▶ Play steps through the stops. The third button shows the Icosaxes
// Hexa (8 Icosaxes round an Unborn Axes), the Lotus Hexa (keyed outward round a Dodecaxes) and a patch of the keyed Icosaxes Kagome
// network (every Icosaxes in two blocks). Geometry: bloom-geometry.js. Names by DICTO.
import { createLayeredWorld } from './world-chains.js';
import { t } from './i18n.js';
import { STOP_FRACTIONS as SF, twenty, hexa, kagome, ICOSAXES } from './bloom-geometry.js';
import JOINED from './bloom-joined-data.js';

export const BLOOM_KINDS = ['icosaxes', 'lotus', 'hexa'];
// three slider positions, evenly spaced: the Bloom, the Bud and the Seed (the Lotus Jewel Seed for Lotus Jewel Axes)
const stopsFor = (lotus) => [[SF.bloom, 'bloom'], [SF.bud, 'bud'], lotus ? [SF.lotusSeed, 'lotusSeed'] : [SF.seed, 'seed']].map(([v, key], i) => ({ u: i * 500, v, key }));
export const BLOOM_STOPS = { icosaxes: stopsFor(false), lotus: stopsFor(true) };
const valueOf = (stops) => (u) => stops.reduce((a, s) => (Math.abs(s.u - u) < Math.abs(a.u - u) ? s : a)).v;   // always a stop
const stopAt = (lotus, f) => BLOOM_STOPS[lotus ? 'lotus' : 'icosaxes'].find((s) => s.v === f);
function caption(lotus, f, L) {
  const st = stopAt(lotus, f), state = st.key === 'bloom' ? 'open' : st.key === 'bud' ? 'sealed' : 'solid';
  return `${t(`bloom.stop.${st.key}`, L)} · ${t(`bloom.state.${state}`, L)}`;
}
// [role, vertices, faces, anchor, { anchor, kind }] — the twenty in the app's frame (y up: the five-fold axis (0, 1, φ) points up)
const PHI = (1 + Math.sqrt(5)) / 2, A = [0, 1, PHI].map((x) => x / Math.hypot(1, PHI));
const B = [1, 0, 0], C = [A[1] * B[2] - A[2] * B[1], A[2] * B[0] - A[0] * B[2], A[0] * B[1] - A[1] * B[0]];
const toApp = (v) => [v[0] * B[0] + v[1] * B[1] + v[2] * B[2], v[0] * A[0] + v[1] * A[1] + v[2] * A[2], v[0] * C[0] + v[1] * C[1] + v[2] * C[2]];
const piece = (role, p) => { const anchor = toApp(p.centre); return [role, p.vertices.map(toApp), p.faces, anchor, { anchor, kind: role }]; };
const cache = new Map();
function twentyAt(lotus, f) {
  const k = `${lotus}${f}`;
  if (!cache.has(k)) { if (cache.size > 40) cache.clear(); cache.set(k, twenty(lotus, f).map((p) => piece(lotus ? 'bloomL' : 'bloomI', p))); }
  return cache.get(k);
}
// The joined solid is stored as triangles: draw only the edges where the surface folds (or ends), not the triangles' own seams.
function featureEdges(V, F) {
  const sub = (a, b) => a.map((x, i) => x - b[i]), cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const N = F.map(([a, b, c]) => { const n = cross(sub(V[b], V[a]), sub(V[c], V[a])), l = Math.hypot(...n) || 1; return n.map((x) => x / l); });
  const by = new Map();
  F.forEach((f, ti) => f.forEach((k, i) => { const m = f[(i + 1) % 3], key = k < m ? `${k},${m}` : `${m},${k}`; if (!by.has(key)) by.set(key, []); by.get(key).push(ti); }));
  const out = [];
  for (const [key, T] of by) {
    const flat = T.length === 2 && N[T[0]].reduce((s, x, i) => s + x * N[T[1]][i], 0) > 0.9998;   // under about 1° of fold: a seam, not an edge
    if (!flat) out.push(key.split(',').map(Number));
  }
  return out;
}
function joined(lotus, f) {
  const key = `${lotus ? 'lotus' : 'icosaxes'}.${stopAt(lotus, f).key}`, k = `j${key}`;
  if (!cache.has(k)) {
    const J = JOINED[key], V = [], F = [];
    for (let i = 0; i < J.v.length; i += 3) V.push(toApp([J.v[i], J.v[i + 1], J.v[i + 2]]));
    for (let i = 0; i < J.t.length; i += 3) F.push([J.t[i], J.t[i + 1], J.t[i + 2]]);
    cache.set(k, [[lotus ? 'bloomL' : 'bloomI', V, F, [0, 0, 0], { anchor: [0, 0, 0], kind: key, edges: featureEdges(V, F) }]]);
  }
  return cache.get(k);
}
const blocks = (list) => list.map((p) => piece(p.role === 'big' ? 'bloomBig' : 'bloomSmall', p));
const sliding = (lotus) => {
  const stops = BLOOM_STOPS[lotus ? 'lotus' : 'icosaxes'];
  return { maxSize: 1, viewDir: [0.25, 0.35, 1],
    param: { start: 0, stops, snap: 250, value: valueOf(stops), caption: (f, L) => caption(lotus, f, L), pauseAt: stops.map((s) => s.u) },
    views: { joined: (size, o) => joined(lotus, o.param), pieces: (size, o) => twentyAt(lotus, o.param) } };
};
export const BLOOM_VIEWS = {
  icosaxes: sliding(false),
  lotus: sliding(true),
  hexa: { maxSize: 1, viewDir: [1, 0.7, 1.3], views: { hexa: blocks(hexa(false)), lotusHexa: blocks(hexa(true)), kagome: blocks(kagome()) } },
};
export function createBloomWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'bloom', data: BLOOM_VIEWS, kinds: BLOOM_KINDS, prefix: 'bloom', glassRoles: {},
    defaultParts: { icosaxes: 'joined', lotus: 'joined', hexa: 'hexa' }, kindButtons: true, hideRows: ['size', 'shells'], foldNote: true, openAction });   // shells hidden: the twenty sit at one distance, nothing to peel
}
/** Points whose convex hull previews the world in the DICTO menu: one Icosaxes. */
export const bloomPreviewPoints = () => ICOSAXES.vertices;
