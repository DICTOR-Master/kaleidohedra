// Counting (DICTO, 2026-10-08: "I have to get a count of DICTO being clicked"): every opening of the
// DICTO wizard is counted as a visit to /dicto, alongside ordinary page views, through Vercel Web
// Analytics: totals only, no cookies, nothing that identifies anyone (PRIVACY.md says so). Only on the
// live sites (*.vercel.app and *.dictospheres.com); locally and in tests nothing loads.
import { inject, track } from '@vercel/analytics';
import { SITE, SITES } from './site.js';

// Only where Web Analytics is switched on in that site's Vercel project (site.js: analytics): with
// it off, Vercel serves no script and loading one would log an error for every visitor.
const LIVE = typeof location !== 'undefined' && 
  (location.hostname.endsWith('.vercel.app') || location.hostname.endsWith('.dictospheres.com')) && 
  SITES[SITE].analytics === true;

if (LIVE) {
  // Initialize Vercel Web Analytics using the official package
  inject({ mode: 'production' });
}

/** One more opening of the DICTO wizard. */
export function countDicto() {
  if (LIVE) track('DICTO Wizard Opened', { route: '/dicto' });
}
