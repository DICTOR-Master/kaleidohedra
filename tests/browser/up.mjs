// The Universal PiTet world (DICTO 2026-10-19) through the real UI on an iPad, from both doors (SITE=kaleidohedra | rhombiverse): first in
// DICTO's block, opened from the wizard, its views (shells 308, Vajras, hexagonal Cleos, the DICTO OG Family up / down / breaks, the cycle), the endless film's Unwrap / Wrap
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
console.log(SITE, 'first DICTO world:', first); assert.equal(first, 'tool:reuleauxWorld'); // The Reuleaux Platonic Solids is the newest work (#45, 2026-10-21)
const btn = page.locator('[data-action="tool:upWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(2500);
const panel = page.locator('#worldup-panel');
const sel = panel.locator('select[data-select="part"]');
const views = await sel.evaluate((s) => [...s.options].map((o) => o.value + '=' + o.textContent));
console.log('views:', views.join(' | ')); assert.equal(views.length, 7); assert.match(views[0], /^shells=.*308/);
for (const v of ['shells', 'vajras', 'hexcleo', 'ogUp', 'ogDown', 'ogBreakUp', 'ogBreakDown']) { await sel.selectOption(v); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/up-${SITE}-${v}.png` }); }
for (const v of ['ogUp', 'ogDown']) { await sel.selectOption(v); await page.waitForTimeout(700); await panel.locator('.ch-apart-row input').fill('500'); await page.waitForTimeout(800); await page.screenshot({ path: `${SH}/up-${SITE}-${v}-apart.png` }); await panel.locator('.ch-apart-row input').fill('0'); }
await sel.selectOption('shells'); await page.waitForTimeout(600);
await panel.locator('.ch-apart-row input').fill('600'); await page.waitForTimeout(700); await page.screenshot({ path: `${SH}/up-${SITE}-apart.png` });
// the cycle film: its own world on Dual Vision's standard, one tap away
await panel.locator('[data-up-film="open"]').tap(); await page.waitForTimeout(3500);
const fp = page.locator('#worldupfilm-panel');
assert.equal(await fp.isVisible(), true, 'the film world opened');
const unwrap = fp.locator('[data-inf="unwrap"]'), wrap = fp.locator('[data-inf="wrap"]'), pauseBtn = fp.locator('[data-inf-pause]');
assert.equal((await unwrap.textContent()).trim(), '', 'no words on the player');
await page.screenshot({ path: `${SH}/up-${SITE}-film.png` });
await unwrap.tap(); await page.waitForTimeout(3000);
assert.ok(await unwrap.evaluate((b) => b.classList.contains('active')), 'Unwrap running');
await page.screenshot({ path: `${SH}/up-${SITE}-film-run.png` });
await pauseBtn.tap(); await page.waitForTimeout(400);
assert.equal(await fp.locator('.upf-film-row').isVisible(), true, 'scrub slider while paused');
await wrap.tap(); await page.waitForTimeout(1200);
assert.ok(await wrap.evaluate((b) => b.classList.contains('active')), 'Wrap running');
await fp.locator('[data-upf="pieces"]').tap(); await page.waitForTimeout(1200); await page.screenshot({ path: `${SH}/up-${SITE}-film-pieces.png` });
// the Kepler–Poinsot–PiTet Cycle film, from UP's panel
await page.goto(`${BASE}/index.html?site=${SITE}&open=up`); await page.waitForTimeout(3000);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(2500); }
await page.locator('#worldup-panel [data-up-film="kp"]').tap(); await page.waitForTimeout(3500);
const kp = page.locator('#worldkpfilm-panel');
assert.equal(await kp.isVisible(), true, 'the Kepler–Poinsot film opened');
await page.screenshot({ path: `${SH}/up-${SITE}-kp.png` });
await kp.locator('[data-inf="unwrap"]').tap(); await page.waitForTimeout(3000);
assert.ok(await kp.locator('[data-inf="unwrap"]').evaluate((b) => b.classList.contains('active')), 'KP Unwrap running');
await page.screenshot({ path: `${SH}/up-${SITE}-kp-run.png` });
await kp.locator('[data-upf="pieces"]').tap(); await page.waitForTimeout(1500); await page.screenshot({ path: `${SH}/up-${SITE}-kp-pieces.png` });
await kp.locator('[data-upf="negative"]').tap(); await page.waitForTimeout(1500); await page.screenshot({ path: `${SH}/up-${SITE}-kp-negative.png` });
assert.ok(await kp.locator('[data-upf="negative"]').evaluate((b) => b.classList.contains('active')), 'Negative on');
// the DICTO OG Family (#39) link: the paper's View in app button
await page.goto(`${BASE}/index.html?site=${SITE}&open=up:ogUp`); await page.waitForTimeout(3500);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(2500); }
assert.equal(await page.locator('#worldup-panel select[data-select="part"]').inputValue(), 'ogUp', 'OG family opened by link');
await page.screenshot({ path: `${SH}/up-${SITE}-og-family-link.png` });
// links
await page.goto(`${BASE}/index.html?site=${SITE}&open=upFilm`); await page.waitForTimeout(4000);
assert.equal(await page.locator('#worldupfilm-panel').isVisible(), true, 'film opened by link');
assert.deepEqual(errors, []);
console.log('up ok', SITE); await b.close();
