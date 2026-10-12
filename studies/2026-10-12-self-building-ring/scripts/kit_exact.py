# Kit pieces in the Lotus frame, snapped to the golden module (coordinates (p + q phi)/2, p, q integers) and checked.
# t3 in the 2026-10-11 data file is degenerate (four coplanar points); it is rebuilt here on a face of the icosahedron (base: an
# equilateral triangle of edge 1, apex on its 3-fold axis at height 1/(sqrt3 phi^2), so the three apex edges are 1/phi).
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
PHI = rc.PHI
def snap(x, tol=2e-5):
    for den in (2, 4, 6, 10):
        for q in range(-60, 61):
            p = x * den - q * PHI
            if abs(p - round(p)) < tol * den: return (round(p) + q * PHI) / den
    raise ValueError(x)
KIT = {}
for k, V in rc.KIT.items():
    if k == 't3': continue
    KIT[k] = np.array([[snap(c) for c in v] for v in V]) if k not in ('A', 'B', 'C', 'K') else V
# t3 (base: equilateral triangle of edge 1, three edges 1/phi to the apex), placed so that all six edges run along two-fold axes
# like every other kit piece: search bases = triangles of icosahedron edges, apex = a corner + (1/phi) * a two-fold unit vector.
Ic = KIT['I'] - KIT['I'].mean(0)
U2 = np.array([Ic[i] - Ic[j] for i, j in itertools.permutations(range(12), 2) if abs(np.linalg.norm(Ic[i] - Ic[j]) - 1) < 1e-9])
def _two_fold(d): return np.any(np.abs(np.abs(U2 @ (d / np.linalg.norm(d))) - 1) < 1e-9)
_t3 = None
for tri in itertools.combinations(range(12), 3):
    T = KIT['I'][list(tri)]
    if not all(abs(np.linalg.norm(T[a] - T[b]) - 1) < 1e-9 for a, b in itertools.combinations(range(3), 2)): continue
    for u in U2:
        P = T[0] + u / PHI
        if all(abs(np.linalg.norm(P - T[k]) - 1 / PHI) < 1e-9 and _two_fold(P - T[k]) for k in range(3)):
            _t3 = np.vstack([T, P]); break
    if _t3 is not None: break
assert _t3 is not None, 't3 has no placement with all edges on two-fold axes'
KIT['t3'] = _t3
EXPECT = {  # edge multisets at the data's scale (MS tiles at 1/tau: edges 1/phi and 1)
    't1': [1 / PHI] * 5 + [1], 't2': [1 / PHI] * 4 + [1] * 2, 't3': [1 / PHI] * 3 + [1] * 3, 't4': [1 / PHI] * 3 + [1] * 3,
    't5': [1 / PHI] * 2 + [1] * 4, 't6': [1 / PHI] + [1] * 5, 'T2': [1 / PHI] + [1] * 4 + [PHI]}
if __name__ == '__main__':
    for k, V in KIT.items():
        msg = ''
        if k in EXPECT:
            d = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2))
            msg = f'edges match Mosseri-Sadoc {k}: {np.allclose(d, sorted(EXPECT[k]), atol=1e-9)}'
        print(f'{k:4s} corners {len(V):2d} volume {rc.vol(V):.12f} {msg}')
