"""Step 3b (27 Nov 2026): Dehn invariants of the 8 piece types of P4 (pieces4.py) as exact vectors, and the combinations of types
with Dehn invariant 0 (space-filling candidates; zero is necessary, Debrunner 1980). With Claude (Anthropic).
Each edge: length c sqrt(d), interior dihedral pi - arccos(sign sqrt(c2)) (pi/2 if c2 = 0). Angle basis: all edge angles reduced
by PSLQ (60 digits) to pi and a few basic angles (identified, not proved). The Dehn vector of a type has one coordinate per
(d, basic angle), rational. Then: the rational kernel of the 8 type vectors, and its nonnegative part (LP): which multisets of
types can have Dehn invariant 0. Control: the whole P4 (every type with its orbit size) must be in it (P4 tiles space)."""
import os, json
from fractions import Fraction as F
import mpmath as mp
import sympy
mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, '../data/pieces4.json')))
def ang(c2, sg):
    c2 = F(c2)
    if c2 == 0: return mp.pi / 2
    return mp.pi - mp.acos(sg * mp.sqrt(mp.mpf(c2.numerator) / c2.denominator))
vals = {}
for t in T:
    for d, c, c2, sg in t['edges']: vals[(c2, sg)] = ang(c2, sg)
basis = []; expr = {}
for k in sorted(vals, key=lambda k: vals[k]):
    x = vals[k]; B = [b for _, b in basis]
    r = mp.pslq([x] + B + [mp.pi], maxcoeff=10**5, maxsteps=10**6)
    if r and r[0] != 0 and abs(sum(a * b for a, b in zip(r, [x] + B + [mp.pi]))) < mp.mpf(10) ** -50:
        expr[k] = [F(-a, r[0]) for a in r[1:-1]]          # coefficients on the basis (pi part dropped: Q pi is zero)
    else:
        basis.append((k, x)); expr[k] = None
nb = len(basis)
for k in expr:
    if expr[k] is None: e = [F(0)] * nb; e[[b for b, _ in basis].index(k)] = F(1); expr[k] = e
    else: expr[k] = expr[k] + [F(0)] * (nb - len(expr[k]))
print('edge angle values', len(vals), '; angle basis (cos^2, sign):', [b for b, _ in basis], flush=True)
ds = sorted({e[0] for t in T for e in t['edges']})
coords = [(d, j) for d in ds for j in range(nb)]
vec = []
for t in T:
    v = {c: F(0) for c in coords}
    for d, c, c2, sg in t['edges']:
        for j, q in enumerate(expr[(c2, sg)]): v[(d, j)] += F(c) * q
    vec.append([v[c] for c in coords])
M = sympy.Matrix([[sympy.Rational(x.numerator, x.denominator) for x in row] for row in vec]).T   # columns = types
nz = [i for i in range(M.rows) if any(M[i, j] != 0 for j in range(M.cols))]
M = M.extract(nz, list(range(M.cols)))
print('Dehn coordinates used', M.rows, '; rank of the 8 type vectors', M.rank(), flush=True)
for i, t in enumerate(T): print(f'   type {i + 1} (orbit {t["orbit_size"]}, {t["n_vertices"]} vertices): Dehn zero by itself: {all(M[r, i] == 0 for r in range(M.rows))}')
K = M.nullspace()
print('kernel dimension', len(K), flush=True)
for k in K: print('   kernel vector', [str(x) for x in (k / max(abs(x) for x in k))])
full = sympy.Matrix([t['orbit_size'] for t in T])
ctl = all(x == 0 for x in (M * full))
print('control: whole P4 (orbit sizes) has Dehn invariant 0:', ctl, flush=True)
# nonnegative kernel: extreme rays of {c >= 0, M c = 0}
from scipy.optimize import linprog
import numpy as np
Mf = np.array(M.tolist(), dtype=float); rays = set()
for i in range(len(T)):
    cvec = np.zeros(len(T)); cvec[i] = 1
    r = linprog(cvec, A_eq=Mf, b_eq=np.zeros(Mf.shape[0]), A_ub=-np.eye(len(T)), b_ub=np.zeros(len(T)),
                bounds=[(0, None)] * len(T), method='highs', options={})
    # minimise c_i subject to sum c = 1 instead: support of minimal combinations
for S in range(1, 2 ** len(T)):
    idx = [i for i in range(len(T)) if S >> i & 1]
    sub = M.extract(list(range(M.rows)), idx); ns = sub.nullspace()
    if len(ns) == 1 and all(x > 0 for x in ns[0]) or len(ns) == 1 and all(x < 0 for x in ns[0]):
        v = ns[0] if ns[0][0] > 0 else -ns[0]; l = sympy.ilcm(*[sympy.fraction(x)[1] for x in v]); v = v * l
        g = sympy.igcd(*[int(x) for x in v]); rays.add(tuple((idx[j] + 1, int(v[j] / g)) for j in range(len(idx))))
minimal = [r for r in rays if not any(set(a for a, _ in q) < set(a for a, _ in r) for q in rays)]
print('minimal Dehn-zero combinations (type: count):', sorted(minimal, key=len), flush=True)
json.dump(dict(basis=[str(b) for b, _ in basis], kernel=[[str(x) for x in k] for k in K], minimal=sorted(minimal, key=len), control=ctl),
          open(os.path.join(HERE, '../data/dehn4.json'), 'w'), indent=1)
print('FINAL ok' if ctl else 'FINAL FAIL (P4 itself not Dehn zero: the reduction is wrong)')
