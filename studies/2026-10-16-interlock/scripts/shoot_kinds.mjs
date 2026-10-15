// Interlock kind gallery tiles (render_kinds.html on localhost:8001): ends 0..11, middle 0..10 -> /tmp/kind-<setting>-<k>.png
import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 700, height: 700 } });
for (const [s, n] of [['ends', 12], ['middle', 11]]) for (let k = 0; k < n; k++) {
  await p.goto(`http://localhost:8001/render_kinds.html?f=interlock-kinds-render-${s}.json&k=${k}`); await p.reload();
  await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 }); await p.screenshot({ path: `/tmp/kind-${s}-${k}.png` });
}
await b.close(); console.log('done');
