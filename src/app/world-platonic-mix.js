// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47, DICTO DOI 10.5281/zenodo.23551326): the "View in app" of the paper.
// Every non-empty mix of the five Platonic solids fills space. Five big letter toggles D I C T O choose the mix (default all five);
// the scene shows a block of that mix's filling: one slab per world, stacked D, C, T/O, I, the solids in their element colours with
// gold edges, the helper pieces (connectors) in muted tones. "Helpers" hides the connectors; a big slider spreads the slabs apart;
// a small list names the helpers the mix uses. Geometry: platonic-mix-geometry.js (ported from the paper's checked study). Words:
// i18n pm.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { WORLDS, PHI, buildMix, helpersOf, isSolid } from './platonic-mix-geometry.js';

// the elements' colours (DICTO): dodecahedron violet, icosahedron blue, cube green, tetrahedron red, octahedron yellow; gold edges
export const SOLID_COLOURS = { D: 0x8a5cc4, I: 0x3a70cd, C: 0x488e48, T: 0xcd3e28, O: 0xe8c852 };
const HELPER_COLOURS = { P: 0x9a937f, Q: 0x9c827a, 'Q′': 0x7d8696, A: 0x6f8199, S: 0x857a96, X: 0x7a7286, Y: 0x9890a6 };
const GOLD = 0xdeb250;
const KEY = { 'Q′': 'Qp' };                              // i18n key of a kind
const GAP = 1.2;                                         // the slabs' extra spacing at Spread 1, in edge lengths
const K = (2 * WS) / ((3 * PHI + 1 + Math.SQRT2 + 1.512 + 3 * GAP) / 2); // one scale for every mix: the whole block, spread, fits
const PRESET = { mix: 'DICTO', helpers: true, spread: 0 };
const lang = () => getSettings().language;
const cleanMix = (m) => WORLDS.filter((w) => String(m).toUpperCase().includes(w)).join('');

/** The pieces of one kind in one slab as one mesh (polygons fanned) and their outlines (edges between non-coplanar faces). */
function kindGeometry(pieces) {
  const tri = [], lines = [];
  const kv = (v) => v.map((x) => x.toFixed(5)).join(',');
  for (const p of pieces) {
    const edges = new Map();
    for (const F of p.faces) {
      for (let i = 1; i + 1 < F.length; i++) tri.push(...F[0], ...F[i], ...F[i + 1]);
      let n = [0, 0, 0];                                 // Newell's normal
      F.forEach((a, i) => { const b = F[(i + 1) % F.length]; n = [n[0] + (a[1] - b[1]) * (a[2] + b[2]), n[1] + (a[2] - b[2]) * (a[0] + b[0]), n[2] + (a[0] - b[0]) * (a[1] + b[1])]; });
      const l = Math.hypot(...n) || 1; n = n.map((x) => x / l);
      F.forEach((a, i) => { const b = F[(i + 1) % F.length], k = [kv(a), kv(b)].sort().join('|'); if (!edges.has(k)) edges.set(k, { a, b, n: [] }); edges.get(k).n.push(n); });
    }
    for (const { a, b, n } of edges.values()) {
      const flat = n.length === 2 && Math.abs(Math.abs(n[0][0] * n[1][0] + n[0][1] * n[1][1] + n[0][2] * n[1][2]) - 1) < 1e-6;
      if (!flat) lines.push(...a, ...b);
    }
  }
  // the study's z is up; the scene's y is up: (x, y, z) → (x, z, −y)
  const turn = (A) => { for (let i = 0; i < A.length; i += 3) { const y = A[i + 1]; A[i + 1] = A[i + 2]; A[i + 2] = -y; } return A; };
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(turn(tri), 3)); g.computeVertexNormals();
  const e = new THREE.BufferGeometry(); e.setAttribute('position', new THREE.Float32BufferAttribute(turn(lines), 3));
  return { g, e };
}

export function createPlatonicMixWorld({ scene, fitView = () => {}, showHudPrompt = () => {} }) {
  const STORAGE_KEY = storageKey('platonicMix');
  const group = new THREE.Group(); group.visible = false; group.scale.setScalar(K); scene.add(group);
  const view = { ...PRESET };
  function read(d) {
    if (!d) return;
    if (typeof d.view?.mix === 'string' && cleanMix(d.view.mix)) view.mix = cleanMix(d.view.mix);
    if (typeof d.view?.helpers === 'boolean') view.helpers = d.view.helpers;
    if (Number.isFinite(d.view?.spread)) view.spread = Math.max(0, Math.min(100, d.view.spread));
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, view: { ...view } });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };

  let active = false, skeleton = false, opacity = 1, built = null, slabGroups = [], drawn = []; // drawn: [{ kind, slab, mesh, line }]
  const mats = {}, lineMats = {};
  const colourOf = (kind) => (isSolid(kind) ? SOLID_COLOURS[kind] : HELPER_COLOURS[kind]);
  function matFor(kind) {
    if (!mats[kind]) {
      mats[kind] = new THREE.MeshStandardMaterial({ color: colourOf(kind), flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: isSolid(kind) ? 0.5 : 0.85 });
      lineMats[kind] = new THREE.LineBasicMaterial({ color: GOLD });
    }
    const m = mats[kind]; m.transparent = opacity < 1; m.opacity = opacity; m.depthWrite = opacity >= 1; m.needsUpdate = true;
    lineMats[kind].color.setHex(skeleton ? colourOf(kind) : isSolid(kind) ? GOLD : 0x4a4640);
    return m;
  }
  function clearGroup() {
    for (const sg of slabGroups) { for (const c of [...sg.children]) c.geometry?.dispose(); group.remove(sg); }
    slabGroups = []; drawn = [];
  }
  function draw() {
    clearGroup();
    if (!active) return;
    built = buildMix(view.mix);
    built.slabs.forEach((slab, i) => {
      const sg = new THREE.Group(); group.add(sg); slabGroups.push(sg);
      const mine = built.pieces.filter((p) => p.slab === i), kinds = [...new Set(mine.map((p) => p.kind))];
      for (const kind of kinds) {
        const { g, e } = kindGeometry(mine.filter((p) => p.kind === kind));
        const mesh = new THREE.Mesh(g, matFor(kind)); mesh.userData = { kind: 'pm', piece: kind };
        const line = new THREE.LineSegments(e, lineMats[kind]);
        sg.add(mesh, line); drawn.push({ kind, slab: i, mesh, line });
      }
    });
    applyVisibility(); applySpread();
  }
  function applyVisibility() {
    for (const d of drawn) {
      const shown = isSolid(d.kind) || view.helpers;
      d.mesh.visible = shown && !skeleton; d.line.visible = shown;
    }
  }
  const height = () => (built ? built.top + (built.slabs.length - 1) * GAP * view.spread / 100 : 0);
  function applySpread() {
    if (!built) return;
    const d = GAP * view.spread / 100, mid = height() / 2;
    slabGroups.forEach((sg, i) => { sg.position.y = i * d - mid; });
  }
  const fit = () => fitView([0, 0, 0], K * Math.max(1.6 * 1.5 * PHI, height() / 2 + 1.5), null, true);

  const pieceName = (kind, L = lang()) => t(`pm.piece.${KEY[kind] ?? kind}`, L);
  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'pm' || mode === 'paint' || mode === 'chisel') return false;
    showHudPrompt(isSolid(ud.piece) ? pieceName(ud.piece) : `${ud.piece} ${pieceName(ud.piece)}`, 2200);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldplatonicmix-panel'; panel.className = 'qc-panel';
  const style = document.createElement('style');
  const hex = (c) => `#${c.toString(16).padStart(6, '0')}`;
  style.textContent = `#worldplatonicmix-panel [hidden]{display:none!important}
#worldplatonicmix-panel .pm-letters{display:flex;gap:8px;justify-content:center}
#worldplatonicmix-panel .pm-letters button{min-width:56px;min-height:56px;font-size:24px;font-weight:700;border-radius:12px;border:3px solid var(--pm-c);background:transparent;color:var(--pm-c);touch-action:manipulation}
#worldplatonicmix-panel .pm-letters button.active{background:var(--pm-c);color:#111;border-color:#deb250}
#worldplatonicmix-panel .pm-helpers{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;font:var(--text-s)/1.4 var(--font-ui);color:#cde}
#worldplatonicmix-panel .pm-helpers span{display:inline-flex;align-items:center;gap:5px}
#worldplatonicmix-panel .pm-helpers i{display:inline-block;width:11px;height:11px;border-radius:2px;border:1px solid #deb250}
#worldplatonicmix-panel .pm-helpers b{color:#deb250}
#worldplatonicmix-panel .pm-spread-row input{width:100%}
#worldplatonicmix-panel .pm-spread-row label{flex:1}`;
  document.head.appendChild(style);
  panel.innerHTML = `
    <div class="w4d-row st-note pm-note"></div>
    <div class="w4d-row pm-letters">${WORLDS.map((w) => `<button type="button" data-pm-world="${w}" style="--pm-c:${hex(SOLID_COLOURS[w])}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options"><button type="button" data-pm="helpers"></button></div>
    <div class="w4d-row pm-helpers"></div>
    <div class="w4d-row pm-spread-row"><label class="hull-pick"><span class="pm-spread-label"></span> <input type="range" class="st-slider" min="0" max="100" step="1"></label></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'platonicMix');
  const slider = panel.querySelector('.pm-spread-row input');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !built) return;
    const L = lang(), used = helpersOf(built.pieces);
    const order = built.slabs.map((s) => (s.world === 'TO' ? ['T', 'O'].filter((x) => view.mix.includes(x)).join('') : s.world)).join(' · ');
    panel.querySelector('.pm-note').textContent = t('pm.note', L, { order, n: built.slabs.length });
    panel.querySelectorAll('[data-pm-world]').forEach((b) => {
      const w = b.dataset.pmWorld, on = view.mix.includes(w);
      b.textContent = w; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on));
      b.title = b.ariaLabel = t(`pm.piece.${w}`, L);
    });
    const hb = panel.querySelector('[data-pm="helpers"]');
    hb.parentElement.hidden = !used.length;          // cubes alone need no helpers: no toggle (nothing unnecessary shown)
    hb.textContent = t(view.helpers ? 'pm.helpers.on' : 'pm.helpers.off', L);
    hb.classList.toggle('active', view.helpers); hb.setAttribute('aria-pressed', String(view.helpers));
    const list = panel.querySelector('.pm-helpers');
    list.hidden = !used.length || !view.helpers;
    list.innerHTML = used.map((k) => `<span><i style="background:${hex(HELPER_COLOURS[k])}"></i><b>${k}</b> ${pieceName(k, L)}</span>`).join('');
    panel.querySelector('.pm-spread-row').hidden = built.slabs.length < 2; // one slab: nothing to spread
    panel.querySelector('.pm-spread-label').textContent = t('pm.spread', L);
    slider.value = String(view.spread);
  }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || !panel.contains(b)) return;
    if (b.dataset.pmWorld) {
      const w = b.dataset.pmWorld, on = view.mix.includes(w);
      if (on && view.mix.length === 1) { showHudPrompt(t('pm.prompt.last', lang()), 2500); return; }
      view.mix = cleanMix(on ? view.mix.replace(w, '') : view.mix + w);
      save(); draw(); renderPanel(); fit();
      return;
    }
    if (b.dataset.pm === 'helpers') { view.helpers = !view.helpers; save(); applyVisibility(); renderPanel(); }
  });
  slider.addEventListener('input', () => { view.spread = Number(slider.value); applySpread(); });
  slider.addEventListener('change', () => { save(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => drawn.filter((d) => d.mesh.visible).map((d) => d.mesh),
    handleTap,
    /** ?open=platonicMix:<letters>, e.g. ?open=platonicMix:DIC. */
    open(arg) {
      const m = cleanMix(arg ?? '');
      if (m) view.mix = m;
      save(); if (active) { draw(); renderPanel(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { clearGroup(); renderPanel(); return; }
      draw(); renderPanel(); fit();
      showHudPrompt(t('pm.prompt.start', lang()), 5000);
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
    probe() {
      return { mix: view.mix, helpers: view.helpers, spread: view.spread, slabs: built?.slabs.map((s) => s.world) ?? [], pieces: built?.pieces.length ?? 0,
        shownKinds: [...new Set(drawn.filter((d) => d.line.visible).map((d) => d.kind))], slabY: slabGroups.map((g) => g.position.y) };
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: a dodecahedron of edge 1. */
export function platonicMixPreviewPoints() {
  const P = [], h = PHI / 2;
  for (const x of [-h, h]) for (const y of [-h, h]) for (const z of [-h, h]) P.push([x, y, z]);
  for (const a of [1, -1]) for (const b of [1, -1]) P.push([0, a / 2, b * PHI * PHI / 2], [b * PHI * PHI / 2, 0, a / 2], [a / 2, b * PHI * PHI / 2, 0]);
  return P;
}
