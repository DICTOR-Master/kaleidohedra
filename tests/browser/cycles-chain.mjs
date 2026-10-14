// DICTO Icosahedral Cycles → Star Chain Reaction (DICTO 2026-10-14): at the side step's dodecahedron, the button opens the Sunstar world on
// its Star Chain Reaction view (the branch lives there, one place only).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra&open=cycles`); await page.waitForTimeout(3000);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(1500); }
await page.waitForSelector('#worldcycles-panel.visible');
await page.tap('[data-cy-loop="3"]'); await page.waitForTimeout(400);
await page.evaluate(() => { const i = document.querySelector('#worldcycles-panel .cy-slider'); i.value = '200'; i.dispatchEvent(new Event('input')); });
await page.waitForTimeout(400);
await page.tap('[data-cy-chain]'); await page.waitForTimeout(2500);
if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="keep"]'); await page.waitForTimeout(1500); }
const sun = await page.isVisible('#worldsunstar-panel'); const txt = sun ? await page.evaluate(() => { const s = document.querySelector('#worldsunstar-panel select'); return s ? s.options[s.selectedIndex].text : ''; }) : '';
console.log('sunstar panel', sun, txt.replace(/\s+/g, ' ').slice(0, 160));
assert.ok(sun, 'Sunstar world opened'); assert.match(txt, /Star Chain/i);
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/cycles-chain.png` });
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('cycles-chain OK');
