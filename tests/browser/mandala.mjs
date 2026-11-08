// The Mandala World (DICTO 2026-11-08) through the real UI on an iPad (1024 × 1366, touch):
// - Kaleidohedra door, DICTO → 3D+: the Mandala World card right after DICTONIC opens the world; the title, a minimise chevron, no
//   ◀ ▶ buttons, no paint, shear or lattice-view controls;
// - Yantra: 9 tetrahedra in 9 cones with 9 marma circles, opening between still positions; tapping along the one big slider reaches
//   the three still positions (the narrowed yantra, 18 meetings) and the turns between them;
// - the button group: Cleo sphere (20 yantras) and 81 sphere (80 + the bindu), the slider hidden there; a one-finger drag turns the sphere;
// - ?open=mandala:81 opens the 81 sphere directly. No console errors.
// Screenshots in $SHOTS (default /tmp/mandala-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/mandala-shots';
mkdirSync(SH, { recursive: true });
const IPAD = { viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true, deviceScaleFactor: 1 };
const P = '#worldmandala-panel';
const b = await chromium.launch();
const ctx = await b.newContext(IPAD), page = await ctx.newPage(), errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
page.on('dialog', (d) => d.accept());
let checks = 0;
const probe = () => page.evaluate(() => window.__mandalaProbe());
const shot = (name) => page.screenshot({ path: `${SH}/${name}.png` });
const enter = async (extra = '') => {
  await page.goto(`${BASE}/index.html?probe&site=kaleidohedra${extra}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }).catch(() => {});
  if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
  await page.waitForTimeout(800);
};
const keep = async () => {
  for (let i = 0; i < 3; i++) {
    if (!(await page.locator('#leave-dialog:not([hidden])').count())) return;
    const pick = (await page.locator('#leave-dialog [data-choice="fresh"]').count()) ? 'fresh' : (await page.locator('#leave-dialog [data-choice="keep"]').count()) ? 'keep' : 'continue';
    await page.tap(`#leave-dialog [data-choice="${pick}"]`); await page.waitForTimeout(900);
  }
};
// a tap on the slider's track where value v sits (the thumb is 40 px, so the track runs from 20 px in to 20 px from the end)
const tapSlider = async (v) => {
  const s = page.locator(`${P} [data-md-spin]`), bx = await s.boundingBox();
  const min = Number(await s.getAttribute('min')), max = Number(await s.getAttribute('max'));
  await page.touchscreen.tap(bx.x + 20 + ((v - min) / (max - min)) * (bx.width - 40), bx.y + bx.height / 2);
  await page.waitForTimeout(900);
};

// ---- the wizard card ----
await enter();
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:mandalaWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
assert.equal(worlds[0], 'tool:dictonicWorld', 'DICTONIC still first');
assert.equal(worlds[1], 'tool:mandalaWorld', 'the Mandala World right after DICTONIC'); checks += 2;
const card = page.locator('[data-action="tool:mandalaWorld"]').first(); await card.scrollIntoViewIfNeeded();
const cb = await card.boundingBox(); assert.ok(cb.width >= 44 && cb.height >= 44, 'touchable card'); checks++;
await shot('ipad-wizard');
await card.tap(); await page.waitForTimeout(400); await keep();
await page.waitForSelector(`${P}.visible`, { timeout: 30000 }); await page.waitForTimeout(1500);
assert.equal((await page.textContent('#hud-world-title')).trim(), 'Mandala World', 'title');
assert.equal(await page.evaluate(async () => (await import('./src/app/site.js')).activeSite()), 'kaleidohedra', 'in Kaleidohedra');
for (const sel of ['#hud-quick-lattice-view', '#shear-panel']) assert.ok(!(await page.locator(sel).isVisible().catch(() => false)), `${sel} hidden`);
assert.ok(await page.locator(`${P} .panel-min`).isVisible(), 'minimise chevron');
const texts = await page.locator(`${P} button`).evaluateAll((els) => els.filter((e) => e.offsetParent).map((e) => e.textContent));
assert.ok(!texts.some((x) => /[◀▶◁▷←→‹›«»]/.test(x)), `no arrow buttons (${texts.join(' | ')})`);
assert.deepEqual(texts.filter(Boolean), ['Yantra', 'Cleo sphere', '81 sphere'], 'one button group');
checks += 6;

// ---- Yantra: the spin slider ----
if ((await probe()).mode !== 'yantra') { await page.tap(`${P} [data-md-mode="yantra"]`); await page.waitForTimeout(800); }
let st = await probe();
assert.equal(st.mode, 'yantra'); assert.equal(st.tetrahedra, 9); assert.equal(st.cones, 9); assert.equal(st.marmaCircles, 9);
assert.equal(st.still, 0, 'opens between still positions'); assert.ok(st.sliderShown, 'the slider shows in the Yantra');
assert.ok(st.glass >= 9, 'the cones as glass'); assert.ok(Math.min(...st.lineWidths) >= 1, 'edges ≥ 1 px');
const sb = await page.locator(`${P} [data-md-spin]`).boundingBox();
assert.ok(sb.width >= 600 && sb.height >= 44, `a big long slider (${Math.round(sb.width)} × ${Math.round(sb.height)})`);
assert.ok(sb.y > 1366 * 0.6, 'at the bottom'); checks += 4;
await shot('ipad-yantra-open');
for (const [v, k] of [[60, 2], [0, 1], [120, 3]]) {
  await tapSlider(v); st = await probe();
  assert.equal(st.spin, v, `snapped to ${v}°`); assert.equal(st.still, k, `still position ${k}`); assert.equal(st.meetings, 18, '18 meetings');
  assert.match(await page.textContent(`${P} .md-caption`), new RegExp(`Still position ${k} of 3`));
  await page.waitForTimeout(600); await shot(`ipad-yantra-still-${k}`); checks += 3;
}
await tapSlider(95); st = await probe();
assert.equal(st.still, 0, 'between still positions'); assert.ok(Math.abs(st.spin - 95) < 4, `turned ${st.spin}`); assert.equal(st.meetings, 0);
assert.match(await page.textContent(`${P} .md-caption`), /^Turned \d+°/); checks += 2;
await page.waitForTimeout(600); await shot('ipad-yantra-turned');

// ---- the spheres ----
await page.tap(`${P} [data-md-mode="cleo"]`); await page.waitForTimeout(1500);
st = await probe();
assert.equal(st.mode, 'cleo'); assert.equal(st.yantras, 20); assert.ok(Math.abs(st.capDegrees - 20.9052) < 1e-3); assert.ok(!st.sliderShown, 'no slider on the sphere');
assert.ok(!(await page.locator(`${P} [data-md-spin]`).isVisible()), 'slider hidden'); checks += 2;
await shot('ipad-cleo');
// one finger drags the sphere round (the view turns)
const before = await page.screenshot();
const cdp = await ctx.newCDPSession(page);
const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
await touch('touchStart', 300, 400);
for (let k = 1; k <= 12; k++) { await touch('touchMove', 300 + k * 25, 400 + k * 6); await page.waitForTimeout(30); }
await touch('touchEnd'); await page.waitForTimeout(900);
assert.ok(!before.equals(await page.screenshot()), 'a drag turns the sphere'); checks++;
await shot('ipad-cleo-turned');
await page.tap(`${P} [data-md-mode="sphere81"]`); await page.waitForTimeout(1500);
st = await probe();
assert.equal(st.mode, 'sphere81'); assert.equal(st.yantras, 80); assert.equal(st.bindu, 1); assert.equal(st.total, 81);
assert.equal(st.corners, 42); assert.equal(st.edges, 120); assert.ok(!st.sliderShown); checks += 2;
assert.match(await page.textContent(`${P} .md-caption`), /bindu at the centre: 81/);
await shot('ipad-81');
// back to the Yantra: the slider is back
await page.tap(`${P} [data-md-mode="yantra"]`); await page.waitForTimeout(800);
assert.ok(await page.locator(`${P} [data-md-spin]`).isVisible(), 'slider back in the Yantra'); checks++;

// ---- the direct link ----
await enter('&open=mandala:81'); await keep();
await page.waitForSelector(`${P}.visible`, { timeout: 30000 }); await page.waitForTimeout(1500);
st = await probe();
assert.equal(st.mode, 'sphere81', '?open=mandala:81'); checks++;
await shot('ipad-link-81');
await enter('&open=mandala'); await keep();
await page.waitForSelector(`${P}.visible`, { timeout: 30000 }); await page.waitForTimeout(1500);
st = await probe();
assert.deepEqual([st.mode, st.spin], ['yantra', 30], '?open=mandala'); checks++;

assert.deepEqual(errors, [], 'no console errors');
await b.close();
console.log(`mandala: ${checks} checks passed, screenshots in ${SH}`);
