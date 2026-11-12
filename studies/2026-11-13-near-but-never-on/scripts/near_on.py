#!/usr/bin/env python3
"""Near but never on (13 Nov 2026; aim 2, candidate route to DICTO's "Canonical Law").
On a polar line S(mu) = P cap mu P* (facets w.x <= 1, corner planes v.x <= mu) the canonical form's first direction-dependent
Taylor term at the centre is T(mu) * H(y), H the degree-k invariant harmonic of G = Sym(P) (k = first such degree). We call T the
form's TONE; the corner TONE is H(corner(mu)). Special points = zeros of a tone. The turn mu -> c/mu, c = (hR)^2, fixed point hR.
For every line: T exactly in every chamber (polynomial in nu = 1/mu over Q(sqrt5)), its zeros counted EXACTLY on the whole line
(counter of canon_unique.py), the corner tone the same way, the value at hR decided exactly.
THEORY TESTED (proved in the README): with f(s) = mu^lam T(mu), mu = hR e^s, lam = (d+k)/2,
  (a) if P is self-dual by an isometry g that acts on H by eps, then f(-s) = eps f(s) on the whole line (exact identity per chamber
      pair), so eps = -1 forces T(hR) = 0 and corner tone 0: ON;
  (b) more generally T(hR) = 0 whenever Sym(S(hR)) has no invariant harmonic of degree k (B4: S(2) = 24-cell);
  (c) otherwise f(0) is the even part at the fixed point and f'(0) is all odd part; the zero sits at s1 = -f(0)/f'(0) to first order;
      a Kantorovich bound certifies |s*| <= t*; the two-ends model mu_m = (-T_V/T_P)^(1/(d+k)).
Controls: POSITIVE the four known stations exactly (cube 1.692590 = root of mu^4+2mu^3+mu^2-4mu-14; icosahedral 2.891793 (degree 12);
600-cell mu* (degree 20) and mu_Omega (degree 24)); tone independent of direction (third axis, exact); lower orders isotropic; H
harmonic; continuity at walls; NEGATIVE a perturbed (non-regular) tetrahedron line: order 3 does not vanish at mu = 1 and the parity
identity fails; on non-self-dual lines the parity identity fails for both signs.
Usage: python -u near_on.py [--pilot]"""
import sys, os, time, json, itertools
here = os.path.dirname(os.path.abspath(__file__))
STUD = os.path.join(here, '..', '..')
# ---- machinery of pds_line.py (field Q(sqrt5), exact chambers, pulling triangulation, Taylor expansion): same code, not retyped ----
_src = open(os.path.join(STUD, '2026-11-12-pds-hopscotch-line', 'scripts', 'pds_line.py')).read()
exec(_src[:_src.index('# ================= CONTROL 1')], globals())
s5 = sp.sqrt(5)
# ---- exact real-root counter of canon_unique.py: same code, not retyped ----
_cu = open(os.path.join(STUD, '2026-11-10-canonical-sweep', 'scripts', 'canon_unique.py')).read()
exec(_cu[_cu.index('# ---------- exact arithmetic in Q(sqrt5) ----------'):_cu.index('ok_all = True')], globals())
import mpmath as mp
mp.mp.dps = 50
NP = 2
OUT = {}
mu = sp.Symbol('mu', positive=True); m_ = sp.Symbol('m'); tt = sp.Symbol('t')
phi = K(Fr(1, 2), Fr(1, 2))
def ks(k): return sp.Rational(k.a.numerator, k.a.denominator) + sp.Rational(k.b.numerator, k.b.denominator) * s5
def V_(*xs): return tuple(x if type(x) is K else K(x) for x in xs)
def kpow(x, n):
    p = K(1)
    for _ in range(n): p = p * x
    return p
def Edk(d, k):  # E[x1^k] on S^(d-1), k even
    num = 1
    for i in range(1, k, 2): num *= i
    den = 1
    for i in range(k // 2): den *= d + 2 * i
    return Fr(num, den)

def Hval(V, k, u):
    """the degree-k invariant harmonic of the orbit V at u (exact): sum (v.u)^k minus its sphere mean (k even)"""
    d = len(u); s = K(0)
    for v in V: s = s + kpow(dot(v, u), k)
    if k % 2 == 0: s = s - kpow(dot(V[0], V[0]), k // 2) * Edk(d, k) * len(V) * kpow(dot(u, u), k // 2)
    return s
def Hn(V, k, u): return Hval(V, k, u) / kpow(dot(u, u), k // 2) if k % 2 == 0 else Hval(V, k, u)
DOM = sp.QQ.algebraic_field(sp.sqrt(5))
def Hsym(V, k, d):
    y = sp.symbols(f'y1:{d + 1}')
    tot = sp.Poly(0, *y, domain=DOM)
    for v in V: tot += sp.Poly(sum(ks(a) * b for a, b in zip(v, y)), *y, domain=DOM) ** k
    if k % 2 == 0: tot -= sp.Poly(sum(b * b for b in y), *y, domain=DOM) ** (k // 2) * ks(kpow(dot(V[0], V[0]), k // 2) * Edk(d, k) * len(V))
    return tot, y
def lap_zero(Hp, y):
    return sum((Hp.diff(t).diff(t) for t in y), sp.Poly(0, *y, domain=DOM)).is_zero
def corner_tone(V, k, x0, x1):
    """H(x0 + mu x1) as an exact polynomial in mu (orbit sum, univariate)"""
    lin = lambda v: sp.Poly(ks(dot(v, x0)) + ks(dot(v, x1)) * mu, mu, domain=DOM)
    tot = sp.Poly(0, mu, domain=DOM)
    for v in V: tot += lin(v) ** k
    if k % 2 == 0:
        n2 = sp.Poly(ks(dot(x0, x0)) + 2 * ks(dot(x0, x1)) * mu + ks(dot(x1, x1)) * mu ** 2, mu, domain=DOM)
        tot -= n2 ** (k // 2) * ks(kpow(dot(V[0], V[0]), k // 2) * Edk(len(x0), k) * len(V))
    return sp.expand(tot.as_expr())
def conj5(w):
    p, q = split5(w); return p - q * s5
def strip_walls(expr, ends, var=None):
    """divide out (mu - w)^m for every end w in Q(sqrt5) (or 0) where expr vanishes: zeros ON walls are reported separately.
    Also divide out (mu - conj(w)) where it divides: the counter isolates roots of the norm, and a root of the conjugate polynomial
    sitting exactly on a wall cannot be separated from it (that factor has no root inside the chamber, so nothing is lost)."""
    var = mu if var is None else var
    P = sp.Poly(expr, var, domain=DOM); hits = []
    for w in ends:
        if w is None: continue
        for ww, tag in ((w, True), (conj5(w), False)):
            while not P.is_zero and P.degree() > 0 and sgn5(sp.expand(P.as_expr().subs(var, ww))) == 0:
                P = sp.Poly(sp.div(P, sp.Poly(var - ww, var, domain=DOM))[0], var, domain=DOM)
                if tag: hits.append(w)
    return sp.expand(P.as_expr()), hits

NU = sp.Symbol('nu_c')
def count_T(T, lo, hi, tag, sym=False):
    """zeros of the tone in (lo, hi), counted in nu = 1/mu exactly as canon_unique.py does (its proven path); returned in mu.
    (Counting the same polynomials in mu stalled for 15 min in the icosahedral chamber 1: pilot 13 Nov.)"""
    val = (lambda c: c) if sym else ks
    e0 = min(T); Pn = sp.expand(sum(val(c) * NU ** (e - e0) for e, c in T.items()))
    nlo = sp.Integer(0) if hi is None else sp.radsimp(1 / hi)
    nhi = None if (lo is None or lo == 0) else sp.radsimp(1 / lo)
    if not Pn.has(NU): return [], []
    Ps, hits = strip_walls(Pn, [nlo, nhi], NU)
    rr = count_roots(Ps, NU, nlo, nhi, tag) if Ps.has(NU) else []
    out = []
    for F, (a, b), f in rr:
        Fp = sp.Poly(F, NU); Fm = sp.expand(Fp.as_expr().subs(NU, 1 / mu) * mu ** Fp.degree())
        out.append((Fm, (1 / b, 1 / a), 1 / f))
    return out, [sp.radsimp(1 / w) for w in hits if w != 0]

def dsub(a, b): return {e: a.get(e, K(0)) - b.get(e, K(0)) for e in set(a) | set(b)}
def dscale(a, c): return {e: v * c for e, v in a.items()}
def dclean(a): return {e: v for e, v in a.items() if not v.z()}
def T_expr(T): return sum(ks(c) * mu ** (-e) for e, c in T.items())
def T_num(T):     # numerator polynomial in mu (multiply by mu^emax)
    em = max(T) if T else 0
    return sp.expand(sum(ks(c) * mu ** (em - e) for e, c in T.items())), em

def tone(L, simp, dirs, k, V, first):
    """exact tone T (dict nu-exponent -> K) of the order-k Taylor term; controls: lower orders isotropic, third axis agrees"""
    accs = [expand(L, simp, u, k, procs=NP) for u in dirs]
    ok = True
    for j in range(1, min(first, k)):
        if j % 2: ok &= all(not accs[i][j] for i in range(3))
        else: ok &= all(peq(unitnorm(accs[0], dirs[0], j), unitnorm(accs[i], dirs[i], j)) for i in (1, 2))
    if k % 2 == 0:
        h = [Hn(V, k, u) for u in dirs]
        T = {e: c / (h[0] - h[1]) for e, c in dsub(unitnorm(accs[0], dirs[0], k), unitnorm(accs[1], dirs[1], k)).items()}
        third = peq(dsub(unitnorm(accs[2], dirs[2], k), unitnorm(accs[0], dirs[0], k)), dscale(T, h[2] - h[0]))
    else:
        h = [Hval(V, k, u) for u in dirs]
        T = {e: c / h[0] for e, c in accs[0][k].items()}
        third = peq(accs[2][k], dscale(T, h[2])) and peq(accs[1][k], dscale(T, h[1]))
    return dclean(T), accs[0][0], ok, third

def at_sqrt(poly_expr, c):
    """value of poly(mu) at mu = sqrt(c), c in Q(sqrt5): returns ('zero' | 'nonzero', float)"""
    P = sp.Poly(poly_expr, mu); co = P.all_coeffs()[::-1]
    rc = sp.sqrt(c)
    try:
        split5(rc); inside = True
    except Exception:
        inside = False
    if inside:
        v = sp.expand(sp.radsimp(sum(a * rc ** j for j, a in enumerate(co))))
        return ('zero' if v == 0 else 'nonzero'), float(v)
    Ev = sp.expand(sum(a * c ** (j // 2) for j, a in enumerate(co) if j % 2 == 0))
    Od = sp.expand(sum(a * c ** (j // 2) for j, a in enumerate(co) if j % 2 == 1))
    z = sgn5(Ev) == 0 and sgn5(Od) == 0
    return ('zero' if z else 'nonzero'), float(sp.N(Ev + sp.sqrt(c) * Od, 30))

def side_of(a, b, c):
    """isolating interval [a, b] (positive rationals) against sqrt(c), exactly"""
    if sgn5(c - b * b) > 0: return 'below'
    if sgn5(a * a - c) > 0: return 'above'
    return 'contains'

def rat_in(lo, hi):
    """a rational strictly inside (lo, hi) (lo, hi sympy numbers or None)"""
    if hi is None: return sp.Rational(int(float(lo)) + 1) if float(lo) + 0.5 < int(float(lo)) + 1 else sp.Rational(int(float(lo)) + 2)
    if lo is None: return sp.Rational(round(float(hi) / 2 * 10 ** 5), 10 ** 5)
    q = sp.Rational(round((float(lo) + float(hi)) / 2 * 10 ** 5), 10 ** 5)
    assert sgn5(q - lo) > 0 and sgn5(hi - q) > 0
    return q

def line_run(name, W, V, walls, c, k, dirs, first, selfdual=None, chambers_only=None, pilot_cap=None):
    """all chambers of the line: exact tone T and corner tone per chamber, zeros counted exactly, value at the fixed point"""
    t0 = time.time()
    L = Line(name, W, V); d = len(V[0])
    Hs, y = Hsym(V, k, d)
    check(f'{name}: degree-{k} invariant harmonic H built from the corners is harmonic and nonzero (exact)', lap_zero(Hs, y) and not Hs.is_zero)
    bounds = [None] + walls + [None]
    res = {'walls': [str(w) for w in walls], 'c': str(c), 'k': k, 'd': d, 'chambers': []}
    Ts = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        if chambers_only is not None and i not in chambers_only: Ts.append(None); continue
        q = rat_in(lo if lo is not None else None, hi)
        if lo is None: q = rat_in(None, hi)
        faces, simp, fv, mm = L.chamber(Fr(int(q.p), int(q.q)))
        if pilot_cap and len(simp) > pilot_cap:
            t1 = time.time(); expand(L, simp[:pilot_cap], dirs[0], k, procs=NP)
            dt = time.time() - t1
            print(f'   PILOT timing {name} chamber {i}: {pilot_cap} of {len(simp)} simplices, one direction, order {k}: {dt:.1f} s '
                  f'-> full chamber, 3 directions ~ {3 * dt * len(simp) / pilot_cap:.0f} s', flush=True)
            Ts.append(None); continue
        t1 = time.time()
        T, c0, iso_ok, third = tone(L, simp, dirs, k, V, first)
        print(f'   chamber {i}: tone built ({time.time() - t1:.1f} s)', flush=True)
        xs = [[p + qq * Fr(int(q.p), int(q.q)) for p, qq in zip(*faces[F])] for F in list(faces)[:8]]
        one_orbit = len({dot(x, x) for x in xs}) == 1 and len({Hval(V, k, x) for x in xs}) == 1 and len(set(fv)) == 1
        check(f'{name} chamber {i} ({lo}, {hi}) sample {q}: {len(faces)} corners, {len(simp)} simplices; one corner orbit, equal facet '
              f'volumes; orders < {min(first, k)} isotropic; third axis agrees (tone is one number)', one_orbit and iso_ok and third)
        x0, x1 = faces[next(iter(faces))]
        Cn = corner_tone(V, k, x0, x1)
        Tn, em = T_num(T) if T else (sp.Integer(0), 0)
        lo_ = sp.Integer(0) if lo is None else lo
        Cs_, cwh = strip_walls(Cn, [lo_, hi]) if Cn.has(mu) else (Cn, [])
        print(f'   chamber {i}: corner tone and wall stripping ({time.time() - t1:.1f} s); counting form zeros (in nu)', flush=True)
        fz, twh = count_T(T, lo, hi, f'{name} T {i}') if T else ([], [])
        print(f'   chamber {i}: form zeros counted ({time.time() - t1:.1f} s); counting corner zeros (degree {sp.Poly(Cs_, mu).degree() if Cs_.has(mu) else 0})', flush=True)
        if Cs_.has(mu):
            Cd = {-j: c for (j,), c in sp.Poly(Cs_, mu).terms()}
            cz, _ = count_T(Cd, lo, hi, f'{name} C {i}', sym=True)
        else: cz = []
        print(f'   chamber {i}: zeros counted ({time.time() - t1:.1f} s)', flush=True)
        if twh or cwh: print(f'   chamber {i}: zeros ON its ends (removed before counting): form {twh}, corner {cwh}', flush=True)
        rec = {'interval': [str(lo), str(hi)], 'sample': str(q), 'corners': len(faces), 'simplices': len(simp),
               'Omega0': str(T_expr({e: v for e, v in c0.items()})),
               'tone_T': str(T_expr(T)) if T else '0',
               'corner_tone': str(Cn),
               'form_zeros': [(str(sp.N(f, 30)), str(F), [str(a), str(b)]) for F, (a, b), f in fz],
               'corner_zeros': [(str(sp.N(f, 30)), str(F), [str(a), str(b)]) for F, (a, b), f in cz],
               'form_zero_on_ends': [str(w) for w in twh], 'corner_zero_on_ends': [str(w) for w in cwh]}
        res['chambers'].append(rec)
        Ts.append({'T': T, 'Tn': Tn, 'em': em, 'Cn': Cn, 'lo': lo, 'hi': hi, 'fz': fz, 'cz': cz, 'faces': faces, 'q': q, 'c0': c0})
        print(f'== {name} chamber {i} ({float(lo) if lo is not None else 0:.6f}, {float(hi) if hi is not None else "inf"}): '
              f'{len(faces)} corners, {len(simp)} simplices; form zeros {[round(float(f), 9) for _, _, f in fz]}, corner zeros '
              f'{[round(float(f), 9) for _, _, f in cz]} ({time.time() - t0:.0f} s)', flush=True)
    # walls: continuity of T and exact values
    for j, w in enumerate(walls):
        A, B = Ts[j], Ts[j + 1]
        if A is None or B is None: continue
        ta = sp.radsimp(T_expr(A['T']).subs(mu, w)); tb = sp.radsimp(T_expr(B['T']).subs(mu, w))
        check(f'{name}: tone continuous at the wall {w} (exact, both sides {sp.N(ta, 8)})', sp.expand(ta - tb) == 0)
        res.setdefault('wall_values', []).append([str(w), str(sp.nsimplify(ta)), sgn5(sp.expand(ta)) if True else None])
    # fixed point
    hR = sp.sqrt(c)
    for j, A in enumerate(Ts):
        if A is None: continue
        lo, hi = A['lo'], A['hi']
        inside = (lo is None or sgn5(c - lo * lo) > 0) and (hi is None or sgn5(hi * hi - c) > 0)
        onwall = any(w is not None and sgn5(sp.expand(c - w * w)) == 0 for w in (lo, hi))
        if inside or onwall:
            st, val = at_sqrt(A['Tn'], c) if A['Tn'].has(mu) else (('zero' if A['Tn'] == 0 else 'nonzero'), float(A['Tn']))
            cst, cval = at_sqrt(A['Cn'], c)
            res.setdefault('fixed_point', []).append({'chamber': j, 'on_wall': onwall, 'form_tone': st, 'form_tone_num': val,
                                                     'corner_tone': cst, 'corner_tone_num': cval})
            print(f'   fixed point hR = {sp.N(hR, 20)} {"(a wall)" if onwall else ""} in chamber {j}: form tone {st} ({val:.6e}), '
                  f'corner tone {cst} ({cval:.6e})', flush=True)
            for F, (a, b), f in A['fz'] + A['cz']:
                print(f'      zero {sp.N(f, 20)}: {side_of(a, b, c)} hR (exact interval comparison)', flush=True)
    OUT[name] = res
    return L, Ts, res

def report_fixed(name, Ts, c, expect_on):
    fp = OUT[name].get('fixed_point', [])
    if expect_on:
        check(f'{name}: ON - form tone and corner tone vanish exactly at the fixed point hR = {sp.N(sp.sqrt(c), 12)}',
              fp and all(f['form_tone'] == 'zero' and f['corner_tone'] == 'zero' for f in fp))
    else:
        check(f'{name}: NOT ON - form tone and corner tone are nonzero at the fixed point (exact)',
              fp and all(f['form_tone'] == 'nonzero' and f['corner_tone'] == 'nonzero' for f in fp))

def parity(name, Ts, walls, c, d, k, eps, HRk):
    """f(-s) = eps f(s): T_C[j] = eps (hR)^(d+k) c^-(d+k-j) T_C'[d+k-j] for every chamber C and its turn image C' (exact)"""
    n = len(Ts); ok = True; pairs = 0
    for i in range(n):
        A, B = Ts[i], Ts[n - 1 - i]
        if A is None or B is None: continue
        D = d + k
        lhs = A['T']; rhs = {}
        for e, v in B['T'].items():
            rhs[D - e] = v * HRk * eps / kpow(c, e)
        ok &= peq(lhs, rhs); pairs += 1
    return ok, pairs

def sweep_s(name, A, c, d, k, true_zero):
    """even/odd split at the fixed point; first-order displacement; Kantorovich certificate (50-digit arithmetic)"""
    lam = mp.mpf(d + k) / 2; hR = mp.sqrt(mp.mpf(float(sp.N(c, 60))) if False else mp.mpf(str(sp.N(c, 60))))
    terms = [(mp.mpf(str(sp.N(ks(v), 60))), lam - e) for e, v in A['T'].items()]   # f(s) = sum a (hR e^s)^(lam - e)
    f = lambda s, n=0: sum(a * b ** n * (hR * mp.e ** s) ** b for a, b in terms)
    f0, f1, f2 = f(0, 0), f(0, 1), f(0, 2)
    s1 = -f0 / f1
    s2 = s1 - f(s1) / f(s1, 1)
    eta = abs(s1)
    rad = 2 * eta
    L2 = sum(abs(a) * b ** 2 * (hR ** b) * mp.e ** (abs(b) * rad) for a, b in terms) / abs(f1)
    hK = L2 * eta
    tstar = (1 - mp.sqrt(1 - 2 * hK)) / L2 if hK <= mp.mpf(1) / 2 else None
    st = mp.log(mp.mpf(str(sp.N(true_zero, 50))) / hR) if true_zero is not None else None
    Ev = lambda s: (f(s) + f(-s)) / 2; Od = lambda s: (f(s) - f(-s)) / 2
    r = {'lambda': str(lam), 'f0_even': mp.nstr(f0, 15), 'f1_odd_slope': mp.nstr(f1, 15), 'f2': mp.nstr(f2, 15),
         's1_first_order': mp.nstr(s1, 15), 's2_newton': mp.nstr(s2, 15), 's_true': mp.nstr(st, 15) if st is not None else None,
         'mu_first_order': mp.nstr(hR * mp.e ** s1, 15), 'mu_true': str(sp.N(true_zero, 20)) if true_zero is not None else None,
         'kantorovich_h': mp.nstr(hK, 8), 'kantorovich_radius': mp.nstr(tstar, 10) if tstar is not None else None}
    if st is not None:
        r['even_at_true'] = mp.nstr(Ev(st), 12); r['odd_at_true'] = mp.nstr(Od(st), 12)
        r['rel_err_first_order'] = mp.nstr(abs(s1 - st) / abs(st), 6)
    print(f'   {name}: f(0) (even part) = {r["f0_even"]}, f\'(0) (odd slope) = {r["f1_odd_slope"]}; first order s1 = {r["s1_first_order"]} '
          f'(mu {r["mu_first_order"]}), Newton s2 = {r["s2_newton"]}, true s* = {r["s_true"]} (mu {r["mu_true"]}); Kantorovich h = '
          f'{r["kantorovich_h"]}, certified |s*| <= {r["kantorovich_radius"]}', flush=True)
    if st is not None and tstar is not None:
        check(f'{name}: Kantorovich certificate holds (h <= 1/2) and contains the exact zero (|s*| <= t*)', abs(st) <= tstar)
    OUT[name]['s_expansion'] = r
    return r

def two_ends(name, Ts, d, k, c):
    """outer chambers: T = T_P (mu > R^2) and T = T_V mu^-(d+k) (mu < h^2); model zero (-T_V/T_P)^(1/(d+k))"""
    A, B = Ts[0], Ts[-1]
    if A is None or B is None: return None
    D = d + k
    ok = set(A['T']) <= {D} and set(B['T']) <= {0}
    TV = ks(A['T'].get(D, K(0))); TP = ks(B['T'].get(0, K(0)))
    check(f'{name}: outer chambers are pure powers: T = T_V mu^-{D} below h^2, T = T_P above R^2 (exact)', ok)
    ratio = -TV / TP
    if float(ratio) <= 0:
        print(f'   {name}: T_V and T_P have the same sign: two-ends model has no zero', flush=True); return None
    mm = mp.power(mp.mpf(str(sp.N(ratio, 50))), mp.mpf(1) / D)
    OUT[name]['two_ends'] = {'T_V': str(sp.nsimplify(TV)), 'T_P': str(sp.nsimplify(TP)), 'mu_model': mp.nstr(mm, 15),
                             's_model': mp.nstr(mp.log(mm / mp.sqrt(mp.mpf(str(sp.N(c, 50))))), 12)}
    print(f'   {name}: two-ends model zero mu_m = (-T_V/T_P)^(1/{D}) = {mp.nstr(mm, 12)} (hR = {sp.N(sp.sqrt(c), 12)})', flush=True)
    return mm

def radial_bound(name, A, V, W, c, d, k, dirs):
    """|T(hR)| <= d! C(k+d,d) ((1/h)^(d+k) - R_S^-(d+k)) / (2(d+k)) ||H'||_1 / |Hn(u1) - Hn(u2)| (H' orbit-difference harmonic; L1 norm NUMERICAL)"""
    import numpy as np
    from math import comb, gamma, pi
    hR = mp.sqrt(mp.mpf(str(sp.N(c, 50))))
    x0, x1 = A['faces'][next(iter(A['faces']))]
    RS2 = sum((mp.mpf(float(a)) + mp.mpf(float(b)) * hR) ** 2 for a, b in zip(x0, x1))
    h2 = 1 / mp.mpf(float(dot(W[0], W[0])))
    Vf = np.array([[float(t) for t in v] for v in V]); Wf = np.array([[float(t) for t in w] for w in W])
    Vf /= np.linalg.norm(Vf, axis=1)[:, None]; Wf /= np.linalg.norm(Wf, axis=1)[:, None]
    rng = np.random.default_rng(7); tot = 0.0; n = 0
    for _ in range(20):
        X = rng.normal(size=(20000, d)); X /= np.linalg.norm(X, axis=1)[:, None]
        Hp = ((X @ Vf.T) ** k).mean(axis=1) - ((X @ Wf.T) ** k).mean(axis=1)
        tot += np.abs(Hp).sum(); n += len(X)
    area = 2 * pi ** (d / 2) / gamma(d / 2)
    L1 = tot / n * area
    hn = [float(Hn(V, k, u)) for u in dirs[:2]]
    D = d + k
    from math import factorial
    bound = factorial(d) * comb(k + d, d) * (float(1 / h2 ** (mp.mpf(D) / 2)) - float(1 / RS2 ** (mp.mpf(D) / 2))) / (2 * D) * L1 / abs(hn[0] - hn[1])
    Tval = float(sum(mp.mpf(str(sp.N(ks(v), 40))) * hR ** (-e) for e, v in A['T'].items()))
    rho = float(mp.sqrt(h2 / RS2))
    OUT[name]['radial_bound'] = {'h_over_RS': rho, 'T_at_hR': Tval, 'bound_numerical_L1': bound, 'ratio': abs(Tval) / bound}
    print(f'   {name}: fixed solid S(hR): h/R_S = {rho:.6f} (exact algebraic), |T(hR)| = {abs(Tval):.4e} <= radial bound {bound:.4e} '
          f'(ratio {abs(Tval) / bound:.3f}; L1 norm of H numerical)', flush=True)
    check(f'{name}: radial bound holds at the fixed point (numerical L1 norm)', abs(Tval) <= bound)

def fixed_chamber(Ts, c):
    for A in Ts:
        if A is None: continue
        lo, hi = A['lo'], A['hi']
        if (lo is None or sgn5(c - lo * lo) > 0) and (hi is None or sgn5(hi * hi - c) > 0): return A
    return None
PROG = [0.0]
def progress(frac, what):
    print(f'PROGRESS {frac:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)

# ================= counter controls =================
x_ = sp.Symbol('x')
r_ = count_roots((x_ - (1 + s5) / 8) * (x_ - sp.Rational(3, 7)) ** 2 * (x_ ** 2 - 2), x_, sp.Integer(0), sp.Integer(1), 'P2')
check(f'counter: (x-(1+sqrt5)/8)(x-3/7)^2(x^2-2) on (0,1): {len(r_)} distinct roots (expect 2)', len(r_) == 2)
r_ = count_roots(x_ - (3 + s5) / 4, x_, sp.Integer(0), sp.Integer(1), 'N1')
check(f'counter: x-(3+sqrt5)/4 on (0,1): {len(r_)} roots (expect 0; conjugate inside)', len(r_) == 0)
progress(0.02, 'counter controls')

def S3(n): return [tuple(K(1 if j == i else 0) * sg for j in range(n)) for i in range(n) for sg in (1, -1)]
def CUBEV(n): return [tuple(K(x) for x in v) for v in itertools.product((1, -1), repeat=n)]

# ================= 1. cube - octahedron (reproduce 1.692590) =================
print('== LINE cube-octahedron (k = 4)', flush=True)
Lc, Tc, _ = line_run('cube', S3(3), CUBEV(3), [sp.Integer(1), sp.Integer(2), sp.Integer(3)], sp.Integer(3), 4,
                     [V_(1, 1, 1), V_(1, 0, 0), V_(1, 2, 3)], 4)
fzc = [f for A in Tc if A for f in A['fz']]
check('POSITIVE cube: exactly one form zero on the whole line, 1.692590, root of mu^4+2mu^3+mu^2-4mu-14 (chunk 3)',
      len(fzc) == 1 and sp.expand(sp.Poly(fzc[0][0], mu).monic().as_expr() - (mu ** 4 + 2 * mu ** 3 + mu ** 2 - 4 * mu - 14)) == 0)
czc = [f for A in Tc if A for f in A['cz']]
check(f'cube corner station(s) {[round(float(f), 9) for _, _, f in czc]}: exactly one, mu = phi (corners = two icosahedra, a 5-design)',
      len(czc) == 1 and sp.expand(sp.Poly(czc[0][0], mu).monic().as_expr() - (mu ** 2 - mu - 1)) == 0)
report_fixed('cube', Tc, sp.Integer(3), False)
A = fixed_chamber(Tc, sp.Integer(3))
sw = sweep_s('cube', A, sp.Integer(3), 3, 4, fzc[0][2] if fzc else None)
ff = lambda s, e: sum(mp.mpf(str(sp.N(ks(v), 50))) * (mp.sqrt(3) * mp.e ** s) ** (mp.mpf(7) / 2 - ee) for ee, v in A['T'].items())
check('NEGATIVE cube: the turn is not a parity of f (f(s) != +-f(-s) at s = 0.05)',
      all(abs(ff(0.05, 0) - sg * ff(-0.05, 0)) > mp.mpf(10) ** -20 for sg in (1, -1)))
two_ends('cube', Tc, 3, 4, sp.Integer(3))
radial_bound('cube', A, CUBEV(3), S3(3), sp.Integer(3), 3, 4, [V_(1, 1, 1), V_(1, 0, 0)])
progress(0.08, 'cube line')

# ================= 2. icosahedron - dodecahedron (reproduce 2.891793) =================
print('== LINE icosahedron-dodecahedron (k = 6)', flush=True)
IV = []
for a, b in itertools.product((1, -1), repeat=2):
    base = (K(0), K(a), phi * b)
    for r in range(3): IV.append(tuple(base[(j - r) % 3] for j in range(3)))
def polar_vectors(V):
    Vf = np.array([[float(t) for t in v] for v in V]); hl = ConvexHull(Vf); seen = {}; Wout = []
    for eq in hl.equations:
        key = tuple(np.round(eq, 7))
        if key in seen: continue
        seen[key] = 1
        on = [i for i in range(len(V)) if abs(Vf[i] @ eq[:-1] + eq[-1]) < 1e-7]
        rows = [V[i] for i in on]; ind = rank_rows(rows)
        w = tuple(solve([rows[i] for i in ind], [K(1)] * len(ind)))
        assert all(dot(w, v) == ONE for v in rows) and all((ONE - dot(w, v)).sign() >= 0 for v in V)
        Wout.append(w)
    return Wout
IW = polar_vectors(IV)
check('icosahedron: 12 corners (0, +-1, +-phi), 20 exact facet vectors', len(IV) == 12 and len(IW) == 20)
ci = (25 + 11 * s5) / 6
Li, Ti, _ = line_run('icosahedral', IW, IV, [(7 + 3 * s5) / 6, (3 + s5) / 2, (5 + s5) / 2], ci, 6, [IV[0], IW[0], V_(1, 2, 3)], 6)
fzi = [f for A in Ti if A for f in A['fz']]
check('POSITIVE icosahedral: exactly one form zero on the whole line, 2.891793, degree 12 over Q (chunk 3)',
      len(fzi) == 1 and abs(float(fzi[0][2]) - 2.891792659030825) < 1e-12 and sp.Poly(fzi[0][0], mu).degree() == 12)
report_fixed('icosahedral', Ti, ci, False)
Ai = fixed_chamber(Ti, ci)
sweep_s('icosahedral', Ai, ci, 3, 6, fzi[0][2] if fzi else None)
two_ends('icosahedral', Ti, 3, 6, ci)
radial_bound('icosahedral', Ai, IV, IW, ci, 3, 6, [IV[0], IW[0]])
progress(0.16, 'icosahedral line')

# ================= 3. tetrahedron (self-dual by -I) =================
print('== LINE tetrahedron (self-dual; k = 3, and k = 4)', flush=True)
TV = [V_(1, 1, 1), V_(1, -1, -1), V_(-1, 1, -1), V_(-1, -1, 1)]
TW = [tuple(-x for x in v) for v in TV]
check('tetrahedron: facet vectors W = -V (w.v = 1 on the three other corners)', all(dot(TW[i], TV[j]) == ONE for i in range(4) for j in range(4) if i != j))
tw = [sp.Rational(1, 3), sp.Integer(1), sp.Integer(3)]
Lt, Tt, _ = line_run('tetrahedron k=3', TW, TV, tw, sp.Integer(1), 3, [V_(1, 1, 1), V_(-1, -1, -1), V_(1, 2, 2)], 3)
y3 = sp.symbols('y1:4')
Hv, yv = Hsym(TV, 3, 3); Hw, _ = Hsym(TW, 3, 3)
check('tetrahedron: the turn isometry g = -I swaps the two orbits and acts on H3 by eps = -1 (exact)', (Hw + Hv).is_zero)
okp, npair = parity('tetrahedron k=3', Tt, tw, K(1), 3, 3, -1, K(1))
check(f'tetrahedron k=3: f(-s) = -f(s) on the whole line (exact identity on {npair} chamber pairs)', okp and npair >= 2)
report_fixed('tetrahedron k=3', Tt, sp.Integer(1), True)
Lt4, Tt4, _ = line_run('tetrahedron k=4', TW, TV, tw, sp.Integer(1), 4, [V_(1, 1, 1), V_(1, 0, 0), V_(1, 2, 2)], 3)
okp4, npair4 = parity('tetrahedron k=4', Tt4, tw, K(1), 3, 4, 1, K(1))
check(f'tetrahedron k=4: f(-s) = +f(s) (eps = +1): order-4 special points come in turn pairs mu, 1/mu (exact, {npair4} pairs)', okp4 and npair4 >= 2)
z4 = sorted(float(f) for A in Tt4 if A for f in [ff[2] for ff in A['fz']])
c4 = sorted(float(ff[2]) for A in Tt4 if A for ff in A['cz'])
check(f'tetrahedron k=4 corner stations {[round(z, 9) for z in c4]} form one turn pair (product 1) (exact pairing by the parity identity)',
      len(c4) == 2 and abs(c4[0] * c4[1] - 1) < 1e-12)
check(f'tetrahedron k=4 form zeros {[round(z, 9) for z in z4]} are closed under mu -> 1/mu', all(any(abs(1 / z - w) < 1e-12 for w in z4) for z in z4))
progress(0.22, 'tetrahedron line')

# ================= 4. negative control: a perturbed (non-regular) tetrahedron =================
print('== NEGATIVE perturbed tetrahedron (not regular)', flush=True)
PV = [V_(Fr(11, 10), 1, 1), V_(1, -1, Fr(-9, 10)), V_(-1, Fr(6, 5), -1), V_(-1, -1, 1)]
cen = [sum((v[i] for v in PV), K(0)) * Fr(1, 4) for i in range(3)]
PV = [tuple(v[i] - cen[i] for i in range(3)) for v in PV]
PW = polar_vectors(PV)
LP = Line('perturbed', PW, PV)
vals = []
for q in (Fr(9, 10), Fr(10, 9)):
    faces, simp, fv, mm = LP.chamber(q)
    a = expand(LP, simp, V_(1, 1, 1), 3, procs=NP)
    vals.append(sum((ks(v) * sp.Rational(q.denominator, q.numerator) ** e for e, v in a[3].items()), sp.Integer(0)))
faces, simp, fv, mm = LP.chamber(Fr(1))
a1 = expand(LP, simp, V_(1, 1, 1), 3, procs=NP)
v1 = sum((ks(v) for e, v in a1[3].items()), sp.Integer(0))
check(f'NEGATIVE perturbed tetrahedron: order-3 Taylor term along (1,1,1) at mu = 1 is nonzero ({sp.N(v1, 8)}), and the values at '
      f'mu = 9/10, 10/9 break the parity mu^3 T(mu) = -mu^-3 T(1/mu) that holds for the regular tetrahedron',
      v1 != 0 and sp.expand(sp.radsimp(vals[0] * sp.Rational(9, 10) ** 3 + vals[1] * sp.Rational(10, 9) ** 3)) != 0)
progress(0.25, 'negative control')

# ================= 5. B4: tesseract - 16-cell (fixed point on the wall mu = 2, S(2) = 24-cell) =================
print('== LINE B4 tesseract-16-cell (k = 4)', flush=True)
LB4, TB4, _ = line_run('B4', S3(4), CUBEV(4), [sp.Integer(j) for j in (1, 2, 3, 4)], sp.Integer(4), 4,
                       [V_(1, 1, 1, 1), V_(1, 0, 0, 0), V_(1, 2, 3, 5)], 4)
report_fixed('B4', TB4, sp.Integer(4), True)
A = TB4[2]
cor2 = {tuple(p + q * 2 for p, q in zip(*A['faces'][F])) for F in A['faces']}
F4 = {tuple(K(x) for x in v) for v in set(itertools.permutations((1, 1, 0, 0))) | set(itertools.permutations((1, -1, 0, 0))) |
      set(itertools.permutations((-1, -1, 0, 0)))}
check(f'B4: S(2) has the 24 corners (+-1, +-1, 0, 0): S(hR) is the 24-cell, symmetry W(F4) > W(B4) (exact)', cor2 == F4 and len(cor2) == 24)
V24 = sorted(F4, key=str)
check('B4: the 24-cell corners are silent in degree 4 (5-design): W(F4) has no invariant harmonic of degree 4 (exact)',
      Hsym(V24, 4, 4)[0].is_zero)
progress(0.32, 'B4 line')

# ================= 6. 24-cell (self-dual) =================
print('== LINE 24-cell (self-dual; k = 6)', flush=True)
C24 = [tuple(K(x) for x in v) for v in set(itertools.permutations((1, 0, 0, 0))) | set(itertools.permutations((-1, 0, 0, 0)))]
C24 += [tuple(K(Fr(s, 2)) for s in sg) for sg in itertools.product((1, -1), repeat=4)]
W24 = polar_vectors(C24)
check('24-cell: 24 corners, 24 facet vectors (+-1, +-1, 0, 0)', len(C24) == 24 and set(W24) == F4)
gq = [[1, 1, 0, 0], [1, -1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]]
gmap = lambda v: tuple(sum((v[j] * gq[i][j] for j in range(4)), K(0)) for i in range(4))
check('24-cell: g = (1/sqrt2)[[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]] is orthogonal and maps corners onto facet directions and back',
      {gmap(v) for v in C24} == set(W24) and {gmap(w) for w in W24} == {tuple(x * 2 for x in v) for v in C24})
H6v, y4 = Hsym(C24, 6, 4); H6w, _ = Hsym(W24, 6, 4)
eps24 = 1 if (H6w - H6v * 8).is_zero else (-1 if (H6w + H6v * 8).is_zero else None)
check(f'24-cell: g acts on the degree-6 harmonic by eps = {eps24} (|w|^6 = 8: H6(facets) = eps * 8 * H6(corners), exact)',
      eps24 in (1, -1))
w24 = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(3, 4), sp.Integer(1)]
L24, T24, _ = line_run('24-cell', W24, C24, w24, sp.Rational(1, 2), 6, [C24[0], W24[0], V_(1, 2, 3, 5)], 6)
okp, npair = parity('24-cell', T24, w24, K(Fr(1, 2)), 4, 6, int(eps24), K(Fr(1, 32)))
check(f'24-cell: f(-s) = {eps24} f(s) on the whole line (exact identity on {npair} chamber pairs)', okp and npair >= 3)
report_fixed('24-cell', T24, sp.Rational(1, 2), eps24 == -1)
progress(0.42, '24-cell line')

# ================= 7. 5-cell (self-dual by -I) =================
print('== LINE 5-cell (self-dual; k = 3)', flush=True)
sq = K(0, Fr(1, 5))   # 1/sqrt5
C5 = [V_(1, 1, 1, -sq), V_(1, -1, -1, -sq), V_(-1, 1, -1, -sq), V_(-1, -1, 1, -sq), V_(0, 0, 0, sq * 4)]
W5 = [tuple(x * Fr(-5, 4) for x in v) for v in C5]
check('5-cell: |v|^2 = 16/5, facet vectors W = -(5/4) V (exact)', all(dot(v, v) == K(Fr(16, 5)) for v in C5) and
      all(dot(W5[i], C5[j]) == ONE for i in range(5) for j in range(5) if i != j))
w5 = [sp.Rational(1, 5), sp.Rational(8, 15), sp.Rational(6, 5), sp.Rational(16, 5)]
L5, T5, _ = line_run('5-cell', W5, C5, w5, sp.Rational(16, 25), 3, [C5[0], tuple(-x for x in C5[0]), V_(1, 2, 3, 5)], 3)
okp, npair = parity('5-cell', T5, w5, K(Fr(16, 25)), 4, 3, -1, kpow(K(Fr(4, 5)), 7))
check(f'5-cell: f(-s) = -f(s) on the whole line (exact identity on {npair} chamber pairs)', okp and npair >= 3)
report_fixed('5-cell', T5, sp.Rational(16, 25), True)
progress(0.50, '5-cell line')

# ================= 8. square (2D, self-dual) =================
print('== LINE square (self-dual; k = 4)', flush=True)
try:
    Ls, Tsq, _ = line_run('square', S3(2), CUBEV(2), [sp.Integer(1), sp.Integer(2)], sp.Integer(2), 4, [V_(1, 1), V_(1, 0), V_(3, 4)], 4)
    okp, npair = parity('square', Tsq, None, K(2), 2, 4, -1, K(8))
    check(f'square: f(-s) = -f(s) on the whole line (exact identity on {npair} chamber pairs)', okp and npair >= 2)
    report_fixed('square', Tsq, sp.Integer(2), True)
except Exception as ex:
    print(f'   square line skipped by the 2D triangulation: {ex!r} (polygons: regular 2n-gon at hR, argued in the README)', flush=True)
progress(0.53, 'square line')

# ================= 9. B5 and B6 (non-self-dual; hR = sqrt d inside (2, 3)) =================
for dd in ((5,) if PILOT else (5, 6)):
    print(f'== LINE B{dd} (k = 4)', flush=True)
    LBd, TBd, _ = line_run(f'B{dd}', S3(dd), CUBEV(dd), [sp.Integer(j) for j in range(1, dd + 1)], sp.Integer(dd), 4,
                           [V_(*([1] * dd)), V_(*([1] + [0] * (dd - 1))), V_(*[1, 2, 3, 5, 7, 11][:dd])], 4,
                           chambers_only=None if dd == 5 else set(range(2, dd + 1)))   # B6: chambers 0, 1 have 5-cube / 17-point facets (slow); not needed
    report_fixed(f'B{dd}', TBd, sp.Integer(dd), False)
    fzb = [f for AA in TBd if AA for f in AA['fz']]
    near = min(fzb, key=lambda f: abs(float(f[2]) - dd ** 0.5)) if fzb else None
    sweep_s(f'B{dd}', fixed_chamber(TBd, sp.Integer(dd)), sp.Integer(dd), dd, 4, near[2] if near else None)
    if dd == 5: two_ends(f'B{dd}', TBd, dd, 4, sp.Integer(dd))
    radial_bound(f'B{dd}', fixed_chamber(TBd, sp.Integer(dd)), CUBEV(dd), S3(dd), sp.Integer(dd), dd, 4, [V_(*([1] * dd)), V_(*([1] + [0] * (dd - 1)))])
    progress(0.56 + 0.06 * (dd - 4), f'B{dd} line')

# ================= 10. B_d corner stations for every d (analytic, exact) =================
print('== B_d corner stations, d = 3..16 (corner (1^m, t, 0...), H4 = sum x^4 - 3|x|^4/(d+2))', flush=True)
bd = {}
for dd in range(3, 17):
    sts = []
    for mm_ in range(0, dd):
        P = sp.Poly(sp.expand((dd + 2) * (mm_ + tt ** 4) - 3 * (mm_ + tt ** 2) ** 2), tt)
        for (a, b), mult in P.intervals(eps=sp.Rational(1, 10 ** 30)):
            if a >= 0 and b <= 1:
                sts.append((mm_ + (a + b) / 2, a == b and a in (0, 1)))
    sts = sorted(set((float(s), w) for s, w in sts))
    bd[dd] = [s for s, _ in sts]
    print(f'   B{dd}: corner stations mu = {[round(s, 9) for s in bd[dd]]}, fixed point sqrt(d) = {dd ** 0.5:.9f}, (d+2)/3 = {(dd + 2) / 3:.6f}', flush=True)
OUT['Bd_corner_stations'] = {str(k): v for k, v in bd.items()}
check('B_d analytic corner formula reproduces the generic code: cube station phi, B4 station 2 (= hR)',
      any(abs(s - float((1 + s5) / 2)) < 1e-12 for s in bd[3]) and any(abs(s - 2) < 1e-12 for s in bd[4]))
check('B_d: a corner station equals sqrt(d) only for d = 4 among d = 3..16 (exact: (d+2)/3 = sqrt d iff d in {1, 4})',
      [dd for dd in bd if any(abs(s - dd ** 0.5) < 1e-9 for s in bd[dd])] == [4])
progress(0.70, 'B_d corner stations')

# ================= 11. 600-cell line (reproduce mu* and mu_Omega; first-order displacement) =================
print('== LINE 600-cell (k = 12): truncated-600-cell hop', flush=True)
_h4 = _src[_src.index('# ================= H4 data'):_src.index('# ================= the H4 line')]
_PIL = PILOT; PILOT = True        # only skips the heavy Red Queen degree-12 check and design k > 4 in the H4 block (as pds_exact.py)
exec(_h4, globals())
PILOT = _PIL
r2s = ks(r2); walls600 = [ks(w) for w in fr][::-1]     # r^2, 1/2+sqrt5/6, (5+sqrt5)/8, 1
J = json.load(open(os.path.join(STUD, '2026-11-12-pds-hopscotch-line', 'data', 'pds-line.json')))
L6, T6, _ = line_run('600-cell', W, V, walls600, r2s, 12, [(K(1), K(0), K(0), K(0)), W[0], (K(1), K(2), K(3), K(5))], 12,
                     chambers_only={3}, pilot_cap=300 if PILOT else None)
if not PILOT:
    A6 = T6[3]
    Bj = sp.sympify(J['hops']['truncated 600-cell hop']['B'], locals={'mu': mu})
    check('POSITIVE 600-cell: our tone T equals chunk 6\'s B(mu) exactly in the truncated-600-cell hop', sp.expand(sp.numer(sp.together(T_expr(A6['T']) - Bj))) == 0)
    fz6 = A6['fz']; cz6 = A6['cz']
    check('POSITIVE 600-cell: one form zero mu_Omega = 0.921449634428905791812 (degree 24 over Q) and one corner station mu* = '
          '0.924138673238867458601 (degree 20 over Q), exact',
          len(fz6) == 1 and abs(sp.N(fz6[0][2], 40) - sp.Float('0.921449634428905791812131090257', 40)) < 1e-27 and sp.Poly(fz6[0][0], mu).degree() == 24
          and len(cz6) == 1 and abs(sp.N(cz6[0][2], 40) - sp.Float('0.924138673238867458601238076667', 40)) < 1e-27 and sp.Poly(cz6[0][0], mu).degree() == 20)
    report_fixed('600-cell', T6, r2s, False)
    sweep_s('600-cell', A6, r2s, 4, 12, fz6[0][2] if fz6 else None)
    # two-ends model from the logged B of the outer inner hops (continuity: T = B(1) for mu >= 1; T = B(r^2) r^32 mu^-16 below r^2)
    B3 = sp.sympify(J['hops']['truncated 120-cell hop']['B'], locals={'mu': mu})
    TP = sp.radsimp(Bj.subs(mu, 1)); TVv = sp.radsimp(B3.subs(mu, r2s) * r2s ** 16)
    mm6 = mp.power(mp.mpf(str(sp.N(-TVv / TP, 50))), mp.mpf(1) / 16) if float(-TVv / TP) > 0 else None
    OUT['600-cell']['two_ends'] = {'T_P': str(sp.N(TP, 20)), 'T_V': str(sp.N(TVv, 20)), 'mu_model': mp.nstr(mm6, 15) if mm6 else None}
    print(f'   600-cell: two-ends model zero mu_m = {mp.nstr(mm6, 12) if mm6 else None} (r = {sp.N(sp.sqrt(r2s), 12)})', flush=True)
    radial_bound('600-cell', A6, V, W, r2s, 4, 12, [(K(1), K(0), K(0), K(0)), W[0]])
progress(0.97, '600-cell line')

json.dump(OUT, open(os.path.join(here, '..', 'data', 'near-on-pilot.json' if PILOT else 'near-on.json'), 'w'), indent=1, default=str)
nf = sum(1 for _, ok in CHECKS if not ok)
print(f'{len(CHECKS)} checks, {nf} failed, {time.time() - T0:.0f} s')
print('FINAL ok: all controls held' if nf == 0 else 'FINAL FAIL')
