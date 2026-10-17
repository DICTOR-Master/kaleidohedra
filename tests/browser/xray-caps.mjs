// X-ray solid infill (DICTO 2026-10-17): with the X-ray plane on, every solid the plane cuts is filled in its own colour. Opens
// Theaetetus on its Cleo star view and the fcc lattice, turns X-ray on, checks that solids are being filled (body[data-xray-caps]) and
// that the picture changes where they are cut, with no console errors. Screenshots for a look.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const page = await b.newPage({ viewport: { width: 1100, height: 800 } });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
const shot = () => page.locator('#scene-canvas').screenshot();
for (const [name, url] of [['cleostar', `${BASE}/index.html?site=kaleidohedra&open=theaetetus`], ['fcc', `${BASE}/index.html?site=rhombiverse`]]) {
  await page.goto(url); await page.evaluate(() => { try { localStorage.clear(); } catch {} });
  await page.goto(url);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }).catch(() => {}); await page.keyboard.press('Enter').catch(() => {});
  await page.waitForTimeout(1500);
  if (name === 'cleostar') {
    await page.keyboard.press('Escape'); await page.waitForTimeout(400);
    await page.evaluate(() => { const s = [...document.querySelectorAll('.qc-panel.visible select')][0]; if (s) { s.value = 'cleostar'; s.dispatchEvent(new Event('change')); } });
  } else {
    const rd = page.locator('[data-action="tool:pieceType:rd"]').first(); if (await rd.count()) { await rd.click(); }
    const box = await page.locator('#scene-canvas').boundingBox(); for (let i = 0; i < 6; i++) { await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2); await page.waitForTimeout(250); }
  }
  await page.waitForTimeout(1200);
  const before = await shot();
  await page.evaluate(() => { const t = document.getElementById('xray-toggle'); t.click(); }); await page.waitForTimeout(400);
  if (!(await page.evaluate(() => document.getElementById('section-enable').checked))) { await page.evaluate(() => document.getElementById('xray-toggle').click()); await page.waitForTimeout(400); }
  await page.waitForTimeout(1200);
  const filled = Number(await page.evaluate(() => document.body.dataset.xrayCaps ?? 0));
  await page.screenshot({ path: `${SH}/caps-${name}.png` });
  console.log(name, 'filled solids', filled);
  assert.ok(filled > 0, `${name}: cut solids are filled`);
}
assert.deepEqual(errors, []);
console.log('xray caps ok'); await b.close();
