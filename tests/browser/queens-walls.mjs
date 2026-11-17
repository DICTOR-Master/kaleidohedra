// The Queens' walls (DICTO 2026-11-16), through the real UI on both doors (DOORS), phone (390×844, touch) and desktop (1280×900, mouse):
// opened from DICTO's list (Book Ten, beside the White Queen); Sheets: 60 sheets of 20 triangles (White), Red: the same 60 sheets of 12
// pentagons; Apart to 0 puts every piece back (nothing moved), up moves them out; Cells: 120 dodecahedral pyramids (Red), 600
// tetrahedral pyramids (White); a direction button; the controls big enough to touch, no arrows; ?open=queenswalls:red opens the Red
// Queen. No console errors. Screenshots ($SHOTS, default /tmp/queens-walls-shots): White Sheets apart, Red Sheets apart, White Cells
// half apart, phone and desktop.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { unfold } from './menu-unfold.mjs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/queens-walls-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldqueensWalls-panel';
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }, desktop: { viewport: { width: 1280, height: 900 } } };
const b = await chromium.launch();
let checks = 0;
const probe = (page) => page.evaluate(() => window.__queensWallsProbe());
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, opts] of Object.entries(DEVICES)) {
    const page = await b.newPage(opts), tag = `${door}-${dev}`, touch = !!opts.hasTouch;
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    const tap = (sel) => (touch ? page.tap(sel) : page.click(sel));
    await page.goto(`${BASE}/index.html?probe&site=${door}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:queensWallsWorld"]').count())) await tap('.dim-wizard-card-btn[data-dim="3D"]'); await unfold(page, 'tool:queensWallsWorld');
    await page.waitForTimeout(500);
    // in DICTO's list right after the White Queen (Book Ten)
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action));
    assert.equal(worlds[worlds.indexOf('tool:whiteQueenWorld') + 1], 'tool:queensWallsWorld', `${tag}: after the White Queen`); checks++;
    await page.locator('[data-action="tool:queensWallsWorld"]').first()[touch ? 'tap' : 'click'](); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    // the controls: big touch targets, no arrows
    for (const sel of ['[data-qw-queen="white"]', '[data-qw-queen="red"]', '[data-qw-mode="cells"]', '[data-qw-mode="sheets"]']) {
      const bx = await page.locator(`${P} ${sel}`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${sel} touchable`);
    }
    const sb = await page.locator(`${P} .qw-apart-row input`).boundingBox(); assert.ok(sb.width >= 200, `${tag}: long Apart slider`);
    assert.ok(!/[◀▶]/.test(await page.locator(P).textContent()), `${tag}: no arrows`); checks++;
    const apart = async (v) => { await page.locator(`${P} .qw-apart-row input`).fill(String(v)); await page.waitForTimeout(500); };
    let st = await probe(page);
    if (st.queen !== 'white') { await tap(`${P} [data-qw-queen="white"]`); await page.waitForTimeout(800); }
    if ((await probe(page)).mode !== 'sheets') { await tap(`${P} [data-qw-mode="sheets"]`); await page.waitForTimeout(800); }
    // White sheets
    await apart(1000); st = await probe(page);
    assert.deepEqual([st.queen, st.mode, st.pieces, st.faces, st.facesPerPiece, st.sides], ['white', 'sheets', 60, 1200, [20], [3]], `${tag}: White sheets`);
    assert.ok(st.moved > 0.01, `${tag}: apart moves`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-white-sheets-apart.png` });
    await apart(0); st = await probe(page); assert.ok(st.moved < 1e-6, `${tag}: at 0 nothing moved`); checks++;
    // Red: the same 60 sheets, pentagons
    await apart(1000);
    await tap(`${P} [data-qw-queen="red"]`); await page.waitForTimeout(1000); st = await probe(page);
    assert.deepEqual([st.queen, st.mode, st.pieces, st.faces, st.facesPerPiece, st.sides], ['red', 'sheets', 60, 720, [12], [5]], `${tag}: Red sheets`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-red-sheets-apart.png` });
    // Cells
    await tap(`${P} [data-qw-mode="cells"]`); await page.waitForTimeout(1000); st = await probe(page);
    assert.deepEqual([st.mode, st.pieces, st.facesPerPiece, st.sides], ['cells', 120, [12], [5]], `${tag}: Red cells`); checks++;
    await tap(`${P} [data-qw-queen="white"]`); await page.waitForTimeout(1500); await apart(500); st = await probe(page);
    assert.deepEqual([st.queen, st.mode, st.pieces, st.facesPerPiece, st.sides, st.apart], ['white', 'cells', 600, [4], [3], 500], `${tag}: White cells`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-white-cells-half.png` });
    await tap(`${P} [data-qw-dir="edge-first"]`); await page.waitForTimeout(1200); st = await probe(page);
    assert.equal(st.dir, 'edge-first'); assert.equal(st.pieces, 600); checks++;
    assert.match(await page.locator(`${P} .ch-param-caption`).textContent(), /600 tetrahedral pyramids/); checks++;
    assert.deepEqual(errors, [], `${tag}: console`); await page.close();
  }
}
const page = await b.newPage({ viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true });
await page.goto(`${BASE}/index.html?probe&site=kaleidohedra&open=queenswalls:red`);
await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
assert.equal((await probe(page)).queen, 'red'); checks++;
await b.close(); console.log(`queens-walls: ${checks} checks ok`);
