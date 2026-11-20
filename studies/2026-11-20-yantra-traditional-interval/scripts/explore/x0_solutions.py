"""Explore (not a certificate): every real solution (t, S) of G = H1 = 0 with v = u, S in (R, 1), t in (0, u), at sample u,
with its smallest admissibility slack. Purpose: see whether the inadmissible solutions stay clear of admissibility, so that a
uniqueness box certificate is feasible."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import mpmath as mp
mp.mp.dps = 50
import yfam as Y
for uf in [0.55, 0.58, 0.588, 0.6, 0.62, 0.65, 0.68, 0.7, 0.72, 0.74, 0.746, 0.75, 0.7505, 0.76]:
    u = mp.mpf(uf); R = 1 / (1 + u * u); out = []
    for S in Y.real_roots(Y.coeffs('G', 3, {0: u, 1: u, 2: 0}), R, 1):
        for t in Y.real_roots(Y.coeffs('H1', 2, {0: u, 1: u, 3: S}), 0, u):
            try: y = Y.build(u, u, t, S); m = Y.margin(y)
            except ZeroDivisionError: m = (None, 'div0')
            out.append((mp.nstr(S, 6), mp.nstr(t, 6), mp.nstr(m[0], 3) if m[0] is not None else None, m[1]))
    print(uf, 'S roots of G in (R,1):', len(Y.real_roots(Y.coeffs('G', 3, {0: u, 1: u, 2: 0}), R, 1)), out, flush=True)
