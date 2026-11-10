// The Bitruncated 600-cell (DICTO 2026-11-10; src/app/world-bitrunc.js), through the real UI, touch, phone (390×844) and iPad
// (820×1180), on the Kaleidohedra and Rhombiverse doors (DOORS): right after DICTONIC in DICTO's list; it opens on the Sweep along the
// generic direction at the swap nearest the middle, the four cells lit (two let go, two meet) and captioned "Swap k of 2166: …";
// the five direction buttons give each sweep's own stops and totals (generic 716 / 716 / 2166, cell-first 1782 = 1782); the big slider
// at the bottom stops at every corner height and gap middle; Play runs the sweep and stops on a touch. Shadow: From / To and one big
// slider snapping at both ends, 3600 corners and 7200 edges. Shells: 1, 32, 142, 242, 232, 71 cells, then Cut open. Each view shows
// only its own rows. ?open=bitrunc[:shadow|shells|whole|cell]; the Queens world's bitruncated stage links here (only there). Every one
// of the 7 languages at phone width: the rows fit on one line. No console errors. Screenshots ($SHOTS, default /tmp/bitrunc-shots) on
// a phone (390×844) and a desktop (1280×800): the Sweep at a swap, a cell-first batch, Shadow, Shells and Cut open.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import * as BT from '../../src/app/bitrunc-geometry.js';
import { middleSwap } from '../../src/app/world-bitrunc.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/bitrunc-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldbitrunc-panel', SIZES = [1, 32, 142, 242, 232, 71];
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  return errors;
}
const probe = (page) => page.evaluate(() => window.__bitruncProbe());
const leave = async (page) => { await page.waitForTimeout(500); if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]'); };
// a swap stop and a gap stop along the generic direction; a batch along cell-first
const G = BT.sweep('generic'), C = BT.sweep('cell-first');
const SWAP_K = G.stops.findIndex((s, k) => k > 1000 && s.level !== undefined && G.events[s.level].letGo.length === 1);
const GAP_K = SWAP_K + 1;
const BATCH_K = C.stops.findIndex((s) => s.level !== undefined && C.events[s.level].letGo.length > 1 && !C.events[s.level].born.length && !C.events[s.level].died.length);

for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:bitruncWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[worlds.indexOf('tool:dictonicWorld') + 1], 'tool:bitruncWorld', `${tag}: right after DICTONIC`); checks++;
    await page.locator('[data-action="tool:bitruncWorld"]').first().tap(); await leave(page);
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    const visible = (sel) => page.locator(`${P} ${sel}`).isVisible();
    // opens on the generic sweep at a swap near the middle, the four cells lit
    let st = await probe(page);
    assert.deepEqual([st.mode, st.dir, st.k, st.lit], ['sweep', 'generic', middleSwap('generic'), { letGo: 2, meet: 2 }], `${tag}: opens at a swap`);
    assert.deepEqual(st.totals, { levels: 3600, born: 716, died: 716, letGo: 2166, meet: 2166, swaps: 2166 });
    assert.ok((await caption()).startsWith(`${t('bt.dir.generic', 'en')} · Swap ${st.event.swapFrom + 1} of 2166: two cells let go, two meet`), `${tag}: swap caption ${await caption()}`);
    assert.ok((await caption()).includes(`${st.cells} cells in the slice (${st.ti} TI · ${st.tt} tt)`), `${tag}: live counts`);
    assert.equal(await page.locator(`${P} .bt-legend .bt-sw:not(.bt-off)`).count(), 4, `${tag}: legend with the swap's colours`); checks++;
    // no empty prompt pill above the panel
    assert.ok(!(await page.evaluate(() => { const e = document.getElementById('hud-prompt'); return e.classList.contains('visible') && !e.textContent.trim(); })), `${tag}: no empty prompt`);
    // only the Sweep's rows
    assert.ok(!(await visible('[data-bt-row="from"]')) && !(await visible('.bt-param-row')) && !(await visible('.bt-shells-row')) && !(await visible('.bt-whole-row')), `${tag}: only Sweep rows`);
    for (const k of BT.DIRECTIONS) { const bx = await page.locator(`${P} [data-bt-dir="${k}"]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${k} touchable`); }
    const slider = page.locator(`${P} .bt-sweep-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`); checks++;
    // the slider stops: a swap, then the gap after it
    await slider.fill(String(SWAP_K)); await page.waitForTimeout(300); st = await probe(page);
    assert.deepEqual([st.k, st.level, st.lit], [SWAP_K, G.stops[SWAP_K].level, { letGo: 2, meet: 2 }], `${tag}: swap stop`);
    assert.ok((await caption()).includes(`Swap ${G.events[G.stops[SWAP_K].level].swapFrom + 1} of 2166`));
    await slider.fill(String(GAP_K)); await page.waitForTimeout(300); st = await probe(page);
    assert.deepEqual([st.k, st.level, st.gap, st.lit], [GAP_K, null, G.stops[GAP_K].gap, { letGo: 0, meet: 0 }], `${tag}: gap stop`);
    assert.ok((await caption()).includes('between two corner heights'), `${tag}: gap caption`);
    assert.equal(await page.locator(`${P} .bt-legend .bt-sw:not(.bt-off)`).count(), 2, `${tag}: legend without the swap's colours`); checks++;
    // the five directions, each its own sweep
    for (const k of BT.DIRECTIONS) {
      await page.tap(`${P} [data-bt-dir="${k}"]`); await page.waitForTimeout(400); st = await probe(page);
      const sw = BT.sweep(k);
      assert.deepEqual([st.dir, st.stops, st.totals], [k, sw.stops.length, sw.totals], `${tag}: ${k} sweep`);
      assert.ok((await caption()).startsWith(k === 'generic' ? t('bt.dir.generic', 'en') : t(`wq.dir.${k}`, 'en')));
    }
    assert.equal(BT.sweep('cell-first').totals.letGo, 1782); checks++;
    await page.tap(`${P} [data-bt-dir="cell-first"]`); await slider.fill(String(BATCH_K)); await page.waitForTimeout(300); st = await probe(page);
    assert.ok(st.event.letGo > 1 && st.event.letGo === st.event.meet, `${tag}: a cell-first batch`);
    assert.ok((await caption()).includes(`${st.event.letGo} pairs let go`) && (await caption()).includes(`${st.event.meet} pairs meet`), `${tag}: batch caption ${await caption()}`); checks++;
    // Play runs the sweep; touching the slider stops it
    await page.tap(`${P} [data-bt-dir="generic"]`); await page.waitForTimeout(300);
    const k0 = (await probe(page)).k;
    const playBox = async () => (await page.locator(`${P} [data-bt-play]`).boundingBox()).y;
    await page.tap(`${P} [data-bt-play]`); const y0 = await playBox(); await page.waitForTimeout(1500); st = await probe(page);
    assert.ok(Math.abs((await playBox()) - y0) < 1, `${tag}: the Play button holds still while the sweep plays`);
    assert.ok(st.playing && st.k > k0, `${tag}: Play runs (${k0} → ${st.k})`);
    assert.equal((await page.locator(`${P} [data-bt-play]`).textContent()), t('bt.pause', 'en'));
    await page.tap(`${P} [data-bt-play]`); await page.waitForTimeout(300); const k1 = (await probe(page)).k; await page.waitForTimeout(500); st = await probe(page);
    assert.ok(!st.playing && st.k === k1, `${tag}: Pause holds`); checks++;
    // Shadow
    await page.tap(`${P} [data-bt-mode="shadow"]`); await page.waitForTimeout(800); st = await probe(page);
    assert.deepEqual([st.mode, st.from, st.to, st.u, st.corners, st.edges], ['shadow', 'vertex-first', 'cell-first', 0, 3600, 7200], `${tag}: Shadow`);
    assert.ok(!(await visible('[data-bt-row="dir"]')) && !(await visible('.bt-sweep-row')) && !(await visible('.bt-play-row')) && (await visible('[data-bt-row="from"]')), `${tag}: only Shadow rows`);
    assert.ok(!(await visible('[data-bt-to="vertex-first"]')), `${tag}: To hides From's direction`);
    assert.ok((await caption()).includes('3600 corners · 120 truncated icosahedra + 600 truncated tetrahedra'), `${tag}: shadow caption`);
    for (const k of ['edge-first', 'face-first']) { await page.tap(`${P} [data-bt-to="${k}"]`); await page.waitForTimeout(600); st = await probe(page); assert.deepEqual([st.to, st.u, st.stop], [k, 1000, k]); }
    const ps = page.locator(`${P} .bt-param-row input`);
    await ps.fill('20'); await page.waitForTimeout(500); assert.equal((await probe(page)).u, 0, `${tag}: snaps to the start`);
    await ps.fill('500'); await page.waitForTimeout(500); st = await probe(page); assert.equal(st.stop, null);
    assert.ok((await caption()).startsWith(t('wq.between', 'en', { a: t('wq.dir.vertex-first', 'en'), b: t('wq.dir.face-first', 'en') })), `${tag}: between`); checks++;
    // Shells
    await page.tap(`${P} [data-bt-mode="shells"]`); await page.waitForTimeout(600);
    assert.ok((await visible('.bt-shells-row')) && (await visible('.bt-whole-row')) && !(await visible('[data-bt-row="from"]')), `${tag}: only Shells rows`);
    const shl = page.locator(`${P} .bt-shells-row input`);
    for (let n = 1; n <= 6; n++) {
      await shl.fill(String(n)); await page.waitForTimeout(300); st = await probe(page);
      assert.equal(await page.locator(`${P} .bt-legend .bt-sw`).count(), 2, `${tag}: Shells legend, the two kinds`);
      assert.deepEqual([st.shells, st.total, st.newest.cells], [n, 6, SIZES[n - 1]], `${tag}: ${n} shells`);
      const cap = await caption();
      assert.ok(n === 1 ? cap === t('bt.shells.core', 'en') : cap.startsWith(`Shell ${n - 1}${n === 6 ? ', the last' : ''}: ${SIZES[n - 1]} cells`), `${tag}: shells caption ${cap}`);
    }
    checks++;
    await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(800); st = await probe(page);
    assert.ok(st.whole && st.wholeKept.length === 6 && st.wholeKept.every((n) => n > 0), `${tag}: Cut open ${JSON.stringify(st.wholeKept)}`);
    assert.ok(!(await visible('.bt-shells-row')), `${tag}: Cut open hides the shells slider`);
    assert.equal(await caption(), t('bt.shells.whole', 'en', { n: 6 }));
    await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(400); assert.ok(!(await probe(page)).whole); checks++;
    assert.ok(!(await page.locator('#hud-quick-lattice-view').isVisible()), `${tag}: no lattice view`);
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
// ?open=bitrunc[:…]
for (const [q, want] of [['bitrunc', { mode: 'sweep' }], ['bitrunc:shadow', { mode: 'shadow' }], ['bitrunc:shells', { mode: 'shells', whole: false }], ['bitrunc:whole', { mode: 'shells', whole: true }], ['bitrunc:cell', { mode: 'sweep', dir: 'cell-first' }]]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=${q}`);
  await page.waitForSelector(`${P}.visible`, { timeout: 20000 }); await page.waitForTimeout(1200);
  const st = await probe(page);
  for (const [k, v] of Object.entries(want)) assert.equal(st[k], v, `?open=${q}: ${k}`);
  assert.deepEqual(errors, [], `?open=${q}: console errors`); checks++;
  await page.close();
}
// the Queens world: one link, at the bitruncated stage only, opens this world
{
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=whitequeen:t12');
  await page.waitForSelector('#worldwhiteQueen-panel.visible'); await page.waitForTimeout(1500);
  const link = page.locator('#worldwhiteQueen-panel [data-wq-bitrunc]');
  assert.ok(await link.isVisible(), 'Queens world: link at the bitruncated stage');
  assert.equal(await link.textContent(), t('wq.link.bitrunc', 'en'));
  await page.screenshot({ path: `${SH}/phone-queens-link.png` });
  await page.locator('#worldwhiteQueen-panel .wq-stage-row input').fill('2'); await page.waitForTimeout(800);
  assert.ok(!(await link.isVisible()), 'Queens world: no link at another stage');
  await page.locator('#worldwhiteQueen-panel .wq-stage-row input').fill('3'); await page.waitForTimeout(800);
  await link.tap(); await leave(page);
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  assert.equal((await probe(page)).mode, 'sweep', 'the link opens the world');
  assert.ok(!(await page.locator('#worldwhiteQueen-panel').isVisible()), 'the Queens panel goes');
  assert.deepEqual(errors, [], 'Queens link: console errors'); checks++;
  await page.close();
}
// every language at phone width: the rows fit on one line
{
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=bitrunc');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  for (const L of LANG_ORDER) {
    await page.selectOption('#hud-tools .lang-btn select', L); await page.waitForTimeout(300);
    for (const mode of ['sweep', 'shadow', 'shells']) {
      await page.tap(`${P} [data-bt-mode="${mode}"]`); await page.waitForTimeout(300);
      const rows = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} .bt-row, ${sel} .bt-modes`)].filter((r) => r.offsetParent)
        .map((r) => ({ over: r.scrollWidth - r.clientWidth, tall: r.getBoundingClientRect().height, btn: Math.max(...[...r.querySelectorAll('button')].map((x) => x.getBoundingClientRect().height)) })), P);
      for (const r of rows) assert.ok(r.over <= 1 && r.tall < r.btn * 1.5, `${L} ${mode}: a row overflows ${JSON.stringify(r)}`);
      const cap = await page.locator(`${P} .ch-param-caption`).textContent();
      assert.ok(cap && !/\b(bt|wq|rq)\.[a-z]/.test(cap), `${L} ${mode}: caption translated (${cap})`);
      if (L === 'ja' && mode === 'sweep') await page.screenshot({ path: `${SH}/phone-ja-sweep.png` });
    }
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors');
  await page.close();
}
// screenshots
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=bitrunc:swap');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  await page.screenshot({ path: `${SH}/${dev}-sweep-swap.png` });
  await page.locator(`${P} .bt-sweep-row input`).fill(String(SWAP_K)); await page.waitForTimeout(900);
  await page.screenshot({ path: `${SH}/${dev}-sweep-swap-2.png` });
  await page.click(`${P} [data-bt-dir="cell-first"]`); await page.locator(`${P} .bt-sweep-row input`).fill(String(BATCH_K)); await page.waitForTimeout(900);
  await page.screenshot({ path: `${SH}/${dev}-sweep-cell-first-batch.png` });
  await page.click(`${P} [data-bt-mode="shadow"]`); await page.click(`${P} [data-bt-from="vertex-first"]`); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-shadow-vertex-first.png` });
  await page.click(`${P} [data-bt-to="cell-first"]`); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-shadow-cell-first.png` });
  await page.click(`${P} [data-bt-mode="shells"]`);
  for (const n of [1, 2, 3, 4, 6]) {
    await page.locator(`${P} .bt-shells-row input`).fill(String(n)); await page.waitForTimeout(1200);
    await page.screenshot({ path: `${SH}/${dev}-shells-${n}.png` });
  }
  await page.click(`${P} [data-bt-whole]`); await page.waitForTimeout(1500);
  await page.screenshot({ path: `${SH}/${dev}-shells-whole.png` });
  await page.click(`${P} [data-bt-whole]`);
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`bitrunc OK: ${checks} checks`);
