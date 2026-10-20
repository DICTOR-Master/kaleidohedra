// Cleo-Icos & Antonius kits (DICTO 2026-10-14), with the Rhombohedra helper; first lines as the CLEO sphere test, through the real UI on an iPad: DICTO's pieces list Penta-cleo and the pentagonal pocket,
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
const k = page.locator('[data-kit="antonius.block"]').first(); await k.scrollIntoViewIfNeeded(); await k.tap(); await page.waitForTimeout(1500);
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/antonius-kit.png` });
// The purple Rhombohedra helper (DICTO 2026-10-14): a toggle on Cleo-Icos & Antonius kits, tapped on and off.
const cel = page.locator('[data-cells]'); assert.equal(await cel.count(), 1, 'rhombohedra toggle shown');
await cel.tap(); await page.waitForTimeout(500); assert.equal(await page.locator('[data-cells]').getAttribute('aria-pressed'), 'true');
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/antonius-cells.png` });
await page.locator('[data-cells]').tap(); await page.waitForTimeout(300); assert.equal(await page.locator('[data-cells]').getAttribute('aria-pressed'), 'false');
assert.equal(await page.locator('[data-pacioli]').count(), 0, 'no golden rectangles on a non-icosahedron kit');
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('antonius OK');
