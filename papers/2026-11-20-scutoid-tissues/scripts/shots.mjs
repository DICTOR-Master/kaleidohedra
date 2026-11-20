// DICTO · dictospheres.com — one transparent frame per scene of a renders/*.html (Playwright), at 1600 px: the shots.mjs of the
// Dehn Canon paper (papers/2026-11-19-dehn-canon) and of the gold-standard figures (studies 2026-10-19-five-fold-octet).   usage: node shots.mjs <html> <outdir>
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const [F, OUT] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1600, height: 1600 } });
await page.goto('file://' + path.resolve(F)); await page.waitForFunction(() => typeof window.show === 'function');
const n = await page.evaluate(() => window.show(0));
for (let i = 0; i < n; i++) { await page.evaluate((i) => window.show(i), i); await page.waitForTimeout(300); await page.screenshot({ path: `${OUT}/p${i}.png`, omitBackground: true }); }
console.log('shots', OUT, n); await b.close();
