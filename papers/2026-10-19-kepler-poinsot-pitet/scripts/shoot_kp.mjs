// Shoot the Kepler–Poinsot–PiTet figures (dicto-node, folder served on :8020): node shoot_kp.mjs <out dir>
import { chromium } from 'playwright';
const OUT = process.argv[2];
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const f of ['cycles', 'turn', 'great', 'small']) {
  await page.goto(`http://localhost:8020/kpfigs.html?fig=${f}`); await page.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await page.waitForTimeout(500); await page.screenshot({ path: `${OUT}/kp-${f}.png` }); console.log(f);
}
await b.close();
