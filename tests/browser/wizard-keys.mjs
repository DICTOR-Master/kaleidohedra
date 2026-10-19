// No raw text keys in the DICTO wizard (DICTO 2026-10-16 audit: rows showed `wiz.3d.ocdStella` and the like). Both doors, all 7
// languages, every dimension opened: no row label or description may be a bare key such as `wiz.3d.cycles`.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const LANGS = ['en', 'ja', 'es', 'fr', 'ko', 'zh', 'ru'];
const b = await chromium.launch();
const raw = new Set(); const errors = [];
for (const site of ['kaleidohedra', 'rhombiverse']) for (const lang of LANGS) {
  const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.addInitScript((l) => { try { localStorage.setItem('rhombiverse-settings', JSON.stringify({ language: l })); } catch {} }, lang);
  await page.goto(`${BASE}/index.html?site=${site}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  const dims = await page.evaluate(() => [...document.querySelectorAll('.dim-wizard-card-btn[data-dim]')].map((e) => e.dataset.dim).filter((d) => !/5D|6D/.test(d)));
  const collect = async (dim) => (await page.evaluate(() => [...document.querySelectorAll('.dim-wizard-overlay .dim-wizard-desc, .dim-wizard-overlay .dim-wizard-label')]
    .map((e) => e.textContent.trim()).filter((s) => /^[a-z][A-Za-z0-9]*(\.[A-Za-z0-9@]+){2,}$/.test(s)))).forEach((k) => raw.add(`${site} ${lang} ${dim}: ${k}`));
  await collect('start'); // whatever opens first; tapping it again below closes it, so it is read here
  // on the Rhombiverse door 3D+ leaves the wizard straight for fcc (2026-10-20), so it is opened last there
  if (site === 'rhombiverse') dims.sort((x, y) => (x === '3D') - (y === '3D'));
  for (const dim of dims) { await page.tap(`.dim-wizard-card-btn[data-dim="${dim}"]`); await page.waitForTimeout(300); await collect(dim); }
  await page.close();
}
await b.close();
console.log([...raw].join('\n') || 'no raw keys');
assert.deepEqual([...raw], [], 'raw keys shown'); assert.deepEqual(errors, []);
console.log('wizard keys: ok');
