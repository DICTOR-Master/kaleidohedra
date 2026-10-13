// Every catalogued stage as a PNG (900 px, the catalogue's own look), with an index of its facts: renders/index.json.
// For the paper (Fable selects). Run on dicto-node with the catalogue served: BASE_URL=http://localhost:8000 node render.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
const OUT = process.env.OUT ?? 'renders';
fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1000, height: 1000 } });
await page.goto(`${process.env.BASE_URL ?? 'http://localhost:8000'}/studies/2026-10-13-fused-shells/catalogue.html`);
await page.waitForFunction(() => window.CATALOGUE);
const worlds = await page.evaluate(() => window.CATALOGUE.map((w) => ({ id: w.id, name: w.name, app: !!w.app, steps: w.steps.map(({ pieces, ...s }) => s), stages: w.stages.map((s) => s) })));
const index = [];
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const save = async (file, w, idx, hi, extra) => {
  const url = await page.evaluate(([w, idx, hi, extra]) => window.renderStage(w, idx, hi, extra, 900), [w, idx, hi, extra]);
  fs.writeFileSync(`${OUT}/${file}`, Buffer.from(url.split(',')[1], 'base64'));
};
for (const [w, world] of worlds.entries()) {
  const base = slug(world.app ? `app-${world.id}` : world.id);
  for (const [k, s] of world.steps.entries()) {
    const file = `${base}-step${String(k + 1).padStart(2, '0')}.png`;
    await save(file, w, Array.from({ length: k + 1 }, (_, i) => i), k, []);
    index.push({ file, structure: world.name, kind: world.app ? 'app Top shell stage' : 'main route step', step: k + 1, of: world.steps.length, adds: s.adds, convex: s.convex, faces: s.faces, faceShapes: s.shapes, planes: s.planes, note: s.note });
  }
  for (const [si, st] of world.stages.entries()) {
    if (!st.p.length && !st.convex) continue; // whole-ring stages already on the route
    const file = `${base}-stage${String(si + 1).padStart(3, '0')}.png`;
    await save(file, w, st.g, null, st.p);
    index.push({ file, structure: world.name, kind: st.p.length ? 'partial ring on a complete shell' : 'convex whole-ring stage', rings: st.g, partial: st.how, convex: st.convex, faces: st.faces, faceShapes: st.shapes, planes: st.planes, name: st.name });
  }
}
fs.writeFileSync(`${OUT}/index.json`, JSON.stringify({ credit: 'DICTO · dictospheres.com', note: 'Orange: the pieces added at that step (or the partial ring); other colours: earlier rings. Counts: the fused solid\'s outside (steps.py).', figures: index }, null, 1));
console.log('rendered', index.length);
await b.close();
