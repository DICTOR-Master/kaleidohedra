// Queen sectors (DICTO 2026-10-31): the Sectors toggle in the Queens world's Shells view through the real UI, phone (390×844, touch) and
// desktop (1280×800, mouse), Kaleidohedra door: both Queens, Sectors on (12 for the Red Queen, 20 for the White), the core falling into
// its 12 pentagonal pyramids / 20 Cleo-Icos, the "Pull the sectors apart" slider (shown only with Sectors on, no arrows), with the shells
// slider, Cut open, RCP view and RCP v4; the deep links ?open=whitequeen:sectors / :redsectors. No console errors.
// Screenshots in $SHOTS (default /tmp/queen-sectors-shots): <dev>-<queen>-*.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/queen-sectors-shots';
mkdirSync(SH, { recursive: true });
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }, desktop: { viewport: { width: 1280, height: 800 } } };
const P = '#worldwhiteQueen-panel', COUNT = { white: 20, red: 12 }, CORE = { white: 20, red: 12 };
const b = await chromium.launch();
let checks = 0;
for (const dev of Object.keys(DEVICES)) {
  const ctx = await b.newContext(DEVICES[dev]), page = await ctx.newPage(), errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  const press = (sel) => (dev === 'phone' ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__whiteQueenProbe());
  const slide = async (sel, v) => { await page.locator(sel).fill(String(v)); await page.locator(sel).dispatchEvent('change'); await page.waitForTimeout(900); };
  await page.goto(`${BASE}/index.html?probe&site=kaleidohedra`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await press('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(500);
  await page.locator('[data-action="tool:whiteQueenWorld"]').first()[dev === 'phone' ? 'tap' : 'click'](); await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await press('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  await press(`${P} [data-wq-mode="shells"]`); await page.waitForTimeout(1200);
  for (const queen of ['white', 'red']) {
    const tag = `${dev}-${queen}`;
    if ((await page.getAttribute(`${P} [data-wq-queen="${queen}"]`, 'aria-pressed')) !== 'true') { await press(`${P} [data-wq-queen="${queen}"]`); await page.waitForTimeout(1200); }
    await slide(`${P} .wq-shells-row input`, 1);
    // Sectors: off at first, its slider hidden; in the Cut open / RCP row
    assert.equal(await page.getAttribute(`${P} [data-wq-sectors]`, 'aria-pressed'), 'false');
    assert.equal(await page.locator(`${P} .wq-sectors-row`).isHidden(), true, `${tag}: slider hidden while off`);
    assert.equal(await page.locator(`${P} [data-wq-sectors]`).textContent(), 'Sectors');
    if (dev === 'phone') { const bx = await page.locator(`${P} [data-wq-sectors]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: touchable ${bx.width}×${bx.height}`); }
    await press(`${P} [data-wq-sectors]`); await page.waitForTimeout(1200);
    let st = await probe();
    assert.equal(st.queen, queen);
    assert.deepEqual([st.sectors.count, st.sectors.wedges], [COUNT[queen], CORE[queen]], `${tag}: the core in its ${CORE[queen]} pieces`); checks++;
    assert.match(await page.locator(`${P} .ch-param-caption`).textContent(), new RegExp(`${COUNT[queen]} sectors · ${CORE[queen]} pieces`));
    // the apart slider: big, shown, no arrows; pulling widens the picture
    assert.equal(await page.locator(`${P} .wq-sectors-row`).isVisible(), true);
    const sb = await page.locator(`${P} .wq-sectors-row input`).boundingBox(); assert.ok(sb.width >= (dev === 'phone' ? 250 : 200), `${tag}: big slider ${sb.width}`);
    assert.equal(await page.locator(`${P} .wq-sectors-row button`).count(), 0, `${tag}: no arrows`);
    await slide(`${P} .wq-sectors-row input`, 0);
    const r0 = (await probe()).radius;
    await slide(`${P} .wq-sectors-row input`, 700);
    st = await probe(); assert.equal(st.sectors.apart, 700); assert.ok(st.radius > r0 * 1.3, `${tag}: pulled apart ${st.radius} vs ${r0}`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-core.png` });
    // with the shells slider: all shells built, every cell cut
    const total = st.total;
    await slide(`${P} .wq-shells-row input`, total);
    st = await probe(); assert.equal(st.shells, total); assert.ok(st.sectors.wedges > CORE[queen], `${tag}: ${st.sectors.wedges} pieces`); checks++;
    await slide(`${P} .wq-shells-row input`, Math.ceil(total / 2));
    await page.screenshot({ path: `${SH}/${tag}-shells.png` });
    // with Cut open, then RCP view and RCP v4 (each with Cut open)
    await press(`${P} [data-wq-whole]`); await page.waitForTimeout(1500);
    st = await probe(); assert.equal(st.whole, true); assert.equal(st.sectors.count, COUNT[queen]); assert.ok(st.sectors.wedges > 0); checks++;
    await page.screenshot({ path: `${SH}/${tag}-cutopen.png` });
    for (const k of ['rcp', 'dicto-rcp']) {
      await press(`${P} [data-wq-${k}]`); await page.waitForTimeout(1500);
      st = await probe(); assert.equal(k === 'rcp' ? st.rcp : st.dictoRcp, true); assert.ok(st.sectors.wedges > 0, `${tag} ${k}`); checks++;
      await page.screenshot({ path: `${SH}/${tag}-cutopen-${k}.png` });
    }
    await press(`${P} [data-wq-dicto-rcp]`); await page.waitForTimeout(800);
    await press(`${P} [data-wq-whole]`); await page.waitForTimeout(1000);
    // off again: the cells whole, the slider hidden
    await press(`${P} [data-wq-sectors]`); await page.waitForTimeout(1000);
    st = await probe(); assert.equal(st.sectors, null); assert.equal(await page.locator(`${P} .wq-sectors-row`).isHidden(), true); checks++;
  }
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  // the deep links: all shells, Cut open, the sectors pulled apart
  for (const [kind, queen] of [['sectors', 'white'], ['redsectors', 'red']]) {
    await page.goto(`${BASE}/index.html?probe&site=kaleidohedra&open=whitequeen:${kind}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }).then(() => page.keyboard.press('Enter')).catch(() => {});
    await page.waitForSelector(`${P}.visible`, { timeout: 30000 }); await page.waitForTimeout(2000);
    const st = await probe();
    assert.deepEqual([st.queen, st.mode, st.sectors?.count, st.sectors?.apart > 0], [queen, 'shells', COUNT[queen], true], `${dev}: ?open=whitequeen:${kind}`); checks++;
    await page.screenshot({ path: `${SH}/${dev}-${queen}-link.png` });
  }
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  await ctx.close();
}
await b.close();
console.log(`queen-sectors: ${checks} checks passed`);
