// The stage slider keeps one view from White to Red (DICTO 2026-11-16, the premise audit's one geometry fault), through the real UI on
// both doors (DOORS): desktop (1280×900, a mouse drag) and phone (390×844, a touch drag). In the Shadow view, for each of the four named
// views (From = vertex-, edge-, face-, cell-first), the stage slider is dragged from 1 to 6 and back: at every position the 4D view
// direction and frame stay the White Queen's for that name, so the projected place of one fixed 4D point, (2, 0, 0, 0), never moves
// (before the fix it jumped at 6 by 22.2° or 10.8°). At 6 the Red Queen's outline has the exact corner count of her own direction with
// that axis (the White Queen's vertex-, edge-, face-, cell-first are her cell-, face-, edge-, vertex-first: 80, 160, 180, 158; her own
// atlas 158 / 180 / 160 / 80), and the caption names both. The White | Red buttons still show her along her own directions (158 at
// vertex-first). No console errors. Screenshots at stages 5 and 6 ($SHOTS, default /tmp/queen-slider-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import RQ from '../../src/app/red-queen-data.js';
import { WQ_DIRECTIONS as DIRS } from '../../src/app/world-white-queen.js';
import { UNIT_DIRECTIONS } from '../../src/app/white-queen-geometry.js';
import { WHITE_AS_RED } from '../../src/app/red-queen-geometry.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/queen-slider-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldwhiteQueen-panel';
const RED_ALONG_WHITE = { 'vertex-first': 80, 'edge-first': 160, 'face-first': 180, 'cell-first': 158 };   // the audit's exact outlines
const RED_OWN = { 'vertex-first': 158, 'edge-first': 180, 'face-first': 160, 'cell-first': 80 };
const REF = [2, 0, 0, 0];   // the White Queen's corner 0
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const close = (a, b, eps = 1e-9) => a.length === b.length && a.every((x, i) => Math.abs(x - b[i]) < eps);
const b = await chromium.launch();
let checks = 0;
const probe = (page) => page.evaluate(() => window.__whiteQueenProbe());
const DEVICES = { desktop: { viewport: { width: 1280, height: 900 } }, phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true } };
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, opts] of Object.entries(DEVICES).filter(([d]) => (process.env.DEVICES ?? 'desktop,phone').split(',').includes(d))) {
    const page = await b.newPage(opts), tag = `${door}-${dev}`, touch = !!opts.hasTouch;
    const cdp = touch ? await page.context().newCDPSession(page) : null;
    const errors = []; page.on('pageerror', (e) => errors.push(`${String(e)} @ ${(e.stack ?? '').split('\n').slice(1, 4).join(' | ')} [stage ${lastStage}]`)); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    const tap = (sel) => (touch ? page.tap(sel) : page.click(sel));
    await page.goto(`${BASE}/index.html?probe&site=${door}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    await page.locator('[data-action="tool:whiteQueenWorld"]').first()[touch ? 'tap' : 'click'](); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    if ((await probe(page)).queen !== 'white') { await tap(`${P} [data-wq-queen="white"]`); await page.waitForTimeout(600); }
    if ((await probe(page)).mode !== 'shadow') { await tap(`${P} [data-wq-mode="shadow"]`); await page.waitForTimeout(600); }
    const slider = page.locator(`${P} .wq-stage-row input`);
    // the thumb's x for a stage k (0..6), and a real drag between two stages: mouse on desktop, touch (CDP touch events) on the phone
    const xAt = async (k) => { const bx = await slider.boundingBox(); const th = Math.min(40, bx.height); return { x: bx.x + th / 2 + (k / 6) * (bx.width - th), y: bx.y + bx.height / 2 }; };
    async function drag(from, to, onStep = async () => {}) {
      const a = await xAt(from), z = await xAt(to), n = Math.abs(to - from) * 6;
      if (touch) await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: a.x, y: a.y }] });
      else { await page.mouse.move(a.x, a.y); await page.mouse.down(); }
      for (let i = 1; i <= n; i++) {
        const x = a.x + ((z.x - a.x) * i) / n;
        if (touch) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: a.y }] }); else await page.mouse.move(x, a.y);
        await page.waitForTimeout(120); await onStep();
      }
      if (touch) await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); else await page.mouse.up();
      await page.waitForTimeout(500);
    }
    const stageNo = async () => Number(await slider.inputValue());
    for (const k of DIRS) {
      // the named view: From k, at its stop
      await tap(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(700);
      let st = await probe(page);
      if (st.stop !== k) { await tap(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(700); st = await probe(page); }
      assert.equal(st.stop, k, `${tag}: at ${k}`);
      const want = UNIT_DIRECTIONS[DIRS.indexOf(k)];
      await drag(await stageNo(), 1); assert.equal(await stageNo(), 1, `${tag} ${k}: dragged to stage 1`);
      st = await probe(page); const ref0 = st.frame.map((f) => dot(REF, f));
      const seen = new Set();
      const check = async () => {
        const s = await probe(page), n = await stageNo(); seen.add(n);
        assert.ok(close(s.dir, want), `${tag} ${k} stage ${n}: the 4D direction stays the White Queen's ${k}`);
        assert.ok(close(s.frame.map((f) => dot(REF, f)), ref0), `${tag} ${k} stage ${n}: the reference corner does not move`);
        checks++;
      };
      await drag(1, 6, check);
      assert.deepEqual([...seen].sort(), [1, 2, 3, 4, 5, 6], `${tag} ${k}: every stage passed`);
      st = await probe(page);
      assert.equal(st.queen, 'red'); assert.equal(st.alongWhite, true); assert.equal(st.stop, k);
      assert.equal(st.vertices, RED_ALONG_WHITE[k], `${tag} ${k}: the Red Queen's outline at 6`);
      assert.equal(st.vertices, RQ.shadows[WHITE_AS_RED[k]].V, `${tag} ${k}: = her own ${WHITE_AS_RED[k]} (atlas)`);
      const cap = await page.locator(`${P} .ch-param-caption`).textContent();
      assert.ok(cap.includes('(White Queen)') && cap.includes('(Red Queen)'), `${tag} ${k}: the caption names both (${cap})`); checks++;
      if (k === 'vertex-first') {
        await page.screenshot({ path: `${SH}/${tag}-stage6.png` });
        await drag(6, 5); assert.equal(await stageNo(), 5); await page.screenshot({ path: `${SH}/${tag}-stage5.png` });
        await drag(5, 6); assert.equal(await stageNo(), 6);
      }
      seen.clear(); await drag(6, 1, check); assert.ok(seen.has(5) && seen.has(1), `${tag} ${k}: back down`);
      await drag(1, 0); assert.equal((await probe(page)).queen, 'white');
    }
    // the White | Red buttons: the Red Queen along her own directions, as before
    await tap(`${P} [data-wq-queen="red"]`); await page.waitForTimeout(1200);
    await tap(`${P} [data-wq-from="vertex-first"]`); await page.waitForTimeout(800);
    let st = await probe(page);
    assert.equal(st.queen, 'red'); assert.equal(st.alongWhite, false); assert.equal(st.stop, 'vertex-first'); assert.equal(st.vertices, RED_OWN['vertex-first'], `${tag}: Red button, her own vertex-first`); checks++;
    await tap(`${P} [data-wq-queen="white"]`); await page.waitForTimeout(800);
    st = await probe(page); assert.equal(st.queen, 'white');
    assert.deepEqual(errors, [], `${tag}: console`); await page.close();
  }
}
await b.close(); console.log(`queen-slider: ${checks} checks ok`);
