// The Icosaxes Bloom (DICTO 2026-10-27, paper #59), through the real UI, touch, phone (390×844) and iPad (820×1180), on the Kaleidohedra
// and Rhombiverse doors (DOORS): right after the Stackings World in DICTO's list; three buttons (big enough to touch); the slider snaps to
// every stop (Bloom, Bud, Seed; Lotus Jewel Seed for Lotus Jewel Axes), twenty pieces drawn, the caption naming the stop; the Icosaxes
// Hexa views; ?open=bloom:<kind>. No console errors. Screenshots ($SHOTS, default /tmp/bloom-shots) at TV 1280×720, iPad 820×1050 and
// phone 390×760 of the Bud and the Lotus Hexa.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { BLOOM_KINDS, BLOOM_STOPS } from '../../src/app/world-bloom.js';
import { t } from '../../src/app/i18n.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/bloom-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldbloom-panel';
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
  return errors;
}
const total = (drawn) => Object.values(drawn).reduce((a, x) => a + x, 0);
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:bloomWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.deepEqual(worlds.slice(0, 4), ['tool:dictonicWorld', 'tool:globalWebWorld', 'tool:stackingsWorld', 'tool:bloomWorld'], `${tag}: after the Stackings World`); checks++;
    await page.locator('[data-action="tool:bloomWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
    const probe = () => page.evaluate(() => window.__bloomProbe());
    const slide = async (u) => { await page.locator(`${P} .ch-param-row input`).fill(String(u)); await page.waitForTimeout(900); };
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    for (const k of BLOOM_KINDS) { const bx = await page.locator(`${P} [data-chains-kind="${k}"]`).boundingBox(); assert.ok(bx && bx.height >= 30, `${tag}: ${k} button`); }
    checks++;
    for (const k of ['icosaxes', 'lotus']) {
      if ((await probe()).kind !== k) { await page.tap(`${P} [data-chains-kind="${k}"]`); await page.waitForTimeout(1200); }
      for (const s of BLOOM_STOPS[k]) {
        await slide(Math.max(0, Math.min(1000, s.u + (s.u < 1000 ? 6 : -6)))); const st = await probe();
        assert.equal(st.param.u, s.u, `${tag}: ${k} snaps to ${s.key}`);
        assert.equal(total(st.drawn), 20, `${tag}: ${k} ${s.key}: twenty pieces`);
        assert.ok((await caption()).startsWith(t(`bloom.stop.${s.key}`, 'en')), `${tag}: ${k} ${s.key} caption`); checks++;
      }
    }
    await page.tap(`${P} [data-chains-kind="hexa"]`); await page.waitForTimeout(1500);
    let st = await probe(); assert.equal(st.kind, 'hexa'); assert.equal(total(st.drawn), 9, `${tag}: Icosaxes Hexa 9 pieces`); checks++;
    assert.equal(await page.locator(`${P} .ch-param-row input`).count() === 0 || !(await page.locator(`${P} .ch-param-row`).isVisible()), true, `${tag}: no slider on the Hexa button`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
for (const [dev, viewport] of Object.entries({ tv: { width: 1280, height: 720 }, ipad: { width: 820, height: 1050 }, phone: { width: 390, height: 760 } })) {
  for (const [kind, name] of [['icosaxes', 'bud'], ['hexa', 'hexa']]) {
    const page = await b.newPage({ viewport, hasTouch: dev !== 'tv', isMobile: dev !== 'tv' });
    const errors = await open(page, `&site=kaleidohedra&open=bloom:${kind}`);
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1800);
    const st = await page.evaluate(() => window.__bloomProbe()); assert.equal(st.kind, kind, `?open=bloom:${kind}`);
    if (kind === 'icosaxes') { await page.locator(`${P} .ch-param-row input`).fill(String(BLOOM_STOPS.icosaxes.find((s) => s.key === 'bud').u)); await page.waitForTimeout(1200); }
    await page.screenshot({ path: `${SH}/${dev}-${name}.png` });
    assert.deepEqual(errors, [], `${dev} ${kind}: console errors`); checks++;
    await page.close();
  }
}
await b.close();
console.log(`bloom OK: ${checks} checks`);
