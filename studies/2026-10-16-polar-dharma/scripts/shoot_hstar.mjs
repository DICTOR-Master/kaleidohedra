import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['three', 'five', 'oblique']) {
  await p.goto(`http://localhost:8001/render_hstar.html#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: `/tmp/hstar-${s}.png` }); console.log(s);
}
await b.close();
