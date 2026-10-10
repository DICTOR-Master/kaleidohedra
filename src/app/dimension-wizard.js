// Dimension-select wizard (2026-09-22): the app's real entry gate --
// force-opened once on every load (see render.js's init(), right after
// this module's factory is called) and reachable again any time via the
// Home wheel's "Change Dimension" face. Picks which dimension tier
// (2D/3D/4D/5D/6D) you're building in, then which lattice family within
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
// through i18n.js ('wiz.*' and 'cat.*'); lattice, piece and tile names
// stay English.
import { polytope4D, POLYTOPES_4D, SYMMETRIES_4D } from '../krp-core/src/polyhedra/polytopes4d.js';
import { FEDOROV_FIVE, PARALLELOHEDRON_VARIANTS, KALEIDOHEDRA_VERIFIED, REGULAR_NINE, SPACE_FILLING_PAIR_LIST } from '../krp-core/src/polyhedra/families.js';
import { BRIDGE_SECTIONS, BRIDGES_3D_IDS } from '../krp-core/src/polyhedra/bridges.js';
import { STELLATION_IDS, stellationInfo, stellatedSolidName } from '../krp-core/src/polyhedra/stellations/index.js';
import { ZOME_PARALLELOHEDRA_ADDITION_IDS, DICTO_SKEWED_ED_IDS } from '../krp-core/src/polyhedra/miscellaneous/zome-parallelohedra/index.js';
import { REGULAR_NINE_ADDITION_IDS } from '../krp-core/src/polyhedra/miscellaneous/regular-nine/index.js';
import { BAIN_PARALLELOHEDRA_ADDITION_IDS } from '../krp-core/src/polyhedra/miscellaneous/bain-parallelohedra/index.js';
import { tileOnEdge } from '../geometry-extensions/kaleidoscope.js';
import { embed } from '../geometry-extensions/trajectory-1d.js';
import { mountWireframePreview } from './wireframe-preview.js';
import { cellStructure, rotation4, matVec, project4, A4_FIRST } from '../geometry-extensions/lattice-4d.js';
import { START_LATTICE_ANGLE, LATTICE_PRIMITIVES, LATTICE_PRIMITIVE_IMPLS } from '../geometry-extensions/lattice-2d.js';
import { VALID_TRIPLES, unitTileVertices } from '../krp-core/src/geometry-extensions/growth.js';
import { PRISM_HEIGHT } from '../krp-core/src/geometry-extensions/quasicrystal.js';
import { loadCatalogue, findBySerial, pieceCount } from '../geometry-extensions/quasicrystal-catalogue.js';
import { t, tn, tFor } from './i18n.js';
import { polyShapeEdges, polyShapeName } from './poly-shapes.js';
import { FAMILY_META, familyIds, familiesFor, pairPartners } from '../krp-core/src/polyhedra/families.js';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { isConvex } from '../krp-core/src/assembly/faceRegistration.js';
import { favourites, recent, isFavourite, toggleFavourite } from './poly-prefs.js';
import { netEligible, mountNetViewer } from './net-viewer.js';
import { mountStarView, mountDuoprismView, mountRadialView } from './shape-views.js';
import { STAR_POLYHEDRON_IDS, STAR_POLYHEDRON_META, STAR_POLYHEDRA } from '../krp-core/src/polyhedra/starPolyhedra.js';
import { FOURD_CAPABLE_IDS } from '../krp-core/src/polyhedra/fourD.js';
import { FOUR_D_SHAPE_PARAMS, resolveParamsKey } from '../krp-core/src/polyhedra/radialProjection.js';
import { SITE, SITES, setActiveSite, activeSite, themeOf } from './site.js';
import { countDicto } from './analytics.js';
import { dimensionLabel } from './dimension-label.js';
import { getSettings } from './settings.js';

const CSS = `
.dim-wizard-overlay {
  display: none;
  position: fixed; inset: 0; z-index: 991;
  align-items: center; justify-content: center;
  background: rgba(5, 5, 10, 0.96);
  padding: 0;
  box-sizing: border-box;
}
.dim-wizard-overlay.open { display: flex; }
.dim-wizard-card {
  /* Full screen (DICTO, 2026-10-08), the list in a readable column. */
  width: 100%; height: 100%; max-height: none; box-sizing: border-box;
  overflow-y: auto; overscroll-behavior: contain;
  padding-left: max(16px, calc((100% - 640px) / 2)) !important;
  padding-right: max(16px, calc((100% - 640px) / 2)) !important;
  color: #ddd; font: var(--text-m)/1.5 var(--font-ui);
  background: rgba(15, 15, 25, 0.97);
  border: 0; border-radius: 0;
  padding-top: max(18px, env(safe-area-inset-top)); padding-bottom: 32px;
}
.dim-wizard-header {
  display: flex; align-items: center; justify-content: space-between;
  font: 800 var(--text-2xl) var(--font-ui); letter-spacing: 0.08em;
  color: var(--pale);
  margin-bottom: 4px;
}
.dim-wizard-close { background: none; border: none; color: var(--accent); cursor: pointer; font: var(--text-xl) var(--font-ui); min-width: var(--touch); min-height: var(--touch); }
/* DICTO: the three apps as an optional filter (DICTO 2026-10-09: off by default; tap one to show
   only its entries, tap it again for all). Wordmarks two-tone like everywhere else. */
.dicto-apps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 16px; }
.dicto-apps-caption { grid-column: 1 / -1; font-size: var(--text-s, 12px); color: var(--pale); opacity: 0.8; letter-spacing: 0.02em; }
/* The shape browser (D4): search at the top of Polyhedraverse's block; a shape's details card. */
.poly-search { margin: 4px 0 8px; }
.poly-search-input { width: 100%; box-sizing: border-box; min-height: var(--touch-compact, 36px); padding: 6px 10px; border-radius: var(--radius-s, 6px);
  background: rgba(0, 0, 0, 0.45); border: 1px solid rgba(255, 255, 255, 0.25); color: #eee; font: var(--text-m, 14px) var(--font-ui, sans-serif); }
.poly-search-results { display: flex; flex-direction: column; gap: 4px; margin-top: 6px; }
/* DICTO's own shapes turn in DICTOspheres gold (DICTO 2026-10-10: "I only wanted dicto shapes"). */
.dicto-gold { --wire: #e8c25a; --wire-rgb: 232, 194, 90; }
.poly-detail { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 12px; }
.poly-section { margin: 0 0 12px; }
.poly-section-title { font: 700 var(--text-s, 13px) var(--font-ui, sans-serif); color: var(--pale, #d8ffcc); border-bottom: 1px solid rgba(var(--accent-rgb, 94, 226, 51), 0.35); padding: 0 0 4px; margin: 0 0 8px; }
.poly-pair { grid-template-columns: 1fr auto 1fr; align-items: center; }
.poly-pair-plus { font: 700 18px var(--font-ui, sans-serif); color: var(--accent, #a9f795); }
.poly-credit { max-width: 380px; font: var(--text-xs, 12px)/1.45 var(--font-ui, sans-serif); color: var(--accent, #a9f795); text-align: center; }
.poly-credit b { color: #d946a8; }
.poly-star-modes { display: flex; gap: 6px; justify-content: center; }
.poly-star-modes button { background: none; border: 1px solid rgba(var(--accent-rgb, 94, 226, 51), 0.4); color: var(--accent, #a9f795); border-radius: 999px; padding: 4px 12px; font: var(--text-xs, 12px) var(--font-ui, sans-serif); cursor: pointer; }
.poly-star-modes button[aria-pressed="true"] { background: rgba(var(--accent-rgb, 94, 226, 51), 0.25); }
.poly-credit button { background: none; border: 0; padding: 0; color: inherit; text-decoration: underline; font: inherit; cursor: pointer; }
.poly-detail-preview { width: 200px; height: 200px; max-width: 100%; }
.poly-detail-name { font: 700 var(--text-l, 18px) var(--font-ui, sans-serif); color: var(--accent); text-align: center; }
.poly-detail-actions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.poly-detail-actions button, .poly-detail-pair { min-height: var(--touch-compact, 36px); padding: 4px 12px; border-radius: var(--radius-s, 6px); cursor: pointer;
  background: rgba(0, 0, 0, 0.45); border: 1px solid rgba(255, 255, 255, 0.25); color: var(--accent); font: var(--text-m, 14px) var(--font-ui, sans-serif); }
.poly-detail-build { border-color: var(--accent-strong) !important; background: rgba(var(--accent-rgb), 0.25) !important; color: #fff !important; }
.poly-detail-fav[aria-pressed="true"] { border-color: var(--accent-strong); }
.poly-detail-stats { display: grid; grid-template-columns: auto 1fr; gap: 4px 12px; margin: 4px 0 0; width: 100%; font: var(--text-s, 13px) var(--font-ui, sans-serif); color: #ccd; }
.poly-detail-stats dt { color: var(--pale); }
.poly-detail-stats dd { margin: 0; min-width: 0; }
.dim-wizard-body .poly-compare { display: grid !important; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px; align-items: start; }
.poly-compare .poly-detail-stats { grid-template-columns: 1fr; gap: 0 0; font-size: var(--text-xs, 12px); }
.poly-compare .poly-detail-stats dd { margin-bottom: 4px; }
.poly-compare-col button { min-height: var(--touch-compact, 36px); padding: 4px 12px; border-radius: var(--radius-s, 6px); cursor: pointer; border: 1px solid var(--accent-strong); background: rgba(var(--accent-rgb), 0.25); color: #fff; font: var(--text-s, 13px) var(--font-ui, sans-serif); }
.poly-compare-col { display: flex; flex-direction: column; align-items: center; gap: 6px; min-width: 0; }
.poly-compare-preview { width: 140px; height: 140px; max-width: 100%; aspect-ratio: 1; }
.poly-compare .poly-detail-name { font-size: var(--text-m, 15px); }
.poly-compare-shared { margin: 8px 4px; color: #ccd; font: var(--text-s, 13px) var(--font-ui, sans-serif); }
.poly-detail-netbox { width: 100%; display: flex; flex-direction: column; gap: 8px; align-items: center; }
.poly-detail-netbox[hidden] { display: none; }
.poly-detail-stage { width: 100%; height: 280px; border-radius: var(--radius-m, 10px); overflow: hidden; background: #0a0a10; }
.poly-detail-4dbox { width: 100%; display: flex; flex-direction: column; gap: 6px; }
.poly-detail-4dbox[hidden] { display: none; }
.net-stage { width: 100%; height: 300px; border-radius: var(--radius-m, 10px); overflow: hidden; background: #0a0a10; display: flex; align-items: center; justify-content: center; color: var(--pale); font: var(--text-s, 13px) var(--font-ui, sans-serif); }
.net-controls { display: flex; gap: 10px; align-items: center; width: 100%; flex-wrap: wrap; justify-content: center; color: var(--pale); font: var(--text-s, 13px) var(--font-ui, sans-serif); }
.net-controls[hidden], .net-note[hidden] { display: none; }
.net-controls input[type=range] { flex: 1; accent-color: var(--accent-strong); }
.net-controls button { min-height: var(--touch-compact, 36px); padding: 4px 12px; border-radius: var(--radius-s, 6px); cursor: pointer; background: rgba(0, 0, 0, 0.45); border: 1px solid rgba(255, 255, 255, 0.25); color: var(--accent); font: inherit; }
.net-download { border-color: var(--accent-strong) !important; background: rgba(var(--accent-rgb), 0.25) !important; color: #fff !important; }
.net-note { color: var(--pale); opacity: 0.8; font: var(--text-xs, 11px) var(--font-ui, sans-serif); text-align: center; }
.dicto-app {
  min-height: var(--touch); padding: 6px 4px; cursor: pointer; touch-action: manipulation;
  /* The whole name on one line at any width (POLYHEDRAVERSE is the longest). */
  font: 800 clamp(9px, 2.6vw, var(--text-m))/1.2 var(--font-ui); letter-spacing: 0.03em; white-space: nowrap;
  color: var(--app-pale); background: rgba(var(--app-rgb), 0.06);
  border: 1px solid rgba(var(--app-rgb), 0.45); border-radius: var(--radius-m);
}
.dicto-app span { color: var(--app); }
.dicto-app[aria-pressed="true"] { background: rgba(var(--app-rgb), 0.3); border: 2px solid var(--app); }
/* Each entry's app, in its colour. */
.dicto-tags { display: flex; flex-wrap: wrap; gap: 4px 8px; margin-top: 2px; }
.dicto-tag { font: 700 var(--text-xs) var(--font-ui); color: var(--app); white-space: nowrap; }
.dicto-tag::before { content: '● '; }
.dim-wizard-kind { font: 800 var(--text-s) var(--font-ui); letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin: 10px 0 0; }
/* The dimension buttons are plain (no app's colour); the open one's content sits under it. */
.dicto-dim { --accent-strong: #d8dce6; --accent-rgb: 200, 205, 220; border-color: rgba(200, 205, 220, 0.35); }
.dicto-dim[aria-expanded="true"] { background: rgba(200, 205, 220, 0.1); }
.dicto-dim-content { display: flex; flex-direction: column; margin: 4px 0 14px; }
/* An app's block: its name, then its entries, all in its colours. */
.dicto-block { display: flex; flex-direction: column; gap: 6px; padding: 10px 10px 12px; border-left: 3px solid var(--accent-strong); background: rgba(var(--accent-rgb), 0.05); border-radius: var(--radius-m); }
.dicto-block + .dicto-block { margin-top: 14px; }
/* DICTO's own work inside an app's block: DICTO's silver livery. */
.dicto-livery { display: flex; flex-direction: column; gap: 6px; padding: 8px 8px 10px; margin: 4px 0 6px; border: 1px solid rgba(var(--accent-rgb), 0.45); border-radius: var(--radius-m); background: rgba(var(--accent-rgb), 0.07); }
.dicto-livery-name { font: 800 var(--text-s) var(--font-ui); letter-spacing: 0.1em; color: var(--pale); }
.dicto-livery-name span { color: var(--accent-strong); }
.dicto-block-name { font: 800 var(--text-xl)/1.2 var(--font-ui); letter-spacing: 0.06em; color: var(--pale); }
.dicto-block-name span { color: var(--accent-strong); }
.dicto-block .dim-wizard-section .dim-wizard-label { color: var(--pale); }
.dim-wizard-back {
  background: none; border: none; color: var(--accent); cursor: pointer;
  font: var(--text-m) var(--font-ui); padding: 0; margin-bottom: 10px;
}
.dim-wizard-sub { color: #99a; font-size: var(--text-s); margin-bottom: 14px; }
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
  border: 1px solid rgba(var(--accent-rgb), 0.3);
  border-radius: var(--radius-m);
  padding: 8px 12px;
  color: #eee;
  cursor: pointer;
  text-align: left;
  width: 100%;
}
.dim-wizard-card-btn:hover { background: rgba(var(--accent-rgb), 0.1); border-color: rgba(var(--accent-rgb), 0.6); }
.dim-wizard-preview { width: 40px; height: 40px; flex: 0 0 auto; }
.dim-wizard-section { display: flex; flex-direction: column; gap: 2px; margin: 10px 0 2px; }
.dim-wizard-section:first-child { margin-top: 0; }
.dim-wizard-piece { margin-left: 14px; width: calc(100% - 14px); }
.dim-wizard-row-text { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.dim-wizard-label { font: 700 var(--text-m) var(--font-ui); color: #fff; }
.dim-wizard-desc { font-size: var(--text-xs); color: #9ab; line-height: 1.35; }
.dim-wizard-serial-row { display: flex; gap: 6px; margin-bottom: 4px; }
.dim-wizard-serial-row input {
  flex: 1; min-width: 0; font: var(--text-l) var(--font-ui); color: #eee;
  background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(var(--accent-rgb), 0.35); border-radius: var(--radius-m); padding: 8px 10px;
}
.dim-wizard-serial-row button {
  font: 600 var(--text-m) var(--font-ui); color: var(--accent); background: rgba(var(--accent-rgb), 0.12);
  border: 1px solid rgba(var(--accent-rgb), 0.45); border-radius: var(--radius-m); padding: 8px 16px; cursor: pointer;
}
.dim-wizard-fold {
  background: none; border: none; padding: 6px 0 2px; text-align: left; cursor: pointer; color: inherit; font: inherit; width: 100%;
}
.dim-wizard-serial-msg { min-height: 16px; font-size: var(--text-s); color: #f9a; margin-bottom: 8px; }
`;

function injectCssOnce() {
  if (document.getElementById('dim-wizard-style')) return;
  const style = document.createElement('style');
  style.id = 'dim-wizard-style';
  style.textContent = CSS;
  document.head.appendChild(style);
}

// 2D lattice tier (Phase 3): one generic wireframe builder for all 12
// (angle, primitive) combinations, reusing geometry-extensions/
// lattice-2d.js's own real tileVerts functions DIRECTLY (via
// LATTICE_PRIMITIVE_IMPLS) rather than re-deriving the same corner math
// a second time here -- same "real corner coordinates, not guessed"
// discipline the old Square/Hexagon/Triangle wireframes each separately
// re-implemented, now guaranteed to match the real placed geometry
// exactly (a single source of truth, not 2 independently-hand-written
// copies of the same construction that could silently drift apart).
function lattice2dEdges(combo) {
  // Flat outline only (the tile's top face), flagged `coin` so the
  // preview spins it like a coin -- edge-on and back -- instead of
  // tumbling a 3D prism (direct request 2026-09-25: 2D previews "should
  // be 2D rotating and disappearing into edge like spinning coins").
  const impl = LATTICE_PRIMITIVE_IMPLS[combo.primitiveId];
  const verts = impl.tileVerts(combo.angleDeg, 1, 1);
  const top = verts.slice(0, verts.length / 2).map(([x, y]) => [x, y, 0]);
  const edges = top.map((p, i) => [p, top[(i + 1) % top.length]]);
  edges.coin = true;
  return edges;
}

// DIMENSIONS: the dimension-select screen's own 5 cards (descriptions:
// 'wiz.dim.<id>').
const DIMENSIONS = [
  // Phase 6 (2026-09-23): 3 real primitives (Parallelogram/Triangle/
  // Hexagon), each its own real store -- picking one here (or from
  // LATTICE_FAMILIES_2D below) just sets a starting default; the ACTUAL
  // angle control (4 named NAMED_LATTICE_ANGLES) lives entirely in
  // render.js's own persistent on-screen toggle panel now, not here --
  // direct correction ("the toggle should work for groups of cells...
  // it just needs to be able to do for real"): angle used to be baked
  // into which of 12 separate (angle, primitive) stores was active,
  // which meant toggling angle silently swapped to an unrelated store
  // instead of reshaping the one you'd actually built. See
  // lattice2dSeedCell's own header in render.js for the full incident.
  // 1D, 2D and 3D show as 1D+, 2D+ and 3D+ (dimension-label.js; direct
  // request: "much of the mode is interacting with other dimensions");
  // their ids stay 1D, 2D, 3D.
  { id: '1D', label: dimensionLabel('1D'), preview: () => signalEdges() },
  { id: '2D', label: dimensionLabel('2D'), preview: () => lattice2dEdges({ primitiveId: LATTICE_PRIMITIVES[0].id, angleDeg: START_LATTICE_ANGLE.angleDeg }) },
  { id: '3D', label: dimensionLabel('3D'), previewAction: 'tool:pieceType:rd' },
  { id: '4D', label: '4D', preview: () => edges4D('cell24') },
  { id: '5D', label: '5D', preview: () => edges5D() },
  { id: '6D', label: '6D', preview: () => edges6D() },
];

// 6D thumbnail: a prolate golden rhombohedron, the same tile world-quasicrystal.js
// places (growth.js's unit tile). Edges join corners one step apart.
// 1D: a stretch of the Signal trajectory, • — • as segments along E(s).
function signalEdges() {
  const out = [];
  const pt = (s) => { const [x, y] = embed(s); return [x * 0.3, y * 0.3 - 1.05, 0]; };
  let s = 0;
  for (const u of [1, 3, 1]) {
    for (let k = 0; k < u * 4; k++) out.push([pt(s + k / 4), pt(s + (k + 1) / 4)]);
    s += u + 1;
  }
  out.coin = true;
  return out;
}
// Construct: the square, its four sides of four cells.
function constructEdges() {
  const out = [];
  const n = 4, k = 2 / n;
  const pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
  pts.forEach((p, i) => {
    const q = pts[(i + 1) % 4];
    for (let a = 0; a < n; a++) {
      const f = (t) => [p[0] + ((q[0] - p[0]) * t) / 2, p[1] + ((q[1] - p[1]) * t) / 2, 0];
      out.push([f(a * k * 0.999 + 0.02), f((a + 1) * k - 0.02)]);
    }
  });
  out.coin = true;
  return out;
}
// Construct · Kagome: its star, two triangles through a hexagon.
function kagomeStarEdges() {
  const out = [];
  const r = 1.1;
  for (const rot of [Math.PI / 2, -Math.PI / 2]) {
    const pts = [0, 1, 2].map((i) => { const a = rot + (i * 2 * Math.PI) / 3; return [r * Math.cos(a), r * Math.sin(a), 0]; });
    pts.forEach((p, i) => out.push([p, pts[(i + 1) % 3]]));
  }
  out.coin = true;
  return out;
}
// Construct · RD: the RD's own rhombus (70.53°).
function rdRhombusEdges() {
  const a = Math.acos(1 / 3), L = 1.25;
  const u = [0, L, 0], v = [L * Math.sin(a), L * Math.cos(a), 0];
  const p0 = [-(u[0] + v[0]) / 2, -(u[1] + v[1]) / 2, 0];
  const pts = [p0, [p0[0] + u[0], p0[1] + u[1], 0], [p0[0] + u[0] + v[0], p0[1] + u[1] + v[1], 0], [p0[0] + v[0], p0[1] + v[1], 0]];
  const out = pts.map((p, i) => [p, pts[(i + 1) % 4]]);
  out.coin = true;
  return out;
}
// 1D's worlds: Signal, and Construct's families (direct decision,
// 2026-09-29: "Wizard cards").
const FAMILIES_1D = [
  { id: 'signal', label: 'Signal', action: 'tool:signalWorld', preview: signalEdges },
  { id: 'construct', label: 'Construct · Square', action: 'tool:constructWorld:square', preview: constructEdges },
  { id: 'constructKagome', label: 'Construct · Kagome', action: 'tool:constructWorld:kagome', preview: kagomeStarEdges },
  { id: 'constructRd', label: 'Construct · RD', action: 'tool:constructWorld:rd', preview: rdRhombusEdges },
];

function edges6D() {
  const v = unitTileVertices(VALID_TRIPLES.find((t) => t.type === 'acute').dirs);
  const c = [0, 1, 2].map((x) => v.reduce((s, p) => s + p[x], 0) / 8);
  const p = v.map((q) => q.map((x, i) => x - c[i]));
  const out = [];
  for (let a = 0; a < 8; a++) for (const bit of [1, 2, 4]) if (!(a & bit)) out.push([p[a], p[a | bit]]);
  return out;
}

// 5D thumbnail: a thick Penrose rhombus prism (72 degrees, edge 1,
// height PRISM_HEIGHT), the piece world-quasicrystal.js places.
function edges5D() {
  const a = (2 * Math.PI) / 5;
  const e1 = [1, 0, 0], e2 = [Math.cos(a), 0, Math.sin(a)], up = [0, PRISM_HEIGHT, 0];
  const v = [];
  for (const i of [0, 1]) for (const j of [0, 1]) for (const k of [0, 1]) v.push([0, 1, 2].map((x) => i * e1[x] + j * e2[x] + k * up[x]));
  const c = [0, 1, 2].map((x) => v.reduce((s, p) => s + p[x], 0) / 8);
  const p = v.map((q) => q.map((x, i) => x - c[i]));
  const out = [];
  for (let m = 0; m < 8; m++) for (const bit of [1, 2, 4]) if (!(m & bit)) out.push([p[m], p[m | bit]]);
  return out;
}

// LATTICE_FAMILIES_2D: 2D's own lattice-family screen. Same "reuse the
// existing real action, one tool one doorway" reasoning as
// LATTICES_3D below. Phase 6: one row per LATTICE_PRIMITIVES
// entry (3, not 12) -- picking one here just sets which primitive
// starts active; its own angle defaults to START_LATTICE_ANGLE
// (Triangular) and from there is controlled entirely by render.js's own
// persistent toggle panel, not by anything on this screen. Action is
// 'tool:pieceType:lattice2d:<primitiveId>', matching core/build.js's
// own `lattice2d` param and render.js's dimensionAllowsMesh's own
// 'lattice2d:' prefix check exactly.
const LATTICE_FAMILIES_2D = [
  ...LATTICE_PRIMITIVES.map((primitive) => ({
    id: primitive.id,
    label: primitive.label,
    action: `tool:pieceType:lattice2d:${primitive.id}`,
    preview: () => lattice2dEdges({ primitiveId: primitive.id, angleDeg: START_LATTICE_ANGLE.angleDeg }),
  })),
  // Kaleidoscope, a 2D world of its own: previewed as the star of five
  // thick rhombi it opens with (5 mirrors reflecting the first one).
  { id: 'kaleido', label: 'Kaleidoscope', action: 'tool:kaleidoWorld', preview: kaleidoStarEdges },
  // Nets, 2D to 3D: previewed as the cube's cross.
  { id: 'nets', label: 'Nets', action: 'tool:netsWorld', preview: netsCrossEdges },
];
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
function kaleidoStarEdges() {
  const edges = [];
  for (let j = 0; j < 5; j++) {
    const v = tileOnEdge('thick', [0, 0], [Math.cos((2 * Math.PI * j) / 5) * 0.6, Math.sin((2 * Math.PI * j) / 5) * 0.6]);
    v.forEach((p, i) => { const q = v[(i + 1) % v.length]; edges.push([[p[0], p[1], 0], [q[0], q[1], 0]]); });
  }
  edges.coin = true;
  return edges;
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
  { key: 'roofFold', label: 'Euclid–Kepler–Pacioli Cell Network (EKP)', pieces: [
    { label: 'Euclid–Kepler–Pacioli Cell Network (EKP)', action: 'tool:roofFoldWorld' },
  ] },
  // New work near the top (direct request, 2026-10-08: "put new originalish work close to top of
  // App wizards"), right after the EKP cell they grow from (ported from Kaleidohedra).
  // Sunstar Lattice: dodecahedra and the Dogstars in their holes.
  { key: 'sunstar', label: 'Sunstar Lattice', pieces: [
    { label: 'Sunstar Lattice', action: 'tool:sunstarWorld' },
  ] },
  // Stella–Jewel Lattice: DICTO Jewels and stella octangulas.
  { key: 'stellaJewel', label: 'Stella–Jewel Lattice', pieces: [
    { label: 'Stella–Jewel Lattice', action: 'tool:stellaJewelWorld' },
  ] },
  { key: 'fcc', label: 'FCC · rhombic dodecahedra', pieces: [
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
  { key: 'rdDual', label: 'RD Dual · cuboctahedra and octahedra', pieces: [
    { label: 'CO', action: 'tool:cuboctaBuild' },
    { label: 'Octahedron', action: 'tool:pieceType:octahedron' },
  ] },
  { key: 'bcc', label: 'BCC · truncated octahedra', pieces: [
    { label: 'TO', action: 'tool:pieceType:to' },
  ] },
  { key: 'bccGaps', label: 'BCC Interstitial · the gaps between truncated octahedra', pieces: [
    { label: 'Flattened Octahedron', action: 'tool:pieceType:ioct' },
    { label: 'Disphenoid', action: 'tool:pieceType:idis' },
  ] },
  { key: 'ed', label: 'ED · elongated dodecahedron', pieces: [
    { label: 'ED', action: 'tool:pieceType:elongdodeca' },
  ] },
  { key: 'hex', label: 'Hexagonal', pieces: [
    { label: 'Hex Prism', action: 'tool:pieceType:hexprism' },
    // DICTO Hex Prism (queued 2026-10-01): DICTO's leaning prism, each layer slid along its lean.
    { label: 'DICTO Hex Prism', action: 'tool:pieceType:dictohex' },
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
];

// 4D thumbnails (direct decision, option B): each cell's 4D edges turned
// by a slight oblique XW 20 / YW 15 / ZW 10 degree rotation, then a
// parallel shadow into 3D (vertex-first collapses the 24-cell and
// tesseract to the same RD outline; cell-first hides the 4D-ness), then
// the same rotating preview as every other card. Real geometry from
// lattice-4d.js (verify:4d), nothing hand-drawn.
const OBLIQUE_4D = rotation4({ xw: 20 * Math.PI / 180, yw: 15 * Math.PI / 180, zw: 10 * Math.PI / 180 });
const FIRST_4D_CENTER = { tesseract: [0, 0, 0, 0], cell24: [0, 0, 0, 0], cell16: [0.5, 0.5, 0.5, 0.5], ...A4_FIRST };
function edges4D(kind) {
  const c = FIRST_4D_CENTER[kind];
  const s = cellStructure(kind, c);
  const p = s.offsets.map((o) => project4(matVec(OBLIQUE_4D, o), false));
  return s.edges.map(([i, j]) => [p[i], p[j]]);
}

// LATTICES_4D: the three 4D worlds (direct decision: wizard = three
// worlds, the 4D wheel = six cells).
export const LATTICES_4D = [
  { key: 'z4', label: 'Z4 (Hypercubic)', pieces: [
    { label: 'Tesseract', action: 'tool:pieceType:tesseract', preview: () => edges4D('tesseract') },
  ] },
  { key: 'd4', label: 'D4 · the 24-cell and 16-cell', pieces: [
    { label: '24-cell', action: 'tool:pieceType:cell24', preview: () => edges4D('cell24') },
    { label: '16-cell', action: 'tool:pieceType:cell16', preview: () => edges4D('cell16') },
  ] },
  { key: 'a4', label: 'Hyper-pyrochlore (4D Kagome)', pieces: [
    { label: 'Truncated 5-cell', action: 'tool:pieceType:a4trunc', preview: () => edges4D('a4trunc') },
    { label: 'Bitruncated 5-cell', action: 'tool:pieceType:a4bitrunc', preview: () => edges4D('a4bitrunc') },
    { label: '5-cell', action: 'tool:pieceType:a4cell5', preview: () => edges4D('a4cell5') },
  ] },
];

// ---- DICTO by dimension (DICTO 2026-10-09, PLAN-DICTO-DIMENSIONS.md) ----
// DICTO opens on the dimensions; inside one, every app's entries are listed together, grouped by
// kind and tagged with their app, so you never land in one app with little choice. Choosing an entry
// enters that app's space. Worlds Kaleidohedra and Rhombiverse share are listed once, in
// Kaleidohedra's; each app's lattices are listed once per app.
const SHARED_WORLDS = ['roofFold', 'sunstar', 'stellaJewel', 'shells', 'golden'];
const K_WORLDS = [
  // DICTO Icosa (DICTO 2026-10-10: "own Icosa world", reached only through the DICTO worlds; newest first)
  { key: 'icosa', label: 'DICTO Icosa', pieces: [{ label: 'DICTO Icosa', action: 'tool:icosaWorld' }] },
  { key: 'roofFold', label: 'Euclid–Kepler–Pacioli Cell Network (EKP)', pieces: [{ label: 'Euclid–Kepler–Pacioli Cell Network (EKP)', action: 'tool:roofFoldWorld' }] },
  // Each world's arrangements as its pieces, one tap each (DICTO 2026-10-09: separate access, no
  // drop-downs; listed under their parent so it shows what belongs to what).
  ...[['stellaJewel', 'Checkerboard', 'DJ'], ['sunstar', 'Dodecahedra and Dogstars', 'DODECA']].map(([world, base, shape]) => {
    const lat = LATTICES_3D.find((l) => l.key === world);
    return { ...lat, pieces: [
      { ...lat.pieces[0], label: base },
      ...[['tetra', 'Tetrahedral clusters', 'TETRAHEDRAL'], ['octa', 'Octahedral clusters', 'OCTAHEDRAL'], ['octet', 'Octet network', 'OCTAHEDRAL'], ['kagome', 'Kagome network', 'TETRAHEDRAL']]
        .map(([mode, label, form]) => ({ label, action: `tool:${world}World:${mode}`, preview: () => polyShapeEdges(`${shape}_${form}_CLUSTER`) })),
      ...(world === 'stellaJewel' ? [{ label: 'DICTO Hexa diamond network', action: 'tool:stellaJewelWorld:hexa', preview: () => polyShapeEdges('DICTO_HEXA') },
        { label: 'DICTO Hexa and Hexa-Key checkerboard', action: 'tool:stellaJewelWorld:hexaKey', preview: () => polyShapeEdges('DICTO_HEXA_KEY') }] : []),
      // The Kagome hulls (DISCOVERIES #17); previews: the hull's cell centres, nearest neighbours joined.
      ...[['hullOcta', 'Octahedral Kagome', 'octa6'], ['hullRhombo', 'Rhombohedral Kagome', 'rhombo8'], ['hullCuboHollow', 'Cuboctahedral Kagome (hollow)', 'cubocta12'],
        ['hullCuboSolid', 'Cuboctahedral Kagome (solid)', 'cubocta13'], ['hullCube', 'Cubic Kagome', 'cube14'], ['hullRd', 'Rhombic dodecahedral Kagome', 'rd33']]
        .map(([mode, label, id]) => ({ label, action: `tool:${world}World:${mode}`, preview: () => hullPreview(id) })),
    ] };
  }),
  { key: 'studies', label: 'Studies', pieces: [{ label: 'Studies', action: 'tool:studiesWorld' }] },
  { key: 'targets', label: 'Targets', pieces: [{ label: 'Targets', action: 'tool:targetsWorld' }] },
  ...['shells', 'golden'].map((k) => LATTICES_3D.find((l) => l.key === k)),
];
// A Kagome hull's preview: its even cells' centres, each joined to its nearest neighbours.
const HULL_EVEN = {
  octa6: [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
  rhombo8: [[0, 0, 0], [1, 1, 0], [1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 2, 1], [1, 1, 2], [2, 2, 2]],
  cubocta12: [[1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0], [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1], [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]],
  cube14: [[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1], [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
};
HULL_EVEN.cubocta13 = [[0, 0, 0], ...HULL_EVEN.cubocta12];
HULL_EVEN.rd33 = [...HULL_EVEN.cubocta13, [2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0], [0, 0, 2], [0, 0, -2]];
function hullPreview(id) {
  const P = HULL_EVEN[id], c = P[0].map((_, i) => P.reduce((t, p) => t + p[i], 0) / P.length), Q = P.map((p) => p.map((v, i) => v - c[i]));
  const d = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
  let min = Infinity;
  for (let i = 0; i < Q.length; i++) for (let j = i + 1; j < Q.length; j++) min = Math.min(min, d(Q[i], Q[j]));
  const edges = [];
  for (let i = 0; i < Q.length; i++) for (let j = i + 1; j < Q.length; j++) if (d(Q[i], Q[j]) < min * 1.01) edges.push([Q[i], Q[j]]);
  return edges;
}
const K_LATTICES = LATTICES_3D.filter((l) => !SHARED_WORLDS.includes(l.key))
  .map((l) => (l.key === 'hex' ? { ...l, pieces: l.pieces.filter((pc) => pc.action === 'tool:pieceType:hexprism') } : l));
const R_LATTICES = LATTICES_3D.filter((l) => !SHARED_WORLDS.includes(l.key));
// Polyhedraverse's families: Platonic at the top as usual (DICTO 2026-10-09: "anyone wanting to
// start at Platonic solids can do so as normal from the top of the green list"), DICTO's own pieces
// above them in DICTO's livery; 4D Polytopes waits for D5.
const POLY_FAMILIES = ['PLATONIC', 'ARCHIMEDEAN', 'CATALAN', 'JOHNSON', 'DELTAHEDRA', 'PRISMS', 'ANTIPRISMS', 'STELLATIONS', 'PARALLELOHEDRA', 'SPACE_FILLING_PAIRS', 'BRIDGES_3D', 'APERIODIC', 'MISCELLANEOUS'];
// DICTO's own work, shown in DICTO's livery (silver) at the top of its app's block (DICTO 2026-10-09);
// it still opens in its app. Lattices and worlds by key, single pieces by action, and DICTO's
// Polyhedraverse pieces gathered from across its families.
const DICTO_WORK = new Set(['icosa', 'roofFold', 'studies', 'stellaJewel', 'sunstar', 'targets', 'shells', 'golden', 'dictofcc', 'djTetra', 'djOcta', 'djOctet', 'djKagome', 'ssTetra', 'ssOcta', 'ssOctet', 'ssKagome', 'djHexa']);
const DICTO_PIECE_ACTIONS = new Set(['tool:pieceType:dictohex']);
// DICTO's block, findings first and tools last (copy audit, DICTO 2026-10-09).
const DICTO_ORDER = ['icosa', 'roofFold', 'stellaJewel', 'sunstar', 'studies', 'targets', 'dictofcc', 'hex', 'shells', 'golden'];
const dictoRank = (e) => { const i = DICTO_ORDER.indexOf(e.lat?.key); return i < 0 ? DICTO_ORDER.length : i; };
const DICTO_POLY = { key: 'DICTO_PIECES', label: "DICTO's pieces", ids: ['DICTO_EDGE_ROOF', 'DICTO_DODECA13', 'DICTO_DODECA13_STAR', 'DICTO_DODECA13_UNIT', 'DICTO_DODECA13_WEDGE', 'DICTO_DODECA13_NEEDLE', 'DICTO_HEXA', 'DICTO_HEXA_KEY', 'DICTO_HEXA_RHOMBO_CLUSTER', 'DICTO_HEXA_DIAMOND_CLUSTER', 'DICTO_HEXA_TRIMMED_JEWEL', 'DICTO_HEXA_ROOF', 'DICTO_SKEWED_RD', 'DICTO_SQUARE_FACED_BLOCK', 'DICTO_ALL_RHOMBUS_BLOCK', 'DICTO_FLATTENED_RHOMBOHEDRON', 'DICTO_LEANING_HEX_PRISM', 'DICTO_SKEWED_ED_16', 'DICTO_SKEWED_ED_18', 'DRAGON_JEWEL', 'DJ_TETRAHEDRAL_CLUSTER', 'DJ_OCTAHEDRAL_CLUSTER', 'DODECA_TETRAHEDRAL_CLUSTER', 'DODECA_OCTAHEDRAL_CLUSTER'] };
// The shape a face was tapped on, while picking: its space-filling partners come first (as the old site).
let partnerIds = [];
const gold = (id) => (DICTO_POLY.ids.includes(id) ? ' dicto-gold' : '');
const polyIds = (key) => (key === 'PARTNERS' ? partnerIds : key === DICTO_POLY.key ? DICTO_POLY.ids.filter((id) => polyShapeName(id) !== id) : key === 'FAVOURITES' ? favourites() : key === 'RECENT' ? recent() : key === 'STARS' ? STAR_POLYHEDRON_IDS : familyIds(key));
const polyLabel = (key) => (key === 'PARTNERS' ? t('poly.d.pairs', getSettings().language) : key === DICTO_POLY.key ? DICTO_POLY.label : key === 'FAVOURITES' ? t('wiz.poly.favourites', getSettings().language) : key === 'RECENT' ? t('wiz.poly.recent', getSettings().language) : key === 'STARS' ? 'Kepler–Poinsot' : FAMILY_META[key].label);
// ---- the shape browser (step D4, DICTO 2026-10-09: inside DICTO) ----
// A shape's faces by kind, each { kind, count, regular }: what its details list and search reads.
const faceKindCache = new Map();
function faceKindsOf(id) {
  if (faceKindCache.has(id)) return faceKindCache.get(id);
  const s = POLYHEDRA[id] ?? STAR_POLYHEDRA[id], V = s.vertices, kinds = new Map();
  const d = (a, b) => Math.hypot(...V[a].map((x, i) => x - V[b][i]));
  const ang = (a, b, c) => { const u = V[a].map((x, i) => x - V[b][i]), w = V[c].map((x, i) => x - V[b][i]); return Math.acos(Math.max(-1, Math.min(1, (u[0] * w[0] + u[1] * w[1] + u[2] * w[2]) / (Math.hypot(...u) * Math.hypot(...w))))); };
  for (const f of s.faces) {
    const n = f.length, sides = f.map((v, i) => d(v, f[(i + 1) % n])), angles = f.map((v, i) => ang(f[(i + n - 1) % n], v, f[(i + 1) % n]));
    const eqS = sides.every((x) => Math.abs(x - sides[0]) < 1e-6 * sides[0]), eqA = angles.every((x) => Math.abs(x - angles[0]) < 1e-6);
    // a regular five-sided face whose corners turn by 36° is a pentagram (the star polyhedra's)
    let kind = n === 3 ? 'triangle' : n === 5 ? (eqA && Math.abs(angles[0] - Math.PI / 5) < 1e-6 ? 'pentagram' : 'pentagon') : n === 6 ? 'hexagon' : n === 8 ? 'octagon' : n === 10 ? 'decagon' : n === 4 ? null : 'polygon';
    if (n === 4) kind = eqS && eqA ? 'square' : eqS ? 'rhombus' : eqA ? 'rectangle' : (Math.abs(sides[0] - sides[1]) < 1e-6 && Math.abs(sides[2] - sides[3]) < 1e-6) || (Math.abs(sides[1] - sides[2]) < 1e-6 && Math.abs(sides[3] - sides[0]) < 1e-6) ? 'kite' : 'quadrilateral';
    const regular = n !== 4 && eqS && eqA, k = `${kind}|${regular}|${n}`;
    kinds.set(k, { kind, regular, n, count: (kinds.get(k)?.count ?? 0) + 1 });
  }
  const out = [...kinds.values()].sort((a, b) => b.count - a.count);
  faceKindCache.set(id, out);
  return out;
}
const faceWord = (k, L) => (k.kind === 'polygon' ? t('poly.face.polygon', L, { n: k.n }) : t(`poly.face.${k.kind}`, L));
// Every shape the browser knows: DICTO's, then each family's.
const browsable = () => [...new Set([...DICTO_POLY.ids, ...POLY_FAMILIES.flatMap((k) => familyIds(k)), ...STAR_POLYHEDRON_IDS])].filter((id) => (POLYHEDRA[id] || STAR_POLYHEDRA[id]) && polyShapeName(id) !== id);
// Search: every word must match the name, a family, a face kind (in this language or English) or,
// as a number, the face count.
function searchShapes(q, L) {
  const words = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  return browsable().filter((id) => {
    const hay = [polyShapeName(id), ...(STAR_POLYHEDRA[id] ? ['Kepler–Poinsot', 'star'] : familiesFor(id).map((f) => FAMILY_META[f]?.label ?? f)),
      ...faceKindsOf(id).flatMap((k) => [faceWord(k, L), faceWord(k, 'en'), k.kind])].join(' ').toLowerCase().replaceAll('_', ' ');
    const faces = (POLYHEDRA[id] ?? STAR_POLYHEDRA[id]).faces.length;
    return words.every((w) => (/^\d+$/.test(w) ? faces === Number(w) : hay.includes(w)));
  }).slice(0, 60);
}
// A lattice's DICTO pieces split off as their own (DICTO) entry, the rest stay the app's.
function splitDicto(e) {
  if (DICTO_WORK.has(e.lat.key)) return [{ ...e, dicto: true }];
  const mine = e.lat.pieces.filter((pc) => DICTO_PIECE_ACTIONS.has(pc.action));
  if (!mine.length) return [e];
  const rest = e.lat.pieces.filter((pc) => !DICTO_PIECE_ACTIONS.has(pc.action));
  return [{ ...e, dicto: true, lat: { ...e.lat, pieces: mine } }, ...(rest.length ? [{ ...e, lat: { ...e.lat, pieces: rest } }] : [])];
}
const APP_ORDER = ['kaleidohedra', 'rhombiverse', 'polyhedraverse'];

// Every entry of a dimension: { app, kind, ... }. kind: 'lattice' and 'world' (a lattice section with
// its pieces), 'family' (a 1D/2D world or tile row), 'shapes' (a Polyhedraverse family).
function dimensionEntries(dim) {
  const R = 'rhombiverse', K = 'kaleidohedra', P = 'polyhedraverse';
  // 1D+ and 2D+ are DICTO's own (DICTO 2026-10-09: "they don't belong to anyone", the easier way in).
  if (dim === '1D') return FAMILIES_1D.map((fam) => ({ app: 'dicto', kind: 'family', fam }));
  if (dim === '2D') return LATTICE_FAMILIES_2D.map((fam) => ({ app: 'dicto', kind: 'family', fam }));
  if (dim === '3D') return [
    ...K_LATTICES.map((lat) => ({ app: K, kind: 'lattice', lat })),
    ...R_LATTICES.map((lat) => ({ app: R, kind: 'lattice', lat })),
    ...K_WORLDS.map((lat) => ({ app: K, kind: 'world', lat })),
  ].flatMap(splitDicto)
    // DICTO's own lattices and worlds (DICTO 2026-10-09: "my lattices available through Rhombiverse"):
    // their own silver DICTO block, first, opening in the door's app (dictoOpen).
    .map((e) => (e.dicto ? { ...e, app: 'dicto', dicto: false, lattice3d: true } : e)).concat(
    { app: P, kind: 'search' },
    { app: P, kind: 'shapes', key: 'FAVOURITES' },
    { app: P, kind: 'shapes', key: 'RECENT' },
    // DICTO's pieces sit at the top of the DICTO block (DICTO 2026-10-11: they were six screens down)
    { app: 'dicto', kind: 'shapes', key: DICTO_POLY.key },
    POLY_FAMILIES.filter((key) => familyIds(key).length).map((key) => ({ app: P, kind: 'shapes', key })),
    { app: P, kind: 'shapes', key: 'STARS' },
  );
  if (dim === '4D') return [...LATTICES_4D.map((lat) => ({ app: R, kind: 'lattice', lat })), { app: P, kind: 'shapes', key: 'POLYTOPES_4D' }];
  return [{ app: R, kind: 'catalogue' }]; // 5D, 6D
}
// Where a DICTO lattice opens: the app whose door you came in by (Rhombiverse: its colours, no Shear;
// Kaleidohedra: with the Shear); the DICTO Hex Prism always in Rhombiverse, whose hexagonal lattice
// has it.
// From Polyhedraverse's door (no lattices of its own) they open in Rhombiverse's space.
const dictoOpen = (action) => (action === 'tool:pieceType:dictohex' || SITE === 'polyhedraverse' ? 'rhombiverse' : SITE);
const appsOf = (dim) => [...new Set(dimensionEntries(dim).map((e) => e.app))];
// DICTO's own entries show whatever app the filter picks.
const passes = (app, filter) => !filter || app === filter || app === 'dicto';
// The kinds inside an app's block, new work first.
const KINDS = [['search', null], ['world', 'wiz.kind.worlds'], ['lattice', 'wiz.kind.lattices'], ['shapes', 'wiz.kind.shapes'], ['family', 'wiz.kind.worlds']];

export function createDimensionWizard({ onSelectFamily, pieceEdges }) {
  injectCssOnce();

  // Rotating previews (wireframe-preview.js): each rendered screen registers its canvases' edge
  // sources here; a preview turns only while its row is on screen (the 3D+ list is long).
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
    const root = overlay.querySelector('.dim-wizard-card');
    const live = new Map();
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) {
        const c = en.target;
        if (en.isIntersecting && !live.has(c)) live.set(c, mountWireframePreview(c, previewSources[Number(c.dataset.preview)](), 40));
        else if (!en.isIntersecting && live.has(c)) { live.get(c)(); live.delete(c); }
      }
    }, { root, rootMargin: '120px' });
    bodyEl.querySelectorAll('canvas[data-preview]').forEach((c) => io.observe(c));
    previewDisposers.push(() => { io.disconnect(); live.forEach((d) => d()); live.clear(); });
  }

  const overlay = document.createElement('div');
  overlay.className = 'dim-wizard-overlay';
  overlay.innerHTML = `
    <div class="dim-wizard-card">
      <div class="dim-wizard-header"><span class="dim-wizard-title"></span><button type="button" class="dim-wizard-close">✕</button></div>
      <div class="dicto-apps"></div>
      <div class="dim-wizard-body"></div>
    </div>`;
  document.body.appendChild(overlay);
  const bodyEl = overlay.querySelector('.dim-wizard-body');
  const titleEl = overlay.querySelector('.dim-wizard-title');

  // ---- the door, the filter, the colours ----
  // The door (the address you came in by) sets the colours and puts its own app's entries first; the
  // filter, off by default, shows one app's entries only (and wears its colours).
  let filter = null;
  let current = showDimensions; // the screen shown, redrawn when the filter changes
  const wordmark = (site) => { const [a, b] = SITES[site].wordmark; return `${a}<span>${b}</span>`; };
  const appStyle = (a) => { const th = themeOf(a); return `--app: ${th.strong}; --app-rgb: ${th.pieceRgb}; --app-pale: ${th.pale}`; };
  // An app's block wears its colours: rows, outlines and turning previews (wireframe-preview.js reads them).
  const blockStyle = (a) => { const th = themeOf(a); return `--pale: ${th.pale}; --accent: ${th.accent}; --accent-rgb: ${th.pieceRgb}; --accent-strong: ${th.strong}`; };
  const tag = (a) => `<span class="dicto-tag" style="${appStyle(a)}">${SITES[a].name}</span>`;
  // DICTO's own block first, then the door's app, then the others.
  const rank = (app) => (app === 'dicto' ? 0 : app === SITE ? 1 : app === 'polyhedraverse' ? 3 : 2);
  const doorFirst = (list) => [...list].sort((x, y) => rank(x.app) - rank(y.app));
  const shownEntries = (dim) => doorFirst(dimensionEntries(dim).filter((e) => passes(e.app, filter)));
  function paintApps() {
    // The colours of the space you are in (copy audit 2026-10-09: green inside Polyhedraverse), or the filter's.
    const th = themeOf(filter ?? activeSite());
    for (const [k, v] of [['--pale', th.pale], ['--accent', th.accent], ['--accent-rgb', th.accentRgb], ['--accent-strong', th.strong]]) overlay.style.setProperty(k, v);
    overlay.dataset.door = SITE;
    const L = getSettings().language;
    const box = overlay.querySelector('.dicto-apps');
    box.setAttribute('aria-label', t('wiz.filter', L));
    box.innerHTML = `<div class="dicto-apps-caption">${t('wiz.filter', L)}</div>` + APP_ORDER.map((a) => `<button type="button" class="dicto-app" data-app="${a}" aria-pressed="${filter === a}" style="${appStyle(a)}">${wordmark(a)}</button>`).join('');
    box.querySelectorAll('.dicto-app').forEach((b) => b.addEventListener('click', () => {
      filter = filter === b.dataset.app ? null : b.dataset.app;
      paintApps();
      current();
    }));
  }
  // Choosing an entry enters its app's space (its colours, its tools), then opens it.
  const choose = (dim, action, app) => { close(); setActiveSite(app); onSelectFamily(dim, action); };
  const back = (L) => `<button type="button" class="dim-wizard-back">${t('wiz.back', L)}</button>`;

  // ---- DICTO: the dimensions, one open in place ----
  // (DICTO 2026-10-09) Plain dimension buttons; the open one shows its content right under it, in app
  // blocks, the door's app first. 3D+ is open to start with; tap another to open it instead, tap the
  // open one to close it. 5D and 6D open their catalogues.
  let openDim = '3D';
  function showDimensions(scrollTo = null) {
    current = () => showDimensions();
    resetPreviews();
    const L = getSettings().language;
    titleEl.textContent = 'DICTO';
    let grid = '';
    for (const dim of DIMENSIONS) {
      const apps = appsOf(dim.id).filter((a) => passes(a, filter));
      if (!apps.length) continue; // filtered to an app with nothing here
      const isOpen = openDim === dim.id && !['5D', '6D'].includes(dim.id);
      const desc = filter && apps.includes(filter) ? tFor(filter, `wiz.dim.${dim.id}`, L) : t(['2D', '3D'].includes(dim.id) ? `wiz.dimAll.${dim.id}` : `wiz.dim.${dim.id}`, L);
      grid += `
        <button type="button" class="dim-wizard-card-btn dicto-dim" data-dim="${dim.id}" aria-expanded="${isOpen}">
          ${previewSlot(dim.previewAction ? () => pieceEdges(dim.previewAction) : dim.preview)}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${['5D', '6D'].includes(dim.id) ? '' : isOpen ? '▾ ' : '▸ '}${dim.label}</span>
            <span class="dim-wizard-desc">${desc}</span>
            ${apps.length > 1 ? `<span class="dicto-tags">${doorFirst(apps.map((app) => ({ app }))).map((e) => tag(e.app)).join('')}</span>` : ''}
          </span>
        </button>`;
    }
    // The dimensions stay together (4D to 6D in sight on a phone); the open one's content follows them.
    const open = DIMENSIONS.find((x) => x.id === openDim && !['5D', '6D'].includes(x.id) && appsOf(x.id).some((a) => passes(a, filter)));
    bodyEl.innerHTML = `<div class="dim-wizard-sub">${t('wiz.sub', L)}</div><div class="dim-wizard-grid">${grid}</div>${open ? `<div class="dicto-dim-content">${dimensionContent(open.id, L)}</div>` : ''}`;
    mountPreviews();
    bodyEl.querySelectorAll('[data-dim]').forEach((el) => el.addEventListener('click', () => {
      const dim = el.dataset.dim;
      if (dim === '5D' || dim === '6D') { showCatalogue(dim); return; }
      openDim = openDim === dim ? null : dim;
      showDimensions(`[data-dim="${dim}"]`);
    }));
    bodyEl.querySelectorAll('.dicto-dim-content [data-action]').forEach((el) => el.addEventListener('click', () => choose(openDim, el.dataset.action, el.dataset.app)));
    bodyEl.querySelectorAll('[data-family]').forEach((el) => el.addEventListener('click', () => showPolyFamily(el.dataset.family)));
    wireSearch(L);
    if (scrollTo) bodyEl.querySelector(scrollTo)?.scrollIntoView({ block: 'start' });
  }

  // A dimension's content: every app's entries, one block per app in its own colours (DICTO
  // 2026-10-09: "divided in each app's colours"), the door's app first; inside a block, its kinds
  // (new work first).
  function dimensionContent(dim, L) {
    const d = dim.toLowerCase();
    // No repeats (DICTO 2026-10-09): a piece already listed by an earlier app (the door's first) is
    // left out of the later ones, and a lattice left with no pieces goes too.
    const seen = new Set();
    const entries = shownEntries(dim).map((e) => {
      if (!e.lat) return e;
      const pieces = e.lat.pieces.filter((pc) => !seen.has(pc.action));
      pieces.forEach((pc) => seen.add(pc.action));
      return pieces.length ? { ...e, lat: { ...e.lat, pieces } } : null;
    }).filter(Boolean);
    // The other door's app, whose lattices are the door's own (its difference is the Shear, or its
    // absence): one row, so each app stays in sight with no list repeated (DICTO 2026-10-09).
    if (dim === '3D') for (const app of ['kaleidohedra', 'rhombiverse']) {
      if (app === SITE || !passes(app, filter) || entries.some((e) => e.app === app)) continue;
      entries.push({ app, kind: 'family', fam: { id: 'otherApp', label: t(`wiz.other.${app}`, L), action: 'tool:pieceType:rd', preview: () => pieceEdges('tool:pieceType:rd') } });
    }
    entries.sort((x, y) => rank(x.app) - rank(y.app)); // stable: each block keeps its own order
    const row = (e) => {
      if (e.kind === 'family') return `
        <button type="button" class="dim-wizard-card-btn" data-action="${e.fam.action}" data-app="${e.app}">
          ${previewSlot(e.fam.preview)}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${e.fam.label}</span>
            <span class="dim-wizard-desc">${tFor(e.app, `wiz.${d}.${e.fam.id}`, L)}</span>
          </span>
        </button>`;
      if (e.kind === 'search') return `
        <div class="poly-search"><input type="search" class="poly-search-input" enterkeyhint="search" placeholder="${t('wiz.poly.searchPh', L)}" aria-label="${t('wiz.poly.searchPh', L)}"><div class="poly-search-results"></div></div>`;
      if (e.kind === 'shapes') {
        const ids = polyIds(e.key);
        if (!ids.length) return '';
        return `
        <button type="button" class="dim-wizard-card-btn" data-family="${e.key}">
          ${previewSlot(() => polyShapeEdges(ids[0]))}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${polyLabel(e.key)}</span>
            <span class="dim-wizard-desc">${tn('wiz.poly.count', L, ids.length)}</span>
          </span>
        </button>`;
      }
      // A world or lattice with one piece: one row, the row itself the thing to tap (copy audit).
      if (e.lat.pieces.length === 1) {
        const piece = e.lat.pieces[0];
        return `
        <button type="button" class="dim-wizard-card-btn" data-action="${piece.action}" data-app="${e.lattice3d ? dictoOpen(piece.action) : e.app}">
          ${previewSlot(() => (piece.preview ? piece.preview() : pieceEdges(piece.action)))}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${e.lat.label}</span>
            <span class="dim-wizard-desc">${tFor(e.app, `wiz.${d}.${e.lat.key}${e.dicto && e.lat.key === 'hex' ? 'Dicto' : ''}`, L)}</span>
          </span>
        </button>`;
      }
      // A lattice or world: its heading, then its pieces.
      return `
        <div class="dim-wizard-section">
          <span class="dim-wizard-label">${e.lat.label}</span>
          <span class="dim-wizard-desc">${tFor(e.app, `wiz.${d}.${e.lat.key}${e.dicto && e.lat.key === 'hex' ? 'Dicto' : ''}`, L)}</span>
        </div>${e.lat.pieces.map((piece) => `
        <button type="button" class="dim-wizard-card-btn dim-wizard-piece" data-action="${piece.action}" data-app="${e.lattice3d ? dictoOpen(piece.action) : e.app}">
          ${previewSlot(() => (piece.preview ? piece.preview() : pieceEdges(piece.action)))}
          <span class="dim-wizard-row-text"><span class="dim-wizard-label">${piece.label}</span></span>
        </button>`).join('')}`;
    };
    let html = '';
    for (const app of [...new Set(entries.map((e) => e.app))]) {
      const mine = entries.filter((e) => e.app === app);
      html += `<div class="dicto-block${app === 'dicto' && mine.some((e) => e.lattice3d) ? ' dicto-gold' : ''}" style="${blockStyle(app)}"><div class="dicto-block-name">${wordmark(app)}</div>`;
      // DICTO's own work first, in DICTO's livery.
      const dictoOwn = mine.filter((e) => e.dicto).sort((x, y) => dictoRank(x) - dictoRank(y));
      if (dictoOwn.length) html += `<div class="dicto-livery dicto-gold" style="${blockStyle('dicto')}"><div class="dicto-livery-name">${wordmark('dicto')}</div>${dictoOwn.map(row).join('')}</div>`;
      const rest = mine.filter((e) => !e.dicto);
      const kinds = app === 'dicto' ? [...KINDS.filter(([k]) => k === 'shapes'), ...KINDS.filter(([k]) => k !== 'shapes')] : KINDS;
      const restKinds = kinds.filter(([kind]) => rest.some((e) => e.kind === kind));
      for (const [kind, label] of restKinds) {
        if (restKinds.length > 1 && label) html += `<div class="dim-wizard-kind">${t(label, L)}</div>`;
        html += rest.filter((e) => e.kind === kind).map(row).join('');
      }
      html += '</div>';
    }
    return html;
  }

  // 5D/6D: one world each (the tiling picks every piece's shape), so the
  // screen is the catalogue: build freely, or summon an item, from the list
  // or by serial number (any tier's serial works from either screen).
  // Sections: zonohedra open, the vertex-star sections folded until tapped
  // (each open row runs a rotating preview, too many at once for a phone).
  const openSections = new Set(['zonohedron']);
  async function showCatalogue(dim) {
    current = () => showCatalogue(dim);
    resetPreviews();
    const L = getSettings().language;
    titleEl.textContent = t('cat.title', L, { dim });
    const entries = await loadCatalogue();
    const tier = dim.toLowerCase();
    const k = tier === '6d' ? 3 : 2;
    const mine = entries.filter((x) => x.tier === tier);
    const buildRow = `
        <button type="button" class="dim-wizard-card-btn" data-action="build">
          ${previewSlot(DIMENSIONS.find((x) => x.id === dim).preview)}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${t('cat.buildFreely', L)}</span>
            <span class="dim-wizard-desc">${t('cat.buildFreelyDesc', L)}</span>
          </span>
        </button>`;
    const row = (x) => {
      const n = pieceCount({ k }, x);
      return `
        <button type="button" class="dim-wizard-card-btn dim-wizard-piece" data-action="summon:${x.serial}">
          ${previewSlot(() => pieceEdges(`summon:${x.serial}`))}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${x.name}</span>
            <span class="dim-wizard-desc">#${x.serial} · ${tn('cat.pieces', L, n)}</span>
          </span>
        </button>`;
    };
    const sections = [
      { id: 'zonohedron', label: t('cat.zonohedra', L), desc: t('cat.zonohedraDesc', L), items: mine.filter((x) => x.kind === 'zonohedron') },
      { id: 'polytope', label: t('cat.polytopes', L), desc: t('cat.polytopesDesc', L), items: mine.filter((x) => x.kind === 'polytope') },
      { id: 'bridge', label: t('cat.bridges', L), desc: t('cat.bridgesDesc', L), items: mine.filter((x) => x.kind === 'bridge') },
      ...[1, 2, 3].map((r) => ({
        id: `patch${r}`,
        label: r === 1 ? t('cat.stars', L) : t('cat.starsRings', L, { n: r }),
        desc: t(r === 1 ? 'cat.starsDesc' : `cat.stars${r}Desc`, L),
        items: mine.filter((x) => x.kind === 'patch' && x.rings === r),
      })),
    ].filter((sec) => sec.items.length);
    const rows = sections.map((sec) => {
      const open = openSections.has(sec.id);
      return `
        <button type="button" class="dim-wizard-section dim-wizard-fold" data-section="${sec.id}" aria-expanded="${open}">
          <span class="dim-wizard-label">${open ? '▾' : '▸'} ${sec.label} (${sec.items.length})</span>
          <span class="dim-wizard-desc">${sec.desc}</span>
        </button>${open ? sec.items.map(row).join('') : ''}`;
    }).join('');
    bodyEl.innerHTML = `
      ${back(L)}
      <div class="dim-wizard-sub">${t('cat.sub', L, { dim })}</div>
      <div class="dim-wizard-serial-row">
        <input type="number" inputmode="numeric" min="1" placeholder="${t('cat.serial', L)}" aria-label="${t('cat.serial', L)}">
        <button type="button" class="dim-wizard-serial-go">${t('cat.summon', L)}</button>
      </div>
      <div class="dim-wizard-serial-msg" aria-live="polite"></div>
      <div class="dim-wizard-grid dicto-block" style="${blockStyle('rhombiverse')}">
        ${buildRow}
        ${rows}
      </div>`;
    mountPreviews();
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', () => showDimensions());
    bodyEl.querySelectorAll('.dim-wizard-fold').forEach((el) => {
      el.addEventListener('click', () => {
        const id = el.dataset.section;
        if (openSections.has(id)) openSections.delete(id); else openSections.add(id);
        const top = bodyEl.parentElement.scrollTop;
        showCatalogue(dim).then(() => { bodyEl.parentElement.scrollTop = top; });
      });
    });
    bodyEl.querySelectorAll('.dim-wizard-card-btn[data-action]').forEach((el) => {
      el.addEventListener('click', () => choose(dim, el.dataset.action === 'build' ? null : el.dataset.action, 'rhombiverse'));
    });
    const input = bodyEl.querySelector('.dim-wizard-serial-row input');
    const msg = bodyEl.querySelector('.dim-wizard-serial-msg');
    const go = () => {
      const serial = Number(input.value);
      const entry = Number.isInteger(serial) ? findBySerial(entries, serial) : null;
      if (!entry) { msg.textContent = input.value ? t('cat.noSerial', L, { serial: input.value }) : t('cat.typeSerial', L); return; }
      choose(entry.tier.toUpperCase(), `summon:${entry.serial}`, 'rhombiverse');
    };
    bodyEl.querySelector('.dim-wizard-serial-go').addEventListener('click', go);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
  }

  // ---- picking a shape for a face (D3's More…): families with only the shapes that fit ----
  let picker = null; // { fits(id), onPick(id) } while picking
  function showShapePicker() {
    current = showShapePicker;
    resetPreviews();
    const L = getSettings().language;
    titleEl.textContent = picker.title ?? t('poly.pickTitle', L);
    let grid = '';
    for (const key of ['PARTNERS', ...(picker.keepOpen ? ['FAVOURITES', 'RECENT'] : []), DICTO_POLY.key, ...POLY_FAMILIES]) {
      const ids = polyIds(key).filter(picker.fits);
      if (!ids.length) continue;
      grid += `
        <button type="button" class="dim-wizard-card-btn" data-family="${key}">
          ${previewSlot(() => polyShapeEdges(ids[0]))}
          <span class="dim-wizard-row-text">
            <span class="dim-wizard-label">${polyLabel(key)}</span>
            <span class="dim-wizard-desc">${tn('wiz.poly.count', L, ids.length)}</span>
          </span>
        </button>`;
    }
    bodyEl.innerHTML = `${picker.back ? back(L) : ''}<div class="dim-wizard-sub">${picker.sub ?? t('poly.pickSub', L)}</div><div class="dim-wizard-grid dicto-block" style="${blockStyle('polyhedraverse')}">${grid}</div>`;
    bodyEl.querySelector('.dim-wizard-back')?.addEventListener('click', () => { const b = picker.back; picker = null; titleEl.textContent = 'DICTO'; b(); });
    mountPreviews();
    bodyEl.querySelectorAll('[data-family]').forEach((el) => el.addEventListener('click', () => showPolyFamily(el.dataset.family)));
  }

  // ---- a Polyhedraverse family's shapes (from 3D+'s Shapes, or the picker) ----
  // Families shown in sections, as the old site's catalogue did (step D6): Parallelohedra (Fedorov's
  // five, variants, Kaleidohedra verified, the Regular 9), Stellations (one per solid), 3D+ Bridges
  // (cells, shadows, slices, corners), 4D Polytopes (by symmetry) and Space-Filling Pairs (a row per
  // pair: its honeycomb, then both shapes). [{ title, ids, pair }] or null for a plain grid.
  function familySections(key, L) {
    if (key === 'PARALLELOHEDRA') return [['fedorov', FEDOROV_FIVE], ['variants', PARALLELOHEDRON_VARIANTS], ['kaleidohedra', KALEIDOHEDRA_VERIFIED], ['regularNine', REGULAR_NINE]].map(([k, ids]) => ({ id: k, title: t(`pv.parallelohedra.section.${k}`, L), ids }));
    if (key === 'STELLATIONS') return [...new Set(STELLATION_IDS.map((id) => stellationInfo(id).solid))].map((solid) => ({ id: solid, title: stellatedSolidName(solid), ids: STELLATION_IDS.filter((id) => stellationInfo(id).solid === solid) }));
    if (key === 'BRIDGES_3D') return BRIDGE_SECTIONS.map((sec) => ({ id: sec.id, title: t(`pv.bridges.section.${sec.id}`, L), ids: sec.ids }));
    if (key === 'POLYTOPES_4D') return SYMMETRIES_4D.map((g) => ({ id: g, title: t('polytope.symmetry', L, { group: g }), ids: POLYTOPES_4D.filter((p) => p.symmetry === g).map((p) => p.id) }));
    if (key === 'SPACE_FILLING_PAIRS') return SPACE_FILLING_PAIR_LIST.map((p) => ({ id: p.ids.join('+'), title: p.honeycomb, ids: p.ids, pair: true }));
    return null;
  }
  function showPolyFamily(key) {
    current = () => showPolyFamily(key);
    resetPreviews();
    const L = getSettings().language;
    const fits = (x) => !picker || picker.fits(x);
    const card = (id) => `
        <button type="button" class="dim-wizard-card-btn dim-wizard-piece${gold(id)}" data-action="tool:polyShape:${id}">
          ${previewSlot(() => polyShapeEdges(id))}
          <span class="dim-wizard-row-text"><span class="dim-wizard-label">${polyShapeName(id).replaceAll('_', ' ')}</span></span>
        </button>`;
    const sections = familySections(key, L);
    const style = blockStyle(key === DICTO_POLY.key ? 'dicto' : 'polyhedraverse');
    const blocks = sections
      ? sections.map((sec) => ({ ...sec, ids: sec.ids.filter((id) => polyIds(key).includes(id) && fits(id)) })).filter((sec) => sec.ids.length)
        .map((sec) => `<div class="poly-section" data-section="${sec.id}"><div class="poly-section-title">${sec.title}</div>
          <div class="dim-wizard-grid dicto-block${sec.pair ? ' poly-pair' : ''}" style="${style}">${sec.ids.map(card).join(sec.pair ? '<span class="poly-pair-plus">+</span>' : '')}</div></div>`).join('')
      : `<div class="dim-wizard-grid dicto-block" style="${style}">${polyIds(key).filter(fits).map(card).join('')}</div>`;
    bodyEl.innerHTML = `
      ${back(L)}
      <div class="dim-wizard-sub"><b>${polyLabel(key)}</b> · ${t('wiz.poly.shapes', L)}</div>
      ${blocks}`;
    mountPreviews();
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', () => { if (picker) { showShapePicker(); return; } openDim = '3D'; showDimensions(`[data-family="${key}"]`); });
    bodyEl.querySelectorAll('[data-action]').forEach((el) => el.addEventListener('click', () => {
      if (picker) {
        const { onPick, keepOpen } = picker, picked = el.dataset.action.replace('tool:polyShape:', '');
        if (keepOpen) { picker = null; titleEl.textContent = 'DICTO'; } else close();
        onPick(picked);
        return;
      }
      const id = el.dataset.action.replace('tool:polyShape:', '');
      (polytope4D(id) ? showPolytopeDetail : showShapeDetail)(id, () => showPolyFamily(key));
    }));
  }

  // Two shapes side by side (D4): previews, families, faces by kind, edges, vertices, convex or not, and
  // the face kinds they share (where one can go on the other); Build with either.
  function showCompare(a, b, backTo) {
    current = () => showCompare(a, b, backTo);
    resetPreviews();
    const L = getSettings().language, A = POLYHEDRA[a], B = POLYHEDRA[b];
    const kinds = (id) => faceKindsOf(id).map((k) => `${k.count} × ${k.regular ? t('poly.d.regular', L) + ' ' : ''}${faceWord(k, L)}`).join(', ');
    const keyOf = (k) => `${k.kind}|${k.regular}|${k.n}`;
    const shared = faceKindsOf(a).filter((k) => faceKindsOf(b).some((m) => keyOf(m) === keyOf(k))).map((k) => faceWord(k, L));
    const col = (id, s) => `<div class="poly-compare-col"><canvas class="poly-compare-preview${gold(id)}" width="140" height="140" data-shape="${id}"></canvas>
      <div class="poly-detail-name">${polyShapeName(id).replaceAll('_', ' ')}</div>
      <div class="dim-wizard-desc">${familiesFor(id).map((f) => FAMILY_META[f]?.label ?? f).join(' · ')}</div>
      <dl class="poly-detail-stats"><dt>${t('poly.d.faces', L)}</dt><dd>${s.faces.length}: ${kinds(id)}</dd><dt>${t('poly.d.edges', L)}</dt><dd>${s.edges.length}</dd>
      <dt>${t('poly.d.vertices', L)}</dt><dd>${s.vertices.length}</dd><dt>${t('poly.d.shape', L)}</dt><dd>${isConvex(s) ? t('poly.d.convex', L) : t('poly.d.notConvex', L)}</dd></dl>
      <button type="button" class="poly-detail-build" data-build="${id}">${t('poly.d.build', L)}</button></div>`;
    bodyEl.innerHTML = `${back(L)}<div class="poly-compare dicto-block" style="${blockStyle('polyhedraverse')}">${col(a, A)}${col(b, B)}</div>
      <div class="poly-compare-shared"><b>${t('poly.d.common', L)}:</b> ${shared.length ? [...new Set(shared)].join(', ') : t('poly.d.noneShared', L)}</div>`;
    bodyEl.querySelectorAll('.poly-compare-preview').forEach((cv) => previewDisposers.push(mountWireframePreview(cv, polyShapeEdges(cv.dataset.shape), 140)));
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', () => backTo());
    bodyEl.querySelectorAll('[data-build]').forEach((x) => x.addEventListener('click', () => choose('3D', `tool:polyShape:${x.dataset.build}`, 'polyhedraverse')));
  }

  // Search, at the top of Polyhedraverse's block: results as rows, a tap opens the shape's details.
  let searchTimer = 0, lastQuery = '';
  function wireSearch(L) {
    const input = bodyEl.querySelector('.poly-search-input');
    if (!input) return;
    const out = bodyEl.querySelector('.poly-search-results');
    const run = () => {
      const q = input.value; lastQuery = q;
      const ids = searchShapes(q, L);
      out.innerHTML = !q.trim() ? '' : ids.length
        ? `<div class="dim-wizard-sub">${tn('wiz.poly.results', L, ids.length)}</div>` + ids.map((id) => `<button type="button" class="dim-wizard-card-btn dim-wizard-piece${gold(id)}" data-shape="${id}">
            <canvas class="dim-wizard-preview" width="40" height="40"></canvas><span class="dim-wizard-row-text"><span class="dim-wizard-label">${polyShapeName(id).replaceAll('_', ' ')}</span>
            <span class="dim-wizard-desc">${faceKindsOf(id).slice(0, 3).map((k) => `${k.count} × ${faceWord(k, L)}`).join(', ')}</span></span></button>`).join('')
        : `<div class="dim-wizard-sub">${t('wiz.poly.noResults', L)}</div>`;
      out.querySelectorAll('canvas').forEach((cv) => previewDisposers.push(mountWireframePreview(cv, polyShapeEdges(cv.parentElement.dataset.shape), 40)));
      out.querySelectorAll('[data-shape]').forEach((b) => b.addEventListener('click', () => showShapeDetail(b.dataset.shape, () => { showDimensions('.poly-search'); const i = bodyEl.querySelector('.poly-search-input'); if (i) { i.value = lastQuery; i.dispatchEvent(new Event('input')); } })));
    };
    input.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(run, 180); });
  }

  // A 4D polytope's details (D5): its finished shadow turning, Schläfli symbol, cells, symmetry, dual;
  // Build grows it cell by cell from its seed (the 600-cell also from a vertex).
  function showPolytopeDetail(id, backTo) {
    current = () => showPolytopeDetail(id, backTo);
    resetPreviews();
    const L = getSettings().language, p = polytope4D(id), dual = polytope4D(p.dual);
    const name = (q) => (q.common ? `${q.name} (${t(`polytope.common.${q.common}`, L)})` : q.name);
    bodyEl.innerHTML = `
      ${back(L)}
      <div class="poly-detail dicto-block" style="${blockStyle('polyhedraverse')}">
        <canvas class="poly-detail-preview" width="200" height="200"></canvas>
        <div class="poly-detail-name">${name(p)}</div>
        <div class="dim-wizard-desc"><span style="font-family:monospace">${p.schlafli}</span> · ${t('polytope.cells', L, { n: p.cells, cell: t(`polytope.cell.${p.seed}`, L) })}<br>${t('polytope.symmetry', L, { group: p.symmetry })} · ${dual.id === p.id ? t('polytope.selfDual', L) : t('polytope.dualOf', L, { name: name(dual) })}</div>
        <div class="poly-detail-actions">
          <button type="button" class="poly-detail-build" data-target="${p.target}">${t('polytope.build', L)}</button>
          ${p.vertexFirstTarget ? `<button type="button" class="poly-detail-build" data-target="${p.vertexFirstTarget}">${t('polytope.buildVertexFirst', L)}</button>` : ''}
        </div>
      </div>`;
    previewDisposers.push(mountWireframePreview(bodyEl.querySelector('.poly-detail-preview'), polyShapeEdges(id), 200));
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', () => backTo());
    bodyEl.querySelectorAll('.poly-detail-build').forEach((b) => b.addEventListener('click', () => choose('3D', `tool:polytope:${p.seed}|${b.dataset.target}`, 'polyhedraverse')));
  }

  // Where a shape came from or what it bridges to (the old site's details, step D6): the 3D+ Bridges
  // note, DICTO's Zometool, Kaleidohedra and Bain credits, the Dogstar's prior art, and the EKP pieces'
  // way into the EKP cell in Kaleidohedra.
  function creditsOf(id, L) {
    const out = [];
    if (BRIDGES_3D_IDS.includes(id)) out.push(`<div class="poly-credit" data-credit="bridge"><b>⤢ ${t('pv.detail.bridges', L)}</b><br>${t(`pv.bridge.${id}`, L)}</div>`);
    if (ZOME_PARALLELOHEDRA_ADDITION_IDS.includes(id) && !DICTO_SKEWED_ED_IDS.includes(id)) out.push(`<div class="poly-credit" data-credit="zome">${t('pv.detail.zomeCredit', L)}</div>`);
    if (DICTO_SKEWED_ED_IDS.includes(id)) out.push(`<div class="poly-credit" data-credit="skewed-ed">${t('pv.detail.dictoSkewedEdCredit', L)}</div>`);
    if (REGULAR_NINE_ADDITION_IDS.includes(id)) out.push(`<div class="poly-credit" data-credit="regular-nine">${t('pv.detail.regularNineCredit', L)}</div>`);
    if (id === 'DOGSTAR' || id === 'SEAMED_DODECAHEDRON') out.push(`<div class="poly-credit" data-credit="dogstar">${t('pv.detail.dogstarCredit', L)}</div>`);
    if (id === 'DOGSTAR' || id === 'SEAMED_DODECAHEDRON' || id === 'DRAGON_JEWEL') out.push(`<div class="poly-credit" data-credit="ekp">${t('pv.detail.ekpLink', L)} <button type="button" data-ekp>Kaleidohedra</button></div>`);
    if (BAIN_PARALLELOHEDRA_ADDITION_IDS.includes(id)) out.push(`<div class="poly-credit" data-credit="bain">${t('pv.detail.bainCredit', L)}</div>`);
    return out.join('');
  }

  // Extend into 4D: the polytope's real cell count first (as the old site's View 4D), e.g. "120
  // dodecahedron cells".
  function fourDCells(id, L) {
    if (!FOURD_CAPABLE_IDS.includes(id)) return '';
    const key = resolveParamsKey(POLYHEDRA[id]), p = FOUR_D_SHAPE_PARAMS[key]?.[0];
    return p ? `<b data-cells="${p.cellCount}">${p.name} · ${t('polytope.cells', L, { n: p.cellCount, cell: t(`polytope.cell.${key}`, L) })}</b><br>` : '';
  }

  // A shape's details: turning preview, its families, faces by kind, corners and edges, convex or not,
  // its pairs; Build with it, and ☆ Favourite (the same as pinning it in the strip).
  function showShapeDetail(id, backTo) {
    current = () => showShapeDetail(id, backTo);
    resetPreviews();
    const L = getSettings().language, star = !POLYHEDRA[id] && STAR_POLYHEDRA[id], s = POLYHEDRA[id] ?? star;
    if (!s) return;
    const fams = star ? ['Kepler–Poinsot'] : familiesFor(id).map((f) => FAMILY_META[f]?.label ?? f);
    const pairs = star ? [] : pairPartners(id).filter((x) => POLYHEDRA[x]);
    const fav = isFavourite(id);
    bodyEl.innerHTML = `
      ${back(L)}
      <div class="poly-detail dicto-block" style="${blockStyle('polyhedraverse')}">
        ${star ? '<div class="poly-detail-stage"></div>' : `<canvas class="poly-detail-preview${gold(id)}" width="200" height="200"></canvas>`}
        <div class="poly-detail-name">${polyShapeName(id).replaceAll('_', ' ')}</div>
        <div class="dim-wizard-desc">${fams.join(' · ')}</div>
        ${creditsOf(id, L)}
        <div class="poly-detail-actions">
          ${star ? '' : `<button type="button" class="poly-detail-build">${t('poly.d.build', L)}</button>`}
          <button type="button" class="poly-detail-fav" aria-pressed="${fav}">${fav ? '★' : '☆'} ${t('poly.d.fav', L)}</button>
          <button type="button" class="poly-detail-net" hidden aria-expanded="false">${t('poly.net.button', L)}</button>
          ${star ? '' : `<button type="button" class="poly-detail-compare">${t('poly.d.compare', L)}</button>
          <button type="button" class="poly-detail-4d" aria-expanded="false">${t(FOURD_CAPABLE_IDS.includes(id) ? 'poly.d.extend4d' : 'poly.d.prism4d', L)}</button>`}
        </div>
        <div class="poly-detail-4dbox" hidden><div class="poly-detail-stage"></div><div class="dim-wizard-desc">${fourDCells(id, L)}${t(FOURD_CAPABLE_IDS.includes(id) ? 'poly.d.extend4dNote' : 'poly.d.prism4dNote', L)}</div></div>
        <div class="poly-detail-netbox" hidden></div>
        <dl class="poly-detail-stats">
          <dt>${t('poly.d.faces', L)}</dt><dd>${s.faces.length}: ${faceKindsOf(id).map((k) => `${k.count} × ${k.regular ? t('poly.d.regular', L) + ' ' : ''}${faceWord(k, L)}`).join(', ')}</dd>
          <dt>${t('poly.d.edges', L)}</dt><dd>${s.edges.length}</dd>
          <dt>${t('poly.d.vertices', L)}</dt><dd>${s.vertices.length}</dd>
          <dt>${t('poly.d.shape', L)}</dt><dd>${isConvex(s) ? t('poly.d.convex', L) : t('poly.d.notConvex', L)}</dd>
          ${star ? `<dt>Schläfli</dt><dd>${STAR_POLYHEDRON_META[id].schlafli}</dd><dt>${t('poly.d.density', L)}</dt><dd>${STAR_POLYHEDRON_META[id].density}</dd>` : ''}
          ${pairs.length ? `<dt>${t('poly.d.pairs', L)}</dt><dd>${pairs.map((x) => `<button type="button" class="poly-detail-pair" data-shape="${x}">${polyShapeName(x).replaceAll('_', ' ')}</button>`).join(' ')}</dd>` : ''}
        </dl>
      </div>`;
    if (star) previewDisposers.push(mountStarView(bodyEl.querySelector('.poly-detail-stage'), id, { solid: t('poly.star.solid', L), translucent: t('poly.star.translucent', L), wireframe: t('poly.star.wireframe', L) }));
    else previewDisposers.push(mountWireframePreview(bodyEl.querySelector('.poly-detail-preview'), polyShapeEdges(id), 200));
    bodyEl.querySelector('.dim-wizard-back').addEventListener('click', () => backTo());
    bodyEl.querySelector('[data-ekp]')?.addEventListener('click', () => choose('3D', 'tool:roofFoldWorld', 'kaleidohedra'));
    if (star) return; // reference only: no building with a star solid
    bodyEl.querySelector('.poly-detail-build').addEventListener('click', () => choose('3D', `tool:polyShape:${id}`, 'polyhedraverse'));
    // 4D: the shape's 4D prism, or (4D-capable shapes) the whole 4D polytope it extends to.
    const b4 = bodyEl.querySelector('.poly-detail-4d'), box4 = bodyEl.querySelector('.poly-detail-4dbox');
    let dispose4 = null;
    b4.addEventListener('click', () => {
      const open = box4.hidden;
      box4.hidden = !open; b4.setAttribute('aria-expanded', String(open));
      if (open) { dispose4 = (FOURD_CAPABLE_IDS.includes(id) ? mountRadialView : mountDuoprismView)(box4.querySelector('.poly-detail-stage'), id); previewDisposers.push(() => dispose4?.()); }
      else { dispose4?.(); dispose4 = null; }
    });
    bodyEl.querySelector('.poly-detail-fav').addEventListener('click', () => { toggleFavourite(id); showShapeDetail(id, backTo); });
    // Compare: pick a second shape (Favourites and Recent first), then the two side by side.
    bodyEl.querySelector('.poly-detail-compare').addEventListener('click', () => {
      picker = { fits: (x) => x !== id, keepOpen: true, title: t('poly.d.compareTitle', L), sub: t('poly.d.compareSub', L, { name: polyShapeName(id).replaceAll('_', ' ') }),
        back: () => showShapeDetail(id, backTo), onPick: (other) => showCompare(id, other, () => showShapeDetail(id, backTo)) };
      showShapePicker();
    });
    // Net + PDF, for the shapes with a printable net.
    const netBtn = bodyEl.querySelector('.poly-detail-net'), netBox = bodyEl.querySelector('.poly-detail-netbox');
    netEligible().then((ok) => { if (ok.has(id) && netBtn.isConnected) netBtn.hidden = false; });
    netBtn.addEventListener('click', () => {
      const open = netBox.hidden;
      netBox.hidden = !open; netBtn.setAttribute('aria-expanded', String(open));
      if (open) previewDisposers.push(mountNetViewer(netBox, id, L));
    });
    bodyEl.querySelectorAll('.poly-detail-pair').forEach((b) => b.addEventListener('click', () => showShapeDetail(b.dataset.shape, () => showShapeDetail(id, backTo))));
  }

  overlay.querySelector('.dim-wizard-close').addEventListener('click', () => close());
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });

  function openOn(screen) {
    filter = null;
    openDim = '3D';
    paintApps();
    screen();
    overlay.classList.add('open');
  }
  function open() {
    countDicto();
    openOn(showDimensions); // always the dimensions on (re)open
  }
  function close() {
    resetPreviews();
    picker = null;
    overlay.querySelector('.dicto-apps').hidden = false;
    overlay.classList.remove('open');
  }
  /** D3's More…: the shapes that fit a face, by family; a tap picks one (onPick), ✕ cancels. */
  function openShapePicker(fits, onPick, { partners = [] } = {}) {
    picker = { fits, onPick };
    partnerIds = partners;
    paintApps();
    overlay.querySelector('.dicto-apps').hidden = true; // picking a shape, not an app
    showShapePicker();
    overlay.classList.add('open');
  }
  // Straight to a 5D/6D catalogue (the in-world Catalogue button).
  const openCatalogue = (dim) => openOn(() => showCatalogue(dim));
  // Straight to one dimension's screen (from inside a world).
  const openDimension = (dim) => openOn(() => {
    if (dim === '5D' || dim === '6D') { showCatalogue(dim); return; }
    if (DIMENSIONS.some((x) => x.id === dim)) openDim = dim;
    showDimensions(`[data-dim="${openDim}"]`);
  });

  return { open, openCatalogue, openDimension, openShapePicker, close, get isOpen() { return overlay.classList.contains('open'); } };
}
