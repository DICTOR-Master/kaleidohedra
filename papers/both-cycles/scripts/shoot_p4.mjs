// Shoots render_p4.html on dicto-node (served from ~/cleo-hold on :8001, files under interlock/): node shoot_p4.mjs <job> -> /tmp/p4/*.png
//   job hero: 3 bearings x 2 settings; job set <view>: the peel layers, kit pieces and locators for the chosen bearing
import { chromium } from 'playwright'; import fs from 'node:fs';
const [job, view = 'A'] = process.argv.slice(2); fs.mkdirSync('/tmp/p4', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
async function shot(qs, name, px = 1200) {
  const p = await b.newPage({ viewport: { width: px, height: px } });
  await p.goto(`http://localhost:8001/interlock/render_p4.html?${qs}&px=${px}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/p4/${name}.png` }); await p.close(); console.log(name);
}
const KN = { ends: 12, middle: 11 };
if (job === 'hero') for (const v of ['A', 'B', 'C']) for (const s of ['ends', 'middle']) await shot(`set=${s}&view=${v}&mode=hero&turns=1`, `hero-${s}-${v}`);
if (job === 'kinds') for (const s of ['ends', 'middle']) for (let k = 1; k <= KN[s]; k++) await shot(`set=${s}&view=${view}&mode=kind&k=${k}&h=2.0`, `kind-${s}-${k}`, 700);
if (job === 'set') for (const s of ['ends', 'middle']) {
  await shot(`set=${s}&view=${view}&mode=hero&turns=1`, `hero-${s}-${view}`);
  for (let l = 0; l < 6; l++) await shot(`set=${s}&view=${view}&mode=layer&layer=${l}`, `layer-${s}-${l}`, 700);
  for (let k = 1; k <= KN[s]; k++) { await shot(`set=${s}&view=${view}&mode=kind&k=${k}&h=2.0`, `kind-${s}-${k}`, 700); await shot(`set=${s}&view=${view}&mode=loc&k=${k}`, `loc-${s}-${k}`, 500); }
}
await b.close(); console.log('done');
