// DICTO Icosahedral Cycles: a 3D+ world of two loops (DICTO 2026-10-14, docs/PLAN-CYCLES.md; the name is DICTO's to choose).
// Loop 1, one size: the icosahedron, great dodecahedron, small stellated dodecahedron and great icosahedron share the same 12 corners;
// the corners stay lit while each solid's faces fade into the next (studies/2026-10-14-cycles/loop1.json: the steps keep the edges,
// the face planes, the edges, then only the corners). The side step: from the icosahedron through the dual compound (the rhombic
// triacontahedron outside as glass, the icosidodecahedron inside as solid) to the dodecahedron and the great stellated dodecahedron
// on its 20 corners. Loop 2, growth: the Spheres of Dharma build movie, piece by piece, its named solids arriving in turn until the
// icosahedron returns φ³ larger. All three start on the same icosahedron (edge 1/φ), where the switch changes path. Each station
// has a Build button that opens its kit (the pieces stay in Polyhedraverse and Multi-shell chains). Words in 7 languages (i18n cy.*).
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
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const scale = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
const mean = (P) => scale(P.reduce(add, [0, 0, 0]), 1 / P.length);

// ---- the icosahedron's 12 corners (edge 1/φ, as Dharma's centre) and the dual dodecahedron's 20 (same midradius, 1/2) ----
const ICO = [];
for (const a of [1, -1]) for (const b of [PHI, -PHI]) ICO.push([0, a, b], [a, b, 0], [b, 0, a]);
ICO.forEach((p, i) => { ICO[i] = scale(p, 1 / (2 * PHI)); });
const E1 = 1 / PHI;
const near = (P, a, b, d) => Math.abs(dist(P[a], P[b]) - d) < 1e-9;
const triangles = (d) => {
  const out = [];
  for (let a = 0; a < 12; a++) for (let b = a + 1; b < 12; b++) for (let c = b + 1; c < 12; c++) if (near(ICO, a, b, d) && near(ICO, b, c, d) && near(ICO, a, c, d)) out.push([a, b, c]);
  return out;
};
const ICO_FACES = triangles(E1);
// points round an axis, in order
function aroundAxis(axis, pts) {
  const n = scale(axis, 1 / Math.hypot(...axis)), c = mean(pts);
  const u0 = add(pts[0], scale(c, -1)); const u = scale(u0, 1 / Math.hypot(...u0)); const w = cross(n, u);
  return [...pts].sort((p, q) => Math.atan2(dot(add(p, scale(c, -1)), w), dot(add(p, scale(c, -1)), u)) - Math.atan2(dot(add(q, scale(c, -1)), w), dot(add(q, scale(c, -1)), u)));
}
const RING = ICO.map((v, i) => aroundAxis(v, ICO.filter((_, j) => near(ICO, i, j, E1)))); // each corner's five neighbours
const RD = (1 / PHI ** 2) * Math.sqrt(3) * PHI / 2; // the dual dodecahedron's circumradius (edge 1/φ²)
const DOD = ICO_FACES.map((f) => { const c = mean(f.map((i) => ICO[i])); return scale(c, RD / Math.hypot(...c)); });
const facesAt = (i) => ICO_FACES.map((f, k) => (f.includes(i) ? k : -1)).filter((k) => k >= 0);
const DOD_PENTS = ICO.map((v, i) => aroundAxis(v, facesAt(i).map((k) => DOD[k])));
// the great stellated dodecahedron: in each plane square to a five-fold axis, the dodecahedron's five corners of the second ring, as a pentagram
const GSD_PENTS = ICO.map((v) => {
  const levels = [...new Set(DOD.map((p) => dot(p, v).toFixed(6)))].map(Number).sort((a, b) => b - a);
  return aroundAxis(v, DOD.filter((p) => Math.abs(dot(p, v) - levels[1]) < 1e-6));
});
const MIDS = (f) => f.map((i, k) => mean([ICO[i], ICO[f[(k + 1) % 3]]]));
const ID_FACES = [...ICO_FACES.map(MIDS), ...ICO.map((v, i) => aroundAxis(v, RING[i].map((p) => mean([v, p]))))];
const ICO_EDGES = []; for (let a = 0; a < 12; a++) for (let b = a + 1; b < 12; b++) if (near(ICO, a, b, E1)) ICO_EDGES.push([ICO[a], ICO[b]]);
const RT_FACES = ICO_EDGES.map(([a, b]) => {
  const two = ICO_FACES.filter((f) => [a, b].every((p) => f.some((i) => dist(ICO[i], p) < 1e-9))).map((f) => DOD[ICO_FACES.indexOf(f)]);
  return [a, two[0], b, two[1]];
});
// a polygon's triangles (convex: a fan; a pentagram: centre to each chord)
const fan = (P) => P.slice(1, -1).map((p, k) => [P[0], p, P[k + 2]]);
const star = (P) => { const c = mean(P); return P.map((p, k) => [c, p, P[(k + 2) % 5]]); };
const edgesOf = (polys, step = 1) => polys.flatMap((P) => P.map((p, k) => [p, P[(k + step) % P.length]]));
const ICO_PTS = ICO, BOTH = [...ICO, ...DOD];

// Stations: faces (triangles), edges, lit corners, an optional glass hull, and the Build action.
const ST = {
  icosahedron: { tris: () => ICO_FACES.flatMap((f) => fan(f.map((i) => ICO[i]))), edges: () => ICO_EDGES, corners: ICO_PTS, build: 'tool:polyShape:D20' },
  greatDodecahedron: { tris: () => RING.flatMap(fan), edges: () => ICO_EDGES, corners: ICO_PTS, build: 'tool:polyKit:stars.gd' },
  smallStellatedDodecahedron: { tris: () => RING.flatMap(star), edges: () => edgesOf(RING, 2), corners: ICO_PTS, build: 'tool:polyKit:stars.ssd' },
  greatIcosahedron: { tris: () => triangles(1).flatMap((f) => fan(f.map((i) => ICO[i]))), edges: () => edgesOf(triangles(1).map((f) => f.map((i) => ICO[i]))), corners: ICO_PTS, build: 'tool:polyKit:greatIcosahedron' },
  dualCompound: { tris: () => ID_FACES.flatMap(fan), edges: () => [...ICO_EDGES, ...edgesOf(DOD_PENTS)], corners: BOTH, glass: () => RT_FACES.flatMap(fan), build: null },
  dodecahedron: { tris: () => DOD_PENTS.flatMap(fan), edges: () => edgesOf(DOD_PENTS), corners: DOD, build: 'tool:polyShape:DODECAHEDRON' },
  greatStellatedDodecahedron: { tris: () => GSD_PENTS.flatMap(star), edges: () => edgesOf(GSD_PENTS, 2), corners: DOD, build: 'tool:polyKit:stars.gsd' },
};
const COLOUR = { icosahedron: 0x5fd38a, greatDodecahedron: 0x4dd0e1, smallStellatedDodecahedron: 0xc792ea, greatIcosahedron: 0xf08fc0,
  dualCompound: 0xc792ea, dodecahedron: 0xffc857, greatStellatedDodecahedron: 0xf08fc0 };
// The paths. Loop 1 wraps (its last station is its first); the side step goes out and back by the same slider.
export const PATHS = {
  1: { stations: ['icosahedron', 'greatDodecahedron', 'smallStellatedDodecahedron', 'greatIcosahedron', 'icosahedron'], keeps: ['edges', 'planes', 'edges', 'corners'] },
  3: { stations: ['icosahedron', 'dualCompound', 'dodecahedron', 'greatStellatedDodecahedron'], keeps: ['dual', 'dualOut', 'dodCorners'] },
};
export const LOOP1 = PATHS[1].stations.slice(0, 4).map((key) => ({ key }));
export const LOOP1_KEEPS = PATHS[1].keeps;
export const GEOMETRY = { ICO, DOD, GSD_PENTS, ID_FACES, RT_FACES, DOD_PENTS }; // for tests

// ---- Loop 2: the Spheres of Dharma cycle movie ----
const DHARMA = CHAINS_DATA.dharma.views.cycle;
const FILM = filmOrder(DHARMA, MOVIE.dharma.cycle);
export const LOOP2_STATIONS = FILM.ends.filter((e) => e.name).map((e) => ({ at: e.at, key: e.name }));
const solidName = (k, L) => (k === 'hecatodihedron' ? 'DICTO Truncated-Icosahedral Hecatodihedron' : k === 'dualCompound' ? t('cy.dualCompound', L) : t(`solid.${k}`, L));

export function createCyclesWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, openAction = () => {} }) {
  const STORAGE_KEY = storageKey('cycles');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { loop: 1, t1: 0, t2: 1, t3: 0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if ([1, 2, 3].includes(d?.loop)) view.loop = d.loop;
    if (Number.isFinite(d?.t1)) view.t1 = Math.max(0, Math.min(4, d.t1));
    if (Number.isInteger(d?.t2)) view.t2 = Math.max(1, Math.min(FILM.seq.length, d.t2));
    if (Number.isFinite(d?.t3)) view.t3 = Math.max(0, Math.min(3, d.t3));
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };

  let active = false, skeleton = false, opacity = 1;
  const meshes = [];
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry?.dispose(); child.material?.dispose?.(); }
    meshes.length = 0;
  }
  const W = (p) => scale(p, WS);
  const cornerGeom = new THREE.SphereGeometry(0.03 * WS, 16, 12);
  function triMesh(tris, colour, alpha) {
    const pos = [];
    for (const tri of tris) for (const p of tri) pos.push(...W(p));
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    const m = new THREE.MeshStandardMaterial({ color: colour, side: THREE.DoubleSide, flatShading: true, transparent: alpha < 1, opacity: alpha, depthWrite: alpha >= 1,
      polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
    const mesh = new THREE.Mesh(g, m); mesh.visible = !skeleton; return mesh;
  }
  function lines(pairs, colour, alpha) {
    const pos = pairs.flatMap(([a, b]) => [...W(a), ...W(b)]);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    return new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: colour, transparent: alpha < 1, opacity: alpha }));
  }
  const ekey = ([a, b]) => [a, b].map((p) => p.map((x) => x.toFixed(5)).join(',')).sort().join('|');
  // where a path's slider is: the station before, the one after, and how far between (0..1)
  const tOf = () => (view.loop === 1 ? view.t1 : view.t3);
  function between() {
    const path = PATHS[view.loop], tt = tOf(), last = path.stations.length - 1;
    const i = Math.min(Math.floor(tt), last), j = Math.min(i + 1, last), f = i === last ? 0 : tt - i;
    return { path, i, j, f };
  }
  function drawPath() {
    const { path, i, j, f } = between();
    const A = ST[path.stations[i]], B = ST[path.stations[j]];
    const a = (1 - f) * opacity, b = f * opacity;
    if (a > 0.01) group.add(triMesh(A.tris(), COLOUR[path.stations[i]], a));
    if (b > 0.01) group.add(triMesh(B.tris(), COLOUR[path.stations[j]], b));
    if (A.glass && 1 - f > 0.01) group.add(triMesh(A.glass(), 0x9fd8ff, 0.18 * (1 - f)));
    if (B.glass && f > 0.01) group.add(triMesh(B.glass(), 0x9fd8ff, 0.18 * f));
    // edges: those both stations have stay solid through the change
    const edgeCol = skeleton ? 0xd8f0ff : 0x0b1220;
    const ea = A.edges(), eb = B.edges(), kb = new Set(eb.map(ekey)), ka = new Set(ea.map(ekey));
    const shared = ea.filter((e) => kb.has(ekey(e)));
    if (shared.length) group.add(lines(shared, edgeCol, 1));
    const onlyA = ea.filter((e) => !kb.has(ekey(e))), onlyB = eb.filter((e) => !ka.has(ekey(e)));
    if (onlyA.length && 1 - f > 0.01) group.add(lines(onlyA, edgeCol, 1 - f));
    if (onlyB.length && f > 0.01) group.add(lines(onlyB, edgeCol, f));
    // corners: lit while both stations have them, fading otherwise
    const ck = (p) => p.map((x) => x.toFixed(5)).join(',');
    const ca = new Set(A.corners.map(ck)), cb = new Set(B.corners.map(ck));
    const all = new Map([...A.corners, ...B.corners].map((p) => [ck(p), p]));
    for (const [k, p] of all) {
      const alpha = ca.has(k) && cb.has(k) ? 1 : ca.has(k) ? 1 - f : f;
      if (alpha < 0.02) continue;
      const m = new THREE.Mesh(cornerGeom, new THREE.MeshStandardMaterial({ color: CORNER, emissive: CORNER, emissiveIntensity: 0.6, transparent: alpha < 1, opacity: alpha }));
      m.position.set(...W(p)); group.add(m);
    }
  }
  function drawLoop2() {
    const n = view.t2, buf = { pos: [], col: [], line: [] }, colour = new THREE.Color();
    for (let r = 0; r < n; r++) {
      const [role, Vp, F] = DHARMA[FILM.seq[r]];
      colour.setHex(r === n - 1 ? ORANGE : ROLE[role] ?? 0x9fb4c8);
      for (const face of F) {
        const Q = face.map((k) => W(Vp[k]));
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
    if (view.loop === 2) drawLoop2(); else drawPath();
  }
  const radius = () => {
    if (view.loop !== 2) return 0.62 * WS; // every station of Loop 1 and the side step lies within the icosahedron's corners or the dodecahedron's
    let r = 0.6;
    for (let k = 0; k < view.t2; k++) for (const p of DHARMA[FILM.seq[k]][1]) r = Math.max(r, Math.hypot(...p));
    return r * WS;
  };
  const fit = () => fitView([0, 0, 0], radius() * 1.15);

  const panel = document.createElement('div');
  panel.id = 'worldcycles-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options"><button type="button" data-cy-loop="1"></button><button type="button" data-cy-loop="3"></button><button type="button" data-cy-loop="2"></button></div>
    <div class="w4d-row st-note cy-note"></div>
    <div class="w4d-row st-note cy-station"></div>
    <div class="w4d-row w4d-options"><button type="button" data-cy-build hidden></button></div>
    <div class="w4d-row cy-slider-row"><input type="range" class="st-slider cy-slider" min="0" step="1" aria-label=""></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'cycles');
  const slider = panel.querySelector('.cy-slider');
  const buildBtn = panel.querySelector('[data-cy-build]');
  let buildAction = null;
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelectorAll('[data-cy-loop]').forEach((b) => { const n = Number(b.dataset.cyLoop); b.textContent = t(`cy.loop${n}`, L); b.setAttribute('aria-pressed', String(view.loop === n)); });
    panel.querySelector('.cy-note').textContent = t(`cy.note${view.loop}`, L);
    slider.setAttribute('aria-label', t('cy.slider', L));
    let line, at = null;
    if (view.loop === 2) {
      slider.min = '1'; slider.max = String(FILM.seq.length); slider.value = String(view.t2);
      const st = [...LOOP2_STATIONS].reverse().find((s) => s.at <= view.t2);
      const last = view.t2 === FILM.seq.length;
      line = `${t('cy.pieces', L, { n: view.t2, total: FILM.seq.length })}${st ? ` · ${last ? t('cy.bigger', L) : solidName(st.key, L)}` : ''}`;
      buildAction = 'tool:chainsWorld:dharma';
    } else {
      const { path, i, j, f } = between(), last = path.stations.length - 1;
      slider.min = '0'; slider.max = String(last * 100); slider.value = String(Math.round(tOf() * 100));
      if (f < 0.02 || f > 0.98) {
        at = path.stations[f > 0.98 ? j : i];
        line = `${solidName(at, L)}${view.loop === 1 && tOf() >= last - 0.02 ? ` · ${t('cy.again', L)}` : ''}`;
      } else line = `${solidName(path.stations[i], L)} → ${solidName(path.stations[j], L)} · ${t(`cy.keep.${path.keeps[i]}`, L)}`;
      buildAction = at ? ST[at].build : null;
    }
    panel.querySelector('.cy-station').textContent = line;
    buildBtn.hidden = !buildAction;
    buildBtn.textContent = t(view.loop === 2 ? 'cy.build.dharma' : 'cy.build', L);
  }
  slider.addEventListener('input', () => {
    const v = Number(slider.value);
    if (view.loop === 2) view.t2 = v;
    else { let x = v / 100; const r = Math.round(x); if (Math.abs(x - r) < 0.06) x = r; if (view.loop === 1) view.t1 = x; else view.t3 = x; } // settles on each station
    save(); draw(); renderPanel();
  });
  slider.addEventListener('change', () => { if (view.loop !== 1) fit(); });
  panel.querySelectorAll('[data-cy-loop]').forEach((b) => b.addEventListener('click', () => {
    // the switch happens at the shared icosahedron: each path starts there
    view.loop = Number(b.dataset.cyLoop); view.t1 = 0; view.t2 = 1; view.t3 = 0;
    save(); draw(); renderPanel(); fit();
  }));
  buildBtn.addEventListener('click', () => { if (buildAction) openAction(buildAction); });
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
    clear() { view.t1 = 0; view.t2 = 1; view.t3 = 0; save(); draw(); renderPanel(); },
    snapshot: () => ({ version: 1, ...view }),
    restore(j) {
      view.loop = [1, 2, 3].includes(j?.loop) ? j.loop : 1;
      if (Number.isFinite(j?.t1)) view.t1 = j.t1; if (Number.isInteger(j?.t2)) view.t2 = j.t2; if (Number.isFinite(j?.t3)) view.t3 = j.t3;
      save(); draw(); renderPanel();
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the shared icosahedron's 12 corners. */
export function cyclesPreviewPoints() {
  return ICO.map((p) => scale(p, WS));
}
