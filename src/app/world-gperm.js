// Generalized Permutohedra (Postnikov 2009): the deformation cone of the 3D permutohedron as its own world, beside The 4D Permutohedron.
// DICTO · dictospheres.com
// Every shape you get from the permutohedron by sliding its 14 faces in or out, each staying parallel to itself (gperm-geometry.js).
//   One big slider at the bottom walks from the permutohedron to Loday's associahedron one face at a time (DICTO's choice, 2026-11-12):
//     the five faces over non-interval subsets slide out in turn, each to nothing, every point in the family (gperm-geometry.js
//     STAGE_ORDER); a wall mark on the track at each vanishing. The heights are the k-research study's (gperm-walls.js, unit-tested).
//   Stops, a tap each: simplex, cube, hypersimplex, cyclohedron, associahedron, permutohedron (DICTO's order). No step arrows.
//   A live badge: fills space by translation or not (the Venkov–McMullen test on the shape drawn).
// Drawn to the app's render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, crisp antialiased edges. The faces are
// coloured by how many of the four numbers their subset holds (1, 2 or 3). Words in all 7 languages (i18n gp.*).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import * as G from './gperm-geometry.js';

export const GP_TITLE = 'Generalized Permutohedra';
export const GP_STOPS = G.PRESET_KEYS;
export const GP_COLOURS = { 1: 0xe7d9b4, 2: 0x5fa6b8, 3: 0xe07a92, edge: 0xf4f1e6 };   // light edges, as the reference Kepler–Poinsot stars: the outline reads on the dark sky
const PER = 100;                                   // slider steps per unit of height moved
const STEPS = G.STAGE_TOTAL * PER;                // 700: the walls fall on whole steps
const VIEW_DIR = [3.2, 2.1, 4.0];
const lang = () => getSettings().language;
const hex = (c) => `#${new THREE.Color(c).getHexString()}`;

/** The staged route's walls: { t (0..1 along the slider), at (slider step), face ('{1,3}') }. */
export function gpWalls() { return G.STAGE_WALLS.map((w) => ({ t: w.s / G.STAGE_TOTAL, at: w.s * PER, face: G.setLabel(w.face) })); }

/** Corners centred and scaled to radius 1 (the picture keeps its size along the slider and at every stop). */
function normalised(P3) {
  const c = [0, 1, 2].map((k) => P3.reduce((s, p) => s + p[k], 0) / P3.length);
  const Q = P3.map((p) => p.map((v, k) => v - c[k])), r = Math.max(...Q.map((p) => Math.hypot(...p))) || 1;
  return Q.map((p) => p.map((v) => v / r));
}

export function createGpermWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('gperm');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // stop: a named member off the route, or null on the route at step s (0 the permutohedron … STEPS the associahedron)
  const view = { stop: null, s: 0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (Number.isFinite(d?.s)) view.s = Math.max(0, Math.min(STEPS, Math.round(d.s)));
    if (GP_STOPS.includes(d?.stop) && d.stop !== 'permutohedron' && d.stop !== 'associahedron') view.stop = d.stop;
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  const walls = gpWalls();
  let active = false, skeleton = false, opacity = 1, shown = null;

  /** The stop shown: a named member, the line's ends by name, or null between. */
  const stopShown = () => view.stop ?? (view.s === 0 ? 'permutohedron' : view.s === STEPS ? 'associahedron' : null);
  const shapeNow = () => (view.stop ? G.shapeOf(G.PRESETS[view.stop]) : G.shapeOfZ(G.stagedZ(view.s / PER)));

  const clear = () => { for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  /** Polygons (3D loops, radius 1) in one colour as one mesh, and their crisp edges. */
  function polys(loops, col, op) {
    if (!loops.length || skeleton) return;
    const pos = [];
    for (const P0 of loops) { const P = P0.map((p) => p.map((x) => x * WS)); for (let i = 1; i + 1 < P.length; i++) pos.push(...P[0], ...P[i], ...P[i + 1]); }
    const see = op < 1, g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const mat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.55, side: THREE.DoubleSide, flatShading: true, transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, emissive: new THREE.Color(col).multiplyScalar(0.12) });
    if (see) mat.userData.hollow = true;
    const m = new THREE.Mesh(g, mat); m.frustumCulled = false; if (see) m.renderOrder = 4; group.add(m);
  }
  function draw() {
    if (!active) return;
    clear();
    const sh = shapeNow(), P = normalised(sh.poly.P3);
    for (const k of [1, 2, 3]) polys(sh.poly.faces.filter((f) => G.popcount(f.S) === k).map((f) => f.loop.map((i) => P[i])), GP_COLOURS[k], opacity);
    const lines = sh.poly.edges.flatMap(([a, b]) => [...P[a].map((x) => x * WS), ...P[b].map((x) => x * WS)]);
    const see = opacity < 1 || skeleton;
    const l = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color: skeleton ? 0xdfe6f0 : GP_COLOURS.edge, linewidth: 1.8, transparent: opacity < 1, opacity: opacity < 1 ? 0.8 : 1, depthWrite: !see }));
    l.geometry.setPositions(lines); l.frustumCulled = false; group.add(l);
    const wallHere = view.stop ? null : walls.find((w) => w.at === view.s) ?? null;
    shown = { stop: stopShown(), onLine: !view.stop, s: view.s, f: sh.poly.f, faces: sh.poly.faces.map((f) => G.setLabel(f.S)), inFamily: sh.inFamily,
      stage: view.stop || view.s === 0 ? null : G.stageAt(view.s / PER) + 1, fills: sh.fill.fills, symmetric: sh.fill.symmetric, facesSymmetric: sh.fill.facesSymmetric, belts: sh.fill.belts, wall: wallHere };
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], WS * 1.08, VIEW_DIR, true);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldgperm-panel';
  panel.className = 'qc-panel';
  const tick = (w) => `<i class="gp-wall" aria-hidden="true" style="left:calc(20px + ${w.t.toFixed(6)} * (100% - 40px))"></i>`;
  panel.innerHTML = `
    <div class="w4d-row w4d-options gp-stops">${GP_STOPS.map((k) => `<button type="button" data-gp-stop="${k}"></button>`).join('')}</div>
    <div class="w4d-row gp-badge-row"><span class="gp-badge" role="status"></span></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row gp-legend"></div>
    <div class="w4d-row gp-line-row"><label class="hull-pick"><span class="gp-line-label"></span><span class="gp-track"><input type="range" class="st-slider" min="0" max="${STEPS}" step="1">${walls.map(tick).join('')}</span></label></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'gperm');
  const lineInput = panel.querySelector('.gp-line-row input');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold'), legend = panel.querySelector('.gp-legend'), badge = panel.querySelector('.gp-badge');
  note.addEventListener('click', () => note.classList.toggle('open'));
  const press = (x, on) => { x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), stop = stopShown();
    panel.querySelectorAll('[data-gp-stop]').forEach((x) => { x.textContent = t(`gp.stop.${x.dataset.gpStop}`, L); press(x, x.dataset.gpStop === stop); });
    badge.textContent = t(shown.fills ? 'gp.badge.yes' : 'gp.badge.no', L);
    badge.title = t('gp.badge.tip', L);
    badge.classList.toggle('gp-fills', shown.fills);
    badge.dataset.fills = String(shown.fills);
    const k = G.stageAt(view.s / PER), name = stop ? t(`gp.stop.${stop}`, L) : t('gp.cap.stage', L, { k: k + 1, n: walls.length, face: walls[k].face });
    const [v, e, f] = shown.f;
    caption.textContent = t('gp.cap', L, { name, v, e, f }) + (view.stop ? ` · ${t('gp.cap.off', L)}` : '') + (shown.wall ? ` · ${t('gp.cap.wall', L, { face: shown.wall.face })}` : '');
    const sw = (k) => `<span class="gp-sw"><i style="background:${hex(GP_COLOURS[k])}"></i>${t(`gp.legend.${k}`, L)}</span>`;
    legend.innerHTML = [1, 2, 3].map(sw).join('');
    panel.querySelector('.gp-line-label').textContent = t('gp.line', L, { p: Math.round((view.s / STEPS) * 100) });
    lineInput.value = String(view.s);
    lineInput.setAttribute('aria-label', t('gp.line', L, { p: Math.round((view.s / STEPS) * 100) }));
    note.textContent = `${t('gp.note', L)} ${t('gp.note.line', L)} ${t('gp.note.fill', L)} ${t('gp.note.credits', L)}`;
  }
  // the slider is the line: moving it leaves any off-line stop
  lineInput.addEventListener('input', () => { const s = Number(lineInput.value); if (s === view.s && !view.stop) return; view.s = s; view.stop = null; save(); draw(); });
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('[data-gp-stop]');
    if (!b) return;
    setStop(b.dataset.gpStop);
  });
  function setStop(k) {
    if (k === 'permutohedron') Object.assign(view, { stop: null, s: 0 });
    else if (k === 'associahedron') Object.assign(view, { stop: null, s: STEPS });
    else view.stop = k;
    save(); draw();
  }
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    /** ?open=gperm:<stop>: that member. */
    setChain(k) { if (!GP_STOPS.includes(k)) return; setStop(k); },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      draw(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);
    },
    resetView() { Object.assign(view, { stop: null, s: 0 }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe). */
    probe: () => (shown ? { ...shown, walls, meshes: group.children.length } : null),
  };
}

/** The world's cover in the DICTO menu: the edges of the shape halfway along the route. */
export function gpermPreviewEdges() {
  const { poly } = G.shapeOfZ(G.stagedZ(G.STAGE_TOTAL / 2)), P = normalised(poly.P3);
  return poly.edges.map(([a, b]) => [P[a], P[b]]);
}
