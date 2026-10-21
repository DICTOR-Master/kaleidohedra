// The Reuleaux Platonic Solids (DICTO 2026-10-21; paper #45) through the real UI on an iPad: first in DICTO's block, opened by the
// ?open=reuleaux link; the film (Unwrap plays, pause, scrub), the Balls toggle, each body's card; Build: three pieces placed face to face
// by tapping the real canvas (?probe gives where a face is on screen); no console errors. Screenshots (SHOTS).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000', SITE = process.env.SITE ?? 'kaleidohedra';
// the wizard lists it first
await page.goto(`${BASE}/index.html?site=${SITE}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:reuleauxWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const first = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World$/.test(a))[0]);
assert.equal(first, 'tool:reuleauxWorld', 'new work first');
// the link
await page.goto(`${BASE}/index.html?site=${SITE}&open=reuleaux&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(3000);
const panel = page.locator('#worldreuleaux-panel');
assert.equal(await panel.isVisible(), true, 'opened by link');
const probe = () => page.evaluate(() => window.__reuleauxProbe());
if ((await probe()).mode !== 'film') { await panel.locator('[data-rl-mode="film"]').tap(); await page.waitForTimeout(800); }
assert.equal(await panel.locator('[data-rl-body]').count(), 5, 'five cards');
assert.equal(await panel.locator('.inf-row').isVisible(), true, 'the ∞ player');
await panel.locator('[data-rl-body="octahedron"]').tap(); await page.waitForTimeout(800);
const unwrap = panel.locator('[data-inf="unwrap"]');
await unwrap.tap(); await page.waitForTimeout(3600);
let st = await probe(); console.log('film t', st.t.toFixed(2));
assert.ok(st.t > 2, 'the film plays');
assert.ok(await unwrap.evaluate((x) => x.classList.contains('active')), 'Unwrap running');
await panel.locator('[data-inf-pause]').tap(); await page.waitForTimeout(300);
await panel.locator('.rl-film-row input').fill('1000'); await page.waitForTimeout(600);
st = await probe(); assert.ok(Math.abs(st.t - 10) < 0.01, 'scrubbed'); assert.equal(st.ballsShown, true, 'balls shown');
await page.screenshot({ path: `${SH}/reuleaux-shot-film.png` });
await panel.locator('[data-rl="balls"]').tap(); await page.waitForTimeout(400);
assert.equal((await probe()).ballsShown, false, 'balls hidden');
await panel.locator('[data-rl="balls"]').tap(); await page.waitForTimeout(400);
assert.equal((await probe()).ballsShown, true, 'balls back');
for (const k of ['tetrahedron', 'cube', 'icosahedron', 'dodecahedron']) { await panel.locator(`[data-rl-body="${k}"]`).tap(); await page.waitForTimeout(500); }
// Build: three pieces, each on a face of the last, tapping the canvas where that face is
await panel.locator('[data-rl-body="tetrahedron"]').tap(); await page.waitForTimeout(300);
await panel.locator('[data-rl-mode="build"]').tap(); await page.waitForTimeout(1200);
assert.equal(await panel.locator('.inf-row').isVisible(), false, 'no player in Build');
if ((await probe()).nodes > 1) { await panel.locator('[data-rl="reset"]').tap(); await page.waitForTimeout(800); }
assert.equal((await probe()).nodes, 1, 'the chosen body at the centre');
const pieces = ['tetrahedron', 'tetrahedron', 'octahedron'];
for (let i = 0; i < pieces.length - 1; i++) {
  await panel.locator(`[data-rl-body="${pieces[i + 1]}"]`).tap(); await page.waitForTimeout(400);
  const before = (await probe()).nodes;
  for (const f of (await probe()).screen) {
    await page.touchscreen.tap(f.x, f.y); await page.waitForTimeout(1500);
    if ((await probe()).nodes > before) break;
  }
  assert.equal((await probe()).nodes, before + 1, `piece ${before + 1} placed face to face`);
}
await page.waitForTimeout(800);
console.log('placed:', JSON.stringify((await probe()).placed));
await page.screenshot({ path: `${SH}/reuleaux-shot-build.png` });
// a body that doesn't fit offers the ones that do
await panel.locator('[data-rl-body="cube"]').tap(); await page.waitForTimeout(400);
const n3 = (await probe()).nodes, f0 = (await probe()).screen[0];
await page.touchscreen.tap(f0.x, f0.y); await page.waitForTimeout(1500);
if ((await probe()).nodes === n3 && await panel.locator('.rl-fits').isVisible()) {
  const offered = await panel.locator('[data-rl-fit]').evaluateAll((xs) => xs.map((x) => x.dataset.rlFit));
  console.log('offered:', offered.join(', ')); assert.ok(!offered.includes('cube'), 'only bodies that fit');
}
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('reuleaux OK', SITE);
