// The 4D Permutohedron (DICTO 2026-11-10; src/app/world-perm4.js), through the real UI, touch, phone (390×844) and iPad (820×1180), on
// the Kaleidohedra and Rhombiverse doors (DOORS): right after the Bitruncated 600-cell in DICTO's list (both after DICTONIC); it opens on Build (30 cells, one the outer
// shell); the pull slider, big and at the bottom, pulls the cells apart; All cells / 3D permutohedra / Hexagonal prisms show 30 / 10 /
// 20; Sweep: the cut slider over the 119 gaps, Next swap lands on a swap with two cells letting go and two meeting, captioned as the page;
// Play runs the sweep and Pause holds it; each view only its own controls; no empty prompt pill. ?open=perm4[:sweep|swap]. Every one of
// the 7 languages at phone width: the rows fit. No console errors. Screenshots ($SHOTS, default /tmp/perm4-shots) on a phone (390×844)
// and a desktop (1280×800): Build at pull 0 and 45 %, each cell kind, and the Sweep at a swap.
// RCP view, RCP v4 and Sectors (DICTO 2026-11-11, PARTS rcp, rcpshots), as in the Queens world: three buttons in Build only, tapped on
// both doors (phone and iPad): RCP view and RCP v4 exclude each other, the seed (the 3D permutohedron at the centre of Build) drawn at
// its true size in RCP v4 so the cells reach further out; Sectors cuts the seed into its 14 pyramids and all 30 cells into 128 pieces,
// its own big slider (no arrows) replaces the cells' pull and, dragged with a finger, pulls the sectors out step by step, everything on
// screen; the kind buttons still pick the cells; off again, the pull is back. ?open=perm4:sectors. Screenshots ($RCP_SHOTS, default
// $SHOTS) of each new view on a phone and a desktop: rcp-perm4-<dev>-*.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import * as PM from '../../src/app/perm4-geometry.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/perm4-shots', RS = process.env.RCP_SHOTS ?? SH;
mkdirSync(SH, { recursive: true }); mkdirSync(RS, { recursive: true });
// PARTS (default all): doors, rcp, open, langs, shots, rcpshots; to run the file in pieces
const PARTS = (process.env.PARTS ?? 'doors,rcp,open,langs,shots,rcpshots').split(',');
const P = '#worldperm4-panel';
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  return errors;
}
const probe = (page) => page.evaluate(() => window.__perm4Probe());
const SWAP = PM.nextSwap(60);   // Next swap from the page's starting cut (itself a swap)
// every drawn corner on screen, above the controls (2 px slack)
async function onScreen(page, what) {
  const s = await page.evaluate(() => window.__perm4Screen());
  assert.ok(s && s.x0 >= -2 && s.x1 <= s.w + 2 && s.y0 >= -2 && s.y1 <= s.h - s.cover + 2, `${what}: off screen ${JSON.stringify(s)}`);
}
// a slider dragged with a finger from its thumb to `to`, in `steps` moves, holding still after each; each(st) sees the probe every step
async function drag(page, row, to, steps, each = async () => {}) {
  const input = page.locator(`${P} ${row} input`), box = await input.boundingBox(), y = box.y + box.height / 2;
  const at = (v) => box.x + 20 + ((box.width - 40) * v) / 1000;   // the thumb is 40 px wide
  const from = Number(await input.inputValue()), cdp = await page.context().newCDPSession(page);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: at(from), y }] });
  for (let i = 1; i <= steps; i++) {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: at(from + ((to - from) * i) / steps), y }] });
    await page.waitForTimeout(500); await each(await probe(page));
  }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForTimeout(700); await cdp.detach();
}

for (const door of (PARTS.includes('doors') ? process.env.DOORS ?? 'kaleidohedra,rhombiverse' : '').split(',').filter(Boolean)) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:perm4World"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[worlds.indexOf('tool:bitruncWorld') + 1], 'tool:perm4World', `${tag}: right after the Bitruncated 600-cell`); checks++;
    await page.locator('[data-action="tool:perm4World"]').first().tap(); await page.waitForTimeout(500);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1000);
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    const visible = (sel) => page.locator(`${P} ${sel}`).isVisible();
    assert.ok(!(await page.evaluate(() => { const e = document.getElementById('hud-prompt'); return e.classList.contains('visible') && !e.textContent.trim(); })), `${tag}: no empty prompt`);
    let st = await probe(page);
    assert.deepEqual([st.mode, st.kind, st.cells, st.to, st.outer, st.pull], ['build', 'all', 30, 10, 1, 0], `${tag}: opens on Build`);
    assert.equal(await caption(), t('pm.cap.all', 'en'));
    assert.ok(!(await visible('.pm-cut-row')) && !(await visible('.pm-sweep-btns')) && (await visible('.pm-pull-row')), `${tag}: only Build's controls`);
    const pull = page.locator(`${P} .pm-pull-row input`), sb = await pull.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`);
    for (const k of PM.KINDS) { const bx = await page.locator(`${P} [data-pm-kind="${k}"]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${k} touchable`); }
    checks++;
    await pull.fill('450'); await page.waitForTimeout(300); st = await probe(page);
    assert.equal(st.pull, 450); assert.ok((await page.locator(`${P} .pm-pull-label`).textContent()).includes('45%'), `${tag}: pull label`); checks++;
    for (const [k, n] of [['to', 10], ['hp', 20], ['all', 30]]) {
      await page.tap(`${P} [data-pm-kind="${k}"]`); await page.waitForTimeout(300); st = await probe(page);
      assert.deepEqual([st.kind, st.cells], [k, n], `${tag}: kind ${k}`); assert.equal(await caption(), t(`pm.cap.${k}`, 'en'));
    }
    checks++;
    // Sweep
    await page.tap(`${P} [data-pm-mode="sweep"]`); await page.waitForTimeout(400); st = await probe(page);
    assert.deepEqual([st.mode, st.gap], ['sweep', 60], `${tag}: Sweep at the page's start`);
    assert.ok(!(await visible('.pm-pull-row')) && (await visible('.pm-cut-row')) && (await visible('[data-pm-next]')), `${tag}: only Sweep's controls`);
    await page.tap(`${P} [data-pm-next]`); await page.waitForTimeout(300); st = await probe(page);
    const s = PM.sweepAt(SWAP, 'all');
    assert.deepEqual([st.gap, st.what, st.swap, st.lit], [SWAP, 'swap', s.swap, { go: 2, meet: 2 }], `${tag}: Next swap`);
    assert.equal(await caption(), `corner ${SWAP} of 119 · swap ${s.swap} of 66: two cells let go, two meet · ${s.alive} cells in the cut (${s.to} permutohedra, ${s.hp} prisms)`);
    assert.equal(await page.locator(`${P} .pm-legend .pm-sw`).count(), 4); checks++;
    const cut = page.locator(`${P} .pm-cut-row input`);
    await cut.fill('0'); await page.waitForTimeout(300); st = await probe(page); assert.equal(st.gap, 0);
    await cut.fill('118'); await page.waitForTimeout(300); st = await probe(page); assert.equal(st.gap, 118); checks++;
    await page.tap(`${P} [data-pm-play]`); await page.waitForTimeout(1300); st = await probe(page);
    assert.ok(st.playing && st.gap >= 0 && st.gap < 5, `${tag}: Play runs round from the top (${st.gap})`);
    await page.tap(`${P} [data-pm-play]`); await page.waitForTimeout(200); const g = (await probe(page)).gap; await page.waitForTimeout(800); st = await probe(page);
    assert.ok(!st.playing && st.gap === g, `${tag}: Pause holds`); checks++;
    await page.tap(`${P} [data-pm-mode="build"]`); await page.waitForTimeout(300);
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
    if (!(await page.locator('[data-action="tool:perm4World"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    await page.locator('[data-action="tool:perm4World"]').first().tap(); await page.waitForTimeout(500);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1000);
    const visible = (sel) => page.locator(`${P} ${sel}`).isVisible(), caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    const pressed = (sel) => page.getAttribute(`${P} ${sel}`, 'aria-pressed');
    // not in the Sweep: nothing unnecessary shown
    await page.tap(`${P} [data-pm-mode="sweep"]`); await page.waitForTimeout(400);
    assert.ok(!(await visible('.pm-rcp-row')) && !(await visible('.pm-sectors-row')), `${tag}: none in the Sweep`);
    await page.tap(`${P} [data-pm-mode="build"]`); await page.waitForTimeout(600);
    assert.deepEqual(await page.evaluate((p) => [...document.querySelectorAll(`${p} .pm-rcp-row button`)].map((x) => [Object.keys(x.dataset)[0], x.textContent]), P), [['pmRcp', 'RCP view'], ['pmDictoRcp', 'RCP v4'], ['pmSectors', 'Sectors']]);
    for (const k of ['rcp', 'dicto-rcp', 'sectors']) {
      const bx = await page.locator(`${P} [data-pm-${k}]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44 && bx.x >= 0 && bx.x + bx.width <= viewport.width, `${tag}: ${k} touchable, on screen ${JSON.stringify(bx)}`);
      assert.equal(await pressed(`[data-pm-${k}]`), 'false');
    }
    assert.equal(await page.locator(`${P} [data-pm-sectors]`).getAttribute('title'), t('pm.sectors.tip', 'en'));
    assert.ok(!(await visible('.pm-sectors-row')) && (await visible('.pm-pull-row')), `${tag}: the sectors' slider hidden while off`); checks++;
    let st = await probe(page);
    assert.deepEqual([st.mode, st.rcp, st.dictoRcp, st.sectors, st.cells, st.outer], ['build', false, false, null, 30, 1]);
    // RCP view: all 30 cells as cells (no see-through outer shell: the eye is far off)
    await page.tap(`${P} [data-pm-rcp]`); await page.waitForTimeout(1000); st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp, st.cells, st.outer], [true, false, 30, 0], `${tag}: RCP view`);
    assert.equal(await caption(), t('pm.cap.all.rcp', 'en'), `${tag}: no outer shell in the caption`);
    assert.equal(await pressed('[data-pm-rcp]'), 'true');
    assert.match(await page.locator(`${P} .st-note.fold`).textContent(), /RCP view draws the cells with the RCP build's own perspective/);
    await onScreen(page, `${tag} RCP view`);
    const rcpRadius = st.radius;
    await page.tap(`${P} [data-pm-dicto-rcp]`); await page.waitForTimeout(1000); st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp], [false, true], `${tag}: RCP v4 excludes RCP view`);
    assert.deepEqual([await pressed('[data-pm-rcp]'), await pressed('[data-pm-dicto-rcp]')], ['false', 'true']);
    assert.ok(st.radius > rcpRadius * 1.05, `${tag}: RCP v4 reaches further (${rcpRadius} → ${st.radius})`);
    await onScreen(page, `${tag} RCP v4`);
    // the kinds still pick the cells
    await page.tap(`${P} [data-pm-kind="hp"]`); await page.waitForTimeout(600); st = await probe(page);
    assert.deepEqual([st.kind, st.cells, st.dictoRcp], ['hp', 20, true]); await onScreen(page, `${tag} RCP v4 prisms`);
    await page.tap(`${P} [data-pm-kind="all"]`); await page.waitForTimeout(400);
    await page.tap(`${P} [data-pm-dicto-rcp]`); await page.waitForTimeout(800); st = await probe(page);
    assert.deepEqual([st.rcp, st.dictoRcp, st.outer], [false, false, 1], `${tag}: back to Build`); checks++;
    // Sectors: 14 sectors, all 30 cells in 128 pieces
    await page.tap(`${P} [data-pm-sectors]`); await page.waitForTimeout(1200); st = await probe(page);
    assert.deepEqual([st.sectors.count, st.sectors.wedges, st.sectors.apart], [14, 128, 0], `${tag}: 14 sectors, 128 pieces`);
    assert.ok((await caption()).endsWith('14 sectors · 128 pieces'), `${tag}: caption ${await caption()}`);
    assert.match(await page.locator(`${P} .st-note.fold`).textContent(), /falls apart into 14 sectors/);
    const ss = await page.locator(`${P} .pm-sectors-row input`).boundingBox();
    assert.ok((await visible('.pm-sectors-row')) && !(await visible('.pm-pull-row')), `${tag}: the sectors' slider in place of the pull`);
    assert.ok(ss.width >= viewport.width * 0.8 && ss.height >= 40 && ss.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(ss)}`);
    assert.equal(await page.locator(`${P} .pm-sectors-row button`).count(), 0, `${tag}: no arrows`);
    assert.equal(await page.locator(`${P} .pm-sectors-label`).textContent(), 'Pull the sectors apart'); checks++;
    let prev = st; const rs0 = st.radius;
    await drag(page, '.pm-sectors-row', 800, 4, async (q) => {
      assert.ok(q.sectors.apart > prev.sectors.apart && q.radius > prev.radius, `${tag}: sectors outward ${prev.sectors.apart} → ${q.sectors.apart}`);
      prev = q; await onScreen(page, `${tag} sectors ${q.sectors.apart}`);
    });
    st = await probe(page); assert.ok(Math.abs(st.sectors.apart - 800) <= 15 && st.radius > rs0 * 1.3, `${tag}: pulled (${st.sectors.apart}, ${st.radius})`); checks++;
    // the kinds, RCP view and RCP v4, all cut
    await page.tap(`${P} [data-pm-kind="to"]`); await page.waitForTimeout(800); st = await probe(page);
    assert.ok(st.cells === 10 && st.sectors.wedges > 14, `${tag}: permutohedra in ${st.sectors.wedges} pieces`); await onScreen(page, `${tag} permutohedra in sectors`);
    await page.tap(`${P} [data-pm-kind="all"]`); await page.waitForTimeout(600);
    for (const k of ['rcp', 'dicto-rcp']) {
      await page.tap(`${P} [data-pm-${k}]`); await page.waitForTimeout(1200); st = await probe(page);
      assert.ok((k === 'rcp' ? st.rcp : st.dictoRcp) && st.sectors.count === 14 && st.sectors.wedges === 128, `${tag}: ${k} in sectors`); await onScreen(page, `${tag} ${k} in sectors`);
    }
    await page.tap(`${P} [data-pm-dicto-rcp]`); await page.waitForTimeout(600);
    await page.tap(`${P} [data-pm-sectors]`); await page.waitForTimeout(800); st = await probe(page);
    assert.ok(st.sectors === null && !(await visible('.pm-sectors-row')) && (await visible('.pm-pull-row')), `${tag}: Sectors off`);
    assert.equal(await caption(), t('pm.cap.all', 'en')); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
for (const [q, want] of !PARTS.includes('open') ? [] : [['perm4', 'build'], ['perm4:sweep', 'sweep'], ['perm4:swap', 'sweep'], ['perm4:sectors', 'build']]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=${q}`);
  await page.waitForSelector(`${P}.visible`, { timeout: 20000 }); await page.waitForTimeout(800);
  const st = await probe(page); assert.equal(st.mode, want, `?open=${q}`); if (q === 'perm4:swap') assert.equal(st.what, 'swap');
  if (q === 'perm4:sectors') assert.deepEqual([st.sectors?.count, st.sectors?.apart], [14, 500], `?open=${q}: in sectors pulled apart`);
  assert.deepEqual(errors, [], `?open=${q}: console errors`); checks++; await page.close();
}
if (PARTS.includes('langs')) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=perm4:swap');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(800);
  for (const L of LANG_ORDER) {
    await page.selectOption('#hud-tools .lang-btn select', L); await page.waitForTimeout(250);
    for (const mode of ['sweep', 'build']) {
      await page.tap(`${P} [data-pm-mode="${mode}"]`); await page.waitForTimeout(250);
      const rows = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} .pm-modes, ${sel} .pm-sweep-btns`)].filter((r) => r.offsetParent)
        .map((r) => ({ over: r.scrollWidth - r.clientWidth, tall: r.getBoundingClientRect().height, btn: Math.max(...[...r.querySelectorAll('button')].map((x) => x.getBoundingClientRect().height)) })), P);
      for (const r of rows) assert.ok(r.over <= 1 && r.tall < r.btn * 1.5, `${L} ${mode}: a row overflows ${JSON.stringify(r)}`);
      // the kind buttons may wrap onto a second line, never off the screen
      const kinds = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} .pm-kinds button`)].map((x) => x.getBoundingClientRect()).map((r) => [r.left, r.right]), P);
      assert.ok(kinds.every(([l, r]) => l >= 0 && r <= 390), `${L} ${mode}: kind buttons on screen ${JSON.stringify(kinds)}`);
      const cap = await page.locator(`${P} .ch-param-caption`).textContent(); assert.ok(cap && !/\bpm\.[a-z]/.test(cap), `${L} ${mode}: ${cap}`);
      if (mode === 'build') {
        // RCP view, RCP v4 and Sectors: translated, every button on screen; with Sectors on its slider's words fit, the caption counts
        const wr = await page.evaluate((sel) => { const row = document.querySelector(`${sel} .pm-rcp-row`); return { over: row.scrollWidth - row.clientWidth, btns: [...row.querySelectorAll('button')].map((x) => { const r = x.getBoundingClientRect(); return [x.textContent, r.left, r.right, r.height]; }) }; }, P);
        assert.ok(wr.over <= 1 && wr.btns.every(([s, l, r, h]) => s && l >= 0 && r <= 390 && h >= 30), `${L}: the RCP row fits ${JSON.stringify(wr)}`);
        assert.deepEqual(wr.btns.map(([s]) => s), [t('wq.rcp', L), t('wq.dictoRcp', L), t('wq.sectors', L)]);
        await page.tap(`${P} [data-pm-sectors]`); await page.waitForTimeout(600);
        const sr = await page.evaluate((sel) => { const row = document.querySelector(`${sel} .pm-sectors-row`), l = row.querySelector('.pm-sectors-label'), lh = parseFloat(getComputedStyle(l).lineHeight) || 20;
          return { text: l.textContent, over: row.scrollWidth - row.clientWidth, lines: l.getBoundingClientRect().height / lh }; }, P);
        assert.ok(sr.text === t('wq.sectors.param', L) && sr.over <= 1 && sr.lines < 1.6, `${L}: Pull the sectors apart fits ${JSON.stringify(sr)}`);
        const cap2 = await page.locator(`${P} .ch-param-caption`).textContent();
        assert.ok(cap2.endsWith(t('wq.sectors.count', L, { n: 14, w: 128 })), `${L}: sectors caption (${cap2})`);
        if (L === 'ja') await page.screenshot({ path: `${RS}/rcp-perm4-phone-ja-sectors.png` });
        await page.tap(`${P} [data-pm-sectors]`); await page.waitForTimeout(400);
      }
    }
    if (L === 'ja') await page.screenshot({ path: `${SH}/phone-ja-build.png` });
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors'); await page.close();
}
for (const [dev, viewport] of Object.entries(!PARTS.includes('shots') ? {} : { phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=perm4:build');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  await page.click(`${P} [data-pm-kind="all"]`); await page.locator(`${P} .pm-pull-row input`).fill('0'); await page.locator(`${P} .pm-pull-row input`).dispatchEvent('change'); await page.waitForTimeout(1000);
  await page.screenshot({ path: `${SH}/${dev}-build-pull0.png` });
  await page.locator(`${P} .pm-pull-row input`).fill('450'); await page.locator(`${P} .pm-pull-row input`).dispatchEvent('change'); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-build-pull45.png` });
  for (const k of ['to', 'hp']) { await page.click(`${P} [data-pm-kind="${k}"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/${dev}-build-pull45-${k}.png` }); }
  await page.locator(`${P} .pm-pull-row input`).fill('0'); await page.locator(`${P} .pm-pull-row input`).dispatchEvent('change');
  for (const k of ['to', 'hp']) { await page.click(`${P} [data-pm-kind="${k}"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/${dev}-build-pull0-${k}.png` }); }
  await page.click(`${P} [data-pm-kind="all"]`); await page.click(`${P} [data-pm-mode="sweep"]`); await page.waitForTimeout(400);
  await page.click(`${P} [data-pm-next]`); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-sweep-swap.png` });
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
// screenshots of each new view, phone and desktop
for (const [dev, viewport] of Object.entries(!PARTS.includes('rcpshots') ? {} : { phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=perm4:build');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  const shot = async (name) => { await page.waitForTimeout(1300); await onScreen(page, `${dev} ${name}`); await page.screenshot({ path: `${RS}/rcp-perm4-${dev}-${name}.png` }); };
  await page.click(`${P} [data-pm-kind="all"]`);
  await page.click(`${P} [data-pm-rcp]`); await shot('rcp');
  await page.click(`${P} [data-pm-kind="hp"]`); await shot('rcp-prisms');
  await page.click(`${P} [data-pm-kind="all"]`); await page.click(`${P} [data-pm-dicto-rcp]`); await shot('rcp4');
  await page.click(`${P} [data-pm-dicto-rcp]`); await page.click(`${P} [data-pm-sectors]`);
  const pull = async (v) => { const a = page.locator(`${P} .pm-sectors-row input`); await a.fill(String(v)); await a.dispatchEvent('change'); };
  await shot('sectors-closed');
  await pull(500); await shot('sectors');
  await page.click(`${P} [data-pm-rcp]`); await shot('sectors-rcp');
  await page.click(`${P} [data-pm-dicto-rcp]`); await shot('sectors-rcp4');
  await page.click(`${P} [data-pm-dicto-rcp]`); await pull(0); await page.click(`${P} [data-pm-sectors]`); await page.waitForTimeout(500);
  assert.deepEqual(errors, [], `${dev} RCP screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`perm4 OK: ${checks} checks`);
