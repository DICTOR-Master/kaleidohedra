// Dimension-select wizard (2026-09-22): the app's real entry gate --
// force-opened once on every load (see render.js's init(), right after
// this module's factory is called) and reachable again any time via the
// Home wheel's "Change Dimension" face. Picks which dimension tier
// (2D+ Nets or 3D+) you're building in, then which lattice family within
// it is active first (families coexist once inside -- this only sets the
// default, same as picking a piece from the existing Piece wheel today).
//
// Direct correction, same session: an earlier draft put this ON the
// Rhombic Wheel itself (a WHEEL_DIMENSION/WHEEL_LATTICE_3D config pair in
// rhombic-wheel-3d-core.js). "As in polyhedraverse one list two routes" --
// polyhedraverse keeps its wheel (PolyhedralWheel) and its card list
// (ShapeBrowser) as two deliberately SEPARATE surfaces, not one folded
// into the other (confirmed directly against polyhedraverse's own
// page.tsx wiring). This is rhombiverse's own version of that list: a
// real wireframe-card overlay, structurally the almanac.js factory
// pattern (create*() -> {open,close,toggle}, CSS injected once, not
// welcome.js's simpler self-mounting <script> pattern -- this has no
// dedicated always-visible trigger button of its own, same reasoning
// almanac.js's own header already gives). "The wheel has breakdown
// family shapes as in 3D currently" -- the wheel keeps doing exactly
// what it already does (Piece -> RD Family), untouched; this file is the
// ONLY place dimension/family selection itself lives now.
//
// "Wheel has simplified 2D symbol shapes [and the] wizard has
// wireframes" -- direct distinction from the same conversation: this
// file's previews are real wireframe line drawings (2D canvas, no THREE/
// WebGL -- a second simultaneous full WebGL render alongside render.js's
// own main scene is a real, already-fixed perf mistake in this codebase,
// see welcome.js's own header), NOT wheel-icons.js's hand-authored
// symbol marks -- a different, more literal visual language for a
// different job (browsing/picking real geometry vs. a compact nav icon).
//
// "Simplicity is key... when all primitives are available, the UI
// should close everything down to simple selections with no extraneous
// out of scope steps visible" -- direct instruction. All wording goes
// through i18n.js ('wiz.*'); lattice, piece and tile names
// stay English.
import { mountWireframePreview } from './wireframe-preview.js';
import { t } from './i18n.js';
import { dimensionLabel } from './dimension-label.js';
import { getSettings } from './settings.js';

const CSS = `
.dim-wizard-overlay {
  display: none;
  position: fixed; inset: 0; z-index: 991;
  align-items: center; justify-content: center;
  background: rgba(5, 5, 10, 0.92);
  backdrop-filter: blur(2px);
  padding: 24px 12px;
  box-sizing: border-box;
}
.dim-wizard-overlay.open { display: flex; }
.dim-wizard-card {
  width: 100%; max-width: 560px; max-height: 88vh;
  overflow-y: auto;
  color: #ddd; font: 14px/1.5 system-ui, sans-serif;
  background: rgba(15, 15, 25, 0.97);
  border: 1px solid rgba(255, 106, 0, 0.35);
  border-radius: 10px;
  padding: 18px 22px 22px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
}
.dim-wizard-header {
  display: flex; align-items: center; justify-content: space-between;
  font: 700 16px system-ui, sans-serif;
  color: #ff9a52;
  margin-bottom: 4px;
}
.dim-wizard-close { background: none; border: none; color: #ff9a52; cursor: pointer; font: 15px system-ui, sans-serif; }
.dim-wizard-back {
  background: none; border: none; color: #ff9a52; cursor: pointer;
  font: 13px system-ui, sans-serif; padding: 0; margin-bottom: 10px;
}
.dim-wizard-sub { color: #99a; font-size: 12px; margin-bottom: 14px; }
/* A vertical LIST of rows (like polyhedraverse's own family tabs/list),
   not a box grid -- direct correction, same session: "each dimension is
   lists like polyhedraverse not boxes"/"run through a list with all
   dimensions like polyhedra families." */
.dim-wizard-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.dim-wizard-card-btn {
  display: flex; flex-direction: row; align-items: center; gap: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 106, 0, 0.3);
  border-radius: 8px;
  padding: 8px 12px;
  color: #eee;
  cursor: pointer;
  text-align: left;
  width: 100%;
}
.dim-wizard-card-btn:hover { background: rgba(255, 106, 0, 0.1); border-color: rgba(255, 106, 0, 0.6); }
.dim-wizard-preview { width: 40px; height: 40px; flex: 0 0 auto; }
.dim-wizard-section { display: flex; flex-direction: column; gap: 2px; margin: 10px 0 2px; }
.dim-wizard-section:first-child { margin-top: 0; }
.dim-wizard-piece { margin-left: 14px; width: calc(100% - 14px); }
.dim-wizard-row-text { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.dim-wizard-label { font: 700 13px system-ui, sans-serif; color: #fff; }
.dim-wizard-desc { font-size: 11px; color: #9ab; line-height: 1.35; }
.dim-wizard-serial-row { display: flex; gap: 6px; margin-bottom: 4px; }
.dim-wizard-serial-row input {
  flex: 1; min-width: 0; font: 16px system-ui, sans-serif; color: #eee;
  background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 106, 0, 0.35); border-radius: 8px; padding: 8px 10px;
}
.dim-wizard-serial-row button {
  font: 600 14px system-ui, sans-serif; color: #ff9a52; background: rgba(255, 106, 0, 0.12);
  border: 1px solid rgba(255, 106, 0, 0.45); border-radius: 8px; padding: 8px 16px; cursor: pointer;
}
.dim-wizard-fold {
  background: none; border: none; padding: 6px 0 2px; text-align: left; cursor: pointer; color: inherit; font: inherit; width: 100%;
}
.dim-wizard-serial-msg { min-height: 16px; font-size: 12px; color: #f9a; margin-bottom: 8px; }
`;

function injectCssOnce() {
  if (document.getElementById('dim-wizard-style')) return;
  const style = document.createElement('style');
  style.id = 'dim-wizard-style';
  style.textContent = CSS;
  document.head.appendChild(style);
}

// Kaleidohedra's dimensions (direct decision, 2026-10-08): 2D+ is Nets
// only, the way from flat pieces into 3D and the shear; 3D+ is every
// lattice and world the shear acts on. 1D and 4D-6D stay in Rhombiverse.
// Descriptions: 'wiz.dim.<id>'.
const DIMENSIONS = [
  { id: '2D', label: dimensionLabel('2D'), preview: () => netsCrossEdges() },
  { id: '3D', label: dimensionLabel('3D'), previewAction: 'tool:pieceType:rd' },
];
// Nets, previewed as the cube's cross.
function netsCrossEdges() {
  const out = [];
  const q = 0.42;
  const squares = [[0, 1.5], [0, 0.5], [0, -0.5], [0, -1.5], [-1, 0.5], [1, 0.5]];
  for (const [cx, cy] of squares) {
    const c = [[cx - 0.5, cy - 0.5], [cx + 0.5, cy - 0.5], [cx + 0.5, cy + 0.5], [cx - 0.5, cy + 0.5]].map(([x, y]) => [x * q * 1.6, y * q * 1.6, 0]);
    c.forEach((p, i) => out.push([p, c[(i + 1) % 4]]));
  }
  out.coin = true;
  return out;
}

// LATTICES_3D (wizard parity, 2026-09-24): direct decision -- "every
// piece listed under the lattice it inhabits", wireframes in the wizard,
// symbols on the wheels. Each lattice is a section header; each piece
// under it is its own row, dispatching the SAME action its wheel face
// already uses. Wireframes are NOT built here: render.js supplies each
// piece's edges from its own real placed geometry (createDimensionWizard's
// pieceEdges param -- the same geometry + EdgesGeometry pipeline Lattice
// View and Skeleton already draw with), so there's one geometry source. Every piece here is reachable on a wheel today (Hemi
// 3/4/Tri/Ring aren't -- they have store support but no UI entry -- so
// they're deliberately not listed). Row names "RD Dual" and "BCC
// Interstitial" reuse the code's own existing descriptions of those
// lattices; they are placeholders pending the user's own naming.
export const LATTICES_3D = [
  { key: 'roofFold', label: 'Euclid–Kepler–Pacioli Cell Network', pieces: [
    { label: 'Euclid–Kepler–Pacioli Cell Network', action: 'tool:roofFoldWorld' },
  ] },
  // Studies (direct decision, 2026-10-08): the EKP cell's exact constructions, a world of their own.
  { key: 'studies', label: 'Studies', pieces: [
    { label: 'Studies', action: 'tool:studiesWorld' },
  ] },
  // Stella–Jewel Lattice (direct request, 2026-10-08): Dragon Jewels and stella octangulas.
  { key: 'stellaJewel', label: 'Stella–Jewel Lattice', pieces: [
    { label: 'Stella–Jewel Lattice', action: 'tool:stellaJewelWorld' },
  ] },
  // Sunstar Lattice (direct request, 2026-10-08): dodecahedra and Dogstars.
  { key: 'sunstar', label: 'Sunstar Lattice', pieces: [
    { label: 'Sunstar Lattice', action: 'tool:sunstarWorld' },
  ] },
  { key: 'fcc', label: 'FCC', pieces: [
    { label: 'RD', action: 'tool:pieceType:rd' },
    { label: 'Hemi RD', action: 'tool:pieceType:halfrd' },
    { label: 'Hourglass', action: 'tool:pieceType:hourglass' },
    { label: 'RD Quarter', action: 'tool:pieceType:rdquarter' },
    { label: 'Cube', action: 'tool:pieceType:cube' },
    { label: 'Pyramid', action: 'tool:pieceType:pyramid' },
  ] },
  // DICTO FCC (direct request 2026-09-30): DICTO's blue-strut skewed RD
  // on its sheared FCC lattice, right after the FCC it shears.
  { key: 'dictofcc', label: 'DICTO FCC', pieces: [
    { label: 'DICTO RD', action: 'tool:pieceType:dictofcc' },
    { label: 'DICTO Blocks', action: 'tool:pieceType:dictoblock' },
  ] },
  { key: 'rdDual', label: 'RD Dual', pieces: [
    { label: 'CO', action: 'tool:cuboctaBuild' },
    { label: 'Octahedron', action: 'tool:pieceType:octahedron' },
  ] },
  { key: 'bcc', label: 'BCC', pieces: [
    { label: 'TO', action: 'tool:pieceType:to' },
  ] },
  { key: 'bccGaps', label: 'BCC Interstitial', pieces: [
    { label: 'Flattened Octahedron', action: 'tool:pieceType:ioct' },
    { label: 'Disphenoid', action: 'tool:pieceType:idis' },
  ] },
  { key: 'ed', label: 'ED', pieces: [
    { label: 'ED', action: 'tool:pieceType:elongdodeca' },
  ] },
  { key: 'hex', label: 'Hexagonal', pieces: [
    { label: 'Hex Prism', action: 'tool:pieceType:hexprism' },
  ] },
  { key: 'rhombohedral', label: 'Rhombohedral', pieces: [
    { label: 'Rhombohedra', action: 'tool:pieceType:rhombohedra' },
  ] },
  { key: 'pyrochlore', label: 'Pyrochlore (3D Kagome)', pieces: [
    { label: 'Truncated Tetrahedron', action: 'tool:pieceType:pyrochlore' },
  ] },
  { key: 'shells', label: 'Shells', pieces: [
    { label: 'Shells', action: 'tool:shellsWorld' },
  ] },
  { key: 'golden', label: 'Golden Rhombohedra', pieces: [
    { label: 'Golden Rhombohedra', action: 'tool:goldenWorld' },
  ] },
  { key: 'targets', label: 'Targets', pieces: [
    { label: 'Targets', action: 'tool:targetsWorld' },
  ] },
];

export function createDimensionWizard({ onSelectFamily, pieceEdges }) {
  injectCssOnce();

  // Rotating previews (wireframe-preview.js): each rendered screen
  // registers its canvases' edge sources here, mounts them after its
  // innerHTML lands, and every screen change / close disposes them so
  // the shared animation loop only ever ticks canvases actually shown.
  let previewSources = [];
  let previewDisposers = [];
  function previewSlot(getEdges) {
    previewSources.push(getEdges);
    return `<canvas class="dim-wizard-preview" data-preview="${previewSources.length - 1}"></canvas>`;
  }
  function resetPreviews() {
    previewDisposers.forEach((dispose) => dispose());
    previewDisposers = [];
    previewSources = [];
  }
  function mountPreviews() {
    bodyEl.querySelectorAll('canvas[data-preview]').forEach((canvas) => {
      previewDisposers.push(mountWireframePreview(canvas, previewSources[Number(canvas.dataset.preview)](), 40));
    });
  }

  const overlay = document.createElement('div');
  overlay.className = 'dim-wizard-overlay';
  overlay.innerHTML = `
    <div class="dim-wizard-card">
      <div class="dim-wizard-header"><span class="dim-wizard-title"></span><button type="button" class="dim-wizard-close">✕</button></div>
      <div class="dim-wizard-body"></div>
    </div>`;
  document.body.appendChild(overlay);
  const bodyEl = overlay.querySelector('.dim-wizard-body');
  const titleEl = overlay.querySelector('.dim-wizard-title');

  function showDimensions() {
    resetPreviews();
    const L = getSettings().language;
    titleEl.textContent = t('wiz.title', L);
    let grid = '';
    for (const dim of DIMENSIONS) {
      grid += `
        <button type="button" class="dim-wizard-card-btn" data-dim="${dim.id}">
          ${previewSlot(dim.previewAction ? () => pieceEdges(dim.previewAction) : dim.preview)}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${dim.label}</span>
            <span class="dim-wizard-desc">${t(`wiz.dim.${dim.id}`, L)}</span>
          </span>
        </button>`;
    }
    bodyEl.innerHTML = `<div class="dim-wizard-sub">${t('wiz.sub', L)}</div><div class="dim-wizard-grid">${grid}</div>`;
    mountPreviews();
    bodyEl.querySelectorAll('.dim-wizard-card-btn').forEach((el) => {
      el.addEventListener('click', () => {
        if (el.dataset.dim === '3D') showLattice3D();
        else showNets();
      });
    });
  }

  // 2D+ is Nets alone: straight in.
  function showNets() {
    close();
    onSelectFamily('2D', 'tool:netsWorld');
  }

  function showLatticeSections(dimension, lattices, edgesFor) {
    resetPreviews();
    const L = getSettings().language;
    const d = dimension.toLowerCase();
    let grid = '';
    for (const lat of lattices) {
      grid += `
        <div class="dim-wizard-section">
          <span class="dim-wizard-label">${lat.label}</span>
          <span class="dim-wizard-desc">${t(`wiz.${d}.${lat.key}`, L)}</span>
        </div>`;
      for (const piece of lat.pieces) {
        grid += `
        <button type="button" class="dim-wizard-card-btn dim-wizard-piece" data-action="${piece.action}">
          ${previewSlot(() => edgesFor(piece))}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${piece.label}</span>
          </span>
        </button>`;
      }
    }
    bodyEl.innerHTML = `
      <button type="button" class="dim-wizard-back">${t('wiz.back', L)}</button>
      <div class="dim-wizard-sub">${t(`wiz.${d}.sub`, L)}</div>
      <div class="dim-wizard-grid">${grid}</div>`;
    mountPreviews();
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', showDimensions);
    bodyEl.querySelectorAll('.dim-wizard-card-btn[data-action]').forEach((el) => {
      el.addEventListener('click', () => {
        close();
        onSelectFamily(dimension, el.dataset.action);
      });
    });
  }
  function showLattice3D() {
    showLatticeSections('3D', LATTICES_3D, (piece) => pieceEdges(piece.action));
  }

  overlay.querySelector('.dim-wizard-close').addEventListener('click', () => close());
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });

  function open() {
    showDimensions(); // always reset to the top-level dimension list on (re)open
    overlay.classList.add('open');
  }
  function close() {
    resetPreviews();
    overlay.classList.remove('open');
  }

  // Straight to one dimension's screen (the welcome screen's 3D+).
  function openDimension(dim) {
    overlay.classList.add('open');
    titleEl.textContent = t('wiz.title', getSettings().language); // the lattice screens keep the list's title
    if (dim === '3D') showLattice3D();
    else if (dim === '2D') showNets();
    else showDimensions();
  }

  return { open, openDimension, close, get isOpen() { return overlay.classList.contains('open'); } };
}
