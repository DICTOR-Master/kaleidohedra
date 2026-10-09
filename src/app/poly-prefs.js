// Polyhedraverse's Favourites and Recent (step D4, DICTO 2026-10-09: pins = Favourites, Recent = the
// build queue), shared by the shape strip and the DICTO menu's browser, saved in this browser.
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { storageKey } from './site.js';

const KEY = storageKey('poly-prefs');
const RECENT_MAX = 8;
let state = { pins: [], recent: [] };
try {
  const data = JSON.parse(localStorage.getItem(KEY) ?? 'null');
  if (data) state = { pins: (data.pins ?? []).filter((id) => POLYHEDRA[id]), recent: (data.recent ?? []).filter((id) => POLYHEDRA[id]).slice(0, RECENT_MAX) };
} catch { /* blocked storage: start empty */ }
const listeners = new Set();
function changed() {
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* best-effort */ }
  listeners.forEach((fn) => fn());
}
export const favourites = () => [...state.pins];
export const recent = () => [...state.recent];
export const isFavourite = (id) => state.pins.includes(id);
export function toggleFavourite(id) {
  state.pins = isFavourite(id) ? state.pins.filter((x) => x !== id) : [...state.pins, id];
  changed();
}
/** A shape used: Recent, newest first. */
export function remember(id) {
  if (!POLYHEDRA[id] || state.recent[0] === id) return;
  state.recent = [id, ...state.recent.filter((x) => x !== id)].slice(0, RECENT_MAX);
  changed();
}
/** Earlier saves kept pins and the queue inside the build: take them over once. */
export function adopt(pins = [], queue = []) {
  if (state.pins.length || state.recent.length) return;
  state = { pins: pins.filter((id) => POLYHEDRA[id]), recent: queue.filter((id) => POLYHEDRA[id]).slice(0, RECENT_MAX) };
  if (state.pins.length || state.recent.length) changed();
}
export function onPrefsChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }
