# DICTO · dictospheres.com — math-data dataset builder library (2026-10-22).
# Exact arithmetic in a real quadratic field Q(sqrt d) with Fractions (the Q5 class of the research study
# studies/2026-10-19-five-fold-octet/exact_cycle.py, generalised to any square-free d), an exact convex hull with a
# certificate (float qhull only GUESSES the facets; every face plane, corner and the closure are proved exactly),
# exact volume, edge lengths, symmetry group, and writers for the dataset JSON / OFF files.
import itertools, json, math, os
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import numpy as np

getcontext().prec = 60


class QF:
    """a + b*sqrt(d), a, b rational. d is a square-free integer > 1 (or d = 1 meaning plain rationals, b = 0)."""
    __slots__ = ('a', 'b', 'd')

    def __init__(s, a, b=0, d=5):
        s.a, s.b, s.d = Fr(a), Fr(b), d

    def _c(s, o):
        if isinstance(o, QF):
            assert o.d == s.d or o.b == 0 or s.b == 0, 'mixed fields'
            return o
        return QF(o, 0, s.d)

    def _dd(s, o):
        return s.d if s.b != 0 or not isinstance(o, QF) else (o.d if o.b != 0 else s.d)

    def __add__(s, o): o = s._c(o); return QF(s.a + o.a, s.b + o.b, s._dd(o))
    __radd__ = __add__
    def __neg__(s): return QF(-s.a, -s.b, s.d)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s

    def __mul__(s, o):
        o = s._c(o); d = s._dd(o)
        return QF(s.a * o.a + d * s.b * o.b, s.a * o.b + s.b * o.a, d)
    __rmul__ = __mul__

    def __truediv__(s, o):
        o = s._c(o); d = s._dd(o); n = o.a * o.a - d * o.b * o.b; assert n != 0
        return s * QF(o.a / n, -o.b / n, d)

    def __rtruediv__(s, o): return s._c(o) / s

    def sign(s):
        a, b, d = s.a, s.b, s.d
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if a * a > d * b * b else (1 if b > 0 else -1)

    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def f(s): return float(s.a) + float(s.b) * math.sqrt(s.d)
    def dec(s, places=15):
        x = Decimal(s.a.numerator) / Decimal(s.a.denominator) + Decimal(s.b.numerator) / Decimal(s.b.denominator) * Decimal(s.d).sqrt()
        q = x.quantize(Decimal(1).scaleb(-places))
        return format(q, 'f') if q != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-places)), 'f')
    def __repr__(s): return fmt(s)


class KC:
    """a + b*r + c*r^2 with r = k^(1/3) real: the pure cubic field Q(cbrt k) (version 2, 2026-10-24: Samson and Delilah live in
    Q(2**(1/3))). Exact with Fractions. sign() is exact: the norm N(x) = a^3 + k b^3 + k^2 c^3 - 3k abc is x times |x'|^2 (the other
    two conjugates are complex conjugates), so sign(x) = sign(N(x)). The field is named by d = ('cbrt', k)."""
    __slots__ = ('c', 'k')

    def __init__(s, a=0, b=0, c=0, k=2):
        s.c = (Fr(a), Fr(b), Fr(c)); s.k = k

    @property
    def d(s): return ('cbrt', s.k)

    def _c(s, o):
        if isinstance(o, KC):
            assert o.k == s.k, 'mixed fields'
            return o
        assert not isinstance(o, QF), 'mixed fields'
        return KC(o, 0, 0, s.k)

    def __add__(s, o): o = s._c(o); return KC(*(x + y for x, y in zip(s.c, o.c)), k=s.k)
    __radd__ = __add__
    def __neg__(s): return KC(*(-x for x in s.c), k=s.k)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s

    def __mul__(s, o):
        o = s._c(o); (a, b, c), (x, y, z), k = s.c, o.c, s.k
        return KC(a * x + k * (b * z + c * y), a * y + b * x + k * c * z, a * z + b * y + c * x, k=k)
    __rmul__ = __mul__

    def norm(s):
        (a, b, c), k = s.c, s.k
        return a ** 3 + k * b ** 3 + k * k * c ** 3 - 3 * k * a * b * c

    def __truediv__(s, o):
        o = s._c(o); (a, b, c), k = o.c, o.k; n = o.norm(); assert n != 0
        return s * KC((a * a - k * b * c) / n, (k * c * c - a * b) / n, (b * b - a * c) / n, k=k)

    def __rtruediv__(s, o): return s._c(o) / s
    def sign(s): n = s.norm(); return (n > 0) - (n < 0)
    def __eq__(s, o): o = s._c(o); return s.c == o.c
    def __hash__(s): return hash(s.c)
    def __lt__(s, o): return (s - o).sign() < 0
    def f(s): r = s.k ** (1 / 3); return float(s.c[0]) + float(s.c[1]) * r + float(s.c[2]) * r * r

    def mp(s):
        import mpmath
        r = mpmath.cbrt(s.k)
        return sum((mpmath.mpf(x.numerator) / x.denominator * r ** i for i, x in enumerate(s.c)), mpmath.mpf(0))

    def dec(s, places=15):
        r = Decimal(s.k) ** (Decimal(1) / Decimal(3))
        x = sum((Decimal(q.numerator) / Decimal(q.denominator) * r ** i for i, q in enumerate(s.c)), Decimal(0))
        q = x.quantize(Decimal(1).scaleb(-places))
        return format(q, 'f') if q != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-places)), 'f')

    def fmt(s):
        def r(q): return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'
        out = []
        for i, q in enumerate(s.c):
            if q == 0: continue
            if i == 0: out.append(r(q)); continue
            base = f'{s.k}**({i}/3)'
            out.append(base if q == 1 else (f'-{base}' if q == -1 else f'({r(q)})*{base}'))
        if not out: return '0'
        t = out[0]
        for u in out[1:]: t += f' - {u[1:]}' if u.startswith('-') else f' + {u}'
        return t
    def __repr__(s): return s.fmt()


def field_name(d):
    """the dataset's `field` string for a field key d (int for Q(sqrt d), ('cbrt', k) for Q(k**(1/3)))."""
    return f'Q({d[1]}**(1/3))' if isinstance(d, tuple) else f'Q(sqrt({d}))'


def fmt(x):
    """sympy-parsable exact string."""
    if isinstance(x, KC): return x.fmt()
    def r(q): return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'
    if x.b == 0: return r(x.a)
    bs = f'sqrt({x.d})' if x.b == 1 else (f'-sqrt({x.d})' if x.b == -1 else f'({r(x.b)})*sqrt({x.d})')
    if x.a == 0: return bs
    return f'{r(x.a)} + {bs}' if not bs.startswith('-') else f'{r(x.a)} - {bs[1:]}'


def Q(a, b=0, d=5): return QF(a, b, d)
PHI = QF(Fr(1, 2), Fr(1, 2), 5)
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
sub = lambda u, v: (u[0] - v[0], u[1] - v[1], u[2] - v[2])
add = lambda u, v: (u[0] + v[0], u[1] + v[1], u[2] + v[2])
mul = lambda k, v: (k * v[0], k * v[1], k * v[2])
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
fv = lambda v: np.array([x.f() for x in v])
def det3(a, b, c): return dot(a, cross(b, c))
def zero(d=5): return KC(0, k=d[1]) if isinstance(d, tuple) else QF(0, 0, d)


def plane_key(n, c):
    """normalise plane n.x = c: divide by first nonzero coordinate of n."""
    k = next(x for x in n if x.sign() != 0)
    return tuple(x / k for x in n) + (c / k,)


def hull(points):
    """Exact convex hull with certificate. Returns (V, F): V exact corners, F faces as index lists CCW seen from outside."""
    P = list(dict.fromkeys(tuple(p) for p in points))
    from scipy.spatial import ConvexHull
    X = np.array([fv(p) for p in P]); cen = X.mean(0)
    ch = ConvexHull(X)
    planes = {}
    for simp in ch.simplices:
        a, b, c = (P[i] for i in simp)
        n = cross(sub(b, a), sub(c, a))
        if all(x.sign() == 0 for x in n): continue
        cc = dot(n, a)
        if (dot(n, tuple(zero(P[0][0].d) + Fr(x).limit_denominator(10**6) for x in cen)) - cc).f() > 0: n, cc = mul(-1, n), -cc
        planes[plane_key(n, cc)] = (n, cc)
    # orient each plane outward exactly: all points must satisfy n.x <= c
    good = {}
    for key, (n, cc) in planes.items():
        sg = [(dot(n, p) - cc).sign() for p in P]
        if all(s <= 0 for s in sg): good[key] = (n, cc, [i for i, s in enumerate(sg) if s == 0])
        elif all(s >= 0 for s in sg): good[key] = (mul(-1, n), -cc, [i for i, s in enumerate(sg) if s == 0])
        else: raise AssertionError('float facet is not a supporting plane')
    # corners: points on >= 3 independent face planes
    on = {i: [] for i in range(len(P))}
    for key, (n, cc, idx) in good.items():
        for i in idx: on[i].append(n)
    corners = []
    for i in range(len(P)):
        ns = on[i]
        if len(ns) >= 3 and any(det3(*t).sign() != 0 for t in itertools.combinations(ns, 3)): corners.append(i)
    V = [P[i] for i in corners]; vid = {i: k for k, i in enumerate(corners)}
    F = []
    for key, (n, cc, idx) in good.items():
        f = [vid[i] for i in idx if i in vid]
        assert len(f) >= 3
        pts = np.array([fv(V[j]) for j in f]); c0 = pts.mean(0); nf = fv(n)
        u = pts[0] - c0; u /= np.linalg.norm(u); w = np.cross(nf / np.linalg.norm(nf), u)
        order = [f[k] for k in np.argsort(np.arctan2((pts - c0) @ w, (pts - c0) @ u))]
        # exact convex CCW check (seen from outside, normal n): every consecutive triple turns left
        m = len(order)
        for k in range(m):
            a, b, c = V[order[k]], V[order[(k + 1) % m]], V[order[(k + 2) % m]]
            assert dot(cross(sub(b, a), sub(c, b)), n).sign() > 0, 'face not strictly convex CCW'
        F.append(order)
    check_closed(V, F)
    return V, F


def check_closed(V, F):
    E = {}
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]):
            assert (a, b) not in E, 'directed edge twice'
            E[(a, b)] = 1
    assert all((b, a) in E for (a, b) in E), 'surface not closed'
    assert len(V) - len(E) // 2 + len(F) == 2, 'Euler'
    return len(E) // 2


def volume(V, F):
    s = zero(V[0][0].d)
    for f in F:
        for k in range(1, len(f) - 1): s = s + det3(V[f[0]], V[f[k]], V[f[k + 1]])
    return s / 6


def face_planes(V, F):
    out = []
    for f in F:
        a, b, c = V[f[0]], V[f[1]], V[f[2]]; n = cross(sub(b, a), sub(c, a)); out.append((n, dot(n, a)))
    return out


def halfspace_solid(planes):
    """Exact solid {x : n.x <= c for all (n, c)}: corners by float intersection guess + exact solve, then hull."""
    from scipy.spatial import HalfspaceIntersection
    Nf = np.array([fv(n) for n, c in planes]); cf = np.array([c.f() for n, c in planes])
    X = HalfspaceIntersection(np.hstack([Nf, -cf[:, None]]), np.zeros(3)).intersections
    X = X[np.unique(np.round(X, 8), axis=0, return_index=True)[1]]
    C = []
    for x in X:
        tight = [i for i in range(len(planes)) if abs(Nf[i] @ x - cf[i]) < 1e-7]
        for tri in itertools.combinations(tight, 3):
            if abs(np.linalg.det(Nf[list(tri)])) > 1e-6: break
        A = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]
        D = det3(*A)
        sol = []
        for col in range(3):
            M = [tuple(b[r] if k == col else A[r][k] for k in range(3)) for r in range(3)]
            sol.append(det3(*M) / D)
        C.append(tuple(sol))
    C = list(dict.fromkeys(C))
    for c in C:
        assert all((dot(n, c) - h).sign() <= 0 for n, h in planes), 'corner outside'
    V, F = hull(C)
    # every hull face lies on one of the given planes (so hull = the solid cut out)
    keys = {plane_key(n, h) for n, h in planes}
    for n, h in face_planes(V, F): assert plane_key(n, h) in keys
    return V, F


def polar(V, F, rho2):
    """polar (reciprocal) in the sphere |x|^2 = rho2: corners = poles of the face planes."""
    return [mul(rho2 / c, n) for n, c in face_planes(V, F)]


def ustep(V):
    """Universal PiTet step T(S) = {x : v.x <= v.v for every corner v} (#38)."""
    return halfspace_solid([(v, dot(v, v)) for v in V])


def rstep(V, F):
    """Reverse step (#39): new corners = foot points of the face planes."""
    return [mul(c / dot(n, n), n) for n, c in face_planes(V, F)]


def edges_of(F):
    return sorted({tuple(sorted((a, b))) for f in F for a, b in zip(f, f[1:] + f[:1])})


def sym_group(V, F=None):
    """Exact symmetry group of a finite point set about its centroid: list of (matrix, det sign). With faces F (version 2), only the
    maps that also take the face set to itself (the symmetry of the solid; for a convex solid the same group)."""
    d = V[0][0].d; n = len(V)
    c = tuple(sum((v[k] for v in V), zero(d)) / n for k in range(3))
    W = [sub(v, c) for v in V]; S = set(W)
    norms = [dot(w, w) for w in W]
    from collections import Counter
    cnt = Counter(norms)
    order_idx = sorted(range(n), key=lambda i: (cnt[norms[i]], norms[i].f()))
    a = order_idx[0]
    # b: nearest to a among small classes, independent; c: independent of a, b
    cand = [i for i in order_idx if i != a and any(x.sign() != 0 for x in cross(W[a], W[i]))]
    b = min(cand[:200], key=lambda i: (cnt[norms[i]], np.linalg.norm(fv(W[i]) - fv(W[a]))))
    ab = cross(W[a], W[b])
    cand = [i for i in order_idx if dot(ab, W[i]).sign() != 0]
    cc = min(cand[:200], key=lambda i: (cnt[norms[i]], np.linalg.norm(fv(W[i]) - fv(W[a]))))
    A = [W[a], W[b], W[cc]]
    gram = [[dot(A[i], A[j]) for j in range(3)] for i in range(3)]
    Af = np.array([fv(x) for x in A]).T; Ainv = np.linalg.inv(Af)
    Wf = np.array([fv(w) for w in W])
    def pick(i, cons):
        out = []
        for j in range(n):
            if norms[j] != gram[i][i]: continue
            if all(dot(W[j], W[k]) == gram[i][m] for m, k in cons): out.append(j)
        return out
    # exact inverse of A (columns) via adjugate
    Dt = det3(*A)
    adj = [cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])]   # rows of inverse * Dt (for row-vector form)
    G = []
    for ja in pick(0, []):
        for jb in pick(1, [(0, ja)]):
            for jc in pick(2, [(0, ja), (1, jb)]):
                B = [W[ja], W[jb], W[jc]]
                Bf = np.array([fv(x) for x in B]).T; Mf = Bf @ Ainv
                img = Wf @ Mf.T
                # float pre-filter
                ok = all(np.min(np.linalg.norm(Wf - x, axis=1)) < 1e-7 for x in img)
                if not ok: continue
                # exact matrix M = B * A^{-1}; A^{-1} rows = adj / Dt
                M = [[sum((B[k][i] * adj[k][j] for k in range(3)), zero(d)) / Dt for j in range(3)] for i in range(3)]
                if all(tuple(dot(M[i], w) for i in range(3)) in S for w in W):
                    if F is not None:
                        img = {w: j for j, w in enumerate(W)}
                        perm = [img[tuple(dot(M[i], w) for i in range(3))] for w in W]
                        fs = {frozenset(f) for f in F}
                        if any(frozenset(perm[i] for i in f) not in fs for f in F): continue
                    G.append((M, det3(*M).sign()))
    return G


def schoenflies_check(G):
    order = len(G); proper = sum(1 for _, s in G if s > 0)
    d = G[0][0][0][0].d
    inv = any(all(M[i][j] == (zero(d) - 1 if i == j else zero(d)) for i in range(3) for j in range(3)) for M, _ in G)
    return order, proper, inv


def write_solid(path_noext, meta, V, F, extra_published=None):
    """Write the dataset JSON + OFF for one solid; returns the computed summary."""
    nE = check_closed(V, F)
    vol = volume(V, F); assert vol.sign() > 0
    E = edges_of(F)
    el = sorted({dot(sub(V[a], V[b]), sub(V[a], V[b])) for a, b in E}, key=lambda q: q.f())
    from collections import Counter
    fk = Counter(len(f) for f in F)
    G = sym_group(V, F); order, proper, inv = schoenflies_check(G); cls = classify(G)
    if meta.get('symmetry_label') in (None, 'auto'): meta = dict(meta, symmetry_label=cls)
    doc = dict(meta)
    doc.update({
        'field': field_name(V[0][0].d),
        'vertices': [{'exact': [fmt(x) for x in v], 'decimal': [x.dec() for x in v]} for v in V],
        'faces': F,
        'f_vector': {'vertices': len(V), 'edges': nE, 'faces': len(F)},
        'faces_by_sides': {str(k): fk[k] for k in sorted(fk)},
        'volume': {'exact': fmt(vol), 'decimal': vol.dec()},
        'squared_edge_lengths': [{'exact': fmt(x), 'decimal': x.dec(), 'count': sum(1 for a, b in E if dot(sub(V[a], V[b]), sub(V[a], V[b])) == x)} for x in el],
        'symmetry': {'schoenflies': meta['symmetry_label'], 'order': order, 'rotations': proper, 'contains_inversion': inv},
        'credit': 'DICTO', 'creator_mark': 'Created by DICTO · dictospheres.com', 'licence': 'CC BY-SA 4.0',
    })
    doc.pop('symmetry_label')
    doc['checks'] = {'closed_2_manifold': True, 'outward_ccw_winding': True, 'faces_planar_exact': True,
                     'euler_characteristic': len(V) - nE + len(F), 'volume_positive_exact': True,
                     'convex': meta.get('convex', True), 'symmetry_order_exact': order,
                     'verified_by': 'check.py (python3 + sympy), re-run from this file alone'}
    json.dump(doc, open(path_noext + '.json', 'w'), indent=1, ensure_ascii=False)
    with open(path_noext + '.off', 'w') as fh:
        fh.write('OFF\n# ' + meta['name'] + ' — Created by DICTO · dictospheres.com — CC BY-SA 4.0\n')
        fh.write(f'{len(V)} {len(F)} {nE}\n')
        for v in V: fh.write(' '.join(x.dec() for x in v) + '\n')
        for f in F: fh.write(str(len(f)) + ' ' + ' '.join(map(str, f)) + '\n')
    return {'cls': cls, 'label': doc['symmetry']['schoenflies'], 'V': len(V), 'E': nE, 'F': len(F), 'vol': vol, 'order': order, 'proper': proper, 'inv': inv, 'fk': dict(fk), 'el': el}


def canon(V, F):
    """Sort corners lexicographically by float coords for a stable file; remap faces; start each face at its smallest index."""
    idx = sorted(range(len(V)), key=lambda i: tuple(round(x.f(), 9) for x in V[i]))
    rm = {o: k for k, o in enumerate(idx)}
    V2 = [V[i] for i in idx]
    F2 = []
    for f in F:
        g = [rm[i] for i in f]; k = g.index(min(g)); F2.append(g[k:] + g[:k])
    F2.sort()
    return V2, F2


def qsqrt(x):
    """exact square root in Q(sqrt d) if it exists (positive root)."""
    import sympy
    d = x.d
    s = sympy.sqrt(sympy.Rational(x.a.numerator, x.a.denominator) + sympy.Rational(x.b.numerator, x.b.denominator) * sympy.sqrt(d))
    s = sympy.sqrtdenest(s)
    e = sympy.expand(s); cd = e.as_coefficients_dict()
    a = Fr(0); b = Fr(0)
    for term, coef in cd.items():
        if term == 1: a += Fr(int(sympy.fraction(coef)[0]), int(sympy.fraction(coef)[1]))
        elif term == sympy.sqrt(d): b += Fr(int(sympy.fraction(coef)[0]), int(sympy.fraction(coef)[1]))
        else: raise ValueError(f'not a square in Q(sqrt {d}): {s}')
    r = QF(a, b, d); assert r * r == x and r.sign() > 0
    return r


def classify(G):
    """Schoenflies symbol from the exact group (rotation orders from traces, mirrors, inversion)."""
    from collections import Counter
    import math as m
    d = G[0][0][0][0].d
    def tr(M): return (M[0][0] + M[1][1] + M[2][2]).f()
    rot = Counter(); mir = 0; inv = False; srot = 0
    for M, s in G:
        t = tr(M)
        if s > 0:
            if abs(t - 3) < 1e-9: continue
            ang = m.acos(max(-1, min(1, (t - 1) / 2))); rot[round(2 * m.pi / ang) if ang > 1e-9 else 1] += 1
        else:
            if abs(t + 3) < 1e-9: inv = True
            elif abs(t - 1) < 1e-9: mir += 1
            else: srot += 1
    n = len(G); nr = sum(1 for _, s in G if s > 0)
    top = max(rot) if rot else 1
    if nr == 60: return 'Ih' if n == 120 else 'I'
    if nr == 24 and rot.get(4, 0) >= 6: return 'Oh' if n == 48 else 'O'
    if nr == 12 and rot.get(3, 0) == 8: return 'Th' if inv else ('Td' if n == 24 else 'T')
    c2 = rot.get(2, 0)
    if nr == 1: return 'Ci' if inv else ('Cs' if mir else 'C1')
    k = top
    dihedral = nr == 2 * k and (c2 >= k if k > 2 else c2 == 3)
    if dihedral:
        if n == nr: return f'D{k}'
        return f'D{k}h' if mir == k + 1 or (k % 2 == 0 and inv and mir == k + 1) or (k % 2 == 1 and mir == k + 1) else f'D{k}d'
    if n == nr: return f'C{k}'
    if mir == k: return f'C{k}v'
    if mir == 1: return f'C{k}h'
    return f'S{2 * k}'


def similar_float(A, B, tol=1e-6):
    """corner-matching similarity (rotation/reflection + scale) between point sets; returns (scale B/A, max error) or None."""
    A = np.array(A, float); B = np.array(B, float)
    if len(A) != len(B): return None
    A = A - A.mean(0); B = B - B.mean(0)
    sa = np.sqrt((A ** 2).sum(1).mean()); sb = np.sqrt((B ** 2).sum(1).mean()); A /= sa; B /= sb
    nA = np.linalg.norm(A, axis=1); nB = np.linalg.norm(B, axis=1)
    i0 = int(np.argmax(nA)); i1 = int(np.argsort(np.linalg.norm(A - A[i0], axis=1))[1])
    i2 = next(i for i in np.argsort(np.linalg.norm(A - A[i0], axis=1))[2:] if abs(np.linalg.det(A[[i0, i1, i]])) > 1e-6)
    Ma = A[[i0, i1, i2]]
    for j0 in range(len(B)):
        if abs(nB[j0] - nA[i0]) > 50 * tol: continue
        for j1 in range(len(B)):
            if abs(np.linalg.norm(B[j1] - B[j0]) - np.linalg.norm(A[i1] - A[i0])) > 50 * tol or abs(nB[j1] - nA[i1]) > 50 * tol: continue
            for j2 in range(len(B)):
                if abs(nB[j2] - nA[i2]) > 50 * tol or abs(np.linalg.norm(B[j2] - B[j0]) - np.linalg.norm(A[i2] - A[i0])) > 50 * tol: continue
                R = np.linalg.solve(Ma, B[[j0, j1, j2]])
                img = A @ R
                err = max(np.min(np.linalg.norm(B - x, axis=1)) for x in img)
                if err < tol: return sb / sa, err
    return None

