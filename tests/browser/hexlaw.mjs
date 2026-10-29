// The Hexagonality Law panel (DICTO 2026-10-29, decisions 1A–5A) in the Stackings world, through the real UI, touch, phone (390×844)
// and iPad (820×1180), on both doors (DOORS): ?open=stackings:4H&law=68 (the site cards' "View in app") opens the world with #68's
// chart showing; seven paper buttons; the gold ring at the world's own h (4H: 1/2); tapping SiC's 6H dot builds 6H; flipping a layer
// moves the ring; #70 (against pressure) has no ring; ✕ closes, the Law button opens again; the card stays inside the
// screen. No console errors. Screenshots ($SHOTS, default /tmp/law-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/law-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldstackings-panel', C = '.hexlaw-card';
const b = await chromium.launch();
let checks = 0;
const ringX = (page) => page.locator(`${C} .law-own`).first().getAttribute('cx');
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(`${BASE}/index.html?site=${door}&open=stackings:4H&law=68`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
    await page.waitForSelector(`${P}.visible`, { timeout: 25000 }); await page.waitForTimeout(1500);
    assert.ok(await page.locator(C).isVisible(), `${tag}: card open from the link`);
    assert.equal(await page.locator(`${C} [data-law-paper]`).count(), 7);
    assert.equal(await page.locator(`${C} [data-law-paper="68"]`).getAttribute('class'), 'active'); checks++;
    assert.match(await page.locator(`${C} .law-note`).textContent(), /h = 1\/2/, `${tag}: 4H own h`);
    assert.equal(await page.locator(`${C} .law-own`).count(), 3, `${tag}: a ring on each of the three lines`); checks++;
    await page.screenshot({ path: `${SH}/${tag}-68.png` });
    const x4 = await ringX(page);
    await page.locator(`${C} [data-law-dot="1.0.1"]`).tap(); await page.waitForTimeout(900);
    assert.equal(await page.locator(`${P} [data-chains-kind="6H"]`).getAttribute('class'), 'active', `${tag}: 6H built`);
    assert.match(await page.locator(`${C} .law-note`).textContent(), /SiC · 6H/); checks++;
    const x6 = await ringX(page); assert.ok(Number(x6) < Number(x4), `${tag}: ring moved to 1/3`); checks++;
    await page.locator(`${P} [data-stk-layer="0"]`).tap(); await page.waitForTimeout(900);
    assert.notEqual(await ringX(page), x6, `${tag}: flipping a layer moves the ring`); checks++;
    await page.locator(`${C} [data-law-paper="70"]`).tap(); await page.waitForTimeout(300);
    assert.equal(await page.locator(`${C} .law-own`).count(), 0, `${tag}: no ring against pressure`); checks++;
    for (const p of [66, 71, 72, 73, 74]) { await page.locator(`${C} [data-law-paper="${p}"]`).tap(); await page.waitForTimeout(200); await page.screenshot({ path: `${SH}/${tag}-${p}.png` }); }
    await page.locator(`${C} [data-law-close]`).tap(); await page.waitForTimeout(200);
    assert.ok(!(await page.locator(C).isVisible()), `${tag}: closed`);
    await page.locator(`${P} [data-stk-law]`).tap(); await page.waitForTimeout(300);
    assert.ok(await page.locator(C).isVisible(), `${tag}: Law button opens`); checks++;
    const box = await page.locator(C).boundingBox();
    assert.ok(box.x >= 0 && box.x + box.width <= viewport.width + 0.5, `${tag}: inside the screen`); checks++;
    assert.deepEqual(errors, [], `${tag}: console`); await page.close();
  }
}
await b.close(); console.log(`hexlaw: ${checks} checks ok`);
