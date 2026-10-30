// The Queens lens (DICTO 2026-10-30): open the White Queen's Shadow view, tap Lens (through the UI), check the round lens shows on
// desktop and phone with no page errors; screenshots to /tmp/queens-lens-*.png.
import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const errs = [];
for (const [tag, vp, mobile] of [['desktop', { width: 1280, height: 800 }, false], ['phone', { width: 390, height: 844 }, true]]) {
  const p = await b.newPage({ viewport: vp, hasTouch: mobile, isMobile: mobile, deviceScaleFactor: mobile ? 2 : 1 });
  p.on('pageerror', (e) => errs.push(tag + ' ' + e.message)); p.on('console', (m) => { if (m.type() === 'error') errs.push(tag + ' ' + m.text().slice(0, 160)); });
  await p.goto('' + (process.env.BASE || 'http://localhost:8000') + '/index.html?site=kaleidohedra&open=whitequeen:vertex');
  await p.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }).then(() => p.keyboard.press('Enter')).catch(() => {});
  await p.waitForTimeout(4000);
  await p.locator('[data-wq-lens]').click();
  await p.waitForTimeout(2500);
  await p.screenshot({ path: `/tmp/queens-lens-${tag}.png` });
  const box = await p.locator('.wq-lens').boundingBox();
  console.log(tag, 'lens', JSON.stringify(box), 'visible', await p.locator('.wq-lens').isVisible());
  if (!(await p.locator('.wq-lens').isVisible())) { errs.push(tag + ' lens not shown'); }
  await p.close();
}
console.log('errors', errs.length, errs.slice(0, 5).join(' | ')); if (errs.length) process.exitCode = 1;
await b.close();
