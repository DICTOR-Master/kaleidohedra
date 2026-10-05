// First-run welcome/entry overlay: the Kaleidohedra mark with an ENTER
// button centred on it, links to the sibling sites, legal-doc links.
// Purely a DOM/localStorage concern, independent of render.js/world state.
import { getSettings, onSettingsChange } from './settings.js';
import { t } from './i18n.js';
import { dimensionLabel } from './dimension-label.js';
import { openGuide } from './guide.js';
import { createLanguagePicker } from './language-picker.js';

// The welcome screen shows on every visit (direct decision 2026-09-25:
// the "Don't show this again" opt-out was removed). This is the key that
// opt-out used to store; it's cleared on load so it can't linger.
const LEGACY_SKIP_KEY = 'rhombiverse-skip-intro';

function logoHtml() {
  return `
    <div id="welcome-logo">
      <img src="./assets/brand/kaleidohedra-mark-480.jpg" width="480" height="354" alt="Kaleidohedra logo: a glowing many-coloured polyhedron on a starfield" />
      <button type="button" id="static-enter-label">ENTER</button>
    </div>`;
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

  function show() {
    overlay.style.display = 'flex';
  }
  function hide() {
    overlay.style.display = 'none';
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
