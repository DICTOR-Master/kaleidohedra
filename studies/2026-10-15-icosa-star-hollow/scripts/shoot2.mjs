import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['closed', 'cut', 'inner', 'apart']) {
  await p.goto(`http://localhost:8001/render2.html#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: `/tmp/heca-${s}.png` }); console.log(s);
}
await b.close();
