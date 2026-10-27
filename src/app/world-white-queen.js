// The White Queen 600-cell (DICTO 2026-10-27): the companion world of paper #63, "The White Queen 600-cell" (DOI not yet assigned).
// Step 2, the shadows: the true orthogonal 3D shadow of the 600-cell, every one computed live from the exact source model
// (white-queen-data.js via white-queen-geometry.js; no other 600-cell code). All 720 edges are drawn projected (the inner ones too),
// the convex hull as a see-through shell, its real faces (coplanar triangles merged) ivory for triangles and blue for four-sided faces,
// as in #63's figures. Six turnings (DICTO 2026-10-27), one for each pair of the four main directions: two rows of four buttons pick
// the start (From) and the end (To), each jumping to its stop, and one big slider turns the 4D view direction along that pair's great
// circle, snapping at both ends; the caption gives the hull's vertices and faces. Words in all 7 languages (i18n wq.*); the slice view
// comes later.
import * as THREE from 'three';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DIRECTIONS, EDGES, shadowAt, viewAt } from './white-queen-geometry.js';

export const WQ_DIRECTIONS = DIRECTIONS;
/** The slider: 0..1000 along the chosen turning, its two ends the stops (it snaps to one within WQ_SNAP). */
export const WQ_SNAP = 40;
export const WQ_DEFAULT = { from: 'vertex-first', to: 'cell-first' };
const SHORT = { vertex: 'vertex-first', edge: 'edge-first', face: 'face-first', cell: 'cell-first' };   // ?open=whitequeen:<short>
const IVORY = 0xefe9dc, BLUE = 0x9fb4c8, OTHER = 0xd8c690;   // as #63's figures (render_atlas.py); faces of 5+ sides never show at the stops
const SHELL = 0.42;   // the see-through shell's opacity
const lang = () => getSettings().language;

/** The caption: the direction at a stop (or "from → to" between them) and the hull's vertex and face counts. */
export function wqCaption({ from, to, u }, s, L) {
  const head = u === 0 ? t(`wq.dir.${from}`, L) : u === 1000 ? t(`wq.dir.${to}`, L) : t('wq.between', L, { a: t(`wq.dir.${from}`, L), b: t(`wq.dir.${to}`, L) });
  const parts = [t('wq.count.vertices', L, { n: s.vertices.length }), t('wq.count.triangles', L, { n: s.triangles })];
  if (s.quads) parts.push(t('wq.count.quads', L, { n: s.quads }));
  if (s.others) parts.push(t('wq.count.others', L, { n: s.others }));
  return `${head} · ${parts.join(' · ')}`;
}

export function createWhiteQueenWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('whiteQueen');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { ...WQ_DEFAULT, u: 0 };   // the turning (from → to) and the slider's place on it
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (DIRECTIONS.includes(d?.from) && DIRECTIONS.includes(d?.to) && d.from !== d.to) Object.assign(view, { from: d.from, to: d.to });
    if (Number.isFinite(d?.u)) view.u = Math.max(0, Math.min(1000, Math.round(d.u)));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;

  const shellMat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: SHELL, depthWrite: false, roughness: 0.6, metalness: 0, emissive: 0x3a3730 });
  shellMat.userData.hollow = true;
  const innerMat = new THREE.LineBasicMaterial({ color: 0xb8c2d6, transparent: true, opacity: 0.3, depthWrite: false });   // the inner edges step back so the outline reads
  const hullMat = new THREE.LineBasicMaterial({ color: 0xfff4d6 });
  // fixed buffers, refilled as the slider moves: 720 edges, and the shell (at most 2 × 120 − 4 hull triangles)
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(EDGES.length * 6), 3));
  const inner = new THREE.LineSegments(edgeGeo, innerMat);
  const shellGeo = new THREE.BufferGeometry();
  shellGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  shellGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  shellGeo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  const shell = new THREE.Mesh(shellGeo, shellMat);
  shell.renderOrder = 2;
  const hullGeo = new THREE.BufferGeometry();
  hullGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(360 * 6), 3));
  const hullLines = new THREE.LineSegments(hullGeo, hullMat);
  group.add(inner, shell, hullLines);
  for (const o of [inner, shell, hullLines]) o.frustumCulled = false;

  function draw() {
    if (!active) return;
    const s = shadowAt(view.from, view.to, view.u / 1000);
    shown = s;
    const P = s.P.map((p) => p.map((c) => c * WS)), Q = s.points.map((p) => p.map((c) => c * WS));
    const ep = edgeGeo.attributes.position.array;
    EDGES.forEach(([i, j], k) => { ep.set(P[i], k * 6); ep.set(P[j], k * 6 + 3); });
    edgeGeo.attributes.position.needsUpdate = true;
    const sp = shellGeo.attributes.position.array, sc = shellGeo.attributes.color.array, sn = shellGeo.attributes.normal.array, hp = hullGeo.attributes.position.array;
    const col = new THREE.Color(), a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
    let n = 0, m = 0;
    for (const f of s.faces) {
      col.setHex(f.length === 3 ? IVORY : f.length === 4 ? BLUE : OTHER);
      a.fromArray(Q[f[0]]); b.fromArray(Q[f[1]]).sub(a); c.fromArray(Q[f[2]]).sub(a);
      const nrm = b.cross(c).normalize();
      for (let i = 1; i + 1 < f.length; i++) {
        for (const k of [f[0], f[i], f[i + 1]]) { sp.set(Q[k], n * 3); sc.set([col.r, col.g, col.b], n * 3); sn.set([nrm.x, nrm.y, nrm.z], n * 3); n++; }
      }
      f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (k < l) { hp.set(Q[k], m * 3); hp.set(Q[l], m * 3 + 3); m += 2; } });
    }
    shellGeo.setDrawRange(0, n);
    hullGeo.setDrawRange(0, m);
    for (const x of ['position', 'color', 'normal']) shellGeo.attributes[x].needsUpdate = true;
    hullGeo.attributes.position.needsUpdate = true;
    shell.visible = !skeleton;
    shellMat.opacity = SHELL * opacity;
    renderPanel();
  }
  const R = 2 * WS;   // the 600-cell's circumradius: every shadow fits inside it
  const fit = () => fitView([0, 0, 0], R * 1.12, [0.3, 0.25, 1]);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldwhiteQueen-panel';
  panel.className = 'qc-panel';
  const row = (end) => `<div class="w4d-row w4d-options wq-row"><span class="hull-pick wq-row-label" data-wq-label="${end}"></span>${DIRECTIONS.map((k) => `<button type="button" data-wq-${end}="${k}"></button>`).join('')}</div>`;
  panel.innerHTML = `
    ${row('from')}
    ${row('to')}
    <div class="w4d-row wq-param-row"><label class="hull-pick"><span class="wq-param-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'whiteQueen');
  const input = panel.querySelector('input'), caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note');
  note.addEventListener('click', () => note.classList.toggle('open'));
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang();
    for (const end of ['from', 'to']) {
      panel.querySelector(`[data-wq-label="${end}"]`).textContent = t(`wq.${end}`, L);
      panel.querySelectorAll(`[data-wq-${end}]`).forEach((x) => {
        const k = x.dataset[end === 'from' ? 'wqFrom' : 'wqTo'];
        x.textContent = t(`wq.dir.${k}`, L);
        x.classList.toggle('active', k === view[end]);
        x.hidden = end === 'to' && k === view.from;   // a direction does not turn to itself: nothing unnecessary shown
      });
    }
    panel.querySelector('.wq-param-label').textContent = t('wq.param', L, { a: t(`wq.dir.${view.from}`, L), b: t(`wq.dir.${view.to}`, L) });
    input.value = String(view.u);
    caption.textContent = wqCaption(view, shown, L);
    note.textContent = t('wq.note', L);
  }
  const go = (v) => { if (v === view.u) return; view.u = v; save(); draw(); };
  input.addEventListener('input', () => {
    let v = Number(input.value);
    if (v <= WQ_SNAP) v = 0; else if (v >= 1000 - WQ_SNAP) v = 1000;
    input.value = String(v);
    go(v);
  });
  // From: the turning starts there (the slider at its start); To: it ends there (the slider at its end). Picking as From the
  // direction that is To swaps the two.
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('[data-wq-from], [data-wq-to]');
    if (!b) return;
    const from = b.dataset.wqFrom, to = b.dataset.wqTo;
    if (from) { if (from === view.to) view.to = view.from; view.from = from; view.u = 0; }
    else if (to && to !== view.from) { view.to = to; view.u = 1000; }
    else return;
    save(); draw();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=whitequeen:<vertex|edge|face|cell>: start at that main direction (turning to cell-first, or vertex-first from cell-first). */
    setChain(kind) {
      const k = SHORT[kind] ?? kind;
      if (!DIRECTIONS.includes(k)) return;
      Object.assign(view, { from: k, to: k === WQ_DEFAULT.to ? WQ_DEFAULT.from : WQ_DEFAULT.to, u: 0 }); save();
      if (active) draw();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      draw(); fit();
    },
    resetView() { Object.assign(view, WQ_DEFAULT, { u: 0 }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the turning, the slider, the direction, the hull's counts and the edges drawn. */
    probe: () => (shown ? { from: view.from, to: view.to, u: view.u, stop: view.u === 0 ? view.from : view.u === 1000 ? view.to : null, dir: viewAt(view.from, view.to, view.u / 1000).u, vertices: shown.vertices.length, triangles: shown.triangles, quads: shown.quads, others: shown.others, faces: shown.faces.length, edges: EDGES.length, shell: shell.visible } : null),
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the vertex-first shadow. */
export const whiteQueenPreviewPoints = () => shadowAt(0, 0, 0).points;
