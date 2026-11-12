# lp_check.py (13 Nov 2026): a COUNTING test for keyed RDs (frequency / charge argument).
# In any filling, at every contact a world point P of one piece meets the world point P - d of its neighbour, with heights summing to 0.
# Average over a large region (a torus, or a ball whose boundary is negligible: Folner): if orientation g occurs with frequency f_g,
# then for each of the 24 contact pairs {P, P'} of world points, sum_g f_g (H_g[P] + H_g[P']) = 0, with f >= 0, sum f = 1.
# No such f  =>  the piece fills no torus and NOT all of space (it may still fill large balls). Exact certificate: a Farkas vector
# y (rational) with y.A_g > 0 for every orientation g, checked in exact arithmetic.
# usage: lp_check.py <deep json files> [IMAX for control]
import sys, os, json
from fractions import Fraction as Fr
here = os.path.dirname(os.path.abspath(__file__)); J = sys.argv[1]
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
from scipy.optimize import linprog
PAIRS = []
for d in range(12):
    for k in range(4):
        a, b = int(MA[d, k]), int(MB[d, k]); p = (min(a, b), max(a, b))
        if p not in PAIRS: PAIRS.append(p)
assert len(PAIRS) == 24
def colmat(H):
    HG = H[ACTINV]                                                    # (48 orientations, 48 world points)
    return np.array([[HG[g, a] + HG[g, b] for g in range(48)] for a, b in PAIRS])   # 24 x 48
def feasible(H):
    A = colmat(H); A_eq = np.vstack([A, np.ones((1, 48))]); b_eq = np.r_[np.zeros(24), 1]
    r = linprog(np.zeros(48), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * 48, method='highs'); return r.status == 0, A
def farkas(A):
    """y with y . A[:, g] >= 1 for all g (then sum_g f_g y.A_g >= 1 > 0 = y.(A f)): exact check on a rounded rational y"""
    r = linprog(np.zeros(24), A_ub=-A.T, b_ub=-np.ones(48), bounds=[(None, None)] * 24, method='highs')
    if r.status != 0: return None
    y = [Fr(v).limit_denominator(1000) for v in r.x]; Ai = A.astype(int).tolist()
    ok = all(sum(y[i] * Ai[i][g] for i in range(24)) > 0 for g in range(48)); return y if ok else None
def pair_feasible(H):
    """stronger LP: frequencies f_g and, for each of the 6 direction pairs, frequencies of fitting neighbour pairs (g at x, h at x+d)
    with both marginals equal to f (any tiling, averaged over a Folner region, gives such numbers)"""
    F = fit_table(H); D6 = [d for d in range(12) if d < NEG[d]]; var = {}; nv = 48
    for d in D6:
        for g, h in zip(*np.nonzero(F[:, d, :])): var[(d, int(g), int(h))] = nv; nv += 1
    rows = []; b = []
    for d in D6:
        for g in range(48):
            r = np.zeros(nv); r[g] = -1
            for h in range(48):
                if (d, g, h) in var: r[var[(d, g, h)]] = 1
            rows.append(r); b.append(0)
            r = np.zeros(nv); r[g] = -1
            for h in range(48):
                if (d, h, g) in var: r[var[(d, h, g)]] = 1
            rows.append(r); b.append(0)
    r = np.zeros(nv); r[:48] = 1; rows.append(r); b.append(1)
    res = linprog(np.zeros(nv), A_eq=np.array(rows), b_eq=np.array(b), bounds=[(0, None)] * nv, method='highs'); return res.status == 0
S = []
for f in J.split(','): S += [x[0] for x in json.load(open(f)) if 'SURVIVOR' in str(x[-1]) or 'no torus' in str(x[-1])]
# control: periodic pieces (random symmetric, judged killed k by hunt.judge) must be LP-feasible; plain RD feasible
rng = np.random.default_rng(3); cls = [G for G in subgroups() if len(G) == 4]; nper = 0; ok = feasible(np.zeros(48, int))[0]
while nper < 10:
    G = cls[int(rng.integers(len(cls)))]; pt = np.zeros(48, int)
    for oi, o in enumerate(orbits_on_points(G)): pt[o] = oi
    H = rng.integers(-1, 2, size=12)[pt]; v = judge(fit_table(H), 8, 2, list(range(48)))
    if v.startswith('killed'): nper += 1; fz, _ = feasible(H); pz = pair_feasible(H); ok &= fz and pz; print('control periodic piece', v, 'LP feasible', fz, 'pair LP', pz, flush=True)
print('controls ok', ok, flush=True)
res = []; ninf = 0; ncert = 0
for i, H in enumerate(S):
    fz, A = feasible(np.array(H)); y = None if fz else farkas(A); ninf += not fz; ncert += y is not None
    pz = pair_feasible(np.array(H)) if fz else False; npair = locals().get('npair', 0) + (not pz)
    res.append(dict(H=H, lp_feasible=bool(fz), pair_lp_feasible=bool(pz), farkas=[str(v) for v in y] if y else None))
print(f'pieces {len(S)}: LP infeasible (untileable by counting) {ninf}, exact Farkas certificates {ncert}; LP feasible {len(S) - ninf}; pair-LP infeasible {npair}', flush=True)
json.dump(res, open(J.split(',')[0].replace('.json', '') + '_lp.json', 'w'))
print('FINAL ok' if ok else 'FINAL FAIL: control', flush=True)
