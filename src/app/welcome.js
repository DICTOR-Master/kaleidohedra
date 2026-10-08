// First-run welcome/entry overlay: rotating RD logo with a static
// integrated "ENTER" label, legal-doc links. Purely a DOM/localStorage
// concern, independent of render.js/world state.
import { getSettings, onSettingsChange } from './settings.js';
import { t } from './i18n.js';
import { dimensionLabel } from './dimension-label.js';
import { openGuide } from './guide.js';
import { createLanguagePicker } from './language-picker.js';
import { SITE, SITES, storageKey } from './site.js';
import { LOGOS } from './logos.js';

const LEGACY_SKIP_KEY = storageKey('skip-intro');
// The welcome screen is the same for every app; what differs comes from the site table and here.
const LOGO = LOGOS[SITE];
const [W1, W2] = SITES[SITE].wordmark;

// ENTER: history of how this got here, briefly --
//  - Originally a fixed button below the logo; direct feedback
//    2026-08-26 said that read "too similar to the old version," so it
//    became two antipodal faces on the rotating RD itself that lit up
//    (an opalescent glow fill) as they swung toward the viewer.
//  - Entry-flow audit 2026-09-02 found that real: those faces were only
//    clickable while actually facing the viewer, with no visible hint
//    that a plain Enter keypress worked at any time. Fixed by adding a
//    second, large, POSITION-STATIC "ENTER" label centered over the
//    logo -- always visible, always clickable, no facing/timing gate.
//  - Direct follow-up feedback, same day: the swinging opalescent glow
//    faces were no longer needed once the static label became the real
//    entry point, so they're gone entirely now -- the RD just rotates
//    as a plain wireframe logo, and the static label is the only ENTER
//    affordance. This keeps ENTER "on the shape" in spirit (it's
//    centered on the logo, not a separately-positioned button) without
//    any per-face geometry/winding/normal-facing machinery at all.

const LOGO_SCALE = 30; // RD vertices have max norm 2 -- 30 keeps the whole shape inside the viewBox below with margin
// rad/SECOND, not rad/frame -- driven by real elapsed time in startLogoSpin
// below, not a frame counter. This Pi doesn't hold 60fps once render.js's
// own WebGL scene is also live behind the overlay; a fixed rad/frame step
// (the first version of this code) made the spin track actual frame rate
// instead of wall-clock time -- confirmed via a real Playwright probe.
// rad/second keeps the spin's real-world pace correct regardless of how
// many frames the machine actually manages.
const SPIN_SPEED = 0.48; // ~13s/revolution
const PULSE_SPEED = 3.0; // ~2.1s breathing cycle, independent of spin -- an attention cue on the static ENTER label

function rotateX([x, y, z], a) {
  const c = Math.cos(a), s = Math.sin(a);
  return [x, y * c - z * s, y * s + z * c];
}
function rotateY([x, y, z], a) {
  const c = Math.cos(a), s = Math.sin(a);
  return [x * c + z * s, y, -x * s + z * c];
}
function transform(p, angle) { return LOGO.spinFirst ? rotateX(rotateY(p, angle), LOGO.tilt) : rotateY(rotateX(p, LOGO.tilt), angle); }

function logoSvg() {
  const lines = LOGO.edges.map((_, i) => `<line class="rd-edge" data-i="${i}" />`).join('');
  return `
    <svg id="welcome-logo-svg" viewBox="-75 -75 150 150" width="180" height="180" role="img" aria-label="${SITES[SITE].name} logo: ${LOGO.label}. Click ENTER, centered on the logo, to begin.">
      <g style="stroke: var(--accent-strong)" stroke-width="1.5" stroke-linecap="round" fill="none">${lines}</g>
      <!-- Static ENTER label: fixed at the SVG's own center, outside the
           rotating group above, so it never turns or tilts with the RD.
           Always full pointer-events -- clicking it never depends on
           rotation phase. A gentle opacity breathe (driven by pulsePhase
           in startLogoSpin) is the only animation it gets. -->
      <text id="static-enter-label" x="0" y="1" text-anchor="middle" dominant-baseline="central"
            font-family="system-ui, sans-serif" font-weight="800" font-size="19" letter-spacing="1.5"
            fill="#eafcff" style="cursor:pointer"
            stroke="#04141c" stroke-width="2.5" paint-order="stroke">ENTER</text>
    </svg>`;
}

// Recomputed every animation frame while the overlay is visible; started/
// stopped by show()/hide() below rather than left running once dismissed.
// `onEnterHit` fires on a click of the static center label -- always,
// regardless of rotation phase. See the module header for ENTER's history.
function startLogoSpin(onEnterHit) {
  const svg = document.getElementById('welcome-logo-svg');
  if (!svg) return () => {};
  const edgeEls = svg.querySelectorAll('.rd-edge');
  const staticLabel = document.getElementById('static-enter-label');
  let raf = null;
  let angle = 0;
  let pulsePhase = 0;
  let lastT = null;

  function frame(t) {
    // Clamp dt: a tab-switch/GC pause shouldn't make the shape jump --
    // just resume the same real-time pace from wherever it left off.
    const dt = lastT === null ? 0 : Math.min(0.1, (t - lastT) / 1000);
    lastT = t;
    angle += SPIN_SPEED * dt;
    pulsePhase += PULSE_SPEED * dt;

    edgeEls.forEach((el, i) => {
      const [a, b] = LOGO.edges[i];
      const [ax, ay] = transform(a, angle);
      const [bx, by] = transform(b, angle);
      el.setAttribute('x1', ax * LOGO_SCALE);
      el.setAttribute('y1', ay * LOGO_SCALE);
      el.setAttribute('x2', bx * LOGO_SCALE);
      el.setAttribute('y2', by * LOGO_SCALE);
    });

    // Static label: fixed position (set once, never touched here), just
    // a gentle always-substantially-visible breathe for attention --
    // never drops low enough to read as "off", and pointer-events stays
    // 'auto' unconditionally (set once below, not per frame).
    if (staticLabel) staticLabel.setAttribute('fill-opacity', String(0.82 + 0.18 * Math.sin(pulsePhase)));

    raf = requestAnimationFrame(frame);
  }
  const listeners = [];
  if (staticLabel) {
    staticLabel.style.pointerEvents = 'auto';
    const onStaticClick = () => onEnterHit();
    staticLabel.addEventListener('click', onStaticClick);
    listeners.push({ el: staticLabel, onClick: onStaticClick });
  }
  raf = requestAnimationFrame(frame);
  return () => {
    if (raf !== null) cancelAnimationFrame(raf);
    listeners.forEach(({ el, onClick }) => el.removeEventListener('click', onClick));
  };
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
// Each app's quick links: Rhombiverse its dimensions (each opens the DICTO wizard there);
// Kaleidohedra 3D+ and its own worlds, where the shear means something (each straight in).
const QUICK = {
  rhombiverse: ['1D', '2D', '3D', '4D', '5D', '6D'].map((d) => ({ dim: d, label: () => dimensionLabel(d) })),
  kaleidohedra: [
    { dim: '3D', label: () => dimensionLabel('3D') },
    { world: 'tool:roofFoldWorld', label: () => 'EKP' },
    { world: 'tool:targetsWorld', label: () => 'Targets' },
  ],
};
function overviewHtml(lang) {
  return `${t('welcome.overview', lang)}<span class="dim-links">${QUICK[SITE].map((q) => `<button type="button" class="dim-link" ${q.dim ? `data-dim="${q.dim}"` : `data-world="${q.world}"`}>${q.label()}</button>`).join('')}</span>`;
}
function overlayHtml() {
  const lang = getSettings().language;
  return `
    <div id="welcome-card">
      <div class="welcome-lang"></div>
      <h1>${W1}<span>${W2}</span></h1>
      <p class="overview">${overviewHtml(lang)}</p>
      <button type="button" class="how-to-link" id="welcome-how-to" data-i18n-html="welcome.howTo">${t('welcome.howTo', lang)}</button>
      ${SITE === 'rhombiverse' ? `<div class="rhombis-link">
        <img src="./assets/rhombis-favicon-64.png" alt="" width="28" height="28" />
        <a href="./rhombis.html" data-i18n-html="welcome.rhombisLink">${t('welcome.rhombisLink', lang)}</a>
      </div>` : ''}
      ${logoSvg()}
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
    if (e.target.closest('#welcome-how-to')) openGuide();
    const link = e.target.closest('.dim-link');
    if (link) {
      hide();
      if (link.dataset.dim) window.dispatchEvent(new CustomEvent('rhombiverse:open-wizard', { detail: link.dataset.dim }));
      else window.dispatchEvent(new CustomEvent('krp:open-world', { detail: link.dataset.world }));
    }
  });
  onSettingsChange((s) => { const p = overlay.querySelector('.overview'); if (p) p.innerHTML = overviewHtml(s.language); });

  let stopLogoSpin = () => {};

  const aboutBtn = document.createElement('button');
  aboutBtn.id = 'about-btn';
  aboutBtn.type = 'button';
  aboutBtn.title = t('welcome.aboutTitle', getSettings().language);
  aboutBtn.dataset.i18nTitle = 'welcome.aboutTitle';
  aboutBtn.textContent = 'ℹ';
  document.body.appendChild(aboutBtn);

  function show() {
    overlay.style.display = 'flex';
    stopLogoSpin();
    stopLogoSpin = startLogoSpin(enterWorld);
  }
  function hide() {
    overlay.style.display = 'none';
    stopLogoSpin();
  }


  function enterWorld() {
    hide();
  }

  // Keyboard fallback -- the static ENTER label is always clickable, but
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
