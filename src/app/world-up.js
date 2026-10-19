// Universal PiTet (UP): a 3D+ world (DICTO 2026-10-19), DICTO's five-fold octet. From the Cleo star (20 Cleo-Icos, 20 spikes, 12 inward
// pyramids, 30 valley tetrahedra filling a dodecahedron) outward in spherical shells: 12 twisted frusta close the icosidodecahedron, then a
// cycle of four shells, ID -> rhombic triacontahedron -> DICTO GTI (golden truncated icosahedron) -> DICTO FPD (flat pentakis dodecahedron) -> ID again, 10/phi^4 larger,
// without end (each next solid has its faces through the last one's corners, at right angles to them). Triangles stay throughout (DICTO's
// name: Pi for the spherical progression, Tet for the triangles). Proved exactly in the research study studies/2026-10-19-five-fold-octet.
// Views: the shells; the 12 five-sided Vajras (inward pyramid + twisted frustum + outward pyramid, one convex piece each); the hexagonal
// Cleo stage (ID -> OG -> RT). The cycle's endless film is its own world on Dual Vision's standard (world-up-film.js), one tap away.
// Data: up-data.js (scripts/build-up-data.py). Words: i18n up.*.
import DATA from './up-data.js';
import { createLayeredWorld, ROLE } from './world-chains.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';

// Colour by shape family (DICTO 2026-10-19: by shape, not shell; then "colour families"): one colour per shape in every view and at
// every size, so the pieces that come back turn after turn show as the same colour (the build checks one shape per role), and the
// colours grouped in families: pyramids and Vajras warm, tetrahedra green, the shell pieces (frusta, cone pieces, caps) blue. The
// Cleo-Ico and its spike are one piece. UP's own role names, so other worlds' colours (Theaetetus's Cleo star) stay as they are.
Object.assign(ROLE, {
  upCleo: 0xffc857, upInPyr5: 0xffa726, upPyr5: 0xf06292, upPyr3: 0xf8bbd0, upHexCleo: 0xfff176, upVajra: 0xff8a65, upKitePyr: 0xffd180,       // pyramids: warm
  upCValley: 0x5fd38a, upValley: 0xaed581, upTet: 0x81c784,                                                                  // tetrahedra: green
  upFrustum: 0x4dd0e1, upRhomb: 0x9fb4c8, upPent: 0x64b5f6, upHex: 0x4db6ac, upTri: 0x7986cb, upCone5: 0x90caf9,           // shell pieces: blue
  upCone3: 0x80deea, upLow: 0xb3c7f7, upIDGlass: 0xf3ead6 });
export function createUpWorld({ scene, fitView, openWorld = () => {} }) {
  const w = createLayeredWorld({ scene, fitView, name: 'up', data: DATA, kinds: ['up'], prefix: 'up',
    glassRoles: { up: new Set(['upIDGlass']) }, defaultParts: { up: 'shells' } });
  // the cycle's film (DICTO 2026-10-19: "Dual Vision is the standard") lives in its own world, as Vajrayana's Cleo button opens Theaetetus
  const panel = document.getElementById('worldup-panel');
  const filmBtn = document.createElement('button'), kpBtn = document.createElement('button');
  filmBtn.type = kpBtn.type = 'button'; filmBtn.dataset.upFilm = 'open'; kpBtn.dataset.upFilm = 'kp';
  panel.querySelector('.w4d-options').append(filmBtn, kpBtn);
  // the tall companion, the DICTO Kepler–Poinsot–PiTet Cycle (DICTO 2026-10-19), has its own film too
  const label = () => { const L = getSettings().language; filmBtn.textContent = `∞ ${t('up.film.open', L)}`; kpBtn.textContent = `∞ ${t('up.film.kp', L)}`; };
  label(); onSettingsChange(label);
  filmBtn.addEventListener('click', () => openWorld('tool:upFilmWorld', 'Universal PiTet'));
  kpBtn.addEventListener('click', () => openWorld('tool:kpFilmWorld', 'Kepler–Poinsot–PiTet'));
  return w;
}

/** Points whose convex hull previews the world in the DICTO menu: the Vajras round the core. */
export function upPreviewPoints() {
  return DATA.up.views.vajras.flatMap((p) => p[1]);
}
