// <folder>/paper.html -> <folder>/<pdf> (A4), footer with the DICTO mark and the record's DOI. Run on dicto-node (needs playwright):
//   node papers/print.mjs <folder> <pdf name> "<short title>" <concept DOI> <version>
// PAGE_W/PAGE_H (e.g. 8.27in / 11.69in, the Amazon KDP A4 trim) override the A4 page size.
import { chromium } from 'playwright';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const [dir, pdf, title, doi, ver] = process.argv.slice(2);
const b = await chromium.launch();
const page = await b.newPage();
await page.goto('file://' + path.join(here, dir, 'paper.html'), { waitUntil: 'load' });
await page.pdf({ path: path.join(here, dir, pdf), ...(process.env.PAGE_W ? { width: process.env.PAGE_W, height: process.env.PAGE_H } : { format: 'A4' }), printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: `<div style="font:8px sans-serif;width:100%;padding:0 15mm;display:flex;justify-content:space-between;color:#666"><span>${title} · DICTO · dictospheres.com · DICTO DOI: ${doi} · v${ver}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
await b.close();
console.log(dir + '/' + pdf + ' written');
