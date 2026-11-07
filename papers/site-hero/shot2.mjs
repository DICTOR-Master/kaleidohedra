import { chromium } from 'playwright';
const b = await chromium.launch();
for (const [name, file, y] of [['live-home', 'site/index.html', 0], ['live-cards', 'site/index.html', -1], ['live-start', 'site/start-here/index.html', 0]]) {
  for (const [tag, w, h] of [['desk', 1280, 1400], ['phone', 390, 1500]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + process.cwd() + '/' + file, { waitUntil: 'load' }); await p.waitForTimeout(600);
    if (y < 0) await p.evaluate(() => { const e = [...document.querySelectorAll('.paper .num')].find(n => n.textContent.trim() === '#22'); e.closest('.paper').scrollIntoView(); });
    await p.screenshot({ path: `${name}-${tag}.png` }); await p.close();
  }
}
const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.goto('file://' + process.cwd() + '/site/index.html', { waitUntil: 'load' }); await p.waitForTimeout(800);
console.log('js errors:', errs.filter(e => !/net::|Failed to load resource/.test(e)).length, errs.slice(0, 3));
await b.close();
