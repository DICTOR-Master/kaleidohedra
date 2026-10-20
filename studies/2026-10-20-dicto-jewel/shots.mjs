// DICTO 2026-10-20 (Jewel paper, 2x pixel ratio for sharp print): one transparent frame per scene of renders/family.html (dicto-node, Playwright). usage: node cover_shots.mjs <html> <outdir>
import { chromium } from 'playwright';
import fs from 'node:fs';
const [F, OUT] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 2 });
await page.goto('file://' + F); await page.waitForFunction(() => typeof window.show === 'function');
const n = await page.evaluate(() => window.show(0));
for (let i = 0; i < n; i++) { await page.evaluate((i) => window.show(i), i); await page.waitForTimeout(400); await page.screenshot({ path: `${OUT}/p${i}.png`, omitBackground: true }); }
console.log('shots', n); await b.close();
