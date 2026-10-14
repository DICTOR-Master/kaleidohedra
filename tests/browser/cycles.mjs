// DICTO Icosahedral Cycles (DICTO 2026-10-14), through the real UI on an iPad: listed once in 3D+, opens on Loop 1 at the icosahedron,
// the slider moves through the four solids on the same 12 corners (with what each step keeps), the loop switch goes to the Dharma
// movie, whose slider ends on the icosahedron φ³ larger. Screenshots of each station.
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
const order = await page.evaluate(() => [...document.querySelectorAll('.dim-wizard-overlay [data-action]')].map((e) => e.dataset.action));
assert.equal(order.filter((a) => a === 'tool:cyclesWorld').length, 1, 'listed once');
const btn = page.locator('[data-action="tool:cyclesWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(400);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForSelector('#worldcycles-panel.visible'); await page.waitForTimeout(1000);
if ((await page.getAttribute('[data-cy-loop="1"]', 'aria-pressed')) !== 'true') { await page.tap('[data-cy-loop="1"]'); await page.waitForTimeout(500); }
const line = () => page.textContent('#worldcycles-panel .cy-station');
const set = (v) => page.evaluate((v) => { const i = document.querySelector('#worldcycles-panel .cy-slider'); i.value = String(v); i.dispatchEvent(new Event('input')); i.dispatchEvent(new Event('change')); }, v);
const seen = [];
for (const [v, name] of [[0, 'icosahedron'], [100, 'great dodecahedron'], [200, 'small stellated dodecahedron'], [300, 'great icosahedron'], [400, 'icosahedron']]) {
  await set(v); await page.waitForTimeout(500); const l = await line(); seen.push(l); assert.ok(l.startsWith(name), `${v}: ${l}`);
  await page.screenshot({ path: `${SH}/cycles-l1-${v}.png` });
}
await set(150); await page.waitForTimeout(400); const mid = await line(); console.log('between:', mid); assert.match(mid, /keeps the 12 face planes/);
await set(350); await page.waitForTimeout(400); assert.match(await line(), /keeps only the 12 corners/);
console.log('loop 1:', seen.join(' | '));
await page.tap('[data-cy-loop="2"]'); await page.waitForTimeout(800);
console.log('loop 2 start:', await line()); assert.match(await line(), /1 of 237 pieces · icosahedron/);
await set(115); await page.waitForTimeout(600); console.log('115:', await line()); assert.match(await line(), /Hecatodihedron/);
await page.screenshot({ path: `${SH}/cycles-l2-115.png` });
await set(237); await page.waitForTimeout(800); console.log('end:', await line()); assert.match(await line(), /φ³ larger/);
await page.screenshot({ path: `${SH}/cycles-l2-237.png` });
const box = await page.locator('#worldcycles-panel .cy-slider').boundingBox();
console.log('slider', Math.round(box.width), 'x', Math.round(box.height));
// The side step: icosahedron → dual compound → dodecahedron → great stellated dodecahedron.
await page.tap('[data-cy-loop="3"]'); await page.waitForTimeout(600);
for (const [v, name] of [[0, 'icosahedron'], [100, 'dual compound'], [200, 'dodecahedron'], [300, 'great stellated dodecahedron']]) {
  await set(v); await page.waitForTimeout(500); const l = await line(); assert.ok(l.startsWith(name), `side ${v}: ${l}`);
  await page.screenshot({ path: `${SH}/cycles-l3-${v}.png` });
}
await set(250); await page.waitForTimeout(300); assert.match(await line(), /keeps the 20 corners/);
// The Cleo-Icos path: 20 Cleo-Icos → + 20 Antonius → rhombic hexecontahedron.
await page.tap('[data-cy-loop="4"]'); await page.waitForTimeout(600);
for (const [v, name] of [[0, 'icosahedron of 20 Cleo-Icos'], [100, '+ 20 Antonius'], [200, 'rhombic hexecontahedron']]) {
  await set(v); await page.waitForTimeout(500); const l = await line(); assert.ok(l.startsWith(name), `cleo-icos ${v}: ${l}`);
  await page.screenshot({ path: `${SH}/cycles-l4-${v}.png` });
}
// Golden rectangles on the Cleo-Icos path's rhombic hexecontahedron, on and off
await page.tap('[data-cy-pacioli]'); await page.waitForTimeout(500); assert.equal(await page.getAttribute('[data-cy-pacioli]', 'aria-pressed'), 'true');
await page.screenshot({ path: `${SH}/cycles-l4-pacioli.png` });
await page.tap('[data-cy-pacioli]'); await page.waitForTimeout(300); assert.equal(await page.getAttribute('[data-cy-pacioli]', 'aria-pressed'), 'false');
await page.tap('[data-cy-loop="3"]'); await page.waitForTimeout(400);
// Build: at the great stellated dodecahedron, the button opens its Polyhedraverse kit
await set(300); await page.waitForTimeout(300);
assert.equal(await page.isVisible('[data-cy-build]'), true, 'Build shown at a station');
await page.tap('[data-cy-build]'); await page.waitForTimeout(1500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(800);
const kitRow = await page.textContent('.poly-kit-row').catch(() => '');
console.log('build opened:', kitRow); assert.match(kitRow, /Great stellated dodecahedron/);
await page.screenshot({ path: `${SH}/cycles-build-gsd.png` });
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('cycles OK');
