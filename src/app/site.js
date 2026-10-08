// Which front door the visitor came in by (KRP, DICTO's decisions 2026-10-08): Kaleidohedra and
// Rhombiverse are one app from one code, each with its own front door (its own address, name,
// colour and saved state). Each page sets <html data-site>; ?site= overrides it for local work.

export const SITES = {
  // netsGroups: the Nets world's groups shown in this app's space (null: all of them).
  // shear: whether this app's space has Kaleidohedra's lattice shear.
  // wordmark: the name in two tones, the second part in the app's accent (as Polyhedraverse's name).
  kaleidohedra: { name: 'Kaleidohedra', wordmark: ['KALEIDO', 'HEDRA'], colour: '#ff9a52', url: 'https://kaleidohedra.vercel.app', netsGroups: ['voronoi', 'platonic', 'ekp'], shear: true, inside: true },
  // inside: whether its worlds run in this app yet (Polyhedraverse opens its own site until KRP step D).
  polyhedraverse: { name: 'Polyhedraverse', wordmark: ['POLYHEDRA', 'VERSE'], colour: '#5ee233', url: 'https://polyhedraverse.vercel.app', netsGroups: null, shear: false, inside: false },
  rhombiverse: { name: 'Rhombiverse', wordmark: ['RHOMBI', 'VERSE'], colour: '#22c3e6', url: 'https://rhombiverse.vercel.app', netsGroups: null, shear: false, inside: true },
};

function detect() {
  const fromQuery = globalThis.location ? new URLSearchParams(globalThis.location.search).get('site') : null;
  const fromPage = globalThis.document?.documentElement?.dataset?.site;
  for (const s of [fromQuery, fromPage]) if (s && SITES[s]?.inside) return s;
  return 'rhombiverse';
}

/** 'kaleidohedra' or 'rhombiverse'. */
export const SITE = detect();
export const IS_KALEIDOHEDRA = SITE === 'kaleidohedra';

/** A localStorage key in this site's own namespace, e.g. storageKey('nets-world') -> 'kaleidohedra-nets-world'.
 *  Each site keeps the key names it always had, so nobody's saved worlds are lost. */
export const storageKey = (name) => `${SITE}-${name}`;

// Kaleidohedra began as a copy of Rhombiverse's engine and kept most of its key names
// ('rhombiverse-settings', 'rhombiverse-world', ...). Now every key carries its own site's name: on
// Kaleidohedra, any old 'rhombiverse-' entry without a 'kaleidohedra-' twin is copied over once, so
// nothing anyone saved is lost. (The two sites are different origins, so they never shared storage.)
function adoptLegacyKeys() {
  if (SITE === 'rhombiverse' || !globalThis.localStorage) return;
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k?.startsWith('rhombiverse-')) continue;
      const mine = `${SITE}-${k.slice('rhombiverse-'.length)}`;
      if (localStorage.getItem(mine) === null) localStorage.setItem(mine, localStorage.getItem(k));
    }
  } catch { /* storage blocked: nothing to adopt */ }
}
adoptLegacyKeys();

// ---- Colour: which app's space you are in (DICTO, 2026-10-08: "colour scheme orients you") ----
// accent: text and outlines; strong: first placements, highlights; piece: the default piece colour;
// contrast: a "tap here" that stands out against the accent (cyan on orange, amber on cyan).
// Rhombiverse cyan, Kaleidohedra orange (Polyhedraverse green joins with step D).
const THEMES = {
  kaleidohedra: { pale: '#ffc9a0', accent: '#ff9a52', accentRgb: '255, 106, 0', strong: '#ff6a00', piece: '#ff6a00', pieceRgb: '255, 106, 0', contrast: '#22c3e6', contrastRgb: '34, 195, 230', accentHex: 0xff9a52, strongHex: 0xff6a00, pieceHex: 0xff6a00, contrastHex: 0x22c3e6 },
  polyhedraverse: { pale: '#d8ffcc', accent: '#a9f795', accentRgb: '94, 226, 51', strong: '#5ee233', piece: '#5ee233', pieceRgb: '94, 226, 51', contrast: '#ff9a52', contrastRgb: '255, 154, 82', accentHex: 0xa9f795, strongHex: 0x5ee233, pieceHex: 0x5ee233, contrastHex: 0xff9a52 },
  rhombiverse: { pale: '#dfefff', accent: '#9de0ff', accentRgb: '124, 204, 255', strong: '#7cf', piece: '#22c3e6', pieceRgb: '34, 195, 230', contrast: '#f59e0b', contrastRgb: '245, 158, 11', accentHex: 0x9de0ff, strongHex: 0x00e5ff, pieceHex: 0x22c3e6, contrastHex: 0xf59e0b },
};
let active = SITE;
/** The colours of the app whose space you are in now (read when drawing, not once at start). */
export const theme = () => THEMES[active];
/** Any app's colours (the DICTO wizard shows each app in its own). */
export const themeOf = (site) => THEMES[site];
export const activeSite = () => active;
function applyTheme() {
  const root = globalThis.document?.documentElement;
  if (!root) return;
  const t = theme();
  root.style.setProperty('--pale', t.pale);
  root.style.setProperty('--accent', t.accent);
  root.style.setProperty('--accent-rgb', t.accentRgb);
  root.style.setProperty('--accent-strong', t.strong);
  root.style.setProperty('--piece', t.piece);
  root.style.setProperty('--piece-rgb', t.pieceRgb);
  root.style.setProperty('--contrast', t.contrast);
  root.style.setProperty('--contrast-rgb', t.contrastRgb);
  root.dataset.activeSite = active;
  const mark = globalThis.document.getElementById('hud-wordmark');
  if (mark) { const [a, b] = SITES[active].wordmark; mark.replaceChildren(a, Object.assign(globalThis.document.createElement('span'), { textContent: b })); }
}
/** Enter another app's space (its worlds opened from its wizard tab): its colours take over. */
export function setActiveSite(site) {
  if (!SITES[site]?.inside || site === active) return;
  active = site;
  applyTheme();
  globalThis.dispatchEvent?.(new CustomEvent('krp-site', { detail: site }));
}
applyTheme();
