// The HexOct kit (DICTO 2026-11-01, approved spec): Polyhedraverse's kit of paper #75's two layer tiles, the c-tile (gold) and the
// h-tile (blue), placed one at a time (DICTO DOI 10.5281/zenodo.23737639). The tiles snap onto the tiles already placed: a tap on a
// tile puts the chosen tile on the empty place on that side, in the same layer or the layer above or below; long-press (Remove)
// takes one away. Each layer takes one kind of tile (a layer's tile is fixed by the layers below and above it), so the kit keeps
// the letters A/B/C of its layers as they are laid: a new layer's tile sets the letter beyond it (h: the same as across the
// tile, c: the third). A fill helper (3C, 2H, 4H, 6H, Fibonacci or the viewer's own c/h sequence) lays out the K demo's crystal
// (world-hexoct.js: 3 × 3 tiles a layer) as a plan and shows the next tile as see-through coloured glass of its kind; a tap on the
// glass places it, so the viewer builds that stacking by hand, tile by tile (as PV's kits: taps go to the outline while it shows).
// Free (no helper) builds with the tile picked on the panel. Drawn to the render standard: solid faces with polygon offset, crisp
// screen-space edges ≥ 1.5 px; the ghost transparent in its tile's colour. Geometry: hexoct-geometry.js (λ = 1/10).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { HEXOCT_FILLS, parseTypes, lettersOf, thirdLetter, hexoctBall, hexoctTileAt } from './hexoct-geometry.js';
import { HEXOCT_COLOURS, hexoctLayers } from './world-hexoct.js';

export const HEXKIT_FILLS = ['free', ...HEXOCT_FILLS, 'own'];
const EDGE = 0x0b1220, GHOST = 0.32, COLS = 3, ROWS = 3;
const lang = () => getSettings().language;
const keyOf = (k, i, j) => `${k},${i},${j}`;
// the six neighbours of a ball in its layer
const IN_LAYER = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1]];

// ---- the build (pure; the unit tests use these) ----
/** An empty build: no tiles, layer 0 on A and layer 1 on B (as lettersOf). */
export const emptyBuild = () => ({ tiles: new Map(), letters: new Map([[0, 'A'], [1, 'B']]) });
const layersOf = (b) => [...new Set([...b.tiles.values()].map((x) => x.k))].sort((x, y) => x - y);
/** The kind of tile layer k holds ('c', 'h'), or null while it is empty. */
export function layerType(b, k) {
  for (const x of b.tiles.values()) if (x.k === k) return x.type;
  return null;
}
/** Whether tile { k, i, j, type } can go into the build: its place empty, its layer of its kind, a new layer next to the others. */
export function canPlace(b, { k, i, j, type }) {
  if (b.tiles.has(keyOf(k, i, j)) || (type !== 'c' && type !== 'h')) return false;
  if (!b.tiles.size) return k === 0;
  const lt = layerType(b, k);
  if (lt) return lt === type;
  const L = layersOf(b);
  return k === L[0] - 1 || k === L.at(-1) + 1;
}
/** Places a tile (false when it cannot go there). A new layer sets the letter beyond it: h the same as across it, c the third. */
export function placeTile(b, tile) {
  if (!canPlace(b, tile)) return false;
  const { k, type } = tile, L = b.letters;
  if (!b.tiles.size) { L.clear(); L.set(0, 'A'); L.set(1, 'B'); }
  if (!layerType(b, k)) {
    const top = b.tiles.size && k > layersOf(b).at(-1);
    if (top) L.set(k + 1, type === 'h' ? L.get(k - 1) : thirdLetter(L.get(k - 1), L.get(k)));
    else L.set(k - 1, type === 'h' ? L.get(k + 1) : thirdLetter(L.get(k), L.get(k + 1)));
  }
  b.tiles.set(keyOf(k, tile.i, tile.j), { k, i: tile.i, j: tile.j, type });
  return true;
}
/** Takes a tile away; refused (false) when it would leave an empty layer between others. */
export function removeTile(b, key) {
  const x = b.tiles.get(key);
  if (!x) return false;
  const L = layersOf(b), alone = [...b.tiles.values()].filter((y) => y.k === x.k).length === 1;
  if (alone && x.k !== L[0] && x.k !== L.at(-1)) return false;
  b.tiles.delete(key);
  if (!b.tiles.size) { b.letters.clear(); b.letters.set(0, 'A'); b.letters.set(1, 'B'); }
  return true;
}
/** A tile's four pieces where the build puts it (study frame, z up). */
export const tilePieces = (b, { k, i, j, type }) => hexoctTileAt(type, b.letters.get(k - 1), b.letters.get(k), b.letters.get(k + 1), i, j, k);

/** A fill helper's plan: the K demo's crystal, layer by layer bottom up, each layer's 3 × 3 tiles row by row. */
export function kitPlan(types) {
  const out = [];
  for (let k = 0; k < types.length; k++) for (let j = 0; j < ROWS; j++) for (let i = 0; i < COLS; i++) out.push({ k, i, j, type: types[k] });
  return out;
}
/** The helper's next tile for the c/h sequence `types`: { tile } (its first tile not yet built), { done }, or { conflict: k } when
 *  the build's layer k is not the plan's (another kind, or other letters), so the plan cannot be followed from here. */
export function nextPlanTile(b, types) {
  const want = lettersOf(types);   // want[k + 1] is layer k's letter
  for (const k of layersOf(b)) {
    if (k < 0 || k >= types.length) continue;
    if (layerType(b, k) !== types[k] || [-1, 0, 1].some((d) => b.letters.get(k + d) !== want[k + d + 1])) return { conflict: k };
  }
  const tile = kitPlan(types).find((x) => !b.tiles.has(keyOf(x.k, x.i, x.j)));
  if (!tile) return { done: true };
  return canPlace(b, tile) ? { tile } : { conflict: tile.k };
}
/** Free building: the empty place next to tile `from` on the side of `dir` (a direction from its ball, study frame) that takes a
 *  tile of `type`; null when none does. Places: the six beside it in its layer, the three above and the three below. */
export function freeTarget(b, from, dir, type) {
  const at = hexoctBall(b.letters.get(from.k), from.i, from.j, from.k), out = [];
  for (const [di, dj] of IN_LAYER) out.push({ k: from.k, i: from.i + di, j: from.j + dj, type });
  for (const d of [-1, 1]) {
    const letter = b.letters.get(from.k + d);
    if (!letter) continue;
    for (let i = from.i - 2; i <= from.i + 2; i++) for (let j = from.j - 2; j <= from.j + 2; j++) {
      const p = hexoctBall(letter, i, j, from.k + d);
      if (Math.abs(Math.hypot(p[0] - at[0], p[1] - at[1]) - 1 / Math.sqrt(3)) < 1e-6) out.push({ k: from.k + d, i, j, type });
    }
  }
  let best = null, score = -Infinity;
  const n = Math.hypot(...dir) || 1;
  for (const c of out) {
    if (!canPlace(b, c)) continue;
    const p = hexoctBall(b.letters.get(c.k), c.i, c.j, c.k), v = p.map((x, q) => x - at[q]);
    const s = (v[0] * dir[0] + v[1] * dir[1] + v[2] * dir[2]) / (Math.hypot(...v) * n);
    if (s > score) { score = s; best = c; }
  }
  return best;
}
const snapshotOf = (b) => ({ tiles: [...b.tiles.values()].map((x) => [x.k, x.i, x.j, x.type]), letters: [...b.letters.entries()] });
/** A tile's pieces as they would be once placed (a new layer's letter beyond it set as placing it would): the ghost's shape. */
export function previewPieces(b, tile) {
  const c = { tiles: new Map(b.tiles), letters: new Map(b.letters) };
  return placeTile(c, tile) ? tilePieces(c, tile) : [];
}
/** A build from its snapshot: the tiles and letters as saved when they agree (every layer one kind, its letters known, no empty
 *  layer between), else the tiles placed again from layer 0 out; an empty build when neither works. */
export function buildFrom(snap) {
  const list = (Array.isArray(snap?.tiles) ? snap.tiles : []).filter((x) => Array.isArray(x) && x.length === 4 && x.slice(0, 3).every(Number.isInteger) && (x[3] === 'c' || x[3] === 'h'))
    .map(([k, i, j, type]) => ({ k, i, j, type }));
  const letters = new Map((Array.isArray(snap?.letters) ? snap.letters : []).filter((e) => Array.isArray(e) && Number.isInteger(e[0]) && /^[ABC]$/.test(e[1])));
  const ks = [...new Set(list.map((x) => x.k))].sort((x, y) => x - y);
  const kinds = new Map(list.map((x) => [x.k, x.type]));
  const ok = ks.length && ks.every((k, n) => (n === 0 || k === ks[n - 1] + 1) && list.every((x) => x.k !== k || x.type === kinds.get(k)) && [-1, 0, 1].every((d) => letters.has(k + d))
    && letters.get(k - 1) !== letters.get(k) && letters.get(k + 1) !== letters.get(k) && (letters.get(k - 1) === letters.get(k + 1)) === (kinds.get(k) === 'h'));
  if (ok) return { tiles: new Map(list.map((x) => [keyOf(x.k, x.i, x.j), x])), letters };
  const b = emptyBuild();
  if (!ks.includes(0)) return b;
  for (const k of [...ks].sort((x, y) => Math.abs(x) - Math.abs(y) || y - x)) for (const x of list.filter((y) => y.k === k)) placeTile(b, x);
  return b;
}

// study frame (z up) to the app's (y up), as world-hexoct.js
const toApp = (v) => [v[0] * WS, v[2] * WS, -v[1] * WS];
const toStudy = (p) => [p.x / WS, -p.z / WS, p.y / WS];

export function createHexoctKitWorld({ scene, fitView = () => {}, showHudPrompt = () => {}, onChange = () => {} }) {
  const STORAGE_KEY = storageKey('hexoct-kit');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const view = { fill: 'free', own: 'cchch', piece: 'c' };
  let build = emptyBuild();
  function read(d) {
    if (HEXKIT_FILLS.includes(d?.fill)) view.fill = d.fill;
    if (parseTypes(d?.own)) view.own = parseTypes(d.own);
    if (d?.piece === 'c' || d?.piece === 'h') view.piece = d.piece;
    build = buildFrom(d);
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: an empty kit */ }
  const snapshot = () => ({ version: 1, fill: view.fill, own: view.own, piece: view.piece, ...snapshotOf(build) });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, pickTargets = [], ghostMesh = null, ghostTile = null, helper = null, lastPlaced = null;

  const solidMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5, metalness: 0.1 });
  const ghostMat = new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: GHOST, depthWrite: false, roughness: 0.4 });
  ghostMat.userData.hollow = true;   // the ghost stays hollow in an X-ray cut (xray-caps.js)
  const lineMats = [];
  function clear() {
    for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); }
    lineMats.splice(0).forEach((m) => m.dispose());
    pickTargets = []; ghostMesh = null;
  }
  const types = () => (view.fill === 'free' ? null : hexoctLayers(view.fill, view.own));
  // the tile the ghost shows: the helper's next, or (free, nothing built) the picked tile where the first one goes
  function ghostFor() {
    helper = types() ? nextPlanTile(build, types()) : null;
    if (helper) return helper.tile ?? null;
    return build.tiles.size ? null : { k: 0, i: 0, j: 0, type: view.piece };
  }
  function lines(edges, colour, width, colours = null) {
    const lg = new LineSegmentsGeometry();
    lg.setPositions(edges);
    if (colours) lg.setColors(colours);
    const lm = new LineMaterial({ color: colour, linewidth: width, vertexColors: !!colours });
    lineMats.push(lm);
    const l = new LineSegments2(lg, lm);
    l.frustumCulled = false;
    group.add(l);
  }
  function draw() {
    clear();
    if (!active) return;
    const pos = [], col = [], rec = [], edges = [], colour = new THREE.Color();
    for (const [key, x] of build.tiles) {
      colour.setHex(HEXOCT_COLOURS[x.type]);
      for (const p of tilePieces(build, x)) {
        const P = p.vertices.map(toApp);
        for (const f of p.faces) {
          for (let i = 1; i + 1 < f.length; i++) { for (const q of [f[0], f[i], f[i + 1]]) { pos.push(...P[q]); col.push(colour.r, colour.g, colour.b); } rec.push(key); }
          f.forEach((a, i) => edges.push(...P[a], ...P[f[(i + 1) % f.length]]));
        }
      }
    }
    if (pos.length) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
      g.computeVertexNormals();
      solidMat.transparent = opacity < 1; solidMat.opacity = opacity; solidMat.depthWrite = opacity >= 1; solidMat.needsUpdate = true;
      const mesh = new THREE.Mesh(g, solidMat);
      mesh.userData.records = rec;
      mesh.visible = !skeleton;
      group.add(mesh);
      pickTargets.push(mesh);
      lines(edges, skeleton ? 0xcfe3ff : EDGE, 1.6);
    }
    ghostTile = ghostFor();
    if (ghostTile) {
      const gp = [], ge = [];
      for (const p of previewPieces(build, ghostTile)) {
        const P = p.vertices.map(toApp);
        for (const f of p.faces) {
          for (let i = 1; i + 1 < f.length; i++) for (const q of [f[0], f[i], f[i + 1]]) gp.push(...P[q]);
          f.forEach((a, i) => ge.push(...P[a], ...P[f[(i + 1) % f.length]]));
        }
      }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(gp, 3));
      g.computeVertexNormals();
      ghostMat.color.setHex(HEXOCT_COLOURS[ghostTile.type]);
      ghostMesh = new THREE.Mesh(g, ghostMat);
      ghostMesh.userData.ghost = true;
      group.add(ghostMesh);
      lines(ge, HEXOCT_COLOURS[ghostTile.type], 2);
    }
    renderPanel();
  }
  // the camera on the build and the ghost, or on the whole plan while a helper shows; as the build grows it stays in view (the
  // camera only backs off, keeping its turn)
  function fit(exact = true) {
    const pts = [];
    const add = (x) => { const p = hexoctBall(build.letters.get(x.k) ?? 'A', x.i, x.j, x.k); pts.push(p); };
    build.tiles.forEach(add);
    if (ghostTile) add(ghostTile);
    if (types()) for (const x of kitPlan(types())) pts.push(hexoctBall(lettersOf(types())[x.k + 1], x.i, x.j, x.k));
    if (!pts.length) pts.push([0, 0, 0]);
    const lo = [0, 1, 2].map((c) => Math.min(...pts.map((p) => p[c]))), hi = [0, 1, 2].map((c) => Math.max(...pts.map((p) => p[c])));
    const mid = lo.map((x, c) => (x + hi[c]) / 2), r = Math.hypot(...hi.map((x, c) => x - lo[c])) / 2 + 1;
    fitView(toApp(mid), r * WS * 0.8, exact ? [1, 0.32, 1.25] : null, exact);
  }
  function commit() { save(); draw(); onChange(); }
  function place(tile) {
    const first = !build.tiles.size;
    if (!placeTile(build, tile)) return false;
    lastPlaced = { ...tile };
    commit();
    fit(first);
    return true;
  }

  function handleTap(hit, mode) {
    if (mode === 'paint') return false;
    if (hit.object === ghostMesh) return mode === 'chisel' ? false : place({ ...ghostTile });
    const key = hit.object.userData.records?.[Math.floor(hit.faceIndex ?? -1)];
    const from = key && build.tiles.get(key);
    if (!from) return false;
    if (mode === 'chisel') {
      if (!removeTile(build, key)) { showHudPrompt(t('hexkit.prompt.gap', lang()), 2500); return true; }
      commit();
      return true;
    }
    const dir = toStudy(group.worldToLocal(hit.point.clone())).map((x, c) => x - hexoctBall(build.letters.get(from.k), from.i, from.j, from.k)[c]);
    const to = freeTarget(build, from, dir, view.piece);
    if (!to) { showHudPrompt(t('hexkit.prompt.layer', lang(), { tile: t(`hexkit.piece.${layerType(build, from.k)}`, lang()) }), 2500); return true; }
    return place(to);
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldhexoctkit-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options hk-fills">${HEXKIT_FILLS.map((k) => `<button type="button" data-hk-fill="${k}"></button>`).join('')}</div>
    <div class="w4d-row hx-own-row hk-own-row"><input type="text" class="hx-own hk-own" maxlength="40" autocomplete="off" autocapitalize="none" spellcheck="false" enterkeyhint="go"><button type="button" data-hk-own-go></button></div>
    <div class="w4d-row w4d-options"><span class="hk-pieces"><button type="button" data-hk-piece="c"></button><button type="button" data-hk-piece="h"></button></span><button type="button" data-hk-clear></button></div>
    <div class="w4d-row ch-param-caption hk-caption" aria-live="polite"></div>
    <div class="w4d-row st-note hk-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'hexoctKit');
  const ownInput = panel.querySelector('.hk-own'), ownRow = panel.querySelector('.hk-own-row');
  let typing = false;
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang(), T = types();
    panel.querySelectorAll('[data-hk-fill]').forEach((b) => {
      const k = b.dataset.hkFill;
      b.textContent = k === 'free' ? t('hexkit.fill.free', L) : t(`hexoct.kind.${k}`, L);
      b.classList.toggle('active', k === view.fill); b.setAttribute('aria-pressed', String(k === view.fill));
    });
    // the field only for the viewer's own sequence; the tile buttons only when building freely (nothing unnecessary shown)
    ownRow.style.display = view.fill === 'own' ? '' : 'none';
    ownInput.placeholder = t('hexoct.own.placeholder', L);
    ownInput.setAttribute('aria-label', t('hexoct.own.label', L));
    if (!typing) ownInput.value = view.own;
    panel.querySelector('[data-hk-own-go]').textContent = t('hexkit.own.go', L);
    panel.querySelector('.hk-pieces').style.display = T ? 'none' : '';
    panel.querySelectorAll('[data-hk-piece]').forEach((b) => {
      const p = b.dataset.hkPiece;
      b.textContent = t(`hexkit.piece.${p}`, L);
      b.classList.toggle('active', p === view.piece); b.setAttribute('aria-pressed', String(p === view.piece));
    });
    const clearBtn = panel.querySelector('[data-hk-clear]');
    clearBtn.textContent = t('hexkit.clear', L);
    clearBtn.style.display = build.tiles.size ? '' : 'none';
    const n = build.tiles.size, c = [...build.tiles.values()].filter((x) => x.type === 'c').length;
    const counts = t('hexkit.count', L, { n, c, h: n - c });
    let cap;
    if (!T) cap = counts;
    else if (helper?.conflict !== undefined) cap = t('hexkit.conflict', L, { fill: t(`hexoct.kind.${view.fill}`, L), layer: helper.conflict + 1 });
    else if (helper?.done) cap = t('hexkit.done', L, { types: [...T].join(' '), n });
    else cap = t('hexkit.next', L, { tile: t(`hexkit.piece.${helper.tile.type}`, L), layer: helper.tile.k + 1, layers: T.length, types: [...T].join(' '), n, all: T.length * COLS * ROWS });
    panel.querySelector('.hk-caption').textContent = cap;
    panel.querySelector('.hk-note').textContent = t(T ? 'hexkit.note.helper' : 'hexkit.note.free', L);
  }
  function setFill(k) {
    if (!HEXKIT_FILLS.includes(k)) return false;
    view.fill = k; typing = false; save(); draw(); fit();
    return true;
  }
  panel.querySelector('.hk-fills').addEventListener('click', (e) => { const k = e.target.closest('[data-hk-fill]')?.dataset.hkFill; if (k && k !== view.fill) setFill(k); });
  function useOwn() {
    const s = parseTypes(ownInput.value);
    if (!s) { panel.querySelector('.hk-note').textContent = t('hexoct.own.bad', lang()); ownInput.focus(); return; }
    view.own = s; ownInput.blur(); typing = false; save(); draw(); fit();
  }
  ownInput.addEventListener('input', () => { typing = true; });
  ownInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); useOwn(); } });
  panel.querySelector('[data-hk-own-go]').addEventListener('click', useOwn);
  panel.querySelectorAll('[data-hk-piece]').forEach((b) => b.addEventListener('click', () => { view.piece = b.dataset.hkPiece; save(); draw(); }));
  panel.querySelector('[data-hk-clear]').addEventListener('click', () => { build = emptyBuild(); commit(); fit(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    // while the helper shows the next tile, taps go to it (through the tiles in front), as PV's kit outlines
    meshes: () => (types() && ghostMesh ? [ghostMesh] : ghostMesh ? [...pickTargets, ghostMesh] : pickTargets),
    handleTap,
    /** tool:hexoctKit:<free|3C|2H|4H|6H|fib|c/h sequence>: the helper (a c/h sequence as the viewer's own). */
    setChain(kind) {
      const k = HEXKIT_FILLS.find((x) => x.toLowerCase() === String(kind).toLowerCase());
      if (k && k !== 'own') view.fill = k;
      else if (parseTypes(kind)) { view.own = parseTypes(kind); view.fill = 'own'; }
      else return;
      typing = false; save();
      if (active) { draw(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); clear(); return; }
      draw(); fit();
      showHudPrompt(t(types() ? 'hexkit.prompt.helper' : 'hexkit.prompt.free', lang()), 4000);
    },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return build.tiles.size === 0; },
    clear() { build = emptyBuild(); commit(); if (active) fit(); },
    snapshot,
    restore(json) { read(json); save(); if (active) draw(); },
    /** For the browser tests (?probe): a point inside the ghost, and every tile face's mid-point and outward normal (app frame). */
    ghostCentre() {   // inside its first piece (a convex piece, so a ray through it meets the ghost)
      if (!ghostTile) return null;
      const V = previewPieces(build, ghostTile)[0].vertices.map(toApp);
      return V.reduce((a, v) => a.map((c, q) => c + v[q] / V.length), [0, 0, 0]);
    },
    tileFaces() {
      const out = [];
      for (const [key, x] of build.tiles) {
        const ball = toApp(hexoctBall(build.letters.get(x.k), x.i, x.j, x.k));
        for (const p of tilePieces(build, x)) {
          const P = p.vertices.map(toApp), m = P.reduce((a, v) => a.map((c, q) => c + v[q] / P.length), [0, 0, 0]);
          for (const f of p.faces) {
            const F = f.map((q) => P[q]), mid = F.reduce((a, v) => a.map((c, q) => c + v[q] / F.length), [0, 0, 0]);
            const u = F[1].map((c, q) => c - F[0][q]), w = F[2].map((c, q) => c - F[0][q]);
            let n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
            const len = Math.hypot(...n) || 1, out_ = (mid[0] - m[0]) * n[0] + (mid[1] - m[1]) * n[1] + (mid[2] - m[2]) * n[2] < 0 ? -1 : 1;
            n = n.map((c) => (c * out_) / len);
            out.push({ key, mid, normal: n, ball });
          }
        }
      }
      return out;
    },
    /** For the browser tests (?probe): the helper, the build, and the ghost (its tile and its pieces' corners, study frame). */
    probe: () => ({ fill: view.fill, own: view.own, piece: view.piece, types: types(), tiles: snapshotOf(build).tiles, letters: Object.fromEntries(build.letters),
      ghost: ghostTile ? { ...ghostTile } : null, ghostCorners: ghostTile ? previewPieces(build, ghostTile).map((p) => p.vertices) : null,
      next: helper?.tile ? { ...helper.tile } : null, lastPlaced,
      lastCorners: lastPlaced && build.tiles.has(`${lastPlaced.k},${lastPlaced.i},${lastPlaced.j}`) ? tilePieces(build, lastPlaced).map((p) => p.vertices) : null, done: !!helper?.done, conflict: helper?.conflict ?? null,
      ghostOpacity: ghostMat.opacity, lineWidth: lineMats[0]?.linewidth ?? null, solid: !solidMat.transparent }),
  };
}
