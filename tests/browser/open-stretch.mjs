// Paper #49's "View in app" (DICTO 2026-10-23), at phone width, on every door: ?open=studies:stretch opens Studies straight on the
// DICTO stretched solids as the paper's theorem shows them (two caps along a face diagonal, equal-edged: 12 pentagons + 10 rhombi),
// even when Studies was last left on another study; and the Almanac's #49 entry → Open lands on the same view. No console errors.
// Works on the source (index.html?site=<door>) and on a built door (BUILT=1: the door is the build's own). Screenshots: SHOTS.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const SH = process.env.SHOTS ?? '/tmp';
const DOORS = (process.env.DOORS ?? 'kaleidohedra,rhombiverse,polyhedraverse').split(',');
const BUILT = !!process.env.BUILT;
const url = (door, q) => `${BASE}/index.html?${BUILT ? '' : `site=${door}&`}${q}&probe`;

const browser = await chromium.launch();
const errors = [];
async function load(page, door, q) {
  await page.goto(url(door, q));
  await page.waitForTimeout(1500);
  if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
  await page.waitForTimeout(2500);
}
async function expectStretch(page, door, how) {
  const st = await page.evaluate(() => window.__studiesProbe());
  const panel = page.locator('#worldstudies-panel');
  assert.deepEqual({ study: st.study, direction: st.direction, caps: st.caps, spacing: st.spacing, faces: st.faces },
    { study: 'stretch', direction: 'face', caps: 2, spacing: 1, faces: 22 }, `${door} ${how}: the stretched-solids view`);
  assert.equal(await panel.isVisible(), true, `${door} ${how}: Studies panel shows`);
  assert.match(await panel.locator('[data-select="study"] option:checked').textContent(), /DICTO stretched solids/);
  assert.match(await panel.locator('[data-st-dir="face"]').getAttribute('aria-pressed'), /true/);
  assert.match(await panel.locator('.st-slider-val').textContent(), /equal-edged/);
  console.log(door, how, JSON.stringify(st), 'title:', JSON.stringify(await page.locator('#hud-world-title').textContent()));
}
for (const door of DOORS) {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  page.on('pageerror', (e) => errors.push(`${door}: ${e}`));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(`${door}: ${m.text()}`); });
  page.on('dialog', (d) => d.accept());
  // Leave Studies on another study first, through its own select, so the link has to override what was saved.
  await load(page, door, 'open=studies');
  await page.locator('#worldstudies-panel [data-select="study"]').selectOption('windows');
  await page.waitForTimeout(600);
  assert.equal((await page.evaluate(() => window.__studiesProbe())).study, 'windows');
  // The deep link.
  await load(page, door, 'open=studies:stretch');
  await expectStretch(page, door, 'deep link');
  await page.screenshot({ path: `${SH}/view49-${door}${BUILT ? '-built' : ''}.png` });
  // The Almanac: 📖 → #49 → Open (after leaving Studies on another study again).
  await page.locator('#worldstudies-panel [data-select="study"]').selectOption('windows');
  await page.waitForTimeout(600);
  await page.tap('#almanac-btn');
  await page.waitForSelector('.almanac-overlay.open');
  await page.tap('.almanac-back').catch(() => {}); // it may open on where you are
  const row = page.locator('.almanac-entry', { hasText: 'The Polyhedral Stretching Theorem' }).first();
  await row.scrollIntoViewIfNeeded();
  await row.tap();
  await page.tap('.almanac-open');
  await page.waitForTimeout(2500);
  assert.equal(await page.locator('.almanac-overlay').evaluate((el) => el.classList.contains('open')), false, `${door}: the Almanac closes`);
  await expectStretch(page, door, 'Almanac Open');
  await page.close();
}
console.log(errors.length ? `ERRORS:\n${errors.join('\n')}` : 'no errors');
assert.equal(errors.length, 0);
await browser.close();
console.log('open-stretch OK');
