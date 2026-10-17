// node shoot_two.mjs -> /tmp/two/*.png (served from ~/cleo-hold on :8001, files in scutoids/)
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/two', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const [name, qs] of [['layers1', 'mode=cutaway&upto=1'], ['layers2', 'mode=cutaway&upto=2'], ['whole', 'mode=cutaway&upto=3'], ['pieces', 'mode=pieces'], ['alt', 'mode=alt']].filter(([n]) => !process.argv[2] || n === process.argv[2])) {
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto(`http://localhost:8001/scutoids/render_two.html?${qs}&px=1400`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/two/${name}.png` }); await p.close(); console.log(name); }
await b.close();
