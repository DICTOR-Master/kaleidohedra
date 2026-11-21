"""Thin PyNormaliz wrapper over Q(phi): hull of points, polytope from inequalities (+ equations); results parsed to QP."""
import PyNormaliz as PN
from qphi import NF, parse, QP, dot


def _row(v): return [x.nz() if isinstance(x, QP) else str(x) for x in v]


def hull(points):
    C = PN.Cone(number_field=NF, vertices=[_row(list(p) + [QP(1)]) for p in points])
    return C


def poly(ineqs, eqs=()):
    """ineqs/eqs rows (c_1..c_d, c0) meaning c.x + c0 >= 0 / = 0"""
    kw = dict(number_field=NF, inhom_inequalities=[_row(r) for r in ineqs])
    if eqs: kw["inhom_equations"] = [_row(r) for r in eqs]
    return PN.Cone(**kw)


def verts(C):
    out = []
    for r in C.VerticesOfPolyhedron():
        r = [parse(x) for x in r]
        h = r[-1]
        out.append(tuple(x / h for x in r[:-1]))
    return list(dict.fromkeys(out))      # a lower-dimensional result can repeat a vertex (seen on polygon tips)


def facets(C):
    """support hyperplanes as (normal, c0): normal.x + c0 >= 0"""
    out = []
    for r in C.SupportHyperplanes():
        r = [parse(x) for x in r]
        out.append((tuple(r[:-1]), r[-1]))
    return out


def equations(C):
    return [[parse(x) for x in r] for r in C.Equations()]


def incid(F, V):
    return [[i for i, v in enumerate(V) if (dot(n, v) + c).sign() == 0] for n, c in F]
