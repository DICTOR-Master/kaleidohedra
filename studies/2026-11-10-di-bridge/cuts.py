"""D–I bridge B, step 2 (DICTO 10 Nov: "go on with B the flat Karma layer"). World 1 fills space, so a flat (111) plane through it cuts
each cell it crosses into two parts: the bridge layer under the plane IS the set of those parts. For every natural plane level (through a
layer of dodecahedron corners) list the cut parts below the plane: which cell (dodecahedral cell or Dogstar), their volume, and
whether the volume matches a known piece (CLEO, AXE, pentagonal pyramid, roof, FUJI, corner tetrahedra) or a simple fraction.
Usage: python cuts.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import phi, CUBE, ROOF, DOD
from scipy.spatial import ConvexHull, HalfspaceIntersection
n = np.ones(3) / 3 ** .5
def cut_vol(V, c, below=True):
    """volume of conv(V) ∩ {n.x <= c} (below) for a convex point set V"""
    H = ConvexHull(V); hs = H.equations.copy()
    extra = np.append(n, -c) if below else np.append(-n, c)
    hs = np.vstack([hs, extra])
    inner = V.mean(0); 
    pts = [p for p in V if (p @ n <= c) == below] + []
    try:
        # find an interior point of the cut
        lam = np.linspace(0, 1, 21); cand = [V.mean(0)] + list(V)
        for q in cand:
            for t in lam:
                x = V.mean(0) * (1 - t) + q * t
                x = x - n * ((x @ n - c) + (0.02 if below else -0.02)) * 0 
        x0 = None
        for q in V:
            for t in np.linspace(0.05, 0.95, 19):
                x = V.mean(0) * (1 - t) + q * t
                if np.all(hs[:, :3] @ x + hs[:, 3] < -1e-7): x0 = x; break
            if x0 is not None: break
        if x0 is None: return 0.0
        I = HalfspaceIntersection(hs, x0); return ConvexHull(I.intersections).volume
    except Exception: return float('nan')
roof = (ConvexHull(DOD).volume - phi ** 3) / 6
e = 1 / phi; cleo = np.sqrt(3) / 4 * e ** 2 * np.sqrt(1 - e ** 2 / 3) / 3
def cm(d):
    M = np.ones((5, 5)); M[0, 0] = 0
    for i in range(4):
        for j in range(4): M[i + 1, j + 1] = d[i][j]
    return np.sqrt(np.linalg.det(M) / 288)
axe = cm([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, e ** 2], [1, 1, e ** 2, 0]])
pp = (5 + 5 ** .5) / 24
KNOWN = {'CLEO': cleo, 'AXE': axe, 'pentagonal pyramid': pp, 'roof': roof, 'D/2': ConvexHull(DOD).volume / 2, 'cube corner tet (legs phi)': phi ** 3 / 6}
print('known volumes:', {k: round(v, 6) for k, v in KNOWN.items()})
# natural levels: projections of the corners of the dodecahedron at the origin cell and of its neighbours' layer offsets
levels = sorted({round(float(v @ n + m * phi / 3 ** .5), 6) for v in DOD for m in range(-3, 4)})
levels = [l for l in levels if 0 <= l < 2 * phi / 3 ** .5 + 1e-9]          # one period of the layer structure
print(f'{len(levels)} natural plane levels in one period (spacing of even layers {2 * phi / 3 ** .5:.6f})')
for c in levels:
    parts = []
    for i, j, k in itertools.product(range(-3, 4), repeat=3):
        ctr = np.array([i, j, k]) * phi; lev = ctr @ n
        if abs(lev - c) > 2: continue
        if (i + j + k) % 2 == 0:
            V = DOD + ctr; lo, hi = (V @ n).min(), (V @ n).max()
            if lo < c - 1e-9 < hi - 2e-9: parts.append(('D-cell', cut_vol(V, c)))
        else:
            C = CUBE + ctr; lo, hi = (C @ n).min(), (C @ n).max()
            if lo < c - 1e-9 < hi - 2e-9:
                v = cut_vol(C, c) - sum(cut_vol(ROOF[(a, -sg)] + ctr + np.eye(3)[a] * sg * phi, c) for a in range(3) for sg in (1, -1))
                parts.append(('Dogstar', v))
    kinds = {}
    for name, v in parts: kinds.setdefault((name, round(v, 5)), 0); kinds[(name, round(v, 5))] += 1
    def match(v):
        hits = [f'{k}' for k, w in KNOWN.items() if abs(v - w) < 1e-5] + [f'{m}×{k}' for k, w in KNOWN.items() for m in (2, 3, 4, 6, 10, 12, 20, 30) if abs(v - m * w) < 1e-5]
        return ','.join(hits)
    print(f'level {c:.6f}: ' + '; '.join(f'{nm} below-part {v} x{cnt}' + (f' [= {match(v)}]' if match(v) else '') for (nm, v), cnt in sorted(kinds.items())))
print('FINAL ok' if len(levels) == 6 else 'FINAL FAIL: unexpected number of plane levels')
