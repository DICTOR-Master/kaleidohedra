"""Independent recheck of the 2026-11-24-resonus-4d README (exact arithmetic in Q(sqrt5)).

Written without reading that study's scripts. Different constructions:
 - 600-cell: the 120 unit icosians generated as a GROUP by quaternion multiplication from two generators;
   its 600 facets found as the supporting 4-cliques of the edge graph.
 - 120-cell: the polar {x : v.x <= 1, v a 600-cell corner}; its facets are these 120 inequalities, its corners
   are computed as the 600 facet points of the 600-cell (never listed).
 - 24-cells: the 25 sets g T h (T = the 24 Hurwitz units), by quaternion products, not by reflections.
 - Vacuus plates: normal = exact null vector of the ridge's corners (not a_F - a_F').
 - Mirrors: exact reflection test of every candidate root b - w (b in a spanning set of corners).
Every quantity is exact; FINAL ok is printed only if every check passes.
"""
from fractions import Fraction as Fr
from itertools import combinations, permutations, product
import sys

# ---------- Q(sqrt5): (a, b) means a + b*sqrt5 ----------
class K:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0):
        s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = k(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = k(o); return K(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return k(o) - s
    def __neg__(s): return K(-s.a, -s.b)
    def __mul__(s, o): o = k(o); return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        return K(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * k(o).inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = k(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        # exact sign of a + b sqrt5
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # opposite signs: compare a^2 with 5 b^2
        c = a * a - 5 * b * b
        if a > 0: return (c > 0) - (c < 0)
        return -((c > 0) - (c < 0))
    def __repr__(s): return f"({s.a}+{s.b}r5)"

def k(x): return x if isinstance(x, K) else K(x)
ZERO, ONE = K(0), K(1)
R5 = K(0, 1)
PHI = K(Fr(1, 2), Fr(1, 2))
IPHI = PHI - 1  # 1/phi

def dot(u, v):
    s = K(0)
    for x, y in zip(u, v): s = s + x * y
    return s
def vsub(u, v): return tuple(x - y for x, y in zip(u, v))
def vadd(u, v): return tuple(x + y for x, y in zip(u, v))
def vscale(c, u): return tuple(c * x for x in u)
def key(v): return tuple((x.a, x.b) for x in v)
def linekey(v):
    """canonical key of the line R v"""
    for x in v:
        if not x.iszero():
            return key(vscale(x.inv(), v))
    raise ValueError("zero vector")

def rank(rows):
    M = [list(r) for r in rows]
    if not M: return 0
    n = len(M[0]); r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][c].inv()
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r

def nullvec(rows, n):
    """exact null vector of rows (must be 1-dimensional)"""
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][c].inv(); M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    assert len(free) == 1, ("null space dim", len(free))
    f = free[0]; v = [K(0)] * n; v[f] = K(1)
    for i, c in enumerate(piv): v[c] = -M[i][f]
    return tuple(v)

NCHK = 0
def check(cond, msg):
    global NCHK
    NCHK += 1
    if not cond:
        print("FAIL:", msg); sys.exit(1)

# ---------- generic polytope engine ----------
class Poly:
    """vertices V (centroid 0), facet normals A with a.x <= 1, ambient constraint rows C (e.g. all-ones for sum-zero)."""
    def __init__(s, name, V, A, d, C=()):
        s.name, s.V, s.A, s.d, s.C = name, V, A, d, list(C)
        n = len(V[0])
        # centroid 0
        cen = tuple(sum((v[i] for v in V), K(0)) for i in range(n))
        check(all(x.iszero() for x in cen), name + " centroid")
        # facets: supporting + tight set of affine dim d-1
        s.T = []
        for a in A:
            vals = [dot(a, v) - 1 for v in V]
            check(all(x.sign() <= 0 for x in vals), name + " supporting")
            t = frozenset(i for i, x in enumerate(vals) if x.iszero())
            p0 = V[min(t)]
            check(rank([vsub(V[i], p0) for i in t]) == d - 1, name + " facet dim")
            s.T.append(t)
        check(len(set(s.T)) == len(A), name + " distinct facets")
        # ridges = facet pairs meeting in affine dim d-2
        s.ridges = []
        for i, j in combinations(range(len(A)), 2):
            t = s.T[i] & s.T[j]
            if t and len(t) >= d - 1:
                p0 = V[min(t)]
                if rank([vsub(V[x], p0) for x in t]) == d - 2:
                    s.ridges.append((i, j, t))
        # closed boundary: each facet's ridges count matches; every ridge in exactly 2 facets (by construction pairs);
        # verify no ridge set is shared by 3 facets
        rs = [r[2] for r in s.ridges]
        check(len(set(rs)) == len(rs), name + " ridge in exactly two facets")

    def edges(s):
        # pairs u,v whose common facets cut out exactly {u,v}
        inc = [set() for _ in s.V]
        for fi, t in enumerate(s.T):
            for x in t: inc[x].add(fi)
        E = 0
        allv = frozenset(range(len(s.V)))
        for u, v in combinations(range(len(s.V)), 2):
            F = inc[u] & inc[v]
            if len(F) < s.d - 1: continue
            t = allv
            for f in F: t = t & s.T[f]
            if t == {u, v}: E += 1
        return E

    def resonus(s):
        return {linekey(a) for a in s.A}

    def vacuus(s):
        out = {}
        for (i, j, t) in s.ridges:
            rows = [s.V[x] for x in t] + s.C
            nv = nullvec(rows, len(s.V[0]))
            out.setdefault(linekey(nv), []).append((i, j))
        return out

    def mirrors(s):
        Vs = {key(v) for v in s.V}
        # spanning set
        base = []
        for i, v in enumerate(s.V):
            if rank([s.V[b] for b in base] + [v]) > len(base): base.append(i)
            if len(base) == s.d: break
        check(len(base) == s.d, s.name + " spanning corners")
        M = set()
        for b in base:
            for w in range(len(s.V)):
                if w == b: continue
                r = vsub(s.V[b], s.V[w]); lk = linekey(r)
                if lk in M: continue
                rr = dot(r, r)
                ok = True
                for v in s.V:
                    img = vsub(v, vscale(2 * dot(v, r) / rr, r))
                    if key(img) not in Vs: ok = False; break
                if ok: M.add(lk)
        return M

def report(P, fvec=None):
    Res = P.resonus(); Vac = P.vacuus(); Mir = P.mirrors()
    resfac = {}
    for a in P.A: resfac[linekey(a)] = resfac.get(linekey(a), 0) + 1
    vr = sorted({len(x) for x in Vac.values()})
    row = dict(name=P.name, mirrors=len(Mir), resonus=len(Res), res_each=sorted(set(resfac.values())),
               vacuus=len(Vac), vac_each=vr, res_cap_vac=len(Res & set(Vac)),
               res_on_mir=len(Res & Mir), vac_on_mir=len(set(Vac) & Mir), facets=len(P.A), ridges=len(P.ridges))
    if fvec:
        E = P.edges()
        f = (len(P.V), E, len(P.ridges), len(P.A))
        check(f == fvec, f"{P.name} f-vector {f} vs {fvec}")
        check(f[0] - f[1] + f[2] - f[3] == 0, P.name + " Euler")
        row["f"] = f
    print(row, flush=True)
    return row, Res, Vac, Mir

def facets_by_subsets(V, d, cands=None):
    """all facet normals a (a.x<=1) from d-subsets of corners"""
    A = {}
    for S in (cands if cands is not None else combinations(range(len(V)), d)):
        rows = [V[i] for i in S]
        if rank(rows) < d: continue
        # solve a . v_i = 1
        M = [list(r) + [ONE] for r in rows]
        # gaussian solve
        n = d
        for c in range(n):
            p = next(i for i in range(c, n) if not M[i][c].iszero())
            M[c], M[p] = M[p], M[c]
            iv = M[c][c].inv(); M[c] = [x * iv for x in M[c]]
            for i in range(n):
                if i != c and not M[i][c].iszero():
                    f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[c])]
        a = tuple(M[i][n] for i in range(n))
        if all((dot(a, v) - 1).sign() <= 0 for v in V):
            A[key(a)] = a
    return list(A.values())

# ---------- quaternions ----------
def qmul(p, q):
    a1, b1, c1, d1 = p; a2, b2, c2, d2 = q
    return (a1*a2 - b1*b2 - c1*c2 - d1*d2, a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2, a1*d2 + b1*c2 - c1*b2 + d1*a2)

def closure(gens):
    G = {key(g): g for g in gens}
    frontier = list(G.values())
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = qmul(x, g)
                if key(y) not in G: G[key(y)] = y; new.append(y)
        frontier = new
    return list(G.values())

def main():
    h = Fr(1, 2)
    rows = []
    # ---- 600-cell from the icosian group ----
    g1 = (K(h), K(h), K(h), K(h))                      # order 6
    g2 = (PHI * h, K(h), IPHI * h, K(0))               # order 10
    I = closure([g1, g2])
    check(len(I) == 120, "icosian group order 120")
    check(all(dot(q, q) == 1 for q in I), "unit icosians")
    ip = {}
    for u, v in combinations(I, 2):
        x = dot(u, v); ip[x] = ip.get(x, 0) + 1
    # edges: inner product phi/2 (nearest neighbours)
    near = PHI * h
    check(near in ip and all((x - near).sign() <= 0 for x in ip), "phi/2 is the largest inner product of distinct corners")
    nb = [set() for _ in I]
    for i, j in combinations(range(120), 2):
        if dot(I[i], I[j]) == near: nb[i].add(j); nb[j].add(i)
    check(all(len(x) == 12 for x in nb), "600-cell: 12 neighbours")
    tets = set()
    for i in range(120):
        for j, kk, l in combinations(sorted(nb[i]), 3):
            if kk in nb[j] and l in nb[j] and l in nb[kk]:
                tets.add(tuple(sorted((i, j, kk, l))))
    A600 = facets_by_subsets(I, 4, cands=sorted(tets))
    check(len(A600) == 600, "600 facets")
    P = Poly("600-cell", I, A600, 4)
    r, ResP, VacP, MirP = report(P, (120, 720, 1200, 600)); rows.append(r)
    check(len(MirP) == 60 and MirP == {linekey(q) for q in I}, "600-cell mirrors = icosian lines")
    check(len(ResP) == 300 and not (ResP & MirP), "600-cell Resonus 300, no mirror")
    check(set(VacP) == MirP and all(len(x) == 20 for x in VacP.values()), "600-cell Vacuus = mirrors, 20 each")

    # ---- 120-cell as the polar: inequalities v.x <= 1 ----
    Qv = A600  # corners of the polar = facet points of the 600-cell
    Q = Poly("120-cell", Qv, list(I), 4)
    r, ResQ, VacQ, _ = report(Q, (600, 1200, 720, 120)); rows.append(r)
    # mirrors: Sym(P*) = Sym(P); confirm each of P's 60 mirrors maps Q's corners to themselves
    Qs = {key(v) for v in Qv}
    for q in I:
        rr = dot(q, q)
        check(all(key(vsub(v, vscale(2 * dot(v, q) / rr, q))) in Qs for v in Qv), "mirror of 120-cell")
    MirQ = MirP
    check(len(_) == 60 and _ == MirP, "120-cell mirrors by direct search = the 60")
    check(ResQ == MirQ, "Resonus(120-cell) = 60 H4 mirrors")
    check(set(VacQ) == MirQ and all(len(x) == 12 for x in VacQ.values()), "120-cell Vacuus = mirrors, 12 each")
    check(ResP == {linekey(v) for v in Qv}, "Resonus(600) normals along 120-cell corners")

    # ---- 25 inscribed 24-cells = g T h ----
    T = [q for q in I if all(x.b == 0 and (x.a.denominator in (1, 2)) for x in q)
         and (all(x.a.denominator == 1 for x in q) or all(abs(x.a) == h for x in q))]
    check(len(T) == 24, "24 Hurwitz units in the icosians")
    cells = set()
    for g in I:
        for hh in I:
            S = frozenset(key(qmul(qmul(g, t), hh)) for t in T)
            cells.add(S)
    check(len(cells) == 25, "25 sets gTh")
    Ikey = {key(q): q for q in I}
    walls = []
    for S in cells:
        W = [Ikey[x] for x in S]
        check(all(dot(u, v) in (K(0), K(h), K(-h), K(1), K(-1)) for u in W for v in W), "24-cell inner products")
        # facets of the 24-cell from orthogonal pairs u+w (candidate directions), checked as facets
        cand = {}
        for u, w in combinations(W, 2):
            if dot(u, w).iszero():
                c = vadd(u, w)
                m = K(0)
                for x in W:
                    z = dot(c, x)
                    if (z - m).sign() > 0: m = z
                a = vscale(m.inv(), c)
                cand[key(a)] = a
        C24 = Poly("24-cell (inscribed)", W, list(cand.values()), 4)
        check(len(C24.A) == 24 and len(C24.ridges) == 96, "inscribed 24-cell: 24 cells, 96 ridges")
        Rs = C24.resonus()
        check(len(Rs) == 12, "24-cell Resonus 12")
        walls.append(Rs)
    allw = set().union(*walls)
    check(sum(len(w) for w in walls) == 300 and len(allw) == 300, "25 x 12 distinct")
    check(allw == ResP, "middle walls of the 25 24-cells = Resonus(600-cell)")
    # each middle wall holds 12 corners of the 600-cell
    for lk in list(allw)[:300]:
        n = tuple(K(a, b) for a, b in lk)
        check(sum(1 for q in I if dot(q, n).iszero()) == 12, "12 corners on each cross wall")
    print("25 inscribed 24-cells: 300 middle walls = Resonus(600-cell); 12 corners each", flush=True)

    # ---- small rows ----
    # 5-cell in R^5 sum-zero
    one5 = tuple(K(1) for _ in range(5))
    V5 = [tuple(K(Fr(4, 5)) if i == j else K(Fr(-1, 5)) for i in range(5)) for j in range(5)]
    # facet opposite corner j: x_j >= -1/5 ... as a.x <= 1 with a = -5 e_j + const*1 (const irrelevant on sum-zero); project
    A5 = [tuple(K(-5) + K(1) if i == j else K(1) for i in range(5)) for j in range(5)]
    A5 = [vsub(a, vscale(dot(a, one5) / 5, one5)) for a in A5]
    P5 = Poly("5-cell", V5, A5, 4, C=[one5])
    rows.append(report(P5, (5, 10, 10, 5))[0])
    # tesseract
    Vt = [tuple(K(s) for s in sg) for sg in product((1, -1), repeat=4)]
    rows.append(report(Poly("tesseract", Vt, facets_by_subsets(Vt, 4), 4), (16, 32, 24, 8))[0])
    # 16-cell
    V16 = [tuple(K(s if i == j else 0) for i in range(4)) for j in range(4) for s in (1, -1)]
    rows.append(report(Poly("16-cell", V16, facets_by_subsets(V16, 4), 4), (8, 24, 32, 16))[0])
    # 24-cell
    V24 = set()
    for i, j in combinations(range(4), 2):
        for s, t in product((1, -1), repeat=2):
            v = [K(0)] * 4; v[i] = K(s); v[j] = K(t); V24.add(tuple(v))
    V24 = sorted(V24, key=key)
    r24 = report(Poly("24-cell", V24, facets_by_subsets(V24, 4), 4), (24, 96, 96, 24)); rows.append(r24[0])
    # permutohedron from its H-description sum_{S} x_i >= |S|(|S|+1)/2 (coordinates 1..5, centred at 3)
    Vp = [tuple(K(x - 3) for x in p) for p in permutations(range(1, 6))]
    Ap = []
    for m in range(1, 5):
        for S in combinations(range(5), m):
            # sum_{i in S} y_i >= m(m+1)/2 - 3m  ->  a.y <= 1 with a = -1_S / (3m - m(m+1)/2)
            c = Fr(3 * m) - Fr(m * (m + 1), 2)
            a = tuple(K(-1 / c) if i in S else K(0) for i in range(5))
            a = vsub(a, vscale(dot(a, one5) / 5, one5))
            Ap.append(a)
    Pp = Poly("4D permutohedron", Vp, Ap, 4, C=[one5])
    rp = report(Pp, (120, 240, 150, 30)); rows.append(rp[0])
    check(rp[1] <= set(rp[2]), "permutohedron Resonus inside Vacuus")

    expect = {"5-cell": (10, 5, 10, 0, 0, 10), "tesseract": (16, 4, 12, 0, 4, 12), "16-cell": (16, 8, 4, 0, 0, 4),
              "24-cell": (24, 12, 12, 12, 12, 12), "600-cell": (60, 300, 60, 0, 0, 60),
              "120-cell": (60, 60, 60, 60, 60, 60), "4D permutohedron": (10, 15, 65, 15, 0, 0)}
    for r in rows:
        got = (r["mirrors"], r["resonus"], r["vacuus"], r["res_cap_vac"], r["res_on_mir"], r["vac_on_mir"])
        check(got == expect[r["name"]], f"table row {r['name']}: {got} vs {expect[r['name']]}")
        print("row agrees:", r["name"], got, "facets-per-Resonus", r["res_each"], "ridges-per-plate", r["vac_each"])
    check(r24[1] == set(r24[2]), "24-cell Resonus = Vacuus")
    print(f"FINAL ok ({NCHK} exact checks)")

if __name__ == "__main__":
    main()
