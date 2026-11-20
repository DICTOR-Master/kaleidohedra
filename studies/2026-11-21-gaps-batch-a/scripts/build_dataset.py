# build_dataset.py -- exact corners of the 5 Platonic (controls), 13 Archimedean and 13 Catalan solids, written in the solids/<slug>.json
# format that census.py (study 2026-11-02-halo-census, copied unchanged) reads, plus exact number-field coordinates for exact_census.py.
# Archimedean: classical coordinate sets (Wikipedia / Coxeter), every one checked exactly: all edges equal, every face a regular polygon,
# the counts V, E, F and faces by sides as in the classical table. Catalan: the polar reciprocal of each Archimedean solid (corners at the
# poles N / (N.p) of its face planes), checked exactly: every face at the same distance from the centre (face-transitive), and V, E, F swapped.
# Fields: Q(sqrt5) (also for the rational solids), Q(sqrt2, sqrt5), Q(t, sqrt5) (snub cube), Q(xi) (snub dodecahedron); all contain sqrt5.
# Usage: python -u build_dataset.py <out dir>   (writes <out>/solids/*.json, <out>/exact.json)       Study 2026-11-21-gaps-batch-a.
import sys, os, json, itertools, time
from fractions import Fraction as Fr
from mpmath import mp, mpf, pslq, findroot
from nf import fields, vsub, vadd, vmul, dot, cross, key
from exactgeo import exact_hull, sides, feet_and_poles
OUT = sys.argv[1]; os.makedirs(os.path.join(OUT, 'solids'), exist_ok=True); T0 = time.time()
Q5, Q25, QT5, QXI = fields()
fails = []
def check(label, ok):
    print(('PASS ' if ok else 'FAIL ') + label, flush=True)
    if not ok: fails.append(label)

def identify(F, value, label):
    """the element of F equal to value (150 digits): PSLQ on 1, theta, ..., theta^(n-1); returned for an exact check by the caller"""
    r = pslq([value] + F.pw, maxcoeff=10 ** 8, maxsteps=10 ** 6, tol=mpf(10) ** -120)
    assert r and r[0] != 0, label
    return F(*[Fr(-r[i + 1], r[0]) for i in range(F.n)])

# generators
r5 = Q5(0, 1); phi5 = (1 + r5) / 2
th = Q25.gen(); r2_25 = (th * th * th - th * 11) / 6; r5_25 = th - r2_25
check('Q(sqrt2, sqrt5): sqrt2^2 = 2 and sqrt5^2 = 5 exactly', r2_25 * r2_25 == Q25(2) and r5_25 * r5_25 == Q25(5))
tt = identify(QT5, findroot(lambda x: x ** 3 - x ** 2 - x - 1, mpf('1.84')), 'tribonacci')
r5_t = QT5.gen() - tt
check('Q(t, sqrt5): t^3 = t^2 + t + 1, sqrt5^2 = 5, t + sqrt5 = theta exactly', tt * tt * tt == tt * tt + tt + 1 and r5_t * r5_t == QT5(5))
xi = QXI.gen(); phi_x = xi * xi * xi - xi * 2
check('Q(xi): phi = xi^3 - 2 xi satisfies phi^2 = phi + 1 exactly', phi_x * phi_x == phi_x + 1)

def orbit(F, base, perm='all', signs='all', zero=None):
    """points from coordinate triples: perm 'all' (6 orders) or 'even' (3 cyclic); signs 'all', 'even+' / 'odd+' (number of plus signs)"""
    out = {}
    P = list(itertools.permutations(range(3))) if perm == 'all' else [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    if perm == 'odd': P = [(1, 0, 2), (0, 2, 1), (2, 1, 0)]
    for v in base:
        for p in P:
            for sg in itertools.product((1, -1), repeat=3):
                if signs == 'even+' and sum(1 for s in sg if s > 0) % 2: continue
                if signs == 'odd+' and sum(1 for s in sg if s > 0) % 2 == 0: continue
                w = [v[p[i]] * sg[i] for i in range(3)]; w = [x if hasattr(x, 'c') else F(x) for x in w]
                out[key(w)] = w
    return list(out.values())

S = []      # (slug, name, family, field, points, expected (V, E, F, faces by sides))
# ---- Platonic (D, I, C, T, O) ----
o, z = Q5(1), Q5(0); p = phi5; ip = p - 1
S.append(('dodecahedron', 'dodecahedron', 'Platonic', Q5, orbit(Q5, [(o, o, o)]) + orbit(Q5, [(z, ip, p)], 'even'), (20, 30, 12, {5: 12})))
S.append(('icosahedron', 'icosahedron', 'Platonic', Q5, orbit(Q5, [(z, o, p)], 'even'), (12, 30, 20, {3: 20})))
S.append(('cube', 'cube', 'Platonic', Q5, orbit(Q5, [(o, o, o)]), (8, 12, 6, {4: 6})))
S.append(('tetrahedron', 'tetrahedron', 'Platonic', Q5, orbit(Q5, [(o, o, o)], 'all', 'odd+'), (4, 6, 4, {3: 4})))
S.append(('octahedron', 'octahedron', 'Platonic', Q5, orbit(Q5, [(o, z, z)]), (6, 12, 8, {3: 8})))
# ---- Archimedean (cubic family, then icosahedral, then snubs) ----
q = lambda *a: tuple(Q5(x) for x in a)
S.append(('truncated-tetrahedron', 'truncated tetrahedron', 'Archimedean', Q5, orbit(Q5, [q(3, 1, 1)], 'all', 'odd+'), (12, 18, 8, {3: 4, 6: 4})))
S.append(('cuboctahedron', 'cuboctahedron', 'Archimedean', Q5, orbit(Q5, [q(1, 1, 0)]), (12, 24, 14, {3: 8, 4: 6})))
S.append(('truncated-octahedron', 'truncated octahedron', 'Archimedean', Q5, orbit(Q5, [q(0, 1, 2)]), (24, 36, 14, {4: 6, 6: 8})))
o2, z2, s2 = Q25(1), Q25(0), r2_25
S.append(('truncated-cube', 'truncated cube', 'Archimedean', Q25, orbit(Q25, [(s2 - 1, o2, o2)]), (24, 36, 14, {3: 8, 8: 6})))
S.append(('rhombicuboctahedron', 'rhombicuboctahedron', 'Archimedean', Q25, orbit(Q25, [(o2, o2, 1 + s2)]), (24, 48, 26, {3: 8, 4: 18})))
S.append(('truncated-cuboctahedron', 'truncated cuboctahedron', 'Archimedean', Q25, orbit(Q25, [(o2, 1 + s2, 1 + 2 * s2)]), (48, 72, 26, {4: 12, 6: 8, 8: 6})))
S.append(('icosidodecahedron', 'icosidodecahedron', 'Archimedean', Q5, orbit(Q5, [(z, z, p)], 'even') + orbit(Q5, [(Q5(Fr(1, 2)), p / 2, p * p / 2)], 'even'), (30, 60, 32, {3: 20, 5: 12})))
S.append(('truncated-icosahedron', 'truncated icosahedron', 'Archimedean', Q5, orbit(Q5, [(z, o, 3 * p), (o, 2 + p, 2 * p), (p, Q5(2), p * p * p)], 'even'), (60, 90, 32, {5: 12, 6: 20})))
S.append(('truncated-dodecahedron', 'truncated dodecahedron', 'Archimedean', Q5, orbit(Q5, [(z, ip, 2 + p), (ip, p, 2 * p), (p, Q5(2), p + 1)], 'even'), (60, 90, 32, {3: 20, 10: 12})))
S.append(('rhombicosidodecahedron', 'rhombicosidodecahedron', 'Archimedean', Q5, orbit(Q5, [(o, o, p * p * p), (p * p, p, 2 * p), (2 + p, z, p * p)], 'even'), (60, 120, 62, {3: 20, 4: 30, 5: 12})))
S.append(('truncated-icosidodecahedron', 'truncated icosidodecahedron', 'Archimedean', Q5, orbit(Q5, [(ip, ip, 3 + p), (2 * ip, p, 1 + 2 * p), (ip, p * p, 3 * p - 1), (2 * p - 1, Q5(2), 2 + p), (p, Q5(3), 2 * p)], 'even'), (120, 180, 62, {4: 30, 6: 20, 10: 12})))
it = 1 / tt; ot = QT5(1)
S.append(('snub-cube', 'snub cube', 'Archimedean', QT5, orbit(QT5, [(ot, it, tt)], 'even', 'even+') + orbit(QT5, [(ot, it, tt)], 'odd', 'odd+'), (24, 60, 38, {3: 32, 4: 6})))
def snub_dodecahedron():
    """the snub dodecahedron as one orbit of the icosahedral rotation group (60 exact matrices in Q(phi), closed exactly), through a point v
    found numerically (equal edges round v), refined to 150 digits, and identified in Q(xi) by PSLQ on the scale-free ratios; the caller
    then checks every claim exactly"""
    import numpy as np
    from scipy.optimize import minimize
    from mpmath import matrix as mmat
    o_, z_, h_ = QXI(1), QXI(0), QXI(Fr(1, 2)); P_ = phi_x
    gens = [[[z_, z_, o_], [o_, z_, z_], [z_, o_, z_]], [[o_, z_, z_], [z_, -o_, z_], [z_, z_, -o_]],
            [[h_, -P_ * h_, (P_ - 1) * h_], [P_ * h_, (P_ - 1) * h_, -h_], [(P_ - 1) * h_, h_, P_ * h_]]]
    def mm(A, B): return [[sum((A[i][k] * B[k][j] for k in range(3)), QXI(0)) for j in range(3)] for i in range(3)]
    kk = lambda A: tuple(x.c for r in A for x in r)
    I3 = [[o_, z_, z_], [z_, o_, z_], [z_, z_, o_]]; G = {kk(I3): I3}; fr = [I3]
    while fr:
        nx = []
        for A in fr:
            for g in gens:
                B = mm(g, A)
                if kk(B) not in G: G[kk(B)] = B; nx.append(B)
        fr = nx
    G = list(G.values())
    ok = len(G) == 60 and all(mm([[A[j][i] for j in range(3)] for i in range(3)], A) == I3 for A in G)
    check('icosahedral rotation group: 60 matrices, all orthogonal (exact, Q(phi))', ok)
    Gf = [np.array([[float(x) for x in r] for r in A]) for A in G]
    def pts(v): return np.array([g @ v for g in Gf])
    def obj(a):
        v = np.array([np.sin(a[0]) * np.cos(a[1]), np.sin(a[0]) * np.sin(a[1]), np.cos(a[0])]); d = np.sort(np.linalg.norm(pts(v)[1:] - v, axis=1))
        return np.var(d[:5]) / d[0] ** 2 + (0 if d[0] > 1e-3 else 1)
    rng = np.random.default_rng(1); best = None
    for _ in range(200):
        r = minimize(obj, rng.uniform(0, np.pi, 2) * [1, 2], method='Nelder-Mead', options=dict(xatol=1e-13, fatol=1e-20, maxiter=4000))
        if r.fun < 1e-14:
            v = np.array([np.sin(r.x[0]) * np.cos(r.x[1]), np.sin(r.x[0]) * np.sin(r.x[1]), np.cos(r.x[0])])
            Pv = pts(v)
            if len(np.unique(np.round(Pv, 8), axis=0)) == 60: best = v; break
    assert best is not None
    d = np.linalg.norm(pts(best) - best, axis=1); five = list(np.argsort(d)[1:6])
    # |v - g v| = |v - g^-1 v| always, so take one rotation from each inverse pair (three distinct classes: about the pentagon's axis,
    # a triangle's axis and an edge's axis), else the equations are degenerate
    nb = []
    for k in five:
        if not any(np.allclose(Gf[k] @ Gf[j], np.eye(3), atol=1e-9) for j in nb): nb.append(k)
    assert len(nb) == 3, nb
    Gm = [mmat([[x.mp() for x in r] for r in G[k]]) for k in nb]
    def eqs(x, y, zz):
        v = mmat([x, y, zz]); dd = [sum((v - g * v)[i] ** 2 for i in range(3)) for g in Gm]
        return [x * x + y * y + zz * zz - 1, dd[0] - dd[1], dd[0] - dd[2]]
    sol = findroot(eqs, [mpf(float(c)) for c in best])
    k0 = max(range(3), key=lambda i: abs(sol[i]))
    v = [QXI(1) if i == k0 else identify(QXI, sol[i] / sol[k0], 'snub ratio') for i in range(3)]
    V = {}
    for A in G:
        w = [sum((A[i][j] * v[j] for j in range(3)), QXI(0)) for i in range(3)]; V[key(w)] = w
    return list(V.values())
S.append(('snub-dodecahedron', 'snub dodecahedron', 'Archimedean', QXI, snub_dodecahedron(), (60, 150, 92, {3: 80, 5: 12})))

def edges_of(F_):
    return {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in F_ for k in range(len(f))}
def fmt5(x):
    """Q(sqrt5) element as a string census.py parses"""
    a, b = x.c; return f'({a}) + ({b})*sqrt(5)'
exact_out = {}; rows = []
def emit(slug, name, family, F, V, faces, extra):
    d = dict(name=name, family=family, field='Q(sqrt(5))' if F is Q5 else F.name, convex=True,
             vertices=[dict(decimal=[repr(float(x)) for x in v], **({'exact': [fmt5(x) for x in v]} if F is Q5 else {})) for v in V],
             faces=faces, source='study 2026-11-21-gaps-batch-a, scripts/build_dataset.py (exact, checked)', **extra)
    json.dump(d, open(os.path.join(OUT, 'solids', slug + '.json'), 'w'), indent=0)
    exact_out[slug] = dict(name=name, family=family, field=F.name, coords=[[[str(c) for c in x.c] for x in v] for v in V], faces=faces)

DUAL = {'tetrahedron': 'tetrahedron', 'cube': 'octahedron', 'octahedron': 'cube', 'dodecahedron': 'icosahedron', 'icosahedron': 'dodecahedron',
        'truncated-tetrahedron': 'triakis tetrahedron', 'cuboctahedron': 'rhombic dodecahedron', 'truncated-octahedron': 'tetrakis hexahedron',
        'truncated-cube': 'triakis octahedron', 'rhombicuboctahedron': 'deltoidal icositetrahedron', 'truncated-cuboctahedron': 'disdyakis dodecahedron',
        'icosidodecahedron': 'rhombic triacontahedron', 'truncated-icosahedron': 'pentakis dodecahedron', 'truncated-dodecahedron': 'triakis icosahedron',
        'rhombicosidodecahedron': 'deltoidal hexecontahedron', 'truncated-icosidodecahedron': 'disdyakis triacontahedron',
        'snub-cube': 'pentagonal icositetrahedron', 'snub-dodecahedron': 'pentagonal hexecontahedron'}
for slug, name, family, F, V, (nV, nE, nF, fs) in S:
    faces, ok = exact_hull(V)
    E_ = edges_of(faces); L = [dot(vsub(V[a], V[b]), vsub(V[a], V[b])) for a, b in E_]
    reg = all(x == L[0] for x in L)
    corners = sorted({i for f in faces for i in f})
    check(f'{name} [{F.name}]: exact hull ok, V {len(corners)}/{nV}, E {len(E_)}/{nE}, F {len(faces)}/{nF}, faces by sides {sides(faces)}, all edges equal exactly ({len(L)}), {round(time.time() - T0)} s',
          ok and len(corners) == nV == len(V) and len(E_) == nE and len(faces) == nF and sides(faces) == fs and reg)
    emit(slug, name, family, F, V, faces, dict(edge2=[str(c) for c in L[0].c]))
    if family == 'Archimedean':
        feet, poles = feet_and_poles(V, faces)
        CF, ok2 = exact_hull(poles)
        cc = sorted({i for f in CF for i in f})
        # face-transitive: every face plane of the polar at the same distance (its poles are the old corners, at one radius)
        _, poles2 = feet_and_poles(poles, CF); r2 = [dot(x, x) for x in poles2]
        dn = DUAL[slug]
        check(f'  polar = {dn}: exact hull ok, V {len(cc)}/{nF}, F {len(CF)}/{nV}, all faces at one distance from the centre (exact)',
              ok2 and len(cc) == nF == len(poles) and len(CF) == nV and all(x == r2[0] for x in r2))
        emit(dn.replace(' ', '-'), dn, 'Catalan', F, poles, CF, dict(dual_of=name))
        rows.append((name, dn))
json.dump(exact_out, open(os.path.join(OUT, 'exact.json'), 'w'))
print('solids written:', len(exact_out), 'pairs', len(rows))
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
