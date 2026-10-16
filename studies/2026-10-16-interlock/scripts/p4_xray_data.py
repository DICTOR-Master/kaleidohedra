# Data for the P4 X-ray figure (DICTO 2026-10-16: "use an actual x-ray cut through, as in the app"): every station of both cycles in one
# setting as a whole shell (faces merged by plane), its exact cut by the mirror plane z = 0 (the section of Figure 2's rings), and which
# stations the two cycles share. One turn of the original cycle (I .. I·φ³) and the turn inside it; reversed stations in the same range.
# -> data/p4-xray-<setting>.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
p = (1 + 5 ** .5) / 2
AB = {'icosahedron': 'I', 'icosidodecahedron': 'ID', 'dodecahedron': 'D', 'truncated icosahedron': 'TI', 'Hecatodihedron': 'H', 'rhombic triacontahedron': 'RT',
      'icosahedron (phi^3)': 'I·φ³', 'dodecahedron (inner)': 'D', 'dual of the Hecatodihedron': 'O', 'pentakis dodecahedron': 'PD', 'dodecahedron (phi^3)': 'D·φ³'}
orig = [(AB[n], np.array(X)) for n, X in json.load(open('data/orig-chain.json'))]
flip0 = [(AB[n], np.array(X)) for n, X in json.load(open('data/flip-ends-chain.json'))][:-1]
def radii(X): h = ConvexHull(X); return -h.equations[:, 3].max(), np.linalg.norm(X, axis=1).max()
def same(X, Y): return len(X) == len(Y) and all(abs(a - b) < 1e-6 for a, b in zip(radii(X), radii(Y)))
def faces(V):
    h = ConvexHull(V); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    F = []
    for e in pl:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; Q = V[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return F
def section(X):
    pts = [x for x in X if abs(x[2]) < 1e-9]
    for a, b in itertools.combinations(X, 2):
        if a[2] * b[2] < -1e-12: t = -a[2] / (b[2] - a[2]); pts.append(a + t * (b - a))
    P = np.array(pts)[:, :2]; h = ConvexHull(P); return [[float(x), float(y), 0.0] for x, y in P[h.vertices]]
def corners(X):
    h = ConvexHull(X); return X[h.vertices]
Rout = radii(orig[-1][1])[1]
for s, (rho2, sc) in {'ends': (p * p / 4, 1.0), 'middle': (3 * p * p / 4, 3.0)}.items():
    O = [(n, X * p ** (-3 * t), t) for t in (0, 1) for n, X in orig[:-1]] + [('I·φ³', orig[-1][1], 0)]
    Rv = [(n + {-1: '·φ⁻³', 0: '', 1: '·φ³'}.get(t, f'·φ^{3 * t}'), X * sc * p ** (3 * t), t) for t in range(-3, 3) for n, X in flip0]
    Rv = [(n, X, t) for n, X, t in Rv if 0.12 < radii(X)[1] <= Rout * 1.0001]
    out = []
    for n, X, t in O:
        if radii(X)[1] < 0.12: continue
        V = corners(X); out.append({'name': n, 'side': 'orig', 'turn': t, 'shared': any(same(X, Y) for _, Y, _ in Rv), 'layer': ['I', 'ID', 'D', 'TI', 'H', 'RT'].index(n) if n in ('I', 'ID', 'D', 'TI', 'H', 'RT') else 0,
                    'v': np.round(V, 6).tolist(), 'f': faces(V), 'sect': section(X), 'r': radii(X)})
    for n, X, t in Rv:
        if any(same(X, Y) for _, Y, _ in O): continue
        V = corners(X); out.append({'name': n, 'side': 'rev', 'turn': t, 'shared': False, 'v': np.round(V, 6).tolist(), 'f': faces(V), 'sect': section(X), 'r': radii(X)})
    json.dump({'stations': out, 'rho': rho2 ** .5, 'Rout': Rout}, open(f'data/p4-xray-{s}.json', 'w'))
    print(s, len(out), 'stations;', 'shared:', [o['name'] for o in out if o['shared']])
