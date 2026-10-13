// Almanac (Stage 1 -- docs/RHOMBIVERSE_SPEC_ALMANAC.md section 5): the
// static list + detail panel view. Wired to the real `openAlmanac`
// action (see render.js's onAction, previously just a "not built yet"
// toast). Content comes entirely from almanac-data.js -- this file only
// renders it, never invents its own copy. No 3D preview yet (Stage 3).
//
// Structurally mirrors cyborg.js's createCyborgMode: a create*() factory
// (render.js's own established convention for interactive sub-panels,
// distinct from welcome.js/changelog.js's simpler self-mounting
// <script> pattern -- Almanac needs an exported open()/close()/toggle()
// API because, unlike those two, it has no dedicated always-visible
// trigger button of its own; it's only ever opened via the wheel's
// Almanac face), CSS injected once via injectCssOnce() rather than
// added to index.html's own embedded stylesheet, same visual language
// (cyan accent, near-black panel) as changelog.js/cyborg.js already use.
import { ALMANAC_ENTRIES } from './almanac-data.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { createLanguageButton } from './language-picker.js';
import { mountWireframePreview } from './wireframe-preview.js';
import { polyShapeEdges } from './poly-shapes.js';
// DICTO's entries read their words in the current language; the older entries are English.
const lang = () => getSettings().language;
// DICTO's findings and the known results have i18n words (alm.d.<key>.*); DICTO's pieces their own names.
const WORDED = new Set(['dicto', 'known']);
const labelOf = (e) => (WORDED.has(e.kind) ? t(`alm.d.${e.key}.label`, lang()) : e.label);
const KIND_KEY = { dicto: 'alm.kind.dicto', dictoPiece: 'alm.kind.pieces', known: 'alm.kind.known' };
import { iconFrame, MARKS } from './wheel-icons.js';

const CSS = `
.almanac-overlay {
  display: none;
  position: fixed; inset: 0; z-index: 990;
  align-items: center; justify-content: center;
  background: rgba(5, 5, 10, 0.88);
  backdrop-filter: blur(2px);
  padding: 24px 12px;
  box-sizing: border-box;
}
.almanac-overlay.open { display: flex; }
.almanac-card {
  width: 100%; max-width: 520px; max-height: 84vh;
  overflow-y: auto;
  color: #ddd; font: var(--text-m)/1.5 var(--font-ui);
  background: rgba(15, 15, 25, 0.96);
  border: 1px solid rgba(var(--accent-rgb), 0.35);
  border-radius: var(--radius-l);
  padding: 18px 22px 22px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
}
.almanac-header {
  display: flex; align-items: center; justify-content: space-between;
  font: 700 var(--text-l) var(--font-ui);
  color: var(--accent);
  margin-bottom: 12px;
}
.almanac-header-tools { display: flex; align-items: center; gap: 8px; }
.almanac-close { background: none; border: none; color: var(--accent); cursor: pointer; font: var(--text-l) var(--font-ui); }
.almanac-list { display: flex; flex-direction: column; gap: 4px; }
.almanac-entry {
  display: flex; align-items: center; gap: 10px;
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-s);
  padding: 8px 10px;
  color: #eee;
  font: var(--text-m) var(--font-ui);
  text-align: left;
  cursor: pointer;
}
.almanac-entry.here { border-color: var(--accent); background: rgba(var(--accent-rgb), 0.16); }
.almanac-entry:hover { background: rgba(var(--accent-rgb), 0.12); border-color: rgba(var(--accent-rgb), 0.4); }
.almanac-entry-icon { flex: 0 0 auto; font-size: 22px; color: var(--accent); line-height: 0; }
.almanac-entry-icon:empty { display: none; }
.almanac-entry-label { flex: 1 1 auto; }
.almanac-kind {
  font: 700 var(--text-xs) var(--font-ui);
  letter-spacing: 0.04em; text-transform: uppercase;
  color: #789;
  margin: 14px 0 4px;
}
.almanac-kind:first-child { margin-top: 0; }
.almanac-detail { display: none; }
.almanac-preview { display: block; width: 120px; height: 120px; margin: 0 auto 8px; }
.almanac-how { margin-top: 12px; padding: 10px 12px; border: 1px solid rgba(var(--accent-rgb), 0.3); border-radius: var(--radius-s); background: rgba(var(--accent-rgb), 0.06); }
.almanac-how-title { font: 700 var(--text-xs) var(--font-ui); letter-spacing: 0.04em; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.almanac-ref { margin-top: 10px; font: var(--text-s) var(--font-ui); color: #9ab; }
.almanac-ref a { color: var(--accent); }
.almanac-open {
  display: block; width: 100%; margin-top: 12px; padding: 10px 12px; min-height: 44px;
  background: rgba(var(--accent-rgb), 0.18); border: 1px solid var(--accent); border-radius: var(--radius-s);
  color: #fff; font: 700 var(--text-m) var(--font-ui); cursor: pointer;
}
.almanac-open:hover { background: rgba(var(--accent-rgb), 0.3); }
.almanac-back {
  background: none; border: none; color: var(--accent); cursor: pointer;
  font: var(--text-m) var(--font-ui); padding: 0; margin-bottom: 12px;
}
.almanac-detail-icon { font-size: 48px; color: var(--accent); text-align: center; margin-bottom: 8px; line-height: 0; }
.almanac-detail-icon:empty { display: none; }
.almanac-detail-title { font: 700 var(--text-xl) system-ui, sans-serif; color: #fff; margin-bottom: 8px; text-align: center; }
.almanac-detail-stats {
  text-align: center;
  color: var(--accent);
  font: 700 var(--text-xs) var(--font-ui);
  letter-spacing: 0.03em;
  margin-bottom: 10px;
}
.almanac-detail-desc { color: #ccd; font-size: var(--text-m); }
`;

function injectCssOnce() {
  if (document.getElementById('almanac-style')) return;
  const style = document.createElement('style');
  style.id = 'almanac-style';
  style.textContent = CSS;
  document.head.appendChild(style);
}

// almanac-data.js's own entry `kind`s (piece/concept/history), given a
// real section heading here -- markKey-less entries (the 2 lattice
// concepts, spec section 6's open question) simply render with no icon
// (.almanac-*-icon:empty collapses to nothing) rather than a placeholder.
const KIND_LABEL = { piece: 'Pieces', concept: 'Lattice Concepts', history: 'History' };

function iconHtml(markKey, label) {
  return markKey && MARKS[markKey] ? iconFrame(MARKS[markKey], { title: label }) : '';
}

// Stage 2 (docs/RHOMBIVERSE_SPEC_ALMANAC.md section 5): entry.stats is
// either a real computed {vertexCount,edgeCount,faceCount} (single-cell
// convex pieces) or a real {composedOf,unit} (cluster pieces -- see
// almanac-data.js's own header for why those don't get a fabricated
// V/E/F). Lattice-concept/history entries have no stats at all, so this
// renders nothing for them, same :empty-collapse convention the icon
// slots already use.
function statsHtml(stats) {
  if (!stats) return '';
  if (typeof stats.vertexCount === 'number') {
    return `<div class="almanac-detail-stats">${stats.vertexCount} vertices &middot; ${stats.edgeCount} edges &middot; ${stats.faceCount} faces</div>`;
  }
  if (typeof stats.composedOf === 'number') {
    // Real singular/plural forms from almanac-data.js, not a naive "+s"
    // (a real bug found live: "Hemi RD half" -> "Hemi RD halfs").
    const unit = stats.composedOf === 1 ? stats.unit : stats.unitPlural;
    return `<div class="almanac-detail-stats">Composed of ${stats.composedOf} &times; ${unit}</div>`;
  }
  return '';
}

// onOpen(entry, label): Open on an entry opens its world or piece in the app (DICTO 2026-10-13).
export function createAlmanac({ onOpen } = {}) {
  injectCssOnce();

  const overlay = document.createElement('div');
  overlay.className = 'almanac-overlay';
  overlay.innerHTML = `
    <div class="almanac-card">
      <div class="almanac-header"><span>Almanac</span><span class="almanac-header-tools"><button type="button" class="almanac-close">✕</button></span></div>
      <div class="almanac-list"></div>
      <div class="almanac-detail"></div>
    </div>`;
  document.body.appendChild(overlay);

  // 🌐 beside ✕ (DICTO 2026-10-13); the list and the open entry redraw in the new language.
  overlay.querySelector('.almanac-close').before(createLanguageButton());
  let shownIndex = -1, shownLang = getSettings().language;
  onSettingsChange((st) => {
    if (st.language === shownLang) return;
    shownLang = st.language;
    if (!overlay.classList.contains('open')) return;
    renderList();
    if (detailEl.style.display === 'block' && shownIndex >= 0) showDetail(shownIndex);
  });
  const listEl = overlay.querySelector('.almanac-list');
  const detailEl = overlay.querySelector('.almanac-detail');

  // Grouped by kind, in ALMANAC_ENTRIES' own order (pieces, then lattice
  // concepts, then history -- see almanac-data.js) rather than one flat
  // list, since which section an entry is in is itself useful context.
  function renderList() {
    let sectionsHtml = '';
    let lastKind = null;
    ALMANAC_ENTRIES.forEach((entry, i) => {
      if (entry.kind !== lastKind) {
        sectionsHtml += `<div class="almanac-kind">${KIND_KEY[entry.kind] ? t(KIND_KEY[entry.kind], lang()) : KIND_LABEL[entry.kind] ?? entry.kind}</div>`;
        lastKind = entry.kind;
      }
      sectionsHtml += `
      <button type="button" class="almanac-entry" data-index="${i}">
        <span class="almanac-entry-icon">${iconHtml(entry.markKey, labelOf(entry))}</span>
        <span class="almanac-entry-label">${labelOf(entry)}</span>
      </button>`;
    });
    listEl.innerHTML = sectionsHtml;
    listEl.querySelectorAll('.almanac-entry').forEach((el) => {
      el.addEventListener('click', () => showDetail(Number(el.dataset.index)));
    });
  }
  let disposePreview = null;

  function showList() {
    listEl.style.display = 'flex';
    detailEl.style.display = 'none';
    listEl.querySelector('.almanac-entry.here')?.scrollIntoView({ block: 'center' });
  }

  function showDetail(index) {
    const entry = ALMANAC_ENTRIES[index];
    if (!entry) return;
    shownIndex = index;
    disposePreview?.(); disposePreview = null;
    if (KIND_KEY[entry.kind]) {
      const L = lang();
      const st = entry.stats;
      const desc = WORDED.has(entry.kind) ? t(`alm.d.${entry.key}.desc`, L)
        : t(entry.finding ? 'alm.piece.desc' : 'alm.piece.descNone', L, { n: entry.finding });
      const ref = entry.kind === 'known' ? `${t('alm.ref', L, { n: entry.finding })} · ${t('alm.known', L)}`
        : entry.finding ? `DICTO · ${t('alm.ref', L, { n: entry.finding })}${entry.doi ? ` · <a href="https://doi.org/${entry.doi}" target="_blank" rel="noopener">DOI ${entry.doi}</a>` : ''}` : 'DICTO';
      detailEl.innerHTML = `
      <button type="button" class="almanac-back">&larr; ${t('alm.back', L)}</button>
      ${entry.shape ? '<canvas class="almanac-preview"></canvas>' : ''}
      <div class="almanac-detail-title">${labelOf(entry)}</div>
      ${st ? `<div class="almanac-detail-stats">${t('alm.stats', L, { v: st.vertexCount, e: st.edgeCount, f: st.faceCount })}</div>` : ''}
      <div class="almanac-detail-desc">${desc}</div>
      ${WORDED.has(entry.kind) ? `<div class="almanac-how"><div class="almanac-how-title">${t('alm.how', L)}</div>${t(`alm.d.${entry.key}.how`, L)}</div>` : ''}
      ${entry.action && onOpen ? `<button type="button" class="almanac-open">${t('alm.open', L)}</button>` : ''}
      <div class="almanac-ref">${ref}</div>`;
      const cv = detailEl.querySelector('.almanac-preview');
      if (cv) disposePreview = mountWireframePreview(cv, polyShapeEdges(entry.shape), 120);
      detailEl.querySelector('.almanac-back').addEventListener('click', showList);
      detailEl.querySelector('.almanac-open')?.addEventListener('click', () => { close(); onOpen(entry, labelOf(entry)); });
      listEl.style.display = 'none';
      detailEl.style.display = 'block';
      return;
    }
    detailEl.innerHTML = `
      <button type="button" class="almanac-back">&larr; Back</button>
      <div class="almanac-detail-icon">${iconHtml(entry.markKey, entry.label)}</div>
      <div class="almanac-detail-title">${entry.label}</div>
      ${statsHtml(entry.stats)}
      <div class="almanac-detail-desc">${entry.desc}</div>`;
    detailEl.querySelector('.almanac-back').addEventListener('click', showList);
    listEl.style.display = 'none';
    detailEl.style.display = 'block';
  }

  overlay.querySelector('.almanac-close').addEventListener('click', () => close());
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });

  // open(id): straight to that entry when there is one (where you are), its row marked in the list.
  function open(id = null) {
    renderList(); // in the current language
    showList(); // always reset to the list view on (re)open
    const i = id ? ALMANAC_ENTRIES.findIndex((e) => e.id === id) : -1;
    if (i >= 0) {
      listEl.querySelector(`[data-index="${i}"]`)?.classList.add('here');
      showDetail(i);
    }
    overlay.classList.add('open');
  }
  function close() {
    disposePreview?.(); disposePreview = null;
    overlay.classList.remove('open');
  }
  function toggle() {
    if (overlay.classList.contains('open')) close();
    else open();
  }

  return { open, close, toggle };
}
