// The OCD Stella Crystals world (DICTO 2026-10-16) through the real UI on an iPad: opened from the DICTO wizard (first of DICTO's worlds),
// the preset (icosahedra, 84.60%), the partner swapped to octahedra (96.33%) and to OCD Stellas by themselves (87.12%), Grow, X-ray offered,
// Gap pieces (offered with icosahedra, hidden with octahedra) and Notches (octahedra only), a tapped solid named, Reset, and the
// ?open=ocdStella:octa link; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const panel = '#worldocdstella-panel';
const note = () => page.locator(`${panel} .os-note`).textContent();
const shown = (k) => page.locator(`${panel} [data-os="${k}"]`).isVisible();
await page.goto(`${BASE}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:ocdStellaWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World/.test(a)));
console.log('first DICTO worlds:', worlds.slice(0, 3).join(', '));
assert.equal(worlds.filter((a) => a === 'tool:ocdStellaWorld').length, 1, 'listed once');
const btn = page.locator('[data-action="tool:ocdStellaWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForFunction(() => /84\.60%/.test(document.querySelector('#worldocdstella-panel .os-note')?.textContent ?? ''), null, { timeout: 15000 });
console.log('preset:', await note()); assert.match(await note(), /Fd-3/);
assert.ok(await shown('gap'), 'gap offered with icosahedra'); assert.ok(!(await shown('notch')), 'notches hidden with icosahedra');
await page.screenshot({ path: `${SH}/os-ico.png` });
// a solid named by a tap at the centre
const box = await page.locator('canvas').first().boundingBox();
await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height * 0.42); await page.waitForTimeout(600);
const hud = await page.evaluate(() => [...document.querySelectorAll('body *')].map((e) => e.childElementCount ? '' : e.textContent).find((s) => /OCD Stella:|Icosahedron of|Regular octahedron/.test(s)) ?? '');
console.log('tapped:', hud); assert.ok(hud, 'a solid named');
// gap pieces
await page.tap(`${panel} [data-os="gap"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/os-gap.png` });
// octahedra
await page.tap(`${panel} [data-os-partner="octa"]`); await page.waitForTimeout(900);
assert.match(await note(), /96\.33%/); assert.ok(!(await shown('gap')), 'gap hidden with octahedra'); assert.ok(await shown('notch'), 'notches offered');
await page.screenshot({ path: `${SH}/os-octa.png` });
await page.tap(`${panel} [data-os="notch"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/os-notch.png` });
// alone
await page.tap(`${panel} [data-os-partner="alone"]`); await page.waitForTimeout(900);
assert.match(await note(), /87\.12%/); assert.match(await note(), /Im-3/);
// grow; the app's X-ray offered here
const grow = page.locator(`${panel} .os-grow-row input`);
await grow.fill('4'); await grow.dispatchEvent('change'); await page.waitForTimeout(900);
assert.match(await page.locator(`${panel} .os-grow-label`).textContent(), /4 joint steps/);
assert.ok(await page.locator('#xray-toggle').isVisible(), 'X-ray offered'); await page.screenshot({ path: `${SH}/os-grow.png` });
// reset
await page.tap(`${panel} [data-os="reset"]`); await page.waitForTimeout(900);
assert.match(await note(), /84\.60%/); assert.ok(!(await page.locator(`${panel} [data-os="reset"]`).isVisible()), 'reset hidden at the preset');
// the link
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=ocdStella:octa`);
await page.waitForFunction(() => /96\.33%/.test(document.querySelector('#worldocdstella-panel .os-note')?.textContent ?? ''), null, { timeout: 20000 });
console.log('link: octahedra');
assert.deepEqual(errors, []); console.log('OCD Stella Crystals: ok'); await b.close();
