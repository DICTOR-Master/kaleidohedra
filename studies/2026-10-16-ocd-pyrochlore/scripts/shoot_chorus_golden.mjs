import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['top', 'tilt', 'apart']) { await p.goto(`http://localhost:8001/ocdnet/render_chorus_golden.html${process.argv[2] ? '?exact' : ''}#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 }); await p.screenshot({ path: `/tmp/chorus-golden${process.argv[2] ? '-exact' : ''}-${s}.png` }); }
console.log('done'); await b.close();
