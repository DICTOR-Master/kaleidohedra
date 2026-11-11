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
steps = [sp.Matrix(v) for v in [(1,-1,0),(1,0,-1),(0,1,-1),(-1,1,0),(-1,0,1),(0,-1,1)]]   # step directions from (a,b,c), values factored out
turn60 = all((steps[k].T * steps[(k + 1) % 6])[0] == 1 for k in range(6))   # unit-free: dot 1, norms sqrt2 -> 60 degree turns
real = all(sp.simplify((H[(k + 1) % 6] - H[k]) - steps[k] * ((b - a) if k % 2 == 0 else (c - b))) == sp.zeros(3, 1) for k in range(6))
chk(turn60 and real, 'the six steps are (b-a) and (c-b) times six root directions, each turned 60 degrees from the last: every angle 120 degrees, symbolically')
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
import numpy as np
from scipy.spatial import ConvexHull
def hull_faces(vals):
    tv = [float(v) for v in vals]; m = sum(tv) / 4
    Hm = np.array([[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]) / 2.0
    X = np.array([[v - m for v in p] for p in itertools.permutations(tv)]) @ Hm.T
    h = ConvexHull(X); G = {}
    for simp, eq in zip(h.simplices, h.equations): G.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    out = []
    for idx in G.values():
        idx = list(idx); c = X[idx].mean(0); n = np.cross(X[idx[1]] - X[idx[0]], X[idx[2]] - X[idx[0]]); u = X[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((X[i] - c) @ w, (X[i] - c) @ u))
        out.append(sorted(round(float(np.linalg.norm(X[idx[k]] - X[idx[(k + 1) % len(idx)]])), 6) for k in range(len(idx))))
    return out
tau = (1 + sp.sqrt(5)) / 2
for name, vals, hexs, quads in [('Kelvin', (1, 2, 3, 4), (1, 1), (1, 1)), ('DICTO 1:2', (1, 2, 4, 5), (1, 2), (1, 1)), ('DICTO 2:1', (-5, -1, 1, 5), (2, 4), (4, 4)),
                                ('golden bond', (-tau**3, -1, 1, tau**3), (2, 2 * tau), (2 * tau, 2 * tau))]:
    F = hull_faces(vals); hx = [f for f in F if len(f) == 6]; qd = [f for f in F if len(f) == 4]
    eh = sorted([round(float(sp.sqrt(2) * hexs[0]), 6)] * 3 + [round(float(sp.sqrt(2) * hexs[1]), 6)] * 3)
    eq_ = sorted([round(float(sp.sqrt(2) * quads[0]), 6)] * 2 + [round(float(sp.sqrt(2) * quads[1]), 6)] * 2)
    chk(len(hx) == 8 and len(qd) == 6 and all(f == eh for f in hx) and all(f == eq_ for f in qd), f'{name}: hull faces computed: 8 hexagons sides sqrt2*{hexs}, 6 four-gons sides sqrt2*{quads}')
for name, vals in [('DICTO 1:2', (1, 2, 4, 5)), ('golden bond T(tau)', (-tau**3, -1, 1, tau**3)), ('Kelvin', (1, 2, 3, 4))]:
    g, r, rect = faces4(vals)
    g = [sp.simplify(x) for x in g]; r = [sp.simplify(x) for x in r]
    print(f'   {name}: gaps {g}, hexagon gap ratios {r}, four-gons {[(sp.simplify(x), sp.simplify(y)) for x, y in rect]}')
    if name == 'DICTO 1:2': chk(r == [2, sp.Rational(1, 2)] and sp.simplify(rect[0][0] - rect[0][1]) == 0, 'DICTO 1:2: hexagons ratio 2 (1:2), four-gons squares')
    if name == 'golden bond T(tau)': chk(sp.simplify(r[0] - 1 / tau) == 0 and sp.simplify(r[1] - tau) == 0 and sp.simplify(g[0] - 2 * tau) == 0, 'golden bond: gaps 2tau, 2, 2tau (tau^3 - 1 = 2tau), hexagons golden (ratio tau)')
    if name == 'Kelvin': chk(r == [1, 1], 'Kelvin: equal gaps, regular hexagons and squares')
print('FINAL ok' if not fails else f'FINAL FAIL {fails}')
