# bird2_base.py -- DICTO Hopscotch, icosahedral line, bird 2 (study 2026-11-09-icosahedral-line): the exact base of #43 Theorem N.
# Copy of studies/2026-11-09-og-margin/scripts/exact_family.py (exact builds of the OG downward family D_0..D_12, t_min checks unchanged)
# with, at every level, the exact face distances: r(D_k)^2, the five-fold face distance^2, R(D_k)^2, and the new-face minimum nu(D_k)^2
# (faces whose normal is not a face normal of D_{k-1}); then the exact checks r(D_9) < ... < r(D_12) on the five-fold faces and
# r(D_12) >= (phi^2/3) R(D_11) = 1.084154 (the base value of Theorem N), all by exact signs.
# Original header: EXACT t_min(D_k) in Q(sqrt5) beyond Table 7 (k = 0..8).
# D_0 = OG (exact, five-fold-octet tools), D_k = P(D_{k-1}); t_min(D_k) = max over listed points v of D_k and faces (m, d) of D_{k+1}
# of m.v/d (points inside the hull never give more, so listing all points is safe).
# Method: float hull only GUESSES the faces; every face is then proved exactly: plane through 3 points (exact cross product), every
# point of the list exactly on the inner side, members = points exactly on the plane; each proved face is carried round its orbit by
# the 60 exact rotations. Completeness: every polygon edge lies in exactly two proved faces, so the proved faces close up; a closed
# sub-collection of the faces of a convex polytope is all of them (the boundary is a connected sphere). Symmetry also reduces t_min:
# max over all points v and face representatives only (g maps faces to faces and fixes the point set).
# Arithmetic: a + b sqrt5 with gmpy2 rationals; signs exact.
# usage: python -u exact_family.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time, itertools
import numpy as np, gmpy2
from gmpy2 import mpq
from scipy.spatial import ConvexHull
OUT = os.path.abspath(sys.argv[3])                      # resolved before the chdir below
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG, G (Fraction-based Q5)
KMAX = int(sys.argv[2])
S5 = 5 ** .5

class R5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = a if isinstance(a, type(mpq(0))) else mpq(a); s.b = b if isinstance(b, type(mpq(0))) else mpq(b)
    def __add__(s, o): return R5(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return R5(s.a - o.a, s.b - o.b)
    def __neg__(s): return R5(-s.a, -s.b)
    def __mul__(s, o): return R5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return R5(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * o.inv()
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > 5 * b * b else -1)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def digits(s): return max(len(str(abs(x.numerator))) + len(str(x.denominator)) for x in (s.a, s.b))
    def __repr__(s): return f'{s.a}+{s.b}r5'

def cv(x): return R5(mpq(x.a.numerator, x.a.denominator), mpq(x.b.numerator, x.b.denominator))
Z = R5(0)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def sub(u, v): return (u[0] - v[0], u[1] - v[1], u[2] - v[2])
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
GX = [tuple(tuple(cv(x) for x in row) for row in M) for M in G]
def app(M, v): return tuple(M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2] for i in range(3))
Gf = np.array([[[x.f() for x in row] for row in M] for M in GX])
fl = lambda v: np.array([x.f() for x in v])
PHI = R5(mpq(1, 2), mpq(1, 2)); TARGET = R5(3) / (PHI * PHI)            # 3/phi^2 = (9 - 3 sqrt5)/2

def float_faces(Wf, tol=1e-9):
    h = ConvexHull(Wf); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    groups = {}
    for f in range(n): groups.setdefault(find(f), []).append(f)
    return h, list(groups.values())

def exact_faces(W, idx, Wf):
    h, groups = float_faces(Wf)
    normals_f = [h.equations[g[0], :3] for g in groups]
    key = lambda m: min(tuple(np.round(M @ m, 6)) for M in Gf)
    reps = {}
    for gi, m in enumerate(normals_f): reps.setdefault(key(m), gi)
    faces = {}
    for gi in reps.values():
        a, b, c = (W[j] for j in h.simplices[groups[gi][0]])
        n = cross(sub(b, a), sub(c, a)); d = dot(n, a)
        sg = [(dot(n, w) - d).sign() for w in W]
        if any(s > 0 for s in sg): n = tuple(-x for x in n); d = -d; sg = [-s for s in sg]
        assert all(s <= 0 for s in sg), 'triangle plane is not supporting (exact)'
        mem = frozenset(j for j, s in enumerate(sg) if s == 0)
        if mem in faces: continue
        for M in GX:
            mem2 = frozenset(idx[app(M, W[j])] for j in mem)
            if mem2 not in faces: faces[mem2] = (app(M, n), d, mem2 == mem)
    # completeness: every polygon edge in exactly two proved faces (closed), and count equals the float count
    edges = {}
    for mem in faces:
        mm = sorted(mem); P = Wf[mm]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]
        o = [mm[k] for k in np.argsort(np.arctan2((P - c0) @ B[1], (P - c0) @ B[0]))]
        for e in zip(o, o[1:] + o[:1]): edges[frozenset(e)] = edges.get(frozenset(e), 0) + 1
    closed = all(v == 2 for v in edges.values()) and len(faces) == len(groups)
    assert closed, f'proved faces do not close up ({len(faces)} proved, {len(groups)} float)'
    corners = len(set(j for mem in faces for j in mem))   # points on some face (upper bound on corners; info only)
    return faces, len(edges), corners

t0 = time.time()
W = [tuple(cv(x) for x in v) for v in OG]
TABLE7_EXACT = {0: '(445 - 16√5)/361', 1: '(5941 - 1622√5)/2071', 2: '(247111 - 104650√5)/11881', 3: '(9 - 3√5)/2', 4: '(21 - √5)/18'}
CHECK = {0: R5(mpq(445, 361), mpq(-16, 361)), 1: R5(mpq(5941, 2071), mpq(-1622, 2071)), 2: R5(mpq(247111, 11881), mpq(-104650, 11881)),
         3: R5(mpq(9, 2), mpq(-3, 2)), 4: R5(mpq(21, 18), mpq(-1, 18))}
TABLE7 = [1.133581, 1.117382, 1.103147, 1.145898, 1.042441, 1.086902, 1.025657, 1.059516, 1.138077]
res = {'mark': 'DICTO #43 Conjecture 1, exact base of Theorem N (icosahedral-line study), 2026-11-09 · DICTO · dictospheres.com', 'k': {}, 'level': {}}
LV = {}; prevnormals = None
ok_all = True; prev = None
for k in range(KMAX + 2):
    t = time.time()
    idx = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W])
    F, ne, oncount = exact_faces(W, idx, Wf)
    print(f'D_{k}: {len(W)} listed points, {len(F)} faces proved exactly, {ne} edges, max digits {max(x.digits() for v in W for x in v)} ({time.time() - t:.0f} s)', flush=True)
    # exact face distances of D_k
    R2 = max((dot(v, v) for v in W), key=lambda q: q.f())
    assert all((dot(v, v) - R2).sign() <= 0 for v in W)
    reps_all = [(n, d) for n, d, isrep in F.values() if isrep]
    def stab(n): return sum(1 for M in GX if app(M, n) == n)
    info = []
    for n, d in reps_all:
        nn = dot(n, n); dist2 = d * d / nn
        osz = 60 // stab(n)
        new = None
        if prevnormals is not None:
            nf_ = fl(n) / np.linalg.norm(fl(n))
            cand = [m for m, mf in prevnormals if mf @ nf_ > 1 - 1e-9]
            new = not any(all(x == Z for x in cross(n, m)) and dot(n, m).sign() > 0 for m in cand)
        info.append((dist2, osz, new))
    r2 = min((q[0] for q in info), key=lambda q: q.f())
    assert all((q[0] - r2).sign() >= 0 for q in info)
    five = [q[0] for q in info if q[1] == 12]
    newd = [q[0] for q in info if q[2]]
    nu2 = min(newd, key=lambda q: q.f()) if newd else None
    if nu2 is not None: assert all((q - nu2).sign() >= 0 for q in newd)
    LV[k] = {'R2': R2, 'r2': r2, 'five2': five[0] if five else None, 'nu2': nu2}
    res['level'][k] = {'R': R2.f() ** .5, 'r': r2.f() ** .5, 'five_fold_face_distance': five[0].f() ** .5 if five else None,
                       'r_on_five_fold_face': bool(five) and five[0] == r2, 'new_face_min': nu2.f() ** .5 if nu2 is not None else None,
                       'face_orbits': len(info), 'new_face_orbits': sum(1 for q in info if q[2]), 'r2_exact_digits': r2.digits(),
                       'r2_exact': repr(r2) if r2.digits() < 200 else None}
    print(f'  D_{k}: R = {R2.f() ** .5:.9f}, r = {r2.f() ** .5:.9f}, five-fold face {five[0].f() ** .5 if five else float("nan"):.9f}'
          f'{" (carries r)" if five and five[0] == r2 else ""}, new faces {sum(1 for q in info if q[2])} of {len(info)} orbits, '
          f'new-face min {nu2.f() ** .5 if nu2 is not None else float("nan"):.9f}', flush=True)
    prevnormals = [(n, fl(n) / np.linalg.norm(fl(n))) for n, d, _ in F.values()]
    if prev is not None:                       # t_min(D_{k-1}) against the faces of D_k
        Wp, Wpf = prev
        reps = [(n, d) for n, d, isrep in F.values() if isrep]
        nf = np.array([fl(n) for n, d in reps]); df = np.array([d.f() for n, d in reps])
        vals = (Wpf @ nf.T) / df[None, :]; i, j = np.unravel_index(np.argmax(vals), vals.shape)
        n0, d0 = reps[j]; tm = dot(n0, Wp[i]) / d0
        exact_max = all((dot(n, v) - tm * d).sign() <= 0 for n, d in reps for v in Wp)
        below = (tm - TARGET).sign() <= 0
        good = exact_max; kk = k - 1
        if kk in CHECK: good &= tm == CHECK[kk]
        elif kk < len(TABLE7): good &= abs(tm.f() - TABLE7[kk]) < 2e-6
        ok_all &= good and below
        res['k'][kk] = {'t_min_float': tm.f(), 't_min_exact': repr(tm) if tm.digits() < 4000 else f'{tm.digits()} digits', 'exact_max': exact_max,
                        'le_3_over_phi2_exact': below, 'target_minus_t_min': (TARGET - tm).f(), 'faces_of_next': len(F), 'listed_points': len(Wp)}
        print(f'  t_min(D_{kk}) = {tm.f():.12f}  exact max {exact_max}  <= 3/phi^2 exactly: {below}  (3/phi^2 - t = {(TARGET - tm).f():+.6f}; digits {tm.digits()})'
              f'{"  matches Table 7" if kk <= 8 and good else ""}', flush=True)
        json.dump(res, open(OUT, 'w'), indent=1)
    if k == KMAX + 1: break
    feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    prev = (W, Wf); W = list(feet)
# the exact base of Theorem N
if KMAX < 11:
    print('pilot run (KMAX < 11): base checks need D_12; levels:', sorted(LV)); print('FINAL ok' if ok_all else 'FINAL FAIL: t_min'); sys.exit()
P2 = PHI * PHI; P4 = P2 * P2
base = {}
base['r(D_k) is carried by the five-fold faces for k = 10, 11, 12 (exact)'] = all(LV[k]['five2'] is not None and LV[k]['five2'] == LV[k]['r2'] for k in (10, 11, 12))
base['five-fold face distance strictly increasing D_9 < D_10 < D_11 < D_12 (exact)'] = all((LV[k + 1]['five2'] - LV[k]['five2']).sign() > 0 for k in (9, 10, 11))
base['r(D_9) < r(D_10) < r(D_11) < r(D_12) (exact)'] = all((LV[k + 1]['r2'] - LV[k]['r2']).sign() > 0 for k in (9, 10, 11))
thr2 = P4 * LV[11]['R2'] / R5(9)
base['r(D_12) >= (phi^2/3) R(D_11) (exact, squares)'] = (LV[12]['r2'] - thr2).sign() > 0
print('info: new faces of D_k above the threshold (exact), k = 1..12:', {k: LV[k]['nu2'] is None or (LV[k]['nu2'] - thr2).sign() > 0 for k in range(1, 13)})
base['R(D_k) non-increasing k = 0..12 (exact)'] = all((LV[k + 1]['R2'] - LV[k]['R2']).sign() <= 0 for k in range(12))
print(f'threshold (phi^2/3) R(D_11) = {thr2.f() ** .5:.9f}; r(D_12) = {LV[12]["r2"].f() ** .5:.9f} (exact r^2 has {LV[12]["r2"].digits()} digits); margin {LV[12]["r2"].f() ** .5 / thr2.f() ** .5 - 1:+.4%}')
print('new-face minima nu(D_k):', {k: round(LV[k]['nu2'].f() ** .5, 9) for k in LV if LV[k]['nu2'] is not None})
res['base'] = {k: bool(v) for k, v in base.items()}; res['threshold'] = thr2.f() ** .5
json.dump(res, open(OUT, 'w'), indent=1)
for kk, v in base.items(): print(('  ok   ' if v else '  FAIL ') + kk)
print(f'done in {time.time() - t0:.0f} s')
print('FINAL ok' if ok_all and all(base.values()) else 'FINAL FAIL: a t_min check or a base check failed')
