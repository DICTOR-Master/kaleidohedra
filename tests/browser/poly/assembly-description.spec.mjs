// From assembly-description.spec.ts: no name for a lone piece; with two, the build's name shows, and
// tapping it opens the whole of it (and closes it again).
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'a lone piece has no name; two pieces show one that opens and closes', async run(b) {
    let h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    assert.ok(await h.page.evaluate(() => document.getElementById('poly-build-name').hidden));
    await h.close();
    h = await open(b, { build: { nodes: [at('D4', [0, 0, 0], [0, 0, 0, 1], 'a'), at('D4', [0, 0, 0], [0, 0, 1, 0], 'b')], connections: [] } });
    assert.ok(!(await h.page.evaluate(() => document.getElementById('poly-build-name').hidden)), 'a name shows');
    assert.ok((await h.page.textContent('#poly-build-name')).length > 2);
    await h.page.tap('#poly-build-name'); await h.wait(300);
    assert.ok(await h.page.evaluate(() => document.getElementById('poly-build-name').classList.contains('open')));
    await h.page.tap('#poly-build-name'); await h.wait(300);
    assert.ok(!(await h.page.evaluate(() => document.getElementById('poly-build-name').classList.contains('open'))));
    h.noErrors(); await h.close();
  } },
];
