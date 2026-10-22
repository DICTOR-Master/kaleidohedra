// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47, DICTO DOI 10.5281/zenodo.23551326): the "View in app" of the paper.
// Every mix of the five Platonic solids fills space. The world opens empty; five big letters D I C T O each add their solid's layer
// (slab), which drops into place in the stack order bottom to top D, C, T/O, I (T and O share the octet slab: adding the other only
// changes which of its solids are whole and which are cut into helpers); a lit letter takes its layer out again (DICTO 2026-10-22,
// after trying the first preview). Solids in their element colours with gold edges, helper pieces (connectors) as coloured glass;
// "Helpers" hides the connectors; a big slider spreads the slabs apart; a small list names the helpers the mix uses.
// Build it yourself: a new layer shows its pieces as ghosts outlined in their own colours; tapping a ghost places that piece; Fill the rest places the
// others. Every change goes through the app's undo (↶). Geometry: platonic-mix-geometry.js (ported from the paper's checked study).
// Words: i18n pm.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { WORLDS, PHI, SLAB_ORDER, slabsOf, slabPieces, pieceKey, pieceCentre, helpersOf, isSolid } from './platonic-mix-geometry.js';

// the elements' colours (DICTO): dodecahedron violet, icosahedron blue, cube green, tetrahedron red, octahedron yellow; gold edges
export const SOLID_COLOURS = { D: 0x8a5cc4, I: 0x3a70cd, C: 0x488e48, T: 0xcd3e28, O: 0xe8c852 };
// helpers are coloured glass (DICTO: the structure shows through); each is tinted after the solid it stands in for or joins:
// P half-octahedra yellow, Q/Q′ quarter-tetrahedra red, A Admiral Caps blue, S Dogstar and X/Y violet
const HELPER_COLOURS = { P: 0xf0d870, Q: 0xe8705a, 'Q′': 0xf09a6a, A: 0x6a9cf0, S: 0xb08ae6, X: 0x9a78d8, Y: 0xc4a8ee };
const GLASS = 0.38;
const GOLD = 0xdeb250;
const KEY = { 'Q′': 'Qp' };                              // i18n key of a kind
const GAP = 1.2;                                         // the slabs' extra spacing at Spread 1, in edge lengths
const K = (2 * WS) / ((3 * PHI + 1 + Math.SQRT2 + 1.512 + 3 * GAP) / 2); // one scale for every mix: the whole block, spread, fits
const DROP = 6;                                          // a new layer falls from this far above its place (edge lengths)
const ANIM_MS = 550;
const PRESET = { mix: '', helpers: true, spread: 0, build: false, placed: {} };
const lang = () => getSettings().language;
const cleanMix = (m) => WORLDS.filter((w) => String(m).toUpperCase().includes(w)).join('');

/** Pieces as one mesh (polygons fanned; tri → piece index) and their outlines (edges between non-coplanar faces). */
function piecesGeometry(pieces) {
  const tri = [], lines = [], pieceOfTri = [];
  const kv = (v) => v.map((x) => x.toFixed(5)).join(',');
  pieces.forEach((p, pi) => {
    const edges = new Map();
    for (const F of p.faces) {
      for (let i = 1; i + 1 < F.length; i++) { tri.push(...F[0], ...F[i], ...F[i + 1]); pieceOfTri.push(pi); }
      let n = [0, 0, 0];                                 // Newell's normal
      F.forEach((a, i) => { const b = F[(i + 1) % F.length]; n = [n[0] + (a[1] - b[1]) * (a[2] + b[2]), n[1] + (a[2] - b[2]) * (a[0] + b[0]), n[2] + (a[0] - b[0]) * (a[1] + b[1])]; });
      const l = Math.hypot(...n) || 1; n = n.map((x) => x / l);
      F.forEach((a, i) => { const b = F[(i + 1) % F.length], k = [kv(a), kv(b)].sort().join('|'); if (!edges.has(k)) edges.set(k, { a, b, n: [] }); edges.get(k).n.push(n); });
    }
    for (const { a, b, n } of edges.values()) {
      const flat = n.length === 2 && Math.abs(Math.abs(n[0][0] * n[1][0] + n[0][1] * n[1][1] + n[0][2] * n[1][2]) - 1) < 1e-6;
      if (!flat) lines.push(...a, ...b);
    }
  });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(turn(tri), 3)); g.computeVertexNormals();
  const e = new THREE.BufferGeometry(); e.setAttribute('position', new THREE.Float32BufferAttribute(turn(lines), 3));
  return { g, e, pieceOfTri };
}
// the study's z is up; the scene's y is up: (x, y, z) → (x, z, −y)
function turn(A) { for (let i = 0; i < A.length; i += 3) { const y = A[i + 1]; A[i + 1] = A[i + 2]; A[i + 2] = -y; } return A; }
const turned = ([x, y, z]) => [x, z, -y];

export function createPlatonicMixWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('platonicMix');
  const group = new THREE.Group(); group.visible = false; group.scale.setScalar(K); scene.add(group);
  const view = { ...PRESET, placed: {} };
  function read(d) {
    if (!d) return;
    if (typeof d.view?.mix === 'string') view.mix = cleanMix(d.view.mix);
    if (typeof d.view?.helpers === 'boolean') view.helpers = d.view.helpers;
    if (typeof d.view?.build === 'boolean') view.build = d.view.build;
    if (Number.isFinite(d.view?.spread)) view.spread = Math.max(0, Math.min(100, d.view.spread));
    view.placed = {};
    if (d.view?.placed && typeof d.view.placed === 'object') {
      for (const w of SLAB_ORDER) if (Array.isArray(d.view.placed[w])) view.placed[w] = d.view.placed[w].filter((k) => typeof k === 'string');
    }
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 2, view: { ...view, placed: Object.fromEntries(Object.entries(view.placed).map(([w, a]) => [w, [...a]])) } });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const commit = () => { save(); onChange(); };

  let active = false, skeleton = false, opacity = 1;
  // slabs: world → { world, pieces, keys, top, group, y, drawn: [{ kind, mesh, line }], ghost: { mesh, line, pieces } | null }
  const slabs = new Map();
  const mats = {}, lineMats = {};
  const ghostLineMats = {};                              // a ghost is outlined in its own piece's colour
  const ghostLineMat = (kind) => (ghostLineMats[kind] ??= new THREE.LineBasicMaterial({ color: colourOf(kind), transparent: true, opacity: 0.7, depthWrite: false }));
  const ghostPickMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false, colorWrite: false, side: THREE.DoubleSide });
  const colourOf = (kind) => (isSolid(kind) ? SOLID_COLOURS[kind] : HELPER_COLOURS[kind]);
  function matFor(kind) {
    if (!mats[kind]) {
      mats[kind] = new THREE.MeshStandardMaterial({ color: colourOf(kind), flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: isSolid(kind) ? 0.5 : 0.85 });
      lineMats[kind] = new THREE.LineBasicMaterial({ color: GOLD });
    }
    const o = isSolid(kind) ? opacity : Math.min(opacity, GLASS);
    const m = mats[kind]; m.transparent = o < 1; m.opacity = o; m.depthWrite = o >= 1; m.needsUpdate = true;
    lineMats[kind].color.setHex(skeleton || !isSolid(kind) ? colourOf(kind) : GOLD);
    return m;
  }
  const shownKind = (kind) => isSolid(kind) || view.helpers;
  const placedSet = (w) => new Set(view.placed[w] ?? []);
  /** Is this piece placed? Outside Build it yourself every piece is. */
  const isPlaced = (w, key, set = placedSet(w)) => !view.build || set.has(key);

  function disposeSlab(s) { for (const c of [...s.group.children]) { s.group.remove(c); c.geometry?.dispose(); } s.drawn = []; s.ghost = null; }
  /** (Re)make a slab's pieces for the current mix (the octet slab's pieces depend on T and O) and draw it. */
  function makeSlab(w) {
    let s = slabs.get(w);
    if (!s) { s = { world: w, group: new THREE.Group(), y: 0, drawn: [], ghost: null }; group.add(s.group); slabs.set(w, s); }
    const made = slabPieces(w, view.mix);
    s.pieces = made.pieces; s.top = made.top; s.keys = made.pieces.map(pieceKey);
    if (view.placed[w]) { const ks = new Set(s.keys); view.placed[w] = view.placed[w].filter((k) => ks.has(k)); }
    drawSlab(s);
    return s;
  }
  function drawSlab(s) {
    disposeSlab(s);
    if (!active) return;
    const set = placedSet(s.world), placed = [], ghosts = [];
    s.pieces.forEach((p, i) => { if (!shownKind(p.kind)) return; (isPlaced(s.world, s.keys[i], set) ? placed : ghosts).push(i); });
    for (const kind of [...new Set(placed.map((i) => s.pieces[i].kind))]) {
      const idx = placed.filter((i) => s.pieces[i].kind === kind);
      const { g, e } = piecesGeometry(idx.map((i) => s.pieces[i]));
      const mesh = new THREE.Mesh(g, matFor(kind)); mesh.userData = { kind: 'pm', piece: kind };
      mesh.visible = !skeleton;
      const line = new THREE.LineSegments(e, lineMats[kind]);
      s.group.add(mesh, line); s.drawn.push({ kind, mesh, line });
    }
    if (ghosts.length) {
      const { g, e, pieceOfTri } = piecesGeometry(ghosts.map((i) => s.pieces[i]));
      const mesh = new THREE.Mesh(g, ghostPickMat); mesh.userData = { kind: 'pm-ghost', world: s.world, pieceOfTri, ghosts };
      s.group.add(mesh); s.ghost = { mesh, ghosts };
      for (const kind of [...new Set(ghosts.map((i) => s.pieces[i].kind))]) {
        s.group.add(new THREE.LineSegments(piecesGeometry(ghosts.filter((i) => s.pieces[i].kind === kind).map((i) => s.pieces[i])).e, ghostLineMat(kind)));
      }
    }
  }
  function syncSlabs({ animate = false } = {}) {
    const want = active ? slabsOf(view.mix) : [];
    for (const [w, s] of slabs) if (!want.includes(w)) { disposeSlab(s); group.remove(s.group); slabs.delete(w); }
    const added = [];
    for (const w of want) { if (!slabs.has(w)) added.push(w); makeSlab(w); }
    place(animate ? added : null);
  }
  const ordered = () => SLAB_ORDER.filter((w) => slabs.has(w)).map((w) => slabs.get(w));
  const height = () => { const o = ordered(); return o.reduce((a, s) => a + s.top, 0) + Math.max(0, o.length - 1) * GAP * view.spread / 100; };
  function targets() {
    const d = GAP * view.spread / 100, out = new Map(); let y = -height() / 2;
    for (const s of ordered()) { out.set(s.world, y); y += s.top + d; }
    return out;
  }
  let anim = null;
  /** Move the slabs to their places: at once, or (dropped = new layers) gliding, the new ones falling from above. */
  function place(dropped) {
    const to = targets();
    if (!dropped) { anim = null; for (const s of ordered()) { s.y = to.get(s.world); s.group.position.y = s.y; } return; }
    const from = new Map(ordered().map((s) => [s.world, dropped.includes(s.world) ? to.get(s.world) + DROP : s.y]));
    const me = anim = { from, to, t0: performance.now() };
    const step = (now) => {
      if (anim !== me) return;                            // a newer move took over
      const u = Math.max(0, Math.min(1, (now - me.t0) / ANIM_MS)), e = 1 - (1 - u) ** 3;
      for (const s of ordered()) { const a = anim.from.get(s.world) ?? s.y, b = anim.to.get(s.world); s.y = a + (b - a) * e; s.group.position.y = s.y; }
      if (u < 1 && active) requestAnimationFrame(step); else { anim = null; for (const s of ordered()) { s.y = to.get(s.world); s.group.position.y = s.y; } }
    };
    requestAnimationFrame(step);
  }
  const fit = () => fitView([0, 0, 0], K * Math.max(1.6 * 1.5 * PHI, height() / 2 + 1.5), null, true);
  const redrawAll = () => { for (const s of slabs.values()) drawSlab(s); };

  const pieceName = (kind, L = lang()) => t(`pm.piece.${KEY[kind] ?? kind}`, L);
  const named = (kind) => (isSolid(kind) ? pieceName(kind) : `${kind} ${pieceName(kind)}`);
  function placePieces(w, keys) {
    const set = placedSet(w); for (const k of keys) set.add(k);
    view.placed[w] = [...set];
  }
  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || (ud.kind !== 'pm' && ud.kind !== 'pm-ghost') || mode === 'paint' || mode === 'chisel') return false;
    if (ud.kind === 'pm') { showHudPrompt(named(ud.piece), 2200); return true; }
    const s = slabs.get(ud.world), i = ud.ghosts[ud.pieceOfTri[hit.faceIndex]];
    if (!s || i === undefined) return false;
    placePieces(ud.world, [s.keys[i]]);
    drawSlab(s); renderPanel(); commit();
    showHudPrompt(named(s.pieces[i].kind), 1600);
    return true;
  }
  const counts = () => {
    let total = 0, placed = 0;
    for (const s of slabs.values()) { const set = placedSet(s.world); s.pieces.forEach((p, i) => { if (!shownKind(p.kind)) return; total++; if (isPlaced(s.world, s.keys[i], set)) placed++; }); }
    return { total, placed };
  };

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldplatonicmix-panel'; panel.className = 'qc-panel';
  const style = document.createElement('style');
  const hex = (c) => `#${c.toString(16).padStart(6, '0')}`;
  style.textContent = `#worldplatonicmix-panel [hidden]{display:none!important}
#worldplatonicmix-panel .pm-letters{display:flex;gap:8px;justify-content:center}
#worldplatonicmix-panel .pm-letters button{min-width:56px;min-height:56px;font-size:24px;font-weight:700;border-radius:12px;border:3px solid var(--pm-c);background:transparent;color:var(--pm-c);touch-action:manipulation}
#worldplatonicmix-panel .pm-letters button.active{background:var(--pm-c);color:#111;border-color:#deb250}
#worldplatonicmix-panel .pm-helpers{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;font:var(--text-s)/1.4 var(--font-ui);color:#cde}
#worldplatonicmix-panel .pm-helpers span{display:inline-flex;align-items:center;gap:5px}
#worldplatonicmix-panel .pm-helpers i{display:inline-block;width:11px;height:11px;border-radius:2px;border:1px solid #deb250}
#worldplatonicmix-panel .pm-helpers b{color:#deb250}
#worldplatonicmix-panel .pm-spread-row input{width:100%}
#worldplatonicmix-panel .pm-spread-row label{flex:1}`;
  document.head.appendChild(style);
  panel.innerHTML = `
    <div class="w4d-row st-note pm-note"></div>
    <div class="w4d-row pm-letters">${WORLDS.map((w) => `<button type="button" data-pm-world="${w}" style="--pm-c:${hex(SOLID_COLOURS[w])}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options"><button type="button" data-pm="build"></button><button type="button" data-pm="fill"></button><button type="button" data-pm="helpers"></button></div>
    <div class="w4d-row pm-helpers"></div>
    <div class="w4d-row pm-spread-row"><label class="hull-pick"><span class="pm-spread-label"></span> <input type="range" class="st-slider" min="0" max="100" step="1"></label></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'platonicMix');
  const slider = panel.querySelector('.pm-spread-row input');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), all = [...slabs.values()].flatMap((s) => s.pieces), used = helpersOf(all), empty = !view.mix;
    const order = ordered().map((s) => (s.world === 'TO' ? ['T', 'O'].filter((x) => view.mix.includes(x)).join('') : s.world)).join(' · ');
    const { total, placed } = counts();
    panel.querySelector('.pm-note').textContent = empty ? t('pm.hint', L)
      : view.build ? t('pm.count', L, { placed, total }) : t('pm.note', L, { order, n: slabs.size });
    panel.querySelectorAll('[data-pm-world]').forEach((b) => {
      const w = b.dataset.pmWorld, on = view.mix.includes(w);
      b.textContent = w; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on));
      b.title = b.ariaLabel = t(`pm.piece.${w}`, L);
    });
    const bb = panel.querySelector('[data-pm="build"]');
    bb.textContent = t('pm.build', L); bb.classList.toggle('active', view.build); bb.setAttribute('aria-pressed', String(view.build));
    const fb = panel.querySelector('[data-pm="fill"]');
    fb.hidden = !view.build || placed >= total; fb.textContent = t('pm.fill', L);
    const hb = panel.querySelector('[data-pm="helpers"]');
    hb.hidden = !used.length;                        // empty, or cubes alone: no helpers, no toggle (nothing unnecessary shown)
    hb.textContent = t(view.helpers ? 'pm.helpers.on' : 'pm.helpers.off', L);
    hb.classList.toggle('active', view.helpers); hb.setAttribute('aria-pressed', String(view.helpers));
    const list = panel.querySelector('.pm-helpers');
    list.hidden = !used.length || !view.helpers;
    list.innerHTML = used.map((k) => `<span><i style="background:${hex(HELPER_COLOURS[k])}"></i><b>${k}</b> ${pieceName(k, L)}</span>`).join('');
    panel.querySelector('.pm-spread-row').hidden = slabs.size < 2; // one slab or none: nothing to spread
    panel.querySelector('.pm-spread-label').textContent = t('pm.spread', L);
    slider.value = String(view.spread);
  }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || !panel.contains(b)) return;
    if (b.dataset.pmWorld) {
      const w = b.dataset.pmWorld, on = view.mix.includes(w);
      view.mix = cleanMix(on ? view.mix.replace(w, '') : view.mix + w);
      const slab = slabsOf(w)[0];
      if (!slabsOf(view.mix).includes(slab)) delete view.placed[slab];   // a layer taken out starts afresh when it comes back
      syncSlabs({ animate: !on }); renderPanel(); fit(); commit();
      if (!on && view.build) showHudPrompt(t('pm.prompt.build', lang()), 3500);
      return;
    }
    if (b.dataset.pm === 'build') {
      view.build = !view.build; view.placed = {};      // on: every layer back to ghosts; off: every piece shown
      redrawAll(); renderPanel(); commit();
      if (view.build) showHudPrompt(t('pm.prompt.build', lang()), 3500);
      return;
    }
    if (b.dataset.pm === 'fill') {
      for (const s of slabs.values()) placePieces(s.world, s.keys.filter((k, i) => shownKind(s.pieces[i].kind)));
      redrawAll(); renderPanel(); commit();
      return;
    }
    if (b.dataset.pm === 'helpers') { view.helpers = !view.helpers; redrawAll(); renderPanel(); commit(); }
  });
  slider.addEventListener('input', () => { view.spread = Number(slider.value); place(null); });
  slider.addEventListener('change', () => { commit(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [...slabs.values()].flatMap((s) => [...s.drawn.filter((d) => d.mesh.visible).map((d) => d.mesh), ...(s.ghost ? [s.ghost.mesh] : [])]),
    handleTap,
    /** ?open=platonicMix:<letters>, e.g. ?open=platonicMix:DIC: those layers in, whole. */
    open(arg) {
      const m = cleanMix(arg ?? '');
      if (m) { view.mix = m; view.build = false; view.placed = {}; }
      save(); if (active) { syncSlabs(); renderPanel(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      syncSlabs(); renderPanel();
      if (!on) return;
      fit();
      showHudPrompt(t('pm.prompt.start', lang()), 5000);
    },
    setSkeleton(on) { skeleton = on; if (active) redrawAll(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) redrawAll(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return !view.mix; },
    clear() { Object.assign(view, PRESET, { placed: {} }); save(); if (active) { syncSlabs(); renderPanel(); fit(); } },
    resetView() {},
    snapshot,
    restore(json) { read(json); save(); if (active) { syncSlabs(); renderPanel(); } },
    /** For the browser tests (?probe). */
    probe() {
      const { total, placed } = counts();
      return { mix: view.mix, helpers: view.helpers, spread: view.spread, build: view.build, slabs: ordered().map((s) => s.world), total, placed,
        ghosts: total - placed, pieces: [...slabs.values()].reduce((a, s) => a + s.pieces.length, 0), animating: !!anim,
        shownKinds: [...new Set([...slabs.values()].flatMap((s) => s.drawn.map((d) => d.kind)))], slabY: ordered().map((s) => s.y) };
    },
    /** For the browser tests: the world-space centre of the k-th ghost nearest the eye (k = 0: the nearest). */
    ghostPoint(eye, k = 0) {
      const all = [];
      group.updateMatrixWorld(true);
      for (const s of slabs.values()) for (const i of s.ghost?.ghosts ?? []) {
        const v = new THREE.Vector3(...turned(pieceCentre(s.pieces[i]))); s.group.localToWorld(v); all.push([v.distanceTo(eye), v]);
      }
      all.sort((a, b) => a[0] - b[0]);
      return all[k]?.[1].toArray() ?? null;
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: a dodecahedron of edge 1. */
export function platonicMixPreviewPoints() {
  const P = [], h = PHI / 2;
  for (const x of [-h, h]) for (const y of [-h, h]) for (const z of [-h, h]) P.push([x, y, z]);
  for (const a of [1, -1]) for (const b of [1, -1]) P.push([0, a / 2, b * PHI * PHI / 2], [b * PHI * PHI / 2, 0, a / 2], [a / 2, b * PHI * PHI / 2, 0]);
  return P;
}
