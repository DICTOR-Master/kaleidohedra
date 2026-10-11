# Icosidodecahedral network, test 1 (DICTO 2026-10-12: "try both, the geometry will tell"). Does an ID (or RT, TI) shell already
# sit cleanly inside the Lotus seed / Chain, i.e. at some size its surface runs only along faces of the pieces, cutting none? Scan
# the size of each form (same turn, centred) and count the Lotus pieces its surface cuts; report the sizes where none is cut.
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
L = json.load(open(sys.argv[1]))[:113]
pieces = [np.array(p['vertices']) for p in L]
MODE = sys.argv[2] if len(sys.argv) > 2 else 'all'
gap_only = [np.array(p['vertices']) for p in L if p['role'] != 'ico']
allv = np.vstack(pieces); R = np.linalg.norm(allv, axis=1).max()
outer = allv[np.isclose(np.linalg.norm(allv, axis=1), R, atol=1e-6)]
outer = np.unique(np.round(outer, 6), axis=0)                          # the Lotus seed's outer icosahedron, edge phi^2
def faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
def edges(V):
    d = min(np.linalg.norm(V[0] - w) for w in V[1:]); return [(a, b) for a, b in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[a] - V[b]) - d) < 1e-6]
I = outer; E = edges(I)
ID = np.array([(I[a] + I[b]) / 2 for a, b in E])
D = np.array([-f[:3] / f[3] for f in faces(I)])
ID2 = np.array([(D[a] + D[b]) / 2 for a, b in edges(D)])
RT = np.vstack([I, D * (np.linalg.norm(ID, axis=1).max() ** 2 / np.linalg.norm(D, axis=1).max() / np.linalg.norm(ID, axis=1).max())])
TI = np.array([p for a, b in E for p in ((2 * I[a] + I[b]) / 3, (I[a] + 2 * I[b]) / 3)])
forms = {'ID': ID, 'TI': TI, 'D': D, 'I': I}
_rng = np.random.default_rng(7)
def _samples(P, k=300):
    return _rng.dirichlet(np.ones(len(P)), k) @ P
SAMP = None
def cuts(F):
    n = 0
    for S in SAMP:
        d = (S @ F[:, :3].T + F[:, 3]).max(axis=1)          # > 0 outside the shell, < 0 inside
        if (d < -1e-7).any() and (d > 1e-7).any(): n += 1
    return n
SAMP = [_samples(P) for P in (gap_only if MODE == 'gap' else pieces)]
for name, V in forms.items():
    F0 = faces(V); best = []
    for s in np.exp(np.linspace(np.log(0.05), np.log(1.2), 700)):
        F = F0.copy(); F[:, 3] *= s
        c = cuts(F)
        if c == 0: best.append(s)
    # group consecutive sizes into intervals
    iv = []
    for s in best:
        if iv and s / iv[-1][1] < 1.004: iv[-1][1] = s
        else: iv.append([s, s])
    edge = lambda s: s * min(np.linalg.norm(V[0] - w) for w in V[1:])
    print(f'{name} ({MODE}): sizes where its surface cuts no Lotus piece (edge length): ' + ('; '.join(f'{edge(a):.5f}-{edge(b):.5f}' for a, b in iv) or 'none'), flush=True)
