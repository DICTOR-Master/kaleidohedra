"""Hollow-straw layer, EXACT certificate (27 Nov 2026; DICTO's Hollow-straw, flat-walled). With Claude (Anthropic).
Straws t = {0 <= D_t <= d_t, D_t/d_t <= D_s/d_s, D_s >= 0}, D_t = c_t - n_t . x (Minana's planes, exact in Q(sqrt5); offsets d_t
rational from c116_straw_lp.py). What holds by definition (no computation): each straw is an intersection of half-spaces (CONVEX,
flat walls); the straws cover the shell and overlap only on walls (each point goes to the smallest D_s/d_s); straw t meets the
core plane exactly in the core's face t and Minana's plane exactly in Minana's face t.
What is computed exactly here: the level sets P(lam) = {D_s >= lam d_s for all s} run from Minana (lam = 0) to the core (lam = 1),
planes moving parallel; the walls are the traces of P(lam)'s edges, and the face pattern of P(lam) can change only at a point where
four or more planes of P(lam) meet (a corner of the straw diagram inside the shell = a Y corner). So:
 (1) the core P(1) has C116's face pattern under the pairing (every C116 corner strictly inside the 57 other planes, exact);
 (2) every set of four planes is solved for (x, lam) with D_t(x) = lam d_t; kept if 0 < lam < 1 and D_s(x) > lam d_s for every
     other s: float filter (generous), then EXACT in Q(sqrt5); also exact: no fifth plane through any kept point;
 (3) the kept points are the Y corners: expected 18, one per swap of the floating-resin floor, each at the swap's four faces.
FINAL ok iff (1), the count, the exactly-four rule and the match with the swaps all hold."""
import os, sys, json, itertools
from fractions import Fraction as Fr
import numpy as np
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
from resin import Q
HERE = os.path.dirname(os.path.abspath(__file__))
Dm = A.build("aequus-377"); PL = [(list(u), c) for u, c in Dm["planes"]]; T = len(PL)
S = json.load(open(os.path.join(HERE, '../data/c116/straw_lp_onefloor_float.json'))); dd = [Fr(x) for x in S['offsets']]
P = json.load(open(os.path.join(HERE, '../data/c116/onefloor_float.json'))); sig = {int(k): int(v) for k, v in P['pairing'].items()}
faces = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))['faces']
NN = np.array([[float(x) for x in u] for u, c in PL]); CC = np.array([float(c) for u, c in PL]); DD = np.array([float(x) for x in dd])
def det3(a, b, c_): return a[0]*(b[1]*c_[2]-b[2]*c_[1]) - a[1]*(b[0]*c_[2]-b[2]*c_[0]) + a[2]*(b[0]*c_[1]-b[1]*c_[0])
def solve(M, r):   # exact Cramer
    n = len(M)
    def det(X):
        if n == 3: return det3(*X)
        s = None
        for j in range(4):
            minor = [[X[i][k] for k in range(4) if k != j] for i in range(1, 4)]
            term = X[0][j] * det3(*minor); term = term if j % 2 == 0 else -term
            s = term if s is None else s + term
        return s
    D = det(M); out = []
    for q in range(n):
        Mq = [list(row) for row in M]
        for i in range(n): Mq[i][q] = r[i]
        out.append(det(Mq) / D)
    return out
# (1) core pattern
at = {}
for k, f in enumerate(faces):
    for v in f: at.setdefault(v, set()).add(k)
T0 = [tuple(sorted(s)) for s in at.values()]; bad1 = 0
for tri in T0:
    ts = [sig[k] for k in tri]; v = solve([PL[t][0] for t in ts], [PL[t][1] - Q(dd[t]) for t in ts])
    bad1 += sum(1 for t in range(T) if t not in ts and (sum((PL[t][0][i] * v[i] for i in range(1, 3)), PL[t][0][0] * v[0]) - PL[t][1] + Q(dd[t])).sign() >= 0)
print(f'(1) core: {len(T0)} C116 corners, violations {bad1} (exact)', flush=True)
# (2) float filter over all quadruples: unknowns (x, lam): n_t . x + lam d_t = c_t
Qd = np.array(list(itertools.combinations(range(T), 4)))
M = np.concatenate([NN[Qd], DD[Qd][..., None]], axis=2); R = CC[Qd]
dt = np.linalg.det(M); okd = np.abs(dt) > 1e-12
sol = np.full((len(Qd), 4), np.nan); sol[okd] = np.linalg.solve(M[okd], R[okd][..., None])[..., 0]
lam = sol[:, 3]; X = sol[:, :3]
cand = np.where(okd & (lam > -1e-6) & (lam < 1 + 1e-6))[0]
ratio = (CC[None, :] - X[cand] @ NN.T) / DD[None, :]
mask = np.ones_like(ratio, bool); mask[np.arange(len(cand))[:, None], Qd[cand]] = False
mins = np.where(mask, ratio, np.inf).min(1)
cand = cand[mins > lam[cand] - 1e-6]
print(f'(2) quadruples {len(Qd)}; float candidates {len(cand)}', flush=True)
Y = []
for i in cand:
    ts = list(Qd[i]); s = solve([PL[t][0] + [Q(dd[t])] for t in ts], [PL[t][1] for t in ts]); x, l = s[:3], s[3]
    if not ((l).sign() > 0 and (l - Q(1)).sign() < 0): continue
    slack = [PL[t][1] - (PL[t][0][0] * x[0] + PL[t][0][1] * x[1] + PL[t][0][2] * x[2]) - l * Q(dd[t]) for t in range(T)]
    sg = [z.sign() for z in slack]
    if any(g < 0 for g in sg): continue
    Y.append(dict(planes=sorted(int(t) for t in ts), tight=sum(1 for g in sg if g == 0), lam=float(l)))
print(f'    exact Y corners {len(Y)}; tight-plane counts {sorted(set(y["tight"] for y in Y))}', flush=True)
# (3) match with the swaps (core labels -> Minana labels)
sw = [frozenset(sig[k] for k in (g + l_)) for g, l_ in P['swaps']]
ys = [frozenset(y['planes']) for y in Y]
match = sorted(map(sorted, ys)) == sorted(map(sorted, sw))
print(f'(3) swaps {len(sw)}; Y corners at exactly the swaps\' four faces: {match}', flush=True)
print('    depths lam of the Y corners:', sorted(round(y['lam'], 6) for y in Y), flush=True)
json.dump(dict(core_violations=bad1, Y=Y, match=match), open(os.path.join(HERE, '../data/c116/hollow_straw_exact.json'), 'w'))
ok = bad1 == 0 and len(Y) == 18 and all(y['tight'] == 4 for y in Y) and match
print('FINAL ok' if ok else 'FINAL FAIL')
