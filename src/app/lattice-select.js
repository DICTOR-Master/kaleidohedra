// Lattice Select (DICTO 2026-10-17): Rhombiverse's 3D+ shows which lattice you are on ("Lattice · fcc") with a Select toggle beside it.
// Select opens three blocks, sized by family: Cubic (the largest), Hexagonal, Golden (the smallest, the specialists). Each block is a metro
// line of at most three stations (DICTO: "3 is a good number to pick from"); a station with more inside it opens onto its own three
// (never a "more" button). A station is one of today's lattices, picked exactly as the DICTO wizard picks it, so nothing else changes:
// Rhombiverse still arrives on fcc with its rhombic dodecahedra, in cyan (DICTO: the heart of Rhombiverse, never to change).
// Rhombiverse door only. Words: i18n lat.*; the lattice names are the wizard's.
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { LATTICES_3D } from './dimension-wizard.js';

// Stations: n = the name shown; key = the wizard's lattice; action = what picking it does (the lattice's first piece or its world).
export const LATTICE_BLOCKS = [
  { id: 'cubic', st: [
    { n: 'fcc', kids: [
      { n: 'fcc · RD', key: 'fcc', action: 'tool:pieceType:rd' },
      { n: 'DICTO FCC', key: 'dictofcc', action: 'tool:pieceType:dictofcc' },
      { n: 'RD Dual', key: 'rdDual', action: 'tool:cuboctaBuild' },
    ] },
    { n: 'bcc', kids: [
      { n: 'bcc · TO', key: 'bcc', action: 'tool:pieceType:to' },
      { n: 'BCC gaps', key: 'bccGaps', action: 'tool:pieceType:ioct' },
      { n: 'ED', key: 'ed', action: 'tool:pieceType:elongdodeca' },
    ] },
    { n: 'Pyrochlore', key: 'pyrochlore', action: 'tool:pieceType:pyrochlore' },
  ] },
  { id: 'hex', st: [
    { n: 'Hexagonal', key: 'hex', action: 'tool:pieceType:hexprism' },
    { n: 'Rhombohedral', key: 'rhombohedral', action: 'tool:pieceType:rhombohedra' },
  ] },
  { id: 'golden', st: [
    { n: 'Golden Rhombohedra', key: 'golden', action: 'tool:goldenWorld' },
    { n: 'Breathing Pyrochlore', key: 'breathing', action: 'tool:breathingWorld' },
    { n: 'Bodhi Networks', key: 'bodhiPyro', action: 'tool:bodhiPyroWorld' },
  ] },
];
// long names on two lines, so three stations fit side by side
const lines = (n) => { const w = n.split(' '); if (n.length <= 11 || w.length < 2) return [n]; const h = Math.ceil(w.length / 2); return [w.slice(0, h).join(' '), w.slice(h).join(' ')]; };
const leaves = (st) => st.flatMap((s) => (s.kids ? leaves(s.kids) : [s]));
const STATION = new Map(LATTICE_BLOCKS.flatMap((b) => leaves(b.st)).map((s) => [s.key, s]));
// any piece of a lattice counts as being on it (Hemi RD, Hourglass … are on fcc)
const KEY_OF = new Map(LATTICES_3D.flatMap((l) => l.pieces.map((p) => [p.action, l.key])));

const CSS = `
#hud-lattice-row { position: fixed; top: 80px; left: 16px; z-index: 900; display: flex; align-items: center; gap: 8px; max-width: calc(100% - 96px); }
#hud-world-row:not([hidden]) ~ #hud-lattice-row { top: 124px; }
#hud-lattice-row[hidden] { display: none; }
#hud-lattice-row .lat-lbl { color: rgba(230, 233, 240, 0.6); font: var(--text-xs) var(--font-ui); letter-spacing: .14em; text-transform: uppercase; }
#hud-lattice-row .lat-name { color: var(--accent); font: 600 var(--text-s) var(--font-ui); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
#hud-lattice-row button, #lattice-select .lat-back { flex: none; box-sizing: border-box; min-height: var(--touch-compact); padding: 0 10px; background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(var(--accent-rgb), 0.45); border-radius: var(--radius-s); color: var(--accent); font: var(--text-xs) var(--font-ui); cursor: pointer; touch-action: manipulation; }
#lattice-select { position: fixed; inset: 0; z-index: 2500; background: rgba(6, 8, 12, 0.9); display: flex; flex-direction: column; padding: 176px 16px 16px; box-sizing: border-box; }
#lattice-select[hidden] { display: none; }
#lattice-select .lat-wall { flex: 1; min-height: 0; display: grid; gap: 10px; grid-template-columns: 1.6fr 1fr; grid-template-rows: 1.15fr 1fr; max-width: 1100px; width: 100%; margin: 0 auto; }
#lattice-select .lat-blk { background: rgba(15, 17, 24, 0.95); border: 1px solid rgba(var(--accent-rgb), 0.25); border-radius: var(--radius-m); display: flex; flex-direction: column; min-width: 0; min-height: 0; padding: 10px 12px; }
#lattice-select .lat-blk.cubic { grid-row: 1 / 3; }
#lattice-select .lat-bh { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
#lattice-select .lat-bh b { color: var(--accent); font: 600 var(--text-m) var(--font-ui); }
#lattice-select .lat-bh span { color: rgba(230, 233, 240, 0.55); font: var(--text-xs) var(--font-ui); }
#lattice-select .lat-bh .lat-back { margin-left: auto; }
#lattice-select svg { flex: 1; min-height: 120px; width: 100%; max-width: 520px; margin: 0 auto; }
#lattice-select .ln { stroke: var(--accent); stroke-width: 5; stroke-linecap: round; opacity: .5; fill: none; }
#lattice-select .st { cursor: pointer; }
#lattice-select .st circle { fill: #0b0d12; stroke: var(--accent); stroke-width: 4; }
#lattice-select .st.on circle { fill: var(--accent); }
#lattice-select .st text { fill: #e6e9f0; font: 13px var(--font-ui); text-anchor: middle; }
#lattice-select .st .kids { fill: rgba(230, 233, 240, 0.55); font-size: 11px; }
@media (max-width: 700px) { #lattice-select .lat-wall { grid-template-columns: 1fr; grid-template-rows: 1.3fr 1fr 1fr; } #lattice-select .lat-blk.cubic { grid-row: auto; } }
`;

export function createLatticeSelect({ go }) {
  const style = document.createElement('style'); style.textContent = CSS; document.head.appendChild(style);
  const row = document.createElement('div'); row.id = 'hud-lattice-row'; row.hidden = true;
  row.innerHTML = '<span class="lat-lbl"></span><span class="lat-name"></span><button type="button" class="lat-toggle"></button>';
  const worldRow = document.getElementById('hud-world-row');
  worldRow ? worldRow.after(row) : document.body.appendChild(row);
  const sheet = document.createElement('div'); sheet.id = 'lattice-select'; sheet.hidden = true;
  sheet.innerHTML = `<div class="lat-wall">${LATTICE_BLOCKS.map((b) => `<section class="lat-blk ${b.id}" data-blk="${b.id}"></section>`).join('')}</div>`;
  document.body.appendChild(sheet);
  let key = 'fcc', dim = '3D'; // Rhombiverse arrives on fcc
  const path = new Map(); // block id -> the station opened inside it (or none)
  const L = () => getSettings().language;

  function renderRow() {
    const st = STATION.get(key);
    row.hidden = dim !== '3D' || !st;
    if (!st) return;
    row.querySelector('.lat-lbl').textContent = t('lat.label', L());
    row.querySelector('.lat-name').textContent = st.n;
    row.querySelector('.lat-toggle').textContent = sheet.hidden ? `${t('lat.select', L())} ▾` : `${t('lat.done', L())} ▴`;
  }
  function renderBlock(b) {
    const el = sheet.querySelector(`[data-blk="${b.id}"]`), open = path.get(b.id), list = open ? open.kids : b.st;
    const xs = list.map((_, i) => (list.length === 1 ? 180 : 50 + i * (260 / (list.length - 1))));
    const count = leaves(b.st).length;
    el.innerHTML = `<div class="lat-bh"><b>${t(`lat.block.${b.id}`, L())}</b><span>${t('lat.count', L(), { n: count })}${open ? ` · ${open.n}` : ''}</span>${open ? `<button type="button" class="lat-back">${t('wiz.back', L())}</button>` : ''}</div>
      <svg viewBox="0 0 360 124" preserveAspectRatio="xMidYMid meet">${list.length > 1 ? `<path class="ln" d="M${xs[0]} 52 H${xs[xs.length - 1]}"/>` : ''}${list.map((s, i) => {
        const on = s.key === key || (s.kids && leaves(s.kids).some((k) => k.key === key));
        return `<g class="st${on ? ' on' : ''}" data-i="${i}"><rect x="${xs[i] - 56}" y="8" width="112" height="112" fill="transparent"/><circle cx="${xs[i]}" cy="52" r="13"/><text x="${xs[i]}" y="86">${lines(s.n).map((w, j) => `<tspan x="${xs[i]}" dy="${j ? 15 : 0}">${w}</tspan>`).join('')}</text>${s.kids ? `<text class="kids" x="${xs[i]}" y="26">${t('lat.more', L(), { n: s.kids.length })} ›</text>` : ''}</g>`;
      }).join('')}</svg>`;
    el.querySelector('.lat-back')?.addEventListener('click', () => { path.delete(b.id); renderBlock(b); });
    el.querySelectorAll('.st').forEach((g) => g.addEventListener('click', () => {
      const s = list[Number(g.dataset.i)];
      if (s.kids) { path.set(b.id, s); renderBlock(b); return; }
      close(); go(s.action, s.n);
    }));
  }
  // the row stays above the open sheet, so Done is where Select was
  function openSheet() { path.clear(); LATTICE_BLOCKS.forEach(renderBlock); sheet.hidden = false; row.style.zIndex = '2600'; renderRow(); }
  function close() { sheet.hidden = true; row.style.zIndex = ''; renderRow(); }
  row.querySelector('.lat-toggle').addEventListener('click', () => (sheet.hidden ? openSheet() : close()));
  sheet.addEventListener('click', (e) => { if (e.target === sheet) close(); });
  onSettingsChange(() => { renderRow(); if (!sheet.hidden) LATTICE_BLOCKS.forEach(renderBlock); });

  return {
    /** A pick from anywhere (the wizard, the Almanac, a station): the lattice it is on, if it is one of the stations. */
    setAction(dimension, action) {
      dim = dimension;
      const k = STATION.has(KEY_OF.get(action)) ? KEY_OF.get(action) : [...STATION.values()].find((s) => s.action === action)?.key;
      key = k ?? null; renderRow();
    },
    setDimension(d) { dim = d; if (d !== '3D') close(); renderRow(); },
    get key() { return key; },
    get isOpen() { return !sheet.hidden; },
    close,
  };
}
