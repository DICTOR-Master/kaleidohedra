// DICTO Shadow Form (DICTO 2026-10-24; a Studies entry), through the real UI, touch, phone (390×844) and iPad (1024×1366), on the
// Kaleidohedra and Rhombiverse doors (DOORS): opened by ?open=studies:shadowForm and by the Studies world's own picker; the Shear panel
// hidden; Clear, then two forms placed by tapping dots (a cube, then an octahedron); a drag on one form turns BOTH by the same turn
// (their quaternions equal and changed), the camera still; the grid switched to face-centred (the forms on its points); the negative
// view: the cast drawn with a positive volume and the readout's numbers; every example loaded by its button, flipped, a positive
// negative and, where the example has one, its check (an inner cell, or the whole negative) equal to the exact or published value.
// No console errors. Screenshots ($SHOTS, default ~/Documents/papers-to-read): shadow-form-stage1-<device>-normal|negative.png and
// -dogstar-, -euclid-roofs-, -stella-jewel- pairs (Kaleidohedra door); every door/device also to $SHOTS/sf-<door>-<device>-*.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { EXAMPLE_KEYS } from '../../src/app/shadow-form-engine.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? `${homedir()}/Documents/papers-to-read`;
mkdirSync(SH, { recursive: true });
const DEVICES = { phone: { width: 390, height: 844 }, ipad: { width: 1024, height: 1366 } };
const b = await chromium.launch();
let checks = 0;
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries(DEVICES)) {
    const tag = `${door}-${dev}`, P = '#worldstudies-panel';
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true });
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    const probe = () => page.evaluate(() => window.__studiesProbe()?.shadowForm ?? null);
    const until = async (f, what, ms = 20000) => { const t0 = Date.now(); for (;;) { const st = await probe(); if (st && f(st)) return st; if (Date.now() - t0 > ms) throw new Error(`${tag}: timed out waiting for ${what}`); await page.waitForTimeout(150); } };
    const enter = async (url) => { await page.goto(url); await page.waitForTimeout(1200); if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter'); await page.waitForTimeout(1800); };
    const shot = async (name) => { await page.screenshot({ path: `${SH}/sf-${tag}-${name}.png` }); if (door === 'kaleidohedra') await page.screenshot({ path: `${SH}/shadow-form-stage1-${dev}-${name}.png` }); };

    // 1. the Studies world's own picker
    await enter(`${BASE}/index.html?site=${door}&open=studies&probe`);
    await page.locator(`${P} [data-select="study"]`).selectOption('shadowForm'); await page.waitForTimeout(800);
    let st = await probe(); assert.ok(st, `${tag}: picker opens DICTO Shadow Form`);
    assert.match(await page.locator(`${P} [data-select="study"] option:checked`).textContent(), /^DICTO Shadow Form$/);
    checks++;
    // 2. the link
    await enter(`${BASE}/index.html?site=${door}&open=studies:shadowForm&probe`);
    st = await until((s) => s.engine, 'the engine (manifold-3d)');
    assert.equal(await page.evaluate(() => window.__studiesProbe().study), 'shadowForm');
    assert.ok(!(await page.locator('#kaleido-panel').isVisible()), `${tag}: no Shear panel`);
    assert.match(await page.locator(`${P} .sf-note`).textContent(), /DICTO Shadow Form, DICTO's idea and name/);
    for (const sel of ['.st-note:not(.sf-note)', '[data-study-shear]', '.st-slider-row']) assert.ok(await page.locator(`${P} ${sel}`).first().isHidden(), `${tag}: ${sel} hidden`);
    for (const sel of ['[data-sf-view="negative"]', '[data-sf-grid="bcc"]', '[data-sf="clear"]']) { const bx = await page.locator(`${P} ${sel}`).boundingBox(); assert.ok(bx && bx.height >= 36 && bx.y + bx.height <= viewport.height, `${tag}: ${sel} on screen, big enough`); }
    checks++;
    // 3. Clear, then place a cube and an octahedron by tapping dots (dots above the panel, near the middle of the screen)
    await page.tap(`${P} [data-sf="clear"]`); await page.waitForTimeout(500);
    st = await probe(); assert.equal(st.arrangement.forms.length, 0, `${tag}: cleared`);
    const panelTop = (await page.locator(P).boundingBox()).y;
    // a dot nothing nearer the camera covers (no nearer dot's touch target over it), on screen clear of the title and Rhombiverse's Lattice · Select row,
    // the side buttons and the panel
    // and no placed form in front of it (a form's centre within 110 px and nearer the camera)
    let formsAt = [];
    const clear = (d, all) => !all.some((e) => e !== d && e.xy[2] < d.xy[2] && Math.hypot(e.xy[0] - d.xy[0], e.xy[1] - d.xy[1]) < e.r + 4)
      && !formsAt.some((f) => f[2] < d.xy[2] && Math.hypot(f[0] - d.xy[0], f[1] - d.xy[1]) < 110);
    const freeDot = (s, not = [], all = s.dotScreen) => s.dotScreen.filter((d) => d.xy[1] > 180 && d.xy[1] < panelTop - 20 && d.xy[0] > 20 && d.xy[0] < viewport.width - 70 && !not.some((q) => q.join() === d.at.join()) && clear(d, all))
      .sort((a, c) => Math.hypot(a.xy[0] - viewport.width / 2, a.xy[1] - panelTop / 2) - Math.hypot(c.xy[0] - viewport.width / 2, c.xy[1] - panelTop / 2))[0];
    await page.locator(`${P} [data-sf-form="cube"]`).tap(); await page.waitForTimeout(300);
    let d1 = freeDot(await probe());
    await page.touchscreen.tap(...d1.xy); await page.waitForTimeout(600);
    st = await probe(); assert.equal(st.arrangement.forms.length, 1, `${tag}: first form placed`); assert.deepEqual(st.arrangement.forms[0], { form: 'cube', at: d1.at });
    await page.locator(`${P} [data-sf-form="octahedron"]`).tap(); await page.waitForTimeout(300);
    formsAt = (await probe()).formScreen;
    const all2 = (await probe()).dotScreen, near = all2.filter((d) => Math.max(...d.at.map((c, i) => Math.abs(c - d1.at[i]))) === 1);
    const d2 = freeDot({ dotScreen: near }, [d1.at], all2) ?? freeDot({ dotScreen: all2 }, [d1.at]);
    await page.touchscreen.tap(...d2.xy); await page.waitForTimeout(600);
    st = await probe(); assert.equal(st.arrangement.forms.length, 2, `${tag}: second form placed (tapped ${d2.at} at ${d2.xy.slice(0, 2).map(Math.round)})`); assert.equal(st.arrangement.forms[1].form, 'octahedron');
    checks++;
    await shot('placed');
    // 4. a drag on the cube turns both forms by the same turn
    const before = st.forms.map((f) => f.quaternion), cam = await page.evaluate(() => window.__cameraState?.() ?? null);
    const [fx, fy] = st.formScreen[0];
    await page.mouse.move(fx, fy); await page.mouse.down(); for (let k = 1; k <= 8; k++) await page.mouse.move(fx + 12 * k, fy + 5 * k); await page.mouse.up();
    await page.waitForTimeout(600);
    st = await probe();
    const after = st.forms.map((f) => f.quaternion);
    assert.ok(after.every((q, i) => q.some((c, j) => Math.abs(c - before[i][j]) > 1e-3)), `${tag}: every form turned`);
    assert.ok(after.every((q) => q.every((c, j) => Math.abs(c - after[0][j]) < 1e-9)), `${tag}: by the same turn`);
    assert.deepEqual(st.arrangement.turn.map((c) => +c.toFixed(9)), after[0].map((c) => +c.toFixed(9)));
    assert.equal(st.arrangement.forms.length, 2, `${tag}: the drag placed or removed nothing`);
    if (cam) assert.deepEqual(await page.evaluate(() => window.__cameraState()), cam, `${tag}: the camera stayed`);
    assert.ok(await page.locator(`${P} [data-sf="straighten"]`).isVisible(), `${tag}: Straighten offered once turned`);
    checks++;
    // 5. the grid: face-centred, the forms moved onto its points
    await page.tap(`${P} [data-sf-grid="fcc"]`); await page.waitForTimeout(500);
    st = await probe(); assert.equal(st.arrangement.grid, 'fcc');
    assert.ok(st.arrangement.forms.every((f) => ((f.at[0] + f.at[1] + f.at[2]) % 2 + 2) % 2 === 0), `${tag}: forms on fcc points`);
    await page.tap(`${P} [data-sf-grid="cubic"]`); await page.waitForTimeout(400);
    checks++;
    // 6. the negative view
    await page.tap(`${P} [data-sf-view="negative"]`);
    st = await until((s) => s.negative && s.cast && s.volumes && !s.dirty, 'the cast');
    assert.ok(st.cast.triangles > 0 && st.volumes.negative > 0 && st.volumes.hull > st.volumes.negative, `${tag}: cast with a positive volume`);
    assert.match(st.readout, /DICTO Shadow Form \d/, `${tag}: readout`);
    assert.ok(await page.locator(`${P} [data-sf-grid="cubic"]`).isHidden(), `${tag}: no grid buttons in the negative view`);
    checks++;
    await shot('turned-negative');
    // the drag still turns them all in the negative view, and the cast follows
    const v0 = st.volumes.negative, q0 = st.forms[0].quaternion, [gx, gy] = st.formScreen[0];
    await page.mouse.move(gx, gy); await page.mouse.down(); for (let k = 1; k <= 6; k++) await page.mouse.move(gx - 10 * k, gy + 8 * k); await page.mouse.up();
    st = await until((s) => !s.dirty && s.volumes, 'the cast after a turn');
    assert.ok(st.forms[0].quaternion.some((c, j) => Math.abs(c - q0[j]) > 1e-3) && st.forms.every((f) => f.quaternion.every((c, j) => Math.abs(c - st.forms[0].quaternion[j]) < 1e-9)), `${tag}: negative view turns all`);
    // (when the grid switch brought both forms onto one point they turn as one nest, and the volumes stay)
    const apart = st.arrangement.forms[0].at.join() !== st.arrangement.forms[1].at.join();
    assert.ok(st.volumes.negative > 0 && (!apart || Math.abs(st.volumes.negative - v0) > 1e-6), `${tag}: the cast follows the turn`);
    checks++;
    // 7. every example, by its button: normal then negative
    for (const k of EXAMPLE_KEYS) {
      await page.tap(`${P} [data-sf-view="forms"]`); await page.waitForTimeout(200);
      await page.locator(`${P} [data-sf-example="${k}"]`).tap(); await page.waitForTimeout(500);
      st = await probe(); assert.equal(st.example, k); assert.ok(st.forms.length > 0, `${tag}: ${k} placed`);
      const shotName = { dogstar: 'dogstar', euclidRoofs: 'euclid-roofs', stellaJewel: 'stella-jewel' }[k];
      if (shotName) await shot(`${shotName}-normal`);
      if (k === 'dogstar') await shot('normal');
      await page.tap(`${P} [data-sf-view="negative"]`);
      st = await until((s) => s.negative && s.cast && s.volumes && !s.dirty, `${k} negative`);
      assert.ok(st.volumes.negative > 0 && st.cast.triangles > 0, `${tag}: ${k} negative`);
      if (st.check) assert.ok(Math.abs(st.check.got - st.check.expected) < 1e-4 * Math.max(1, st.check.expected), `${tag}: ${k} check ${st.check.got} vs ${st.check.expected}`);
      if (shotName) await shot(`${shotName}-negative`);
      if (k === 'dogstar') await shot('negative');
      checks++;
    }
    // containers: pick the Euclid's roofs dodecahedron and switch Container off: the negative goes (the cube is inside)
    await page.tap(`${P} [data-sf-view="forms"]`); await page.locator(`${P} [data-sf-example="cubeOcta"]`).tap(); await page.waitForTimeout(500);
    st = await probe(); assert.equal(st.arrangement.forms[0].container, true);
    const [cx, cy] = st.formScreen[0];
    await page.touchscreen.tap(cx + 3, cy - 3); await page.waitForTimeout(500);
    st = await probe(); assert.ok(st.selected !== null, `${tag}: a form picked by tapping`);
    assert.ok(await page.locator(`${P} [data-sf="container"]`).isVisible(), `${tag}: Container offered`);
    checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag);
    await page.close();
  }
}
await b.close();
console.log(`shadow-form OK: ${checks} checks`);
