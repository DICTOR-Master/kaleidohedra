"""Aim 1, step 5b (DICTO 10 Nov 2026; checks 16 Nov 2026): what is extremal at the icosahedral point of the line?
Scheme at x as in ico_tiles.py: physical star P(x), internal map Q_x = P(-1/x), lattice Z^6.
Claims:
 (1) symmetry: the signed permutations of the six edge directions preserving the Gram matrix of P(x) (= the point symmetries of the
     whole scheme: star, window, lattice) form a group of order 24 for every x > 0 except x = 1 (order 48, cubic: the 1/1 crystal,
     fixed point of the turn x -> 1/x) and x = phi, 1/phi (order 120, icosahedral: the quasicrystal). Largest exactly at phi, 1/phi.
     The six edge directions are equiangular exactly at x = phi, 1/phi.
 (2) tiles: the 20 rhombohedra fall into four volume classes 2x^2 (6), 1+x^3 (4), 2x (6), |x^3-1| (4); every tile occurs with frequency
     proportional to its volume (Pluecker duality |det P_I| = x^3 |det Q_(I^c)|); the classes merge into two shapes (the prolate and
     oblate golden rhombohedra, ten types each, frequency ratio phi) exactly at x = phi and 1/phi; at x = 1 the volumes are 2, 2, 2
     and 0 (one class flat, absent); everywhere else at least three distinct volumes.
 (3) Diophantine (the 3D analogue of Hurwitz): at x = phi every nonzero n in Z^6 has |pi(n)| |pi_perp(n)| >= 1/2 (orthogonal
     projections onto physical and internal space), equality for the unit vectors and their images under every power of A
     (infinitely many); at every crystal (rational x) the periods give 0. Proof: |P n|^2 |Q n|^2 = N(alpha) for alpha = |P(phi) n|^2 in
     Z[phi] (Galois conjugate = |Q n|^2), a positive integer; A multiplies alpha by phi^6 (a unit), so N is A-invariant; balancing by
     powers of A bounds |n|^2 <= phi^3 sqrt(N) / 2, so N <= 4 would need |n|^2 <= 4: exhaust them.
usage: python3 ico_extremal.py"""
import itertools, time
import sympy as sp
T0 = time.time()
def prog(m): print(f'PROGRESS [{time.time()-T0:6.1f}s] {m}', flush=True)
x = sp.symbols('x', positive=True); phi = (1 + sp.sqrt(5)) / 2
def P(t): return sp.Matrix([[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]])
def Q(t): return P(-1 / t)
A = sp.Matrix([[2, 1, 1, -1, 1, -1], [1, 2, 1, -1, -1, 1], [1, 1, 2, 1, 1, 1], [-1, -1, 1, 2, 1, 1], [1, -1, 1, 1, 2, -1], [-1, 1, 1, 1, -1, 2]])
OK = {}
# (1) symmetry group order
Gs = sp.expand(P(x).T * P(x))
vals = sorted(set(sp.expand(Gs[i, j]) for i in range(6) for j in range(6)), key=str)
prog(f'(1) Gram entries of P(x): {vals}')
special = set()
for a_, b_ in itertools.combinations(vals, 2):
    for sgn in (1, -1):
        for r in sp.solve(sp.Eq(a_, sgn * b_), x): special.add(sp.nsimplify(r))
special = sorted([r for r in special if r.is_positive], key=lambda r: sp.N(r))
prog(f'    x > 0 where two Gram entries coincide up to sign (only places the symmetry can change): {special}')
def order_at(val):
    G = (Gs.subs(x, val)).applyfunc(sp.nsimplify)
    lab = {}
    def L(v):
        v = sp.simplify(v)
        for key, idx in lab.items():
            if sp.simplify(key - v) == 0: return idx
        lab[v] = len(lab); return lab[v]
    Gl = [[L(G[i, j]) for j in range(6)] for i in range(6)]; Gn = [[L(-G[i, j]) for j in range(6)] for i in range(6)]
    cnt = 0
    for perm in itertools.permutations(range(6)):
        for sg in itertools.product((1, -1), repeat=6):
            if all((Gl if sg[i] * sg[j] == 1 else Gn)[perm[i]][perm[j]] == Gl[i][j] for i in range(6) for j in range(i, 6)): cnt += 1
    return cnt
orders = {}
for val in [sp.Rational(1, 3), sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2), sp.Rational(7, 3), phi, 1 / phi]:
    orders[val] = order_at(val); prog(f'    x = {val}: symmetry group order {orders[val]}')
OK['special points are exactly 1, 1/phi, phi'] = [sp.simplify(r) for r in special] == [sp.simplify(1 / phi), 1, sp.simplify(phi)] or \
    set(sp.N(r, 20) for r in special) == {sp.N(1 / phi, 20), sp.N(1, 20), sp.N(phi, 20)}
OK['orders: 24 generic, 48 at 1, 120 at phi and 1/phi'] = all(o == 24 for v, o in orders.items() if v not in (1, phi, 1 / phi)) and orders[1] == 48 and orders[phi] == 120 and orders[1 / phi] == 120
eq = [r for r in sp.solve(sp.Eq((x ** 2 - 1) ** 2, x ** 2), x) if r.is_positive]
OK['equiangular exactly at phi, 1/phi'] = sorted(sp.N(r, 20) for r in eq) == sorted([sp.N(1 / phi, 20), sp.N(phi, 20)])
prog(f'    equiangular six directions (|cos| = |x^2-1|/(1+x^2) = x/(1+x^2)) at x = {eq}')
# (2) tiles
TR = list(itertools.combinations(range(6), 3))
vol = {I: sp.factor(P(x)[:, list(I)].det()) for I in TR}
wvol = {I: sp.factor(Q(x)[:, [l for l in range(6) if l not in I]].det()) for I in TR}
OK['Pluecker: det P_I = +- x^3 det Q_(I^c), all 20'] = all(sp.simplify(vol[I] ** 2 - x ** 6 * wvol[I] ** 2) == 0 for I in TR)
classes = {}
for I in TR:
    classes.setdefault(sp.factor(vol[I] ** 2), []).append(I)
prog('(2) tile volume classes (volume^2: count): ' + ', '.join(f'{k}: {len(v)}' for k, v in classes.items()))
want = {sp.factor((2 * x ** 2) ** 2): 6, sp.factor((2 * x) ** 2): 6, sp.factor((1 + x ** 3) ** 2): 4, sp.factor((x ** 3 - 1) ** 2): 4}
OK['four classes 2x^2 (6), 2x (6), 1+x^3 (4), |x^3-1| (4)'] = {k: len(v) for k, v in classes.items()} == want
# which x > 0 have at most two distinct tile volumes with no flat tile? all set partitions of the four classes into <= 2 blocks
V = [2 * x ** 2, 2 * x, 1 + x ** 3, x ** 3 - 1]
def partitions2(items):
    for mask in range(2 ** (len(items) - 1)):
        b1 = [items[0]] + [items[i] for i in range(1, len(items)) if not mask >> (i - 1) & 1]
        b2 = [items[i] for i in range(1, len(items)) if mask >> (i - 1) & 1]
        yield [blk for blk in (b1, b2) if blk]
two_vol = set(); flat_two = set()
for part in partitions2([0, 1, 2, 3]):
    eqs = [sp.expand(V[blk[0]] ** 2 - V[j] ** 2) for blk in part for j in blk[1:]]
    if not eqs: continue
    G = sp.groebner(eqs, x)
    for r in sp.Poly(G.exprs[-1], x).real_roots() if G.exprs != [1] else []:
        if r > 0 and all(sp.simplify(e.subs(x, r)) == 0 for e in eqs):
            (flat_two if any(sp.simplify(v.subs(x, r)) == 0 for v in V) else two_vol).add(sp.nsimplify(sp.simplify(r)))
prog(f'    at most two tile volumes, none flat, exactly at x = {sorted(two_vol, key=sp.N)}; with a flat class at x = {sorted(flat_two, key=sp.N)}')
OK['two volumes and no flat tile exactly at phi, 1/phi'] = {sp.N(r, 20) for r in two_vol} == {sp.N(phi, 20), sp.N(1 / phi, 20)} and {sp.N(r, 20) for r in flat_two} == {sp.N(1, 20)}
OK['golden ratio of the two shapes at phi'] = sp.simplify((2 * x ** 2 / (2 * x)).subs(x, phi) - phi) == 0
# (3) Diophantine constant at phi
ph2 = sp.simplify(phi ** 2); Pp, Qp = P(phi), P(-1 / phi)
OK['normalisation P^T P/(2 sqrt5 phi) + Q^T Q phi/(2 sqrt5) = I'] = sp.simplify(Pp.T * Pp / (2 * sp.sqrt(5) * phi) + Qp.T * Qp * phi / (2 * sp.sqrt(5)) - sp.eye(6)) == sp.zeros(6, 6)
OK['P(phi) A = phi^3 P(phi), Q A = -phi^-3 Q'] = sp.simplify(Pp * A - phi ** 3 * Pp) == sp.zeros(3, 6) and sp.simplify(Qp * A + phi ** -3 * Qp) == sp.zeros(3, 6)
def alpha(n):   # |P(phi) n|^2 = a + b phi exactly: coordinates A_i + phi B_i
    AB = [(n[0] - n[1], n[4] - n[5]), (n[2] - n[3], n[0] + n[1]), (n[4] + n[5], n[2] + n[3])]
    return sum(a * a + b * b for a, b in AB), sum(2 * a * b + b * b for a, b in AB)
OK['alpha formula matches P(phi)'] = all(sp.simplify((Pp * sp.Matrix(n)).dot(Pp * sp.Matrix(n)) - (alpha(n)[0] + alpha(n)[1] * phi)) == 0 and
    sp.simplify((Qp * sp.Matrix(n)).dot(Qp * sp.Matrix(n)) - (alpha(n)[0] + alpha(n)[1] * (1 - phi))) == 0
    for n in [(1, 0, 0, 0, 0, 0), (1, 2, -1, 0, 3, 1), (0, 1, 1, -2, 0, 5)])
Nm = lambda n: (lambda a, b: a * a + a * b - b * b)(*alpha(n))
best = None; cnt = 0
for n in itertools.product(range(-2, 3), repeat=6):
    if 0 < sum(c * c for c in n) <= 4:
        cnt += 1; v = Nm(n)
        if best is None or v < best: best = v
prog(f'(3) {cnt} nonzero n with |n|^2 <= 4: least N(|P n|^2) = {best}')
OK['least norm over |n|^2 <= 4 is 5'] = best == 5
# completeness of the search: balanced n has |n|^2 <= phi^3 sqrt(N) / 2; for N <= 4 that is <= phi^3 < 5
OK['bound phi^3 sqrt(4)/2 < 5'] = sp.N(phi ** 3 * 2 / 2) < 5
orb = [sp.Matrix([1, 0, 0, 0, 0, 0])]
for _ in range(5): orb.append(A * orb[-1])
for _ in range(3): orb.insert(0, A.inv() * orb[0])
prods = [sp.simplify(sp.sqrt(Nm(list(v))) / (2 * sp.sqrt(5))) for v in orb]
OK['product 1/2 along the A-orbit of e1 (9 vectors, growing)'] = all(p == sp.Rational(1, 2) for p in prods) and len(set(tuple(v) for v in orb)) == 9
prog(f'    |pi n||pi_perp n| along A^j e1, j = -3..5: {prods}; |n|^2: {[int(v.dot(v)) for v in orb]}')
# NEG: a crystal has periods: product 0
for xv in (sp.Rational(3, 2), sp.Rational(8, 5)):
    ker = Q(xv).nullspace()[0]; ker = ker * sp.lcm([sp.fraction(c)[1] for c in ker])
    OK[f'NEG crystal {xv}: a period has product 0'] = Q(xv) * ker == sp.zeros(3, 1) and P(xv) * ker != sp.zeros(3, 1)
    prog(f'    crystal x = {xv}: period {list(ker)} has internal part 0 (product 0)')
for k_, v in OK.items(): print(f'CHECK {k_}: {v}')
print('FINAL ok' if all(OK.values()) else 'FINAL FAIL')
