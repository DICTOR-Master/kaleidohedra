// The Icosaxes Bloom (DICTO 2026-10-27): the companion world of paper #59, "The Icosaxes Hexa: Bloom, Bud and Seed" (DICTO DOI
// 10.5281/zenodo.23677485). Twenty Icosaxes (or Lotus Jewel Axes), one on each corner of a dodecahedron, slid in towards the centre
// by one big slider that snaps to the exact stops: first touch, the Bloom (twelve open windows); 1/φ, the Bud (sealed round a hollow);
// 1/3, the Seed (one solid; Lotus Jewel Axes 1/φ³). ▶ Play runs them in and holds at each stop. The third button shows the Icosaxes
// Hexa (8 Icosaxes round an Unborn Axes), the Lotus Hexa (keyed outward round a Dodecaxes) and a patch of the keyed Icosaxes Kagome
// network (every Icosaxes in two blocks). Geometry: bloom-geometry.js. Names by DICTO.
import { createLayeredWorld } from './world-chains.js';
import { t } from './i18n.js';
import { STOP_FRACTIONS as SF, twenty, hexa, kagome, ICOSAXES } from './bloom-geometry.js';

export const BLOOM_KINDS = ['icosaxes', 'lotus', 'hexa'];
const F_HI = 1.25, F_LO = 0.2;                                    // the slider runs from a little apart to deep inside
const uOf = (f) => Math.round((1000 * (F_HI - f)) / (F_HI - F_LO));
const stopsFor = (lotus) => [[F_HI, 'apart'], [SF.bloom, 'bloom'], [SF.bud, 'bud'], lotus ? [SF.lotusSeed, 'lotusSeed'] : [SF.seed, 'seed'], [F_LO, 'end']]
  .map(([v, key]) => ({ u: uOf(v), v, key }));
export const BLOOM_STOPS = { icosaxes: stopsFor(false), lotus: stopsFor(true) };
const valueOf = (stops) => (u) => stops.find((s) => s.u === u)?.v ?? F_HI - ((F_HI - F_LO) * u) / 1000;
const seedOf = (lotus) => (lotus ? SF.lotusSeed : SF.seed);
function caption(lotus, f, L) {
  const st = BLOOM_STOPS[lotus ? 'lotus' : 'icosaxes'].find((s) => s.v === f);
  const state = f > SF.bloom + 1e-9 ? 'apart' : f > SF.bud + 1e-9 ? 'open' : f > seedOf(lotus) + 1e-9 ? 'sealed' : 'solid';
  const head = st ? t(`bloom.stop.${st.key}`, L) : t('bloom.caption.at', L, { f: f.toFixed(3) });
  return `${head} · ${t(`bloom.state.${state}`, L)}`;
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
const blocks = (list) => list.map((p) => piece(p.role === 'big' ? 'bloomBig' : 'bloomSmall', p));
const sliding = (lotus) => {
  const stops = BLOOM_STOPS[lotus ? 'lotus' : 'icosaxes'];
  return { maxSize: 1, viewDir: [0.25, 0.35, 1],
    param: { start: stops.find((s) => s.key === 'bloom').u, stops, value: valueOf(stops), caption: (f, L) => caption(lotus, f, L), pauseAt: stops.filter((s) => ['bloom', 'bud', 'seed', 'lotusSeed'].includes(s.key)).map((s) => s.u) },
    views: { twenty: (size, o) => twentyAt(lotus, o.param) } };
};
export const BLOOM_VIEWS = {
  icosaxes: sliding(false),
  lotus: sliding(true),
  hexa: { maxSize: 1, viewDir: [1, 0.7, 1.3], views: { hexa: blocks(hexa(false)), lotusHexa: blocks(hexa(true)), kagome: blocks(kagome()) } },
};
export function createBloomWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'bloom', data: BLOOM_VIEWS, kinds: BLOOM_KINDS, prefix: 'bloom', glassRoles: {},
    defaultParts: { icosaxes: 'twenty', lotus: 'twenty', hexa: 'hexa' }, kindButtons: true, hideRows: ['size', 'shells'], foldNote: true, openAction });   // shells hidden: the twenty sit at one distance, nothing to peel
}
/** Points whose convex hull previews the world in the DICTO menu: one Icosaxes. */
export const bloomPreviewPoints = () => ICOSAXES.vertices;
