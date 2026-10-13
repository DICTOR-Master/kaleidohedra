// The Icosahedral Octet Lattice (DICTO 2026-10-13), through the real UI on an iPad: listed right after the Sunstar Lattice in the
// DICTO menu, and a tap adds a cell (or a whole cluster) in three of its versions.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action^="tool:sunstarWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const order = await page.evaluate(() => [...document.querySelectorAll('.dim-wizard-overlay [data-action]')].map((e) => e.dataset.action));
const iSun = order.findIndex((a) => a.startsWith('tool:sunstarWorld')), iB = order.indexOf('tool:octetBuildWorld:caps');
const lastSun = order.map((a, i) => (a.startsWith('tool:sunstarWorld') ? i : -1)).filter((i) => i >= 0).pop();
console.log('sunstar entries', iSun, '..', lastSun, '; octet build first entry', iB, '; build entries', order.filter((a) => a.startsWith('tool:octetBuildWorld')).length);
assert.ok(iB > lastSun && iB - lastSun <= 3, 'octet lattice right after the Sunstar Lattice');
const count = () => page.textContent('#worldoctetbuild-panel .octb-note');
for (const id of ['caps', 'lotusJewel.clusters', 'frog']) {
  if (!(await page.locator('.dim-wizard-overlay.open').count())) await page.tap('#hud-wizard-cue');
  await page.waitForTimeout(400);
  if (!(await page.locator('[data-action^="tool:octetBuildWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  const btn = page.locator(`[data-action="tool:octetBuildWorld:${id}"]`).first();
  await btn.scrollIntoViewIfNeeded(); await btn.tap();
  await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) { console.log('asked to keep the build: keep'); await page.tap('#leave-dialog [data-choice="keep"]'); }
  await page.waitForSelector('#worldoctetbuild-panel.visible'); await page.waitForTimeout(1200);
  await page.tap('[data-octb="reset"]'); await page.waitForTimeout(500);
  const before = await count();
  // tap a few points around the middle of the screen until a cell is added
  let after = before;
  for (const [dx, dy] of [[0, 0], [30, -20], [-40, 25], [60, 40], [-60, -50]]) {
    await page.touchscreen.tap(512 + dx, 600 + dy); await page.waitForTimeout(400);
    after = await count(); if (after !== before) break;
  }
  console.log(id, '|', before, '->', after);
  assert.notEqual(after, before, `${id}: a tap adds cells`);
  await page.screenshot({ path: `${process.env.SHOTS ?? '/tmp'}/octb-${id}.png` });
}
console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors');
assert.equal(errors.length, 0);
await b.close();
console.log('octet-build OK');
