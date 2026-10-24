// DICTONIC (DICTO 2026-10-23), through the real UI, touch, phone (390×844) and iPad (820×1180), on the Kaleidohedra and Rhombiverse
// doors (DOORS): first in DICTO's list; the bond buttons (big enough to touch) and one slider, with Layers (up to 6, 4 on a phone) and
// Top layer sliders (DICTO 2026-10-25), a Web of bonds button (rods = the shared faces webOf finds) and a Loop button that runs the slider;
// Golden opens at x = τ (Icosaxes + Unborn Axes named in the caption), X-ray shows the cores and AXE pyramids there, the slider snaps
// to x = 1 (Kelvin) and reaches x → 0 and x → ∞, each drawing the pieces goldenFamily builds; Keyed has no slider and its "Set keys
// one by one" opens the Golden split; Delian opens at the Delian bond (Samson + Delilah in the caption) and snaps to the octet, the
// pieces as delianFamily builds them. No console errors. Screenshots to $SHOTS (default /tmp/dictonic-shots):
// <door>-<device>-golden-tau|golden-kelvin|golden-xray|keyed|delian-bond|delian-octet.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { goldenFamily, delianFamily, GOLDEN_STOPS, DELIAN_STOPS, DICTONIC_VIEWS } from '../../src/app/world-dictonic.js';
import { goldenPieces } from '../../src/app/world-octet.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/dictonic-shots';
mkdirSync(SH, { recursive: true });
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
const gStop = (k) => GOLDEN_STOPS.find((s) => s.key === k), dStop = (k) => DELIAN_STOPS.find((s) => s.key === k);
const DEVICES = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const b = await chromium.launch();
let checks = 0;
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries(DEVICES)) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true });
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(`${BASE}/index.html?site=${door}&probe`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
    const tag = `${door}-${dev}`, P = '#worlddictonic-panel';
    await page.waitForSelector('.dim-wizard-overlay.open');
    await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:dictonicWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[0], 'tool:dictonicWorld', `${tag}: DICTONIC first in DICTO's list`); checks++;
    await page.locator('[data-action="tool:dictonicWorld"]').first().tap();
    await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    const probe = () => page.evaluate(() => window.__dictonicProbe());
    const shot = (name) => page.screenshot({ path: `${SH}/${tag}-${name}.png` });
    const slide = async (u) => { await page.locator(`${P} .ch-param-row input`).fill(String(u)); await page.waitForTimeout(700); };
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    let st = await probe();
    assert.equal(st.kind, 'golden'); assert.equal(st.param.u, gStop('tau').u); assert.equal(st.param.value, gStop('tau').v);
    assert.deepEqual(st.drawn, count(goldenFamily(2, gStop('tau').v)), `${tag}: golden at τ`);
    assert.match(await caption(), /Icosaxes .*Unborn Axes/, `${tag}: τ caption names the pieces`);
    for (const k of ['golden', 'keyed', 'delian']) { const bx = await page.locator(`${P} [data-chains-kind="${k}"]`).boundingBox(); assert.ok(bx && bx.height >= 30, `${tag}: ${k} button`); }
    assert.ok(await page.locator(`${P} [data-select="part"]`).isHidden(), `${tag}: no view menu`);
    for (const sel of ['.ch-size-row', '.ch-shells-row']) assert.ok(await page.locator(`${P} ${sel}`).isVisible(), `${tag}: ${sel} shown`);
    assert.match(await page.locator(`${P} .ch-size-label`).textContent(), /Layers/); assert.match(await page.locator(`${P} .ch-shells-label`).textContent(), /Top layer/);
    assert.equal(st.maxSize, dev === 'phone' ? 4 : 6, `${tag}: layer cap`);
    assert.equal(await page.locator(`${P} .ch-size-row input`).getAttribute('max'), String(st.maxSize));
    assert.ok(await page.locator(`${P} .ch-param-row input`).isVisible(), `${tag}: the slider`);
    // the theorem block (DICTO 2026-10-25): statement, live chart with the marker, bonds per piece; no Delian switch picture on Golden
    assert.match(await page.locator(`${P} .thm-statement`).textContent(), /Theorem \(golden\)/, `${tag}: golden statement`);
    // upright screens: the evidence folds behind a button (it would cover the picture); open it
    assert.ok(await page.locator(`${P} .thm-evidence`).isHidden(), `${tag}: evidence folded on an upright screen`);
    await page.tap(`${P} .thm-evidence-toggle`); await page.waitForTimeout(300);
    assert.ok(await page.locator(`${P} .thm-chart svg`).isVisible(), `${tag}: the chart`);
    assert.equal(await page.locator(`${P} .thm-chart polyline`).count(), 3, `${tag}: three bond curves`);
    assert.match(await page.locator(`${P} .thm-count`).textContent(), /8 bonds to the other kind \+ 6/, `${tag}: bonds per piece`);
    assert.ok(await page.locator(`${P} .thm-flip`).isHidden(), `${tag}: no switch picture for golden`);
    checks++;
    await shot('golden-tau');
    // X-ray at τ: the icosahedron / Unborn cores and the AXE pyramids
    await page.tap('#xray-toggle'); await page.waitForTimeout(900);
    st = await probe(); assert.equal(st.xray, true);
    assert.deepEqual(st.drawn, count(goldenFamily(2, gStop('tau').v, true)), `${tag}: X-ray parts`);
    assert.ok(st.drawn.axe > 0 && st.drawn.mxIco > 0 && st.drawn.mxUnborn > 0); checks++;
    await shot('golden-xray');
    await page.tap('#xray-toggle'); await page.waitForTimeout(700);
    // the slider snaps: 512 → x = 1 (Kelvin)
    await slide(512);
    st = await probe(); assert.equal(st.param.u, 500, `${tag}: snapped to Kelvin`); assert.equal(st.param.value, 1);
    assert.deepEqual(st.drawn, count(goldenFamily(2, 1)), `${tag}: Kelvin pieces`); assert.match(await caption(), /Kelvin/); checks++;
    await shot('golden-kelvin');
    for (const k of ['zero', 'inf']) {
      await slide(gStop(k).u); st = await probe();
      assert.equal(st.param.value, gStop(k).v); assert.deepEqual(st.drawn, count(goldenFamily(2, gStop(k).v)), `${tag}: golden ${k}`); checks++;
    }
    await slide(300); st = await probe(); assert.equal(st.param.u, 300, `${tag}: between stops`); assert.deepEqual(st.drawn, count(goldenFamily(2, st.param.value))); checks++;
    // Keyed: no slider; all keyed
    await page.tap(`${P} [data-chains-kind="keyed"]`); await page.waitForTimeout(900);
    st = await probe(); assert.equal(st.kind, 'keyed'); assert.equal(st.param, null);
    assert.ok(await page.locator(`${P} .ch-param-row`).isHidden(), `${tag}: no slider for Keyed`);
    assert.deepEqual(st.drawn, count(goldenPieces(2, { pattern: 'allKeyed' })), `${tag}: keyed pieces`); checks++;
    await shot('keyed');
    // Delian: opens at the bond, snaps to the octet
    await page.tap(`${P} [data-chains-kind="delian"]`); await page.waitForTimeout(900);
    st = await probe(); assert.equal(st.kind, 'delian'); assert.equal(st.param.value, dStop('bond').v);
    assert.deepEqual(st.drawn, count(delianFamily(2, dStop('bond').v)), `${tag}: Delian bond pieces`);
    assert.match(await caption(), /Samson 0\.2357 · Delilah 0\.2357/, `${tag}: bond caption`); checks++;
    await shot('delian-bond');
    await slide(345); st = await probe();
    assert.equal(st.param.value, 1 / 3, `${tag}: snapped to the octet`); assert.deepEqual(st.drawn, count(delianFamily(2, 1 / 3))); checks++;
    await shot('delian-octet');
    assert.match(await page.locator(`${P} .thm-statement`).textContent(), /Theorem \(Delian\)/);
    assert.ok(await page.locator(`${P} .thm-flip`).isVisible(), `${tag}: the switch picture`);
    assert.ok(await page.locator(`${P} .thm-flip.now`).count(), `${tag}: the switch picture glows at the octet`);
    assert.match(await page.locator(`${P} .thm-count`).textContent(), /Octahedron piece: 8 bonds · tetrahedron piece: 4 bonds/); checks++;
    // Web of bonds at the octet: one rod per shared face, only octahedron–tetrahedron bonds there
    await page.tap(`${P} [data-chains-web]`); await page.waitForTimeout(900);
    st = await probe(); assert.equal(st.web, true, `${tag}: web on`);
    assert.equal(st.drawn.web, DICTONIC_VIEWS.delian.web(2, { param: 1 / 3 }).filter((w) => w[2] > 1e-9).length, `${tag}: octet rods`);
    assert.match(await caption(), /shared face/); checks++;
    await shot('web-octet');
    await slide(dStop('bond').u); st = await probe();
    assert.equal(st.drawn.web, DICTONIC_VIEWS.delian.web(2, { param: dStop('bond').v }).filter((w) => w[2] > 1e-9).length, `${tag}: bond rods`); checks++;
    await shot('web-delian-bond');
    // Loop: the slider moves by itself until paused
    const u0 = st.param.u;
    await page.tap(`${P} [data-chains-loop]`); await page.waitForTimeout(1500);
    st = await probe(); assert.equal(st.looping, true); assert.notEqual(st.param.u, u0, `${tag}: loop moves the slider`);
    await page.tap(`${P} [data-chains-loop]`); await page.waitForTimeout(300);
    const u1 = (await probe()).param.u; await page.waitForTimeout(600);
    assert.equal((await probe()).param.u, u1, `${tag}: paused`); checks++;
    await page.tap(`${P} [data-chains-web]`); await page.waitForTimeout(600);
    // Layers: the largest the device allows
    await page.locator(`${P} .ch-size-row input`).fill(String(st.maxSize)); await page.waitForTimeout(2500);
    st = await probe(); assert.equal(st.size, st.maxSize);
    assert.deepEqual(st.drawn, count(delianFamily(st.maxSize, st.param.value)), `${tag}: ${st.maxSize} layers`); checks++;
    await shot(`layers-${st.maxSize}`);
    await page.locator(`${P} .ch-size-row input`).fill('2'); await page.waitForTimeout(900);
    await slide(dStop('octet').u);
    for (const k of ['rd', 'cube']) { await slide(dStop(k).u); st = await probe(); assert.deepEqual(st.drawn, count(delianFamily(2, dStop(k).v)), `${tag}: Delian ${k}`); checks++; }
    assert.equal(await page.locator(`${P} [data-chains-link]`).count(), 2, `${tag}: Samson and Delilah links`);
    // Keyed's "Set keys one by one" opens the Golden split
    await page.tap(`${P} [data-chains-kind="keyed"]`); await page.waitForTimeout(600);
    await page.tap(`${P} [data-chains-link="tool:octetWorld:goldenSplit"]`); await page.waitForTimeout(2500);
    if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="keep"]'); await page.waitForTimeout(1500); }
    assert.equal((await page.evaluate(() => window.__octetProbe())).kind, 'goldenSplit', `${tag}: Set keys one by one opens the Golden split`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag);
    await page.close();
  }
}
await b.close();
console.log(`dictonic OK: ${checks} checks`);
