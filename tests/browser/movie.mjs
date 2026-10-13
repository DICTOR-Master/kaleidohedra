// The build movie (DICTO 2026-10-14), through the real UI on an iPad: Spheres of Dharma built piece by piece, each piece named, the
// named solid shown when its ring completes (the Shields complete the DICTO Truncated-Icosahedral Hecatodihedron); Play runs.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:chainsWorld:dharma"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
const btn = page.locator('[data-action="tool:chainsWorld:dharma"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForSelector('#worldchains-panel.visible'); await page.waitForTimeout(1200);
const set = (n) => page.evaluate((n) => { const i = document.querySelector('#worldchains-panel .ch-film-row input'); i.value = n; i.dispatchEvent(new Event('input')); }, n);
await set(115); await page.waitForTimeout(500);
const note = await page.textContent('#worldchains-panel .ch-film-note');
console.log('at 115:', note);
assert.ok(/Hecatodihedron/.test(note) && /Shield/.test(note), 'the Shields complete the Hecatodihedron');
const worldNote = await page.evaluate(() => document.querySelector('#worldchains-panel .st-note:not(.ch-film-note)').textContent);
console.log('world note:', worldNote); assert.ok(/φ³|Dharma|#23/.test(worldNote), 'the world note stays');
await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/movie-115.png` });
await set(53); await page.waitForTimeout(300); console.log('at 53:', await page.textContent('#worldchains-panel .ch-film-note'));
await set(10); await page.tap('[data-chains-play]'); await page.waitForTimeout(2500);
console.log('playing:', await page.textContent('#worldchains-panel .ch-film-note'), '|', await page.textContent('[data-chains-play]'));
await page.tap('[data-chains-play]');
const box = await page.locator('#worldchains-panel .ch-film-row input').boundingBox();
console.log('film slider', Math.round(box.width), 'x', Math.round(box.height));
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('movie OK');
