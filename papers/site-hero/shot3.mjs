import { chromium } from 'playwright';
const b = await chromium.launch();
for (const [name, file] of [['v-home', 'site/index.html'], ['v-start', 'site/start-here/index.html']]) {
  const p = await b.newPage({ viewport: { width: 390, height: 1600 } });
  await p.goto('file://' + process.cwd() + '/' + file, { waitUntil: 'load' }); await p.waitForTimeout(2500);
  if (name === 'v-home') console.log('video', await p.evaluate(() => { const v = document.querySelector('.hero-video video'); return v ? [v.readyState, v.videoWidth, v.paused, v.error && v.error.code] : 'none'; }));
  await p.screenshot({ path: name + '.png' }); await p.close();
}
await b.close();
