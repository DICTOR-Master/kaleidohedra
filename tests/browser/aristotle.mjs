// Aristotle's Pyramid (DICTO 2026-10-21; paper #44) through the real UI on an iPad: in DICTO's block right after the newest work,
// opened by the ?open=aristotle link; the five solids' cards (each split into its face pyramids), the draw-apart slider, the three
// fills, and "Build it yourself" opening the Polyhedraverse kit 'antonius.block'; then the kit's own link ?open=kit:antonius.block.
// No console errors. Screenshots (SHOTS): the pyramids drawn apart, and the golden fix.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('dialog', (d) => d.accept());
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000', SITE = process.env.SITE ?? 'kaleidohedra';
// the wizard lists it second, after The Reuleaux Platonic Solids (#45)
await page.goto(`${BASE}/index.html?site=${SITE}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:aristotleWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World$/.test(a)));
assert.deepEqual(worlds.slice(0, 2), ['tool:reuleauxWorld', 'tool:aristotleWorld'], 'near the top of DICTO\'s list');
// the link
await page.goto(`${BASE}/index.html?site=${SITE}&open=aristotle&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2000);
const panel = page.locator('#worldaristotle-panel');
assert.equal(await panel.isVisible(), true, 'opened by link');
const probe = () => page.evaluate(() => window.__aristotleProbe());
if ((await probe()).mode !== 'pyramids') { await panel.locator('[data-ar-mode="pyramids"]').tap(); await page.waitForTimeout(600); }
assert.equal(await panel.locator('[data-ar-solid]').count(), 5, 'five cards');
assert.equal(await panel.locator('[data-ar="build"]').isVisible(), false, 'no kit button among the pyramids');
const FACES = { cube: 6, tetrahedron: 4, octahedron: 8, dodecahedron: 12, icosahedron: 20 };
for (const k of Object.keys(FACES)) {
  await panel.locator(`[data-ar-solid="${k}"]`).tap(); await page.waitForTimeout(400);
  const st = await probe(); assert.equal(st.solid, k); assert.equal(st.pieces, FACES[k], `${k}: its face pyramids`);
  console.log(k, '-', await panel.locator('.ar-note').textContent());
}
assert.match(await panel.locator('[data-ar-solid="icosahedron"]').textContent(), /Cleo-Icos/, 'the Cleo-Icos named');
await panel.locator('.ar-apart-row input').fill('0'); await page.waitForTimeout(300);
assert.ok((await probe()).offset < 1e-6, 'together');
await panel.locator('.ar-apart-row input').fill('70'); await page.waitForTimeout(500);
assert.ok((await probe()).offset > 0.5, 'drawn apart');
await page.screenshot({ path: `${SH}/aristotle-shot-1.png` });
// Fills
await panel.locator('[data-ar-mode="fills"]').tap(); await page.waitForTimeout(800);
assert.equal(await panel.locator('.ar-apart-row').isVisible(), false, 'no slider in Fills');
const KINDS = { cube: ['cube'], octet: ['octahedron', 'tetrahedron'], golden: ['icosahedron', 'antonius'] };
for (const f of ['cube', 'octet', 'golden']) {
  await panel.locator(`[data-ar-fill="${f}"]`).tap(); await page.waitForTimeout(600);
  const st = await probe(); assert.equal(st.fill, f); assert.deepEqual(st.kinds.sort(), KINDS[f].sort(), `${f}: its pieces`);
  console.log(f, st.pieces, 'pieces -', await panel.locator('.ar-note').textContent());
}
await page.waitForTimeout(600);
await page.screenshot({ path: `${SH}/aristotle-shot-2.png` });
// Build it yourself: the Cleo-Icos & Antonius kit
const build = panel.locator('[data-ar="build"]');
assert.equal(await build.isVisible(), true, 'Build it yourself on the golden fix');
await build.tap(); await page.waitForTimeout(1500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(800);
let kitRow = await page.textContent('.poly-kit-row').catch(() => '');
console.log('build opened:', kitRow); assert.match(kitRow, /Cleo-Icos & Antonius · space filling/);
assert.equal(await panel.isVisible(), false, 'the world closed');
// the kit's own link
await page.goto(`${BASE}/index.html?site=${SITE}&open=kit:antonius.block`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2000);
kitRow = await page.textContent('.poly-kit-row').catch(() => '');
console.log('kit link opened:', kitRow); assert.match(kitRow, /Cleo-Icos & Antonius · space filling/);
assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, 'no wizard over it');
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('aristotle OK', SITE);
