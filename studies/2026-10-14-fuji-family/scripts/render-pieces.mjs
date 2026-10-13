// Screenshot each piece from render-pieces.html (run on dicto-node: node render-pieces.mjs). DICTO · dictospheres.com
import { chromium } from 'playwright';
import fs from 'node:fs'; import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const data = fs.readFileSync(path.join(here, '..', 'paper', 'figures', process.env.SOLIDS ?? 'solids.json'), 'utf8');
const html = fs.readFileSync(path.join(here, 'render-pieces.html'), 'utf8').replace('<script>\n//', `<script>const DATA = ${data};\n//`);
fs.writeFileSync(path.join(here, '_r.html'), html);
const VIEWS = JSON.parse(process.argv[2] ?? '{}');
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1200, height: 1100 } });
await p.goto('file://' + path.join(here, '_r.html')); await p.waitForFunction(() => window.THREE && window.show);
fs.mkdirSync(path.join(here, 'out'), { recursive: true });
for (const [name, [dir, up, fixR]] of Object.entries(VIEWS)) {
  await p.evaluate(([n, d, u, r]) => window.show(n, d, u ?? undefined, r ?? undefined), [name.split(':')[0], dir, up ?? null, fixR ?? null]);
  await p.waitForTimeout(300); await p.locator('#c').screenshot({ path: path.join(here, 'out', name.replace(':', '-') + '.png') });
}
await b.close(); fs.unlinkSync(path.join(here, '_r.html')); console.log('done');
