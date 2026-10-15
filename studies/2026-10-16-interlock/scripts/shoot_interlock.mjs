import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 900, height: 900 } });
for (const h of [2.65, 1.0]) for (const a of ['5', '3', '2']) for (const c of ['orig', 'flip']) {
  await p.goto(`http://localhost:8001/interlock/render_interlock.html?axis=${a}&col=${c}&h=${h}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 });
  await p.screenshot({ path: `/tmp/il-${h === 1 ? 'centre' : 'whole'}-${a}-${c}.png` });
}
console.log('done'); await b.close();
