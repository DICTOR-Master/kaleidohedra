import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1200, height: 1000 } });
await p.goto('file://' + process.cwd() + '/bodhi.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
const V = {
  'seed-closed': { outer: true, outerOp: 0.16, copies: true, centre: true, r: 6.2 },
  'seed-open': { outer: true, outerOp: 0.10, copies: true, cex: 0.45, centre: true, r: 8.6 },
  'kitB-open': { copies: 'glass', centre: true, kit: 'B', ex: 0.55, r: 8.8 },
  'kitB-closed-gap': { centre: true, kit: 'B', ex: 0.0, r: 6.2 },
  'kitA-open': { copies: 'glass', centre: true, kit: 'A', ex: 0.55, r: 8.8 },
  'hollow': { centre: true, kit: 'B', only: ['B1'], ex: 0.35, r: 3.6 },
  'crowns': { centre: true, kit: 'B', only: ['B1', 'B4'], ex: 0.35, r: 7.2 },
};
for (const [n, o] of Object.entries(V)) { await p.evaluate(o => window.view(o), o); await p.waitForTimeout(800); await p.screenshot({ path: `${n}.png` }); }
await b.close();
