// X-ray's icosahedral axes (DICTO 2026-10-15): through the real UI on an iPad, each world's X-ray menu offers the 5-, 3- and 2-fold
// axes only when the scene has 5-fold symmetry, in the right frame (Karma and Dharma (0, φ, 1), Bodhi (0, 1, φ)). Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp';
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
async function open(action) {
  if (!(await page.locator('.dim-wizard-overlay.open').count())) { await page.tap('#hud-wizard-cue'); await page.waitForSelector('.dim-wizard-overlay.open'); }
  if (!(await page.locator(`[data-action="${action}"]`).count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(500);
  const btn = page.locator(`[data-action="${action}"]`).first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
  await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
  await page.waitForTimeout(2500);
}
const state = () => page.evaluate(() => { const s = document.getElementById('section-axis'); return { frame: s.dataset.icoFrame, shown: [...s.querySelectorAll('option[data-ico]')].filter((o) => !o.hidden).map((o) => o.textContent) }; });
async function xrayOn() { if (!(await page.locator('#xray-toggle.active').count())) await page.tap('#xray-toggle'); await page.waitForTimeout(800); }
for (const [action, frame] of [['tool:chainsWorld:karma', 'b'], ['tool:chainsWorld:dharma', 'b'], ['tool:chainsWorld:bodhi', 'a'], ['tool:icosaWorld', null]]) {
  await open(action); await xrayOn();
  const st = await state(); console.log(action, JSON.stringify(st));
  if (frame) { assert.equal(st.frame, frame, action); assert.deepEqual(st.shown, ['5-fold axis', '3-fold axis', '2-fold axis']); }
  if (st.frame) {
    await page.tap('#lab-toggle'); await page.waitForTimeout(400);
    await page.locator('#section-axis').scrollIntoViewIfNeeded(); await page.selectOption('#section-axis', 'i5'); await page.waitForTimeout(400);
    await page.screenshot({ path: `${SH}/xray-ico-${action.split(':').pop()}-menu.png` });
    await page.tap('#lab-close'); await page.waitForTimeout(600);
    await page.screenshot({ path: `${SH}/xray-ico-${action.split(':').pop()}.png` });
  }
}
// a cubic world: the icosahedral choices stay hidden
await open('tool:octetWorld:pyrochlore'); await xrayOn();
const cub = await state(); console.log('pyrochlore', JSON.stringify(cub)); assert.equal(cub.frame, ''); assert.deepEqual(cub.shown, []);
assert.deepEqual(errors, []);
console.log('xray-ico ok'); await b.close();
