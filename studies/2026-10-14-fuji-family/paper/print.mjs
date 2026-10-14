// paper.html -> paper.pdf (A4, as laid out by build_pdf.py's print CSS). Run on dicto-node: node print.mjs (needs playwright).
import { chromium } from 'playwright';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch();
const page = await b.newPage();
await page.goto('file://' + path.join(here, process.argv[2] ?? 'paper.html'), { waitUntil: 'load' });
await page.pdf({ path: path.join(here, process.argv[3] ?? 'paper.pdf'), format: 'A4', printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: '<div style="font:8px sans-serif;width:100%;padding:0 15mm;display:flex;justify-content:space-between;color:#666"><span>The FUJI Family · DICTO · dictospheres.com · DICTO DOI: 10.5281/zenodo.23357897</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
await b.close();
console.log('paper.pdf written');
