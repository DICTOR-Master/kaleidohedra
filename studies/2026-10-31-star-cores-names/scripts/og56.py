# Star Cores names (2026-10-31): OG chain steps 5 and 6 dumped for pictures; copied from study 4 (DICTO 2026-10-30 "study 4"): the long chains of DICTO's growth rule T (#38), exactly in Q(sqrt5). The float
# survey (survey2) followed TQHD -> TQP -> TQH -> TPH -> OG and OG -> KRE -> PHE -> TPP -> DPHP, then lost the thread in float noise (its
# later steps broke the icosahedral symmetry). Here the chain from OG is followed exactly: each step's corners, faces by sides, kinds of
# corner radius and edge length, whether it is a dataset solid (exact similarity), and whether it returns to an earlier step.
# Usage: ~/geom/bin/python study4.py <dataset solids dir> <exactlib dir> <out json> [max corners]
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
MAXC = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
def load_exact(path):
    m = json.load(open(path)); d = fkey(m['field'])
    V = [tuple(parse(x, d) for x in v['exact']) for v in m['vertices']]; return m['name'], hull(V)
lib = []
for p in sorted(glob.glob(os.path.join(SOL, '*.json'))):
    m = json.load(open(p))
    if m.get('field') != 'Q(sqrt(5))' or str(m.get('convex')) != 'True': continue
    try: n, (V, F) = load_exact(p); lib.append((n, V, F, rad2(V)))
    except Exception: pass
print('library', len(lib), flush=True)
def kinds_r(V): return len({fmt(dot(v, v)) for v in V})
def kinds_e(V, F): return len({fmt(dot(sub(V[a], V[b]), sub(V[a], V[b]))) for a, b in edges_of(F)})
name, (S, SF) = load_exact(os.path.join(SOL, 'dicto-ogdoecontahedron.json'))
hist = [(S, SF, rad2(S))]; out = dict(start=name, steps=[])
DUMP = {}
for k in range(1, 7):
    t0 = time.time(); S, SF = ustep(S); r2 = rad2(S)
    st = dict(step=k, corners=len(S), faces=kinds(SF), radius_kinds=kinds_r(S), edge_kinds=kinds_e(S, SF), seconds=round(time.time() - t0))
    for n, A, AF, ra in lib:
        if len(A) == len(S) and kinds(AF) == kinds(SF) and similar(A, S, r2 / ra): st['is'] = n; break
    for j, (A, AF, ra) in enumerate(hist):
        if kinds(AF) == kinds(SF) and similar(A, S, r2 / ra): st['returns_to_step'] = j; break
    if k >= 5: DUMP[k] = dict(V=[[x.f() for x in v] for v in S], F=SF, faces=kinds(SF))
    out['steps'].append(st); print(st, flush=True); hist.append((S, SF, r2))
    json.dump(out, open(OUT, 'w'), indent=1, default=str)
    if 'returns_to_step' in st or len(S) > MAXC: break
json.dump(DUMP, open(OUT.replace('.json', '-shapes.json'), 'w'))
print('done', flush=True)
