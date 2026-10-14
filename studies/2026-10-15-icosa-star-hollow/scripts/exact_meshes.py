# Exact meshes for the paper's figures (2026-10-15): every piece of both stories with exact corners (from exact.py / exact_stations.py),
# faces merged into whole polygons (exactly coplanar now, so no stray edges), written as float JSON for the renderer.
import json, numpy as np
from scipy.spatial import ConvexHull
src = open('scripts/exact_stations.py').read()
exec(src.split("out = ['== stations (exact)']")[0])          # builds `pieces` (stations, exact)
stations = pieces
J102 = json.load(open('data/cut102.json'))
def exact_from(m): return [[S(x) for x in v] for v in m['v']]
c102 = {k: [exact_from(m) for m in L] for k, L in J102.items()}
def polys(V):
    W = np.array([[x.f() for x in v] for v in V]); h = ConvexHull(W); groups = []
    for e, t in zip(h.equations, h.simplices):
        for G in groups:
            if G['n'] @ e[:3] > 1 - 1e-9 and abs(G['d'] - e[3]) < 1e-9: G['i'].update(int(i) for i in t); break
        else: groups.append({'n': e[:3], 'd': e[3], 'i': {int(i) for i in t}})
    out = []
    for G in groups:
        idx = sorted(G['i']); Q_ = W[idx]; c = Q_.mean(0); a = Q_[0] - c; a /= np.linalg.norm(a); b = np.cross(G['n'], a)
        out.append([idx[i] for i in np.argsort(np.arctan2((Q_ - c) @ b, (Q_ - c) @ a))])
    return W, out
def dump(G):
    res = {}
    for k, L in G.items():
        res[k] = []
        for V in L:
            W, F = polys(V); res[k].append({'v': np.round(W, 9).tolist(), 'f': F, 'c': np.round(W.mean(0), 9).tolist()})
    return res
json.dump({'stations': dump(stations), 'c102': dump(c102)}, open('data/exact_meshes.json', 'w'))
for nm, G in (('stations', stations), ('c102', c102)):
    print(nm, {k: (len(L), sorted(len(f) for f in polys(L[0])[1])) for k, L in G.items()})
# the Hecatodihedron's own surface for the closed views: whole faces tagged by sides (5 gold, 4 cyan, 3 wisteria, as in the
# Hecatodihedron paper)
D = json.load(open('data/exact_meshes.json'))
allc = list({tuple((x.a, x.b) for x in v): v for L in c102.values() for V in L for v in V}.values())
W, F = polys(allc)
hull_idx = sorted({i for f in F for i in f})
D['hull'] = {'v': np.round(W, 9).tolist(), 'f': F, 'sides': sorted(len(f) for f in F)}
json.dump(D, open('data/exact_meshes.json', 'w'))
print('hull faces', len(F), {n: sum(1 for f in F if len(f) == n) for n in (3, 4, 5)})
