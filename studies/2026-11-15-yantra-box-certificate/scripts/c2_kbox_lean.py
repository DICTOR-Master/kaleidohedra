"""Lean export of the Krawczyk box (step 4 of the Lean plan).  Writes lean/YantraCert/KBox.lean.

Two boxes around Theorem 10's solution in the main coordinates (u, tau, rho), for F~ = (G~, H~, D~) of data/polys-utr.json:
  X  = the certificate's hole "Krawczyk" (data/holes-main.json; half-width 2^-22): at most one zero (contraction, `krawczyk_unique`);
  Xs = a box of half-width 2^-100 around a 120-digit Newton zero: a zero exists (Banach, `krawczyk_exists`), and Xs lies in X.
Slopes are the polynomial slopes of YantraCert.Krawczyk (Krawczyk and Neumaier 1985), enclosed by their corner sums; Y is a
2^-60 dyadic rounding of the inverse Jacobian at the centre; every bound is checked here in exact rationals before it is written,
and again in Lean (kernel evaluation of the corner sums, norm_num for the 3 x 3 inequalities).
Usage: c2_kbox_lean.py   FINAL ok iff all checks hold."""
import json, os, sys
from fractions import Fraction as Fq
import mpmath as mp
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
data = json.load(open(D_('data', 'polys-utr.json')))
NAMES = ['G', 'H1', 'D']
F = [[(tuple(e), int(c)) for e, c in data['F'][k]] for k in NAMES]
DEG = [[max(e[j] for e, c in p) for j in range(3)] for p in F]
def split(p): return [(e, c) for e, c in p if c > 0], [(e, -c) for e, c in p if c < 0]
def ev(p, x): return sum(c * x[0]**e[0] * x[1]**e[1] * x[2]**e[2] for e, c in p)
def gs(a, t): return a * t**(a - 1) if a > 0 else 0
def corner(p, j, t):
    """slope part j of a natural-coefficient polynomial at (t, t)"""
    s = 0
    for e, c in p:
        f = [t[0]**e[0], t[1]**e[1], t[2]**e[2]]; f[j] = gs(e[j], t[j]); s += c * f[0] * f[1] * f[2]
    return s
mp.mp.dps = 130
hole = [h for h in json.load(open(D_('data', 'holes-main.json')))['holes'] if h['name'] == 'Krawczyk'][0]['box']
X = [(Fq(a), Fq(b)) for a, b in hole]
def jac(x):
    out = []
    for p in F:
        row = []
        for j in range(3):
            row.append(sum(c * e[j] * x[0]**(e[0] - (j == 0)) * x[1]**(e[1] - (j == 1)) * x[2]**(e[2] - (j == 2)) for e, c in p if e[j] > 0))
        out.append(row)
    return out
# a 120-digit zero by Newton from the centre of X
x = [mp.mpf(((a + b) / 2).numerator) / ((a + b) / 2).denominator for a, b in X]
for it in range(12):
    Fv = mp.matrix([ev(p, x) for p in F]); Jv = mp.matrix(jac(x)); dx = mp.lu_solve(Jv, Fv); x = [x[i] - dx[i] for i in range(3)]
print('zero:', [mp.nstr(v, 40) for v in x], '|F| =', mp.nstr(max(abs(ev(p, x)) for p in F), 5))
def analyse(Lo, Hi, Q, Yf):
    """exact checks for the box [Lo/Q, Hi/Q]; returns dict of data (Fractions)"""
    lo = [Fq(n, Q) for n in Lo]; hi = [Fq(n, Q) for n in Hi]
    c = [(lo[j] + hi[j]) / 2 for j in range(3)]; r = [(hi[j] - lo[j]) / 2 for j in range(3)]
    Y = [[Fq(int(mp.nint(Yf[i, k] * 2**60)), 2**60) for k in range(3)] for i in range(3)]
    l = [[None] * 3 for _ in range(3)]; h = [[None] * 3 for _ in range(3)]
    for k, p in enumerate(F):
        pp, pn = split(p)
        for j in range(3):
            l[k][j] = corner(pp, j, lo) - corner(pn, j, hi); h[k][j] = corner(pp, j, hi) - corner(pn, j, lo)
    M = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            a = (1 if i == j else 0) - sum(Y[i][k] * (l[k][j] + h[k][j]) / 2 for k in range(3))
            s = sum(abs(Y[i][k]) * (h[k][j] - l[k][j]) / 2 for k in range(3))
            v = abs(a) + s; M[i][j] = Fq(-((-v.numerator * 2**60) // v.denominator), 2**60)   # rounded up
            assert M[i][j] >= v
    Fc = [ev(p, c) for p in F]
    out = {'lo': lo, 'hi': hi, 'c': c, 'r': r, 'Y': Y, 'l': l, 'h': h, 'M': M, 'Fc': Fc}
    out['contract'] = [sum(M[i][j] * r[j] for j in range(3)) / r[i] for i in range(3)]
    out['incl'] = [(abs(sum(Y[i][k] * Fc[k] for k in range(3))) + sum(M[i][j] * r[j] for j in range(3))) / r[i] for i in range(3)]
    return out
Q1 = 1
for a, b in X: Q1 = max(Q1, a.denominator, b.denominator)
assert all(Q1 % a.denominator == 0 and Q1 % b.denominator == 0 for a, b in X)
L1 = [int(a * Q1) for a, b in X]; H1 = [int(b * Q1) for a, b in X]
cX = [(a + b) / 2 for a, b in X]
Yf = mp.inverse(mp.matrix(jac([mp.mpf(v.numerator) / v.denominator for v in cX])))
A1 = analyse(L1, H1, Q1, Yf)
print('X: contraction ratios', [float(v) for v in A1['contract']], 'inclusion ratios', [float(v) for v in A1['incl']])
# small box
Q2 = 2**140
C2 = [int(mp.nint(v * Q2)) for v in x]; R2 = 2**40
L2 = [n - R2 for n in C2]; H2 = [n + R2 for n in C2]
Yf2 = mp.inverse(mp.matrix(jac(x)))
A2 = analyse(L2, H2, Q2, Yf2)
print('Xs: contraction ratios', [float(v) for v in A2['contract']], 'inclusion ratios', [float(v) for v in A2['incl']])
Kc = max(A2['contract']); K2 = Fq(-((-Kc.numerator * 2**20) // Kc.denominator), 2**20)
Ym = A2['Y']
# exact inverse of Y (Gauss-Jordan in Fractions)
Aug = [Ym[i][:] + [Fq(int(i == j)) for j in range(3)] for i in range(3)]
for col in range(3):
    piv = max(range(col, 3), key=lambda r_: abs(Aug[r_][col])); Aug[col], Aug[piv] = Aug[piv], Aug[col]
    pv = Aug[col][col]; Aug[col] = [v / pv for v in Aug[col]]
    for r_ in range(3):
        if r_ != col:
            f = Aug[r_][col]; Aug[r_] = [Aug[r_][t] - f * Aug[col][t] for t in range(6)]
Z = [row[3:] for row in Aug]
assert all(sum(Z[i][k] * Ym[k][l] for k in range(3)) == (1 if i == l else 0) for i in range(3) for l in range(3))
sub = all(A1['lo'][j] <= A2['lo'][j] and A2['hi'][j] <= A1['hi'][j] for j in range(3))
ok = all(v < 1 for v in A1['contract']) and all(v <= 1 for v in A2['incl']) and K2 < 1 and all(v <= K2 for v in A2['contract']) and sub
print('Xs inside X:', sub, '; K =', float(K2), '; all checks:', ok)

# ---------------- Lean output ----------------
def rl(q):
    q = Fq(q)
    if q.denominator == 1: return f'({q.numerator} : ℝ)'
    return f'(({q.numerator} : ℝ) / {q.denominator})'
def npl(terms):
    s = '.nil'
    for e, c in reversed(terms): s = f'(.cons {c} {e[0]} {e[1]} {e[2]} {s})'
    return s
def mat(Mx): return '![' + ', '.join('![' + ', '.join(rl(v) for v in row) + ']' for row in Mx) + ']'
def vec(v): return '![' + ', '.join(rl(t) for t in v) + ']'
out = ['import YantraCert.Krawczyk', '', 'set_option maxRecDepth 100000', 'set_option maxHeartbeats 4000000', '',
       '/-! # The Krawczyk box of the main chart (generated by scripts/c2_kbox_lean.py)',
       '',
       'The equations `G~, H~, D~` in the main coordinates `(u, τ, ρ)` (data/polys-utr.json, not rescaled).  The box `X` is the',
       "certificate's hole `Krawczyk` (half-width 2^-22); `Xs` (half-width 2^-100) lies inside it.  Krawczyk's test (R. Krawczyk 1969;",
       'uniqueness form R. E. Moore 1977, A. Neumaier 1990 Thm 5.1.7; slopes after Krawczyk and Neumaier 1985) gives at most one zero',
       "in `X`, and a zero in `Xs` by Banach's fixed-point theorem (Mathlib `ContractingWith.fixedPoint`). -/", '',
       'namespace YantraCert.KBox', 'open YantraCert', '']
for k, p in enumerate(F):
    pp, pn = split(p)
    out.append(f'noncomputable def P{k} : SP := ⟨{DEG[k][0]}, {DEG[k][1]}, {DEG[k][2]}, {npl(pp)}, {npl(pn)}⟩   -- {NAMES[k]}~')
out += ['', 'theorem P_deg : P0.degOK = true ∧ P1.degOK = true ∧ P2.degOK = true := ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩',
        '', 'noncomputable def Fv : Fin 3 → SP := ![P0, P1, P2]',
        '/-- the system `F~` as functions on `ℝ³` -/',
        'noncomputable def F (k : Fin 3) (x : Fin 3 → ℝ) : ℝ := (Fv k).eval (x 0) (x 1) (x 2)', '']
def emit_box(tag, A, Q, Lo, Hi):
    s = [f'/-! ## Box {tag} -/', f'def Q{tag} : Nat := {Q}', f'def L{tag} : Fin 3 → Nat := ![{", ".join(map(str, Lo))}]',
         f'def H{tag} : Fin 3 → Nat := ![{", ".join(map(str, Hi))}]',
         f'noncomputable def c{tag} : Fin 3 → ℝ := fun j => ((L{tag} j : ℝ) / Q{tag} + (H{tag} j : ℝ) / Q{tag}) / 2',
         f'noncomputable def r{tag} : Fin 3 → ℝ := fun j => ((H{tag} j : ℝ) / Q{tag} - (L{tag} j : ℝ) / Q{tag}) / 2',
         f'noncomputable def lo{tag} : Fin 3 → Fin 3 → ℝ := {mat(A["l"])}', f'noncomputable def hi{tag} : Fin 3 → Fin 3 → ℝ := {mat(A["h"])}',
         f'noncomputable def Y{tag} : Fin 3 → Fin 3 → ℝ := {mat(A["Y"])}', f'noncomputable def M{tag} : Fin 3 → Fin 3 → ℝ := {mat(A["M"])}', '']
    # corner sums by the kernel
    for k in range(3):
        pp, pn = split(F[k])
        for j, nm in enumerate(('sx', 'sy', 'sz')):
            for side, N, P_, lbl in ((0, Lo, pp, 'ppL'), (1, Hi, pp, 'ppH'), (2, Lo, pn, 'pnL'), (3, Hi, pn, 'pnH')):
                t = [Fq(n, Q) for n in N]; val = corner(P_, j, t)
                dx = DEG[k][0] - (j == 0); dy = DEG[k][1] - (j == 1); dz = DEG[k][2] - (j == 2)
                nat = val * Fq(Q)**(dx + dy + dz); assert nat.denominator == 1
                part = 'pp' if lbl.startswith('pp') else 'pn'
                s.append(f'theorem e{tag}_{k}{j}_{lbl} : (P{k}.{part}.{nm} P{k}.Dx P{k}.Dy P{k}.Dz Q{tag} (({"L" if lbl.endswith("L") else "H"}{tag}) 0) '
                         f'(({"L" if lbl.endswith("L") else "H"}{tag}) 1) (({"L" if lbl.endswith("L") else "H"}{tag}) 2)) = {nat.numerator} := by decide +kernel')
    return s
out += emit_box('X', A1, Q1, L1, H1)
out += emit_box('S', A2, Q2, L2, H2)
# values at the centre of Xs (grid of denominator 2 Q2)
for k in range(3):
    pp, pn = split(F[k])
    cn = [L2[j] + H2[j] for j in range(3)]
    for part, P_ in (('pp', pp), ('pn', pn)):
        val = ev(P_, [Fq(n, 2 * Q2) for n in cn]) * Fq(2 * Q2)**sum(DEG[k]); assert val.denominator == 1
        out.append(f'theorem vS_{k}_{part} : P{k}.{part}.vq P{k}.Dx P{k}.Dy P{k}.Dz (2 * QS) (LS 0 + HS 0) (LS 1 + HS 1) (LS 2 + HS 2) = {val.numerator} := by decide +kernel')
out += [f'noncomputable def FcS : Fin 3 → ℝ := {vec(A2["Fc"])}', f'noncomputable def ZS : Fin 3 → Fin 3 → ℝ := {mat(Z)}',
        f'noncomputable def KS : ℝ := {rl(K2)}', '']
out += ['end YantraCert.KBox', '']
open(D_('lean', 'YantraCert', 'KBoxData.lean'), 'w').write('\n'.join(out))
json.dump({'X': {'contract': [str(v) for v in A1['contract']], 'incl': [str(v) for v in A1['incl']]},
           'Xs': {'centre_num': [str(n) for n in C2], 'Q': str(Q2), 'radius_num': str(R2), 'contract': [str(v) for v in A2['contract']],
                  'incl': [str(v) for v in A2['incl']], 'K': str(K2)}, 'Xs_in_X': sub, 'ok': ok},
          open(D_('data', 'lean-kbox.json'), 'w'), indent=1)
print('wrote lean/YantraCert/KBoxData.lean')
print('FINAL ok' if ok else 'FINAL FAIL')
