// The 4D Permutohedron (DICTO 2026-11-10; working name, DICTO names it): DICTO's page "The 4D Permutohedron" as its own world, the same
// model, views and behaviour (perm4-geometry.js), drawn to the app's render standard (docs/RENDER-STANDARD.md: solid faces with polygon
// offset, crisp antialiased edges).
//   Build: the Schlegel view from just outside one truncated octahedron, that cell the see-through outer shell, the other 29 solid;
//     one big slider pulls the cells apart; All cells / 3D permutohedra / Hexagonal prisms.
//   Sweep: the 3D cut moving through the 120 corner heights (a stop in every gap), the cells' cross-sections tiling its surface, the
//     pair letting go rose and the pair meeting green at the last swap; Play the sweep, Next swap.
// Colours as on the page: truncated octahedron cream, hexagonal prism teal, letting go rose, meeting green, dark edges.
// Words in all 7 languages (i18n pm.*).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import * as PM from './perm4-geometry.js';

export const PM_TITLE = 'The 4D Permutohedron';   // working name (DICTO renames)
export const PM_MODES = ['build', 'sweep'];
export const PM_KINDS = PM.KINDS;
export const PM_GAP0 = 60;                        // the page's starting cut
export const PM_COLOURS = { to: 0xe7d9b4, hp: 0x5fa6b8, go: 0xe07a92, meet: 0x3fcf8a, edge: 0x111318 };
const VIEW_DIR = [3.3, 2.2, 3.9];                 // the page's camera
const lang = () => getSettings().language;
const hex = (c) => `#${new THREE.Color(c).getHexString()}`;

/** The caption, as the page's. */
export function pmCaption(view, L) {
  if (view.mode === 'build') return t(`pm.cap.${view.kind}`, L);
  const s = PM.sweepAt(view.gap, view.kind);
  const what = s.what === 'swap' ? t('pm.sweep.swap', L, { n: s.swap, total: PM.SWAP_TOTAL }) : t(`pm.sweep.${s.what}`, L);
  return t('pm.sweep.cap', L, { k: view.gap, n: PM.GAPS.length, what, cells: s.alive, a: s.to, b: s.hp });
}

export function createPerm4World({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('perm4');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { mode: 'build', kind: 'all', pull: 0, gap: PM_GAP0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (PM_MODES.includes(d?.mode)) view.mode = d.mode;
    if (PM_KINDS.includes(d?.kind)) view.kind = d.kind;
    if (Number.isFinite(d?.pull)) view.pull = Math.max(0, Math.min(1000, Math.round(d.pull)));
    if (Number.isInteger(d?.gap)) view.gap = Math.max(0, Math.min(PM.GAPS.length - 1, d.gap));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null, timer = null;

  const clear = () => { for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  /** Polygons (3D loops, model units) in one colour as one mesh and their crisp edges. */
  function polys(loops, col, op) {
    const pos = [], lines = [];
    for (const P0 of loops) {
      const P = P0.map((p) => p.map((x) => x * WS));
      for (let i = 1; i + 1 < P.length; i++) pos.push(...P[0], ...P[i], ...P[i + 1]);
      P.forEach((p, i) => lines.push(...p, ...P[(i + 1) % P.length]));
    }
    if (!pos.length) return;
    const see = op < 1;
    if (!skeleton) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.computeVertexNormals();
      const mat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.6, side: THREE.DoubleSide, flatShading: true, transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, emissive: new THREE.Color(col).multiplyScalar(0.12) });
      if (see) mat.userData.hollow = true;
      const m = new THREE.Mesh(g, mat); m.frustumCulled = false; if (see) m.renderOrder = 4; group.add(m);
    }
    const l = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color: skeleton ? 0xdfe6f0 : PM_COLOURS.edge, linewidth: see ? 1.4 : 1.8, transparent: see, opacity: see ? 0.5 : 1, depthWrite: !see }));
    l.geometry.setPositions(lines); l.frustumCulled = false; group.add(l);
  }
  function draw() {
    if (!active) return;
    clear();
    const see = opacity < 1;   // the app's Translucent view
    if (view.mode === 'build') {
      const cells = PM.buildCells(view.kind, view.pull / 1000);
      // the outer shell see-through (0.10 as the page), the other cells solid (0.95 on the page: here solid, the render standard)
      const outer = cells.filter((c) => c.outer), inner = cells.filter((c) => !c.outer);
      for (const k of ['TO', 'HP']) polys(inner.filter((c) => c.kind === k).flatMap((c) => c.faces), k === 'TO' ? PM_COLOURS.to : PM_COLOURS.hp, see ? opacity : 1);
      polys(outer.flatMap((c) => c.faces), PM_COLOURS.to, 0.1);
      shown = { mode: 'build', cells: cells.length, to: cells.filter((c) => c.kind === 'TO').length, outer: outer.length };
    } else {
      const s = PM.sweepAt(view.gap, view.kind);
      for (const [role, col] of [['go', PM_COLOURS.go], ['meet', PM_COLOURS.meet]]) polys(s.cells.filter((c) => c.role === role).map((c) => c.points), col, see ? opacity : 1);
      for (const k of ['TO', 'HP']) polys(s.cells.filter((c) => !c.role && c.kind === k).map((c) => c.points), k === 'TO' ? PM_COLOURS.to : PM_COLOURS.hp, see ? opacity : 1);
      const ev = s.event;
      shown = { mode: 'sweep', k: s.k, alive: s.alive, to: s.to, hp: s.hp, what: s.what, swap: s.swap, ev: { lost: ev.lost.length, gained: ev.gained.length, born: ev.born.length, died: ev.died.length },
        lit: { go: s.cells.filter((c) => c.role === 'go').length, meet: s.cells.filter((c) => c.role === 'meet').length } };
    }
    renderPanel();
  }
  // the picture fits radius 1 (Build) or 1.15 (Sweep) in model units; pulled apart, the cells reach out to 1 + 0.9 × pull
  const fitRadius = () => WS * (view.mode === 'build' ? 1 + 0.9 * (view.pull / 1000) : 1.15) * 1.08;
  const fit = () => fitView([0, 0, 0], fitRadius(), VIEW_DIR, true);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldperm4-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options pm-modes">${PM_MODES.map((m) => `<button type="button" data-pm-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options pm-kinds">${PM_KINDS.map((k) => `<button type="button" data-pm-kind="${k}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options pm-sweep-btns"><button type="button" data-pm-play></button><button type="button" data-pm-next></button></div>
    <div class="w4d-row st-note pm-legend"></div>
    <div class="w4d-row pm-pull-row"><label class="hull-pick"><span class="pm-pull-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row pm-cut-row"><label class="hull-pick"><span class="pm-cut-label"></span> <input type="range" class="st-slider" min="0" max="${PM.GAPS.length - 1}" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'perm4');
  const pullInput = panel.querySelector('.pm-pull-row input'), cutInput = panel.querySelector('.pm-cut-row input');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold'), legend = panel.querySelector('.pm-legend');
  note.addEventListener('click', () => note.classList.toggle('open'));
  const press = (x, on) => { x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), build = view.mode === 'build';
    panel.querySelectorAll('[data-pm-mode]').forEach((x) => { x.textContent = t(`pm.view.${x.dataset.pmMode}`, L); press(x, x.dataset.pmMode === view.mode); });
    panel.querySelectorAll('[data-pm-kind]').forEach((x) => { x.textContent = t(`pm.kind.${x.dataset.pmKind}`, L); press(x, x.dataset.pmKind === view.kind); });
    // nothing unnecessary shown: each view only its own slider and buttons
    panel.querySelector('.pm-pull-row').hidden = !build;
    panel.querySelector('.pm-cut-row').hidden = panel.querySelector('.pm-sweep-btns').hidden = build;
    const pb = panel.querySelector('[data-pm-play]');
    pb.textContent = t(timer ? 'pm.pause' : 'pm.play', L); press(pb, !!timer);
    panel.querySelector('[data-pm-next]').textContent = t('pm.next', L);
    // the legend: the two kinds, and in the Sweep the two colours of a swap
    const sw = (c, key) => `<span class="pm-sw"><i style="background:${hex(c)}"></i>${t(key, L)}</span>`;
    legend.innerHTML = [sw(PM_COLOURS.to, 'pm.legend.to'), sw(PM_COLOURS.hp, 'pm.legend.hp'), ...(build ? [] : [sw(PM_COLOURS.go, 'pm.legend.go'), sw(PM_COLOURS.meet, 'pm.legend.meet')])].join('');
    panel.querySelector('.pm-pull-label').textContent = t('pm.pull', L, { p: Math.round(view.pull / 10) });
    pullInput.value = String(view.pull);
    panel.querySelector('.pm-cut-label').textContent = t('pm.cut', L, { k: view.gap, n: PM.GAPS.length });
    cutInput.value = String(view.gap);
    caption.textContent = pmCaption(view, L);
    caption.classList.toggle('pm-swap', !build && shown.what === 'swap');
    note.textContent = t(build ? 'pm.note.build' : 'pm.note.sweep', L);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; save(); renderPanel(); } }
  pullInput.addEventListener('input', () => { stop(); view.pull = Number(pullInput.value); save(); draw(); });
  pullInput.addEventListener('change', fit);
  cutInput.addEventListener('input', () => { stop(); const k = Number(cutInput.value); if (k === view.gap) return; view.gap = k; save(); draw(); });
  panel.addEventListener('click', (e) => {
    if (e.target.closest('[data-pm-play]')) {
      if (timer) { stop(); return; }
      // the page's pace: a step every 380 ms (900 ms with reduced motion), round and round
      timer = setInterval(() => { if (!active || view.mode !== 'sweep') { stop(); return; } view.gap = (view.gap + 1) % PM.GAPS.length; draw(); }, matchMedia('(prefers-reduced-motion: reduce)').matches ? 900 : 380);
      renderPanel(); return;
    }
    if (e.target.closest('[data-pm-next]')) { stop(); view.gap = PM.nextSwap(view.gap); save(); draw(); return; }
    const b = e.target.closest('[data-pm-mode], [data-pm-kind]');
    if (!b) return;
    const { pmMode: mode, pmKind: kind } = b.dataset;
    if (mode) { if (mode === view.mode) return; stop(); view.mode = mode; save(); draw(); fit(); return; }
    if (kind && kind !== view.kind) { view.kind = kind; save(); draw(); }
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    /** ?open=perm4[:build|sweep|swap|to|hp]: that view (swap: the Sweep at its first swap after the page's starting cut). */
    setChain(kind) {
      if (PM_MODES.includes(kind)) view.mode = kind;
      else if (kind === 'swap') Object.assign(view, { mode: 'sweep', gap: PM.nextSwap(PM_GAP0 - 1) });
      else if (kind === 'to' || kind === 'hp') Object.assign(view, { mode: 'build', kind });
      else return;
      save();
      if (active) { draw(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { stop(); panel.classList.remove('visible'); return; }
      draw(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);
    },
    resetView() { stop(); Object.assign(view, { mode: 'build', kind: 'all', pull: 0, gap: PM_GAP0 }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe). */
    probe: () => (shown ? { ...shown, kind: view.kind, pull: view.pull, gap: view.gap, playing: !!timer, meshes: group.children.length } : null),
  };
}

/** The world's cover in the DICTO menu: the Build's edges (the outer truncated octahedron and the cells inside), the truncated
 *  octahedra cream and the prisms teal, the outer shell thicker. [[a, b], …] with .colours, .layers, .widths (wireframe-preview.js). */
export function perm4PreviewEdges() {
  const P = PM.BUILD_POINTS, cellOf = (a, b) => PM.CELLS.filter((c) => c.V.includes(a) && c.V.includes(b));
  const edges = [], colours = [], layers = [], widths = [];
  for (const [a, b] of PM.EDGES) {
    const cs = cellOf(a, b), outer = cs.some((c) => c === PM.CELLS[PM.OUTER]), hp = cs.some((c) => c.kind === 'HP');
    edges.push([P[a], P[b]]); colours.push(hex(hp ? PM_COLOURS.hp : PM_COLOURS.to)); layers.push(outer ? 1 : 0); widths.push(outer ? 2 : 1);
  }
  return Object.assign(edges, { colours, layers, widths });
}
