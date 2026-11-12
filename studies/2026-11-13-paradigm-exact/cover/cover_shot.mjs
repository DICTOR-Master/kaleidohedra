// Rasterise the cover square SVG crisply (vector edges, antialiased, no blur) with the print pipeline's browser: 1000 px at scale 2.4 -> 2400 px.
import { createRequire } from 'node:module';
const require = createRequire(process.env.HOME + '/kaleidohedra-papers/');
const { chromium } = require('playwright');
const [svg, png] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1000 }, deviceScaleFactor: 2.4 });
await p.goto('file://' + svg); await p.screenshot({ path: png, clip: { x: 0, y: 0, width: 1000, height: 1000 } }); await b.close();
console.log('wrote', png);
