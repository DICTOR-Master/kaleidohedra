// Kaleidohedra by DICTO: the lattice shear (direct decisions 2026-10-01).
//
// Every piece of geometry lives in one group whose transform is a linear
// map A. A comes from six lattice parameters -- the lengths a, b, c
// (relative to FCC) and the angles alpha, beta, gamma between FCC's three
// primitive cell vectors (60 degrees each for plain FCC). Building works
// exactly as in Rhombiverse: taps are resolved in each piece's own frame,
// and raycasting follows the group's transform.
//
// One "path" slider moves all six along a straight line from FCC (0)
// through a halfway stop (1) to the "Towards" target (2: DICTO FCC, or
// Bain, where BCC becomes FCC) and beyond, stopping before the cells
// would collapse. The six sliders give full control. Export
// saves the current state as a named "population member".
import * as THREE from 'three';

import { KEYS, FCC_PARAMS, TOWARDS, pathStops, pathRange, paramsOnPath, paramsValid, shearMatrix, cellDirections, cellDirectionsPreShear, cellQuality, disphenoidQuality, pathTargets, pathGaps, cellFillsSpace } from '../krp-core/src/geometry-extensions/kaleido-lattice.js';

import { objectId, parseObjectId } from '../krp-core/src/vocabulary.js';
import { keepEntry, checkKept, isKeptEntry } from '../krp-core/src/retention.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { storageKey } from './site.js';

const STORAGE_KEY = storageKey('shear');
// Kept states (KRP stage 4, DICTO's decisions 2026-10-08): each visitor's own list, in this browser
// only, of { id, fingerprint, kept, name }; never coordinates. DICTO curates.
const KEPT_KEY = storageKey('kept');
const lang = () => getSettings().language;
const readKept = () => { try { const a = JSON.parse(localStorage.getItem(KEPT_KEY) || '[]'); return Array.isArray(a) ? a.filter(isKeptEntry) : []; } catch { return []; } };
const writeKept = (list) => { try { localStorage.setItem(KEPT_KEY, JSON.stringify(list)); } catch { /* private mode: this session only */ } };
/** The current slider state's object ID in krp-core. */
export const shearId = (state) => objectId('kaleido/cell', { ...state.params, t: state.cell });

/**
 * Installs the shear: routes everything added to the scene (except the
 * camera) into one group, and builds the slider panel.
 */
export function installShear({ scene, camera, onChange = () => {}, onCell = () => {} }) {
  const group = new THREE.Group();
  group.name = 'kaleidohedra-shear';
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
  if (!TOWARDS[state.towards]) state.towards = 'dicto';

  // Off (another app's space, which has no shear): the lattice unsheared and the cell the regular
  // rhombic dodecahedron, without touching the saved state; on again, the saved shear returns.
  let enabled = true;
  const apply = () => {
    if (!enabled) {
      group.matrix.identity();
      group.matrixWorldNeedsUpdate = true;
      onCell(cellDirectionsPreShear(FCC_PARAMS, 1));
      onChange(state);
      return;
    }
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
  return {
    group,
    getState: () => state,
    setEnabled(on) {
      if (on === enabled) return;
      enabled = on;
      panel.hidden = !on;
      apply();
    },
    isEnabled: () => enabled,
  };
}

function buildPanel(state, apply) {
  const panel = document.createElement('div');
  panel.id = 'kaleido-panel';
  panel.innerHTML = `
    <button type="button" id="kaleido-toggle" aria-expanded="false" title="Shear the lattice">⟋ Shear</button>
    <div id="kaleido-body" hidden>
      <button type="button" id="kaleido-reset" title="Back to the ordinary FCC lattice and its regular rhombic dodecahedron">↺ Reset to FCC</button>
      <label class="kaleido-row">Towards
        <select id="kaleido-towards">${Object.entries(TOWARDS).map(([id, t]) => `<option value="${id}">${t.name}</option>`).join('')}</select>
      </label>
      <label class="kaleido-row">Path <span id="kaleido-path-val"></span>
        <input type="range" id="kaleido-path" step="0.01" list="kaleido-stops">
        <span id="kaleido-band" aria-hidden="true"></span>
      </label>
      <datalist id="kaleido-stops"></datalist>
      <div class="kaleido-stops" id="kaleido-stop-buttons"></div>
      <label class="kaleido-row">Cell <span id="kaleido-cell-val"></span>
        <input type="range" id="kaleido-cell" min="0" max="1" step="0.01"></label>
      <div id="kaleido-meter" title="How regular the cell is: 1 = every angle special (36, 45, 60, 70.5, 72 or 90 degrees)"></div>
      <div class="kaleido-stops"><button type="button" id="kaleido-find">Find</button></div>
      <details><summary>Six sliders</summary>
        ${KEYS.map((k) => {
          const isAngle = k.length > 1;
          return `<label class="kaleido-row">${isAngle ? `${{ alpha: 'α', beta: 'β', gamma: 'γ' }[k]}` : k} <span data-val="${k}"></span>
            <input type="range" data-key="${k}" min="${isAngle ? 20 : 0.3}" max="${isAngle ? 150 : 2.5}" step="${isAngle ? 0.1 : 0.005}"></label>`;
        }).join('')}
      </details>
      <button type="button" id="kaleido-export">Export member</button>
      <div class="kaleido-stops"><button type="button" id="kaleido-keep"></button></div>
      <details id="kaleido-kept"><summary></summary><div id="kaleido-kept-list"></div></details>
      <div id="kaleido-note" aria-live="polite"></div>
    </div>`;
  const style = document.createElement('style');
  style.textContent = `
    /* Beside the tools column (top right), never under it: the column's width plus a gap from the edge. */
    #kaleido-panel { position: fixed; right: calc(12px + var(--touch) + 8px); top: 150px; z-index: 50; max-width: min(300px, calc(100vw - 88px)); font: var(--text-m) var(--font-ui); color: #d8f0ff; }
    @media (pointer: coarse) and (min-width: 700px) and (min-height: 600px) { #kaleido-panel { right: calc(28px + var(--touch) + 14px); top: 166px; } } /* tablets: clear of the tools column, which moves in from the iPad's edges */
    #kaleido-panel button { min-height: var(--touch-compact); background: rgba(30, 14, 4, .85); color: var(--accent); border: 1px solid #7a3300; border-radius: var(--radius-m); padding: 4px 10px; cursor: pointer; }
    #kaleido-body { margin-top: 6px; padding: 10px; background: rgba(18, 8, 2, .92); border: 1px solid #7a3300; border-radius: var(--radius-l); display: grid; gap: 8px;
      max-height: calc(100dvh - 280px); overflow-y: auto; overscroll-behavior: contain; } /* phones: the Kept list or the six sliders must stay reachable */
    #kaleido-body[hidden] { display: none; }
    .kaleido-row { display: grid; grid-template-columns: auto 1fr; gap: 2px 8px; align-items: center; }
    .kaleido-row input, .kaleido-row select { grid-column: 1 / -1; width: 100%; min-height: 28px; }
    #kaleido-towards { min-height: var(--touch-compact); background: rgba(30, 14, 4, .85); color: var(--accent); border: 1px solid #7a3300; border-radius: var(--radius-m); }
    .kaleido-stops { display: flex; gap: 6px; flex-wrap: wrap; }
    /* The red band (DICTO, 2026-10-08): where on the path the cell stops filling space, for this Cell value.
       Inset by half a thumb so it lines up with the slider's travel. */
    #kaleido-band { grid-column: 1 / -1; height: 5px; margin: -2px 9px 0; border-radius: 3px; }
    .kaleido-gap { color: #ff6b6b; }
    #kaleido-note { font-size: var(--text-s); color: var(--accent); min-height: 1em; overflow-wrap: anywhere; }
    #kaleido-kept-list { display: grid; gap: 6px; margin-top: 6px; }
    .kept-row { display: grid; grid-template-columns: 1fr auto; gap: 4px 6px; align-items: center; padding: 6px; border: 1px solid #4a2000; border-radius: var(--radius-m); }
    .kept-row .kept-name { overflow-wrap: anywhere; }
    .kept-row .kept-when { grid-column: 1 / -1; font-size: var(--text-xs); opacity: .75; }
    .kept-row .kept-actions { grid-column: 1 / -1; display: flex; gap: 6px; flex-wrap: wrap; }
    .kept-row .kept-actions button { min-height: var(--touch-compact); }`;
  panel.appendChild(style);
  const $ = (sel) => panel.querySelector(sel);
  const path = $('#kaleido-path');
  const towards = $('#kaleido-towards');
  // Stops and range belong to the chosen target.
  const layoutPath = () => {
    const [lo, hi] = pathRange(state.towards);
    path.min = lo; path.max = hi;
    const stops = pathStops(state.towards);
    $('#kaleido-stops').innerHTML = stops.map((s) => `<option value="${s.at}" label="${s.name}"></option>`).join('');
    $('#kaleido-stop-buttons').innerHTML = stops.map((s) => `<button type="button" data-stop="${s.at}">${s.name}</button>`).join('');
    $('#kaleido-stop-buttons').querySelectorAll('[data-stop]').forEach((b) => b.addEventListener('click', () => setPath(Number(b.dataset.stop))));
  };
  const refresh = () => {
    towards.value = state.towards;
    path.value = state.path ?? 0;
    $('#kaleido-cell').value = state.cell;
    $('#kaleido-cell-val').textContent = state.cell >= 0.995 ? '1 (equal edges)' : state.cell <= 0.005 ? '0 (sheared)' : state.cell.toFixed(2);
    const q = cellQuality(cellDirections(state.params, state.cell));
    $('#kaleido-meter').innerHTML = `Regularity <b>${q.score.toFixed(2)}</b> <span style="opacity:.75">· angles ${q.angles.map((a) => a.toFixed(1)).sort((x, y) => x - y).join(', ')}°</span>`;
    if (state.towards === 'bain') {
      // The BCC disphenoids: shortest / longest edge, 1 = regular tetrahedron.
      const d = disphenoidQuality(state.params);
      $('#kaleido-meter').innerHTML += `<br>Disphenoids <b>${d.best.toFixed(3)}</b> <span style="opacity:.75">· ${d.regular} of 6 regular tetrahedra</span>`;
    }
    $('#kaleido-path-val').textContent = state.path === null ? '(off path)' : Number(state.path).toFixed(2);
    if (!cellFillsSpace(state.params, state.cell)) $('#kaleido-meter').innerHTML += `<br><span class="kaleido-gap">${t('shear.gap', lang())}</span>`;
    paintBand();
    for (const k of KEYS) {
      panel.querySelector(`[data-key="${k}"]`).value = state.params[k];
      panel.querySelector(`[data-val="${k}"]`).textContent = k.length > 1 ? `${state.params[k].toFixed(1)}°` : state.params[k].toFixed(3);
    }
  };
  // Recomputed for each Cell value (about 0.2 s), cached; while the Cell slider moves, the last band stays.
  const gapsFor = new Map();
  const paintBand = (force = false) => {
    const key = `${state.towards} ${state.cell.toFixed(2)}`;
    if (!gapsFor.has(key) && !force && cellDragging) return;
    if (!gapsFor.has(key)) gapsFor.set(key, pathGaps(state.cell, state.towards));
    const [lo, hi] = pathRange(state.towards);
    const at = (x) => `${(((x - lo) / (hi - lo)) * 100).toFixed(2)}%`;
    const red = 'rgba(255, 70, 70, .85)';
    const stops = gapsFor.get(key).flatMap(([a, b]) => [`transparent ${at(a)}`, `${red} ${at(a)}`, `${red} ${at(b)}`, `transparent ${at(b)}`]);
    $('#kaleido-band').style.background = stops.length ? `linear-gradient(to right, ${stops.join(', ')})` : 'none';
    $('#kaleido-band').title = gapsFor.get(key).length ? t('shear.gap', lang()) : '';
  };
  let cellDragging = false;
  const setPath = (s) => { state.path = s; state.params = paramsOnPath(s, state.towards); refresh(); apply(); };
  const cell = $('#kaleido-cell');
  cell.addEventListener('input', () => { cellDragging = true; state.cell = Number(cell.value); refresh(); apply(); });
  cell.addEventListener('change', () => { cellDragging = false; paintBand(true); });
  // Find (no arrows, DICTO 2026-10-09): the next of the path's quality peaks and hexagon events for the
  // current Cell value, round to the first after the last.
  const targetsFor = new Map();
  const find = () => {
    if (state.path === null) { $('#kaleido-note').textContent = 'Find works along the path: tap a stop first.'; return; }
    const key = `${state.towards} ${state.cell.toFixed(2)}`;
    if (!targetsFor.has(key)) targetsFor.set(key, pathTargets(state.cell, 0.6, pathRange(state.towards), 0.02, state.towards));
    const list = targetsFor.get(key);
    const next = list.find((e) => e.at > state.path + 1e-3) ?? list[0];
    if (!next) { $('#kaleido-note').textContent = 'Nothing to find on this path.'; return; }
    setPath(Math.round(next.at * 10000) / 10000);
    const what = { hexagons: 'Hexagons: three edge directions in a plane', 'regular tetrahedra': 'Disphenoids become regular tetrahedra (BCC is now FCC)' }[next.kind] || 'Regular cell';
    $('#kaleido-note').textContent = `${what} at ${next.at.toFixed(3)}.`;
  };
  $('#kaleido-find').addEventListener('click', find);
  $('#kaleido-toggle').addEventListener('click', () => {
    const body = $('#kaleido-body');
    body.hidden = !body.hidden;
    $('#kaleido-toggle').setAttribute('aria-expanded', String(!body.hidden));
  });
  path.addEventListener('input', () => setPath(Number(path.value)));
  towards.addEventListener('change', () => { state.towards = towards.value; layoutPath(); setPath(0); });
  // Reset (direct request: "I got lost and couldn't figure where normal was"): the
  // starting state, the ordinary FCC lattice with its regular RD. Towards goes back
  // to DICTO FCC too, since on the Bain path 0 is BCC, not FCC.
  $('#kaleido-reset').addEventListener('click', () => {
    state.towards = 'dicto';
    state.cell = 1;
    layoutPath();
    setPath(0);
    $('#kaleido-note').textContent = 'Back to the ordinary FCC lattice.';
  });
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
    const member = { name, credit: 'Kaleidohedra by DICTO', created: new Date().toISOString(), towards: state.towards, path: state.path, params: state.params, cell: state.cell, matrix: shearMatrix(state.params), cellDirections: cellDirections(state.params, state.cell), regularity: cellQuality(cellDirections(state.params, state.cell)).score };
    const blob = new Blob([JSON.stringify(member, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `kaleidohedra-${name.replace(/[^a-z0-9-]+/gi, '-')}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    $('#kaleido-note').textContent = `Exported "${name}".`;
  });
  // ---- Keep (KRP stage 4) ----
  const note = (text) => { $('#kaleido-note').textContent = text; };
  const MARK = { same: '✓', changed: '⚠', unavailable: '✗' };
  const renderKept = () => {
    const L = lang();
    const list = readKept();
    $('#kaleido-keep').textContent = `☆ ${t('kept.keep', L)}`;
    $('#kaleido-kept').hidden = !list.length;
    $('#kaleido-kept summary').textContent = t('kept.list', L, { n: list.length });
    $('#kaleido-kept-list').innerHTML = list.map((e, i) => {
      const c = checkKept(e);
      return `<div class="kept-row" data-i="${i}">
        <span class="kept-name">${escapeHtml(e.name || t('kept.unnamed', L))}</span>
        <span title="${escapeHtml(t(`kept.check.${c.result}`, L, { version: c.madeWith ?? '' }))}">${MARK[c.result]}</span>
        <span class="kept-when">${escapeHtml(new Date(e.kept).toLocaleString(L))}${c.madeWith ? ` · krp-core ${escapeHtml(c.madeWith)}` : ''}</span>
        <span class="kept-actions">
          <button type="button" data-act="open"${c.result === 'unavailable' ? ' hidden' : ''}>${t('kept.open', L)}</button>
          <button type="button" data-act="copy">${t('kept.copy', L)}</button>
          <button type="button" data-act="remove" aria-label="${escapeHtml(t('kept.remove', L))}">✕</button>
        </span></div>`;
    }).join('');
  };
  $('#kaleido-keep').addEventListener('click', () => {
    const L = lang();
    const suggested = state.path === null ? '' : `${t('kept.path', L)} ${Number(state.path).toFixed(2)} · ${t('kept.cell', L)} ${state.cell.toFixed(2)}`;
    const name = prompt(t('kept.name', L), suggested);
    if (name === null) return;
    let entry;
    try { entry = keepEntry(shearId(state), name.trim()); } catch (e) { note(e.message); return; }
    writeKept([entry, ...readKept().filter((k) => k.id !== entry.id)]);
    renderKept();
    $('#kaleido-kept').open = true;
    note(t('kept.done', L));
  });
  $('#kaleido-kept-list').addEventListener('click', (ev) => {
    const b = ev.target.closest('button[data-act]');
    if (!b) return;
    const L = lang();
    const list = readKept();
    const e = list[Number(b.closest('.kept-row').dataset.i)];
    if (!e) return;
    if (b.dataset.act === 'open') {
      const c = checkKept(e);
      if (c.result === 'unavailable') { note(t('kept.check.unavailable', L)); return; }
      const { t: cellT, ...params } = parseObjectId(e.id).params;
      state.params = Object.fromEntries(KEYS.map((k) => [k, params[k]]));
      state.cell = cellT;
      state.path = null;
      refresh();
      apply();
      note(`${e.name || t('kept.unnamed', L)}: ${t(`kept.check.${c.result}`, L, { version: c.madeWith ?? '' })}`);
    } else if (b.dataset.act === 'copy') {
      const done = () => note(t('kept.copied', L));
      if (navigator.clipboard?.writeText) navigator.clipboard.writeText(e.id).then(done, () => note(e.id));
      else note(e.id);
    } else if (b.dataset.act === 'remove') {
      if (!confirm(t('kept.removeAsk', L, { name: e.name || t('kept.unnamed', L) }))) return;
      writeKept(list.filter((k) => k !== e));
      renderKept();
    }
  });
  onSettingsChange(renderKept);

  layoutPath();
  refresh();
  renderKept();
  return panel;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}
