// The Mandala World (DICTO 2026-11-08; placeholder name): the DICTO Yantra in three dimensions and on the sphere. DICTO proposed the
// triangles as tetrahedra, spinning them, the Cleo-Icos sphere and the 81 sphere; the geometry is the DICTO Yantra study's
// (k-research studies/2026-11-08-sri-yantra, 2026-11-08-tetra-yantra), ported in mandala-geometry.js from the exact data
// (mandala-data.js, generated from golden_family.json GF1).
// Three views, one button group:
// - Yantra: the nine triangles as tetrahedra (up gold, down blue) turning about the vertical axis on one big slider, inside the nine
//   nested cones they sweep (see-through glass) with the nine red marma circles where two cones and a disc meet. The slider has three
//   still stops, one in each mirror plane: there the view turns level and the yantra is seen narrowed to cos 30° in the plane through
//   the axis, all 18 meetings kept (red), the tetrahedra as glass behind it. No step buttons (DICTO).
// - Cleo sphere: twenty DICTO Yantras by gnomonic projection in the inscribed circles of the twenty faces of the Cleo-Icos (the
//   spherical icosahedron); every line a great circle. Turned by touch like any view.
// - 81 sphere: eighty on the twice-split Cleo sphere and the bindu at the centre (81, the number of Shingon's Kongōkai mandala).
// The spheres are a see-through crystal shell (the far side dimmed through it), the bindu solid inside. Slider only where it applies.
// Pure geometry: the slider moves the spin, nothing runs by itself.
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { N_TRI, isUp, GREAT, tetra, cone, marmaCircles, narrowed, STILL_STOPS, SPIN_MIN, SPIN_MAX, stopAt, SPIN_START as START, cleoSphere, sphere81, sphereYantra, capRim, arc, studyTilt } from './mandala-geometry.js';

// Colours as in the study renders: tetrahedra up gold, down blue, marma circles red
const GOLD = 0xe8c25a, BLUE = 0x3a70cd, RED = 0xcd3e28, RIM = 0xaaaab4, GRID = 0x5f5f69, SHELL = 0x16202e;
const MODES = ['yantra', 'cleo', 'sphere81'];
const SNAP = 4;                                    // degrees: the slider snaps to a still position this close
const ELEV = (18 * Math.PI) / 180;                 // the study's 3D view: 18° above level
const VIEW_3D = [0, Math.sin(ELEV), Math.cos(ELEV)], VIEW_LEVEL = [0, 0, 1];
const colourOf = (i) => (isUp(i) ? GOLD : BLUE);
const lang = () => getSettings().language;

export function createMandalaWorld({ scene, fitView = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // it always opens on the Yantra at its opening spin (DICTO: "opens on the DICTO Yantra in 3D"), unless a link names a view
  const view = { mode: 'yantra', spin: START };
  let active = false, skeleton = false, opacity = 1, named = false;
  const lineMats = [];
  let counts = {};

  function clear() {
    for (const c of [...group.children]) { group.remove(c); c.traverse((o) => o.geometry?.dispose()); }
    lineMats.splice(0).forEach((m) => m.dispose());
    group.quaternion.identity();
  }
  function lines(segs, color, width, order = 0, o = 1, parent = group) {
    if (!segs.length) return;
    const g = new LineSegmentsGeometry();
    g.setPositions(segs.flatMap(([a, b]) => [...a, ...b]));
    // in the transparent pass, by render order: edges over the glass they belong to, the far side of a sphere under its shell
    const m = new LineMaterial({ color, linewidth: width, transparent: true, opacity: o, depthWrite: o >= 1 });
    lineMats.push(m);
    const l = new LineSegments2(g, m);
    l.frustumCulled = false;
    l.renderOrder = order;
    parent.add(l);
  }
  const polySegs = (pts) => pts.slice(1).map((p, k) => [pts[k], p]);
  const glass = (color, o) => { const m = new THREE.MeshStandardMaterial({ color, side: THREE.DoubleSide, transparent: true, opacity: o, depthWrite: false, roughness: 0.4 }); m.userData.hollow = true; return m; };
  function mesh(geometry, material, order = 0, parent = group) {
    const m = new THREE.Mesh(geometry, material);
    m.renderOrder = order;
    parent.add(m);
    return m;
  }
  const ring = (r, y, n = 96) => Array.from({ length: n + 1 }, (_, s) => { const a = (2 * Math.PI * s) / n; return [r * Math.cos(a), y, r * Math.sin(a)]; });

  // ---- Yantra: the tetrahedra, the cones, the marma circles; at a still position the narrowed yantra ----
  function drawYantra() {
    const k = stopAt(view.spin), still = k >= 0;
    // the sphere of the yantra's circle, a faint crystal shell
    if (!skeleton) mesh(new THREE.SphereGeometry(1, 48, 32), glass(0xcfe0ff, 0.05 * opacity), 1);
    // the nine cones the spinning tetrahedra sweep, as glass, each with its base disc
    for (let i = 0; i < N_TRI; i++) {
      const c = cone(i);
      if (!skeleton) {
        const g = new THREE.ConeGeometry(c.r, Math.abs(c.apex - c.base), 64, 1, true);
        if (c.apex < c.base) g.rotateX(Math.PI);             // ConeGeometry points up (apex above the base); apex below: turned over
        g.translate(0, (c.apex + c.base) / 2, 0);
        mesh(g, glass(colourOf(i), 0.07 * opacity), 2);
        const disc = new THREE.CircleGeometry(c.r, 64).rotateX(-Math.PI / 2).translate(0, c.base, 0);
        mesh(disc, glass(colourOf(i), 0.05 * opacity), 2);
      }
      lines(polySegs(ring(c.r, c.base)), colourOf(i), 1.2, 3, 0.55);
    }
    // the marma circles: two cones and a disc meet
    const circles = marmaCircles();
    for (const { r, y } of circles) lines(polySegs(ring(r, y)), RED, 3, 5);
    // the tetrahedra: faces lightly filled in their colour, edges bright (the great pair, 3 and 7, thicker); glass at a still position
    for (let i = 0; i < N_TRI; i++) {
      const { base, apex } = tetra(i, view.spin), col = colourOf(i);
      if (!skeleton) {
        const pos = new Float32Array([...base[0], ...base[1], ...base[2], ...base[0], ...base[1], ...apex, ...base[1], ...base[2], ...apex, ...base[2], ...base[0], ...apex]);
        const g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        g.computeVertexNormals();
        mesh(g, glass(col, (still ? 0.08 : 0.22) * opacity), 4);
      }
      const segs = [[base[0], base[1]], [base[1], base[2]], [base[2], base[0]], ...base.map((p) => [p, apex])];
      lines(segs, col, still ? 1.2 : GREAT.has(i) ? 3.2 : 2.2, 6, still ? 0.45 : 1);
    }
    let meetings = 0;
    if (still) {
      // seen level along the mirror plane: the yantra narrowed to cos 30°, drawn in the plane through the axis facing you
      const { segs, meet } = narrowed();
      for (const col of [GOLD, BLUE]) lines(segs.filter(([, , i]) => colourOf(i) === col).map(([p, q]) => [p, q]), col, 2.4, 7);
      const dot = new THREE.SphereGeometry(0.028, 16, 12), red = new THREE.MeshBasicMaterial({ color: RED, transparent: true });
      for (const p of meet) mesh(dot, red, 8).position.set(...p);
      meetings = meet.length;
    }
    counts = { tetrahedra: N_TRI, cones: N_TRI, marmaCircles: circles.length, still: still ? k + 1 : 0, meetings };
  }

  // ---- the spheres: yantras on the crystal shell, the far side dimmed through it ----
  function shell(parent) {
    if (skeleton) return;
    const m = new THREE.MeshStandardMaterial({ color: SHELL, transparent: true, opacity: 0.8 * opacity, depthWrite: false, roughness: 0.35, metalness: 0.1 });
    m.userData.hollow = true;
    mesh(new THREE.SphereGeometry(0.985, 64, 48), m, 10, parent);
  }
  function yantraLines(list, parent, width) {
    const gold = [], blue = [];
    for (const [pts, i] of list) (isUp(i) ? gold : blue).push(...polySegs(pts));
    lines(gold, GOLD, width, 2, 1, parent);
    lines(blue, BLUE, width, 2, 1, parent);
  }
  function drawCleo(spin) {
    const { caps, rho } = cleoSphere();
    yantraLines(caps.flatMap(({ cen, point }) => sphereYantra(cen, point, rho, 20)), spin, 1.5);
    lines(caps.flatMap(({ cen, point }) => polySegs(capRim(cen, point, rho))), RIM, 1.2, 2, 1, spin);
    shell(spin);
    counts = { yantras: caps.length, capDegrees: (rho * 180) / Math.PI };
  }
  function drawSphere81(spin) {
    const s = sphere81();
    yantraLines(s.tris.flatMap((tr) => sphereYantra(tr.cen, tr.point, tr.rho, 10)), spin, 1.2);
    lines(s.tris.flatMap((tr) => [[0, 1], [1, 2], [2, 0]].flatMap(([i, j]) => polySegs(arc(tr.v[i], tr.v[j])))), GRID, 1, 1, 1, spin);
    shell(spin);
    // the bindu: one point at the centre, solid inside the shell
    mesh(new THREE.SphereGeometry(0.045, 24, 16), new THREE.MeshBasicMaterial({ color: RED, transparent: true }), 11, spin);
    counts = { yantras: s.tris.length, bindu: 1, total: s.tris.length + 1, corners: s.corners, edges: s.edges };
  }

  function draw() {
    clear();
    if (!active) return;
    if (view.mode === 'yantra') drawYantra();
    else {
      // the spheres are shown as in the study renders: tilted by Rx(0.35)·Ry(0.3), seen from the front
      const T = studyTilt(), m = new THREE.Matrix4().set(...T[0], 0, ...T[1], 0, ...T[2], 0, 0, 0, 0, 1);
      const spin = new THREE.Group();
      spin.quaternion.setFromRotationMatrix(m);
      group.add(spin);
      if (view.mode === 'cleo') drawCleo(spin); else drawSphere81(spin);
    }
    renderPanel();
  }
  const fit = (dir) => fitView([0, 0, 0], 1.02, dir, true);
  const viewDir = () => (view.mode !== 'yantra' ? VIEW_LEVEL : stopAt(view.spin) >= 0 ? VIEW_LEVEL : VIEW_3D);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldmandala-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row w4d-options md-modes">${MODES.map((m) => `<button type="button" data-md-mode="${m}"></button>`).join('')}</div>
    <div class="w4d-row ch-param-row md-spin-row"><label class="hull-pick"><span class="md-spin-label"></span> <input type="range" class="st-slider" data-md-spin min="${SPIN_MIN}" max="${SPIN_MAX}" step="0.5" value="${START}"></label></div>
    <div class="w4d-row ch-param-caption md-caption" aria-live="polite"></div>
    <div class="w4d-row st-note md-note fold"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'mandala');
  const slider = panel.querySelector('[data-md-spin]');
  panel.querySelector('.md-note').addEventListener('click', (e) => e.currentTarget.classList.toggle('open'));
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelectorAll('[data-md-mode]').forEach((b) => { const on = b.dataset.mdMode === view.mode; b.textContent = t(`mandala.mode.${b.dataset.mdMode}`, L); b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    // the spin slider only in the Yantra view (the spheres turn by touch)
    panel.querySelector('.md-spin-row').hidden = view.mode !== 'yantra';
    panel.querySelector('.md-spin-label').textContent = t('mandala.spin', L);
    slider.value = String(view.spin);
    panel.querySelector('.md-caption').textContent = caption(L);
    panel.querySelector('.md-note').textContent = `${t(`mandala.note.${view.mode}`, L)} ${t('mandala.credit', L)}`;
  }
  function caption(L) {
    if (view.mode === 'cleo') return t('mandala.caption.cleo', L);
    if (view.mode === 'sphere81') return t('mandala.caption.sphere81', L);
    const k = stopAt(view.spin);
    return k >= 0 ? t('mandala.caption.still', L, { n: k + 1 }) : t('mandala.caption.turn', L, { deg: Math.round(view.spin) });
  }
  panel.querySelector('.md-modes').addEventListener('click', (e) => {
    const m = e.target.closest('[data-md-mode]')?.dataset.mdMode;
    if (!m || m === view.mode) return;
    view.mode = m; draw(); fit(viewDir());
  });
  // the one big slider: it snaps to a still position within SNAP degrees (no step buttons, DICTO); let go at a still position the
  // view turns level to see the narrowed yantra, let go between them it goes back to the 3D view
  slider.addEventListener('input', () => {
    let v = Number(slider.value);
    const s = STILL_STOPS.find((x) => Math.abs(x - v) <= SNAP);
    if (s !== undefined) { v = s; slider.value = String(v); }
    if (v === view.spin) return;
    view.spin = v; draw();
  });
  slider.addEventListener('change', () => fit(viewDir()));
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** ?open=mandala:<yantra|cleo|81> and tool:mandalaWorld:<the same>: that view (the Yantra from its opening spin). */
    setChain(arg) {
      const k = String(arg).toLowerCase(), m = k === '81' || k === 'sphere81' ? 'sphere81' : MODES.includes(k) ? k : 'yantra';
      Object.assign(view, { mode: m, spin: START });
      named = !active;   // read when the world opens next; already open, it is shown at once
      if (active) { draw(); fit(viewDir()); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); clear(); return; }
      if (!named) Object.assign(view, { mode: 'yantra', spin: START });
      named = false;
      draw();
      fit(viewDir());
    },
    resetView() { Object.assign(view, { mode: 'yantra', spin: START }); if (active) { draw(); fit(viewDir()); } },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): the view, the spin and what is drawn. */
    probe() {
      const all = []; group.traverse((o) => { if (o !== group) all.push(o); });
      return { mode: view.mode, spin: view.spin, stops: STILL_STOPS, ...counts,
        glass: all.filter((c) => c.isMesh && c.material.transparent && c.material.userData.hollow).length,
        lineWidths: lineMats.map((m) => m.linewidth), sliderShown: !panel.querySelector('.md-spin-row').hidden };
    },
  };
}
