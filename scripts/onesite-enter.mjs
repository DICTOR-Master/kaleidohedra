// One site, four doors: enter each app door (click ENTER) through its own host and report console errors and the canvas.
import { chromium } from 'playwright';
const PORT = +(process.argv[2] || 8090);
const HOSTS = ['kaleidohedra.dictospheres.com', 'rhombiverse.dictospheres.com', 'polyhedraverse.dictospheres.com'];
const b = await chromium.launch({ args: [`--host-resolver-rules=${HOSTS.map((h) => `MAP ${h} 127.0.0.1:${PORT}`).join(',')}`, '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const h of HOSTS) {
  const page = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = [];
  page.on('console', (m) => { if (m.type() === 'error' && !/insights/.test(m.text())) errs.push(m.text().slice(0, 140)); });
  page.on('pageerror', (e) => errs.push('pageerror ' + e.message.slice(0, 140)));
  page.on('response', (r) => { if (r.status() >= 400 && !/insights/.test(r.url())) errs.push(r.status() + ' ' + r.url()); });
  await page.goto(`http://${h}/`, { waitUntil: 'load' }); await page.waitForTimeout(3000);
  await page.getByText('ENTER', { exact: true }).first().click(); await page.waitForTimeout(12000);
  const canvases = await page.evaluate(() => [...document.querySelectorAll('canvas')].filter((c) => c.width > 300).length);
  await page.screenshot({ path: `onesite-enter-${h}.png` });
  console.log(`${errs.length ? 'BAD' : 'OK '} ${h}: canvases ${canvases}; errors ${JSON.stringify(errs.slice(0, 4))}`); await page.close();
}
await b.close();
