import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['stations-closed', 'stations-cut', 'stations-inner', 'stations-apart', 'stations-cut5', 'c102-closed', 'c102-cut', 'c102-inner', 'c102-apart', 'c102-cut3']) {
  await p.goto(`http://localhost:8001/render4.html#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: `/tmp/fig-${s}.png` }); console.log(s);
}
await b.close();
