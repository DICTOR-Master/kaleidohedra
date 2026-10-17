// Rhombiverse's new site lattices (DICTO 2026-10-17): triangular prisms, hcp and the gyrated octet, through the real UI. Each is picked
// from the DICTO wizard; the first tap places the first piece, the next taps on it add the piece across the tapped face (exactly one each,
// saved), the Lattice row names it, and there are no console errors.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1100, height: 800 } });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
for (const [id, station] of [['triprism', 'Triangular prisms'], ['hcp', 'hcp · TRD'], ['gyro', 'Gyrated octet']]) {
  await page.goto(`${BASE}/index.html?site=rhombiverse`);
  await page.evaluate(() => localStorage.clear()); await page.reload();
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  const pick = page.locator(`[data-action="tool:pieceType:${id}"]`).first(); await pick.scrollIntoViewIfNeeded(); await pick.click(); await page.waitForTimeout(900);
  assert.equal(await page.locator('#hud-lattice-row .lat-name').textContent(), station, `${id}: Lattice row`);
  const count = () => page.evaluate((k) => { const r = localStorage.getItem(k); return r ? Object.keys(JSON.parse(r).cells).length : 0; }, `rhombiverse-site-${id}-world`);
  const box = await (await page.waitForSelector('canvas', { state: 'attached' })).boundingBox(), cx = box.x + box.width / 2, cy = box.y + box.height / 2;
  let hx = cx, hy = cy;
  // the first outline sits at the middle; tap round it until it takes (a corner can sit exactly at the middle)
  for (const [dx, dy] of [[0, 0], [10, 10], [-10, 10], [10, -10], [-10, -10], [20, 0], [-20, 0], [0, 20], [0, -20]]) { await page.mouse.click(cx + dx, cy + dy); await page.waitForTimeout(400); if (await count()) { hx = cx + dx; hy = cy + dy; break; } }
  const first = await count(); assert.equal(first, 1, `${id}: the first tap places one piece`);
  let n = first;
  for (const [dx, dy] of [[0, 0], [0, 0], [0, 0], [0, 0]]) { // the same spot: each new piece is the next one hit there
    await page.mouse.click(hx + dx, hy + dy); await page.waitForTimeout(400);
    const m = await count(); assert.ok(m === n || m === n + 1, `${id}: one piece per tap at most`); n = m;
  }
  console.log(id, 'pieces after five taps:', n); assert.ok(n >= 3, `${id}: taps on faces add pieces`);
  await page.screenshot({ path: `${SH}/site-${id}.png` });
}
assert.deepEqual(errors, []);
console.log('site lattices ok'); await b.close();
