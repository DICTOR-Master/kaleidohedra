// Which front door the visitor came in by (KRP, DICTO's decisions 2026-10-08): Kaleidohedra and
// Rhombiverse are one app from one code (Polyhedraverse too since step D6), each with its own front door (its own address, name,
// colour and saved state). Each page sets <html data-site>; ?site= overrides it for local work.

export const SITES = {
  // netsGroups: the Nets world's groups shown in this app's space (null: all of them).
  // shear: whether this app's space has Kaleidohedra's lattice shear.
  // analytics: Vercel Web Analytics is switched on for this site's project (analytics.js counts DICTO).
  // wordmark: the name in two tones, the second part in the app's accent (as Polyhedraverse's name).
  kaleidohedra: { name: 'Kaleidohedra', wordmark: ['KALEIDO', 'HEDRA'], colour: '#ff9a52', url: 'https://kaleidohedra.dictospheres.com', netsGroups: ['voronoi', 'platonic', 'ekp'], shear: true, inside: true, door: true, analytics: false },
  // inside: whether its worlds run in this app (Polyhedraverse's since step D2); door: whether this
  // build can open as that app (?site=, SITE). Polyhedraverse is a door since step D6.
  polyhedraverse: { name: 'Polyhedraverse', wordmark: ['POLYHEDRA', 'VERSE'], colour: '#5ee233', url: 'https://polyhedraverse.dictospheres.com', netsGroups: null, shear: false, inside: true, door: true, analytics: false },
  // DICTO's own space (DICTO 2026-10-09): 1D+ and 2D+ belong to no app, an easier way in; silver.
  // Going up to 3D+ from there lands in the door's app.
  dicto: { name: 'DICTO', wordmark: ['DIC', 'TO'], colour: '#d8dce6', url: '', netsGroups: null, shear: false, inside: true, door: false },
  rhombiverse: { name: 'Rhombiverse', wordmark: ['RHOMBI', 'VERSE'], colour: '#22c3e6', url: 'https://rhombiverse.dictospheres.com', netsGroups: null, shear: false, inside: true, door: true, analytics: false },
};

function detect() {
  const fromQuery = globalThis.location ? new URLSearchParams(globalThis.location.search).get('site') : null;
  const fromPage = globalThis.document?.documentElement?.dataset?.site;
  for (const s of [fromQuery, fromPage]) if (s && SITES[s]?.door) return s;
  return 'rhombiverse';
}

/** 'kaleidohedra', 'rhombiverse' or 'polyhedraverse'. */
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

// The new home (DICTO 2026-10-10): each door moved from <app>.vercel.app to <app>.dictospheres.com. A
// browser keeps saved builds per address, so the old address carries them across once: it packs this
// browser's saved state into the new address's #fragment (never sent to a server) and goes there; the
// new address unpacks it, keeping anything it already has, and reloads clean. Later visits to the old
// address just go to the new one.
const NEW_HOME = { 'kaleidohedra.vercel.app': 'kaleidohedra.dictospheres.com', 'rhombiverse.vercel.app': 'rhombiverse.dictospheres.com', 'polyhedraverse.vercel.app': 'polyhedraverse.dictospheres.com' };
const MOVE_TAG = '#krp-move=';
async function packed(text) {
  const bytes = new TextEncoder().encode(text);
  if (!globalThis.CompressionStream) return 'p' + btoa(String.fromCharCode(...bytes));
  const gz = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer());
  let bin = '';
  for (let i = 0; i < gz.length; i += 0x8000) bin += String.fromCharCode(...gz.subarray(i, i + 0x8000));
  return 'g' + btoa(bin);
}
async function unpacked(data) {
  const bin = atob(data.slice(1)), bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  if (data[0] === 'p') return new TextDecoder().decode(bytes);
  return new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
}
function moveHome() {
  const loc = globalThis.location;
  if (!loc || !globalThis.localStorage) return;
  const target = NEW_HOME[loc.hostname];
  if (target) {
    let saved = {};
    try {
      if (!localStorage.getItem('krp-moved')) for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); saved[k] = localStorage.getItem(k); }
    } catch { saved = {}; }
    const go = (frag) => loc.replace(`${loc.protocol}//${target}${loc.port ? `:${loc.port}` : ""}${loc.pathname}${loc.search}${frag}`);
    if (!Object.keys(saved).length) { go(''); return; }
    packed(JSON.stringify(saved)).then((data) => {
      if (data.length > 1500000) return; // too big to carry in an address: stay here, nothing lost
      try { localStorage.setItem('krp-moved', '1'); } catch { /* best-effort */ }
      go(MOVE_TAG + encodeURIComponent(data));
    }).catch(() => go(''));
    return;
  }
  if (loc.hash.startsWith(MOVE_TAG)) {
    const data = decodeURIComponent(loc.hash.slice(MOVE_TAG.length));
    history.replaceState(null, '', loc.pathname + loc.search);
    unpacked(data).then((text) => {
      const saved = JSON.parse(text);
      for (const [k, v] of Object.entries(saved)) if (localStorage.getItem(k) === null) localStorage.setItem(k, v);
      loc.reload();
    }).catch(() => { /* a damaged move: start fresh here, the old address still has everything */ });
  }
}
moveHome();

// ---- Colour: which app's space you are in (DICTO, 2026-10-08: "colour scheme orients you") ----
// accent: text and outlines; strong: first placements, highlights; piece: the default piece colour;
// contrast: a "tap here" that stands out against the accent (cyan on orange, amber on cyan);
// highlight: the dimension label, Send, the undo strip (Rhombiverse amber, Kaleidohedra orange).
// Rhombiverse cyan, Kaleidohedra orange, Polyhedraverse green, DICTO's own space silver.
const THEMES = {
  kaleidohedra: { pale: '#ffc9a0', highlight: '#ff6a00', highlightRgb: '255, 106, 0', accent: '#ff9a52', accentRgb: '255, 106, 0', strong: '#ff6a00', piece: '#ff6a00', pieceRgb: '255, 106, 0', contrast: '#22c3e6', contrastRgb: '34, 195, 230', accentHex: 0xff9a52, strongHex: 0xff6a00, pieceHex: 0xff6a00, contrastHex: 0x22c3e6 },
  polyhedraverse: { pale: '#d8ffcc', highlight: '#5ee233', highlightRgb: '94, 226, 51', accent: '#a9f795', accentRgb: '94, 226, 51', strong: '#5ee233', piece: '#5ee233', pieceRgb: '94, 226, 51', contrast: '#ff9a52', contrastRgb: '255, 154, 82', accentHex: 0xa9f795, strongHex: 0x5ee233, pieceHex: 0x5ee233, contrastHex: 0xff9a52 },
  dicto: { pale: '#f2f4f8', highlight: '#e6e9ef', highlightRgb: '230, 233, 239', accent: '#d8dce6', accentRgb: '200, 205, 220', strong: '#ffffff', piece: '#c9ced8', pieceRgb: '201, 206, 216', contrast: '#22c3e6', contrastRgb: '34, 195, 230', accentHex: 0xd8dce6, strongHex: 0xffffff, pieceHex: 0xc9ced8, contrastHex: 0x22c3e6 },
  rhombiverse: { pale: '#dfefff', highlight: '#f59e0b', highlightRgb: '245, 158, 11', accent: '#9de0ff', accentRgb: '124, 204, 255', strong: '#7cf', piece: '#22c3e6', pieceRgb: '34, 195, 230', contrast: '#f59e0b', contrastRgb: '245, 158, 11', accentHex: 0x9de0ff, strongHex: 0x00e5ff, pieceHex: 0x22c3e6, contrastHex: 0xf59e0b },
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
  root.style.setProperty('--highlight', t.highlight);
  root.style.setProperty('--highlight-rgb', t.highlightRgb);
  root.style.setProperty('--contrast-rgb', t.contrastRgb);
  root.dataset.activeSite = active;
  const mark = globalThis.document.getElementById('hud-wordmark');
  if (mark) { const [a, b] = SITES[active].wordmark; mark.replaceChildren(a, Object.assign(globalThis.document.createElement('span'), { textContent: b })); }
}
/** Enter another app's space (or DICTO's own, 1D+ and 2D+): its colours take over. */
export function setActiveSite(site) {
  if (!SITES[site]?.inside || site === active) return;
  active = site;
  applyTheme();
  globalThis.dispatchEvent?.(new CustomEvent('krp-site', { detail: site }));
}
applyTheme();
