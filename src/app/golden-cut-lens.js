// ✂ Golden Cut (DICTO, paper #88): Polyhedraverse's view of a Platonic solid cut the same depth x at every corner, live as the slider
// moves (the geometry is golden-cut-geometry.js). The regular corner polygons gold, the truncated faces in the solid's own colour, so
// the cut reads at a glance. While it is on, its drawing stands in for the build, as DICTO Vacuus's and the ★ Star step's do. Drawn
// to the render standard (docs/RENDER-STANDARD.md) and with DICTO Vacuus's look: solid faces with polygon offset, crisp screen-space
// edges of 2 px.
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { GCUT_IDS, GCUT_STOPS, X_MIN, X_MAX, stopX, stopAt, sidesAt, goldenCut } from './golden-cut-geometry.js';
import { t } from './i18n.js';

const EDGE = 0x0b1220;
/** The corner polygons' gold (the app's gold piece colour, as DICTO Vacuus's first class colour). */
export const GCUT_GOLD = 0xd9a520;
/** Dragging the slider this close to a stop lands on it exactly. */
const SNAP = 0.004;

export function createGoldenCutLens({ scene, look = () => ({ skeleton: false, opacity: 1 }) }) {
  const root = new THREE.Group();
  root.visible = false;
  scene.add(root);
  let st = null;      // { key, colour, x, R }

  const mat = (color) => new THREE.MeshStandardMaterial({ color, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.55 });
  const faceMat = mat(0xffffff), cornerMat = mat(GCUT_GOLD);
  const lineMat = new LineMaterial({ color: EDGE, linewidth: 2 });

  function clear() {
    for (const c of [...root.children]) { root.remove(c); c.geometry.dispose(); }
  }
  function mesh(loops, material) {
    const tris = loops.flatMap((L) => L.slice(1, -1).map((_, i) => [L[0], L[i + 1], L[i + 2]]));   // every loop convex: a fan
    const pos = new Float32Array(tris.length * 9);
    tris.forEach((tr, i) => tr.forEach((p, k) => pos.set(p, i * 9 + k * 3)));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.computeVertexNormals();
    root.add(new THREE.Mesh(g, material));
  }
  function draw() {
    clear();
    if (!st) return;
    const { skeleton, opacity } = look(), see = opacity < 1;
    for (const m of [faceMat, cornerMat]) { m.transparent = see; m.opacity = see ? opacity : 1; m.depthWrite = !see; m.visible = !skeleton; }
    faceMat.color.copy(st.colour);
    const cs = goldenCut(st.key, st.x);
    mesh(cs.faces, faceMat);
    mesh(cs.corners, cornerMat);
    // every edge once: each lies on exactly one corner polygon
    const g = new LineSegmentsGeometry();
    g.setPositions(cs.corners.flatMap((L) => L.flatMap((p, i) => [...p, ...L[(i + 1) % L.length]])).concat(
      cs.faces.flatMap((L) => L.flatMap((p, i) => (i % 2 ? [] : [...p, ...L[(i + 1) % L.length]])))));   // and the faces' original sides
    lineMat.color.setHex(skeleton ? 0xffffff : EDGE);
    const l = new LineSegments2(g, lineMat);
    l.frustumCulled = false;
    root.add(l);
  }

  return {
    root,
    get on() { return !!st; },
    get key() { return st?.key ?? null; },
    get x() { return st?.x ?? NaN; },
    /** The stop the cut is at, else null. */
    get stop() { return st ? stopAt(st.key, st.x) : null; },
    /** The uncut solid's circumradius: the frame stays on it, so the cut is seen eating into a still solid. */
    get reach() { return st?.R ?? 0; },
    /** Start on solid `key` in colour `colour`, placed by `transform` ({ position, quaternion }), at a stop or a cut x. */
    start(key, colour, transform, at = 'greater') {
      if (!GCUT_IDS[key]) return false;
      const x = typeof at === 'number' ? Math.min(X_MAX, Math.max(X_MIN, at)) : stopX(key, GCUT_STOPS.includes(at) ? at : 'greater');
      const R = Math.max(...goldenCut(key, 0).vertices.map((p) => Math.hypot(...p)));
      st = { key, colour: new THREE.Color(colour), x, R };
      // drawn about the solid's centre (golden-cut-geometry centres it), put back where the shape stands
      const V = POLYHEDRA[GCUT_IDS[key]].vertices, m = [0, 1, 2].map((k) => V.reduce((s, v) => s + v[k], 0) / V.length);
      const q = new THREE.Quaternion(...(transform?.quaternion ?? [0, 0, 0, 1]));
      root.quaternion.copy(q);
      root.position.set(...(transform?.position ?? [0, 0, 0])).add(new THREE.Vector3(...m).applyQuaternion(q));
      draw();
      return true;
    },
    /** Snap exactly to a stop. */
    setStop(stop) { if (st && GCUT_STOPS.includes(stop)) { st.x = stopX(st.key, stop); draw(); } },
    /** The slider: x, landing on a stop when within SNAP of it. */
    setX(x) {
      if (!st) return;
      x = Math.min(X_MAX, Math.max(X_MIN, Number(x) || X_MIN));
      const near = GCUT_STOPS.map((s) => stopX(st.key, s)).find((s) => Math.abs(s - x) <= SNAP);
      st.x = near ?? x;
      draw();
    },
    reset() { st = null; clear(); root.visible = false; },
    setVisible(on) { root.visible = on && !!st; if (root.visible) draw(); },
    redraw() { if (st) draw(); },
    /** The name at a stop ("Greater Golden Cut Dodecahedron", Icosaxes …), else ''. */
    name(L) {
      const s = this.stop;
      if (!st || !s) return '';
      if (s === 'archimedean') return t(`poly.gcut.arch.${st.key}`, L);
      if (st.key === 'octahedron') return t(`poly.gcut.oct.${s}`, L);
      return t(`poly.gcut.name.${s}`, L, { solid: t(`ar.solid.${st.key}`, L) });
    },
    /** The heading: the name at a stop, else the solid cut between stops. */
    title(L) { return st ? this.name(L) || t('poly.gcut.free', L, { solid: t(`ar.solid.${st.key}`, L) }) : ''; },
    /** The numbers line: x, the two sides, long/short. */
    caption(L) {
      if (!st) return '';
      const { corner, original, ratio } = sidesAt(st.key, st.x), f = (v) => v.toFixed(4);
      const s = this.stop, gold = s === 'greater' || s === 'lesser';
      return t('poly.gcut.cap', L, { x: f(st.x), c: f(corner), o: f(original), r: `${ratio.toFixed(4)}${gold ? ' = φ' : ''}` });
    },
    /** For the browser tests (?probe): the state in numbers. */
    probe() {
      if (!st) return null;
      const cs = goldenCut(st.key, st.x), sd = sidesAt(st.key, st.x);
      return { key: st.key, x: st.x, stop: this.stop, ratio: sd.ratio, corner: sd.corner, original: sd.original,
        corners: cs.corners.length, faces: cs.faces.length, drawn: root.children.length, visible: root.visible };
    },
  };
}
