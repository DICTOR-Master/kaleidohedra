// Aristotle's Pyramid (DICTO 2026-10-21; DICTO's question, paper #44, DICTO DOI 10.5281/zenodo.23529497): the "View in app" of the
// paper. Aristotle wrote that among solids only the pyramid and the cube fill space; DICTO asked whether he could have meant the
// Cleo-Icos. Two views:
//   - The five pyramids: a Platonic solid (tappable cards) split into its face pyramids, a big slider drawing them apart, and one line
//     from the paper's theorem on whether its pyramid fills space (the cube's alone; the tetrahedron's and octahedron's only together;
//     the dodecahedron's and the Cleo-Icos never, with face pyramids).
//   - Fills: three ready-made blocks: cube pyramids filling cubes; the octet cut up; the golden fix (2 Cleo-Icos + 1 Antonius make a
//     prolate golden rhombohedron; rhombohedra fill space), each piece kind its own tone; "Build it yourself" opens the
//     Polyhedraverse kit 'antonius.block'.
// Geometry: aristotle-geometry.js (from krp-core's Platonic solids and the Cleo-Icos & Antonius kit). Words: i18n ar.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey, theme } from './site.js';
import { SOLID_KEYS, FILL_KEYS, GOLDEN_KIT, facePyramids, fillPieces } from './aristotle-geometry.js';

export const ARISTOTLE_KIT_ACTION = `tool:polyKit:${GOLDEN_KIT}`;
const EDGE_COLOR = 0x0b1220;
const PRESET = { mode: 'pyramids', solid: 'cube', fill: 'cube', apart: 30 };
const lang = () => getSettings().language;

/** One piece as a mesh (its polygons fanned into triangles) and its edges as lines. */
function pieceGeometry(p) {
  const tri = [], lines = [];
  for (const F of p.faces) {
    for (let i = 1; i + 1 < F.length; i++) tri.push(...F[0], ...F[i], ...F[i + 1]);
    F.forEach((v, i) => lines.push(...v, ...F[(i + 1) % F.length]));
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(tri, 3)); g.computeVertexNormals();
  const l = new THREE.BufferGeometry(); l.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  return { g, l };
}
const reach = (pieces) => Math.max(...pieces.flatMap((p) => p.faces.flat().map((v) => Math.hypot(...v))));

export function createAristotleWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, openAction = () => {} }) {
  const STORAGE_KEY = storageKey('aristotle');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  function read(d) {
    if (!d) return;
    if (['pyramids', 'fills'].includes(d.view?.mode)) view.mode = d.view.mode;
    if (SOLID_KEYS.includes(d.view?.solid)) view.solid = d.view.solid;
    if (FILL_KEYS.includes(d.view?.fill)) view.fill = d.view.fill;
    if (Number.isFinite(d.view?.apart)) view.apart = Math.max(0, Math.min(100, d.view.apart));
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, view: { ...view } });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };

  let active = false, skeleton = false, opacity = 1, pickTargets = [], drawn = []; // drawn: [{ piece, mesh, line }]
  // the app's piece look; a second tone of the app colour for the second kind of piece (as in the Reuleaux build, DICTO)
  const pieceMat = new THREE.MeshStandardMaterial({ color: theme().pieceHex, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const pieceMat2 = pieceMat.clone(); const toneOf = (hex) => new THREE.Color(hex).offsetHSL(0.03, -0.1, -0.3);
  const edgeMat = new THREE.LineBasicMaterial({ color: EDGE_COLOR });
  function styleMaterials() {
    for (const [m, c] of [[pieceMat, new THREE.Color(theme().pieceHex)], [pieceMat2, toneOf(theme().pieceHex)]]) {
      m.color.copy(c); m.transparent = opacity < 1; m.opacity = opacity; m.depthWrite = opacity >= 1; m.needsUpdate = true;
    }
    edgeMat.color.setHex(skeleton ? theme().accentHex : EDGE_COLOR);
  }
  function clearGroup() {
    for (const c of [...group.children]) { group.remove(c); c.geometry?.dispose(); }
    pickTargets = []; drawn = [];
  }
  const pieces = () => (view.mode === 'pyramids' ? facePyramids(view.solid) : fillPieces(view.fill));
  // every solid and block about the same size on screen
  const sizeOf = () => (view.mode === 'pyramids' ? 1.1 : 1.6) * WS / reach(pieces());
  function draw() {
    clearGroup();
    if (!active) return;
    styleMaterials();
    const s = sizeOf();
    pieces().forEach((p, i) => {
      const { g, l } = pieceGeometry(p);
      const mesh = new THREE.Mesh(g, p.tone ? pieceMat2 : pieceMat); mesh.userData = { kind: 'ar', piece: i };
      const line = new THREE.LineSegments(l, edgeMat);
      for (const o of [mesh, line]) { o.scale.setScalar(s); group.add(o); }
      mesh.visible = !skeleton;
      pickTargets.push(mesh); drawn.push({ piece: p, mesh, line });
    });
    applyApart();
  }
  function applyApart() {
    const d = view.mode === 'pyramids' ? (view.apart / 100) * 0.9 * WS : 0;
    for (const { piece, mesh, line } of drawn) for (const o of [mesh, line]) o.position.set(...piece.axis.map((x) => x * d));
  }
  const fit = () => fitView([0, 0, 0], view.mode === 'pyramids' ? 1.1 * WS + 0.9 * WS : 1.6 * WS, null, true);

  const pieceName = (kind, L = lang()) => t(`ar.piece.${kind}`, L);
  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'ar' || mode === 'paint' || mode === 'chisel') return false;
    const p = drawn[ud.piece]?.piece;
    if (p) showHudPrompt(pieceName(p.kind), 2200);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldaristotle-panel'; panel.className = 'qc-panel';
  const style = document.createElement('style');
  style.textContent = `#worldaristotle-panel .ar-cards{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
#worldaristotle-panel .ar-cards button{display:flex;flex-direction:column;align-items:center;min-width:96px;min-height:52px;padding:6px 8px;line-height:1.15}
#worldaristotle-panel .ar-cards button small{opacity:.7;font-size:11px}
#worldaristotle-panel .ar-cards button.active{border-color:var(--accent,#ff9a52);color:var(--accent,#ff9a52)}
#worldaristotle-panel .ar-apart-row input{width:100%}
#worldaristotle-panel .ar-apart-row label{flex:1}`;
  document.head.appendChild(style);
  panel.innerHTML = `
    <div class="w4d-row st-note ar-note"></div>
    <div class="w4d-row w4d-options ar-modes"><button type="button" data-ar-mode="pyramids"></button><button type="button" data-ar-mode="fills"></button></div>
    <div class="w4d-row ar-cards"></div>
    <div class="w4d-row ar-apart-row"><label class="hull-pick"><span class="ar-apart-label"></span> <input type="range" class="st-slider" min="0" max="100" step="1"></label></div>
    <div class="w4d-row w4d-options"><button type="button" data-ar="build"></button></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'aristotle');
  const slider = panel.querySelector('.ar-apart-row input');
  const cardHtml = (attr, k, on, label, small) => `<button type="button" ${attr}="${k}" class="${on ? 'active' : ''}" aria-pressed="${on}">${label}<small>${small}</small></button>`;
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), pyr = view.mode === 'pyramids';
    panel.querySelector('.ar-note').textContent = pyr ? t(`ar.fills.${view.solid}`, L) : t(`ar.fill.${view.fill}.note`, L);
    panel.querySelectorAll('[data-ar-mode]').forEach((b) => { const on = b.dataset.arMode === view.mode; b.textContent = t(`ar.mode.${b.dataset.arMode}`, L); b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    panel.querySelector('.ar-cards').innerHTML = pyr
      ? SOLID_KEYS.map((k) => cardHtml('data-ar-solid', k, k === view.solid, t(`ar.solid.${k}`, L), k === 'icosahedron' ? t('ar.count.cleo', L) : t('ar.count', L, { n: facePyramids(k).length }))).join('')
      : FILL_KEYS.map((k) => cardHtml('data-ar-fill', k, k === view.fill, t(`ar.fill.${k}`, L), t('ar.pieces', L, { n: fillPieces(k).length }))).join('');
    panel.querySelector('.ar-apart-row').hidden = !pyr;
    panel.querySelector('.ar-apart-label').textContent = t('ar.apart', L);
    slider.value = String(view.apart);
    const build = panel.querySelector('[data-ar="build"]');
    build.hidden = pyr || view.fill !== 'golden'; // the kit is the golden fix's
    build.textContent = t('ar.build', L);
  }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || !panel.contains(b)) return;
    if (b.dataset.arMode) {
      if (b.dataset.arMode === view.mode) return;
      view.mode = b.dataset.arMode; save(); draw(); renderPanel(); fit();
      showHudPrompt(t(view.mode === 'pyramids' ? 'ar.prompt.start' : 'ar.prompt.fills', lang()), 3500);
      return;
    }
    if (b.dataset.arSolid) { if (b.dataset.arSolid === view.solid) return; view.solid = b.dataset.arSolid; save(); draw(); renderPanel(); return; }
    if (b.dataset.arFill) { if (b.dataset.arFill === view.fill) return; view.fill = b.dataset.arFill; save(); draw(); renderPanel(); return; }
    if (b.dataset.ar === 'build') openAction(ARISTOTLE_KIT_ACTION);
  });
  slider.addEventListener('input', () => { view.apart = Number(slider.value); applyApart(); });
  slider.addEventListener('change', save);
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets.filter((m) => m.visible),
    handleTap,
    /** ?open=aristotle:<pyramids|fills|cube|tetrahedron|octahedron|dodecahedron|icosahedron|octet|golden>. */
    open(arg) {
      if (arg === 'pyramids' || arg === 'fills') view.mode = arg;
      else if (SOLID_KEYS.includes(arg)) { view.mode = 'pyramids'; view.solid = arg; }
      else if (FILL_KEYS.includes(arg)) { view.mode = 'fills'; view.fill = arg; }
      save(); if (active) { draw(); renderPanel(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { clearGroup(); renderPanel(); return; }
      draw(); renderPanel(); fit();
      showHudPrompt(t(view.mode === 'pyramids' ? 'ar.prompt.start' : 'ar.prompt.fills', lang()), 5000);
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() { Object.assign(view, PRESET); save(); if (active) { draw(); renderPanel(); fit(); } },
    resetView() {},
    snapshot,
    restore(json) { read(json); save(); if (active) { draw(); renderPanel(); } },
    /** For the browser tests (?probe). */
    probe() { return { mode: view.mode, solid: view.solid, fill: view.fill, apart: view.apart, pieces: drawn.length, kinds: [...new Set(drawn.map((d) => d.piece.kind))], offset: drawn[0]?.mesh.position.length() ?? 0 }; },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the Cleo-Icos, tip at the centre. */
export function aristotlePreviewPoints() { return facePyramids('icosahedron')[0].faces[0].concat([[0, 0, 0]]); }
