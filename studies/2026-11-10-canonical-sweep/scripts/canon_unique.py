"""Aim 2, chunk 3, closing item (12 Nov 2026): EXACT proof that the icosahedral roundest point mu* = 2.891792659... is the ONLY zero
of the order-6 anisotropy of Omega(S(mu); t u) on the whole icosahedral line, mu in (0, infinity) (four chambers: S = mu P* below
(7+3sqrt5)/6, the two inner chambers, S = P above (5+sqrt5)/2). Until now uniqueness rested on a 400-point float scan per chamber.
Method (no floating point in any decision):
  1. In every chamber each facet of S has b = 1 or b = mu, so every expansion coefficient is a polynomial in nu = 1/mu over Q(sqrt5)
     (canon_closed.py); build the order-6 anisotropy A(nu) = (vertex axis) - (face axis) exactly in each chamber.
  2. Write A = P + sqrt5 R with P, R in Q[nu]; its norm N = P^2 - 5 R^2 lies in Q[nu] and every root of A is a root of N.
  3. Factor N over Q. For each irreducible factor F: G = gcd(A, F) over Q(sqrt5) (squarefree, its roots are simple roots of F).
     Isolate the real roots of F exactly (sympy's exact real-root isolation, rational intervals); keep those strictly inside the
     chamber (interval endpoints compared exactly with the walls in Q(sqrt5), refined until clear of them); a root xi of F is a
     root of A iff G changes sign on its isolating interval (G has simple roots and no other root there): sign of G at the rational
     endpoints decided exactly in Q(sqrt5).
  4. At the walls themselves A is evaluated exactly (from both sides; the two sides must agree, a continuity control).
Controls: (P1) inner chamber (phi^2, (5+sqrt5)/2): exactly one root, equal to mu* (canon_closed: 2.891792659030825043) and its factor F
is the known degree-12 polynomial; (P2) the counter on the cube line's exact order-4 anisotropies (chunk 3) finds exactly one root,
1.692590 in (1, 2); (P3) synthetic: (nu - (1+sqrt5)/8)(nu - 3/7)^2(nu^2 - 2) on (0, 1) has 2 distinct roots; (N1) nu - (3+sqrt5)/4 on
(0, 1) has 0 roots although its conjugate root (3-sqrt5)/4 lies inside (the counter must not count conjugate roots); (C1) A equals the
raw canon_turn series at one rational mu per chamber; (C2) the anisotropy along a third axis (edge axis) is a constant multiple of
A in the inner chamber (degree-6 harmonic invariants of the icosahedral group form a line); (C3) continuity of A at every wall.
Usage: python -u canon_unique.py [pilot]   (pilot = synthetic controls + the root chamber only)"""
import sys, os, time
T0 = time.time()
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'canon_turn.py')).read()
defs = src[:src.index('# ---------- controls on the cube ----------')]
ico = src[src.index('# ---------- icosahedron / dodecahedron ----------'):src.index('Hi_, pi_, fixi')]
g = {'__name__': 'canon_turn_defs'}; exec(defs, g); exec(ico, g)
sp, mu, phi, check = g['sp'], g['mu'], g['phi'], g['check']
PILOT = len(sys.argv) > 1 and sys.argv[1] == 'pilot'
s5 = sp.sqrt(5); nu = sp.Symbol('nu', positive=True); x = sp.Symbol('x')
H = g['sweep'](g['icoA'], g['icoV']); faces, icoV = g['faces'], g['icoV']

# ---------- exact arithmetic in Q(sqrt5) ----------
def split5(c):
    c = sp.expand(sp.radsimp(sp.expand(c))); q = c.coeff(s5); p = sp.expand(c - q * s5)
    assert p.is_Rational and q.is_Rational, ('not in Q(sqrt5)', c); return p, q
def sgn5(c):
    p, q = split5(c)
    if q == 0: return int(sp.sign(p))
    if p == 0: return int(sp.sign(q))
    if p > 0 and q > 0: return 1
    if p < 0 and q < 0: return -1
    d = p * p - 5 * q * q
    return int(sp.sign(d)) if p > 0 else -int(sp.sign(d))
def evalpoly(coeffs, r):                          # coeffs high -> low, exact
    v = sp.Integer(0)
    for c in coeffs: v = v * r + c
    return v

def count_roots(Aexpr, var, lo, hi, tag):
    """distinct real roots of Aexpr (coefficients in Q(sqrt5)) in the open interval (lo, hi); lo, hi in Q(sqrt5) or None (= -inf/+inf).
    Returns a list of (F, isolating interval, float value)."""
    A = sp.Poly(sp.expand(Aexpr), var)
    PR = [split5(c) for c in A.all_coeffs()]
    P = sp.Poly([p for p, q in PR], var, domain='QQ'); R = sp.Poly([q for p, q in PR], var, domain='QQ')
    N = P ** 2 - 5 * R ** 2
    assert not N.is_zero
    found = []
    for F, m in sp.factor_list(N.as_expr(), var)[1]:
        F = sp.Poly(F, var)
        if F.degree() < 1: continue
        G = sp.Poly(sp.gcd(A.as_expr(), F.as_expr(), extension=s5), var)
        Gc = G.all_coeffs()
        eps = sp.Rational(1, 10 ** 40)            # isolating intervals of width < 1e-40
        def rel(a, b, w):                         # interval [a, b] against the wall w: below, above or touching
            if sgn5(w - b) > 0: return 'below'
            if sgn5(a - w) > 0: return 'above'
            return 'touch'
        for _ in range(8):
            keep, bad = [], False
            for (a, b), mult in F.intervals(eps=eps):
                if a == b and any(w is not None and sp.radsimp(a - w) == 0 for w in (lo, hi)): continue   # a root ON an open end
                rl =None if lo is None else rel(a, b, lo); rh = None if hi is None else rel(a, b, hi)
                if (rl in (None, 'above')) and (rh in (None, 'below')): keep.append((a, b))
                elif rl == 'below' or rh == 'above': pass
                else: bad = True                  # touches a wall: refine
            if not bad: break
            eps = eps / 10 ** 12
        assert not bad, f'{tag}: could not separate a root of {F} from a wall'
        for a, b in keep:
            if G.degree() < 1: continue
            if a == b:                            # an exact rational root
                if evalpoly(Gc, a) == 0: found.append((F.as_expr(), (a, b), float(a)))
                continue
            assert F.eval(a) != 0 and F.eval(b) != 0
            sa, sb = sgn5(evalpoly(Gc, a)), sgn5(evalpoly(Gc, b))
            assert sa != 0 and sb != 0
            if sa != sb: found.append((F.as_expr(), (a, b), (a + b) / 2))
    return found

ok_all = True
def chk(name, cond):
    global ok_all; ok_all &= bool(cond); check(name, cond)

# ---------- counter controls ----------
r = count_roots((x - (1 + s5) / 8) * (x - sp.Rational(3, 7)) ** 2 * (x ** 2 - 2), x, sp.Integer(0), sp.Integer(1), 'P3')
chk(f'(P3) synthetic (x-(1+sqrt5)/8)(x-3/7)^2(x^2-2) on (0,1): {len(r)} distinct roots (expect 2) at {[round(float(f), 6) for _, _, f in r]}',
    len(r) == 2 and abs(float(sorted(f for _, _, f in r)[0]) - float((1 + s5) / 8)) < 1e-9)
r = count_roots(x - (3 + s5) / 4, x, sp.Integer(0), sp.Integer(1), 'N1')
chk(f'(N1) x-(3+sqrt5)/4 on (0,1): {len(r)} roots (expect 0; its conjugate (3-sqrt5)/4 = 0.191 lies inside)', len(r) == 0)
cube = [(None, sp.Integer(1), sp.Integer(-28)),
        (sp.Integer(1), sp.Integer(2), x ** 4 + 2 * x ** 3 + x ** 2 - 4 * x - 14),
        (sp.Integer(2), sp.Integer(3), 3 * x ** 4 + 2 * x ** 3 - 2 * x ** 2 - 8 * x - 12),
        (sp.Integer(3), None, sp.Integer(3))]          # numerators of the order-4 anisotropy/c0 (canon_turn.log), mu > 0
tot = []
for lo, hi, num in cube:
    if num.has(x): tot += count_roots(num, x, lo if lo is not None else sp.Integer(0), hi, 'P2')
chk(f'(P2) cube line: exactly one zero of the order-4 anisotropy, at {[round(float(f), 6) for _, _, f in tot]} (expect 1.692590)',
    len(tot) == 1 and abs(float(tot[0][2]) - 1.692590) < 1e-5)
print(f'PROGRESS 0.05 counter controls ({time.time() - T0:.0f} s)', flush=True)

# ---------- the icosahedral line ----------
w1, w2, w3 = (7 + 3 * s5) / 6, (3 + s5) / 2, (5 + s5) / 2
inv = lambda w: sp.radsimp(1 / w)
chambers = [('mu < (7+3sqrt5)/6 (S = mu P*)', sp.Integer(2), inv(w1), None),
            ('(7+3sqrt5)/6 < mu < phi^2', sp.Rational(49, 20), inv(w2), inv(w1)),
            ('phi^2 < mu < (5+sqrt5)/2', sp.Rational(1559, 500), inv(w3), inv(w2)),
            ('mu > (5+sqrt5)/2 (S = P)', sp.Integer(4), sp.Integer(0), inv(w3))]   # (name, m0, nu_lo, nu_hi)
if PILOT: chambers = [chambers[2]]
ORD = 6
dirs = {'vertex axis': sp.Matrix([0, 1, phi]), 'face axis': sp.Matrix([sum(icoV[f][q] for f in faces[0]) for q in range(3)]),
        'edge axis': sp.Matrix([icoV[faces[0][0]][q] + icoV[faces[0][1]][q] for q in range(3)])}

def series_nu(u, order, m0):
    vs = g['vertices'](H, m0); co = [sp.Integer(0)] * (order + 1)
    for X, tight0 in vs.items():
        for tri in g['vertex_triangles'](H, X, tight0):
            d = abs(sp.nsimplify(sp.radsimp(sp.Matrix.hstack(*[H[k][0] for k in tri]).det()), [s5]))
            ser = [d] + [sp.Integer(0)] * order
            for k in tri:
                ib = sp.Integer(1) if H[k][1] == 1 else nu
                c = sp.radsimp(sp.expand((H[k][0].T * u)[0])); gg = [sp.expand((c * ib) ** j) for j in range(order + 1)]
                ser = [sp.expand(ib * sum(ser[i] * gg[j - i] for i in range(j + 1))) for j in range(order + 1)]
            for j in range(order + 1): co[j] += ser[j]
    return [sp.radsimp(sp.expand(xx)) for xx in co], len(vs)

KNOWN = 25*nu**12 + 50*nu**11 - 150*nu**10 - 670*nu**9 + 789*nu**8 + 52*nu**7 - 47052*nu**6 - 26016*nu**5 - 8365*nu**4 - 1298*nu**3 + 370*nu**2 + 402*nu + 199
MUSTAR = 2.891792659030825043
Aw = {}; allroots = []
for ci, (name, m0, lo, hi) in enumerate(chambers):
    t1 = time.time(); co = {}
    use = ['vertex axis', 'face axis'] + (['edge axis'] if 'phi^2 <' in name else [])
    for dn in use:
        u = dirs[dn]; n2 = sp.radsimp(sp.expand(sum(xx ** 2 for xx in u)))
        ser, nv = series_nu(u, ORD, m0)
        co[dn] = [sp.expand(sp.radsimp(ser[j] / n2 ** (j // 2))) for j in range(ORD + 1)]
    A = sp.expand(sp.radsimp(co['vertex axis'][ORD] - co['face axis'][ORD]))
    c0 = co['vertex axis'][0]
    print(f'chamber {name}: {nv} vertices; c0 = {sp.factor(c0, extension=s5)}; A(nu) = {sp.factor(A, extension=s5)} ({time.time() - t1:.0f} s)', flush=True)
    # (C1) against the raw canon_turn series at m0
    raw = {dn: g['series_warren'](H, m0, dirs[dn], ORD, raw=True) for dn in ('vertex axis', 'face axis')}
    n2s = {dn: sp.radsimp(sp.expand(sum(xx ** 2 for xx in dirs[dn]))) for dn in raw}
    rv = sp.radsimp(sp.expand((raw['vertex axis'][ORD] / n2s['vertex axis'] ** 3 - raw['face axis'][ORD] / n2s['face axis'] ** 3).subs(mu, m0)))
    chk(f'(C1) {name}: A equals the raw canon_turn series exactly at mu = {m0}', sp.radsimp(sp.expand(rv - A.subs(nu, 1 / m0))) == 0)
    chk(f'(C0) {name}: c0 > 0 at mu = {m0}', sgn5(c0.subs(nu, 1 / m0)) > 0)
    if 'edge axis' in co:
        E = sp.expand(sp.radsimp(co['vertex axis'][ORD] - co['edge axis'][ORD]))
        ratio = sp.radsimp(sp.cancel(E / A))
        chk(f'(C2) {name}: vertex-minus-edge anisotropy = ({sp.nsimplify(ratio)}) x A, a constant (one degree-6 harmonic invariant)', not ratio.has(nu))
    Aw[ci] = A
    if not A.has(nu):
        z = [] if sgn5(A) != 0 else ['identically zero']
        print(f'   A is the constant {A}: zeros {z}', flush=True)
        chk(f'{name}: A is a nonzero constant', not z)
        roots = []
    else:
        roots = count_roots(A, nu, lo, hi, name)
    for F, (a, b), f in roots:
        print(f'   root nu = {sp.N(f, 30)}, mu = {sp.N(1 / f, 30)}, isolating interval width {float(b - a):.1e}, factor of N: {F}', flush=True)
    allroots += [(name, F, 1 / f) for F, _, f in roots]
    print(f'   {name}: {len(roots)} zero(s) of the order-6 anisotropy inside the chamber (exact)', flush=True)
    if 'phi^2 <' in name:
        chk(f'(P1) {name}: exactly one zero, mu* = {MUSTAR}, with the known degree-12 factor',
            len(roots) == 1 and abs(sp.N(1 / roots[0][2], 30) - sp.Float('2.891792659030825042847886342940', 30)) < 1e-25 and sp.simplify(sp.Poly(roots[0][0], nu).monic().as_expr() - sp.Poly(KNOWN, nu).monic().as_expr()) == 0)
    print(f'PROGRESS {(ci + 1) / len(chambers):.2f} chamber {ci + 1}/{len(chambers)} ({time.time() - T0:.0f} s)', flush=True)

if not PILOT:
    # walls: A from both sides, exactly; continuity and nonvanishing
    for wn, w, l, r_ in (('(7+3sqrt5)/6', w1, 0, 1), ('phi^2', w2, 1, 2), ('(5+sqrt5)/2', w3, 2, 3)):
        vl = sp.radsimp(sp.expand(Aw[l].subs(nu, inv(w)))) if Aw[l].has(nu) else Aw[l]
        vr = sp.radsimp(sp.expand(Aw[r_].subs(nu, inv(w)))) if Aw[r_].has(nu) else Aw[r_]
        chk(f'(C3) wall mu = {wn}: A continuous ({sp.nsimplify(vl)} from both sides) and nonzero there', sp.radsimp(vl - vr) == 0 and sgn5(vl) != 0)
    chk(f'THEOREM: on the whole icosahedral line (0 < mu < infinity) the order-6 anisotropy has exactly one zero, mu* = {MUSTAR} '
        f'(found: {[(n, round(float(m), 12)) for n, _, m in allroots]})', len(allroots) == 1 and abs(float(allroots[0][2]) - MUSTAR) < 1e-12)
print(f'time {time.time() - T0:.0f} s', flush=True)
if PILOT: print('FINAL ok: pilot controls held' if ok_all and g['ok'] else 'FINAL FAIL')
else: print('FINAL ok: all controls held, uniqueness proved exactly' if ok_all and g['ok'] else 'FINAL FAIL')
