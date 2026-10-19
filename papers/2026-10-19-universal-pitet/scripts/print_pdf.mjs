// Print paper.html to PDF (A4) with the DICTO footer. Run on dicto-node: node print_pdf.mjs <paper.html> <out.pdf>
import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
const [src, out] = process.argv.slice(2);
const b = await chromium.launch(); const page = await b.newPage();
await page.goto(pathToFileURL(src).href, { waitUntil: 'networkidle' });
await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
  footerTemplate: '<div style="font: 8px system-ui; color: #888; width: 100%; text-align: center;">DICTO · Universal PiTet · DICTO DOI 10.5281/zenodo.23463305 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
await b.close();
