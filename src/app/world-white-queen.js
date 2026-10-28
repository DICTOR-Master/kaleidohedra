// The White Queen 600-cell (DICTO 2026-10-27): the companion world of paper #63, "The White Queen 600-cell" (DOI not yet assigned).
// Step 2, the shadows: the true orthogonal 3D shadow of the 600-cell, every one computed live from the exact source model
// (white-queen-data.js via white-queen-geometry.js; no other 600-cell code). All 720 edges are drawn projected (the inner ones too),
// the convex hull as a see-through shell, its real faces (coplanar triangles merged) ivory for triangles and blue for four-sided faces,
// as in #63's figures. Six turnings (DICTO 2026-10-27), one for each pair of the four main directions: two rows of four buttons pick
// the start (From) and the end (To), each jumping to its stop, and one big slider turns the 4D view direction along that pair's great
// circle, snapping at both ends; the caption gives the hull's vertices and faces. The Slice view (W3): one row of four directions and
// one big slider from the centre to the tip that stops only at #63's slice patterns (every vertex height and the exact midpoint of
// every gap), each slice computed live; the tips drawn small. Named stops in gold (W4, DICTO's names): Humpty Dumpty, the real
// 48-vertex cell-first slice at 1 + √5/2 (shown larger, solid ivory with gold edges, turning slowly until touched), and Shadow-17,
// the edge-first slice at 1 + √5. Shells (W4b): the 600 cells round one vertex in 15 shells, each one kind of piece, in perspective
// from just beyond the opposite vertex; one slider builds them from the gold Cleo core outwards, the newest shell solid, the inner ones
// see-through, coloured as the study's picture (blue → green → yellow). Halves (W5) in the Shadow view: the front cells (centre·u > 0)
// gold-ivory, the back cells blue, each tiling the shadow once in the main views; a slider pulls the two layers apart along the
// picture's depth (DICTO's Double Vision); side-on cells are flat and left out. Words in all 7 languages (i18n wq.*).
import * as THREE from 'three';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { DIRECTIONS, EDGES, CELLS, shadowAt, viewAt, SLICE_STOPS, sliceAt, CLEO_POINTS, CLEO_SHELLS, halves, quadKind, quadKinds, SLICE_AXES } from './white-queen-geometry.js';

export const WQ_DIRECTIONS = DIRECTIONS;
/** The slider: 0..1000 along the chosen turning, its two ends the stops (it snaps to one within WQ_SNAP). */
export const WQ_SNAP = 40;
export const WQ_DEFAULT = { from: 'vertex-first', to: 'cell-first' };
export const WQ_MODES = ['shadow', 'slice', 'shells'];
export const WQ_SHELLS = CLEO_SHELLS.length;   // 15
export const WQ_CUT = [0.55, 0.45, 1];   // the Whole view's cut: its normal points at the Shells view's starting camera
export const WQ_ARISTOTLE_ACTION = 'tool:aristotleWorld:icosahedron';   // the Cleo-Icos in Aristotle's Pyramid (paper #44)
// the study picture's colours (matplotlib viridis from 0.15 to 0.95), the core gold
const VIRIDIS = [[0, 0x440154], [0.125, 0x482878], [0.25, 0x3e4989], [0.375, 0x31688e], [0.5, 0x26828e], [0.625, 0x1f9e89], [0.75, 0x35b779], [0.875, 0x6ece58], [1, 0xfde725]];
function viridis(x) {
  const i = Math.min(VIRIDIS.length - 2, Math.floor(x * 8)), [a, ca] = VIRIDIS[i], [b, cb] = VIRIDIS[i + 1], f = (x - a) / (b - a);
  return new THREE.Color(ca).lerp(new THREE.Color(cb), f).getHex();
}
export const shellColour = (k) => (k === 0 ? 0xffc857 : viridis(0.15 + (0.8 * k) / (WQ_SHELLS - 1)));
/** The Shells caption at n shells built: the newest shell, its pieces, one kind. */
export function wqShellsCaption(n, L) {
  const k = n - 1, m = CLEO_SHELLS[k].cells.length;
  if (k === 0) return t('wq.shells.core', L);
  return t(k === WQ_SHELLS - 1 ? 'wq.shells.wrap' : 'wq.shells.shell', L, { k, n: m });
}
const FRONT = 0xf6e7bf, BACK = 0x7fa6dc;   // Halves: the front layer gold-ivory, the back layer blue
/** DICTO's named slices (gold captions): direction and exact height. */
export const WQ_NAMED = [{ key: 'humpty', dir: 'cell-first', height: '1 + 1/2√5' }, { key: 'shadow17', dir: 'edge-first', height: '1 + √5' }];
const namedAt = (dir, height) => WQ_NAMED.find((x) => x.dir === dir && x.height === height) ?? null;
/** A slice stop's place on its slider (0..1000, by height from the centre to the tip). */
export const sliceU = (dir, k) => { const S = SLICE_STOPS[DIRECTIONS.indexOf(dir)]; return Math.round((1000 * S[k].value) / S[S.length - 1].value); };
const faceSizes = (faces) => faces.reduce((m, f) => ({ ...m, [f.length]: (m[f.length] ?? 0) + 1 }), {});
/** The slice caption: [name ·] direction · height h · at a vertex height | between heights · counts (or what the tip is). */
export function wqSliceCaption(dir, k, L) {
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
export function wqCaption({ from, to, u }, s, L) {
  const head = u === 0 ? t(`wq.dir.${from}`, L) : u === 1000 ? t(`wq.dir.${to}`, L) : t('wq.between', L, { a: t(`wq.dir.${from}`, L), b: t(`wq.dir.${to}`, L) });
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
  const view = { mode: 'shadow', ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0, shells: 1, halves: false, apart: 0, lineUp: false, whole: false };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (WQ_MODES.includes(d?.mode)) view.mode = d.mode;
    if (DIRECTIONS.includes(d?.from) && DIRECTIONS.includes(d?.to) && d.from !== d.to) Object.assign(view, { from: d.from, to: d.to });
    if (Number.isFinite(d?.u)) view.u = Math.max(0, Math.min(1000, Math.round(d.u)));
    if (DIRECTIONS.includes(d?.sliceDir)) view.sliceDir = d.sliceDir;
    if (Number.isInteger(d?.shells)) view.shells = Math.max(1, Math.min(WQ_SHELLS, d.shells));
    view.halves = d?.halves === true;
    view.lineUp = d?.lineUp === true;
    view.whole = d?.whole === true;
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1000, Math.round(d.apart)));
    if (Number.isInteger(d?.sliceK)) view.sliceK = Math.max(0, Math.min(SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length - 1, d.sliceK));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;

  // ---- the Shadow view ----
  const shadowGroup = new THREE.Group();
  const shellMat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: SHELL, depthWrite: false, roughness: 0.6, metalness: 0, emissive: 0x4e4a40 });
  shellMat.userData.hollow = true;
  const innerMat = new THREE.LineBasicMaterial({ color: 0xb8c2d6, transparent: true, opacity: 0.3, depthWrite: false });   // the inner edges step back so the outline reads
  const hullMat = new THREE.LineBasicMaterial({ color: 0xfff4d6 });
  // fixed buffers, refilled as the slider moves: 720 edges, and the shell (at most 2 × 120 − 4 hull triangles)
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(EDGES.length * 6), 3));
  const inner = new THREE.LineSegments(edgeGeo, innerMat);
  const shellGeo = new THREE.BufferGeometry();
  shellGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  shellGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  shellGeo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(236 * 9), 3));
  const shell = new THREE.Mesh(shellGeo, shellMat);
  shell.renderOrder = 2;
  const hullGeo = new THREE.BufferGeometry();
  hullGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(360 * 6), 3));
  const hullLines = new THREE.LineSegments(hullGeo, hullMat);
  shadowGroup.add(inner, shell, hullLines);
  for (const o of [inner, shell, hullLines]) o.frustumCulled = false;

  // ---- the Slice view: rebuilt per stop, in its own turning group (Humpty Dumpty turns) ----
  // Line up (W7): the align group turns the slice so its direction's main symmetry axis (SLICE_AXES) points at the viewer
  const sliceGroup = new THREE.Group(), align = new THREE.Group(), spin = new THREE.Group();
  sliceGroup.add(align); align.add(spin);
  const Z = new THREE.Vector3(0, 0, 1);
  const applyAlign = () => { if (view.lineUp) align.quaternion.setFromUnitVectors(new THREE.Vector3(...SLICE_AXES[DIRECTIONS.indexOf(view.sliceDir)]), Z); else align.quaternion.identity(); };
  group.add(shadowGroup, sliceGroup);
  const dotGeo = new THREE.SphereGeometry(1, 16, 12);
  let humpty = false, spinStopped = false;
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clearSpin() {
    for (const c of [...spin.children]) { spin.remove(c); if (c.geometry !== dotGeo) c.geometry.dispose(); c.material.dispose(); }
  }
  function drawShadow() {
    const s = shadowAt(view.from, view.to, view.u / 1000);
    shown = s;
    const P = s.P.map((p) => p.map((c) => c * WS)), Q = s.points.map((p) => p.map((c) => c * WS));
    const ep = edgeGeo.attributes.position.array;
    EDGES.forEach(([i, j], k) => { ep.set(P[i], k * 6); ep.set(P[j], k * 6 + 3); });
    edgeGeo.attributes.position.needsUpdate = true;
    const sp = shellGeo.attributes.position.array, sc = shellGeo.attributes.color.array, sn = shellGeo.attributes.normal.array, hp = hullGeo.attributes.position.array;
    const col = new THREE.Color(), a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
    let n = 0, m = 0;
    for (const f of s.faces) {
      col.setHex(f.length === 3 ? IVORY : f.length === 4 ? BLUE : OTHER);
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
    shell.visible = !skeleton;
    shellMat.opacity = SHELL * opacity;
  }
  function drawSlice() {
    clearSpin();
    const s = sliceAt(view.sliceDir, view.sliceK), nm = namedAt(view.sliceDir, s.stop.height);
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
        const hex = f.length === 3 ? IVORY : qk === 'kite' ? ROSE : qk === 'square' ? DEEP_BLUE : f.length === 4 ? BLUE : OTHER;
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
      spin.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: s.dim < 3 ? IVORY : edgeHex })));
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
  /** Cells (indices into CELLS) at points Q as one mesh (4 triangles each) and their edges. */
  function cellsMesh(g, list, Q, hex, { opacity: op = 1, edge = SLICE_EDGE, edgeOpacity = 1, offset = [0, 0, 0], order = 3, glow = GLOW * 0.8, roughness = 0.6, shrink = 1 } = {}) {
    const pos = [], lines = [];
    for (const ci of list) {
      const c = CELLS[ci];
      // shrink < 1: each cell drawn a little smaller about its own centre, so shared faces never coincide (no flicker) and every
      // cell reads as its own piece
      const m = [0, 1, 2].map((i) => c.reduce((a, k) => a + Q[k][i], 0) / c.length);
      const at = (k) => Q[k].map((x, i) => m[i] + shrink * (x - m[i]) + offset[i]);
      for (const [a, b, d] of [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]) pos.push(...at(c[a]), ...at(c[b]), ...at(c[d]));
      for (let a = 0; a < 4; a++) for (let b = a + 1; b < 4; b++) lines.push(...at(c[a]), ...at(c[b]));
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
    const l = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? 0xdfe6f0 : edge, transparent: edgeOpacity < 1, opacity: edgeOpacity, depthWrite: edgeOpacity >= 1 }));
    l.frustumCulled = false; g.add(l);
  }
  let halvesShown = null;
  function drawHalves() {
    clear(halvesGroup);
    const s = shown, h = halves(s.u), P = s.P.map((p) => p.map((c) => c * WS));
    // apart: the two layers move away from each other along the picture's depth (the axis towards the starting camera), up to the
    // shadow's diameter in all
    const off = (view.apart / 1000) * R;
    cellsMesh(halvesGroup, h.front, P, FRONT, { opacity: 0.55, edge: 0xfff4d6, edgeOpacity: 0.7, offset: [0, 0, off], order: 5 });   // the front layer drawn last: on top where they meet
    cellsMesh(halvesGroup, h.back, P, BACK, { opacity: 0.55, edge: 0xcfe0ff, edgeOpacity: 0.7, offset: [0, 0, -off], order: 4 });
    halvesShown = { front: h.front.length, back: h.back.length, side: h.side.length };
  }
  let shellsRadius = 1, wholeKept = [];
  function drawShells() {
    clear(shellsGroup);
    const Q = CLEO_POINTS.map((p) => p.map((c) => c * WS)), n = view.shells;
    if (view.whole) {
      // Whole (DICTO 2026-10-28): all 15 shells at once, cut open like an onion: the half facing the starting camera removed (a cell
      // stays when its centre lies behind the cut through the centre), every shell solid in its own colour, lit (little glow) so the
      // nested shells read in depth
      const cut = new THREE.Vector3(...WQ_CUT).normalize(); wholeKept = [];
      for (let k = 0; k < WQ_SHELLS; k++) {
        const keep = CLEO_SHELLS[k].cells.filter((ci) => { const c = CELLS[ci]; let d = 0; for (const v of c) d += Q[v][0] * cut.x + Q[v][1] * cut.y + Q[v][2] * cut.z; return d < 0; });
        wholeKept.push(keep.length);
        cellsMesh(shellsGroup, keep, Q, shellColour(k), { opacity: 1, edge: 0x1d2027, edgeOpacity: 0.5, glow: 0.12, roughness: 0.45, shrink: 0.94 });
      }
      shellsRadius = Math.max(...Q.map((p) => Math.hypot(...p)).filter(Number.isFinite));
      shown = { shells: WQ_SHELLS, whole: true };
      return;
    }
    // the newest shell solid (a touch see-through, so the gaps of shells 6 and 8 show what is inside), the ones inside it faint
    for (let k = 0; k < n; k++) {
      const newest = k === n - 1;
      cellsMesh(shellsGroup, CLEO_SHELLS[k].cells, Q, shellColour(k), newest ? { opacity: 0.9, edge: 0xf3ead2, edgeOpacity: 0.85, glow: 0.16, roughness: 0.45 } : { opacity: 0.1, edge: 0xffffff, edgeOpacity: 0.12 });
    }
    shellsRadius = Math.max(...CLEO_SHELLS[n - 1].cells.flatMap((c) => CELLS[c]).map((k) => Math.hypot(...Q[k])));
    shown = { shells: n };
  }
  function draw() {
    if (!active) return;
    const halvesOn = view.mode === 'shadow' && view.halves;
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
  const R = 2 * WS;   // the 600-cell's circumradius: every shadow and slice fits inside it
  const fitShadow = () => fitView([0, 0, 0], R * 1.12, [0.3, 0.25, 1]);
  // the Shells view frames the newest shell (they grow from the small core to the outer wrap), zooming in as well as out
  const fit = () => (view.mode === 'slice' && view.lineUp ? fitView([0, 0, 0], R * 1.12, [0, 0, 1], true) : view.mode === 'shells' ? fitView([0, 0, 0], shellsRadius * 1.15, WQ_CUT, true) : view.mode === 'shadow' && view.halves && view.apart ? fitView([0, 0, 0], R * (1.12 + view.apart / 1000), [1, 0.35, 0.55], true) : fitShadow());

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldwhiteQueen-panel';
  panel.className = 'qc-panel';
  const row = (end, label = true) => `<div class="w4d-row w4d-options wq-row" data-wq-row="${end}">${label ? `<span class="hull-pick wq-row-label" data-wq-label="${end}"></span>` : ''}${DIRECTIONS.map((k) => `<button type="button" data-wq-${end}="${k}"></button>`).join('')}</div>`;
  panel.innerHTML = `
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
    <div class="w4d-row w4d-options wq-whole-row"><button type="button" data-wq-whole></button></div>
    <div class="w4d-row wq-shells-row"><label class="hull-pick"><span class="wq-shells-label"></span> <input type="range" class="st-slider" min="1" max="${CLEO_SHELLS.length}" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'whiteQueen');
  const input = panel.querySelector('.wq-param-row input'), sliceInput = panel.querySelector('.wq-slice-row input');
  const apartInput = panel.querySelector('.wq-apart-row input'), shellsInput = panel.querySelector('.wq-shells-row input'), halvesBtn = panel.querySelector('[data-wq-halves]');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold');
  note.addEventListener('click', () => note.classList.toggle('open'));
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), shadow = view.mode === 'shadow', slice = view.mode === 'slice', shells = view.mode === 'shells';
    panel.querySelectorAll('[data-wq-mode]').forEach((x) => { x.textContent = t(`wq.view.${x.dataset.wqMode}`, L); x.classList.toggle('active', x.dataset.wqMode === view.mode); });
    // nothing unnecessary shown: each view only its own rows
    panel.querySelector('[data-wq-row="from"]').hidden = panel.querySelector('[data-wq-row="to"]').hidden = panel.querySelector('.wq-param-row').hidden = !shadow;
    panel.querySelector('[data-wq-row="slice"]').hidden = panel.querySelector('.wq-slice-row').hidden = !slice;
    panel.querySelector('.wq-halves-row').hidden = !shadow;
    panel.querySelector('.wq-apart-row').hidden = !(shadow && view.halves);
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
    panel.querySelector('[data-wq-link]').textContent = t('wq.link.aristotle', L);
    const wb = panel.querySelector('[data-wq-whole]');
    wb.textContent = t('wq.whole', L); wb.classList.toggle('active', view.whole); wb.setAttribute('aria-pressed', String(view.whole));
    panel.querySelector('.wq-whole-row').hidden = !shells;
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
    const nm = slice ? namedAt(view.sliceDir, shown.stop.height) : null;
    caption.classList.toggle('wq-gold', !!nm || (shells && view.shells === 1 && !view.whole));
    if (shadow) {
      panel.querySelector('.wq-param-label').textContent = t('wq.param', L, { a: t(`wq.dir.${view.from}`, L), b: t(`wq.dir.${view.to}`, L) });
      input.value = String(view.u);
      caption.textContent = wqCaption(view, shown, L) + (halvesShown ? ` · ${t('wq.halves.counts', L, { f: halvesShown.front, b: halvesShown.back, s: halvesShown.side })}` : '');
      note.textContent = t(view.halves ? 'wq.note.halves' : 'wq.note', L);
      panel.querySelector('.wq-apart-label').textContent = t('wq.halves.param', L);
      apartInput.value = String(view.apart);
    } else if (shells && view.whole) {
      caption.textContent = t('wq.shells.whole', L);
      note.textContent = t('wq.note.shells', L);
    } else if (shells) {
      panel.querySelector('.wq-shells-label').textContent = t('wq.shells.param', L, { n: view.shells, total: WQ_SHELLS });
      shellsInput.value = String(view.shells);
      caption.textContent = wqShellsCaption(view.shells, L);
      note.textContent = t('wq.note.shells', L);
    } else {
      panel.querySelector('.wq-slice-label').textContent = t('wq.slice.param', L, { d: t(`wq.dir.${view.sliceDir}`, L) });
      sliceInput.value = String(sliceU(view.sliceDir, view.sliceK));
      caption.textContent = wqSliceCaption(view.sliceDir, view.sliceK, L);
      note.textContent = t('wq.note.slice', L);
    }
  }
  const go = (v) => { if (v === view.u) return; view.u = v; save(); draw(); };
  input.addEventListener('input', () => {
    let v = Number(input.value);
    if (v <= WQ_SNAP) v = 0; else if (v >= 1000 - WQ_SNAP) v = 1000;
    input.value = String(v);
    go(v);
  });
  apartInput.addEventListener('input', () => { view.apart = Number(apartInput.value); save(); draw(); });
  apartInput.addEventListener('change', fit);
  panel.querySelector('[data-wq-whole]').addEventListener('click', () => { view.whole = !view.whole; save(); draw(); fit(); });
  shellsInput.addEventListener('input', () => { const n = Number(shellsInput.value); if (n === view.shells) return; view.shells = n; save(); draw(); fit(); });
  // the slice slider stops only at the atlas's stops: the nearest one
  sliceInput.addEventListener('input', () => {
    const v = Number(sliceInput.value), S = SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)];
    let k = 0;
    S.forEach((_, i) => { if (Math.abs(sliceU(view.sliceDir, i) - v) < Math.abs(sliceU(view.sliceDir, k) - v)) k = i; });
    sliceInput.value = String(sliceU(view.sliceDir, k));
    if (k === view.sliceK) return;
    view.sliceK = k; save(); draw();
  });
  // From: the turning starts there (the slider at its start); To: it ends there (the slider at its end). Picking as From the
  // direction that is To swaps the two. Slice: the direction, from its centre.
  panel.addEventListener('click', (e) => {
    if (e.target.closest('[data-wq-link]')) { openAction(WQ_ARISTOTLE_ACTION); return; }
    if (e.target.closest('[data-wq-lineup]')) { view.lineUp = !view.lineUp; if (!view.lineUp) spinStopped = false; save(); draw(); fit(); return; }
    if (e.target.closest('[data-wq-halves]')) { view.halves = !view.halves; save(); draw(); fit(); return; }
    const b = e.target.closest('[data-wq-from], [data-wq-to], [data-wq-slice], [data-wq-mode]');
    if (!b) return;
    const { wqFrom: from, wqTo: to, wqSlice: sl, wqMode: mode } = b.dataset;
    if (mode) { if (mode === view.mode) return; view.mode = mode; save(); draw(); fit(); return; }
    else if (from) { if (from === view.to) view.to = view.from; view.from = from; view.u = 0; }
    else if (to && to !== view.from) { view.to = to; view.u = 1000; }
    else if (sl) { if (sl === view.sliceDir) return; view.sliceDir = sl; view.sliceK = 0; }
    else return;
    save(); draw();
  });
  // the app's projection button (3D → ∥ → ISO → REV): REV adds its slider to this panel, so the picture is framed again above it
  // (only on entering or leaving REV, keeping the view's direction; ∥ and ISO are left alone, ISO being a direction)
  const fitRadius = () => (view.mode === 'shells' ? shellsRadius * 1.15 : view.mode === 'shadow' && view.halves && view.apart ? R * (1.12 + view.apart / 1000) : R * 1.12);
  let wasRev = false;
  document.addEventListener('click', (e) => {
    if (!active || !e.target.closest?.('#projection-toggle')) return;
    setTimeout(() => { const rev = !!document.getElementById('reverse-row')?.isConnected; if (rev !== wasRev) { wasRev = rev; fitView([0, 0, 0], fitRadius(), null, true); } }, 50);   // only on entering or leaving REV
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=whitequeen:<vertex|edge|face|cell>: the Shadow view at that main direction (turning to cell-first, or vertex-first from
     *  cell-first); ?open=whitequeen:slice | :shells those views; ?open=whitequeen:humpty the Slice view at Humpty Dumpty. */
    setChain(kind) {
      const k = SHORT[kind] ?? kind;
      if (kind === 'slice') view.mode = kind;
      else if (kind === 'shells') Object.assign(view, { mode: 'shells', shells: 1 });   // the link from Aristotle's Pyramid: the Cleo core
      else if (kind === 'humpty') {
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
    },
    resetView() { Object.assign(view, { mode: 'shadow', ...WQ_DEFAULT, u: 0, sliceDir: 'vertex-first', sliceK: 0, shells: 1, halves: false, apart: 0, lineUp: false }); save(); if (active) { draw(); fit(); } },
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
        return { mode: 'shells', whole: view.whole, wholeKept: view.whole ? wholeKept.slice() : null, shells: view.shells, newest: { k, pieces: CLEO_SHELLS[k].cells.length }, colours: Array.from({ length: view.shells }, (_, i) => shellColour(i)), radius: shellsRadius };
      }
      if (view.mode === 'slice') {
        const s = shown, nm = namedAt(view.sliceDir, s.stop.height);
        return { mode: 'slice', dir: view.sliceDir, k: view.sliceK, stops: SLICE_STOPS[DIRECTIONS.indexOf(view.sliceDir)].length, height: s.stop.height, atVertex: s.stop.atVertex, tip: s.stop.tip, dim: s.dim,
          V: s.dim === 3 ? s.vertices.length : s.points.length, faceSizes: s.dim === 3 ? faceSizes(s.faces) : null, named: nm?.key ?? null, humpty, spinning: !!raf, spinAngle: spin.rotation.y, quadKinds: s.dim === 3 ? quadKinds(s) : null, lineUp: view.lineUp, axis: view.lineUp ? new THREE.Vector3(...SLICE_AXES[DIRECTIONS.indexOf(view.sliceDir)]).applyQuaternion(align.quaternion).toArray() : null };
      }
      return { mode: 'shadow', from: view.from, to: view.to, u: view.u, stop: view.u === 0 ? view.from : view.u === 1000 ? view.to : null, dir: viewAt(view.from, view.to, view.u / 1000).u, vertices: shown.vertices.length, triangles: shown.triangles, quads: shown.quads, others: shown.others, faces: shown.faces.length, edges: EDGES.length, shell: shell.visible, halves: halvesShown ? { ...halvesShown, apart: view.apart } : null };
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
