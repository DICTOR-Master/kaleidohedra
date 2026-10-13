// Icosahedral Octet Lattice (DICTO 2026-10-13): the DICTO Icosahedral Octet (#21) to build, cell by cell or a cluster at a time, in
// the section after the Sunstar Lattice; the growing views stay in the octet world (world-octet.js). Five versions, each a set of
// sites with the cell that sits there (cells from octet-data.js, the same as the views):
//   caps, allIco, pyrochlore: octahedra (icosahedron + 6 Admiral Caps) at the octet's octahedral sites, tetrahedra between them
//     (Weirdstones and Tadpoles round a small icosahedron in the all-icosahedral octet; pyrochlore's own tetrahedra coloured);
//   frog: the icosahedra and small icosahedra, and a Frog Chorus star on the other octahedral sites;
//   lotusJewel: Lotus Jewels, and the dodecahedral voids between them.
// Sites are integer points q (units of a/4, or φ/2 for the Lotus Jewel); every cell's neighbours across its faces are q + (±1, ±1, ±1).
// A tap on a cell adds the empty neighbour on that side (or, in a cluster entry, a whole octahedron or jewel with its eight
// neighbours); long-press (chisel) removes one. Words: i18n octb.*.
import * as THREE from 'three';
import OCTET from './octet-data.js';
import { ROLE } from './world-chains.js';
import { pyro } from './world-octet.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const { a: A, phi: PHI, cells: C } = OCTET;
export const OCTET_BUILD_KINDS = ['caps', 'allIco', 'frog', 'pyrochlore', 'lotusJewel'];
const GLASS_ROLES = new Set(['octGlass', 'tetGlass']);
const DIAG = [-1, 1].flatMap((x) => [-1, 1].flatMap((y) => [-1, 1].map((z) => [x, y, z])));
const mod = (n, m) => ((n % m) + m) % m;
const allEven = (q) => q.every((c) => mod(c, 2) === 0);
const allOdd = (q) => q.every((c) => mod(c, 2) === 1);
const keyOf = (q) => q.join(',');
const lang = () => getSettings().language;

// One cell at a place, or turned inside out through its middle (the octet's other tetrahedra), as in world-octet.js.
const put = (cell, t0, invert = false, role = null) => cell.map(([r, V, F]) => [role ?? r,
  V.map((v) => v.map((x, i) => (invert ? -x : x) + t0[i])), invert ? F.map((f) => [...f].reverse()) : F]);

/** What sits at site q in a version: { hub, pieces } (hub: an octahedron or jewel site, the centre of a cluster), or null. */
export function cellAt(kind, q) {
  if (kind === 'lotusJewel') {
    const p = q.map((c) => (c * PHI) / 2);
    if (allEven(q)) return { hub: true, pieces: put(C.lotusJewel, p) };
    if (allOdd(q)) return { hub: false, pieces: put(C.voidDodeca, p) };
    return null;
  }
  const p = q.map((c) => (c * A) / 4);
  if (allEven(q)) {
    const even = mod(q.reduce((s, c) => s + c / 2, 0), 2) === 0;
    if (kind === 'frog') return { hub: even, pieces: even ? put(C.oct.slice(0, 1), p) : put(C.frog, p) };
    if (!even) return null;
    return { hub: true, pieces: put(C.oct, p, false, kind === 'pyrochlore' ? 'octGlass' : null) };
  }
  if (allOdd(q)) {
    const invert = mod(q.reduce((s, c) => s + c, 0), 4) === 1;
    if (kind === 'allIco') return { hub: false, pieces: put(C.tetIco, p, invert) };
    if (kind === 'frog') return { hub: false, pieces: put(C.tetIco.slice(0, 1), p, invert) };
    if (kind === 'pyrochlore') return { hub: false, pieces: put(C.tet, p, invert, pyro(q) ? (invert ? 'pyroDown' : 'pyroUp') : 'tetGlass') };
    return { hub: false, pieces: put(C.tet, p, invert) };
  }
  return null;
}
const unit = (kind) => (kind === 'lotusJewel' ? PHI / 2 : A / 4);
export const neighbours = (kind, q) => DIAG.map((d) => q.map((c, i) => c + d[i])).filter((n) => cellAt(kind, n));
const START = [0, 0, 0];

export function createOctetBuildWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('octetBuild');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { kind: 'caps', clusters: false };
  const builds = Object.fromEntries(OCTET_BUILD_KINDS.map((k) => [k, new Map()])); // per version: key -> q
  const cells = () => builds[view.kind];
  function read(d) {
    if (OCTET_BUILD_KINDS.includes(d?.kind)) view.kind = d.kind;
    view.clusters = d?.clusters === true;
    for (const k of OCTET_BUILD_KINDS) {
      builds[k].clear();
      for (const q of Array.isArray(d?.builds?.[k]) ? d.builds[k] : []) if (Array.isArray(q) && q.length === 3 && q.every(Number.isInteger) && cellAt(k, q)) builds[k].set(keyOf(q), q);
    }
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: empty */ }
  const snapshot = () => ({ version: 1, kind: view.kind, clusters: view.clusters, builds: Object.fromEntries(OCTET_BUILD_KINDS.map((k) => [k, [...builds[k].values()]])) });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const commit = () => { save(); draw(); renderPanel(); onChange(); };

  let active = false, skeleton = false, opacity = 1;
  const solid = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.22, depthWrite: false });
  let pickTargets = [];
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
    pickTargets = [];
  }
  function draw() {
    clearGroup();
    if (!active) return;
    const buf = { solid: { pos: [], col: [], line: [], rec: [] }, glass: { pos: [], col: [], line: [], rec: [] } };
    const colour = new THREE.Color();
    for (const q of cells().values()) {
      for (const [role, V, F] of cellAt(view.kind, q).pieces) {
        const b = GLASS_ROLES.has(role) ? buf.glass : buf.solid;
        const P = V.map((p) => p.map((c) => c * WS));
        colour.setHex(ROLE[role] ?? 0xb8c4bd);
        for (const f of F) {
          for (let i = 1; i + 1 < f.length; i++) {
            for (const k of [f[0], f[i], f[i + 1]]) { b.pos.push(...P[k]); b.col.push(colour.r, colour.g, colour.b); }
            b.rec.push(q);
          }
          f.forEach((k, i) => b.line.push(...P[k], ...P[f[(i + 1) % f.length]]));
        }
      }
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
      pickTargets.push(mesh);
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(b.line, 3));
      group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x0b1220, transparent: key === 'glass', opacity: key === 'glass' ? 0.5 : 1 })));
    }
  }
  const radius = () => {
    let r = 1;
    for (const q of cells().values()) r = Math.max(r, Math.hypot(...q) * unit(view.kind) + 1.2);
    return r;
  };
  const fit = () => fitView([0, 0, 0], radius() * WS * 1.1);

  // A cluster: a hub (octahedron, or jewel) and its eight neighbours.
  const clusterAt = (hub) => [hub, ...neighbours(view.kind, hub)];
  function start() {
    for (const q of view.clusters ? clusterAt(START) : [START]) cells().set(keyOf(q), q);
  }
  function add(list) {
    let added = 0;
    for (const q of list) if (!cells().has(keyOf(q))) { cells().set(keyOf(q), q); added++; }
    if (added) commit();
    return added > 0;
  }
  function handleTap(hit, mode) {
    const q = hit.object.userData.records?.[Math.floor(hit.faceIndex ?? -1)];
    if (!q || mode === 'paint') return false;
    if (mode === 'chisel') {
      if (cells().size <= 1) return false;
      cells().delete(keyOf(q)); commit();
      return true;
    }
    // The empty neighbour on the tapped side: the one whose direction from this cell's centre is nearest the tap's.
    const local = group.worldToLocal(hit.point.clone()).divideScalar(WS);
    const centre = q.map((c) => c * unit(view.kind));
    const dir = [local.x - centre[0], local.y - centre[1], local.z - centre[2]];
    const free = neighbours(view.kind, q).filter((n) => !cells().has(keyOf(n)));
    if (!free.length) { showHudPrompt(t('octb.prompt.full', lang()), 2000); return true; }
    const score = (n) => n.reduce((s, c, i) => s + (c - q[i]) * dir[i], 0) / Math.hypot(...n.map((c, i) => c - q[i]));
    const n = free.reduce((best, x) => (score(x) > score(best) ? x : best));
    if (!view.clusters) return add([n]);
    // A cluster: round the neighbour if it is a hub, otherwise round its hub on the far side (away from this cell).
    const hub = cellAt(view.kind, n).hub ? n : neighbours(view.kind, n).filter((h) => cellAt(view.kind, h).hub && keyOf(h) !== keyOf(q))
      .reduce((best, h) => (Math.hypot(...h.map((c, i) => c - q[i])) > Math.hypot(...best.map((c, i) => c - q[i])) ? h : best));
    return add(clusterAt(hub));
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldoctetbuild-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note octb-note"></div>
    <div class="w4d-row w4d-options"><button type="button" data-octb="reset"></button></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'octetBuild');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.octb-note').textContent = `${t(`octet.${view.kind}.network`, L)} · ${t(view.clusters ? 'octb.mode.clusters' : 'octb.mode.cells', L)} · ${t('octb.count', L, { n: cells().size })}`;
    panel.querySelector('[data-octb="reset"]').textContent = t('octb.reset', L);
  }
  panel.querySelector('[data-octb="reset"]').addEventListener('click', () => { cells().clear(); start(); commit(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    /** Which version, and single cells or clusters (each its own DICTO entry: 'caps', 'caps.clusters', ...). */
    setChain(id) {
      const [kind, how] = String(id ?? '').split('.');
      if (!OCTET_BUILD_KINDS.includes(kind)) return;
      view.kind = kind; view.clusters = how === 'clusters';
      if (!cells().size) start();
      save();
      if (active) { draw(); renderPanel(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!cells().size) start();
      draw(); renderPanel();
      if (on) { fit(); showHudPrompt(t(view.clusters ? 'octb.prompt.clusters' : 'octb.prompt.cells', lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return cells().size === 0; },
    clear() { cells().clear(); start(); commit(); if (active) fit(); },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews an entry in the DICTO menu: one cluster's cells. */
export function octetBuildPreviewPoints(id) {
  const kind = String(id ?? '').split('.')[0];
  if (!OCTET_BUILD_KINDS.includes(kind)) return [];
  const qs = String(id).endsWith('.clusters') ? [START, ...neighbours(kind, START)] : [START];
  return qs.flatMap((q) => cellAt(kind, q).pieces.flatMap((p) => p[1]));
}
