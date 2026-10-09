// From view-mode.spec.ts: World View's three views (the old Solid is the joined app's Colour), in
// Settings, applied in Polyhedraverse's space.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'World View offers Colour (solid), Translucent and Skeleton, and each applies', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    // In the joined app World View is in Settings.
    await h.settings();
    const opts = await h.page.evaluate(() => [...document.querySelectorAll('#world-view-select option')].map((o) => [o.value, o.textContent.trim().toLowerCase()]));
    for (const want of ['colour', 'translucent', 'skeleton']) assert.ok(opts.some(([, label]) => label.includes(want)), `${want} in ${opts}`);
    for (const [v] of opts) { await h.page.selectOption('#world-view-select', v); await h.wait(400); assert.equal(await h.page.inputValue('#world-view-select'), v); }
    h.noErrors(); await h.close();
  } },
];
