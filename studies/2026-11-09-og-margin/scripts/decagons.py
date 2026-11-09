# DICTO 9 Nov: "truncated triangles?" For every level with faces on the 3-fold axes: the axis face's corner count, side lengths in
# order, interior angles; a truncated triangle = hexagon with sides alternating a, b and all angles 120 deg (3-fold, not 6-fold).
# Also at levels with NO axis hexagon: what lies on the 3-fold axis (corner, or which face) and the faces touching the axis region.
import sys, os, math
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); exec(open('exact_upward.py').read().split("def kinds(S)")[0])
q5 = lambda x: float(x.a) + float(x.b) * 5 ** .5
W = np.array([[q5(x) for x in v] for v in OG]); KMAX = int(sys.argv[2])
Gf = np.array([[[q5(x) for x in row] for row in M] for M in G]); A3 = None
for g in Gf:
    c = (np.trace(g) - 1) / 2
    if abs(c - (5 ** .5 - 1) / 4) < 1e-9 or abs(c - (1 + 5 ** .5) / 4) < 1e-9: w, v = np.linalg.eig(g); A3 = np.real(v[:, np.argmin(np.abs(w - 1))]); A3 /= np.linalg.norm(A3); break
def faces(W, tol=1e-9):
    h = ConvexHull(W); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    G_ = {}
    for f in range(n): G_.setdefault(find(f), []).append(f)
    return [(h.equations[g[0], :3], -h.equations[g[0], 3], sorted(set(int(j) for f in g for j in h.simplices[f]))) for g in G_.values()]
for k in range(KMAX + 1):
    F = faces(W)
    best = max(F, key=lambda f: abs(f[0] @ A3))
    n, d, mem = best; P = W[mem]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ B.T
    o = np.argsort(np.arctan2(Q[:, 1], Q[:, 0])); P = P[o]; m = len(P)
    sides = [np.linalg.norm(P[(i + 1) % m] - P[i]) for i in range(m)]
    angs = [math.degrees(math.acos(np.clip(np.dot(P[i - 1] - P[i], P[(i + 1) % m] - P[i]) / (np.linalg.norm(P[i - 1] - P[i]) * np.linalg.norm(P[(i + 1) % m] - P[i])), -1, 1))) for i in range(m)]
    on = abs(n @ A3) > 1 - 1e-9
    kind = ''
    if on and m == 10:
        a, b = sides[0], sides[1]; alt = all(abs(sides[i] - (a if i % 2 == 0 else b)) < 1e-9 for i in range(10)); eq120 = all(abs(x - 144) < 1e-6 for x in angs)
        kind = ('REGULAR hexagon' if abs(a - b) < 1e-9 and eq120 else 'TRUNCATED PENTAGON (sides alternate, angles 144)' if alt and eq120 else
                'alternating sides, angles not all 120' if alt else 'irregular')
        kind += f'  long/short = {max(a, b) / min(a, b):.6f}'
    print(f'k {k:2d}: 5-fold axis meets ' + (f'a {m}-gon face: sides ' + ', '.join(f'{x:.4f}' for x in sides) + ' | angles ' + ', '.join(f'{x:.1f}' for x in angs) + f' | {kind}'
          if on else f'no face (nearest face {math.degrees(math.acos(min(1, abs(n @ A3)))):.2f} deg off, a {m}-gon)'), flush=True)
    if k == KMAX: break
    W = np.array([f[0] * f[1] for f in F])
print('FINAL ok' if A3 is not None and k == KMAX else 'FINAL FAIL: axis not found or run incomplete')
