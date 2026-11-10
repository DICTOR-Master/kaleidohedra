"""[chain_num.py, cube version of chain_num5.py] B1 #80, numerical route (DICTO 10 Nov: 'dodecahedron answer unacceptable … without clear outcomes'). Same chain as chain_sym5.py at a
fixed depth s0, in floating point: start = 12 five-fold planes at foot 1 (|n|² scaling as there) and 30 two-fold planes at foot s0;
step = intersection of the half-spaces x·v <= v·v over the corners v. For each step: corner count, kinds (valences), the sorted corner
radii normalised by the largest (a shape fingerprint), and the similarity test between every pair of steps: same corner directions up to
one scale (the chain_sym5 test), and also up to any icosahedral rotation (directions compared as sets).
Usage: python chain_num5.py s0 steps"""
import sys, itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
s0 = float(eval(sys.argv[1])); N = int(sys.argv[2]); ph = (1 + 5 ** .5) / 2
ax4 = np.array([v for v in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, v)) == 1], float)
ax2 = np.array([v for v in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, v)) == 2], float)
assert len(ax4) == 6 and len(ax2) == 12
def poly(normals, feet):
    hs = np.hstack([normals, -feet[:, None]]); H = HalfspaceIntersection(hs, np.zeros(3))
    V = H.intersections; keep = []
    for v in V:
        if not any(np.linalg.norm(v - u) < 1e-9 for u in keep): keep.append(v)
    V = np.array(keep); h = ConvexHull(V)
    # valence = number of distinct face planes at a corner
    E = h.equations; planes = []
    for e in E:
        if not any(np.abs(e - q).max() < 1e-9 for q in planes): planes.append(e)
    P = np.array(planes); val = [(np.abs(P[:, :3] @ v + P[:, 3]) < 1e-8).sum() for v in V]
    kinds = {}
    for x in val: kinds[int(x)] = kinds.get(int(x), 0) + 1
    return V, kinds
n0 = np.vstack([ax4, ax2]); f0 = np.concatenate([np.ones(6), np.full(12, 2 * s0)])   # as chain_sym.py: (n, 1) and (n, 2s)
V, kinds = poly(n0, f0); hist = [(V, kinds)]
print(f'step 0: {len(V)} corners, kinds {kinds}')
for k in range(1, N + 1):
    V, kinds = poly(V, np.einsum('ij,ij->i', V, V)); hist.append((V, kinds))
    r = np.sort(np.linalg.norm(V, axis=1)); print(f'step {k}: {len(V)} corners, kinds {kinds}, R {r[-1]:.6f}, r_min/R {r[0]/r[-1]:.6f}', flush=True)
# rotations of the icosahedral group (as 3x3 matrices) from the five-fold axes: generate by closure
def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
G = [np.eye(3)]; gens = [rot(np.array([0, 0, 1.]), np.pi / 2), rot(np.array([1, 1, 1.]), 2 * np.pi / 3)]
while True:
    new = [g @ h for g in G for h in gens if not any(np.allclose(g @ h, q) for q in G)]
    uniq = []
    for m in new:
        if not any(np.allclose(m, q) for q in uniq): uniq.append(m)
    if not uniq: break
    G += uniq
assert len(G) == 24, len(G)
def same_dirs(A, B, R=np.eye(3)):
    a = A / np.linalg.norm(A, axis=1)[:, None]; b = (B @ R.T) / np.linalg.norm(B, axis=1)[:, None]
    ra = np.linalg.norm(A, axis=1); rb = np.linalg.norm(B, axis=1); ratios = []
    for v, nb in zip(b, rb):
        d = np.linalg.norm(a - v, axis=1); i = d.argmin()
        if d[i] > 1e-7: return None
        ratios.append(nb / ra[i])
    ratios = np.array(ratios); return ratios.mean() if ratios.std() < 1e-9 * ratios.mean() else None
found = []
for j, k in itertools.combinations(range(len(hist)), 2):
    A, ka = hist[j]; B, kb = hist[k]
    if len(A) != len(B) or ka != kb: continue
    g = same_dirs(A, B); gr = None if g is not None else next((same_dirs(A, B, R) for R in G if same_dirs(A, B, R) is not None), None)
    fa = np.sort(np.linalg.norm(A, axis=1)) / np.linalg.norm(A, axis=1).max(); fb = np.sort(np.linalg.norm(B, axis=1)) / np.linalg.norm(B, axis=1).max()
    print(f'steps {j} and {k}: same counts and kinds; similar (same directions): {g is not None}; similar after a rotation: {gr is not None}; '
          f'shape fingerprint difference {np.abs(fa - fb).max():.3e}' + (f'; scale {g if g is not None else gr:.9f}' if (g or gr) else ''))
    if g is not None or gr is not None: found.append((j, k))
print('closure:', found[0] if found else 'none within the steps run')
print('FINAL ok' if len(hist) == N + 1 else 'FINAL FAIL: chain stopped early')
