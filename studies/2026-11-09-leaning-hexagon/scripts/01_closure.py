"""01: what leaning sides can do in ONE layer (exact).

(a) Three tilted plates round a corner meet in one line  <=>  their tilts sum to zero (sympy, general tilts).
(b) Potential: the tilts of a whole layer are differences psi(Y) - psi(X) of a function on the cells; the corner lines
    lean along the gradient of psi; every horizontal cross-section is the power (Laguerre) diagram of the seats with
    weights -2 z psi.  Checked exactly on a random 6x6 torus; the solution space of the closure equations has
    dimension (#cells - 1) + 2 (potential + two global shears).
(c) Classification of every leaning hexagon with planar sides in the box w0 in {-1,0,1}^2, lam in {-1,0,1}^6
    (corner leans w_{s+1} = w_s + lam_s D_{s+2}), up to the 24 motions: which ones can fill a layer, on every torus of
    index <= 12 and on an open patch of radius 4; predictions of the rigidity theorem:
      P1 lam = 0 (pure shear): layers exist; every layer is ONE shear (all cells the same corner lines);
      P2 lam != 0, first-order area change a1 = 0: no layer (discrete Liouville);
      P3 second-order area change a2 != 0: no layer (area of a torus layer is constant in z);
      P4 the rest (a1 != 0, a2 = 0): layers need upright and turned-over copies, exactly half each on every torus.
"""
import sys, time, json, itertools, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import sympy as sp
from leanplates import *

t0 = time.time()
ok = True

# ---------------------------------------------------------------- (a) corner closure
t1, t2, t3, z = sp.symbols('t1 t2 t3 z')
es = [sp.Matrix([sp.cos(2 * sp.pi * k / 3), sp.sin(2 * sp.pi * k / 3)]) for k in range(3)]
fs = [sp.Matrix([-e[1], e[0]]) for e in es]                 # normals (ccw), sum zero
ts = [t1, t2, t3]
# wall i at height z: f_i . x = t_i z ; three lines concurrent iff augmented 3x3 determinant vanishes
Mx = sp.Matrix([[fs[i][0], fs[i][1], ts[i] * z] for i in range(3)])
dd = sp.factor(sp.simplify(Mx.det()))
print('(a) concurrency determinant of the three wall lines at height z:', dd)
ok &= dd != 0 and sp.simplify(dd.subs(t3, -t1 - t2)) == 0
# ---------------------------------------------------------------- (b) potential and power diagram on a 6x6 torus
s3 = sp.sqrt(3)
def cart(p): return sp.Matrix([sp.Rational(p[0], 2), (sp.Rational(p[0], 6) + sp.Rational(p[1], 3)) * s3])
N = 6
M = (N, 0, N)
R, up, nb = torus_struct(M)
rnd = random.Random(7)
psi = [sp.Rational(rnd.randint(-5, 5), 3) for _ in R]
pos = {}
for n, r in enumerate(R):
    pos[n] = (r[0] * A1[0] + r[1] * A2[0], r[0] * A1[1] + r[1] * A2[1])
# lift of psi to the universal cover: psi(X + period) = psi(X) (periodic potential, no shear)
def cell_at(X):
    q = reduce_mod(coarse(X), M)
    return R.index(q)
lean_c = {}            # Cartesian corner lean at (cell n, corner s) = gradient of psi on the 3 cells round it
bad = 0
for n in range(len(R)):
    X = pos[n]
    for s in range(6):
        P = add(X, D[s])
        Xs = [X, add(X, AC[(s - 1) % 6]), add(X, AC[s])]      # the 3 cells round corner P
        assert all(sum(cart(sub(P, Y)).applyfunc(lambda t: t**2)) == sp.Rational(1, 3) for Y in Xs)
        g = sp.Matrix(sp.symbols('g0 g1'))
        eqs = [(cart(Xs[i]) - cart(Xs[0])).dot(g) - (psi[cell_at(Xs[i])] - psi[cell_at(Xs[0])]) for i in (1, 2)]
        sol = sp.solve(eqs, list(g))
        lean_c[(n, s)] = sp.Matrix([sol[g[0]], sol[g[1]]])
# corner lines agree between the 3 cells (same gradient) and walls are planar
for n in range(len(R)):
    X = pos[n]
    for s in range(6):
        Y = add(X, AC[s])
        m2 = cell_at(Y)
        if (lean_c[(n, s)] - lean_c[(m2, (s + 4) % 6)]).norm() != 0 or \
           (lean_c[(n, (s + 1) % 6)] - lean_c[(m2, (s + 3) % 6)]).norm() != 0:
            bad += 1
        e = cart(D[(s + 2) % 6])
        d = lean_c[(n, (s + 1) % 6)] - lean_c[(n, s)]
        if sp.simplify(d[0] * e[1] - d[1] * e[0]) != 0:
            bad += 1
print(f'(b) random periodic potential on a {N}x{N} torus: corner-line / wall-planarity mismatches: {bad}')
ok &= bad == 0
# cross-section areas: sum over cells of hexagon area at height z == torus area (identity in z); power vertex check
tot = 0
pv_bad = 0
for n in range(len(R)):
    X = pos[n]
    cs = [cart(add(X, D[s])) + z * lean_c[(n, s)] for s in range(6)]
    a = sum(cs[s][0] * cs[(s + 1) % 6][1] - cs[s][1] * cs[(s + 1) % 6][0] for s in range(6)) / 2
    tot += sp.expand(a)
    # power vertex of the three cells round corner 0 with weights w = -2 z psi
    Xs = [X, add(X, AC[5]), add(X, AC[0])]
    x = sp.Matrix(sp.symbols('x0 x1'))
    wgt = [-2 * z * psi[cell_at(Y)] for Y in Xs]
    eqs = [((x - cart(Xs[0])).dot(x - cart(Xs[0])) - wgt[0]) - ((x - cart(Xs[i])).dot(x - cart(Xs[i])) - wgt[i])
           for i in (1, 2)]
    sol = sp.solve([sp.expand(e) for e in eqs], list(x))
    pvx = sp.Matrix([sol[x[0]], sol[x[1]]])
    if sp.simplify((pvx - cs[0]).norm()) != 0:
        pv_bad += 1
torus_area = N * N * 6 * s3 / 12          # N*N cells, each 6 fine triangles of area sqrt3/12
print('    total cross-section area - torus area, as a polynomial in z:', sp.simplify(tot - torus_area))
print(f'    corner positions that are not the power vertex (weights -2 z psi): {pv_bad} of {len(R)}')
ok &= sp.simplify(tot - torus_area) == 0 and pv_bad == 0
# dimension of the closure solution space on the torus: unknown = one tilt per wall, equations = one per corner
walls = {}
for n in range(len(R)):
    for s in range(3):
        walls[(n, s)] = len(walls)
corners = []
for n in range(len(R)):          # each cell owns its corners D_0 (coset 1) and D_1 (coset 2)
    for s in (0, 1):
        # walls round corner X + D_s: wall (n, s-1 dir), wall (n, s dir) and the wall between the two other cells
        corners.append((n, s))
rows = []
def wall_id(n, s):        # wall between cell n and cell at AC[s]; oriented from n to the neighbour
    if s < 3:
        return walls[(n, s)], 1
    m2 = cell_at(add(pos[n], AC[s]))
    return walls[(m2, s - 3)], -1
for (n, s) in corners:
    X = pos[n]
    A_ = n
    B_ = cell_at(add(X, AC[(s - 1) % 6]))
    C_ = cell_at(add(X, AC[s]))
    row = [0] * len(walls)
    # oriented cycle A -> C -> B -> A round the corner: flows (psi differences) must sum to zero
    for (a, sdir) in ((A_, s), (C_, (s + 4) % 6), (B_, (s + 2) % 6)):
        wid, sg = wall_id(a, sdir)
        row[wid] += sg
    rows.append(row)
rk = sp.Matrix(rows).rank()
dim = len(walls) - rk
print(f'    closure equations: {len(walls)} wall tilts, rank {rk}, solution dimension {dim} = (#cells-1)+2 = {len(R)+1}')
ok &= dim == len(R) + 1

# ---------------------------------------------------------------- (c) classification of leaning hexagons
F6, Fm6 = flat_relief(6), flat_relief(-6)
BOX2 = 'box2' in sys.argv          # second run: w0 in {-2..2}^2, lam in {-2..2}^6, tori of index <= 9
RNG = tuple(range(-2, 3)) if BOX2 else (-1, 0, 1)
profiles = {}
for w0 in itertools.product(RNG, repeat=2):
    for lam in itertools.product(RNG, repeat=6):
        w = corner_leans(w0, lam)
        if w is None:
            continue
        P = make(F6, Fm6, w)
        orbit = sorted(place_l(P, g)[2] for g in G_ALL)
        profiles.setdefault(orbit[0], (w0, lam, w))
print(f'(c) leaning hexagons with planar sides in the box: {len(profiles)} classes up to the 24 motions')


def torus_layer(T, nst, M, extra=None):
    from pysat.solvers import Cadical153
    R_, _, nb_ = torus_struct(M)
    m = len(R_)
    v = lambda c, i: c * nst + i + 1
    S = Cadical153()
    for c in range(m):
        S.add_clause([v(c, i) for i in range(nst)])
        for i in range(nst):
            for j in range(i + 1, nst):
                S.add_clause([-v(c, i), -v(c, j)])
    for q in range(m):
        for s in range(6):
            p = nb_[q][s]
            for i in range(nst):
                S.add_clause([-v(q, i)] + [v(p, j) for j in range(nst) if T[s][i] >> j & 1])
    for cl in (extra or []):
        for c_ in cl(v, m):
            S.add_clause(c_)
    r = S.solve()
    mod = None
    if r:
        mset = set(x for x in S.get_model() if x > 0)
        mod = [next(i for i in range(nst) if v(c, i) in mset) for c in range(m)]
    S.delete()
    return r, mod


TORI = [M_ for M_ in hnf(9 if BOX2 else 12)]
rows_out = []
counts = {}
for key, (w0, lam, w) in sorted(profiles.items()):
    P = make(F6, Fm6, w)
    a = hex_area2(w, None)
    shear = all(l == 0 for l in lam)
    rec = {'w0': w0, 'lam': lam, 'w': w, 'area2': a, 'shear': shear}
    for mirrors in (False, True):
        sts, info = states_l([P], mirrors)
        T = inlayer_table(sts)
        n = len(sts)
        solv = []
        mixed_seen = False
        balance_ok = True
        multi_lean = False
        for M_ in TORI:
            r, mod = torus_layer(T, n, M_)
            if r:
                solv.append(M_)
                zs = [info[i][1][2] for i in mod]
                if 0 < sum(zs) < len(zs):
                    mixed_seen = True
                if a[1] != 0 and 2 * sum(zs) != len(zs):
                    balance_ok = False
                # can two cells of a layer carry different corner lines?  (only asked for shears)
                if shear and not multi_lean:
                    lean_classes = {}
                    for i, st in enumerate(sts):
                        lean_classes.setdefault(st[2], []).append(i)
                    if len(lean_classes) > 1 and M_[0] * M_[2] > 1:
                        cls = list(lean_classes.values())
                        for ci, c0 in enumerate(cls):
                            others = [i for k, cc in enumerate(cls) if k != ci for i in cc]
                            def ex(v, m, c0=c0, others=others):   # cell 0 in one lean class, some cell in another
                                return [[v(0, i) for i in c0], [v(q, i) for q in range(1, m) for i in others]]
                            if torus_layer(T, n, M_, [ex])[0]:
                                multi_lean = True
                                break
        # open patch, radius 4
        cells = {}
        for i_ in range(-15, 16):
            for j_ in range(-15, 16):
                p = (i_, j_)
                if coset(p) == 0 and cart2(p) <= 16:
                    cells[p] = len(cells)
        from pysat.solvers import Cadical153
        S = Cadical153()
        vv = lambda c, i: c * n + i + 1
        for c in range(len(cells)):
            S.add_clause([vv(c, i) for i in range(n)])
            for i in range(n):
                for j in range(i + 1, n):
                    S.add_clause([-vv(c, i), -vv(c, j)])
        for p, c in cells.items():
            for s in range(6):
                q = add(p, AC[s])
                if q in cells:
                    for i in range(n):
                        S.add_clause([-vv(c, i)] + [vv(cells[q], j) for j in range(n) if T[s][i] >> j & 1])
        patch_ok = S.solve()
        S.delete()
        rec['mirrors' if mirrors else 'proper'] = {'states': n, 'tori': len(solv), 'patch_R4': patch_ok,
                                                    'mixed': mixed_seen, 'balance_ok': balance_ok,
                                                    'multi_lean_in_layer': multi_lean,
                                                    'first_tori': solv[:6]}
    pr = rec['proper']
    if shear:
        cls = 'P1 shear'
        good = (pr['tori'] > 0) and not pr['multi_lean_in_layer'] and not rec['mirrors']['multi_lean_in_layer']
    elif a[2] != 0:
        cls = 'P3 a2!=0'
        good = pr['tori'] == 0 and rec['mirrors']['tori'] == 0
    elif a[1] == 0:
        cls = 'P2 a1=0'
        good = pr['tori'] == 0 and rec['mirrors']['tori'] == 0
    else:
        cls = 'P4 a1!=0,a2=0'
        good = pr['balance_ok'] and rec['mirrors']['balance_ok']
    rec['class'] = cls
    nz = [i for i in range(6) if lam[i] != 0]
    rec['stripe_type'] = len(nz) == 2 and nz[1] - nz[0] == 3 and lam[nz[0]] == lam[nz[1]]
    rec['prediction_holds'] = good
    ok &= good
    k_ = (cls, pr['tori'] > 0, rec['mirrors']['tori'] > 0)
    counts[k_] = counts.get(k_, 0) + 1
    rows_out.append(rec)
print('    class, layer on some torus (proper), (with mirror copies): count')
for k_, c in sorted(counts.items()):
    print(f'      {k_}: {c}')
print('    P4 classes that fill a layer (w0, lam, 2*area coefficients, tori proper/mirror, patch R4):')
for rec in rows_out:
    if rec['class'].startswith('P4') and (rec['proper']['tori'] or rec['mirrors']['tori']):
        print(f"      w0={rec['w0']} lam={rec['lam']} area2={rec['area2']} tori {rec['proper']['tori']}/"
              f"{rec['mirrors']['tori']} patch {rec['proper']['patch_R4']}/{rec['mirrors']['patch_R4']} "
              f"first tori {rec['proper']['first_tori'] or rec['mirrors']['first_tori']}")
p4f = [r for r in rows_out if r['class'].startswith('P4') and (r['proper']['tori'] or r['mirrors']['tori'])]
print(f'    P4 classes that fill a layer: {len(p4f)}; of stripe type (lam only on one opposite pair of sides): '
      f'{sum(r["stripe_type"] for r in p4f)}')
print('    patch R4 fillable but no torus of index <= 12 (would be a lead):',
      [(r['w0'], r['lam']) for r in rows_out if (r['proper']['patch_R4'] and not r['proper']['tori']) or
       (r['mirrors']['patch_R4'] and not r['mirrors']['tori'])])
json.dump(rows_out, open(__file__.rsplit('/', 2)[0] + ('/data/01_profiles_box2.json' if BOX2 else '/data/01_profiles.json'), 'w'), default=list, indent=0)
print(f'time {time.time()-t0:.1f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a closure identity or a rigidity prediction failed')
