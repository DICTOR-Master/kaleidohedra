import { chromium } from 'playwright';
const b = await chromium.launch();
for (const [tag, w] of [['desk', 1280], ['phone', 390]]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 } });
  await p.goto('file://' + process.cwd() + '/site/index.html', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => { const h = document.getElementById('books'); h.scrollIntoView(); window.scrollBy(0, -20);
    const n = document.querySelector('.disc-note').getBoundingClientRect(); const bk = [...document.querySelectorAll('.book')].map(e => e.getBoundingClientRect().top);
    return { noteBottom: Math.round(n.bottom), firstBookTop: Math.round(Math.min(...bk)) }; });
  console.log(tag, JSON.stringify(r));
  await p.waitForTimeout(400); await p.screenshot({ path: `books-${tag}.png` }); await p.close();
}
await b.close();
