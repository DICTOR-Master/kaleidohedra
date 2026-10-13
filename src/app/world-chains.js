// Multi-shell chains: a 3D+ world (DICTO 2026-10-13) with DICTO's three published nestings, one at a time: the Chain of Karma (#22,
// doi:10.5281/zenodo.23310541), Spheres of Dharma (#23, doi:10.5281/zenodo.23310833) and the Bodhi Seed (#24,
// doi:10.5281/zenodo.23311353). Each has its views, a slider that pulls the pieces apart and a Crystal switch that makes the
// shells see-through. Geometry: seeds-data.js, built by scripts/build-seeds-data.py from the checked study data.
// Words in all 7 languages (i18n chains.*); DICTO's names stay untranslated.
import * as THREE from 'three';
import CHAINS_DATA from './seeds-data.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const CHAINS_KINDS = ['karma', 'dharma', 'bodhi'];
// Colours as in the papers' figures. Hexagonal caps of the fullerene layer gold (DICTO 2026-10-12).
const ROLE = { ico: 0x5fd38a, cap: 0x5fd38a, lcap: 0x5fd38a, lj11: 0x5fd38a, npyr5: 0x5fd38a, core: 0xffc857, nfru3: 0xffc857, nfru5: 0xffc857,
  axe: 0x4dd0e1, laxe: 0x4dd0e1, nt1: 0x4dd0e1, nedge: 0x4dd0e1, fuji: 0xc792ea, cleo: 0xc792ea, lfuji: 0xc792ea, lcleo: 0xc792ea, npyr3: 0xc792ea,
  nface: 0xc792ea, ncap: 0xc792ea, nwedge: 0xdfe6f0, outer: 0x9fd8ff, copy: 0x5fd38a, centre: 0xffc857, B1: 0xffc857, B4: 0x4dd0e1,
  B5L: 0xc792ea, B5R: 0xf08fc0, B2: 0x4dd0e1, B3: 0xc792ea,
  // DICTO Dodeca
  dodeca: 0xffc857, j63: 0x5fd38a, pyr5: 0xffc857, tet: 0x5fd38a, ipyr5: 0xffc857, itet: 0x5fd38a, wedge: 0x4dd0e1, needle: 0xc792ea, star: 0xc792ea, unit: 0xffc857,
  // The 13s (the neighbours' copies in RD 13's blocks view, N, are dimmer)
  j11: 0x5fd38a, hasu: 0x5fd38a, idd: 0xffc857, vajra: 0xc792ea, rdCentre: 0xffc857, rd: 0x9fb4c8, rdA: 0x5fd38a, rdB: 0x4dd0e1,
  rdCentreN: 0x8a7440, rdAN: 0x3f7a57, rdBN: 0x33808a,
  // DICTO Icosahedral Octet
  admiral: 0x4dd0e1, icoSmall: 0xffc857, weirdstone: 0xc792ea, tadpole: 0xf08fc0, tet: 0xc792ea, frog: 0xf08fc0, pyroUp: 0xffc857,
  pyroDown: 0xc792ea, octGlass: 0x9fd8ff, tetGlass: 0x9fd8ff, lotusJewel: 0x5fd38a, voidDodeca: 0xffc857 };
// Crystal: which roles turn see-through (the shells), per chain.
const CHAINS_GLASS = { karma: new Set(['ico']), dharma: new Set(['core', 'lj11']), bodhi: new Set(['copy']) };
// Always see-through: an outer form, and the octet's cells round the pyrochlore view's tetrahedra.
const ALWAYS_GLASS = new Set(['outer', 'octGlass', 'tetGlass']);
const EDGE_COLOR = 0x0b1220;
const lang = () => getSettings().language;

/** A world of nested shells (Multi-shell chains, DICTO Dodeca): data { kind: { views: { view: [[role, vertices, faces]] } } },
 *  words under '<prefix>.<kind>.<view>' and '<prefix>.note.<kind>'. */
export function createLayeredWorld({ scene, fitView = () => {}, name, data: DATA, kinds: KINDS, glassRoles: GLASS, prefix, defaultParts }) {
  const STORAGE_KEY = storageKey(name);
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // size: for views that grow (a function of the size, DICTO Icosahedral Octet), how far out the network goes.
  const view = { kind: KINDS[0], part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (KINDS.includes(d?.kind)) view.kind = d.kind;
    for (const k of KINDS) if (DATA[k].views[d?.part?.[k]]) view.part[k] = d.part[k];
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1.2, d.apart));
    if (Number.isFinite(d?.shells)) view.shells = Math.max(0, Math.min(1, d.shells));
    view.crystal = d?.crystal === true;
    if (Number.isInteger(d?.size)) view.size = Math.max(1, Math.min(4, d.size));
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false;
  let skeleton = false, opacity = 1; // the app's view modes: Solid, Translucent, Skeleton
  const solid = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.22, depthWrite: false });
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
  }
  // A view is a list of pieces, or a function of the size that builds one (cached per size).
  const grown = new Map();
  const growing = () => typeof DATA[view.kind].views[view.part[view.kind]] === 'function';
  const maxSize = () => DATA[view.kind].maxSize ?? 3;
  function viewList() {
    const v = DATA[view.kind].views[view.part[view.kind]];
    if (typeof v !== 'function') return v;
    const size = Math.min(view.size, maxSize()), key = `${view.kind}.${view.part[view.kind]}.${size}`;
    if (!grown.has(key)) grown.set(key, v(size));
    return grown.get(key);
  }
  const centreOf = (P) => P.reduce((a, p) => a.map((c, i) => c + p[i] / P.length), [0, 0, 0]);
  let radius = 1;
  function draw() {
    clearGroup();
    if (!active) return;
    const list = viewList();
    const all = list.flatMap((p) => p[1]);
    const c0 = centreOf(all);
    radius = Math.max(...all.map((p) => Math.hypot(...p.map((c, i) => c - c0[i]))));
    const buf = { solid: { pos: [], col: [], line: [] }, glass: { pos: [], col: [], line: [] } };
    const colour = new THREE.Color();
    // Shells (DICTO 2026-10-13): pieces grouped by the distance of their centres from the middle; the Top shell slider steps
    // through them, the chosen shell uppermost and every shell outside it lifted away (shown as crystal when Crystal is on).
    const dist = list.map(([, V]) => Math.hypot(...centreOf(V).map((c, i) => c - c0[i])));
    const levels = [...dist].sort((a, b) => a - b).reduce((acc, d) => (acc.length && d - acc[acc.length - 1] < radius * 0.06 ? acc : [...acc, d]), []);
    const shellOf = (d) => levels.reduce((best, l, i) => (Math.abs(l - d) < Math.abs(levels[best] - d) ? i : best), 0);
    list.forEach(([role, V, F], n) => {
      const sh = shellOf(dist[n]); const top = Math.round(view.shells * (levels.length - 1));
      if (sh > top && !ALWAYS_GLASS.has(role) && !view.crystal) return;
      const see = ALWAYS_GLASS.has(role) || (view.crystal && (GLASS[view.kind]?.has(role) || sh > top));
      const b = see ? buf.glass : buf.solid;
      // Pulled apart: each piece moves out along the line from the centre through its own centre; see-through shells stay put.
      const off = see ? [0, 0, 0] : centreOf(V).map((c, i) => (c - c0[i]) * view.apart);
      const P = V.map((p) => p.map((c, i) => (c - c0[i] + off[i]) * WS));
      colour.setHex(role === 'ncap' && V.length === 7 ? 0xffc857 : (ROLE[role] ?? 0xb8c4bd));
      for (const f of F) {
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { b.pos.push(...P[k]); b.col.push(colour.r, colour.g, colour.b); }
        f.forEach((k, i) => b.line.push(...P[k], ...P[f[(i + 1) % f.length]]));
      }
    });
    solid.transparent = opacity < 1; solid.opacity = opacity; solid.depthWrite = opacity >= 1; solid.needsUpdate = true;
    for (const [key, mat] of [['solid', solid], ['glass', glass]]) {
      const b = buf[key];
      if (!b.line.length) continue;
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(b.pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(b.col, 3));
      g.computeVertexNormals();
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(b.line, 3));
      if (!skeleton) group.add(new THREE.Mesh(g, mat));
      group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial(key === 'glass' ? { color: 0x9fa8c0, transparent: true, opacity: 0.55 } : { color: skeleton ? 0xcfe3ff : EDGE_COLOR })));
    }
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], radius * (1 + view.apart) * WS * 1.1);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = `world${name}-panel`;
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="ch-view-label"></span> <select class="hull-select" data-select="part"></select></label></div>
    <div class="w4d-row ch-size-row"><label class="hull-pick"><span class="ch-size-label"></span> <input type="range" class="st-slider" min="1" max="3" step="1"></label></div>
    <div class="w4d-row ch-apart-row"><label class="hull-pick"><span class="ch-apart-label"></span> <input type="range" class="st-slider" min="0" max="1200" step="1"></label></div>
    <div class="w4d-row ch-shells-row"><label class="hull-pick"><span class="ch-shells-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row w4d-options"><button type="button" data-chains-crystal></button></div>
    <div class="w4d-row st-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, name);
  const partSelect = panel.querySelector('[data-select="part"]');
  const apartInput = panel.querySelector('.ch-apart-row input');
  const crystalBtn = panel.querySelector('[data-chains-crystal]');
  const shellsInput = panel.querySelector('.ch-shells-row input');
  const sizeInput = panel.querySelector('.ch-size-row input');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.ch-view-label').textContent = t('icosa.view', L);
    partSelect.innerHTML = Object.keys(DATA[view.kind].views)
      .map((v) => `<option value="${v}"${v === view.part[view.kind] ? ' selected' : ''}>${t(`${prefix}.${view.kind}.${v}`, L)}</option>`).join('');
    panel.querySelector('.ch-size-row').hidden = !growing();
    panel.querySelector('.ch-size-label').textContent = t('chains.size', L);
    sizeInput.max = String(maxSize()); sizeInput.value = String(Math.min(view.size, maxSize()));
    panel.querySelector('.ch-apart-label').textContent = t('icosa.apart', L);
    apartInput.value = String(Math.round(view.apart * 1000));
    panel.querySelector('.ch-shells-label').textContent = t('chains.shells', L);
    shellsInput.value = String(Math.round(view.shells * 1000));
    crystalBtn.textContent = t(view.crystal ? 'chains.crystal.on' : 'chains.crystal.off', L);
    panel.querySelector('.st-note').textContent = t(`${prefix}.note.${view.kind}`, L);
  }
  partSelect.addEventListener('change', () => { if (!DATA[view.kind].views[partSelect.value]) return; view.part[view.kind] = partSelect.value; save(); draw(); fit(); });
  apartInput.addEventListener('input', () => { view.apart = Number(apartInput.value) / 1000; save(); draw(); });
  apartInput.addEventListener('change', fit);
  shellsInput.addEventListener('input', () => { view.shells = Number(shellsInput.value) / 1000; save(); draw(); });
  shellsInput.addEventListener('change', fit);
  sizeInput.addEventListener('input', () => { view.size = Number(sizeInput.value); save(); draw(); fit(); });
  crystalBtn.addEventListener('click', () => { view.crystal = !view.crystal; save(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** Which of the world's shapes to show (the menu entries); anything else keeps the current one. */
    setChain(kind) {
      if (!KINDS.includes(kind) || kind === view.kind) return;
      view.kind = kind; save();
      if (active) { draw(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) panel.classList.remove('visible');
      draw();
      if (on) fit();
    },
    /** Back to each shape's first view (leaving the world, DICTO 2026-10-13). */
    resetView() {
      Object.assign(view, { part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2 }); save();
      if (active) { draw(); fit(); }
    },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
  };
}

export function createChainsWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'chains', data: CHAINS_DATA, kinds: CHAINS_KINDS, glassRoles: CHAINS_GLASS, prefix: 'chains',
    defaultParts: { karma: 'lotus', dharma: 'cycle', bodhi: 'seed' } });
}

/** Points whose convex hull previews a chain in the DICTO menu (its first view's outline). */
export function chainPreviewPoints(kind) {
  const views = CHAINS_DATA[kind]?.views;
  return views ? Object.values(views)[0].flatMap((p) => p[1]) : [];
}
