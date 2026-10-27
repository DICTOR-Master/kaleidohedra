# Volume Swap Rule below s0, step (1) (DICTO 2026-10-27): exact half volumes of the central-gap pieces in the 16 four-layer windows.
# For each window (types of layers k-1, k, k+1, k+2 = hc[0..3]; central gap between k and k+1, t = hc[1], t' = hc[2]) and each role:
#   dLo = Vlow(actual) - Vlow(pure t), dUp = Vup(actual) - Vup(pure t')  (coordinate volumes in (x, y, zeta), exact rationals)
# and the table says which window letters each defect depends on.  Usage: python additive.py <s> <lam,...>
import sys, os, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
from validate import Net, Cell, net_for, half, ROLE_OF
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts'))
from catalogue import word_for
def det3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
def hull_vol(P):
    P = sorted(set(P))
    if len(P) < 4: return Fr(0)
    A = np.array([[float(x) for x in p] for p in P])
    if np.linalg.matrix_rank(A[1:] - A[0], tol=1e-9) < 3: return Fr(0)
    H = ConvexHull(A); c = tuple(sum(p[r] for p in P) / len(P) for r in range(3)); V = Fr(0)
    for f in H.simplices:
        a, b, d = (tuple(P[k][r] - c[r] for r in range(3)) for k in f); V += abs(det3(a, b, d)) / 6
    return V
def halves_vol(net, n, i, k, lam):
    c = Cell(net, i, (lam,), Fr(12))
    if c.empty: return Fr(0), Fr(0)
    zc = (k + Fr(1, 2)) / n
    tz = lambda pts: [(p[0], p[1], p[2] * n) for p in pts]            # zeta in layer spacings
    return hull_vol(tz(half(c, lam, zc, False))), hull_vol(tz(half(c, lam, zc, True)))
s = Fr(sys.argv[1])
def build(w): spec = net_for(w, s); return Net(w, spec['G'], spec['T'], spec['motif'], spec['w'])
out = []
for lam in [Fr(x) for x in sys.argv[2].split(',')]:
    ref = {}
    for t, w in (('c', 'ABC'), ('h', 'AC')):
        net = build(w)
        for jr in range(3): ref[(t, jr)] = halves_vol(net, len(w), jr, 0, lam)
    rows = {}
    for hc in map(''.join, itertools.product('hc', repeat=4)):
        w = word_for(hc); net = build(w); n = len(w)
        for jr in range(3):
            lo, up = halves_vol(net, n, 3 * 2 + jr, 2, lam)
            rows[(hc, jr)] = (lo - ref[(hc[1], jr)][0], up - ref[(hc[2], jr)][1], lo + up)
    for jr in range(3):
        print(f'== s={s} lam={lam} {ROLE_OF[jr]}: pure halves c {ref[("c", jr)]}, h {ref[("h", jr)]}')
        for hc in sorted({h for h, _ in rows}):
            dl, du, V = rows[(hc, jr)]
            if dl or du: print(f'   window {hc}: dLo = {dl}, dUp = {du}, V = {V}')
        for name, idx in (('dLo', 0), ('dUp', 1), ('V', 2)):
            deps = [p for p in range(4) if any(rows[(h, jr)][idx] != rows[(h[:p] + ('c' if h[p] == 'h' else 'h') + h[p + 1:], jr)][idx] for h in {h for h, _ in rows})]
            print(f'   {name} depends on window letters {deps} (0 = layer k-1, 1 = t, 2 = t\', 3 = layer k+2)')
        g = {(h[1], h[2]): rows[(h, jr)][2] for h, _ in rows if _ == jr}
        print(f'   Swap: V(c|h) + V(h|c) - V(c|c) - V(h|h) = {g[("c","h")] + g[("h","c")] - g[("c","c")] - g[("h","h")]}', flush=True)
