// The DICTO Kepler–Poinsot–UP Cycle film (DICTO 2026-10-19; the tall companion of Universal PiTet): I ⊂ great stellated dodecahedron ⊂ D1
// ⊂ small stellated dodecahedron ⊂ I·φ³, one turn with the turns inside it, on Dual Vision's standard (cloned from the Universal PiTet film,
// itself cloned from Vajrayana's cycle): cut away (the side bar's ⛶ wedge → X-ray plane → off, glass), the ∞ film peeling one station at a
// time from the outside, pausing on each, zooming by φ³ a turn for ever (◀ builds back out); a Pieces switch fills each shell in the Cleo
// star's pattern, DICTO's pieces in their own colours (CLEO lilac, cap green, AXE cyan; the second shell's new valley tetrahedron amber),
// peeling with the hull that closes them. The second shell's inward pyramid is CLEO's golden reciprocal (height φ⁻² against CLEO's φ²), pale lilac. Data: kp-film-data.js (scripts/build-kp-data.py), proved exactly in the research study
// studies/2026-10-19-kepler-poinsot-up. Words: i18n kpf.* and the film words of Dual Vision and Vajrayana.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { createInfinityPlayer } from './infinity-player.js';

// colours by solid, as in the UP world's shells: ID gold, RT cyan, GTI rose, FPD green
const COL = { I: 0xe8c060, GSD: 0xc792ea, D1: 0x9fd8ff, SSD: 0xf06292, Ik: 0xe8c060 };
const PIECE_COL = { cap: 0x5fd38a, axe: 0x4dd0e1, cleoR: 0xe1c8f0, stet: 0xffa726 };
const NAMES = { I: 'I', GSD: 'great stellated dodecahedron', D1: 'D1', SSD: 'small stellated dodecahedron', Ik: 'I·φ³' };
const FULL = { I: 'the icosahedron, the core', GSD: 'Kepler\'s great stellated dodecahedron: the core with 20 CLEO spikes, tips at 3× the face distance',
  D1: 'the dodecahedron of edge φ, the great star\'s hull', SSD: 'Kepler\'s small stellated dodecahedron: D1 with 12 spires, tips at √5× the face distance',
  Ik: 'the next icosahedron, φ³ larger: the next turn begins' };
const PIECE_NAMES = { cap: 'cap', axe: 'AXE', cleoR: 'CLEO\'s golden reciprocal', stet: 'valley tetrahedron' };
const PEEL = ['Ik', 'SSD', 'D1', 'GSD'];
const N = PEEL.length;
const PRESET = { pieces: false };
const STEP_SECONDS = 1.6, PAUSE_MS = 900;
const lang = () => getSettings().language;

export function createKpFilmWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {}, openWorld = () => {} }) {
  const STORAGE_KEY = storageKey('kpfilm');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  try { const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'); if (d) restoreView(d); } catch { /* the preset */ }
  function restoreView(d) { if (typeof d.pieces === 'boolean') view.pieces = d.pieces; }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...view })); } catch { /* best-effort */ } };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, wedge = true, pickTargets = [], items = [];
  const load = () => (loading ??= import('./kp-film-data.js').then((m) => { DATA = m.default; }));
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
    mat.userData.hollow = !wedge && !key.startsWith('p:') && !['GSD', 'SSD'].includes(key);
    const mesh = new THREE.Mesh(g, mat); mesh.userData = { kind: 'kpf', key, turn };
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
      // the outer I of a turn is the next turn's core (Ik); the core at 1 is drawn by the turn inside
      for (const S of DATA.stations.I) addSolid(S, COL.Ik, s * DATA.K, 'Ik', turn);
      for (const k of ['SSD', 'D1', 'GSD']) for (const S of DATA.stations[k]) addSolid(S, COL[k], s, k, turn);
      if (view.pieces) for (const k of ['Ik', 'D1']) for (const p of DATA.pieces[k]) addSolid(p, PIECE_COL[p.kind], s, `p:${k}:${p.kind}`, turn, 0.965);
    }
    // the very centre: the innermost turn's core icosahedron, so the core never shows a hole
    const inner = turns[turns.length - 1];
    for (const S of DATA.stations.I) addSolid(S, COL.I, DATA.K ** inner, 'I', inner);
    applyFilm();
  }
  // ---- the film: u runs over the 4 peels of a turn; station PEEL[j] of turn 0 lifts away and fades while u passes j, its shell's pieces
  // with it; the whole scene grows by φ^(3/4) a step, so after 4 the turn inside has become the first
  const film = { on: false, dir: 0, t: 0, pauseUntil: 0, last: 0, raf: 0, lastDir: 1 };
  const modN = (x) => ((x % N) + N) % N;
  const peelIndex = (key) => PEEL.indexOf(key.startsWith('p:') ? key.split(':')[1] : key);
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
    if (!ud || ud.kind !== 'kpf' || !DATA || mode === 'paint') return false;
    if (ud.key.startsWith('p:')) { const kind = ud.key.split(':')[2]; showHudPrompt(t('kpf.prompt.piece', lang(), { piece: PIECE_NAMES[kind] }), 3200); return true; }
    showHudPrompt(`${NAMES[ud.key]} · ${FULL[ud.key]}`, 3200);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldkpfilm-panel'; panel.className = 'qc-panel';
  const player = createInfinityPlayer({
    onDir: (d) => { const first = !film.on; setFilm(d); if (first) showHudPrompt(t('kpf.prompt.film', lang()), 4500); },
    onPause: () => { if (!film.on) return; if (film.dir) setFilm(film.dir); else setFilm(film.lastDir || 1); },
    words: (L) => ({ wrap: t('dv.film.wrap', L), unwrap: t('dv.film.unwrap', L), pause: t('dv.film.pause', L) }),
  });
  panel.innerHTML = `
    <div class="w4d-row st-note upf-note"></div>
    <div class="w4d-row upf-film-row"><label class="hull-pick"><span class="upf-film-pos"></span> <input type="range" class="st-slider" min="0" max="400" step="1"></label></div>
    <div class="w4d-row w4d-options"><button type="button" data-upf="pieces"></button><button type="button" data-upf="up"></button><button type="button" data-upf="reset"></button></div>`;
  panel.insertBefore(player.el, panel.querySelector('.upf-film-row'));
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'kpfilm');
  const slider = panel.querySelector('.upf-film-row input');
  const syncSlider = () => { slider.value = String(Math.round(modN(film.t) * 100)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    if (!DATA) { panel.querySelector('.upf-note').textContent = t('vj.loading', L); return; }
    panel.querySelector('.upf-note').textContent = t('kpf.note', L);
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
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('kpf.prompt.start', lang()), 5500); });
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
