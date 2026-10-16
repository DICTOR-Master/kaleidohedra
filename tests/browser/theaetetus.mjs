// The Theaetetus world (DICTO 2026-10-15) through the real UI on an iPad: opened from the DICTO wizard, its three views (102 clean pieces, 215-piece stations, the Cleo star), the X-ray
// icosahedral axes offered, Pull apart, the ?open= link; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
await page.goto(`${BASE}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:theaetetusWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const firstDicto = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World/.test(a)).slice(0, 3));
console.log('first DICTO worlds:', firstDicto.join(', '));
const btn = page.locator('[data-action="tool:theaetetusWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(2000);
const sel = page.locator('select.hull-select[data-select="part"]:visible').first();
const views = await sel.evaluate((s) => [...s.options].map((o) => o.value + '=' + o.textContent));
console.log('views:', views.join(' | ')); assert.equal(views.length, 3); assert.match(views[0], /^c102=102/); assert.match(views[1], /^stations=/); assert.match(views[2], /^cleostar=The Cleo star.*82/);
for (const v of ['c102', 'stations', 'cleostar']) { await sel.selectOption(v); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/theaetetus-${v}.png` }); }

assert.equal(await page.locator('#xray-toggle').isHidden(), false, 'X-ray offered (shell world)');
await page.tap('#xray-toggle'); await page.waitForTimeout(1200);
const frame = await page.evaluate(() => document.getElementById('section-axis').dataset.icoFrame);
console.log('X-ray icosahedral frame:', frame); assert.ok(frame === 'a' || frame === 'b');
await page.tap('#xray-toggle'); await page.waitForTimeout(400);
// ?open= link
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=theaetetus`); await page.waitForTimeout(3500);
assert.ok(await page.locator('select.hull-select[data-select="part"]:visible').count(), 'opened by link');
assert.deepEqual(errors, []);
console.log('theaetetus ok'); await b.close();
