import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
const out = '/tmp/forkframes'; mkdirSync(out, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
await p.goto('http://localhost:8001/ocdnet/render_fork_movie.html'); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 });
for (let i = 0; i < 360; i++) { await p.evaluate((i) => window.draw(i), i); await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png` }); }
console.log('frames done'); await b.close();
