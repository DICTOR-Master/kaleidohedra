// The Almanac's Open (DICTO 2026-10-13), through the real UI: 📖 → an entry → Open lands in its world or
// piece, the world title set, the app space switched, no errors. Assumes the app is served at BASE_URL.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8000';
const DOOR = process.env.DOOR ?? 'kaleidohedra';
// [entry id, the world title expected after Open, the app space]
const CASES = [
  ['dicto:karma', 'Multi-shell chains · Chain of Karma', 'kaleidohedra'],
  ['dicto:atom13', 'DICTO ATOM-13×13 · DICTO Icosa-13 (Lotus seed)', 'kaleidohedra'],
  ['dicto:equalEdge', 'DICTO FCC · DICTO RD', 'kaleidohedra'],
  ['dicto:stretched', 'Studies', 'kaleidohedra'],
  ['dictoPiece:KIT13_ICOSA13_FUJI', 'FUJI', 'polyhedraverse'],
  ['known:bainRd', 'Bain rhombic dodecahedron', 'polyhedraverse'],
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('dialog', (d) => d.accept());
await page.goto(`${BASE_URL}/index.html?site=${DOOR}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 });
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
await page.keyboard.press('Escape'); // the wizard opens on load
await page.waitForTimeout(500);

const ids = await page.evaluate(async () => (await import('./src/app/almanac-data.js')).ALMANAC_ENTRIES.map((e) => e.id));
for (const [id, title, site] of CASES) {
  await page.tap('#almanac-btn');
  await page.waitForSelector('.almanac-overlay.open');
  await page.tap('.almanac-back').catch(() => {}); // it may open on where you are
  const row = page.locator(`.almanac-entry[data-index="${ids.indexOf(id)}"]`);
  await row.scrollIntoViewIfNeeded();
  await row.tap();
  await page.tap('.almanac-open');
  await page.waitForTimeout(2500);
  const got = await page.evaluate(async () => ({
    title: document.getElementById('hud-world-title')?.textContent,
    almanacOpen: document.querySelector('.almanac-overlay')?.classList.contains('open'),
    site: (await import('./src/app/site.js')).activeSite(),
  }));
  console.log(id, JSON.stringify(got));
  assert.equal(got.almanacOpen, false, `${id}: the Almanac should close`);
  assert.equal(got.title, title, `${id}: world title`);
  assert.equal(got.site, site, `${id}: app space`);
  await page.screenshot({ path: `/tmp/almanac-open-${id.replace(/[:]/g, '_')}.png` });
}
console.log(errors.length ? `ERRORS:\n${errors.join('\n')}` : 'no errors');
assert.equal(errors.length, 0);
await browser.close();
console.log('almanac-open OK');
