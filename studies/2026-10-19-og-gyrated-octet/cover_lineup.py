# DICTO 2026-10-20: the cover line-up for #37a V3: the four solids (OG, OCD Stella, DBT, OTT) over the four fill pieces
# (DICTO Fill set 1 (DBT) F1; DICTO Fill set 2 (OTT) F1, F2, F3), true relative size, one view direction.
# 1) meshes -> renders/lineup.html (three.js, orthographic, one piece per frame); 2) cover_shots.mjs screenshots; 3) compose (PIL).
import os, sys, json, numpy as np, manifold3d as m3
H = os.path.dirname(os.path.abspath(__file__))
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def mesh(mf):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
    return P, T
def from_kit(f): return np.array(f['v']), np.array(f['t'])
D1 = json.load(open(os.path.join(H, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
OG = hull([[fq(c) for c in v] for v in D1['V']]); ST = hull(json.load(open(os.path.join(H, 'stella-37frame.json')))['V'])
DBT = hull([[fq(c) for c in v] for v in json.load(open(os.path.join(H, 'dbt-exact.json')))['V']])
OTT = hull([[fq(c) for c in v] for v in json.load(open(os.path.join(H, 'cut8-exact.json')))['V']])
K = json.load(open(os.path.join(H, 'renders', 'kits-data.json')))['kits']
f2 = next(f for f in K['cut8-oct']['fills'] if f['hand'] > 0); f3 = next(f for f in K['cut8-oct']['fills'] if f['hand'] < 0)
items = [('OG', 'Ogdoecontahedron', mesh(OG), '#d9a521'), ('OCD Stella', 'in the octahedron', mesh(ST), '#e8c33a'),
         ('DBT', 'Belted Triacontahedron', mesh(DBT), '#cf9418'), ('OTT', 'Octahedrally Truncated Triacontahedron', mesh(OTT), '#e0ae2c'),
         ('Fill set 1 (DBT) F1', 'grown bipyramid', from_kit(K['dbt-gyr']['fills'][0]), '#3f9a5b'), ('Fill set 2 (OTT) F1', 'grown bipyramid', from_kit(K['cut8-gyr']['fills'][0]), '#57b06f'),
         ('Fill set 2 (OTT) F2', 'grown tetrahedron, left', from_kit(f2), '#3f9a5b'), ('Fill set 2 (OTT) F3', 'grown tetrahedron, right', from_kit(f3), '#2a9d9a')]
out = []
for name, sub, (P, T), col in items:
    c = P.mean(0); out.append(dict(name=name, sub=sub, colour=col, v=np.round(P - c, 5).tolist(), t=T.tolist()))
ext = max(np.abs(np.array(o['v'])).max() for o in out) * 1.15
html = '''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}canvas{display:block}</style></head><body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script>
const D = __D__, E = __E__;
const r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(1200, 1200); r.setClearColor(0x000000, 0); document.body.append(r.domElement);
const scene = new THREE.Scene(); const cam = new THREE.OrthographicCamera(-E, E, E, -E, 0.1, 50);
const n = new THREE.Vector3(1, 1, 1).normalize(); const side = new THREE.Vector3(1, -1, 0).normalize();
const dir = side.clone().multiplyScalar(Math.cos(0.42)).addScaledVector(n, Math.sin(0.42)).applyAxisAngle(n, 0.35);
cam.up.copy(n); cam.position.copy(dir.clone().multiplyScalar(10)); cam.lookAt(0, 0, 0);
scene.add(new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.6)); const F = new THREE.DirectionalLight(0xffffff, 0.38); F.position.copy(dir.clone().multiplyScalar(6).add(n.clone().multiplyScalar(-2))); scene.add(F); const L = new THREE.DirectionalLight(0xffffff, 0.78); L.position.copy(dir.clone().multiplyScalar(4).add(n.clone().multiplyScalar(5)).add(new THREE.Vector3(-1.5, 1, 2))); scene.add(L);
let grp = null;
window.show = (i) => { if (grp) scene.remove(grp); const d = D[i]; const g = new THREE.BufferGeometry(); const p = new Float32Array(d.t.length * 9); let k = 0;
  for (const tr of d.t) for (const j of tr) { p[k++] = d.v[j][0]; p[k++] = d.v[j][1]; p[k++] = d.v[j][2]; }
  g.setAttribute('position', new THREE.BufferAttribute(p, 3)); g.computeVertexNormals();
  grp = new THREE.Group(); grp.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: d.colour, roughness: 0.5, metalness: 0.06, flatShading: true })));
  grp.add(new THREE.LineSegments(new THREE.EdgesGeometry(g, 18), new THREE.LineBasicMaterial({ color: 0x2b261e, transparent: true, opacity: 0.45 })));
  scene.add(grp); r.render(scene, cam); return D.length; };
</script></body></html>'''
open(os.path.join(H, 'renders', 'lineup.html'), 'w').write(html.replace('__D__', json.dumps(out, separators=(',', ':'))).replace('__E__', f'{ext:.4f}'))
json.dump([dict(name=o['name'], sub=o['sub']) for o in out], open(os.path.join(H, 'renders', 'lineup-labels.json'), 'w'))
print('lineup.html written, half-width', round(ext, 4))
