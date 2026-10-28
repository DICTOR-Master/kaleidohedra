// Opens every door of the one-site build through its own host name (mapped to the local test server) in Chromium:
// checks the page title, data-site, console errors and failed requests, the pretty paths and door files, and saves screenshots.
import { chromium } from 'playwright';
const PORT = +(process.argv[2] || 8090);
const HOSTS = ['dictospheres.com', 'www.dictospheres.com', 'kaleidohedra.dictospheres.com', 'rhombiverse.dictospheres.com', 'polyhedraverse.dictospheres.com'];
const b = await chromium.launch({ args: [`--host-resolver-rules=${HOSTS.map((h) => `MAP ${h} 127.0.0.1:${PORT}`).join(',')}`] });
let bad = 0;
for (const h of HOSTS) {
  const page = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = [], fails = [];
  page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)); });
  page.on('response', (r) => { if (r.status() >= 400 && new URL(r.url()).hostname === h) fails.push(r.status() + ' ' + new URL(r.url()).pathname); });
  await page.goto(`http://${h}/`, { waitUntil: 'load', timeout: 60000 }); await page.waitForTimeout(6000);
  const title = await page.title(), site = await page.evaluate(() => document.documentElement.dataset.site || '-');
  const extra = [];
  for (const p of h.includes('.dictospheres.com') ? ['/guide', '/terms', '/robots.txt', '/sitemap.xml'] : ['/robots.txt', '/sitemap.xml', '/favicon.png']) {
    const r = await page.request.get(`http://${h}${p}`); const t = await r.text();
    extra.push(`${p} ${r.status()} ${r.headers()['x-served']}${p === '/robots.txt' ? ' [' + (t.match(/Sitemap: (\S+)/) || [])[1] + ']' : ''}`);
  }
  await page.screenshot({ path: `onesite-${h}.png` });
  const ok = !fails.length;
  bad += !ok;
  console.log(`${ok ? 'OK ' : 'BAD'} ${h}: title "${title}", data-site ${site}; console errors ${errs.length}${errs.length ? ' ' + JSON.stringify(errs.slice(0, 3)) : ''}; failed ${JSON.stringify(fails.slice(0, 5))}\n     ${extra.join(' | ')}`);
  await page.close();
}
await b.close(); process.exit(bad ? 1 : 0);
