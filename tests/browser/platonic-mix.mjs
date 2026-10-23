// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47) through the real UI on an iPad: first in DICTO's block (newest work),
// opened by the ?open=platonicMix link. It starts empty (a hint, no Helpers, no list, no slider); tapping letters adds layers in the
// stack order D, C, T/O, I, each dropping into place; T and O share one layer; a lit letter takes its layer out, down to empty again.
// Helpers hides the connectors and their list; the Spread slider pulls the slabs apart. Build it yourself: a new layer comes as ghosts,
// tapping one on the canvas places it, ↶ takes it back, Fill the rest places them all. ?open=platonicMix:DIC opens those layers whole.
// No console errors. Screenshots (SHOTS): all five whole; mid-build (D and I layers, a few pieces placed).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('dialog', (d) => d.accept());
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000', SITE = process.env.SITE ?? 'kaleidohedra';
await page.goto(`${BASE}/index.html?site=${SITE}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:platonicMixWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World$/.test(a)));
assert.equal(worlds[0], 'tool:dictonicWorld', 'DICTONIC first (2026-10-23)'); assert.equal(worlds[1], 'tool:platonicMixWorld', 'then Every Mix in DICTO\'s list');
await page.goto(`${BASE}/index.html?site=${SITE}&open=platonicMix&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2500);
const panel = page.locator('#worldplatonicmix-panel');
assert.equal(await panel.isVisible(), true, 'opened by link');
const probe = () => page.evaluate(() => window.__platonicMixProbe());
const letter = async (w) => { await panel.locator(`[data-pm-world="${w}"]`).tap(); await page.waitForTimeout(800); };
let st = await probe();
assert.equal(st.mix, ''); assert.deepEqual(st.slabs, [], 'starts empty');
assert.match(await panel.locator('.pm-note').textContent(), /Tap a letter to add its layer/);
for (const sel of ['[data-pm="helpers"]', '.pm-helpers', '.pm-spread-row', '[data-pm="fill"]']) assert.equal(await panel.locator(sel).isVisible(), false, `empty: no ${sel}`);
// add layers out of order: they stack D, C, TO, I
await letter('I'); st = await probe(); assert.deepEqual(st.slabs, ['I']);
await panel.locator(`[data-pm-world="D"]`).tap(); await page.waitForTimeout(80);
assert.equal((await probe()).animating, true, 'the new layer drops in');
await page.waitForTimeout(800);
st = await probe(); assert.deepEqual(st.slabs, ['D', 'I']); assert.equal(st.animating, false); assert.ok(st.slabY[0] < st.slabY[1], 'D below I');
await letter('O'); await letter('C');
st = await probe(); assert.deepEqual(st.slabs, ['D', 'C', 'TO', 'I']); assert.ok(st.shownKinds.includes('Q'), 'O without T: quarter tetrahedra');
await letter('T');
st = await probe(); assert.equal(st.mix, 'DICTO'); assert.deepEqual(st.slabs, ['D', 'C', 'TO', 'I'], 'T joins the octet layer');
assert.ok(st.shownKinds.includes('T') && !st.shownKinds.includes('Q'), 'tetrahedra whole');
assert.match(await panel.locator('.pm-helpers').textContent(), /Admiral Cap/);
await page.screenshot({ path: `${SH}/platonic-mix-dicto.png` });
// Helpers off: only the solids
await panel.locator('[data-pm="helpers"]').tap(); await page.waitForTimeout(400);
st = await probe(); assert.equal(st.helpers, false); assert.deepEqual(st.shownKinds.sort(), ['C', 'D', 'I', 'O', 'T'], 'only the solids');
assert.equal(await panel.locator('.pm-helpers').isVisible(), false, 'no list with helpers off');
await panel.locator('[data-pm="helpers"]').tap(); await page.waitForTimeout(400);
// spread
const row = panel.locator('.pm-spread-row input');
await row.fill('100'); await page.waitForTimeout(300);
st = await probe(); const gaps = st.slabY.slice(1).map((y, i) => y - st.slabY[i]); assert.ok(gaps.every((g) => g > 1), 'pulled apart');
await row.fill('0'); await page.waitForTimeout(300);
// lit letters take their layers out, down to empty
for (const w of ['D', 'I', 'C', 'T']) await letter(w);
st = await probe(); assert.equal(st.mix, 'O'); assert.deepEqual(st.slabs, ['TO']);
assert.equal(await panel.locator('.pm-spread-row').isVisible(), false, 'no slider for one slab');
await letter('O'); st = await probe(); assert.equal(st.mix, ''); assert.deepEqual(st.slabs, [], 'empty again');
// Build it yourself: D and I as ghosts, tap to place
await panel.locator('[data-pm="build"]').tap(); await page.waitForTimeout(400);
await letter('D'); await letter('I');
st = await probe(); assert.equal(st.build, true); assert.equal(st.placed, 0); assert.ok(st.ghosts > 100, 'ghosts');
assert.equal(await panel.locator('[data-pm="fill"]').isVisible(), true, 'Fill the rest');
// tap the ghost nearest the eye; if a placed piece is in front of it (the tap names that piece), try the next nearest
for (let n = 1; n <= 6; n++) {
  for (let k = 0; k < 12 && (await probe()).placed < n; k++) {
    const at = await page.evaluate((k) => window.__platonicMixGhostAt(k), k);
    await page.touchscreen.tap(at.x, at.y); await page.waitForTimeout(500);
  }
  st = await probe(); assert.equal(st.placed, n, `a tap places piece ${n}`);
}
console.log('mid-build', JSON.stringify({ placed: st.placed, total: st.total }), await panel.locator('.pm-note').textContent());
await page.screenshot({ path: `${SH}/platonic-mix-build.png` });
await page.tap('#undo-btn'); await page.waitForTimeout(500);
assert.equal((await probe()).placed, 5, '↶ takes the last piece back');
await panel.locator('[data-pm="fill"]').tap(); await page.waitForTimeout(600);
st = await probe(); assert.equal(st.ghosts, 0); assert.equal(st.placed, st.total, 'all placed');
assert.equal(await panel.locator('[data-pm="fill"]').isVisible(), false, 'nothing left to fill');
// a mix by link
await page.goto(`${BASE}/index.html?site=${SITE}&open=platonicMix:DIC&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2000);
// the build above is saved: asked first (fresh-start.mjs); Continue
assert.equal(await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count(), 1, 'asked about the saved build');
await page.tap('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(400);
st = await probe(); assert.equal(st.mix, 'DIC'); assert.deepEqual(st.slabs, ['D', 'C', 'I']); assert.equal(st.build, false); assert.equal(st.ghosts, 0);
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('platonic-mix OK', SITE);
