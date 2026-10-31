// HexOct (DICTO 2026-10-31; paper #75) through the real UI, phone (390×844, touch) and desktop (1280×800, mouse), Polyhedraverse door:
// DICTO's pieces list HexOct first; it opens in Polyhedraverse on the c-tiles (3C); each fill button (3C, 2H, 4H, 6H, Fibonacci) stacks
// its layers, 3 × 3 tiles of 4 pieces each; the field takes the viewer's own c/h sequence (Enter or Stack) and refuses anything else;
// Helpers turns the pieces to glass and back; edges ≥ 1.5 px; no paint, shear or lattice-view controls. The deep links
// ?open=hexoct:fib and ?open=hexoct:chh. No console errors.
// Screenshots in $SHOTS (default /tmp/hexoct-shots): <dev>-<fill>.png, <dev>-fib-helpers.png, <dev>-own.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/hexoct-shots';
mkdirSync(SH, { recursive: true });
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }, desktop: { viewport: { width: 1280, height: 800 } } };
const P = '#worldhexoct-panel';
const FILLS = { '3C': 'cccccccc', '2H': 'hhhhhhhh', '4H': 'chchchch', '6H': 'hcchcchc', fib: 'chcchchc' };
const b = await chromium.launch();
let checks = 0;
for (const dev of Object.keys(DEVICES)) {
  const ctx = await b.newContext(DEVICES[dev]), page = await ctx.newPage(), errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  const press = (sel) => (dev === 'phone' ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__hexoctProbe());
  await page.goto(`${BASE}/index.html?probe&site=polyhedraverse`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('[data-family="DICTO_PIECES"]').count())) await press('.dim-wizard-card-btn[data-dim="3D"]');
  const fam = page.locator('[data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam[dev === 'phone' ? 'tap' : 'click'](); await page.waitForTimeout(800);
  // HexOct is the first section of DICTO's pieces
  assert.equal(await page.locator('.poly-section').first().getAttribute('data-section'), 'hexoct', `${dev}: HexOct first`); checks++;
  await page.locator('[data-hexoct]').first()[dev === 'phone' ? 'tap' : 'click'](); await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await press('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'HexOct', `${dev}: title`);
  // Polyhedraverse's space; nothing that does not apply
  for (const sel of ['#hud-quick-lattice-view', '#shear-panel']) assert.ok(!(await page.locator(sel).isVisible().catch(() => false)), `${dev}: ${sel} hidden`);
  checks++;
  let st = await probe();
  assert.deepEqual([st.kind, st.helpers, st.glass], ['3C', false, false], `${dev}: c-tiles, solid`);
  assert.ok(st.lineWidth >= 1.5, `${dev}: edges ${st.lineWidth} px`); checks++;
  for (const [fill, types] of Object.entries(FILLS)) {
    const btn = `${P} [data-hx-kind="${fill}"]`;
    if (dev === 'phone') { const bx = await page.locator(btn).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 36, `${dev} ${fill}: touchable ${bx.width}×${bx.height}`); }
    await press(btn); await page.waitForTimeout(900);
    st = await probe();
    assert.deepEqual([st.kind, st.types, st.pieces, st.c, st.h], [fill, types, types.length * 36, [...types].filter((x) => x === 'c').length, [...types].filter((x) => x === 'h').length], `${dev}: ${fill}`);
    assert.equal(await page.getAttribute(btn, 'aria-pressed'), 'true');
    assert.match(await page.locator(`${P} .hx-caption`).textContent(), new RegExp(`${types.length} layers, bottom up: ${[...types].join(' ')}`));
    assert.equal(await page.locator(`${P} .hx-own`).inputValue(), types, `${dev} ${fill}: the field shows the layers`);
    checks++;
    if (fill !== 'fib') await page.screenshot({ path: `${SH}/${dev}-${fill}.png` });
  }
  // Helpers on Fibonacci: glass, and back
  await press(`${P} [data-hx-helpers]`); await page.waitForTimeout(900);
  st = await probe(); assert.deepEqual([st.kind, st.helpers, st.glass], ['fib', true, true], `${dev}: helpers on`);
  assert.equal(await page.getAttribute(`${P} [data-hx-helpers]`, 'aria-pressed'), 'true'); checks++;
  await page.screenshot({ path: `${SH}/${dev}-fib-helpers.png` });
  await press(`${P} [data-hx-helpers]`); await page.waitForTimeout(700);
  st = await probe(); assert.deepEqual([st.helpers, st.glass], [false, false], `${dev}: helpers off`); checks++;
  await page.screenshot({ path: `${SH}/${dev}-fib.png` });
  // the viewer's own sequence: a bad one is refused (the crystal stays), a good one stacks (Enter on the desktop, Stack on the phone)
  await page.locator(`${P} .hx-own`).fill('chx');
  await press(`${P} [data-hx-own-go]`); await page.waitForTimeout(500);
  st = await probe(); assert.equal(st.kind, 'fib', `${dev}: refused`);
  assert.match(await page.locator(`${P} .hx-note`).textContent(), /c and h only/); checks++;
  await page.locator(`${P} .hx-own`).fill('C H H');
  if (dev === 'phone') await press(`${P} [data-hx-own-go]`); else await page.locator(`${P} .hx-own`).press('Enter');
  await page.waitForTimeout(900);
  st = await probe(); assert.deepEqual([st.kind, st.own, st.types, st.pieces], ['own', 'chh', 'chhchh', 6 * 36], `${dev}: own`);
  assert.equal(await page.getAttribute(`${P} [data-hx-kind="own"]`, 'aria-pressed'), 'true'); checks++;
  await page.screenshot({ path: `${SH}/${dev}-own.png` });
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  // the deep links
  for (const [link, kind, types] of [['hexoct:fib', 'fib', FILLS.fib], ['hexoct:chh', 'own', 'chhchh']]) {
    await page.goto(`${BASE}/index.html?probe&open=${link}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 8000 }).then(() => page.keyboard.press('Enter')).catch(() => {});
    await page.waitForSelector(`${P}.visible`, { timeout: 30000 }); await page.waitForTimeout(1500);
    st = await probe();
    assert.deepEqual([st.kind, st.types], [kind, types], `${dev}: ?open=${link}`);
    assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, `${dev}: no wizard over it`); checks++;
  }
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  await ctx.close();
}
await b.close();
console.log(`hexoct: ${checks} checks passed`);
