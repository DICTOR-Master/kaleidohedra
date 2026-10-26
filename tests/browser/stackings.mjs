// The Stackings World (DICTO 2026-10-26), through the real UI, touch, phone (390×844) and iPad (820×1180), on the Kaleidohedra and
// Rhombiverse doors (DOORS): right after the Global Web of Bonds in DICTO's list; the six polytype buttons (big enough to touch); one
// slider snapping to every stop of #57's walk (the pieces drawn = stackingColumn, the caption naming the stop and the census); the
// ?open=stackings:<polytype> link. No console errors. Then screenshots ($SHOTS, default /tmp/stackings-shots) at TV 1280×720,
// iPad 820×1050 and phone 390×760 of 4H at λ = 0 (Janus pieces in gold and platinum).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { STACKING_KINDS, STACKING_STOPS, STACKING_VIEWS, stackingColumn, wordFromTypes } from '../../src/app/world-stackings.js';
import { PRESETS, layerTypes } from '../../src/app/stackings-geometry.js';
import { t } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/stackings-shots';
mkdirSync(SH, { recursive: true });
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
const P = '#worldstackings-panel';
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
  return errors;
}
const sizeOf = (k) => Math.min(2, typeof STACKING_VIEWS[k].maxSize === 'function' ? STACKING_VIEWS[k].maxSize() : STACKING_VIEWS[k].maxSize);
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:stackingsWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.deepEqual(worlds.slice(0, 3), ['tool:dictonicWorld', 'tool:globalWebWorld', 'tool:stackingsWorld'], `${tag}: after the Global Web`); checks++;
    await page.locator('[data-action="tool:stackingsWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    const probe = () => page.evaluate(() => window.__stackingsProbe());
    const slide = async (u) => { await page.locator(`${P} .ch-param-row input`).fill(String(u)); await page.waitForTimeout(900); };
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    for (const k of STACKING_KINDS) { const bx = await page.locator(`${P} [data-chains-kind="${k}"]`).boundingBox(); assert.ok(bx && bx.height >= 30, `${tag}: ${k} button`); }
    checks++;
    for (const k of ['3C', '4H']) {
      if ((await probe()).kind !== k) { await page.tap(`${P} [data-chains-kind="${k}"]`); await page.waitForTimeout(1200); }
      let st = await probe(); assert.equal(st.kind, k);
      for (const s of STACKING_STOPS) {
        await slide(Math.max(0, Math.min(1000, s.u + (s.u < 1000 ? 9 : -9)))); st = await probe();
        assert.equal(st.param.u, s.u, `${tag}: ${k} snaps to ${s.key}`); assert.equal(st.param.value, s.v);
        assert.deepEqual(st.drawn, count(stackingColumn(PRESETS[k], Math.min(st.size ?? 2, sizeOf(k)), s.v)), `${tag}: ${k} ${s.key} pieces`);
        assert.ok((await caption()).startsWith(t(`stackings.stop.${s.key}`, 'en')), `${tag}: ${k} ${s.key} caption`); checks++;
      }
    }
    // phase 2: flip layer 1 of 4H (c → h), the column follows the new word; reset; tap a piece for its volume
    const u0 = STACKING_STOPS.find((x) => x.key === 's2').u + 100; await slide(u0);
    let st = await probe(); const lam = st.param.value;
    const chip = page.locator(`${P} [data-stk-layer="0"]`), cb = await chip.boundingBox();
    assert.ok(cb && cb.height >= 30, `${tag}: layer chip big enough to touch`);
    await chip.tap(); await page.waitForTimeout(1500);
    const flipped = wordFromTypes(layerTypes('ABAC').map((x, j) => (j === 0 ? (x === 'c' ? 'h' : 'c') : x)));
    assert.equal(await page.locator(`${P} .stk-chips [data-stk-layer]`).count(), flipped.length, `${tag}: one chip per layer of ${flipped}`);
    st = await probe(); assert.deepEqual(st.drawn, count(stackingColumn(flipped, 1, lam)), `${tag}: flipped column`);
    assert.match(await caption(), new RegExp(layerTypes(flipped).join('')), `${tag}: caption shows the new h/c sequence`); checks++;
    await page.tap(`${P} [data-stk-reset]`); await page.waitForTimeout(1200);
    st = await probe(); assert.deepEqual(st.drawn, count(stackingColumn('ABAC', 1, lam)), `${tag}: reset`); checks++;
    const f = await page.evaluate(() => window.__frameProbe());
    let picked = false;
    for (const [dx, dy] of [[0, 0], [0, 0.2], [0, -0.2], [0.05, 0.4], [-0.05, -0.4], [0.1, 0.1], [-0.1, -0.1], [0, 0.6], [0, -0.6]]) {
      await page.touchscreen.tap(f.cx + dx * f.r, f.cy + dy * f.r); await page.waitForTimeout(600);
      if ((await probe()).drawn.stkSel === 1) { picked = true; break; }
    }
    assert.ok(picked, `${tag}: a tapped piece is picked`);
    assert.match(await page.locator(`${P} .stk-info`).textContent(), /volume \d/, `${tag}: picked piece's volume`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
for (const [dev, viewport] of Object.entries({ tv: { width: 1280, height: 720 }, ipad: { width: 820, height: 1050 }, phone: { width: 390, height: 760 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'tv', isMobile: dev !== 'tv' });
  const errors = await open(page, '&site=kaleidohedra&open=stackings:4H');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1800);
  const st = await page.evaluate(() => window.__stackingsProbe());
  assert.equal(st.kind, '4H', '?open=stackings:4H'); assert.equal(st.param.value, 0);
  await page.screenshot({ path: `${SH}/${dev}-4H-lambda0.png` });
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`stackings OK: ${checks} checks`);
