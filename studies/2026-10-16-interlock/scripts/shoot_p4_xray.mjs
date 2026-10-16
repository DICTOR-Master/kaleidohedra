// node shoot_p4_xray.mjs -> /tmp/p4/xray-<set>.png (render_p4_xray.html served from ~/cleo-hold/interlock on :8001)
import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const s of ['ends', 'middle']) {
  const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  await p.goto(`http://localhost:8001/interlock/render_p4_xray.html?set=${s}&px=1200`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/p4/xray-${s}.png` }); await p.close(); console.log(s);
}
await b.close();
