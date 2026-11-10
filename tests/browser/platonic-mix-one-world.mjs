// One world view of the Every Mix world, through the real UI (DICTO 2026-11-10): letters D I C T O, then the One world button.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch();
const BASE = process.env.BASE_URL ?? 'http://localhost:8000', out = {};
for (const [name, vp, mobile] of [['ipad', { width: 1024, height: 1366 }, true], ['phone', { width: 390, height: 844 }, true], ['desk', { width: 1280, height: 900 }, false]]) {
  const page = await b.newPage({ viewport: vp, hasTouch: mobile, isMobile: mobile });
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?site=kaleidohedra&open=platonicMix&probe`); await page.waitForTimeout(1500);
  if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
  await page.waitForTimeout(2500);
  const panel = page.locator('#worldplatonicmix-panel');
  for (const w of 'DICTO') { await panel.locator(`[data-pm-world="${w}"]`).click(); await page.waitForTimeout(400); }
  const one = panel.locator('[data-pm="one"]');
  assert.equal(await one.isVisible(), true, 'One world button shown');
  await one.click(); await page.waitForTimeout(1500);
  const st = await page.evaluate(() => window.__platonicMixProbe());
  out[name] = { slabs: st.slabs, kinds: st.shownKinds, note: await panel.locator('.pm-note').textContent(), errors };
  await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/oneworld-${name}.png` });
  await one.click(); await page.waitForTimeout(1200);
  out[name].back = (await page.evaluate(() => window.__platonicMixProbe())).slabs;
}
console.log(JSON.stringify(out, null, 1));
const ok = Object.values(out).every((o) => o.errors.length === 0 && o.slabs.length === 1 && ['JD', 'JI', 'JC', 'JT', 'JO'].every((k) => o.kinds.includes(k)) && o.back.length === 4);
console.log(ok ? 'FINAL ok' : 'FINAL FAIL');
await b.close();
