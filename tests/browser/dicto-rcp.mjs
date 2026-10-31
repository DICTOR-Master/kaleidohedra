// RCP v4 (DICTO's adjusted RCP, DICTO 2026-10-31, to try out): the eye beyond the far side, the seed at its true size, through the real UI on a phone
// (390×844, touch) and a desktop (1280×800, mouse). Polyhedraverse's 4D build: the RCP v4 button in the 4D row, beside the target,
// toggles and is saved (view.rcp.dicto, absent when off), for the 600-cell vertex-first and the 120-cell, and the build keeps its
// cells and shells. The Queens world (Kaleidohedra door): RCP v4 is a third toggle beside Whole and RCP view; it and RCP view
// exclude each other, Whole (its button now 'Cut open') goes with either; saved and back after a reload; the note says what it is. No console errors.
// Screenshots in $SHOTS (default /tmp/dicto-rcp-shots): <dev>-pv-600-{rcp,dicto}.png, <dev>-pv-120-…, <dev>-<queen>-{rcp,dicto}.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/dicto-rcp-shots';
mkdirSync(SH, { recursive: true });
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }, desktop: { viewport: { width: 1280, height: 800 } } };
const b = await chromium.launch();
let checks = 0;

async function openDoor(dev, door, seed) {
  const ctx = await b.newContext(DEVICES[dev]), page = await ctx.newPage(), errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  if (seed) await ctx.addInitScript((s) => { if (sessionStorage.getItem('seeded')) return; sessionStorage.setItem('seeded', '1'); localStorage.setItem('polyhedraverse-poly-world', JSON.stringify(s)); }, seed);
  await page.goto(`${BASE}/index.html?probe&site=${door}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  const press = (sel) => (dev === 'phone' ? page.tap(sel) : page.click(sel));
  return { ctx, page, errors, press };
}
async function closeWizard(h) {
  await h.press('.dim-wizard-close'); await h.page.waitForTimeout(400);
  if (await h.page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await h.press('#leave-dialog [data-choice="continue"]'); await h.page.waitForTimeout(300); }
}
const touchable = async (page, sel, tag) => { const bx = await page.locator(sel).boundingBox(); assert.ok(bx && bx.height >= 30 && bx.width >= 44, `${tag}: ${sel} touchable (${bx?.width}×${bx?.height})`); };

// ---- Polyhedraverse: the 4D build ----
const pvSaved = (page) => page.evaluate(() => JSON.parse(localStorage.getItem('polyhedraverse-poly-world') ?? 'null'));
for (const dev of Object.keys(DEVICES)) {
  for (const [name, shape, target, cellTaps, shellTaps] of [['600', 'D4', '600-cell (vertex-first)', 19, 2], ['120', 'DODECAHEDRON', '120-cell', 12, 2]]) {
    const tag = `${dev}-pv-${name}`;
    const h = await openDoor(dev, 'polyhedraverse', { version: 1, connections: [], view: {}, nodes: [{ id: 'a', shape, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] });
    await closeWizard(h);
    await h.press('[data-rcp-start]'); await h.page.waitForTimeout(800);
    if (await h.page.locator('[data-rcp-target]').inputValue() !== target) { await h.page.selectOption('[data-rcp-target]', target); await h.page.waitForTimeout(1500); }
    // RCP v4 sits in the 4D row, right after the target; off at first
    assert.equal(await h.page.evaluate(() => document.querySelector('[data-rcp-target]').nextElementSibling?.matches('[data-rcp-dicto]')), true, `${tag}: beside the target`);
    assert.equal(await h.page.getAttribute('[data-rcp-dicto]', 'aria-pressed'), 'false');
    if (dev === 'phone') await touchable(h.page, '[data-rcp-dicto]', tag);
    for (let i = 0; i < cellTaps + shellTaps; i++) { await h.press('[data-rcp-next]'); await h.page.waitForTimeout(350); }
    await h.page.waitForTimeout(800);
    const n = (await pvSaved(h.page)).view.rcp.n;
    assert.ok(n > cellTaps + 1, `${tag}: shells built (${n} cells)`); checks++;
    await h.page.screenshot({ path: `${SH}/${tag}-rcp.png` });
    await h.press('[data-rcp-dicto]'); await h.page.waitForTimeout(1500);
    let s = (await pvSaved(h.page)).view.rcp;
    assert.equal(await h.page.getAttribute('[data-rcp-dicto]', 'aria-pressed'), 'true');
    assert.deepEqual([s.dicto, s.n, s.target, s.open], [true, n, target, false], `${tag}: RCP v4 on, the build kept`); checks++;
    await h.page.screenshot({ path: `${SH}/${tag}-dicto.png` });
    // off again: the RCP view in the same (widened) frame, to compare; then on again
    await h.press('[data-rcp-dicto]'); await h.page.waitForTimeout(1200);
    await h.page.screenshot({ path: `${SH}/${tag}-rcp-same.png` });
    await h.press('[data-rcp-dicto]'); await h.page.waitForTimeout(1200);
    // still building on in RCP v4, and a reload keeps it
    await h.press('[data-rcp-next]'); await h.page.waitForTimeout(800);
    assert.ok((await pvSaved(h.page)).view.rcp.n > n, `${tag}: next shell in RCP v4`);
    await h.page.reload(); await h.page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await h.page.keyboard.press('Enter');
    await h.page.waitForSelector('.dim-wizard-overlay.open'); await h.page.waitForTimeout(400); await closeWizard(h); await h.page.waitForTimeout(800);
    assert.equal(await h.page.getAttribute('[data-rcp-dicto]', 'aria-pressed'), 'true', `${tag}: kept after reload`); checks++;
    await h.press('[data-rcp-dicto]'); await h.page.waitForTimeout(800);
    s = (await pvSaved(h.page)).view.rcp;
    assert.equal('dicto' in s, false, `${tag}: off leaves no dicto key`); checks++;
    assert.deepEqual(h.errors, [], `${tag}: console errors`); checks++;
    await h.ctx.close();
  }
}

// ---- the Queens world (Kaleidohedra door) ----
const P = '#worldwhiteQueen-panel';
for (const dev of Object.keys(DEVICES)) {
  const h = await openDoor(dev, 'kaleidohedra'), { page } = h, probe = () => page.evaluate(() => window.__whiteQueenProbe());
  if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await h.press('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(500);
  await page.locator('[data-action="tool:whiteQueenWorld"]').first()[dev === 'phone' ? 'tap' : 'click'](); await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await h.press('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  await h.press(`${P} [data-wq-mode="shells"]`); await page.waitForTimeout(1200);
  // the third toggle in the Whole / RCP view row
  assert.deepEqual(await page.evaluate((p) => [...document.querySelectorAll(`${p} .wq-whole-row button`)].map((x) => Object.keys(x.dataset)[0]), P), ['wqWhole', 'wqRcp', 'wqDictoRcp']);
  assert.equal(await page.locator(`${P} [data-wq-dicto-rcp]`).textContent(), 'RCP v4');
  assert.equal(await page.locator(`${P} [data-wq-whole]`).textContent(), 'Cut open');
  if (dev === 'phone') await touchable(page, `${P} [data-wq-dicto-rcp]`, dev);
  assert.match(await page.locator(`${P} .st-note.fold`).textContent(), /RCP v4: the eye beyond the far side/); checks++;
  for (const [queen, shells] of [['white', 6], ['red', 5]]) {
    const tag = `${dev}-${queen}`;
    if ((await probe()).queen !== queen) { await h.press(`${P} [data-wq-queen="${queen}"]`); await page.waitForTimeout(1500); }
    if ((await probe()).mode !== 'shells') { await h.press(`${P} [data-wq-mode="shells"]`); await page.waitForTimeout(1200); }
    await page.locator(`${P} .wq-shells-row input`).fill(String(shells)); await page.waitForTimeout(800);
    await h.press(`${P} [data-wq-rcp]`); await page.waitForTimeout(1200);
    let st = await probe(); assert.deepEqual([st.queen, st.shells, st.rcp, st.dictoRcp], [queen, shells, true, false], `${tag}: RCP view`);
    const rcpRadius = st.radius;
    await page.screenshot({ path: `${SH}/${tag}-rcp.png` });
    await h.press(`${P} [data-wq-whole]`); await page.waitForTimeout(1500);
    await page.screenshot({ path: `${SH}/${tag}-whole-rcp.png` });
    await h.press(`${P} [data-wq-whole]`); await page.waitForTimeout(800);
    // RCP v4 turns RCP view off, and is larger out at the newest shell
    await h.press(`${P} [data-wq-dicto-rcp]`); await page.waitForTimeout(1200);
    st = await probe(); assert.deepEqual([st.rcp, st.dictoRcp, st.shells], [false, true, shells], `${tag}: RCP v4 excludes RCP view`);
    assert.equal(await page.getAttribute(`${P} [data-wq-dicto-rcp]`, 'aria-pressed'), 'true');
    assert.equal(await page.getAttribute(`${P} [data-wq-rcp]`, 'aria-pressed'), 'false');
    console.log(`${tag}: shell ${shells} radius RCP ${rcpRadius.toFixed(3)} → RCP v4 ${st.radius.toFixed(3)}`);
    assert.ok(st.radius > rcpRadius, `${tag}: shell ${shells} reaches further out`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-dicto.png` });
    // Whole goes with RCP v4
    await h.press(`${P} [data-wq-whole]`); await page.waitForTimeout(1500);
    st = await probe(); assert.deepEqual([st.whole, st.dictoRcp], [true, true], `${tag}: Whole + RCP v4`);
    await page.screenshot({ path: `${SH}/${tag}-whole-dicto.png` });
    await h.press(`${P} [data-wq-whole]`); await page.waitForTimeout(800);
    // RCP view turns RCP v4 off; then back to RCP v4 for the reload
    await h.press(`${P} [data-wq-rcp]`); await page.waitForTimeout(800);
    st = await probe(); assert.deepEqual([st.rcp, st.dictoRcp], [true, false], `${tag}: RCP view excludes RCP v4`);
    await h.press(`${P} [data-wq-dicto-rcp]`); await page.waitForTimeout(800); checks++;
  }
  const saved = await page.evaluate(() => Object.entries(localStorage).filter(([k]) => /whiteQueen/.test(k)).map(([, v]) => JSON.parse(v))[0]);
  assert.deepEqual([saved.rcp, saved.dictoRcp], [false, true], `${dev}: saved`);
  await page.reload(); await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await h.press('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(500);
  await page.locator('[data-action="tool:whiteQueenWorld"]').first()[dev === 'phone' ? 'tap' : 'click'](); await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await h.press('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  const st = await probe(); assert.deepEqual([st.mode, st.dictoRcp, st.rcp], ['shells', true, false], `${dev}: back after reload`);
  await h.press(`${P} [data-wq-dicto-rcp]`); await page.waitForTimeout(500);   // leave it off
  checks++;
  assert.deepEqual(h.errors, [], `${dev} Queens: console errors`); checks++;
  await h.ctx.close();
}
await b.close();
console.log(`dicto-rcp: ${checks} checks passed`);
