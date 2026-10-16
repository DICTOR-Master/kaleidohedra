// Double Vision (DICTO 2026-10-16; paper "Double Vision – Both Cycles in One Space", DICTO DOI 10.5281/zenodo.23407106): the Spheres of
// Dharma (yours) and their polar reversal (flipped) in one space, as the paper builds them, the first preset of DICTO's nest-and-reverse
// engine. One switch is the paper's toggle, the sphere of reciprocation: Ends shared (ρ² = φ²/4: the cycles share the icosahedron and
// dodecahedron) or Middle shared (ρ² = 3φ²/4: the icosidodecahedron and triacontahedron). Three views follow the paper:
//   cycles     the stations of both cycles as see-through shells (§1–2); the big slider fades from yours to the flipped cycle, both in the middle;
//   interlock  both cycles as one solid (§3, Figure 1): one turn of exact convex pieces, 536 (DICTO Interlock set 1, Dharma-Ends) or 502
//              (set 2, Dharma-Middle), a slice removed and the next turn in at the centre; the slider recolours every piece from its
//              original layer to its flipped layer, so the seams of each cycle show in turn;
//   layer      one original layer alone (Figure 3), with its count in this setting (Table 3).
// The film (Unwrap / Wrap, one switch): the interlock unwraps layer by layer into the next turn and on for ever, or wraps back outwards,
// pausing at every station; tapping the running direction pauses it, a slider scrubs through the turn.
// Tapping a piece names its kind (I1·n / I2·n with its shape code, Tables 1–2) and lights every piece of that kind. X-ray cuts it like
// the paper's Figure 2 (tree rings). The paper's data (scripts/build-double-vision-data.py) loads on first entry; leaving the world
// lets its pieces go, and only the view (setting, view, layer, slider) is kept, with Reset back to the paper's preset. Words: i18n dv.*.
import * as THREE from 'three';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const MODES = ['cycles', 'interlock', 'layer'];
const SETTINGS = ['ends', 'middle'];
// mixCycles: both cycles at the middle; mixColour: the paper's Figure 1 colours (each piece by its original layer)
const PRESET = { setting: 'ends', mode: 'interlock', layer: 0, mixCycles: 0.5, mixColour: 0, slice: true, inner: true };
// the paper's layer colours (original cycle) and a second set for the flipped cycle's layers
const ORIG = [0x4dd0e1, 0xc792ea, 0x5fd38a, 0xf08fc0, 0x9fd8ff, 0xff9a52];
const FLIP = [0xffc857, 0xe85d88, 0x7e57c2, 0x26a69a, 0xf4a261, 0x6fa8ff];
const PALE = 0xe2dbcc, SHARED = 0xffc857;
const SOLID_COLOUR = { I: 0x4dd0e1, ID: 0xc792ea, D: 0x5fd38a, TI: 0xf08fc0, H: 0x9fd8ff, RT: 0xff9a52, O: 0xb98ad8, PD: 0xe85d88 };
const ORIG_LAYERS = ['I → ID', 'ID → D', 'D → TI', 'TI → H', 'H → RT', 'RT → I·φ³'];
const FLIP_LAYERS = ['D → ID', 'ID → O', 'O → PD', 'PD → I', 'I → RT', 'RT → D·φ³'];
const WEDGE = 90; // degrees, the paper's cake slice facing the camera
const lang = () => getSettings().language;
const baseName = (n) => n.replace(/·.*$/, '');

export function createDoubleVisionWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('doublevision');
  const group = new THREE.Group(); group.visible = false; scene.add(group);
  const view = { ...PRESET };
  let kind = null, lastTap = 0; // the tapped kind (index), lit; not saved
  function read(d) {
    if (!d || typeof d !== 'object') return;
    if (SETTINGS.includes(d.setting)) view.setting = d.setting;
    if (MODES.includes(d.mode)) view.mode = d.mode;
    if (Number.isInteger(d.layer) && d.layer >= 0 && d.layer < 6) view.layer = d.layer;
    for (const k of ['mixCycles', 'mixColour']) if (Number.isFinite(d[k])) view[k] = Math.min(1, Math.max(0, d[k]));
    for (const k of ['slice', 'inner']) if (typeof d[k] === 'boolean') view[k] = d[k];
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the preset */ }
  const snapshot = () => ({ version: 1, ...view });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };

  let DATA = null, loading = null, active = false, skeleton = false, opacity = 1, pickTargets = [];
  let layerMeshes = []; // the drawn pieces: one mesh per (turn, layer)
  let shells = []; // cycles view: { mesh, edges, side, shared }
  const load = () => (loading ??= import('./double-vision-data.js').then((m) => { DATA = m.default; }));
  const S = () => DATA.settings[view.setting];

  const pieceMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, metalness: 0.05, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry?.dispose(); if (child.material !== pieceMat) child.material?.dispose(); }
    pickTargets = []; layerMeshes = []; shells = [];
  }
  // The paper's slice: a wedge about the view's vertical, facing the camera; whole pieces dropped, none clipped.
  function wedgeTest() {
    const vw = S().view, wa = new THREE.Vector3(...vw.up).normalize(), d0 = new THREE.Vector3(...vw.dir);
    const wr = d0.clone().sub(wa.clone().multiplyScalar(d0.dot(wa))).normalize(), wr2 = wa.clone().cross(wr);
    return (c) => { const x = c.dot(wr), y = c.dot(wr2); return Math.hypot(x, y) > 1e-9 && Math.abs(Math.atan2(y, x)) < (WEDGE / 2) * Math.PI / 180; };
  }
  const centroid = (V) => V.reduce((a, v) => a.add(new THREE.Vector3(...v)), new THREE.Vector3()).multiplyScalar(1 / V.length);

  // Pieces as one mesh per (turn, original layer), so the film can lift each layer away on its own. Each mesh keeps its pieces (shown) and,
  // per triangle, the piece's index (tri), for colours and taps.
  function drawPieces() {
    const P = S().pieces, inWedge = wedgeTest();
    const turns = film.on ? [0, 1, 2] : view.inner && view.mode === 'interlock' ? [0, 1] : [0];
    for (const turn of turns) {
      const s = Math.pow(PHI, -3 * turn);
      for (let layer = 0; layer < 6; layer++) {
        if (view.mode === 'layer' && layer !== view.layer) continue;
        const shown = [];
        for (const p of P) {
          if (p.o !== layer) continue;
          const c = centroid(p.v);
          if (view.slice && inWedge(c)) continue;
          shown.push({ p, turn, s, c });
        }
        if (!shown.length) continue;
        const pos = [], edges = [], tri = [];
        shown.forEach((e, i) => {
          const V = e.p.v.map((v) => new THREE.Vector3(...v).sub(e.c).multiplyScalar(0.985).add(e.c).multiplyScalar(e.s * WS));
          for (const f of e.p.f) {
            for (let k = 1; k + 1 < f.length; k++) { for (const j of [f[0], f[k], f[k + 1]]) pos.push(V[j].x, V[j].y, V[j].z); tri.push(i); }
            f.forEach((a, k) => { const b = f[(k + 1) % f.length]; edges.push(V[a].x, V[a].y, V[a].z, V[b].x, V[b].y, V[b].z); });
          }
        });
        const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
        g.setAttribute('color', new THREE.Float32BufferAttribute(new Float32Array(pos.length), 3)); g.computeVertexNormals();
        const mat = pieceMat.clone(); mat.userData.base = { transparent: pieceMat.transparent, opacity: pieceMat.opacity, depthWrite: pieceMat.depthWrite };
        const mesh = new THREE.Mesh(g, mat); mesh.userData = { kind: 'pieces', shown, tri, turn, layer };
        const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
        const line = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: skeleton ? 0xd8f0ff : 0x2a2218, transparent: true, opacity: skeleton ? 0.9 : 0.45 }));
        line.userData.baseOpacity = line.material.opacity;
        group.add(mesh, line); pickTargets.push(mesh); layerMeshes.push({ mesh, line, turn, layer });
      }
    }
    recolour(); applyFilm();
  }
  // Colours: each piece from its original layer's colour to its flipped layer's, by the slider; a tapped kind lit, the rest pale.
  function recolour() {
    const a = new THREE.Color(), b = new THREE.Color();
    for (const { mesh } of layerMeshes) {
      const col = mesh.geometry.attributes.color, { shown, tri } = mesh.userData;
      for (let t = 0; t < tri.length; t++) {
        const e = shown[tri[t]];
        if (kind !== null && e.p.k !== kind) a.setHex(PALE);
        else { a.setHex(ORIG[e.p.o]).lerp(b.setHex(FLIP[e.p.r]), view.mixColour); if (e.turn && !film.on) a.lerp(b.setHex(0xffffff), 0.25); }
        for (let k = 0; k < 3; k++) col.setXYZ(t * 3 + k, a.r, a.g, a.b);
      }
      col.needsUpdate = true;
    }
  }
  // ---- the film (DICTO 2026-10-16: "a movie: unwrap forwards or backwards at the flick of one toggle", "infinity backwards and forwards,
  // pausing on the way"). Film time u runs over the 6 layers of a turn, outermost first; layer j of the outer turn lifts away and fades while
  // u passes 5 - j, and the whole scene grows by φ^(1/2) per layer, so after 6 layers the next turn (φ³ smaller) has become the first: the
  // film loops without a seam, unwrapping inwards for ever, or wrapping outwards for ever when run backwards. It pauses at every station.
  const film = { on: false, dir: 0, t: 0, pauseUntil: 0, last: 0, raf: 0 };
  const LAYER_SECONDS = 1.7, PAUSE_MS = 900;
  const mod6 = (x) => ((x % 6) + 6) % 6;
  function applyFilm() {
    const u = film.on ? mod6(film.t) : 0;
    group.scale.setScalar(film.on ? Math.pow(PHI, u / 2) : 1);
    for (const { mesh, line, turn, layer } of layerMeshes) {
      const prog = film.on && turn === 0 ? Math.min(1, Math.max(0, u - (5 - layer))) : 0;
      const k = 1 + 0.55 * prog * prog;                                    // lift outward
      mesh.scale.setScalar(k); line.scale.setScalar(k);
      const o = 1 - prog, base = mesh.material.userData.base;
      mesh.visible = line.visible = o > 0.01;
      mesh.material.transparent = base.transparent || o < 1; mesh.material.opacity = base.opacity * o; mesh.material.depthWrite = base.depthWrite && o >= 1;
      line.material.opacity = line.userData.baseOpacity * o;
    }
  }
  function tick(now) {
    film.raf = 0;
    if (!active || !film.on) return;
    const dt = film.last ? Math.min(0.1, (now - film.last) / 1000) : 0; film.last = now;
    if (film.dir && now >= film.pauseUntil) {
      const before = film.t; film.t += film.dir * dt / LAYER_SECONDS;
      // a station crossed (in the direction of travel): stop on it and pause
      const crossed = film.dir > 0 ? Math.floor(film.t) > Math.floor(before) : Math.ceil(film.t) < Math.ceil(before);
      if (crossed) { film.t = film.dir > 0 ? Math.floor(film.t) : Math.ceil(film.t); film.pauseUntil = now + PAUSE_MS; }
      applyFilm(); syncFilmSlider();
    }
    film.raf = requestAnimationFrame(tick);
  }
  function setFilm(dir) {
    const wasOn = film.on;
    if (dir === film.dir && film.on) dir = 0;                               // tapping the running direction pauses
    film.dir = dir; film.on = film.on || dir !== 0; film.last = 0;
    if (film.on && !wasOn) { if (view.mode !== 'interlock') view.mode = 'interlock'; draw(); }
    if (!film.raf && film.on) film.raf = requestAnimationFrame(tick);
    renderPanel();
  }
  function stopFilm() { film.on = false; film.dir = 0; film.t = 0; if (film.raf) cancelAnimationFrame(film.raf); film.raf = 0; group.scale.setScalar(1); }
  function drawCycles() {
    for (const st of S().stations) {
      const V = st.v.map((v) => new THREE.Vector3(...v).multiplyScalar(WS)), pos = [], edges = [];
      for (const f of st.f) {
        for (let k = 1; k + 1 < f.length; k++) for (const j of [f[0], f[k], f[k + 1]]) pos.push(V[j].x, V[j].y, V[j].z);
        f.forEach((a, k) => { const b = f[(k + 1) % f.length]; edges.push(V[a].x, V[a].y, V[a].z, V[b].x, V[b].y, V[b].z); });
      }
      const colour = st.shared ? SHARED : SOLID_COLOUR[baseName(st.name)] ?? 0xcccccc;
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
      const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: colour, roughness: 0.4, transparent: true, depthWrite: false, side: THREE.DoubleSide }));
      mesh.userData = { kind: 'shell', st };
      const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
      const line = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: colour, transparent: true }));
      group.add(mesh, line); pickTargets.push(mesh); shells.push({ mesh, line, st });
    }
    fade();
  }
  // Cycles view: yours fades out as the flipped cycle fades in; the shared solids belong to both and stay.
  function fade() {
    for (const { mesh, line, st } of shells) {
      const w = st.shared ? 1 : st.side === 'orig' ? Math.min(1, 2 * (1 - view.mixCycles)) : Math.min(1, 2 * view.mixCycles);
      mesh.material.opacity = (skeleton ? 0 : 0.13) * w * (opacity < 1 ? 0.6 : 1); line.material.opacity = 0.95 * w;
      mesh.visible = line.visible = w > 0.01;
    }
  }
  function draw() {
    clearGroup();
    if (!active || !DATA) return;
    pieceMat.transparent = opacity < 1 || skeleton; pieceMat.opacity = skeleton ? 0 : opacity; pieceMat.depthWrite = opacity >= 1 && !skeleton; pieceMat.needsUpdate = true;
    if (view.mode === 'cycles') drawCycles(); else drawPieces();
  }
  // framed from the paper's view B, so the slice faces you
const fit = () => DATA && fitView([0, 0, 0], (view.mode === 'cycles' ? 2.0 : 1.35) * 2.49 * WS, S().view.dir);

  function handleTap(hit, mode) {
    const ud = hit.object?.userData;
    if (!ud || !DATA || mode === 'paint') return false;
    const L = lang();
    if (ud.kind === 'shell') {
      const st = ud.st;
      showHudPrompt(t(st.shared ? 'dv.prompt.shared' : `dv.prompt.${st.side}`, L, { name: st.name }), 2600);
      return true;
    }
    if (ud.kind !== 'pieces') return false;
    const e = ud.shown[ud.tri[Math.floor(hit.faceIndex ?? -1)]];
    if (!e) return false;
    // a second tap on the lit kind shows all again (taps closer than 0.7 s are one tap)
    const now = performance.now();
    if (now - lastTap < 700 && kind === e.p.k) return true;
    lastTap = now;
    kind = kind === e.p.k ? null : e.p.k;
    recolour(); renderPanel();
    if (kind !== null) {
      const k = S().kinds[e.p.k];
      showHudPrompt(t('dv.prompt.piece', L, { name: k.name, code: k.code, n: k.n, o: ORIG_LAYERS[e.p.o], r: FLIP_LAYERS[e.p.r] }), 5000);
    }
    return true;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worlddoublevision-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row st-note dv-note"></div>
    <div class="w4d-row w4d-options dv-top">${SETTINGS.map((x) => `<button type="button" data-dv-setting="${x}"></button>`).join('')}<span class="dv-gap"></span>${['unwrap', 'wrap'].map((d) => `<button type="button" data-dv-film="${d}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options dv-modes">${MODES.map((m) => `<button type="button" data-dv-mode="${m}"></button>`).join('')}<span class="dv-gap"></span><button type="button" data-dv="slice"></button><button type="button" data-dv="inner"></button><button type="button" data-dv="reset"></button><button type="button" class="dv-paper"></button></div>
    <div class="w4d-row w4d-options dv-layers">${ORIG_LAYERS.map((n, i) => `<button type="button" data-dv-layer="${i}">${n}</button>`).join('')}</div>
    <div class="w4d-row dv-film-row"><label class="hull-pick"><span class="dv-film-pos"></span> <input type="range" class="st-slider" min="0" max="600" step="1"></label></div>
    <div class="w4d-row dv-mix-row"><label class="hull-pick"><span class="dv-mix-label"></span> <input type="range" class="st-slider" min="0" max="100" step="1"></label></div>
    <style>#worlddoublevision-panel .dv-gap{display:inline-block;width:14px}#worlddoublevision-panel .dv-note{max-width:62ch;margin:0 auto}</style>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'doublevision');
  const slider = panel.querySelector('.dv-mix-row input'), filmSlider = panel.querySelector('.dv-film-row input');
  const syncFilmSlider = () => { filmSlider.value = String(Math.round(mod6(film.t) * 100)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), m = view.mode;
    if (!DATA) { panel.querySelector('.dv-note').textContent = t('dv.loading', L); return; }
    const s = S(), setNo = view.setting === 'ends' ? 1 : 2;
    const vars = { shared: t(`dv.shared.${view.setting}`, L), n: s.pieces.length, k: s.kinds.length, set: setNo,
      setName: `DICTO Interlock set ${setNo} (${view.setting === 'ends' ? 'Dharma-Ends' : 'Dharma-Middle'})`,
      layer: ORIG_LAYERS[view.layer], ln: s.pieces.filter((p) => p.o === view.layer).length };
    panel.querySelector('.dv-note').textContent = t(`dv.short.${m}`, L, vars);
    panel.querySelectorAll('[data-dv-setting]').forEach((b) => { b.textContent = t(`dv.set.${b.dataset.dvSetting}`, L); b.classList.toggle('active', b.dataset.dvSetting === view.setting); });
    panel.querySelectorAll('[data-dv-mode]').forEach((b) => { b.textContent = t(`dv.mode.${b.dataset.dvMode}`, L); b.classList.toggle('active', b.dataset.dvMode === m); });
    panel.querySelectorAll('[data-dv-film]').forEach((b) => { const d = b.dataset.dvFilm === 'unwrap' ? 1 : -1; b.textContent = t(`dv.film.${b.dataset.dvFilm}`, L); b.classList.toggle('active', film.on && film.dir === d); });
    panel.querySelector('.dv-film-row').hidden = !film.on; panel.querySelector('.dv-mix-row').hidden = film.on; panel.querySelector('.dv-film-pos').textContent = t('dv.film.position', L); syncFilmSlider();
    panel.querySelector('.dv-layers').hidden = m !== 'layer';
    panel.querySelectorAll('[data-dv-layer]').forEach((b) => b.classList.toggle('active', Number(b.dataset.dvLayer) === view.layer));
    const tog = (k, on) => { const b = panel.querySelector(`[data-dv="${k}"]`); b.hidden = !on; if (on) b.textContent = t(`dv.${k}.${view[k] ? 'on' : 'off'}`, L); };
    tog('slice', m !== 'cycles'); tog('inner', m === 'interlock');
    const reset = panel.querySelector('[data-dv="reset"]');
    reset.hidden = Object.keys(PRESET).every((k) => view[k] === PRESET[k]); reset.textContent = t('dv.reset', L);
    panel.querySelector('.dv-paper').textContent = t('dv.paper', L);
    slider.value = String(Math.round((m === 'cycles' ? view.mixCycles : view.mixColour) * 100));
    panel.querySelector('.dv-mix-label').textContent = t(m === 'cycles' ? 'dv.mix.cycles' : 'dv.mix.colour', L);
  }
  const commit = (refit = false) => { save(); draw(); renderPanel(); onChange(); if (refit) fit(); };
  panel.querySelectorAll('[data-dv-setting]').forEach((b) => b.addEventListener('click', () => {
    if (view.setting === b.dataset.dvSetting) return;
    view.setting = b.dataset.dvSetting; kind = null; commit(true);
    showHudPrompt(t(`dv.prompt.toggle.${view.setting}`, lang()), 4500);
  }));
  panel.querySelectorAll('[data-dv-mode]').forEach((b) => b.addEventListener('click', () => { view.mode = b.dataset.dvMode; kind = null; if (view.mode !== 'interlock') stopFilm(); commit(true); }));
  panel.querySelectorAll('[data-dv-film]').forEach((b) => b.addEventListener('click', () => {
    const first = !film.on; setFilm(b.dataset.dvFilm === 'unwrap' ? 1 : -1);
    if (first) showHudPrompt(t('dv.prompt.film', lang()), 5000);
  }));
  filmSlider.addEventListener('input', () => { if (!film.on) return; film.dir = 0; film.t = Math.floor(film.t / 6) * 6 + Number(filmSlider.value) / 100; applyFilm(); renderPanel(); });
  panel.querySelectorAll('[data-dv-layer]').forEach((b) => b.addEventListener('click', () => { view.layer = Number(b.dataset.dvLayer); kind = null; commit(); }));
  for (const k of ['slice', 'inner']) panel.querySelector(`[data-dv="${k}"]`).addEventListener('click', () => { view[k] = !view[k]; commit(); });
  panel.querySelector('.dv-paper').addEventListener('click', () => { if (DATA) window.open(`https://doi.org/${DATA.paperDoi}`, '_blank', 'noopener'); });
  panel.querySelector('[data-dv="reset"]').addEventListener('click', () => { Object.assign(view, PRESET); kind = null; stopFilm(); commit(true); });
  slider.addEventListener('input', () => { view[view.mode === 'cycles' ? 'mixCycles' : 'mixColour'] = Number(slider.value) / 100; save(); if (view.mode === 'cycles') fade(); else recolour(); });
  slider.addEventListener('change', () => { renderPanel(); onChange(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on; group.visible = on; kind = null;
      if (!on) { stopFilm(); clearGroup(); DATA = null; loading = null; renderPanel(); return; } // leaving lets the pieces and the data go
      renderPanel();
      load().then(() => { if (!active) return; draw(); renderPanel(); fit(); showHudPrompt(t('dv.prompt.start', lang()), 5500); });
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return false; },
    clear() { Object.assign(view, PRESET); kind = null; commit(active); },
    resetView() {},
    open(sub) { if (SETTINGS.includes(sub)) view.setting = sub; else if (MODES.includes(sub)) view.mode = sub; else return; save(); if (active) { draw(); renderPanel(); fit(); } },
    snapshot,
    restore(json) { read(json); save(); draw(); renderPanel(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: an icosahedron inside a dodecahedron, the shared pair of the ends setting. */
export function doubleVisionPreviewPoints() {
  const ico = [], dod = [];
  for (const a of [-1, 1]) for (const b of [-1, 1]) { ico.push([0, a, b * PHI], [a, b * PHI, 0], [b * PHI, 0, a]); dod.push([0, a / PHI, b * PHI], [a / PHI, b * PHI, 0], [b * PHI, 0, a / PHI]); }
  for (const a of [-1, 1]) for (const b of [-1, 1]) for (const c of [-1, 1]) dod.push([a, b, c]);
  return [...ico.map((v) => v.map((x) => x * 0.8)), ...dod];
}
