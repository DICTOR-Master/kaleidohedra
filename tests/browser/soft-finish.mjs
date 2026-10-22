// Soft (DICTO 2026-10-21), through the real UI from each door: open a build, tap the puffed-square button, turn Soft on,
// go through the finishes, move the Softness slider (shown only while Soft is on), no console errors. In Polyhedraverse the
// same small build (a cube with two square pyramids) is shot Flat Plain, Soft Plain, Soft Metallic, Soft Ceramic, and the
// open panel. SHOTS = where the screenshots go.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Each door in its own process (the node's headless Chromium tires after a few full app loads in one run).
if (!process.env.DOORS) {
  let bad = 0;
  for (const door of ['polyhedraverse', 'rhombiverse', 'kaleidohedra']) for (const vp of (process.env.VPS ?? 'phone,ipad').split(',')) bad += spawnSync(process.execPath, [fileURLToPath(import.meta.url)], { stdio: 'inherit', env: { ...process.env, DOORS: door, VP: vp } }).status ? 1 : 0;
  process.exit(bad ? 1 : 0);
}

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8000';
const SHOTS = process.env.SHOTS ?? '/tmp';
const VP = process.env.VP ?? 'ipad', VIEWPORT = VP === 'phone' ? { width: 390, height: 844 } : { width: 820, height: 1180 };
const BUILD = [
  { id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } },
  { id: 'p0', shape: 'J1_SQUARE_PYRAMID', transform: { position: [0.6414213562373094, 0, 0], quaternion: [-0.6532814824381882, 0.2705980500730985, -0.6532814824381882, 0.2705980500730985] } },
  { id: 'p2', shape: 'J1_SQUARE_PYRAMID', transform: { position: [0, 0.6414213562373094, 0], quaternion: [-0.6532814824381882, 0.27059805007309845, 0.27059805007309845, 0.6532814824381882] } },
];

let failures = 0;
for (const door of process.env.DOORS.split(',')) {
  const browser = await chromium.launch(); // one browser per door: the node's software GL tires over several big app loads
  const ctx = await browser.newContext({ viewport: VIEWPORT, hasTouch: true, isMobile: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource|Ignored attempt to cancel a touch/.test(m.text())) errors.push(m.text()); });
  // "Continue where you left off" when a stored build is entered (the dialog can take a moment)
  const keep = async () => { for (let k = 0; k < 8; k++) { if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="continue"], #leave-dialog [data-choice="keep"]'); await page.waitForTimeout(700); return; } await page.waitForTimeout(400); } };
  page.on('dialog', (d) => d.accept());
  page.on('crash', () => console.log(`${door}: the page crashed`));
  if (door === 'polyhedraverse') {
    await ctx.addInitScript((build) => {
      if (sessionStorage.getItem('seeded')) return;
      sessionStorage.setItem('seeded', '1');
      localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, nodes: build, connections: [], view: {} }));
      localStorage.setItem('polyhedraverse-color-mode', 'type'); // each kind of piece its own colour
    }, BUILD);
  }
  try {
    await page.goto(`${BASE_URL}/index.html?site=${door}&probe`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 });
    await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
    await page.tap('.dim-wizard-close');
    await page.waitForTimeout(1200);
    await keep();
    if (door === 'polyhedraverse') {
      await page.mouse.move(VIEWPORT.width / 2, VIEWPORT.height / 2); await page.mouse.wheel(0, -400); // a little closer
      await page.waitForTimeout(900);
    } else {
      // an empty lattice: tap its outline for the first cell, then tap that cell for a few more
      for (let k = 0; k < 4; k++) { await page.touchscreen.tap(VIEWPORT.width / 2 + 12 * k, VIEWPORT.height / 2 - 10 * k); await page.waitForTimeout(800); }
    }
    const shot = (name) => door === 'polyhedraverse' && page.screenshot({ path: `${SHOTS}/${name}-${VP}.png` });
    if (door === 'polyhedraverse') await shot('soft-1'); // Flat Plain: today's look
    // The button: in the tools column, a line icon (not text), shown in this build.
    await page.waitForSelector('#soft-toggle:not([hidden])', { timeout: 15000 });
    assert.ok(await page.$eval('#soft-toggle', (b) => !!b.querySelector('svg path') && b.textContent.trim() === ''), `${door}: icon button`);
    await page.tap('#soft-toggle');
    await page.waitForTimeout(400);
    assert.ok(await page.$eval('#soft-panel', (p) => p.classList.contains('visible')), `${door}: the panel opens`);
    const sliderShown = () => page.$eval('#soft-panel .soft-amount', (r) => !r.hidden && r.getBoundingClientRect().height > 0);
    if (await page.$eval('#soft-panel [data-mode=soft]', (b) => b.classList.contains('active'))) { await page.tap('#soft-panel [data-mode=flat]'); await page.waitForTimeout(300); }
    assert.equal(await sliderShown(), false, `${door}: no Softness slider while Flat`);
    assert.deepEqual(await page.$$eval('#soft-panel [data-finish]', (bs) => bs.map((b) => b.dataset.finish)), ['plain', 'metallic', 'ceramic'], `${door}: three finishes`);
    await page.tap('#soft-panel [data-finish=plain]');
    await page.tap('#soft-panel [data-mode=soft]');
    await page.waitForTimeout(600);
    assert.equal(await sliderShown(), true, `${door}: Softness slider once Soft is on`);
    // a big slider, low on the screen: right above the bottom buttons or above the other bottom panel there, never over it
    const geo = await page.$eval('#soft-amount', (s) => { const r = s.getBoundingClientRect(), o = [...document.querySelectorAll('.qc-panel.visible:not(#soft-panel), #world4d-panel.visible, #kaleido-body:not([hidden])')].map((e) => e.getBoundingClientRect()).filter((q) => q.height > 0);
      return { w: r.width, h: r.height, bottom: r.bottom, vh: innerHeight, over: o.some((q) => q.top < r.bottom - 1 && q.bottom > r.top + 1), above: o.length ? Math.min(...o.map((q) => q.top)) - r.bottom : null }; });
    assert.ok(geo.w >= 300 && geo.h >= 44 && !geo.over && (geo.vh - geo.bottom < 200 || (geo.above !== null && geo.above < 60)), `a big low slider, clear of other panels ${JSON.stringify(geo)}`);
    if (door === 'polyhedraverse') { await page.screenshot({ path: `${SHOTS}/soft-panel.png` }); }
    const probe = () => page.evaluate(() => window.__softProbe?.());
    if (door !== 'polyhedraverse') {
      const p = await probe();
      console.log(door, 'probe', JSON.stringify(p));
      assert.ok(p.applies && p.twins > 0, `${door}: the lattice cells get puffed copies`);
    }
    // Move the slider by touch: drag its thumb along the track.
    const s = await page.$eval('#soft-amount', (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top + r.height / 2, w: r.width, v: +el.value, max: +el.max }; });
    const before = s.v;
    const cdp = await ctx.newCDPSession(page);
    const drag = async (from, to) => {
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: s.x + s.w * from, y: s.y }] });
      for (let k = 1; k <= 8; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: s.x + s.w * (from + ((to - from) * k) / 8), y: s.y }] }); await page.waitForTimeout(40); }
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await page.waitForTimeout(500);
    };
    await drag(before / s.max, 0.85);
    const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('rv-soft-finish')));
    assert.ok(saved.soft && saved.amount > before / 100 + 0.1, `${door}: Softness moved by touch and remembered ${JSON.stringify(saved)}`);
    await drag(0.85, 25 / s.max);
    // Fold the panel away (its chevron) for the shots, then go through the finishes.
    for (const [i, f] of [[2, 'plain'], [3, 'metallic'], [4, 'ceramic']]) {
      await page.tap(`#soft-panel [data-finish=${f}]`);
      await page.waitForTimeout(500);
      assert.ok(await page.$eval(`#soft-panel [data-finish=${f}]`, (b) => b.classList.contains('active')), `${door}: ${f} chosen`);
      if (door === 'polyhedraverse') {
        await page.tap('#soft-toggle'); await page.waitForTimeout(500); // close the panel for a clear view
        await shot(`soft-${i}`);
        await page.tap('#soft-toggle'); await page.waitForTimeout(300);
      }
    }
    // Remembered after a reload.
    await page.reload({ waitUntil: 'commit' });
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 });
    await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
    await page.tap('.dim-wizard-close');
    await page.waitForTimeout(1000);
    await keep();
    assert.ok(await page.$eval('#soft-toggle', (b) => b.classList.contains('active')), `${door}: Soft remembered`);
    // Back to Flat Plain for the next door.
    await page.tap('#soft-toggle'); await page.waitForTimeout(300);
    await page.tap('#soft-panel [data-finish=plain]'); await page.tap('#soft-panel [data-mode=flat]');
    await page.waitForTimeout(400);
    if (door !== 'polyhedraverse') assert.equal((await probe()).twins, 0, `${door}: Flat Plain is today's look (no copies)`);
    assert.deepEqual(errors, [], `${door}: console errors: ${errors.join(' | ')}`);
    console.log(`ok ${door} ${VP}`);
  } catch (e) {
    failures++;
    console.log(`FAIL ${door} ${VP}: ${e.message.split('\n')[0]}`);
    await page.screenshot({ path: `${SHOTS}/soft-fail-${door}.png` }).catch(() => {});
  }
  await ctx.close().catch(() => {});
  await browser.close();
}
process.exit(failures ? 1 : 0);
