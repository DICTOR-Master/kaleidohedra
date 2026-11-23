// <folder>/paper.html -> <folder>/<pdf> (A4), footer with the DICTO mark and the record's DOI. Run on compute-host-2 (needs playwright):
//   node papers/print.mjs <folder> <pdf name> "<short title>" <concept DOI> <version>
// PAGE_W/PAGE_H (e.g. 8.27in / 11.69in, the Amazon KDP A4 trim) override the A4 page size.
// After any change here: run papers/guard_regress.sh on compute-host (every translated book must still print).
// LIGHT PRINT (default since 24 Nov 2026, study 2026-11-24-palomar-pdf-display: Zenodo's pdf.js preview loads the whole file and
// 6000-px figures failed to display): every figure above 450 ppi at its printed size is resampled to 300 ppi, lossless (PNG stays PNG;
// JPEG stays JPEG at q 0.92); the layout is unchanged (an unsized figure keeps its old width as a width attribute). FULL_RES=1 prints figures as they are; LIGHT_DPI=200 resamples to 200 ppi (above 300 ppi).
// SIZE GUARD: warns above 4 MB or for a figure above 4 Mpx; a figure above 16.7 Mpx (the iPad/iPhone canvas cap, 4096 x 4096) stops the print.
import { chromium } from 'playwright';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const [dir, pdf, title, doi, ver] = process.argv.slice(2);
if (!title || title === 'undefined') { console.error('GUARD: short title missing (arg 3): footer would read "undefined"'); process.exit(4); }
// BANNED-PHRASE GUARD (DICTO FIRM rules; 10 Nov 2026 adds MACHINE DETAILS: our machine names, home paths, local model names never appear in a paper; built in 5 Nov 2026 so no PDF can carry them). Override only with ALLOW_BANNED=1.
import fs from 'node:fs';
{ const txt = fs.readFileSync(path.join(here, dir, 'paper.html'), 'utf8').replace(/<[^>]+>/g, ' ');
  const BAN = /in plain words|in plain terms|put simply|simply put|\bplainly\b|layman|\bin short\s*[:.]|DICTO asked|asked by DICTO|DICTO's question|flat-ended|big.brother|dicto-node|dicto-big|~\/geom|~\/study-runs|~\/kaleidohedra|\/home\/dicto|\.local\b|Qwen|gpt-oss|やさしい日本語|平たく言えば|簡単に言えば|わかりやすく言えば/gi;
  const hits = [...txt.matchAll(BAN)].map(m => txt.slice(Math.max(0, m.index - 40), m.index + 50).replace(/\s+/g, ' '));
  const raw = fs.readFileSync(path.join(here, dir, 'paper.html'), 'utf8');
  if (/^DRAFT/i.test(path.basename(pdf)) && !/class="status/.test(raw) && !process.env.ALLOW_BANNED) { console.error('DRAFT without the red status box - not printed'); process.exit(3); }
  // 15 Nov RED-BOX RULE (DICTO FIRM: ALL temporary draft text inside the red status box; broken twice): in a DRAFT, draft wording outside a class="status" box stops the print.
  if (/^DRAFT/i.test(path.basename(pdf)) && !process.env.ALLOW_BANNED) { const outside = raw.replace(/<div class="status[^"]*"[\s\S]*?<\/div>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/DICTO: [^.]*\(draft of/g, ''); const m = outside.match(/New chapter \([^.]{0,60}|\((?:draft|DRAFT)[^)]{0,40}\)[,:][^.]{0,40}|working title[^.]{0,40}|not published[^.]{0,40}/); if (m) { console.error('RED-BOX GUARD: draft wording outside the red status box: "' + m[0] + '"'); process.exit(10); } }
  // 15 Nov (Platonic v1 went out with two chapter heads saying "New chapter (draft of 11 November 2026)"): a final (non-DRAFT) PDF may carry no draft wording of our own.
  if (!/^DRAFT/i.test(path.basename(pdf)) && /New chapter \(|\(draft of \d+ \w+ 20\d\d\)[,:]|working title/i.test(raw.replace(/<[^>]+>/g,' ').replace(/DICTO: [^.]*\(draft of/g,'')) && !process.env.ALLOW_BANNED) { console.error('GUARD: draft wording in a final PDF ("New chapter (draft…", "(draft of …)", "working title")'); process.exit(9); }
  // HOUSE-STYLE REMINDER (DICTO 21 Nov 2026, papers/HOUSE-STYLE.md: Winston's promise, cycling, fence, contributions close; Pledge-Turn-Prestige): warns, never stops a print.
  if (!/>\s*(Contributions|What this paper gives)\s*</i.test(raw)) console.warn('STYLE: no Contributions close yet (papers/HOUSE-STYLE.md: apply at this paper\'s next version)');
  const lang = (raw.match(/<html[^>]*lang="([^"]+)"/) || [])[1] || 'en';   // (native-review requirement dropped 11-07: DICTO's reader already checked; accuracy is guarded by the ja text guard)
  // KATAKANA-COVER GUARD (DICTO 11-07: "any japanese language version gets a katakana cover"): a final ja book needs its own cover
  // image (file name with -ja) whose alt text carries the katakana title.
  if (!/^en/i.test(lang) && !/^DRAFT/i.test(path.basename(pdf))) { const cv = raw.match(/class="page coverpage"[\s\S]*?<img[^>]*>/);
    const img = cv ? cv[0].match(/<img[^>]*>/)[0] : '';
    if (!new RegExp('src="[^"]*-' + lang.slice(0, 2) + '[^"]*"').test(img) || !/alt="[^"]*[\u0600-\u06FF\u3040-\u30FF\u4E00-\u9FFF]{3,}/.test(img)) { console.error(`GUARD: ${lang} edition without its own-script title cover (cover img src must contain -${lang.slice(0, 2)} and alt the title in its script)`); process.exit(6); } }
  // VERSION LINE GUARD (11-07: HexOct v10 and #39 v2 went out with their "Version N adds" sentence twice): a final PDF names its version's changes once.
  if (!/^DRAFT/i.test(path.basename(pdf)) && process.argv[6]) {
    const ver = process.argv[6].replace(/[.]/g, '\\.'), txt = raw.replace(/<[^>]+>/g, '');
    const n = (txt.match(new RegExp('Version ' + ver + ' (adds|corrects|writes|brings)', 'g')) || []).length;
    if (n > 1 && !process.env.ALLOW_BANNED) { console.error(`GUARD: "Version ${process.argv[6]} adds/corrects" appears ${n} times; keep one`); process.exit(8); } }
  // JA TEXT GUARD (11-07, reader: "reads like machine translation"): a final ja book may not carry leftover English words outside
  // （…） glosses, nor the known bad variants found in Quanta-ja v1.
  if (!/^en/i.test(lang) && !/^DRAFT/i.test(path.basename(pdf))) {
    const body = raw.replace(/<style[\s\S]*?<\/style>/g, '').replace(/<(sub|sup|code|a|i|em)\b[^>]*>[\s\S]*?<\/\1>/g, ' ').replace(/<[^>]+>/g, ' ');
    let body2 = body.replace(/(?<![\p{L}\w])[a-z]{2,}(?=\()/gu, ' '), prevB;   // function notation like polar(P(S)) is not prose
    do { prevB = body2; body2 = body2.replace(/（[^（）]*）|\([^()]*\)|「[ -~]*」|«[ -~]*»/g, ' '); } while (body2 !== prevB);   // nested brackets (11-07, ar: "(Keyed octahedron (golden-key octet))"); on-screen labels in 「」 or «»
    const latin = [...new Set((body2.match(/(?<![\p{L}\w.\-@\/_])[a-z]{4,}(?![\p{L}\w.\-@\/_(])/gu) || []).filter(w => !/^(zenodo|https?|www|dictospheres|com|org|arccos|arcsin|arctan|netlib|diag|[hc]+)$/.test(w)))];
    const BADJA = /白い女王|フル章|アリシアの不思議の国|いぶし十二面体|ポアン(?!ソ)|正の四次元|四次元の正多面体/g;
    const bad = [...new Set(body.match(BADJA) || [])];
    if ((latin.length || bad.length) && !process.env.ALLOW_BANNED) { console.error(`GUARD (${lang} text): leftover English ` + '' + latin.slice(0, 30).join(', ') + (bad.length ? '; bad variants ' + bad.join(', ') : '')); process.exit(7); } }
  if (hits.length && !process.env.ALLOW_BANNED) { console.error('BANNED PHRASE — not printed:\n  ' + hits.join('\n  ')); process.exit(2); } }
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });   // file:// figures may be read back from a canvas (light print)
const page = await b.newPage();
await page.goto('file://' + path.join(here, dir, 'paper.html'), { waitUntil: 'load' });
if (!process.env.FULL_RES) {
  // measure each figure's printed width on a second page laid out at the printed column width (print media), then resample on the real page
  const mm = v => { const m = String(v).match(/^([\d.]+)\s*(mm|in)$/); return m ? (m[2] === 'in' ? m[1] * 25.4 : +m[1]) : NaN; };
  const colMM = (process.env.PAGE_W ? mm(process.env.PAGE_W) : 210) - 30;   // left + right margins 15 mm
  const mp = await b.newPage({ viewport: { width: Math.round(colMM * 96 / 25.4), height: 1000 } });
  await mp.emulateMedia({ media: 'print' });
  await mp.goto('file://' + path.join(here, dir, 'paper.html'), { waitUntil: 'load' });
  const printedW = await mp.evaluate(() => [...document.images].map(i => Math.max(i.getBoundingClientRect().width, 0)));
  await mp.close();
  const done = await page.evaluate(async ([printedW, DPI]) => {
    const out = [];
    const imgs = [...document.images];
    for (let k = 0; k < imgs.length; k++) {
      const img = imgs[k]; await img.decode().catch(() => {});
      const nw = img.naturalWidth, nh = img.naturalHeight, w = printedW[k] || img.getBoundingClientRect().width;
      if (!w || !nw) continue;
      const tw = Math.ceil(w * DPI / 96);
      if (tw >= nw * 0.66) continue;   // at or below 1.5 x DPI (450 ppi): kept (mild smoothing makes flat-colour renders compress worse)
      const th = Math.max(1, Math.round(tw * nh / nw));
      const c = document.createElement('canvas'); c.width = tw; c.height = th;
      const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      g.drawImage(img, 0, 0, tw, th);
      const jpeg = /\.jpe?g($|\?)/i.test(img.currentSrc || img.src);
      const blob = await new Promise(r => c.toBlob(r, jpeg ? 'image/jpeg' : 'image/png', 0.92));
      if (!img.getAttribute('width') && !img.getAttribute('height')) img.setAttribute('width', nw);   // same layout as before if no CSS sizes it
      img.removeAttribute('srcset'); img.src = URL.createObjectURL(blob);
      await img.decode().catch(() => {});
      out.push(`${nw}x${nh}->${tw}x${th}`);
    }
    return out;
  }, [printedW, Number(process.env.LIGHT_DPI || 300)]);
  if (done.length) console.log('LIGHT: ' + done.length + ' figure(s) resampled to ' + (process.env.LIGHT_DPI || 300) + ' ppi (' + done.join(', ') + '); FULL_RES=1 keeps them as they are');
}
await page.pdf({ path: path.join(here, dir, pdf), ...(process.env.PAGE_W ? { width: process.env.PAGE_W, height: process.env.PAGE_H } : { format: 'A4' }), printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: `<div style="font:8px sans-serif;width:100%;padding:0 15mm;display:flex;justify-content:space-between;color:#666"><span>${title} · DICTO · dictospheres.com${doi && doi !== 'draft' ? ' · DICTO DOI: ' + doi : ''}${ver ? ' · v' + ver : ''}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
await b.close();
{ // SIZE GUARD (24 Nov 2026): over 4 MB or a figure over 4 Mpx = warning; a figure over 16.7 Mpx (iPad canvas cap) = error, PDF removed
  const out = path.join(here, dir, pdf), bytes = fs.statSync(out).size;
  if (bytes > 4e6) console.warn(`SIZE: ${(bytes / 1e6).toFixed(2)} MB (above 4 MB): check figures (study 2026-11-24-palomar-pdf-display)`);
  let rows = [];
  try { const { execFileSync } = await import('node:child_process');
    rows = execFileSync('pdfimages', ['-list', out]).toString().split('\n').slice(2).map(l => l.trim().split(/\s+/)).filter(r => r.length > 5 && r[2] === 'image').map(r => ({ page: +r[0], w: +r[3], h: +r[4] }));
  } catch { console.warn('SIZE: pdfimages not found; figure sizes not checked'); }
  const big = rows.filter(r => r.w * r.h > 4e6), huge = rows.filter(r => r.w * r.h > 16777216);
  if (big.length) console.warn('SIZE: figure(s) above 4 Mpx: ' + big.map(r => `p${r.page} ${r.w}x${r.h}`).join(', '));
  if (huge.length) { fs.unlinkSync(out); console.error('SIZE GUARD: figure(s) above 16.7 Mpx (iPad canvas cap), PDF not kept: ' + huge.map(r => `p${r.page} ${r.w}x${r.h}`).join(', ')); process.exit(11); }
}
console.log(dir + '/' + pdf + ' written');
