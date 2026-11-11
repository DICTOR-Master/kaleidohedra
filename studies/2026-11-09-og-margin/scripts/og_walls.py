import sys, os, numpy as np
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
src = open(here + '/og_sweep.py').read().split('rows_out = []')[0]
sys.argv = ['x', os.path.expanduser('~/k-research/studies/2026-10-19-five-fold-octet'), '0', '/dev/null']; exec(src)
from scipy.spatial import cKDTree
V = OGf; FF = faces(V)
for k in range(15):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); act = np.zeros(len(W), bool); act[FN[2]] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; x2 = np.einsum('ij,ij->i', X, X)
    R = np.sqrt(x2).max()
    tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]; seen = set(); lams = []
    for i in np.where(~act)[0]:
        if i in seen: continue
        for p in perms: seen.add(p[i])
        li, yi = death(X, x2, i); lams.append(li)
    w = np.unique(np.round(np.array(lams) / R**2, 6))   # walls, in units of R(X)^2 (scale-free); in distance: lam/|X| per plane
    gaps = np.diff(np.concatenate([[0], w]))
    print(f'k {k:2d}: cut {int((~act).sum()):4d} | walls {len(w):2d} | heights {np.round(w, 4).tolist()} | gaps {np.round(gaps, 4).tolist()}', flush=True)
    V, FF = W, FN
