// The Star Cores world (DICTO 2026-11-02; DICTO's Star Cores papers #79–#81 and the Star Cores book): any of the 52 convex Star
// Cores shapes (all in Polyhedraverse's catalogue, krp-core star-cores-shapes.js STAR_CORES_LIST) given the star core treatment one
// step at a time on a slider: the solid, its star (every face's pyramid from the centre turned outwards, tip t × the foot, t = 2 or
// φ), the halo (the hull of the tips, see-through), the core of the turn (the common part of the face families' tip hulls), and on
// through the chain, each core scaled back to the solid's size as the next solid. Helpers (the star, at the core) are coloured glass,
// DICTO's standing rule for constructions. The geometry is star-cores-geometry.js (on star-step-geometry.js, Polyhedraverse's ★ Star
// step); drawn to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, crisp screen-space edges ≥ 1.5 px.
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { POLYHEDRA, STAR_CORES_LIST } from '../krp-core/src/polyhedra/index.js';
import { starCoresChain, positionsOf, phaseAt, sameShape, findStarCoresShape, starCounts } from './star-cores-geometry.js';

const SOLID = 0xd9a520, SPIKE = 0x8f5bd8, CORE = 0x2bb7c4, HALO = 0xcfe0ff;
const EDGE = 0x0b1220, HALO_EDGE = 0xe8eefc;
const HALO_GLASS = 0.24, HELPER_GLASS = 0.3;
const DEFAULT_SHAPE = 'D109';
const lang = () => getSettings().language;
const specOf = (s) => POLYHEDRA[s.id];

export function createStarCoresWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('star-cores-world');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { shape: DEFAULT_SHAPE, t: '2', pos: 0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (typeof d?.shape === 'string') view.shape = d.shape;
    if (d?.t === '2' || d?.t === 'phi') view.t = d.t;
    if (Number.isInteger(d?.pos) && d.pos >= 0) view.pos = d.pos;
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shapes = STAR_CORES_LIST, chain = null, chainKey = '', radius = 1;

  const solidMat = (color) => new THREE.MeshStandardMaterial({ color, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5, metalness: 0.1 });
  const glassMat = (color, o) => { const m = new THREE.MeshStandardMaterial({ color, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: o, depthWrite: false, roughness: 0.4 }); m.userData.hollow = true; return m; };
  const mats = { solid: solidMat(SOLID), spike: solidMat(SPIKE), core: solidMat(CORE), halo: glassMat(HALO, HALO_GLASS), spikeGlass: glassMat(SPIKE, HELPER_GLASS), solidGlass: glassMat(SOLID, HELPER_GLASS) };
  const lineMats = [];
  function clear() {
    for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); }
    lineMats.splice(0).forEach((m) => m.dispose());
  }
  const fan = (loop) => loop.slice(1, -1).map((_, i) => [loop[0], loop[i + 1], loop[i + 2]]);
  function mesh(tris, material, order = 0) {
    if (skeleton || !tris.length) return;
    const pos = new Float32Array(tris.length * 9);
    tris.forEach((tr, i) => tr.forEach((p, k) => pos.set(p, i * 9 + k * 3)));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, material);
    m.renderOrder = order;
    group.add(m);
  }
  function lines(segs, color, width = 2, order = 0, o = 1) {
    if (!segs.length) return;
    const g = new LineSegmentsGeometry();
    g.setPositions(segs.flatMap(([a, b]) => [...a, ...b]));
    const m = new LineMaterial({ color, linewidth: width, transparent: o < 1, opacity: o, depthWrite: o >= 1 });
    lineMats.push(m);
    const l = new LineSegments2(g, m);
    l.frustumCulled = false;
    l.renderOrder = order;
    group.add(l);
  }
  const faceTris = (S) => S.faces.flatMap((f) => fan(f.map((k) => S.vertices[k])));
  const edgeSegs = (S) => { const seen = new Set(), out = []; for (const f of S.faces) f.forEach((a, i) => { const b = f[(i + 1) % f.length], k = a < b ? `${a},${b}` : `${b},${a}`; if (!seen.has(k)) { seen.add(k); out.push([S.vertices[a], S.vertices[b]]); } }); return out; };
  const spikeTris = (solid, tips) => solid.faces.flatMap((f, fi) => f.map((k, i) => [solid.vertices[k], solid.vertices[f[(i + 1) % f.length]], tips[fi]]));
  const spikeSegs = (solid, tips) => solid.faces.flatMap((f, fi) => f.map((k) => [solid.vertices[k], tips[fi]]));
  const far = (P) => Math.max(...P.map((p) => Math.hypot(...p)));

  function setLook() {
    const see = opacity < 1;
    for (const m of [mats.solid, mats.spike, mats.core]) { m.transparent = see; m.opacity = see ? opacity : 1; m.depthWrite = !see; m.needsUpdate = true; }
  }
  function draw() {
    clear();
    if (!active || !chain) return;
    setLook();
    const { turn, phase } = phaseAt(view.pos), T = chain.turns[turn];
    const { solid, step } = T, line = skeleton ? 0xffffff : EDGE;
    if (phase === 'core') {
      // the core solid, the star round it as coloured glass (a helper), the halo's outline
      mesh(faceTris(T.core), mats.core, 2);
      lines(edgeSegs(T.core), line, 2, 2);
      mesh(spikeTris(solid, step.tips), mats.spikeGlass, 3);
      mesh(faceTris(solid), mats.solidGlass, 3);
      lines([...edgeSegs(solid), ...spikeSegs(solid, step.tips)], SPIKE, 1.5, 3, 0.55);
      lines(edgeSegs(step.halo), skeleton ? 0xffffff : HALO_EDGE, 1.5, 4, 0.8);
    } else {
      mesh(faceTris(solid), mats.solid);
      const segs = edgeSegs(solid);
      if (phase !== 'solid') { mesh(spikeTris(solid, step.tips), mats.spike); segs.push(...spikeSegs(solid, step.tips)); }
      lines(segs, line, 2);
      if (phase === 'halo') {
        mesh(faceTris(step.halo), mats.halo, 3);
        lines(edgeSegs(step.halo), skeleton ? 0xffffff : HALO_EDGE, 2, 4);
      }
    }
    radius = Math.max(far(step.halo.vertices), far(solid.vertices), T.core ? far(T.core.vertices) : 0);
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], radius, [1, 0.45, 1.3]);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldstarCores-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="sc-shape-label"></span> <select class="hull-select" data-sc-shape></select></label></div>
    <div class="w4d-row w4d-options sc-ts"><button type="button" data-sc-t="2"></button><button type="button" data-sc-t="phi"></button></div>
    <div class="w4d-row sc-step-row"><label class="hull-pick"><span class="sc-step-label"></span> <input type="range" class="st-slider" data-sc-step min="0" max="1" step="1" value="0"></label></div>
    <div class="w4d-row ch-param-caption sc-caption" aria-live="polite"></div>
    <div class="w4d-row st-note sc-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'starCores');
  const select = panel.querySelector('[data-sc-shape]'), slider = panel.querySelector('[data-sc-step]');
  // the long note folded to one line, so the solid keeps the screen on a phone; a tap opens it (as in the Chains world)
  panel.querySelector('.sc-note').addEventListener('click', (e) => e.currentTarget.classList.toggle('open'));
  let listed = '';
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.sc-shape-label').textContent = t('sc.shape', L);
    if (listed !== L) {
      listed = L;
      select.innerHTML = shapes.map((s) => `<option value="${s.D}">${s.D} · ${s.name}</option>`).join('');
    }
    select.value = view.shape;
    panel.querySelectorAll('[data-sc-t]').forEach((b) => { const on = b.dataset.scT === view.t; b.textContent = t(`sc.t.${b.dataset.scT}`, L); b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    panel.querySelector('.sc-step-label').textContent = t('sc.step', L);
    const max = positionsOf(chain);
    slider.max = String(max);
    slider.value = String(view.pos);
    // the slider only when there is a chain to step through
    panel.querySelector('.sc-step-row').hidden = !chain;
    panel.querySelector('.sc-caption').textContent = caption(L);
    panel.querySelector('.sc-note').textContent = t(chain ? 'sc.note' : 'sc.notConvex', L);
  }
  function caption(L) {
    if (!chain) return '';
    const { turn, phase } = phaseAt(view.pos), T = chain.turns[turn];
    // the counts of what the step shows: the solid, the star itself (solid + spikes), the halo, the core
    const c = phase === 'star' ? starCounts(T.solid, T.step.tips) : (({ vertices, faces }) => ({ v: vertices.length, f: faces.length }))(phase === 'core' ? T.core : phase === 'halo' ? T.step.halo : T.solid);
    const parts = [t('sc.turn', L, { n: turn + 1 }), t(`sc.phase.${phase}`, L), t('sc.counts', L, c)];
    if (phase === 'core') {
      if (sameShape(T.core, T.solid)) parts.push(t('sc.period1', L));
      else if (turn >= 1 && sameShape(T.core, chain.turns[turn - 1].solid)) parts.push(t('sc.period2', L, { n: turn }));
    }
    if (phase === 'halo' && view.pos === positionsOf(chain)) parts.push(t('sc.noCore', L));
    return parts.join(' · ');
  }
  function rebuild() {
    const s = findStarCoresShape(shapes, view.shape) ?? findStarCoresShape(shapes, DEFAULT_SHAPE);
    view.shape = s.D;
    const key = `${s.D}|${view.t}`;
    if (key !== chainKey) { chain = starCoresChain(specOf(s), view.t); chainKey = key; }
    view.pos = Math.min(view.pos, positionsOf(chain));
  }
  function show(refit = true) {
    rebuild();
    if (!active) return;
    draw();
    if (!chain) renderPanel();
    if (refit) fit();
  }
  select.addEventListener('change', () => { view.shape = select.value; view.pos = 0; save(); show(); });
  panel.querySelector('.sc-ts').addEventListener('click', (e) => { const k = e.target.closest('[data-sc-t]')?.dataset.scT; if (k && k !== view.t) { view.t = k; save(); show(); } });
  slider.addEventListener('input', () => { const p = Number(slider.value); if (p !== view.pos) { view.pos = p; save(); show(false); } });
  slider.addEventListener('change', () => fit());
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=starcores:<D-number or key>[:<2|phi>[:<step>]] and tool:starCoresWorld:<the same>: that shape, t and slider position. */
    setChain(arg) {
      const [id, tk, k] = String(arg).split(':');
      if (id) view.shape = id;
      if (tk === '2' || tk?.toLowerCase() === 'phi') view.t = tk.toLowerCase();
      view.pos = Number.isInteger(Number(k)) && Number(k) >= 0 ? Number(k) : 0;
      save();
      if (active) show();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); clear(); return; }
      renderPanel();
      show();
    },
    resetView() { Object.assign(view, { shape: DEFAULT_SHAPE, t: '2', pos: 0 }); save(); if (active) show(); },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the shape, t, slider position and what is drawn. */
    probe() {
      if (!chain) return { shape: view.shape, t: view.t, pos: view.pos, chain: false };
      const { turn, phase } = phaseAt(view.pos), T = chain.turns[turn];
      return { shape: view.shape, t: view.t, pos: view.pos, max: positionsOf(chain), chain: true, turn, phase, turns: chain.turns.length,
        corners: T.solid.vertices.length, faces: T.solid.faces.length, star: starCounts(T.solid, T.step.tips), haloCorners: T.step.halo.vertices.length, core: T.core ? { corners: T.core.vertices.length, faces: T.core.faces.length } : null,
        glass: group.children.filter((c) => c.isMesh && c.material.transparent && c.material.userData.hollow).length, meshes: group.children.filter((c) => c.isMesh).length,
        lineWidths: lineMats.map((m) => m.linewidth), radius };
    },
  };
}
