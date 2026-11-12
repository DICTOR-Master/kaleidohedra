// Generalized Permutohedra (src/app/world-gperm.js), through the real UI, by touch, on a phone (390×844) and an iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors: listed in Kaleidohedra's block, first among its worlds; opens on the permutohedron (24, 36, 14,
// fills space); the big slider at the bottom, its wall marked on the track; dragged with a finger the shape stays 14-faced and the badge
// turns to "does not"; at the end the associahedron (14, 21, 9) with the wall's 5 faces named; each stop tapped gives its known counts and
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
// the slider dragged with a finger from its thumb to `to` (0..1000)
async function drag(page, to, steps = 6) {
  const input = page.locator(`${P} .gp-line-row input`), box = await input.boundingBox(), y = box.y + box.height / 2;
  const at = (v) => box.x + 20 + ((box.width - 40) * v) / 1000;
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
    // the big slider at the bottom, its wall marked at the associahedron end
    const slider = page.locator(`${P} .gp-line-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`);
    const wall = await page.locator(`${P} .gp-wall`).boundingBox();
    assert.equal(await page.locator(`${P} .gp-wall`).count(), 1, `${tag}: one wall`);
    assert.ok(Math.abs(wall.x + wall.width / 2 - (sb.x + sb.width - 20)) < 3, `${tag}: the wall at the associahedron end ${JSON.stringify({ wall, sb })}`);
    assert.deepEqual(st.walls.map((w) => [w.t, w.faces.length, w.source]), [[1, 5, 'live']]);
    for (const k of G.PRESET_KEYS) { const bx = await page.locator(`${P} [data-gp-stop="${k}"]`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44 && bx.x >= 0 && bx.x + bx.width <= viewport.width, `${tag}: ${k} touchable, on screen`); }
    await onScreen(page, `${tag} permutohedron`);
    checks++;
    // a finger drags halfway: still 14 faces, no longer centrally symmetric
    await drag(page, 500); st = await probe(page);
    assert.ok(st.onLine && st.s > 400 && st.s < 600 && !st.stop, `${tag}: halfway ${st.s}`);
    assert.deepEqual([st.f, st.fills, st.symmetric, st.inFamily], [[24, 36, 14], false, false, true], `${tag}: halfway shape`);
    assert.equal(await page.locator(`${P} .gp-badge`).textContent(), t('gp.badge.no', 'en'));
    assert.ok((await page.locator(`${P} .ch-param-caption`).textContent()).includes('of the way to the associahedron'), `${tag}: caption between`);
    await onScreen(page, `${tag} halfway`);
    // to the end: the associahedron, the wall's 5 faces named
    await drag(page, 1015); st = await probe(page);
    assert.deepEqual([st.stop, st.s, st.f], ['associahedron', 1000, [14, 21, 9]], `${tag}: the end`);
    const cap = await page.locator(`${P} .ch-param-caption`).textContent();
    assert.ok(cap.includes('5 faces vanish here') && cap.includes('{1,3}') && cap.includes('{1,3,4}'), `${tag}: wall caption (${cap})`);
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
    await drag(page, 300); st = await probe(page);
    assert.ok(st.onLine && st.stop === null && st.f[2] === 14, `${tag}: back on the line`); checks++;
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
  await page.click(`${P} [data-gp-stop="permutohedron"]`); await page.locator(`${P} .gp-line-row input`).fill('500'); await page.waitForTimeout(900);
  await page.screenshot({ path: `${SH}/${dev}-halfway.png` });
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`gperm OK: ${checks} checks`);
