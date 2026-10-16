// node shoot_p4_slice.mjs -> /tmp/p4/slice-<set>.png and slice-<set>.json (label anchors) from render_p4.html?mode=slice
import { chromium } from 'playwright'; import fs from 'node:fs';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const s of ['ends', 'middle']) {
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto(`http://localhost:8001/interlock/render_p4.html?set=${s}&mode=slice&turns=3&px=1400`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/p4/slice-${s}.png` }); fs.writeFileSync(`/tmp/p4/slice-${s}.json`, JSON.stringify(await p.evaluate(() => ({ labels: window.__labels, rho: window.__rho }))));
  await p.close(); console.log(s);
}
await b.close();
