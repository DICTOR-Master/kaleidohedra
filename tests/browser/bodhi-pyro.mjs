// Golden Bodhi Pyrochlore Networks (DICTO 2026-10-15) through the real UI on an iPad: opened from the wizard, its four views (one network
// with joints, double network with gap pieces, the five voices, the chorus with ghosts and spine), Build with helper outlines (a tap
// adds a copy), the grow slider, the ?open=bodhiPyro:chorus link; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const site = process.env.SITE ?? 'kaleidohedra';
await page.goto(`${BASE}/index.html?site=${site}`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:bodhiPyroWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const btn = page.locator('[data-action="tool:bodhiPyroWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForTimeout(1800);
const panel = page.locator('#worldbodhipyro-panel');
assert.ok(await panel.isVisible(), 'panel shows');
const note = () => panel.locator('.gbp-note').textContent();
const count = async () => Number((await note()).match(/(\d+) cop/)?.[1] ?? NaN);
for (const m of ['network', 'double', 'voice', 'chorus']) {
  await panel.locator(`[data-gbp-mode="${m}"]`).tap(); await page.waitForTimeout(1500);
  console.log(m, '|', await note());
  if (m === 'double') { await panel.locator('[data-gbp="gaps"]').tap(); await page.waitForTimeout(1200); }
  if (m === 'voice') { await panel.locator('[data-gbp-voice="2"]').tap(); await page.waitForTimeout(1000); assert.match(await note(), /3/); }
  await page.screenshot({ path: `${SH}/bodhipyro-${m}.png` });
}
assert.match(await note(), /kept|copies/);
// grow slider in the chorus
const slider = panel.locator('.gbp-size-row input');
await slider.evaluate((s) => { s.value = '8'; s.dispatchEvent(new Event('input')); s.dispatchEvent(new Event('change')); });
await page.waitForTimeout(1500); console.log('chorus r8 |', await note()); await page.screenshot({ path: `${SH}/bodhipyro-chorus8.png` });
// Build in one network: helper outlines, a tap adds a copy
await panel.locator('[data-gbp-mode="network"]').tap(); await page.waitForTimeout(1200);
await panel.locator('[data-gbp="build"]').tap(); await page.waitForTimeout(1200);
const before = await count();
let after = before;
outer: for (const fy of [0.35, 0.3, 0.4, 0.25, 0.45, 0.2]) for (const fx of [0.5, 0.42, 0.58, 0.35, 0.65, 0.3, 0.7]) {
  await page.touchscreen.tap(1024 * fx, 1366 * fy); await page.waitForTimeout(500);
  after = await count(); if (after > before) break outer;
}
console.log('build: copies', before, '->', after); assert.ok(after > before, 'a tap in Build adds a copy');
await page.screenshot({ path: `${SH}/bodhipyro-build.png` });
// ?open= link straight to the chorus
await page.goto(`${BASE}/index.html?site=${site}&open=bodhiPyro:chorus`); await page.waitForTimeout(4000);
assert.ok(await page.locator('#worldbodhipyro-panel').isVisible(), 'opened by link');
assert.match(await page.locator('#worldbodhipyro-panel .gbp-note').textContent(), /kept/);
await page.screenshot({ path: `${SH}/bodhipyro-link.png` });
assert.deepEqual(errors, []);
console.log('bodhi-pyro ok', site); await b.close();
