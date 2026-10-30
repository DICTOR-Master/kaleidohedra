# Star Cores study 3 (DICTO 2026-10-31 "meanwhile start study 6", with study 3 next in the plan): a search for counter-examples to the
# book's main statement. Every convex solid whose face planes lie in two families, on two kinds of symmetry axis (icosahedral 5+3, 5+2,
# 3+2; octahedral 4+3, 4+2, 3+2), is swept over the ratio of the two plane distances, exactly; three-family solids (5+3+2, 4+3+2) are
# swept as the contrast. Each is run under DICTO's growth rule T (#38) until it returns, and its cores (#78, Proposition 5) are turned
# until they return. Main statement: two families give hulls of period four (two for one family) and cores of period two.
# A solid with planes at the feet s*n (n an axis vector) is T of the points s*n: halfspace_solid([(s n, s^2 n.n)]).
# Usage: ~/geom/bin/python study3.py <exactlib dir> <out json> [fine]
import sys, os, json
LIB, OUT = sys.argv[1:3]; sys.path.insert(0, LIB)
from exactlib import *
from fractions import Fraction as Fr
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
def core_turn(V, F):
    """the core of one turn at t = 1 (any t only scales it by t): the faces grouped into families (number of sides, distance of the face
    plane from the centre); the tips at the feet of the face perpendiculars; the hull of each family's tips that is solid; the core =
    their intersection."""
    fam = {}
    for f, (n, c) in zip(F, face_planes(V, F)):
        foot = mul(c / dot(n, n), n); fam.setdefault((len(f), fmt(dot(foot, foot))), []).append(foot)
    planes = []; used = 0
    for key, T in fam.items():
        if len(T) < 4: continue
        try: A, AF = hull(T)
        except Exception: continue
        if len(A) < 4: continue
        planes += face_planes(A, AF); used += 1
    C, CF = halfspace_solid(planes)
    return C, CF, len(fam), used
q = lambda a, b=0, d=5: QF(Fr(a), Fr(b), d)
AX = {'Ih': {5: orbit(Ih, (q(0), q(1), ph)), 3: orbit(Ih, (q(1), q(1), q(1))), 2: orbit(Ih, (q(0), q(0), ph))},
      'Oh': {4: orbit(Oh1, (q(1), q(0), q(0))), 3: orbit(Oh1, (q(1), q(1), q(1))), 2: orbit(Oh1, (q(1), q(1), q(0)))}}
for g, A in AX.items(): print(g, {k: len(v) for k, v in A.items()}, flush=True)
assert [len(AX['Ih'][k]) for k in (5, 3, 2)] == [12, 20, 30] and [len(AX['Oh'][k]) for k in (4, 3, 2)] == [6, 8, 12]
GRID = [q(Fr(a, 8)) for a in range(5, 17)] + [iph, ph * Fr(1, 2), q(Fr(1, 2), Fr(1, 4)), ph * ph * Fr(1, 3)]   # s of the second family
GRID3 = [q(Fr(a, 4)) for a in range(3, 8)] + [iph, q(Fr(1, 2), Fr(1, 4))]
def solid(fams):
    planes = []
    for P, s in fams: planes += [(mul(s, n), s * s * dot(n, n)) for n in P]
    V, F = halfspace_solid(planes); return V, F
def tchain(V, F):
    hist = [(V, F, rad2(V))]; S = V
    for k in range(1, 9):
        S, SF = ustep(S); r = rad2(S)
        for j, (A, AF, ra) in enumerate(hist):
            if kinds(AF) == kinds(SF) and similar(A, S, r / ra): return dict(enters=j, period=k - j, gain2=fmt(r / ra), corners=len(S))
        hist.append((S, SF, r))
        if len(S) > 600: break
    return dict(period=None, steps=k, corners=len(S))
def cchain(V, F):
    hist = [(V, F, rad2(V))]; S, SF = V, F
    for k in range(1, 7):
        S, SF, nf, used = core_turn(S, SF); r = rad2(S)
        for j, (A, AF, ra) in enumerate(hist):
            if kinds(AF) == kinds(SF) and similar(A, S, r / ra): return dict(enters=j, period=k - j, gain2_t1=fmt(r / ra), families=nf)
        hist.append((S, SF, r))
        if len(S) > 400: break
    return dict(period=None, turns=k)
CASES = []
for g, (a, b) in [('Ih', (5, 3)), ('Ih', (5, 2)), ('Ih', (3, 2)), ('Oh', (4, 3)), ('Oh', (4, 2)), ('Oh', (3, 2))]:
    for s in GRID: CASES.append((g, (a, b), (q(1), s)))
for g, ax in [('Ih', (5, 3, 2)), ('Oh', (4, 3, 2))]:
    for s in GRID3:
        for u in GRID3: CASES.append((g, ax, (q(1), s, u)))
if len(sys.argv) > 3 and sys.argv[3] == 'fine':   # second pass: fine sweeps where the first pass found chains that do not close
    CASES = [('Oh', (4, 2), (q(1), q(Fr(a, 80)))) for a in range(44, 81)] + [('Ih', (5, 2), (q(1), q(Fr(a, 80)))) for a in range(76, 117)]
res = []
for g, ax, ss in CASES:
    fams = [(AX[g][a], s) for a, s in zip(ax, ss)]; want = sum(len(AX[g][a]) for a in ax)
    row = dict(group=g, axes=list(ax), s=[fmt(s) for s in ss])
    try:
        V, F = solid(fams)
        row.update(corners=len(V), faces=kinds(F), all_planes_faces=len(F) == want)
        if len(F) != want: row['skip'] = 'a family is not all faces'; res.append(row); continue
        row['T'] = tchain(V, F); row['cores'] = cchain(V, F)
    except Exception as e:
        row['error'] = type(e).__name__ + ' ' + str(e)[:150]
    res.append(row); print({k: v for k, v in row.items()}, flush=True)
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('done', len(res), flush=True)
