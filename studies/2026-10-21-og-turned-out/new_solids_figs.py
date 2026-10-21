# DICTO 2026-10-21 ("show the new solids"): pictures of the new solids D5-D11 (DICTO's names: faces + face count), each scaled to
# the same size, faces coloured by kind, #18 standard; and the 3-beat shell (beat 4 -> beat 7) cut into towers, drawn apart.
# Float copies of the exact points (golden-long-solids.pkl).   usage: python3 new_solids_figs.py <five-fold-octet dir>
import sys, os, json, pickle, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
sys.path.insert(0, sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
phi = (1 + 5 ** .5) / 2
NAMES = {5: 'DICTO TQP-252', 6: 'DICTO TQ-320', 7: 'DICTO TQP-402', 8: 'DICTO TQ-500', 9: 'DICTO TQD-732', 10: 'DICTO TQHD-662', 11: 'DICTO TQP-672'}
COL = {3: '#d9a441', 4: '#6b3fa0', 5: '#9a78c8', 6: '#8a5a24', 10: '#f0d48a'}
KIND = {3: 'triangles gold', 4: 'quads purple', 5: 'pentagons lilac', 6: 'hexagons bronze', 10: 'decagons pale gold'}
def faces(P):
    H = ConvexHull(P); G = {}
    for s, e in zip(H.simplices, H.equations): G.setdefault(tuple(np.round(e, 8)), set()).update(s)
    out = []
    for ids in G.values():
        ids = list(ids); c = P[ids].mean(0); n = c / np.linalg.norm(c); u = P[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ids.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append(ids)
    return out
def poly_part(P, F, col=None):
    v, t, c = [], [], []
    for f in F:
        o = len(v); v += P[f].tolist(); t += [[int(o), int(o + a), int(o + a + 1)] for a in range(1, len(f) - 1)]; c += [col or COL.get(len(f), '#cccccc')] * (len(f) - 2)
    E = sorted({tuple(sorted((f[a], f[(a + 1) % len(f)]))) for f in F for a in range(len(f))})
    o = len(v); v += P.tolist()
    return {'v': np.round(v, 5).tolist(), 't': t, 'c': c, 'e': [[int(o + a), int(o + b)] for a, b in E], 'a': 1.0}
scenes = []
for k in range(5, 12):
    P = np.array([[x.f() for x in v] for v in D[k]]); P = P[sorted(set(ConvexHull(P).vertices))]; P /= np.linalg.norm(P, axis=1).max()
    F = faces(P); kinds = sorted({len(f) for f in F})
    scenes.append({'title': NAMES[k], 'sub': f'beat {k}: {len(P)} corners, {len(F)} faces', 'parts': [poly_part(P, F)]})
# the 3-beat shell: towers over each face of beat 4, cut by beat 7, drawn apart
B4 = np.array([[x.f() for x in v] for v in D[4]]) * phi ** 4; B7 = np.array([[x.f() for x in v] for v in D[7]]) * phi ** 7
hull = lambda Q: m3.Manifold.hull_points(np.asarray(Q, float)); out7 = hull(B7); R = np.linalg.norm(B7, axis=1).max() * 3
parts = []; cut = m3.Manifold.cube([400, 400, 400]).translate([-200, -200, 0])
for f in faces(B4):
    Fp = B4[f]; cone = hull(np.vstack([Fp * 1e-4, Fp / np.linalg.norm(Fp, axis=1)[:, None] * R]))
    tw = (cone ^ out7) - hull(np.vstack([np.zeros(3), Fp])); d = Fp.mean(0); d /= np.linalg.norm(d)
    if tw.is_empty(): continue
    me = tw.translate(list(d * 0.10 * np.linalg.norm(B7, axis=1).max())).to_mesh()
    parts.append({'v': np.round(np.asarray(me.vert_properties[:, :3]), 5).tolist(), 't': np.asarray(me.tri_verts).tolist(), 'c': [COL.get(len(f), '#ccc')] * len(me.tri_verts), 'e': None, 'a': 1.0})
core = hull(B4); me = core.to_mesh()
parts.append({'v': np.round(np.asarray(me.vert_properties[:, :3]), 5).tolist(), 't': np.asarray(me.tri_verts).tolist(), 'c': ['#f0d48a'] * len(me.tri_verts), 'e': None, 'a': 1.0})
scenes.append({'title': 'The 3-beat shell', 'sub': 'beat 4 to beat 7: 200 towers, drawn apart', 'parts': parts})
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(sys.argv[1], 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'new-solids.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'new-solids-labels.json'), 'w'), indent=1)
print('new-solids.html', len(scenes))
