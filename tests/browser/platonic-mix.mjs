// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47) through the real UI on an iPad: first in DICTO's block (newest work),
// opened by the ?open=platonicMix link; all five letters on by default (four slabs D, C, TO, I); tapping letters changes the mix and the
// slabs, the last letter can't be turned off; Helpers hides the connectors and their list; cubes alone hide Helpers and the slider;
// the Spread slider pulls the slabs apart. ?open=platonicMix:DIC opens a mix. No console errors. Screenshot (SHOTS): all five on.
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
assert.equal(worlds[0], 'tool:platonicMixWorld', 'first in DICTO\'s list');
await page.goto(`${BASE}/index.html?site=${SITE}&open=platonicMix&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2500);
const panel = page.locator('#worldplatonicmix-panel');
assert.equal(await panel.isVisible(), true, 'opened by link');
const probe = () => page.evaluate(() => window.__platonicMixProbe());
let st = await probe();
console.log('default', JSON.stringify(st));
assert.equal(st.mix, 'DICTO'); assert.deepEqual(st.slabs, ['D', 'C', 'TO', 'I']);
assert.equal(await panel.locator('[data-pm-world]').count(), 5, 'five letters');
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
// letters: down to the cube alone
for (const w of ['D', 'I', 'T', 'O']) { await panel.locator(`[data-pm-world="${w}"]`).tap(); await page.waitForTimeout(500); }
st = await probe(); assert.equal(st.mix, 'C'); assert.deepEqual(st.slabs, ['C']);
assert.equal(await panel.locator('[data-pm="helpers"]').isVisible(), false, 'no Helpers for cubes alone');
assert.equal(await panel.locator('.pm-spread-row').isVisible(), false, 'no slider for one slab');
await panel.locator('[data-pm-world="C"]').tap(); await page.waitForTimeout(400);
assert.equal((await probe()).mix, 'C', 'the last letter stays');
await panel.locator('[data-pm-world="O"]').tap(); await page.waitForTimeout(500);
st = await probe(); assert.equal(st.mix, 'CO'); assert.deepEqual(st.slabs, ['C', 'TO']);
assert.match(await panel.locator('.pm-helpers').textContent(), /quarter tetrahedron/);
// a mix by link
await page.goto(`${BASE}/index.html?site=${SITE}&open=platonicMix:DIC&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2000);
st = await probe(); assert.equal(st.mix, 'DIC'); assert.deepEqual(st.slabs, ['D', 'C', 'I']);
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('platonic-mix OK', SITE);
