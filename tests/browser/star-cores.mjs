// DICTO's four Star Cores solids and Kagemusha's crests in Polyhedraverse, and the Star Cores world in Kaleidohedra (DICTO 2026-11-02),
// through the real UI on a phone (390 × 844) and an iPad (820 × 1180), both touch:
// - Polyhedraverse door, DICTO's pieces (and the 42 Star Cores shapes new to PV in their own section, two of them built): Cube Pearl, Golden Clasp, Hamlet, Ophelia first in DICTO's own section; a "Kagemusha's crests"
//   section after it with Kagemusha + MAEDATE, Kagemusha + KUWAGATA, MAEDATE, KUWAGATA; each card's details, Build and a tap on the outline place that one piece (★ Star step
//   offered on the four convex solids);
// - Kaleidohedra door: the Star Cores card right after HexOct opens the world in Kaleidohedra; the shape list (52, newest first), the
//   t = 2 / t = φ buttons and one long step slider, no ◀ ▶ buttons, no paint, shear or lattice-view controls; tapping along the slider
//   steps solid → star → halo (glass) → core (the star as glass round it) and on to the last turn; edges ≥ 1.5 px;
// - ?open=starcores:D40:phi:3 from both doors opens the GTI's core at t = φ in Kaleidohedra. No console errors.
// Screenshots in $SHOTS (default /tmp/star-cores-shots): <dev>-pv-<id>.png, <dev>-sc-<phase>.png, <dev>-sc-link.png.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/star-cores-shots';
mkdirSync(SH, { recursive: true });
const DEVICES = {
  phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 },
  ipad: { viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 },
};
const P = '#worldstarCores-panel';
const NEW4 = ['DICTO_CUBE_PEARL', 'DICTO_GOLDEN_CLASP', 'DICTO_HAMLET', 'DICTO_OPHELIA'];
const CRESTS = ['KAGEMUSHA_MAEDATE', 'KAGEMUSHA_KUWAGATA', 'DICTO_MAEDATE', 'DICTO_KUWAGATA'];
// two of the 42 Star Cores shapes new to PV (the section "Star Cores shapes", newest first: the TI Star core D105 first)
const SC_PICK = ['DICTO_SC_TI_STAR_CORE', 'DICTO_SC_OGDOECONTAHEDRON'];
const b = await chromium.launch();
let checks = 0;
for (const dev of Object.keys(DEVICES)) {
  const ctx = await b.newContext(DEVICES[dev]), page = await ctx.newPage(), errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const tap = (sel) => page.tap(sel);
  const probe = () => page.evaluate(() => window.__starCoresProbe());
  const enter = async (site, extra = '') => {
    await page.goto(`${BASE}/index.html?probe&site=${site}${extra}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }).catch(() => {});
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(800);
  };
  // over a saved build the app asks first: start fresh where it offers that (one piece at a time here), else keep the build
  const keep = async () => {
    for (let i = 0; i < 3; i++) {
    if (!(await page.locator('#leave-dialog:not([hidden])').count())) return;
    const pick = (await page.locator('#leave-dialog [data-choice="fresh"]').count()) ? 'fresh' : (await page.locator('#leave-dialog [data-choice="keep"]').count()) ? 'keep' : 'continue';
    await tap(`#leave-dialog [data-choice="${pick}"]`); await page.waitForTimeout(900);
    }
  };

  // ---- Polyhedraverse: DICTO's pieces ----
  const openPieces = async () => {
    await enter('polyhedraverse');
    await page.waitForSelector('.dim-wizard-overlay.open');
    if (!(await page.locator('[data-family="DICTO_PIECES"]').count())) await tap('.dim-wizard-card-btn[data-dim="3D"]');
    const fam = page.locator('[data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await page.waitForTimeout(900);
  };
  pv: {
  if (process.env.ONLY === 'world') break pv;   // ONLY=world: the Star Cores world alone
  await openPieces();
  const own = await page.locator('.poly-section[data-section="dicto"] [data-action]').evaluateAll((els) => els.map((e) => e.dataset.action.replace('tool:polyShape:', '')));
  assert.deepEqual(own.slice(0, 4), NEW4, `${dev}: the four new solids first in DICTO's own`);
  const sections = await page.locator('.poly-section').evaluateAll((els) => els.map((e) => e.dataset.section));
  assert.equal(sections[sections.indexOf('dicto') + 1], 'crests', `${dev}: the crests right after DICTO's own`);
  assert.equal(sections[sections.indexOf('dicto') + 2], 'starCores', `${dev}: then the Star Cores shapes`);
  const sc = await page.locator('.poly-section[data-section="starCores"] [data-action]').evaluateAll((els) => els.map((e) => e.dataset.action.replace('tool:polyShape:', '')));
  assert.equal(sc.length, 42, `${dev}: 42 Star Cores shapes`); assert.equal(sc[0], 'DICTO_SC_TI_STAR_CORE', `${dev}: newest first`);
  assert.equal((await page.textContent('.poly-section[data-section="starCores"] .poly-section-title')).trim(), 'Star Cores shapes');
  assert.equal((await page.textContent('.poly-section[data-section="crests"] .poly-section-title')).trim(), "Kagemusha's crests");
  const crests = await page.locator('.poly-section[data-section="crests"] [data-action]').evaluateAll((els) => els.map((e) => e.dataset.action.replace('tool:polyShape:', '')));
  assert.deepEqual(crests, CRESTS, `${dev}: the crests`); checks += 3;
  for (const id of [...NEW4, ...CRESTS, ...SC_PICK]) {
    if (id !== NEW4[0]) await openPieces();
    const card = page.locator(`[data-action="tool:polyShape:${id}"]`).first();
    await card.scrollIntoViewIfNeeded();
    const bx = await card.boundingBox(); assert.ok(bx.width >= 44 && bx.height >= 44, `${dev} ${id}: touchable card`);
    await card.tap(); await page.waitForTimeout(700);
    // the shape's details, then Build
    const build = page.locator('.poly-detail-build'); await build.waitFor({ state: 'visible', timeout: 15000 }); await build.scrollIntoViewIfNeeded();
    await build.tap(); await page.waitForTimeout(500); await keep();
    await page.waitForFunction(() => !document.querySelector('.dim-wizard-overlay.open'), null, { timeout: 15000 }); await page.waitForTimeout(1500);
    const c = await (await page.$('canvas')).boundingBox();
    await page.touchscreen.tap(c.x + c.width / 2, c.y + c.height / 2); await page.waitForTimeout(1800);   // the outline: tap it to place the piece
    const st = await page.evaluate(() => window.__polyProbe.state());
    assert.equal(st.nodes.length, 1, `${dev} ${id}: one piece`); assert.equal(st.nodes[0].shape, id, `${dev} ${id}: the piece`);
    const star = page.locator('.poly-star-go');
    // ★ Star step wherever the piece is convex with its centre inside every face (the four solids, MAEDATE), not on Kagemusha with crests
    const convex = await page.evaluate(async (sid) => { const { solidOf } = await import('./src/app/star-step-geometry.js'); const { POLYHEDRA } = await import('./src/krp-core/src/polyhedra/index.js'); return !!solidOf(POLYHEDRA[sid]); }, id);
    if (NEW4.includes(id)) assert.ok(convex, `${dev} ${id}: convex`);
    if (id.startsWith('KAGEMUSHA_')) assert.ok(!convex, `${dev} ${id}: not convex`);
    assert.equal(await star.isVisible().catch(() => false), convex, `${dev} ${id}: ★ Star step exactly when convex`);
    await page.screenshot({ path: `${SH}/${dev}-pv-${id}.png` });
    checks += 2;
  }

  }

  // ---- Kaleidohedra: the Star Cores world ----
  await enter('kaleidohedra');
  await page.waitForSelector('.dim-wizard-overlay.open');
  if (!(await page.locator('[data-action="tool:starCoresWorld"]').count())) await tap('.dim-wizard-card-btn[data-dim="3D"]');
  await page.waitForTimeout(500);
  const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((x) => /World$/.test(x)));
  assert.equal(worlds[worlds.indexOf('tool:hexoctWorld') + 1], 'tool:starCoresWorld', `${dev}: right after HexOct`);
  assert.equal(worlds[0], 'tool:dictonicWorld', `${dev}: DICTONIC still first`); checks++;
  const card = page.locator('[data-action="tool:starCoresWorld"]').first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await page.waitForTimeout(400);
  await keep();
  await page.waitForSelector(`${P}.visible`);
  await page.waitForFunction(() => window.__starCoresProbe()?.chain === true, null, { timeout: 30000 }); await page.waitForTimeout(800);
  assert.equal((await page.textContent('#hud-world-title')).trim(), 'Star Cores', `${dev}: title`);
  assert.equal(await page.evaluate(async () => (await import('./src/app/site.js')).activeSite()), 'kaleidohedra', `${dev}: in Kaleidohedra`);
  for (const sel of ['#hud-quick-lattice-view', '#shear-panel']) assert.ok(!(await page.locator(sel).isVisible().catch(() => false)), `${dev}: ${sel} hidden`);
  const texts = await page.locator(`${P} button`).evaluateAll((els) => els.filter((e) => e.offsetParent).map((e) => e.textContent));
  assert.ok(!texts.some((x) => /[◀▶◁▷←→‹›«»]/.test(x)), `${dev}: no arrow buttons (${texts.join(' | ')})`); checks += 2;
  const options = await page.locator(`${P} [data-sc-shape] option`).evaluateAll((els) => els.map((e) => e.value));
  assert.equal(options.length, 52); assert.deepEqual(options.slice(0, 4), ['D109', 'D108', 'D107', 'D106'], `${dev}: newest first`);
  // pick Cube Pearl, t = 2
  await page.selectOption(`${P} [data-sc-shape]`, 'D106'); await page.waitForTimeout(600);
  if ((await probe()).t !== '2') { await tap(`${P} [data-sc-t="2"]`); await page.waitForTimeout(500); }
  let st = await probe();
  assert.deepEqual([st.shape, st.t, st.pos, st.phase, st.corners, st.faces, st.max], ['D106', '2', 0, 'solid', 32, 18, 19], `${dev}: Cube Pearl`);
  assert.ok(st.lineWidths.every((w) => w >= 1.5), `${dev}: edges ${st.lineWidths}`); checks += 2;
  // the slider: long, and a tap along it sets the step
  const slider = page.locator(`${P} [data-sc-step]`), sb = await slider.boundingBox();
  assert.ok(sb.width >= Math.min(300, DEVICES[dev].viewport.width * 0.55) && sb.height >= 30, `${dev}: a long slider ${sb.width} × ${sb.height}`);
  // a finger drag of the slider's thumb (touch events through CDP): from where the thumb is to where step `pos` sits
  const cdp = await ctx.newCDPSession(page);
  const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
  const tapAt = async (pos, max) => {
    const bx = await slider.boundingBox();   // measured now: the panel's text above it changes with each step
    const th = 40, xOf = (p) => bx.x + th / 2 + (bx.width - th) * (p / max), y = bx.y + bx.height / 2;
    const from = xOf((await probe()).pos), to = xOf(pos);
    await touch('touchStart', from, y);
    // past the target first (a finger moves more than the touch slop before the thumb follows), then back onto it
    const over = to + (to >= from ? 40 : -40);
    for (let i = 1; i <= 12; i++) { await touch('touchMove', from + ((over - from) * i) / 12, y); await page.waitForTimeout(25); }
    for (let i = 1; i <= 4; i++) { await touch('touchMove', over + ((to - over) * i) / 4, y); await page.waitForTimeout(25); }
    await touch('touchEnd', to, y); await page.waitForTimeout(800);
  };
  const want = { 1: ['star', 0], 2: ['halo', 1], 3: ['core', 2] };
  for (const [pos, [phase, glassMin]] of Object.entries(want)) {
    await tapAt(Number(pos), 19);
    st = await probe();
    assert.deepEqual([st.pos, st.phase, st.turn], [Number(pos), phase, 0], `${dev}: step ${pos}`);
    assert.ok(st.glass >= glassMin, `${dev} ${phase}: see-through helpers (${st.glass})`);
    const cap = await page.textContent(`${P} .sc-caption`);
    assert.match(cap, new RegExp(`Turn 1 · ${phase[0].toUpperCase()}${phase.slice(1)}`), `${dev}: caption ${cap}`);
    if (phase === 'star') { assert.deepEqual(st.star, { v: 50, f: 96 }); assert.match(cap, /50 corners, 96 faces/, `${dev}: the star's own counts`); }
    if (phase === 'core') { assert.deepEqual(st.core, { corners: 24, faces: 14 }); assert.match(cap, /24 corners, 14 faces/); }
    await page.screenshot({ path: `${SH}/${dev}-sc-${phase}.png` });
    checks++;
  }
  // the end of the chain: turn 5's core is turn 4's solid again (period two)
  await tapAt(19, 19);
  st = await probe();
  assert.deepEqual([st.pos, st.turn, st.phase], [19, 4, 'core'], `${dev}: the last core`);
  assert.match(await page.textContent(`${P} .sc-caption`), /period two/); checks++;
  // t = φ
  await tap(`${P} [data-sc-t="phi"]`); await page.waitForTimeout(600);
  st = await probe();
  assert.equal(st.t, 'phi'); assert.equal(await page.getAttribute(`${P} [data-sc-t="phi"]`, 'aria-pressed'), 'true'); checks++;
  // a large one: Ophelia's star at t = 2
  await page.selectOption(`${P} [data-sc-shape]`, 'D109'); await tap(`${P} [data-sc-t="2"]`); await page.waitForTimeout(800);
  await tapAt(2, (await probe()).max);
  st = await probe();
  assert.deepEqual([st.shape, st.phase, st.corners], ['D109', 'halo', 642], `${dev}: Ophelia's halo`);
  await page.screenshot({ path: `${SH}/${dev}-sc-ophelia-halo.png` }); checks++;
  // the deep link, from both doors
  for (const site of ['kaleidohedra', 'polyhedraverse']) {
    await enter(site, '&open=starcores:D40:phi:3'); await keep();
    await page.waitForFunction(() => window.__starCoresProbe?.()?.chain === true && window.__starCoresProbe().shape === 'D40', null, { timeout: 30000 }); await page.waitForTimeout(800);
    st = await probe();
    assert.deepEqual([st.shape, st.t, st.pos, st.phase, st.core?.corners], ['D40', 'phi', 3, 'core', 30], `${dev} ${site}: the GTI's core`);
    assert.equal(await page.evaluate(async () => (await import('./src/app/site.js')).activeSite()), 'kaleidohedra', `${dev} ${site}: opens in Kaleidohedra`);
    assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0);
    if (site === 'kaleidohedra') await page.screenshot({ path: `${SH}/${dev}-sc-link.png` });
    checks++;
  }
  assert.deepEqual(errors, [], `${dev}: console errors`);
  await ctx.close();
}
await b.close();
console.log(`star-cores: ${checks} checks passed`);
