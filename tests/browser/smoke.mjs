// Real-browser smoke test -- the CI equivalent of "Harness 2" in
// .claude/skills/browser-test-harness/SKILL.md, scoped down to a fast,
// deterministic check suitable for every push/PR (not a full
// regression suite). Assumes the app is already being served at
// BASE_URL (the CI workflow starts `python3 -m http.server`).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8000';
// Which front door (KRP: Kaleidohedra and Rhombiverse are one app); CI runs both.
const DOOR = process.env.DOOR ?? 'kaleidohedra';

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // Logged live, not just collected for the end-of-run check below --
  // a real error that happens before some later assertion throws (e.g.
  // a timeout) would otherwise never make it into the CI log at all.
  const errors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const text = `[console] ${msg.text()}`;
      errors.push(text);
      console.log(text);
    }
  });
  page.on('pageerror', (err) => {
    const text = `[pageerror] ${err}`;
    errors.push(text);
    console.log(text);
  });
  page.on('dialog', (dialog) => dialog.accept());

  await page.goto(`${BASE_URL}/index.html?site=${DOOR}`);

  // Welcome overlay shows on first load and can be dismissed. Timeout
  // recalibrated 2026-08-19: render.js's own module graph has grown
  // (B1-B6 added dozens of files) to where cold JS parse/eval genuinely
  // takes several seconds on CI's shared runners -- confirmed via direct
  // timing (not a real app bug: zero console/page errors at any point,
  // and this is a no-build-step app by design, so shrinking the module
  // graph via a bundler isn't the right fix for a test timeout).
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 });
  // Real, stale-selector CI break found and fixed 2026-08-29: '#enter-
  // world-btn' hasn't existed since the 2026-08-26 welcome-screen
  // redesign (rotating RD logo, two live ENTER faces) -- every CI run
  // since has been failing on this exact line, unnoticed. welcome.js's
  // own ENTER faces are only clickable while animated to face the
  // viewer, so its own header comment already documents the reliable
  // path: "a literal Enter keypress ... is the reliable path when it's
  // mid-swing." Use that same real, intended fallback here instead of a
  // fragile click on geometry that's only sometimes actionable.
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
  const overlayDisplay = await page.$eval('#welcome-overlay', (el) => getComputedStyle(el).display);
  assert.equal(overlayDisplay, 'none', 'welcome overlay should hide after Enter');

  // The DICTO wizard opens on every load (the wheels are gone, 2026-10-08), on this door's app;
  // Escape closes it, leaving the default 3D+ world.
  const wizard = await page.evaluate(() => ({ open: document.querySelector('.dim-wizard-overlay')?.classList.contains('open'), shown: document.querySelector('.dicto-shown')?.textContent }));
  assert.ok(wizard.open, 'the DICTO wizard should open on load');
  assert.equal(wizard.shown, DOOR.toUpperCase(), `the wizard should open on ${DOOR}`);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);

  // Nothing is saved to localStorage until the first onChange() fires
  // (documented, pre-existing behavior -- render.js only persists on a
  // real mutation, not right after initial seeding). So this checks the
  // DELTA from one build action, not an absolute count -- the only thing
  // actually worth asserting here.
  const cellCount = async () => {
    const raw = await page.evaluate((door) => localStorage.getItem(`${door}-world`), DOOR);
    return raw ? Object.keys(JSON.parse(raw).cells).length : 0;
  };

  // A real Build-mode click on the seed cell's face adds a neighbor.
  // waitForSelector (not page.$, which does a single instantaneous
  // query) actively retries until the canvas is actually attached --
  // a single-shot query flaked once in local testing even though the
  // canvas was confirmed present a moment later.
  const canvas = await page.waitForSelector('canvas', { state: 'attached', timeout: 25000 });
  const box = await canvas.boundingBox();
  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  await page.waitForTimeout(500);
  const afterFirstClick = await cellCount();
  assert.ok(afterFirstClick > 0, 'expected at least one cell to exist after the first click');

  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  await page.waitForTimeout(500);
  const afterSecondClick = await cellCount();
  assert.equal(afterSecondClick, afterFirstClick + 1, 'expected exactly one new cell from the second build click');

  // Mode switching is tested directly against the real primitive (.mode-btn[data-mode=...]).
  async function clickMode(modeName) {
    const clicked = await page.evaluate((mode) => {
      const el = document.querySelector(`.mode-btn[data-mode="${mode}"]`);
      if (!el) return false;
      el.click();
      return true;
    }, modeName);
    assert.ok(clicked, `.mode-btn[data-mode="${modeName}"] should exist and be clickable`);
  }

  // One piece at a time (2026-09-25): Build is the only user mode left
  // (Fill/Round/Excavate/Sculpt/Report are gone) -- it must still exist,
  // since other code resets to it by clicking this button.
  await clickMode('build');
  for (const gone of ['fill', 'round', 'excavate', 'sculpt', 'report']) {
    assert.equal(await page.$(`.mode-btn[data-mode="${gone}"]`), null, `${gone} mode should be gone`);
  }

  // Tab opens and closes the DICTO wizard (Menu and Space do too).
  const wizardOpen = () => page.evaluate(() => document.querySelector('.dim-wizard-overlay').classList.contains('open'));
  await page.keyboard.press('Tab');
  await page.waitForTimeout(400);
  assert.ok(await wizardOpen(), 'Tab should open the DICTO wizard');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(400);
  assert.ok(!(await wizardOpen()), 'Tab again should close the DICTO wizard');

  // Almanac (docs/RHOMBIVERSE_SPEC_ALMANAC.md, Stage 1): exercises the real
  // createAlmanac() module directly (the
  // same function render.js's own init calls once for real; this makes
  // a second, independent instance for the test, which is fine -- the
  // module has no singleton state to collide with). Queries are scoped
  // to the overlay THIS call appends (the last '.almanac-overlay' in
  // DOM order), not an unscoped selector, since render.js's own real
  // instance is also present in the page by this point.
  const almanacResult = await page.evaluate(async () => {
    const { createAlmanac } = await import('./src/app/almanac.js');
    const { ALMANAC_ENTRIES } = await import('./src/app/almanac-data.js');
    createAlmanac().open();
    const overlays = document.querySelectorAll('.almanac-overlay');
    const overlay = overlays[overlays.length - 1];
    const opened = overlay.classList.contains('open');
    const entryCount = overlay.querySelectorAll('.almanac-entry').length;
    overlay.querySelector('.almanac-entry')?.click();
    const detailShown = getComputedStyle(overlay.querySelector('.almanac-detail')).display !== 'none';
    overlay.querySelector('.almanac-close')?.click();
    const closed = !overlay.classList.contains('open');
    return { opened, entryCount, expectedCount: ALMANAC_ENTRIES.length, detailShown, closed };
  });
  assert.ok(almanacResult.opened, 'Almanac overlay should open');
  assert.equal(almanacResult.entryCount, almanacResult.expectedCount, 'Almanac should list every ALMANAC_ENTRIES entry');
  assert.ok(almanacResult.detailShown, 'clicking an Almanac entry should show its detail panel');
  assert.ok(almanacResult.closed, 'the close button should close Almanac');

  if (errors.length > 0) {
    throw new Error(`Console/page errors during smoke test:\n${errors.join('\n')}`);
  }

  await browser.close();
  console.log(`smoke test passed (${DOOR}): welcome overlay, DICTO wizard, build, mode switching, and Almanac, zero console errors`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
