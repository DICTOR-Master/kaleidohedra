// DICTO's Vacuus and Resonus in a polyhedron's details (DICTO 2026-11-25; ported from the archived Polyhedraverse, branch
// vacuus-resonus-view): the central planes through each edge (Vacuus) and parallel to each face (Resonus), on the 137 polyhedra of the
// exact catalogue. Either or both can be on; the view stands in for the preview. Under it: a one-line colour key, the centre switch
// (Johnson polyhedra whose corner and volume centroids differ; it opens on the corner centroid, DICTO's decision) and the info card.
// The card's counts come from the exact catalogue (data/vacuus-resonus-catalogue.json); the 3D planes are computed here from the
// polyhedron's own corners (vacuus-resonus.js) and checked against it by scripts/verify-vacuus-resonus.mjs.
// House look (docs/RENDER-STANDARD.md): see-through shell with crisp screen-space edges, planes with crisp outlines, and a pull-apart
// slider that lifts the shell's faces off the planes. Plane colours are a neutral set, none of them a polyhedron's colour in the app.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { analyse, cornerCentroid, volumeCentroid } from './vacuus-resonus.js';
import { t } from './i18n.js';

export const VR_COLORS = { vacuus: '#ff9a3c', resonus: '#3fd0e0', both: '#ff7ad9' };
const SHELL_COLOR = 0x47cc24, SHELL_EDGE = 0xa9f795;

let catalogue = null;
/** The exact catalogue, keyed by shape id (loaded once). */
export async function vrCatalogue() {
  if (!catalogue) catalogue = fetch(new URL('../../data/vacuus-resonus-catalogue.json', import.meta.url)).then((r) => r.json()).catch(() => ({}));
  return catalogue;
}

function lineObject(pairs, color, width, resolution, opacity = 1) {
  const geo = new LineSegmentsGeometry();
  geo.setPositions(pairs.flatMap(([a, b]) => [...a, ...b]));
  const mat = new LineMaterial({ color: new THREE.Color(color), linewidth: width, transparent: opacity < 1, opacity, depthWrite: opacity === 1 });
  mat.resolution = resolution;
  return new LineSegments2(geo, mat);
}
const loop = (poly) => poly.map((p, k) => [p, poly[(k + 1) % poly.length]]);
function fan(poly) {
  const out = [];
  for (let k = 1; k + 1 < poly.length; k++) out.push(...poly[0], ...poly[k], ...poly[k + 1]);
  return out;
}
function meshOf(positions, color, opacity) {
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geo.computeVertexNormals();
  return new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: new THREE.Color(color), transparent: true, opacity, side: THREE.DoubleSide, depthWrite: false, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }));
}
const disposeTree = (o) => o.traverse((x) => { x.geometry?.dispose?.(); x.material?.dispose?.(); });

/** The 3D view in `box`: draw({ spec, vacuus, resonus, centre }) redraws, keeping the angle; setPull(0..1); dispose(). */
function createViewer(box) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a10);
  const w = () => box.clientWidth || 320, h = () => box.clientHeight || 320;
  const camera = new THREE.PerspectiveCamera(45, w() / h(), 0.1, 100);
  camera.position.set(0.6, 0.9, 3.6);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(w(), h());
  renderer.domElement.style.display = 'block';
  renderer.domElement.style.touchAction = 'none';
  renderer.domElement.classList.add('vr-canvas');
  box.appendChild(renderer.domElement);
  scene.add(new THREE.AmbientLight(0xffffff, 0.75));
  const light = new THREE.DirectionalLight(0xffffff, 1.1);
  light.position.set(3, 4, 5); camera.add(light); scene.add(camera);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 1.6; controls.maxDistance = 8;
  // One finger turns the polyhedron, two fingers zoom (phone and iPad).
  controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_ROTATE };
  controls.autoRotate = true; controls.autoRotateSpeed = 1.2;
  controls.addEventListener('start', () => { controls.autoRotate = false; });
  const resolution = new THREE.Vector2(w(), h());
  let group = null, faces = [], pull = 0;
  let frame = 0;
  const animate = () => { controls.update(); renderer.render(scene, camera); frame = requestAnimationFrame(animate); };
  animate();
  const ro = new ResizeObserver(() => { camera.aspect = w() / h(); camera.updateProjectionMatrix(); renderer.setSize(w(), h()); resolution.set(w(), h()); });
  ro.observe(box);
  const place = () => faces.forEach(({ obj, dir }) => obj.position.copy(dir).multiplyScalar(pull * 0.6));

  function draw({ spec, vacuus: showV, resonus: showR, centre }) {
    if (group) { scene.remove(group); disposeTree(group); }
    const O = centre === 'volume' ? volumeCentroid(spec) : cornerCentroid(spec);
    const vr = analyse(spec, O);
    const s = 1 / Math.max(...vr.corners.map((c) => Math.hypot(...c)));
    const sc = (p) => [p[0] * s, p[1] * s, p[2] * s];
    const C = vr.corners.map(sc);
    group = new THREE.Group();
    // See-through shell, one group per face so pull-apart can lift it.
    faces = spec.faces.map((f) => {
      const poly = f.map((i) => C[i]), g = new THREE.Group();
      g.add(meshOf(fan(poly), SHELL_COLOR, 0.16), lineObject(loop(poly), SHELL_EDGE, 2, resolution));
      const mid = poly.reduce((a, p) => a.add(new THREE.Vector3(...p)), new THREE.Vector3()).multiplyScalar(1 / poly.length);
      group.add(g);
      return { obj: g, dir: mid.normalize() };
    });
    group.add(new THREE.Mesh(new THREE.SphereGeometry(0.025, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff })));   // the centre
    const both = showV && showR;
    const colourOf = (inBoth, own) => (both && inBoth ? VR_COLORS.both : own);
    const planeKey = (n) => { const m = Math.abs(n[0]) > 1e-6 ? Math.sign(n[0]) : Math.abs(n[1]) > 1e-6 ? Math.sign(n[1]) : Math.sign(n[2]); return n.map((x) => (x * m).toFixed(5)).join(','); };
    const drawnBoth = new Set();
    // Many see-through planes stack up: the more there are, the fainter each one, so the crowd stays see-through and the outlines
    // carry the shape.
    const count = (showV ? vr.plates.length : 0) + (showR ? vr.resonus.length : 0);
    const plateOpacity = Math.min(0.2, Math.max(0.035, 1.4 / count)), finOpacity = Math.min(0.6, Math.max(0.12, 3 / count));
    const plate = (slice, colour) => { const poly = slice.map(sc); group.add(meshOf(fan(poly), colour, plateOpacity), lineObject(loop(poly), colour, 1.5, resolution, 0.9)); };
    if (showV) for (const p of vr.plates) {
      const colour = colourOf(p.both, VR_COLORS.vacuus);
      plate(p.slice, colour);
      if (both && p.both) drawnBoth.add(planeKey(p.normal));
      // Its fins: the triangle from O to each edge on the plate.
      group.add(meshOf(p.edges.flatMap((e) => [0, 0, 0, ...C[spec.edges[e][0]], ...C[spec.edges[e][1]]]), colour, finOpacity));
      group.add(lineObject(p.edges.map((e) => [C[spec.edges[e][0]], C[spec.edges[e][1]]]), colour, 2.5, resolution));
    }
    if (showR) for (const r of vr.resonus) {
      if (both && r.both && drawnBoth.has(planeKey(r.normal))) continue;
      plate(r.slice, colourOf(r.both, VR_COLORS.resonus));
    }
    scene.add(group);
    place();
  }
  return {
    draw,
    setPull(v) { pull = v; place(); },
    dispose() { cancelAnimationFrame(frame); ro.disconnect(); controls.dispose(); if (group) disposeTree(group); renderer.dispose(); renderer.domElement.remove(); },
  };
}

/** The Vacuus / Resonus panel for shape `id` in `box`: view, pull-apart, key, centre switch, card. update({ vacuus, resonus }) redraws
 *  for the toggles; returns dispose. */
export function mountVacuusResonus(box, id, spec, entry, L) {
  const johnson = 'volume' in entry, same = johnson && entry.sameCentre;
  let centre = 'corner', on = { vacuus: false, resonus: false };
  box.innerHTML = `<div class="vr-stage"><div class="vr-view" aria-label="${t('vr.viewerLabel', L)}"></div>
      <label class="vr-pull"><span>${t('vr.pullApart', L)}</span><input type="range" min="0" max="100" value="0" data-vr-pull aria-label="${t('vr.pullApart', L)}"></label></div>
    <div class="vr-key" data-vr-key></div>
    ${johnson && !same ? `<div class="vr-centre" role="group" aria-label="${t('vr.centre', L)}" data-vr-centre><span>${t('vr.centre', L)}</span>
      <button type="button" data-vr-centre-pick="corner" aria-pressed="true">${t('vr.centreCorner', L)}</button>
      <button type="button" data-vr-centre-pick="volume" aria-pressed="false">${t('vr.centreVolume', L)}</button></div>` : ''}
    <div class="vr-card" data-vr-card></div>`;
  const viewer = createViewer(box.querySelector('.vr-view'));
  const swatch = (colour, label, title = '') => `<span class="vr-swatch"${title ? ` title="${title}"` : ''}><i style="background:${colour}"></i>${label}</span>`;
  const sphere = (s) => t('vr.sphere', L, { V: s[0], E: s[1], R: s[2] });
  function render() {
    const card = johnson && centre === 'volume' ? entry.volume : entry.corner, v = card.vacuus, r = card.resonus;
    box.querySelector('[data-vr-key]').innerHTML = (on.vacuus ? swatch(VR_COLORS.vacuus, 'Vacuus', t('vr.vacuusKey', L)) : '')
      + (on.resonus ? swatch(VR_COLORS.resonus, 'Resonus', t('vr.resonusKey', L)) : '')
      + (on.vacuus && on.resonus && card.both > 0 ? swatch(VR_COLORS.both, t('vr.inBoth', L)) : '');
    box.querySelector('[data-vr-card]').innerHTML = (same ? `<div>${t('vr.centre', L)}: ${t('vr.centresEqual', L)}</div>` : '')
      + (on.vacuus ? `<div data-vr-card-vacuus><div class="vr-head" style="color:${VR_COLORS.vacuus}">Vacuus</div>
        <div>${t('vr.plates', L, { n: v.plates, full: v.full, shared: v.shared, single: v.single })}; ${t('vr.mirrors', L, { n: v.onMirrors })}</div>
        <div>${t('vr.kind', L, { kind: v.kind })}</div>
        <div>${sphere(v.sphere)}; ${t(v.simplicial ? 'vr.simplicial' : 'vr.notSimplicial', L)}</div></div>` : '')
      + (on.resonus ? `<div data-vr-card-resonus><div class="vr-head" style="color:${VR_COLORS.resonus}">Resonus</div>
        <div>${t('vr.resPlanes', L, { n: r.planes, two: r.twoFaces, one: r.oneFace })}; ${t('vr.mirrors', L, { n: r.onMirrors })}</div>
        <div>${sphere(r.sphere)}; ${t(r.simplicial ? 'vr.simplicial' : 'vr.notSimplicial', L)}</div></div>` : '')
      + `<div class="vr-both" data-vr-card-both>${t('vr.both', L, { n: card.both })}</div><div class="vr-source">${t('vr.source', L)} <a href="/vacuus-resonus/" data-vr-builds>${t('vr.builds', L)}</a></div>`;
    box.querySelectorAll('[data-vr-centre-pick]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.vrCentrePick === centre)));
    viewer.draw({ spec, vacuus: on.vacuus, resonus: on.resonus, centre });
  }
  box.querySelector('[data-vr-pull]').addEventListener('input', (e) => viewer.setPull(Number(e.target.value) / 100));
  box.querySelector('[data-vr-centre]')?.addEventListener('click', (e) => { const c = e.target.closest('[data-vr-centre-pick]')?.dataset.vrCentrePick; if (c && c !== centre) { centre = c; render(); } });
  return {
    update(next) { on = { ...next }; render(); },
    dispose() { viewer.dispose(); box.innerHTML = ''; },
  };
}

export const VR_CSS = `
.poly-detail-preview[hidden] { display: none; }
.poly-detail-actions .poly-detail-vr { border-color: var(--vr) !important; color: var(--vr) !important; border-radius: 999px; }
.poly-detail-actions .poly-detail-vr[aria-pressed="true"] { background: var(--vr) !important; color: #04140a !important; font-weight: 700; }
.poly-detail-vrbox { width: 100%; max-width: 720px; display: flex; flex-direction: column; gap: 10px; align-items: center; }
.poly-detail-vrbox[hidden] { display: none; }
.vr-stage { position: relative; width: 100%; height: min(440px, 58vh); border-radius: 12px; overflow: hidden; background: #0a0a10; }
.vr-view { width: 100%; height: 100%; touch-action: none; }
.vr-pull { position: absolute; left: 10px; right: 10px; bottom: 6px; display: flex; align-items: center; gap: 10px; color: #a9f795; font: var(--text-xs, 12px) var(--font-ui, sans-serif); white-space: nowrap; }
.vr-pull input { flex: 1; min-width: 0; height: 44px; accent-color: #5ee233; touch-action: none; }
.vr-key { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; color: #a9f795; font: var(--text-xs, 12px) var(--font-ui, sans-serif); }
.vr-key:empty { display: none; }
.vr-swatch { display: inline-flex; align-items: center; gap: 5px; }
.vr-swatch i { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.vr-centre { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; justify-content: center; color: #a9f795; font: var(--text-xs, 12px) var(--font-ui, sans-serif); }
.vr-centre button { background: none; color: #5ee233; border: 1px solid rgba(71, 204, 36, .4); border-radius: 999px; padding: 8px 14px; min-height: 40px; cursor: pointer; font: var(--text-s, 13px) var(--font-ui, sans-serif); }
.vr-centre button[aria-pressed="true"] { background: #2e8a17; color: #04140a; font-weight: 700; }
.vr-card { width: 100%; max-width: 420px; box-sizing: border-box; background: rgba(10, 14, 8, .78); border: 1px solid rgba(71, 204, 36, .25); border-radius: 10px; padding: 10px 14px; color: #c9f7bb; font: var(--text-xs, 12px)/1.45 var(--font-ui, sans-serif); }
.vr-card > div > div, .vr-card > div { margin: 2px 0; }
.vr-head { font-weight: 700; margin-top: 6px; }
.vr-both { margin-top: 6px !important; }
.vr-source { opacity: .7; font-size: 11px; margin-top: 6px !important; }
.vr-source a { color: #a9f795; }
`;
