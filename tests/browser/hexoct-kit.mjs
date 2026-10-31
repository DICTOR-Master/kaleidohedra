// The HexOct kit (DICTO 2026-11-01; paper #75) through the real UI, touch, phone (390×844) and iPad (820×1180), Polyhedraverse door:
// first among DICTO's pieces; opens in Polyhedraverse with Free and the c-tile picked, a see-through ghost where the first tile goes;
// a tap on the ghost places it, taps on placed tiles add the picked tile on that side (each layer one kind); the tile buttons hide
// while a helper shows. The 4H helper: its ghost is always the plan's next tile, of its layer's kind, and a tap on it lands exactly
// that tile (its corners the ghost's); the own field (shown only for Your own) and a build that leaves the plan (3C after 4H).
// Edges ≥ 1.5 px, solid tiles, see-through ghost; no paint, shear or lattice-view controls; no console errors.
// Screenshots in $SHOTS (default /tmp/hexkit-shots): <dev>-free.png, <dev>-4h-ghost.png, <dev>-own.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/hexkit-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldhexoctkit-panel';
const b = await chromium.launch();
let checks = 0;
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
  const ctx = await b.newContext({ viewport, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), page = await ctx.newPage(), errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  const probe = () => page.evaluate(() => window.__hexoctKitProbe());
  const site = () => page.evaluate(async () => (await import('./src/app/site.js')).activeSite());
  const tapAt = async (pt) => { await page.touchscreen.tap(pt.x, pt.y); await page.waitForTimeout(450); };
  // faces in sight: on screen and above the panel
  const facesInSight = async () => { const top = (await page.locator(P).boundingBox()).y; return (await page.evaluate(() => window.__hexoctKitScreen.faces())).filter((f) => f.x > 10 && f.x < viewport.width - 10 && f.y > 70 && f.y < top - 10); };
  const tapGhost = async () => { const g = await page.evaluate(() => window.__hexoctKitScreen.ghost()); assert.ok(g, `${dev}: a ghost on screen`); await tapAt(g); };
  await page.goto(`${BASE}/index.html?probe&site=polyhedraverse`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('[data-family="DICTO_PIECES"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  const fam = page.locator('[data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await page.waitForTimeout(800);
  assert.equal(await page.locator('.poly-section').first().getAttribute('data-section'), 'hexoct-kit', `${dev}: the kit first`); checks++;
  await page.locator('[data-hexoct-kit]').first().tap(); await page.waitForTimeout(400);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'HexOct kit', `${dev}: title`);
  assert.equal(await site(), 'polyhedraverse', `${dev}: in Polyhedraverse`);
  for (const sel of ['#hud-quick-lattice-view', '#shear-panel']) assert.ok(!(await page.locator(sel).isVisible().catch(() => false)), `${dev}: ${sel} hidden`);
  checks++;
  // Free, the c-tile picked, the ghost where the first tile goes; buttons big enough to touch
  let st = await probe();
  assert.deepEqual([st.fill, st.piece, st.tiles.length, st.ghost], ['free', 'c', 0, { k: 0, i: 0, j: 0, type: 'c' }], `${dev}: empty, free`);
  assert.ok(await page.locator(`${P} [data-hk-piece="h"]`).isVisible() && !(await page.locator(`${P} .hk-own`).isVisible()), `${dev}: tile buttons, no field`);
  for (const sel of ['[data-hk-fill="4H"]', '[data-hk-piece="c"]']) { const bx = await page.locator(`${P} ${sel}`).boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 36, `${dev} ${sel}: touchable ${bx.width}×${bx.height}`); }
  assert.ok(st.ghostOpacity < 0.5 && st.solid, `${dev}: ghost see-through`); checks++;
  await page.tap(`${P} [data-hk-piece="h"]`); await page.waitForTimeout(300);
  assert.equal((await probe()).ghost.type, 'h'); await page.tap(`${P} [data-hk-piece="c"]`); await page.waitForTimeout(300);
  // a tap on the ghost places the first tile; taps on placed tiles add more beside, above or below
  await tapGhost();
  st = await probe(); assert.deepEqual(st.tiles, [[0, 0, 0, 'c']], `${dev}: the first tile`);
  assert.ok(st.lineWidth >= 1.5, `${dev}: edges ${st.lineWidth} px`); checks++;
  for (let n = 2; n <= 4; n++) {
    const f = (await facesInSight()).reduce((x, y) => (y.facing > x.facing ? y : x));
    await tapAt(f);
    st = await probe(); assert.equal(st.tiles.length, n, `${dev}: tile ${n} placed by a tap`);
  }
  assert.ok(st.tiles.every((x) => x[3] === 'c'));
  // an h-tile from a top face: it goes into a layer of its own
  await page.tap(`${P} [data-hk-piece="h"]`); await page.waitForTimeout(300);
  const top = (await facesInSight()).reduce((x, y) => (y.ny > x.ny ? y : x));
  await tapAt(top);
  st = await probe();
  const h = st.tiles.filter((x) => x[3] === 'h');
  assert.equal(h.length, 1, `${dev}: an h-tile placed`);
  assert.ok(st.tiles.filter((x) => x[0] === h[0][0]).every((x) => x[3] === 'h'), `${dev}: one kind per layer`); checks++;
  await page.screenshot({ path: `${SH}/${dev}-free.png` });
  // the 4H helper: Clear, then each ghost is the plan's next tile; a tap lands exactly it
  await page.tap(`${P} [data-hk-clear]`); await page.waitForTimeout(300);
  await page.tap(`${P} [data-hk-fill="4H"]`); await page.waitForTimeout(700);
  st = await probe();
  assert.deepEqual([st.fill, st.types, st.tiles.length, st.next], ['4H', 'chchchch', 0, { k: 0, i: 0, j: 0, type: 'c' }], `${dev}: 4H from the start`);
  assert.ok(!(await page.locator(`${P} [data-hk-piece="c"]`).isVisible()), `${dev}: no tile buttons with a helper`); checks++;
  for (let n = 0; n < 12; n++) {
    const before = await probe();
    assert.equal(before.ghost.type, 'chchchch'[before.ghost.k], `${dev}: the ghost's kind is its layer's`);
    assert.deepEqual(before.ghost, { k: Math.floor(n / 9), i: n % 3, j: Math.floor((n % 9) / 3), type: 'chchchch'[Math.floor(n / 9)] }, `${dev}: plan order ${n}`);
    await tapGhost();
    const after = await probe();
    assert.equal(after.tiles.length, n + 1, `${dev}: tile ${n + 1} by a tap on the ghost`);
    assert.deepEqual(after.lastPlaced, before.ghost);
    assert.deepEqual(after.lastCorners, before.ghostCorners, `${dev}: the tile that lands is the ghost`);
  }
  checks++;
  st = await probe();
  assert.deepEqual(st.next, { k: 1, i: 0, j: 1, type: 'h' }, `${dev}: next an h-tile in layer 2`);
  assert.match(await page.locator(`${P} .hk-caption`).textContent(), /next: the h-tile \(blue\), layer 2 of 8 · 12 of 72 tiles placed/); checks++;
  await page.screenshot({ path: `${SH}/${dev}-4h-ghost.png` });
  // the viewer's own sequence (the field shows only then): chh agrees with the build so far; 3C does not
  await page.tap(`${P} [data-hk-fill="own"]`); await page.waitForTimeout(400);
  assert.ok(await page.locator(`${P} .hk-own`).isVisible(), `${dev}: the field`);
  await page.locator(`${P} .hk-own`).fill('C H H'); await page.tap(`${P} [data-hk-own-go]`); await page.waitForTimeout(600);
  st = await probe(); assert.deepEqual([st.fill, st.own, st.types, st.conflict, st.next?.k], ['own', 'chh', 'chhchh', null, 1], `${dev}: own`); checks++;
  await page.screenshot({ path: `${SH}/${dev}-own.png` });
  await page.tap(`${P} [data-hk-fill="3C"]`); await page.waitForTimeout(400);
  st = await probe(); assert.deepEqual([st.conflict, st.ghost], [1, null], `${dev}: 3C leaves the build at layer 2`);
  assert.match(await page.locator(`${P} .hk-caption`).textContent(), /leaves 3C at layer 2/); checks++;
  assert.deepEqual(errors, [], `${dev}: console errors`); checks++;
  await ctx.close();
}
await b.close();
console.log(`hexoct-kit: ${checks} checks passed`);
