// DICTO Shadow Form (DICTO 2026-10-24; DICTO's idea and name), the public demo, hosted by the Studies world as its study 'shadowForm'
// (?open=studies:shadowForm). Stage 1: place solids with their centres on the points of a grid, turn them, switch the grid, and flip
// to the negative view, where the space between them inside their convex hull is a solid coloured cast and the forms are glass.
//   Placing: tap a dot (a grid point) to put the chosen form there; tap a form to pick it, then a dot moves it there (two forms on one
//     point nest), a form button changes its shape, Container makes its inside count as space, Remove (or a long-press) takes it away.
//   Turning (DICTO 2026-10-24: "rotate one shape but all others move synchronised"): drag any form and every form turns with it, each
//     about its own grid point; with Snap turns on, the turn snaps on release to multiples of 15° or 36° about each axis.
//   Examples: DICTO's own void finds and classical nests, from their worlds' data (shadow-form-engine.js EXAMPLES).
// The geometry (grids, the shared turn, nesting, the negative through manifold-3d, volumes) is all in shadow-form-engine.js, with no
// DOM; this file is only the screen. manifold-3d loads from the CDN the first time the study opens. Words: i18n sf.*.
import * as THREE from 'three';
import * as E from './shadow-form-engine.js';
import { t } from './i18n.js';
import { getSettings } from './settings.js';
import { storageKey, theme } from './site.js';

const STORAGE_KEY = storageKey('shadow-form');
const EDGE_COLOR = 0x0b1220;
const GRID_REACH = 2;            // dots within this many steps of a form (index units) ...
const REACH_RADIUS = 2;         // ... and this far (index units): cubic 32, face-centred 18, body-centred 14 points round each form
const DRAG_SLOP = 6;             // px before a press on a form becomes a turn
const lang = () => getSettings().language;
const fmt = (v) => (Math.abs(v) < 5e-7 ? '0' : v.toFixed(v >= 100 ? 1 : 3));

export function createShadowForm({ panel, scene, fitView = () => {}, camera, controls, canvas, showHudPrompt = () => {} }) {
  let arr = E.START(), pick = 'cube', selected = null, viewNegative = false, snap = false, example = null;
  function read(d) {
    if (!d) return;
    if (d.arrangement) arr = E.normaliseArrangement(d.arrangement);
    if (E.FORM_KEYS.includes(d.pick)) pick = d.pick;
    snap = !!d.snap; viewNegative = !!d.negative;
    example = E.EXAMPLE_KEYS.includes(d.example) ? d.example : null;
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: the start */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ arrangement: arr, pick, snap, negative: viewNegative, example })); } catch { /* best-effort */ } };

  let active = false, wasm = null, loading = null, result = null, dirty = false, raf = 0;
  const holder = new THREE.Group(); holder.visible = false; scene.add(holder); // its own group (the Studies' group is cleared on each draw)

  // ---- materials ----
  const solidMat = new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const pickedMat = solidMat.clone();
  // see-through glass, as the app's crystal shells (light, no depth writes, edges carrying the shape)
  const glassMat = new THREE.MeshStandardMaterial({ color: 0xbfe6ff, roughness: 0.15, metalness: 0.1, transparent: true, opacity: 0.2, depthWrite: false, side: THREE.DoubleSide });
  const edgeMat = new THREE.LineBasicMaterial({ color: EDGE_COLOR });
  const glassEdgeMat = new THREE.LineBasicMaterial({ color: 0xdff4ff, transparent: true, opacity: 0.9 });
  const castMat = new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, roughness: 0.55, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const castEdgeMat = new THREE.LineBasicMaterial({ color: EDGE_COLOR, transparent: true, opacity: 0.6 });
  const dotMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.55 });
  const hitMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false });
  function styleMaterials() {
    const th = theme();
    solidMat.color.setHex(th.pieceHex);
    pickedMat.color.setHex(th.pieceHex).offsetHSL(0, 0, 0.18); pickedMat.emissive.setHex(th.accentHex).multiplyScalar(0.35);
    castMat.color.setHex(th.contrastHex);
    dotMat.color.setHex(th.accentHex);
  }

  // ---- form geometry (one per form kind) ----
  const geoCache = new Map();
  function formGeo(key) {
    if (geoCache.has(key)) return geoCache.get(key);
    const g = E.formGeometry(key);
    if (!g) return null;
    const pos = [];
    for (const f of g.faces) for (let m = 1; m + 1 < f.length; m++) for (const i of [f[0], f[m], f[m + 1]]) pos.push(...g.vertices[i]);
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.computeVertexNormals();
    const out = { geo, edges: new THREE.EdgesGeometry(geo, 8), r: Math.max(...g.vertices.map((v) => Math.hypot(...v))) };
    geoCache.set(key, out);
    return out;
  }

  // ---- drawing ----
  let nodes = [], formMeshes = [], dots = null, dotHits = null, dotIdx = [], cast = null;
  function clearHolder() {
    for (const c of [...holder.children]) { holder.remove(c); if (c.userData.own) { c.geometry?.dispose(); c.children.forEach((k) => k.geometry?.dispose()); } }
    nodes = []; formMeshes = []; dots = dotHits = cast = null; dotIdx = [];
  }
  const turnQ = () => new THREE.Quaternion(...E.turnOf(arr));
  function draw() {
    clearHolder();
    if (!active) return;
    styleMaterials();
    const s = arr.spacing;
    arr.forms.forEach((f, i) => {
      const G = formGeo(f.form);
      if (!G) return;
      const node = new THREE.Group(); node.position.set(...f.at.map((c) => c * s)); node.quaternion.copy(turnQ());
      const inner = new THREE.Group(); inner.position.set(...(f.offset ?? [0, 0, 0])); inner.quaternion.set(...(f.q ?? E.IDENTITY)); inner.scale.setScalar(f.scale ?? 1);
      const glass = viewNegative || f.container;
      const m = new THREE.Mesh(G.geo, glass ? glassMat : i === selected ? pickedMat : solidMat); m.userData.sf = { form: i };
      if (glass) m.renderOrder = 2;
      const l = new THREE.LineSegments(G.edges, glass ? glassEdgeMat : edgeMat);
      inner.add(m, l); node.add(inner); holder.add(node);
      nodes.push(node); formMeshes.push(m);
    });
    if (!viewNegative) {
      const list = dotPoints();
      const nn = E.neighbourDistance(arr.grid, s);
      dots = new THREE.InstancedMesh(new THREE.SphereGeometry(Math.min(0.07, nn * 0.06), 10, 6), dotMat, list.length);
      dotHits = new THREE.InstancedMesh(new THREE.SphereGeometry(nn * 0.3, 8, 6), hitMat, list.length);
      const M = new THREE.Matrix4();
      list.forEach((q, i) => { M.makeTranslation(...q.map((c) => c * s)); dots.setMatrixAt(i, M); dotHits.setMatrixAt(i, M); });
      dots.userData.own = dotHits.userData.own = true; dotHits.userData.sf = { dots: true };
      dotIdx = list;
      holder.add(dots, dotHits);
    } else drawCast();
  }
  // The dots: the grid points next to the forms (one step in each direction), or round the centre when there are none; not a whole
  // cloud of grid, which would hide the forms and make taps land on the wrong point.
  function dotPoints() {
    const keys = new Set(), list = [], put = (q) => { const k = q.join(','); if (!keys.has(k) && E.onGrid(arr.grid, q)) { keys.add(k); list.push(q); } };
    const seeds = arr.forms.length ? arr.forms.map((f) => f.at) : [[0, 0, 0]];
    for (const c of seeds) for (let i = -GRID_REACH; i <= GRID_REACH; i++) for (let j = -GRID_REACH; j <= GRID_REACH; j++) for (let k = -GRID_REACH; k <= GRID_REACH; k++) {
      const q = [c[0] + i, c[1] + j, c[2] + k];
      if (Math.hypot(i, j, k) <= REACH_RADIUS + 1e-9) put(q);
    }
    return list;
  }
  function drawCast() {
    if (cast) { holder.remove(cast); cast.geometry.dispose(); cast.children.forEach((k) => k.geometry.dispose()); cast = null; }
    if (!viewNegative || !result?.positions) return;
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(result.positions, 3)); geo.computeVertexNormals();
    cast = new THREE.Mesh(geo, castMat); cast.userData = { own: true, sf: { cast: true } };
    cast.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), castEdgeMat));
    holder.add(cast);
  }

  // ---- the negative (manifold-3d, loaded the first time the study opens) ----
  function ensureEngine() {
    return (loading ??= Promise.all([E.loadManifold(), E.loadFormData()]).then(([w]) => { wasm = w; }).catch((err) => { loading = null; throw err; }));
  }
  function compute() {
    raf = 0;
    if (!wasm || !active) return;
    dirty = false;
    const r = E.shadowForm(arr, wasm);
    result = { hullVolume: r.hullVolume, formsVolume: r.formsVolume, negativeVolume: r.negativeVolume, positions: r.negative ? E.meshOf(r.negative).positions : null };
    r.negative?.delete();
    drawCast(); renderReadout();
  }
  function schedule() { dirty = true; if (!raf && wasm) raf = requestAnimationFrame(compute); }

  // ---- fitting the view ----
  /** Fit the view to the forms; exact: zoom in as well as out (a new example, or opening the study). */
  function fit(exact = false) {
    if (!arr.forms.length) { fitView([0, 0, 0], 2 * arr.spacing * 1.1, null, exact); return; }
    const cs = arr.forms.map((f) => f.at.map((c) => c * arr.spacing)), c = [0, 1, 2].map((a) => cs.reduce((t0, p) => t0 + p[a], 0) / cs.length);
    const r = Math.max(...arr.forms.map((f, i) => Math.hypot(...cs[i].map((x, a) => x - c[a])) + Math.hypot(...(f.offset ?? [0, 0, 0])) + (formGeo(f.form)?.r ?? 1) * (f.scale ?? 1)));
    // the forms fill the view; in the forms view at least one grid step round them shows (more dots run off the edges)
    fitView(c, Math.max(r, viewNegative ? 0 : E.neighbourDistance(arr.grid, arr.spacing) * 1.2) * 1.1, null, exact);
  }

  // ---- taps (through the app's build taps: 'build' = tap, 'chisel' = long-press) ----
  let lastTurnAt = 0;
  function handleTap(hit, mode) {
    const ud = hit?.object?.userData?.sf;
    if (!ud || !active) return false;
    if (performance.now() - lastTurnAt < 400) return true; // the release of a turn, not a tap
    if (ud.form !== undefined) {
      if (mode === 'chisel') { remove(ud.form); return true; }
      selected = selected === ud.form ? null : ud.form;
      commit(false);
      return true;
    }
    if (ud.dots && hit.instanceId !== undefined) {
      const at = dotIdx[hit.instanceId];
      if (!at) return false;
      // a dot's touch target is wider than the dot: a tap beside the dot that goes on to a form is a tap on that form
      const o = camera.position.clone(), dir = hit.point.clone().sub(o).normalize(), c = new THREE.Vector3(...at.map((x) => x * arr.spacing));
      const off = c.clone().sub(o).cross(dir).length(), behind = new THREE.Raycaster(o, dir).intersectObjects(formMeshes, false)[0];
      if (behind && off > Math.max(0.1, E.neighbourDistance(arr.grid, arr.spacing) * 0.1)) return handleTap(behind, mode);
      if (mode === 'chisel') return false;
      if (selected !== null && arr.forms[selected]) arr.forms[selected].at = [...at];
      else { arr.forms.push({ form: pick, at: [...at] }); }
      example = null;
      commit(true);
      return true;
    }
    return false;
  }
  function remove(i) {
    arr.forms.splice(i, 1);
    if (selected === i) selected = null; else if (selected > i) selected--;
    example = null;
    commit(true);
  }
  function commit(changed) { save(); draw(); renderPanel(); if (changed) schedule(); }

  // ---- turning: drag any form, all of them turn (each about its own grid point) ----
  let drag = null;
  const ray = new THREE.Raycaster();
  function formUnder(e) {
    const rect = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1), camera);
    return ray.intersectObjects(formMeshes, false)[0] ?? null;
  }
  function applyTurn() { const q = turnQ(); for (const n of nodes) n.quaternion.copy(q); }
  function onDown(e) {
    if (drag) { endDrag(false); return; } // a second finger: leave it to the camera
    if (!active || e.target !== canvas || e.button > 0 || !formMeshes.length || !formUnder(e)) return;
    drag = { id: e.pointerId, x: e.clientX, y: e.clientY, moved: false, controls: controls?.enabled ?? true };
    if (controls) controls.enabled = false; // the camera stays still while the forms turn
  }
  function onMove(e) {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.moved && Math.hypot(dx, dy) < DRAG_SLOP) return;
    drag.moved = true; drag.x = e.clientX; drag.y = e.clientY;
    const k = (2 * Math.PI) / Math.max(200, canvas.getBoundingClientRect().height);
    const up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion), right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
    const dq = E.qmul(E.qAxisAngle(up.toArray(), dx * k), E.qAxisAngle(right.toArray(), dy * k));
    arr.turn = E.qnorm(E.qmul(dq, E.turnOf(arr)));
    applyTurn(); schedule();
  }
  function endDrag(release = true) {
    if (!drag) return;
    if (controls) controls.enabled = drag.controls;
    const moved = drag.moved; drag = null;
    if (!moved || !release) return;
    lastTurnAt = performance.now();
    if (snap) { arr.turn = E.snapTurn(E.turnOf(arr)); applyTurn(); }
    save(); schedule(); renderPanel();
  }
  const onUp = (e) => { if (drag && e.pointerId === drag.id) endDrag(true); };
  window.addEventListener('pointerdown', onDown, true);
  window.addEventListener('pointermove', onMove, true);
  window.addEventListener('pointerup', onUp, true);
  window.addEventListener('pointercancel', onUp, true);

  // ---- panel rows (direct children of the Studies panel, so the slider sits lowest as in every world) ----
  const style = document.createElement('style');
  style.textContent = `.sf-row[hidden]{display:none!important}
.qc-panel .sf-chips{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;-webkit-overflow-scrolling:touch;scrollbar-width:thin;padding-bottom:2px}
.qc-panel .sf-chips button{flex:0 0 auto;min-height:40px}
.qc-panel .sf-chips .sf-chip-label{flex:0 0 auto;align-self:center;color:#cde;font:var(--text-s) var(--font-ui);padding:0 4px}
.qc-panel .sf-views button{min-height:44px;min-width:120px;font-weight:600}
.qc-panel .sf-readout{color:#ffe2b8;font:600 var(--text-s)/1.4 var(--font-ui);text-align:center;text-shadow:0 1px 2px rgba(0,0,0,.8)}
.qc-panel .sf-picked{color:#fde6b0;font:var(--text-s)/1.4 var(--font-ui);align-self:center}
@media (max-width:600px){#worldstudies-panel.sf-on{width:calc(100vw - 72px);left:calc(50% - 28px)}}`; // phones: clear of the side buttons
  document.head.appendChild(style);
  const row = (cls, html = '') => { const d = document.createElement('div'); d.className = `w4d-row sf-row ${cls}`; d.innerHTML = html; d.hidden = true; panel.appendChild(d); return d; };
  const R = {
    note: row('st-note sf-note'),
    views: row('w4d-options sf-views', '<button type="button" data-sf-view="forms"></button><button type="button" data-sf-view="negative"></button>'),
    readout: row('sf-readout'),
    examples: row('sf-chips sf-examples'),
    forms: row('sf-chips sf-forms'),
    grids: row('w4d-options sf-grids'),
    picked: row('w4d-options sf-picked-row'),
    options: row('w4d-options sf-options', '<button type="button" data-sf="snap"></button><button type="button" data-sf="straighten"></button><button type="button" data-sf="clear"></button>'),
    spacing: row('sf-spacing', '<label class="hull-pick"><span class="sf-spacing-label"></span> <input type="range" class="sf-slider" min="250" max="3000" step="1"> <span class="sf-spacing-val"></span></label>'),
  };
  const spacingInput = R.spacing.querySelector('input');
  const SPACING_SNAPS = [Math.SQRT1_2, 1, Math.SQRT2, (1 + Math.sqrt(5)) / 2, 2];
  const btn = (attr, k, on, label) => `<button type="button" ${attr}="${k}" class="${on ? 'active' : ''}" aria-pressed="${on}">${label}</button>`;
  const isTurned = () => { const q = E.turnOf(arr); return Math.abs(Math.abs(q[3]) - 1) > 1e-9; };
  function renderReadout() {
    const L = lang();
    R.readout.hidden = !active || !viewNegative;
    if (R.readout.hidden) return;
    if (!wasm) { R.readout.textContent = t('sf.loading', L); return; }
    if (!result) { R.readout.textContent = ''; return; }
    const pct = result.hullVolume > 0 ? (100 * result.negativeVolume) / result.hullVolume : 0;
    R.readout.textContent = t('sf.volumes', L, { hull: fmt(result.hullVolume), neg: fmt(result.negativeVolume), pct: pct.toFixed(1) });
  }
  function renderPanel() {
    for (const r of Object.values(R)) r.hidden = !active;
    if (!active) return;
    const L = lang();
    R.note.textContent = t('sf.note', L);
    R.views.querySelectorAll('[data-sf-view]').forEach((b) => { const on = (b.dataset.sfView === 'negative') === viewNegative; b.textContent = t(`sf.view.${b.dataset.sfView}`, L); b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    R.examples.innerHTML = `<span class="sf-chip-label">${t('sf.examples', L)}</span>${E.EXAMPLE_KEYS.map((k) => btn('data-sf-example', k, k === example, t(`sf.ex.${k}`, L))).join('')}`;
    // the form buttons: with a form picked they change its shape, otherwise they choose what a tap on a dot places
    const current = selected !== null ? arr.forms[selected]?.form : pick;
    R.forms.innerHTML = `<span class="sf-chip-label">${t('sf.forms', L)}</span>${E.FORM_KEYS.filter((k) => k !== 'ocdStella' || E.formGeometry(k)).map((k) => btn('data-sf-form', k, k === current, t(`sf.form.${k}`, L))).join('')}`;
    R.forms.hidden = viewNegative; R.grids.hidden = viewNegative;
    R.grids.innerHTML = E.GRIDS.map((g) => btn('data-sf-grid', g, g === arr.grid, t(`sf.grid.${g}`, L))).join('');
    const f = selected !== null ? arr.forms[selected] : null;
    R.picked.hidden = !f;
    if (f) R.picked.innerHTML = `<span class="sf-picked">${t('sf.picked', L, { name: t(`sf.form.${f.form}`, L) })}</span>${btn('data-sf', 'container', !!f.container, t(f.container ? 'sf.container.on' : 'sf.container.off', L))}<button type="button" data-sf="remove">${t('sf.remove', L)}</button><button type="button" data-sf="done">${t('sf.done', L)}</button>`;
    const snapB = R.options.querySelector('[data-sf="snap"]');
    snapB.textContent = t(snap ? 'sf.snap.on' : 'sf.snap.off', L); snapB.classList.toggle('active', snap); snapB.setAttribute('aria-pressed', String(snap));
    const st = R.options.querySelector('[data-sf="straighten"]'); st.textContent = t('sf.straighten', L); st.hidden = !isTurned();
    const cl = R.options.querySelector('[data-sf="clear"]'); cl.textContent = t('sf.clear', L); cl.hidden = !arr.forms.length;
    R.spacing.querySelector('.sf-spacing-label').textContent = t('sf.spacing', L);
    spacingInput.value = String(Math.round(arr.spacing * 1000));
    R.spacing.querySelector('.sf-spacing-val').textContent = arr.spacing.toFixed(3);
    renderReadout();
  }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!active || !b || !b.closest('.sf-row')) return;
    if (b.dataset.sfView) {
      const neg = b.dataset.sfView === 'negative';
      if (neg === viewNegative) return;
      viewNegative = neg; selected = null; save(); draw(); renderPanel(); fit();
      if (neg) { if (wasm) schedule(); else ensureEngine().then(() => { if (active) { schedule(); renderPanel(); } }).catch(() => { R.readout.textContent = t('sf.loadFailed', lang()); }); }
      return;
    }
    if (b.dataset.sfExample) {
      example = b.dataset.sfExample; arr = E.exampleArrangement(example); selected = null;
      commit(true); fit(true); return;
    }
    if (b.dataset.sfForm) {
      if (selected !== null && arr.forms[selected]) { arr.forms[selected].form = b.dataset.sfForm; delete arr.forms[selected].q; delete arr.forms[selected].scale; delete arr.forms[selected].offset; example = null; commit(true); return; }
      pick = b.dataset.sfForm; save(); renderPanel();
      showHudPrompt(t('sf.prompt.place', lang(), { name: t(`sf.form.${pick}`, lang()) }), 2600);
      return;
    }
    if (b.dataset.sfGrid) {
      if (b.dataset.sfGrid === arr.grid) return;
      arr.grid = b.dataset.sfGrid;
      // every form to the nearest point of the new grid (two may meet on one point: they nest)
      for (const f of arr.forms) if (!E.onGrid(arr.grid, f.at)) f.at = E.snapToGrid(arr.grid, 1, f.at);
      example = null; commit(true); fit(); return;
    }
    const k = b.dataset.sf;
    if (k === 'snap') { snap = !snap; if (snap) { arr.turn = E.snapTurn(E.turnOf(arr)); applyTurn(); schedule(); } save(); renderPanel(); }
    else if (k === 'straighten') { arr.turn = [...E.IDENTITY]; commit(true); }
    else if (k === 'clear') { arr = E.normaliseArrangement({ grid: arr.grid, spacing: arr.spacing, forms: [] }); selected = null; example = null; commit(true); }
    else if (k === 'container' && selected !== null) { const f = arr.forms[selected]; if (f.container) delete f.container; else f.container = true; commit(true); }
    else if (k === 'remove' && selected !== null) remove(selected);
    else if (k === 'done') { selected = null; commit(false); }
  });
  spacingInput.addEventListener('input', () => {
    let v = Number(spacingInput.value) / 1000;
    const near = SPACING_SNAPS.find((x) => Math.abs(x - v) < 0.03);
    if (near !== undefined) v = near;
    arr.spacing = v;
    R.spacing.querySelector('.sf-spacing-val').textContent = v.toFixed(3);
    save(); draw(); schedule();
  });
  spacingInput.addEventListener('change', fit);

  return {
    fit: () => fit(true),
    meshes: () => (active ? [...formMeshes, ...(dotHits ? [dotHits] : [])] : []),
    handleTap,
    renderPanel,
    /** Opening the study: load the engine (lazily, once), draw, fit. */
    setActive(on) {
      if (on === active) return;
      active = on; holder.visible = on; panel.classList.toggle('sf-on', on);
      if (!on) { endDrag(false); selected = null; clearHolder(); renderPanel(); return; }
      draw(); renderPanel(); fit(true);
      ensureEngine().then(() => { if (!active) return; draw(); schedule(); renderPanel(); }).catch(() => { R.readout.textContent = t('sf.loadFailed', lang()); });
      showHudPrompt(t('sf.prompt.start', lang()), 4500);
    },
    /** For the browser tests (?probe): the arrangement and what is drawn. */
    probe() {
      // where a scene point is on screen (CSS px), for taps and drags through the real canvas
      const rect = canvas?.getBoundingClientRect();
      const screen = (p) => { const v = new THREE.Vector3(...p).project(camera); return [rect.left + ((v.x + 1) / 2) * rect.width, rect.top + ((1 - v.y) / 2) * rect.height, v.z]; };
      // the example's own check (the negative in a whole inner cell, or all of it) against its exact or published value
      let check = null;
      const ex = example && E.EXAMPLES[example]?.check;
      if (ex && wasm && !dirty) {
        const r = E.shadowForm(arr, wasm);
        check = { got: ex.whole ? r.negativeVolume : E.volumeInBox(wasm, r.negative, ex.min, ex.max), expected: ex.expected };
        r.negative?.delete();
      }
      // each dot's touch target as a screen radius (px)
      const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion).multiplyScalar(E.neighbourDistance(arr.grid, arr.spacing) * 0.3);
      const dotAt = (q) => { const p = q.map((c) => c * arr.spacing), a = screen(p), b2 = screen(new THREE.Vector3(...p).add(right).toArray()); return { at: q, xy: a, r: Math.hypot(b2[0] - a[0], b2[1] - a[1]) }; };
      return { check, dotScreen: rect ? dotIdx.map(dotAt) : [],
        formScreen: rect ? nodes.map((n) => screen(n.position.toArray())) : [], arrangement: JSON.parse(JSON.stringify(arr)), negative: viewNegative, selected, pick, snap, example, engine: !!wasm, dirty,
        forms: nodes.map((n) => ({ position: n.position.toArray(), quaternion: n.quaternion.toArray() })), dots: dotIdx.length,
        cast: cast ? { triangles: cast.geometry.attributes.position.count / 3, visible: cast.visible } : null,
        volumes: result ? { hull: result.hullVolume, forms: result.formsVolume, negative: result.negativeVolume } : null,
        readout: R.readout.hidden ? '' : R.readout.textContent };
    },
  };
}
