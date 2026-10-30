// Rhombiverse's choice of lattices (DICTO 2026-10-31) through the real UI, on a phone (390 × 844, touch) and a desktop: from the
// Kaleidohedra door, the wizard's 3D+ shows Rhombiverse as one row ("Every lattice, piece by piece"); a tap opens Rhombiverse's
// lattice list (every lattice with its pieces, in Rhombiverse's colours, each opening in Rhombiverse) instead of jumping to FCC;
// Back returns to 3D+ with the row; tapping hcp opens Rhombiverse on hcp (its title in the header). No console errors.
// Screenshots (SHOTS): rhombi-choice-phone.png, rhombi-choice-desktop.png (the opened lattice choice).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch();
for (const [name, opts] of [['phone', { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 3 }], ['desktop', { viewport: { width: 1280, height: 800 } }]]) {
  const page = await b.newPage(opts);
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = async (sel) => { const l = page.locator(sel).first(); await l.scrollIntoViewIfNeeded(); await (opts.hasTouch ? l.tap() : l.click()); };
  await page.goto(`${BASE}/index.html?site=kaleidohedra`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  const row = '.dim-wizard-body [data-lattices="rhombiverse"]';
  assert.equal(await page.locator(row).count(), 1, `${name}: one Rhombiverse row in 3D+`);
  assert.match(await page.locator(`${row} .dim-wizard-label`).textContent(), /Every lattice, piece by piece/, `${name}: the row's new label`);
  assert.match(await page.locator(`${row} .dim-wizard-desc`).textContent(), /The original app/, `${name}: the row's new description`);
  await press(row); await page.waitForTimeout(600);
  // still in the wizard, in Kaleidohedra's space: the tap opened the choice, not FCC
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 1, `${name}: the wizard stays open`);
  assert.equal(await page.evaluate(() => document.documentElement.dataset.activeSite), 'kaleidohedra', `${name}: no jump to Rhombiverse yet`);
  const list = await page.evaluate(() => {
    const btns = [...document.querySelectorAll('.dim-wizard-body .dicto-block [data-action]')];
    return { names: [...document.querySelectorAll('.dim-wizard-body .dicto-block-name')].map((x) => x.textContent), apps: [...new Set(btns.map((x) => x.dataset.app))],
      actions: btns.map((x) => x.dataset.action), heights: btns.map((x) => x.getBoundingClientRect().height), back: !!document.querySelector('.dim-wizard-body .dim-wizard-back') };
  });
  console.log(name, `${list.actions.length} choices:`, list.actions.join(' '));
  assert.deepEqual(list.names, ['RHOMBIVERSE'], `${name}: one Rhombiverse block`);
  assert.deepEqual(list.apps, ['rhombiverse'], `${name}: every choice opens in Rhombiverse`);
  for (const a of ['tool:pieceType:rd', 'tool:pieceType:hcp', 'tool:pieceType:triprism', 'tool:pieceType:gyro']) assert.ok(list.actions.includes(a), `${name}: ${a} listed`);
  assert.ok(list.actions.length >= 8, `${name}: every lattice with its pieces`);
  assert.ok(Math.min(...list.heights) >= 44, `${name}: full touch targets (smallest ${Math.min(...list.heights)})`);
  assert.ok(list.back, `${name}: a way back`);
  assert.equal(await page.locator('.dim-wizard-body').evaluate((el) => /[◀▶]/.test(el.textContent)), false, `${name}: no arrows`);
  await page.evaluate(() => document.querySelector('.dim-wizard-body').parentElement.scrollTop = 0);
  await page.waitForTimeout(1500); // the turning previews start a moment after the list
  await page.screenshot({ path: `${SH}/rhombi-choice-${name}.png` });
  // Back: 3D+ again, the row still there; then in again
  await press('.dim-wizard-body .dim-wizard-back'); await page.waitForTimeout(400);
  assert.equal(await page.locator(row).count(), 1, `${name}: back to 3D+ with the Rhombiverse row`);
  await press(row); await page.waitForTimeout(600);
  // hcp (Rhombiverse's own, not in Kaleidohedra): opens Rhombiverse on hcp
  await press('.dim-wizard-body [data-action="tool:pieceType:hcp"]'); await page.waitForTimeout(1200);
  if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(600); }
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, `${name}: the wizard closed`);
  assert.equal(await page.evaluate(() => document.documentElement.dataset.activeSite), 'rhombiverse', `${name}: in Rhombiverse's space`);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'HCP · trapezo-rhombic dodecahedra', `${name}: on hcp`);
  console.log(name, errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.deepEqual(errors, []);
  await page.close();
}
await b.close(); console.log('rhombi-choice OK');
