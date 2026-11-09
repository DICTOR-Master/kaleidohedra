# DICTO #43, 9 Nov ("proceed", cheapest safe option): RING LEMMA data. Per level: for every pair of faces sharing an edge, the ratio
# of their angular radii gamma (larger/smaller); max and 99th percentile over all pairs, and for the largest face its biggest
# neighbour ratio. Bounded ratios (+ face count growing ~1.3x) would force the largest face to shrink (Rodin-Sullivan style).
# usage: python -u ring_lemma.py <five-fold-octet dir> <kmax>
import sys, os, math
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); exec(open('exact_upward.py').read().split("def kinds(S)")[0])
q5 = lambda x: float(x.a) + float(x.b) * 5 ** .5
W = np.array([[q5(x) for x in v] for v in OG]); KMAX = int(sys.argv[2]); rows = []
for k in range(KMAX + 1):
    h = ConvexHull(W); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < 1e-9: par[find(f)] = find(g)
    roots = sorted(set(find(f) for f in range(n))); gid = {r: i for i, r in enumerate(roots)}; F = len(roots)
    mem = [set() for _ in range(F)]; N = np.zeros((F, 3)); D = np.zeros(F)
    for f in range(n):
        i = gid[find(f)]; mem[i].update(int(j) for j in h.simplices[f]); N[i] = E[f, :3]; D[i] = -E[f, 3]
    gam = np.array([np.arccos(np.clip((W[list(m)] @ N[i]) / np.linalg.norm(W[list(m)], axis=1), -1, 1)).max() for i, m in enumerate(mem)])
    pairs = set()
    for f in range(n):
        for g in h.neighbors[f]:
            a, b = gid[find(f)], gid[find(g)]
            if a != b: pairs.add((min(a, b), max(a, b)))
    P = np.array(list(pairs)); R = np.maximum(gam[P[:, 0]], gam[P[:, 1]]) / np.maximum(np.minimum(gam[P[:, 0]], gam[P[:, 1]]), 1e-15)
    top = int(np.argmax(gam)); nb = [b if a == top else a for a, b in pairs if top in (a, b)]
    rt = max(gam[top] / gam[j] for j in nb)
    rows.append((k, F, float(R.max()), float(np.percentile(R, 99)), float(rt)))
    print(f'k {k:2d} F {F:6d} neighbour gamma ratio: max {R.max():8.2f}  99% {np.percentile(R, 99):6.2f}  median {np.median(R):5.2f} | largest face vs its neighbours: up to {rt:6.2f}', flush=True)
    if k == KMAX: break
    W = N * D[:, None]
late = [r for r in rows if r[0] >= 20]
print(f'k >= 20: max neighbour ratio {max(r[2] for r in late):.2f}, 99% {max(r[3] for r in late):.2f}, largest-face ratio {max(r[4] for r in late):.2f}')
print('FINAL ok' if len(rows) == KMAX + 1 else 'FINAL FAIL: run incomplete')
