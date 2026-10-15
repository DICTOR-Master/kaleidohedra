// Golden Bodhi Pyrochlore Networks (DICTO 2026-10-15): the DICTO Ogdoecontahedron (20 regular hexagons, 60 kites) and the networks it
// makes by joining copies face to face on hexagons, next to the Pyrochlore and the Golden Breathing Pyrochlore. Four views:
//   network  one diamond network (four tetrahedral hexagons per copy); its joints, the hexagon centres, lie on a pyrochlore lattice;
//   double   the second network in the gaps: together one body-centred cubic packing (77.43% of space), with the 72 gap pieces per
//            copy that fill the rest exactly (48 + 12 on kites, 12 on hexagons);
//   voice    each of the five inscribed cubes gives its own body-centred cubic packing (a "voice");
//   chorus   the five voices in five 72° wedges round a five-fold axis, exact to radius 10 (paper #30, DICTO DOI 10.5281/zenodo.23396361):
//            removed copies as ghosts, and the Fibonacci spine on the axis.
// A grow slider sets the size; Build lets a tap add the copy joined on the tapped hexagon (long-press removes), with helper outlines
// showing every free place a copy can join. Sites are integer points (i, j, k) of one parity in a cube's frame M; a copy sits at M·(i,j,k).
// Geometry: bodhi-pyro-data.js (scripts/build-bodhi-pyro-data.py, from studies/2026-10-16-ocd-pyrochlore). Words: i18n gbp.*.
import * as THREE from 'three';
import DATA from './bodhi-pyro-data.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const MODES = ['network', 'double', 'voice', 'chorus'];
const VOICE_COLOUR = [0xf08a3c, 0x4dd0e1, 0xb98ad8, 0x5fd38a, 0xe85d88];
const NET_COLOUR = [0xffc857, 0x6fa8ff]; // first network warm, second cool
const CENTRE_COLOUR = 0xffc857;
const GAP_COLOUR = { kiteWedge: 0x4dd0e1, kite: 0xf08fc0, hex: 0xb98ad8 };
const SIZE = { network: [1, 5, 3], double: [1, 4, 2], voice: [1, 4, 2], chorus: [2, 10, 5] }; // min, max, start (bond steps; chorus: radius)
const EDGE_LIMIT = 900;   // copies drawn with outlines; above that, faces only
const OUTLINE_LIMIT = 240; // helper outlines shown at once
const lang = () => getSettings().language;
const keyOf = (q) => q.join(',');
const mod = (n, m) => ((n % m) + m) % m;
const CUBES = DATA.cubes.map((c) => ({ M: new THREE.Matrix3().set(c.M[0][0], c.M[1][0], c.M[2][0], c.M[0][1], c.M[1][1], c.M[2][1], c.M[0][2], c.M[1][2], c.M[2][2]), faceBond: c.faceBond }));
const BOND = Math.hypot(...new THREE.Vector3(1, 1, 1).applyMatrix3(CUBES[0].M).toArray());
const pos = (cube, q) => new THREE.Vector3(...q).applyMatrix3(CUBES[cube].M);
// Diamond networks in a cube's frame: the class of a site is (i + j + k) mod 4; network 0 holds classes 0 and 3, network 1 classes 1 and 2.
// From a class-0 site the bonds are the tetrahedral set s1 s2 s3 = +1, from a class-3 site their opposites (and likewise for network 1).
const netOf = (q) => ([0, 3].includes(mod(q[0] + q[1] + q[2], 4)) ? 0 : 1);
const tetraOut = (q) => { const c = mod(q[0] + q[1] + q[2], 4); return c === 0 || c === 2 ? 1 : -1; }; // sign of s1 s2 s3 for bonds leaving q
const SIGNS = [...Array(8)].map((_, i) => [i & 1 ? -1 : 1, i & 2 ? -1 : 1, i & 4 ? -1 : 1]);
const bondsFrom = (q, mode) => (mode === 'network' ? SIGNS.filter((s) => s[0] * s[1] * s[2] === tetraOut(q)) : SIGNS);
const allowed = (q, mode) => (mode !== 'network' || netOf(q) === 0) && new Set(q.map((c) => mod(c, 2))).size === 1;

// ---- geometry ----
function solidGeometry(V, F) {
  const p = [], faceOf = [];
  F.forEach((f, fi) => { for (let i = 1; i + 1 < f.length; i++) { for (const k of [f[0], f[i], f[i + 1]]) p.push(...V[k].map((x) => x * WS)); faceOf.push(fi); } });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); g.computeVertexNormals();
  g.userData.faceOf = faceOf; return g;
}
function edgeSegments(V, F) {
  const seen = new Set(), seg = [];
  for (const f of F) f.forEach((a, i) => { const b = f[(i + 1) % f.length], k = a < b ? `${a},${b}` : `${b},${a}`; if (!seen.has(k)) { seen.add(k); seg.push(V[a], V[b]); } });
  return seg.map((v) => v.map((x) => x * WS));
}
const OCD = solidGeometry(DATA.ocd.v, DATA.ocd.f);
const OCD_EDGES = edgeSegments(DATA.ocd.v, DATA.ocd.f);
const GAPS = (() => {
  const p = [], c = [], col = new THREE.Color();
  for (const g of DATA.gaps) { col.setHex(GAP_COLOUR[g.kind]); for (const tri of g.t) for (const k of tri) { p.push(...g.v[k].map((x) => x * WS)); c.push(col.r, col.g, col.b); } }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(c, 3)); geo.computeVertexNormals();
  return geo;
})();

export function createBodhiPyroWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('bodhipyro');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { mode: 'network', voice: 0, size: Object.fromEntries(MODES.map((m) => [m, SIZE[m][2]])), joints: true, gaps: false, ghosts: true, spine: true, build: false };
  const builds = { network: null, double: null, voice: null }; // null: the preset for the size; else a Map key -> q
  const cubeOf = () => (view.mode === 'voice' ? view.voice : 0);
  function preset(mode, n) {
    const out = new Map(), r = n * BOND + 1e-6, lim = n + 1, cube = cubeOf();
    for (let i = -2 * lim; i <= 2 * lim; i++) for (let j = -2 * lim; j <= 2 * lim; j++) for (let k = -2 * lim; k <= 2 * lim; k++) {
      const q = [i, j, k];
      if (!allowed(q, mode) || pos(cube, q).length() > r) continue;
      out.set(keyOf(q), q);
    }
    return out;
  }
  const sites = () => builds[view.mode] ?? preset(view.mode, view.size[view.mode]);
  function read(d) {
    if (!d || typeof d !== 'object') return;
    if (MODES.includes(d.mode)) view.mode = d.mode;
    if (Number.isInteger(d.voice) && d.voice >= 0 && d.voice < 5) view.voice = d.voice;
    for (const m of MODES) { const n = Number(d.size?.[m]); if (Number.isFinite(n)) view.size[m] = Math.min(SIZE[m][1], Math.max(SIZE[m][0], Math.round(n))); }
    for (const k of ['joints', 'gaps', 'ghosts', 'spine', 'build']) if (typeof d[k] === 'boolean') view[k] = d[k];
    for (const m of ['network', 'double', 'voice']) {
      const b = d.builds?.[m];
      builds[m] = Array.isArray(b) ? new Map(b.filter((q) => Array.isArray(q) && q.length === 3 && q.every(Number.isInteger) && allowed(q, m)).map((q) => [keyOf(q), q])) : null;
      if (builds[m] && !builds[m].size) builds[m] = null;
    }
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: start fresh */ }
  const snapshot = () => ({ version: 1, mode: view.mode, voice: view.voice, size: { ...view.size }, joints: view.joints, gaps: view.gaps, ghosts: view.ghosts,
    spine: view.spine, build: view.build, builds: Object.fromEntries(Object.entries(builds).map(([m, b]) => [m, b ? [...b.values()] : null])) });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const commit = () => { save(); draw(); renderPanel(); onChange(); };

  let active = false, skeleton = false, opacity = 1, pickTargets = [];
  const solid = new THREE.MeshStandardMaterial({ roughness: 0.5, metalness: 0.05, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const ghost = new THREE.MeshStandardMaterial({ color: 0xd8cdb8, roughness: 0.6, flatShading: true, transparent: true, opacity: 0.12, depthWrite: false });
  const helper = new THREE.MeshBasicMaterial({ color: 0xffe9a8, transparent: true, opacity: 0.16, depthWrite: false });
  const gapMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, flatShading: true, side: THREE.DoubleSide });
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      if (child.isInstancedMesh) child.dispose();
      if (child.geometry && child.geometry !== OCD && child.geometry !== GAPS) child.geometry.dispose();
      if (child.isLineSegments || child.userData.ownMaterial) child.material.dispose();
    }
    pickTargets = [];
  }
  function instanced(geo, mat, list, colourOf, kind) {
    const m = new THREE.InstancedMesh(geo, mat, Math.max(1, list.length)); m.count = list.length;
    const mat4 = new THREE.Matrix4(), col = new THREE.Color();
    list.forEach((e, i) => { mat4.makeTranslation(e.p.x * WS, e.p.y * WS, e.p.z * WS); m.setMatrixAt(i, mat4); if (colourOf) m.setColorAt(i, col.setHex(colourOf(e))); });
    m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true;
    m.userData = { kind, list }; group.add(m); return m;
  }
  function outlines(list) {
    if (list.length > EDGE_LIMIT) return;
    const p = [];
    for (const e of list) for (const v of OCD_EDGES) p.push(v[0] + e.p.x * WS, v[1] + e.p.y * WS, v[2] + e.p.z * WS);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
    group.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x2a2218, transparent: true, opacity: skeleton ? 0.9 : 0.55 })));
  }
  // Free places a copy can join (helper outlines): neighbours of built copies along the view's bonds, not yet built.
  function freePlaces(map) {
    const out = new Map();
    for (const q of map.values()) for (const s of bondsFrom(q, view.mode)) {
      const n = q.map((c, i) => c + s[i]), k = keyOf(n);
      if (!map.has(k) && allowed(n, view.mode)) out.set(k, n);
    }
    return [...out.values()].sort((a, b) => pos(cubeOf(), a).length() - pos(cubeOf(), b).length()).slice(0, OUTLINE_LIMIT);
  }
  function draw() {
    clearGroup();
    if (!active) return;
    solid.transparent = opacity < 1 || skeleton; solid.opacity = skeleton ? 0 : opacity; solid.depthWrite = opacity >= 1 && !skeleton; solid.needsUpdate = true;
    if (view.mode === 'chorus') return drawChorus();
    const cube = cubeOf(), map = sites();
    const list = [...map.values()].map((q) => ({ q, p: pos(cube, q) }));
    const colourOf = (e) => (e.q.every((c) => c === 0) ? CENTRE_COLOUR
      : view.mode === 'voice' ? VOICE_COLOUR[view.voice] : view.mode === 'double' ? NET_COLOUR[netOf(e.q)] : NET_COLOUR[0]);
    pickTargets.push(instanced(OCD, solid, list, colourOf, 'copies'));
    outlines(list);
    if (view.mode === 'network' && view.joints) {
      // the joints: hexagon centres where two copies meet, at the bond midpoints (a pyrochlore lattice)
      const pts = [];
      for (const e of list) for (const s of bondsFrom(e.q, 'network')) {
        const n = e.q.map((c, i) => c + s[i]);
        if (map.has(keyOf(n)) && keyOf(e.q) < keyOf(n)) pts.push({ p: pos(cube, e.q).add(pos(cube, n)).multiplyScalar(0.5) });
      }
      // drawn over the copies (the joints lie on the touching hexagons), with each copy's four joints joined as the pyrochlore's
      // corner-sharing tetrahedra
      const dot = new THREE.SphereGeometry(0.07 * WS, 14, 10); const m = new THREE.MeshBasicMaterial({ color: 0xe53935, depthTest: false, transparent: true });
      const inst = instanced(dot, m, pts, null, 'joints'); inst.userData.ownMaterial = true; inst.renderOrder = 10;
      const seg = [];
      for (const e of list) {
        const J = bondsFrom(e.q, 'network').map((s) => e.q.map((c, i) => c + s[i])).filter((n) => map.has(keyOf(n)))
          .map((n) => pos(cube, e.q).add(pos(cube, n)).multiplyScalar(0.5 * WS));
        for (let i = 0; i < J.length; i++) for (let j = i + 1; j < J.length; j++) seg.push(...J[i].toArray(), ...J[j].toArray());
      }
      if (seg.length) {
        const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(seg, 3));
        const tl = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xff8a80, depthTest: false, transparent: true, opacity: 0.85 }));
        tl.renderOrder = 9; group.add(tl);
      }
    }
    if (view.mode === 'double' && view.gaps) instanced(GAPS, gapMat, list, null, 'gaps');
    if (view.build) {
      const free = freePlaces(map).map((q) => ({ q, p: pos(cube, q) }));
      if (free.length) pickTargets.push(instanced(OCD, helper, free, null, 'outline'));
      const p = [];
      for (const e of free) for (const v of OCD_EDGES) p.push(v[0] + e.p.x * WS, v[1] + e.p.y * WS, v[2] + e.p.z * WS);
      if (p.length) { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); group.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xffe08a, transparent: true, opacity: 0.45 }))); }
    }
  }
  function drawChorus() {
    const R = view.size.chorus, A = new THREE.Vector3(...DATA.chorus.axis);
    const kept = [], gone = [];
    for (const [x, y, z, w, r] of DATA.chorus.sites) {
      const p = new THREE.Vector3(x, y, z);
      if (p.length() > R + 1e-6) continue;
      (r ? gone : kept).push({ p, w });
    }
    pickTargets.push(instanced(OCD, solid, kept, (e) => (e.w < 0 ? CENTRE_COLOUR : VOICE_COLOUR[e.w]), 'chorus'));
    outlines(kept);
    if (view.ghosts && gone.length) instanced(OCD, ghost, gone, null, 'removed');
    if (view.spine) {
      const L = R + 1.2, g = new THREE.BufferGeometry().setFromPoints([A.clone().multiplyScalar(-L * WS), A.clone().multiplyScalar(L * WS)]);
      // the spine runs inside the copies: drawn over them
      const ax = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xe53935, depthTest: false, transparent: true })); ax.renderOrder = 9; group.add(ax);
      const dots = DATA.chorus.chain.filter((h) => Math.abs(h) <= R).map((h) => ({ p: A.clone().multiplyScalar(h), h }));
      const m = new THREE.MeshBasicMaterial({ color: 0xe53935, depthTest: false, transparent: true });
      const inst = instanced(new THREE.SphereGeometry(0.13 * WS, 16, 12), m, dots, null, 'spine'); inst.userData.ownMaterial = true; inst.renderOrder = 10;
    }
  }
  const radius = () => (view.mode === 'chorus' ? view.size.chorus + 1 : Math.max(1.5, ...[...sites().values()].map((q) => pos(cubeOf(), q).length() + 0.8)));
  const fit = () => fitView([0, 0, 0], radius() * WS * 1.05);

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || view.mode === 'chorus' || mode === 'paint') return false;
    if (!view.build) { showHudPrompt(t('gbp.prompt.buildOff', lang()), 2200); return true; }
    if (!builds[view.mode]) builds[view.mode] = new Map(sites());
    const map = builds[view.mode], e = ud.list?.[hit.instanceId];
    if (!e) return false;
    if (ud.kind === 'outline') { map.set(keyOf(e.q), e.q); commit(); return true; }
    if (mode === 'chisel') {
      if (map.size <= 1 || e.q.every((c) => c === 0)) return false;
      map.delete(keyOf(e.q)); commit(); return true;
    }
    const fi = OCD.userData.faceOf[Math.floor(hit.faceIndex ?? -1)];
    const s = CUBES[cubeOf()].faceBond[fi];
    if (!s || !bondsFrom(e.q, view.mode).some((b) => b.every((x, i) => x === s[i]))) { showHudPrompt(t('gbp.prompt.notJoint', lang()), 2200); return true; }
    const n = e.q.map((c, i) => c + s[i]);
    if (map.has(keyOf(n))) { showHudPrompt(t('gbp.prompt.taken', lang()), 1800); return true; }
    map.set(keyOf(n), n); commit(); return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldbodhipyro-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note gbp-note"></div>
    <div class="w4d-row w4d-options gbp-modes">${MODES.map((m) => `<button type="button" data-gbp-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options gbp-voices">${[0, 1, 2, 3, 4].map((v) => `<button type="button" data-gbp-voice="${v}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options gbp-toggles"><button type="button" data-gbp="joints"></button><button type="button" data-gbp="gaps"></button><button type="button" data-gbp="ghosts"></button><button type="button" data-gbp="spine"></button><button type="button" data-gbp="build"></button><button type="button" data-gbp="reset"></button></div>
    <div class="w4d-row gbp-size-row"><label class="hull-pick"><span class="gbp-size-label"></span> <input type="range" class="st-slider" step="1"></label></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'bodhipyro');
  const slider = panel.querySelector('.gbp-size-row input');
  const show = (sel, on) => { panel.querySelector(sel).hidden = !on; };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), m = view.mode, n = view.mode === 'chorus' ? null : sites().size;
    const chorusCount = () => { let k = 0, g = 0; for (const s of DATA.chorus.sites) if (Math.hypot(s[0], s[1], s[2]) <= view.size.chorus + 1e-6) (s[4] ? g++ : k++); return { k, g }; };
    const c = m === 'chorus' ? chorusCount() : null;
    panel.querySelector('.gbp-note').textContent = m === 'chorus' ? t('gbp.note.chorus', L, { k: c.k, g: c.g }) : t(`gbp.note.${m}`, L, { n, v: view.voice + 1 });
    panel.querySelectorAll('[data-gbp-mode]').forEach((b) => { b.textContent = t(`gbp.mode.${b.dataset.gbpMode}`, L); b.classList.toggle('active', b.dataset.gbpMode === m); });
    show('.gbp-voices', m === 'voice');
    panel.querySelectorAll('[data-gbp-voice]').forEach((b) => { b.textContent = t('gbp.voice', L, { v: Number(b.dataset.gbpVoice) + 1 }); b.classList.toggle('active', Number(b.dataset.gbpVoice) === view.voice); });
    const tog = (k, on) => { const b = panel.querySelector(`[data-gbp="${k}"]`); b.hidden = !on; if (on && k !== 'reset') b.textContent = t(`gbp.${k}.${view[k] ? 'on' : 'off'}`, L); };
    tog('joints', m === 'network'); tog('gaps', m === 'double'); tog('ghosts', m === 'chorus'); tog('spine', m === 'chorus'); tog('build', m !== 'chorus');
    const reset = panel.querySelector('[data-gbp="reset"]'); reset.hidden = m === 'chorus' || !builds[m]; reset.textContent = t('gbp.reset', L);
    const [lo, hi] = SIZE[m]; slider.min = String(lo); slider.max = String(hi); slider.value = String(view.size[m]);
    panel.querySelector('.gbp-size-label').textContent = t(m === 'chorus' ? 'gbp.size.chorus' : 'gbp.size.grow', L, { n: view.size[m] });
  }
  panel.querySelectorAll('[data-gbp-mode]').forEach((b) => b.addEventListener('click', () => {
    view.mode = b.dataset.gbpMode; commit(); fit();
    if (view.mode === 'chorus') showHudPrompt(t('gbp.prompt.chorus', lang()), 5000);
  }));
  panel.querySelectorAll('[data-gbp-voice]').forEach((b) => b.addEventListener('click', () => { view.voice = Number(b.dataset.gbpVoice); builds.voice = null; commit(); fit(); }));
  for (const k of ['joints', 'gaps', 'ghosts', 'spine', 'build']) panel.querySelector(`[data-gbp="${k}"]`).addEventListener('click', () => {
    view[k] = !view[k]; commit();
    if (k === 'build' && view.build) showHudPrompt(t('gbp.prompt.build', lang()), 4500);
  });
  panel.querySelector('[data-gbp="reset"]').addEventListener('click', () => { builds[view.mode] = null; commit(); fit(); });
  slider.addEventListener('input', () => {
    view.size[view.mode] = Number(slider.value);
    if (view.mode !== 'chorus') builds[view.mode] = null; // the slider grows the preset; a tapped build starts again from it
    save(); draw(); renderPanel();
  });
  slider.addEventListener('change', () => { onChange(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      draw(); renderPanel();
      if (on) { fit(); showHudPrompt(t('gbp.prompt.start', lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { for (const m of Object.keys(builds)) builds[m] = null; commit(); if (active) fit(); },
    resetView() {},
    open(sub) { if (MODES.includes(sub)) { view.mode = sub; commit(); if (active) fit(); } },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: a copy and its eight neighbours of the first voice. */
export function bodhiPyroPreviewPoints() {
  const centres = [[0, 0, 0], ...SIGNS].map((q) => pos(0, q));
  return centres.flatMap((c) => DATA.ocd.v.map((v) => [v[0] + c.x, v[1] + c.y, v[2] + c.z]));
}
