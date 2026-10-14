# Cycles world, stage 1 (DICTO, 2026-10-14): the convex stations already inside the checked builds (fused-shells study), measured.
# For each closed convex stage: hull of its pieces, face shapes, edge(s), circumradius, inradius, volume, and the size against the
# starting icosahedron. DICTO · dictospheres.com
import json, os, itertools
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FS = os.path.join(ROOT, '..', '2026-10-13-fused-shells')
facts = json.load(open(os.path.join(FS, 'stages-facts.json'))); pieces = json.load(open(os.path.join(FS, 'pieces.json')))
def measure(P):
    h = ConvexHull(P); V = P[h.vertices]; V = np.array([v for i, v in enumerate(V) if all(np.linalg.norm(v - w) > 1e-6 for w in V[:i])])
    eq = np.unique(np.round(h.equations, 6), axis=0); edges = set()
    for e in eq:
        on = [i for i, v in enumerate(V) if abs(v @ e[:3] + e[3]) < 1e-5]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        o = [on[k] for k in np.argsort([np.arctan2((V[i] - c) @ b, (V[i] - c) @ a) for i in on])]
        for i in range(len(o)): edges.add(round(float(np.linalg.norm(V[o[i]] - V[o[(i + 1) % len(o)]])), 5))
    r = np.linalg.norm(V, axis=1)
    return dict(corners=len(V), edges=sorted(edges), circumradius=[round(float(r.min()), 5), round(float(r.max()), 5)],
                inradius=[round(float(-eq[:, 3].max()), 5), round(float(-eq[:, 3].min()), 5)], volume=round(float(h.volume), 6))
out = {}
for build, L in facts.items():
    P = pieces[build]
    for i, s in enumerate(L):
        if not s.get('convex') or s.get('partial'): continue
        pts = np.array([q for j in s['pieces'] for q in P[j][1]], float)
        out[f'{build}#{i}'] = dict(faces=s['faceShapes'], last=s['groups'][-1], **measure(pts))
base = out['dharma.cycle#0']['circumradius'][1]
for k, v in out.items(): v['size_vs_start'] = round(v['circumradius'][1] / base, 5)
json.dump(out, open(os.path.join(ROOT, 'stations-measured.json'), 'w'), indent=1)
for k, v in out.items(): print(k, v['faces'], 'edges', v['edges'], 'R', v['circumradius'], 'x', v['size_vs_start'])
