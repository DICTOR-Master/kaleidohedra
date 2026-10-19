// Shoot the Universal PiTet paper figures (run on dicto-node with the folder served on :8020): node shoot_figs.mjs <out dir>
import { chromium } from 'playwright';
const OUT = process.argv[2];
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const f of ['shells', 'cycle', 'vajras', 'hexcleo']) {
  await page.goto(`http://localhost:8020/figs.html?fig=${f}`); await page.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await page.waitForTimeout(500); await page.screenshot({ path: `${OUT}/${f}.png` }); console.log(f);
}
await b.close();
