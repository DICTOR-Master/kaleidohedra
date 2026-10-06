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
// dodecahedron (the wheel's geometry, DISCOVERIES.md #5), turning slowly in
// its livery colours. Plain SVG, no second WebGL context.
const ED_FACES = buildWheelFaces();
const LOGO_SCALE = 30;
const LOGO_TILT = 0.42;
const SPIN_SPEED = 0.42; // rad per second
const rotX = ([x, y, z], a) => [x, y * Math.cos(a) - z * Math.sin(a), y * Math.sin(a) + z * Math.cos(a)];
const rotY = ([x, y, z], a) => [x * Math.cos(a) + z * Math.sin(a), y, -x * Math.sin(a) + z * Math.cos(a)];
// Shape upright: its elongation axis (z in the wheel frame) becomes screen-vertical.
const place = ([x, y, z], angle) => rotX(rotY([x, z, -y], angle), LOGO_TILT);
function shade(hex, k) {
  const n = parseInt(hex.slice(1), 16);
  const c = [n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.round(v * k));
  return `rgb(${c.join(',')})`;
}
function drawLogo(svg, angle) {
  const polys = ED_FACES.map((f) => {
    const p = f.verts.map((v) => place(v, angle));
    const c = p.reduce((a, v) => [a[0] + v[0], a[1] + v[1], a[2] + v[2]], [0, 0, 0]).map((v) => v / p.length);
    const len = Math.hypot(...c);
    return { f, p, facing: c[2] / len, depth: c[2] };
  }).filter((q) => q.facing > 0).sort((a, b) => a.depth - b.depth);
  svg.querySelector('g.ed').innerHTML = polys.map(({ f, p, facing }) =>
    `<polygon points="${p.map(([x, y]) => `${(x * LOGO_SCALE).toFixed(1)},${(-y * LOGO_SCALE).toFixed(1)}`).join(' ')}" fill="${shade(f.color, 0.55 + 0.45 * facing)}" />`).join('');
}
function logoHtml() {
  return `
    <div id="welcome-logo">
      <svg id="welcome-logo-svg" viewBox="-75 -75 150 150" role="img" aria-label="Kaleidohedra symbol: the regular-hexagon elongated dodecahedron, turning slowly">
        <g class="ed" stroke="rgba(234, 252, 255, 0.85)" stroke-width="1.2" stroke-linejoin="round"></g>
      </svg>
      <button type="button" id="static-enter-label">ENTER</button>
    </div>`;
}
function startLogoSpin() {
  const svg = document.getElementById('welcome-logo-svg');
  if (!svg) return () => {};
  const still = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  let angle = 0.5, lastT = null, raf = null;
  const frame = (t) => {
    const dt = lastT === null ? 0 : Math.min(0.1, (t - lastT) / 1000);
    lastT = t;
    angle += SPIN_SPEED * dt;
    drawLogo(svg, angle);
    raf = requestAnimationFrame(frame);
  };
  drawLogo(svg, angle);
  if (!still) raf = requestAnimationFrame(frame);
  return () => { if (raf !== null) cancelAnimationFrame(raf); };
}

// Real user feedback (2026-09-10): the welcome card had grown to three
// pieces of "extra info" below the title/logo (the changelog-derived
// tagline, the RHOMBIS cross-link, the Polyhedraverse cross-link) --
// "two bits of extra info [is] enough on welcome." The changelog tagline
// (previously right under the h1, its own loadLatestUpdate() fetch) is
// the one that was cut, in favor of the RHOMBIS link taking that top
// spot instead -- the "What's New" changelog panel (src/app/changelog.js)
// is still the real place for that content, this was always a secondary
// teaser of it.
// The overview line, then every dimension (1D ... 6D) as a button that
// opens the Wizard at that dimension, all on one row of their own
// (direct request: no '&', the row never splitting across lines), named
// as everywhere else (dimensionLabel: 1D+, 2D+, 3D+, 4D, 5D, 6D).
// Redrawn here on a language change (data-i18n would drop the buttons).
const DIMS = ['1D', '2D', '3D', '4D', '5D', '6D'];
function overviewHtml(lang) {
  return `${t('welcome.overview', lang)}<span class="dim-links">${DIMS.map((d) => `<button type="button" class="dim-link" data-dim="${d}">${dimensionLabel(d)}</button>`).join('')}</span>`;
}

function overlayHtml() {
  const lang = getSettings().language;
  return `
    <div id="welcome-card">
      <div class="welcome-lang"></div>
      <h1>Kaleidohedra</h1>
      <p class="overview">${overviewHtml(lang)}</p>
      <button type="button" class="how-to-link" id="welcome-how-to" data-i18n-html="welcome.howTo">${t('welcome.howTo', lang)}</button>
      <div class="rhombis-link">
        <img src="./assets/rhombis-favicon-64.png" alt="" width="28" height="28" />
        <a href="https://rhombiverse.vercel.app/rhombis.html" target="_blank" rel="noopener" data-i18n-html="welcome.rhombisLink">${t('welcome.rhombisLink', lang)}</a>
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
    const dim = e.target.closest('.dim-link')?.dataset.dim;
    if (dim) {
      hide();
      window.dispatchEvent(new CustomEvent('rhombiverse:open-wizard', { detail: dim }));
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
