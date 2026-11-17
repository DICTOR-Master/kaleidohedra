// Rhombiverse's Lattice · Select (DICTO 2026-10-17) through the real UI on an iPad: the row shows the lattice you are on (fcc on arrival,
// with its rhombic dodecahedra); Select opens the lattices in the world menu's order (DICTO 2026-11-17: the books' own, then Others'
// lattices and tilings), under neutral headings, the one you are on marked; a station picks the lattice the way the wizard does, and
// Done closes. Kaleidohedra's door has no row.
import { chromium, devices } from 'playwright';
import assert from 'node:assert/strict';
import { unfold } from './menu-unfold.mjs';
import { LATTICE_SECTIONS } from '../../src/app/lattice-select.js';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPad (gen 7) landscape'] }); const page = await ctx.newPage();
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
const row = '#hud-lattice-row', sheet = '#lattice-select', name = () => page.locator(`${row} .lat-name`).textContent();
const pick = async (key) => { const s = page.locator(`${sheet} .lat-st[data-key="${key}"]`); await s.scrollIntoViewIfNeeded(); await s.tap(); await page.waitForTimeout(1500); };
await page.goto(`${BASE}/index.html?site=rhombiverse`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
// pick fcc's RD from the wizard, as anyone arriving would
await unfold(page, 'tool:pieceType:rd'); const rd = page.locator('[data-action="tool:pieceType:rd"]').first(); await rd.scrollIntoViewIfNeeded(); await rd.tap(); await page.waitForTimeout(900);
assert.equal(await page.locator(row).isVisible(), true, 'row shown in 3D+'); assert.equal(await name(), 'fcc · RD');
await page.screenshot({ path: `${SH}/lat-row.png` });
// Select: the menu's sections and order, fcc marked
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(400);
assert.equal(await page.locator(sheet).isVisible(), true, 'sheet open');
assert.match(await page.locator(`${row} .lat-toggle`).textContent(), /Done/);
const shown = await page.evaluate(() => [...document.querySelectorAll('#lattice-select .lat-sec')].map((s) => [s.dataset.sec, [...s.querySelectorAll('.lat-st')].map((e) => e.dataset.key)]));
assert.deepEqual(shown, LATTICE_SECTIONS.map((s) => [s.id, s.items.map((i) => i.key)]), 'the menu\'s order');
assert.deepEqual(await page.locator(`${sheet} .lat-st.on`).evaluateAll((E) => E.map((e) => e.dataset.key)), ['fcc'], 'fcc marked');
await page.screenshot({ path: `${SH}/lat-sheet.png` });
await pick('bcc');
assert.equal(await page.locator(sheet).isHidden(), true, 'a pick closes the sheet'); assert.equal(await name(), 'bcc · TO');
assert.match(await page.locator('#hud-world-title').textContent(), /BCC/i, 'the wizard pick ran');
// a golden world from the others' shelf, and a world of Book One
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300); await pick('golden');
assert.equal(await name(), 'Golden Rhombohedra'); await page.screenshot({ path: `${SH}/lat-golden.png` });
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300); await pick('breathing');
assert.equal(await name(), 'Breathing Pyrochlore');
// Done closes without a pick
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300); await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300);
assert.equal(await page.locator(sheet).isHidden(), true, 'Done closes');
// Kaleidohedra's door: no row
await page.goto(`${BASE}/index.html?site=kaleidohedra`); await page.waitForTimeout(1500);
assert.equal(await page.locator(row).count(), 0, 'no row on Kaleidohedra');
assert.deepEqual(errors, []);
console.log('lattice select ok'); await b.close();
