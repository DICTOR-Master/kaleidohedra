import { chromium } from 'playwright';
import { execSync } from 'node:child_process';
const files = process.argv.slice(2);
const scale = Number(process.env.SCALE || 1.5);
const browser = await chromium.launch();
const rss = () => { try { const rows = execSync('ps -eo pid=,ppid=,rss=').toString().trim().split('\n').map(l=>l.trim().split(/\s+/).map(Number)); const kids = new Map(); for (const [p,pp,r] of rows){ if(!kids.has(pp)) kids.set(pp,[]); kids.get(pp).push([p,r]); } let s=0; const st=[process.pid]; while(st.length){ const q=st.pop(); for (const [p,r] of (kids.get(q)||[])){ s+=r; st.push(p);} } return s/1024; } catch { return 0; } };
const results = [];
for (const f of files) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const errs = []; page.on('console', m => { if (m.type()==='error'||m.type()==='warning') errs.push(m.text().slice(0,200)); });
  page.on('crash', () => errs.push('PAGE CRASH'));
  await page.goto('http://127.0.0.1:8765/render.html'); await page.waitForFunction('window.ready');
  let peak = 0; const iv = setInterval(() => { const r = rss(); if (r > peak) peak = r; }, 250);
  let r; try { r = await page.evaluate(([u,s]) => window.runPdf(u,s), ['/zen/'+f, scale]); } catch (e) { r = {error: String(e).slice(0,300)}; }
  clearInterval(iv);
  const heap = await page.evaluate(() => performance.memory ? Math.round(performance.memory.usedJSHeapSize/1e6) : null).catch(()=>null);
  results.push({file: f, scale, ...r, peakRssMB: Math.round(peak), jsHeapMB: heap, warnings: [...new Set(errs)].slice(0,10)});
  console.log(JSON.stringify(results.at(-1)));
  await ctx.close();
}
await browser.close();
