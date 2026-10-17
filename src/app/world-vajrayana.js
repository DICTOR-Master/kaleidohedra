// Vajrayana (DICTO 2026-10-17; paper "Vajrayana", DICTO DOI 10.5281/zenodo.23429911): the twelve-station golden cycle
//   I ⊂ Cleo star ⊂ D′ ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ jtI ⊂ RT ⊂ M ⊂ I·φ³
// one turn, the outer I·φ³ being the next turn's I, the turn inside it drawn too. DICTO's choices: it opens on the cycle cut away (the
// side bar's ⛶ wedge, a quarter facing the camera; ⛶ again gives the X-ray plane, then off, when the shells turn to glass); the ∞ film
// peels one station at a time from the outside, pausing on each, and zooms by φ³ a turn so it runs for ever (Wrap builds back out); a
// Pieces switch fills the two closing steps with their pieces, RT → M (30 of one kind) and M → I·φ³ (60 of one kind); the paper's
// colours. Tapping a shell names its station; the Cleo star build (82 pieces) lives in Theaetetus, one tap away (no crossover).
// The data (scripts/build-vajrayana-data.py) loads on first entry and is let go on leaving. Words: i18n vj.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { createInfinityPlayer } from './infinity-player.js';

const PHI = (1 + Math.sqrt(5)) / 2, PHI3 = PHI ** 3;
const COL = { star: 0x4dd0e1, Dp: 0xf5f0e2, ID: 0xc792ea, O: 0x2bb3a3, rTI: 0xf08fc0, TI: 0x5fd38a, H: 0xe8b84a, hull: 0x9fd8ff, RT: 0xff9a52, M: 0xc0392b, Ip3: 0x4dd0e1 };
const LAYER_COL = { rtM: 0xf4b183, mI: 0xe9c79a };
export const VJ_NAMES = { I: 'I', star: 'Cleo star', Dp: 'D′', ID: 'ID', O: 'O', rTI: 'rTI', TI: 'TI', H: 'H', hull: 'jtI', RT: 'RT', M: 'M', Ip3: 'I·φ³' };
const FULL = { star: 'the Cleo star: the icosahedron as 20 Cleo-Icos with 20 more turned out as spikes', Dp: 'the dodecahedron at two thirds, D′, the hull of the Cleo star',
  ID: 'the icosidodecahedron', O: 'the DICTO Ogdoecontahedron', rTI: 'the rectified truncated icosahedron', TI: 'the truncated icosahedron', H: 'the DICTO Hecatodihedron',
  hull: 'the joined truncated icosahedron (jtI)', RT: 'the rhombic triacontahedron', M: 'the DICTO Metaxyhexecontahedron', Ip3: 'the next icosahedron, I·φ³, the next turn begins' };
// the film peels a turn outside in: 11 stations, then the turn inside has become the first (φ³ larger), so it loops without a seam
const PEEL = ['Ip3', 'M', 'RT', 'hull', 'H', 'TI', 'rTI', 'O', 'ID', 'Dp', 'star'];
const PRESET = { pieces: false };
const STEP_SECONDS = 1.6, PAUSE_MS = 900;
const lang = () => getSettings().language;

export function createVajrayanaWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {}, openWorld = () => {} }) {
  const STORAGE_KEY = storageKey('vajrayana');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  try { const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'); if (d && typeof d.pieces === 'boolean') view.pieces = d.pieces; } catch { /* the preset */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...view })); } catch { /* best-effort */ } };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, wedge = true, pickTargets = [], items = [];
  const load = () => (loading ??= import('./vajrayana-data.js').then((m) => { DATA = m.default; }));
  function clearGroup() { for (const c of [...group.children]) { group.remove(c); c.geometry?.dispose(); c.material?.dispose(); } pickTargets = []; items = []; }
  // the wedge: two planes through the centre a quarter turn apart, facing the camera; a material carries them (userData.wedgePlanes),
  // and render.js applies them while the X-ray plane is off
  let wedgePlanes = null;
  function makeWedge() {
    const v3 = (a) => new THREE.Vector3(...a), dir = v3(DATA.view.dir), up = v3(DATA.view.up);
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
    const mat = new THREE.MeshStandardMaterial({ color: colour, roughness: 0.5, flatShading: true, side: THREE.DoubleSide, transparent: glass, opacity: skeleton ? 0 : glass ? (wedge ? opacity : 0.14) : 1, depthWrite: !glass });
    mat.userData.wedgePlanes = wedge ? wedgePlanes : null; mat.userData.baseOpacity = mat.opacity;
    const mesh = new THREE.Mesh(g, mat); mesh.userData = { kind: 'vj', key, turn };
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
      const s = PHI3 ** turn;
      for (const st of DATA.stations) {
        if (st.key === 'I') continue;   // turn 0's I is the turn inside's I·φ³
        if (st.key === 'star') { for (const sp of DATA.spikes) addSolid(sp, COL.star, s, 'star', turn); continue; }
        addSolid(st, COL[st.key], s, st.key, turn);
      }
      if (view.pieces) { for (const p of DATA.rtM) addSolid(p, LAYER_COL.rtM, s, 'rtM', turn, 0.965); for (const p of DATA.mI) addSolid(p, LAYER_COL.mI, s, 'mI', turn, 0.965); }
    }
    // the very centre (turn -2's I, or -1's when still): a small solid icosahedron, so the core never shows a hole
    addSolid(DATA.stations[0], COL.Ip3, PHI3 ** turns[turns.length - 1], 'I', turns[turns.length - 1]);
    applyFilm();
  }
  // ---- the film: u runs over the 11 peels of a turn; station PEEL[j] of turn 0 lifts away and fades while u passes j, the 30 and 60
  // pieces go with M and I·φ³; the whole scene grows by φ^(3/11) a step, so after 11 the turn inside has become the first
  const film = { on: false, dir: 0, t: 0, pauseUntil: 0, last: 0, raf: 0, lastDir: 1 };
  const mod11 = (x) => ((x % 11) + 11) % 11;
  const peelIndex = (key) => (key === 'mI' ? 0 : key === 'rtM' ? 1 : PEEL.indexOf(key));
  function applyFilm() {
    const u = film.on ? mod11(film.t) : 0;
    group.scale.setScalar(film.on ? PHI3 ** (u / 11) : 1);
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
  function showStation() {
    const key = PEEL[Math.round(mod11(film.t)) % 11];
    showHudPrompt(`${VJ_NAMES[key]} · ${FULL[key]}`, 1600);
  }
  function setFilm(dir) {
    const wasOn = film.on; if (film.dir) film.lastDir = film.dir;
    if (dir === film.dir && film.on) dir = 0;
    film.dir = dir; film.on = film.on || dir !== 0; film.last = 0;
    if (film.on && !wasOn) draw();
    if (!film.raf && film.on) film.raf = requestAnimationFrame(tick);
    renderPanel();
  }
  function stopFilm() { const was = film.on; film.on = false; film.dir = 0; film.t = 0; if (film.raf) cancelAnimationFrame(film.raf); film.raf = 0; group.scale.setScalar(1); if (was) draw(); }
  const fit = () => DATA && fitView([0, 0, 0], 1.05 * 2.49 * WS, DATA.view.dir);

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || ud.kind !== 'vj' || !DATA || mode === 'paint') return false;
    const L = lang();
    if (ud.key === 'rtM' || ud.key === 'mI') { showHudPrompt(t(`vj.prompt.${ud.key}`, L), 3200); return true; }
    if (ud.key === 'I') { showHudPrompt(`I · ${t('vj.prompt.core', L)}`, 2600); return true; }
    showHudPrompt(`${VJ_NAMES[ud.key]} · ${FULL[ud.key]}${ud.key === 'star' ? ` — ${t('vj.prompt.cleoLink', L)}` : ''}`, 3200);
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldvajrayana-panel'; panel.className = 'qc-panel';
  const player = createInfinityPlayer({
    onDir: (d) => { const first = !film.on; setFilm(d); if (first) showHudPrompt(t('vj.prompt.film', lang()), 4500); },
    onPause: () => { if (!film.on) return; if (film.dir) setFilm(film.dir); else setFilm(film.lastDir || 1); },
    words: (L) => ({ wrap: t('dv.film.wrap', L), unwrap: t('dv.film.unwrap', L), pause: t('dv.film.pause', L) }),
  });
  panel.innerHTML = `
    <div class="w4d-row st-note vj-note"></div>
    <div class="w4d-row vj-film-row"><label class="hull-pick"><span class="vj-film-pos"></span> <input type="range" class="st-slider" min="0" max="1100" step="1"></label></div>
    <div class="w4d-row w4d-options vj-opts"><button type="button" data-vj="pieces"></button><button type="button" data-vj="cleo"></button><button type="button" data-vj="reset"></button><button type="button" data-vj="paper"></button></div>`;
  panel.insertBefore(player.el, panel.querySelector('.vj-film-row'));
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'vajrayana');
  const slider = panel.querySelector('.vj-film-row input');
  const syncSlider = () => { slider.value = String(Math.round(mod11(film.t) * 100)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    if (!DATA) { panel.querySelector('.vj-note').textContent = t('vj.loading', L); return; }
    panel.querySelector('.vj-note').textContent = t(view.pieces ? 'vj.note.pieces' : 'vj.note', L);
    player.render(film, L);
    panel.querySelector('.vj-film-row').style.display = film.on && film.dir === 0 ? '' : 'none';
    panel.querySelector('.vj-film-pos').textContent = t('vj.film.position', L);
    const b = (k) => panel.querySelector(`[data-vj="${k}"]`);
    b('pieces').textContent = t(view.pieces ? 'vj.pieces.on' : 'vj.pieces.off', L); b('pieces').classList.toggle('active', view.pieces);
    b('cleo').textContent = t('vj.cleo', L); b('paper').textContent = t('dv.paper', L);
    b('reset').textContent = t('dv.reset', L); b('reset').hidden = view.pieces === PRESET.pieces && !film.on;
  }
  const commit = () => { save(); draw(); renderPanel(); onChange(); window.dispatchEvent(new Event('krp-hud-refresh')); };
  panel.querySelector('[data-vj="pieces"]').addEventListener('click', () => { view.pieces = !view.pieces; commit(); });
  panel.querySelector('[data-vj="cleo"]').addEventListener('click', () => openWorld('tool:theaetetusWorld:cleostar', 'Theaetetus'));
  panel.querySelector('[data-vj="paper"]').addEventListener('click', () => { if (DATA) window.open(`https://doi.org/${DATA.paperDoi}`, '_blank', 'noopener'); });
  panel.querySelector('[data-vj="reset"]').addEventListener('click', () => { Object.assign(view, PRESET); stopFilm(); commit(); fit(); });
  slider.addEventListener('input', () => { if (!film.on) return; film.dir = 0; film.t = Math.floor(film.t / 11) * 11 + Number(slider.value) / 100; applyFilm(); renderPanel(); });
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
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('vj.prompt.start', lang()), 5500); });
    },
    // the side bar's ⛶ (DICTO 2026-10-17): wedge → X-ray plane → off; with the wedge off the shells turn to glass
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
    open(sub) { if (sub === 'pieces') { view.pieces = true; save(); if (active) { draw(); renderPanel(); } } },
    snapshot: () => ({ version: 1, ...view }),
    restore(json) { if (json && typeof json.pieces === 'boolean') view.pieces = json.pieces; save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: an icosahedron with a dodecahedron round it, a member of the hull
 *  family the DICTO Metaxyhexecontahedron belongs to (an outline for the menu only, not M's exact proportions). */
export function vajrayanaPreviewPoints() {
  const P = [];
  for (const a of [-1, 1]) for (const b of [-1, 1]) P.push([0, a, b * PHI], [a, b * PHI, 0], [b * PHI, 0, a]);
  const k = 1.18;
  for (const a of [-1, 1]) for (const b of [-1, 1]) { P.push([0, a / PHI * k, b * PHI * k], [a / PHI * k, b * PHI * k, 0], [b * PHI * k, 0, a / PHI * k]); }
  for (const a of [-1, 1]) for (const b of [-1, 1]) for (const c of [-1, 1]) P.push([a * k, b * k, c * k]);
  return P;
}
