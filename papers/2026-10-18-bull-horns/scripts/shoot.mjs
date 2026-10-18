// DICTO 2026-10-18 paper figures: screenshots of the study 3D pages (dicto-node, Playwright). usage: node shoot.mjs <root> <out>
import { chromium } from 'playwright';
import fs from 'node:fs';
const [ROOT, OUT] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const S = (p) => `${ROOT}/studies/${p}`;
const jobs = [
  ['p1', S('2026-10-18-p1-golden-key-octet/renders/p1-golden-key-octet.html'), null],
  ['p2', S('2026-10-18-p2-penrose-core-octet/renders/p2-penrose-core-octet.html'), null],
  ['p3', S('2026-10-18-p3-golden-envelope-octet/renders/p3-golden-envelope-octet.html'), ['3 · Two-shape set']],
  ['p4', S('2026-10-18-p4-golden-octet-adaptor/renders/p4-golden-octet-adaptor.html'), null],
  ['keyedW', S('2026-10-18-p4-golden-octet-adaptor/renders/p4-keyed-W.html'), null],
  ['holes', S('2026-10-18-bcc-hole-pieces/renders/bcc-hole-pieces.html'), null],
  ['octet', S('2026-10-18-ocd-octet/renders/step10-pieces.html'), ['Assembly round one OCD', 'Keyless kit, 3 Penrose cores (DICTO\'s choice)', 'Network: OCDs and tetrahedra']],
];
const flat = [['penrose-cut', S('2026-10-18-ocd-octet/renders/step13-penrose.html')], ['stars', S('2026-10-18-ocd-octet/renders/step4-stars.html')],
  ['slab-section', S('2026-10-18-slab-cover/renders/slab-section.html')], ['bcc-stars', S('2026-10-18-bcc-golden-kit/renders/step4-stars.html')]];
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 1.5 });
const wrap = (f) => 'data:text/html;base64,' + Buffer.from('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">' + fs.readFileSync(f, 'utf8')).toString('base64');
for (const [name, f, only] of jobs) {
  await page.goto(wrap(f)); await page.waitForTimeout(3500);
  const spin = page.locator('#spin'); if (await spin.count() && (await spin.getAttribute('aria-pressed')) === 'true') await spin.click();
  const btns = page.locator('#btns button'); const n = await btns.count();
  for (let i = 0; i < n; i++) {
    const label = (await btns.nth(i).textContent()).trim();
    if (only && !only.includes(label)) continue;
    await btns.nth(i).click(); await page.waitForTimeout(2500);
    const file = `${OUT}/${name}-${String(i).padStart(2, '0')}.png`;
    await page.locator('#stage').screenshot({ path: file }); console.log(file, '|', label);
  }
}
for (const [name, f] of flat) { await page.goto(wrap(f)); await page.waitForTimeout(1500); await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true }); console.log(name); }
await b.close();
