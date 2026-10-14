// X-ray check of the hollow DICTO-ICOSA star (DICTO 2026-10-15): cut through the centre along the 5-, 3- and 2-fold axes, both sides.
import { chromium } from 'playwright';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1000, height: 1000 } });
const errors = []; page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:8000/index.html?site=kaleidohedra&open=dodeca:icosaStar'); await page.waitForTimeout(3500);
for (let i = 0; i < 3 && await page.locator('#welcome-overlay:visible').count(); i++) { await page.keyboard.press('Enter'); await page.waitForTimeout(800); }
if (await page.locator('.dim-wizard-overlay.open').count()) { await page.keyboard.press('Escape'); await page.waitForTimeout(800); }
await page.evaluate(() => { const w = document.getElementById('welcome-overlay'); if (w) w.style.display = 'none'; });
await page.locator('select.hull-select[data-select="part"]:visible').first().selectOption('hollow'); await page.waitForTimeout(1200);
await page.evaluate(() => { const i = [...document.querySelectorAll('.ch-apart-row input')].find((x) => x.offsetParent); i.value = '0'; i.dispatchEvent(new Event('input')); });
await page.click('#xray-toggle'); await page.waitForTimeout(800);
const set = async (axis, flip) => {
  await page.click('#lab-toggle'); await page.waitForTimeout(300);
  await page.selectOption('#section-axis', axis); await page.evaluate(() => { const p = document.getElementById('section-pos'); p.value = '0'; p.dispatchEvent(new Event('input')); });
  const f = page.locator('#section-flip'); if ((await f.isChecked()) !== flip) await f.click({ force: true });
  await page.click('#lab-close'); await page.waitForTimeout(700);
  // look straight at the cut face: camera on the axis, on the removed side
  await page.evaluate(([axis, flip]) => { const n = window.__xrayNormal?.(); }, [axis, flip]);
};
for (const [axis, flip] of [['i5', false], ['i5', true], ['i3', false], ['i2', false]]) {
  await set(axis, flip);
  await page.evaluate(() => document.querySelectorAll('[id$="-panel"], .w4d-panel').forEach((p) => { p.style.visibility = 'hidden'; }));
  await page.screenshot({ path: `/tmp/xray-${axis}${flip ? '-flip' : ''}.png` });
  await page.evaluate(() => document.querySelectorAll('[id$="-panel"], .w4d-panel').forEach((p) => { p.style.visibility = ''; }));
}
console.log('frame', await page.evaluate(() => document.getElementById('section-axis').dataset.icoFrame), 'errors', errors.length);
await b.close();
