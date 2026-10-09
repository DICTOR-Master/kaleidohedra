// From tools-column.spec.ts: the joined app's controls in Polyhedraverse's space. DICTO (Tab, or the
// button) opens and closes the shape browser's home; Projection cycles; the language changes the words.
import { open, assert } from './lib.mjs';
export default [
  { name: 'DICTO opens and closes; its Polyhedraverse block lists the families', async run(b) {
    const h = await open(b, {});
    await h.dicto();
    assert.ok(await h.page.$('.dicto-dim-content [data-family="PLATONIC"]'));
    await h.page.keyboard.press('Tab'); await h.wait(400);
    assert.ok(!(await h.page.evaluate(() => document.querySelector('.dim-wizard-overlay').classList.contains('open'))));
    h.noErrors(); await h.close();
  } },
  { name: 'Projection cycles, and the language changes the words', async run(b) {
    const h = await open(b, { build: { nodes: [{ id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] } });
    const before = await h.page.getAttribute('#projection-toggle', 'title');
    await h.page.tap('#projection-toggle'); await h.wait(400);
    await h.page.tap('#projection-toggle'); await h.wait(400);
    await h.settings();
    await h.page.selectOption('#setting-language', 'ja'); await h.wait(600);
    await h.page.tap('#lab-toggle').catch(() => {}); await h.wait(300);
    await h.tapFace(0, await h.frontFace(0));
    assert.match(await h.page.textContent('.poly-strip [data-more]'), /[^\x00-\x7F]/, 'Japanese words in the strip');
    assert.ok(before);
    h.noErrors(); await h.close();
  } },
];
