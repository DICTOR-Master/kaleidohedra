// Lattice Select (DICTO 2026-10-17): Rhombiverse's 3D+ shows which lattice you are on ("Lattice · fcc") with a Select toggle beside it.
// Select opens the lattices in the order of the world menu by the books (DICTO 2026-11-17, book-menu-data.js), the same order as every
// other door: the books' own (in series order, paper order inside a book), then Others' lattices and tilings, then Studies and tools;
// a section with none of the lattices is not listed. Neutral headings (cover, "Book N", title), no ring or app colours. A station is
// one of today's lattices, picked exactly as the DICTO wizard picks it, so nothing else changes: Rhombiverse still arrives on fcc with
// its rhombic dodecahedra, in cyan (DICTO: the heart of Rhombiverse, never to change). Rhombiverse door only. Words: i18n lat.* and
// the menu's own (wiz.book.*, wiz.books.*); the names are the menu's.
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { K_WORLDS, LATTICES_3D } from './dimension-wizard.js';
import { BOOKS, EXTRA_WORLDS, OTHERS_SHELF, TOOLS_SHELF } from './book-menu-data.js';

// Stations: the wizard's lattice (key), the short name the Lattice row shows (n) and what picking it does (action: the lattice's
// first piece or its world).
export const STATIONS = {
  fcc: { n: 'fcc · RD', action: 'tool:pieceType:rd' },
  dictofcc: { n: 'DICTO FCC', action: 'tool:pieceType:dictofcc' },
  rdDual: { n: 'RD Dual', action: 'tool:cuboctaBuild' },
  bcc: { n: 'bcc · TO', action: 'tool:pieceType:to' },
  bccGaps: { n: 'BCC gaps', action: 'tool:pieceType:ioct' },
  ed: { n: 'ED', action: 'tool:pieceType:elongdodeca' },
  pyrochlore: { n: 'Pyrochlore', action: 'tool:pieceType:pyrochlore' },
  hex: { n: 'Hex prisms', action: 'tool:pieceType:hexprism' },
  triprism: { n: 'Triangular prisms', action: 'tool:pieceType:triprism' },
  dictohex: { n: 'DICTO Hex Prism', action: 'tool:pieceType:dictohex' },
  hcp: { n: 'hcp · TRD', action: 'tool:pieceType:hcp' },
  gyro: { n: 'Gyrated octet', action: 'tool:pieceType:gyro' },
  rhombohedral: { n: 'Rhombohedral', action: 'tool:pieceType:rhombohedra' },
  golden: { n: 'Golden Rhombohedra', action: 'tool:goldenWorld' },
  breathing: { n: 'Breathing Pyrochlore', action: 'tool:breathingWorld' },
  bodhiPyro: { n: 'Bodhi Networks', action: 'tool:bodhiPyroWorld' },
};
const worldLabel = (k) => EXTRA_WORLDS[k]?.label ?? (K_WORLDS.find((w) => w.key === k) ?? LATTICES_3D.find((l) => l.key === k))?.label ?? STATIONS[k].n;
// The sheet's sections, in the menu's order: [{ id, book?, items: [{ key, name }] }].
export const LATTICE_SECTIONS = [
  ...BOOKS.map((b) => ({ id: b.id, book: b, items: b.worlds.map(([k]) => k).filter((k) => STATIONS[k]).map((k) => ({ key: k, name: worldLabel(k) })) })),
  { id: 'others', items: OTHERS_SHELF.filter((s) => STATIONS[s.lat ?? s.world]).map((s) => ({ key: s.lat ?? s.world, name: s.name })) },
  { id: 'tools', items: TOOLS_SHELF.filter((s) => STATIONS[s.world]).map((s) => ({ key: s.world, name: worldLabel(s.world) })) },
].filter((s) => s.items.length);
// any piece of a lattice counts as being on it (Hemi RD, Hourglass … are on fcc)
const KEY_OF = new Map(LATTICES_3D.flatMap((l) => l.pieces.map((p) => [p.action, l.key])));
const esc = (x) => String(x).replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;');

const CSS = `
#hud-lattice-row { position: fixed; top: 80px; left: 16px; z-index: 900; display: flex; align-items: center; gap: 8px; max-width: calc(100% - 96px); }
#hud-world-row:not([hidden]) ~ #hud-lattice-row { top: 124px; }
#hud-lattice-row[hidden] { display: none; }
#hud-lattice-row .lat-lbl { color: rgba(230, 233, 240, 0.6); font: var(--text-xs) var(--font-ui); letter-spacing: .14em; text-transform: uppercase; }
#hud-lattice-row .lat-name { color: var(--accent); font: 600 var(--text-s) var(--font-ui); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
#hud-lattice-row button { flex: none; box-sizing: border-box; min-height: var(--touch-compact); padding: 0 10px; background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(var(--accent-rgb), 0.45); border-radius: var(--radius-s); color: var(--accent); font: var(--text-xs) var(--font-ui); cursor: pointer; touch-action: manipulation; }
#lattice-select { --ls-line: rgba(220, 214, 200, 0.16); --ls-ink: #ece6d8; --ls-dim: #a59c8c; position: fixed; inset: 0; z-index: 2500; background: rgba(6, 8, 12, 0.92);
  overflow-y: auto; overscroll-behavior: contain; padding: 176px 16px 24px; box-sizing: border-box; }
#lattice-select[hidden] { display: none; }
#lattice-select .lat-list { max-width: 720px; margin: 0 auto; background: rgba(15, 17, 24, 0.96); border: 1px solid var(--ls-line); border-radius: var(--radius-m); padding: 4px 12px 8px; }
#lattice-select .lat-sec { border-bottom: 1px solid var(--ls-line); padding-bottom: 6px; }
#lattice-select .lat-sec:last-child { border-bottom: 0; }
#lattice-select .lat-head { display: flex; align-items: center; gap: 12px; min-height: 64px; padding: 6px 4px; box-sizing: border-box; color: var(--ls-ink); }
#lattice-select .lat-cover { flex: none; width: 40px; height: 56px; object-fit: cover; border-radius: 3px; background: #222; }
#lattice-select .lat-shelf { flex: none; width: 40px; height: 56px; }
#lattice-select .lat-titles { display: flex; flex-direction: column; min-width: 0; }
#lattice-select .lat-num { color: var(--ls-dim); font: 600 var(--text-xs) var(--font-ui); letter-spacing: 0.06em; text-transform: uppercase; }
#lattice-select .lat-title { font: 600 var(--text-m)/1.25 var(--font-ui); color: var(--ls-ink); }
#lattice-select .lat-st { display: flex; align-items: center; gap: 10px; width: 100%; min-height: 48px; padding: 4px 10px 4px 56px; box-sizing: border-box; background: none; border: 0;
  border-radius: var(--radius-m); color: var(--ls-ink); text-align: left; cursor: pointer; touch-action: manipulation; font: var(--text-s) var(--font-ui); }
#lattice-select .lat-st:hover, #lattice-select .lat-st:focus-visible { background: rgba(255, 255, 255, 0.05); }
#lattice-select .lat-st.on { background: rgba(255, 255, 255, 0.1); font-weight: 600; }
#lattice-select .lat-st.on::after { content: '●'; margin-left: auto; color: var(--ls-dim); font-size: 10px; }
@media (max-width: 600px) { #lattice-select { padding-top: 168px; } #lattice-select .lat-st { padding-left: 14px; } }
`;

export function createLatticeSelect({ go }) {
  const style = document.createElement('style'); style.textContent = CSS; document.head.appendChild(style);
  const row = document.createElement('div'); row.id = 'hud-lattice-row'; row.hidden = true;
  row.innerHTML = '<span class="lat-lbl"></span><span class="lat-name"></span><button type="button" class="lat-toggle"></button>';
  const worldRow = document.getElementById('hud-world-row');
  worldRow ? worldRow.after(row) : document.body.appendChild(row);
  const sheet = document.createElement('div'); sheet.id = 'lattice-select'; sheet.hidden = true;
  document.body.appendChild(sheet);
  let key = 'fcc', dim = '3D'; // Rhombiverse arrives on fcc
  const L = () => getSettings().language;

  function renderRow() {
    const st = STATIONS[key];
    row.hidden = dim !== '3D' || !st;
    if (!st) return;
    row.querySelector('.lat-lbl').textContent = t('lat.label', L());
    row.querySelector('.lat-name').textContent = st.n;
    row.querySelector('.lat-toggle').textContent = sheet.hidden ? `${t('lat.select', L())} ▾` : `${t('lat.done', L())} ▴`;
  }
  function renderSheet() {
    sheet.innerHTML = `<div class="lat-list">${LATTICE_SECTIONS.map((s) => {
      const b = s.book;
      const pic = b?.cover ? `<img class="lat-cover" src="assets/books/${b.cover}.webp" alt="" width="40" height="56">` : '<span class="lat-shelf"></span>';
      const titles = b ? `<span class="lat-num">${esc(t(`wiz.book.${b.id}`, L()))}</span><span class="lat-title">${esc(b.title)}</span>` : `<span class="lat-title">${esc(t(`wiz.books.${s.id}`, L()))}</span>`;
      return `<section class="lat-sec" data-sec="${s.id}"><div class="lat-head">${pic}<span class="lat-titles">${titles}</span></div>${s.items.map((it) => `<button type="button" class="lat-st${it.key === key ? ' on' : ''}" data-key="${it.key}"${it.key === key ? ' aria-current="true"' : ''}>${esc(it.name)}</button>`).join('')}</section>`;
    }).join('')}</div>`;
    sheet.querySelectorAll('img.lat-cover').forEach((img) => img.addEventListener('error', () => { img.style.visibility = 'hidden'; }, { once: true }));
    sheet.querySelectorAll('.lat-st').forEach((el) => el.addEventListener('click', () => { const st = STATIONS[el.dataset.key]; close(); go(st.action, st.n); }));
  }
  // the row stays above the open sheet, so Done is where Select was
  function openSheet() { renderSheet(); sheet.hidden = false; sheet.scrollTop = 0; row.style.zIndex = '2600'; renderRow(); }
  function close() { sheet.hidden = true; row.style.zIndex = ''; renderRow(); }
  row.querySelector('.lat-toggle').addEventListener('click', () => (sheet.hidden ? openSheet() : close()));
  sheet.addEventListener('click', (e) => { if (e.target === sheet) close(); });
  onSettingsChange(() => { renderRow(); if (!sheet.hidden) renderSheet(); });

  return {
    /** A pick from anywhere (the wizard, the Almanac, a station): the lattice it is on, if it is one of the stations. */
    setAction(dimension, action) {
      dim = dimension;
      const k = Object.keys(STATIONS).find((s) => STATIONS[s].action === action) ?? (STATIONS[KEY_OF.get(action)] ? KEY_OF.get(action) : undefined);
      key = k ?? null; renderRow();
    },
    setDimension(d) { dim = d; if (d !== '3D') close(); renderRow(); },
    get key() { return key; },
    get isOpen() { return !sheet.hidden; },
    close,
  };
}
