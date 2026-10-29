// The Red Queen switch (DICTO 2026-10-29, paper #65) in the White Queen world, through the real UI, touch, phone (390×844) and iPad
// (820×1180), on both doors (DOORS): the White | Red row on top, big enough to touch; Red shows the 120-cell: each From button's
// shadow with the atlas's corners and faces by sides (tests via src/app/red-queen-data.js); the Slice slider stopping at exactly the
// atlas's 31 / 45 / 33 / 15 stops; Shells building the nine cell layers 1, 12, 20, 12, 30, 12, 20, 12, 1 with the gold core and its
// link to the pentagonal pyramids; Whole; Halves balanced. White again gives back the White Queen as she was (vertex-first 42
// vertices). The queen row on one line in every language. No console errors. Screenshots ($SHOTS, default /tmp/rq-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import RQ from '../../src/app/red-queen-data.js';
import { WQ_DIRECTIONS as DIRS } from '../../src/app/world-white-queen.js';
import { LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/rq-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldwhiteQueen-panel';
const b = await chromium.launch();
let checks = 0;
const probe = (page) => page.evaluate(() => window.__whiteQueenProbe());
const sizes = (fs) => Object.fromEntries(Object.entries(fs).map(([k, v]) => [k, v]));
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(`${BASE}/index.html?probe&site=${door}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    await page.locator('[data-action="tool:whiteQueenWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    // the queen row: two touchable buttons, White on at first
    for (const q of ['white', 'red']) { const bx = await page.locator(`${P} [data-wq-queen="${q}"]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${q} touchable`); }
    assert.equal(await page.getAttribute(`${P} [data-wq-queen="white"]`, 'aria-pressed'), 'true'); checks++;
    await page.tap(`${P} [data-wq-queen="red"]`); await page.waitForTimeout(1500);
    let st = await probe(page);
    assert.equal(st.queen, 'red'); assert.equal(st.edges, 1200, `${tag}: 1200 edges`); checks++;
    // Shadow: every From button's view has the atlas's corners and faces by sides
    for (const k of DIRS) {
      if (k === 'cell-first') { await page.tap(`${P} [data-wq-from="vertex-first"]`); await page.waitForTimeout(400); await page.tap(`${P} [data-wq-to="cell-first"]`); }
      else await page.tap(`${P} [data-wq-from="${k}"]`);
      await page.waitForTimeout(900);
      st = await probe(page);
      assert.equal(st.stop, k, `${tag}: at ${k}`);
      assert.equal(st.vertices, RQ.shadows[k].V, `${tag} ${k}: corners`); assert.equal(st.faces, RQ.shadows[k].F, `${tag} ${k}: faces`);
      assert.deepEqual(sizes(st.faceSizes), RQ.shadows[k].face_sizes, `${tag} ${k}: faces by sides`); checks++;
      if (dev === 'phone' || k === 'vertex-first') await page.screenshot({ path: `${SH}/${tag}-shadow-${k}.png` });
    }
    // Halves: front and back balanced
    await page.tap(`${P} [data-wq-halves]`); await page.waitForTimeout(900);
    st = await probe(page); assert.equal(st.halves.front, st.halves.back, `${tag}: halves`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-halves.png` });
    await page.tap(`${P} [data-wq-halves]`); await page.waitForTimeout(400);
    // Slice: the slider stops at exactly the atlas's stops in each direction
    await page.tap(`${P} [data-wq-mode="slice"]`); await page.waitForTimeout(900);
    for (const k of DIRS) {
      await page.tap(`${P} [data-wq-slice="${k}"]`); await page.waitForTimeout(700);
      st = await probe(page); assert.equal(st.stops, RQ.slice_patterns[k], `${tag} ${k}: stops`); checks++;
    }
    await page.tap(`${P} [data-wq-slice="vertex-first"]`); await page.waitForTimeout(800);
    const first = RQ.slices.find((s) => s.direction === 'vertex-first');
    st = await probe(page); assert.equal(st.V, first.V, `${tag}: vertex-first centre slice corners`); assert.deepEqual(st.faceSizes, first.face_sizes); checks++;
    assert.ok(!/Humpty|Shadow-17/.test(await caption()), `${tag}: no White Queen names on the Red Queen`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-slice-vertex-centre.png` });
    // Shells: the nine cell layers
    await page.tap(`${P} [data-wq-mode="shells"]`); await page.waitForTimeout(1200);
    st = await probe(page); assert.equal(st.total, 9); assert.equal(st.shells, 1); assert.equal(st.newest.pieces, 1);
    assert.ok(await page.locator(`${P} [data-wq-link]`).isVisible(), `${tag}: core link`);
    assert.match(await page.locator(`${P} [data-wq-link]`).textContent(), /pentagonal pyramids/); checks++;
    const slider = page.locator(`${P} .wq-shells-row input`), got = [];
    for (let n = 1; n <= 9; n++) { await slider.fill(String(n)); await page.waitForTimeout(500); got.push((await probe(page)).newest.pieces); }
    assert.deepEqual(got, [1, 12, 20, 12, 30, 12, 20, 12, 1], `${tag}: nine layers`); checks++;
    await slider.fill('5'); await page.waitForTimeout(800); await page.screenshot({ path: `${SH}/${tag}-layers-5.png` });
    await page.tap(`${P} [data-wq-whole]`); await page.waitForTimeout(1500);
    st = await probe(page); assert.equal(st.whole, true); assert.equal(st.wholeKept.length, 9); checks++;
    await page.screenshot({ path: `${SH}/${tag}-whole.png` });
    await page.tap(`${P} [data-wq-whole]`); await page.waitForTimeout(500);
    // White again: the White Queen as she was
    await page.tap(`${P} [data-wq-mode="shadow"]`); await page.waitForTimeout(500);
    await page.tap(`${P} [data-wq-queen="white"]`); await page.waitForTimeout(1200);
    await page.tap(`${P} [data-wq-from="vertex-first"]`); await page.waitForTimeout(800);
    st = await probe(page); assert.deepEqual([st.queen, st.vertices, st.triangles, st.edges], ['white', 42, 80, 720], `${tag}: White Queen back`);
    assert.equal(await page.textContent('#hud-world-title'), 'The White Queen 600-cell', `${tag}: title back`); checks++;
    if (dev === 'phone' && door === 'kaleidohedra') {
      // the queen row on one line in every language
      for (const L of LANG_ORDER) {
        await page.selectOption('#hud-tools .lang-btn select', L); await page.waitForTimeout(300);
        const ys = await page.$$eval(`${P} [data-wq-queen]`, (els) => els.map((e) => Math.round(e.getBoundingClientRect().top)));
        assert.equal(new Set(ys).size, 1, `${L}: queen row on one line`);
        if (L === 'ja') await page.screenshot({ path: `${SH}/phone-ja.png` });
      }
      await page.selectOption('#hud-tools .lang-btn select', 'en');
      checks++;
    }
    assert.deepEqual(errors, [], `${tag}: no console errors`); checks++;
    await page.close();
    console.log(`${tag}: ok`);
  }
}
await b.close();
console.log(`red queen: ${checks} checks passed`);
