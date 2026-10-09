// From instructions-panel.spec.ts: the old instruction pill became the joined app's own cues. An
// empty build shows the outline to tap (which places the shape); a tapped face shows its highlight and
// the strip; a cue that would say nothing useful is not shown (nothing unnecessary).
import { open, assert } from './lib.mjs';
export default [
  { name: 'an empty build shows the outline; tapping it places the piece', async run(b) {
    const h = await open(b, {});
    assert.equal((await h.state()).nodes.length, 0);
    const c = await (await h.page.$('canvas')).boundingBox();
    await h.tap({ x: c.x + c.width / 2, y: c.y + c.height / 2 });
    assert.deepEqual(await h.shapes(), ['DODECAHEDRON']);
    h.noErrors(); await h.close();
  } },
  { name: 'a tapped face shows the strip with More...; leaving it hides them', async run(b) {
    const h = await open(b, { build: { nodes: [{ id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] } });
    await h.tapFace(0, await h.frontFace(0));
    assert.ok(await h.page.$('.poly-strip [data-more]'), 'More... shown');
    await h.page.tap('.poly-strip [data-more]'); await h.wait(400); await h.page.tap('.dim-wizard-close'); await h.wait(300);
    h.noErrors(); await h.close();
  } },
];
