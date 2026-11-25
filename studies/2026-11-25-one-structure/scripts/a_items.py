"""Part A checks (one-structure study, 25 Nov 2026).
A2: (a) the tetrahedron and the octahedron share their Resonus (4 planes) but differ in degree 3 (exact, rational);
    (b) the family P_t = cube [-1, 1]^3 cut by the octahedron |x| + |y| + |z| <= t (1 < t < 3): solid-angle weights, the unique
        t* where the square faces subtend 4 pi / 15 each (certified interval, ball arithmetic; uniqueness by the monotone-cell
        lemma, Lemma 9 of study 2026-11-25-stellation-cycle), and the exact silent degrees k <= 20 of P_t* (weights 8 : 9
        per face, exact rational zonal sums) against the truncated octahedron with unit weights.
A3: the factor-3 bridge, exact in Q(sqrt5) (q5.py of the stellation-cycle study): I0 inside the regular octahedron
    |x| + |y| + |z| <= phi^2 (8 faces shared, 12 corners on its edges in golden ratio), its corners on the midsphere of I1,
    the five octahedra and the 20 three-fold planes, the polarity identity R(D0) r(I0) = m^2, the norm of 3, and the 41 dice
    of data/factor3.json of that study (every hit a two-fold orbit over a three-fold orbit with r^2 = 3 / phi^2).
Writes data/a-items.json."""
import os, sys, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
SC = os.path.normpath(os.path.join(HERE, "../../2026-11-25-stellation-cycle"))
sys.path.insert(0, os.path.join(SC, "scripts"))
from q5 import Q, dot, cross, vsub, vadd, vsc, phipow
from flint import arb, ctx
ctx.prec = 200
OUT = {}
PHI = Q(Fr(1, 2), Fr(1, 2))


# ---------------------------------------------------------------- A2 (a)
T = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
Oct = T + [tuple(-c for c in v) for v in T]
xyz = lambda v: Fr(v[0] * v[1] * v[2])
OUT["A2a"] = {"tetrahedron_sum_xyz": str(sum(xyz(v) for v in T)), "octahedron_sum_xyz": str(sum(xyz(v) for v in Oct)),
              "same_resonus_axes": sorted(set(tuple(abs(c) for c in v) for v in T)) == sorted(set(tuple(abs(c) for c in v) for v in Oct))}
assert OUT["A2a"]["tetrahedron_sum_xyz"] == "4" and OUT["A2a"]["octahedron_sum_xyz"] == "0"
print("A2a", OUT["A2a"], flush=True)


# ---------------------------------------------------------------- A2 (b)
def solid(poly):
    """solid angle at the origin of a convex planar polygon (Van Oosterom and Strackee 1983), ball arithmetic"""
    a = poly[0]; s = arb(0)
    nrm = lambda v: (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt()
    d = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
    for b, c in zip(poly[1:-1], poly[2:]):
        trip = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
        A, B, C = nrm(a), nrm(b), nrm(c)
        den = A * B * C + d(a, b) * C + d(a, c) * B + d(b, c) * A
        s += 2 * arb.atan2(abs(trip), den)
    return s


def square_face(t):
    o = arb(1); z = arb(0)
    if t <= 2:
        a = t - 1
        return [(o, a, z), (o, z, a), (o, -a, z), (o, z, -a)]
    b = t - 2
    return [(o, o, b), (o, b, o), (o, -b, o), (o, -o, b), (o, -o, -b), (o, -b, -o), (o, b, -o), (o, o, -b)]


def omega_s(t): return solid(square_face(arb(t)))


target = 4 * arb.pi() / 15
lo, hi = Fr(1), Fr(3)
for _ in range(60):
    mid = (lo + hi) / 2
    v = omega_s(arb(mid.numerator) / mid.denominator) - target
    if v < 0: lo = mid
    elif v > 0: hi = mid
    else: break
flo = omega_s(arb(lo.numerator) / lo.denominator) - target
fhi = omega_s(arb(hi.numerator) / hi.denominator) - target
assert flo < 0 and fhi > 0, "sign change not certified"
OUT["A2b"] = {"t_star_interval": [str(lo), str(hi)], "t_star_approx": float(lo), "Omega_square_target": "4pi/15", "Omega_octahedron_face (hexagon here)": "3pi/10",
              "sign_at_lo": str(flo), "sign_at_hi": str(fhi), "square_face_shape": "4-gon (1 < t <= 2)" if hi <= 2 else "8-gon (2 < t < 3)"}
# exact silent degrees: 6 square normals (weight 8), 8 diagonal normals (weight 9), and the truncated octahedron (unit weights)
N6 = [tuple(s if i == j else 0 for j in range(3)) for i in range(3) for s in (1, -1)]
N8 = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]


def even_legendre(k, x2):
    # P_k(x) for even k as a polynomial in x^2, via exact coefficients
    co = legendre_coeffs(k)
    return sum(c * x2 ** (i // 2) for i, c in enumerate(co) if c)


def legendre_coeffs(k):
    from math import comb
    # P_k(x) = 2^-k sum_j (-1)^j C(k,j) C(2k-2j,k) x^(k-2j)
    co = [Fr(0)] * (k + 1)
    for j in range(k // 2 + 1):
        co[k - 2 * j] += Fr((-1) ** j * comb(k, j) * comb(2 * k - 2 * j, k), 2 ** k)
    return co


def silent(weights):
    out = []
    for k in range(1, 21):
        if k % 2 == 1:
            # centrally symmetric weighted set: every odd degree is silent (each term cancels with the opposite normal)
            out.append(k); continue
        tot = Fr(0)
        for (n, w), (m, u) in itertools.product(weights, repeat=2):
            dd = sum(a * b for a, b in zip(n, m)); nn = sum(a * a for a in n) * sum(a * a for a in m)
            tot += w * u * even_legendre(k, Fr(dd * dd, nn))
        if tot == 0: out.append(k)
    return out


Wstar = [(n, Fr(8)) for n in N6] + [(n, Fr(9)) for n in N8]
Wto = [(n, Fr(1)) for n in N6] + [(n, Fr(1)) for n in N8]
OUT["A2b"]["silent_degrees_P_tstar"] = silent(Wstar)
OUT["A2b"]["silent_degrees_TO_unit_weights"] = silent(Wto)
OUT["A2b"]["Oh_forced_degrees"] = "odd and 2 (Tacitus study)"
assert 4 in OUT["A2b"]["silent_degrees_P_tstar"] and 4 not in OUT["A2b"]["silent_degrees_TO_unit_weights"]
print("A2b", OUT["A2b"], flush=True)

# ---------------------------------------------------------------- A3
P2 = PHI * PHI
I0 = []
for a, b in itertools.product((PHI, -PHI), (Q(1), -Q(1))):
    base = (Q(0), a, b)
    for r in range(3): I0.append(tuple(base[(k - r) % 3] for k in range(3)))
cube = [(Q(a), Q(b), Q(c)) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
D0 = cube[:]
for s1 in (1, -1):
    for s2 in (1, -1):
        base = (Q(0), (PHI - 1) * s1, PHI * s2)
        for r in range(3): D0.append(tuple(base[(k - r) % 3] for k in range(3)))
assert len(I0) == 12 and len(D0) == 20
r2 = lambda v: dot(v, v)
A3 = {}
A3["D0_corners_squared_radius"] = sorted({repr(r2(v)) for v in D0})                       # all 3
A3["phi2_plus_phi-2"] = repr(P2 + Q(1) / P2)                                                # 3 (Lucas L2)
l1 = lambda v: sum((x if x.sign() >= 0 else -x for x in v), Q(0))
A3["I0_on_octahedron_boundary"] = all(l1(v) == P2 for v in I0)
A3["I0_corners_on_octahedron_edges"] = all(sum(1 for x in v if x == 0) == 1 for v in I0)
# golden division of the octahedron edge (0, phi^2, 0)-(0, 0, phi^2) by the corner (0, phi, 1)
s = Q(1) / P2
A3["edge_division_ratio"] = repr((Q(1) - s) / s)                                             # phi
octa_corner = (P2, Q(0), Q(0))
A3["octahedron_circumradius_equals_midradius_of_I1"] = r2(octa_corner) == phipow(4)
mid_I0 = r2(vsc(Q(Fr(1, 2)), vadd(I0[0], next(w for w in I0 if r2(vsub(I0[0], w)) == Q(4)))))
A3["midradius2_I0"] = repr(mid_I0)                                                            # phi^2
in2_I0 = P2 * P2 / Q(3)
A3["inradius2_I0 (plane x+y+z = phi^2)"] = repr(in2_I0)
A3["r2 = mid2/in2"] = repr(mid_I0 / in2_I0)                                                   # 3/phi^2
A3["R(O)^2/in(O)^2"] = repr(r2(octa_corner) / in2_I0)                                         # 3
A3["mid(I0)^2/R(O)^2"] = repr(mid_I0 / r2(octa_corner))                                       # 1/phi^2
assert mid_I0 / in2_I0 == (r2(octa_corner) / in2_I0) * (mid_I0 / r2(octa_corner))
assert r2(octa_corner) / in2_I0 == Q(3) and mid_I0 / r2(octa_corner) == phipow(-2)
# polarity: R(D0) r(I0) = m^2  <=>  R(D0)^2 r(I0)^2 = m^4
A3["polarity R(D0)^2 in(I0)^2 = m^4"] = (Q(3) * in2_I0) == mid_I0 * mid_I0
A3["R(D0)/in(I0) squared = (m/in)^4 ? R(D0)^2/in2 = 3 * 3/phi^4"] = repr(Q(3) / in2_I0)
A3["gap_d_octahedron_vs_I0_planes"] = repr(Q(3) / P2)                                         # 3/phi^2 = r^2
A3["norm_3_over_phi2"] = str((Q(3) / P2).norm())                                              # 9
A3["3_inert_mod_3"] = all((x * x - x - 1) % 3 != 0 for x in range(3))
# five cubes in D0: corner i with three corners at squared distance 4 that are pairwise at squared distance 8 span a cube;
# kept when all 8 of its corners are corners of D0
adj4 = {i: [j for j in range(20) if j != i and r2(vsub(D0[i], D0[j])) == Q(4)] for i in range(20)}
found = set()
for i in range(20):
    for a, b, c in itertools.combinations(adj4[i], 3):
        if r2(vsub(D0[a], D0[b])) == Q(8) and r2(vsub(D0[a], D0[c])) == Q(8) and r2(vsub(D0[b], D0[c])) == Q(8):
            # the cube spanned: corners i + e_a + e_b combinations
            e = [vsub(D0[x], D0[i]) for x in (a, b, c)]
            pts = []
            for m in itertools.product((0, 1), repeat=3):
                p = D0[i]
                for k, mm in enumerate(m):
                    if mm: p = vadd(p, e[k])
                pts.append(p)
            ks = frozenset(tuple(x.key() for x in p) for p in pts)
            if all(any(tuple(x.key() for x in p) == tuple(y.key() for y in q) for q in D0) for p in pts): found.add(ks)
A3["cubes_in_D0"] = len(found)
assert len(found) == 5
# each three-fold axis (D0 corner) is a body diagonal of exactly two of the five cubes; the octahedron of cube j has its faces on
# the I0 planes through cube j's 8 corners (n.x = phi^2, n a corner of cube j) and its corners on the 2-fold axes
cnt = {tuple(x.key() for x in v): 0 for v in D0}
for ks in found:
    for k in ks: cnt[k] += 1
A3["cubes_per_D0_corner"] = sorted(set(cnt.values()))
# planes n.x = phi^2 for n in D0 are exactly the 20 face planes of I0 (each holds 3 corners of I0)
A3["I0_face_planes_are_n.x=phi^2_for_n_in_D0"] = all(sum(1 for v in I0 if dot(n, v) == P2) == 3 for n in D0)
# S and B of one die are never body diagonal + face normal of one cube: cos^2 between a 3-fold face normal of I_k and the
# 2-fold normal of the neighbouring RT_k rhombus = (in/mid)^2 = phi^2/3; a cube's diagonal and face normal: 1/3
A3["cos2_S_B_neighbours"] = repr(in2_I0 / mid_I0)                                             # phi^2/3
A3["cos2_cube_diagonal_face"] = "1/3"
assert in2_I0 / mid_I0 != Q(Fr(1, 3))
# the 41 dice
f3 = json.load(open(os.path.join(SC, "data/factor3.json")))
istwo = lambda lab: lab.startswith("C6") or lab.startswith("RT24")
isthree = lambda lab: lab.startswith("O8") or lab.startswith("I12")
kinds = {}
for h in f3["hits"]:
    for X_, Y_, r, k in h["hits"]:
        if istwo(X_) and isthree(Y_): kind = ("two-fold over three-fold", r == "3" and k == -2)
        elif isthree(X_) and istwo(Y_): kind = ("three-fold over two-fold", r == "1/3" and k == 2)
        else: kind = ("other", False)
        kinds[kind] = kinds.get(kind, 0) + 1
A3["dice"] = len(f3["hits"])
A3["hit_kinds (ratio squared = 3/phi^2 or its inverse)"] = {f"{a}: {c}": v for (a, c), v in kinds.items()}
assert A3["dice"] == 41 and all(c and a != "other" for (a, c) in kinds)
OUT["A3"] = A3
print("A3", json.dumps(A3, indent=1), flush=True)
json.dump(OUT, open(os.path.join(STUDY, "data/a-items.json"), "w"), indent=1, default=str)
print("FINAL ok a_items", flush=True)
