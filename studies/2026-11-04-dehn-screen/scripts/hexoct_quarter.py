import os, sys, math, json, numpy as np
from fractions import Fraction as Fr
sys.argv_lams = sys.argv[1:]; sys.argv = sys.argv[:1] + ["x", "8", "300"]
exec(open('scripts/dehn.py').read().split("if __name__")[0])
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here); H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
for lam in [Fr(x) for x in sys.argv_lams]:
    for word, L, nm in (('AB', 0, 'h'),):
        os.chdir(HEX); pieces, tz = T.tile(word, L, lam); os.chdir(here)
        row = []
        for k, up, s_, P, J in pieces:
            X = np.unique(np.round(np.array([cart(p) for p in P]), 11), axis=0); X, F = hull_faces(X); r = dehn(X, F)
            row.append(f"{k}{'+' if up else '-'}:{len(X)}c " + ' '.join(f"{a}°→{v:+.2e}" for a, v in r['coefficient_sums_over_maxL'].items()))
        print(f"λ={str(lam):7s} {nm}-tile | " + ' | '.join(row), flush=True)
