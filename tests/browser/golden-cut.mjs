// ✂ Golden Cut (paper #88) through the real UI, on a phone (390 × 844, touch), an iPad (1024 × 1366, touch) and a desktop:
//   - ?open=goldencut:OCTAHEDRON:greater opens Polyhedraverse on the octahedron at DICTO's Icosaxes; goldencut:DODECAHEDRON (no stop)
//     at the Greater Golden Cut;
//   - the three stops are full touch targets, the slider long, low and thick with the stops marked on its track; the solid picker lists
//     the five in D·I·C·T·O order;
//   - on each of the five (chosen in the picker), each stop is tapped: the cut lands exactly on its value (all fifteen, the ten golden
//     ones from the paper), the name and long/short ratio read right, and the render is measured (the scene alone): gold corners
//     growing Lesser → Archimedean → Greater, the faces in the solid's own green;
//   - the slider: between stops no name; near a stop it lands on it;
//   - a one-piece Platonic build offers ✂ Golden Cut (tap: on; Close: back, the button again); any other solid has no button (hidden,
//     not greyed) and its link opens nothing;
//   - the same-size comparison with DICTO Vacuus on the cube (both framed on the solid).
// No console errors. Screenshots (SHOTS): gcut-<device>-<solid>-<stop>.png and gcut-<device>-vacuus-cube.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const DEVICES = [
  ['phone', { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 3 }],
  ['ipad', { viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true }],
  ['desktop', { viewport: { width: 1280, height: 800 } }],
];
const PHI = (1 + Math.sqrt(5)) / 2, S2 = Math.SQRT2, S5 = Math.sqrt(5), S10 = Math.sqrt(10);
// The five in D·I·C·T·O order; each stop's exact x (paper #88), its name and the Archimedean solid's name.
const SOLIDS = [
  ['dodecahedron', 'Dodecahedron', { lesser: (7 - S5) / 22, archimedean: 1 / (PHI + 2), greater: 1 / 3 }, 'Truncated dodecahedron'],
  ['icosahedron', 'Icosahedron', { lesser: 0.5 - S5 / 10, archimedean: 1 / 3, greater: (3 - S5) / 2 }, 'Truncated icosahedron'],
  ['cube', 'Cube', { lesser: (-2 * S5 - 2 + S10 + 3 * S2) / 4, archimedean: 1 / (2 + S2), greater: (-3 * S2 - 2 + S10 + 2 * S5) / 4 }, 'Truncated cube'],
  ['tetrahedron', 'Tetrahedron', { lesser: 0.5 - S5 / 10, archimedean: 1 / 3, greater: (3 - S5) / 2 }, 'Truncated tetrahedron'],
  ['octahedron', 'Octahedron', { lesser: 0.5 - S5 / 10, archimedean: 1 / 3, greater: (3 - S5) / 2 }, 'Truncated octahedron'],
];
const STOPS = ['lesser', 'archimedean', 'greater'];
const nameOf = (key, Name, stop, arch) => (stop === 'archimedean' ? arch : key === 'octahedron' ? { greater: 'Icosaxes', lesser: 'Unborn Axes' }[stop]
  : `${stop === 'greater' ? 'Greater' : 'Lesser'} Golden Cut ${Name}`);

const b = await chromium.launch();
const report = {};
for (const [name, opts] of DEVICES) {
  const page = await b.newPage(opts);
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = (sel) => (opts.hasTouch ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__goldenCutProbe());
  const settle = () => page.waitForTimeout(1200);   // the camera's fit glides for a moment
  const open = async (query) => {
    await page.goto(`${BASE}/index.html?${query}&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(800); }
  };
  // The scene alone, measured (as vacuus.mjs): the bounding box of what differs from the background, and pixels in hue bands.
  async function measure(label) {
    await page.addStyleTag({ content: 'html.gc-measure *:not(canvas):not(:has(canvas)) { visibility: hidden !important; }' });
    await page.evaluate(() => document.documentElement.classList.add('gc-measure'));
    await page.waitForTimeout(250);
    const png = await page.screenshot();
    await page.evaluate(() => document.documentElement.classList.remove('gc-measure'));
    await page.screenshot({ path: `${SH}/gcut-${name}-${label}.png` });
    return page.evaluate(async (b64) => {
      const img = new Image(); img.src = `data:image/png;base64,${b64}`; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      const { data, width, height } = g.getImageData(0, 0, c.width, c.height);
      const px = (x, y) => { const i = (y * width + x) * 4; return [data[i], data[i + 1], data[i + 2]]; };
      const bg = px(2, Math.floor(height / 2));
      let x0 = width, y0 = height, x1 = -1, y1 = -1, n = 0;
      const bands = { gold: 0, green: 0, dark: 0 };
      for (let y = 0; y < height; y += 2) for (let x = 0; x < width; x += 2) {
        const [r, g2, bl] = px(x, y);
        if (Math.abs(r - bg[0]) + Math.abs(g2 - bg[1]) + Math.abs(bl - bg[2]) < 60) continue;
        n++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
        const mx = Math.max(r, g2, bl), mn = Math.min(r, g2, bl);
        if (mx < 40) { bands.dark++; continue; }
        if (mx - mn < 40) continue;
        const h = mx === r ? ((g2 - bl) / (mx - mn) + 6) % 6 : mx === g2 ? (bl - r) / (mx - mn) + 2 : (r - g2) / (mx - mn) + 4;
        const deg = h * 60;
        if (deg >= 33 && deg <= 55) bands.gold++;
        else if (deg >= 80 && deg <= 135) bands.green++;
      }
      return { w: x1 - x0, h: y1 - y0, pixels: n * 4, bands, size: [width, height] };
    }, png.toString('base64'));
  }
  const nameText = async () => (await page.textContent('[data-gcut-name]')).trim();

  // 1. The octahedron at Icosaxes, by its link.
  await open('site=polyhedraverse&open=goldencut:OCTAHEDRON:greater');
  assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, `${name}: no wizard over it`);
  let st = await probe();
  assert.ok(st, `${name}: Golden Cut on`);
  assert.deepEqual([st.key, st.stop, st.corners, st.faces], ['octahedron', 'greater', 6, 8], `${name}: goldencut:OCTAHEDRON:greater`);
  assert.ok(Math.abs(st.x - (3 - S5) / 2) < 1e-15, `${name}: x = 1/φ² (${st.x})`);
  assert.equal(await nameText(), 'Icosaxes', `${name}: DICTO's name`);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'Octahedron', `${name}: the solid in the header`);
  assert.match(await page.textContent('[data-gcut-caption]'), /1\.6180 = φ/, `${name}: long/short φ`);
  await settle();
  const icosaxes = await measure('octahedron-icosaxes');

  // 2. The dodecahedron with no stop given: the Greater Golden Cut; the controls.
  await open('site=polyhedraverse&open=goldencut:DODECAHEDRON');
  st = await probe();
  assert.deepEqual([st.key, st.stop], ['dodecahedron', 'greater'], `${name}: goldencut:DODECAHEDRON at the Greater Golden Cut`);
  assert.ok(Math.abs(st.x - 1 / 3) < 1e-15, `${name}: x = 1/3 (${st.x})`);
  assert.equal(await nameText(), 'Greater Golden Cut Dodecahedron', `${name}: its name`);
  assert.equal(await page.locator('.poly-shapes, [data-hints], [data-best], .poly-star-go, [data-vac]').count(), 0, `${name}: only the Golden Cut's rows while it is on`);
  assert.ok(!/[◀▶◂▸]/.test(await page.textContent('.poly-strip')), `${name}: no step arrows`);
  assert.deepEqual(await page.$$eval('[data-gcut-solid] option', (o) => o.map((x) => x.value)), SOLIDS.map((s) => s[0]), `${name}: the five in D·I·C·T·O order`);
  for (const s of STOPS) {
    const box = await page.locator(`[data-gcut-stop="${s}"]`).boundingBox();
    assert.ok(box.height >= 44 && box.width >= 44, `${name}: ${s} stop a full touch target (${box.width} × ${box.height})`);
  }
  const slider = page.locator('[data-gcut-x]'), sb = await slider.boundingBox(), vp = page.viewportSize();
  console.log(name, 'slider box', sb, 'viewport', vp);
  assert.ok(sb.width >= Math.min(0.8 * vp.width, 600), `${name}: a long slider (${sb.width})`);
  assert.ok(sb.y + sb.height > vp.height - 160, `${name}: the slider low on the screen (${sb.y + sb.height} of ${vp.height})`);
  assert.ok(sb.height >= 40, `${name}: a thick slider (${sb.height})`);
  // the stops marked on the track, in order, at their place along it
  const ticks = await page.$$eval('.gcut-tick', (ts) => ts.map((t) => { const r = t.getBoundingClientRect(); return r.x + r.width / 2; }));
  assert.equal(ticks.length, 3, `${name}: three marks`);
  STOPS.forEach((s, i) => {
    const want = sb.x + 20 + ((SOLIDS[0][2][s] - 0.01) / 0.48) * (sb.width - 40);
    assert.ok(Math.abs(ticks[i] - want) < 3, `${name}: ${s} mark at ${ticks[i].toFixed(1)} (want ${want.toFixed(1)})`);
  });

  // 3. Each of the five, each stop: exact, named, measured.
  const m = {};
  for (const [key, Name, X, arch] of SOLIDS) {
    if ((await probe()).key !== key) { await page.selectOption('[data-gcut-solid]', key); await page.waitForTimeout(300); }
    assert.equal((await probe()).key, key, `${name}: picked ${key}`);
    assert.equal((await page.textContent('#hud-world-title')).trim(), Name, `${name}: ${key} in the header`);
    m[key] = {};
    for (const s of STOPS) {
      await press(`[data-gcut-stop="${s}"]`);
      st = await probe();
      assert.equal(st.stop, s, `${name}: ${key} tapped ${s}`);
      assert.ok(Math.abs(st.x - X[s]) < 1e-12, `${name}: ${key} ${s} x = ${st.x} (exact ${X[s]})`);
      assert.ok(Math.abs(st.ratio - (s === 'archimedean' ? 1 : PHI)) < 1e-9, `${name}: ${key} ${s} ratio ${st.ratio}`);
      assert.equal(await page.locator(`[data-gcut-stop="${s}"]`).getAttribute('aria-pressed'), 'true', `${name}: ${s} shown as chosen`);
      assert.equal(await nameText(), nameOf(key, Name, s, arch), `${name}: ${key} ${s} name`);
      assert.ok(Math.abs(Number(await slider.inputValue()) - X[s]) < 1e-9, `${name}: the thumb on the stop`);
      if (key === 'cube' || key === 'dodecahedron' || s === 'greater') { await settle(); m[key][s] = await measure(`${key}-${s}`); }
    }
  }
  console.log(name, JSON.stringify(m));
  for (const [key, r] of Object.entries(m)) for (const [s, v] of Object.entries(r)) {
    assert.ok(v.pixels > 2000 && v.w > 60 && v.h > 60, `${name}: ${key} ${s} drawn (${JSON.stringify(v)})`);
    assert.ok(v.bands.gold > 300, `${name}: ${key} ${s} gold corners (${v.bands.gold})`);
    assert.ok(v.bands.green > 300, `${name}: ${key} ${s} green faces (${v.bands.green})`);
  }
  for (const key of ['cube', 'dodecahedron']) {
    const g = (s) => m[key][s].bands.gold;
    assert.ok(g('lesser') < g('archimedean') && g('archimedean') < g('greater'), `${name}: ${key} gold grows lesser → greater (${g('lesser')}, ${g('archimedean')}, ${g('greater')})`);
  }

  // 4. The slider: between stops no name; near a stop it lands on it (the dodecahedron again).
  await page.selectOption('[data-gcut-solid]', 'dodecahedron'); await page.waitForTimeout(300);
  await slider.fill('0.12'); await page.waitForTimeout(200);
  st = await probe();
  assert.ok(Math.abs(st.x - 0.12) < 1e-9 && st.stop === null, `${name}: x 0.12, no stop (${st.x}, ${st.stop})`);
  assert.equal(await nameText(), 'Dodecahedron, cut the same at every corner', `${name}: no stop name between stops`);
  assert.equal(await page.locator('[data-gcut-stop][aria-pressed="true"]').count(), 0, `${name}: no stop chosen`);
  await slider.fill('0.335'); await page.waitForTimeout(200);
  st = await probe();
  assert.ok(st.stop === 'greater' && Math.abs(st.x - 1 / 3) < 1e-15, `${name}: 0.335 lands on the Greater Golden Cut (${st.x})`);
  if (!opts.hasTouch) {   // a real drag on the desktop to the far left, then back to a stop by its button
    const y = sb.y + sb.height / 2;
    await page.mouse.move(sb.x + 20 + ((1 / 3 - 0.01) / 0.48) * (sb.width - 40), y); await page.mouse.down();
    await page.mouse.move(sb.x + 25, y, { steps: 20 }); await page.mouse.up(); await page.waitForTimeout(200);
    st = await probe();
    assert.ok(st.x < 0.05 && st.stop === null, `${name}: dragged to ${st.x}`);
  }
  m.free = await measure('dodecahedron-free');
  assert.ok(m.free.pixels > 2000, `${name}: drawn between stops`);
  await press('[data-gcut-off]'); await page.waitForTimeout(500);
  assert.equal(await probe(), null, `${name}: closed`);

  // 5. The button on a one-piece build: Platonic yes, anything else no.
  const one = (shape) => page.evaluate((s) => localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, connections: [], view: { shape: s },
    nodes: [{ id: 'n1', shape: s, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] })), shape);
  const reload = async () => {
    await page.goto(`${BASE}/index.html?site=polyhedraverse&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    if (await page.locator('.dim-wizard-overlay.open').count()) { await press('.dim-wizard-close'); await page.waitForTimeout(500); }
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(400); }
  };
  await one('D4'); await reload();
  const go = page.locator('[data-gcut]');
  assert.equal(await go.isVisible(), true, `${name}: ✂ Golden Cut for a one-piece tetrahedron`);
  assert.equal((await go.textContent()).trim(), '✂ Golden Cut', `${name}: its label`);
  const gb = await go.boundingBox();
  assert.ok(gb.height >= 44, `${name}: a full touch target (${gb.height})`);
  await page.screenshot({ path: `${SH}/gcut-${name}-button.png` });
  await press('[data-gcut]'); await page.waitForTimeout(500);
  st = await probe();
  assert.deepEqual([st.key, st.stop], ['tetrahedron', 'greater'], `${name}: the tetrahedron's Greater Golden Cut`);
  await press('[data-gcut-off]'); await page.waitForTimeout(500);
  assert.equal(await probe(), null, `${name}: closed`);
  assert.equal(await page.locator('[data-gcut]').isVisible(), true, `${name}: the button again`);
  for (const other of ['TRUNCATED_CUBE', 'CUBOCTAHEDRON']) {
    await one(other); await reload();
    assert.equal(await page.locator('[data-vac]').isVisible(), true, `${name}: ${other}'s strip is up (DICTO Vacuus offered)`);
    assert.equal(await page.locator('[data-gcut]').count(), 0, `${name}: no Golden Cut button for ${other}`);
  }
  await page.evaluate(() => localStorage.removeItem('polyhedraverse-poly-world'));
  await open('site=polyhedraverse&open=goldencut:CUBOCTAHEDRON');
  assert.equal(await probe(), null, `${name}: no Golden Cut on the cuboctahedron`);

  // 6. Same size as DICTO Vacuus: the cube in both, one after the other.
  await open('site=polyhedraverse&open=vacuus:CUBE'); await settle();
  const vac = await measure('vacuus-cube');
  await open('site=polyhedraverse&open=goldencut:CUBE:archimedean'); await settle();
  const gc = await measure('cube-archimedean-compare');
  const size = (r) => Math.max(r.w, r.h);
  console.log(name, 'same size: vacuus', size(vac), 'golden cut', size(gc), 'icosaxes', size(icosaxes));
  assert.ok(size(gc) > 0.75 * size(vac) && size(gc) < 1.25 * size(vac), `${name}: framed as DICTO Vacuus (${size(gc)} vs ${size(vac)})`);
  report[name] = { vac: size(vac), gc: size(gc) };

  console.log(name, errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
  await page.close();
}
await b.close();
console.log('golden cut OK', JSON.stringify(report));
