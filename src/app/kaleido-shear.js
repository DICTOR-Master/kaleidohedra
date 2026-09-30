// Kaleidoverse by DICTO: the lattice shear (direct decisions 2026-10-01).
//
// Every piece of geometry lives in one group whose transform is a linear
// map A. A comes from six lattice parameters -- the lengths a, b, c
// (relative to FCC) and the angles alpha, beta, gamma between FCC's three
// primitive cell vectors (60 degrees each for plain FCC). Building works
// exactly as in Rhombiverse: taps are resolved in each piece's own frame,
// and raycasting follows the group's transform.
//
// One "path" slider moves all six along a straight line from FCC (0)
// through a halfway stop (1) to DICTO FCC (2) and beyond, stopping before
// the cells would collapse. The six sliders give full control. Export
// saves the current state as a named "population member".
import * as THREE from 'three';

import { KEYS, FCC_PARAMS, PATH_STOPS, PATH_RANGE, paramsOnPath, paramsValid, shearMatrix, cellDirections, cellDirectionsPreShear, cellQuality, pathTargets } from '../geometry-extensions/kaleido-lattice.js';

const STORAGE_KEY = 'kaleidoverse-shear';

/**
 * Installs the shear: routes everything added to the scene (except the
 * camera) into one group, and builds the slider panel.
 */
export function installShear({ scene, camera, onChange = () => {}, onCell = () => {} }) {
  const group = new THREE.Group();
  group.name = 'kaleidoverse-shear';
  group.matrixAutoUpdate = false;
  const add = scene.add.bind(scene);
  const remove = scene.remove.bind(scene);
  add(group);
  // Everything already in the scene, and everything added later, goes in the group.
  for (const child of [...scene.children]) if (child !== group && child !== camera) group.add(child);
  scene.add = (...objs) => { for (const o of objs) (o === camera || o === group ? add : group.add.bind(group))(o); return scene; };
  scene.remove = (...objs) => { for (const o of objs) (o.parent === group ? group.remove.bind(group) : remove)(o); return scene; };

  let state;
  try { state = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch { state = null; }
  if (!state || !KEYS.every((k) => typeof state.params?.[k] === 'number')) state = { path: 0, params: { ...FCC_PARAMS }, cell: 1 };
  if (typeof state.cell !== 'number') state.cell = 1;

  const apply = () => {
    const S = shearMatrix(state.params); // rows
    group.matrix.set(S[0][0], S[0][1], S[0][2], 0, S[1][0], S[1][1], S[1][2], 0, S[2][0], S[2][1], S[2][2], 0, 0, 0, 0, 1);
    group.matrixWorldNeedsUpdate = true;
    onCell(cellDirectionsPreShear(state.params, state.cell));
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch { /* private mode */ }
    onChange(state);
  };

  const panel = buildPanel(state, apply);
  document.body.appendChild(panel);
  apply();
  return { group, getState: () => state };
}

function buildPanel(state, apply) {
  const panel = document.createElement('div');
  panel.id = 'kaleido-panel';
  panel.innerHTML = `
    <button type="button" id="kaleido-toggle" aria-expanded="false" title="Shear the lattice">⟋ Shear</button>
    <div id="kaleido-body" hidden>
      <label class="kaleido-row">Path <span id="kaleido-path-val"></span>
        <input type="range" id="kaleido-path" min="${PATH_RANGE[0]}" max="${PATH_RANGE[1]}" step="0.01" list="kaleido-stops">
      </label>
      <datalist id="kaleido-stops">${PATH_STOPS.map((s) => `<option value="${s.at}" label="${s.name}"></option>`).join('')}</datalist>
      <div class="kaleido-stops">${PATH_STOPS.map((s) => `<button type="button" data-stop="${s.at}">${s.name}</button>`).join('')}</div>
      <label class="kaleido-row">Cell <span id="kaleido-cell-val"></span>
        <input type="range" id="kaleido-cell" min="0" max="1" step="0.01"></label>
      <div id="kaleido-meter" title="How regular the cell is: 1 = every angle special (36, 45, 60, 70.5, 72 or 90 degrees)"></div>
      <div class="kaleido-stops"><button type="button" id="kaleido-prev">◀ Find</button><button type="button" id="kaleido-next">Find ▶</button></div>
      <details><summary>Six sliders</summary>
        ${KEYS.map((k) => {
          const isAngle = k.length > 1;
          return `<label class="kaleido-row">${isAngle ? `${{ alpha: 'α', beta: 'β', gamma: 'γ' }[k]}` : k} <span data-val="${k}"></span>
            <input type="range" data-key="${k}" min="${isAngle ? 20 : 0.3}" max="${isAngle ? 150 : 2.5}" step="${isAngle ? 0.1 : 0.005}"></label>`;
        }).join('')}
      </details>
      <button type="button" id="kaleido-export">Export member</button>
      <div id="kaleido-note" aria-live="polite"></div>
    </div>`;
  const style = document.createElement('style');
  style.textContent = `
    #kaleido-panel { position: fixed; right: 12px; top: 150px; z-index: 50; max-width: min(300px, calc(100vw - 24px)); font: 13px system-ui, sans-serif; color: #d8f0ff; }
    #kaleido-panel button { min-height: 36px; background: rgba(8, 20, 30, .85); color: #9de0ff; border: 1px solid #2c5a70; border-radius: 8px; padding: 4px 10px; cursor: pointer; }
    #kaleido-body { margin-top: 6px; padding: 10px; background: rgba(5, 12, 20, .92); border: 1px solid #2c5a70; border-radius: 10px; display: grid; gap: 8px; }
    #kaleido-body[hidden] { display: none; }
    .kaleido-row { display: grid; grid-template-columns: auto 1fr; gap: 2px 8px; align-items: center; }
    .kaleido-row input { grid-column: 1 / -1; width: 100%; min-height: 28px; }
    .kaleido-stops { display: flex; gap: 6px; flex-wrap: wrap; }
    #kaleido-note { font-size: 12px; color: #9de0ff; min-height: 1em; }`;
  panel.appendChild(style);
  const $ = (sel) => panel.querySelector(sel);
  const path = $('#kaleido-path');
  const refresh = () => {
    path.value = state.path ?? 0;
    $('#kaleido-cell').value = state.cell;
    $('#kaleido-cell-val').textContent = state.cell >= 0.995 ? '1 (equal edges)' : state.cell <= 0.005 ? '0 (sheared)' : state.cell.toFixed(2);
    const q = cellQuality(cellDirections(state.params, state.cell));
    $('#kaleido-meter').innerHTML = `Regularity <b>${q.score.toFixed(2)}</b> <span style="opacity:.75">· angles ${q.angles.map((a) => a.toFixed(1)).sort((x, y) => x - y).join(', ')}°</span>`;
    $('#kaleido-path-val').textContent = state.path === null ? '(off path)' : Number(state.path).toFixed(2);
    for (const k of KEYS) {
      panel.querySelector(`[data-key="${k}"]`).value = state.params[k];
      panel.querySelector(`[data-val="${k}"]`).textContent = k.length > 1 ? `${state.params[k].toFixed(1)}°` : state.params[k].toFixed(3);
    }
  };
  const setPath = (s) => { state.path = s; state.params = paramsOnPath(s); refresh(); apply(); };
  const cell = $('#kaleido-cell');
  cell.addEventListener('input', () => { state.cell = Number(cell.value); refresh(); apply(); });
  // Find previous / next: the path's quality peaks and hexagon events for the current Cell value.
  const targetsFor = new Map();
  const find = (dir) => {
    if (state.path === null) { $('#kaleido-note').textContent = 'Find works along the path: tap a stop first.'; return; }
    const key = state.cell.toFixed(2);
    if (!targetsFor.has(key)) targetsFor.set(key, pathTargets(state.cell));
    const list = targetsFor.get(key);
    const next = dir > 0 ? list.find((e) => e.at > state.path + 1e-3) : [...list].reverse().find((e) => e.at < state.path - 1e-3);
    if (!next) { $('#kaleido-note').textContent = 'Nothing further that way.'; return; }
    setPath(Math.round(next.at * 10000) / 10000);
    $('#kaleido-note').textContent = `${next.kind === 'hexagons' ? 'Hexagons: three edge directions in a plane' : 'Regular cell'} at ${next.at.toFixed(3)}.`;
  };
  $('#kaleido-prev').addEventListener('click', () => find(-1));
  $('#kaleido-next').addEventListener('click', () => find(1));
  $('#kaleido-toggle').addEventListener('click', () => {
    const body = $('#kaleido-body');
    body.hidden = !body.hidden;
    $('#kaleido-toggle').setAttribute('aria-expanded', String(!body.hidden));
  });
  path.addEventListener('input', () => setPath(Number(path.value)));
  panel.querySelectorAll('[data-stop]').forEach((b) => b.addEventListener('click', () => setPath(Number(b.dataset.stop))));
  panel.querySelectorAll('[data-key]').forEach((input) => input.addEventListener('input', () => {
    const next = { ...state.params, [input.dataset.key]: Number(input.value) };
    if (!paramsValid(next)) { $('#kaleido-note').textContent = 'That would flatten the cells to nothing.'; refresh(); return; }
    $('#kaleido-note').textContent = '';
    state.params = next;
    state.path = null; // off the straight path now
    refresh();
    apply();
  }));
  $('#kaleido-export').addEventListener('click', () => {
    const name = prompt('Name this population member:', state.path === null ? 'member' : `path ${Number(state.path).toFixed(2)}`);
    if (!name) return;
    const member = { name, credit: 'Kaleidoverse by DICTO', created: new Date().toISOString(), path: state.path, params: state.params, cell: state.cell, matrix: shearMatrix(state.params), cellDirections: cellDirections(state.params, state.cell), regularity: cellQuality(cellDirections(state.params, state.cell)).score };
    const blob = new Blob([JSON.stringify(member, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `kaleidoverse-${name.replace(/[^a-z0-9-]+/gi, '-')}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    $('#kaleido-note').textContent = `Exported "${name}".`;
  });
  refresh();
  return panel;
}
