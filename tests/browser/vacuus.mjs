// ◌ DICTO Vacuus through the real UI, on a phone (390 × 844, touch) and an iPad (1024 × 1366, touch) and a desktop:
//   - the link ?site=polyhedraverse&open=vacuus:CUBE opens Polyhedraverse on the cube with the lens on Pyramids;
//   - each of the five views is chosen by tapping its button, and each is measured on the screen (the scene alone, the panels hidden
//     for the shot): something is drawn, Exploded's slider at 100 reaches farther than at 0, Star reaches farther than Pyramids, and
//     Star shows the spikes' purple, Sheets and Struts their class colours;
//   - the link with a view (vacuus:D20:sheets);
//   - a one-piece build offers the lens button (tap: Pyramids; Close: back, the button again); a solid whose centre is outside a face
//     plane (DICTO Hexa) has no button, and its link opens no lens;
//   - Kaleidohedra's door: Aristotle's Pyramid's "DICTO Vacuus" link opens the same solid in the lens, and the lens's Pyramids view
//     links back to Aristotle's Pyramid on that solid.
// No console errors. Screenshots (SHOTS): vacuus-<device>-<view>.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const DEVICES = [
  ['phone', { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 3 }],
  ['ipad', { viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true }],
  ['desktop', { viewport: { width: 1280, height: 800 } }],
];
const VIEWS = ['pyramids', 'exploded', 'star', 'sheets', 'struts'];
const b = await chromium.launch();
const report = {};
for (const [name, opts] of DEVICES) {
  const page = await b.newPage(opts);
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = (sel) => (opts.hasTouch ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__vacuusProbe());
  const settle = async () => { await page.waitForTimeout(1200); };   // the camera's fit glides for a moment
  const open = async (query) => {
    await page.goto(`${BASE}/index.html?${query}&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(800); }
  };
  // The scene alone, measured: the bounding box of what differs from the background, and how many pixels fall in a few hue bands.
  async function measure(label) {
    await page.addStyleTag({ content: 'html.vac-measure *:not(canvas):not(:has(canvas)) { visibility: hidden !important; }' });
    await page.evaluate(() => document.documentElement.classList.add('vac-measure'));
    await page.waitForTimeout(250);
    const png = await page.screenshot();
    await page.evaluate(() => document.documentElement.classList.remove('vac-measure'));
    await page.screenshot({ path: `${SH}/vacuus-${name}-${label}.png` });
    return page.evaluate(async (b64) => {
      const img = new Image(); img.src = `data:image/png;base64,${b64}`; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      const { data, width, height } = g.getImageData(0, 0, c.width, c.height);
      const px = (x, y) => { const i = (y * width + x) * 4; return [data[i], data[i + 1], data[i + 2]]; };
      const bg = px(2, Math.floor(height / 2));
      let x0 = width, y0 = height, x1 = -1, y1 = -1, n = 0;
      const bands = { purple: 0, gold: 0, teal: 0 };
      for (let y = 0; y < height; y += 2) for (let x = 0; x < width; x += 2) {
        const [r, g2, bl] = px(x, y);
        if (Math.abs(r - bg[0]) + Math.abs(g2 - bg[1]) + Math.abs(bl - bg[2]) < 60) continue;
        n++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
        const mx = Math.max(r, g2, bl), mn = Math.min(r, g2, bl);
        if (mx - mn < 40) continue;
        const h = mx === r ? ((g2 - bl) / (mx - mn) + 6) % 6 : mx === g2 ? (bl - r) / (mx - mn) + 2 : (r - g2) / (mx - mn) + 4;
        const deg = h * 60;
        if (deg >= 255 && deg <= 290) bands.purple++;
        else if (deg >= 35 && deg <= 52) bands.gold++;
        else if (deg >= 178 && deg <= 198) bands.teal++;
      }
      return { w: x1 - x0, h: y1 - y0, pixels: n * 4, bands, size: [width, height] };
    }, png.toString('base64'));
  }

  // 1. The link on the cube: Pyramids.
  await open('site=polyhedraverse&open=vacuus:CUBE');
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, `${name}: no wizard over it`);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'Cube', `${name}: the shape's name in the header`);
  let st = await probe();
  assert.ok(st, `${name}: the lens is on`);
  assert.deepEqual([st.view, st.faces, st.edges, st.corners], ['pyramids', 6, 12, 8], `${name}: the cube`);
  for (const v of VIEWS) {
    const btn = page.locator(`[data-vac-view="${v}"]`);
    assert.equal(await btn.isVisible(), true, `${name}: ${v} button`);
    const box = await btn.boundingBox();
    assert.ok(box.height >= 44, `${name}: ${v} a full touch target (${box.width} × ${box.height})`);
  }
  assert.equal(await page.locator('.poly-shapes, [data-hints], [data-best], .poly-star-go').count(), 0, `${name}: only the lens row while it is on`);
  const m = {};
  for (const v of VIEWS) {
    await press(`[data-vac-view="${v}"]`); await settle();
    st = await probe();
    assert.equal(st.view, v, `${name}: tapped ${v}`);
    assert.equal(await page.locator(`[data-vac-view="${v}"]`).getAttribute('aria-pressed'), 'true', `${name}: ${v} shown as chosen`);
    const cap = await page.textContent('[data-vac-caption]');
    console.log(name, v, '-', cap);
    // only the controls that apply: the slider in Exploded, the Aristotle link in Pyramids, the colour key in Sheets and Struts
    assert.equal(await page.locator('[data-vac-apart]').count(), v === 'exploded' ? 1 : 0, `${name}: ${v} slider`);
    assert.equal(await page.locator('[data-vac-aristotle]').count(), v === 'pyramids' ? 1 : 0, `${name}: ${v} Aristotle link`);
    assert.equal(await page.locator('.vac-legend').count(), v === 'sheets' || v === 'struts' ? 1 : 0, `${name}: ${v} colour key`);
    if (v === 'exploded') {
      const slider = page.locator('[data-vac-apart]'), sb = await slider.boundingBox(), vp = page.viewportSize();
      console.log(name, 'slider box', sb, 'viewport', vp);
      assert.ok(sb.width >= Math.min(0.8 * vp.width, 600), `${name}: a long slider (${sb.width})`);
      assert.ok(sb.y + sb.height > vp.height - 160, `${name}: the slider low on the screen (${sb.y + sb.height} of ${vp.height})`);
      assert.ok(sb.height >= 40, `${name}: a thick slider (${sb.height})`);
      await slider.fill('0'); await page.waitForTimeout(300);
      m.exploded0 = await measure('exploded-0');
      await slider.fill('100'); await page.waitForTimeout(300);
      assert.equal((await probe()).apart, 100, `${name}: slider moved the pyramids`);
      m.exploded = await measure('exploded');
    } else m[v] = await measure(v);
    if (v === 'sheets') assert.match(await page.textContent('.vac-legend'), /0\.866 · 0\.866 · 1 ×12/, `${name}: one fin shape`);
    if (v === 'struts') assert.match(await page.textContent('.vac-legend'), /0\.866 ×8/, `${name}: one strut length`);
  }
  // the camera only ever widens (for Exploded and Star), so Pyramids again, in the same frame as the Star, to compare their reach
  await press('[data-vac-view="pyramids"]'); await settle();
  m.pyramidsAgain = await measure('pyramids-again');
  console.log(name, JSON.stringify(m));
  for (const [k, r] of Object.entries(m)) assert.ok(r.pixels > 2000 && r.w > 40 && r.h > 40, `${name}: ${k} draws something (${JSON.stringify(r)})`);
  assert.ok(m.exploded.w > 1.3 * m.exploded0.w, `${name}: Exploded at 100 reaches farther than at 0 (${m.exploded.w} vs ${m.exploded0.w})`);
  assert.ok(m.star.w > 1.05 * m.pyramidsAgain.w, `${name}: the Star reaches farther than the Pyramids (${m.star.w} vs ${m.pyramidsAgain.w})`);
  assert.ok(m.star.bands.purple > 20 * m.pyramids.bands.purple + 500, `${name}: the Star's purple spikes (${m.star.bands.purple})`);
  assert.ok(m.sheets.bands.gold > 500, `${name}: the fins in their class colour (${m.sheets.bands.gold})`);
  assert.ok(m.struts.bands.gold > 200, `${name}: the struts in their length colour (${m.struts.bands.gold})`);
  report[name] = m;
  // Close: back to the outline, no lens
  await press('[data-vac-off]'); await page.waitForTimeout(500);
  assert.equal(await probe(), null, `${name}: closed`);

  // 2. The link with a view.
  await open('site=polyhedraverse&open=vacuus:D20:sheets');
  st = await probe();
  assert.deepEqual([st.view, st.edges, st.finClasses], ['sheets', 30, [30]], `${name}: vacuus:D20:sheets`);

  // 3. A one-piece build offers the button; a tap opens Pyramids; Close brings the button back.
  const one = (shape) => page.evaluate((s) => localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, connections: [], view: { shape: s },
    nodes: [{ id: 'n1', shape: s, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] })), shape);
  const reload = async () => {
    await page.goto(`${BASE}/index.html?site=polyhedraverse&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    if (await page.locator('.dim-wizard-overlay.open').count()) { await press('.dim-wizard-close'); await page.waitForTimeout(500); }
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(400); }
  };
  await one('D8'); await reload();
  assert.equal(await page.locator('[data-vac]').isVisible(), true, `${name}: lens button for a one-piece octahedron`);
  await press('[data-vac]'); await page.waitForTimeout(500);
  st = await probe();
  assert.deepEqual([st.view, st.faces], ['pyramids', 8], `${name}: the octahedron's pyramids`);
  await press('[data-vac-off]'); await page.waitForTimeout(500);
  assert.equal(await probe(), null, `${name}: closed`);
  assert.equal(await page.locator('[data-vac]').isVisible(), true, `${name}: the button again`);
  // DICTO Hexa: its centre is outside some face planes: no button (hidden, not greyed), and its link opens no lens
  await one('DICTO_HEXA'); await reload();
  assert.equal(await page.locator('[data-vac]').count(), 0, `${name}: no lens button for DICTO Hexa`);
  await page.evaluate(() => localStorage.removeItem('polyhedraverse-poly-world'));
  await open('site=polyhedraverse&open=vacuus:DICTO_HEXA');
  assert.equal(await probe(), null, `${name}: no lens on DICTO Hexa`);

  // 4. Kaleidohedra's door: Aristotle's Pyramid → DICTO Vacuus → back.
  await open('site=kaleidohedra&open=aristotle:octahedron');
  assert.equal(await page.locator('#worldaristotle-panel').isVisible(), true, `${name}: Aristotle's Pyramid`);
  const link = page.locator('#worldaristotle-panel [data-ar="vacuus"]');
  assert.equal(await link.isVisible(), true, `${name}: the DICTO Vacuus link among the pyramids`);
  await press('#worldaristotle-panel [data-ar="vacuus"]');
  await page.waitForFunction(() => window.__vacuusProbe()?.view === 'pyramids', null, { timeout: 20000 });
  if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(800); }
  st = await probe();
  assert.deepEqual([st.view, st.faces], ['pyramids', 8], `${name}: the octahedron in the lens`);
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${SH}/vacuus-${name}-from-aristotle.png` });
  await press('[data-vac-aristotle]');
  await page.waitForFunction(() => window.__aristotleProbe?.()?.solid === 'octahedron' && document.querySelector('#worldaristotle-panel')?.classList.contains('visible'), null, { timeout: 20000 });
  const ar = await page.evaluate(() => window.__aristotleProbe());
  assert.deepEqual([ar.mode, ar.solid], ['pyramids', 'octahedron'], `${name}: back to Aristotle's Pyramid on the octahedron`);

  console.log(name, errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
  await page.close();
}
await b.close();
console.log('vacuus OK');
