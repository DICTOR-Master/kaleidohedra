# The 13s side by side (paper facts): for each 13, its centre and twelve (sizes, distances, how they touch) and each kit's totals.
# Usage: python3 papers/thirteens/fig/facts.py thirteens-raw.json > facts.json
import sys, json, itertools, numpy as np
from scipy.spatial import ConvexHull
D = json.load(open(sys.argv[1]))
MAIN = {'icosa13': ('pieces', 'ico'), 'dodeca13': ('pieces', 'dodeca'), 'bodhi': ('seed', None), 'unity': ('open', None), 'dictoStar': ('star', ('centre', 'dodeca')),
        'deshi': ('deshi', None), 'rd13': ('plain', None)}
def edge(V, F): return float(np.mean([np.linalg.norm(np.array(V[f[i]]) - np.array(V[f[(i + 1) % len(f)]])) for f in F for i in range(len(f))]))
def vol(V, F):
    V = np.array(V, float); c = V.mean(0)
    return abs(sum(np.linalg.det(np.array([V[f[0]] - c, V[f[i]] - c, V[f[i + 1]] - c])) for f in F for i in range(1, len(f) - 1)) / 6)
def contact(A, B):
    VA, FA = np.array(A[1]), A[2]; VB = np.array(B[1])
    shared = [i for i, v in enumerate(VA) if np.min(np.linalg.norm(VB - v, axis=1)) < 1e-4]
    if not shared: return None
    s = set(shared)
    if any(set(f) <= s for f in FA): return 'face'
    return 'edge' if len(shared) >= 2 else 'corner'
out = {}
for kind, (view, roles) in MAIN.items():
    P = D[kind][view]
    if roles: P = [p for p in P if p[0] in roles]
    P = P[:13]
    ci = next((i for i, p in enumerate(P) if p[0] in ('centre', 'rdCentre')), 0)   # the centre (Bodhi lists it last)
    P = [P[ci]] + P[:ci] + P[ci + 1:]
    c = np.array(P[0][1]).mean(0)
    cen, twelve = P[0], P[1:]
    d = [float(np.linalg.norm(np.array(p[1]).mean(0) - c)) for p in twelve]
    cc = [contact(cen, p) for p in twelve]
    tt = [contact(a, b) for a, b in itertools.combinations(twelve, 2)]
    allV = np.array([v for p in P for v in p[1]])
    hull = ConvexHull(allV).volume
    out[kind] = {
        'centre': {'role': cen[0], 'edge': edge(cen[1], cen[2]), 'faces': len(cen[2]), 'volume': vol(cen[1], cen[2])},
        'twelve': {'role': twelve[0][0], 'edge': edge(twelve[0][1], twelve[0][2]), 'faces': len(twelve[0][2]), 'volume': vol(twelve[0][1], twelve[0][2])},
        'distance': [min(d), max(d)],
        'centre_contacts': {k: cc.count(k) for k in set(cc)},
        'twelve_contacts': {str(k): tt.count(k) for k in set(tt)},
        'kits': {},
    }
    for kit, pieces in D[kind].items():
        if kit == 'blocks': continue
        V = np.array([v for p in pieces for v in p[1]]); total = sum(vol(p[1], p[2]) for p in pieces); hv = ConvexHull(V).volume
        types = sorted(set(p[0] for p in pieces))
        out[kind]['kits'][kit] = {'pieces': len(pieces), 'roles': {r: sum(1 for p in pieces if p[0] == r) for r in types}, 'volume': total, 'hull': hv, 'ratio': total / hv}
json.dump(out, sys.stdout, indent=1)
