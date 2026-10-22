// DICTO stretched solids (DICTO 2026-10-22; paper #49) through the real UI on an iPad: Studies → DICTO stretched solids; each caps
// choice and (with 2 caps) each direction draws the hull with the paper's face count at spacing 1; the direction hides with 3 or 4
// caps; the slider moves the spacing and the readout says equal-edged at 1, telescoped elsewhere. Screenshot (SHOTS): 4 caps at 1.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=studies&probe`); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForTimeout(2000);
const panel = page.locator('#worldstudies-panel');
await panel.locator('[data-select="study"]').selectOption('stretch'); await page.waitForTimeout(800);
const probe = () => page.evaluate(() => window.__studiesProbe());
let st = await probe(); assert.equal(st.study, 'stretch'); assert.equal(st.spacing, 1);
assert.match(await panel.locator('[data-select="study"] option:checked').textContent(), /DICTO stretched solids/);
assert.match(await panel.locator('.st-slider-val').textContent(), /equal-edged/);
const DIRS = { cube: 14, face: 22, body: 24, five: 22 };
for (const [d, n] of Object.entries(DIRS)) {
  await panel.locator(`[data-st-dir="${d}"]`).tap(); await page.waitForTimeout(500);
  st = await probe(); assert.equal(st.direction, d); assert.equal(st.faces, n, `${d}: ${n} faces`);
}
for (const [c, n] of [[3, 29], [4, 34]]) {
  await panel.locator(`[data-st-caps="${c}"]`).tap(); await page.waitForTimeout(500);
  st = await probe(); assert.equal(st.caps, c); assert.equal(st.faces, n, `${c} caps: ${n} faces`);
  assert.equal(await panel.locator('.st-dirs').isVisible(), false, 'no direction with 3 or 4 caps');
}
await panel.locator('[data-study-shear]').tap(); await page.waitForTimeout(600); // one solid, not copies on the lattice
await page.screenshot({ path: `${SH}/stretch-studies.png` });
await panel.locator('.st-slider').fill('1700'); await page.waitForTimeout(500);
st = await probe(); assert.ok(Math.abs(st.spacing - 1.7) < 1e-9, 'the slider moves'); assert.equal(st.faces, 34, 'same faces telescoped');
assert.match(await panel.locator('.st-slider-val').textContent(), /telescoped/);
await panel.locator('[data-st-caps="2"]').tap(); await page.waitForTimeout(400);
assert.equal(await panel.locator('.st-dirs').isVisible(), true, 'direction back with 2 caps');
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('stretch-studies OK');
