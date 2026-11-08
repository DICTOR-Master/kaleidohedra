// UI test of the return cover (DICTO 11-08): in a world with a build, coming back to the tab shows the blank cover; Clear it opens
// the menu over a hidden scene and keeps the build saved; picking a world opens it at once; Keep it carries on.
import { chromium } from 'playwright';
const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true }); const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
async function go(u) { await p.goto(`${BASE}/index.html?${u}`); await p.waitForTimeout(1500); if (await p.locator('#welcome-overlay').isVisible()) await p.keyboard.press('Enter'); await p.waitForTimeout(2000); }
const state = () => p.evaluate(() => { const d = document.getElementById('leave-dialog'); return { shown: !d.hidden, blank: d.classList.contains('blank'), btns: [...d.querySelectorAll('[data-choice]')].map(x => x.textContent), hidden: window.__sceneHidden?.() }; });
await go('site=kaleidohedra&open=platonicMix&probe');
for (const w of ['D', 'I']) { await p.locator(`[data-pm-world="${w}"]`).tap(); await p.waitForTimeout(700); }
let ok = true;
// 1. back to the tab -> Keep it
p.evaluate(() => window.__returnCover()); await p.waitForTimeout(500);
let s = await state(); console.log('return 1:', JSON.stringify(s)); await p.screenshot({ path: (process.env.SHOTS ?? '/tmp') + '/return-cover.png' });
ok &&= s.shown && s.blank && s.btns.join('|') === 'Clear it|Keep it' && s.hidden === true;
await p.tap('[data-choice="keep"]'); await p.waitForTimeout(600);
s = await state(); const mixK = await p.evaluate(() => window.__platonicMixProbe().mix);
console.log('Keep it:', JSON.stringify(s), 'mix', mixK); ok &&= !s.shown && s.hidden === false && mixK === 'DI';
// 2. back again -> Clear it -> the menu, scene hidden, build saved
p.evaluate(() => window.__returnCover()); await p.waitForTimeout(500);
await p.tap('[data-choice="clear"]'); await p.waitForTimeout(800);
s = await state(); const wiz = await p.locator('text=Pick a dimension to build in.').isVisible();
console.log('Clear it:', JSON.stringify(s), 'menu:', wiz); ok &&= !s.shown && wiz && s.hidden === true;
await p.screenshot({ path: (process.env.SHOTS ?? '/tmp') + '/return-cover-cleared.png' });
// 3. pick a world straight away -> it opens and is shown
await p.locator('text="The Stackings World" >> visible=true').first().tap(); await p.waitForTimeout(2500);
s = await state(); console.log('picked Stackings:', JSON.stringify(s)); ok &&= s.hidden === false;
// 4. the mix build is still saved: entering asks Continue / Start fresh
await go('site=kaleidohedra&open=platonicMix&probe');
const asked = await p.locator('#leave-dialog:not([hidden]) [data-choice="fresh"]').count();
console.log('mix still saved (asked):', asked); ok &&= asked === 1;
console.log('page errors:', errs.length, errs.slice(0, 3));
console.log(ok && !errs.length ? 'FINAL ok' : 'FINAL FAIL');
await b.close();
