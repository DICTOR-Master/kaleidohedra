// First-run welcome/entry overlay: Kaleidohedra's symbol (the regular-hexagon
// ED, turning) with an ENTER button centred on it, links to the sibling sites, legal-doc links.
// Purely a DOM/localStorage concern, independent of render.js/world state.
import { buildWheelFaces } from './rhombic-wheel-3d-core.js';
import { getSettings, onSettingsChange } from './settings.js';
import { t } from './i18n.js';
import { dimensionLabel } from './dimension-label.js';
import { openGuide } from './guide.js';
import { createLanguagePicker } from './language-picker.js';

// The welcome screen shows on every visit (direct decision 2026-09-25:
// the "Don't show this again" opt-out was removed). This is the key that
// opt-out used to store; it's cleared on load so it can't linger.
const LEGACY_SKIP_KEY = 'rhombiverse-skip-intro';

// The welcome symbol: Kaleidohedra's own shape, the regular-hexagon elongated
// dodecahedron (the wheel's geometry, DISCOVERIES.md #5), as a turning
// wireframe like Rhombiverse's and Polyhedraverse's logos. Plain SVG, no
// second WebGL context; each frame only moves its edges' end points.
const ED_FACES = buildWheelFaces();
const ED_EDGES = (() => {
  const seen = new Map();
  for (const { verts } of ED_FACES) verts.forEach((a, i) => {
    const b = verts[(i + 1) % verts.length];
    const key = [a, b].map((v) => v.map((c) => c.toFixed(5)).join()).sort().join('|');
    if (!seen.has(key)) seen.set(key, [a, b]);
  });
  return [...seen.values()];
})();
const LOGO_SCALE = 30;
const LOGO_TILT = 0.08;
// Sway: back and forth about the vertical, never end-on, so it always lies horizontal.
const SWAY = 0.38; // radians each way (about 22 degrees)
const SWAY_SPEED = 0.75; // radians of phase per second (one sway in about 8 seconds)
const rotX = ([x, y, z], a) => [x, y * Math.cos(a) - z * Math.sin(a), y * Math.sin(a) + z * Math.cos(a)];
const rotY = ([x, y, z], a) => [x * Math.cos(a) + z * Math.sin(a), y, -x * Math.sin(a) + z * Math.cos(a)];
// As in the logo (direct request): lying level, its long axis (z in the wheel
// frame) exactly left to right and side-on, a belt hexagon facing the viewer so
// the view is symmetric. (The logo also shows a square face-on, which the true
// shape can't do at the same time: its squares sit at 45 degrees to the long
// axis.) The frame comes from the geometry: toward the viewer = that hexagon's
// centre direction, screen right = the long axis, up = right x toward. It sways
// gently about the vertical, never turning end-on.
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const unit3 = (a) => { const l = Math.hypot(...a); return a.map((c) => c / l); };
const VIEW = (() => {
  const sq = ED_FACES.find((f) => f.type === 'hexagon');
  const toward = unit3(sq.verts.reduce((acc, v) => acc.map((c, i) => c + v[i]), [0, 0, 0]));
  const along = dot3([0, 0, 1], toward);
  const right = unit3([0, 0, 1].map((c, i) => c - along * toward[i]));
  const up = [right[1] * toward[2] - right[2] * toward[1], right[2] * toward[0] - right[0] * toward[2], right[0] * toward[1] - right[1] * toward[0]];
  return { right, up, toward };
})();
function place(v, angle) {
  const view = [dot3(v, VIEW.right), dot3(v, VIEW.up), dot3(v, VIEW.toward)];
  return rotX(rotY(view, angle), LOGO_TILT);
}
function drawLogo(svg, angle) {
  svg.querySelectorAll('.ed-edge').forEach((el, i) => {
    const [a, b] = ED_EDGES[i].map((v) => place(v, angle));
    el.setAttribute('x1', (a[0] * LOGO_SCALE).toFixed(1));
    el.setAttribute('y1', (-a[1] * LOGO_SCALE).toFixed(1));
    el.setAttribute('x2', (b[0] * LOGO_SCALE).toFixed(1));
    el.setAttribute('y2', (-b[1] * LOGO_SCALE).toFixed(1));
  });
}
function logoHtml() {
  return `
    <div id="welcome-logo">
      <svg id="welcome-logo-svg" viewBox="-75 -75 150 150" role="img" aria-label="Kaleidohedra symbol: a wireframe regular-hexagon elongated dodecahedron, turning slowly">
        <g stroke="#9de0ff" stroke-width="1.5" stroke-linecap="round" fill="none">${ED_EDGES.map(() => '<line class="ed-edge" />').join('')}</g>
      </svg>
      <button type="button" id="static-enter-label">ENTER</button>
    </div>`;
}
function startLogoSpin() {
  const svg = document.getElementById('welcome-logo-svg');
  if (!svg) return () => {};
  const still = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  let phase = 0, lastT = null, raf = null;
  const frame = (t) => {
    const dt = lastT === null ? 0 : Math.min(0.1, (t - lastT) / 1000);
    lastT = t;
    phase += SWAY_SPEED * dt;
    drawLogo(svg, SWAY * Math.sin(phase));
    raf = requestAnimationFrame(frame);
  };
  drawLogo(svg, 0);
  if (!still) raf = requestAnimationFrame(frame);
  return () => { if (raf !== null) cancelAnimationFrame(raf); };
}

// The overview line, then Kaleidohedra's own worlds, where the shear
// means something: 3D+ (the Wizard's sheared lattices), EKP and Targets.
// Redrawn on a language change.
const OWN_WORLDS = [
  { label: () => dimensionLabel('3D'), dim: '3D' },
  { label: () => 'EKP', world: 'tool:roofFoldWorld' },
  { label: () => 'Targets', world: 'tool:targetsWorld' },
];
function overviewHtml(lang) {
  return `${t('welcome.overview', lang)}<span class="dim-links">${OWN_WORLDS.map((w) => `<button type="button" class="dim-link" ${w.dim ? `data-dim="${w.dim}"` : `data-world="${w.world}"`}>${w.label()}</button>`).join('')}</span>`;
}

function overlayHtml() {
  const lang = getSettings().language;
  return `
    <div id="welcome-card">
      <div class="welcome-lang"></div>
      <h1>Kaleidohedra</h1>
      <p class="overview">${overviewHtml(lang)}</p>
      <button type="button" class="how-to-link" id="welcome-how-to" data-i18n-html="welcome.howTo">${t('welcome.howTo', lang)}</button>
      <div class="rhombiverse-link">
        <img src="./assets/rhombiverse-favicon-64.png" alt="" width="28" height="28" />
        <a href="https://rhombiverse.vercel.app" target="_blank" rel="noopener" data-i18n-html="welcome.rhombiverseLink">${t('welcome.rhombiverseLink', lang)}</a>
      </div>
      ${logoHtml()}
      <div class="polyhedraverse-link">
        <img src="./assets/polyhedraverse-favicon-64.png" alt="" width="28" height="28" />
        <a href="https://polyhedraverse.vercel.app" target="_blank" rel="noopener" data-i18n-html="welcome.polyhedraverseLink">${t('welcome.polyhedraverseLink', lang)}</a>
      </div>
      <div class="legal-links">
        <a href="./legal.html?doc=terms" target="_blank" rel="noopener">Terms</a>
        · <a href="./legal.html?doc=privacy" target="_blank" rel="noopener">Privacy</a>
        · <a href="./legal.html?doc=security" target="_blank" rel="noopener">Security</a>
        · <a href="https://github.com/DICTOR-Master/kaleidohedra" target="_blank" rel="noopener">Source</a>
      </div>
    </div>`;
}

function init() {
  const overlay = document.createElement('div');
  overlay.id = 'welcome-overlay';
  overlay.innerHTML = overlayHtml();
  document.body.appendChild(overlay);
  overlay.querySelector('.welcome-lang').appendChild(createLanguagePicker());
  // Delegated, so it survives overlayHtml() being re-rendered.
  overlay.addEventListener('click', (e) => {
    if (e.target.closest('#static-enter-label')) { enterWorld(); return; }
    if (e.target.closest('#welcome-how-to')) openGuide();
    const link = e.target.closest('.dim-link');
    if (link) {
      hide();
      if (link.dataset.dim) window.dispatchEvent(new CustomEvent('rhombiverse:open-wizard', { detail: link.dataset.dim }));
      else window.dispatchEvent(new CustomEvent('kaleidohedra:open-world', { detail: link.dataset.world }));
    }
  });
  onSettingsChange((s) => { const p = overlay.querySelector('.overview'); if (p) p.innerHTML = overviewHtml(s.language); });

  const aboutBtn = document.createElement('button');
  aboutBtn.id = 'about-btn';
  aboutBtn.type = 'button';
  aboutBtn.title = t('welcome.aboutTitle', getSettings().language);
  aboutBtn.dataset.i18nTitle = 'welcome.aboutTitle';
  aboutBtn.textContent = 'ℹ';
  document.body.appendChild(aboutBtn);

  let stopLogoSpin = () => {};
  function show() {
    overlay.style.display = 'flex';
    stopLogoSpin();
    stopLogoSpin = startLogoSpin();
  }
  function hide() {
    overlay.style.display = 'none';
    stopLogoSpin();
  }


  function enterWorld() {
    hide();
  }

  // Keyboard fallback -- the ENTER button is always clickable, but
  // a literal Enter keypress works too, for anyone who reaches for the
  // keyboard instead of the mouse/touch. Only acts while the overlay is
  // actually shown.
  window.addEventListener('keydown', (e) => {
    if (overlay.style.display === 'none') return;
    if (e.code === 'Enter' || e.code === 'NumpadEnter') {
      e.preventDefault();
      enterWorld();
    }
  });

  aboutBtn.addEventListener('click', show);

  try {
    localStorage.removeItem(LEGACY_SKIP_KEY);
  } catch (err) {
    // localStorage unavailable -- nothing to clear.
  }
  show();
}

init();
