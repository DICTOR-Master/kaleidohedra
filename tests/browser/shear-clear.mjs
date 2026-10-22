// Shears are never remembered (DICTO 2026-10-22: "all shears should clear when exiting"), through the real UI on an iPad: shear the
// lattice in a world, go Back and enter it again: unsheared; No shear shows only while sheared and undoes it in one tap; shear
// again and reload: unsheared.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('dialog', (d) => d.accept());
const path = () => page.evaluate(() => window.__shearState().path);
const lattice = '.dicto-dim-content [data-action^="tool:pieceType:"]';
async function enter() {
  if (!(await page.locator('.dim-wizard-overlay.open').count())) await page.tap('#hud-wizard-cue');
  await page.waitForTimeout(400);
  if (!(await page.locator(lattice).count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(400);
  await page.locator(lattice).first().tap(); await page.waitForTimeout(1200);
  if (await page.locator('#leave-dialog:not([hidden]) [data-choice="keep"]').count()) { await page.tap('#leave-dialog [data-choice="keep"]'); await page.waitForTimeout(800); }
}
async function shearIt() {
  if ((await page.getAttribute('#kaleido-toggle', 'aria-expanded')) !== 'true') await page.tap('#kaleido-toggle');
  await page.waitForTimeout(300);
  const max = Number(await page.getAttribute('#kaleido-path', 'max'));
  await page.locator('#kaleido-path').fill(String(max / 2)); await page.waitForTimeout(400);
  const p = await path(); assert.ok(p !== 0, `sheared (${p})`);
}
await page.goto(`${BASE}/index.html?site=kaleidohedra&probe`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
await enter(); assert.equal(await path(), 0, 'starts unsheared');
assert.equal(await page.locator('#kaleido-noshear').isVisible(), false, 'no No shear button when unsheared');
await shearIt();
await page.tap('#hud-world-back'); await page.waitForTimeout(600);
await enter(); assert.equal(await path(), 0, 'left and entered again: unsheared');
await shearIt();
// No shear: one big tap back, shown only while sheared
const noShear = page.locator('#kaleido-noshear');
assert.equal(await noShear.isVisible(), true, 'No shear shows when sheared');
assert.ok((await noShear.boundingBox()).height >= 44, 'big enough for a finger');
await noShear.tap(); await page.waitForTimeout(400);
assert.equal(await path(), 0, 'No shear: unsheared'); assert.equal(await noShear.isVisible(), false, 'hidden when there is none');
await shearIt();
await page.reload(); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(1500);
assert.equal(await path(), 0, 'after a reload: unsheared');
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('shear-clear OK');
