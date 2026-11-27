import { chromium } from 'playwright';
const URL = process.argv[2], OUT = process.argv[3], cases = [['Oh', 4], ['Td', 9], ['Td', 8], ['T', 58], ['Ih', 1]];
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1300, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto(URL); await p.waitForFunction(() => document.querySelectorAll('#groupSel option').length > 5, null, { timeout: 60000 });
const notes = () => p.evaluate(() => Array.from(document.querySelectorAll('.note')).map(n => n.textContent).filter(t => /^(Vacuus|Resonus):/.test(t)));
const press = async (id, on) => { const cur = await p.getAttribute(id, 'aria-pressed'); if ((cur === 'true') !== on) await p.click(id); };
for (const [g, k] of cases) {
  await p.selectOption('#groupSel', g); await p.waitForTimeout(400);
  if (await p.getAttribute('#modeList', 'aria-pressed') !== 'true' && await p.isVisible('#modeList')) await p.click('#modeList');
  await p.waitForTimeout(400); await p.click(`.item[data-k="${k}"]`); await p.waitForTimeout(600);
  for (const [v, r, tag] of [[true, false, 'vac'], [false, true, 'res'], [true, true, 'both']]) {
    await press('#vacBtn', v); await press('#resBtn', r); await p.waitForTimeout(1200);
    await p.screenshot({ path: `${OUT}/k${k}-${tag}.png`, clip: { x: 150, y: 60, width: 550, height: 500 } });
    console.log(g, k, tag, JSON.stringify(await notes()).slice(0, 400));
  }
  await press('#vacBtn', false); await press('#resBtn', false);
}
console.log('errors', JSON.stringify(errs)); await b.close(); console.log(errs.length ? 'FINAL FAIL' : 'FINAL ok');
