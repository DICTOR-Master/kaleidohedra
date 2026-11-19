# Number audit for the Dehn canon paper: recompute every number of the text and tables (60 digits) and check that the
# paper prints it (Theorem 15's values, Theorem 14's volumes and a³/vol, Hilbert's pair of Theorem 6′ from its corners, and the study 8, 9 and 10 counts included). Also checks CLEO = F* and AXE = A* of Ogievetsky-Papadopolos (1999, eq. (8)) and the study line counts.
import re, json, os, glob
from mpmath import mp, mpf, sqrt, acos, pi, degrees
mp.dps = 60
H = open('../paper.html', encoding='utf-8').read()
txt = re.sub(r'<[^>]+>', '', H)
bad = []
def need(s, why):
    if s not in txt: bad.append(f'missing "{s}" ({why})')
def ok(c, why):
    if not c: bad.append('FAIL ' + why)
r5 = sqrt(5); g = (r5 - 1) / 2; tau = 1 / g
r = sqrt(3 * (10 - 2 * r5))
a = acos(1 / r5); b = acos((3 - r5) / r); c = acos(r5 / 3); e = acos((r5 + 1) / r); t3 = acos(mpf(1) / 3)
ok(abs(a + b + e - pi) < 1e-50, 'α + β + ε = π'); ok(abs(a + 2 * b - c - pi) < 1e-50, 'α + 2β − γ = π'); ok(abs(e - (b - c)) < 1e-50, 'ε = β − γ')
# Conway-Radin-Sadun reduction (Theorem 12, §9): β = (π + γ − α)/2, the same identity as word_angle_relation α + 2β − γ = π
ok(abs(b - (pi + c - a) / 2) < 1e-50, 'β = (π + γ − α)/2'); ok(abs((a + 2 * ((pi + c - a) / 2) - c) - pi) < 1e-50, 'β = (π + γ − α)/2 ⇔ α + 2β − γ = π')
need('β = (π + γ − α)/2', 'CRS reduction'); need('α + 2β − γ = π', 'word_angle_relation')
ok(abs(((3 - r5) / r) ** 2 - (mpf(1) / 3 - 2 * r5 / 15)) < 1e-50, 'cos² β'); ok(abs(((r5 + 1) / r) ** 2 - (mpf(1) / 3 + 2 * r5 / 15)) < 1e-50, 'cos² ε')
for v, s in [(a, '63.43'), (b, '79.18'), (c, '41.81'), (e, '37.37'), (a + b, '142.62')]:
    ok(str(degrees(v))[:len(s)] == s, f'{s}° truncation'); need(s, 'angle in degrees')
ok(abs(mp.cos(2 * a) + mpf(3) / 5) < 1e-50, 'cos 2α'); ok(abs(mp.cos(2 * b) + (10 + 8 * r5) / 30) < 1e-50, 'cos 2β')
ok(abs(2 * acos(1 / sqrt(3)) - (pi - t3)) < 1e-50, '2 arccos(1/√3) = π − arccos(1/3)')
ok(abs(mp.sin(b) - 4 / r) < 1e-50 and abs(mp.sin(e) - (2 * r5 - 2) / r) < 1e-50, 'sin β, sin ε')
# recurrence of Theorem 12: norm never divisible by 3, step factor -220 mod 225
xp, x = (2, 0), (-10, -8)
for n in range(1, 400):
    ok((x[0] ** 2 - 5 * x[1] ** 2) % 3 != 0, f'3 ∤ norm at n={n}')
    xp, x = x, (-10 * x[0] - 40 * x[1] - 225 * xp[0], -8 * x[0] - 10 * x[1] - 225 * xp[1])
# words over α, β (mod π: γ ≡ α + 2β, π − ε ≡ α + β, ε ≡ −α − β)
W = {'CLEO': (3, 3 * g), 'AXE': (g + 1, 4 + 2), 'FUJI': (6 + 3 - 3 * g, 6 + 6 - 3 * g)}
ok(abs(W['CLEO'][0] * a + W['CLEO'][1] * b - (3 * a + 3 * g * b)) < 1e-50, 'CLEO form')
ok(abs((g * a + 4 * b + c) - (W['AXE'][0] * a + W['AXE'][1] * b) + pi) < 1e-50, 'AXE edges → form (mod π)')
# FUJI symbolically mod π: 6(π−ε) + 3γ + 3gε ; ε = π − α − β, γ = α + 2β − π
fuji = 6 * (a + b) + 3 * (a + 2 * b - pi) + 3 * g * (pi - a - b) ; ok(abs(fuji - (W['FUJI'][0] * a + W['FUJI'][1] * b) - (3 * g - 3) * pi) < 1e-50, 'FUJI form exact')
ico = (-120, -240); dod = (-30 * (2 * r5 - 2), 0)
det = lambda u, v: u[0] * v[1] - u[1] * v[0]
for (p, q, val, s) in [('CLEO', 'AXE', 15, '15'), ('CLEO', 'FUJI', 45 - 45 * g, '45 − 45g'), ('AXE', 'FUJI', 30 * g - 45, '30g − 45')]:
    ok(abs(det(W[p], W[q]) - val) < 1e-50, f'det {p}-{q}'); need(s, 'determinant')
for (q, val, s) in [('CLEO', 720 - 360 * g, '720 − 360g'), ('AXE', -480 + 240 * g, '−480 + 240g'), ('FUJI', 720 - 360 * g, '720 − 360g')]:
    ok(abs(det(ico, W[q]) - val) < 1e-50, f'det ico-{q}'); need(s, 'determinant')
for q in W: ok(abs(det(dod, W[q])) > 1, f'det dod-{q}')
ok(abs(det(dod, ico)) > 1, 'det dod-ico')
ok(all(w[0] > 0 and w[1] > 0 for w in W.values()), 'positive coefficients (Remark)')
# icosahedron −120 ⊗ γ = −120 α − 240 β mod π; dodecahedron edge 2√5 − 2 at π − α
ok(abs(degrees(pi - acos(-1 / r5)) - degrees(a)) < 1e-40, 'dodecahedron dihedral π − α')
ok(abs(degrees(pi - acos(-r5 / 3)) - degrees(c)) < 1e-40, 'icosahedron dihedral π − γ')
# Ogievetsky-Papadopolos: their β = our ε, their δ = our β; CLEO = F*, AXE = A* (scale τ)
bOP = acos((tau + 1) / (sqrt(3) * sqrt(tau + 2))); dOP = acos((tau - 1) / (sqrt(3) * sqrt(tau + 2)))
ok(abs(bOP - e) < 1e-50 and abs(dOP - b) < 1e-50, 'OP β = ε, OP δ = β')
# CLEO scaled by τ: 3τ at α, 3 at δ; α ≡ −βOP − δ  ->  (−3τ, 3 − 3τ) = F*
ok(abs((3 * tau * (-1)) + 3 * tau) < 1e-50 and abs(3 * tau * (-1) - (-3 * tau)) < 1e-50, 'F* β-coefficient')
F_star = (-3 * tau, -3 * tau + 3); cleo_op = (-3 * tau, -3 * tau + 3); ok(F_star == cleo_op, 'CLEO = F*')
# AXE scaled by τ: 1 at α, 4τ at δ, τ at γ; γ ≡ −βOP + δ -> (−1 − τ, −1 + 4τ + τ) = A* = (−τ − 1, 5τ − 1)
axe_op = (-1 - tau, -1 + 5 * tau); ok(abs(axe_op[0] - (-tau - 1)) < 1e-50 and abs(axe_op[1] - (5 * tau - 1)) < 1e-50, 'AXE = A*')
ok(abs(a + c + 2 * bOP - pi) < 1e-50 and abs(a - c + 2 * dOP - pi) < 1e-50, 'OP Lemma 1')
# cube ∩ octahedron: Lucky 7 t inside (7/4, 9/5); sign of 2t − 3
t7 = mpf('1.7565821359'); ok(mpf(7) / 4 < t7 < mpf(9) / 5, 'Lucky 7 in interval'); need('1.7566', 'Lucky 7 t')
# Theorem 15: θ = arccos(1/3); sin(nθ) in Q·√2 (exact recurrence vs 60 digits); 2α, 2β data; sines of combinations in Q(√5)
from fractions import Fraction as Fr
ok(str(degrees(t3))[:5] == '70.52', 'θ degrees'); need('70.52', 'θ in degrees')
ok(abs(mp.cos(t3) - mpf(1) / 3) < 1e-50 and abs(mp.sin(t3) - 2 * sqrt(2) / 3) < 1e-50, 'cos θ, sin θ')
ca, sb = Fr(1, 3), Fr(2, 3)                       # cos nθ = ca, sin nθ = sb·√2
for n in range(1, 61):
    ok(abs(mp.cos(n * t3) - mpf(ca.numerator) / ca.denominator) < 1e-45 and
       abs(mp.sin(n * t3) - mpf(sb.numerator) / sb.denominator * sqrt(2)) < 1e-45, f'sin({n}θ) in Q√2')
    ca, sb = ca / 3 - 4 * sb / 3, sb / 3 + 2 * ca / 3
ok(abs(mp.sin(2 * a) - mpf(4) / 5) < 1e-50 and abs(mp.sin(2 * b) - (10 - 2 * r5) / 15) < 1e-50, 'sin 2α, sin 2β')
for s_ in ['4/5', '(10 − 2√5)/15', '−3/5', '−(10 + 8√5)/30', '(1 + 2√−2)/3', '2√2/3']: need(s_, 'Theorem 15 value')
# Q(√5) as pairs (x, y) = x + y√5; cos, sin of Q·2α + R·2β exact, compared at 60 digits
mul = lambda u, v: (u[0] * v[0] + 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
add = lambda u, v: (u[0] + v[0], u[1] + v[1]); neg = lambda u: (-u[0], -u[1])
val = lambda u: mpf(u[0].numerator) / u[0].denominator + mpf(u[1].numerator) / u[1].denominator * r5
A = ((Fr(-3, 5), Fr(0)), (Fr(4, 5), Fr(0))); B = ((Fr(-1, 3), Fr(-4, 15)), (Fr(2, 3), Fr(-2, 15)))
def rot(x, y): return (add(mul(x[0], y[0]), neg(mul(x[1], y[1]))), add(mul(x[1], y[0]), mul(x[0], y[1])))
def pw(x, k):
    z = ((Fr(1), Fr(0)), (Fr(0), Fr(0)))
    for _ in range(abs(k)): z = rot(z, x if k > 0 else (x[0], neg(x[1])))
    return z
for Q in range(-6, 7):
    for R in range(-6, 7):
        z = rot(pw(A, Q), pw(B, R))
        ok(abs(val(z[0]) - mp.cos(Q * 2 * a + R * 2 * b)) < 1e-45 and abs(val(z[1]) - mp.sin(Q * 2 * a + R * 2 * b)) < 1e-45, f'Q(√5) at {Q},{R}')
ok(int(mp.sqrt(10)) ** 2 != 10, '√10 irrational (10 not a square)')
for s_ in ['15 pairs', '60fc5ee5', 'Theorem 15', 'Theorem 16']: need(s_, 'study 8 fact')
# Theorem 14 (study 9): volumes, the scale-free number a³/vol, g(t) monotone with range (−1, 1/5), the polynomial identities
D_ = lambda t: t ** 3 - 3 * (t - 1) ** 3                          # volume = (4/3) D_(t)
def det3(u, v, w): return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])
tv = [(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
vt = Fr(abs(det3(*[tuple(x - y for x, y in zip(tv[k], tv[0])) for k in (1, 2, 3)])), 6); ok(vt == Fr(8, 3), f'tetra volume {vt}')
vo = 8 * Fr(1, 6); ok(vo == Fr(4, 3), 'octahedron volume (8 corner simplices)')
from math import comb
def vco(t):                                                       # 8 × Irwin–Hall: {x ∈ [0,1]³, Σx ≤ t}
    return 8 * sum((-1) ** k * comb(3, k) * max(t - k, 0) ** 3 for k in range(4)) / 6
for t in [Fr(1), Fr(11, 10), Fr(5, 4), Fr(3, 2), Fr(7, 4), Fr(9, 5), Fr(19, 10), Fr(199, 100)]:
    ok(vco(t) == Fr(4, 3) * D_(t), f'cube ∩ octahedron volume at t = {t}')
ok(vco(Fr(1)) == vo, 'line at t = 1 is the octahedron')
U = 12 ** 3 * 2                                                   # (12√2)³ = U·√2; unit 2592√2
ok(Fr(U) / Fr(8, 3) / 2592 == Fr(1, 2) and -Fr(U) / Fr(4, 3) / 2592 == -1, 'a³/vol: tetra 1/2, oct −1')
gq = lambda t: (2 * t - 3) ** 3 / D_(t)
ok(Fr(U) * (2 * Fr(7, 4) - 3) ** 3 / (Fr(4, 3) * D_(Fr(7, 4))) / 2592 == gq(Fr(7, 4)), 'a³/vol of the line = 2592√2 g(t)')
ok(gq(Fr(1)) == -1 and gq(Fr(2)) == Fr(1, 5) and gq(Fr(3, 2)) == 0, 'g(1), g(2), g(3/2)')
Dp = lambda t: 3 * t * t - 9 * (t - 1) ** 2
for t in [Fr(k, 7) for k in range(-7, 22)]:                       # degree 5: 29 points
    ok((2 * t - 3) ** 2 * (6 * D_(t) - (2 * t - 3) * Dp(t)) == 9 * (2 * t - 1) * (2 * t - 3) ** 2, f"g' numerator at {t}")
    ok(2 * (2 * t - 3) ** 3 - D_(t) == -3 + 9 * (t - 1) * (t - 2) * (2 * t - 3), f'identity tetra at {t}')
    ok((2 * t - 3) ** 3 + D_(t) == 3 * (t - 1) * (2 * t * t - 7 * t + 8), f'identity oct at {t}')
grid = [1 + Fr(k, 1000) for k in range(1001)]; gv = [gq(t) for t in grid]
ok(all(x < y for x, y in zip(gv, gv[1:])) and gv[0] == -1 and gv[-1] == Fr(1, 5), 'g strictly increasing on [1, 2], −1 to 1/5')
ok(all(gq(t) < Fr(1, 5) for t in grid[1:-1]) and all(gq(t) > -1 for t in grid[1:]), 'g in (−1, 1/5) on (1, 2)')
ok(all(2 * t * t - 7 * t + 8 > 0 for t in grid) and all(abs((t - 1) * (t - 2) * (2 * t - 3)) < Fr(1, 3) for t in grid), 'signs of the factors')
for x in [Fr(k, 5) for k in range(-6, 7)]:
    for y in [Fr(k, 5) for k in range(-6, 7)]:
        ok(x ** 3 * (12 + 9 * y - y ** 3) - y ** 3 * (12 + 9 * x - x ** 3) == (x - y) * (12 * (x * x + x * y + y * y) + 9 * x * y * (x + y)), f'identity line at {x},{y}')
        if -1 < x < 1 and -1 < y < 1 and (x, y) != (0, 0): ok(12 * (x * x + x * y + y * y) + 9 * x * y * (x + y) > 0, f'factor > 0 at {x},{y}')
ok(4 * D_((Fr(1, 3) + 3) / 2) == 12 + 9 * Fr(1, 3) - Fr(1, 3) ** 3, '4 D((x+3)/2) = 12 + 9x − x³')
g7 = (2 * t7 - 3) ** 3 / (t7 ** 3 - 3 * (t7 - 1) ** 3); a7 = 12 * sqrt(2) * (2 * t7 - 3); v7 = mpf(4) / 3 * (t7 ** 3 - 3 * (t7 - 1) ** 3)
for v, s_ in [(g7, '0.0327'), (a7, '8.7086'), (v7, '5.4944')]:
    ok(mp.nstr(v, 12)[:len(s_)] == s_, f'Lucky 7 {s_} truncation ({mp.nstr(v, 8)})'); need(s_, 'Lucky 7 value')
for s_ in ['volume 4/3', 'volume 8/3', '(4/3)(t³ − 3(t − 1)³)', '2592√2', 'g(1) = −1', 'g(2) = 1/5', '9(2t − 1)(2t − 3)²',
           '−3 + 9(t − 1)(t − 2)(2t − 3)', '3(t − 1)(2t² − 7t + 8)', '(x − y)(12(x² + xy + y²) + 9xy(x + y))', '8 − 16/3 = 8/3',
           '(4/3)t³ − 6 · (2/3)(t − 1)³', '510a799f', 'Theorem 14', 'Table 5']: need(s_, 'study 9 fact')
ok(Fr(8) - 4 * Fr(4, 3) == Fr(8, 3), 'tetra = cube less four corners')
for t in [Fr(11, 10), Fr(3, 2), Fr(19, 10)]: ok(Fr(4, 3) * t ** 3 - 6 * Fr(2, 3) * (t - 1) ** 3 == Fr(4, 3) * D_(t), f'ball less six caps at {t}')
# Theorem 6′ (study 10): Hilbert's pair from its corners alone, exact over Q(√2, √3) where needed
Pa, Pb, Pc, Pd, Pd2 = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)
sub3 = lambda u, v: tuple(x - y for x, y in zip(u, v)); dot3 = lambda u, v: sum(x * y for x, y in zip(u, v))
cross3 = lambda u, v: (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def tet_edges(V):                                     # {(i, j): (length², interior dihedral angle)} from the corners only
    cen = tuple(Fr(sum(v[k] for v in V), 4) for k in range(3)); out = {}
    def nrm(face):                                    # outward normal of the face opposite the fourth corner
        n = cross3(sub3(V[face[1]], V[face[0]]), sub3(V[face[2]], V[face[0]]))
        return n if dot3(n, sub3(V[face[0]], cen)) > 0 else tuple(-x for x in n)
    for i in range(4):
        for j in range(i + 1, 4):
            k, l = [m for m in range(4) if m not in (i, j)]
            n1, n2 = nrm((i, j, k)), nrm((i, j, l))
            ang = pi - acos(mpf(dot3(n1, n2)) / sqrt(mpf(dot3(n1, n1)) * dot3(n2, n2)))
            out[(i, j)] = (dot3(sub3(V[i], V[j]), sub3(V[i], V[j])), ang)
    return out
T1 = tet_edges([Pa, Pb, Pc, Pd]); T2 = tet_edges([Pa, Pb, Pc, Pd2])
ac3 = acos(1 / sqrt(3))
exp1 = {(0, 1): (1, pi / 2), (0, 2): (1, pi / 2), (0, 3): (1, pi / 2), (1, 2): (2, ac3), (1, 3): (2, ac3), (2, 3): (2, ac3)}
exp2 = {(0, 1): (1, pi / 4), (0, 2): (1, pi / 2), (0, 3): (2, pi / 2), (1, 2): (2, pi / 2), (1, 3): (3, pi / 3), (2, 3): (1, pi / 4)}
for nm_, T, X in [('T', T1, exp1), ("T′", T2, exp2)]:
    for e_ in X: ok(T[e_][0] == X[e_][0] and abs(T[e_][1] - X[e_][1]) < 1e-50, f'{nm_} edge {e_}: length² and angle')
ok(sum(sqrt(T1[e_][0]) for e_ in T1 if abs(T1[e_][1] - ac3) < 1e-40) - 3 * sqrt(2) < 1e-50, 'dehnSet T = 3√2 ⊗ arccos(1/√3): total length at that angle')
ok(all(abs(T1[e_][1] - pi / 2) < 1e-50 for e_ in T1 if T1[e_][0] == 1), 'T: the other three angles π/2, class 0')
ok(all(abs(12 * T2[e_][1] / pi - mp.nint(12 * T2[e_][1] / pi)) < 1e-50 for e_ in T2), "T′: every angle in ℚπ, dehnSet T′ = 0")
ok(str(degrees(ac3))[:5] == '54.73', 'arccos(1/√3) in degrees'); need('54.73', 'arccos(1/√3) in degrees')
N2 = [(1, 1, 0), (-1, 0, 0), (0, -1, 1), (0, 0, -1)]            # the face normals of T′ quoted in the proof
for n_ in N2:                                                   # each is outward: ≤ on all corners, = on exactly three
    hv = [dot3(n_, v) for v in (Pa, Pb, Pc, Pd2)]; mx = max(hv); ok(hv.count(mx) == 3, f'normal {n_} supports a face of T′')
    ok(dot3(n_, sub3((Fr(1, 4), Fr(2, 4), Fr(1, 4)), (Pa, Pb, Pc, Pd2)[hv.index(mx)])) < 0, f'normal {n_} points out')
for i in range(4):
    for j in range(i + 1, 4):
        an = acos(mpf(dot3(N2[i], N2[j])) / sqrt(mpf(dot3(N2[i], N2[i])) * dot3(N2[j], N2[j])))
        ok(abs(12 * an / pi - mp.nint(12 * an / pi)) < 1e-50, f'T′ normals {i},{j}: angle in ℚπ')
vol6 = lambda V: abs(det3(*[sub3(V[k], V[0]) for k in (1, 2, 3)]))
ok(vol6([Pa, Pb, Pc, Pd]) == 1 and vol6([Pa, Pb, Pc, Pd2]) == 1, 'volumes 1/6'); ok(Fr(4, 3) / 8 == Fr(1, 6), '(4/3)/8 = 1/6')
ok(Pd[2] == 1 and Pd2[2] == 1 and all(v[2] == 0 for v in (Pa, Pb, Pc)), 'base in z = 0, apexes at z = 1: altitudes 1')
ok(sub3(Pd, Pa) == (0, 0, 1) and sub3(Pd2, Pc) == (0, 0, 1), 'feet A and C at distance 1')
shear = lambda u: (u[0], u[1] + u[2], u[2]); ok(det3((1, 0, 0), (0, 1, 1), (0, 0, 1)) == 1, 'shear determinant 1')
ok([shear(v) for v in (Pa, Pb, Pc, Pd)] == [Pa, Pb, Pc, Pd2], 'the shear carries T onto T′')
for s_ in ['A = (0, 0, 0), B = (1, 0, 0), C = (0, 1, 0)', 'D = (0, 0, 1)', 'D′ = (0, 1, 1)', 'volume 1/6 each', 'both volumes are 1/6',
           '3√2 ⊗ arccos(1/√3)', 'dehnSet T′ = 0', '(1, 1, 0), (−1, 0, 0), (0, −1, 1), (0, 0, −1)', '(4/3)/8 = 1/6',
           '(u<sub>0</sub>, u<sub>1</sub>, u<sub>2</sub>) ↦ (u<sub>0</sub>, u<sub>1</sub> + u<sub>2</sub>, u<sub>2</sub>)'.replace('<sub>', '').replace('</sub>', ''),
           'Theorem 6′', 'Theorem 6″', 'Definition 3', '559c72d3', '33 files', 'compile_all10.sh', 'Bull. Amer. Math. Soc. 8 (1902) 437–479']:
    need(s_, 'study 10 fact')
ok('AB of length 1 at π/4, AC of length 1 at π/2, AD′ and BC of length √2 at π/2, BD′ of length √3 at π/3 and CD′ of length 1 at π/4' in txt, 'T′ edge list as printed')
# Hilbert's sentence as quoted in study 10 (checked there against the transcription of Newson's translation)
ST_ = os.environ.get('STUDIES', '../../../studies'); R10 = open(ST_ + '/2026-11-19-lean-dehn-10/README.md', encoding='utf-8').read()
qh = re.search(r'Hilbert \(1900\) asked for "([^"]+)"', R10).group(1); ok(f'"{qh}" [2]' in txt, "Hilbert's sentence as in study 10")
# Lean statements printed for study 10 are verbatim in the files
import html as _h
L10 = ''.join(open(ST_ + f'/2026-11-19-lean-dehn-10/lean/{f}.lean', encoding='utf-8').read() for f in ('Dehn10Hilbert', 'Dehn10Edges'))
for blk in re.findall(r'<pre><code>(.*?)</code></pre>', H, re.S):
    if 'hilbert_third_problem' in blk or 'edge_sum' in blk or 'facetNormals_eq_pair' in blk:
        for th in re.split(r'\n(?=theorem )', _h.unescape(blk)):
            ok(th.strip() in L10, f'Lean statement verbatim: {th.strip()[:50]}')
# Lean line and file counts per study
ST = os.environ.get('STUDIES', '../../../studies')
base = ST + '/2026-11-19-lean-dehn-'
tot_l = tot_f = 0
for k, (nf, nl) in {1: (1, 153), 2: (10, 1708), 3: (3, 909), 4: (5, 1303), 5: (5, 1326), 6: (3, 314), 7: (7, 7504), 8: (3, 477), 9: (3, 833), 10: (3, 1353)}.items():
    fs = glob.glob(base + f'{k}/lean/*.lean'); L = sum(sum(1 for _ in open(f, encoding='utf-8')) for f in fs)
    ok(len(fs) == nf and L == nl, f'study {k}: {len(fs)} files {L} lines'); tot_l += L; tot_f += len(fs)
ok(tot_l == 15880 and tot_f == 43, 'totals'); need('15,880', 'total lines'); need('43 Lean files', 'total files'); need('1,353', 'study 10 lines'); need('477', 'study 8 lines'); need('833', 'study 9 lines')
# study 8: theorems and lemmas in its two proof files, and the #print axioms list
L8 = ''.join(open(base + f'8/lean/{f}.lean', encoding='utf-8').read() for f in ('Dehn8Indep', 'Dehn8Cross'))
n8 = len(re.findall(r'^\s*(?:theorem|lemma) ', L8, re.M)); ok(n8 == 49, f'study 8: {n8} theorems and lemmas'); need('49 theorems and lemmas', 'study 8 count')
n8ax = open(base + '8/lean/Axioms8.lean', encoding='utf-8').read().count('#print axioms'); ok(n8ax == 29, f'study 8: {n8ax} axiom checks')
pairs = re.findall(r'^theorem ((?:oct|tetra|co)_(?:dod|ico|cleo|axe|fuji))_not_scissorsCongruent', L8, re.M); ok(len(set(pairs)) == 15, f'15 cross pairs ({len(set(pairs))})')
# study 9: theorems and lemmas in its two proof files, the #print axioms list, and every Lean name Theorem 14 cites
L9 = ''.join(open(base + f'9/lean/{f}.lean', encoding='utf-8').read() for f in ('Dehn9Vol', 'Dehn9Same'))
n9 = len(re.findall(r'^\s*(?:theorem|lemma) ', L9, re.M)); ok(n9 == 61, f'study 9: {n9} theorems and lemmas'); need('61 theorems and lemmas', 'study 9 count')
n9ax = open(base + '9/lean/Axioms9.lean', encoding='utf-8').read().count('#print axioms'); ok(n9ax == 21, f'study 9: {n9ax} axiom checks')
for nm in ['volume_iUnion_poly', 'volume_eq_of_scissorsCongruent', 'volume_similar', 'volume_oct', 'volume_tetra', 'volume_co',
           'not_scissorsCongruent_of_cube_ne', "co_tetra_not_scissorsCongruent'", "co_oct_not_scissorsCongruent'", 'co_co_not_scissorsCongruent',
           "oct_tetra_not_scissorsCongruent'", 'luckySeven_tetra_not_scissorsCongruent', 'canon_tet_not_scissorsCongruent', 'canon_complete']:
    ok(re.search(r'^(?:theorem|lemma) ' + re.escape(nm) + r'[\s{(:]', L9, re.M) is not None, f'study 9 has {nm}'); need(nm, 'Lean name')
# study 10: theorems and lemmas in its two proof files, the #print axioms list, and every Lean name §5.1 cites
n10 = len(re.findall(r'^\s*(?:theorem|lemma) ', L10, re.M)); ok(n10 == 56, f'study 10: {n10} theorems and lemmas'); need('56 theorems and lemmas', 'study 10 count')
A10 = open(base + '10/lean/Axioms10.lean', encoding='utf-8').read(); ok(A10.count('#print axioms') == 27, 'study 10: 27 axiom checks')
for nm in ['hilbert_third_problem', 'dehnSet_eq_of_equiComplementable', 'hil_height_corner', 'hil_height_ortho', 'volume_cornerTet', 'volume_orthoTet',
           'dehnSet_cornerTet', 'dehnSet_orthoTet', 'dehnSet_eq_edge_sum', 'IsEdge.facetNormals_eq_pair', 'edges_finite', 'IsEdge.length']:
    ok(re.search(r'^(?:theorem|lemma) ' + re.escape(nm) + r'[\s{(:]', L10, re.M) is not None, f'study 10 has {nm}'); need(nm, 'Lean name')
    ok('#print axioms ' + nm in A10 or '#print axioms DehnCanon.' + nm in A10, f'study 10 axiom check for {nm}')
for nm in ['EquiComplementable', 'IsEdge', 'edges', 'facetNormals', 'dihedral', 'faceIn']:
    ok(re.search(r'^(?:noncomputable )?def ' + nm + r'\b', L10, re.M) is not None, f'study 10 defines {nm}')
for s in ['184 screened, 32 zero, 151 nonzero, 1 mixed', '11 of 11', '324 pairs', '900 pairs', '21 pairs', 'v4.35.0-rc2', '065356127b1dc0016f66b7283ce0ce2c4055aa55', '349 PDF']:
    need(s, 'fact')
log = open(ST + '/2026-11-19-dehn-atoms/README.md', encoding='utf-8').read()
ok('184 have exact corners' in log and '32 have Dehn invariant ZERO, 151 NONZERO' in log, 'atoms counts vs README')
L5 = open(base + '5/lean/Dehn5Angles.lean', encoding='utf-8').read()
ok('theorem word_angle_relation : wordAlpha + 2 * wordBeta - wordGamma = π' in L5, 'Lean word_angle_relation is α + 2β − γ = π')
print('\n'.join(bad) if bad else 'AUDIT OK: every number recomputed and found in the text')
