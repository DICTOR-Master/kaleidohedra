// <folder>/paper.html -> <folder>/<pdf> (A4), footer with the DICTO mark and the record's DOI. Run on dicto-node (needs playwright):
//   node papers/print.mjs <folder> <pdf name> "<short title>" <concept DOI> <version>
// PAGE_W/PAGE_H (e.g. 8.27in / 11.69in, the Amazon KDP A4 trim) override the A4 page size.
import { chromium } from 'playwright';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const [dir, pdf, title, doi, ver] = process.argv.slice(2);
if (!title || title === 'undefined') { console.error('GUARD: short title missing (arg 3): footer would read "undefined"'); process.exit(4); }
// BANNED-PHRASE GUARD (DICTO FIRM rules; built in 5 Nov 2026 so no PDF can carry them). Override only with ALLOW_BANNED=1.
import fs from 'node:fs';
{ const txt = fs.readFileSync(path.join(here, dir, 'paper.html'), 'utf8').replace(/<[^>]+>/g, ' ');
  const BAN = /in plain words|in plain terms|put simply|simply put|\bplainly\b|layman|\bin short\s*[:.]|DICTO asked|asked by DICTO|DICTO's question|flat-ended|やさしい日本語|平たく言えば|簡単に言えば|わかりやすく言えば/gi;
  const hits = [...txt.matchAll(BAN)].map(m => txt.slice(Math.max(0, m.index - 40), m.index + 50).replace(/\s+/g, ' '));
  const raw = fs.readFileSync(path.join(here, dir, 'paper.html'), 'utf8');
  if (/^DRAFT/i.test(path.basename(pdf)) && !/class="status/.test(raw) && !process.env.ALLOW_BANNED) { console.error('DRAFT without the red status box - not printed'); process.exit(3); }
  // NATIVE-REVIEW GUARD (11-07): a non-English book prints only as DRAFT-… until native-review.json says verdict ok.
  const lang = (raw.match(/<html[^>]*lang="([^"]+)"/) || [])[1] || 'en';
  if (!/^en/i.test(lang) && !/^DRAFT/i.test(path.basename(pdf))) { const f = path.join(here, dir, 'native-review.json');
    let ok = false; try { const j = JSON.parse(fs.readFileSync(f, 'utf8')); ok = j.verdict === 'ok' && !!j.reviewer; } catch (e) {}
    if (!ok) { console.error(`GUARD: lang ${lang} needs ${f} with a native reader's verdict ok - print it as DRAFT-… instead`); process.exit(5); } }
  if (hits.length && !process.env.ALLOW_BANNED) { console.error('BANNED PHRASE — not printed:\n  ' + hits.join('\n  ')); process.exit(2); } }
const b = await chromium.launch();
const page = await b.newPage();
await page.goto('file://' + path.join(here, dir, 'paper.html'), { waitUntil: 'load' });
await page.pdf({ path: path.join(here, dir, pdf), ...(process.env.PAGE_W ? { width: process.env.PAGE_W, height: process.env.PAGE_H } : { format: 'A4' }), printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: `<div style="font:8px sans-serif;width:100%;padding:0 15mm;display:flex;justify-content:space-between;color:#666"><span>${title} · DICTO · dictospheres.com${doi && doi !== 'draft' ? ' · DICTO DOI: ' + doi : ''}${ver ? ' · v' + ver : ''}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
await b.close();
console.log(dir + '/' + pdf + ' written');
