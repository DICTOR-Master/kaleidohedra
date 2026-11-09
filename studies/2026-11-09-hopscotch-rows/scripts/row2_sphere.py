"""Row 2 (sphere row): #43's containment constants from the bilinear form of the antipol (S, S^v), and #81's core turn.
S = {n_i.x <= h_i} (unit normals), P(S) = conv(h_i n_i), S^v = {n_i.x <= 1/h_i} = polar(P(S)).  Bipolar theorem:
  t_min(S) = max_{x in S} gauge_P(x) = max_{x in S, y in S^v} x.y            (B)
Parts: (1) (B) against the direct gauge computation, Theorem 1's chain from (B) [lower bound: y parallel to x; upper: Cauchy-Schwarz
with R(S^v) = 1/r(P) <= R/r^2], Lemma A as (B) maximised over x first, Lemma G as the pairing (h_i n_i).(n_i/h_i) = 1 (float, random
polytopes); (2) Platonic constants 9, 3, 3, 15-6sqrt5, 15-6sqrt5 exactly (S^v = S/h^2, max at x = y); (3) orbit moments, exact symbolic,
for T, T_h, O, I and the three polynomial certificates (2-design -> 9, 3-design -> 3, 5-design -> only 5/3 > 15-6sqrt5);
(4) the cube-octahedron line P_mu: P_mu^v = P_{3/mu}, walls as determinants linear in mu (1, 3/2, 2, 3), the turn's fixed point sqrt3
is the self-antipol (every face tangent to the unit sphere), t_min there = R^2 = (R/r)^2 = 5 - 2sqrt3, and the closed form
t_min = min(mu, 3/mu, 5 - mu - 3/mu) on 1 < mu < 3 (exact corner enumeration at 46 rational mu)."""
import itertools, random
from fractions import Fraction as Fr
import numpy as np, sympy as sp
from scipy.spatial import ConvexHull, HalfspaceIntersection
checks = {}

# ---------- (1) float: (B), Theorem 1, Lemma A, Lemma G on random polytopes
rng = np.random.default_rng(43)
def facets(points):
    H = ConvexHull(points); out = []
    for eq in H.equations:                      # a.x + b <= 0, |a| = 1
        n, h = eq[:3], -eq[3]
        if not any(np.allclose(n, m) for m, _ in out): out.append((n, h))
    return out
ok_B = ok_T1 = ok_A = ok_G = ok_R = True; worst = 0
for trial in range(300):
    pts = rng.normal(size=(rng.integers(6, 30), 3)) * rng.uniform(0.3, 2, size=3)
    pts = pts - pts.mean(axis=0)
    try: F = facets(pts)
    except Exception: continue
    if min(h for _, h in F) <= 1e-3: continue
    V = ConvexHull(pts).points[ConvexHull(pts).vertices]
    N = np.array([n for n, _ in F]); h = np.array([h for _, h in F])
    Pp = N * h[:, None]                                         # foot points
    PF = facets(Pp)                                             # facets of P(S)
    gauge_P = lambda x: max(n @ x / hh for n, hh in PF)
    t_direct = max(gauge_P(v) for v in V)
    Sv = HalfspaceIntersection(np.hstack([N, -1 / h[:, None]]), np.zeros(3)).intersections   # S^v corners
    t_bil = max(float(x @ y) for x in V for y in Sv)
    ok_B &= abs(t_direct - t_bil) < 1e-9 * max(1, t_bil); worst = max(worst, abs(t_direct - t_bil))
    R = max(np.linalg.norm(V, axis=1)); r = h.min(); rP = min(hh for _, hh in PF); RSv = max(np.linalg.norm(Sv, axis=1))
    hP = lambda u: max(Pp @ u)
    lower = max(v @ v / hP(v) for v in V)
    ok_T1 &= lower <= t_bil + 1e-9 and t_bil <= R / rP + 1e-9 and R / rP <= (R / r)**2 + 1e-9
    ok_R &= abs(RSv - 1 / rP) < 1e-9 * RSv and RSv <= R / r**2 + 1e-9
    # Lemma A: max over u of h_S(u)/h_P(u); the max sits at u = a corner of S^v (the boundary point y = u/gauge_{S^v}(u))
    hS = lambda u: max(V @ u)
    ok_A &= abs(max(hS(y) / hP(y) for y in Sv) - t_bil) < 1e-9 * t_bil
    ok_G &= all(hP(n) >= hh - 1e-12 for n, hh in zip(N, h)) and all(abs((hh * n) @ (n / hh) - 1) < 1e-12 for n, hh in zip(N, h))
checks['(B) t_min = max x.y over S x S^v (300 random polytopes)'] = ok_B
checks['Theorem 1 chain from (B) holds'] = ok_T1
checks['R(S^v) = 1/r(P(S)) <= R/r^2'] = ok_R
checks['Lemma A = (B) maximised over x first'] = ok_A
checks['Lemma G: h_P(n_i) >= h_i; pairing (h_i n_i).(n_i/h_i) = 1'] = ok_G
print(f'(1) largest |gauge - bilinear| = {worst:.2e}')

# ---------- (2) Platonic constants, exact
s5, phi = sp.sqrt(5), (1 + sp.sqrt(5)) / 2
def ps(v, even=False):
    out = set()
    for p in itertools.permutations(range(3)):
        if even and sp.Permutation(list(p)).is_odd: continue
        for sg in itertools.product([1, -1], repeat=3):
            out.add(tuple(sg[i] * v[p[i]] for i in range(3)))
    return [sp.Matrix(t) for t in out]
def cyc(v):
    out = set()
    for k in range(3):
        w = v[k:] + v[:k]
        for sg in itertools.product([1, -1], repeat=3): out.add(tuple(sg[i] * w[i] for i in range(3)))
    return [sp.Matrix(t) for t in out]
tet = [sp.Matrix(t) for t in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
cube = ps((1, 1, 1)); octa = ps((1, 0, 0)); ico = cyc((0, 1, phi)); dod = ps((1, 1, 1)) + cyc((0, phi, 1 / phi))   # dual orientation to ico = cyc((0, 1, phi))
solids = {'tetrahedron': (tet, [-v for v in tet], 9), 'cube': (cube, octa, 3), 'octahedron': (octa, cube, 3),
          'dodecahedron': (dod, ico, 15 - 6 * s5), 'icosahedron': (ico, dod, 15 - 6 * s5)}
for name, (Vs, normals, const) in solids.items():
    R2 = sp.nsimplify(sp.simplify(max((v.T * v)[0] for v in Vs)))
    hs = [sp.simplify(max((v.T * n)[0] for v in Vs) / sp.sqrt((n.T * n)[0])) for n in normals]
    hset = set(sp.nsimplify(sp.radsimp(x)) for x in hs)
    h0 = hs[0]
    Svc = [v / h0**2 for v in Vs]                     # all h equal -> S^v = S / h^2
    tmin = sp.simplify(max(((x.T * y)[0] for x in Vs for y in Svc), key=lambda e: float(e)))
    ok = len(hset) == 1 and sp.simplify(tmin - const) == 0 and sp.simplify(R2 / h0**2 - const) == 0
    checks[f'{name}: one face distance, t_min = (R/r)^2 = {const}'] = ok
    print(f'(2) {name:13s} R^2 = {R2}, r^2 = {sp.nsimplify(sp.radsimp(h0**2))}, t_min = {sp.radsimp(tmin)}')

# ---------- (3) orbit moments, exact symbolic
u = sp.Matrix(sp.symbols('u1 u2 u3', real=True)); w = sp.Matrix(sp.symbols('w1 w2 w3', real=True))
uu, ww = (u.T * u)[0], (w.T * w)[0]
def perm_mats(vs):
    return [sp.Matrix(3, 3, lambda i, j: 1 if p[i] == j else 0) for p in vs]
D = lambda s: sp.diag(*s)
signs = list(itertools.product([1, -1], repeat=3))
P3 = list(itertools.permutations(range(3))); Pcyc = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
O_grp = [D(s) * Pm for Pm in perm_mats(P3) for s in signs if (D(s) * Pm).det() == 1]
T_grp = [D(s) * Pm for Pm in perm_mats(Pcyc) for s in signs if s[0] * s[1] * s[2] == 1]
Th_grp = [D(s) * Pm for Pm in perm_mats(Pcyc) for s in signs]
# I: generated by the 5-fold rotation about (0,1,phi) and the 3-fold cyclic permutation (exact in Q(sqrt5))
g3 = perm_mats([(1, 2, 0)])[0]
g2 = D((1, -1, -1))
cv = 1 / (2 * phi); vax = sp.Matrix([0, 1, phi])          # Rodrigues about (0,1,phi): sin72 * k = vax/2 exactly
cross = sp.Matrix([[0, -vax[2], vax[1]], [vax[2], 0, -vax[0]], [-vax[1], vax[0], 0]])
h5 = (cv * sp.eye(3) + cross / 2 + (1 - cv) / (1 + phi**2) * vax * vax.T).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))
gens = [g3, g2, sp.simplify(h5)]
I_grp = [sp.eye(3)]; frontier = [sp.eye(3)]
key = lambda M: tuple(sp.nsimplify(sp.radsimp(e)) for e in M)
seen = {key(sp.eye(3))}
while frontier:
    nxt = []
    for A in frontier:
        for g in gens:
            B = (g * A).applyfunc(lambda e: sp.radsimp(sp.expand(e)))
            k = key(B)
            if k not in seen: seen.add(k); I_grp.append(B); nxt.append(B)
    frontier = nxt
    if len(I_grp) > 60: break
checks['I generated exactly: 60 rotations, orthogonal'] = len(I_grp) == 60 and all(sp.simplify(M.T * M - sp.eye(3)) == sp.zeros(3) and sp.simplify(M.det() - 1) == 0 for M in I_grp)
uniform = {1: 0, 2: sp.Rational(1, 3), 3: 0, 4: sp.Rational(1, 5), 5: 0}
VARS = list(u) + list(w)
def design_strength(G, kmax):
    strength = 0
    lin = [sp.Poly(((M * u).T * w)[0], *VARS, extension=sp.sqrt(5)) for M in G]
    for k in range(1, kmax + 1):
        s = sum((L**k for L in lin), sp.Poly(0, *VARS, extension=sp.sqrt(5)))
        e = {2: sp.Rational(1, 3), 4: sp.Rational(1, 5), 6: sp.Rational(1, 7)}.get(k, 0)
        target = sp.Poly(sp.expand(len(G) * e * (uu * ww)**(k // 2)) if e else 0, *VARS, extension=sp.sqrt(5))
        if (s - target).is_zero: strength = k
        else: break
    return strength
strengths = {name: design_strength(G, km) for name, G, km in [('T', T_grp, 4), ('T_h', Th_grp, 4), ('O', O_grp, 4), ('I', I_grp, 6)]}
print('(3) design strengths (generic orbits):', strengths)
checks['design strengths T 2, T_h 3, O 3, I 5'] = strengths == {'T': 2, 'T_h': 3, 'O': 3, 'I': 5}
m, t = sp.symbols('m t', positive=True)
def mean_of(poly):     # mean of poly(t) over an orbit of a design strong enough (unit u, w)
    pp = sp.Poly(sp.expand(poly), t); return sum(cf * uniform[k] if k else cf for (k,), cf in pp.terms())
c2 = sp.simplify(mean_of((m - t) * (1 + t)))
c3 = sp.simplify(mean_of((t - m) * (t + 1 / (3 * m))**2))
c5 = sp.simplify(mean_of((t - m) * (t + m)**2 * t**2))
print('(3) certificates: 2-design mean', c2, '| 3-design mean', sp.factor(c3), '| 5-design mean', sp.factor(c5))
checks['2-design: mean (m-t)(1+t) = m - 1/3 -> m >= 1/3 -> constant 9'] = sp.simplify(c2 - (m - sp.Rational(1, 3))) == 0
checks['3-design: mean = (1-3m^2)/(9m) -> m >= 1/sqrt3 -> constant 3'] = sp.simplify(c3 - (1 - 3 * m**2) / (9 * m)) == 0
checks['5-design: mean = m/5 - m^3/3 -> m >= sqrt(3/5) -> only 5/3'] = sp.simplify(c5 - (m / 5 - m**3 / 3)) == 0
checks['5/3 > 15 - 6 sqrt5 (moments alone miss the icosahedral constant)'] = sp.Rational(5, 3) - (15 - 6 * s5) > 0
ci2 = (5 + 2 * s5) / 15
checks['icosahedral c^2 = (5+2sqrt5)/15, 1/c^2 = 15-6sqrt5'] = sp.simplify(1 / ci2 - (15 - 6 * s5)) == 0

# ---------- (4) the cube-octahedron line
mu = sp.Symbol('mu', positive=True)
fam = [(sp.Matrix(n), d) for n, d in [((1, 0, 0), 1)] ]
cube_n = [sp.Matrix(v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
oct_n = [sp.Matrix(v) for v in itertools.product([1, -1], repeat=3)]
Pmu = [(n, 1) for n in cube_n] + [(n, mu) for n in oct_n]
Pdual = [(n, sp.simplify((n.T * n)[0] / d)) for n, d in Pmu]      # inverted distances |N|^2/d
checks['P_mu^v = P_{3/mu} (same planes, d -> |N|^2/d)'] = all(sp.simplify(d2 - (1 if (n.T * n)[0] == 1 else 3 / mu)) == 0 for n, d2 in Pdual)
fixed = sp.solve(sp.Eq(mu, 3 / mu), mu)
checks['turn mu -> 3/mu has fixed point sqrt3; there every face is at unit distance (tangent to the sphere)'] = fixed == [sp.sqrt(3)] and \
    all(sp.simplify(sp.sympify(d).subs(mu, sp.sqrt(3)) / sp.sqrt((n.T * n)[0]) - 1) == 0 for n, d in Pmu)
def conc(planes):      # 4 planes concurrent <=> det [N | -d] = 0
    return sp.factor(sp.Matrix([[*n, -d] for n, d in planes]).det())
w2 = conc([(sp.Matrix([1, 0, 0]), 1), (sp.Matrix([0, 1, 0]), 1), (sp.Matrix([1, 1, 1]), mu), (sp.Matrix([1, 1, -1]), mu)])
w1 = conc([(sp.Matrix([1, 0, 0]), 1), (sp.Matrix([1, 1, 1]), mu), (sp.Matrix([1, 1, -1]), mu), (sp.Matrix([1, -1, 1]), mu)])
print('(4) wall determinants: square faces vanish', w2, '| octahedron corner reaches the cube plane', w1)
checks['wall det linear in mu, root 2 (cuboctahedron); its turn image 3/2 is the same event on S^v'] = sp.solve(w2, mu) == [2] and sp.degree(w2, mu) == 1
checks['wall det linear in mu, root 1 (octahedron end); turn image 3 (cube end)'] = sp.solve(w1, mu) == [1] and sp.degree(w1, mu) == 1
def corners_exact(planes):
    out = set()
    for A, B, C in itertools.combinations(planes, 3):
        M = sp.Matrix([list(A[0]), list(B[0]), list(C[0])])
        if M.det() == 0: continue
        X = M.LUsolve(sp.Matrix([A[1], B[1], C[1]]))
        if all((n.T * X)[0] <= d for n, d in planes): out.add(tuple(X))
    return [sp.Matrix(p) for p in out]
def tmin_mu(mv):
    S = corners_exact([(n, d.subs(mu, mv) if hasattr(d, 'subs') else d) for n, d in Pmu])
    Sv = corners_exact([(n, d.subs(mu, mv) if hasattr(d, 'subs') else d) for n, d in Pdual])
    return max((x.T * y)[0] for x in S for y in Sv)
mus = [sp.Rational(k, 16) for k in range(17, 48)] + [sp.Rational(k, 7) for k in range(8, 21) if k % 7] + [sp.Rational(3, 2), sp.Integer(2)]
mus = sorted(set(mus))
okc = True
for mv in mus:
    tv = tmin_mu(mv); cf = min(mv, 3 / mv, 5 - mv - 3 / mv)
    okc &= sp.simplify(tv - cf) == 0
checks[f't_min(P_mu) = min(mu, 3/mu, 5 - mu - 3/mu) at {len(mus)} rational mu (exact)'] = okc
tq = tmin_mu(sp.sqrt(3)); R2q = max((x.T * x)[0] for x in corners_exact([(n, d.subs(mu, sp.sqrt(3)) if hasattr(d, 'subs') else d) for n, d in Pmu]))
print('(4) at the turn mu = sqrt3: t_min =', sp.radsimp(tq), ' R^2 =', sp.radsimp(R2q))
checks['at the turn: t_min = R^2 = (R/r)^2 = 5 - 2sqrt3 (self-antipol, r = 1)'] = sp.simplify(tq - (5 - 2 * sp.sqrt(3))) == 0 and sp.simplify(R2q - tq) == 0
s_ = mu + 3 / mu
checks['5 - mu - 3/mu <= 5 - 2sqrt3, equality only at sqrt3 (AM-GM in the turn-invariant s = mu + 3/mu)'] = sp.simplify((5 - 2 * sp.sqrt(3)) - (5 - s_) - (mu - sp.sqrt(3))**2 / mu) == 0

for k, ok in checks.items(): print(('ok   ' if ok else 'FAIL ') + k)
bad = [k for k, ok in checks.items() if not ok]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
