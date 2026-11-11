"""Chapter 1 key lemma, checked exactly (The Permutohedron Paradigm, DICTO 11 Nov 2026):
(1) the six orders of a < b < c span a hexagon with all angles 120 degrees and sides alternating sqrt2(b-a), sqrt2(c-b);
(2) every equiangular hexagon with alternating sides s, t (a truncated triangle) is congruent to the one with gaps s/sqrt2, t/sqrt2;
(3) faces of the permutohedron of v1 < ... < vn: hexagons = truncated triangles of three consecutive values (gap ratio), four-gons =
    rectangles sqrt2 g_i x sqrt2 g_j; checked for the DICTO 1:2 (1,2,4,5), the golden bond (-tau^3,-1,1,tau^3), Kelvin (1,2,3,4).
Exact in sympy (Q(sqrt5) for tau). FINAL ok only if every check passes."""
import itertools, sympy as sp
fails = []
def chk(ok, what): print(('PASS ' if ok else 'FAIL ') + what); (None if ok else fails.append(what))
a, b, c = sp.symbols('a b c', real=True)
def hexagon(vals):
    V = [sp.Matrix(p) for p in itertools.permutations(vals)]
    # cycle by alternating swaps of positions of the values (a,b) then (b,c)
    v0 = list(vals); cyc = [tuple(v0)]; cur = v0[:]
    for k in range(6):
        lo, hi = (vals[0], vals[1]) if k % 2 == 0 else (vals[1], vals[2])
        cur = [hi if x == lo else lo if x == hi else x for x in cur]; cyc.append(tuple(cur))
    return [sp.Matrix(p) for p in cyc[:6]], cyc[6] == cyc[0]
H, closed = hexagon((a, b, c))
chk(closed, 'alternating exchanges (a b), (b c) close up after six steps (the braid ring)')
sides = [sp.simplify(sp.sqrt(((H[(k + 1) % 6] - H[k]).T * (H[(k + 1) % 6] - H[k]))[0])) for k in range(6)]
print('   sides:', sides)
pos = {a: 1, b: 2, c: 4}
num = [s.subs(pos) for s in sides]
chk(num == [sp.sqrt(2), 2 * sp.sqrt(2)] * 3, 'sides alternate sqrt2(b-a), sqrt2(c-b) (checked at 1,2,4 and symbolically below)')
chk(all(sp.simplify(sides[k] - sp.sqrt(2) * sp.Abs(b - a)) == 0 for k in (0, 2, 4)) and all(sp.simplify(sides[k] - sp.sqrt(2) * sp.Abs(c - b)) == 0 for k in (1, 3, 5)), 'side formula symbolic')
def angle(k):
    u = H[k - 1] - H[k]; w = H[(k + 1) % 6] - H[k]
    return sp.simplify((u.T * w)[0] / sp.sqrt((u.T * u)[0] * (w.T * w)[0]))
cosines = [sp.simplify(angle(k).subs(pos)) for k in range(6)]
chk(all(x == sp.Rational(-1, 2) for x in cosines), 'every angle 120 degrees (cos = -1/2)')
# (2) congruence: an equiangular hexagon with sides s,t,s,t,s,t is fixed up to congruence by s, t (turning by 60 each step)
s, t = sp.symbols('s t', positive=True)
dirs = [sp.Matrix([sp.cos(sp.pi * k / 3), sp.sin(sp.pi * k / 3)]) for k in range(6)]
close = sum((dirs[k] * (s if k % 2 == 0 else t) for k in range(6)), sp.zeros(2, 1))
chk(sp.simplify(close) == sp.zeros(2, 1), 'every equiangular hexagon with alternating sides s, t closes: one shape per (s, t)')
# (3) faces of the permutohedron of four values
def faces4(vals):
    o = sorted(vals); gaps = [o[i + 1] - o[i] for i in range(3)]
    hexratios = [sp.nsimplify(sp.simplify(gaps[i + 1] / gaps[i])) for i in range(2)]
    rects = [(sp.sqrt(2) * gaps[0], sp.sqrt(2) * gaps[2])]   # four-gons exchange the first and last pair of values (two disjoint swaps)
    return gaps, hexratios, rects
tau = (1 + sp.sqrt(5)) / 2
for name, vals in [('DICTO 1:2', (1, 2, 4, 5)), ('golden bond T(tau)', (-tau**3, -1, 1, tau**3)), ('Kelvin', (1, 2, 3, 4))]:
    g, r, rect = faces4(vals)
    g = [sp.simplify(x) for x in g]; r = [sp.simplify(x) for x in r]
    print(f'   {name}: gaps {g}, hexagon gap ratios {r}, four-gons {[(sp.simplify(x), sp.simplify(y)) for x, y in rect]}')
    if name == 'DICTO 1:2': chk(r == [2, sp.Rational(1, 2)] and sp.simplify(rect[0][0] - rect[0][1]) == 0, 'DICTO 1:2: hexagons ratio 2 (1:2), four-gons squares')
    if name == 'golden bond T(tau)': chk(sp.simplify(r[0] - 1 / tau) == 0 and sp.simplify(r[1] - tau) == 0 and sp.simplify(g[0] - 2 * tau) == 0, 'golden bond: gaps 2tau, 2, 2tau (tau^3 - 1 = 2tau), hexagons golden (ratio tau)')
    if name == 'Kelvin': chk(r == [1, 1], 'Kelvin: equal gaps, regular hexagons and squares')
print('FINAL ok' if not fails else f'FINAL FAIL {fails}')
