// The Global Web of Bonds (DICTO 2026-10-25), through the real UI, touch, phone (390×844) and iPad (820×1180), on the Kaleidohedra and
// Rhombiverse doors (DOORS): next to DICTONIC in DICTO's list; the three network buttons (big enough to touch), one slider snapping to
// every stop (the pieces drawn = globalWebFamily, the caption naming the stop), the theorem statement, Web of bonds (rods = the shared
// edges/faces webOf finds), ▶ Loop holding at the switch point, the 📖 Almanac sheet (chart, bonds per piece, the switch picture) and
// its link to the Almanac entry; the ?open=globalWeb:<network> link. No console errors. Then screenshots ($SHOTS, default
// /tmp/global-web-shots) at TV 1280×720, iPad 820×1050 and phone 390×760 of each network at its switch point with the web on.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { GLOBAL_WEB_NETWORKS, GLOBAL_WEB_STOPS, SWITCH, globalWebFamily, globalWeb } from '../../src/app/world-global-web.js';
import { t } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/global-web-shots';
mkdirSync(SH, { recursive: true });
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
const swStop = (n) => GLOBAL_WEB_STOPS[n].find((s) => s.key === 'switch');
const P = '#worldglobalweb-panel';
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
  return errors;
}
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:globalWebWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.deepEqual(worlds.slice(0, 2), ['tool:dictonicWorld', 'tool:globalWebWorld'], `${tag}: next to DICTONIC`); checks++;
    await page.locator('[data-action="tool:globalWebWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    const probe = () => page.evaluate(() => window.__globalWebProbe());
    const slide = async (u) => { await page.locator(`${P} .ch-param-row input`).fill(String(u)); await page.waitForTimeout(500); };
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    for (const k of GLOBAL_WEB_NETWORKS) { const bx = await page.locator(`${P} [data-chains-kind="${k}"]`).boundingBox(); assert.ok(bx && bx.height >= 30, `${tag}: ${k} button`); }
    assert.ok(await page.locator(`${P} [data-select="part"]`).isHidden(), `${tag}: no view menu`);
    assert.match(await page.locator(`${P} .ch-size-label`).textContent(), /Layers/);
    for (const n of GLOBAL_WEB_NETWORKS) {
      if ((await probe()).kind !== n) { await page.tap(`${P} [data-chains-kind="${n}"]`); await page.waitForTimeout(800); }
      let st = await probe();
      assert.equal(st.kind, n); assert.equal(st.param.value, SWITCH[n], `${tag}: ${n} opens at the switch point`);
      assert.match(await page.locator(`${P} .thm-statement`).textContent(), /^Theorem \(/, `${tag}: ${n} statement`);
      for (const s of GLOBAL_WEB_STOPS[n]) {
        await slide(Math.max(0, Math.min(1000, s.u + (s.u < 1000 ? 9 : -9)))); st = await probe();
        assert.equal(st.param.u, s.u, `${tag}: ${n} snaps to ${s.key}`); assert.equal(st.param.value, s.v);
        assert.deepEqual(st.drawn, count(globalWebFamily(n, 2, s.v)), `${tag}: ${n} ${s.key} pieces`);
        assert.ok((await caption()).startsWith(t(`globalWeb.stop.${n}.${s.key}`, 'en')), `${tag}: ${n} ${s.key} caption`); checks++;
      }
      // the web at the switch point: one rod per shared edge / face, only unlike bonds
      await slide(swStop(n).u);
      await page.tap(`${P} [data-chains-web]`); await page.waitForTimeout(800);
      st = await probe(); const web = globalWeb(n, 2, SWITCH[n]).filter((w) => w[2] > 1e-9);
      assert.equal(st.web, true); assert.equal(st.drawn.web, web.length, `${tag}: ${n} rods`); assert.ok(web.every((w) => w[4] === 'ab'), 'only unlike bonds'); checks++;
      // Loop holds at the switch point
      await slide(swStop(n).u - 40);
      await page.tap(`${P} [data-chains-loop]`);
      let held = false;
      for (let i = 0; i < 40 && !held; i++) { await page.waitForTimeout(100); held = (await probe()).param.u === swStop(n).u; }
      assert.ok(held, `${tag}: ${n} loop reaches the switch point`);
      await page.waitForTimeout(900); assert.equal((await probe()).param.u, swStop(n).u, `${tag}: ${n} loop holds there`);
      await page.tap(`${P} [data-chains-loop]`); await page.waitForTimeout(300); assert.equal((await probe()).looping, false); checks++;
      await page.tap(`${P} [data-chains-web]`); await page.waitForTimeout(400);
      // the Almanac sheet
      await page.tap(`${P} .thm-almanac-open`); await page.waitForTimeout(300);
      assert.ok(await page.locator('.thm-almanac .thm-chart svg').isVisible()); assert.equal(await page.locator('.thm-almanac .thm-chart polyline').count(), 3);
      assert.ok(await page.locator('.thm-almanac .thm-flip').isVisible(), `${tag}: ${n} switch picture`);
      assert.match(await page.locator('.thm-almanac .thm-count').textContent(), /bonds/);
      await page.locator('.thm-almanac .thm-alm-close').tap(); await page.waitForTimeout(300); checks++;
    }
    await page.tap(`${P} .thm-almanac-open`); await page.waitForTimeout(300);
    await page.locator('.thm-almanac .thm-alm-entry').tap(); await page.waitForTimeout(700);
    assert.match(await page.locator('body').innerText(), /The Global Web of Bonds: how bonds hand over across crystal networks/, `${tag}: Almanac entry`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
// the link, and the screenshots: each network at its switch point with the web on
for (const [dev, viewport] of Object.entries({ tv: { width: 1280, height: 720 }, ipad: { width: 820, height: 1050 }, phone: { width: 390, height: 760 } })) {
  for (const n of GLOBAL_WEB_NETWORKS) {
    const page = await b.newPage({ viewport, hasTouch: dev !== 'tv', isMobile: dev !== 'tv' });
    const errors = await open(page, `&site=kaleidohedra&open=globalWeb:${n}`);
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    const st = await page.evaluate(() => window.__globalWebProbe());
    assert.equal(st.kind, n, `?open=globalWeb:${n}`); assert.equal(st.param.value, SWITCH[n]);
    await page.locator(`${P} [data-chains-web]`).click(); await page.waitForTimeout(1800);
    await page.screenshot({ path: `${SH}/${dev}-${n}-switch-web.png` });
    assert.deepEqual(errors, [], `${dev} ${n}: console errors`); checks++;
    await page.close();
  }
}
await b.close();
console.log(`global-web OK: ${checks} checks`);
