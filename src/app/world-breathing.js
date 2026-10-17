// Golden Breathing Pyrochlore (DICTO 2026-10-14): the pyrochlore with its two sets of corner-sharing tetrahedra in two sizes, edge 1
// and edge r (the breathing ratio), to build cell by cell, next to the Pyrochlore (3D Kagome) lattice. Every corner is still shared
// tip to tip by one big and one small tetrahedron; between them two kinds of truncated tetrahedra fill the rest of space, and all
// their hexagons are flat-ended triangles with sides 1 and r: at r = 1/φ (golden, where the world opens) FUJI's base, at r = 1/2 the
// space-filling truncated tetrahedron's faces, at r = 1 the ordinary pyrochlore's regular hexagons (FUJI family study,
// studies/2026-10-14-fuji-family). Cells and neighbours come from breathing-data.js (generated and checked there).
// Sites q are integers in quarter cubes; a cell's corners are (q + offset + f d) u with f = 1/(1 + r), u = √2 (1 + r)/4.
// A tap adds the empty neighbour on the tapped side, long-press (chisel) removes; the slider changes r for the whole build;
// "Kagome layer" shows one flat (111) layer of a patch: the triangles and the flat-ended hexagons. Words: i18n bp.*.
import * as THREE from 'three';
import DATA from './breathing-data.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const KINDS = Object.keys(DATA.kinds); // A (big tetrahedra), B (small), T1, T2 (truncated tetrahedra)
const COLOUR = { A: 0xffc857, B: 0xc792ea, T1: 0x4dd0e1, T2: 0x9fd8ff };
const GLASS = new Set(['T1', 'T2']);
// Named stops on the slider (snapped to when close): golden first.
export const BREATHING_STOPS = [{ key: 'golden', r: 1 / PHI }, { key: 'half', r: 0.5 }, { key: 'regular', r: 1 }];
const R_MIN = 0.2;
const keyOf = (q) => q.join(',');
const lang = () => getSettings().language;
const mod = (n, m) => ((n % m) + m) % m;

/** The kind of cell at site q (A, B, T1, T2), or null. */
export function kindAt(q) {
  for (const k of KINDS) {
    const d = q.map((c, i) => c - DATA.kinds[k][i]);
    if (d.every((x) => mod(x, 2) === 0) && mod(d.reduce((s, x) => s + x, 0), 4) === 0) return k;
  }
  return null;
}
const scale = (r) => ({ f: 1 / (1 + r), u: (Math.SQRT2 * (1 + r)) / 4 });
/** The cell at q for breathing ratio r: { kind, V, F } (unit: the big tetrahedron's edge). */
export function cellAt(q, r) {
  const kind = kindAt(q);
  if (!kind) return null;
  const { f, u } = scale(r);
  const V = DATA.cells[kind].corners.map(([o, j]) => o.map((x, i) => (q[i] + x + f * DATA.directions[j][i]) * u));
  return { kind, V, F: DATA.cells[kind].faces };
}
export const neighbours = (q) => DATA.neighbours[kindAt(q)].map((n) => q.map((c, i) => c + n.offset[i]));
const START = [0, 0, 0];
const startCells = () => [START, ...neighbours(START)]; // a big tetrahedron with its 4 small ones and 4 truncated tetrahedra

export function createBreathingWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('breathing');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { r: 1 / PHI, layer: false };
  const cells = new Map(); // key -> q
  function read(d) {
    const r = Number(d?.r);
    view.r = Number.isFinite(r) ? Math.min(1, Math.max(R_MIN, r)) : 1 / PHI;
    view.layer = d?.layer === true;
    cells.clear();
    for (const q of Array.isArray(d?.cells) ? d.cells : []) if (Array.isArray(q) && q.length === 3 && q.every(Number.isInteger) && kindAt(q)) cells.set(keyOf(q), q);
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: start fresh */ }
  const snapshot = () => ({ version: 1, r: view.r, layer: view.layer, cells: [...cells.values()] });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const commit = () => { save(); draw(); renderPanel(); onChange(); };
  const start = () => { for (const q of startCells()) cells.set(keyOf(q), q); };

  let active = false, skeleton = false, opacity = 1;
  const solid = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.24, depthWrite: false });
  glass.userData.hollow = true; // glass shells and helpers stay hollow in an X-ray cut (xray-caps.js)
  let pickTargets = [];
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
    pickTargets = [];
  }
  // Faces to draw: [kind, points, record]. The layer view takes the faces of a patch that lie in one (111) plane.
  function facesToDraw() {
    const out = [];
    if (!view.layer) {
      for (const q of cells.values()) {
        const c = cellAt(q, view.r);
        for (const f of c.F) out.push([c.kind, f.map((k) => c.V[k]), q]);
      }
      return out;
    }
    const n = [1, 1, 1].map((x) => x / Math.sqrt(3));
    const level = cellAt(START, view.r).V.map((p) => p[0] * n[0] + p[1] * n[1] + p[2] * n[2]).reduce((a, b) => Math.min(a, b));
    const seen = new Set();
    const R = 6;
    for (let x = -R; x <= R; x++) for (let y = -R; y <= R; y++) for (let z = -R; z <= R; z++) {
      const q = [x, y, z];
      if (!kindAt(q)) continue;
      const c = cellAt(q, view.r);
      for (const f of c.F) {
        const P = f.map((k) => c.V[k]);
        if (!P.every((p) => Math.abs(p[0] * n[0] + p[1] * n[1] + p[2] * n[2] - level) < 1e-6)) continue;
        if (P.some((p) => Math.hypot(...p) > 3.2)) continue;
        // each flat face belongs to two cells: keep the hexagons from the truncated tetrahedra, the triangles from the tetrahedra
        if ((P.length === 6) !== GLASS.has(c.kind)) continue;
        const key = P.map((p) => p.map((v) => v.toFixed(4)).join(',')).sort().join('|');
        if (seen.has(key)) continue;
        seen.add(key);
        out.push([c.kind, P, null]);
      }
    }
    // keep only the triangles that touch a kept hexagon (no stray triangles at the patch's rim)
    const near = (p, P) => P.some((v) => Math.hypot(v[0] - p[0], v[1] - p[1], v[2] - p[2]) < 1e-6);
    const hex = out.filter(([, P]) => P.length === 6);
    return out.filter(([, P]) => P.length === 6 || hex.some(([, H]) => P.some((p) => near(p, H))));
  }
  function draw() {
    clearGroup();
    if (!active) return;
    const buf = { solid: { pos: [], col: [], line: [], rec: [] }, glass: { pos: [], col: [], line: [], rec: [] } };
    const colour = new THREE.Color();
    for (const [kind, P0, q] of facesToDraw()) {
      // in the layer view the hexagons are drawn solid too, so the flat-ended triangles read clearly
      const b = GLASS.has(kind) && !view.layer ? buf.glass : buf.solid;
      const P = P0.map((p) => p.map((c) => c * WS));
      colour.setHex(view.layer && GLASS.has(kind) ? 0x4dd0e1 : COLOUR[kind]);
      for (let i = 1; i + 1 < P.length; i++) {
        for (const p of [P[0], P[i], P[i + 1]]) { b.pos.push(...p); b.col.push(colour.r, colour.g, colour.b); }
        b.rec.push(q);
      }
      P.forEach((p, i) => b.line.push(...p, ...P[(i + 1) % P.length]));
    }
    solid.transparent = opacity < 1; solid.opacity = opacity; solid.depthWrite = opacity >= 1; solid.needsUpdate = true;
    for (const [key, mat] of [['solid', solid], ['glass', glass]]) {
      const b = buf[key];
      if (!b.pos.length) continue;
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(b.pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(b.col, 3));
      g.computeVertexNormals();
      const mesh = new THREE.Mesh(g, mat);
      mesh.userData.records = b.rec;
      mesh.visible = !skeleton || key === 'glass';
      group.add(mesh);
      if (!view.layer) pickTargets.push(mesh);
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(b.line, 3));
      group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x0b1220, transparent: key === 'glass', opacity: key === 'glass' ? 0.55 : 1 })));
    }
  }
  const radius = () => {
    if (view.layer) return 3.4;
    let r = 1;
    const { u } = scale(view.r);
    for (const q of cells.values()) r = Math.max(r, Math.hypot(...q) * u + 1.2);
    return r;
  };
  const fit = () => fitView([0, 0, 0], radius() * WS * 1.1);

  function handleTap(hit, mode) {
    if (view.layer) return false;
    const q = hit.object.userData.records?.[Math.floor(hit.faceIndex ?? -1)];
    if (!q || mode === 'paint') return false;
    if (mode === 'chisel') {
      if (cells.size <= 1) return false;
      cells.delete(keyOf(q)); commit();
      return true;
    }
    const local = group.worldToLocal(hit.point.clone()).divideScalar(WS);
    const { u } = scale(view.r);
    const dir = [local.x - q[0] * u, local.y - q[1] * u, local.z - q[2] * u];
    const free = neighbours(q).filter((n) => !cells.has(keyOf(n)));
    if (!free.length) { showHudPrompt(t('bp.prompt.full', lang()), 2000); return true; }
    const score = (n) => n.reduce((s, c, i) => s + (c - q[i]) * dir[i], 0) / Math.hypot(...n.map((c, i) => c - q[i]));
    const n = free.reduce((best, x) => (score(x) > score(best) ? x : best));
    cells.set(keyOf(n), n); commit();
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldbreathing-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note bp-note"></div>
    <div class="w4d-row w4d-options"><button type="button" data-bp="layer"></button><button type="button" data-bp="reset"></button></div>
    <div class="w4d-row bp-ratio-row"><label class="hull-pick"><span class="bp-ratio-label"></span> <input type="range" class="st-slider" min="${R_MIN * 1000}" max="1000" step="1"></label></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'breathing');
  const ratio = panel.querySelector('.bp-ratio-row input');
  const stopAt = (r) => BREATHING_STOPS.find((s) => Math.abs(s.r - r) < 0.004);
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), stop = stopAt(view.r);
    panel.querySelector('.bp-note').textContent = `${t(stop ? `bp.stop.${stop.key}` : 'bp.stop.free', L, { r: view.r.toFixed(3) })} · ${t('bp.count', L, { n: cells.size })}`;
    panel.querySelector('[data-bp="layer"]').textContent = t(view.layer ? 'bp.layer.on' : 'bp.layer.off', L);
    panel.querySelector('[data-bp="reset"]').textContent = t('bp.reset', L);
    panel.querySelector('.bp-ratio-label').textContent = t('bp.ratio', L);
    ratio.value = String(Math.round(view.r * 1000));
  }
  ratio.addEventListener('input', () => {
    let r = Number(ratio.value) / 1000;
    const near = BREATHING_STOPS.find((s) => Math.abs(s.r - r) < 0.02);
    if (near) r = near.r;
    view.r = r;
    save(); draw(); renderPanel();
  });
  ratio.addEventListener('change', () => { onChange(); fit(); });
  panel.querySelector('[data-bp="layer"]').addEventListener('click', () => { view.layer = !view.layer; save(); draw(); renderPanel(); fit(); });
  panel.querySelector('[data-bp="reset"]').addEventListener('click', () => { cells.clear(); start(); view.r = 1 / PHI; view.layer = false; commit(); fit(); });
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
      if (!cells.size) start();
      draw(); renderPanel();
      if (on) { fit(); showHudPrompt(t('bp.prompt.start', lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return cells.size === 0; },
    clear() { cells.clear(); start(); commit(); if (active) fit(); },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the starting cluster at the golden ratio. */
export function breathingPreviewPoints() {
  return startCells().flatMap((q) => cellAt(q, 1 / PHI).V);
}
