# DICTO 2026-10-20: figures for the OG polytypes paper. Float copies of the exact solids of polytype_exact.py (same frame, same layer
# maps: c = translation 2R(1,0,0), h = mirror in the top plane). Side views with the stacking axis (1,1,1) upright; one row of octahedra
# per layer along R(1,-1,0); solids in their first orientation gold, mirror twins blue; twin (h) layers as faint red planes.
# Writes renders/stacks.html (three.js, window.show(i)) and renders/stacks-labels.json; shots: ../2026-10-19-five-fold-octet/shots.mjs.
#   scenes: OG stacks 3C, 2H, 6H, Fibonacci; OTT and DBT on the Fibonacci stacking; the golden envelope across a c and an h layer
#   (overlap in red).  usage: python3 polytype_figs.py <ocd-octet scripts> <gyrated-octet study>
import sys, os, json
import numpy as np, manifold3d as m3
sys.path.insert(0, sys.argv[1]); GYR = sys.argv[2]
from q5 import q, qf
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); OCT = os.path.join(sys.argv[1], '..', 'data')
PHI = (1 + 5 ** .5) / 2; R = 2 * PHI / 3
L = lambda f: np.array([[qf(q(c)) for c in v] for v in json.load(open(f))['V']])
OG = L(os.path.join(OCT, 'step1-ocd-exact.json')); DBT = L(os.path.join(GYR, 'dbt-exact.json')); OTT = L(os.path.join(GYR, 'cut8-exact.json'))
def hull_faces(V):
    h = ConvexHull(V); E = np.unique(np.round(h.equations, 7), axis=0); F = []
    for e in E:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; P = V[idx]; c = P.mean(0)
        a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return F
# the envelope: the DBT without its two pole cuts
eq = [e for e in np.unique(np.round(ConvexHull(DBT).equations, 7), axis=0) if not np.allclose(np.abs(e[:3]), abs(e[0]))]
from scipy.spatial import HalfspaceIntersection
RT = HalfspaceIntersection(np.array(eq), np.zeros(3)).intersections; RT = RT[np.unique(np.round(RT, 7), axis=0, return_index=True)[1]]
assert len(RT) == 32
SOLID = {'OG': OG, 'OTT': OTT, 'DBT': DBT, 'RT': RT}; FACES = {k: hull_faces(V) for k, V in SOLID.items()}
MIR = np.eye(3) - 2 / 3 * np.ones((3, 3)); Tc = (np.eye(3), np.array([2 * R, 0, 0])); M0 = (MIR, np.full(3, 2 * R / 3))
def comp(F, G): return (F[0] @ G[0], F[0] @ G[1] + F[1])
TcD = (np.eye(3), -Tc[1]); M0D = (MIR, -M0[1])                                     # the steps taken downward (for a mirrored layer)
def maps(word):
    out = [(np.eye(3), np.zeros(3))]
    for w in word:
        up = np.allclose(out[-1][0], np.eye(3))
        out.append(comp(out[-1], (Tc if up else TcD) if w == 'c' else (M0 if up else M0D)))
    return out
N = np.ones(3) / 3 ** .5; E1 = np.array([1, -1, 0]) / 2 ** .5; E2 = np.cross(N, E1)          # upright axis, row direction, view direction
GOLD, BLUE = '#e0ae2c', '#4f8fd6'
def solid_part(V, F, col, alpha=1.0):
    tris = [[o[0], a, b] for o in F for a, b in zip(o[1:-1], o[2:])]
    return {'v': np.round(V, 5).tolist(), 't': tris, 'c': [col] * len(tris), 'e': [[o[i], o[(i + 1) % len(o)]] for o in F for i in range(len(o))], 'a': alpha}
def plane_part(h, half_w, col='#d65a5a', alpha=0.16):
    c = h * N; P = [c + s * half_w * E1 + t * 1.2 * E2 for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return {'v': np.round(P, 5).tolist(), 't': [[0, 1, 2], [0, 2, 3]], 'c': [col] * 2, 'e': None, 'a': alpha}
def stack(word, solid='OG', row=2):
    parts = []; Ms = maps(word); xs = []
    for k, (A, b) in enumerate(Ms):
        # the row of octahedra through this layer's image of the origin, along the in-layer lattice vector R(1,-1,0)
        # the row of this layer nearest the picture plane, within the window: the A/B/C offsets show as sideways shifts
        cs = [A @ (R * np.array([a_, b_, -a_ - b_])) + b for a_ in range(-8, 9) for b_ in range(-8, 9)]
        d0 = min(abs(c @ E2) for c in cs)
        for c in sorted([c for c in cs if abs(c @ E2) - d0 < 1e-6 and abs(c @ E1) <= (row + 0.6) * R * 2 ** .5], key=lambda c: c @ E1):
            V = SOLID[solid] @ A.T + c; xs.append(c)
            parts.append(solid_part(V, FACES[solid], GOLD if np.allclose(A, np.eye(3)) else BLUE))
    span = (row + 1.2) * R * 2 ** .5
    for k, w in enumerate(word):
        if w == 'h': parts.append(plane_part((2 * k + 1) * R / 3 ** .5, span))
    xs = np.array(xs); ctr = np.array([0.0, (xs @ N).mean()])
    return parts, ctr
scenes = []
fibw = 'c'
for _ in range(6): fibw = ''.join('ch' if x == 'c' else 'c' for x in fibw)
for nm, w in (('3C (octet)', 'cccccc'), ('2H (gyrated octet)', 'hhhhhh'), ('6H', 'hcchcc'), ('Fibonacci', fibw[:6])):
    p, ctr = stack(w); scenes.append({'title': nm, 'sub': ' '.join(w), 'parts': p, 'ctr': ctr.tolist()})
for s in ('OTT', 'DBT'):
    p, ctr = stack(fibw[:6], s); scenes.append({'title': f'{s}, Fibonacci', 'sub': ' '.join(fibw[:6]), 'parts': p, 'ctr': ctr.tolist()})
# the golden envelope: two envelopes across one layer boundary, c (they touch) and h (the tips overlap, in red)
for w in ('c', 'h'):
    Ms = maps(w); parts = []; Vs = []
    for (A, b) in Ms:
        V = RT @ A.T + b; Vs.append(V); parts.append(solid_part(V, FACES['RT'], GOLD if np.allclose(A, np.eye(3)) else BLUE, 0.25))
    ov = m3.Manifold.hull_points(Vs[0]) ^ m3.Manifold.hull_points(Vs[1]); vol = ov.volume()
    if vol > 1e-9:
        me = ov.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
        parts.append({'v': np.round(P, 5).tolist(), 't': T, 'c': ['#d11f1f'] * len(T), 'e': None, 'a': 1.0})
    parts.append(plane_part(R / 3 ** .5, 2.2, '#d65a5a' if w == 'h' else '#9aa0a6', 0.14))
    c = np.array([np.mean([V @ E1 for V in Vs]), np.mean([V @ N for V in Vs])])
    scenes.append({'title': f'Envelope across a {w} layer', 'sub': f'overlap {vol:.6f}' if vol > 1e-9 else 'they meet face to face', 'parts': parts, 'ctr': c.tolist()})
# one scale for the stacks, one for the envelope pair
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts'] if p['e'] is not None])
    s['E'] = round(float(max(np.abs(pts @ E1 - s['ctr'][0]).max(), np.abs(pts @ N - s['ctr'][1]).max())) * 1.06, 4)
Es = max(s['E'] for s in scenes[:6]); [s.__setitem__('E', Es) for s in scenes[:6]]
html = '''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}canvas{display:block}</style></head><body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script>
const SC = __D__, N = new THREE.Vector3(__N__), E1 = new THREE.Vector3(__E1__), E2 = new THREE.Vector3(__E2__);
const r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(1200, 1200); r.setClearColor(0x000000, 0); document.body.append(r.domElement);
const scene = new THREE.Scene(); const dir = E2.clone().multiplyScalar(-1).applyAxisAngle(N, 0.18).addScaledVector(N, 0.12).normalize();
scene.add(new THREE.HemisphereLight(0xffffff, 0xa89f8c, 0.5)); const F = new THREE.DirectionalLight(0xffffff, 0.45); F.position.copy(dir.clone().multiplyScalar(6)); scene.add(F);
const L = new THREE.DirectionalLight(0xffffff, 0.8); L.position.copy(dir.clone().multiplyScalar(4).addScaledVector(N, 4).addScaledVector(E1, -2)); scene.add(L);
let grp = null;
window.show = (i) => { if (grp) scene.remove(grp); const s = SC[i], E = s.E; const cam = new THREE.OrthographicCamera(-E, E, E, -E, -50, 50);
  const ctr = E1.clone().multiplyScalar(s.ctr[0]).addScaledVector(N, s.ctr[1]);
  cam.up.copy(N); cam.position.copy(ctr.clone().addScaledVector(dir, 20)); cam.lookAt(ctr); grp = new THREE.Group();
  for (const d of s.parts) {
    const g = new THREE.BufferGeometry(); const p = new Float32Array(d.t.length * 9), c = new Float32Array(d.t.length * 9); let k = 0;
    d.t.forEach((tr, ti) => { const col = new THREE.Color(d.c[ti]); for (const j of tr) { p[k] = d.v[j][0]; p[k + 1] = d.v[j][1]; p[k + 2] = d.v[j][2]; c[k] = col.r; c[k + 1] = col.g; c[k + 2] = col.b; k += 3; } });
    g.setAttribute('position', new THREE.BufferAttribute(p, 3)); g.setAttribute('color', new THREE.BufferAttribute(c, 3)); g.computeVertexNormals();
    const glass = d.a < 1; grp.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, metalness: 0.05, flatShading: true, transparent: glass, opacity: d.a, depthWrite: !glass, side: THREE.DoubleSide })));
    if (d.e) { const q = new Float32Array(d.e.length * 6); d.e.forEach((e, n) => { q.set(d.v[e[0]], n * 6); q.set(d.v[e[1]], n * 6 + 3); }); const eg = new THREE.BufferGeometry(); eg.setAttribute('position', new THREE.BufferAttribute(q, 3));
      grp.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x2b261e, transparent: true, opacity: glass ? 0.35 : 0.7 }))); }
  }
  scene.add(grp); r.render(scene, cam); return SC.length; };
</script></body></html>'''
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
f3 = lambda v: ','.join(f'{x:.6f}' for x in v)
open(os.path.join(HERE, 'renders', 'stacks.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))).replace('__N__', f3(N)).replace('__E1__', f3(E1)).replace('__E2__', f3(E2)))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'stacks-labels.json'), 'w'), indent=1)
print('stacks.html', len(scenes), 'scenes; envelope overlap at h:', scenes[-1]['sub'])
