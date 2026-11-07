// figcheck: every figure/image/table/svg must sit inside the page's text column (DICTO standing rule 2026-11-03).
// Usage (cw-print dir): node figcheck.mjs <folder>   -> prints OK or each offender; exit 1 on any offender.
import { chromium } from 'playwright';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const dir = process.argv[2];
const b = await chromium.launch(); const page = await b.newPage();
await page.emulateMedia({ media: 'print' });
await page.setViewportSize({ width: 794 - 2 * 64, height: 1123 }); // A4 at 96 dpi minus ~17 mm side margins
await page.goto('file://' + path.join(here, dir, 'paper.html'), { waitUntil: 'networkidle' });
const r = await page.evaluate(() => {
  const W = document.documentElement.clientWidth, out = [];
  const sw = document.documentElement.scrollWidth;
  if (sw > W + 1) out.push(`page wider than column: ${sw}px > ${W}px (Chromium would shrink the whole PDF)`);
  for (const el of document.querySelectorAll('img, svg, table, figure, pre, canvas')) {
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
    const q = el.getBoundingClientRect();
    if (q.width === 0) continue;
    if (q.left < -1 || q.right > W + 1) out.push(`${el.tagName.toLowerCase()} ${(el.getAttribute('src') || el.id || el.className || '').toString().slice(0, 60)}: ${Math.round(q.left)}..${Math.round(q.right)} of ${W}`);
    if (el.tagName === 'IMG' && !el.complete) out.push(`img not loaded: ${el.getAttribute('src')}`);
    if (el.tagName === 'IMG' && el.naturalWidth === 0) out.push(`img broken: ${el.getAttribute('src')}`);
  }
  // 11-07 (HexOct v9 draft): a fixed-height cover/title page whose contents are taller than it pushes its top (the logo) above the page
  for (const el of document.querySelectorAll('.titlepage, .coverpage')) {
    if (el.scrollHeight > el.clientHeight + 2) out.push(`${el.className} overflows its own height: ${el.scrollHeight}px of ${el.clientHeight}px (use min-height and top alignment)`);
  }
  return out;
});
await b.close();
if (r.length) { console.log('FIGCHECK FAIL ' + dir); r.forEach(x => console.log('  ' + x)); process.exit(1); }
console.log('FIGCHECK OK ' + dir);
