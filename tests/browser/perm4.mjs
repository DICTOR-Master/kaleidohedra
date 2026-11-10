// The 4D Permutohedron (DICTO 2026-11-10; src/app/world-perm4.js), through the real UI, touch, phone (390×844) and iPad (820×1180), on
// the Kaleidohedra and Rhombiverse doors (DOORS): right after DICTONIC in DICTO's list; it opens on Build (30 cells, one the outer
// shell); the pull slider, big and at the bottom, pulls the cells apart; All cells / Truncated octahedra / Hexagonal prisms show 30 / 10 /
// 20; Sweep: the cut slider over the 119 gaps, Next swap lands on a swap with two cells letting go and two meeting, captioned as the page;
// Play runs the sweep and Pause holds it; each view only its own controls; no empty prompt pill. ?open=perm4[:sweep|swap]. Every one of
// the 7 languages at phone width: the rows fit. No console errors. Screenshots ($SHOTS, default /tmp/perm4-shots) on a phone (390×844)
// and a desktop (1280×800): Build at pull 0 and 45 %, each cell kind, and the Sweep at a swap.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import * as PM from '../../src/app/perm4-geometry.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/perm4-shots';
mkdirSync(SH, { recursive: true });
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

for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:perm4World"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[worlds.indexOf('tool:dictonicWorld') + 1], 'tool:perm4World', `${tag}: right after DICTONIC`); checks++;
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
    assert.equal(await caption(), `corner ${SWAP} of 119 · swap ${s.swap} of 66: two cells let go, two meet · ${s.alive} cells in the cut (${s.to} truncated octahedra, ${s.hp} prisms)`);
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
for (const [q, want] of [['perm4', 'build'], ['perm4:sweep', 'sweep'], ['perm4:swap', 'sweep']]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=${q}`);
  await page.waitForSelector(`${P}.visible`, { timeout: 20000 }); await page.waitForTimeout(800);
  const st = await probe(page); assert.equal(st.mode, want, `?open=${q}`); if (q === 'perm4:swap') assert.equal(st.what, 'swap');
  assert.deepEqual(errors, [], `?open=${q}: console errors`); checks++; await page.close();
}
{
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
    }
    if (L === 'ja') await page.screenshot({ path: `${SH}/phone-ja-build.png` });
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors'); await page.close();
}
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
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
await b.close();
console.log(`perm4 OK: ${checks} checks`);
