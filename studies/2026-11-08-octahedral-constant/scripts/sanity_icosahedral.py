# sanity_icosahedral.py -- known case: the vertex-lemma machinery of proof_check.py, run on the icosahedral group,
# must give #43 Theorem 2's constant c^2 = (5 + 2 sqrt5)/15, i.e. 1/c^2 = 15 - 6 sqrt5. Exact in Q(sqrt5) (sympy).
# Case A: the chamber's own vertex pairs; case B: for each of the three mirrors s in the sides of the Moebius triangle T,
# the single bound (identity on T x sT) -- the kite of #43 -- and the average of the three, all on the 9 vertex pairs.
import itertools
import sympy as sp

s5 = sp.sqrt(5); phi = (1 + s5) / 2
def red(M): return M.applyfunc(lambda x: sp.nsimplify(sp.radsimp(sp.expand(x))))
A = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])                       # 3-fold, cyclic
B = sp.diag(1, -1, -1)                                                 # 2-fold
C = red(sp.Rational(1, 2) * sp.Matrix([[1, -phi, 1 / phi], [phi, 1 / phi, -1], [1 / phi, 1, phi]]))   # 5-fold
assert red(C.T * C) == sp.eye(3) and sp.simplify(C.det() - 1) == 0
G = {tuple(sp.eye(3))}; frontier = [sp.eye(3)]; mats = [sp.eye(3)]
while frontier:
    nxt = []
    for M in frontier:
        for g in (A, B, C):
            P = red(g * M)
            if tuple(P) not in G:
                G.add(tuple(P)); mats.append(P); nxt.append(P)
    frontier = nxt
checks = {'|I| = 60': len(mats) == 60}

# Moebius triangle: 5-fold axis, adjacent 3-fold axis, 2-fold axis between them (exact, from the standard frame)
a5 = sp.Matrix([0, 1, phi])                    # icosahedron corner
a3 = sp.Matrix([1 / phi, 0, phi])              # centre of the face (0,1,phi),(0,-1,phi),(phi,0,1)
a2 = sp.Matrix([0, 0, 1])                      # midpoint of that face's edge (0,1,phi)-(0,-1,phi)
V = [red(a5), red(a3), red(a2)]
def c2(v, w): return sp.nsimplify(sp.radsimp(v.dot(w)**2 / (v.dot(v) * w.dot(w))))
sides = {('5', '3'): c2(V[0], V[1]), ('3', '2'): c2(V[1], V[2]), ('5', '2'): c2(V[0], V[2])}
print('cos^2 of the sides:', sides)
cstar2 = sp.nsimplify((5 + 2 * s5) / 15)
deg = lambda q: float(sp.acos(sp.sqrt(q)) * 180 / sp.pi)
print('angles (deg):', {k: round(deg(v), 4) for k, v in sides.items()})
# the triangle is a Moebius (2,3,5) triangle iff its angles are 90, 60, 36: check the three axes are adjacent axes
checks['sides 31.717, 20.905, 37.377 deg'] = [round(deg(v), 3) for v in sides.values()] == [20.905, 31.717, 37.377] or \
    sorted(round(deg(v), 3) for v in sides.values()) == [20.905, 31.717, 37.377]
checks['longest side has cos^2 = (5+2sqrt5)/15'] = min(sides.values(), key=lambda q: float(q)) == cstar2 or \
    sp.simplify(min(sides.values(), key=lambda q: float(q)) - cstar2) == 0

def plane_mirror(p, q):
    n = p.cross(q); return red(sp.eye(3) - 2 * n * n.T / n.dot(n))
def passes(Lfun, W):
    out = True; eq = 0
    for v in V:
        for w in W:
            L = sp.nsimplify(sp.radsimp(Lfun(v, w))); n2 = sp.radsimp(v.dot(v) * w.dot(w))
            d = sp.nsimplify(sp.radsimp(L**2 - cstar2 * n2))
            good = (L == 0 or bool(L > 0)) and (d == 0 or bool(d > 0))
            out &= good; eq += (d == 0)
    return out, eq

# case A
okA, eqA = passes(lambda v, w: v.dot(w), V)
print('case A (T x T, identity): passes', okA, '| equality pairs', eqA)
checks['case A'] = okA
# case B: mirrors in the three sides; the kite = T u sT for the mirror s in the longest side
mir = {'side 5-3': plane_mirror(V[0], V[1]), 'side 3-2': plane_mirror(V[1], V[2]), 'side 5-2': plane_mirror(V[0], V[2])}
res = {}
for name, s in mir.items():
    ok, eq = passes(lambda v, w, s=s: v.dot(s * w), V)
    res[name] = ok
    print(f'case B single mirror in {name}: passes {ok} (equality pairs {eq})')
ok3, eq3 = passes(lambda v, w: sum(v.dot(s * w) for s in mir.values()) / 3, V)
print('case B average of the three mirrors: passes', ok3)
checks['case B: the kite (mirror in the longest side 5-3) passes, as in #43'] = res['side 5-3']
print('so every icosahedral orbit hull has inradius >= c, c^2 = (5+2sqrt5)/15, 1/c^2 =', sp.nsimplify(sp.radsimp(1 / cstar2)))
checks['1/c^2 = 15 - 6 sqrt5'] = sp.simplify(1 / cstar2 - (15 - 6 * s5)) == 0
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
