import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/adapter', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const [n, qs] of [['alone-a', 'mode=alone&az=20'], ['alone-b', 'mode=alone&az=140'], ['alone-c', 'mode=alone&az=260'], ['cell', 'mode=cell']]) {
  const p = await b.newPage({ viewport: { width: 1100, height: 1100 } });
  await p.goto(`http://localhost:8001/adapter/render_adapter.html?${qs}&px=1100`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 });
  await p.screenshot({ path: `/tmp/adapter/${n}.png` }); await p.close(); console.log(n); }
await b.close();
