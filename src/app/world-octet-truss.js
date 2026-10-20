// The OG on the Octet Truss (DICTO 2026-10-19; paper #37, DICTO DOI 10.5281/zenodo.23457016): the DICTO Ogdoecontahedron in the
// octahedra of the octet truss, and the exact space-filling kits round it, in four families:
//   keys       the golden-key octet (keyed octahedron, dented tetrahedron left and right);
//   penrose    the Penrose-core octet (notched octahedron, middle piece, notched tetrahedron) and the keyless kit with three Penrose cores;
//   envelopes  golden envelopes on every octahedron: envelope + grown piece, envelope + adaptor halves, one piece, and the chamber
//              (outside the plan);
//   glue       one-piece glue: envelope + W, OG + W with OG imprints, OG + W on the Penrose star (the keyed W waits for its keys to be
//              recalculated exactly, DICTO 2026-10-19).
//   twins      Octet ↔ gyrated (DICTO 2026-10-20; paper #37a, DICTO DOI 10.5281/zenodo.23484012): the OG, the OG with its caps, the OCD
//              Stella or the DICTO Belted Triacontahedron in every octahedron, on the octet or the gyrated octet (A B A B, every layer a
//              twin boundary, shown as a faint plane); data: scripts/build-gyrated-octet-data.py (gyrated-octet-data.js).
// Each kit shows its set, its pieces round one OG, and its network grown from one lattice cell (data: scripts/build-octet-truss-data.mjs,
// loads on entry and is released on leaving). Words: i18n ot.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const FAMILIES = { keys: ['keys'], penrose: ['penrose', 'cores'], envelopes: ['grown', 'halves', 'one', 'chamber'], glue: ['envW', 'ogW', 'starW'],
  twins: ['gOG', 'gCaps', 'gStella', 'gDBT', 'gOTT'] };
const KITS = Object.values(FAMILIES).flat();
const familyOf = (kit) => Object.keys(FAMILIES).find((f) => FAMILIES[f].includes(kit));
const SHOWS = ['set', 'round', 'pair', 'network'];
const LATTICES = ['octet', 'gyrated'];
const PRESET = { kit: 'keys', show: 'round', apart: 30, size: 2, lattice: 'gyrated' };
const isTwins = (kit) => FAMILIES.twins.includes(kit);
// the views a kit offers: the twins family has a twin pair (gyrated only) in place of "round one OG"
const showsOf = (kit, lattice) => (isTwins(kit) ? ['set', ...(lattice === 'gyrated' ? ['pair'] : []), 'network'] : ['set', 'round', 'network']);
// what a tap names: the piece's role (the data's names come from the study pages)
const ROLE = { ko: 'keyedOct', no: 'notchedOct', mid: 'middle', k_ocd: 'og', k_cap: 'cap', k_core_c: 'coreC', k_core_f1: 'flank', k_core_f2: 'flank',
  k_rest3: 'rest', env: 'envelope', 'grown~': 'grown', grown: 'grown', half: 'half', rdglass: 'rd', W: 'W', Wo: 'Wog', Ws: 'Wstar' };
const TWIN_ROLE = { og: 'og', capL: 'capL', capR: 'capR', twinCap: 'twinCap', tet: 'tet', bipyramid: 'bipyramid', stella: 'stella', dbt: 'dbt',
  ogTwin: 'ogTwin', stellaTwin: 'stellaTwin', dbtTwin: 'dbtTwin' };
const roleOf = (kit, name) => (isTwins(kit) ? TWIN_ROLE[name] ?? 'piece' : ROLE[name] ?? (name.startsWith('tet') ? (kit === 'keys' ? 'dented' : 'notchedTet') : 'piece'));
const lang = () => getSettings().language;

export function createOctetTrussWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('octettruss');
  const group = new THREE.Group(); group.visible = false; group.scale.setScalar(WS); scene.add(group);
  const view = { ...PRESET };
  function read(d) {
    if (!d || typeof d !== 'object') return;
    if (KITS.includes(d.kit)) view.kit = d.kit;
    if (SHOWS.includes(d.show)) view.show = d.show;
    if (Number.isInteger(d.apart) && d.apart >= 0 && d.apart <= 100) view.apart = d.apart;
    if (Number.isInteger(d.size) && d.size >= 1 && d.size <= 4) view.size = d.size;
    if (LATTICES.includes(d.lattice)) view.lattice = d.lattice;
    if (!showsOf(view.kit, view.lattice).includes(view.show)) view.show = 'set';
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, ...view });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };

  let DATA = null, GDATA = null, loading = null, active = false, skeleton = false, opacity = 1, pickTargets = [];
  const load = () => (loading ??= Promise.all([import('./octet-truss-data.js'), import('./gyrated-octet-data.js')]).then(([m, g]) => { DATA = m.default; GDATA = g.default; }));
  const src = () => (isTwins(view.kit) ? GDATA : DATA);   // the data set the shown kit's pieces come from
  const fixed = () => !isTwins(view.kit) && !!DATA?.kits[view.kit].fixed;

  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry?.dispose(); child.material?.dispose(); }
    pickTargets = [];
  }
  // the items shown: [piece, 3×3 by rows, translation, centre]; the network repeats one cell's items by the fcc vectors R(a, b, c), a + b + c even
  function items() {
    if (isTwins(view.kit)) return twinItems();
    const K = DATA.kits[view.kit];
    if (K.fixed) return K.fixed.map((it) => ({ it, off: [0, 0, 0] }));
    if (view.show !== 'network') {
      const f = view.apart / 100 * 0.9;
      return K[view.show].map((it) => ({ it, off: [it[13] * f, it[14] * f, it[15] * f] }));
    }
    const n = view.size, R = DATA.R, out = [], lim = (n + 0.35) * R * Math.SQRT2;
    for (let a = -n - 1; a <= n + 1; a++) for (let b = -n - 1; b <= n + 1; b++) for (let c = -n - 1; c <= n + 1; c++) {
      if ((a + b + c) % 2) continue;
      for (const it of K.unit) {
        const off = [a * R, b * R, c * R];
        if (Math.hypot(it[13] + off[0], it[14] + off[1], it[15] + off[2]) <= lim) out.push({ it, off });
      }
    }
    return out;
  }
  // twins family: the set or the twin pair pulled apart; the network stacks layers: octet = layer 0 moved by R(1, 1, 0) per layer,
  // gyrated = layer 0 and its mirror image (layer 1) alternating, moved by (4R/3)(1, 1, 1) every two layers
  function twinItems() {
    const K = GDATA.kits[view.kit];
    if (view.show !== 'network') {
      const f = view.apart / 100 * 0.9, list = view.show === 'pair' ? K.pair : K.set;
      return list.map((it) => ({ it, off: [it[13] * f, it[14] * f, it[15] * f] }));
    }
    const n = view.size, R = GDATA.R, out = [], lim = (n + 0.35) * R * Math.SQRT2, gyr = view.lattice === 'gyrated';
    for (let k = -n - 1; k <= n + 1; k++) {
      const unit = gyr && k % 2 ? K.unit1 : K.unit0;
      const lift = gyr ? Array(3).fill((4 * R / 3) * Math.floor(k / 2)) : [k * R, k * R, 0];
      for (let i = -2 * n - 3; i <= 2 * n + 3; i++) for (let j = -2 * n - 3; j <= 2 * n + 3; j++) {
        const off = [lift[0] + i * R, lift[1] - i * R + j * R, lift[2] - j * R];
        for (const it of unit) if (Math.hypot(it[13] + off[0], it[14] + off[1], it[15] + off[2]) <= lim) out.push({ it, off });
      }
    }
    return out;
  }
  // the gyrated octet's twin layers x + y + z = (2k + 1)R as faint discs, in the twin pair and the network
  function twinPlanes() {
    if (!isTwins(view.kit) || view.lattice !== 'gyrated' || view.show === 'set') return;
    const R = GDATA.R, n = view.show === 'network' ? view.size : 0, rad = (n + 0.5) * R * Math.SQRT2, ks = view.show === 'network' ? [] : [0];
    if (view.show === 'network') for (let k = -n - 1; k <= n; k++) ks.push(k);
    const nrm = new THREE.Vector3(1, 1, 1).normalize(), f = view.show === 'pair' ? 1 + view.apart / 100 * 0.9 : 1;   // the pair's plane stays midway
    for (const k of ks) {
      const g = new THREE.CircleGeometry(rad, 48); g.lookAt(nrm);
      const d = (2 * k + 1) * R / Math.sqrt(3) * f; g.translate(nrm.x * d, nrm.y * d, nrm.z * d);
      const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x9ec9ff, transparent: true, opacity: 0.07, side: THREE.DoubleSide, depthWrite: false }));
      m.renderOrder = 3; m.userData.plane = true; group.add(m);
    }
  }
  const edgeCache = new Map();
  function edgesOf(p) {   // the piece's edges at a crease angle, once per piece
    const key = (isTwins(view.kit) ? 'g' : 'o') + p;
    if (!edgeCache.has(key)) {
      const P = src().pieces[p], g = new THREE.BufferGeometry(), a = [];
      for (const tri of P.t) for (const k of tri) a.push(...P.v[k]);
      g.setAttribute('position', new THREE.Float32BufferAttribute(a, 3));
      const e = new THREE.EdgesGeometry(g, 20); edgeCache.set(key, e.attributes.position.array); g.dispose(); e.dispose();
    }
    return edgeCache.get(key);
  }
  const place = (it, off, v) => [it[1] * v[0] + it[2] * v[1] + it[3] * v[2] + it[10] + off[0], it[4] * v[0] + it[5] * v[1] + it[6] * v[2] + it[11] + off[1], it[7] * v[0] + it[8] * v[1] + it[9] * v[2] + it[12] + off[2]];
  function draw() {
    clearGroup();
    if (!active || !DATA || !GDATA) return;
    const byPiece = new Map();
    for (const e of items()) (byPiece.get(e.it[0]) ?? byPiece.set(e.it[0], []).get(e.it[0])).push(e);
    for (const [p, list] of byPiece) {
      const P = src().pieces[p], pos = [], edges = [], E = edgesOf(p);
      for (const { it, off } of list) {
        const V = P.v.map((v) => place(it, off, v));
        for (const tri of P.t) for (const k of tri) pos.push(...V[k]);
        for (let i = 0; i < E.length; i += 3) edges.push(...place(it, off, [E[i], E[i + 1], E[i + 2]]));
      }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
      const glass = P.o < 1, see = glass || skeleton || opacity < 1, op = skeleton ? 0 : glass ? Math.min(P.o, 0.35) : opacity;
      const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: P.c, roughness: 0.5, metalness: 0.05, flatShading: true, side: THREE.DoubleSide,
        transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }));
      mesh.renderOrder = see ? 2 : 0; mesh.userData = { kind: 'piece', name: P.name };
      const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
      group.add(mesh, new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x2a2218, transparent: true, opacity: skeleton ? 0.9 : glass ? 0.3 : 0.5 })));
      pickTargets.push(mesh);
    }
    twinPlanes();
  }
  const fit = () => {
    if (!DATA) return;
    const box = new THREE.Box3();
    for (const child of group.children) if (child.isMesh && !child.userData.plane) { child.geometry.computeBoundingBox(); box.union(child.geometry.boundingBox); }
    if (box.isEmpty()) return;
    const s = box.getBoundingSphere(new THREE.Sphere());
    // the twins family frames each view exactly, side-on to the twin axis (1, 1, 1) where the twins or the layers are shown
    if (isTwins(view.kit)) fitView(s.center.toArray().map((x) => x * WS), s.radius * WS * 1.6, view.show === 'set' ? null : [1, -1, view.show === 'pair' ? 0.35 : 0.6], true);
    else fitView(s.center.toArray().map((x) => x * WS), s.radius * WS * 1.02);
  };

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'piece' || mode === 'paint') return false;
    showHudPrompt(t(`ot.piece.${roleOf(view.kit, ud.name)}`, lang()), 4500);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldoctettruss-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note ot-note"></div>
    <div class="w4d-row w4d-options ot-families">${Object.keys(FAMILIES).map((f) => `<button type="button" data-ot-family="${f}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options ot-kits">${KITS.map((k) => `<button type="button" data-ot-kit="${k}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options ot-lattices">${LATTICES.map((l) => `<button type="button" data-ot-lattice="${l}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options ot-shows">${SHOWS.map((s) => `<button type="button" data-ot-show="${s}"></button>`).join('')}<button type="button" data-ot="reset"></button></div>
    <div class="w4d-row ot-apart-row"><label class="hull-pick"><span class="ot-apart-label"></span> <input type="range" class="st-slider ot-apart" min="0" max="100" step="5"></label></div>
    <div class="w4d-row ot-size-row"><label class="hull-pick"><span class="ot-size-label"></span> <input type="range" class="st-slider ot-size" min="1" max="4" step="1"></label></div>
    <style>#worldoctettruss-panel .ot-note{max-width:62ch;margin:0 auto}</style>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'octettruss');
  const apart = panel.querySelector('.ot-apart'), size = panel.querySelector('.ot-size');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), fam = familyOf(view.kit);
    if (!DATA || !GDATA) { panel.querySelector('.ot-note').textContent = t('ot.loading', L); return; }
    panel.querySelector('.ot-note').textContent = t(`ot.note.${view.kit}`, L);
    panel.querySelectorAll('[data-ot-family]').forEach((b) => { b.textContent = t(`ot.family.${b.dataset.otFamily}`, L); b.classList.toggle('active', b.dataset.otFamily === fam); });
    panel.querySelectorAll('[data-ot-kit]').forEach((b) => {
      const mine = FAMILIES[fam].includes(b.dataset.otKit);
      b.hidden = !mine || FAMILIES[fam].length < 2; // a family of one kit needs no kit buttons
      if (mine) { b.textContent = t(`ot.kit.${b.dataset.otKit}`, L); b.classList.toggle('active', b.dataset.otKit === view.kit); }
    });
    panel.querySelector('.ot-lattices').hidden = !isTwins(view.kit);   // the lattice switch belongs to the twins family only
    panel.querySelectorAll('[data-ot-lattice]').forEach((b) => { b.textContent = t(`ot.lattice.${b.dataset.otLattice}`, L); b.classList.toggle('active', b.dataset.otLattice === view.lattice); });
    panel.querySelector('.ot-shows').hidden = fixed();
    const offered = showsOf(view.kit, view.lattice);
    panel.querySelectorAll('[data-ot-show]').forEach((b) => { b.hidden = !offered.includes(b.dataset.otShow); b.textContent = t(`ot.show.${b.dataset.otShow}`, L); b.classList.toggle('active', b.dataset.otShow === view.show); });
    const reset = panel.querySelector('[data-ot="reset"]');
    reset.hidden = Object.keys(PRESET).every((k) => view[k] === PRESET[k]); reset.textContent = t('ot.reset', L);
    panel.querySelector('.ot-apart-row').hidden = fixed() || view.show === 'network';
    panel.querySelector('.ot-size-row').hidden = fixed() || view.show !== 'network';
    apart.value = String(view.apart); size.value = String(view.size);
    panel.querySelector('.ot-apart-label').textContent = t('ot.apart', L);
    panel.querySelector('.ot-size-label').textContent = t('ot.size', L, { n: view.size });
  }
  const commit = (refit = false) => { save(); draw(); renderPanel(); onChange(); if (refit) fit(); };
  const keepShow = () => { if (!showsOf(view.kit, view.lattice).includes(view.show)) view.show = isTwins(view.kit) && view.lattice === 'gyrated' ? 'pair' : 'set'; };
  panel.querySelectorAll('[data-ot-family]').forEach((b) => b.addEventListener('click', () => {
    if (familyOf(view.kit) === b.dataset.otFamily) return;
    view.kit = FAMILIES[b.dataset.otFamily][0]; keepShow(); commit(true);
  }));
  panel.querySelectorAll('[data-ot-kit]').forEach((b) => b.addEventListener('click', () => { if (view.kit !== b.dataset.otKit) { view.kit = b.dataset.otKit; keepShow(); commit(true); } }));
  panel.querySelectorAll('[data-ot-lattice]').forEach((b) => b.addEventListener('click', () => { if (view.lattice !== b.dataset.otLattice) { view.lattice = b.dataset.otLattice; keepShow(); commit(true); } }));
  panel.querySelectorAll('[data-ot-show]').forEach((b) => b.addEventListener('click', () => { if (view.show !== b.dataset.otShow) { view.show = b.dataset.otShow; commit(true); } }));
  panel.querySelector('[data-ot="reset"]').addEventListener('click', () => { Object.assign(view, PRESET); commit(true); });
  apart.addEventListener('input', () => { view.apart = Number(apart.value); save(); draw(); });
  apart.addEventListener('change', () => onChange());
  size.addEventListener('input', () => { view.size = Number(size.value); save(); draw(); renderPanel(); });
  size.addEventListener('change', () => { onChange(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { clearGroup(); DATA = null; GDATA = null; loading = null; edgeCache.clear(); renderPanel(); return; } // leaving lets the pieces and the data go
      renderPanel();
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('ot.prompt.start', lang()), 5500); });
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { Object.assign(view, PRESET); commit(active); },
    resetView() {},
    open(sub) {
      if (sub === 'gyrated') { view.kit = 'gCaps'; view.lattice = 'gyrated'; view.show = 'network'; }   // ?open=octetTruss:gyrated
      else if (KITS.includes(sub)) { view.kit = sub; keepShow(); } else return;
      save(); if (active) { draw(); renderPanel(); fit(); }
    },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the octahedron |x| + |y| + |z| = 2φ/3 and the eight tetrahedra on it. */
export function octetTrussPreviewPoints() {
  const R = (1 + Math.sqrt(5)) / 3, pts = [];
  for (const s of [-1, 1]) pts.push([s * R, 0, 0], [0, s * R, 0], [0, 0, s * R]);
  for (const a of [-1, 1]) for (const b of [-1, 1]) for (const c of [-1, 1]) pts.push([a * R * 2 / 3, b * R * 2 / 3, c * R * 2 / 3]);
  return pts;
}
