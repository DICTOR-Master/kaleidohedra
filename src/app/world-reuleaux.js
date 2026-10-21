// The Reuleaux Platonic Solids (DICTO 2026-10-21; DICTO's idea, paper #45, DICTO DOI 10.5281/zenodo.23529499): for each Platonic solid,
// the common part of balls centred on its corners, of radius D, the solid's diameter. Named by look: balls on the tetrahedron make the
// Reuleaux tetrahedron, on the cube the Reuleaux octahedron, on the octahedron the Reuleaux cube, on the dodecahedron the Reuleaux
// icosahedron, on the icosahedron the Reuleaux dodecahedron. Two modes:
//   - Film, "balls into body": the bare solid; glass balls grow on its corners; their shared part appears and grows until the balls reach
//     radius D, where it is the Reuleaux body. Played on the ∞ player (Dual Vision's standard), with a big scrub slider.
//   - Build: the five bodies as pieces placed by hand, face to face, settling corner to corner: tap a face (a ball patch) of a placed
//     body and the chosen body attaches with one of its faces' corners on the tapped face's corners, on the other side. The caps are
//     convex, so neighbours overlap in a lens (DICTO: the look). Each body is drawn at the size where its face corners are 1 apart, so
//     every three-cornered face takes every three-cornered body. When the chosen body doesn't fit a face, the ones that do are offered
//     (no arrows). Long-press (Remove) takes one away; undo and clear as usual.
// Data: reuleaux-data.js (scripts/build-reuleaux-data.py), loaded on first entry and let go on leaving. Words: i18n rl.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey, theme } from './site.js';
import { createInfinityPlayer } from './infinity-player.js';

export const REULEAUX_KEYS = ['tetrahedron', 'octahedron', 'cube', 'icosahedron', 'dodecahedron'];
const EDGE_COLOR = 0x0b1220;
const STEP_SECONDS = 0.45, END_PAUSE_MS = 1600, APPEAR = 2;
const PRESET = { body: 'tetrahedron', mode: 'film', balls: true };
const lang = () => getSettings().language;
const name = (key, L = lang()) => t(`rl.name.${key}`, L);

/** Decoded meshes, one per body: { geometry (indexed), seams (LineSegments geometry), patch } for a stored {v, t, s, patch?}. */
function decode(m, Q) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(m.v.map((x) => x / Q), 3));
  g.setIndex(m.t); g.computeVertexNormals(); g.computeBoundingSphere();
  const P = m.v, s = [];
  for (const i of m.s) s.push(P[3 * i] / Q, P[3 * i + 1] / Q, P[3 * i + 2] / Q);
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(s, 3));
  return { geometry: g, seams: lg, patch: m.patch ?? null };
}

/** Where a body of type B goes on a face whose corners W (world, counter-clockwise seen from outside the old body) are given: one of
 *  B's faces with its corners on W, B on the other side. Returns { position, quaternion } or null if the corners don't match. */
export function placeOn(B, W) {
  const k = W.length, f = B.faces[0];
  if (f.length !== k) return null;
  const s = 1 / B.side, L = f.map((i) => new THREE.Vector3(...B.corners[i]).multiplyScalar(s));
  // seen from outside B, its face runs the other way round: L[j] onto W[-j]
  const Wr = [W[0], ...W.slice(1).reverse()];
  const frame = (P) => {
    const e1 = P[1].clone().sub(P[0]).normalize(), n = P[1].clone().sub(P[0]).cross(P[2].clone().sub(P[0])).normalize();
    return new THREE.Matrix4().makeBasis(e1, n.clone().cross(e1), n);
  };
  const R = frame(Wr).multiply(frame(L).transpose());
  const quaternion = new THREE.Quaternion().setFromRotationMatrix(R);
  const position = Wr[0].clone().sub(L[0].clone().applyQuaternion(quaternion));
  for (let j = 0; j < k; j++) if (L[j].clone().applyQuaternion(quaternion).add(position).distanceTo(Wr[j]) > 1e-6) return null;
  return { position, quaternion };
}

export function createReuleauxWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('reuleaux');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  let nodes = []; // the build: { type, p: [x, y, z], q: [x, y, z, w] }, in units of a face side
  const validNode = (n) => n && REULEAUX_KEYS.includes(n.type) && Array.isArray(n.p) && n.p.length === 3 && Array.isArray(n.q) && n.q.length === 4 && [...n.p, ...n.q].every(Number.isFinite);
  function read(d) {
    if (!d) return;
    if (REULEAUX_KEYS.includes(d.view?.body)) view.body = d.view.body;
    if (['film', 'build'].includes(d.view?.mode)) view.mode = d.view.mode;
    if (typeof d.view?.balls === 'boolean') view.balls = d.view.balls;
    nodes = Array.isArray(d.nodes) ? d.nodes.filter(validNode).map((n) => ({ type: n.type, p: [...n.p], q: [...n.q] })) : [];
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, view: { ...view }, nodes: nodes.map((n) => ({ type: n.type, p: [...n.p], q: [...n.q] })) });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const startBuild = () => { nodes = [{ type: view.body, p: [0, 0, 0], q: [0, 0, 0, 1] }]; };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, pickTargets = [];
  const bodies = new Map(), frameCache = new Map();
  const load = () => (loading ??= import('./reuleaux-data.js').then((m) => {
    DATA = m.default;
    for (const B of DATA.bodies) bodies.set(B.key, B);
  }));
  const bodyMesh = (B) => (B._mesh ??= decode(B.body, DATA.Q));
  const frames = (B) => { if (!frameCache.has(B.key)) frameCache.set(B.key, B.frames.map((f) => decode(f, DATA.Q))); return frameCache.get(B.key); };
  function releaseData() {
    for (const B of bodies.values()) if (B._mesh) { B._mesh.geometry.dispose(); B._mesh.seams.dispose(); delete B._mesh; }
    for (const list of frameCache.values()) for (const f of list) { f.geometry.dispose(); f.seams.dispose(); }
    frameCache.clear(); bodies.clear(); DATA = null; loading = null;
  }

  // materials: the app's piece look; glass for the balls and the bare solid
  const pieceMat = new THREE.MeshStandardMaterial({ color: theme().pieceHex, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xbfe6ff, roughness: 0.15, metalness: 0.1, transparent: true, opacity: 0.13, depthWrite: false, side: THREE.FrontSide });
  ballMat.userData.hollow = true;
  const solidMat = new THREE.MeshStandardMaterial({ color: 0xdfe6ea, flatShading: true, transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide });
  solidMat.userData.hollow = true;
  const seamMat = new THREE.LineBasicMaterial({ color: EDGE_COLOR });
  const solidEdgeMat = new THREE.LineBasicMaterial({ color: EDGE_COLOR, transparent: true, opacity: 0.85 });
  const ballGeo = new THREE.SphereGeometry(1, 48, 24);
  function styleMaterials() {
    pieceMat.color.setHex(theme().pieceHex);
    pieceMat.transparent = opacity < 1; pieceMat.opacity = opacity; pieceMat.depthWrite = opacity >= 1; pieceMat.needsUpdate = true;
    seamMat.color.setHex(skeleton ? theme().accentHex : EDGE_COLOR);
    solidEdgeMat.color.setHex(skeleton ? theme().accentHex : EDGE_COLOR);
  }

  function clearGroup() {
    for (const c of [...group.children]) { group.remove(c); if (c.userData.ownGeometry) c.geometry.dispose(); }
    pickTargets = []; filmParts = null;
  }

  // ---- the film ----
  // t runs 0 → END: over [0, 1] the balls grow to the circumradius R (where they first all meet, at the centre); over [1, END] the
  // radius runs on from R to D, and the shared part at the largest stored radius not above it is shown (it appears at t = APPEAR).
  const film = { on: false, dir: 0, t: 0, pauseUntil: 0, last: 0, raf: 0, lastDir: 1 };
  const END = () => (DATA ? DATA.frames + 1 : 17);
  let filmParts = null;
  const filmScale = (B) => WS * 1.6 / (B.R + B.D); // every body about the same size on screen
  function radiusAt(B, u) { return u <= 1 ? B.R * u : B.R + (B.D - B.R) * (u - 1) / DATA.frames; }
  function drawFilm() {
    const B = bodies.get(view.body), s = filmScale(B);
    const holder = new THREE.Group(); holder.scale.setScalar(s); group.add(holder);
    // the bare solid: glass faces and its edges
    const V = B.balls, hp = [], el = [];
    for (const tri of B.hull) for (const i of tri) hp.push(...V[i]);
    for (const [a, b] of B.edges) el.push(...V[a], ...V[b]);
    const hg = new THREE.BufferGeometry(); hg.setAttribute('position', new THREE.Float32BufferAttribute(hp, 3)); hg.computeVertexNormals();
    const solid = new THREE.Mesh(hg, solidMat); solid.userData = { kind: 'rl', film: 'solid', ownGeometry: true }; solid.visible = !skeleton;
    const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(el, 3));
    const edges = new THREE.LineSegments(eg, solidEdgeMat); edges.userData.ownGeometry = true;
    holder.add(solid, edges);
    // the balls, one per corner
    const balls = V.map((v) => { const m = new THREE.Mesh(ballGeo, ballMat); m.position.set(...v); m.userData = { kind: 'rl', film: 'ball' }; holder.add(m); return m; });
    // the shared part, one mesh per stored radius
    const parts = frames(B).map((f) => {
      const m = new THREE.Mesh(f.geometry, pieceMat); m.userData = { kind: 'rl', film: 'part' };
      const l = new THREE.LineSegments(f.seams, seamMat); m.visible = l.visible = false; holder.add(m, l); return [m, l];
    });
    filmParts = { B, holder, solid, balls, parts };
    pickTargets.push(solid, ...parts.map((p) => p[0]));
    applyFilm();
  }
  function applyFilm() {
    if (!filmParts) return;
    const { B, balls, parts } = filmParts, u = film.t, r = radiusAt(B, u);
    for (const b of balls) { b.scale.setScalar(Math.max(1e-4, r)); b.visible = view.balls && r > 1e-3; }
    const k = Math.floor(u + 1e-9) - APPEAR;
    parts.forEach(([m, l], i) => { m.visible = i === Math.min(k, parts.length - 1) && !skeleton; l.visible = i === Math.min(k, parts.length - 1); });
    syncSlider();
  }
  function tick(now) {
    film.raf = 0;
    if (!active || !film.on || view.mode !== 'film') return;
    const dt = film.last ? Math.min(0.1, (now - film.last) / 1000) : 0; film.last = now;
    if (film.dir && now >= film.pauseUntil) {
      const before = film.t, end = END();
      film.t += film.dir * dt / STEP_SECONDS;
      if (film.dir > 0 && before < APPEAR && film.t >= APPEAR) showHudPrompt(t('rl.prompt.appear', lang()), 2200);
      if (film.dir > 0 && film.t >= end) {
        if (before < end) { film.t = end; film.pauseUntil = now + END_PAUSE_MS; showHudPrompt(t('rl.prompt.done', lang(), { name: name(view.body) }), 2400); }
        else film.t = 0; // round the ∞: the bare solid again
      } else if (film.dir < 0 && film.t <= 0) {
        if (before > 0) { film.t = 0; film.pauseUntil = now + END_PAUSE_MS; } else film.t = end;
      }
      applyFilm();
    }
    film.raf = requestAnimationFrame(tick);
  }
  function setFilm(dir) {
    if (film.dir) film.lastDir = film.dir;
    if (dir === film.dir && film.on) dir = 0;
    film.dir = dir; film.on = film.on || dir !== 0; film.last = 0;
    if (dir > 0 && film.t >= END()) film.t = 0;
    if (dir < 0 && film.t <= 0) film.t = END();
    if (!film.raf && film.on) film.raf = requestAnimationFrame(tick);
    renderPanel();
  }
  function stopFilm() { film.on = false; film.dir = 0; film.t = 0; if (film.raf) cancelAnimationFrame(film.raf); film.raf = 0; }

  // ---- the build ----
  const nodeQ = (n) => new THREE.Quaternion(...n.q), nodeP = (n) => new THREE.Vector3(...n.p);
  function drawBuild() {
    const holder = new THREE.Group(); holder.scale.setScalar(WS); group.add(holder);
    nodes.forEach((n, i) => {
      const B = bodies.get(n.type), M = bodyMesh(B);
      const m = new THREE.Mesh(M.geometry, pieceMat); m.userData = { kind: 'rl', node: i };
      const l = new THREE.LineSegments(M.seams, seamMat);
      for (const o of [m, l]) { o.position.copy(nodeP(n)); o.quaternion.copy(nodeQ(n)); o.scale.setScalar(1 / B.side); holder.add(o); }
      m.visible = !skeleton;
      pickTargets.push(m);
    });
  }
  /** Face fi of node n: its corners in build units, counter-clockwise from outside; its mid-point on the patch; its outward direction. */
  function faceOf(n, fi) {
    const B = bodies.get(n.type), s = 1 / B.side, q = nodeQ(n), p = nodeP(n);
    const at = (v) => new THREE.Vector3(...v).multiplyScalar(s).applyQuaternion(q).add(p);
    const corners = B.faces[fi].map((i) => at(B.corners[i]));
    const c = new THREE.Vector3(...B.balls[fi]), mean = B.faces[fi].reduce((a, i) => a.add(new THREE.Vector3(...B.corners[i])), new THREE.Vector3()).divideScalar(B.faces[fi].length);
    const mid = at(mean.clone().sub(c).normalize().multiplyScalar(B.D).add(c).toArray());
    return { corners, mid, normal: mid.clone().sub(p).normalize() };
  }
  // Which bodies fit face fi of node n: those whose faces have as many corners (all faces are regular, side 1).
  const fitting = (n, fi) => REULEAUX_KEYS.filter((k) => bodies.get(k).faces[0].length === bodies.get(n.type).faces[fi].length);
  let pending = null; // a tapped face waiting for a body that fits: { node, face }
  function attach(type, ni, fi) {
    const n = nodes[ni], F = faceOf(n, fi), put = placeOn(bodies.get(type), F.corners);
    if (!put) return false;
    const pos = put.position;
    if (nodes.some((m) => m.type === type && nodeP(m).distanceTo(pos) < 1e-4)) { showHudPrompt(t('rl.prompt.taken', lang()), 2000); return true; }
    nodes.push({ type, p: pos.toArray().map((x) => Math.round(x * 1e9) / 1e9), q: put.quaternion.toArray() });
    pending = null;
    commit(); fit();
    return true;
  }
  const fitRadius = () => {
    if (view.mode === 'film' || !DATA) return 1.7 * WS;
    let r = 0;
    for (const n of nodes) { const B = bodies.get(n.type); r = Math.max(r, nodeP(n).length() + B.R / B.side * 1.25); }
    return Math.max(r, 1) * WS * 1.15;
  };
  const centre = () => {
    if (view.mode === 'film' || !nodes.length) return [0, 0, 0];
    const c = nodes.reduce((a, n) => a.add(nodeP(n)), new THREE.Vector3()).divideScalar(nodes.length).multiplyScalar(WS);
    return c.toArray();
  };
  const fit = () => fitView(centre(), fitRadius());

  function draw() {
    clearGroup();
    if (!active || !DATA) return;
    styleMaterials();
    if (view.mode === 'film') drawFilm(); else drawBuild();
  }

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'rl' || !DATA || mode === 'paint') return false;
    if (view.mode === 'film') {
      if (ud.film === 'solid') showHudPrompt(t('rl.prompt.solid', lang(), { solid: t(`rl.src.${bodies.get(view.body).source}`, lang()) }), 2600);
      else showHudPrompt(t('rl.prompt.part', lang(), { name: name(view.body) }), 2600);
      return true;
    }
    const ni = ud.node, n = nodes[ni];
    if (!n) return false;
    if (mode === 'chisel') {
      if (nodes.length <= 1) return false;
      nodes.splice(ni, 1); pending = null; commit();
      return true;
    }
    const B = bodies.get(n.type), tri = Math.floor(hit.faceIndex ?? -1), fi = bodyMesh(B).patch[tri];
    if (fi == null) return false;
    if (fitting(n, fi).includes(view.body)) return attach(view.body, ni, fi);
    pending = { node: ni, face: fi };
    showHudPrompt(t('rl.prompt.choose', lang(), { name: name(view.body), n: B.faces[fi].length }), 3200);
    renderPanel();
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldreuleaux-panel'; panel.className = 'qc-panel';
  const player = createInfinityPlayer({
    onDir: (d) => { const first = !film.on; setFilm(d); if (first) showHudPrompt(t('rl.prompt.film', lang()), 4000); },
    onPause: () => { if (!film.on) return; if (film.dir) setFilm(film.dir); else setFilm(film.lastDir || 1); },
    words: (L) => ({ wrap: t('dv.film.wrap', L), unwrap: t('dv.film.unwrap', L), pause: t('dv.film.pause', L) }),
  });
  const style = document.createElement('style');
  style.textContent = `#worldreuleaux-panel .rl-cards{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
#worldreuleaux-panel .rl-cards button{display:flex;flex-direction:column;align-items:center;min-width:96px;min-height:52px;padding:6px 8px;line-height:1.15}
#worldreuleaux-panel .rl-cards button small{opacity:.7;font-size:11px}
#worldreuleaux-panel .rl-cards button.active{border-color:var(--accent,#ff9a52);color:var(--accent,#ff9a52)}
#worldreuleaux-panel .rl-film-row input{width:100%}
#worldreuleaux-panel .rl-film-row label{flex:1}`;
  document.head.appendChild(style);
  panel.innerHTML = `
    <div class="w4d-row st-note rl-note"></div>
    <div class="w4d-row w4d-options rl-modes"><button type="button" data-rl-mode="film"></button><button type="button" data-rl-mode="build"></button></div>
    <div class="w4d-row rl-cards"></div>
    <div class="w4d-row rl-fits"></div>
    <div class="w4d-row rl-film-row"><label class="hull-pick"><span class="rl-film-pos"></span> <input type="range" class="st-slider" min="0" max="1700" step="1"></label></div>
    <div class="w4d-row w4d-options"><button type="button" data-rl="balls"></button><button type="button" data-rl="reset"></button></div>`;
  panel.insertBefore(player.el, panel.querySelector('.rl-film-row'));
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'reuleaux');
  const slider = panel.querySelector('.rl-film-row input');
  function syncSlider() { slider.max = String(END() * 100); slider.value = String(Math.round(film.t * 100)); }
  const card = (k, L, attr) => `<button type="button" ${attr}="${k}" class="${k === view.body ? 'active' : ''}" aria-pressed="${k === view.body}">${name(k, L)}<small>${t('rl.on', L, { solid: t(`rl.src.${bodies.get(k)?.source ?? ''}`, L) })}</small></button>`;
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), filmMode = view.mode === 'film';
    if (!DATA) { panel.querySelector('.rl-note').textContent = t('vj.loading', L); return; }
    const B = bodies.get(view.body);
    panel.querySelector('.rl-note').textContent = filmMode
      ? t('rl.note.film', L, { solid: t(`rl.src.${B.source}`, L), name: name(view.body, L) })
      : t('rl.note.build', L, { n: nodes.length });
    panel.querySelectorAll('[data-rl-mode]').forEach((b) => { const on = b.dataset.rlMode === view.mode; b.textContent = t(`rl.mode.${b.dataset.rlMode}`, L); b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    panel.querySelector('.rl-cards').innerHTML = REULEAUX_KEYS.map((k) => card(k, L, 'data-rl-body')).join('');
    const fits = panel.querySelector('.rl-fits');
    if (!filmMode && pending && nodes[pending.node]) {
      fits.hidden = false;
      fits.innerHTML = `<span class="rl-fits-label">${t('rl.fits', L)}</span>${fitting(nodes[pending.node], pending.face).map((k) => `<button type="button" data-rl-fit="${k}">${name(k, L)}</button>`).join('')}`;
    } else { fits.hidden = true; fits.innerHTML = ''; }
    player.el.hidden = !filmMode;
    if (filmMode) player.render(film, L);
    panel.querySelector('.rl-film-row').hidden = !filmMode;
    panel.querySelector('.rl-film-pos').textContent = t('rl.film.position', L);
    const balls = panel.querySelector('[data-rl="balls"]');
    balls.hidden = !filmMode; balls.textContent = t(view.balls ? 'rl.balls.on' : 'rl.balls.off', L); balls.classList.toggle('active', view.balls); balls.setAttribute('aria-pressed', String(view.balls));
    const reset = panel.querySelector('[data-rl="reset"]');
    reset.textContent = t(filmMode ? 'rl.reset.film' : 'rl.reset.build', L);
    reset.hidden = filmMode ? !film.on && film.t === 0 : nodes.length <= 1;
    syncSlider();
  }
  function commit() { save(); draw(); renderPanel(); onChange(); window.dispatchEvent(new Event('krp-hud-refresh')); }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || !panel.contains(b)) return;
    if (b.dataset.rlMode) {
      if (b.dataset.rlMode === view.mode) return;
      view.mode = b.dataset.rlMode; pending = null;
      if (view.mode === 'build') { if (film.raf) cancelAnimationFrame(film.raf); film.raf = 0; film.dir = 0; if (!nodes.length) startBuild(); showHudPrompt(t('rl.prompt.build', lang()), 4500); }
      commit(); fit(); return;
    }
    if (b.dataset.rlBody) {
      if (b.dataset.rlBody === view.body) return;
      view.body = b.dataset.rlBody;
      if (view.mode === 'film') { film.t = film.on ? film.t : 0; commit(); fit(); return; }
      if (nodes.length <= 1) startBuild(); // the first piece is the chosen body
      if (pending && fitting(nodes[pending.node], pending.face).includes(view.body)) { const p = pending; attach(view.body, p.node, p.face); return; }
      commit(); return;
    }
    if (b.dataset.rlFit) { const p = pending; if (!p) return; view.body = b.dataset.rlFit; attach(view.body, p.node, p.face); return; }
    if (b.dataset.rl === 'balls') { view.balls = !view.balls; save(); applyFilm(); renderPanel(); return; }
    if (b.dataset.rl === 'reset') {
      if (view.mode === 'film') { stopFilm(); applyFilm(); renderPanel(); return; }
      startBuild(); pending = null; commit(); fit();
    }
  });
  slider.addEventListener('input', () => {
    film.on = true; film.dir = 0; film.t = Number(slider.value) / 100;
    applyFilm(); player.render(film, lang()); panel.querySelector('[data-rl="reset"]').hidden = false;
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets.filter((m) => m.visible),
    handleTap,
    /** ?open=reuleaux:<build|film|key>: open in that mode, or with that body's film. */
    open(arg) {
      if (arg === 'build' || arg === 'film') view.mode = arg;
      else if (REULEAUX_KEYS.includes(arg)) { view.body = arg; view.mode = 'film'; }
      save(); if (active) { draw(); renderPanel(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { stopFilm(); clearGroup(); pending = null; releaseData(); renderPanel(); return; }
      renderPanel();
      load().then(() => {
        if (!active) return;
        if (!nodes.length) startBuild();
        draw(); renderPanel(); fit();
        showHudPrompt(t(view.mode === 'film' ? 'rl.prompt.start' : 'rl.prompt.build', lang()), 5000);
      });
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return nodes.length <= 1; },
    clear() { startBuild(); pending = null; stopFilm(); save(); if (active) { draw(); renderPanel(); fit(); } },
    resetView() {},
    snapshot,
    restore(json) { read(json); if (!nodes.length) startBuild(); pending = null; save(); draw(); renderPanel(); },
    /** For the browser tests (?probe): the build, and the mid-points and outward directions of the last piece's faces (scene units). */
    probe() {
      const n = nodes[nodes.length - 1];
      return { mode: view.mode, body: view.body, nodes: nodes.length, placed: nodes.map((m) => ({ type: m.type, p: m.p })), t: film.t, ballsShown: !!filmParts?.balls.some((b) => b.visible),
        faces: n && DATA ? bodies.get(n.type).faces.map((_, fi) => { const F = faceOf(n, fi); return { mid: F.mid.clone().multiplyScalar(WS).toArray(), normal: F.normal.toArray() }; }) : [] };
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the tetrahedron's corners pushed out round its Reuleaux body. */
export function reuleauxPreviewPoints() {
  const s = 1.15, V = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]];
  const out = [...V];
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) { const m = V[i].map((x, k) => (x + V[j][k]) / 2), l = Math.hypot(...m) || 1; out.push(m.map((x) => (x / l) * s * Math.sqrt(3) * 0.62)); }
  return out;
}
