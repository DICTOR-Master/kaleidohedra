// The Universal PiTet world (DICTO 2026-10-19) through the real UI on an iPad, from both doors (SITE=kaleidohedra | rhombiverse): first in
// DICTO's block, opened from the wizard, its four views (shells 308, Vajras, hexagonal Cleos, the cycle), the endless film's Unwrap / Wrap
// toggles (play, pause, the other way), Pull apart, the ?open=up:cycle link; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000', SITE = process.env.SITE ?? 'kaleidohedra';
await page.goto(`${BASE}/index.html?site=${SITE}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:upWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const first = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World/.test(a))[0]);
console.log(SITE, 'first DICTO world:', first); assert.equal(first, 'tool:upWorld');
const btn = page.locator('[data-action="tool:upWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(2500);
const panel = page.locator('#worldup-panel');
const sel = panel.locator('select[data-select="part"]');
const views = await sel.evaluate((s) => [...s.options].map((o) => o.value + '=' + o.textContent));
console.log('views:', views.join(' | ')); assert.equal(views.length, 4); assert.match(views[0], /^shells=.*308/); assert.match(views[3], /^cycle=/);
const film = panel.locator('[data-inf="unwrap"]'), filmIn = panel.locator('[data-inf="wrap"]'), pauseBtn = panel.locator('[data-inf-pause]');
for (const v of ['shells', 'vajras', 'hexcleo']) {
  await sel.selectOption(v); await page.waitForTimeout(900);
  assert.equal(await film.isVisible(), false, `no film player in ${v}`);
  await page.screenshot({ path: `${SH}/up-${SITE}-${v}.png` });
}
// Pull apart on the shells
await sel.selectOption('shells'); await page.waitForTimeout(600);
await panel.locator('.ch-apart-row input').fill('600'); await page.waitForTimeout(700); await page.screenshot({ path: `${SH}/up-${SITE}-apart.png` });
// the cycle and its endless film: DICTO's infinity player (Wrap / Unwrap in the rings, VHS pause)
await sel.selectOption('cycle'); await page.waitForTimeout(1200);
assert.equal(await film.isVisible(), true, 'the infinity player shows in the cycle view');
await page.screenshot({ path: `${SH}/up-${SITE}-cycle.png` });
await film.tap(); await page.waitForTimeout(2500);
assert.ok(await film.evaluate((b) => b.classList.contains('active')), 'Unwrap running');
assert.equal(await pauseBtn.isVisible(), true, 'pause shown while the film is on');
await page.screenshot({ path: `${SH}/up-${SITE}-cycle-unwrap.png` });
await filmIn.tap(); await page.waitForTimeout(1200);
assert.ok(await filmIn.evaluate((b) => b.classList.contains('active')), 'Wrap running');
await pauseBtn.tap(); await page.waitForTimeout(300);
assert.ok(await pauseBtn.evaluate((b) => b.classList.contains('active')), 'paused');
// ?open= link straight to the cycle
await page.goto(`${BASE}/index.html?site=${SITE}&open=up:cycle`); await page.waitForTimeout(4000);
assert.equal(await page.locator('#worldup-panel select[data-select="part"]').inputValue(), 'cycle', 'opened by link on the cycle');
assert.deepEqual(errors, []);
console.log('up ok', SITE); await b.close();
