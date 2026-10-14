import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['closed', 'cut', 'bare', 'apart']) {
  await p.goto(`http://localhost:8001/render.html#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 30000 });
  await p.screenshot({ path: `/tmp/cleo-hold-${s}.png` }); console.log(s);
}
await b.close();
