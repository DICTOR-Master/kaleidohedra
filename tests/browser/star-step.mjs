// ★ Star step (DICTO's Star Cores papers, #79) through the real UI, on a phone (390 × 844, touch) and a desktop: the papers' link
// ?site=polyhedraverse&open=starstep:TRUNCATED_ICOSAHEDRON opens Polyhedraverse on the truncated icosahedron; three taps of the button
// go Star → Halo (the layer: 60 corner pyramids + 90 edge tetrahedra) → Next (the halo, 32 corners and 60 faces, the new solid);
// Reset; a one-piece build offering the button (a tap starts the icosahedron's star); the link with a step (starstep:CUBE:2) and
// the Rule choice (Doubling on the cube: the star sticks out of its halo, no layer);
// no button for a non-convex solid. No console errors. Screenshots (SHOTS): star-step-phone.png, star-step-desktop.png (at the halo).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch();
for (const [name, opts] of [['phone', { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 3 }], ['desktop', { viewport: { width: 1280, height: 800 } }]]) {
  const page = await b.newPage(opts);
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = (sel) => (opts.hasTouch ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__starStepProbe());
  const open = async (what) => {
    await page.goto(`${BASE}/index.html?site=polyhedraverse&open=${what}&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    // over a saved build the app asks first (fresh-start.mjs): go on with it; the star step starts once that is answered
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(800); }
  };
  await open('starstep:TRUNCATED_ICOSAHEDRON');
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, `${name}: no wizard over it`);
  let st = await probe();
  assert.ok(st, `${name}: the star step is on`);
  assert.deepEqual([st.n, st.phase, st.corners, st.faces], [0, 'solid', 60, 32], `${name}: the truncated icosahedron`);
  const go = page.locator('.poly-star-go');
  assert.equal(await go.isVisible(), true, `${name}: ★ Star step shown`);
  const box = await go.boundingBox();
  assert.ok(box.height >= 44 && box.width >= 44, `${name}: a full touch target (${box.width} × ${box.height})`);
  assert.equal(await page.locator('.poly-star-caption').isVisible(), true, `${name}: caption`);
  const expect = [['star', 60, 32], ['halo', 60, 32], ['next', 32, 60]];
  for (const [i, [phase, v, f]] of expect.entries()) {
    await press('.poly-star-go');
    // ~0.6 s of animation; headless Chromium on dicto-node can starve frames, so wait for it to settle rather than a fixed time
    await page.waitForFunction(() => window.__starStepProbe()?.animating === false, null, { timeout: 15000 }); await page.waitForTimeout(300);
    st = await probe();
    assert.deepEqual([st.n, st.phase, st.corners, st.faces, st.animating], [i + 1, phase, v, f, false], `${name}: tap ${i + 1}`);
    const cap = await page.textContent('.poly-star-caption');
    console.log(name, `tap ${i + 1}:`, cap);
    assert.match(cap, new RegExp(`Step ${i + 1}`));
    assert.match(cap, new RegExp(`${v} corners, ${f} faces`));
    if (phase === 'halo') {
      assert.equal(st.layer, true, `${name}: the polar layer`);
      assert.match(cap, /layer: 60 corner pyramids \+ 90 edge tetrahedra/);
      assert.equal(await page.locator('[data-star-layer]').isVisible(), true, `${name}: Layer toggle at the halo`);
      await page.screenshot({ path: `${SH}/star-step-${name}.png` });
    }
  }
  await page.screenshot({ path: `${SH}/star-step-${name}-next.png` });
  assert.equal(await page.locator('.poly-shapes, [data-hints], [data-best]').count(), 0, `${name}: only the star row while it runs`);
  // Reset: back to the solid (here the empty build's outline, which has no button: the outline is not yet a piece)
  await press('[data-star-reset]'); await page.waitForTimeout(500);
  assert.equal(await probe(), null, `${name}: reset`);
  assert.equal(await go.isVisible(), false, `${name}: no button over an empty build`);
  // a build of one convex piece offers the button; a tap starts the star step on it
  await page.evaluate(() => localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, connections: [], view: { shape: 'D20' },
    nodes: [{ id: 'n1', shape: 'D20', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] })));
  await page.goto(`${BASE}/index.html?site=polyhedraverse&probe`); await page.waitForTimeout(1500);
  if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  if (await page.locator('.dim-wizard-overlay.open').count()) { await press('.dim-wizard-close'); await page.waitForTimeout(500); }
  // a saved build: closing the menu over it asks first (fresh-start.mjs); go on with it
  if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(400); }
  assert.equal(await go.isVisible(), true, `${name}: button for the one-piece build`);
  await press('.poly-star-go');
  await page.waitForFunction(() => window.__starStepProbe()?.animating === false, null, { timeout: 15000 });
  st = await probe();
  assert.deepEqual([st.n, st.phase, st.corners, st.faces], [1, 'star', 12, 20], `${name}: the icosahedron's star`);
  await press('[data-star-reset]'); await page.waitForTimeout(500);
  assert.equal(await go.isVisible(), true, `${name}: button after reset`);
  // the link with a step, and the Rule: the cube's doubling star sticks out of its halo
  await open('starstep:CUBE:2');
  st = await probe();
  assert.deepEqual([st.n, st.phase, st.corners, st.faces, st.layer], [2, 'halo', 8, 6, true], `${name}: starstep:CUBE:2`);
  assert.match(await page.textContent('.poly-star-caption'), /layer: 8 corner pyramids \+ 12 edge tetrahedra/);
  await page.selectOption('[data-star-rule]', 'doubling'); await page.waitForTimeout(400);
  st = await probe();
  assert.deepEqual([st.rule, st.contains, st.layer], ['doubling', false, false], `${name}: doubling cube`);
  assert.match(await page.textContent('.poly-star-caption'), /sticks out of its halo/);
  assert.equal(await page.locator('[data-star-layer]').count(), 0, `${name}: no Layer toggle without a layer`);
  await page.screenshot({ path: `${SH}/star-step-${name}-doubling.png` });
  // a non-convex solid (on an empty build): no button
  await page.evaluate(() => localStorage.removeItem('polyhedraverse-poly-world'));
  await open('starstep:STELLA_OCTANGULA');
  assert.equal(await probe(), null, `${name}: not for a non-convex solid`);
  assert.equal(await page.locator('.poly-star-go').isVisible(), false, `${name}: button hidden`);
  console.log(name, errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
  await page.close();
}
await b.close(); console.log('star-step OK');
