"""Exact (sympy) Archimedean coordinates and their polar duals, the Catalan solids; companions of gcb.py."""
import itertools
import numpy as np
import sympy as sp
import gcb

phi = (1 + sp.sqrt(5)) / 2
R2, P_ = sp.sqrt(2), phi
SEEDS = {  # exact Archimedean seeds, as in gcb.archimedean (any scale)
    'truncated tetrahedron': ([(3, 1, 1)], 'all', 'even-minus'),
    'cuboctahedron': ([(1, 1, 0)], 'all', None),
    'truncated cube': ([(R2 - 1, 1, 1)], 'all', None),
    'truncated octahedron': ([(0, 1, 2)], 'all', None),
    'rhombicuboctahedron': ([(1, 1, 1 + R2)], 'all', None),
    'truncated cuboctahedron': ([(1, 1 + R2, 1 + 2 * R2)], 'all', None),
    'icosidodecahedron': ([(0, 0, P_), (sp.Rational(1, 2), P_ / 2, P_ ** 2 / 2)], 'even', None),
    'truncated dodecahedron': ([(0, 1 / P_, 2 + P_), (1 / P_, P_, 2 * P_), (P_, 2, P_ + 1)], 'even', None),
    'truncated icosahedron': ([(0, 1, 3 * P_), (1, 2 + P_, 2 * P_), (P_, 2, P_ ** 3)], 'even', None),
    'rhombicosidodecahedron': ([(1, 1, P_ ** 3), (P_ ** 2, P_, 2 * P_), (2 + P_, 0, P_ ** 2)], 'even', None),
    'truncated icosidodecahedron': ([(1 / P_, 1 / P_, 3 + P_), (2 / P_, P_, 1 + 2 * P_), (1 / P_, P_ ** 2, -1 + 3 * P_),
                                     (2 * P_ - 1, 2, 2 + P_), (P_, 3, 2 * P_)], 'even', None)}
CATALAN_NAME = {'truncated tetrahedron': 'triakis tetrahedron', 'cuboctahedron': 'rhombic dodecahedron',
                'truncated cube': 'triakis octahedron', 'truncated octahedron': 'tetrakis hexahedron',
                'rhombicuboctahedron': 'deltoidal icositetrahedron', 'truncated cuboctahedron': 'disdyakis dodecahedron',
                'snub cube': 'pentagonal icositetrahedron', 'icosidodecahedron': 'rhombic triacontahedron',
                'truncated dodecahedron': 'triakis icosahedron', 'truncated icosahedron': 'pentakis dodecahedron',
                'rhombicosidodecahedron': 'deltoidal hexecontahedron', 'truncated icosidodecahedron': 'disdyakis triacontahedron',
                'snub dodecahedron': 'pentagonal hexecontahedron'}


def exact_arch(name):
    seeds, kind, filt = SEEDS[name]
    P = {}
    for s in seeds:
        s = tuple(sp.sympify(t) for t in s)
        perms = set(itertools.permutations(s)) if kind == 'all' else {s, (s[1], s[2], s[0]), (s[2], s[0], s[1])}
        for p in perms:
            for sg in itertools.product([1, -1], repeat=3):
                q = tuple(sp.radsimp(sg[i] * p[i]) for i in range(3))
                if filt == 'even-minus' and sum(1 for i in range(3) if sp.N(q[i]) < 0) % 2: continue
                P[tuple(round(float(t), 9) for t in q)] = q
    return P




def exact_dual(name):
    """Exact Catalan corners (polar of the exact Archimedean solid in the unit sphere), float faces, orbit labels."""
    EA = exact_arch(name); exA = list(EA.values())
    A0 = np.array([[float(t) for t in q] for q in exA]); FA = gcb.faces(A0)
    D = []
    for f in FA:
        p0, p1, p2 = [sp.Matrix(exA[i]) for i in f[:3]]
        n = (p1 - p0).cross(p2 - p0); dd = n.dot(p0)
        if sp.N(dd) < 0: n, dd = -n, -dd
        D.append(sp.Matrix([sp.radsimp(t / dd) for t in n]))
    Df = np.array([[float(t) for t in v] for v in D]); FD = gcb.faces(Df)
    orb = []
    for f in FA:
        nb = sorted(len(h) for h in FA if len(set(h) & set(f)) == 2); orb.append(str(len(f)) + '|' + ''.join(map(str, nb)))
    return D, Df, FD, orb
