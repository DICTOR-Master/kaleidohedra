# Swap Rule proof: the exact threshold s0 (DICTO 2026-10-27). For an outside site j and a half-cell, g_j(q) = max over lam in the walk
# range and p in the half-cell of [pow_i(p) - pow_j(p)] at fixed q (exact LP). The lifted set is one convex polyhedron, so g_j is
# CONCAVE and piecewise linear in q; j cuts the half-cell at spacing q iff g_j(q) > 0. q0 = sup{q : some g_j(q) > 0}.
# Method: g at a coarse exact grid finds the sites that ever cut; bisection (exact LPs) brackets each zero crossing; two exact values on
# the last linear piece give the crossing exactly; then g(q0) = 0 exactly and g(q0 - 1/10^6) > 0 exactly (sharpness).
import sys
from fractions import Fraction as Fr
from swapgeom import *
from locality import half_rows
def g(role, t, j, q):
    i, S, R = half_rows(role, t, q, qmax=q); a, b = row(i, j); res = lp_max(a, R)
    if res['status'] in ('infeasible',): return None
    assert res['status'].startswith('optimal'), res
    return res['value'] - b
grid = [Fr(k, 60) for k in range(4, 41)]           # q = 1/15 ... 2/3
cands = {}
for role in ROLE:
    for t in 'ch':
        i, S, _ = half_rows(role, t, 0)
        for grp in ('up1', 'dn2', 'up2', 'dn3'):
            for j in S[grp]:
                pos = [q for q in grid if (v := g(role, t, j, q)) is not None and v > 0]
                if pos: cands[(role, t, grp, j)] = max(pos)
print(len(cands), 'sites cut somewhere on the grid; largest grid q with a cut:', max(cands.values()), flush=True)
top = max(cands.values()); crit = {k: v for k, v in cands.items() if v == top}
q0s = []
for (role, t, grp, j), qa in crit.items():
    lo, hi = qa, qa + Fr(1, 60)                      # g(lo) > 0 >= g(hi)
    for _ in range(40):
        m = (lo + hi) / 2
        if g(role, t, j, m) > 0: lo = m
        else: hi = m
    q1, q2 = lo - (hi - lo) * 3, lo - (hi - lo) * 1
    g1, g2 = g(role, t, j, q1), g(role, t, j, q2)
    root = q1 - g1 * (q2 - q1) / (g2 - g1)
    rs = Fr(root).limit_denominator(10000)
    print(role, t, grp, j, 'crossing ~', float(root), '->', rs, ' g(q0) =', g(role, t, j, rs), ' g(q0 - 1e-6) =', g(role, t, j, rs - Fr(1, 10**6)),
          ' g(q0 + 1e-6) =', g(role, t, j, rs + Fr(1, 10**6)), flush=True)
    q0s.append(rs)
q0 = max(q0s); print('q0 =', q0, ' s0 = 3 q0 / 2 =', Fr(3, 2) * q0)
