# Builds the RAW of krp-core's src/polyhedra/star-cores-solids.js: D106-D109 from DICTO Solids v7 and Kagemusha's crests (t = 2), after
# research studies 2026-11-01-star-cores-d/scripts/kagemusha_variants.py (same notch pieces).
import json, sys, math, numpy as np
from scipy.spatial import ConvexHull
DS, OUT = sys.argv[1], sys.argv[2]   # usage: pv_solids.py <DICTO Solids v7 solids dir> <out raw.json>, pasted as RAW into krp-core
def load(n):
    d = json.load(open(f'{DS}/dicto-{n}.json'))
    return d, np.array([[float(x) for x in v['decimal']] for v in d['vertices']]), d['faces']
R = lambda x: round(float(x), 12) + 0.0
RAW = {}
for key, n, nm in [('DICTO_CUBE_PEARL', 'cube-pearl', 'Cube Pearl'), ('DICTO_GOLDEN_CLASP', 'golden-clasp', 'Golden Clasp'),
                   ('DICTO_HAMLET', 'hamlet', 'Hamlet'), ('DICTO_OPHELIA', 'ophelia', 'Ophelia')]:
    d, V, F = load(n); assert d['name'] == nm
    RAW[key] = dict(name=nm, vertices=[[R(x) for x in v] for v in V], faces=F)
# Kagemusha (D86, file dicto-shadow-17) about its corner centroid, its five notches (reflex edges)
d, V0, F0 = load('shadow-17'); V0 = V0 - V0.mean(0); t = 2.0
def finfo(f):
    P = V0[f]; n = np.zeros(3)
    for i in range(len(f)): n += np.cross(P[i], P[(i + 1) % len(f)])
    n /= np.linalg.norm(n); return n, float(n @ P.mean(0))
FI = [finfo(f) for f in F0]
E = {}
for i, f in enumerate(F0):
    for k in range(3): E.setdefault(tuple(sorted((f[k], f[(k + 1) % 3]))), []).append(i)
runs = lambda i, e: F0[i][(F0[i].index(e[0]) + 1) % 3] == e[1]
notches = [(e, i, j) for e, (i, j) in E.items() if np.cross(FI[i][0], FI[j][0]) @ ((V0[e[1]] - V0[e[0]]) if runs(i, e) else (V0[e[0]] - V0[e[1]])) < -1e-12]
assert len(notches) == 5
tip = lambda i: t * FI[i][1] * FI[i][0]
def hull_loops(Q):
    h = ConvexHull(Q); g = {}
    for sm, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq, 7)), (eq, set()))[1].update(sm.tolist())
    out = []
    for eq, ids in g.values():
        ids = sorted(ids); P = Q[ids]; c = P.mean(0); u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(eq[:3], u)
        out.append([ids[k] for k in np.argsort([math.atan2((p - c) @ w, (p - c) @ u) for p in P])])
    return out
class Mesh:
    def __init__(s): s.V, s.F, s.C = [], [], []
    def idx(s, p):
        for k, q in enumerate(s.V):
            if np.linalg.norm(q - p) < 1e-9: return k
        s.V.append(np.array(p)); return len(s.V) - 1
    def add(s, Q, loops, col):
        for L in loops: s.F.append([s.idx(Q[k]) for k in L]); s.C.append(col)
    def fuse(s):
        # faces where two parts meet (the same corners twice) are inside: drop both; check the rest is closed and oriented
        from collections import Counter
        cnt = Counter(tuple(sorted(f)) for f in s.F)
        keep = [k for k, f in enumerate(s.F) if cnt[tuple(sorted(f))] == 1]
        s.F = [s.F[k] for k in keep]; s.C = [s.C[k] for k in keep]
        de = Counter((f[k], f[(k + 1) % len(f)]) for f in s.F for k in range(len(f)))
        assert all(c == 1 and de[(b, a)] == 1 for (a, b), c in de.items()), 'not closed'
        V = np.array(s.V); vol = sum(np.linalg.det(np.array([V[f[0]], V[f[k]], V[f[k + 1]]])) for f in s.F for k in range(1, len(f) - 1)) / 6
        assert len(s.V) - len(de) // 2 + len(s.F) == 2
        return vol
GOLD, TEAL = 0xd9a520, 0x2bb7c4
crest_pieces = {}
for variant in ('conjoined', 'sloping'):
    pcs = []
    for e, i, j in notches:
        a, b = V0[e[0]], V0[e[1]]; c = V0[[v for v in F0[i] if v not in e][0]]; c2 = V0[[v for v in F0[j] if v not in e][0]]
        if variant == 'conjoined': pcs.append(np.vstack([a, b, c, c2, tip(i), tip(j)]))
        else:
            m = np.cross(b - a, -a); m /= np.linalg.norm(m); X = []
            for cc, T in ((c, tip(i)), (c2, tip(j))): X.append(cc + (cc @ m) / ((cc - T) @ m) * (T - cc))
            assert np.linalg.norm(X[0] - X[1]) < 1e-9
            pcs.append(np.vstack([a, b, c, X[0]])); pcs.append(np.vstack([a, b, c2, X[0]]))
    crest_pieces[variant] = pcs
vols = {k: [ConvexHull(Q).volume for Q in v] for k, v in crest_pieces.items()}
VK = sum(np.linalg.det(np.array([V0[f[0]], V0[f[1]], V0[f[2]]])) for f in F0) / 6
print('Kagemusha volume', VK, 'maedate', vols['conjoined'][0] / VK, 'kuwagata', vols['sloping'][0] / VK)
for key, variant, nm in [('KAGEMUSHA_MAEDATE', 'conjoined', 'Kagemusha with MAEDATE'), ('KAGEMUSHA_KUWAGATA', 'sloping', 'Kagemusha with KUWAGATA')]:
    M = Mesh()
    M.add(V0, [list(f) for f in F0], GOLD)
    for Q in crest_pieces[variant]: M.add(Q, hull_loops(Q), TEAL)
    v = M.fuse(); assert abs(v - VK - sum(vols[variant])) < 1e-9, (v, VK, sum(vols[variant])); print(key, 'volume', v)
    RAW[key] = dict(name=nm, vertices=[[R(x) for x in v] for v in M.V], faces=M.F, faceColours=M.C, parts=1 + len(crest_pieces[variant]))
# the single pieces (one notch), each centred on its own corners
for key, variant, nm, k in [('DICTO_MAEDATE', 'conjoined', 'MAEDATE', 1), ('DICTO_KUWAGATA', 'sloping', 'KUWAGATA', 2)]:
    M = Mesh(); Qs = crest_pieces[variant][:k]; c = np.vstack(Qs).mean(0)
    for Q in Qs: M.add(Q - c, hull_loops(Q - c), TEAL)
    v = M.fuse(); assert abs(v - sum(vols[variant][:k])) < 1e-12; print(key, 'volume', v)
    RAW[key] = dict(name=nm, vertices=[[R(x) for x in v] for v in M.V], faces=M.F, faceColours=M.C, parts=k)
json.dump(RAW, open(OUT, 'w'), separators=(',', ':'))
for k, v in RAW.items(): print(k, len(v['vertices']), len(v['faces']))
