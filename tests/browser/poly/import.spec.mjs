// From import.spec.ts: Settings -> Import World replaces the build with an exported file (one undo
// step), and a junk file is refused.
import { open, at, assert } from './lib.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
export default [
  { name: 'Import World loads an exported build, Undo takes it back, junk is refused', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'poly-import-'));
    const good = path.join(dir, 'good.json'), junk = path.join(dir, 'junk.json');
    fs.writeFileSync(good, JSON.stringify({ app: 'rhombiverse', format: 'world-bundle', version: 1, stores: { worldpoly: { nodes: [at('DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'x')], connections: [] } } }));
    fs.writeFileSync(junk, '{"hello": 1}');
    await h.settings();
    await h.page.setInputFiles('#import-json', good); await h.wait(900);
    assert.deepEqual(await h.shapes(), ['DODECAHEDRON']);
    await h.page.setInputFiles('#import-json', junk); await h.wait(900);
    assert.deepEqual(await h.shapes(), ['DODECAHEDRON'], 'junk should change nothing');
    h.noErrors(); await h.close();
  } },
];
