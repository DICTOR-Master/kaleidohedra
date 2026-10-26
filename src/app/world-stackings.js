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
export const MAX_LAYERS = 30;   // a flipped stacking whose period would be longer is refused (the column would be too heavy)

// phase 2 (DICTO 2026-10-26): each polytype's current word (flipped layers change it) and the piece last tapped
const state = { words: { ...PRESETS }, picked: null };
export const currentWord = (k) => state.words[k];
const third = (a, b) => 'ABC'.replace(a, '').replace(b, '');
/** The ABC word with the given cyclic h/c sequence (layer k is h when layers k−1 and k+1 match), repeated until it closes, or null. */
export function wordFromTypes(types) {
  const n = types.length;
  for (let reps = 1; reps <= 3; reps++) {
    const m = n * reps, L = ['A', 'B'];
    for (let k = 1; k <= m; k++) L.push(types[k % n] === 'h' ? L[k - 1] : third(L[k - 1], L[k]));
    if (L[m] === L[0] && L[m + 1] === L[1]) return m <= MAX_LAYERS ? L.slice(0, m).join('') : null;
  }
  return null;
}
/** Flip layer k of polytype `kind` between c and h; false if the result would be too long. */
export function flipLayer(kind, k) {
  const types = layerTypes(state.words[kind]); types[k] = types[k] === 'c' ? 'h' : 'c';
  const w = wordFromTypes(types);
  if (!w) return false;
  state.words[kind] = w; state.picked = null; return true;
}
export function resetLayers(kind) { state.words[kind] = PRESETS[kind]; state.picked = null; }

// one column of holes, `size` periods tall, centred on the origin; pieces cached per word and λ
const cache = new Map();
function column(word, lam) {
  const key = `${word}.${lam}`;
  if (!cache.has(key)) { if (cache.size > 60) cache.clear(); cache.set(key, stackingPieces(word, lam)); }
  return cache.get(key);
}
/** [role, vertices, faces, site, { anchor, kind }] for the drawn column. */
export function stackingColumn(word, size, lam) {
  const P = column(word, lam), H = word.length * LAYER_H, out = [], mid = (size * H) / 2;   // size: periods (one in the world)
  for (let r = 0; r < size; r++) for (const p of P) {
    const dz = r * H - mid, move = (v) => [v[0] - 0.5, v[2] + dz, v[1] - 0.3];   // z up in the study, y up in the app
    const anchor = move(p.site), tag = `${word}|${P.indexOf(p)}`;
    out.push([state.picked === tag ? 'stkSel' : ROLE_OF[p.type], p.vertices.map(move), p.faces, anchor, { anchor, kind: `${p.role}.${p.type}`, tags: p.faces.map(() => tag) }]);
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
  maxSize: 1, viewDir: [1, 0.35, 1.2],
  param: { start: uOf(0), stops: STACKING_STOPS, value: lamOf, caption: (l, L) => caption(currentWord(k), l, L), pauseAt: [] },
  views: { column: (size, o) => stackingColumn(currentWord(k), size, o.param) },
  onTap: (tag) => { if (!tag.startsWith(`${currentWord(k)}|`)) return false; state.picked = state.picked === tag ? null : tag; return true; },
}]));

/** The piece last tapped, in words: which piece, its layer and type, its volume (and for a half, the whole piece and whether it is Janus). */
export function pickedInfo(kind, lam, L) {
  if (!state.picked) return t('stackings.info.tap', L);
  const [word, i] = state.picked.split('|'); if (word !== currentWord(kind)) return t('stackings.info.tap', L);
  const P = column(word, lam), p = P[Number(i)]; if (!p) return t('stackings.info.tap', L);
  const vars = { n: p.layer + 1, type: p.type, v: fmt(p.volume, 4) };
  if (p.role === 'tet') return t('stackings.info.tet', L, vars);
  const both = P.filter((q) => q.role !== 'tet' && q.gap === p.gap), whole = both.reduce((a, q) => a + q.volume, 0);
  const janus = new Set(both.map((q) => q.type)).size > 1;
  return t(p.role === 'octTop' ? 'stackings.info.top' : 'stackings.info.bottom', L, { ...vars, w: fmt(whole, 4) }) + (janus ? t('stackings.info.janus', L) : '');
}
function mountLayers(panel, getWorld) {
  const box = document.createElement('div'); box.className = 'stk-layers'; box.style.order = '10'; box.style.textAlign = 'center';
  box.innerHTML = '<div class="stk-layers-label st-note"></div><div class="w4d-row w4d-options stk-chips"></div><div class="stk-info st-note"></div>';
  const cap = panel.querySelector('.ch-param-caption'); (cap?.parentElement ?? panel).insertBefore(box, cap?.nextSibling ?? null);
  let last = null;
  const paint = ({ kind, v, L }) => {
    last = { kind, v, L };
    const w = currentWord(kind), types = layerTypes(w);
    box.querySelector('.stk-layers-label').textContent = t('stackings.layers', L);
    const chips = box.querySelector('.stk-chips'); chips.textContent = '';
    types.forEach((ty, k) => { const b = document.createElement('button'); b.type = 'button'; b.dataset.stkLayer = String(k); b.className = `stk-chip stk-${ty}`; b.style.borderColor = ty === 'c' ? '#f2b84b' : '#d9d6cf'; b.textContent = `${k + 1} ${w[k]} ${ty}`; chips.append(b); });
    if (w !== PRESETS[kind]) { const r = document.createElement('button'); r.type = 'button'; r.dataset.stkReset = '1'; r.className = 'stk-chip'; r.textContent = t('stackings.reset', L, { k: kind }); chips.append(r); }
    box.querySelector('.stk-info').textContent = pickedInfo(kind, v, L);
  };
  box.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b || !last) return;
    if (b.dataset.stkReset) resetLayers(last.kind);
    else if (b.dataset.stkLayer && !flipLayer(last.kind, Number(b.dataset.stkLayer))) { box.querySelector('.stk-info').textContent = t('stackings.toolong', last.L, { n: MAX_LAYERS }); return; }
    getWorld()?.refresh();
  });
  return { update: paint };
}

export function createStackingsWorld({ scene, fitView, openAction }) {
  let world = null;
  world = createLayeredWorld({ scene, fitView, name: 'stackings', data: STACKING_VIEWS, kinds: STACKING_KINDS, prefix: 'stackings', glassRoles: {},
    defaultParts: Object.fromEntries(STACKING_KINDS.map((k) => [k, 'column'])), kindButtons: true, hideRows: ['size'], rowWords: { shells: 'dictonic.topLayer' }, foldNote: true,
    theorem: (panel) => mountLayers(panel, () => world), openAction });
  return world;
}

/** Points whose convex hull previews the world in the DICTO menu: Chucky, the Janus piece of 4H at λ = 0, both halves. */
export const stackingsPreviewPoints = () => {
  const P = stackingPieces('ABAC', 0), gap = P.find((p) => p.role === 'octBottom' && p.type !== P.find((q) => q.role === 'octTop' && q.gap === p.gap)?.type)?.gap ?? 0;
  return P.filter((p) => p.role !== 'tet' && p.gap === gap).flatMap((p) => p.vertices);
};
