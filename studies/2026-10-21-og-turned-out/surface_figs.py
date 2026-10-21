# DICTO 2026-10-21: pictures of the surface patterns (float copies of the exact solids in surface-patterns.json and golden-exact.json),
# #18 standard. Scenes: the nine boundary solids, faces coloured by kind (orbit of the 60 rotations), all seen the same way; then the
# ribbons of phi^2 TQH: the shell-3 towers on its 60 trapezoids on the TQH, and one ribbon (two trapezoids) with its two towers close up.
# Run on dicto-node (manifold3d); renderer and camera as golden_figs.py. Then: node shots.mjs renders/surface.html renders/surface-shots;
# python3 surface_compose.py.
import os, json
import numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'surface-patterns.json')))['solids']; Gd = json.load(open(os.path.join(HERE, 'golden-exact.json')))
COL = {('triangle', 0): '#a77be0', ('triangle', 1): '#d9c2f5', 'pentagon': '#d9a334', 'hexagon': '#f0d48a', 'kite': '#a77be0', 'rhombus': '#5fb3a8', 'trapezoid': '#e0603a'}
def colour(sh, tri_seen):
    if 'triangle' in sh: return COL[('triangle', min(tri_seen, 1))]
    for k in ('pentagon', 'hexagon', 'kite', 'rhombus', 'trapezoid'):
        if k in sh: return COL[k]
    return '#cccccc'
def solid_part(nm):
    s = P[nm]; V = np.array(s['corners_float']); V = V / np.linalg.norm(V, axis=1).max()
    kc, tri = {}, 0
    for i, k in enumerate(s['kinds']):
        kc[i] = colour(k['shape'], tri); tri += 'triangle' in k['shape']
    T, C, E = [], [], []
    for f, kd in zip(s['faces_idx'], s['face_kind']):
        for j in range(1, len(f) - 1): T.append([f[0], f[j], f[j + 1]]); C.append(kc[kd])
        E += [[a, b] for a, b in zip(f, f[1:] + f[:1])]
    return {'v': np.round(V, 5).tolist(), 't': T, 'c': C, 'e': E, 'a': 1.0}
scenes = []; add = lambda t, s, parts, E=None: scenes.append({'title': t, 'sub': s, 'parts': parts, 'E': E})
SUB = {'ID': 'icosidodecahedron', 'RT': 'rhombic triacontahedron', 'GTI': 'DICTO GTI', 'FPD': 'DICTO FPD', 'OG': 'DICTO OG', 'TPH': 'DICTO TPH', 'TQH': 'DICTO TQH', 'TQP': 'DICTO TQP', 'TQHD': 'DICTO TQHD'}
for nm in ['ID', 'RT', 'GTI', 'FPD', 'OG', 'TPH', 'TQH', 'TQP', 'TQHD']: add(nm, SUB[nm], [solid_part(nm)], 1.04)
# the ribbons: shell 3 of the OG turned out (phi^2 TQH -> phi^4 TQHD), towers on the trapezoids
B = {k: np.array(v, float) for k, v in Gd['boundaries_float'].items()}; A_, O_ = B['phi^2 TQH'], B['phi^4 TQHD']
hull = lambda Q: m3.Manifold.hull_points(np.asarray(Q, float))
def faces(Q):
    h = ConvexHull(Q); g = {}
    for simp, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    out = []
    for ix in g.values():
        ix = list(ix); F = Q[ix]; c = F.mean(0); n = np.cross(F[1] - F[0], F[2] - F[0]); u = F[0] - c; w = np.cross(n, u)
        out.append([ix[k] for k in np.argsort(np.arctan2((F - c) @ w, (F - c) @ u))])
    return out
FA = faces(A_); quads = [f for f in FA if len(f) == 4]; outer = hull(O_); R = np.linalg.norm(O_, axis=1).max() * 3
def tower(f):
    F = A_[f]; cone = hull(np.vstack([F * 0.0001, F / np.linalg.norm(F, axis=1)[:, None] * R]))
    nn = np.cross(F[1] - F[0], F[2] - F[0]); nn /= np.linalg.norm(nn); nn = nn if nn @ F[0] > 0 else -nn
    return (cone ^ outer).trim_by_plane(list(nn), float(nn @ F[0]))          # the part beyond the face
def mf_part(mf, col, a=1.0):
    me = mf.to_mesh(); V = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(V, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': a}
pair = None
for i, f in enumerate(quads):
    for j, g in enumerate(quads[i + 1:], i + 1):
        if len(set(f) & set(g)) == 2: pair = (f, g); break
    if pair: break
# one ribbon close up: turn it so that its two-fold axis points to the camera, seam across
ax = np.array([0.62, 0.48, 0.62]); ax /= np.linalg.norm(ax)
def rot(a, t):
    a = a / np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
cam = rot(np.array([0, 1, 0]), 0.22) @ rot(np.array([1, 0, 0]), 0.30) @ ax
f, g = pair; ctr = A_[list(set(f) | set(g))].mean(0); n = ctr / np.linalg.norm(ctr)
sh = list(set(f) & set(g)); sd = A_[sh[1]] - A_[sh[0]]; sd -= (sd @ n) * n; sd /= np.linalg.norm(sd)    # the seam's direction
hp = np.cross(n, sd)                                                                                      # across the ribbon
view = 0.6 * hp + 0.55 * n + 1.0 * sd; view /= np.linalg.norm(view)                                           # oblique, from outside
up_t = np.array([0.0, 1.0, 0.0]) - (np.array([0.0, 1.0, 0.0]) @ cam) * cam; up_t /= np.linalg.norm(up_t)
up_s = n - (n @ view) * view; up_s /= np.linalg.norm(up_s)
Sf = np.array([view, up_s, np.cross(view, up_s)]); Tf = np.array([cam, up_t, np.cross(cam, up_t)]); Rm = Tf.T @ Sf   # view -> camera, ray -> up
tw = [tower(f), tower(g)]
def moved(mf, col, a=1.0):
    p = mf_part(mf, col, a); V = (np.array(p['v']) - ctr) @ Rm.T; p['v'] = np.round(V, 5).tolist(); return p
ring1 = {v for h in FA if len(set(h) & (set(f) | set(g))) > 0 for v in h}
near = [h for h in FA if len(set(h) & ring1) > 0 and h not in (f, g)]
base = []
for h in near + [f, g]:
    V = (A_[h] - ctr) @ Rm.T; k = len(h)
    base.append({'v': np.round(V, 5).tolist(), 't': [[0, j, j + 1] for j in range(1, k - 1)], 'c': [('#f0d48a' if h not in (f, g) else '#e8a090')] * (k - 2), 'e': [[j, (j + 1) % k] for j in range(k)], 'a': 1.0})
half_ = [h for h in (f, g)]; side = [np.sign((A_[h].mean(0) - ctr) @ hp) for h in half_]
tw = [t.translate(list(sg * 0.06 * hp)) for t, sg in zip(tw, side)]                  # drawn a little apart across the seam
add('One ribbon close up', 'two trapezoids across their shorter side, with their two towers', base + [moved(tw[0], '#e0603a'), moved(tw[1], '#f08a5a')])
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts'] if p['v']]); c = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - c).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - c, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'surface.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'surface-labels.json'), 'w'), indent=1)
print('surface.html', len(scenes))
