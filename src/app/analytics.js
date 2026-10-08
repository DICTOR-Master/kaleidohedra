// Counting (DICTO, 2026-10-08: "I have to get a count of DICTO being clicked"): every opening of the
// DICTO wizard is counted as a visit to /dicto, alongside ordinary page views, through Vercel Web
// Analytics: totals only, no cookies, nothing that identifies anyone (PRIVACY.md says so). Only on the
// live sites (*.vercel.app); locally and in tests nothing loads.
import { SITE, SITES } from './site.js';

// Only where Web Analytics is switched on in that site's Vercel project (site.js: analytics): with
// it off, Vercel serves no script and loading one would log an error for every visitor.
const LIVE = typeof location !== 'undefined' && location.hostname.endsWith('.vercel.app') && SITES[SITE].analytics === true;

if (LIVE) {
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  const s = document.createElement('script');
  s.defer = true;
  s.src = '/_vercel/insights/script.js';
  document.head.appendChild(s);
}

/** One more opening of the DICTO wizard. */
export function countDicto() {
  if (LIVE) window.va('pageview', { route: '/dicto', path: '/dicto' });
}
