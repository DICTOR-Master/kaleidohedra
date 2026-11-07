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
  const lang = (raw.match(/<html[^>]*lang="([^"]+)"/) || [])[1] || 'en';   // (native-review requirement dropped 11-07: DICTO's reader already checked; accuracy is guarded by the ja text guard)
  // KATAKANA-COVER GUARD (DICTO 11-07: "any japanese language version gets a katakana cover"): a final ja book needs its own cover
  // image (file name with -ja) whose alt text carries the katakana title.
  if (!/^en/i.test(lang) && !/^DRAFT/i.test(path.basename(pdf))) { const cv = raw.match(/class="page coverpage"[\s\S]*?<img[^>]*>/);
    const img = cv ? cv[0].match(/<img[^>]*>/)[0] : '';
    if (!new RegExp('src="[^"]*-' + lang.slice(0, 2) + '[^"]*"').test(img) || !/alt="[^"]*[\u0600-\u06FF\u3040-\u30FF\u4E00-\u9FFF]{3,}/.test(img)) { console.error(`GUARD: ${lang} edition without its own-script title cover (cover img src must contain -${lang.slice(0, 2)} and alt the title in its script)`); process.exit(6); } }
  // JA TEXT GUARD (11-07, reader: "reads like machine translation"): a final ja book may not carry leftover English words outside
  // （…） glosses, nor the known bad variants found in Quanta-ja v1.
  if (!/^en/i.test(lang) && !/^DRAFT/i.test(path.basename(pdf))) {
    const body = raw.replace(/<style[\s\S]*?<\/style>/g, '').replace(/<(sub|sup|code|a|i|em)\b[^>]*>[\s\S]*?<\/\1>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/（[^（）]*）|\([^()]*\)|「[ -~]*」/g, ' ');
    const latin = [...new Set((body.match(/(?<![\p{L}\w.\-@\/_])[a-z]{4,}(?![\p{L}\w.\-@\/_(])/gu) || []).filter(w => !/^(zenodo|https?|www|dictospheres|com|org|arccos|arcsin|arctan|netlib|diag|[hc]+)$/.test(w)))];
    const BADJA = /白い女王|フル章|アリシアの不思議の国|いぶし十二面体|ポアン(?!ソ)|正の四次元|四次元の正多面体/g;
    const bad = [...new Set(body.match(BADJA) || [])];
    if ((latin.length || bad.length) && !process.env.ALLOW_BANNED) { console.error(`GUARD (${lang} text): leftover English ` + '' + latin.slice(0, 30).join(', ') + (bad.length ? '; bad variants ' + bad.join(', ') : '')); process.exit(7); } }
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
