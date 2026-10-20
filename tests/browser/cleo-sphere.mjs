// The CLEO sphere kits (DICTO 2026-10-14), through the real UI on an iPad: DICTO's pieces list Penta-cleo and the pentagonal pocket,
// the CLEO sphere kits have their own section, and starting a kit places its first Cleo with no errors.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-family="DICTO_PIECES"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
const fam = page.locator('[data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await page.waitForTimeout(800);
const kits = await page.evaluate(() => [...document.querySelectorAll('[data-section="kits-cleo"] [data-kit]')].map((e) => e.dataset.kit));
console.log('CLEO sphere kits:', kits); assert.deepEqual(kits.sort(), ['antonius.block', 'antonius.rhex', 'antonius.rhombohedron', 'cleoSphere', 'cleoSphere.allCleo', 'cleoSphere.icosahedron', 'cleoTowers', 'cleoTowers.three', 'ogAktis']);
const html = await page.evaluate(() => document.querySelector('.dim-wizard-body').textContent);
assert.ok(/Penta-cleo/.test(html), 'Penta-cleo listed'); assert.ok(/Antonius/.test(html) && /Cleo-Icos/.test(html), 'Antonius and Cleo-Icos listed');
const k = page.locator('[data-kit="cleoSphere.icosahedron"]').first(); await k.scrollIntoViewIfNeeded(); await k.tap(); await page.waitForTimeout(1500);
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/cleo-sphere-kit.png` });
// Pacioli's golden rectangles (DICTO 2026-10-14): a toggle on icosahedron kits, tapped on and off.
const pac = page.locator('[data-pacioli]'); assert.equal(await pac.count(), 1, 'golden rectangles toggle shown');
await pac.tap(); await page.waitForTimeout(500); assert.equal(await page.locator('[data-pacioli]').getAttribute('aria-pressed'), 'true');
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/cleo-sphere-pacioli.png` });
await page.locator('[data-pacioli]').tap(); await page.waitForTimeout(300); assert.equal(await page.locator('[data-pacioli]').getAttribute('aria-pressed'), 'false');
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('cleo-sphere OK');
