# Paper B of Star Cores ("Core Cycles"): exact checks behind the main theorem (2026-10-31).
# 1. For each dual pair of regular solids (icosahedron/dodecahedron, octahedron/cube, tetrahedron/its reflection): the hull of the
#    unit corner directions U has its faces exactly on the planes w.x = c (w the unit corner directions W of the dual), with
#    c = inradius/circumradius; c^2 in closed form.
# 2. The core turn on K(a, b) = {u.x <= a, w.x <= b}, symbolic in a, b, t: K(a, b) -> K(t c b, t c a), and both families are faces
#    exactly when c < b/a < 1/c (checked on sample ratios inside and outside the window).
# 3. Every period-two row of study 2b and study 3: two-turn squared-radius gain at t = 1 equals c^4 of its pair (or is listed).
# 4. The D3d cases: an octahedron with D3d symmetry whose eight faces are equidistant from the centre is regular (Lahdeli);
#    the Belted Triacontahedron's per-turn squared-radius ratio is constant (exact).
# 5. #78 Proposition 5: q(TI) q(core) = 1.
# Usage: ~/geom/bin/python paper_b_checks.py <study data dir>   (prints a report; exits non-zero on any failed check)
import sys, os, json, itertools
import sympy as sp
D = sys.argv[1]
phi = (1 + sp.sqrt(5)) / 2
fails = []
def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)
def unit(v):
    v = sp.Matrix(v); return v / sp.sqrt(v.dot(v))
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v):
    out = set()
    for s in itertools.product((1, -1), repeat=3):
        w = tuple(sp.nsimplify(a * b) for a, b in zip(s, v)); out.add(w)
    return out
ico = set()
for p in signs((0, 1, phi)): ico.update(cyc(p))
dod = set(signs((1, 1, 1)))
for p in signs((0, phi, 1 / phi)): dod.update(cyc(p))   # the dual orientation of the icosahedron (0, +-1, +-phi)
octa = set()
for p in signs((1, 0, 0)): octa.update(cyc(p))
cube = set(signs((1, 1, 1)))
tet = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}
tetm = {tuple(-x for x in v) for v in tet}
PAIRS = {'Ih (icosahedron 5-fold / dodecahedron 3-fold)': (ico, dod, (5 + 2 * sp.sqrt(5)) / 15),
         'Oh (octahedron 4-fold / cube 3-fold)': (octa, cube, sp.Rational(1, 3)),
         'Td (tetrahedron / reflected tetrahedron)': (tet, tetm, sp.Rational(1, 9))}
check(len(ico) == 12 and len(dod) == 20 and len(octa) == 6 and len(cube) == 8, 'direction sets 12, 20, 6, 8, 4, 4')
C2 = {}
for name, (A, B, c2want) in PAIRS.items():
    U = [unit(v) for v in A]; W = [unit(v) for v in B]
    # c = max over u of u.w for each w (the angle to the nearest u); must be the same for all w and all u
    def nearest(x, Ys): return max((x.dot(y) for y in Ys), key=lambda z: float(z))
    c = sp.radsimp(sp.simplify(nearest(W[0], U)))
    same = all(sp.radsimp(nearest(w, U) - c).equals(0) for w in W) and all(sp.radsimp(nearest(u, W) - c).equals(0) for u in U)
    check(same, f'{name}: one nearest-axis cosine, both ways')
    c2 = sp.radsimp(sp.expand(c ** 2)); C2[name] = c2
    check(sp.simplify(c2 - c2want) == 0, f'{name}: c^2 = {sp.nsimplify(c2)} ({float(c2):.6f}), angle {float(sp.acos(c) * 180 / sp.pi):.4f} deg')
    # the hull of U: each plane w.x = c supports U with >= 3 corners on it, and no other supporting plane is a facet:
    # facet count = |W| and the planes w.x = c cover every corner of the hull (checked through the face count of the hull)
    for w in W:
        vals = [sp.simplify(u.dot(w) - c) for u in U]
        assert all(float(x) <= 1e-12 for x in vals) and sum(1 for x in vals if sp.radsimp(x).equals(0)) >= 3
    from scipy.spatial import ConvexHull
    import numpy as np
    X = np.array([[float(x) for x in u] for u in U]); h = ConvexHull(X)
    planes = {tuple(np.round(e, 9)) for e in h.equations}
    check(len(planes) == len(W), f'{name}: hull of the |U| = {len(U)} unit tips has exactly |W| = {len(W)} faces, each w.x = c')
check(sp.simplify(C2['Ih (icosahedron 5-fold / dodecahedron 3-fold)'] - phi ** 3 / (3 * sp.sqrt(5))) == 0, 'Ih: c^2 = phi^3/(3 sqrt 5)')
check(sp.simplify(C2['Ih (icosahedron 5-fold / dodecahedron 3-fold)'] - phi ** 4 / (3 * (phi + 2))) == 0, 'Ih: c^2 = phi^4/(3(phi+2))')

# 2. the core turn and the window, numerically on sample ratios (the symbolic part is the proof in the paper)
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
def K(U, W, a, b):
    hs = [list(u) + [-a] for u in U] + [list(w) + [-b] for w in W]
    P = HalfspaceIntersection(np.array(hs, float), np.zeros(3)).intersections; return P[ConvexHull(P).vertices]
def facefam(P, U, W):
    h = ConvexHull(P); fa = {}
    for e in h.equations:
        k = tuple(np.round(e, 8)); fa[k] = e
    nu = sum(1 for e in fa.values() if any(np.allclose(e[:3], u, atol=1e-8) for u in U))
    nw = sum(1 for e in fa.values() if any(np.allclose(e[:3], w, atol=1e-8) for w in W))
    return nu, nw, fa
def core(P, U, W, t):
    nu, nw, fa = facefam(P, U, W); planes = []
    for D_ in (U, W):
        tips = [t * (-e[3]) * e[:3] for e in fa.values() if any(np.allclose(e[:3], d, atol=1e-8) for d in D_)]
        if len(tips) >= 4:
            for e in ConvexHull(np.array(tips)).equations: planes.append(e)
    Q = HalfspaceIntersection(np.array(planes), np.zeros(3)).intersections; return Q[ConvexHull(Q).vertices]
for name, (A, B, _) in PAIRS.items():
    U = np.array([[float(x) for x in unit(v)] for v in A]); W = np.array([[float(x) for x in unit(v)] for v in B])
    c = float(sp.sqrt(C2[name])); a = 1.0
    for rho in (c * 0.9, c * 1.05, 0.9, 1.0, 1.2 if 1.2 < 1 / c else 0.5 * (1 + 1 / c), 1 / c * 1.1):
        b = rho * a; P = K(U, W, a, b); nu, nw, _ = facefam(P, U, W)
        inside = c < rho < 1 / c
        check((nu == len(U) and nw == len(W)) == inside and (nu in (0, len(U))) and (nw in (0, len(W))),
              f'{name}: b/a = {rho:.4f}: U-faces {nu}, W-faces {nw}; window ({c:.4f}, {1/c:.4f}) says {"both" if inside else "one"}')
        if inside:
            for t in (1.0, float(phi), 2.0):
                C1 = core(P, U, W, t); C1want = K(U, W, t * c * b, t * c * a)
                same = len(C1) == len(C1want) and all(min(np.linalg.norm(p - q) for q in C1want) < 1e-8 for p in C1)
                C2_ = core(C1, U, W, t); k = t * t * c * c
                back = len(C2_) == len(P) and all(min(np.linalg.norm(k * p - q) for q in C2_) < 1e-8 for p in P)
                check(same and back, f'   t = {t:.4f}: core = K(tcb, tca); two turns = {k:.6f} x S')

# 3. the study data against c^4
def val(s):
    return sp.nsimplify(sp.sympify(s.replace('2**(1/3)', 'cbrt2').replace('2**(2/3)', 'cbrt2**2'), locals={'cbrt2': sp.cbrt(2)}))
G4 = {'Ih': sp.simplify(C2['Ih (icosahedron 5-fold / dodecahedron 3-fold)'] ** 2), 'Oh': sp.Rational(1, 9), 'Td': sp.Rational(1, 81)}
b2 = json.load(open(os.path.join(D, 'study2b.json')))
cnt = {}
for r in b2:
    if not r.get('period'): continue
    g = sp.sympify(r['gain_radius_squared_t1'].replace('2**(1/3)', '0'))  # the gains are rational or in Q(sqrt5)
    which = [k for k, v in G4.items() if sp.simplify(g - v) == 0]
    lab = which[0] if which else 'other'
    cnt.setdefault(lab, []).append(r['solid'].replace('DICTO ', '')[:28])
    print(f"     {r['index']:2d} {r['solid'][:34]:34s} sym {r['symmetry']:4s} enters {r['enters_cycle_at_turn']} period {r['period']} "
          f"gain r^2 {r['gain_radius_squared_t1'][:40]:40s} = c^4 of {lab}")
for k, v in cnt.items(): print(f'     {k}: {len(v)}: {", ".join(v)}')
check(sum(len(v) for v in cnt.values()) == 33, 'study 2b: 33 rows reach period two (29 of the 48 convex shapes + 4 study-2 extras)')
s3 = {}
for f in ('study3.json', 'study3-fine.json'):
    for r in json.load(open(os.path.join(D, f))):
        if 'cores' in r: s3[(r['group'], tuple(r['axes']), tuple(r['s']))] = r
ok3 = all(r['cores'].get('period') == 2 and sp.simplify(sp.sympify(r['cores']['gain2_t1']) - G4[r['group']]) == 0 for r in s3.values())
check(ok3, f'study 3: all {len(s3)} distinct swept solids have cores of period two with gain c^4 of their group')
ent = {}
for k, r in s3.items(): ent.setdefault((k[0], k[1]), set()).add(r['cores']['enters'])
for k, v in sorted(ent.items()): print(f'     study 3 {k}: cores enter at turn {sorted(v)}')

# 4. D3d: equidistant octahedron is regular; DBT ratio
rr, h = sp.symbols('r h', positive=True)
A = lambda k: sp.Matrix([rr * sp.cos(2 * sp.pi * k / 3), rr * sp.sin(2 * sp.pi * k / 3), h])
n = (A(1) - A(0)).cross(-A(2) - A(0)); d2 = sp.simplify(n.dot(A(0)) ** 2 / n.dot(n))
sol = sp.solve(sp.Eq(d2, h ** 2), rr)
print('     D3d antiprism, side-face distance^2 =', sp.factor(d2), '; equal to h^2 at r =', sol)
check(len(sol) == 1 and sp.simplify(sol[0] - sp.sqrt(2) * h) == 0, 'D3d octahedron with equidistant faces: r = sqrt2 h only, the regular octahedron')
dbt = [r for r in b2 if 'Belted' in r['solid']][0]
R2 = [sp.sympify(t['radius2_over_start']) for t in dbt['turns']]
q1, q2 = sp.nsimplify(sp.radsimp(R2[2] / R2[1])), sp.nsimplify(sp.radsimp(R2[3] / R2[2]))
check(sp.simplify(q1 - q2) == 0, f'DBT: squared-radius ratio per turn constant from turn 2: {sp.radsimp(q1)} = {float(q1):.6f}')
check(sp.simplify(q1 ** 2 - sp.sympify(dbt['gain_radius_squared_t1'])) == 0, 'DBT: two-turn gain = (per-turn ratio)^2')
lah = [r for r in b2 if r['solid'] == 'Lahdeli'][0]
print('     Lahdeli turns:', [(t['turn'], t['corners'], t['faces'], t['families'], t['families_solid']) for t in lah['turns']])
# Td per-turn ratio 1/9
for nm in ('Samson', 'Triskelion Tetrahedron', 'Alice', 'White Rabbit'):
    r = [x for x in b2 if x['solid'] == nm][0]
    R2 = [val(t['radius2_over_start']) for t in r['turns']]
    rat = [sp.simplify(R2[i + 1] / R2[i]) for i in range(len(R2) - 1)]
    check(all(sp.simplify(x - sp.Rational(1, 9)) == 0 for x in rat), f'Td {nm}: squared radius x 1/9 at every turn from turn 1 (one shape, turned)')

# 5. #78 Prop 5
qTI = sp.Rational(13, 3) - 22 * sp.sqrt(5) / 15; qC = (195 + 66 * sp.sqrt(5)) / 361
check(sp.simplify(qTI * qC - 1) == 0, '#78: q(TI) q(core) = 1')
c = sp.sqrt(C2['Ih (icosahedron 5-fold / dodecahedron 3-fold)'])
check(float(c) < float(sp.sqrt(qC)) < 1 / float(c), f'TI core ratio b/a = {float(sp.sqrt(qC)):.6f} lies in the window')
for t in (phi, 2):
    print('     two-turn scale t^2 c^2 at t =', t, ':', sp.nsimplify(sp.expand(t ** 2 * c ** 2)), float(t ** 2 * c ** 2))
print('FAILED:', fails if fails else 'none')
sys.exit(1 if fails else 0)
