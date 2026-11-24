"""(The angle table below was a first attempt: the angles are not rational multiples of pi; the fan identity is used.)
Exact curvature for the 3 dice whose corners all have equal curvature in ball arithmetic but are not all congruent.
At each corner the normal cone is a spherical polygon on the unit normals. Each inner angle A satisfies, with unnormalised
exact normals a (previous), b (corner), c (next) over Q(sqrt5):
  cos A = ((a.c)|b|^2 - (a.b)(b.c)) / (|a x b| |b x c|),  so cos^2 A and the sign of cos A are exact in Q(sqrt5).
An angle is identified exactly as j*pi/60 when cos(2A) = 2cos^2 A - 1 equals cos(j*pi/30) for j in {0,6,10,12,15,18,20,24,30,...}
(the values in Q(sqrt5)) and the sign of cos A matches. Curvature = sum of angles - (n - 2) pi, exactly.  FINAL ok if all three are proved."""
import os, sys, math, json
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import polar_aequi as PA
from q5 import Q, PHI
import numpy as np
C = PA.C
EX = [tuple(Q(a) + Q(b) * PHI for a, b in q) for q in C.EXACT]
def d(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def x(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
S5 = Q(0, 1)
COS = {0: Q(1), 6: (Q(1) + S5) / 4, 10: Q(Fr(1, 2)), 12: (S5 - 1) / 4, 15: Q(0)}      # cos(j pi/30)
for j in list(COS):
    COS[30 - j] = -COS[j]
def angle(a, b, c):
    num = d(a, c) * d(b, b) - d(a, b) * d(b, c); den2 = d(x(a, b), x(a, b)) * d(x(b, c), x(b, c))
    c2 = num * num / den2; cos2A = 2 * c2 - 1
    A = math.acos(max(-1, min(1, math.copysign(math.sqrt(c2.f()), num.f()))))
    j = round(2 * A / math.pi * 30)
    if j not in COS or COS[j] != cos2A: return None
    if (num.sign() >= 0) != (j <= 15): return None
    return Fr(j, 60)                                       # A = (j/60) pi
WANT = {('4404', 2009), ('2a', 1967), ('2a', 4289)}
out = []; ok = True
for rec in PA.records():
    if (rec['part'], rec['sid']) not in WANT: continue
    if rec['part'] == '4404' and rec['study'] != '2026-11-19-aequi-complete': continue
    idx = rec['idx']; V, inc = C.combinatorics(idx, rec['sizes'], rec['depths']); nf = C.DIRS[idx]; kap = set()
    for I in inc:
        m = sum(nf[i] for i in I); m = m / np.linalg.norm(m)
        e1 = np.cross(m, [1, 0, 0] if abs(m[0]) < 0.9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(m, e1)
        o = sorted(I, key=lambda i: np.arctan2(nf[i] @ e2, nf[i] @ e1)); n = len(o)
        # Van Oosterom-Strackee fan: tan(E_t/2) = T_t / D_t with unit vectors; here all normals have one squared norm nn,
        # so T_t^2 = det^2/nn^3 and D_t = 1 + (ab + bc + ca)/nn are exact in Q(sqrt5).  Target: total E = 4 pi / N.
        q = [EX[idx[i]] for i in o]; nn = d(q[0], q[0])
        if any(d(v, v) != nn for v in q) or n != 3: ok = False; kap.add('not handled'); continue
        a, b, c = q; tt = d(a, x(b, c)); T2 = tt * tt / (nn * nn * nn); D = 1 + (d(a, b) + d(b, c) + d(c, a)) / nn
        kap.add(('E=pi/3 exactly' if (3 * T2 == D * D and D.sign() > 0) else 'other'))
    N = len(V); r = dict(part=rec['part'], sid=rec['sid'], label=rec['label'], corners=N, curvatures_over_pi=sorted(kap), target_over_pi=str(Fr(4, N)))
    ok &= (N == 12 and kap == {'E=pi/3 exactly'}); out.append(r); print(r)
json.dump(out, open(os.path.join(HERE, '..', 'data', 'angles-exact.json'), 'w'), indent=1)
if ok and len(out) == 3: print('FINAL ok')
