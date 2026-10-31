# Splash Rules II, approximants, part 3: cubic approximants of the 3D Penrose (Ammann-Kramer-Neri) tiling, tile counts (exact).
# Z^6 with physical icosahedral star e_i (columns of PHYS with tau irrational); the approximant n/m replaces tau by the Fibonacci
# ratio F(k+1)/F(k) (1/1, 2/1, 3/2, 5/3, 8/5, 13/8, 21/13). The period lattice is Z^6 cap E' (E' the rational 3-space);
# in the canonical tiling the number of rhombohedra with edges {e_i, e_j, e_k} per period is |3x3 minor| of a basis of it.
# ~/geom/bin/python ico.py out/
import sys, os, json, itertools
from fractions import Fraction as Fr
from qf import QF
from zono import int_kernel, det

OUT = sys.argv[1]
def phys(t):
    # columns e_1..e_6: (1,t,0), (-1,t,0), (0,1,t), (0,-1,t), (t,0,1), (-t,0,1)
    return [[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]]
TRI = list(itertools.combinations(range(6), 3))
TAU = QF(Fr(1, 2), Fr(1, 2), 5)
P = phys(TAU)
vol = {T: det([[P[r][c] for c in T] for r in range(3)]) for T in TRI}
absv = {T: (v if v > 0 else -v) for T, v in vol.items()}
big = max(absv.values(), key=float); small = min(absv.values(), key=float)
kind = {T: ('prolate' if absv[T] == big else 'oblate') for T in TRI}
assert all(absv[T] in (big, small) for T in TRI) and big / small == TAU
print('irrational: prolate/oblate volumes', big, small, 'ratio tau; triples prolate', sum(k == 'prolate' for k in kind.values()), 'oblate', sum(k == 'oblate' for k in kind.values()))
sgn = {T: vol[T].sign() for T in TRI}
# limit tile shares: in the canonical tiling the frequency of {ijk} is proportional to the internal minor, |minor of the complement|
TAUc = TAU.conj()
Q = phys(TAUc)
ivol = {T: det([[Q[r][c] for c in T] for r in range(3)]) for T in TRI}
comp = {T: tuple(sorted(set(range(6)) - set(T))) for T in TRI}
w = {T: (ivol[comp[T]] if ivol[comp[T]] > 0 else -ivol[comp[T]]) for T in TRI}
tot = sum(w.values(), QF(0, 0, 5))
lim_pro = sum((w[T] for T in TRI if kind[T] == 'prolate'), QF(0, 0, 5)) / tot
print('limit prolate share', lim_pro, float(lim_pro), ' (1/tau =', float(1 / TAU), ')')
assert lim_pro == 1 / TAU

fib = [1, 1]
while len(fib) < 12: fib.append(fib[-1] + fib[-2])
rows = []
for k in range(0, 9):
    p, q = fib[k + 1], fib[k]          # tau ~ p/q : 1/1, 2/1, 3/2, 5/3, ...
    M = [[x * q for x in r] for r in phys(Fr(p, q))]
    M = [[int(x) for x in r] for r in M]
    N = int_kernel(M)                  # annihilator lattice (3 vectors)
    L = int_kernel(N)                  # Z^6 cap E', saturated (3 vectors)
    assert len(L) == 3
    mn = {T: det([[L[r][c] for c in T] for r in range(3)]) for T in TRI}
    s = 1 if sum(mn[T] * sgn[T] for T in TRI) > 0 else -1
    mn = {T: s * v for T, v in mn.items()}
    okS = all(mn[T] * sgn[T] >= 0 for T in TRI)
    cnt = {T: abs(v) for T, v in mn.items()}
    pro = sum(cnt[T] for T in TRI if kind[T] == 'prolate'); obl = sum(cnt[T] for T in TRI if kind[T] == 'oblate')
    # unsaturated (cubic) cell: rows of M scaled; index of the sublattice spanned by M's rows in L
    cub = {T: det([[M[r][c] for c in T] for r in range(3)]) for T in TRI}
    idx = Fr(sum(abs(v) for v in cub.values()), pro + obl)
    zero = [T for T in TRI if cnt[T] == 0]
    rows.append({'approximant': f'{p}/{q}', 'prolate': pro, 'oblate': obl, 'vertices': pro + obl, 'sign_ok': okS, 'zero_minors': len(zero),
                 'index_cubic_over_primitive': str(idx), 'prolate_cubic': int(pro * idx), 'oblate_cubic': int(obl * idx), 'share_prolate': str(Fr(pro, pro + obl)),
                 'basis': L})
    print(f'{p}/{q}: per primitive cell prolate {pro}, oblate {obl} (vertices {pro + obl}); signs as in E: {okS}; zero minors {len(zero)}; cubic cell = {idx} primitive cells -> {pro * idx} + {obl * idx}; prolate share {Fr(pro, pro + obl)} = {pro / (pro + obl):.6f}')
# laws in p, q (cubic cell spanned by the rows of M)
import sympy as sp
pp, qq = sp.symbols('p q')
Ms = sp.Matrix(phys(pp / qq)) * qq
proS = sp.factor(sum(sgn[T] * Ms[:, list(T)].det() for T in TRI if kind[T] == 'prolate'))
oblS = sp.factor(sum(sgn[T] * Ms[:, list(T)].det() for T in TRI if kind[T] == 'oblate'))
print('cubic cell (rows of the rational projection times q): prolate', proS, '; oblate', oblS)
for r in rows:
    p, q = map(int, r['approximant'].split('/'))
    assert proS.subs({pp: p, qq: q}) == r['prolate_cubic'] and oblS.subs({pp: p, qq: q}) == r['oblate_cubic'], r
print('cubic-cell formulas match every approximant')
json.dump({'limit_prolate_share': repr(lim_pro), 'rows': rows, 'formula': {'prolate': str(proS), 'oblate': str(oblS)}}, open(os.path.join(OUT, 'ico.json'), 'w'), indent=0)
