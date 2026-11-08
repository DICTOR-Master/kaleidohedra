import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 1000 }, deviceScaleFactor: 2 });
await p.goto('file://' + process.cwd() + '/site/start-here/index.html', { waitUntil: 'load' }); await p.waitForTimeout(800);
await p.evaluate(() => document.getElementById('rule-1').scrollIntoView());
await p.screenshot({ path: 'rule1.png' }); await b.close();
