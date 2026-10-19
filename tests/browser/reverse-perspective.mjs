// Reverse perspective (DICTO 2026-10-19) through the real UI on an iPad: the projection button cycles 3D → ∥ → ISO → REV; in REV a big
// slider shows in the world's panel (perspective ↔ flat ↔ reverse), changes the picture, and is remembered; back to 3D hides it; no errors.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=upFilm`); await page.waitForTimeout(3000);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(2500); }
const btn = page.locator('#projection-toggle');
for (const want of ['∥', 'ISO', 'REV']) { await btn.tap(); await page.waitForTimeout(500); assert.equal((await btn.textContent()).trim(), want); }
const row = page.locator('#reverse-row');
assert.equal(await row.isVisible(), true, 'slider shown in REV');
assert.ok(await row.evaluate((r) => !!r.closest('.qc-panel.visible')), 'in a visible panel');
const shot = async (n) => { await page.waitForTimeout(800); return page.screenshot({ path: `${SH}/rev-${n}.png` }); };
const input = row.locator('input');
await input.fill('-100'); await input.dispatchEvent('input'); const a = await shot('reverse');
await input.fill('0'); await input.dispatchEvent('input'); const f = await shot('flat');
await input.fill('100'); await input.dispatchEvent('input'); const p = await shot('perspective');
assert.ok(!a.equals(f) && !f.equals(p), 'the picture changes along the slider');
await input.fill('-80'); await input.dispatchEvent('input');
await page.reload(); await page.waitForTimeout(3000);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(2500); }
assert.equal((await btn.textContent()).trim(), 'REV', 'REV remembered');
assert.equal(await page.locator('#reverse-row input').inputValue(), '-80', 'amount remembered');
await btn.tap(); await page.waitForTimeout(500);
assert.equal((await btn.textContent()).trim(), '3D'); assert.equal(await page.locator('#reverse-row').count(), 0, 'slider gone in 3D');
assert.deepEqual(errors, []);
console.log('reverse-perspective ok'); await b.close();
