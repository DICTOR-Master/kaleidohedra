// The shape details' special viewers (step D4, from Polyhedraverse's browser): a small turning 3D view
// (drag to turn) of a star polyhedron with its true star faces, of a shape's 4D prism (the shape, its
// far copy and a prism cell on every face, as a 3D shadow), or, for the 4D-capable shapes, the whole
// 4D polytope it extends to, every cell projected (krp-core: starTriangulation, duoprism,
// radialProjection). Reference views only, apart from the build.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { ConvexGeometry } from 'three/addons/geometries/ConvexGeometry.js';
import { STAR_POLYHEDRA } from '../krp-core/src/polyhedra/starPolyhedra.js';
import { triangulateStarFace } from '../krp-core/src/polyhedra/starTriangulation.js';
import { buildDuoprismShadow } from '../krp-core/src/polyhedra/duoprism.js';
import { buildRadialProjectionScene } from '../krp-core/src/polyhedra/radialProjection.js';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { theme } from './site.js';

// A small 3D stage in `box`: build(root) fills the group; the view fits it and turns slowly until
// dragged. Returns dispose.
function stage(box, build) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a10);
  const w = box.clientWidth || 320, h = box.clientHeight || 300;
  const camera = new THREE.PerspectiveCamera(45, w / h, 0.01, 200);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(w, h);
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
  renderer.domElement.style.touchAction = 'none';
  box.appendChild(renderer.domElement);
  scene.add(new THREE.AmbientLight(0xffffff, 0.7));
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(2, 3, 5); camera.add(light); scene.add(camera);
  const root = new THREE.Group();
  const disposables = build(root) ?? [];
  const bbox = new THREE.Box3().setFromObject(root), r = bbox.getSize(new THREE.Vector3()).length() / 2 || 1;
  root.position.copy(bbox.getCenter(new THREE.Vector3())).multiplyScalar(-1);
  const pivot = new THREE.Group(); pivot.add(root); pivot.scale.setScalar(1 / r); scene.add(pivot);
  camera.position.set(0, 0.4, 2.8);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 0.3; controls.maxDistance = 10;
  controls.autoRotate = true; controls.autoRotateSpeed = 1.2;
  controls.addEventListener('start', () => { controls.autoRotate = false; });
  let frame = 0;
  const animate = () => { controls.update(); renderer.render(scene, camera); frame = requestAnimationFrame(animate); };
  animate();
  return () => { cancelAnimationFrame(frame); controls.dispose(); disposables.forEach((d) => d.dispose?.()); renderer.dispose(); renderer.domElement.remove(); };
}
const material = (opts) => new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, ...opts });
function meshOfTriangles(tris, mat) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(tris.flat(2), 3));
  g.computeVertexNormals();
  return [new THREE.Mesh(g, mat), g];
}
function edgesOf(spec, offset = [0, 0, 0], mat) {
  const pos = spec.edges.flatMap(([a, b]) => [...spec.vertices[a].map((x, i) => x + offset[i]), ...spec.vertices[b].map((x, i) => x + offset[i])]);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  return [new THREE.LineSegments(g, mat), g];
}

/** A Kepler–Poinsot solid with its real star faces. */
export function mountStarView(box, id) {
  const s = STAR_POLYHEDRA[id], th = theme();
  return stage(box, (root) => {
    const mat = material({ color: th.strongHex }), line = new THREE.LineBasicMaterial({ color: th.accentHex });
    const tris = s.faces.flatMap((f) => triangulateStarFace(f.map((i) => s.vertices[i])));
    const [m, g] = meshOfTriangles(tris, mat), [l, lg] = edgesOf(s, undefined, line);
    root.add(m, l);
    return [mat, line, g, lg];
  });
}
/** A shape's 4D prism as a 3D shadow: the shape, its far copy, and a see-through prism cell per face. */
export function mountDuoprismView(box, id) {
  const s = POLYHEDRA[id], th = theme();
  return stage(box, (root) => {
    const { offset, walls } = buildDuoprismShadow(s);
    const solid = material({ color: th.strongHex }), wall = material({ color: th.contrastHex, transparent: true, opacity: 0.25, depthWrite: false }), line = new THREE.LineBasicMaterial({ color: th.accentHex });
    const tris = (spec, off) => spec.faces.flatMap((f) => f.slice(1, -1).map((_, i) => [f[0], f[i + 1], f[i + 2]].map((k) => spec.vertices[k].map((x, j) => x + off[j]))));
    const out = [solid, wall, line];
    for (const off of [[0, 0, 0], offset]) { const [m, g] = meshOfTriangles(tris(s, off), solid); const [l, lg] = edgesOf(s, off, line); root.add(m, l); out.push(g, lg); }
    const wt = walls.flatMap((w) => w.faces.slice(2).flatMap((f) => f.slice(1, -1).map((_, i) => [f[0], f[i + 1], f[i + 2]].map((k) => w.verts[k]))));
    const [wm, wg] = meshOfTriangles(wt, wall); root.add(wm); out.push(wg);
    return out;
  });
}
/** The whole 4D polytope a 4D-capable shape extends to, every cell projected in perspective. */
export function mountRadialView(box, id) {
  const s = POLYHEDRA[id], th = theme();
  return stage(box, (root) => {
    const { cellsVertices3D } = buildRadialProjectionScene(s);
    const line = new THREE.LineBasicMaterial({ color: th.accentHex, transparent: true, opacity: 0.7 });
    const out = [line];
    const centre = (pts) => pts.reduce((t, p) => t.map((x, i) => x + p[i] / pts.length), [0, 0, 0]);
    const far = Math.max(...cellsVertices3D.map((c) => Math.hypot(...centre(c))), 1e-6);
    cellsVertices3D.forEach((pts) => {
      const g = new ConvexGeometry(pts.map((p) => new THREE.Vector3(...p)));
      // nearer the centre, warmer and more solid: the inner cells read through the outer ones
      const d = Math.hypot(...centre(pts)) / far;
      const mat = material({ color: new THREE.Color(th.strongHex).lerp(new THREE.Color(th.contrastHex), d), transparent: true, opacity: 0.55 - 0.35 * d, depthWrite: false });
      root.add(new THREE.Mesh(g, mat), new THREE.LineSegments(new THREE.EdgesGeometry(g), line));
      out.push(g, mat);
    });
    return out;
  });
}
