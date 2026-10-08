// The Stella–Jewel Lattice (direct request, 2026-10-08): a 3D+ world of Dragon Jewels (DJ,
// DICTO's name for the windows solid, DISCOVERIES #10) on the even cells and stella octangulas
// on the odd cells, which fill space exactly (study 10b; the face-centred cubic lattice with two
// pieces per point). Tap a face to grow the piece across it; long-press to remove. Two views:
// both pieces, or the Dragon Jewels alone (they meet face to face on all 12 rhombi, leaving
// stella-shaped holes). The Shear either moves the cell centres and keeps every piece exact
// (copies), or bends the whole packing (solid). The five-fold toggle overlays each Dragon Jewel's
// six five-fold axes and the five window positions on each face, the cube's choice bright.
// Geometry in geometry-extensions/roof-fold.js, checked in scripts/verify-roof-fold.mjs §13(f, g).
import * as THREE from 'three';
import {
  ekpWindowsSolid, roofFoldSolids, ROOF_FOLD_COLOURS, ROOF_FOLD_WORLD_SCALE as WS,
  insideDragonJewel, insideStella, DJ_NEIGHBOURS, fiveWindowPositions, fiveFoldAxes,
} from '../geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';

const STORAGE_KEY = 'kaleidohedra-stella-jewel';
const C = ROOF_FOLD_COLOURS;
const DJ_RHOMBUS = C.dodeca;
const DJ_WALL = 0xb8892a;
const STELLA = C.stella;
const EDGE_COLOR = 0x0b1220;
const GHOST_COLOR = 0xff9a52;
const FIRST_COLOR = 0x22c3e6; // "tap here first": cyan, against the orange livery
const AXIS_COLOR = 0xffffff;
const MODES = ['both', 'jewels'];
const lang = () => getSettings().language;
const key = (s) => s.join(',');
const isEven = (s) => (((s[0] + s[1] + s[2]) % 2) + 2) % 2 === 0;

export function createStellaJewelWorld({ scene, fitView = () => {}, shear = () => null, showHudPrompt = () => {}, onChange = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const DJ = ekpWindowsSolid();
  const STELLA_FACES = roofFoldSolids().stella.faces;
  const FIVE = fiveWindowPositions();
  const AXES = fiveFoldAxes();

  // ---- state ----
  const cells = new Map(); // key -> [x, y, z]
  const view = { mode: 'both', shear: 'copies', axes: false };
  let active = false, skeleton = false, opacity = 1, latticeView = false;
  function read(data) {
    cells.clear();
    for (const s of Array.isArray(data?.cells) ? data.cells : []) if (Array.isArray(s) && s.length === 3 && s.every(Number.isInteger)) cells.set(key(s), [...s]);
    if (MODES.includes(data?.view?.mode)) view.mode = data.view.mode;
    if (['copies', 'solid'].includes(data?.view?.shear)) view.shear = data.view.shear;
    view.axes = data?.view?.axes === true;
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: start empty */ }
  const snapshot = () => ({ version: 1, cells: [...cells.values()], view: { ...view } });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const shown = () => [...cells.values()].filter((s) => view.mode === 'both' || isEven(s));

  // ---- placement through the shear ----
  const shearMap = (p) => { const A = shear(); return A ? A.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]) : p; };
  const shearInv = (p) => {
    const A = shear();
    if (!A) return p;
    const [a, b, c] = A, det = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);
    const inv = [
      [b[1] * c[2] - b[2] * c[1], a[2] * c[1] - a[1] * c[2], a[1] * b[2] - a[2] * b[1]],
      [b[2] * c[0] - b[0] * c[2], a[0] * c[2] - a[2] * c[0], a[2] * b[0] - a[0] * b[2]],
      [b[0] * c[1] - b[1] * c[0], a[1] * c[0] - a[0] * c[1], a[0] * b[1] - a[1] * b[0]],
    ].map((r) => r.map((v) => v / det));
    return inv.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]);
  };
  const copies = () => view.shear === 'copies';
  // A cell-unit point of the piece at site s, in world units.
  const toWorld = (s, p) => {
    const c = s.map((x) => 2 * x);
    return (copies() ? shearMap(c).map((v, a) => v + p[a]) : shearMap(p.map((v, a) => v + c[a]))).map((v) => v * WS);
  };
  // A world point back into the frame of the piece at site s (cell units, unsheared).
  const toLocal = (s, w) => {
    const q = w.map((v) => v / WS), c = s.map((x) => 2 * x);
    return copies() ? q.map((v, a) => v - shearMap(c)[a]) : shearInv(q).map((v, a) => v - c[a]);
  };

  // ---- drawing ----
  const pieceMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const ghostMaterial = new THREE.MeshStandardMaterial({ color: GHOST_COLOR, transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  const firstMaterial = new THREE.MeshStandardMaterial({ color: FIRST_COLOR, transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  const pickTargets = [];
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
    }
    pickTargets.length = 0;
  }
  const facesOf = (s) => (isEven(s) ? [...DJ.rhombi.map((f) => [f, DJ_RHOMBUS]), ...DJ.walls.map((f) => [f, DJ_WALL])] : STELLA_FACES.map((f) => [f, STELLA]));
  function meshOf(sitesList, material, tag, colourOverride, edgeColor = EDGE_COLOR) {
    const pos = [], col = [], line = [], records = [];
    for (const s of sitesList) for (const [f, hex] of facesOf(s)) {
      const colour = new THREE.Color(colourOverride ?? hex);
      const P = f.map((p) => toWorld(s, p));
      for (let i = 1; i + 1 < P.length; i++) {
        for (const p of [P[0], P[i], P[i + 1]]) { pos.push(...p); col.push(colour.r, colour.g, colour.b); }
        records.push(s);
      }
      P.forEach((p, i) => line.push(...p, ...P[(i + 1) % P.length]));
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const mesh = new THREE.Mesh(g, material);
    mesh.userData.stellaJewel = tag;
    mesh.userData.records = records;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    return [mesh, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: edgeColor }))];
  }
  // Empty cells touching the build: across faces (Dragon Jewel <-> stella), and Dragon Jewel to
  // Dragon Jewel across the rhombi; in the jewels-alone view, the rhombus neighbours only.
  function emptyNeighbours() {
    const out = new Map();
    for (const s of shown()) for (const d of DJ_NEIGHBOURS) {
      const fcc = Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]) === 2;
      if (fcc ? !isEven(s) : view.mode === 'jewels') continue;
      const n = s.map((c, i) => c + d[i]);
      if (!cells.has(key(n))) out.set(key(n), n);
    }
    return [...out.values()];
  }
  function draw() {
    clearGroup();
    if (!active) return;
    const S = shown();
    if (!S.length) {
      const [m, l] = meshOf([[0, 0, 0]], firstMaterial, 'first', FIRST_COLOR, FIRST_COLOR);
      group.add(m, l);
      pickTargets.push(m);
    } else {
      pieceMaterial.transparent = opacity < 1;
      pieceMaterial.opacity = opacity;
      pieceMaterial.depthWrite = opacity >= 1;
      const [m, l] = meshOf(S, pieceMaterial, 'piece');
      m.visible = !skeleton;
      if (skeleton) l.material.color.setHex(GHOST_COLOR);
      group.add(m, l);
      pickTargets.push(m);
      if (latticeView) {
        const ghosts = emptyNeighbours();
        if (ghosts.length) {
          const [gm, gl] = meshOf(ghosts, ghostMaterial, 'ghost', GHOST_COLOR, GHOST_COLOR);
          gl.material.transparent = true;
          gl.material.opacity = 0.4;
          group.add(gm, gl);
          pickTargets.push(gm);
        }
      }
      if (view.axes) group.add(...fiveFoldOverlay(S.filter(isEven)));
    }
    renderPanel();
  }
  // The six five-fold axes through each Dragon Jewel, and on every face the five window
  // positions: faint, with the cube's choice (the window itself) bright.
  function fiveFoldOverlay(jewels) {
    const axis = [], faint = [], bright = [];
    for (const s of jewels) {
      for (const a of AXES) axis.push(...toWorld(s, a.map((c) => -2.1 * c)), ...toWorld(s, a.map((c) => 2.1 * c)));
      for (const { rhombus, chosen } of FIVE) rhombus.forEach((p, i) => (chosen ? bright : faint).push(...toWorld(s, p), ...toWorld(s, rhombus[(i + 1) % 4])));
    }
    const lines = (pts, color, op) => {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      const ls = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color, transparent: true, opacity: op, depthTest: false }));
      ls.renderOrder = 3;
      return ls;
    };
    return [lines(axis, AXIS_COLOR, 0.7), lines(faint, FIRST_COLOR, 0.35), lines(bright, DJ_RHOMBUS, 1)];
  }
  function fit() {
    const S = shown();
    if (!S.length) { fitView([0, 0, 0], 2.2 * WS); return; }
    const P = S.map((s) => toWorld(s, [0, 0, 0]));
    const c = [0, 1, 2].map((a) => P.reduce((t0, p) => t0 + p[a], 0) / P.length);
    fitView(c, Math.max(...P.map((p) => Math.hypot(...p.map((v, a) => v - c[a])))) + 2 * WS);
  }

  // ---- building ----
  function commit() { save(); draw(); onChange(); }
  function add(s) {
    if (cells.has(key(s))) return false;
    if (view.mode === 'jewels' && !isEven(s)) return false;
    cells.set(key(s), [...s]);
    commit();
    fit();
    return true;
  }
  // The piece across the tapped face: the neighbour whose piece holds a point just outside it.
  function across(s, hit) {
    const n = hit.face.normal;
    const w = [hit.point.x + n.x * 0.03 * WS, hit.point.y + n.y * 0.03 * WS, hit.point.z + n.z * 0.03 * WS];
    const q = toLocal(s, w);
    for (const d of DJ_NEIGHBOURS) {
      const nb = s.map((c, i) => c + d[i]);
      const p = q.map((v, a) => v - 2 * d[a]);
      if (isEven(nb) ? insideDragonJewel(p) : insideStella(p)) return nb;
    }
    return null;
  }
  function handleTap(hit, mode) {
    const tag = hit.object.userData.stellaJewel;
    const s = hit.object.userData.records?.[hit.faceIndex];
    if (!tag || !s || mode === 'paint') return false;
    const chisel = mode === 'chisel';
    if (tag === 'first' || tag === 'ghost') return chisel ? false : add(s);
    if (chisel) {
      if (!cells.delete(key(s))) return false;
      commit();
      return true;
    }
    const nb = across(s, hit);
    if (!nb) return false;
    if (view.mode === 'jewels' && !isEven(nb)) { showHudPrompt(t('dj.prompt.hole', lang()), 2500); return false; }
    if (add(nb)) return true;
    showHudPrompt(t('dj.prompt.taken', lang()), 2000);
    return false;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldstellajewel-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="sj-view-label"></span> <select class="hull-select" data-select="mode"></select></label></div>
    <div class="w4d-row sj-count"></div>
    <div class="w4d-row w4d-options"><button type="button" data-sj="shear"></button><button type="button" data-sj="axes"></button></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'stella-jewel');
  const modeSelect = panel.querySelector('[data-select="mode"]');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.sj-view-label').textContent = t('dj.view', L);
    modeSelect.innerHTML = MODES.map((m) => `<option value="${m}"${m === view.mode ? ' selected' : ''}>${t(`dj.view.${m}`, L)}</option>`).join('');
    const all = [...cells.values()];
    panel.querySelector('.sj-count').textContent = t('dj.count', L, { jewels: all.filter(isEven).length, stellas: all.filter((s) => !isEven(s)).length });
    const shearBtn = panel.querySelector('[data-sj="shear"]');
    shearBtn.textContent = t(`studies.shear.${view.shear}`, L);
    const axesBtn = panel.querySelector('[data-sj="axes"]');
    axesBtn.textContent = t('dj.axes', L);
    axesBtn.classList.toggle('active', view.axes);
  }
  modeSelect.addEventListener('change', () => {
    if (!MODES.includes(modeSelect.value)) return;
    view.mode = modeSelect.value;
    save(); draw(); fit();
  });
  panel.querySelector('[data-sj="shear"]').addEventListener('click', () => { view.shear = copies() ? 'solid' : 'copies'; save(); draw(); fit(); });
  panel.querySelector('[data-sj="axes"]').addEventListener('click', () => { view.axes = !view.axes; save(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) panel.classList.remove('visible');
      draw();
      if (on) { fit(); if (!shown().length) showHudPrompt(t('dj.prompt.start', lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView(on) { latticeView = on; if (active) draw(); },
    shearChanged() { if (active) draw(); },
    get isEmpty() { return cells.size === 0; },
    clear() { cells.clear(); commit(); if (active) fit(); },
    snapshot,
    restore(json) { read(json); save(); draw(); },
  };
}
