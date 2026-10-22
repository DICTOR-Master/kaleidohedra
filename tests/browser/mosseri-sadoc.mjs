// The Mosseri–Sadoc tiles (DICTO 2026-10-23), through the real UI on every door, on a phone (touch): DICTO → 3D+ →
// Mosseri–Sadoc tiles (1982) lists M-S t1, Cleo (M-S t4), M-S t5 and AXE (M-S t6); M-S t1 and M-S t5 open their details
// with the Mosseri–Sadoc credit; Build places M-S t5; search "Mosseri" finds the four. SHOTS saves screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SHOTS = process.env.SHOTS ?? '/tmp';
const DOORS = (process.env.DOORS ?? 'kaleidohedra,rhombiverse,polyhedraverse').split(',');
const VIEWPORTS = { phone: { width: 390, height: 844 }, ipad: { width: 1024, height: 1366 } };
const b = await chromium.launch();
for (const door of DOORS) for (const [vp, viewport] of Object.entries(VIEWPORTS)) {
  const page = await b.newPage({ viewport, hasTouch: true, isMobile: true });
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?site=${door}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  if (!(await page.locator('[data-family="MOSSERI_SADOC"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  const fam = page.locator('[data-family="MOSSERI_SADOC"]').first(); await fam.scrollIntoViewIfNeeded();
  assert.match(await fam.textContent(), /Mosseri–Sadoc tiles \(1982\)/);
  await fam.tap(); await page.waitForTimeout(800);
  const labels = await page.$$eval('.dim-wizard-body [data-action^="tool:polyShape:"] .dim-wizard-label', (els) => els.map((e) => e.textContent.trim()));
  assert.deepEqual(labels, ['M-S t1', 'Cleo (M-S t4)', 'M-S t5', 'AXE (M-S t6)'], `${door} ${vp}: family list`);
  await page.screenshot({ path: `${SHOTS}/ms-t1-t5-${door}-${vp}-family.png` });
  for (const [id, letter] of [['MS_T1', 'B'], ['MS_T5', 'C']]) {
    const card = page.locator(`[data-action="tool:polyShape:${id}"]`).first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await page.waitForTimeout(800);
    assert.equal((await page.textContent('.poly-detail-name')).trim(), `M-S ${id.slice(-2).toLowerCase()}`);
    const credit = await page.textContent('[data-credit="mosseri-sadoc"]');
    assert.ok(credit.includes(`their letter ${letter}`) && credit.includes('Mosseri & Sadoc 1982') && credit.includes('Koca'), `${id} credit`);
    await page.screenshot({ path: `${SHOTS}/ms-t1-t5-${door}-${vp}-${id.toLowerCase()}-detail.png` });
    if (id === 'MS_T5') break;
    await page.tap('.dim-wizard-back'); await page.waitForTimeout(600);
  }
  // Build with M-S t5: the wizard closes and the piece is placed in Polyhedraverse's space.
  await page.tap('.poly-detail-build'); await page.waitForTimeout(2500);
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, 'wizard closed on Build');
  await page.screenshot({ path: `${SHOTS}/ms-t1-t5-${door}-${vp}-t5-built.png` });
  // Search finds the four by the family's name.
  await page.goto(`${BASE}/index.html?site=${door}`);
  await page.waitForSelector('.dim-wizard-overlay.open, #welcome-overlay', { timeout: 25000 });
  if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForSelector('.dim-wizard-overlay.open'); }
  if (!(await page.locator('.poly-search-input').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  const input = page.locator('.poly-search-input').first(); await input.scrollIntoViewIfNeeded(); await input.tap(); await input.fill('mosseri'); await page.waitForTimeout(800);
  const found = await page.$$eval('.poly-search-results [data-shape]', (els) => els.map((e) => e.dataset.shape));
  assert.deepEqual(found.sort(), ['KIT13_ICOSA13_AXE', 'KIT13_ICOSA13_CLEO', 'MS_T1', 'MS_T5'], `${door} ${vp}: search`);
  console.log(`${door} ${vp}: ${labels.join(', ')} · search ${found.length} · ${errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'}`);
  assert.equal(errors.length, 0);
  await page.close();
}
await b.close(); console.log('mosseri-sadoc OK');
