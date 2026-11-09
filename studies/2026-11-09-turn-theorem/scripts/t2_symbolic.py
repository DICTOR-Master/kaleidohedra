# t2_symbolic.py -- symbolic parts of the turn theorem (study 2026-11-09-turn-theorem), sympy 1.14.
#  (1) the three identities the proof uses (same-hop AM-GM, the cross-hop bound, the sign of g - mu);
#  (2) the published closed forms recovered: C-O line (hopscotch-rows), D-I line (icosahedral-line, unit form), tetrahedron;
#  (3) the peak value R(S(sqrt c))^2/h^2 exactly for all 11 regular polytopes of dimensions 3 and 4;
#  (4) the fixed-point solid by brute force (sympy corners) for the five Platonic solids: every face at distance h, S^v = S/h^2,
#      t_min = R(S)^2/h^2 equal to the closed form;
#  (5) where the kinks of t_min sit (one turned pair) and when the min-of-three form is valid (sqrt c in the first or last hop).
import math, itertools, json
import numpy as np
import sympy as sp
from scipy.spatial import HalfspaceIntersection
from turnlib import *

ok = True
def check(label, cond):
    global ok
    ok = ok and bool(cond); print(('  ok   ' if cond else '  FAIL ') + label, flush=True)

r, A, s, k, mu, c = sp.symbols('r A s k mu c', positive=True)
F = lambda a, b: r + (a - r) * (b - r) / (A - r)          # E min of two laws on the same hop [r, A]
print('(1) identities')
check('same hop: F(s,s) - F(sk, s/k) = r (sqrt(sk) - sqrt(s/k))^2/(A - r)',
      sp.simplify(F(s, s) - F(s * k, s / k) - r * (sp.sqrt(s * k) - sp.sqrt(s / k)) ** 2 / (A - r)) == 0)
check('cross hop: r + (s - r)^2/(A - r) - s^2/A = r (A - s)^2/(A (A - r))',
      sp.simplify(r + (s - r) ** 2 / (A - r) - s ** 2 / A - r * (A - s) ** 2 / (A * (A - r))) == 0)
check('g(mu) - mu = (mu - r)(c/mu - A)/(A - r), g = F(mu, c/mu)',
      sp.simplify(F(mu, c / mu) - mu - (mu - r) * (c / mu - A) / (A - r)) == 0)

def tosp(x): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(5)

def closed_sym(nodes, h2, cc, m):
    """symbolic closed form on the piece containing the float value of m; returns expression in mu valid there"""
    def br(a, af):
        for rr, AA in zip(nodes, nodes[1:]):
            if float(rr) - 1e-12 <= af <= float(AA) + 1e-12:
                p = (a - rr) / (AA - rr); return [(rr, 1 - p), (AA, p)]
    a, b = mu, cc / mu
    af, bf = m, float(cc) / m
    terms = 0
    for u, p in br(a, af):
        for v, q in br(b, bf):
            terms += p * q * (u if float(u) <= float(v) else v)
    return sp.simplify(terms / h2)

print('(2) published closed forms')
# C-O line: nodes 1, 2, 3; c = 3; t_min = min(mu, 3/mu, 5 - mu - 3/mu)
nC = [sp.Integer(1), sp.Integer(2), sp.Integer(3)]
pub = {1.2: mu, 1.7: 5 - mu - 3 / mu, 2.5: 3 / mu}
check('C-O: closed form = min(mu, 3/mu, 5 - mu - 3/mu) on [1, 3/2], [3/2, 2], [2, 3]',
      all(sp.simplify(closed_sym(nC, 1, 3, m) - e) == 0 for m, e in pub.items()))
# D-I line (dodecahedron as P): nodes h^2 = 1 + 2sqrt5/5, phi^2, 3; c = h^2 * 3; unit mu_u = mu/sqrt(c)
S5 = sp.sqrt(5); ph = (1 + S5) / 2
h2D = 1 + 2 * S5 / 5; nD = [h2D, ph ** 2, sp.Integer(3)]; cD = 3 * h2D
mu_u = sp.symbols('mu_u', positive=True); k0 = (15 + 3 * S5) / 2; cpr = 1 / sp.sqrt(15 - 6 * S5)
pubD = {0.9: mu_u / cpr, 1.0: 10 - S5 - sp.sqrt(k0) * (mu_u + 1 / mu_u), 1.1: 1 / (cpr * mu_u)}
goodD = True
for mu0, e in pubD.items():
    m = float(sp.sqrt(cD)) * mu0
    ex = closed_sym(nD, h2D, cD, m).subs(mu, sp.sqrt(cD) * mu_u)
    diff = sp.simplify(sp.expand(ex - e))
    vals = [abs(float(diff.subs(mu_u, t))) for t in (mu0 - 0.01, mu0, mu0 + 0.01)]
    goodD = goodD and (diff == 0 or max(vals) < 1e-12)
    print(f'     piece at mu_u = {mu0}: closed form - published = {diff}  (|.| at 3 points {max(vals):.1e})')
check('D-I: closed form = min(mu/c, 1/(c mu), 10 - sqrt5 - sqrt(k0)(mu + 1/mu)) in unit form (bird 3 Theorem 3)', goodD)
# tetrahedron: nodes 1/3, 1, 3; c = 1; h^2 = 1/3: t_min = 3 min(mu, 1/mu)
nT = [sp.Rational(1, 3), sp.Integer(1), sp.Integer(3)]
check('T: closed form = 3 min(mu, 1/mu) (the fixed point mu = 1 is the edge wall: the octahedron)',
      sp.simplify(closed_sym(nT, sp.Rational(1, 3), 1, 0.6) - 3 * mu) == 0 and sp.simplify(closed_sym(nT, sp.Rational(1, 3), 1, 2.0) - 3 / mu) == 0)

print('(3) peak values R(S(sqrt c))^2/h^2, exact')
NAMES = [('D', dodecahedron), ('I', icosahedron), ('C', cube), ('T', tetrahedron), ('O', octahedron),
         ('5-cell', simplex4), ('tesseract', tesseract), ('16-cell', cross16), ('24-cell', cell24),
         ('600-cell', cell600), ('120-cell', cell120)]
EXPECT = {'D': 10 - S5 - sp.sqrt(30 + 6 * S5), 'I': 10 - S5 - sp.sqrt(30 + 6 * S5), 'C': 5 - 2 * sp.sqrt(3),
          'O': 5 - 2 * sp.sqrt(3), 'T': sp.Integer(3), '5-cell': sp.Rational(16, 5), 'tesseract': sp.Integer(2),
          '16-cell': sp.Integer(2), '24-cell': 24 - 16 * sp.sqrt(2)}
table = {}
for name, fn in NAMES:
    st = setup(fn())
    nodes = [tosp(x) for x in st['nodes']]; h2 = tosp(st['h2']); cc = tosp(st['c']); sc = sp.sqrt(cc)
    scf = float(sc)
    hop = [(a, b) for a, b in zip(nodes, nodes[1:]) if float(a) <= scf <= float(b)][0]
    rr, AA = hop
    peak = sp.nsimplify(sp.radsimp((rr + (sc - rr) ** 2 / (AA - rr)) / h2))
    peak = sp.simplify(peak)
    pos = 'node' if any(abs(float(x) - scf) < 1e-12 for x in nodes) else \
          ('first hop' if hop[0] == nodes[0] else ('last hop' if hop[1] == nodes[-1] else 'middle hop'))
    lo = max(float(rr), float(cc) / float(AA)); hi = min(float(AA), float(cc) / float(rr))
    table[name] = dict(nodes=[str(x) for x in nodes], h2=str(h2), c=str(sp.nsimplify(cc)), sqrt_c=scf, position=pos,
                       peak=str(peak), peak_f=float(peak), kinks=[lo, hi], R_over_r_sq=float(peak))
    line = f'     {name:10s} nodes {[round(float(x), 6) for x in nodes]}, sqrt c = {scf:.6f} ({pos}), peak = {peak} = {float(peak):.10f}, kinks of t_min at {lo:.6f}, {hi:.6f} (product {lo * hi:.6f} = c {float(cc):.6f})'
    print(line)
    if name in EXPECT:
        check(f'{name}: peak = {EXPECT[name]}', abs(float(peak - EXPECT[name])) < 1e-13 and sp.simplify(sp.radsimp(peak - EXPECT[name])) == 0)
    # (5) kinks of the float closed form = {lo, hi} (or only sqrt c when it is a node); min-of-three validity
    nf = [float(x) for x in nodes]; h2f = float(h2); cf = float(cc)
    grid = np.exp(np.linspace(math.log(nf[0]), math.log(nf[-1]), 20001))
    v = np.array([tmin_closed_f(m, nf, h2f, cf) for m in grid])
    lg = np.log(grid); dv = np.diff(v) / np.diff(lg); jump = np.abs(np.diff(dv))
    kinks = sorted({round(float(grid[i + 1]), 3) for i in np.where(jump > 1e-2)[0]})
    symhop = pos != 'node' and sp.simplify(rr * AA - cc) == 0     # the hop of sqrt c is turned onto itself (r A = c)
    if pos == 'node': expect = [round(scf, 3)]
    elif symhop: expect = []      # slopes agree at r and A: t_min is C^1 there, only the curvature jumps
    else: expect = sorted({round(lo, 3), round(hi, 3)})
    table[name]['hop_turned_onto_itself'] = bool(symhop)
    # merge neighbours (a kink between grid points can show in two adjacent second differences)
    merged = []
    for x in kinks:
        if not merged or x - merged[-1] > 2e-3: merged.append(x)
    check(f'{name}: corners (slope jumps) of t_min on the open line = {merged}, predicted {expect} ({"sqrt c is a node" if pos == "node" else ("hop of sqrt c turned onto itself: C^1, curvature jumps at r, A" if symhop else "a wall of S and its turn, product c")})',
          len(merged) == len(expect) and all(abs(a - b) <= 2e-3 for a, b in zip(merged, expect)))
    if pos == 'node':   # sqrt c is a node: t_min = min(mu, c/mu)/h^2, the middle piece is empty
        g3 = np.array([min(m, cf / m) / h2f for m in grid])
    else:
        g3 = np.array([min(m, cf / m, float(rr) + (m - float(rr)) * (cf / m - float(rr)) / (float(AA) - float(rr))) / h2f
                       for m in grid])
    valid3 = bool(np.max(np.abs(g3 - v)) < 1e-12)
    table[name]['min_of_three_valid'] = valid3
    check(f'{name}: min(mu, c/mu, g(mu))/h^2 (g absent when sqrt c is a node) valid on the whole line = {valid3}, predicted {pos != "middle hop"}', valid3 == (pos != 'middle hop'))

print('(4) fixed-point solid by brute force, five Platonic solids (sympy corners)')
def sp_corners(Ns, bs):
    d = 3
    A = np.array([[float(x) for x in N] + [-float(b)] for N, b in zip(Ns, bs)])
    hs = HalfspaceIntersection(A, np.zeros(d)); pts = []
    for p in hs.intersections:
        if not any(np.abs(p - q).max() < 1e-7 for q in pts): pts.append(p)
    out = []
    for p in pts:
        act = [i for i in range(len(Ns)) if abs(A[i, :3] @ p + A[i, 3]) < 1e-7]
        for tri in itertools.combinations(act, 3):
            M = sp.Matrix([list(Ns[i]) for i in tri])
            if abs(float(M.det())) > 1e-9:
                x = M.LUsolve(sp.Matrix([bs[i] for i in tri])); out.append([sp.radsimp(t) for t in x]); break
    return out
for name, fn in NAMES[:5]:
    st = setup(fn()); Ns = [[tosp(t) for t in N] for N in st['N']]; Vs = [[tosp(t) for t in v] for v in st['V']]
    h2 = tosp(st['h2']); cc = tosp(st['c']); sc = sp.sqrt(cc)
    planes = [(N, sp.Integer(1)) for N in Ns] + [(v, sc) for v in Vs]
    tang = all(sp.simplify(b ** 2 / sum(t * t for t in N) - h2) == 0 for N, b in planes)
    X = sp_corners([p[0] for p in planes], [p[1] for p in planes])
    R2s = [sp.radsimp(sum(t * t for t in x)) for x in X]
    fl = [float(t) for t in R2s]; Rmax = R2s[int(np.argmax(fl))]
    # t_min = max x.y over S x S^v with S^v = S/h^2; Cauchy-Schwarz: = R^2/h^2, float check over all pairs
    Xf = np.array([[float(t) for t in x] for x in X]); tm_f = float((Xf @ Xf.T).max()) / float(h2)
    peak = sp.simplify(sp.radsimp(Rmax / h2))
    eq = sp.simplify(sp.radsimp(peak - sp.sympify(table[name]['peak']))) == 0 or abs(float(peak) - table[name]['peak_f']) < 1e-13
    check(f'{name}: S(sqrt c) has {len(X)} corners, every face tangent to the sphere of radius h: {tang}; t_min = {peak} (pairs, float {tm_f:.12f}) = closed-form peak',
          tang and eq and abs(tm_f - float(peak)) < 1e-12)

with open('../data/t2_table.json', 'w') as f: json.dump(table, f, indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: see FAIL lines')
