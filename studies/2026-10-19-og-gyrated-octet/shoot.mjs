// DICTO 2026-10-20: screenshots of every view of renders/gyrated-octet.html (dicto-node, Playwright). usage: node shoot.mjs <html> <outdir>
import { chromium } from 'playwright';
import fs from 'node:fs';
const [F, OUT] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1000, height: 1000 }, deviceScaleFactor: 1.5 });
await page.goto('file://' + F); await page.waitForTimeout(3000);
await page.evaluate(() => { ctl.autoRotate = false; const e = document.getElementById('ex'); e.value = 0; e.dispatchEvent(new Event('input')); });
const btns = page.locator('#btns button'); const n = await btns.count();
for (let i = 0; i < n; i++) {
  const label = (await btns.nth(i).textContent()).trim(); await btns.nth(i).click(); await page.evaluate(() => { const e = document.getElementById('ex'); e.value = 0; explode(); }); await page.waitForTimeout(2000);
  const file = `${OUT}/${String(i).padStart(2, '0')}.png`; await page.locator('#stage').screenshot({ path: file }); console.log(file, '|', label);
}
await b.close();
