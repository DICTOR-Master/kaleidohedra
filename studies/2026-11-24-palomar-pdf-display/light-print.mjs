// LIGHT print test (study 2026-11-24, Palomar/Zenodo PDF display): the same page.pdf call as papers/print.mjs,
// but every figure above 1.5 x DPI (default 300, so above 450 ppi) is first resampled in the page to DPI at its printed size;
// milder resampling is skipped: smoothing makes flat-colour renders compress worse (a 0.9 threshold left #103 at 7.37 MB). PNG stays PNG.
//   node light-print.mjs <folder>/paper.html <out.pdf> "<footer title>" [DPI]
// Proposed for print.mjs as LIGHT=1 (or default), placed just before page.pdf.
import { chromium } from 'playwright';
import path from 'node:path';
const [html, out, title, dpiArg] = process.argv.slice(2);
const DPI = Number(dpiArg || 300);
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });   // file:// figures may be read back from a canvas
// 180 mm text column (A4 minus 15 mm margins) = 680 CSS px at 96 px/in: lay the page out at the printed width
const page = await b.newPage({ viewport: { width: 680, height: 1000 } });
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.resolve(html), { waitUntil: 'load' });
const log = await page.evaluate(async (DPI) => {
  const rows = [];
  for (const img of [...document.images]) {
    await img.decode().catch(() => {});
    const r = img.getBoundingClientRect();
    if (!r.width || !img.naturalWidth) continue;
    const tw = Math.ceil(r.width * DPI / 96), th = Math.round(tw * img.naturalHeight / img.naturalWidth);
    if (tw >= img.naturalWidth * 0.66) { rows.push([img.src.split('/').pop(), img.naturalWidth, img.naturalHeight, 'kept']); continue; }
    const c = document.createElement('canvas'); c.width = tw; c.height = th;
    const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    g.drawImage(img, 0, 0, tw, th);
    const isJpeg = /\.jpe?g$/i.test(img.src);
    img.src = c.toDataURL(isJpeg ? 'image/jpeg' : 'image/png', 0.92);
    await img.decode().catch(() => {});
    rows.push([img.src.slice(0, 0) + (img.alt || '').slice(0, 30), img.naturalWidth, img.naturalHeight, `${tw}x${th}`]);
  }
  return rows;
}, DPI);
console.log(JSON.stringify(log));
await page.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: `<div style="font:8px sans-serif;width:100%;padding:0 15mm;display:flex;justify-content:space-between;color:#666"><span>${title} · DICTO · dictospheres.com</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
await b.close();
console.log(out + ' written');
