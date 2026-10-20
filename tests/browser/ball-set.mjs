// The ball set (DICTO 2026-10-20), through the real UI on an iPad: DICTO's pieces list its two kits under Construction sets
// and starting each builds without errors.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const open = async () => {
  await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  if (!(await page.locator('[data-family="DICTO_PIECES"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  const fam = page.locator('[data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await page.waitForTimeout(800);
};
await open();
const kits = await page.evaluate(() => [...document.querySelectorAll('[data-section="kits-sets"] [data-kit]')].map((e) => e.dataset.kit));
for (const k of ['ballSet', 'ballSet.block']) assert.ok(kits.includes(k), `${k} listed under Construction sets (${kits})`);
for (const k of ['ballSet', 'ballSet.block']) {
  if (k !== 'ballSet') await open();
  const card = page.locator(`[data-kit="${k}"]`).first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await page.waitForTimeout(2500);
  await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/kit-${k}.png` });
}
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('ball-set OK');
