// The octet world's Golden split (DICTO 2026-10-23), through the real UI, touch, on a phone (390×844) and an iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors (DOORS): it opens from the DICTO menu; the view menu is hidden and the pattern buttons show, big
// enough to touch; Smooth, All keyed, Checker, Pyrochlore and Random each draw the pieces goldenPieces builds (by role); the Block
// size slider shows only for Checker and Pyrochlore, Swap only where something is keyed, and Swap turns the keys; a tap on the model
// steps one hexagon's key (the drawing changes, a second pattern tap lets it go); X-ray shows the cores and the AXE pyramids and turns
// back to whole pieces; a link opens Icosaxes in Polyhedraverse. No console errors. Screenshots to $SHOTS (default /tmp/gs-shots):
// <door>-<device>-smooth|allKeyed|pyrochlore|xray|tapped.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { goldenPieces, GS_PATTERNS } from '../../src/app/world-octet.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/gs-shots';
mkdirSync(SH, { recursive: true });
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
const want = (o) => count(goldenPieces(2, { pattern: 'smooth', block: 1, swap: false, flips: {}, ...o }));
const DEVICES = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const b = await chromium.launch();
let checks = 0;
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries(DEVICES)) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true });
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(`${BASE}/index.html?site=${door}&probe`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
    async function open(action) {
      if (!(await page.locator('.dim-wizard-overlay.open').count())) { await page.tap('#hud-wizard-cue'); await page.waitForSelector('.dim-wizard-overlay.open'); }
      await page.waitForTimeout(400);
      if (!(await page.locator(`[data-action="${action}"]`).count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
      await page.waitForTimeout(500);
      const btn = page.locator(`[data-action="${action}"]`).first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
      await page.waitForTimeout(400);
      if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
      await page.waitForTimeout(2000);
    }
    const tag = `${door}-${dev}`, P = '#worldoctet-panel';
    const probe = () => page.evaluate(() => window.__octetProbe());
    const shot = (name) => page.screenshot({ path: `${SH}/${tag}-${name}.png` });
    await open('tool:octetWorld:goldenSplit');
    await page.waitForSelector(`${P}.visible`);
    let st = await probe();
    assert.equal(st.kind, 'goldenSplit', tag); assert.equal(st.opts.pattern, 'smooth', tag); assert.equal(st.xray, false);
    assert.deepEqual(st.drawn, want({}), `${tag}: smooth pieces`); checks++;
    assert.ok(await page.locator(`${P} [data-select="part"]`).isHidden(), `${tag}: view menu hidden`);
    assert.ok(await page.locator(`${P} .ch-pattern-row`).isHidden(), `${tag}: pattern menu replaced by buttons`);
    for (const p of GS_PATTERNS) {
      const btn = page.locator(`${P} [data-chains-pattern="${p}"]`);
      assert.ok(await btn.isVisible(), `${tag}: ${p} button`);
      const box = await btn.boundingBox(); assert.ok(box.height >= 30, `${tag}: ${p} button big enough to touch (${box.height})`);
    }
    assert.ok(await page.locator(`${P} .ch-block-row`).isHidden(), `${tag}: no block size for Smooth`);
    assert.ok(await page.locator(`${P} [data-chains-swap]`).isHidden(), `${tag}: no Swap for Smooth`);
    assert.equal(await page.locator(`${P} [data-chains-link]`).count(), 4, `${tag}: four Polyhedraverse links`);
    checks++;
    await shot('smooth');
    for (const pattern of GS_PATTERNS.slice(1)) {
      await page.tap(`${P} [data-chains-pattern="${pattern}"]`); await page.waitForTimeout(600);
      st = await probe();
      assert.equal(st.opts.pattern, pattern);
      assert.deepEqual(st.drawn, want({ pattern }), `${tag}: ${pattern} pieces`);
      const blocky = pattern === 'checker' || pattern === 'pyrochlore';
      assert.equal(await page.locator(`${P} .ch-block-row`).isVisible(), blocky, `${tag}: block size only for checker and pyrochlore`);
      assert.ok(await page.locator(`${P} [data-chains-swap]`).isVisible(), `${tag}: Swap shown for ${pattern}`);
      if (pattern === 'allKeyed') await shot('allKeyed');
      if (pattern === 'pyrochlore') {
        await page.locator(`${P} .ch-block-row input`).fill('2'); await page.waitForTimeout(500);
        assert.deepEqual((await probe()).drawn, want({ pattern, block: 2 }), `${tag}: pyrochlore block 2`);
        await shot('pyrochlore');
        await page.locator(`${P} .ch-block-row input`).fill('1'); await page.waitForTimeout(400);
      }
      checks++;
    }
    // Swap: the keys the other way (dents on the small pieces)
    await page.tap(`${P} [data-chains-pattern="allKeyed"]`); await page.waitForTimeout(400);
    await page.tap(`${P} [data-chains-swap]`); await page.waitForTimeout(600);
    st = await probe(); assert.equal(st.opts.swap, true); assert.deepEqual(st.drawn, want({ pattern: 'allKeyed', swap: true }), `${tag}: swapped`); checks++;
    await page.tap(`${P} [data-chains-swap]`); await page.waitForTimeout(400);
    await page.tap(`${P} [data-chains-pattern="smooth"]`); await page.waitForTimeout(600);
    // a tap on the model steps one hexagon: try points round the model's middle until one lands on a hexagon
    const f = await page.evaluate(() => window.__frameProbe());
    let flipped = false;
    for (const [dx, dy] of [[0, 0], [0.15, 0.1], [-0.2, 0.05], [0.1, -0.2], [-0.1, -0.15], [0.25, -0.05], [-0.25, 0.2], [0.05, 0.3]]) {
      await page.touchscreen.tap(f.cx + dx * f.r, f.cy + dy * f.r); await page.waitForTimeout(600);
      if ((await probe()).flips === 1) { flipped = true; break; }
    }
    assert.ok(flipped, `${tag}: a tap on a hexagon flips its key`); checks++;
    await shot('tapped');
    await page.tap(`${P} [data-chains-pattern="smooth"]`); await page.waitForTimeout(500);
    assert.equal((await probe()).flips, 0, `${tag}: a pattern tap lets the tapped key go`); checks++;
    // X-ray: the cores, AXE pyramids (cyan) and keys
    await page.tap(`${P} [data-chains-pattern="pyrochlore"]`); await page.waitForTimeout(500);
    await page.tap('#xray-toggle'); await page.waitForTimeout(900);
    st = await probe();
    assert.equal(st.xray, true, `${tag}: X-ray on`);
    assert.deepEqual(st.drawn, want({ pattern: 'pyrochlore', xray: true }), `${tag}: X-ray parts`);
    assert.ok(st.drawn.axe > 0 && st.drawn.mxIco > 0 && st.drawn.mxUnborn > 0, `${tag}: cores and AXE pyramids`); checks++;
    await shot('xray');
    await page.tap('#xray-toggle'); await page.waitForTimeout(700);
    st = await probe(); assert.equal(st.xray, false); assert.deepEqual(st.drawn, want({ pattern: 'pyrochlore' }), `${tag}: whole again`); checks++;
    await page.tap(`${P} [data-chains-pattern="smooth"]`); await page.waitForTimeout(300);
    // the link opens the piece where it lives
    await page.tap(`${P} [data-chains-link="tool:polyShape:DICTO_ICOSAXES"]`); await page.waitForTimeout(2500);
    if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="keep"]'); await page.waitForTimeout(1500); }
    await shot('poly-icosaxes');
    assert.ok(await page.locator('body').getByText('Icosaxes', { exact: true }).first().isVisible(), `${tag}: Icosaxes opened in Polyhedraverse`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag);
    await page.close();
  }
}
await b.close();
console.log(`golden-split OK: ${checks} checks`);
