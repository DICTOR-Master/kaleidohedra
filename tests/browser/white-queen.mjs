// The White Queen 600-cell (DICTO 2026-10-27, paper #63), through the real UI, touch, phone (390×844) and iPad (820×1180), on the
// Kaleidohedra and Rhombiverse doors (DOORS): right after the Icosaxes Bloom in DICTO's list; two rows of four direction buttons (From,
// To; big enough to touch, the To matching From hidden), default vertex-first → cell-first; each From button jumps to its start and each
// To button to its end with the hull counts of #62/#63, all six turnings; the slider long, low and snapping at both ends; an in-between
// position captioned "From → To"; ?open=whitequeen:<vertex|edge|face|cell>. No console errors. Screenshots ($SHOTS, default
// /tmp/wq-shots) on a phone (390×844) and a desktop (1280×800) at the four main directions and halfway from vertex-first to cell-first.
// The Slice view (W3, W4): Shadow | Slice toggle, the shadow's rows hidden there; for every direction the slider stops at exactly the
// atlas's stops (tests/unit/white-queen-atlas.json), each with the atlas's vertices and face sizes; Humpty Dumpty and Shadow-17 in gold;
// Humpty Dumpty turns until the picture is touched. Every one of the 7 languages at phone width: the direction rows fit on one line.
// Slice screenshots: Humpty Dumpty, Shadow-17, a gap slice, the cell-first tip, and the Slice panel in Russian.
// Shells (W4b): the slider builds 1..15 shells (20, 20, 30, 60, …), the core caption gold. Halves (W5) in the Shadow view: off at first,
// the four main views' front / back / side-on counts, the apart slider only while Halves is on. Screenshots of both.
// W7: kites and squares counted in the caption with a legend only where present; Line up turns the slice's axis to the viewer; the app's
// projection button (3D → ∥ → ISO → REV) shows in all three views and REV's slider lands in this world's panel. Screenshots of kite
// slices lined up, in normal perspective and in full REV.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { WQ_DIRECTIONS as DIRS } from '../../src/app/world-white-queen.js';
import { t, LANG_ORDER } from '../../src/app/i18n.js';
import { sliceU } from '../../src/app/world-white-queen.js';
import { readFileSync } from 'node:fs';
const ATLAS = JSON.parse(readFileSync(new URL('../unit/white-queen-atlas.json', import.meta.url)));

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/wq-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldwhiteQueen-panel';
const EXPECT = { 'vertex-first': [42, 80, 0], 'edge-first': [52, 60, 20], 'face-first': [56, 84, 12], 'cell-first': [44, 72, 6] };
const b = await chromium.launch();
let checks = 0;
async function open(page, query = '') {
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/index.html?probe${query}`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
  return errors;
}
const probe = (page) => page.evaluate(() => window.__whiteQueenProbe());
const counts = (st) => [st.vertices, st.triangles, st.quads];
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } })) {
    const page = await b.newPage({ viewport, hasTouch: true, isMobile: true }), tag = `${door}-${dev}`;
    const errors = await open(page, `&site=${door}`);
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    await page.waitForTimeout(500);
    const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
    assert.equal(worlds[worlds.indexOf('tool:bloomWorld') + 1], 'tool:whiteQueenWorld', `${tag}: right after the Icosaxes Bloom`); checks++;
    await page.locator('[data-action="tool:whiteQueenWorld"]').first().tap(); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    const caption = () => page.locator(`${P} .ch-param-caption`).textContent();
    let st = await probe(page);
    assert.deepEqual([st.from, st.to, st.u], ['vertex-first', 'cell-first', 0], `${tag}: default turning`);
    assert.ok(!(await page.locator(`${P} [data-wq-to="vertex-first"]`).isVisible()), `${tag}: To hides From's direction`); checks++;
    for (const end of ['from', 'to']) for (const k of DIRS) {
      const btn = page.locator(`${P} [data-wq-${end}="${k}"]`);
      if (!(await btn.isVisible())) continue;
      const bx = await btn.boundingBox(); assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${end} ${k} touchable`);
    }
    checks++;
    const tapFrom = async (k) => { await page.tap(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(350); };
    const tapTo = async (k) => { await page.tap(`${P} [data-wq-to="${k}"]`); await page.waitForTimeout(350); };
    const turnings = DIRS.flatMap((a, i) => DIRS.slice(i + 1).map((b) => [a, b]));
    assert.equal(turnings.length, 6);
    for (const [a, z] of turnings) {
      await tapFrom(a); st = await probe(page);
      assert.deepEqual([st.from, st.u, st.stop], [a, 0, a], `${tag}: From ${a}`); assert.deepEqual(counts(st), EXPECT[a], `${tag}: ${a} counts`);
      assert.ok((await caption()).startsWith(`${t(`wq.dir.${a}`, 'en')} · ${EXPECT[a][0]} vertices`), `${tag}: ${a} caption`);
      await tapTo(z); st = await probe(page);
      assert.deepEqual([st.from, st.to, st.u, st.stop], [a, z, 1000, z], `${tag}: ${a} → To ${z}`); assert.deepEqual(counts(st), EXPECT[z], `${tag}: ${z} counts`);
      assert.equal(st.edges, 720);
      assert.ok((await caption()).startsWith(`${t(`wq.dir.${z}`, 'en')} · ${EXPECT[z][0]} vertices`), `${tag}: ${z} caption`); checks++;
    }
    // From = the current To swaps the two
    await tapFrom('cell-first'); await tapTo('vertex-first'); await tapFrom('vertex-first'); st = await probe(page);
    assert.deepEqual([st.from, st.to], ['vertex-first', 'cell-first'], `${tag}: swap`); checks++;
    const slider = page.locator(`${P} .wq-param-row input`), sb = await slider.boundingBox();
    assert.ok(sb.width >= viewport.width * 0.8 && sb.height >= 40 && sb.y > viewport.height * 0.6, `${tag}: big slider at the bottom ${JSON.stringify(sb)}`); checks++;
    for (const [v, u, k] of [[25, 0, 'vertex-first'], [975, 1000, 'cell-first']]) {
      await slider.fill(String(v)); await page.waitForTimeout(400);
      st = await probe(page); assert.equal(st.u, u, `${tag}: snaps to ${k}`); assert.deepEqual(counts(st), EXPECT[k]); checks++;
    }
    await slider.fill('500'); await page.waitForTimeout(400);
    st = await probe(page); assert.equal(st.stop, null); assert.equal(st.u, 500);
    assert.ok((await caption()).startsWith(t('wq.between', 'en', { a: t('wq.dir.vertex-first', 'en'), b: t('wq.dir.cell-first', 'en') })), `${tag}: between`); checks++;
    // the Slice view
    await page.tap(`${P} [data-wq-mode="slice"]`); await page.waitForTimeout(400);
    st = await probe(page); assert.equal(st.mode, 'slice');
    assert.ok(!(await page.locator(`${P} [data-wq-row="from"]`).isVisible()) && !(await page.locator(`${P} .wq-param-row`).isVisible()), `${tag}: Shadow rows hidden in Slice`);
    const sl = page.locator(`${P} .wq-slice-row input`);
    for (const dir of DIRS) {
      await page.tap(`${P} [data-wq-slice="${dir}"]`); await page.waitForTimeout(300);
      const E = ATLAS.filter((e) => e.direction === dir);
      for (let k = 0; k < E.length; k++) {
        await sl.fill(String(Math.min(1000, sliceU(dir, k) + (k ? 1 : 0)))); await page.waitForTimeout(120);
        st = await probe(page);
        assert.deepEqual([st.dir, st.k, st.height, st.V], [dir, k, E[k].height, E[k].V], `${tag}: ${dir} stop ${k}`);
        if (E[k].dim === undefined) assert.deepEqual(st.faceSizes, Object.fromEntries(Object.entries(E[k].face_sizes).map(([a, b]) => [a, b])), `${tag}: ${dir} ${E[k].height} faces`);
        else assert.equal(st.dim, E[k].dim);
      }
      checks++;
    }
    for (const [dir, h, key] of [['edge-first', '1 + √5', 'shadow17'], ['cell-first', '1 + 1/2√5', 'humpty']]) {
      await page.tap(`${P} [data-wq-slice="${dir}"]`); await page.waitForTimeout(200);
      const k = ATLAS.filter((e) => e.direction === dir).findIndex((e) => e.height === h);
      await sl.fill(String(sliceU(dir, k))); await page.waitForTimeout(300);
      st = await probe(page); assert.equal(st.named, key);
      assert.ok((await caption()).startsWith(t(`wq.name.${key}`, 'en')), `${tag}: ${key} caption`);
      assert.ok(await page.locator(`${P} .ch-param-caption.wq-gold`).count(), `${tag}: ${key} gold`); checks++;
    }
    // kites, squares, legend and Line up (W7)
    await page.tap(`${P} [data-wq-slice="edge-first"]`); await sl.fill('0'); await page.waitForTimeout(300);
    st = await probe(page); assert.equal(st.quadKinds.kite, 20, `${tag}: edge-first centre kites`);
    assert.ok((await caption()).includes('20 kites') && await page.locator(`${P} .wq-legend`).isVisible(), `${tag}: kites in caption and legend`);
    await page.tap(`${P} [data-wq-lineup]`); await page.waitForTimeout(300);
    st = await probe(page); assert.ok(st.lineUp && Math.abs(st.axis[2] - 1) < 1e-6, `${tag}: lined up ${st.axis}`);
    await page.tap(`${P} [data-wq-lineup]`); await page.waitForTimeout(200);
    await page.tap(`${P} [data-wq-slice="vertex-first"]`); await page.waitForTimeout(300);
    assert.ok(!(await page.locator(`${P} .wq-legend`).isVisible()), `${tag}: no legend without kites or squares`);
    const sqK = ATLAS.filter((e) => e.direction === 'vertex-first').findIndex((e) => !e.at_vertex_layer && e.face_sizes?.['4']);
    await sl.fill(String(sliceU('vertex-first', sqK))); await page.waitForTimeout(300); st = await probe(page);
    if (st.quadKinds.square) assert.ok((await caption()).includes(`${st.quadKinds.square} squares`), `${tag}: squares in caption`);
    checks++;
    // the projection button in all three views; REV's slider in this world's panel
    const proj = page.locator('#projection-toggle');
    for (const mode of ['slice', 'shells', 'shadow']) {
      await page.tap(`${P} [data-wq-mode="${mode}"]`); await page.waitForTimeout(250);
      assert.ok(await proj.isVisible(), `${tag}: projection button in ${mode}`);
      for (const want of ['∥', 'ISO', 'REV']) { await proj.tap(); await page.waitForTimeout(250); assert.equal((await proj.textContent()).trim(), want); }
      assert.ok(await page.locator(`${P} #reverse-row`).isVisible(), `${tag}: REV slider in the panel (${mode})`);
      await proj.tap(); await page.waitForTimeout(250); assert.equal((await proj.textContent()).trim(), '3D');
    }
    await page.tap(`${P} [data-wq-mode="slice"]`); await page.waitForTimeout(250);
    await page.tap(`${P} [data-wq-slice="cell-first"]`); await page.waitForTimeout(200);
    await sl.fill(String(sliceU('cell-first', ATLAS.filter((e) => e.direction === 'cell-first').findIndex((e) => e.height === '1 + 1/2√5')))); await page.waitForTimeout(400);
    checks++;
    // Humpty Dumpty turns on his own, and stops when the picture is touched
    const a0 = (await probe(page)).spinAngle; await page.waitForTimeout(800); st = await probe(page);
    assert.ok(st.humpty && st.spinning && st.spinAngle > a0, `${tag}: Humpty turns`);
    await page.touchscreen.tap(viewport.width / 2, viewport.height * 0.3); await page.waitForTimeout(300);
    const a1 = (await probe(page)).spinAngle; await page.waitForTimeout(500); st = await probe(page);
    assert.ok(!st.spinning && st.spinAngle === a1, `${tag}: Humpty stops when touched`); checks++;
    // Shells
    await page.tap(`${P} [data-wq-mode="shells"]`); await page.waitForTimeout(400);
    assert.ok(!(await page.locator(`${P} [data-wq-row="slice"]`).isVisible()) && !(await page.locator(`${P} .wq-halves-row`).isVisible()), `${tag}: only the Shells rows`);
    const SIZES = [20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20], shl = page.locator(`${P} .wq-shells-row input`);
    for (let n = 1; n <= 15; n++) {
      await shl.fill(String(n)); await page.waitForTimeout(150);
      st = await probe(page); assert.deepEqual([st.mode, st.shells, st.newest.pieces], ['shells', n, SIZES[n - 1]], `${tag}: ${n} shells`);
      const cap = await caption();
      assert.ok(n === 1 ? cap === t('wq.shells.core', 'en') : cap.includes(`${SIZES[n - 1]} pieces · one kind`), `${tag}: shells caption ${cap}`);
      assert.equal(await page.locator(`${P} .ch-param-caption.wq-gold`).count(), n === 1 ? 1 : 0);
    }
    checks++;
    // Whole (DICTO 2026-10-28): all 15 shells cut open; the slider steps aside; every shell keeps cells on the far side of the cut
    await page.tap(`${P} [data-wq-whole]`); await page.waitForTimeout(500);
    st = await probe(page);
    assert.ok(st.whole && st.wholeKept.length === 15 && st.wholeKept.every((n) => n > 0), `${tag}: Whole keeps cells of every shell ${JSON.stringify(st.wholeKept)}`);
    const kept = st.wholeKept.reduce((a, b) => a + b, 0);
    assert.ok(kept > 240 && kept < 360, `${tag}: Whole shows about half the 600 cells (${kept})`);
    assert.ok(!(await page.locator(`${P} .wq-shells-row`).isVisible()), `${tag}: Whole hides the shells slider`);
    assert.equal(await caption(), t('wq.shells.whole', 'en'), `${tag}: Whole caption`);
    await page.tap(`${P} [data-wq-whole]`); await page.waitForTimeout(400);
    st = await probe(page); assert.ok(!st.whole && (await page.locator(`${P} .wq-shells-row`).isVisible()), `${tag}: Whole off again`);
    checks++;
    // the links both ways with Aristotle's Pyramid (paper #44): the back link only at the Cleo core
    assert.ok(!(await page.locator(`${P} [data-wq-link]`).isVisible()), `${tag}: no Aristotle link beyond the core`);
    await shl.fill('1'); await page.waitForTimeout(250);
    const leave = async () => { await page.waitForTimeout(500); if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]'); };
    await page.tap(`${P} [data-wq-link]`); await leave();
    await page.waitForSelector('#worldaristotle-panel.visible'); await page.waitForTimeout(800);
    let ar = await page.evaluate(() => window.__aristotleProbe());
    assert.deepEqual([ar.mode, ar.solid], ['pyramids', 'icosahedron'], `${tag}: back link opens the Cleo-Icos`);
    assert.equal(await page.locator('#worldaristotle-panel [data-ar="whiteQueen"]').textContent(), t('ar.link.whiteQueen', 'en'));
    await page.tap('#worldaristotle-panel [data-ar="whiteQueen"]'); await leave();
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(800);
    st = await probe(page); assert.deepEqual([st.mode, st.shells], ['shells', 1], `${tag}: Aristotle links to the Cleo core`);
    assert.equal(await page.locator(`${P} [data-wq-link]`).textContent(), t('wq.link.aristotle', 'en')); checks++;
    // Halves, in the Shadow view
    await page.tap(`${P} [data-wq-mode="shadow"]`); await page.waitForTimeout(300);
    st = await probe(page); assert.equal(st.mode, 'shadow'); assert.equal(st.halves, null, `${tag}: Halves off at first`);
    assert.ok(!(await page.locator(`${P} .wq-apart-row`).isVisible()), `${tag}: no apart slider while Halves is off`);
    await page.tap(`${P} [data-wq-halves]`); await page.waitForTimeout(300);
    const HALF = { 'vertex-first': [270, 270, 60], 'edge-first': [290, 290, 20], 'face-first': [288, 288, 24], 'cell-first': [273, 273, 54] };
    for (const k of DIRS) {
      await tapFrom(k); st = await probe(page);
      assert.deepEqual([st.halves.front, st.halves.back, st.halves.side], HALF[k], `${tag}: halves ${k}`);
      assert.ok((await caption()).includes(`${HALF[k][0]} front · ${HALF[k][1]} back · ${HALF[k][2]} side-on`), `${tag}: halves caption ${k}`);
    }
    await page.locator(`${P} .wq-apart-row input`).fill('500'); await page.waitForTimeout(250);
    assert.equal((await probe(page)).halves.apart, 500); checks++;
    await page.tap(`${P} [data-wq-halves]`); await page.waitForTimeout(250);
    assert.equal((await probe(page)).halves, null); assert.ok(!(await page.locator(`${P} .wq-apart-row`).isVisible()));
    // nothing unnecessary: the app's lattice-view button is hidden in this world
    assert.ok(!(await page.locator('#hud-quick-lattice-view').isVisible()), `${tag}: no lattice view`); checks++;
    assert.deepEqual(errors, [], `${tag}: console errors`);
    console.log('ok', tag); await page.close();
  }
}
for (const [short, key] of [['vertex', 'vertex-first'], ['cell', 'cell-first']]) {
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, `&site=kaleidohedra&open=whitequeen:${short}`);
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  const st = await probe(page); assert.equal(st.stop, key, `?open=whitequeen:${short}`); assert.deepEqual(counts(st), EXPECT[key]);
  assert.deepEqual(errors, [], `?open=whitequeen:${short}: console errors`); checks++;
  await page.close();
}
// the cover in the DICTO menu: the Cleo shells, the gold core and the shells' own colours on the card's rotating preview
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, deviceScaleFactor: 3, hasTouch: dev === 'phone', isMobile: dev === 'phone' });
  const errors = await open(page, '&site=kaleidohedra');
  await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
  if (!(await page.locator('[data-action="tool:whiteQueenWorld"]').count())) await page.click('.dim-wizard-card-btn[data-dim="3D"]');
  const card = page.locator('[data-action="tool:whiteQueenWorld"]').first();
  await card.scrollIntoViewIfNeeded(); await page.waitForTimeout(1200);
  const hues = await card.evaluate((el) => {
    const c = el.querySelector('canvas.dim-wizard-preview'); if (!c) return null;
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let gold = 0, blue = 0, green = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i + 3] < 100) continue; const [r, g, bl] = [d[i], d[i + 1], d[i + 2]];
      if (r > 200 && g > 150 && bl < 140) gold++; else if (bl > r + 30 && bl >= g) blue++; else if (g > r + 30 && g > bl) green++; }
    return { gold, blue, green };
  });
  assert.ok(hues && hues.gold > 0 && hues.blue > 0 && hues.green > 0, `${dev}: the cover shows the gold core and coloured shells ${JSON.stringify(hues)}`); checks++;
  await card.screenshot({ path: `${SH}/${dev}-cover-card.png` });
  await page.screenshot({ path: `${SH}/${dev}-cover-menu.png` });
  assert.deepEqual(errors, [], `${dev} cover: console errors`);
  await page.close();
}
// every language at phone width: the direction rows fit on one line (no wrap, no sideways scroll)
{
  const page = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const errors = await open(page, '&site=kaleidohedra&open=whitequeen:vertex');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  for (const L of LANG_ORDER) {
    await page.selectOption('#hud-tools .lang-btn select', L); await page.waitForTimeout(300);
    for (const mode of ['shadow', 'slice', 'shells']) {
      await page.tap(`${P} [data-wq-mode="${mode}"]`); await page.waitForTimeout(250);
      const rows = await page.evaluate((sel) => [...document.querySelectorAll(`${sel} .wq-row, ${sel} .wq-modes`)].filter((r) => r.offsetParent)
        .map((r) => ({ over: r.scrollWidth - r.clientWidth, tall: r.getBoundingClientRect().height, btn: Math.max(...[...r.querySelectorAll('button')].map((x) => x.getBoundingClientRect().height)) })), P);
      for (const r of rows) assert.ok(r.over <= 1 && r.tall < r.btn * 1.5, `${L} ${mode}: a direction row overflows ${JSON.stringify(r)}`);
      if (L === 'ru' && mode === 'slice') await page.screenshot({ path: `${SH}/phone-ru-slice.png` });
    }
    checks++;
  }
  await page.selectOption('#hud-tools .lang-btn select', 'en');
  assert.deepEqual(errors, [], 'languages: console errors');
  await page.close();
}
for (const [dev, viewport] of Object.entries({ phone: { width: 390, height: 844 }, desktop: { width: 1280, height: 800 } })) {
  const page = await b.newPage({ viewport, hasTouch: dev !== 'desktop', isMobile: dev !== 'desktop' });
  const errors = await open(page, '&site=kaleidohedra&open=whitequeen:vertex');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1500);
  for (const k of DIRS) {
    await page.click(`${P} [data-wq-from="${k}"]`); await page.waitForTimeout(700);
    await page.screenshot({ path: `${SH}/${dev}-${k}.png` });
  }
  await page.click(`${P} [data-wq-from="vertex-first"]`); await page.click(`${P} [data-wq-to="cell-first"]`);
  await page.locator(`${P} .wq-param-row input`).fill('500'); await page.waitForTimeout(700);
  await page.screenshot({ path: `${SH}/${dev}-between-vertex-cell.png` });
  await page.click(`${P} [data-wq-mode="slice"]`);
  for (const [dir, h, name] of [['cell-first', '1 + 1/2√5', 'slice-humpty'], ['edge-first', '1 + √5', 'slice-shadow17'], ['face-first', '-1/6 + 1/6√5', 'slice-face-gap'], ['cell-first', '7/4 + 3/4√5', 'slice-cell-tip'], ['edge-first', '5/2 + 1/2√5', 'slice-edge-tip']]) {
    await page.click(`${P} [data-wq-slice="${dir}"]`);
    const k = ATLAS.filter((e) => e.direction === dir).findIndex((e) => e.height === h);
    await page.locator(`${P} .wq-slice-row input`).fill(String(sliceU(dir, k))); await page.waitForTimeout(900);
    await page.screenshot({ path: `${SH}/${dev}-${name}.png` });
  }
  await page.click(`${P} [data-wq-mode="shells"]`);
  for (const n of [1, 3, 7, 12, 14, 15]) {
    await page.locator(`${P} .wq-shells-row input`).fill(String(n)); await page.waitForTimeout(1100);
    await page.screenshot({ path: `${SH}/${dev}-shells-${n}.png` });
  }
  await page.click(`${P} [data-wq-whole]`); await page.waitForTimeout(1100);
  await page.screenshot({ path: `${SH}/${dev}-shells-whole.png` });
  await page.click(`${P} [data-wq-whole]`); await page.waitForTimeout(300);
  // kite slices lined up, in normal perspective and in full reverse perspective
  await page.click(`${P} [data-wq-mode="slice"]`); await page.click(`${P} [data-wq-lineup]`);
  for (const [dir, h] of [['edge-first', '0'], ['cell-first', '11/8 + 5/8√5']]) {
    await page.click(`${P} [data-wq-slice="${dir}"]`);
    const k = ATLAS.filter((e) => e.direction === dir).findIndex((e) => e.height === h);
    await page.locator(`${P} .wq-slice-row input`).fill(String(sliceU(dir, k))); await page.waitForTimeout(1100);
    const nm = `${dev}-kites-${dir}-lined-up`;
    await page.screenshot({ path: `${SH}/${nm}.png` });
    for (let i = 0; i < 3; i++) await page.click('#projection-toggle');   // 3D → ∥ → ISO → REV
    await page.locator('#reverse-row input').fill('-100'); await page.locator('#reverse-row input').dispatchEvent('input'); await page.waitForTimeout(1100);
    await page.screenshot({ path: `${SH}/${nm}-rev.png` });
    await page.click('#projection-toggle'); await page.waitForTimeout(300);   // back to 3D
  }
  await page.click(`${P} [data-wq-lineup]`); await page.click(`${P} [data-wq-mode="shells"]`);
  await page.locator(`${P} .wq-shells-row input`).fill('1'); await page.waitForTimeout(300);
  await page.click(`${P} [data-wq-link]`); await page.waitForTimeout(600);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await page.click('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector('#worldaristotle-panel.visible'); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-aristotle-link.png` });
  await page.click('#worldaristotle-panel [data-ar="whiteQueen"]'); await page.waitForTimeout(600);
  if (await page.locator('#leave-dialog:not([hidden])').count()) await page.click('#leave-dialog [data-choice="keep"]');
  await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${SH}/${dev}-shells-core-link.png` });
  await page.click(`${P} [data-wq-mode="shadow"]`); await page.click(`${P} [data-wq-halves]`);
  for (const [k, a] of [['vertex-first', 0], ['vertex-first', 600], ['cell-first', 600]]) {
    await page.click(`${P} [data-wq-from="${k}"]`); await page.locator(`${P} .wq-apart-row input`).fill(String(a));
    await page.locator(`${P} .wq-apart-row input`).dispatchEvent('change'); await page.waitForTimeout(1100);
    await page.screenshot({ path: `${SH}/${dev}-halves-${k}-${a}.png` });
  }
  await page.click(`${P} [data-wq-halves]`);
  assert.deepEqual(errors, [], `${dev} screenshots: console errors`); checks++;
  await page.close();
}
await b.close();
console.log(`white-queen OK: ${checks} checks`);
