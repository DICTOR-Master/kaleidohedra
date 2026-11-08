# certificate.py -- exact (rational) proof of the octahedral covering lemma, case B.
#
# Claim (case B). For all a, b in the chamber cone T = cone(e1, e1+e2, e1+e2+e3) = {x1 >= x2 >= x3 >= 0}
#     max over improper h in O_h of  a.(h b)  >=  |a| |b| / sqrt3.
# Method. Split T x T into product cells cone(V) x cone(W) (V, W: three rational generators each).
# On each cell pick fixed weights lam_k >= 0, sum = 1 (exact rationals) on improper matrices H_k and
# L(a, b) = sum_k lam_k a.(H_k b)  (bilinear, <= the max).  If for all generator pairs (v, w)
#     L(v, w) >= 0   and   3 L(v, w)^2 >= |v|^2 |w|^2           (*)
# then L(a, b) >= |a||b|/sqrt3 on the whole cell (vertex lemma: write a = sum al_i v_i, al_i >= 0;
# L(a, w) = sum al_i L(v_i, w) >= |w|/sqrt3 sum al_i |v_i| >= |w||a|/sqrt3 by the triangle inequality;
# then the same in b).  (*) is checked in exact rational arithmetic (fractions.Fraction); floats are
# used only to FIND the weights (scipy LP), never to decide.
import itertools, sys, time, json
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

t0 = time.time()

def signed_perms():
    P, I = [], []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = [[0] * 3 for _ in range(3)]
            for i, j in enumerate(perm):
                M[j][i] = sg[i]
            det = round(np.linalg.det(np.array(M, float)))
            (P if det == 1 else I).append(M)
    return P, I

PROP, IMPR = signed_perms()
assert len(PROP) == 24 and len(IMPR) == 24
H = IMPR                                     # case B uses the 24 improper elements
Hn = np.array(H, float)

def dot(x, y): return sum(p * q for p, q in zip(x, y))
def mat(M, x): return [sum(M[i][j] * x[j] for j in range(3)) for i in range(3)]
def nrm2(x): return dot(x, x)

def ok_pair(L, v, w):
    """exact test of (*)"""
    return L >= 0 and 3 * L * L >= nrm2(v) * nrm2(w)

def Lval(lam, v, w):
    return sum(l * dot(v, mat(H[k], w)) for k, l in lam.items())

def unit(x):
    x = np.array([float(t) for t in x]); return x / np.linalg.norm(x)

def is_crit(v, w):
    """the two equality pairs (e1, e1+e2+e3) and (e1+e2+e3, e1), up to positive scaling"""
    def ray(x, y):
        return all(x[i] * y[j] == x[j] * y[i] for i in range(3) for j in range(3))
    e1, c3 = [1, 0, 0], [1, 1, 1]
    return (ray(v, e1) and ray(w, c3)) or (ray(v, c3) and ray(w, e1))

C = 1 / np.sqrt(3)

def find_weights(V, W):
    """LP: maximise t with sum lam_k a.(H_k b) >= C + t on non-critical pairs, >= C on critical ones."""
    rows, rhs = [], []
    for v in V:
        for w in W:
            vu, wu = unit(v), unit(w)
            vals = np.einsum('kij,j,i->k', Hn, wu, vu)
            crit = is_crit(v, w)
            rows.append(np.concatenate([-vals, [0.0 if crit else 1.0]])); rhs.append(-C)
    nk = len(H)
    res = linprog(np.concatenate([np.zeros(nk), [-1.0]]), A_ub=np.array(rows), b_ub=np.array(rhs),
                  A_eq=np.array([np.concatenate([np.ones(nk), [0.0]])]), b_eq=[1.0],
                  bounds=[(0, None)] * nk + [(None, 1.0)], method='highs')
    if res.status != 0:
        return None, -1.0
    return res.x[:nk], res.x[-1]

def rationalise(x, den=10**6):
    lam = {k: Fr(float(t)).limit_denominator(den) for k, t in enumerate(x) if t > 1e-9}
    s = sum(lam.values())
    lam = {k: l / s for k, l in lam.items()}        # exact: sum = 1, all >= 0
    assert sum(lam.values()) == 1 and all(l >= 0 for l in lam.values())
    return lam

def exact_cell(lam, V, W):
    return all(ok_pair(Lval(lam, v, w), v, w) for v in V for w in W)

def ang(x, y):
    return np.degrees(np.arccos(np.clip(unit(x) @ unit(y), -1, 1)))

def mid(x, y, den=64):
    """rational point strictly inside the edge, close to the arc midpoint: al x + be y with al, be > 0"""
    al = Fr(1 / np.sqrt(float(nrm2(x)))).limit_denominator(den)
    be = Fr(1 / np.sqrt(float(nrm2(y)))).limit_denominator(den)
    assert al > 0 and be > 0
    m = [al * p + be * q for p, q in zip(x, y)]
    g = max(abs(t.denominator) for t in m)       # clear denominators (direction only matters)
    return [t * g for t in m]

def split(T):
    """longest-edge bisection of the cone triangle T (three generators)"""
    pairs = [(0, 1), (1, 2), (0, 2)]
    i, j = max(pairs, key=lambda p: ang(T[p[0]], T[p[1]]))
    k = 3 - i - j
    m = mid(T[i], T[j])
    return [[T[i], m, T[k]], [m, T[j], T[k]]]

def diam(T):
    return max(ang(T[0], T[1]), ang(T[1], T[2]), ang(T[0], T[2]))

ROOT = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
MAXDEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 40
cert, stack, nlp = [], [(ROOT, ROOT, 0)], 0
fail = None
while stack:
    V, W, d = stack.pop()
    x, t = find_weights(V, W); nlp += 1
    if x is not None and t > -1e-12:
        lam = rationalise(x)
        if exact_cell(lam, V, W):
            cert.append({'V': [[str(c) for c in v] for v in V], 'W': [[str(c) for c in w] for w in W],
                         'lam': {str(k): str(l) for k, l in lam.items()}})
            continue
    if d >= MAXDEPTH:
        fail = (V, W, t); break
    if diam(V) >= diam(W):
        for Vs in split(V): stack.append((Vs, W, d + 1))
    else:
        for Ws in split(W): stack.append((V, Ws, d + 1))
    if nlp % 2000 == 0:
        print(f'  heartbeat: {nlp} LPs, {len(cert)} cells certified, stack {len(stack)}, {time.time()-t0:.0f}s', flush=True)

print(f'LPs solved: {nlp}; certified product cells: {len(cert)}; time {time.time()-t0:.1f}s')

# ---- independent re-check of the certificate: (1) every cell passes (*) exactly; (2) the cells tile T x T.
# (2) is by construction (each split replaces a cone triangle by its two halves along a rational point
# of one edge); as an extra exact check the cells' volumes in the barycentric chart add up:
# the normalised det of each cone triangle in the coordinates of ROOT sums to 1 for every fixed partner.
def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))

recheck = True
for cell in cert:
    V = [[Fr(c) for c in v] for v in cell['V']]; W = [[Fr(c) for c in w] for w in cell['W']]
    lam = {int(k): Fr(l) for k, l in cell['lam'].items()}
    if not (sum(lam.values()) == 1 and all(l >= 0 for l in lam.values()) and exact_cell(lam, V, W)):
        recheck = False

# tiling check in the projective (simplex) chart: map a generator x to x / (x.(1,0,0)) ... use the
# simplex chart x -> x / s(x) with s(x) = coordinates in ROOT basis summed; area = |det| of the chart
# points, which is additive under edge bisection.
Rinv = np.linalg.inv(np.array(ROOT, float).T)
def chart(x):
    # exact barycentric coordinates in ROOT: x = c1 e1 + c2 (e1+e2) + c3 (e1+e2+e3)
    x = [Fr(t) for t in x]
    c3_ = x[2]; c2_ = x[1] - x[2]; c1_ = x[0] - x[1]
    s = c1_ + c2_ + c3_
    return [c1_ / s, c2_ / s, c3_ / s]
def area(T):
    p = [chart(x) for x in T]
    return abs(det3(p[0], p[1], p[2]))
tot = sum(area([[Fr(c) for c in v] for v in cell['V']]) * area([[Fr(c) for c in w] for w in cell['W']]) for cell in cert)
tiling = (tot == 1)
print('exact re-check of every cell:', recheck, '| product areas sum to exactly 1:', tiling, f'({tot})')
used = sorted({int(k) for cell in cert for k in cell['lam']})
print('improper elements used by the certificate:', [H[k] for k in used])
maxw = max(len(cell['lam']) for cell in cert)
print('largest number of matrices mixed in one cell:', maxw)
json.dump({'claim': 'case B, max_h improper a.(h b) >= |a||b|/sqrt3 on T x T', 'H': H, 'cells': cert},
          open('certificate.json', 'w'))
ok = fail is None and recheck and tiling
print('FINAL ok' if ok else f'FINAL FAIL: fail={fail is not None} recheck={recheck} tiling={tiling}')
