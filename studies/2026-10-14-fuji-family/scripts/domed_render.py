# Render data for the domed icosahedron (DICTO, 2026-10-14): (a) the 20 domed units pulled apart; (b) faceted: each unit cut into the
# icosahedron's face pyramid (cyan) and a dome cap (gold), pulled apart. Writes paper/figures/domed.json. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
V = np.array([(ico[a] + ico[b]) / 2 for a, b in E]); V /= np.linalg.norm(V[0])
H = ConvexHull(V); F = []
for e in np.unique(np.round(H.equations, 9), axis=0):
    F.append(list(np.where(np.abs(V @ e[:3] + e[3]) < 1e-7)[0]))
tris = [f for f in F if len(f) == 3]; pens = [f for f in F if len(f) == 5]
pc = [V[f].mean(0) for f in pens]
def solids(kind):
    out = []
    for f in tris:
        tips = [c for c, p in zip(pc, pens) if len(set(p) & set(f)) == 2]
        if kind == 'domed': out.append(('w1', np.vstack([np.zeros(3), V[f], tips])))
        else: out += [('w0', np.vstack([np.zeros(3), tips]))]
    return out
res = {}
for kind, ex in (('domed', 0.45), ('faceted', 0.45)):
    verts, faces, tags = [], [], []
    for tag, P in solids(kind):
        c = P.mean(0); Y = P + c / np.linalg.norm(c) * ex * (1.6 if tag == 'w2' else 1.0); h = ConvexHull(Y); b = len(verts); verts += Y.tolist()
        for e in np.unique(np.round(h.equations, 9), axis=0):
            on = np.where(np.abs(Y @ e[:3] + e[3]) < 1e-7)[0]; cc = Y[on].mean(0); a = Y[on[0]] - cc; a /= np.linalg.norm(a); bb = np.cross(e[:3], a)
            faces.append([int(b + i) for i in on[np.argsort(np.arctan2((Y[on] - cc) @ bb, (Y[on] - cc) @ a))]]); tags.append(tag)
    res[kind] = dict(v=verts, f=faces, t=tags)
json.dump(res, open(os.path.join(ROOT, 'paper', 'figures', 'domed.json'), 'w')); print({k: len(v['f']) for k, v in res.items()})
