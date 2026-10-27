// The White Queen 600-cell (DICTO 2026-10-27): the companion world of paper #63, "The White Queen 600-cell" (DOI not yet assigned).
// Step 2, the shadows: the true orthogonal 3D shadow of the 600-cell, every one computed live from the exact source model
// (white-queen-data.js via white-queen-geometry.js; no other 600-cell code). All 720 edges are drawn projected (the inner ones too),
// the convex hull as a see-through shell, its real faces (coplanar triangles merged) ivory for triangles and blue for four-sided faces,
// as in #63's figures. Four buttons (vertex-, edge-, face-, cell-first) and one big slider that turns the 4D view direction along the
// path vertex → edge → face → cell first, snapping at the four main directions; the caption gives the hull's vertices and faces.
// Words in all 7 languages (i18n wq.*); the slice view comes later.
import * as THREE from 'three';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DIRECTIONS, EDGES, shadowAt, viewAt } from './white-queen-geometry.js';

export const WQ_DIRECTIONS = DIRECTIONS;
/** The slider: 0..3000, the four main directions at 0, 1000, 2000, 3000 (it snaps to one within SNAP). */
export const WQ_STOPS = DIRECTIONS.map((key, i) => ({ key, u: i * 1000 }));
export const WQ_SNAP = 40;
const SHORT = { vertex: 'vertex-first', edge: 'edge-first', face: 'face-first', cell: 'cell-first' };   // ?open=whitequeen:<short>
const IVORY = 0xefe9dc, BLUE = 0x9fb4c8, OTHER = 0xd8c690;   // as #63's figures (render_atlas.py); faces of 5+ sides never show at the stops
const SHELL = 0.42;   // the see-through shell's opacity
const lang = () => getSettings().language;

/** The caption: the direction (or "a → b" for the two it lies between) and the hull's vertex and face counts. */
export function wqCaption(u, s, L) {
  const st = WQ_STOPS.find((x) => x.u === u);
  const head = st ? t(`wq.dir.${st.key}`, L) : t('wq.between', L, { a: t(`wq.dir.${DIRECTIONS[Math.floor(u / 1000)]}`, L), b: t(`wq.dir.${DIRECTIONS[Math.ceil(u / 1000)]}`, L) });
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
  let u = 0;
  try { const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'); if (Number.isFinite(d?.u)) u = Math.max(0, Math.min(3000, Math.round(d.u))); } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ u })); } catch { /* best-effort */ } };
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
    const s = shadowAt(u / 1000);
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
  panel.innerHTML = `
    <div class="w4d-row w4d-options wq-dir-buttons">${DIRECTIONS.map((k) => `<button type="button" data-wq-dir="${k}"></button>`).join('')}</div>
    <div class="w4d-row wq-param-row"><label class="hull-pick"><span class="wq-param-label"></span> <input type="range" class="st-slider" min="0" max="3000" step="1"></label></div>
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
    panel.querySelectorAll('[data-wq-dir]').forEach((x) => { x.textContent = t(`wq.dir.${x.dataset.wqDir}`, L); x.classList.toggle('active', WQ_STOPS.find((s) => s.key === x.dataset.wqDir).u === u); });
    panel.querySelector('.wq-param-label').textContent = t('wq.param', L);
    input.value = String(u);
    caption.textContent = wqCaption(u, shown, L);
    note.textContent = t('wq.note', L);
  }
  const go = (v) => { if (v === u) return; u = v; save(); draw(); };
  input.addEventListener('input', () => {
    let v = Number(input.value);
    const st = WQ_STOPS.find((s) => Math.abs(s.u - v) <= WQ_SNAP);
    if (st) { v = st.u; input.value = String(v); }
    go(v);
  });
  panel.querySelector('.wq-dir-buttons').addEventListener('click', (e) => {
    const k = e.target.closest('[data-wq-dir]')?.dataset.wqDir;
    const st = WQ_STOPS.find((s) => s.key === k);
    if (st) go(st.u);
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=whitequeen:<vertex|edge|face|cell>: start at that main direction. */
    setChain(kind) {
      const st = WQ_STOPS.find((s) => s.key === (SHORT[kind] ?? kind));
      if (st) { u = st.u; save(); if (active) draw(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      draw(); fit();
    },
    resetView() { u = 0; save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the slider, the direction, the hull's counts and the edges drawn. */
    probe: () => (shown ? { u, stop: WQ_STOPS.find((s) => s.u === u)?.key ?? null, dir: viewAt(u / 1000).u, vertices: shown.vertices.length, triangles: shown.triangles, quads: shown.quads, others: shown.others, faces: shown.faces.length, edges: EDGES.length, shell: shell.visible } : null),
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the vertex-first shadow. */
export const whiteQueenPreviewPoints = () => shadowAt(0).points;
