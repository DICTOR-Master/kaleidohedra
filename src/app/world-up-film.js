// The Universal PiTet film (DICTO 2026-10-19): the UP cycle ID ⊂ RT ⊂ DICTO GTI ⊂ DICTO FPD ⊂ ID·10/φ⁴, one turn with the turn inside it,
// on Dual Vision's standard (DICTO: "Dual Vision is the standard"), cloned from Vajrayana's cycle: it opens cut away (the side bar's ⛶
// wedge, a quarter facing the camera; ⛶ again gives the X-ray plane, then off, when the shells turn to glass); the ∞ film peels one station
// at a time from the outside, pausing on each, and zooms by 10/φ⁴ a turn so it runs for ever (◀ builds back out); a Pieces switch fills
// each shell with its pieces (one per face of the solid inside it), which peel with the station that closes them. Tapping a shell names it.
// Opened from the Universal PiTet world's panel (world-up.js). Data: up-film-data.js (scripts/build-up-data.py), loaded on first entry and
// let go on leaving. Words: i18n upf.* and Dual Vision's / Vajrayana's film words.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { createInfinityPlayer } from './infinity-player.js';

// colours by solid, as in the UP world's shells: ID gold, RT cyan, GTI rose, FPD green
const COL = { ID: 0xfff176, RT: 0x4dd0e1, GTI: 0xf06292, FPD: 0x5fd38a, IDk: 0xfff176 };
const PIECE_COL = { RT: 0x90caf9, GTI: 0x9fb4c8, FPD: 0x64b5f6, IDk: 0x7986cb };
const NAMES = { ID: 'ID', RT: 'RT', GTI: 'DICTO GTI', FPD: 'DICTO FPD', IDk: 'ID·10/φ⁴' };
const FULL = { ID: 'the icosidodecahedron', RT: 'the rhombic triacontahedron', GTI: 'the DICTO Golden Truncated Icosahedron',
  FPD: 'the DICTO Flat Pentakis Dodecahedron', IDk: 'the next icosidodecahedron, 10/φ⁴ larger: the next turn begins' };
// the film peels a turn outside in: 4 stations, then the turn inside has become the first (10/φ⁴ larger), so it loops without a seam
const PEEL = ['IDk', 'FPD', 'GTI', 'RT'];
const N = PEEL.length;
const PRESET = { pieces: false };
const STEP_SECONDS = 1.6, PAUSE_MS = 900;
const lang = () => getSettings().language;

export function createUpFilmWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {}, openWorld = () => {} }) {
  const STORAGE_KEY = storageKey('upfilm');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  try { const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'); if (d) restoreView(d); } catch { /* the preset */ }
  function restoreView(d) { if (typeof d.pieces === 'boolean') view.pieces = d.pieces; }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...view })); } catch { /* best-effort */ } };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, wedge = true, pickTargets = [], items = [];
  const load = () => (loading ??= import('./up-film-data.js').then((m) => { DATA = m.default; }));
  function clearGroup() { for (const c of [...group.children]) { group.remove(c); c.geometry?.dispose(); c.material?.dispose(); } pickTargets = []; items = []; }
  // the wedge: two planes through the centre a quarter turn apart, facing the camera; a material carries them (userData.wedgePlanes),
  // and render.js applies them while the X-ray plane is off
  let wedgePlanes = null;
  function makeWedge() {
    const v3 = (a) => new THREE.Vector3(...a), dir = v3(DATA.view.dir).normalize(), up = v3(DATA.view.up);
    const wr = dir.clone().sub(up.clone().multiplyScalar(dir.dot(up))).normalize(), side = up.clone().cross(wr), a = Math.PI / 4;
    wedgePlanes = [new THREE.Plane(wr.clone().multiplyScalar(-Math.sin(a)).add(side.clone().multiplyScalar(Math.cos(a))), 0),
      new THREE.Plane(wr.clone().multiplyScalar(-Math.sin(a)).sub(side.clone().multiplyScalar(Math.cos(a))), 0)];
  }
  function addSolid(S, colour, s, key, turn, shrink = 1) {
    const c = S.v.reduce((a, v) => a.map((x, i) => x + v[i] / S.v.length), [0, 0, 0]);
    const V = S.v.map((v) => v.map((x, i) => (c[i] + shrink * (x - c[i])) * s * WS)), pos = [], line = [];
    for (const f of S.f) {
      for (let i = 1; i + 1 < f.length; i++) pos.push(...V[f[0]], ...V[f[i]], ...V[f[i + 1]]);
      for (let i = 0; i < f.length; i++) line.push(...V[f[i]], ...V[f[(i + 1) % f.length]]);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    const glass = !wedge || opacity < 1 || skeleton;
    const op = skeleton ? 0 : glass ? (wedge ? opacity : 0.14) : 1;
    const mat = new THREE.MeshStandardMaterial({ color: colour, roughness: 0.5, flatShading: true, side: THREE.DoubleSide, transparent: glass, opacity: op, depthWrite: !glass });
    mat.userData.wedgePlanes = wedge ? wedgePlanes : null; mat.userData.baseOpacity = mat.opacity;
    // in glass (the wedge off) the stations are shells and stay hollow in a cut; the pieces are always solid
    mat.userData.hollow = !wedge && !key.startsWith('p:');
    const mesh = new THREE.Mesh(g, mat); mesh.userData = { kind: 'upf', key, turn };
    const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    const lmat = new THREE.LineBasicMaterial({ color: skeleton ? colour : 0x2a2218, transparent: true, opacity: skeleton ? 0.9 : glass && !wedge ? 0.55 : 0.5 });
    lmat.userData.wedgePlanes = mat.userData.wedgePlanes; lmat.userData.baseOpacity = lmat.opacity;
    const ln = new THREE.LineSegments(lg, lmat);
    group.add(mesh, ln); pickTargets.push(mesh); items.push({ mesh, line: ln, key, turn });
  }
  function draw() {
    clearGroup();
    if (!active || !DATA) return;
    if (!wedgePlanes) makeWedge();
    const turns = film.on ? [0, -1, -2] : [0, -1];
    for (const turn of turns) {
      const s = DATA.K ** turn;
      // the outer ID of a turn is the next turn's ID (IDk); the ID at 1 is drawn by the turn inside
      addSolid(DATA.stations.ID, COL.IDk, s * DATA.K, 'IDk', turn);
      for (const k of ['FPD', 'GTI', 'RT']) addSolid(DATA.stations[k], COL[k], s, k, turn);
      if (view.pieces) for (const k of PEEL) for (const p of DATA.pieces[k]) addSolid(p, PIECE_COL[k], s, `p:${k}`, turn, 0.965);
    }
    // the very centre (the innermost turn's ID): a small solid, so the core never shows a hole
    addSolid(DATA.stations.ID, COL.ID, DATA.K ** turns[turns.length - 1], 'ID', turns[turns.length - 1]);
    applyFilm();
  }
  // ---- the film: u runs over the 4 peels of a turn; station PEEL[j] of turn 0 lifts away and fades while u passes j, its shell's pieces
  // with it; the whole scene grows by (10/φ⁴)^(1/4) a step, so after 4 the turn inside has become the first
  const film = { on: false, dir: 0, t: 0, pauseUntil: 0, last: 0, raf: 0, lastDir: 1 };
  const modN = (x) => ((x % N) + N) % N;
  const peelIndex = (key) => PEEL.indexOf(key.startsWith('p:') ? key.slice(2) : key);
  function applyFilm() {
    const u = film.on ? modN(film.t) : 0;
    group.scale.setScalar(film.on ? DATA.K ** (u / N) : 1);
    for (const it of items) {
      const j = peelIndex(it.key), prog = film.on && it.turn === 0 && j >= 0 ? Math.min(1, Math.max(0, u - j)) : 0;
      const k = 1 + 0.45 * prog * prog; it.mesh.scale.setScalar(k); it.line.scale.setScalar(k);
      const o = 1 - prog; it.mesh.visible = it.line.visible = o > 0.01;
      const m = it.mesh.material, b = m.userData.baseOpacity;
      m.transparent = m.transparent || o < 1; m.opacity = b * o; if (o < 1) m.depthWrite = false;
      it.line.material.opacity = it.line.material.userData.baseOpacity * o;
    }
  }
  function tick(now) {
    film.raf = 0;
    if (!active || !film.on) return;
    const dt = film.last ? Math.min(0.1, (now - film.last) / 1000) : 0; film.last = now;
    if (film.dir && now >= film.pauseUntil) {
      const before = film.t; film.t += film.dir * dt / STEP_SECONDS;
      const crossed = film.dir > 0 ? Math.floor(film.t) > Math.floor(before) : Math.ceil(film.t) < Math.ceil(before);
      if (crossed) { film.t = film.dir > 0 ? Math.floor(film.t) : Math.ceil(film.t); film.pauseUntil = now + PAUSE_MS; showStation(); }
      applyFilm(); syncSlider();
    }
    film.raf = requestAnimationFrame(tick);
  }
  // the station the film has stopped on: the outermost one still standing
  function showStation() { const key = PEEL[Math.round(modN(film.t)) % N]; showHudPrompt(`${NAMES[key]} · ${FULL[key]}`, 1600); }
  function setFilm(dir) {
    const wasOn = film.on; if (film.dir) film.lastDir = film.dir;
    if (dir === film.dir && film.on) dir = 0;
    film.dir = dir; film.on = film.on || dir !== 0; film.last = 0;
    if (film.on && !wasOn) draw();
    if (!film.raf && film.on) film.raf = requestAnimationFrame(tick);
    renderPanel();
  }
  function stopFilm() { const was = film.on; film.on = false; film.dir = 0; film.t = 0; if (film.raf) cancelAnimationFrame(film.raf); film.raf = 0; group.scale.setScalar(1); if (was) draw(); }
  const fit = () => DATA && fitView([0, 0, 0], 1.05 * DATA.radius * WS, DATA.view.dir);

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'upf' || !DATA || mode === 'paint') return false;
    const key = ud.key.startsWith('p:') ? ud.key.slice(2) : ud.key;
    showHudPrompt(ud.key.startsWith('p:') ? t('upf.prompt.piece', lang(), { solid: NAMES[key] }) : `${NAMES[key]} · ${FULL[key]}`, 3200);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldupfilm-panel'; panel.className = 'qc-panel';
  const player = createInfinityPlayer({
    onDir: (d) => { const first = !film.on; setFilm(d); if (first) showHudPrompt(t('upf.prompt.film', lang()), 4500); },
    onPause: () => { if (!film.on) return; if (film.dir) setFilm(film.dir); else setFilm(film.lastDir || 1); },
    words: (L) => ({ wrap: t('dv.film.wrap', L), unwrap: t('dv.film.unwrap', L), pause: t('dv.film.pause', L) }),
  });
  panel.innerHTML = `
    <div class="w4d-row st-note upf-note"></div>
    <div class="w4d-row upf-film-row"><label class="hull-pick"><span class="upf-film-pos"></span> <input type="range" class="st-slider" min="0" max="400" step="1"></label></div>
    <div class="w4d-row w4d-options"><button type="button" data-upf="pieces"></button><button type="button" data-upf="up"></button><button type="button" data-upf="reset"></button></div>`;
  panel.insertBefore(player.el, panel.querySelector('.upf-film-row'));
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'upfilm');
  const slider = panel.querySelector('.upf-film-row input');
  const syncSlider = () => { slider.value = String(Math.round(modN(film.t) * 100)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    if (!DATA) { panel.querySelector('.upf-note').textContent = t('vj.loading', L); return; }
    panel.querySelector('.upf-note').textContent = t('upf.note', L);
    player.render(film, L);
    panel.querySelector('.upf-film-row').style.display = film.on && film.dir === 0 ? '' : 'none';
    panel.querySelector('.upf-film-pos').textContent = t('vj.film.position', L);
    const b = (k) => panel.querySelector(`[data-upf="${k}"]`);
    b('pieces').textContent = t(view.pieces ? 'vj.pieces.on' : 'vj.pieces.off', L); b('pieces').classList.toggle('active', view.pieces);
    b('up').textContent = t('upf.back', L);
    b('reset').textContent = t('upf.reset', L); b('reset').hidden = view.pieces === PRESET.pieces && !film.on;
  }
  const commit = () => { save(); draw(); renderPanel(); onChange(); window.dispatchEvent(new Event('krp-hud-refresh')); };
  panel.querySelector('[data-upf="pieces"]').addEventListener('click', () => { view.pieces = !view.pieces; commit(); });
  panel.querySelector('[data-upf="up"]').addEventListener('click', () => openWorld('tool:upWorld', 'Universal PiTet'));
  panel.querySelector('[data-upf="reset"]').addEventListener('click', () => { Object.assign(view, PRESET); stopFilm(); commit(); fit(); });
  slider.addEventListener('input', () => { if (!film.on) return; film.dir = 0; film.t = Math.floor(film.t / N) * N + Number(slider.value) / 100; applyFilm(); renderPanel(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on;
      if (!on) { stopFilm(); clearGroup(); DATA = null; loading = null; wedgePlanes = null; renderPanel(); return; }
      renderPanel();
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('upf.prompt.start', lang()), 5500); });
    },
    // the side bar's ⛶ (as Vajrayana): wedge → X-ray plane → off; with the wedge off the shells turn to glass
    get wedgeApplies() { return true; },
    get wedge() { return wedge; },
    setWedge(on) { if (wedge !== on) { wedge = on; if (active) draw(); window.dispatchEvent(new Event('krp-hud-refresh')); } },
    planeChanged() {},
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { Object.assign(view, PRESET); stopFilm(); save(); if (active) { draw(); renderPanel(); } },
    resetView() {},
    snapshot: () => ({ version: 1, ...view }),
    restore(json) { if (json) restoreView(json); save(); draw(); renderPanel(); },
  };
}
