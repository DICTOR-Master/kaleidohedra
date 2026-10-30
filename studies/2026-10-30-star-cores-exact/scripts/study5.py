# Star Cores study 5 (DICTO 2026-10-30 "start study 5"): the gains side by side, to test DICTO's idea of a new series of ratios. The
# classical convex solids with icosahedral, octahedral and tetrahedral symmetry (Platonic, Archimedean but the snubs, Catalan) are built
# exactly as orbits of a seed corner (and their polars) and run under DICTO's growth rule T (#38) until they return; the gain over one
# period is given exactly, with its minimal polynomial and the primes of its norm. The ten dataset solids come from study 1 (study1.json).
# Usage: ~/geom/bin/python study5.py <dataset solids dir> <exactlib dir> <out json>
import sys, os, json
SOL, LIB, OUT = sys.argv[1:4]; sys.path.insert(0, LIB)
from exactlib import *
from fractions import Fraction as Fr
import sympy
SOLIDS = ['dicto-gti', 'dicto-fpd', 'dicto-palintriacontahedron', 'dicto-icosaxes', 'dicto-unborn-axes', 'dicto-metaxyhexecontahedron',
          'dicto-tweedledum', 'dicto-samson', 'dicto-david', 'dicto-delilah']
def fkey(s): return 1 if s == 'Q' else (('cbrt', 2) if s == 'Q(2**(1/3))' else int(s[7:-2]))
def parse(s, d):
    if d == 1:
        e = sympy.Rational(sympy.sympify(s)); return QF(Fr(int(e.p), int(e.q)), 0, 5)
    e = sympy.expand(sympy.sympify(s))
    if isinstance(d, tuple):
        cs = [Fr(0)] * 3; basis = {sympy.Integer(1): 0, sympy.Integer(2) ** sympy.Rational(1, 3): 1, sympy.Integer(2) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items(): cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=2)
    a = b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        if t == 1: a += Fr(int(c.p), int(c.q))
        else: assert t == sympy.sqrt(d), s; b += Fr(int(c.p), int(c.q))
    return QF(a, b, d)
def kinds(F):
    k = {}
    for f in F: k[len(f)] = k.get(len(f), 0) + 1
    return {str(a): b for a, b in sorted(k.items())}
def rad2(V): return max((dot(v, v) for v in V), key=lambda x: x.f())
def similar(A, B, g2):
    """exact: the corners of B are k x the corners of A, k^2 = g2 (|B|^2/|A|^2), by matching each corner of B to a parallel corner of A
    with the right squared ratio; no square root needed."""
    if len(A) != len(B): return False
    for v in B:
        if not any(all(x.sign() == 0 for x in cross(u, v)) and dot(u, v).sign() > 0 and (dot(v, v) - g2 * dot(u, u)).sign() == 0 for u in A):
            return False
    return True
def gstr(x): return fmt(x)
import time, glob, itertools, numpy as np
import exactlib
def exact_order(V, f, n):
    # the face's corners in exact CCW order seen from outside (normal n): gift wrapping with exact left-turn tests (float angle sorting
    # fails on the very short edges the long chains make)
    start = min(f, key=lambda j: tuple(x.f() for x in V[j])); order = [start]
    while True:
        a = order[-1]; cand = None
        for b in f:
            if b == a: continue
            if cand is None: cand = b; continue
            s = dot(cross(sub(V[cand], V[a]), sub(V[b], V[a])), n).sign()
            if s < 0: cand = b                     # b lies to the right of a->cand: wrap tighter
        if cand == start: break
        order.append(cand)
        assert len(order) <= len(f)
    return order
def hull_exact_order(points):
    P = list(dict.fromkeys(tuple(p) for p in points))
    from scipy.spatial import ConvexHull
    X = np.array([fv(p) for p in P]); cen = X.mean(0); ch = ConvexHull(X); planes = {}
    for simp in ch.simplices:
        a, b, c = (P[i] for i in simp); n = cross(sub(b, a), sub(c, a))
        if all(x.sign() == 0 for x in n): continue
        planes[plane_key(n, dot(n, a))] = (n, dot(n, a))
    good = {}
    for key, (n, cc) in planes.items():
        sg = [(dot(n, p) - cc).sign() for p in P]
        if all(x <= 0 for x in sg): good[key] = (n, cc, [i for i, x in enumerate(sg) if x == 0])
        elif all(x >= 0 for x in sg): good[key] = (mul(-1, n), -cc, [i for i, x in enumerate(sg) if x == 0])
        else: raise AssertionError('float facet is not a supporting plane')
    on = {i: [] for i in range(len(P))}
    for key, (n, cc, idx) in good.items():
        for i in idx: on[i].append(n)
    corners = [i for i in range(len(P)) if len(on[i]) >= 3 and any(det3(*t).sign() != 0 for t in itertools.combinations(on[i], 3))]
    V = [P[i] for i in corners]; vid = {i: k for k, i in enumerate(corners)}; F = []
    for key, (n, cc, idx) in good.items():
        f = [vid[i] for i in idx if i in vid]; assert len(f) >= 3
        order = exact_order(V, f, n)
        assert len(order) == len(f), 'a face point is not a corner of the face'
        F.append(order)
    exactlib.check_closed(V, F)
    return V, F
exactlib.hull = hull_exact_order; hull = hull_exact_order

import sympy as sp
def matmul(A, B): return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), A[0][0] * 0) for j in range(3)) for i in range(3))
def apply(M, v): return tuple(sum((M[i][k] * v[k] for k in range(3)), v[0] * 0) for i in range(3))
def group(gens, one):
    G = {one}; frontier = [one]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                x = matmul(g, h)
                k = tuple(fmt(e) for r in x for e in r)
                if x not in G: G.add(x); nxt.append(x)
        frontier = nxt
    return G
def mat(rows, d): return tuple(tuple(x if isinstance(x, QF) else QF(x, 0, d) for x in r) for r in rows)
H = Fr(1, 2); ph = PHI; iph = PHI - 1
I5 = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 5)
Cyc5 = mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]], 5); Sg5 = mat([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], 5); Inv5 = mat([[-1, 0, 0], [0, -1, 0], [0, 0, -1]], 5)
R5 = mat([[QF(H, 0, 5), -ph * H, iph * H], [ph * H, iph * H, QF(-H, 0, 5)], [iph * H, QF(H, 0, 5), ph * H]], 5)
Ih = group([Cyc5, Sg5, R5, Inv5], I5)
_ico = (QF(0, 0, 5), QF(1, 0, 5), PHI)
if len({apply(g, _ico) for g in Ih}) != 12:   # R5 belongs to the other orientation of the icosahedral group: conjugate it by the x<->y swap
    W = mat([[0, 1, 0], [1, 0, 0], [0, 0, 1]], 5); Ih = group([Cyc5, Sg5, matmul(matmul(W, R5), W), Inv5], I5)
assert len({apply(g, _ico) for g in Ih}) == 12, 'icosahedron orbit'
def oh(d):
    one = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]], d)
    return group([mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]], d), mat([[0, 1, 0], [1, 0, 0], [0, 0, 1]], d), mat([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], d)], one)
def td(d):
    one = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]], d)
    return group([mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]], d), mat([[0, 1, 0], [1, 0, 0], [0, 0, 1]], d), mat([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], d)], one)
Oh1, Oh2, Td1 = oh(5), oh(2), td(5)
print('group orders', len(Ih), len(Oh1), len(Oh2), len(Td1), flush=True)
def orbit(G, seed): return list({apply(g, seed) for g in G})
q = lambda a, b=0, d=5: QF(Fr(a), Fr(b), d)
r2 = lambda a, b=0: QF(Fr(a), Fr(b), 2)
SEEDS = [  # name, group, seed corner (standard coordinates)
    ('tetrahedron', Td1, (q(1), q(1), q(1))), ('truncated tetrahedron', Td1, (q(3), q(1), q(1))),
    ('octahedron', Oh1, (q(1), q(0), q(0))), ('cube', Oh1, (q(1), q(1), q(1))), ('cuboctahedron', Oh1, (q(1), q(1), q(0))),
    ('truncated octahedron', Oh1, (q(0), q(1), q(2))), ('truncated cube', Oh2, (r2(-1, 1), r2(1), r2(1))),
    ('rhombicuboctahedron', Oh2, (r2(1), r2(1), r2(1, 1))), ('truncated cuboctahedron', Oh2, (r2(1), r2(1, 1), r2(1, 2))),
    ('icosahedron', Ih, (q(0), q(1), ph)), ('dodecahedron', Ih, (q(1), q(1), q(1))), ('icosidodecahedron', Ih, (q(0), q(0), ph)),
    ('truncated icosahedron', Ih, (q(0), q(1), 3 * ph)), ('truncated dodecahedron', Ih, (q(0), 2 + ph, iph)),
    ('rhombicosidodecahedron', Ih, (q(1), q(1), ph * ph * ph)), ('truncated icosidodecahedron', Ih, (iph, iph, 3 + ph))]
DUAL = {'tetrahedron': None, 'octahedron': None, 'cube': None, 'icosahedron': None, 'dodecahedron': None,
        'truncated tetrahedron': 'triakis tetrahedron', 'cuboctahedron': 'rhombic dodecahedron', 'truncated octahedron': 'tetrakis hexahedron',
        'truncated cube': 'triakis octahedron', 'rhombicuboctahedron': 'deltoidal icositetrahedron', 'truncated cuboctahedron': 'disdyakis dodecahedron',
        'icosidodecahedron': 'rhombic triacontahedron', 'truncated icosahedron': 'pentakis dodecahedron', 'truncated dodecahedron': 'triakis icosahedron',
        'rhombicosidodecahedron': 'deltoidal hexecontahedron', 'truncated icosidodecahedron': 'disdyakis triacontahedron'}
x = sp.Symbol('x')
def gain_info(g2):
    e = sp.sympify(fmt(g2)); g = sp.sqrt(e); g = sp.nsimplify(sp.sqrtdenest(sp.simplify(g)))
    mp = sp.minimal_polynomial(g, x); C = sp.Poly(mp, x).all_coeffs(); norm = sp.Rational(C[-1], C[0]) * (-1) ** (len(C) - 1)
    return dict(gain_radius=str(sp.simplify(g)), minpoly=str(mp), norm=str(norm), norm_primes={str(k): int(v) for k, v in sp.factorrat(norm).items()}, decimal=float(g))
def run(name, V0):
    V, F = hull(V0); hist = [(V, F, rad2(V))]; S = V; row = dict(solid=name, steps=[])
    for k in range(1, 9):
        S, SF = ustep(S); r = rad2(S)
        st = dict(step=k, corners=len(S), faces=kinds(SF)); row['steps'].append(st)
        for j, (A, AF, ra) in enumerate(hist):
            if kinds(AF) == kinds(SF) and similar(A, S, r / ra):
                row.update(enters_cycle_at_step=j, period=k - j, gain_radius_squared=fmt(r / ra)); row.update(gain_info(r / ra)); break
        hist.append((S, SF, r))
        if 'period' in row or len(S) > 600: break
    print(name, {k: v for k, v in row.items() if k != 'steps'}, flush=True); return row
res = []
ONLY = sys.argv[4].split(',') if len(sys.argv) > 4 else None   # names to rerun
for name, G, seed in SEEDS:
    if ONLY and name not in ONLY: continue
    try:
        P = orbit(G, seed); res.append(run(name, P))
        if DUAL[name]:
            V, F = hull(P); res.append(run(DUAL[name], polar(V, F, dot(seed, seed))))
    except Exception as e:
        res.append(dict(solid=name, error=type(e).__name__ + ' ' + str(e)[:150])); print(name, 'ERROR', e, flush=True)
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('done', flush=True)
