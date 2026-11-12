"""LEAD 4: close the icosahedral constant by the moment route plus ONE invariant harmonic.
Setting (row 2): for a G-symmetric body, t_min <= 1/c^2 with c = min_{u,w unit} max_{g in G} (gu).w. Orbit moments alone give, for
I (a 5-design), only c >= sqrt(3/5) (constant 5/3). The true c^2 = (5 + 2sqrt5)/15 (constant 15 - 6sqrt5).
Certificate: p(t) = (t - c) * prod_{v in V, v != c} (t - v)^2, V = the inner products of the extremal pair (u5 = five-fold axis,
w3 = three-fold axis). p <= 0 on [-1, c]. Its orbit mean, for unit u, w, uses the design property up to degree 5, the degree-6
invariant harmonic h(u, w) = mean_g ((gu).w)^6 - 1/7, and mean t^7 = 0 (I has no invariant harmonic of odd degree below 15):
    mean p = A + p6 * h(u, w).
h has rank one, h = kappa Phi(u) Phi(w) (exact: coefficient matrix of rank 1). If mean p >= 0 for all unit u, w, then
max_g (gu).w >= c for every pair (else every p(t_g) <= 0, mean p = 0, forcing the extremal configuration, whose max is c).
mean p >= 0 for all pairs <=> h(u5, w3) is the extreme of h in the direction of -p6, i.e. Phi takes its max and min on the sphere
at the five-fold and three-fold axes. That range statement is checked exactly at all axes and numerically on the sphere.
POSITIVE CONTROL: the tetrahedral group T with its degree-3 invariant xyz, the same construction, reproduces c = 1/3 (constant 9),
with the range of xyz on the sphere exact (AM-GM). NEGATIVE CONTROL: without the harmonic term (A alone) the certificate fails
(A < 0), and moments of degree <= 5 give only sqrt(3/5) < c."""
import itertools, random, sympy as sp, numpy as np
checks = {}
def check(k, ok): checks[k] = bool(ok); print(('ok   ' if ok else 'FAIL ') + k, flush=True)
s5 = sp.sqrt(5); phi = (1 + s5) / 2
u = sp.Matrix(sp.symbols('u1 u2 u3', real=True)); w = sp.Matrix(sp.symbols('w1 w2 w3', real=True)); VARS = list(u) + list(w)
D = lambda s: sp.diag(*s)
def gen_group(gens, n):
    G = [sp.eye(3)]; fr = [sp.eye(3)]; key = lambda M: tuple(round(float(e), 9) for e in M); seen = {key(sp.eye(3))}
    while fr:
        nx = []
        for M in fr:
            for g in gens:
                N = (g * M).applyfunc(lambda e: sp.radsimp(sp.expand(e)))
                if key(N) not in seen: seen.add(key(N)); G.append(N); nx.append(N)
        fr = nx
    assert len(G) == n, len(G); return G
g3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]); g2 = D((1, -1, -1))
cv = 1 / (2 * phi); vax = sp.Matrix([0, 1, phi])
cross = sp.Matrix([[0, -vax[2], vax[1]], [vax[2], 0, -vax[0]], [-vax[1], vax[0], 0]])
h5 = (cv * sp.eye(3) + cross / 2 + (1 - cv) / (1 + phi**2) * vax * vax.T).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))
I = gen_group([g3, g2, h5], 60)
T = gen_group([g3, g2], 12)
check('groups: I 60 exact rotations, T 12', len(I) == 60 and len(T) == 12)
t = sp.Symbol('t')
uniform = {0: 1, 1: 0, 2: sp.Rational(1, 3), 3: 0, 4: sp.Rational(1, 5), 5: 0, 6: sp.Rational(1, 7), 7: 0}
def moment_poly(G, k):
    lin = [sp.Poly(((M * u).T * w)[0], *VARS, extension=s5) for M in G]
    return sum((L**k for L in lin), sp.Poly(0, *VARS, extension=s5)) * sp.Rational(1, len(G))
def coeff_matrix(P, k):     # P bihomogeneous of degree (k, k) in (u, w): matrix over the monomial bases
    mons = [m for m in itertools.product(range(k + 1), repeat=3) if sum(m) == k]
    ix = {m: i for i, m in enumerate(mons)}
    C = sp.zeros(len(mons), len(mons))
    for exps, cf in P.terms(): C[ix[exps[:3]], ix[exps[3:]]] += cf
    return C
def run(name, G, k, u_ext, w_ext, c_true, range_exact=None, needs_harmonic=True):
    print(f'--- {name}: harmonic degree {k}', flush=True)
    uu = (u.T * u)[0]; ww = (w.T * w)[0]
    Mk = moment_poly(G, k)
    unif = sp.Poly(uniform[k] * (uu * ww)**(k // 2), *VARS, extension=s5) if k % 2 == 0 else sp.Poly(0, *VARS, extension=s5)
    H = Mk - unif                                                  # the invariant-harmonic part of the degree-k mean
    check(f'{name}: degree-{k} mean has a nonzero invariant-harmonic part', not H.is_zero)
    C = coeff_matrix(H, k); r = C.rank(simplify=True)
    check(f'{name}: h(u, w) has rank one (coefficient matrix {C.shape[0]}x{C.shape[1]}, exact rank {r})', r == 1)
    # extremal configuration and its inner products
    ue = u_ext / sp.sqrt((u_ext.T * u_ext)[0]); we = w_ext / sp.sqrt((w_ext.T * w_ext)[0])
    vals = [sp.radsimp(sp.simplify(((M * ue).T * we)[0])) for M in G]
    V = []
    for v in vals:
        if not any(sp.simplify(v - x) == 0 for x in V): V.append(v)
    c = max(V, key=lambda e: float(e))
    check(f'{name}: extremal pair max = c with c^2 = {c_true}', sp.simplify(c**2 - c_true) == 0)
    p = sp.expand((t - c) * sp.prod([(t - v)**2 for v in V if sp.simplify(v - c) != 0]))
    deg = sp.degree(p, t); print(f'{name}: distinct inner products {len(V)}: {[sp.nsimplify(sp.N(v, 30), [s5]) for v in V]}; certificate degree {deg}', flush=True)
    check(f'{name}: certificate degree {deg} <= {k + 1} (only the degree-{k} harmonic enters)', deg <= k + 1)
    if deg == k + 1:
        Mk1 = moment_poly(G, k + 1)
        unif1 = sp.Poly(uniform[k + 1] * (uu * ww)**((k + 1) // 2), *VARS, extension=s5) if (k + 1) % 2 == 0 else sp.Poly(0, *VARS, extension=s5)
        check(f'{name}: degree-{k + 1} mean has no harmonic part (equals the uniform value)', (Mk1 - unif1).is_zero)
    pp = sp.Poly(p, t)
    A = sp.radsimp(sp.simplify(sum(cf * uniform[e[0]] for e, cf in pp.terms())))
    pk = sp.radsimp(pp.coeff_monomial(t**k))
    h_ext = sp.radsimp(sp.simplify(H.as_expr().subs(dict(zip(VARS, list(ue) + list(we))))))
    mean_ext = sp.radsimp(sp.simplify(A + pk * h_ext))
    direct = sp.radsimp(sp.simplify(sum(p.subs(t, v) for v in vals) / len(G)))
    check(f'{name}: at the extremal pair mean p = A + p_k h = 0 (and = the direct orbit mean {direct})', mean_ext == 0 and direct == 0)
    print(f'{name}: A = {A} ~ {float(A):.6f}, p_k = {pk} ~ {float(pk):.6f}, h(extremal) = {h_ext} ~ {float(h_ext):.6g}', flush=True)
    check(f'{name}: NEGATIVE CONTROL: treating the orbit as a design of degree {k} (h = 0) contradicts the exact orbit mean at the extremal pair (A = {float(A):.6g} != 0): the harmonic term is essential', sp.simplify(A) != 0)
    # range of h: h = kappa Phi(u) Phi(w); Phi(x) = h(x, x0) for a fixed axis x0 with h(x0, x0) != 0
    x0 = u_ext                                   # unnormalised axis (entries in Q(sqrt5)); h = Phi(u) Phi(w) / h(x0, x0) for any scale
    Phi = sp.Poly(H.as_expr().subs(dict(zip(list(w), list(x0)))).expand(), *list(u), extension=s5)
    need = 'min' if float(pk) > 0 else 'max'
    # numeric sphere range of h(u, w) = h(u,x0) h(x0,w) / h(x0,x0)
    f = sp.lambdify(list(u), Phi.as_expr(), 'numpy'); hxx = float(H.as_expr().subs(dict(zip(VARS, list(x0) + list(x0)))))
    rng = np.random.default_rng(4); X = rng.normal(size=(400000, 3)); X /= np.linalg.norm(X, axis=1)[:, None]
    F = f(X[:, 0], X[:, 1], X[:, 2])
    from scipy.optimize import minimize
    def refine(sign):
        best = None
        for idx in np.argsort(sign * F)[:40]:
            r = minimize(lambda z: sign * f(*(z / np.linalg.norm(z))), X[idx], method='Nelder-Mead', options=dict(xatol=1e-13, fatol=1e-15, maxiter=4000))
            val = sign * r.fun
            best = val if best is None else (min(best, val) if sign > 0 else max(best, val))
        return best
    fmin, fmax = refine(1), refine(-1)
    hvals = [fmin * fmax / hxx, fmin * fmin / hxx, fmax * fmax / hxx]
    hext_num = min(hvals) if need == 'min' else max(hvals)
    print(f'{name}: Phi range on the sphere (numeric) [{fmin:.15f}, {fmax:.15f}]; extreme of h needed ({need}) {hext_num:.15g}; h at the extremal pair {float(h_ext):.15g}', flush=True)
    check(f'{name}: the extremal pair attains the {need} of h on the sphere (numeric, 1e-12)', abs(hext_num - float(h_ext)) < 1e-12)
    # exact values of Phi (unit vectors) at the extremal axes vs the numeric range ends
    scale = lambda x: x / sp.sqrt((x.T * x)[0])
    Pu = sp.radsimp(sp.simplify(Phi.as_expr().subs(dict(zip(list(u), list(ue))))))
    Pw = sp.radsimp(sp.simplify(Phi.as_expr().subs(dict(zip(list(u), list(we))))))
    print(f'{name}: Phi exact at the extremal u axis {Pu} ~ {float(Pu):.15f}, at the extremal w axis {Pw} ~ {float(Pw):.15f}', flush=True)
    ends = sorted([float(Pu), float(Pw)])
    check(f'{name}: the numeric range ends of Phi on the sphere are the exact values at the two extremal axes (1e-12)', abs(ends[0] - fmin) < 1e-12 and abs(ends[1] - fmax) < 1e-12)
    if range_exact is not None:
        check(f'{name}: range of Phi on the sphere exact: {range_exact[0]}', range_exact[1](Phi, ue, we))
    # sanity: random pairs never beat c
    ok = True; Gf = [np.array(M.evalf(), float) for M in G]; cf = float(c); worst = 9
    for _ in range(20000):
        a = rng.normal(size=3); b = rng.normal(size=3); a /= np.linalg.norm(a); b /= np.linalg.norm(b)
        m = max(float((M @ a) @ b) for M in Gf); worst = min(worst, m); ok &= m >= cf - 1e-12
    check(f'{name}: sanity, 20000 random unit pairs: min over pairs of max_g (gu).w = {worst:.9f} >= c = {cf:.9f}', ok)
    return c, A, pk, h_ext
# POSITIVE CONTROL: tetrahedral, degree-3 invariant (xyz)
def T_range(Phi, ue, we):
    # Phi is a multiple of u1 u2 u3; |u1 u2 u3| <= 3^(-3/2) on the sphere (AM-GM), attained at (1,1,1)/sqrt3 = ue
    q = sp.Poly(u[0] * u[1] * u[2], *list(u), extension=s5)
    ratio = sp.simplify(Phi.as_expr() / q.as_expr())
    return ratio.free_symbols == set() and sp.simplify(abs(ue[0] * ue[1] * ue[2]) - 3**sp.Rational(-3, 2)) == 0
cT, AT, pT, hT = run('T (positive control)', T, 3, sp.Matrix([1, 1, 1]), sp.Matrix([-1, -1, -1]), sp.Rational(1, 9), ('|xyz| <= 3^(-3/2), AM-GM', T_range), needs_harmonic=False)
check('T: constant 1/c^2 = 9 recovered', sp.simplify(1 / cT**2 - 9) == 0)
cI, AI, pI, hI = run('I', I, 6, sp.Matrix([0, 1, phi]), sp.Matrix([1, 1, 1]), (5 + 2 * s5) / 15)
check('I: constant 1/c^2 = 15 - 6sqrt5 (Theorem 2 of #43) from moments + the degree-6 harmonic', sp.simplify(1 / cI**2 - (15 - 6 * s5)) == 0)
check('I: moments alone give only sqrt(3/5) < c (5/3 > 15 - 6sqrt5)', float(sp.sqrt(sp.Rational(3, 5))) < float(cI))
bad = [k for k, v in checks.items() if not v]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
