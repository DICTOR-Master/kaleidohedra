# Exact checks for every number in paper #54 (proposed) "gnomon-polar" draft, 2026-10-25.
# Part A inputs: the twelve station volumes of studies/2026-10-24-gnomon-cycle/gnomon-all12.txt (I, star, D', ID, OG from #34/#35 layer
# volumes; rTI, jtI computed there). Part B: sympy, frame of #48. Prints PASS/FAIL per check and ALL PASS.
from fractions import Fraction as F
import sympy as sp
ok_all = True
def say(t, k):
    global ok_all; ok_all &= bool(k); print(('PASS ' if k else 'FAIL ') + t)
class Q:
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o); n = o.a*o.a - 5*o.b*o.b; return s * Q(o.a / n, -o.b / n)
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b) * 5 ** .5
    def __repr__(s): return f'{s.a}' + (f' + {s.b}√5' if s.b else '')
phi = Q(F(1, 2), F(1, 2))
def pw(k):
    r = Q(1)
    for _ in range(abs(k)): r = r * phi
    return r if k >= 0 else Q(1) / r
I = Q(F(-5, 12), F(5, 12))
S = [('I', I), ('Cleo star', Q(F(-5, 6), F(5, 6))), ("D′", Q(F(10, 9), F(14, 27))), ('ID', Q(F(175, 48), F(79, 48))),
     ('OG', Q(F(1975, 456), F(895, 456))), ('rTI', Q(F(-15, 2), F(73, 8))), ('TI', Q(F(-35, 4), F(39, 4))), ('H', Q(F(-365, 4), F(189, 4))),
     ('jtI', Q(F(-3465, 38), F(900, 19))), ('RT', Q(-135, F(135, 2))), ('M', Q(F(145, 12), F(65, 12))), ('I·φ³', Q(F(235, 12), F(35, 4)))]
V = dict(S)
# icosahedron edge 1/φ: V = (5/12)(3+√5) a³
a = Q(1) / phi; say('I is the icosahedron of edge 1/φ', I == Q(F(5, 12)) * Q(3, 1) * a * a * a)
# Fibonacci/Lucas test: x = a + b√5 equals q·φ^k (q rational, k integer) iff b/a = ±F_k/L_k (or b = 0, k = 0)
fib = [0, 1]; luc = [2, 1]
for _ in range(200): fib.append(fib[-1] + fib[-2]); luc.append(luc[-1] + luc[-2])
def phiform(x):
    if x.b == 0: return (x.a, 0)
    if x.a == 0: return None
    r = x.b / x.a
    for k in range(1, 200):
        if abs(r) * 2 > 1 and luc[k] > 2 * r.denominator + 4 and k > 3: pass
        for sg in (1, -1):
            if r == sg * F(fib[k], luc[k]):
                kk = k if sg == 1 else -k; q = x / pw(kk)
                if q.b == 0: return (q.a, kk)
        if luc[k] > 4 * max(r.denominator, 1) + 4: break     # F_k/L_k in lowest terms has denominator ≥ L_k/2
    return None
say('φ-power test is sound on known values (φ^9, 81/φ², 3/(4φ²), √5 not a φ-power)', phiform(pw(9)) == (1, 9) and phiform(Q(81) / pw(2)) == (81, -2)
    and phiform(Q(F(3, 4)) / pw(2)) == (F(3, 4), -2) and phiform(Q(0, 1)) is None)
say('the twelve volumes grow strictly', all(float(x) < float(y) for (_, x), (_, y) in zip(S, S[1:])))
R = {n: v / I for n, v in S}
exp_R = {'Cleo star': Q(2), "D′": Q(F(20, 9), F(44, 45)), 'ID': Q(F(57, 8), F(127, 40)), 'OG': Q(F(645, 76), F(287, 76)), 'rTI': Q(F(183, 8), F(39, 40)),
         'TI': Q(24, F(3, 5)), 'H': Q(87, F(-132, 5)), 'jtI': Q(F(3321, 38), F(-999, 38)), 'RT': Q(F(243, 2), F(-81, 2)), 'M': Q(F(47, 2), F(21, 2)), 'I·φ³': Q(38, 17)}
say('Table 1 column V/I (11 exact entries)', all(R[k] == v for k, v in exp_R.items()))
say('Cleo star = 2·I', R['Cleo star'] == 2)
say('RT = 81·I/φ²', R['RT'] == Q(81) / pw(2))
say('M = φ⁸·I and φ⁸ = (47 + 21√5)/2', R['M'] == pw(8) and pw(8) == Q(F(47, 2), F(21, 2)))
say('I·φ³ = φ⁹·I = (38 + 17√5)·I and I·φ³ = φ·M', R['I·φ³'] == pw(9) and V['I·φ³'] == phi * V['M'])
say('M/RT = φ¹⁰/81, I·φ³/RT = φ¹¹/81', V['M'] / V['RT'] == pw(10) / 81 and V['I·φ³'] / V['RT'] == pw(11) / 81)
# all ratios between stations: which are q·φ^k
pairs = [(n2, n1, phiform(v2 / v1)) for i, (n1, v1) in enumerate(S) for (n2, v2) in S[i + 1:]]
neat = [(a_, b_, f) for a_, b_, f in pairs if f]
say('exactly 10 of the 66 station ratios are rational·φ^k, all among I, Cleo star, RT, M, I·φ³',
    len(pairs) == 66 and len(neat) == 10 and all({a_, b_} <= {'I', 'Cleo star', 'RT', 'M', 'I·φ³'} for a_, b_, _ in neat))
G = [(n2, n1, (v2 - v1) / I) for (n1, v1), (n2, v2) in zip(S, S[1:])]
gf = {n2: phiform(g) for n2, n1, g in G}
say('exactly 4 of the 11 gnomons are rational·φ^k·I: star−I = I, TI−rTI = (3/4)φ⁻²I, H−TI = 18φ⁻⁴I, I·φ³−M = φ⁷I',
    {k: v for k, v in gf.items() if v} == {'Cleo star': (1, 0), 'TI': (F(3, 4), -2), 'H': (18, -4), 'I·φ³': (1, 7)})
for n2, n1, g in G: print(f'   {n2} − {n1} = ({g})·I ≈ {float(g):.4f} I   form {gf[n2]}')
say('gnomons add up to one turn: sum = (φ⁹ − 1)·I', sum((g for _, _, g in G), Q(0)) == pw(9) - 1)
say('Júlia step check: (n+1)² = n² + n + (n+1) (symbolic)', sp.expand((sp.Symbol('n') + 1)**2 - (sp.Symbol('n')**2 + 2*sp.Symbol('n') + 1)) == 0)
say('cube: n³ + 3n² + 3n + 1 = (n+1)³; turn volume ratio (φ³)³ = φ⁹', sp.expand((sp.Symbol('n')+1)**3 - (sp.Symbol('n')**3 + 3*sp.Symbol('n')**2 + 3*sp.Symbol('n') + 1)) == 0 and pw(3)*pw(3)*pw(3) == pw(9))
# ---------- Part B ----------
x = sp.symbols('x', positive=True)
def pyr_height(a_, b_):   # T with corners all perms of (±a, ±b, 0), a < b, about its centre: squares at |coord| = b, hexagons x+y+z = a+b
    # polar in the unit sphere: square pole (1/b)e1, hexagon poles (±1,±1,±1)/(a+b): cube half edge 1/(a+b); height in half edges
    return sp.simplify((1 / b_) / (1 / (a_ + b_)) - 1)
hT = pyr_height(x, 1 + x); hT1 = pyr_height(1 / x, 1 + 1 / x)
say('polar of T(x) has face pyramids of height x/(1+x); of T(1/x) 1/(1+x) (half cube edges)', sp.simplify(hT - x / (1 + x)) == 0 and sp.simplify(hT1 - 1 / (1 + x)) == 0)
say('the two heights add to 1 for every x > 0 (the rhombic dodecahedron height)', sp.simplify(hT + hT1 - 1) == 0)
p = (1 + sp.sqrt(5)) / 2
say('Icosaxes = perms (1/2, φ/2, 0): height 1/φ; Unborn Axes = perms (1/(2φ), φ/2, 0): height 1/φ²',
    sp.simplify(pyr_height(sp.Rational(1, 2), p / 2) - 1 / p) == 0 and sp.simplify(pyr_height(1 / (2 * p), p / 2) - 1 / p**2) == 0)
say('these are T(φ) and T(1/φ) of #48 Theorem 4: x/(1+x) at x = φ is 1/φ', sp.simplify(hT.subs(x, p) - 1 / p) == 0)
say('Kelvin x = 1: both heights 1/2 (tetrakis hexahedron)', hT.subs(x, 1) == sp.Rational(1, 2))
say('polar corner distances: apex 2/φ (both), hexagon poles 2√3/φ² and 2√3/√5',
    sp.simplify(1 / (p / 2) - 2 / p) == 0 and sp.simplify(sp.sqrt(3) / (p**2 / 2) - 2 * sp.sqrt(3) / p**2) == 0 and sp.simplify(sp.sqrt(3) / ((1 / p + p) / 2) - 2 * sp.sqrt(3) / sp.sqrt(5)) == 0)
vt = (3 - sp.sqrt(5)) / 24
say('Tricap volume (3 − √5)/24 = 1/(12φ²)', sp.simplify(vt - 1 / (12 * p**2)) == 0)
say('√5 = (1 + 2√5/3) − 8 Tricaps, 2 = (1 + √5/3) + 8 Tricaps, sum φ³', sp.simplify(1 + 2*sp.sqrt(5)/3 - 8*vt - sp.sqrt(5)) == 0 and sp.simplify(1 + sp.sqrt(5)/3 + 8*vt - 2) == 0
    and sp.simplify(sp.sqrt(5) + 2 - p**3) == 0)
say('8 Tricaps = 1 − √5/3 ≈ 0.2546 = 10.2% of the Icosaxes, 14.6% of the Unborn Axes', abs(float(8*vt) - 0.254644) < 1e-6
    and round(float(8*vt / (1 + 2*sp.sqrt(5)/3)) * 100, 1) == 10.2 and round(float(8*vt / (1 + sp.sqrt(5)/3)) * 100, 1) == 14.6)
say('tan²72° = 5 + 2√5', sp.simplify(sp.tan(2*sp.pi/5)**2 - (5 + 2*sp.sqrt(5))) == 0)
# one-centre polar of the Lotus Jewel Axes: poles of the three dent walls of the (1,1,1) dent
A = sp.Matrix([1, 1, 1]) / (2 * p); B = [sp.Matrix([0, sp.Rational(1, 2), p / 2]), sp.Matrix([p / 2, 0, sp.Rational(1, 2)]), sp.Matrix([sp.Rational(1, 2), p / 2, 0])]
say('dent (1,1,1): base corners are Icosaxes corners on the hexagon x+y+z = φ²/2, apex at x+y+z = 3/(2φ) inside',
    all(sp.simplify(sum(b) - p**2 / 2) == 0 for b in B) and sp.simplify(sum(A) - 3 / (2 * p)) == 0 and float(sum(A)) < float(p**2 / 2))
hexpole = sp.Matrix([1, 1, 1]) / (p**2 / 2)
dist = []; ang = []
for i in range(3):
    n = (B[i] - A).cross(B[(i + 1) % 3] - A); d = n.dot(A); pole = n / d
    dist.append(sp.nsimplify(sp.simplify(pole.norm()**2), [sp.sqrt(5)])); ang.append(float(sp.acos(sp.simplify(pole.dot(hexpole) / (pole.norm() * hexpole.norm()))) * 180 / sp.pi))
r2 = sp.radsimp(sp.simplify(dist[0]))
say(f'the three dent-wall poles are equidistant: |pole|² = {r2} ≈ {float(sp.sqrt(r2)):.4f}² against the hexagon pole 2√3/φ² ≈ {float(hexpole.norm()):.4f}',
    all(sp.simplify(d_ - dist[0]) == 0 for d_ in dist) and float(sp.sqrt(r2)) > float(hexpole.norm()))
print(f'   dent-wall pole distance {float(sp.sqrt(r2)):.4f}, angle to the hexagon pole {ang[0]:.2f}°, {ang[1]:.2f}°, {ang[2]:.2f}°')
say('dent-wall pole distance √(10 − 2√5) = 4 sin 36°, and 37.38° rounded', sp.simplify(sp.sqrt(r2) - 4*sp.sin(sp.pi/5)) == 0 and round(ang[0], 2) == 37.38)
print('ALL PASS' if ok_all else 'SOME FAIL')
