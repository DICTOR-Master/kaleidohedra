// The Queens' walls (DICTO 2026-11-16; working name, DICTO may rename it).
// DICTO · dictospheres.com
// Part 1, the Queens pulled apart: one switch White (the 600-cell) | Red (the 120-cell), the modes Cells | Sheets, a row of the four named
// directions (the Queens world's own, along the White Queen's turnings as its stage slider), and one long Apart slider at the bottom. The
// geometry is queens-walls-geometry.js (the Queens world's exact models; unit-tested):
//   Cells: each cell a pyramid from the centre, pulled out along its own cell's 4D direction and then projected, the 4D twin of the Vacuus
//     lens's Exploded view. The White Queen's tetrahedra in the app's tetrahedron red, the Red Queen's dodecahedra in its dodecahedron
//     violet: those cells are those solids.
//   Sheets: the 60 central sheets on the 60 mirrors (the Vacuus of the heart kind), the White Queen's as fans of 20 triangles, the Red
//     Queen's as fans of 12 pentagons, on the same 60 planes: switching the Queen keeps the sheets in place and swaps the faces. Apart
//     slides each sheet out along its own normal, like DICTO's cardboard Vacuus. The sheets in the label colour sky (the papers' full
//     sheet), not a solid's colour.
// Part 2, the cats (Silent Running #109, Walls of Silence #110; geometry queens-cats-geometry.js, unit-tested), the same projection and
// the same named views:
//   A and B: the White Queen with the golden solids A and B centred on her own corners; their fins (the cone from the centre over each
//     face) on her walls, A's 30 all on mirrors, B's 80 on 40 mirrors and 40 cross walls; Apart slides each fin along its wall's normal.
//   Cats: the Red Queen with her 10 inscribed White Queens, one state of 5 at a time; her 600 corners glow (each is in exactly 2, one
//     of each state); one copy of A or B at a time, stepped through by a big Next copy button.
//   Dual cats: the Red Queen with one of her five dual cats A*, −A*, C3*, B*, −B* (their overlap is the Red Queen); its fins on her
//     mirrors with her pentagons on those mirrors; Apart slides each mirror's fins and pentagons out together.
//   Wherever a shape is shown, a line gives its kind (heart / inherited heart / non-heart, DICTO's names), read from its plates.
// Colours: app solid colours only for real solids (the cells; the Red Queen's pentagons, faces of her dodecahedra, in dodecahedron
// violet). The cats and the walls are labels, in the papers' label palette: A teal, −A cream, C3 slate, B apricot, −B pink, full sheets
// sky; the five 600-cells of a state teal, cream, slate, apricot, pink.
// Drawn to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, crisp antialiased edges (1.6 px), no haze;
// one merged mesh per layer, moved in place as Apart moves (600 pyramids stay smooth on an iPad).
// Words in all 7 languages (i18n qw.*).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { storageKey } from './site.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { QW_QUEENS, QW_DIRECTIONS, QW_VERTICES, QW_RADIUS, QW_CELLS, QW_SHEETS, MIRRORS, qwView } from './queens-walls-geometry.js';
import { ORBITS, whiteCats, whiteWalls, inscribed, inscribedEdges, copiesIn, dualCats, dualRadius, solid, kindOf } from './queens-cats-geometry.js';
import * as WQG from './white-queen-geometry.js';
import * as RQG from './red-queen-geometry.js';

export const QW_TITLE = "Queens' walls";
export const QW_MODES = ['cells', 'sheets', 'ab', 'cats', 'duals'];
/** The papers' label palette (Silent Running, Walls of Silence): labels only, never a solid's colour. */
export const QW_LABEL = { teal: 0x20a89e, cream: 0xf0e6be, slate: 0x647088, apricot: 0xf0a88a, pink: 0xf096c0, sky: 0x78c8f0 };
/** The papers' group mapping: A teal, −A cream, C3 slate, B apricot, −B pink (their duals the same). */
export const QW_GROUP = { A: QW_LABEL.teal, '-A': QW_LABEL.cream, C3: QW_LABEL.slate, B: QW_LABEL.apricot, '-B': QW_LABEL.pink };
export const QW_COLOURS = { white: 0xcd3e28, red: 0x8a5cc4, sheet: QW_LABEL.sky, edge: 0x1d2027, strut: 0xc8ced8, glow: 0xfff6e0, host: 0xdfe6f0 };
const STATE_COLOURS = [QW_LABEL.teal, QW_LABEL.cream, QW_LABEL.slate, QW_LABEL.apricot, QW_LABEL.pink];
const AB = ['A', 'B', 'both'], COPY = ['none', 'A', 'B'], EDGES = ['light', 'all'];
const APART_MAX = 3;   // at the slider's end each piece has moved 3 × the Queen's radius (in 4D, before the shadow)
const MODE_QUEEN = { ab: 'white', cats: 'red', duals: 'red' };
const lang = () => getSettings().language;
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
/** A cat's name as the papers write it: A, −A, C3, B, −B (and A*, … for the duals). */
const nameOf = (k, star = '') => `${k.replace('-', '−')}${star}`;

export function createQueensWallsWorld({ scene, fitView = () => {} }) {
  const STORAGE_KEY = storageKey('queensWalls');
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const DEFAULTS = { queen: 'white', mode: 'sheets', dir: 'vertex-first', apart: 500, ab: 'both', state: 0, copy: 'none', copyN: 0, dual: 'A', edges: 'light' };
  const view = { ...DEFAULTS };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (QW_QUEENS.includes(d?.queen)) view.queen = d.queen;
    if (QW_MODES.includes(d?.mode)) view.mode = d.mode;
    if (QW_DIRECTIONS.includes(d?.dir)) view.dir = d.dir;
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1000, Math.round(d.apart)));
    if (AB.includes(d?.ab)) view.ab = d.ab;
    if (d?.state === 0 || d?.state === 1) view.state = d.state;
    if (COPY.includes(d?.copy)) view.copy = d.copy;
    if (Number.isInteger(d?.copyN) && d.copyN >= 0 && d.copyN < 600) view.copyN = d.copyN;
    if (ORBITS.includes(d?.dual)) view.dual = d.dual;
    if (EDGES.includes(d?.edges)) view.edges = d.edges;
  } catch { /* defaults */ }
  if (MODE_QUEEN[view.mode]) view.queen = MODE_QUEEN[view.mode];
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false, skeleton = false, opacity = 1, shown = null;
  // the picture as base + a · offset per vertex, per layer; rebuilt when anything but Apart changes
  let built = null;
  const clear = () => { for (const c of [...group.children]) { group.remove(c); c.geometry.dispose(); c.material.dispose(); } };
  const copySolids = new Map();   // the solid of a copy (hull, plates, kind), by its corners
  /** The copy of the state shown: 600 per state (5 inscribed 600-cells × 60 S5s × the orbit and its negative). */
  function copyAt(n) {
    const ci = inscribed().states[view.state][Math.floor(n / 120)], j = n % 120, o = copiesIn(ci)[Math.floor(j / 2)];
    const k = view.copy === 'A' ? (j % 2 ? '-A' : 'A') : (j % 2 ? '-B' : 'B'), corners = o[k], key = corners.join(',');
    if (!copySolids.has(key)) copySolids.set(key, solid(corners.map((i) => QW_VERTICES.red[i])));
    return { cell: ci, orbit: k, corners, solid: copySolids.get(key) };
  }

  function build() {
    clear();
    const q = view.queen, { frame } = qwView(view.dir), pr = (x) => frame.map((f) => dot(x, f) * WS);
    const R = QW_RADIUS[q], ZERO = [0, 0, 0];
    // layers: F opaque faces, T see-through fins, L crisp lines (coloured), S faint lines, G glowing corners (still)
    const F = { b: [], o: [], c: [] }, T = { b: [], o: [], c: [] }, L = { b: [], o: [], c: [] }, S = { b: [], o: [] }, C = { b: [], c: [] }, G = [];
    const col = new THREE.Color(), edgeCol = new THREE.Color(skeleton ? 0xdfe6f0 : QW_COLOURS.edge);
    const poly = (lay, pts, o, c) => { for (let i = 1; i + 1 < pts.length; i++) for (const p of [pts[0], pts[i], pts[i + 1]]) { lay.b.push(...p); lay.o.push(...o); lay.c.push(c.r, c.g, c.b); } };
    const line = (a, b, o, c = edgeCol) => { L.b.push(...a, ...b); L.o.push(...o, ...o); L.c.push(c.r, c.g, c.b, c.r, c.g, c.b); };
    const faint = (a, b, o = ZERO) => { S.b.push(...a, ...b); S.o.push(...o, ...o); };
    const faded = (a, b, c) => { C.b.push(...a, ...b); C.c.push(c.r, c.g, c.b, c.r, c.g, c.b); };   // still, coloured and strongly faded
    /** A fin: the cone from the centre over a face (3D points), its face and sides in one colour, the face's edges crisp. */
    const fin = (lay, pts, o, c, ec = edgeCol) => {
      poly(lay, pts, o, c);
      pts.forEach((p, i) => { const r = pts[(i + 1) % pts.length]; poly(lay, [ZERO, p, r], o, c); line(p, r, o, ec); });
      for (const p of pts) faint(ZERO, p, o);
    };
    const info = { queen: q, mode: view.mode, dir: view.dir };
    let base = new THREE.Color(QW_COLOURS.sheet);
    if (view.mode === 'cells' || view.mode === 'sheets') {
      const P = QW_VERTICES[q].map(pr);
      const pieces = view.mode === 'cells' ? QW_CELLS[q].map((c) => ({ dir: c.dir, faces: c.faces, corners: c.corners })) : QW_SHEETS[q].map((s) => ({ dir: s.normal, faces: s.faces, corners: [...new Set(s.faces.flat())] }));
      base = new THREE.Color(view.mode === 'cells' ? QW_COLOURS[q] : QW_COLOURS.sheet);
      pieces.forEach((p, n) => {
        const o = pr(p.dir).map((x) => x * R);
        // each piece a shade of the one colour (a label, so the pieces can be told apart), spread by the golden angle
        col.copy(base).multiplyScalar(0.72 + 0.4 * ((n * 0.6180339887) % 1));
        for (const f of p.faces) poly(F, f.map((k) => P[k]), o, col);
        const seen = new Set();
        for (const f of p.faces) f.forEach((a, i) => { const b = f[(i + 1) % f.length], key = a < b ? `${a},${b}` : `${b},${a}`; if (seen.has(key)) return; seen.add(key); line(P[a], P[b], o); });
        if (view.mode === 'cells') for (const k of p.corners) faint(ZERO, P[k], o);   // the struts from the centre: the pyramid's sides
      });
      Object.assign(info, { pieces: pieces.length, faces: pieces.reduce((n, p) => n + p.faces.length, 0), facesPerPiece: [...new Set(pieces.map((p) => p.faces.length))], sides: [...new Set(pieces.flatMap((p) => p.faces.map((f) => f.length)))], kinds: [['queen', 'heart']] });
    } else if (view.mode === 'ab') {
      const P = QW_VERTICES.white.map(pr), W = whiteWalls(), cats = whiteCats();
      for (const [a, b] of WQG.EDGES) faint(P[a], P[b]);   // the White Queen, faint
      const show = view.ab === 'both' ? ['A', 'B'] : [view.ab], used = { mirror: new Map(), cross: new Set() };
      const stats = {};
      for (const k of show) {
        const s = cats[k], Q3 = s.corners.map(pr), c0 = new THREE.Color(QW_GROUP[k]), c1 = c0.clone().lerp(new THREE.Color(0xffffff), 0.5);
        let m = 0, x = 0;
        for (const p of s.plates) {
          const isM = p.wall.kind === 'mirror', n = isM ? W.mirrors[p.wall.index] : W.cross[p.wall.index];
          if (isM) { m++; used.mirror.set(p.wall.index, (used.mirror.get(p.wall.index) ?? 0) + 1); } else { x++; used.cross.add(p.wall.index); }
          const o = pr(n).map((v) => v * R);
          for (const fi of p.faces) fin(F, s.faces[fi].map((i) => Q3[i]), o, isM ? c0 : c1);
        }
        stats[k] = { plates: s.plates.length, mirrors: m, cross: x, faces: s.faces.length, kind: s.kind };
      }
      Object.assign(info, { ab: view.ab, stats, mirrorsUsed: used.mirror.size, mirrorsShared: [...used.mirror.values()].filter((v) => v > 1).length, crossUsed: used.cross.size, kinds: [['queen', 'heart'], ...show.map((k) => [k, cats[k].kind])] });
    } else if (view.mode === 'cats') {
      const P = QW_VERTICES.red.map(pr), ins = inscribed(), cells = ins.states[view.state];
      for (const [a, b] of RQG.EDGES) faint(P[a], P[b]);   // the Red Queen, faint
      let copy = null;
      if (view.copy !== 'none') copy = copyAt(view.copyN);
      cells.forEach((ci, n) => {
        if (copy && ci !== copy.cell) return;   // with a copy shown: only its own 600-cell, in grey
        col.set(copy ? QW_COLOURS.host : STATE_COLOURS[n]);
        // light (the default): the 600-cells' edges strongly faded, so the glowing corners and a copy read clearly; All edges: crisp
        for (const [a, b] of inscribedEdges(ci)) (view.edges === 'all' ? line(P[a], P[b], ZERO, col) : faded(P[a], P[b], col));
      });
      for (const p of P) G.push(p);   // every corner glows: each is in exactly 2 of the 10, one of each state
      const count = new Array(P.length).fill(0); ins.cells.forEach((c) => c.forEach((i) => count[i]++));
      if (copy) {
        const Q3 = copy.solid.corners.map(pr), c0 = new THREE.Color(QW_GROUP[copy.orbit]);
        for (const f of copy.solid.faces) poly(F, f.map((i) => Q3[i]), ZERO, c0);
        for (const [a, b] of copy.solid.edges) line(Q3[a], Q3[b], ZERO);
      }
      Object.assign(info, {
        state: view.state, edges: view.edges, cellsShown: cells.length, inscribed: ins.cells.length, glow: G.length, membership: [...new Set(count)],
        disjoint: cells.every((a) => cells.every((b) => a === b || ins.meet(a, b) === 0)),
        copy: copy ? { type: view.copy, n: view.copyN, orbit: copy.orbit, cell: copy.cell, corners: copy.corners.length, faces: copy.solid.faces.length, plates: copy.solid.plates.length, kind: copy.solid.kind } : null,
        kinds: [['queen', 'heart'], ['inscribed', kindOf(ins.cells[cells[0]].map((i) => QW_VERTICES.red[i]), [])], ...(copy ? [[copy.orbit, copy.solid.kind]] : [])],
      });
    } else {
      const P = QW_VERTICES.red.map(pr), d = dualCats()[view.dual], D3 = d.corners.map(pr), c0 = new THREE.Color(QW_GROUP[view.dual]);
      const ec = c0.clone().multiplyScalar(0.55), violet = new THREE.Color(QW_COLOURS.red);
      for (const [a, b] of RQG.EDGES) faint(P[a], P[b]);
      const mirrors = new Set();
      let covered = 0;
      for (const p of d.plates) {
        const o = pr(MIRRORS[p.wall.index]).map((v) => v * R);
        for (const fi of p.faces) fin(T, d.faces[fi].map((i) => D3[i]), o, c0, ec);
        if (mirrors.has(p.wall.index)) continue;
        mirrors.add(p.wall.index);
        // the Red Queen's pentagons on this mirror (her sheet), moving with the fins: those the fins cover whole filled violet (faces of
        // her dodecahedra), the others as edges
        const cov = new Set(d.plates.filter((x) => x.wall.index === p.wall.index).flatMap((x) => x.covers.whole));
        QW_SHEETS.red[p.wall.index].faces.forEach((f, j) => { const pts = f.map((k) => P[k]); if (cov.has(j)) { poly(F, pts, o, violet); covered++; } pts.forEach((a, i) => line(a, pts[(i + 1) % pts.length], o)); });
      }
      const fpp = [...new Set(d.plates.map((p) => p.faces.length))];
      Object.assign(info, { dual: view.dual, corners: d.corners.length, edges: d.edges.length, faces: d.faces.length, cells: d.facets.length, plates: d.plates.length, mirrorsUsed: mirrors.size, onMirrors: d.plates.every((p) => p.wall.kind === 'mirror'), facesPerPlate: fpp, pentagons: mirrors.size * 12, covered, kinds: [['queen', 'heart'], [`${view.dual}*`, d.kind]] });
      base = c0;
    }

    // ---- the layers ----
    const see = opacity < 1;
    const mk = (lay) => { const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(lay.b), 3)); geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(lay.c), 3)); return geo; };
    const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, side: THREE.DoubleSide, flatShading: true, transparent: see, opacity, depthWrite: !see, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, emissive: base.clone().multiplyScalar(0.1) });
    if (see) mat.userData.hollow = true;
    const mesh = new THREE.Mesh(mk(F), mat); mesh.frustumCulled = false; mesh.visible = !skeleton; if (see) mesh.renderOrder = 4;
    // the dual's fins see-through, so the Red Queen's pentagons inside them show
    const tmat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.42 * opacity, depthWrite: false, polygonOffset: true, polygonOffsetFactor: 2, polygonOffsetUnits: 2 });
    const tmesh = new THREE.Mesh(mk(T), tmat); tmesh.frustumCulled = false; tmesh.visible = !skeleton && T.b.length > 0; tmesh.renderOrder = 5;
    const edges = new LineSegments2(new LineSegmentsGeometry(), new LineMaterial({ color: 0xffffff, vertexColors: true, linewidth: 1.6 }));
    edges.frustumCulled = false;
    // the struts and the faint Queen thin and faint (plain lines, moved in place: 2400 of them for the White Queen's cells)
    const sgeo = new THREE.BufferGeometry(); sgeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(S.b.length), 3));
    const struts = new THREE.LineSegments(sgeo, new THREE.LineBasicMaterial({ color: QW_COLOURS.strut, transparent: true, opacity: 0.22, depthWrite: false }));
    struts.frustumCulled = false;
    const cgeo = new THREE.BufferGeometry(); cgeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(C.b), 3)); cgeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(C.c), 3));
    const fadedLines = new THREE.LineSegments(cgeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.2, depthWrite: false }));
    fadedLines.frustumCulled = false; fadedLines.visible = C.b.length > 0;
    group.add(mesh, tmesh, edges, struts, fadedLines);
    if (G.length) {
      // the glowing corners: one merged mesh of small balls, unlit so they read as light
      const ball = new THREE.IcosahedronGeometry(R * WS * 0.016, 1), bp = ball.attributes.position.array, idx = ball.index ? ball.index.array : null;
      const tri = idx ? [...idx] : [...Array(bp.length / 3).keys()], out = new Float32Array(G.length * tri.length * 3);
      let w = 0;
      for (const g of G) for (const i of tri) { out[w++] = bp[3 * i] + g[0]; out[w++] = bp[3 * i + 1] + g[1]; out[w++] = bp[3 * i + 2] + g[2]; }
      ball.dispose();
      const ggeo = new THREE.BufferGeometry(); ggeo.setAttribute('position', new THREE.BufferAttribute(out, 3));
      const glow = new THREE.Mesh(ggeo, new THREE.MeshBasicMaterial({ color: QW_COLOURS.glow }));
      glow.frustumCulled = false; group.add(glow);
    }
    built = { mesh, tmesh, edges, struts, F: { b: new Float32Array(F.b), o: new Float32Array(F.o) }, T: { b: new Float32Array(T.b), o: new Float32Array(T.o) }, L: { b: new Float32Array(L.b), o: new Float32Array(L.o), c: new Float32Array(L.c), pos: new Float32Array(L.b.length) }, S: { b: new Float32Array(S.b), o: new Float32Array(S.o) } };
    shown = { ...info, lines: L.b.length / 6, faint: S.b.length / 6, faded: C.b.length / 6, solidTriangles: F.b.length / 9, seeTriangles: T.b.length / 9 };
    move();
  }
  const usesApart = () => view.mode !== 'cats';
  /** Apart: every piece moves in place (no rebuild). */
  function move() {
    if (!built) return;
    const a = usesApart() ? (view.apart / 1000) * APART_MAX : 0;
    for (const [m, lay] of [[built.mesh, built.F], [built.tmesh, built.T]]) {
      const pos = m.geometry.attributes.position.array;
      for (let i = 0; i < pos.length; i++) pos[i] = lay.b[i] + a * lay.o[i];
      m.geometry.attributes.position.needsUpdate = true;   // flat shading: no normals to recompute
    }
    const L = built.L;
    for (let i = 0; i < L.pos.length; i++) L.pos[i] = L.b[i] + a * L.o[i];
    built.edges.geometry.dispose(); built.edges.geometry = new LineSegmentsGeometry();
    if (L.pos.length) { built.edges.geometry.setPositions(L.pos); built.edges.geometry.setColors(L.c); }
    const sp = built.struts.geometry.attributes.position.array;
    for (let i = 0; i < sp.length; i++) sp[i] = built.S.b[i] + a * built.S.o[i];
    built.struts.geometry.attributes.position.needsUpdate = true;
    shown.apart = view.apart;
    renderPanel();
  }
  const fitRadius = () => {
    const a = usesApart() ? (view.apart / 1000) * APART_MAX : 0, R = QW_RADIUS[view.queen];
    if (view.mode === 'duals') return (dualRadius() + R * a) * WS * 1.05;
    return R * WS * (1.1 + a);
  };
  const fit = () => fitView([0, 0, 0], fitRadius(), [0.3, 0.25, 1], true);   // the app stands the picture in the free area above the panel
  const draw = () => { if (active) build(); };

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldqueensWalls-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options qw-modes">${QW_MODES.map((m) => `<button type="button" data-qw-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-queens">${QW_QUEENS.map((q) => `<button type="button" data-qw-queen="${q}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-ab">${AB.map((k) => `<button type="button" data-qw-ab="${k}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-states">${[0, 1].map((k) => `<button type="button" class="qw-big" data-qw-state="${k}"></button>`).join('')}<button type="button" class="qw-big" data-qw-edges="1" aria-pressed="false"></button></div>
    <div class="w4d-row w4d-options qw-copies">${COPY.map((k) => `<button type="button" data-qw-copy="${k}"></button>`).join('')}<button type="button" class="qw-big qw-next" data-qw-next="1"></button></div>
    <div class="w4d-row w4d-options qw-duals">${ORBITS.map((k) => `<button type="button" data-qw-dual="${k}"></button>`).join('')}</div>
    <div class="w4d-row w4d-options qw-dirs">${QW_DIRECTIONS.map((k) => `<button type="button" data-qw-dir="${k}"></button>`).join('')}</div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row vac-legend qw-key"></div>
    <div class="w4d-row vac-kind-row"><span class="vac-kind qw-kind"></span></div>
    <div class="w4d-row qw-apart-row"><label class="hull-pick"><span class="qw-apart-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row st-note fold"></div>`;
  // Fold (DICTO 2026-11-16): one big tap target at the top folds the panel to a slim bar with the mode's name, and unfolds it; the shape
  // is refitted into the free area. It is the panel's minimise handle (class panel-min: the app reads the panel's cover from it),
  // remembered for this session only.
  const FOLD_KEY = storageKey('queensWallsFold');
  const fold = document.createElement('button');
  fold.type = 'button'; fold.className = 'panel-min qw-fold';
  panel.prepend(fold);
  let folded = false;
  try { folded = sessionStorage.getItem(FOLD_KEY) === '1'; } catch { /* not folded */ }
  const applyFold = () => { panel.classList.toggle('minimised', folded); fold.setAttribute('aria-expanded', String(!folded)); };
  applyFold();
  fold.addEventListener('click', () => {
    folded = !folded;
    try { sessionStorage.setItem(FOLD_KEY, folded ? '1' : '0'); } catch { /* best-effort */ }
    applyFold(); renderPanel();
    requestAnimationFrame(() => { if (active) fit(); });
  });
  document.body.appendChild(panel);
  const $ = (s) => panel.querySelector(s);
  const apartInput = $('.qw-apart-row input'), caption = $('.ch-param-caption'), note = $('.st-note.fold'), key = $('.qw-key'), kind = $('.qw-kind');
  note.addEventListener('click', () => note.classList.toggle('open'));
  const press = (x, on) => { x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); };
  const hide = (sel, off) => { $(sel).hidden = off; };
  const chip = (c, text) => `<span class="vac-chip"><i style="background:#${new THREE.Color(c).getHexString()}"></i>${text}</span>`;
  const KIND_NAME = { queen: (L) => t(`wq.queen.${view.queen}`, L), inscribed: (L) => t('qw.inscribed', L) };
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active || !shown) return;
    const L = lang(), m = view.mode;
    panel.querySelectorAll('[data-qw-mode]').forEach((x) => { x.textContent = t(`qw.mode.${x.dataset.qwMode}`, L); press(x, x.dataset.qwMode === m); });
    panel.querySelectorAll('[data-qw-queen]').forEach((x) => { x.textContent = t(`wq.queen.${x.dataset.qwQueen}`, L); press(x, x.dataset.qwQueen === view.queen); });
    panel.querySelectorAll('[data-qw-ab]').forEach((x) => { x.textContent = x.dataset.qwAb === 'both' ? t('qw.ab.both', L) : x.dataset.qwAb; press(x, x.dataset.qwAb === view.ab); });
    panel.querySelectorAll('[data-qw-state]').forEach((x) => { x.textContent = t('qw.state', L, { n: Number(x.dataset.qwState) + 1 }); press(x, Number(x.dataset.qwState) === view.state); });
    panel.querySelectorAll('[data-qw-copy]').forEach((x) => { x.textContent = x.dataset.qwCopy === 'none' ? t('qw.copy.none', L) : t('qw.copy.type', L, { s: x.dataset.qwCopy }); press(x, x.dataset.qwCopy === view.copy); });
    panel.querySelectorAll('[data-qw-dual]').forEach((x) => { x.textContent = nameOf(x.dataset.qwDual, '*'); press(x, x.dataset.qwDual === view.dual); });
    panel.querySelectorAll('[data-qw-dir]').forEach((x) => { x.textContent = t(`wq.btn.${x.dataset.qwDir}`, L); x.title = t(`wq.dir.${x.dataset.qwDir}`, L); press(x, x.dataset.qwDir === view.dir); });
    fold.textContent = folded ? t('qw.fold.show', L, { m: t(`qw.mode.${m}`, L) }) : t('qw.fold.hide', L);
    const all = $('[data-qw-edges]');
    all.textContent = t('qw.edges.all', L); press(all, view.edges === 'all');
    const next = $('[data-qw-next]');
    next.textContent = t('qw.copy.next', L);
    next.hidden = view.copy === 'none';
    // hide whatever does not apply
    hide('.qw-queens', !!MODE_QUEEN[m]); hide('.qw-ab', m !== 'ab'); hide('.qw-states', m !== 'cats'); hide('.qw-copies', m !== 'cats'); hide('.qw-duals', m !== 'duals');
    hide('.qw-apart-row', !usesApart());
    const p = Math.round(view.apart / 10);
    $('.qw-apart-label').textContent = t('qw.apart', L, { p });
    apartInput.value = String(view.apart);
    apartInput.setAttribute('aria-label', t('qw.apart', L, { p }));
    let cap = '', keyHtml = '';
    if (m === 'cells' || m === 'sheets') cap = t(`qw.cap.${m}.${view.queen}`, L);
    else if (m === 'ab') {
      const S = shown.stats;
      cap = view.ab === 'both' ? t('qw.cap.ab.both', L, { m: shown.mirrorsUsed, k: shown.mirrorsShared, c: shown.crossUsed, p: S.A.plates + S.B.plates })
        : t('qw.cap.ab.one', L, { s: view.ab, p: S[view.ab].plates, m: S[view.ab].mirrors, c: S[view.ab].cross });
      const ks = view.ab === 'both' ? ['A', 'B'] : [view.ab], lite = (k) => new THREE.Color(QW_GROUP[k]).lerp(new THREE.Color(0xffffff), 0.5);
      keyHtml = ks.flatMap((k) => [chip(QW_GROUP[k], t('qw.key.mirror', L, { s: k })), ...(S[k].cross ? [chip(lite(k), t('qw.key.cross', L, { s: k }))] : [])]).join('');
    } else if (m === 'cats') {
      if (shown.copy) {
        const c = shown.copy;
        cap = t('qw.cap.copy', L, { s: nameOf(c.orbit), t: c.type, i: c.n + 1, n: 600, N: 1200, st: view.state + 1 });
        keyHtml = chip(QW_GROUP[c.orbit], nameOf(c.orbit)) + chip(QW_COLOURS.host, t('qw.key.host', L)) + chip(QW_COLOURS.glow, t('qw.key.corners', L));
      } else {
        cap = t('qw.cap.cats', L, { n: view.state + 1 });
        keyHtml = `<span class="vac-chip">${STATE_COLOURS.map((c) => `<i style="background:#${new THREE.Color(c).getHexString()}"></i>`).join('')}${t('qw.key.cells', L)}</span>` + chip(QW_COLOURS.glow, t('qw.key.corners', L));
      }
    } else {
      const d = shown;
      cap = t('qw.cap.dual', L, { s: nameOf(view.dual, '*'), v: d.corners, e: d.edges, f: d.faces, c: d.cells, p: d.plates, k: d.facesPerPlate.join(', ') });
      keyHtml = chip(QW_GROUP[view.dual], t('qw.key.fins', L, { s: nameOf(view.dual, '*') })) + chip(QW_COLOURS.red, t('qw.key.pentagons', L, { n: d.covered, m: d.pentagons }));
    }
    caption.textContent = `${t(`wq.dir.${view.dir}`, L)} · ${cap}`;
    key.innerHTML = keyHtml; key.hidden = !keyHtml;
    kind.textContent = shown.kinds.map(([s, k]) => t('qw.kindOf', L, { s: KIND_NAME[s] ? KIND_NAME[s](L) : nameOf(s.replace('*', ''), s.endsWith('*') ? '*' : ''), k: t(`poly.vac.kind.${k}`, L) })).join(' · ');
    note.textContent = m === 'cells' || m === 'sheets' ? `${t('qw.note', L)} ${t(`qw.note.${m}`, L)}` : t(`qw.note.${m}`, L);
  }
  apartInput.addEventListener('input', () => { const v = Number(apartInput.value); if (v === view.apart) return; view.apart = v; save(); move(); });
  apartInput.addEventListener('change', fit);
  const setMode = (m) => { view.mode = m; if (MODE_QUEEN[m]) view.queen = MODE_QUEEN[m]; };
  panel.addEventListener('click', (e) => {
    const g = (k) => e.target.closest(`[data-qw-${k}]`);
    const q = g('queen'), m = g('mode'), d = g('dir'), ab = g('ab'), st = g('state'), cp = g('copy'), nx = g('next'), du = g('dual'), ed = g('edges');
    if (ed) { view.edges = view.edges === 'all' ? 'light' : 'all'; save(); draw(); return; }
    if (q && q.dataset.qwQueen !== view.queen) { view.queen = q.dataset.qwQueen; save(); draw(); fit(); }
    else if (m && m.dataset.qwMode !== view.mode) { setMode(m.dataset.qwMode); save(); draw(); fit(); }
    else if (d && d.dataset.qwDir !== view.dir) { view.dir = d.dataset.qwDir; save(); draw(); }
    else if (ab && ab.dataset.qwAb !== view.ab) { view.ab = ab.dataset.qwAb; save(); draw(); }
    else if (st && Number(st.dataset.qwState) !== view.state) { view.state = Number(st.dataset.qwState); save(); draw(); }
    else if (cp && cp.dataset.qwCopy !== view.copy) { view.copy = cp.dataset.qwCopy; save(); draw(); }
    else if (nx) { view.copyN = (view.copyN + 1) % 600; save(); draw(); }
    else if (du && du.dataset.qwDual !== view.dual) { view.dual = du.dataset.qwDual; save(); draw(); }
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    /** ?open=queenswalls:<white|red|cells|sheets|ab|cats|duals>. */
    setChain(k) {
      if (QW_QUEENS.includes(k)) { view.queen = k; if (MODE_QUEEN[view.mode]) view.mode = 'sheets'; }
      else if (QW_MODES.includes(k)) setMode(k);
      else return;
      save(); draw(); if (active) fit();
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); return; }
      build(); fit();
      setTimeout(() => { if (active) renderPanel(); }, 0);
    },
    resetView() { Object.assign(view, DEFAULTS); save(); if (active) { build(); fit(); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) build(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) build(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, the pieces and how far the pieces have moved (the largest move on screen). */
    probe: () => {
      if (!shown || !built) return null;
      let moved = 0;
      for (const [m, lay] of [[built.mesh, built.F], [built.tmesh, built.T]]) {
        const pos = m.geometry.attributes.position.array;
        for (let i = 0; i < pos.length; i += 3) moved = Math.max(moved, Math.hypot(pos[i] - lay.b[i], pos[i + 1] - lay.b[i + 1], pos[i + 2] - lay.b[i + 2]));
      }
      return { ...shown, moved, folded };
    },
  };
}

/** The world's cover in the DICTO menu: the White Queen's 60 sheets half apart, their triangles' edges, vertex-first. */
export function queensWallsPreviewEdges() {
  const { frame } = qwView('vertex-first'), V = QW_VERTICES.white, out = [];
  for (const s of QW_SHEETS.white) {
    const o = frame.map((f) => dot(s.normal, f) * 0.9);
    const P = (i) => frame.map((f, k) => (dot(V[i], f) + o[k] * 2) / 3.8);
    for (const f of s.faces) f.forEach((a, i) => out.push([P(a), P(f[(i + 1) % 3])]));
  }
  return out;
}
