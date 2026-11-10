"""#61 below 1/4, the two-parameter Hopscotch (DICTO 10 Nov "run the walk with s symbolic"). s enters only the vertical metric
(G33 = s·2n²/3), so every plane has a normal linear in s and an offset linear in s and λ; every corner (3 planes) is rational in
(s, λ) and affine in λ. For each cell of the chamber map (a polygon): build all power cells of the six words at a sample point, re-solve
every corner symbolically, prove every plane's slack >= 0 on the WHOLE polygon (affine in λ: check the two boundary walls, exact
rational functions of s, roots located exactly), then the volumes and the Swap defect D(s, λ) symbolically, compared with the closed
forms. Usage: python swap_cells2.py <cell> ; cells: b (s in [1/7,1/4], -9s/8..-(4-s)/24), c1 ([1/8,1/7], -9s/8..-5s/8),
c2 ([1/7,1/4], -(4-s)/24..-5s/8), d1 ([1/8,1/4], -5s/8..-s/8), d2 ([1/8,1/4], -s/8..3s/8)."""
import sys, os, itertools, time
from fractions import Fraction as Fr
import sympy as sp
# helper modules from the repository itself (11 Nov 2026, #104 v2 reproducibility): byte-identical to the copies the v1 run used
_R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
for _p in ('2026-10-25-stackings/scripts', '2026-10-27-splash-rules/proof', '2026-10-27-splash-rules/scripts'): sys.path.insert(0, os.path.join(_R, _p))
from engine import Net, Cell, gdot, vsub, order
from splash import net_for
from validate import layer_type, ROLE_OF
S, L = sp.symbols('s lam')
WORDS = ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']
q = sp.Rational
CELLS = {'b': (q(1, 7), q(1, 4), -9 * S / 8, -(4 - S) / 24), 'c1': (q(1, 8), q(1, 7), -9 * S / 8, -5 * S / 8),
         'c2': (q(1, 7), q(1, 4), -(4 - S) / 24, -5 * S / 8), 'd1': (q(1, 8), q(1, 4), -5 * S / 8, -S / 8), 'd2': (q(1, 8), q(1, 4), -S / 8, 3 * S / 8)}
FORM = {'b': ((1 - 4 * S) ** 2 * (72 * L + 8 + 13 * S) / (108 * S), -(1 - 4 * S) ** 3 / (54 * S)),
        'c1': ((8 * L + 5 * S) ** 3 / (64 * S), -(8 * L + 5 * S) ** 2 * (8 * L + 2 - 3 * S) / (64 * S))}
FORM['c2'] = FORM['c1']; FORM['d1'] = FORM['d2'] = (sp.Integer(0), sp.Integer(0))
cell = sys.argv[1]; sa, sb, lo, hi = CELLS[cell]
D2 = int(os.environ.get('D2', '12'))   # neighbourhood (squared distance); panel 10 Nov: prove farther sites never cut (rho bound below)
RHO = [0.0]
s0 = (sa + sb) / 2; l0 = (lo.subs(S, s0) + hi.subs(S, s0)) / 2
s0f, l0f = Fr(int(s0.p), int(s0.q)), Fr(int(l0.p), int(l0.q))
print(f'START cell {cell}: s in [{sa}, {sb}], λ from {lo} to {hi}; sample ({s0}, {l0})', flush=True)
K = sp.QQ.frac_field(S)
from sympy.polys.matrices import DomainMatrix
def Kc(x): return K.convert(sp.Rational(x.numerator, x.denominator)) if isinstance(x, Fr) else K.from_sympy(sp.sympify(x))
from math import comb
def _dense(pe):                                            # PolyElement of QQ[s] -> Fraction coefficients, highest degree first
    return [Fr(int(c.numerator), int(c.denominator)) for c in pe.to_dense()] if pe else [Fr(0)]
def _bern_sign(cf, a, b):
    """sign of the polynomial (coeffs cf, highest first) on [a, b] if the Bernstein coefficients all share one strict sign, else None"""
    n = len(cf) - 1; q = [Fr(0)] * (n + 1)                # p(a + (b - a) t) = sum q_j t^j
    for k, c in enumerate(reversed(cf)):                  # c * (a + h t)^k
        h = b - a
        for j in range(k + 1): q[j] += c * comb(k, j) * a ** (k - j) * h ** j
    bc = [sum(Fr(comb(i, j), comb(n, j)) * q[j] for j in range(i + 1)) for i in range(n + 1)]
    if all(x > 0 for x in bc): return 1
    if all(x < 0 for x in bc): return -1
    return None
SA, SB = Fr(int(sa.p), int(sa.q)), Fr(int(sb.p), int(sb.q))
def nonneg_K(f):
    """f in K: fast exact test first (Bernstein: no root of numerator or denominator in [sa, sb]), exact fallback otherwise"""
    sn = _bern_sign(_dense(f.numer), SA, SB); sd = _bern_sign(_dense(f.denom), SA, SB)
    if sn is not None and sd is not None: return sn * sd > 0
    return nonneg_on(K.to_sympy(f))
def nonneg_on(e):
    """e (sympy, rational in s): >= 0 on [sa, sb], exact: no odd-multiplicity root of numerator or denominator strictly inside"""
    nu, de = sp.fraction(sp.cancel(e))
    for poly in (nu, de):
        P = sp.Poly(poly, S)
        if P.degree() <= 0: continue
        for fac, m in P.sqf_list()[1]:
            if m % 2 == 0: continue
            inside = fac.count_roots(sa, sb) - (1 if fac.eval(sa) == 0 else 0) - (1 if fac.eval(sb) == 0 else 0)
            if inside > 0: return False
    return sp.cancel(e).subs(S, (sa + sb) / 2) >= 0
loK, hiK = K.from_sympy(lo), K.from_sympy(hi)
def triple(a, b, c):
    """a, b, c = (P0, P1) with P = P0 + λ P1 (lists of K); a.(b x c) as [c0, c1, c2, c3] in λ"""
    out = [K.zero] * 4
    for i_, j_, k_ in itertools.product(range(2), repeat=3):
        A_, B_, C_ = a[i_], b[j_], c[k_]
        out[i_ + j_ + k_] += A_[0] * (B_[1] * C_[2] - B_[2] * C_[1]) + A_[1] * (B_[2] * C_[0] - B_[0] * C_[2]) + A_[2] * (B_[0] * C_[1] - B_[1] * C_[0])
    return out
ok = True; V = {}; t0 = time.time(); nchk = 0
for w in WORDS:
    n = len(w); spec0 = net_for(w, s0f); net0 = Net(w, spec0['G'], spec0['T'], spec0['motif'], spec0['w']); wc = spec0['w']
    g33 = K.from_sympy(S * sp.Rational(2, 3) * n * n)
    for i in range(3 * n):
        c = Cell(net0, i, (l0f,), Fr(D2)); k = i // 3
        key = (ROLE_OF[i % 3],) + tuple(layer_type(w, k + j) for j in (-1, 0, 1, 2))
        if c.empty: vol = [K.zero] * 4
        else:
            ki, ci = net0.motif[i]
            q2 = lambda x: Kc(x[0] * x[0] + x[0] * x[1] + x[1] * x[1]) + g33 * Kc(x[2] * x[2])
            PL = []
            for h in c.H:                                     # plane n.x <= b0 + λ b1, with s symbolic (only G33 carries s)
                cc = h['c']; kj = net0.motif[h['j']][0]; dv = vsub(cc, ci)
                nvec = [Kc(2 * (dv[0] + Fr(1, 2) * dv[1])), Kc(2 * (Fr(1, 2) * dv[0] + dv[1])), g33 * Kc(2 * dv[2])]
                PL.append((nvec, q2(cc) - q2(ci) + Kc(Fr(wc[ki][0] - wc[kj][0])), Kc(Fr(wc[ki][1] - wc[kj][1]))))
            corners = []
            for cr in c.corners:
                sol = None
                for tri in itertools.combinations(sorted(cr['on']), 3):
                    A = DomainMatrix([[PL[t][0][r] for r in range(3)] for t in tri], (3, 3), K)
                    if A.det() == K.zero: continue
                    rows = A.inv().to_list(); r0 = [PL[t][1] for t in tri]; r1 = [PL[t][2] for t in tri]
                    sol = ([sum((rows[r][t] * r0[t] for t in range(3)), K.zero) for r in range(3)],
                           [sum((rows[r][t] * r1[t] for t in range(3)), K.zero) for r in range(3)]); break
                assert sol is not None; corners.append(sol)
                # rho: the corner's metric distance from its site over a grid of the cell polygon (for the neighbourhood bound)
                for ss in [sa + (sb - sa) * q / 8 for q in range(9)]:
                    l_lo, l_hi = float(lo.subs(S, ss)), float(hi.subs(S, ss)); sf = float(ss)
                    for ll in [l_lo + (l_hi - l_lo) * q / 8 for q in range(9)]:
                        ev = lambda e: float(sp.sympify(K.to_sympy(e)).subs(S, ss))
                        x = [ev(sol[0][r]) + ll * ev(sol[1][r]) for r in range(3)]
                        dv = [x[r] - float(ci[r]) for r in range(3)]
                        RHO[0] = max(RHO[0], (dv[0] ** 2 + dv[0] * dv[1] + dv[1] ** 2 + sf * 2 / 3 * n * n * dv[2] ** 2) ** 0.5)
                for kk, (nv, b0, b1) in enumerate(PL):          # slack = c0 + λ c1 >= 0 on the polygon: check both boundary walls exactly
                    c0 = b0 - sum((nv[r] * sol[0][r] for r in range(3)), K.zero); c1 = b1 - sum((nv[r] * sol[1][r] for r in range(3)), K.zero)
                    if c0 == K.zero and c1 == K.zero: continue
                    nchk += 1
                    if not (nonneg_K(c0 + c1 * loK) and nonneg_K(c0 + c1 * hiK)):
                        ok = False; print(f'   VIOLATION word {w} site {i} plane {kk}: slack {sp.factor(K.to_sympy(c0))} + λ·{sp.factor(K.to_sympy(c1))}', flush=True)
            vol = [K.zero] * 4
            for kf, pts in c.faces().items():
                idx = [c.corners.index(p) for p in order(pts, c.H[kf]['n'])]; P_ = [corners[t] for t in idx]
                for t in range(1, len(P_) - 1):
                    tr = triple(P_[0], P_[t], P_[t + 1]); vol = [vol[e] + tr[e] * Kc(Fr(n, 6)) for e in range(4)]
        if key in V and any(V[key][e] != vol[e] for e in range(4)): ok = False; print('   CLASH', key, w, flush=True)
        V.setdefault(key, vol)
        print(f'PROGRESS {(WORDS.index(w) + (i + 1) / (3 * n)) / len(WORDS):.3f} word {w} site {i} ({time.time() - t0:.0f} s, {nchk} slack checks)', flush=True)
V = {k_: sum(K.to_sympy(v[e]) * L ** e for e in range(4)) for k_, v in V.items()}
fo, ft = FORM[cell]
for r, f in (('oct', fo), ('tetX', ft), ('tetY', ft)):
    for a, b in itertools.product('ch', repeat=2):
        ks = [(r, a, x, y, b) for x, y in (('c', 'h'), ('h', 'c'), ('c', 'c'), ('h', 'h'))]
        D = sp.cancel(V[ks[0]] + V[ks[1]] - V[ks[2]] - V[ks[3]])
        good = sp.cancel(D - f) == 0; ok &= good
        print(f'   {r} {a}{b}: D = {sp.factor(D)}  {"= closed form" if good else "≠ " + str(f)}', flush=True)
import math
Dn = math.sqrt(D2); rho = RHO[0] * 1.05                                   # 5 % margin over the grid maximum
bound = (Dn - rho) ** 2 >= rho ** 2 + 0.35                                # 0.35 > |w_j - w_i| = |λ| on #61's range
print(f'neighbourhood: D^2 = {D2}; largest corner distance on the grid {RHO[0]:.4f} (with 5% margin {rho:.4f}); bound (D - rho)^2 >= rho^2 + 0.35: {bound}', flush=True)
ok &= bound
print(f'FINAL ok (cell {cell} proved for all s in [{sa}, {sb}], neighbourhood D^2 = {D2})' if ok else 'FINAL FAIL')
