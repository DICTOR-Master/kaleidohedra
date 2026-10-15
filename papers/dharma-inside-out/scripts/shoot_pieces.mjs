// Piece gallery tiles for the paper (render_pieces.html served on localhost:8001): six faithful layers + the two tight end layers.
import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 700, height: 700 } });
const jobs = [0, 1, 2, 3, 4, 5].map((k) => ['polar-render.json', k, `/tmp/piece-${k}.png`]).concat([['polar-tight-render.json', 0, '/tmp/piece-t0.png'], ['polar-tight-render.json', 5, '/tmp/piece-t5.png']]);
for (const [f, k, out] of jobs) {
  await p.goto(`http://localhost:8001/render_pieces.html?f=${f}&k=${k}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: out }); console.log(out);
}
await b.close();
