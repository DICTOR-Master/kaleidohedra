// Targets: a 3D gallery of the 160 target cells (TARGETS.md, geometry in
// geometry-extensions/targets.js). Pick a type and a cell; it is drawn at
// edge 1 with its faces coloured by kind, alone, with its face neighbours, or
// as a 3x3x3 block of its lattice. Info gives its faces, angles, volume and
// whether it is already a Polyhedraverse piece. Nothing is built here: a
// viewer. Lives outside the shear group (shearing would change the angles).
import * as THREE from 'three';
import { TARGET_TYPES, buildTarget, loadTargets, targetAngles } from '../geometry-extensions/targets.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';

const STORAGE_KEY = 'kaleidohedra-targets-world';
const SHOWS = ['cell', 'neighbours', 'block'];
// One colour per face kind, as Polyhedraverse's Kaleidohedra-verified pieces.
const KIND_COLOR = { square: 0x5b8def, rhombus: 0xf06292, 'regular hexagon': 0xffc857, hexagon: 0xa77bf3 };
const EDGE_COLOR = 0x0b1220;
const GHOST_COLOR = 0x9de0ff;
const NEIGHBOUR_SHADE = 0.72;
const lang = () => getSettings().language;
const kindBase = (kind) => (kind.startsWith('rhombus') ? 'rhombus' : kind.startsWith('hexagon') ? 'hexagon' : kind);
const typeKey = (type) => type.replace(/ /g, '-');

export function createTargetsWorld({ scene, fitView = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  let targets = [];
  const cells = new Map(); // index -> built cell (lazy)
  const view = { type: 'all', index: 0, show: 'cell' };
  let active = false;
  let skeleton = false;
  let opacity = 1;
  let infoOpen = false;
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (data) {
      if (data.type === 'all' || TARGET_TYPES.includes(data.type)) view.type = data.type;
      if (Number.isInteger(data.index) && data.index >= 0) view.index = data.index;
      if (SHOWS.includes(data.show)) view.show = data.show;
    }
  } catch { /* blocked storage: defaults */ }
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ }
  }
  loadTargets().then((list) => {
    targets = list;
    if (view.index >= targets.length) view.index = 0;
    if (active) { rebuild(); fit(); }
  });
  const cellOf = (i) => { if (!cells.has(i)) cells.set(i, buildTarget(targets[i])); return cells.get(i); };
  const shown = () => targets.map((tg, i) => i).filter((i) => view.type === 'all' || targets[i].type === view.type);
  const typeName = (type, L) => t(`targets.type.${typeKey(type)}`, L);
  const nameOf = (i, L) => `${typeName(targets[i].type, L)} #${targets[i].number} · ${targetAngles(targets[i])}`;
  const kindName = (kind, L) => {
    const base = kindBase(kind);
    const rest = kind.slice(base.length).trim();
    return rest ? `${t(`targets.face.${base}`, L)} ${rest}${base === 'rhombus' ? '°' : ''}` : t(`targets.face.${base.replace(' ', '-')}`, L);
  };

  // ---- drawing ----
  const material = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
    }
  }
  // Lattice offsets drawn around the cell: itself, its face neighbours, or the 3x3x3 block of its basis.
  function offsets(cell) {
    if (view.show === 'cell' || !cell.basis) return [[0, 0, 0]];
    if (view.show === 'neighbours') return [[0, 0, 0], ...cell.faces.map((f) => f.centre.map((c) => 2 * c))];
    const out = [];
    for (const i of [-1, 0, 1]) for (const j of [-1, 0, 1]) for (const k of [-1, 0, 1]) out.push([0, 1, 2].map((a) => i * cell.basis[0][a] + j * cell.basis[1][a] + k * cell.basis[2][a]));
    return out;
  }
  function rebuild() {
    renderPanel();
    renderInfo();
    clearGroup();
    if (!active || !targets.length) return;
    const cell = cellOf(view.index);
    material.transparent = opacity < 1;
    material.opacity = opacity;
    material.depthWrite = opacity >= 1;
    const pos = [], col = [], line = [];
    for (const off of offsets(cell)) {
      const centre = !off.some((c) => Math.abs(c) > 1e-9);
      for (const { polygon, kind } of cell.faces) {
        const c = new THREE.Color(KIND_COLOR[kindBase(kind)]);
        if (!centre) c.multiplyScalar(NEIGHBOUR_SHADE);
        const P = polygon.map((p) => p.map((v, a) => v + off[a]));
        for (let i = 1; i + 1 < P.length; i++) for (const p of [P[0], P[i], P[i + 1]]) { pos.push(...p); col.push(c.r, c.g, c.b); }
        P.forEach((p, i) => line.push(...p, ...P[(i + 1) % P.length]));
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const mesh = new THREE.Mesh(g, material);
    mesh.visible = !skeleton;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    const lines = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? GHOST_COLOR : EDGE_COLOR }));
    group.add(mesh, lines);
  }
  function fit() {
    if (!targets.length) return;
    const cell = cellOf(view.index);
    const pts = offsets(cell).flatMap((off) => cell.faces.flatMap((f) => f.polygon.map((p) => p.map((v, a) => v + off[a]))));
    fitView([0, 0, 0], Math.max(...pts.map((p) => Math.hypot(...p))) * 1.05);
  }

  // ---- info ----
  const info = document.createElement('div');
  info.id = 'worldtargets-info';
  info.className = 'qc-info';
  info.setAttribute('aria-live', 'polite');
  document.body.appendChild(info);
  function renderInfo() {
    const show = active && infoOpen && targets.length > 0;
    info.classList.toggle('visible', show);
    if (!show) return;
    const L = lang();
    const tg = targets[view.index];
    const row = (k, v) => `<div><span class="w4d-info-k">${k}</span> ${v}</div>`;
    const faces = Object.entries(tg.faces).sort((a, b) => b[1] - a[1]).map(([k, n]) => `${n} ${kindName(k, L)}`).join(', ');
    info.innerHTML = [
      `<div><strong>${nameOf(view.index, L)}</strong></div>`,
      row(t('targets.info.faces', L), faces),
      row(t('targets.info.angles', L), `${tg.line_angles.map((a) => `${Math.round(a * 100) / 100}°`).join(', ')}`),
      row(t('targets.info.volume', L), tg.volume),
      row(t('targets.info.tiles', L), t(`targets.lattice.${typeKey(tg.type)}`, L)),
      row(t('targets.info.status', L), tg.in_polyhedraverse.length ? t('targets.status.built', L, { id: tg.in_polyhedraverse[0] }) : t('targets.status.toFind', L)),
    ].join('');
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldtargets-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="tg-type-label"></span> <select class="hull-select" data-select="type"></select></label></div>
    <div class="w4d-row"><button type="button" data-step="-1" aria-label="◀">◀</button> <select class="hull-select" data-select="cell"></select> <button type="button" data-step="1" aria-label="▶">▶</button></div>
    <div class="w4d-row"><label class="hull-pick"><span class="tg-show-label"></span> <select class="hull-select" data-select="show"></select></label></div>
    <div class="w4d-row w4d-options"></div>`;
  document.body.appendChild(panel);
  const typeSelect = panel.querySelector('[data-select="type"]');
  const cellSelect = panel.querySelector('[data-select="cell"]');
  const showSelect = panel.querySelector('[data-select="show"]');
  const optionsRow = panel.querySelector('.w4d-options');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.tg-type-label').textContent = t('targets.type', L);
    panel.querySelector('.tg-show-label').textContent = t('targets.show', L);
    const count = (type) => targets.filter((tg) => type === 'all' || tg.type === type).length;
    typeSelect.innerHTML = ['all', ...TARGET_TYPES].map((type) => `<option value="${type}"${type === view.type ? ' selected' : ''}>${type === 'all' ? t('targets.all', L) : typeName(type, L)} (${count(type)})</option>`).join('');
    cellSelect.innerHTML = shown().map((i) => `<option value="${i}"${i === view.index ? ' selected' : ''}>${nameOf(i, L)}${targets[i].in_polyhedraverse.length ? ' ✓' : ''}</option>`).join('');
    showSelect.innerHTML = SHOWS.map((s) => `<option value="${s}"${s === view.show ? ' selected' : ''}>${t(`targets.show.${s}`, L)}</option>`).join('');
    optionsRow.innerHTML = `<button type="button" data-opt="info" class="${infoOpen ? 'active' : ''}">${t('hyper.info', L)}</button>`;
  }
  function select(i) {
    view.index = i;
    save();
    rebuild();
    fit();
  }
  typeSelect.addEventListener('change', () => {
    const type = typeSelect.value;
    if (type !== 'all' && !TARGET_TYPES.includes(type)) return;
    view.type = type;
    const list = shown();
    select(list.includes(view.index) ? view.index : list[0] ?? 0);
  });
  cellSelect.addEventListener('change', () => { const i = Number(cellSelect.value); if (targets[i]) select(i); });
  panel.addEventListener('click', (ev) => {
    const step = ev.target.closest('button[data-step]');
    if (step) {
      const list = shown();
      if (!list.length) return;
      const at = Math.max(0, list.indexOf(view.index));
      select(list[(at + Number(step.dataset.step) + list.length) % list.length]);
      return;
    }
    if (ev.target.closest('button[data-opt="info"]')) { infoOpen = !infoOpen; rebuild(); }
  });
  showSelect.addEventListener('change', () => {
    if (!SHOWS.includes(showSelect.value)) return;
    view.show = showSelect.value;
    save();
    rebuild();
    fit();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) rebuild(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); info.classList.remove('visible'); }
      rebuild();
      if (on) fit();
    },
    setSkeleton(on) { skeleton = on; if (active) rebuild(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) rebuild(); } },
    setLatticeView() {},
    get isEmpty() { return true; },
    clear() {},
  };
}
