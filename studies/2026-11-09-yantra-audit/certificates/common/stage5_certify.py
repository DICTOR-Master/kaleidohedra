"""Stage 5: the certificate of Theorem 9 (case D) / Theorem 10 (case K).
usage: python -u stage5_certify.py D|K [digits]
(1) Interval Newton (Krawczyk test, mpmath interval arithmetic at `digits` digits): the square system G = H1 = D = 0 of stage 4
    in the unknowns (u, t, S) has EXACTLY ONE solution X* in a box of radius 10^-(digits-40) around the numerical point.
(2) Elimination identities: R1 = Res_S(G, H1) and R2 = Res_S(G, D) vanish at X* (a resultant is a polynomial combination of its
    two arguments); so do their norms N1, N2 (case D). Every factor of N1 (N2) except the kept one, a (b), is shown NONZERO on
    the box by interval evaluation, so a(t*, u*) = b(t*, u*) = 0; hence R = Res_t(a, b) vanishes at u*. Every factor of R
    except f is shown to have NO real root in the rational isolating interval [a40, b40] of stage 1 (PARI polsturm, exact);
    the box's u-range lies inside that interval; so f(u*) = 0 and u* is THE root u0 of f isolated in stage 1.
(3) The solution is the yantra: from (u*, t*, S*) the whole yantra is rebuilt by model.solve in interval arithmetic (every
    division checked to have a divisor interval excluding 0, so every divisor is nonzero); the closing equation holds since H1
    does and the cleared denominators and dropped factors are nonzero; (b) holds by the circle parametrisation, (c) by G, (d)
    by D together with the sign conditions that undo the squaring; every Huet condition then holds exactly by the stage-2 lemma;
    the order and admissibility inequalities hold strictly (corners on the circle are exact); the slope condition is built in
    (v = u, resp. v = (2 sqrt5 - 4)/u). The rebuilt numbers agree with the paper's stored values.
Writes stage5-<case>.json (interval enclosures of every coordinate, for the piece counts) and FINAL ok / FINAL FAIL."""
import sys, json, time, io, contextlib
from fractions import Fraction as Fr
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
case = sys.argv[1]; DIG = int(sys.argv[2]) if len(sys.argv) > 2 else 520
import mpmath as mp
from mpmath import iv
mp.mp.dps = DIG + 20; iv.dps = DIG + 20
from sage.all__sagemath_singular import QQ, PolynomialRing
Rg = PolynomialRing(QQ, 'w,u,t,S'); W, U, Tt, SS = Rg.gens()
sysd = dict(l.split(' = ', 1) for l in open(f'stage4-{case}-system.txt').read().strip().split('\n'))
G, H1, D = (Rg(sysd[k]) for k in ('G', 'H1', 'D'))
ok = True
def check(c, msg):
    global ok
    say(('ok   ' if c else 'FAIL ') + msg); ok = ok and bool(c)
def compile_poly(F):
    return [(e, Fr(int(c.numerator()), int(c.denominator()))) for e, c in F.dict().items()]
def evalp(cp, vals, num):
    """vals = (w, u, t, S); num = mp or iv module"""
    tot = num.mpf(0)
    pw = [dict() for _ in range(4)]
    for e, c in cp:
        term = num.mpf(c.numerator) / c.denominator
        for k in range(4):
            if e[k]:
                if e[k] not in pw[k]: pw[k][e[k]] = vals[k] ** e[k]
                term = term * pw[k][e[k]]
        tot = tot + term
    return tot
eqs = [compile_poly(F) for F in (G, H1, D)]
jac = [[compile_poly(F.derivative(x)) for x in (U, Tt, SS)] for F in (G, H1, D)]
st1 = json.load(open(f'stage1-{case}.json'))
stored = {'K': {'t1b': '0.103270075308203946272572702702691751496327239362942147553129', 'S': '0.920060145909595975294968707108293454053174101126889036281854',
                'Q': '0.550705232975448904641094020607886607493801159518652756832912'},
          'D': {'t1b': '0.04397772610421809944376588907842364688956', 'S': '0.9682686074586943741422847787587545440601',
                'Q': '0.576510321707840427511505969737023869726'}}[case]
w5 = mp.sqrt(5)
lo = lambda z: mp.make_mpf(z._mpi_[0]); hi = lambda z: mp.make_mpf(z._mpi_[1]); mid = lambda z: (lo(z) + hi(z)) / 2
F = lambda uu, tt, s: [evalp(e, (w5, uu, tt, s), mp) for e in eqs]
b1s = mp.mpf(stored['t1b'])
x0 = mp.findroot(F, (mp.mpf(st1['u_1000_digits'][:DIG + 10]), mp.sqrt(b1s / (1 - b1s)), mp.mpf(stored['S'])), tol=mp.mpf(10)**(-DIG), maxsteps=100)
x0 = [x0[i] for i in range(3)]
say('Newton point found; residuals', [mp.nstr(abs(r), 3) for r in F(*x0)])
# (1) Krawczyk
rad = mp.mpf(10) ** (-(DIG - 40))
X = [iv.mpf([x - rad, x + rad]) for x in x0]
w5i = iv.sqrt(5)
xt = [iv.mpf(x) for x in x0]
Fx = [evalp(e, (w5i, *xt), iv) for e in eqs]
J0 = mp.matrix([[evalp(jac[i][j], (w5, *x0), mp) for j in range(3)] for i in range(3)])
Y = J0 ** -1
JX = [[evalp(jac[i][j], (w5i, *X), iv) for j in range(3)] for i in range(3)]
Kr = []
for i in range(3):
    s = xt[i] - sum((iv.mpf(Y[i, j]) * Fx[j] for j in range(3)), iv.mpf(0))
    for k in range(3):
        m = (iv.mpf(1) if i == k else iv.mpf(0)) - sum((iv.mpf(Y[i, j]) * JX[j][k] for j in range(3)), iv.mpf(0))
        s = s + m * (X[k] - xt[k])
    Kr.append(s)
inside = all(Kr[i].a > X[i].a and Kr[i].b < X[i].b for i in range(3))
check(inside, f'Krawczyk: K(X) lies inside the box X (radius 1e-{DIG - 40}), so G = H1 = D = 0 has exactly one solution X* in X')
Xb = [iv.mpf([max(Kr[i].a, X[i].a), min(Kr[i].b, X[i].b)]) for i in range(3)]   # X* lies in K(X) and in X
uI, tI, SI = Xb
# (2) elimination chain
def factors_of(path, tag):
    out = []
    for l in open(path):
        if l.startswith(tag + ' factor'):
            out.append(Rg(l.split('): ', 1)[1]))
    return out
kept = dict(l.split(' = ', 1) for l in open(f'stage4-{case}-kept.txt').read().strip().split('\n'))
for tag, kk in (('N1', 'a'), ('N2', 'b')):
    fl = factors_of(f'stage4-{case}.txt', tag); kp = Rg(kept[kk])
    nz = 0; kept_seen = False
    for fac in fl:
        val = evalp(compile_poly(fac), (w5i, uI, tI, SI), iv)
        if fac == kp:
            kept_seen = True; check(val.a <= 0 <= val.b, f'{tag}: the kept factor {kk} (degrees t {fac.degree(Tt)}, u {fac.degree(U)}) contains 0 on the box (consistent)')
        else:
            if val.a > 0 or val.b < 0: nz += 1
            else: check(False, f'{tag}: a dropped factor (degrees t {fac.degree(Tt)}, u {fac.degree(U)}) is not certified nonzero')
    check(kept_seen and nz == len(fl) - 1, f'{tag}: all {nz} dropped factors certified nonzero on the box, so {kk}(t*, u*) = 0')
import cypari2
pari = cypari2.Pari(); pari.allocatemem(8 * 10**9)
A40, B40 = (Fr(x) for x in st1['interval40'])
check(uI.a > iv.mpf(A40.numerator) / A40.denominator and uI.b < iv.mpf(B40.numerator) / B40.denominator,
      'the u-range of the box lies inside the isolating interval [a40, b40] of f')
f = pari(open({'D': 'dicto-yantra-exact-u.txt', 'K': 'kulaichev-minpoly-u.txt'}[case]).read().strip().replace('x', 'u'))
iv40 = [pari(f'{A40.numerator}/{A40.denominator}'), pari(f'{B40.numerator}/{B40.denominator}')]
nf_, others_ok = 0, True
for l in open(f'stage4-{case}-Rfactors.txt'):
    m, P = l.split(' ', 1); P = pari(P)
    if pari.poldegree(P, 'u') == pari.poldegree(f, 'u') and pari.pollead(f, 'u') * P == pari.pollead(P, 'u') * f: nf_ += 1; continue
    cnt = int(pari.polsturm(P, iv40)) if pari.poldegree(P, 'u') > 0 else 0
    others_ok = others_ok and cnt == 0
check(nf_ == 1 and others_ok, 'R = Res_t(a, b): every factor other than f has no real root in [a40, b40] (PARI polsturm, exact); so f(u*) = 0, u* = u0')
# (3) the yantra, rebuilt in interval arithmetic
import model
class I:
    def __init__(s, x): s.x = x if isinstance(x, type(iv.mpf(0))) else iv.mpf(x)
    def _w(o): return o.x if isinstance(o, I) else iv.mpf(o)
    def __add__(s, o): return I(s.x + I._w(o))
    __radd__ = __add__
    def __sub__(s, o): return I(s.x - I._w(o))
    def __rsub__(s, o): return I(I._w(o) - s.x)
    def __mul__(s, o): return I(s.x * I._w(o))
    __rmul__ = __mul__
    def __truediv__(s, o):
        d = I._w(o); I.ndiv += 1
        if d.a <= 0 <= d.b: I.bad += 1
        return I(s.x / d)
    def __rtruediv__(s, o):
        I.ndiv += 1
        if s.x.a <= 0 <= s.x.b: I.bad += 1
        return I(I._w(o) / s.x)
    def __neg__(s): return I(-s.x)
    def __pow__(s, k): return I(s.x ** k)
    def pos(s): return s.x.a > 0
    def neg(s): return s.x.b < 0
    def zero_in(s): return s.x.a <= 0 <= s.x.b
I.ndiv = 0; I.bad = 0
uu = I(uI); tt = I(tI); Sx = I(SI)
p = I(2 * w5i - 4)
vv = uu if case == 'K' else p / uu
Pp = vv * vv / (1 + vv * vv); Rr = 1 / (1 + uu * uu); w3 = vv / (1 + vv * vv); w7 = uu / (1 + uu * uu)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
Qexpr = sp.factor(N.Q)
Qn, Qd = sp.fraction(Qexpr)
def sp_eval(e, vals):
    """evaluate a sympy polynomial expression with I objects (u, v, t, S)"""
    P_ = sp.Poly(sp.expand(e), N.u, N.v, N.t, N.S)
    tot = I(0)
    for (a1, a2, a3, a4), c in P_.terms():
        term = I(iv.mpf(int(sp.numer(c))) / int(sp.denom(c)))
        for base, ex in zip(vals, (a1, a2, a3, a4)):
            if ex: term = term * base ** ex
        tot = tot + term
    return tot
vals = (uu, vv, tt, Sx)
Qd_i = sp_eval(Qd, vals); check(not Qd_i.zero_in(), 'denominator of Q(t) nonzero')
Qx = sp_eval(Qn, vals) / Qd_i
b1 = tt * tt / (1 + tt * tt)
tri = model.solve(Pp, Qx, Rr, Sx, w3, w7, sqrt=None, b1=b1)
check(I.bad == 0, f'model.solve in interval arithmetic: all {I.ndiv} divisions have divisor intervals excluding 0 (every divisor nonzero)')
b, w, a = tri['b'], tri['w'], tri['a']
# closing equation: natural.py's H = numer(together(F)); F(b1) = A b1^2 + B b1 + C
Fexpr = sp.together(N.F); Fden = sp.denom(Fexpr)
check(not sp_eval(Fden, vals).zero_in(), 'cleared denominator of the closing equation nonzero')
triv = [f_ for f_, m in sp.factor_list(N.H)[1] if sp.degree(f_, N.t) != 10]
check(all(not sp_eval(f_, vals).zero_in() for f_ in triv), f'the {len(triv)} dropped factors of the closing numerator (u, v, tu +- 1, t +- v) nonzero; so H1 = 0 gives the closing equation exactly')
Gfull = sp.together((N.xW * (N.S - N.R) / (N.R - N.P))**2 - N.S * (1 - N.S))
check(not sp_eval(sp.denom(Gfull), vals).zero_in(), 'denominator of condition (c) nonzero; so G = 0 gives (c) exactly')
check(sp.expand(sp.numer(Gfull) - N.G) == 0, 'G is exactly the cleared numerator of condition (c)')
m1 = w[1] / (b[6] - b[1]); h = b[6] - b[5]; hw = m1 * h; c_ = I(iv.mpf(1) / 2) - b[5]
check(h.pos() and hw.pos() and c_.pos() and (h - c_).pos(), 'signs h > 0, hw > 0, 1/2 - b5 > 0, h - (1/2 - b5) > 0: the squared bindu condition D = 0 gives exactly incircle centre at depth 1/2')
# D's cleared denominator (built in Singular by stage 4, variables w, u, t, S)
Ddens = [Rg(l) for l in open(f'stage4-{case}-Dden.txt').read().split('\n') if l.strip()]
check(all(not I(evalp(compile_poly(fa), (w5i, uI, tI, SI), iv)).zero_in() for fa in Ddens), f'all {len(Ddens)} factors of the cleared denominator of the bindu condition nonzero; so D = 0 gives the squared bindu condition exactly')
check((w[1] * w[1] + b[1] * b[1] - b[1]).zero_in() and (w[9] * w[9] + b[9] * b[9] - b[9]).zero_in(), 'sanity: (b), (c) residual intervals contain 0')
check(abs(w[1].x - tt.x / (1 + tt.x ** 2)).b < mp.mpf(10) ** (-(DIG - 60)), 'sanity: t1\'s corner from the model is the circle point of t (identity of natural.py)')
# order / admissibility, strictly
on_circle = {1, 3, 7, 9}
ordered = all((b[i + 1] - b[i]).pos() for i in range(1, 9)); widths = all(w[i].pos() for i in range(1, 10))
apex = all(((a[i] - b[i]).pos() if i in model.DOWN else (b[i] - a[i]).pos()) for i in range(1, 10))
inside_ = all((w[i] * w[i] + b[i] * b[i] - b[i]).neg() for i in range(1, 10) if i not in on_circle)
check(ordered and widths and apex and inside_, 'admissible: bases strictly ordered, half-widths > 0, apexes on the right side, corners of t2, t4, t5, t6, t8 strictly inside the circle (t1, t3, t7, t9 exactly on it)')
worst = max(max(abs(lo(I._w(val))), abs(hi(I._w(val)))) for name, val in model.all_conditions(tri))
say(f'sanity: every Huet condition interval lies within +-{mp.nstr(worst, 3)} (exactly 0 by the stage-2 lemma)')
# agreement with stored values
dev = max(abs(mid(b[1].x) - mp.mpf(stored['t1b'])), abs(mid(b[9].x) - mp.mpf(stored['S'])), abs(mid(b[6].x) - mp.mpf(stored['Q'])))
check(dev < mp.mpf(10) ** -38, f'rebuilt b1, Q, S agree with the stored values (max difference {mp.nstr(dev, 3)})')
if case == 'D':
    check(abs(mid((uu * vv).x) - 2 / ((1 + w5) / 2) ** 3) < mp.mpf(10) ** -(DIG - 60), 'uv = 2/phi^3 (built in)')
eps = mp.mpf(10) ** -(DIG + 5)           # outward rounding of the written enclosures (strings carry DIG + 25 digits)
ser = lambda z: [mp.nstr(lo(z.x) - eps, DIG + 25), mp.nstr(hi(z.x) + eps, DIG + 25)]
json.dump({'case': case, 'digits': DIG, 'u': ser(uu), 'v': ser(vv), 'b': {i: ser(b[i]) for i in range(1, 10)}, 'w': {i: ser(w[i]) for i in range(1, 10)},
           'a': {i: ser(I(a[i]) if not isinstance(a[i], I) else a[i]) for i in range(1, 10)}, 'box': {'u': ser(uu), 't': ser(tt), 'S': ser(Sx)}},
          open(f'stage5-{case}.json', 'w'))
say(f'u* = {mp.nstr(mid(uI), 60)}; box widths ' + ', '.join(mp.nstr(hi(x) - lo(x), 3) for x in Xb))
print('FINAL ok' if ok else 'FINAL FAIL: a certificate step failed')
