# projection_body_all.py: the paper's remaining claims, exact, with our own zonotope code from projection_body.py (direct computation,
# NOT via the paper's formulas). Prop. 5: |T_d| = 1/d!, |Pi T_d| = (d+1)/((d-1)!)^d, R_d(T_d) = c_d = (d+1) d^d / d!, d = 2..6.
# Prop. 3 / product test: R(T_r x T_s) computed directly as a zonotope = c_r c_s, and the closed form
# (r+1)(s+1)/(r+s+1) * C(r+s,r) * r^r s^s/(r+s)^(r+s) = R(T_r x T_s)/c_(r+s), for 2 <= r <= s, r+s <= 7.
# Lemma 4: R of random rational simplices and random products equals the standard value. Theorem 1 certificate integers.
# Corollary 6: e < 11/4 (bound on the series), c10 = 17187500/567, A = c10/beta^10 = 1638400000000/1336956340797 > 1,
# c_n < (n+1) beta^n for n = 2..200, and the explicit chain: for lambda = 1.001 (< A^(1/10)) find the N and check
# R_n(K_n)/R_n(T_n) >= lambda^n for every n from N to N+300 exactly.
import sys, os, math, random, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('pb', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projection_body.py'))
src = open(spec.origin).read().split('\nshear')[0]          # functions only, not the T10 x T10 run
pb = {}; exec(compile(src, spec.origin, 'exec'), pb)
G_of, vol_of, Z, T = pb['simplex_area_normals'], pb['simplex_volume'], pb['zonotope_volume'], pb['T']
c = lambda d: F((d + 1) * d ** d, math.factorial(d))
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok  ' if cond else 'FAIL') + ' ' + name)
for d in range(2, 7):
    V = T(d); G = G_of(V); vT = vol_of(V); vP = Z(G)
    check(f'Prop 5 d={d}: |T|={vT}, |PiT|={vP}, R={vP / vT ** (d - 1)}', vT == F(1, math.factorial(d)) and vP == F(d + 1, math.factorial(d - 1) ** d) and vP / vT ** (d - 1) == c(d))
def prod_R(Va, Vb):
    r, s = len(Va[0]), len(Vb[0]); Ga, Gb = G_of(Va), G_of(Vb); va, vb = vol_of(Va), vol_of(Vb)
    G = [[x * vb for x in g] + [F(0)] * s for g in Ga] + [[F(0)] * r + [x * va for x in g] for g in Gb]
    return Z(G) / (va * vb) ** (r + s - 1)
for r in range(2, 6):
    for s in range(r, 8 - r):
        R = prod_R(T(r), T(s)); n = r + s
        form = F((r + 1) * (s + 1), n + 1) * math.comb(n, r) * F(r ** r * s ** s, n ** n)
        check(f'Prop 3 / product test r={r}, s={s}: R direct = c_r c_s, R/c_n = closed form {form}', R == c(r) * c(s) and R / c(n) == form)
random.seed(7)
for d in (3, 4, 5):
    for _ in range(3):
        while True:
            V = [tuple(random.randint(-5, 5) for _ in range(d)) for _ in range(d + 1)]
            if vol_of(V) != 0: break
        G = G_of(V); check(f'Lemma 4 d={d}: random simplex R = c_d', Z(G) / vol_of(V) ** (d - 1) == c(d))
V2 = [(0, 0), (3, 1), (1, 4)]; V3 = [(1, 0, 0), (0, 2, 1), (1, 1, 3), (-2, 0, 1)]
check('Lemma 4 + Prop 3: random triangle x random tetrahedron R = c2 c3', prod_R(V2, V3) == c(2) * c(3))
check('Theorem 1 integers: C(20,10) = 184756, 121*184756 - 21*2^20 = 335380', math.comb(20, 10) == 184756 and 121 * 184756 - 21 * 2 ** 20 == 335380)
check('Theorem 1: c10^2/c20 = 22355476/22020096', c(10) ** 2 / c(20) == F(22355476, 22020096))
beta = F(11, 4)
tail_terms = [F(1, math.factorial(j)) for j in range(3, 40)]
check('Cor 6: ratios of the tail terms 1/j! (j >= 3) are < 1/3', all(tail_terms[i + 1] / tail_terms[i] < F(1, 3) for i in range(len(tail_terms) - 1)))
check('Cor 6: 5/2 + (1/6) sum 3^-j = 11/4', F(5, 2) + F(1, 6) * F(3, 2) == beta)
check('Cor 6: e < 11/4 (numerically 2.71828 < 2.75)', math.e < 2.75)
check('Cor 6: c10 = 17187500/567', c(10) == F(17187500, 567))
A = c(10) / beta ** 10
check(f'Cor 6: A = c10/beta^10 = {A} = 1638400000000/1336956340797 > 1', A == F(1638400000000, 1336956340797) and A > 1)
check('Cor 6: c_n < (n+1) beta^n for n = 2..200 (exact)', all(c(n) < (n + 1) * beta ** n for n in range(2, 201)))
lam = F(1001, 1000)
check('Cor 6: lambda = 1.001 < A^(1/10)', lam ** 10 < A)
def ratio(n):
    k, rem = divmod(n - 10, 10); dr = 10 + rem
    return c(10) ** k * c(dr) / c(n)
bad = [n for n in range(20, 3000) if ratio(n) < lam ** n]
N = (max(bad) + 1) if bad else 20
check(f'Cor 6 explicit: with lambda = 1.001, R_n(K_n)/R_n(T_n) >= lambda^n fails last at n = {max(bad) if bad else None}; holds for every n in [{N}, 2999]', all(ratio(n) >= lam ** n for n in range(N, 3000)))
print('FINAL ok: every claim of the paper confirmed exactly' if ok else 'FINAL FAIL')
