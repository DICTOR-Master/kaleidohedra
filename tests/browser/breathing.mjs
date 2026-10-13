// Golden Breathing Pyrochlore (DICTO 2026-10-14), through the real UI on an iPad: listed right after the Pyrochlore (3D Kagome)
// lattice, opens on golden, the slider snaps to the named stops, the Kagome layer shows, and a tap adds a cell.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:breathingWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const order = await page.evaluate(() => [...document.querySelectorAll('.dim-wizard-overlay [data-action]')].map((e) => e.dataset.action));
const iPyro = order.indexOf('tool:pieceType:pyrochlore'), iB = order.indexOf('tool:breathingWorld');
console.log('pyrochlore', iPyro, 'breathing', iB, 'times listed', order.filter((a) => a === 'tool:breathingWorld').length);
assert.ok(iB === iPyro + 1, 'right after the Pyrochlore');
assert.equal(order.filter((a) => a === 'tool:breathingWorld').length, 1, 'listed once');
const btn = page.locator('[data-action="tool:breathingWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(400);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForSelector('#worldbreathing-panel.visible'); await page.waitForTimeout(1200);
await page.tap('[data-bp="reset"]'); await page.waitForTimeout(500);
const note = () => page.textContent('#worldbreathing-panel .bp-note');
console.log('opens:', await note()); assert.match(await note(), /1\/φ/);
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/bp-golden.png` });
const before = await note();
let after = before;
for (const [dx, dy] of [[0, 0], [30, -20], [-40, 25], [60, 40], [-60, -50]]) {
  await page.touchscreen.tap(512 + dx, 600 + dy); await page.waitForTimeout(400);
  after = await note(); if (after !== before) break;
}
console.log('tap:', before, '->', after); assert.notEqual(after, before, 'a tap adds a cell');
const set = (v) => page.evaluate((v) => { const i = document.querySelector('#worldbreathing-panel .bp-ratio-row input'); i.value = String(v); i.dispatchEvent(new Event('input')); i.dispatchEvent(new Event('change')); }, v);
await set(510); await page.waitForTimeout(400); console.log('near 1/2:', await note()); assert.match(await note(), /0\.500/);
await set(1000); await page.waitForTimeout(400); console.log('regular:', await note());
await set(618); await page.tap('[data-bp="layer"]'); await page.waitForTimeout(800);
console.log('layer:', await page.textContent('[data-bp="layer"]'));
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/bp-layer.png` });
const box = await page.locator('#worldbreathing-panel .bp-ratio-row input').boundingBox();
console.log('slider', Math.round(box.width), 'x', Math.round(box.height));
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('breathing OK');
