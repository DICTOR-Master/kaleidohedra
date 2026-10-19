// Universal PiTet (UP): a 3D+ world (DICTO 2026-10-19), DICTO's five-fold octet. From the Cleo star (20 Cleo-Icos, 20 spikes, 12 inward
// pyramids, 30 valley tetrahedra filling a dodecahedron) outward in spherical shells: 12 twisted frusta close the icosidodecahedron, then a
// cycle of four shells, ID -> rhombic triacontahedron -> DICTO GTI (golden truncated icosahedron) -> DICTO FPD (flat pentakis dodecahedron) -> ID again, 10/phi^4 larger,
// without end (each next solid has its faces through the last one's corners, at right angles to them). Triangles stay throughout (DICTO's
// name: Pi for the spherical progression, Tet for the triangles). Proved exactly in the research study studies/2026-10-19-five-fold-octet.
// Views: the shells; the 12 five-sided Vajras (inward pyramid + twisted frustum + outward pyramid, one convex piece each); the hexagonal
// Cleo stage (ID -> OG -> RT); the cycle, four turns, with the endless film: one toggle zooms out (Unwrap) or in (Wrap) for ever, as each
// turn is the last one 10/phi^4 larger, so the film loops without a seam (DICTO's infinity player idea).
// Data: up-data.js (scripts/build-up-data.py). Words: i18n up.*.
import DATA from './up-data.js';
import { createLayeredWorld, ROLE } from './world-chains.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';

// Colour by shape family (DICTO 2026-10-19: by shape, not shell; then "colour families"): one colour per shape in every view and at
// every size, so the pieces that come back turn after turn show as the same colour (the build checks one shape per role), and the
// colours grouped in families: pyramids and Vajras warm, tetrahedra green, the shell pieces (frusta, cone pieces, caps) blue. The
// Cleo-Ico and its spike are one piece. UP's own role names, so other worlds' colours (Theaetetus's Cleo star) stay as they are.
Object.assign(ROLE, {
  upCleo: 0xffc857, upInPyr5: 0xffa726, upPyr5: 0xf06292, upPyr3: 0xf8bbd0, upHexCleo: 0xfff176, upVajra: 0xff8a65,       // pyramids: warm
  upCValley: 0x5fd38a, upValley: 0xaed581, upTet: 0x81c784,                                                                  // tetrahedra: green
  upFrustum: 0x4dd0e1, upRhomb: 0x9fb4c8, upPent: 0x64b5f6, upHex: 0x4db6ac, upTri: 0x7986cb, upCone5: 0x90caf9,           // shell pieces: blue
  upCone3: 0x80deea, upLow: 0xb3c7f7, upCap: 0x5c6bc0, upIDGlass: 0xf3ead6,
  upSolidID: 0xfff176, upSolidRT: 0x4dd0e1, upSolidTI: 0xf06292, upSolidQ: 0x5fd38a });                                     // the cycle's solids
// The cycle view shows the four solids of each turn (role + 'G'), drawn by their far faces only, so the endless film looks into them
// like a bowl and sees every layer at once.
const CYCLE = ['upSolidID', 'upSolidRT', 'upSolidTI', 'upSolidQ'];
for (const r of CYCLE) ROLE[`${r}G`] = ROLE[r];

export function createUpWorld({ scene, fitView }) {
  const w = createLayeredWorld({ scene, fitView, name: 'up', data: DATA, kinds: ['up'], prefix: 'up',
    glassRoles: { up: new Set(['upIDGlass']) }, defaultParts: { up: 'shells' }, backOnly: new Set(CYCLE.map((r) => `${r}G`)) });
  // ---- the endless film (cycle view): the world's group scales by 10/phi^4 per turn and wraps round without a seam ----
  const K = DATA.up.K, R0 = DATA.up.turnRadius;
  const panel = document.getElementById('worldup-panel');
  const row = document.createElement('div');
  row.className = 'w4d-row w4d-options';
  row.innerHTML = '<button type="button" data-up-film="out"></button><button type="button" data-up-film="in"></button>';
  panel.querySelector('.w4d-options').after(row);
  const select = panel.querySelector('[data-select="part"]');
  let dir = 0, raf = null, phase = 0, last = 0, active = false;
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isCycle = () => select.value === 'cycle';
  function label() {
    const L = getSettings().language;
    row.hidden = !isCycle();
    row.querySelector('[data-up-film="out"]').textContent = dir > 0 ? `⏸ ${t('up.film.pause', L)}` : `∞ ${t('up.film.unwrap', L)}`;
    row.querySelector('[data-up-film="in"]').textContent = dir < 0 ? `⏸ ${t('up.film.pause', L)}` : `∞ ${t('up.film.wrap', L)}`;
  }
  const setScale = () => w.group.scale.setScalar(K ** -phase);              // phase 0..1: one turn
  function tick(now) {
    // one turn about every 8 s (reduced motion: one turn every 2 s, in a step)
    const dt = Math.min(0.1, (now - last) / 1000); last = now;
    phase += dir * (reduce() ? 0 : dt / 8);
    phase = ((phase % 1) + 1) % 1;
    setScale();
    raf = requestAnimationFrame(tick);
  }
  let stepper = null;
  function play(d) {
    stop();
    dir = d; last = performance.now();
    if (reduce()) stepper = setInterval(() => { phase = ((phase + dir * 0.25) % 1 + 1) % 1; setScale(); }, 2000);
    else raf = requestAnimationFrame(tick);
    label();
  }
  function stop() { if (raf) cancelAnimationFrame(raf); if (stepper) clearInterval(stepper); raf = stepper = null; dir = 0; label(); }
  function rest() { stop(); phase = 0; setScale(); }
  row.addEventListener('click', (e) => {
    const b = e.target.closest('[data-up-film]'); if (!b) return;
    const d = b.dataset.upFilm === 'out' ? 1 : -1;
    if (dir === d) stop(); else play(d);
  });
  // the cycle view opens on the middle turn (the inner turn small inside it, the outer one round the edge)
  const fitCycle = () => { if (isCycle()) fitView([0, 0, 0], R0 * WS * 1.2); };
  select.addEventListener('change', () => { rest(); fitCycle(); });
  onSettingsChange(() => { if (active) label(); });
  return {
    ...w,
    get group() { return w.group; },
    openView(name) { w.openView(name); rest(); fitCycle(); },
    setActive(on) { active = on; if (!on) rest(); w.setActive(on); if (on) { label(); fitCycle(); } },
    resetView() { rest(); w.resetView(); },
  };
}

/** Points whose convex hull previews the world in the DICTO menu: the first ID's shell. */
export function upPreviewPoints() {
  return DATA.up.views.vajras.flatMap((p) => p[1]);
}
