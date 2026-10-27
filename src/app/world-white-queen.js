// The White Queen 600-cell (DICTO 2026-10-27): the companion world of paper #63, "The White Queen 600-cell" (DOI not yet assigned).
// Step 2, the shadows: the true orthogonal 3D shadow of the 600-cell, every one computed live from the exact source model
// (white-queen-data.js via white-queen-geometry.js; no other 600-cell code). All 720 edges are drawn projected (the inner ones too),
// the convex hull as a see-through shell, its real faces (coplanar triangles merged) ivory for triangles and blue for four-sided faces,
// as in #63's figures. Six turnings (DICTO 2026-10-27), one for each pair of the four main directions: two rows of four buttons pick
// the start (From) and the end (To), each jumping to its stop, and one big slider turns the 4D view direction along that pair's great
// circle, snapping at both ends; the caption gives the hull's vertices and faces. The Slice view (W3): one row of four directions and
// one big slider from the centre to the tip that stops only at #63's slice patterns (every vertex height and the exact midpoint of
// every gap), each slice computed live; the tips drawn small. Named stops in gold (W4, DICTO's names): Humpty Dumpty, the real
// 48-vertex cell-first slice at 1 + √5/2 (shown larger, solid ivory with gold edges, turning slowly until touched), and Shadow-17,
// the edge-first slice at 1 + √5. Words in all 7 languages (i18n wq.*).
import * as THREE from 'three';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DIRECTIONS, EDGES, shadowAt, viewAt, SLICE_STOPS, sliceAt } from './white-queen-geometry.js';

export const WQ_DIRECTIONS = DIRECTIONS;
/** The slider: 0..1000 along the chosen turning, its two ends the stops (it snaps to one within WQ_SNAP). */
export const WQ_SNAP = 40;
export const WQ_DEFAULT = { from: 'vertex-first', to: 'cell-first' };
export const WQ_MODES = ['shadow', 'slice'];
/** DICTO's named slices (gold captions): direction and exact height. */
export const WQ_NAMED = [{ key: 'humpty', dir: 'cell-first', height: '1 + 1/2√5' }, { key: 'shadow17', dir: 'edge-first', height: '1 + √5' }];
const namedAt = (dir, height) => WQ_NAMED.find((x) => x.dir === dir && x.height === height) ?? null;
/** A slice stop's place on its slider (0..1000, by height from the centre to the tip). */
export const sliceU = (dir, k) => { const S = SLICE_STOPS[DIRECTIONS.indexOf(dir)]; return Math.round((1000 * S[k].value) / S[S.length - 1].value); };
const faceSizes = (faces) => faces.reduce((m, f) => ({ ...m, [f.length]: (m[f.length] ?? 0) + 1 }), {});
/** The slice caption: [name ·] direction · height h · at a vertex height | between heights · counts (or what the tip is). */
export function wqSliceCaption(dir, k, L) {
  const s = sliceAt(dir, k), st = s.stop, nm = namedAt(dir, st.height);
  const parts = [t(`wq.dir.${dir}`, L), t('wq.slice.height', L, { h: st.height }), t(st.atVertex ? 'wq.slice.at' : 'wq.slice.between', L)];
  if (s.dim === 3) {
    const fs = faceSizes(s.faces);
    parts.push(t('wq.count.vertices', L, { n: s.vertices.length }), t('wq.count.triangles', L, { n: fs[3] ?? 0 }));
    if (fs[4]) parts.push(t('wq.count.quads', L, { n: fs[4] }));
  }
  if (st.tip) parts.push(t(`wq.tip.${s.dim}`, L));
  return `${nm ? `${t(`wq.name.${nm.key}`, L)} · ` : ''}${parts.join(' · ')}`;
}
const SHORT = { vertex: 'vertex-first', edge: 'edge-first', face: 'face-first', cell: 'cell-first' };   // ?open=whitequeen:<short>
const IVORY = 0xefe9dc, BLUE = 0x9fb4c8, OTHER = 0xd8c690;   // as #63's figures (render_atlas.py); faces of 5+ sides never show at the stops
const SHELL = 0.42;   // the see-through shell's opacity
const GOLD = 0xffc857, SLICE_EDGE = 0x4a505c, HUMPTY_SCALE = 1.3;   // Humpty Dumpty: gold edges, a bit larger
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
  // the view: Shadow (the turning from → to, the slider's place u) or Slice (a direction and its stop k)
  const view = { mode: 'shadow', ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (WQ_MODES.includes(d?.mode)) view.mode = d.mode;
    if (DIRECTIONS.includes(d?.from) && DIRECTIONS.includes(d?.to) && d.from !== d.to) Object.assign(view, { from: d.from, to: d.to });
    if (Number.isFinite(d?.u)) view.u = Math.max(0, Math.min(1000, Math.round(d.u)));
    if (DIRECTIONS.includes(d?.sliceDir)) view.sliceDir = d.sliceDir;
    if (Number.isInteger(d?.sliceK)) view.sliceK = Math.max(0, Math.min(SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length - 1, d.sliceK));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;

  // ---- the Shadow view ----
  const shadowGroup = new THREE.Group();
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
  shadowGroup.add(inner, shell, hullLines);
  for (const o of [inner, shell, hullLines]) o.frustumCulled = false;

  // ---- the Slice view: rebuilt per stop, in its own turning group (Humpty Dumpty turns) ----
  const sliceGroup = new THREE.Group(), spin = new THREE.Group();
  sliceGroup.add(spin);
  group.add(shadowGroup, sliceGroup);
  const sliceMat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, roughness: 0.55, metalness: 0, emissive: 0x2a2824, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const dotGeo = new THREE.SphereGeometry(1, 16, 12);
  let humpty = false, spinStopped = false;
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clearSpin() {
    for (const c of [...spin.children]) { spin.remove(c); if (c.geometry !== dotGeo) c.geometry.dispose(); if (c.material !== sliceMat) c.material.dispose(); }
  }
  function drawShadow() {
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
  }
  function drawSlice() {
    clearSpin();
    const s = sliceAt(view.sliceDir, view.sliceK), nm = namedAt(view.sliceDir, s.stop.height);
    shown = s;
    const wasHumpty = humpty;
    humpty = nm?.key === 'humpty';
    if (humpty && !wasHumpty) spinStopped = false;   // arriving at Humpty Dumpty: he turns again
    if (!humpty) spin.rotation.set(0, 0, 0);
    const scale = WS * (humpty ? HUMPTY_SCALE : 1), Q = s.points.map((p) => p.map((c) => c * scale));
    const edgeHex = humpty ? GOLD : skeleton ? 0xdfe6f0 : SLICE_EDGE;
    const lines = [];
    if (s.dim === 3) {
      const pos = [], col = [], c = new THREE.Color();
      for (const f of s.faces) {
        c.setHex(f.length === 3 ? IVORY : f.length === 4 ? BLUE : OTHER);
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { pos.push(...Q[k]); col.push(c.r, c.g, c.b); }
        f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (k < l) lines.push(...Q[k], ...Q[l]); });
      }
      if (!skeleton) {
        const g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
        g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
        g.computeVertexNormals();
        sliceMat.transparent = opacity < 1 && !humpty; sliceMat.opacity = humpty ? 1 : opacity; sliceMat.depthWrite = !sliceMat.transparent; sliceMat.needsUpdate = true;
        spin.add(new THREE.Mesh(g, sliceMat));
      }
    } else {
      // a tip: a point, an edge or a triangle, drawn small but visible (dots at its corners)
      const r = 0.045 * WS;
      for (const p of Q) { const m = new THREE.Mesh(dotGeo, new THREE.MeshStandardMaterial({ color: IVORY, emissive: 0x2a2824 })); m.scale.setScalar(r); m.position.fromArray(p); spin.add(m); }
      Q.forEach((p, i) => Q.slice(i + 1).forEach((q) => lines.push(...p, ...q)));
      if (s.dim === 2 && !skeleton) {
        const g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.Float32BufferAttribute(Q.slice(0, 3).flat(), 3));
        g.computeVertexNormals();
        spin.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: IVORY, side: THREE.DoubleSide, emissive: 0x2a2824 })));
      }
    }
    if (lines.length) {
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
      spin.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: s.dim < 3 ? IVORY : edgeHex })));
    }
    for (const o of spin.children) o.frustumCulled = false;
    tickSpin();
  }
  // Humpty Dumpty turns slowly on his own while the slider rests on him, until the picture is touched (not with reduced motion)
  let raf = 0;
  function tickSpin() {
    if (raf) return;
    const step = () => {
      raf = 0;
      if (!active || view.mode !== 'slice' || !humpty || spinStopped || reduceMotion()) return;
      spin.rotation.y += 0.004;
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  }
  document.addEventListener('pointerdown', (e) => { if (active && humpty && e.target?.tagName === 'CANVAS') spinStopped = true; });

  function draw() {
    if (!active) return;
    shadowGroup.visible = view.mode === 'shadow';
    sliceGroup.visible = view.mode === 'slice';
    if (view.mode === 'shadow') { humpty = false; clearSpin(); drawShadow(); } else drawSlice();
    renderPanel();
  }
  const R = 2 * WS;   // the 600-cell's circumradius: every shadow and slice fits inside it
  const fit = () => fitView([0, 0, 0], R * 1.12, [0.3, 0.25, 1]);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldwhiteQueen-panel';
  panel.className = 'qc-panel';
  const row = (end, label = true) => `<div class="w4d-row w4d-options wq-row" data-wq-row="${end}">${label ? `<span class="hull-pick wq-row-label" data-wq-label="${end}"></span>` : ''}${DIRECTIONS.map((k) => `<button type="button" data-wq-${end}="${k}"></button>`).join('')}</div>`;
  panel.innerHTML = `
    <div class="w4d-row w4d-options wq-modes">${WQ_MODES.map((m) => `<button type="button" data-wq-mode="${m}"></button>`).join('')}</div>
    ${row('from')}
    ${row('to')}
    ${row('slice', false)}
    <div class="w4d-row wq-param-row"><label class="hull-pick"><span class="wq-param-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row wq-slice-row"><label class="hull-pick"><span class="wq-slice-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'whiteQueen');
  const input = panel.querySelector('.wq-param-row input'), sliceInput = panel.querySelector('.wq-slice-row input');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note');
  note.addEventListener('click', () => note.classList.toggle('open'));
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), shadow = view.mode === 'shadow';
    panel.querySelectorAll('[data-wq-mode]').forEach((x) => { x.textContent = t(`wq.view.${x.dataset.wqMode}`, L); x.classList.toggle('active', x.dataset.wqMode === view.mode); });
    // nothing unnecessary shown: each view only its own rows
    panel.querySelector('[data-wq-row="from"]').hidden = panel.querySelector('[data-wq-row="to"]').hidden = panel.querySelector('.wq-param-row').hidden = !shadow;
    panel.querySelector('[data-wq-row="slice"]').hidden = panel.querySelector('.wq-slice-row').hidden = shadow;
    for (const end of ['from', 'to', 'slice']) {
      const lab = panel.querySelector(`[data-wq-label="${end}"]`);
      if (lab) lab.textContent = t(`wq.${end}`, L);
      panel.querySelectorAll(`[data-wq-${end}]`).forEach((x) => {
        const k = x.getAttribute(`data-wq-${end}`);
        x.textContent = t(`wq.btn.${k}`, L);
        x.title = t(`wq.dir.${k}`, L);
        x.classList.toggle('active', k === (end === 'slice' ? view.sliceDir : view[end]));
        x.hidden = end === 'to' && k === view.from;   // a direction does not turn to itself: nothing unnecessary shown
      });
    }
    const nm = shadow ? null : namedAt(view.sliceDir, shown.stop.height);
    caption.classList.toggle('wq-gold', !!nm);
    if (shadow) {
      panel.querySelector('.wq-param-label').textContent = t('wq.param', L, { a: t(`wq.dir.${view.from}`, L), b: t(`wq.dir.${view.to}`, L) });
      input.value = String(view.u);
      caption.textContent = wqCaption(view, shown, L);
      note.textContent = t('wq.note', L);
    } else {
      panel.querySelector('.wq-slice-label').textContent = t('wq.slice.param', L, { d: t(`wq.dir.${view.sliceDir}`, L) });
      sliceInput.value = String(sliceU(view.sliceDir, view.sliceK));
      caption.textContent = wqSliceCaption(view.sliceDir, view.sliceK, L);
      note.textContent = t('wq.note.slice', L);
    }
  }
  const go = (v) => { if (v === view.u) return; view.u = v; save(); draw(); };
  input.addEventListener('input', () => {
    let v = Number(input.value);
    if (v <= WQ_SNAP) v = 0; else if (v >= 1000 - WQ_SNAP) v = 1000;
    input.value = String(v);
    go(v);
  });
  // the slice slider stops only at the atlas's stops: the nearest one
  sliceInput.addEventListener('input', () => {
    const v = Number(sliceInput.value), S = SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)];
    let k = 0;
    S.forEach((_, i) => { if (Math.abs(sliceU(view.sliceDir, i) - v) < Math.abs(sliceU(view.sliceDir, k) - v)) k = i; });
    sliceInput.value = String(sliceU(view.sliceDir, k));
    if (k === view.sliceK) return;
    view.sliceK = k; save(); draw();
  });
  // From: the turning starts there (the slider at its start); To: it ends there (the slider at its end). Picking as From the
  // direction that is To swaps the two. Slice: the direction, from its centre.
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('[data-wq-from], [data-wq-to], [data-wq-slice], [data-wq-mode]');
    if (!b) return;
    const { wqFrom: from, wqTo: to, wqSlice: sl, wqMode: mode } = b.dataset;
    if (mode) { if (mode === view.mode) return; view.mode = mode; }
    else if (from) { if (from === view.to) view.to = view.from; view.from = from; view.u = 0; }
    else if (to && to !== view.from) { view.to = to; view.u = 1000; }
    else if (sl) { if (sl === view.sliceDir) return; view.sliceDir = sl; view.sliceK = 0; }
    else return;
    save(); draw();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=whitequeen:<vertex|edge|face|cell>: the Shadow view at that main direction (turning to cell-first, or vertex-first from
     *  cell-first); ?open=whitequeen:slice the Slice view; ?open=whitequeen:humpty the Slice view at Humpty Dumpty. */
    setChain(kind) {
      const k = SHORT[kind] ?? kind;
      if (kind === 'slice') view.mode = 'slice';
      else if (kind === 'humpty') {
        const n = DIRECTIONS.indexOf('cell-first');
        Object.assign(view, { mode: 'slice', sliceDir: 'cell-first', sliceK: SLICE_STOPS[n].findIndex((s) => s.height === WQ_NAMED[0].height) });
      } else if (DIRECTIONS.includes(k)) Object.assign(view, { mode: 'shadow', from: k, to: k === WQ_DEFAULT.to ? WQ_DEFAULT.from : WQ_DEFAULT.to, u: 0 });
      else return;
      save();
      if (active) draw();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      draw(); fit();
    },
    resetView() { Object.assign(view, { mode: 'shadow', ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0 }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, and in it what is shown and its counts. */
    probe: () => {
      if (!shown) return null;
      if (view.mode === 'slice') {
        const s = shown, nm = namedAt(view.sliceDir, s.stop.height);
        return { mode: 'slice', dir: view.sliceDir, k: view.sliceK, stops: SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length, height: s.stop.height, atVertex: s.stop.atVertex, tip: s.stop.tip, dim: s.dim,
          V: s.dim === 3 ? s.vertices.length : s.points.length, faceSizes: s.dim === 3 ? faceSizes(s.faces) : null, named: nm?.key ?? null, humpty, spinning: !!raf, spinAngle: spin.rotation.y };
      }
      return { mode: 'shadow', from: view.from, to: view.to, u: view.u, stop: view.u === 0 ? view.from : view.u === 1000 ? view.to : null, dir: viewAt(view.from, view.to, view.u / 1000).u, vertices: shown.vertices.length, triangles: shown.triangles, quads: shown.quads, others: shown.others, faces: shown.faces.length, edges: EDGES.length, shell: shell.visible };
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the vertex-first shadow. */
export const whiteQueenPreviewPoints = () => shadowAt(0, 0, 0).points;
