// DICTO 2026-10-23: X-ray in every 3D world and lattice ("a useful tool on any page where groups of pieces work together"; it was
// missing in the Icosahedral Octet Lattice and Targets), and the picture centred above the controls panel in every world ("fix all
// worlds"). Through the real UI, phone (390×844) and iPad (820×1180), one door per run (DOOR, default kaleidohedra): each world opens by
// its link; the X-ray button shows and a tap turns the cut on (and off); the model's centre sits in the free space above the panel
// (between the top of the screen and the panel's top, within 12% of that space's middle). No console errors. Screenshots: SHOTS.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const BASE = process.env.BASE_URL ?? 'http://localhost:8000', DOOR = process.env.DOOR ?? 'kaleidohedra', SH = process.env.SHOTS ?? '/tmp';
const WORLDS = (process.env.WORLDS ?? 'octet:lotusJewel,octetBuild:lotusJewel,targets,platonicMix,reuleaux,aristotle,octetTruss,studies,chains,shells,up,bodhiPyro').split(',');
const VPS = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const b = await chromium.launch(); const errors = []; let fails = 0;
for (const [vp, size] of Object.entries(VPS)) for (const w of WORLDS) {
  const page = await b.newPage({ viewport: size, hasTouch: true, isMobile: vp === 'phone' });
  page.on('pageerror', (e) => errors.push(`${vp} ${w}: ${e}`));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(`${vp} ${w}: ${m.text()}`); });
  try {
    await page.goto(`${BASE}/index.html?site=${DOOR}&open=${w}&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(3500);
    const x = page.locator('#xray-toggle');
    assert.ok(await x.isVisible(), 'X-ray button shows');
    await x.tap(); await page.waitForTimeout(800);
    assert.equal(await page.locator('#section-enable').isChecked(), true, 'X-ray on after a tap');
    await page.screenshot({ path: `${SH}/xray-${DOOR}-${vp}-${w.replace(':', '-')}.png` });
    await x.tap(); await page.waitForTimeout(500);
    assert.equal(await page.locator('#section-enable').isChecked(), false, 'X-ray off again');
    const f = await page.evaluate(() => window.__frameProbe());
    assert.ok(f, 'frame probe');
    assert.ok(f.cover > 40, `the controls panel is found (cover ${f.cover.toFixed(0)}px)`);
    const freeMid = (f.h - f.cover) / 2;
    assert.ok(Math.abs(f.cy - freeMid) <= 0.12 * (f.h - f.cover), `model centre ${f.cy.toFixed(0)} near free-space middle ${freeMid.toFixed(0)} (cover ${f.cover.toFixed(0)})`);
    console.log('ok', vp, w, `cover ${f.cover.toFixed(0)}px, centre y ${f.cy.toFixed(0)} / free middle ${freeMid.toFixed(0)}`);
    await page.screenshot({ path: `${SH}/frame-${DOOR}-${vp}-${w.replace(':', '-')}.png` });
  } catch (e) { fails++; console.log('FAIL', vp, w, e.message.split('\n')[0]); await page.screenshot({ path: `${SH}/fail-${DOOR}-${vp}-${w.replace(':', '-')}.png` }); }
  await page.close();
}
await b.close();
if (errors.length) { console.log('console errors:', errors.slice(0, 8).join(' | ')); fails++; }
console.log(fails ? `${fails} failed` : 'xray-and-frame OK'); process.exit(fails ? 1 : 0);
