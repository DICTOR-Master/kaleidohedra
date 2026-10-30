// The White Queen 600-cell (DICTO 2026-10-27): the companion world of paper #63, "The White Queen 600-cell" (DOI not yet assigned).
// Step 2, the shadows: the true orthogonal 3D shadow of the 600-cell, every one computed live from the exact source model
// (white-queen-data.js via white-queen-geometry.js; no other 600-cell code). All 720 edges are drawn projected (the inner ones too),
// the convex hull as a see-through shell, its real faces (coplanar triangles merged) ivory for triangles and blue for four-sided faces,
// as in #63's figures. Six turnings (DICTO 2026-10-27), one for each pair of the four main directions: two rows of four buttons pick
// the start (From) and the end (To), each jumping to its stop, and one big slider turns the 4D view direction along that pair's great
// circle, snapping at both ends; the caption gives the hull's vertices and faces. The Slice view (W3): one row of four directions and
// one big slider from the centre to the tip that stops only at #63's slice patterns (every vertex height and the exact midpoint of
// every gap), each slice computed live; the tips drawn small. Named stops in gold (W4, DICTO's names): Humpty Dumpty, the real
// 48-vertex cell-first slice at 1 + √5/2 (shown larger, solid ivory with gold edges, turning slowly until touched), and Kagemusha,
// the edge-first slice at 1 + √5. Shells (W4b): the 600 cells round one vertex in 15 shells, each one kind of piece, in perspective
// from just beyond the opposite vertex; one slider builds them from the gold Cleo core outwards, the newest shell solid, the inner ones
// see-through, coloured as the study's picture (blue → green → yellow). Halves (W5) in the Shadow view: the front cells (centre·u > 0)
// gold-ivory, the back cells blue, each tiling the shadow once in the main views; a slider pulls the two layers apart along the
// picture's depth (DICTO's Double Vision); side-on cells are flat and left out. Words in all 7 languages (i18n wq.*).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DIRECTIONS, EDGES, CELLS, shadowAt, viewAt, SLICE_STOPS, sliceAt, CLEO_POINTS, CLEO_SHELLS, quadKind, quadKinds } from './white-queen-geometry.js';
import * as WQG from './white-queen-geometry.js';
import * as RQG from './red-queen-geometry.js';
import { STAGE_KEYS, STAGE_FACTS, stageShadowAt } from './queen-stages-geometry.js';

export const WQ_DIRECTIONS = DIRECTIONS;
/** The slider: 0..1000 along the chosen turning, its two ends the stops (it snaps to one within WQ_SNAP). */
export const WQ_SNAP = 40;
export const WQ_DEFAULT = { from: 'vertex-first', to: 'cell-first' };
export const WQ_MODES = ['shadow', 'slice', 'shells'];
export const WQ_SHELLS = CLEO_SHELLS.length;   // 15
export const WQ_CUT = [0.55, 0.45, 1];   // the Whole view's cut: its normal points at the Shells view's starting camera
export const WQ_ARISTOTLE_ACTION = 'tool:aristotleWorld:icosahedron';   // the Cleo-Icos in Aristotle's Pyramid (paper #44)
// The Red Queen (DICTO 2026-10-29, "start the red queen switch"; paper #65): the 120-cell, built from the White Queen
// (red-queen-geometry.js), in the same three views; her Shells are the nine cell layers round one dodecahedron, her core that
// dodecahedron, the twelve pentagonal pyramids of Aristotle's Pyramid by a cut from its centre.
export const WQ_QUEENS = ['white', 'red'];
export const RQ_LAYERS = RQG.CELL_LAYERS.length;   // 9
export const RQ_ARISTOTLE_ACTION = 'tool:aristotleWorld:dodecahedron';
// RCP view (DICTO 2026-10-29, the Polyhedraverse exact builds): the shells drawn with the RCP build's own perspective formula,
// (x, y, z) / (d − w) with the eye at d = 5 × the radius on the seed's side (krp-core rcpBuild.js, VIEW_MARGIN 5), w along the axis
// through the seed (the White Queen's vertex, as RCP's vertex-first build; the Red Queen's core dodecahedron, as RCP's 120-cell build),
// scaled by d so the sizes stay those of the model.
const UP = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], RCP_MARGIN = 5;
const rcpPoints = (V, r) => V.map((x) => UP.map((f) => (f.reduce((s, c, i) => s + c * x[i], 0) * RCP_MARGIN * r) / (RCP_MARGIN * r - x[0])));
const RCP_POINTS = { white: rcpPoints(WQG.VERTICES, 2), red: rcpPoints(RQG.VERTICES, RQG.RADIUS) };
const RED_FACES = { 5: 0xc8504a, 6: 0xd9a441, 7: 0x7fae7a, 8: 0x8b78c4, 9: 0x4fa3a5, 10: 0xd07fb0 };   // #65's figures (render_atlas120.py), by sides
// the study picture's colours (matplotlib viridis from 0.15 to 0.95), the core gold
const VIRIDIS = [[0, 0x440154], [0.125, 0x482878], [0.25, 0x3e4989], [0.375, 0x31688e], [0.5, 0x26828e], [0.625, 0x1f9e89], [0.75, 0x35b779], [0.875, 0x6ece58], [1, 0xfde725]];
function viridis(x) {
  const i = Math.min(VIRIDIS.length - 2, Math.floor(x * 8)), [a, ca] = VIRIDIS[i], [b, cb] = VIRIDIS[i + 1], f = (x - a) / (b - a);
  return new THREE.Color(ca).lerp(new THREE.Color(cb), f).getHex();
}
export const shellColour = (k, total = WQ_SHELLS) => (k === 0 ? 0xffc857 : viridis(0.15 + (0.8 * k) / (total - 1)));
/** The Shells caption at n shells built: the newest shell, its pieces, one kind. */
export function wqShellsCaption(n, L, red = false) {
  if (red) { const k = n - 1, m = RQG.CELL_LAYERS[k].cells.length; return k === 0 ? t('rq.layers.core', L) : t(k === RQ_LAYERS - 1 ? 'rq.layers.far' : 'rq.layers.layer', L, { k, n: m }); }
  const k = n - 1, m = CLEO_SHELLS[k].cells.length;
  if (k === 0) return t('wq.shells.core', L);
  return t(k === WQ_SHELLS - 1 ? 'wq.shells.wrap' : 'wq.shells.shell', L, { k, n: m });
}
const FRONT = 0xf6e7bf, BACK = 0x7fa6dc;   // Halves: the front layer gold-ivory, the back layer blue
/** DICTO's named slices (gold captions): direction and exact height. */
export const WQ_NAMED = [{ key: 'humpty', dir: 'cell-first', height: '1 + 1/2√5' }, { key: 'shadow17', dir: 'edge-first', height: '1 + √5' }];
const namedAt = (dir, height) => WQ_NAMED.find((x) => x.dir === dir && x.height === height) ?? null;
/** A slice stop's place on its slider (0..1000, by height from the centre to the tip). */
export const sliceU = (dir, k, red = false) => { const S = (red ? RQG : WQG).SLICE_STOPS[DIRECTIONS.indexOf(dir)]; return Math.round((1000 * S[k].value) / S[S.length - 1].value); };
const faceSizes = (faces) => faces.reduce((m, f) => ({ ...m, [f.length]: (m[f.length] ?? 0) + 1 }), {});
/** The slice caption: [name ·] direction · height h · at a vertex height | between heights · counts (or what the tip is). */
/** The Red Queen's faces by sides: triangles, four-sided faces, then faces of k sides. */
const sidedCounts = (faces, L) => Object.entries(faceSizes(faces)).map(([k, n]) => (k === '3' ? t('wq.count.triangles', L, { n }) : k === '4' ? t('wq.count.quads', L, { n }) : t('rq.count.sided', L, { n, k })));
export function wqSliceCaption(dir, k, L, red = false) {
  if (red) {
    const s = RQG.sliceAt(dir, k), st = s.stop;
    const parts = [t(`wq.dir.${dir}`, L), t('wq.slice.height', L, { h: st.height }), t(st.atVertex ? 'wq.slice.at' : 'wq.slice.between', L)];
    if (s.dim === 3) parts.push(t('wq.count.vertices', L, { n: s.vertices.length }), ...sidedCounts(s.faces, L));
    if (st.tip) parts.push(t(`rq.tip.${s.dim}`, L));
    return parts.join(' · ');
  }
  const s = sliceAt(dir, k), st = s.stop, nm = namedAt(dir, st.height);
  const parts = [t(`wq.dir.${dir}`, L), t('wq.slice.height', L, { h: st.height }), t(st.atVertex ? 'wq.slice.at' : 'wq.slice.between', L)];
  if (s.dim === 3) {
    const fs = faceSizes(s.faces);
    parts.push(t('wq.count.vertices', L, { n: s.vertices.length }), t('wq.count.triangles', L, { n: fs[3] ?? 0 }));
    if (fs[4]) parts.push(t('wq.count.quads', L, { n: fs[4] }));
    // the four-sided faces' kinds (W7): kites and squares named in the caption
    const q = quadKinds(s);
    if (q.kite) parts.push(t('wq.kind.kite', L, { n: q.kite }));
    if (q.square) parts.push(t('wq.kind.square', L, { n: q.square }));
  }
  if (st.tip) parts.push(t(`wq.tip.${s.dim}`, L));
  return `${nm ? `${t(`wq.name.${nm.key}`, L)} · ` : ''}${parts.join(' · ')}`;
}
const SHORT = { vertex: 'vertex-first', edge: 'edge-first', face: 'face-first', cell: 'cell-first' };   // ?open=whitequeen:<short>
const IVORY = 0xefe9dc, BLUE = 0x9fb4c8, OTHER = 0xd8c690;   // as #63's figures (render_atlas.py); faces of 5+ sides never show at the stops
const SHELL = 0.42;   // the see-through shell's opacity
const ROSE = 0xd98fa6, DEEP_BLUE = 0x5b7fb8;   // W7: kites rose, squares a deeper blue than the other four-sided faces
const GOLD = 0xffc857, SLICE_EDGE = 0x4a505c, HUMPTY_SCALE = 1.3, GLOW = 0.38;   // GLOW: each face lit from within in its own colour (ivory, not grey)   // Humpty Dumpty: gold edges, a bit larger
const lang = () => getSettings().language;

/** The caption: the direction at a stop (or "from → to" between them) and the hull's vertex and face counts. */
export function wqCaption({ from, to, u }, s, L, red = false) {
  const head = u === 0 ? t(`wq.dir.${from}`, L) : u === 1000 ? t(`wq.dir.${to}`, L) : t('wq.between', L, { a: t(`wq.dir.${from}`, L), b: t(`wq.dir.${to}`, L) });
  if (red) return `${head} · ${[t('wq.count.vertices', L, { n: s.vertices.length }), ...sidedCounts(s.faces, L)].join(' · ')}`;
  const parts = [t('wq.count.vertices', L, { n: s.vertices.length }), t('wq.count.triangles', L, { n: s.triangles })];
  if (s.quads) parts.push(t('wq.count.quads', L, { n: s.quads }));
  if (s.others) parts.push(t('wq.count.others', L, { n: s.others }));
  return `${head} · ${parts.join(' · ')}`;
}

export function createWhiteQueenWorld({ scene, fitView = () => {}, openAction = () => {} }) {
  const STORAGE_KEY = storageKey('whiteQueen');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // the view: Shadow (the turning from → to, the slider's place u) or Slice (a direction and its stop k)
  const view = { queen: 'white', stage: 0, mode: 'shadow', ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0, shells: 1, halves: false, apart: 0, lineUp: false, whole: false, rcp: false };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (WQ_QUEENS.includes(d?.queen)) view.queen = d.queen;
    if (WQ_MODES.includes(d?.mode)) view.mode = d.mode;
    view.stage = view.queen === 'red' ? 6 : 0;
    if (Number.isInteger(d?.stage) && d.stage > 0 && d.stage < 6 && d?.mode === 'shadow') view.stage = d.stage;
    if (DIRECTIONS.includes(d?.from) && DIRECTIONS.includes(d?.to) && d.from !== d.to) Object.assign(view, { from: d.from, to: d.to });
    if (Number.isFinite(d?.u)) view.u = Math.max(0, Math.min(1000, Math.round(d.u)));
    if (DIRECTIONS.includes(d?.sliceDir)) view.sliceDir = d.sliceDir;
    if (Number.isInteger(d?.shells)) view.shells = Math.max(1, Math.min(d?.queen === 'red' ? RQ_LAYERS : WQ_SHELLS, d.shells));
    view.halves = d?.halves === true;
    view.lineUp = d?.lineUp === true;
    view.whole = d?.whole === true;
    view.rcp = d?.rcp === true;
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1000, Math.round(d.apart)));
    if (Number.isInteger(d?.sliceK)) view.sliceK = Math.max(0, Math.min((view.queen === 'red' ? RQG : WQG).SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length - 1, d.sliceK));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;
  // the queen shown: her model (both modules have the same names), her shells (the Cleo shells or the nine cell layers), her radius
  const red = () => view.queen === 'red';
  // the five stages between the queens (DICTO 2026-10-30): in the Shadow view the stage slider runs White → five truncations → Red;
  // at a stage between them only the shadow is drawn (Slice and Shells belong to the queens)
  const mid = () => view.mode === 'shadow' && view.stage > 0 && view.stage < 6;
  const stageKey = () => STAGE_KEYS[view.stage];
  const M = () => (red() ? RQG : WQG);
  const totalShells = () => (red() ? RQ_LAYERS : WQ_SHELLS);
  const shellList = () => (red() ? RQG.CELL_LAYERS : CLEO_SHELLS);
  const rad = () => (mid() ? 2 : red() ? RQG.RADIUS : 2) * WS;   // the circumradius: every shadow and slice fits inside it
  /** A cell's faces as corner loops and its corners: the White Queen's tetrahedra, the Red Queen's dodecahedra. */
  const facesOf = (ci) => { if (red()) return RQG.cellFaces(ci); const c = CELLS[ci]; return [[c[0], c[1], c[2]], [c[0], c[1], c[3]], [c[0], c[2], c[3]], [c[1], c[2], c[3]]]; };
  const cornersOf = (ci) => (red() ? RQG.CELLS[ci].corners : CELLS[ci]);
  /** Keep the view inside the queen's own ranges (after switching). */
  const clampToQueen = () => { view.shells = Math.max(1, Math.min(totalShells(), view.shells)); view.sliceK = Math.max(0, Math.min(M().SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length - 1, view.sliceK)); };

  // ---- the Shadow view ----
  const shadowGroup = new THREE.Group();
  // Render standard (docs/RENDER-STANDARD.md, DICTO 10-30): solid faces with polygon offset in the app's Colour (solid) view, glass only
  // in the Translucent view; no milky emissive wash; edges as antialiased screen-space lines (outline 2.4 px, inner 1.4 px).
  const shellMat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: SHELL, depthWrite: false, roughness: 0.5, metalness: 0, emissive: 0x16140f, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  shellMat.userData.hollow = true;
  const innerMat = new THREE.LineBasicMaterial({ color: 0xb8c2d6, transparent: true, opacity: 0.3, depthWrite: false });   // the inner edges step back so the outline reads
  const hullMat = new THREE.LineBasicMaterial({ color: 0xfff4d6 });
  // fixed buffers, refilled as the slider moves, sized for the larger queen: 1200 edges (the Red Queen's; the White Queen's 720), and the
  // shell (at most 2 × 600 − 4 hull triangles, 1794 hull edges)
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(RQG.EDGES.length * 6), 3));
  const inner = new THREE.LineSegments(edgeGeo, innerMat);
  const shellGeo = new THREE.BufferGeometry();
  shellGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(1196 * 9), 3));
  shellGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(1196 * 9), 3));
  shellGeo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(1196 * 9), 3));
  const shell = new THREE.Mesh(shellGeo, shellMat);
  shell.renderOrder = 2;
  const hullGeo = new THREE.BufferGeometry();
  hullGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(1794 * 6), 3));
  const hullLines = new THREE.LineSegments(hullGeo, hullMat);
  // a stage's edges (at most the bitruncated stage's 7200)
  const stageGeo = new THREE.BufferGeometry();
  stageGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(7200 * 6), 3));
  const stageLines = new THREE.LineSegments(stageGeo, innerMat);
  const fat = (color, width, op = 1) => { const l = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color, linewidth: width, transparent: op < 1, opacity: op, depthWrite: op >= 1 })); l.frustumCulled = false; return l; };
  const setFat = (l, arr, count) => { l.geometry.dispose(); l.geometry = new LineSegmentsGeometry(); if (count > 0) l.geometry.setPositions(arr.subarray(0, count)); l.visible = l.visible && count > 0; };
  const fatInner = fat(0xb8c2d6, 1.4, 0.55), fatStage = fat(0xb8c2d6, 1.2, 0.5), fatHull = fat(0xfff4d6, 2.4);
  fatInner.renderOrder = 1; fatStage.renderOrder = 1; fatHull.renderOrder = 3;
  shadowGroup.add(fatInner, fatStage, shell, fatHull);
  for (const o of [inner, stageLines, shell, hullLines]) o.frustumCulled = false;

  // ---- the Slice view: rebuilt per stop, in its own turning group (Humpty Dumpty turns) ----
  // Line up (W7): the align group turns the slice so its direction's main symmetry axis (SLICE_AXES) points at the viewer
  const sliceGroup = new THREE.Group(), align = new THREE.Group(), spin = new THREE.Group();
  sliceGroup.add(align); align.add(spin);
  const Z = new THREE.Vector3(0, 0, 1);
  const applyAlign = () => { if (view.lineUp) align.quaternion.setFromUnitVectors(new THREE.Vector3(...M().SLICE_AXES[DIRECTIONS.indexOf(view.sliceDir)]), Z); else align.quaternion.identity(); };
  group.add(shadowGroup, sliceGroup);
  const dotGeo = new THREE.SphereGeometry(1, 16, 12);
  let humpty = false, spinStopped = false;
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clearSpin() {
    for (const c of [...spin.children]) { spin.remove(c); if (c.geometry !== dotGeo) c.geometry.dispose(); c.material.dispose(); }
  }
  function drawShadow() {
    const md = mid(), s = md ? stageShadowAt(stageKey(), view.from, view.to, view.u / 1000) : M().shadowAt(view.from, view.to, view.u / 1000), E = md ? s.edges : M().EDGES;
    shown = s;
    const P = s.P.map((p) => p.map((c) => c * WS)), Q = s.points.map((p) => p.map((c) => c * WS));
    const geo = md ? stageGeo : edgeGeo, ep = geo.attributes.position.array;
    E.forEach(([i, j], k) => { ep.set(P[i], k * 6); ep.set(P[j], k * 6 + 3); });
    geo.setDrawRange(0, E.length * 2);
    geo.attributes.position.needsUpdate = true;
    fatInner.visible = !md; fatStage.visible = md;
    setFat(md ? fatStage : fatInner, ep, E.length * 6);
    const sp = shellGeo.attributes.position.array, sc = shellGeo.attributes.color.array, sn = shellGeo.attributes.normal.array, hp = hullGeo.attributes.position.array;
    const col = new THREE.Color(), a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
    let n = 0, m = 0;
    for (const f of s.faces) {
      col.setHex(f.length === 3 ? IVORY : f.length === 4 ? BLUE : red() || md ? RED_FACES[f.length] ?? OTHER : OTHER);
      a.fromArray(Q[f[0]]); b.fromArray(Q[f[1]]).sub(a); c.fromArray(Q[f[2]]).sub(a);
      const nrm = b.cross(c).normalize();
      for (let i = 1; i + 1 < f.length; i++) {
        for (const k of [f[0], f[i], f[i + 1]]) { sp.set(Q[k], n * 3); sc.set([col.r, col.g, col.b], n * 3); sn.set([nrm.x, nrm.y, nrm.z], n * 3); n++; }
      }
      f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (k < l) { hp.set(Q[k], m * 3); hp.set(Q[l], m * 3 + 3); m += 2; } });
    }
    shellGeo.setDrawRange(0, n);
    hullGeo.setDrawRange(0, m);
    for (const x of ['position', 'color', 'normal']) shellGeo.attributes[x].needsUpdate = true;
    hullGeo.attributes.position.needsUpdate = true;
    fatHull.visible = true; setFat(fatHull, hp, m * 3);
    shell.visible = !skeleton;
    const solid = opacity >= 1;   // Colour (solid): an opaque shell like the Polyhedraverse stars; Translucent: the glass shows the inside
    if (shellMat.transparent === solid) { shellMat.transparent = !solid; shellMat.depthWrite = solid; shellMat.needsUpdate = true; }
    shellMat.opacity = solid ? 1 : SHELL * opacity;
  }
  function drawSlice() {
    clearSpin();
    const s = M().sliceAt(view.sliceDir, view.sliceK), nm = red() ? null : namedAt(view.sliceDir, s.stop.height);
    shown = s;
    const wasHumpty = humpty;
    humpty = nm?.key === 'humpty';
    if (humpty && !wasHumpty) spinStopped = false;   // arriving at Humpty Dumpty: he turns again
    if (!humpty || view.lineUp) spin.rotation.set(0, 0, 0);
    if (view.lineUp) spinStopped = true;   // lined up: Humpty Dumpty holds still on the axis
    applyAlign();
    const scale = WS * (humpty ? HUMPTY_SCALE : 1), Q = s.points.map((p) => p.map((c) => c * scale));
    const edgeHex = humpty ? GOLD : skeleton ? 0xdfe6f0 : SLICE_EDGE;
    const lines = [];
    if (s.dim === 3) {
      // one mesh per colour, each lit a little from within in its own colour, so the ivory and the blue read as in #63's figures
      const byColour = new Map();
      for (const f of s.faces) {
        const qk = f.length === 4 ? quadKind(f.map((k) => s.points[k])) : null;
        const hex = f.length === 3 ? IVORY : qk === 'kite' ? ROSE : qk === 'square' ? DEEP_BLUE : f.length === 4 ? BLUE : red() ? RED_FACES[f.length] ?? OTHER : OTHER;
        if (!byColour.has(hex)) byColour.set(hex, []);
        const pos = byColour.get(hex);
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) pos.push(...Q[k]);
        f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (k < l) lines.push(...Q[k], ...Q[l]); });
      }
      if (!skeleton) {
        const see = opacity < 1 && !humpty;
        for (const [hex, pos] of byColour) {
          const g = new THREE.BufferGeometry();
          g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
          g.computeVertexNormals();
          spin.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: hex, emissive: new THREE.Color(hex).multiplyScalar(GLOW), side: THREE.DoubleSide, flatShading: true, roughness: 0.55,
            transparent: see, opacity: see ? opacity : 1, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 })));
        }
      }
    } else {
      // a tip: a point, an edge or a triangle, drawn small but visible (dots at its corners)
      const r = 0.045 * WS;
      for (const p of Q) { const m = new THREE.Mesh(dotGeo, new THREE.MeshStandardMaterial({ color: IVORY, emissive: 0x4a463c })); m.scale.setScalar(r); m.position.fromArray(p); spin.add(m); }
      Q.forEach((p, i) => Q.slice(i + 1).forEach((q) => lines.push(...p, ...q)));
      if (s.dim === 2 && !skeleton) {
        const g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.Float32BufferAttribute(Q.slice(0, 3).flat(), 3));
        g.computeVertexNormals();
        spin.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: IVORY, side: THREE.DoubleSide, emissive: 0x4a463c })));
      }
    }
    if (lines.length) {
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
      const fl = fat(s.dim < 3 ? IVORY : edgeHex, 2); fl.geometry.setPositions(lines); spin.add(fl); lg.dispose();
    }
    for (const o of spin.children) o.frustumCulled = false;
    tickSpin();
  }
  // Humpty Dumpty turns slowly on his own while the slider rests on him, until the picture is touched (not with reduced motion)
  let raf = 0;
  function tickSpin() {
    if (raf) return;
    const step = () => {
      raf = 0;
      if (!active || view.mode !== 'slice' || !humpty || spinStopped || reduceMotion()) return;
      spin.rotation.y += 0.004;
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  }
  document.addEventListener('pointerdown', (e) => { if (active && humpty && e.target?.tagName === 'CANVAS') spinStopped = true; });

  // ---- Halves and Shells: meshes rebuilt on change ----
  const halvesGroup = new THREE.Group(), shellsGroup = new THREE.Group();
  group.add(halvesGroup, shellsGroup);
  const clear = (g) => { for (const c of [...g.children]) { g.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  /** Cells (indices into the queen's cells) at points Q as one mesh (their faces fanned into triangles) and their edges. */
  function cellsMesh(g, list, Q, hex, { opacity: op = 1, edge = SLICE_EDGE, edgeOpacity = 1, offset = [0, 0, 0], order = 3, glow = GLOW * 0.8, roughness = 0.6, shrink = 1 } = {}) {
    const pos = [], lines = [];
    for (const ci of list) {
      const c = cornersOf(ci);
      // shrink < 1: each cell drawn a little smaller about its own centre, so shared faces never coincide (no flicker) and every
      // cell reads as its own piece
      const m = [0, 1, 2].map((i) => c.reduce((a, k) => a + Q[k][i], 0) / c.length);
      const at = (k) => Q[k].map((x, i) => m[i] + shrink * (x - m[i]) + offset[i]);
      for (const f of facesOf(ci)) {
        for (let i = 1; i + 1 < f.length; i++) pos.push(...at(f[0]), ...at(f[i]), ...at(f[i + 1]));
        f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (red() || k < l) lines.push(...at(k), ...at(l)); });
      }
    }
    const see = op < 1;
    if (!skeleton) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      geo.computeVertexNormals();
      const mat = new THREE.MeshStandardMaterial({ color: hex, side: THREE.DoubleSide, flatShading: true, roughness, emissive: new THREE.Color(hex).multiplyScalar(glow), transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
      if (see) mat.userData.hollow = true;
      const m = new THREE.Mesh(geo, mat); m.frustumCulled = false; if (see) m.renderOrder = order; g.add(m);
    }
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
    const l = fat(skeleton ? 0xdfe6f0 : edge, 1.8, edgeOpacity); if (lines.length) l.geometry.setPositions(lines); lg.dispose();
    g.add(l);
  }
  let halvesShown = null;
  function drawHalves() {
    clear(halvesGroup);
    const s = shown, h = M().halves(s.u), P = s.P.map((p) => p.map((c) => c * WS));
    // apart: the two layers move away from each other along the picture's depth (the axis towards the starting camera), up to the
    // shadow's diameter in all
    const off = (view.apart / 1000) * rad();
    cellsMesh(halvesGroup, h.front, P, FRONT, { opacity: 0.55, edge: 0xfff4d6, edgeOpacity: 0.7, offset: [0, 0, off], order: 5 });   // the front layer drawn last: on top where they meet
    cellsMesh(halvesGroup, h.back, P, BACK, { opacity: 0.55, edge: 0xcfe0ff, edgeOpacity: 0.7, offset: [0, 0, -off], order: 4 });
    halvesShown = { front: h.front.length, back: h.back.length, side: h.side.length };
  }
  let shellsRadius = 1, wholeKept = [];
  function drawShells() {
    clear(shellsGroup);
    const Q = (view.rcp ? RCP_POINTS[view.queen] : red() ? RQG.LAYER_POINTS : CLEO_POINTS).map((p) => p.map((c) => c * WS)), n = view.shells, SH = shellList(), N = totalShells();
    if (view.whole) {
      // Whole (DICTO 2026-10-28): all 15 shells at once, cut open like an onion: the half facing the starting camera removed (a cell
      // stays when its centre lies behind the cut through the centre), every shell solid in its own colour, lit (little glow) so the
      // nested shells read in depth
      const cut = new THREE.Vector3(...WQ_CUT).normalize(); wholeKept = [];
      for (let k = 0; k < N; k++) {
        const keep = SH[k].cells.filter((ci) => { const c = cornersOf(ci); let d = 0; for (const v of c) d += Q[v][0] * cut.x + Q[v][1] * cut.y + Q[v][2] * cut.z; return d < 0; });
        wholeKept.push(keep.length);
        // the Red Queen's far dodecahedron wraps all the others in this perspective, whole (no cut opens it): it stays see-through
        const wrap = red() && k === N - 1 && !view.rcp;
        cellsMesh(shellsGroup, wrap ? SH[k].cells : keep, Q, shellColour(k, N), wrap ? { opacity: 0.08, edge: 0xffffff, edgeOpacity: 0.25 } : { opacity: 1, edge: 0x1d2027, edgeOpacity: 0.5, glow: 0.12, roughness: 0.45, shrink: 0.94 });
      }
      shellsRadius = Math.max(...Q.map((p) => Math.hypot(...p)).filter(Number.isFinite));
      shown = { shells: N, whole: true };
      return;
    }
    // the newest shell solid (a touch see-through, so the gaps of shells 6 and 8 show what is inside), the ones inside it faint
    for (let k = 0; k < n; k++) {
      const newest = k === n - 1;
      cellsMesh(shellsGroup, SH[k].cells, Q, shellColour(k, N), newest ? { opacity: 0.9, edge: 0xf3ead2, edgeOpacity: 0.85, glow: 0.16, roughness: 0.45 } : { opacity: 0.1, edge: 0xffffff, edgeOpacity: 0.12 });
    }
    shellsRadius = Math.max(...SH[n - 1].cells.flatMap((c) => cornersOf(c)).map((k) => Math.hypot(...Q[k])));
    shown = { shells: n };
  }
  function draw() {
    if (!active) return;
    const halvesOn = view.mode === 'shadow' && view.halves && !mid();
    shadowGroup.visible = view.mode === 'shadow' && !halvesOn;
    halvesGroup.visible = halvesOn;
    sliceGroup.visible = view.mode === 'slice';
    shellsGroup.visible = view.mode === 'shells';
    if (view.mode !== 'slice') { humpty = false; clearSpin(); }
    if (view.mode !== 'shells') clear(shellsGroup);
    if (!halvesOn) { clear(halvesGroup); halvesShown = null; }
    if (view.mode === 'shadow') { drawShadow(); if (halvesOn) drawHalves(); } else if (view.mode === 'slice') drawSlice(); else drawShells();
    renderPanel();
  }
  const fitShadow = () => fitView([0, 0, 0], rad() * 1.12, [0.3, 0.25, 1]);
  // the Shells view frames the newest shell (they grow from the small core to the outer wrap), zooming in as well as out
  const fit = () => (view.mode === 'slice' && view.lineUp ? fitView([0, 0, 0], rad() * 1.12, [0, 0, 1], true) : view.mode === 'shells' ? fitView([0, 0, 0], shellsRadius * 1.15, WQ_CUT, true) : view.mode === 'shadow' && view.halves && view.apart ? fitView([0, 0, 0], rad() * (1.12 + view.apart / 1000), [1, 0.35, 0.55], true) : fitShadow());

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldwhiteQueen-panel';
  panel.className = 'qc-panel';
  const row = (end, label = true) => `<div class="w4d-row w4d-options wq-row" data-wq-row="${end}">${label ? `<span class="hull-pick wq-row-label" data-wq-label="${end}"></span>` : ''}${DIRECTIONS.map((k) => `<button type="button" data-wq-${end}="${k}"></button>`).join('')}</div>`;
  panel.innerHTML = `
    <div class="w4d-row w4d-options wq-queens">${WQ_QUEENS.map((q) => `<button type="button" data-wq-queen="${q}"></button>`).join('')}</div>
    <div class="w4d-row wq-stage-row"><label class="hull-pick"><span class="wq-stage-label"></span> <input type="range" class="st-slider" min="0" max="6" step="1"></label></div>
    <div class="w4d-row w4d-options wq-modes">${WQ_MODES.map((m) => `<button type="button" data-wq-mode="${m}"></button>`).join('')}</div>
    ${row('from')}
    ${row('to')}
    ${row('slice', false)}
    <div class="w4d-row w4d-options wq-halves-row"><button type="button" data-wq-halves></button></div>
    <div class="w4d-row wq-param-row"><label class="hull-pick"><span class="wq-param-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row wq-slice-row"><label class="hull-pick"><span class="wq-slice-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row wq-apart-row"><label class="hull-pick"><span class="wq-apart-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row w4d-options wq-link-row"><button type="button" data-wq-link></button></div>
    <div class="w4d-row w4d-options wq-lineup-row"><button type="button" data-wq-lineup></button></div>
    <div class="w4d-row st-note wq-legend"></div>
    <div class="w4d-row w4d-options wq-whole-row"><button type="button" data-wq-whole></button><button type="button" data-wq-rcp></button></div>
    <div class="w4d-row wq-shells-row"><label class="hull-pick"><span class="wq-shells-label"></span> <input type="range" class="st-slider" min="1" max="${CLEO_SHELLS.length}" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'whiteQueen');
  const input = panel.querySelector('.wq-param-row input'), sliceInput = panel.querySelector('.wq-slice-row input');
  const apartInput = panel.querySelector('.wq-apart-row input'), shellsInput = panel.querySelector('.wq-shells-row input'), halvesBtn = panel.querySelector('[data-wq-halves]');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold'), stageInput = panel.querySelector('.wq-stage-row input');
  note.addEventListener('click', () => note.classList.toggle('open'));
  // the world's title beside Back follows the queen shown (the names are DICTO's, in every language)
  const TITLE = { white: 'The White Queen 600-cell', red: 'The Red Queen 120-cell', t01: 'The truncated 600-cell', t1: 'The rectified 600-cell', t12: 'The bitruncated 600-cell', t2: 'The rectified 120-cell', t23: 'The truncated 120-cell' };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const title = document.getElementById('hud-world-title');
    if (title && Object.values(TITLE).includes(title.textContent)) title.textContent = TITLE[mid() ? stageKey() : view.queen];
    const L = lang(), shadow = view.mode === 'shadow', slice = view.mode === 'slice', shells = view.mode === 'shells';
    panel.querySelectorAll('[data-wq-queen]').forEach((x) => { const on = !mid() && x.dataset.wqQueen === view.queen; x.textContent = t(`wq.queen.${x.dataset.wqQueen}`, L); x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); });
    panel.querySelector('.wq-stage-row').hidden = !shadow;
    panel.querySelector('.wq-stage-label').textContent = t('wq.stage.param', L, { name: mid() ? t(`wq.stage.${stageKey()}`, L) : t(`wq.queen.${view.queen}`, L) });
    stageInput.value = String(view.stage);
    panel.querySelectorAll('[data-wq-mode]').forEach((x) => { x.textContent = t(`wq.view.${x.dataset.wqMode}`, L); x.classList.toggle('active', x.dataset.wqMode === view.mode); });
    // nothing unnecessary shown: each view only its own rows
    panel.querySelector('[data-wq-row="from"]').hidden = panel.querySelector('[data-wq-row="to"]').hidden = panel.querySelector('.wq-param-row').hidden = !shadow;
    panel.querySelector('[data-wq-row="slice"]').hidden = panel.querySelector('.wq-slice-row').hidden = !slice;
    panel.querySelector('.wq-halves-row').hidden = !shadow || mid();
    panel.querySelector('.wq-apart-row').hidden = !(shadow && view.halves && !mid());
    panel.querySelector('.wq-shells-row').hidden = !shells;
    panel.querySelector('.wq-lineup-row').hidden = !slice;
    const lu = panel.querySelector('[data-wq-lineup]');
    lu.textContent = t('wq.lineUp', L); lu.classList.toggle('active', view.lineUp); lu.setAttribute('aria-pressed', String(view.lineUp));
    // the legend: only when the slice has kites or squares
    const legend = panel.querySelector('.wq-legend'), qk = slice && shown.dim === 3 ? quadKinds(shown) : null;
    legend.hidden = !(qk && (qk.kite || qk.square));
    if (!legend.hidden) {
      const sw = (hex, key) => `<span class="wq-sw"><i style="background:#${new THREE.Color(hex).getHexString()}"></i>${t(key, L)}</span>`;
      legend.innerHTML = [qk.kite ? sw(ROSE, 'wq.legend.kite') : '', qk.square ? sw(DEEP_BLUE, 'wq.legend.square') : '', sw(BLUE, 'wq.legend.quad'), sw(IVORY, 'wq.legend.triangle')].join('');
    }
    // at the Cleo core, the back link to the Cleo-Icos in Aristotle's Pyramid (each shape lives in one place, the others link)
    panel.querySelector('.wq-link-row').hidden = !(shells && view.shells === 1 && !view.whole);
    panel.querySelector('[data-wq-link]').textContent = t(red() ? 'rq.link.aristotle' : 'wq.link.aristotle', L);
    const wb = panel.querySelector('[data-wq-whole]');
    wb.textContent = t('wq.whole', L); wb.classList.toggle('active', view.whole); wb.setAttribute('aria-pressed', String(view.whole));
    panel.querySelector('.wq-whole-row').hidden = !shells;
    const rb = panel.querySelector('[data-wq-rcp]');
    rb.textContent = t('wq.rcp', L); rb.classList.toggle('active', view.rcp); rb.setAttribute('aria-pressed', String(view.rcp));
    panel.querySelector('.wq-shells-row').hidden = !shells || view.whole;   // nothing unnecessary shown: the slider builds shells one by one
    halvesBtn.textContent = t('wq.halves', L); halvesBtn.classList.toggle('active', view.halves); halvesBtn.setAttribute('aria-pressed', String(view.halves));
    for (const end of ['from', 'to', 'slice']) {
      const lab = panel.querySelector(`[data-wq-label="${end}"]`);
      if (lab) lab.textContent = t(`wq.${end}`, L);
      panel.querySelectorAll(`[data-wq-${end}]`).forEach((x) => {
        const k = x.getAttribute(`data-wq-${end}`);
        x.textContent = t(`wq.btn.${k}`, L);
        x.title = t(`wq.dir.${k}`, L);
        x.classList.toggle('active', k === (end === 'slice' ? view.sliceDir : view[end]));
        x.hidden = end === 'to' && k === view.from;   // a direction does not turn to itself: nothing unnecessary shown
      });
    }
    const nm = slice && !red() ? namedAt(view.sliceDir, shown.stop.height) : null;
    caption.classList.toggle('wq-gold', !!nm || (shells && view.shells === 1 && !view.whole));
    if (shadow) {
      panel.querySelector('.wq-param-label').textContent = t('wq.param', L, { a: t(`wq.dir.${view.from}`, L), b: t(`wq.dir.${view.to}`, L) });
      input.value = String(view.u);
      caption.textContent = mid() ? `${t(`wq.stage.${stageKey()}.cells`, L)} · ${wqCaption(view, shown, L, true)}`
        : wqCaption(view, shown, L, red()) + (halvesShown ? ` · ${t('wq.halves.counts', L, { f: halvesShown.front, b: halvesShown.back, s: halvesShown.side })}` : '');
      note.textContent = mid() ? t('wq.note.stage', L) : t(`${red() ? 'rq' : 'wq'}.note${view.halves ? '.halves' : ''}`, L);
      panel.querySelector('.wq-apart-label').textContent = t('wq.halves.param', L);
      apartInput.value = String(view.apart);
    } else if (shells && view.whole) {
      caption.textContent = t(red() ? 'rq.layers.whole' : 'wq.shells.whole', L);
      note.textContent = `${t(red() ? 'rq.note.layers' : 'wq.note.shells', L)} ${t('wq.note.rcp', L)}`;
    } else if (shells) {
      panel.querySelector('.wq-shells-label').textContent = t(red() ? 'rq.layers.param' : 'wq.shells.param', L, { n: view.shells, total: totalShells() });
      shellsInput.max = String(totalShells());
      shellsInput.value = String(view.shells);
      caption.textContent = wqShellsCaption(view.shells, L, red());
      note.textContent = `${t(red() ? 'rq.note.layers' : 'wq.note.shells', L)} ${t('wq.note.tapNext', L)} ${t('wq.note.rcp', L)}`;
    } else {
      panel.querySelector('.wq-slice-label').textContent = t('wq.slice.param', L, { d: t(`wq.dir.${view.sliceDir}`, L) });
      sliceInput.value = String(sliceU(view.sliceDir, view.sliceK, red()));
      caption.textContent = wqSliceCaption(view.sliceDir, view.sliceK, L, red());
      note.textContent = t(red() ? 'rq.note.slice' : 'wq.note.slice', L);
    }
  }
  const go = (v) => { if (v === view.u) return; view.u = v; save(); draw(); };
  input.addEventListener('input', () => {
    let v = Number(input.value);
    if (v <= WQ_SNAP) v = 0; else if (v >= 1000 - WQ_SNAP) v = 1000;
    input.value = String(v);
    go(v);
  });
  // the stage slider: its ends are the queens; between them the five stages (Shadow view only)
  stageInput.addEventListener('input', () => {
    const k = Number(stageInput.value); if (k === view.stage) return;
    view.stage = k; if (k === 0) view.queen = 'white'; else if (k === 6) view.queen = 'red';
    clampToQueen(); save(); draw(); fit();
  });
  apartInput.addEventListener('input', () => { view.apart = Number(apartInput.value); save(); draw(); });
  apartInput.addEventListener('change', fit);
  panel.querySelector('[data-wq-whole]').addEventListener('click', () => { view.whole = !view.whole; save(); draw(); fit(); });
  panel.querySelector('[data-wq-rcp]').addEventListener('click', () => { view.rcp = !view.rcp; save(); draw(); fit(); });
  shellsInput.addEventListener('input', () => { const n = Number(shellsInput.value); if (n === view.shells) return; view.shells = n; save(); draw(); fit(); });
  // the slice slider stops only at the atlas's stops: the nearest one
  sliceInput.addEventListener('input', () => {
    const v = Number(sliceInput.value), S = M().SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)], rd = red();
    let k = 0;
    S.forEach((_, i) => { if (Math.abs(sliceU(view.sliceDir, i, rd) - v) < Math.abs(sliceU(view.sliceDir, k, rd) - v)) k = i; });
    sliceInput.value = String(sliceU(view.sliceDir, k, rd));
    if (k === view.sliceK) return;
    view.sliceK = k; save(); draw();
  });
  // From: the turning starts there (the slider at its start); To: it ends there (the slider at its end). Picking as From the
  // direction that is To swaps the two. Slice: the direction, from its centre.
  panel.addEventListener('click', (e) => {
    if (e.target.closest('[data-wq-link]')) { openAction(red() ? RQ_ARISTOTLE_ACTION : WQ_ARISTOTLE_ACTION); return; }
    const qb = e.target.closest('[data-wq-queen]');
    if (qb) { if (qb.dataset.wqQueen === view.queen && !mid()) return; view.queen = qb.dataset.wqQueen; view.stage = red() ? 6 : 0; clampToQueen(); save(); draw(); fit(); return; }
    if (e.target.closest('[data-wq-lineup]')) { view.lineUp = !view.lineUp; if (!view.lineUp) spinStopped = false; save(); draw(); fit(); return; }
    if (e.target.closest('[data-wq-halves]')) { view.halves = !view.halves; save(); draw(); fit(); return; }
    const b = e.target.closest('[data-wq-from], [data-wq-to], [data-wq-slice], [data-wq-mode]');
    if (!b) return;
    const { wqFrom: from, wqTo: to, wqSlice: sl, wqMode: mode } = b.dataset;
    if (mode) { if (mode === view.mode) return; if (mid()) view.stage = red() ? 6 : 0; view.mode = mode; save(); draw(); fit(); return; }
    else if (from) { if (from === view.to) view.to = view.from; view.from = from; view.u = 0; }
    else if (to && to !== view.from) { view.to = to; view.u = 1000; }
    else if (sl) { if (sl === view.sliceDir) return; view.sliceDir = sl; view.sliceK = 0; }
    else return;
    save(); draw();
  });
  // the app's projection button (3D → ∥ → ISO → REV): REV adds its slider to this panel, so the picture is framed again above it
  // (only on entering or leaving REV, keeping the view's direction; ∥ and ISO are left alone, ISO being a direction)
  const fitRadius = () => (view.mode === 'shells' ? shellsRadius * 1.15 : view.mode === 'shadow' && view.halves && view.apart ? rad() * (1.12 + view.apart / 1000) : rad() * 1.12);
  let wasRev = false;
  document.addEventListener('click', (e) => {
    if (!active || !e.target.closest?.('#projection-toggle')) return;
    setTimeout(() => { const rev = !!document.getElementById('reverse-row')?.isConnected; if (rev !== wasRev) { wasRev = rev; fitView([0, 0, 0], fitRadius(), null, true); } }, 50);   // only on entering or leaving REV
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    // Shells: tapping the picture adds the next shell, a shell per tap as in the RCP build (DICTO 2026-10-29)
    meshes: () => (active && view.mode === 'shells' && !view.whole ? shellsGroup.children.filter((c) => c.isMesh) : []),
    handleTap: () => {
      if (!active || view.mode !== 'shells' || view.whole || view.shells >= totalShells()) return false;
      view.shells++; save(); draw(); fit();
      return true;
    },
    /** ?open=whitequeen:<vertex|edge|face|cell>: the Shadow view at that main direction (turning to cell-first, or vertex-first from
     *  cell-first); ?open=whitequeen:slice | :shells those views; ?open=whitequeen:humpty the Slice view at Humpty Dumpty;
     *  ?open=whitequeen:red | :white that queen (as she was left); ?open=whitequeen:redcore the Red Queen's core dodecahedron. */
    setChain(kind) {
      const k = SHORT[kind] ?? kind;
      if (kind === 'red' || kind === 'white') { view.queen = kind; view.stage = kind === 'red' ? 6 : 0; clampToQueen(); }
      else if (STAGE_KEYS.includes(kind)) Object.assign(view, { mode: 'shadow', stage: STAGE_KEYS.indexOf(kind), halves: false });   // ?open=whitequeen:t12 (a stage)
      else if (kind === 'redcore') Object.assign(view, { queen: 'red', stage: 6, mode: 'shells', shells: 1, whole: false });
      else if (kind === 'slice') view.mode = kind;
      else if (kind === 'shells') Object.assign(view, { queen: 'white', stage: 0, mode: 'shells', shells: 1, whole: false });   // the link from Aristotle's Pyramid: the Cleo core
      else if (kind === 'humpty') {
        view.queen = 'white'; view.stage = 0;
        const n = DIRECTIONS.indexOf('cell-first');
        Object.assign(view, { mode: 'slice', sliceDir: 'cell-first', sliceK: SLICE_STOPS[n].findIndex((s) => s.height === WQ_NAMED[0].height) });
      } else if (DIRECTIONS.includes(k)) Object.assign(view, { mode: 'shadow', from: k, to: k === WQ_DEFAULT.to ? WQ_DEFAULT.from : WQ_DEFAULT.to, u: 0 });
      else return;
      save();
      if (active) draw();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      draw(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);   // after the entry has written the menu's title
    },
    resetView() { Object.assign(view, { mode: 'shadow', stage: red() ? 6 : 0, ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0, shells: 1, halves: false, apart: 0, lineUp: false }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, and in it what is shown and its counts. */
    probe: () => {
      if (!shown) return null;
      if (view.mode === 'shells') {
        const k = view.shells - 1;
        return { queen: view.queen, mode: 'shells', rcp: view.rcp, whole: view.whole, wholeKept: view.whole ? wholeKept.slice() : null, shells: view.shells, total: totalShells(), newest: { k, pieces: shellList()[k].cells.length }, colours: Array.from({ length: view.shells }, (_, i) => shellColour(i, totalShells())), radius: shellsRadius };
      }
      if (view.mode === 'slice') {
        const s = shown, nm = red() ? null : namedAt(view.sliceDir, s.stop.height);
        return { queen: view.queen, mode: 'slice', dir: view.sliceDir, k: view.sliceK, stops: M().SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length, height: s.stop.height, atVertex: s.stop.atVertex, tip: s.stop.tip, dim: s.dim,
          V: s.dim === 3 ? s.vertices.length : s.points.length, faceSizes: s.dim === 3 ? faceSizes(s.faces) : null, named: nm?.key ?? null, humpty, spinning: !!raf, spinAngle: spin.rotation.y, quadKinds: s.dim === 3 ? quadKinds(s) : null, lineUp: view.lineUp, axis: view.lineUp ? new THREE.Vector3(...M().SLICE_AXES[DIRECTIONS.indexOf(view.sliceDir)]).applyQuaternion(align.quaternion).toArray() : null };
      }
      if (mid()) return { queen: view.queen, stage: stageKey(), mode: 'shadow', from: view.from, to: view.to, u: view.u, vertices: shown.vertices.length, corners: shown.P.length, edges: shown.edges.length, faceSizes: faceSizes(shown.faces), faces: shown.faces.length, title: document.getElementById('hud-world-title')?.textContent };
      return { queen: view.queen, stage: STAGE_KEYS[view.stage], mode: 'shadow', from: view.from, to: view.to, u: view.u, stop: view.u === 0 ? view.from : view.u === 1000 ? view.to : null, dir: M().viewAt(view.from, view.to, view.u / 1000).u, vertices: shown.vertices.length, triangles: shown.triangles, quads: shown.quads, others: shown.others, faceSizes: faceSizes(shown.faces), faces: shown.faces.length, edges: M().EDGES.length, shell: shell.visible, halves: halvesShown ? { ...halvesShown, apart: view.apart } : null };
    },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the vertex-first shadow. */
export const whiteQueenPreviewPoints = () => shadowAt(0, 0, 0).points;
/** The world's cover in the DICTO menu (DICTO 2026-10-27: the Cleo shells, "absolutely beautiful"): the edges of the gold Cleo core and
 *  of three shells round it in the Shells view's perspective, each edge in its shell's colour (blue → green → yellow); the core is
 *  drawn over the shells and thicker, so it shows at thumbnail size. [[a, b], …] with .colours, .layers, .widths (wireframe-preview.js). */
export const WQ_COVER_SHELLS = [0, 4, 9, 13];
export function whiteQueenPreviewEdges() {
  const seen = new Set(), edges = [], colours = [], layers = [], widths = [];
  for (const k of WQ_COVER_SHELLS) {
    const css = `#${new THREE.Color(shellColour(k)).getHexString()}`;
    for (const ci of CLEO_SHELLS[k].cells) {
      const c = CELLS[ci];
      for (let a = 0; a < 4; a++) for (let b = a + 1; b < 4; b++) {
        const key = c[a] < c[b] ? `${c[a]},${c[b]}` : `${c[b]},${c[a]}`;
        if (seen.has(key)) continue;
        seen.add(key); edges.push([CLEO_POINTS[c[a]], CLEO_POINTS[c[b]]]); colours.push(css); layers.push(k ? 0 : 1); widths.push(k ? 1 : 2);
      }
    }
  }
  Object.assign(edges, { colours, layers, widths });
  return edges;
}
