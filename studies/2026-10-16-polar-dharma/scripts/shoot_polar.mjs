import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
const T = process.argv[2] ? '?' + process.argv[2] : '', X = T ? '-' + process.argv[2] : '';
for (const s of (process.argv[3] ? process.argv[3].split(',') : ['closed', 'cut', 'inner', 'apart'])) {
  await p.goto(`http://localhost:8001/render_polar.html${T}#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: `/tmp/polar${X}-${s}.png` }); console.log(s);
}
await b.close();
