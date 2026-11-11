// The Bitruncated 600-cell (DICTO 2026-11-10; src/app/world-bitrunc.js), through the real UI, touch, phone (390×844) and iPad
// (820×1180), on the Kaleidohedra and Rhombiverse doors (DOORS): right after DICTONIC in DICTO's list; it opens on the Sweep along the
// generic direction at the swap nearest the middle, the four cells lit (two let go, two meet) and captioned "Swap k of 2166: …";
// the five direction buttons give each sweep's own stops and totals (generic 716 / 716 / 2166, cell-first 1782 = 1782); the big slider
// at the bottom stops at every corner height and gap middle; Play runs the sweep and stops on a touch. Shadow: From / To and one big
// slider snapping at both ends, 3600 corners and 7200 edges. Shells: 1, 32, 142, 242, 232, 71 cells, then Cut open. Pull apart (Shells
// and Cut open only), dragged with a finger: every drawn cell moves out from the centre, step by step, and stays on screen; kept
// across shells, Cut open and the other views. Each view shows only its own rows. ?open=bitrunc[:shadow|shells|whole|cell]; the Queens world's bitruncated stage links here (only there). Every one
// of the 7 languages at phone width: the rows fit on one line. No console errors. Screenshots ($SHOTS, default /tmp/bitrunc-shots) on
// a phone (390×844) and a desktop (1280×800): the Sweep at a swap, a cell-first batch, Shadow, Shells and Cut open; and ($APART_SHOTS)
// Pull apart: Cut open halfway and fully, the first shell (round the core) fully.
// RCP view, RCP v4 and Sectors (DICTO 2026-11-11, PARTS rcp, rcpshots), as in the Queens world's Shells: the three buttons beside Cut
// open in Shells only, tapped on both doors (phone and iPad): RCP view and RCP v4 exclude each other, RCP v4 reaches further out than
// RCP view, Cut open goes with either; Sectors cuts the core into its 32 pyramids ("32 sectors · 32 pieces"), its own big slider (no
// arrows) replaces Pull apart and, dragged with a finger, pulls the sectors out step by step, everything on screen; with more shells,
// Cut open, RCP view and RCP v4; off again, Pull apart is back. ?open=bitrunc:sectors. Screenshots ($RCP_SHOTS, default $SHOTS) of
// each new view on a phone and a desktop: rcp-bitrunc-<dev>-*.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import * as BT from '../../src/app/bitrunc-geometry.js';
import { middleSwap } from '../../src/app/world-bitrunc.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/bitrunc-shots', AS = process.env.APART_SHOTS ?? SH, RS = process.env.RCP_SHOTS ?? SH;
mkdirSync(SH, { recursive: true }); mkdirSync(AS, { recursive: true }); mkdirSync(RS, { recursive: true });
// PARTS (default all): doors, rcp (RCP view, RCP v4, Sectors on both doors), open (?open= and the Queens link), langs, shots, rcpshots;
// to run the file in pieces
const PARTS = (process.env.PARTS ?? 'doors,rcp,open,langs,shots,rcpshots').split(',');
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
// every drawn corner on screen, above the controls (2 px slack)
async function onScreen(page, what) {
  const s = await page.evaluate(() => window.__bitruncScreen());
  assert.ok(s && s.x0 >= -2 && s.x1 <= s.w + 2 && s.y0 >= -2 && s.y1 <= s.h - s.cover + 2, `${what}: off screen ${JSON.stringify(s)}`);
}
// Pull apart with a finger: from the thumb to the value `to`, in `steps` moves, holding still after each while the view refits;
// each(st) sees the probe at every step
async function dragApart(page, to, steps, each = async () => {}, row = '.bt-apart-row') {
  const input = page.locator(`${P} ${row} input`), box = await input.boundingBox(), y = box.y + box.height / 2;
  const at = (v) => box.x + 20 + ((box.width - 40) * v) / 1000;   // the thumb is 40 px wide
  const from = Number(await input.inputValue()), cdp = await page.context().newCDPSession(page);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: at(from), y }] });
  for (let i = 1; i <= steps; i++) {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: at(from + ((to - from) * i) / steps), y }] });
    await page.waitForTimeout(550); await each(await probe(page));
  }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForTimeout(700); await cdp.detach();
}
const leave = async (page) => { await page.waitForTimeout(500); if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]'); };
// a swap stop and a gap stop along the generic direction; a batch along cell-first
const G = BT.sweep('generic'), C = BT.sweep('cell-first');
const SWAP_K = G.stops.findIndex((s, k) => k > 1000 && s.level !== undefined && G.events[s.level].letGo.length === 1);
const GAP_K = SWAP_K + 1;
const BATCH_K = C.stops.findIndex((s) => s.level !== undefined && C.events[s.level].letGo.length > 1 && !C.events[s.level].born.length && !C.events[s.level].died.length);

for (const door of (PARTS.includes('doors') ? process.env.DOORS ?? 'kaleidohedra,rhombiverse' : '').split(',').filter(Boolean)) {
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
    assert.ok(!(await visible('[data-bt-row="from"]')) && !(await visible('.bt-param-row')) && !(await visible('.bt-shells-row')) && !(await visible('.bt-whole-row')) && !(await visible('.bt-apart-row')), `${tag}: only Sweep rows`);
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
    assert.ok(!(await visible('[data-bt-row="dir"]')) && !(await visible('.bt-sweep-row')) && !(await visible('.bt-play-row')) && !(await visible('.bt-apart-row')) && (await visible('[data-bt-row="from"]')), `${tag}: only Shadow rows`);
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
    // Pull apart in Shells: big, at the bottom; a finger drags it from closed to full, every drawn cell moving out, all on screen
    const apart = page.locator(`${P} .bt-apart-row input`), ab = await apart.boundingBox();
    assert.ok((await visible('.bt-apart-row')) && ab.width >= viewport.width * 0.8 && ab.height >= 40 && ab.y > viewport.height * 0.6, `${tag}: Pull apart big at the bottom ${JSON.stringify(ab)}`);
    assert.equal(await page.locator(`${P} .bt-apart-label`).textContent(), t('bt.apart', 'en', { p: 0 }));
    await shl.fill('3'); await page.waitForTimeout(800); st = await probe(page);
    assert.deepEqual([st.apart, st.drawn], [0, 1 + 32 + 142], `${tag}: three shells, closed`);
    await onScreen(page, `${tag} three shells closed`);
    let prev = st;
    await dragApart(page, 1000, 5, async (q) => {
      assert.ok(q.apart > prev.apart && q.centres.mean > prev.centres.mean && q.centres.max > prev.centres.max && q.radius > prev.radius, `${tag}: outward ${prev.apart} → ${q.apart}`);
      assert.equal(q.drawn, 175); prev = q; await onScreen(page, `${tag} pulling, ${q.apart}`);
    });
    st = await probe(page);
    assert.ok(st.apart >= 990, `${tag}: pulled fully (${st.apart})`); await onScreen(page, `${tag} three shells pulled`);
    assert.ok((await page.locator(`${P} .bt-apart-label`).textContent()).endsWith(`${Math.round(st.apart / 10)}%`), `${tag}: pull label`); checks++;
    // kept when the shells change, then in Cut open; dragged back halfway, inward and on screen
    const pulled = st.apart;
    await shl.fill('5'); await page.waitForTimeout(800); st = await probe(page);
    assert.deepEqual([st.shells, st.apart], [5, pulled], `${tag}: kept across shells`); await onScreen(page, `${tag} five shells pulled`);
    await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(900); st = await probe(page);
    assert.ok(st.whole && st.apart === pulled && (await visible('.bt-apart-row')), `${tag}: kept in Cut open`); await onScreen(page, `${tag} Cut open pulled`);
    prev = st;
    await dragApart(page, 500, 3, async (q) => { assert.ok(q.apart < prev.apart && q.centres.mean < prev.centres.mean, `${tag}: inward ${prev.apart} → ${q.apart}`); prev = q; await onScreen(page, `${tag} Cut open, ${q.apart}`); });
    st = await probe(page); assert.ok(Math.abs(st.apart - 500) <= 15, `${tag}: Cut open halfway (${st.apart})`);
    // kept across the other views; hidden there
    const half = st.apart;
    await page.tap(`${P} [data-bt-mode="sweep"]`); await page.waitForTimeout(500); assert.ok(!(await visible('.bt-apart-row')), `${tag}: hidden in Sweep`);
    await page.tap(`${P} [data-bt-mode="shells"]`); await page.waitForTimeout(800); st = await probe(page);
    assert.deepEqual([st.whole, st.apart], [true, half], `${tag}: kept across views`); await onScreen(page, `${tag} back in Cut open`);
    await apart.fill('0'); await page.waitForTimeout(300); await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(400);
    await shl.fill('6'); await page.waitForTimeout(400); checks++;
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
// RCP view, RCP v4 and Sectors, through the real UI on both doors, phone and iPad, by touch
for (const door of (PARTS.includes('rcp') ? process.env.DOORS ?? 'kaleidohedra,rhombiverse' : '').split(',').filter(Boolean)) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev} rcp`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:bitruncWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    await page.locator('[data-action="tool:bitruncWorld"]').first().tap(); await leave(page);
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    const visible = (sel) => page.locator(`${P} ${sel}`).isVisible(), caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    const pressed = (sel) => page.getAttribute(`${P} ${sel}`, 'aria-pressed');
    // not in the Sweep or the Shadow: nothing unnecessary shown
    for (const m of ['sweep', 'shadow']) {
      await page.tap(`${P} [data-bt-mode="${m}"]`); await page.waitForTimeout(500);
      for (const k of ['rcp', 'dicto-rcp', 'sectors']) assert.ok(!(await visible(`[data-bt-${k}]`)), `${tag}: no ${k} in ${m}`);
    }
    await page.tap(`${P} [data-bt-mode="shells"]`); await page.waitForTimeout(900);
    // the Queens world's row: Cut open, RCP view, RCP v4, Sectors; their words; big enough for a finger; all off
    assert.deepEqual(await page.evaluate((p) => [...document.querySelectorAll(`${p} .bt-whole-row button`)].map((x) => Object.keys(x.dataset)[0]), P), ['btWhole', 'btRcp', 'btDictoRcp', 'btSectors']);
    assert.deepEqual(await page.evaluate((p) => [...document.querySelectorAll(`${p} .bt-whole-row button`)].map((x) => x.textContent), P), ['Cut open', 'RCP view', 'RCP v4', 'Sectors']);
    for (const k of ['rcp', 'dicto-rcp', 'sectors']) {
      const bx = await page.locator(`${P} [data-bt-${k}]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44 && bx.x >= 0 && bx.x + bx.width <= viewport.width, `${tag}: ${k} touchable, on screen ${JSON.stringify(bx)}`);
      assert.equal(await pressed(`[data-bt-${k}]`), 'false');
    }
    assert.equal(await page.locator(`${P} [data-bt-sectors]`).getAttribute('title'), t('bt.sectors.tip', 'en'));
    assert.ok(!(await visible('.bt-sectors-row')), `${tag}: the sectors' slider hidden while off`); checks++;
    const shl = page.locator(`${P} .bt-shells-row input`);
    await shl.fill('3'); await page.waitForTimeout(900);
    let st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp, st.sectors, st.shells], [false, false, null, 3]);
    const r0 = st.radius;
    // RCP view
    await page.tap(`${P} [data-bt-rcp]`); await page.waitForTimeout(1200); st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp, st.shells, st.drawn], [true, false, 3, 175], `${tag}: RCP view`);
    assert.ok(Math.abs(st.radius - r0) > 1e-3, `${tag}: the picture changes (${r0} → ${st.radius})`);
    assert.equal(await pressed('[data-bt-rcp]'), 'true');
    assert.match(await page.locator(`${P} .st-note.fold`).textContent(), /RCP view draws the shells with the RCP build's own perspective/);
    await onScreen(page, `${tag} RCP view`);
    const rcpRadius = st.radius;
    // RCP v4: turns RCP view off, the third shell reaches further out
    await page.tap(`${P} [data-bt-dicto-rcp]`); await page.waitForTimeout(1200); st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp, st.shells], [false, true, 3], `${tag}: RCP v4 excludes RCP view`);
    assert.deepEqual([await pressed('[data-bt-rcp]'), await pressed('[data-bt-dicto-rcp]')], ['false', 'true']);
    assert.ok(st.radius > rcpRadius, `${tag}: RCP v4 reaches further (${rcpRadius} → ${st.radius})`);
    await onScreen(page, `${tag} RCP v4`);
    // Cut open goes with it
    await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(1500); st = await probe(page);
    assert.deepEqual([st.whole, st.dictoRcp], [true, true], `${tag}: Cut open + RCP v4`);
    assert.ok(st.wholeKept.every((n) => n > 0)); await onScreen(page, `${tag} Cut open + RCP v4`);
    await page.tap(`${P} [data-bt-rcp]`); await page.waitForTimeout(1500); st = await probe(page);
    assert.deepEqual([st.whole, st.rcp, st.dictoRcp], [true, true, false], `${tag}: Cut open + RCP view`); await onScreen(page, `${tag} Cut open + RCP view`);
    await page.tap(`${P} [data-bt-rcp]`); await page.waitForTimeout(800); await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(800);
    st = await probe(page); assert.deepEqual([st.whole, st.rcp, st.dictoRcp], [false, false, false], `${tag}: back to the Shells perspective`); checks++;
    // Sectors: the core in its 32 pyramids
    await shl.fill('1'); await page.waitForTimeout(800);
    await page.tap(`${P} [data-bt-sectors]`); await page.waitForTimeout(1200); st = await probe(page);
    assert.deepEqual([st.sectors.count, st.sectors.wedges, st.sectors.apart], [32, 32, 0], `${tag}: the core in its 32 pieces`);
    assert.ok((await caption()).endsWith('32 sectors · 32 pieces'), `${tag}: caption ${await caption()}`);
    assert.match(await page.locator(`${P} .st-note.fold`).textContent(), /falls apart into 32 sectors/);
    // its own slider, big, at the bottom, no arrows; Pull apart rests
    const ss = await page.locator(`${P} .bt-sectors-row input`).boundingBox();
    assert.ok((await visible('.bt-sectors-row')) && !(await visible('.bt-apart-row')), `${tag}: the sectors' slider in place of Pull apart`);
    assert.ok(ss.width >= viewport.width * 0.8 && ss.height >= 40 && ss.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(ss)}`);
    assert.equal(await page.locator(`${P} .bt-sectors-row button`).count(), 0, `${tag}: no arrows`);
    assert.equal(await page.locator(`${P} .bt-sectors-label`).textContent(), 'Pull the sectors apart'); checks++;
    // dragged with a finger: each step further out, on screen
    let prev = st; const rs0 = st.radius;
    await dragApart(page, 700, 4, async (q) => {
      assert.ok(q.sectors.apart > prev.sectors.apart && q.radius > prev.radius, `${tag}: sectors outward ${prev.sectors.apart} → ${q.sectors.apart}`);
      prev = q; await onScreen(page, `${tag} sectors ${q.sectors.apart}`);
    }, '.bt-sectors-row');
    st = await probe(page); assert.ok(Math.abs(st.sectors.apart - 700) <= 15 && st.radius > rs0 * 1.2, `${tag}: pulled (${st.sectors.apart}, ${st.radius})`); checks++;
    // more shells, Cut open, RCP view and RCP v4, all cut
    await shl.fill('3'); await page.waitForTimeout(1200); st = await probe(page);
    assert.ok(st.sectors.wedges > 175, `${tag}: three shells in ${st.sectors.wedges} pieces`); await onScreen(page, `${tag} three shells in sectors`);
    await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(1500); st = await probe(page);
    assert.ok(st.whole && st.sectors.wedges > 0, `${tag}: Cut open in sectors`); await onScreen(page, `${tag} Cut open in sectors`);
    for (const k of ['rcp', 'dicto-rcp']) {
      await page.tap(`${P} [data-bt-${k}]`); await page.waitForTimeout(1500); st = await probe(page);
      assert.ok((k === 'rcp' ? st.rcp : st.dictoRcp) && st.sectors.count === 32 && st.sectors.wedges > 0, `${tag}: ${k} in sectors`); await onScreen(page, `${tag} ${k} in sectors`);
    }
    await page.tap(`${P} [data-bt-dicto-rcp]`); await page.waitForTimeout(800); await page.tap(`${P} [data-bt-whole]`); await page.waitForTimeout(800);
    // off: the cells whole, Pull apart back
    await page.tap(`${P} [data-bt-sectors]`); await page.waitForTimeout(1000); st = await probe(page);
    assert.ok(st.sectors === null && !(await visible('.bt-sectors-row')) && (await visible('.bt-apart-row')), `${tag}: Sectors off`);
    assert.ok(!(await caption()).includes('sectors'), `${tag}: caption without sectors`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
// ?open=bitrunc[:…]
for (const [q, want] of !PARTS.includes('open') ? [] : [['bitrunc', { mode: 'sweep' }], ['bitrunc:shadow', { mode: 'shadow' }], ['bitrunc:shells', { mode: 'shells', whole: false }], ['bitrunc:whole', { mode: 'shells', whole: true }], ['bitrunc:cell', { mode: 'sweep', dir: 'cell-first' }], ['bitrunc:sectors', { mode: 'shells', whole: true }]]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=${q}`);
  await page.waitForSelector(`${P}.visible`, { timeout: 20000 }); await page.waitForTimeout(1200);
  const st = await probe(page);
  for (const [k, v] of Object.entries(want)) assert.equal(st[k], v, `?open=${q}: ${k}`);
  if (q === 'bitrunc:sectors') assert.deepEqual([st.sectors?.count, st.sectors?.apart], [32, 500], `?open=${q}: in sectors pulled apart`);
  assert.deepEqual(errors, [], `?open=${q}: console errors`); checks++;
  await page.close();
}
// the Queens world: one link, at the bitruncated stage only, opens this world
if (PARTS.includes('open')) {
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
if (PARTS.includes('langs')) {
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
      if (mode === 'shells') {
        const r = await page.evaluate((sel) => { const row = document.querySelector(`${sel} .bt-apart-row`), l = row.querySelector('.bt-apart-label'), lh = parseFloat(getComputedStyle(l).lineHeight) || 20;
          return { text: l.textContent, over: row.scrollWidth - row.clientWidth, lines: l.getBoundingClientRect().height / lh }; }, P);
        assert.ok(r.text === t('bt.apart', L, { p: 0 }) && r.text !== 'bt.apart' && r.over <= 1 && r.lines < 1.6, `${L}: Pull apart fits ${JSON.stringify(r)}`);
        // Cut open, RCP view, RCP v4 and Sectors: translated, every button on screen (the row may wrap, as the Queens world's), and with
        // Sectors on its slider's words fit
        const wr = await page.evaluate((sel) => { const row = document.querySelector(`${sel} .bt-whole-row`); return { over: row.scrollWidth - row.clientWidth, btns: [...row.querySelectorAll('button')].map((x) => { const r = x.getBoundingClientRect(); return [x.textContent, r.left, r.right, r.height]; }) }; }, P);
        assert.ok(wr.over <= 1 && wr.btns.every(([s, l, r, h]) => s && l >= 0 && r <= 390 && h >= 30), `${L}: the RCP row fits ${JSON.stringify(wr)}`);
        assert.deepEqual(wr.btns.map(([s]) => s), [t('wq.whole', L), t('wq.rcp', L), t('wq.dictoRcp', L), t('wq.sectors', L)]);
        await page.tap(`${P} [data-bt-sectors]`); await page.waitForTimeout(600);
        const sr = await page.evaluate((sel) => { const row = document.querySelector(`${sel} .bt-sectors-row`), l = row.querySelector('.bt-sectors-label'), lh = parseFloat(getComputedStyle(l).lineHeight) || 20;
          return { text: l.textContent, over: row.scrollWidth - row.clientWidth, lines: l.getBoundingClientRect().height / lh }; }, P);
        assert.ok(sr.text === t('wq.sectors.param', L) && sr.over <= 1 && sr.lines < 1.6, `${L}: Pull the sectors apart fits ${JSON.stringify(sr)}`);
        const cap2 = await page.locator(`${P} .ch-param-caption`).textContent();
        assert.ok(cap2.endsWith(t('wq.sectors.count', L, { n: 32, w: 32 })), `${L}: sectors caption (${cap2})`);
        if (L === 'ja') await page.screenshot({ path: `${RS}/rcp-bitrunc-phone-ja-sectors.png` });
        await page.tap(`${P} [data-bt-sectors]`); await page.waitForTimeout(400);
      }
      if (L === 'ja' && mode === 'sweep') await page.screenshot({ path: `${SH}/phone-ja-sweep.png` });
    }
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors');
  await page.close();
}
// screenshots
for (const [dev, viewport] of Object.entries(!PARTS.includes('shots') ? {} : { phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
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
  // Pull apart: Cut open halfway and fully, then the first shell round the core fully (fill, then the release that fits the view)
  const pull = async (v) => { const a = page.locator(`${P} .bt-apart-row input`); await a.fill(String(v)); await a.dispatchEvent('change'); await page.waitForTimeout(1500); await onScreen(page, `${dev} shot at ${v}`); };
  await pull(500); await page.screenshot({ path: `${AS}/apart-${dev}-cutopen-half.png` });
  await pull(1000); await page.screenshot({ path: `${AS}/apart-${dev}-cutopen-full.png` });
  await page.click(`${P} [data-bt-whole]`); await page.locator(`${P} .bt-shells-row input`).fill('2'); await page.waitForTimeout(1500); await onScreen(page, `${dev} the first shell`);
  await page.screenshot({ path: `${AS}/apart-${dev}-shell1-full.png` });
  await pull(0);
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
// screenshots of each new view, phone and desktop
for (const [dev, viewport] of Object.entries(!PARTS.includes('rcpshots') ? {} : { phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=bitrunc:shells');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  const shot = async (name) => { await page.waitForTimeout(1500); await onScreen(page, `${dev} ${name}`); await page.screenshot({ path: `${RS}/rcp-bitrunc-${dev}-${name}.png` }); };
  await page.locator(`${P} .bt-shells-row input`).fill('3'); await page.waitForTimeout(800);
  await page.click(`${P} [data-bt-rcp]`); await shot('rcp-shells3');
  await page.click(`${P} [data-bt-whole]`); await shot('rcp-cutopen');
  await page.click(`${P} [data-bt-dicto-rcp]`); await shot('rcp4-cutopen');
  await page.click(`${P} [data-bt-whole]`); await shot('rcp4-shells3');
  await page.click(`${P} [data-bt-dicto-rcp]`); await page.locator(`${P} .bt-shells-row input`).fill('1'); await page.waitForTimeout(600);
  await page.click(`${P} [data-bt-sectors]`);
  const pull = async (v) => { const a = page.locator(`${P} .bt-sectors-row input`); await a.fill(String(v)); await a.dispatchEvent('change'); };
  await pull(500); await shot('sectors-core');
  await page.locator(`${P} .bt-shells-row input`).fill('3'); await shot('sectors-shells3');
  await page.click(`${P} [data-bt-whole]`); await shot('sectors-cutopen');
  await page.click(`${P} [data-bt-rcp]`); await shot('sectors-rcp-cutopen');
  await page.click(`${P} [data-bt-dicto-rcp]`); await shot('sectors-rcp4-cutopen');
  await page.click(`${P} [data-bt-dicto-rcp]`); await page.click(`${P} [data-bt-whole]`); await pull(0); await page.click(`${P} [data-bt-sectors]`); await page.waitForTimeout(500);
  assert.deepEqual(errors, [], `${dev} RCP screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`bitrunc OK: ${checks} checks`);
