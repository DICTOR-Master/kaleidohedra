// DICTO Icosa: a 3D+ world of its own (DICTO, 2026-10-10: "own Icosa world", reached only through the DICTO
// worlds). The DICTO Icosa family (Kaleidohedra DISCOVERIES #19, #20; names by DICTO), one shape at a time:
// the clusters with their parts views and a slider that pulls the pieces apart, the Kepler Star Diadem with its
// gaps filled by the 120 Shark Teeth or left open, and the single pieces. Geometry in
// krp-core/src/geometry-extensions/icosa.js, checked in scripts/verify-icosa.mjs.
// English first; the other languages fall back to it until translated.
import * as THREE from 'three';
import { ICOSA_SOLIDS, ICOSA_PARTS, ICOSA_NAMES, ICOSA_PIECE_KEYS, ICOSA_CLUSTER_KEYS } from '../krp-core/src/geometry-extensions/icosa.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const STORAGE_KEY = storageKey('icosa');
const ITEMS = [...ICOSA_CLUSTER_KEYS, ...ICOSA_PIECE_KEYS];
// The study colours (DICTO 2026-10-10: kept): icosahedra green, icosidodecahedra and dodecahedra gold, AXE cyan,
// FUJI and CLEO purple, Kepler Star spikes orange-red, VAJRA orange, Shark Teeth grey.
const ROLE = { ico: 0x5fd38a, j11: 0x5fd38a, cap: 0x5fd38a, hasu: 0x5fd38a, idd: 0xffc857, dodeca: 0xffc857, axe: 0x4dd0e1,
  fuji: 0xc792ea, cleo: 0xc792ea, spike: 0xff7a59, vajra: 0xff9a52, shark: 0x9fb4c8 };
const PIECE = { AXE: 'axe', FUJI: 'fuji', CLEO: 'cleo', TRISKELION: 'cleo', TRISKELION_HEX: 'fuji', INNER_EYE: 'axe', HASU: 'ico',
  VAJRA: 'vajra', HMV: 'cap', FIVE_OF_CUPS: 'cap', KING_OF_PENTACLES: 'cap', HOUND_TOOTH: 'axe', TRICAP: 'fuji', KEPLER_STAR: 'spike',
  SHARK_TOOTH: 'shark', BERMUDA_PYRAMID: 'shark', LOTUS_SEED: 'ico', UNITY: 'ico', VENUS: 'vajra', STELLA_CORONA: 'ico', KEPLER_STAR_DIADEM: 'spike' };
const VIEW_LABEL = { pieces: 'icosa.view.pieces', build: 'icosa.view.build', units: 'icosa.view.units' };
const EDGE_COLOR = 0x0b1220;
const lang = () => getSettings().language;

export function createIcosaWorld({ scene, fitView = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { item: 'STELLA_CORONA', part: 'pieces', apart: 0, fill: false };
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (ITEMS.includes(data?.item)) view.item = data.item;
    if (typeof data?.part === 'string') view.part = data.part;
    if (Number.isFinite(data?.apart)) view.apart = Math.max(0, Math.min(1.2, data.apart));
    view.fill = data?.fill === true;
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false;

  const material = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
  }
  // The parts views a cluster offers (the Diadem's 'filled' view is the Fill gaps switch, not a view).
  const viewsOf = (key) => Object.keys(ICOSA_PARTS[key] ?? {}).filter((v) => v !== 'filled');
  // What to draw: [{ vertices, faces, colour }] in the shape's frame.
  function solids() {
    const parts = ICOSA_PARTS[view.item];
    if (parts) {
      const v = view.item === 'KEPLER_STAR_DIADEM' && view.fill ? 'filled' : (viewsOf(view.item).includes(view.part) ? view.part : viewsOf(view.item)[0]);
      return parts[v].map((p) => ({ vertices: p.vertices, faces: p.faces, colour: ROLE[p.role] ?? 0xb8c4bd }));
    }
    const S = ICOSA_SOLIDS[view.item];
    return [{ vertices: S.vertices, faces: S.faces, colour: ROLE[PIECE[view.item]] ?? 0xb8c4bd }];
  }
  const centreOf = (P) => P.reduce((a, p) => a.map((c, i) => c + p[i] / P.length), [0, 0, 0]);
  let radius = 1;
  function draw() {
    clearGroup();
    if (!active) return;
    const list = solids();
    const all = list.flatMap((s) => s.vertices);
    const c0 = centreOf(all);
    radius = Math.max(...all.map((p) => Math.hypot(...p.map((c, i) => c - c0[i]))));
    const pos = [], col = [], line = [];
    const colour = new THREE.Color();
    for (const s of list) {
      // Pulled apart: each part moves out along the line from the centre through its own centre.
      const off = centreOf(s.vertices).map((c, i) => (c - c0[i]) * view.apart);
      const P = s.vertices.map((p) => p.map((c, i) => (c - c0[i] + off[i]) * WS));
      colour.setHex(s.colour);
      for (const f of s.faces) {
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { pos.push(...P[k]); col.push(colour.r, colour.g, colour.b); }
        f.forEach((k, i) => line.push(...P[k], ...P[f[(i + 1) % f.length]]));
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    group.add(new THREE.Mesh(g, material), new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: EDGE_COLOR })));
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], radius * (1 + view.apart) * WS * 1.1);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldicosa-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="ic-item-label"></span> <select class="hull-select" data-select="item"></select></label></div>
    <div class="w4d-row ic-view-row"><label class="hull-pick"><span class="ic-view-label"></span> <select class="hull-select" data-select="part"></select></label></div>
    <div class="w4d-row ic-apart-row"><label class="hull-pick"><span class="ic-apart-label"></span> <input type="range" class="st-slider" min="0" max="1200" step="1"></label></div>
    <div class="w4d-row w4d-options ic-fill-row"><button type="button" data-icosa-fill></button></div>
    <div class="w4d-row st-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'icosa');
  const itemSelect = panel.querySelector('[data-select="item"]');
  const partSelect = panel.querySelector('[data-select="part"]');
  const apartInput = panel.querySelector('.ic-apart-row input');
  const fillBtn = panel.querySelector('[data-icosa-fill]');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.ic-item-label').textContent = t('icosa.shape', L);
    const opt = (k) => `<option value="${k}"${k === view.item ? ' selected' : ''}>${ICOSA_NAMES[k]}</option>`;
    itemSelect.innerHTML = `<optgroup label="${t('icosa.clusters', L)}">${ICOSA_CLUSTER_KEYS.map(opt).join('')}</optgroup><optgroup label="${t('icosa.pieces', L)}">${ICOSA_PIECE_KEYS.map(opt).join('')}</optgroup>`;
    const views = viewsOf(view.item);
    panel.querySelector('.ic-view-row').style.display = views.length > 1 ? '' : 'none';
    panel.querySelector('.ic-view-label').textContent = t('icosa.view', L);
    partSelect.innerHTML = views.map((v) => `<option value="${v}"${v === view.part ? ' selected' : ''}>${t(VIEW_LABEL[v] ?? v, L)}</option>`).join('');
    panel.querySelector('.ic-apart-row').style.display = ICOSA_PARTS[view.item] ? '' : 'none';
    panel.querySelector('.ic-apart-label').textContent = t('icosa.apart', L);
    apartInput.value = String(Math.round(view.apart * 1000));
    panel.querySelector('.ic-fill-row').style.display = view.item === 'KEPLER_STAR_DIADEM' ? '' : 'none';
    fillBtn.textContent = t(view.fill ? 'icosa.fill.on' : 'icosa.fill.off', L);
    panel.querySelector('.st-note').textContent = t(`icosa.note.${view.item}`, L);
  }
  itemSelect.addEventListener('change', () => {
    if (!ITEMS.includes(itemSelect.value)) return;
    view.item = itemSelect.value;
    if (!viewsOf(view.item).includes(view.part)) view.part = viewsOf(view.item)[0] ?? 'pieces';
    save(); draw(); fit();
  });
  partSelect.addEventListener('change', () => { view.part = partSelect.value; save(); draw(); });
  apartInput.addEventListener('input', () => { view.apart = Number(apartInput.value) / 1000; save(); draw(); });
  apartInput.addEventListener('change', fit);
  fillBtn.addEventListener('click', () => { view.fill = !view.fill; save(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) panel.classList.remove('visible');
      draw();
      if (on) fit();
    },
    setSkeleton() {},
    setTranslucent() {},
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
  };
}
