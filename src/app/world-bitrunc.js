// The Bitruncated 600-cell (DICTO 2026-11-10; working name, DICTO names it): its own world, the midpoint between the White Queen and
// the Red Queen (the stage t12 of the Queens world, whose stage slider links here), built from the White Queen's exact model by
// bitrunc-geometry.js (queen-stages-geometry.js's corners and edges; nothing built twice). Three views, as the White Queen's:
//   Sweep: the slice by a 3-space at one height along one of five directions (the White Queen's four main ones and one generic one),
//     its surface tiled by the cells' cross-sections, truncated icosahedra ivory and truncated tetrahedra blue. One big slider stops at
//     every corner height and at the exact middle of every gap; at a corner the cells that let go (rose) and those that meet (green)
//     are lit: along the generic direction each corner is one cell appearing, one disappearing, or one scutoid swap (two let go, two
//     meet), 716, 716 and 2166. Play runs the sweep.
//   Shadow: the true 3D shadow, its 3600 corners and 7200 edges and the see-through hull, turned along the six turnings between the
//     four main directions (From, To, one big slider), as in the Queens world.
//   Shells: the 720 cells in shells by graph distance from one truncated icosahedron (the gold core), in perspective from just beyond
//     the opposite one, so the core is drawn undistorted at its true size; one slider builds them outwards, the newest solid, the inner
//     ones see-through; Whole shows them all at once, cut open like an onion. In Shells and Cut open one big slider pulls the cells
//     apart: each moves rigidly out along the line from the centre through its own centre, the camera keeping them all in view.
//     RCP view, RCP v4 and Sectors (DICTO 2026-11-11, "we didn't put RCP/RCP 4 and sectors buttons on new apps"), as in the Queens
//     world's Shells: the same shells drawn with the RCP build's own perspective (the eye on the core's side) or DICTO's RCP v4 (the
//     eye beyond the far side, the core at its true size); Sectors cuts every drawn cell by the planes through the core's axis over
//     the core truncated icosahedron's 32 faces, so the whole falls apart into 32 sectors (12 over its pentagons, 20 over its
//     hexagons), each pulled out along its own axis by its own big slider (queen-sectors.js, dicto-rcp.js: the Queens world's code).
// Words in all 7 languages (i18n bt.*, and the Queens world's wq.* where the words are the same).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { shellColour } from './world-white-queen.js';
import * as BT from './bitrunc-geometry.js';
import { STAGE_FACTS } from './queen-stages-geometry.js';
import { farEyePoints, seedEyePoints } from './dicto-rcp.js';
import { conesOverFaces, cellWedges } from './queen-sectors.js';

export const BT_TITLE = 'Bitruncated 600-cell';   // working name (DICTO renames)
export const BT_MODES = ['sweep', 'shadow', 'shells'];
export const BT_DIRECTIONS = BT.DIRECTIONS;                  // the sweep's five
export const BT_MAIN = BT.DIRECTIONS.slice(0, 4);            // the shadow's four
export const BT_DEFAULT = { from: 'vertex-first', to: 'cell-first' };
export const BT_SNAP = 40;
export const BT_CUT = [0.55, 0.45, 1];   // Whole: the cut's normal points at the Shells view's camera, as the White Queen's
/** The number of shells (6), from the model (built on first use). */
export const btShells = () => BT.model().SHELLS.length;
const TI_HEX = 0xefe9dc, TT_HEX = 0x9fb4c8;     // the Queens world's ivory and blue
const LET_GO = 0xd98fa6, MEET = 0x47b07f;        // the swap: the pair letting go rose, the pair meeting green
const EDGE = 0x3a3f4a, EDGE_DARK = 0x1d2027, GLOW = 0.3, SHELL = 0.42;
const IVORY = 0xefe9dc, BLUE = 0x9fb4c8, OTHER = 0xd8c690;
const SIDED = { 5: 0xc8504a, 6: 0xd9a441, 7: 0x7fae7a, 8: 0x8b78c4, 9: 0x4fa3a5, 10: 0xd07fb0 };   // the Queens world's shadow faces, by sides
const SHORT = { vertex: 'vertex-first', edge: 'edge-first', face: 'face-first', cell: 'cell-first' };
const lang = () => getSettings().language;
/** Pull apart at full (1000): every cell's centre twice as far from the centre as closed (the cells themselves unchanged). */
export const BT_PULL = 1;

// the Shells picture, made on first use: the corners in perspective, each cell's centre, and the far truncated icosahedron's shell
// (opposite the core), which wraps all the others in this perspective
let shellData = null;
export function btShellsModel() {
  if (shellData) return shellData;
  const M = BT.model(), SQ = M.SHELL_POINTS.map((p) => p.map((c) => c * WS));
  const CENTRES = M.CELLS.map((c) => [0, 1, 2].map((i) => c.corners.reduce((a, k) => a + SQ[k][i], 0) / c.corners.length));
  const farTI = M.CELLS.findIndex((c) => c.kind === 'TI' && c.corners.every((k) => M.CORNERS[k][0] < -M.CORE_HEIGHT + 1e-9));
  shellData = { M, SQ, CENTRES, farTI, FAR: M.SHELLS.findIndex((list) => list.includes(farTI)) };
  return shellData;
}
// The Shells view's three pictures, as the Queens world's (DICTO 2026-11-11): 'shells' (from just beyond the opposite truncated
// icosahedron), 'rcp' (the RCP build's perspective, the eye at 5 × the radius on the core's side, krp-core rcpBuild.js) and 'dictoRcp'
// (RCP v4: the eye as far beyond the far side, then scaled so the core is at its true size). The axis through the core is the first
// coordinate (the core round the White Queen's vertex (2, 0, 0, 0)), the picture's frame the Shells view's (BT.FRAMES[0]).
export const BT_PICTURES = ['shells', 'rcp', 'dictoRcp'];
const RCP_MARGIN = 5;
const pictures = {};
/** A picture's corners (world units) and each cell's centre in it: { SQ, CENTRES }. */
export function btPicture(key = 'shells') {
  if (key === 'shells') { const { SQ, CENTRES } = btShellsModel(); return { SQ, CENTRES }; }
  if (!pictures[key]) {
    const M = BT.model(), F = BT.FRAMES[0];
    const P = key === 'rcp' ? seedEyePoints(M.CORNERS, 2, F, RCP_MARGIN) : farEyePoints(M.CORNERS, 2, [M.CELLS[M.CORE].corners], F, RCP_MARGIN);
    const SQ = P.map((p) => p.map((c) => c * WS));
    pictures[key] = { SQ, CENTRES: M.CELLS.map((c) => [0, 1, 2].map((i) => c.corners.reduce((a, k) => a + SQ[k][i], 0) / c.corners.length)) };
  }
  return pictures[key];
}
/** Pulled apart by a (0…1000): the shift of cell ci, along the line from the centre (the core's centre, the picture's origin)
 *  through its own centre, a/1000 × BT_PULL × that distance; the core and the far truncated icosahedron, centred there, stay. */
export const btApartShift = (ci, a, key = 'shells') => btPicture(key).CENTRES[ci].map((x) => (x * BT_PULL * a) / 1000);
/** The farthest any corner of the cells in list reaches from the centre, pulled apart by a. */
export function btApartRadius(list, a, key = 'shells') {
  const M = BT.model(), { SQ } = btPicture(key);
  let r = 0;
  for (const ci of list) { const s = btApartShift(ci, a, key); for (const k of M.CELLS[ci].corners) r = Math.max(r, Math.hypot(SQ[k][0] + s[0], SQ[k][1] + s[1], SQ[k][2] + s[2])); }
  return r;
}
// Sectors (as the Queens world's, queen-sectors.js): the cones from the centre over the core truncated icosahedron's 32 faces (its
// corners across the axis, the frame of every picture); in every picture a corner x is drawn at (frame · x) / f(x₀) with f > 0, so
// each cone's planes are the same planes through the centre in all three
export const BT_SECTORS = 32;
let cones = null;
export function btSectorCones() {
  if (cones) return cones;
  const M = BT.model(), F = BT.FRAMES[0], across = (x) => F.map((f) => f.reduce((s, c, i) => s + c * x[i], 0));
  cones = conesOverFaces(M.CELL_FACES[M.CORE].map((fi) => M.FACES[fi].loop.map((k) => across(M.CORNERS[k]))));
  return cones;
}
/** Cell ci in picture key cut into its wedges: [{ sector, faces (3D loops, world units) }]. */
export function btCellWedges(ci, key = 'shells') {
  const M = BT.model(), { SQ } = btPicture(key);
  return cellWedges(M.CELL_FACES[ci].map((fi) => M.FACES[fi].loop.map((k) => SQ[k])), btSectorCones());
}
/** Sectors pulled apart at full (1000): each sector moves out along its axis by half the radius of what is drawn (as the Queens world). */
export const BT_SECTOR_PULL = 0.5;

export const dirName = (d, L) => t(d === 'generic' ? 'bt.dir.generic' : `wq.dir.${d}`, L);
const btnName = (d, L) => t(d === 'generic' ? 'bt.btn.generic' : `wq.btn.${d}`, L);
/** The stop of a sweep nearest the middle that is a swap (the world opens there). */
export function middleSwap(dir) {
  const sw = BT.sweep(dir), mid = Math.floor(sw.stops.length / 2);
  let best = mid, bd = Infinity;
  sw.stops.forEach((s, k) => { if (s.level !== undefined && sw.events[s.level].letGo.length && Math.abs(k - mid) < bd) { bd = Math.abs(k - mid); best = k; } });
  return best;
}
/** What happens at a corner height, in words: a single scutoid swap, or the batch's parts. */
function eventWords(e, total, L) {
  if (e.letGo.length === 1 && e.meet.length === 1 && !e.born.length && !e.died.length) return [t('bt.swap.one', L, { k: e.swapFrom + 1, n: total })];
  const out = [];
  if (e.letGo.length) out.push(e.letGo.length === 1 ? t('bt.swap.at', L, { k: e.swapFrom + 1, n: total }) : t('bt.swaps.range', L, { a: e.swapFrom + 1, b: e.swapFrom + e.letGo.length, n: total }));
  if (e.letGo.length) out.push(e.letGo.length === 1 ? t('bt.event.letGo.one', L) : t('bt.event.letGo', L, { n: e.letGo.length }));
  if (e.meet.length) out.push(e.meet.length === 1 ? t('bt.event.meet.one', L) : t('bt.event.meet', L, { n: e.meet.length }));
  if (e.born.length) out.push(e.born.length === 1 ? t('bt.event.born.one', L) : t('bt.event.born', L, { n: e.born.length }));
  if (e.died.length) out.push(e.died.length === 1 ? t('bt.event.died.one', L) : t('bt.event.died', L, { n: e.died.length }));
  return out;
}
/** The Sweep caption at stop k of direction dir. */
export function btSweepCaption(dir, k, L) {
  const sw = BT.sweep(dir), s = BT.sliceAt(dir, k), st = s.stop, parts = [dirName(dir, L)];
  if (st.level !== undefined) {
    const last = sw.levels.length - 1;
    if (st.level === 0) parts.push(t('bt.sweep.start', L));
    else if (st.level === last) parts.push(t('bt.sweep.end', L));
    else parts.push(...eventWords(sw.events[st.level], sw.totals.letGo, L));
    parts.push(t('bt.sweep.corner', L, { k: st.level + 1, n: sw.levels.length }));
  } else parts.push(t('bt.sweep.gap', L, { k: st.gap + 1, n: sw.levels.length - 1 }));
  if (s.cells.length) parts.push(t('bt.count.cells', L, { n: s.cells.length, a: s.ti, b: s.tt }));
  return parts.join(' · ');
}
/** The Shadow caption: the direction at a stop (or "from → to"), the cells, and the hull's corners and faces by sides. */
export function btShadowCaption({ from, to, u }, s, L) {
  const head = u === 0 ? t(`wq.dir.${from}`, L) : u === 1000 ? t(`wq.dir.${to}`, L) : t('wq.between', L, { a: t(`wq.dir.${from}`, L), b: t(`wq.dir.${to}`, L) });
  const sizes = s.faces.reduce((m, f) => ({ ...m, [f.length]: (m[f.length] ?? 0) + 1 }), {});
  const sided = Object.entries(sizes).map(([k, n]) => (k === '3' ? t('wq.count.triangles', L, { n }) : k === '4' ? t('wq.count.quads', L, { n }) : t('rq.count.sided', L, { n, k })));
  return [head, t('wq.stage.t12.cells', L), t('wq.count.vertices', L, { n: s.vertices.length }), ...sided].join(' · ');
}
const kinds = (list) => { const a = list.filter((c) => c < BT.TI_COUNT).length; return { a, b: list.length - a }; };
/** The Shells caption at n shells built. */
export function btShellsCaption(n, L) {
  const k = n - 1, list = BT.model().SHELLS[k];
  if (k === 0) return t('bt.shells.core', L);
  return t(k === btShells() - 1 ? 'bt.shells.last' : 'bt.shells.shell', L, { k, n: list.length, ...kinds(list) });
}

export function createBitruncWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('bitrunc');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // k: the sweep's stop; −1 until first drawn (then the swap nearest the middle), so nothing is built while the app starts
  const view = { mode: 'sweep', dir: 'generic', k: -1, ...BT_DEFAULT, u: 0, shells: 1, whole: false, apart: 0, rcp: false, dictoRcp: false, sectors: false, sectorsApart: 0 };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (BT_MODES.includes(d?.mode)) view.mode = d.mode;
    if (BT_DIRECTIONS.includes(d?.dir)) view.dir = d.dir;
    if (Number.isInteger(d?.k) && d.k >= 0) view.k = d.k;   // kept to the direction's stops when drawn
    if (BT_MAIN.includes(d?.from) && BT_MAIN.includes(d?.to) && d.from !== d.to) Object.assign(view, { from: d.from, to: d.to });
    if (Number.isFinite(d?.u)) view.u = Math.max(0, Math.min(1000, Math.round(d.u)));
    if (Number.isInteger(d?.shells)) view.shells = Math.max(1, d.shells);   // at most the number of shells: kept to it when drawn
    view.whole = d?.whole === true;
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1000, Math.round(d.apart)));
    view.rcp = d?.rcp === true;
    view.dictoRcp = d?.dictoRcp === true && !view.rcp;   // one perspective at a time
    view.sectors = d?.sectors === true;
    if (Number.isFinite(d?.sectorsApart)) view.sectorsApart = Math.max(0, Math.min(1000, Math.round(d.sectorsApart)));
  } catch { /* defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null, playing = false, lit = null;
  const rad = () => 2 * WS;

  // Render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, antialiased screen-space edges, no milky wash
  const fat = (color, width, op = 1) => { const l = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color, linewidth: width, transparent: op < 1, opacity: op, depthWrite: op >= 1 })); l.frustumCulled = false; return l; };
  const sweepGroup = new THREE.Group(), shadowGroup = new THREE.Group(), shellsGroup = new THREE.Group();
  group.add(sweepGroup, shadowGroup, shellsGroup);
  const clear = (g) => { for (const c of [...g.children]) { g.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  /** Triangles (flat positions) and edges (flat segment ends) as one mesh in one colour and its crisp edges. */
  function meshFrom(g, pos, lines, hex, { opacity: op = 1, edge = EDGE, edgeOpacity = 1, order = 3, glow = GLOW, roughness = 0.55, width = 1.6 } = {}) {
    const see = op < 1;
    if (!skeleton && pos.length) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      geo.computeVertexNormals();
      const mat = new THREE.MeshStandardMaterial({ color: hex, side: THREE.DoubleSide, flatShading: true, roughness, emissive: new THREE.Color(hex).multiplyScalar(glow), transparent: see, opacity: op, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
      if (see) mat.userData.hollow = true;
      const m = new THREE.Mesh(geo, mat); m.frustumCulled = false; if (see) m.renderOrder = order; g.add(m);
    }
    if (lines.length) { const l = fat(skeleton ? 0xdfe6f0 : edge, width, edgeOpacity); l.geometry.setPositions(lines); g.add(l); }
  }
  const fan = (P, pos) => { for (let i = 1; i + 1 < P.length; i++) pos.push(...P[0], ...P[i], ...P[i + 1]); };
  const ring = (P, lines) => P.forEach((p, i) => lines.push(...p, ...P[(i + 1) % P.length]));

  // ---- Sweep ----
  function drawSweep() {
    clear(sweepGroup);
    const nStops = BT.sweep(view.dir).stops.length;
    if (view.k < 0 || view.k >= nStops) view.k = middleSwap(view.dir);
    const s = BT.sliceAt(view.dir, view.k), e = s.event, sw = BT.sweep(view.dir);
    shown = s;
    const inner = e && s.stop.level > 0 && s.stop.level < sw.levels.length - 1;
    const letGo = new Set(inner ? e.letGo.flat() : []), meet = new Set(inner ? e.meet.flat() : []);
    lit = { letGo: [...letGo], meet: [...meet] };
    const buckets = new Map([[TI_HEX, []], [TT_HEX, []], [LET_GO, []], [MEET, []]]), lines = [];
    const see = opacity < 1;
    for (const c of s.cells) {
      const P = c.points.map((p) => p.map((x) => x * WS));
      // a cell both letting go and meeting (in a batch) shows as letting go
      const hex = letGo.has(c.cell) ? LET_GO : meet.has(c.cell) ? MEET : c.kind === 'TI' ? TI_HEX : TT_HEX;
      fan(P, buckets.get(hex)); ring(P, lines);
    }
    for (const [hex, pos] of buckets) meshFrom(sweepGroup, pos, [], hex, { opacity: see ? opacity : 1, glow: hex === LET_GO || hex === MEET ? 0.42 : GLOW });
    meshFrom(sweepGroup, [], lines, 0, { edge: EDGE, width: 1.6 });
  }
  // Play: the sweep runs from where it is to the top (from the bottom when it is at the top), the whole way in about 45 s along the
  // generic direction, slower along the main ones (fewer stops); any slider touch or button stops it
  let raf = 0, last = 0, carry = 0;
  const rate = () => Math.max(5, BT.sweep(view.dir).stops.length / 45);
  function play(on) {
    playing = on;
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    if (!on) { save(); renderPanel(); return; }
    const n = BT.sweep(view.dir).stops.length;
    if (view.k >= n - 1) view.k = 0;
    last = performance.now(); carry = 0;
    const step = (now) => {
      raf = 0;
      if (!active || !playing || view.mode !== 'sweep') { playing = false; renderPanel(); return; }
      carry += ((now - last) / 1000) * rate(); last = now;
      const adv = Math.floor(carry);
      if (adv > 0) { carry -= adv; view.k = Math.min(n - 1, view.k + adv); draw(); }
      if (view.k >= n - 1) { playing = false; save(); renderPanel(); return; }
      raf = requestAnimationFrame(step);
    };
    renderPanel();
    raf = requestAnimationFrame(step);
  }

  // ---- Shadow (as the Queens world's stages) ----
  const shellMat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: SHELL, depthWrite: false, roughness: 0.5, metalness: 0, emissive: 0x16140f, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  shellMat.userData.hollow = true;
  const shellGeo = new THREE.BufferGeometry();
  const MAXT = 2 * STAGE_FACTS[BT.STAGE].V;   // hull triangles of 3600 points: at most 2n − 4
  shellGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXT * 9), 3));
  shellGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(MAXT * 9), 3));
  shellGeo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(MAXT * 9), 3));
  const shell = new THREE.Mesh(shellGeo, shellMat);
  shell.renderOrder = 2; shell.frustumCulled = false;
  const edgeArr = new Float32Array(STAGE_FACTS[BT.STAGE].E * 6), hullArr = new Float32Array(MAXT * 9);
  const fatInner = fat(0xb8c2d6, 1.2, 0.5), fatHull = fat(0xfff4d6, 2.4);
  fatInner.renderOrder = 1; fatHull.renderOrder = 3;
  shadowGroup.add(fatInner, shell, fatHull);
  const setFat = (l, arr, count) => { l.geometry.dispose(); l.geometry = new LineSegmentsGeometry(); if (count > 0) l.geometry.setPositions(arr.subarray(0, count)); l.visible = count > 0; };
  function drawShadow() {
    const s = BT.stageShadowAt(BT.STAGE, view.from, view.to, view.u / 1000);
    shown = s;
    const P = s.P.map((p) => p.map((c) => c * WS)), Q = s.points.map((p) => p.map((c) => c * WS));
    s.edges.forEach(([i, j], k) => { edgeArr.set(P[i], k * 6); edgeArr.set(P[j], k * 6 + 3); });
    setFat(fatInner, edgeArr, s.edges.length * 6);
    const sp = shellGeo.attributes.position.array, sc = shellGeo.attributes.color.array, sn = shellGeo.attributes.normal.array;
    const col = new THREE.Color(), a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
    let n = 0, m = 0;
    for (const f of s.faces) {
      col.setHex(f.length === 3 ? IVORY : f.length === 4 ? BLUE : SIDED[f.length] ?? OTHER);
      a.fromArray(Q[f[0]]); b.fromArray(Q[f[1]]).sub(a); c.fromArray(Q[f[2]]).sub(a);
      const nrm = b.cross(c).normalize();
      for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { sp.set(Q[k], n * 3); sc.set([col.r, col.g, col.b], n * 3); sn.set([nrm.x, nrm.y, nrm.z], n * 3); n++; }
      f.forEach((k, i) => { const l = f[(i + 1) % f.length]; if (k < l) { hullArr.set(Q[k], m * 3); hullArr.set(Q[l], m * 3 + 3); m += 2; } });
    }
    shellGeo.setDrawRange(0, n);
    for (const x of ['position', 'color', 'normal']) shellGeo.attributes[x].needsUpdate = true;
    setFat(fatHull, hullArr, m * 3);
    shell.visible = !skeleton;
    const solid = opacity >= 1;
    if (shellMat.transparent === solid) { shellMat.transparent = !solid; shellMat.depthWrite = solid; shellMat.needsUpdate = true; }
    shellMat.opacity = solid ? 1 : SHELL * opacity;
  }

  // ---- Shells ----
  const shellsModel = btShellsModel;
  let drawnCells = [];
  // the picture drawn (the Shells perspective, RCP view or RCP v4); with Sectors on the sectors are the pieces, pulled by their own
  // slider, and the cells' Pull apart rests (its slider hidden, its value kept)
  const pic = () => (view.rcp ? 'rcp' : view.dictoRcp ? 'dictoRcp' : 'shells');
  const cellApart = () => (view.sectors ? 0 : view.apart);
  let sectorsShown = null, sectorPull = 0;
  const wedgeCache = new Map();   // by picture, then cell: each cell's wedges, cut once
  const wedgesOf = (ci) => { const key = pic(); if (!wedgeCache.has(key)) wedgeCache.set(key, new Map()); const m = wedgeCache.get(key); if (!m.has(ci)) m.set(ci, btCellWedges(ci, key)); return m.get(ci); };
  /** Cells as one mesh, each drawn a little smaller about its own centre (shrink) so shared faces never coincide, and moved out
   *  rigidly by Pull apart (btApartShift); with Sectors on, each cell's wedges, each moved out along its sector's axis. */
  function cellsMesh(list, hex, { shrink = 1, ...opts } = {}) {
    const M = BT.model(), key = pic(), { SQ, CENTRES } = btPicture(key), a = cellApart(), pos = [], lines = [];
    if (view.sectors) {
      const C = btSectorCones();
      for (const ci of list) {
        const W = wedgesOf(ci);
        sectorsShown.wedges += W.length;
        for (const w of W) {
          const o = C[w.sector].axis.map((x) => x * sectorPull), all = w.faces.flat(), m = [0, 1, 2].map((i) => all.reduce((s, p) => s + p[i], 0) / all.length);
          const at = (p) => p.map((x, i) => m[i] + shrink * (x - m[i]) + o[i]);
          for (const f of w.faces) { const P = f.map(at); fan(P, pos); ring(P, lines); }
        }
        drawnCells.push(ci);
      }
      meshFrom(shellsGroup, pos, lines, hex, opts);
      return;
    }
    for (const ci of list) {
      const m = CENTRES[ci], s = btApartShift(ci, a, key), at = (k) => SQ[k].map((x, i) => m[i] + shrink * (x - m[i]) + s[i]);
      for (const fi of M.CELL_FACES[ci]) { const P = M.FACES[fi].loop.map(at); fan(P, pos); ring(P, lines); }
      drawnCells.push(ci);
    }
    meshFrom(shellsGroup, pos, lines, hex, opts);
  }
  let shellsRadius = 1, wholeKept = [];
  const radiusOf = (list, a = cellApart()) => btApartRadius(list, a, pic());
  function drawShells() {
    clear(shellsGroup);
    drawnCells = [];
    const { M, FAR, farTI } = shellsModel(), { CENTRES } = btPicture(pic()), SH = M.SHELLS, N = SH.length;
    // the far truncated icosahedron wraps all the others only in the Shells perspective (as the Red Queen's far dodecahedron); in the
    // RCP pictures the eye is far off and nothing wraps
    const wrapping = pic() === 'shells';
    view.shells = Math.min(view.shells, N);
    // Sectors pulled apart: each moves out along its own axis, by up to BT_SECTOR_PULL × the radius of what is drawn closed
    const R0 = view.whole ? radiusOf(wrapping ? SH[Math.max(0, FAR - 1)] : SH.flat(), 0) : radiusOf(SH[view.shells - 1], 0);
    sectorPull = view.sectors ? (view.sectorsApart / 1000) * BT_SECTOR_PULL * R0 : 0;
    sectorsShown = view.sectors ? { count: BT_SECTORS, wedges: 0, apart: view.sectorsApart } : null;
    if (view.whole) {
      // all the shells at once, cut open: a cell stays when its centre lies behind the cut through the centre; the shell holding the
      // far truncated icosahedron wraps all the others in this perspective, so it stays whole and see-through
      const cut = new THREE.Vector3(...BT_CUT).normalize();
      wholeKept = [];
      for (let k = 0; k < N; k++) {
        const wrap = wrapping && k === FAR, keep = wrap ? SH[k] : SH[k].filter((ci) => CENTRES[ci][0] * cut.x + CENTRES[ci][1] * cut.y + CENTRES[ci][2] * cut.z < 0);
        wholeKept.push(keep.length);
        cellsMesh(keep, shellColour(k, N), wrap ? { opacity: 0.08, edge: 0xffffff, edgeOpacity: 0.25 } : { opacity: 1, edge: view.sectors ? EDGE_DARK : 0x1d2027, edgeOpacity: view.sectors ? 1 : 0.55, glow: 0.12, roughness: 0.45, shrink: 0.94 });
      }
      // the camera's radius: closed, the shell inside the wrapping one (as before); pulled apart, whatever is drawn reaches farthest
      shellsRadius = view.sectors ? R0 + sectorPull : Math.max(R0, cellApart() ? radiusOf(drawnCells) : 0);
      shown = { whole: true };
      return;
    }
    // the inner shells faint in their shell's colour; the newest solid, each cell in its kind's colour (truncated icosahedra ivory,
    // truncated tetrahedra blue, as in the Sweep) with crisp dark edges, so every cell reads as its own piece
    const n = view.shells;
    for (let k = 0; k < n - 1; k++) cellsMesh(SH[k], shellColour(k, N), { opacity: 0.1, edge: 0xffffff, edgeOpacity: 0.12, shrink: 0.97 });
    // the far truncated icosahedron wraps all the others in this perspective: in the last shell it stays see-through, so the shell's
    // other cells and everything inside show
    const newest = SH[n - 1].filter((c) => !wrapping || c !== farTI), solid = { opacity: 1, edge: EDGE_DARK, edgeOpacity: 1, glow: 0.14, roughness: 0.5, shrink: 0.97, width: 2 };
    if (wrapping && SH[n - 1].includes(farTI)) cellsMesh([farTI], TI_HEX, { opacity: 0.08, edge: 0xffffff, edgeOpacity: 0.3 });
    cellsMesh(newest.filter((c) => c < BT.TI_COUNT), TI_HEX, solid);
    cellsMesh(newest.filter((c) => c >= BT.TI_COUNT), TT_HEX, solid);
    shellsRadius = view.sectors ? R0 + sectorPull : Math.max(R0, cellApart() ? radiusOf(drawnCells) : 0);
    shown = { shells: n };
  }

  function draw() {
    if (!active) return;
    sweepGroup.visible = view.mode === 'sweep';
    shadowGroup.visible = view.mode === 'shadow';
    shellsGroup.visible = view.mode === 'shells';
    if (view.mode !== 'sweep') { clear(sweepGroup); lit = null; }
    if (view.mode !== 'shells') clear(shellsGroup);
    if (view.mode === 'sweep') drawSweep(); else if (view.mode === 'shadow') drawShadow(); else drawShells();
    renderPanel();
  }
  const fitRadius = () => (view.mode === 'shells' ? shellsRadius * 1.15 : rad() * 1.12);
  const fit = () => (view.mode === 'shells' ? fitView([0, 0, 0], fitRadius(), BT_CUT, true) : fitView([0, 0, 0], fitRadius(), [0.3, 0.25, 1], true));

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldbitrunc-panel';
  panel.className = 'qc-panel';
  const dirRow = (end) => `<div class="w4d-row w4d-options bt-row" data-bt-row="${end}"><span class="hull-pick bt-row-label" data-bt-label="${end}"></span>${BT_MAIN.map((k) => `<button type="button" data-bt-${end}="${k}"></button>`).join('')}</div>`;
  panel.innerHTML = `
    <div class="w4d-row w4d-options bt-modes">${BT_MODES.map((m) => `<button type="button" data-bt-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options bt-row" data-bt-row="dir">${BT_DIRECTIONS.map((k) => `<button type="button" data-bt-dir="${k}"></button>`).join('')}</div>
    ${dirRow('from')}
    ${dirRow('to')}
    <div class="w4d-row w4d-options bt-play-row"><button type="button" data-bt-play></button></div>
    <div class="w4d-row w4d-options bt-whole-row"><button type="button" data-bt-whole></button><button type="button" data-bt-rcp></button><button type="button" data-bt-dicto-rcp></button><button type="button" data-bt-sectors></button></div>
    <div class="w4d-row st-note bt-legend"></div>
    <div class="w4d-row bt-sweep-row"><label class="hull-pick"><span class="bt-sweep-label"></span> <input type="range" class="st-slider" min="0" max="1" step="1"></label></div>
    <div class="w4d-row bt-param-row"><label class="hull-pick"><span class="bt-param-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row bt-shells-row"><label class="hull-pick"><span class="bt-shells-label"></span> <input type="range" class="st-slider" min="1" max="1" step="1"></label></div>
    <div class="w4d-row bt-apart-row"><label class="hull-pick"><span class="bt-apart-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row bt-sectors-row"><label class="hull-pick"><span class="bt-sectors-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row st-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'bitrunc');
  const sweepInput = panel.querySelector('.bt-sweep-row input'), input = panel.querySelector('.bt-param-row input'), shellsInput = panel.querySelector('.bt-shells-row input'), apartInput = panel.querySelector('.bt-apart-row input');
  const sectorsInput = panel.querySelector('.bt-sectors-row input');
  const caption = panel.querySelector('.ch-param-caption'), note = panel.querySelector('.st-note.fold'), legend = panel.querySelector('.bt-legend');
  note.addEventListener('click', () => note.classList.toggle('open'));
  const press = (x, on) => { x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), sweepOn = view.mode === 'sweep', shadow = view.mode === 'shadow', shells = view.mode === 'shells';
    panel.querySelectorAll('[data-bt-mode]').forEach((x) => { x.textContent = t(x.dataset.btMode === 'sweep' ? 'bt.view.sweep' : `wq.view.${x.dataset.btMode}`, L); press(x, x.dataset.btMode === view.mode); });
    // nothing unnecessary shown: each view only its own rows
    panel.querySelector('[data-bt-row="dir"]').hidden = panel.querySelector('.bt-sweep-row').hidden = panel.querySelector('.bt-play-row').hidden = !sweepOn;
    panel.querySelector('[data-bt-row="from"]').hidden = panel.querySelector('[data-bt-row="to"]').hidden = panel.querySelector('.bt-param-row').hidden = !shadow;
    panel.querySelector('.bt-whole-row').hidden = !shells;
    panel.querySelector('.bt-shells-row').hidden = !shells || view.whole;
    panel.querySelector('.bt-apart-row').hidden = !shells || view.sectors;   // Shells and Cut open; with Sectors on, the sectors' own slider
    panel.querySelector('.bt-sectors-row').hidden = !(shells && view.sectors);
    panel.querySelectorAll('[data-bt-dir]').forEach((x) => { const k = x.dataset.btDir; x.textContent = btnName(k, L); x.title = dirName(k, L); press(x, k === view.dir); });
    for (const end of ['from', 'to']) {
      panel.querySelector(`[data-bt-label="${end}"]`).textContent = t(`wq.${end}`, L);
      panel.querySelectorAll(`[data-bt-${end}]`).forEach((x) => {
        const k = x.getAttribute(`data-bt-${end}`);
        x.textContent = t(`wq.btn.${k}`, L); x.title = t(`wq.dir.${k}`, L);
        x.classList.toggle('active', k === view[end]);
        x.hidden = end === 'to' && k === view.from;   // a direction does not turn to itself
      });
    }
    const pb = panel.querySelector('[data-bt-play]');
    pb.textContent = t(playing ? 'bt.pause' : 'bt.play', L); press(pb, playing);
    const wb = panel.querySelector('[data-bt-whole]');
    wb.textContent = t('wq.whole', L); press(wb, view.whole);
    // RCP view, RCP v4 and Sectors: the Queens world's buttons and words
    const rb = panel.querySelector('[data-bt-rcp]'), db = panel.querySelector('[data-bt-dicto-rcp]'), sb = panel.querySelector('[data-bt-sectors]');
    rb.textContent = t('wq.rcp', L); press(rb, view.rcp);
    db.textContent = t('wq.dictoRcp', L); press(db, view.dictoRcp);
    sb.textContent = t('wq.sectors', L); sb.title = t('bt.sectors.tip', L); press(sb, view.sectors);
    // the legend: the two kinds of cell (Sweep, and the newest shell in Shells), and in the Sweep the swap's two colours
    legend.hidden = !(sweepOn || (shells && !view.whole));
    if (shells && !view.whole) {
      const sw = (hex, key) => `<span class="bt-sw"><i style="background:#${new THREE.Color(hex).getHexString()}"></i>${t(key, L)}</span>`;
      legend.innerHTML = [sw(TI_HEX, 'bt.legend.ti'), sw(TT_HEX, 'bt.legend.tt')].join('');
    }
    if (sweepOn) {
      // the swap's two swatches keep their room when no swap is shown (hidden, not removed), so nothing jumps while the sweep plays
      const sw = (hex, key, on = true) => `<span class="bt-sw${on ? '' : ' bt-off'}"><i style="background:#${new THREE.Color(hex).getHexString()}"></i>${t(key, L)}</span>`;
      legend.innerHTML = [sw(TI_HEX, 'bt.legend.ti'), sw(TT_HEX, 'bt.legend.tt'), sw(LET_GO, 'bt.legend.letGo', !!lit?.letGo.length), sw(MEET, 'bt.legend.meet', !!lit?.meet.length)].join('');
    }
    caption.classList.toggle('bt-swap', sweepOn && !!lit?.letGo.length);
    panel.classList.toggle('bt-sweeping', sweepOn);
    if (sweepOn) {
      const n = BT.sweep(view.dir).stops.length;
      sweepInput.max = String(n - 1); sweepInput.value = String(view.k);
      panel.querySelector('.bt-sweep-label').textContent = t('bt.sweep.param', L, { d: dirName(view.dir, L) });
      caption.textContent = btSweepCaption(view.dir, view.k, L);
      note.textContent = t('bt.note.sweep', L);
    } else if (shadow) {
      panel.querySelector('.bt-param-label').textContent = t('wq.param', L, { a: t(`wq.dir.${view.from}`, L), b: t(`wq.dir.${view.to}`, L) });
      input.value = String(view.u);
      caption.textContent = btShadowCaption(view, shown, L);
      note.textContent = t('bt.note.shadow', L);
    } else {
      panel.querySelector('.bt-shells-label').textContent = t('bt.shells.param', L, { n: view.shells, total: btShells() });
      shellsInput.max = String(btShells()); shellsInput.value = String(view.shells);
      panel.querySelector('.bt-apart-label').textContent = t('bt.apart', L, { p: Math.round(view.apart / 10) });
      apartInput.value = String(view.apart);
      panel.querySelector('.bt-sectors-label').textContent = t('wq.sectors.param', L);
      sectorsInput.value = String(view.sectorsApart);
      const sectorsCaption = sectorsShown ? ` · ${t('wq.sectors.count', L, { n: sectorsShown.count, w: sectorsShown.wedges })}` : '';
      caption.textContent = (view.whole ? t('bt.shells.whole', L, { n: btShells() }) : btShellsCaption(view.shells, L)) + sectorsCaption;
      note.textContent = `${t('bt.note.shells', L)}${view.whole ? '' : ` ${t('wq.note.tapNext', L)}`} ${t('wq.note.rcp', L)} ${t('wq.note.dictoRcp', L)}${view.sectors ? ` ${t('bt.note.sectors', L)}` : ''}`;
    }
  }
  sweepInput.addEventListener('input', () => { if (playing) play(false); const k = Number(sweepInput.value); if (k === view.k) return; view.k = k; save(); draw(); });
  input.addEventListener('input', () => {
    let v = Number(input.value);
    if (v <= BT_SNAP) v = 0; else if (v >= 1000 - BT_SNAP) v = 1000;
    input.value = String(v);
    if (v === view.u) return;
    view.u = v; save(); draw();
  });
  shellsInput.addEventListener('input', () => { const n = Number(shellsInput.value); if (n === view.shells) return; view.shells = n; save(); draw(); fit(); });
  // Pull apart: while dragging the camera only backs off (keeping its turn), so nothing leaves the view; let go, it fits exactly
  const fitApart = (exact) => fitView([0, 0, 0], fitRadius(), null, exact);
  apartInput.addEventListener('input', () => { const a = Number(apartInput.value); if (a === view.apart) return; view.apart = a; save(); draw(); fitApart(false); });
  apartInput.addEventListener('change', () => fitApart(true));
  // Pull the sectors apart: as Pull apart, the camera backing off while dragging and fitting exactly on letting go
  sectorsInput.addEventListener('input', () => { const a = Number(sectorsInput.value); if (a === view.sectorsApart) return; view.sectorsApart = a; save(); draw(); fitApart(false); });
  sectorsInput.addEventListener('change', () => fitApart(true));
  panel.addEventListener('click', (e) => {
    if (e.target.closest('[data-bt-play]')) { play(!playing); return; }
    if (e.target.closest('[data-bt-whole]')) { view.whole = !view.whole; save(); draw(); fit(); return; }
    // RCP view and RCP v4 exclude each other; Cut open and Sectors go with either (as in the Queens world)
    if (e.target.closest('[data-bt-rcp]')) { view.rcp = !view.rcp; if (view.rcp) view.dictoRcp = false; save(); draw(); fit(); return; }
    if (e.target.closest('[data-bt-dicto-rcp]')) { view.dictoRcp = !view.dictoRcp; if (view.dictoRcp) view.rcp = false; save(); draw(); fit(); return; }
    if (e.target.closest('[data-bt-sectors]')) { view.sectors = !view.sectors; save(); draw(); fit(); return; }
    const b = e.target.closest('[data-bt-mode], [data-bt-dir], [data-bt-from], [data-bt-to]');
    if (!b) return;
    const { btMode: mode, btDir: dir, btFrom: from, btTo: to } = b.dataset;
    if (playing) play(false);
    if (mode) { if (mode === view.mode) return; view.mode = mode; save(); draw(); fit(); return; }
    if (dir) { if (dir === view.dir) return; view.dir = dir; view.k = -1; }
    else if (from) { if (from === view.to) view.to = view.from; view.from = from; view.u = 0; }
    else if (to && to !== view.from) { view.to = to; view.u = 1000; }
    else return;
    save(); draw();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    // Shells: tapping the picture adds the next shell, as in the Queens world
    meshes: () => (active && view.mode === 'shells' && !view.whole ? shellsGroup.children.filter((c) => c.isMesh) : []),
    handleTap: () => {
      if (!active || view.mode !== 'shells' || view.whole || view.shells >= btShells()) return false;
      view.shells++; save(); draw(); fit();
      return true;
    },
    /** ?open=bitrunc:<sweep|shadow|shells|whole>, :<vertex|edge|face|cell|generic> (the Sweep along it, at the swap nearest its
     *  middle), :swap (the generic Sweep at that swap), :sectors (Cut open in its 32 sectors pulled apart, as whitequeen:sectors). */
    setChain(kind) {
      const k = SHORT[kind] ?? kind;
      if (kind === 'sweep' || kind === 'shadow') view.mode = kind;
      else if (kind === 'shells') Object.assign(view, { mode: 'shells', whole: false });
      else if (kind === 'whole') Object.assign(view, { mode: 'shells', whole: true });
      else if (kind === 'sectors') Object.assign(view, { mode: 'shells', whole: true, sectors: true, sectorsApart: 500 });
      else if (kind === 'swap') Object.assign(view, { mode: 'sweep', dir: 'generic', k: middleSwap('generic') });
      else if (BT_DIRECTIONS.includes(k)) Object.assign(view, { mode: 'sweep', dir: k, k: middleSwap(k) });
      else return;
      save();
      if (active) { draw(); fit(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { if (playing) { playing = false; if (raf) cancelAnimationFrame(raf); raf = 0; } panel.classList.remove('visible'); return; }
      draw(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);   // after the entry has written the menu's title
    },
    resetView() { if (playing) play(false); Object.assign(view, { mode: 'sweep', dir: 'generic', k: -1, ...BT_DEFAULT, u: 0, shells: 1, whole: false, apart: 0, sectors: false, sectorsApart: 0 }); save(); if (active) { draw(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, and in it what is shown and its counts. */
    probe: () => {
      if (!shown) return null;
      if (view.mode === 'sweep') {
        const sw = BT.sweep(view.dir), s = shown, e = s.event;
        return { mode: 'sweep', dir: view.dir, k: view.k, stops: sw.stops.length, levels: sw.levels.length, level: s.stop.level ?? null, gap: s.stop.gap ?? null, value: s.value, cells: s.cells.length, ti: s.ti, tt: s.tt, touching: s.touching.length,
          event: e ? { born: e.born.length, died: e.died.length, letGo: e.letGo.length, meet: e.meet.length, swapFrom: e.swapFrom } : null, lit: lit ? { letGo: lit.letGo.length, meet: lit.meet.length } : null, totals: { ...sw.totals }, playing, meshes: sweepGroup.children.length };
      }
      if (view.mode === 'shadow') return { mode: 'shadow', from: view.from, to: view.to, u: view.u, stop: view.u === 0 ? view.from : view.u === 1000 ? view.to : null, vertices: shown.vertices.length, corners: shown.P.length, edges: shown.edges.length, faces: shown.faces.length, shell: shell.visible };
      // apart: the pull (0…1000) and how far the drawn cells' centres sit from the centre (least, mean, most)
      const { CENTRES } = btPicture(pic()), d = drawnCells.map((ci) => Math.hypot(...CENTRES[ci].map((x, i) => x + btApartShift(ci, cellApart(), pic())[i])));
      return { mode: 'shells', rcp: view.rcp, dictoRcp: view.dictoRcp, sectors: sectorsShown ? { ...sectorsShown } : null, whole: view.whole, wholeKept: view.whole ? wholeKept.slice() : null, shells: view.shells, total: btShells(), sizes: BT.model().SHELLS.map((x) => x.length), newest: { k: view.shells - 1, cells: BT.model().SHELLS[view.shells - 1].length }, radius: shellsRadius, meshes: shellsGroup.children.length,
        apart: view.apart, drawn: drawnCells.length, centres: { min: Math.min(...d), mean: d.reduce((a, x) => a + x, 0) / d.length, max: Math.max(...d) } };
    },
  };
}

/** The world's cover in the DICTO menu: the gold core truncated icosahedron and the 32 cells round it (the first shell), in the Shells
 *  view's perspective, each edge in its shell's colour, the core drawn over and thicker (quick: bitrunc-geometry.js coverEdges).
 *  [[a, b], …] with .colours, .layers, .widths (wireframe-preview.js). */
export function bitruncPreviewEdges() {
  const { core, ring } = BT.coverEdges(), N = 6;   // six shells (tests/unit/bitrunc.test.mjs)
  const css = (k) => `#${new THREE.Color(shellColour(k, N)).getHexString()}`;
  const edges = [...ring, ...core];
  Object.assign(edges, { colours: [...ring.map(() => css(1)), ...core.map(() => css(0))], layers: [...ring.map(() => 0), ...core.map(() => 1)], widths: [...ring.map(() => 1), ...core.map(() => 2)] });
  return edges;
}
