// The HexOct family (paper #86, DICTO 2026-11-03) through the real UI, touch on phone (390×844) and iPad (820×1180), mouse on the
// desktop (1280×800). HexOct world (Kaleidohedra): ?open=hexoct:3C:A, #86's link, opens on pair A; the picker lists all six sets, #75's
// tiles and the five pairs by the paper's names (A · HexOct 3/8 … E · HexOct 1/10), each a full touch target, none hidden; a tap on
// each pair draws it solid as merged faces (one solid per tile, no seams), with its line under the picker; Helpers still shows the
// pieces; ?open=hexoct:3C, #75's link, still opens #75's tiles though a pair was picked before. HexOct kit (Polyhedraverse):
// ?open=hexoctkit:4H:B opens the kit with pair B; taps on the ghost place B's tiles (both the c- and the h-tile), a tap on pair A
// turns the same build into A's tiles; old #75 kit on the 75 button. Edges ≥ 1.5 px; no console errors.
// Screenshots in $SHOTS (default /tmp/hexfam-shots): <dev>-world-<set>.png, <dev>-picker.png, <dev>-kit-B.png, <dev>-kit-A.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/hexfam-shots';
mkdirSync(SH, { recursive: true });
const DEVICES = {
  phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 },
  ipad: { viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 },
  desktop: { viewport: { width: 1280, height: 800 } },
};
const NAMES = ['HexOct #75', 'A · HexOct 3/8', 'B · HexOct −1/8 (whole octahedra)', 'C · HexOct −1/8', 'D · HexOct −11/24', 'E · HexOct 1/10'];
const SETS = ['75', 'A', 'B', 'C', 'D', 'E'];
const W = '#worldhexoct-panel', K = '#worldhexoctkit-panel';
const b = await chromium.launch();
let checks = 0;
for (const [dev, opts] of Object.entries(DEVICES)) {
  const ctx = await b.newContext(opts), page = await ctx.newPage(), errors = [], touch = !!opts.hasTouch;
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  const press = (sel) => (touch ? page.tap(sel) : page.click(sel));
  const site = () => page.evaluate(async () => (await import('./src/app/site.js')).activeSite());
  const open = async (door, link, panel) => {
    await page.goto(`${BASE}/index.html?probe&site=${door}&open=${link}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 8000 }).then(() => page.keyboard.press('Enter')).catch(() => {});
    await page.waitForSelector(`${panel}.visible`, { timeout: 30000 }); await page.waitForTimeout(1500);
  };
  const world = () => page.evaluate(() => window.__hexoctProbe());
  const kit = () => page.evaluate(() => window.__hexoctKitProbe());

  // ---- the world: #86's link ----
  await open('kaleidohedra', 'hexoct:3C:A', W);
  assert.equal(await site(), 'kaleidohedra');
  let st = await world();
  assert.deepEqual([st.set, st.kind, st.whole, st.tiles], ['A', '3C', true, 72], `${dev}: #86's link opens pair A`);
  assert.ok(st.lineWidth >= 1.5, `${dev}: edges ${st.lineWidth}`); checks++;
  // the picker: every set, by name, in order, all visible and touchable
  const labels = await page.locator(`${W} [data-hx-set]`).allTextContents();
  assert.deepEqual(labels, NAMES, `${dev}: the picker lists every pair by its paper name`);
  for (const k of SETS) {
    const bx = await page.locator(`${W} [data-hx-set="${k}"]`).boundingBox();
    assert.ok(bx && bx.height >= 44 && bx.width >= 44 && bx.x >= 0 && bx.x + bx.width <= opts.viewport.width, `${dev} ${k}: on screen and touchable ${bx?.width}×${bx?.height}`);
  }
  assert.equal(await page.locator('[class*="arrow"], [aria-label*="Next"], [aria-label*="Previous"]').filter({ visible: true }).count(), 0, `${dev}: no arrows`);
  checks++;
  await page.locator(`${W} .hx-sets`).screenshot({ path: `${SH}/${dev}-picker.png` });
  for (const k of SETS) {
    await press(`${W} [data-hx-set="${k}"]`); await page.waitForTimeout(900);
    st = await world();
    assert.deepEqual([st.set, st.whole, await page.getAttribute(`${W} [data-hx-set="${k}"]`, 'aria-pressed')], [k, k !== '75', 'true'], `${dev}: pair ${k}`);
    const note = await page.locator(`${W} .hx-set-note`).textContent();
    assert.match(note, k === '75' ? /single point/ : new RegExp(`${NAMES[SETS.indexOf(k)].replace(/[()]/g, '.')} \\(paper #86`), `${dev} ${k}: its line`);
    checks++;
    await page.screenshot({ path: `${SH}/${dev}-world-${k}.png` });
  }
  // Helpers on a pair: the pieces as glass
  await press(`${W} [data-hx-set="C"]`); await page.waitForTimeout(600);
  await press(`${W} [data-hx-helpers]`); await page.waitForTimeout(800);
  st = await world(); assert.deepEqual([st.set, st.helpers, st.glass, st.whole], ['C', true, true, false], `${dev}: helpers on a pair`);
  assert.match(await page.locator(`${W} .hx-note`).textContent(), /tetrahedral pieces dark/);
  await page.screenshot({ path: `${SH}/${dev}-world-C-helpers.png` });
  await press(`${W} [data-hx-helpers]`); await page.waitForTimeout(600); checks++;
  // #75's link: #75's tiles, as always
  await open('kaleidohedra', 'hexoct:fib', W);
  st = await world(); assert.deepEqual([st.set, st.kind, st.whole, st.pieces], ['75', 'fib', false, 8 * 36], `${dev}: #75's link unchanged`); checks++;

  // ---- the kit in Polyhedraverse ----
  await open('polyhedraverse', 'hexoctkit:4H:B', K);
  assert.equal(await site(), 'polyhedraverse');
  st = await kit(); assert.deepEqual([st.set, st.fill], ['B', '4H'], `${dev}: kit link`);
  if ((st.tiles ?? []).length) { await press(`${K} [data-hk-clear]`); await page.waitForTimeout(500); }
  assert.deepEqual(await page.locator(`${K} [data-hx-set]`).allTextContents(), NAMES, `${dev}: the kit's picker`);
  for (let n = 1; n <= 12; n++) {
    const g = await page.evaluate(() => window.__hexoctKitScreen.ghost());
    assert.ok(g, `${dev}: ghost ${n} on screen`);
    if (touch) await page.touchscreen.tap(g.x, g.y); else await page.mouse.click(g.x, g.y);
    await page.waitForTimeout(450);
    st = await kit(); assert.equal(st.tiles.length, n, `${dev}: kit tile ${n} placed`);
    assert.equal(st.lastCorners.length, st.lastPlaced.type === 'c' ? 4 : 4, `${dev}: B's tile, 3 pieces with the octahedron in halves`);
  }
  assert.deepEqual([...new Set(st.tiles.map((x) => x[3]))].sort(), ['c', 'h'], `${dev}: both tiles of the pair placed`);
  assert.ok(st.lineWidth >= 1.5 && st.solid, `${dev}: kit edges`); checks++;
  await page.screenshot({ path: `${SH}/${dev}-kit-B.png` });
  await press(`${K} [data-hx-set="A"]`); await page.waitForTimeout(900);
  st = await kit(); assert.deepEqual([st.set, st.tiles.length], ['A', 12], `${dev}: the same build in pair A`);
  assert.equal(st.lastCorners.length, 2, `${dev}: A's tiles are two pieces`); checks++;
  await page.screenshot({ path: `${SH}/${dev}-kit-A.png` });
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  await ctx.close();
}
await b.close();
console.log(`hexoct-family: ${checks} checks passed`);
