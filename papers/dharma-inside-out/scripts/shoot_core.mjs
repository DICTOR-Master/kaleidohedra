// The seamless infinite core: orthographic cut views, each phi^3 narrower (same centre), for turns_nested.py.
import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const phi3 = 4.236067977499790, H = 2.3;
for (const [k, px] of [[0, 3000], [1, 1200], [2, 1200], [3, 1200]]) {
  const p = await b.newPage({ viewport: { width: px, height: px } });
  await p.goto(`http://localhost:8001/render_polar.html?turns${k ? '&notag' : ''}&px=${px}&ortho=${H / phi3 ** k}#cut`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 });
  await p.screenshot({ path: `/tmp/core-${k}.png` }); console.log(k); await p.close();
}
await b.close();
