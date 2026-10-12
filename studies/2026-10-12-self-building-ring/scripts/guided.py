# Guided build of the J2 ring from the pieces the local test forces (2026-10-12).
# Forced: a J2 corner at each floor corner (same turn as phi*J2) and a FUJI delta-edge along each floor edge.
import sys, os, itertools, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.spatial import ConvexHull
rc.KIT.update(KIT); PHI = rc.PHI
src = open(os.path.join(rc.HERE, 'local_cover.py')).read()
G = None; exec(src[src.index('# the 120 frame symmetries'):src.index('pieces = {k')])
RING = sys.argv[1] if len(sys.argv) > 1 else 'J2'
r = rc.ring(RING); band, hole = r['band'], r['hole']; Fb, Fh = rc.planes(band), rc.planes(hole)
RV = rc.vol(band) - rc.vol(hole)
def sep(A, B, tol=1e-7):
    HA, HB = ConvexHull(A), ConvexHull(B); ax = list(HA.equations[:, :3]) + list(HB.equations[:, :3])
    for u in [A[i] - A[j] for i, j in itertools.combinations(range(len(A)), 2)]:
        for v in [B[i] - B[j] for i, j in itertools.combinations(range(len(B)), 2)]:
            w = np.cross(u, v); n = np.linalg.norm(w)
            if n > 1e-9: ax.append(w / n)
    return any((A @ a).max() <= (B @ a).min() + tol or (B @ a).max() <= (A @ a).min() + tol for a in ax)
def fits(W, placed=()):
    if not np.all(W @ Fb[:, :3].T + Fb[:, 3] <= 1e-9): return False
    if not sep(W, hole): return False
    return all(sep(W, P) for P in placed)
placed = []
# 1. J2(1/phi) at each floor corner: phi*J2 shrunk about the corner by 1/phi^2
J2big = np.vstack([r['floor'], r['apex'][None]])
for B in r['floor']:
    W = B + (J2big - B) / PHI ** 2
    assert fits(W, placed), 'corner J2 does not fit'
    placed.append(W)
top_hit = [np.min(np.linalg.norm(r['top'] - W[-1], axis=1)) for W in placed]
print(f'{RING} ring volume {RV:.9f}; 5 corner J2(1/phi) fit, their apices at the top corners: {np.allclose(top_hit, 0)}; volume {sum(rc.vol(W) for W in placed):.9f}')
# 2. which pieces (any type, sizes phi^-1..phi^-3, 120 turns) have an edge with the band's floor dihedral lying on the free middle of a floor edge?
f0, f1 = r['floor'][0], r['floor'][np.argmin([np.linalg.norm(r['floor'][0] - q) if np.linalg.norm(r['floor'][0] - q) > 1e-9 else 9 for q in r['floor']])]
m0, m1 = f0 + (f1 - f0) / PHI ** 2, f1 + (f0 - f1) / PHI ** 2       # the free middle segment (corner pentagons take 1/phi from each end)
print(f'free middle of a floor edge: length {np.linalg.norm(m1 - m0):.9f} (1/phi^2 = {1 / PHI ** 2:.9f})')
found = []
for name in ('FUJI', 'J2', 't1', 't2', 't5', 'AXE', 'CLEO'):
    V0 = KIT[name]
    for k in (-1, -2, -3):
        V = PHI ** k * (V0 - V0.mean(0))
        for gi, g in enumerate(G):
            W = V @ g.T
            for i, j in itertools.permutations(range(len(W)), 2):
                if abs(np.linalg.norm(W[i] - W[j]) - np.linalg.norm(m1 - m0)) > 1e-9: continue
                d1 = (W[j] - W[i]); d0 = m1 - m0
                if np.linalg.norm(np.cross(d1, d0)) > 1e-9 or d1 @ d0 < 0: continue
                X = W + (m0 - W[i])
                if fits(X, placed): found.append((name, k, gi, X))
uniq = {}
for name, k, gi, X in found: uniq.setdefault(tuple(sorted(map(tuple, np.round(X, 6)))), (name, k, X))
print(f'pieces filling a floor-edge middle exactly: {len(uniq)}: ' + ', '.join(f'{n}@phi^{k}' for n, k, _ in uniq.values()))
np.save(os.path.join(rc.HERE, f'../data/guided-{RING}-corners.npy'), np.array(placed))
json.dump([{'name': n, 'k': k, 'vertices': X.tolist()} for n, k, X in uniq.values()], open(os.path.join(rc.HERE, f'../data/guided-{RING}-edge-options.json'), 'w'))
