// The White Queen 600-cell (DICTO 2026-10-27, paper #63), through the real UI, touch, phone (390×844) and iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors (DOORS): right after the Icosaxes Bloom in DICTO's list; two rows of four direction buttons (From,
// To; big enough to touch, the To matching From hidden), default vertex-first → cell-first; each From button jumps to its start and each
// To button to its end with the hull counts of #62/#63, all six turnings; the slider long, low and snapping at both ends; an in-between
// position captioned "From → To"; ?open=whitequeen:<vertex|edge|face|cell>. No console errors. Screenshots ($SHOTS, default
// /tmp/wq-shots) on a phone (390×844) and a desktop (1280×800) at the four main directions and halfway from vertex-first to cell-first.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { WQ_DIRECTIONS as DIRS } from '../../src/app/world-white-queen.js';
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
    let st = await probe(page);
    assert.deepEqual([st.from, st.to, st.u], ['vertex-first', 'cell-first', 0], `${tag}: default turning`);
    assert.ok(!(await page.locator(`${P} [data-wq-to="vertex-first"]`).isVisible()), `${tag}: To hides From's direction`); checks++;
    for (const end of ['from', 'to']) for (const k of DIRS) {
      const btn = page.locator(`${P} [data-wq-${end}="${k}"]`);
      if (!(await btn.isVisible())) continue;
      const bx = await btn.boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${end} ${k} touchable`);
    }
    checks++;
    const tapFrom = async (k) => { await page.tap(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(350); };
    const tapTo = async (k) => { await page.tap(`${P} [data-wq-to="${k}"]`); await page.waitForTimeout(350); };
    const turnings = DIRS.flatMap((a, i) => DIRS.slice(i + 1).map((b) => [a, b]));
    assert.equal(turnings.length, 6);
    for (const [a, z] of turnings) {
      await tapFrom(a); st = await probe(page);
      assert.deepEqual([st.from, st.u, st.stop], [a, 0, a], `${tag}: From ${a}`); assert.deepEqual(counts(st), EXPECT[a], `${tag}: ${a} counts`);
      assert.ok((await caption()).startsWith(`${t(`wq.dir.${a}`, 'en')} · ${EXPECT[a][0]} vertices`), `${tag}: ${a} caption`);
      await tapTo(z); st = await probe(page);
      assert.deepEqual([st.from, st.to, st.u, st.stop], [a, z, 1000, z], `${tag}: ${a} → To ${z}`); assert.deepEqual(counts(st), EXPECT[z], `${tag}: ${z} counts`);
      assert.equal(st.edges, 720);
      assert.ok((await caption()).startsWith(`${t(`wq.dir.${z}`, 'en')} · ${EXPECT[z][0]} vertices`), `${tag}: ${z} caption`); checks++;
    }
    // From = the current To swaps the two
    await tapFrom('cell-first'); await tapTo('vertex-first'); await tapFrom('vertex-first'); st = await probe(page);
    assert.deepEqual([st.from, st.to], ['vertex-first', 'cell-first'], `${tag}: swap`); checks++;
    const slider = page.locator(`${P} .wq-param-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`); checks++;
    for (const [v, u, k] of [[25, 0, 'vertex-first'], [975, 1000, 'cell-first']]) {
      await slider.fill(String(v)); await page.waitForTimeout(400);
      st = await probe(page); assert.equal(st.u, u, `${tag}: snaps to ${k}`); assert.deepEqual(counts(st), EXPECT[k]); checks++;
    }
    await slider.fill('500'); await page.waitForTimeout(400);
    st = await probe(page); assert.equal(st.stop, null); assert.equal(st.u, 500);
    assert.ok((await caption()).startsWith(t('wq.between', 'en', { a: t('wq.dir.vertex-first', 'en'), b: t('wq.dir.cell-first', 'en') })), `${tag}: between`); checks++;
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
  for (const k of DIRS) {
    await page.click(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(700);
    await page.screenshot({ path: `${SH}/${dev}-${k}.png` });
  }
  await page.click(`${P} [data-wq-from="vertex-first"]`); await page.click(`${P} [data-wq-to="cell-first"]`);
  await page.locator(`${P} .wq-param-row input`).fill('500'); await page.waitForTimeout(700);
  await page.screenshot({ path: `${SH}/${dev}-between-vertex-cell.png` });
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`white-queen OK: ${checks} checks`);
