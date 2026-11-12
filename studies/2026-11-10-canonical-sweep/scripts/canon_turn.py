"""Aim 2, chunk 3 (12 Nov 2026): the turn mu -> mu_lo*mu_hi/mu in canonical-form language, and is its fixed point special there?
Sweeps S(mu) = P ∩ mu·P* for a polar pair: (A) cube [-1,1]^3 / octahedron (turn mu -> 3/mu, fixed point sqrt3);
(B) icosahedron (0,±1,±phi) cyclic / its polar dodecahedron.  P = {a·x <= 1}, P* = conv(a) = {v·x <= 1, v vertex of P},
so S(mu) = {a·x <= 1 (P-facets), v·x <= mu (P*-facets)}.
Canonical form: Warren's formula  Omega(S; y) = sum over vertices |det(n1,n2,n3)| / prod (b_i - n_i·y) over the three facets at
a simple vertex; at a vertex on k > 3 facets, the sum over a fan triangulation of its dual polygon (pilot fault 12 Nov: the octahedron
and icosahedron ends are not simple).
CONTROLS: (P1) cube: Omega(y) = prod 2/(1-y_i^2), Omega(0) = 8; (P2) cube sweep: Warren = triangulation formula (chunk 2) at
generic rational (mu, y) in every chamber; (P3) Omega(S(mu); 0) = 3!·vol(S*) exactly (chunk-2 bridge) in every chamber of both
sweeps; (N1) dropping one vertex term must break P2; (N2) a wrong turn (mu -> 2/mu) must NOT fix the insphere point.
RESULTS printed: chambers and walls; the walls under the turn; Omega(S(mu);0) per chamber and under the turn; the similarity
test of S(mu) against S(turn mu) (facet counts differ by type, so a similarity keeps types and the distance ratio); the expansion of Omega at the centre (isotropic and anisotropic parts) per chamber.
Usage: python -u canon_turn.py"""
import itertools, sys, sympy as sp, numpy as np
from scipy.spatial import Delaunay
mu, t = sp.symbols('mu t', positive=True)
phi = (1 + sp.sqrt(5)) / 2
ok = True
def Z(x): return sp.simplify(sp.radsimp(sp.expand(x))) == 0
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)

def sweep(A, V):
    """planes (n, b(mu)) of S(mu): P-facets a·x <= 1, P*-facets v·x <= mu"""
    return [(sp.Matrix(a), sp.Integer(1), 'P') for a in A] + [(sp.Matrix(v), mu, 'D') for v in V]

def vertices(H, m):
    """exact vertices of S at numeric mu = m with their tight planes; asserts simplicity (exactly 3 tight planes)"""
    out = {}
    Hn = [(np.array([float(x) for x in n]), float(b.subs(mu, m))) for n, b, _ in H]
    for tri in itertools.combinations(range(len(H)), 3):
        M = np.array([Hn[k][0] for k in tri])
        if abs(np.linalg.det(M)) < 1e-9: continue
        X = np.linalg.solve(M, [Hn[k][1] for k in tri])
        if all(Hn[k][0] @ X <= Hn[k][1] + 1e-9 for k in range(len(H))):
            tight = tuple(k for k in range(len(H)) if abs(Hn[k][0] @ X - Hn[k][1]) < 1e-9)
            out[tuple(np.round(X, 9))] = tight
    return out

def vertex_triangles(H, X, tight):
    """the tight planes at a vertex, as triangles of a fan over its dual polygon (cyclic order of the normals around the vertex).
    Exact for every y inside S: the points n_i/(b_i - n_i·y) of one vertex are coplanar, so 3! vol of the pyramid over that dual
    facet = sum over the fan of |det(n_i,n_j,n_k)| / (l_i l_j l_k). A simple vertex gives its one triangle (Warren)."""
    if len(tight) == 3: return [tuple(tight)]
    Nn = np.array([[float(x) for x in H[k][0]] for k in tight]); Nn = Nn / np.linalg.norm(Nn, axis=1)[:, None]
    c = Nn.sum(0); c /= np.linalg.norm(c); e1 = Nn[0] - (Nn[0] @ c) * c; e1 /= np.linalg.norm(e1); e2 = np.cross(c, e1)
    order = [tight[i] for i in np.argsort([np.arctan2(n @ e2, n @ e1) for n in Nn])]
    return [(order[0], order[i], order[i + 1]) for i in range(1, len(order) - 1)]

def warren(H, m, y):
    """Omega(S(mu); y), symbolic in mu, using the vertex/facet structure at mu = m (must be inside a chamber)"""
    vs = vertices(H, m); tot = 0
    for X, tight in vs.items():
        for tri in vertex_triangles(H, X, tight):
            N = sp.Matrix.hstack(*[H[k][0] for k in tri]); d = abs(sp.nsimplify(sp.simplify(N.det())))
            den = 1
            for k in tri: den *= (H[k][1] - (H[k][0].T * sp.Matrix(y))[0])
            tot += d / den
    return tot, len(vs)

def tri_omega(H, m, y):
    """chunk-2 formula: sum over a triangulation of positively oriented simplex forms"""
    vs = vertices(H, m); Xs = list(vs)
    ex = []
    for X in Xs:
        tight = vs[X][:3]; M = sp.Matrix.hstack(*[H[k][0] for k in tight]).T
        ex.append(M.LUsolve(sp.Matrix([H[k][1].subs(mu, m) for k in tight])))
    T = Delaunay(np.array(Xs, float)); Y = sp.Matrix([1, *y]); tot = 0
    br = lambda *Z: sp.Matrix.hstack(*Z).det()
    for simp in T.simplices:
        Z = [sp.Matrix([1, *ex[k]]) for k in simp]; o = br(*Z)
        if o < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o
        den = 1
        for j in range(4): den *= br(*[Z[k] if k != j else Y for k in range(4)])
        tot += o ** 3 / den
    return sp.nsimplify(sp.simplify(tot))

def vol_polar0(H, m):
    """3! vol(S*) about the centre: S* = conv of n/b over the facets of S at mu = m"""
    vs = vertices(H, m); used = sorted({k for tight in vs.values() for k in tight})
    U = [H[k][0] / H[k][1] for k in used]; Uf = np.array([[float(x.subs(mu, m)) for x in u] for u in U])
    from scipy.spatial import ConvexHull
    h = ConvexHull(Uf); tot = 0
    for simp in h.simplices:
        d = sp.Matrix.hstack(*[U[k] for k in simp]).det(); tot += d * sp.sign(d.subs(mu, m))
    return sp.simplify(tot)        # = 6 vol

def walls(H, lo, hi):
    """exact mu where the combinatorics change, in [lo, hi]: a fourth plane passes through a vertex. X(mu) = X0 + mu X1 is affine
    in mu, so each candidate is one linear root (found in floats, then identified exactly in Q(sqrt5) and re-verified)."""
    Hn = [(np.array([float(x) for x in n]), (1.0, 0.0) if b == 1 else (0.0, 1.0)) for n, b, _ in H]   # b = c0 + c1 mu
    cand = set()
    for tri in itertools.combinations(range(len(H)), 3):
        M = np.array([Hn[k][0] for k in tri])
        if abs(np.linalg.det(M)) < 1e-9: continue
        X0 = np.linalg.solve(M, [Hn[k][1][0] for k in tri]); X1 = np.linalg.solve(M, [Hn[k][1][1] for k in tri])
        for k in range(len(H)):
            if k in tri: continue
            a = Hn[k][0] @ X1 - Hn[k][1][1]; c = Hn[k][0] @ X0 - Hn[k][1][0]
            if abs(a) > 1e-12:
                r = -c / a
                if lo - 1e-9 <= r <= hi + 1e-9: cand.add(round(r, 9))
    real = []
    for r in sorted(cand):
        e = 1e-5; A_ = vertices(H, r - e); B_ = vertices(H, r + e)
        sig = lambda D: sorted(tuple(sorted(H[k][2] for k in s)) for s in D.values())
        if len(A_) != len(B_) or sig(A_) != sig(B_): real.append(r)
    exact = [sp.nsimplify(r, [sp.sqrt(5)], tolerance=1e-8) for r in real]
    for r, x in zip(real, exact): assert abs(float(x) - r) < 1e-8, (r, x)
    return exact

def study(name, A, V, Tm):
    global ok
    print(f'\n===== {name} =====', flush=True)
    H = sweep(A, V)
    r_in = 1 / sp.sqrt(sum(x ** 2 for x in A[0])); R = sp.sqrt(sum(x ** 2 for x in V[0]))
    lo, hi = sp.simplify(r_in ** 2), sp.simplify(R ** 2)
    fix = sp.sqrt(lo * hi); turn = lambda m: sp.simplify(lo * hi / m)
    print(f'P: inradius r = {sp.nsimplify(r_in)}, circumradius R = {sp.simplify(R)}; sweep from mu_lo = r^2 = {lo} (S = mu P*) '
          f'to mu_hi = R^2 = {hi} (S = P); turn mu -> {sp.simplify(lo*hi)}/mu, fixed point rR = {sp.simplify(fix)}', flush=True)
    check(f'{name}: the turn constant given ({Tm}) equals mu_lo*mu_hi', sp.simplify(lo * hi - Tm) == 0)
    # insphere: P-facets at distance r, P*-facets at distance mu/R -> equal iff mu = rR
    check(f'{name}: S(mu) has all facets at one distance iff mu = rR = turn fixed point', sp.solve(sp.Eq(mu / R, r_in), mu) == [sp.simplify(fix)])
    check(f'{name}: (N2) the wrong turn mu -> 2/mu does NOT fix the insphere point', sp.simplify(2 / fix - fix) != 0)
    W = walls(H, float(lo), float(hi))
    if name.startswith('cube'): check('cube: walls in [1, 3] are exactly 1, 2, 3 (chunk 2)', W == [1, 2, 3])
    print(f'walls in [mu_lo, mu_hi]: {W} = {[round(float(w), 6) for w in W]}', flush=True)
    imgs = [turn(w) for w in W]
    print(f'walls under the turn: {imgs}; walls mapped onto walls: {[any(sp.simplify(i - w) == 0 for w in W) for i in imgs]}', flush=True)
    pts = [float(lo) / 2] + [float(a + b) / 2 for a, b in zip([lo] + W, W + [hi]) if b - a > 1e-9] + [float(hi) * 1.5]
    pts = sorted(set(round(p, 9) for p in pts))
    bounds = sorted(set([0.0, float(lo), float(hi)] + [float(w) for w in W] + [1e9]))
    pieces = []
    for p in pts:
        m = sp.nsimplify(p, rational=True)
        om, nv = warren(H, m, (0, 0, 0)); om = sp.factor(sp.simplify(om))
        vp = vol_polar0(H, m)
        check(f'{name}: (P3) mu in chamber at {p:.4f} ({nv} vertices): Omega(S;0) = 3! vol(S*) = {om}', sp.simplify(om - vp) == 0)
        a = max(b for b in bounds if b < p); b = min(b for b in bounds if b > p)
        pieces.append((a, b, m, om))
    # the turn on Omega(S;0): f(mu) vs f(turn mu), and the weighted forms mu^k f
    def f_at(x):
        for a, b, m, om in pieces:
            if a < float(x) < b: return om.subs(mu, x)
    print('Omega(S(mu); 0) per chamber:', [(round(a, 4), round(b, 4) if b < 1e8 else 'inf', om) for a, b, m, om in pieces], flush=True)
    for k in range(0, 4):
        g = lambda x: sp.simplify(x ** k * f_at(x))
        samp = [sp.nsimplify(float(lo) + (float(hi) - float(lo)) * q, rational=True) for q in (sp.Rational(1, 7), sp.Rational(2, 7), sp.Rational(3, 7), sp.Rational(5, 9), sp.Rational(6, 7))]
        sym = [sp.simplify(g(x) - g(turn(x))) == 0 for x in samp]
        print(f'   mu^{k}·Omega(S(mu);0) turn-symmetric at samples {[round(float(x), 4) for x in samp]} (turn images {[round(float(turn(x)), 4) for x in samp]}): {sym}', flush=True)
    # similarity and affine tests of S(turn mu) against S(mu): P-facet / P*-facet distance ratio is a similarity invariant
    rho = sp.simplify((mu / R) / r_in)                      # distance(P*-facets) / distance(P-facets)
    sol = sp.solve(sp.Eq(rho, rho.subs(mu, lo * hi / mu)), mu)
    print(f'similarity: facet-distance ratio rho(mu) = {rho}; rho(mu) = rho(turn mu) only at mu = {sol}', flush=True)
    sim_pos = [s for s in sol if s.is_positive]
    # compare squares (all in Q(sqrt5); nested radicals defeated the direct comparison in the pilot)
    check(f'{name}: S(turn mu) is similar to S(mu) only at the fixed point', len(sim_pos) == 1 and sp.simplify(sp.radsimp(sim_pos[0] ** 2 - lo * hi)) == 0)
    # expansion of Omega at the centre along unit directions (series in t), per chamber
    return H, pieces, fix, r_in, R

def series_warren(H, m, u, order, raw=False):
    """coefficients of t^0..t^order of Omega(S(mu); t u): each vertex term |det| / prod (b_i - t c_i), c_i = n_i·u, expanded as
    |det|/prod b_i * prod sum_k (t c_i / b_i)^k (exact, truncated)"""
    vs = vertices(H, m); co = [0] * (order + 1)
    for X, tight0 in vs.items():
      for tight in vertex_triangles(H, X, tight0):
        d = abs(sp.nsimplify(sp.simplify(sp.Matrix.hstack(*[H[k][0] for k in tight]).det())))
        ser = [d] + [0] * order
        for k in tight:
            b = H[k][1]; c = sp.simplify((H[k][0].T * u)[0]); g = [(c / b) ** j for j in range(order + 1)]
            ser = [sum(ser[i] * g[j - i] for i in range(j + 1)) for j in range(order + 1)]
            ser = [x / b for x in ser]
        for j in range(order + 1): co[j] += ser[j]
    return co if raw else [sp.factor(sp.radsimp(sp.simplify(sp.expand(x)))) for x in co]

def expansion(H, pieces, dirs, order, fix, name):
    print(f'expansion of Omega(S(mu); t u) at the centre (orders 0..{order}), directions {list(dirs)}:', flush=True)
    for a, b, m, om in pieces:
        coeffs = {}
        for dn, u in dirs.items():
            u = sp.Matrix(u); n2 = sp.simplify(sum(x ** 2 for x in u))      # unnormalised u: keep everything in Q(sqrt5)
            raw = series_warren(H, m, u, order)
            coeffs[dn] = [sp.factor(sp.radsimp(sp.simplify(raw[j] / n2 ** (j // 2)))) if j % 2 == 0 else raw[j] for j in range(order + 1)]
        c0 = coeffs[list(dirs)[0]][0]
        iso = all(Z(coeffs[d][2] - coeffs[list(dirs)[0]][2]) for d in dirs)
        check(f'{name}: (P4) odd orders vanish and the order-2 term is isotropic', iso and all(Z(coeffs[d][j]) for d in dirs for j in range(1, order + 1, 2)))
        if order == 6:
            check(f'{name}: (P5) the order-4 term is isotropic (the icosahedral group has no quartic invariant but |y|^4)',
                  Z(coeffs[list(dirs)[0]][4] - coeffs[list(dirs)[1]][4]))
        # 12 Nov fix (run 1 hit its 2 h cap here in an icosahedral chamber): no exact factor/solve of degree-6 polynomials over
        # Q(sqrt5); cancel to one fraction, zeros by numeric roots of the numerator polynomial, values at the fixed point to 15 digits
        an = sp.cancel(sp.radsimp(sp.expand(coeffs[list(dirs)[0]][order] - coeffs[list(dirs)[1]][order])))
        rel = sp.cancel(sp.radsimp(an / c0)); q2 = sp.cancel(sp.radsimp(coeffs[list(dirs)[0]][2] / c0))
        roots = []
        if rel.has(mu):
            num = sp.Poly(sp.numer(sp.together(rel)), mu)
            roots = [complex(r).real for r in num.nroots(n=20) if abs(complex(r).imag) < 1e-12 and float(a) < complex(r).real < float(b)]
        print(f'  chamber ({round(a,4)}, {round(b,4) if b < 1e8 else "inf"}): c0 = {c0}; c2/c0 = {q2} (isotropic: {iso}); '
              f'order-{order} anisotropy/c0 = {rel}; its real zeros in the chamber: {roots}', flush=True)
        if float(a) < float(fix) < float(b):
            fq2 = sp.N(q2.subs(mu, fix), 15); fr = sp.N(rel.subs(mu, fix), 15); fd = sp.N(sp.diff(rel, mu).subs(mu, fix), 15)
            fd2 = sp.N(sp.diff(q2, mu).subs(mu, fix), 15)
            print(f'    at the fixed point mu = {sp.N(fix, 15)}: c2/c0 = {fq2} (d/dmu {fd2}); anisotropy/c0 = {fr} (d/dmu {fd})', flush=True)
        print(f'PROGRESS {name} chamber done ({time.time() - T0:.0f}s)', flush=True)

def expansion_numeric(H, pieces, dirs, order, fix, name):
    """icosahedral sweep (12 Nov fix 2: exact one-fraction forms of 60-vertex sums over Q(sqrt5) do not finish): coefficients kept as
    unsimplified exact sums; checks EXACT at 5 rational mu per chamber (each value radsimp'd to a + b sqrt5); zeros of the
    anisotropy by a 400-point mpmath scan + bisection (numeric); values at the fixed point to 15 digits (numeric)."""
    import mpmath as mp
    mp.mp.dps = 40
    print(f'expansion of Omega(S(mu); t u) at the centre (orders 0..{order}), directions {list(dirs)} [exact at sample mu, numeric elsewhere]:', flush=True)
    d0, d1 = list(dirs)
    for a, b, m, om in pieces:
        co = {}
        for dn, u in dirs.items():
            u = sp.Matrix(u); n2 = sp.radsimp(sp.expand(sum(x ** 2 for x in u)))
            rw = series_warren(H, m, u, order, raw=True)
            co[dn] = [rw[j] / n2 ** (j // 2) for j in range(order + 1)]
        hi_ = float(b) if b < 1e8 else float(a) * 3
        samp = [sp.nsimplify(float(a) + (hi_ - float(a)) * q, rational=True) for q in (0.13, 0.31, 0.5, 0.67, 0.89)]
        ex = lambda e, x: sp.radsimp(sp.expand(e.subs(mu, x)))
        p4 = all(ex(co[d][j], x) == 0 for d in dirs for j in range(1, order + 1, 2) for x in samp[:2]) and \
             all(ex(co[d0][2] - co[d1][2], x) == 0 for x in samp)
        check(f'{name}: (P4) odd orders vanish and the order-2 term is isotropic (exact at sample mu)', p4)
        check(f'{name}: (P5) the order-4 term is isotropic (exact at 5 sample mu)', all(ex(co[d0][4] - co[d1][4], x) == 0 for x in samp))
        check(f'{name}: (P3b) the order-0 term equals Omega(S;0) of the chamber (exact at 5 sample mu)', all(ex(co[d0][0] - om, x) == 0 for x in samp))
        f_an = sp.lambdify(mu, (co[d0][order] - co[d1][order]) / om, 'mpmath'); f_q2 = sp.lambdify(mu, co[d0][2] / om, 'mpmath')
        xs = [mp.mpf(float(a)) + (mp.mpf(hi_) - float(a)) * (k + 0.5) / 400 for k in range(400)]
        vs = [f_an(x) for x in xs]; zeros = []
        for x1, x2, v1, v2 in zip(xs, xs[1:], vs, vs[1:]):
            if v1 * v2 < 0: zeros.append(float(mp.findroot(f_an, (x1, x2), solver='bisect')))
        print(f'  chamber ({round(a,4)}, {round(b,4) if b < 1e8 else "inf"}): c0 = {om}; c2/c0 at sample mu {[float(x) for x in samp[:3]]}: '
              f'{[float(ex(co[d0][2] / om, x)) for x in samp[:3]]}; order-{order} anisotropy/c0 sign {"+" if vs[0] > 0 else "-"} at the left end; real zeros in the chamber (numeric): {zeros}', flush=True)
        if float(a) < float(fix) < float(b):
            F = mp.mpf(sp.N(fix, 40)); h = mp.mpf('1e-12')
            print(f'    at the fixed point mu = {mp.nstr(F, 15)}: c2/c0 = {mp.nstr(f_q2(F), 15)} (d/dmu {mp.nstr(mp.diff(f_q2, F), 15)}); '
                  f'anisotropy/c0 = {mp.nstr(f_an(F), 15)} (d/dmu {mp.nstr(mp.diff(f_an, F), 15)}) [numeric, 40-digit arithmetic]', flush=True)
        print(f'PROGRESS {name} chamber done ({time.time() - T0:.0f}s)', flush=True)

# ---------- controls on the cube ----------
cubeA = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
cubeV = [list(s) for s in itertools.product([1, -1], repeat=3)]
y1, y2, y3 = sp.symbols('y1 y2 y3')
Hc = [(sp.Matrix(a), sp.Integer(1), 'P') for a in cubeA]
wc, _ = warren(Hc, 1, (y1, y2, y3))
check('(P1) Warren on the cube = prod 2/(1 - y_i^2)', sp.simplify(wc - 8 / ((1 - y1**2) * (1 - y2**2) * (1 - y3**2))) == 0)
H = sweep(cubeA, cubeV)
Yg = (sp.Rational(1, 97), sp.Rational(1, 89), sp.Rational(1, 83))
for m in (sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(5, 2), 5):
    w, _ = warren(H, m, Yg); tri = tri_omega(H, m, Yg)
    check(f'(P2) cube sweep mu = {m}: Warren = triangulation formula at a generic point', sp.simplify(w.subs(mu, m) - tri) == 0)
# N1: drop one vertex term
vs = vertices(H, sp.Rational(3, 2)); X0 = next(iter(vs)); tight = vs[X0]
N = sp.Matrix.hstack(*[H[k][0] for k in tight]); den = 1
for k in tight: den *= (H[k][1] - (H[k][0].T * sp.Matrix(Yg))[0])
wbad = warren(H, sp.Rational(3, 2), Yg)[0] - abs(N.det()) / den
check('(N1) Warren with one vertex term dropped is caught by the triangulation check', sp.simplify(wbad.subs(mu, sp.Rational(3, 2)) - tri_omega(H, sp.Rational(3, 2), Yg)) != 0)
print('PROGRESS 0.2 controls', flush=True)
import time; T0 = time.time()

if 'ico' not in sys.argv[1:]:
    Hc_, pc, fixc, rc, Rc = study('cube / octahedron', cubeA, cubeV, 3)
    expansion(Hc_, pc, {'face axis': (1, 0, 0), 'corner axis': (1, 1, 1)}, 4, fixc, 'cube')
else: ok = False; print('PILOT MODE (cube part skipped): FINAL cannot be ok', flush=True)
print('PROGRESS 0.6 cube sweep', flush=True)

# ---------- icosahedron / dodecahedron ----------
icoV = []
for s1, s2 in itertools.product([1, -1], repeat=2):
    for p in ([0, s1, s2 * phi], [s1, s2 * phi, 0], [s2 * phi, 0, s1]): icoV.append(p)
# facet normals a of the icosahedron with a·x <= 1: a = (sum of a face's 3 vertices) / (that sum · one of them)
icoVn = np.array([[float(x) for x in v] for v in icoV]); faces = []
for i, j, k in itertools.combinations(range(12), 3):
    d = [np.linalg.norm(icoVn[p] - icoVn[q]) for p, q in ((i, j), (j, k), (i, k))]
    if max(d) - min(d) < 1e-9 and abs(d[0] - 2) < 1e-9: faces.append((i, j, k))
assert len(faces) == 20
icoA = []
for i, j, k in faces:
    c = [sp.simplify(icoV[i][q] + icoV[j][q] + icoV[k][q]) for q in range(3)]
    h = sp.simplify(sum(c[q] * icoV[i][q] for q in range(3)))
    icoA.append([sp.nsimplify(sp.simplify(x / h), [sp.sqrt(5)]) for x in c])
Hi_, pi_, fixi, ri, Ri = study('icosahedron / dodecahedron', icoA, icoV, phi ** 4 * (phi + 2) / 3)   # r^2 = phi^4/3 (edge 2), R^2 = phi + 2
expansion_numeric(Hi_, pi_, {'vertex axis': (0, 1, phi), 'face axis': tuple(sum(icoV[f][q] for f in faces[0]) for q in range(3))}, 6, fixi, 'icosahedron')
print('PROGRESS 1.0 icosahedral sweep', flush=True)
print('FINAL ok: all controls held' if ok else 'FINAL FAIL')
