// From persistence.spec.ts: a build saves itself and comes back exactly after a reload.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'reloading restores the build exactly', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
    await h.page.tap('.dim-wizard-body [data-family="PRISMS"]'); await h.wait(500);
    await h.page.tap('.dim-wizard-body [data-action="tool:polyShape:PRISM_3"]'); await h.wait(1200);
    const before = await h.state();
    await h.page.reload();
    await h.page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await h.page.keyboard.press('Enter'); await h.wait(900);
    const after = await h.state();
    assert.deepEqual(after.nodes, before.nodes); assert.deepEqual(after.connections, before.connections);
    h.noErrors(); await h.close();
  } },
];
