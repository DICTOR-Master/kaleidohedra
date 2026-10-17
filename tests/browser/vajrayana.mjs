// The Vajrayana world (DICTO 2026-10-17) through the real UI on an iPad: opened from the DICTO wizard (top of DICTO's worlds), it opens on
// the twelve-station cycle cut away (⛶ lit); the ∞ film peels and pauses (slider only when paused); Pieces fills the closing steps;
// ⛶ steps wedge → plane → off (glass); the Cleo star link opens Theaetetus on its Cleo star view; no console errors.
import { chromium, devices } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPad (gen 7) landscape'] }); const page = await ctx.newPage();
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
const panel = '#worldvajrayana-panel', note = () => page.locator(`${panel} .vj-note`).textContent();
await page.goto(`${BASE}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World$/.test(a)));
console.log('first DICTO worlds:', worlds.slice(0, 3).join(', ')); assert.equal(worlds[0], 'tool:vajrayanaWorld', 'new work first');
await page.locator('[data-action="tool:vajrayanaWorld"]').first().tap();
await page.waitForFunction(() => /twelve-station/.test(document.querySelector('#worldvajrayana-panel .vj-note')?.textContent ?? ''), null, { timeout: 15000 });
await page.waitForTimeout(900);
assert.match(await page.locator('#hud-world-title').textContent(), /Vajrayana/);
assert.equal(await page.locator('#xray-toggle.active').count(), 1, '⛶ lit: the cutaway');
await page.screenshot({ path: `${SH}/vj-open.png` });
// the film
await page.tap(`${panel} [data-inf="unwrap"]`); await page.waitForTimeout(3200);
assert.equal(await page.locator(`${panel} .inf.run`).count(), 1, 'film runs'); assert.equal(await page.locator(`${panel} .vj-film-row`).isVisible(), false, 'no slider while playing');
await page.screenshot({ path: `${SH}/vj-film.png` });
await page.tap(`${panel} [data-inf-pause]`); await page.waitForTimeout(300);
assert.equal(await page.locator(`${panel} .vj-film-row`).isVisible(), true, 'slider when paused');
await page.locator(`${panel} .vj-film-row input`).fill('450'); await page.waitForTimeout(400); await page.screenshot({ path: `${SH}/vj-scrub.png` });
await page.tap(`${panel} [data-vj="reset"]`); await page.waitForTimeout(800);
// pieces
await page.tap(`${panel} [data-vj="pieces"]`); await page.waitForTimeout(900);
assert.match(await note(), /30 pieces of one kind/); await page.screenshot({ path: `${SH}/vj-pieces.png` });
// ⛶: wedge -> plane -> off (glass)
await page.tap('#xray-toggle'); await page.waitForTimeout(500);
assert.equal(await page.evaluate(() => document.getElementById('section-enable').checked), true, 'plane on');
await page.tap('#xray-toggle'); await page.waitForTimeout(500);
assert.equal(await page.locator('#xray-toggle.active').count(), 0, 'off'); await page.screenshot({ path: `${SH}/vj-glass.png` });
await page.tap('#xray-toggle'); await page.waitForTimeout(500); assert.equal(await page.locator('#xray-toggle.active').count(), 1, 'wedge again');
// the Cleo star build lives in Theaetetus
await page.tap(`${panel} [data-vj="cleo"]`); await page.waitForTimeout(1500);
const ask = await page.locator('#leave-dialog:not([hidden])').count(); if (ask) { await page.tap('#leave-dialog [data-choice="keep"]'); await page.waitForTimeout(1200); }
assert.match(await page.locator('#hud-world-title').textContent(), /Theaetetus/);
const view = await page.evaluate(() => document.querySelector('.qc-panel.visible select')?.value ?? '');
console.log('Theaetetus view:', view); assert.equal(view, 'cleostar');
await page.screenshot({ path: `${SH}/vj-theaetetus.png` });
assert.deepEqual(errors, []);
console.log('vajrayana ok'); await b.close();
