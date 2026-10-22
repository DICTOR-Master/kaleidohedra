// DICTO 2026-10-23: Figure 3's right panel ("Keyless, three Penrose cores") redrawn from the app's verified kit. The study page's
// assembly3 view placed caps, rests and tetrahedra by all 24 operations of Th, which these pieces do not all share, so it drew
// overlapping wrong copies (its cell sums to 5.5079, not 2.5103). The app's kit (Kaleidohedra scripts/build-octet-truss-data.mjs,
// kits.cores.round, exported to app-cores-round.json) keeps the right copies: 1 OG, 6 caps, 12 central and 24 flanking cores,
// 12 rests, 4 + 4 tetrahedra. Same page, camera, colours and pull-apart as the other panels; only the pieces are swapped.
// Run on dicto-node: node shoot_k3_app.mjs <repo root> <out dir>
import { chromium } from 'playwright';
import fs from 'node:fs';
const [ROOT, OUT] = process.argv.slice(2);
const OC = `${ROOT}/studies/2026-10-18-ocd-octet/renders/step10-pieces.html`;
const APP = JSON.parse(fs.readFileSync(new URL('./app-cores-round.json', import.meta.url)));
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1100, height: 1100 }, deviceScaleFactor: 1 });
const wrap = (f) => 'data:text/html;base64,' + Buffer.from('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">' + fs.readFileSync(f, 'utf8')).toString('base64');
const CLEAN = `body>*:not(#stage){display:none!important} body{padding:0!important;margin:0!important;background:#f4f1ea!important}
#stage{flex:none!important;width:1000px!important;height:1000px!important;border:0!important;border-radius:0!important;background:#f4f1ea!important}
#info,.mark{display:none!important}`;
await page.goto(wrap(OC)); await page.waitForTimeout(3000); await page.addStyleTag({ content: CLEAN }); await page.waitForTimeout(800);
await page.evaluate(() => [...document.querySelectorAll('#btns button')].find((x) => x.textContent.trim().startsWith('Keyless kit, 3 Penrose cores')).click());
await page.waitForTimeout(1500);
const report = await page.evaluate((APP) => {
  ctl.autoRotate = false; ctl.enableDamping = false;
  const before = items.length;
  // the page's OG and the app's OG: same solid, maybe another scale
  const rad = (vs) => Math.max(...vs.map((v) => Math.hypot(...v)));
  const appOG = Object.values(APP.pieces).find((p) => p.name === 'k_ocd');
  const s = rad(D.k.ocd.v) / rad(appOG.v);
  const MAT = { k_ocd: mats.ocd, k_cap: mats.cap, k_core_c: mats.core, k_core_f1: mats.core2, k_core_f2: mats.core2, k_rest3: mats.mid, tet: mats.tl, 'tet~': mats.tr };
  world.clear(); items = [];
  const placed = APP.round.map((it) => {
    const p = APP.pieces[it[0]], m = it.slice(1, 10), tr = it.slice(10, 13);
    const M = new THREE.Matrix4().set(m[0], m[1], m[2], tr[0], m[3], m[4], m[5], tr[1], m[6], m[7], m[8], tr[2], 0, 0, 0, 1);
    const g = geo(p, false); g.applyMatrix4(M); g.scale(s, s, s);
    return { name: p.name, g, c: centroid(g).clone() };
  });
  // a middle piece's three cores and its rest pull apart together, as on the page (home = the rest's centre)
  const rests = placed.filter((x) => x.name === 'k_rest3');
  for (const x of placed) {
    let home = x.c.clone();
    if (x.name.startsWith('k_core')) home = rests.reduce((a, r) => (r.c.distanceTo(x.c) < a.distanceTo(x.c) ? r.c : a), rests[0].c).clone();
    if (x.name === 'k_ocd') home = new THREE.Vector3();
    add(x.g, MAT[x.name] ?? mats.mid, null, home);
  }
  explode();
  // the app's tetrahedra sit a little farther out than the page's wrong copies: pull the camera back to frame the whole kit
  cam.zoom = 1 / 1.36; cam.updateProjectionMatrix();
  const count = {}; placed.forEach((x) => (count[x.name] = (count[x.name] || 0) + 1));
  return { before, after: items.length, scale: s, count };
}, APP);
console.log(JSON.stringify(report));
await page.waitForTimeout(1500);
fs.mkdirSync(OUT, { recursive: true });
await page.locator('#stage').screenshot({ path: `${OUT}/k3.png` }); console.log('k3');
await b.close();
