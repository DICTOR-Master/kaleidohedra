// figcheck: every figure/image/table/svg must sit inside the page's text column (DICTO standing rule 2026-11-03).
// Usage (cw-print dir): node figcheck.mjs <folder>   -> prints OK or each offender; exit 1 on any offender.
// Needs edgecheck.py + edgecheck-allow.txt beside it (book-* folders; copy them with figcheck.mjs to the print host).
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
const srcs = await page.evaluate(() => [...new Set([...document.querySelectorAll('img')].map(i => i.getAttribute('src')).filter(s => s && !/^(data|https?):/.test(s)))]);
await b.close();
// 15 Nov (DICTO: "fig 6.7 too big for fig frame again"): every book build also checks that no model runs off its image frame
// (edgecheck.py; deliberate close-ups go in edgecheck-allow.txt with a reason). A missing edgecheck.py stops the build too.
if (path.basename(path.resolve(here, dir)).startsWith('book-') && srcs.length) {
  const { spawnSync } = await import('node:child_process');
  const ec = spawnSync('python3', [path.join(here, 'edgecheck.py'), ...srcs.map(s => path.join(here, dir, decodeURIComponent(s)))], { encoding: 'utf8' });
  if (ec.status !== 0) r.push(...(((ec.stdout || '') + (ec.stderr || '')).trim().split('\n').filter(Boolean)), ...(ec.status === null || ec.error ? ['edgecheck.py could not run: ' + (ec.error || '')] : []));
}
if (r.length) { console.log('FIGCHECK FAIL ' + dir); r.forEach(x => console.log('  ' + x)); process.exit(1); }
console.log('FIGCHECK OK ' + dir);
