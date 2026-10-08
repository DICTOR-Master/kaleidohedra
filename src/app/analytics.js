// Counting (DICTO, 2026-10-08: "I have to get a count of DICTO being clicked"): every opening of the
// DICTO wizard is counted as a visit to /dicto, alongside ordinary page views, through Vercel Web
// Analytics: totals only, no cookies, nothing that identifies anyone (PRIVACY.md says so). Only on the
// live sites (*.vercel.app); locally and in tests nothing loads.
const LIVE = typeof location !== 'undefined' && location.hostname.endsWith('.vercel.app');

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
