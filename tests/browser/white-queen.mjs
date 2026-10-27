// The White Queen 600-cell (DICTO 2026-10-27, paper #63), through the real UI, touch, phone (390×844) and iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors (DOORS): right after the Icosaxes Bloom in DICTO's list; four direction buttons (big enough to touch)
// each jumping to its stop with the hull counts of #62/#63; the slider long, low and snapping to the four stops, an in-between position
// captioned "Edge first → Face first"; ?open=whitequeen:<vertex|edge|face|cell>. No console errors. Screenshots ($SHOTS, default /tmp/wq-shots) on a
// phone (390×844) and a desktop (1280×800) at the four stops and halfway from edge-first to face-first.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { WQ_STOPS } from '../../src/app/world-white-queen.js';
import { t } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/wq-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldwhiteQueen-panel';
const EXPECT = { 'vertex-first': [42, 80, 0], 'edge-first': [52, 60, 20], 'face-first': [56, 84, 12], 'cell-first': [44, 72, 6] };
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  return errors;
}
const probe = (page) => page.evaluate(() => window.__whiteQueenProbe());
const counts = (st) => [st.vertices, st.triangles, st.quads];
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[worlds.indexOf('tool:bloomWorld') + 1], 'tool:whiteQueenWorld', `${tag}: right after the Icosaxes Bloom`); checks++;
    await page.locator('[data-action="tool:whiteQueenWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    for (const { key } of WQ_STOPS) {
      const btn = page.locator(`${P} [data-wq-dir="${key}"]`), bx = await btn.boundingBox();
      assert.ok(bx && bx.height >= 30, `${tag}: ${key} button touchable`);
      await btn.tap(); await page.waitForTimeout(500);
      const st = await probe(page);
      assert.equal(st.stop, key, `${tag}: ${key} button`); assert.deepEqual(counts(st), EXPECT[key], `${tag}: ${key} counts`); assert.equal(st.edges, 720);
      assert.ok((await caption()).startsWith(t(`wq.dir.${key}`, 'en')), `${tag}: ${key} caption`);
      assert.ok((await caption()).includes(`${EXPECT[key][0]} vertices`), `${tag}: ${key} caption counts`); checks++;
    }
    const slider = page.locator(`${P} .wq-param-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`); checks++;
    for (const { key, u } of WQ_STOPS) {
      await slider.fill(String(Math.max(0, Math.min(3000, u + (u < 3000 ? 25 : -25))))); await page.waitForTimeout(400);
      const st = await probe(page); assert.equal(st.u, u, `${tag}: snaps to ${key}`); assert.deepEqual(counts(st), EXPECT[key]); checks++;
    }
    await slider.fill('1500'); await page.waitForTimeout(400);
    let st = await probe(page); assert.equal(st.stop, null); assert.equal(st.u, 1500);
    assert.ok((await caption()).startsWith(t('wq.between', 'en', { a: t('wq.dir.edge-first', 'en'), b: t('wq.dir.face-first', 'en') })), `${tag}: between`); checks++;
    // nothing unnecessary: the app's lattice-view button is hidden in this world
    assert.ok(!(await page.locator('#hud-quick-lattice-view').isVisible()), `${tag}: no lattice view`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
for (const [short, key] of [['vertex', 'vertex-first'], ['cell', 'cell-first']]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=whitequeen:${short}`);
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  const st = await probe(page); assert.equal(st.stop, key, `?open=whitequeen:${short}`); assert.deepEqual(counts(st), EXPECT[key]);
  assert.deepEqual(errors, [], `?open=whitequeen:${short}: console errors`); checks++;
  await page.close();
}
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=whitequeen:vertex');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  for (const [name, u] of [...WQ_STOPS.map((s) => [s.key, s.u]), ['between-edge-face', 1500]]) {
    await page.locator(`${P} .wq-param-row input`).fill(String(u)); await page.waitForTimeout(700);
    await page.screenshot({ path: `${SH}/${dev}-${name}.png` });
  }
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`white-queen OK: ${checks} checks`);
