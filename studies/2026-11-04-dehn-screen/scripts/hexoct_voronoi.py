"""Dictionary test: along the HexOct walk (#75), is the c-tile ever the RD and the h-tile the TRD (the Voronoi cells of fcc / hcp)?
Each tile = union of its 4 pieces (convex hull compared, plus volume of the union = hull volume). Compare by distance multisets (scale-free: ball spacing 1)."""
import os, sys, math, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
exec(open('scripts/halfcell.py').read().split('print("RD"')[0])
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as Tl
os.chdir(here); H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
def sig(P): D = np.linalg.norm(P[:, None] - P[None], axis=2); return np.sort(np.round(D.ravel(), 5))
sRD, sTRD = sig(RD[ConvexHull(RD).vertices]), sig(TRD[ConvexHull(TRD).vertices])
best = {'c': (9, None), 'h': (9, None)}
for i in range(0, 161):
    lam = Fr(-7, 16) + Fr(i, 160)*(Fr(3, 8) + Fr(7, 16))
    for word, L, k, ref in (('ABC', 1, 'c', sRD), ('AB', 0, 'h', sTRD)):
        try:
            os.chdir(HEX); pcs, _ = Tl.tile(word, L, lam); os.chdir(here)
        except Exception: os.chdir(here); continue
        X = np.unique(np.round(np.vstack([np.array([cart(p) for p in P]) for _, _, _, P, _ in pcs]), 9), axis=0); h = ConvexHull(X)
        vol = sum(ConvexHull(np.array([cart(p) for p in P])).volume for _, _, _, P, _ in pcs if len(P) >= 4)
        conv = abs(h.volume - vol) < 1e-6
        Y = X[h.vertices]; d = 9 if len(Y) != 14 else float(np.max(np.abs(sig(Y) - ref)))
        if conv and d < best[k][0]: best[k] = (d, str(lam))
print('closest c-tile to the RD :', best['c'], '| closest h-tile to the TRD:', best['h'], '(0 = congruent; 9 = never convex with 14 corners)')
