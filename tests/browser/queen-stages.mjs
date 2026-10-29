// The stage slider in the White Queen world (DICTO 2026-10-30), through the real UI, touch, phone (390×844) and iPad (820×1180), both
// doors (DOORS): Shadow view, the slider from White to Red through the five stages: each stage shows its classical corners and edges
// (STAGE_FACTS) and the title names it; at a stage the queen buttons are off and Halves is hidden; Red at the end is the Red Queen
// (1200 edges), White again the White Queen; a mode button at a stage returns to a queen. ?open=whitequeen:t12 opens the midpoint.
// No console errors. Screenshots ($SHOTS, default /tmp/stage-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { STAGE_KEYS, STAGE_FACTS } from '../../src/app/queen-stages-geometry.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/stage-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldwhiteQueen-panel';
const b = await chromium.launch();
let checks = 0;
const probe = (page) => page.evaluate(() => window.__whiteQueenProbe());
const setStage = async (page, k) => { await page.locator(`${P} .wq-stage-row input`).evaluate((el, v) => { el.value = String(v); el.dispatchEvent(new Event('input', { bubbles: true })); }, k); await page.waitForTimeout(700); };
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
    if ((await probe(page)).queen !== 'white') { await page.tap(`${P} [data-wq-queen="white"]`); await page.waitForTimeout(600); }
    if ((await probe(page)).mode !== 'shadow') { await page.tap(`${P} [data-wq-mode="shadow"]`); await page.waitForTimeout(600); }
    const box = await page.locator(`${P} .wq-stage-row input`).boundingBox(); assert.ok(box.width >= 200 && box.height >= 20, `${tag}: big slider`); checks++;
    for (let k = 1; k <= 5; k++) {
      await setStage(page, k); const st = await probe(page), f = STAGE_FACTS[STAGE_KEYS[k]];
      assert.equal(st.stage, STAGE_KEYS[k]); assert.equal(st.corners, f.V, `${tag} ${st.stage} corners`); assert.equal(st.edges, f.E, `${tag} ${st.stage} edges`);
      assert.match(st.title, /cell/); assert.ok(await page.locator(`${P} .wq-halves-row`).isHidden(), `${tag}: no Halves at a stage`);
      assert.equal(await page.locator(`${P} [data-wq-queen].active`).count(), 0); checks++;
      if (k === 3) await page.screenshot({ path: `${SH}/${tag}-midpoint.png` });
    }
    await setStage(page, 6); let st = await probe(page); assert.equal(st.queen, 'red'); assert.equal(st.edges, 1200); checks++;
    await setStage(page, 0); st = await probe(page); assert.equal(st.queen, 'white'); assert.equal(st.edges, 720); checks++;
    await setStage(page, 3); await page.tap(`${P} [data-wq-mode="slice"]`); await page.waitForTimeout(800);
    st = await probe(page); assert.equal(st.mode, 'slice'); assert.equal(st.queen, 'white'); checks++;
    await page.tap(`${P} [data-wq-mode="shadow"]`); await page.waitForTimeout(600); assert.equal((await probe(page)).stage, 'white'); checks++;
    assert.deepEqual(errors, [], `${tag}: console`); await page.close();
  }
}
const page = await b.newPage({ viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true });
await page.goto(`${BASE}/index.html?probe&site=kaleidohedra&open=whitequeen:t12`);
await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
const st = await probe(page); assert.equal(st.stage, 't12'); assert.equal(st.corners, 3600); checks++;
await b.close(); console.log(`queen-stages: ${checks} checks ok`);
