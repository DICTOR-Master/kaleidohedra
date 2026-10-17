// Rhombiverse's Lattice · Select (DICTO 2026-10-17) through the real UI on an iPad: the row shows the lattice you are on (fcc on arrival,
// with its rhombic dodecahedra), Select opens the three blocks (Cubic, Hexagonal, Golden), a station with more inside opens onto its own
// three, a station picks the lattice the way the wizard does, and Done closes. Kaleidohedra's door has no row.
import { chromium, devices } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPad (gen 7) landscape'] }); const page = await ctx.newPage();
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
const row = '#hud-lattice-row', sheet = '#lattice-select', name = () => page.locator(`${row} .lat-name`).textContent();
await page.goto(`${BASE}/index.html?site=rhombiverse`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
// pick fcc's RD from the wizard, as anyone arriving would
const rd = page.locator('[data-action="tool:pieceType:rd"]').first(); await rd.scrollIntoViewIfNeeded(); await rd.tap(); await page.waitForTimeout(900);
assert.equal(await page.locator(row).isVisible(), true, 'row shown in 3D+'); assert.equal(await name(), 'fcc · RD');
await page.screenshot({ path: `${SH}/lat-row.png` });
// Select: three blocks, three stations at most on each line
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(400);
assert.equal(await page.locator(sheet).isVisible(), true, 'sheet open');
assert.match(await page.locator(`${row} .lat-toggle`).textContent(), /Done/);
const blocks = await page.locator(`${sheet} .lat-blk`).count(); assert.equal(blocks, 3, 'three blocks');
for (const id of ['cubic', 'hex', 'golden']) assert.ok((await page.locator(`${sheet} [data-blk="${id}"] .st`).count()) <= 3, `${id}: three at most`);
assert.equal(await page.locator(`${sheet} [data-blk="cubic"] .st.on`).count(), 1, 'fcc lit');
await page.screenshot({ path: `${SH}/lat-sheet.png` });
// bcc has three inside: open it, Back, open it again, pick the truncated octahedra
await page.tap(`${sheet} [data-blk="cubic"] .st[data-i="1"]`); await page.waitForTimeout(300);
assert.deepEqual(await page.locator(`${sheet} [data-blk="cubic"] .st text:not(.kids)`).allTextContents(), ['bcc · TO', 'BCC gaps', 'ED']);
// no station label overlaps its neighbour, in any block
for (const id of ['cubic', 'hex', 'golden']) { const bx = await page.locator(`${sheet} [data-blk="${id}"] .st text:not(.kids)`).evaluateAll((T) => T.map((e) => e.getBoundingClientRect()).map((r) => [r.left, r.right]));
  for (let i = 1; i < bx.length; i++) assert.ok(bx[i][0] >= bx[i - 1][1] - 0.5, `${id}: labels ${i - 1} and ${i} overlap`); }
await page.screenshot({ path: `${SH}/lat-bcc.png` });
await page.tap(`${sheet} [data-blk="cubic"] .lat-back`); await page.waitForTimeout(200);
assert.equal(await page.locator(`${sheet} [data-blk="cubic"] .st`).count(), 3, 'back to the top line');
await page.tap(`${sheet} [data-blk="cubic"] .st[data-i="1"]`); await page.waitForTimeout(200);
await page.tap(`${sheet} [data-blk="cubic"] .st[data-i="0"]`); await page.waitForTimeout(1200);
assert.equal(await page.locator(sheet).isHidden(), true, 'a pick closes the sheet'); assert.equal(await name(), 'bcc · TO');
assert.match(await page.locator('#hud-world-title').textContent(), /BCC/i, 'the wizard pick ran');
// a golden world from its block
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300);
await page.tap(`${sheet} [data-blk="golden"] .st[data-i="0"]`); await page.waitForTimeout(1500);
assert.equal(await name(), 'Golden Rhombohedra'); await page.screenshot({ path: `${SH}/lat-golden.png` });
// Done closes without a pick
await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300); await page.tap(`${row} .lat-toggle`); await page.waitForTimeout(300);
assert.equal(await page.locator(sheet).isHidden(), true, 'Done closes');
// Kaleidohedra's door: no row
await page.goto(`${BASE}/index.html?site=kaleidohedra`); await page.waitForTimeout(1500);
assert.equal(await page.locator(row).count(), 0, 'no row on Kaleidohedra');
assert.deepEqual(errors, []);
console.log('lattice select ok'); await b.close();
