// A shape's printable net (step D4, from Polyhedraverse's NetViewer): the net unfolds off the first
// paint, folds up and back with a slider or a tap, and downloads as an A4 PDF with numbered glue
// pairs and optional tabs (krp-core polyhedra-nets: netOf, printableNetPdf).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { netOf, triangulate } from '../krp-core/src/polyhedra-nets/unfold.js';
import { printableNetPdf } from '../krp-core/src/polyhedra-nets/printable.js';
import { t } from './i18n.js';
import { polyShapeName } from './poly-shapes.js';
import { theme } from './site.js';

const FOLD_MS = 1600;
let eligible = null;
/** The shapes with a printable net (krp-core's list), loaded once. */
export async function netEligible() {
  if (eligible) return eligible;
  try { eligible = new Set(await (await fetch(new URL('../krp-core/src/polyhedra-nets/eligible.json', import.meta.url))).json()); } catch { eligible = new Set(); }
  return eligible;
}

/** Mount the net viewer for shape `id` into `box`; returns a dispose function. */
export function mountNetViewer(box, id, L) {
  const spec = POLYHEDRA[id];
  box.innerHTML = `<div class="net-stage">${t('poly.net.unfolding', L)}</div>
    <div class="net-controls" hidden><button type="button" class="net-play"></button><input type="range" class="net-fold" min="0" max="1000" value="0" aria-label="${t('poly.net.fold', L)}"></div>
    <div class="net-controls net-print" hidden><label><input type="checkbox" class="net-tabs" checked> ${t('poly.net.tabs', L)}</label><button type="button" class="net-download">${t('poly.net.download', L)}</button></div>
    <div class="net-note" hidden></div>`;
  const stage = box.querySelector('.net-stage');
  let disposed = false, cleanup = () => {}, raf = 0, fold = 0, place = () => {};
  const timer = setTimeout(() => {
    const net = spec ? netOf(spec.vertices, spec.faces) : null;
    if (disposed) return;
    if (!net) { stage.textContent = t('poly.net.none', L); return; }
    stage.textContent = '';
    const th = theme();
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a10);
    const w = stage.clientWidth || 320, h = stage.clientHeight || 300;
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.01, 100);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
    renderer.domElement.style.touchAction = 'none';
    stage.appendChild(renderer.domElement);
    scene.add(new THREE.AmbientLight(0xffffff, 0.75));
    const light = new THREE.DirectionalLight(0xffffff, 1);
    camera.add(light); light.position.set(2, 3, 5); scene.add(camera);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 0.8; controls.maxDistance = 8;
    // Fit the flat net and the closed solid together into a unit-ish view.
    const bbox = new THREE.Box3();
    for (const tt of [0, 1]) net.at(tt).forEach((M, i) => net.faces[i].pts.forEach((p) => bbox.expandByPoint(new THREE.Vector3(...p).applyMatrix4(new THREE.Matrix4().fromArray(M)))));
    const r = bbox.getSize(new THREE.Vector3()).length() / 2 || 1, k = 1 / r;
    const root = new THREE.Group();
    root.scale.setScalar(k); root.position.copy(bbox.getCenter(new THREE.Vector3())).multiplyScalar(-k);
    scene.add(root);
    camera.position.set(0, -0.35, 2.6);
    const faceMat = new THREE.MeshStandardMaterial({ color: th.strongHex, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
    const lineMat = new THREE.LineBasicMaterial({ color: th.accentHex });
    const disposables = [faceMat, lineMat];
    const groups = net.faces.map((f, i) => {
      const g = new THREE.Group(); g.matrixAutoUpdate = false;
      const pos = [];
      for (const tri of triangulate(net.flat[i])) for (const j of tri) pos.push(...f.pts[j]);
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.computeVertexNormals();
      const line = new THREE.BufferGeometry().setFromPoints([...f.pts, f.pts[0]].map((p) => new THREE.Vector3(...p)));
      disposables.push(geo, line);
      g.add(new THREE.Mesh(geo, faceMat), new THREE.Line(line, lineMat));
      root.add(g);
      return g;
    });
    place = (tt) => net.at(tt).forEach((M, i) => { groups[i].matrix.fromArray(M); groups[i].matrixWorldNeedsUpdate = true; });
    place(0);
    let frame = 0;
    const animate = () => { controls.update(); renderer.render(scene, camera); frame = requestAnimationFrame(animate); };
    animate();
    cleanup = () => { cancelAnimationFrame(frame); controls.dispose(); disposables.forEach((d) => d.dispose()); renderer.dispose(); renderer.domElement.remove(); };
    // controls
    box.querySelectorAll('.net-controls, .net-note').forEach((el) => { el.hidden = false; });
    const slider = box.querySelector('.net-fold'), play = box.querySelector('.net-play');
    const setFold = (v) => { fold = v; slider.value = String(Math.round(v * 1000)); play.textContent = fold < 1 ? t('poly.net.foldUp', L) : t('poly.net.unfold', L); place(v); };
    setFold(0);
    slider.addEventListener('input', () => { cancelAnimationFrame(raf); setFold(Number(slider.value) / 1000); });
    play.addEventListener('click', () => {
      cancelAnimationFrame(raf);
      const from = fold, to = from < 1 ? 1 : 0, t0 = performance.now();
      const step = (now) => { const q = Math.min(1, (now - t0) / (FOLD_MS * Math.abs(to - from) || 1)); setFold(from + (to - from) * q * q * (3 - 2 * q)); if (q < 1) raf = requestAnimationFrame(step); };
      raf = requestAnimationFrame(step);
    });
    box.querySelector('.net-note').textContent = t('poly.net.note', L, { n: net.faces.length, pairs: net.pairs.length });
    box.querySelector('.net-download').addEventListener('click', () => {
      const tabs = box.querySelector('.net-tabs').checked, name = polyShapeName(id).replaceAll('_', ' ');
      const bytes = printableNetPdf(net, { title: name, tabs, credit: 'Polyhedraverse by DICTO - polyhedraverse.dictospheres.com' });
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/pdf' }));
      const a = document.createElement('a'); a.href = url; a.download = `${name.toLowerCase().replaceAll(' ', '-')}-net${tabs ? '-tabs' : ''}.pdf`;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
    });
  }, 30);
  return () => { disposed = true; clearTimeout(timer); cancelAnimationFrame(raf); cleanup(); };
}
