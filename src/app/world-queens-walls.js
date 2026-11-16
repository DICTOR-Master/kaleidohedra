// The Queens' walls (DICTO 2026-11-16; working name, DICTO may rename it): part 1, the Queens pulled apart.
// DICTO · dictospheres.com
// One switch White (the 600-cell) | Red (the 120-cell), one switch Cells | Sheets, a row of the four named directions (the Queens
// world's own, along the White Queen's turnings as its stage slider), and one long Apart slider at the bottom. The geometry is
// queens-walls-geometry.js (the Queens world's exact models; unit-tested):
//   Cells: each cell a pyramid from the centre, pulled out along its own cell's 4D direction and then projected, the 4D twin of the Vacuus
//     lens's Exploded view. The White Queen's tetrahedra in the app's tetrahedron red, the Red Queen's dodecahedra in its dodecahedron
//     violet: those cells are those solids.
//   Sheets: the 60 central sheets on the 60 mirrors (the Vacuus of the heart kind), the White Queen's as fans of 20 triangles, the Red
//     Queen's as fans of 12 pentagons, on the same 60 planes: switching the Queen keeps the sheets in place and swaps the faces. Apart
//     slides each sheet out along its own normal, like DICTO's cardboard Vacuus. The sheets in the label colour sky (the papers' full
//     sheet), not a solid's colour.
// Drawn to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, crisp antialiased edges (1.6 px), no haze;
// one merged mesh and one line set for the whole picture, moved in place as Apart moves (600 pyramids stay smooth on an iPad).
// Words in all 7 languages (i18n qw.*).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { QW_QUEENS, QW_MODES, QW_DIRECTIONS, QW_VERTICES, QW_RADIUS, QW_CELLS, QW_SHEETS, qwView } from './queens-walls-geometry.js';

export const QW_TITLE = "Queens' walls";
export const QW_COLOURS = { white: 0xcd3e28, red: 0x8a5cc4, sheet: 0x78c8f0, edge: 0x1d2027, strut: 0xc8ced8 };
const APART_MAX = 3;   // at the slider's end each piece has moved 3 × the Queen's radius (in 4D, before the shadow)
const lang = () => getSettings().language;
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);

export function createQueensWallsWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('queensWalls');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { queen: 'white', mode: 'sheets', dir: 'vertex-first', apart: 500 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (QW_QUEENS.includes(d?.queen)) view.queen = d.queen;
    if (QW_MODES.includes(d?.mode)) view.mode = d.mode;
    if (QW_DIRECTIONS.includes(d?.dir)) view.dir = d.dir;
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1000, Math.round(d.apart)));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;
  // the picture as base + a · offset per vertex (faces) and per line end, rebuilt when the queen, mode or direction changes
  let built = null;
  const clear = () => { for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  function build() {
    clear();
    const q = view.queen, { frame } = qwView(view.dir), pr = (x) => frame.map((f) => dot(x, f)).map((c) => c * WS);
    const P = QW_VERTICES[q].map(pr), R = QW_RADIUS[q];
    const pieces = view.mode === 'cells' ? QW_CELLS[q].map((c) => ({ dir: c.dir, faces: c.faces, corners: c.corners })) : QW_SHEETS[q].map((s) => ({ dir: s.normal, faces: s.faces, corners: [...new Set(s.faces.flat())] }));
    const fb = [], fo = [], fc = [], lb = [], lo = [], sb = [], so = [];
    const base = new THREE.Color(view.mode === 'cells' ? QW_COLOURS[q] : QW_COLOURS.sheet), c = new THREE.Color();
    pieces.forEach((p, n) => {
      const o = pr(p.dir).map((x) => x * R);
      // each piece a shade of the one colour (a label, so the pieces can be told apart), spread by the golden angle
      c.copy(base).multiplyScalar(0.72 + 0.4 * ((n * 0.6180339887) % 1));
      for (const f of p.faces) for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { fb.push(...P[k]); fo.push(...o); fc.push(c.r, c.g, c.b); }
      const seen = new Set();
      for (const f of p.faces) f.forEach((a, i) => { const b = f[(i + 1) % f.length], key = a < b ? `${a},${b}` : `${b},${a}`; if (seen.has(key)) return; seen.add(key); lb.push(...P[a], ...P[b]); lo.push(...o, ...o); });
      if (view.mode === 'cells') for (const k of p.corners) { sb.push(0, 0, 0, ...P[k]); so.push(...o, ...o); }   // the struts from the centre: the pyramid's sides
    });
    const see = opacity < 1;
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(fb), 3));
    geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(fc), 3));
    const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, side: THREE.DoubleSide, flatShading: true, transparent: see, opacity, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, emissive: base.clone().multiplyScalar(0.1) });
    if (see) mat.userData.hollow = true;
    const mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false; mesh.visible = !skeleton; if (see) mesh.renderOrder = 4;
    const line = (c, w, op) => { const l = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color: c, linewidth: w, transparent: op < 1, opacity: op, depthWrite: op >= 1 })); l.frustumCulled = false; return l; };
    const edges = line(skeleton ? 0xdfe6f0 : QW_COLOURS.edge, 1.6, 1);
    // the struts thin and faint (plain lines, moved in place: 2400 of them for the White Queen's cells)
    const sgeo = new THREE.BufferGeometry(); sgeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(sb.length), 3));
    const struts = new THREE.LineSegments(sgeo, new THREE.LineBasicMaterial({ color: QW_COLOURS.strut, transparent: true, opacity: 0.22, depthWrite: false }));
    struts.frustumCulled = false;
    group.add(mesh, edges, struts);
    built = { mesh, edges, struts, fb: new Float32Array(fb), fo: new Float32Array(fo), lb: new Float32Array(lb), lo: new Float32Array(lo), sb: new Float32Array(sb), so: new Float32Array(so), lpos: new Float32Array(lb.length) };
    shown = { queen: q, mode: view.mode, dir: view.dir, pieces: pieces.length, faces: pieces.reduce((n, p) => n + p.faces.length, 0), facesPerPiece: [...new Set(pieces.map((p) => p.faces.length))], sides: [...new Set(pieces.flatMap((p) => p.faces.map((f) => f.length)))] };
    move();
  }
  /** Apart: every piece moves in place (no rebuild). */
  function move() {
    if (!built) return;
    const a = (view.apart / 1000) * APART_MAX, pos = built.mesh.geometry.attributes.position.array;
    for (let i = 0; i < pos.length; i++) pos[i] = built.fb[i] + a * built.fo[i];
    built.mesh.geometry.attributes.position.needsUpdate = true;   // flat shading: no normals to recompute
    const out = built.lpos;
    for (let i = 0; i < out.length; i++) out[i] = built.lb[i] + a * built.lo[i];
    built.edges.geometry.dispose(); built.edges.geometry = new LineSegmentsGeometry(); built.edges.geometry.setPositions(out);
    const sp = built.struts.geometry.attributes.position.array;
    for (let i = 0; i < sp.length; i++) sp[i] = built.sb[i] + a * built.so[i];
    built.struts.geometry.attributes.position.needsUpdate = true;
    shown.apart = view.apart;
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], QW_RADIUS[view.queen] * WS * (1.1 + (view.apart / 1000) * APART_MAX), [0.3, 0.25, 1], true);
  const draw = () => { if (active) build(); };

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldqueensWalls-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options qw-queens">${QW_QUEENS.map((q) => `<button type="button" data-qw-queen="${q}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-modes">${QW_MODES.map((m) => `<button type="button" data-qw-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-dirs">${QW_DIRECTIONS.map((k) => `<button type="button" data-qw-dir="${k}"></button>`).join('')}</div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row qw-apart-row"><label class="hull-pick"><span class="qw-apart-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'queensWalls');
  const apartInput = panel.querySelector('.qw-apart-row input'), caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold');
  note.addEventListener('click', () => note.classList.toggle('open'));
  const press = (x, on) => { x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang();
    panel.querySelectorAll('[data-qw-queen]').forEach((x) => { x.textContent = t(`wq.queen.${x.dataset.qwQueen}`, L); press(x, x.dataset.qwQueen === view.queen); });
    panel.querySelectorAll('[data-qw-mode]').forEach((x) => { x.textContent = t(`qw.mode.${x.dataset.qwMode}`, L); press(x, x.dataset.qwMode === view.mode); });
    panel.querySelectorAll('[data-qw-dir]').forEach((x) => { x.textContent = t(`wq.btn.${x.dataset.qwDir}`, L); x.title = t(`wq.dir.${x.dataset.qwDir}`, L); press(x, x.dataset.qwDir === view.dir); });
    const p = Math.round(view.apart / 10);
    panel.querySelector('.qw-apart-label').textContent = t('qw.apart', L, { p });
    apartInput.value = String(view.apart);
    apartInput.setAttribute('aria-label', t('qw.apart', L, { p }));
    caption.textContent = `${t(`wq.dir.${view.dir}`, L)} · ${t(`qw.cap.${view.mode}.${view.queen}`, L)}`;
    note.textContent = `${t('qw.note', L)} ${t(`qw.note.${view.mode}`, L)}`;
  }
  apartInput.addEventListener('input', () => { const v = Number(apartInput.value); if (v === view.apart) return; view.apart = v; save(); move(); });
  apartInput.addEventListener('change', fit);
  panel.addEventListener('click', (e) => {
    const q = e.target.closest('[data-qw-queen]'), m = e.target.closest('[data-qw-mode]'), d = e.target.closest('[data-qw-dir]');
    if (q && q.dataset.qwQueen !== view.queen) { view.queen = q.dataset.qwQueen; save(); draw(); fit(); }
    else if (m && m.dataset.qwMode !== view.mode) { view.mode = m.dataset.qwMode; save(); draw(); }
    else if (d && d.dataset.qwDir !== view.dir) { view.dir = d.dataset.qwDir; save(); draw(); }
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    /** ?open=queenswalls:<white|red|cells|sheets>. */
    setChain(k) {
      if (QW_QUEENS.includes(k)) view.queen = k; else if (QW_MODES.includes(k)) view.mode = k; else return;
      save(); draw();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      build(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);
    },
    resetView() { Object.assign(view, { queen: 'white', mode: 'sheets', dir: 'vertex-first', apart: 500 }); save(); if (active) { build(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) build(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) build(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, the pieces and how far the pieces have moved (the largest move on screen). */
    probe: () => {
      if (!shown || !built) return null;
      const pos = built.mesh.geometry.attributes.position.array;
      let moved = 0;
      for (let i = 0; i < pos.length; i += 3) moved = Math.max(moved, Math.hypot(pos[i] - built.fb[i], pos[i + 1] - built.fb[i + 1], pos[i + 2] - built.fb[i + 2]));
      return { ...shown, moved };
    },
  };
}

/** The world's cover in the DICTO menu: the White Queen's 60 sheets half apart, their triangles' edges, vertex-first. */
export function queensWallsPreviewEdges() {
  const { frame } = qwView('vertex-first'), V = QW_VERTICES.white, out = [];
  for (const s of QW_SHEETS.white) {
    const o = frame.map((f) => dot(s.normal, f) * 0.9);
    const P = (i) => frame.map((f, k) => (dot(V[i], f) + o[k] * 2) / 3.8);
    for (const f of s.faces) f.forEach((a, i) => out.push([P(a), P(f[(i + 1) % 3])]));
  }
  return out;
}
