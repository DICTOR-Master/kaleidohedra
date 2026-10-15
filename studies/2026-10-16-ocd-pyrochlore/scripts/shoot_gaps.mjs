import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['closed', 'cut', 'apart']) { await p.goto(`http://localhost:8001/ocdnet/render_gaps.html#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 }); await p.screenshot({ path: `/tmp/ocdgap-${s}.png` }); }
console.log('done'); await b.close();
