// OCD Stella Crystals (DICTO 2026-10-16): the DICTO OCD Stella, the stella cut of the Ogdoecontahedron's companion solid, on one network
// of the OCD's bcc packing, and a partner on the other network, swapped with one switch:
//   icosahedra   the OCD's 20 hexagon planes; every solid meets its 8 joint neighbours face to face; fill 1523/32 − 669√5/32 ≈ 84.60%;
//   octahedra    the regular octahedron of the cell's 8 joint planes; its 6 tips nest in OCD Stellas, each notched by 6; ≈ 96.33% (float);
//   alone        OCD Stellas on both networks, the plain bcc packing; fill 151/2 − 267√5/8 ≈ 87.12%.
// With icosahedra or octahedra the crystal is Fd-3 (No. 203), both solids on sites of symmetry 23: the same crystal with the partner
// swapped. Grow builds it joint step by joint step from one OCD Stella; Gap shows the exact pass's 4 kinds of convex gap piece
// (icosahedra and alone), Notches turns the OCD Stellas to glass to show the octahedron tips in them. The app's X-ray cuts it open.
// Data: scripts/build-ocd-stella-data.py (loads on entry, released on leaving). Words: i18n os.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const PARTNERS = ['ico', 'octa', 'alone'];
const PRESET = { partner: 'ico', layers: 2, gap: false, notch: false };
const COLOUR = { stella: 0xe8b84a, notched: 0xe8b84a, ico: 0x4dd0e1, octa: 0x9575cd };
const GAP_COLOUR = [0x1e88e5, 0x26a69a, 0xc792ea, 0xef6c8f]; // icosahedron wedge, OCD Stella cap, slab, thin wedge
const GAP_COUNT = [12, 12, 6, 24];
const FILL = { ico: '84.60%', octa: '96.33%', alone: '87.12%' };
const GROUP = { ico: 'Fd-3 (No. 203)', octa: 'Fd-3 (No. 203)', alone: 'Im-3 (No. 204)' };
const lang = () => getSettings().language;

export function createOcdStellaWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('ocdstella');
  const group = new THREE.Group(); group.visible = false; group.scale.setScalar(WS); scene.add(group);
  const view = { ...PRESET };
  function read(d) {
    if (!d || typeof d !== 'object') return;
    if (PARTNERS.includes(d.partner)) view.partner = d.partner;
    if (Number.isInteger(d.layers) && d.layers >= 0 && d.layers <= 4) view.layers = d.layers;
    for (const k of ['gap', 'notch']) if (typeof d[k] === 'boolean') view[k] = d[k];
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, ...view });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, pickTargets = [];
  const load = () => (loading ??= import('./ocd-stella-data.js').then((m) => { DATA = m.default; }));
  const gapShown = () => view.gap && view.partner !== 'octa';
  const notchShown = () => view.notch && view.partner === 'octa';

  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry?.dispose(); child.material?.dispose(); }
    pickTargets = [];
  }
  // the solid at a site: network 1 always an OCD Stella (notched beside octahedra), network 2 the partner
  const solidAt = (net) => (net === 1 ? (view.partner === 'octa' ? 'notched' : 'stella') : view.partner === 'alone' ? 'stella' : view.partner);
  const shownSites = () => DATA.sites.filter((s) => s[4] <= view.layers);
  // one merged mesh (and its edges) per kind of solid; per triangle the site it belongs to, for taps
  function addMerged(S, offsets, colour, glass, userData) {
    const pos = [], edges = [], tri = [];
    const edgeList = S.e ?? S.f.flatMap((f) => f.map((a, k) => [a, f[(k + 1) % f.length]]));
    offsets.forEach((o, i) => {
      const V = S.v.map((v) => [v[0] + o[0], v[1] + o[1], v[2] + o[2]]);
      for (const f of S.f) for (let k = 1; k + 1 < f.length; k++) { for (const j of [f[0], f[k], f[k + 1]]) pos.push(...V[j]); tri.push(i); }
      for (const [a, b] of edgeList) edges.push(...V[a], ...V[b]);
    });
    if (!pos.length) return;
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    const see = glass || skeleton || opacity < 1, op = skeleton ? 0 : glass ? 0.22 : opacity;
    const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: colour, roughness: 0.45, metalness: 0.05, flatShading: true, side: THREE.DoubleSide,
      transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }));
    mesh.renderOrder = see ? 2 : 0; mesh.userData = { ...userData, tri };
    const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
    const line = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x2a2218, transparent: true, opacity: skeleton ? 0.9 : glass ? 0.25 : 0.6 }));
    group.add(mesh, line); pickTargets.push(mesh);
  }
  function draw() {
    clearGroup();
    if (!active || !DATA) return;
    const sites = shownSites(), byKind = {};
    for (const s of sites) (byKind[solidAt(s[3])] ??= []).push(s);
    for (const [k, list] of Object.entries(byKind)) {
      const glass = gapShown() || (notchShown() && (k === 'notched' || k === 'stella'));
      addMerged(DATA.solids[k], list, COLOUR[k], glass && (k !== 'octa'), { kind: 'solid', solid: k, sites: list });
    }
    if (gapShown()) {
      for (let g = 0; g < 4; g++) {
        const pieces = [], offs = [];
        for (const s of sites) {
          const holder = solidAt(s[3]) === 'ico' ? 'ico' : 'stella';
          for (const p of DATA.gap[holder]) if (p.k === g) { pieces.push(p); offs.push(s); }
        }
        if (!pieces.length) continue;
        // pieces differ in shape within a kind (turned copies), so each is its own small solid in the merged mesh
        const pos = [], edges = [];
        pieces.forEach((p, i) => {
          const o = offs[i], c = p.v.reduce((a, v) => [a[0] + v[0], a[1] + v[1], a[2] + v[2]], [0, 0, 0]).map((x) => x / p.v.length);
          const V = p.v.map((v) => [0, 1, 2].map((j) => (v[j] - c[j]) * 0.97 + c[j] + o[j]));
          for (const f of p.f) { for (let k = 1; k + 1 < f.length; k++) for (const j of [f[0], f[k], f[k + 1]]) pos.push(...V[j]); f.forEach((a, k) => edges.push(...V[a], ...V[f[(k + 1) % f.length]])); }
        });
        const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.computeVertexNormals();
        const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: GAP_COLOUR[g], roughness: 0.5, flatShading: true, side: THREE.DoubleSide }));
        mesh.userData = { kind: 'gap', g };
        const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
        group.add(mesh, new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x2a2218, transparent: true, opacity: 0.35 }))); pickTargets.push(mesh);
      }
    }
  }
  const fit = () => {
    if (!DATA) return;
    const r = Math.max(1, ...DATA.sites.filter((s) => s[4] <= view.layers).map((s) => Math.hypot(s[0], s[1], s[2]))) + 0.9;
    fitView([0, 0, 0], r * WS, DATA.axis);
  };

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || !DATA || mode === 'paint') return false;
    const L = lang();
    if (ud.kind === 'gap') { showHudPrompt(t(`os.prompt.gap${ud.g}`, L, { n: GAP_COUNT[ud.g] }), 4500); return true; }
    if (ud.kind !== 'solid') return false;
    showHudPrompt(t(`os.prompt.${ud.solid}`, L), 4500);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldocdstella-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note os-note"></div>
    <div class="w4d-row w4d-options os-partners">${PARTNERS.map((x) => `<button type="button" data-os-partner="${x}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options os-toggles"><button type="button" data-os="gap"></button><button type="button" data-os="notch"></button><button type="button" data-os="reset"></button></div>
    <div class="w4d-row os-grow-row"><label class="hull-pick"><span class="os-grow-label"></span> <input type="range" class="st-slider" min="0" max="4" step="1"></label></div>
    <style>#worldocdstella-panel .os-note{max-width:62ch;margin:0 auto}</style>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'ocdstella');
  const grow = panel.querySelector('.os-grow-row input');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), p = view.partner;
    if (!DATA) { panel.querySelector('.os-note').textContent = t('os.loading', L); return; }
    panel.querySelector('.os-note').textContent = t(`os.short.${p}`, L, { fill: FILL[p], group: GROUP[p] });
    panel.querySelectorAll('[data-os-partner]').forEach((b) => { b.textContent = t(`os.partner.${b.dataset.osPartner}`, L); b.classList.toggle('active', b.dataset.osPartner === p); });
    const tog = (k, on) => { const b = panel.querySelector(`[data-os="${k}"]`); b.hidden = !on; if (on) { b.textContent = t(`os.${k}`, L); b.classList.toggle('active', view[k]); } };
    tog('gap', p !== 'octa'); tog('notch', p === 'octa');
    const reset = panel.querySelector('[data-os="reset"]');
    reset.hidden = Object.keys(PRESET).every((k) => view[k] === PRESET[k]); reset.textContent = t('os.reset', L);
    grow.value = String(view.layers);
    panel.querySelector('.os-grow-label').textContent = t('os.grow', L, { n: view.layers });
  }
  const commit = (refit = false) => { save(); draw(); renderPanel(); onChange(); if (refit) fit(); };
  panel.querySelectorAll('[data-os-partner]').forEach((b) => b.addEventListener('click', () => {
    if (view.partner === b.dataset.osPartner) return;
    view.partner = b.dataset.osPartner; commit();
    showHudPrompt(t(`os.prompt.swap.${view.partner}`, lang()), 4500);
  }));
  for (const k of ['gap', 'notch']) panel.querySelector(`[data-os="${k}"]`).addEventListener('click', () => { view[k] = !view[k]; commit(); });
  panel.querySelector('[data-os="reset"]').addEventListener('click', () => { Object.assign(view, PRESET); commit(true); });
  grow.addEventListener('input', () => { view.layers = Number(grow.value); save(); draw(); renderPanel(); });
  grow.addEventListener('change', () => { onChange(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { clearGroup(); DATA = null; loading = null; renderPanel(); return; } // leaving lets the solids and the data go
      renderPanel();
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('os.prompt.start', lang()), 5500); });
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { Object.assign(view, PRESET); commit(active); },
    resetView() {},
    open(sub) { if (PARTNERS.includes(sub)) view.partner = sub; else return; save(); if (active) { draw(); renderPanel(); fit(); } },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: an icosahedron, the OCD Stella's outline. */
export function ocdStellaPreviewPoints() {
  const PHI = (1 + Math.sqrt(5)) / 2, ico = [];
  for (const a of [-1, 1]) for (const b of [-1, 1]) ico.push([0, a, b * PHI], [a, b * PHI, 0], [b * PHI, 0, a]);
  return ico;
}
