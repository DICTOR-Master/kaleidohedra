// Soft (DICTO 2026-10-21): a view of any build in which every flat face bulges into a soft cap
// (krp-core puffed.js), with a finish: Plain (today's look), Metallic or Ceramic. View only: the real
// pieces stay underneath, unseen, for taps, fitting and snapping. One puffed geometry per shape and
// softness, shared by every copy. The choice is remembered per viewer on this device.
import * as THREE from 'three';
import { puffSpec, specFromTriangles } from '../krp-core/src/polyhedra/puffed.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { getSettings, onSettingsChange } from './settings.js';
import { t } from './i18n.js';

export const FINISHES = ['plain', 'metallic', 'ceramic'];
export const SOFT_MAX = 0.6;
const KEY = 'rv-soft-finish';
const SEAM_COLOR = 0x0b1220;

let state = { soft: false, finish: 'plain', amount: 0.25 };
try {
  const s = JSON.parse(localStorage.getItem(KEY) ?? 'null');
  if (s) state = { soft: s.soft === true, finish: FINISHES.includes(s.finish) ? s.finish : 'plain', amount: Number.isFinite(s.amount) ? Math.max(0, Math.min(SOFT_MAX, s.amount)) : 0.25 };
} catch { /* blocked storage: defaults */ }
const listeners = new Set();
export const softState = () => ({ ...state });
/** Anything to draw: Soft on, or a finish other than Plain (on the flat faces, Soft off). Flat + Plain is today's look. */
export const softActive = () => state.soft || state.finish !== 'plain';
/** The bulge in use: the Softness while Soft is on, else flat. */
export const softAmount = () => (state.soft ? state.amount : 0);
export function onSoftChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }
export function setSoft(patch) {
  state = { ...state, ...patch };
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* best-effort */ }
  for (const fn of listeners) fn(softState());
}

// ---- geometry: one per shape (or drawn geometry) and softness, least recently used dropped ----
const CACHE_MAX = 200;
const cache = new Map();
export const softStats = { made: 0 };
function remember(key, make) {
  if (cache.has(key)) { const g = cache.get(key); cache.delete(key); cache.set(key, g); return g; }
  const g = make();
  softStats.made++;
  cache.set(key, g);
  while (cache.size > CACHE_MAX) { const [k, old] = cache.entries().next().value; cache.delete(k); old.dispose(); }
  return g;
}
function toGeometry(p, faceColours) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(p.positions, 3));
  g.setAttribute('normal', new THREE.BufferAttribute(p.normals, 3));
  const col = new Float32Array(p.positions.length).fill(1), c = new THREE.Color();
  if (faceColours) for (let i = 0; i < p.faceIds.length; i++) { c.setHex(faceColours[p.faceIds[i]] ?? 0xffffff); col.set([c.r, c.g, c.b], 3 * i); }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.computeBoundingSphere();
  g.userData = { puffed: true, seams: p.seams, triangles: p.triangles, faceIds: p.faceIds };
  return g;
}
/** The puffed geometry of a piece spec (vertices + faces, optional faceColours), cached under `key`. */
export function puffedFor(key, spec, amount = softAmount()) {
  return remember(`${key}|${amount.toFixed(3)}`, () => toGeometry(puffSpec(spec, { amount }), spec.faceColours));
}
/** The same for a shape that exists only as drawn triangles (the lattice worlds' cells). */
export function puffedForGeometry(geometry, amount = softAmount()) {
  return remember(`${geometry.uuid}|${amount.toFixed(3)}`, () => {
    const pos = geometry.attributes.position.array, idx = geometry.index?.array ?? null;
    return toGeometry(puffSpec(specFromTriangles(pos, idx), { amount }));
  });
}

// ---- finishes ----
let envTexture = null;
/** A soft studio light for reflections: a gradient room with two bright panels, through PMREM. */
export function initSoftEnvironment(renderer) {
  if (envTexture || !renderer) return;
  const room = new THREE.Scene();
  const sky = new THREE.SphereGeometry(10, 32, 16), col = [], c = new THREE.Color();
  const top = new THREE.Color(0xf4f6fb), mid = new THREE.Color(0x8a93a6), low = new THREE.Color(0x14161c);
  for (let i = 0; i < sky.attributes.position.count; i++) {
    const y = sky.attributes.position.getY(i) / 10;
    if (y > 0) c.copy(mid).lerp(top, y); else c.copy(mid).lerp(low, -y);
    col.push(c.r, c.g, c.b);
  }
  sky.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  room.add(new THREE.Mesh(sky, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide })));
  for (const [x, y, z, w, h] of [[6, 5, 4, 5, 3], [-7, 2, -3, 3, 4]]) {
    const panel = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }));
    panel.position.set(x, y, z); panel.lookAt(0, 0, 0); room.add(panel);
  }
  const pmrem = new THREE.PMREMGenerator(renderer);
  envTexture = pmrem.fromScene(room, 0.02).texture;
  pmrem.dispose();
  room.traverse((o) => { o.geometry?.dispose(); o.material?.dispose(); });
}
export function applyFinish(mat, finish = state.finish) {
  const env = finish === 'plain' ? null : envTexture;
  const set = {
    plain: { metalness: 0.15, roughness: 0.55, clearcoat: 0, clearcoatRoughness: 0, envMapIntensity: 1 },
    metallic: { metalness: 1, roughness: 0.2, clearcoat: 0, clearcoatRoughness: 0, envMapIntensity: 1.15 },
    ceramic: { metalness: 0, roughness: 0.32, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 0.75 },
  }[finish] ?? {};
  Object.assign(mat, set);
  if (mat.envMap !== env) { mat.envMap = env; mat.needsUpdate = true; }
  mat.userData.finish = finish;
  return mat;
}
export function finishMaterial(extra = {}) {
  return applyFinish(new THREE.MeshPhysicalMaterial({ color: 0xffffff, vertexColors: true, ...extra }));
}
export const seamMaterial = () => new THREE.LineBasicMaterial({ color: SEAM_COLOR, transparent: true, opacity: 0.6 });
const noPick = () => {};

/** Seam lines of `geometry` (puffed) at each of `matrices` (or once, untransformed). */
export function seamLines(geometry, matrices = null, material = seamMaterial()) {
  const s = geometry.userData.seams, n = matrices ? matrices.length : 1, out = new Float32Array(s.length * n), v = new THREE.Vector3();
  for (let k = 0; k < n; k++) for (let i = 0; i < s.length; i += 3) {
    v.set(s[i], s[i + 1], s[i + 2]);
    if (matrices) v.applyMatrix4(matrices[k]);
    out[k * s.length + i] = v.x; out[k * s.length + i + 1] = v.y; out[k * s.length + i + 2] = v.z;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(out, 3));
  const l = new THREE.LineSegments(g, material);
  l.raycast = noPick;
  return l;
}

// ---- twins for the lattice worlds: each drawn piece mesh gets an unpickable puffed copy as its child,
// sharing its instance matrices and colours; the original stays for taps (its material not drawn). ----
const SEAM_CAP = 3000; // instances with seam lines; above this the seams are the creases alone
export function createSoftTwins() {
  const twins = new Map(); // target -> record
  const seamMat = seamMaterial();
  function drop(tgt, rec) {
    tgt.remove(rec.twin);
    if (rec.seams) { tgt.remove(rec.seams); rec.seams.geometry.dispose(); }
    rec.mat.dispose();
    if (rec.srcMat) rec.srcMat.visible = true;
    twins.delete(tgt);
  }
  function sync(targets, on) {
    const live = new Set();
    if (on) for (const tgt of targets) {
      if (!tgt?.geometry?.attributes?.position || !tgt.material || Array.isArray(tgt.material)) continue;
      live.add(tgt);
      let rec = twins.get(tgt);
      if (!rec) {
        const mat = finishMaterial({ side: tgt.material.side });
        const twin = tgt.isInstancedMesh ? new THREE.InstancedMesh(new THREE.BufferGeometry(), mat, 1) : new THREE.Mesh(new THREE.BufferGeometry(), mat);
        twin.raycast = noPick; twin.frustumCulled = false; twin.userData.softTwin = true; twin.userData.noIcoScan = true;
        tgt.add(twin);
        rec = { twin, mat, base: null, amount: -1, sig: '', seams: null, srcMat: null, finish: null };
        twins.set(tgt, rec);
      }
      if (rec.srcMat !== tgt.material) { if (rec.srcMat) rec.srcMat.visible = true; rec.srcMat = tgt.material; }
      rec.srcMat.visible = false;
      if (rec.base !== tgt.geometry || rec.amount !== softAmount()) {
        rec.base = tgt.geometry; rec.amount = softAmount(); rec.sig = '';
        rec.twin.geometry = puffedForGeometry(tgt.geometry);
      }
      if (rec.finish !== state.finish) { applyFinish(rec.mat); rec.finish = state.finish; }
      const src = rec.srcMat, m = rec.mat;
      // the X-ray plane, Translucent and the ghosts follow the piece's own material
      if (m.clippingPlanes !== src.clippingPlanes) { m.clippingPlanes = src.clippingPlanes; seamMat.clippingPlanes = src.clippingPlanes; }
      if (m.transparent !== src.transparent) { m.transparent = src.transparent; m.needsUpdate = true; }
      m.opacity = src.opacity; m.depthWrite = src.depthWrite;
      if (src.color) m.color.copy(src.color);
      if (tgt.isInstancedMesh) {
        rec.twin.instanceMatrix = tgt.instanceMatrix;
        rec.twin.instanceColor = tgt.instanceColor;
        rec.twin.count = tgt.count;
      }
      const count = tgt.isInstancedMesh ? tgt.count : 1;
      const sig = `${count}:${tgt.instanceMatrix?.version ?? 0}:${rec.twin.geometry.uuid}:${state.soft}`;
      if (sig !== rec.sig) {
        rec.sig = sig;
        if (rec.seams) { tgt.remove(rec.seams); rec.seams.geometry.dispose(); rec.seams = null; }
        if (state.soft && count <= SEAM_CAP && count > 0) { // flat cells keep today's look: no lines
          const mats = tgt.isInstancedMesh ? Array.from({ length: count }, (_, i) => { const M = new THREE.Matrix4(); tgt.getMatrixAt(i, M); return M; }) : null;
          rec.seams = seamLines(rec.twin.geometry, mats, seamMat);
          rec.seams.userData.noIcoScan = true;
          tgt.add(rec.seams);
        }
      }
    }
    for (const [tgt, rec] of [...twins]) if (!live.has(tgt)) drop(tgt, rec);
  }
  return { sync, get size() { return twins.size; } };
}

// ---- the toolbar button and its panel ----
// The icon: a small square whose four sides bulge softly outward, a line drawing in the accent colour.
export const SOFT_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true"><path d="M6 6 Q12 3.2 18 6 Q20.8 12 18 18 Q12 20.8 6 18 Q3.2 12 6 6 Z"/></svg>';
export function mountSoftControls({ tools, before = null, showHudPrompt = () => {} }) {
  const btn = document.createElement('button');
  btn.type = 'button'; btn.id = 'soft-toggle'; btn.innerHTML = SOFT_ICON; btn.hidden = true;
  tools.insertBefore(btn, before);
  const panel = document.createElement('div');
  panel.id = 'soft-panel'; panel.className = 'qc-panel';
  panel.innerHTML = `<div class="w4d-row soft-mode"><button type="button" data-mode="flat"></button><button type="button" data-mode="soft"></button></div>
    <div class="w4d-row soft-finishes">${FINISHES.map((f) => `<button type="button" data-finish="${f}"></button>`).join('')}</div>
    <div class="w4d-row soft-amount"><label><span class="soft-amount-name"></span><input id="soft-amount" type="range" min="0" max="${Math.round(SOFT_MAX * 100)}" step="1"></label></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'soft');
  let open = false, applies = false;
  const slider = panel.querySelector('#soft-amount');
  function render() {
    const L = getSettings().language;
    btn.title = t('soft.title', L); btn.setAttribute('aria-label', t('soft.title', L));
    btn.classList.toggle('active', softActive());
    panel.querySelector('[data-mode=flat]').textContent = t('soft.flat', L);
    panel.querySelector('[data-mode=soft]').textContent = t('soft.soft', L);
    for (const b of panel.querySelectorAll('[data-mode]')) b.classList.toggle('active', (b.dataset.mode === 'soft') === state.soft);
    for (const b of panel.querySelectorAll('[data-finish]')) { b.textContent = t(`soft.${b.dataset.finish}`, L); b.classList.toggle('active', b.dataset.finish === state.finish); }
    panel.querySelector('.soft-amount-name').textContent = t('soft.amount', L);
    slider.title = t('soft.amount', L);
    slider.value = String(Math.round(state.amount * 100));
    panel.querySelector('.soft-amount').hidden = !state.soft; // the Softness slider only while Soft is on
    panel.classList.toggle('visible', open && applies);
  }
  btn.addEventListener('click', () => { open = !open; render(); });
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.mode) setSoft({ soft: b.dataset.mode === 'soft' });
    else if (b.dataset.finish) setSoft({ finish: b.dataset.finish });
    else return;
    render();
  });
  slider.addEventListener('input', () => { setSoft({ amount: Number(slider.value) / 100 }); });
  onSettingsChange(render);
  render();
  return {
    /** Shown only where Soft applies; elsewhere the button and its panel go. */
    setApplies(on) {
      if (on === applies) return;
      applies = on; btn.hidden = !on;
      if (!on) open = false;
      render();
    },
    get applies() { return applies; },
    close() { open = false; render(); },
  };
}
