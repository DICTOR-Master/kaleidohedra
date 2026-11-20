# Item 3 (#111 Equanimity, open question 2): the fields of the radii of T ∩ D and of the 42- and 50-face dice, from the
# closed forms of Corollary 7.
# Set-up as in #111 and study 2026-11-18-fair-32-die (fair_line2.py): A faces {n.x <= 1}, B faces {m.x <= mu} with unit
# normals; r = 1 (mu_f > 1), R = largest corner distance; the question is the field Q((R/r)^2) = Q(R^2).
#   td  T ∩ D   (16 faces): A = 4 tetrahedron normals (product of signs +1), B = 12 dodecahedron face normals
#   dt  D ∩ RT  (42 faces): A = 12 dodecahedron face normals, B = 30 rhombic triacontahedron normals
#   it  I ∩ RT  (50 faces): A = 20 icosahedron face normals, B = 30 rhombic triacontahedron normals
# Corollary 7: mu_f = b.a + (b.u) t, t = sqrt(tan^2(pi/m) tan^2(theta) - 1), theta = pi/2 - (N - 2) pi/(m N).
# Method: (1) mu_f from the closed form, compared with the 140-digit value of the earlier study (control);
# (2) all corners at 80 digits, the farthest corner and its three planes; (3) R^2 exactly in sympy from those three planes;
# (4) its minimal polynomial by exact algebra (sympy minimal_polynomial), irreducibility, value check at 80 digits;
# (5) the field: degree, number of real roots (exact count), and, if not totally real, "not Galois, so in no field of a
#     regular polygon" (Kronecker-Weber), as in #111 Proposition 5. Controls: O ∩ D (Theorem 4A: (R/r)^2 = 109 - 48 sqrt5)
#     and C ∩ O (Theorem 2: (R/r)^2 = 19 - 8c - 32c^2, c = cos 2pi/7; minimal polynomial of degree 3).
# Usage: radii_fields.py td|dt|it|od|co
import sys, os, json, itertools, time
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, "..", "..")
mode = sys.argv[1]
mp.mp.dps = 80
checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


phi = (1 + sp.sqrt(5)) / 2
X = sp.Symbol("x")


def unit(v):
    n = sp.sqrt(sum(c * c for c in v)); return [sp.nsimplify(c) / n for c in v]


def ico_vertices():  # the 12 five-fold axes (dodecahedron face normals), as in fair_line2.py
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1 * phi, s2), (s2, 0, s1 * phi), (s1 * phi, s2, 0)]
    return V


def dod_vertices():  # the 20 three-fold axes (icosahedron face normals)
    V = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1 / phi, s2 * phi), (s1 / phi, s2 * phi, 0), (s2 * phi, 0, s1 / phi)]
    return V


AX = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
CORN = list(itertools.product((1, -1), repeat=3))
TET = [v for v in CORN if v[0] * v[1] * v[2] == 1]


def rt_normals():
    V = list(AX)
    for s1, s2, s3 in itertools.product((1, -1), repeat=3):
        V += [(s1, s2 * phi, s3 / phi), (s3 / phi, s1, s2 * phi), (s2 * phi, s3 / phi, s1)]
    return V


s5, s3 = sp.sqrt(5), sp.sqrt(3)
LINES = {
    "td": dict(A=TET, B=ico_vertices(), m=3, N=16, ba=sp.sqrt((5 + 2 * s5) / 15), bu=sp.sqrt((5 - s5) / 30)),
    "dt": dict(A=ico_vertices(), B=rt_normals(), m=5, N=42, ba=sp.sqrt((5 + s5) / 10), bu=sp.sqrt((5 + s5) / 10) / 2),
    "it": dict(A=dod_vertices(), B=rt_normals(), m=3, N=50, ba=(s3 + sp.sqrt(15)) / 6, bu=(sp.sqrt(15) - s3) / 12),
    "od": dict(A=CORN, B=ico_vertices(), m=3, N=20, ba=sp.sqrt((5 + 2 * s5) / 15), bu=sp.sqrt((5 - s5) / 30)),
    "co": dict(A=AX, B=CORN, m=4, N=14, ba=1 / s3, bu=1 / s3),
}
L = LINES[mode]
m, N = L["m"], L["N"]
theta = sp.pi / 2 - (N - 2) * sp.pi / (m * N)
# tan^2(theta) through cos(2 theta), exact
c2 = sp.cos(2 * theta)
tan2 = (1 - c2) / (1 + c2)
tanm2 = sp.tan(sp.pi / m) ** 2
t = sp.sqrt(sp.nsimplify(tanm2) * tan2 - 1)
mu = L["ba"] + L["bu"] * t
muv = sp.N(mu, 120)
print(f"{mode}: N = {N}, m = {m}, theta = {theta}, mu_f = {sp.N(mu, 40)}", flush=True)
old = {"td": "td", "dt": "dt", "it": "it", "od": "od", "co": "co"}[mode]
p = os.path.join(ST, "2026-11-18-fair-32-die", "data", f"verts-{old}.json")
if os.path.exists(p):
    ref = mp.mpf(json.load(open(p))["mu"])
    check(f"{mode}: Corollary 7 closed form = the earlier study's 140-digit mu_f (to 1e-100)",
          abs(mp.mpf(str(muv)) - ref) < mp.mpf(10) ** -100, f"diff {mp.nstr(abs(mp.mpf(str(muv)) - ref), 3)}")
else:
    check(f"{mode}: (no earlier value file; Table 1 value to 10 digits)", True)

# planes with exact unit normals
An = [unit(v) for v in L["A"]]; Bn = [unit(v) for v in L["B"]]
planes = [(n, sp.Integer(1)) for n in An] + [(n, mu) for n in Bn]
Pn = [([mp.mpf(str(sp.N(c, 90))) for c in n], mp.mpf(str(sp.N(d, 90)))) for n, d in planes]
# vertices: all triples, feasible
import numpy as np
Pf = np.array([[float(c) for c in nn] for nn, dd in Pn]); bf = np.array([float(dd) for nn, dd in Pn])


def cramer(M, b):
    def det(A):
        return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
                + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
    D = det(M)
    out = []
    for k in range(3):
        A = [list(r) for r in M]
        for r in range(3): A[r][k] = b[r]
        out.append(det(A) / D)
    return out


verts = []
for tri in itertools.combinations(range(len(Pn)), 3):
    A3 = Pf[list(tri)]
    if abs(np.linalg.det(A3)) < 1e-9: continue
    xf = np.linalg.solve(A3, bf[list(tri)])
    if not np.all(Pf @ xf <= bf + 1e-9): continue
    x = cramer([Pn[k][0] for k in tri], [Pn[k][1] for k in tri])
    if all(sum(nn[i] * x[i] for i in range(3)) <= dd + mp.mpf(10) ** -50 for nn, dd in Pn):
        verts.append((sum(x[i] ** 2 for i in range(3)), tri, x))
R2max = max(v[0] for v in verts)
far = [v for v in verts if abs(v[0] - R2max) < mp.mpf(10) ** -50]
kinds = sorted(set(tuple(sorted("A" if k < len(An) else "B" for k in v[1])) for v in far))
print(f"  {len(verts)} corner-plane triples feasible; R^2 = {mp.nstr(R2max, 40)}; farthest corners {len(far)}, plane kinds {kinds}",
      flush=True)
rr = 1 / mp.sqrt(R2max)
print(f"  r/R = {mp.nstr(rr, 12)}", flush=True)
TABLE = {"td": "0.7494098635", "dt": "0.9274314879", "it": "0.8375974356", "od": "0.7741159964", "co": "0.7974733889"}
check(f"{mode}: r/R = Table 1 of #111 (10 digits)", mp.nstr(rr, 10) == TABLE[mode][:12] or abs(rr - mp.mpf(TABLE[mode])) < 1e-10,
      mp.nstr(rr, 12))
# exact R^2 from one farthest corner's three planes (r = 1 since mu_f > 1)
check(f"{mode}: mu_f > 1, so r = 1", muv > 1)
tri = far[0][1]
Mx = sp.Matrix([planes[k][0] for k in tri]); bx = sp.Matrix([planes[k][1] for k in tri])
x = Mx.LUsolve(bx)
if len(sys.argv) > 2 and sys.argv[2] == 'scan':
    print('farthest triple', tri, kinds); sys.exit(0)
R2 = sp.expand(sum(sp.radsimp(xx) ** 2 for xx in x))
check(f"{mode}: exact R^2 expression agrees with the corner search to 1e-70", abs(mp.mpf(str(sp.N(R2, 90))) - R2max) < mp.mpf(10) ** -70)
t0 = time.time()
mpoly = sp.minimal_polynomial(R2, X, polys=True)
print(f"  minimal polynomial of R^2 found in {time.time() - t0:.1f} s, degree {mpoly.degree()}", flush=True)
check(f"{mode}: minimal polynomial irreducible over Q", mpoly.is_irreducible)
val = mpoly.eval(sp.Float(str(sp.N(R2, 100)), 100))
check(f"{mode}: R^2 is a root (80 digits)", abs(sp.N(mpoly.as_expr().subs(X, sp.N(R2, 110)), 50)) < sp.Float("1e-60"))
nreal = sp.Poly(mpoly, X).count_roots()
deg = mpoly.degree()
coeffs = mpoly.all_coeffs()
print(f"  {mode}: degree {deg}, real roots {nreal} of {deg}", flush=True)
print(f"  polynomial: {mpoly.as_expr()}", flush=True)
disc = sp.factorint(sp.discriminant(mpoly)) if deg <= 40 else None
if disc is not None: print(f"  discriminant primes: {sorted(disc)}", flush=True)
res = dict(mode=mode, N=N, m=m, theta=str(theta), mu=str(sp.N(mu, 60)), R2=str(sp.N(R2, 60)), r_over_R=mp.nstr(rr, 30),
           farthest_planes=kinds, R2_exact=str(R2), minpoly=str(mpoly.as_expr()), degree=deg, real_roots=int(nreal),
           totally_real=(nreal == deg), discriminant_primes=sorted(disc) if disc else None)
if mode == "od":
    check("control O ∩ D: (R/r)^2 = 109 - 48 sqrt5 (Theorem 4A)", sp.simplify(mpoly.as_expr() - (X ** 2 - 218 * X + 361)) == 0
          or sp.Poly(X ** 2 - 218 * X + 109 ** 2 - 48 ** 2 * 5, X) == mpoly, str(mpoly.as_expr()))
if mode == "co":
    c7 = sp.cos(2 * sp.pi / 7)
    check("control C ∩ O: (R/r)^2 = 19 - 8c - 32c^2, minimal polynomial of degree 3 (Theorem 2)",
          deg == 3 and abs(sp.N(R2 - (19 - 8 * c7 - 32 * c7 ** 2), 60)) < 1e-50, str(mpoly.as_expr()))
if nreal < deg:
    print(f"  {mode}: (R/r)^2 has non-real conjugates: its field is not Galois over Q, so it lies in no cyclotomic field and in "
          f"no field of a regular polygon (Kronecker-Weber)", flush=True)
json.dump(res, open(os.path.join(HERE, "..", "data", f"radii-{mode}.json"), "w"), indent=1)
with open(os.path.join(HERE, "..", "data", f"radii-{mode}-checks.txt"), "w") as fh:
    for s_, n, det in checks: fh.write(f"{s_} {n} {det}\n")
nf = sum(1 for c in checks if c[0] == "FAIL")
print(f"{len(checks) - nf}/{len(checks)} PASS")
print("FINAL ok" if checks and nf == 0 else f"FINAL FAIL: {nf} of {len(checks)} checks failed")
