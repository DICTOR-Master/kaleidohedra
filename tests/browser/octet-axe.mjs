// The AXE gap in the DICTO Icosahedral Octet (DICTO 2026-10-23), through the real UI on a phone (390×844) and an iPad (820×1180), touch,
// on all three doors: each of the three simple cubic networks (Lotus Jewel network, Icosahedra and Unborn, Icosahedra, dodecahedra and
// AXE) opens from the DICTO menu with the pieces of the network view by role (as world-octet.js builds them), the AXE button hides
// and shows the AXE (shown at first), Crystal on and off, and the build world's three versions draw their AXE; Mixed blocks (DICTO
// 2026-10-23): every pattern at block sizes 1 and 2, Swap off and on, its pieces by kind as mixedPieces makes them. No console errors.
// Screenshots to $SHOTS (default /tmp/axe-shots).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { OCTET_VIEWS, mixedPieces, MIXED_PATTERNS } from '../../src/app/world-octet.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/axe-shots';
mkdirSync(SH, { recursive: true });
const KINDS = ['lotusJewel', 'icoUnborn', 'axeNet'];
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
const want = Object.fromEntries(KINDS.map((k) => [k, count(OCTET_VIEWS[k].views.network(2))]));
const DEVICES = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const b = await chromium.launch();
let checks = 0;
// DOORS (comma list) runs some doors only, to keep each run short; all three by default.
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse,polyhedraverse').split(',')) {
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
    const tag = `${door}-${dev}`;
    for (const kind of KINDS) {
      await open(`tool:octetWorld:${kind}`);
      await page.waitForSelector('#worldoctet-panel.visible');
      let st = await page.evaluate(() => window.__octetProbe());
      // a fresh page: the network view at size 2
      assert.equal(st.kind, kind, tag); assert.equal(st.part, 'network', tag); assert.equal(st.size, 2, tag);
      assert.deepEqual(st.drawn, want[kind], `${tag} ${kind}: pieces by role`); checks++;
      const hide = page.locator('#worldoctet-panel [data-chains-hide]');
      assert.ok(await hide.isVisible(), `${tag} ${kind}: AXE button shown`);
      assert.match(await hide.textContent(), /AXE/);
      const box = await hide.boundingBox(); assert.ok(box.height >= 30, `${tag}: AXE button big enough to touch (${box.height})`);
      await page.screenshot({ path: `${SH}/${tag}-${kind}.png` });
      await hide.tap(); await page.waitForTimeout(500);
      st = await page.evaluate(() => window.__octetProbe());
      const { axe, ...rest } = want[kind];
      assert.equal(st.hidden, 'axe'); assert.deepEqual(st.drawn, rest, `${tag} ${kind}: AXE hidden`); checks++;
      await page.screenshot({ path: `${SH}/${tag}-${kind}-noaxe.png` });
      await hide.tap(); await page.waitForTimeout(500);
      st = await page.evaluate(() => window.__octetProbe());
      assert.equal(st.hidden, null); assert.deepEqual(st.drawn, want[kind], `${tag} ${kind}: AXE shown again`); checks++;
      await page.tap('#worldoctet-panel [data-chains-crystal]'); await page.waitForTimeout(500);
      assert.equal((await page.evaluate(() => window.__octetProbe())).crystal, true);
      await page.screenshot({ path: `${SH}/${tag}-${kind}-crystal.png` });
      // closed up (Pull apart 0): the network fills its ball, in Crystal and solid
      await page.locator('#worldoctet-panel .ch-apart-row input').fill('0'); await page.waitForTimeout(400);
      await page.screenshot({ path: `${SH}/${tag}-${kind}-closed-crystal.png` });
      await page.tap('#worldoctet-panel [data-chains-crystal]'); await page.waitForTimeout(300);
      await page.screenshot({ path: `${SH}/${tag}-${kind}-closed.png` });
      await page.locator('#worldoctet-panel .ch-apart-row input').fill('300'); await page.waitForTimeout(300);
      // the one-piece views have no AXE, so no AXE button
      await page.selectOption('#worldoctet-panel [data-select="part"]', Object.keys(OCTET_VIEWS[kind].views)[1]); await page.waitForTimeout(500);
      assert.ok(await hide.isHidden(), `${tag} ${kind}: no AXE button without AXE`); checks++;
      if (kind === 'axeNet') await page.screenshot({ path: `${SH}/${tag}-${kind}-ico.png` });
      await page.selectOption('#worldoctet-panel [data-select="part"]', 'network'); await page.waitForTimeout(300);
    }
    // Mixed blocks: pattern menu, block slider and Swap button, each choice drawn as mixedPieces builds it
    await open('tool:octetWorld:mixed');
    await page.waitForSelector('#worldoctet-panel.visible');
    for (const sel of ['.ch-pattern-row', '.ch-block-row', '[data-chains-swap]']) assert.ok(await page.locator(`#worldoctet-panel ${sel}`).isVisible(), `${tag}: mixed ${sel} shown`);
    for (const pattern of Object.keys(MIXED_PATTERNS)) {
      await page.selectOption('#worldoctet-panel [data-select="pattern"]', pattern);
      for (const block of [1, 2]) {
        await page.locator('#worldoctet-panel .ch-block-row input').fill(String(block));
        for (const swap of [false, true]) {
          let st = await page.evaluate(() => window.__octetProbe());
          if (st.opts.swap !== swap) { await page.tap('#worldoctet-panel [data-chains-swap]'); await page.waitForTimeout(300); st = await page.evaluate(() => window.__octetProbe()); }
          assert.deepEqual(st.opts, { pattern, block, swap }, `${tag} mixed options`);
          assert.deepEqual(st.drawn, count(mixedPieces(st.size, st.opts)), `${tag} mixed ${pattern} ${block} ${swap}: pieces by kind`); checks++;
          if (block === 2 || dev === 'phone') await page.screenshot({ path: `${SH}/${tag}-mixed-${pattern}-b${block}${swap ? '-swap' : ''}.png` });
          if (block === 2 && !swap && dev === 'ipad') {
            await page.tap('#worldoctet-panel [data-chains-crystal]'); await page.waitForTimeout(400);
            await page.screenshot({ path: `${SH}/${tag}-mixed-${pattern}-b2-crystal.png` });
            await page.tap('#worldoctet-panel [data-chains-crystal]'); await page.waitForTimeout(300);
          }
        }
      }
    }
    // the one-piece-kind view keeps the controls; the octet's other networks hide them
    await open('tool:octetWorld:lotusJewel');
    for (const sel of ['.ch-pattern-row', '.ch-block-row', '[data-chains-swap]']) assert.ok(await page.locator(`#worldoctet-panel ${sel}`).isHidden(), `${tag}: ${sel} hidden outside Mixed blocks`);
    checks++;
    // the build world: a cluster in each simple cubic version draws its AXE; the button hides them
    for (const kind of KINDS) {
      await open(`tool:octetBuildWorld:${kind}.clusters`);
      await page.waitForSelector('#worldoctetbuild-panel.visible');
      await page.tap('[data-octb="reset"]'); await page.waitForTimeout(500);
      let st = await page.evaluate(() => window.__octetBuildProbe());
      assert.equal(st.kind, kind); assert.equal(st.cells, 9);
      assert.equal(st.drawn.axe, 24, `${tag} build ${kind}: 24 AXE round one cluster (${JSON.stringify(st.drawn)})`); checks++;
      if (kind === 'axeNet') assert.equal(st.drawn.tricap, 8 + 8 * 7, 'the Jewel\'s 8 Tricaps and 7 more round each void');
      await page.tap('[data-octb="axe"]'); await page.waitForTimeout(400);
      st = await page.evaluate(() => window.__octetBuildProbe());
      assert.equal(st.drawn.axe, undefined, `${tag} build ${kind}: AXE hidden`);
      await page.tap('[data-octb="axe"]'); await page.waitForTimeout(400);
      if (dev === 'phone' && door === 'kaleidohedra') await page.screenshot({ path: `${SH}/${tag}-build-${kind}.png` });
    }
    await open('tool:octetBuildWorld:caps');
    assert.ok(await page.locator('[data-octb="axe"]').isHidden(), `${tag}: no AXE button in the octet with Admiral Caps`); checks++;
    console.log(tag, errors.length ? `ERRORS ${errors.join(' | ')}` : 'no errors');
    assert.deepEqual(errors, [], tag);
    await page.close();
  }
}
await b.close();
console.log(`octet-axe OK (${checks} checks)`);
