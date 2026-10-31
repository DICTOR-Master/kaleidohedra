// HexOct (DICTO 2026-10-31, approved spec): the Polyhedraverse world of paper #75, "HexOct: Two Tiles for Every Stacking" (DICTO DOI
// 10.5281/zenodo.23737639). The two layer tiles DICTO named HexOct, the c-tile gold and the h-tile blue (as in his HexOct book), stacked
// as a crystal: a button for each fill (3C c-tiles only, 2H h-tiles only, 4H, 6H, Fibonacci c → ch, h → c from c) and a field for the
// viewer's own c/h sequence; each layer a 3 × 3 patch of its tile. Helpers turns every tile into its four pieces as see-through
// coloured glass (DICTO's standing rule for constructions), tetrahedral pieces dark and octahedral halves light, so one sees how each
// tile is cut from the packing's holes. Drawn to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset by
// default, crisp screen-space edges ≥ 1.5 px. Geometry: hexoct-geometry.js (λ = 1/10, the paper's figures).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { HEXOCT_FILLS, fillTypes, parseTypes, lettersOf, hexoctCrystal } from './hexoct-geometry.js';

export const HEXOCT_KINDS = [...HEXOCT_FILLS, 'own'];
// c-tile gold, h-tile blue (DICTO's HexOct book; #75 Figure 2); with Helpers the tetrahedral pieces darker, the octahedral halves lighter
export const HEXOCT_COLOURS = { c: 0xf2b84b, h: 0x4a90e2, cTet: 0xa8740c, cOct: 0xf8dc8c, hTet: 0x1f56a8, hOct: 0xaed2f7 };
const EDGE = 0x0b1220, GLASS = 0.34;
const MIN_LAYERS = 6;   // a short own sequence is repeated up to this many layers, so it reads as a crystal
const lang = () => getSettings().language;
/** The layers shown for a kind: a fill's eight, or the viewer's own sequence (repeated to at least MIN_LAYERS). */
export function hexoctLayers(kind, own) {
  if (kind !== 'own') return fillTypes(kind);
  const s = parseTypes(own) ?? 'c';
  return s.length >= MIN_LAYERS ? s : s.repeat(Math.ceil(MIN_LAYERS / s.length));
}
// study frame (z up) to the app's (y up), a proper turn so the tiles keep their hand
const toApp = (v) => [v[0] * WS, v[2] * WS, -v[1] * WS];

export function createHexoctWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('hexoct-world');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { kind: '3C', own: 'cchch', helpers: false };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (HEXOCT_KINDS.includes(d?.kind)) view.kind = d.kind;
    if (parseTypes(d?.own)) view.own = parseTypes(d.own);
    view.helpers = d?.helpers === true;
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, radius = 1, shown = null;

  const solidMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5, metalness: 0.1 });
  const glassMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: GLASS, depthWrite: false, roughness: 0.4 });
  glassMat.userData.hollow = true;   // helpers stay hollow in an X-ray cut (xray-caps.js)
  const lineMats = [];
  function clear() {
    for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); }
    lineMats.splice(0).forEach((m) => m.dispose());
  }
  function draw() {
    clear();
    if (!active) return;
    const types = hexoctLayers(view.kind, view.own), pieces = hexoctCrystal(types);
    const pos = [], col = [], edges = [], edgeCol = [], colour = new THREE.Color();
    let far = 0;
    for (const p of pieces) {
      const P = p.vertices.map(toApp);
      const key = view.helpers ? `${p.type}${p.role === 'tet' ? 'Tet' : 'Oct'}` : p.type;
      colour.setHex(HEXOCT_COLOURS[key]);
      for (const f of p.faces) {
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { pos.push(...P[k]); col.push(colour.r, colour.g, colour.b); }
        f.forEach((a, i) => edges.push(...P[a], ...P[f[(i + 1) % f.length]]));
      }
      for (const v of P) far = Math.max(far, Math.hypot(...v));
      // with Helpers each piece's edges in a deeper shade of its own colour, so the cut reads through the glass
      if (view.helpers) { const e = colour.clone().multiplyScalar(0.55); for (let n = edges.length / 6 - edgeCol.length / 6; n > 0; n--) edgeCol.push(e.r, e.g, e.b, e.r, e.g, e.b); }
    }
    radius = far;
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const mat = view.helpers ? glassMat : solidMat;
    if (!view.helpers) { solidMat.transparent = opacity < 1; solidMat.opacity = opacity; solidMat.depthWrite = opacity >= 1; solidMat.needsUpdate = true; }
    if (!skeleton) group.add(new THREE.Mesh(g, mat));
    else g.dispose();
    const lg = new LineSegmentsGeometry();
    lg.setPositions(edges);
    if (view.helpers) lg.setColors(edgeCol);
    const lm = new LineMaterial({ color: view.helpers ? 0xffffff : (skeleton ? 0xcfe3ff : EDGE), linewidth: view.helpers ? 1.5 : 1.6, vertexColors: view.helpers });
    lineMats.push(lm);
    const lines = new LineSegments2(lg, lm);
    lines.frustumCulled = false;
    group.add(lines);
    shown = { types, pieces: pieces.length, tiles: pieces.length / 4, c: [...types].filter((x) => x === 'c').length, h: [...types].filter((x) => x === 'h').length };
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], radius * 0.75, [1, 0.32, 1.25]);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldhexoct-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options hx-kinds">${HEXOCT_KINDS.map((k) => `<button type="button" data-hx-kind="${k}"></button>`).join('')}</div>
    <div class="w4d-row hx-own-row"><input type="text" class="hx-own" maxlength="40" autocomplete="off" autocapitalize="none" spellcheck="false" enterkeyhint="go"><button type="button" class="hx-own-go" data-hx-own-go></button></div>
    <div class="w4d-row w4d-options"><button type="button" data-hx-helpers aria-pressed="false"></button></div>
    <div class="w4d-row ch-param-caption hx-caption" aria-live="polite"></div>
    <div class="w4d-row st-note hx-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'hexoct');
  const ownInput = panel.querySelector('.hx-own'), helpersBtn = panel.querySelector('[data-hx-helpers]');
  let typing = false;   // the field keeps what the viewer types until it is used
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelectorAll('[data-hx-kind]').forEach((b) => { const k = b.dataset.hxKind; b.textContent = t(`hexoct.kind.${k}`, L); b.classList.toggle('active', k === view.kind); b.setAttribute('aria-pressed', String(k === view.kind)); });
    ownInput.placeholder = t('hexoct.own.placeholder', L);
    ownInput.setAttribute('aria-label', t('hexoct.own.label', L));
    if (!typing) ownInput.value = view.kind === 'own' ? view.own : (shown?.types ?? '');
    panel.querySelector('[data-hx-own-go]').textContent = t('hexoct.own.go', L);
    helpersBtn.textContent = t(view.helpers ? 'hexoct.helpers.on' : 'hexoct.helpers.off', L);
    helpersBtn.classList.toggle('active', view.helpers); helpersBtn.setAttribute('aria-pressed', String(view.helpers));
    if (shown) {
      const word = lettersOf(shown.types).slice(1, -1).join('');
      panel.querySelector('.hx-caption').textContent = t('hexoct.caption', L, { types: [...shown.types].join(' '), word, n: shown.types.length, c: shown.c, h: shown.h });
    }
    panel.querySelector('.hx-note').textContent = t(view.helpers ? 'hexoct.note.helpers' : 'hexoct.note', L);
  }
  const setKind = (k) => { if (!HEXOCT_KINDS.includes(k)) return false; view.kind = k; typing = false; save(); draw(); fit(); return true; };
  panel.querySelector('.hx-kinds').addEventListener('click', (e) => { const k = e.target.closest('[data-hx-kind]')?.dataset.hxKind; if (k && k !== view.kind) setKind(k); });
  // the viewer's own sequence: c and h only; anything else leaves the crystal as it is and says what the field takes
  function useOwn() {
    const s = parseTypes(ownInput.value);
    if (!s) { panel.querySelector('.hx-note').textContent = t('hexoct.own.bad', lang()); ownInput.focus(); return; }
    view.own = s; ownInput.blur(); setKind('own');
  }
  ownInput.addEventListener('input', () => { typing = true; });
  ownInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); useOwn(); } });
  panel.querySelector('[data-hx-own-go]').addEventListener('click', useOwn);
  helpersBtn.addEventListener('click', () => { view.helpers = !view.helpers; save(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=hexoct:<3C|2H|4H|6H|fib>, or hexoct:<c/h sequence> (e.g. hexoct:chh) as the viewer's own; anything else keeps the fill shown. */
    setChain(kind) {
      const k = HEXOCT_KINDS.find((x) => x.toLowerCase() === String(kind).toLowerCase());
      if (k && k !== 'own') view.kind = k;
      else if (parseTypes(kind)) { view.own = parseTypes(kind); view.kind = 'own'; }
      else return;
      typing = false; save();
      if (active) { draw(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); clear(); return; }
      draw(); fit();
    },
    resetView() { Object.assign(view, { kind: '3C', helpers: false }); typing = false; save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the fill, its layers, and what is drawn. */
    probe: () => ({ kind: view.kind, own: view.own, helpers: view.helpers, types: shown?.types ?? null, pieces: shown?.pieces ?? 0, tiles: shown?.tiles ?? 0, c: shown?.c ?? 0, h: shown?.h ?? 0,
      radius, glass: group.children.some((c) => c.isMesh && c.material === glassMat), lineWidth: lineMats[0]?.linewidth ?? null }),
  };
}
