import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const [n, u] of [['one-tilt', '?net=1&tilt=1'], ['double-tilt', '?tilt=1'], ['double-cut', '#cut'], ['one-cut', '?net=1#cut']]) {
  await p.goto(`http://localhost:8001/ocdnet/render_network.html${u}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 }); await p.screenshot({ path: `/tmp/ocdnet-${n}.png` });
}
console.log('done'); await b.close();
