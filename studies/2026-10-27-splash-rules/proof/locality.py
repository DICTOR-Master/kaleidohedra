# Swap Rule proof, step 1: LOCALITY and the exact threshold s0 (DICTO 2026-10-27).
# For each role (tetY, oct, tetX) and type t of the lower layer (c, h): K = the power cell of the site against the sites of its own gap
# and the gap below (finite lateral lists; lateral dominance makes them complete, see PROOF.md), cut at the mid-plane zeta <= 1/2.
# (a) THRESHOLD: for every outside site j (gap 1 both choices, gap -2 both choices, supersets of gaps 2 and -3) the largest q at which
#     j still reaches the half-cell, q*_j = max{ q : (q, lam, p) in the lifted polyhedron, pow_i(p) >= pow_j(p) } (exact LP).
#     The set of (q, lam) where j cuts is convex (a superlevel set of a concave function), so j never cuts above q*_j.
#     q0 = max q*_j, s0 = 3 q0 / 2.
# (b) PROOF for q >= q0: one exact Farkas certificate per (role, t, j): pow_i(p) <= pow_j(p) on all (q, lam, p) with q >= q0, lam in the
#     walk range, p in the half-cell. Plus zeta >= -1 on the half-cell (needed by the vertical dominance of far gaps).
# Usage: python locality.py [q0]      (no argument: compute q0 first, then certify at q0)
import sys, json
from fractions import Fraction as Fr
from swapgeom import *

def half_rows(role, t, q0, cut=True, qmax=None):
    i, S = sites(role, t)
    return i, S, [row(i, j) for j in S['K']] + domain_rows(t, q0, cut, qmax)

def threshold():
    best = []; per = {}
    for role in ROLE:
        for t in 'ch':
            i, S, R = half_rows(role, t, 0)
            for g in ('up1', 'dn2', 'up2', 'dn3'):
                for j in S[g]:
                    a, b = row(i, j)
                    res = lp_max([Fr(1), 0, 0, 0, 0], R + [([-x for x in a], -b)])
                    if res['status'] == 'infeasible': continue
                    if res['status'] != 'optimal': print('!!', role, t, g, j, res, flush=True); best.append((None, role, t, g, j)); continue
                    per.setdefault((role, t, g), []).append(res['value'])
                    best.append((res['value'], role, t, g, j, res['z']))
    for k, v in sorted(per.items()): print(f'{k}: {len(v)} sites reach for some q; largest q* = {max(v)} (s = {Fr(3, 2) * max(v)})')
    top = max(b for b in best if b[0] is not None)
    print('TOP', top, flush=True)
    return top

def certify(q0):
    ok = bad = 0; fails = []; vals = {}
    for role in ROLE:
        for t in 'ch':
            i, S, R = half_rows(role, t, q0)
            # zeta >= -1 on the half-cell: maximise -(u + q) <= 0
            c = [Fr(-1), 0, 0, 0, Fr(-1)]; res = lp_max(c, R)
            good = res['status'].startswith('optimal') and res['value'] <= 0 and check_cert(c, R, res['y'], 0)
            ok += good; bad += not good
            if not good: fails.append(('zeta>=-1', role, t, res.get('status')))
            for g in ('up1', 'dn2', 'up2', 'dn3'):
                for j in S[g]:
                    a, b = row(i, j)
                    res = lp_max(a, R)          # max a.z over the half-cell polyhedron; need <= b
                    good = res['status'].startswith('optimal') and res['value'] <= b and check_cert(a, R, res['y'], b)
                    ok += good; bad += not good
                    if good: vals.setdefault((role, t, g), []).append(b - res['value'])
                    else: fails.append((role, t, g, j, res.get('status'), res.get('value'), b))
            print(f'{role} {t}: running {ok} PASS {bad} FAIL', flush=True)
    for k, v in sorted(vals.items()): print(f'  {k}: {len(v)} certificates, smallest margin {min(v)}')
    print('FAILS', fails[:20]); print(f'TOTAL certificates {ok} PASS, {bad} FAIL (q0 = {q0}, s0 = {Fr(3, 2) * q0})')
    return ok, bad

if __name__ == '__main__':
    if len(sys.argv) > 1: q0 = Fr(sys.argv[1])
    else: q0 = threshold()[0]
    certify(q0)
