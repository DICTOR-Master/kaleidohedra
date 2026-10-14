// DICTO-TIC's Hypsicles and Golden rectangles paths and Slow play (DICTO 2026-10-14), through the real UI on an iPad: each path's
// stations by the slider, what each step keeps, Build at the stations that have one, Slow toggles and slows Play. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp';
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:cyclesWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const btn = page.locator('[data-action="tool:cyclesWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(400);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForSelector('#worldcycles-panel.visible'); await page.waitForTimeout(1000);
const line = () => page.textContent('#worldcycles-panel .cy-station');
const set = (v) => page.evaluate((v) => { const i = document.querySelector('#worldcycles-panel .cy-slider'); i.value = String(v); i.dispatchEvent(new Event('input')); i.dispatchEvent(new Event('change')); }, v);
const buildShown = () => page.evaluate(() => !document.querySelector('[data-cy-build]').hidden);
console.log('paths:', await page.evaluate(() => [...document.querySelectorAll('[data-cy-loop]')].map((b) => b.textContent).join(' | ')));
await page.tap('[data-cy-loop="6"]'); await page.waitForTimeout(600);
assert.match(await page.textContent('#worldcycles-panel .cy-note'), /Hypsicles/);
for (const [v, name, build] of [[0, 'icosahedron', true], [100, 'The icosahedron as 20 Cleo-Icos', true], [200, 'The dodecahedron as 12 pyramids', false], [300, 'The dodecahedron in the same sphere', true]]) {
  await set(v); await page.waitForTimeout(600); const l = await line(); assert.ok(l.startsWith(name), `${v}: ${l}`); assert.equal(await buildShown(), build, `build at ${v}`);
  await page.screenshot({ path: `${SH}/cycles-hyp-${v}.png` });
}
await set(150); await page.waitForTimeout(400); assert.match(await line(), /one sphere touches every base/); await page.screenshot({ path: `${SH}/cycles-hyp-150.png` });
await page.tap('[data-cy-loop="7"]'); await page.waitForTimeout(600);
assert.equal(await page.evaluate(() => document.querySelector('[data-cy-pacioli]').hidden), true, 'rectangles toggle hidden on the rectangles path');
for (const [v, name] of [[0, 'One golden rectangle'], [100, 'Two golden rectangles'], [200, 'Three golden rectangles, 12 corners'], [300, 'icosahedron']]) {
  await set(v); await page.waitForTimeout(600); const l = await line(); assert.ok(l.startsWith(name), `${v}: ${l}`);
  await page.screenshot({ path: `${SH}/cycles-gr-${v}.png` });
}
await set(250); await page.waitForTimeout(400); assert.match(await line(), /faces fill in/);
// Slow: toggles, and Play advances more slowly with it on
await page.tap('[data-cy-slow]'); assert.equal(await page.getAttribute('[data-cy-slow]', 'aria-pressed'), 'true');
await page.tap('[data-cy-play]'); await page.waitForTimeout(9000);
const slowAt = await page.evaluate(() => Number(document.querySelector('#worldcycles-panel .cy-slider').value));
await page.tap('[data-cy-play]');
await page.tap('[data-cy-slow]'); assert.equal(await page.getAttribute('[data-cy-slow]', 'aria-pressed'), 'false');
await page.tap('[data-cy-play]'); await page.waitForTimeout(9000);
const fastAt = await page.evaluate(() => Number(document.querySelector('#worldcycles-panel .cy-slider').value));
await page.tap('[data-cy-play]');
console.log('after 9 s of play: slow', slowAt, 'normal', fastAt); assert.ok(fastAt > slowAt, 'slow is slower');
assert.deepEqual(errors, []);
console.log('cycles-hyp ok'); await b.close();
