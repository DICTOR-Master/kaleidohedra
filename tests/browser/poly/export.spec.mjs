// From export.spec.ts: Settings -> Export World downloads a real JSON file holding this build.
import { open, at, assert } from './lib.mjs';
import fs from 'node:fs';
export default [
  { name: 'Export World downloads valid JSON with the Polyhedraverse build in it', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a'), at('D8', [2, 0, 0], [0, 0, 0, 1], 'b')] } });
    await h.settings();
    const [dl] = await Promise.all([h.page.waitForEvent('download'), h.page.click('#export-json')]);
    const json = JSON.parse(fs.readFileSync(await dl.path(), 'utf8'));
    assert.equal(json.format, 'world-bundle');
    assert.deepEqual(json.stores.worldpoly.nodes.map((n) => n.shape), ['CUBE', 'D8']);
    h.noErrors(); await h.close();
  } },
];
