// Counting (DICTO, 2026-10-08: "I have to get a count of DICTO being clicked"): every opening of the
// DICTO wizard is counted as a visit to /dicto, alongside ordinary page views, through Vercel Web
// Analytics: totals only, no cookies, nothing that identifies anyone (PRIVACY.md says so). Only on the
// live sites (*.vercel.app or *.dictospheres.com); locally and in tests nothing loads.
//
// Configured according to @vercel/analytics v2.0.1 best practices (2024-10-13).
import { SITE, SITES } from './site.js';

// Detect production environment: analytics should run on live sites only
const LIVE = typeof location !== 'undefined' && 
  (location.hostname.endsWith('.vercel.app') || location.hostname.endsWith('.dictospheres.com')) && 
  SITES[SITE].analytics === true;

// Initialize Vercel Web Analytics queue (matches @vercel/analytics inject() implementation)
function initQueue() {
  if (window.va) return;
  window.va = function va(...params) {
    if (!window.vaq) window.vaq = [];
    window.vaq.push(params);
  };
}

// Inject the analytics script (based on @vercel/analytics v2.0.1)
function injectScript() {
  const src = '/_vercel/insights/script.js';
  
  // Check if script is already loaded
  if (document.head.querySelector(`script[src*="${src}"]`)) return;
  
  const script = document.createElement('script');
  script.src = src;
  script.defer = true;
  script.onerror = () => {
    console.log(
      `[Vercel Web Analytics] Failed to load script from ${src}. ` +
      'Be sure to enable Web Analytics for your project and deploy again. ' +
      'See https://vercel.com/docs/analytics/quickstart for more information.'
    );
  };
  document.head.appendChild(script);
}

// Initialize analytics if in production environment
if (LIVE) {
  initQueue();
  injectScript();
}

/** Track a custom pageview event. */
export function pageview({ route, path }) {
  if (LIVE && window.va) {
    window.va('pageview', { route, path });
  }
}

/** Track a custom event. */
export function track(name, properties) {
  if (LIVE && window.va) {
    window.va('event', { name, data: properties });
  }
}

/** One more opening of the DICTO wizard. */
export function countDicto() {
  pageview({ route: '/dicto', path: '/dicto' });
}
