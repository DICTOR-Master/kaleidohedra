# exploration: for fixed q, the lam-range where an outside site cuts the half-cell (exact LPs)
import sys
from fractions import Fraction as Fr
from swapgeom import *
from locality import half_rows
for q in [Fr(x) for x in sys.argv[1].split(',')]:
    for role in ROLE:
        for t in 'ch':
            i, S, R = half_rows(role, t, q, qmax=q)
            for g in ('up1', 'dn2', 'up2', 'dn3'):
                for j in S[g]:
                    a, b = row(i, j); Rj = R + [([-x for x in a], -b)]
                    lo = lp_max([0, Fr(-1), 0, 0, 0], Rj)
                    if lo['status'] != 'optimal': continue
                    hi = lp_max([0, Fr(1), 0, 0, 0], Rj); mx = lp_max(a, R)
                    print(f'q={q} {role} {t} {g} j={j}: cuts for lam in [{-lo["value"]}, {hi["value"]}]  depth {mx["value"]-b}', flush=True)
