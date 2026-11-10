"""Near-sphere scutoid shell (DICTO 10 Nov: "as a near sphere", core a truncated icosahedron). Inner: truncated icosahedron (TI).
Middle: every hexagon-hexagon edge collapses to a point -> icosidodecahedron (ID) (hexagons -> triangles; the Y points). Outer: each
point reopens ACROSS (T1), the new edge between the two pentagons -> truncated dodecahedron (TD) (pentagons -> decagons).
Cells: 12 'pentagon scutoids' 5 -> 5 -> 10, 20 'hexagon scutoids' 6 -> 3 -> 3. Checks: every face flat; cell volumes add up to
V(TD) - V(TI) (the shell is filled exactly once). Usage: python scutoid_sphere.py [r_mid] [r_out]   (TI circumradius 1)"""
import sys, json, itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def evenperm(v):
    out = []
    for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        for s in itertools.product([1, -1], repeat=3):
            p = (s[0] * v[a], s[1] * v[b], s[2] * v[c]); out.append(p)
    return np.unique(np.round(np.array(out, float), 12), axis=0)
TI = np.vstack([evenperm((0, 1, 3 * phi)), evenperm((1, 2 + phi, 2 * phi)), evenperm((phi, 2, phi ** 3))])
ID = np.vstack([evenperm((0, 0, phi)), evenperm((0.5, phi / 2, phi ** 2 / 2))])
TD = np.vstack([evenperm((0, 1 / phi, 2 + phi)), evenperm((1 / phi, phi, 2 * phi)), evenperm((phi, 2, phi + 1))])
assert (len(TI), len(ID), len(TD)) == (60, 30, 60)
def penta_axes(P):                                         # face normals of the 5-sided faces (or 10-sided)
    h = ConvexHull(P); g = {}
    for simp, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq[:3], 6)), set()).update(simp)
    return np.array([k for k, v in g.items() if len(v) in (5, 10)])
def aligned(P):                                            # same icosahedral orientation as the TI core (5-fold axes coincide)
    A = penta_axes(TI); best = None
    for Q in (P, P[:, [1, 0, 2]]):
        sc = np.mean([max(np.dot(x / np.linalg.norm(x), y / np.linalg.norm(y)) for y in penta_axes(Q)) for x in A])
        if best is None or sc > best[0]: best = (sc, Q)
    assert best[0] > 1 - 1e-6, best[0]; return best[1]
ID = aligned(ID); TD = aligned(TD)
rm = float(sys.argv[1]) if len(sys.argv) > 1 else 1.18; ro = float(sys.argv[2]) if len(sys.argv) > 2 else 1.42
TI /= np.linalg.norm(TI[0]); ID *= rm / np.linalg.norm(ID[0]); TD *= ro / np.linalg.norm(TD[0])
def faces(P):
    h = ConvexHull(P); groups = {}
    for simp, eq in zip(h.simplices, h.equations): groups.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    out = []
    for eq, vs in groups.items():
        n = np.array(eq[:3]); vs = list(vs); c = P[vs].mean(0); e1 = P[vs[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        vs.sort(key=lambda v: np.arctan2((P[v] - c) @ e2, (P[v] - c) @ e1)); out.append((n, vs))   # counter-clockwise seen from outside
    return out
FTI, FID, FTD = faces(TI), faces(ID), faces(TD)
def match(F, n): return max(F, key=lambda f: f[0] @ n)[1]
near = lambda P, Q, x: int(np.argmax((Q / np.linalg.norm(Q, axis=1)[:, None]) @ (x / np.linalg.norm(x))))
mTI = {u: near(TI, ID, TI[u] + TI[[w for w in range(60) if abs(np.linalg.norm(TI[u] - TI[w]) - np.linalg.norm(TI[0] - TI[1 if np.linalg.norm(TI[0]-TI[1])<0.5 else 0])) < 1] [0]]) for u in []}
# the ID point of a TI vertex: midpoint direction of its hexagon-hexagon edge
hexes = [vs for n, vs in FTI if len(vs) == 6]
hh = {}
for a, b in itertools.combinations(range(len(hexes)), 2):
    sh = set(hexes[a]) & set(hexes[b])
    if len(sh) == 2:
        u, w = sh; m = near(None, ID, TI[u] + TI[w]); hh[u] = m; hh[w] = m
assert len(hh) == 60
pTD = {t: near(None, ID, TD[t]) for t in range(60)}       # each TD vertex sits by the 2-fold axis of its decagon-decagon edge
cells = []; worst = 0.0; vol = 0.0
def svol(V, F): return sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
for n, b in FTI:
    m_ = match(FID, n); t_ = match(FTD, n)
    pts, F = [], []
    def idx(p):
        for q, v in enumerate(pts):
            if np.allclose(v, p, atol=1e-10): return q
        pts.append(p); return len(pts) - 1
    F.append([idx(TI[u]) for u in b][::-1])
    for k in range(len(b)):
        u, w = b[k], b[(k + 1) % len(b)]; f = [idx(TI[u]), idx(TI[w]), idx(ID[hh[w]]), idx(ID[hh[u]])]
        F.append(list(dict.fromkeys(f)))
    for k in range(len(t_)):
        t, s = t_[k], t_[(k + 1) % len(t_)]; f = [idx(ID[pTD[t]]), idx(ID[pTD[s]]), idx(TD[s]), idx(TD[t])]
        F.append(list(dict.fromkeys(f)))
    F.append([idx(TD[t]) for t in t_])
    V = np.array(pts)
    for f in F:
        if len(f) > 3:
            P = V[f]; nr = np.cross(P[1] - P[0], P[2] - P[0]); nr /= np.linalg.norm(nr); worst = max(worst, float(np.abs((P - P[0]) @ nr).max()))
    v = svol(V, F); vol += v
    cells.append({'V': V.tolist(), 'F': F, 'kind': f'{len(b)}-{len(m_)}-{len(t_)}', 'vol': v})
shell = ConvexHull(TD).volume - ConvexHull(TI).volume
from collections import Counter
print('cells:', Counter(c['kind'] for c in cells))
print(f'largest distance of a corner from its face plane {worst:.1e}')
print(f'cell volumes {min(c["vol"] for c in cells):.4f} .. {max(c["vol"] for c in cells):.4f}; sum {vol:.10f}; shell V(TD) - V(TI) {shell:.10f}')
json.dump(cells, open('scutoid-sphere.json', 'w'))
print('FINAL ok' if worst < 1e-9 and abs(vol - shell) < 1e-9 and min(c['vol'] for c in cells) > 0 else 'FINAL FAIL')
