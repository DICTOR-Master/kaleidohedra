"""Step 3: the Krawczyk box around Theorem 10's yantra, in exact rational arithmetic (no floating point in the test itself).

Krawczyk's operator (R. Krawczyk 1969; uniqueness form R. E. Moore 1977, A. Neumaier 1990, Interval Methods for Systems of Equations, Thm 5.1.7):
    K(X) = y - Y F(y) + (I - Y J(X)) (X - y),
with y the box centre, Y any real matrix (here a dyadic rounding of J(y)^-1) and J(X) an interval enclosure of the Jacobian on X.
If K(X) lies in the interior of X, F has exactly one zero in X.  J(X) uses the monotone split on X (all coordinates > 0), exactly as
the leaf checker.  The box X is dyadic; Theorem 10's solution (studies/2026-11-15-yantra-uniqueness, data/census-K.json, 60 digits,
itself certified there in a box of radius 1e-300) is converted to (u, tau, rho) and must lie in X.
Usage: b3_krawczyk.py polys.json census.json out.json [log2 half-width, default 24]
FINAL ok iff K(X) is inside int X, the census point is in X, and the control (F + 1e-6 in the first component, i.e. a perturbed system)
FAILS the test (its zero moves out or the inclusion breaks)."""
import json, sys, time
from fractions import Fraction as Fq
import mpmath as mp
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
src, cen, dst = sys.argv[1], sys.argv[2], sys.argv[3]
HW = int(sys.argv[4]) if len(sys.argv) > 4 else 24
mp.mp.dps = 80
data = json.load(open(src))
F = [[(tuple(e), int(c)) for e, c in data['F'][k]] for k in ('G', 'H1', 'D')]
def deriv(p, j): return [(tuple(e[i] - (i == j) for i in range(3)), c * e[j]) for e, c in p if e[j] > 0]
J = [[deriv(f, j) for j in range(3)] for f in F]
def ev(p, x): return sum(c * x[0]**e[0] * x[1]**e[1] * x[2]**e[2] for e, c in p)
def enc(p, lo, hi):                                   # monotone split on a box with lo >= 0 (exact)
    l = Fq(0); h = Fq(0)
    for e, c in p:
        a = lo[0]**e[0] * lo[1]**e[1] * lo[2]**e[2]; b = hi[0]**e[0] * hi[1]**e[1] * hi[2]**e[2]
        if c > 0: l += c * a; h += c * b
        else: l += c * b; h += c * a
    return l, h
c = json.load(open(cen))['admissible'][0]
u, t, S = mp.mpf(c['u']), mp.mpf(c['t']), mp.mpf(c['S'])
R = 1 / (1 + u * u)
x0 = [u, t / u, (S - R) / ((1 - R) * (1 - u))]
say('Theorem 10 in (u, tau, rho):', [mp.nstr(v, 25) for v in x0])
# refine by Newton (mpmath) for a good centre
x = list(x0)
for it in range(5):
    Fv = mp.matrix([ev(f, x) for f in F]); Jv = mp.matrix([[ev(J[i][j], x) for j in range(3)] for i in range(3)])
    dx = mp.lu_solve(Jv, Fv); x = [x[i] - dx[i] for i in range(3)]
say('Newton-refined:', [mp.nstr(v, 25) for v in x], ' |F| =', mp.nstr(max(abs(ev(f, x)) for f in F), 5))
def dy(v, k): return Fq(int(mp.nint(v * 2**k)), 2**k)
yc = [dy(v, HW + 30) for v in x]
X = [(yc[i] - Fq(1, 2**HW), yc[i] + Fq(1, 2**HW)) for i in range(3)]
def krawczyk(Fl, Jl, X, yc):
    Jy = mp.matrix([[float(ev(Jl[i][j], yc)) for j in range(3)] for i in range(3)])
    Yf = mp.inverse(Jy)
    Y = [[Fq(int(mp.nint(Yf[i, j] * 2**60)), 2**60) for j in range(3)] for i in range(3)]
    Fy = [ev(f, yc) for f in Fl]
    lo = [a for a, b in X]; hi = [b for a, b in X]
    JX = [[enc(Jl[i][j], lo, hi) for j in range(3)] for i in range(3)]
    K = []
    for i in range(3):
        base = yc[i] - sum(Y[i][k] * Fy[k] for k in range(3))
        l = base; h = base
        for j in range(3):
            # M_ij = delta_ij - sum_k Y_ik J_kj  (interval)
            ml = Fq(1 if i == j else 0); mh = ml
            for k in range(3):
                a, b = JX[k][j]; y = Y[i][k]
                if y >= 0: ml -= y * b; mh -= y * a
                else: ml -= y * a; mh -= y * b
            r = X[j][1] - yc[j]                         # X_j - y_j = [-r, r]
            m = max(abs(ml), abs(mh))
            l -= m * r; h += m * r
        K.append((l, h))
    inside = all(X[i][0] < K[i][0] and K[i][1] < X[i][1] for i in range(3))
    return inside, K
inside, K = krawczyk(F, J, X, yc)
ratio = [float((K[i][1] - K[i][0]) / (X[i][1] - X[i][0])) for i in range(3)]
say('Krawczyk: K(X) inside int X:', inside, '; width ratios K/X:', [f'{r:.3g}' for r in ratio])
cin = all(X[i][0] < Fq(mp.nstr(x0[i], 70)) < X[i][1] for i in range(3))
say('Theorem 10 point (census) inside X:', cin)
# control: perturbed system G + 2^-20 (shifts the zero by far more than the box): the test must fail
Fp = [F[0] + [((0, 0, 0), 0)], F[1], F[2]]
Fp[0] = [(e, c) for e, c in F[0]]
Gs = [(e, Fq(c)) for e, c in F[0]] + [((0, 0, 0), Fq(1, 2**20))]
inside_p, _ = krawczyk([Gs, F[1], F[2]], J, X, yc)
say('control: G + 2^-20 passes the same box (must be False):', inside_p)
dig = max(max(len(str(abs(v.numerator))), len(str(v.denominator))) for iv in X for v in iv)
json.dump({'box': [[str(a), str(b)] for a, b in X], 'centre': [str(v) for v in yc], 'half_width_log2': HW,
           'K': [[str(a), str(b)] for a, b in K], 'inside': inside, 'census_point_inside': cin, 'control_passes': inside_p,
           'max_digits': dig}, open(dst, 'w'), indent=1)
ok = inside and cin and not inside_p
print('FINAL ok' if ok else 'FINAL FAIL')
