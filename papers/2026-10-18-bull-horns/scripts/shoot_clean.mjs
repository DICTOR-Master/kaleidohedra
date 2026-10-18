// DICTO 2026-10-19: clean renders for the octet paper (no page captions, house background, fixed square stage), from the study 3D pages.
// Run on dicto-node: node shoot_clean.mjs <repo root> <out dir> [only-name ...]
import { chromium } from 'playwright';
import fs from 'node:fs';
const [ROOT, OUT, ...ONLY] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const S = (p) => `${ROOT}/studies/${p}`;
const P1 = S('2026-10-18-p1-golden-key-octet/renders/p1-golden-key-octet.html'), P2 = S('2026-10-18-p2-penrose-core-octet/renders/p2-penrose-core-octet.html');
const P3 = S('2026-10-18-p3-golden-envelope-octet/renders/p3-golden-envelope-octet.html'), P4 = S('2026-10-18-p4-golden-octet-adaptor/renders/p4-golden-octet-adaptor.html');
const KW = S('2026-10-18-p4-golden-octet-adaptor/renders/p4-keyed-W.html'), OC = S('2026-10-18-ocd-octet/renders/step10-pieces.html');
// [name, page, button label, pull-apart 0..100 (null = page default), turn about the vertical (deg), zoom]
const jobs = [
  ['p1set', P1, 'The set (2 shapes)', null, 0, 1], ['p1round', P1, 'Round one octahedron', null, 0, 1], ['p1net', P1, 'Network', 0, 0, 1],
  ['p2set', P2, 'The set (3 shapes)', null, 0, 1], ['p2round', P2, 'Round one octahedron', null, 0, 1], ['p2net', P2, 'Network (middle pieces hidden)', 0, 0, 1],
  ['k3', OC, 'Keyless kit, 3 Penrose cores (DICTO\'s choice)', null, 0, 1],
  ['p3two', P3, '3 · Two-shape set', null, 0, 1],
  ['p4two', P4, 'Two shapes: envelope + adaptor half', null, 0, 1], ['p4one', P4, 'One piece (fused) — network', 0, 0, 1], ['p4inside', P4, 'One piece, see-through', 0, 0, 1],
  ['p4envW', P4, 'Envelope + W (Fable)', null, 0, 1], ['p4ocdW', P4, 'OCD + W with OCD imprints', null, 0, 1], ['p4ocdWset', P4, 'OCD + W, the set', null, 0, 1],
  ['p4starW', P4, 'OCD + W centred on the Penrose star', null, 0, 1], ['p4starWset', P4, 'Star-centred W, the set', null, 0, 1],
  ['p4chamber', P4, 'Chamber, cut open', 0, 0, 1],
  ['kWone', KW, 'Keyed W, one piece', null, 0, 1], ['kWpair', KW, 'Bump meets dent', null, 0, 1], ['kWring', KW, '12 round one OCD', null, 0, 1],
];
const flat = [['penrose', S('2026-10-18-ocd-octet/renders/step13-penrose.html')], ['stars', S('2026-10-18-ocd-octet/renders/step4-stars.html')]];
const want = (n) => !ONLY.length || ONLY.includes(n);
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await b.newPage({ viewport: { width: 1100, height: 1100 }, deviceScaleFactor: 1 });
const wrap = (f) => 'data:text/html;base64,' + Buffer.from('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">' + fs.readFileSync(f, 'utf8')).toString('base64');
const CLEAN = `body>*:not(#stage){display:none!important} body{padding:0!important;margin:0!important;background:#f4f1ea!important}
#stage{flex:none!important;width:1000px!important;height:1000px!important;border:0!important;border-radius:0!important;background:#f4f1ea!important}
#info,.mark{display:none!important}`;
let last = null;
for (const [name, f, label, ex, turn, zoom] of jobs) {
  if (!want(name)) continue;
  if (last !== f) { await page.goto(wrap(f)); await page.waitForTimeout(3000); await page.addStyleTag({ content: CLEAN }); last = f; await page.waitForTimeout(800); }
  await page.evaluate((label) => { const btn = [...document.querySelectorAll('#btns button')].find((x) => x.textContent.trim() === label); if (!btn) throw new Error('no button ' + label); btn.click(); }, label);
  await page.waitForTimeout(1500);
  await page.evaluate(([ex, turn, zoom]) => {
    ctl.autoRotate = false; ctl.enableDamping = false;
    const e = document.getElementById('ex'); if (e && ex !== null) { e.value = ex; e.dispatchEvent(new Event('input')); }
    // frame what is shown: bounding sphere of the visible meshes, camera kept on its direction, fitted to the square
    const box = new THREE.Box3(); scene.updateMatrixWorld(true);
    scene.traverse((o) => { if (o.isMesh && o.visible && o.material && (o.material.opacity ?? 1) > 0.02) { let p = o, vis = true; while (p) { if (p.visible === false) vis = false; p = p.parent; } if (vis) box.expandByObject(o); } });
    const s = box.getBoundingSphere(new THREE.Sphere()), a = turn * Math.PI / 180;
    const v = cam.position.clone().sub(ctl.target).normalize(), x = v.x * Math.cos(a) + v.z * Math.sin(a), z = -v.x * Math.sin(a) + v.z * Math.cos(a); v.set(x, v.y, z);
    cam.aspect = 1; cam.updateProjectionMatrix();
    const d = s.radius / Math.sin(cam.fov * Math.PI / 360) * 1.02 / zoom;
    ctl.target.copy(s.center); cam.position.copy(s.center).addScaledVector(v, d); cam.lookAt(s.center); ctl.update();
  }, [ex, turn, zoom]);
  await page.waitForTimeout(1500);
  await page.locator('#stage').screenshot({ path: `${OUT}/${name}.png` }); console.log(name);
}
for (const [name, f] of flat) {
  if (!want(name)) continue;
  await page.goto(wrap(f)); await page.waitForTimeout(1200);
  const svg = page.locator('svg').first(); await svg.screenshot({ path: `${OUT}/${name}.png` }); console.log(name);
}
await b.close();
