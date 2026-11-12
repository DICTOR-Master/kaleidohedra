// Generalized Permutohedra (src/app/world-gperm.js), through the real UI, by touch, on a phone (390×844) and an iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors: listed in Kaleidohedra's block, first among its worlds; opens on the permutohedron (24, 36, 14,
// fills space); the big slider at the bottom with its 5 walls marked on the track (one face vanishing at each, DICTO's staged route);
// dragged with a finger the badge turns to "does not" and the caption names the stage; at a wall that face is named and gone; at the end
// the associahedron (14, 21, 9); each stop tapped gives its known counts and
// the right badge; ?open=gperm:cyclohedron. Every one of the 7 languages at phone width: the stop buttons on screen, no raw keys.
// No console errors. Screenshots ($SHOTS, default /tmp/gperm-shots): phone and desktop, at each stop and halfway.
// DICTO · dictospheres.com
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import * as G from '../../src/app/gperm-geometry.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/gperm-shots';
mkdirSync(SH, { recursive: true });
const PARTS = (process.env.PARTS ?? 'doors,open,langs,shots').split(',');
const P = '#worldgperm-panel';
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  return errors;
}
const probe = (page) => page.evaluate(() => window.__gpermProbe());
async function onScreen(page, what) {
  const s = await page.evaluate(() => window.__gpermScreen());
  assert.ok(s && s.x0 >= -2 && s.x1 <= s.w + 2 && s.y0 >= -2 && s.y1 <= s.h - s.cover + 2, `${what}: off screen ${JSON.stringify(s)}`);
}
// the slider dragged with a finger from its thumb to `to` (0..700, its max)
async function drag(page, to, steps = 6) {
  const input = page.locator(`${P} .gp-line-row input`), box = await input.boundingBox(), y = box.y + box.height / 2;
  const at = (v) => box.x + 20 + ((box.width - 40) * v) / 700;
  const from = Number(await input.inputValue()), cdp = await page.context().newCDPSession(page);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: at(from), y }] });
  for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: at(from + ((to - from) * i) / steps), y }] }); await page.waitForTimeout(250); }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForTimeout(500); await cdp.detach();
}
const FILLS = { simplex: false, cube: true, hypersimplex: false, cyclohedron: false, associahedron: false, permutohedron: true };

for (const door of (PARTS.includes('doors') ? process.env.DOORS ?? 'kaleidohedra,rhombiverse' : '').split(',').filter(Boolean)) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:gpermWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    // in Kaleidohedra's block, its first world; the other app's one row still there (smoke-both-doors rule)
    const row = page.locator('[data-action="tool:gpermWorld"]');
    assert.equal(await row.count(), 1, `${tag}: listed once`);
    assert.equal(await row.getAttribute('data-app'), 'kaleidohedra', `${tag}: opens in Kaleidohedra`);
    const firstKWorld = await page.evaluate(() => { const blk = [...document.querySelectorAll('.dim-wizard-body .dicto-block')].find((x) => x.querySelector(':scope > .dicto-block-name')?.textContent === 'KALEIDOHEDRA');
      return [...(blk?.querySelectorAll('[data-action$="World"]') ?? [])].map((e) => e.dataset.action)[0]; });
    assert.equal(firstKWorld, 'tool:gpermWorld', `${tag}: first among Kaleidohedra's worlds`);
    if (door === 'rhombiverse') assert.ok(await page.locator('.dim-wizard-body [data-app="kaleidohedra"][data-action="tool:pieceType:rd"]').count(), `${tag}: Kaleidohedra keeps its one row`);
    checks++;
    await row.tap(); await page.waitForTimeout(500);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(900);
    // a fresh page starts on the permutohedron (localStorage is per page here)
    let st = await probe(page);
    assert.deepEqual([st.stop, st.onLine, st.s, st.f, st.fills, st.inFamily], ['permutohedron', true, 0, [24, 36, 14], true, true], `${tag}: opens on the permutohedron`);
    assert.equal(await page.locator(`${P} .gp-badge`).textContent(), t('gp.badge.yes', 'en'));
    assert.equal(await page.locator(`${P} [data-gp-stop="permutohedron"]`).getAttribute('aria-pressed'), 'true');
    // the big slider at the bottom, its 5 walls marked where each face vanishes (s = 1, 2, 3, 5, 7 of 7)
    const slider = page.locator(`${P} .gp-line-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`);
    assert.equal(await page.locator(`${P} .gp-wall`).count(), 5, `${tag}: five walls`);
    const wallX = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} .gp-wall`)].map((w) => { const r = w.getBoundingClientRect(); return r.x + r.width / 2; }), P);
    [1, 2, 3, 5, 7].forEach((s, i) => assert.ok(Math.abs(wallX[i] - (sb.x + 20 + ((sb.width - 40) * s) / 7)) < 3, `${tag}: wall ${i} at ${s}/7`));
    assert.deepEqual(st.walls.map((w) => [w.at, w.face]), [[100, '{1,3}'], [200, '{1,4}'], [300, '{2,4}'], [500, '{1,2,4}'], [700, '{1,3,4}']]);
    for (const k of G.PRESET_KEYS) { const bx = await page.locator(`${P} [data-gp-stop="${k}"]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44 && bx.x >= 0 && bx.x + bx.width <= viewport.width, `${tag}: ${k} touchable, on screen`); }
    await onScreen(page, `${tag} permutohedron`);
    checks++;
    // a finger drags into stage 1: the face {1,3} sliding out, no longer centrally symmetric
    await drag(page, 50); st = await probe(page);
    assert.ok(st.onLine && st.s > 20 && st.s < 90 && !st.stop && st.stage === 1, `${tag}: stage 1 (${st.s})`);
    assert.deepEqual([st.f, st.fills, st.symmetric, st.inFamily], [[24, 36, 14], false, false, true], `${tag}: stage 1 shape`);
    assert.equal(await page.locator(`${P} .gp-badge`).textContent(), t('gp.badge.no', 'en'));
    assert.ok((await page.locator(`${P} .ch-param-caption`).textContent()).startsWith('stage 1 of 5: the face {1,3} slides out'), `${tag}: stage caption`);
    // on to stage 4 by finger: three faces gone, {1,2,4} sliding
    await drag(page, 400); st = await probe(page);
    assert.ok(st.stage === 4 && st.f[2] === 11, `${tag}: stage 4 ${JSON.stringify([st.s, st.f])}`);
    await onScreen(page, `${tag} stage 4`);
    // a wall exactly (the slider's value set): the face {2,4} named and gone
    await slider.fill('300'); await page.waitForTimeout(300); st = await probe(page);
    assert.deepEqual([st.wall?.face, st.f, st.faces.includes('{2,4}')], ['{2,4}', [15, 24, 11], false], `${tag}: the {2,4} wall`);
    assert.ok((await page.locator(`${P} .ch-param-caption`).textContent()).includes('wall: the face {2,4} vanishes here'));
    // to the end by finger: the associahedron, its last wall
    await drag(page, 715); st = await probe(page);
    assert.deepEqual([st.stop, st.s, st.f, st.wall?.face], ['associahedron', 700, [14, 21, 9], '{1,3,4}'], `${tag}: the end`);
    checks++;
    // every stop by a tap
    for (const k of G.PRESET_KEYS) {
      await page.tap(`${P} [data-gp-stop="${k}"]`); await page.waitForTimeout(300); st = await probe(page);
      assert.deepEqual([st.stop, st.f, st.fills, st.inFamily], [k, G.KNOWN_F[k], FILLS[k], true], `${tag}: stop ${k}`);
      assert.equal(await page.locator(`${P} [data-gp-stop="${k}"]`).getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator(`${P} .gp-badge`).textContent(), t(FILLS[k] ? 'gp.badge.yes' : 'gp.badge.no', 'en'));
      await onScreen(page, `${tag} ${k}`);
    }
    checks++;
    // off the line, the slider brings you back to it
    await page.tap(`${P} [data-gp-stop="simplex"]`); await page.waitForTimeout(200);
    await drag(page, 50); st = await probe(page);
    assert.ok(st.onLine && st.stop === null && st.f[2] === 14, `${tag}: back on the route`); checks++;
    assert.ok(!(await page.locator('#hud-quick-lattice-view').isVisible()), `${tag}: no lattice view`);
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
if (PARTS.includes('open')) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=gperm:cyclohedron');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(800);
  const st = await probe(page);
  assert.deepEqual([st.stop, st.f], ['cyclohedron', [20, 30, 12]], '?open=gperm:cyclohedron');
  assert.deepEqual(errors, [], 'open: console errors'); checks++; await page.close();
}
if (PARTS.includes('langs')) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=gperm:permutohedron');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(800);
  for (const L of LANG_ORDER) {
    await page.selectOption('#hud-tools .lang-btn select', L); await page.waitForTimeout(250);
    const btns = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} [data-gp-stop]`)].map((x) => { const r = x.getBoundingClientRect(); return [x.textContent, r.left, r.right, r.height]; }), P);
    assert.ok(btns.every(([s, l, r, h]) => s && l >= 0 && r <= 390 && h >= 30), `${L}: stops on screen ${JSON.stringify(btns)}`);
    assert.deepEqual(btns.map(([s]) => s), G.PRESET_KEYS.map((k) => t(`gp.stop.${k}`, L)));
    const texts = await page.evaluate((sel) => [sel + ' .gp-badge', sel + ' .ch-param-caption', sel + ' .gp-legend', sel + ' .gp-line-label', sel + ' .st-note.fold'].map((q) => document.querySelector(q).textContent), P);
    for (const x of texts) assert.ok(x && !/\bgp\.[a-z]/.test(x), `${L}: ${x}`);
    const bg = await page.locator(`${P} .gp-badge`).boundingBox(); assert.ok(bg.x >= 0 && bg.x + bg.width <= 390, `${L}: badge fits`);
    if (L === 'ja') await page.screenshot({ path: `${SH}/phone-ja.png` });
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors'); await page.close();
}
for (const [dev, viewport] of Object.entries(!PARTS.includes('shots') ? {} : { phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=gperm:permutohedron');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  for (const k of G.PRESET_KEYS) { await page.click(`${P} [data-gp-stop="${k}"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/${dev}-${k}.png` }); }
  await page.click(`${P} [data-gp-stop="permutohedron"]`); for (const v of [50, 150, 250, 400, 600]) { await page.locator(`${P} .gp-line-row input`).fill(String(v)); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/${dev}-stage-${v}.png` }); }
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`gperm OK: ${checks} checks`);
