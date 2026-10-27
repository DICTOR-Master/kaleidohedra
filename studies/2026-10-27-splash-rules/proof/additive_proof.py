# Volume Swap Rule below s0 = 1/2: proof of ADDITIVITY (DICTO 2026-10-27, "obviously needs or relates to some other fact of influence").
# Frame and linearisation as in swapgeom.py (gap between layer 0 = A and layer 1 = B; layer -1 = C (t = c) or B (t = h)).
# Layer 2 is C exactly when layer 1 is c (t' = c), A when t' = h. Gap 1 sites: option C (t' = c) or option A (t' = h).
# Claim, for q1 <= q <= 1/3 (s1 <= s <= 1/2) and lam in [lam_-(t), 9q/16]:
#  (P1) the lower half of every piece is cut by NO hole outside gaps -1, 0, 1 and by no gap-1 hole of option A:
#       lower half = K_low(t) ∩ {zeta <= 1/2} when t' = h, and = K_low(t) ∩ {zeta <= 1/2} ∩ (option-C gap-1 halfspaces) when t' = c.
#  (P2) the part carved off by the option-C holes does not depend on t: on Pi_j = K0 ∩ {zeta <= 1/2} ∩ {pow_j <= pow_i}
#       (K0 = cell against gap 0 and the gap -1 hole common to both types, A at -3/4), every type-specific gap -1 hole k
#       (c-only and h-only) satisfies pow_i <= pow_k. Hence K_low(t) ∩ low ∩ {pow_j <= pow_i} = Pi_j for both t, and the carved set
#       D = union_j (K_low(t) ∩ low ∩ {pow_j < pow_i}) is one set for c and h.
#  Then Vlow(t, t') = |K_low(t) ∩ low| - [t' = c] |D_low|; by the mirror Vup(t, t') = |K_up(t') ∩ up| - [t = c] |D_up|; so
#  V = A(t) + B(t') with A(t) = |K_low(t) ∩ low| - [t = c] |D_up|, B(t') = |K_up(t') ∩ up| - [t' = c] |D_low|: ADDITIVE, Swap Rule.
# Steps: (T) exact threshold q1 = sup{q : some hole of dn2/dn3/up2/up1-option-A cuts a lower half}; (C1) certificates for P1 on
# [q1, 1/3]; (C2) certificates for P2 on [q1, 1/3].  Usage: python additive_proof.py [q1]
import sys
from fractions import Fraction as Fr
from swapgeom import *

def lists(role, t):
    i, S = sites(role, t)
    P, zi, ti = ROLE[role]; ci = POS[P]
    def pts(lvs): return [(c, z, tt) for z, Pj, tt in lvs for c in coset_points(Pj, ci) if not (z == zi and c == ci)]
    optA, optC = pts(gap_levels(1, 'B', 'A')), pts(gap_levels(1, 'B', 'C'))
    W = {'c': 'C', 'h': 'B'}
    g0 = [j for j in S['K'] if j[1] > 0]
    gm = {tt: pts(gap_levels(-1, W[tt], 'A')) for tt in 'ch'}
    common = [j for j in gm['c'] if j in gm['h']]
    spec = {tt: [j for j in gm[tt] if j not in common] for tt in 'ch'}
    return i, S, optA, optC, g0, common, spec

def half_rows_q(role, t, q0, qmax):
    i, S = sites(role, t)
    return [row(i, j) for j in S['K']] + domain_rows(t, q0, True, qmax)

def g(role, t, j, q):
    i, S = sites(role, t); R = half_rows_q(role, t, q, q); a, b = row(i, j); res = lp_max(a, R)
    if res['status'] == 'infeasible': return None
    assert res['status'].startswith('optimal'), res
    return res['value'] - b

def outside(role, t):
    i, S, optA, optC, *_ = lists(role, t)
    return i, [('dn2', j) for j in S['dn2']] + [('dn3', j) for j in S['dn3']] + [('up2', j) for j in S['up2']] + [('up1A', j) for j in optA]

def threshold():
    grid = [Fr(k, 240) for k in range(16, 81)]           # q = 1/15 .. 1/3
    best = Fr(0); crit = []
    for role in ROLE:
        for t in 'ch':
            i, L = outside(role, t)
            R0 = half_rows_q(role, t, 0, Fr(1, 3))
            for grp, j in L:
                a, b = row(i, j)                                     # prefilter: does j reach the half anywhere on q <= 1/3?
                if lp_max([Fr(1), 0, 0, 0, 0], R0 + [([-x for x in a], -b)])['status'] == 'infeasible': continue
                pos = [q for q in grid if (v := g(role, t, j, q)) is not None and v > 0]
                if pos:
                    m = max(pos)
                    if m > best: best, crit = m, [(role, t, grp, j)]
                    elif m == best: crit.append((role, t, grp, j))
    print('largest grid q with a cut:', best, 'by', len(crit), 'sites', flush=True)
    roots = []
    for role, t, grp, j in crit:
        lo, hi = best, best + Fr(1, 240)
        for _ in range(40):
            m = (lo + hi) / 2
            if g(role, t, j, m) > 0: lo = m
            else: hi = m
        q1_, q2_ = lo - (hi - lo) * 3, lo - (hi - lo)
        g1, g2 = g(role, t, j, q1_), g(role, t, j, q2_)
        r = Fr(q1_ - g1 * (q2_ - q1_) / (g2 - g1)).limit_denominator(10000)
        print(f'  {role} {t} {grp} {j}: crossing {r}; g(r) = {g(role, t, j, r)}, g(r - 1e-6) = {g(role, t, j, r - Fr(1, 10**6))}, g(r + 1e-6) = {g(role, t, j, r + Fr(1, 10**6))}', flush=True)
        roots.append(r)
    return max(roots)

def certify(q1):
    ok = bad = 0; fails = []
    for role in ROLE:
        for t in 'ch':
            i, S, optA, optC, g0, common, spec = lists(role, t)
            R = half_rows_q(role, t, q1, Fr(1, 3))
            c = [Fr(-1), 0, 0, 0, Fr(-1)]; res = lp_max(c, R)              # zeta >= -1 (vertical dominance)
            good = res['status'].startswith('optimal') and res['value'] <= 0 and check_cert(c, R, res['y'], 0)
            ok += good; bad += not good
            if not good: fails.append(('zeta', role, t))
            _, L = outside(role, t)
            for grp, j in L:                                                 # (P1)
                a, b = row(i, j); res = lp_max(a, R)
                good = res['status'].startswith('optimal') and res['value'] <= b and check_cert(a, R, res['y'], b)
                ok += good; bad += not good
                if not good: fails.append(('P1', role, t, grp, j, res.get('status'), res.get('value'), b))
            p1 = ok
            # (P2) Pi_j for each option-C hole j, against every type-specific gap -1 hole (both types)
            K0 = [row(i, j) for j in g0 + common] + domain_rows('h', q1, True, Fr(1, 3))
            for j in optC:
                a, b = row(i, j); Pi = K0 + [([-x for x in a], -b)]            # pow_j <= pow_i
                if lp_max([Fr(1), 0, 0, 0, 0], Pi)['status'] == 'infeasible': continue   # j never reaches the half
                for tt in 'ch':
                    for k in spec[tt]:
                        ak, bk = row(i, k); res = lp_max(ak, Pi)
                        if res['status'] == 'infeasible': continue
                        good = res['status'].startswith('optimal') and res['value'] <= bk and check_cert(ak, Pi, res['y'], bk)
                        ok += good; bad += not good
                        if not good: fails.append(('P2', role, t, j, tt, k, res.get('status'), res.get('value'), bk))
            print(f'{role} {t}: running {ok} PASS {bad} FAIL', flush=True)
    print('FAILS', fails[:20]); print(f'TOTAL {ok} PASS, {bad} FAIL on q in [{q1}, 1/3] (s in [{Fr(3, 2) * q1}, 1/2])')

if __name__ == '__main__':
    q1 = Fr(sys.argv[1]) if len(sys.argv) > 1 else threshold()
    print('q1 =', q1, ' s1 =', Fr(3, 2) * q1, flush=True)
    certify(q1)
