// DICTO Icosahedral Cycles: a 3D+ world of two loops (DICTO 2026-10-14, docs/PLAN-CYCLES.md; the name is DICTO's to choose).
// Loop 1, one size: the icosahedron, great dodecahedron, small stellated dodecahedron and great icosahedron share the same 12 corners;
// the corners stay lit while each solid's faces fade into the next (studies/2026-10-14-cycles/loop1.json: the steps keep the edges,
// the face planes, the edges, then only the corners). Loop 2, growth: the Spheres of Dharma build movie, piece by piece, its named
// solids arriving in turn until the icosahedron returns φ³ larger. Both start on the same icosahedron (edge 1/φ), where the loop
// switch changes loop. Words in all 7 languages (i18n cy.*).
import * as THREE from 'three';
import CHAINS_DATA from './seeds-data.js';
import MOVIE from './movie-names.js';
import { ROLE, filmOrder } from './world-chains.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const lang = () => getSettings().language;
const ORANGE = 0xff9a52;
const CORNER = 0xffc857;
const STATION_COLOUR = [0x5fd38a, 0x4dd0e1, 0xc792ea, 0xf08fc0];

// ---- Loop 1: four solids on the icosahedron's 12 corners (edge 1/φ, as Dharma's centre) ----
const V = [];
for (const a of [1, -1]) for (const b of [PHI, -PHI]) V.push([0, a, b], [a, b, 0], [b, 0, a]);
const S = 1 / (2 * PHI); // edge 2 -> edge 1/φ
const CORNERS = V.map((p) => p.map((x) => x * S));
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
const E1 = 1 / PHI, E2 = 1;
const near = (a, b, d) => Math.abs(dist(CORNERS[a], CORNERS[b]) - d) < 1e-9;
const triangles = (d) => {
  const out = [];
  for (let a = 0; a < 12; a++) for (let b = a + 1; b < 12; b++) for (let c = b + 1; c < 12; c++) if (near(a, b, d) && near(b, c, d) && near(a, c, d)) out.push([a, b, c]);
  return out;
};
// the five neighbours of a corner, in order round it
function ring(i) {
  const nb = CORNERS.map((_, j) => j).filter((j) => near(i, j, E1));
  const c = CORNERS[i], n = c.map((x) => x / Math.hypot(...c));
  const a0 = CORNERS[nb[0]].map((x, k) => x - c[k]); const u = a0.map((x) => x / Math.hypot(...a0));
  const w = [n[1] * u[2] - n[2] * u[1], n[2] * u[0] - n[0] * u[2], n[0] * u[1] - n[1] * u[0]];
  const ang = (j) => { const d = CORNERS[j].map((x, k) => x - c[k]); return Math.atan2(d[0] * w[0] + d[1] * w[1] + d[2] * w[2], d[0] * u[0] + d[1] * u[1] + d[2] * u[2]); };
  return nb.sort((p, q) => ang(p) - ang(q));
}
const pentagons = CORNERS.map((_, i) => ring(i));
// A station: its faces as triangles (corner indices; a pentagram as five triangles centre–chord, the centre as index -1-face) and edges.
export const LOOP1 = [
  { key: 'icosahedron', faces: triangles(E1).map((f) => [f]), edges: 'short' },
  { key: 'greatDodecahedron', faces: pentagons.map((p) => [[p[0], p[1], p[2]], [p[0], p[2], p[3]], [p[0], p[3], p[4]]]), edges: 'short' },
  { key: 'smallStellatedDodecahedron', faces: pentagons.map((p) => [0, 1, 2, 3, 4].map((k) => ['c', p[k], p[(k + 2) % 5], p])), edges: 'long' },
  { key: 'greatIcosahedron', faces: triangles(E2).map((f) => [f]), edges: 'long' },
];
// What each step keeps (loop1.json): edges, planes, edges, corners only.
export const LOOP1_KEEPS = ['edges', 'planes', 'edges', 'corners'];
const edgeList = (d) => { const out = []; for (let a = 0; a < 12; a++) for (let b = a + 1; b < 12; b++) if (near(a, b, d)) out.push([a, b]); return out; };
const EDGES = { short: edgeList(E1), long: edgeList(E2) };

// ---- Loop 2: the Spheres of Dharma cycle movie ----
const DHARMA = CHAINS_DATA.dharma.views.cycle;
const FILM = filmOrder(DHARMA, MOVIE.dharma.cycle);
export const LOOP2_STATIONS = FILM.ends.filter((e) => e.name).map((e) => ({ at: e.at, key: e.name }));
const solidName = (k, L) => (k === 'hecatodihedron' ? 'DICTO Truncated-Icosahedral Hecatodihedron' : t(`solid.${k}`, L));

export function createCyclesWorld({ scene, fitView = () => {}, showHudPrompt = () => {} }) {
  const STORAGE_KEY = storageKey('cycles');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { loop: 1, t1: 0, t2: 1 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (d?.loop === 2) view.loop = 2;
    if (Number.isFinite(d?.t1)) view.t1 = Math.max(0, Math.min(4, d.t1));
    if (Number.isInteger(d?.t2)) view.t2 = Math.max(1, Math.min(FILM.seq.length, d.t2));
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };

  let active = false, skeleton = false, opacity = 1;
  const meshes = [];
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry?.dispose(); child.material?.dispose?.(); }
    meshes.length = 0;
  }
  const P = (i) => CORNERS[i].map((x) => x * WS);
  const cornerGeom = new THREE.SphereGeometry(0.035 * WS, 16, 12);
  function triMesh(tris, colour, alpha) {
    const pos = [];
    for (const tri of tris) for (const p of tri) pos.push(...p);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    const m = new THREE.MeshStandardMaterial({ color: colour, side: THREE.DoubleSide, flatShading: true, transparent: alpha < 1, opacity: alpha, depthWrite: alpha >= 1,
      polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
    const mesh = new THREE.Mesh(g, m); mesh.visible = !skeleton; return mesh;
  }
  function lines(pairs, colour, alpha) {
    const pos = pairs.flatMap(([a, b]) => [...a, ...b]);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    return new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: colour, transparent: alpha < 1, opacity: alpha }));
  }
  function stationTris(s) {
    const out = [];
    for (const face of LOOP1[s].faces) for (const tri of face) {
      if (tri[0] === 'c') { const [, a, b, p] = tri; const c = p.map(P).reduce((x, y) => x.map((v, k) => v + y[k] / 5), [0, 0, 0]); out.push([c, P(a), P(b)]); }
      else out.push(tri.map(P));
    }
    return out;
  }
  const station = () => Math.round(view.t1) % 4;
  function drawLoop1() {
    const i = Math.floor(view.t1) % 4, j = (i + 1) % 4, f = view.t1 - Math.floor(view.t1);
    const a = (1 - f) * opacity, b = f * opacity;
    if (a > 0.01) group.add(triMesh(stationTris(i), STATION_COLOUR[i], Math.min(a, opacity)));
    if (b > 0.01 && view.t1 < 4) group.add(triMesh(stationTris(j), STATION_COLOUR[j], b));
    // edges: kept ones stay solid through the change
    const ei = EDGES[LOOP1[i].edges], ej = EDGES[LOOP1[j].edges], same = LOOP1[i].edges === LOOP1[j].edges;
    const edgeCol = skeleton ? 0xd8f0ff : 0x0b1220;
    if (same || f < 0.01) group.add(lines(ei.map(([p, q]) => [P(p), P(q)]), edgeCol, 1));
    else { group.add(lines(ei.map(([p, q]) => [P(p), P(q)]), edgeCol, 1 - f)); group.add(lines(ej.map(([p, q]) => [P(p), P(q)]), edgeCol, f)); }
    for (let k = 0; k < 12; k++) { const m = new THREE.Mesh(cornerGeom, new THREE.MeshStandardMaterial({ color: CORNER, emissive: CORNER, emissiveIntensity: 0.6 })); m.position.set(...P(k)); group.add(m); }
  }
  function drawLoop2() {
    const n = view.t2, buf = { pos: [], col: [], line: [] }, colour = new THREE.Color();
    for (let r = 0; r < n; r++) {
      const [role, Vp, F] = DHARMA[FILM.seq[r]];
      colour.setHex(r === n - 1 ? ORANGE : ROLE[role] ?? 0x9fb4c8);
      for (const face of F) {
        const Q = face.map((k) => Vp[k].map((x) => x * WS));
        for (let m = 1; m + 1 < Q.length; m++) for (const p of [Q[0], Q[m], Q[m + 1]]) { buf.pos.push(...p); buf.col.push(colour.r, colour.g, colour.b); }
        Q.forEach((p, m) => buf.line.push(...p, ...Q[(m + 1) % Q.length]));
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(buf.col, 3)); g.computeVertexNormals();
    const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: opacity < 1, opacity, depthWrite: opacity >= 1,
      polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }));
    mesh.visible = !skeleton; group.add(mesh); meshes.push(mesh);
    const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(buf.line, 3));
    group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x0b1220 })));
  }
  function draw() {
    clearGroup();
    if (!active) return;
    if (view.loop === 1) drawLoop1(); else drawLoop2();
  }
  const radius = () => {
    if (view.loop === 1) return 0.62 * WS;
    let r = 0.6;
    for (let k = 0; k < view.t2; k++) for (const p of DHARMA[FILM.seq[k]][1]) r = Math.max(r, Math.hypot(...p));
    return r * WS;
  };
  const fit = () => fitView([0, 0, 0], radius() * 1.15);

  const panel = document.createElement('div');
  panel.id = 'worldcycles-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options"><button type="button" data-cy-loop="1"></button><button type="button" data-cy-loop="2"></button></div>
    <div class="w4d-row st-note cy-note"></div>
    <div class="w4d-row st-note cy-station"></div>
    <div class="w4d-row cy-slider-row"><input type="range" class="st-slider cy-slider" min="0" step="1" aria-label=""></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'cycles');
  const slider = panel.querySelector('.cy-slider');
  const KEEP_AT = (i) => LOOP1_KEEPS[i];
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelectorAll('[data-cy-loop]').forEach((b) => { const n = Number(b.dataset.cyLoop); b.textContent = t(`cy.loop${n}`, L); b.setAttribute('aria-pressed', String(view.loop === n)); });
    panel.querySelector('.cy-note').textContent = t(`cy.note${view.loop}`, L);
    slider.setAttribute('aria-label', t('cy.slider', L));
    let line;
    if (view.loop === 1) {
      slider.max = '400'; slider.value = String(Math.round(view.t1 * 100));
      const f = view.t1 - Math.floor(view.t1), i = Math.floor(view.t1) % 4;
      line = f < 0.02 || f > 0.98 ? `${t(`solid.${LOOP1[station()].key}`, L)}${view.t1 >= 3.98 ? ` · ${t('cy.again', L)}` : ''}`
        : `${t(`solid.${LOOP1[i].key}`, L)} → ${t(`solid.${LOOP1[(i + 1) % 4].key}`, L)} · ${t(`cy.keep.${KEEP_AT(i)}`, L)}`;
    } else {
      slider.min = '1'; slider.max = String(FILM.seq.length); slider.value = String(view.t2);
      const st = [...LOOP2_STATIONS].reverse().find((s) => s.at <= view.t2);
      const last = view.t2 === FILM.seq.length;
      line = `${t('cy.pieces', L, { n: view.t2, total: FILM.seq.length })}${st ? ` · ${last ? t('cy.bigger', L) : solidName(st.key, L)}` : ''}`;
    }
    if (view.loop === 1) slider.min = '0';
    panel.querySelector('.cy-station').textContent = line;
  }
  slider.addEventListener('input', () => {
    const v = Number(slider.value);
    if (view.loop === 1) {
      let x = v / 100; const r = Math.round(x); if (Math.abs(x - r) < 0.06) x = r; // settles on each station
      view.t1 = x;
    } else view.t2 = v;
    save(); draw(); renderPanel();
  });
  slider.addEventListener('change', () => { if (view.loop === 2) fit(); });
  panel.querySelectorAll('[data-cy-loop]').forEach((b) => b.addEventListener('click', () => {
    // the switch happens at the shared icosahedron: each loop starts there
    view.loop = Number(b.dataset.cyLoop); view.t1 = 0; view.t2 = 1;
    save(); draw(); renderPanel(); fit();
  }));
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => meshes,
    handleTap: () => false,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      draw(); renderPanel();
      if (on) { fit(); showHudPrompt(t('cy.prompt', lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { view.t1 = 0; view.t2 = 1; save(); draw(); renderPanel(); },
    snapshot: () => ({ version: 1, ...view }),
    restore(j) { if (j?.loop === 2) view.loop = 2; else view.loop = 1; if (Number.isFinite(j?.t1)) view.t1 = j.t1; if (Number.isInteger(j?.t2)) view.t2 = j.t2; save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the shared icosahedron's 12 corners. */
export function cyclesPreviewPoints() {
  return CORNERS.map((p) => p.map((x) => x * WS));
}
