// Studies: a 3D+ world of its own (direct decision, 2026-10-08: "study may
// need its own section"), right after the Euclid–Kepler–Pacioli Cell Network
// in the Wizard. Exact constructions on the EKP cell (DISCOVERIES.md #10 and
// its study 10a, #11), one at a time, with a slider where the study has one
// and the Shear either moving exact copies on the lattice or bending the
// solid itself. Geometry in krp-core/src/geometry-extensions/roof-fold.js, checked in
// scripts/verify-roof-fold.mjs.
import * as THREE from 'three';
import {
  ekpWindowsSolid, dogstarSolid, neighbourStellas, stretchedDodeca, expandedWindows, morphedWindowRhombi, rdMorphRhombi,
  RD_MORPH_SQUARE, EXPANDED_WINDOWS_GOLDEN, convexHullFaces, roofFoldSolids, ROOF_FOLD_COLOURS,
  ROOF_FOLD_WORLD_SCALE as WS, PHI,
} from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey, theme } from './site.js';

const STORAGE_KEY = storageKey('studies');
const STUDIES = ['windows', 'windowsStellas', 'checker', 'dogstar', 'expanded', 'icosido', 'rdMorph', 'stretch'];
const C = ROOF_FOLD_COLOURS;
const GHOST_COLOR = () => theme().accentHex; // read when drawing: follows the app whose space you're in
const EDGE_COLOR = 0x0b1220;
// Each slider study: its value in view, range, snaps and label.
const SLIDERS = {
  stretch: { key: 'stretch', max: 2.6, snaps: [2 / PHI, 2], label: 'studies.slider.stretch' }, // one edge (squares), the lattice spacing
  expanded: { key: 'push', max: 1.6, snaps: [EXPANDED_WINDOWS_GOLDEN], label: 'studies.push' }, // the golden rhombi
  icosido: { key: 'morph', max: 1, snaps: [0, 1], label: 'studies.morph' },
  rdMorph: { key: 'rdMorph', max: 1, snaps: [0, RD_MORPH_SQUARE, 1], label: 'studies.morph' }, // squares on the way
  checker: { key: 'apart', max: 1, snaps: [0], label: 'studies.apart' }, // packed tight
  dogstar: { key: 'apart', max: 1, snaps: [0], label: 'studies.apart' },
};
const lang = () => getSettings().language;
const sideOf = (f) => Math.hypot(...f[0].map((c, k) => c - f[1][k]));

export function createStudiesWorld({ scene, fitView = () => {}, shear = () => null }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const DODECA = roofFoldSolids().dodeca;

  const view = { study: 'windows', stretch: SLIDERS.stretch.snaps[0], push: EXPANDED_WINDOWS_GOLDEN, morph: 1, rdMorph: 1, apart: 0.35, studyShear: 'copies' };
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (STUDIES.includes(data?.study)) view.study = data.study;
    if (['copies', 'solid'].includes(data?.studyShear)) view.studyShear = data.studyShear;
    for (const { key, max } of Object.values(SLIDERS)) if (Number.isFinite(data?.[key])) view[key] = Math.max(0, Math.min(max, data[key]));
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false;

  // ---- drawing ----
  const solidMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  // Rhombi inlaid on a hull face they lie in: drawn over it, never fighting it.
  const inlayMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -4 });
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
    }
  }
  // Polygons (cell units, each with a world offset) as one mesh, plus their edges.
  function meshOf(polys, material, edgeColor = EDGE_COLOR) {
    const pos = [], col = [], line = [];
    for (const { polygon, offset, colour } of polys) {
      const P = polygon.map((p) => p.map((c, a) => c * WS + offset[a]));
      for (let i = 1; i + 1 < P.length; i++) for (const p of [P[0], P[i], P[i + 1]]) { pos.push(...p); col.push(colour.r, colour.g, colour.b); }
      P.forEach((p, i) => line.push(...p, ...P[(i + 1) % P.length]));
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    return [new THREE.Mesh(g, material), new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: edgeColor }))];
  }
  // The Shear: as copies on a 2 x 2 x 2 block of cells, each at its sheared cell
  // centre and left exact, or as one solid put through the shear itself.
  const BLOCK = [0, 1].flatMap((x) => [0, 1].flatMap((y) => [0, 1].map((z) => [x, y, z])));
  const copies = () => view.studyShear === 'copies';
  const shearMap = (p) => { const A = shear(); return A ? A.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]) : p; };
  function placements() {
    if (!copies()) return [{ offset: [0, 0, 0], map: shearMap }];
    const centres = BLOCK.map((s) => shearMap(s.map((c) => 2 * c)).map((c) => c * WS));
    const mid = [0, 1, 2].map((a) => centres.reduce((t0, c) => t0 + c[a], 0) / centres.length);
    return centres.map((c) => ({ offset: c.map((v, a) => v - mid[a]), map: (p) => p }));
  }
  // Windows and stellas in a checkerboard (direct question, 2026-10-08: "a male counterpart
  // to window"): the stella octangula is it. Even cells hold the windows, odd cells a stella;
  // each odd cube is its stella plus its six neighbours' carved roofs, exactly (12 + 4 = two
  // cubes). Pulled `apart` to see them mate; the Shear moves the cell centres (copies) or
  // bends the whole packing (solid).
  const STELLA = roofFoldSolids().stella.faces;
  // Dodecahedra and Dogstars (DICTO, 2026-10-08: "reverse engineer from gap"): the same
  // checkerboard, with regular dodecahedra on the even cells and the holes they leave on the odd.
  const DOGSTAR = dogstarSolid();
  function checkerPlacements() {
    const k = 1 + view.apart;
    const cells = BLOCK.map((s) => ({ s, c: s.map((x) => 2 * x * k) }));
    const mid = [0, 1, 2].map((a) => cells.reduce((t0, { c }) => t0 + shearMap(c)[a], 0) / cells.length * WS);
    return cells.map(({ s, c }) => {
      const even = (s[0] + s[1] + s[2]) % 2 === 0;
      if (copies()) return { even, offset: shearMap(c).map((v, a) => v * WS - mid[a]), map: (p) => p };
      return { even, offset: mid.map((m) => -m), map: (p) => shearMap(p.map((x, a) => x + c[a])) };
    });
  }
  function checkerFaces(even) {
    if (view.study === 'dogstar') return even ? DODECA.faces.map((f) => [f, C.dodeca]) : DOGSTAR.map((f) => [f, C.star]);
    if (!even) return STELLA.map((f) => [f, C.stella]);
    const { rhombi, walls } = ekpWindowsSolid();
    return [...rhombi.map((f) => [f, C.dodeca]), ...walls.map((f) => [f, C.stella])];
  }
  // The faces a study shows, [polygon, colour] in cell units.
  function studyFaces() {
    const out = [];
    const put = (f, hex) => out.push([f, hex]);
    if (view.study === 'stretch') {
      for (const f of stretchedDodeca(view.stretch)) put(f, f.length === 5 ? C.dodeca : f.length === 6 ? C.star : C.cube);
    } else if (view.study === 'expanded') {
      // Thick rhombi gold, golden rhombi coral, cube-corner triangles grey, joining triangles purple.
      const equal = (f) => f.every((p, i) => Math.abs(Math.hypot(...p.map((c, k) => c - f[(i + 1) % f.length][k])) - sideOf(f)) < 1e-6);
      for (const f of expandedWindows(view.push)) put(f, f.length === 4 ? (Math.abs(sideOf(f) - 2 / PHI) < 1e-6 ? C.dodeca : C.star) : equal(f) ? C.cube : C.stella);
    } else if (view.study === 'icosido' || view.study === 'rdMorph') {
      // An opaque hull, the rhombi inlaid on it (direct request: floating rhombi "remind me of
      // post-it notes"). Hull colours: pentagons coral, triangles purple, the RD's rhombi gold.
      const rhombi = view.study === 'icosido' ? morphedWindowRhombi(view.morph) : rdMorphRhombi(view.rdMorph);
      for (const f of convexHullFaces(rhombi.flat())) put(f, f.length === 5 ? C.star : f.length === 3 ? C.stella : C.dodeca);
    } else {
      const { rhombi, walls } = ekpWindowsSolid();
      rhombi.forEach((f) => put(f, C.dodeca));
      walls.forEach((f) => put(f, C.stella));
    }
    return out;
  }
  function draw() {
    clearGroup();
    if (!active) return;
    const where = placements();
    const polys = [];
    if (view.study === 'checker' || view.study === 'dogstar') {
      for (const { even, offset, map } of checkerPlacements()) for (const [f, hex] of checkerFaces(even)) polys.push({ polygon: f.map(map), offset, colour: new THREE.Color(hex) });
    } else for (const { offset, map } of where) for (const [f, hex] of studyFaces()) polys.push({ polygon: f.map(map), offset, colour: new THREE.Color(hex) });
    group.add(...meshOf(polys, solidMaterial));
    if (view.study === 'icosido' || view.study === 'rdMorph') {
      // The rhombi: inlaid where they lie on the hull; mid-morph they're inside it, so their
      // outlines also show faintly through it, to follow them.
      const rhombi = view.study === 'icosido' ? morphedWindowRhombi(view.morph) : rdMorphRhombi(view.rdMorph);
      const inlays = [];
      for (const { offset, map } of where) for (const f of rhombi) inlays.push({ polygon: f.map(map), offset, colour: new THREE.Color(C.dodeca) });
      const [mesh, lines] = meshOf(inlays, inlayMaterial, C.dodeca);
      lines.material.depthTest = false;
      lines.material.transparent = true;
      lines.material.opacity = 0.55;
      lines.renderOrder = 2;
      group.add(mesh, lines);
    }
    // Context, faint: the six stellas round the windows, or the two dodecahedra the stretch joins.
    const context = [];
    if (view.study === 'windowsStellas') for (const tet of neighbourStellas()) for (const f of tet) f.forEach((p, i) => context.push([p, f[(i + 1) % f.length]]));
    if (view.study === 'stretch') for (const dx of [-view.stretch / 2, view.stretch / 2]) for (const [a, b] of DODECA.edges) context.push([[a[0] + dx, a[1], a[2]], [b[0] + dx, b[1], b[2]]]);
    if (context.length) {
      const ghost = [];
      for (const { offset, map } of where) for (const [a, b] of context) ghost.push(...map(a).map((c, i) => c * WS + offset[i]), ...map(b).map((c, i) => c * WS + offset[i]));
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(ghost, 3));
      group.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: view.study === 'stretch' ? GHOST_COLOR() : C.stella, transparent: true, opacity: 0.55 })));
    }
    renderPanel();
  }
  function fit() {
    if (view.study === 'checker' || view.study === 'dogstar') { fitView([0, 0, 0], (Math.sqrt(3) * (1 + view.apart) + 1.8) * WS * 1.15); return; }
    const r = view.study === 'windowsStellas' ? 3.4 : view.study === 'stretch' ? view.stretch / 2 + 1.8 : view.study === 'expanded' ? 1.9 + view.push : view.study === 'icosido' || view.study === 'rdMorph' ? 2.1 : 1.8;
    const spread = copies() ? Math.max(...placements().map(({ offset }) => Math.hypot(...offset))) : 0;
    fitView([0, 0, 0], r * WS + spread);
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldstudies-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="st-study-label"></span> <select class="hull-select" data-select="study"></select></label></div>
    <div class="w4d-row st-slider-row"><label class="hull-pick"><span class="st-slider-label"></span> <input type="range" class="st-slider" min="0" step="1"> <span class="st-slider-val"></span></label></div>
    <div class="w4d-row st-note"></div>
    <div class="w4d-row w4d-options"><button type="button" data-study-shear></button></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'studies');
  const studySelect = panel.querySelector('[data-select="study"]');
  const sliderRow = panel.querySelector('.st-slider-row');
  const sliderInput = panel.querySelector('.st-slider');
  const sliderVal = panel.querySelector('.st-slider-val');
  const note = panel.querySelector('.st-note');
  const shearBtn = panel.querySelector('[data-study-shear]');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.st-study-label').textContent = t('studies.study', L);
    studySelect.innerHTML = STUDIES.map((k) => `<option value="${k}"${k === view.study ? ' selected' : ''}>${t(`studies.${k}`, L)}</option>`).join('');
    const slider = SLIDERS[view.study];
    sliderRow.style.display = slider ? '' : 'none';
    if (slider) {
      panel.querySelector('.st-slider-label').textContent = t(slider.label, L);
      sliderInput.max = String(slider.max * 1000);
      sliderInput.value = String(Math.round(view[slider.key] * 1000));
      sliderVal.textContent = view[slider.key].toFixed(3);
    }
    note.textContent = t(`studies.note.${view.study}`, L);
    shearBtn.textContent = t(`studies.shear.${view.studyShear}`, L);
  }
  studySelect.addEventListener('change', () => {
    if (!STUDIES.includes(studySelect.value)) return;
    view.study = studySelect.value;
    save();
    draw();
    fit();
  });
  sliderInput.addEventListener('input', () => {
    const slider = SLIDERS[view.study];
    if (!slider) return;
    let v = Number(sliderInput.value) / 1000;
    const snap = slider.snaps.find((x) => Math.abs(x - v) < 0.03);
    if (snap !== undefined) v = snap;
    view[slider.key] = v;
    save();
    draw();
  });
  sliderInput.addEventListener('change', fit);
  shearBtn.addEventListener('click', () => {
    view.studyShear = copies() ? 'solid' : 'copies';
    save();
    draw();
    fit();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) panel.classList.remove('visible');
      draw();
      if (on) fit();
    },
    setSkeleton() {},
    setTranslucent() {},
    setLatticeView() {},
    shearChanged() { if (active) draw(); },
    get isEmpty() { return true; },
    clear() {},
  };
}
