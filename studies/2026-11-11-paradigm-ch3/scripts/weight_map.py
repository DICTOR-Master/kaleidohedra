"""Chapter 3 (The Permutohedron Paradigm): the bonds as spacing, exact. Body-centred cubic sites, kind A at 2Z^3 and kind B at
2Z^3 + (1,1,1), power distance |y - s|^2 - w_s, weight difference d = w_A - w_B. Claim: the A cell is the permutohedron of four values
placed symmetrically with gaps (g, m, g) (outer g, middle m), where d = (g - m)/(g + m); the B cell is the same with d -> -d (gaps
swapped in ratio). Checked: (1) the A cell's corners from its 14 planes equal the orders of (-q, -p, p, q), mapped by the isometry of
#105 Theorem 4, with g = q - p, m = 2p, (q - p)/(2p) = (1 + d)/(1 - d); symbolic in d on (-1, 1); (2) the special stops exactly."""
import itertools, sympy as sp
fails = []
def chk(ok, what): print(('PASS ' if ok else 'FAIL ') + what); (None if ok else fails.append(what))
d = sp.symbols('d', real=True)
# planes of the A cell at the origin: |y_i| <= 1 (A neighbours at 2e_i), |e.y| <= (3 + d)/2 for the 8 B neighbours e in {+-1}^3
def cell_corners(dv):
    planes = [(tuple(s * (1 if j == i else 0) for j in range(3)), 1) for i in range(3) for s in (1, -1)]
    planes += [(e, sp.Rational(3, 2) + dv / 2) for e in itertools.product((1, -1), repeat=3)]
    pts = set()
    for P3 in itertools.combinations(planes, 3):
        M = sp.Matrix([list(p[0]) for p in P3]); r = sp.Matrix([p[1] for p in P3])
        if M.det() == 0: continue
        y = M.LUsolve(r); y = tuple(sp.nsimplify(sp.simplify(v)) for v in y)
        if all(sp.simplify(sum(a * b for a, b in zip(n, y)) - c) <= 0 for n, c in planes): pts.add(y)
    return sorted(pts, key=str)
# the permutohedron of (-q,-p,p,q) in 3D by the isometry y -> (y1+y2-y3-y4, y1-y2+y3-y4, y1-y2-y3+y4)/2: signed orders of (p+q, q-p, 0)
def perm_corners(p, q):
    s = set()
    for perm in itertools.permutations((p + q, q - p, 0)):
        for sg in itertools.product((1, -1), repeat=3): s.add(tuple(sp.nsimplify(a * b) for a, b in zip(perm, sg)))
    return sorted(s, key=str)
tau = (1 + sp.sqrt(5)) / 2
for name, dv, xexp in [('Kelvin', 0, 1), ('DICTO 1:2', sp.Rational(-1, 3), sp.Rational(1, 2)), ('DICTO 2:1', sp.Rational(1, 3), 2),
                       ('golden bond', 1 / tau**3, tau), ('a generic stop', sp.Rational(2, 7), sp.Rational(9, 5))]:
    C = cell_corners(sp.nsimplify(dv))
    x = sp.simplify((1 + dv) / (1 - dv))
    # scale: the cell has squares at |y_i| = 1, so p + q = 1 and (q - p)/(2p) = x  ->  p = 1/(2(1 + x)), q = (1 + 2x)/(2(1 + x))
    p = 1 / (2 * (1 + x)); q = (1 + 2 * x) / (2 * (1 + x))
    T = perm_corners(sp.simplify(p), sp.simplify(q))
    same = len(C) == 24 and sorted(sp.simplify(sum(v)) for v in C) is not None and set(map(lambda v: tuple(sp.simplify(c) for c in v), C)) == set(map(lambda v: tuple(sp.simplify(c) for c in v), T))
    g, m = q - p, 2 * p
    chk(same and sp.simplify(x - xexp) == 0 and sp.simplify(dv - (g - m) / (g + m)) == 0,
        f'{name}: d = {sp.nsimplify(dv)}, cell = permutohedron with gap ratio outer:middle = {sp.simplify(x)}, d = (g - m)/(g + m)')
# symbolic: the map d <-> x is a bijection of (-1,1) onto (0, oo) with d -> -d  <->  x -> 1/x
x = (1 + d) / (1 - d)
chk(sp.simplify(x.subs(d, -d) * x) == 1, 'd -> -d sends the gap ratio x to 1/x: the two kinds of site swap their ratios')
chk(sp.simplify(sp.solve(sp.Eq(sp.Symbol('X'), x), d)[0] - (sp.Symbol('X') - 1) / (sp.Symbol('X') + 1)) == 0, 'inverse: d = (x - 1)/(x + 1) (as in #53, Corollary 1)')
chk(sp.simplify(1 / tau**3 - (tau - 1) / (tau + 1)) == 0, 'golden bond: d = (tau - 1)/(tau + 1) = 1/tau^3')
print('FINAL ok' if not fails else f'FINAL FAIL {fails}')
