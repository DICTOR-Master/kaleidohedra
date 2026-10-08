// In-app User Guide: renders site/<app>/guide.md (the same file
// guide.html serves as the shareable /guide page) in a full-screen
// overlay. English only for now -- the guide itself isn't translated.
import { renderMarkdown, GUIDE_CSS } from './markdown.js';
import { getSettings, onSettingsChange } from './settings.js';
import { t } from './i18n.js';
import { createLanguagePicker } from './language-picker.js';
import { SITE, SITES } from './site.js';

// site/<app>/guide.md is English; each other language has guide.<lang>.md beside it.
// A missing translation falls back to English.
export function guideUrl(lang) {
  // Each app's own guide, in its site folder (site/<app>/guide.md, guide.<lang>.md).
  return lang === 'en' ? `./site/${SITE}/guide.md` : `./site/${SITE}/guide.${lang}.md`;
}

let overlay = null;
let loadedLang = null;

function loadGuide(lang) {
  loadedLang = lang;
  const body = overlay.querySelector('.md-guide');
  const share = overlay.querySelector('#guide-share');
  share.href = lang === 'en' ? './guide.html' : `./guide.html?lang=${lang}`;
  share.innerHTML = t('guide.openPage', lang);
  overlay.querySelector('#guide-close').title = t('guide.close', lang);
  overlay.setAttribute('lang', lang);
  body.textContent = t('guide.loading', lang);
  const get = (url) => fetch(url).then((r) => (r.ok ? r.text() : Promise.reject(new Error(`HTTP ${r.status}`))));
  get(guideUrl(lang))
    .catch(() => (lang === 'en' ? Promise.reject(new Error('no guide')) : get(guideUrl('en'))))
    .then((md) => { if (loadedLang === lang) body.innerHTML = renderMarkdown(md); })
    .catch((err) => {
      console.warn(`${SITES[SITE].name}: failed to load guide`, err);
      if (loadedLang === lang) body.textContent = t('guide.failed', lang);
    });
}

function build() {
  const style = document.createElement('style');
  style.textContent = `${GUIDE_CSS}
#guide-overlay { position: fixed; inset: 0; z-index: 1100; display: none; flex-direction: column; background: #0a0c14; }
#guide-overlay.open { display: flex; }
#guide-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; padding: 10px 16px; border-bottom: 1px solid #2c3444; font: var(--text-m) var(--font-ui); }
#guide-bar a { color: var(--accent); }
#guide-bar .lang-picker { margin-left: auto; }
#guide-close { min-width: 44px; min-height: var(--touch); background: none; border: 1px solid rgba(var(--accent-rgb), 0.35); border-radius: var(--radius-m); color: #ddd; font-size: var(--text-xl); cursor: pointer; }
#guide-body { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 20px 16px 48px; }`;
  document.head.appendChild(style);

  overlay = document.createElement('div');
  overlay.id = 'guide-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-label', `${SITES[SITE].name} User Guide`);
  overlay.innerHTML = `
    <div id="guide-bar">
      <button id="guide-close" type="button" title="Close (Esc)" aria-label="Close">✕</button>
      <a id="guide-share" target="_blank" rel="noopener"></a>
    </div>
    <div id="guide-body"><div class="md-guide">Loading…</div></div>`;
  document.body.appendChild(overlay);

  overlay.querySelector('#guide-close').addEventListener('click', closeGuide);
  // In-page #anchor links scroll inside the overlay instead of touching
  // location.hash, which the app itself uses for share links.
  overlay.querySelector('#guide-body').addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    e.preventDefault();
    overlay.querySelector(`[id="${CSS.escape(a.getAttribute('href').slice(1))}"]`)?.scrollIntoView({ behavior: 'smooth' });
  });
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('open')) {
      e.stopPropagation();
      closeGuide();
    }
  }, true);

  overlay.querySelector('#guide-bar').appendChild(createLanguagePicker());
  loadGuide(getSettings().language);
  onSettingsChange((s) => { if (s.language !== loadedLang) loadGuide(s.language); });
}

export function openGuide() {
  if (!overlay) build();
  overlay.classList.add('open');
  overlay.querySelector('#guide-body').scrollTop = 0;
}

export function closeGuide() {
  overlay?.classList.remove('open');
}
