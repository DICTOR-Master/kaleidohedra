# Item 2 (#54 One Turn Is a Gnomon, open points of §7):
#  (a) "whether another choice of stations makes a shorter run of steps a classical gnomon";
#  (b) "whether pyramid-capped cubes with heights adding to 1 can fill space together at other sizes or with the Tricaps as
#      separate pieces".
#
# (a) A run from station X to a later station Y is a classical gnomon of X exactly when Y is similar to X (#54 Theorem A).
#     With free stations the question is empty (X and 1.01 X are always nested). So we ask it for the cycle's own solids:
#     can a scaled copy sX (1 < s < phi^3) of one of the twelve stations be inserted into the chain, nested between two
#     consecutive stations? Then X -> ... -> sX is a run shorter than a turn and a classical gnomon of X.
#     Exact: stations from studies/2026-10-25-gnomon-shapes/stations-exact.json (coordinates a + b sqrt5, exact),
#     facets found by a float hull and then proved exactly (every corner on the inner side), support values exact.
#     Window of s for X in the gap (S_j, S_j+1):  max_f h_Sj(u_f)/c_f  <=  s  <=  min_g c_g / h_X(u_g).
# (b) Dihedral-angle obstruction (valid for tilings at any sizes, face-to-face or not): round a generic point of an edge of
#     a tile the dihedral angles of the tiles that have the point on an edge, plus pi for each tile that has it inside a face,
#     add to 2 pi. Capped cube P(h): cube of half edge 1 with a square pyramid of height h on each face, 0 < h < 1;
#     cube-edge angle A(h) = pi/2 + 2 atan h, apex-edge angle B(h) = pi - arccos(1/(1 + h^2)); both in (pi/2, pi).
#     Every combination is then exactly three angles (two are < 2 pi, four are > 2 pi, pi + anything > pi needs a second
#     angle < pi/2). sin(x + y + z) = 0 with x + y + z in (3pi/2, 3pi) means x + y + z = 2pi; the square roots are eliminated
#     by resultants, the real roots in (0, 1) isolated exactly (sympy), and each root tested at 60 digits.
import json, os, sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, "..", "..")
checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


# ---------------- exact Q(sqrt5)
class Q5:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)

    def __rsub__(s, o): return Q5(o) - s

    def __neg__(s): return Q5(-s.a, -s.b)

    def __mul__(s, o):
        o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b; assert n != 0; return Q5(s.a / n, -s.b / n)

    def __truediv__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s * o.inv()

    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # a, b opposite signs: compare a^2 with 5 b^2
        if a > 0: return 1 if a * a > 5 * b * b else -1
        return 1 if 5 * b * b > a * a else -1

    def __lt__(s, o): return (s - o).sign() < 0

    def __le__(s, o): return (s - o).sign() <= 0

    def __gt__(s, o): return (s - o).sign() > 0

    def __ge__(s, o): return (s - o).sign() >= 0

    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b

    def __hash__(s): return hash((s.a, s.b))

    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5

    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f"{s.a} + {s.b}√5" if s.b > 0 else f"{s.a} − {-s.b}√5"


PHI = Q5(Fr(1, 2), Fr(1, 2)); PHI3 = PHI * PHI * PHI


def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def sub(u, v): return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def scale(s, P): return [tuple(s * x for x in p) for p in P]


def facets(P):
    """Exact facets (u, c) with u.x <= c for all corners, c > 0; float hull proposes, exact test decides."""
    X = np.array([[float(x) for x in p] for p in P])
    hull = ConvexHull(X)
    out = {}
    for simp in hull.simplices:
        a, b, c = (P[i] for i in simp)
        n = cross(sub(b, a), sub(c, a)); cc = dot(n, a)
        if cc < 0: n = tuple(-x for x in n); cc = -cc
        assert cc > 0
        assert all(dot(n, p) <= cc for p in P), "not a facet"
        # normalise so that c = 1 (exact) to deduplicate coplanar triangles
        u = tuple(x / cc for x in n)
        out[u] = Q5(1)
    return list(out.items()), hull


def h(P, u): return max((dot(u, p) for p in P), key=lambda q: float(q)) if False else maxq([dot(u, p) for p in P])


def maxq(L):
    m = L[0]
    for x in L[1:]:
        if x > m: m = x
    return m


def minq(L):
    m = L[0]
    for x in L[1:]:
        if x < m: m = x
    return m


def solve3(rows, rhs):
    """Exact 3x3 solve over Q(sqrt5) by Cramer."""
    def det(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det(rows)
    if D == Q5(0): return None
    out = []
    for k in range(3):
        M = [list(r) for r in rows]
        for r in range(3): M[r][k] = rhs[r]
        out.append(det(M) / D)
    return tuple(out)


def star_hi(QP, QF, IP, tips, sc):
    """Largest s with s*Q inside the Cleo star scaled by sc. Per face F of I (with tip t_F): the star inside the cone over F
    is the bipyramid conv(0, F, t_F); its outer facets are the planes through t_F and an edge of F. Exact vertex enumeration
    of Q ∩ cone_F (float prefilter, exact solve and exact feasibility)."""
    IP = scale(sc, IP); tips = scale(sc, tips)
    Ff, _ = facets(IP)
    best = None
    for u, c in Ff[:1]:  # one face suffices: every station is invariant under the 120 symmetries of I (checked in part_a)
        Fv = [p for p in IP if dot(u, p) == c]
        assert len(Fv) == 3
        cenF = tuple(sum((p[i] for p in Fv), Q5(0)) / 3 for i in range(3))
        tip = [t for t in tips if all((t[i] * 2 - 4 * cenF[i]) == Q5(0) for i in range(3)) or
               all((t[i] - 2 * cenF[i]) == Q5(0) for i in range(3))]
        assert len(tip) == 1, "tip = 2 x face centre"
        tip = tip[0]
        cone = []   # n.x >= 0
        outer = []  # n.x <= c
        for a, b in itertools.combinations(Fv, 2):
            r = [p for p in Fv if p != a and p != b][0]
            n = cross(a, b)
            if dot(n, r) < Q5(0): n = tuple(-x for x in n)
            cone.append(n)
            m = cross(sub(a, tip), sub(b, tip)); cc = dot(m, tip)
            if dot(m, r) > cc: m = tuple(-x for x in m); cc = -cc
            assert dot(m, (Q5(0), Q5(0), Q5(0))) <= cc
            outer.append((m, cc))
        planes = [(uu, cc) for uu, cc in QF] + [(tuple(-x for x in n), Q5(0)) for n in cone]
        Pf = np.array([[float(x) for x in p[0]] for p in planes]); bf = np.array([float(p[1]) for p in planes])
        verts = []
        for t3 in itertools.combinations(range(len(planes)), 3):
            A3 = Pf[list(t3)]
            if abs(np.linalg.det(A3)) < 1e-12: continue
            x = np.linalg.solve(A3, bf[list(t3)])
            if np.all(Pf @ x <= bf + 1e-9):
                X = solve3([planes[k][0] for k in t3], [planes[k][1] for k in t3])
                if X is not None and all(dot(pp, X) <= cc for pp, cc in planes):
                    verts.append(X)
        assert verts
        for m, cc in outer:
            mx = maxq([dot(m, v) for v in verts])
            if mx > Q5(0):
                val = cc / mx
                best = val if best is None or val < best else best
    return best


def apply3(g, p): return tuple(dot(g[r], p) for r in range(3))


def sym_I(IP):
    """All orthogonal maps (exact, Q(sqrt5)) taking the icosahedron's corner set to itself."""
    a = IP[0]
    nb = [q for q in IP if q != a and dot(sub(q, a), sub(q, a)) == minq([dot(sub(r, a), sub(r, a)) for r in IP if r != a])]
    b = nb[0]
    c = [q for q in nb if dot(sub(q, b), sub(q, b)) == dot(sub(b, a), sub(b, a))][0]
    src = [a, b, c]
    out = []
    S3 = [list(r) for r in src]  # rows = source points; g maps src_k -> dst_k: g = D^T (S^T)^{-1}
    for a2 in IP:
        for b2 in IP:
            for c2 in IP:
                if len({repr(a2), repr(b2), repr(c2)}) < 3: continue
                if any(dot(x, y) != dot(u, v) for (x, u) in zip(src, (a2, b2, c2)) for (y, v) in zip(src, (a2, b2, c2))):
                    continue
                # solve g * src_k = dst_k: for each row r of g, g_r . src_k = dst_k[r]
                g = [solve3(S3, [d[r] for d in (a2, b2, c2)]) for r in range(3)]
                if any(x is None for x in g): continue
                if frozenset(map(repr, IP)) == frozenset(repr(apply3(g, p)) for p in IP):
                    out.append(g)
    return out


def part_a():
    raw = json.load(open(os.path.join(ST, "2026-10-25-gnomon-shapes", "stations-exact.json")))
    S = {k: [tuple(Q5(Fr(c[0]), Fr(c[1])) for c in p) for p in v] for k, v in raw.items()}
    names = ["I", "Cleo star", "D′", "ID", "OG", "rTI", "TI", "H", "jtI", "RT", "M", "I·φ³"]
    pts = {n: S[n] for n in names if n in S}
    pts["Cleo star"] = S["I"] + S["Cleo star tips"]  # corners of the (non-convex) Cleo star: I's 12 and the 20 tips
    F, conv = {}, {}
    for n in names:
        F[n], hull = facets(pts[n])
        conv[n] = (len(hull.vertices) == len(pts[n]))
    check("every station except the Cleo star is convex with all stored points as corners",
          all(conv[n] for n in names if n != "Cleo star") and not conv["Cleo star"],
          "; ".join(f"{n}: {len(pts[n])} corners, {len(F[n])} facets" for n in names))
    check("control: I·φ³ = φ³ I exactly", sorted(map(repr, scale(PHI3, pts["I"]))) == sorted(map(repr, pts["I·φ³"])))
    # nesting S_j subset S_j+1 exactly (upper convex station: facet test; Cleo star upper: test against D' = its hull and
    # the I-part separately)
    nest = []
    for j in range(len(names) - 1):
        lo, up = names[j], names[j + 1]
        ok = all(dot(u, p) <= c for u, c in F[up] for p in pts[lo])
        nest.append(ok)
    check("control: every nesting S_j ⊂ hull(S_j+1) holds exactly (11 steps)", all(nest))
    G = sym_I(pts["I"])
    check("the symmetry group of I has 120 elements (exact)", len(G) == 120)
    inv_ok = {n: all(frozenset(map(repr, pts[n])) == frozenset(repr(apply3(g, p)) for p in pts[n]) for g in G) for n in names}
    check("every station's corner set is invariant under all 120 symmetries of I (so one face cone of the star suffices)",
          all(inv_ok.values()), str([n for n in names if not inv_ok[n]]))
    sI = star_hi(pts["I"], F["I"], pts["I"], S["Cleo star tips"], Q5(1))
    check("control (star test): s·I lies in the Cleo star exactly for s <= 1 (its corners leave the star at once)", sI == Q5(1), repr(sI))
    sD = star_hi(pts["D′"], F["D′"], pts["I"], S["Cleo star tips"], Q5(1))
    check("control (star test): the Cleo star's own hull D′ is not inside it (s < 1)", sD < Q5(1), repr(sD))
    rev = all(dot(u, p) <= c for u, c in F["TI"] for p in pts["RT"])
    check("control that fails as it should: RT ⊄ TI", not rev)
    # windows
    convex = [n for n in names if n != "Cleo star"]
    chain = [(n, 0) for n in names] + [(n, 1) for n in names[1:]]  # this turn and the next (scaled by φ³)

    def P_of(n, m): return pts[n] if m == 0 else scale(PHI3, pts[n])

    def F_of(n, m): return F[n] if m == 0 else [(tuple(x / PHI3 for x in u), c) for u, c in F[n]]
    res = []
    for i, X in enumerate(names):
        if X == "Cleo star": continue
        for j in range(i, i + 11):  # gaps (chain[j], chain[j+1]) with the run X -> sX shorter than a turn
            (Lo, mlo), (Up, mup) = chain[j], chain[j + 1]
            PL = P_of(Lo, mlo)
            lo = maxq([h(PL, u) / c for u, c in F[X]])   # PL ⊂ sX
            hi = minq([c / h(pts[X], u) for u, c in F_of(Up, mup)])  # sX ⊂ hull(Up)
            star = (Up == "Cleo star")
            if star:  # exact: the Cleo star is star-shaped; per face cone it is the bipyramid conv(0, F, tip)
                hi2 = star_hi(pts[X], F[X], pts["I"], S["Cleo star tips"], PHI3 if mup else Q5(1))
                hi = hi2 if hi2 < hi else hi
            # a proper insertion: 1 < s < phi^3 (s = 1 is X itself, s = phi^3 is X one turn later)
            lo_eff = lo if lo > Q5(1) else Q5(1)
            hi_eff = hi if hi < PHI3 else PHI3
            if lo_eff < hi_eff:
                nonempty = True
            elif lo_eff == hi_eff:
                nonempty = (Q5(1) < lo_eff < PHI3)
            else:
                nonempty = False
            res.append(dict(X=X, i=i, j=j, gap=f"{Lo}{'·φ³' if mlo else ''} → {Up}{'·φ³' if mup else ''}", lo=repr(lo), hi=repr(hi),
                            lo_f=float(lo), hi_f=float(hi), window=nonempty, upper_star_exact=star,
                            steps_X_to_sX=(j + 1) - i if nonempty else None))
    wins = [r for r in res if r["window"]]
    for r in wins: print("  WINDOW", r)
    check("windows computed for 11 convex stations × 11 gaps", len(res) == 121)
    # D (the full Dharma dodecahedron) = (3/2) D′: is it in a window?
    out = dict(windows=res, nonempty=wins)
    # the closest approach: for each X, the largest ratio hi/lo over its gaps (window exists iff some ratio >= 1)
    best = {}
    for r in res:
        q = r["hi_f"] / r["lo_f"]
        if r["X"] not in best or q > best[r["X"]][0]: best[r["X"]] = (q, r["gap"], r["lo_f"], r["hi_f"])
    for X, v in best.items(): print(f"  {X}: best gap {v[1]}: need s >= {v[2]:.6f} and s <= {v[3]:.6f} (ratio {v[0]:.6f})")
    out["best"] = best
    return out, wins


# ---------------- (b) capped cubes
hs = sp.symbols("h", positive=True)
u_, v_ = sp.symbols("u v", positive=True)   # u = sqrt(2 + h^2), v = sqrt(2 + (1 - h)^2)


def cs(kind, which):
    """(cos, sin) of the angle as rational functions of h, u, v."""
    x = hs if which == 0 else 1 - hs
    r = u_ if which == 0 else v_
    if kind == "A":   # pi/2 + 2 atan x
        return (-2 * x / (1 + x ** 2), (1 - x ** 2) / (1 + x ** 2))
    else:             # pi - arccos(1/(1 + x^2))
        return (-1 / (1 + x ** 2), x * r / (1 + x ** 2))


def ang(kind, which, hv):
    x = hv if which == 0 else 1 - hv
    return mp.pi / 2 + 2 * mp.atan(x) if kind == "A" else mp.pi - mp.acos(1 / (1 + x ** 2))


ANG = [("A", 0), ("B", 0), ("A", 1), ("B", 1)]
NAME = {("A", 0): "A(h)", ("B", 0): "B(h)", ("A", 1): "A(1−h)", ("B", 1): "B(1−h)"}


def triple_roots(T):
    (c1, s1), (c2, s2), (c3, s3) = (cs(*t) for t in T)
    expr = sp.together(s1 * c2 * c3 + c1 * s2 * c3 + c1 * c2 * s3 - s1 * s2 * s3)
    num = sp.expand(sp.numer(expr))
    p = sp.Poly(num, u_, v_, hs)
    p1 = sp.resultant(p.as_expr(), u_ ** 2 - (2 + hs ** 2), u_)
    p2 = sp.resultant(sp.expand(p1), v_ ** 2 - (2 + (1 - hs) ** 2), v_)
    P = sp.Poly(sp.expand(p2), hs)
    if P.is_zero: return None, []
    roots = []
    for fac, _ in sp.factor_list(P)[1]:
        for iv in sp.Poly(fac, hs).intervals():
            (a, b), _m = iv
            if b <= 0 or a >= 1: continue
            if not (a >= 0 and b <= 1):
                # refine to decide whether the root is inside (0, 1)
                iv2 = sp.Poly(fac, hs).refine_root(a, b, eps=sp.Rational(1, 10 ** 12))
                a, b = iv2
                if b <= 0 or a >= 1: continue
            mp.mp.dps = 60
            a2, b2 = sp.Poly(fac, hs).refine_root(a, b, eps=sp.Rational(1, 10 ** 58))
            r = (mp.mpf(a2.p) / a2.q + mp.mpf(b2.p) / b2.q) / 2
            if not (0 < r < 1): continue
            tot = sum(ang(k, w, r) for k, w in T)
            roots.append((r, tot - 2 * mp.pi, sp.Poly(fac, hs)))
    return P, roots


def part_b():
    mp.mp.dps = 60
    out = {"triples": []}
    triples = list(itertools.combinations_with_replacement(ANG, 3))
    cand = []
    for T in triples:
        P, roots = triple_roots(T)
        true = [(r, e, f) for r, e, f in roots if abs(e) < mp.mpf(10) ** -45]
        spur = [(r, e, f) for r, e, f in roots if abs(e) >= mp.mpf(10) ** -45]
        assert all(abs(e) > mp.mpf(10) ** -6 for r, e, f in spur), "ambiguous root"
        out["triples"].append(dict(triple=[NAME[t] for t in T], true_roots=[mp.nstr(r, 30) for r, e, f in true],
                                   minpolys=[str(f.as_expr()) for r, e, f in true], spurious=len(spur)))
        print("  triple", [NAME[t] for t in T], "roots in (0,1):", [mp.nstr(r, 20) for r, e, f in true], flush=True)
        for r, e, f in true: cand.append((r, T, f))
    # at each candidate h, which of the four edge angles can be completed by some triple?
    verdicts = []
    for r, T0, f in cand:
        ok = {}
        for a in ANG:
            ok[NAME[a]] = any(a in T and abs(sum(ang(k, w, r) for k, w in T) - 2 * mp.pi) < mp.mpf(10) ** -45 for T in triples)
        margin = min(abs(sum(ang(k, w, r) for k, w in T) - 2 * mp.pi) for T in triples
                     if abs(sum(ang(k, w, r) for k, w in T) - 2 * mp.pi) >= mp.mpf(10) ** -45)
        both = all(ok.values())
        alone_h = ok["A(h)"] and ok["B(h)"]
        verdicts.append(dict(h=mp.nstr(r, 30), minpoly=str(f.as_expr()), from_triple=[NAME[t] for t in T0], completable=ok,
                             both_pieces_pass=both, P_h_alone_passes=alone_h, margin_others=mp.nstr(margin, 5)))
        print("  candidate h =", mp.nstr(r, 25), ok, "both pass:", both, flush=True)
    out["candidates"] = verdicts
    check("controls: A(1) = pi (cube edge flattens: the rhombic dodecahedron's rhombi), B(1) = 2pi/3 (RD's 120°), "
          "A(1/2) = B(1/2) = arccos(-4/5) (tetrakis hexahedron)",
          abs(ang("A", 0, mp.mpf(1)) - mp.pi) < 1e-50 and abs(ang("B", 0, mp.mpf(1)) - 2 * mp.pi / 3) < 1e-50
          and abs(ang("A", 0, mp.mpf(1) / 2) - mp.acos(-mp.mpf(4) / 5)) < 1e-50 and abs(ang("B", 0, mp.mpf(1) / 2) - mp.acos(-mp.mpf(4) / 5)) < 1e-50)
    g = (1 + mp.sqrt(5)) / 2
    check("control: golden polars' angles as in #54 Remarks (153.43°, 136.35° / 131.81°, 150.77°)",
          [round(float(mp.degrees(ang(k, 0, x))), 2) for x in (1 / g, 1 / g ** 2) for k in ("A", "B")] == [153.43, 136.35, 131.81, 150.77])
    # pass control: h = 2 - sqrt3 makes 3 A(h) = 2pi, so P(h) passes for its cube edges (the test can say yes)
    h0 = 2 - mp.sqrt(3)
    check("pass control: h = 2 − √3 gives A(h) = 2π/3 exactly (three cube edges close)", abs(3 * ang("A", 0, h0) - 2 * mp.pi) < 1e-50)
    found = any(abs(mp.mpf(c["h"]) - h0) < 1e-25 for c in verdicts)
    check("pass control: the elimination finds h = 2 − √3 among the roots of 3·A(h) = 2π", found)
    return out, verdicts


def tricap_angles():
    """Exact interior dihedral angles of the Tricap: apex (1,1,1)/(2φ), base (0,1/2,φ/2), (φ/2,0,1/2), (1/2,φ/2,0)."""
    half = Fr(1, 2)
    ap = tuple(Q5(1) / (2 * PHI) for _ in range(3))
    b1 = (Q5(0), Q5(half), PHI / 2); b2 = (PHI / 2, Q5(0), Q5(half)); b3 = (Q5(half), PHI / 2, Q5(0))
    V = [ap, b1, b2, b3]
    cen = tuple(sum((v[i] for v in V), Q5(0)) / 4 for i in range(3))
    faces = list(itertools.combinations(range(4), 3))
    N = {}
    for f in faces:
        a, b, c = (V[i] for i in f)
        n = cross(sub(b, a), sub(c, a))
        if dot(n, sub(cen, a)) > Q5(0): n = tuple(-x for x in n)
        N[f] = n
    out = []
    for e in itertools.combinations(range(4), 2):
        f1, f2 = [f for f in faces if set(e) <= set(f)]
        n1, n2 = N[f1], N[f2]
        c2num = dot(n1, n2)  # cos(interior) = - n1.n2 / (|n1||n2|)
        # exact: cos^2 = (n1.n2)^2 / (|n1|^2 |n2|^2), sign from -n1.n2
        cos2 = (c2num * c2num) / (dot(n1, n1) * dot(n2, n2))
        sgn = -c2num.sign()
        val = -float(c2num) / (float(dot(n1, n1)) ** 0.5 * float(dot(n2, n2)) ** 0.5)
        out.append(dict(edge=e, cos2=repr(cos2), cos_sign=sgn, deg=float(np.degrees(np.arccos(val)))))
    return out, V


def part_b_tricaps():
    mp.mp.dps = 60
    g = (1 + mp.sqrt(5)) / 2
    tri, V = tricap_angles()
    vol = abs(float(dot(sub(V[1], V[0]), cross(sub(V[2], V[0]), sub(V[3], V[0]))))) / 6
    check("control: Tricap volume (3 − √5)/24 = 1/(12φ²) as in #54", abs(vol - (3 - 5 ** 0.5) / 24) < 1e-14, f"{vol}")
    # high-precision Tricap angles from the exact cos^2 and sign
    # recompute at 60 digits directly
    def mpv(q): return mp.mpf(q.a.numerator) / q.a.denominator + mp.mpf(q.b.numerator) / q.b.denominator * mp.sqrt(5)
    half = Fr(1, 2)
    ap = tuple(Q5(1) / (2 * PHI) for _ in range(3))
    faces = list(itertools.combinations(range(4), 3))
    cen = tuple(sum((v[i] for v in V), Q5(0)) / 4 for i in range(3))
    N = {}
    for f in faces:
        a, b, c = (V[i] for i in f)
        n = cross(sub(b, a), sub(c, a))
        if dot(n, sub(cen, a)) > Q5(0): n = tuple(-x for x in n)
        N[f] = n
    tri_mp = []
    for e in itertools.combinations(range(4), 2):
        f1, f2 = [f for f in faces if set(e) <= set(f)]
        n1, n2 = N[f1], N[f2]
        tri_mp.append(mp.acos(-mpv(dot(n1, n2)) / mp.sqrt(mpv(dot(n1, n1)) * mpv(dot(n2, n2)))))
    distinct = []
    for x in tri_mp:
        if not any(abs(x - y) < 1e-40 for y in distinct): distinct.append(x)
    pol = {"A(1/φ)": ang("A", 0, 1 / g), "B(1/φ)": ang("B", 0, 1 / g), "A(1/φ²)": ang("A", 0, 1 / g ** 2), "B(1/φ²)": ang("B", 0, 1 / g ** 2)}
    allang = dict(pol);
    for i, x in enumerate(distinct): allang[f"Tricap{i + 1}"] = x
    allang["pi (face interior)"] = mp.pi
    print("  angles (deg):", {k: mp.nstr(mp.degrees(v), 12) for k, v in allang.items()}, flush=True)
    keys = list(allang)
    vals = [allang[k] for k in keys]
    mn = min(vals)
    maxk = int(2 * mp.pi / mn) + 1
    combos = []

    def rec(start, left, cur):
        if abs(left) < mp.mpf(10) ** -40 and cur:
            combos.append(list(cur)); return
        if left < -mp.mpf(10) ** -40: return
        for i in range(start, len(keys)):
            if vals[i] - left > mp.mpf(10) ** -40: continue
            cur.append(keys[i]); rec(i, left - vals[i], cur); cur.pop()
    rec(0, 2 * mp.pi, [])
    # remove combos that are only 2 x pi (no edge)
    combos = [c for c in combos if any(k != "pi (face interior)" for k in c)]
    # near misses (closest sums not equal to 2pi), to show the margin
    near = []

    def rec2(start, tot, cur, depth):
        if cur:
            d = abs(tot - 2 * mp.pi)
            if d >= mp.mpf(10) ** -40 and d < mp.mpf("0.01"): near.append((float(mp.degrees(d)), list(cur)))
        if depth == 0 or tot > 2 * mp.pi: return
        for i in range(start, len(keys)):
            cur.append(keys[i]); rec2(i, tot + vals[i], cur, depth - 1); cur.pop()
    rec2(0, mp.mpf(0), [], maxk)
    near.sort()
    print("  combinations closing 2π:", combos, flush=True)
    print("  nearest misses (deg):", near[:5], flush=True)
    covered = {k: any(k in c for c in combos) for k in pol}
    return dict(angles_deg={k: mp.nstr(mp.degrees(v), 15) for k, v in allang.items()}, tricap_exact=tri, combos=combos,
                near_misses=near[:10], polar_edges_completable=covered), covered, combos


if __name__ == "__main__":
    A, wins = part_a()
    B, verd = part_b()
    C, covered, combos = part_b_tricaps()
    print(f"  (a) {len(wins)} proper windows (1 < s < φ³) for a scaled station inside one turn")
    check("(b) no h in (0,1) lets P(h) and P(1−h) pass the edge test together", not any(v["both_pieces_pass"] for v in verd),
          f"candidates {[(v['h'][:12], v['completable']) for v in verd]}")
    check("(b) with the Tricaps: some edge of the golden polars still has no closing combination",
          not all(covered.values()), f"{covered}")
    json.dump(dict(a=A, b=B, tricaps=C), open(os.path.join(HERE, "..", "data", "gnomon_open.json"), "w"), indent=1, default=str)
    with open(os.path.join(HERE, "..", "data", "gnomon_open-checks.txt"), "w") as fh:
        for s_, n, det in checks: fh.write(f"{s_} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print("FINAL ok" if checks and nf == 0 else f"FINAL FAIL: {nf} of {len(checks)} checks failed")
