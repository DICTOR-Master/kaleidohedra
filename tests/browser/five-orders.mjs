// The gold DICTO block under The Five Orders of Space (DICTO 2026-11-16, from the apps census of 2026-11-15), through the real UI by
// touch on a phone (390×844) and an iPad (820×1180), on all three doors (DOORS): DICTO → 3D+ shows DICTO's pieces, then a row of the
// five ring labels (Earth, Water, Fire, Wind, Void; big enough to touch, no arrows), then each ring's heading in its element colour with
// its worlds and lattices in book order (DICTO_SHELF), and Golamandalas (no book yet) after the rings. Tapping a ring label scrolls
// that ring's heading to the top of the list. Golden Breathing Pyrochlore and Golden Bodhi Pyrochlore Networks are listed once, in the
// gold block under Earth (Book One), no longer among either app's lattices, and each opens its world from there. The newest work
// (the Bitruncated 600-cell, The 4D Permutohedron) carries the "new" mark, nothing else. Every language: the labels translated and
// on one row. No console errors. Screenshots ($SHOTS): five-orders-<door>-<dev>.png; PREVIEW_PHONE / PREVIEW_DESKTOP, if set, get
// the Kaleidohedra door at phone and desktop width with the ring row in sight.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { t, LANG_ORDER } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/five-orders-shots';
mkdirSync(SH, { recursive: true });
const RINGS = ['earth', 'water', 'fire', 'wind', 'void'];
// DICTO_SHELF's order, by the actions of each entry's first row (the approved census order, Table 1)
const SHELF = {
  earth: ['tool:octetTrussWorld', 'tool:ocdStellaWorld', 'tool:icosaWorld', 'tool:dodecaWorld:dodeca13', 'tool:bodhiPyroWorld', 'tool:breathingWorld',
    'tool:octetWorld:caps', 'tool:thirteensWorld:icosa13', 'tool:stellaJewelWorld', 'tool:sunstarWorld', 'tool:octetBuildWorld:caps', 'tool:targetsWorld',
    'tool:shellsWorld', 'tool:pieceType:dictofcc', 'tool:pieceType:dictohex'],
  water: ['tool:dictonicWorld', 'tool:globalWebWorld', 'tool:bloomWorld', 'tool:upWorld', 'tool:vajrayanaWorld', 'tool:doubleVisionWorld', 'tool:cyclesWorld',
    'tool:theaetetusWorld', 'tool:chainsWorld:karma', 'tool:starCoresWorld'],
  fire: ['tool:stackingsWorld', 'tool:hexoctWorld', 'tool:bitruncWorld', 'tool:perm4World'],
  wind: ['tool:platonicMixWorld', 'tool:reuleauxWorld', 'tool:aristotleWorld', 'tool:roofFoldWorld', 'tool:studiesWorld'],
  void: ['tool:goldenWorld', 'tool:whiteQueenWorld'],
};
const b = await chromium.launch();
let checks = 0;
async function open(page, door) {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  await page.goto(`${BASE}/index.html?site=${door}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('.dicto-ring').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForSelector('.dicto-ring-jump'); await page.waitForTimeout(400);
  return errors;
}
// The gold block, read from the page: ring headings, each ring's entries (first action of each row or section), the jump row.
const readGold = (page) => page.evaluate(() => {
  const gold = document.querySelector('.dim-wizard-body .dicto-block.dicto-gold');
  const rings = {}; let ring = null;
  for (const el of gold.children) {
    if (el.classList.contains('dicto-ring')) { ring = el.dataset.ring ?? 'none'; rings[ring] = []; continue; }
    if (!ring) continue;
    if (el.matches('[data-action]') && !el.classList.contains('dim-wizard-piece')) rings[ring].push(el.dataset.action);
    else if (el.classList.contains('dim-wizard-section')) { let n = el.nextElementSibling; rings[ring].push(n.dataset.action); }
  }
  const heads = [...gold.querySelectorAll('.dicto-ring[data-ring]')].map((h) => ({ ring: h.dataset.ring, colour: getComputedStyle(h).borderLeftColor }));
  const jump = [...gold.querySelectorAll('.dicto-ring-jump [data-ring-jump]')].map((x) => { const r = x.getBoundingClientRect(); return { ring: x.dataset.ringJump, w: r.width, h: r.height, top: r.top, text: x.textContent.trim() }; });
  const kinds = [...gold.querySelectorAll('.dim-wizard-kind')].map((k) => k.textContent);
  const news = [...gold.querySelectorAll('.dicto-new')].map((n) => n.closest('[data-action]')?.dataset.action ?? n.closest('.dim-wizard-section')?.nextElementSibling?.dataset.action);
  const order = [...gold.children].map((c) => c.className.split(' ')[0]);
  return { rings, heads, jump, kinds, news, firstRingAt: order.indexOf('dicto-ring-jump'), piecesAt: order.findIndex((c, i) => gold.children[i].matches('[data-family="DICTO_PIECES"]')) };
});

for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse,polyhedraverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, door);
    const g = await readGold(page);
    // the rings in book order, each heading in its element colour, the entries as DICTO_SHELF, Golamandalas after them
    assert.deepEqual(g.heads.map((h) => h.ring), RINGS, `${tag}: five ring headings in order`);
    assert.deepEqual(g.heads.map((h) => h.colour), ['rgb(72, 142, 72)', 'rgb(58, 112, 205)', 'rgb(205, 62, 40)', 'rgb(232, 200, 82)', 'rgb(138, 92, 196)'], `${tag}: element colours`);
    for (const r of RINGS) assert.deepEqual(g.rings[r], SHELF[r], `${tag}: ${r} in book order`);
    assert.deepEqual(g.rings.none, ['tool:mandalaWorld'], `${tag}: Golamandalas after the rings`);
    assert.equal(Object.values(g.rings).flat().length, 37, `${tag}: 37 entries`);
    assert.ok(g.piecesAt >= 0 && g.piecesAt < g.firstRingAt, `${tag}: DICTO's pieces first, then the ring row`);
    assert.ok(!g.kinds.includes(t('wiz.kind.worlds', 'en')) && !g.kinds.includes(t('wiz.kind.lattices', 'en')), `${tag}: rings instead of Worlds / Lattices`);
    assert.deepEqual(g.news.sort(), ['tool:bitruncWorld', 'tool:perm4World'], `${tag}: the "new" mark on the newest work only`);
    // the jump row: five labels on one row, big enough for a finger, no arrows
    assert.deepEqual(g.jump.map((j) => j.ring), RINGS, `${tag}: the jump row`);
    assert.ok(g.jump.every((j) => j.h >= 44 && j.w >= 44 && Math.abs(j.top - g.jump[0].top) < 1), `${tag}: one row of touch-size labels ${JSON.stringify(g.jump)}`);
    assert.ok(g.jump.every((j) => !/[◀▶‹›<>←→]/.test(j.text)), `${tag}: no arrows`);
    checks += 10;
    // the two Golden Pyrochlore worlds: once in the whole list, in the gold block only
    const where = await page.evaluate(() => ['tool:breathingWorld', 'tool:bodhiPyroWorld'].map((a) => [...document.querySelectorAll(`.dim-wizard-body [data-action="${a}"]`)]
      .map((el) => el.closest('.dicto-block')?.classList.contains('dicto-gold'))));
    assert.deepEqual(where, [[true], [true]], `${tag}: each pyrochlore world once, in the gold block`); checks++;
    // a tap on each ring label brings its heading to the top of the list (Void last: it may stop short when the list ends)
    for (const r of ['wind', 'fire', 'water', 'void', 'earth']) {
      await page.locator(`[data-ring-jump="${r}"]`).tap(); await page.evaluate(() => { delete document.querySelector('.dim-wizard-card').dataset.was; }); await page.waitForTimeout(200);
      // the smooth scroll glides for a second or two down a long list: wait until it rests
      await page.waitForFunction(() => { const c = document.querySelector('.dim-wizard-card'), was = c.dataset.was; c.dataset.was = c.scrollTop; return was === String(c.scrollTop); }, null, { polling: 300, timeout: 8000 });
      const pos = await page.evaluate((r) => { const card = document.querySelector('.dim-wizard-card'), h = document.querySelector(`.dicto-ring[data-ring="${r}"]`);
        const top = h.getBoundingClientRect().top - card.getBoundingClientRect().top, end = card.scrollTop + card.clientHeight >= card.scrollHeight - 2;
        return { top, end, h: card.clientHeight }; }, r);
      assert.ok((pos.top >= 0 && pos.top <= 40) || (pos.end && pos.top >= 0 && pos.top < pos.h), `${tag}: ${r} heading at the top after its tap ${JSON.stringify(pos)}`); checks++;
      if (r === 'earth') await page.screenshot({ path: `${SH}/five-orders-${door}-${dev}.png` });
    }
    // the rings row from Rhombiverse's own lattice list (another door): the pyrochlore worlds are not there either
    if (door !== 'rhombiverse' && dev === 'phone') {
      const latRow = page.locator('[data-lattices]');
      if (await latRow.count()) {
        await latRow.first().scrollIntoViewIfNeeded(); await latRow.first().tap(); await page.waitForTimeout(500);
        assert.equal(await page.locator('[data-action="tool:breathingWorld"], [data-action="tool:bodhiPyroWorld"]').count(), 0, `${tag}: not in Rhombiverse's lattice list`); checks++;
        await page.tap('.dim-wizard-back'); await page.waitForTimeout(500);
      }
    }
    // each Golden Pyrochlore world opens from the gold block
    for (const [action, panel] of [['tool:breathingWorld', '#worldbreathing-panel'], ['tool:bodhiPyroWorld', '#worldbodhipyro-panel']]) {
      if (!(await page.locator('.dim-wizard-overlay.open').count())) {
        await page.goto(`${BASE}/index.html?site=${door}`); await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
        await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
        if (!(await page.locator('.dicto-ring').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
        await page.waitForTimeout(400);
      }
      await page.locator('[data-ring-jump="earth"]').tap(); await page.waitForTimeout(700);
      const btn = page.locator(`.dicto-gold [data-action="${action}"]`); await btn.scrollIntoViewIfNeeded(); await btn.tap();
      await page.waitForTimeout(500);
      if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
      await page.waitForSelector(`${panel}.visible`, { timeout: 15000 }); checks++;
      await page.goto('about:blank');
    }
    assert.deepEqual(errors, [], `${tag}: console errors`);
    await page.close();
  }
}
// every language at phone width: the ring labels translated, on one row, inside the screen
{
  const page = await b.newPage({ viewport: { width: 360, height: 780 }, hasTouch: true, isMobile: true });
  const errors = await open(page, 'kaleidohedra');
  for (const L of LANG_ORDER) {
    await page.selectOption('.dim-wizard-header .lang-btn select', L); await page.waitForTimeout(500);
    const g = await readGold(page);
    const want = RINGS.map((r) => { const n = t(`wiz.ring.${r}`, L), k = { earth: '地', water: '水', fire: '火', wind: '風', void: '空' }[r]; return n === k ? k : k + n; });
    assert.deepEqual(g.jump.map((j) => j.text.replace(/\s+/g, '')), want.map((w) => w.replace(/\s+/g, '')), `${L}: ring labels`);
    const fit = await page.evaluate(() => [...document.querySelectorAll('.dicto-ring-btn')].map((x) => { const r = x.getBoundingClientRect(); return { l: r.left, r: r.right, over: x.scrollWidth - x.clientWidth }; }));
    assert.ok(fit.every((f) => f.l >= 0 && f.r <= 360 && f.over <= 1) && Math.abs(g.jump[0].top - g.jump[4].top) < 1, `${L}: the ring row fits ${JSON.stringify(fit)}`);
    const text = await page.locator('.dicto-gold').textContent();
    assert.ok(!/wiz\.(ring|new)/.test(text) && text.includes(t('wiz.ring.none', L)) && text.includes(t('wiz.new', L)), `${L}: translated`);
    if (L === 'ja') { await page.locator('[data-ring-jump="earth"]').tap(); await page.waitForTimeout(800); await page.screenshot({ path: `${SH}/five-orders-phone-ja.png` }); }
    checks++;
  }
  await page.selectOption('.dim-wizard-header .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors');
  await page.close();
}
// the previews for DICTO: the Kaleidohedra door, the ring row and Earth in sight
for (const [env, viewport, mobile] of [['PREVIEW_PHONE', { width: 390, height: 844 }, true], ['PREVIEW_DESKTOP', { width: 1280, height: 900 }, false]]) {
  if (!process.env[env]) continue;
  const page = await b.newPage({ viewport, hasTouch: mobile, isMobile: mobile, deviceScaleFactor: 2 });
  await open(page, 'kaleidohedra');
  await page.evaluate(() => { const card = document.querySelector('.dim-wizard-card'), j = document.querySelector('.dicto-ring-jump');
    card.scrollTop += j.getBoundingClientRect().top - card.getBoundingClientRect().top - 140; });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: process.env[env] });
  await page.close();
}
await b.close();
console.log(`five-orders OK (${checks} checks)`);
