# Figures for the Hecatodihedron paper (DICTO, 2026-10-14): (a) the solid; (b) the same down a five-fold axis; (c) the truncated
# icosahedron and its 20 Shields pulled apart. Colours as the Dharma figures: pentagons gold, rhombi cyan, triangles wisteria; the
# truncated icosahedron green, Shields wisteria. DICTO · dictospheres.com
import json, sys, os
import numpy as np
from scipy.spatial import ConvexHull
S = json.load(open(sys.argv[1]))['TRANS_DHARMA_80']; V = np.array(S['v'], float); V -= V.mean(0)
SH = [np.array(p, float) for p in json.load(open(sys.argv[2]))]
def faces_of(P):
    h = ConvexHull(P); planes = []
    for e in h.equations:
        if not any(np.abs(e - q).max() < 1e-4 for q in planes): planes.append(e)
    out = []
    for e in planes:
        on = np.where(np.abs(P @ e[:3] + e[3]) < 1e-4)[0]; c = P[on].mean(0); a = P[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        out.append(on[np.argsort(np.arctan2((P[on] - c) @ b, (P[on] - c) @ a))])
    return out
def mesh(items):
    v, f, t = [], [], []
    for tag, P, F in items:
        b = len(v); v += P.tolist()
        for fa in F: f.append([int(b + i) for i in fa]); t.append(tag(len(fa)) if callable(tag) else tag)
    return dict(v=v, f=f, t=t)
TF = faces_of(V)
solid = mesh([(lambda n: {5: 'w2', 4: 'w0', 3: 'w1'}[n], V, TF)])
inner = V[np.abs(np.linalg.norm(V, axis=1) - np.linalg.norm(V, axis=1).max()) > 1e-4]
items = [('w3', inner, faces_of(inner))]
for P in SH:
    d = P.mean(0) / np.linalg.norm(P.mean(0)) * 0.35; Q = P + d; items.append(('w1', Q, faces_of(Q)))
json.dump({'tih': solid, 'tih_apart': mesh(items)}, open(os.path.join(os.path.dirname(__file__), 'tih-fig.json'), 'w'))
print('faces', len(TF), 'shields', len(SH))
