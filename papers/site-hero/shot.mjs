// screenshots of the prototype (and the live-copy original) at desktop and phone width
import { chromium } from 'playwright';
const b = await chromium.launch();
for (const [name, file] of [['proto', 'site/proto-index.html'], ['now', 'site/index.html']]) {
  for (const [tag, w, h] of [['desk', 1280, 1500], ['phone', 390, 1700]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: tag === 'phone' ? 2 : 1 });
    await p.goto('file://' + process.cwd() + '/' + file, { waitUntil: 'load' });
    await p.waitForTimeout(800);
    await p.screenshot({ path: `${name}-${tag}.png` });
    await p.close();
  }
}
await b.close(); console.log('shots ok');
