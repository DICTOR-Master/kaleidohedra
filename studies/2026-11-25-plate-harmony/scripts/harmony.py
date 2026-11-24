"""The harmony tests for one central plane arrangement in R^3, exact (plate-harmony study, 25 Nov 2026).

Input: a number field F (nf.NF) and plane normals with entries in F. Every equality is decided exactly in F; Arb balls are
used only for orders and for picking a root, never to decide an equality.

Tests (DICTO's numbering):
 (3) equiangular: all pairwise angles equal (cos^2 equal, exact);
 (4) the planes split into mutually perpendicular triples (exact perpendicularity; exhaustive search with a node cap);
 (5) equal emptiness: all regions on the sphere have equal area. Necessary condition used (exact): two planes that are
     neighbours in a pencil bound a lune of area 2a holding whole regions, so a*R/(2 pi) must be an integer (R regions).
     If a/pi is irrational this fails exactly. If every lune passes and the arrangement is a reflection arrangement, the
     regions are congruent (the reflection group permutes them simply transitively), so it holds;
 (6) rational angles: every angle between two planes is a rational multiple of pi (nf.rational_angle);
 (7) characteristic polynomial chi(t) = (t - 1)(t^2 - (n - 1)t + b3) (Orlik-Solomon / Zaslavsky counts) factors over Z;
     freeness: not factoring => not free (Terao's factorisation theorem); reflection => free (Saito, Terao);
     supersolvable => free (Stanley; Jambu-Terao); otherwise Yoshinaga's criterion (2005): free exactly when chi factors
     with the exponents of the Ziegler multirestriction to one plane, computed here by exact linear algebra in F;
 (9) regular pencils: the k >= 2 planes through each intersection line are equally spaced (pi/k) exactly when every pair
     angle t satisfies cos(2k t) = 1, i.e. C_k(2cos 2t) = 2 (Chebyshev), exact in F.
Also: simplicial (every region a triangle: 2 f1 = 3 f2), reflection arrangement (closed under the reflection in each of its
planes), regions R = |chi(-1)| (Zaslavsky).
"""
import itertools, time, functools
from fractions import Fraction
from collections import Counter
from flint import arb, ctx
from nf import rational_angle, cheb_C


def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def canon(n):
    for x in n:
        if x:
            ix = x.inv()
            return tuple(y * ix for y in n)
    raise ValueError("zero vector")


def vkey(v): return tuple(x.key() for x in v)


def dedupe(N):
    seen = {}
    for n in N:
        c = canon(n); seen.setdefault(vkey(c), c)
    return list(seen.values())


def perp_triples(n, adj, cap=2_000_000):
    """True / False / None (cap reached): can 0..n-1 be split into triples of mutually adjacent vertices?"""
    if n % 3: return False
    tri = [set() for _ in range(n)]
    for v in range(n):
        for a in adj[v]:
            if adj[v] & adj[a]: tri[v].add(a)
    if any(not tri[v] for v in range(n)): return False
    used = [False] * n; cnt = [0]

    def rec():
        cnt[0] += 1
        if cnt[0] > cap: raise TimeoutError
        try:
            v = used.index(False)
        except ValueError:
            return True
        used[v] = True
        for a in sorted(adj[v]):
            if used[a] or a < v: continue
            used[a] = True
            for b in sorted(adj[v] & adj[a]):
                if used[b] or b < a: continue
                used[b] = True
                if rec(): return True
                used[b] = False
            used[a] = False
        used[v] = False
        return False
    try:
        return rec()
    except TimeoutError:
        return None


def multirestriction_d1(F, N, H, pts):
    """Smallest exponent of the Ziegler multirestriction of the arrangement to plane H (exact linear algebra in F)."""
    h = N[H]
    e = None
    for ee in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        ev = tuple(F.c(x) for x in ee)
        if any(cross(h, ev)): e = ev; break
    u = cross(h, e); v = cross(h, u)
    uu, vv = dot(u, u), dot(v, v)
    lines = []
    for p, S in pts:
        if H in S:
            lam = dot(p, u) / uu; mu = dot(p, v) / vv
            lines.append((mu, -lam, len(S) - 1))
    tot = sum(m for _, _, m in lines)
    assert tot == len(N) - 1, "multiplicities do not add up"
    for d in range(0, tot // 2 + 1):
        # monomials lam'^i mu'^(d-i); substitute lam' = a s - b T, mu' = b s + a T; need coefficient of s^j (j < m) zero
        rows = []
        for a, b, m in lines:
            exps = []
            for i in range(d + 1):
                poly = {0: F.one}                      # dict: power of s -> coefficient (T power = degree - s power)
                for _ in range(i): poly = _mul(poly, {1: a, 0: -b}, F)
                for _ in range(d - i): poly = _mul(poly, {1: b, 0: a}, F)
                exps.append(poly)
            for j in range(min(m, d + 1)):
                rows.append([a * exps[i].get(j, F.zero) for i in range(d + 1)] + [b * exps[i].get(j, F.zero) for i in range(d + 1)])
        r = rank(rows, 2 * (d + 1))
        if r < 2 * (d + 1): return d, tot - d
    return None


def _mul(p, q, F):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i + j] = out.get(i + j, F.zero) + a * b
    return out


def rank(rows, ncol):
    M = [list(r) for r in rows]
    r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        iv = M[r][c].inv()
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r


def pencil_order(p, idx, N):
    """indices of the planes through the line p, in angular order of their normals (mod pi), with the angle gaps (balls)"""
    e1 = N[idx[0]]; e2 = cross(p, e1)
    b1 = [x.ball() for x in e1]; b2 = [x.ball() for x in e2]
    n1 = sum(x * x for x in b1).sqrt(); n2 = sum(x * x for x in b2).sqrt()
    ang = []
    pi = arb.pi()
    for i in idx:
        nb = [x.ball() for x in N[i]]
        a = arb.atan2(sum(x * y for x, y in zip(nb, b2)) / n2, sum(x * y for x, y in zip(nb, b1)) / n1)
        while a < 0: a += pi
        while a >= pi: a -= pi
        if a.contains(pi) or a.contains(0): a = arb(0) if i == idx[0] else a
        ang.append((a, i))
    ang.sort(key=lambda t: float(t[0].mid()))
    gaps = []
    for k in range(len(ang)):
        a, i = ang[k]; b, j = ang[(k + 1) % len(ang)]
        g = b - a if k + 1 < len(ang) else pi - a + b
        gaps.append((i, j, g))
    return gaps


def _bv(v): return [x.ball() for x in v]
def _bd(a, b): return sum(x * y for x, y in zip(a, b))
def _bx(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def esort(m, items):
    """exact counterclockwise order around the axis m of the vectors in items [(id, exact vector)], all at right angles to m"""
    ref = items[0][1]
    def half(q):
        d = dot(m, cross(ref, q)).sign()
        if d: return 0 if d > 0 else 1
        return 0 if dot(ref, q).sign() > 0 else 1
    H = {i: half(q) for i, q in items}
    def cmp(x, y):
        if H[x[0]] != H[y[0]]: return H[x[0]] - H[y[0]]
        if x[0] == y[0]: return 0
        return -dot(m, cross(x[1], y[1])).sign()
    return [i for i, _ in sorted(items, key=functools.cmp_to_key(cmp))]


def sphericus(N, P, cos2, pair_ang, R):
    """Sphericus (DICTO's name, 25 Nov 2026; exact definition to be fixed with him): the network of great circles, one per
    plane, read on the sphere. (a) crossing points with the number of circles through each; (b) the crossing angles at each
    point (gaps between neighbouring circles); (c) the arcs between consecutive crossings along each circle; (d) region
    shapes (side counts) and areas. Equalities exact: arcs compared by sign of p.q and the exact (p.q)^2/(|p|^2|q|^2); angles by
    the exact cos^2 class of the two planes and the sign of the cosine of the gap; areas exact when every corner angle is a
    rational multiple of pi, otherwise counted as balls that are certified apart (a lower bound on the number of values)."""
    pi = arb.pi()
    V = []; on = []; EX = []
    for c, S in P:
        b = _bv(c)
        V.append(b); on.append(S); EX.append(c); V.append([-x for x in b]); on.append(S); EX.append(tuple(-x for x in c))
    nb = {u: {} for u in range(len(V))}
    arcs = Counter(); percircle = []
    for i in range(len(N)):
        ids = [u for u in range(len(V)) if i in on[u]]
        cyc = esort(N[i], [(u, EX[u]) for u in ids])
        here = set()
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            nb[a][b] = i; nb[b][a] = i
            p, q = EX[a], EX[b]; d = dot(p, q)
            k = (d.sign(), (d * d / (dot(p, p) * dot(q, q))).key())
            arcs[k] += 1; here.add(k)
        percircle.append(len(here))
    def tang(u, w):
        uu = _bd(V[u], V[u]); return [y - _bd(V[w], V[u]) / uu * x for x, y in zip(V[u], V[w])]
    rot = {}
    for u in nb:
        U = EX[u]; uu = dot(U, U)
        rot[u] = esort(U, [(w, tuple(y * uu - dot(EX[w], U) * x for x, y in zip(U, EX[w]))) for w in nb[u]])
    pos = {u: {w: k for k, w in enumerate(r)} for u, r in rot.items()}
    seen = set(); sides = Counter(); exact_areas = []; ball_areas = []; cang = Counter(); allrat = True
    for u in rot:
        for w in rot[u]:
            if (u, w) in seen: continue
            a, b = u, w; tot = Fraction(0); totb = arb(0); k = 0
            while (a, b) not in seen:
                seen.add((a, b)); k += 1
                r = rot[b]; c = r[(pos[b][a] - 1) % len(r)]
                t1, t2 = tang(b, a), tang(b, c)
                cb = _bd(t1, t2) / (_bd(t1, t1) * _bd(t2, t2)).sqrt()
                th = cb.acos(); totb += th
                i, j = nb[b][a], nb[b][c]; ij = (min(i, j), max(i, j))
                sg = 0 if cb.contains(0) else (1 if cb > 0 else -1)
                cang[(cos2[ij].key(), sg)] += 1
                al = pair_ang.get(ij)
                if al is None: allrat = False
                else:
                    hit = [x for x in {al, 1 - al} if abs(th - pi * x.numerator / x.denominator) < arb(10) ** -60]
                    assert len(hit) == 1, "corner angle not identified"
                    tot += hit[0]
                a, b = b, c
            sides[k] += 1
            ball_areas.append(totb - (k - 2) * pi)
            if allrat: exact_areas.append(tot - (k - 2))
    assert sum(sides.values()) == R
    out = {"crossing_points_histogram": {}, "crossing_angle_values": len(cang), "arc_length_values": len(arcs),
           "arc_length_values_per_circle_max": max(percircle), "region_sides": {str(k): v for k, v in sorted(sides.items())}}
    for c, S in P: out["crossing_points_histogram"][str(len(S))] = out["crossing_points_histogram"].get(str(len(S)), 0) + 2
    if allrat:
        assert sum(exact_areas) == 4
        out["area_values_over_pi"] = sorted(str(x) for x in set(exact_areas))[:12]
        out["area_values"] = len(set(exact_areas)); out["areas_exact"] = True; out["_areas"] = exact_areas
    else:
        cl = []
        for x in sorted(ball_areas, key=lambda y: float(y.mid())):
            if cl and cl[-1].overlaps(x): continue
            cl.append(x)
        out["area_values"] = len(cl); out["areas_exact"] = False
    out["harmonious_crossing"] = len(out["crossing_points_histogram"]) == 1 and len(cang) == 1 and len(arcs) == 1
    return out


def analyse(F, normals, name="", reflection_known=None):
    t0 = time.time()
    N = dedupe(normals)
    n = len(N)
    out = {"name": name, "planes": n, "field_degree": F.D}
    if n < 3:
        out.update(rank=n, regions=2 * n, simplicial=False, note="fewer than 3 planes")
        return out
    nn = [dot(a, a) for a in N]
    G = {}
    for i in range(n):
        for j in range(i + 1, n): G[i, j] = dot(N[i], N[j])
    # intersection lines (points on the sphere)
    pts = {}
    for i in range(n):
        for j in range(i + 1, n):
            c = canon(cross(N[i], N[j])); k = vkey(c)
            pts.setdefault(k, [c, set()])[1].update((i, j))
    P = [(c, S) for c, S in pts.values()]
    mult = Counter(len(S) for _, S in P)
    f0 = len(P); f1 = sum(len(S) for _, S in P)
    if f0 == 1:
        out.update(rank=2, regions=2 * n, simplicial=False, chi=f"t(t - 1)(t - {n - 1})", note="a pencil")
        rank3 = False
    else:
        rank3 = True
    b2 = sum(len(S) - 1 for _, S in P); b3 = b2 - n + 1
    R = 2 * (n + b3) if rank3 else 2 * n
    out.update(rank=3 if rank3 else 2, lines=f0, line_multiplicities={str(k): v for k, v in sorted(mult.items())}, regions=R)
    if rank3:
        assert R == 2 * (1 - f0 + f1), "Zaslavsky count disagrees with Euler"
        out["simplicial"] = 2 * f1 == 3 * (1 - f0 + f1)
        out["chi"] = f"(t - 1)(t^2 - {n - 1}t + {b3})"
    # reflection arrangement
    keys = {vkey(a) for a in N}
    refl = True
    for i in range(n):
        for j in range(n):
            if i == j: continue
            g = G[min(i, j), max(i, j)]
            if not g: continue
            r = tuple(x - (g * 2 / nn[i]) * y for x, y in zip(N[j], N[i]))
            if vkey(canon(r)) not in keys: refl = False; break
        if not refl: break
    out["reflection"] = refl
    if reflection_known is not None: assert refl == reflection_known, "reflection flag disagrees"
    # (3) equiangular
    cos2 = {k: v * v / (nn[k[0]] * nn[k[1]]) for k, v in G.items()}
    c0 = cos2[0, 1]
    out["p3_equiangular"] = all(v == c0 for v in cos2.values())
    # (4) perpendicular triples
    adj = [set() for _ in range(n)]
    for (i, j), v in G.items():
        if not v: adj[i].add(j); adj[j].add(i)
    out["perpendicular_pairs"] = sum(len(a) for a in adj) // 2
    out["p4_perp_triples"] = perp_triples(n, adj)
    # (6) rational angles: distinct cos^2 values
    cls = {}
    for k, v in cos2.items(): cls.setdefault(v.key(), (v, []))[1].append(k)
    ang = {}
    for kk, (v, prs) in cls.items():
        c = v * 4 - 2                                   # 2 cos(2 theta), theta the acute angle between the planes
        ang[kk] = rational_angle(c)
    out["angle_classes"] = len(cls)
    out["p6_rational"] = all(a is not None for a in ang.values())
    out["angles_over_pi"] = sorted(str(a) for a in set(ang.values()) if a is not None)[:40]
    out["irrational_angle_classes"] = sum(1 for a in ang.values() if a is None)
    pair_ang = {}
    for kk, (v, prs) in cls.items():
        for pr in prs: pair_ang[pr] = ang[kk]
    # (9) pencils
    ptypes = {}
    allreg = True; reg3 = True
    for c, S in P:
        k = len(S); idx = sorted(S)
        ok = all(cheb_C(k, cos2[a, b] * 4 - 2, F.one) == 2 for a, b in itertools.combinations(idx, 2))
        t = ptypes.setdefault(k, [0, 0]); t[0] += 1; t[1] += ok
        if not ok:
            allreg = False
            if k >= 3: reg3 = False
    out["pencils"] = {str(k): {"count": v[0], "regular": v[1]} for k, v in sorted(ptypes.items())}
    out["p9_all_pencils_regular"] = allreg
    out["p9_pencils_k3_regular"] = reg3
    # (5) equal area: lune test, exact
    lune = True; why = ""
    if rank3:
        for c, S in P:
            idx = sorted(S)
            for i, j, gap in pencil_order(c, idx, N):
                a = pair_ang[min(i, j), max(i, j)]
                if a is None:
                    lune = False; why = "a lune with an irrational angle"; break
                pi = arb.pi()
                hit = [al for al in {a, 1 - a} if abs(gap - pi * al.numerator / al.denominator) < arb(10) ** -60]
                assert len(hit) == 1, "gap not identified"
                al = hit[0]
                if (al * R / 2).denominator != 1:
                    lune = False; why = f"a lune of angle {al} pi holds {al * R / 2} regions' worth"; break
            if not lune: break
    if rank3:
        out["sphericus"] = sphericus(N, P, cos2, {k: v for k, v in pair_ang.items() if v is not None}, R)
    if not lune:
        out["p5_equal_area"] = False; out["p5_how"] = "lune test fails: " + why
    elif refl:
        out["p5_equal_area"] = True; out["p5_how"] = "reflection arrangement: congruent regions"
    else:
        areas = out["sphericus"].pop("_areas")
        out["region_areas_over_pi"] = {str(k): v for k, v in sorted(Counter(areas).items())}
        out["p5_equal_area"] = len(set(areas)) == 1
        out["p5_how"] = "exact areas by face tracing (all angles rational multiples of pi)"
    # (7) factoring and freeness
    if rank3:
        disc = (n - 1) ** 2 - 4 * b3
        s = int(round(disc ** 0.5)) if disc >= 0 else -1
        fac = disc >= 0 and s * s == disc
        out["p7_factors"] = fac
        if fac:
            d1, d2 = (n - 1 - s) // 2, (n - 1 + s) // 2
            out["exponents"] = [1, d1, d2]
            if refl:
                out["p7_free"] = True; out["p7_how"] = "reflection arrangement (Saito; Terao)"
            else:
                ss = None
                for c, S in P:
                    if all(S & T for c2, T in P if T is not S): ss = len(S); break
                if ss is not None:
                    out["p7_free"] = True; out["p7_how"] = f"supersolvable (modular line of {ss} planes; Jambu-Terao)"
                    assert sorted([ss - 1, n - ss]) == [d1, d2], "supersolvable exponents disagree"
                else:
                    ex = multirestriction_d1(F, N, 0, P)
                    out["multirestriction"] = list(ex)
                    out["p7_free"] = sorted(ex) == [d1, d2]
                    out["p7_how"] = "Yoshinaga's criterion (exact multirestriction)"
        else:
            out["p7_free"] = False; out["p7_how"] = "chi does not factor over Z (Terao's factorisation theorem)"
    else:
        out["p7_factors"] = True; out["p7_free"] = True; out["p7_how"] = "rank 2"
    if rank3:
        out["sphericus"].pop("_areas", None)
        out["tacitus_crossings"] = tacitus_cross(N, P)
    out["secs"] = round(time.time() - t0, 2)
    return out


def score(o):
    """how many of the six harmony properties hold (3, 4, 5, 6, 7 = factoring, 9)"""
    ks = ["p3_equiangular", "p4_perp_triples", "p5_equal_area", "p6_rational", "p7_factors", "p9_all_pencils_regular"]
    return sum(1 for k in ks if o.get(k) is True)


# ---------------------------------------------------------------- Tacitus of the crossing points ("crossing the silences")
_TAC = None
def _tac():
    global _TAC
    if _TAC is None:
        import importlib.util, os
        p = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-25-tacitus/scripts/tacitus.py"))
        spec = importlib.util.spec_from_file_location("tacitus", p); _TAC = importlib.util.module_from_spec(spec); spec.loader.exec_module(_TAC)
    return _TAC


def legendre_even(k):
    """P_k(t) for even k as a polynomial in t^2: list of Fractions, low -> high"""
    from fractions import Fraction as Fq
    P = [[Fq(1)], [Fq(0), Fq(1)]]
    for n in range(1, k):
        a = [Fq(0)] + [c * (2 * n + 1) / (n + 1) for c in P[n]]
        b = [c * n / (n + 1) for c in P[n - 1]] + [Fq(0)] * 2
        P.append([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])
    c = P[k]
    return [c[2 * j] for j in range((len(c) + 1) // 2)]


def tacitus_cross(N, P, maxpts=1000):
    """Tacitus silence (study 2026-11-25-tacitus, its code reused: energies, symmetry group, character dimensions) of the
    crossing points (both antipodes), unweighted and weighted by the number of circles through each point. The set is
    centrally symmetric, so every odd degree is silent; even degrees k <= 20 are tested. Float screen as in the Tacitus
    study (silent < 1e-11, nonzero > 1e-8); every float-silent degree that the symmetry group does not force is then
    decided exactly in the field (for even k, P_k(t) is a polynomial in t^2 = (p.q)^2/(|p|^2 |q|^2), which lies in F)."""
    import numpy as np
    T = _tac()
    half = [(c, len(S)) for c, S in P]
    if 2 * len(half) > maxpts: return {"note": f"{2 * len(half)} points: not run (size cap {maxpts})"}
    X = np.array([[float(x.ball().mid()) for x in c] for c, _ in half]); X /= np.linalg.norm(X, axis=1)[:, None]
    PP = np.vstack([X, -X]); out = {}
    for var, w in (("unweighted", np.ones(len(PP))), ("weighted", np.array([m for _, m in half] * 2, float))):
        Rs = T.sym_group(PP, T.labels(w)); dims = T.char_dims(Rs)
        e = T.energies(PP, w, 3)
        res = {"G": len(Rs), "forced_even": [k for k in range(2, 21, 2) if dims[k] == 0], "silent_even": [], "beyond": [], "grey": []}
        for k in range(2, 21, 2):
            if e[k] > T.NONZERO: continue
            if dims[k] == 0:
                assert e[k] < T.ZERO; res["silent_even"].append(k); continue
            # exact decision
            L = legendre_even(k); tot = None
            for i in range(len(half)):
                for j in range(len(half)):
                    p, q = half[i][0], half[j][0]; d = dot(p, q)
                    t2 = d * d / (dot(p, p) * dot(q, q))
                    val = t2 * 0; pw = t2 * 0 + 1
                    for cf in L: val = val + pw * cf; pw = pw * t2
                    ww = 1 if var == "unweighted" else half[i][1] * half[j][1]
                    tot = val * ww if tot is None else tot + val * ww
            if not tot: res["silent_even"].append(k); res["beyond"].append(k)
            else: res["grey"].append(k)
        out[var] = res
    out["silent_beyond_symmetry"] = bool(out["unweighted"]["beyond"] or out["weighted"]["beyond"])
    return out
