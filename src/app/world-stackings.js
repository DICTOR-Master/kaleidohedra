// The Stackings World (DICTO 2026-10-26, "yes to all" on the design): the companion world of paper #57, "The Rule of Halves: the
// Holes of Every Close-Packed Stacking" (DICTO DOI 10.5281/zenodo.23647898). A button for each standard polytype (3C, 2H, 4H, 6H, 9R,
// 15R), one big slider for the weight λ over the walk −11/24 … 3/8, and one column of holes through a period of the stacking: every
// tetrahedral piece coloured by its nearest layer, every octahedral piece cut at its mid-plane into the two halves the rule of halves
// names, each coloured by the layer on its side; cubic gold, hexagonal platinum (as the #57 card and #58 Figure 3). A Janus c/h
// piece shows both metals. The caption gives the census: c and h layers, and the share of space in tetrahedral and octahedral pieces,
// which depends only on the fraction of h layers (k-research studies/2026-10-26-rule-of-halves-census). Geometry: stackings-geometry.js.
import { createLayeredWorld } from './world-chains.js';
import { t } from './i18n.js';
import { PRESETS, LAYER_H, LAM_LO, LAM_HI, stackingPieces, census, layerTypes } from './stackings-geometry.js';

export const STACKING_KINDS = Object.keys(PRESETS);
const ROLE_OF = { c: 'stkC', h: 'stkH' };

// one column of holes, `size` periods tall, centred on the origin; pieces cached per word and λ
const cache = new Map();
function column(word, lam) {
  const key = `${word}.${lam}`;
  if (!cache.has(key)) { if (cache.size > 60) cache.clear(); cache.set(key, stackingPieces(word, lam)); }
  return cache.get(key);
}
/** [role, vertices, faces, site, { anchor, kind }] for the drawn column. */
export function stackingColumn(word, size, lam) {
  const P = column(word, lam), H = word.length * LAYER_H, out = [], mid = (size * H) / 2;
  for (let r = 0; r < size; r++) for (const p of P) {
    const dz = r * H - mid, move = (v) => [v[0] - 0.5, v[2] + dz, v[1] - 0.3];   // z up in the study, y up in the app
    const anchor = move(p.site);
    out.push([ROLE_OF[p.type], p.vertices.map(move), p.faces, anchor, { anchor, kind: `${p.role}.${p.type}` }]);
  }
  return out;
}

// ---- the slider: u = 0..1000 runs λ over the walk; the stops are the ends of #57's four stretches ----
const STOPS = [[LAM_LO, 'start'], [-3 / 8, 's1'], [-1 / 8, 's2'], [5 / 24, 's3'], [LAM_HI, 'end']];
const uOf = (l) => Math.round((1000 * (l - LAM_LO)) / (LAM_HI - LAM_LO));
export const STACKING_STOPS = STOPS.map(([v, key]) => ({ u: uOf(v), v, key }));
const lamOf = (u) => STACKING_STOPS.find((s) => s.u === u)?.v ?? LAM_LO + ((LAM_HI - LAM_LO) * u) / 1000;
const fmt = (v, d = 3) => v.toFixed(d).replace('-', '−');
const pct = (v) => `${(100 * v).toFixed(1)}%`;
function caption(word, l, L) {
  const st = STACKING_STOPS.find((s) => s.v === l), c = census(word, l, column(word, l));
  const head = st ? t(`stackings.stop.${st.key}`, L) : `λ = ${fmt(l)}`;
  return `${head} · ${layerTypes(word).join('')} · ${t('stackings.caption.census', L, { c: c.c, h: c.h, tet: pct(c.tetShare), oct: pct(c.octShare) })}`;
}

export const STACKING_VIEWS = Object.fromEntries(STACKING_KINDS.map((k) => [k, {
  maxSize: PRESETS[k].length > 6 ? 1 : 2, viewDir: [1, 0.35, 1.2],
  param: { start: uOf(0), stops: STACKING_STOPS, value: lamOf, caption: (l, L) => caption(PRESETS[k], l, L), pauseAt: [] },
  views: { column: (size, o) => stackingColumn(PRESETS[k], size, o.param) },
}]));

export function createStackingsWorld({ scene, fitView, openAction }) {
  return createLayeredWorld({ scene, fitView, name: 'stackings', data: STACKING_VIEWS, kinds: STACKING_KINDS, prefix: 'stackings', glassRoles: {},
    defaultParts: Object.fromEntries(STACKING_KINDS.map((k) => [k, 'column'])), kindButtons: true, rowWords: { size: 'stackings.periods', shells: 'dictonic.topLayer' }, foldNote: true,
    openAction });
}

/** Points whose convex hull previews the world in the DICTO menu: Chucky, the Janus piece of 4H at λ = 0, both halves. */
export const stackingsPreviewPoints = () => {
  const P = stackingPieces('ABAC', 0), gap = P.find((p) => p.role === 'octBottom' && p.type !== P.find((q) => q.role === 'octTop' && q.gap === p.gap)?.type)?.gap ?? 0;
  return P.filter((p) => p.role !== 'tet' && p.gap === gap).flatMap((p) => p.vertices);
};
