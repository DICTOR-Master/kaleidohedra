import sys, numpy as np
from fractions import Fraction as Fr
src = open('scripts/hexoct_harmonic.py').read().split("lams = ")[0]; exec(src)
for d in (Fr(-1, 100), Fr(-1, 1000), Fr(-1, 10000), Fr(0), Fr(1, 10000), Fr(1, 1000), Fr(1, 100)):
    lam = Fr(5, 24) + d; X, _ = pts('AB', 0, lam); c = X.mean(0); X = X[np.linalg.norm(X - c, axis=1) > 1e-9]
    print(f"λ = 5/24 {'+' if d >= 0 else '-'} {abs(float(d)):.4f}: corners {len(X)}, Q6 = {M.Q3d(X, 6, centre=c):.8f}")
