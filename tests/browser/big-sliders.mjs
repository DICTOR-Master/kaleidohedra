// Big sliders and 🌐 everywhere (DICTO 2026-10-13, after an iPad demo), through the real UI on an iPad and a phone:
// the Shear's sliders and a world panel's sliders are long, low (just above the bottom buttons) and thick; the
// 🌐 button is in the tools column, the DICTO menu and the Almanac, and choosing a language redraws the menu.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8000';
const SHOTS = process.env.SHOTS ?? '/tmp';
const browser = await chromium.launch();
for (const [name, viewport] of [['ipad', { width: 1024, height: 1366 }], ['phone', { width: 390, height: 844 }]]) {
  const page = await browser.newPage({ viewport, hasTouch: true, isMobile: true });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE_URL}/index.html?site=kaleidohedra`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 });
  await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open');
  // 🌐 in the DICTO menu: pick Japanese, the menu redraws in it.
  assert.ok(await page.locator('.dim-wizard-header .lang-btn select').count(), `${name}: 🌐 in the DICTO menu`);
  await page.selectOption('.dim-wizard-header .lang-btn select', 'ja');
  await page.waitForTimeout(400);
  const sub = await page.textContent('.dim-wizard-sub');
  console.log(name, 'menu in ja:', sub.slice(0, 40));
  assert.ok(/[぀-ヿ一-鿿]/.test(sub), `${name}: the menu should redraw in Japanese`);
  await page.screenshot({ path: `${SHOTS}/lang-menu-${name}.png` });
  // The Shear panel follows the language too.
  const shearJa = await page.textContent('#kaleido-toggle');
  console.log(name, 'shear in ja:', shearJa);
  assert.ok(/シアー/.test(shearJa), `${name}: the Shear button in Japanese`);
  await page.selectOption('.dim-wizard-header .lang-btn select', 'en');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  // 🌐 at the top of the tools column.
  const firstTool = await page.evaluate(() => document.getElementById('hud-tools').firstElementChild.className);
  assert.equal(firstTool, 'lang-btn', `${name}: 🌐 first in the tools column`);
  // The Shear sheet: Path lowest, long, above the bottom buttons.
  await page.tap('#kaleido-toggle');
  await page.waitForTimeout(400);
  const geo = await page.evaluate(() => {
    const r = (el) => el.getBoundingClientRect();
    const path = r(document.getElementById('kaleido-path')), cell = r(document.getElementById('kaleido-cell'));
    const undo = r(document.getElementById('undo-btn'));
    return { path: [path.left, path.width, path.height, path.bottom], cell: [cell.width, cell.bottom], undoTop: undo.top, vw: innerWidth, vh: innerHeight };
  });
  console.log(name, 'shear', JSON.stringify(geo));
  assert.ok(geo.path[1] >= Math.min(600, geo.vw - 60), `${name}: Path slider long`);
  assert.ok(geo.path[2] >= 44, `${name}: Path slider tall enough for a finger`);
  assert.ok(geo.path[3] > geo.cell[1], `${name}: Path lowest`);
  assert.ok(geo.path[3] <= geo.undoTop && geo.vh - geo.path[3] < 140, `${name}: Path just above the bottom buttons`);
  // Drag the thumb with a finger: the value moves.
  const before = await page.inputValue('#kaleido-path');
  const box = await page.locator('#kaleido-path').boundingBox();
  const startX = box.x + 20 + (box.width - 40) * ((Number(before) - Number(await page.getAttribute('#kaleido-path', 'min') ?? 0)) / ((Number(await page.getAttribute('#kaleido-path', 'max') ?? 1)) - Number(await page.getAttribute('#kaleido-path', 'min') ?? 0) || 1));
  const cdp = await page.context().newCDPSession(page);
  const y = box.y + box.height / 2;
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: startX, y }] });
  for (let i = 1; i <= 10; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: startX + i * 25, y }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  const after = await page.inputValue('#kaleido-path');
  console.log(name, 'path drag', before, '->', after);
  assert.notEqual(after, before, `${name}: a finger drag moves the Path slider`);
  await page.screenshot({ path: `${SHOTS}/shear-${name}.png` });
  await page.tap('#kaleido-toggle');
  // A world panel: Multi-shell chains, its sliders long and lowest.
  await page.evaluate(async () => { document.querySelector('#hud-wizard-cue')?.click(); });
  await page.waitForTimeout(300);
  await page.keyboard.press('Escape');
  const wiz = await page.evaluate(() => !!document.querySelector('.dim-wizard-overlay.open'));
  if (wiz) await page.keyboard.press('Escape');
  await page.tap('#almanac-btn');
  assert.ok(await page.locator('.almanac-header .lang-btn').count(), `${name}: 🌐 in the Almanac`);
  const ids = await page.evaluate(async () => (await import('./src/app/almanac-data.js')).ALMANAC_ENTRIES.map((e) => e.id));
  await page.tap('.almanac-back').catch(() => {});
  const row = page.locator(`.almanac-entry[data-index="${ids.indexOf('dicto:karma')}"]`);
  await row.scrollIntoViewIfNeeded();
  await row.tap();
  await page.tap('.almanac-open');
  await page.waitForTimeout(2500);
  const w = await page.evaluate(() => {
    const ins = [...document.querySelectorAll('#worldchains-panel input[type=range]')].filter((i) => i.offsetParent);
    const undo = document.getElementById('undo-btn').getBoundingClientRect();
    return { sliders: ins.map((i) => { const r = i.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height), Math.round(r.bottom)]; }), undoTop: undo.top, vw: innerWidth };
  });
  console.log(name, 'chains', JSON.stringify(w));
  assert.ok(w.sliders.length && w.sliders.every(([wd, h]) => wd >= Math.min(600, w.vw - 60) && h >= 44), `${name}: world sliders long and tall`);
  assert.ok(w.sliders.every(([, , b]) => b <= w.undoTop), `${name}: world sliders above the bottom buttons`);
  await page.screenshot({ path: `${SHOTS}/chains-${name}.png` });
  // The 4D geared slider: tall, long, lowest in its panel and above the bottom buttons; a finger drag moves it.
  await page.tap('#hud-wizard-cue');
  await page.tap('.dim-wizard-card-btn[data-dim="4D"]');
  await page.tap('[data-action="tool:pieceType:tesseract"]');
  await page.waitForSelector('#world4d-panel.visible', { timeout: 15000 });
  await page.waitForTimeout(800);
  const g = await page.evaluate(() => {
    const p = document.getElementById('world4d-panel');
    const tr = p.querySelector('.w4d-track').getBoundingClientRect();
    const lowest = Math.max(...[...p.children].filter((c) => c.offsetParent && !c.classList.contains('panel-min')).map((c) => c.getBoundingClientRect().bottom));
    const thumb = p.querySelector('.w4d-thumb').getBoundingClientRect();
    return { track: [tr.left, tr.width, tr.height, tr.top, tr.bottom], lowest, thumb: [thumb.left + thumb.width / 2, thumb.height], undoTop: document.getElementById('undo-btn').getBoundingClientRect().top, vw: innerWidth };
  });
  console.log(name, '4d', JSON.stringify(g));
  assert.ok(g.track[1] >= Math.min(600, g.vw - 60) && g.track[2] >= 48 && g.thumb[1] >= 40, `${name}: 4D slider long and tall`);
  assert.ok(g.track[4] >= g.lowest - 0.5, `${name}: 4D slider lowest in its panel`);
  assert.ok(g.track[4] <= g.undoTop, `${name}: 4D slider above the bottom buttons`);
  const thumbX = () => page.evaluate(() => { const r = document.querySelector('#world4d-panel .w4d-thumb').getBoundingClientRect(); return r.left + r.width / 2; });
  const x0 = await thumbX();
  const cdp4 = await page.context().newCDPSession(page);
  const ty = (g.track[3] + g.track[4]) / 2;
  await cdp4.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: ty }] });
  for (let i = 1; i <= 10; i++) await cdp4.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + i * 15, y: ty }] });
  await cdp4.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForTimeout(200);
  const x1 = await thumbX();
  console.log(name, '4d drag thumb', Math.round(x0), '->', Math.round(x1));
  assert.ok(Math.abs(x1 - x0) > 20, `${name}: a finger drag moves the 4D slider`);
  await page.screenshot({ path: `${SHOTS}/4d-${name}.png` });
  console.log(name, errors.length ? `ERRORS: ${errors.join(' | ')}` : 'no errors');
  assert.equal(errors.length, 0);
  await page.close();
}
await browser.close();
console.log('big-sliders OK');
