# DICTO 2026-10-20: figures for the OG family paper (both ways). Builds the nine solids exactly (4 down, the OG, 4 up), writes
# data/og-family-solids.json (float corners + ordered faces) and renders/family.html (three.js, one scene per frame, window.show(i)):
#   scenes 0-8   the nine solids alone, true relative size, faces coloured by number of sides
#   scenes 9-10  the two breaks: DICTO TPP inside DICTO DPHP (glass), DICTO TQP inside DICTO TQH (glass), corners poking out in red
#   scenes 11-16 the six shells that fill exactly: the inner solid with the shell pieces placed on the faces round one five-fold axis
# Shots: shots.mjs (Playwright, dicto-node); compose: family_compose.py.
import json, os
import numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'exact_upward.py')).read().split("names = ['DICTO KRE'")[0])      # OG, G, step, solid, polytope ...

def rev(S):
    out = []
    for n, d in solid(S):
        k = d / dot(n, n); out.append(tuple(k * x for x in n))
    return list(dict.fromkeys(out))

UP = ['DICTO KRE', 'DICTO PHE', 'DICTO TPP', 'DICTO DPHP']; DOWN = ['DICTO TPH', 'DICTO TQH', 'DICTO TQP', 'DICTO TQHD']
chain = {'DICTO OG': OG}; S = OG
for nm in UP: S = step(S)[0]; chain[nm] = S; print(nm, len(S), flush=True)
S = OG
for nm in DOWN: S = rev(S); chain[nm] = S; print(nm, len(S), flush=True)
order = DOWN[::-1] + ['DICTO OG'] + UP
solids = {}
for nm in order:
    C, F = polytope(solid(chain[nm]))
    solids[nm] = {'v': [[x.f() for x in c] for c in C], 'f': [list(o) for o, _ in F]}
json.dump({'mark': 'DICTO OG family (both ways), float corners + ordered faces from the exact builds, 2026-10-20', 'order': order, 'solids': solids},
          open(os.path.join(HERE, 'data', 'og-family-solids.json'), 'w'))

COL = {3: ['#e0ae2c', '#f3d77a'], 4: ['#3f9a5b', '#a5d9ae'], 5: ['#2f6fb0', '#79a6db'], 6: ['#c4553a', '#f0a68f'], 10: ['#7a4fa0', '#c2a3dc']}
def shape_key(V, o):                     # face shape: number of sides and its sorted side lengths
    return (len(o), tuple(sorted(round(float(np.linalg.norm(V[o[(i + 1) % len(o)]] - V[o[i]])), 5) for i in range(len(o)))))
def faces_mesh(sd, alpha=1.0, solid_col=None):
    V = np.array(sd['v']); tris, cols, edges = [], [], []
    from collections import Counter
    cnt = Counter(shape_key(V, o) for o in sd['f']); shade = {}
    for key, _ in sorted(cnt.items(), key=lambda kv: (kv[0][0], -kv[1], kv[0][1])):
        n = sum(1 for k in shade if k[0] == key[0]); shade[key] = COL.get(key[0], ['#999999'])[min(n, 1)]
    info = [[k[0], c, shade[k]] for k, c in cnt.items()]
    for o in sd['f']:
        c = solid_col or shade[shape_key(V, o)]
        for a, b in zip(o[1:-1], o[2:]): tris.append([o[0], a, b]); cols.append(c)
        edges += [[o[i], o[(i + 1) % len(o)]] for i in range(len(o))]
    return {'v': np.round(V, 6).tolist(), 't': tris, 'c': cols, 'e': edges, 'a': alpha, 'kinds_info': info}
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def mesh_of(mf, col, alpha=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 6).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': alpha}
dots = lambda P: {'dots': np.round(np.asarray(P), 6).tolist()}

AX = np.array([0.0, 1.0, (1 + 5 ** .5) / 2]); AX /= np.linalg.norm(AX)          # a five-fold axis (an icosahedron corner direction)
scenes = []
for nm in order: scenes.append({'title': nm, 'parts': [faces_mesh(solids[nm])], 'E': None})
for inner, outer in [('DICTO TPP', 'DICTO DPHP'), ('DICTO TQP', 'DICTO TQH')]:
    Vi = np.array(solids[inner]['v']); Hn = np.array([[x.f() for x in n] + [d.f()] for n, d in solid(chain[outer])])
    out = [v for v in Vi if np.max(Hn[:, :3] @ v - Hn[:, 3]) > 1e-9]
    scenes.append({'title': f'{inner} in {outer}', 'parts': [faces_mesh(solids[inner]), faces_mesh(solids[outer], 0.18, '#bfc7cc'), dots(out)], 'E': None})
PAL = ['#2f6fb0', '#c4553a', '#3f9a5b', '#7a4fa0', '#e0ae2c']
for inner, outer in [('DICTO OG', 'DICTO KRE'), ('DICTO KRE', 'DICTO PHE'), ('DICTO PHE', 'DICTO TPP'),
                     ('DICTO TPH', 'DICTO OG'), ('DICTO TQH', 'DICTO TPH'), ('DICTO TQHD', 'DICTO TQP')]:
    Vi = np.array(solids[inner]['v']); Hout = hull(solids[outer]['v']); Hin = hull(Vi); parts = [faces_mesh(solids[inner], 1.0, '#d8d2c4')]
    kinds = {}
    for o in solids[inner]['f']:
        P = Vi[o]; c = P.mean(0)
        if c @ AX / np.linalg.norm(c) < np.cos(np.radians(38)): continue
        pc = (hull(np.vstack([np.zeros(3), 3 * P])) ^ Hout) - Hin; vol = round(pc.volume(), 6)
        key = (len(o), vol); kinds.setdefault(key, PAL[len(kinds) % len(PAL)])
        parts.append(mesh_of(pc, kinds[key]))
    scenes.append({'title': f'{inner} to {outer}', 'parts': parts, 'E': None, 'kinds': [[k[0], k[1], c] for k, c in kinds.items()]})
R = max(np.linalg.norm(np.array(s['v']), axis=1).max() for s in solids.values())
for s in scenes: s['E'] = round(R * 1.06, 4)
html = '''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}canvas{display:block}</style></head><body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script>
const SC = __D__;
const r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(1200, 1200); r.setClearColor(0x000000, 0); document.body.append(r.domElement);
const scene = new THREE.Scene(); const ax = new THREE.Vector3(__AX__);
const dir = ax.clone().applyAxisAngle(new THREE.Vector3(1, 0, 0), 0.30).applyAxisAngle(new THREE.Vector3(0, 1, 0), 0.22).normalize();
scene.add(new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)); const F = new THREE.DirectionalLight(0xffffff, 0.40); F.position.copy(dir.clone().multiplyScalar(6)); scene.add(F);
const L = new THREE.DirectionalLight(0xffffff, 0.62); L.position.copy(dir.clone().multiplyScalar(4).add(new THREE.Vector3(-2, 3, 1))); scene.add(L);
let grp = null, cam = null;
window.show = (i) => { if (grp) scene.remove(grp); const s = SC[i]; const E = s.E; cam = new THREE.OrthographicCamera(-E, E, E, -E, 0.1, 50);
  cam.up.set(0, 1, 0); cam.position.copy(dir.clone().multiplyScalar(10)); cam.lookAt(0, 0, 0); grp = new THREE.Group();
  for (const d of s.parts) {
    if (d.dots) { for (const p of d.dots) { if (p[0] * dir.x + p[1] * dir.y + p[2] * dir.z < 0) continue; const m = new THREE.Mesh(new THREE.SphereGeometry(E * 0.02, 14, 10), new THREE.MeshBasicMaterial({ color: 0xd11f1f, depthTest: false })); m.position.set(...p); m.renderOrder = 9; grp.add(m); } continue; }
    const g = new THREE.BufferGeometry(); const p = new Float32Array(d.t.length * 9), c = new Float32Array(d.t.length * 9); let k = 0;
    d.t.forEach((tr, ti) => { const col = new THREE.Color(d.c[ti]); for (const j of tr) { p[k] = d.v[j][0]; p[k + 1] = d.v[j][1]; p[k + 2] = d.v[j][2]; c[k] = col.r; c[k + 1] = col.g; c[k + 2] = col.b; k += 3; } });
    g.setAttribute('position', new THREE.BufferAttribute(p, 3)); g.setAttribute('color', new THREE.BufferAttribute(c, 3)); g.computeVertexNormals();
    const glass = d.a < 1; grp.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, metalness: 0.05, flatShading: true, transparent: glass, opacity: d.a, depthWrite: !glass, side: THREE.DoubleSide })));
    let eg;
    if (d.e) { const q = new Float32Array(d.e.length * 6); d.e.forEach((e, n) => { q.set(d.v[e[0]], n * 6); q.set(d.v[e[1]], n * 6 + 3); }); eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.BufferAttribute(q, 3)); }
    else eg = new THREE.EdgesGeometry(g, 10);
    grp.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x2b261e, transparent: true, opacity: glass ? 0.3 : 0.85 })));
  }
  scene.add(grp); r.render(scene, cam); return SC.length; };
</script></body></html>'''
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'family.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))).replace('__AX__', ','.join(f'{x:.6f}' for x in AX)))
json.dump([{'title': s['title'], 'kinds': s.get('kinds'), 'face_kinds': s['parts'][0].get('kinds_info')} for s in scenes], open(os.path.join(HERE, 'renders', 'family-labels.json'), 'w'), indent=1)
print('family.html', len(scenes), 'scenes; R', round(R, 4))
