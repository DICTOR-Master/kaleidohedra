"""Hollow-straw version 3 as a linear programme (27 Nov 2026). With Claude (Anthropic).
c116_straw_rank.py: the pressures allowed by Minana's corners are exactly f_k = mu_k (n_t . x - c_t) (t = sigma(k)) plus one common
affine function: each straw has ONE pump setting mu_k. Straw k then wins where mu_k x (distance to Minana's plane t) is smallest, so
every wall is flat and every straw convex. Take the core as the level set {min_k mu_k D_k = 1}: its face k is parallel to Minana's
face sigma(k), set in by d_k = 1/mu_k. So flat-walled straws exist (with this core) exactly when some inward offsets d_k give a
polyhedron with Minana's face directions and C116's face pattern (under the pairing): a linear programme in the 60 offsets.
At each C116 corner (faces a, c, d) the corner of the offset planes must be strictly inside every other offset plane (margin m,
maximised); offsets positive (core inside Minana). Feasible with m > 0 <=> the flat-walled Hollow-straw layer exists; every
piece = (straw cell) between core and Minana, convex. Floats to solve; the offsets are then rounded to rationals and checked EXACTLY."""
import os, sys, json
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); faces = d['faces']
Dm = A.build("aequus-377")
from resin import Q
PL = [(list(u), c) for u, c in Dm["planes"]]   # exact (Q(sqrt5))
NN = np.array([[float(x) for x in u] for u, c in PL]); CC = np.array([float(c) for u, c in PL])
def corners(fl):
    at = {}
    for k, f in enumerate(fl):
        for v in f: at.setdefault(v, set()).add(k)
    return [tuple(sorted(s)) for s in at.values()]
T0 = corners(faces)
out = {}
for which, fn in (('symmetric (30 swaps)', 'onefloor.json'), ('floating (18 swaps)', 'onefloor_float.json')):
    sig = {int(k): int(v) for k, v in json.load(open(os.path.join(HERE, '../data/c116/' + fn)))['pairing'].items()}
    # unknowns: d_t (t = Minana face, 60) and m; corner of planes t1,t2,t3 offset: v = Ainv (c - d)
    Aub, bub = [], []
    for tri in T0:
        ts = [sig[k] for k in tri]; Ai = np.linalg.inv(NN[ts])
        for t in range(60):
            if t in ts: continue
            # n_t . Ai (c_ts - d_ts) <= c_t - d_t - m   ->   -n_t Ai d_ts + d_t + m <= c_t - n_t Ai c_ts
            w = NN[t] @ Ai; row = np.zeros(61); row[ts] -= w; row[t] += 1; row[60] = 1
            Aub.append(row); bub.append(CC[t] - w @ CC[ts])
    for t in range(60):   # d_t >= m (core strictly inside)
        row = np.zeros(61); row[t] = -1; row[60] = 1; Aub.append(row); bub.append(0.0)
    bounds = [(0, float(CC[t])) for t in range(60)] + [(None, None)]
    c = np.zeros(61); c[60] = -1
    r = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=bounds, method='highs')
    m = -r.fun if r.status == 0 else None
    print(f'{which}: LP status {r.status} ({r.message.split(".")[0]}); best margin {m}', flush=True)
    ok_exact = None
    if m is not None and m > 1e-9:
        dd = [Fr(int(round(x * 10**9)), 10**9) for x in r.x[:60]]
        def corner(ts):   # exact solve of three planes
            M = [PL[t][0] for t in ts]; rhs = [PL[t][1] - Q(dd[t]) for t in ts]
            det = lambda a, b, c_: a[0]*(b[1]*c_[2]-b[2]*c_[1]) - a[1]*(b[0]*c_[2]-b[2]*c_[0]) + a[2]*(b[0]*c_[1]-b[1]*c_[0])
            D = det(*M); cols = []
            for q in range(3):
                Mq = [list(row) for row in M]
                for i in range(3): Mq[i][q] = rhs[i]
                cols.append(det(*Mq) / D)
            return cols
        bad = 0
        for tri in T0:
            ts = [sig[k] for k in tri]; v = corner(ts)
            bad += sum(1 for t in range(60) if t not in ts and (PL[t][0][0] * v[0] + PL[t][0][1] * v[1] + PL[t][0][2] * v[2] - PL[t][1] + Q(dd[t])).sign() >= 0)
        bad += sum(1 for t in range(60) if dd[t] <= 0)
        ok_exact = bad == 0
        print(f'   exact check of the rounded offsets: violations {bad} -> core with Minana face directions and C116 pattern: {ok_exact}', flush=True)
        json.dump(dict(pairing=fn, offsets=[str(x) for x in dd], margin=m), open(os.path.join(HERE, f'../data/c116/straw_lp_{fn}'), 'w'))
    out[which] = dict(margin=m, exact=ok_exact)
print('RESULT:', out)
print('FINAL ok' if all(v['margin'] is not None for v in out.values()) else 'FINAL FAIL (LP did not solve)')
