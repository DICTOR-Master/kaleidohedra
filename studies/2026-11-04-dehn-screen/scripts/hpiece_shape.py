import os, sys, math, json, numpy as np
from fractions import Fraction as Fr
from collections import Counter
lams = sys.argv[1:]; sys.argv = sys.argv[:1] + ['x', '8', '300']
exec(open('scripts/dehn.py').read().split("if __name__")[0])
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here); H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
from scipy.spatial import ConvexHull
for l in lams:
    lam = Fr(l); os.chdir(HEX); pieces, tz = T.tile('AB', 0, lam); os.chdir(here)
    for k, up, s_, P, J in pieces[:2] if len(pieces) == 4 else pieces[:1]:
        X = np.unique(np.round(np.array([cart(p) for p in P]), 11), axis=0); X, F = hull_faces(X)
        rows = dehn(X, F, rows_only=True)
        angs = Counter(round(math.degrees(t), 4) for L, t in rows)
        N = [np.cross(X[f[1]] - X[f[0]], X[f[2]] - X[f[0]]) for f in F]; N = [n/np.linalg.norm(n) for n in N]
        vert = sum(1 for n in N if abs(n[2]) > 1 - 1e-9); hor = sum(1 for n in N if abs(n[2]) < 1e-9)
        print(f"λ={l} piece {k}: corners {len(X)}, faces {sorted(Counter(len(f) for f in F).items())}, horizontal faces {vert}, vertical faces {hor}, "
              f"dihedrals {dict(angs)}, z-range {X[:,2].min()/H:.4f}..{X[:,2].max()/H:.4f}, vol {ConvexHull(X).volume:.6f}")
