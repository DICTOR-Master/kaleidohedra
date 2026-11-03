// DICTO Vacuus (DICTO 2026-11-03): Polyhedraverse's lens on the solid on show, seen from its centre O, in five views (Pyramids,
// Exploded, Star, Sheets, Struts; the geometry is vacuus-geometry.js). While the lens is on, its drawing stands in for the build, as
// the ★ Star step's does. Drawn to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset, crisp screen-space
// edges ≥ 1.5 px; the Star view's spikes in the Star step's purple.
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { VACUUS_VIEWS, vacuusSolidOf, pyramidsOf, starTipsOf, finsOf, strutsOf, isCube } from './vacuus-geometry.js';
import { t } from './i18n.js';

const EDGE = 0x0b1220, SPIKE = 0x8f5bd8, GREY_ROD = 0x8a93a6, CENTRE_BALL = 0x1a1f2b;
/** Class colours (fins by congruence, struts by length), from the app's piece palette; shortest/smallest first. */
export const CLASS_COLOURS = [0xd9a520, 0x4dd0e1, 0x8f5bd8, 0xff8a65, 0x5fd38a, 0xc792ea, 0xffc857, 0x6f8cff, 0x7ae0b8, 0xff6f91];
const classColour = (i) => CLASS_COLOURS[i % CLASS_COLOURS.length];
const GAP = 0.04;                     // Pyramids: each pyramid drawn this much (× R) off along its normal, so the cuts read
const APART_MAX = 1.0;                // Exploded: the slider's far end moves each pyramid this far (× R)
const STRUT_R = 0.03, EDGE_ROD_R = 0.012, BALL_R = 0.075;   // × R
const num = (x) => String(Number(x.toFixed(3)));

export function createVacuusLens({ scene, look = () => ({ skeleton: false, opacity: 1 }) }) {
  const root = new THREE.Group();
  root.visible = false;
  scene.add(root);
  let st = null;      // { solid, colour, view, apart, fins, struts, tips }

  const solidMat = new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.55 });
  const spikeMat = new THREE.MeshStandardMaterial({ color: SPIKE, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5 });
  const classMats = CLASS_COLOURS.map((c) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5 }));
  const rodMats = CLASS_COLOURS.map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.45 }));   // struts: the rods are the picture, kept in Wireframe too
  const greyMat = new THREE.MeshStandardMaterial({ color: GREY_ROD, roughness: 0.6 });
  const ballMat = new THREE.MeshStandardMaterial({ color: CENTRE_BALL, roughness: 0.4 });
  const rodGeometry = new THREE.CylinderGeometry(1, 1, 1, 14, 1);      // shared: unit radius, unit height along y
  const ballGeometry = new THREE.SphereGeometry(1, 24, 16);
  const shared = new Set([rodGeometry, ballGeometry]);
  const lineMats = [];
  const lineMat = (color, width) => { const m = new LineMaterial({ color, linewidth: width }); lineMats.push(m); return m; };

  function clear() {
    for (const c of [...root.children]) { root.remove(c); if (!shared.has(c.geometry)) c.geometry.dispose(); }
    lineMats.splice(0).forEach((m) => m.dispose());
  }
  function mesh(tris, material) {
    const pos = new Float32Array(tris.length * 9);
    tris.forEach((tr, i) => tr.forEach((p, k) => pos.set(p, i * 9 + k * 3)));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, material);
    root.add(m);
    return m;
  }
  function lines(segs, color, width) {
    if (!segs.length) return;
    const g = new LineSegmentsGeometry();
    g.setPositions(segs.flatMap(([a, b]) => [...a, ...b]));
    const l = new LineSegments2(g, lineMat(color, width));
    l.frustumCulled = false;
    root.add(l);
  }
  // Rods (each [a, b]) of radius r as one instanced mesh.
  function rods(segs, r, material) {
    if (!segs.length) return;
    const im = new THREE.InstancedMesh(rodGeometry, material, segs.length);
    const up = new THREE.Vector3(0, 1, 0), m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    segs.forEach(([a, b], i) => {
      const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), d = B.clone().sub(A), len = d.length();
      q.setFromUnitVectors(up, d.normalize());
      m.compose(p.copy(A).add(B).multiplyScalar(0.5), q, s.set(r, len, r));
      im.setMatrixAt(i, m);
    });
    im.instanceMatrix.needsUpdate = true;
    root.add(im);
  }
  // A face (outward loop of points, normal n) as triangles: a fan when it is convex, else the earcut of three.js on its plane.
  function faceTris(loop, n) {
    const N = new THREE.Vector3(...n);
    const convex = loop.every((p, i) => {
      const a = loop[(i + 1) % loop.length], b = loop[(i + 2) % loop.length];
      const e1 = new THREE.Vector3(a[0] - p[0], a[1] - p[1], a[2] - p[2]), e2 = new THREE.Vector3(b[0] - a[0], b[1] - a[1], b[2] - a[2]);
      return e1.cross(e2).dot(N) >= -1e-12;
    });
    if (convex) return loop.slice(1, -1).map((_, i) => [loop[0], loop[i + 1], loop[i + 2]]);
    const u = new THREE.Vector3().subVectors(new THREE.Vector3(...loop[1]), new THREE.Vector3(...loop[0])).normalize(), w = new THREE.Vector3().crossVectors(N, u);
    const flat = loop.map((p) => new THREE.Vector2(u.dot(new THREE.Vector3(...p)), w.dot(new THREE.Vector3(...p))));
    return THREE.ShapeUtils.triangulateShape(flat, []).map(([i, j, k]) => [loop[i], loop[j], loop[k]]);
  }
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const times = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
  const loopEdges = (loop) => loop.map((p, i) => [p, loop[(i + 1) % loop.length]]);

  // The pyramids, each moved `d` (× R) out along its face normal.
  function drawPyramids(d) {
    const { solid } = st, tris = [], segs = [];
    for (const { base, n } of pyramidsOf(solid)) {
      const off = times(n, d * solid.R), B = base.map((p) => add(p, off));
      tris.push(...faceTris(B, n), ...B.map((p, i) => [off, B[(i + 1) % B.length], p]));
      segs.push(...loopEdges(B), ...B.map((p) => [off, p]));
    }
    mesh(tris, solidMat);
    lines(segs, look().skeleton ? 0xffffff : EDGE, 2);
  }
  function drawStar() {
    const { solid, tips } = st, P = solid.vertices, tris = [], spikes = [], segs = solid.edges.map(([a, b]) => [P[a], P[b]]);
    solid.faces.forEach((f, fi) => {
      const B = f.map((k) => P[k]);
      tris.push(...faceTris(B, solid.planes[fi].n));                 // the face: the pyramid's base, its inside now empty
      B.forEach((p, i) => { spikes.push([p, B[(i + 1) % B.length], tips[fi]]); segs.push([p, tips[fi]]); });
    });
    mesh(tris, solidMat);
    mesh(spikes, spikeMat);
    lines(segs, look().skeleton ? 0xffffff : EDGE, 2);
  }
  function drawSheets() {
    const { fins } = st, O = [0, 0, 0], byClass = new Map(), segs = [];
    for (const { a, b, cls } of fins.fins) {
      if (!byClass.has(cls)) byClass.set(cls, []);
      byClass.get(cls).push([O, a, b]);
      segs.push([a, b], [O, a], [O, b]);
    }
    for (const [cls, tris] of byClass) mesh(tris, classMats[cls % classMats.length]);
    lines(segs, look().skeleton ? 0xffffff : EDGE, 1.5);
  }
  function drawStruts() {
    const { solid, struts } = st, R = solid.R, P = solid.vertices, O = [0, 0, 0], byClass = new Map();
    for (const { v, cls } of struts.struts) { if (!byClass.has(cls)) byClass.set(cls, []); byClass.get(cls).push([O, v]); }
    for (const [cls, segs] of byClass) rods(segs, STRUT_R * R, rodMats[cls % rodMats.length]);
    rods(solid.edges.map(([a, b]) => [P[a], P[b]]), EDGE_ROD_R * R, greyMat);
    const ball = new THREE.Mesh(ballGeometry, ballMat);
    ball.scale.setScalar(BALL_R * R);
    root.add(ball);
  }

  function draw() {
    clear();
    if (!st) return;
    const { skeleton, opacity } = look();
    const see = opacity < 1;
    for (const m of [solidMat, spikeMat, ...classMats]) { m.transparent = see; m.opacity = see ? opacity : 1; m.depthWrite = !see; m.visible = !skeleton; }
    solidMat.color.copy(st.colour);
    if (st.view === 'pyramids') drawPyramids(GAP);
    else if (st.view === 'exploded') drawPyramids((st.apart / 100) * APART_MAX);
    else if (st.view === 'star') drawStar();
    else if (st.view === 'sheets') drawSheets();
    else drawStruts();
  }
  const legendOf = () => {
    if (!st) return [];
    if (st.view === 'sheets') return st.fins.classes.map((c, i) => ({ colour: classColour(i), label: `${c.sides.map(num).join(' · ')} ×${c.count}` }));
    if (st.view === 'struts') return st.struts.classes.map((c, i) => ({ colour: classColour(i), label: `${num(c.len)} ×${c.count}` }));
    return [];
  };

  return {
    root,
    get on() { return !!st; },
    get view() { return st?.view ?? 'pyramids'; },
    get apart() { return st?.apart ?? 40; },
    /** Start on a shape spec ({ vertices, faces }) in colour `colour`, placed by `transform` ({ position, quaternion }), at `view`. */
    start(spec, colour, transform, view = 'pyramids') {
      const solid = vacuusSolidOf(spec);
      if (!solid) return false;
      st = { solid, colour: new THREE.Color(colour), view: VACUUS_VIEWS.includes(view) ? view : 'pyramids', apart: st?.apart ?? 40,
        fins: finsOf(solid), struts: strutsOf(solid), tips: starTipsOf(solid) };
      // drawn about O (vacuus-geometry centres it), put back where the shape stands
      const m = [0, 1, 2].map((k) => spec.vertices.reduce((s, v) => s + v[k], 0) / spec.vertices.length);
      const q = new THREE.Quaternion(...(transform?.quaternion ?? [0, 0, 0, 1]));
      root.quaternion.copy(q);
      root.position.set(...(transform?.position ?? [0, 0, 0])).add(new THREE.Vector3(...m).applyQuaternion(q));
      draw();
      return true;
    },
    setView(view) { if (st && VACUUS_VIEWS.includes(view) && view !== st.view) { st.view = view; draw(); } },
    setApart(a) { if (!st) return; st.apart = Math.max(0, Math.min(100, Number(a) || 0)); if (st.view === 'exploded') draw(); },
    reset() { st = null; clear(); root.visible = false; },
    setVisible(on) { root.visible = on && !!st; if (root.visible) draw(); },
    redraw() { if (st) draw(); },
    /** How far the picture now reaches from O, for framing each view on its own shape: the star's tips; the pyramids as far as they
     *  are drawn apart (Pyramids' small gap, Exploded's slider); else the solid's circumradius. */
    get reach() {
      if (!st) return 0;
      const R = st.solid.R;
      if (st.view === 'star') return Math.max(R, ...st.tips.map((p) => Math.hypot(...p)));
      if (st.view === 'pyramids' || st.view === 'exploded') {
        const d = (st.view === 'pyramids' ? GAP : (st.apart / 100) * APART_MAX) * R;
        return Math.max(d, ...pyramidsOf(st.solid).flatMap(({ base, n }) => base.map((p) => Math.hypot(p[0] + d * n[0], p[1] + d * n[1], p[2] + d * n[2]))));
      }
      return R;
    },
    caption(L) {
      if (!st) return '';
      const s = st.solid, v = st.view;
      const one = (k) => (k === 1 ? '1' : '');   // all congruent / all one length: its own wording
      if (v === 'sheets') return t(`poly.vac.cap.sheets${one(st.fins.classes.length)}`, L, { e: s.edges.length, k: st.fins.classes.length });
      if (v === 'struts') return t(`poly.vac.cap.struts${one(st.struts.classes.length)}`, L, { v: s.vertices.length, k: st.struts.classes.length });
      const cap = t(`poly.vac.cap.${v}`, L, { n: s.faces.length });
      return v === 'star' && isCube(s) ? cap + t('poly.vac.cap.starCube', L) : cap;   // DICTO 11-04: name the cube's Star
    },
    /** The colour key for Sheets and Struts: [{ colour, label }]. */
    legend: legendOf,
    /** For the browser tests (?probe): the state in numbers. */
    probe() {
      if (!st) return null;
      return { view: st.view, apart: st.apart, corners: st.solid.vertices.length, faces: st.solid.faces.length, edges: st.solid.edges.length,
        finClasses: st.fins.classes.map((c) => c.count), strutClasses: st.struts.classes.map((c) => c.count), drawn: root.children.length, visible: root.visible };
    },
  };
}
